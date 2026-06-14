#!/usr/bin/env python3
"""
Polyglot Pulse CLI entry point.
Usage: python -m polyglot_pulse [--test|--pulse [language]]
"""

import sys
import json
from polyglot_pulse import measure_pulse, load_rotation, run_tests


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--pulse":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        if language:
            result = measure_pulse(language)
            print(json.dumps(result, indent=2))
        else:
            config = load_rotation()
            current = config["languages"][config["current_index"]]
            result = measure_pulse(current)
            print(json.dumps(result, indent=2))
    else:
        print("💓 Polyglot Pulse v1.0.0")
        print("Usage:")
        print("  python -m polyglot_pulse --test         # Run test suite")
        print("  python -m polyglot_pulse --pulse         # Measure current language")
        print("  python -m polyglot_pulse --pulse Rust    # Measure specific language")


if __name__ == "__main__":
    main()