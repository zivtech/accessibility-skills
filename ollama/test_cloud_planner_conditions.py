#!/usr/bin/env python3
"""Offline regressions for hosted planner condition isolation."""

import importlib.util
import json
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "run_cloud_benchmark_conditions", os.path.join(HERE, "run_cloud_benchmark.py")
)
cloud = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cloud)

LOCAL_SPEC = importlib.util.spec_from_file_location(
    "run_benchmark_conditions", os.path.join(HERE, "run_benchmark.py")
)
local = importlib.util.module_from_spec(LOCAL_SPEC)
LOCAL_SPEC.loader.exec_module(local)

TIER = {"name": "5.5-low", "model": "gpt-5.5", "effort": "low", "label": "test"}
FIXTURE = "keyboard-breadcrumb"


class PromptAndIdentityTests(unittest.TestCase):
    def test_federal_system_prompt_is_byte_identical_to_local_runner(self):
        self.assertEqual(
            cloud.load_planner_federal_system_prompt(),
            local.load_planner_federal_system_prompt(),
        )
        self.assertTrue(cloud.load_planner_federal_system_prompt().endswith("\n```\n"))

    def test_plain_and_federal_use_identical_user_prompt(self):
        seen = []
        with mock.patch.object(cloud, "run_codex", side_effect=lambda *a, **k: seen.append((a, k))):
            cloud.run_codex_planner(TIER, FIXTURE, "planner")
            cloud.run_codex_planner(TIER, FIXTURE, "planner-federal")
        self.assertEqual(seen[0][0][3], seen[1][0][3])
        self.assertEqual(seen[0][0][4], "planner")
        self.assertEqual(seen[1][1]["condition"], "planner-federal")

    def test_result_and_message_paths_are_condition_isolated(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            plain = cloud.output_path("codex", TIER["name"], FIXTURE, "planner", "planner")
            federal = cloud.output_path(
                "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
            )
            self.assertNotEqual(plain, federal)
            self.assertIn("planner-federal", federal)
            self.assertEqual(
                plain,
                cloud.output_path("codex", TIER["name"], FIXTURE, "planner"),
            )
            self.assertNotEqual(
                cloud.codex_message_path(TIER["name"], FIXTURE, "planner", "planner"),
                cloud.codex_message_path(
                    TIER["name"], FIXTURE, "planner", "planner-federal"
                ),
            )

    def test_result_cache_is_condition_isolated_and_rejects_errors(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            plain = cloud.output_path("codex", TIER["name"], FIXTURE, "planner")
            federal = cloud.output_path(
                "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
            )
            with open(plain, "w") as f:
                json.dump({"response": "x" * 101, "_benchmark": {"skill": "planner"}}, f)
            with open(federal, "w") as f:
                json.dump({"response": "", "error": "offline"}, f)
            self.assertTrue(cloud.result_exists("codex", TIER["name"], FIXTURE, "planner"))
            self.assertFalse(
                cloud.result_exists(
                    "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
                )
            )

    def test_result_cache_rejects_mislabeled_condition_and_malformed_shapes(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            federal = cloud.output_path(
                "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
            )
            with open(federal, "w") as f:
                json.dump({
                    "response": "x" * 101,
                    "_benchmark": {"skill": "planner", "condition": "planner"},
                }, f)
            self.assertFalse(cloud.result_exists(
                "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
            ))
            with open(federal, "w") as f:
                json.dump([], f)
            self.assertFalse(cloud.result_exists(
                "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
            ))

    def test_result_cache_rejects_unfinished_row_with_complete_metadata(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            plain = cloud.output_path("codex", TIER["name"], FIXTURE, "planner")
            with open(plain, "w") as f:
                json.dump({
                    "response": "partial" * 30,
                    "done": False,
                    "_benchmark": {
                        "skill": "planner", "condition": "planner",
                        "fixture_id": FIXTURE, "tier": TIER["name"],
                    },
                }, f)
            self.assertFalse(
                cloud.result_exists("codex", TIER["name"], FIXTURE, "planner")
            )


class CodexMetadataTests(unittest.TestCase):
    def _run_error(self, proc):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            with mock.patch.object(cloud.subprocess, "run", return_value=proc):
                out = cloud.run_codex(
                    TIER, FIXTURE, "system", "user", "planner",
                    condition="planner-federal",
                )
            with open(out) as f:
                return json.load(f)

    def test_success_preserves_output_prompt_path_and_condition_metadata(self):
        for condition, system in (
            ("planner", "plain-system"),
            ("planner-federal", "federal-system"),
        ):
            with self.subTest(condition=condition), tempfile.TemporaryDirectory() as tmp, \
                 mock.patch.object(cloud, "RESULTS_DIR", tmp):
                captured = {}

                def fake_run(cmd, input, **kwargs):
                    captured["cmd"] = cmd
                    captured["input"] = input
                    message_path = cmd[cmd.index("-o") + 1]
                    captured["message_path"] = message_path
                    with open(message_path, "w") as f:
                        f.write(f"synthetic {condition} response")
                    return SimpleNamespace(returncode=0, stdout="", stderr="")

                with mock.patch.object(cloud.subprocess, "run", side_effect=fake_run):
                    out = cloud.run_codex(
                        TIER, FIXTURE, system, "user-task", "planner",
                        condition=condition,
                    )
                with open(out) as f:
                    data = json.load(f)

                expected_prompt = (
                    f"{cloud.PREAMBLES['planner']}\n\n"
                    f"## Investigation Protocol\n\n{system}\n\n"
                    "## Task\n\nuser-task"
                )
                self.assertEqual(captured["input"], expected_prompt)
                self.assertEqual(
                    captured["message_path"],
                    cloud.codex_message_path(TIER["name"], FIXTURE, "planner", condition),
                )
                self.assertEqual(data["response"], f"synthetic {condition} response")
                self.assertTrue(data["done"])
                self.assertEqual(data["_benchmark"]["skill"], "planner")
                self.assertEqual(data["_benchmark"]["condition"], condition)

    def test_error_metadata_keeps_skill_and_condition_separate(self):
        data = self._run_error(SimpleNamespace(returncode=2, stdout="", stderr="boom"))
        self.assertEqual(data["_benchmark"]["skill"], "planner")
        self.assertEqual(data["_benchmark"]["condition"], "planner-federal")
        self.assertTrue(data["error"])

    def test_exception_metadata_keeps_skill_and_condition_separate(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            with mock.patch.object(cloud.subprocess, "run", side_effect=TimeoutError("late")):
                out = cloud.run_codex(
                    TIER, FIXTURE, "system", "user", "planner",
                    condition="planner-federal",
                )
            with open(out) as f:
                data = json.load(f)
        self.assertEqual(data["_benchmark"]["skill"], "planner")
        self.assertEqual(data["_benchmark"]["condition"], "planner-federal")
        self.assertIn("TimeoutError", data["error"])


class ScoringTests(unittest.TestCase):
    def _write(self, directory, name, metadata=None, response="response", **extra):
        benchmark = metadata if metadata is not None else {}
        data = {"response": response, "done": True, "_benchmark": benchmark}
        data.update(extra)
        with open(os.path.join(directory, name), "w") as f:
            json.dump(data, f)

    def test_plain_and_federal_scoring_do_not_overlap(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cloud, "RESULTS_DIR", tmp):
            common = {"fixture_id": FIXTURE, "tier": TIER["name"], "skill": "planner"}
            self._write(tmp, "codex-bench-planner-legacy-55low-response.json", common)
            self._write(
                tmp, "codex-bench-planner-current-55low-response.json",
                {**common, "condition": "planner"},
            )
            self._write(
                tmp, "codex-bench-planner-federal-current-55low-response.json",
                {**common, "condition": "planner-federal"},
            )
            self._write(
                tmp, "codex-bench-planner-federal-legacy-55low-response.json", common,
            )
            self._write(
                tmp, "codex-bench-planner-federal-mislabeled-55low-response.json",
                {**common, "condition": "planner"},
            )
            self._write(
                tmp, "codex-bench-planner-federal-error-55low-response.json",
                {**common, "condition": "planner-federal"}, response="", error="infra",
            )
            with open(os.path.join(tmp, "codex-bench-planner-malformed-55low-response.json"), "w") as f:
                f.write("{")
            with open(os.path.join(tmp, "codex-bench-planner-list-55low-response.json"), "w") as f:
                json.dump([], f)
            self._write(
                tmp, "codex-bench-planner-badmeta-55low-response.json", [],
            )
            self._write(
                tmp, "codex-bench-planner-badresponse-55low-response.json",
                common, response=["not", "text"],
            )
            scored = []
            fake = SimpleNamespace(stdout="Status: PASS\n")
            with mock.patch.object(cloud.subprocess, "run", side_effect=lambda cmd, **kw: scored.append(cmd[2]) or fake):
                plain = cloud.score_codex_results("planner", "planner")
                plain_files = list(scored)
                scored.clear()
                federal = cloud.score_codex_results("planner", "planner-federal")
                federal_files = list(scored)
            self.assertEqual(plain[TIER["name"]]["pass"], 2)
            self.assertEqual(federal[TIER["name"]]["pass"], 1)
            self.assertEqual(len(plain_files), 2)
            self.assertEqual(len(federal_files), 1)
            self.assertTrue(all("federal" not in os.path.basename(p) for p in plain_files))
            self.assertTrue(all("federal" in os.path.basename(p) for p in federal_files))


class CliWiringTests(unittest.TestCase):
    def _main(self, argv):
        with mock.patch.object(cloud.sys, "argv", argv):
            cloud.main()

    def test_single_federal_command(self):
        with mock.patch.object(cloud, "run_codex_planner") as run:
            self._main(["runner", "codex-planner-federal", TIER["name"], FIXTURE])
        run.assert_called_once_with(
            cloud.get_tier("codex", TIER["name"]), FIXTURE, "planner-federal"
        )

    def test_all_federal_command_uses_federal_cache_and_runner(self):
        with mock.patch.object(cloud, "PLANNER_FIXTURES", [FIXTURE]), \
             mock.patch.object(cloud, "result_exists", return_value=False) as exists, \
             mock.patch.object(cloud, "run_codex_planner") as run:
            self._main(["runner", "codex-planner-federal-all", TIER["name"]])
        exists.assert_called_once_with(
            "codex", TIER["name"], FIXTURE, "planner", "planner-federal"
        )
        run.assert_called_once_with(
            cloud.get_tier("codex", TIER["name"]), FIXTURE, "planner-federal"
        )

    def test_federal_score_command(self):
        with mock.patch.object(cloud, "score_codex_results") as score:
            self._main(["runner", "score-codex-planner-federal"])
        score.assert_called_once_with("planner", "planner-federal")


if __name__ == "__main__":
    unittest.main()
