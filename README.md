# Markdown Editor

A modern, native Markdown editor for Windows built with Python and PyWebView. Features live preview, syntax highlighting, RTL support for Persian, and a distraction-free writing experience.

## Screenshots

![Editor Screenshot](docs/screenshot.png)

## Features

### Writing
- 📝 **Live Preview** – Real-time rendering with syntax highlighting
- 🖋️ **Syntax Highlighting** – Powered by Pygments for 50+ languages
- 🔤 **RTL Support** – Full Persian/Farsi Markdown support with auto-detection
- 👁️ **Distraction-Free Mode** – Hide the sidebar or go full-screen
- 🔄 **Split View & Focus Modes** – Switch between editor-only, split, or preview-only

### File Management
- 📂 **File Browser** – Navigate your markdown files directly
- 💾 **Auto-save** – Never lose your work
- 📤 **Export to HTML** – Share polished documents

### Themes
- 🌙 **Dark Mode** – Easy on the eyes
- ☀️ **Light Mode** – Clean, GitHub-inspired theme
- 🎨 **Customizable** – Adjustable font size & sidebar width

## Getting Started

### Prerequisites
- Python 3.10+
- Windows 10/11 (WebView2 Runtime included with Edge)

### Installation

```bash
git clone https://github.com/alirezachali/Markdown-editor.git
cd Markdown-editor
pip install -r requirements.txt
```

### Running

```bash
python -m src.app
```

## Building a Standalone Executable

To create a Windows `.exe` without requiring Python:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "src\webview\app.html;src\webview" src/app.py --name "Markdown Editor"
```

## Project Structure

```
Markdown-editor/
├── src/
│   ├── app.py               # Entry point
│   ├── core/
│   │   ├── editor.py        # File ops & state
│   │   ├── markdown.py      # Markdown → HTML renderer
│   │   ├── settings.py      # Configurable settings
│   │   └── markdown_extensions.py
│   └── webview/
│       ├── app.html         # Frontend UI
│       └── ui.py            # Webview controller/API
├── assets/                  # Icons, images
├── docs/                    # Documentation
├── tests/                   # Unit tests
├── requirements.txt
└── README.md
```

## License

MIT License – see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) first.
