---
name: a11y-role-audit
description: "ARRM-based accessibility role audit — runs responsibility-based review lenses (visual design, UX design, front-end dev, content authoring, business analysis, testing) to produce role-attributed findings. Complements the access-method perspectives in perspective-audit."
license: Apache-2.0
compatibility: Claude Code-compatible; protocol is model-agnostic
metadata:
  author: zivtech
  version: "1.0.0"
  arrm_source: "W3C WAI ARRM (https://www.w3.org/WAI/planning/arrm/)"
  attribution: "Role definitions adapted from Mike Gifford's ARRM roles (MIT)"
---

# Accessibility Role Audit

Review a component, page, or design from the responsibility perspective of specific team roles. Each role brings a distinct vantage point with explicit blind spots — what it CAN see and what it CANNOT. Running multiple roles catches barriers that no single role would find alone.

## Relationship to Other Skills

| Skill | Dimension | Question |
|-------|-----------|----------|
| `a11y-critic` | Design decisions | "Is the accessibility approach sound?" |
| `perspective-audit` | Access methods | "Who is blocked?" (users with disabilities) |
| `a11y-role-audit` (this) | Team responsibilities | "Who on the team owns preventing/fixing this?" |

These three are complementary layers:
1. Critic identifies design gaps
2. Perspective audit identifies impact on specific user groups
3. Role audit identifies which team member is responsible and what each sees from their vantage point

## When to Use

### Mode 1: Design Review (before code)

Run visual-design + ux-design lenses over mockups, wireframes, or design specs. Catches accessibility barriers before implementation hardens them.

```
/a11y-role-audit design <target> [--roles visual-design,ux-design]
```

### Mode 2: Implementation Review (after code)

Run all roles (or a subset) over implemented code. Each lens reviews from its domain-specific vantage point.

```
/a11y-role-audit code <target> [--roles all]
/a11y-role-audit code <target> [--roles front-end-development,content-authoring]
```

### Mode 3: Finding Attribution (post-critic)

After a11y-critic or perspective-audit produces findings, attribute each to the responsible ARRM role using the decision tree.

```
/a11y-role-audit attribute <findings>
```

## The 6 Roles

| # | Role | Focus | Primary ARRM Tasks |
|---|------|-------|-------------------|
| 1 | Visual Design | Contrast, zoom, focus indicators, targets, motion, forced-colors | 30 |
| 2 | UX Design | Patterns, focus order, error flows, state, consistency, timing | 96 |
| 3 | Front-End Development | Semantic HTML, ARIA, keyboard, live regions, CSS a11y | 90+ |
| 4 | Content Authoring | Alt text, headings, links, captions, language, labels | 42 |
| 5 | Business Analysis | CAPTCHA, time limits, error prevention, requirements | 1 |
| 6 | Testing | AT validation, regression, coverage gaps | 0 (verification) |

## Steps

### Step 1 — Determine mode and roles

Parse the invocation to identify:
- **Mode**: `design`, `code`, or `attribute`
- **Target**: file path(s), URL, or findings to attribute
- **Roles**: specific roles requested, or `all` (default: all)

If mode is `attribute`, skip to Step 5.

### Step 2 — Read reference materials

Read the role definitions for each requested role:
- `roles/<role-name>.md` — perspective, blind spots, checklist, WCAG criteria

Read the ARRM mapping:
- `roles/arrm-task-mapping.yaml` — SC-to-role routing for attribution

### Step 3 — Read the artifact under review

Read all source files relevant to the requested roles. For `design` mode, this may be mockup descriptions, Figma exports, or wireframe specs. For `code` mode, read HTML/CSS/JS/template files.

### Step 4 — Run per-role review

For each requested role, evaluate the artifact through that role's lens:

1. Work through the role's **review checklist** (from the role definition file) item by item.
2. For each checklist item:
   - **PASS** — implementation satisfies the criterion. Note evidence briefly.
   - **FINDING** — gap identified. Generate a finding (Step 6 format).
   - **N/A** — criterion doesn't apply to this artifact.
3. After the checklist, consider the role's **blind spots** — flag any areas where a different role's review would be needed.

### Step 5 — Attribution mode (for existing findings)

For each finding in the input:
1. Identify the WCAG SC referenced
2. Look up the SC in `roles/arrm-task-mapping.yaml`
3. Apply the decision tree (first matching rule wins)
4. Tag the finding with primary and secondary responsible roles

### Step 6 — Output format

```markdown
## Role Audit Results

### [Role Name]

**Items reviewed**: [count from checklist]
**Findings**: [count]
**Blind spots flagged**: [list of areas needing other roles]

#### Findings

1. **[Severity]**: [Description]
   - **Evidence**: [file:line or observed characteristic]
   - **WCAG**: [SC number — criterion name]
   - **Role ownership**: Primary: [this role] | Secondary: [other role]
   - **Fix**: [Recommended action within this role's domain]

#### Blind Spot Escalations

- [ ] [Area] → needs review from [other role]
```

## Severity Calibration

| Severity | When to apply |
|----------|---------------|
| CRITICAL | Blocks access entirely for a user group — no workaround exists |
| MAJOR | Significant barrier — degraded experience with difficult workaround |
| MINOR | Usability degradation — workaround exists and is reasonable |
| ENHANCEMENT | AAA criterion or best practice beyond AA compliance |

## Cross-Role Synthesis

After all requested roles complete, produce a synthesis section:

```markdown
## Cross-Role Synthesis

### Coverage Map
| WCAG SC | Visual | UX | Front-End | Content | Business | Testing |
|---------|--------|-----|-----------|---------|----------|---------|
| [SC]    | PASS   | —   | FINDING   | N/A     | —        | —       |

### Gaps Requiring Multi-Role Collaboration
- [Description of gap that spans roles, with roles needed]

### Unreviewed Areas
- [Areas that no requested role covers — suggest which role to add]
```

## Evidence Requirements

- CRITICAL/MAJOR findings: file:line reference required (code mode) or specific design element reference (design mode)
- All findings: WCAG SC citation required
- Assertions without evidence are not findings — they are hunches. Mark them `[UNVERIFIED]` and note what evidence would confirm them.

## Integration with Workflow

In the full a11y-workflow lifecycle:

```
scout → plan → [ROLE AUDIT: design mode] → critique plan → implement → test → [ROLE AUDIT: code mode] → critique implementation → [perspective audit]
```

The role audit runs at two points:
1. **After planning** (design mode) — catches role-specific gaps before implementation
2. **After testing** (code mode) — produces role-attributed findings for targeted fixes
