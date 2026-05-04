#!/usr/bin/env python3
"""
Validate internal markdown links across the repository.
Finds broken references (links to files that don't exist).

Usage:
    python3 tools/validate_links.py
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {'.git', '.venv', 'site', '__pycache__', '.pytest_cache', 'node_modules', '.gemini'}

# Match markdown links: [text](path.md) or [text](path.md#anchor)
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+\.(?:md|py|html|yml|yaml))(?:#[^)]*)?\)')


def find_markdown_files():
    """Find all markdown files in the repo."""
    md_files = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    return md_files


def validate_links(filepath):
    """Check all markdown links in a file. Returns list of broken links."""
    broken = []
    filedir = os.path.dirname(filepath)
    
    with open(filepath, 'r') as f:
        for lineno, line in enumerate(f, 1):
            for match in LINK_PATTERN.finditer(line):
                link_text = match.group(1)
                link_path = match.group(2)
                
                # Skip external links
                if link_path.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                
                # Resolve relative path
                target = os.path.normpath(os.path.join(filedir, link_path))
                
                if not os.path.exists(target):
                    rel_source = os.path.relpath(filepath, REPO)
                    broken.append({
                        'source': rel_source,
                        'line': lineno,
                        'link_text': link_text,
                        'target': link_path,
                        'resolved': os.path.relpath(target, REPO),
                    })
    
    return broken


def main():
    md_files = find_markdown_files()
    print(f"Scanning {len(md_files)} markdown files...")
    
    all_broken = []
    for filepath in md_files:
        broken = validate_links(filepath)
        all_broken.extend(broken)
    
    if all_broken:
        print(f"\n❌ Found {len(all_broken)} broken link(s):\n")
        for b in all_broken:
            print(f"  {b['source']}:{b['line']}")
            print(f"    [{b['link_text']}]({b['target']})")
            print(f"    → resolves to: {b['resolved']} (NOT FOUND)")
            print()
        sys.exit(1)
    else:
        print(f"\n✅ All links valid across {len(md_files)} files.")
        sys.exit(0)


if __name__ == "__main__":
    main()
