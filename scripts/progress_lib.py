"""Shared helpers: progress file, tamper-evident chain, gating logic.

HONEST NOTE: this chain makes casual edits *visible* (the card shows UNVERIFIED).
It is not cryptographic security - anyone with the repo can rebuild it.
The point is a clear, fair record for the learner, not a lock for a vault.
"""
import datetime, hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRICULUM = os.path.join(ROOT, "ai", "curriculum.json")
BANK = os.path.join(ROOT, "ai", "question-bank.json")
PROGRESS = os.path.join(ROOT, "learner", "progress.json")
NOTES_DIR = os.path.join(ROOT, "learner", "notes")
GENESIS = "0" * 64


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canon(entry):
    return json.dumps({k: v for k, v in entry.items() if k != "hash"}, sort_keys=True, separators=(",", ":"))


def entry_hash(entry):
    return hashlib.sha256((entry["prev"] + _canon(entry)).encode()).hexdigest()


def verify_chain(chain):
    """Return (ok, index_of_first_bad_entry_or_None)."""
    prev = GENESIS
    for i, e in enumerate(chain):
        if e.get("i") != i or e.get("prev") != prev or e.get("hash") != entry_hash(e):
            return False, i
        prev = e["hash"]
    return True, None


def new_progress(name="Learner", goal="SOC Analyst (L1)"):
    return {"learner": {"name": name, "goal": goal, "started": now()[:10]}, "chain": []}


def append_entry(progress, section, correct, total, passed, source="checkpoint-cli"):
    chain = progress["chain"]
    entry = {"i": len(chain), "ts": now(), "section": section, "correct": correct,
             "total": total, "percent": round(100 * correct / total) if total else 0,
             "passed": bool(passed), "source": source,
             "prev": chain[-1]["hash"] if chain else GENESIS}
    entry["hash"] = entry_hash(entry)
    chain.append(entry)
    return entry


def derive_status(curriculum, chain):
    status = {}
    for s in curriculum["sections"]:
        status[s["id"]] = {"attempts": 0, "best": None, "passed": False}
    for e in chain:
        st = status.get(e["section"])
        if not st:
            continue
        st["attempts"] += 1
        st["best"] = e["percent"] if st["best"] is None else max(st["best"], e["percent"])
        st["passed"] = st["passed"] or e["passed"]
    return status


def gated(curriculum):
    return [s for s in curriculum["sections"] if s.get("gated")]


def next_section(curriculum, status):
    for s in gated(curriculum):
        if not status[s["id"]]["passed"]:
            return s
    return None


def is_unlocked(curriculum, status, section_id):
    for s in gated(curriculum):
        if s["id"] == section_id:
            return True
        if not status[s["id"]]["passed"]:
            return False
    return True  # optional sections are open once the program is started


def level_title(passed_count, total):
    if passed_count == 0:
        return "Starting out"
    if passed_count >= total:
        return "SOC-Ready"
    ratio = passed_count / total
    if ratio < 0.34:
        return "Explorer"
    if ratio < 0.67:
        return "Builder"
    return "Defender"


def count_notes():
    if not os.path.isdir(NOTES_DIR):
        return 0
    return len([f for f in os.listdir(NOTES_DIR)
                if f.endswith(".md") and f.lower() not in ("readme.md", "notes-template.md")])
