"""
Webview UI controller.
Creates the PyWebView window and registers API methods.
"""

import webview
from pathlib import Path
from typing import Optional

from src.core.editor import MarkdownEditor
from src.core.settings import Settings


class EditorAPI:
    """API layer exposing editor functionality to JavaScript."""

    def __init__(self, editor: MarkdownEditor, settings: Settings):
        self.editor = editor
        self.settings = settings

    def get_markdown_files(self) -> list[dict]:
        """Get list of markdown files from the working directory/folder."""
        cwd = self.settings.config_path.parent  # default folder
        folder = getattr(self.editor, "_workspace", Path.cwd())
        folder = Path(folder)
        files = []
        try:
            for f in sorted(folder.glob("*.md")):
                files.append({
                    "path": str(f),
                    "name": f.name,
                    "active": str(f) == str(self.editor.current_path) if self.editor.current_path else False,
                })
            for f in sorted(folder.rglob("*.md")):
                rel = f.relative_to(folder)
                if len(rel.parts) > 1:
                    files.append({
                        "path": str(f),
                        "name": str(rel),
                        "active": str(f) == str(self.editor.current_path) if self.editor.current_path else False,
                    })
        except OSError:
            pass
        return files

    def load_file(self, path: str) -> dict:
        """Load a markdown file and return its content."""
        if self.editor.load_file(path):
            return {"success": True, "content": self.editor.get_content(), "path": path}
        return {"success": False, "error": "Failed to load file"}

    def save_file(self, path: Optional[str] = None) -> bool:
        """Save current content. If path provided, use it."""
        if not hasattr(self, "_last_js_content") or self._last_js_content is None:
            pass  # content already in editor
        content = getattr(self, "_last_js_content", None)
        if content is not None:
            self.editor.set_content(content)
        if path:
            return self.editor.save_as(path)
        return self.editor.save_file()

    def update_content(self, content: str):
        """Receive content changes from the JS editor."""
        self.editor.set_content(content)
        self._last_js_content = content
        self.settings  # keep ref alive

    def set_content(self, content: str):
        """Set the editor content (called from JS)."""
        self._last_js_content = content

    def create_file(self, name: str) -> bool:
        """Create a new markdown file with empty content."""
        folder = getattr(self.editor, "_workspace", Path.cwd())
        folder = Path(folder)
        path = folder / name
        try:
            path.write_text("# New Document\n\nStart writing your markdown here...\n", encoding="utf-8")
            self.editor.current_path = path
            self.editor.set_content("# New Document\n\nStart writing your markdown here...\n")
            self._last_js_content = self.editor.get_content()
            return True
        except OSError as e:
            print(f"Error creating file: {e}")
            return False

    def render_preview(self) -> str:
        """Render markdown preview HTML."""
        content = getattr(self, "_last_js_content", None)
        if content is not None:
            self.editor.set_content(content)
        return self.editor.render_preview()

    def export_html(self) -> str:
        """Export content as HTML."""
        content = getattr(self, "_last_js_content", None)
        if content is not None:
            self.editor.set_content(content)
        return self.editor.export_html()

    def set_theme(self, theme: str):
        """Set the preview theme."""
        self.settings.theme = theme
        self.settings.save()

    def get_stats(self) -> dict:
        """Get document statistics."""
        content = getattr(self, "_last_js_content", "")
        return {
            "characters": len(content),
            "words": len([w for w in content.split() if w.strip()]),
            "lines": len(content.splitlines()),
        }

    def minimize(self):
        print("minimize")

    def maximize(self):
        print("maximize")

    def close(self):
        print("close")

    def open_folder_dialog(self) -> Optional[str]:
        """Open a folder dialog to select workspace."""
        try:
            return self.editor.open_folder_dialog()
        except Exception:
            return None

    # --- Window controls (no-op on pywebview; handled by HTML titlebar) ---
    def noop(self) -> str:
        return ""


def get_html_path() -> Path:
    """Get path to the HTML file."""
    return Path(__file__).parent / "app.html"


def create_window(editor: MarkdownEditor, settings: Settings) -> webview.Window:
    """Create and configure the webview window."""
    api = EditorAPI(editor, settings)

    window = webview.create_window(
        title="Markdown Editor",
        html=get_html_path().read_text(encoding="utf-8"),
        js_api=api,
        width=1400,
        height=900,
        min_size=(800, 600),
        resizable=True,
        fullscreen=False,
        background_color="#1e1e1e",
        text_select=True,
        draggable=True,  # custom titlebar dragging enabled
    )

    return window
