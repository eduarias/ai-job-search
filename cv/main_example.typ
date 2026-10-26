// Example CV - [YOUR_NAME]
// Comprehensive overview of all competencies, experience, and achievements.
// Use as a master reference when tailoring role-specific CVs.
//
// SETUP: Run /setup to populate this with your actual information.
// Compile from the repo root: typst compile --font-path cover_letters/OpenFonts/fonts cv/main_example.typ

#let accent = rgb("#3973af") // moderncv "blue"

#set document(title: "[YOUR_NAME] - CV", author: "[YOUR_NAME]")
#set page(paper: "a4", margin: (x: 1.8cm, top: 1.6cm, bottom: 1.6cm))
#set text(font: ("Lato", "Liberation Sans", "DejaVu Sans"), size: 10.5pt, lang: "en")
#set par(leading: 0.6em, spacing: 0.7em, justify: false)
#set list(indent: 0.3em, body-indent: 0.5em, spacing: 0.45em)
#show link: set text(fill: blue)

// ---- helpers ------------------------------------------------------------

#let section(title) = {
  v(0.9em, weak: true)
  block(sticky: true, width: 100%)[
    #text(fill: accent, weight: "bold", size: 12pt)[#title]
    #v(-0.45em)
    #line(length: 100%, stroke: 0.6pt + accent)
  ]
}

// One job/education entry. Unbreakable, so a title can never be orphaned at the
// bottom of a page with its bullets on the next one.
#let cventry(dates, title, org, place, body) = block(breakable: false, width: 100%)[
  #grid(
    columns: (3.2cm, 1fr),
    column-gutter: 0.4cm,
    align(right, text(fill: accent, weight: "bold")[#dates]),
    [*#title*, #emph[#org], #place #v(0.15em) #body],
  )
  #v(0.5em)
]

// ---- personal data --------------------------------------------------------

#align(center)[
  #text(size: 28pt, weight: "bold", fill: accent)[\[First\] \[Last\]]
  #v(-0.3em)
  // If you have no address to list, DELETE the address item below.
  #text(size: 10pt)[
    [Your Address, City, Country] | [+XX XXXXXXXXXX] |
    #link("mailto:your.email@example.com")[your.email\@example.com] |
    #link("https://linkedin.com/in/your-profile")[LinkedIn],
    #link("https://github.com/your-username")[GitHub]
  ]
]

// ============================================================
//     PROFILE STATEMENT
// ============================================================

#v(6pt)
#text(size: 9.5pt)[\[Write a 3-5 line profile statement tailored to the role you're applying for. Focus on what makes you uniquely qualified. Example: "Data scientist with a PhD in \[field\] and X years of industry experience. Combines deep domain expertise in \[domain\] with strong applied machine learning and Python development skills. Experienced in developing end-to-end ML pipelines, from data ingestion to stakeholder-facing dashboards."\]]

// ============================================================
//     CORE COMPETENCIES
// ============================================================

#section[Core Competencies]

- *[Skill Category 1]*: [Specific skills, frameworks, tools. Be concrete.]
- *[Skill Category 2]*: [Specific skills, frameworks, tools.]
- *[Skill Category 3]*: [Specific skills, frameworks, tools.]
- *[Skill Category 4]*: [Domain expertise, methods, approaches.]
- *[Skill Category 5]*: [Tools, platforms, software.]

// ============================================================
//     PROFESSIONAL EXPERIENCE
// ============================================================

#section[Professional Experience]

// --- Most Recent Role ---
#cventry("[YYYY-Present]", "[Job Title]", "[Company]", "[City, Country]")[
  - [Achievement or responsibility 1 - be specific, use numbers where possible]
  - [Achievement or responsibility 2]
  - [Achievement or responsibility 3]
  - [Achievement or responsibility 4]
]

// --- Previous Role ---
#cventry("[YYYY-YYYY]", "[Job Title]", "[Company]", "[City, Country]")[
  - [Achievement or responsibility 1]
  - [Achievement or responsibility 2]
  - [Achievement or responsibility 3]
]

// --- Earlier Role ---
#cventry("[YYYY-YYYY]", "[Job Title]", "[Company]", "[City, Country]")[
  - [Achievement or responsibility 1]
  - [Achievement or responsibility 2]
]

// ============================================================
//     EDUCATION
// ============================================================

#section[Education]

#cventry("[YYYY-YYYY]", "[Degree] in [Field]", "[Institution]", "[City, Country]")[
  Thesis: "[Thesis Title]." [Brief description of research focus.]
]

#cventry("[YYYY-YYYY]", "[Degree] in [Field]", "[Institution]", "[City, Country]")[
  [Brief description or key topics.]
]

// ============================================================
//     LANGUAGES
// ============================================================

#section[Languages]

- [Language 1] (native), [Language 2] (fluent), [Language 3] (intermediate).

// ============================================================
//     PUBLICATIONS (optional)
// ============================================================

#section[Publications]

- [Author(s)] ([Year]). [Title]. [Journal/Conference]. #link("[DOI_URL]")[DOI link]

// ============================================================
//     HONORS AND AWARDS (optional)
// ============================================================

#section[Honors and Awards]

- *[Award Name]* -- [Event/Organization] ([Year]).

// ============================================================
//     REFERENCES
// ============================================================

#section[References]

- Available upon request.
