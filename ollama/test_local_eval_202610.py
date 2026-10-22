"""Offline protocol checks; never contact a model runtime."""
import io
import json
import tempfile
import unittest
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ollama.local_eval_202610 import freeze as fr, runner as rr, transport as tr


def attempt(text="Verdict: ACCEPT", reason="stop", **extra):
    return {"response": text, "terminal": {"done_reason": reason}, "exception": None,
            "contaminated": False, **extra}


class ProtocolTests(unittest.TestCase):
    def test_neutralization_blind_and_features(self):
        text = "# Fixture: CLEAN\n\n## Component Code\nkeep\n## Accessibility Features Present\nleak\n## Expected Behavior\nkeep2\n## Accessibility Issues\nanswer"
        clean = fr.neutralize(text)
        self.assertTrue(clean.startswith("# Component under review\n"))
        self.assertIn("keep2", clean)
        for forbidden in ("CLEAN", "leak", "answer"):
            self.assertNotIn(forbidden, clean)
        self.assertIn("keep", fr.neutralize("# Heading\nkeep"))
        with self.assertRaises(ValueError):
            fr.neutralize("# Heading\n## Accessibility Features Present\nx\n## Next\ny\n## Accessibility Features Implemented\nz")
        with self.assertRaises(ValueError):
            fr.neutralize("no heading")

    def test_wrong_source(self):
        with patch.object(fr.subprocess, "check_output", return_value="wrong"):
            with self.assertRaisesRegex(ValueError, "wrong source"):
                fr.source_guard()

    def test_freeze_real_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            self.assertEqual(len(manifest["screen"]), 10)
            self.assertEqual(len(manifest["clean"]), 4)
            self.assertEqual(len(manifest["bugreport"]), 7)
            self.assertEqual(fr.verify(directory), manifest)
            with self.assertRaises(FileExistsError):
                fr.freeze(directory)
            prompt = Path(directory) / "freeze/prompts/critic/button-skip-link-clean.json"
            self.assertNotIn("fixture_id", json.loads(prompt.read_text()))
            prompt.write_text("tampered")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                fr.verify(directory)

    def test_strict_verdict_and_noanswer(self):
        for text in ("I would ACCEPT this", "Please provide context REVISE", "Verdict: ACCEPT\nVerdict: REJECT", "Verdict: ACCEPT-WITH-UNKNOWN"):
            row = rr.evaluate_attempts([attempt(text)], "critic")
            self.assertEqual(row["status"], "NON_EXECUTION")
            self.assertEqual(row["detection_credit"], 0)
        for text in ("**Verdict:** **ACCEPT**", "### Verdict: REVISE", "Verdict: ACCEPT-WITH-RESERVATIONS", "Verdict: REVISE — association missing"):
            self.assertEqual(rr.eligibility(attempt(text), "critic")[0], "EXECUTED")

    def test_termination_and_retry(self):
        for row in (attempt(reason="length"), attempt(exception="failure"), attempt(terminal=None), attempt("<think>unfinished")):
            self.assertEqual(rr.eligibility(row, "critic")[0], "NON_EXECUTION")
            self.assertNotEqual(rr.eligibility(row, "critic")[1], "empty")
        row = rr.evaluate_attempts([attempt(""), attempt()], "critic")
        self.assertFalse(row["first_attempt_completed"])
        self.assertTrue(row["retry_assisted_completed"])
        self.assertEqual(row["selected_attempt"], 2)
        self.assertEqual(rr.eligibility(attempt(contaminated=True), "critic")[0], "INVALID")
        self.assertEqual(rr.eligibility(attempt("I need a scan"), "bugreport")[0], "NON_EXECUTION")
        self.assertEqual(rr.eligibility(attempt("# Accessibility issue (WCAG 1.1.1)\nreport"), "bugreport")[0], "NON_EXECUTION")

    def report(self, snippet="```html\n<img src='x'>\n```", absent=False):
        values = ("Not provided" if absent else "actual value")
        return "## Accessibility Issue: Image\n" + "\n".join(
            f"**{label}:** {values}" for label in rr.sb.REQUIRED_LABELS
        ) + "\n### HTML Snippet\n" + snippet

    def test_bugreport_requires_nonempty_fields_in_every_block(self):
        canonical = self.report()
        for text in ("## Accessibility Issue: Image", "URL:\nXPath:\nRule:\n",
                     canonical.replace("**XPath:** actual value", "**XPath:**"),
                     canonical + "\n## Accessibility Issue: second\nURL: value"):
            with self.subTest(text=text):
                self.assertEqual(rr.eligibility(attempt(text), "bugreport")[0], "NON_EXECUTION")
        self.assertEqual(rr.eligibility(attempt(canonical), "bugreport")[0], "EXECUTED")
        self.assertEqual(rr.eligibility(attempt(canonical + "\n" + canonical), "bugreport")[0], "EXECUTED")
        # Exact values, IDs, expected count and citations remain correctness dimensions.
        self.assertEqual(rr.eligibility(attempt(self.report(absent=True)), "bugreport")[0], "EXECUTED")

    def test_bugreport_requires_html_content_or_honest_absence(self):
        for snippet in ("", "```html\n\n```", "Please supply source."):
            self.assertEqual(rr.eligibility(attempt(self.report(snippet)), "bugreport")[0], "NON_EXECUTION")
        for snippet in ("HTML not provided in the scan.", "`<img src='x'>`"):
            self.assertEqual(rr.eligibility(attempt(self.report(snippet, absent=True)), "bugreport")[0], "EXECUTED")
        shell = self.report().replace("**URL:** actual value", "| URL | |")
        self.assertEqual(rr.eligibility(attempt(shell), "bugreport")[0], "NON_EXECUTION")

    def test_residency_rejects_malformed_shared_and_own(self):
        valid = {"models": []}
        for malformed in ({}, {"models": None}, {"models": {}}, [], {"models": [None]}, {"models": [{}]}):
            for responses in ([malformed, valid], [valid, malformed]):
                with self.subTest(responses=responses), patch.object(tr, "get_json", side_effect=responses):
                    with self.assertRaisesRegex(ValueError, "residency"):
                        tr.residency("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m")
        with patch.object(tr, "get_json", return_value=valid):
            self.assertEqual(tr.residency("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m")[1], False)
        with patch.object(tr, "get_json", return_value={}):
            with self.assertRaisesRegex(ValueError, "residency"):
                tr.residency("http://127.0.0.1:2", "http://127.0.0.1:1", "openai", "m")

    def test_offload_requires_evidence_for_each_sample_and_final(self):
        loaded = {"own": {"models": [{"name": "m", "size": 100, "size_vram": 100}]}}
        for missing in ({}, {"own": {}}, {"own": {"models": []}},
                        {"own": {"models": [{"name": "other", "size": 100, "size_vram": 100}]}}):
            for snaps in ([missing, loaded], [loaded, missing], [loaded, missing, loaded]):
                self.assertFalse(rr.offload_verified(attempt(snapshots=snaps), "m"))
        self.assertTrue(rr.offload_verified(attempt(snapshots=[loaded, loaded]), "m"))
        cold = {"own": {"models": []}}
        probe = attempt(snapshots=[cold, loaded])
        self.assertIsNone(rr.qualify_probe(probe, 42, "ollama", "m", rr.OPTIONS))
        for snaps in ([{}, loaded], [loaded, cold], [cold], [cold, loaded, cold, loaded]):
            self.assertIsNotNone(rr.qualify_probe(attempt(snapshots=snaps), 42, "ollama", "m", rr.OPTIONS))

    def test_scored_admission_requires_current_own_offload(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            args = SimpleNamespace(out=directory, url="http://127.0.0.1:2", shared_url="http://127.0.0.1:1",
                                   backend="ollama", model="m", num_predict=16384, identity_file=None, stage="screen", draws=3)
            loaded = {"own": {"models": [{"name": "m", "size": 100, "size_vram": 100}]}}
            def streamed(*values):
                values[-1].write("raw\n")
                return attempt("", reason="length", terminal={"done_reason": "length", "prompt_eval_count": 100}, snapshots=[loaded])
            for bad in ({}, {"own": {"models": []}}, {"own": {"models": [{"name": "m", "size": 100, "size_vram": 10}]}}):
                with self.subTest(bad=bad), tempfile.TemporaryDirectory() as lane:
                    fr.freeze(lane)
                    args.out = lane
                    with patch.object(tr, "identity", return_value={"declared_context_length": 32768}), patch.object(tr, "residency", side_effect=[({}, False), ({}, False), (bad, False)]), patch.object(tr, "stream", side_effect=streamed) as stream, patch.object(rr, "cells", return_value=[("critic", manifest["screen"][0], 1)]):
                        with self.assertRaisesRegex(ValueError, "offload"):
                            rr.run(args)
                        self.assertEqual(stream.call_count, 1, "only the cold-capable probe may run")
                    self.assertTrue(list(Path(lane).glob("runs/*/*-blocked-*.json")))

    def test_stream_rejects_missing_residency_during_and_after(self):
        class Response(io.BytesIO):
            pass
        loaded = {"models": [{"name": "m", "size": 100, "size_vram": 100}]}
        valid = {"models": []}
        for responses in ([{}, loaded, valid, loaded], [valid, loaded, valid, {}]):
            with self.subTest(responses=responses), patch.object(tr, "get_json", side_effect=responses), patch.object(tr.urllib.request, "urlopen", return_value=Response(b'{"response":"Verdict: ACCEPT","done":true,"done_reason":"stop"}\n')):
                receipt = io.StringIO()
                result = tr.stream("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m", {}, receipt, deadline=1)
                self.assertIn("residency", result["exception"])
                self.assertEqual(rr.eligibility(result, "critic")[0], "NON_EXECUTION")
                self.assertIn('"kind": "exception"', receipt.getvalue())
                self.assertIn('"kind": "outcome"', receipt.getvalue())

    def test_inline_html_absence_is_structure_not_correctness(self):
        text = self.report().split("### HTML Snippet")[0] + "**HTML Snippet:** Not provided in scan"
        self.assertEqual(rr.eligibility(attempt(text), "bugreport")[0], "EXECUTED")

    def test_freeze_captures_and_rechecks_all_executable_modules(self):
        original = Path.read_bytes
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            for name in ("__init__.py", "__main__.py", "freeze.py", "runner.py", "transport.py"):
                key = f"sources/local_eval_202610/{name}"
                self.assertIn(key, manifest["files"])
                live = fr.ROOT / "ollama/local_eval_202610" / name
                self.assertEqual((Path(directory) / "freeze" / key).read_bytes(), live.read_bytes())
                def tampered(path, live=live):
                    return original(path) + b"\n# tampered\n" if path == live else original(path)
                with patch.object(Path, "read_bytes", tampered):
                    with self.assertRaisesRegex(ValueError, "live supplemental"):
                        fr.verify(directory)
                    with self.assertRaisesRegex(ValueError, "live supplemental"):
                        rr.summary(directory)
                    with self.assertRaisesRegex(ValueError, "live supplemental"), patch.object(tr, "identity") as identity:
                        rr.run(SimpleNamespace(out=directory))
                    identity.assert_not_called()

    def test_payload_stateless_and_identity(self):
        prompt = {"system": "skill", "prompt": "input"}
        payload = tr.payload("ollama", "model", prompt, rr.OPTIONS)
        self.assertEqual(set(payload), {"model", "system", "prompt", "stream", "keep_alive", "options"})
        self.assertNotIn("seed", payload["options"])
        self.assertEqual(tr.payload("ollama", "m", prompt, rr.OPTIONS, True)["options"]["num_predict"], 1)
        self.assertEqual(len(tr.payload("openai", "m", prompt, rr.OPTIONS)["messages"]), 2)
        with self.assertRaises(ValueError):
            tr.identity("openai", "http://127.0.0.1:1", "m", {})
        for url in ("https://example.com", "http://user:secret@127.0.0.1", "http://127.0.0.1?x=y"):
            with self.assertRaises(ValueError):
                tr.local_url(url)

    def test_stream_parse_reasoning_and_usage(self):
        result = {"response": "", "thinking": "", "terminal": None}
        tr.consume("ollama", '{"thinking":"hmm","response":"hi","done":true,"done_reason":"stop"}', result)
        self.assertEqual(result["thinking"], "hmm")
        result = {"response": "", "thinking": "", "terminal": None}
        tr.consume("openai", 'data: {"choices":[{"index":0,"delta":{"content":"hi","reasoning_content":"hmm"},"finish_reason":"stop"}],"usage":{"prompt_tokens":7}}', result)
        tr.consume("openai", "data: [DONE]", result)
        tr.consume("openai", ": ping", result)
        self.assertEqual(result["usage"]["prompt_tokens"], 7)
        self.assertEqual(result["thinking"], "hmm")
        with self.assertRaises(ValueError):
            tr.consume("ollama", '{"error":"bad"}', result)

    def test_stream_allows_prefill_until_total_deadline(self):
        raw = io.BytesIO(b'{"response":"ok","done":true,"done_reason":"stop"}\n')
        with patch.object(tr.urllib.request, "urlopen", return_value=raw) as opening, patch.object(tr, "residency", return_value=({}, False)):
            result = tr.stream("http://127.0.0.1:1", "http://127.0.0.1:2", "ollama", "m", {}, io.StringIO(), deadline=20)
        self.assertIsNone(result["exception"])
        self.assertGreater(opening.call_args.kwargs["timeout"], 10)
        self.assertLessEqual(opening.call_args.kwargs["timeout"], 20)

    def test_probe(self):
        probe = attempt(snapshots=[{"own": {"models": [{"name": "m", "size": 100, "size_vram": 100}]}}])
        self.assertIsNone(rr.qualify_probe(probe, 42, "ollama", "m", rr.OPTIONS))
        for count in (None, 0, 32768):
            self.assertIsNotNone(rr.qualify_probe(probe, count, "ollama", "m", rr.OPTIONS))
        probe["snapshots"][0]["own"]["models"][0]["size_vram"] = 10
        self.assertIn("offload", rr.qualify_probe(probe, 42, "ollama", "m", rr.OPTIONS))

    def test_hash_resume_missing_and_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cell.json"
            receipt = Path(directory) / "receipt.ndjson"
            fr.exclusive(receipt, b"raw")
            contract = {"hash": "original"}
            fr.exclusive(path, {"contract": contract, "outcome": {"status": "EXECUTED"},
                                "attempts": [{"receipt": receipt.name, "sha256": fr.digest(b"raw")}]})
            fr.exclusive(path.with_suffix(".sha256"), (fr.digest(path.read_bytes()) + "\n").encode())
            self.assertEqual(rr.validate_resume(path, contract)["outcome"]["status"], "EXECUTED")
            with self.assertRaisesRegex(ValueError, "resume mismatch"):
                rr.validate_resume(path, {"hash": "changed"})
            with self.assertRaises(FileExistsError):
                fr.exclusive(path, {})
            receipt.write_text("edited")
            with self.assertRaisesRegex(ValueError, "receipt hash"):
                rr.validate_resume(path, contract)

    def test_stream_eof_error_contamination_deadline(self):
        class Response:
            def __init__(self, lines):
                self.lines = lines
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def __iter__(self):
                return iter(self.lines)
        for lines, busy, expected in [
            ([b'{"response":"partial"}\n'], False, "EOF"),
            ([b'{"response":"Verdict: ACCEPT","done":true,"done_reason":"stop"}\n'], True, None),
            ([b'not-json\n'], False, "parse"),
        ]:
            with patch.object(tr.urllib.request, "urlopen", return_value=Response(lines)), patch.object(tr, "residency", return_value=({}, busy)):
                receipt = io.StringIO()
                result = tr.stream("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m", {}, receipt, deadline=1)
            if expected:
                self.assertIn(expected, result["exception"])
            self.assertEqual(result["contaminated"], busy)
            self.assertIn('"kind": "request"', receipt.getvalue())

    def test_repeated_draw_denominators(self):
        manifest = {"clean": ["a", "b"], "screen": ["a"]}
        cells = rr.cells(manifest, "clean", 3)
        self.assertEqual(len(cells), 6)
        self.assertEqual(len({cell[1] for cell in cells}), 2)

    def test_mocked_run_resume_summary_and_retry_policy(self):
        runtime = {"model": "m", "url": "http://127.0.0.1:2", "digest": "d", "declared_context_length": 32768}
        snapshots = [{"own": {"models": [{"name": "m", "size": 100, "size_vram": 100}]}}]
        def streamed(url, shared, backend, model, payload, receipt):
            receipt.write(json.dumps(payload) + "\n")
            if payload["options"]["num_predict"] == 1:
                return attempt("", reason="length", terminal={"done_reason": "length", "prompt_eval_count": 100}, snapshots=snapshots)
            return attempt(snapshots=snapshots)
        def scorer(path, frozen, suite, fixture, eligible):
            return {"must_found": int(eligible), "must_total": 1, "existing_scorer_output": "Status: PASS"}
        with tempfile.TemporaryDirectory() as directory:
            fr.freeze(directory)
            args = SimpleNamespace(out=directory, url="http://127.0.0.1:2", shared_url="http://127.0.0.1:1",
                                   backend="ollama", model="m", num_predict=16384, identity_file=None, stage="screen", draws=3)
            with patch.object(tr, "identity", return_value=runtime), patch.object(tr, "residency", return_value=(snapshots[0], False)), patch.object(tr, "stream", side_effect=streamed) as mock_stream, patch.object(rr, "score", side_effect=scorer):
                self.assertEqual(len(rr.run(args)["completed"]), 10)
                self.assertEqual(mock_stream.call_count, 20)
                self.assertEqual(len(rr.run(args)["completed"]), 10)
                self.assertEqual(mock_stream.call_count, 20, "resume must not generate")
                args.stage = "clean"
                self.assertEqual(len(rr.run(args)["completed"]), 12)
                self.assertEqual(mock_stream.call_count, 36, "four screening rows reused in scoped CLEAN draw1")
                identity = json.loads(next(Path(directory).glob("runs/*/identity.json")).read_text())
                self.assertEqual(identity["condition"], fr.CONDITION)
                summary = rr.summary(directory)
                lane = next(iter(summary["lanes"].values()))
                self.assertTrue(lane["screen_execution_complete"])
                self.assertEqual(lane["stages"]["clean"]["planned_cells"], 12)
                self.assertEqual(lane["stages"]["bugreport"]["missing_cells"], 7)
                self.assertEqual(lane["unique_fixtures"], 10)
                args.num_predict = 8192
                with self.assertRaisesRegex(ValueError, "frozen common"):
                    rr.run(args)

    def test_empty_only_retries_and_blocked_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = fr.freeze(directory)
            args = SimpleNamespace(out=directory, url="http://127.0.0.1:2", shared_url="http://127.0.0.1:1",
                                   backend="openai", model="m", num_predict=16384, identity_file=None, stage="screen", draws=3)
            runtime = {"declared_context_length": 32768}
            probe = attempt("", reason="length", usage={"prompt_tokens": 100})
            answers = [probe, attempt(""), attempt(""), attempt("Verdict: REVISE")]
            def streamed(*values):
                values[-1].write("raw\n")
                return answers.pop(0)
            with patch.object(tr, "identity", return_value=runtime), patch.object(tr, "residency", return_value=({}, False)), patch.object(tr, "stream", side_effect=streamed), patch.object(rr, "cells", return_value=[("critic", manifest["screen"][0], 1)]):
                rr.run(args)
            row_path = next(Path(directory).glob("runs/*/critic-*.json"))
            row = json.loads(row_path.read_text())
            self.assertEqual(len(row["attempt_outcomes"]), 3)
            self.assertFalse(row["outcome"]["first_attempt_completed"])
            self.assertTrue(row["outcome"]["retry_assisted_completed"])
            self.assertEqual(len(row["attempts"]), 4, "probe plus all attempts retained")
            args.model = "busy"
            with patch.object(tr, "identity", return_value=runtime), patch.object(tr, "residency", return_value=({}, True)), patch.object(tr, "stream") as stream:
                with self.assertRaisesRegex(RuntimeError, "BLOCKED"):
                    rr.run(args)
                stream.assert_not_called()
            self.assertTrue(list(Path(directory).glob("runs/*/*-blocked-*.json")))

    def test_invalid_probe_and_noverdict_zero_credit(self):
        manifest = {"screen": ["button-skip-link-clean"]}
        with tempfile.TemporaryDirectory() as directory:
            fr.freeze(directory)
            args = SimpleNamespace(out=directory, url="http://127.0.0.1:2", shared_url="http://127.0.0.1:1",
                                   backend="openai", model="m", num_predict=16384, identity_file=None, stage="screen", draws=3)
            def streamed(*values):
                values[-1].write("raw\n")
                return attempt("REVISE")
            with patch.object(tr, "identity", return_value={"declared_context_length": 32768}), patch.object(tr, "residency", return_value=({}, False)), patch.object(tr, "stream", side_effect=streamed) as stream, patch.object(rr, "cells", return_value=[("critic", manifest["screen"][0], 1)]):
                rr.run(args)
                self.assertEqual(stream.call_count, 1)
            row = json.loads(next(Path(directory).glob("runs/*/critic-*.json")).read_text())
            self.assertEqual(row["outcome"]["status"], "INVALID")
            self.assertEqual(row["outcome"]["detection_credit"], 0)

    def test_bugreport_original_scorer_retained(self):
        with tempfile.TemporaryDirectory() as directory:
            fr.freeze(directory)
            response = Path(directory) / "response.json"
            fr.exclusive(response, {"response": "I need context"})
            result = rr.score(response, Path(directory) / "freeze", "bugreport", "axe-image-alt-single", False)
            self.assertIn("Status: FAIL", result["existing_scorer_output"])
            self.assertIsNone(result["adjudicated_fabrication"])

    def test_transport_identity_and_residency_sources(self):
        tags = {"models": [{"name": "m:latest", "digest": "sha", "details": {"context_length": 32768}}]}
        show = {"template": "native", "model_info": {"arch.context_length": 32768}}
        with patch.object(tr, "get_json", side_effect=[tags, show, {"version": "v"}]), patch.object(tr.rb, "fetch_declared_context_length", return_value=32768) as ceiling:
            result = tr.identity("ollama", "http://127.0.0.1:2", "m")
            self.assertEqual(result["digest"], "sha")
            ceiling.assert_called_once_with("m", tags_url="http://127.0.0.1:2/api/tags", show_url="http://127.0.0.1:2/api/show")
        with patch.object(tr, "get_json", return_value={"models": []}):
            with self.assertRaises(ValueError):
                tr.identity("ollama", "http://127.0.0.1:2", "m")
        with patch.object(tr, "get_json", side_effect=[tags, {}]):
            with self.assertRaises(ValueError):
                tr.identity("ollama", "http://127.0.0.1:2", "m")
        supplied = {key: "value" for key in ("digest", "quantization", "runtime", "version", "template", "reasoning_mode", "loader")}
        supplied.update(model="m", url="http://127.0.0.1:2", declared_context_length=32768, full_offload=True)
        self.assertEqual(tr.identity("openai", supplied["url"], "m", supplied), supplied)
        with self.assertRaises(ValueError):
            tr.identity("openai", supplied["url"], "other", supplied)
        supplied["full_offload"] = False
        with self.assertRaises(ValueError):
            tr.identity("openai", supplied["url"], "m", supplied)
        with patch.object(tr, "get_json", side_effect=[{"models": []}, {"models": [{"name": "other"}]}]):
            self.assertTrue(tr.residency("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m")[1])
        with patch.object(tr, "get_json", return_value={"models": [{"name": "busy"}]}):
            self.assertTrue(tr.residency("http://127.0.0.1:2", "http://127.0.0.1:1", "openai", "m")[1])
        with self.assertRaises(TimeoutError):
            tr.residency("http://127.0.0.1:2", "http://127.0.0.1:1", "openai", "m", until=0)

    def test_json_transport_and_stream_exception_deadline(self):
        with patch.object(tr.urllib.request, "urlopen", return_value=io.BytesIO(b'{"ok":true}')) as open_mock:
            self.assertEqual(tr.get_json("http://127.0.0.1:2", {"probe": 1}, timeout=2), {"ok": True})
            self.assertEqual(open_mock.call_args.kwargs["timeout"], 2)
        with patch.object(tr.urllib.request, "urlopen", side_effect=TimeoutError("silent socket")), patch.object(tr, "residency", return_value=({}, False)):
            result = tr.stream("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m", {}, io.StringIO(), deadline=1)
            self.assertIn("silent socket", result["exception"])
        with patch.object(tr.urllib.request, "urlopen", side_effect=TimeoutError("silent socket")), patch.object(tr, "residency", return_value=({}, False)):
            result = tr.stream("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m", {}, io.StringIO(), deadline=0)
            self.assertIn("deadline", result["exception"])
        with patch.object(tr.urllib.request, "urlopen", side_effect=TimeoutError("socket")), patch.object(tr, "residency", side_effect=RuntimeError("unreachable")):
            result = tr.stream("http://127.0.0.1:2", "http://127.0.0.1:1", "ollama", "m", {}, io.StringIO(), deadline=1)
            self.assertIn("residency", result["exception"])

    def test_cli_freeze_summary_and_failclosed(self):
        from ollama.local_eval_202610 import __main__ as cli
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(sys, "argv", ["cli", "freeze", "--out", directory]), context_redirect():
                cli.main()
            with patch.object(sys, "argv", ["cli", "summary", "--out", directory]), context_redirect():
                cli.main()
            with patch.object(sys, "argv", ["cli", "freeze", "--out", directory]), self.assertRaises(SystemExit):
                cli.main()
        with patch.object(sys, "argv", ["cli", "run", "--out", "x", "--model", "m", "--stage", "clean", "--backend", "ollama", "--url", "http://127.0.0.1:2", "--draws", "2"]), self.assertRaises(SystemExit):
            cli.main()


def context_redirect():
    import contextlib
    return contextlib.redirect_stdout(io.StringIO())


if __name__ == "__main__":
    unittest.main()
