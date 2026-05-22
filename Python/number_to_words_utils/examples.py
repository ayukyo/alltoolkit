#!/usr/bin/env python3
"""
Examples for number_to_words_utils

Demonstrates all features of the number to words conversion library.
"""

from converter import (
    number_to_words,
    number_to_currency_words,
    number_to_ordinal_words,
    get_supported_languages,
)


def print_separator(title: str):
    """Print a section separator."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def main():
    print("Number to Words Utility - Examples")
    print("=" * 60)
    
    # Supported languages
    print_separator("Supported Languages")
    languages = get_supported_languages()
    print(f"Supported language codes: {', '.join(sorted(set(languages)))}")
    
    # Basic English conversion
    print_separator("Basic English Conversion")
    test_numbers = [0, 1, 5, 10, 11, 15, 19, 20, 21, 42, 99, 100, 101, 500, 999, 
                   1000, 1234, 10000, 100000, 1000000, 1000000000]
    
    for num in test_numbers:
        words = number_to_words(num)
        print(f"{num:>12,} → {words}")
    
    # Negative numbers
    print_separator("Negative Numbers")
    for num in [-1, -42, -1000]:
        words = number_to_words(num)
        print(f"{num:>12} → {words}")
    
    # Decimal numbers
    print_separator("Decimal Numbers")
    for num in [1.5, 3.14159, 0.123, 99.99]:
        words = number_to_words(num)
        print(f"{num:>12} → {words}")
    
    # Ordinal numbers
    print_separator("Ordinal Numbers (English)")
    for num in [1, 2, 3, 4, 5, 10, 11, 12, 20, 21, 22, 100, 101]:
        words = number_to_ordinal_words(num)
        print(f"{num:>12} → {words}")
    
    # Currency
    print_separator("Currency (English)")
    amounts = [1, 5, 42, 100, 42.50, 99.99, 1234.56]
    for amount in amounts:
        words = number_to_currency_words(amount)
        print(f"${amount:>10} → {words}")
    
    # Chinese
    print_separator("Chinese Conversion")
    for num in [0, 1, 5, 10, 11, 15, 20, 42, 100, 101, 1000, 10000, 100000000]:
        words = number_to_words(num, lang="zh")
        print(f"{num:>12,} → {words}")
    
    # Chinese ordinals
    print_separator("Chinese Ordinals")
    for num in [1, 2, 3, 10, 100]:
        words = number_to_ordinal_words(num, lang="zh")
        print(f"{num:>12} → {words}")
    
    # Chinese currency (人民币大写)
    print_separator("Chinese Currency (人民币大写)")
    amounts = [1, 100, 42.5, 1234.56, 10000]
    for amount in amounts:
        words = number_to_currency_words(amount, lang="zh")
        print(f"¥{amount:>10} → {words}")
    
    # Japanese
    print_separator("Japanese Conversion")
    for num in [0, 1, 5, 10, 20, 42, 100, 1000, 10000]:
        words = number_to_words(num, lang="ja")
        print(f"{num:>12,} → {words}")
    
    # Korean
    print_separator("Korean Conversion")
    for num in [0, 1, 5, 10, 20, 42, 100, 1000, 10000]:
        words = number_to_words(num, lang="ko")
        print(f"{num:>12,} → {words}")
    
    # Spanish
    print_separator("Spanish Conversion")
    for num in [0, 1, 5, 10, 15, 20, 21, 25, 42, 100, 101, 1000]:
        words = number_to_words(num, lang="es")
        print(f"{num:>12,} → {words}")
    
    # French
    print_separator("French Conversion")
    for num in [0, 1, 5, 10, 15, 20, 42, 70, 71, 80, 90, 100, 1000]:
        words = number_to_words(num, lang="fr")
        print(f"{num:>12,} → {words}")
    
    # German
    print_separator("German Conversion")
    for num in [0, 1, 5, 10, 15, 20, 21, 42, 100, 1000]:
        words = number_to_words(num, lang="de")
        print(f"{num:>12,} → {words}")
    
    # Cross-language comparison
    print_separator("Cross-Language Comparison (Number 42)")
    for lang in ["en", "zh", "ja", "ko", "es", "fr", "de"]:
        words = number_to_words(42, lang=lang)
        print(f"{lang:>4}: {words}")
    
    # Cross-language comparison for 100
    print_separator("Cross-Language Comparison (Number 100)")
    for lang in ["en", "zh", "ja", "ko", "es", "fr", "de"]:
        words = number_to_words(100, lang=lang)
        print(f"{lang:>4}: {words}")
    
    # Different input types
    print_separator("Different Input Types")
    print(f"int:    {number_to_words(42)}")
    print(f"float:  {number_to_words(42.0)}")
    print(f"str:    {number_to_words('42')}")
    from decimal import Decimal
    print(f"Decimal: {number_to_words(Decimal('42.5'))}")
    
    print_separator("Done!")
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()