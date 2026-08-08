"""Guard the MkDocs link-rewrite hook against layer drift."""

import importlib.util
import os
import sys
import unittest

REPO = os.path.join(os.path.dirname(__file__), "..")
_MODULE = os.path.join(REPO, "lab", "tools", "mkdocs_repo_links.py")


def _load():
    spec = importlib.util.spec_from_file_location("mkdocs_repo_links", _MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


hook = _load()


class _Page:
    def __init__(self, src_path):
        self.file = type("File", (), {"src_path": src_path})()


class TestLayerListMatchesDocsTree(unittest.TestCase):
    def test_root_layers_equal_docs_symlinks(self):
        docs = os.path.join(REPO, "docs")
        symlinked = {
            name
            for name in os.listdir(docs)
            if os.path.islink(os.path.join(docs, name))
        }
        self.assertEqual(set(hook.ROOT_LAYERS), symlinked)


class _Files:
    """Stand-in for the MkDocs file collection: only these paths are built."""

    def __init__(self, published):
        self._published = set(published)

    def get_file_from_path(self, path):
        return object() if path in self._published else None


class TestRewriteBehavior(unittest.TestCase):
    def _run(self, markdown, src_path="index.md"):
        return hook.on_page_markdown(
            markdown, page=_Page(src_path), config=None, files=None
        )

    def test_layer_links_are_rewritten_on_root_pages(self):
        for layer in hook.ROOT_LAYERS:
            self.assertEqual(
                self._run(f"[x](../{layer}/a.md)"),
                f"[x]({layer}/a.md)",
            )

    def test_non_layer_links_are_untouched(self):
        for markdown in (
            "[x](../ideas/note.md)",          # ideas is deliberately off-site
            "[x](../assets/img.png)",         # not a layer prefix
            "[x](thinking-space.md)",         # already docs-relative
            "[x](https://example.com/../theory/)",  # not a markdown link start
        ):
            self.assertEqual(self._run(markdown), markdown)

    def test_non_root_pages_are_untouched(self):
        markdown = "[x](../theory/core/conceptual-map.md)"
        self.assertEqual(
            self._run(markdown, src_path="theory/README.md"), markdown
        )


class TestUnpublishedRedirect(unittest.TestCase):
    REPO_URL = "https://github.com/frnkptrln/systems-and-intelligence"
    BLOB = REPO_URL + "/blob/main/"

    def _run(self, markdown, src_path, published):
        return hook.on_page_markdown(
            markdown,
            page=_Page(src_path),
            config={"repo_url": self.REPO_URL},
            files=_Files(published),
        )

    def test_published_targets_stay_relative(self):
        markdown = "[x](conceptual-map.md)"
        self.assertEqual(
            self._run(markdown, "theory/core/a.md", {"theory/core/conceptual-map.md"}),
            markdown,
        )

    def test_unpublished_targets_go_to_github(self):
        self.assertEqual(
            self._run("[x](conceptual-map.md)", "theory/core/a.md", set()),
            f"[x]({self.BLOB}theory/core/conceptual-map.md)",
        )

    def test_anchors_survive_the_redirect(self):
        self.assertEqual(
            self._run("[x](../veto/b.md#section)", "theory/core/a.md", set()),
            f"[x]({self.BLOB}theory/veto/b.md#section)",
        )

    def test_absolute_urls_are_left_alone(self):
        markdown = "[x](https://example.com/a.md)"
        self.assertEqual(self._run(markdown, "theory/core/a.md", set()), markdown)

    def test_fenced_code_is_not_rewritten(self):
        markdown = "```\n[x](gone.md)\n```"
        self.assertEqual(self._run(markdown, "theory/core/a.md", set()), markdown)

    def test_source_files_are_redirected_too(self):
        self.assertEqual(
            self._run("[x](../../lab/experiments/exp6.py)", "theory/core/a.md", set()),
            f"[x]({self.BLOB}lab/experiments/exp6.py)",
        )

    def test_image_embeds_are_left_alone(self):
        markdown = "![x](diagram.png)"
        self.assertEqual(self._run(markdown, "theory/core/a.md", set()), markdown)

    def test_missing_repo_url_disables_the_redirect(self):
        markdown = "[x](gone.md)"
        result = hook.on_page_markdown(
            markdown, page=_Page("theory/core/a.md"), config={}, files=_Files(set())
        )
        self.assertEqual(result, markdown)


if __name__ == "__main__":
    unittest.main()
