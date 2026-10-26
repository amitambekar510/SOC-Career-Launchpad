#!/usr/bin/env python3
"""The learning gate. Read a section -> answer its checkpoint -> unlock the next.

  python scripts/checkpoint.py --init         # create your progress file
  python scripts/checkpoint.py                # take the next checkpoint
  python scripts/checkpoint.py --status       # see where you are
  python scripts/checkpoint.py --verify       # check your record is untampered
  python scripts/checkpoint.py --card         # make your progress card

The gate is a promise you make to yourself. It cannot physically stop you from
opening the files, but it records honestly, shows edits, and only YOU lose if you skip.
"""
import argparse, hashlib, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import progress_lib as P
from progress_card import render_card


def load_all():
    cur = P.load(P.CURRICULUM)
    bank = P.load(P.BANK)
    if os.path.exists(P.PROGRESS):
        prog = P.load(P.PROGRESS)
    else:
        prog = None
    return cur, bank, prog


def ahash(bank, qid, letter):
    return hashlib.sha256(f"{bank['salt']}:{qid}:{letter}".encode()).hexdigest()


def cmd_init(args):
    if os.path.exists(P.PROGRESS) and not args.force:
        print("A progress file already exists. Use --force to start over (this erases your record).")
        return 1
    name = args.name or input("Your name: ").strip() or "Learner"
    goal = args.goal or "SOC Analyst (L1)"
    P.save(P.PROGRESS, P.new_progress(name, goal))
    os.makedirs(P.NOTES_DIR, exist_ok=True)
    print(f"Created learner/progress.json for {name}. Run: python scripts/checkpoint.py")
    return 0


def print_status(cur, prog):
    ok, bad = P.verify_chain(prog["chain"])
    st = P.derive_status(cur, prog["chain"] if ok else [])
    print(f"\nRecord: {'VERIFIED' if ok else 'UNVERIFIED (edited at entry %s)' % bad}")
    for s in P.gated(cur):
        x = st[s["id"]]
        tag = "PASSED" if x["passed"] else ("in progress" if x["attempts"] else "locked")
        extra = ""
        if s.get("requires_cases"):
            extra = f", evidence cases: {x['cases_n']}/{s['requires_cases']['min_cases']}" + (f" (avg {x['cases_avg']}%)" if x["cases_avg"] is not None else "")
        print(f"  [{tag:11}] {s['title']}  (best: {x['best'] if x['best'] is not None else '-'}%, attempts: {x['attempts']}{extra})")
    return ok, st


def cmd_run(args):
    cur, bank, prog = load_all()
    if prog is None:
        print("No progress file yet. Run: python scripts/checkpoint.py --init")
        return 1
    ok, st = print_status(cur, prog)
    if not ok:
        print("\nYour progress file was edited outside this tool, so the gate is closed.")
        print("Restore the original file, or start fresh with: python scripts/checkpoint.py --init --force")
        return 2
    sec = P.next_section(cur, st)
    if args.section:
        want = next((s for s in cur["sections"] if s["id"] == args.section), None)
        if not want:
            print("Unknown section id.")
            return 1
        if want.get("gated") and not P.is_unlocked(cur, st, want["id"]):
            print(f"\nLOCKED: '{want['title']}' opens only after you pass the sections before it.")
            return 3
        sec = want if want.get("gated") else None
    if sec is None:
        print("\nAll gated sections are complete. Run --card for your card, then take the capstone with your AI tutor.")
        return 0

    pass_mark = cur["pass_mark_percent"]
    req = sec.get("requires_cases")
    if req and st[sec["id"]]["mcq_passed"] and not st[sec["id"]]["passed"]:
        print(f"\nYour quiz for '{sec['title']}' is passed. One more step: evidence cases.")
        print(f"Work through at least {req['min_cases']} cases from ai/evidence-cases.json with your AI tutor or a mentor")
        print(f"(average reasoning score {req['min_avg_percent']}%+). Reasoning needs a human or AI grader, so the script can't mark it itself.")
        print("When a case is graded, record it:  python scripts/checkpoint.py --record-case <case-id> --verdict <close|escalate|insufficient> --points N --max M --source ai-tutor")
        return 0
    print(f"\n=== Checkpoint: {sec['title']} ===")
    print("Read these first:")
    for f in sec["files"]:
        print("  -", f)
    print("\nThe gate works on honesty. Type exactly:  I HAVE READ IT   to continue.")
    if input("> ").strip() != "I HAVE READ IT":
        print("Go and read the section first. The questions will be here when you're ready.")
        return 0

    qs = [q for q in bank["questions"] if q["section"] == sec["id"] and q["type"] == "mcq"]
    random.shuffle(qs)
    correct = 0
    missed = []
    for n, q in enumerate(qs, 1):
        print(f"\nQ{n}/{len(qs)}. {q['prompt']}")
        for letter, text in q["options"].items():
            print(f"   {letter}) {text}")
        ans = ""
        while ans not in q["options"]:
            try:
                ans = input("Your answer (A/B/C/D): ").strip().upper()
            except EOFError:
                print("\nNo input received. Stopping without recording an attempt.")
                return 0
        if ahash(bank, q["id"], ans) == q["answer_hash"]:
            correct += 1
        else:
            missed.append(q["objective"])
    percent = round(100 * correct / len(qs))
    passed = percent >= pass_mark
    P.append_entry(prog, sec["id"], correct, len(qs), passed)
    P.save(P.PROGRESS, prog)
    print(f"\nScore: {correct}/{len(qs)} ({percent}%).  Pass mark: {pass_mark}%.")
    if passed and req:
        print("QUIZ PASSED. This section also needs evidence cases (graded by an AI tutor or mentor) before the next one unlocks.")
        print(f"Do at least {req['min_cases']} cases from ai/evidence-cases.json; then record each with --record-case.")
    elif passed:
        print("PASSED. The next section is now unlocked.")
        sc = [q for q in bank["questions"] if q["section"] == sec["id"] and q["type"] == "scenario"]
        if sc:
            print("\nBonus (not gated): talk this scenario through with your AI tutor or mentor:\n  " + sc[0]["prompt"])
    else:
        print("Not yet. Nothing is lost: re-read the parts below, then try again.")
        for m in dict.fromkeys(missed):
            print("  - Review:", m)
    cur_prog = P.load(P.PROGRESS)
    render_card(cur_prog, cur, os.path.join(P.ROOT, "learner", "progress-card.png"),
                os.path.join(P.ROOT, "learner", "progress-card.md"))
    print("\nProgress card updated: learner/progress-card.png")
    return 0


def cmd_record(args):
    """For AI tutors with shell access that ran the checkpoint conversationally."""
    cur, bank, prog = load_all()
    if prog is None:
        print("No progress file. Run --init first.")
        return 1
    ok, st = P.verify_chain(prog["chain"])[0], None
    if not ok:
        print("Record is unverified; refusing to add entries.")
        return 2
    st = P.derive_status(cur, prog["chain"])
    if not P.is_unlocked(cur, st, args.record):
        print("LOCKED: that section is not unlocked yet.")
        return 3
    passed = round(100 * args.correct / args.total) >= cur["pass_mark_percent"]
    P.append_entry(prog, args.record, args.correct, args.total, passed, source=args.source)
    P.save(P.PROGRESS, prog)
    print("Recorded.", "PASSED" if passed else "not passed")
    return 0


def cmd_record_case(args):
    """Record one graded evidence case (graded by an AI tutor or a mentor, never self-scored for the gate)."""
    cur, bank, prog = load_all()
    if prog is None:
        print("No progress file. Run --init first.")
        return 1
    ok = P.verify_chain(prog["chain"])[0]
    if not ok:
        print("Record is unverified; refusing to add entries.")
        return 2
    cases = P.load(os.path.join(P.ROOT, "ai", "evidence-cases.json"))["cases"]
    if args.record_case not in [c["id"] for c in cases]:
        print("Unknown case id. See ai/evidence-cases.json")
        return 1
    if args.verdict not in P.CASE_VERDICTS:
        print("--verdict must be one of: " + ", ".join(P.CASE_VERDICTS))
        return 1
    if args.points is None or not args.max or not (0 <= args.points <= args.max):
        print("--points and --max are required and must satisfy 0 <= points <= max")
        return 1
    st = P.derive_status(cur, prog["chain"])
    if not P.is_unlocked(cur, st, "s20-incomplete-evidence"):
        print("LOCKED: the evidence-case section is not unlocked yet.")
        return 3
    P.append_case(prog, args.record_case, args.verdict, args.points, args.max,
                  premature_close=args.premature_close, source=args.source)
    P.save(P.PROGRESS, prog)
    counted = args.source in P.COUNTING_SOURCES
    print("Recorded." + ("" if counted else " (source 'self' is saved for your own reflection but does not count toward the gate.)"))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--name")
    ap.add_argument("--goal")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--card", action="store_true")
    ap.add_argument("--section")
    ap.add_argument("--record", help="section id (AI tutor use)")
    ap.add_argument("--correct", type=int)
    ap.add_argument("--total", type=int)
    ap.add_argument("--source", default="ai-tutor")
    ap.add_argument("--record-case", dest="record_case", help="evidence case id (AI tutor or mentor use)")
    ap.add_argument("--verdict")
    ap.add_argument("--points", type=int)
    ap.add_argument("--max", type=int)
    ap.add_argument("--premature-close", dest="premature_close", action="store_true")
    a = ap.parse_args()

    if a.init:
        return cmd_init(a)
    if a.record_case:
        return cmd_record_case(a)
    if a.record:
        if a.correct is None or not a.total:
            print("--record needs --correct and --total")
            return 1
        return cmd_record(a)
    cur, bank, prog = load_all()
    if a.status or a.verify or a.card:
        if prog is None:
            print("No progress file yet. Run --init")
            return 1
        if a.status:
            print_status(cur, prog)
        if a.verify:
            ok, bad = P.verify_chain(prog["chain"])
            print("Record intact." if ok else f"Record was edited at entry {bad}.")
            return 0 if ok else 2
        if a.card:
            render_card(prog, cur, os.path.join(P.ROOT, "learner", "progress-card.png"),
                        os.path.join(P.ROOT, "learner", "progress-card.md"))
            print("Card written to learner/progress-card.png")
        return 0
    return cmd_run(a)


if __name__ == "__main__":
    sys.exit(main())
