import Rules from "@siteimprove/alfa-rules";
const ids = ["sia-r85","sia-r61","sia-r57","sia-r87","sia-r70","sia-r72"];
for (const r of Rules) {
  const id = r.uri.split("/").pop();
  if (ids.includes(id)) {
    const reqTitles = r.requirements.map(req => `${req.type}:${req.title || req.uri}`);
    console.log(id, "->", reqTitles.join(" | "));
  }
}
