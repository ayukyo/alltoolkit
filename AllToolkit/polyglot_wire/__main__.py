#!/usr/bin/env python3
"""Entry point for polyglot_wire module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_wire import run_tests, wire, format_wire_text
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--wire":
        result = wire()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--text":
        result = wire()
        print(format_wire_text(result))
    else:
        print("Polyglot Wire v1.0.0")
        print("Usage:")
        print("  python -m polyglot_wire --test   # Run tests")
        print("  python -m polyglot_wire --wire   # Generate wire report (JSON)")
        print("  python -m polyglot_wire --text   # Generate wire report (text)")