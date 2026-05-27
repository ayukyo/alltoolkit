#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Etymology Utils Usage Examples

Demonstrates various ways to use the etymology_utils module for
word origin analysis, root extraction, and etymology visualization.

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from etymology_utils.mod import (
    # Enums
    LanguageOrigin, HistoricalPeriod,
    
    # Data classes
    EtymologyEntry, EtymologyTree, WordFamily,
    
    # Core functions
    get_etymology, add_etymology, search_by_origin, search_by_period,
    find_cognates, get_word_family, build_etymology_tree, extract_root,
    analyze_word, detect_compound, compare_words, visualize_tree,
    get_statistics, search_words, validate_etymology, export_to_json,
    
    # Advanced functions
    trace_word_evolution, find_language_contributions,
    find_period_contributions, generate_word_report,
    
    # Convenience functions
    quick_lookup, is_loanword, get_loanwords, get_native_words
)


def example_basic_lookup():
    """Example: Basic etymology lookup."""
    print("=" * 60)
    print("Example 1: Basic Etymology Lookup")
    print("=" * 60)
    
    # Look up etymology for common words
    words = ["computer", "philosophy", "king", "coffee"]
    
    for word in words:
        print(f"\n--- {word} ---")
        entry = get_etymology(word)
        if entry:
            print(f"Language Origin: {entry.language_origin.value}")
            print(f"Historical Period: {entry.historical_period.value}")
            print(f"Original Form: {entry.original_form}")
            print(f"Confidence: {entry.confidence:.0%}")
            if entry.notes:
                print(f"Notes: {entry.notes}")
        else:
            print("No etymology data available")


def example_quick_lookup():
    """Example: Quick lookup for fast results."""
    print("\n" + "=" * 60)
    print("Example 2: Quick Lookup")
    print("=" * 60)
    
    words = ["computer", "philosophy", "education", "telephone", "karate"]
    
    for word in words:
        result = quick_lookup(word)
        print(f"  {result}")


def example_analyze_word():
    """Example: Comprehensive word analysis."""
    print("\n" + "=" * 60)
    print("Example 3: Comprehensive Word Analysis")
    print("=" * 60)
    
    analysis = analyze_word("information")
    
    print("\nAnalysis for 'information':")
    print(f"  Word: {analysis['word']}")
    
    if analysis['etymology']:
        print(f"  Origin: {analysis['etymology']['language_origin']}")
        print(f"  Period: {analysis['etymology']['historical_period']}")
        print(f"  Original: {analysis['etymology']['original_form']}")
    
    if analysis['prefix']:
        print(f"  Prefix: {analysis['prefix']['prefix']} ({analysis['prefix']['meaning']})")
    
    if analysis['suffix']:
        print(f"  Suffix: {analysis['suffix']['suffix']} ({analysis['suffix']['meaning']})")
    
    print(f"  Is Compound: {analysis['is_compound']}")
    
    if analysis['cognates']:
        print("  Cognates:")
        for lang, cognate in analysis['cognates'].items():
            print(f"    - {lang}: {cognate}")


def example_etymology_tree():
    """Example: Building and visualizing etymology trees."""
    print("\n" + "=" * 60)
    print("Example 4: Etymology Tree Visualization")
    print("=" * 60)
    
    words = ["telephone", "philosophy", "computer"]
    
    for word in words:
        print(f"\n--- Tree for '{word}' ---")
        tree = build_etymology_tree(word)
        print(visualize_tree(tree))
        print(f"Tree depth: {tree.depth()}")
        print(f"Tree size: {tree.size()}")


def example_word_family():
    """Example: Finding word families."""
    print("\n" + "=" * 60)
    print("Example 5: Word Family")
    print("=" * 60)
    
    roots = ["work", "act", "form", "read"]
    
    for root in roots:
        family = get_word_family(root)
        if family:
            print(f"\nWord Family for '{root}':")
            print(f"  Members: {', '.join(family.members[:10])}")
            print(f"  Total members: {len(family.members)}")


def example_cognates():
    """Example: Finding cognates across languages."""
    print("\n" + "=" * 60)
    print("Example 6: Cross-Language Cognates")
    print("=" * 60)
    
    words = ["computer", "philosophy", "mathematics", "justice", "beauty"]
    
    for word in words:
        cognates = find_cognates(word)
        if cognates:
            print(f"\nCognates for '{word}':")
            for lang, cognate in cognates.items():
                print(f"  {lang}: {cognate}")


def example_search_by_origin():
    """Example: Searching by language origin."""
    print("\n" + "=" * 60)
    print("Example 7: Search by Language Origin")
    print("=" * 60)
    
    origins = [
        LanguageOrigin.LATIN,
        LanguageOrigin.GREEK,
        LanguageOrigin.OLD_ENGLISH,
        LanguageOrigin.ARABIC
    ]
    
    for origin in origins:
        results = search_by_origin(origin)
        print(f"\nWords from {origin.value}:")
        for entry in results[:5]:
            print(f"  - {entry.word}")


def example_search_by_period():
    """Example: Searching by historical period."""
    print("\n" + "=" * 60)
    print("Example 8: Search by Historical Period")
    print("=" * 60)
    
    periods = [
        HistoricalPeriod.ANCIENT,
        HistoricalPeriod.MEDIEVAL,
        HistoricalPeriod.MODERN
    ]
    
    for period in periods:
        results = search_by_period(period)
        print(f"\nWords from {period.value} period:")
        for entry in results[:5]:
            print(f"  - {entry.word} ({entry.language_origin.value})")


def example_compare_words():
    """Example: Comparing word etymologies."""
    print("\n" + "=" * 60)
    print("Example 9: Compare Words")
    print("=" * 60)
    
    pairs = [
        ("computer", "information"),
        ("philosophy", "mathematics"),
        ("king", "friend"),
        ("coffee", "tea")
    ]
    
    for word1, word2 in pairs:
        result = compare_words(word1, word2)
        print(f"\nComparing '{word1}' vs '{word2}':")
        print(f"  Same Origin: {result['same_origin']}")
        print(f"  Same Period: {result['same_period']}")
        print(f"  Related: {result['related']}")
        if result['common_root']:
            print(f"  Common Root: {result['common_root']}")


def example_loanword_detection():
    """Example: Detecting loanwords."""
    print("\n" + "=" * 60)
    print("Example 10: Loanword Detection")
    print("=" * 60)
    
    words = ["computer", "philosophy", "king", "friend", "coffee", "karate"]
    
    print("\nLoanword analysis:")
    for word in words:
        is_loan = is_loanword(word)
        entry = get_etymology(word)
        origin = entry.language_origin.value if entry else "Unknown"
        status = "外来词" if is_loan else "原生词"
        print(f"  {word}: {status} (from {origin})")


def example_compound_detection():
    """Example: Detecting compound words."""
    print("\n" + "=" * 60)
    print("Example 11: Compound Word Detection")
    print("=" * 60)
    
    words = ["breakfast", "airport", "computer", "philosophy", "telephone"]
    
    for word in words:
        parts = detect_compound(word)
        analysis = analyze_word(word)
        if parts or analysis['is_compound']:
            print(f"  {word}: compound → {parts if parts else 'detected'}")
        else:
            print(f"  {word}: not a compound")


def example_word_evolution():
    """Example: Tracing word evolution."""
    print("\n" + "=" * 60)
    print("Example 12: Word Evolution Trace")
    print("=" * 60)
    
    words = ["computer", "philosophy", "telephone"]
    
    for word in words:
        print(f"\nEvolution of '{word}':")
        stages = trace_word_evolution(word)
        for stage in stages:
            form = stage['form']
            period = stage['period']
            origin = stage['origin']
            meaning = stage.get('meaning', '')
            meaning_str = f" → {meaning}" if meaning else ""
            print(f"  {form} [{period}] ({origin}){meaning_str}")


def example_statistics():
    """Example: Getting database statistics."""
    print("\n" + "=" * 60)
    print("Example 13: Database Statistics")
    print("=" * 60)
    
    stats = get_statistics()
    
    print(f"\nDatabase Overview:")
    print(f"  Total Words: {stats['total_words']}")
    print(f"  Total Roots: {stats['total_roots']}")
    print(f"  Total Prefixes: {stats['total_prefixes']}")
    print(f"  Total Suffixes: {stats['total_suffixes']}")
    print(f"  Average Confidence: {stats['average_confidence']:.1%}")
    
    print("\nWords by Language Origin:")
    for origin, count in stats['by_origin'].items():
        print(f"  {origin}: {count}")
    
    print("\nWords by Historical Period:")
    for period, count in stats['by_period'].items():
        print(f"  {period}: {count}")


def example_generate_report():
    """Example: Generating detailed word reports."""
    print("\n" + "=" * 60)
    print("Example 14: Word Report Generation")
    print("=" * 60)
    
    report = generate_word_report("philosophy")
    print(report)


def example_search_words():
    """Example: Searching words in database."""
    print("\n" + "=" * 60)
    print("Example 15: Word Search")
    print("=" * 60)
    
    # Prefix search
    print("\nPrefix search for 'com':")
    results = search_words("com")
    print(f"  Found: {results}")
    
    # Fuzzy search
    print("\nFuzzy search for 'phil':")
    results = search_words("phil", fuzzy=True)
    print(f"  Found: {results}")


def example_language_contributions():
    """Example: Analyzing language contributions."""
    print("\n" + "=" * 60)
    print("Example 16: Language Contributions")
    print("=" * 60)
    
    contributions = find_language_contributions()
    print("\nWords contributed by each language:")
    for lang, count in sorted(contributions.items(), key=lambda x: -x[1]):
        print(f"  {lang}: {count} words")


def example_period_contributions():
    """Example: Analyzing period contributions."""
    print("\n" + "=" * 60)
    print("Example 17: Period Contributions")
    print("=" * 60)
    
    contributions = find_period_contributions()
    print("\nWords from each historical period:")
    for period, count in sorted(contributions.items(), key=lambda x: -x[1]):
        print(f"  {period}: {count} words")


def example_loanwords_and_native():
    """Example: Getting loanwords and native words."""
    print("\n" + "=" * 60)
    print("Example 18: Loanwords vs Native Words")
    print("=" * 60)
    
    loanwords = get_loanwords()
    native = get_native_words()
    
    print(f"\nTotal Loanwords: {len(loanwords)}")
    print(f"Examples: {loanwords[:10]}")
    
    print(f"\nTotal Native Words: {len(native)}")
    print(f"Examples: {native[:10]}")


def example_add_custom_entry():
    """Example: Adding custom etymology entry."""
    print("\n" + "=" * 60)
    print("Example 19: Adding Custom Entry")
    print("=" * 60)
    
    # Create a custom entry
    custom_entry = EtymologyEntry(
        word="algorithm",
        language_origin=LanguageOrigin.ARABIC,
        historical_period=HistoricalPeriod.MEDIEVAL,
        original_form="al-Khwārizmī",
        intermediate_forms=["algorismus", "algorithm"],
        meaning_evolution=["procedure", "step-by-step method"],
        related_words=["algorithmic", "algorithmically"],
        cognates={"Spanish": "algoritmo", "French": "algorithme"},
        notes="Named after Persian mathematician al-Khwārizmī",
        confidence=0.95
    )
    
    # Add to database
    add_etymology(custom_entry)
    
    # Verify it was added
    entry = get_etymology("algorithm")
    if entry:
        print(f"\nSuccessfully added 'algorithm':")
        print(f"  Origin: {entry.language_origin.value}")
        print(f"  Original: {entry.original_form}")
        print(f"  Confidence: {entry.confidence:.0%}")


def example_export_json():
    """Example: Exporting data to JSON."""
    print("\n" + "=" * 60)
    print("Example 20: Export to JSON")
    print("=" * 60)
    
    # Export all data
    json_str = export_to_json()
    
    # Show first few lines
    lines = json_str.split('\n')[:20]
    print("\nJSON Export Preview:")
    for line in lines:
        print(f"  {line}")
    
    print(f"\n  ... (Total {len(json_str)} characters)")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("ETYMOLOGY UTILS - USAGE EXAMPLES")
    print("=" * 60)
    
    example_basic_lookup()
    example_quick_lookup()
    example_analyze_word()
    example_etymology_tree()
    example_word_family()
    example_cognates()
    example_search_by_origin()
    example_search_by_period()
    example_compare_words()
    example_loanword_detection()
    example_compound_detection()
    example_word_evolution()
    example_statistics()
    example_generate_report()
    example_search_words()
    example_language_contributions()
    example_period_contributions()
    example_loanwords_and_native()
    example_add_custom_entry()
    example_export_json()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()