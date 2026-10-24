"""Markdown editor core logic - file operations, markdown parsing, export."""

import re
import threading
import time
from pathlib import Path
from typing import Callable, Optional


class MarkdownEditor:
    """Core markdown editor logic."""

    def __init__(self, settings):
        self.settings = settings
        self.current_path: Optional[Path] = None
        self.content = ""
        self.unsaved = False
        self._lock = threading.Lock()
        self._save_callbacks: list[Callable] = []
        self._change_callbacks: list[Callable] = []

    # ---------- Content management ----------

    def set_content(self, content: str):
        """Set the editor content and notify UI of changes."""
        with self._lock:
            self.content = content
            self.unsaved = True
            self._notify_change()

    def get_content(self) -> str:
        with self._lock:
            return self.content

    def append_content(self, content: str):
        with self._lock:
            self.content += content
            self.unsaved = True
            self._notify_change()

    def clear(self):
        with self._lock:
            self.content = ""
            self.unsaved = True
            self._notify_change()

    # ---------- File operations ----------

    def new_file(self):
        """Create a new empty file."""
        with self._lock:
            self.content = ""
            self.current_path = None
            self.unsaved = True
            self._notify_change()

    def load_file(self, path: str | Path) -> bool:
        """Load a markdown file. Returns True on success."""
        path = Path(path)
        try:
            content = path.read_text(encoding="utf-8")
            with self._lock:
                self.content = content
                self.current_path = path
                self.unsaved = False
                self._notify_change()
            return True
        except (OSError, UnicodeDecodeError) as e:
            print(f"Error loading file {path}: {e}")
            return False

    def save_file(self) -> bool:
        """Save current content to file. Returns True on success."""
        if self.current_path is None:
            return False
        try:
            Path(self.current_path).write_text(self.content, encoding="utf-8")
            with self._lock:
                self.unsaved = False
            return True
        except OSError as e:
            print(f"Error saving file {self.current_path}: {e}")
            return False

    def save_as(self, path: str | Path) -> bool:
        """Save content to a new path."""
        path = Path(path)
        try:
            path.write_text(self.content, encoding="utf-8")
            with self._lock:
                self.current_path = path
                self.unsaved = False
                self._notify_change()
            return True
        except OSError as e:
            print(f"Error saving as {path}: {e}")
            return False

    def export_html(self, output_path: Optional[str | Path] = None) -> Optional[str]:
        """Export content to HTML. Optionally save to file."""
        from src.core.markdown import parse_markdown

        html = parse_markdown(self.content)
        if output_path:
            Path(output_path).write_text(html, encoding="utf-8")
        return html

    # ---------- Live preview ----------

    def render_preview(self) -> str:
        """Convert markdown to HTML for live preview."""
        from src.core.markdown import parse_markdown

        return parse_markdown(self.content)

    def render_preview_raw(self) -> str:
        """Get raw HTML without document wrapper."""
        from src.core.markdown import parse_markdown

        return parse_markdown(self.content, wrapped=False)

    # ---------- Undo/Redo ----------

    def undo(self) -> bool:
        return False

    def redo(self) -> bool:
        return False

    # ---------- Callbacks ----------

    def on_change(self, callback: Callable):
        """Register a callback for content changes."""
        self._change_callbacks.append(callback)

    def on_save(self, callback: Callable):
        """Register a callback for save events."""
        self._save_callbacks.append(callback)

    def _notify_change(self):
        for callback in self._change_callbacks:
            try:
                callback(self.content)
            except Exception as e:
                print(f"Change callback error: {e}")

    # ---------- Auto-save ----------

    def start_auto_save(self, interval: Optional[int] = None):
        """Start automatic saving."""
        interval = interval or self.settings.auto_save_interval
        threading.Thread(target=self._auto_save_loop, args=(interval,), daemon=True).start()

    def stop_auto_save(self):
        pass  # Thread is daemon, will stop when app exits

    def _auto_save_loop(self, interval: int):
        while True:
            time.sleep(interval)
            if self.current_path and self.unsaved:
                self.save_file()
