# Judge prompt (per batch)

You are drafting accessibility judgments for a named human ratifier on a website accessibility audit.
Read `judgment-rubric.md` in full first. Then read the batch file. Each line is one JSON unit
captured from a live page: `type` (title | heading | link | image | field | ident), `sc`, `name` (the
text or accessible name the user receives), `detail`, `href`, `context` (surrounding text block),
`landmark`, `visible`, `views` (how many pages carry this unit), and `flags` (deterministic
heuristics — evidence to weigh, not the verdict).

For every input line write exactly one output line to `<batch>.judged.jsonl` (same directory, same
basename plus `.judged`), as JSON with these keys and nothing else:

{"id","judgment":"yes|no|unsure","confidence":"high|medium|low","rationale":"≤25 words naming what the user experiences","fix":"≤20 words, empty when yes","needs_human":true|false,"drafted_by":"<your model id>"}

Rules that override everything: judge the person's experience, not the checklist; a `no` names what
the person loses; never invent what a destination page contains; when context is truncated or is a
whole navigation block, say `unsure` with `needs_human:true`; length alone is never a `no`. Do not
skip lines, do not merge lines, do not add commentary to the file. When done, report only: batch
name, lines in, lines out, and the yes/no/unsure tally.
