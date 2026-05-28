# Manual Axe Check: LABEL-IN-NAME-004 Filter Format Configure Links

> Status: Manual before/after evidence captured
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> URL: `http://drupal-core.ddev.site:33000/admin/config/content/formats`
> Rule used: `label-content-name-mismatch`

## Why This Manual Check Was Needed

The generated evaluator config for `a11y-LABEL-IN-NAME-004-filter-format-aria-label` requests `label-in-name`, but the installed axe-core rule ID is `label-content-name-mismatch`. As a result, the evaluator report was `INCONCLUSIVE` even though the underlying accessible-name mismatch exists.

## Before Patch

Exact command used; exit code `0`:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
set -e
cleanup() {
  git apply -R patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label.patch >/dev/null 2>&1 || true
  ddev drush cache-rebuild >/dev/null 2>&1 || true
}
trap cleanup EXIT
node <<'NODE'
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const axePath = require.resolve('axe-core/axe.min.js');
const base = process.env.DRUPAL_BASE_URL || 'http://drupal-core.ddev.site:33000';

async function inspect(label) {
  const uli = execSync('ddev drush user:login --uid=1 --uri=' + base, { encoding: 'utf8' })
    .trim()
    .split(/\s+/)
    .find((part) => part.startsWith('http'));
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 1024 } });
  await page.goto(uli, { waitUntil: 'domcontentloaded' });
  await page.goto(base + '/admin/config/content/formats', { waitUntil: 'networkidle' });
  await page.addScriptTag({ path: axePath });
  const axe = await page.evaluate(async () => {
    const results = await window.axe.run(document, {
      runOnly: { type: 'rule', values: ['label-content-name-mismatch'] },
    });
    return results.violations.map((violation) => ({
      id: violation.id,
      nodes: violation.nodes.map((node) => ({
        target: node.target,
        html: node.html,
        failureSummary: node.failureSummary,
      })),
    }));
  });
  const links = await page.locator('table a:has-text("Configure")').evaluateAll((nodes) =>
    nodes.map((node) => ({
      text: node.textContent.trim(),
      ariaLabel: node.getAttribute('aria-label'),
    }))
  );
  console.log(JSON.stringify({ label, axeViolationCount: axe.reduce((count, violation) => count + violation.nodes.length, 0), axe, links }, null, 2));
  await browser.close();
}

(async () => {
  await inspect('before');
})();
NODE
git apply patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label.patch
ddev drush cache-rebuild
node <<'NODE'
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const axePath = require.resolve('axe-core/axe.min.js');
const base = process.env.DRUPAL_BASE_URL || 'http://drupal-core.ddev.site:33000';

(async () => {
  const uli = execSync('ddev drush user:login --uid=1 --uri=' + base, { encoding: 'utf8' })
    .trim()
    .split(/\s+/)
    .find((part) => part.startsWith('http'));
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 1024 } });
  await page.goto(uli, { waitUntil: 'domcontentloaded' });
  await page.goto(base + '/admin/config/content/formats', { waitUntil: 'networkidle' });
  await page.addScriptTag({ path: axePath });
  const axe = await page.evaluate(async () => {
    const results = await window.axe.run(document, {
      runOnly: { type: 'rule', values: ['label-content-name-mismatch'] },
    });
    return results.violations.map((violation) => ({
      id: violation.id,
      nodes: violation.nodes.map((node) => ({
        target: node.target,
        html: node.html,
        failureSummary: node.failureSummary,
      })),
    }));
  });
  const links = await page.locator('table a:has-text("Configure")').evaluateAll((nodes) =>
    nodes.map((node) => ({
      text: node.textContent.trim(),
      ariaLabel: node.getAttribute('aria-label'),
    }))
  );
  console.log(JSON.stringify({ label: 'after', axeViolationCount: axe.reduce((count, violation) => count + violation.nodes.length, 0), axe, links }, null, 2));
  await browser.close();
})();
NODE
```

Tool versions:

```text
axe-core: 4.11.4
Playwright: installed in the runtime checkout root dependencies
```

Observed before patch:

```text
axeViolationCount: 4
Configure link aria-label values:
- Edit Basic HTML
- Edit Restricted HTML
- Edit Full HTML
- Edit Plain text
```

Each failing link had visible text `Configure`, but the visible text was not included in the accessible name.

## After Patch

Patch applied:

```bash
git apply patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label.patch
ddev drush cache-rebuild
```

Observed after patch:

```text
axeViolationCount: 0
Configure link aria-label values:
- Configure Basic HTML
- Configure Restricted HTML
- Configure Full HTML
- Configure Plain text
```

The patch was then reverted and cache was rebuilt.

## Interpretation

Manual evidence supports the patch's intended fix for the target route. The remaining blocker is evaluator accuracy: replace or alias `label-in-name` to axe-core's `label-content-name-mismatch`, then rerun the standard evaluator with broad regression classification before marking the patch `VERIFIED`.
