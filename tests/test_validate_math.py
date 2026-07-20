from lab.tools.validate_math import scan_file


def scan(tmp_path, source):
    markdown = tmp_path / 'sample.md'
    markdown.write_text(source, encoding='utf-8')
    problems, expression_count = scan_file(str(markdown))
    return [problem.message for problem in problems], expression_count


def test_accepts_portable_inline_and_display_math(tmp_path):
    problems, expression_count = scan(
        tmp_path,
        'Inline $x^2$ expression.\n\n$$\n\\frac{x}{y} = z\n$$\n',
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
