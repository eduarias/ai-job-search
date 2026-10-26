// Cover letter template (Typst port of cover.cls).
// Compile from the repo root:
//   typst compile --font-path cover_letters/OpenFonts/fonts cover_letters/cover_<company>_<role>.typ

#let primary = rgb("#2b2b2b")
#let headings = rgb("#6A6A6A")
#let subheadings = rgb("#333333")

#let body-font = (font: "Raleway", weight: 500, size: 11pt)

// Page + base text setup. Wrap the whole letter: #show: cover
// `lang` sets hyphenation and quote rules: #show: cover.with(lang: "es") for a Spanish letter.
#let cover(body, lang: "en") = {
  set page(paper: "a4", margin: 2.3cm)
  set text(font: "Lato", weight: "light", fill: primary, size: 11pt, lang: lang)
  set par(leading: 0.65em, spacing: 1.2em, justify: false)
  set list(indent: 0.4em, body-indent: 0.6em, spacing: 0.6em)
  // Lists use the same Raleway body font as lettercontent, so a plain `- item` list
  // matches the letter without the bullets() helper.
  show list: set text(..body-font)
  body
}

// Name block. `first` renders hairline, `last` light; `contact` sits underneath.
// Pass "" as `first` to set the whole name in one light run: a separate empty run
// would add a stray space and push the name off-centre.
#let namesection(first, last, contact) = align(center)[
  #let name-run(weight, c) = text(font: "Lato", size: 40pt, weight: weight)[#c]
  #if first in ("", []) {
    name-run("light", last)
  } else {
    name-run("thin", first) + [ ] + name-run("light", last)
  }
  #v(2pt)
  #text(..body-font, fill: headings)[#contact]
  #v(10pt)
]

#let currentdate(d) = align(right, text(..body-font)[#d])

// Body paragraph / closing / signature all share the Raleway-Medium body font.
#let lettercontent(c) = [#text(..body-font)[#c] #parbreak()]

// Bullet list in the body font. Kept for explicitness and for use outside `#show: cover`;
// inside it a plain `- item` list gets the same font from the show rule above.
#let bullets(..items) = text(..body-font, list(..items.pos()))

#let closing(c) = align(right, text(..body-font)[#c])
#let signature(c) = align(right, text(..body-font)[#c])

// Optional building blocks, ported from the LaTeX class.
#let companyname(c) = text(font: "Lato", size: 12pt, weight: "bold", fill: subheadings)[#c]
#let companyaddress(c) = text(..body-font)[#c]
