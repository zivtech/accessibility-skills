# Input: accessibility finding with cross-detector corroboration

Convert the finding below into an accessibility bug report ready to file as
a GitHub Issue, following the bug-reporting skill.

**Engagement context:** this finding belongs to a WCAG 2.2 AA audit of
permits.riverbend.example (evaluation_id `rmp-2026q3`). The scan environment
was Chrome 126 on macOS 15, viewport 1280×800. No Section 508 scope is
declared for this engagement.

```
finding_id: a11y_rmp_header_text_contrast
fingerprint: 3a7bc901
severity: MAJOR
wcag_or_apg: WCAG 1.4.3 Contrast (Minimum)
evaluation_context: evaluation_id=rmp-2026q3; sample_id=S01
evidence: body text on the blue permit-portal header bar at
  permits.riverbend.example/apply/step-1 measures 2.8:1 against the header
  background (#1a4a8c background, #e8edf4 text); 4.5:1 required for normal
  text (font-size 14px, font-weight 400); the defect appears on every page
  that uses this header pattern
html_snippet: >
  <header class="permit-header" style="background:#1a4a8c">
    <span class="header-label" style="color:#e8edf4">Building Permits</span>
  </header>
selector: .permit-header .header-label
detected_by: [axe-core, wave]
corroboration: corroborated
```
