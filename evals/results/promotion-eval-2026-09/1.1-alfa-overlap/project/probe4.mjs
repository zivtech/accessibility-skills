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

const failedOnes = json.outcomes.filter(o => o.outcome === "failed");
console.log("num failed:", failedOnes.length);
console.log(JSON.stringify(failedOnes.slice(0,3), null, 1));

const cantTellOnes = json.outcomes.filter(o => o.outcome === "cantTell");
console.log("num cantTell:", cantTellOnes.length);
console.log(JSON.stringify(cantTellOnes.slice(0,2), null, 1));

// distinct outcome values
console.log("distinct outcome vals:", [...new Set(json.outcomes.map(o=>o.outcome))]);

await browser.close();
