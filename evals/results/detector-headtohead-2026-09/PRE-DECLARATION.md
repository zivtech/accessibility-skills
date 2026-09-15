# Pre-declaration of the PT-06(a) + PT-07(b) decision rule (receipt)

Stated **before the run** (session 2026-09-15, started ~00:40 UTC; the receipt
is this file's own commit SHA once committed — recorded here after commit, then
copied into every run artifact's header). Executed under the protocol
`docs/plans/2026-09-14-detector-headtohead-protocol.md` (issue #86).

**Confirmer scoping (decided before the run, user's ruling 2026-09-15):** the
run is executed by an agent, and §5.4 requires each candidate defect to be
confirmed by a **named human, never an agent**. Therefore this run's engine
measurement and §5 packet staging (live inspection, locator, snippet, computed
value, frozen-state capture) are done in-session, but every candidate stays
**agent-assessed, not human-confirmed**, until a named human ratifies the
packet. By construction this run reports **INCONCLUSIVE-pending-confirmation**
against both bars until that ratification happens; it cannot self-certify the
"≥1 human-confirmed true positive" clause. This is disclosed here, before the
run, so the outcome is not reinterpreted after the fact.

## Pre-declared threshold (do not soften it)

**PT-06(a), verbatim** (`docs/alfa-scan-adoption-assessment.md`, reopen trigger (a);
`docs/plans/2026-09-02-promotion-candidate-dispositions.md`):

> ≥5 *independent* defect-bearing surfaces (not pages from one demo template)
> yield ≥3 Alfa-only A/AA rule classes over axe+htmlcs, ≥1 human-confirmed true
> positive.

The reopened base bar it sits on
(`evals/results/promotion-eval-2026-09/1.1-alfa-overlap/PRE-DECLARATION.md`):
Alfa-only = distinct Alfa rules mapping to A/AA criteria, **FAILED outcomes
only, not cantTell**, that neither axe nor htmlcs flagged on the same surface,
≥1 a plausible true positive on inspection. This re-run carries the strictly
higher bar per protocol §1: **human-confirmed**, not agent-assessed.

**PT-07(b), verbatim** (`docs/wave-adoption-assessment.md`, reopen trigger (b);
same dispositions doc):

> A WAVE licence-holder runs a five-page head-to-head against axe (the Lighthouse
> comparison in `docs/tools.md` is the template) and finds A/AA defect classes
> axe misses.

**PT-07(b) operative thresholds for this run**, per protocol §1's PT-07 note
(these are the harder, non-gameable operationalization, committed here as the
single source of truth for this run — not softer than, and never invented
beyond, the trigger text):
- Surfaces, not pages: **5 independent surfaces** per §2, not five pages of one
  template.
- Class-count threshold: PT-07(b) names **no number**; pinning it is a
  promotion-policy decision the protocol does not make, so this run **inherits
  PT-06's ≥3 A/AA-classes as the conservative floor** — WAVE-only A/AA rule
  classes over axe (htmlcs excluded from the axe baseline for the WAVE leg,
  since PT-07(b) says "against axe"; also reported over axe+htmlcs for context),
  FAILED/candidate outcomes only.
- Confirmation: **≥1 human-confirmed true positive** among the WAVE-only
  classes, same §5 packet as PT-06(a).

**Independence (§2), committed:** a surface counts iff it has (1) a distinct
origin (different site/app/hosting boundary, not just a different path on the
same deployment) AND (2) a distinct template/CMS/authoring source. **≥1
human-confirmed A/AA defect (§5), found by any engine, makes a surface
"defect-bearing"** — an engine-flagged-but-unconfirmed candidate does not.

## Surface count committed (exact N per §6)

**N = 5.** Not "≥5." Fixed so the shortfall clause below is meaningful.

## Surfaces committed, with independence justification per §2

Frozen **before any accessibility scan**. Each is a distinct origin AND a
distinct template/CMS/authoring source; both conditions shown.

| # | Surface (URL) | (1) Distinct origin | (2) Distinct template/CMS/authoring source |
|---|---|---|---|
| 1 | `https://www.epa.gov/climate-change` | www.epa.gov — nginx behind CloudFront | Drupal 10 (`x-generator: Drupal 10`), EPA WebCMS theme |
| 2 | `https://cfpub.epa.gov/roe/` | cfpub.epa.gov — Apache, separate hosting boundary | Adobe ColdFusion (`.cfm`) legacy application, not Drupal |
| 3 | `https://enviro.epa.gov/` | enviro.epa.gov — nginx/1.28.2, separate boundary | Envirofacts application (query/data app), distinct authoring source, not the WebCMS |
| 4 | `https://ordspub.epa.gov/ords/guideme_ext/f?p=guideme:home` | ordspub.epa.gov — Apache (reached via `ofmpub.epa.gov/apex` → `ordspub.epa.gov/ords`) | Oracle APEX / ORDS application, distinct generator and authoring source |
| 5 | `https://comptox.epa.gov/dashboard/` | comptox.epa.gov — Apache, separate boundary | CompTox Chemicals Dashboard, client-rendered React SPA, distinct build/authoring source |

**SPA caveat, disclosed before the run (not a post-hoc excuse):** surface 5 is
client-rendered. The axe leg runs through Playwright (rendered DOM) and sees the
real content; the WAVE API leg fetches server HTML and may see only an app
shell. A WAVE-blind result on surface 5 is therefore a genuine head-to-head
finding about the WAVE **API** on SPAs, and surface 5 remains defect-bearing if
any engine confirms ≥1 A/AA defect on it (the axe/Playwright leg can).

**Rejected during freezing (recorded so the set is auditable):**
`www3.epa.gov/climatechange/` — now **301-redirects into `www.epa.gov`** (Drupal
10), so it is no longer a distinct origin+template and would double-count
surface 1. `echo.epa.gov` — also `x-generator: Drupal 10`, i.e. the **same CMS
generator** as surface 1; excluded to avoid a §2 condition-(2) failure (two
Drupal-10 EPA properties are not two independent authoring sources under the
strict reading).

## Prior attempts at this bar (attempt-family accounting, §6)

- **PT-06(a):** one prior attempt against the *base* Alfa-overlap bar —
  `evals/results/promotion-eval-2026-09/1.1-alfa-overlap/` (2026-09-02). Outcome:
  **below threshold** — 2 Alfa-only A/AA classes (`sia-r14`→2.5.3,
  `sia-r69`→1.4.3), both **agent-assessed, not human-confirmed**, on a sample its
  own README corrected to ~3 independent defect-bearing surfaces ("one template
  sampled four times"). That run did **not** target trigger (a)'s ≥5-independent
  -surfaces + human-confirmed bar; this is the **first** attempt at PT-06(a) as
  reopened.
- **PT-07(b):** **none.** No WAVE-vs-axe head-to-head has ever been run in this
  repo (`docs/wave-adoption-assessment.md`: "This head-to-head has never been
  run"). This is the first attempt.

## Pilot-scan disclosure (§6)

Before this pre-declaration was committed, the only automated interaction with
any of the 5 committed surfaces was: (a) HTTP header inspection
(`curl -sI`) to read tech stack, and (b) HTTP liveness checks (`curl -o
/dev/null -w %{http_code}`) to confirm 200/redirect targets. **No accessibility
engine (axe, htmlcs, Alfa, WAVE) was run on any committed surface before this
file was committed.** The single WAVE API call made during setup was a
1-credit `reporttype=1` key-validation call against `https://example.com` — not
a committed surface — to confirm the key works (it did; 99 credits remained).
The surface set was chosen on origin/template distinctness and liveness, **not**
on which pages looked defect-promising.

## Shortfall handling (§6, pre-declared)

If, after the §5 packet is staged and (later) ratified on every candidate,
fewer than **5** surfaces qualify as defect-bearing (≥1 human-confirmed A/AA
defect each), the run reports **INCONCLUSIVE** against that bar. Surfaces are
**not** re-rolled, swapped, or topped up to reach 5 after the fact. Any later
attempt at either bar must cite this file and explain what changed.

## Reporting split (§3, WAVE terms — pre-committed)

All raw WAVE output, per-page/per-item counts, category totals, item IDs, and
any cross-engine table carrying a WAVE column stay **private** (this run writes
them only to an out-of-repo scratchpad, never a tracked path). The only
publishable facts are independently verified defects (SC + plain description),
the SC-level human-confirmed engine attribution + class tally (§3 boundary), and
the decision. Nothing is published at all this session (user ruling: no
publication until WebAIM permission is obtained via wave.webaim.org/feedback).

Report either outcome plainly.
