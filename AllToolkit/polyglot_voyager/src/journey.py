"""Polyglot Voyager — tracks multi-stop learning journeys across languages.

A creative tool that logs each language visit in a journey.json file,
builds a "passport" of visited languages with timestamps, and provides
a map of the polyglot ecosystem showing which languages have been
visited on the journey so far.
"""

import json
import os
import random
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_ROTATION_CONFIG = str(
    Path(__file__).parent.parent.parent.parent / "language_rotation.json"
)
DEFAULT_JOURNEY_LOG = str(
    Path(__file__).parent.parent.parent.parent / "AllToolkit" / "polyglot_voyager" / "journey.json"
)


def _load_rotation_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_journey_log(log_path: str, data: Dict[str, Any]) -> None:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_journey_log(log_path: str) -> Dict[str, Any]:
    if not Path(log_path).exists():
        return {"journey": [], "total_visits": 0, "languages_visited": []}
    with open(log_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------


def get_journey_snapshot(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Return the current language based on the rotation index.

    Reads language_rotation.json and returns the language at
    current_index without modifying the index.

    Args:
        config_path: Path to language_rotation.json.
                     Defaults to workspace root.

    Returns:
        {
            "current_language": str,
            "current_index": int,
            "last_language": str,
            "updated_at": str,
            "total_languages": int
        }
    """
    if config_path is None:
        config_path = DEFAULT_ROTATION_CONFIG

    data = _load_rotation_config(config_path)
    languages = data["languages"]
    idx = data["current_index"]

    return {
        "current_language": languages[idx],
        "current_index": idx,
        "last_language": data.get("last_language", ""),
        "updated_at": data.get("updated_at", ""),
        "total_languages": len(languages),
    }


def advance_and_log(
    config_path: Optional[str] = None,
    journey_log_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Advance the rotation index, log the visit, and return journey metadata.

    This is the main creative function:
      1. Reads current index from language_rotation.json
      2. Advances the index to the next language (circular rotation)
      3. Writes the updated index back to language_rotation.json
      4. Appends a visit record to journey.json

    Args:
        config_path: Path to language_rotation.json.
        journey_log_path: Path to journey.json.

    Returns:
        {
            "previous_language": str,
            "current_language": str,
            "current_index": int,
            "journey": List[Dict],   # last 5 visits
            "languages_visited": List[str],
            "total_visits": int,
            "passport_stamps": List[str]  # emoji stamps for each visit
        }
    """
    if config_path is None:
        config_path = DEFAULT_ROTATION_CONFIG
    if journey_log_path is None:
        journey_log_path = DEFAULT_JOURNEY_LOG

    # 1. Read and advance rotation
    data = _load_rotation_config(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    previous_language = languages[current_index]
    new_index = (current_index + 1) % len(languages)
    current_language = languages[new_index]

    # 2. Persist updated rotation
    data["current_index"] = new_index
    data["last_language"] = current_language
    data["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 3. Log the visit
    journey = _load_journey_log(journey_log_path)

    stamp = _emoji_stamp(current_language)
    visit_record = {
        "language": current_language,
        "index": new_index,
        "visited_at": datetime.now(timezone.utc).isoformat(),
        "stamp": stamp,
    }
    journey["journey"].append(visit_record)
    journey["total_visits"] += 1

    if current_language not in journey["languages_visited"]:
        journey["languages_visited"].append(current_language)

    # Keep only last 20 visits in memory; full log persists
    recent = journey["journey"][-20:]
    journey["journey"] = recent

    _save_journey_log(journey_log_path, journey)

    # 4. Build passport stamps (last 10)
    passport_stamps = [v["stamp"] for v in journey["journey"][-10:]]

    return {
        "previous_language": previous_language,
        "current_language": current_language,
        "current_index": new_index,
        "journey": journey["journey"][-5:],
        "languages_visited": journey["languages_visited"],
        "total_visits": journey["total_visits"],
        "passport_stamps": passport_stamps,
    }


def get_polyglot_map(
    journey_log_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Return a map of visited vs unvisited languages.

    Args:
        journey_log_path: Path to journey.json.

    Returns:
        {
            "visited": List[str],
            "not_yet_visited": List[str],
            "total_visits": int,
            "map_legend": Dict[str, str]
        }
    """
    if journey_log_path is None:
        journey_log_path = DEFAULT_JOURNEY_LOG

    journey = _load_journey_log(journey_log_path)
    visited = journey.get("languages_visited", [])

    # Full ecosystem list
    all_languages = [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]
    not_yet = [lang for lang in all_languages if lang not in visited]

    return {
        "visited": visited,
        "not_yet_visited": not_yet,
        "total_visits": journey.get("total_visits", 0),
        "map_legend": {
            "visited": "🌍",
            "not_yet": "⚪",
        },
    }


def _emoji_stamp(language: str) -> str:
    """Return a unique emoji stamp for a language."""
    stamps = {
        "Rust": "🦀",
        "Go": "🐹",
        "Swift": "🦅",
        "Kotlin": "🧃",
        "TypeScript": "📘",
        "JavaScript": "📒",
        "Java": "☕",
        "C/C++": "⚙️",
    }
    return stamps.get(language, "🔮")


def main() -> None:
    """CLI entry point — advance rotation and display journey summary."""
    result = advance_and_log()

    print("=" * 50)
    print("  🧳 POLYGLOT VOYAGER — Journey Report")
    print("=" * 50)
    print(f"  Previous: {result['previous_language']}")
    print(f"  Current:  {result['current_language']} {result['journey'][-1]['stamp']}")
    print(f"  Index:    {result['current_index']}")
    print()
    print(f"  Total visits: {result['total_visits']}")
    print(f"  Languages visited: {', '.join(result['languages_visited'])}")
    print()
    print(f"  Passport stamps (recent):")
    stamps = " ".join(result["passport_stamps"])
    print(f"    {stamps}")
    print("=" * 50)
