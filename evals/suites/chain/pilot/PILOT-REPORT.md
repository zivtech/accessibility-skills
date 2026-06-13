# Chain Eval Pilot Report — /a11y-workflow

**Date**: 2026-06-13 · **Set**: modal-broken-focus-trap, video-tutorial-no-captions,
login-form-clean (protocol set) · **Mechanism**: Claude Code subagents (Haiku scout +
Opus planner/critic/audit), hand-orchestrated Mode 1 steps 1–4, depth-1 · **Cost**: 12
subagent calls (3 Haiku + 9 Opus; all 3 fixtures escalated → 3 audits).

## Headline

**The instrument is NOT ready for the full 8-fixture run.** The chain *under test* performed
encouragingly — file handoff was perfect, audits were the strongest link (they caught a critic
false-positive and re-grounded an artifact mismatch), and escalation mechanically fired correctly
on both HAS-BUGS fixtures. But the **measurement apparatus** has a contamination hole and four
scorer defects that make the automated numbers untrustworthy. Fix the instrument (I1–I4 below)
before paying for the remaining 5 fixtures, or the full run's scores will be systematically wrong.

Manual fixture results: **modal PASS, video PASS\* (S3 contaminated), login FAIL (mislabeled fixture)**.

---

## INSTRUMENT findings (defects in the eval/harness — fix in this plan's files)

**I1 — CRITICAL: ground-truth leak; agents are not sandboxed.** Targets live under
`evals/suites/chain/targets/`, so a critic with Read/Glob can navigate to
`evals/suites/chain/rubrics/<id>.chain.yaml` and read the expected alarm levels, tracer, and
acceptable verdict. The **video critic did exactly this** — it opened with "Expected alarm levels
are pre-defined: auditory_access: HIGH…" and then produced a perfect 7/7 match. Whether a stage
stays blind is currently left to the agent's own discretion: of the 5 judgment stages run (3
critics + 2 audits that could peek), 1 peeked, 2 critics explicitly stayed blind, 2 audits stayed
blind. Any peeking stage's S3/S4 is invalid. **Fix options**: (a) move `targets/` outside the eval
tree and pass only the target path; (b) inject the component code into the prompt instead of a
path under the suite; (c) sandbox subagent file access to the target dir; (d) at minimum, the
orchestrator must instruct every stage not to read `rubrics/` or `*.metadata.yaml`.

**I2 — MAJOR: critic perspective taxonomy is unstable and doesn't match the rubric's 7.** Three
critics produced three vocabularies: modal = 6 lenses (screen reader / keyboard-only / low vision /
voice control / switch access / cognitive); login = a different 7 (…low vision / motor / speech-voice
/ seizure-vestibular); video = the rubric's exact 7 — *but only because it peeked (I1)*. `score_chain.py`'s
`P_MAP` lacks "low vision", "voice control", "switch access", "speech/voice", "seizure/vestibular",
so real findings register as `MISSING` → S3 artificially low (modal 0.214, login 0.429; manual ~0.6
and ~0.86). **Fix**: standardize the critic's perspective output to the 7 canonical keys, OR expand
`P_MAP` and add an explicit lens→perspective crosswalk.

**I3 — MAJOR: tracer match is too literal.** `score_chain.py` does an 18-char exact substring match.
Both surviving tracers scored 0 ("No focus movement INTO the dialog" ≠ "Focus not moved to modal";
"no `<track>` child" ≠ "Missing `<track kind=captions>`") even though both concepts were present in
the audit. **Fix**: keyword-set or concept match (e.g., require N of the tracer's content words), not
a leading-substring match.

**I4 — MAJOR: audit-verdict token match false-positives on checklist "PASS" lines.** login's audit
verdict was REVISE (3 MAJOR), but the scorer reported audit-verdict=1 ("PASS" FOUND) because the word
"PASS" appears in the audit's checklist-pass rows. **Fix**: parse the explicit verdict/recommendation
line, not any "PASS" token. (The scorer's own docstring says "confirm by hand" — confirmed wrong here.)

**I5 — MINOR: S5a leak heuristic false-positives.** It flags LOW-perspective "leakage" whenever a
LOW-perspective keyword co-occurs anywhere with "major/finding/issue". Both modal and login audits
scored S5a=0 despite scoping correctly to escalated perspectives. **Fix**: scope the check to
per-perspective sections.

**I6 — MINOR: filename mismatch.** Protocol/RESULTS-TEMPLATE say save stage outputs as `.md`;
`score_chain.py` reads `.txt`. **Fix**: scorer should read `.md` with `.txt` fallback (or the protocol
should standardize on `.txt`). (Worked around in the pilot by copying `.md`→`.txt`.)

**I7 — MINOR: scout systematically over the 1500-char budget.** All 3 scouts produced 1779–2072 chars
→ S1a=0 every time, dragging S1 mean to 1.0 (below the 1.5 threshold) on otherwise-fine recon. The
budget is unrealistic for a multi-file directory target, OR the scout prompt invites too much. **Fix**:
raise the S1a budget to ~2000, or tighten the scout prompt to enforce brevity.

**I8 — FIXTURE: login-form-clean is mislabeled.** It is tagged CLEAN with `expected_audit_verdict: PASS`
and narrow `expected_escalated_perspectives: [cognitive_neurodivergent]`. But the component carries a
genuine MAJOR stale-error-state bug (errors computed only on submit, never cleared on change; `submitted`
latches true → corrected fields keep `aria-invalid="true"` + red border + stale error text). The planner,
critic, AND audit all independently found it (verified in source: `component.jsx:53/70`, `onChange` at
`:51/:68`). So the "scope-inflated escalation" (S4=0) and "non-PASS audit" are the chain correctly
catching a real defect the fixture's static alarm ground truth missed — NOT a chain false-positive.
**Fix**: either re-label the fixture (it is not clean) and update its rubric/ground truth, or fix the
component so it is genuinely clean. As-is it cannot serve as the "narrow-escalation + clean-audit" probe.

---

## CHAIN findings (about the /a11y-workflow product — REPORT, do not fix here; the workflow is out of scope)

**C1 — Critic prose can contradict its own structured alarms.** Modal critic flagged 3 perspectives
MEDIUM, then wrote "This does NOT require a separate perspective-audit escalation." A human following
the prose would NOT escalate (S4 miss); the documented mechanical rule (any MEDIUM/HIGH → escalate)
saved it. The chain's headline metric depends on the orchestrator obeying the structured alarm, not
the prose. The team/skill should state that the structured alarm is authoritative.

**C2 — Critic↔audit artifact mismatch in pre-implementation mode.** The critic reviews the PLAN
(proposed fixes); SKILL.md Step 4 points the audit at SOURCE files (current broken code). The modal
audit caught that the escalation described proposed-fix elements ("white box-shadow ring", "error
summary tabindex") absent from the source, and re-grounded every finding in actual code. Graceful,
but the chain is passing plan-level findings to a source-level reviewer. Consider giving the audit the
plan path too, or clarifying which artifact the audit reviews pre-implementation.

**C3 — Critic over-escalated keyboard on login (real false positive); the audit corrected it.** The
login critic flagged keyboard MEDIUM over a "focus-yank on every submit" — but the source has NO focus
management at all (no `.focus()`/`useRef`/`useEffect`). The critic alarmed on a *feared* implementation.
The audit verified the source and overturned it. Net: the audit is a valuable false-positive backstop;
the critic invented an alarm from an imagined implementation.

**C4 — Critic severity under-rating.** Modal critic rated keyboard/SR MEDIUM where the source defects
(no `role="dialog"`, no focus management at all) are HIGH. Escalation still fired (MEDIUM triggers it),
but the calibration is soft on a fixture whose expected levels are HIGH.

---

## What worked (the encouraging half)

- **S2 handoff: 2/2 on every fixture.** Planner wrote to `docs/a11y-plans/<date>-<feature>-a11y-plan.md`
  at the documented path each time; all plans carried 8+ phase sections; the critic read the plan file
  cleanly. The planner→file→critic seam — a prime suspected failure point — is solid.
- **Audits are the strongest link.** All 3 scoped correctly to the escalated perspectives, found real
  issues, AND added value the critic missed: corrected a false positive (C3), re-grounded an artifact
  mismatch (C2), and gave a genuinely expert 1.2.3-vs-1.2.5 analysis (video). 2/2 audits that could have
  peeked stayed blind.
- **Escalation mechanically correct** on both HAS-BUGS fixtures; **both defined tracers survived** the
  full chain (manual verification).
- **Planners were uniformly strong and blind** — each went beyond the scout recon by reading source
  (modal: focus-never-enters-dialog; login: stale-error lifecycle; video: kept `aria-live="off"`).

---

## Verdict on the pilot's question

**Is the instrument ready for the full 8-fixture run? NO — not until I1 (contamination) and I2–I4
(scorer parsing) are fixed.** With those open, the full run's automated S3 would be under-counted, the
tracer survival rate would false-negative, audit verdicts would false-positive, and any peeking critic
would silently invalidate its fixture. I8 (login mislabel) must also be resolved before fixtures 4–5
can serve as clean-audit probes.

**The chain under test, by contrast, looks healthy** on this evidence: handoff solid, escalation
mechanically correct, audits excellent. The bottleneck is the *measurement*, which is the right thing
for a pilot to discover before money is spent on the full run.

## Recommended next actions (a follow-up plan, not this one)
1. Fix I1: sandbox/relocate so judgment stages cannot read the rubrics. (Blocks a trustworthy full run.)
2. Fix I2–I4 in `score_chain.py` (taxonomy crosswalk, concept-based tracer match, verdict-line parse).
3. Resolve I8: re-label login-form-clean or fix the component; pick a genuinely-all-LOW CLEAN fixture
   for the never-escalate branch (the protocol's known S4 gap).
4. Re-run the pilot after fixes to confirm the instrument before the full 8-fixture run.
