#!/usr/bin/env python3
"""Mechanical scorer for chain eval sessions (S3–S5). S1–S2 are human-scored.

Usage: python3 evals/suites/chain/score_chain.py <fixture-id> <session-dir>

session-dir must contain:
  critic.txt   — critic stage output text
  audit.txt    — audit output (empty file or absent if not run)
  escalated.txt — "true" or "false" (whether audit was spawned)
"""
import os, re, sys, yaml

LEVELS = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
RUBRICS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rubrics")
P_MAP = {  # keyword → canonical perspective key
    "magnification": "magnification_reflow", "reflow": "magnification_reflow",
    "contrast": "environmental_contrast", "environmental": "environmental_contrast",
    "vestibular": "vestibular_motion", "motion": "vestibular_motion",
    "auditory": "auditory_access", "caption": "auditory_access",
    "keyboard": "keyboard_motor", "motor": "keyboard_motor",
    "screen reader": "screen_reader_semantic", "screen_reader": "screen_reader_semantic",
    "cognitive": "cognitive_neurodivergent", "neurodivergent": "cognitive_neurodivergent",
}


def alarm_score(act, exp):
    a, e = LEVELS.get(str(act).upper(), -1), LEVELS.get(str(exp).upper(), -1)
    if a < 0 or e < 0: return 0.0
    d = abs(a - e)
    return 1.0 if d == 0 else (0.5 if d == 1 else 0.0)


def parse_alarms(text):
    found = {}
    for line in text.split("\n"):
        up = line.upper()
        lv = next((l for l in ("HIGH", "MEDIUM", "LOW") if l in up), None)
        if not lv: continue
        lo = line.lower()
        for kw, key in P_MAP.items():
            if kw in lo and key not in found:
                found[key] = lv; break
    return found


def s3_alarm(rubric, critic):
    exp = rubric.get("expected_alarm_levels") or {}
    if not exp: return None, "no expected_alarm_levels"
    act = parse_alarms(critic)
    rows = []
    for p, e in exp.items():
        a = act.get(p, "MISSING")
        sc = alarm_score(a, e) if a != "MISSING" else 0.0
        rows.append((p, e, a, sc))
    mean = sum(r[3] for r in rows) / len(rows)
    detail = "\n".join(f"  {p}: exp={e} act={a} → {sc}" for p, e, a, sc in rows)
    return round(mean, 3), detail


def s3_must_find(rubric, critic):
    items = rubric.get("must_find_items") or []
    if not items: return None, "no must_find_items"
    lo = critic.lower()
    rows = [(item, " ".join(item.lower().split()[:5])[:18] in lo) for item in items]
    score = round(sum(int(f) for _, f in rows) / len(rows), 3)
    detail = "\n".join(f"  {'FOUND' if f else 'MISS'}: {item[:70]}" for item, f in rows)
    return score, detail


def s4(rubric, escalated, critic):
    if rubric.get("s4_graded", True) is False:
        return None, "ungraded — no alarm ground truth in source suite (observational only)"
    exp = rubric.get("expected_escalation", False)
    if exp != escalated:
        return 0, f"expected={exp} actual={escalated}"
    scope = rubric.get("expected_escalated_perspectives")
    if scope and escalated:  # CLEAN fixtures: escalated set must match exactly
        act = sorted(p for p, lv in parse_alarms(critic).items() if lv in ("MEDIUM", "HIGH"))
        if act != sorted(scope):
            return 0, f"scope mismatch: expected={sorted(scope)} critic-flagged={act}"
    return 1, f"expected={exp} actual={escalated}"


def audit_verdict(rubric, audit):
    exp = rubric.get("expected_audit_verdict")
    if not exp: return None, "not defined for this fixture"
    if not audit.strip(): return 0, "audit output empty — verdict cannot match"
    hit = re.search(rf"\b{re.escape(exp)}\b", audit, re.I) is not None
    return int(hit), f"  provisional token match '{exp}': {'FOUND' if hit else 'MISSING'} — confirm by hand"


def s5(rubric, audit):
    if not audit.strip(): return None, "audit not run"
    alarms = rubric.get("expected_alarm_levels") or {}
    low_ps = [p for p, v in alarms.items() if v == "LOW"]
    esc_ps = [p for p, v in alarms.items() if v in ("MEDIUM", "HIGH")]
    alo = audit.lower()
    impact = {"critical", "major", "finding", "issue", "fail"}
    leak = any(p.split("_")[0] in alo and any(w in alo for w in impact) for p in low_ps)
    a = 0 if leak else 1  # S5a: no LOW perspective at findings level
    b = 1 if all(p.split("_")[0] in alo for p in esc_ps) else 0  # S5b: escalated covered
    return a + b, f"  S5a(no-low-leak)={a}  S5b(esc-covered)={b}"


def tracer(rubric, final):
    t = rubric.get("tracer_finding")
    if not t: return None, "no tracer (CLEAN fixture)"
    key = " ".join(t.lower().split()[:5])[:18]
    found = key in final.lower()
    return int(found), f"  {'FOUND' if found else 'MISSING'}: {t[:60]}"


def read(path, default=""):
    return open(path).read() if os.path.exists(path) else default


def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    fid, sdir = sys.argv[1], sys.argv[2]
    rpath = os.path.join(RUBRICS, f"{fid}.chain.yaml")
    if not os.path.exists(rpath):
        print(f"Rubric not found: {rpath}"); sys.exit(1)
    rb = yaml.safe_load(open(rpath))
    critic_t = read(os.path.join(sdir, "critic.txt"))
    audit_t  = read(os.path.join(sdir, "audit.txt"))
    esc_raw  = read(os.path.join(sdir, "escalated.txt"), "false").strip().lower()
    escalated = esc_raw == "true" if esc_raw in ("true","false") else bool(audit_t.strip())

    mode = rb.get("s3_scoring_mode", "alarm")
    s3v, s3d = (s3_must_find if mode == "must_find" else s3_alarm)(rb, critic_t)
    s4v, s4d = s4(rb, escalated, critic_t)
    final_t = audit_t if audit_t.strip() else critic_t
    s5v, s5d = s5(rb, audit_t)
    avv, avd = audit_verdict(rb, audit_t)
    tv, td = tracer(rb, final_t)

    ok = ((s4v is None or s4v == 1) and (s3v is None or s3v > 0)
          and (tv is None or tv == 1) and (avv is None or avv == 1))
    print(f"\n=== {fid} ===")
    print(f"S3 [{mode}]: {s3v}\n{s3d}")
    print(f"S4 [escalation]: {s4v}  {s4d}")
    print(f"S5 [audit scope]: {s5v}\n{s5d}")
    print(f"Audit verdict: {avv}  {avd}")
    print(f"Tracer: {tv}\n{td}")
    print(f"\nPASS: {ok}  (S1/S2 human-scored separately; audit verdict is provisional)")


if __name__ == "__main__":
    main()
