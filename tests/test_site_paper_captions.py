"""The website PDF keeps scientific captions visible and image URLs intact."""

import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import re

import pytest


# The PDF builder belongs to the optional documentation dependency set.
pytest.importorskip("weasyprint")
pytest.importorskip("markdown")

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "site_paper_pdf", ROOT / "lab/tools/build_paper_pdf.py"
)
site_pdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site_pdf)


def test_all_six_source_captions_preserve_their_wording_and_math():
    source = site_pdf.DEFAULT_PAPER.read_text(encoding="utf-8")
    figures = re.findall(r"^!\[(.*?)\]\((.*?)\)$", source, re.MULTILINE)
    assert len(figures) == 6
    result = site_pdf.visible_figure_captions(source)
    for caption, target in figures:
        assert f"![Figure]({target})\n\n{caption}" in result
        assert result.count(caption) == 1


@pytest.mark.parametrize("fence", ["```", "~~~"])
def test_fenced_examples_and_ordinary_images_remain_unchanged(fence):
    figure = r"![**Figure 1.** A caption with $K > K_c$.](figure.png)"
    source = f"{fence}markdown\n{figure}\n{fence}\n\n![](empty.png)\n\n![Logo](logo.png)"
    assert site_pdf.visible_figure_captions(source) == source
    # A real figure following the example must still acquire visible prose.
    result = site_pdf.visible_figure_captions(source + "\n\n" + figure)
    assert result.startswith(source + "\n\n")
    assert result.endswith("![Figure](figure.png)\n\n**Figure 1.** A caption with $K > K_c$.")


def test_build_promotes_captions_before_math_and_preserves_images(tmp_path, monkeypatch):
    class Document(HTMLParser):
        def __init__(self, string, base_url):
            super().__init__()
            self.images = []
            self.text = []
            self.feed(string)

        def handle_starttag(self, tag, attrs):
            if tag == "img":
                self.images.append(dict(attrs))

        def handle_data(self, data):
            self.text.append(data)

        def write_pdf(self, output, font_config):
            expected = re.findall(
                r"^!\[.*?\]\(\.\./(.*?)\)$",
                site_pdf.DEFAULT_PAPER.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
            actual = [image for image in self.images if image.get("src") in expected]
            assert len(actual) == 6
            assert all(image["alt"] == "Figure" for image in actual)
            visible = " ".join(self.text)
            for label in ("Figure 1:", "Figure C1", "Figure C2", "Figure C3", "Figure C4", "Figure D1"):
                assert label in visible
            assert "Schematic only; numerical thresholds are not calibrated." in visible
            assert r"\gamma > \gamma_c" in visible
            Path(output).write_bytes(b"%PDF-test")

    monkeypatch.setattr(site_pdf, "HTML", Document)
    monkeypatch.setattr(site_pdf, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        site_pdf, "render_math",
        lambda expression, inline: f"<span>{site_pdf.html.escape(expression)}</span>",
    )
    site_pdf.build(site_pdf.DEFAULT_PAPER, tmp_path / "paper.pdf")
