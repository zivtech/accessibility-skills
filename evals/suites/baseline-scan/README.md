# baseline-scan regression rig

Proves the automated slice of "old defect classes still get caught on a new
target": `baseline-url-scan.mjs --census` fires every expected axe rule and
census check on `fixtures/synthetic-target.html` (a fictional public
library catalog page planting 14 known defect classes) and stays silent on
`fixtures/clean-sibling.html` (same layout, done correctly — zero axe
violations, zero census findings, verified by running). See
`expected-rules.json` for the defect -> rule map, built from and reproduced
against a real run.

**Does NOT prove:** two planted classes (a div-based fake list, a
headerless layout table) fire no rule in this stack at all — real gaps for
manual/critic review, not rig bugs — nor any interaction/judgment evidence
(keyboard operability, focus order, SR announcements); that's
`keyboard-a11y-tester` / `virtual-screen-reader` per the a11y-test
Verification evidence contract.

**Reproduce:**
```bash
npm install -D playwright @axe-core/playwright && npx playwright install chromium
bash evals/suites/baseline-scan/run_rig.sh
```
