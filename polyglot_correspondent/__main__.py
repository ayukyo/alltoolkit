#!/usr/bin/env python3
"""Entry point for polyglot_correspondent."""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_correspondent.src.correspondent import (
    generate_correspondent_report,
    format_correspondent_report,
    run_tests,
)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_correspondent_report()
        print(format_correspondent_report(report))
    else:
        print(f"✉️  Polyglot Correspondent v1.0.0")
        print("  Epistolary Engine — every language writes letters differently.")
        print("")
        print("Usage:")
        print("  python -m polyglot_correspondent --test    # Run all tests")
        print("  python -m polyglot_correspondent --report  # Generate a letter from current language")
