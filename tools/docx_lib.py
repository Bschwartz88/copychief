"""Shared rendering engine for CopyChief build tools.

Renders block lists (defined in tools/data/{slug}.py) into brand-formatted
Word documents, Markdown, and HTML. Used by build_prep.py and build_review.py.

Block kinds:
    ("h1", text)            Montserrat bold 24pt, brand navy
    ("h2", text)            Montserrat semi-bold 16pt
    ("h3", text)            Montserrat bold 12pt
    ("body", text)          Open Sans 11pt paragraph
    ("bullet", text)        bulleted list item
    ("meta", label, value)  bold label + value on one line
    ("hr",)                 horizontal spacer

Inline markup inside any text:
    **bold** and *italic*
    [text](url)             live hyperlink
    {{hl:text}}             yellow-highlighted suggested edit
    {{note:text}}           light-blue inline comment/reasoning
    {{c3}}                  anchors sidebar comment #3 (from COMMENTS dict)
                            to the run immediately before it
"""

from __future__ import annotations

import html as htmllib
import re
from _security import safe_url, safe_comment_id

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

NAVY = (26, 58, 143)
BLUE = (40, 80, 160)
LIGHT_BLUE_FILL = "CFE7F5"  # inline note shading (approximates light blue highlight)

TOKEN_RE = re.compile(
    r"(\{\{hl:.*?\}\}|\{\{note:.*?\}\}|\{\{c\d+\}\}|\[[^\]]+\]\([^)]+\)|\*\*.*?\*\*|\*[^*]+\*)",
    re.S,
)


def _set_font(run, name="Open Sans", size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def _add_hyperlink(paragraph, text, url, size=11):
    url = safe_url(url)
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = paragraph.add_run(text)
    _set_font(run, size=size, color=(5, 99, 193))
    run.font.underline = True
    run._r.getparent().remove(run._r)
    link.append(run._r)
    paragraph._p.append(link)
    return run


def render_runs(doc, paragraph, text, comments=None, size=11):
    """Render inline-markup text into runs. Returns list of created runs."""
    runs = []
    for part in TOKEN_RE.split(text):
        if not part:
            continue
        if part.startswith("{{hl:"):
            run = paragraph.add_run(part[5:-2])
            _set_font(run, size=size)
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            runs.append(run)
        elif part.startswith("{{note:"):
            run = paragraph.add_run(part[7:-2])
            _set_font(run, size=size, italic=True, color=(23, 84, 122))
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:fill"), LIGHT_BLUE_FILL)
            run._r.get_or_add_rPr().append(shd)
            runs.append(run)
        elif re.fullmatch(r"\{\{c\d+\}\}", part):
            cid = int(part[3:-2])
            if comments and cid in comments:
                label, reason = comments[cid]
                anchor = runs[-1:] or paragraph.runs[-1:]
                if anchor:
                    doc.add_comment(
                        runs=anchor,
                        text=f"[{cid}] {label}: {reason}",
                        author="CopyChief",
                        initials="CC",
                    )
        elif part.startswith("[") and "](" in part:
            m = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", part)
            runs.append(_add_hyperlink(paragraph, m.group(1), m.group(2), size=size))
        elif part.startswith("**"):
            run = paragraph.add_run(part[2:-2])
            _set_font(run, size=size, bold=True)
            runs.append(run)
        elif part.startswith("*"):
            run = paragraph.add_run(part[1:-1])
            _set_font(run, size=size, italic=True)
            runs.append(run)
        else:
            run = paragraph.add_run(part)
            _set_font(run, size=size)
            runs.append(run)
    return runs


def render_docx(blocks, comments=None, title=None):
    """Render a block list to a python-docx Document."""
    doc = docx.Document()
    if title:
        blocks = [("h1", title)] + list(blocks)
    for block in blocks:
        kind = block[0]
        if kind == "h1":
            p = doc.add_paragraph()
            p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(18), Pt(6)
            _set_font(p.add_run(block[1]), "Montserrat", 24, bold=True, color=NAVY)
        elif kind == "h2":
            p = doc.add_paragraph()
            p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(14), Pt(4)
            _set_font(p.add_run(block[1]), "Montserrat", 16, bold=True, color=BLUE)
        elif kind == "h3":
            p = doc.add_paragraph()
            p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(10), Pt(2)
            _set_font(p.add_run(block[1]), "Montserrat", 12, bold=True, color=(60, 90, 160))
        elif kind == "body":
            p = doc.add_paragraph()
            p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(2), Pt(6)
            render_runs(doc, p, block[1], comments)
        elif kind == "bullet":
            p = doc.add_paragraph(style="List Bullet")
            render_runs(doc, p, block[1], comments)
        elif kind == "meta":
            p = doc.add_paragraph()
            p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(1), Pt(2)
            _set_font(p.add_run(block[1] + ": "), bold=True)
            render_runs(doc, p, block[2], comments)
        elif kind == "hr":
            doc.add_paragraph()
    return doc


def _md_inline(text):
    text = re.sub(r"\{\{hl:(.*?)\}\}", r"==\1==", text, flags=re.S)
    text = re.sub(r"\{\{note:(.*?)\}\}", r"> \1", text, flags=re.S)
    return re.sub(r"\{\{c(\d+)\}\}", r"[c\1]", text)


def render_md(blocks, title=None):
    """Render a block list to Markdown text."""
    out = [f"# {title}", ""] if title else []
    for block in blocks:
        kind = block[0]
        if kind in ("h1", "h2", "h3"):
            out += ["#" * int(kind[1]) + " " + block[1], ""]
        elif kind == "body":
            out += [_md_inline(block[1]), ""]
        elif kind == "bullet":
            out.append("- " + _md_inline(block[1]))
        elif kind == "meta":
            out.append(f"**{block[1]}:** {_md_inline(block[2])}")
        elif kind == "hr":
            out += ["---", ""]
    return "\n".join(out).rstrip() + "\n"


def _html_inline(text, comments=None):
    parts = []
    for part in TOKEN_RE.split(text):
        if not part:
            continue
        if part.startswith("{{hl:"):
            parts.append(f"<mark>{htmllib.escape(part[5:-2])}</mark>")
        elif part.startswith("{{note:"):
            parts.append(f'<span class="note">{htmllib.escape(part[7:-2])}</span>')
        elif re.fullmatch(r"\{\{c\d+\}\}", part):
            cid = part[3:-2]
            parts.append(f'<sup class="cref"><a href="#c{cid}">[{cid}]</a></sup>')
        elif part.startswith("[") and "](" in part:
            m = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", part)
            parts.append(f'<a href="{htmllib.escape(safe_url(m.group(2)))}">{htmllib.escape(m.group(1))}</a>')
        elif part.startswith("**"):
            parts.append(f"<strong>{htmllib.escape(part[2:-2])}</strong>")
        elif part.startswith("*"):
            parts.append(f"<em>{htmllib.escape(part[1:-1])}</em>")
        else:
            parts.append(htmllib.escape(part))
    return "".join(parts)


HTML_CSS = """
body { font-family: 'Open Sans', Arial, sans-serif; font-size: 15px; line-height: 1.6;
       max-width: 760px; margin: 40px auto; color: #1a1a1a; padding: 0 20px; }
h1, h2, h3 { font-family: 'Montserrat', Arial, sans-serif; color: #1a3a8f; }
mark { background: #fff176; }
.note { background: #cfe7f5; font-style: italic; color: #17547a; }
.cref a { text-decoration: none; color: #1a3a8f; font-weight: bold; }
.comments { border-top: 2px solid #1a3a8f; margin-top: 40px; padding-top: 16px; }
"""


def render_html(blocks, comments=None, title=None):
    """Render a block list (plus comment appendix) to a standalone HTML page."""
    out = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{htmllib.escape(title or 'CopyChief')}</title><style>{HTML_CSS}</style></head><body>"]
    if title:
        out.append(f"<h1>{htmllib.escape(title)}</h1>")
    for block in blocks:
        kind = block[0]
        if kind in ("h1", "h2", "h3"):
            n = kind[1]
            out.append(f"<h{n}>{htmllib.escape(block[1])}</h{n}>")
        elif kind == "body":
            out.append(f"<p>{_html_inline(block[1])}</p>")
        elif kind == "bullet":
            out.append(f"<ul><li>{_html_inline(block[1])}</li></ul>")
        elif kind == "meta":
            out.append(f"<p><strong>{htmllib.escape(block[1])}:</strong> {_html_inline(block[2])}</p>")
        elif kind == "hr":
            out.append("<hr>")
    if comments:
        out.append('<div class="comments"><h2>Editorial Comments</h2><ol>')
        for cid in sorted(comments):
            label, reason = comments[cid]
            cid = safe_comment_id(cid)
            out.append(f'<li id="c{cid}"><strong>{htmllib.escape(label)}.</strong> {htmllib.escape(reason)}</li>')
        out.append("</ol></div>")
    out.append("</body></html>")
    return "\n".join(out)
