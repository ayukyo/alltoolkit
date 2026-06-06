#!/usr/bin/env python3
"""Entry point for polyglot_flavor module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_flavor import flavor, run_tests
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = flavor()
        print(result["tasting_card"])
        print(f"\nOverall Score: {result['overall_score']}/5.0")
        print(f"Rotated at: {result['rotated_at']}")