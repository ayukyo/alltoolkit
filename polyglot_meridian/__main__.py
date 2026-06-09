#!/usr/bin/env python3
"""Entry point for polyglot_meridian module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_meridian import run_tests, meridian, generate_meridian_chart, calculate_distance, generate_all_positions
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--meridian":
        result = meridian()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--chart":
        lang = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = generate_meridian_chart(lang)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--distance":
        if len(sys.argv) < 4:
            print("Usage: --distance <lang_a> <lang_b>")
            sys.exit(1)
        result = calculate_distance(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--all":
        result = generate_all_positions()
        print(json.dumps(result, indent=2))
    else:
        print("🌡️ Polyglot Meridian v1.0.0")
        print("  🗺️  Map programming languages on spectral dimensions.")
        print("")
        print("Usage:")
        print("  python -m polyglot_meridian --test        # Run all tests")
        print("  python -m polyglot_meridian --meridian   # Generate for current language (with rotation)")
        print("  python -m polyglot_meridian --chart <lang>  # Generate chart for specific language")
        print("  python -m polyglot_meridian --distance <a> <b>  # Calculate distance between two languages")
        print("  python -m polyglot_meridian --all        # Generate all 8 language positions")