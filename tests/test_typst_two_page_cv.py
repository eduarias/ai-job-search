"""The stock Typst CV must hold the two-page format on realistic content.

The shipped `cv/main_example.typ` is a short placeholder (one page), so CI's
example assertion cannot see a regression in the real two-page layout: a margin
or font change that pushes a full CV to three pages, or breaks an entry across
the page boundary, would pass. This test fills the template with realistic roles (see SHAPES), compiles it, and asserts exactly two
pages and a clean `tools/verify_layout.py` report.

It needs `typst` and Poppler's `pdftotext`/`pdfinfo`, so it skips where they are
absent; the `typst-smoke` CI job installs both and runs it. Output goes inside
the repo because a snap-installed Typst cannot write outside the home directory.
"""
import io
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.verify_layout import find_pdftotext, parse_pdf, report

REPO = Path(__file__).resolve().parent.parent
EXAMPLE_CV = REPO / "cv" / "main_example.typ"
FONT_PATH = REPO / "cover_letters" / "OpenFonts" / "fonts"
# (roles, bullets per role). 7x4 is the typical shape. 5x6 is long entries: with an
# unbreakable cventry it overflowed to 3 pages after a 229pt hole at the foot of page 1,
# so it guards the breakable cventry.
SHAPES = [(7, 4), (5, 6)]


def full_cv_source(roles: int, bullets: int) -> str:
    src = EXAMPLE_CV.read_text(encoding="utf-8")
    start = src.index("// --- Most Recent Role ---")
    end = src.index("#section[Education]")
    roles = "".join(
        f'#cventry("20{10 + i}-20{12 + i}", "Senior Engineer {i}", "Company {i}", "City, Country")[\n'
        + "".join(
            f"  - Delivered measurable result {j} on project {i}, reducing latency and improving "
            "reliability across several production services for a large customer base.\n"
            for j in range(bullets)
        )
        + "]\n\n"
        for i in range(roles)
    )
    return src[:start] + roles + src[end:]


@unittest.skipUnless(
    shutil.which("typst") and shutil.which("pdfinfo") and find_pdftotext(),
    "needs typst plus Poppler (pdfinfo, pdftotext)",
)
class TestStockCvHoldsTwoPages(unittest.TestCase):
    def test_full_cvs_are_exactly_two_pages_with_a_clean_layout(self):
        for roles, bullets in SHAPES:
            with self.subTest(roles=roles, bullets=bullets):
                self.assert_two_clean_pages(full_cv_source(roles, bullets))

    def assert_two_clean_pages(self, text: str) -> None:
        build_root = REPO / "build"
        build_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=build_root) as tmp:
            source, pdf = Path(tmp) / "cv_full.typ", Path(tmp) / "cv_full.pdf"
            source.write_text(text, encoding="utf-8")
            subprocess.run(
                ["typst", "compile", "--font-path", str(FONT_PATH), str(source), str(pdf)],
                check=True,
                capture_output=True,
            )
            info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
            pages = int(next(l for l in info.splitlines() if l.startswith("Pages:")).split()[1])
            self.assertEqual(pages, 2, "a full CV on the stock template must be exactly 2 pages")
            with redirect_stdout(io.StringIO()):
                problems = report(pdf, parse_pdf(pdf))
            self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
