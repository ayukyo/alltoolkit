#!/usr/bin/env python3
"""Entry point for polyglot_weather module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_weather import (
    run_tests,
    rotate_and_update,
    get_rotation_language,
    collision_forecast,
    generate_ecosystem_barometer,
    get_seasonal_pattern,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--weather":
        result = rotate_and_update()
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        lang = get_rotation_language()
        print(f"Current language: {lang}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--collision":
        if len(sys.argv) < 4:
            print("Usage: --collision <lang_a> <lang_b>")
            sys.exit(1)
        result = collision_forecast(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--barometer":
        result = generate_ecosystem_barometer()
        print(json.dumps(result, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "--seasonal":
        lang = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = get_seasonal_pattern(lang)
        print(json.dumps(result, indent=2))

    else:
        print("🌦️  Polyglot Weather v1.0.0")
        print("   Language weather forecasting — atmospheric pressure systems.")
        print("")
        print("Usage:")
        print("  python -m polyglot_weather --test           # Run all tests")
        print("  python -m polyglot_weather --weather       # Generate weather report for current language")
        print("  python -m polyglot_weather --current        # Show current language (no rotation)")
        print("  python -m polyglot_weather --collision <a> <b>  # Collision forecast between two languages")
        print("  python -m polyglot_weather --barometer      # Ecosystem-wide barometric readings")
        print("  python -m polyglot_weather --seasonal [lang]  # Seasonal pattern for a language")
