# Accessibility Roles (ARRM-Based Review Lenses)

Role-based accessibility review lenses derived from the [W3C WAI ARRM](https://www.w3.org/WAI/planning/arrm/) (Accessibility Roles and Responsibilities Mapping). Each role is a proactive review perspective that catches issues from its responsibility domain.

## Relationship to Perspective Audit

This bundle has two complementary audit dimensions:

| Dimension | Skill | Question answered |
|-----------|-------|-------------------|
| **Access perspectives** | `perspective-audit` | "Who is blocked?" (screen reader user, keyboard user, low-vision user...) |
| **Responsibility roles** | `a11y-role-audit` | "Who on the team owns fixing this?" (designer, developer, content author...) |

They are orthogonal. A single finding like "accordion state isn't communicated" touches both:
- **Perspective**: Screen reader user can't tell if section is expanded
- **Role**: UX Design owns the pattern choice; Front-End Dev owns the ARIA implementation

Neither replaces the other. Run both for complete coverage.

## Available Roles

| Role | Primary ARRM Tasks | Focus Domain |
|------|-------------------|--------------|
| [Visual Design](./visual-design.md) | 30 | Contrast, zoom, focus indicators, target size, motion, forced-colors |
| [UX Design](./ux-design.md) | 96 | Interaction patterns, focus order, error flows, state, consistency |
| [Front-End Development](./front-end-development.md) | 90+ | Semantic HTML, ARIA, keyboard handlers, live regions, CSS a11y |
| [Content Authoring](./content-authoring.md) | 42 | Alt text, headings, link text, captions, plain language, labels |
| [Business Analysis](./business-analysis.md) | 1 | CAPTCHA, time limits, error prevention, requirements tracking |
| [Testing](./testing.md) | 0 (verification) | AT validation, regression, coverage gaps |

## When to Use

### Design-Phase Gate (before code)

Run visual-design + ux-design lenses over mockups, wireframes, or design specs to catch barriers before implementation hardens them. This is the "virtual designer critiquing an accessibility issue" use case.

```
/a11y-role-audit design <target> [--roles visual-design,ux-design]
```

### Implementation Review (after code)

Run all roles (or a subset) over implemented code to produce role-attributed findings — each finding tagged with who owns fixing it.

```
/a11y-role-audit code <target> [--roles all]
```

### Finding Attribution (post-critic)

After `a11y-critic` or `perspective-audit` produces findings, run the role-attribution pass to tag each finding with the responsible ARRM role. Uses the decision tree in `arrm-task-mapping.yaml`.

```
/a11y-role-audit attribute <findings-file>
```

## How Roles Combine

```
Visual Design      "Does the visual presentation work for all users?"
       ↕
UX Design          "Does the interaction pattern work for everyone?"
       ↕
Content Authoring  "Is the content clear and structured for all users?"
       ↕
Front-End Dev      "Is this implemented correctly in code?"
       ↕
Business Analysis  "Are requirements and processes supporting inclusion?"
       ↕
Testing            "Does this actually work with real assistive technology?"
```

Each role has explicit **blind spots** — things it cannot evaluate. When all six perspectives align, the result is robust accessibility. When any is missing, a category of barriers goes undetected.

## Attribution

Role definitions adapted from [Mike Gifford's ARRM-based roles](https://github.com/mgifford/accessibility-skills/tree/main/roles) (MIT), which apply the [W3C WAI ARRM framework](https://www.w3.org/WAI/planning/arrm/) to AI agent personas. ARRM task data sourced from the [W3C WAI ARRM repository](https://github.com/w3c/wai-arrm/).
