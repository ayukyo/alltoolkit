#!/usr/bin/env python3
"""CLI entry point for polyglot_lexicon module."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_lexicon.src.lexicon import (
    run_tests,
    get_current_language,
    generate_lexicon_card,
    format_lexicon_entry,
)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--card":
        result = generate_lexicon_card()
        print(format_lexicon_entry(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        lang = get_current_language()
        print(f"Current language: {lang}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--entry":
        lang = sys.argv[2] if len(sys.argv) > 2 else get_current_language()
        from polyglot_lexicon.src.lexicon import generate_lexicon_card
        result = generate_lexicon_card(language=lang)
        print(format_lexicon_entry(result))
    else:
        print("📖 Polyglot Lexicon v1.0.0")
        print("   Programming languages as dictionary entries.")
        print("")
        print("Usage:")
        print("  python -m polyglot_lexicon --test    # Run all tests")
        print("  python -m polyglot_lexicon --card   # Generate lexicon card (rotates)")
        print("  python -m polyglot_lexicon --current  # Show current language")
        print("  python -m polyglot_lexicon --entry [lang]  # Show entry for a language")