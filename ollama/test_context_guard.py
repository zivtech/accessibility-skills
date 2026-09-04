#!/usr/bin/env python3
"""Deterministic tests for the context-overflow guard (context-utilization
plan Phase 0.2/0.3, 2026-08-24) — stdlib unittest, no pytest dependency.

Run:
    python3 -m unittest ollama/test_context_guard.py -v
    python3 ollama/test_context_guard.py

No live model generations here — that's the parallel Phase 0.4 retro-probe
lane's job (cache-warm receipt against a running Ollama server). Everything
below is pure arithmetic on the client-side estimate, plus a static read of
the two edited files' source to confirm every generation call site is gated.
"""
import ast
import importlib.util
import io
import os
import unittest
import urllib.error
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_module(name, relpath):
    """Import a sibling script by file path. ollama/*.py are standalone
    scripts (no __init__.py, not a package), so a plain `import` statement
    can't find them from an arbitrary cwd — load by path instead. This does
    NOT execute either script's `if __name__ == "__main__":` block, since the
    loaded module's __name__ is `name`, never "__main__" — no argparse, no
    network calls happen just by importing."""
    path = os.path.join(HERE, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_benchmark = _load_module("run_benchmark", "run_benchmark.py")
ollama_a11y = _load_module("ollama_a11y", "ollama_a11y.py")

# F15 (gate re-review round 4, 2026-08-25): 60,373 chars measured 14,276
# tokens on qwen3.6:35b / 13,853 on qwen3:32b, 2026-08-25 probes — see
# estimate_tokens()'s docstring (run_benchmark.py) for the full
# estimate-vs-measured comparison. Supersedes the earlier stale "16,157
# prompt_eval tokens" figure.
MEASURED_PROTOCOL_CHARS = 60373

# check_ollama() (ollama_a11y.py) hits GET /api/tags to list installed
# models — a health check, not a generation call. It sends no prompt, so the
# context-overflow gate does not apply to it and it is deliberately excluded
# from the "every API call site is gated" static scan below.
#
# fetch_declared_context_length() (both files, F13 fast-follow) also hits
# GET /api/tags — it supplies a value TO the gate (declared_context_length),
# it doesn't send a prompt itself, so the same exclusion applies for the
# same reason.
# Functions that hit the Ollama API for METADATA, never to generate. The
# gate-coverage test below exists to catch a generation lane that skips
# context_overflow(); these fetch model facts and send no prompt, so a
# prompt-size gate is meaningless for them. Add here only after checking
# the function cannot send a prompt.
NON_LANE_API_FUNCTIONS = {
    "check_ollama",
    "fetch_declared_context_length",
    # R5 follow-up (2026-08-27): /api/show metadata read, used only when
    # /api/tags reports a null context_length (gemma4:31b, gemma4:26b).
    "_fetch_context_length_from_show",
}


class TwinConstantsTests(unittest.TestCase):
    """Both files carry an independent copy of the same ~15-line helper
    (spec: duplicate rather than share a module) — assert the copies match
    each other AND the plan's mandated values, so drift between the twins
    would fail loudly here rather than silently diverging in the field."""

    def test_constants_match_the_plan(self):
        self.assertEqual(run_benchmark.CHARS_PER_TOKEN_CONSERVATIVE, 3.5)
        self.assertEqual(run_benchmark.RESPONSE_RESERVE, 8192)
        self.assertEqual(ollama_a11y.CHARS_PER_TOKEN_CONSERVATIVE, 3.5)
        self.assertEqual(ollama_a11y.RESPONSE_RESERVE, 8192)

    def test_estimate_tokens_matches_between_twins(self):
        sample = "The quick brown fox jumps over the lazy dog. " * 400
        self.assertEqual(
            run_benchmark.estimate_tokens(sample),
            ollama_a11y.estimate_tokens(sample),
        )

    def test_context_overflow_matches_between_twins(self):
        system_text = "s" * 12000
        prompt_text = "p" * 30000
        self.assertEqual(
            run_benchmark.context_overflow(system_text, prompt_text, 16384),
            ollama_a11y.context_overflow(system_text, prompt_text, 16384),
        )


class ContextOverflowGateTests(unittest.TestCase):
    """Case 1 (spec item E-1): an oversized synthetic input fires, and fires
    again on an identical second call. The plan's cache-warm requirement is
    about `prompt_eval_count` deflating under Ollama's warm KV-prefix cache
    (critic-review finding M1) — that risk doesn't apply here because the
    client-side estimate has no cache at all; it's pure arithmetic on
    len(text). Determinism across two consecutive evaluations is the correct
    analogue: unlike prompt_eval_count, this gate cannot go quiet on a second
    call against the same input."""

    def test_oversized_input_fires_twice_in_a_row_run_benchmark(self):
        huge_system = "x" * 40000
        huge_prompt = "y" * 40000
        num_ctx = 16384

        overflow1, est1 = run_benchmark.context_overflow(huge_system, huge_prompt, num_ctx)
        overflow2, est2 = run_benchmark.context_overflow(huge_system, huge_prompt, num_ctx)

        self.assertTrue(overflow1)
        self.assertTrue(overflow2)
        self.assertEqual(est1, est2)

    def test_oversized_input_fires_twice_in_a_row_ollama_a11y(self):
        huge_system = "x" * 40000
        huge_prompt = "y" * 40000
        num_ctx = 16384

        overflow1, est1 = ollama_a11y.context_overflow(huge_system, huge_prompt, num_ctx)
        overflow2, est2 = ollama_a11y.context_overflow(huge_system, huge_prompt, num_ctx)

        self.assertTrue(overflow1)
        self.assertTrue(overflow2)
        self.assertEqual(est1, est2)

    def test_normal_size_protocol_does_not_fire(self):
        # Spec item E-2: the measured 60,373-char critic protocol + an 8KB
        # fixture, at num_ctx 32768 — comfortably fits even under the
        # conservative (overestimating) 3.5 chars/token ratio.
        system_text = "p" * MEASURED_PROTOCOL_CHARS
        fixture_text = "f" * 8192
        num_ctx = 32768

        overflow, estimated = run_benchmark.context_overflow(system_text, fixture_text, num_ctx)

        self.assertFalse(overflow)
        expected = run_benchmark.estimate_tokens(system_text + fixture_text)
        self.assertEqual(estimated, expected)
        self.assertLess(estimated + run_benchmark.RESPONSE_RESERVE, num_ctx)

    def test_boundary_just_under_does_not_fire(self):
        # Spec item E-3. Solve for a char count whose estimate lands exactly
        # one token under the (estimated + reserve > num_ctx) boundary.
        num_ctx = 16384
        reserve = run_benchmark.RESPONSE_RESERVE
        target_tokens = (num_ctx - reserve) - 1
        chars = int(target_tokens * run_benchmark.CHARS_PER_TOKEN_CONSERVATIVE)
        text = "a" * chars

        overflow, estimated = run_benchmark.context_overflow("", text, num_ctx)

        self.assertLessEqual(estimated + reserve, num_ctx)
        self.assertFalse(overflow)

    def test_boundary_just_over_fires(self):
        # Spec item E-3, the other side of the same boundary.
        num_ctx = 16384
        reserve = run_benchmark.RESPONSE_RESERVE
        target_tokens = (num_ctx - reserve) + 50
        chars = int(target_tokens * run_benchmark.CHARS_PER_TOKEN_CONSERVATIVE) + 100
        text = "a" * chars

        overflow, estimated = run_benchmark.context_overflow("", text, num_ctx)

        self.assertGreater(estimated + reserve, num_ctx)
        self.assertTrue(overflow)

    def test_exact_equality_is_not_overflow(self):
        # Gate rule is "> num_ctx", not ">=" — exact equality must NOT flag.
        text = "a" * int(100 * run_benchmark.CHARS_PER_TOKEN_CONSERVATIVE)
        estimated_only = run_benchmark.estimate_tokens(text)
        num_ctx = estimated_only + run_benchmark.RESPONSE_RESERVE  # exact boundary

        overflow, estimated = run_benchmark.context_overflow("", text, num_ctx)

        self.assertEqual(estimated, estimated_only)
        self.assertFalse(overflow)


class ContextPressureTests(unittest.TestCase):
    """Post-run corroboration (spec item B): prompt_eval_count >= num_ctx -
    RESPONSE_RESERVE flags context_pressure but stays a valid row."""

    def test_no_pressure_when_far_under(self):
        self.assertFalse(run_benchmark.flag_context_pressure(1000, 32768))

    def test_pressure_at_the_boundary(self):
        num_ctx = 32768
        reserve = run_benchmark.RESPONSE_RESERVE
        self.assertTrue(run_benchmark.flag_context_pressure(num_ctx - reserve, num_ctx))

    def test_pressure_just_under_boundary_is_false(self):
        num_ctx = 32768
        reserve = run_benchmark.RESPONSE_RESERVE
        self.assertFalse(run_benchmark.flag_context_pressure(num_ctx - reserve - 1, num_ctx))

    def test_no_pressure_when_count_missing(self):
        # Older Ollama versions may not report prompt_eval_count; the guard
        # must not crash or false-flag on absent data.
        self.assertFalse(run_benchmark.flag_context_pressure(None, 32768))


class CtxMapHygieneTests(unittest.TestCase):
    """Spec item C: every lane's num_ctx map must preserve the pre-existing
    effective value for every model — no behavior change — with the single
    deliberate exception of the new CRITIC_CTX qwen3:32b entry."""

    def test_critic_ctx_has_the_new_qwen3_32b_entry(self):
        self.assertEqual(run_benchmark.CRITIC_CTX.get("qwen3:32b"), 32768)

    def test_perspective_ctx_already_had_qwen3_32b(self):
        # Plan F7: PERSPECTIVE_CTX already mapped qwen3:32b -> 32768 before
        # this change; confirm it is untouched.
        self.assertEqual(run_benchmark.PERSPECTIVE_CTX.get("qwen3:32b"), 32768)

    # R5.4 (2026-08-27): the Phase 0.2 lift's behavior-preservation lock is
    # SUPERSEDED for four of the six defaults. The lift's job was to change
    # nothing; R5's is to correct values that were measured wrong. Old ->
    # new, with the receipt in the R5 decision memo §3:
    #   CRITIC_CTX_DEFAULT       16384 -> 32768   (41/41 fixtures refused)
    #   PLANNER_CTX_DEFAULT      32768 -> 40960   (19/28 plain, 28/28 federal)
    #   BUGREPORT_CTX_DEFAULT    16384 -> 32768   (7/7; system prompt alone over)
    #   PERSPECTIVE_CTX_DEFAULT  16384 -> 32768   (21/25 refused)
    #   EVALREPORT_CTX_DEFAULT / ACR_CTX_DEFAULT  unchanged (measured fine)
    SUPERSEDED_PHASE0_LITERALS = {
        "PLANNER_CTX_DEFAULT": 32768,
        "BUGREPORT_CTX_DEFAULT": 16384,
        "CRITIC_CTX_DEFAULT": 16384,
        "PERSPECTIVE_CTX_DEFAULT": 16384,
    }

    def test_lane_ctx_defaults_are_the_r5_corrected_values(self):
        self.assertEqual(run_benchmark.CRITIC_CTX_DEFAULT, 32768)
        self.assertEqual(run_benchmark.PLANNER_CTX_DEFAULT, 40960)
        self.assertEqual(run_benchmark.BUGREPORT_CTX_DEFAULT, 32768)
        self.assertEqual(run_benchmark.PERSPECTIVE_CTX_DEFAULT, 32768)
        # untouched by R5 — measured as already sufficient
        self.assertEqual(run_benchmark.EVALREPORT_CTX_DEFAULT, 32768)
        self.assertEqual(run_benchmark.ACR_CTX_DEFAULT, 40960)

    def test_the_wrapper_twin_map_is_hand_synced_with_the_benchmark_defaults(self):
        """R5.4 put a per-command num_ctx dict in ollama_a11y.py because the
        wrapper's flat 32768 was wrong for planner. The two files are
        standalone scripts synced by hand (run_benchmark.py:33-34); this is
        the only thing that catches the drift that convention invites."""
        self.assertEqual(ollama_a11y.SKILL_NUM_CTX["critic"], run_benchmark.CRITIC_CTX_DEFAULT)
        self.assertEqual(ollama_a11y.SKILL_NUM_CTX["planner"], run_benchmark.PLANNER_CTX_DEFAULT)
        self.assertEqual(ollama_a11y.SKILL_NUM_CTX["perspective"], run_benchmark.PERSPECTIVE_CTX_DEFAULT)
        self.assertEqual(ollama_a11y.SKILL_NUM_CTX["bugreport"], run_benchmark.BUGREPORT_CTX_DEFAULT)
        self.assertEqual(ollama_a11y.SKILL_NUM_CTX["evalreport"], run_benchmark.EVALREPORT_CTX_DEFAULT)

    def test_wrapper_run_sizes_num_ctx_from_the_skill_when_not_given(self):
        """The default is None, not a literal — so a caller that passes
        nothing gets the per-skill value, and one that passes a number still
        wins. run_chain_local.py's planner step is the caller this fixes."""
        import inspect
        self.assertIsNone(inspect.signature(ollama_a11y.run).parameters["num_ctx"].default)
        self.assertEqual(ollama_a11y.SKILL_NUM_CTX.get("planner"), 40960)
        self.assertEqual(
            ollama_a11y.SKILL_NUM_CTX.get("nonexistent-skill",
                                          ollama_a11y.SKILL_NUM_CTX_DEFAULT), 32768)

    def test_every_raised_default_actually_clears_its_suite_today(self):
        """The lock with teeth. A default is only correct against the CURRENT
        protocol + fixtures; SKILL.md files grow (a11y-planner grew 11,132
        chars in the six weeks to 2026-08-25, R5.3 §4.4). This fails the day
        growth pushes a suite's largest assembled prompt past its default's
        budget — which is the signal to re-probe and raise, and, for
        planner-federal on qwen3:32b (declared ceiling 40,960, current margin
        759 estimated tokens), the signal that no larger legal value exists."""
        reserve = run_benchmark.RESPONSE_RESERVE
        cases = []
        critic_sys = run_benchmark.load_system_prompt()
        for fid in sorted(f[:-3] for f in os.listdir(run_benchmark.FIXTURES_DIR)
                          if f.endswith(".md")):
            cases.append(("critic", run_benchmark.CRITIC_CTX_DEFAULT, critic_sys,
                          run_benchmark.PROMPT_PREFIX + run_benchmark.load_fixture(fid), fid))
        for label, sysp, ctx_default in (
                ("planner", run_benchmark.load_planner_system_prompt(),
                 run_benchmark.PLANNER_CTX_DEFAULT),
                ("planner-federal", run_benchmark.load_planner_federal_system_prompt(),
                 run_benchmark.PLANNER_FEDERAL_CTX_DEFAULT)):
            for fid in run_benchmark.PLANNER_FIXTURES:
                cases.append((label, ctx_default, sysp,
                              run_benchmark.PLANNER_PROMPT_PREFIX
                              + run_benchmark.load_fixture(fid, run_benchmark.PLANNER_FIXTURES_DIR), fid))
        with open(run_benchmark.BUGREPORT_SKILL_PATH) as f:
            bug_sys = run_benchmark.strip_frontmatter(f.read())
        for fid in run_benchmark.BUGREPORT_FIXTURES:
            cases.append(("bugreport", run_benchmark.BUGREPORT_CTX_DEFAULT, bug_sys,
                          run_benchmark.BUGREPORT_PROMPT_PREFIX
                          + run_benchmark.load_fixture(fid, run_benchmark.BUGREPORT_FIXTURES_DIR), fid))
        persp_sys = run_benchmark.load_perspective_system_prompt()
        for fid in sorted(f[:-3] for f in os.listdir(run_benchmark.PERSPECTIVE_FIXTURES_DIR)
                          if f.endswith(".md")):
            cases.append(("perspective", run_benchmark.PERSPECTIVE_CTX_DEFAULT, persp_sys,
                          run_benchmark.build_escalation_prompt(fid), fid))

        over = []
        for suite, ctx, sysp, prompt, fid in cases:
            overflow, est = run_benchmark.context_overflow(sysp, prompt, ctx)
            if overflow:
                over.append(f"{suite}/{fid}: est {est} + reserve {reserve} > num_ctx {ctx}")
        self.assertEqual(over, [], "suites whose largest prompts no longer fit their "
                                   "R5.4 default — re-probe and raise:\n" + "\n".join(over))

    def test_lifted_maps_are_behavior_preserving_for_any_unmapped_model(self):
        # Each lifted map (planner/bugreport/evalreport/acr) was a flat
        # literal for every model before this change; an empty dict + a
        # default equal to that literal reproduces the identical value for
        # any model, mapped or not.
        for mapping, default in [
            (run_benchmark.PLANNER_CTX, run_benchmark.PLANNER_CTX_DEFAULT),
            (run_benchmark.BUGREPORT_CTX, run_benchmark.BUGREPORT_CTX_DEFAULT),
            (run_benchmark.EVALREPORT_CTX, run_benchmark.EVALREPORT_CTX_DEFAULT),
            (run_benchmark.ACR_CTX, run_benchmark.ACR_CTX_DEFAULT),
        ]:
            for model in ("qwen3:32b", "qwen3.6:35b", "some-brand-new-model:1b"):
                self.assertEqual(mapping.get(model, default), default)


class InvalidRowShapeTests(unittest.TestCase):
    """The INVALID row's filename must not collide with the *-response.json
    glob pattern score-all/score-perspective/*-remaining all use, so those
    commands skip it automatically instead of handing a differently-shaped
    JSON to a scorer that expects a completed generation."""

    def test_overflow_row_filename_is_skipped_by_response_json_glob(self):
        import fnmatch
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            fake_out_path = os.path.join(
                tmpdir, "ollama-bench-some-fixture-some-model-response.json"
            )
            path = run_benchmark.write_overflow_row(
                fake_out_path,
                model="test-model",
                fixture_id="test-fixture",
                estimated=99999,
                num_ctx=16384,
                skill="a11y-critic",
            )

            self.assertFalse(fnmatch.fnmatch(os.path.basename(path), "*-response.json"))
            self.assertTrue(os.path.exists(path))

            with open(path) as f:
                row = json.load(f)
            self.assertEqual(row["invalid"], "context_overflow")
            self.assertEqual(row["estimated_prompt_tokens"], 99999)
            self.assertEqual(row["num_ctx"], 16384)
            self.assertEqual(row["response_reserve"], run_benchmark.RESPONSE_RESERVE)
            self.assertEqual(row["_benchmark"]["model"], "test-model")
            self.assertEqual(row["_benchmark"]["fixture_id"], "test-fixture")
            self.assertEqual(row["_benchmark"]["skill"], "a11y-critic")

    def test_overflow_row_records_declared_context_length_when_provided(self):
        # F13: a row that overflowed because Ollama would have clamped below
        # the requested num_ctx must be distinguishable from one that
        # overflowed on the requested value alone.
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            fake_out_path = os.path.join(tmpdir, "ollama-bench-x-y-response.json")
            path = run_benchmark.write_overflow_row(
                fake_out_path, model="qwen3:32b", fixture_id="x", estimated=99999,
                num_ctx=49152, skill="a11y-critic", declared_context_length=40960,
            )
            with open(path) as f:
                row = json.load(f)
            self.assertEqual(row["declared_context_length"], 40960)

    def test_overflow_row_declared_context_length_defaults_to_none(self):
        # Backward-compat: an un-updated caller must not crash, and the key
        # must be explicitly None, never silently absent from the row.
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            fake_out_path = os.path.join(tmpdir, "ollama-bench-x-y-response.json")
            path = run_benchmark.write_overflow_row(
                fake_out_path, model="test-model", fixture_id="x", estimated=1,
                num_ctx=16384, skill="a11y-critic",
            )
            with open(path) as f:
                row = json.load(f)
            self.assertIn("declared_context_length", row)
            self.assertIsNone(row["declared_context_length"])


def _fake_tags_response(models):
    """Builds the exact /api/tags shape confirmed live, 2026-08-25
    (models[].name, models[].details.context_length). `models` is a list of
    (name, context_length_or_None) pairs; None omits the field entirely, for
    the "listed but no context_length" failure case."""
    import json as _json

    body = {"models": [
        {"name": name, "details": ({"context_length": ctx} if ctx is not None else {})}
        for name, ctx in models
    ]}
    return _json.dumps(body).encode()


def _fake_endpoint_router(tags_models, show_info=None):
    """urlopen side_effect that answers /api/tags and /api/show differently,
    so the R5 fallback path can be exercised without a live server.
    show_info maps model name -> the model_info dict /api/show returns."""
    import json as _json

    def _router(req, *a, **kw):
        url = req.full_url if hasattr(req, "full_url") else str(req)
        if url.endswith("/api/show"):
            name = _json.loads(req.data.decode())["model"]
            return io.BytesIO(_json.dumps(
                {"model_info": (show_info or {}).get(name, {})}).encode())
        return io.BytesIO(_fake_tags_response(tags_models))
    return _router


class TagResolutionAndShowFallbackTests(unittest.TestCase):
    """R5 follow-up (2026-08-27). Three defects found while probing for R5.2,
    all of which stopped a model running ANY lane — none of them a num_ctx
    value problem:
      1. /api/tags always reports a tagged name, so the bare string
         `laguna-xs-2.1` (12 committed critic rows, and a CRITIC_CTX entry)
         raised GuardConfigError while `laguna-xs-2.1:latest` resolved.
      2. gemma4:31b / gemma4:26b list with a NULL details.context_length, so
         the F13 raise hard-blocked two CRITIC_CTX-mapped models.
      3. The *_CTX maps are keyed on the caller's string, so the same
         spelling gap silently dropped a mapped model to the _DEFAULT."""

    def setUp(self):
        run_benchmark._DECLARED_CONTEXT_LENGTH_CACHE.clear()
        ollama_a11y._DECLARED_CONTEXT_LENGTH_CACHE.clear()

    def test_tag_variants_implies_only_latest(self):
        for mod in (run_benchmark, ollama_a11y):
            self.assertEqual(mod._tag_variants("foo"), ["foo", "foo:latest"])
            self.assertEqual(mod._tag_variants("foo:latest"), ["foo:latest", "foo"])
            # A real tag is NOT interchangeable with :latest. qwen3.5:27b and
            # qwen3.5:latest are different models (a 27B that is not installed
            # vs the installed 9.7B) — conflating them would silently apply
            # one model's window to another.
            self.assertEqual(mod._tag_variants("qwen3.5:27b"), ["qwen3.5:27b"])
            self.assertEqual(mod._tag_variants("qwen3:32b"), ["qwen3:32b"])

    def test_bare_name_resolves_against_a_tagged_tags_listing(self):
        body = _fake_tags_response([("laguna-xs-2.1:latest", 262144)])
        for mod in (run_benchmark, ollama_a11y):
            with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
                self.assertEqual(mod.fetch_declared_context_length("laguna-xs-2.1"), 262144)
            mod._DECLARED_CONTEXT_LENGTH_CACHE.clear()

    def test_show_fallback_supplies_a_null_tags_context_length(self):
        router = _fake_endpoint_router(
            [("gemma4:31b", None)], {"gemma4:31b": {"gemma4.context_length": 262144}})
        for mod in (run_benchmark, ollama_a11y):
            with mock.patch("urllib.request.urlopen", side_effect=router):
                self.assertEqual(mod.fetch_declared_context_length("gemma4:31b"), 262144)
            mod._DECLARED_CONTEXT_LENGTH_CACHE.clear()

    def test_still_raises_when_neither_source_has_a_value(self):
        """The fallback must not become a silent default — the whole point of
        F13. No context_length anywhere still fails loud."""
        router = _fake_endpoint_router([("mystery:1b", None)], {"mystery:1b": {}})
        for mod in (run_benchmark, ollama_a11y):
            with mock.patch("urllib.request.urlopen", side_effect=router):
                with self.assertRaises(mod.GuardConfigError):
                    mod.fetch_declared_context_length("mystery:1b")

    def test_a_genuinely_absent_model_still_raises(self):
        body = _fake_tags_response([("qwen3:32b", 40960)])
        for mod in (run_benchmark, ollama_a11y):
            with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
                with self.assertRaises(mod.GuardConfigError):
                    mod.fetch_declared_context_length("qwen3.5:27b")

    def test_show_fallback_never_overrides_a_real_tags_ceiling(self):
        """qwen3:32b's declared 40,960 is F13's whole reason for existing. If
        /api/show's architecture metadata (which can report a larger figure)
        ever won, the clamp would go undetected again."""
        router = _fake_endpoint_router(
            [("qwen3:32b", 40960)], {"qwen3:32b": {"qwen3.context_length": 262144}})
        for mod in (run_benchmark, ollama_a11y):
            with mock.patch("urllib.request.urlopen", side_effect=router):
                self.assertEqual(mod.fetch_declared_context_length("qwen3:32b"), 40960)
            mod._DECLARED_CONTEXT_LENGTH_CACHE.clear()

    def test_ctx_for_resolves_the_latest_spelling_gap_both_ways(self):
        mapping = {"laguna-xs-2.1": 32768, "qwen3.6:35b": 32768}
        self.assertEqual(run_benchmark.ctx_for("laguna-xs-2.1:latest", mapping, 16384), 32768)
        self.assertEqual(run_benchmark.ctx_for("laguna-xs-2.1", mapping, 16384), 32768)
        self.assertEqual(run_benchmark.ctx_for("qwen3.6:35b", mapping, 16384), 32768)
        # unrelated model still falls to the default
        self.assertEqual(run_benchmark.ctx_for("qwen3.5:27b", mapping, 16384), 16384)

    def test_every_lane_uses_ctx_for_not_a_bare_dict_get(self):
        """A lane that goes back to `MAP.get(model, DEFAULT)` silently
        reintroduces defect 3 for that lane only."""
        source = open(os.path.join(HERE, "run_benchmark.py")).read()
        for name in ("CRITIC_CTX", "PLANNER_CTX", "BUGREPORT_CTX",
                     "EVALREPORT_CTX", "ACR_CTX", "PERSPECTIVE_CTX"):
            self.assertIn(f"ctx_for(model, {name}, {name}_DEFAULT)", source)
            self.assertNotIn(f"{name}.get(model,", source)


class DeclaredContextLengthGuardTests(unittest.TestCase):
    """F13 fast-follow (bench-reviewer gate re-review, 2026-08-25): the
    guard used to check the estimate against the REQUESTED num_ctx only.
    Proven live the same day — a live over/under probe found qwen3:32b
    requested at 49,152 was silently clamped server-side to its declared
    40,960 (`n_ctx = 40960` in the server log), and a 45,176-token prompt
    lost 54.7% of itself to truncation (`prompt=45176 ... new=20482`) while
    this exact guard, checking only the requested value, would have waved
    it through. These are the failing-direction cases the fix must close."""

    def test_declared_smaller_than_requested_fires_even_though_requested_alone_fits(self):
        num_ctx = 49152
        declared = 40960
        reserve = run_benchmark.RESPONSE_RESERVE
        # Sized to fit under num_ctx-reserve but NOT under declared-reserve
        # — the live-proven qwen3:32b scenario.
        target_tokens = (declared - reserve) + 200
        chars = int(target_tokens * run_benchmark.CHARS_PER_TOKEN_CONSERVATIVE)
        text = "a" * chars

        without_declared, _ = run_benchmark.context_overflow("", text, num_ctx)
        with_declared, _ = run_benchmark.context_overflow("", text, num_ctx, declared)

        self.assertFalse(without_declared, "sanity check: must fit the OLD (bugged) 3-arg guard")
        self.assertTrue(with_declared, "F13 fix: must fire once declared < requested is supplied")

    def test_declared_larger_than_requested_never_relaxes_the_guard(self):
        # qwen3.6:35b declares 262144 — a large declared ceiling must not
        # override a smaller REQUESTED num_ctx (min(), never max()).
        overflow, _ = run_benchmark.context_overflow("", "a" * 200000, 16384, 262144)
        self.assertTrue(overflow)

    def test_declared_none_is_the_old_unfixed_behavior(self):
        text = "a" * 1000
        self.assertEqual(
            run_benchmark.context_overflow("", text, 16384),
            run_benchmark.context_overflow("", text, 16384, None),
        )

    def test_matches_between_twins_with_a_declared_ceiling(self):
        text = "p" * 60000
        self.assertEqual(
            run_benchmark.context_overflow("", text, 49152, 40960),
            ollama_a11y.context_overflow("", text, 49152, 40960),
        )


class FetchDeclaredContextLengthTests(unittest.TestCase):
    """F13: fetch_declared_context_length must cache per model and fail
    loud — never a silent default — on /api/tags being unreachable, the
    model missing from the listing, or listed with no context_length field.
    A silent default here would recreate the exact bug this function exists
    to close, so 'never a return value on failure' is checked directly."""

    def setUp(self):
        run_benchmark._DECLARED_CONTEXT_LENGTH_CACHE.clear()
        ollama_a11y._DECLARED_CONTEXT_LENGTH_CACHE.clear()

    def test_caches_after_first_fetch(self):
        body = _fake_tags_response([("qwen3:32b", 40960)])
        with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)) as m:
            first = run_benchmark.fetch_declared_context_length("qwen3:32b")
            second = run_benchmark.fetch_declared_context_length("qwen3:32b")
        self.assertEqual(first, 40960)
        self.assertEqual(second, 40960)
        self.assertEqual(m.call_count, 1, "second call must be served from cache")

    def test_matches_live_confirmed_values(self):
        # 2026-08-25 live probe: qwen3:32b -> 40960, qwen3.6:35b -> 262144.
        body = _fake_tags_response([("qwen3:32b", 40960), ("qwen3.6:35b", 262144)])
        with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
            self.assertEqual(run_benchmark.fetch_declared_context_length("qwen3:32b"), 40960)
        run_benchmark._DECLARED_CONTEXT_LENGTH_CACHE.clear()
        with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
            self.assertEqual(run_benchmark.fetch_declared_context_length("qwen3.6:35b"), 262144)

    def test_unreachable_tags_endpoint_fails_loud(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("connection refused")):
            with self.assertRaises(run_benchmark.GuardConfigError):
                run_benchmark.fetch_declared_context_length("qwen3:32b")

    def test_model_missing_from_tags_fails_loud(self):
        body = _fake_tags_response([("some-other-model:1b", 8192)])
        with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
            with self.assertRaises(run_benchmark.GuardConfigError):
                run_benchmark.fetch_declared_context_length("qwen3:32b")

    def test_model_present_but_no_context_length_field_fails_loud(self):
        body = _fake_tags_response([("qwen3:32b", None)])
        with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
            with self.assertRaises(run_benchmark.GuardConfigError):
                run_benchmark.fetch_declared_context_length("qwen3:32b")

    def test_failure_never_returns_a_silent_default(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            try:
                result = run_benchmark.fetch_declared_context_length("qwen3:32b")
            except run_benchmark.GuardConfigError:
                return
            self.fail(f"expected GuardConfigError, got a silent return value instead: {result!r}")

    def test_ollama_a11y_twin_fetches_and_fails_identically(self):
        body = _fake_tags_response([("qwen3:32b", 40960)])
        with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
            self.assertEqual(ollama_a11y.fetch_declared_context_length("qwen3:32b"), 40960)
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            with self.assertRaises(ollama_a11y.GuardConfigError):
                ollama_a11y.fetch_declared_context_length("some-uncached-model:1b")


class GuardedResponseBackwardCompatTests(unittest.TestCase):
    """ollama_a11y.run() must keep returning something that behaves as a
    plain str for its two existing callers outside this task's file
    ownership — ollama/run_chain_local.py (`plan = oa.run(...)`, then
    `write(fixture, "planner-plan.md", plan)` -> `f.write(plan)`, and
    f-string interpolation into the next stage's prompt) and
    ollama/run_critic_control.py (`critic = oa.run(...)`). A naive
    (response, overflowed) tuple return breaks both immediately (file.write()
    raises TypeError on a tuple). GuardedResponse (a str subclass carrying an
    .overflowed attribute) is the fix — these tests pin that contract."""

    def test_guarded_response_is_a_real_str(self):
        r = ollama_a11y.GuardedResponse("some finding text")
        self.assertIsInstance(r, str)
        self.assertEqual(r, "some finding text")
        self.assertEqual(len(r), len("some finding text"))
        self.assertEqual(r.upper(), "SOME FINDING TEXT")

    def test_guarded_response_survives_file_write(self):
        # The exact operation that would raise TypeError on a bare tuple
        # (ollama/run_chain_local.py:58-59's write() helper).
        import tempfile

        r = ollama_a11y.GuardedResponse("plan text")
        r.overflowed = True
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.md")
            with open(path, "w") as f:
                f.write(r)  # must not raise
            with open(path) as f:
                self.assertEqual(f.read(), "plan text")

    def test_guarded_response_survives_fstring_interpolation(self):
        # ollama/run_chain_local.py:71 embeds the planner output into the
        # next stage's prompt via an f-string.
        r = ollama_a11y.GuardedResponse("the plan")
        embedded = f"PLAN UNDER REVIEW:\n{r}\n"
        self.assertEqual(embedded, "PLAN UNDER REVIEW:\nthe plan\n")

    def test_guarded_response_carries_the_overflow_flag(self):
        r = ollama_a11y.GuardedResponse("text")
        r.overflowed = True
        self.assertTrue(r.overflowed)

    def test_guarded_response_defaults_to_not_overflowed(self):
        r = ollama_a11y.GuardedResponse("text")
        self.assertFalse(r.overflowed)

    def test_guarded_response_json_dumps_as_plain_string(self):
        import json

        r = ollama_a11y.GuardedResponse('has "quotes" and \n newline')
        r.overflowed = True
        dumped = json.dumps({"response": r})
        # The extra attribute must not leak into the JSON — only the string
        # value is representable.
        self.assertEqual(json.loads(dumped)["response"], 'has "quotes" and \n newline')
        self.assertNotIn("overflowed", dumped)


class GateCoverageStaticTests(unittest.TestCase):
    """Spec item E-4: verify by static check that no lane function calls the
    API without the gate. Reads each file's source as an AST (rather than
    importing + mocking the network) so this never needs a live model."""

    def _check_file(self, relpath, expected_functions):
        path = os.path.join(HERE, relpath)
        with open(path) as f:
            source = f.read()
        tree = ast.parse(source, filename=relpath)

        gated_functions = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or node.name in NON_LANE_API_FUNCTIONS:
                continue

            urlopen_lines = []
            gate_lines = []
            for sub in ast.walk(node):
                if not isinstance(sub, ast.Call):
                    continue
                func = sub.func
                if isinstance(func, ast.Attribute) and func.attr == "urlopen":
                    urlopen_lines.append(sub.lineno)
                if isinstance(func, ast.Name) and func.id == "context_overflow":
                    gate_lines.append(sub.lineno)

            if not urlopen_lines:
                continue
            gated_functions.add(node.name)

            with self.subTest(function=node.name):
                self.assertTrue(
                    gate_lines,
                    f"{relpath}:{node.name} calls urlopen() with no "
                    "context_overflow() gate anywhere in the function body",
                )
                if gate_lines:
                    self.assertLess(
                        min(gate_lines),
                        min(urlopen_lines),
                        f"{relpath}:{node.name} calls the gate AFTER urlopen(), "
                        "not before — the send is not actually guarded",
                    )

        missing = expected_functions - gated_functions
        self.assertFalse(
            missing,
            f"{relpath}: expected API-calling function(s) not found at all "
            f"(renamed? refactored away?): {missing}",
        )

    def test_run_benchmark_every_lane_is_gated(self):
        self._check_file(
            "run_benchmark.py",
            {
                "run_ollama",
                "run_planner",
                "run_bugreport",
                "run_evalreport",
                "run_acr",
                "run_perspective",
            },
        )

    def test_ollama_a11y_run_is_gated(self):
        self._check_file("ollama_a11y.py", {"run"})


if __name__ == "__main__":
    unittest.main()
