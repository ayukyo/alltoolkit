#!/usr/bin/env python3
"""Entry point for polyglot_cartographer module."""

import sys
import os
from pathlib import Path

# Ensure workspace/AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_cartographer.src.cartographer import (
    generate_world_report,
    format_world_report,
    run_tests,
)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = generate_world_report(rotate=True)
        print(format_world_report(result))
    else:
        print(f"Polyglot Cartographer v1.0.0")
        print("  🗺️  Geopolitical World Map of Programming Languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_cartographer --test    # Run all tests")
        print("  python -m polyglot_cartographer --report  # Generate world report")