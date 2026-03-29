#!/usr/bin/env python3
"""Generate metadata.yaml and rubric.yaml files for all remaining fixtures."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── Fixture specifications ────────────────────────────────────────────
# Each spec drives generation of .metadata.yaml and .rubric.yaml
# The .md files (with component code) are written separately.

FIXTURES = [
    # ─── HAS-BUGS: New Dimensions ───────────────────────────────
    {
        "id": "dense-admin-jargon",
        "name": "Dense Admin Settings Panel With Technical Jargon",
        "category": "HAS-BUGS",
        "domain": "Data Display",
        "primary": "cognitive_neurodivergent",
        "secondary": "magnification_reflow",
        "description": "React admin settings panel with dense 3-column layout, 9px text, technical jargon without tooltips, 12+ ungrouped toggles, and error codes instead of descriptions. All toggles are native checkbox elements with labels.",
        "alarms": {"magnification_reflow": "HIGH", "environmental_contrast": "MEDIUM", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "HIGH"},
        "must_find": [
            {"desc": "Dense 3-column layout at 9px text with no density control", "sev": "CRITICAL", "wcag": "1.4.4 Resize Text", "ev": "font-size: 9px on .settings-grid cells; no toggle for density", "ug": "Low-vision users, magnification users"},
            {"desc": "Technical jargon throughout with no tooltips or glossary", "sev": "MAJOR", "wcag": "3.1.3 Unusual Words (AAA) / Cognitive", "ev": "Labels like 'Enable HSTS preloading', 'Set CSP nonce strategy' with no explanation", "ug": "Cognitive disability users, non-expert users"},
        ],
        "should_find": [
            {"desc": "12+ toggle switches in single view with no grouping or sections", "sev": "MAJOR", "wcag": "1.3.1 Info and Relationships / Cognitive", "ev": "All toggles in flat list with no fieldset or heading groups", "ug": "Cognitive/attention users"},
            {"desc": "Save button at bottom of long form with no unsaved-changes indicator", "sev": "MAJOR", "wcag": "3.3.4 Error Prevention / Cognitive", "ev": "No dirty-state indicator, save button below fold", "ug": "Cognitive users, all users"},
        ],
        "nice_to_find": [
            {"desc": "Error messages use error codes (ERR_CSP_001) not human descriptions", "sev": "MINOR", "wcag": "3.3.1 Error Identification / Cognitive", "ev": "Error text shows 'ERR_CSP_001' with no human-readable message", "ug": "Cognitive users"},
            {"desc": "Required fields marked with tiny red asterisk only", "sev": "MINOR", "wcag": "1.4.1 Use of Color", "ev": "Red asterisk is sole required indicator — color + tiny size", "ug": "Color-blind users, low-vision users"},
        ],
        "fp_traps": [
            {"desc": "All toggles are native checkbox elements with labels", "note": "Keyboard and screen reader accessible — do not flag"},
            {"desc": "Focus styles present on all interactive elements", "note": "Correct implementation — do not flag"},
        ],
        "scores": {"A": "25-35", "B": "45-55", "C": "75-85"},
        "verdict": "REVISE",
    },
    {
        "id": "chat-cognitive-load",
        "name": "Chat Interface With Cognitive Overload Patterns",
        "category": "HAS-BUGS",
        "domain": "Interactive Widgets",
        "primary": "cognitive_neurodivergent",
        "secondary": "vestibular_motion",
        "description": "React chat/messaging interface with auto-scrolling message stream, animated typing indicator without reduced-motion guard, color-flash-only new message notification, and emoji picker lacking keyboard grid navigation.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "MEDIUM", "auditory_access": "LOW", "keyboard_motor": "MEDIUM", "screen_reader_semantic": "LOW", "cognitive_neurodivergent": "HIGH"},
        "must_find": [
            {"desc": "Messages auto-scroll with no pause mechanism", "sev": "CRITICAL", "wcag": "2.2.2 Pause, Stop, Hide", "ev": "scrollIntoView called on every new message; no pause button", "ug": "Cognitive/attention users, vestibular users"},
            {"desc": "Typing indicator animated dots with no reduced-motion alternative", "sev": "MAJOR", "wcag": "2.3.1 Three Flashes / 2.3.3 Animation", "ev": "CSS @keyframes bounce on .typing-dot; no prefers-reduced-motion", "ug": "Vestibular users, cognitive/attention users"},
        ],
        "should_find": [
            {"desc": "New message notification uses only subtle color flash on tab", "sev": "MAJOR", "wcag": "1.4.1 Use of Color", "ev": "Tab title flashes color; no text badge, no sound option", "ug": "Color-blind users, users not watching tab"},
        ],
        "nice_to_find": [
            {"desc": "Message timestamps are relative and change while reading", "sev": "MINOR", "wcag": "Cognitive best practice", "ev": "'3m ago' text updates live, creating moving targets", "ug": "Cognitive/attention users"},
            {"desc": "Emoji picker has no keyboard grid navigation", "sev": "MINOR", "wcag": "2.1.1 Keyboard", "ev": "Arrow keys don't navigate emoji grid; only Tab moves between emojis", "ug": "Keyboard users"},
        ],
        "fp_traps": [
            {"desc": "Send button is keyboard accessible with proper label", "note": "Correct — do not flag"},
            {"desc": "Message input has proper label and aria-describedby", "note": "Correct — do not flag"},
            {"desc": "Chat area has aria-live='polite' for new messages", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "30-40", "B": "50-60", "C": "75-85"},
        "verdict": "REVISE",
    },
    {
        "id": "multi-column-pricing",
        "name": "Pricing Comparison Table With Color-Only Feature Indicators",
        "category": "HAS-BUGS",
        "domain": "Content & Layout",
        "primary": "environmental_contrast",
        "secondary": "cognitive_neurodivergent",
        "description": "React pricing comparison table with 3-4 tiers where feature availability is shown by green checkmark vs red X (color-only, both pass contrast), 'Recommended' tier highlighted by background color only, and feature tooltips on hover only.",
        "alarms": {"magnification_reflow": "MEDIUM", "environmental_contrast": "HIGH", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "MEDIUM"},
        "must_find": [
            {"desc": "Feature availability shown by green check vs red X — color-only", "sev": "CRITICAL", "wcag": "1.4.1 Use of Color", "ev": "Check/X icons use color alone; both pass contrast ratio checks", "ug": "Color-blind users, monochrome display users"},
            {"desc": "'Recommended' tier highlighted with background color only", "sev": "MAJOR", "wcag": "1.4.1 Use of Color", "ev": "No text badge, no border — only background-color distinguishes recommended", "ug": "Color-blind users"},
        ],
        "should_find": [
            {"desc": "Pricing text 12px gray #767676 on white — 4.54:1, borderline contrast", "sev": "MAJOR", "wcag": "1.4.3 Contrast (Minimum)", "ev": "Price text at 12px uses #767676 — 4.54:1 passes AA for large text but not for body text at this size", "ug": "Low-vision users"},
        ],
        "nice_to_find": [
            {"desc": "Feature comparison tooltips on hover only, no focus equivalent", "sev": "MINOR", "wcag": "1.4.13 Content on Hover or Focus", "ev": "CSS :hover shows tooltip; no :focus rule", "ug": "Keyboard users"},
            {"desc": "'Most popular' badge uses animated shimmer, no reduced-motion", "sev": "MINOR", "wcag": "2.3.3 Animation from Interactions", "ev": "@keyframes shimmer on .popular-badge; no media query guard", "ug": "Vestibular users"},
        ],
        "fp_traps": [
            {"desc": "Table has proper thead/tbody/th with scope", "note": "Correct semantics — do not flag"},
            {"desc": "CTA buttons are real buttons with descriptive labels", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "30-40", "B": "55-65", "C": "80-90"},
        "verdict": "REVISE",
    },
    {
        "id": "data-viz-color-encoding",
        "name": "Data Visualization With Color-Only Series Encoding",
        "category": "HAS-BUGS",
        "domain": "Data Display",
        "primary": "environmental_contrast",
        "secondary": "screen_reader_semantic",
        "description": "React SVG bar/pie chart with 5 color-coded data series distinguished only by fill color — no pattern fills, no direct labels. Legend uses small colored squares only. Hover tooltips have no keyboard equivalent.",
        "alarms": {"magnification_reflow": "MEDIUM", "environmental_contrast": "HIGH", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "MEDIUM", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "LOW"},
        "must_find": [
            {"desc": "5 data series distinguished only by fill color — no patterns or labels", "sev": "CRITICAL", "wcag": "1.4.1 Use of Color", "ev": "SVG rect elements use fill color as sole differentiator", "ug": "Color-blind users, monochrome display users"},
            {"desc": "Hover tooltips on SVG bars with no keyboard/focus equivalent", "sev": "MAJOR", "wcag": "2.1.1 Keyboard / 1.4.13 Content on Hover", "ev": "onMouseEnter shows tooltip; no focus handler on SVG elements", "ug": "Keyboard users"},
        ],
        "should_find": [
            {"desc": "Legend uses small colored squares only, no text-shape mapping", "sev": "MAJOR", "wcag": "1.4.1 Use of Color", "ev": "Legend items: colored div + text label, but color is sole series identifier", "ug": "Color-blind users"},
        ],
        "nice_to_find": [
            {"desc": "Chart title in SVG with no accessible name on svg element", "sev": "MINOR", "wcag": "1.1.1 Non-text Content", "ev": "svg element has no role='img' or aria-label", "ug": "Screen reader users"},
            {"desc": "Y-axis labels at 10px font size", "sev": "MINOR", "wcag": "1.4.4 Resize Text", "ev": "SVG text elements at font-size 10px", "ug": "Low-vision users"},
        ],
        "fp_traps": [
            {"desc": "SVG colors all pass contrast against white background", "note": "Contrast ratio is fine — the issue is color-ONLY encoding, not contrast"},
            {"desc": "Page heading structure and landmarks are correct", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "30-40", "B": "50-60", "C": "80-90"},
        "verdict": "REVISE",
    },
    {
        "id": "animated-onboarding-flow",
        "name": "Animated Onboarding Wizard With Unguarded Transitions",
        "category": "HAS-BUGS",
        "domain": "Interactive Widgets",
        "primary": "vestibular_motion",
        "secondary": "cognitive_neurodivergent",
        "description": "React multi-step onboarding wizard with full-viewport slide transitions, confetti celebration, progress bar animation, and bouncing step icons — all without prefers-reduced-motion guards.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "HIGH", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "LOW", "cognitive_neurodivergent": "MEDIUM"},
        "must_find": [
            {"desc": "Full-viewport slide transitions with no prefers-reduced-motion", "sev": "CRITICAL", "wcag": "2.3.1 Three Flashes or Below Threshold", "ev": "translateX(100%) transition with no @media (prefers-reduced-motion)", "ug": "Vestibular disorder users"},
            {"desc": "Confetti particle animation — 200+ moving elements for 3 seconds", "sev": "CRITICAL", "wcag": "2.3.1 Three Flashes", "ev": "Canvas confetti with no reduced-motion check", "ug": "Vestibular users, photosensitive users"},
        ],
        "should_find": [
            {"desc": "Progress bar smooth-scrolling fill animation, no reduced-motion", "sev": "MAJOR", "wcag": "2.3.3 Animation from Interactions", "ev": "CSS transition on .progress-fill width; no media query guard", "ug": "Vestibular users"},
            {"desc": "Step icons bounce/scale on activation, no reduced-motion guard", "sev": "MAJOR", "wcag": "2.3.3 Animation from Interactions", "ev": "@keyframes bounce on .step-icon.active; no media query", "ug": "Vestibular users, cognitive/attention users"},
        ],
        "nice_to_find": [
            {"desc": "Background gradient shift animation on each step", "sev": "MINOR", "wcag": "2.3.3 Animation from Interactions", "ev": "CSS transition on background gradient; subtle but continuous", "ug": "Vestibular users"},
        ],
        "fp_traps": [
            {"desc": "Next/Back buttons properly labeled with aria-label", "note": "Correct — do not flag"},
            {"desc": "Step content uses headings, form fields have labels", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "25-35", "B": "50-60", "C": "85-95"},
        "verdict": "REVISE",
    },
    {
        "id": "image-gallery-small-targets",
        "name": "Image Gallery With Undersized Touch Targets",
        "category": "HAS-BUGS",
        "domain": "Interactive Widgets",
        "primary": "magnification_reflow",
        "secondary": "keyboard_motor",
        "description": "React image gallery with 32x32px thumbnail grid, 16x16px lightbox close button, 20x20px zoom controls, and horizontal overflow at 200% zoom.",
        "alarms": {"magnification_reflow": "HIGH", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "MEDIUM", "screen_reader_semantic": "LOW", "cognitive_neurodivergent": "LOW"},
        "must_find": [
            {"desc": "Thumbnails 32x32px with 2px gap — below WCAG 2.5.8 minimum", "sev": "CRITICAL", "wcag": "2.5.8 Target Size (Minimum)", "ev": ".thumbnail { width: 32px; height: 32px; margin: 2px }", "ug": "Motor impairment users, touch users"},
            {"desc": "Lightbox close button 16x16px — tiny target", "sev": "MAJOR", "wcag": "2.5.8 Target Size (Minimum)", "ev": ".close-btn { width: 16px; height: 16px; padding: 0 }", "ug": "Motor impairment users"},
        ],
        "should_find": [
            {"desc": "Zoom in/out buttons 20x20px with no padding", "sev": "MAJOR", "wcag": "2.5.8 Target Size (Minimum)", "ev": ".zoom-btn { width: 20px; height: 20px }", "ug": "Motor users, touch users"},
        ],
        "nice_to_find": [
            {"desc": "At 200% zoom, thumbnail grid overflows horizontally", "sev": "MINOR", "wcag": "1.4.10 Reflow", "ev": "Grid uses fixed widths; no flex-wrap at zoom", "ug": "Magnification users"},
            {"desc": "Lightbox nav arrows clipped at zoom levels", "sev": "MINOR", "wcag": "1.4.10 Reflow", "ev": "Arrows positioned at viewport edge; overflow: hidden", "ug": "Magnification users"},
        ],
        "fp_traps": [
            {"desc": "All buttons are real button elements", "note": "Correct — do not flag"},
            {"desc": "Images have alt text", "note": "Correct — do not flag"},
            {"desc": "Lightbox traps focus correctly, Escape closes", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "35-45", "B": "45-55", "C": "80-90"},
        "verdict": "REVISE",
    },
    {
        "id": "map-interface-zoom",
        "name": "Interactive Map With Mouse-Only Navigation",
        "category": "HAS-BUGS",
        "domain": "Interactive Widgets",
        "primary": "magnification_reflow",
        "secondary": "keyboard_motor",
        "description": "React interactive map with mouse-drag-only panning, undersized zoom controls, controls overlapping at 200% zoom, and hover-only info popups on markers.",
        "alarms": {"magnification_reflow": "HIGH", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "LOW"},
        "must_find": [
            {"desc": "Map panning relies on mouse drag only — no keyboard alternative", "sev": "CRITICAL", "wcag": "2.1.1 Keyboard", "ev": "onMouseDown/Move/Up handlers; no arrow key handlers for panning", "ug": "Keyboard users, switch users"},
            {"desc": "Zoom +/- buttons 18x18px — below minimum target size", "sev": "MAJOR", "wcag": "2.5.8 Target Size (Minimum)", "ev": ".zoom-control { width: 18px; height: 18px }", "ug": "Motor impairment users"},
        ],
        "should_find": [
            {"desc": "At 200% zoom, map controls overlap and become unusable", "sev": "MAJOR", "wcag": "1.4.10 Reflow", "ev": "Controls use position: absolute with fixed px; overlap at zoom", "ug": "Magnification users"},
            {"desc": "Info popup on marker hover only — no focus/click alternative", "sev": "MAJOR", "wcag": "1.4.13 Content on Hover or Focus / 2.1.1 Keyboard", "ev": "onMouseEnter shows popup; no focus/click handler", "ug": "Keyboard users, touch users"},
        ],
        "nice_to_find": [
            {"desc": "Scroll wheel zoom hijacks page scroll without escape", "sev": "MINOR", "wcag": "2.5.3 Label in Name", "ev": "onWheel prevents default; no way to pass through to page", "ug": "All users scrolling past the map"},
        ],
        "fp_traps": [
            {"desc": "Map container has role='application'", "note": "Correct for complex widget — do not flag"},
            {"desc": "Zoom buttons are real button elements", "note": "Correct — do not flag"},
            {"desc": "Location search input has proper label", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "40-50", "B": "50-60", "C": "75-85"},
        "verdict": "REVISE",
    },
    # ─── HAS-BUGS: Existing Dimensions (regression) ────────────
    {
        "id": "custom-select-combobox",
        "name": "Custom Select Combobox Without Keyboard Navigation",
        "category": "HAS-BUGS",
        "domain": "Interactive Widgets",
        "primary": "keyboard_motor",
        "secondary": "screen_reader_semantic",
        "regression": True,
        "description": "React custom select/combobox dropdown with search filtering. Arrow keys don't navigate options, no ARIA roles, no aria-selected, Escape doesn't close.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "HIGH", "cognitive_neurodivergent": "LOW"},
        "must_find": [
            {"desc": "Arrow keys don't navigate options — only Tab works", "sev": "CRITICAL", "wcag": "2.1.1 Keyboard", "ev": "No onKeyDown handler for ArrowUp/ArrowDown", "ug": "Keyboard users, switch users"},
            {"desc": "No role='combobox' or role='listbox' — div soup", "sev": "CRITICAL", "wcag": "4.1.2 Name, Role, Value", "ev": "Options container is plain div with no ARIA role", "ug": "Screen reader users"},
        ],
        "should_find": [
            {"desc": "Selected option not announced — no aria-selected or activedescendant", "sev": "MAJOR", "wcag": "4.1.2 Name, Role, Value", "ev": "No aria-selected on options; no aria-activedescendant on input", "ug": "Screen reader users"},
        ],
        "nice_to_find": [
            {"desc": "Escape doesn't close dropdown", "sev": "MINOR", "wcag": "APG Combobox pattern", "ev": "No Escape key handler in onKeyDown", "ug": "Keyboard users"},
            {"desc": "No live region announces filtered count", "sev": "MINOR", "wcag": "4.1.3 Status Messages", "ev": "Filter changes option count visually but no aria-live", "ug": "Screen reader users"},
        ],
        "fp_traps": [
            {"desc": "Visual focus indicator exists on options", "note": "Correct — do not flag"},
            {"desc": "Label is associated with the input", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "70-85", "B": "70-85", "C": "75-90"},
        "verdict": "REVISE",
    },
    {
        "id": "search-results-dynamic-update",
        "name": "Search Results With No Live Region Announcements",
        "category": "HAS-BUGS",
        "domain": "Dynamic Content",
        "primary": "screen_reader_semantic",
        "secondary": "cognitive_neurodivergent",
        "regression": True,
        "description": "React search interface with real-time results updating as user types. No aria-live on results, no 'N results found' announcement, loading spinner is CSS-only with no accessible text.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "HIGH", "cognitive_neurodivergent": "MEDIUM"},
        "must_find": [
            {"desc": "No aria-live on results container — SR users unaware results changed", "sev": "CRITICAL", "wcag": "4.1.3 Status Messages", "ev": "Results container div has no aria-live attribute", "ug": "Screen reader users"},
            {"desc": "'N results found' count updates visually but no live announcement", "sev": "MAJOR", "wcag": "4.1.3 Status Messages", "ev": "Count text updates on render; no aria-live wrapping it", "ug": "Screen reader users"},
        ],
        "should_find": [
            {"desc": "Loading spinner CSS-only — no aria-busy, no accessible text", "sev": "MAJOR", "wcag": "4.1.3 Status Messages", "ev": "Spinner is CSS animation; no aria-busy on container, no sr-only text", "ug": "Screen reader users"},
        ],
        "nice_to_find": [
            {"desc": "Search input type='text' not type='search'", "sev": "MINOR", "wcag": "Semantic HTML best practice", "ev": "<input type='text'> instead of type='search'", "ug": "Screen reader users"},
            {"desc": "Clear search button '×' has no aria-label", "sev": "MINOR", "wcag": "4.1.2 Name, Role, Value", "ev": "Button contains only '×' text, no aria-label", "ug": "Screen reader users"},
        ],
        "fp_traps": [
            {"desc": "Results are in a landmark region with aria-label", "note": "Correct — do not flag"},
            {"desc": "Each result card has heading", "note": "Correct — do not flag"},
            {"desc": "Keyboard navigation between results works", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "70-80", "B": "70-80", "C": "75-85"},
        "verdict": "REVISE",
    },
    {
        "id": "tab-panel-arrow-keys",
        "name": "Tab Panel Without Arrow Key Navigation",
        "category": "HAS-BUGS",
        "domain": "Interactive Widgets",
        "primary": "keyboard_motor",
        "secondary": "screen_reader_semantic",
        "regression": True,
        "description": "React tabs component where Arrow Left/Right don't switch tabs (only Tab key works), no ARIA roles, no aria-selected, no aria-controls.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "HIGH", "cognitive_neurodivergent": "LOW"},
        "must_find": [
            {"desc": "No Arrow Left/Right — only Tab key switches panels", "sev": "CRITICAL", "wcag": "2.1.1 Keyboard", "ev": "No ArrowLeft/ArrowRight in onKeyDown handler", "ug": "Keyboard users"},
            {"desc": "No role='tablist'/role='tab'/role='tabpanel'", "sev": "MAJOR", "wcag": "4.1.2 Name, Role, Value", "ev": "Container is div, tabs are buttons with no role", "ug": "Screen reader users"},
        ],
        "should_find": [
            {"desc": "No aria-selected on active tab, no aria-controls linking tab to panel", "sev": "MAJOR", "wcag": "4.1.2 Name, Role, Value", "ev": "Active tab has CSS class only, no aria-selected; no aria-controls", "ug": "Screen reader users"},
        ],
        "nice_to_find": [
            {"desc": "Home/End keys don't jump to first/last tab", "sev": "MINOR", "wcag": "APG Tabs pattern", "ev": "No Home/End key handlers", "ug": "Keyboard users"},
            {"desc": "Tab panel has no aria-labelledby pointing to its tab", "sev": "MINOR", "wcag": "4.1.2 Name, Role, Value", "ev": "Panel div has no aria-labelledby", "ug": "Screen reader users"},
        ],
        "fp_traps": [
            {"desc": "Visual active tab indicator is present", "note": "Correct — do not flag"},
            {"desc": "Content shows/hides correctly on tab change", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "75-85", "B": "75-85", "C": "80-90"},
        "verdict": "REVISE",
    },
    # ─── CLEAN ──────────────────────────────────────────────────
    {
        "id": "login-form-clean",
        "name": "Login Form With Complete Accessibility (CLEAN)",
        "category": "CLEAN",
        "domain": "Form & Validation",
        "primary": "all",
        "secondary": "all",
        "description": "React login form with email, password, remember-me, and forgot-password link. All labels matched, aria-describedby on errors, role='alert', aria-invalid, aria-required, autocomplete, visible focus styles.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "LOW", "cognitive_neurodivergent": "MEDIUM"},
        "must_find": [],
        "should_find": [],
        "nice_to_find": [
            {"desc": "Could add aria-live='polite' to error summary region", "sev": "ENHANCEMENT", "wcag": "4.1.3 Status Messages", "ev": "Error summary updates on submit but has no live region", "ug": "Screen reader users"},
            {"desc": "Could add show/hide password toggle for usability", "sev": "ENHANCEMENT", "wcag": "Cognitive best practice", "ev": "No password visibility toggle", "ug": "Cognitive users"},
        ],
        "fp_traps": [
            {"desc": "type='password' on password field — correct, not a bug", "note": "Standard password field"},
            {"desc": "autocomplete='current-password' — correct usage", "note": "Proper autocomplete attribute"},
            {"desc": "'Remember me' checkbox without fieldset — acceptable as single checkbox", "note": "Fieldset not required for single checkbox"},
        ],
        "scores": {"A": "75-88", "B": "70-85", "C": "80-95"},
        "verdict": "ACCEPT",
    },
    {
        "id": "nav-menu-landmarks",
        "name": "Navigation Menu With Complete Landmarks (CLEAN)",
        "category": "CLEAN",
        "domain": "Navigation",
        "primary": "all",
        "secondary": "all",
        "description": "React site navigation with primary nav, breadcrumb with aria-current, sidebar, skip links, and all landmarks correctly labeled.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "LOW"},
        "must_find": [],
        "should_find": [],
        "nice_to_find": [
            {"desc": "Could add aria-expanded on mobile menu toggle (desktop has no toggle)", "sev": "ENHANCEMENT", "wcag": "4.1.2 Name, Role, Value", "ev": "No mobile menu toggle visible in desktop view", "ug": "Screen reader users on mobile"},
        ],
        "fp_traps": [
            {"desc": "Multiple nav elements on page — correct with distinct aria-labels", "note": "Correct — each nav has unique label"},
            {"desc": "aria-current='page' on breadcrumb — correct", "note": "Standard breadcrumb pattern"},
            {"desc": "aside element for sidebar — correct landmark", "note": "Proper use of aside"},
        ],
        "scores": {"A": "78-90", "B": "75-88", "C": "82-95"},
        "verdict": "ACCEPT",
    },
    {
        "id": "media-player-captions",
        "name": "Media Player With Full Caption Support (CLEAN)",
        "category": "CLEAN",
        "domain": "Media & Content",
        "primary": "all",
        "secondary": "all",
        "description": "React video player with captions track (default), audio descriptions track, transcript section, all keyboard-accessible controls, role='toolbar', poster with alt, and reduced-motion handling.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "MEDIUM", "keyboard_motor": "LOW", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "LOW"},
        "must_find": [],
        "should_find": [],
        "nice_to_find": [
            {"desc": "Could add chapter markers for long video navigation", "sev": "ENHANCEMENT", "wcag": "2.4.5 Multiple Ways", "ev": "No chapter navigation for video", "ug": "Cognitive users, all users"},
            {"desc": "Could add playback speed control", "sev": "ENHANCEMENT", "wcag": "Cognitive best practice", "ev": "No speed adjustment", "ug": "Cognitive users, second-language users"},
        ],
        "fp_traps": [
            {"desc": "autoplay={false} — correct, no autoplay", "note": "Not autoplay — do not flag"},
            {"desc": "Caption track has default attribute — correct", "note": "Captions show by default — correct"},
            {"desc": "Video element has tabIndex={-1}", "note": "Correct — controls receive focus, not video element"},
        ],
        "scores": {"A": "75-88", "B": "72-85", "C": "80-95"},
        "verdict": "ACCEPT",
    },
    {
        "id": "dashboard-text-labels",
        "name": "Analytics Dashboard With Text Status Labels (CLEAN)",
        "category": "CLEAN",
        "domain": "Data Display",
        "primary": "all",
        "secondary": "all",
        "description": "React analytics dashboard with stat cards, bar chart with text labels on each bar, and data table. Status uses text+icons (not color-only), contrast meets AA, layout reflows, reduced-motion respected.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "MEDIUM", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "LOW", "screen_reader_semantic": "LOW", "cognitive_neurodivergent": "MEDIUM"},
        "must_find": [],
        "should_find": [],
        "nice_to_find": [
            {"desc": "Could add data table alternative view for the chart", "sev": "ENHANCEMENT", "wcag": "1.1.1 Non-text Content", "ev": "Chart data not available as accessible table", "ug": "Screen reader users"},
            {"desc": "Could add high-contrast mode toggle", "sev": "ENHANCEMENT", "wcag": "1.4.11 Non-text Contrast", "ev": "No contrast mode toggle", "ug": "Low-vision users"},
        ],
        "fp_traps": [
            {"desc": "Status uses both text AND color — not color-only", "note": "Correct — text labels present alongside color"},
            {"desc": "Chart animation respects prefers-reduced-motion", "note": "Correct — media query present"},
            {"desc": "Table has role='table' (redundant but harmless)", "note": "Do not flag — redundant but not incorrect"},
        ],
        "scores": {"A": "78-90", "B": "75-88", "C": "82-95"},
        "verdict": "ACCEPT",
    },
    # ─── ADVERSARIAL ────────────────────────────────────────────
    {
        "id": "infinite-scroll-cognitive",
        "name": "Infinite Scroll Feed With Cognitive Navigation Breakdown",
        "category": "ADVERSARIAL",
        "domain": "Dynamic Content",
        "primary": "cognitive_neurodivergent",
        "secondary": "keyboard_motor",
        "description": "React infinite scroll feed with no position indicator, no 'load more' alternative, virtual scrolling that removes offscreen DOM nodes, and relative timestamps that change while reading.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "HIGH"},
        "must_find": [
            {"desc": "No position indicator, no 'back to top', no page numbers", "sev": "CRITICAL", "wcag": "2.4.8 Location / Cognitive", "ev": "No feed position UI; no way to know where user is in content", "ug": "Cognitive users, all users"},
            {"desc": "Auto-loads content on scroll — no 'Load more' button alternative", "sev": "MAJOR", "wcag": "2.2.2 Pause, Stop, Hide / 2.1.1 Keyboard", "ev": "IntersectionObserver auto-fetches; no explicit load button; keyboard users trapped in infinite Tab", "ug": "Keyboard users, cognitive users"},
        ],
        "should_find": [
            {"desc": "Virtual scrolling removes offscreen DOM nodes — user loses position on Tab backward", "sev": "MAJOR", "wcag": "2.4.3 Focus Order", "ev": "Previously focused elements removed from DOM; focus reset on backward navigation", "ug": "Keyboard users, screen reader users"},
        ],
        "nice_to_find": [
            {"desc": "Relative timestamps change during reading", "sev": "MINOR", "wcag": "Cognitive best practice", "ev": "'2h ago' updates to '3h ago' while user reads", "ug": "Cognitive/attention users"},
            {"desc": "No 'end of feed' indicator", "sev": "MINOR", "wcag": "Cognitive best practice", "ev": "Feed appears infinite; no empty state or end message", "ug": "Cognitive users"},
        ],
        "fp_traps": [
            {"desc": "Each card has proper heading and image alt text", "note": "Correct — do not flag"},
            {"desc": "Landmark regions are present", "note": "Correct — do not flag"},
            {"desc": "aria-live='polite' on new content announcements", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "30-40", "B": "45-55", "C": "75-85"},
        "verdict": "REVISE",
    },
    {
        "id": "hover-reveal-navigation",
        "name": "Mega-Menu Navigation With Hover-Only Submenus",
        "category": "ADVERSARIAL",
        "domain": "Navigation",
        "primary": "keyboard_motor",
        "secondary": "cognitive_neurodivergent",
        "description": "React mega-menu where submenus appear on mouseenter only — no keyboard trigger despite focusable parent links. No hover grace period, no Escape handler, and submenu animation without reduced-motion check.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "MEDIUM"},
        "must_find": [
            {"desc": "Submenus appear on mouseenter only — no keyboard trigger", "sev": "CRITICAL", "wcag": "2.1.1 Keyboard", "ev": "onMouseEnter shows submenu; no onFocus or onKeyDown handler", "ug": "Keyboard users, switch users"},
            {"desc": "Submenu disappears with no hover grace period", "sev": "MAJOR", "wcag": "1.4.13 Content on Hover or Focus", "ev": "onMouseLeave immediately hides; no delay or grace zone", "ug": "Motor impairment users, magnification users"},
        ],
        "should_find": [
            {"desc": "No Escape key handler to close open submenu", "sev": "MAJOR", "wcag": "1.4.13 Content on Hover or Focus", "ev": "No onKeyDown handler for Escape on submenu", "ug": "Keyboard users"},
        ],
        "nice_to_find": [
            {"desc": "Submenu slide-down animation without reduced-motion check", "sev": "MINOR", "wcag": "2.3.3 Animation from Interactions", "ev": "200ms slide-down transition; no prefers-reduced-motion", "ug": "Vestibular users"},
            {"desc": "Submenu items not wrapped in role='menu'", "sev": "MINOR", "wcag": "4.1.2 Name, Role, Value", "ev": "Nested links in div, no menu role", "ug": "Screen reader users"},
        ],
        "fp_traps": [
            {"desc": "Top-level nav items are proper links with descriptive text", "note": "Correct — do not flag"},
            {"desc": "aria-label on nav element", "note": "Correct — do not flag"},
            {"desc": "Skip link present and working", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "40-50", "B": "50-60", "C": "80-90"},
        "verdict": "REVISE",
    },
    {
        "id": "autocomplete-fast-timeout",
        "name": "Address Autocomplete With Fast Timeout and Double-Action Enter",
        "category": "ADVERSARIAL",
        "domain": "Form & Validation",
        "primary": "keyboard_motor",
        "secondary": "cognitive_neurodivergent",
        "description": "React address autocomplete where suggestions disappear after 800ms inactivity, Enter both selects suggestion AND submits form, suggestions list has no ARIA roles, and loading/empty states lack accessible announcements.",
        "alarms": {"magnification_reflow": "LOW", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "HIGH"},
        "must_find": [
            {"desc": "Suggestions disappear after 800ms inactivity — too fast for slow navigators", "sev": "CRITICAL", "wcag": "2.2.1 Timing Adjustable", "ev": "setTimeout(closeSuggestions, 800) on blur; no option to extend", "ug": "Motor impairment users, switch users, cognitive users"},
            {"desc": "Enter both selects suggestion AND submits form — double-action", "sev": "MAJOR", "wcag": "3.2.2 On Input", "ev": "Enter key handler selects option then calls form.submit()", "ug": "Keyboard users, cognitive users"},
        ],
        "should_find": [
            {"desc": "Suggestions list has no role='listbox' — SR can't announce as options", "sev": "MAJOR", "wcag": "4.1.2 Name, Role, Value", "ev": "Suggestions in plain div with no ARIA role", "ug": "Screen reader users"},
        ],
        "nice_to_find": [
            {"desc": "'No results' state shows italic gray text with no aria-live", "sev": "MINOR", "wcag": "4.1.3 Status Messages", "ev": "Empty state text rendered with no live announcement", "ug": "Screen reader users"},
            {"desc": "Loading spinner during fetch has no aria-busy or text", "sev": "MINOR", "wcag": "4.1.3 Status Messages", "ev": "CSS-only spinner; no aria-busy on container", "ug": "Screen reader users"},
        ],
        "fp_traps": [
            {"desc": "Input has proper label and aria-describedby instructions", "note": "Correct — do not flag"},
            {"desc": "Visible focus styles on input and suggestions", "note": "Correct — do not flag"},
        ],
        "scores": {"A": "35-45", "B": "50-60", "C": "75-85"},
        "verdict": "REVISE",
    },
]

CALIBRATION = [
    {
        "id": "calibration-animated-dashboard",
        "name": "Animated Dashboard (Calibration C4)",
        "archetype": "animated_data_display",
        "description": "React analytics dashboard with live-updating charts, animated counters, scrolling ticker, and color-coded alerts. Tests whether escalation correctly identifies many simultaneous HIGH perspectives.",
        "alarms": {"magnification_reflow": "MEDIUM", "environmental_contrast": "HIGH", "vestibular_motion": "HIGH", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "HIGH", "cognitive_neurodivergent": "MEDIUM"},
        "rationale": "This is the 'loud' fixture — almost everything is HIGH. Scrolling ticker + chart animations (Vestibular), color-coded alerts (Contrast), interactive charts (Keyboard), live data (Screen Reader). Tests whether escalation avoids flattening all perspectives to MEDIUM.",
    },
    {
        "id": "calibration-drag-drop-kanban",
        "name": "Drag-and-Drop Kanban Board (Calibration C5)",
        "archetype": "drag_drop_interactive",
        "description": "React kanban board with drag-and-drop columns (To Do, In Progress, Done) and card reordering. No keyboard alternative for drag. Tests keyboard + cognitive HIGH detection.",
        "alarms": {"magnification_reflow": "MEDIUM", "environmental_contrast": "LOW", "vestibular_motion": "LOW", "auditory_access": "LOW", "keyboard_motor": "HIGH", "screen_reader_semantic": "MEDIUM", "cognitive_neurodivergent": "HIGH"},
        "rationale": "Drag-and-drop without keyboard alternative is the canonical keyboard accessibility failure. Cognitive is HIGH due to spatial organization and multi-column state tracking. Tests specific pattern recognition.",
    },
]


def gen_metadata(spec):
    """Generate .metadata.yaml content for a main fixture."""
    is_regression = spec.get("regression", False)
    is_clean = spec["category"] == "CLEAN"

    lines = [
        f'fixture_id: {spec["id"]}',
        f'name: "{spec["name"]}"',
        f'description: >',
        f'  {spec["description"]}',
        f'language: jsx',
        f'framework: React',
        f'difficulty: {spec["category"]}',
        f'domain: {spec["domain"]}',
        f'work_type: component_review',
    ]

    if is_regression:
        lines.append("regression_fixture: true")
        lines.append(f'regression_note: "Tests existing-dimension strength. All conditions should score 70%+. C must not regress below A."')

    lines.append("")
    lines.append("expected_findings:")

    for cat, items in [("must_find", spec["must_find"]), ("should_find", spec["should_find"]), ("nice_to_find", spec["nice_to_find"])]:
        lines.append(f"  - category: {cat}")
        lines.append(f"    count: {len(items)}")
        if items:
            lines.append("    items:")
            for item in items:
                lines.append(f'      - description: "{item["desc"]}"')
                lines.append(f'        severity: {item["sev"]}')
                lines.append(f'        wcag: "{item["wcag"]}"')
                lines.append(f'        evidence: "{item["ev"]}"')
                lines.append(f'        user_group: "{item["ug"]}"')

    lines.append("")
    lines.append("perspectives_tested:")
    lines.append(f'  primary: "{spec["primary"]}"')
    lines.append(f'  secondary: "{spec["secondary"]}"')

    lines.append("")
    lines.append("expected_alarm_levels:")
    for k, v in spec["alarms"].items():
        lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("false_positive_traps:")
    lines.append(f"  count: {len(spec['fp_traps'])}")
    if spec["fp_traps"]:
        lines.append("  items:")
        for trap in spec["fp_traps"]:
            lines.append(f'    - description: "{trap["desc"]}"')
            lines.append(f'      note: "{trap["note"]}"')

    lines.append("")
    if is_clean:
        lines.append("expected_verdict: ACCEPT")
        lines.append("scoring_notes:")
        lines.append("  false_positive_weight: -2")
        lines.append("  critical_false_positive_penalty: -3")
    else:
        lines.append(f'expected_verdict: {spec["verdict"]}')

    lines.append("")
    lines.append(f'notes: "Generated fixture for {spec["category"]} category, primary perspective {spec["primary"]}."')

    return "\n".join(lines) + "\n"


def gen_rubric(spec):
    """Generate .rubric.yaml content for a main fixture."""
    is_regression = spec.get("regression", False)
    is_clean = spec["category"] == "CLEAN"

    lines = [
        f'fixture_id: {spec["id"]}',
        f'rubric_version: "1.0"',
        f'scoring_method: hybrid',
        f'hybrid_weights:',
        f'  rule_based: 0.7',
        f'  llm_judge: 0.3',
    ]

    if is_regression:
        lines.append("primary_metric: existing_dimension_tpr")

    lines.append("")
    lines.append("dimensions:")

    if is_clean:
        dims = [
            ("false_positive_trap", "False Positive Avoidance", -2),
            ("critical_false_positive", "Critical False Positive Penalty", -3),
            ("clean_recognition", "Clean Implementation Recognition", 3),
            ("false_positive_trap_recognition", "Known False Positive Trap Recognition", 2),
            ("nice_to_find", "Legitimate Enhancement Suggestions", 1),
            ("perspective_alarm_accuracy", "Perspective Alarm Level Accuracy", 2),
            ("format_compliance", "Format Compliance", 1),
        ]
    else:
        dims = [
            ("must_find", "Must-Find Issues", 3),
            ("should_find", "Should-Find Issues", 2),
            ("nice_to_find", "Nice-to-Find Issues", 1),
            ("false_positive_trap", "False Positive Avoidance", -2),
            ("evidence_quality", "Evidence Quality", 1),
            ("format_compliance", "Format Compliance", 1),
            ("perspective_coverage", "Perspective Coverage", 2),
        ]

    for did, dname, dweight in dims:
        lines.append(f"  - id: {did}")
        lines.append(f'    name: "{dname}"')
        lines.append(f"    weight: {dweight}")

    lines.append("")
    lines.append("scoring_thresholds:")
    lines.append("  excellent: 90-100")
    lines.append("  good: 75-89")
    lines.append("  adequate: 60-74")
    lines.append("  weak: 40-59")
    lines.append("  poor: 0-39")

    lines.append("")
    lines.append("expected_reviewer_performance:")
    for cond in ["A", "B", "C"]:
        labels = {"A": "Current skills (no perspectives)", "B": "Strong generic baseline", "C": "Enhanced skills with perspective audit"}
        lines.append(f"  - condition: {cond}")
        lines.append(f'    label: "{labels[cond]}"')
        lines.append(f'    expected_score: "{spec["scores"][cond]}"')

    lines.append("")
    verd = spec["verdict"]
    lines.append("verdict_expectations:")
    if is_clean:
        lines.append("  A: ACCEPT")
        lines.append("  B: ACCEPT")
        lines.append("  C: ACCEPT")
    elif is_regression:
        lines.append(f"  A: {verd}")
        lines.append(f"  B: {verd}")
        lines.append(f"  C: {verd}")
    else:
        lines.append(f"  A: {verd}")
        lines.append(f"  B: {verd}")
        lines.append(f"  C: {verd}")

    if is_regression:
        lines.append("")
        lines.append("non_inferiority_test:")
        lines.append("  metric: existing_dimension_tpr")
        lines.append('  comparison: "C >= A"')
        lines.append('  tolerance: "-5%"')
        lines.append('  pass_condition: "C_tpr >= A_tpr - 0.05"')

    lines.append("")
    lines.append(f'notes: "Generated rubric for {spec["id"]}. Category: {spec["category"]}."')

    return "\n".join(lines) + "\n"


def gen_calibration_metadata(spec):
    """Generate .metadata.yaml for calibration fixtures."""
    lines = [
        f'fixture_id: {spec["id"]}',
        f'name: "{spec["name"]}"',
        f'description: "{spec["description"]}"',
        f'type: calibration',
        f'archetype: {spec["archetype"]}',
        "",
        "expected_alarm_levels:",
    ]
    for k, v in spec["alarms"].items():
        lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("scoring:")
    lines.append("  method: alarm_level_accuracy")
    lines.append("  exact_match_score: 1.0")
    lines.append("  within_one_score: 0.5")
    lines.append("  off_by_two_score: 0.0")
    lines.append("  total_assessments: 7")
    lines.append("  passing_threshold_exact: 5")
    lines.append("  target_threshold_exact: 6")

    lines.append("")
    lines.append(f'rationale: |')
    lines.append(f'  {spec["rationale"]}')

    return "\n".join(lines) + "\n"


def main():
    fixtures_dir = os.path.join(BASE, "fixtures")
    rubrics_dir = os.path.join(BASE, "rubrics")
    calibration_dir = os.path.join(BASE, "calibration")

    created = []

    for spec in FIXTURES:
        meta_path = os.path.join(fixtures_dir, f'{spec["id"]}.metadata.yaml')
        rubric_path = os.path.join(rubrics_dir, f'{spec["id"]}.rubric.yaml')

        if not os.path.exists(meta_path):
            with open(meta_path, "w") as f:
                f.write(gen_metadata(spec))
            created.append(meta_path)

        if not os.path.exists(rubric_path):
            with open(rubric_path, "w") as f:
                f.write(gen_rubric(spec))
            created.append(rubric_path)

    for spec in CALIBRATION:
        meta_path = os.path.join(calibration_dir, f'{spec["id"]}.metadata.yaml')
        if not os.path.exists(meta_path):
            with open(meta_path, "w") as f:
                f.write(gen_calibration_metadata(spec))
            created.append(meta_path)

    print(f"Created {len(created)} files:")
    for p in created:
        print(f"  {os.path.relpath(p, BASE)}")


if __name__ == "__main__":
    main()
