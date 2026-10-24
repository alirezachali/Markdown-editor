"""
Main application entry point.
Starts the PyWebView window with the markdown editor interface.
"""

import webview
from pathlib import Path

from src.core.editor import MarkdownEditor
from src.core.settings import Settings
from src.webview.ui import create_window


def main():
    """Initialize and run the Markdown Editor application."""
    settings = Settings()
    editor = MarkdownEditor(settings=settings)

    # Create the main window (PyWebView will use the API + HTML)
    window = create_window(editor, settings)

    print("Markdown Editor started successfully!")
    print(f"Window title: {window.title}")
    print(f"Working directory: {Path.cwd()}")
    print(f"HTML loaded: {Path(window.url).name if window.url else 'from html string'}")

    # Start the webview event loop
    webview.start()


if __name__ == "__main__":
    main()
