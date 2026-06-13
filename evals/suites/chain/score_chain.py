#!/usr/bin/env python3
"""Mechanical scorer for chain eval sessions (S3-S5). S1-S2 are human-scored.

Usage: python3 evals/suites/chain/score_chain.py <fixture-id> <session-dir>

session-dir must contain (plan 011: reads <stage>.md, falls back to <stage>.txt):
  critic.md / critic.txt     -- critic stage output text (PRISTINE agent output only;
                                operator notes belong in <stage>.notes.md -- see I9)
  audit.md  / audit.txt      -- audit output (empty/absent if not run)
  escalated.txt              -- "true" or "false" (whether audit was spawned)

Plan 011 fixes baked in:
  I1  detect_peek() flags answer-key contamination -> S3/S4/tracer marked INVALID.
  I2  lens->canonical CROSSWALK + max-collapse + absent-perspective-is-LOW (not MISSING=0).
  I3  concept/word-overlap tracer match (not an 18-char leading substring).
  I4  audit verdict = recommendation line + MAJOR/CRITICAL counts (not a bare "PASS" token).
  I5  S5a LOW-leak check scoped to per-perspective sections.
  I6  read .md with .txt fallback.
"""
import os, re, sys, math, yaml

LEVELS = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
INV = {v: k for k, v in LEVELS.items()}
RUBRICS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rubrics")

# I2(a): lens phrase -> canonical perspective key. Critics emit heterogeneous
# taxonomies; this crosswalk maps every lens observed across the pilot's three
# critics onto the perspectives suite's canonical 7. Ambiguous mappings are
# documented in plan 011 (e.g. "low vision" -> magnification_reflow; voice/switch/
# speech -> keyboard_motor, the input-modality/motor axis). Longer phrases first
# so "low vision" wins before a bare "vision" and "screen reader" before "reader".
CROSSWALK = [
    ("screen reader", "screen_reader_semantic"),
    ("screen_reader", "screen_reader_semantic"),
    ("semantic", "screen_reader_semantic"),
    ("keyboard", "keyboard_motor"),
    ("switch access", "keyboard_motor"),
    ("voice control", "keyboard_motor"),
    ("speech", "keyboard_motor"),
    ("motor", "keyboard_motor"),
    ("low vision", "magnification_reflow"),
    ("magnification", "magnification_reflow"),
    ("reflow", "magnification_reflow"),
    ("zoom", "magnification_reflow"),
    ("contrast", "environmental_contrast"),
    ("color", "environmental_contrast"),
    ("environmental", "environmental_contrast"),
    ("seizure", "vestibular_motion"),
    ("photosensit", "vestibular_motion"),
    ("vestibular", "vestibular_motion"),
    ("motion", "vestibular_motion"),
    ("auditory", "auditory_access"),
    ("caption", "auditory_access"),
    ("hearing", "auditory_access"),
    ("deaf", "auditory_access"),
    ("cognitive", "cognitive_neurodivergent"),
    ("neurodivergent", "cognitive_neurodivergent"),
]

# I1: answer-key fingerprints. Their presence in a judgment stage's PRISTINE output
# means the stage read the rubric/metadata -> its measurement is void.
PEEK_TOKENS = [
    "expected_alarm_levels", "expected alarm levels are", "expected alarm level",
    "tracer_finding", "tracer finding is", "expected_escalated_perspectives",
    "expected_audit_verdict", "s3_scoring_mode", "must_find_items",
    ".chain.yaml", "source_metadata", "acceptable critic verdict",
]

# I3: stopwords dropped before tracer content-word overlap.
STOP = {"the", "not", "and", "or", "for", "with", "into", "onto", "a", "an", "is",
        "are", "was", "to", "on", "in", "of", "no", "it", "its", "this", "that",
        "from", "but", "as", "at", "by", "be", "has", "have"}


def alarm_score(act, exp):
    a, e = LEVELS.get(str(act).upper(), -1), LEVELS.get(str(exp).upper(), -1)
    if a < 0 or e < 0:
        return 0.0
    d = abs(a - e)
    return 1.0 if d == 0 else (0.5 if d == 1 else 0.0)


def lens_to_key(text):
    """First canonical key whose lens phrase appears in text (longest-phrase order)."""
    lo = text.lower()
    for phrase, key in CROSSWALK:
        if phrase in lo:
            return key
    return None


def parse_alarms(text):
    """Map each alarm-bearing line to a canonical key; keep the HIGHEST level per key
    when multiple lenses collapse onto one axis (I2: max-collapse)."""
    found = {}
    for line in text.split("\n"):
        up = line.upper()
        lv = next((l for l in ("HIGH", "MEDIUM", "LOW") if l in up), None)
        if not lv:
            continue
        lo = line.lower()
        for phrase, key in CROSSWALK:
            if phrase in lo:
                if key not in found or LEVELS[lv] > LEVELS[found[key]]:
                    found[key] = lv
    return found


def s3_alarm(rubric, critic):
    exp = rubric.get("expected_alarm_levels") or {}
    if not exp:
        return None, "no expected_alarm_levels"
    act = parse_alarms(critic)
    rows = []
    for p, e in exp.items():
        # I2(b): a perspective the critic never raised is NOT an alarm == LOW,
        # not a zero. Penalising correct silence was the dominant S3 distortion.
        a = act.get(p, "LOW")
        sc = alarm_score(a, e)
        rows.append((p, e, a, sc))
    mean = sum(r[3] for r in rows) / len(rows)
    detail = "\n".join(f"  {p}: exp={e} act={a} -> {sc}" for p, e, a, sc in rows)
    return round(mean, 3), detail


def s3_must_find(rubric, critic):
    items = rubric.get("must_find_items") or []
    if not items:
        return None, "no must_find_items"
    lo = critic.lower()
    rows = [(item, _concept_present(item, lo)) for item in items]
    score = round(sum(int(f) for _, f in rows) / len(rows), 3)
    detail = "\n".join(f"  {'FOUND' if f else 'MISS'}: {item[:70]}" for item, f in rows)
    return score, detail


def _content_words(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower())
            if len(w) >= 3 and w not in STOP]


def _concept_present(needle, haystack_lo):
    """I3: word-overlap concept match. Require >= max(2, ceil(half)) of the needle's
    distinctive content words to appear in the haystack."""
    words = _content_words(needle)
    if not words:
        return False
    hits = [w for w in words if w in haystack_lo]
    need = max(2, (len(words) + 1) // 2)
    return len(hits) >= need


def s4(rubric, escalated, critic):
    if rubric.get("s4_graded", True) is False:
        return None, "ungraded -- no alarm ground truth in source suite (observational only)"
    exp = rubric.get("expected_escalation", False)
    if exp != escalated:
        return 0, f"expected={exp} actual={escalated}"
    scope = rubric.get("expected_escalated_perspectives")
    if scope and escalated:  # CLEAN fixtures: escalated set must match exactly
        act = sorted(p for p, lv in parse_alarms(critic).items() if lv in ("MEDIUM", "HIGH"))
        if act != sorted(scope):
            return 0, f"scope mismatch: expected={sorted(scope)} critic-flagged={act}"
    return 1, f"expected={exp} actual={escalated}"


def _finding_count(audit, level):
    """Prefer an explicit summary count ('MAJOR: 3'); else count 'MAJOR N' finding labels."""
    m = re.search(rf"\b{level}\b\s*[:=]\s*(\d+)", audit, re.I)
    if m:
        return int(m.group(1))
    return len(re.findall(rf"\b{level}\b\s*\d", audit, re.I))


def audit_verdict(rubric, audit):
    """I4: parse the explicit recommendation/verdict line + finding counts.
    expected_audit_verdict: PASS  ==  verdict in {ACCEPT, ACCEPT-WITH-RESERVATIONS}
                                       AND zero CRITICAL AND zero MAJOR."""
    exp = rubric.get("expected_audit_verdict")
    if not exp:
        return None, "not defined for this fixture"
    if not audit.strip():
        return 0, "audit output empty -- verdict cannot match"
    m = re.search(r"(?:overall\s+)?(?:recommendation|verdict)\s*[:\-]\s*"
                  r"([A-Za-z][A-Za-z\- ]*)", audit, re.I)
    verdict = (m.group(1).strip().upper() if m else "")
    crit = _finding_count(audit, "CRITICAL")
    major = _finding_count(audit, "MAJOR")
    if exp.strip().upper() == "PASS":
        clean_verdict = "ACCEPT" in verdict  # ACCEPT or ACCEPT-WITH-RESERVATIONS
        hit = clean_verdict and crit == 0 and major == 0
        why = f"verdict='{verdict or '?'}' CRITICAL={crit} MAJOR={major} -> {'PASS' if hit else 'NON-PASS'}"
    else:
        hit = exp.strip().upper() in verdict
        why = f"verdict='{verdict or '?'}' expected '{exp}' -> {'MATCH' if hit else 'MISMATCH'}"
    return int(hit), f"  {why}"


def _sections(audit):
    """Split an audit into (heading, body) sections on markdown headings."""
    secs, head, body = [], None, []
    for line in audit.split("\n"):
        if re.match(r"^\s*#{1,6}\s", line):
            if head is not None or body:
                secs.append((head or "", "\n".join(body)))
            head, body = line, []
        else:
            body.append(line)
    if head is not None or body:
        secs.append((head or "", "\n".join(body)))
    return secs


def s5(rubric, audit, critic):
    if not audit.strip():
        return None, "audit not run"
    # I5: S5a is defined relative to what the CRITIC escalated (protocol S5a), not the
    # rubric ground truth. A "leak" is the audit opening a findings-level section for a
    # perspective the critic did NOT flag MEDIUM/HIGH -- and only its OWN section, not a
    # mere keyword co-occurrence. (The login audit legitimately reviews keyboard because
    # the critic escalated it, even though that escalation was a false positive.)
    escalated = {p for p, lv in parse_alarms(critic).items() if lv in ("MEDIUM", "HIGH")}
    rub = rubric.get("expected_alarm_levels") or {}
    esc_ps = [p for p, v in rub.items() if v in ("MEDIUM", "HIGH")]
    impact = ("critical", "major", "finding", "fail")
    leak = False
    for head, body in _sections(audit):
        key = lens_to_key(head)
        if key and key not in escalated and any(w in body.lower() for w in impact):
            leak = True
            break
    a = 0 if leak else 1
    alo = audit.lower()
    b = 1 if all(p.split("_")[0] in alo for p in esc_ps) else 0
    return a + b, f"  S5a(no-low-leak)={a}  S5b(esc-covered)={b}"


def tracer(rubric, final):
    t = rubric.get("tracer_finding")
    if not t:
        return None, "no tracer (CLEAN fixture)"
    words = _content_words(t)
    hits = [w for w in words if w in final.lower()]
    need = max(2, (len(words) + 1) // 2)
    found = len(hits) >= need
    return int(found), (f"  {'FOUND' if found else 'MISSING'}: {len(hits)}/{len(words)} "
                        f"content words present (need {need}) -- {t[:50]}")


def detect_peek(text):
    """I1: answer-key fingerprints in pristine stage output -> contamination."""
    lo = text.lower()
    return [tok for tok in PEEK_TOKENS if tok in lo]


def read_stage(sdir, stem, default=""):
    """I6: <stem>.md preferred, <stem>.txt fallback."""
    for ext in (".md", ".txt"):
        p = os.path.join(sdir, stem + ext)
        if os.path.exists(p):
            return open(p).read()
    return default


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    fid, sdir = sys.argv[1], sys.argv[2]
    rpath = os.path.join(RUBRICS, f"{fid}.chain.yaml")
    if not os.path.exists(rpath):
        print(f"Rubric not found: {rpath}")
        sys.exit(1)
    rb = yaml.safe_load(open(rpath))
    critic_t = read_stage(sdir, "critic")
    audit_t = read_stage(sdir, "audit")
    esc_raw = read_stage(sdir, "escalated", "false").strip().lower()
    escalated = esc_raw == "true" if esc_raw in ("true", "false") else bool(audit_t.strip())

    # I1: contamination gate. A peeking judgment stage voids S3/S4/tracer.
    peek_c = detect_peek(critic_t)
    peek_a = detect_peek(audit_t)
    contaminated = bool(peek_c or peek_a)

    mode = rb.get("s3_scoring_mode", "alarm")
    s3v, s3d = (s3_must_find if mode == "must_find" else s3_alarm)(rb, critic_t)
    s4v, s4d = s4(rb, escalated, critic_t)
    final_t = audit_t if audit_t.strip() else critic_t
    s5v, s5d = s5(rb, audit_t, critic_t)
    avv, avd = audit_verdict(rb, audit_t)
    tv, td = tracer(rb, final_t)

    print(f"\n=== {fid} ===")
    if contaminated:
        print("INVALID -- CONTAMINATED: judgment stage read the answer key (I1).")
        if peek_c:
            print(f"  critic peek tokens: {peek_c}")
        if peek_a:
            print(f"  audit  peek tokens: {peek_a}")
        print("  S3/S4/tracer are NOT independent measurements for this fixture.")
    print(f"S3 [{mode}]: {s3v}\n{s3d}")
    print(f"S4 [escalation]: {s4v}  {s4d}")
    print(f"S5 [audit scope]: {s5v}\n{s5d}")
    print(f"Audit verdict: {avv}  {avd}")
    print(f"Tracer: {tv}\n{td}")

    ok = (not contaminated
          and (s4v is None or s4v == 1) and (s3v is None or s3v > 0)
          and (tv is None or tv == 1) and (avv is None or avv == 1))
    note = "CONTAMINATED -> auto-fail" if contaminated else "S1/S2 human-scored separately"
    print(f"\nPASS: {ok}  ({note})")


if __name__ == "__main__":
    main()
