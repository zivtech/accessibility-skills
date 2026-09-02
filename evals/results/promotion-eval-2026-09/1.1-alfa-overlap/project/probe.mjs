import Rules from "@siteimprove/alfa-rules";
import { Branched } from "@siteimprove/alfa-branched";

const rulesArr = [...Rules];
console.log("Total rules:", rulesArr.length);

const r0 = rulesArr[0];
console.log("Sample rule uri:", r0.uri);
console.log("Sample rule tags:", r0.tags.map(t => t.toJSON ? JSON.stringify(t.toJSON()) : String(t)));
console.log("Sample rule requirements count:", r0.requirements.length);
for (const req of r0.requirements) {
  console.log("  req type:", req.type, "uri:", req.uri, "hasLevel:", "level" in req, "hasTitle:", "title" in req);
}

// find a rule with a criterion requirement
let foundCriterion = null;
for (const r of rulesArr) {
  for (const req of r.requirements) {
    if (req.type === "criterion") {
      foundCriterion = req;
      break;
    }
  }
  if (foundCriterion) break;
}
console.log("\nFirst criterion requirement uri:", foundCriterion?.uri);
console.log("title:", foundCriterion?.title);
const level = foundCriterion?.level;
console.log("level object:", level);
console.log("level.constructor.name:", level?.constructor?.name);
console.log("Branched.isBranched:", Branched.isBranched ? Branched.isBranched(level) : "n/a");
// try to inspect Branched API
console.log("Branched keys on instance:", level ? Object.getOwnPropertyNames(Object.getPrototypeOf(level)) : "n/a");
