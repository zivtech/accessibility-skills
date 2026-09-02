// Runs axe-core (via @axe-core/playwright) and Alfa (via @siteimprove/alfa-test-utils
// + @siteimprove/alfa-playwright) against the same live Playwright page for each of
// the 6 target pages. One run per engine per page. Saves raw JSON to raw/.
import { chromium } from "playwright";
import { AxeBuilder } from "@axe-core/playwright";
import { Audit } from "@siteimprove/alfa-test-utils";
import { Playwright as AlfaPlaywright } from "@siteimprove/alfa-playwright";
import { writeFileSync, mkdirSync } from "node:fs";

const RAW_DIR = process.env.RAW_DIR || "../raw";
mkdirSync(RAW_DIR, { recursive: true });

const PAGES = [
  { n: 1, url: "https://example.com" },
  { n: 2, url: "https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/" },
  { n: 3, url: "https://www.w3.org/WAI/demos/bad/before/home.html" },
  { n: 4, url: "https://www.w3.org/WAI/demos/bad/before/news.html" },
  { n: 5, url: "https://www.w3.org/WAI/demos/bad/before/tickets.html" },
  { n: 6, url: "https://www.w3.org/WAI/demos/bad/before/survey.html" },
];

const AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

const browser = await chromium.launch();

for (const { n, url } of PAGES) {
  console.log(`\n=== Page ${n}: ${url} ===`);
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();
  const t0 = Date.now();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(3000);

  // --- axe-core ---
  try {
    const axeResults = await new AxeBuilder({ page }).withTags(AXE_TAGS).analyze();
    writeFileSync(
      `${RAW_DIR}/page-${n}-axe.json`,
      JSON.stringify(
        {
          page: n,
          url,
          engine: "axe-core",
          testEngineVersion: axeResults.testEngine?.version,
          tags: AXE_TAGS,
          violations: axeResults.violations,
          incomplete: axeResults.incomplete,
          passes_count: axeResults.passes?.length ?? null,
          timestamp: axeResults.timestamp,
        },
        null,
        1
      )
    );
    console.log(`  axe: ${axeResults.violations.length} violations, ${axeResults.incomplete.length} incomplete`);
  } catch (e) {
    console.log(`  axe FAILED: ${e.message}`);
    writeFileSync(`${RAW_DIR}/page-${n}-axe.json`, JSON.stringify({ page: n, url, engine: "axe-core", error: String(e) }, null, 1));
  }

  // --- Alfa ---
  try {
    const alfaPage = await AlfaPlaywright.toPage(await page.evaluateHandle(() => window.document));
    const audit = await Audit.run(alfaPage);
    const json = audit.toJSON();
    writeFileSync(
      `${RAW_DIR}/page-${n}-alfa.json`,
      JSON.stringify(
        {
          page: n,
          url,
          engine: "alfa",
          alfaVersion: json.alfaVersion,
          outcomes: json.outcomes,
          resultAggregates: json.resultAggregates,
          durations: json.durations,
        },
        null,
        1
      )
    );
    const failedCount = json.outcomes.filter((o) => o.outcome === "failed").length;
    const cantTellCount = json.outcomes.filter((o) => o.outcome === "cantTell").length;
    console.log(`  alfa: ${failedCount} failed outcomes, ${cantTellCount} cantTell outcomes, ${json.outcomes.length} total outcome entries`);
  } catch (e) {
    console.log(`  alfa FAILED: ${e.message}\n${e.stack}`);
    writeFileSync(`${RAW_DIR}/page-${n}-alfa.json`, JSON.stringify({ page: n, url, engine: "alfa", error: String(e), stack: e.stack }, null, 1));
  }

  await context.close();
  console.log(`  done in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}

await browser.close();
console.log("\nAll pages done.");
