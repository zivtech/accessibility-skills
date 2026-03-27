# Baseline A: Zero-Shot Generic Planning Prompt

## Usage

This baseline represents a simple, unstructured request for an accessibility design plan. No protocol guidance, no examples, no emphasis on WCAG grounding or APG pattern mapping.

## Prompt

You are an accessibility expert. Create a comprehensive accessibility design plan for the following feature or component:

**Feature:** {feature_description}

Your plan should cover all aspects of accessibility including:
- Semantic HTML structure and landmarks
- ARIA attributes and roles
- Keyboard navigation and focus management
- State communication for interactive elements
- Visual accessibility (contrast, sizing, motion)
- Content accessibility (alt text, link text, form labels)
- Testing approach and acceptance criteria
- Implementation guidance

Ensure the plan is complete, specific, and implementable by a developer with no accessibility knowledge.

---

## Expected Performance

**Estimated composite score range:** 65-75
**Strengths:** Covers major accessibility topics, recognizes importance of ARIA and keyboard navigation
**Weaknesses:** No structured approach, may miss WCAG citations, may not map to APG patterns, incomplete focus management planning, limited testing strategy specificity

## Rationale

This baseline provides minimal structure and no examples, so the model must rely on general accessibility knowledge. It lacks:
- Explicit requirement for APG pattern mapping
- Requirement for WCAG 2.2 citations
- Structured protocol (9 phases)
- Examples of good practice
- Emphasis on WCAG grounding vs generic "accessibility"

Result: Competent but less comprehensive than a11y-planner with its 9-phase protocol.

