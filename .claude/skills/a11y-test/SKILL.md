---
name: a11y-test
description: "Use when you need to run real accessibility tests — Playwright keyboard interactions, axe-core scanning, visual regression, and WCAG 2.2 compliance checks. The measurement layer that feeds evidence into a11y-critic reviews."
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: zivtech
  version: "2.0.0-router"
---

# Accessibility Testing — Router

This skill is a router. The full testing protocol lives in the `a11y-test` agent.

## Route

Invoke with:

```
Agent(subagent_type="a11y-test", prompt=<user's testing prompt>)
```

## Use when

- The user wants to run Playwright + axe-core keyboard and scan tests against an implementation.
- `a11y-critic` has requested evidence for a review.

## Do not use when

- The user wants a design review without tests — route to `a11y-critic`.
- The user wants to plan before coding — route to `a11y-planner`.
