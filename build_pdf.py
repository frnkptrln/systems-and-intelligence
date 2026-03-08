import os
import re
import urllib.parse
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

"""
build_pdf.py

Compiles the entire Systems & Intelligence 'Book' from markdown files
into a single, beautifully formatted PDF document.
"""

def generate_pdf():
    book_dir = "docs/book"
    output_filename = "systems-and-intelligence-book.pdf"
    
    # Ensure chapters are read in order
    chapters = sorted([f for f in os.listdir(book_dir) if f.endswith('.md')])
    
    # Exclude non-book markdown if any, though all 00-07 are book.
    # Accumulate all markdown content
    full_markdown = "# Systems & Intelligence\n\n## The Grand Synthesis\n\n*By Frank Peterlein*\n\n<div style='page-break-after: always;'></div>\n\n"
    
    for chapter in chapters:
        filepath = os.path.join(book_dir, chapter)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace("../../", "") 
            full_markdown += content + "\n\n<div style='page-break-after: always;'></div>\n\n"

    # Pre-process math into SVG images via Codecogs
    def block_repl(match):
        math_expr = match.group(1).strip()
        encoded = urllib.parse.quote(math_expr)
        return f'\n<div style="text-align: center; margin: 1.5em 0;"><img src="https://latex.codecogs.com/svg.image?\\color{{black}}{encoded}" alt="{math_expr}" /></div>\n'
    
    def inline_repl(match):
        math_expr = match.group(1).strip()
        encoded = urllib.parse.quote(math_expr)
        return f'<img src="https://latex.codecogs.com/svg.image?\\color{{black}}{encoded}" alt="{math_expr}" style="vertical-align: middle; height: 1.2em;" />'

    full_markdown = re.sub(r'\$\$(.*?)\$\$', block_repl, full_markdown, flags=re.DOTALL)
    full_markdown = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', inline_repl, full_markdown)

    # Convert Markdown to HTML
    # We use extensions to support tables, footnotes, and code blocks
    html_body = markdown.markdown(
        full_markdown, 
        extensions=['tables', 'fenced_code', 'footnotes', 'nl2br']
    )
    
    # Wrap in a full HTML document with custom CSS for the PDF
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Systems & Intelligence</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono&display=swap');
            
            @page {{
                size: A4;
                margin: 2.5cm;
                @bottom-center {{
                    content: counter(page);
                    font-family: 'Inter', sans-serif;
                    font-size: 9pt;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: 'Inter', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #222;
            }}
            
            h1, h2, h3, h4 {{
                font-family: 'Outfit', sans-serif;
                color: #111;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            
            h1 {{
                font-size: 24pt;
                font-weight: 700;
                border-bottom: 1px solid #ddd;
                padding-bottom: 0.2em;
                page-break-before: always;
            }}
            
            /* Special styling for the title page */
            h1:first-of-type {{
                font-size: 32pt;
                text-align: center;
                margin-top: 30%;
                border-bottom: none;
                page-break-before: avoid;
            }}
            
            h2:first-of-type {{
                text-align: center;
                font-weight: 400;
                color: #555;
            }}
            
            blockquote {{
                border-left: 4px solid #5e35b1;
                margin: 1.5em 0;
                padding: 0.5em 1em;
                background-color: #f8f9fa;
                font-style: italic;
                color: #444;
            }}
            
            code {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 9pt;
                background-color: #f1f3f5;
                padding: 0.1em 0.3em;
                border-radius: 3px;
            }}
            
            pre {{
                background-color: #1e1e1e;
                color: #d4d4d4;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
                page-break-inside: avoid;
            }}
            
            pre code {{
                background-color: transparent;
                color: inherit;
                padding: 0;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1.5em 0;
                page-break-inside: avoid;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }}
            
            th {{
                background-color: #f8f9fa;
                font-family: 'Outfit', sans-serif;
            }}
            
            a {{
                color: #5e35b1;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    print("Generating PDF from Markdown chapters...")
    font_config = FontConfiguration()
    HTML(string=html_content).write_pdf(
        output_filename, 
        font_config=font_config
    )
    print(f"Success! Book exported to {output_filename}")

if __name__ == "__main__":
    generate_pdf()
