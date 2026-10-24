"""Basic tests for all core components."""

import tempfile
from pathlib import Path

from src.core.editor import MarkdownEditor
from src.core.settings import Settings
from src.core.markdown import parse_markdown


class TestSettings:
    def test_defaults(self):
        s = Settings()
        assert s.theme == "dark"
        assert s.auto_save is True
        assert s.font_size == 14

    def test_save_load(self, tmp_path):
        s = Settings()
        s.config_path = tmp_path / "config.json"
        s.theme = "light"
        s.save()
        loaded = Settings(config_path=tmp_path / "config.json")
        assert loaded.theme == "light"


class TestMarkdownParser:
    def test_heading(self):
        html = parse_markdown("# Hello World")
        assert "<h1>" in html
        assert "Hello World" in html

    def test_bold_italic(self):
        html = parse_markdown("**Bold** and _italic_")
        assert "<strong>" in html
        assert "<em>" in html

    def test_code_block(self):
        code = 'print("hello")'
        html = parse_markdown("```python\n" + code + "\n```")
        assert "<pre>" in html
        assert "highlight" in html or "hljs" in html

    def test_table(self):
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        html = parse_markdown(md)
        assert "<table>" in html

    def test_rtl_detection(self):
        html = parse_markdown("# سلام دنیا")
        assert 'dir="rtl"' in html

    def test_external_link(self):
        html = parse_markdown('[Google](https://google.com)')
        assert 'target="_blank"' in html
        assert 'rel="noopener' in html


class TestEditor:
    def test_set_get_content(self):
        s = Settings()
        e = MarkdownEditor(s)
        e.set_content("# Test")
        assert e.get_content() == "# Test"

    def test_load_save_file(self, tmp_path):
        s = Settings()
        e = MarkdownEditor(s)
        test_file = tmp_path / "test.md"
        test_file.write_text("# Hello")
        assert e.load_file(test_file)
        assert e.get_content() == "# Hello"

    def test_new_file(self):
        s = Settings()
        e = MarkdownEditor(s)
        e.set_content("content")
        e.new_file()
        assert e.get_content() == ""
        assert e.current_path is None

    def test_export_html(self, tmp_path):
        s = Settings()
        e = MarkdownEditor(s)
        e.set_content("# Hello")
        html = e.export_html()
        assert "Hello" in html
        assert "<h1>" in html


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
