"""
AllToolkit - Python Fuzzy Search Utilities Examples

Demonstrates various use cases for fuzzy string matching.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Distance functions
    levenshtein_distance,
    levenshtein_ratio,
    damerau_levenshtein_distance,
    jaro_distance,
    jaro_winkler_distance,
    
    # N-gram functions
    ngram_similarity,
    dice_coefficient,
    
    # Phonetic functions
    soundex,
    metaphone,
    phonetic_similarity,
    
    # Search functions
    fuzzy_search,
    fuzzy_find,
    extract_best,
    extract_top_n,
    
    # Advanced matching
    partial_ratio,
    token_sort_ratio,
    token_set_ratio,
    weighted_ratio,
    
    # Classes and utilities
    FuzzyMatcher,
    deduplicate,
    suggest_corrections,
)


def example_distance_functions():
    """Example: Using distance functions."""
    print("=" * 60)
    print("Distance Functions Examples")
    print("=" * 60)
    
    # Levenshtein distance
    print("\n1. Levenshtein Distance:")
    pairs = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
        ("book", "back"),
    ]
    for s1, s2 in pairs:
        distance = levenshtein_distance(s1, s2)
        ratio = levenshtein_ratio(s1, s2)
        print(f"   '{s1}' vs '{s2}': distance={distance}, ratio={ratio:.2f}")
    
    # Damerau-Levenshtein (supports transposition)
    print("\n2. Damerau-Levenshtein (supports transposition):")
    print(f"   'abc' vs 'acb': lev={levenshtein_distance('abc', 'acb')}, "
          f"damerau={damerau_levenshtein_distance('abc', 'acb')}")
    
    # Jaro-Winkler distance
    print("\n3. Jaro-Winkler Distance:")
    names = [("MARTHA", "MARHTA"), ("JONES", "JOHNSON")]
    for s1, s2 in names:
        jaro = jaro_distance(s1, s2)
        jw = jaro_winkler_distance(s1, s2)
        print(f"   '{s1}' vs '{s2}': jaro={jaro:.3f}, jaro_winkler={jw:.3f}")


def example_ngram_similarity():
    """Example: Using n-gram similarity."""
    print("\n" + "=" * 60)
    print("N-gram Similarity Examples")
    print("=" * 60)
    
    pairs = [
        ("hello", "hallo"),
        ("programming", "programmer"),
        ("database", "databse"),  # typo
    ]
    
    for s1, s2 in pairs:
        ngram = ngram_similarity(s1, s2)
        dice = dice_coefficient(s1, s2)
        print(f"   '{s1}' vs '{s2}': ngram={ngram:.2f}, dice={dice:.2f}")


def example_phonetic_matching():
    """Example: Using phonetic matching."""
    print("\n" + "=" * 60)
    print("Phonetic Matching Examples")
    print("=" * 60)
    
    # Soundex - homophone detection
    print("\n1. Soundex (homophone detection):")
    names = [
        ("Robert", "Rupert"),
        ("Smith", "Smythe"),
        ("Ashcraft", "Ashcroft"),
    ]
    for s1, s2 in names:
        print(f"   '{s1}' ({soundex(s1)}) vs '{s2}' ({soundex(s2)})")
    
    # Metaphone - better phonetic encoding
    print("\n2. Metaphone:")
    words = [("phone", "fone"), ("write", "rite"), ("Smith", "Schmidt")]
    for s1, s2 in words:
        print(f"   '{s1}' ({metaphone(s1)}) vs '{s2}' ({metaphone(s2)})")
    
    # Phonetic similarity
    print("\n3. Phonetic Similarity:")
    pairs = [("Robert", "Rupert"), ("hello", "world")]
    for s1, s2 in pairs:
        sim = phonetic_similarity(s1, s2)
        print(f"   '{s1}' vs '{s2}': {sim:.2f}")


def example_fuzzy_search():
    """Example: Basic fuzzy search."""
    print("\n" + "=" * 60)
    print("Fuzzy Search Examples")
    print("=" * 60)
    
    # Dictionary for search
    fruits = ["apple", "banana", "orange", "grape", "pineapple", "strawberry"]
    
    # Search with typo
    print("\n1. Search with typo:")
    results = fuzzy_search("aple", fruits, threshold=0.6)
    for match in results:
        print(f"   {match}")
    
    # Search with different algorithms
    print("\n2. Compare algorithms:")
    query = "bananna"  # typo
    for algo in ["levenshtein", "jaro_winkler", "ngram", "phonetic"]:
        results = fuzzy_search(query, fruits, algorithm=algo, threshold=0.5)
        best = results[0] if results else None
        print(f"   {algo}: best match = {best.value if best else 'None'} "
              f"(score: {best.score if best else 0:.2f})")
    
    # Find best match
    print("\n3. Find best match:")
    best = fuzzy_find("orenge", fruits, threshold=0.6)
    print(f"   'orenge' -> '{best}'")


def example_advanced_matching():
    """Example: Advanced matching techniques."""
    print("\n" + "=" * 60)
    print("Advanced Matching Examples")
    print("=" * 60)
    
    # Partial ratio - substring matching
    print("\n1. Partial Ratio (substring matching):")
    pairs = [
        ("hello", "hello world"),
        ("world", "hello world"),
        ("xyz", "hello world"),
    ]
    for s1, s2 in pairs:
        ratio = partial_ratio(s1, s2)
        print(f"   '{s1}' in '{s2}': {ratio:.2f}")
    
    # Token sort ratio - word order independence
    print("\n2. Token Sort Ratio (word order independent):")
    pairs = [
        ("hello world", "world hello"),
        ("Python is great", "great is Python"),
    ]
    for s1, s2 in pairs:
        ratio = token_sort_ratio(s1, s2)
        print(f"   '{s1}' vs '{s2}': {ratio:.2f}")
    
    # Token set ratio - duplicate handling
    print("\n3. Token Set Ratio (ignores duplicates):")
    pairs = [
        ("hello hello world", "world hello"),
        ("quick brown fox", "fox brown quick"),
    ]
    for s1, s2 in pairs:
        ratio = token_set_ratio(s1, s2)
        print(f"   '{s1}' vs '{s2}': {ratio:.2f}")
    
    # Weighted ratio - combination of metrics
    print("\n4. Weighted Ratio:")
    pairs = [("hello world", "hallo world"), ("Python code", "Python coding")]
    for s1, s2 in pairs:
        ratio = weighted_ratio(s1, s2)
        print(f"   '{s1}' vs '{s2}': {ratio:.2f}")


def example_fuzzy_matcher():
    """Example: Using FuzzyMatcher class."""
    print("\n" + "=" * 60)
    print("FuzzyMatcher Class Examples")
    print("=" * 60)
    
    # Create matcher with dictionary
    words = [
        "python", "programming", "program", "programmer",
        "code", "coding", "coder", "developer",
        "javascript", "java", "ruby", "rust",
    ]
    matcher = FuzzyMatcher(words)
    
    print(f"\nMatcher initialized with {matcher.count} candidates")
    
    # Search examples
    print("\n1. Search for 'progrming' (typo):")
    results = matcher.search("progrming", threshold=0.6, limit=5)
    for match in results:
        print(f"   {match.value}: {match.score:.2f}")
    
    print("\n2. Search for 'javscript' (typo):")
    results = matcher.search("javscript", threshold=0.6)
    for match in results:
        print(f"   {match.value}: {match.score:.2f}")
    
    # Add new candidates
    print("\n3. Adding new candidates:")
    matcher.add_candidates(["typescript", "golang"])
    print(f"   New count: {matcher.count}")
    
    # Search for new candidates
    results = matcher.search("typescrip", threshold=0.7)
    for match in results:
        print(f"   {match.value}: {match.score:.2f}")
    
    # Find best match quickly
    print("\n4. Quick find:")
    best = matcher.find("codr", threshold=0.7)
    print(f"   'codr' -> '{best}'")


def example_spell_correction():
    """Example: Spell correction suggestions."""
    print("\n" + "=" * 60)
    print("Spell Correction Examples")
    print("=" * 60)
    
    # English dictionary (partial)
    dictionary = [
        "apple", "banana", "orange", "grape", "strawberry",
        "blueberry", "raspberry", "blackberry", "kiwi",
        "mango", "papaya", "pineapple", "coconut",
        "watermelon", "melon", "peach", "plum",
    ]
    
    # Common typos
    typos = ["appel", "bananna", "orenge", "stawberry", "pineaple"]
    
    print("\nSuggesting corrections for typos:")
    for typo in typos:
        suggestions = suggest_corrections(typo, dictionary, max_suggestions=3)
        suggestion_str = ", ".join([f"{s[0]}({s[1]:.2f})" for s in suggestions])
        print(f"   '{typo}' -> {suggestion_str}")


def example_deduplicate():
    """Example: Deduplicating similar strings."""
    print("\n" + "=" * 60)
    print("Deduplication Examples")
    print("=" * 60)
    
    # List with similar names
    names = [
        "John Smith", "J. Smith", "John S.", "Smith John",
        "Jane Doe", "J. Doe", "Jane D.",
        "Robert Johnson", "R. Johnson", "Bob Johnson",
    ]
    
    print(f"\nOriginal list: {names}")
    
    # Group similar names
    groups = deduplicate(names, threshold=0.7)
    
    print("\nGrouped similar names:")
    for i, group in enumerate(groups, 1):
        print(f"   Group {i}: {group}")


def example_real_world_use():
    """Example: Real-world use case - command matching."""
    print("\n" + "=" * 60)
    print("Real-world Example: Command Matching")
    print("=" * 60)
    
    # Valid commands
    commands = [
        "help", "exit", "quit", "status", "info",
        "start", "stop", "restart", "pause", "resume",
        "config", "settings", "options", "debug",
        "list", "show", "display", "clear", "reset",
    ]
    
    matcher = FuzzyMatcher(commands)
    
    # User inputs with typos
    inputs = ["hlep", "exiit", "statu", "startt", "confg", "lst"]
    
    print("\nMatching user commands:")
    for input_cmd in inputs:
        best = matcher.find(input_cmd, threshold=0.7)
        if best:
            print(f"   '{input_cmd}' -> '{best}'")
        else:
            suggestions = extract_top_n(input_cmd, commands, n=2, threshold=0.5)
            if suggestions:
                print(f"   '{input_cmd}' -> No match. Did you mean: {suggestions}")
            else:
                print(f"   '{input_cmd}' -> Unknown command")


def example_contact_search():
    """Example: Contact name search."""
    print("\n" + "=" * 60)
    print("Contact Search Example")
    print("=" * 60)
    
    contacts = [
        "John Smith", "Jane Doe", "Robert Johnson",
        "Emily Brown", "Michael Wilson", "Sarah Davis",
        "David Martinez", "Jennifer Anderson", "Thomas Taylor",
    ]
    
    matcher = FuzzyMatcher(contacts)
    
    # Search by partial name
    queries = ["john", "jane d", "robert j", "wilson", "taylor tom"]
    
    print("\nSearching contacts:")
    for query in queries:
        results = matcher.search(query, threshold=0.6, limit=3)
        print(f"   '{query}' matches:")
        for match in results:
            print(f"      {match.value}: {match.score:.2f}")


def main():
    """Run all examples."""
    example_distance_functions()
    example_ngram_similarity()
    example_phonetic_matching()
    example_fuzzy_search()
    example_advanced_matching()
    example_fuzzy_matcher()
    example_spell_correction()
    example_deduplicate()
    example_real_world_use()
    example_contact_search()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()