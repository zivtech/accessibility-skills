// Build a uri -> [{criterion, title, level_2_2}] map from @siteimprove/alfa-rules.
// This is the "requirements join" the task asks to document exactly.
//
// Method:
// 1. Import the default export of @siteimprove/alfa-rules — a Sequence of all
//    89 "stable" Flattened.Rule objects (same set Audit.run() uses by default).
// 2. For each rule, read rule.uri (e.g. "https://alfa.siteimprove.com/rules/sia-r1")
//    and rule.requirements (an array of Requirement objects of mixed .type:
//    "criterion" | "eaa" | "technique" | "ARIA" | "best practice").
// 3. Keep only requirements with .type === "criterion" (these are actual
//    @siteimprove/alfa-wcag Criterion instances). Each has:
//      .chapter -> the WCAG SC number as a string, e.g. "2.4.2"
//      .title   -> the SC title, e.g. "Page Titled"
//      .level   -> a Branched<Level, Version> value. Its .toJSON() serializes
//                  as an array of [level, [versions...]] pairs, e.g.
//                  [["A", ["2.2","2.1","2.0"]]] or [["AA",["2.2"]]].
//                  We scan this array for the pair whose versions list
//                  includes "2.2" and take that pair's level as level_2_2.
//                  If no pair's versions list includes "2.2", the criterion
//                  is not defined/applicable under WCAG 2.2 (rare; recorded
//                  as level_2_2: null).
// 4. A rule can carry more than one criterion requirement (e.g. sia-r11 maps
//    to 2.4.4, 2.4.9, and 4.1.2), so the map value is a list.
// 5. Rules with zero "criterion" requirements (technique/ARIA/eaa/best-practice
//    only) map to an empty list — these are the "unmapped" rules reported
//    separately per the task's join-coverage requirement.
import Rules from "@siteimprove/alfa-rules";
import { writeFileSync } from "node:fs";

function level2_2(criterionReq) {
  const pairs = criterionReq.level.toJSON(); // [[level, [versions]], ...]
  const hit = pairs.find(([, versions]) => versions.includes("2.2"));
  return hit ? hit[0] : null;
}

const rulesArr = [...Rules];
const map = {}; // rule.uri -> [{criterion, title, level_2_2}]
const unmapped = []; // rule.uri of rules with zero criterion requirements
const ruleIdOf = (uri) => uri.split("/").pop();

for (const rule of rulesArr) {
  const criteria = rule.requirements
    .filter((r) => r.type === "criterion")
    .map((c) => ({
      criterion: c.chapter,
      title: c.title,
      level_2_2: level2_2(c),
    }));

  map[rule.uri] = criteria;
  if (criteria.length === 0) {
    unmapped.push({ uri: rule.uri, id: ruleIdOf(rule.uri), tags: rule.tags.map((t) => t.toJSON()) });
  }
}

const totalRules = rulesArr.length;
const mappedRuleCount = totalRules - unmapped.length;

const out = {
  meta: {
    totalRules,
    mappedRuleCount,
    unmappedRuleCount: unmapped.length,
    alfaRulesVersion: (await import("@siteimprove/alfa-rules")).alfaVersion,
    generatedAt: new Date().toISOString(),
  },
  map,
  unmapped,
};

writeFileSync("requirements-map.json", JSON.stringify(out, null, 1));
console.log(`Total rules: ${totalRules}`);
console.log(`Rules with >=1 WCAG criterion requirement: ${mappedRuleCount}`);
console.log(`Rules with zero criterion requirements (unmapped): ${unmapped.length}`);
console.log("Unmapped rule ids:", unmapped.map((u) => u.id).join(", "));
