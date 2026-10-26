---
framework_version: 1.0.2
---

# Cover Letter Templates and Tailoring Guide

## Template: Typst (`cover.typ`)

Cover letters use a Typst template (`cover_letters/cover.typ`) with Lato/Raleway fonts.

**Output file:** `cover_letters/cover_<company>_<role>.typ`
**Compile with:** `typst compile` from the repo root, with the bundled fonts on the font path
**Font directory:** `cover_letters/OpenFonts/fonts/`
**Master reference:** `cover_letters/cover_example.typ`

### Compile command

```bash
typst compile --font-path cover_letters/OpenFonts/fonts cover_letters/cover_<company>_<role>.typ
```

The PDF lands next to the source. Confirm the page count with `python3 tools/verify_pdf.py cover_letters/cover_<company>_<role>.pdf --pages 1`; any count other than 1 is a failure that must be fixed before presenting to the user. A snap-installed Typst cannot write outside the home directory, so keep output inside the repo.

## Compile-and-Inspect Loop (MANDATORY)

After writing the cover letter and before presenting to the user, always compile and visually inspect the PDF. Iterate until the layout is clean:

1. Run the compile command above
2. Confirm page count is exactly 1 and compile succeeded
3. Read the PDF via the Read tool and visually check: signature fits at the bottom, no text cut off, bullet font matches body

### Bullet lists

Start every letter with `#show: cover`: it sets lists in the same Raleway-Medium body font as `lettercontent`, so a plain `- item` list and the `bullets(...)` helper (one content argument per bullet) look identical. Without `#show: cover` the list falls back to the default Lato font and visibly mismatches the letter.

## Document Structure

```typst
// Cover Letter - [Company], [Role]
#import "cover.typ": *
#show: cover

#namesection("", "[YOUR_NAME]",
  [#link("mailto:[YOUR_EMAIL]")[[YOUR_EMAIL]] | [YOUR_PHONE] | #link("[YOUR_LINKEDIN_URL]")[LinkedIn]])

#currentdate(datetime.today().display("[month repr:long] [day], [year]"))

#lettercontent[Dear [Name/Team],]

#lettercontent[[Opening paragraph - role, connection to background, 2-3 sentences]]

#lettercontent[[Body paragraph - most relevant experience, introducing the bullet list]]

#bullets(
  [[Concrete achievement/skill 1]],
  [[Concrete achievement/skill 2]],
  [[Concrete achievement/skill 3]],
)
#v(6pt)

#lettercontent[[Connection to company - why this role, why this company specifically]]

#lettercontent[[Personal fit paragraph - behavioral strengths, team contribution, 2-3 sentences]]

#lettercontent[I look forward to hearing from you.]

#align(right, block(breakable: false)[
  #closing[Kind regards,]
  #v(1.2em)
  #signature[[YOUR_NAME]]
])
```

The closing block is unbreakable so the signature can never be stranded on a second page.

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `#namesection(first, last, contact)` | Header with name and contact |
| `#currentdate(date)` | Date field (use `datetime.today().display(...)` or an explicit date) |
| `#lettercontent[text]` | Body paragraph (adds spacing after) |
| `#bullets(..items)` | Bullet list in the body font (a plain `- item` list matches too under `#show: cover`) |
| `#closing[text]` | Closing line |
| `#signature[name]` | Printed name below the closing |

## Tailoring Guidelines

### Salutation
- If you know the hiring manager's name: "Dear [First Last],"
- If you know the team: "Dear [Company] hiring team,"
- Generic: "Dear [Company]," (avoid "To whom it may concern")

### Length - Hard 1-Page Limit
- Target: 1 page including signature block
- Maximum: **never exceed 1 page**
- **Word budget: 250-300 words** of body text (not counting Typst markup). This is the safe maximum. 350 words will overflow.
- **Always count**: opening paragraph + bullet list paragraph + closing paragraph = 3 blocks. Add a 4th only if the others are short.
- When adding company-specific content, trim other content to compensate rather than adding net length

### Line Spacing
- Never shrink margins or leading to force a fit; trim text instead
- Use `#v(6pt)` between blocks only if space permits

### Bullet Lists
- Use a plain `- item` list or the `bullets(...)` helper; both match the body font under `#show: cover` (see "Bullet lists" above)
- 3-5 bullets is ideal
- Start each bullet with bold label or action verb
- Use `*Label:*` for category-style bullets
- A bullet or paragraph that begins with a literal `[` must be wrapped in its own content brackets, e.g. `[[text]]`; bare brackets in a content block must stay balanced

### Typst Special Characters
Typst markup treats a few characters specially. Escape them with a backslash wherever they appear in body text:
- `@` as `\@`: an unescaped `@` starts a reference, so `jane@example.com` fails to compile ("label does not exist"). Use `#link("mailto:...")[jane\@example.com]`
- `#` as `\#` ("ranked \#1", C\#): an unescaped `#` starts code
- `$` as `\$` (salary and cost figures): an unescaped `$` opens math mode, and an unclosed one fails the compile
- `*` and `_` as `\*` and `\_` when literal: they toggle bold and italic, and an unpaired one silently changes the rest of the paragraph
- `<` as `\<` before a name and `` ` `` as `` \` ``: they open labels and raw text
- `%` and `&` need no escaping in Typst (company names like Brüel & Kjær and "30%" are safe)
- `--` renders as an en-dash and `---` as an em-dash (the no-em-dash rule below still applies)

### Non-English Cover Letters
- Same template structure, just write content in the posting's language
- Set the language code: `#show: cover.with(lang: "es")` (hyphenation and quote rules follow it)
- Write the date as text in the local format instead of `datetime.today().display(...)`: Typst's date formatting always uses English month names
- Adjust closing to local convention (e.g. "Med venlig hilsen," for Danish)

## Checklist Before Finalizing
- [ ] No em-dashes (use commas or periods instead)
- [ ] No cliches or empty filler
- [ ] Every claim backed by specific example
- [ ] Forward-looking framing: focuses on tasks you'll solve, not just past duties
- [ ] Motivation section references this specific company's mission/values
- [ ] Company name and role are correct throughout
- [ ] Date is current
- [ ] Fits on one page (compiled, not estimated)
- [ ] Language matches the job posting language
- [ ] Salutation is appropriate (named person if possible)
- [ ] Headline is engaging and specific, not generic

## Submission Guidelines (Best Practice)
- Submit only the documents the employer requests
- Export as PDF to preserve formatting
- Name files clearly: "[Your Name] CV" and "[Your Name] Cover Letter"
- Follow all employer instructions regarding anonymity or specific materials
