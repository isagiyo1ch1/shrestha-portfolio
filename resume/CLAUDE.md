# Shrestha Roy — CV Generation System

This folder contains the scripts to generate Shrestha Roy's CV in three formats.
Read this file first before making any CV changes.

---

## Output Files

> **The portfolio's public résumé is the Corporate version** (converted to PDF, saved as `assets/pdfs/resume/ShresthaRoy_CV.pdf`). The Rose Cartography PDFs are kept as an optional alternative design and are not linked from the site.

| Format | Script | Output Path |
|--------|--------|-------------|
| Rose Cartography Circle PDF | `cv_design.py` | `/mnt/user-data/outputs/ShresthaRoy_CV_Circle.pdf` |
| Rose Cartography Rectangle PDF | `cv_design.py` | `/mnt/user-data/outputs/ShresthaRoy_CV_Rectangle.pdf` |
| Corporate DOCX (one page) | `corporate_cv.js` | `/mnt/user-data/outputs/ShresthaRoy_CV_Corporate.docx` |

---

## Running the Scripts

```bash
# Rose Cartography PDFs (Python / ReportLab)
pip install reportlab --break-system-packages
python3 resume/cv_design.py

# Corporate DOCX (Node.js / docx)
cd resume && npm install docx && node corporate_cv.js
```

**Fonts required** (must be present at `/home/claude/canvas-fonts/`):
- `CrimsonPro-Regular.ttf`, `CrimsonPro-Italic.ttf`
- `WorkSans-Regular.ttf`, `WorkSans-Bold.ttf`, `WorkSans-Italic.ttf`
- `PoiretOne-Regular.ttf`
- `DMMono-Regular.ttf`

If fonts are missing, download from Google Fonts and place at that path.

**QR code** required at `/home/claude/qr_website.png`:
- Links to `https://shrestha-roy.netlify.app`
- Style: burgundy (#611426) on blush background
- If missing, regenerate with: `pip install qrcode pillow --break-system-packages` and create a 300×300 QR

---

## Design System — Rose Cartography Palette

| Token | Hex / RGB | Usage |
|-------|-----------|-------|
| DEEP  | `#611426` / (0.38, 0.08, 0.15) | Primary headings, borders |
| MID   | `#8E3850` / (0.56, 0.22, 0.30) | Sub-headings, accents |
| PALE  | `#D1A6A6` / (0.82, 0.65, 0.65) | Light accents |
| BG    | `#F5E5E1` / (0.961, 0.898, 0.882) | Background wash |

PDF fonts: CrimsonPro (body), WorkSans (labels/headers), PoiretOne (name), DMMono (mono)
DOCX fonts: Calibri throughout

---

## CV Content (as of Oct 2026)

**Personal**
- Name: Shrestha Roy
- Title: Fashion Design · Kolkata, India
- Email: shrestharoy.work@gmail.com
- Phone: +91 62892 78968
- Website: shrestha-roy.netlify.app

**Profile**
Fashion designer with strong grounding in garment construction, textile research and creative direction. Experienced in design, illustration, styling, product development and B2B management. Collaborative and detail-oriented; eager to contribute to forward-thinking fashion environments.

**Experience (newest first)**
1. Junior Designer · Kiran Uttam Ghosh · 2026 – Present
2. Graduation Collection "What Remains" · Sister Nivedita University · Jan–May 2026
3. Assistant Designer & Backstage Stylist · Rohan Pariyar Studios · Nov 2025
4. Fashion Design Intern · Abhishek Dutta India · Jun–Aug 2025
5. Assistant Designer · Roy Calcutta — Calcutta Times Fashion Week · March 2025
6. Assistant Designer & Stylist · SNU Fashion Show 2025 · Dec 2024–Jan 2025
7. Store Associate · Sutra Handloom · Aug 2024

**Education**
- B.Des Fashion Design · Sister Nivedita University, Kolkata · 2022–2026 · CGPA 8.91
- ISC · Modern High School for Girls, Kolkata · 2020–2022 · 93%
- ICSE · Loreto Day School, Dharamtala, Kolkata · 2009–2020 · 90.6%

**Skills (5 groups)**
- Design & Construction: Pattern Making, Draping, Garment Construction, Sewing & Finishing, Hand Embroidery
- Illustration & Software: Digital Illustration, Technical Flats, Photoshop, Illustrator, InDesign, CLO3D, CorelDraw
- Textile & Research: Fabric Sourcing, Print Development, Natural Dyeing, Trend Forecasting, Market Analysis
- Fashion & Creative Direction: Fashion Design, Fashion Illustration, Creative Direction, Product Development & Management, Fashion Styling
- Business & Management: Fashion Merchandising, Inventory Management, B2B Sales Management, Quality Management, Graphic Design

**Achievements**
- Nov 2025 · Assistant Designer Certificate · Rohan Pariyar Studios (I-Medici × Victoria Memorial × Consulate General of Italy)
- Jun–Aug 2025 · Internship Certificate · Abhishek Dutta India
- 2024–2025 · Certificate of Merit — Designer of the Year · Sister Nivedita University
- March 2024 · Assistant Designer Certificate · Roy Calcutta (Swatantra Fashion Show — 38th AIU)
- Certificate of Merit · Sister Nivedita University (representing SNU Fashion Dept. at AIU fest)
- 2024 · Volunteer Certificate · Sutra Handloom Studies

---

## Portfolio Site

- **URL**: https://shrestha-roy.netlify.app
- **Repo**: isagiyo1ch1/shrestha-portfolio (Netlify ID: d63ecf2e-256a-4a8c-8271-893855b71907)
- **Workflow**: create branch → commit changes → `gh api repos/isagiyo1ch1/shrestha-portfolio/pulls --method POST` (REST, not GraphQL) → merge

---

## How to Update the CV

1. Edit content in `corporate_cv.js` (DOCX) or `cv_design.py` (PDFs)
2. Run the relevant script to regenerate outputs
3. To update the portfolio résumé: build the corporate DOCX, convert with `soffice --headless --convert-to pdf`, confirm it is 1 page, and commit it as `assets/pdfs/resume/ShresthaRoy_CV.pdf`
4. Create a PR and merge it

## How to Update the Portfolio Site

1. Edit `index.html` in the repo root
2. Create a new branch: `git checkout -b update/description`
3. Commit and push
4. Open PR via REST API: `gh api repos/isagiyo1ch1/shrestha-portfolio/pulls --method POST -f title="..." -f body="..." -f head="branch-name" -f base="main"`
5. Merge via REST API: `gh api repos/isagiyo1ch1/shrestha-portfolio/pulls/NUMBER/merge --method PUT -f merge_method="squash"`
