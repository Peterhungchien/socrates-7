#!/usr/bin/env python3
"""Split textbook PDFs into section-level files based on the curriculum map.

Usage:
    python tools/split_pdf.py [--map MAP_FILE] [--output-dir OUTPUT_DIR]

Reads the curriculum map (default: teacher/curriculum_map.md), parses the
Markdown table for textbook filenames and page ranges, and writes individual
section PDFs to course_material/sections/.

Requires: pip install pypdf
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    sys.exit("Error: pypdf is not installed. Run: pip install pypdf")


def parse_curriculum_map(map_path: Path) -> list[dict]:
    """Parse the Markdown table in the curriculum map file.

    Returns a list of dicts with keys: unit, topic, textbook, pages, section_pdf.
    """
    text = map_path.read_text()
    # Find table rows (skip header and separator lines)
    rows = []
    in_table = False
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if not in_table:
            # First row is the header
            in_table = True
            continue
        # Skip separator row (e.g. |---|---|...)
        if all(re.fullmatch(r":?-+:?", c) for c in cols):
            continue
        if len(cols) >= 4:
            rows.append(
                {
                    "unit": cols[0],
                    "topic": cols[1],
                    "textbook": cols[2],
                    "pages": cols[3],
                    "section_pdf": cols[4] if len(cols) >= 5 else "",
                }
            )
    return rows


def parse_page_range(pages_str: str) -> tuple[int, int]:
    """Parse '16-25' into (16, 25). Pages are 1-indexed."""
    match = re.match(r"(\d+)\s*[-–]\s*(\d+)", pages_str.strip())
    if not match:
        raise ValueError(f"Cannot parse page range: {pages_str!r}")
    return int(match.group(1)), int(match.group(2))


def slugify(text: str) -> str:
    """Convert 'Unit 1.2 Activation Functions' to 'unit_1_2_activation_functions'."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", "_", text).strip("_")
    return text


def split_pdf(
    reader: PdfReader, start_page: int, end_page: int, output_path: Path
) -> None:
    """Extract pages [start_page, end_page] (1-indexed) and write to output_path."""
    writer = PdfWriter()
    for i in range(start_page - 1, min(end_page, len(reader.pages))):
        writer.add_page(reader.pages[i])
    with open(output_path, "wb") as f:
        writer.write(f)


def main():
    parser = argparse.ArgumentParser(description="Split textbook PDFs by curriculum map")
    parser.add_argument(
        "--map",
        default="teacher/curriculum_map.md",
        help="Path to curriculum map (default: teacher/curriculum_map.md)",
    )
    parser.add_argument(
        "--output-dir",
        default="course_material/sections",
        help="Output directory (default: course_material/sections)",
    )
    args = parser.parse_args()

    map_path = Path(args.map)
    output_dir = Path(args.output_dir)

    if not map_path.exists():
        sys.exit(f"Error: Curriculum map not found: {map_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    rows = parse_curriculum_map(map_path)
    if not rows:
        sys.exit("Error: No rows found in curriculum map table.")

    # Cache opened PDFs by filename
    readers: dict[str, PdfReader] = {}
    course_dir = Path("course_material")

    for row in rows:
        textbook = row["textbook"]
        if not textbook:
            continue

        # Open the PDF (cached)
        if textbook not in readers:
            pdf_path = course_dir / textbook
            if not pdf_path.exists():
                print(f"Warning: {pdf_path} not found, skipping rows for this textbook")
                readers[textbook] = None
                continue
            readers[textbook] = PdfReader(pdf_path)

        reader = readers[textbook]
        if reader is None:
            continue

        start, end = parse_page_range(row["pages"])
        section_name = f"{slugify(row['unit'])}_{slugify(row['topic'])}.pdf"
        output_path = output_dir / section_name

        split_pdf(reader, start, end, output_path)
        print(f"  {section_name}  (pages {start}-{end} from {textbook})")

    # Print reminder to update curriculum map
    print(f"\nDone. Section PDFs written to {output_dir}/")
    print("Update the 'Section PDF' column in your curriculum map if needed.")


if __name__ == "__main__":
    main()
