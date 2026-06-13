#!/usr/bin/env python3
"""
Entry point for polyglot_tempo module.
"""

import sys
import os
from pathlib import Path

# Ensure workspace/AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_tempo.src.tempo import generate_tempo_map, format_tempo_card, run_tests


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = generate_tempo_map(rotate=True)
        print(format_tempo_card(result))
    else:
        print(f"Polyglot Tempo v1.0.0")
        print("  🎵  Rhythm Pattern Generator — the tempo and feel of languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_tempo --test    # Run all tests")
        print("  python -m polyglot_tempo --report  # Generate tempo report")