---
name: maintain-accessibility-skills
description: Safely maintain the public accessibility-skills repository. Use when adding tracked-file hygiene scanners, proving whether reset or rebase work was lost, splitting mixed changes into focused commits, or recovering review-worthy commits made on the local default branch.
---

# Maintain Accessibility Skills

Apply the matching workflow below. Preserve the exact checkout and dirty baseline before changing history or staging files.

## Add a tracked-file hygiene scanner

1. Define the scanner's boundary as Git-tracked files.
2. Exclude the scanner's own path if its source must contain the forbidden pattern.
3. Stage the scanner, then run it. An untracked scanner cannot prove its behavior after commit.
4. Manually inspect the commit message, pull request body, and issue comments because the tracked-file gate cannot see them.

Do not claim a local pass proves the committed gate works unless the scanner was staged during the test.

## Prove history-rewrite safety

1. Locate the exact reset, rebase, or rewrite operation in the reflog.
2. Identify the commit immediately before the operation.
3. Diff that tree against the current tree.
4. Describe the observed delta precisely before saying no work was lost.

A clean status and empty stash list do not prove a history rewrite was safe.

## Split mixed work into focused commits

1. Read every changed and untracked file before proposing the split.
2. Back up files that contain more than one theme.
3. Split mixed files at hunk level instead of assigning the whole file to the first theme.
4. Run project validators on new fixtures and data before committing them.
5. Compare the final committed state with the backup to detect dropped or duplicated content.
6. Run the full applicable suite after the split is complete.

## Recover commits made on the default branch

1. Create a feature branch at the current tip.
2. Push the feature branch and open the pull request.
3. After the commits are safe on the remote, remain on the feature branch while moving the local default-branch ref back to its remote-tracking ref.
4. Check the pull request's remote CI status.

Do not push review-worthy commits directly to the shared default branch. Do not treat local tests as a substitute for the remote gate.

## Guard generated and frozen files

Generated or frozen files — receipts, freeze snapshots, hash-bound manifests, rendered reports — carry a hash or signature that a later hand-edit silently invalidates: the file still looks fine, but the chain it anchored is now a lie. Treat this as a repo trap, not a competence failure — more than one actor hitting the same trap is a property of the repo, and the guard is the warning the repo otherwise lacks.

1. List the project's frozen paths in a manifest (`frozen-files.manifest`), one repo-relative path per line — see `scripts/frozen-files.manifest.example` for the format.
2. Wire `scripts/check_frozen_files.py --staged` into pre-commit and `--range origin/main` into CI, so an edit to any listed path fails closed before it lands.
3. When a frozen file legitimately changes, re-freeze it from stable sources and update the manifest in the same commit — never hand-edit the frozen artifact in place.

Keep the manifest project-specific: never ship a real project's frozen-path list inside a shared skill bundle — only the `.example` template travels.
