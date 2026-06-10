#!/usr/bin/env python3
"""Entry point for polyglot_ecosystem_map module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_ecosystem_map import (
    run_tests,
    calculate_relationship,
    find_ecosystem_neighbors,
    generate_ecosystem_map,
    get_rotation_state,
    rotate_and_update,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--map":
        # Generate ecosystem map for current rotated language
        result = rotate_and_update()
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        # Show current language without rotating
        state = get_rotation_state()
        idx = state["current_index"]
        lang = state["languages"][idx]
        print(f"Current language: {lang}")
        print(f"Index: {idx}/{len(state['languages'])-1}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--neighbors":
        lang = sys.argv[2] if len(sys.argv) > 2 else None
        if not lang:
            print("Usage: --neighbors <language>")
            sys.exit(1)
        result = find_ecosystem_neighbors(lang, top_n=5)
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--rel":
        if len(sys.argv) < 4:
            print("Usage: --rel <lang_a> <lang_b>")
            sys.exit(1)
        result = calculate_relationship(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--ecosystem":
        lang = sys.argv[2] if len(sys.argv) > 2 else None
        if not lang:
            print("Usage: --ecosystem <language>")
            sys.exit(1)
        result = generate_ecosystem_map(lang)
        print(json.dumps(result, indent=2))

    else:
        print("🗺️  Polyglot Ecosystem Map v1.0.0")
        print("   Map programming language ecosystems and relationships.")
        print("")
        print("Usage:")
        print("  python -m polyglot_ecosystem_map --test          # Run all tests")
        print("  python -m polyglot_ecosystem_map --map           # Generate map for current rotated language")
        print("  python -m polyglot_ecosystem_map --current       # Show current language")
        print("  python -m polyglot_ecosystem_map --neighbors <lang>  # Find ecosystem neighbors")
        print("  python -m polyglot_ecosystem_map --rel <a> <b>   # Calculate relationship between two languages")
        print("  python -m polyglot_ecosystem_map --ecosystem <lang>  # Generate full ecosystem map for a language")