# Critic standalone v2

`critic-standalone-v2-202610` repairs the input condition exposed by the October
local screen. [system.md](system.md) is the actual standalone system prompt;
[protocol.md](protocol.md) defines scoped detection, delivery and calibration.
The canonical critic skill and its mirrors are corrected separately, while the
benchmark no longer sends a tool-enabled orchestration wrapper to a tool-free model.

Create a fresh output directory:

```sh
python3 -m ollama.local_eval_202610 freeze --condition critic-standalone-v2-202610 --out evals/results/YOUR-NEW-RUN
```

`verify-files` checks retained frozen bytes without granting resume authority.
`run` and `summary` additionally require the selected live source to match its
freeze. Legacy October freezes are preserved; creating another capture under
their sealed condition ID is refused. Changes are new measurements, not a claim
that a previous model result improved. This repair does not launch inference.

Only the four screened CLEAN controls are source-reviewed/repaired here. Browser
checks extract their actual JSX/CSS; scope and reproducible evidence are recorded
under `evals/results/benchmark-repair-2026-10-09/`. These checks do not establish
NVDA/JAWS/VoiceOver speech, an entire page, or every arbitrary child/option value.

Primary grounding for the corrected rules:

- [ARIA current values](https://www.w3.org/TR/wai-aria-1.2/#aria-current)
- [Composite focus strategies](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)
- [Listbox naming and interaction](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/)
- [Optional accordion panel regions](https://www.w3.org/WAI/ARIA/apg/patterns/accordion/)
- [Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [G183 alternative](https://www.w3.org/WAI/WCAG22/Techniques/general/G183)
- [Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html), [Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [Focus Appearance AAA](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)

Before model selection, complete the corrected same-condition control and
candidates. A prompt-quality repair is not evidence of new model performance.
