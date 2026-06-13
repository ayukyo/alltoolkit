#!/usr/bin/env python3
"""
Entry point for polyglot_chef module.
"""

import sys
import os
from pathlib import Path

# Ensure workspace/AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_chef.src.chef import (
    generate_station_report,
    format_station_card,
    run_tests,
)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = generate_station_report(rotate=True)
        print(format_station_card(result))
    else:
        print(f"Polyglot Chef v1.0.0")
        print("  🧑‍🍳  Kitchen Brigade Tribute to Programming Languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_chef --test    # Run all tests")
        print("  python -m polyglot_chef --report  # Generate station report")