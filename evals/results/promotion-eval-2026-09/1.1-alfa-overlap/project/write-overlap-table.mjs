import { readFileSync, writeFileSync } from "node:fs";
import { perPage, pageClassification, alfaOnlyRuleHits, RULE_TO_CRITERIA, ruleIdOf } from "./analyze.mjs";

const PAGES = [1,2,3,4,5,6];
const PAGE_LABELS = {
  1: "1. example.com",
  2: "2. WAI-ARIA APG disclosure-faq example",
  3: "3. WAI \"Before\" demo — home.html",
  4: "4. WAI \"Before\" demo — news.html",
  5: "5. WAI \"Before\" demo — tickets.html",
  6: "6. WAI \"Before\" demo — survey.html",
};

let md = `# Cross-engine overlap analysis: Alfa vs axe-core vs HTML_CodeSniffer (htmlcs)\n\n`;
md += `Generated ${new Date().toISOString()}. Method and versions: see README.md.\n\n`;
md += `Legend: FAILED rule classes only (Alfa \`cantTell\` outcomes are excluded from all counts below and reported separately). SC = WCAG 2.2 success criterion; only A/AA-level SCs are in scope (AAA-only mapped criteria are dropped per the analysis rule).\n\n`;

for (const n of PAGES) {
  const p = perPage[n];
  const c = pageClassification[n];
  md += `## Page ${PAGE_LABELS[n]}\n\n`;
  md += `URL: ${p.url}\n\n`;

  md += `### FAILED rule classes per engine, normalized to WCAG 2.2 A/AA SC\n\n`;
  md += `| SC | axe | htmlcs | Alfa | Engines agreeing |\n|---|---|---|---|---|\n`;
  const allSCs = new Set([...p.axeSCs.keys(), ...p.htmlcsSCs.keys(), ...p.alfaSCs.keys()]);
  const sortedSCs = [...allSCs].sort((a,b) => a.localeCompare(b, undefined, {numeric:true}));
  if (sortedSCs.length === 0) {
    md += `| _none_ | | | | |\n`;
  }
  for (const sc of sortedSCs) {
    const hasAxe = p.axeSCs.has(sc) ? "✓" : "";
    const hasHtmlcs = p.htmlcsSCs.has(sc) ? "✓" : "";
    const hasAlfa = p.alfaSCs.has(sc) ? "✓" : "";
    const n_engines = [hasAxe, hasHtmlcs, hasAlfa].filter(Boolean).length;
    md += `| ${sc} | ${hasAxe} | ${hasHtmlcs} | ${hasAlfa} | ${n_engines} |\n`;
  }

  const alfaCantTellCount = p.alfaCantTellRuleIds.size;
  md += `\nAlfa \`cantTell\` rule classes on this page (not counted as failures, listed for completeness): ${alfaCantTellCount ? [...p.alfaCantTellRuleIds].join(", ") : "none"}\n\n`;

  md += `### Cross-engine classification (by SC)\n\n`;
  md += `- Alfa-only: ${c.alfaOnly.size ? [...c.alfaOnly].sort().join(", ") : "none"}\n`;
  md += `- axe-only: ${c.axeOnly.size ? [...c.axeOnly].sort().join(", ") : "none"}\n`;
  md += `- htmlcs-only: ${c.htmlcsOnly.size ? [...c.htmlcsOnly].sort().join(", ") : "none"}\n`;
  md += `- Flagged by ≥2 engines: ${c.multi.size ? [...c.multi].sort().join(", ") : "none"}\n\n`;
}

md += `## Cross-page summary: distinct Alfa-only A/AA rule classes\n\n`;
md += `"Alfa-only" = an Alfa rule FAILED on a page, mapped to an A/AA-under-2.2 WCAG criterion, where that criterion was **not** flagged (as a violation/error) by axe or htmlcs on the **same page**.\n\n`;

const byRuleSc = new Map();
for (const h of alfaOnlyRuleHits) {
  const key = `${h.ruleId}::${h.sc}`;
  if (!byRuleSc.has(key)) byRuleSc.set(key, h);
}
const rows = [...byRuleSc.values()];

md += `| Alfa rule id | SC | Level (2.2) | Page found on | Example target (≤120 chars, agent-assessed) | Assessment |\n|---|---|---|---|---|---|\n`;

const assessments = {
  "sia-r14": "plausible true positive — visible text “skip to content option0” vs. accessible name “skip to content shortcut option 0” is a real SC 2.5.3 Label-in-Name mismatch (voice-control users saying the visible label won't reliably match); worth a human check of the live disclosure-faq page markup to rule out a stray templating artifact, but the mismatch itself is real, not a parsing error.",
  "sia-r69": "plausible true positive — Alfa reports a specific computed contrast ratio (4.02:1) against the AA threshold (4.5:1) with the actual foreground/background sRGB values; this is a quantitative, checkable claim, not a heuristic guess. A human should confirm with a contrast checker against the live page, but the arithmetic is falsifiable and the ratio is close enough to the threshold that a real near-miss is plausible.",
};

for (const h of rows) {
  md += `| ${h.ruleId} | ${h.sc} | ${h.level} | ${h.page} | ${h.example.replace(/\|/g, "\\|").replace(/\n/g, " ")} | ${assessments[h.ruleId] || "agent-assessed, needs human confirmation"} |\n`;
}

md += `\n**Distinct Alfa-only A/AA rule classes across all 6 pages: ${new Set(rows.map(r=>r.ruleId)).size}** (${[...new Set(rows.map(r=>r.ruleId))].join(", ")})\n\n`;
md += `All assessments above are agent-assessed and need human confirmation before being treated as verified findings.\n\n`;

md += `## Threshold verdict\n\n`;
const distinctCount = new Set(rows.map(r=>r.ruleId)).size;
const meetsCountBar = distinctCount >= 3;
const hasPlausibleTP = rows.some(r => (assessments[r.ruleId]||"").startsWith("plausible true positive"));
const verdict = (meetsCountBar && hasPlausibleTP) ? "THRESHOLD CANDIDATE" : "BELOW THRESHOLD";
md += `Pre-declared rule: Alfa is a "threshold candidate" only if it fails ≥3 distinct A/AA rule classes that neither axe nor htmlcs flagged on the same page, AND at least one of those is a plausible true positive.\n\n`;
md += `- Distinct Alfa-only A/AA rule classes found: **${distinctCount}** (need ≥3)\n`;
md += `- At least one plausible true positive among them: **${hasPlausibleTP ? "yes" : "no"}**\n`;
md += `- **Verdict: ${verdict}**\n\n`;
if (verdict === "BELOW THRESHOLD") {
  md += `The count bar (≥3) is not met (found ${distinctCount}), even though both findings that were found look like genuine, checkable defects. The pre-declared rule is not softened for this result.\n`;
}

writeFileSync("../overlap-table.md", md);
console.log("Wrote overlap-table.md, verdict:", verdict, "distinctCount:", distinctCount);
