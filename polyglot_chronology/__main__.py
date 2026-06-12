#!/usr/bin/env python3
"""CLI entry point for polyglot_chronology module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_chronology import (
    run_tests,
    get_current_language,
    get_epoch_for_language,
    generate_temporal_map,
    format_epoch_card,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        lang = get_current_language()
        print(f"Current language: {lang}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--epoch":
        lang = sys.argv[2] if len(sys.argv) > 2 else get_current_language()
        epoch = get_epoch_for_language(lang)
        if epoch:
            print(json.dumps(epoch, indent=2, ensure_ascii=False))
        else:
            print(f"No epoch data for language: {lang}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--map":
        result = generate_temporal_map(rotate=True)
        card = format_epoch_card(result)
        print(card)

    elif len(sys.argv) > 1 and sys.argv[1] == "--map-no-rotate":
        result = generate_temporal_map(rotate=False)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print("🗺️  Polyglot Chronology v1.0.0")
        print("   Temporal Cartography — programming languages as geological eras.")
        print("")
        print("Usage:")
        print("  python -m polyglot_chronology --test            # Run all tests")
        print("  python -m polyglot_chronology --current         # Show current language (no rotation)")
        print("  python -m polyglot_chronology --epoch [lang]     # Show epoch for a language")
        print("  python -m polyglot_chronology --map              # Generate temporal map (rotates)")
        print("  python -m polyglot_chronology --map-no-rotate    # Generate map without rotating")