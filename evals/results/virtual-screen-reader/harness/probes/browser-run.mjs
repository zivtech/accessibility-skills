import { chromium } from "playwright";
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("http://127.0.0.1:8931/probes/vsr-browser.html");
await page.waitForFunction(() => window.probeReady === true, { timeout: 10000 });
const result = await page.evaluate(() => window.probe());
console.log(JSON.stringify(result, null, 2));
await browser.close();
