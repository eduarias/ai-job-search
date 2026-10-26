"""Guards for the Typst authoring guidance and the example documents.

The silent-failure modes found by the 2026-08-19 review (F31, F34), ported
to Typst. Each one produces a clean compile and a green CI run while the
rendered document or its ATS extraction is wrong, so the spec files and the
example sources are the only place a test can catch them:

- F31: an unescaped special character in body text corrupts or breaks the
  document (`@` fails loudly, a paired `$` silently becomes math). The
  guidance must name the escapes.
- F34: `pdftotext` without `-enc UTF-8` emits Latin-1 on Xpdf builds,
  so a correct Danish CV fails the documented "no replacement
  characters" check and the agent is sent to "fix" a healthy document.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / ".claude" / "skills" / "job-application-assistant"
CV_TEMPLATES = SKILL_DIR / "05-cv-templates.md"
COVER_TEMPLATES = SKILL_DIR / "06-cover-letter-templates.md"
APPLY = REPO / ".claude" / "commands" / "apply.md"
EXAMPLE_CV = REPO / "cv" / "main_example.typ"
EXAMPLE_COVER = REPO / "cover_letters" / "cover_example.typ"

# The escapes both guidance files must document. `@` and `$` are the
# load-bearing ones: `@` breaks the compile, a paired `$` silently turns text
# into a formula.
REQUIRED_ESCAPES = ["\\@", "\\#", "\\$", "\\*", "\\_"]


def section(text, heading):
    """Return the body of a markdown section up to the next heading."""
    pattern = re.compile(
        rf"^#+ {re.escape(heading)}[^\n]*\n(.*?)(?=^#+ |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


class TestExampleDocumentsExist(unittest.TestCase):
    def test_example_sources_and_template_exist(self):
        for path in (EXAMPLE_CV, EXAMPLE_COVER, REPO / "cover_letters" / "cover.typ"):
            self.assertTrue(path.is_file(), f"{path} must exist")

    def test_example_cv_entries_break_but_keep_the_title_with_its_bullets(self):
        text = EXAMPLE_CV.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"#let cventry\([^)]*\)\s*=\s*block\(breakable: true",
            "cventry must be breakable so a long entry cannot leave a page-sized hole",
        )
        self.assertIn(
            "block(sticky: true)[*#title*",
            text,
            "the title block must be sticky so a title is never orphaned from its bullets",
        )

    def test_example_cover_letter_uses_the_bullets_helper(self):
        text = EXAMPLE_COVER.read_text(encoding="utf-8")
        self.assertIn("#bullets(", text)
        self.assertNotRegex(text, r"(?m)^- ", "bare lists lose the Raleway body font")


class TestSpecialCharacterGuidance(unittest.TestCase):
    """F31: both template guides must document the Typst escapes."""

    def assert_escapes_documented(self, path):
        body = section(path.read_text(encoding="utf-8"), "Typst Special Characters")
        if body is None:
            body = section(
                path.read_text(encoding="utf-8"), "Typst Special Characters (important)"
            )
        self.assertIsNotNone(
            body, f"{path.name} has no 'Typst Special Characters' section"
        )
        missing = [esc for esc in REQUIRED_ESCAPES if esc not in body]
        self.assertEqual(
            missing,
            [],
            f"{path.name}'s special-characters section is missing: {missing}",
        )

    def test_cv_guide_documents_the_escapes(self):
        self.assert_escapes_documented(CV_TEMPLATES)

    def test_cover_letter_guide_documents_the_escapes(self):
        self.assert_escapes_documented(COVER_TEMPLATES)

    def test_cv_guide_warns_that_paired_dollars_fail_silently(self):
        body = section(
            CV_TEMPLATES.read_text(encoding="utf-8"), "Typst Special Characters (important)"
        )
        self.assertIsNotNone(body)
        self.assertRegex(
            body,
            re.compile(r"silent", re.IGNORECASE),
            "the paired-$ failure mode must be called out as silent - it "
            "compiles cleanly while the text between the dollars becomes math",
        )


class TestAtsExtractionEncoding(unittest.TestCase):
    """F34: every documented extraction command must pin the encoding."""

    def assert_pdftotext_commands_pin_utf8(self, path):
        offending = [
            f"{path.name}:{lineno}: {line.strip()}"
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            if "pdftotext" in line and "-layout" in line and "-enc UTF-8" not in line
        ]
        self.assertEqual(
            offending,
            [],
            "pdftotext without -enc UTF-8 emits Latin-1 on Xpdf builds, so "
            "the ATS check reports phantom replacement characters on any "
            "non-ASCII CV; add -enc UTF-8:\n" + "\n".join(offending),
        )

    def test_apply_extraction_command_pins_utf8(self):
        self.assert_pdftotext_commands_pin_utf8(APPLY)

    def test_cv_guide_extraction_command_pins_utf8(self):
        self.assert_pdftotext_commands_pin_utf8(CV_TEMPLATES)


class TestNoStaleLatexGuidance(unittest.TestCase):
    """The stock workflow is Typst; LaTeX engines must not be documented as the default."""

    def test_stock_compile_guidance_does_not_name_a_latex_engine(self):
        for path in (CV_TEMPLATES, COVER_TEMPLATES):
            text = path.read_text(encoding="utf-8")
            for engine in ("lualatex", "xelatex", "pdflatex"):
                self.assertNotIn(engine, text, f"{path.name} still mentions {engine}")

    def test_apply_stock_defaults_use_typst(self):
        text = APPLY.read_text(encoding="utf-8")
        self.assertIn("typst compile --font-path cover_letters/OpenFonts/fonts cv/main_<company>_<role>.typ", text)


if __name__ == "__main__":
    unittest.main()
