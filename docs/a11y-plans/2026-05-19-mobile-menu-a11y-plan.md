# MobileMenu Accessibility Design Plan

> **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
> **Compliance target:** WCAG 2.2 AA
> **Users who need accessibility:** Screen reader, keyboard-only, low vision, cognitive, voice control, switch access
> **Assistive technologies:** NVDA, JAWS, VoiceOver (macOS/iOS), keyboard-only, screen magnifiers, high contrast mode

**Feature:** Mobile navigation toolbar and bookmark dialog for the client digital law library book reader
**Risk Level:** High (dialog with focus trap, dynamic state changes, anonymous/authenticated split, multi-widget toolbar)
**Component Type:** Navigation toolbar (Disclosure + Toggle Buttons + Modal Dialog)

---

## Scope & Context

### What is being built?
Accessibility remediation of the existing `MobileMenu` component -- a mobile navigation toolbar that provides book navigation (Chapters, Appendices, Index), bookmarking with collection management, fullscreen toggle, print/download, share-by-email, and a "what's new" content highlight toggle.

### What user need does it address?
Legal professionals and researchers use the client's digital library to read consumer law treatises. The mobile menu is the primary navigation and utility toolbar on mobile viewports. Every feature behind these buttons -- bookmarking, chapter navigation, printing -- must be operable by keyboard-only and assistive technology users.

### Who needs accessibility?
All users. Specific access concerns:
- **Screen reader users**: No `<nav>` landmark, dialog labeling is redundant, no live regions for state changes, anonymous share-by-email is a non-interactive span that looks like a button
- **Keyboard-only users**: Menu close does not restore focus to toggle, no `aria-controls` relationship on menu toggle, focus trap in dialog has edge cases
- **Low vision users**: Touch targets on toolbar icons, focus indicator visibility, reflow at mobile zoom levels
- **Cognitive users**: Error messages for anonymous users are vague, "what's new" toggle purpose unclear, collection input lacks instructions

### Compliance target
WCAG 2.2 AA (project standard per existing client contract)

### Existing code
- Primary: `<client-repo>/drupal/react-app/src/components/navigation/MobileMenu.js` (497 lines)
- Child: `<client-repo>/drupal/react-app/src/components/navigation/mobileMenuMainLink.js` (53 lines)
- Related: `chapterMenuNvigation.js`, `indexMenu.js`, `rightSidebar.js`

### Open Product Decisions (resolve before implementation)

1. **Anonymous "Share by email" treatment**: Currently renders as a non-interactive `<span>` (MobileMenu.js:293) -- a WCAG failure. Two options:
   - **Option A (recommended)**: Render a real `<button aria-disabled="true">` with a login hint, keeping the feature discoverable for anonymous users.
   - **Option B**: Do not render the share button for anonymous users at all.
   - **Not acceptable**: Preserving the current `<span>` that looks like a button but has no role, state, or keyboard operability.
   - This decision affects Task 9.

2. **"What's new" toggle label**: Current label "See what's new" is vague. The toggle sets `book.whatNew` in context, but what that flag does downstream (highlight new sections? filter to new content?) is not visible from this file. Task 7 proposes "Highlight updated content" as a replacement, but **the correct label must be verified with the product team** based on the feature's actual behavior. The plan cannot determine the right label from source code alone.

### Constraints
- React 16+ (existing project)
- Drupal backend provides content and CSRF tokens
- Third-party MUI Dialog can appear on top of bookmark dialog (lines 88, 96 guard against this)
- Mobile viewport is the primary context; these controls are hidden on desktop (desktop has a separate `controls.js`)

---

## Semantic Structure Plan

### Current problems
1. **No `<nav>` landmark**: Entire component is `<div className="bookreader-mobile-mobile-nav">` (MobileMenu.js:175). Screen reader users cannot locate the navigation via landmark shortcuts. WCAG 1.3.1 Info and Relationships.
2. **Heading hierarchy broken in dialog**: `<h4>Create a bookmark</h4>` (MobileMenu.js:343) appears with no h1/h2/h3 above it in the dialog context. Within a dialog, headings should start at h2 (the dialog establishes its own outline). WCAG 1.3.1.
3. **Menu list not labeled**: `<ul className="bookreader-mobile-nav">` (MobileMenu.js:480) has no accessible label or relationship to the toggle button. WCAG 1.3.1.

### Planned structure

```
<nav aria-label="Book tools and navigation">
  <!-- Toolbar: menu toggle, what's new, bookmark, print, share, fullscreen -->
  <button aria-expanded aria-controls="mobile-nav-list">  <!-- Menu toggle -->
  <button aria-pressed>                                     <!-- What's new toggle -->
  <button aria-haspopup="dialog" aria-disabled?>            <!-- Bookmark trigger -->
  <button>                                                  <!-- Print/download -->
  <button aria-haspopup="dialog" disabled?>                 <!-- Share by email -->
  <button aria-pressed>                                     <!-- Fullscreen toggle -->

  <!-- Navigation drawer -->
  <ul id="mobile-nav-list">
    <li>
      <button aria-expanded aria-controls="chapters-panel">Chapters</button>
      <div id="chapters-panel">...</div>
    </li>
    <li>
      <button aria-expanded aria-controls="appendices-panel">Appendices</button>
      <div id="appendices-panel">...</div>
    </li>
    <li>
      <button aria-expanded aria-controls="index-panel">Index</button>
      <div id="index-panel">...</div>
    </li>
    <!-- RightSidebar content -->
  </ul>

  <!-- Bookmark dialog (conditional render) -->
  <div role="dialog" aria-labelledby="bookmark-dialog-title-mobile"
       aria-describedby="bookmark-dialog-desc-mobile" aria-modal="true">
    <h2 id="bookmark-dialog-title-mobile">Create a bookmark</h2>
    <p id="bookmark-dialog-desc-mobile">Add bookmark to existing collection...</p>
    ...
  </div>
</nav>
```

### Landmark regions
| Region | Element | Label | WCAG |
|--------|---------|-------|------|
| Navigation | `<nav>` | `aria-label="Book tools and navigation"` | 1.3.1, 2.4.1 |

### Heading hierarchy within dialog
| Level | Content | WCAG |
|-------|---------|------|
| h2 | "Create a bookmark" (promoted from current h4) | 1.3.1 |

### Form structure within dialog
| Element | Label | Association | WCAG |
|---------|-------|-------------|------|
| Text input `#new-collection-input-mobile` | "Or create a new collection:" | `<label htmlFor>` (exists at MobileMenu.js:394) | 1.3.1, 3.3.2 |
| Collection buttons group | "Add bookmark to:" | `role="group" aria-labelledby` (exists at MobileMenu.js:350) | 1.3.1 |

---

## Interaction Pattern Design

**Critical clarification**: None of these widgets are WAI-ARIA Menu Buttons. A Menu Button opens a `role="menu"` with `menuitem` children navigated by arrow keys. This component uses Disclosure (show/hide panel), Toggle Buttons, and a Modal Dialog. Using the wrong APG pattern would create incorrect keyboard expectations.

### Widget 1: Menu Toggle (Book navigation disclosure)

**APG Pattern**: Disclosure (Show/Hide) -- https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

**Current state** (MobileMenu.js:176-181): Has `aria-expanded` and `aria-label`. Missing `aria-controls` reference to the controlled panel.

**Planned ARIA attributes:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-expanded` | `true`/`false` | Toggle button | 4.1.2 Name, Role, Value |
| `aria-controls` | `"mobile-nav-list"` | Toggle button | 1.3.1 Info and Relationships |
| `aria-label` | `"Book navigation menu"` | Toggle button | 4.1.2 Name, Role, Value |
| `id` | `"mobile-nav-list"` | `<ul>` nav list | 1.3.1 Info and Relationships |

**Keyboard interactions:**
| Key | Behavior | WCAG |
|-----|----------|------|
| Tab | Focuses toggle button in natural tab order | 2.1.1 Keyboard |
| Enter/Space | Toggles `aria-expanded`, shows/hides nav list | 2.1.1 Keyboard |

**Screen reader experience:**
- On focus: "Book navigation menu, button, collapsed" (or "expanded")
- On activation: State change announced ("expanded"/"collapsed")

### Widget 2: Chapter/Appendix/Index Section Toggles

**APG Pattern**: Disclosure (Show/Hide) -- https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

**Current state** (mobileMenuMainLink.js:29-47): Has `aria-expanded`. Missing `aria-controls`.

**Planned ARIA attributes:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-expanded` | `true`/`false` | Section toggle button | 4.1.2 Name, Role, Value |
| `aria-controls` | `"{key}-panel"` (dynamic) | Section toggle button | 1.3.1 Info and Relationships |
| `id` | `"{key}-panel"` | Content panel `<div>` | 1.3.1 Info and Relationships |

**Keyboard interactions:**
| Key | Behavior | WCAG |
|-----|----------|------|
| Tab | Focuses button in natural tab order within the nav list | 2.1.1 |
| Enter/Space | Toggles section open/closed; closes other open section | 2.1.1 |

**Screen reader experience:**
- On focus: "Chapters, button, expanded" (or "collapsed")
- On activation: State change announced; focus moves to first interactive element in opened panel (existing behavior at chapterMenuNvigation.js:72-78)

### Widget 3: "What's New" Toggle

**APG Pattern**: Toggle Button -- https://www.w3.org/WAI/ARIA/apg/patterns/button/

**Current state** (MobileMenu.js:197-213): Has `aria-pressed` and `aria-label="See what's new"`. Also has a `<span className="visually-hidden">see what's new</span>` which is dead weight because `aria-label` overrides it.

**Issues to fix:**
1. Remove the redundant `<span className="visually-hidden">see what's new</span>` (MobileMenu.js:212). When `aria-label` is present, it overrides all descendant text content per the accessible name computation algorithm. The span contributes nothing and creates maintenance confusion.
2. Clarify the label. "See what's new" does not describe what the toggle does. The button highlights updated content within the book. Better: `aria-label="Highlight updated content"`.

**Planned ARIA attributes:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-pressed` | `true`/`false` | Toggle button | 4.1.2 Name, Role, Value |
| `aria-label` | `"Highlight updated content"` | Toggle button | 4.1.2 Name, Role, Value |

**Keyboard interactions:**
| Key | Behavior | WCAG |
|-----|----------|------|
| Tab | Focuses button | 2.1.1 |
| Enter/Space | Toggles `aria-pressed` | 2.1.1 |

**Screen reader experience:**
- On focus: "Highlight updated content, toggle button, not pressed" (or "pressed")
- On activation: "pressed"/"not pressed" state change announced

### Widget 4: Bookmark Trigger Button

**APG Pattern**: Button (activates dialog) -- https://www.w3.org/WAI/ARIA/apg/patterns/button/ + https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

**Current state** (MobileMenu.js:214-239): Has `aria-label`, `aria-haspopup="dialog"`, `aria-disabled` (conditional). Two problems:

1. **`aria-disabled="true"` but onClick still fires** (MobileMenu.js:221-227): When anonymous, the button has `aria-disabled="true"` but the click handler still runs and calls `setError(...)`. Screen reader users will hear "Bookmark this page, button, dimmed" and if they activate it, an error appears -- but they may not know it appeared because there is no live region. Decision required: either prevent click entirely when `aria-disabled="true"`, or keep the handler but ensure the error message reaches a `role="alert"` region.

2. The `aria-disabled` value falls through to `undefined` for logged-in users (MobileMenu.js:220: `aria-disabled={!get(user, 'id') ? 'true' : undefined}`). This is correct React behavior -- `undefined` removes the attribute.

**Recommended approach**: Keep `aria-disabled="true"` on the button for anonymous users (so it remains discoverable, unlike `disabled` which removes it from tab order). Prevent the default click handler from running when aria-disabled. Instead, show a tooltip or status message via a live region: "Log in to bookmark pages." This communicates the feature's existence and what's needed to use it. WCAG 4.1.2 + 3.3.2 Labels or Instructions.

**Planned ARIA attributes:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-label` | `"Bookmark this page"` | Button | 4.1.2 |
| `aria-haspopup` | `"dialog"` | Button | 4.1.2 |
| `aria-disabled` | `"true"` (anonymous only) | Button | 4.1.2 |
| `aria-describedby` | `"bookmark-login-hint"` (anonymous only, points to hidden hint text) | Button | 1.3.1, 3.3.2 |

**Keyboard interactions:**
| Key | Behavior | WCAG |
|-----|----------|------|
| Tab | Focuses button | 2.1.1 |
| Enter/Space | Opens bookmark dialog (logged in) or announces "Log in to bookmark pages" in status region (anonymous) | 2.1.1 |

### Widget 5: Bookmark Dialog

**APG Pattern**: Modal Dialog -- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

**Current state** (MobileMenu.js:333-478): Has `role="dialog"`, `aria-label="Create a bookmark"`, `aria-modal="true"`, `tabIndex="-1"`. Focus trap implemented (lines 94-110). Focus on open goes to close button (lines 117-120). Focus restoration to trigger button on close (line 63).

**Issues to fix:**

1. **Redundant labeling** (MobileMenu.js:333 + 343): `aria-label="Create a bookmark"` and `<h4>Create a bookmark</h4>` -- screen readers will announce the aria-label, ignoring the heading content. Replace `aria-label` with `aria-labelledby` pointing to the heading's id. This is the APG-recommended approach for dialogs with visible headings.

2. **Heading level** (MobileMenu.js:343): `<h4>` should be `<h2>`. Within a dialog's own outline, h2 is the correct starting level. There are no h1/h2/h3 ancestors within this dialog. WCAG 1.3.1.

3. **Missing `aria-describedby`** (MobileMenu.js:346): The descriptive paragraph "Add bookmark to existing collection or simply create a new collection by giving it a name" should be referenced by `aria-describedby` on the dialog so screen readers announce the instructions when the dialog receives focus.

4. **Focus trap edge case** (MobileMenu.js:97-100): The focusable element query correctly handles an empty result (`if (focusable.length === 0) return`), but returning without preventing default means Tab will escape the dialog to browser chrome. When no focusable elements exist, `e.preventDefault()` should fire to maintain the trap. In practice this is unlikely (close button always exists), but defensive coding is warranted.

5. **`<title>` inside SVG in collection checkboxes** (MobileMenu.js:385): The checkmark SVG has `<title />` (empty title tag). This should be removed -- empty titles create empty accessible names. The SVG already has `aria-hidden="true"`, but the `<title>` is noise in the source.

6. **The "x" close button text** (MobileMenu.js:341): `<span aria-hidden="true">&times;</span>` is correctly hidden from screen readers, and the button has `aria-label="Close bookmark popup"`. This is correct.

7. **Collection input lacks instruction about Enter behavior** (MobileMenu.js:397-434): Users can press Enter to create a collection, but this is not communicated. Add `aria-describedby` pointing to instruction text: "Press Enter or click Add to create."

**Planned ARIA attributes for dialog container:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `role` | `"dialog"` | Dialog wrapper | 4.1.2 |
| `aria-modal` | `"true"` | Dialog wrapper | 4.1.2 |
| `aria-labelledby` | `"bookmark-dialog-title-mobile"` | Dialog wrapper | 4.1.2 |
| `aria-describedby` | `"bookmark-dialog-desc-mobile"` | Dialog wrapper | 1.3.1 |
| `tabIndex` | `"-1"` | Dialog wrapper | 2.4.3 Focus Order |

**Planned ARIA attributes for dialog contents:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `id` | `"bookmark-dialog-title-mobile"` | `<h2>` heading | 1.3.1 |
| `id` | `"bookmark-dialog-desc-mobile"` | Description `<p>` | 1.3.1 |
| `aria-label` | `"Close bookmark popup"` | Close button | 4.1.2 |
| `role` | `"group"` | Collection buttons wrapper | 1.3.1 |
| `aria-labelledby` | `"bookmark-group-label-mobile"` | Collection buttons wrapper | 1.3.1 |
| `aria-pressed` | `true`/`false` | Each collection toggle button | 4.1.2 |
| `aria-label` | `"{collection title}"` (static name only) | Each collection toggle button | 4.1.2 |
| `aria-describedby` | `"collection-input-instructions-mobile"` | New collection input | 1.3.1, 3.3.2 |

**Collection button label simplification**: Currently (MobileMenu.js:359) the label is dynamic: `"Remove from collection X"` / `"Add to collection X"`. Combined with `aria-pressed`, this creates double-announcement of state (the label says "Remove" AND the state says "pressed"). Simplify to a static `aria-label` of the collection title. `aria-pressed` alone communicates whether the bookmark is in that collection. Screen reader experience becomes: "Favorites, toggle button, pressed" (clear) instead of "Remove from collection Favorites, toggle button, pressed" (redundant).

**Keyboard interactions:**
| Key | Behavior | WCAG |
|-----|----------|------|
| Tab | Cycles through focusable elements within dialog (focus trapped) | 2.1.2 No Keyboard Trap |
| Shift+Tab | Cycles backward through focusable elements | 2.1.2 |
| Escape | Closes dialog, restores focus to bookmark trigger button | 2.1.1, 2.4.3 |
| Enter (in input) | Creates new collection, focuses the new collection button | 2.1.1 |

**Screen reader experience:**
- On dialog open: "Create a bookmark, dialog. Add bookmark to existing collection or simply create a new collection by giving it a name." (from `aria-labelledby` + `aria-describedby`)
- Close button focused: "Close bookmark popup, button"

### Widget 6: Print/Download Button

**APG Pattern**: Button -- https://www.w3.org/WAI/ARIA/apg/patterns/button/

**Current state** (MobileMenu.js:240-271): Has `aria-label="Download or print this page"`. Opens a new window for printing.

**Issue**: Opens a new browser window with no warning to the user. WCAG 3.2.2 On Input recommends informing users when new windows open.

**Planned fix**: Change `aria-label` to `"Download or print this page (opens print dialog in new window)"`. WCAG 3.2.2.

**Planned ARIA attributes:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-label` | `"Download or print this page (opens print dialog in new window)"` | Button | 4.1.2, 3.2.2 |

### Widget 7: Share by Email

**APG Pattern**: Button (activates dialog) -- https://www.w3.org/WAI/ARIA/apg/patterns/button/

**Current state** (MobileMenu.js:272-294): Two code branches:
- **Logged in** (line 273-291): `<button>` with `aria-haspopup="dialog"` and visible text "Share by email". Has a `<span className="link-icon" aria-hidden="true">` decorative icon. Missing `aria-label` -- but visible text "Share by email" serves as the accessible name, which is fine.
- **Anonymous** (line 293): `<span className="anonymous share-by-email">Share by email</span>` -- a non-interactive `<span>` styled to look like a button. This is a **WCAG 4.1.2 failure**: the element looks interactive but cannot be activated by keyboard, and has no role or state communicated to assistive technology.

**Decision required (product)**: Should anonymous users see the share button at all? Two options:

**Option A (recommended)**: Render a real `<button>` for anonymous users with `aria-disabled="true"` and an `aria-describedby` hint explaining "Log in to share by email." This mirrors the bookmark button's anonymous treatment and makes the feature discoverable.

**Option B**: Do not render the share button for anonymous users. This is simpler but removes feature discovery.

**Do NOT preserve Option C (current)**: A `<span>` that looks like a button but is not interactive. This fails WCAG 4.1.2 Name, Role, Value and 2.1.1 Keyboard.

**Planned ARIA attributes (Option A):**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-haspopup` | `"dialog"` | Button (logged in) | 4.1.2 |
| `aria-disabled` | `"true"` | Button (anonymous) | 4.1.2 |
| `aria-describedby` | `"share-login-hint"` | Button (anonymous) | 1.3.1, 3.3.2 |

### Widget 8: Fullscreen Toggle

**APG Pattern**: Toggle Button -- https://www.w3.org/WAI/ARIA/apg/patterns/button/

**Current state** (MobileMenu.js:296-331): Has `aria-label` (dynamic: "Enter fullscreen mode"/"Exit fullscreen mode") AND `aria-pressed`. This is a dual-mechanism problem.

**Issue**: `aria-pressed` already communicates state. A dynamic `aria-label` that also encodes state creates redundant announcements. Screen reader says: "Exit fullscreen mode, toggle button, pressed" -- the "Exit" and "pressed" both convey the same information. Per APG Toggle Button guidance, use a **static label** and let `aria-pressed` carry the state.

**Planned fix**: Change to static `aria-label="Fullscreen mode"` and rely on `aria-pressed` for state.

**Note on SVGs**: Both enter and exit SVGs have `aria-hidden="true"` (MobileMenu.js:308, 321). CSS shows/hides the appropriate one. Since both are aria-hidden, screen readers never encounter them. This is correct.

**Planned ARIA attributes:**
| Attribute | Value | Element | WCAG |
|-----------|-------|---------|------|
| `aria-pressed` | `true`/`false` | Toggle button | 4.1.2 |
| `aria-label` | `"Fullscreen mode"` | Toggle button | 4.1.2 |

### Interactive Elements Summary Table

| Widget | APG Pattern | Keyboard | Key ARIA | WCAG |
|--------|-------------|----------|----------|------|
| Menu toggle | [Disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) | Enter/Space: toggle | `aria-expanded`, `aria-controls` | 4.1.2, 1.3.1, 2.1.1 |
| Section toggles | [Disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) | Enter/Space: toggle | `aria-expanded`, `aria-controls` | 4.1.2, 1.3.1, 2.1.1 |
| What's new | [Toggle Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter/Space: toggle | `aria-pressed` | 4.1.2, 2.1.1 |
| Bookmark trigger | [Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter/Space: open dialog | `aria-haspopup`, `aria-disabled` | 4.1.2, 2.1.1 |
| Bookmark dialog | [Modal Dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Tab: cycle, Esc: close | `role="dialog"`, `aria-modal`, `aria-labelledby`, `aria-describedby` | 4.1.2, 2.1.2, 2.4.3 |
| Collection chips | [Toggle Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter/Space: toggle | `aria-pressed` | 4.1.2, 2.1.1 |
| Print/download | [Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter/Space: activate | `aria-label` | 4.1.2, 2.1.1 |
| Share by email | [Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter/Space: activate | `aria-haspopup`, `aria-disabled` | 4.1.2, 2.1.1 |
| Fullscreen toggle | [Toggle Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter/Space: toggle | `aria-pressed` | 4.1.2, 2.1.1 |

---

## Focus Management Plan

### Tab Order

The logical tab order within the mobile menu toolbar follows visual left-to-right order. All elements are native `<button>` elements, so no `tabindex` manipulation is needed for the toolbar itself. WCAG 2.4.3 Focus Order.

Planned tab sequence:
1. Menu toggle button ("Book navigation menu")
2. What's new toggle (conditional: hidden for materials pages)
3. Bookmark trigger button
4. Print/download button
5. Share by email button
6. Fullscreen toggle button
7. (When menu expanded) Section toggle buttons within `<ul>`: Chapters, Appendices, Index, etc.
8. (Within expanded section) Content links and controls from child components

### Focus on Menu Open

**Current** (MobileMenu.js:124-131): When `menuOpen` becomes true, `requestAnimationFrame` focuses the first `button` or `a` inside `navRef`. This is correct per the Disclosure pattern -- user opens the drawer, focus moves into it.

**No change needed.**

### Focus on Menu Close -- MISSING

**Current**: When the menu closes (toggle clicked again at MobileMenu.js:181, or `closeMobileMenu` event at MobileMenu.js:135), focus is NOT managed. It stays wherever it was within the now-hidden nav list, which means it lands on an element that may be hidden by CSS.

**Fix**: On menu close, restore focus to the menu toggle button. This follows the Disclosure pattern: user opened a region, interacted with it, closed it, focus returns to the trigger. WCAG 2.4.3.

**Implementation approach**: In the `setMenuOpen(false)` handler and the `closeMobileMenu` event handler, add: `setTimeout(() => menuToggleRef.current?.focus(), 0)`. This requires adding a ref to the menu toggle button (currently has no ref).

### Focus Trap: Bookmark Dialog

**Current** (MobileMenu.js:94-110): Tab key wrapping is implemented. Guards against MUI Dialog being open on top. Guards against empty focusable list.

**Issue**: When `focusable.length === 0` (line 100), the handler returns without preventing default. Tab would escape to browser chrome. Fix: add `e.preventDefault()` in this branch. In practice the close button is always present, but this is a defensive correctness fix for WCAG 2.1.2 No Keyboard Trap.

**No other changes needed to the trap logic.**

### Focus Restoration: Bookmark Dialog Close

**Current** (MobileMenu.js:60-64): `closeBookmark` calls `setTimeout(() => bookmarkBtnRef.current?.focus(), 0)`. This correctly restores focus to the trigger button per APG Modal Dialog pattern.

**No change needed.**

### Focus After Collection Create

**Current** (MobileMenu.js:423-429, 457-463): After creating a new collection, `setTimeout` finds the new button by text content and focuses it. This is correct -- new item appears in the list, focus moves to it per WCAG 2.4.3 Focus Order.

**No change needed**, but the duplicate code blocks (lines 423-429 and 457-463 are identical) should be extracted to a shared function for maintainability.

### Focus After Bookmark Toggle (Collection Chip)

**Current**: When a collection chip is toggled (add/remove bookmark), no focus management occurs. The button remains focused because the handler does not navigate. This is correct -- the button's `aria-pressed` state changes in place.

**No change needed.**

### Hidden Content Strategy

**Current**: The navigation drawer `<ul>` is always in the DOM. When `menuOpen` is false, it is hidden by CSS (class-based). The bookmark dialog is conditionally rendered (`{bookmark && <div ...>`), which is the preferred React pattern.

**Issue with nav drawer**: When hidden by CSS only, the nav list items remain in the tab order. Keyboard users can Tab into the hidden drawer. This needs verification -- if the CSS uses `display: none` or `visibility: hidden`, elements are removed from tab order. If it uses `transform`, `opacity`, or `height: 0`, they are NOT.

**Plan**: Verify the CSS hiding mechanism. If it does NOT remove from tab order, add conditional rendering (`{menuOpen && <ul ...>}`) or apply the `hidden` attribute / `inert` attribute when closed. WCAG 2.1.1 Keyboard, 2.4.3 Focus Order.

---

## State Communication Design

### Missing: Live Regions

The component has NO live regions. Error messages are set via `setError()` (context), but whether the error context renders into a `role="alert"` element is not visible in this component's code. The following state changes happen silently for screen reader users:

| Event | Current announcement | Required announcement |
|-------|---------------------|----------------------|
| Bookmark added to collection | None | "Bookmark added to {collection}" via `role="status"` |
| Bookmark removed from collection | None | "Bookmark removed from {collection}" via `role="status"` |
| New collection created | None (focus moves to new button, which is good) | Focus move is sufficient; optionally add status |
| Error saving bookmark | `setError()` -- need to verify reaches `role="alert"` | Must reach `role="alert"` or `aria-live="assertive"` |
| Anonymous user activates disabled feature | `setError('Please log in to use this feature.')` | Must reach `role="alert"` |
| Fullscreen entered/exited | None | `role="status"`: "Entered fullscreen mode" / "Exited fullscreen mode" |
| Collection limit reached | Visible text only | Already visible; no live region needed since dialog is already open |

**Plan**: Add a single `role="status"` (`aria-live="polite"`) region within the `<nav>` for non-error state changes (bookmark add/remove, fullscreen). Verify the error context upstream renders into a `role="alert"` region -- if not, add one. WCAG 4.1.3 Status Messages.

Per Known Pitfall #1: Plan ONE announcement region per event class. Do NOT put `role="alert"` on each collection button or error message instance. Use a single status region whose text content is updated.

### State Communication Table

| State | Visual Indicator | Programmatic Indicator | ARIA | WCAG |
|-------|-----------------|----------------------|------|------|
| Menu open/closed | Drawer visible/hidden, button icon rotates | `aria-expanded` on toggle button | `aria-expanded="true"/"false"` | 4.1.2, 1.4.1 |
| Section open/closed | Panel visible/hidden | `aria-expanded` on section button | `aria-expanded="true"/"false"` | 4.1.2, 1.4.1 |
| What's new active/inactive | Star icon filled green / outline | `aria-pressed` on toggle | `aria-pressed="true"/"false"` | 4.1.2, 1.4.1 |
| Bookmarked/not bookmarked | Icon has `.marked` class (visual change) | `aria-pressed` on collection buttons within dialog | `aria-pressed="true"/"false"` | 4.1.2, 1.4.1 |
| Bookmark feature disabled (anonymous) | Different visual class `.anonymous` | `aria-disabled="true"` + `aria-describedby` hint | `aria-disabled="true"` | 4.1.2, 3.3.2 |
| Share feature disabled (anonymous) | Styled as span (current -- change to disabled button) | `aria-disabled="true"` + `aria-describedby` hint | `aria-disabled="true"` | 4.1.2, 3.3.2 |
| Fullscreen on/off | Different SVG icon shown | `aria-pressed` on toggle | `aria-pressed="true"/"false"` | 4.1.2, 1.4.1 |
| Dialog open | Dialog overlay visible | `role="dialog"`, `aria-modal="true"` | Dialog semantics | 4.1.2 |
| Bookmark save error | Error message via context | Must reach `role="alert"` | `aria-live="assertive"` | 4.1.3 |
| Bookmark save success | Visual state change on chip | Status region text update | `aria-live="polite"` | 4.1.3 |
| Collection limit reached | Text message in dialog | Visible text (already in dialog focus trap) | N/A | 3.3.1 |

### Visual-Only State Indicators That Need Non-Color Alternatives

| State | Current visual | Color-only? | Non-color alternative needed | WCAG |
|-------|---------------|-------------|------------------------------|------|
| What's new active | Green filled star vs outline stroke | Yes -- green fill is the only differentiator | `aria-pressed` communicates programmatically; visually the filled vs outline shape is a non-color indicator (shape change). Verify the outline star is visible against background at 3:1 contrast. | 1.4.1, 1.4.11 |
| Bookmark marked | `.marked` class -- need to verify what this changes | Possibly | Verify the visual change includes more than color (e.g., filled vs outline icon) | 1.4.1 |
| Anonymous button styling | `.anonymous` class | Verify | Must have visual indicator beyond color (e.g., reduced opacity is acceptable if combined with cursor change) | 1.4.1 |

### The "&times;" Symbol in Close Button

**Current** (MobileMenu.js:341): `<span aria-hidden="true">&times;</span>` -- correctly hidden. The button has `aria-label="Close bookmark popup"`. No change needed. Per Phase 5 guidance on visual text symbols, the `aria-hidden` is already applied.

### The "+" Symbol in Add Button

**Current** (MobileMenu.js:468): `<span aria-hidden="true" className="btn-link-icon">+</span>` -- correctly hidden. The button's visible text is "Add" via `<span>Add</span>`. No change needed.

---

## Visual Accessibility Plan

### Color Contrast (WCAG 1.4.3)

The toolbar icons use `fill="currentColor"` which inherits from the CSS `color` property. Verify:
- Icon color against toolbar background: must meet 3:1 for non-text UI components (WCAG 1.4.11)
- Any text labels (e.g., "Share by email" button text): must meet 4.5:1 (WCAG 1.4.3)
- Dialog text and input fields: standard contrast requirements

The "What's new" toggle uses `fill={whatNew ? '#048D36' : 'none'}` (MobileMenu.js:208). `#048D36` (green) against the toolbar background must meet 3:1.

### Focus Indicators (WCAG 2.4.7, 2.4.11)

Plan a two-color focus indicator for all toolbar buttons:
- `outline: 2px solid #005fcc` (dark ring)
- `box-shadow: 0 0 0 4px #ffffff` (light ring)
- Use `:focus-visible` (not `:focus`) to avoid showing on mouse click
- Verify focus ring visibility in both light and dark contexts within the toolbar
- Verify focus ring on dialog close button, collection chips, and input field

### Touch Targets (WCAG 2.5.8)

This is a mobile toolbar. All toolbar buttons MUST be at least 44x44 CSS pixels. Currently the SVG icons are `width="1.5rem" height="1.5rem"` (24px at default font size). The clickable `<button>` elements must have sufficient padding/sizing to reach 44x44.

**Verify**: Measure the rendered button dimensions. If under 44x44, add padding.

### Reflow at 320px (WCAG 1.4.10)

The mobile menu is already designed for narrow viewports. Verify:
- At 320px wide (or 1280px at 400% zoom), no horizontal scroll
- Toolbar buttons wrap or resize appropriately
- Bookmark dialog is usable without horizontal scroll (the dialog uses percentage width on desktop; verify mobile)

### Animation and Motion (WCAG 2.3.3)

The fullscreen toggle uses `setTimeout` with a 500ms delay for class transitions (MobileMenu.js:169-171). If there are CSS transitions on the fullscreen state change, ensure they respect `prefers-reduced-motion: reduce`.

### Font Sizing (WCAG 1.4.4)

Dialog text, labels, and collection names must use relative units (`rem`/`em`). The input placeholder "New Collections Name" (MobileMenu.js:399) should not be the only size reference. Verify the CSS does not use fixed `px` for font sizes in the bookmark dialog.

---

## Content Accessibility Plan

### Alt Text Strategy (WCAG 1.1.1)

All SVGs in the toolbar have `aria-hidden="true"`. The buttons have `aria-label` attributes providing the accessible name. This is the correct pattern for icon-only buttons.

**One fix**: The SVG at MobileMenu.js:385 (checkmark in collection chips) has an empty `<title />` element. Remove it. Empty `<title>` elements can create empty accessible name entries in some browser/AT combinations. The SVG already has `aria-hidden="true"`.

### Link Text Quality (WCAG 2.4.4)

The "Companion materials" link in `mobileMenuMainLink.js:13-24` opens in a new tab and correctly includes `<span className="visually-hidden"> (opens in new page)</span>`. No change needed.

### Form Label Association (WCAG 1.3.1, 3.3.2)

The collection name input has a proper `<label htmlFor="new-collection-input-mobile">` (MobileMenu.js:394). This is correct.

**Addition needed**: `aria-describedby` on the input pointing to instruction text about Enter behavior: "Press Enter or click Add to create a collection." WCAG 3.3.2 Labels or Instructions.

### Error Message Clarity (WCAG 3.3.1, 3.3.4)

Current error messages:
- `"Please log in to use this feature."` (MobileMenu.js:226) -- adequate but generic
- `"Failed to update bookmark. Please try again."` (MobileMenu.js:379) -- adequate
- `"Failed to save collection. Please try again."` (MobileMenu.js:431, 465) -- adequate

**Verify**: These errors are set via `setError()` from context. Confirm the `Errors` context renders its content into a `role="alert"` region somewhere in the component tree. If not, this is a critical gap -- errors would be visually displayed but never announced. WCAG 4.1.3.

### Reading Order (WCAG 1.3.2)

DOM order matches visual order: toolbar buttons left-to-right, then navigation list below. The bookmark dialog renders after the toolbar in the DOM but is visually overlaid -- this is standard for dialogs and acceptable because `aria-modal="true"` signals the overlay relationship.

### Language (WCAG 3.1.1)

All content is English. No foreign language fragments. `<html lang="en">` assumed on the page root.

---

## Testing Strategy

### 1. Automated Testing (axe-core)

Run axe-core on each state variant:
- Default state (menu closed, logged in)
- Menu open (with Chapters expanded)
- Bookmark dialog open (with collections)
- Bookmark dialog open (no collections -- new user)
- Bookmark dialog open (at collection limit)
- Anonymous user state (share as disabled button, bookmark as aria-disabled)

axe-core validates: contrast, ARIA attribute validity, label association, heading hierarchy, landmark regions.

axe-core does NOT validate: focus management, live region announcements, keyboard navigation, focus trap correctness, dynamic state changes.

### 2. Manual Keyboard Testing

| Test | Steps | Expected | WCAG |
|------|-------|----------|------|
| Tab through toolbar | Tab from page content to toolbar | Focus visits each toolbar button in L-to-R order | 2.4.3 |
| Open menu | Focus menu toggle, press Enter | Menu expands, `aria-expanded="true"`, focus moves to first nav item | 2.1.1, 4.1.2 |
| Close menu | Focus menu toggle (or press toggle again), press Enter | Menu collapses, `aria-expanded="false"`, focus returns to menu toggle | 2.1.1, 2.4.3 |
| Open section | Focus "Chapters" button, press Space | Section expands, `aria-expanded="true"`, focus moves to first element in panel | 2.1.1, 4.1.2 |
| Toggle what's new | Focus what's new, press Enter | `aria-pressed` toggles, visual star changes | 2.1.1, 4.1.2 |
| Open bookmark dialog | Focus bookmark button, press Enter | Dialog opens, focus on close button, `aria-modal="true"` | 2.1.1, 4.1.2 |
| Tab within dialog | Tab through dialog | Focus cycles: close button -> collection chips -> input -> add button -> close button | 2.1.2 |
| Escape from dialog | Press Escape in dialog | Dialog closes, focus returns to bookmark trigger button | 2.1.1, 2.4.3 |
| Toggle collection chip | Focus a chip, press Enter | `aria-pressed` toggles, status region announces change | 2.1.1, 4.1.2, 4.1.3 |
| Create collection via Enter | Type name in input, press Enter | Collection created, focus moves to new chip button | 2.1.1, 2.4.3 |
| Anonymous bookmark | Focus bookmark (aria-disabled), press Enter | No dialog opens; status region announces "Log in to bookmark pages" | 4.1.2, 4.1.3 |
| Anonymous share | Focus share button (aria-disabled), press Enter | No action; described by login hint | 4.1.2, 3.3.2 |
| Fullscreen toggle | Focus fullscreen button, press Space | `aria-pressed` toggles, status region announces mode change | 2.1.1, 4.1.2 |
| Print button | Focus print button, press Enter | Print dialog opens in new window | 2.1.1 |
| Focus indicators | Tab through all elements | Visible two-color focus ring on every focusable element | 2.4.7 |

### 3. Screen Reader Testing

Test with NVDA (Windows, Firefox) and VoiceOver (macOS Safari, iOS Safari):

| Test | Expected announcement |
|------|----------------------|
| Navigate to toolbar | "Book tools and navigation, navigation" (landmark) |
| Focus menu toggle | "Book navigation menu, button, collapsed" |
| After opening menu | "Book navigation menu, button, expanded" |
| Focus what's new | "Highlight updated content, toggle button, not pressed" |
| Focus bookmark (logged in) | "Bookmark this page, button, has popup dialog" |
| Focus bookmark (anonymous) | "Bookmark this page, button, dimmed" (NVDA) or "dimmed" (VO) |
| Dialog opens | "Create a bookmark, dialog. Add bookmark to existing collection..." |
| Focus collection chip | "Favorites, toggle button, pressed" |
| Toggle collection chip | Status region: "Bookmark added to Favorites" |
| Focus fullscreen | "Fullscreen mode, toggle button, not pressed" |
| Focus share (anonymous) | "Share by email, button, dimmed" |

### 4. DOM Verification (Required per Known Pitfall #9)

After implementation, inspect rendered DOM to confirm:
- `aria-controls` on menu toggle points to an element with matching `id` that exists in DOM
- `aria-controls` on section toggles point to existing panel `id`s
- `aria-labelledby` on dialog points to existing heading `id`
- `aria-describedby` on dialog points to existing paragraph `id`
- `aria-describedby` on input points to existing instruction `id`
- `aria-describedby` on anonymous buttons points to existing hint `id`s
- `role="status"` region exists and is populated on state changes
- Error context renders into `role="alert"` somewhere in the tree

### 5. Acceptance Criteria

- All toolbar buttons are keyboard operable (Enter and Space activate)
- Menu toggle has `aria-expanded` and `aria-controls` with valid id reference
- Menu open focuses first nav item; menu close focuses toggle button
- Bookmark dialog traps focus (Tab cycles, Escape closes)
- Bookmark dialog focus restores to trigger on close
- Dialog heading is h2, referenced by `aria-labelledby`
- All toggle buttons use static labels with `aria-pressed` (no dual-mechanism labels)
- Anonymous share renders as `<button aria-disabled="true">` not `<span>`
- Status region announces bookmark add/remove and fullscreen state changes
- Error messages reach a `role="alert"` region
- No `<nav>` landmark missing -- wrapper is `<nav aria-label="Book tools and navigation">`
- axe-core reports zero violations in all state variants
- Touch targets are 44x44 minimum on mobile

---

## Implementation Tasks

### Task 1: Wrap in `<nav>` Landmark

**Files:** `MobileMenu.js`

**Structure stub:**
```
Current:  <div className="bookreader-mobile-mobile-nav">
Planned:  <nav className="bookreader-mobile-mobile-nav" aria-label="Book tools and navigation">
```

**ARIA Attributes:**
- `aria-label="Book tools and navigation"` -- WCAG 1.3.1 Info and Relationships, 2.4.1 Bypass Blocks

**Tests:**
- axe-core landmark validation
- Screen reader announces navigation landmark

**WCAG Criteria:** 1.3.1, 2.4.1

### Task 2: Add `aria-controls` to Menu Toggle and Section Toggles

**Files:** `MobileMenu.js`, `mobileMenuMainLink.js`

**Structure stub:**
```
MobileMenu.js toggle button:
  Add: aria-controls="mobile-nav-list"

MobileMenu.js <ul>:
  Add: id="mobile-nav-list"

mobileMenuMainLink.js section button:
  Add: aria-controls="{items.key}-panel"

mobileMenuMainLink.js content wrapper:
  Wrap items.content in: <div id="{items.key}-panel">
```

**ARIA Attributes:**
- `aria-controls` -- WCAG 1.3.1 Info and Relationships
- `id` on controlled panels -- WCAG 1.3.1

**Tests:**
- DOM verify: `aria-controls` values resolve to existing `id`s
- Screen reader: button announces relationship to controlled region

**WCAG Criteria:** 1.3.1

### Task 3: Focus Restoration on Menu Close

**Files:** `MobileMenu.js`

**Logic:**
1. Add `useRef` for the menu toggle button (currently has none)
2. When `setMenuOpen(false)` is called (line 181 toggle, line 135 event handler), restore focus: `setTimeout(() => menuToggleRef.current?.focus(), 0)`
3. Only restore focus if the menu was previously open (avoid stealing focus on initial render)

**Keyboard Interactions:**
- Close menu via toggle button: focus stays on toggle (already there)
- Close menu via `closeMobileMenu` event: focus moves to toggle button

**Tests:**
- Open menu, Tab into nav, trigger closeMobileMenu event -- verify focus on toggle
- Open menu, click toggle to close -- verify focus remains on toggle

**WCAG Criteria:** 2.4.3 Focus Order

### Task 4: Fix Bookmark Dialog Labeling

**Files:** `MobileMenu.js`

**Structure stub:**
```
Current:
  <div role="dialog" aria-label="Create a bookmark" aria-modal="true">
    <h4>Create a bookmark</h4>
    <p>Add bookmark to existing collection...</p>

Planned:
  <div role="dialog" aria-labelledby="bookmark-dialog-title-mobile"
       aria-describedby="bookmark-dialog-desc-mobile" aria-modal="true">
    <h2 id="bookmark-dialog-title-mobile">Create a bookmark</h2>
    <p id="bookmark-dialog-desc-mobile">Add bookmark to existing collection...</p>
```

**ARIA Attributes:**
- Remove `aria-label="Create a bookmark"` -- replaced by `aria-labelledby`
- Add `aria-labelledby="bookmark-dialog-title-mobile"` -- WCAG 4.1.2 Name, Role, Value
- Add `aria-describedby="bookmark-dialog-desc-mobile"` -- WCAG 1.3.1 Info and Relationships
- Promote `<h4>` to `<h2>` -- WCAG 1.3.1

**Tests:**
- DOM verify: `aria-labelledby` resolves to heading id
- DOM verify: `aria-describedby` resolves to description id
- Screen reader: on dialog open, announces title then description
- axe-core: heading hierarchy passes

**WCAG Criteria:** 1.3.1, 4.1.2

### Task 5: Fix Dialog Focus Trap Edge Case

**Files:** `MobileMenu.js`

**Logic:** At line 100, change `if (focusable.length === 0) return` to:
```
if (focusable.length === 0) {
  e.preventDefault()
  return
}
```

**Tests:**
- (Defensive) If dialog somehow has no focusable elements, Tab does not escape

**WCAG Criteria:** 2.1.2 No Keyboard Trap

### Task 6: Simplify Collection Button Labels

**Files:** `MobileMenu.js`

**Current** (line 359):
```
aria-label={`${bookmarkItems && bookmarkItems.includes(id) ? 'Remove from' : 'Add to'} collection ${data.title}`}
```

**Planned:**
```
aria-label={data.title}
```

The `aria-pressed` attribute already communicates the state (in collection / not in collection). The dynamic "Add to"/"Remove from" prefix creates redundant and confusing announcements.

**Tests:**
- Screen reader: focus chip -- hears "Favorites, toggle button, pressed" (not "Remove from collection Favorites, toggle button, pressed")
- Toggle chip -- hears state change "not pressed" (not label change + state change)

**WCAG Criteria:** 4.1.2 Name, Role, Value

### Task 7: Fix "What's New" Toggle Label and Remove Dead Span

**Files:** `MobileMenu.js`

**PRODUCT DECISION REQUIRED**: The replacement label "Highlight updated content" is a best guess. The `whatNew` flag's downstream behavior is not visible from this component. **Verify with product team what the toggle actually does before choosing the final label.** The current label "See what's new" is vague and does not describe the toggle action.

**Changes:**
1. Change `aria-label="See what's new"` to `aria-label="Highlight updated content"` (line 201) -- or whatever label product confirms
2. Remove `<span className="visually-hidden">see what's new</span>` (line 212) -- `aria-label` already provides the accessible name; the span is dead weight

**Tests:**
- Screen reader: "{confirmed label}, toggle button, not pressed"
- DOM verify: no duplicate accessible name sources

**WCAG Criteria:** 4.1.2 Name, Role, Value

### Task 8: Fix Fullscreen Toggle Dual-Mechanism Label

**Files:** `MobileMenu.js`

**Current** (lines 299-300):
```
aria-label={isFullscreen ? 'Exit fullscreen mode' : 'Enter fullscreen mode'}
aria-pressed={isFullscreen}
```

**Planned:**
```
aria-label="Fullscreen mode"
aria-pressed={isFullscreen}
```

**Tests:**
- Screen reader: "Fullscreen mode, toggle button, not pressed" (then "pressed" after activation)

**WCAG Criteria:** 4.1.2 Name, Role, Value

### Task 9: Fix Anonymous Share-by-Email

**Files:** `MobileMenu.js`

**Current** (line 293):
```
<span className="anonymous share-by-email">Share by email</span>
```

**Planned:**
```
<button
  type="button"
  className="anonymous share-by-email"
  aria-disabled="true"
  aria-describedby="share-login-hint-mobile"
  onClick={(e) => {
    if (e.currentTarget.getAttribute('aria-disabled') === 'true') return
  }}
>
  <span className="link-icon" aria-hidden="true"></span>
  Share by email
</button>
<span id="share-login-hint-mobile" className="visually-hidden">
  Log in to share by email
</span>
```

**ARIA Attributes:**
- `aria-disabled="true"` -- WCAG 4.1.2 Name, Role, Value
- `aria-describedby="share-login-hint-mobile"` -- WCAG 1.3.1, 3.3.2

**Tests:**
- Keyboard: Tab reaches the button; Enter/Space does nothing
- Screen reader: "Share by email, button, dimmed. Log in to share by email."
- DOM verify: element is `<button>` not `<span>`

**WCAG Criteria:** 4.1.2, 2.1.1, 1.3.1, 3.3.2

### Task 10: Fix Anonymous Bookmark Button Behavior

**Files:** `MobileMenu.js`

**Current** (lines 220-227): `aria-disabled="true"` is set, but click handler still calls `setError()`.

**Planned:**
- Guard the click handler: if `aria-disabled`, do not call `setOverlay`/`setBookmark`
- Instead, update the status region with "Log in to bookmark pages"
- Add `aria-describedby` pointing to a persistent hint: "Log in to bookmark pages"

**Structure stub:**
```
<button
  aria-disabled={!userId ? 'true' : undefined}
  aria-describedby={!userId ? 'bookmark-login-hint-mobile' : undefined}
  onClick={() => {
    if (!userId) {
      // Update status region, do NOT open dialog
      setStatusMessage('Log in to bookmark pages')
      return
    }
    setOverlay(!bookmark)
    setBookmark(!bookmark)
  }}
>
...
<span id="bookmark-login-hint-mobile" className="visually-hidden">
  Log in to bookmark pages
</span>
```

**Tests:**
- Anonymous: Enter on bookmark button -- status region announces "Log in to bookmark pages", no dialog opens
- Logged in: Enter on bookmark button -- dialog opens normally

**WCAG Criteria:** 4.1.2, 4.1.3, 3.3.2

### Task 11: Add Live Regions for State Changes

**Files:** `MobileMenu.js`

**Structure stub:**
```
<!-- Single status region for non-error announcements -->
<div role="status" aria-live="polite" className="visually-hidden"
     id="mobile-menu-status">
  {statusMessage}
</div>
```

**State changes that populate the status region:**
- Bookmark added: "Bookmark added to {collection title}"
- Bookmark removed: "Bookmark removed from {collection title}"
- Fullscreen entered: "Entered fullscreen mode"
- Fullscreen exited: "Exited fullscreen mode"
- Anonymous feature attempt: "Log in to bookmark pages" / "Log in to share by email"

**Error path verification:**
- Confirm `setError()` from `Errors` context renders into a `role="alert"` region upstream
- If not, add one in the appropriate parent component

**ARIA Attributes:**
- `role="status"` -- WCAG 4.1.3 Status Messages (equivalent to `aria-live="polite"`)
- Per Known Pitfall #1: ONE region, not per-collection

**Tests:**
- Toggle collection chip -- status region text changes, screen reader announces
- Toggle fullscreen -- status region text changes
- DOM verify: only one `role="status"` region in the component, text updates on each event

**WCAG Criteria:** 4.1.3

### Task 12: Add Input Instructions for Collection Creation

**Files:** `MobileMenu.js`

**Structure stub:**
```
<input
  id="new-collection-input-mobile"
  aria-describedby="collection-input-instructions-mobile"
  ...
/>
<span id="collection-input-instructions-mobile" className="visually-hidden">
  Press Enter or click Add to create a collection
</span>
```

**ARIA Attributes:**
- `aria-describedby="collection-input-instructions-mobile"` -- WCAG 3.3.2 Labels or Instructions, 1.3.1

**Tests:**
- Screen reader: focus input -- hears label then description
- DOM verify: `aria-describedby` resolves to existing id

**WCAG Criteria:** 1.3.1, 3.3.2

### Task 13: Update Print Button Label

**Files:** `MobileMenu.js`

**Change:**
```
Current:  aria-label="Download or print this page"
Planned:  aria-label="Download or print this page (opens print dialog in new window)"
```

**WCAG Criteria:** 3.2.2 On Input, 4.1.2

### Task 14: Remove Empty SVG Title Element

**Files:** `MobileMenu.js`

**Change:** Remove `<title />` from the SVG at line 385 (inside collection chip buttons). The SVG already has `aria-hidden="true"`.

**WCAG Criteria:** 1.1.1 Non-text Content (cleanup)

### Task 15: Verify Hidden Nav Drawer Tab Order

**Files:** CSS files for `.bookreader-mobile-nav`

**Investigation:** Determine how the nav drawer is hidden when closed. If it uses `display: none` or `visibility: hidden`, elements are already removed from tab order. If it uses `transform`, `opacity`, `max-height: 0`, or similar, elements remain focusable when visually hidden.

**If focusable when hidden:** Switch to conditional rendering (`{menuOpen && <ul ...>}`) or add the `hidden` attribute when closed.

**Tests:**
- With menu closed, Tab through toolbar -- verify focus never enters the nav list
- With menu closed, screen reader browse mode -- verify nav list content not reachable

**WCAG Criteria:** 2.1.1 Keyboard, 2.4.3 Focus Order

### Task 16: Verify Touch Targets

**Files:** CSS for `.bookreader-mobile-mobile-nav button`

**Verification:** Measure rendered button dimensions. All toolbar buttons must be 44x44 CSS pixels minimum. SVG icons are 24px; buttons need sufficient padding.

**If under 44x44:** Add `min-width: 44px; min-height: 44px;` or equivalent padding.

**WCAG Criteria:** 2.5.8 Target Size

### Task 17: Verify Error Context Reaches `role="alert"`

**Files:** Upstream error rendering component (trace `Errors` context from `menuContext.js`)

**Verification:** Find where `Errors` context value is rendered. Confirm the container has `role="alert"` or `aria-live="assertive"`.

**This audit may result in one of two outcomes:**
- **Simple case**: The existing error rendering element just needs `role="alert"` added to its container.
- **Complex case**: The error context renders into a generic element with no live region semantics, or renders in a location that is not perceivable (e.g., hidden by the dialog overlay). In this case, a new `role="alert"` container must be added at an appropriate level in the component tree -- outside any `aria-modal` dialog so it is always announced.

**If missing:** Add `role="alert"` to the error rendering element, or create a dedicated alert region.

**Tests:**
- Trigger an error (e.g., bookmark save failure) -- screen reader announces immediately
- Trigger an error while the bookmark dialog is open -- verify announcement is not suppressed by `aria-modal`
- DOM verify: error text is inside a `role="alert"` element

**WCAG Criteria:** 4.1.3 Status Messages

---

## a11y-Critic Review Checkpoints

| Checkpoint | After Task | Focus |
|-----------|-----------|-------|
| 1 | Task 1-2 | Landmark structure present. `aria-controls` references resolve. No orphaned ids. |
| 2 | Task 3-5 | Focus management: menu close restores focus, dialog trap has no escape path, dialog focus restoration works. |
| 3 | Task 4, 6-8 | APG pattern compliance: dialog uses `aria-labelledby` not `aria-label`, toggle buttons use static labels with `aria-pressed`, no dual-mechanism labels. |
| 4 | Task 9-10 | Anonymous user path: both share and bookmark render as real buttons with `aria-disabled`, describedby hints present, click handlers guarded. |
| 5 | Task 11-12 | Live regions: single `role="status"` region exists, bookmark/fullscreen changes populate it, input instructions present, error path reaches `role="alert"`. |
| 6 | Task 13-17 | Polish: print label warns about new window, SVG title removed, hidden nav not in tab order, touch targets verified, error context verified. |

---

### Contract Appendix (for spec-kitty-bridge WP translation)

### Architecture Overview

The MobileMenu component requires accessibility fixes across four interaction patterns: Disclosure (menu and section toggles), Toggle Button (what's new, fullscreen, collection chips), Modal Dialog (bookmark popup), and Button (print, share). The primary architectural changes are: wrapping the component in a `<nav>` landmark, adding `aria-controls` relationships to all disclosure toggles, introducing a `role="status"` live region for dynamic state announcements, fixing dialog labeling from `aria-label` to `aria-labelledby`/`aria-describedby`, replacing the anonymous share `<span>` with a disabled `<button>`, and adding focus restoration on menu close. No new components are needed; all changes are within `MobileMenu.js` and `mobileMenuMainLink.js`.

### Implementation Tasks

#### Task 1: Nav Landmark
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 1
axe-core landmark validation. Screen reader landmark navigation.
#### Acceptance Criteria for Task 1
Outer wrapper is `<nav aria-label="Book tools and navigation">`. axe-core reports no landmark violations.

#### Task 2: aria-controls Relationships
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 2
DOM inspection: every `aria-controls` value resolves to an existing element `id`.
#### Acceptance Criteria for Task 2
Menu toggle has `aria-controls="mobile-nav-list"`. Each section toggle has `aria-controls="{key}-panel"`. All referenced ids exist in DOM.

#### Task 3: Focus Restoration on Menu Close
Estimated Effort: medium
Depends on: none
#### Test Strategy for Task 3
Keyboard test: open menu, tab into nav, trigger close event, verify focus is on toggle button.
#### Acceptance Criteria for Task 3
After menu closes (by any mechanism), `document.activeElement` is the menu toggle button.

#### Task 4: Dialog Labeling Fix
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 4
DOM inspection: `aria-labelledby` and `aria-describedby` resolve. axe-core heading hierarchy. Screen reader announces title + description on dialog open.
#### Acceptance Criteria for Task 4
Dialog has `aria-labelledby` (not `aria-label`). Heading is `<h2>`. `aria-describedby` references description paragraph.

#### Task 5: Focus Trap Edge Case
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 5
Unit test: mock dialog with no focusable elements, verify Tab event is prevented.
#### Acceptance Criteria for Task 5
`e.preventDefault()` called when `focusable.length === 0` in the bookmark dialog keydown handler.

#### Task 6: Collection Button Label Simplification
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 6
Screen reader test: focus chip, verify announcement is "{title}, toggle button, pressed" without "Add to"/"Remove from" prefix.
#### Acceptance Criteria for Task 6
Collection buttons have `aria-label={data.title}` (static). No dynamic Add/Remove prefix.

#### Task 7: What's New Label + Dead Span Removal
Estimated Effort: low
Depends on: none (but requires product decision on correct label -- see "Open Product Decisions" in Scope)
#### Test Strategy for Task 7
Screen reader test: "{confirmed label}, toggle button". DOM verify: no visually-hidden span with duplicate text.
#### Acceptance Criteria for Task 7
`aria-label` set to product-confirmed label (placeholder: "Highlight updated content"). Visually-hidden span removed.

#### Task 8: Fullscreen Toggle Label Fix
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 8
Screen reader test: "Fullscreen mode, toggle button, not pressed".
#### Acceptance Criteria for Task 8
`aria-label="Fullscreen mode"` (static). No dynamic Enter/Exit prefix.

#### Task 9: Anonymous Share-by-Email Fix
Estimated Effort: medium
Depends on: [11]
#### Test Strategy for Task 9
DOM verify: element is `<button>` not `<span>`. Keyboard: Tab reaches it, Enter does nothing. Screen reader: "Share by email, button, dimmed. Log in to share by email."
#### Acceptance Criteria for Task 9
Anonymous state renders `<button aria-disabled="true" aria-describedby="...">` with login hint.

#### Task 10: Anonymous Bookmark Behavior Fix
Estimated Effort: medium
Depends on: [11]
#### Test Strategy for Task 10
Click on anonymous bookmark: no dialog opens, status region updated. Screen reader: status message announced.
#### Acceptance Criteria for Task 10
Click handler guarded by `aria-disabled` check. Status region receives "Log in to bookmark pages." No dialog opens for anonymous users.

#### Task 11: Live Regions
Estimated Effort: medium
Depends on: none
#### Test Strategy for Task 11
Screen reader: toggle collection chip -- hear "Bookmark added/removed." Toggle fullscreen -- hear mode change. DOM verify: single `role="status"` region, text content changes.
#### Acceptance Criteria for Task 11
One `role="status"` region in component. Bookmark add/remove and fullscreen state changes populate it. Only one announcement region (not per-collection).

#### Task 12: Input Instructions
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 12
Screen reader: focus input, hear label then "Press Enter or click Add to create a collection." DOM verify: `aria-describedby` resolves.
#### Acceptance Criteria for Task 12
Input has `aria-describedby` pointing to instruction span. Instructions visible in screen reader description.

#### Task 13: Print Button Label Update
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 13
Screen reader: "Download or print this page, opens print dialog in new window, button."
#### Acceptance Criteria for Task 13
`aria-label` includes new-window warning text.

#### Task 14: SVG Title Cleanup
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 14
DOM verify: no `<title>` element inside the collection chip SVG.
#### Acceptance Criteria for Task 14
Empty `<title />` removed from SVG at former line 385.

#### Task 15: Hidden Nav Tab Order Verification
Estimated Effort: low-medium (depends on CSS investigation)
Depends on: none
#### Test Strategy for Task 15
Keyboard: with menu closed, Tab through toolbar, verify focus never enters nav list. Use `document.activeElement` logging.
#### Acceptance Criteria for Task 15
When menu is closed, no element inside the nav list is reachable by Tab.

#### Task 16: Touch Target Verification
Estimated Effort: low
Depends on: none
#### Test Strategy for Task 16
Measure rendered button dimensions with DevTools. All toolbar buttons 44x44 minimum.
#### Acceptance Criteria for Task 16
All interactive elements in toolbar are at least 44x44 CSS pixels.

#### Task 17: Error Context Audit
Estimated Effort: low-medium (depends on upstream investigation; may escalate if no existing alert region)
Depends on: none
#### Test Strategy for Task 17
Trace `Errors` context. DOM verify: error text renders inside `role="alert"`. Screen reader: trigger error, verify immediate announcement. Trigger error while bookmark dialog is open -- verify announcement not suppressed by `aria-modal`.
#### Acceptance Criteria for Task 17
Error messages from `setError()` are rendered inside a `role="alert"` element that is outside any `aria-modal` dialog container.

### Failure Modes

1. **Missing focus restoration on menu close**: Keyboard users lose focus position after closing the navigation drawer. Focus falls to `<body>` or stays on a hidden element. WCAG 2.4.3.
2. **Incorrect ARIA states on toggle buttons**: Dual-mechanism labels (dynamic aria-label + aria-pressed) cause confusing redundant announcements. Blocks efficient screen reader operation.
3. **No live regions for bookmark operations**: Screen reader users toggle a collection chip and get no confirmation. They cannot verify the action succeeded without navigating away and back.
4. **Anonymous share as non-interactive span**: Keyboard users cannot reach the element. Screen reader users do not know the feature exists. WCAG 4.1.2, 2.1.1.
5. **Dialog labeled with aria-label instead of aria-labelledby**: Heading content is ignored by screen readers; the heading exists visually but is invisible to the accessibility tree's labeling chain.
6. **Dialog focus trap allows escape on empty focusable list**: Edge case where Tab exits the dialog to browser chrome. WCAG 2.1.2.
7. **Error messages not in role="alert"**: If the upstream error context doesn't render into an alert region, all error announcements are silent for screen reader users.
8. **Hidden nav drawer remains in tab order**: If CSS hiding mechanism doesn't remove from tab order, keyboard users enter an invisible navigation list.
