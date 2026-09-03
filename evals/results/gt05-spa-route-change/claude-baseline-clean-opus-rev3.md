I'll read the specified file.

---

## Verdict: **REVISE**

The focus and title machinery is genuinely well-built — the single-source title, the previous-pathname guard, and the first-render exemption all do what their comments claim, and I verified each. The defect is in the layer the fixture never reconciles: **the route table and the nav's active-state computation disagree about what URL "Accounts" lives at.**

---

### Findings

**F1 — No current-page indicator at `/` or at any trailing-slash URL — MAJOR**
`spa-route-change-clean.blind.md:132-133`, `:68-74`, `:187-191`

The index route renders `AccountsView` at `/` (`:132`), but `NavLink to="/accounts" end` (`:69-70`) decides `isActive` by literal string comparison of `location.pathname` against the resolved `to`, with `end` disabling the prefix branch. At `/`, `"/" !== "/accounts"` → **`isActive` is false**. The accounts view is on screen and no nav item carries `aria-current="page"`, and none carries the `.is-active` color / weight / underline (`:187-191`).

This is the site's most common cold entry — the exact URL the design at `:266` optimizes for by refusing a root redirect. The cost of that (correct) choice is never paid for in the nav.

The same comparison fails on trailing slashes: React Router matches the *route* while ignoring a trailing slash, so `/accounts/` renders the accounts view — but `"/accounts/" !== "/accounts"`, so again no `aria-current`, no active styling. Ditto `/transfers/`, `/statements/`.

The file's own contract at `:258` asserts `NavLink` marks the active section `aria-current="page"`. On `/` and on every trailing-slash URL, it does not.

*WCAG:* **2.4.8 Location (AAA)** is the honest primary citation. Confidence note: this is **not** an A/AA failure, because the indicator is absent in *both* modalities simultaneously — there is no visible state for `aria-current` to be out of sync with, so 1.3.1 and 4.1.2 do not bite. I am rating it MAJOR on impact rather than rule weight (per this repo's own severity doctrine): at the default URL, every user loses orientation, and a screen-reader user tabbing the nav gets three peers with no "you are here." A visual-only fix would convert this into a genuine **1.3.1 (A)** failure, so fix both together.

**F2 — `index.html` has no `<meta name="viewport">` — MAJOR (conditional)**
`spa-route-change-clean.blind.md:148-151`

The head carries `charset` and `title` and nothing else. Without a viewport meta, mobile browsers apply a 980px layout viewport and scale down: the responsive CSS (`flex-wrap` at `:164`, `:173`; `max-width: 760px` at `:215`) never engages, and 16px text renders at roughly 6–7 effective px.

*WCAG:* **1.4.10 Reflow (AA)**, **1.4.4 Resize Text (AA)**.

Confidence caveat, stated plainly: the snippet is captioned "the initial title" (`:145`), so this may be an abridged excerpt rather than the shipped document. If the head is complete as written, it is a hard AA failure. If it was trimmed for the fixture, disregard.

**F3 — Redundant focus move and false "arrival" announcement — MINOR (derivative of F1)**
`spa-route-change-clean.blind.md:46-54`

Because nothing is marked current at `/`, a user is invited to click "Accounts" while already viewing it. That navigates `/` → `/accounts`, the pathname guard at `:47` sees a change, and focus jumps to an `<h1>` announcing "Accounts, heading level 1" — signalling that a new view arrived when the rendered content is byte-identical. Same on `/accounts/` → `/accounts`.

*WCAG:* none. This is a usability consequence, not an SC failure — I am not going to manufacture a criterion for it. It resolves on its own once F1 is fixed.

---

### Checked and deliberately not flagged

Recording these so the negative space is explicit:

- **Letter-case URLs are fine.** `NavLink` lowercases both sides when `caseSensitive` is false (the default), so `/Accounts` *is* marked current. Route matching is also case-insensitive. The trailing-slash and case cases behave differently — only the former is broken.
- **The StrictMode claim at `:36-39` is accurate.** StrictMode double-invokes effects on mount only, and `pathname` is unchanged then, so the `previousPath` guard is genuinely idempotent under the repeat. A boolean would indeed have failed.
- **The first-render exemption (`:40,47-48`) is correct**, not an oversight — moving focus on cold load would skip past the skip link and nav.
- **`:focus-visible` on a programmatically focused `<h1>` (`:196`) works.** The heuristic matches when the previously focused element matched, so keyboard activation shows the ring and mouse activation correctly does not.
- **`role="list"` on `list-style: none` ULs** (`:65`, `:91`, `:115`) is the deliberate Safari/VoiceOver workaround, not redundancy.
- **Active state is not color-alone** (color + `font-weight: 600` + border-bottom, `:187-191`) — 1.4.1 satisfied.
- **Contrast passes.** `#0b4fa8` on white ≈ 7.8:1; white on `#0b4fa8` for `.primary` is the same pair.
- **Target size 2.5.8 passes.** Nav links ≈31px tall. Statement links are ≈19px tall, but `padding: 10px 0` plus the 1px rule puts link centers ≈40px apart vertically, satisfying the spacing exception.
- **No motion obligation.** `window.scrollTo({ top: 0 })` (`:50`) omits `behavior`, so it is instant — no `prefers-reduced-motion` requirement.
- **Single-source title/heading (`:21-31`) genuinely prevents the desync described at `:17-20`**, and the catch-all (`:136`) carries a real heading and title — no dead ends, as claimed.
- **No focus loss during navigation.** The nav lives in the persistent shell, so focus is never in an unmounting subtree; `cancelAnimationFrame` (`:53`) correctly discards a superseded frame.

---

### Suggested fix for F1

Make the nav's notion of "current" match the router's. Either give the accounts section a real URL and redirect `/` to it (rejected at `:266` for a defensible reason), or — better, preserving that choice — compute active state from the router's own matcher rather than string equality: drop `end` and use `useMatch('/accounts/*')`-style resolution, or add an explicit `isActive` override that treats `/` as the accounts section and normalizes trailing slashes before comparison.

## Provenance

Files read (complete list — one file, read once, in full):

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md`

No other file was read, no search or grep was run, no git command was run, and no skill was invoked. All React Router `NavLink`/matching behavior cited above is from my own knowledge of the library, not from anything read in this session — flagging that as the one place my confidence rests on recall rather than on the provided text.