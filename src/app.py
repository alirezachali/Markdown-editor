"""
Main application entry point.
Starts the PyWebView window with the markdown editor interface.
"""

import webview

from src.core.editor import MarkdownEditor
from src.core.settings import Settings
from src.webview.ui import create_window


def main():
    """Initialize and run the Markdown Editor application."""
    settings = Settings()
    editor = MarkdownEditor(settings=settings)

    # Create the main window (PyWebView will use the API + HTML)
    window = create_window(editor, settings)

    # Start the webview event loop
    webview.start()


if __name__ == "__main__":
    main()
