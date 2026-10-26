#!/usr/bin/env python3
"""Build the learner-facing question bank (hashed answers, no explanations)
from the AI-only source of truth.

  python scripts/build_question_bank.py
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "ai", "_ai-only", "questions.source.json")
OUT = os.path.join(ROOT, "ai", "question-bank.json")
CASES_SRC = os.path.join(ROOT, "ai", "_ai-only", "evidence-cases.source.json")
CASES_OUT = os.path.join(ROOT, "ai", "evidence-cases.json")
SALT = "soc-career-launchpad:v1"


def answer_hash(qid: str, letter: str) -> str:
    return hashlib.sha256(f"{SALT}:{qid}:{letter}".encode()).hexdigest()


def build() -> dict:
    src = json.load(open(SRC, encoding="utf-8"))["questions"]
    questions = []
    for q in src:
        if q["type"] == "mcq":
            questions.append({
                "id": q["id"], "section": q["section"], "type": "mcq",
                "objective": q["objective"], "prompt": q["prompt"],
                "options": q["options"], "answer_hash": answer_hash(q["id"], q["answer"]),
            })
        else:
            questions.append({"id": q["id"], "section": q["section"], "type": "scenario",
                              "prompt": q["prompt"]})
    return {"version": 1, "salt": SALT,
            "note": "Answers are stored only as hashes here. Scenario answers are checked by an AI tutor or a human mentor.",
            "questions": questions}


def build_cases() -> dict:
    """Learner-facing evidence cases: the alert and the evidence only. No verdicts, gaps or rubrics."""
    src = json.load(open(CASES_SRC, encoding="utf-8"))
    return {"version": 1,
            "note": "Present each case exactly as written and ask the prompts in order. Grading is done by an AI tutor or a mentor.",
            "verdict_options": {"close": "Close it (false positive or benign)",
                                "escalate": "Escalate it",
                                "insufficient": "Insufficient evidence, keep it open and get more data"},
            "prompts": src["prompts"],
            "cases": [{"id": c["id"], "title": c["title"], "alert": c["alert"],
                       "context": c["context"], "evidence": c["evidence"]} for c in src["cases"]]}


if __name__ == "__main__":
    bank = build()
    json.dump(bank, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {OUT} ({len(bank['questions'])} items)")
    cases = build_cases()
    json.dump(cases, open(CASES_OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {CASES_OUT} ({len(cases['cases'])} cases)")
