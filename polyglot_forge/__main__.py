#!/usr/bin/env python3
"""CLI entry point for polyglot_forge module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_forge.src.forge import (
    ROTATION_FILE,
    get_current_language,
    advance_rotation,
    generate_forge_card,
    format_alloy_card,
)
import json


def run_tests() -> None:
    """Run the full test suite."""
    import pytest
    import sys as _sys
    _sys.exit(pytest.main(["-v", str(__file__.replace("__main__.py", "tests"))]))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    elif len(sys.argv) > 1 and sys.argv[1] == "--current":
        lang = get_current_language(ROTATION_FILE)
        print(f"Current language: {lang}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--card":
        result = generate_forge_card(ROTATION_FILE)
        print(format_alloy_card(result))

    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = generate_forge_card(ROTATION_FILE)
        # Convert AlloyCard to dict for JSON serialization
        card = result["alloy_card"]
        out = {
            "current_language": result["current_language"],
            "pairing_language": result["pairing_language"],
            "alloy_card": {
                "primary_language": card.primary_language,
                "secondary_language": card.secondary_language,
                "primary_element": card.primary_element,
                "secondary_element": card.secondary_element,
                "alloy_name": card.alloy_name,
                "compatibility_score": card.compatibility_score,
                "tier": card.tier,
                "forge_process": card.forge_process,
                "primary_properties": card.primary_properties,
                "secondary_properties": card.secondary_properties,
                "alloy_strength": card.alloy_strength,
                "recommended_applications": card.recommended_applications,
            },
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))

    else:
        print("⚒️  Polyglot Forge v1.0.0")
        print("   Language Alloy Workshop — forging code from paired languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_forge --test     # Run all tests")
        print("  python -m polyglot_forge --current # Show current language")
        print("  python -m polyglot_forge --card    # Forge alloy card")
        print("  python -m polyglot_forge --json    # Output card as JSON")
