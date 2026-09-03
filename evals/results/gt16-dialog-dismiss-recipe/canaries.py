#!/usr/bin/env python3
"""Scorer-discrimination canaries for the GT-16 pair (a11y-test-recipe), fixture rev3 / rubric 1.3.

The BUG rubric is the first to use score_output.py's explicit `keywords_all`
field with any-of groups (2026-09-03). The first-four-words fallback is
polarity-blind on this fixture: every review that quotes the selector —
including one that ratifies it — would score the must-find. And because the
scorer's abort threshold is 0.4, two separate must-finds could be half-earned
by a review that ratifies the FAIL. So the must-find is ONE item requiring
three groups at once: names the semantics, names the remedy or name source,
and withdraws the filed FAIL.

Cases (the lettered ones are the bench-reviewer gate's probes against rev1,
which rev1 scored wrongly — see bench-reviewer-gate-opus-rev1.md, C-2):

    trap-only (REVISE, blames the component)              must 0/1 -> FAIL
    A  wrong diagnosis, "text content", FAIL stands        must 0/1 -> FAIL   (rev1: PASS)
    B  ratifies FAIL + getByRole "nit"                     must 0/1 -> FAIL   (rev1: PASS)
    C  ratifies FAIL, quotes trace, "not a false positive" must 0/1 -> FAIL; should not credited
    D  correct, never types the literal `has-text`         must 1/1 -> PASS   (rev1: FAIL)
    correct review                                         must 1/1, should 1/1 -> PASS
    CLEAN correct ACCEPT                                    PASS
    CLEAN lint-style REVISE (flags p:has-text)              FAIL  (FALSE ALARM)
    E  CLEAN flags the rev1 focus-return defect             FAIL  (FALSE ALARM — correct under rev2, where the defect is repaired)
    P1a ratifies: "dialog does not support keyboard access"  must 0/1 -> FAIL   (rev2: PASS — gate rev2 C-1)
    P1b ratifies: "unsupported in older AT"                 must 0/1 -> FAIL   (rev2: PASS)
    P1c ratifies: "confirmed genuine, not spurious"          must 0/1 -> FAIL   (rev2: PASS — polarity inversion)
    P7  correct diagnosis, then certifies the dialog         PASS by design — the over-claim is hand-adjudicated; the scorer cannot see it
    R1  ratifies: "a keyboard route … does not exist"        must 0/1 -> FAIL   (rubric 1.2: PASS — gate rev3 C-1)
    R2  ratifies: "not in the component's focus trap"        must 0/1 -> FAIL   (rubric 1.2: PASS)
    R3  ratifies: "ruled out a false positive"               must 0/1 -> FAIL   (rubric 1.2: PASS)
    N1  ratifies: "the trace contradicts nothing"            must 0/1 -> FAIL   (rubric 1.2: PASS)
    G2  correct: "does not match the accessible name"        must 1/1 -> PASS   (rubric 1.2: FAIL — window gated group 2)
    N5  correct: "is not sound; withdraw it"                 must 1/1 -> PASS   (rubric 1.2: FAIL)
    N6  correct: "does not support it, so retract"           must 1/1 -> PASS   (rubric 1.2: FAIL)

Line numbers inside the review texts are fixture-relative; a model reading
prompts/*.blind.md sees every line +2 (the task prefix is prompt lines 1-2).

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

# (fixture, label, expected Status, required output line, forbidden output line or None, review text)
CASES = [
 (BUG, "trap-only", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.5.3): the close button has no visible text label; add the word Close
  so users can see what it does (dialog-dismiss-recipe.md:95-99). Its aria-label
  alone is not enough.
  MAJOR (2.4.3): initial focus should land on the heading, not Cancel (:56-57).
  MINOR: the page has two controls named Close — the account section's Close
  account button (:32-34) should be renamed to avoid the collision.
  MINOR: six Tab presses is an arbitrary bound (:190)."""),
 (BUG, "A-wrong-diagnosis", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  MAJOR: `button:has-text("Close")` (:185) matches on text content anywhere in
  the page, so it is not scoped to the dialog and can reach the page underneath;
  use dialog.locator('button:has-text("Close")') instead. The 2.1.1 FAIL stands
  until the scoped selector is re-run."""),
 (BUG, "B-ratifies-with-nit", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): the close control is genuinely not reachable — the recipe
  pressed Tab six times and `button:has-text("Close")` never received focus
  (:195, :226). The component must add the close button to the focus trap.
  As a nit, prefer getByRole over `button:has-text("Close")`; the aria-label is
  "Close dialog" so getByRole('button', { name: 'Close dialog' }) reads better."""),
 (BUG, "C-ratifies-quotes-trace", "FAIL", "Must-find issues: 0/1", "Should-find issues: 1/1",
  """VERDICT: REVISE
  CRITICAL (2.1.1): confirmed. trace.json (:245-251) shows focus cycling
  Cancel/Delete/Close dialog but the assertion at :195 still failed, so the
  control the test targets is not operable by keyboard. This is not a false
  positive; the test instrument recorded it twice. Fix the component's focus
  handling before re-running."""),
 (BUG, "D-correct-no-literal", "PASS", "Must-find issues: 1/1", None,
  """VERDICT: REVISE
  CRITICAL: the locator on :185 selects by rendered text content, not by
  accessible name. The close control (:95-99) has no text — its name "Close
  dialog" comes from aria-label — so the locator cannot match it; the call log
  (:226) shows it resolved to the inert "Close account" button instead. Build the
  locator from the census row (:261): getByRole('button', { name: 'Close dialog',
  exact: true }) scoped to the dialog. The filed 2.1.1 FAIL (:275) is therefore
  unsupported and must be withdrawn; the trace at :247 and :250 shows the control
  focused on the second press of each cycle."""),
 (BUG, "correct", "PASS", "Must-find issues: 1/1", None,
  """VERDICT: REVISE
  CRITICAL: `button:has-text("Close")` (:185) matches rendered text content, not the
  accessible name. The close control's name comes from aria-label over an
  aria-hidden svg (:95-99) and has no text content, so the locator bound to the
  inert "Close account" button — the call log says so (:226). Derive the selector
  from the census row (:261): dialog.getByRole('button', { name: 'Close dialog', exact: true }).
  CRITICAL: the filed 2.1.1 FAIL (:275) is contradicted by its own trace — steps 2
  and 5 (:247, :250) record focus on "Close dialog". The finding is an instrument
  artifact and must be withdrawn; re-run before filing anything."""),
 (BUG, "P1a-ratifies-does-not-support", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): the dialog does not support keyboard access to its close
  control — `button:has-text("Close")` (:185) never received focus after six Tab
  presses, and the aria-label on the icon button (:95) is not enough on its own.
  The component must add the close button to the focus trap. The FAIL stands as
  filed."""),
 (BUG, "P1b-ratifies-unsupported", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL: the close control relies on aria-label over an aria-hidden svg (:95-99),
  which is unsupported in older assistive technology, and `button:has-text("Close")`
  (:185) confirms it is unreachable. Ratify the 2.1.1 FAIL and fix the component."""),
 (BUG, "P1c-ratifies-not-spurious", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): confirmed genuine, not spurious — `button:has-text("Close")`
  (:185) could not be focused and the aria-label (:95) does not change that. The
  filed FAIL is correct; the component must expose the control in the trap."""),
 (BUG, "P7-correct-then-certifies", "PASS", "Must-find issues: 1/1", None,
  """VERDICT: REVISE
  CRITICAL: `button:has-text("Close")` (:185) matches text content, not the
  accessible name from aria-label (:95); the call log (:226) shows it bound to
  Close account. Use getByRole from the census row (:261). The filed FAIL (:275)
  is refuted by the trace (:247, :250) and must be withdrawn. The dialog PASSES
  2.1.1 and can be certified conformant on this evidence."""),
 (BUG, "R1-ratifies-does-not-exist", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): a keyboard route to the close control does not exist —
  `button:has-text("Close")` (:185) never received focus, and the aria-label (:95)
  does not make the button reachable. Ratify the filed FAIL and add the button to
  the focus trap."""),
 (BUG, "R2-ratifies-not-in-component", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): the close button is not in the component's focus trap, which is
  why `button:has-text("Close")` (:185) was never focused; the aria-label (:95) is
  irrelevant to reachability. The filed FAIL is correct as recorded."""),
 (BUG, "R3-ratifies-ruled-out-false-positive", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): I considered whether this was a false positive and ruled that
  out — `button:has-text("Close")` (:185) is the right control and it never got
  focus despite its aria-label (:95). The FAIL stands; fix the component."""),
 (BUG, "N1-ratifies-contradicts-nothing", "FAIL", "Must-find issues: 0/1", None,
  """VERDICT: REVISE
  CRITICAL (2.1.1): the trace contradicts nothing here — `button:has-text("Close")`
  (:185) was never focused and the aria-label (:95) does not change that. The 2.1.1
  FAIL stands as filed."""),
 (BUG, "G2-correct-does-not-match-name", "PASS", "Must-find issues: 1/1", None,
  """VERDICT: REVISE
  CRITICAL: the selector at :185 does not match the accessible name of the control
  under test — has-text reads rendered text, and the button (:95-99) has none. The
  call log (:226) proves it resolved to "Close account". The filed FAIL (:275) is an
  instrument artifact and must be withdrawn; re-run with a role+name locator."""),
 (BUG, "N5-correct-not-sound-withdraw", "PASS", "Must-find issues: 1/1", None,
  """VERDICT: REVISE
  CRITICAL: `button:has-text("Close")` (:185) matches text content; the control's
  name is aria-label (:95). Rebuild the locator from the census row (:261) with
  getByRole. The filed 2.1.1 FAIL is not sound; withdraw it and re-run."""),
 (BUG, "N6-correct-does-not-support-retract", "PASS", "Must-find issues: 1/1", None,
  """VERDICT: REVISE
  CRITICAL: has-text (:185) cannot see the aria-label name (:95); the call log
  (:226) shows the wrong element. Use getByRole from the census (:261). The trace
  does not support it, so retract the finding and re-run."""),
 (CLEAN, "correct-accept", "PASS", "Verdict correct: YES", None,
  """VERDICT: ACCEPT
  The selector for the control under test is role+name with exact matching (:187),
  taken from the census row (:236); the trace reaches it on press 2 (:225) and the
  dismiss/return step executed (:226). p:has-text on the description (:183) targets
  a text-bearing element and resolves. Both PASS rows carry a claim_boundary
  (:251, :261). ENHANCEMENT: Escape and Shift+Tab wrap are not exercised."""),
 (CLEAN, "lint-style-revise", "FAIL", "FALSE ALARM", None,
  """VERDICT: REVISE
  MAJOR: `p:has-text("cannot be undone")` (:183) — has-text selectors are unreliable;
  use getByText. MAJOR: exact: true (:187) makes the locator brittle. MINOR: the
  close button needs visible text (:95-99)."""),
 (CLEAN, "E-flags-focus-return", "FAIL", "FALSE ALARM", None,
  """VERDICT: REVISE
  MAJOR (2.4.3): focus return is unreliable — the trigger is inside #app-root
  (:17), which is inert until the state update flushes, so focusing it from the
  dialog (:60) is a no-op and focus falls to body. The trace's step 3 (:226)
  records behaviour the component cannot produce."""),
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
for fid, label, want_status, want_line, forbid_line, text in CASES:
    out = run(fid, text)
    status = next((l for l in out.splitlines() if l.startswith("Status:")), "Status: ?")
    ok = (f"Status: {want_status}" in status) and (want_line in out) and (forbid_line is None or forbid_line not in out)
    bad += 0 if ok else 1
    extra = f"  forbid[{forbid_line}]: {'absent' if forbid_line not in out else 'PRESENT'}" if forbid_line else ""
    print(f"{'ok ' if ok else 'BAD'} {fid:30s} {label:24s} -> {status}   [{want_line}: {'yes' if want_line in out else 'NO'}]{extra}")
sys.exit(1 if bad else 0)
