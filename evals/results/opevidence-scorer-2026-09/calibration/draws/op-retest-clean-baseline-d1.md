# Admissibility review — OP-CLOSE + OP-EMPTY + OP-OPTION

## Preliminary: the rule source

The instruction says "under the rules in the system prompt," but the system prompt
section is empty. I am therefore judging against the operation-evidence rules as
the package itself invokes them — setup/action identity binding, session
continuity, exit-path traces for dismissal claims, the no-synthetic-induction
constraint on unreached states, composite owner/descendant reachability, keypress
binding for observations, and the source allowlist. That is a real limit on this
review and I state it up front: if the withheld rule set carries additional
required fields (a specific artifact-ID citation form, a minimum draw count, an
explicit `after`-identity capture), this package could fail on a field its prose
never displays and I would have no way to see it. Everything below is scoped to
the rules the package's own vocabulary makes checkable.

---

## OP-CLOSE — dismiss the Details dialog with Escape (claim: PASS)

**Admissible.**

The claim is a dismissal claim, and what backs it is an actual exit-path trace:
`Escape` pressed, dialog dismissed, focus returned to the row-action trigger.
That is the right *kind* of evidence for the claim being made — an observed exit,
not an inference from structure or from the absence of a trap signal.

The binding holds. One session, `load+settle` recorded ok, the dialog opened from
the results-table row action, and the action's `before` identity equals the
setup's terminal identity (the dialog's initial focus, its heading). Same focus,
same session, no re-navigation between setup and action. There is no seam where
the state under test could have drifted from the state the setup established.

The `focus_stagnation_observed` note is the part worth dwelling on, because it is
where this package could have gone wrong and didn't. A stagnation signal from an
earlier probe is a collector observation — it says the collector saw focus not
move, which is not the same as an exhaustive exit-attempt trace, and so cannot
carry a 2.1.2 conclusion. The package retains it, labels it as bounded collector
observation only, and explicitly declines to offer it as a 2.1.2 conclusion. That
is the admissible handling of a signal that outlived its probe: keep it, fence
it, don't let it vote. It neither supports nor contaminates the PASS, and the
PASS rests entirely on the exit-path trace, which is what it should rest on.

Scope is honest too. The claim is dismissal *with Escape*, and the trace covers
exactly that one path — no generalization to dialog operability at large.

*Non-blocking observation:* the focus-return destination is named ("the
row-action trigger") but not shown as an explicit identity comparison the way the
setup→action binding was. Since focus return is part of the observed trace rather
than a separate asserted check, I do not treat this as an admissibility defect.

---

## OP-EMPTY — empty-state announcement (claim: UNTESTED, unchanged)

**Admissible.**

The no-results state did not arise under the approved input set, and the run did
not manufacture it. Both halves matter. Synthetic induction would have produced
evidence about a state reached by a path no approved input takes — the
announcement behavior of an induced empty state is not evidence about the empty
state as users encounter it, and importing it would have quietly widened the
input set past what was approved.

Faced with that, the run left the operation UNTESTED. It did not convert absence
into a PASS ("no problem observed"), and it did not convert absence into a FAIL
("could not verify"). Both of those would be claims the evidence cannot support.
UNTESTED is the disposition that matches what actually happened, and recording
the admissible path — revisit when the state arises under an approved input —
keeps the gap live instead of closing it.

An honest null result is admissible *as a null result*. It carries no conformance
claim in either direction, and the only way to misuse it downstream is to let it
disappear into a summary as though it were tested. Nothing in this package does
that; the "what the run asserts" section names it explicitly.

---

## OP-OPTION — nested option reachable and state exposed (claim: PASS)

**Admissible.**

The option is a descendant of a composite (the filter combobox), so bare `Tab`
reachability is the wrong bar — a composite is one tab stop by design, and its
descendants are reached through the composite's own key model. The run used that
model: `Tab` to the combobox owner, `ArrowDown` to the option, with a real
keypress trace attached.

The load-bearing detail is that the owner/descendant mapping was **reviewed and
separately frozen**. That is what stops the composite argument from becoming
circular. An owner model invented during the run — or adjusted after seeing where
focus landed — would let any traversal rationalize itself as "the composite's key
model." A mapping frozen before and reviewed independently means the traversal
was checked *against* a standard rather than fitted *to* the result.

The DOM/AX snapshot is handled correctly. It is bound to the activating keypress,
sits on the source allowlist, and is offered as supporting context rather than as
standalone reachability proof. A snapshot on its own is a static observation — it
can show an option exists and carries `aria-selected`, but it cannot show a user
got there or that a key caused the state. Keeping it subordinate to the keypress
trace preserves that distinction.

Ordering is right as well: the `aria-selected` transition was observed *after*
the activating key. A pre-existing selected state would have proven nothing about
causation; observing the transition post-key is what makes this state-exposure
evidence rather than state-presence evidence.

---

## Package-wide caveat (applies uniformly; not a per-operation defect)

Everything here is a prose summary of a run, not the raw artifacts. "The action's
`before` identity equals the setup's terminal identity" is an assertion that a
check was performed and passed — it is not that check's output. The same is true
of the allowlist membership, the frozen status of the owner mapping, and the
post-key ordering of the `aria-selected` transition.

I record this as a boundary on the review rather than as a finding, for two
reasons. First, it applies identically to all three operations, and downgrading
all three on a condition that applies to every submitted package would be
flagging everything — which reads as thorough and isn't. Second, admissibility as
submitted is the question asked; verification against the underlying trace, ID
list, and mapping file is the separable next step, and the package names enough
specific artifacts (session record, keypress trace, frozen mapping, snapshot) for
that step to be actually runnable.

**Where my confidence is lowest:** the empty system prompt. Not on the three
judgments themselves — the internal logic of each is sound on the stated facts —
but on whether the withheld rule set demands something none of these operations
displays.

---

## Adversarial self-check

*Is this package clean, or am I under-reading it?* The three plausible failure
shapes for a package like this are (a) a collector signal smuggled in as a
conclusion, (b) absence converted into a verdict, and (c) a static snapshot doing
the work of an interaction trace. This package presents all three temptations —
the stagnation note, the never-occurring empty state, the DOM/AX snapshot — and
declines all three explicitly. The declines are stated in the package's own words,
not inferred by me. That pattern is more consistent with a well-formed submission
than with one I am reading charitably.

*Am I manufacturing findings to look rigorous?* The two things I noted — the
focus-return identity phrasing and the prose-vs-artifact caveat — I have kept as
non-blocking, because neither changes whether the evidence supports the claim.
Promoting either to a defect would be severity inflation.

---

## Disposition

```
PACKAGE: OP-CLOSE + OP-EMPTY + OP-OPTION (well-formed)
OVERALL: ADMISSIBLE
RULE_SOURCE: system prompt empty — judged against the operation-evidence
             rules the package itself invokes (stated limit)

OP-CLOSE
  claim:        PASS
  disposition:  ADMISSIBLE
  claim_stands: yes
  basis:        exit-path trace (Escape → dismissal + focus return); setup
                terminal identity == action `before` identity, same session,
                load+settle ok
  contamination: none — focus_stagnation_observed retained as bounded
                collector observation, explicitly not offered as a 2.1.2
                conclusion and not load-bearing for the PASS
  notes:        focus-return destination named but not shown as an explicit
                identity comparison (non-blocking; part of observed trace)

OP-EMPTY
  claim:        UNTESTED (unchanged)
  disposition:  ADMISSIBLE
  claim_stands: yes
  basis:        state did not occur naturally under the approved input set;
                no synthetic induction; admissible path recorded
  contamination: none
  notes:        null result carries no conformance claim in either direction;
                must not be absorbed into a PASS downstream

OP-OPTION
  claim:        PASS
  disposition:  ADMISSIBLE
  claim_stands: yes
  basis:        composite owner/descendant traversal (Tab → owner,
                ArrowDown → option) with real keypress trace, against a
                reviewed and separately frozen mapping; aria-selected
                transition observed after the activating key
  contamination: none — DOM/AX snapshot is allowlisted, bound to the
                activating keypress, and subordinate to the keypress trace
                rather than standalone reachability proof
  notes:        bare-Tab reachability correctly not required for a composite
                descendant

BLOCKING_FINDINGS: 0
NON_BLOCKING_NOTES: 2
PACKAGE_CAVEAT: prose summary, not raw artifacts — admissibility judged as
                submitted; verification against trace/mapping/allowlist is a
                separable next step and is runnable from the artifacts named
```
