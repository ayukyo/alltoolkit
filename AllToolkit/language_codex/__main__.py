#!/usr/bin/env python3
"""Entry point for Language Codex module."""
from language_codex import run_tests, reveal
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--reveal":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        if language:
            result = reveal(language)
        else:
            # Auto-detect from rotation
            from language_codex import load_rotation
            config = load_rotation()
            language = config["languages"][config["current_index"]]
            result = reveal(language)
        print(json.dumps(result, indent=2))
    else:
        from language_codex import TOOL_NAME, TOOL_VERSION
        print(f"Language Codex v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_codex --test       # Run tests")
        print("  python -m language_codex --reveal [lang]  # Reveal hidden syntax")