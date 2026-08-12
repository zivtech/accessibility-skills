# Input: axe-core scan result from a declared Section 508 audit (single violation, single node)

Convert this scan output into an accessibility bug report ready to file as a
GitHub Issue, following the bug-reporting skill.

**Engagement context:** this scan belongs to a declared Revised Section 508
audit — the engagement's audit-scope plan carries the conformance floor
declaration (evaluation_id `rga-portal-2026q3`). Apply the skill's rules for
that scope, including the baseline test citation. The engagement's valid
baseline test IDs (web baseline, from the pinned manifest) are:

```text
1.A-KeyboardAccess
1.B-NoKeyboardTrap
2.A-FocusVisible
2.B-FocusOrder
2.C-OnFocus
3.A-NonInterference
4.A-BypassBlocks
4.B-ConsistentNavigation
4.C-ConsistentIdentification
5.A-ControlName
5.B-ControlRole
5.C-ControlState
5.D-ControlValue
6.A-MeaningfulImage
6.B-DecorativeImage
6.C-Captcha
6.D-ImageText
7.A-Color
7.B-SensoryCharacteristics
7.C-AudibleCues
8.A-ContrastMinimum
9.A-Flashes
10.A-FormName
10.B-FormDescriptiveLabel
10.C-OnInput
10.D-ErrorIdentification
10.E-FormHasLabel
10.F-ErrorSuggestion
10.G-ErrorPrevention
11.A-PageTitled
12.A-DataTableRole
12.B-DataTableHeaderAssociation
12.C-LayoutTable
13.A-HeadingDescriptive
13.B-VisHeadingProg
13.C-ProgHeadingVisual
13.D-List
14.A-LinkPurpose
15.A-LanguagePage
15.B-LanguagePart
16.A-AudioOnlyTranscript
16.B-VideoOnlyAlt
16.C-AudioMediaAlternative
16.D-VideoMediaAlternative
17.A-MediaPlayerCCADControls
17.B-MediaPlayerCCLevel
17.C-MediaPlayerADLevel
17.D-CaptionsPrerecorded
17.E-ADPrerecorded
17.F-CaptionsLive
17.G-SyncMediaAlternative
18.B-CSSPositionedContent
19.A-FrameTitle
19.B-iFrameName
20.A-ConformingAltVersion
21.A-TimingAdjustable
21.B-MovingInfo
21.C-AutoUpdate
21.D-AudioControl
22.A-ResizeText
23.A-MultipleWays
24.A-Parsing
```

```json
{
  "url": "https://apply.ruralgrants.example.gov/application/step-2",
  "timestamp": "2026-08-12T14:22:07Z",
  "testEnvironment": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36",
    "windowWidth": 1280,
    "windowHeight": 800
  },
  "toolOptions": { "runner": "axe-core", "version": "4.9.1" },
  "violations": [
    {
      "id": "button-name",
      "impact": "critical",
      "tags": ["cat.name-role-value", "wcag2a", "wcag412", "ACT", "TTv5", "TT6.a"],
      "description": "Ensures buttons have discernible text",
      "help": "Buttons must have discernible text",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.9/button-name",
      "nodes": [
        {
          "html": "<button class=\"doc-remove\"><svg aria-hidden=\"true\" viewBox=\"0 0 16 16\"><path d=\"M4 4l8 8m0-8l-8 8\"/></svg></button>",
          "target": ["ul.uploaded-docs > li:nth-child(3) button.doc-remove"],
          "failureSummary": "Fix any of the following: Element does not have inner text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; element has no title attribute"
        }
      ]
    }
  ]
}
```
