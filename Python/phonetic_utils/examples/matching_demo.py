#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matching and search examples for Phonetic Algorithm Utilities."""

import sys
sys.path.insert(0, '..')

from mod import (
    phonetic_match, phonetic_search, phonetic_similarity,
    group_by_phonetic, find_duplicates, PhoneticAlgorithm
)


def main():
    print("=" * 60)
    print("Phonetic Algorithms - Matching and Search Examples")
    print("=" * 60)
    
    print("\n--- Phonetic Matching ---")
    print("Check if names match phonetically:")
    
    pairs = [
        ("Robert", "Rupert"),
        ("Smith", "Schmidt"),
        ("Catherine", "Katherine"),
        ("Johnson", "Johnsen"),
        ("MacDonald", "McDonald"),
        ("Wilson", "Willson"),
        ("Smith", "John"),
        ("Robert", "William"),
    ]
    
    for name1, name2 in pairs:
        matches, similarity = phonetic_match(name1, name2)
        status = "✓ MATCH" if matches else "✗ NO MATCH"
        print(f"  {name1:12} vs {name2:12}: {status} (similarity: {similarity:.2f})")
    
    print("\n--- Phonetic Search ---")
    print("Search for phonetically similar names:")
    
    candidates = [
        "Smith", "Smyth", "Smithe", "Schmidt", "Schmitt",
        "John", "Johnson", "Johnsen", "Jonson",
        "Williams", "Wilson", "Willson",
        "Brown", "Browne"
    ]
    
    queries = ["Smith", "Johnson", "Wilson"]
    
    for query in queries:
        print(f"\n  Query: '{query}'")
        results = phonetic_search(query, candidates, threshold=0.5)
        for name, similarity in results[:5]:
            print(f"    - {name:12} (similarity: {similarity:.2f})")
    
    print("\n--- Phonetic Similarity ---")
    print("Calculate overall similarity using multiple algorithms:")
    
    pairs_for_similarity = [
        ("Robert", "Rupert"),
        ("Smith", "Smyth"),
        ("Catherine", "Katherine"),
        ("Smith", "John"),
    ]
    
    for name1, name2 in pairs_for_similarity:
        similarity = phonetic_similarity(name1, name2)
        print(f"  {name1:12} vs {name2:12}: {similarity:.2f}")
    
    print("\n--- Grouping by Phonetic Code ---")
    print("Group similar-sounding names together:")
    
    names = [
        "Robert", "Rupert", "Robin",
        "Smith", "Smyth", "Schmidt",
        "Johnson", "Johnsen", "Jonson",
        "Williams", "Wilson", "Willson",
    ]
    
    groups = group_by_phonetic(names)
    for code, group_names in sorted(groups.items())[:6]:
        print(f"  {code:10} -> {', '.join(group_names)}")
    
    print("\n--- Finding Duplicates ---")
    print("Identify phonetic duplicates in a list:")
    
    duplicate_list = [
        "Robert", "Rupert", "Smith", "Smyth", "Schmidt",
        "Johnson", "Johnsen", "John", "Wilson", "Willson"
    ]
    
    duplicates = find_duplicates(duplicate_list)
    if duplicates:
        print("  Potential duplicate groups:")
        for group in duplicates:
            print(f"    - {', '.join(group)}")
    else:
        print("  No duplicates found")
    
    print("\n--- Different Algorithms ---")
    print("Compare matching with different algorithms:")
    
    name1, name2 = "Smith", "Schmidt"
    
    algorithms = [
        PhoneticAlgorithm.SOUNDEX,
        PhoneticAlgorithm.METAPHONE,
        PhoneticAlgorithm.DOUBLE_METAPHONE,
        PhoneticAlgorithm.NYSIIS,
        PhoneticAlgorithm.CAVERPHONE,
    ]
    
    print(f"  Matching '{name1}' vs '{name2}':")
    for algo in algorithms:
        matches, similarity = phonetic_match(name1, name2, algo)
        status = "✓" if matches else "✗"
        print(f"    {algo.value:20}: {status} (similarity: {similarity:.2f})")
    
    print("\n" + "=" * 60)
    print("Examples completed!")


if __name__ == '__main__':
    main()