---
name: a11y-planner
description: "Use when you know what component, flow, or interface you need but not yet the right accessibility approach. Best for turning WCAG 2.2 requirements into an accessible implementation plan with WAI-ARIA APG patterns before code hardens bad interaction and state patterns."
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: zivtech
  version: "2.0.0-router"
---

# Accessibility Design Planner — Router

This skill is a router. The full planning protocol lives in the `a11y-planner` agent.

## Route

Invoke with:

```
Agent(subagent_type="a11y-planner", prompt=<user's planning prompt>)
```

## Use when

- The user needs to plan accessibility BEFORE coding — mapping WCAG 2.2 requirements to WAI-ARIA patterns, designing focus order, state communication, keyboard interaction.

## Do not use when

- The user wants to review an existing implementation — route to `a11y-critic` instead.
- The user wants to run real accessibility tests — route to `a11y-test` instead.
