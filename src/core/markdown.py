"""
Markdown to HTML conversion using mistune 3.x
"""

from functools import lru_cache
from pathlib import Path

import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from mistune.directives import Admonition

# HTML wrapper template
HTML_WRAPPER_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --bg: #ffffff;
            --text: #1a1a1a;
            --code-bg: #f5f5f5;
            --border: #e0e0e0;
            --accent: #0078d4;
        }}
        [data-theme="dark"] {{
            --bg: #1e1e1e;
            --text: #e0e0e0;
            --code-bg: #252526;
            --border: #3c3c3c;
            --accent: #0078d4;
        }}
        body {{
            font-size: {font_size}px;
            line-height: 1.6;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 45px 20px;
            max-width: 980px;
            margin-left: auto;
            margin-right: auto;
        }}
        .markdown-body {{
            box-sizing: border-box;
        }}
        pre {{
            border-radius: 6px;
            background: var(--code-bg);
            border: 1px solid var(--border);
            padding: 16px;
            overflow-x: auto;
        }}
        pre code {{
            background: transparent;
            padding: 0;
            font-size: 13px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        }}
        code {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: var(--code-bg);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 85%;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid var(--border);
            padding: 8px 12px;
            text-align: right;
        }}
        th {{
            background: var(--code-bg);
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}
        a {{
            color: var(--accent);
        }}
        h1, h2, h3, h4, h5, h6 {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.3em;
            margin-top: 24px;
        }}
        blockquote {{
            border-right: 4px solid var(--accent);
            padding: 10px 16px;
            margin: 16px 0;
            background: var(--code-bg);
            border-radius: 0 4px 4px 0;
        }}
    </style>
</head>
<body data-theme="{theme}" class="markdown-body">
    {content}
</body>
</html>"""

THEME_CSS = {
    "dark": "#1e1e1e",
    "light": "#ffffff",
}


def get_syntax_highlighter():
    """Return a syntax highlighter renderer."""
    formatter = HtmlFormatter(nowrap=True, cssclass="highlight")

    def highlight_code(code: str, language: str) -> str:
        if not language:
            return code
        try:
            lexer = get_lexer_by_name(language)
        except Exception:
            try:
                lexer = guess_lexer_for_filename(f"file.{language}", code)
            except Exception:
                return code
        return highlight(code, lexer, formatter)

    return highlight_code


class HighlightedRenderer(mistune.HTMLRenderer):
    """Custom renderer with syntax highlighting for code blocks."""

    def __init__(self, highlight_func=None):
        super().__init__()
        self.highlight = highlight_func or get_syntax_highlighter()

    def block_code(self, code, info=None):
        language = info or ""
        highlighted = self.highlight(code, language)
        classes = "highlight"
        if language:
            classes += f" language-{language}"
        return f'<pre class="{classes}"><code class="{classes}">{highlighted}</code></pre>\n'

    def inline_code(self, code):
        return f'<code class="highlight">{mistune.escape(code)}</code>'


def get_plugins():
    """Get list of mistune plugin names."""
    return [
        "url",
        "table",
        "footnotes",
        "task_lists",
        "def_list",
        "speedup",
    ]


@lru_cache(maxsize=128)
def create_markdown_renderer(theme: str = "dark"):
    """Create a configured markdown renderer."""
    plugins = get_plugins()

    # Directives for advanced Markdown features
    directives = [Admonition()]

    md = mistune.create_markdown(
        renderer=HighlightedRenderer(get_syntax_highlighter()),
        plugins=plugins,
        hard_wrap=True,
    )
    return md


@lru_cache(maxsize=128)
def parse_markdown(markdown_text: str, *, theme: str = "dark", font_size: int = 16, wrapped: bool = True) -> str:
    """Parse markdown text into HTML."""
    if not markdown_text:
        markdown_text = ""

    md = create_markdown_renderer(theme=theme)
    html_content = md(markdown_text)

    # Post-process: ensure links open in new tab
    import re
    html_content = re.sub(
        r'<a href="((?:https?|mailto):[^"]+)"',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        html_content,
    )

    if not wrapped:
        return html_content

    direction = "rtl" if "ی" in markdown_text or "ک" in markdown_text else "ltr"

    return HTML_WRAPPER_TEMPLATE.format(
        content=html_content,
        title="Markdown Preview",
        theme=theme,
        direction=direction,
        font_size=font_size,
    )


def parse_file(file_path: str | Path, *, theme: str = "dark") -> str:
    """Parse a markdown file into HTML."""
    markdown_text = Path(file_path).read_text(encoding="utf-8")
    return parse_markdown(markdown_text, theme=theme)
