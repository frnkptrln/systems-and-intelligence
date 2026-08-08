"""Keep Markdown links working across the repository/site boundary.

Two rewrites happen here, both about the same seam: the repository is the
whole body of work, the site publishes a curated part of it.

1. Root pages (``index.md`` and friends) live in ``docs/`` but link with
   ``../layer/...`` so the links also resolve when read on GitHub. Inside
   ``docs_dir`` the layers are symlinked at the top level, so the ``../``
   has to go.

2. Pages excluded from the site by ``exclude_docs`` are still real files in
   the repository, and published pages still legitimately point at them.
   Rather than break those links — or force the site to publish everything
   so they resolve — the link is redirected to the file on GitHub. Nothing
   is hidden; it just stops competing for a reader's attention.
"""

import posixpath
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

ROOT_PAGES = {'index.md', 'synthesis.md', 'thinking-space.md', 'repository-map.md'}
REPO_ROOT_LINK = re.compile(
    r'(\]\()\.\./'
    r'(?=(?:' + '|'.join(re.escape(layer) for layer in ROOT_LAYERS) + r')/)'
)

# ``](target.ext)`` or ``](target.ext#anchor)``, excluding absolute URLs.
# Not restricted to Markdown: prose links to the source files that back a
# claim (``lab/experiments/exp6_binding_observables.py``) need the same
# treatment.
MARKDOWN_LINK = re.compile(
    r'\]\((?!\w+:)(?P<target>[^)\s#]+\.[A-Za-z0-9]{1,6})(?P<anchor>#[^)\s]*)?\)'
)

# Image embeds are skipped by extension rather than by trying to spot the
# leading ``!`` from the closing bracket: a GitHub blob URL is a page, not an
# image, so rewriting one would replace the picture with a broken embed.
IMAGE_SUFFIXES = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.avif', '.ico')

# Links inside fenced code are examples, not navigation.
FENCE = re.compile(r'```.*?```|~~~.*?~~~', re.DOTALL)

DEFAULT_BRANCH = 'main'


def _rewrite_root_links(markdown, page):
    """Map repository paths to the aliases visible inside ``docs_dir``."""
    if page.file.src_path not in ROOT_PAGES:
        return markdown
    return REPO_ROOT_LINK.sub(r'\1', markdown)


def _is_published(file):
    """True when MkDocs will actually build a page for this file.

    ``exclude_docs`` does not drop files from the collection; it marks their
    inclusion level. A file object alone therefore proves nothing — an
    excluded page is still present and still answers to its path.
    """
    if file is None:
        return False
    inclusion = getattr(file, 'inclusion', None)
    is_included = getattr(inclusion, 'is_included', None)
    return is_included() if callable(is_included) else True


def _redirect_unpublished(markdown, page, config, files):
    """Point links at GitHub when their target is not part of the built site."""
    if files is None or config is None:
        return markdown

    repo_url = (config.get('repo_url') or '').rstrip('/')
    if not repo_url:
        return markdown
    blob = f'{repo_url}/blob/{DEFAULT_BRANCH}/'

    here = posixpath.dirname(page.file.src_path.replace('\\', '/'))

    protected = []

    def stash(match):
        protected.append(match.group(0))
        return f'\x00FENCE{len(protected) - 1}\x00'

    markdown = FENCE.sub(stash, markdown)

    def redirect(match):
        target = match.group('target')
        anchor = match.group('anchor') or ''
        if target.startswith('/') or target.lower().endswith(IMAGE_SUFFIXES):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(here, target))
        if resolved.startswith('..'):
            # Points outside docs_dir entirely; leave it for MkDocs to report.
            return match.group(0)
        if _is_published(files.get_file_from_path(resolved)):
            return match.group(0)
        return f']({blob}{resolved}{anchor})'

    markdown = MARKDOWN_LINK.sub(redirect, markdown)

    for index, block in enumerate(protected):
        markdown = markdown.replace(f'\x00FENCE{index}\x00', block)
    return markdown


def on_page_markdown(markdown, *, page, config, files):
    markdown = _rewrite_root_links(markdown, page)
    return _redirect_unpublished(markdown, page, config, files)
