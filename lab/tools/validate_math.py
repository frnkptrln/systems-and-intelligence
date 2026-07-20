#!/usr/bin/env python3
"""Validate portable mathematical Markdown across the repository.

The documentation is read in two places with different renderers:

- GitHub renders Markdown with MathJax.
- MkDocs renders the public site with Arithmatex and KaTeX.

Both accept ``$...$`` for inline mathematics and ``$$...$$`` for display
mathematics, but GitHub can reinterpret malformed display blocks as ordinary
Markdown. In particular, a bare ``=`` inside an unrecognised block becomes a
Setext heading. This validator keeps the shared subset explicit.

Usage:
    python lab/tools/validate_math.py
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import re
import sys


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {
    '.git',
    '.venv',
    'site',
    '__pycache__',
    '.pytest_cache',
    'node_modules',
    '.gemini',
}
FENCE_RE = re.compile(r'^\s{0,3}(`{3,}|~{3,})')
SETEXT_RE = re.compile(r'^\s*(?:=+|-+)\s*$')
LEGACY_INLINE_RE = re.compile(r'(?<!\\)\\\((.+?)(?<!\\)\\\)')
LEGACY_INLINE_TOKEN_RE = re.compile(r'(?<!\\)\\(?:\(|\))')
LEGACY_DISPLAY_OPEN_RE = re.compile(r'^\s*\\\[\s*$')
LEGACY_DISPLAY_CLOSE_RE = re.compile(r'^\s*\\\]\s*$')
LATEX_COMMAND_RE = re.compile(
    r'(?<!\\)\\(?:'
    r'begin|end|frac|sqrt|sum|prod|int|lim|text|operatorname|mathrm|mathbf|mathbb|mathcal|'
    r'alpha|beta|gamma|delta|theta|lambda|omega|Omega|Sigma|phi|psi|varepsilon|'
    r'left|right|quad|qquad|times|otimes|rightsquigarrow|Longleftrightarrow'
    r')\b'
)


@dataclass(frozen=True)
class Problem:
    path: str
    line: int
    message: str


def find_markdown_files() -> list[str]:
    """Return every Markdown source file that belongs to the repository."""
    paths = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
        for filename in files:
            if filename.endswith('.md'):
                paths.append(os.path.join(root, filename))
    return sorted(paths)


def strip_inline_code(line: str) -> str:
    """Replace inline-code spans with spaces while preserving character offsets."""
    chars = list(line)
    index = 0
    while index < len(line):
        if line[index] != '`':
            index += 1
            continue
        run_end = index
        while run_end < len(line) and line[run_end] == '`':
            run_end += 1
        marker = line[index:run_end]
        close = line.find(marker, run_end)
        if close == -1:
            index = run_end
            continue
        for position in range(index, close + len(marker)):
            chars[position] = ' '
        index = close + len(marker)
    return ''.join(chars)


def strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Mask HTML comments, including comments spanning several lines."""
    chars = list(line)
    index = 0
    while index < len(line):
        if in_comment:
            close = line.find('-->', index)
            if close == -1:
                return ' ' * len(line), True
            for position in range(index, close + 3):
                chars[position] = ' '
            index = close + 3
            in_comment = False
            continue
        start = line.find('<!--', index)
        if start == -1:
            break
        close = line.find('-->', start + 4)
        if close == -1:
            for position in range(start, len(line)):
                chars[position] = ' '
            return ''.join(chars), True
        for position in range(start, close + 3):
            chars[position] = ' '
        index = close + 3
    return ''.join(chars), in_comment


def single_dollar_positions(line: str) -> list[int]:
    """Return unescaped dollar signs that are not part of ``$$``."""
    positions = []
    index = 0
    while index < len(line):
        if line[index] == '\\':
            index += 2
            continue
        if line[index] != '$':
            index += 1
            continue
        if (index > 0 and line[index - 1] == '$') or (
            index + 1 < len(line) and line[index + 1] == '$'
        ):
            index += 1
            continue
        positions.append(index)
        index += 1
    return positions


def brace_problem(expression: str) -> str | None:
    """Return a message for unbalanced TeX grouping braces, if present."""
    depth = 0
    index = 0
    while index < len(expression):
        if expression[index] == '\\':
            index += 2
            continue
        if expression[index] == '{':
            depth += 1
        elif expression[index] == '}':
            depth -= 1
            if depth < 0:
                return 'mathematical expression has an unmatched closing brace'
        index += 1
    if depth:
        return 'mathematical expression has an unmatched opening brace'
    return None


def scan_file(filepath: str) -> tuple[list[Problem], int]:
    """Validate one Markdown file and return problems plus expression count."""
    relative = os.path.relpath(filepath, REPO)
    with open(filepath, encoding='utf-8') as handle:
        lines = handle.read().splitlines()

    problems: list[Problem] = []
    expression_count = 0
    fence_marker: str | None = None
    in_comment = False
    display_start: int | None = None
    display_lines: list[str] = []
    legacy_display_start: int | None = None
    legacy_display_lines: list[str] = []

    for offset, raw_line in enumerate(lines):
        line_number = offset + 1
        fence = FENCE_RE.match(raw_line)
        if fence_marker:
            if fence and fence.group(1)[0] == fence_marker[0] and len(fence.group(1)) >= len(fence_marker):
                fence_marker = None
            continue
        if fence:
            fence_marker = fence.group(1)
            continue

        line, in_comment = strip_html_comments(raw_line, in_comment)
        line = strip_inline_code(line)
        stripped = line.strip()

        if legacy_display_start is not None:
            if LEGACY_DISPLAY_CLOSE_RE.match(stripped):
                expression_count += 1
                message = brace_problem('\n'.join(legacy_display_lines))
                if message:
                    problems.append(Problem(relative, legacy_display_start, message))
                legacy_display_start = None
                legacy_display_lines = []
            else:
                legacy_display_lines.append(line)
            continue

        if LEGACY_DISPLAY_OPEN_RE.match(stripped):
            problems.append(Problem(
                relative,
                line_number,
                r'non-portable display-math delimiter \[; use $$ on its own line',
            ))
            legacy_display_start = line_number
            legacy_display_lines = []
            continue

        if LEGACY_DISPLAY_CLOSE_RE.match(stripped):
            problems.append(Problem(
                relative,
                line_number,
                r'unpaired display-math delimiter \]; use a matching $$ block',
            ))
            continue

        if stripped == '$$':
            if display_start is None:
                display_start = line_number
                display_lines = []
                if offset and lines[offset - 1].strip():
                    problems.append(Problem(
                        relative,
                        line_number,
                        'display mathematics needs a blank line before opening $$ for GitHub',
                    ))
            else:
                expression_count += 1
                if offset + 1 < len(lines) and lines[offset + 1].strip():
                    problems.append(Problem(
                        relative,
                        line_number,
                        'display mathematics needs a blank line after closing $$ for GitHub',
                    ))
                expression = '\n'.join(display_lines)
                message = brace_problem(expression)
                if message:
                    problems.append(Problem(relative, display_start, message))
                display_start = None
                display_lines = []
            continue

        if display_start is not None:
            if SETEXT_RE.match(stripped):
                problems.append(Problem(
                    relative,
                    line_number,
                    'bare Markdown heading marker inside display mathematics; attach it to an equation line',
                ))
            display_lines.append(line)
            continue

        for match in re.finditer(r'(?<!\\)\$\$(.+?)(?<!\\)\$\$', line):
            expression_count += 1
            message = brace_problem(match.group(1))
            if message:
                problems.append(Problem(relative, line_number, message))
        without_same_line_display = re.sub(
            r'(?<!\\)\$\$(.+?)(?<!\\)\$\$',
            lambda match: ' ' * len(match.group(0)),
            line,
        )

        without_legacy_inline = list(without_same_line_display)
        for match in LEGACY_INLINE_RE.finditer(without_same_line_display):
            expression_count += 1
            problems.append(Problem(
                relative,
                line_number,
                r'non-portable inline-math delimiters \(...\); use $...$',
            ))
            message = brace_problem(match.group(1))
            if message:
                problems.append(Problem(relative, line_number, message))
            for position in range(match.start(), match.end()):
                without_legacy_inline[position] = ' '

        without_legacy_inline = ''.join(without_legacy_inline)
        legacy_token = LEGACY_INLINE_TOKEN_RE.search(without_legacy_inline)
        if legacy_token:
            problems.append(Problem(
                relative,
                line_number,
                f'unpaired non-portable math delimiter {legacy_token.group(0)!r}',
            ))

        positions = single_dollar_positions(without_legacy_inline)
        if len(positions) % 2:
            problems.append(Problem(
                relative,
                line_number,
                'unpaired inline $ delimiter; inline mathematics must open and close on one line',
            ))
            continue

        outside = list(without_legacy_inline)
        for start, end in zip(positions[::2], positions[1::2]):
            expression_count += 1
            expression = without_legacy_inline[start + 1:end]
            if not expression.strip():
                problems.append(Problem(relative, line_number, 'empty inline mathematical expression'))
            message = brace_problem(expression)
            if message:
                problems.append(Problem(relative, line_number, message))
            for position in range(start, end + 1):
                outside[position] = ' '

        command = LATEX_COMMAND_RE.search(''.join(outside))
        if command:
            problems.append(Problem(
                relative,
                line_number,
                f'LaTeX command {command.group(0)!r} appears outside mathematical delimiters',
            ))

    if display_start is not None:
        problems.append(Problem(relative, display_start, 'unclosed $$ display-math block'))
    if legacy_display_start is not None:
        problems.append(Problem(
            relative,
            legacy_display_start,
            r'unclosed non-portable display-math block beginning with \[',
        ))

    return problems, expression_count


def main() -> int:
    markdown_files = find_markdown_files()
    all_problems = []
    expression_count = 0
    for filepath in markdown_files:
        problems, count = scan_file(filepath)
        all_problems.extend(problems)
        expression_count += count

    print(
        f'Scanned {expression_count} mathematical expressions across '
        f'{len(markdown_files)} Markdown files.'
    )
    if all_problems:
        print(f'\nFound {len(all_problems)} mathematical Markdown problem(s):\n')
        for problem in all_problems:
            print(f'  {problem.path}:{problem.line}')
            print(f'    {problem.message}')
        return 1

    print('\nAll mathematical Markdown uses the portable GitHub/MkDocs syntax.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
