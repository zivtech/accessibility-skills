# Input: content-judgment batch — clean-control

Briarcliff Community Center offers classes, studio space, and youth programs for the general public in its neighborhood. Most visitors are residents browsing class offerings, but one section is aimed at certified pottery instructors who already know the center's internal studio shorthand, including "SKC-2" (Studio Kiln Certification, Level 2). Three pages were captured: the home page, a class listing page, and an instructor requirements page.

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
{"id":"TITLE-CO-489de8946e","type":"title","sc":"2.4.2","name":"Briarcliff Community Center — Instructor Requirements","detail":"h1: Instructor requirements","href":"https://www.briarcliff-community.example/instructors.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"TITLE-CO-a92da72862","type":"title","sc":"2.4.2","name":"Briarcliff Community Center — Class Schedule","detail":"h1: Welcome to Briarcliff Community Center","href":"https://www.briarcliff-community.example/index.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"TITLE-CO-ff952e02cd","type":"title","sc":"2.4.2","name":"Briarcliff Community Center Department of Recreation and Lifelong Learning Fall Session Course Catalog","detail":"h1: Fall class catalog","href":"https://www.briarcliff-community.example/classes.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-01c0e1fe88","type":"heading","sc":"2.4.6","name":"Register for Fall Pottery Class","detail":"h2","href":null,"context":"Six Tuesday evenings covering wheel-throwing basics. All materials and one glaze firing are included.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-333a24dd3f","type":"heading","sc":"2.4.6","name":"Youth Swim Lessons: Ages 6-10","detail":"h2","href":null,"context":"Small groups of six children per instructor, held Saturday mornings at the indoor pool.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-432b03f5e8","type":"heading","sc":"2.4.6","name":"Fall class catalog","detail":"h1","href":null,"context":"Registration opens two weeks before each session and closes once a class fills.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-43cffb6185","type":"heading","sc":"2.4.6","name":"Instructor requirements","detail":"h1","href":null,"context":"This page is for certified studio instructors renewing their kiln clearance for the coming season.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-5342aa957e","type":"heading","sc":"2.4.6","name":"Certified Studio Kiln Operation and Safety Compliance Requirements for Instructional Staff","detail":"h2","href":null,"context":"Every instructor leading a firing must hold a current clearance on file with the studio manager before the first class of the term.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-5a41d9eca2","type":"heading","sc":"2.4.6","name":"New Studio Now Open","detail":"h2","href":null,"context":"New Studio Now Open","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-6952395793","type":"heading","sc":"2.4.6","name":"Welcome to Briarcliff Community Center","detail":"h1","href":null,"context":"Browse this fall's classes, studio hours, and youth programs, or drop by the front desk with questions any weekday morning.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-a71c39affe","type":"heading","sc":"2.4.6","name":"Full schedule","detail":"h2","href":null,"context":"View the fall class schedule","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-b7dd32d005","type":"heading","sc":"2.4.6","name":"Submit your renewal","detail":"h2","href":null,"context":"Instructor ID SKC-2 Level Submit renewal","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-CO-e78ec7135c","type":"heading","sc":"2.4.6","name":"Getting here","detail":"h2","href":null,"context":"The center is a short walk from the Elm Street bus stop, with free parking behind the building.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"FIELD-CO-367e158395","type":"field","sc":"2.4.6","name":"SKC-2 Level","detail":"text; label from label[for]","href":null,"context":"","landmark":"form","visible":true,"views":1,"flags":[]}
{"id":"FIELD-CO-617f5a88b7","type":"field","sc":"2.4.6","name":"Instructor ID","detail":"text; label from label[for]","href":null,"context":"","landmark":"form","visible":true,"views":1,"flags":[]}
{"id":"LINK-CO-26172863dc","type":"link","sc":"2.4.4","name":"View the fall class schedule","detail":"content; file pdf","href":"https://www.briarcliff-community.example/files/fall-schedule.pdf","context":"Full schedule View the fall class schedule","landmark":"main","visible":true,"views":1,"flags":["file_pdf_not_indicated"]}
{"id":"LINK-CO-362f81eadd","type":"link","sc":"2.4.4","name":"Briarcliff Community Center home","detail":"img-alt; icon-only alt=\"Briarcliff Community Center home\"","href":"https://www.briarcliff-community.example/","context":"","landmark":"header","visible":true,"views":3,"flags":[]}
{"id":"LINK-CO-6c6213add6","type":"link","sc":"2.4.4","name":"Home","detail":"content","href":"https://www.briarcliff-community.example/","context":"","landmark":"nav[Primary]","visible":true,"views":6,"flags":[]}
{"id":"LINK-CO-7e389940fd","type":"link","sc":"2.4.4","name":"Classes","detail":"content","href":"https://www.briarcliff-community.example/classes.html","context":"","landmark":"nav[Primary]","visible":true,"views":3,"flags":[]}
{"id":"LINK-CO-aaf075f5ef","type":"link","sc":"2.4.4","name":"Instructors","detail":"content","href":"https://www.briarcliff-community.example/instructors.html","context":"","landmark":"nav[Primary]","visible":true,"views":3,"flags":[]}
{"id":"LINK-CO-b2b5d6a703","type":"link","sc":"2.4.4","name":"Contact us","detail":"content","href":"https://www.briarcliff-community.example/contact.html","context":"","landmark":"footer","visible":true,"views":3,"flags":[]}
{"id":"LINK-CO-d03461d186","type":"link","sc":"2.4.4","name":"Read more","detail":"content","href":"https://www.briarcliff-community.example/studio-expansion.html","context":"Curious what changed? Read more about the pottery studio expansion and its new kiln room, open for open-studio hours starting this month.","landmark":"main","visible":true,"views":1,"flags":["link_generic_text"]}
{"id":"IMAGE-CO-3afdf110e0","type":"image","sc":"1.1.1","name":"(alt=\"\")","detail":"img 0x0; role:decorative-declared; src sparkle.svg","href":"/icons/sparkle.svg","context":"New Studio Now Open","landmark":"main","visible":false,"views":1,"flags":[]}
{"id":"IMAGE-CO-95ed7d38dd","type":"image","sc":"1.1.1","name":"Renovated pottery studio with six new wheel stations","detail":"img 358x18; role:informative?; src studio.jpg","href":"/photos/studio.jpg","context":"New Studio Now Open New Studio Now Open Curious what changed? Read more about the pottery studio expansion and its new kiln room, open for open-studio hours starting this month.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"IMAGE-CO-9bf32183b0","type":"image","sc":"1.1.1","name":"Briarcliff Community Center home","detail":"img 242x18; role:functional; in a \"Briarcliff Community Center home\"; src logo.png","href":"/images/logo.png","context":"","landmark":"header","visible":true,"views":3,"flags":[]}
{"id":"IDENT-CO-2c687abd06","type":"ident","sc":"3.2.4","name":"\"Briarcliff Community Center home\" (3 views, header) | \"Home\" (3 views, nav[Primary])","detail":"2 names for one destination","href":"www.briarcliff-community.example","context":"","landmark":null,"visible":true,"views":3,"flags":["same_href_multiple_names"]}
```
