"""Freeze source material and rendered blind prompts before generation."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

from ollama import run_benchmark as rb

SOURCE = "3ffc2cca364456d09e4daca31f54623b02fe9d93"
ROOT = Path(__file__).resolve().parents[2]
LEGACY_CONDITION = "neutral-H1-blind-no-features-202610"
CONDITION = "critic-standalone-v2-202610"
CONDITION_DIR = ROOT / "evals/conditions/critic-standalone-v2"
CONDITION_FILES = ("system.md", "protocol.md", "README.md")
REVIEWED_CLEAN = ["button-skip-link-clean", "interactive-dropdown-clean",
                  "modal-complete-clean", "search-results-dynamic-clean"]
SCREEN = [
    "form-validation-missing-aria-describedby", "toast-notification-no-role",
    "infinite-scroll-no-announcement", "accordion-no-region-role",
    "tooltip-no-role-no-association", "button-skip-link-clean",
    "interactive-dropdown-clean", "modal-complete-clean",
    "search-results-dynamic-clean", "tabbed-nav-vs-tab-pattern",
]


def digest(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def encoded(data):
    return (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()


def exclusive(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data if isinstance(data, bytes) else encoded(data))


def source_guard(expected=SOURCE):
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head) or (expected is not None and head != expected):
        raise ValueError(f"wrong source: {head}; expected {expected}")
    return head


def neutralize(content):
    content = rb.strip_answer_key(content)
    content, count = re.subn(r"^# [^\n]*$", "# Component under review", content, count=1, flags=re.M)
    if count != 1:
        raise ValueError("critic fixture must have one H1")
    content, removed = rb.FEATURES_SECTION_RE.subn("", content)
    if removed > 1:
        raise ValueError("multiple features sections")
    return re.sub(r"\n{3,}", "\n\n", content).rstrip() + "\n"


def freeze_suite(save, manifest, suite, fixtures, directory, skill, prefix):
    raw_system = Path(skill).read_bytes()
    save(f"sources/{suite}-skill.md", raw_system)
    system = rb.strip_frontmatter(raw_system.decode())
    for fixture in fixtures:
        raw = (Path(directory) / f"{fixture}.md").read_bytes()
        body = neutralize(raw.decode()) if suite == "critic" else rb.strip_answer_key(raw.decode())
        prompt = {"system": system, "prompt": prefix + body}
        key = f"{suite}/{fixture}"
        save(f"prompts/{key}.json", encoded(prompt))
        save(f"sources/{key}.md", raw)
        for suffix in ("metadata.yaml", "rubric.yaml"):
            base = Path(directory) if suffix == "metadata.yaml" else Path(directory).parent / "rubrics"
            path = base / f"{fixture}.{suffix}"
            if path.exists():
                save(f"sources/{key}.{suffix}", path.read_bytes())
        manifest["prompts"][key] = digest(encoded(prompt))


def freeze(out, num_predict=16384, condition=CONDITION):
    if condition == LEGACY_CONDITION:
        raise ValueError("legacy condition is sealed; inspect its existing frozen files instead")
    if condition != CONDITION:
        raise ValueError(f"unknown condition: {condition}")
    head = source_guard(expected=None)
    if num_predict < rb.RESPONSE_RESERVE:
        raise ValueError("output budget must be at least RESPONSE_RESERVE")
    target = Path(out) / "freeze"
    if target.exists():
        raise FileExistsError(f"refusing existing freeze: {target}")
    manifest = {"schema": 2, "source": head, "condition": condition, "files": {}, "prompts": {},
                "options": {"temperature": .3, "num_ctx": 32768, "num_predict": num_predict},
                "response_reserve": rb.RESPONSE_RESERVE, "clean_draws": 3,
                "max_attempts": 3, "attempt_deadline_seconds": 1800,
                "screen": SCREEN, "clean": REVIEWED_CLEAN,
                "bugreport": [f for f in rb.BUGREPORT_FIXTURES if f != "riverbend-permits-corroboration"]}
    def save(name, data):
        exclusive(target / name, data)
        manifest["files"][name] = digest(data)
    for name in CONDITION_FILES:
        save(f"sources/condition/{name}", (CONDITION_DIR / name).read_bytes())
    save("sources/critic-canonical-guidance.md", Path(rb.SKILL_PATH).read_bytes())
    for suite, fixtures, directory, skill, prefix in [
        ("critic", SCREEN, rb.FIXTURES_DIR, CONDITION_DIR / "system.md",
         "Review the supplied component and CSS. Return the completed review.\n\n"),
        ("bugreport", manifest["bugreport"], rb.BUGREPORT_FIXTURES_DIR, rb.BUGREPORT_SKILL_PATH, rb.BUGREPORT_PROMPT_PREFIX),
    ]:
        freeze_suite(save, manifest, suite, fixtures, directory, skill, prefix)
    # Preserve the exact scorer/guard sources used for this condition as evidence.
    for name in ("run_benchmark.py", "score_output.py", "score_common.py", "score_bugreport.py"):
        save(f"sources/{name}", (ROOT / "ollama" / name).read_bytes())
    for module in sorted((ROOT / "ollama/local_eval_202610").glob("*.py")):
        save(f"sources/local_eval_202610/{module.name}", module.read_bytes())
    save("sources/ict-baseline-test-id-manifest.yaml", (ROOT / "docs/ict-baseline-test-id-manifest.yaml").read_bytes())
    exclusive(target / "manifest.json", manifest)
    exclusive(target / "manifest.sha256", (digest(encoded(manifest)) + "\n").encode())
    return manifest


def verify_files(out):
    """Inspect immutable history only; this never authorizes inference/resume."""
    target = Path(out) / "freeze"
    raw = (target / "manifest.json").read_bytes()
    if digest(raw) != (target / "manifest.sha256").read_text().strip():
        raise ValueError("manifest hash mismatch")
    manifest = json.loads(raw)
    for name, expected in manifest["files"].items():
        path = (target / name).resolve()
        if not path.is_relative_to(target.resolve()):
            raise ValueError(f"frozen path escapes root: {name}")
        if digest((target / name).read_bytes()) != expected:
            raise ValueError(f"frozen file hash mismatch: {name}")
    return {"manifest": manifest, "verified_files": len(manifest["files"]),
            "resume_authorized": False}


def verify(out):
    manifest = verify_files(out)["manifest"]
    source_guard(expected=manifest["source"])
    condition = manifest.get("condition", LEGACY_CONDITION)
    if condition not in (CONDITION, LEGACY_CONDITION):
        raise ValueError(f"unknown frozen condition: {condition}")
    for name in ("run_benchmark.py", "score_output.py", "score_common.py", "score_bugreport.py"):
        if digest((ROOT / "ollama" / name).read_bytes()) != manifest["files"][f"sources/{name}"]:
            raise ValueError(f"live scorer/guard changed: {name}")
    modules = sorted((ROOT / "ollama/local_eval_202610").glob("*.py"))
    live_keys = {f"sources/local_eval_202610/{module.name}" for module in modules}
    frozen_keys = {name for name in manifest["files"] if name.startswith("sources/local_eval_202610/")}
    if live_keys != frozen_keys or not live_keys:
        raise ValueError("live supplemental module set changed")
    for module in modules:
        if digest(module.read_bytes()) != manifest["files"][f"sources/local_eval_202610/{module.name}"]:
            raise ValueError(f"live supplemental module changed: {module.name}")
    baseline = ROOT / "docs/ict-baseline-test-id-manifest.yaml"
    if digest(baseline.read_bytes()) != manifest["files"]["sources/ict-baseline-test-id-manifest.yaml"]:
        raise ValueError("live baseline manifest changed")
    if condition == CONDITION:
        for name in CONDITION_FILES:
            if digest((CONDITION_DIR / name).read_bytes()) != manifest["files"][f"sources/condition/{name}"]:
                raise ValueError(f"live condition changed: {name}")
        verify_fixture_sources(manifest)
    return manifest


def verify_fixture_sources(manifest):
    for suite, directory in (("critic", rb.FIXTURES_DIR), ("bugreport", rb.BUGREPORT_FIXTURES_DIR)):
        prefix = f"sources/{suite}/"
        for name, expected in manifest["files"].items():
            if not name.startswith(prefix):
                continue
            filename = name[len(prefix):]
            base = Path(directory).parent / "rubrics" if filename.endswith(".rubric.yaml") else Path(directory)
            if digest((base / filename).read_bytes()) != expected:
                raise ValueError(f"live fixture source changed: {name}")
