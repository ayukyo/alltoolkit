#!/usr/bin/env python3
"""Entry point for polyglot_oracle module."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_oracle import run_tests, oracle, format_oracle_reading, TOOL_NAME, TOOL_VERSION
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--oracle":
        result = oracle()
        print(format_oracle_reading(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = oracle()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Oracle v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_oracle --test    # Run tests")
        print("  python -m polyglot_oracle --oracle  # Get oracle reading")
        print("  python -m polyglot_oracle --json    # Get reading as JSON")
