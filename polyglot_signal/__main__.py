#!/usr/bin/env python3
"""
Entry point for polyglot_signal module.
"""

import sys
import os
from pathlib import Path

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_signal.src.signal import generate_signal_report, format_signal_report, run_tests


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_signal_report()
        print(format_signal_report(report))
    else:
        print(f"Polyglot Signal v1.0.0")
        print("  🛰️  Signal Semantics Cartography — how languages communicate.")
        print("")
        print("Usage:")
        print("  python -m polyglot_signal --test    # Run all tests")
        print("  python -m polyglot_signal --report  # Generate signal report")