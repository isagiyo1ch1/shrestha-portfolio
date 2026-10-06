"""
Shrestha Roy — Rose Cartography CV
Pixel-matched to original ShresthaRoy_CV_Circle-10.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math, os

F = "/home/claude/canvas-fonts/"
pdfmetrics.registerFont(TTFont("Crimson",  F+"CrimsonPro-Regular.ttf"))
pdfmetrics.registerFont(TTFont("CrimsonB", F+"CrimsonPro-Bold.ttf"))
pdfmetrics.registerFont(TTFont("CrimsonI", F+"CrimsonPro-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Work",     F+"WorkSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("WorkB",    F+"WorkSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Poiret",   F+"PoiretOne-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Mono",     F+"DMMono-Regular.ttf"))

BG   = (0.961, 0.898, 0.882)
DEEP = (0.38,  0.08,  0.15)
MID  = (0.56,  0.22,  0.30)
PALE = (0.82,  0.65,  0.65)

W, H = A4        # 595.28 × 841.89 pt
m    = 14 * mm   # page margin

def sf(c, rgb): c.setFillColorRGB(*rgb)
def ss(c, rgb): c.setStrokeColorRGB(*rgb)

def wrap_text(c, text, font, size, max_w):
    c.setFont(font, size)
    words = text.split()
    lines, line = [], ""
    for w in words:
        t = (line + " " + w).strip()
        if c.stringWidth(t, font, size) <= max_w:
            line = t
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

# ── Background decoration ─────────────────────────────────────────────────────
def draw_bg(c):
    sf(c, BG); c.rect(0, 0, W, H, fill=1, stroke=0)

    # Scattered + crosshairs (arm=4pt)
    ss(c, PALE); c.setLineWidth(0.3)
    cross_pos = [
        (0.12, 0.92), (0.45, 0.88), (0.75, 0.83),
        (0.22, 0.71), (0.60, 0.68), (0.88, 0.63),
        (0.30, 0.52), (0.68, 0.47), (0.15, 0.38),
        (0.52, 0.34), (0.82, 0.30), (0.25, 0.22),
        (0.65, 0.19), (0.42, 0.10), (0.88, 0.12),
    ]
    arm = 4
    for px, py in cross_pos:
        x, y = px * W, py * H
        c.line(x - arm, y, x + arm, y)
        c.line(x, y - arm, x, y + arm)

    # Scattered dots
    sf(c, PALE)
    dot_pos = [(0.35,0.82),(0.58,0.76),(0.18,0.60),(0.48,0.55),
               (0.78,0.50),(0.38,0.42),(0.72,0.38),(0.55,0.26),(0.20,0.15)]
    for px, py in dot_pos:
        c.circle(px*W, py*H, 1.5, fill=1, stroke=0)

# ── Section header: single rule ABOVE, then Poiret label below ───────────────
def section_header(c, label, x, y, col_w):
    ss(c, PALE); c.setLineWidth(0.5)
    c.line(x, y, x + col_w, y)
    y -= 12
    sf(c, DEEP); c.setFont("Poiret", 10.5)
    c.drawString(x, y, label.upper())
    return y - 7

# ── Bullet line ───────────────────────────────────────────────────────────────
def bullet_line(c, text, x, y, col_w, size=7.2, lead=10):
    sf(c, DEEP)
    dash = "– "
    dw = c.stringWidth(dash, "Work", size)
    c.setFont("Work", size); c.drawString(x, y, dash)
    lines = wrap_text(c, text, "Work", size, col_w - dw)
    for i, ln in enumerate(lines):
        c.setFont("Work", size); c.drawString(x + dw, y - i * lead, ln)
    return y - len(lines) * lead

# ── Experience entry ──────────────────────────────────────────────────────────
def exp_entry(c, title, org, dates, bullets, x, y, col_w, gap=7):
    y -= gap
    # Title (WorkB bold) + date right-aligned (Mono)
    sf(c, DEEP); c.setFont("WorkB", 8.8)
    c.drawString(x, y, title)
    sf(c, PALE); c.setFont("Mono", 7)
    c.drawRightString(x + col_w, y, dates)
    # Org italic
    y -= 10
    sf(c, MID); c.setFont("CrimsonI", 8)
    c.drawString(x, y, org)
    y -= 10
    for b in bullets:
        y = bullet_line(c, b, x, y, col_w)
        y -= 1
    return y

# ── Achievement entry (same structure) ───────────────────────────────────────
def achiev_entry(c, title, org, dates, bullets, x, y, col_w, gap=8):
    y -= gap
    sf(c, DEEP); c.setFont("WorkB", 9)
    c.drawString(x, y, title)
    if dates:
        sf(c, PALE); c.setFont("Mono", 7)
        c.drawRightString(x + col_w, y, dates)
    y -= 11
    sf(c, MID); c.setFont("CrimsonI", 8.5)
    c.drawString(x, y, org)
    y -= 11
    for b in bullets:
        y = bullet_line(c, b, x, y, col_w)
        y -= 1
    return y

# ── Skill group ───────────────────────────────────────────────────────────────
def skill_group(c, label, items, x, y, col_w, gap=6):
    y -= gap
    sf(c, DEEP); c.setFont("WorkB", 7.5)
    c.drawString(x, y, label)
    y -= 10
    text = "  ·  ".join(items)
    for ln in wrap_text(c, text, "Work", 7.5, col_w):
        sf(c, DEEP); c.setFont("Work", 7.5)
        c.drawString(x, y, ln); y -= 10
    return y

# ── Rose compass ──────────────────────────────────────────────────────────────
def draw_rose(c, cx, cy, r=28):
    # Dotted concentric circles
    for ri in [r * 0.35, r * 0.65, r]:
        steps = 72
        for i in range(steps):
            if i % 4 != 0: continue
            a = 2 * math.pi * i / steps
            px = cx + ri * math.cos(a)
            py = cy + ri * math.sin(a)
            sf(c, PALE); c.circle(px, py, 0.5, fill=1, stroke=0)

    # Cardinal lines — explicit coords (N=up, S=down, E=right, W=left)
    ss(c, MID); c.setLineWidth(0.6)
    c.line(cx, cy, cx,     cy + r)   # N
    c.line(cx, cy, cx,     cy - r)   # S
    c.line(cx, cy, cx + r, cy)       # E
    c.line(cx, cy, cx - r, cy)       # W

    # Intercardinal (shorter, pale)
    ss(c, PALE); c.setLineWidth(0.3)
    diag = r * 0.55 * 0.7071  # r*sin(45)
    c.line(cx, cy, cx + diag, cy + diag)   # NE
    c.line(cx, cy, cx - diag, cy + diag)   # NW
    c.line(cx, cy, cx + diag, cy - diag)   # SE
    c.line(cx, cy, cx - diag, cy - diag)   # SW

    # N diamond (dark, pointing up)
    mid_y = cy + r * 0.32
    p = c.beginPath()
    p.moveTo(cx,     cy + r)    # tip N
    p.lineTo(cx - 5, mid_y)
    p.lineTo(cx,     cy)        # center
    p.lineTo(cx + 5, mid_y)
    p.close()
    sf(c, DEEP); c.drawPath(p, fill=1, stroke=0)

    # S diamond (pale)
    mid_s = cy - r * 0.32
    p2 = c.beginPath()
    p2.moveTo(cx,     cy - r)   # tip S
    p2.lineTo(cx - 4, mid_s)
    p2.lineTo(cx,     cy)
    p2.lineTo(cx + 4, mid_s)
    p2.close()
    sf(c, PALE); ss(c, MID); c.setLineWidth(0.4)
    c.drawPath(p2, fill=1, stroke=1)

    # E diamond
    mid_e = cx + r * 0.32
    p3 = c.beginPath()
    p3.moveTo(cx + r, cy)    # tip E
    p3.lineTo(mid_e,  cy + 4)
    p3.lineTo(cx,     cy)
    p3.lineTo(mid_e,  cy - 4)
    p3.close()
    sf(c, PALE); c.drawPath(p3, fill=1, stroke=0)

    # W diamond
    mid_w = cx - r * 0.32
    p4 = c.beginPath()
    p4.moveTo(cx - r, cy)
    p4.lineTo(mid_w,  cy + 4)
    p4.lineTo(cx,     cy)
    p4.lineTo(mid_w,  cy - 4)
    p4.close()
    sf(c, PALE); c.drawPath(p4, fill=1, stroke=0)

    # Extension ticks on E/W
    ss(c, MID); c.setLineWidth(0.5)
    c.line(cx + r, cy, cx + r + 6, cy)
    c.line(cx - r, cy, cx - r - 6, cy)

    # Center circle
    sf(c, BG); ss(c, MID); c.setLineWidth(0.5)
    c.circle(cx, cy, 4, fill=1, stroke=1)
    sf(c, MID); c.setFont("Poiret", 5.5)
    c.drawCentredString(cx, cy - 2, "SR")

    # Cardinal labels — outside the compass radius
    sf(c, DEEP); c.setFont("Mono", 6.5)
    c.drawCentredString(cx, cy + r + 8,   "N")
    c.drawCentredString(cx, cy - r - 9,   "S")
    c.drawCentredString(cx + r + 13, cy - 2, "E")
    c.drawCentredString(cx - r - 13, cy - 2, "W")


# ═════════════════════════════════════════════════════════════════════════════
def draw_cv(frame_style, out_path):
    c = Canvas(out_path, pagesize=A4)

    draw_bg(c)

    # ── Page border ────────────────────────────────────────────────────────────
    ss(c, MID); c.setLineWidth(0.8)
    c.rect(m - 2, m - 2, W - 2*m + 4, H - 2*m + 4, fill=0, stroke=1)

    # ── Corner cartouches (L-shaped brackets with label) ──────────────────────
    def cartouche(cx, cy, flip_x, flip_y, label):
        c.saveState()
        c.translate(cx, cy)
        c.scale(flip_x, flip_y)
        ss(c, MID); c.setLineWidth(0.7)
        p = c.beginPath()
        p.moveTo(0, 22); p.lineTo(0, 0); p.lineTo(22, 0)
        c.drawPath(p, fill=0, stroke=1)
        if label:
            sf(c, MID); c.setFont("Mono", 5.5)
            c.drawString(3, 3, label)
        c.restoreState()

    cartouche(m - 2, m - 2,   1,  1, "SR·2026")
    cartouche(W - m + 2, m - 2, -1,  1, "KOL·IND")
    cartouche(m - 2, H - m + 2,  1, -1, "")
    cartouche(W - m + 2, H - m + 2, -1, -1, "")

    # ══════════════════════════════════════════════════════════════════════════
    # HEADER AREA
    # Name baseline sits 36pt below top margin (leaving space for ascenders)
    # ══════════════════════════════════════════════════════════════════════════
    #
    # Layout (from top of page going down):
    #   m        = top margin (14mm ≈ 39.7pt)
    #   name_y   = H - m - 38   ← baseline of 36pt name
    #   subtitle = name_y - 18
    #   rule     = name_y - 30
    #   coord    = name_y - 41
    #   columns start = H - 53mm

    name_x = m + 8
    name_y = H - m - 38      # baseline

    # Name
    sf(c, DEEP); c.setFont("WorkB", 36)
    c.drawString(name_x, name_y, "SHRESTHA ROY")

    # Subtitle
    sf(c, MID); c.setFont("CrimsonI", 10.5)
    c.drawString(name_x, name_y - 18, "FASHION DESIGN  ·  KOLKATA, INDIA")

    # Single thin rule under subtitle
    ss(c, MID); c.setLineWidth(0.5)
    c.line(name_x, name_y - 28, W - m - 8, name_y - 28)

    # Coordinate decoration
    sf(c, PALE); c.setFont("Mono", 6)
    c.drawString(name_x + 2, name_y - 40, "22°34N  88°22E")

    # ── Contacts (top right, above photo) ─────────────────────────────────────
    # Photo is in the right section, at the very top right
    photo_size = 28 * mm   # ~79pt
    photo_x = W - m - photo_size - 6
    photo_y = H - m - photo_size - 5

    cx_p = photo_x + photo_size / 2
    cy_p = photo_y + photo_size / 2

    if frame_style == "circle":
        c.saveState()
        clip = c.beginPath(); clip.circle(cx_p, cy_p, photo_size / 2)
        c.clipPath(clip, stroke=0)
        c.drawImage("/home/claude/headshot2_circle.png",
                    photo_x, photo_y, width=photo_size, height=photo_size, mask="auto")
        c.restoreState()
        ss(c, MID); c.setLineWidth(1.2)
        c.circle(cx_p, cy_p, photo_size / 2, fill=0, stroke=1)
        ss(c, PALE); c.setLineWidth(0.4)
        c.circle(cx_p, cy_p, photo_size / 2 + 4, fill=0, stroke=1)
    else:
        c.drawImage("/home/claude/headshot2.jpg",
                    photo_x, photo_y, width=photo_size, height=photo_size)
        ss(c, MID); c.setLineWidth(1.2)
        c.rect(photo_x, photo_y, photo_size, photo_size, fill=0, stroke=1)

    # Contacts: right-aligned, between page right and photo left, vertically centered in header
    contacts = [
        "shrestharoy.work@gmail.com",
        "+91 62892 78968",
        "shrestha-roy.netlify.app",
    ]
    c_right = photo_x - 10   # right edge for contacts
    c_top   = H - m - 12     # start near top
    sf(c, DEEP)
    for i, txt in enumerate(contacts):
        c.setFont("Mono", 7)
        c.drawRightString(c_right, c_top - i * 12, txt)

    # ══════════════════════════════════════════════════════════════════════════
    # TWO COLUMNS
    # Left: Profile + Experience + Skills
    # Right: Education + Achievements (photo is in right top area)
    # ══════════════════════════════════════════════════════════════════════════
    col_L    = m + 8
    col_R    = W / 2 + 4 * mm
    col_w_L  = W / 2 - m - 14   # ≈ 219pt
    col_w_R  = W / 2 - m - 18   # ≈ 215pt

    # Vertical rule between columns (from below name header to above footer)
    ss(c, MID); c.setLineWidth(0.4)
    col_divider_x = W / 2 + 1 * mm
    c.line(col_divider_x, m + 4, col_divider_x, name_y - 50)

    # Footer top boundary (leave ~2mm above footer rule)
    footer_top = m + 4    # absolute bottom of content area

    # ── LEFT COLUMN ───────────────────────────────────────────────────────────
    y_L = name_y - 52   # just below header area

    # --- PROFILE ---
    y_L = section_header(c, "Profile", col_L, y_L, col_w_L)
    profile = (
        "Motivated and detail-oriented fashion design graduate with a solid grasp of design "
        "principles, garment construction, and trend analysis. Strong creative and technical "
        "skills with a collaborative mindset — eager to contribute fresh perspectives within "
        "a forward-thinking fashion environment."
    )
    for ln in wrap_text(c, profile, "Work", 7.2, col_w_L):
        sf(c, DEEP); c.setFont("Work", 7.2)
        c.drawString(col_L, y_L, ln); y_L -= 10
    y_L -= 4

    # --- EXPERIENCE ---
    y_L = section_header(c, "Experience", col_L, y_L, col_w_L)

    y_L = exp_entry(c, "Junior Designer", "Kiran Uttam Ghosh", "2026 – Present", [
        "Fashion design & illustration for seasonal collections; creative direction and product development.",
        "Fashion merchandising, inventory & B2B sales management; styling and graphic design for brand collateral.",
    ], col_L, y_L, col_w_L, gap=6)

    y_L = exp_entry(c, "Graduation Collection — What Remains", "Sister Nivedita University", "Jan – May 2026", [
        "6-look S/S '26 avant-garde womenswear on survival & resilience. Palette: black, navy, beige, crimson.",
        "Sculptural corset, faux-leather ensemble, sheer floral mesh dress; full spec sheets & pattern drafts.",
    ], col_L, y_L, col_w_L)

    y_L = exp_entry(c, "Assistant Designer & Backstage Stylist", "Rohan Pariyar Studios", "Nov 2025", [
        "Styling for I-Medici collection — Victoria Memorial Hall × Consolate Generale of Italy.",
    ], col_L, y_L, col_w_L)

    y_L = exp_entry(c, "Fashion Design Intern", "Abhishek Dutta India", "Jun – Aug 2025", [
        "Celebrity styling for Anandabazaar Patrika, Sananda, Anandalok; Sananda editorial swimwear shoot.",
        "Style & THE CITY podcast pre-production (Darshoo OTT). Full uniform range for NIPS Hospitality.",
    ], col_L, y_L, col_w_L)

    y_L = exp_entry(c, "Assistant Designer", "Roy Calcutta — Calcutta Times Fashion Week", "March 2025", [
        "Backstage coordination & styling for Nawabs of Bengal collection.",
    ], col_L, y_L, col_w_L)

    y_L = exp_entry(c, "Assistant Designer & Stylist", "SNU Fashion Show 2025", "Dec 2024 – Jan 2025", [
        "28-look collection for 38th AIU Inter-University East Zonal Youth Festival; runway hosting.",
    ], col_L, y_L, col_w_L)

    y_L = exp_entry(c, "Store Associate", "Sutra Handloom", "Aug 2024", [
        "Styling advice, product selection, fitting & visual merchandising.",
    ], col_L, y_L, col_w_L)
    y_L -= 6

    # --- SKILLS ---
    y_L = section_header(c, "Skills", col_L, y_L, col_w_L)

    all_skills = [
        ("Design & Construction",
         ["Pattern Making", "Draping", "Garment Construction", "Sewing & Finishing", "Hand Embroidery"]),
        ("Illustration & Software",
         ["Digital Illustration", "Technical Flats", "Photoshop", "Illustrator", "InDesign", "CLO3D", "CorelDraw"]),
        ("Textile & Research",
         ["Fabric Sourcing", "Print Development", "Natural Dyeing", "Trend Forecasting", "Market Analysis"]),
        ("Fashion & Creative Direction",
         ["Fashion Design", "Fashion Illustration", "Creative Direction",
          "Product Development & Management", "Fashion Styling"]),
        ("Business & Management",
         ["Fashion Merchandising", "Inventory Management", "B2B Sales Management",
          "Quality Management", "Graphic Design"]),
    ]

    # Compact skill render — label on one line, all items inline on next, smaller font
    def skill_compact(c2, label, items, x, y, col_w, gap=5):
        y -= gap
        sf(c2, DEEP); c2.setFont("WorkB", 7)
        c2.drawString(x, y, label)
        y -= 9
        text = "  ·  ".join(items)
        for ln in wrap_text(c2, text, "Work", 7, col_w):
            sf(c2, DEEP); c2.setFont("Work", 7)
            c2.drawString(x, y, ln); y -= 9
        return y

    # Render all skill groups in left column (compact mode)
    right_skills_overflow = []
    for label, items in all_skills:
        item_text = "  ·  ".join(items)
        est_lines = max(1, len(item_text) // 38)
        est_h = 5 + 9 + est_lines * 9 + 2
        if y_L - est_h > footer_top + 2:
            y_L = skill_compact(c, label, items, col_L, y_L, col_w_L, gap=5)
        else:
            right_skills_overflow.append((label, items))

    # ── RIGHT COLUMN ──────────────────────────────────────────────────────────
    # Education starts below photo (photo bottom = photo_y)
    y_R = photo_y - 8

    # --- EDUCATION ---
    y_R = section_header(c, "Education", col_R, y_R, col_w_R)

    def edu_row(title, org, dates, detail=None):
        nonlocal y_R
        y_R -= 5
        sf(c, DEEP); c.setFont("WorkB", 8.5)
        c.drawString(col_R, y_R, title)
        sf(c, PALE); c.setFont("Mono", 7)
        c.drawRightString(col_R + col_w_R, y_R, dates)
        y_R -= 11
        sf(c, MID); c.setFont("CrimsonI", 8.5)
        c.drawString(col_R, y_R, org)
        if detail:
            sf(c, DEEP); c.setFont("WorkB", 8)
            c.drawRightString(col_R + col_w_R, y_R, detail)
        y_R -= 10

    edu_row("B.Des Fashion Design",            "Sister Nivedita University, Kolkata",  "2022 – 2026", "CGPA 8.91")
    edu_row("Indian School Certificate (ISC)", "Modern High School for Girls, Kolkata", "2020 – 2022", "93%")
    edu_row("ICSE",                            "Loreto Day School, Dharamtala, Kolkata","2009 – 2020", "90.6%")
    y_R -= 4

    # --- ACHIEVEMENTS ---
    y_R = section_header(c, "Achievements & Certificates", col_R, y_R, col_w_R)

    y_R = achiev_entry(c, "Assistant Designer Certificate", "Rohan Pariyar Studios", "November 2025", [
        "Backstage styling for I-Medici — Victoria Memorial Hall & Consulate General of Italy, Kolkata.",
    ], col_R, y_R, col_w_R, gap=5)

    y_R = achiev_entry(c, "Internship Certificate", "Abhishek Dutta India", "Jun – Aug 2025", [
        "Completing internship under the mentorship of Fashion Designer Abhishek Dutta.",
    ], col_R, y_R, col_w_R, gap=6)

    y_R = achiev_entry(c, "Certificate of Merit — Designer of the Year", "Sister Nivedita University", "2024 – 2025", [],
        col_R, y_R, col_w_R, gap=6)

    y_R = achiev_entry(c, "Assistant Designer Certificate", "Roy Calcutta", "March 2024", [
        "Spearheading Swatantra Fashion Show, Dept. of Fine Arts & Design, SNU — 38th AIU Inter-University East Zonal Youth Festival 2024–25.",
    ], col_R, y_R, col_w_R, gap=6)

    y_R = achiev_entry(c, "Certificate of Merit", "Sister Nivedita University", "", [
        "For designing, developing and styling in the AIU fest, representing SNU from the Fashion Department.",
    ], col_R, y_R, col_w_R, gap=6)

    y_R = achiev_entry(c, "Volunteer Certificate", "Sutra Handloom Studies", "2024", [
        "Design assisting and retail work at Sutra Handloom boutique.",
    ], col_R, y_R, col_w_R, gap=6)

    # Overflow skills in right column (if any)
    # right column bottom: above QR/rose
    right_bottom = m + 16*mm + 28*mm + 16  # qr_y + qr_size + margin
    if right_skills_overflow and y_R > right_bottom + 30:
        y_R -= 8
        y_R = section_header(c, "Skills (cont.)", col_R, y_R, col_w_R)
        for label, items in right_skills_overflow:
            item_text = "  ·  ".join(items)
            est_lines = max(1, len(item_text) // 35)
            est_h = 5 + 9 + est_lines * 9 + 2
            if y_R - est_h > right_bottom:
                y_R = skill_compact(c, label, items, col_R, y_R, col_w_R, gap=4)

    # ── QR code (bottom-right) ────────────────────────────────────────────────
    qr_size = 28 * mm
    qr_x    = W - m - qr_size - 6
    qr_y    = m + 16 * mm        # above footer line

    ss(c, MID); c.setLineWidth(0.8)
    c.rect(qr_x - 2, qr_y - 2, qr_size + 4, qr_size + 4, fill=0, stroke=1)
    c.drawImage("/home/claude/qr_website.png", qr_x, qr_y,
                width=qr_size, height=qr_size, mask="auto")
    sf(c, DEEP); c.setFont("Mono", 6)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "shrestha-roy.netlify.app")

    # ── Rose compass (left of QR, in bottom right area) ───────────────────────
    rose_cx = qr_x - 44
    rose_cy = qr_y + qr_size / 2
    draw_rose(c, rose_cx, rose_cy, r=24)

    # ── Footer line + text ────────────────────────────────────────────────────
    ss(c, MID); c.setLineWidth(0.4)
    c.line(m + 4, m + 9, W - m - 4, m + 9)

    sf(c, MID); c.setFont("Poiret", 7)
    c.drawCentredString(W / 2, m + 3, "ROSE CARTOGRAPHY")

    sf(c, PALE); c.setFont("Mono", 5.5)
    c.drawString(m + 8, m + 3, "Kolkata, India")
    c.drawRightString(W - m - 8, m + 3, "Sister Nivedita University  ·  Class of 2026")

    c.save()
    print(f"Saved: {out_path}")


os.makedirs("/mnt/user-data/outputs", exist_ok=True)
draw_cv("circle",    "/mnt/user-data/outputs/ShresthaRoy_CV_Circle.pdf")
draw_cv("rectangle", "/mnt/user-data/outputs/ShresthaRoy_CV_Rectangle.pdf")
print("Done.")
