---
name: a11y-critic
description: "Use when you have an existing component, flow, or interface and need an evidence-backed accessibility design review after basic checks pass. Best for WCAG 2.2 compliance, focus management, ARIA pattern quality, semantics, and state communication gaps automated tools miss."
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: zivtech
  version: "2.0.0-router"
---

# Accessibility Critic — Router

This skill is a router. The full review protocol lives in the `a11y-critic` agent.

## Route

Invoke with:

```
Agent(subagent_type="a11y-critic", prompt=<user's review prompt>)
```

## Use when

- The user has an implementation and wants an evidence-backed accessibility review after basic automated checks pass.
- The user needs WCAG 2.2 compliance review, ARIA pattern quality review, focus and state gap analysis.

## Do not use when

- The user wants to plan accessibility before coding — route to `a11y-planner` instead.
- The user wants perspective-based deep audit — route to `perspective-audit` instead.
