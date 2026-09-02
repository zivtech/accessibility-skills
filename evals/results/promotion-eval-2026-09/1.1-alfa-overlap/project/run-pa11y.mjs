// Runs pa11y with the htmlcs (HTML_CodeSniffer) runner against each of the 6
// target pages. One run per page. Saves raw JSON to raw/.
import pa11y from "pa11y";
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

for (const { n, url } of PAGES) {
  console.log(`\n=== Page ${n}: ${url} ===`);
  const t0 = Date.now();
  try {
    const results = await pa11y(url, {
      runners: ["htmlcs"],
      standard: "WCAG2AA",
      includeWarnings: false,
      viewport: { width: 1280, height: 800 },
      timeout: 60000,
      wait: 3000,
      chromeLaunchConfig: {
        // pa11y bundles puppeteer; keep default headless chromium it installed
      },
    });
    writeFileSync(
      `${RAW_DIR}/page-${n}-htmlcs.json`,
      JSON.stringify(
        {
          page: n,
          url,
          engine: "htmlcs (pa11y)",
          documentTitle: results.documentTitle,
          pageUrl: results.pageUrl,
          issues: results.issues,
        },
        null,
        1
      )
    );
    const errorCount = results.issues.filter((i) => i.type === "error").length;
    console.log(`  htmlcs: ${results.issues.length} issues total (${errorCount} errors)`);
  } catch (e) {
    console.log(`  htmlcs FAILED: ${e.message}`);
    writeFileSync(`${RAW_DIR}/page-${n}-htmlcs.json`, JSON.stringify({ page: n, url, engine: "htmlcs (pa11y)", error: String(e) }, null, 1));
  }
  console.log(`  done in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}

console.log("\nAll pages done.");
