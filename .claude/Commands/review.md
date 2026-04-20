# This document provides instructions when asked to review a document

## Tasks

1. Read these files:
   - Brief: blog/briefs/$ARGUMENTS.md
   - Prep: blog/research/$ARGUMENTS-prep.md
   - Draft: blog/drafts/$ARGUMENTS-draft.md

2. Generate an editorial summary assessment (2–3 sentences).

3. Perform a detailed review across these dimensions:
   - Alignment with the brief. Does it deliver on everything the brief asked for? Flag anything missing.
   - Structure: Is the post scannable? Are H2s descriptive and parallel? Is any section too long without a break?
   - Grammar and mechanics
   - Clarity and flow
   - Brand voice adherence
   - Persona resonance — does it speak to the target buyer persona effectively?
   - Use the ai-seo skill to evaluate SEO / AEO / GEO and flag gaps or improvements
   - Claims that need substantiation or should be softened
   - Any missed opportunities from the original outline
   - Internal links: Are there at least 2 links to resource links from corporate content?

4. Execute Content Review Scoring Rubric

### Scoring Overview

Evaluate the draft against five categories. Each category is scored 0–100%. The Overall Score is a weighted average.

| Category | Weight | Reference Document |
|---|---|---|
| Assignment Alignment | 30% | Assignment brief |
| Brand Voice Alignment | 17.5% | Brand voice guide |
| Author Voice Alignment | 17.5% | Author writing samples |
| Persona Alignment | 17.5% | Target persona profile |
| SEO/AEO/GEO Alignment | 17.5% | SEO/search strategy brief |

**Overall Score** = (Assignment × 0.30) + (Brand × 0.175) + (Author × 0.175) + (Persona × 0.175) + (SEO × 0.175)

### Score Legend

| Range | Rating | Meaning |
|---|---|---|
| 90–100% | Publish-Ready | Minimal edits needed. Meets or exceeds brief requirements. |
| 70–89% | Solid Draft | Fundamentally sound but needs targeted revisions. |
| 50–69% | Needs Rework | Significant gaps or misfires requiring substantial revision. |
| Below 50% | Off-Target | Does not meet the brief. Recommend restart or major restructure. |

### Category 1: Assignment Alignment (30%)

Score this category by evaluating both coverage (quantitative) and execution (qualitative).

**Coverage Checks (50% of category)**
For each point listed in the assignment brief, answer:
- Was this point addressed in the draft? (Yes/No)
- If yes, was it given appropriate depth relative to its importance?

Coverage Score = (points adequately addressed ÷ total points assigned) × 100, adjusted downward if depth is insufficient on key points.

**Execution Checks (50% of category)**
- Relevance: Does all content serve the assignment's purpose, or is there filler/off-topic material?
- Effectiveness: Does the piece achieve what the assignment intended (inform, persuade, guide, etc.)?
- Structure: Is the content organized in a way that delivers the assignment's objectives logically?
- Completeness: Does the piece feel finished and appropriately scoped, or does it feel thin/bloated?

Category Score = (Coverage Score × 0.5) + (Execution Score × 0.5)

### Category 2: Brand Voice Alignment (17.5%)

Compare the draft against the brand voice guide. Evaluate:
- Tone match: Does the draft's tone (formal/casual, authoritative/conversational, etc.) match brand guidelines?
- Language & terminology: Does it use brand-preferred terms, phrasing patterns, and vocabulary level?
- Values alignment: Does the content reflect the brand's stated values, positions, and perspective?
- Consistency: Is the brand voice sustained throughout, or does it drift between sections?

### Category 3: Author Voice Alignment (17.5%)

Compare the draft against the author's writing samples. Evaluate:
- Stylistic fingerprint: Does the draft read like the author could have written it (sentence rhythm, complexity, personality)?
- Perspective & authority: Does it reflect how the author typically frames ideas and establishes credibility?
- Natural expression: Does the language feel organic to the author, or forced/generic?
- Signature patterns: Are the author's characteristic habits present (e.g., use of anecdotes, directness, humor, rhetorical questions)?

### Category 4: Persona Alignment (17.5%)

Compare the draft against the target persona profile. Evaluate:
- Audience awareness: Is the content written for the target persona's knowledge level, concerns, and interests?
- Pain points & motivations: Does it speak to the persona's specific challenges and goals?
- Language accessibility: Is vocabulary and complexity calibrated to the persona (not too technical, not too simplistic)?
- Engagement fit: Would this persona find the content relevant, valuable, and worth their time?

### Category 5: SEO/AEO/GEO Alignment (17.5%)

Compare the draft against the SEO/search strategy brief. Evaluate:
- Keyword integration: Are target keywords and semantic variants present naturally (not stuffed)?
- Search intent match: Does the content satisfy the likely intent behind the target queries?
- Structure for discoverability: Are headings, subheadings, and content blocks formatted for search engine and AI answer extraction?
- Authority signals: Does the content demonstrate expertise, cite/reference credible framing, and provide substantive answers to likely questions?

### Output Format for Each Category

For each of the five categories, produce:

```
### [Category Name]: [Score]%
[2–3 sentence summary explaining the score.]

**Worked well:**
- [Specific strength with brief example from the draft]
- [Specific strength with brief example from the draft]

**Improvement focus:**
- [Specific, actionable recommendation]
- [Specific, actionable recommendation]
```

### Output Format for Overall Score

After all five categories, produce:

```
## Overall Score: [Weighted Score]%
**Rating: [Publish-Ready / Solid Draft / Needs Rework / Off-Target]**
[2–3 sentence summary of overall quality, noting the strongest and weakest categories.]
```

### Scoring Discipline

- Score against the reference documents, not general best practices. If the draft contradicts a reference document, that is a deduction even if the draft's approach is otherwise reasonable.
- Be specific. Cite passages or sections from the draft when noting strengths or weaknesses.
- Calibrate honestly. A competent first draft that hits most points but lacks polish is a 70–80, not a 90+. Reserve 90+ for work that genuinely needs only light touch-ups.
- The coverage check in Assignment Alignment is binary first (was it addressed?), then qualitative (how well?). Do not give full marks for mentioning a point superficially.

---

5. Generate a Word document (.docx) and an HTML document (.html) showing the full revised draft with all suggested edits highlighted in yellow. Comments and reasoning within the document should be highlighted in light blue. After the suggested revisions, include a bullet list of specific reasonings for each suggestion, with a citation to the relevant point in the article. Export the Word document to blog/drafts/$ARGUMENTS-edits.docx and the .html document to blog/drafts/$ARGUMENTS-edits.html.
