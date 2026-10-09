# tools/data/ — per-article content files

One Python file per slug: `tools/data/{slug}.py`. Claude writes CONTENT here,
not code. All formatting, docx generation, sidebar comments, highlights, and
HTML output are handled by the shared tools (`build_prep.py`, `build_review.py`,
`docx_lib.py`). Never write a new build script for an article.

## Schema

Only literal assignments are accepted: dictionaries, lists, tuples, strings,
numbers, booleans and None. Do not add imports, function calls, variable references
or other executable code. The loader reads content without executing Python.

```python
PREP = {
    "title": "Prep: Article Title",
    "blocks": [
        ("h2", "Assignment Summary"),
        ("body", "Text with **bold**, *italic*, and [links](https://...)."),
        ("bullet", "A bulleted item."),
        ("meta", "Meta Title", "Under 60 characters"),
        ("hr",),
    ],
}

REVIEW = {
    "title": "Editorial Review: Article Title",
    "comments": {
        1: ("Short label", "Full reasoning shown in the sidebar comment and reasoning list."),
    },
    "blocks": [
        ("h2", "Editorial Summary"),
        ("body", "2-3 sentence assessment."),
        ("h2", "Revised Draft"),
        ("body", "Original text {{hl:suggested replacement}}{{c1}} continues here."),
    ],
}
```

## Inline markup

| Markup | Renders as |
|---|---|
| `**bold**` / `*italic*` | bold / italic |
| `[text](url)` | live hyperlink (docx and HTML) |
| `{{hl:text}}` | yellow-highlighted suggested edit |
| `{{note:text}}` | light-blue inline comment text |
| `{{c3}}` | anchors sidebar comment #3 to the run before it |

Block types: `h1`, `h2`, `h3`, `body`, `bullet`, `meta` and `hr`.

Two limits to know:
- Inline markup renders only in `body`, `bullet` and `meta` blocks. Heading text is printed
  as is, so to suggest a new heading, use the new text as the heading and put the
  `{{note:...}}` and `{{cN}}` in the body line below it.
- Markup doesn't nest. A `[link](url)` inside `{{hl:...}}` prints as raw text, so close
  the highlight before the link: `{{hl:See}} [title](url){{c3}}`.

A data file can contain PREP, REVIEW, or both. Build with:

```powershell
python tools/build_prep.py {slug}
python tools/build_review.py {slug}
```

## Tracked-changes reviews (`build_review_tracked.py`)

Add a `TRACKED` dict to the same data file:

```python
TRACKED = {
    "title": "Editorial Review: Article Title",
    "author": "CopyChief (Editor)",          # optional
    "comments": {1: ("Short label", "Full reasoning")},
    "blocks": [ (style, op, comment_id, tokens), ... ],
}
```

The block and token shapes, and how to express edits so that rejecting one restores the
original wording, are in `data/_template_tracked.py`. Build with
`python tools/build_review_tracked.py {slug}`.

## Where the data file lives

In a client folder, it's `tools/data/{slug}.py`. In the projects workspace, it's
`{slug}/data.py`. See `tools/_paths.py`.
