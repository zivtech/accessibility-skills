## Scout Recon: Login Form (Clean)

**Component type**: Form with validation (email + password + checkbox + error summary)
**APG pattern match**: WAI-ARIA Form (standard form validation pattern with error announcement)
**Complexity**: Low

**Files** (paths only):
- evals/suites/chain/targets/login-form-clean/component.jsx (main)
- evals/suites/chain/targets/login-form-clean/styles.css (styles)

**Existing ARIA inventory**:
- aria-label="Sign in" (form, line 31)
- role="alert" (error summary, line 35)
- aria-describedby="email-error" (input, line 52, conditional)
- aria-invalid (email input, line 53, conditional on submission + error state)
- aria-required="true" (email input, line 54)
- aria-describedby="password-error" (input, line 69, conditional)
- aria-invalid (password input, line 70, conditional on submission + error state)
- aria-required="true" (password input, line 71)

**Existing semantic HTML**:
- <button> elements: 1 (submit button, line 89)
- <main> landmark: yes (line 30)
- <form> element: yes, with aria-label (line 31)
- Heading hierarchy: h1 → h2 (h1 "Sign In", h2 nested in error alert, line 36)
- Form labels: all associated via htmlFor (email, password, remember me)
- <label> elements: 3 (email, password, checkbox)

**Notable patterns**:
- Client-side validation with error state tracking
- Conditional error message display tied to submitted flag
- Error summary uses role="alert" + anchor links to field errors
- Checkbox field label follows input (non-standard order but accessible)
- noValidate attribute disables browser validation (intentional)

**Flags for reviewer**:
- Error summary links anchor to input IDs but inputs use aria-describedby, not aria-label — double-linked but not redundant (anchor + error text)
- aria-required hardcoded "true" — not responsive to form state (minor, semantic attribute only)
- Checkbox has no aria-label or additional labeling — relies on visual label association (works, standard pattern)
- Missing optional form fields indicator (optional vs required distinction not communicated)
