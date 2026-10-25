#!/usr/bin/env python3
"""Generate every picture, chart and animated GIF in /visuals from code.

  pip install pillow
  python scripts/make_visuals.py

Because they are generated, anyone can tweak the numbers or colours and rebuild,
and the GitHub Action keeps them fresh.
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "visuals")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)

NAVY, TEAL, GREEN, AMBER, RED = "#0B1F3A", "#0F8B8D", "#2E9E5B", "#E0A800", "#C0392B"
BG, CARD, GRAY, TXT, MUTED, BLUE = "#F4F7FB", "#FFFFFF", "#DDE3EC", "#1B2A41", "#5B6B82", "#2F6FDE"


def font(size, bold=False):
    n = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/", ""):
        try:
            return ImageFont.truetype(base + n, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def canvas(w, h, bg=BG):
    im = Image.new("RGB", (w, h), bg)
    return im, ImageDraw.Draw(im)


def box(d, xy, fill=CARD, outline=GRAY, r=14, w=2):
    d.rounded_rectangle(xy, r, fill=fill, outline=outline, width=w)


def ctext(d, cx, cy, s, size=16, bold=False, fill=TXT, gap=4):
    lines = s.split("\n")
    f = font(size, bold)
    total = len(lines) * size + (len(lines) - 1) * gap
    y = cy - total / 2
    for ln in lines:
        d.text((cx, y), ln, font=f, fill=fill, anchor="ma")
        y += size + gap


def save_gif(frames, durations, name):
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=96) for f in frames]
    pal[0].save(os.path.join(OUT, name), save_all=True, append_images=pal[1:],
                duration=durations, loop=0, optimize=True, disposal=2)
    print("wrote", name, f"{os.path.getsize(os.path.join(OUT, name))//1024} KB")


def save_png(im, name):
    im.save(os.path.join(OUT, name))
    print("wrote", name)


def header(d, w, title, sub=None):
    d.rectangle((0, 0, w, 70), fill=NAVY)
    d.text((28, 16), title, font=font(24, True), fill="white")
    if sub:
        d.text((28, 46), sub, font=font(14), fill="#BBD3EE")


# ------------------------------------------------------------------ STATIC PNGs
def regulation_map():
    W, H = 1100, 640
    im, d = canvas(W, H)
    header(d, W, "Regulations and standards at a glance", "Left: rules you MUST follow (India)   ·   Right: methods and checklists (global)")
    d.text((60, 92), "INDIA: LAWS AND REGULATORS", font=font(16, True), fill=RED)
    d.text((640, 92), "GLOBAL: STANDARDS AND FRAMEWORKS", font=font(16, True), fill=BLUE)
    left = [("CERT-In Directions (2022)", "Report in 6 hours  ·  keep logs 180 days"),
            ("SEBI CSCRF (2024)", "Securities market  ·  tiered controls  ·  SOC"),
            ("RBI frameworks", "Banks, NBFCs, payment operators"),
            ("DPDP Act 2023 + Rules 2025", "Personal data  ·  72-hour breach report")]
    right = [("ISO/IEC 27001", "Security management system (certifiable)"),
             ("NIST CSF 2.0", "6 functions: Govern, Identify, Protect, Detect, Respond, Recover"),
             ("MITRE ATT&CK", "How attackers behave (14 tactics)"),
             ("ISO/IEC 27090", "Security threats to AI systems"),
             ("ISO/IEC 42001:2023", "AI management system (certifiable)")]
    y = 125
    for t, s in left:
        box(d, (40, y, 500, y + 82), CARD, RED)
        d.text((60, y + 14), t, font=font(18, True), fill=NAVY)
        d.text((60, y + 46), s, font=font(14), fill=MUTED)
        y += 100
    y = 125
    for t, s in right:
        box(d, (620, y, 1060, y + 70), CARD, BLUE)
        d.text((640, y + 10), t, font=font(18, True), fill=NAVY)
        d.text((640, y + 40), s, font=font(12), fill=MUTED)
        y += 80
    for yy in (166, 266, 366, 466):
        d.line((500, yy, 540, 310), fill="#B8C3D4", width=3)
    for yy in (160, 240, 320, 400, 480):
        d.line((620, yy, 580, 310), fill="#B8C3D4", width=3)
    d.ellipse((505, 255, 615, 365), fill=TEAL)
    ctext(d, 560, 296, "Your\nSOC", 20, True, "white", 2)
    d.text((40, 600), "Laws set the minimum you must meet. Frameworks help you do it well. Always confirm with your compliance team.",
           font=font(14), fill=MUTED)
    save_png(im, "regulation-map.png")


def reporting_clocks():
    W, H = 1000, 430
    im, d = canvas(W, H)
    header(d, W, "Three numbers every SOC beginner remembers", "6 hours · 72 hours · 180 days")
    x0, x1 = 120, 920
    d.text((40, 100), "Reporting windows (hours, to scale)", font=font(16, True), fill=NAVY)
    rows = [("CERT-In: report incident", 6, RED), ("DPDP: detailed breach report", 72, AMBER)]
    y = 140
    for label, hrs, col in rows:
        d.text((40, y), label, font=font(15), fill=TXT)
        bw = (x1 - x0) * hrs / 72
        d.rounded_rectangle((x0 + 150, y + 26, x0 + 150 + (x1 - x0 - 150) * hrs / 72, y + 56), 8, fill=col)
        d.text((x0 + 150 + (x1 - x0 - 150) * hrs / 72 + 10, y + 30), f"{hrs} h", font=font(18, True), fill=TXT)
        y += 80
    d.text((40, 300), "Log retention", font=font(16, True), fill=NAVY)
    box(d, (40, 330, 480, 400), CARD, TEAL)
    ctext(d, 260, 365, "CERT-In: 180 days rolling\n(logs of all ICT systems, kept in India)", 15, False, TXT)
    box(d, (520, 330, 960, 400), CARD, TEAL)
    ctext(d, 740, 365, "DPDP Rules: certain logs kept 1 year\n(for breach detection and investigation)", 15, False, TXT)
    save_png(im, "reporting-clocks.png")


def regulation_timeline():
    W, H = 1200, 520
    im, d = canvas(W, H)
    header(d, W, "Timeline of the key dates", "Dates as of October 2026. Verify on official sources.")
    x0, x1, y = 70, 1130, 270
    y0, y1 = 2022, 2028.5
    X = lambda yr: x0 + (x1 - x0) * (yr - y0) / (y1 - y0)
    d.line((x0, y, x1, y), fill=NAVY, width=5)
    for yr in range(2022, 2029):
        d.line((X(yr), y - 10, X(yr), y + 10), fill=NAVY, width=3)
        d.text((X(yr), y + 16), str(yr), font=font(14, True), fill=NAVY, anchor="ma")
    ev = [(2022.32, "CERT-In Directions\nissued 28 Apr 2022", RED, -1, 1, 20),
          (2023.95, "ISO/IEC 42001\npublished Dec 2023", BLUE, 1, 1, -95),
          (2024.15, "NIST CSF 2.0\nFeb 2024", BLUE, -1, 2, -50),
          (2024.25, "RBI IT Governance MD\neffective 1 Apr 2024", RED, 1, 2, 95),
          (2024.58, "SEBI CSCRF 20 Aug 2024\nRBI PSO cyber MD 30 Jul 2024", RED, -1, 1, 40),
          (2025.66, "CSCRF final extended\ndeadline 31 Aug 2025", RED, 1, 1, -30),
          (2025.87, "DPDP Rules\nnotified 13 Nov 2025", RED, -1, 2, 0),
          (2026.25, "RBI: medium PSOs\n1 Apr 2026", RED, 1, 2, 60),
          (2027.4, "DPDP phased duties\nfully in force ~May 2027", RED, -1, 1, 0),
          (2028.25, "RBI: small PSOs\n1 Apr 2028", RED, 1, 1, -30)]
    for yr, label, col, side, tier, dx in ev:
        x = X(yr)
        ty = y + side * (75 if tier == 1 else 155)
        w = max(170, 7.4 * max(len(t) for t in label.split(chr(10))) + 24)
        d.line((x, y, x + dx, ty - side * 28), fill=col, width=2)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=col)
        box(d, (x + dx - w / 2, ty - 28, x + dx + w / 2, ty + 28), CARD, col, 10, 2)
        ctext(d, x + dx, ty, label, 12, False, TXT, 2)
    d.rectangle((70, 480, 90, 494), fill=RED); d.text((98, 478), "India: must follow", font=font(13), fill=TXT)
    d.rectangle((290, 480, 310, 494), fill=BLUE); d.text((318, 478), "Global standard", font=font(13), fill=TXT)
    save_png(im, "regulation-timeline.png")


def siem_pipeline():
    W, H = 1100, 470
    im, d = canvas(W, H)
    header(d, W, "How any SIEM works", "Same steps, whichever product you use")
    d.text((46, 90), "LOG SOURCES:  firewalls  ·  servers  ·  endpoints (EDR)  ·  identity  ·  cloud  ·  apps", font=font(15, True), fill=MUTED)
    steps = [("1  Collect", "agents,\nforwarders,\nconnectors, syslog", TEAL),
             ("2  Parse", "split raw log\nlines into\nfields", TEAL),
             ("3  Normalise", "same field\nnames for\nevery source", TEAL),
             ("4  Enrich", "user, asset\nowner, threat\nintel", BLUE),
             ("5  Store", "index for fast\nsearch, keep\nper policy", BLUE),
             ("6  Detect", "rules,\nthresholds,\ncorrelation", AMBER),
             ("7  Alert", "you triage\nand\ninvestigate", RED)]
    bw, gap, x = 132, 14, 46
    for i, (t, sub, col) in enumerate(steps):
        box(d, (x, 130, x + bw, 330), CARD, col, 14, 3)
        d.rounded_rectangle((x, 130, x + bw, 178), 14, fill=col)
        ctext(d, x + bw / 2, 154, t, 15, True, "white", 0)
        ctext(d, x + bw / 2, 240, sub, 13, False, TXT, 4)
        if i < len(steps) - 1:
            d.polygon([(x + bw + 2, 230), (x + bw + gap - 1, 238), (x + bw + 2, 246)], fill=MUTED)
        x += bw + gap
    box(d, (46, 360, 1054, 440), "#FFF8E1", AMBER, 12, 2)
    ctext(d, 550, 386, "Silent SIEM = warning sign.  If a source stops sending logs, an outage or an attacker may be why.", 15, True, TXT, 0)
    ctext(d, 550, 418, "Learn the idea once. Elastic, Splunk, Sentinel, QRadar and Wazuh all follow it.", 14, False, MUTED, 0)
    save_png(im, "siem-pipeline.png")


def arrow(d, a, b, col=MUTED, w=4):
    d.line((a, b), fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for da in (2.6, -2.6):
        d.line((b, (b[0] + 14 * math.cos(ang + da), b[1] + 14 * math.sin(ang + da))), fill=col, width=w)


def ir_lifecycle():
    W, H = 1000, 540
    im, d = canvas(W, H)
    header(d, W, "The incident response lifecycle", "NIST SP 800-61 Rev. 2 phases, with the SANS six steps underneath")
    boxes = {"prep": (500, 150, "1  Preparation", "Preparation", TEAL),
             "det": (790, 290, "2  Detection and Analysis", "Identification", BLUE),
             "con": (500, 424, "3  Containment, Eradication\nand Recovery", "Containment · Eradication · Recovery", AMBER),
             "post": (210, 290, "4  Post-Incident Activity", "Lessons learned", GREEN)}
    for k, (cx, cy, t, sub, col) in boxes.items():
        box(d, (cx - 150, cy - 42, cx + 150, cy + 42), CARD, col, 14, 4)
        ctext(d, cx, cy - 8, t, 14, True, NAVY, 2)
        ctext(d, cx, cy + 28 if "\n" in t else cy + 22, "SANS: " + sub, 11, False, MUTED, 0)
    arrow(d, (640, 165), (735, 245), MUTED)
    arrow(d, (745, 335), (620, 405), MUTED)
    arrow(d, (380, 410), (270, 335), MUTED)
    arrow(d, (160, 245), (370, 160), MUTED)
    ctext(d, 500, 290, "Every incident feeds\nthe next round of\npreparation", 15, True, TEAL, 4)
    box(d, (40, 488, 960, 528), "#E8F6F3", TEAL, 10, 2)
    ctext(d, 500, 508, "NIST SP 800-61 Rev. 3 (2025) now maps IR onto the six CSF 2.0 functions: Govern, Identify, Protect, Detect, Respond, Recover", 12, False, TXT, 0)
    save_png(im, "ir-lifecycle.png")


def career_map():
    W, H = 1100, 520
    im, d = canvas(W, H)
    header(d, W, "From learner to specialist", "Many routes. Skills and labs matter at every step")
    path = [("Foundations", "networking, Windows,\nLinux, security basics", TEAL),
            ("SOC Intern / L1", "triage, escalate,\ndocument", BLUE),
            ("L2 Analyst", "investigate,\ncontain, tune", AMBER),
            ("L3 / Hunter / IR", "hunt, lead incidents,\nmentor", RED)]
    xs = [40, 300, 560, 820]
    for (t, sub, col), x in zip(path, xs):
        box(d, (x, 100, x + 240, 200), CARD, col, 14, 4)
        ctext(d, x + 120, 130, t, 17, True, NAVY, 0)
        ctext(d, x + 120, 168, sub, 12, False, MUTED, 3)
    for x in (280, 540, 800):
        arrow(d, (x, 150), (x + 20, 150), MUTED, 4)
    ctext(d, 550, 245, "Branch out from L2 / L3 into...", 15, True, NAVY, 0)
    spec = ["Threat\nIntelligence", "Detection\nEngineering", "DFIR\n(forensics + IR)", "Cloud\nSecurity", "SOC Lead /\nManager", "Red Team /\nPen Testing"]
    d.line((120, 285, 995, 285), fill=MUTED, width=3)
    d.line((680, 200, 680, 285), fill=MUTED, width=3)
    d.line((940, 200, 940, 285), fill=MUTED, width=3)
    for i, sname in enumerate(spec):
        x = 40 + i * 175
        d.line((x + 80, 285, x + 80, 320), fill=MUTED, width=3)
        box(d, (x, 320, x + 160, 390), CARD, TEAL, 12, 3)
        ctext(d, x + 80, 355, sname, 14, True, NAVY, 2)
    box(d, (40, 430, 1060, 490), "#FFF8E1", AMBER, 12, 2)
    ctext(d, 550, 450, "Certifications can open doors, but a lab portfolio and clear thinking win interviews.", 15, True, TXT, 0)
    ctext(d, 550, 474, "Pick certifications that match the tools and roles you actually want.", 13, False, MUTED, 0)
    save_png(im, "career-map.png")


# ------------------------------------------------------------------ GIFs
def cert_in_clock():
    W, H = 960, 440
    ms = [(0, "Noticed", "L1 writes down\nthe exact time", 1),
          (1, "Triage + escalate", "Quick checks, flag\npersonal data", -1),
          (3, "Scope confirmed", "L2 / IR confirm\nwhat happened", 1),
          (5, "Compliance decides", "Reportable?\nPrepare report", -1),
          (6, "Report to CERT-In", "Deadline: 6 hours", 1)]
    x0, x1, y = 130, 830, 230
    frames, durs = [], []
    steps = 54
    for i in range(steps + 1):
        t = 6 * i / steps
        im, d = canvas(W, H)
        header(d, W, "The CERT-In 6-hour clock", "From the moment you NOTICE an incident")
        d.rounded_rectangle((x0, y - 11, x1, y + 11), 11, fill=GRAY)
        px = x0 + (x1 - x0) * t / 6
        col = TEAL if t < 5 else (AMBER if t < 6 else RED)
        if px > x0:
            d.rounded_rectangle((x0, y - 11, px, y + 11), 11, fill=col)
        for h, title, sub, side in ms:
            mx = x0 + (x1 - x0) * h / 6
            hit = t >= h - 1e-6
            d.ellipse((mx - 13, y - 13, mx + 13, y + 13), fill=(col if hit else CARD), outline=NAVY, width=3)
            d.text((mx, y + (30 if side > 0 else -48)), f"T+{h}h", font=font(13, True), fill=MUTED, anchor="ma")
            by = y + (62 if side > 0 else -150)
            box(d, (mx - 95, by, mx + 95, by + 70), CARD if not hit else "#E8F6F3", col if hit else GRAY, 10, 2)
            ctext(d, mx, by + 20, title, 14, True, NAVY, 2)
            ctext(d, mx, by + 48, sub, 12, False, MUTED, 1)
        hh, mm = int(t), int((t % 1) * 60)
        d.text((W - 28, 22), f"T + {hh}h {mm:02d}m", font=font(26, True), fill="white", anchor="ra")
        frames.append(im)
        durs.append(90)
    for _ in range(2):
        frames.append(frames[-1]); durs.append(900)
    save_gif(frames, durs, "cert-in-6-hour-clock.gif")


def alert_lifecycle():
    W, H = 960, 470
    nodes = [("1  Alert\narrives", 130, 150), ("2  Triage\nbasic checks", 345, 150), ("3  Advanced\nchecks", 560, 150),
             ("4  Real or\nfalse positive?", 790, 150), ("5  Contain\nisolate / block", 790, 340),
             ("6  Notify +\nescalate", 560, 340), ("7  Investigate\n+ mitigate", 345, 340), ("8  Learn +\nimprove", 130, 340)]
    notes = ["Read the rule, severity, user and host", "Who? Which machine? When? Known-bad indicator?",
             "Logs before and after, process, ports, threat intel", "False positive: close with a clear reason. Real: raise it",
             "Isolate the host through EDR, block the bad IP", "Tell the right people. Note exact times",
             "Correlate in the SIEM, find the cause, hunt for more", "Document, update playbooks and detections"]
    frames, durs = [], []
    seq = list(range(8))
    for active in seq + [8]:
        for sub in range(3):
            im, d = canvas(W, H)
            header(d, W, "Life of an alert", "From first beep to lessons learned")
            # arrows
            order = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
            for a, b in order:
                ax, ay = nodes[a][1], nodes[a][2]; bx, by = nodes[b][1], nodes[b][2]
                done = active > a
                c = TEAL if done else GRAY
                if ay == by:
                    s = 1 if bx > ax else -1
                    d.line((ax + s * 85, ay, bx - s * 85, by), fill=c, width=5)
                    d.polygon([(bx - s * 85, by), (bx - s * 100, by - 9), (bx - s * 100, by + 9)], fill=c)
                else:
                    d.line((ax, ay + 40, bx, by - 40), fill=c, width=5)
                    d.polygon([(bx, by - 40), (bx - 9, by - 56), (bx + 9, by - 56)], fill=c)
            # shortcut: false positive branch
            d.text((790, 98), "False positive? yes → close ticket", font=font(13, True), fill=AMBER, anchor="ma")
            for k, (label, cx, cy) in enumerate(nodes):
                on = (k == active)
                done = k < active
                fill = TEAL if on else ("#E8F6F3" if done else CARD)
                pulse = 3 + (1 if sub == 1 else 0) if on else 2
                box(d, (cx - 85, cy - 40, cx + 85, cy + 40), fill, TEAL if (on or done) else GRAY, 14, pulse)
                ctext(d, cx, cy, label, 15, True, "white" if on else NAVY, 2)
            if active < 8:
                box(d, (60, 410, 900, 450), "#FFF8E1", AMBER, 10, 2)
                ctext(d, 480, 430, notes[active], 15, False, TXT)
            else:
                box(d, (60, 410, 900, 450), "#E8F6F3", GREEN, 10, 2)
                ctext(d, 480, 430, "Every alert follows this loop. Write clear notes at every step.", 15, True, GREEN)
            frames.append(im); durs.append(380 if active < 8 else 1500)
    save_gif(frames, durs, "alert-lifecycle.gif")


def kill_chain():
    W, H = 960, 470
    stages = [("Recon", "Attacker researches and scans", "Port scans, probing"),
              ("Weaponize", "Builds the malicious payload", "Usually invisible to you"),
              ("Delivery", "Sends phishing email / link", "Email alerts, odd attachments"),
              ("Exploit", "Triggers a weakness", "EDR exploit alerts"),
              ("Install", "Plants persistence", "New services, scheduled tasks"),
              ("C2", "Malware phones home", "Beacons, odd DNS"),
              ("Actions", "Steals / encrypts / destroys", "Mass file changes, big uploads")]
    n = len(stages)
    cw = 124
    frames, durs = [], []
    for active in range(n + 1):
        for sub in range(2):
            im, d = canvas(W, H)
            header(d, W, "The Cyber Kill Chain", "Seven steps of an attack, and where you can stop it")
            for k, (nm, what, see) in enumerate(stages):
                x = 36 + k * (cw + 6)
                y = 120
                col = GREEN if k >= 2 and k <= 3 else TEAL
                if active < n:
                    fill = col if k <= active else GRAY
                else:
                    fill = GREEN if k < 4 else GRAY
                pts = [(x, y), (x + cw - 22, y), (x + cw, y + 34), (x + cw - 22, y + 68), (x, y + 68), (x + 22, y + 34)]
                d.polygon(pts, fill=fill)
                ctext(d, x + cw / 2, y + 34, f"{k+1}\n{nm}", 14, True, "white", 0)
            if active < n:
                nm, what, see = stages[active]
                box(d, (60, 250, 900, 400), CARD, TEAL, 14, 3)
                d.text((90, 268), f"Stage {active+1}: {nm}", font=font(24, True), fill=NAVY)
                d.text((90, 312), "What the attacker does:  " + what, font=font(17), fill=TXT)
                d.text((90, 346), "What you might see:        " + see, font=font(17, True), fill=TEAL)
            else:
                box(d, (60, 250, 900, 400), "#E8F6F3", GREEN, 14, 3)
                ctext(d, 480, 285, "The earlier you catch it, the cheaper it is.", 24, True, GREEN)
                ctext(d, 480, 335, "Catch it at Delivery or Exploitation (stages 3 and 4)\nand there is far less damage than at Actions on Objectives.", 16, False, TXT, 6)
            frames.append(im); durs.append(700 if active < n else 2000)
    save_gif(frames, durs, "kill-chain.gif")


def tutor_gate():
    W, H = 960, 500
    tiles = ["Networking", "Linux", "Fundamentals", "Attacks", "Workflow"]
    # scenes: (unlocked_count, step, left_text, right_text, banner, banner_col)
    scenes = [
        (1, 0, "", "", "TEACH: you read the section (visuals, examples, notes)", TEAL),
        (1, 1, "AI tutor:  Which port does RDP use by default?", "", "CHECK: the AI asks first, before you move on", BLUE),
        (1, 1, "AI tutor:  Which port does RDP use by default?", "You:  3389", "CHECK: you answer in your own words or by choice", BLUE),
        (1, 2, "", "", "GATE: score 100%  ≥ pass mark 80%   →   PASSED", GREEN),
        (2, 3, "", "", "NEXT: section 2 unlocks. Progress card updated", GREEN),
        (2, 1, "AI tutor:  Which log records SSH logins on Ubuntu?", "You:  /var/log/syslog", "CHECK: a wrong answer is not a disaster", BLUE),
        (2, 2, "", "", "GATE: score 50%  <  80%   →   NOT YET. Section 3 stays locked", RED),
        (2, 0, "", "", "RE-LEARN: review the weak objectives, then retry", AMBER),
        (2, 1, "AI tutor:  Let's try again. Where are SSH logins recorded on Debian?", "You:  /var/log/auth.log", "CHECK: second attempt, fresh question", BLUE),
        (3, 3, "", "", "GATE passed → section 3 unlocks. Learning is the point, not the score", GREEN),
    ]
    frames, durs = [], []
    steps = ["Teach", "Check", "Gate", "Next"]
    for unlocked, step, left, right, banner, bcol in scenes:
        im, d = canvas(W, H)
        header(d, W, "The AI Tutor Gate", "Teach → Check → Gate → Next. No skipping.")
        # tiles
        for k, t in enumerate(tiles):
            x = 40 + k * 178
            op = k < unlocked
            box(d, (x, 100, x + 164, 170), "#E8F6F3" if op else "#ECEFF4", GREEN if op else "#9AA6B8", 12, 3)
            ctext(d, x + 82, 126, f"{k+1}. {t}", 14, True, NAVY if op else "#8A95A8", 0)
            ctext(d, x + 82, 150, "OPEN" if op else "LOCKED", 13, True, GREEN if op else "#8A95A8", 0)
        # flow
        for k, s in enumerate(steps):
            x = 90 + k * 210
            on = (k == step)
            d.ellipse((x, 220, x + 56, 276), fill=(bcol if on else GRAY))
            ctext(d, x + 28, 238, str(k + 1), 20, True, "white", 0)
            d.text((x + 28, 284), s, font=font(16, True), fill=NAVY, anchor="ma")
            if k < 3:
                d.line((x + 62, 248, x + 200, 248), fill=GRAY, width=4)
        # chat
        if left:
            box(d, (60, 330, 600, 372), "#FFFFFF", BLUE, 12, 2)
            d.text((76, 340), left, font=font(15), fill=TXT)
        if right:
            box(d, (360, 380, 900, 422), "#FFFFFF", GREEN if "3389" in right or "auth.log" in right else RED, 12, 2)
            d.text((376, 390), right, font=font(15), fill=TXT)
        box(d, (40, 440, 920, 484), "#FFFFFF", bcol, 12, 3)
        ctext(d, 480, 462, banner, 16, True, bcol, 0)
        frames.append(im); durs.append(1800)
    save_gif(frames, durs, "tutor-gate.gif")


def sample_progress_card():
    import progress_lib as P
    from progress_card import render_card
    cur = P.load(P.CURRICULUM)
    prog = P.new_progress("Sample Learner", "SOC Analyst (L1)")
    for sec, c, t, passed in [("s00-start-here", 3, 4, False), ("s00-start-here", 4, 4, True),
                              ("s01-networking", 4, 4, True), ("s02-linux", 3, 3, True),
                              ("s12-windows-and-active-directory", 3, 4, False)]:
        P.append_entry(prog, sec, c, t, passed, source="sample")
    render_card(prog, cur, os.path.join(OUT, "progress-card-sample.png"))
    print("wrote progress-card-sample.png")


if __name__ == "__main__":
    regulation_map(); reporting_clocks(); regulation_timeline(); siem_pipeline(); ir_lifecycle(); career_map()
    cert_in_clock(); alert_lifecycle(); kill_chain(); tutor_gate(); sample_progress_card()
