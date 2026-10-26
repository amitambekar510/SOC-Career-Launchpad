#!/usr/bin/env python3
"""Project health check used locally and by GitHub Actions.

  python scripts/validate_repo.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_question_bank as B

errors = []


def err(msg):
    errors.append(msg)
    print("FAIL:", msg)


def exists(rel):
    return os.path.exists(os.path.join(ROOT, rel))


# 1. curriculum files and visuals exist
cur = json.load(open(os.path.join(ROOT, "ai", "curriculum.json"), encoding="utf-8"))
bank = json.load(open(os.path.join(ROOT, "ai", "question-bank.json"), encoding="utf-8"))
for s in cur["sections"]:
    for rel in s["files"] + s["visuals"]:
        if not exists(rel):
            err(f"curriculum: missing {rel} (section {s['id']})")
    if s.get("gated"):
        n = sum(1 for q in bank["questions"] if q["section"] == s["id"] and q["type"] == "mcq")
        sc = sum(1 for q in bank["questions"] if q["section"] == s["id"] and q["type"] == "scenario")
        if n < 3:
            err(f"{s['id']}: needs at least 3 multiple-choice questions (has {n})")
        if sc < 1:
            err(f"{s['id']}: needs a scenario question")

# 2. question bank matches the source and leaks no answers
if B.build() != bank:
    err("ai/question-bank.json is out of date. Run scripts/build_question_bank.py")
raw = json.dumps(bank)
for bad in ('"answer":', '"why":', '"rubric":'):
    if bad in raw:
        err(f"question-bank.json must not contain {bad}")

# 3. AI entry points reference the policy
for rel in ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md"):
    if not exists(rel):
        err(f"missing {rel}")
    elif "ai/TUTOR_POLICY.md" not in open(os.path.join(ROOT, rel), encoding="utf-8").read():
        err(f"{rel} must reference ai/TUTOR_POLICY.md")
for rel in ("ai/TUTOR_POLICY.md", "LEARNING_CONTRACT.md", "ai/_ai-only/questions.source.json"):
    if not exists(rel):
        err(f"missing {rel}")

# 3b. evidence cases: in sync, balanced, no answer leakage
cases_path = os.path.join(ROOT, "ai", "evidence-cases.json")
src_path = os.path.join(ROOT, "ai", "_ai-only", "evidence-cases.source.json")
if not (os.path.exists(cases_path) and os.path.exists(src_path)):
    err("evidence cases files are missing")
else:
    cases_pub = json.load(open(cases_path, encoding="utf-8"))
    cases_src = json.load(open(src_path, encoding="utf-8"))
    if B.build_cases() != cases_pub:
        err("ai/evidence-cases.json is out of date. Run scripts/build_question_bank.py")
    for leak in ('"expected"', '"known_gaps"', '"reckless"', '"decision_changers"', '"safe_interim"', '"teaching_note"', '"scoring"'):
        if leak in json.dumps(cases_pub):
            err(f"evidence-cases.json must not contain {leak}")
    cl = cases_src["cases"]
    suff = sum(1 for c in cl if c["expected"]["evidence_sufficient"])
    if len(cl) < 6:
        err("need at least 6 evidence cases")
    if suff < 2 or (len(cl) - suff) < 3 or not (0.25 <= suff / len(cl) <= 0.5):
        err(f"evidence cases need a healthy mix (about a third sufficient). Found {suff} sufficient of {len(cl)}")
    for c in cl:
        if not c["expected"]["evidence_sufficient"] and len(c["known_gaps"]) < 3:
            err(f"{c['id']}: insufficient-evidence cases need at least 3 known gaps")
        if not c["safe_interim"] or not c["reckless"]:
            err(f"{c['id']}: needs safe_interim and reckless lists")
for s in cur["sections"]:
    if s.get("requires_cases") and not exists("ai/evidence-cases.json"):
        err(f"{s['id']} requires evidence cases but ai/evidence-cases.json is missing")
if "R15" not in open(os.path.join(ROOT, "ai", "TUTOR_POLICY.md"), encoding="utf-8").read():
    err("TUTOR_POLICY.md must contain rule R15 (evidence cases)")

# 4. markdown relative links resolve; forbidden words absent
FORBIDDEN = ["seceon", "comtei"]
link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        if not f.endswith((".md", ".json", ".html", ".py", ".yml")):
            continue
        txt = open(p, encoding="utf-8", errors="ignore").read()
        low = txt.lower()
        if rel != os.path.join("scripts", "validate_repo.py"):
            for w in FORBIDDEN:
                if w in low:
                    err(f"{rel}: contains forbidden word '{w}'")
        if f.endswith(".md"):
            for m in link_re.finditer(txt):
                tgt = m.group(1).split("#")[0]
                if not tgt or tgt.startswith(("http://", "https://", "mailto:")):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(dp, tgt))):
                    err(f"{rel}: broken link -> {m.group(1)}")

print("\nOK: all checks passed." if not errors else f"\n{len(errors)} problem(s) found.")
sys.exit(1 if errors else 0)
