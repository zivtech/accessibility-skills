#!/bin/bash
# Verbatim commands run for the Alfa vs axe/htmlcs overlap measurement.
# All work happened under $SCRATCH/project (npm project) and $SCRATCH/raw (scan output).

SCRATCH=/private/tmp/claude-501/-Users-AlexUA-1-claude-accessibility-skills/cc4558f7-32f1-41a4-ae3c-334870666e5a/scratchpad/phase1/1.1-alfa-overlap
mkdir -p "$SCRATCH/project" "$SCRATCH/raw"
cd "$SCRATCH/project"

# --- setup ---
npm init -y

npm install --save-exact \
  @siteimprove/alfa-test-utils@0.84.2 \
  @siteimprove/alfa-playwright@0.84.2 \
  playwright@1.62.1 \
  @axe-core/playwright@4.13.0 \
  pa11y

npx playwright install chromium

# resolved versions (recorded after install; see README.md for the full table)
node -p "require('./node_modules/@siteimprove/alfa-test-utils/package.json').version"
node -p "require('./node_modules/@siteimprove/alfa-playwright/package.json').version"
node -p "require('./node_modules/@siteimprove/alfa-rules/package.json').version"
node -p "require('./node_modules/@siteimprove/alfa-wcag/package.json').version"
node -p "require('./node_modules/playwright/package.json').version"
node -p "require('./node_modules/@axe-core/playwright/package.json').version"
node -p "require('./node_modules/axe-core/package.json').version"
node -p "require('./node_modules/pa11y/package.json').version"
node -p "require('./node_modules/@pa11y/html_codesniffer/package.json').version"

# --- robots.txt check (once) ---
curl -s https://example.com/robots.txt -w "\nHTTP:%{http_code}\n"
curl -s https://www.w3.org/robots.txt | grep -iE "wai|demos"

# --- requirements join: build rule.uri -> WCAG criteria map from @siteimprove/alfa-rules ---
node build-requirements-map.mjs
# writes project/requirements-map.json

# --- scans (one run per engine per page, 1280x800, domcontentloaded + 3s settle) ---
RAW_DIR="$SCRATCH/raw" node run-axe-alfa.mjs   # axe-core + Alfa, same live Playwright page per site
RAW_DIR="$SCRATCH/raw" node run-pa11y.mjs      # pa11y with runners:['htmlcs'], standard 'WCAG2AA', includeWarnings:false

# --- analysis ---
node join-coverage.mjs                          # join coverage % + unmapped rule ids
RAW_DIR="$SCRATCH/raw" SCRATCH_DIR="$SCRATCH" node analyze.mjs   # per-page + cross-page classification
node write-overlap-table.mjs                    # writes $SCRATCH/overlap-table.md + threshold verdict

# --- deliverable copies ---
cp package.json package-lock.json "$SCRATCH/"
