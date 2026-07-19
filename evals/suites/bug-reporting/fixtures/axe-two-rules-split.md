# Input: axe-core scan result (two different rules)

Convert this scan output into accessibility bug report(s) ready to file as
GitHub Issue(s), following the bug-reporting skill.

```json
{
  "url": "https://app.example.io/settings/profile",
  "timestamp": "2026-07-15T16:44:02Z",
  "testEnvironment": {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36",
    "windowWidth": 1920,
    "windowHeight": 1080
  },
  "toolOptions": { "runner": "axe-core", "version": "4.9.1" },
  "violations": [
    {
      "id": "color-contrast",
      "impact": "serious",
      "tags": ["cat.color", "wcag2aa", "wcag143"],
      "description": "Ensures the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds",
      "help": "Elements must meet minimum color contrast ratio thresholds",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.9/color-contrast",
      "nodes": [
        {
          "html": "<span class=\"field-hint\">Shown on your public profile</span>",
          "target": ["#display-name-field > span.field-hint"],
          "failureSummary": "Fix any of the following: Element has insufficient color contrast of 3.13 (foreground color: #8b8b8b, background color: #f5f5f5, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        {
          "html": "<span class=\"field-hint\">Optional</span>",
          "target": ["#pronouns-field > span.field-hint"],
          "failureSummary": "Fix any of the following: Element has insufficient color contrast of 3.13 (foreground color: #8b8b8b, background color: #f5f5f5, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1"
        }
      ]
    },
    {
      "id": "link-name",
      "impact": "serious",
      "tags": ["cat.name-role-value", "wcag2a", "wcag244", "wcag412", "ACT"],
      "description": "Ensures links have discernible text",
      "help": "Links must have discernible text",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.9/link-name",
      "nodes": [
        {
          "html": "<a href=\"/help/profile-visibility\" class=\"help-icon\"><svg aria-hidden=\"true\"></svg></a>",
          "target": ["#visibility-section > a.help-icon"],
          "failureSummary": "Fix all of the following: Element is in tab order and does not have accessible text"
        }
      ]
    }
  ]
}
```
