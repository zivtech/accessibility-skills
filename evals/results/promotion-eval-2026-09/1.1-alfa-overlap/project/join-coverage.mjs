import { readFileSync, writeFileSync } from "node:fs";
const reqMap = JSON.parse(readFileSync("requirements-map.json", "utf8"));
const RULE_TO_CRITERIA = reqMap.map;
const ruleIdOf = (uri) => uri.split("/").pop();

const PAGES = [1,2,3,4,5,6];
const failedRuleUris = new Set();
const perPageFailedCount = {};

for (const n of PAGES) {
  const alfaRaw = JSON.parse(readFileSync(`../raw/page-${n}-alfa.json`, "utf8"));
  let c = 0;
  for (const o of alfaRaw.outcomes) {
    if (o.outcome === "failed") {
      failedRuleUris.add(o.rule.uri);
      c++;
    }
  }
  perPageFailedCount[n] = c;
}

const mapped = [];
const unmapped = [];
for (const uri of failedRuleUris) {
  const criteria = RULE_TO_CRITERIA[uri] || [];
  if (criteria.length > 0) mapped.push(uri);
  else unmapped.push(uri);
}

console.log("Distinct Alfa rule ids with >=1 FAILED outcome across all 6 pages:", failedRuleUris.size);
console.log("  of those, mapped to >=1 WCAG criterion:", mapped.length);
console.log("  of those, unmapped (no criterion requirement):", unmapped.length);
console.log("  join coverage %:", ((mapped.length / failedRuleUris.size) * 100).toFixed(1));
console.log("  unmapped rule ids:", unmapped.map(ruleIdOf).join(", "));
console.log("  per-page raw FAILED outcome-entry counts (includes multi-target dup):", JSON.stringify(perPageFailedCount));

writeFileSync("join-coverage.json", JSON.stringify({
  totalFailedRuleIds: failedRuleUris.size,
  mappedCount: mapped.length,
  unmappedCount: unmapped.length,
  coveragePct: (mapped.length / failedRuleUris.size) * 100,
  unmappedRuleIds: unmapped.map(ruleIdOf),
}, null, 1));
