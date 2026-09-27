"""Where a slug's data file and outputs live.

CopyChief uses two folder layouts, and every build tool resolves paths here so
the same tools work in both:

  Client folder (has blog/ at the root, e.g. acme-corp):
      data     tools/data/{slug}.py
      prep     blog/research/{slug}-prep.md / .docx
      review   blog/reviews/{slug}-edits.docx / .html

  Projects workspace (no blog/; one folder per one-off job):
      data     {slug}/data.py   (review-data.py is still accepted)
      prep     {slug}/research/{slug}-prep.md / .docx
      review   {slug}/reviews/{slug}-edits.docx / .html
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _find(root: Path, name: str):
    """Case-insensitive child lookup (Windows is case-insensitive, Linux isn't)."""
    for child in root.iterdir() if root.is_dir() else []:
        if child.name.lower() == name.lower():
            return child
    return None


def resolve(slug: str) -> dict:
    blog = _find(ROOT, "blog")
    if blog is not None:
        return {
            "layout": "client",
            "data": ROOT / "tools" / "data" / f"{slug}.py",
            "research": blog / "research",
            "reviews": blog / "reviews",
        }
    proj = ROOT / slug
    data = proj / "data.py"
    if not data.exists() and (proj / "review-data.py").exists():
        data = proj / "review-data.py"
    return {
        "layout": "project",
        "data": data,
        "research": proj / "research",
        "reviews": proj / "reviews",
    }


def load_data(slug: str):
    path = resolve(slug)["data"]
    if not path.exists():
        sys.exit(f"ERROR: no data file at {path}. Create it first (see tools/data/README.md).")
    spec = importlib.util.spec_from_file_location(f"data_{slug.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
