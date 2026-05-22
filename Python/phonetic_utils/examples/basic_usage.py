#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basic usage examples for Phonetic Algorithm Utilities."""

import sys
sys.path.insert(0, '..')

from mod import (
    soundex, metaphone, double_metaphone, caverphone,
    nysiis, match_rating_codex, encode_all
)


def main():
    print("=" * 60)
    print("Phonetic Algorithms - Basic Usage Examples")
    print("=" * 60)
    
    # Example names
    names = ["Robert", "Rupert", "Smith", "Schmidt", "Catherine", "Katherine"]
    
    print("\n--- Soundex Encoding ---")
    print("Standard US Census Soundex encoding:")
    for name in names:
        result = soundex(name)
        print(f"  {name:15} -> {result.primary}")
    
    print("\n--- Metaphone Encoding ---")
    print("Improved Soundex with English pronunciation rules:")
    for name in names:
        result = metaphone(name)
        print(f"  {name:15} -> {result.primary}")
    
    print("\n--- Double Metaphone Encoding ---")
    print("Handles multiple possible pronunciations:")
    for name in names:
        result = double_metaphone(name)
        if result.alternate:
            print(f"  {name:15} -> {result.primary} (alternate: {result.alternate})")
        else:
            print(f"  {name:15} -> {result.primary}")
    
    print("\n--- Caverphone Encoding ---")
    print("10-character codes for NZ electoral rolls:")
    for name in names[:4]:
        result = caverphone(name)
        print(f"  {name:15} -> {result.primary}")
    
    print("\n--- NYSIIS Encoding ---")
    print("New York State Identification System:")
    for name in names:
        result = nysiis(name)
        print(f"  {name:15} -> {result.primary}")
    
    print("\n--- Match Rating Codex ---")
    print("Simplified encoding for name matching:")
    for name in names:
        result = match_rating_codex(name)
        print(f"  {name:15} -> {result.primary}")
    
    print("\n--- All Algorithms Comparison ---")
    print("Compare all encodings for a single name:")
    name = "Schmidt"
    results = encode_all(name)
    for algo, result in results.items():
        print(f"  {algo:20} -> {result}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")


if __name__ == '__main__':
    main()