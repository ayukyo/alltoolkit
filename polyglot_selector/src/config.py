"""Configuration reader and writer for language_rotation.json."""

import json
from pathlib import Path


def load_config(path: str) -> dict:
    """Load and parse a JSON configuration file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path: str, data: dict) -> None:
    """Serialize a dictionary to a JSON file with pretty formatting."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")