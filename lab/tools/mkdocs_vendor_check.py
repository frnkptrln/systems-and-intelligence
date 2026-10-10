"""Refuse to build the site without its self-hosted browser assets.

The notebook loads no code, styles or fonts from third-party hosts: KaTeX, the
fonts and the libraries of the interactive apps are copied from pinned npm
packages into docs/assets/vendor/ by lab/tools/vendor_assets.mjs. That
directory is generated and ignored by git, so a build without it would publish
pages whose math, type and charts fail to load. This hook stops such a build,
and one whose copied assets no longer match the versions in package.json.
"""

import json
from pathlib import Path

from mkdocs.exceptions import PluginError

HINT = "run `npm ci && npm run vendor` before building the site"


def on_config(config):
    repo = Path(config["config_file_path"]).resolve().parent
    marker = Path(config["docs_dir"]) / "assets" / "vendor" / "VERSIONS.json"
    if not marker.is_file():
        raise PluginError(f"self-hosted site assets are missing ({marker.relative_to(repo)}); {HINT}")
    vendored = json.loads(marker.read_text(encoding="utf-8"))
    pinned = json.loads((repo / "package.json").read_text(encoding="utf-8"))["devDependencies"]
    stale = sorted(name for name, version in vendored.items() if pinned.get(name) != version)
    if stale:
        raise PluginError(f"self-hosted site assets are stale ({', '.join(stale)}); {HINT}")
    return config
