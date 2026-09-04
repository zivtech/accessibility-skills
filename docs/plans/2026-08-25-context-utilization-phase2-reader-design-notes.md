# Phase 2.1 — `a11y-evidence-reader` design notes

**Date:** 2026-08-25
**Branch:** `feat/verification-evidence-contract`
**Status:** REVISED after proposal-critic REVISE verdict (6 MAJOR, 5 MINOR — all applied; Q1–Q4 gate-decided, recorded in §6)
**Deliverable:** `.claude/agents/a11y-evidence-reader.md` — **14,430 bytes** (a11y-critic: 41,833; a11y-planner: 46,150; a11y-scout: 2,918). Pre-revision draft was 12,522B; the gate's MAJOR fixes added ~2,400B and its Q3 furniture cuts removed ~500B.
**Binding spec:** `docs/plans/2026-08-24-context-utilization-plan.md` task 2.1 (line 95), Phase 3 blind-curation rule (line 111), design principles 1–3 (lines 58–60)

---

## 1. The one decision everything else follows from

The plan says "evidence-contract-shaped digest." The evidence-finding contract (`docs/a11y-evidence-finding-contract.md`) has 11 required fields. **Four of them are judgments the reader is explicitly forbidden to make** — `severity`, `perspective_alarms`, `expected_behavior`, `section_508_fpc_context`. A reader that filled them would be a critic with a smaller model.

So the def splits the contract into three tiers rather than emitting it whole:

| Tier | Fields | Rule |
|---|---|---|
| **Emit** | `observation_id`, `source`, `handle`, `actual_behavior`, `evidence` | Derivable from the artifact alone |
| **Pass through verbatim, never derive** | `wcag_or_apg`, `finding_id`, `baseline_test`, producing command | If the artifact doesn't state it → `not stated in artifact` |
| **Never emit** | `severity`, `perspective_alarms`, `expected_behavior`, `trend`, `section_508_fpc_context`, any fix/recommendation/"should" | Consumer's job |

Two consequences worth naming, because both are load-bearing and both are where a reviewer should push:

**`observation_id`, not `finding_id`.** Minting a `finding_id` asserts that an observation *is* a finding — a judgment. The reader emits `observation_id` for things it saw, and passes `finding_id` through verbatim only when the artifact already carries one. Provenance stays honest and the consumer still gets a stable handle either way.

**Tool severities stay inside `evidence`.** axe says `impact: serious`; keyboard-a11y-tester says `severity: moderate`. Those are quoted as tool values inside the excerpt, never promoted to a contract `severity` field. The contract's own mapping tables (lines 62, 77) make serious→MAJOR an author's judgment call, and the repo's standing rule is that conformance outcome and impact severity are orthogonal — never derive one from the other. Letting a haiku reader do that mapping silently would import a judgment under an extraction label.

## 2. How the def satisfies each binding-spec bullet

| Spec bullet | Where | Mechanism |
|---|---|---|
| Input = artifact paths + question under adjudication | `<Execution>` 1 | No question supplied → return that fact and **stop**. A reader without a question can only dump — the thing it exists to prevent. |
| Output = contract-shaped digest | `<What_You_Emit>`, `<Output_Format>` | Three-tier field split above |
| Coverage note partitioning read / not read / ambiguous | `<Execution>` 2 + 7, `<Output_Format>` | **The partition is built from a pre-read inventory** (Glob/`ls -l`/`wc -c`), not backfilled from what happened to get read. This is the structural reason silent skipping is impossible — it is not a discipline the model has to remember at the end. |
| Excerpts ≤10 lines, every one tied to a stable handle | `<What_You_Emit>`, `<Constraints>` | Handle forms enumerated: `finding_id`, `file:line`, artifact + jq path, trace `step_id`, image + crop ref. Excerpts must be **verbatim** with `…` elision — a paraphrased excerpt is a second summarization hop and voids the handle (plan principle 2). |
| Nothing else — no recommendations, severity, or fixes | `<What_You_Emit>` never-emit list, `<Constraints>`, `<Execution>` 8 | Includes a keyword-level tell: no sentence containing "should" |
| Vision mode in **this** def | `<Vision_Mode>` | Admissibility gated on the a11y-test evidence table's visual-only row; verdict + crop ref + confidence; interaction-class questions get a refusal, not a pixel view |
| Runtime routing haiku / sonnet / never opus | frontmatter `model:` + `<Model_Routing>` | haiku default (scout precedent); sonnet on caller escalation; opus never, with the reason stated |
| Blind curation (Phase 3 depends on it) | `<Blind_Reading>` — its own top-level block | Five rules: **question reproduced verbatim + `question_source` recorded** (see §2a); no metadata/rubric/scorer/answer-key reads even when handed one; **leading questions get "no row matches," never manufactured corroboration**; no inference of what an artifact "usually" contains; no gap-filling from training knowledge |
| Depth-1, never spawns | frontmatter `tools:` + `<Constraints>` | Config: the allowlist omits the Agent tool. Prose retained to state the intent behind the omission. |
| Honest coverage — unreadable/oversized/missing declared, never silently skipped | `<Execution>` 2, `<Output_Format>` | Eight enumerated NOT-READ reasons; "every inventoried artifact appears in exactly one partition" |
| "artifact says X" vs "artifact absent" | `<What_You_Emit>`, `<Output_Format>` | **Made structural, not exhortative**: absence-of-a-row is a digest line in a separate `Absence claims` section citing the query that returned empty; absence-of-an-artifact is a coverage-note row. Different sections, so they cannot blur. |

## 2a. Question provenance — the blind-curation leak the gate caught

The original draft had the digest header **restate** the question in one line. The gate flagged this as a blind-curation leak, and it is right: the reader's protocol can be perfectly blind while the *question it was handed* was authored by someone looking at ground truth — and a restated question makes that unrecoverable after the fact. The digest looks clean either way.

Fix applied: the header carries the question **verbatim** plus a `question_source:` field naming who or what authored it. `<Blind_Reading>` now leads with the rule and says why ("a restated question destroys the only evidence a later reader has").

**Consequence for Phase 3 that must be honoured at pack construction:** blindness is a property of the *question*, not only of the reader. The lane's pack rules must record, per pack, the verbatim question and its author, and attest that the question was authored **without ground-truth access**. A blind reader answering a ground-truth-informed question is not blind curation, and the pack-omission number (plan line 112) would be measuring the wrong thing — it would understate curation's miss cost by exactly the amount the question leaked.

## 3. Tool surface — the justification

**Shipped:** `tools: ["Read", "Grep", "Glob", "Bash"]` **and** `disallowedTools: Write, Edit`.

The allowlist is the primary surface — it drops WebFetch, WebSearch, browser MCP, and the Agent tool in config rather than prose. `disallowedTools` is retained as belt-and-braces: repo-local `tools:` handling is unverified until the 2.3 spawn (see §3a), and if the key is ignored there, Write/Edit still need to be blocked.

| Tool | Why it is required |
|---|---|
| `Read` | Artifacts, source files, and images (vision mode reads image paths) |
| `Grep` | Locate handles inside large artifacts without ingesting them whole — the entire point of the agent |
| `Glob` | Resolve artifact globs, and **prove absence cheaply**: an artifact named in the prompt that doesn't exist must land in the coverage note as absent, which requires a resolution step |
| `Bash` | The extraction recipes in `.claude/skills/a11y-test/references/evidence-extraction.md` are `jq` one-liners. Without Bash the reader would have to `Read` whole axe/trace/census JSON into its own window — which still isolates the payload from the caller, but risks its own truncation and abandons the repo's own verified recipes. Also `wc -c` / `ls -l` for the inventory that drives the read/not-read partition. |

**Denied and why:**

- **`Write` / `Edit`** — the digest is the return message. A reader that writes files creates a second summarization surface (plan principle 2 permits exactly one hop) and an ownership problem: a file nobody gated becomes a citable artifact.
- **`WebFetch` / `WebSearch` / browser MCP** — dropped by the allowlist. A reader that can look up the APG pattern for the component under test starts reporting *expectations*: the blind-curation failure arriving through a side door rather than through a metadata file.
- **Agent (subagent spawning)** — dropped by the allowlist. Depth-1 (repo rule; 92% error rate at depth-2+).

**The network hole is narrowed, not closed — and the def now says so.** My pre-revision claim that an allowlist "closes the network hole" was wrong, and the gate caught it: **Bash still reaches the network.** `curl`, `gh`, `npx`, and `agent-browser` all run from inside an allowed tool. Dropping WebFetch/WebSearch/browser MCP removes the *convenient* paths, not the capability. So the prose ban is not redundant with the config — it is the only thing covering the residual path, and `<Constraints>` now states this explicitly and extends the ban to network-reaching Bash commands. A future reviewer should not read the allowlist as making the prose ban decorative.

**"Read-only" was also overstated** (gate MINOR 8): Bash can create and modify files via redirection, `tee`, or `sed -i`. The def's constraint is now phrased as **"you emit no artifacts of your own"** and names those three mechanisms, rather than claiming a read-only surface the tool set does not actually provide.

### 3a. Verification status of the allowlist

`tools:` is honoured for **user-global** agent defs — verified directly, not assumed: `~/.claude/agents/codex-implementer.md:5` ships `tools: ["Bash", "Read", "Grep", "Glob"]`, and three other user-global defs (`codex-tester`, `lit-review-planner`, `study-design-planner`) use the same key. This falsifies my pre-revision claim that the key was "unproven in this harness."

What remains genuinely unverified is **repo-local** (`.claude/agents/` inside this project) handling — no def in this repo used the key before now, so this def is the first data point. That verification happens at the 2.3 spawn: if the reader can call WebFetch there, the allowlist is not being honoured repo-locally and the prose ban is carrying the whole load. **2.3 should check this explicitly rather than assume it.**

## 4. Rejected alternatives

1. **A second `a11y-vision-reader` def.** Rejected because the plan says so (task 2.1: "one contract family, not a second def") and because the reasons hold up: the admissibility question ("is this defect class visual?") must be answered *before* you know which reader to spawn, so a split forces the caller to make the classification the reader exists to make. One def, one gate.
2. **Emitting the full evidence-finding contract with judgment fields filled.** Rejected — see §1. It would make a haiku agent the severity authority.
3. **Emitting the contract with judgment fields present-but-empty** (`severity: [withheld]`). Rejected: ritual empty fields are what the contract itself warns against (line 5), and an empty field invites a downstream consumer to fill it without re-reading the evidence.
4. ~~**`tools:` allowlist frontmatter instead of `disallowedTools:`.**~~ **Reversed at the gate — now shipped (see §3, §3a).** My rejection rested on a false premise: I checked only this repo's defs, concluded the key was "unproven in this harness," and never checked `~/.claude/agents/`, where four defs use it. Checking one directory would have settled it. The lesson generalises past this def: *"no precedent in this repo"* is not *"no precedent in this harness,"* and the two were conflated in a load-bearing safety decision.
5. **A hard cap on images viewed.** Rejected in favour of **budget-and-declare**: view one at a time, stop when the question is answered or at four, and unviewed images become coverage-note rows with a count. A hard cap silently drops evidence; a declared budget makes the drop visible.
   *Gate MINOR 11, applied:* the original collapsed both stop conditions into one `image budget` label, which conflated two different facts. They are now split — `question answered (N unviewed)` vs `image budget (N remaining)`. Only the second tells the caller to re-invoke narrowed; labelling an early success as a budget drop would have manufactured phantom follow-up work.
8. **A `mixed` evidence class as a catch-all.** The original enum carried `mixed` with no definition, which — as the gate noted — routed straight around the vision-admissibility gate: call a question `mixed` and pixels become arguable for any part of it. Kept rather than dropped, but now defined: `mixed` requires naming each sub-question's class, and **the vision gate is per-sub-question, never per-question.** Dropping it was the alternative; defining it is better, because real retest questions genuinely do span classes and forcing them into one label would have produced a worse misclassification.
6. **A novel size threshold for "too big to Read whole."** Rejected in favour of reusing the repo's existing 30KB navigate-by-Grep threshold (CLAUDE.md "Working In This Repo"). Same underlying reasoning, one fewer number to keep in sync.
7. **A hard output cap.** Rejected. The def instead says: if an honest digest exceeds ~4K tokens, **emit it and flag `BUDGET EXCEEDED`**. Truncating evidence to hit a context budget is the exact failure this whole phase exists to prevent — the budget loses to honesty, deliberately.

## 5. Mirror / drift obligations — **none**

Verified by reading `scripts/check_mirrors.py` (strict run below), not inferred:

- `SKILL_NAMES` (line 45) drives the `.claude/skills/` ↔ `.agents/skills/` mirror check. `a11y-evidence-reader` **has no SKILL.md counterpart**, so it is out of scope. It is an agent-only surface, like `a11y-scout`.
- `EMBEDDED_AGENT_DEFS` (line 51) covers only `a11y-planner` and `a11y-critic` — defs that embed a condensed copy of a skill protocol. The reader embeds no skill protocol; it *references* two files (`a11y-test/SKILL.md`'s evidence table, `references/evidence-extraction.md`) by path rather than copying their content, which is the drift-free shape by construction.
- `WRAPPER_AGENT_DEFS` (line 64) covers thin wrappers that load a canonical SKILL.md at runtime. The reader is not a wrapper — it carries its own protocol, which is short enough not to need one.
- The script's comment at lines 47–50 already names the exact precedent: *"Not covered: a11y-scout (no skill counterpart)."*

**No Codex mirror is required.** `.codex/agents/*.toml` exists only for the planner and critic (the two embedded-protocol defs). Nothing in the script demands one, so none was created — per the instruction not to create mirrors unless the script provably demands it.

**The 2.2 wiring edit (`a11y-workflow/SKILL.md`) carries the same "none" answer, independently checked:** it is Claude-Code-only (its own frontmatter declares `compatibility: Claude Code only`) and is not in `check_mirrors.py`'s `SKILL_NAMES` (`a11y-critic`, `a11y-planner`, `a11y-test`, `perspective-audit`, `bug-reporting`, `acr-reporting` only) — so it has no `.agents/skills/` mirror to drift from. No drift obligation; the strict run exits 0.

**Trigger that would change this:** if an `a11y-evidence-reader` SKILL.md is ever created, or if the def is ever changed to embed a condensed copy of another skill's protocol markers, it must be added to the matching dict in `check_mirrors.py` in the same commit.

**Verification:** `python3 scripts/check_mirrors.py --strict` → `No drift detected — mirrors are in sync` (exit 0) with the new def in place.

## 6. Gate decisions (resolved) and what remains open

### Resolved at the gate — binding

**Q1 — tool surface.** Adopt the `tools:` allowlist. Applied; premise correction and residual-risk note in §3/§3a. The prose network ban is **kept and strengthened**, because the allowlist does not close the Bash network path.

**Q2 — haiku stays the default.** And the consequence is made concrete: **2.3 runs at haiku, as the binding test of whether the default holds.** A haiku-produced pack that comes back carrying `AMBIGUOUS` / `re-invoke at sonnet` rows gets **re-curated at sonnet before freezing**. The gate ruled this is *not* a regeneration loop under plan line 112 — that rule forbids regenerating a pack in response to a *post-row miss* (which would launder ground truth into the pack); re-curating in response to the reader's own self-declared ambiguity, before any model row exists, uses no ground truth at all. The distinction is worth keeping visible, because the two operations look identical from outside and only one is legitimate.

**Q3 — keep the literal `<Output_Format>` template**, and pay for it by cutting named furniture instead: Role para 4, three verbatim-restating `<Constraints>` lines, the second clause of the one-hop line, and the hardcoded model-id strings in `<Model_Routing>` (tier names kept). All applied; ~500B recovered.

*My Q3 measurement was wrong and the gate corrected it.* I asserted `<Output_Format>` was "the largest single block (~2.5KB)". Re-measured on the pre-revision draft: `<Output_Format>` 2,097B, `<What_You_Emit>` 2,284B — `What_You_Emit` was the largest, and Output_Format was second. I eyeballed it instead of measuring. Post-revision the order is unchanged (`What_You_Emit` 2,473B, `<Output_Format>` 2,522B — Output_Format is now marginally larger after the glob and provenance rows).

**Q4 — question provenance.** New requirement, §2a. Carries a Phase 3 obligation: pack rules must record the verbatim question and its author, attested as authored without ground-truth access.

### Still open

1. **Repo-local `tools:` handling is unverified.** Proven for user-global defs (§3a); this def is the first repo-local instance. **2.3 must check it explicitly** — if the reader can reach WebFetch there, the prose ban is carrying the entire network boundary alone.
2. **Depth-1 is prose-only for every *other* def in this repo.** Closed in config for the reader via the allowlist; the repo-wide gap remains. Flagged, not fixed — out of scope for 2.1.
3. **14.4KB is 4.9× the scout**, up from 4.3× pre-revision. The gate's MAJOR fixes were worth more than the bytes they cost, but plan R4's "skill bloat irony" now applies harder than when I first raised it, and a frugality tool that keeps growing deserves a re-look at the next gate rather than a shrug here.
4. **`fingerprint` computation.** Unaddressed by the gate. Still worth a ruling: is permitting it scope creep for an extraction agent — or the highest-value thing it can produce, given the bug-reporting lane scores "recomputed stable IDs verified" and has measured hosted models at 2/2 on that check at best?
5. **Untested by construction.** Zero model rows; 2.3 is first contact. The coverage note remains the field most likely to degrade — an honest "not read" is the hardest output for a model that wants to look thorough. Recommendation stands and now has a third case: **2.3 should grade the coverage note against a corpus containing a deliberately missing artifact, a deliberately oversized one, and a glob matching more files than the reader can read.**

### 2.3 receipt outcomes (2026-08-25, same day — closes open items 1 and partially 5)

Receipts: `evals/results/context-utilization-phase2/README.md`.

- **Open item 1 CLOSED (positive control run, 2026-08-25):** a follow-up probe explicitly instructed the registered repo-local def to *attempt* WebFetch, WebSearch, Agent, and Write — not merely report its visible list. All four came back `TOOL-NOT-AVAILABLE`: schema absent, not addressable at all, distinct from "called and rejected." `SendMessage` was likewise absent (its own report had to be recovered from the transcript). `Read`/`Bash` delivered and working. This is the positive control the 2.3 self-report lacked; the allowlist is confirmed config-enforced at the schema level for repo-local defs. Provenance: transcript `c648a303-3902-4c5a-a233-a90ffaded752.jsonl`, project sessions dir, 2026-08-25; disposition recorded in `docs/plans/2026-08-25-context-utilization-phase2-gate-review.md`. **New caveat surfaced by the same probe:** `Grep`/`Glob` — which the `tools:` allowlist *grants* — were also `TOOL-NOT-AVAILABLE`. Attribution: this harness build treats Grep/Glob as deferred tools generally (the main session lacks them natively too), so this is a harness-build property, not allowlist-stripping — but the practical consequence holds: the reader runs with Read+Bash only. Execution 2's inventory now states the Bash `grep`/`ls`/`find` fallback explicitly; the file-granularity coverage obligation is unaffected (observed working in the 2.3 worked example).
- **Open item 5 partially exercised:** haiku produced a contract-shaped digest with an honest coverage note — missing artifact NOT READ (absent), oversized artifact NOT READ (but reasoned "out of scope" rather than citing the 30KB threshold — wrong vocabulary, honest outcome). Glob-partial and "should"-excerpt cases were not exercised by this corpus; both carry to Phase 3 pack construction.
- **One def amendment adopted from the receipt:** ARIA-state observations carry the full `states` dict verbatim — the consuming critic's targeted lookup showed a condensed states block invited a wrong 4.1.3-vs-4.1.2 mapping (the receipt's headline lesson: the consumer's per-finding lookup at the cited handle is load-bearing, not optional).

## 7. Negative space — what this def does not do

- It does not decide **whether** to spawn the reader. That is task 2.2 (wiring), and the CLAUDE.md bullet already added there ("when artifacts exceed the inject budget") is the current trigger.
- It does not define an inject-budget number. 2.2's call.
- It does not touch the evidence-finding contract itself — the contract's judgment fields are unchanged; the reader simply declines to fill them.
- It carries no eval lane. Whether the reader deserves one is a Phase 3-adjacent question the plan does not currently answer.
