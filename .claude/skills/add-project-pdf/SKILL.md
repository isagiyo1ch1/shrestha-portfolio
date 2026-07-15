---
name: add-project-pdf
description: Convert a project PDF to WebP images and wire it up in the portfolio. Usage: /add-project-pdf <pdf-path> [slug]
---

You are helping add a new project PDF to Shrestha Roy's fashion design portfolio at `c:\Users\Ashueep\shrestha-portfolio`.

## What this skill does

1. Converts the PDF to per-page WebP images using the existing conversion script
2. Reads the generated manifest to get the page count
3. Updates the `PROJECTS` array in `index.html` to point to the local images instead of the Google Drive link

## Arguments

The user invokes this skill as:
```
/add-project-pdf <pdf-path> [slug]
```

- `<pdf-path>`: path to the PDF, relative to the project root (e.g. `assets/pdfs/what-remains.pdf`) or absolute
- `[slug]`: optional. If omitted, derive it from the PDF filename: lowercase, spaces → hyphens, strip `.pdf`
  - e.g. `"what remains.pdf"` → `what-remains`
  - e.g. `"ad internship reprt.pdf"` → `ad-internship-reprt` (use as-is from filename unless user specified)

## Step-by-step instructions

### Step 1 — Resolve paths and slug

Parse the args. Determine:
- Absolute path to the PDF
- The project slug (from args or derived from filename)

### Step 2 — Run the conversion script

Run the following PowerShell command from the project root:

```powershell
python canvas/pdf_to_webp.py "<pdf-path>" "<slug>"
```

If pymupdf or Pillow are not installed, pip install them first:
```powershell
pip install pymupdf Pillow --quiet
```

Capture and show the output so the user can see page-by-page progress.

### Step 3 — Read the manifest

After conversion, read `assets/images/<slug>/manifest.json`. Extract:
- `page_count`: total number of pages

### Step 4 — Find the matching project in PROJECTS

Read `index.html` and locate the `PROJECTS` array (starts around line 474).

Find the entry whose `title` most closely matches the PDF filename or slug — do a fuzzy match (e.g. slug `ad-internship` matches `Abhishek Dutta India` because that's the project that was already wired up; for a new PDF, match on keywords in the title vs the slug/filename).

If you cannot determine which project it maps to with reasonable confidence, show the user the list of projects and ask them to confirm which one this PDF belongs to before making any changes.

### Step 5 — Update index.html

In the matched PROJECTS entry:
- Add `slug: '<slug>'`
- Add `pages: <page_count>`
- Remove the `href` field (the Drive link) — the viewer will handle navigation

The entry should go from:
```js
{ title: 'Example Project', tag: 'Category · Year', img: 'assets/thumbnails/example.jpg', href: 'https://drive.google.com/...' },
```
to:
```js
{ title: 'Example Project', tag: 'Category · Year', img: 'assets/thumbnails/example.jpg', slug: 'example-slug', pages: 22 },
```

Use the Edit tool to make this change — match enough surrounding context to be unambiguous.

### Step 6 — Report

Tell the user:
- How many pages were converted
- Total image size in MB
- Which PROJECTS entry was updated
- That they can now test it by navigating to the project in the wheel and clicking "Open Project"

## Important rules

- Never overwrite an existing `assets/images/<slug>/` directory without warning the user first
- If the slug already exists in PROJECTS (already wired up), tell the user and stop
- Do not modify anything other than the matching PROJECTS entry in index.html
- Do not create any documentation files or READMEs
- If the conversion script fails, show the error and stop — do not proceed to edit index.html
