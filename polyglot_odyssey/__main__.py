#!/usr/bin/env python3
"""Entry point for polyglot_odyssey module."""

import sys
import os

# Ensure workspace/AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_odyssey.src import (
    TOOL_NAME,
    TOOL_VERSION,
    odyssey,
    format_odyssey_report,
    run_tests,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = odyssey(rotate=True)
        print(format_odyssey_report(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = odyssey(rotate=True)
        print(json.dumps(result, indent=2))
    else:
        print(f"🚀 Polyglot Odyssey v{TOOL_VERSION}")
        print("  A time-travel journey through programming language history.")
        print("")
        print("Usage:")
        print("  python -m polyglot_odyssey --test    # Run all tests")
        print("  python -m polyglot_odyssey --report  # Generate journey report")
        print("  python -m polyglot_odyssey --json    # JSON output")
