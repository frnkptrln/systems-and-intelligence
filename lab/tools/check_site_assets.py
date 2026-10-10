#!/usr/bin/env python3
"""Fail if the built site loads anything from a third-party host.

Every page of the notebook is served from frnkptrln.github.io, the origin the
other Pages sites share. A script, stylesheet, font, image or frame fetched
from another host would run in or report on that origin, and the privacy
statement says the site loads no third-party resources. This check scans the
built HTML (resource attributes and inline styles) and CSS (@import and url())
and lists every reference to another host. Ordinary links (<a href>) are
navigation, not loads, and are not checked.

    python lab/tools/check_site_assets.py site
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

OWN_HOSTS = {"frnkptrln.github.io"}
RESOURCE_RELS = {"stylesheet", "preload", "modulepreload", "prefetch", "preconnect", "dns-prefetch", "icon", "manifest"}
RESOURCE_ATTRS = {
    "script": ("src",),
    "img": ("src", "srcset"),
    "iframe": ("src",),
    "frame": ("src",),
    "embed": ("src",),
    "object": ("data",),
    "video": ("src", "poster"),
    "audio": ("src",),
    "source": ("src", "srcset"),
    "track": ("src",),
}
CSS_URL = re.compile(r"""@import\s+(?:url\()?\s*['"]?([^'")\s;]+)|url\(\s*['"]?([^'")]+)""", re.I)


def third_party(url: str) -> bool:
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    parts = urlsplit(url)
    return parts.scheme in {"http", "https"} and parts.hostname not in OWN_HOSTS


def css_hits(text: str) -> list[str]:
    return [a or b for a, b in CSS_URL.findall(text) if third_party(a or b)]


class Scanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hits: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "style":
            self._in_style = True
        if tag == "link" and RESOURCE_RELS & set((attrs.get("rel") or "").lower().split()):
            if third_party(attrs.get("href") or ""):
                self.hits.append(f"<link rel={attrs.get('rel')}> {attrs['href']}")
        for attr in RESOURCE_ATTRS.get(tag, ()):
            value = attrs.get(attr) or ""
            candidates = [part.split()[0] for part in value.split(",") if part.strip()] if attr == "srcset" else [value]
            self.hits.extend(f"<{tag} {attr}> {c}" for c in candidates if third_party(c))
        if attrs.get("style"):
            self.hits.extend(f"<{tag} style> {c}" for c in css_hits(attrs["style"]))

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.hits.extend(f"<style> {c}" for c in css_hits(data))


def scan(site: Path) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in sorted(site.rglob("*")):
        if path.suffix == ".html":
            scanner = Scanner()
            scanner.feed(path.read_text(encoding="utf-8", errors="replace"))
            hits = scanner.hits
        elif path.suffix == ".css":
            hits = css_hits(path.read_text(encoding="utf-8", errors="replace"))
        else:
            continue
        if hits:
            findings[str(path.relative_to(site))] = sorted(set(hits))
    return findings


def main(argv: list[str]) -> int:
    site = Path(argv[1] if len(argv) > 1 else "site")
    if not site.is_dir():
        print(f"{site} is not a built site; run mkdocs build first", file=sys.stderr)
        return 2
    findings = scan(site)
    for page, hits in findings.items():
        for hit in hits:
            print(f"{page}: {hit}")
    if findings:
        print(f"{sum(map(len, findings.values()))} third-party loads in {len(findings)} files", file=sys.stderr)
        return 1
    print("no third-party loads")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
