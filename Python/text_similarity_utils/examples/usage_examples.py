#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Text Similarity Utilities Usage Examples

Demonstrates practical usage of text similarity functions.

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '..')

from mod import (
    levenshtein_distance, levenshtein_ratio,
    damerau_levenshtein_distance, hamming_distance,
    jaro_similarity, jaro_winkler_similarity,
    jaccard_similarity, dice_coefficient, overlap_coefficient,
    cosine_similarity, cosine_similarity_words,
    TFIDFCalculator,
    lcs, lcs_length, lcs_ratio,
    ngram_similarity,
    soundex, metaphone, phonetic_similarity,
    find_best_match, find_all_matches, fuzzy_search,
    combined_similarity, compare_strings,
    similar
)


def example_edit_distance():
    """Example: Edit distance comparisons."""
    print("\n" + "=" * 60)
    print("Edit Distance Examples")
    print("=" * 60)
    
    pairs = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
        ("ca", "abc"),
        ("Saturday", "Sunday"),
    ]
    
    for s1, s2 in pairs:
        lev = levenshtein_distance(s1, s2)
        dl = damerau_levenshtein_distance(s1, s2)
        ratio = levenshtein_ratio(s1, s2)
        print(f"\n'{s1}' vs '{s2}':")
        print(f"  Levenshtein distance: {lev}")
        print(f"  Damerau-Levenshtein: {dl}")
        print(f"  Similarity ratio: {ratio:.2%}")


def example_jaro_winkler():
    """Example: Jaro-Winkler similarity for name matching."""
    print("\n" + "=" * 60)
    print("Jaro-Winkler Examples - Name Matching")
    print("=" * 60)
    
    names = [
        ("John", "Jon"),
        ("Martha", "Marhta"),
        ("Jonathan", "Jonathon"),
        ("Jannet", "Janet"),
    ]
    
    for name1, name2 in names:
        jaro = jaro_similarity(name1, name2)
        jw = jaro_winkler_similarity(name1, name2)
        print(f"\n'{name1}' vs '{name2}':")
        print(f"  Jaro similarity: {jaro:.3f}")
        print(f"  Jaro-Winkler: {jw:.3f}")


def example_set_based():
    """Example: Set-based similarity metrics."""
    print("\n" + "=" * 60)
    print("Set-Based Similarity Examples")
    print("=" * 60)
    
    s1, s2 = "hello world", "hello there"
    
    print(f"\nComparing '{s1}' and '{s2}':")
    
    print(f"\nCharacter-level (ngram=1):")
    print(f"  Jaccard: {jaccard_similarity(s1, s2, ngram=1):.2%}")
    print(f"  Overlap: {overlap_coefficient(s1, s2, ngram=1):.2%}")
    
    print(f"\nBigram-level (ngram=2):")
    print(f"  Jaccard: {jaccard_similarity(s1, s2, ngram=2):.2%}")
    print(f"  Dice: {dice_coefficient(s1, s2, ngram=2):.2%}")
    
    print(f"\nWord-level:")
    print(f"  Jaccard: {jaccard_similarity(s1, s2.replace(' ', ''), ngram=1):.2%}")


def example_cosine_similarity():
    """Example: Cosine similarity for document comparison."""
    print("\n" + "=" * 60)
    print("Cosine Similarity Examples")
    print("=" * 60)
    
    documents = [
        "the quick brown fox jumps over the lazy dog",
        "a quick brown fox jumped over a lazy dog",
        "the lazy dog slept in the sun",
    ]
    
    print("\nDocument comparison (bigram-based):")
    for i, d1 in enumerate(documents):
        for j, d2 in enumerate(documents):
            if i < j:
                sim = cosine_similarity(d1, d2, ngram=2)
                print(f"\nDoc {i+1} vs Doc {j+1}:")
                print(f"  Cosine similarity: {sim:.2%}")
    
    print("\nWord-level cosine similarity:")
    print(f"  '{documents[0][:20]}...' vs '{documents[1][:20]}...'")
    print(f"  Similarity: {cosine_similarity_words(documents[0], documents[1]):.2%}")


def example_tfidf():
    """Example: TF-IDF for document similarity."""
    print("\n" + "=" * 60)
    print("TF-IDF Example - Document Corpus Similarity")
    print("=" * 60)
    
    calc = TFIDFCalculator()
    
    # Build a small corpus
    corpus = [
        "machine learning algorithms for data science",
        "deep learning neural networks",
        "natural language processing with python",
        "machine learning fundamentals",
        "python programming for beginners",
    ]
    
    for doc in corpus:
        calc.add_document(doc)
    
    print(f"\nCorpus size: {len(corpus)} documents")
    
    # Compare queries to corpus
    queries = [
        "machine learning",
        "python programming",
        "neural network algorithms",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        for doc in corpus[:3]:
            sim = calc.similarity(query, doc)
            print(f"  Similar to '{doc[:30]}...': {sim:.2%}")


def example_lcs():
    """Example: Longest Common Subsequence."""
    print("\n" + "=" * 60)
    print("Longest Common Subsequence Examples")
    print("=" * 60)
    
    sequences = [
        ("ABCBDAB", "BDCABA"),
        ("XMJYAUZ", "MZJAWUX"),
        ("this is a test", "this test"),
    ]
    
    for s1, s2 in sequences:
        lcs_str = lcs(s1, s2)
        lcs_len = lcs_length(s1, s2)
        ratio = lcs_ratio(s1, s2)
        print(f"\n'{s1}' vs '{s2}':")
        print(f"  LCS: '{lcs_str}'")
        print(f"  LCS length: {lcs_len}")
        print(f"  LCS ratio: {ratio:.2%}")


def example_phonetic():
    """Example: Phonetic matching for names."""
    print("\n" + "=" * 60)
    print("Phonetic Matching Examples")
    print("=" * 60)
    
    name_pairs = [
        ("Robert", "Rupert"),
        ("Smith", "Schmidt"),
        ("Johnson", "Johnsen"),
        ("Catherine", "Katherine"),
        ("Donald", "Donaldo"),
    ]
    
    print("\nSoundex matching:")
    for name1, name2 in name_pairs:
        sx1 = soundex(name1)
        sx2 = soundex(name2)
        match = "MATCH" if sx1 == sx2 else "NO MATCH"
        print(f"  {name1} ({sx1}) vs {name2} ({sx2}): {match}")
    
    print("\nMetaphone codes:")
    for name in ["Smith", "Schmidt", "phone", "fone"]:
        print(f"  {name}: {metaphone(name)}")


def example_fuzzy_matching():
    """Example: Fuzzy matching for search and suggestions."""
    print("\n" + "=" * 60)
    print("Fuzzy Matching Examples")
    print("=" * 60)
    
    # Spelling correction scenario
    dictionary = [
        "apple", "banana", "orange", "grape", "kiwi",
        "strawberry", "blueberry", "raspberry", "mango",
    ]
    
    typos = ["appel", "bannana", "orang", "grap", "stawberry"]
    
    print("\nSpelling correction:")
    for typo in typos:
        match, score = find_best_match(typo, dictionary, threshold=0.6)
        print(f"  '{typo}' -> '{match}' (confidence: {score:.1%})")
    
    # Multiple matches scenario
    print("\nFinding all similar matches for 'berry':")
    berry_words = ["strawberry", "blueberry", "raspberry", "blackberry", "cherry", "berry"]
    matches = find_all_matches("berry", berry_words, threshold=0.6)
    for word, score in matches:
        print(f"  {word}: {score:.1%}")
    
    # Fuzzy search in text
    print("\nFuzzy search for 'python' in text:")
    text = "I love Pythan programming and pithon scripting is great too"
    results = fuzzy_search("python", text, threshold=0.7)
    for start, end, word, score in results:
        print(f"  Found '{word}' at position {start}-{end} (score: {score:.1%})")


def example_comprehensive_comparison():
    """Example: Comprehensive string comparison."""
    print("\n" + "=" * 60)
    print("Comprehensive Comparison Example")
    print("=" * 60)
    
    pairs = [
        ("hello", "hallo"),
        ("python", "pyton"),
        ("javascript", "javascripting"),
    ]
    
    for s1, s2 in pairs:
        print(f"\n'{s1}' vs '{s2}':")
        scores = compare_strings(s1, s2)
        
        # Display key metrics
        key_metrics = ['levenshtein', 'jaro_winkler', 'jaccard_char', 'dice', 'lcs', 'combined']
        for metric in key_metrics:
            value = scores.get(metric, 0)
            print(f"  {metric}: {value:.2%}")
    
    # Similar check
    print("\nQuick similarity check:")
    print(f"  similar('hello', 'hallo', threshold=0.7): {similar('hello', 'hallo', threshold=0.7)}")
    print(f"  similar('hello', 'hallo', threshold=0.9): {similar('hello', 'hallo', threshold=0.9)}")


def example_real_world_use_cases():
    """Example: Real-world use cases."""
    print("\n" + "=" * 60)
    print("Real-World Use Cases")
    print("=" * 60)
    
    # Use case 1: Duplicate detection
    print("\n1. Duplicate Detection in User Input:")
    user_inputs = [
        "John Smith",
        "John Smith",  # Exact duplicate
        "Jon Smith",   # Similar name
        "John Smithe", # Similar name
        "Jane Doe",    # Different person
    ]
    
    print("\nChecking for duplicates (threshold 0.85):")
    duplicates = []
    for i, name1 in enumerate(user_inputs):
        for j, name2 in enumerate(user_inputs):
            if i < j:
                if similar(name1, name2, threshold=0.85, method='jaro_winkler'):
                    duplicates.append((i+1, j+1, name1, name2))
    
    if duplicates:
        print("  Potential duplicates found:")
        for i1, i2, n1, n2 in duplicates:
            print(f"    Entry {i1} '{n1}' and Entry {i2} '{n2}'")
    else:
        print("  No duplicates detected")
    
    # Use case 2: Search ranking
    print("\n2. Search Result Ranking:")
    search_results = [
        "Python Tutorial for Beginners",
        "Python Programming Guide",
        "Learn Python Fast",
        "Python vs Java Comparison",
        "Advanced Python Techniques",
    ]
    
    query = "python beginner tutorial"
    print(f"\nQuery: '{query}'")
    print("\nRanked results:")
    ranked = []
    for result in search_results:
        score = cosine_similarity_words(query, result)
        ranked.append((result, score))
    
    ranked.sort(key=lambda x: x[1], reverse=True)
    for result, score in ranked:
        print(f"  {score:.1%}: {result}")
    
    # Use case 3: Address matching
    print("\n3. Address Matching:")
    addresses = [
        "123 Main Street, New York",
        "123 Main St, New York",
        "123 Mainstreet NY",
        "124 Main Street, New York",
        "456 Oak Avenue, Boston",
    ]
    
    target = "123 Main Street, New York"
    print(f"\nTarget address: '{target}'")
    print("\nSimilarity scores:")
    for addr in addresses:
        score = combined_similarity(target, addr)
        print(f"  '{addr}': {score:.1%}")


def main():
    """Run all examples."""
    print("Text Similarity Utilities - Usage Examples")
    print("=" * 60)
    
    example_edit_distance()
    example_jaro_winkler()
    example_set_based()
    example_cosine_similarity()
    example_tfidf()
    example_lcs()
    example_phonetic()
    example_fuzzy_matching()
    example_comprehensive_comparison()
    example_real_world_use_cases()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()