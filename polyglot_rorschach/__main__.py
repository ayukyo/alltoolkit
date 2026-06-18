#!/usr/bin/env python3
"""Entry point for polyglot_rorschach module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_rorschach import (
    rorschach,
    format_rorschach,
    get_current_language,
    advance_rotation,
    run_tests,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        lang, idx = get_current_language()
        print(f"Current language: {lang}")
        print(f"Index: {idx}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--card":
        result = rorschach()
        print(format_rorschach(result))

    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = rorschach()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif len(sys.argv) > 1 and sys.argv[1] == "--lang":
        if len(sys.argv) < 3:
            print("Usage: --lang <language>")
            sys.exit(1)
        result = rorschach(sys.argv[2])
        print(format_rorschach(result))

    else:
        result = rorschach()
        print(format_rorschach(result))
