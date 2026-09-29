#!/usr/bin/env python3
"""
Convert PDF slide files from slides-input/ to MARP markdown format in slides/.

For each PDF in slides-input/, the script extracts text AND images page by page
using PyMuPDF and writes one MARP markdown file per PDF. Output files get a
'_image' suffix (e.g. Slides_AI_Programming_afspraken_image.md) so the existing
text-only versions are not overwritten.

Content images are extracted into a single shared folder (slides/images/) with
filenames that reference the original PDF (e.g.
Slides_AI_Programming_afspraken_p03_img001.png).

Processing steps per slide:
  - Uses page.get_text("dict") which returns text and image blocks in reading
    order. Text and images are interleaved naturally.
  - Footer ornament text blocks (date, "IT Research", "AI Programming",
    "Powerpointsjabloon AP", page numbers) are filtered out by position
    (x0 > 500, y0 < 100). Repeated decorative images (AP logo, background
    bars, header logos) are recognized by position/size/frequency.
  - The first page becomes a title slide with <!-- _class: title-slide -->.
  - For each subsequent page, the first line becomes a ## header.
  - Soft line breaks inside sentences (from PDF word-wrapping) are collapsed.
"""

import pymupdf
import os
import re
from collections import Counter

INPUT_DIR = "/mnt/c/Users/p136704/Documents/brunohermanap_repos/AI_Prog_student/slides-input"
OUTPUT_DIR = "/mnt/c/Users/p136704/Documents/brunohermanap_repos/AI_Prog_student/slides"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

# Relative path (from the .md files in OUTPUT_DIR) to the shared image folder
IMAGE_SUBDIR = "images"

# MARP front matter template
FRONT_MATTER = """---
marp: true
theme: ap-theme
paginate: true
---"""

# X/threshold constants for footer/header ornament filtering.
# Footer text blocks and page numbers always appear at x0 > 500, y0 < 100.
# Content in right-column layouts (y0 >= 100) is preserved.
ORNAMENT_MIN_X = 500
ORNAMENT_MAX_Y = 100


def get_output_path(pdf_path: str) -> str:
    """Derive the output .md path from the input PDF path, with _image suffix."""
    basename = os.path.basename(pdf_path)
    md_name = re.sub(r"\.pdf$", "_image.md", basename, flags=re.IGNORECASE)
    return os.path.join(OUTPUT_DIR, md_name)


def image_signature(blk) -> tuple:
    """Return a rounded (w, h, x, y) signature for an image dict block."""
    bbox = blk["bbox"]
    w = int(round((bbox[2] - bbox[0]) / 10) * 10)
    h = int(round((bbox[3] - bbox[1]) / 10) * 10)
    x = int(round(bbox[0] / 10) * 10)
    y = int(round(bbox[1] / 10) * 10)
    return (w, h, x, y)


def find_decorative_images(doc) -> set:
    """Return set of image signatures that appear on 3+ pages (page furniture).

    Decorative images such as the AP logo, background bars and header logos
    repeat at the same position/size on many pages. Content images do not.
    """
    counter = Counter()
    for page in doc:
        for blk in page.get_text("dict")["blocks"]:
            if blk["type"] == 1:  # image block
                counter[image_signature(blk)] += 1
    return {sig for sig, count in counter.items() if count >= 3}


def is_decorative_image(blk, decorative_sigs) -> bool:
    """Check if an image dict block is decorative page furniture."""
    if image_signature(blk) in decorative_sigs:
        return True
    bbox = blk["bbox"]
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0
    # Bottom-right corner logo (AP logo area)
    if x0 > 380 and y0 > 680 and w < 180 and h < 180:
        return True
    # Full-height side decorations / background bars
    if h > 600:
        return True
    return False


def save_image(pdf_base, page_no, seq, blk) -> str | None:
    """Save one image dict block to the shared image folder.

    Returns the relative path used in the markdown, or None on failure.
    """
    image_bytes = blk.get("image")
    if not image_bytes:
        return None
    ext = blk.get("ext") or "png"
    name = f"{pdf_base}_p{page_no:02d}_img{seq:03d}.{ext}"
    path = os.path.join(IMAGE_DIR, name)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return f"{IMAGE_SUBDIR}/{name}"


def extract_text_block(blk) -> str:
    """Reconstruct the text of a text dict block."""
    lines = []
    for line in blk.get("lines", []):
        line_text = "".join(span["text"] for span in line["spans"])
        lines.append(line_text)
    return "\n".join(lines)


def is_bullet_line(line: str) -> bool:
    """Check if a line looks like a bullet point."""
    stripped = line.strip()
    return stripped.startswith("•") or stripped.startswith("-")


def is_continuation_line(line: str) -> bool:
    """Check if a line is a continuation of the previous sentence.

    A line is a continuation when the first alphabetic character is a
    lowercase letter. This handles lines that start with quote characters
    (e.g. "'belief'"), brackets (e.g. "[bron:") or other non-letter
    punctuation, while keeping table cell items such as "(International)"
    on their own line.
    """
    lead = line.strip()
    while lead and not lead[0].isalpha():
        lead = lead[1:]
    return bool(lead) and lead[0].islower()


def collapse_soft_enters(text: str) -> str:
    """Collapse soft line breaks inside sentences.

    The PDF text extraction wraps sentences across multiple lines. This
    function joins a line to the previous line when it is a continuation:
      - the line starts with a lowercase letter (possibly after leading
        punctuation), or
      - the previous line is an orphan bullet ('•')
    Lines that start a new context (bullets, titles in uppercase, table
    cells) are preserved on their own line.
    """
    lines = text.split("\n")
    result = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if result and result[-1] != "":
                result.append("")
            continue

        if stripped == "•":
            # Orphan bullet: keep it; it is joined with the following line
            result.append(stripped)
        elif is_bullet_line(stripped):
            # Normal bullet point starts a new line
            result.append(stripped)
        elif result and result[-1] != "":
            last = result[-1]
            if last == "•":
                # Join orphan bullet with this line
                result[-1] = last + " " + stripped
            elif is_continuation_line(stripped):
                # Continuation of the previous sentence
                result[-1] = last + " " + stripped
            else:
                # Upper-case start = new context (title / table cell / paragraph)
                result.append(stripped)
        else:
            result.append(stripped)

    return "\n".join(result)


def make_title_slide(text: str) -> str:
    """Format the first page content as a MARP title slide.

    The first line (plus any following lines that look like a continuation,
    i.e. start with a lowercase letter) becomes the main # heading.
    The next non-bullet line becomes the ## subheading.
    Any remaining content after the heading(s) is kept as-is.
    """
    lines = text.splitlines()
    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return ""

    # Gather title lines: first line + continuation lines that start lowercase
    title_parts = [lines[0].strip()]
    idx = 1
    while idx < len(lines):
        line = lines[idx].strip()
        if not line or is_bullet_line(line):
            break
        first_char = line[0]
        if first_char.islower() or first_char.isdigit():
            title_parts.append(line)
            idx += 1
        else:
            break
    title = " ".join(title_parts)
    result = ["<!-- _class: title-slide -->", "", f"# {title}"]

    # Check remaining lines for a subtitle candidate
    remaining = lines[idx:]
    if remaining and remaining[0].strip() and not is_bullet_line(remaining[0]):
        # It's a subtitle
        result.append(f"## {remaining[0].strip()}")
        remaining = remaining[1:]

    # Remaining content (if any)
    if remaining:
        # Skip any leading empty lines
        while remaining and not remaining[0].strip():
            remaining.pop(0)
        if remaining:
            result.append("")
            result.extend(remaining)

    return "\n".join(result)


def page_units(page, pdf_base, page_no, decorative_sigs, include_images=True):
    """Return ordered content units for one page.

    Each unit is either ('text', text) or ('image', markdown_line).
    Consecutive text blocks are merged into a single text unit so that
    soft-line-break collapsing works across them. Images are placed at their
    reading-order position (dict blocks already come in reading order).
    """
    units = []
    pending_text = []

    def flush():
        if pending_text:
            units.append(("text", "\n".join(pending_text)))
            pending_text.clear()

    seq = 0
    for blk in page.get_text("dict")["blocks"]:
        if blk["type"] == 1:
            # Image block
            if not include_images:
                continue
            if is_decorative_image(blk, decorative_sigs):
                continue
            seq += 1
            rel = save_image(pdf_base, page_no, seq, blk)
            if rel:
                flush()
                units.append(("image", f"![]({rel})"))
        else:
            # Text block
            bbox = blk["bbox"]
            if bbox[0] > ORNAMENT_MIN_X and bbox[1] < ORNAMENT_MAX_Y:
                continue  # footer ornament block
            text = extract_text_block(blk).strip()
            if text:
                pending_text.append(text)
    flush()
    return units


def convert_pdf_to_marp(pdf_path: str) -> str:
    """Extract text and images from a PDF and return a MARP markdown string."""
    doc = pymupdf.open(pdf_path)
    pdf_base = os.path.splitext(os.path.basename(pdf_path))[0]
    decorative_sigs = find_decorative_images(doc)

    lines = [FRONT_MATTER, ""]

    for i, page in enumerate(doc):
        page_no = i + 1
        units = page_units(page, pdf_base, page_no, decorative_sigs, include_images=(i > 0))

        if i == 0:
            # Title slide: text only (cover decorations restyled by MARP CSS)
            text_parts = [u[1] for u in units if u[0] == "text"]
            full_text = "\n".join(text_parts).strip()
            if not full_text:
                full_text = "(geen titel)"
            lines.append(make_title_slide(full_text))
        else:
            lines.append("")
            lines.append("---")
            lines.append("")
            if not units:
                continue
            parts = []
            header_done = False
            for kind, content in units:
                if kind == "image":
                    parts.append(content)
                else:
                    text = collapse_soft_enters(content).strip()
                    if not text:
                        continue
                    if not header_done:
                        split = text.split("\n", 1)
                        first = split[0].strip()
                        if is_bullet_line(first):
                            first = re.sub(r"^[•\-]\s*", "", first)
                        parts.append(f"## {first}")
                        header_done = True
                        if len(split) > 1 and split[1].strip():
                            parts.append(split[1].strip())
                    else:
                        parts.append(text)
            if parts:
                lines.append("\n\n".join(parts))

    doc.close()
    return "\n".join(lines) + "\n"


def main():
    # Ensure output directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Gather all PDF files in the input directory
    pdf_files = sorted(
        f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")
    )

    if not pdf_files:
        print("No PDF files found in slides-input/.")
        return

    for pdf_name in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_name)
        output_path = get_output_path(pdf_path)

        print(f"Processing: {pdf_name} …")
        marp_content = convert_pdf_to_marp(pdf_path)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(marp_content)

        print(f"  → Wrote {output_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
