#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Phonetic Utilities Usage Examples
================================================

Demonstrates practical applications of phonetic encoding algorithms.

Applications:
    - Name matching and deduplication
    - Search with spelling tolerance
    - Genealogy and record linkage
    - Customer database deduplication
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import directly from mod.py in parent directory
import importlib.util
spec = importlib.util.spec_from_file_location("mod", os.path.join(parent_dir, "mod.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Use functions from mod
soundex = mod.soundex
soundex_words = mod.soundex_words
metaphone = mod.metaphone
double_metaphone = mod.double_metaphone
nysiis = mod.nysiis
caverphone = mod.caverphone
match_rating_codex = mod.match_rating_codex
soundex_match = mod.soundex_match
double_metaphone_match = mod.double_metaphone_match
phonetic_similarity = mod.phonetic_similarity
encode_all = mod.encode_all
find_phonetic_matches = mod.find_phonetic_matches
batch_encode = mod.batch_encode
PhoneticAlgorithm = mod.PhoneticAlgorithm


def example_basic_encoding():
    """
    Example 1: Basic phonetic encoding.
    
    Shows how different names are encoded by various algorithms.
    """
    print("=" * 60)
    print("Example 1: Basic Phonetic Encoding")
    print("=" * 60)
    
    names = [
        "Smith", "Schmidt", "Smythe",
        "Johnson", "Jonson", "Johnston",
        "Catherine", "Katherine", "Kathryn",
        "O'Connor", "Connor", "Oconnor"
    ]
    
    print("\nName          Soundex  Metaphone  Double Metaphone  NYSIIS")
    print("-" * 60)
    
    for name in names:
        result = encode_all(name)
        dm = result.double_metaphone
        dm_str = f"{dm[0]}/{dm[1]}" if dm[1] else dm[0]
        print(f"{name:<12} {result.soundex:<8} {result.metaphone:<10} {dm_str:<16} {result.nysiis}")
    
    print("\n" + "-" * 60)


def example_name_deduplication():
    """
    Example 2: Name deduplication in a customer database.
    
    Shows how phonetic encoding can identify duplicate names
    that are spelled differently.
    """
    print("\n" + "=" * 60)
    print("Example 2: Customer Database Deduplication")
    print("=" * 60)
    
    # Sample customer names with potential duplicates
    customers = [
        "John Smith",
        "Jon Smith",
        "John Smythe",
        "J. Smith",
        "Johnny Smith",
        "Robert Johnson",
        "Rupert Johnson",
        "Rob Johnston",
        "Catherine Williams",
        "Katherine Williams",
        "Kate Williams",
        "William Jones",
        "Will Jones",
        "Bill Jones"
    ]
    
    print("\nAnalyzing customer list for potential duplicates...")
    print("-" * 60)
    
    # Use Double Metaphone for more accurate matching
    potential_duplicates = []
    
    for i, name1 in enumerate(customers):
        for name2 in customers[i + 1:]:
            similarity = phonetic_similarity(name1, name2)
            if similarity >= 0.6:
                potential_duplicates.append((name1, name2, similarity))
    
    print("\nPotential duplicates found:")
    for name1, name2, score in sorted(potential_duplicates, key=lambda x: -x[2])[:10]:
        print(f"  {name1} <-> {name2}  (similarity: {score:.1%})")
    
    print(f"\nTotal potential duplicates: {len(potential_duplicates)}")


def example_genealogy_matching():
    """
    Example 3: Genealogy - Finding surname variations.
    
    Demonstrates how phonetic encoding helps find name variations
    in historical records.
    """
    print("\n" + "=" * 60)
    print("Example 3: Genealogy - Surname Variations")
    print("=" * 60)
    
    # Historical surname variations
    surname_variations = {
        "Smith": ["Smith", "Smyth", "Smythe", "Schmidt", "Schmitt"],
        "Johnson": ["Johnson", "Jonson", "Johnston", "Johnstone"],
        "Williams": ["Williams", "Williamson", "Willims", "Willems"],
        "Brown": ["Brown", "Browne", "Broun"],
        "Davis": ["Davis", "Davies", "Davison", "Davidson"]
    }
    
    for original, variations in surname_variations.items():
        print(f"\nSurname: {original}")
        print(f"  Soundex codes: {[soundex(v) for v in variations]}")
        print(f"  Metaphone codes: {[metaphone(v) for v in variations]}")
        
        # Show which variations match
        matches = [v for v in variations if soundex_match(original, v)]
        print(f"  Soundex matches: {matches}")


def example_search_tolerance():
    """
    Example 4: Search with spelling tolerance.
    
    Shows how phonetic encoding enables fuzzy name search.
    """
    print("\n" + "=" * 60)
    print("Example 4: Search with Spelling Tolerance")
    print("=" * 60)
    
    # Employee database
    employees = [
        "John Smith",
        "Jane Doe",
        "Robert Johnson",
        "Emily Williams",
        "Michael Brown",
        "Sarah Davis",
        "David Wilson",
        "Jennifer Miller",
        "Christopher Moore",
        "Amanda Taylor"
    ]
    
    search_queries = [
        "Jhn Smth",      # Missing vowels
        "Jon Smith",     # Spelling variation
        "Rupert Johnson", # Different first name, same Soundex
        "Katherine Williams", # Known variation
    ]
    
    print("\nSearching employee database with spelling tolerance...")
    print("-" * 60)
    
    for query in search_queries:
        print(f"\nSearch: '{query}'")
        matches = find_phonetic_matches(query, employees, 
                                        PhoneticAlgorithm.DOUBLE_METAPHONE,
                                        threshold=0.3)
        for match, score in matches[:3]:
            print(f"  -> {match} (score: {score:.1%})")


def example_algorithm_comparison():
    """
    Example 5: Comparing different phonetic algorithms.
    
    Shows strengths and weaknesses of each algorithm.
    """
    print("\n" + "=" * 60)
    print("Example 5: Algorithm Comparison")
    print("=" * 60)
    
    test_pairs = [
        ("Smith", "Schmidt"),
        ("Catherine", "Katherine"),
        ("Brian", "Bryan"),
        ("Gene", "Jean"),
        ("Sean", "Shawn"),
        ("O'Connor", "Connor"),
    ]
    
    algorithms = [
        ("Soundex", PhoneticAlgorithm.SOUNDEX),
        ("Metaphone", PhoneticAlgorithm.METAPHONE),
        ("Double Metaphone", PhoneticAlgorithm.DOUBLE_METAPHONE),
        ("NYSIIS", PhoneticAlgorithm.NYSIIS),
        ("Caverphone", PhoneticAlgorithm.CAVERPHONE),
        ("MRC", PhoneticAlgorithm.MATCH_RATING_CODEX),
    ]
    
    print("\nName pair              Algorithm matches:")
    print("-" * 60)
    
    for name1, name2 in test_pairs:
        matches = []
        for alg_name, alg in algorithms:
            if phonetic_match(name1, name2, alg):
                matches.append(alg_name)
        
        print(f"{name1} vs {name2:<10}  {matches if matches else 'None'}")


def example_batch_processing():
    """
    Example 6: Batch processing large name lists.
    
    Shows efficient encoding of many names at once.
    """
    print("\n" + "=" * 60)
    print("Example 6: Batch Processing")
    print("=" * 60)
    
    # Large list of names
    names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Anderson", "Thomas", "Jackson", "White", "Harris",
        "Martin", "Thompson", "Garcia", "Martinez", "Robinson"
    ]
    
    print(f"\nBatch encoding {len(names)} names...")
    print("-" * 60)
    
    # Batch encode with different algorithms
    soundex_codes = batch_encode(names, PhoneticAlgorithm.SOUNDEX)
    metaphone_codes = batch_encode(names, PhoneticAlgorithm.METAPHONE)
    
    # Find unique codes (shows clustering)
    unique_soundex = len(set(soundex_codes.values()))
    unique_metaphone = len(set(metaphone_codes.values()))
    
    print(f"\nSoundex: {unique_soundex} unique codes for {len(names)} names")
    print(f"Metaphone: {unique_metaphone} unique codes for {len(names)} names")
    
    # Show clustering by Soundex
    print("\nSoundex code clusters:")
    code_to_names = {}
    for name, code in soundex_codes.items():
        code_to_names.setdefault(code, []).append(name)
    
    for code, clustered_names in sorted(code_to_names.items()):
        if len(clustered_names) > 1:
            print(f"  {code}: {clustered_names}")


def example_similarity_analysis():
    """
    Example 7: Detailed similarity analysis.
    
    Shows similarity scores between names.
    """
    print("\n" + "=" * 60)
    print("Example 7: Similarity Analysis")
    print("=" * 60)
    
    names = ["Smith", "Schmidt", "Smythe", "Jones", "Smithson"]
    
    print("\nSimilarity matrix:")
    print("-" * 60)
    
    # Header
    print("         ", end="")
    for name in names:
        print(f"{name[:6]:>8}", end="")
    print()
    
    # Matrix
    for name1 in names:
        print(f"{name1[:6]:<8}", end="")
        for name2 in names:
            score = phonetic_similarity(name1, name2)
            print(f"{score:>7.0%}", end=" ")
        print()


def example_real_world_scenario():
    """
    Example 8: Real-world scenario - Merging contact lists.
    
    Shows how to merge multiple contact lists while avoiding duplicates.
    """
    print("\n" + "=" * 60)
    print("Example 8: Merging Contact Lists")
    print("=" * 60)
    
    # Two contact lists to merge
    contacts_list_a = [
        ("John Smith", "john.smith@email.com"),
        ("Jane Doe", "jane.doe@email.com"),
        ("Robert Johnson", "rob.j@email.com"),
    ]
    
    contacts_list_b = [
        ("Jon Smith", "jon.smith@email.com"),       # Duplicate
        ("J. Doe", "j.doe@email.com"),             # Duplicate
        ("Michael Brown", "m.brown@email.com"),    # New
        ("Catherine Williams", "c.w@email.com"),   # New
        ("Katherine Williams", "k.w@email.com"),   # Duplicate of Catherine
    ]
    
    print("\nList A contacts:")
    for name, email in contacts_list_a:
        print(f"  {name} ({email})")
    
    print("\nList B contacts:")
    for name, email in contacts_list_b:
        print(f"  {name} ({email})")
    
    # Find duplicates
    print("\nDuplicate analysis:")
    duplicates = []
    new_contacts = []
    
    for name_b, email_b in contacts_list_b:
        found_dup = False
        for name_a, email_a in contacts_list_a:
            similarity = phonetic_similarity(name_a, name_b)
            if similarity >= 0.7:
                duplicates.append((name_a, name_b, similarity))
                found_dup = True
                break
        if not found_dup:
            new_contacts.append((name_b, email_b))
    
    print("\nDuplicates to skip:")
    for name_a, name_b, score in duplicates:
        print(f"  '{name_b}' matches '{name_a}' ({score:.1%})")
    
    print("\nNew contacts to add:")
    for name, email in new_contacts:
        print(f"  {name} ({email})")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Phonetic Encoding Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_encoding()
    example_name_deduplication()
    example_genealogy_matching()
    example_search_tolerance()
    example_algorithm_comparison()
    example_batch_processing()
    example_similarity_analysis()
    example_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()