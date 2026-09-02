// Cross-engine overlap analysis. Loads raw/*.json + requirements-map.json,
// normalizes each engine's failures to WCAG 2.2 A/AA success criteria, and
// produces the per-page + cross-page overlap tables plus the threshold verdict.
import { readFileSync, writeFileSync } from "node:fs";

const RAW_DIR = process.env.RAW_DIR || "../raw";
const SCRATCH = process.env.SCRATCH_DIR || "..";

const reqMap = JSON.parse(readFileSync("requirements-map.json", "utf8"));
const RULE_TO_CRITERIA = reqMap.map; // rule.uri -> [{criterion, title, level_2_2}]

const PAGES = [1, 2, 3, 4, 5, 6];
const PAGE_URLS = {};

// ---------- normalizers ----------

// axe tag "wcagXYZ" (all digits) -> "X.Y.Z" (principle.guideline.sc; guideline is
// always a single digit in WCAG's own numbering, so this split is unambiguous)
function axeTagToSC(tag) {
  const m = /^wcag(\d+)$/.exec(tag);
  if (!m) return null;
  const digits = m[1];
  if (digits.length < 3) return null; // e.g. bare "wcag2"/"wcag21" style tags don't occur, guard anyway
  return `${digits[0]}.${digits[1]}.${digits.slice(2)}`;
}

function axeViolationSCs(violation) {
  const scs = new Set();
  for (const tag of violation.tags) {
    const sc = axeTagToSC(tag);
    if (sc) scs.add(sc);
  }
  return [...scs];
}

// htmlcs code "WCAG2AA.Principle3.Guideline3_1.3_1_1.H57.2" -> "3.1.1"
function htmlcsCodeToSC(code) {
  const parts = code.split(".");
  for (const p of parts) {
    if (/^\d+(_\d+){2,}$/.test(p)) {
      return p.split("_").join(".");
    }
  }
  return null;
}

// Alfa rule uri -> Alfa rule id
const ruleIdOf = (uri) => uri.split("/").pop();

// Alfa rule uri -> mapped [{criterion, level_2_2}], A/AA under 2.2 only
function alfaRuleAAcriteria(ruleUri) {
  const all = RULE_TO_CRITERIA[ruleUri] || [];
  return all.filter((c) => c.level_2_2 === "A" || c.level_2_2 === "AA");
}

// ---------- load + normalize per page ----------

const perPage = {};

for (const n of PAGES) {
  const axeRaw = JSON.parse(readFileSync(`${RAW_DIR}/page-${n}-axe.json`, "utf8"));
  const htmlcsRaw = JSON.parse(readFileSync(`${RAW_DIR}/page-${n}-htmlcs.json`, "utf8"));
  const alfaRaw = JSON.parse(readFileSync(`${RAW_DIR}/page-${n}-alfa.json`, "utf8"));
  PAGE_URLS[n] = axeRaw.url;

  // axe: violations -> SC set + evidence
  const axeSCs = new Map(); // SC -> [{ruleId, help, nodeHtml}]
  for (const v of axeRaw.violations || []) {
    for (const sc of axeViolationSCs(v)) {
      if (!axeSCs.has(sc)) axeSCs.set(sc, []);
      axeSCs.get(sc).push({ ruleId: v.id, help: v.help, example: (v.nodes[0]?.html || "").slice(0, 120) });
    }
  }

  // htmlcs: error-type issues -> SC set + evidence
  const htmlcsSCs = new Map();
  for (const i of htmlcsRaw.issues || []) {
    if (i.type !== "error") continue;
    const sc = htmlcsCodeToSC(i.code);
    if (!sc) continue;
    if (!htmlcsSCs.has(sc)) htmlcsSCs.set(sc, []);
    htmlcsSCs.get(sc).push({ code: i.code, message: i.message, example: (i.context || "").slice(0, 120) });
  }

  // alfa: FAILED outcomes, mapped to A/AA-2.2 criteria only
  const alfaSCs = new Map(); // SC -> [{ruleId, level, example}]
  const alfaFailedRules = new Map(); // ruleId -> {uri, criteria:[...], examples:[...]}
  const alfaCantTellRuleIds = new Set();

  for (const o of alfaRaw.outcomes || []) {
    if (o.outcome === "cantTell") alfaCantTellRuleIds.add(ruleIdOf(o.rule.uri));
    if (o.outcome !== "failed") continue;
    const ruleUri = o.rule.uri;
    const ruleId = ruleIdOf(ruleUri);
    const criteria = alfaRuleAAcriteria(ruleUri);
    if (criteria.length === 0) continue; // not mapped to an A/AA-2.2 criterion (unmapped or AAA-only)

    const msg =
      (o.expectations || [])
        .map(([, e]) => e?.error?.message)
        .find(Boolean) ||
      o.diagnostic?.message ||
      "";
    const example = `[${o.target?.type || "?"}] ${msg}`.slice(0, 120);

    if (!alfaFailedRules.has(ruleId)) {
      alfaFailedRules.set(ruleId, { uri: ruleUri, criteria, examples: [] });
    }
    if (alfaFailedRules.get(ruleId).examples.length < 3) {
      alfaFailedRules.get(ruleId).examples.push(example);
    }

    for (const c of criteria) {
      if (!alfaSCs.has(c.criterion)) alfaSCs.set(c.criterion, []);
      alfaSCs.get(c.criterion).push({ ruleId, level: c.level_2_2, example });
    }
  }

  perPage[n] = {
    url: axeRaw.url,
    axeSCs, // Map SC -> evidence[]
    htmlcsSCs,
    alfaSCs,
    alfaFailedRules, // Map ruleId -> {uri, criteria, examples}
    alfaCantTellRuleIds,
  };
}

// ---------- cross-engine per-page classification ----------

function scSetFromMap(m) {
  return new Set(m.keys());
}

const pageClassification = {}; // n -> {alfaOnly:Set, axeOnly:Set, htmlcsOnly:Set, multi:Set}

for (const n of PAGES) {
  const p = perPage[n];
  const a = scSetFromMap(p.alfaSCs);
  const x = scSetFromMap(p.axeSCs);
  const h = scSetFromMap(p.htmlcsSCs);
  const allSCs = new Set([...a, ...x, ...h]);

  const alfaOnly = new Set();
  const axeOnly = new Set();
  const htmlcsOnly = new Set();
  const multi = new Set();

  for (const sc of allSCs) {
    const flags = [a.has(sc), x.has(sc), h.has(sc)];
    const count = flags.filter(Boolean).length;
    if (count >= 2) multi.add(sc);
    else if (a.has(sc)) alfaOnly.add(sc);
    else if (x.has(sc)) axeOnly.add(sc);
    else if (h.has(sc)) htmlcsOnly.add(sc);
  }

  pageClassification[n] = { alfaOnly, axeOnly, htmlcsOnly, multi };
}

// ---------- Alfa-only RULE classes across all pages ----------
// A rule counts as "Alfa-only on page n" if at least one of its mapped A/AA-2.2
// criteria is in that page's alfaOnly SC set (i.e., failed by Alfa, and that SC
// was not also flagged -- as a violation/error -- by axe or htmlcs on the same page).

const alfaOnlyRuleHits = []; // {page, ruleId, uri, sc, level, example}
const alfaOnlyRuleIds = new Set();
const alfaOnlySCsGlobal = new Set();

for (const n of PAGES) {
  const p = perPage[n];
  const pageAlfaOnlySCs = pageClassification[n].alfaOnly;
  for (const [ruleId, info] of p.alfaFailedRules) {
    const hitCriteria = info.criteria.filter((c) => pageAlfaOnlySCs.has(c.criterion));
    if (hitCriteria.length === 0) continue;
    alfaOnlyRuleIds.add(ruleId);
    for (const c of hitCriteria) {
      alfaOnlySCsGlobal.add(c.criterion);
      alfaOnlyRuleHits.push({
        page: n,
        url: p.url,
        ruleId,
        uri: info.uri,
        sc: c.criterion,
        level: c.level_2_2,
        example: info.examples[0] || "",
      });
    }
  }
}

// dedupe rule hits to one representative example per (ruleId, sc) across pages
const repByRuleSC = new Map();
for (const hit of alfaOnlyRuleHits) {
  const key = `${hit.ruleId}::${hit.sc}`;
  if (!repByRuleSC.has(key)) repByRuleSC.set(key, hit);
}

writeFileSync(
  `${SCRATCH}/analysis-summary.json`,
  JSON.stringify(
    {
      alfaOnlyRuleIdCount: alfaOnlyRuleIds.size,
      alfaOnlyRuleIds: [...alfaOnlyRuleIds],
      alfaOnlySCsGlobalCount: alfaOnlySCsGlobal.size,
      alfaOnlySCsGlobal: [...alfaOnlySCsGlobal],
      repByRuleSC: [...repByRuleSC.entries()],
    },
    null,
    1
  )
);

console.log("=== Alfa-only distinct RULE classes across all 6 pages (A/AA-2.2, FAILED, not flagged by axe/htmlcs on the same page) ===");
console.log("Count:", alfaOnlyRuleIds.size);
console.log("Rule ids:", [...alfaOnlyRuleIds].join(", "));
console.log("Distinct SCs involved:", [...alfaOnlySCsGlobal].sort().join(", "));

// Export everything analyze needed downstream for the markdown writer
export { perPage, pageClassification, PAGE_URLS, alfaOnlyRuleHits, repByRuleSC, alfaOnlyRuleIds, alfaOnlySCsGlobal, RULE_TO_CRITERIA, ruleIdOf };
