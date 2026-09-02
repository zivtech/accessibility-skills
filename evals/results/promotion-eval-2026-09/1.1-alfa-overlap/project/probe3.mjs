import { chromium } from "playwright";
import { Audit } from "@siteimprove/alfa-test-utils";
import { Playwright as AlfaPlaywright } from "@siteimprove/alfa-playwright";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto("https://example.com", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

const alfaPage = await AlfaPlaywright.toPage(await page.evaluateHandle(() => window.document));
const audit = await Audit.run(alfaPage);
const json = audit.toJSON();

console.log("Top-level keys:", Object.keys(json));
console.log("outcomes type:", Array.isArray(json.outcomes) ? "array" : typeof json.outcomes);
console.log("outcomes sample (first 2):", JSON.stringify(json.outcomes.slice ? json.outcomes.slice(0,2) : json.outcomes, null, 1).slice(0, 2000));
console.log("resultAggregates sample (first 5):", JSON.stringify(json.resultAggregates.slice(0,5), null, 1));
console.log("total outcome entries (Map size proxy):", json.outcomes.length);

await browser.close();
