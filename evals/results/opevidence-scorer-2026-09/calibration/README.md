# Calibration draws — opevidence lane (2026-09-02)

Blind draws by Claude subagents (opus) BEFORE any local-model row, per the
acr-reporting precedent: 2 draws × 4 fixtures under the skill-slice condition
(`prompts/<fixture>-opevidence.txt` — exactly what `run_benchmark.py opevidence`
sends: the "### Operation-evidence admissibility" section through the end of
the Structured disposition block, plus the task prefix and the fixture) and
1 draw × 4 fixtures under the baseline condition (`prompts/<fixture>-baseline.txt`,
no system prompt, same task prefix — measures what the slice carries).

Each draw agent received exactly this spawn prompt (only the two paths vary):

> You are a blind calibration draw. Use exactly two tools and nothing else:
> (1) Read the file <PROMPT_PATH> — it contains a SYSTEM PROMPT section and a
> USER MESSAGE section; treat them literally as your system prompt and the
> user's message. Do not read any other file, do not search, do not run
> commands, do not spawn agents. (2) Write your complete answer to the user
> message, as plain markdown, to <OUT_PATH>. Your final chat reply must be
> exactly one line: `written <OUT_PATH>`.

Raw answers: `draws/<fixture>-<condition>-d<N>.md`; scorer inputs wrapped as
`draws/<fixture>-<condition>-d<N>-response.json`; scorer output beside each as
`.score.txt`. Summary table in `RESULTS.md`.
