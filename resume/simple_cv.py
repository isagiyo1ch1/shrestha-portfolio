"""
Shrestha Roy — Simple CV (plain black & white, Arial-style).
Mirrors the layout of Resume_Shrestha_Roy-1.pdf; content matches the portfolio.
Usage: python3 simple_cv.py <qr_png> <out_pdf>
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

F = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Arial", F + "LiberationSans-Regular.ttf"))     # metric-compatible with Arial
pdfmetrics.registerFont(TTFont("Arial-Bold", F + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

QR, OUT = sys.argv[1], sys.argv[2]
W, H = A4
LEFT, HEAD_X, RIGHT = 47.8, 35.5, 547.0
TEXT_W = RIGHT - LEFT

body = ParagraphStyle("b", fontName="Arial", fontSize=9, leading=11.7)
ach  = ParagraphStyle("a", parent=body, leftIndent=5.7, firstLineIndent=-5.7)

c = Canvas(OUT, pagesize=A4)
c.setTitle("Shrestha Roy — Résumé"); c.setAuthor("Shrestha Roy")

# ── Header
c.setFont("Arial-Bold", 20); c.drawString(HEAD_X, H - 93, "Shrestha Roy")
c.setFont("Arial", 9)
c.drawString(HEAD_X, H - 105.5, "shrestharoy.work@gmail.com   |   +91 6289278968   |   Kolkata, India")
link_y = H - 117.5
txt = "Behance: https://www.behance.net/shrestha_roy   |   Portfolio: shrestha-roy.netlify.app"
c.drawString(HEAD_X, link_y, txt)
bx = HEAD_X + c.stringWidth("Behance: ", "Arial", 9)
c.linkURL("https://www.behance.net/shrestha_roy",
          (bx, link_y - 2, bx + c.stringWidth("https://www.behance.net/shrestha_roy", "Arial", 9), link_y + 8), relative=0)
px = HEAD_X + c.stringWidth(txt.split("shrestha-roy")[0], "Arial", 9)
c.linkURL("https://shrestha-roy.netlify.app",
          (px, link_y - 2, px + c.stringWidth("shrestha-roy.netlify.app", "Arial", 9), link_y + 8), relative=0)
c.drawImage(QR, 495.9, H - 121.2, 48, 48)

y = H - 131   # running cursor (top of next block)

def section(title):
    global y
    y -= 19
    c.setFont("Arial-Bold", 10); c.drawString(LEFT, y, title)
    y -= 5

def para(markup, style=body, gap=0):
    global y
    p = Paragraph(markup, style)
    _, h = p.wrap(TEXT_W, 1000)
    p.drawOn(c, LEFT, y - h); y -= h + gap

B = lambda s: f"<b>{s}</b>"
BUL = "•&nbsp;&nbsp;&nbsp;&nbsp;"

section("OVERVIEW")
para("Fashion designer with a strong foundation in garment construction, textile research, and creative direction. "
     "Currently working as a Junior Designer at Kiran Uttam Ghosh, bringing experience across design, illustration, "
     "styling, product development, and B2B management. Detail-oriented, collaborative, and driven by craft.")

section("EDUCATION")
para(B("Sister Nivedita University, Kolkata") + " (2022–2026) — Bachelor of Design in Fashion Design, CGPA: 8.91")
para(B("Modern High School for Girls, Kolkata") + " (2020–2022) — ISC: 93%")
para(B("Loreto Day School, Dharamtala, Kolkata") + " (2009–2020) — ICSE: 90.6%")

section("SKILLS")
for head, items in [
    ("Fashion Design &amp; Construction", "Pattern Making, Draping, Garment Construction, Sewing and Finishing Techniques, Hand Embroidery"),
    ("Illustration &amp; Visualization", "Digital Illustration, Technical Flats, Adobe Photoshop, Illustrator, InDesign, CLO3D, CorelDraw"),
    ("Textile &amp; Research", "Fabric Sourcing, Print Development, Natural Dyeing, Trend Forecasting, Market Analysis"),
    ("Fashion &amp; Creative Direction", "Fashion Design, Fashion Illustration, Creative Direction, Product Development and Management, Fashion Styling"),
    ("Business &amp; Management", "Fashion Merchandising, Inventory Management, B2B Sales Management, Quality Management, Graphic Design"),
]:
    para(B(head + ":") + " " + items)

section("PROFESSIONAL EXPERIENCE")
for head, text in [
    ("Junior Designer, Kiran Uttam Ghosh (2026–Present):",
     "Fashion design and illustration for seasonal collections; creative direction, product development and quality "
     "management; fashion merchandising, inventory and B2B sales management; fashion styling and graphic design."),
    ("Graduation Collection — What Remains, Sister Nivedita University (Jan–May 2026):",
     "Developed a 6-look S/S '26 avant-garde womenswear collection exploring survival, trauma and resilience; created "
     "full spec sheets, pattern drafts, toiles and documentation."),
    ("Assistant Designer &amp; Backstage Stylist, Rohan Pariyar Studios (Nov 2025):",
     "Styling and coordination for the I-Medici collection at Victoria Memorial Hall in collaboration with the "
     "Consulate General of Italy."),
    ("Fashion Design Intern, Abhishek Dutta India (Jun–Aug 2025):",
     "Styled celebrities, assisted editorial shoots, contributed to podcast pre-production, and designed a complete "
     "NIPS Hospitality uniform range."),
    ("Assistant Designer, Roy Calcutta (Mar 2025):",
     "Assisted with backstage coordination and styling for the Nawabs of Bengal collection at Calcutta Times Fashion Week."),
    ("Assistant Designer &amp; Stylist, Sister Nivedita University Fashion Show 2025 (Dec 2024–Jan 2025):",
     "Conceptualized a 28-look collection inspired by Bengal's textile heritage; managed garment construction, "
     "fittings, backstage logistics and live runway hosting."),
    ("Store Associate, Sutra Handloom (Aug 2024):",
     "Provided styling advice, product selection, fitting assistance and visual merchandising support."),
]:
    para(BUL + B(head) + " " + text)

section("ACHIEVEMENTS &amp; CERTIFICATES".replace("&amp;", "&"))
for line in [
    B("Assistant Designer Certificate") + " — Rohan Pariyar Studios (2025).",
    B("Internship Certificate") + " — Abhishek Dutta India (2025).",
    B("Certificate of Merit") + " — Designer of the Year, Sister Nivedita University (2024–2025).",
    B("Assistant Designer Certificate") + " — Roy Calcutta (2025).",
    B("Certificate of Merit") + " for representing Sister Nivedita University at the 38th AIU Inter-University East Zonal Youth Festival (2024–2025).",
    B("Volunteer Certificate") + " — Sutra Handloom Studies (2024).",
]:
    para("• " + line, ach)

assert y > 36, f"overflowed page (y={y:.1f})"
c.save()
print(f"saved {OUT}  (bottom cursor y={y:.1f}pt)")
