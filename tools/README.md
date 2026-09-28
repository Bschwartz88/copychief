# tools/

The shared CopyChief build tools. **One version, used everywhere.** The master copy is
this folder in the `copychief` GitHub template. Every client folder and the projects
workspace carries an identical copy. To change formatting or behavior, change it here,
then copy the folder to each client, so the copies never drift apart.

Claude writes *content* into a data file. It never writes a new build script per article.

| Script | What it builds |
|---|---|
| `build_prep.py {slug}` | Prep doc: `{slug}-prep.md` + `.docx` from the data file's `PREP` dict |
| `build_review.py {slug}` | Highlight review: yellow edits, light-blue notes and Word sidebar comments (`REVIEW` dict) |
| `build_review_tracked.py {slug}` | Tracked-changes review: native Word insertions and deletions plus anchored comments. It opens in Google Docs as accept/reject **suggestions** (`TRACKED` dict, or `BLOCKS`/`COMMENTS`) |
| `quick.py` | Quick mode for one-off jobs with no folder (used by the `copychief-quick` skill). Reads an attached draft, builds a tracked review from plain revised text by word diff and checks it, and renders prep, scorecard and draft docs. Nothing in the folder workflows calls it. Usage is in its docstring |

Supporting files:
- `docx_lib.py` handles brand formatting (Montserrat/Open Sans, colors, links and comments) for the prep and highlight builds.
- `_paths.py` finds the data file and output folders for either layout (below).
- `data/README.md` describes the data-file schema, and `data/_template_tracked.py` is a worked tracked-changes example.

## Layouts (resolved automatically by `_paths.py`)

| | Client folder (has `blog/`) | Projects workspace |
|---|---|---|
| Data file | `tools/data/{slug}.py` | `{slug}/data.py` |
| Prep output | `blog/research/` | `{slug}/research/` |
| Review output | `blog/reviews/` | `{slug}/reviews/` |

## Which review style?

- **Highlight** (`build_review.py`) is for an author who reads the edits and retypes them. It's easy to scan, and the reasoning is shown inline.
- **Tracked** (`build_review_tracked.py`) is for an author who accepts or rejects each edit in Word or Google Docs. Rejecting an edit restores the exact original wording. To use it in Google Docs, upload the `.docx` to Drive and choose **Open with → Google Docs**.

## Setup

- **Windows:** `py -m venv .venv`, activate it with `.venv\Scripts\Activate.ps1`, then run `pip install -r requirements.txt`.
- **Linux sandbox:** use `python3` directly, and run `pip install -r requirements.txt --break-system-packages` if packages are missing.
