"""Publication cuts preserve formal content; cached figures cannot drift silently."""
import importlib.util
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "viable_publication", ROOT / "lab/tools/build_viable_publication.py")
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


def test_article_preserves_displays_erratum_and_limitations():
    source = publication.PAPER.read_text()
    body = source[source.index("## Abstract"):source.index("## TODO (post-v1.0)")]
    article = publication.article_body(body)
    before = body.split("## Appendices")[0]
    after = article.split("## Appendices")[0]
    displays = re.compile(r"\$\$[\s\S]*?\$\$")
    assert len(displays.findall(before)) > 10
    assert displays.findall(after) == displays.findall(before)
    # The sufficiency erratum and limitations are outside editorial cuts.
    for start, end in (("### 3.4", "### 3.5"), ("## §6.", "## §7.")):
        assert after[after.index(start):after.index(end)].strip() == before[before.index(start):before.index(end)].strip()
    # Appendix derivations and source references remain available unchanged
    # for the accompanying Supplement even when absent from the Article PDF.
    assert article[article.index("## Appendices"):].strip() == body[body.index("## Appendices"):].strip()


def test_article_edit_drift_fails_instead_of_silently_omitting_a_cut():
    with pytest.raises(ValueError, match="no longer matches exactly once"):
        publication.article_body("A revised manuscript with no matching passages.")


def test_scientific_figure_captions_are_visible_prose_not_only_alt_text():
    source = publication.PAPER.read_text().replace("../lab/tools/", "figures/")
    images = re.findall(r"!\[(.*?)\]\((figures/[^)]+)\)", source, flags=re.DOTALL)
    assert len(images) == 6
    result = publication.visible_figure_captions(source)
    for caption, path in images:
        # The caption is outside the image syntax, where Pandoc renders it as
        # visible manuscript text rather than an accessibility-only attribute.
        assert f"]({path})\n\n{caption}" in result


def test_reference_format_preserves_entries_and_continuation_lines():
    source = publication.PAPER.read_text()
    body = source[source.index("## Abstract"):source.index("## TODO (post-v1.0)")]
    references = body.split("## References\n\n", 1)[1]
    note, entries = references.split("\n\n- ", 1)
    expected = re.sub(r"(?m)^- ", "", "- " + entries).strip()
    formatted = publication.reference_paragraphs(body)
    assert note in formatted
    assert expected in formatted
    continued = "## References\n\nA note.\n\n- First line\n  continuation.\n\n- Second entry.\n"
    assert "First line\n  continuation.\n\nSecond entry." in publication.reference_paragraphs(continued)


@pytest.mark.parametrize("damage", ["source", "artifact", "missing", "unrecorded"])
def test_figure_reuse_rejects_stale_or_missing_inputs(tmp_path, monkeypatch, damage):
    repo = tmp_path / "repo"
    output = tmp_path / "export"
    monkeypatch.setattr(publication, "ROOT", repo)
    sources = {}
    artifacts = {}
    for name in publication.FIGURE_SOURCES:
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Original figure-generating source")
        sources[name] = publication.sha(path)
    for name in publication.FIGURE_NAMES:
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"Original generated figure")
        artifacts[name] = publication.sha(path)
    (output / "manifest.json").write_text(json.dumps({
        "sources_sha256": sources, "artifacts_sha256": artifacts}))
    publication.validate_figure_cache(output)
    if damage == "source":
        (repo / publication.FIGURE_SOURCES[0]).write_text("Changed source")
    elif damage == "artifact":
        (output / publication.FIGURE_NAMES[0]).write_bytes(b"Changed figure")
    elif damage == "missing":
        (output / publication.FIGURE_NAMES[0]).unlink()
    else:
        del artifacts[publication.FIGURE_NAMES[0]]
        (output / "manifest.json").write_text(json.dumps({"sources_sha256": sources, "artifacts_sha256": artifacts}))
    with pytest.raises(ValueError, match="Figure source changed|Cached figure changed|Missing canonical figure"):
        publication.validate_figure_cache(output)
