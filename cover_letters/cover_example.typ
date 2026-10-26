// Cover Letter - [Company], [Role]
//
// Example cover letter with placeholder content. This is the structural
// reference for /apply (see 06-cover-letter-templates.md) and the CI smoke
// test for cover.typ: it must always compile to exactly 1 page.
// Compile from the repo root:
//   typst compile --font-path cover_letters/OpenFonts/fonts cover_letters/cover_example.typ

#import "cover.typ": *
#show: cover

#namesection("", "[YOUR NAME]",
  [#link("mailto:your.email@example.com")[your.email\@example.com] | [+XX XXXXXXXXXX] | #link("https://www.linkedin.com/in/yourprofile")[LinkedIn]])

#currentdate(datetime.today().display("[month repr:long] [day], [year]"))

#lettercontent[Dear [Hiring Manager / Team],]

#lettercontent[[Opening paragraph: name the role and where you found it, state your strongest connection to it in one sentence, and preview why you are a fit. Keep it to 2--3 sentences.]]

#lettercontent[[Body paragraph: your most relevant experience, framed toward the tasks in the posting. Follow with 3--5 concrete bullets:]]

#bullets(
  [*[Achievement 1]:* [concrete result with a number where possible]],
  [*[Achievement 2]:* [skill or project mapped to a posting requirement]],
  [*[Achievement 3]:* [evidence for a nice-to-have requirement]],
)
#v(6pt)

#lettercontent[[Connection paragraph: why this company specifically. Reference a verified specific: a product, a stated priority, a team. Never generic.]]

#lettercontent[[Personal fit paragraph: behavioral strengths and what you bring to the team, 2--3 sentences.]]

#lettercontent[I look forward to hearing from you.]

#align(right, block(breakable: false)[
  #closing[Kind regards,]
  #v(1.2em)
  #signature[[YOUR NAME]]
])
