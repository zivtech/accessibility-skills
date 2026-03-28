# Baseline A — Current Skills (No Perspectives)

## Condition

Run the current a11y-planner, a11y-critic, and a11y-test skills **without** perspective enhancements against each fixture. This represents the pre-enhancement baseline.

## Prompt

Use the standard skill invocation with no modifications:

```
Review this component for accessibility issues using /a11y-critic.
```

For planner fixtures:

```
Design the accessibility implementation for this component using /a11y-planner.
```

## Expected Performance

| Metric | Expected Range | Reasoning |
|---|---|---|
| Precision-weighted coverage | Baseline (1.0x) | Strong on keyboard, screen reader, ARIA; weak on auditory, vestibular, cognitive, contrast |
| New-dimension precision | 30-50% | May catch obvious issues (missing captions) but miss subtle ones (motion sensitivity, cognitive load) |
| New-dimension recall | 20-40% | No structured checklist for these dimensions |
| Existing-dimension TPR | 70-85% | This is the skill's strength area |
| False positive rate | 10-20% | Well-calibrated severity from realist check |
| Actionability | 75-85% | Good evidence format but may lack perspective-specific user group detail |
| Escalation accuracy | N/A | No alarm levels in current skills |

## What This Baseline Measures

Condition A establishes the floor. It measures what the current skill set catches without any perspective awareness. The key gap should be in new dimensions (auditory, vestibular, cognitive, contrast) where the current skills have minimal structured coverage.
