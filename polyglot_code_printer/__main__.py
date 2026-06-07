#!/usr/bin/env python3
"""Entry point for polyglot_code_printer module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_code_printer import run_tests, generate_code_print, format_printable
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--print":
        result = generate_code_print()
        print(format_printable(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = generate_code_print()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Code Printer v1.0.0")
        print("Usage:")
        print("  python -m polyglot_code_printer --test   # Run tests")
        print("  python -m polyglot_code_printer --print  # Generate code print")
        print("  python -m polyglot_code_printer --json   # Generate JSON output")