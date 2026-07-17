# Input: axe-core scan result (one rule, two nodes, crawl context)

Convert this scan output into accessibility bug report(s) ready to file as
GitHub Issue(s), following the bug-reporting skill.

```json
{
  "url": "https://shop.example.org/products?category=outdoor",
  "timestamp": "2026-07-15T14:22:09Z",
  "testEnvironment": { "userAgent": "Mozilla/5.0 Chrome/126.0", "windowWidth": 1440, "windowHeight": 900 },
  "toolOptions": { "runner": "axe-core", "version": "4.9.1" },
  "violations": [
    {
      "id": "select-name",
      "impact": "critical",
      "tags": ["cat.forms", "wcag2a", "wcag412", "ACT"],
      "description": "Ensures select element has an accessible name",
      "help": "Select element must have an accessible name",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.9/select-name",
      "nodes": [
        {
          "html": "<select class=\"sort-control\"><option value=\"price-asc\">Price: Low to High</option><option value=\"price-desc\">Price: High to Low</option></select>",
          "target": ["#product-toolbar > select.sort-control"],
          "failureSummary": "Fix any of the following: Form element does not have an implicit (wrapped) <label>; Form element does not have an explicit <label>; aria-label attribute does not exist or is empty"
        },
        {
          "html": "<select class=\"sort-control\"><option value=\"newest\">Newest</option><option value=\"rating\">Rating</option></select>",
          "target": ["#mobile-toolbar > select.sort-control"],
          "failureSummary": "Fix any of the following: Form element does not have an implicit (wrapped) <label>; Form element does not have an explicit <label>; aria-label attribute does not exist or is empty"
        }
      ]
    }
  ],
  "crawl_context": { "pages_scanned": 38, "pages_with_this_violation": 19, "notes": "sort control appears in the shared product-listing template" }
}
```
