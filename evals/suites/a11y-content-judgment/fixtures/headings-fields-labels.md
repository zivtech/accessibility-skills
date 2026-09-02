# Input: content-judgment batch — headings-fields-labels

Northbridge Water Quality Lab runs an internal portal where certified lab technicians submit water samples for analysis and read back the resulting reports. The audience is specialist staff already trained on the lab's internal shorthand, including "TCLI" (Turbidity-Chlorine Load Index), the lab's own composite reading of turbidity and residual chlorine levels. Two pages were captured: the sample submission form and a report page.

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
{"id":"TITLE-WA-2aefe37679","type":"title","sc":"2.4.2","name":"Northbridge Water Quality Lab — Sample Submission","detail":"h1: Submit a sample","href":"https://www.northbridge-waterlab.example/intake.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"TITLE-WA-85b3d95b62","type":"title","sc":"2.4.2","name":"Northbridge Water Quality Lab — Reports","detail":"h1: Sample report NB-3391","href":"https://www.northbridge-waterlab.example/reports.html","context":"","landmark":null,"visible":true,"views":1,"flags":[]}
{"id":"HEADING-WA-001086e629","type":"heading","sc":"2.4.6","name":"Compliance and Reporting Obligations Under the Regional Watershed Monitoring Agreement","detail":"h2","href":null,"context":"This section summarizes the lab's ongoing obligations to the regional watershed authority under the current multi-year monitoring agreement.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-WA-29d24d1db5","type":"heading","sc":"2.4.6","name":"Details","detail":"h2","href":null,"context":"The intake line near the north reservoir showed a two-hour window of elevated sediment following Tuesday's rainfall.","landmark":"main","visible":true,"views":1,"flags":["heading_generic"]}
{"id":"HEADING-WA-55e1c33b47","type":"heading","sc":"2.4.6","name":"Sample report NB-3391","detail":"h1","href":null,"context":"Overview Turbidity readings held steady this week while residual chlorine dipped slightly below the usual weekday range.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-WA-a6eba7ca21","type":"heading","sc":"2.4.6","name":"Look up a past submission","detail":"h2","href":null,"context":"Search","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-WA-aa218aa0e0","type":"heading","sc":"2.4.6","name":"Submit a sample","detail":"h1","href":null,"context":"Complete the form below for each sample collected during today's rounds. Submissions are reviewed within one business day.","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"HEADING-WA-bc179b1620","type":"heading","sc":"2.4.6","name":"24.3","detail":"h2","href":null,"context":"Any reading outside the posted range should be flagged to the shift lead before the sample is logged as complete.","landmark":"main","visible":true,"views":1,"flags":["heading_numeric_only"]}
{"id":"HEADING-WA-c67484fbba","type":"heading","sc":"2.4.6","name":"","detail":"h2","href":null,"context":"Full trend charts for the quarter are attached as a separate download for technicians who want the underlying readings.","landmark":"main","visible":false,"views":1,"flags":["heading_empty","name_from_none"]}
{"id":"HEADING-WA-e180f996ca","type":"heading","sc":"2.4.6","name":"Overview","detail":"h2","href":null,"context":"Turbidity readings held steady this week while residual chlorine dipped slightly below the usual weekday range.","landmark":"main","visible":true,"views":1,"flags":["heading_generic"]}
{"id":"FIELD-WA-452339d1be","type":"field","sc":"2.4.6","name":"Collection date","detail":"date; label from label[for]","href":null,"context":"","landmark":"form","visible":true,"views":1,"flags":[]}
{"id":"FIELD-WA-7e6f8a75d0","type":"field","sc":"2.4.6","name":"TCLI","detail":"number; label from label[for]","href":null,"context":"","landmark":"form","visible":true,"views":1,"flags":[]}
{"id":"FIELD-WA-851a4e854b","type":"field","sc":"2.4.6","name":"(no label; placeholder-only)","detail":"text; label from placeholder-only; placeholder \"Enter sample ID\"","href":null,"context":"","landmark":"form","visible":true,"views":1,"flags":["field_unlabeled_placeholder-only"]}
{"id":"FIELD-WA-ae1a2e68cc","type":"field","sc":"2.4.6","name":"Field notes","detail":"textarea; label from label[for]","href":null,"context":"","landmark":"form","visible":true,"views":1,"flags":[]}
{"id":"FIELD-WA-c7f6cc14da","type":"field","sc":"2.4.6","name":"Search past submissions","detail":"search; label from aria-label","href":null,"context":"","landmark":"main","visible":true,"views":1,"flags":[]}
{"id":"LINK-WA-04b70e124f","type":"link","sc":"2.4.4","name":"Contact","detail":"content","href":"https://www.northbridge-waterlab.example/contact.html","context":"","landmark":"footer","visible":true,"views":2,"flags":[]}
{"id":"LINK-WA-bd8454d80f","type":"link","sc":"2.4.4","name":"Submit a Sample","detail":"content","href":"https://www.northbridge-waterlab.example/intake.html","context":"","landmark":"nav","visible":true,"views":2,"flags":[]}
{"id":"LINK-WA-fc188a29f8","type":"link","sc":"2.4.4","name":"Northbridge Water Quality Lab","detail":"content","href":"https://www.northbridge-waterlab.example/","context":"","landmark":"header","visible":true,"views":2,"flags":[]}
{"id":"LINK-WA-fd0eb2e84f","type":"link","sc":"2.4.4","name":"Reports","detail":"content","href":"https://www.northbridge-waterlab.example/reports.html","context":"","landmark":"nav","visible":true,"views":2,"flags":[]}
```
