#!/usr/bin/env python3
"""Verify retained-artifact hashes in historical evaluation run manifests.

This verifier establishes file integrity only.  It deliberately does not turn
an incomplete historical record into a replayable or provider-verified run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_DIR = pathlib.Path("evals/results/run-manifests")
ALLOWED_STATUSES = {"stale", "invalid"}
FULL_COMMIT_RE = re.compile(r"[0-9a-f]{40}")


class ManifestError(AssertionError):
    """Raised when a manifest is malformed or no longer matches its artifacts."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def sha256_path(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_relative_path(path_value: str, label: str) -> pathlib.Path:
    path = pathlib.PurePosixPath(path_value)
    require(not path.is_absolute() and ".." not in path.parts, f"{label}: unsafe path {path_value!r}")
    return pathlib.Path(path)


def ensure_path_inside_root(repo_root: pathlib.Path, path: pathlib.Path, label: str) -> pathlib.Path:
    root = repo_root.resolve()
    try:
        relative = path.relative_to(repo_root)
    except ValueError as exc:
        raise ManifestError(f"{label}: path is outside repository root") from exc
    current = repo_root
    for part in relative.parts:
        current /= part
        require(not current.is_symlink(), f"{label}: symlinked path is not allowed: {relative}")
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(root), f"{label}: resolved path escapes repository root")
    return resolved


def require_full_commit(repo_root: pathlib.Path, git_ref: object, label: str) -> str:
    require(isinstance(git_ref, str) and FULL_COMMIT_RE.fullmatch(git_ref), f"{label}: historical_git_ref must be a full lowercase commit hash")
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{git_ref}^{{commit}}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    require(result.returncode == 0, f"{label}: historical_git_ref is not a commit object")
    resolved = result.stdout.strip()
    require(resolved == git_ref, f"{label}: historical_git_ref did not resolve to itself")
    return git_ref


def sha256_at_git_ref(repo_root: pathlib.Path, git_ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{git_ref}:{path}"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"{path}: unavailable at git ref {git_ref}")
    return hashlib.sha256(result.stdout).hexdigest()


def is_absent_from_reachable_history(repo_root: pathlib.Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "log", "--all", "--format=%H", "--", path],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    require(result.returncode == 0, f"unable to inspect reachable history for {path}")
    return not result.stdout.strip()


def ensure_absent_path_is_safe(repo_root: pathlib.Path, rel_path: pathlib.Path, label: str) -> pathlib.Path:
    """Reject symlinks before checking whether a claimed-absent path exists."""
    target = repo_root / rel_path
    current = repo_root
    for index, part in enumerate(rel_path.parts):
        current /= part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            break
        except OSError as exc:
            raise ManifestError(f"{label}: cannot inspect absent path component {current}: {exc}") from exc
        require(not stat.S_ISLNK(mode), f"{label}: symlinked absent-path component is not allowed: {rel_path}")
        if index < len(rel_path.parts) - 1:
            require(stat.S_ISDIR(mode), f"{label}: absent-path parent is not a directory: {rel_path}")
    require(not os.path.lexists(target), f"{label}: expected absent artifact exists or is a symlink: {rel_path}")
    return target


def validate_artifact(repo_root: pathlib.Path, manifest_label: str, artifact: object) -> None:
    require(isinstance(artifact, dict), f"{manifest_label}: artifact is not an object")
    for field in ("role", "path", "sha256"):
        require(isinstance(artifact.get(field), str) and artifact[field], f"{manifest_label}: artifact missing {field}")
    rel_path = validate_relative_path(artifact["path"], manifest_label)
    target = repo_root / rel_path
    require(target.is_file(), f"{manifest_label}: retained artifact missing: {rel_path}")
    ensure_path_inside_root(repo_root, target, manifest_label)
    actual_hash = sha256_path(target)
    require(actual_hash == artifact["sha256"], f"{manifest_label}: SHA-256 mismatch for {rel_path}")

    git_ref = artifact.get("historical_git_ref")
    historical_hash = artifact.get("historical_sha256")
    require((git_ref is None) == (historical_hash is None), f"{manifest_label}: historical ref/hash must appear together")
    if git_ref is not None:
        require_full_commit(repo_root, git_ref, manifest_label)
        require(isinstance(historical_hash, str) and historical_hash, f"{manifest_label}: empty historical_sha256")
        require(
            sha256_at_git_ref(repo_root, git_ref, artifact["path"]) == historical_hash,
            f"{manifest_label}: historical SHA-256 mismatch for {rel_path} at {git_ref}",
        )


def validate_manifest(repo_root: pathlib.Path, manifest_path: pathlib.Path) -> None:
    ensure_path_inside_root(repo_root, manifest_path, "manifest")
    label = str(manifest_path.relative_to(repo_root))
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{label}: invalid JSON: {exc}") from exc
    require(data.get("schema_version") == 1, f"{label}: unsupported schema_version")
    require(data.get("record_type") in {"run_manifest", "gap_record"}, f"{label}: invalid record_type")
    require(isinstance(data.get("id"), str) and data["id"], f"{label}: missing id")
    require(data.get("status") in ALLOWED_STATUSES, f"{label}: invalid status")
    if "integrity_verified" in data:
        require(data["integrity_verified"] is True, f"{label}: integrity_verified must be true when present")
    require(isinstance(data.get("evidence_boundary"), str) and data["evidence_boundary"], f"{label}: missing evidence_boundary")
    missing_fields = data.get("missing_fields")
    require(isinstance(missing_fields, list), f"{label}: missing_fields must be a list")
    require(all(isinstance(item, str) and item for item in missing_fields), f"{label}: invalid missing_fields entry")
    if missing_fields:
        require(data["status"] in {"stale", "invalid"}, f"{label}: incomplete provenance cannot be verified")
    require(isinstance(data.get("status_reasons"), list) and data["status_reasons"], f"{label}: missing status_reasons")
    require(all(isinstance(item, str) and item for item in data["status_reasons"]), f"{label}: invalid status_reasons entry")

    artifacts = data.get("retained_artifacts")
    require(isinstance(artifacts, list) and artifacts, f"{label}: no retained_artifacts")
    roles = [artifact.get("role") for artifact in artifacts if isinstance(artifact, dict)]
    paths = [artifact.get("path") for artifact in artifacts if isinstance(artifact, dict)]
    require(len(roles) == len(artifacts) and len(set(roles)) == len(roles), f"{label}: artifact roles must be unique")
    require(len(paths) == len(artifacts) and len(set(paths)) == len(paths), f"{label}: artifact paths must be unique")
    for artifact in artifacts:
        validate_artifact(repo_root, label, artifact)

    if data["record_type"] == "run_manifest":
        require(isinstance(data.get("skill"), str) and data["skill"], f"{label}: run manifest missing skill")
    else:
        require(data["status"] == "invalid", f"{label}: gap records must be invalid")
        absent = data.get("known_absent_artifacts")
        require(isinstance(absent, list) and absent, f"{label}: gap record missing known_absent_artifacts")
        for item in absent:
            require(isinstance(item, dict), f"{label}: invalid known_absent_artifacts entry")
            require(isinstance(item.get("path"), str) and item["path"], f"{label}: absent artifact missing path")
            require(isinstance(item.get("reason"), str) and item["reason"], f"{label}: absent artifact missing reason")
            rel_path = validate_relative_path(item["path"], label)
            ensure_absent_path_is_safe(repo_root, rel_path, label)
            if item.get("absence_from_reachable_history") is True:
                require(is_absent_from_reachable_history(repo_root, item["path"]), f"{label}: expected absent artifact is reachable in history: {rel_path}")
            elif "absence_from_reachable_history" in item:
                require(item["absence_from_reachable_history"] is False, f"{label}: absence_from_reachable_history must be boolean")


def validate_directory(repo_root: pathlib.Path, manifest_dir: pathlib.Path = DEFAULT_MANIFEST_DIR) -> int:
    manifest_dir = validate_relative_path(str(manifest_dir), "manifest directory")
    root = repo_root / manifest_dir
    ensure_path_inside_root(repo_root, root, "manifest directory")
    require(root.is_dir(), f"manifest directory missing: {manifest_dir}")
    manifests = sorted(root.glob("*.json"))
    require(manifests, f"no manifests in {manifest_dir}")
    ids: set[str] = set()
    for manifest in manifests:
        validate_manifest(repo_root, manifest)
        manifest_id = json.loads(manifest.read_text(encoding="utf-8"))["id"]
        require(manifest_id not in ids, f"duplicate manifest id: {manifest_id}")
        ids.add(manifest_id)
    return len(manifests)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-dir", type=pathlib.Path, default=DEFAULT_MANIFEST_DIR)
    args = parser.parse_args()
    try:
        count = validate_directory(REPO_ROOT, args.manifest_dir)
    except ManifestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: verified SHA-256 for every retained artifact in {count} run manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
