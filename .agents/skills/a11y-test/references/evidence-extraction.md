# Evidence Extraction Recipes

**Principle: handles, not payloads.** Cite artifact paths in findings and reports; extract only the fields under adjudication; keep raw JSON, logs, and screenshots on disk. Never paste a full `trace.json`, axe scan result, or census file into context to answer a narrow question a `jq` filter can answer in one line.

## 1. Axe-core scan results (`baseline-url-scan.mjs`)

Verified against real committed artifacts: both recipes below reproduce cleanly against `evals/results/lighthouse-compare-2026-08/ours/` (per-URL files + `summary.json`, produced by this script 2026-08-14), and the field names match the writer code in `references/baseline-url-scan.mjs`.

Per-URL result → `[viewport, rule, impact, node_count, selector-sample]`:

```bash
jq -r '.viewports | to_entries[] | .key as $vp | .value.violations[]?
  | [$vp, .id, .impact, .node_count, (.sample_selectors[0] // "-")] | @tsv' 003-example-com-page.json
```
```
1280x800  color-contrast  serious  3  a.nav-link
1280x800  image-alt       critical 1  img.hero
320x800   target-size     minor    2  button.icon-btn
```

`summary.json` → violations by rule, most nodes first:

```bash
jq -r '.violations_by_rule[] | [.rule_id, .impact, .nodes, .page_count] | @tsv' summary.json
```
```
color-contrast  serious   14  6
image-alt       critical  3   2
```

## 2. `trace.json` → failing steps only

Verified against real committed artifacts: all 6 trace files in `evals/results/keyboard-a11y-tester/driven/`. Loop per-file rather than handing the glob straight to `jq` — every trace restarts step numbering at `step_0001`, so a bare `*.trace.json` filter collides `step_id`s across files with no way to tell which trace a hit came from. The loop adds a `src` column instead.

Steps where a keypress didn't move focus (focus-trap / dead-control candidates):

```bash
for f in *.trace.json; do
  jq -c --arg f "$f" '.steps[] | select(.focus_moved == false)
    | {src: $f, step_id, keystroke: .keystroke_sent, selector: .active_element_selector}' "$f"
done
```
```json
{"src":"async-form-vague-success.trace.json","step_id":"step_0002","keystroke":"type:\"Ada Lovelace\"","selector":"#feedback-name"}
{"src":"async-form-vague-success.trace.json","step_id":"step_0004","keystroke":"type:\"ada@example.com\"","selector":"#feedback-email"}
{"src":"async-form-vague-success.trace.json","step_id":"step_0006","keystroke":"type:\"The export feature saves me hours.\"","selector":"#feedback-message"}
{"src":"form-validation-missing-aria-describedby.trace.json","step_id":"step_0004","keystroke":"Enter","selector":"#root > form > button"}
{"src":"interactive-dropdown-focus-bug.trace.json","step_id":"step_0002","keystroke":"Enter","selector":"#dropdown-btn"}
{"src":"interactive-dropdown-focus-bug.trace.json","step_id":"step_0004","keystroke":"ArrowDown","selector":"#dropdown-list"}
{"src":"popover-no-focus-management.trace.json","step_id":"step_0002","keystroke":"Enter","selector":"#root > div > button"}
{"src":"popover-no-focus-management.trace.json","step_id":"step_0004","keystroke":"Escape","selector":"#root > div > div > button"}
{"src":"tabs-missing-arrow-nav.trace.json","step_id":"step_0002","keystroke":"ArrowRight","selector":"#tab-overview"}
{"src":"tabs-missing-arrow-nav.trace.json","step_id":"step_0003","keystroke":"ArrowLeft","selector":"#tab-overview"}
```

Steps where the focused control's AX state changed but no live-region announcement fired — candidates for 4.1.3 review per the SKILL.md "observe → decide → act" rule, never a proven failure on their own:

```bash
for f in *.trace.json; do
  jq -c --arg f "$f" '
    .steps as $s
    | range(1; $s|length) as $i
    | select($s[$i].focus_moved == false
        and $s[$i].ax_name_role_state.states != $s[$i-1].ax_name_role_state.states
        and ($s[$i].sr_announcement.live_announcements | length) == 0)
    | {src: $f, step_id: $s[$i].step_id, keystroke: $s[$i].keystroke_sent, selector: $s[$i].active_element_selector}
  ' "$f"
done
```
```json
{"src":"interactive-dropdown-focus-bug.trace.json","step_id":"step_0002","keystroke":"Enter","selector":"#dropdown-btn"}
```
(That hit is real: the dropdown's `aria-expanded` flips `false → true` with focus unmoved and `live_announcements` empty. Run across all 6 files, this recipe surfaces that one hit and no others.)

## 3. Screen-reader census — counts + first divergence

`screen-reader-census.json` is emitted by keyboard-a11y-tester (driven sessions and batch crawls).

**Note:** no census artifact is committed in this repo as of this writing. The recipe below is derived from the documented shape only (SKILL.md: "whole-page reading order (spoken phrase, role, selector) + declared live regions") — field names (`entries`, `live_regions`, and per-entry `phrase`/`role`/`selector` used in the divergence recipe below) are inferred, not verified against a real file. Check them against the first real artifact before trusting this as-is.

```bash
# Entry + live-region counts for one census
jq '{entries: (.entries | length), live_regions: (.live_regions | length)}' screen-reader-census.json
```
```json
{"entries": 84, "live_regions": 2}
```

```bash
# First index where two censuses (before/after a fix) diverge in phrase, role, or selector
jq -n --slurpfile a before.census.json --slurpfile b after.census.json '
  ($a[0].entries) as $before | ($b[0].entries) as $after
  | ([range(0; [$before|length, $after|length] | min) | select($before[.] != $after[.])] | first) as $i
  | if $i == null then "no divergence in the overlapping range"
    else {index: $i, before: $before[$i], after: $after[$i]} end
'
```
```json
{"index": 17, "before": {"phrase": "Submit", "role": "button", "selector": "#submit-btn"}, "after": {"phrase": "Submit form", "role": "button", "selector": "#submit-btn"}}
```
(Length difference beyond the overlapping range — entries added or removed at the tail — shows up in the count recipe above, not this one.)

## 4. PreToolUse filter hook (documented pattern — user-level only)

**This is a recipe for users to adopt in their own `~/.claude/settings.json` or project `.claude/settings.json` — it is NEVER shipped as config in this repo.** The bundle stays prompt-only (see this repo's `CLAUDE.md`); hooks are a Claude Code harness feature configured per-user or per-consuming-project, not a skill artifact.

`settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/block-wholesale-evidence-reads.sh" }
      ]}
    ]
  }
}
```

`block-wholesale-evidence-reads.sh` — reads the tool-call JSON on stdin; blocking with exit code 2 returns the stderr message to the model as feedback, so it retries with a narrower command instead of dumping the file:

```bash
#!/usr/bin/env bash
input="$(cat)"
cmd="$(jq -r '.tool_input.command // empty' <<<"$input")"
if [[ "$cmd" =~ cat[[:space:]].*\.(trace|findings|census)\.json ]]; then
  echo "Don't cat evidence JSON wholesale — extract the field you need with jq (see evidence-extraction.md)." >&2
  exit 2
fi
exit 0
```

Adapt the match pattern and message to your own evidence file naming; re-verify the hook I/O contract against your installed Claude Code version before relying on it.
