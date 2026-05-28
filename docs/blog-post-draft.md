# We Built an Accessibility Reviewer That Has to Pass Its Own Test

I've been building AI agent skills for about six months now — Markdown protocols that teach models how to do specific jobs. The latest one is an accessibility skill bundle, and it forced me to answer a question I wasn't expecting: how do you know the reviewer is any good?

## The bundle

[a11y-meta-skills](https://github.com/zivtech/a11y-meta-skills) is four skills that cover the full accessibility development lifecycle:

- **a11y-planner** designs accessible implementations before you write code — semantic structure, ARIA patterns, keyboard behavior, focus management
- **a11y-critic** reviews what you built after testing, looking for design-level gaps that automated tools miss
- **a11y-test** runs real Playwright keyboard tests and axe-core scans
- **perspective-audit** reviews from 7 actual disability perspectives — screen reader users, keyboard-only users, low vision, cognitive, vestibular, auditory, and environmental contrast

That last one is the one I'm most proud of. Most accessibility tools check attributes. This one asks: what would a screen reader user actually experience? What about someone with a vestibular disorder watching your page transition animations?

```bash
npx skills add zivtech/a11y-meta-skills
```

## But does it work?

Here's where it gets interesting. I built 83 graded evaluation fixtures — React components with intentional accessibility patterns (some correct, some broken, some deliberately ambiguous). Every fixture has a rubric that defines what a competent reviewer should find.

Then I ran hosted and local AI models against them, including Claude, Codex/OpenAI, and Ollama local models, with the benchmark structure ready to track Gemini and other hosted baselines as peer rows.

The fixtures come in four difficulty tiers:
- **CLEAN** — no bugs, tests false positive resistance
- **HAS-BUGS** — clear accessibility violations
- **FLAWED** — subtle, incomplete patterns
- **ADVERSARIAL** — genuinely ambiguous tradeoffs where reasonable reviewers disagree

## What I found

The headline: **the cheapest Claude model catches every real accessibility bug.** Haiku 4.5 — the $0.25/million-token model — detected 100% of must-find items across all 21 HAS-BUGS fixtures and all 5 FLAWED fixtures.

Where it fails is more interesting than where it succeeds. Haiku's 5 failures (out of 33 fixtures) were all judgment calls:
- 1 false positive on clean code (flagged a well-built component as having issues)
- 1 WARN on a tricky clean fixture
- 3 adversarial fixtures where it found the right tradeoffs but gave the wrong verdict

Detection is solved. Judgment isn't. That's a meaningful distinction — it means you can trust the cheap model to find real problems, and only escalate to a more expensive model when you need nuanced assessment of ambiguous patterns.

The escalation strategy costs $0.65 total for 33 components. Start at Haiku, promote failures to Sonnet, promote the remaining failure to Sonnet with thinking enabled. 100% pass rate.

## You don't even need a cloud API

The local model story is just as good. qwen3:32b (an 18.8 GB model running on Ollama, on my laptop) passed 100% of all 33 fixtures with 96% must-find detection. No API key, no cloud dependency, no per-token cost.

The one thing several local models consistently miss? `role="alert"` on toast notifications — qwen3:32b, llama3.3:70b, and qwen3.5:latest score 3/4 on that fixture instead of 4/4. Claude, GPT-5.2, and qwen3.5:27b get it. It's a real detection gap, not a rubric issue. But it's one item out of 83 fixtures.

## The meta part

Here's where this gets recursive. The benchmark dashboard I built to present these results? It had to be accessible. You can't promote an accessibility skill suite with charts that a screen reader can't read.

Every chart has a data table fallback. Every visualization uses redundant encoding (not just color). Every interactive element is keyboard-navigable. The page respects `prefers-reduced-motion`.

It's accessibility skills all the way down.

## Try it

```bash
npx skills add zivtech/a11y-meta-skills
```

The full benchmark data, eval fixtures, and scoring scripts are all in the repo. If you want to test your own model against the fixtures, there's a runner for that too.

If you're using agentic coding tools and care about accessibility — or if you just want to see what a rigorous AI skill eval suite looks like — [take a look](https://github.com/zivtech/a11y-meta-skills).
