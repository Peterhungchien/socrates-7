#!/usr/bin/env python3
"""Extract embedded TOC (bookmarks/outlines) from a PDF and output as YAML.

Usage:
    python extract_toc.py <pdf_path>

Outputs YAML to stdout with the full TOC hierarchy and quality metrics.
Exit code 0 if TOC found, 1 if no TOC embedded.

Requires: pip install pymupdf pyyaml
"""

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


def compute_quality(toc: list[list], page_count: int) -> dict:
    """Compute quality metrics for the extracted TOC."""
    if not toc:
        return {"entry_count": 0, "page_count": page_count, "coverage_ratio": 0.0, "max_gap": page_count}

    pages = sorted(entry[2] for entry in toc)

    # Coverage: fraction of the book's pages that fall between the first and last TOC entry
    first_page = pages[0]
    last_page = pages[-1]
    covered = last_page - first_page + 1
    coverage_ratio = round(covered / page_count, 2) if page_count > 0 else 0.0

    # Max gap between consecutive TOC-referenced pages
    max_gap = 0
    for i in range(1, len(pages)):
        gap = pages[i] - pages[i - 1]
        if gap > max_gap:
            max_gap = gap

    return {
        "entry_count": len(toc),
        "page_count": page_count,
        "coverage_ratio": coverage_ratio,
        "max_gap": max_gap,
    }


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pdf_path>", file=sys.stderr)
        sys.exit(2)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        sys.exit(2)

    doc = pymupdf.open(pdf_path)
    raw_toc = doc.get_toc()
    page_count = len(doc)
    doc.close()

    if not raw_toc:
        print("No embedded TOC found.", file=sys.stderr)
        sys.exit(1)

    toc_entries = [{"level": entry[0], "title": entry[1], "page": entry[2]} for entry in raw_toc]
    quality = compute_quality(raw_toc, page_count)

    output = {"toc": toc_entries, "quality": quality}
    yaml.dump(output, sys.stdout, default_flow_style=False, sort_keys=False, allow_unicode=True)


if __name__ == "__main__":
    main()
