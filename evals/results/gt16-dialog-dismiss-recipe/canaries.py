#!/usr/bin/env python3
"""Scorer-discrimination canaries for the GT-16 pair (a11y-test-recipe).

The BUG rubric is the first to use score_output.py's explicit
`keywords_all` / `keywords_any` fields (2026-09-03). The first-four-words
fallback is polarity-blind on this fixture: every review that quotes the
selector — including one that ratifies it — would score the must-find.
The explicit fields demand `has-text` AND one of the semantics/remedy
tokens. These canaries are the standing proof; the CLEAN rows exercise the
verdict gate.

    trap-only (REVISE, blames the component)      must 0/1 -> FAIL
    wrong diagnosis (scope :has-text to dialog)   must 0/1 -> FAIL
    remedy without the selector named              must 0/1 -> FAIL (documented limit)
    correct review                                 must 1/1, should 1/1 -> PASS
    CLEAN correct ACCEPT                            PASS
    CLEAN lint-style REVISE (flags p:has-text)      FAIL

Run:  python3 evals/results/gt16-dialog-dismiss-recipe/canaries.py    (exit 0 = CLEAN)
"""
import contextlib, importlib.util, io, json, os, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "ollama"))
spec = importlib.util.spec_from_file_location("so", os.path.join(REPO, "ollama", "score_output.py"))
so = importlib.util.module_from_spec(spec); spec.loader.exec_module(so)
RUBRICS = os.path.join(REPO, "evals", "suites", "a11y-test-recipe", "rubrics")

BUG = "dialog-dismiss-recipe"
CLEAN = "dialog-dismiss-recipe-clean"

CASES = [
 (BUG, "trap-only", "FAIL", "Must-find issues: 0/1",
  """VERDICT: REVISE
  CRITICAL (2.5.3): the close button has no visible text label; add the word Close
  so users can see what it does (dialog-dismiss-recipe.md:96-100).
  MAJOR (2.4.3): initial focus should land on the heading, not Cancel (:60-62).
  MINOR: the page has two controls named Close — the account section's Close
  account button (:37-39) should be renamed to avoid the collision.
  MINOR: six Tab presses is an arbitrary bound (:190)."""),
 (BUG, "wrong-diagnosis", "FAIL", "Must-find issues: 0/1",
  """VERDICT: REVISE
  MAJOR: `button:has-text("Close")` (:186) is not scoped to the dialog, so it
  can reach the page underneath; use dialog.locator('button:has-text("Close")')
  instead. The 2.1.1 FAIL stands until the scoped selector is re-run."""),
 (BUG, "remedy-without-selector", "FAIL", "Must-find issues: 0/1",
  """VERDICT: REVISE
  CRITICAL: the locator on line 186 should be getByRole('button', { name: 'Close dialog' })
  built from the census row (:255); the current one resolves to Close account."""),
 (BUG, "correct", "PASS", "Must-find issues: 1/1",
  """VERDICT: REVISE
  CRITICAL: `button:has-text("Close")` (:186) matches rendered text content, not the
  accessible name. The close control's name comes from aria-label over an
  aria-hidden svg (:96-100) and has no text content, so the locator bound to the
  inert "Close account" button — the call log says so (:225). Derive the selector
  from the census row (:255): dialog.getByRole('button', { name: 'Close dialog', exact: true }).
  CRITICAL: the filed 2.1.1 FAIL (:270) is contradicted by its own trace — steps 2
  and 5 (:242, :245) record focus on "Close dialog". The finding is an instrument
  artifact and must be withdrawn; re-run before filing anything."""),
 (CLEAN, "correct-accept", "PASS", "Verdict correct: YES",
  """VERDICT: ACCEPT
  The selector for the control under test is role+name with exact matching (:188),
  taken from the census row (:255); the trace reaches it on press 2 and the
  dismiss/return step executed (:230). p:has-text on the description (:184) targets
  a text-bearing element and resolves. ENHANCEMENT: Escape and Shift+Tab wrap are
  not exercised."""),
 (CLEAN, "lint-style-revise", "FAIL", "FALSE ALARM",
  """VERDICT: REVISE
  MAJOR: `p:has-text("cannot be undone")` (:184) — has-text selectors are unreliable;
  use getByText. MAJOR: exact: true (:188) makes the locator brittle. MINOR: the
  close button needs visible text (:96-100)."""),
]

def run(fid, text):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump({"response": text, "done": True}, fh); path = fh.name
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        so.score(path, os.path.join(RUBRICS, f"{fid}.rubric.yaml"))
    os.unlink(path)
    return buf.getvalue()

bad = 0
for fid, label, want_status, want_line, text in CASES:
    out = run(fid, text)
    status = next((l for l in out.splitlines() if l.startswith("Status:")), "Status: ?")
    ok = (f"Status: {want_status}" in status) and (want_line in out)
    bad += 0 if ok else 1
    print(f"{'ok ' if ok else 'BAD'} {fid:30s} {label:24s} -> {status}   [{want_line}: {'yes' if want_line in out else 'NO'}]")
sys.exit(1 if bad else 0)
