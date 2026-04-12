#!/usr/bin/env python3
"""Split textbook PDFs into section-level files based on the curriculum map.

Usage:
    python tools/split_pdf.py [--map MAP_FILE] [--output-dir OUTPUT_DIR]

Reads the curriculum map (default: teacher/curriculum_map.yaml), parses the
YAML sections for textbook filenames and page ranges, and writes individual
section PDFs to course_material/sections/.

Requires: pip install pymupdf pyyaml
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    sys.exit("Error: pymupdf is not installed. Run: pip install pymupdf pyyaml")

try:
    import yaml
except ImportError:
    sys.exit("Error: pyyaml is not installed. Run: pip install pymupdf pyyaml")


def slugify(text: str) -> str:
    """Convert 'Unit 1.2 Activation Functions' to 'unit_1_2_activation_functions'."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", "_", text).strip("_")
    return text


def split_pdf(
    doc: pymupdf.Document, start_page: int, end_page: int, output_path: Path
) -> None:
    """Extract pages [start_page, end_page] (1-indexed) and write to output_path."""
    output = pymupdf.open()
    # insert_pdf uses 0-indexed pages, end is inclusive
    output.insert_pdf(doc, from_page=start_page - 1, to_page=min(end_page, len(doc)) - 1)
    output.save(output_path)
    output.close()


def main():
    parser = argparse.ArgumentParser(description="Split textbook PDFs by curriculum map")
    parser.add_argument(
        "--map",
        default="teacher/curriculum_map.yaml",
        help="Path to curriculum map (default: teacher/curriculum_map.yaml)",
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

    data = yaml.safe_load(map_path.read_text())
    rows = data.get("sections") or []
    if not rows:
        sys.exit("Error: No sections found in curriculum map.")

    # Cache opened PDFs by filename
    docs: dict[str, pymupdf.Document | None] = {}
    course_dir = Path("course_material")

    for row in rows:
        textbook = row.get("textbook", "")
        if not textbook:
            continue

        # Open the PDF (cached)
        if textbook not in docs:
            pdf_path = course_dir / textbook
            if not pdf_path.exists():
                print(f"Warning: {pdf_path} not found, skipping rows for this textbook")
                docs[textbook] = None
                continue
            docs[textbook] = pymupdf.open(pdf_path)

        doc = docs[textbook]
        if doc is None:
            continue

        start = int(row["start_page"])
        end = int(row["end_page"])
        section_name = f"{slugify(str(row['unit']))}_{slugify(row['topic'])}.pdf"
        output_path = output_dir / section_name

        split_pdf(doc, start, end, output_path)
        row["section_pdf"] = section_name
        print(f"  {section_name}  (pages {start}-{end} from {textbook})")

    # Close cached documents
    for doc in docs.values():
        if doc is not None:
            doc.close()

    # Write section_pdf values back to the YAML file
    data["sections"] = rows
    with open(map_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f"\nDone. Section PDFs written to {output_dir}/")
    print(f"Updated section_pdf fields in {map_path}.")


if __name__ == "__main__":
    main()
