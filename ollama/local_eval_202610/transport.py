"""Local streaming receipts with a wall-clock deadline and residency samples."""
import json
import queue
import socket
import threading
import time
import urllib.request
from urllib.parse import urlparse

from ollama import run_benchmark as rb


def local_url(url):
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("runtime must use a loopback HTTP URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("runtime URL must not contain credentials/query/fragment")
    return url.rstrip("/")


def get_json(url, payload=None, timeout=10):
    request = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def identity(backend, url, model, supplied=None):
    if backend == "openai":
        required = ("digest", "quantization", "runtime", "version", "template", "reasoning_mode",
                    "declared_context_length", "full_offload", "loader")
        if not supplied or any(key not in supplied for key in required):
            raise ValueError(f"OpenAI identity requires fields: {required}")
        if supplied.get("model") != model or supplied.get("url") != url:
            raise ValueError("OpenAI identity model/url mismatch")
        if supplied["full_offload"] is not True:
            raise ValueError("OpenAI full-offload qualification missing")
        return supplied
    tags = get_json(url + "/api/tags")
    entries = [entry for entry in tags.get("models", []) if entry.get("name") in rb._tag_variants(model)]
    if len(entries) != 1 or not entries[0].get("digest"):
        raise ValueError("model identity absent or ambiguous in same-server tags")
    show = get_json(url + "/api/show", {"model": model})
    if not show.get("template") or not show.get("model_info"):
        raise ValueError("same-server template/model_info incomplete")
    # Existing helper caches by tag only: clear to prevent cross-server ceiling reuse.
    rb._DECLARED_CONTEXT_LENGTH_CACHE.pop(model, None)
    ceiling = rb.fetch_declared_context_length(model, tags_url=url + "/api/tags", show_url=url + "/api/show")
    return {"model": model, "url": url, "digest": entries[0]["digest"], "tags_entry": entries[0],
            "show": show, "version": get_json(url + "/api/version"),
            "reasoning_mode": "runtime default", "declared_context_length": ceiling}


def payload(backend, model, prompt, options, probe=False):
    budget = 1 if probe else options["num_predict"]
    if backend == "ollama":
        return {"model": model, **prompt, "stream": True, "keep_alive": "15m",
                "options": {**options, "num_predict": budget}}
    return {"model": model, "messages": [{"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["prompt"]}], "stream": True,
            "stream_options": {"include_usage": True}, "temperature": options["temperature"],
            "max_tokens": budget}


def resident_models(snapshot):
    """Malformed occupancy evidence must never be interpreted as idle."""
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("models"), list):
        raise ValueError("malformed residency: expected an object with a models list")
    models = snapshot["models"]
    for item in models:
        if not isinstance(item, dict) or not isinstance(item.get("name", item.get("model")), str) or not item.get("name", item.get("model")):
            raise ValueError("malformed residency: model entry requires a nonempty name")
    return models


def residency(url, shared, backend, model, until=None):
    def remaining():
        if until is None:
            return 10
        available = until - time.monotonic()
        if available <= 0:
            raise TimeoutError("total attempt deadline exceeded during residency")
        return min(10, available)
    snapshots = {"shared": get_json(shared + "/api/ps", timeout=remaining())}
    if backend == "ollama":
        snapshots["own"] = get_json(url + "/api/ps", timeout=remaining())
    shared_busy = bool(resident_models(snapshots["shared"]))
    own = resident_models(snapshots["own"]) if backend == "ollama" else []
    foreign = any(item.get("name", item.get("model")) not in rb._tag_variants(model) for item in own)
    return snapshots, shared_busy or foreign


def stream(url, shared, backend, model, request_payload, receipt, deadline=1800):
    """Main thread bounds the entire request, including a silent blocked reader."""
    events = queue.Queue()
    stopped = threading.Event()
    active = {}
    start = time.monotonic()
    endpoint = "/api/generate" if backend == "ollama" else "/v1/chat/completions"
    def reader():
        try:
            request = urllib.request.Request(url + endpoint, data=json.dumps(request_payload).encode(),
                                             headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=max(.001, deadline - (time.monotonic() - start))) as response:
                active["response"] = response
                for line in response:
                    if stopped.is_set():
                        break
                    events.put(("raw", line.decode("utf-8")))
            events.put(("eof", None))
        except Exception as error:
            events.put(("exception", f"{type(error).__name__}: {error}"))
    result = {"response": "", "thinking": "", "terminal": None, "exception": None,
              "contaminated": False, "snapshots": [], "elapsed_seconds": 0}
    def record(kind, value):
        receipt.write(json.dumps({"elapsed_seconds": time.monotonic() - start,
                                  "kind": kind, "value": value}) + "\n")
        receipt.flush()
    record("request", request_payload)
    threading.Thread(target=reader, daemon=True).start()
    next_sample = start
    while True:
        now = time.monotonic()
        if now - start >= deadline:
            result["exception"] = "total attempt deadline exceeded"
            record("exception", result["exception"])
            break
        if now >= next_sample:
            try:
                snapshots, contaminated = residency(url, shared, backend, model, until=start + deadline)
                result["snapshots"].append(snapshots)
                result["contaminated"] |= contaminated
                record("residency", snapshots)
            except Exception as error:
                result["exception"] = f"residency monitoring failed: {error}"
                record("exception", result["exception"])
                break
            next_sample = time.monotonic() + 5
        try:
            kind, value = events.get(timeout=min(1, max(.001, deadline - (time.monotonic() - start))))
        except queue.Empty:
            continue
        record(kind, value)
        if kind == "exception":
            result["exception"] = value
            break
        if kind == "eof":
            if result["terminal"] is None:
                result["exception"] = "EOF without final termination metadata"
            break
        try:
            consume(backend, value, result)
        except Exception as error:
            result["exception"] = f"stream parse error: {error}"
            record("exception", result["exception"])
            break
    stopped.set()
    if result["exception"] and active.get("response") is not None:
        # Cancel only this request's connection; never unload a runtime/model.
        try:
            active["response"].fp.raw._sock.shutdown(socket.SHUT_RDWR)
        except (AttributeError, OSError):
            pass
    try:
        snapshots, contaminated = residency(url, shared, backend, model, until=start + deadline)
        result["snapshots"].append(snapshots)
        result["contaminated"] |= contaminated
        record("after_residency", snapshots)
    except Exception as error:
        result["exception"] = f"after residency failed: {error}"
        record("exception", result["exception"])
    result["elapsed_seconds"] = time.monotonic() - start
    record("outcome", result)
    return result


def consume(backend, raw, result):
    raw = raw.strip()
    if not raw or (backend == "openai" and raw.startswith(": ")):
        return
    if backend == "openai":
        if not raw.startswith("data:"):
            return
        raw = raw[5:].strip()
        if raw == "[DONE]":
            return
    item = json.loads(raw)
    if item.get("error"):
        raise ValueError(item["error"])
    if backend == "ollama":
        result["response"] += item.get("response", "")
        result["thinking"] += item.get("thinking", "")
        if item.get("done") is True:
            result["terminal"] = item
        return
    if item.get("usage"):
        result["usage"] = item["usage"]
    if item.get("timings"):
        result["timings"] = item["timings"]
    for choice in item.get("choices", []):
        if choice.get("index", 0) != 0:
            raise ValueError("unexpected multiple choice stream")
        delta = choice.get("delta", {})
        result["response"] += delta.get("content") or ""
        result["thinking"] += delta.get("reasoning_content") or delta.get("thinking") or ""
        if choice.get("finish_reason"):
            result["terminal"] = choice
