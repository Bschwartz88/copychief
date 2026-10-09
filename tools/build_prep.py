"""Build a prep document from tools/data/{slug}.py.

Usage:
    python tools/build_prep.py {slug}

Requires the slug's data file (see _paths.py: tools/data/{slug}.py in a client
folder, {slug}/data.py in the projects workspace) defining:
    PREP = {
        "title": "Document title",
        "blocks": [ (kind, ...), ... ],   # see docx_lib.py for block kinds
    }

Outputs (client folder / projects workspace):
    blog/research/{slug}-prep.md + .docx   or   {slug}/research/{slug}-prep.md + .docx
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docx_lib
from _paths import load_data, resolve, checked_path


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python tools/build_prep.py {slug}")
    slug = sys.argv[1]
    mod = load_data(slug)
    if not hasattr(mod, "PREP"):
        sys.exit(f"ERROR: {resolve(slug)['data']} has no PREP dict.")
    prep = mod.PREP

    out_dir = resolve(slug)["research"]
    out_dir.mkdir(parents=True, exist_ok=True)

    md_path = checked_path(out_dir / f"{slug}-prep.md")
    docx_path = checked_path(out_dir / f"{slug}-prep.docx")
    md_path.write_text(
        docx_lib.render_md(prep["blocks"], title=prep.get("title")), encoding="utf-8"
    )

    doc = docx_lib.render_docx(prep["blocks"], title=prep.get("title"))
    doc.save(docx_path)

    print(f"OK: {md_path}")
    print(f"OK: {docx_path}")


if __name__ == "__main__":
    main()
