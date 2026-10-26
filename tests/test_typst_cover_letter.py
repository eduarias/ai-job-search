"""The cover letter's name block must be centred on the page.

`namesection("", last, ...)` once emitted a separate empty text run before the
name, which added a stray space and left the stock example ~1.5pt off-centre; a
two-part name must centre too. Measured from the rendered PDF's word boxes, so it
needs `typst` and Poppler's `pdftotext` and skips where they are absent (the
`typst-smoke` CI job installs both). Output goes inside the repo because a
snap-installed Typst cannot write outside the home directory.
"""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.verify_layout import find_pdftotext

REPO = Path(__file__).resolve().parent.parent
FONT_PATH = REPO / "cover_letters" / "OpenFonts" / "fonts"
WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="[\d.]+">')
TOLERANCE_PT = 0.5


def name_center(typ_source: str, binary: str) -> tuple[float, float]:
    """(center of the first printed line, page center) for a compiled letter."""
    build_root = REPO / "build"
    build_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=build_root) as tmp:
        source, pdf = Path(tmp) / "letter.typ", Path(tmp) / "letter.pdf"
        source.write_text(typ_source, encoding="utf-8")
        subprocess.run(
            ["typst", "compile", "--root", str(REPO), "--font-path", str(FONT_PATH), str(source), str(pdf)],
            check=True,
            capture_output=True,
        )
        out = subprocess.run([binary, "-bbox", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    page_width = float(re.search(r'<page width="([\d.]+)"', out).group(1))
    words = [(float(x0), float(y), float(x1)) for x0, y, x1 in WORD.findall(out)]
    top = min(y for _, y, _ in words)
    first_line = [(x0, x1) for x0, y, x1 in words if abs(y - top) < 2]
    return (min(x0 for x0, _ in first_line) + max(x1 for _, x1 in first_line)) / 2, page_width / 2


@unittest.skipUnless(shutil.which("typst") and find_pdftotext(), "needs typst plus Poppler pdftotext")
class TestNameSectionIsCentred(unittest.TestCase):
    def assert_centred(self, first: str):
        binary = find_pdftotext()
        src = (
            '#import "/cover_letters/cover.typ": *\n#show: cover\n'
            f'#namesection("{first}", "Doe", [contact])\n'
        )
        center, page_center = name_center(src, binary)
        self.assertAlmostEqual(center, page_center, delta=TOLERANCE_PT)

    def test_name_with_no_first_name_is_centred(self):
        self.assert_centred("")

    def test_two_part_name_is_centred(self):
        self.assert_centred("Jane")


if __name__ == "__main__":
    unittest.main()
