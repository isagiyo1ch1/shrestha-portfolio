"""
pdf_to_webp.py
Converts a PDF to per-page WebP images for use in the portfolio site.

Usage:
    python canvas/pdf_to_webp.py <pdf_path> <project_slug>

Example:
    python canvas/pdf_to_webp.py "assets/pdfs/ad internship reprt.pdf" ad-internship

Output:
    assets/images/<project_slug>/01.webp, 02.webp, ...
    assets/images/<project_slug>/manifest.json
"""

import sys
import json
import time
from pathlib import Path

try:
    import fitz  # pymupdf
except ImportError:
    print("pymupdf not installed. Run: pip install pymupdf")
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# Target width in pixels for the longest side of each page.
# 1920px covers full HD screens; 4K users will see slight softness but files stay manageable.
TARGET_PX = 1920
WEBP_QUALITY = 87


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def convert(pdf_path: Path, project_slug: str):
    out_dir = Path("assets/images") / project_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    page_count = len(doc)
    manifest_pages = []

    print(f"\n  PDF:     {pdf_path.name}")
    print(f"  Pages:   {page_count}")
    print(f"  Output:  {out_dir}/\n")

    for i, page in enumerate(doc):
        page_num = i + 1
        rect = page.rect
        w, h = rect.width, rect.height

        # Scale so the longest side hits TARGET_PX
        scale = TARGET_PX / max(w, h)
        mat = fitz.Matrix(scale, scale)

        pix = page.get_pixmap(matrix=mat, alpha=False)

        out_path = out_dir / f"{page_num:02d}.webp"
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(str(out_path), "WEBP", quality=WEBP_QUALITY, method=6)

        size_kb = out_path.stat().st_size // 1024
        orientation = "landscape" if w > h else "portrait"
        print(f"  [{page_num:02d}/{page_count}]  {pix.width}×{pix.height}  {orientation}  {size_kb} KB")

        manifest_pages.append({
            "page": page_num,
            "file": f"{page_num:02d}.webp",
            "width": pix.width,
            "height": pix.height,
            "orientation": orientation,
            "size_kb": size_kb,
        })

    doc.close()

    manifest = {
        "slug": project_slug,
        "title": slug_to_title(project_slug),
        "page_count": page_count,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "pages": manifest_pages,
    }

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    total_kb = sum(p["size_kb"] for p in manifest_pages)
    orientations = set(p["orientation"] for p in manifest_pages)

    print(f"\n  Done.")
    print(f"  Total size:    {total_kb} KB ({total_kb / 1024:.1f} MB)")
    print(f"  Orientations:  {', '.join(orientations)}")
    print(f"  Manifest:      {manifest_path}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python canvas/pdf_to_webp.py <pdf_path> <project_slug>")
        print('Example: python canvas/pdf_to_webp.py "assets/pdfs/ad internship reprt.pdf" ad-internship')
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    project_slug = sys.argv[2]

    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    convert(pdf_path, project_slug)
