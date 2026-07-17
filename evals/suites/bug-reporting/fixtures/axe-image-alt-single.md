# Input: axe-core scan result (single violation, single node)

Convert this scan output into an accessibility bug report ready to file as a
GitHub Issue, following the bug-reporting skill.

```json
{
  "url": "https://news.example.com/articles/spring-garden-guide",
  "timestamp": "2026-07-14T09:03:41Z",
  "testEnvironment": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36",
    "windowWidth": 1280,
    "windowHeight": 800
  },
  "toolOptions": { "runner": "axe-core", "version": "4.9.1" },
  "violations": [
    {
      "id": "image-alt",
      "impact": "critical",
      "tags": ["cat.text-alternatives", "wcag2a", "wcag111", "ACT"],
      "description": "Ensures <img> elements have alternate text or a role of none or presentation",
      "help": "Images must have alternate text",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.9/image-alt",
      "nodes": [
        {
          "html": "<img src=\"/img/hero-2481.jpg\" class=\"hero\">",
          "target": ["article.feature-story > img.hero"],
          "failureSummary": "Fix any of the following: Element does not have an alt attribute; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; element has no title attribute"
        }
      ]
    }
  ]
}
```
