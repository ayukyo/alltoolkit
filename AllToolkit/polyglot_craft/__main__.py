#!/usr/bin/env python3
"""
Entry point for polyglot_craft module.
"""

import sys
import os
from pathlib import Path

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_craft.src.craft import generate_craft_card, format_craft_card, run_tests


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--card":
        card = generate_craft_card()
        print(format_craft_card(card))
    else:
        print(f"Polyglot Craft v1.0.0")
        print("  🛠️  Language Crafting Recipes — practical skill cards.")
        print("")
        print("Usage:")
        print("  python -m polyglot_craft --test   # Run all tests")
        print("  python -m polyglot_craft --card   # Generate craft card")
