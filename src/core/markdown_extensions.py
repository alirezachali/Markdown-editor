"""
Custom mistune extensions for the markdown editor.
Includes code blocks, tables, task lists, and link handling.
"""

from typing import Any, Dict, Optional


def create_extensions() -> list[str]:
    """Create list of mistune extension names."""
    return [
        "tables",      # GitHub-flavored tables
        "strikethrough",  # ~~strikethrough~~
        "autolink",    # http://... and email autolinking
        "tasklists",   # - [ ] task items
        "sane_lists",  # better list handling
    ]


def create_code_renderer():
    """Create a custom code block renderer that supports language detection."""
    from mistune import escape

    def code_block(self, token: Any) -> str:
        """Render code blocks with syntax highlighting support."""
        language = token.get("language", "") or ""
        content = escape(token["text"], True)

        # Handle indented code blocks (no fence)
        if language:
            return f'<div class="custom-code-block" data-language="{language}"><pre><code class="hljs language-{language}">{content}</code></pre></div>'
        else:
            return f'<div class="custom-code-block"><pre><code class="hljs">{content}</code></pre></div>'

    return code_block


def create_link_renderer():
    """Create link renderer with external link handling."""
    from mistune import escape

    def link(self, token: Any) -> str:
        """Render links, opening external links in new tab."""
        title = token.get("title")
        href = escape(token["url"], True)
        text = escape(token["text"], True)

        attrs = []
        if href.startswith(("http://", "https://", "mailto:")):
            attrs.append('target="_blank"')
            attrs.append('rel="noopener noreferrer"')

        if title:
            attrs.append(f'title="{escape(title, True)}"')

        return f'<a href="{href}" {" ".join(attrs)}>{text}</a>'

    return link
