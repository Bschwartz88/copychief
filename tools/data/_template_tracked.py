"""TEMPLATE for tracked-changes review data. Copy the BLOCKS/COMMENTS into the slug's
data file (tools/data/{slug}.py in a client folder, {slug}/data.py in projects).

This file holds the FULL article as a typed BLOCKS list and the editorial rationale
as a COMMENTS dict. `tools/build_review_tracked.py <slug>` reads it and emits the
tracked-changes .docx and HTML redline into the slug's reviews folder.

How to fill it in (the editor does this, not the script):
  1. Start from the author's original draft. Every block's base text must be the
     ORIGINAL wording, so a reader who REJECTS a change gets their exact text back.
  2. For an in-place edit, keep op=None and mix token kinds:
       ("d", "<original span>"), ("i", "<replacement>")  -> a delete+insert pair
  3. For a whole-paragraph rewrite, emit the original as ("p", "del", None, [("k", original)])
     immediately followed by the new version as ("p", "ins", <cid>, [("k", new)]).
  4. Attach a COMMENTS entry (the "why") to the block that carries the change via its
     comment_id. Rationale lives ONLY in comments — never as inline [1] markers —
     so "Accept all" leaves clean copy.

BLOCKS tuple shapes:
  (style, op, comment_id, tokens)     text:  style in {"h1","h2","h3","p","li"}
  ("table", None, None, rows)         table: rows = list of cell-string lists (row 0 = header)

op:        None  -> in-place edits via token kinds below
           "ins" -> entire paragraph is an insertion (new content)
           "del" -> entire paragraph is a deletion (removed content)
comment_id: int key into COMMENTS, or None

Token kinds:
  ("k",  text)        keep (unchanged)        ("kb", text)  keep, bold
  ("i",  text)        insert                  ("ib", text)  insert, bold
  ("d",  text)        delete
  ("kl", text, url)   keep link               ("il", text, url) insert link
  ("c",  cid)         point comment (zero-width anchor; no text change)
"""

# Optional metadata --------------------------------------------------------
TITLE = "Sample one-off article"          # shows in the .docx/redline heading
AUTHOR = "CopyChief (Editor)"             # tracked-change / comment author

# Editorial rationale: cid -> (short label, full reasoning) -----------------
COMMENTS = {
    1: ("Headline clarity", "Tightened the headline to lead with the primary keyword "
        "and cut the trailing clause that buried the value proposition."),
    2: ("Lead rewrite", "Replaced the throat-clearing first paragraph with a direct, "
        "second-person hook that states the stakes in the first sentence."),
    3: ("Grammar", "Removed the comma splice and split into two sentences."),
}

# The article ---------------------------------------------------------------
BLOCKS = [
    ("h1", None, 1, [
        ("d", "Some Things You Might Want To Know About The Topic At Hand"),
        ("i", "What you need to know about the topic"),
    ]),

    ("p", "del", None, [("k",
        "In today's fast-paced world, it is important to note that there are many "
        "things to consider before getting started with the subject of this article.")]),
    ("p", "ins", 2, [("k",
        "You have a decision to make, and the wrong call is expensive. Here is what "
        "actually matters before you commit.")]),

    ("h2", None, None, [("k", "The first consideration")]),
    ("p", None, 3, [
        ("k", "This matters a great deal"),
        ("d", ", it affects everything downstream"),
        ("i", ". It affects everything downstream"),
        ("k", ".")]),

    ("li", None, None, [("kb", "Point one: "), ("k", "a kept bullet, unchanged.")]),
    ("li", None, None, [
        ("k", "A bullet with an inline fix from "),
        ("d", "alot"), ("i", "a lot"),
        ("k", " of small errors.")]),

    ("table", None, None, [
        ["Option", "Strength", "Trade-off"],
        ["Option A", "Fast to set up", "Less flexible"],
        ["Option B", "Highly flexible", "Slower to set up"],
    ]),
]
