# Drupal Accessibility Patch Evaluation Packet

> One patch, one accessibility issue pattern. This packet evaluates an **upstream core MR** (not a local patch file), so patch-hygiene applies to the MR checkout and the "site" evidence lane is replaced by provider-endpoint evidence plus render-path code verification. Deviations from the standard lanes are stated inline.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-CORE-3613614-oembed-language-params` |
| Source status | Core MR "Needs review" (issue #3613614, MR !16491) |
| Local status | `INCONCLUSIVE` — mechanism evidence is decisive against the MR, but no live multilingual before/after run exists, so `FAILED` is not claimable under the outcome definitions |
| Manual status | `debt_explicit` |
| Owner / run ID | Main / `2026-08-06-main` |
| Report path | `docs/drupal-patch-evaluations/reports/current-wave/2026-08-06-3613614-critic-gate.md` |
| Project/package | `project/drupal` (drupalcode.org), branch `3613614-oembed-iframe-pass` |
| Target commit | MR head `f1aac5c73c2296508fea10552cd4a14e70e00d7f`; merge base with `origin/main` `73847ce09f3543e4bbe8c251eafd22687cd53fd4` |
| Patch file | n/a — MR checkout at `/Users/AlexUA_1/claude/drupal-core-git/.worktrees/3613614-oembed-lang-20260806` (machine-local; do not copy into upstream content) |
| Evaluation date | 2026-08-06 |
| Evaluator | Claude Code (Fable 5) session operated by Alex Urevick-Ackelsberg |
| AI assistance disclosed? | yes |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | Belgian federal accessibility audit finding, filed as core issue #3613614 |
| Tool version | curl 8.x (macOS), PHPUnit via core `phpunit.xml.dist`, PHP 8.5.8 |
| WCAG SC | 3.1.2 Language of Parts (AA) — embedded player UI language; the MR's wrapper `lang` change maps to 3.1.1 (scope of issue #3593533) |
| Impact | serious (screen reader users receive player controls in the wrong language) |
| User groups affected | screen reader users, cognitive accessibility, all multilingual-site users |
| Route(s) | `media.oembed_iframe` (`/media/oembed?url=...`), any page rendering an oEmbed field |
| Selector(s) | provider `<iframe>` inside the oEmbed wrapper document |
| Pattern ID(s) | n/a (behavioral/language, not an axe rule) |
| Theme/profile/modules | media (core), any theme |
| Auth/content state | anonymous, published media |
| Viewport(s) | n/a |
| Color mode / forced colors / direction | n/a |

## What the MR changes

1. `MediaHooks::oembedResourceUrlAlter()` — new `hook_oembed_resource_url_alter()` implementation appending `hl=<langcode>` (provider "YouTube") / `locale=<langcode>` (provider "Vimeo") to the **oEmbed API request URL** built by `UrlResolver::getResourceUrl()`. Language source: `getCurrentLanguage()` → `TYPE_INTERFACE`.
2. `UrlResolver::getResourceUrl()` — langcode added to static and persistent cache keys.
3. `MediaThemeHooks::preprocessMediaOembedIframe()` + `media-oembed-iframe.html.twig` — `lang="{{ langcode }}"` on the wrapper `<html>`. Language source: `TYPE_CONTENT`.
4. Unrelated: full DI conversion of `MediaHooks` (7 injected services, ~10 call-site rewrites).

## Baseline Evidence

Standard lane (live site, unpatched, violation observed) **was not run** — no current-base multilingual runtime was available this session. Substituted baseline: core at the merge base passes no language parameter of any kind to providers (`UrlResolver::getResourceUrl()` sends only `url`, `maxwidth`, `maxheight`), so the player loads with the provider's own default language behavior regardless of page language. This is a code-verified baseline, not a scanned one; it is the reason Local status cannot exceed `INCONCLUSIVE`.

### Baseline Acceptance Gate

- [ ] The target violation was observed live before applying the patch. *(not run — explicit gap)*
- [x] The mechanism producing the violation is identified in source at the merge base.
- [x] WCAG/rule mapping matches the issue summary.

## Patch Hygiene

- MR head checked out cleanly in a dedicated worktree branched for this evaluation; `composer install` exit 0.
- Unit tests: `vendor/bin/phpunit -c core core/modules/media/tests/src/Unit/UrlResolverTest.php` → **OK (2 tests, 2 assertions)**.
- Functional tests: `SIMPLETEST_BASE_URL=http://127.0.0.1:8988 SIMPLETEST_DB=sqlite://localhost/sites/default/files/eval.sqlite vendor/bin/phpunit -c core core/modules/media/tests/src/Functional/UrlResolverTest.php` → **OK (10 tests, 72 assertions)**. Matches the CI-green claim in issue comment #9.

## Verification Evidence (provider-endpoint lane)

The render-path chain, verified by reading MR-head source:

- `OEmbedFormatter::viewElements()` renders an iframe whose `src` is Drupal's own `media.oembed_iframe` route.
- `OEmbedIframeController::render()` fetches the oEmbed resource server-side and renders `'#media' => IFrameMarkup::create($resource->getHtml())` — the visitor's player iframe is **the provider's `html` field from the oEmbed API response, verbatim**.
- Therefore the MR can only change the player if the provider's `html` field changes when the language parameter is added to the API request.

Empirical result (2026-08-06, unauthenticated curl, US network):

| Test | Result |
|---|---|
| YouTube oEmbed with vs without `hl=fr` (video `dQw4w9WgXcQ`) | **Byte-identical JSON** (diff of pretty-printed responses); also tested `hl=pt-br`, `pt-BR`, `zh-hans` |
| Embed src inside YouTube `html` field | `https://www.youtube.com/embed/dQw4w9WgXcQ?feature=oembed` — no language param, all cases |
| Vimeo oEmbed with vs without `locale=fr` / `locale=de` (live video `347119375`) | **Byte-identical JSON**; `locale` is not in Vimeo's oEmbed argument table (developer.vimeo.com/api/oembed/videos), so it is dropped |
| Vimeo oEmbed with **recognized** params `texttrack=fr` / `audiotrack=fr` / `cc=false` | **Pass through into the embed src** (`&texttrack=fr`, `&audiotrack=fr`, `cc=0`) — Vimeo's oEmbed is parameter-transparent for documented player params; the MR's mechanism works there, it just used a nonexistent param |
| Vimeo player UI language probes (`?locale/lang/language/hl/texttrack=fr` on `player.vimeo.com/video/...`) | All ignored — player document stays `lang="en"`, config `"lang":"en"` |
| Vimeo player with `Accept-Language: fr-FR` request header | Player config flips to `"lang":"fr-FR"` — empirical confirmation that UI language follows the viewer's browser, which server-side Drupal cannot set |
| Control — `hl` on the **embed URL** `youtube.com/embed/dQw4w9WgXcQ?hl=fr` | Player document `<html lang="fr"` (vs `lang="en"` without); `?hl=pt-br` → `lang="pt"` |

**Conclusion**: the MR's parameter is ignored where it is sent and absent where it would work. With the MR applied, the embed HTML Drupal renders is unchanged for both targeted providers; the SC 3.1.2 player-language goal is not achieved. Observable MR effects reduce to (a) the wrapper `lang` attribute (issue #3593533's scope — real but out of scope here), (b) per-language cache fragmentation, (c) an inert query parameter on server-side API requests.

Raw artifacts: `yt-nohl.json`, `yt-hlfr.json`, `vim-noloc.json`, `vim-locfr.json`, `vim-locde.json` (session scratchpad; copy under `reports/` if this packet advances).

## Secondary findings (code review)

| # | Severity | Finding |
|---|---|---|
| F3 | MAJOR | Language-type inconsistency: alter hook + cache key use `TYPE_INTERFACE`; template preprocess uses `TYPE_CONTENT`. Wrapper and player can disagree where interface ≠ content language. Content language is correct for SC 3.1.2. |
| F4 | MAJOR | `OEmbedIframeController` response cacheability is `['url.site','url']` only; output is now language-dependent. Non-URL language negotiation (session/cookie/user/browser) gets no Dynamic Page Cache separation → cross-language cache bleed served to the wrong users. `dynamic_page_cache` + `page_cache` ship enabled in the standard profile, so exposure is default-config. This is a regression the MR introduces: pre-patch output was language-invariant. |
| F5 | normal | Raw Drupal langcodes (`pt-br`, `zh-hans`) passed as provider params without BCP-47 mapping; `und`/`zxx` not skipped; `empty($langcode)` guard is dead code. |
| F6 | normal | Scope: (a) unrelated `MediaHooks` DI conversion (7 services, 8 unrelated methods) inflates the diff — the MR's only test churn (the `LanguageManagerInterface` stub in Unit/UrlResolverTest) is caused by `UrlResolver`'s own in-scope constructor change, not by this refactor; (b) wrapper `lang` duplicates #3593533, which this issue's summary explicitly scopes out. |
| F7 | MAJOR | Tests assert the parameter is appended to the API request URL — they cannot detect that providers ignore it. If `$langcode = 'en'` were hardcoded, every test in the file would still pass. `testCacheKeyIncludesLanguage()` never switches language (duplicate assertion, name overpromises); no non-English language installed in any test; `/hl=[a-z]{2}/` and `/locale=[a-z]{2}/` are both unanchored. |
| F8 | minor | Static cache key still omits max dimensions (pre-existing); cache fragmentation hits all providers though only two get params; CR node/3614470 documents only the template `lang` attribute and is silent on the `UrlResolver` constructor change. |
| F9 | closed | Wrapper-`lang` end-to-end behavior was unverified by any executed test (all 10 functional tests target query-string building). Closed 2026-08-06: evaluation-only assertion `assertStringContainsString('<html lang="en">', $content)` added to kernel test `OEmbedIframeControllerTest::testResourcePassedToPreprocess()` (renders the real controller/preprocess/template) passes on MR head — OK (1 test, 15 assertions). Merge-base template renders plain `<html>`. Instrumentation: `patches/a11y-CORE-3613614-eval-instrumentation-wrapper-lang-assertion.patch`; worktree restored to exact MR head after the run. |
| F10 | MAJOR (context) | Any embed-src rewrite direction touches code with an active security history: SA-CORE-2022-015 (XSS in `OEmbedIframeController` iframe-domain handling, CVE-2022-25276) and SA-CORE-2026-008 (SSRF in `UrlResolver::discoverResourceUrl()`, 2026-06-17; mitigation `media_oembed_discovery_trusted_host_patterns` verified present at MR head). Expect strong security-team scrutiny of any provider-HTML rewriting; both SA numbers verified against drupal.org. |
| F11 | debt | The iframe `title` attribute (untranslated video title — identical across all langcodes in the JSON diffs) lives in Drupal's wrapper document; an unconditional content-language `lang` may mislabel that English title text — a narrow potential 3.1.2 mismatch of its own. Needs real AT verification. |

## Manual and Perspective Verification

| Check | Status | Notes |
|---|---|---|
| Live multilingual before/after (player UI language) | `not run` | Requires current-base multilingual runtime; decisive only if provider behavior changes, which endpoint evidence already excludes |
| NVDA/VoiceOver on embedded player | `not run` | Debt — explicitly out of this packet's claims |
| `zh-hans` on YouTube **embed** URL | `not run` | Only tested against the API endpoint (which ignores all params) |
| Wrapper `<html lang>` renders end-to-end | `complete` | F9 closure: kernel render via `OEmbedIframeControllerTest::testResourcePassedToPreprocess()` + evaluation-only assertion — `<html lang="en">` present on MR head; merge-base template renders plain `<html>` |
| AT handling of English iframe `title` inside `lang`-tagged wrapper (F11) | `not run` | New debt from critic gate — real AT check needed, code reading insufficient |

Manual status: `debt_explicit`.

## Critic Gate

- a11y-critic review: **complete** — `reports/current-wave/2026-08-06-3613614-critic-gate.md`. All load-bearing findings CONFIRMED (F1 independently re-verified and extended with more langcodes plus realistic request headers — still byte-identical). Corrections applied: one wrong F6a sub-clause removed (DI refactor did not cause the test churn); F3/F4/F7 elevated to MAJOR; F2 security caution strengthened with verified advisories (F10); F6b "works today" overclaim resolved by executing the wrapper render (F9); iframe-`title` nuance recorded (F11).
- perspective-audit: not escalated (patch does not change any working AT behavior; the finding is that it changes nothing user-facing except the wrapper attribute).

## Recommended upstream position (critic-gated)

Do not merge as-is. Share on the issue (operator rewrites per `core/AGENTS.md` before posting):
1. Provider-endpoint evidence that the API-request parameter is inert for both targeted providers (repro commands included).
2. Working mechanism for YouTube: `hl` on the embed iframe `src` inside the resource HTML (documented IFrame player parameter; empirically switches player document language). Rewriting provider HTML must reckon with SA-CORE-2022-015 and SA-CORE-2026-008 in this exact code path — expect security-team pushback, possibly rejection.
3. Vimeo: player UI language is browser-detected only (documented + empirically confirmed via Accept-Language); no server-side lever exists for the SC 3.1.2 chrome-language goal. However, Vimeo's oEmbed passes documented player params through to the embed src — `texttrack`/`audiotrack` (caption and audio language) would work via this MR's exact alter-hook mechanism as a separate content-language enhancement.
4. Move the wrapper `lang` change to #3593533; drop the unrelated DI refactor; fix language-type consistency (F3), cache context (F4), langcode mapping (F5), and test coverage (F7) in whichever direction survives.

## Negative space — what this packet does NOT claim

- Not adjudicating whether third-party player chrome is a host-page conformance failure under WCAG 3.1.2; the audit finding is taken as given.
- Provider behavior tested unauthenticated from one US network on one date; regional/authenticated variation is very unlikely given byte-identical responses across four langcodes, but not excluded.
- No claim of full human AT verification anywhere in this packet.
- The `FAILED` outcome is *recommended by the evidence* but not *set*: the skill's outcome definitions require a live reproduced baseline before `FAILED`, and that lane was not run.
