"""Application settings and configuration."""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Settings:
    """Application settings managed through a JSON config file."""

    default_font: str = "Consolas"
    font_size: int = 14
    theme: str = "dark"
    auto_save: bool = True
    auto_save_interval: int = 30  # seconds
    live_preview: bool = True
    sidebar_width: int = 250
    tab_size: int = 4
    word_wrap: bool = False
    show_line_numbers: bool = True

    config_path: Path = field(default_factory=lambda: Path.home() / ".markdown_editor" / "config.json")

    def __post_init__(self):
        """Load settings from file if it exists."""
        if self.config_path.exists():
            try:
                data = json.loads(self.config_path.read_text(encoding="utf-8"))
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
            except (json.JSONDecodeError, OSError):
                # Fall back to defaults if config is invalid
                pass

    def save(self):
        """Save current settings to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "default_font": self.default_font,
            "font_size": self.font_size,
            "theme": self.theme,
            "auto_save": self.auto_save,
            "auto_save_interval": self.auto_save_interval,
            "live_preview": self.live_preview,
            "sidebar_width": self.sidebar_width,
            "tab_size": self.tab_size,
            "word_wrap": self.word_wrap,
            "show_line_numbers": self.show_line_numbers,
        }
        self.config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def from_file(cls, path: str | Path):
        """Create a Settings instance from a file path."""
        instance = cls.__new__(cls)
        instance.config_path = Path(path)
        instance.__post_init__()
        return instance
