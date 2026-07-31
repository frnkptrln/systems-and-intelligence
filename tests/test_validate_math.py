import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lab.tools.validate_math import scan_file


def scan(tmp_path, source):
    markdown = tmp_path / 'sample.md'
    markdown.write_text(source, encoding='utf-8')
    problems, expression_count = scan_file(str(markdown))
    return [problem.message for problem in problems], expression_count


def test_accepts_portable_inline_and_display_math(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        (
            'Inline $\\mathrm{IP}(t)$ expression.\n\n'
            '$$\n'
            'S = \\left\\lbrace x \\right\\rbrace,\n'
            '\\qquad q = \\mathop{\\mathrm{arg\\,min}}\\limits_x f(x)\n'
            '$$\n'
        ),
    )

    assert problems == []
    assert expression_count == 2


def test_rejects_markdown_heading_marker_inside_display_math(tmp_path):
    problems, _ = scan(tmp_path, '$$\n\\frac{dx}{dt}\n=\nf(x)\n$$\n')

    assert any('heading marker' in message for message in problems)


def test_requires_blank_lines_around_display_math(tmp_path):
    problems, _ = scan(tmp_path, 'Before\n$$\nx = 1\n$$\nAfter\n')

    assert sum('needs a blank line' in message for message in problems) == 2


def test_rejects_legacy_math_delimiters(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        'Inline \\(x\\).\n\n\\[\ny = 2\n\\]\n',
    )

    assert any('inline-math delimiters' in message for message in problems)
    assert any('display-math delimiter' in message for message in problems)
    assert expression_count == 2


def test_ignores_literal_escaped_brackets_and_code(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        '*\\[Stage direction.\\]*\n\n```text\n\\(not math here\\)\n```\n',
    )

    assert problems == []
    assert expression_count == 0


def test_rejects_github_blocked_operatorname_macro(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        (
            'Inline $\\operatorname{IP}(t)$ expression.\n\n'
            '$$\n'
            'q = \\operatorname*{arg\\,min}_x f(x)\n'
            '$$\n'
        ),
    )

    assert sum('operatorname' in message for message in problems) == 2
    assert expression_count == 2


def test_rejects_github_unsafe_plain_escaped_braces(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        '$$\nS = \\{x : x > 0\\}\n$$\n',
    )

    assert any(r'\lbrace' in message and r'\rbrace' in message for message in problems)
    assert expression_count == 1


def test_rejects_github_unsafe_sized_escaped_braces(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        '$$\nS = \\left\\{x : x > 0\\right\\}\n$$\n',
    )

    assert any(r'\lbrace' in message and r'\rbrace' in message for message in problems)
    assert expression_count == 1
