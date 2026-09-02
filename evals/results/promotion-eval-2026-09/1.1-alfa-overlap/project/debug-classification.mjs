import { perPage, pageClassification, alfaOnlyRuleHits, RULE_TO_CRITERIA } from "./analyze.mjs";

for (const n of [1,2,3,4,5,6]) {
  const c = pageClassification[n];
  console.log(`\n--- Page ${n}: ${perPage[n].url} ---`);
  console.log("  alfaOnly SCs:", [...c.alfaOnly].sort());
  console.log("  axeOnly SCs:", [...c.axeOnly].sort());
  console.log("  htmlcsOnly SCs:", [...c.htmlcsOnly].sort());
  console.log("  multi (>=2 engines) SCs:", [...c.multi].sort());
  console.log("  Alfa distinct A/AA-2.2 FAILED rule count:", perPage[n].alfaFailedRules.size);
}

console.log("\n=== all alfaOnlyRuleHits ===");
for (const h of alfaOnlyRuleHits) {
  console.log(`page ${h.page} | ${h.ruleId} | SC ${h.sc} (${h.level}) | ${h.example}`);
}
