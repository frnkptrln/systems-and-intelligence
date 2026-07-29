import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lab.tools.mkdocs_repo_links import on_page_markdown
from lab.tools.validate_links import validate_links


def test_rejects_link_that_traverses_repository_symlink(tmp_path):
    docs = tmp_path / 'docs'
    theory = tmp_path / 'theory'
    docs.mkdir()
    theory.mkdir()
    (theory / 'target.md').write_text('# Target\n', encoding='utf-8')
    (docs / 'theory').symlink_to(theory, target_is_directory=True)
    source = docs / 'source.md'
    source.write_text('[Target](theory/target.md)\n', encoding='utf-8')

    problems = validate_links(str(source))

    assert len(problems) == 1
    assert 'TRAVERSES SYMLINK' in problems[0]['resolved']


def test_accepts_repository_relative_link_avoiding_symlink(tmp_path):
    docs = tmp_path / 'docs'
    theory = tmp_path / 'theory'
    docs.mkdir()
    theory.mkdir()
    (theory / 'target.md').write_text('# Target\n', encoding='utf-8')
    source = docs / 'source.md'
    source.write_text('[Target](../theory/target.md)\n', encoding='utf-8')

    assert validate_links(str(source)) == []


def test_mkdocs_hook_maps_root_link_only_for_root_pages():
    markdown = '[Target](../theory/core/target.md)'
    root_page = SimpleNamespace(file=SimpleNamespace(src_path='synthesis.md'))
    nested_page = SimpleNamespace(
        file=SimpleNamespace(src_path='interactive/example.md')
    )

    assert on_page_markdown(
        markdown, page=root_page, config=None, files=None
    ) == '[Target](theory/core/target.md)'
    assert on_page_markdown(
        markdown, page=nested_page, config=None, files=None
    ) == markdown
