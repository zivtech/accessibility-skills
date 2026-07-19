# Input: keyboard-a11y-tester finding

Convert this keyboard-a11y-tester finding into an accessibility bug report
ready to file as a GitHub Issue, following the bug-reporting skill.

```json
{
  "test_case_id": "233-0-4-1",
  "viewport": "desktop",
  "generated_at": "2026-07-12T14:52:31.882Z",
  "findings": [
    {
      "id": "focus-appearance-weak-desktop",
      "wcag": "2.4.13",
      "source": "deterministic",
      "persona": "keyboard",
      "evidence_kind": "step_id",
      "conformance_level": "AAA",
      "confidence": 0.5,
      "severity": "minor",
      "viewport": "desktop",
      "goal_id": "adhoc",
      "url": "https://staging.example.dev/pricing",
      "locations": [],
      "summary": "4 focus stop(s) have a visible indicator that does not meet the AAA Focus Appearance bar (>= 2px-perimeter area and >= 3:1 contrast). Informative only. e.g. #plans > div.tier:nth-of-type(1) > button.select-plan (contrast 2.41), #plans > div.tier:nth-of-type(2) > button.select-plan (contrast 1.98), #billing-toggle > button.annual (contrast 2.05), #plans > div.tier:nth-of-type(1) > button.select-plan (contrast 2.41)",
      "persona_impact": "The focus indicator is present but may be hard to perceive for low-vision users tracking keyboard focus across the pricing tiers.",
      "evidence": ["step_0002", "step_0003", "step_0007", "step_0011"]
    }
  ]
}
```
