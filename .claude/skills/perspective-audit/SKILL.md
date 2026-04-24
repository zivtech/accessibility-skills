---
name: perspective-audit
description: "Deep accessibility review from 7 access perspectives — activated by escalation from a11y-planner or a11y-critic when one or more perspectives are flagged at MEDIUM or HIGH alarm level."
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: zivtech
  version: "2.0.0-router"
disallowedTools:
  - Write
  - Edit
  - NotebookEdit
---

# Perspective Audit — Router

This skill is a router. The full audit protocol lives in the `perspective-audit` agent.

## Route

Invoke with:

```
Agent(subagent_type="perspective-audit", prompt=<escalated prompt with flagged perspectives>)
```

## Use when

- `a11y-planner` or `a11y-critic` has escalated a finding at MEDIUM or HIGH alarm level.

## Do not use when

- No perspective has been flagged — defer to the escalating skill.
