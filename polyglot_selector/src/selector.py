"""Polyglot Selector — rotates through languages and generates challenges."""

from pathlib import Path

from .config import load_config, save_config
from .challenges import generate_challenge


def select_next_language(config_path: str, seed=None):
    """Read the rotation config, advance to the next language, and return the result.

    Steps:
        1. Load language_rotation.json
        2. Compute new_index = (current_index + 1) % len(languages)
        3. Select the language at new_index
        4. Save updated config back to disk
        5. Generate a challenge for the selected language
        6. Return result dict

    Args:
        config_path: Path to language_rotation.json.
        seed: Optional random seed for deterministic challenge generation.

    Returns:
        {
            "previous_language": str,
            "current_language": str,
            "current_index": int,
            "challenge": Challenge
        }
    """
    data = load_config(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    previous_language = languages[current_index]

    new_index = (current_index + 1) % len(languages)
    current_language = languages[new_index]

    # Update and persist config
    data["current_index"] = new_index
    data["last_language"] = current_language
    from datetime import datetime, timezone
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_config(config_path, data)

    try:
        challenge = generate_challenge(current_language, seed=seed)
    except ValueError:
        # Language not in LANGUAGE_FEATURES — still valid for rotation, just no challenge
        challenge = None

    return {
        "previous_language": previous_language,
        "current_language": current_language,
        "current_index": new_index,
        "challenge": challenge,
    }


def main() -> None:
    """CLI entry point."""
    config_path = str(Path(__file__).parent.parent.parent / "language_rotation.json")
    result = select_next_language(config_path)
    print("Language rotation: {} → {}".format(result['previous_language'], result['current_language']))
    print("Index: {}".format(result['current_index']))
    print("Challenge: {}".format(result['challenge'].description))