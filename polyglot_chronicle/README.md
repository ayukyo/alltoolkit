# 📜 Polyglot Chronicle v1.0

A "language daily chronicle" — creates a daily diary entry for the current rotation language featuring on-this-day history, a themed coding challenge, a creator quote, and a community mood assessment.

## Features

- **On This Day**: Notable version releases, first commits, RFCs, and landmark events that happened on today's date across all years
- **Daily Challenge**: A themed coding challenge with difficulty rating and tags
- **Creator Quote**: A motivational quote from a language creator or influential figure
- **Language Mood**: A community mood assessment — how the community feels today
- **Age Tracking**: Computes the age of each language from its birth year
- **Rotation Support**: Automatically advances the next language via `language_rotation.json`

## Installation

```bash
cd polyglot_chronicle
python -m polyglot_chronicle --help
```

## Usage

```bash
# Run tests
python -m polyglot_chronicle --test

# Generate today's chronicle for the current rotation language
python -m polyglot_chronicle --chronicle

# Generate for a specific language
python -c "from polyglot_chronicle import chronicle; import json; print(json.dumps(chronicle(language='Rust'), indent=2))"
```

## API

### `chronicle(language=None, force_today=None)`

Generates a daily chronicle for the selected language.

- **language** (str, optional): Override the selected language (for testing)
- **force_today** (datetime, optional): Override today's date (for testing reproducibility)

Returns a dict with the following keys:

```python
{
    "tool": "polyglot-chronicle",
    "version": "1.0.0",
    "selected_language": "Rust",
    "emoji": "🦀",
    "age_years": 11,
    "date": "2026-06-21",
    "date_human": "June 21, 2026",
    "on_this_day": ["2026 — ..."],
    "daily_challenge": {"title": "...", "difficulty": "⭐⭐⭐", "tags": [...]},
    "creator_quote": "...",
    "community_mood": "...",
    "next_language": "Go",
    "rotation": ["Rust", "Go", ...],
    "timestamp": "2026-06-21T00:00:00+08:00"
}
```

### Helper Functions

- `get_on_this_day(language, today)` — Returns "On This Day" events for the given language
- `get_daily_challenge(language, seed=None)` — Selects a daily challenge (deterministic if seed given)
- `get_quote(language)` — Returns a random motivational quote
- `get_mood(language)` — Returns a community mood
- `load_rotation()` — Loads the rotation config
- `save_rotation(data)` — Saves the rotation config

## Languages Covered

Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

Each language has 12+ history events, 5+ challenges, 3+ quotes, and 2+ moods.

## Module Structure

```
polyglot_chronicle/
├── __init__.py             # Core module with HISTORY_EVENTS, DAILY_CHALLENGES, etc.
├── __main__.py             # CLI entry point (--test, --chronicle)
└── README.md
```

## Testing

```bash
# Module's own test suite
python -m polyglot_chronicle --test

# Pytest test suite
python -m pytest polyglot_chronicle/tests/ -v
```
