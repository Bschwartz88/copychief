# CopyChief

A Claude Code workflow system for B2B content marketing teams. CopyChief turns Claude into a full content writing and editorial partner — handling research, drafting, and structured review against your brand standards.

## What It Does

CopyChief gives Claude persistent knowledge about your brand so it can:

- **Prep** assignments before writing: research angle, SEO recommendations, outline, and lead paragraph draft
- **Review** drafts against your brief, brand voice, author voice, persona, and SEO strategy — with a weighted scoring rubric
- **Write** content that consistently matches your voice, targets the right keywords, and serves the right audience

All outputs are delivered as formatted .html documents or Word documents with sidebar editorial comments (that can be imported easily into a Google Doc).

## How It Works

The system uses four layers:

1. **`CLAUDE.md`** — Project-level instructions that Claude loads in every session. Defines Claude's role, which context files to load, and your working preferences.
2. **`/context/` files** — Your brand's knowledge base: editorial standards, SEO strategy, audience personas, messaging framework, brand reference, and named author voices.
3. **`/commands/` scripts** — Two slash commands (`/prep` and `/review`) that execute structured workflows against any assignment brief.
4. **`/skills/` files** — Add skills if you like for topics like AEO/GEO/SEO or humanizing text.

---

## Setup

### 1. Prerequisites

- [Claude Code](https://claude.ai/code) installed (CLI, desktop app, or IDE extension)
- Python 3.10+ with a virtual environment
- Required Python packages: `python-docx`, `markdown`, `openpyxl`, `pypandoc`, `pillow`

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install python-docx markdown openpyxl pypandoc pillow
```

### 2. Fill in the Context Files

Open each file in `/context/` and replace the `[PLACEHOLDER]` values with your company's information:

| File | What It Contains |
|---|---|
| `editorial-standards.md` | Voice, tone, style rules, content templates, source tiers |
| `seo-strategy.md` | Keyword architecture, SEO specs by content type, differentiators |
| `personas.md` | Buyer and practitioner audience profiles |
| `messaging-framework.md` | Brand pillars, taglines, proof points, boilerplate |
| `brand-reference.md` | Visual identity, competitor SWOT, competitive SEO landscape |
| `expert-voice.md` | Named author's voice, vocabulary, structural templates |

> The system works without all files populated — fill in what you have and expand over time.

### 3. Update `CLAUDE.md`

Replace `[COMPANY NAME]` and `[INDUSTRY]` at the top of `CLAUDE.md` with your company name and industry.

### 4. Update the Prep Command

In `.claude/Commands/prep.md`, replace `[YOUR COMPANY WEBSITE URL]` and `[YOUR BLOG URL]` in step 5 with your actual URLs.

---

## Usage

### Writing an Assignment Brief

Create a Markdown file in `/blog/briefs/` named after your assignment slug (e.g., `zero-trust-explainer.md`).

A brief should include:
- Topic and working title
- Primary goal (inform / persuade / generate leads)
- Target persona
- Target keywords
- Word count target
- Author (byline name or "staff")
- CTA
- Any specific points to cover

### Running /prep

Open Claude Code in this project directory and run:

```
/prep zero-trust-explainer
```

Claude will read your brief, load the relevant context files, and deliver a prep document to `/blog/research/zero-trust-explainer-prep.docx` containing:

- Assignment summary confirmation
- Recommended workflow
- Unique angle recommendation
- SEO meta title and description
- Full outline with H2 descriptions and transition sentences
- Draft lead paragraph
- Internal link suggestions
- "What would be really interesting..." closing insight

### Running /review

After you have a draft saved to `/blog/drafts/zero-trust-explainer-draft.md`, run:

```
/review zero-trust-explainer
```

Claude will read the brief, prep, and draft, then deliver a review document to `/blog/drafts/zero-trust-explainer-edits.docx` containing:

- Editorial summary (2–3 sentences)
- Detailed review across 8 dimensions
- Weighted scoring rubric across 5 categories
- Full revised draft with suggested edits highlighted in yellow and comments in light blue

---

## File Structure

```
copychief/
├── CLAUDE.md                      # Claude's project instructions
├── .claude/
│   └── Commands/
│       ├── prep.md                # /prep slash command
│       └── review.md              # /review slash command
├── context/
│   ├── editorial-standards.md     # How to write
│   ├── seo-strategy.md            # What to optimize for
│   ├── personas.md                # Who we write for
│   ├── messaging-framework.md     # Brand positioning pillars
│   ├── brand-reference.md         # Visual identity + competitive intelligence
│   └── expert-voice.md            # Named author voice overlay
├── blog/
│   ├── briefs/                    # Assignment briefs (input)
│   ├── research/                  # Prep outputs
│   ├── drafts/                    # Working drafts and review outputs
│   └── published/                 # Final approved content
└── .gitignore
```

---

## Tips

- **Start with `editorial-standards.md` and `personas.md`** — these two files have the highest impact on output quality.
- **The review rubric is calibrated, not generous** — a 70–80 score means "solid draft, needs polish." Reserve 90+ for near-final copy.
- **Named author voice matters** — if you publish under a specific byline, invest time in `expert-voice.md`. The difference is noticeable.
- **Briefs are the foundation** — vague briefs produce vague output. The more specific your brief, the better the prep and review.
- **Use NotebookLM to perform a secondary review** — Create a detailed notebook about your targeted persona. Then, via NotebookLM directly or via Claude, ask how that persona would: react to that content, identify missing points and suggestion questions or areas of improvement that the persona would have.  

---

## License

MIT — use freely, adapt for your team, and contribute improvements back.
