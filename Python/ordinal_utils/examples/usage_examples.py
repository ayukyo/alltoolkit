"""
Ordinal Utils - Usage Examples

This file demonstrates the various features of the ordinal_utils module.
Run with: python usage_examples.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    to_ordinal,
    to_ordinal_word,
    from_ordinal,
    is_ordinal,
    get_all_ordinal_forms,
    format_date_with_ordinal,
    get_rank_suffix,
    format_ranking,
    ordinal_range,
    compare_ordinals,
    ordinal_to_roman,
    roman_to_ordinal,
    get_ordinal_suffix,
    get_ordinal_suffix_only,
)


def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_basic_ordinals():
    """Basic ordinal number conversion"""
    print_section("Basic Ordinal Numbers")
    
    print("\nConverting cardinal to ordinal (1-20):")
    for i in range(1, 21):
        print(f"  {i} → {to_ordinal(i)}", end="  ")
        if i % 5 == 0:
            print()
    
    print("\n\nSpecial cases (11, 12, 13):")
    for i in [11, 12, 13, 21, 22, 23, 111, 112, 113]:
        print(f"  {i} → {to_ordinal(i)}")


def example_ordinal_words():
    """Ordinal word forms"""
    print_section("Ordinal Words")
    
    print("\nConverting to ordinal words:")
    examples = [1, 2, 3, 4, 5, 10, 11, 12, 20, 21, 22, 30, 33, 100]
    for n in examples:
        print(f"  {n} → {to_ordinal_word(n)}")


def example_multilingual():
    """Multilingual ordinal support"""
    print_section("Multilingual Ordinals")
    
    print("\nOrdinal representations in different languages:")
    numbers = [1, 2, 3, 5, 10]
    languages = ["en", "fr", "de", "zh", "ja"]
    
    print(f"\n{'Number':<10}", end="")
    for lang in languages:
        print(f"{lang:<10}", end="")
    print()
    print("-" * 60)
    
    for n in numbers:
        print(f"{n:<10}", end="")
        for lang in languages:
            print(f"{to_ordinal(n, lang):<10}", end="")
        print()
    
    print("\n\nAll language forms for 5:")
    forms = get_all_ordinal_forms(5)
    for lang, form in sorted(forms.items()):
        print(f"  {lang}: {form}")


def example_parsing():
    """Parsing ordinal strings"""
    print_section("Parsing Ordinal Strings")
    
    print("\nParsing ordinal strings back to numbers:")
    examples = [
        "1st", "2nd", "3rd", "11th", "21st", "100th",
        "第5", "第100", "5番目",
        "first", "second", "tenth", "twenty-first"
    ]
    
    for s in examples:
        result = from_ordinal(s)
        print(f"  '{s}' → {result}")


def example_validation():
    """Validating ordinal strings"""
    print_section("Validation")
    
    print("\nChecking if strings are valid ordinals:")
    test_cases = [
        "1st", "2nd", "3rd", "3th",  # 3th is wrong suffix but still parseable
        "第5", "5番目",
        "first", "twenty-second",
        "hello", ""
    ]
    
    for s in test_cases:
        valid = is_ordinal(s)
        print(f"  '{s}': {'✓ Valid' if valid else '✗ Invalid'}")


def example_date_formatting():
    """Date formatting with ordinals"""
    print_section("Date Formatting with Ordinals")
    
    print("\nFormatting dates:")
    examples = [
        (4, "July", 2026, "mdy"),
        (22, "March", 2026, "dmy"),
        (1, "January", 2026, "ymd"),
        (11, "November", 2026, "mdy"),
        (3, "May", 2026, "dmy"),
    ]
    
    for day, month, year, fmt in examples:
        result = format_date_with_ordinal(day, month, year, fmt)
        print(f"  {day}, {month}, {year} ({fmt}) → {result}")
    
    print("\nDates without year:")
    print(f"  {format_date_with_ordinal(4, 'July')}")
    print(f"  {format_date_with_ordinal(1, 'January')}")


def example_rankings():
    """Ranking and competition formatting"""
    print_section("Rankings and Competitions")
    
    print("\nTop 5 rankings:")
    teams = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    scores = [100, 95, 90, 85, 80]
    
    for i, (team, score) in enumerate(zip(teams, scores), 1):
        print(f"  {format_ranking(i, team, score)}")
    
    print("\nJust medals (top 3):")
    for i in range(1, 4):
        print(f"  {get_rank_suffix(i)} Place")


def example_ranges():
    """Ordinal ranges"""
    print_section("Ordinal Ranges")
    
    print("\nGenerating ordinal ranges:")
    print(f"  1-10: {', '.join(ordinal_range(1, 10))}")
    print(f"  1-3 (French): {', '.join(ordinal_range(1, 3, 'fr'))}")
    print(f"  Count down 5-1: {', '.join(ordinal_range(5, 1))}")


def example_comparison():
    """Comparing ordinals"""
    print_section("Comparing Ordinals")
    
    print("\nComparing ordinal strings:")
    pairs = [
        ("1st", "2nd"),
        ("10th", "5th"),
        ("3rd", "3rd"),
        ("第1", "第10"),
    ]
    
    for o1, o2 in pairs:
        result = compare_ordinals(o1, o2)
        symbol = "<" if result < 0 else (">" if result > 0 else "==")
        print(f"  {o1} {symbol} {o2}")


def example_roman_numerals():
    """Roman numeral conversion"""
    print_section("Roman Numerals")
    
    print("\nConverting to Roman numerals:")
    numbers = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000, 2024, 3999]
    for n in numbers:
        roman = ordinal_to_roman(n)
        print(f"  {n:4d} → {roman}")
    
    print("\nParsing Roman numerals:")
    romans = ["I", "IV", "IX", "XL", "XC", "CD", "CM", "MMXXIV", "MMMCMXCIX"]
    for r in romans:
        n = roman_to_ordinal(r)
        print(f"  {r:12s} → {n}")


def example_suffix_extraction():
    """Suffix extraction"""
    print_section("Suffix Extraction")
    
    print("\nGetting just the suffix:")
    for i in [1, 2, 3, 4, 11, 21, 111]:
        suffix = get_ordinal_suffix_only(i)
        print(f"  {i} → '{suffix}'")


def example_practical_use_cases():
    """Practical use cases"""
    print_section("Practical Use Cases")
    
    print("\n1. Generating a leaderboard:")
    players = [
        ("Alice", 1500),
        ("Bob", 1420),
        ("Charlie", 1380),
        ("Diana", 1350),
        ("Eve", 1300),
    ]
    
    print("\n   Leaderboard:")
    for rank, (name, score) in enumerate(players, 1):
        print(f"   {format_ranking(rank, name, score)}")
    
    print("\n2. Formatting step-by-step instructions:")
    for i in range(1, 6):
        print(f"   {to_ordinal(i)} step: Complete this task")
    
    print("\n3. Anniversary/celebration text:")
    for year in [1, 5, 10, 25, 50, 100]:
        print(f"   Celebrating our {to_ordinal(year)} anniversary!")
    
    print("\n4. Sequential numbering in documents:")
    print("   Article sections:")
    for i, title in enumerate(["Introduction", "Methods", "Results", "Discussion", "Conclusion"], 1):
        print(f"   {to_ordinal_word(i).title()}: {title}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("  ORDINAL NUMBER UTILITIES - USAGE EXAMPLES")
    print("="*60)
    
    example_basic_ordinals()
    example_ordinal_words()
    example_multilingual()
    example_parsing()
    example_validation()
    example_date_formatting()
    example_rankings()
    example_ranges()
    example_comparison()
    example_roman_numerals()
    example_suffix_extraction()
    example_practical_use_cases()
    
    print("\n" + "="*60)
    print("  Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()