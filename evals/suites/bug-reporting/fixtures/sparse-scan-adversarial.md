# Input: minimal scan output (incomplete data)

Convert this scan output into an accessibility bug report ready to file as a
GitHub Issue, following the bug-reporting skill.

```json
{
  "tool": "pa11y",
  "url": "/checkout",
  "issues": [
    {
      "code": "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail",
      "type": "error",
      "message": "This element has insufficient contrast at this conformance level. Expected a contrast ratio of at least 4.5:1, but text in this element has a contrast ratio of 2.9:1.",
      "selector": "#promo-banner > p",
      "context": "<p>Limited time offer — free shipping ends tonight</p>"
    }
  ]
}
```
