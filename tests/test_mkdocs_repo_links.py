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


if __name__ == "__main__":
    unittest.main()
