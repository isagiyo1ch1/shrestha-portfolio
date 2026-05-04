import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
import math, random

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 2480, 3508   # A4 at 300 dpi
img  = Image.new("RGB", (W, H), "#F2D0CC")
draw = ImageDraw.Draw(img)

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#F2D0CC"   # blush rose
DEEP     = "#5C1F2E"   # deep burgundy
MID      = "#A05068"   # muted mauve
LIGHT    = "#F9EAE8"   # near-cream
ACCENT   = "#8B3A50"   # rose-wine

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_DIR = r"C:\Users\ashua\.claude\skills\canvas-design\canvas-fonts"
def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}\\{name}", size)

f_italiana   = font("Italiana-Regular.ttf",    52)
f_italiana_s = font("Italiana-Regular.ttf",    28)
f_jura       = font("Jura-Light.ttf",          22)
f_jura_xs    = font("Jura-Light.ttf",          17)
f_crimson_i  = font("CrimsonPro-Italic.ttf",   34)
f_gloock     = font("Gloock-Regular.ttf",      96)

# ── Helpers ───────────────────────────────────────────────────────────────────
def line(x0, y0, x1, y1, color=DEEP, w=1):
    draw.line([(x0, y0), (x1, y1)], fill=color, width=w)

def circle(cx, cy, r, outline=DEEP, width=1, fill=None):
    draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], outline=outline, width=width, fill=fill)

def text_centered(txt, cx, cy, fnt, color=DEEP):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((cx - tw//2, cy - th//2), txt, font=fnt, fill=color)

# ── 1. Subtle grain overlay ───────────────────────────────────────────────────
random.seed(42)
grain = Image.new("RGB", (W, H), "#F2D0CC")
gd    = ImageDraw.Draw(grain)
for _ in range(60000):
    x, y = random.randint(0, W-1), random.randint(0, H-1)
    v    = random.randint(0, 12)
    gd.point((x, y), fill=(min(242+v,255), min(208+v,255), min(204+v,255)))
img = Image.blend(img, grain, alpha=0.35)
draw = ImageDraw.Draw(img)

# ── 2. Large background circle (moon) ─────────────────────────────────────────
CX, CY, R = W//2, int(H*0.40), int(W*0.34)
circle(CX, CY, R, outline=MID, width=3, fill=None)
circle(CX, CY, R+18, outline=DEEP, width=1)
circle(CX, CY, R-22, outline=MID, width=1)

# ── 3. Radial petal / embroidery system ──────────────────────────────────────
# Chikankari-inspired: radiating fine lines with leaf nodes
N_PETALS = 36
for i in range(N_PETALS):
    angle = 2 * math.pi * i / N_PETALS
    # main stem
    r_inner = R * 0.18
    r_outer = R * 0.88
    x0 = CX + r_inner * math.cos(angle)
    y0 = CY + r_inner * math.sin(angle)
    x1 = CX + r_outer * math.cos(angle)
    y1 = CY + r_outer * math.sin(angle)
    line(x0, y0, x1, y1, color=DEEP, w=1)

    # leaf pairs along each stem (every other petal)
    if i % 2 == 0:
        for t in [0.35, 0.58, 0.76]:
            lx = CX + (r_inner + t*(r_outer-r_inner)) * math.cos(angle)
            ly = CY + (r_inner + t*(r_outer-r_inner)) * math.sin(angle)
            leaf_len = 38
            perp = angle + math.pi/2
            lx2 = lx + leaf_len * math.cos(perp)
            ly2 = ly + leaf_len * math.sin(perp)
            lx3 = lx - leaf_len * math.cos(perp)
            ly3 = ly - leaf_len * math.sin(perp)
            line(lx, ly, lx2, ly2, color=MID, w=1)
            line(lx, ly, lx3, ly3, color=MID, w=1)
            circle(int(lx2), int(ly2), 3, outline=MID, width=1)
            circle(int(lx3), int(ly3), 3, outline=MID, width=1)

# ── 4. Inner botanical rings ──────────────────────────────────────────────────
for r_frac in [0.12, 0.24, 0.48, 0.64]:
    rr = int(R * r_frac)
    circle(CX, CY, rr, outline=DEEP, width=1)
    # dot markers on each ring
    for k in range(12):
        a = 2 * math.pi * k / 12
        px = CX + rr * math.cos(a)
        py = CY + rr * math.sin(a)
        circle(int(px), int(py), 4, outline=DEEP, width=1)

# ── 5. Fine cross-hair grid inside inner circle ──────────────────────────────
inner_r = int(R * 0.12)
step = 18
for dx in range(-inner_r, inner_r+1, step):
    y_max = int(math.sqrt(max(0, inner_r**2 - dx**2)))
    line(CX+dx, CY-y_max, CX+dx, CY+y_max, color=MID, w=1)
for dy in range(-inner_r, inner_r+1, step):
    x_max = int(math.sqrt(max(0, inner_r**2 - dy**2)))
    line(CX-x_max, CY+dy, CX+x_max, CY+dy, color=MID, w=1)

# ── 5b. Outer halo of fine dashes ────────────────────────────────────────────
N_DASHES = 72
for i in range(N_DASHES):
    a = 2 * math.pi * i / N_DASHES
    r1 = R + 38
    r2 = R + 38 + (14 if i % 3 == 0 else 7)
    x0 = CX + r1 * math.cos(a)
    y0 = CY + r1 * math.sin(a)
    x1 = CX + r2 * math.cos(a)
    y1 = CY + r2 * math.sin(a)
    line(int(x0), int(y0), int(x1), int(y1), color=DEEP, w=1)

# ── 6. Scattered field dots (outside main circle) ─────────────────────────────
random.seed(7)
MARGIN = 160
for _ in range(320):
    x = random.randint(MARGIN, W-MARGIN)
    y = random.randint(MARGIN, H-MARGIN)
    dist = math.sqrt((x-CX)**2 + (y-CY)**2)
    if dist > R + 60:
        r_dot = random.choice([2, 2, 2, 3, 4])
        col   = random.choice([DEEP, MID, MID])
        circle(x, y, r_dot, outline=col, width=1)

# ── 7. Corner botanical sprigs ────────────────────────────────────────────────
def sprig(sx, sy, angle_base, n=5):
    for j in range(n):
        a = angle_base + math.radians(j * 14 - (n//2)*14)
        length = 55 + j*8
        ex = sx + length * math.cos(a)
        ey = sy + length * math.sin(a)
        line(sx, sy, int(ex), int(ey), color=DEEP, w=1)
        # tip leaf
        perp = a + math.pi/2
        circle(int(ex), int(ey), 5, outline=MID, width=1)

sprig(MARGIN+40, MARGIN+40, math.radians(45))
sprig(W-MARGIN-40, MARGIN+40, math.radians(135))
sprig(MARGIN+40, H-MARGIN-40, math.radians(-45))
sprig(W-MARGIN-40, H-MARGIN-40, math.radians(-135))

# ── 8. Outer border rules ─────────────────────────────────────────────────────
PAD = 90
# outer rect
draw.rectangle([PAD, PAD, W-PAD, H-PAD], outline=DEEP, width=2)
# inner rule
draw.rectangle([PAD+14, PAD+14, W-PAD-14, H-PAD-14], outline=MID, width=1)

# ── 9. Horizontal rule bands ─────────────────────────────────────────────────
# top text area band
BAND_TOP = int(H * 0.075)
line(PAD+14, BAND_TOP, W-PAD-14, BAND_TOP, color=DEEP, w=1)
# bottom text band
BAND_BOT = int(H * 0.900)
line(PAD+14, BAND_BOT, W-PAD-14, BAND_BOT, color=DEEP, w=1)

# ── 10. Typography ────────────────────────────────────────────────────────────
# Eyebrow label — top left
draw.text((PAD+32, PAD+32), "PORTFOLIO  ·  2025", font=f_jura_xs, fill=DEEP)

# Top right — coordinate
draw.text((W-PAD-200, PAD+32), "23°N  88°E", font=f_jura_xs, fill=MID)

# Main name — large, centered, below center circle
NAME_Y = int(H * 0.745)
text_centered("SHRESTHA  ROY", CX, NAME_Y, f_gloock, color=DEEP)

# Discipline — italic, centered, below name
text_centered("fashion design", CX, NAME_Y + 76, f_crimson_i, color=ACCENT)

# Thin rule below name
line(CX - 260, NAME_Y + 108, CX + 260, NAME_Y + 108, color=MID, w=1)

# Tagline row
text_centered("SISTER NIVEDITA UNIVERSITY  ·  KOLKATA", CX, NAME_Y + 138, f_jura_xs, color=MID)

# Bottom caption
CAP_Y = int(H * 0.930)
text_centered("R O S E   C A R T O G R A P H Y", CX, CAP_Y, f_italiana_s, color=DEEP)

# Bottom corners
draw.text((PAD+32, H-PAD-46), "SR", font=f_jura, fill=MID)
draw.text((W-PAD-72, H-PAD-46), "I", font=f_jura, fill=MID)

# ── 11. Central monogram (over crosshair, very faint) ─────────────────────────
mono_img = Image.new("RGBA", (W, H), (0,0,0,0))
mono_draw = ImageDraw.Draw(mono_img)
bb = mono_draw.textbbox((0,0), "SR", font=font("Italiana-Regular.ttf", 64))
tw, th = bb[2]-bb[0], bb[3]-bb[1]
mono_draw.text((CX - tw//2, CY - th//2), "SR", font=font("Italiana-Regular.ttf", 64),
               fill=(92, 31, 46, 55))
img = Image.alpha_composite(img.convert("RGBA"), mono_img).convert("RGB")
draw = ImageDraw.Draw(img)

# ── 12. Thin vertical rules flanking name ─────────────────────────────────────
line(CX-320, NAME_Y-18, CX-320, NAME_Y+118, color=MID, w=1)
line(CX+320, NAME_Y-18, CX+320, NAME_Y+118, color=MID, w=1)

# ── Save ──────────────────────────────────────────────────────────────────────
out = r"c:\Users\ashua\shrestha\FashionDesigner-Portfolio\canvas\shrestha_roy_poster.png"
img.save(out, dpi=(300, 300))
print("Saved:", out)
