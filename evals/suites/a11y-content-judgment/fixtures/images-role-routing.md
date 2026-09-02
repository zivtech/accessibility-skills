# Input: content-judgment batch — images-role-routing

Northfield Health Monitor is a companion web dashboard for a home wellness wearable, used by everyday members to check their daily readings and longer trends. The audience is the general public, including older adults managing chronic conditions who are not comfortable with technical jargon. Two pages were captured: a daily dashboard and a thirty-day trends page.

Draft one accessibility judgment per row below for a named human ratifier.
Each row is one element captured from a live page of the product described
above: `type` (title | heading | link | image | field | ident), `sc` (the WCAG
success criterion the row belongs to), `name` (the text or accessible name the
user receives), `detail`, `href`, `context` (the surrounding text block),
`landmark`, `visible`, `views` (how many captured pages carry this unit), and
`flags` (heuristic labels attached by the inventory tool).

Return exactly one JSON line per input row, in input order, inside a single
```jsonl fence, with these keys and nothing else:

{"id","judgment":"yes|no|unsure","confidence":"high|medium|low","rationale":"one sentence, at most 25 words","fix":"at most 20 words; empty when yes","needs_human":true|false,"drafted_by":"<your model id>"}

```jsonl
{"id":"TITLE-HE-516192346d","type":"title","sc":"2.4.2","name":"Northfield Health Monitor — Trends","detail":"h1: Thirty-day trends","href":"https://www.northfield-healthmonitor.example/trends.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"TITLE-HE-d47648247f","type":"title","sc":"2.4.2","name":"Northfield Health Monitor — Today","detail":"h1: Today's summary","href":"https://www.northfield-healthmonitor.example/dashboard.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-0f8df2d6d4","type":"heading","sc":"2.4.6","name":"Today's reading","detail":"h2","href":null,"context":"","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-29ebc32566","type":"heading","sc":"2.4.6","name":"What moved the needle","detail":"h2","href":null,"context":"Sleep consistency improved the most, followed by a small increase in daily steps. Resting heart rate held steady.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-49e62f41c5","type":"heading","sc":"2.4.6","name":"Sharing with a caregiver","detail":"h2","href":null,"context":"You can share a read-only link to this page with a family member or caregiver from the settings menu.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-53d57fbb68","type":"heading","sc":"2.4.6","name":"Vitality Index over time","detail":"h2","href":null,"context":"Vitality Index rose from 38 to 42 over the last 30 days, driven mainly by improved sleep consistency.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-7709847ca1","type":"heading","sc":"2.4.6","name":"Recent activity screenshot","detail":"h2","href":null,"context":"A snapshot of yesterday's walk, captured automatically from your phone.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-8fa20fc6bd","type":"heading","sc":"2.4.6","name":"Your device","detail":"h2","href":null,"context":"Paired and syncing normally. Battery last checked this morning.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-a0ef4e53f8","type":"heading","sc":"2.4.6","name":"Vitality Index","detail":"h2","href":null,"context":"Your Vitality Index blends sleep, activity, and resting heart rate into a single daily number between zero and one hundred.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-a78eaf7d41","type":"heading","sc":"2.4.6","name":"Thirty-day trends","detail":"h1","href":null,"context":"Longer patterns often say more than any single day's number.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-aa72915d8c","type":"heading","sc":"2.4.6","name":"Today's summary","detail":"h1","href":null,"context":"Your device Paired and syncing normally. Battery last checked this morning.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-HE-fe58389cc8","type":"heading","sc":"2.4.6","name":"Status","detail":"h2","href":null,"context":"All systems normal","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"LINK-HE-755c745db2","type":"link","sc":"2.4.4","name":"Support","detail":"content","href":"https://www.northfield-healthmonitor.example/support.html","context":"","landmark":"footer","visible":true,"views":2,"flags":[]}
{"id":"LINK-HE-92d4a96b2f","type":"link","sc":"2.4.4","name":"","detail":"none; icon-only alt=\"\"","href":"https://www.northfield-healthmonitor.example/","context":"","landmark":"header","visible":false,"views":2,"flags":["link_empty_name","icon_only_link_weak_alt"]}
{"id":"LINK-HE-e500b02151","type":"link","sc":"2.4.4","name":"Today","detail":"content","href":"https://www.northfield-healthmonitor.example/dashboard.html","context":"","landmark":"nav","visible":true,"views":2,"flags":[]}
{"id":"LINK-HE-f511578a2b","type":"link","sc":"2.4.4","name":"Trends","detail":"content","href":"https://www.northfield-healthmonitor.example/trends.html","context":"","landmark":"nav","visible":true,"views":2,"flags":[]}
{"id":"IMAGE-HE-3874bb13ba","type":"image","sc":"1.1.1","name":"Vitality Index 42, Good","detail":"img 168x18; role:informative?; src vitality-today.png","href":"/charts/vitality-today.png","context":"Today's reading","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"IMAGE-HE-6b3ae0d95c","type":"image","sc":"1.1.1","name":"(alt=\"\")","detail":"img 0x0; role:functional; in a \"\"; src home.svg","href":"/icons/home.svg","context":"","landmark":"header","visible":false,"views":2,"flags":["functional_image_no_name"]}
{"id":"IMAGE-HE-6c04cd305c","type":"image","sc":"1.1.1","name":"(no alt attribute)","detail":"img 16x16; role:informative?; src screenshot.jpg","href":"/photos/screenshot.jpg","context":"Recent activity screenshot A snapshot of yesterday's walk, captured automatically from your phone.","landmark":"main","visible":true,"views":1,"flags":["img_missing_alt_attr"]}
{"id":"IMAGE-HE-81bb016fc0","type":"image","sc":"1.1.1","name":"Vitality Index trend, last 30 days","detail":"img 225x18; role:informative?; figcaption \"Vitality Index rose from 38 to 42 over the last 30 days, driven mainly by improved sleep consistency.\"; src vitality-trend.png","href":"/charts/vitality-trend.png","context":"Vitality Index over time Vitality Index rose from 38 to 42 over the last 30 days, driven mainly by improved sleep consistency.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"IMAGE-HE-8290c606ac","type":"image","sc":"1.1.1","name":"(alt=\"\")","detail":"img 0x0; role:decorative-declared; src check.svg","href":"/icons/check.svg","context":"All systems normal","landmark":"main","visible":false,"views":1,"flags":[]}
{"id":"IMAGE-HE-8b21f8062f","type":"image","sc":"1.1.1","name":"gauge","detail":"img 54x18; role:informative?; src vitality-gauge.png","href":"/charts/vitality-gauge.png","context":"Vitality Index Your Vitality Index blends sleep, activity, and resting heart rate into a single daily number between zero and one hundred.","landmark":"main","visible":true,"views":1,"flags":["complex_image_short_alt"]}
{"id":"IMAGE-HE-e521df0769","type":"image","sc":"1.1.1","name":"IMG_4021.jpg","detail":"img 112x18; role:informative?; src device.jpg","href":"/photos/device.jpg","context":"Your device Paired and syncing normally. Battery last checked this morning.","landmark":"main","visible":true,"views":1,"flags":["alt_is_filename"]}
```
