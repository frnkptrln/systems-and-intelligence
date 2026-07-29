"""Translate GitHub-relative root links for the symlinked MkDocs tree."""

import re


ROOT_PAGES = {'index.md', 'synthesis.md', 'thinking-space.md'}
REPO_ROOT_LINK = re.compile(
    r'(\]\()\.\./'
    r'(?=(?:book|fiction|lab|logs|meta|papers|simulation-models|theory)/)'
)


def on_page_markdown(markdown, *, page, config, files):
    """Map repository paths to the aliases visible inside ``docs_dir``."""
    if page.file.src_path not in ROOT_PAGES:
        return markdown
    return REPO_ROOT_LINK.sub(r'\1', markdown)
