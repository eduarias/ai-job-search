// Cover letter template (Typst port of cover.cls).
// Compile from the repo root:
//   typst compile --font-path cover_letters/OpenFonts/fonts cover_letters/cover_<company>_<role>.typ

#let primary = rgb("#2b2b2b")
#let headings = rgb("#6A6A6A")
#let subheadings = rgb("#333333")

#let body-font = (font: "Raleway", weight: 500, size: 11pt)

// Page + base text setup. Wrap the whole letter: #show: cover
#let cover(body) = {
  set page(paper: "a4", margin: 2.3cm)
  set text(font: "Lato", weight: "light", fill: primary, size: 11pt, lang: "en")
  set par(leading: 0.65em, spacing: 1.2em, justify: false)
  set list(indent: 0.4em, body-indent: 0.6em, spacing: 0.6em)
  body
}

// Name block. `first` renders hairline, `last` light; `contact` sits underneath.
#let namesection(first, last, contact) = align(center)[
  #text(font: "Lato", size: 40pt, weight: "thin")[#first]
  #text(font: "Lato", size: 40pt, weight: "light")[#last]
  #v(2pt)
  #text(..body-font, fill: headings)[#contact]
  #v(10pt)
]

#let currentdate(d) = align(right, text(..body-font)[#d])

// Body paragraph / closing / signature all share the Raleway-Medium body font.
#let lettercontent(c) = [#text(..body-font)[#c] #parbreak()]

// Bullet list in the body font (matches lettercontent).
#let bullets(..items) = text(..body-font, list(..items.pos()))

#let closing(c) = align(right, text(..body-font)[#c])
#let signature(c) = align(right, text(..body-font)[#c])

// Optional building blocks, ported from the LaTeX class.
#let companyname(c) = text(font: "Lato", size: 12pt, weight: "bold", fill: subheadings)[#c]
#let companyaddress(c) = text(..body-font)[#c]
