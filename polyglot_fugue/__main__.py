#!/usr/bin/env python3
"""Entry point for polyglot_fugue module."""

import sys
import os
from pathlib import Path

# Ensure workspace/AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_fugue.src.fugue import fugue, format_fugue, run_tests


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--format":
        result = fugue()
        print(format_fugue(result))
    else:
        result = fugue()
        print(format_fugue(result))
