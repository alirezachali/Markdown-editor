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
    print("Window created. Starting webview...")

    # Log state for debugging
    html_path = Path(__file__).parent / "webview" / "app.html"
    print(f"HTML file exists: {html_path.exists()}")
    print("Starting webview...")

    # Start the webview event loop
    try:
        webview.start(gui="edge")
    except Exception as e:
        import traceback
        print(f"Error starting webview edge, falling back: {e}")
        try:
            webview.start(gui="chromium")
        except Exception as e2:
            print(f"Error starting webview chromium: {e2}")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
