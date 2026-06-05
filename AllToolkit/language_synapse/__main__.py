#!/usr/bin/env python3
"""Entry point for language_synapse module."""

import sys
from . import run_tests, find_synapses

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--synapse":
        import json
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = find_synapses(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language Synapse v1.0.0")
        print("Usage:")
        print("  python -m language_synapse --test        # Run tests")
        print("  python -m language_synapse --synapse [lang]  # Map neural pathways")