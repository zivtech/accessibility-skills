import Rules from "@siteimprove/alfa-rules";

const rulesArr = [...Rules];
let foundCriterion = null;
for (const r of rulesArr) {
  for (const req of r.requirements) {
    if (req.type === "criterion") { foundCriterion = req; break; }
  }
  if (foundCriterion) break;
}
console.log("criterion toJSON:", JSON.stringify(foundCriterion.toJSON()));
console.log("criterion chapter:", foundCriterion.chapter);

const level = foundCriterion.level;
console.log("level.toJSON():", JSON.stringify(level.toJSON()));
console.log("level.toArray():", JSON.stringify(level.toArray()));

// try .get semantics via branch()
try {
  console.log("branch('2.2'):", JSON.stringify(level.branch ? level.branch("2.2") : "no branch method usable directly"));
} catch(e) { console.log("branch err:", e.message); }

// versions iterable
console.log("versions:", [...foundCriterion.versions]);

// Now scan across ALL rules: collect distinct req.type values, and for criterion reqs, print uri/chapter/level.toArray()
const typeSet = new Set();
let criterionCount = 0, sampleCriteria = [];
for (const r of rulesArr) {
  for (const req of r.requirements) {
    typeSet.add(req.type);
    if (req.type === "criterion" && sampleCriteria.length < 8) {
      sampleCriteria.push({ ruleUri: r.uri, chapter: req.chapter, uri: req.uri, levelArr: req.level.toArray() });
    }
    if (req.type === "criterion") criterionCount++;
  }
}
console.log("\nAll requirement types seen:", [...typeSet]);
console.log("Total criterion-typed requirement entries (across all rules, with dup):", criterionCount);
console.log("Sample criteria:", JSON.stringify(sampleCriteria, null, 1));
