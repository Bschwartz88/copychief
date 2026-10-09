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

import ast
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent


def _find(root: Path, name: str):
    """Case-insensitive child lookup (Windows is case-insensitive, Linux isn't)."""
    for child in root.iterdir() if root.is_dir() else []:
        if child.name.lower() == name.lower():
            return child
    return None


def resolve(slug: str) -> dict:
    # Accept historical mixed-case/underscore slugs, but never paths or devices.
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", slug)
            or slug.upper() in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
            or re.fullmatch(r"(?i)(COM|LPT)[0-9]", slug)):
        raise ValueError("Invalid article slug: use letters, numbers, hyphens or underscores.")
    blog = _find(ROOT, "blog")
    if blog is not None:
        paths = {
            "layout": "client",
            "data": ROOT / "tools" / "data" / f"{slug}.py",
            "research": blog / "research",
            "reviews": blog / "reviews",
        }
    else:
        proj = ROOT / slug
        data = proj / "data.py"
        if not data.exists() and (proj / "review-data.py").exists():
            data = proj / "review-data.py"
        paths = {"layout": "project", "data": data,
                 "research": proj / "research", "reviews": proj / "reviews"}
    for key in ("data", "research", "reviews"):
        checked_path(paths[key])
    return paths


def checked_path(path: Path) -> Path:
    """Reject symlinks/junctions that redirect a build outside its project."""
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Build path escapes the project root.")
    return path


def load_data(slug: str):
    path = resolve(slug)["data"]
    if not path.exists():
        sys.exit(f"ERROR: no data file at {path}. Create it first (see tools/data/README.md).")
    # These files are content, not programs. Never import or execute them.
    if path.stat().st_size > 2_000_000:
        raise ValueError("Article data exceeds the 2 MB limit.")
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=path.name)
    allowed = {"PREP", "REVIEW", "TRACKED", "BLOCKS", "COMMENTS", "TITLE", "AUTHOR"}
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue  # module documentation
        if (not isinstance(node, ast.Assign) or len(node.targets) != 1
                or not isinstance(node.targets[0], ast.Name)
                or node.targets[0].id not in allowed):
            raise ValueError("Article data must contain only literal content assignments.")
        name = node.targets[0].id
        if name in values:
            raise ValueError("Duplicate article data assignment.")
        try:
            values[name] = ast.literal_eval(node.value)
        except (ValueError, TypeError, RecursionError) as exc:
            raise ValueError("Article data cannot contain executable expressions.") from exc
    return SimpleNamespace(**values)
