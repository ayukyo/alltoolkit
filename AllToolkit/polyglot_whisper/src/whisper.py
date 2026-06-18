"""Polyglot Whisper — rotates through languages and generates insight cards."""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .cards import get_card


DEFAULT_ROTATION_CONFIG = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)


def load_rotation_config(config_path: str = DEFAULT_ROTATION_CONFIG) -> dict:
    """Load the language rotation JSON file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation_config(config_path: str, data: dict) -> None:
    """Persist the updated language rotation JSON file."""
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def rotate_and_whisper(
    config_path: str = DEFAULT_ROTATION_CONFIG,
    seed: Optional[int] = None,
) -> dict:
    """Read the rotation config, advance to the next language, update the config,
    generate an insight card, and return the result.

    Steps:
        1. Load language_rotation.json
        2. Compute new_index = (current_index + 1) % len(languages)
        3. Select the language at new_index
        4. Save updated config back to disk
        5. Generate an insight card for the selected language
        6. Return result dict

    Args:
        config_path: Path to language_rotation.json.
        seed: Optional random seed for deterministic card selection (future use).

    Returns:
        {
            "previous_language": str,
            "current_language": str,
            "current_index": int,
            "insight_card": {
                "idiom": str,
                "proverb": str,
                "quirk": str,
                "fun_fact": str,
                "syntax_gem": str,
                "philosophy": str,
            }
        }
    """
    data = load_rotation_config(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    previous_language = languages[current_index]

    new_index = (current_index + 1) % len(languages)
    current_language = languages[new_index]

    # Persist updated rotation state
    data["current_index"] = new_index
    data["last_language"] = current_language
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation_config(config_path, data)

    try:
        insight_card = get_card(current_language)
    except ValueError:
        # Language not in INSIGHT_CARDS — still valid for rotation, just no card
        insight_card = None

    return {
        "previous_language": previous_language,
        "current_language": current_language,
        "current_index": new_index,
        "insight_card": insight_card,
    }


def main() -> None:
    """CLI entry point — print the rotated language and its insight card."""
    result = rotate_and_whisper()

    card = result["insight_card"]
    print("=" * 60)
    print(f"  Language Rotation: {result['previous_language']} → {result['current_language']}")
    print(f"  Index: {result['current_index']}")
    print("=" * 60)

    if card:
        print(f"\n💬 Idiom:\n   {card['idiom']}")
        print(f"\n📜 Proverb:\n   {card['proverb']}")
        print(f"\n🧩 Quirk:\n   {card['quirk']}")
        print(f"\n🪄 Fun Fact:\n   {card['fun_fact']}")
        print(f"\n💎 Syntax Gem:\n   {card['syntax_gem']}")
        print(f"\n🌍 Philosophy:\n   {card['philosophy']}")
    else:
        print("\n⚠️  No insight card available for this language.")


if __name__ == "__main__":
    main()


# Convenience alias
generate_insight_card = rotate_and_whisper