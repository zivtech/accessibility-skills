# Baseline B — Strong Generic (Named Dimensions)

## Condition

Run the current a11y-planner and a11y-critic skills **with** a prompt appendage that names the new dimensions. This isolates whether simply naming the dimensions (without structured JTBD checklists) is sufficient.

## Prompt

Append to standard skill invocation:

```
Review this component for accessibility issues using /a11y-critic.

Also review for auditory, vestibular, cognitive, and contrast accessibility.
```

For planner fixtures:

```
Design the accessibility implementation for this component using /a11y-planner.

Also consider auditory, vestibular, cognitive, and contrast accessibility.
```

## Expected Performance

| Metric | Expected Range | Reasoning |
|---|---|---|
| Precision-weighted coverage | 1.1-1.2x A | Naming dimensions prompts some additional coverage |
| New-dimension precision | 50-65% | Finds more issues but without JTBD structure, findings may be vague |
| New-dimension recall | 40-55% | Better than A but misses checklist-level specifics |
| Existing-dimension TPR | 70-85% | Same as A — no regression expected |
| False positive rate | 15-25% | May over-flag in new dimensions without calibration |
| Actionability | 70-80% | Findings in new dimensions may lack specific element refs and fix suggestions |
| Escalation accuracy | N/A | No alarm levels |

## What This Baseline Measures

Condition B is the strong control. If C outperforms B, it demonstrates that the structured JTBD/escalation approach adds value beyond simply telling the model to "also check for X." This is the critical comparison — B vs C isolates the methodology's contribution.

## Why This Is a Fair Baseline

- Uses the same underlying model (claude-opus-4-6)
- Uses the same skill protocol (10-phase investigation for critic, 9-phase for planner)
- Only difference is an explicit instruction to consider the named dimensions
- This is what a practitioner would do without the perspective-audit skill: append a reminder
