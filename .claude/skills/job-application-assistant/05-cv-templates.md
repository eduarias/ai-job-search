---
framework_version: 1.4.8
---

# CV Templates and Tailoring Guide

<!-- SETUP: Profile statements and section ordering are personalized by running /setup -->

## Template: Typst (Banking-Style Layout)

All CVs use a single Typst file with a blue accent colour, a centred name block, ruled section headings and a dates-left entry grid.

**Output file:** `cv/main_<company>_<role>.typ`
**Compile with:** `typst compile` from the repo root with the bundled fonts on the font path (a single binary; no TeX distribution needed). Without `--font-path` the CV silently falls back to a different font on machines without Lato, which changes line breaks and the page count.
**Master reference:** `cv/main_example.typ` (comprehensive CV with all competencies, experience, and achievements - use as source when building targeted CVs)

### Compile command

```bash
typst compile --font-path cover_letters/OpenFonts/fonts cv/main_<company>_<role>.typ
```

The PDF lands next to the source. Verify the page count with `python3 tools/verify_pdf.py cv/main_<company>_<role>.pdf --pages 2`; any count other than 2 is a failure that must be fixed before presenting to the user. A snap-installed Typst cannot write outside the home directory, so keep output inside the repo.

## Document Structure

Copy `cv/main_example.typ` and edit it. Its shape:

```typst
#let accent = rgb("#3973af")
#let lang = "en"   // CV language code: hyphenation and quote rules
#set document(title: "[YOUR_NAME] - CV", author: "[YOUR_NAME]")
#set page(paper: "a4", margin: (x: 1.8cm, top: 1.6cm, bottom: 1.6cm))
#set text(font: ("Lato", "Liberation Sans", "DejaVu Sans"), size: 10.5pt, lang: lang)

#let section(title) = ...   // accent-coloured heading with a rule, sticky to the next block
#let cventry(dates, title, org, place, body) = block(breakable: true, ...)    // dates-left grid; the title block is sticky

// Personal data
#align(center)[
  #text(size: 28pt, weight: "bold", fill: accent)[[FIRST_NAME] [LAST_NAME]]
  [YOUR_ADDRESS] | [YOUR_PHONE] | #link("mailto:[YOUR_EMAIL]")[[YOUR_EMAIL]] |
  #link("[YOUR_LINKEDIN_URL]")[LinkedIn], #link("[YOUR_GITHUB_URL]")[GitHub]
]

// 1. Profile statement (1-3 sentences, tailored per role)
// 2. Skills section
// 3. Education section
// 4. Professional Experience section
// 5. Selected Publications (if applicable)
// 6. Honors and Awards (if applicable)
// 7. References
```

Entries are written `#cventry("YYYY-YYYY", "Role Title", "Organization", "Location")[ - bullet ... ]`. If you have no address to list, delete the address item and its `|` separator.

### Section headings must match the CV's language (important)

Section headings such as `#section[Core Competencies]`, `Professional Experience`, `Education`, `Languages`, `Publications`, `Honors and Awards`, `References` (and any others your template defines), plus the `Available upon request.` line under References, are all **literal English text baked into the template** - they do not translate themselves. Whenever the CV language (see `CV language` in the candidate profile) is not English, translate every one of these too, whatever they are, not just the body prose - a CV with a fully localized profile statement and bullets sitting under untouched English section headers reads as sloppy and inconsistent, and it's an easy thing to forget precisely because the prose translation is the obvious, visible part of the job. Worked example for Spanish: `Competencias Clave`, `Experiencia Profesional`, `Educación`, `Idiomas`, `Publicaciones`, `Distinciones y Premios`, `Referencias`, `Disponibles a solicitud.` Also change `#let lang = "en"` at the top of the file to the CV language code (e.g. `"es"`), so hyphenation and quote rules match. The same rule applies for any other target language - check this explicitly during the verification pass.

## Section-by-Section Tailoring

### Profile Statement / Elevator Pitch (Best Practice)
This is the most important section to customize. It appears right after the name and contact block.

Write 5-7 lines that function as an "elevator pitch": a concise, compelling introduction explaining why you're qualified for *this specific role*. Focus on what the employer gains from hiring you.

When the role sits outside your home domain, **lead with the domain-transfer argument** - the one or two sentences connecting your background to their problem (e.g. wave physics to radar signal processing) belong in the profile statement's opening, not buried in the cover letter. It is the strongest card a domain-changer holds; play it first.

**Create 2-3 profile statement templates for your main role types:**

<!-- SETUP: These are populated based on your background -->
**For [YOUR_PRIMARY_ROLE_TYPE] roles:**
> [YOUR_PROFILE_STATEMENT_TEMPLATE_1]

**For [YOUR_SECONDARY_ROLE_TYPE] roles:**
> [YOUR_PROFILE_STATEMENT_TEMPLATE_2]

Statements labeled *[Used for: <company>_<role>]* were extracted from archived application drafts by `/setup` Path A. They are **phrasing references, never fact sources**: when drafting from one, every factual claim still comes from `01-candidate-profile.md` - a past tailored draft does not vouch for its own accuracy.

### Core Competencies / Skills Section (Best Practice)
Reorder and emphasize based on the role. Use bold category labels.

List **5-7 key competencies** in bullet format, tailored to the specific job. For each competency, briefly explain how it adds value to the position.

Use the posting's own core term in the matching bullet's bold label when it truthfully applies - ATS and skim-reading hiring managers match literally, and "MLOps" in a heading outperforms a paraphrase like "ML Deployment".

### Education
- Always include your highest degrees
- For senior roles, keep education brief (dates and titles only)
- Include thesis topics when relevant to the target role

#### In-progress qualifications must say so explicitly

**A bare year range is not enough.** An entry reading `2025–2026`, seen partway through 2026, looks like a *finished* degree, because a reader skimming a CV treats a closed range as closed. A profile statement that says "currently completing…" does not fix it: the education entry is where a reader checks the credential, so it has to stand on its own.

State completion inside the entry itself:

```typst
#cventry("2025-2026", "[Degree], [Field]", "[Institution]", "[Location]")[
  In progress, expected [Month Year]. [Relevant topics]
]
```

Any consistent form works: `In progress, expected <Month Year>.` / `Expected completion <Month Year>.` / a date field of `2025-present`.

Claiming a credential not yet held is a factual misstatement, and it is the kind discovered at transcript or reference check rather than at interview. It costs nothing to prevent. The same applies to in-progress certifications and courses.

**Check for agreement:** for a current student, the profile statement, the education entry, and any availability or work-permit note must all give the same completion date. Contradiction between them is worse than any single version.

### Professional Experience
- Rewrite bullet points to emphasize aspects most relevant to the target role
- Use 4-6 bullets for most recent role, 3-4 for previous, 2-3 for older
- **Emphasize measurable results** where possible: "Reduced processing time by X%", "Model adopted by the team"

#### Check tenure against visible output

Before finalizing, look at each role the way a stranger will: **date span versus how much work is shown.** A two-year role represented by a single project reads as low output, whether or not that is fair. The reader cannot know what filled the time, so they guess, and the guess is unflattering.

This bites hardest on **career changers** (part of the tenure went into learning the new field), on **long-cycle work** (industrial deployment, clinical or regulatory projects, research — one delivery genuinely takes quarters), and on anyone whose employer kept them on a single account or product.

Three honest fixes, in order of preference:

1. **Surface more real work.** Ask what else the period contained. There are often real secondary projects, internal tooling, or support work that never reached the CV because it felt minor. Best fix when the material exists.
2. **Make the phases within the role explicit.** If the span genuinely had stages, say so — an initial period learning the domain or supporting the team, then ownership of the named work through to delivery. A phased arc reads as a growth curve; an undifferentiated multi-year block reads as stagnation.
3. **Name what made the cycle long.** Data collection from a live environment, validation with domain experts, deployment and iteration against real output. Reviewers who know the domain accept this immediately.

**Never** pad with invented projects, and **never** quietly shorten the employment dates so the ratio looks better. Both are discoverable, and both are worse than the perception problem being solved.

**Prepare the interview answer too.** If a long span against little visible output survives these fixes, the question is coming. The candidate needs a ready two-part answer — what actually filled the time, and what the outcome was — recorded in their interview prep rather than improvised in the room.

### Handling Employment Gaps (Best Practice)
If there is a gap in your employment history:
- The gap should be explained matter-of-factly if needed
- Describe how professional development continued during the gap
- Frame as deliberate skill-building and career repositioning

### Publications
- Include Google Scholar link if applicable
- Select 3-4 most relevant publications (not always all of them)
- For non-academic roles, keep brief

### Evidence Links
Wherever the CV names a verifiable artifact - a public project, a hackathon entry, a publication - carry its link (`#link("url")[text]`) so a reader can verify the claim in one click. A CV whose strongest claims are checkable reads as more credible everywhere else too.

### Honors and Awards
- Keep format brief, one line each

### References
- List 2-4 references with name, title, company, and contact
- End with: "More references are available upon request."
- **Do not attach reference letters** - employers typically contact references directly

### Typst Special Characters (important)

Postings and profile data arrive as plain text; the CV is Typst markup. Escape these with a backslash wherever they land in body text - company names, achievement bullets, skill lists:

| Character | Write | Typical trigger |
|---|---|---|
| `@` | `\@` | email addresses: `jane\@example.com` |
| `#` | `\#` | "ranked \#1", C\# |
| `$` | `\$` | salary and cost figures |
| `*` | `\*` | literal asterisks (a lone `*` toggles bold) |
| `_` | `\_` | file names, code identifiers (a lone `_` toggles italics) |
| `<` | `\<` | text like `<20ms` (opens a label) |
| `` ` `` | `` \` `` | stray backticks (opens raw text) |

`%` and `&` need **no** escaping in Typst, so "cut latency by 40%" and "Bang & Olufsen" are safe as written. Failure modes to watch:

- **`@` fails loudly**: an unescaped `@` starts a reference, and the compile stops with "label ... does not exist in the document". Inside `#link("mailto:...")` the string is code, so no escape is needed there; the visible link text does need `\@`.
- **`$` opens math mode.** An unclosed one is a compile error, but a *paired* `$` (two salary figures in one bullet) compiles and silently turns the text between them into a formula. Escape every `$`.
- **Unbalanced `[` / `]` in content.** Square brackets delimit content blocks, so a stray `]` ends the block early. The stock placeholders are written as `[text]` inside a content block, which is balanced and safe. When a bullet should *begin* with a literal bracket, keep the pair balanced or escape it (`\[`).
- **`--` and `---`** render as en-dash and em-dash. See the ASCII date rule below for date fields.

## Compile-and-Inspect Loop (MANDATORY)

After writing the CV and before presenting to the user, always compile and visually inspect the PDF. Iterate until the layout is clean. Workflow:

1. Run `typst compile --font-path cover_letters/OpenFonts/fonts cv/main_<company>_<role>.typ`
2. Check the page count: must be exactly 2 (`python3 tools/verify_pdf.py <pdf> --pages 2`)
3. Read the PDF via the Read tool and visually inspect both pages
4. Check for **orphaned entries**: a job/education title line must never sit alone at the bottom of page 1 with its bullets on page 2

### Fixing common page-break problems

**Problem: entry title on page 1, bullets orphaned to page 2**
The stock `cventry` helper is breakable: a long entry fills the page it starts on and continues on the next, and its title block is `sticky`, so the title always keeps at least its first bullets with it. That avoids both the orphaned title and the large hole an unbreakable entry leaves at the bottom of a page. A hand-written entry that bypasses `cventry` has no such protection: use the helper, or wrap the entry in `#block(sticky: true)` for its title line. To keep a short entry whole, wrap it in `#block(breakable: false)[ ... ]`; the cost is a hole at the bottom of the previous page, which `tools/verify_layout.py` reports, and the fix for a hole is to shorten the entry that follows it.

**Problem: a section heading stranded at the bottom of a page**
The `section` helper is a `sticky` block, which keeps it with the content after it. Keep that property in any custom heading.

**Problem: one trailing section spills to page 3 (e.g., References alone on page 3)**
Trim one line from page 2, or tighten a single block with `#v(-3pt)`. Do not change the page margins or text size to force a fit.

**Problem: 3 pages with significant content on page 3**
Cut content - do not compress margins or spacing. See "Relevance-weighted cutting" below for the rule.

**Problem: content finishes early on page 2 (feels thin)**
Restore the highest-relevance item that was previously cut - a CV that ends mid-page 2 looks incomplete.

## ATS Parseability

Most employers run CVs through an ATS before a human sees them, and the ATS reads the PDF's embedded **text layer**, not the rendered page. A CV can pass visual inspection and still extract as garbage. After the layout passes the compile-and-inspect loop, verify the text layer:

> **Windows:** run these tools as `python`, not `python3`. A python.org install ships no `python3`, so that name reaches the Microsoft Store alias, which either exits 49 with no output (#669) or starts a separate Store Python without the packages `pip` installed (such as pypdf). `.claude/settings.json` allows both spellings.

```bash
python3 tools/verify_pdf.py cv/main_<company>_<role>.pdf --dump-text cv/main_<company>_<role>.txt
```

Extraction tries **pypdf** first (`pip install pypdf`, BSD license), then Poppler `pdftotext`. If a fallback still uses `pdftotext -layout`, it must also pass `-enc UTF-8`: Xpdf-based builds default to Latin-1, which makes every non-ASCII character in a perfectly good CV read back as a replacement character. If neither extractor is available, skip the mechanical check with a warning and rely on the visual PDF read for keyword coverage.

What to check in the extraction:

- **Contact details as literal text.** The stock template prints the address, phone and email as plain text. The failure mode is a contact detail carried *only* by an icon or a hyperlink (like the `LinkedIn` link text, whose URL is not in the text layer): invisible to an ATS. The email address must always appear as printed text.
- **No garbled output.** `(cid:NNN)` markers or `�` characters mean a font is embedded without a Unicode mapping - an ATS sees the same garbage. This shows up with unusual fonts in custom templates, not with the stock Typst template.
- **Reading order.** The stock layout is single-column, so extraction order matches visual order. Custom templates (via `/add-template`) with sidebars or multi-column layouts can interleave unrelated lines; if extraction order is scrambled, the user is trading ATS compatibility for looks and should be told.
- **Keyword coverage.** Match the posting's required/preferred terms against the extracted text, in the posting's language. Prefer the posting's exact term over a synonym when it is truthfully applicable - ATS matching is often literal. Never add a keyword the profile does not support. `verify_pdf.py --contains` folds both sides for whitespace, Unicode normalization (NFC) and typographic substitutions before comparing - Typst's smart quotes put `'` in the text layer as U+2019 and `--` as U+2013, so `--contains "Master's degree"` and `--contains "2016-2024"` match what the template actually renders. The dumped `.txt` is never folded: it is the raw layer the ATS sees, which is why the date-range check below reads the dump, not `--contains`.
- **Accents intact.** Typst writes accented letters as single precomposed characters, so `Genève` extracts and matches normally; check non-Latin names and unusual diacritics in the dump all the same.

### Date fields must be ASCII ranges (confirmed ATS import failure)

This one is worth knowing about because it fails **silently**. A CV that passes every other check in this section - clean extraction, no `(cid:)` markers, contact details intact, correct reading order - can still have its dates dropped on import. In a real Workday resume import, a CV built from this template lost the end date of a short contract role and failed to import **any** education entry at all, forcing manual re-entry. Nothing about the PDF or its text layer looked wrong.

Two independent causes, both easy to avoid:

1. **`--` in a date renders as an en-dash (U+2013), not a hyphen.** Typst converts `--` (two ASCII hyphens, U+002D) into a single en-dash glyph, so `2016--2024` reaches the PDF text layer as `2016<U+2013>2024`. Many parsers split date ranges only on an ASCII hyphen and see no range at all. Write the date argument with a **single hyphen**:

   ```typst
   #cventry("2016-2024", "Role Title", "Organization", "Location")[...]    // parses
   #cventry("2016--2024", "Role Title", "Organization", "Location")[...]   // en-dash, may not
   ```

   This applies to the **date argument only**. Keep `--` everywhere it is typographically correct in prose, for example a numeric range like `EUR 600k--1M`.

2. **A bare single year gives the parser no end date.** A short contract, mandate or internship written as `#cventry("2016", ...)` imports as a start date with nothing to close it. Use an explicit range, with months where the role ran under a year:

   ```typst
   #cventry("Mar 2016 - Jul 2016", "Contract Role", "Client", "Location")[...]
   ```

   Where a genuine range exists, use it even when a single year would be factually accurate - a degree written `1995` is true but imports worse than `1992-1995`. Do not invent a start date you do not have; a lone graduation year is fine, just expect it to be typed in by hand.

**Cause 1 is mechanical in step 5d**: `python3 tools/verify_pdf.py cv/main_<company>_<role>.pdf --ascii-dates` scans the raw text layer for a year joined to a Unicode dash and exits 1 naming each hit with its code point (`U+2013 in 'Role Title 2016–2024'`). It deliberately reads the raw layer: the fold that lets `--contains "2016-2024"` match what the template renders maps that same en-dash back to `-`, so `--contains` can never see this. A year on either side of the dash is enough, so `Mar 2016 – Jul 2016` and `2016 – Present` are caught too; a numeric range with no year (`EUR 600k–1M`) is left alone. **Cause 2 stays a read-through check**: after extracting the text layer, confirm every experience entry shows a start *and* an end. Because both failures are silent and invisible in the PDF, the candidate otherwise discovers them only while filling in the application form.

## Page Budget - Hard 2-Page Limit

The CV **must** fit on exactly 2 pages when compiled. Use these content limits as a guide:

| Section | Max budget |
|---------|-----------|
| Profile statement | 3-4 lines |
| Skills | 5 items, each 1-2 lines |
| Most recent role | 4-5 bullets |
| Previous role | 2-3 bullets |
| Older roles | 2 bullets (1 line each) |
| Education | 2-3 entries |
| Publications | 2-3 entries |
| Awards | 3 entries, single line each |
| References | "Available upon request." (single line) |

**If in doubt, cut rather than squeeze.** Reducing spacing or page margins to force-fit content makes the CV look cramped.

## Relevance-weighted cutting (the right way to shrink a CV)

**Cut by signal, not by section.** Static priority lists ("remove oldest education first, then shorten the earliest role...") are wrong when a relevant "lower-priority" item is competing with an irrelevant "higher-priority" item. An older-role bullet that speaks directly to the posting is worth more than a recent-role bullet that does not.

For every candidate line, score three things:

1. **Relevance to THIS posting** — does the line hit a named tool, keyword, or stated responsibility in the job ad?
2. **Uniqueness** — is it the only place this claim appears, or is it duplicated elsewhere in the CV?
3. **Narrative load** — does the cover letter depend on it? If cutting the line would force you to rewrite a cover-letter paragraph, it is load-bearing.

Cut the lowest-total-score line first, regardless of which section it sits in.

### Practical order of cuts (easiest → last resort)

1. **Redundancy.** If an achievement appears in both Core Competencies AND a role bullet, the Core Competencies version is usually the cleaner cut (the experience bullet is more concrete evidence).
2. **Profile-statement fluff.** A sentence that just restates what Publications or Skills will show. ("Peer-reviewed publications on X..." is already a Publications entry — profile can claim it once and stop.)
3. **Low-relevance experience bullets.** A bullet about work that does not touch posting keywords, wherever it sits. This cuts across sections before touching the structural list.
4. **Low-relevance supporting content.** An older-role bullet that does not speak to the target role. A certification that does not touch the posting's stack. A language entry that can be condensed to one line.
5. **Low-relevance publications.** Keep 1-2 publications that best match the posting. Cut the rest before touching experience bullets.
6. **Last-resort structural cuts.** Oldest education entry, tightening an older role to 2 bullets, collapsing Certifications into a single line. These only happen if the relevance-weighted cuts above have already been exhausted.

### Pitfalls to avoid

- Do not mechanically cut from the bottom of a static section list without checking relevance. "Cut the oldest role first" is wrong if that role is literally about the skill the posting asks for.
- Do not cut the one concrete example the cover letter leans on. Relevance is measured against the cover letter you wrote, not just the job posting — interviewers will have read both.
- Do not cut to fit if the fit is borderline (2.02 pages). Prefer trimming a single line for near-misses; reserve content cuts for genuine overflow (content on page 3 that is more than a single trailing section).

## Recommended Section Order

The section order varies by role type:

**For technical / data science / ML roles:**
1. Profile statement / elevator pitch
2. Core competencies / Skills
3. Professional Experience (reverse chronological)
4. Education (reverse chronological)
5. Languages
6. Publications & Awards
7. References

**For domain-specific / specialist roles:**
1. Profile statement / elevator pitch
2. Core competencies / Skills
3. Education (reverse chronological) - credentials are a key qualifier
4. Professional Experience (reverse chronological)
5. Publications & Awards
6. References
