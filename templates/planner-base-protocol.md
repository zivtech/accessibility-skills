# Planner Base Protocol Template
## Universal Skeleton for All Zivtech Planner Skills

This document defines the shared protocol that all domain-specific planner skills inherit from. Each planner (react-planner, drupal-planner, a11y-planner, plan-writer, etc.) implements this universal structure while adding domain-specific phases.

---

## Architecture

```
Planner Base Protocol
├── Phase 1: Scope & Context (universal)
├── Phase 2: Existing Architecture Analysis (universal)
├── Phase 3: {{DOMAIN_DESIGN}} (domain-specific placeholder)
│   ├── May expand to 1-5 phases depending on domain complexity
│   └── Each phase produces domain-specific outputs
├── Phase 4: Assumption Register (universal)
├── Phase 5: Test Strategy (universal)
├── Phase 6: Implementation Tasks (universal)
├── Phase 7: Review Checkpoint Plan (universal)
└── Output Format Contract (universal)
```

---

## Phase 1: Scope & Context (Universal)

**Purpose:** Establish clear boundaries, understand user needs, identify constraints.

**Inputs:** User request, project context

**Outputs:**
- Feature description (one sentence)
- Risk level classification (Low/Medium/High)
- Existing architecture summary
- Scope boundaries (in/out)

**Key Questions:**
1. What is being built? (One sentence)
2. What user need does it address?
3. What is the risk level?
   - Low: Isolated component, no cross-dependencies, proven patterns
   - Medium: Feature with state/dependencies, some uncertainty
   - High: Multi-component system, architectural implications, new territory
4. What is the consequence of wrong design? (Refactor cost, performance regression, security gap?)
5. What constraints exist?
   - Technology stack, browser compatibility, performance budgets
   - Team capability, timeline, third-party dependencies
6. What is the existing architecture (if modifying)?
   - What's already there? What conventions are established?
7. What is explicitly OUT of scope?

**Hard Gate:** Don't proceed without clear scope. If the user can't articulate what "correct" means, STOP and clarify.

---

## Phase 2: Existing Architecture Analysis (Universal)

**Purpose:** Understand current implementation before designing what's new.

**Inputs:** User's existing codebase/system (if modifying)

**Outputs:**
- Documented current state
- Identified patterns and conventions
- Pain points in current design
- Constraints imposed by existing code

**Key Questions:**
1. What exists today? (Read current implementation)
   - Code structure, components, modules, services
   - Data model, state management approach
   - Established patterns and conventions
2. What patterns are established?
   - Naming conventions, folder structure, API design patterns
   - Error handling strategy, testing approach
   - Styling/layout methodology
3. What are the pain points?
   - Hard-to-maintain code, performance issues, tight coupling
   - Missing error handling, unclear ownership
4. What anti-patterns should we avoid?
   - Common mistakes made in this codebase
   - Things that looked good initially but caused problems

**{{EXISTING_ANALYSIS}} Placeholder:**
This phase ends with a domain-specific investigation. Each domain adds:
- **React planner:** Component tree analysis, state management investigation, hook usage patterns
- **Drupal planner:** Entity type analysis, module landscape, permission model review
- **A11y planner:** Current accessibility audit, missing patterns, ARIA implementation review
- **Plan-writer:** Historical analysis of similar efforts, lessons learned

**Hard Gate:** No modification plan without understanding current architecture. Ignoring existing code leads to breaking conventions and creating inconsistency.

---

## Phase 3: {{DOMAIN_DESIGN}} (Domain-Specific Placeholder)

**Purpose:** Design the solution in the domain's language before implementation.

**Structure:** Varies by domain complexity
- Simple domain: 1 design phase (e.g., basic form)
- Medium domain: 2-3 design phases (e.g., React component with state)
- Complex domain: 4-5 design phases (e.g., Drupal multi-entity system with migrations)

**Required Interface:**

Each domain must define:

```
Phase 3[a]: [Domain-Specific Phase Name]
**Purpose:** [What this phase accomplishes]
**Outputs:**
- [Artifact 1: e.g., component tree diagram, entity relationship diagram, interaction patterns]
- [Artifact 2: e.g., state ownership map, permission model, focus management plan]
- [Artifact 3: e.g., performance budget, cache strategy, test strategy]
**Key Tables/Diagrams:**
- [Table/diagram showing relationships, ownership, design decisions]
**Verification:**
- Does every element have a one-sentence purpose?
- Is every design decision justified ("Why this design vs alternatives?")?
- Are all dependencies documented?
```

**Examples of Domain-Specific Phases:**

### React Planner Domain Design (3 phases)
- Phase 3a: Component Architecture (tree, responsibilities, props/events contracts)
- Phase 3b: State Ownership & Hook Composition (ownership map, hook dependency arrays)
- Phase 3c: Performance Budget & Next.js Boundaries (render performance, server/client split, cache strategy)

### Drupal Planner Domain Design (3 phases)
- Phase 3a: Data Model Design (entity types, fields, relationships)
- Phase 3b: Module Architecture & Config (contrib vs custom decisions, config schema, permissions)
- Phase 3c: Cache & Migration Strategy (cache tags/contexts, migration idempotency)

### A11y Planner Domain Design (4 phases)
- Phase 3a: Semantic Structure Plan (landmarks, heading hierarchy, form structure)
- Phase 3b: Interaction Pattern Design (map to APG patterns, keyboard model, ARIA)
- Phase 3c: Focus Management & State Communication (tab order, focus traps, state indicators)
- Phase 3d: Visual Accessibility & Content Strategy (contrast, alt text, link text, error messages)

### Plan-Writer Domain Design (2 phases)
- Phase 3a: Competing Alternatives Analysis (rate cost/risk/speed/maintainability)
- Phase 3b: Pre-Mortem Analysis (failure scenarios at day 1/month 1/month 6)

---

## Phase 4: Assumption Register (Universal)

**Purpose:** Explicitly document every assumption with fragility ratings.

**Outputs:** Assumption Register table

**Structure:**

| Assumption | Fragility | Evidence | Risk if Wrong | Mitigation |
|-----------|-----------|----------|--------------|-----------|
| [What we're betting on] | FRAGILE / MODERATE / ROBUST | [What evidence supports this?] | [What breaks if it's wrong?] | [What will we do to handle it?] |

**Definition of Fragility:**

- **ROBUST:** Evidence in code, data, or documentation. Everyone agrees. Risk: low.
  - Example: "We're using React" (it's in package.json)
  - Action: Include in implementation, no special handling needed

- **MODERATE:** Plausible and consistent with team experience, but untested.
  - Example: "API latency will be < 100ms" (seems reasonable based on similar APIs)
  - Action: Measure early in implementation. Include performance test in acceptance criteria.

- **FRAGILE:** Could easily be wrong; significant consequence if it is.
  - Example: "All users will enable notifications" (behavioral assumption, not guaranteed)
  - Action: Include validation checkpoint in implementation. Have fallback strategy.

**Required Content:**

Every planner must:
1. Extract at least 5-7 assumptions
2. Rate at least ONE assumption as FRAGILE (if nothing is fragile, you haven't looked hard enough)
3. For every FRAGILE assumption, specify:
   - Detection mechanism: "We'll know this is wrong if [signal]"
   - Mitigation strategy: "We'll respond by [action]"
   - Validation checkpoint: "Test this at [stage] with [test]"

**Examples:**

### React Planner Assumptions
| Assumption | Fragility | Evidence | Risk if Wrong | Mitigation |
|-----------|-----------|----------|--------------|-----------|
| State ownership in SearchHeader won't cause re-render waterfalls | FRAGILE | No measurement yet | Performance regression; component unusable at scale (100+ results) | Measure re-render frequency in React DevTools; create render budget test; checkpoint after SearchInput task |
| Custom hook dependency arrays are correct | FRAGILE | Designed before implementation | Stale closure bugs; hard-to-reproduce timing issues | Write unit tests for each custom hook; test with different prop/state combinations; code review focused on dependencies |
| Next.js RSC boundaries are performant enough | FRAGILE | Not measured in this codebase | Over-fetching; client-side rendering bottleneck | Measure First Contentful Paint and JS bundle size before/after; set performance budget (< 100ms CCP); checkpoint after Phase 3c |

### Drupal Planner Assumptions
| Assumption | Fragility | Evidence | Risk if Wrong | Mitigation |
|-----------|-----------|----------|--------------|-----------|
| Cache tag invalidation will bubble correctly from ProductReview to Product | MODERATE | Drupal docs show this works; haven't tested with custom entity refs | Stale product data in reviews | Write Kernel test for cache tag bubbling; test with simulated entity updates |
| All permissions can be enforced via hook_entity_access | FRAGILE | Not verified for field-level access; some cases might need custom access handler | Privilege escalation; information disclosure | Implement access handler for edge cases; security review checkpoint |
| Migration will be idempotent with source ID tracking | MODERATE | Standard Migrate API pattern | Duplicate data if migration re-runs | Test migration with re-run; verify no duplicates; include rollback test |

### Plan-Writer Assumptions
| Assumption | Fragility | Evidence | Risk if Wrong | Mitigation |
|-----------|-----------|----------|--------------|-----------|
| Team has capacity to deliver by deadline | FRAGILE | Not verified with PM or team | Schedule slip; pressure to cut scope | Confirm capacity before phase 1; include buffer for unknowns |
| API vendor X will deliver by month 2 | FRAGILE | Depends on vendor, not our control | Blocked on critical path; cascading delays | Establish fallback (use existing API or mock); weekly check-in with vendor; contingency plan in phase 2 |

**Hard Gate:** Assumption Register must exist BEFORE implementation tasks are defined. No implementation without explicit assumptions.

---

## Phase 5: Test Strategy (Universal)

**Purpose:** Design test approach before code (TDD rhythm).

**Outputs:** Testing plan with coverage levels and acceptance criteria

**Structure:**

Define testing at these levels:

### Level 1: Unit Tests
- What: Individual components, functions, hooks tested in isolation
- How: Mock external dependencies, test behavior
- Example: "SearchInput component test: user types → onSearch callback fires with text"

### Level 2: Integration Tests
- What: Multiple components working together, real interactions
- Example: "User types in SearchInput → fetch triggered → ResultsList renders with data"

### Level 3: E2E Tests
- What: Full user journeys in production-like environment
- Example: "User searches → views results → selects item → details load"

### Level 4: Acceptance Tests
- What: Does the feature meet requirements? Is it performant? Accessible?
- Example: "Search completes in < 100ms", "All results keyboard-navigable"

**{{TEST_DOMAIN}} Placeholder:**

Each domain adds specific test strategies:

- **React:** Component tests (RTL), integration tests (Playwright), accessibility tests (axe, keyboard), performance tests (render budget, bundle size)
- **Drupal:** Kernel tests (entity creation, relationships), Functional tests (forms, permissions), Migration tests (idempotency, rollback)
- **A11y:** Automated testing (axe-core), keyboard navigation tests (manual), screen reader tests (real tech), visual regression (focus, zoom, contrast)
- **Plan-Writer:** Assumption validation tests, dependency verification, rollback/recovery drills

**Required Content:**

For each level:
1. Define specific test cases
2. Identify test data (normal cases, edge cases, error cases)
3. Specify what should be mocked vs tested real
4. Define acceptance criteria (what makes a test pass)

**Example Test Strategy:**

```
## Test Strategy

### Unit Tests (React Component)
- SearchInput component:
  - Type text → onSearch not called (debounced)
  - Wait 300ms → onSearch called with text
  - isLoading=true → input disabled, spinner visible
  - Accessibility: aria-label present, onChange fires correctly

### Integration Tests
- SearchHeader + SearchInput + ResultsList:
  - Type → fetch triggered → results render
  - Filter toggle → ResultsList re-fetches
  - Pagination: click next → ResultsList scrolls, new page loads

### E2E Tests
- Full search flow:
  - Open search page
  - Type query → results load
  - Apply filters → see filtered results
  - Select result → detail page loads

### Acceptance Criteria
- Search completes in < 100ms on staging
- All results keyboard-navigable
- No re-render waterfalls (measure in DevTools)
- 200% zoom: layout reflows without horizontal scroll
```

**Hard Gate:** Test strategy defined before implementation. "We'll test after implementation" guarantees missed edge cases.

---

## Phase 6: Implementation Tasks (Universal)

**Purpose:** Break design into ordered, testable, reviewable tasks.

**Structure:**

Each task follows this format:

```yaml
---
wp_id: WP01
lane: planned
depends_on: []
acceptance_criteria:
  - "{{CRITIC_NAME}} verdict = ACCEPT or ACCEPT-WITH-RESERVATIONS"
  - "All CRITICAL findings resolved"
  - "[Feature-specific criteria]"
---

### Task N: [Task Name]

🔍 **Review checkpoint** — {{CRITIC_NAME}} should focus on: [specific areas]

**Files:** [Create/modify files list]

**Component/Entity/Module Structure:** [If applicable, show structure stub]

**What to build:** [Detailed description]
- Do X
- Implement Y with Z strategy
- Handle error case A
- Test behavior B

**Acceptance Criteria:**
- User action A → behavior B occurs
- Error scenario X → graceful handling Y
- Performance: < Nms, no waterfalls/stale closures/dangling refs
- Accessibility: keyboard navigable, screen reader announces state
- {{CRITIC_NAME}} review: all findings ACCEPT-WITH-RESERVATIONS or better

**TDD Rhythm:**
1. Write test first (describe desired behavior)
2. Verify test fails
3. Implement component/function
4. Verify test passes
5. Add accessibility/performance/error handling
6. Verify all tests still pass
7. Submit for {{CRITIC_NAME}} review checkpoint

**Estimated Complexity:** Simple / Medium / Complex

**Dependencies:** [What must be done first?]
```

**Required Content:**

For each task:
- Exact file paths (create, test, modify)
- Clear description of what to build (not "implement the thing", but detailed behavior)
- Component/entity/function signature (props interface, return type, parameters)
- Test cases (from acceptance perspective)
- Error handling strategy
- Performance/accessibility requirements
- Failure detection (how will we know if this is wrong?)
- {{CRITIC_NAME}} focus areas for review checkpoint

**Task Sequencing:**

1. **Dependency ordering:** Define which tasks must complete before others start
2. **Parallelization:** Identify tasks that can run in parallel
3. **Critical path:** Highlight tasks that block others
4. **Risk ordering:** Consider doing highest-risk tasks early (to fail fast)

**Example Task (React):**

```yaml
---
wp_id: WP01
lane: planned
depends_on: []
acceptance_criteria:
  - "react-critic verdict = ACCEPT or ACCEPT-WITH-RESERVATIONS"
  - "Test: user types → onSearch fires after 300ms debounce"
  - "Performance: onChange callback stable (useCallback)"
  - "Accessibility: input labeled, keyboard-operable"
---

### Task 1: SearchInput Component

🔍 **Review checkpoint** — react-critic should focus on: useCallback necessity, dependency array correctness, accessibility

**Files:**
- Create: src/components/SearchInput.tsx
- Create: src/components/SearchInput.test.tsx

**Component Signature:**
```typescript
interface SearchInputProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  isLoading?: boolean;
  debounceMs?: number;
}

export function SearchInput(props: SearchInputProps): JSX.Element
```

**What to build:**
- Input element with placeholder and disabled state
- onChange handler that debounces calls to onSearch
- useCallback to stabilize onChange callback (so it can be a dependency in parent)
- useEffect with cleanup for debounce timer
- aria-label for accessibility (or use label element)

**Acceptance Criteria:**
- User types text → onSearch NOT called immediately
- User types text, waits 300ms → onSearch called once with accumulated text
- isLoading=true → input disabled, shows spinner
- Tab focuses input, Space/Enter don't submit (not a form)
- Screen reader announces "Search input" label
- Callback is stable (no new function on each render)

**TDD Rhythm:**
1. Write RTL test: type text, wait 300ms, verify onSearch called
2. Run test, verify fails
3. Implement input with onChange, useRef for timer, useEffect for debounce
4. Run test, verify passes
5. Add aria-label test
6. Verify accessibility test passes
7. Performance check: is onChange stable? YES → add useCallback
8. Verify all tests pass
9. Submit for react-critic review

**Error Handling:**
- If parent unmounts while debounce timer pending: useEffect cleanup clears timer
- If onSearch throws: let error bubble (parent handles via error boundary)

**Performance Plan:**
- onChange is stable (useCallback) so SearchInput can be memoized if needed
- Debounce prevents excessive re-renders of parent
- Dependency array: [onSearch, debounceMs] (NOT function refs)

**Accessibility:**
- Input labeled (aria-label or associated label element)
- Type → debounced onSearch (good for REST API calls)
- No Enter submission (not a form input, unless parent wraps in <form>)

**Estimated Complexity:** Medium (hook dependencies, debounce cleanup)

**Dependencies:** None (can start immediately)
```

**spec-kitty Integration:**

If using spec-kitty for task tracking, the YAML frontmatter format is:

```yaml
---
wp_id: WP01
lane: planned
depends_on: []
acceptance_criteria:
  - "{{CRITIC_NAME}} verdict = ACCEPT or ACCEPT-WITH-RESERVATIONS"
  - "[Feature-specific criteria]"
---
```

Fields:
- `wp_id`: Unique identifier (WP01, WP02, etc.)
- `lane`: Status (planned, in_progress, done)
- `depends_on`: Array of wp_ids this task depends on
- `acceptance_criteria`: Array of specific, measurable criteria

**Hard Gate:** Implementation tasks must include {{CRITIC_NAME}} review checkpoints. Each checkpoint specifies exactly what the critic should verify.

---

## Phase 7: Review Checkpoint Plan (Universal)

**Purpose:** Define when to invoke companion critic during implementation.

**Outputs:** Review checkpoint table with timing and focus areas

**Structure:**

```markdown
## Review Checkpoint Plan

| Checkpoint | After Task | {{CRITIC_NAME}} Focus | Decision Gate |
|-----------|-----------|-------------------|--------------|
| 🔍 1 | Task N (Architecture complete) | [Specific focus areas] | ACCEPT or ACCEPT-WITH-RESERVATIONS required before proceeding |
| 🔍 2 | Task M (Core implementation) | [Specific focus areas] | Any CRITICAL findings must be fixed before continuing |
| 🔍 3 | Final submission | [Specific focus areas] | ACCEPT required for merge |
```

**Minimum Checkpoint Strategy:**

Every planner must include at least 3 checkpoints:

1. **After Architecture/Design is complete** (Phase 2-3)
   - Critic focus: Are assumptions sound? Is design correct before code?
   - Decision gate: ACCEPT or ACCEPT-WITH-RESERVATIONS required to proceed to implementation
   - Risk if skipped: Implement wrong architecture, expensive to fix later

2. **After Core Implementation** (Phase 6, midway through tasks)
   - Critic focus: Are critical components/entities/systems correct?
   - Decision gate: CRITICAL findings must be fixed before continuing
   - Risk if skipped: Uncover fundamental issues late, require major rework

3. **Before Merge/Deployment** (Phase 6, final)
   - Critic focus: Overall quality, completeness, adherence to design
   - Decision gate: ACCEPT required (or explicit approval for reservations)
   - Risk if skipped: Ship bugs, incomplete implementation, technical debt

**Companion Critic Routing:**

Each domain has a specific critic. Use the {{CRITIC_NAME}} placeholder:

- **React planner:** Invoke `react-critic`
- **Drupal planner:** Invoke `drupal-critic`
- **A11y planner:** Invoke `a11y-critic` (or `accessibility-testing`, `a11y-test`)
- **Plan-writer:** Invoke `proposal-critic`

**Critic Focus Guidelines:**

Define explicitly what each checkpoint should verify:

```markdown
🔍 **Checkpoint 1: After Component Architecture Design**

**react-critic focus:**
- Component tree is correct (parent-child relationships, data flow)
- Every component has a one-sentence responsibility
- State ownership justified ("Why does X own this state?")
- Props interfaces are complete (no missing types)
- Custom hook dependencies are designed before implementation

🔍 **Checkpoint 2: After SearchInput & ResultsList Implementation**

**react-critic focus:**
- useCallback on callbacks is justified (not premature optimization)
- Dependency arrays are correct (no stale closures)
- React.memo decisions justified (performance measured, not speculative)
- Error handling complete (timeout, offline, server error)
- Accessibility tests pass (keyboard navigation, screen reader)

🔍 **Checkpoint 3: Final Implementation Review**

**react-critic focus:**
- All components meet their responsibility statement
- No re-render waterfalls (performance budget achieved)
- All FRAGILE assumptions validated (via tests)
- Integration tests pass
- E2E tests pass
- Ready for production
```

**Decision Gates:**

Each checkpoint must specify:
- What verdict is required (ACCEPT, ACCEPT-WITH-RESERVATIONS, REVISE)
- What happens if verdict is not met
- Can work continue? (CRITICAL findings block, MAJOR findings slow, MINOR findings noted)

**Example Decision Gate:**

```markdown
🔍 **Checkpoint 1: Architecture Review**

**Verdict required:** ACCEPT or ACCEPT-WITH-RESERVATIONS

**If REVISE:**
- Fix architectural issues identified
- Re-submit to react-critic before proceeding to implementation

**If ACCEPT-WITH-RESERVATIONS:**
- Note the reservations
- Create follow-up tasks to address them
- Can proceed to implementation with those tasks on the roadmap

**If ACCEPT:**
- Proceed to implementation tasks immediately
```

**Hard Gate:** Every plan must include review checkpoints. No implementation without explicit verification strategy.

---

## Output Format Contract (Universal)

Every planner produces output in this format:

```markdown
# [Feature Name] {{DOMAIN}} Implementation Plan

> **For Claude:** Use {{PLANNER_NAME}} protocol. Invoke {{CRITIC_NAME}} at each checkpoint marked with 🔍.
> **Framework/Stack:** [Framework version or domain specification]
> **Companion skills:** [Comma-separated list of skills to use if available]

**Feature:** [One sentence describing what we're building]
**Risk Level:** Low / Medium / High
**Existing Architecture:** [Brief summary of current state]

---

## Feature Overview

[2-3 paragraphs describing the feature, user need, approach, key decisions]

## {{DOMAIN_DESIGN_SECTIONS}}

[Domain-specific sections for Phase 3 phases, each with tables/diagrams]

## Assumption Register

[Table: Assumption | Fragility | Evidence | Risk if Wrong | Mitigation]

## Test Strategy

[Structured by test levels: Unit, Integration, E2E, Acceptance]

## Implementation Tasks

[Ordered list of tasks with TDD rhythm, dependencies, {{CRITIC_NAME}} checkpoints]

### Task 1: [Name]
🔍 **Review checkpoint**

[Task details: files, structure, acceptance criteria, estimated complexity]

[Continue for each task...]

## Review Checkpoint Plan

[Table: Checkpoint | After Task | {{CRITIC_NAME}} Focus | Decision Gate]
```

**Required Section Headings:**

These headings are used by downstream tools and must be preserved exactly:
- `# [Feature Name] {{DOMAIN}} Implementation Plan`
- `## Feature Overview`
- `## Assumption Register`
- `## Test Strategy`
- `## Implementation Tasks`
- `## Review Checkpoint Plan`
- Plus any `{{DOMAIN_DESIGN_SECTIONS}}` as appropriate

**Save Location:**

`docs/plans/YYYY-MM-DD-<feature-name>-{{DOMAIN}}-plan.md`

Example:
- `docs/plans/2024-03-08-product-search-react-plan.md`
- `docs/plans/2024-03-08-reviews-drupal-plan.md`
- `docs/plans/2024-03-08-search-form-a11y-plan.md`

---

## Worked Example 1: React Planner Implementation

### How react-planner Extends the Base Protocol

**Phase 1: Scope & Context** (from base)
- Detect framework (React, Next.js, React Native)
- Understand risk: performance-sensitive? Data-heavy? RSC boundaries?

**Phase 2: Existing Architecture Analysis** (from base)
- Read component tree structure
- Identify state management approach (Context, Redux, Zustand, props?)
- Identify patterns: API calls, error handling, styling
- Identify pain points: prop drilling, re-render waterfalls, unclear state ownership

**Phase 3: React-Specific Design (3 sub-phases)**

**Phase 3a: Component Architecture**
- Design component tree (parent-child, data flow)
- Define each component's responsibility (one sentence)
- Define props/events contracts
- Identify container vs presentational components

**Phase 3b: State Ownership & Hook Composition**
- Map state ownership with "Why Here" justifications
- Design custom hook dependency arrays upfront
- Plan memoization strategy (React.memo, useCallback, useMemo)

**Phase 3c: Performance & Next.js Boundaries** (if Next.js)
- Create render performance budget
- Classify components (server/client)
- Design cache/revalidation strategy
- Plan error & loading states

**Phase 4: Assumption Register** (from base)
- Example: "State ownership in SearchHeader won't cause re-render waterfalls" (FRAGILE)
- Example: "Custom hook dependency arrays are correct" (FRAGILE)

**Phase 5: Test Strategy** (from base, with React-specific tests)
- Component tests (React Testing Library)
- Integration tests (multi-component flows)
- E2E tests (user journeys)
- Accessibility tests (keyboard, screen reader)

**Phase 6: Implementation Tasks** (from base, with React-specific format)
- Each task: component file, test file, hook stubs, TDD rhythm
- Acceptance criteria: behavior tests, performance goals, accessibility

**Phase 7: Review Checkpoint Plan** (from base, with react-critic)
- Checkpoint 1: After component architecture (react-critic verifies tree, responsibilities, state ownership)
- Checkpoint 2: After SearchInput & ResultsList (react-critic verifies hooks, performance, a11y)
- Checkpoint 3: Final review (react-critic verifies everything)

### Example React Planner Output

```markdown
# Product Search React Implementation Plan

> **For Claude:** Use react-planner protocol. Invoke react-critic at each checkpoint marked with 🔍.
> **Framework:** Next.js App Router
> **Companion skills:** brainstorming, test-driven-development, react-critic, executing-plans

**Feature:** Product search interface with live results, filtering, and pagination
**Risk Level:** Medium (multiple async operations, render optimization needed)
**Existing Architecture:** Monolithic search page, hardcoded data, no performance optimization

---

## Feature Overview

Users need to search products by name and filter by category. Current implementation loads all products on page load (scalability problem). New implementation: live search with debounce, category filters, pagination, results cached per search query.

Key design decisions:
1. SearchHeader (client) owns searchQuery and filters state, calls useSearchResults hook
2. ResultsList (server component) fetches data via server action, wraps ListItem in client component for selection
3. ListItem (client) uses optimistic updates for favorite toggle
4. Cache strategy: results invalidated on-demand only (on search submission), not real-time

## Component Architecture

```
SearchPage (Server)
├── SearchHeader (Client)
│   ├── SearchInput (input + debounce)
│   └── FilterSidebar (toggle filters)
├── ResultsList (Server)
│   └── ListItem (Client) × N (with optimistic updates)
└── Pagination (Client)
```

[Table: Component | Responsibility | Props | Events]

## State Ownership Map

| State | Owner | Type | Lifetime | Accessed By | Why Here | Consequence |
|-------|-------|------|----------|-------------|----------|------------|
| searchQuery | SearchHeader | string | page session | ResultsList via server action | SearchHeader needs to display value and debounce; ResultsList needs current query | If in ResultsList: prop drilling; if global context: unneeded re-renders |
| filters | SearchHeader | object | page session | ResultsList via server action | Same as searchQuery | Same as searchQuery |
| selectedId | SearchPage | string | undefined | ListItem via prop | Multiple ListItems need to show selection; SearchPage needs to navigate on selection | If in ListItem: can't coordinate selection across items |

## Hook Composition Plan

[Table: Hook | Component | Purpose | Dependencies | Cleanup | Risk]

## Render Performance Budget

[Table: Scenario | Trigger | Affected Components | Current | Target | Optimization]

## Server/Client Boundaries (Next.js)

| Component | Type | Rationale |
|-----------|------|-----------|
| SearchPage | Server | Fetches product config, needs backend access |
| SearchHeader | Client | Uses useState for query and filters |
| ResultsList | Server | Fetches results from database |
| ListItem | Client | Uses state for expanded details, event handlers for selection |

## Assumption Register

| Assumption | Fragility | Evidence | Risk if Wrong | Mitigation |
|-----------|-----------|----------|--------------|-----------|
| State ownership won't cause re-render waterfalls | FRAGILE | No measurement yet | Performance regression at scale | Create render budget test; measure in React DevTools; checkpoint after Task 2 |
| useCallback on onChange is necessary | FRAGILE | Designed but not verified | Unnecessary optimization (minor) or stale closures (major) | Implement without memo first; measure re-renders; add memo only if needed |
| RSC boundary between ResultsList (server) and ListItem (client) is performant | FRAGILE | Not measured in codebase | Over-fetching or client-side rendering bottleneck | Measure bundle size and CCP; establish SLO (< 100ms); benchmark test in staging |

## Test Strategy

### Component Tests
- SearchInput: type text → onSearch not called immediately, called after 300ms debounce
- FilterSidebar: click filter → onChange fired, filter state updated
- ListItem: click favorite → optimistic update + server mutation, rollback on error

### Integration Tests
- Type in SearchInput → results load → paginate through results
- Toggle filter → results re-fetch with new filter

### E2E Tests
- Search flow: open page → type query → see results → apply filter → select item → navigate to details

### Accessibility Tests
- All inputs labeled
- Tab order logical
- Keyboard navigation works (Enter in search, Tab through results)
- Screen reader announces results count and selection

## Implementation Tasks

### Task 1: SearchInput Component
🔍 **Review checkpoint**

**Files:** src/components/SearchInput.tsx, src/components/SearchInput.test.tsx

**Component Signature:**
```typescript
interface SearchInputProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  isLoading?: boolean;
  debounceMs?: number;
}
export function SearchInput(props: SearchInputProps): JSX.Element
```

**What to build:** Input with debounced onSearch callback, stable callback reference via useCallback, cleanup for timer

**Acceptance Criteria:**
- Type text → onSearch not called immediately
- Wait 300ms → onSearch called once with text
- isLoading=true → input disabled, spinner shows
- Tab focuses input, Screen reader announces label
- onChange callback is stable (useCallback)

**TDD Rhythm:**
1. Write RTL test: type, wait, verify callback
2. Verify fails
3. Implement with useState, useRef, useEffect
4. Verify passes
5. Add accessibility test
6. Performance check: add useCallback if callback is dependency elsewhere
7. Verify all tests pass
8. Submit for react-critic review

**Estimated Complexity:** Medium

**Dependencies:** None

### Task 2: ResultsList Server Component + ListItem Client Component
🔍 **Review checkpoint**

[Similar detailed format...]

### Task 3: Pagination & Integration
🔍 **Review checkpoint**

[Similar detailed format...]

## Review Checkpoint Plan

| Checkpoint | After Task | react-critic Focus | Decision Gate |
|-----------|-----------|-------------------|--------------|
| 🔍 1 | Complete Phase 3 (Architecture) | Component tree correct, state ownership justified, props clear | ACCEPT or ACCEPT-WITH-RESERVATIONS required before implementation |
| 🔍 2 | Tasks 1-2 complete (SearchInput, ResultsList, ListItem) | useCallback necessity, dependency arrays, memo decisions, performance assumptions | CRITICAL findings block; MAJOR findings require fix before Task 3 |
| 🔍 3 | All tasks complete | All assumptions validated, performance budget achieved, a11y tests pass, ready for production | ACCEPT required for merge |
```

---

## Worked Example 2: Hypothetical "Infra Planner" Implementation

### How infra-planner Would Extend the Base Protocol

**Phase 1: Scope & Context** (from base)
- Understand infrastructure goal (deploy new service, migrate to new region, upgrade database)
- Identify constraints: budget, availability requirements, compliance needs
- Risk assessment: availability SLA, data integrity, cost impact

**Phase 2: Existing Architecture Analysis** (from base)
- Map current infrastructure (services, databases, CDN, monitoring)
- Identify bottlenecks: scaling limits, cost drivers, reliability issues
- Document conventions: naming, deployment process, monitoring approach

**Phase 3: Infrastructure-Specific Design (4 sub-phases)**

**Phase 3a: Architecture Decision & Trade-offs**
- Design target architecture (monolith vs microservices, on-prem vs cloud, etc.)
- Compare alternatives (cost, complexity, scaling, maintenance)
- Define capacity planning (expected growth, peak load, resource allocation)

**Phase 3b: Deployment Strategy**
- Define deployment approach (blue-green, canary, rolling update)
- Plan rollback strategy (how to revert if things go wrong)
- Plan monitoring checkpoints (health checks, metrics)

**Phase 3c: Data Migration & Backup**
- Define data migration path (if changing database)
- Plan backup/restore strategy
- Define RTO/RPO requirements

**Phase 3d: Cost & Reliability Models**
- Estimate infrastructure costs
- Define SLO/SLA targets (99.9% uptime?)
- Plan scaling triggers (when to add resources)

**Phase 4: Assumption Register** (from base)
- Example: "Database performance will scale linearly to N connections" (FRAGILE)
- Example: "Region X has sufficient capacity for new workload" (FRAGILE)
- Example: "Rollback can be completed in < 30 minutes" (MODERATE)

**Phase 5: Test Strategy** (from base, infrastructure-specific)
- Load testing (can system handle peak load?)
- Failover testing (does backup work? How long to recover?)
- Cost validation (does infrastructure cost match budget?)
- Monitoring validation (do alerts fire correctly?)

**Phase 6: Implementation Tasks** (from base, infrastructure-specific)
- Task 1: Provision new infrastructure (VMs, databases, networking)
- Task 2: Deploy service to new infrastructure
- Task 3: Set up monitoring and alerts
- Task 4: Run load tests and failover tests
- Task 5: Migration of data (if applicable) with verification
- Task 6: Cutover to new infrastructure

**Phase 7: Review Checkpoint Plan** (from base, with infra-critic)
- Checkpoint 1: After architecture design (infra-critic reviews cost estimates, scaling strategy, reliability assumptions)
- Checkpoint 2: After infrastructure provisioning (infra-critic verifies configuration, security, monitoring)
- Checkpoint 3: After migration/cutover (infra-critic verifies performance, cost, monitoring, alerting)

### Example Infra Planner Output

```markdown
# Database Migration to PostgreSQL Implementation Plan

> **For Claude:** Use infra-planner protocol. Invoke infra-critic at each checkpoint marked with 🔍.
> **Current Stack:** MySQL 5.7, 10GB data, 100 QPS peak
> **Target Stack:** PostgreSQL 14, managed on AWS RDS
> **Companion skills:** code-archaeology, test-driven-development, infra-critic, executing-plans

**Feature:** Migrate application database from MySQL to PostgreSQL
**Risk Level:** High (data-critical, downtime impacts all users)
**Existing Architecture:** Single MySQL instance, daily backups, no replication

---

## Feature Overview

Current MySQL instance has performance issues at peak load. PostgreSQL offers better query planner and native JSON support (needed for new features). Migration must happen with < 1 hour total downtime.

Key design decisions:
1. Use AWS Database Migration Service (DMS) for automated migration
2. Blue-green approach: run PostgreSQL in parallel, cutover once validated
3. RTO (Recovery Time Objective): < 1 hour
4. RPO (Recovery Point Objective): < 5 minutes (acceptable data loss)

## Architecture Decision & Trade-offs

### Option A: AWS RDS PostgreSQL (Chosen)
- Cost: $500-1000/month
- Scaling: vertical (instance size) + read replicas
- Maintenance: AWS handles patches, backups
- Risk: vendor lock-in, limited customization

### Option B: Self-Hosted PostgreSQL on EC2
- Cost: $200-300/month (cheaper)
- Scaling: manual, requires DevOps expertise
- Maintenance: we manage everything
- Risk: operational burden, high complexity

**Chosen Option A** because: lower operational overhead, automatic backups, AWS RDS migration tools, acceptable cost.

## Capacity Planning

| Metric | Current | Projected Year 1 | Projected Year 2 | Target Capacity |
|--------|---------|------------------|------------------|-----------------|
| Data Size | 10 GB | 20 GB | 40 GB | 100 GB (10x buffer) |
| QPS Peak | 100 | 200 | 400 | 1000 (2.5x buffer) |
| Connections | 20 | 40 | 80 | 200 (2.5x buffer) |

PostgreSQL db.t4g.large instance supports up to 1000 connections, 10,000 IOPS.

## Deployment Strategy

**Blue-Green Approach:**
1. Provision PostgreSQL (green) in parallel with MySQL (blue)
2. Use AWS DMS to replicate data continuously
3. Validate data integrity (counts, checksums)
4. Run performance tests on PostgreSQL
5. Cut over: update application connection string, run smoke tests
6. Monitor for 24 hours, keep MySQL running as rollback
7. Decommission MySQL after 48-hour observation period

**Rollback Strategy:**
- If PostgreSQL issues detected within 24 hours: revert connection string to MySQL
- MySQL remains running for 48 hours post-cutover as fallback

## Assumption Register

| Assumption | Fragility | Evidence | Risk if Wrong | Mitigation |
|-----------|-----------|----------|--------------|-----------|
| AWS DMS will replicate data accurately | MODERATE | AWS claim, used by many companies | Data corruption, missing records | Validation queries: count records, checksum key columns, compare sample records |
| PostgreSQL query performance will be faster | FRAGILE | Not benchmarked yet | Same or slower performance, wasted migration effort | Benchmark key queries on staging: select, insert, update, complex joins |
| Rollback to MySQL within 24 hours is safe | FRAGILE | Depends on application idempotency | Lost writes during cutover, data inconsistency | Test application handles read-from-PostgreSQL + write-to-MySQL scenario; validate transaction logs |

## Test Strategy

### Load Testing
- Benchmark key queries on PostgreSQL (select, insert, update, delete)
- Test peak load (200 QPS) on PostgreSQL, verify sub-500ms latency
- Compare with MySQL baseline

### Failover Testing
- Kill PostgreSQL instance, verify cutover to MySQL in < 5 minutes
- Revert to MySQL connection string, verify application works
- Revert to PostgreSQL connection string, verify application works

### Data Validation
- Count total records in MySQL vs PostgreSQL (must match)
- Checksum key columns (id, created_at) to ensure no corruption
- Spot-check 100 random records for accuracy

### Monitoring Validation
- Verify alarms fire for: high CPU, connection limit, replication lag, query latency > 500ms
- Verify dashboards show: QPS, latency, connections, replication status

## Implementation Tasks

### Task 1: Provision PostgreSQL on AWS RDS
🔍 **Review checkpoint**

**Infrastructure Setup:**
- AWS RDS PostgreSQL 14, db.t4g.large instance
- Subnet: private VPC, security group allows inbound from app VPC only
- Backup: automated daily, 30-day retention
- Monitoring: CloudWatch metrics + alarms for CPU, connections, storage

**Acceptance Criteria:**
- PostgreSQL instance is up and running
- Can connect from application server (test connection)
- Security groups configured correctly (no direct internet access)
- Backups scheduled and tested
- CloudWatch alarms configured for CPU > 80%, connections > 800

**Estimated Complexity:** Medium

**Dependencies:** AWS account access, VPC configuration

### Task 2: Set Up AWS DMS for Data Replication
🔍 **Review checkpoint**

**DMS Setup:**
- Create DMS replication instance (dms.t3.medium)
- Configure source endpoint (MySQL), target endpoint (PostgreSQL)
- Create replication task: full load + CDC (Change Data Capture)
- Run replication, monitor for completion

**Acceptance Criteria:**
- DMS replication task completes (full load of 10 GB data)
- CDC captures ongoing changes from MySQL
- Replication lag < 5 seconds at peak load
- No errors or warnings in DMS task logs

**Estimated Complexity:** Medium

**Dependencies:** Task 1 complete, MySQL credentials, network connectivity

### Task 3: Validate Data Integrity
🔍 **Review checkpoint**

**Validation Queries:**
- Count total rows in each table: MySQL vs PostgreSQL (must match exactly)
- Checksum key columns (id, created_at, updated_at)
- Spot-check 100 random records for accuracy

**Acceptance Criteria:**
- All tables have matching row counts
- No checksum mismatches detected
- Spot-check validation passes
- Sample foreign key relationships validated

**Estimated Complexity:** Medium

**Dependencies:** Task 2 complete (DMS replication done)

### Task 4: Performance Benchmark
🔍 **Review checkpoint**

**Benchmark Queries:**
- Select by primary key (should be < 1ms)
- Select with complex join (current: 50ms on MySQL, target: < 50ms on PostgreSQL)
- Insert 1000 rows (current: 100ms, target: < 100ms)
- Update with where clause (current: 50ms, target: < 50ms)

**Load Test:**
- Simulate 200 QPS (2x current peak) for 5 minutes
- Measure: latency, CPU usage, memory, connection count
- Verify latency stays sub-500ms

**Acceptance Criteria:**
- All benchmarked queries meet target latency
- Load test at 200 QPS: latency < 500ms p99
- CPU stays below 60% at peak load
- No query timeouts or connection rejections

**Estimated Complexity:** High

**Dependencies:** Task 1, 2, 3 complete

### Task 5: Cutover & Monitoring
🔍 **Review checkpoint**

**Cutover Steps:**
1. Stop new writes to MySQL (put app in read-only mode, 30 seconds)
2. Wait for CDC to catch up (replication lag = 0)
3. Update application connection string to PostgreSQL
4. Restart application servers one at a time (rolling restart)
5. Run smoke tests (login, search, create record)
6. Monitor for errors for 30 minutes
7. If errors: revert to MySQL

**Monitoring:**
- Watch error rate (must stay < 0.1%)
- Watch latency (p99 < 500ms)
- Watch PostgreSQL CPU, connections, disk usage
- Verify all CloudWatch alarms are healthy

**Acceptance Criteria:**
- Cutover completed with < 5 minutes downtime
- Application running on PostgreSQL
- Error rate normal (< 0.1%)
- Latency normal (p99 < 500ms)
- All smoke tests pass

**Estimated Complexity:** High

**Dependencies:** Task 1-4 complete

### Task 6: Post-Cutover Observation & Decommission MySQL
🔍 **Review checkpoint**

**Observation Period (48 hours):**
- Monitor PostgreSQL stability
- Monitor application for any data inconsistencies
- Monitor cost to verify estimates accurate
- Keep MySQL running as warm standby

**Decommission MySQL (if all good):**
- Final backup of MySQL
- Document connection details for archive
- Terminate RDS instance or stop it (keep for 30 days in case)

**Acceptance Criteria:**
- 48 hours of monitoring with zero critical issues
- Cost within budget estimate
- Performance stable and meeting SLO
- MySQL safely decommissioned

**Estimated Complexity:** Low

**Dependencies:** Task 5 complete

## Review Checkpoint Plan

| Checkpoint | After Task | infra-critic Focus | Decision Gate |
|-----------|-----------|-------------------|--------------|
| 🔍 1 | Task 1 (RDS provision) | Configuration secure, monitoring complete, backup working | ACCEPT required before proceeding |
| 🔍 2 | Task 4 (Performance benchmark) | Performance meets SLO, load test passes, no bottlenecks | ACCEPT required before cutover |
| 🔍 3 | Task 5 (Cutover) | Downtime minimal, cutover procedure executed correctly, rollback ready | ACCEPT required for success |
| 🔍 4 | Task 6 (Post-cutover) | System stable 48 hours, cost within budget, ready to decommission MySQL | ACCEPT for project completion |
```

---

## Key Principles

### 1. Universal vs Domain-Specific

**Universal Phases** (every planner implements):
- Phase 1: Scope & Context
- Phase 2: Existing Architecture Analysis
- Phase 4: Assumption Register
- Phase 5: Test Strategy
- Phase 6: Implementation Tasks
- Phase 7: Review Checkpoint Plan

**Domain-Specific Phases** (Phase 3, varies by domain):
- React: Component Architecture, State Ownership, Performance & RSC Boundaries
- Drupal: Data Model, Module Architecture, Cache & Migration Strategy
- A11y: Structure Plan, Interaction Patterns, Focus Management, State Communication
- Plan-Writer: Competing Alternatives, Pre-Mortem Analysis
- Infra: Architecture Decisions, Deployment Strategy, Data Migration, Monitoring

### 2. Hard Gates

Planners enforce hard gates to prevent implementation disasters:

1. **Scope clarity gate** (Phase 1): Don't proceed without clear boundaries
2. **Architecture understanding gate** (Phase 2): Read existing code before designing
3. **Assumption documentation gate** (Phase 4): Every assumption must be explicit
4. **Test strategy gate** (Phase 5): Tests must be designed before code
5. **Review checkpoint gate** (Phase 7): Implementation must include verification stages

### 3. Output Format Consistency

All planners preserve exact section headings so downstream tools can parse them:
- `# [Feature Name] {{DOMAIN}} Implementation Plan`
- `## Feature Overview`
- `## {{DOMAIN_DESIGN_SECTIONS}}`
- `## Assumption Register`
- `## Test Strategy`
- `## Implementation Tasks`
- `## Review Checkpoint Plan`

### 4. Critic Integration

Every plan includes {{CRITIC_NAME}} review checkpoints:
- Checkpoints mark where domain critic (react-critic, drupal-critic, etc.) should review
- Each checkpoint specifies explicit focus areas
- Verdict gates determine if work can proceed

### 5. Scalability to Consequence

Plans scale complexity based on consequence:
- **Low consequence** (prototype, utility): 2-3 pages, essential sections only
- **Medium consequence** (production feature): 5-8 pages, all sections
- **High consequence** (data system, migration, compliance): 10-15 pages, maximum detail

---

## Template Author Checklist (Verify Before Shipping)

Before merging a new planner built from this template, verify:

- [ ] **All placeholders filled**: Every `{{PLACEHOLDER}}` replaced with domain-specific content (or marked N/A with rationale)
- [ ] **All 7 phases present**: Scope & Context, Architecture Analysis, Domain Design, Assumption Register, Test Strategy, Implementation Tasks, Review Checkpoints
- [ ] **Phase 3 has substance**: Domain design has 1-5 sub-phases with specific steps (not just "design the solution")
- [ ] **Assumption Register populated**: Example assumptions with diverse fragility ratings (ROBUST/MODERATE/FRAGILE) and evidence types:
  - ROBUST evidence: "Checked source code, documented in package.json, verified in team records"
  - MODERATE evidence: "Inferred from similar past projects, team consensus, documented patterns"
  - FRAGILE evidence: "Untested, new territory, significant uncertainty"
- [ ] **Test strategy is domain-specific**: Not just "write tests" — specific test types for your domain
- [ ] **Implementation tasks have WP-compatible format**: Task title, estimated effort, dependencies, acceptance criteria per task
- [ ] **Review checkpoint specifies critic**: Names the domain critic (e.g., react-critic) and focus areas
- [ ] **Output format matches contract**: All required sections present with immutable headings
- [ ] **Worked example complete**: At least one filled example showing realistic plan output
- [ ] **Companion skills listed**: References to related critics/planners are accurate and exist
- [ ] **Tested on real plans**: Run 5-10 planning sessions before release

## Implementation Checklist for Domain Planners

When implementing a new planner (extending this base protocol):

- [ ] Phase 1: Scope & Context (copy from base, add domain questions)
- [ ] Phase 2: Existing Architecture Analysis (copy from base, add domain-specific investigation)
- [ ] Phase 3: Design (1-5 domain-specific phases, define {{DOMAIN_DESIGN}} interface)
- [ ] Phase 4: Assumption Register (copy from base, add domain-specific assumptions with evidence types)
- [ ] Phase 5: Test Strategy (copy from base, add {{TEST_DOMAIN}} section with domain-specific tests)
- [ ] Phase 6: Implementation Tasks (copy from base, add domain-specific task format)
- [ ] Phase 7: Review Checkpoint Plan (copy from base, specify {{CRITIC_NAME}} and focus areas)
- [ ] Output Format (copy from base, add {{DOMAIN_DESIGN_SECTIONS}} and {{CRITIC_NAME}})
- [ ] Worked Example (show how new planner extends base protocol)
- [ ] Hard Gates (define domain-specific gates if needed)
- [ ] Failure Modes (list domain-specific failure modes to avoid)
- [ ] **Run the Template Author Checklist above** — every box must be checked

---

## Files to Update When Adding New Planner

1. **New planner agent file:** `.claude/agents/{{new-planner}}.md`
   - Define Role, Success Criteria, Constraints
   - Implement Planning Protocol (Phase 1-7)
   - Define Output Format (preserve universal structure + add {{DOMAIN_DESIGN}})
   - Include Failure Modes & Examples

2. **Update base protocol template** (this file):
   - Add new domain to "Examples of Domain-Specific Phases" section in Phase 3
   - Add new domain to "Worked Example" section if significant enough
   - Document any new hard gates or principles

3. **Update meta-skills documentation:**
   - List new planner in ecosystem overview
   - Show how it fits with other planners
   - Link to agent file and example usage

---

## References

### Planner Agents in Zivtech Meta-Skills

- `react-planner.md`: React/Next.js/React Native implementation planning
- `drupal-planner.md`: Drupal module, entity, and content type planning
- `a11y-planner.md`: Accessibility design planning (WCAG 2.2, APG patterns)
- `plan-writer.md`: General-purpose planning with risk analysis

### Critic Agents

- `react-critic.md`: Review React implementation architecture
- `drupal-critic.md`: Review Drupal entity design, permissions, migrations
- `a11y-critic.md`: Review accessibility implementation
- `proposal-critic.md`: General-purpose plan review (competing alternatives, pre-mortem, backcasting)

### Testing Skills

- `test-driven-development.md`: TDD implementation with spec-kitty integration
- `accessibility-testing.md`: Automated accessibility testing (axe-core, WCAG)
- `a11y-test.md`: Manual keyboard and screen reader testing

### Execution Skills

- `executing-plans.md`: Batch execution of tasks with review checkpoints
- `brainstorming.md`: Design phase exploration before implementation

---

## Version History

- **2026-03-08** (Initial): Template created with universal protocol, Phase 1-7, working examples for react-planner and hypothetical infra-planner
