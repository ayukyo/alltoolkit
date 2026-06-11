#!/usr/bin/env python3
"""Entry point for polyglot_sentinel module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_sentinel import (
    run_tests,
    run,
    get_current_language,
    advance_rotation,
    generate_sentinel_report,
    format_report,
)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        lang = sys.argv[2] if len(sys.argv) > 2 else None
        if lang:
            prev = get_current_language()
            report = generate_sentinel_report(lang, previous_language=prev)
            print(format_report(report))
        else:
            print(run())
    else:
        print(run())