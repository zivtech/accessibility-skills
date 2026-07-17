# Input: manual screen reader testing note

Convert this manual testing note into an accessibility bug report ready to
file as a GitHub Issue, following the bug-reporting skill.

---

Tested the donation form at https://give.example.org/donate today with
VoiceOver on macOS 14 (Safari 17.4).

If you submit the form with the amount field empty, an error message appears
visually in red above the form — but VoiceOver announced nothing at all when
it appeared. I only found the error because I happened to navigate back to the
top of the form. Sighted users see it immediately; a blind user gets silence
and a form that just didn't submit.

Looking at the page source afterwards, the error markup seems to be a plain
`<div class="form-error">Please enter a donation amount.</div>` that gets
inserted into the page when validation fails. The amount field itself is
`<input id="donation-amount" type="text">` and doesn't visually change or get
any error styling.

No automated scan was run — found this by hand during the monthly giving
campaign QA pass.
