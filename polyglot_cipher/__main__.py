#!/usr/bin/env python3
"""Entry point for polyglot_cipher module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_cipher import cipher, run_tests


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = cipher()
        print(result["cipher_card"])
        print(f"\nChallenge : {result['challenge']}")
        print(f"Encoded   : {result['encoded']}")
        print(f"Cipher    : {result['cipher_name']}")
        print(f"Key       : {result['key']}")
        print(f"Rotated at: {result['rotated_at']}")
