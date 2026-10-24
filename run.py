"""Debug launcher - logs startup info to a file."""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.settings import Settings
from src.webview.ui import EditorAPI
from src.core.editor import MarkdownEditor

log_file = PROJECT_ROOT / "startup_log.txt"
log_content = []

try:
    import webview
    log_content.append(f"pywebview imported OK: {webview.__version__ if hasattr(webview, '__version__') else 'unknown'}")

    settings = Settings()
    editor = MarkdownEditor(settings=settings)
    log_content.append("Editor initialized OK")

    from src.webview.ui import create_window
    window = create_window(editor, settings)

    log_content.append("Window created OK")
    log_content.append(f"HTML file exists: {(Path(__file__).parent / 'src/webview/app.html').exists()}")

    # Write HTML test to verify
    html = editor.render_preview()
    log_content.append(f"Markdown render OK - HTML length: {len(html)}")

    log_content.append("Starting webview...")

except Exception as e:
    import traceback
    log_content.append(f"ERROR: {e}")
    log_content.append(traceback.format_exc())

# Write log
log_file.write_text("\n".join(log_content), encoding="utf-8")
print("\n".join(log_content))
print(f"\nLog written to: {log_file}")
print("If window didn't appear, check the log above.")
