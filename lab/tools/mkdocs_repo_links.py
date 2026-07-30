"""Translate GitHub-relative root links for the symlinked MkDocs tree."""

import re


# Repository layers exposed inside docs_dir as symlinks. Kept as an explicit
# tuple so the hook stays deterministic; tests/test_mkdocs_repo_links.py
# asserts this tuple matches the actual symlink set in docs/, so adding a new
# layer without updating the hook fails the test suite instead of silently
# leaving that layer's root-page links unrewritten.
ROOT_LAYERS = (
    'book',
    'fiction',
    'lab',
    'logs',
    'meta',
    'papers',
    'simulation-models',
    'theory',
)

ROOT_PAGES = {'index.md', 'synthesis.md', 'thinking-space.md'}
REPO_ROOT_LINK = re.compile(
    r'(\]\()\.\./'
    r'(?=(?:' + '|'.join(re.escape(layer) for layer in ROOT_LAYERS) + r')/)'
)


def on_page_markdown(markdown, *, page, config, files):
    """Map repository paths to the aliases visible inside ``docs_dir``."""
    if page.file.src_path not in ROOT_PAGES:
        return markdown
    return REPO_ROOT_LINK.sub(r'\1', markdown)
