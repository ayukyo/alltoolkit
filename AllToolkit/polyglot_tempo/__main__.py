#!/usr/bin/env python3
"""CLI entry point for polyglot_tempo module."""

import sys
import os
import json

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_tempo import run_tests, tempo, generate_rhythm_report, format_rhythm_card


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = tempo()
        print(format_rhythm_card(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = tempo()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("🎵 Polyglot Tempo v1.0.0")
        print("   Rhythm Pattern Generator — programming languages as musical rhythms.")
        print("")
        print("Usage:")
        print("  python -m polyglot_tempo --test     # Run all tests")
        print("  python -m polyglot_tempo --report  # Human-readable rhythm card")
        print("  python -m polyglot_tempo --json     # JSON output")