#!/usr/bin/env python3
"""Require every publishable Markdown page to be reachable from MkDocs nav.

The documentation tree is assembled from repository directories through
symlinks, so discovery follows symlinks deliberately. Pages matched by
``exclude_docs`` are not publishable and are ignored. Rare deliberate
exceptions must be entered in ``ALLOWLIST`` with a non-empty reason.

Usage:
    python lab/tools/validate_nav.py
"""

from __future__ import annotations

from fnmatch import fnmatchcase
import os
from pathlib import Path, PurePosixPath
import sys
from typing import Iterable

import yaml


REPO = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO / "mkdocs.yml"

# A path may appear here only when it is deliberately publishable but should
# remain unreachable from the site navigation. Every entry needs a reviewable
# reason. There are currently no such exceptions.
ALLOWLIST: dict[str, str] = {}


class MkDocsLoader(yaml.SafeLoader):
    """Safe loader that treats MkDocs callable references as inert strings."""


def _construct_python_name(loader, suffix, node):
    loader.construct_scalar(node)
    return suffix


MkDocsLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    _construct_python_name,
)


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load the MkDocs configuration without importing configured callables."""
    with path.open(encoding="utf-8") as handle:
        config = yaml.load(handle, Loader=MkDocsLoader)
    if not isinstance(config, dict):
        raise ValueError(f"{path} must contain a mapping")
    return config


def nav_markdown_paths(value) -> set[str]:
    """Collect Markdown targets recursively from a MkDocs nav value."""
    paths: set[str] = set()
    if isinstance(value, str):
        target = value.split("#", 1)[0]
        if target.endswith(".md") and "://" not in target:
            paths.add(PurePosixPath(target).as_posix())
    elif isinstance(value, list):
        for item in value:
            paths.update(nav_markdown_paths(item))
    elif isinstance(value, dict):
        for item in value.values():
            paths.update(nav_markdown_paths(item))
    return paths


def exclude_patterns(value) -> tuple[str, ...]:
    """Normalize MkDocs ``exclude_docs`` strings or lists."""
    if value is None:
        return ()
    lines: Iterable[str]
    if isinstance(value, str):
        lines = value.splitlines()
    elif isinstance(value, list):
        lines = (str(item) for item in value)
    else:
        raise ValueError("exclude_docs must be a string or list")
    return tuple(
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    )


def _pattern_matches(path: str, pattern: str) -> bool:
    """Match the useful Gitignore-style subset accepted by MkDocs."""
    anchored = pattern.startswith("/")
    pattern = pattern.lstrip("/")
    if pattern.endswith("/"):
        prefix = pattern.rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    if anchored:
        return fnmatchcase(path, pattern)
    if "/" not in pattern:
        return any(fnmatchcase(part, pattern) for part in path.split("/"))
    return fnmatchcase(path, pattern) or PurePosixPath(path).match(pattern)


def is_excluded(path: str, patterns: Iterable[str]) -> bool:
    """Apply ordered exclusion patterns, including ``!`` re-inclusions."""
    excluded = False
    for raw_pattern in patterns:
        negate = raw_pattern.startswith("!")
        pattern = raw_pattern[1:] if negate else raw_pattern
        if pattern and _pattern_matches(path, pattern):
            excluded = not negate
    return excluded


def markdown_pages(docs_dir: Path, patterns: Iterable[str]) -> set[str]:
    """Discover publishable Markdown pages while following docs symlinks."""
    pages: set[str] = set()
    visited: set[Path] = set()
    for root, directories, filenames in os.walk(docs_dir, followlinks=True):
        real_root = Path(root).resolve()
        if real_root in visited:
            directories[:] = []
            continue
        visited.add(real_root)
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            path = (Path(root) / filename).relative_to(docs_dir).as_posix()
            if not is_excluded(path, patterns):
                pages.add(path)
    return pages


def main() -> int:
    config = load_config()
    docs_dir = REPO / config.get("docs_dir", "docs")
    patterns = exclude_patterns(config.get("exclude_docs"))
    pages = markdown_pages(docs_dir, patterns)
    nav_paths = nav_markdown_paths(config.get("nav", []))

    invalid_allowlist = sorted(
        path
        for path, reason in ALLOWLIST.items()
        if path not in pages or not reason.strip()
    )
    if invalid_allowlist:
        print("Invalid navigation ALLOWLIST entries:", file=sys.stderr)
        for path in invalid_allowlist:
            print(f"  {path}", file=sys.stderr)
        return 1

    missing = sorted(pages - nav_paths - set(ALLOWLIST))
    if missing:
        print(
            f"{len(missing)} publishable Markdown page(s) are missing from nav:",
            file=sys.stderr,
        )
        for path in missing:
            print(f"  {path}", file=sys.stderr)
        return 1

    print(
        f"Navigation covers all {len(pages)} publishable Markdown pages "
        f"({len(ALLOWLIST)} allowlisted)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
