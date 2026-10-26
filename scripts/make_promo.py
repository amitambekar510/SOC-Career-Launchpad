#!/usr/bin/env python3
"""Build the LinkedIn promo GIF (1200x627) and a still cover image.

  python scripts/make_promo.py
"""
import os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_visuals as V
from make_visuals import font, ctext, box

W, H = 1200, 627
OUT = os.path.join(os.path.dirname(HERE), "promo")
os.makedirs(OUT, exist_ok=True)
NAVY, TEAL, AMBER, GREEN, RED, WHITE, SOFT = "#0B1F3A", "#14A3A5", "#F2B705", "#34C27A", "#E5533D", "#FFFFFF", "#BBD3EE"
TOTAL = 9


def base(step):
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 8), fill=TEAL)
    d.text((40, 572), "SOC-Career-Launchpad", font=font(22, True), fill=SOFT)
    for i in range(TOTAL):
        x = W - 40 - (TOTAL - i) * 26
        d.ellipse((x, 580, x + 12, 592), fill=TEAL if i == step else "#1C3558")
    return im, d


def shield(d, cx, cy, s, fill=TEAL):
    pts = [(cx, cy - s), (cx + .82 * s, cy - .6 * s), (cx + .82 * s, cy + .1 * s), (cx, cy + s), (cx - .82 * s, cy + .1 * s), (cx - .82 * s, cy - .6 * s)]
    d.polygon(pts, fill=fill)
    d.line([(cx - .35 * s, cy), (cx - .08 * s, cy + .3 * s), (cx + .42 * s, cy - .3 * s)], fill=WHITE, width=max(6, int(s / 8)))


def chip(d, x, y, text, fill=TEAL, fg=WHITE, size=26, pad=22):
    f = font(size, True)
    w = d.textlength(text, font=f) + pad * 2
    d.rounded_rectangle((x, y, x + w, y + size + 26), 26, fill=fill)
    d.text((x + pad, y + 12), text, font=f, fill=fg)
    return w


def chips_row(d, items, cx, y, size=26, gap=16, fills=None):
    f = font(size, True)
    widths = [d.textlength(t, font=f) + 44 for t in items]
    x = cx - (sum(widths) + gap * (len(items) - 1)) / 2
    for i, t in enumerate(items):
        chip(d, x, y, t, (fills[i] if fills else TEAL), size=size)
        x += widths[i] + gap


frames, durs = [], []
def add(im, ms):
    frames.append(im); durs.append(ms)


def scene_hook():
    for n, ms in ((1, 500), (2, 600), (3, 1300)):
        im, d = base(0)
        ctext(d, W / 2, 190, "Want a career in\ncybersecurity?", 76, True, WHITE, 10)
        if n == 2:
            ctext(d, W / 2, 410, "Plenty of tutorials. No clear path.", 42, False, SOFT, 8)
        if n >= 3:
            ctext(d, W / 2, 410, "So where do you even begin?", 48, True, AMBER, 8)
        add(im, ms)


def scene_intro():
    for n, ms in ((1, 600), (2, 1600)):
        im, d = base(1)
        shield(d, W / 2, 170, 95)
        ctext(d, W / 2, 330, "SOC-Career-Launchpad", 66, True, WHITE, 0)
        if n >= 2:
            ctext(d, W / 2, 440, "A plain-English, AI-ready tutor for the\nSecurity Operations Center (SOC)", 34, False, SOFT, 8)
        add(im, ms)


def scene_topics():
    items = ["Networking", "Linux", "Windows + AD", "Attacks", "SIEM", "EDR", "Incident Response", "Regulations"]
    for k in (2, 4, 6, 8):
        im, d = base(2)
        ctext(d, W / 2, 105, "Learn what a SOC analyst really does", 44, True, WHITE, 0)
        rows = [items[:4], items[4:]]
        for r, row in enumerate(rows):
            vis = [t for t in row if items.index(t) < k]
            if vis:
                chips_row(d, vis, W / 2, 230 + r * 110, 30)
        add(im, 420 if k < 8 else 1300)


def scene_ai_asks():
    steps = [(False, False), (True, False), (True, True)]
    for i, (user, ok) in enumerate(steps):
        im, d = base(3)
        ctext(d, W / 2, 85, "The AI asks first.  You answer.  Then it moves on.", 38, True, WHITE, 0)
        d.rounded_rectangle((70, 175, 960, 285), 28, fill=TEAL)
        d.text((100, 193), "AI Tutor", font=font(22, True), fill="#D9F4F4")
        d.text((100, 228), "Which port does Remote Desktop (RDP) use?", font=font(30, True), fill=WHITE)
        if user:
            d.rounded_rectangle((430, 320, 1130, 410), 28, fill=WHITE)
            d.text((460, 335), "You", font=font(22, True), fill="#5B6B82")
            d.text((460, 366), "3389", font=font(34, True), fill=NAVY)
        if ok:
            d.rounded_rectangle((70, 445, 790, 535), 28, fill="#145C3C")
            d.line([(105, 492), (125, 514), (162, 470)], fill=GREEN, width=9)
            d.text((185, 478), "Correct. Next question unlocked", font=font(30, True), fill=WHITE)
        add(im, 850 if not ok else 1500)


def scene_gate():
    names = ["Teach", "Check", "Gate", "Next"]
    for active in range(4):
        im, d = base(4)
        ctext(d, W / 2, 85, "No skipping. Pass to unlock the next section.", 38, True, WHITE, 0)
        for k, nm in enumerate(names):
            cx = 190 + k * 273
            on = k <= active
            d.ellipse((cx - 55, 215, cx + 55, 325), fill=TEAL if k == active else ("#1C6E70" if on else "#1C3558"))
            ctext(d, cx, 255, str(k + 1), 44, True, WHITE, 0)
            ctext(d, cx, 355, nm, 34, True, WHITE if on else "#6F86A8", 0)
            if k < 3:
                d.line((cx + 65, 270, cx + 208, 270), fill=TEAL if k < active else "#1C3558", width=8)
        if active == 3:
            chip(d, W / 2 - 245, 450, "Pass mark 80%  =  next section opens", GREEN, NAVY, 30)
        else:
            ctext(d, W / 2, 478, ["Read it with visuals and examples", "The AI asks the questions", "Score 80%+ to pass", ""][active], 32, False, SOFT, 0)
        add(im, 650 if active < 3 else 1500)


def scene_visuals():
    labels = ["Recon", "Weaponize", "Delivery", "Exploit", "Install", "C2", "Actions"]
    for k in range(1, 8):
        im, d = base(5)
        ctext(d, W / 2, 85, "See it, don't just read it", 46, True, WHITE, 0)
        for i, nm in enumerate(labels):
            x = 40 + i * 162
            fill = (GREEN if i in (2, 3) else TEAL) if i < k else "#1C3558"
            pts = [(x, 200), (x + 140, 200), (x + 162, 245), (x + 140, 290), (x, 290), (x + 22, 245)]
            d.polygon(pts, fill=fill)
            ctext(d, x + 88, 245, nm, 22, True, WHITE if i < k else "#6F86A8", 0)
        ctext(d, W / 2, 400, "Animated GIFs  ·  charts  ·  an interactive lab", 34, False, SOFT, 0)
        ctext(d, W / 2, 465, "Kill Chain  ·  alert lifecycle  ·  6-hour reporting clock", 28, False, "#7F9BC2", 0)
        add(im, 260 if k < 7 else 1300)


def scene_card():
    for k, pct in enumerate((0, 20, 40, 60)):
        im, d = base(6)
        ctext(d, W / 2, 85, "A progress card after every section", 46, True, WHITE, 0)
        box(d, (200, 160, 1000, 545), "#F4F7FB", TEAL, 22, 4)
        d.text((240, 180), "Learner Progress Card", font=font(32, True), fill=NAVY)
        d.rounded_rectangle((240, 238, 960, 274), 18, fill="#DDE3EC")
        if pct:
            d.rounded_rectangle((240, 238, 240 + 720 * pct / 100, 274), 18, fill=TEAL)
        d.text((240, 286), f"{pct}% of sections passed", font=font(26, True), fill=NAVY)
        rows = ["Networking", "Windows + AD", "Attacks", "SIEM"]
        passed = {0: 0, 1: 1, 2: 2, 3: 3}[k]
        for j, nm in enumerate(rows):
            y = 340 + j * 49
            if j < passed:
                shown, c = "PASSED", GREEN
            elif j == passed:
                shown, c = "UP NEXT", TEAL
            else:
                shown, c = "LOCKED", "#8A95A8"
            d.text((240, y + 4), nm, font=font(24), fill=NAVY)
            chip(d, 790, y - 6, shown, c, WHITE, 18, 16)
        if pct == 60:
            chip(d, 690, 176, "Level: Builder", AMBER, NAVY, 24)
        add(im, 520 if pct < 60 else 1500)


def scene_who():
    items = ["Freshers", "Career switchers", "Interns and L1", "Mentors and teams"]
    for k in (1, 2, 3, 4):
        im, d = base(7)
        ctext(d, W / 2, 105, "Built for everyone starting out", 50, True, WHITE, 0)
        vis = items[:k]
        for i, t in enumerate(vis):
            col = [TEAL, "#2F6FDE", AMBER, GREEN][i]
            fg = NAVY if col in (AMBER, GREEN) else WHITE
            x = 150 + (i % 2) * 450
            y = 240 + (i // 2) * 130
            d.rounded_rectangle((x, y, x + 400, y + 95), 28, fill=col)
            ctext(d, x + 200, y + 48, t, 32, True, fg, 0)
        add(im, 450 if k < 4 else 1300)


def scene_cta():
    for k in range(3):
        im, d = base(8)
        shield(d, W / 2, 130, 70)
        ctext(d, W / 2, 255, "Start learning SOC today", 58, True, WHITE, 0)
        ctext(d, W / 2, 335, "Free  ·  Open source  ·  Plain English  ·  AI-ready", 32, False, SOFT, 0)
        d.rounded_rectangle((60, 405, 1140, 495), 45, fill=AMBER if k % 2 == 0 else "#FFD54A")
        ctext(d, W / 2, 438, "github.com/amitambekar510/SOC-Career-Launchpad", 32, True, NAVY, 0)
        add(im, 800 if k < 2 else 2200)
    return im


scene_hook(); scene_intro(); scene_topics(); scene_ai_asks(); scene_gate(); scene_visuals(); scene_card(); scene_who()
last = scene_cta()
last.save(os.path.join(OUT, "linkedin-cover.png"))
pal = [f.convert("P", palette=Image.ADAPTIVE, colors=48) for f in frames]
path = os.path.join(OUT, "linkedin-promo.gif")
pal[0].save(path, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True, disposal=2)
print(f"{len(frames)} frames, {sum(durs)/1000:.1f} s, {os.path.getsize(path)/1024:.0f} KB -> {path}")
