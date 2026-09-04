from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts/verify_run_manifests.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("verify_run_manifests", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VerifyRunManifestsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verifier = load_verifier()

    def manifest(self, root, *, status="stale", artifact=None, **overrides):
        target = root / "retained.txt"
        if artifact is None:
            target.write_text("actual", encoding="utf-8")
            artifact = {
                "role": "output",
                "path": "retained.txt",
                "sha256": self.verifier.sha256_path(target),
            }
        data = {
            "schema_version": 1,
            "record_type": "run_manifest",
            "id": "test-run",
            "skill": "test",
            "status": status,
            "status_reasons": ["test"],
            "missing_fields": ["provider.version"],
            "evidence_boundary": "test only",
            "retained_artifacts": [artifact],
        }
        data.update(overrides)
        return data

    def write_manifest(self, root, data, name="manifest.json"):
        manifest_dir = root / "manifests"
        manifest_dir.mkdir(exist_ok=True)
        (manifest_dir / name).write_text(json.dumps(data), encoding="utf-8")
        return manifest_dir

    def test_repository_manifests_validate(self):
        self.assertEqual(self.verifier.validate_directory(REPO_ROOT), 2)

    def test_hash_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            (root / "retained.txt").write_text("actual", encoding="utf-8")
            manifest_dir = self.write_manifest(
                root,
                self.manifest(root, artifact={"role": "output", "path": "retained.txt", "sha256": "0" * 64}),
            )
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, pathlib.Path("manifests"))

    def test_verified_status_is_rejected_for_legacy_records(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            manifest_dir = self.write_manifest(root, self.manifest(root, status="verified"))
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, manifest_dir.relative_to(root))

    def test_short_or_mutable_historical_refs_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            for index, git_ref in enumerate(("666e6eb", "HEAD", "main", "v1.0", "abc^{commit}")):
                artifact = {
                    "role": "output",
                    "path": "retained.txt",
                    "sha256": self.verifier.sha256_path(root / "retained.txt") if (root / "retained.txt").exists() else "",
                    "historical_git_ref": git_ref,
                    "historical_sha256": "0" * 64,
                }
                if not artifact["sha256"]:
                    (root / "retained.txt").write_text("actual", encoding="utf-8")
                    artifact["sha256"] = self.verifier.sha256_path(root / "retained.txt")
                manifest_dir = self.write_manifest(root, self.manifest(root, artifact=artifact), f"bad-ref-{index}.json")
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, manifest_dir.relative_to(root))

    def test_symlinked_artifact_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            outside = root.parent / "outside-retained.txt"
            outside.write_text("outside", encoding="utf-8")
            os.symlink(outside, root / "retained.txt")
            artifact = {"role": "output", "path": "retained.txt", "sha256": self.verifier.sha256_path(outside)}
            manifest_dir = self.write_manifest(root, self.manifest(root, artifact=artifact))
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, manifest_dir.relative_to(root))

    def test_symlinked_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            outside_manifest = root.parent / "outside-manifest.json"
            outside_manifest.write_text(json.dumps(self.manifest(root)), encoding="utf-8")
            manifest_dir = root / "manifests"
            manifest_dir.mkdir()
            os.symlink(outside_manifest, manifest_dir / "manifest.json")
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, pathlib.Path("manifests"))

    def test_duplicate_manifest_ids_and_artifacts_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            manifest_dir = self.write_manifest(root, self.manifest(root))
            self.write_manifest(root, self.manifest(root), "duplicate-id.json")
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, manifest_dir.relative_to(root))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            target = root / "one.txt"
            target.write_text("one", encoding="utf-8")
            artifact = {"path": "one.txt", "sha256": self.verifier.sha256_path(target)}
            artifacts = [
                {"role": "output", **artifact},
                {"role": "summary", **artifact},
            ]
            manifest_dir = self.write_manifest(root, self.manifest(root, retained_artifacts=artifacts))
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, manifest_dir.relative_to(root))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            first = root / "one.txt"
            second = root / "two.txt"
            first.write_text("one", encoding="utf-8")
            second.write_text("two", encoding="utf-8")
            artifacts = [
                {"role": "output", "path": "one.txt", "sha256": self.verifier.sha256_path(first)},
                {"role": "output", "path": "two.txt", "sha256": self.verifier.sha256_path(second)},
            ]
            manifest_dir = self.write_manifest(root, self.manifest(root, retained_artifacts=artifacts))
            with self.assertRaises(self.verifier.ManifestError):
                self.verifier.validate_directory(root, manifest_dir.relative_to(root))

    def test_known_absent_paths_reject_parent_and_dangling_symlinks(self):
        for absent_path, setup in (
            ("linked.json", lambda root: os.symlink(root.parent, root / "linked.json")),
            ("missing.json", lambda root: os.symlink(root.parent / "does-not-exist", root / "missing.json")),
            ("missing-parent/missing.json", lambda root: os.symlink(root.parent, root / "missing-parent")),
        ):
            with self.subTest(absent_path=absent_path), tempfile.TemporaryDirectory() as temporary_directory:
                root = pathlib.Path(temporary_directory)
                data = self.manifest(
                    root,
                    status="invalid",
                    record_type="gap_record",
                    missing_fields=["raw_output"],
                    known_absent_artifacts=[{
                        "path": absent_path,
                        "reason": "test",
                        "absence_from_reachable_history": False,
                    }],
                )
                data.pop("skill")
                setup(root)
                manifest_dir = self.write_manifest(root, data)
                with self.assertRaises(self.verifier.ManifestError):
                    self.verifier.validate_directory(root, manifest_dir.relative_to(root))


if __name__ == "__main__":
    unittest.main()
