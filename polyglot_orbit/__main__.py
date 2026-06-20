#!/usr/bin/env python3
"""Entry point for polyglot_orbit module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_orbit import (
    run_tests,
    orbit_report,
    get_current_language,
    find_conjunctions,
    rank_ecosystems,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--orbit":
        result = orbit_report()
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        lang = get_current_language()
        print(f"Current language: {lang}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--conjunction":
        if len(sys.argv) < 4:
            print("Usage: --conjunction <lang_a> <lang_b> [days]")
            sys.exit(1)
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 365
        result = find_conjunctions(sys.argv[2], sys.argv[3], days_ahead=days)
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--rank":
        result = rank_ecosystems()
        print(json.dumps(result, indent=2))

    else:
        print(f"🌌 Polyglot Orbit v1.0.0")
        print("   Celestial mechanics for programming languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_orbit --test           # Run all tests")
        print("  python -m polyglot_orbit --orbit        # Generate orbital report")
        print("  python -m polyglot_orbit --current       # Show current language (no rotation)")
        print("  python -m polyglot_orbit --conjunction <a> <b> [days]  # Find conjunctions")
        print("  python -m polyglot_orbit --rank          # Rank ecosystems by gravity")
