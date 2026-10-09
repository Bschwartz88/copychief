"""Build a review document from tools/data/{slug}.py.

Usage:
    python tools/build_review.py {slug}

Highlight-style review (yellow edits + sidebar comments). For native Word tracked
changes that become accept/reject suggestions in Google Docs, use
build_review_tracked.py instead.

Requires the slug's data file (see _paths.py) defining:
    REVIEW = {
        "title": "Review title",
        "comments": { 1: ("short label", "full reasoning"), ... },
        "blocks": [ (kind, ...), ... ],   # revised draft + rubric, with
                                          # {{hl:...}} edits and {{cN}} anchors
    }

Outputs (in the slug's reviews folder, see _paths.py):
    {slug}-edits.docx   (yellow highlights + Word sidebar comments)
    {slug}-edits.html   (same content, browser-viewable)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docx_lib
from _paths import load_data, resolve, checked_path


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python tools/build_review.py {slug}")
    slug = sys.argv[1]
    mod = load_data(slug)
    if not hasattr(mod, "REVIEW"):
        sys.exit(f"ERROR: {resolve(slug)['data']} has no REVIEW dict.")
    review = mod.REVIEW
    comments = review.get("comments", {})
    blocks = list(review["blocks"])

    # Append the reasoning bullet list from the comment library.
    if comments:
        blocks += [("hr",), ("h2", "Edit Reasoning")]
        blocks += [
            ("bullet", f"**[{cid}] {label}** — {reason}")
            for cid, (label, reason) in sorted(comments.items())
        ]

    out_dir = resolve(slug)["reviews"]
    out_dir.mkdir(parents=True, exist_ok=True)
    docx_path = checked_path(out_dir / f"{slug}-edits.docx")
    html_path = checked_path(out_dir / f"{slug}-edits.html")

    doc = docx_lib.render_docx(blocks, comments=comments, title=review.get("title"))
    doc.save(docx_path)

    html_path.write_text(
        docx_lib.render_html(review["blocks"], comments=comments, title=review.get("title")),
        encoding="utf-8",
    )

    print(f"OK: {docx_path}")
    print(f"OK: {html_path}")


if __name__ == "__main__":
    main()
