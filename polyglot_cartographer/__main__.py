#!/usr/bin/env python3
"""Entry point for polyglot_cartographer module."""
from . import generate_world_report, format_world_report, run_tests
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_world_report()
        print(format_world_report(report))
    else:
        print("Polyglot Cartographer v1.0.0")
        print("Usage:")
        print("  python -m polyglot_cartographer --test   # Run tests")
        print("  python -m polyglot_cartographer --report # Generate world report")