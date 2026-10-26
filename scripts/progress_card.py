#!/usr/bin/env python3
"""Render the learner's progress card (PNG + Markdown).

  python scripts/progress_card.py            # uses learner/progress.json
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import progress_lib as P

NAVY, TEAL, GREEN, AMBER, RED = "#0B1F3A", "#0F8B8D", "#2E9E5B", "#E0A800", "#C0392B"
BG, CARD, GRAY, TXT = "#F4F7FB", "#FFFFFF", "#DDE3EC", "#1B2A41"
MUTED_C = "#5B6B82"


def font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for base in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/", ""):
        for n in names:
            try:
                return ImageFont.truetype(base + n, size)
            except OSError:
                pass
    return ImageFont.load_default(size=size)


def render_card(progress, curriculum, out_png, out_md=None):
    chain = progress.get("chain", [])
    ok, bad = P.verify_chain(chain)
    status = P.derive_status(curriculum, chain if ok else [])
    gs = P.gated(curriculum)
    passed = sum(1 for s in gs if status[s["id"]]["passed"])
    pct = round(100 * passed / len(gs))
    level = P.level_title(passed, len(gs))
    nxt = P.next_section(curriculum, status)
    notes = P.count_notes()
    rs = P.derive_reasoning(chain if ok else [])
    learner = progress.get("learner", {})

    W, H = 1100, 150 + 44 * len(gs) + 330
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 110), fill=NAVY)
    d.text((36, 28), "SOC-Career-Launchpad", font=font(30, True), fill="white")
    d.text((36, 70), "Learner Progress Card", font=font(18), fill="#BBD3EE")

    if not chain:
        badge, bcol = "NO DATA YET", GRAY
    elif ok:
        badge, bcol = "VERIFIED RECORD", GREEN
    else:
        badge, bcol = f"UNVERIFIED (edited at entry {bad})", RED
    tw = d.textlength(badge, font=font(16, True))
    d.rounded_rectangle((W - tw - 70, 34, W - 30, 76), 18, fill=bcol)
    d.text((W - tw - 50, 45), badge, font=font(16, True), fill="white")

    y = 128
    d.text((36, y), f"{learner.get('name','Learner')}  ·  goal: {learner.get('goal','')}",
           font=font(20, True), fill=TXT)
    d.text((W - 36, y + 2), f"Level: {level}", font=font(20, True), fill=TEAL, anchor="ra")
    y += 44
    d.rounded_rectangle((36, y, W - 36, y + 26), 13, fill=GRAY)
    if pct:
        d.rounded_rectangle((36, y, 36 + (W - 72) * pct / 100, y + 26), 13, fill=TEAL)
    d.text((W / 2, y + 13), f"{passed} of {len(gs)} sections passed  ({pct}%)", font=font(15, True),
           fill="white" if pct > 45 else TXT, anchor="mm")
    y += 50

    for s in gs:
        st = status[s["id"]]
        d.rounded_rectangle((36, y, W - 36, y + 38), 10, fill=CARD, outline=GRAY)
        d.text((52, y + 9), s["title"][:48], font=font(16), fill=TXT)
        req = s.get("requires_cases")
        if req and st["mcq_passed"] and not st["passed"]:
            label, col = f"QUIZ PASSED  ·  evidence cases {st['cases_n']}/{req['min_cases']}", AMBER
        elif st["passed"]:
            label, col = f"PASSED  best {st['best']}%  ·  {st['attempts']} attempt(s)", GREEN
        elif st["attempts"]:
            label, col = f"IN PROGRESS  best {st['best']}%  ·  {st['attempts']} attempt(s)", AMBER
        elif nxt and nxt["id"] == s["id"]:
            label, col = "UP NEXT", TEAL
        else:
            label, col = "LOCKED", "#8A95A8"
        lw = d.textlength(label, font=font(14, True))
        d.rounded_rectangle((W - 52 - lw - 20, y + 6, W - 52, y + 32), 12, fill=col)
        d.text((W - 62, y + 19), label, font=font(14, True), fill="white", anchor="rm")
        y += 44

    y += 6
    d.rounded_rectangle((36, y, W - 36, y + 112), 12, fill=CARD, outline=GRAY)
    d.text((52, y + 10), "Evidence reasoning  (scored separately from quiz accuracy)", font=font(16, True), fill=NAVY)
    avg_txt = f"{rs['avg']}%" if rs["avg"] is not None else "-"
    d.text((52, y + 40), f"Cases graded: {rs['cases']}   ·   Average reasoning: {avg_txt}   ·   Premature closes: {rs['premature_closes']}",
           font=font(15), fill=TXT)
    jcol = GREEN if rs["label"].startswith("Knows") else (GRAY if rs["label"] == "Not started" else AMBER)
    d.text((52, y + 72), "Judgment:", font=font(15, True), fill=TXT)
    d.text((150, y + 72), rs["label"], font=font(15, True), fill=jcol if jcol != GRAY else MUTED_C)
    y += 130
    strong = [s["title"].split(":")[0] for s in gs if status[s["id"]]["passed"] and status[s["id"]]["attempts"] == 1]
    weak = [s["title"].split(":")[0] for s in gs if status[s["id"]]["attempts"] >= 2 or
            (status[s["id"]]["best"] is not None and status[s["id"]]["best"] < 100)]
    d.text((36, y), "Strong (passed first try): " + (", ".join(strong[:4]) or "-"), font=font(15), fill=GREEN)
    d.text((36, y + 26), "Review again: " + (", ".join(weak[:4]) or "-"), font=font(15), fill=AMBER)
    d.text((36, y + 52), f"Learner notes written: {notes}   ·   Next step: " +
           (nxt["title"] if nxt else "All gated sections complete. Take the capstone review with your AI tutor."),
           font=font(15), fill=TXT)
    d.text((36, y + 88), "Gate rule: no section opens until the previous checkpoint is passed (80%+).",
           font=font(13), fill="#5B6B82")

    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    im.save(out_png)
    if out_md:
        lines = [f"# Progress Card: {learner.get('name','Learner')}", "",
                 f"**Record:** {badge}  |  **Level:** {level}  |  **Passed:** {passed}/{len(gs)} ({pct}%)", "",
                 "| Section | Status | Best | Attempts |", "|---|---|---|---|"]
        for s in gs:
            st = status[s["id"]]
            lines.append(f"| {s['title']} | {'PASSED' if st['passed'] else ('IN PROGRESS' if st['attempts'] else 'LOCKED/NEXT')} | "
                         f"{st['best'] if st['best'] is not None else '-'} | {st['attempts']} |")
        lines += ["", f"**Evidence reasoning:** {rs['cases']} case(s) graded · average {rs['avg'] if rs['avg'] is not None else '-'}% · premature closes {rs['premature_closes']} · {rs['label']}", f"**Notes written:** {notes}", f"**Next:** {nxt['title'] if nxt else 'All gated sections complete'}"]
        with open(out_md, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return out_png


if __name__ == "__main__":
    cur = P.load(P.CURRICULUM)
    prog = P.load(P.PROGRESS) if os.path.exists(P.PROGRESS) else P.new_progress()
    render_card(prog, cur, os.path.join(P.ROOT, "learner", "progress-card.png"),
                os.path.join(P.ROOT, "learner", "progress-card.md"))
    print("Progress card written to learner/progress-card.png and .md")
