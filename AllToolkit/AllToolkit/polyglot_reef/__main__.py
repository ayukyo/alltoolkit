#!/usr/bin/env python3
"""CLI entry point for polyglot_reef module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_reef import (
    run_tests,
    get_ecosystem_report,
    format_reef_report,
)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = get_ecosystem_report(rotate=True)
        card = format_reef_report(report)
        print(card)

    elif len(sys.argv) > 1 and sys.argv[1] == "--report-no-rotate":
        report = get_ecosystem_report(rotate=False)
        card = format_reef_report(report)
        print(card)

    else:
        print("🐚  Polyglot Reef v1.0.0")
        print("    Language Ecosystem Simulator — programming languages as species.")
        print("")
        print("Usage:")
        print("  python -m polyglot_reef --test              # Run all tests")
        print("  python -m polyglot_reef --report           # Generate ecosystem report (rotates)")
        print("  python -m polyglot_reef --report-no-rotate # Generate report (no rotation)")
