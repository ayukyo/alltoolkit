#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Number Words Utilities Usage Examples
====================================================
Demonstrates the various features of the number_words_utils module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from number_words_utils.mod import (
    number_to_words,
    words_to_number,
    number_to_currency_words,
    is_valid_number_word,
    get_number_words_list,
    Language,
)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def example_basic_conversions():
    """Basic number to words conversions."""
    print_section("Basic Number to Words Conversions")
    
    numbers = [0, 1, 10, 42, 100, 123, 1000, 1234, 10000, 12345, 100000, 1000000, 123456789]
    
    for num in numbers:
        words = number_to_words(num)
        print(f"{num:>15,} → {words}")


def example_ordinal_numbers():
    """Ordinal number conversions."""
    print_section("Ordinal Numbers (1st, 2nd, 3rd...)")
    
    for i in range(1, 32):
        ordinal = number_to_words(i, ordinal=True)
        print(f"{i:>2} → {ordinal}")


def example_negative_numbers():
    """Negative number handling."""
    print_section("Negative Numbers")
    
    numbers = [-1, -10, -42, -100, -123, -1000]
    
    for num in numbers:
        words = number_to_words(num)
        print(f"{num:>6} → {words}")


def example_decimal_numbers():
    """Decimal number handling."""
    print_section("Decimal Numbers")
    
    numbers = [0.5, 1.25, 3.14159, 123.45, 100.01]
    
    for num in numbers:
        words = number_to_words(num)
        print(f"{num:>10} → {words}")


def example_chinese_conversions():
    """Chinese number conversions."""
    print_section("Chinese Number Conversions")
    
    numbers = [0, 1, 10, 11, 20, 21, 100, 101, 123, 1000, 1234, 10000, 12345, 100000, 1000000, 100000000]
    
    print("\nNumber → Chinese:")
    for num in numbers:
        words = number_to_words(num, Language.CHINESE)
        print(f"{num:>12,} → {words}")
    
    print("\nOrdinal Numbers:")
    for i in range(1, 11):
        ordinal = number_to_words(i, Language.CHINESE, ordinal=True)
        print(f"{i:>2} → {ordinal}")


def example_words_to_number():
    """Words to number conversions."""
    print_section("Words to Number Conversions")
    
    words_list = [
        "zero",
        "one",
        "ten",
        "twenty-one",
        "one hundred",
        "one hundred twenty-three",
        "one thousand",
        "one thousand two hundred thirty-four",
        "one million",
        "two million three hundred thousand",
        "one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine",
        "minus forty-two",
        "one point five",
    ]
    
    for words in words_list:
        number = words_to_number(words)
        print(f"'{words}' → {number:,}")


def example_chinese_words_to_number():
    """Chinese words to number conversions."""
    print_section("Chinese Words to Number")
    
    words_list = [
        "零",
        "一",
        "十",
        "十一",
        "二十",
        "二十一",
        "一百",
        "一百二十三",
        "一千",
        "一万",
        "一万二千三百四十五",
        "一亿",
        "负一百",
        "一点五",
    ]
    
    for words in words_list:
        number = words_to_number(words, Language.CHINESE)
        print(f"'{words}' → {number:,}")


def example_currency():
    """Currency amount conversions."""
    print_section("Currency Conversions")
    
    amounts = [1, 10, 100, 123.45, 1000.01]
    
    print("\nUSD (US Dollars):")
    for amount in amounts:
        words = number_to_currency_words(amount, "USD")
        print(f"${amount:>10.2f} → {words}")
    
    print("\nEUR (Euros):")
    for amount in amounts:
        words = number_to_currency_words(amount, "EUR")
        print(f"€{amount:>10.2f} → {words}")
    
    print("\nGBP (British Pounds):")
    for amount in amounts:
        words = number_to_currency_words(amount, "GBP")
        print(f"£{amount:>10.2f} → {words}")
    
    print("\nCNY (Chinese Yuan):")
    for amount in amounts:
        words = number_to_currency_words(amount, "CNY")
        print(f"¥{amount:>10.2f} → {words}")
    
    print("\nCNY in Chinese:")
    for amount in amounts:
        words = number_to_currency_words(amount, "CNY", Language.CHINESE)
        print(f"¥{amount:>10.2f} → {words}")


def example_round_trip():
    """Round-trip conversion examples."""
    print_section("Round-Trip Conversions (Number → Words → Number)")
    
    print("\nEnglish:")
    numbers = [0, 42, 123, 1234, 12345, 123456, 1234567]
    for num in numbers:
        words = number_to_words(num)
        back = words_to_number(words)
        status = "✓" if back == num else "✗"
        print(f"{num:>10,} → '{words}' → {back} {status}")
    
    print("\nChinese:")
    for num in numbers:
        words = number_to_words(num, Language.CHINESE)
        back = words_to_number(words, Language.CHINESE)
        status = "✓" if back == num else "✗"
        print(f"{num:>10,} → '{words}' → {back} {status}")


def example_large_numbers():
    """Large number conversions."""
    print_section("Large Numbers")
    
    numbers = [
        10**6,   # Million
        10**9,   # Billion
        10**12,  # Trillion
        10**15,  # Quadrillion
        10**18,  # Quintillion
    ]
    
    print("\nEnglish:")
    for num in numbers:
        words = number_to_words(num)
        print(f"{num:>20,} → {words}")
    
    print("\nChinese (using 兆 for 10^12):")
    for num in numbers[:3]:
        words = number_to_words(num, Language.CHINESE)
        print(f"{num:>20,} → {words}")


def example_utility_functions():
    """Utility function examples."""
    print_section("Utility Functions")
    
    print("\nValid English number words:")
    test_words = ["one", "hundred", "million", "hello", "world", "first", "point"]
    for word in test_words:
        valid = is_valid_number_word(word)
        print(f"  '{word}': {valid}")
    
    print("\nValid Chinese number words:")
    test_words = ["一", "百", "万", "你好", "世界"]
    for word in test_words:
        valid = is_valid_number_word(word, Language.CHINESE)
        print(f"  '{word}': {valid}")
    
    print("\nAll English number words:")
    words = get_number_words_list(Language.ENGLISH)
    print(f"  Count: {len(words)}")
    print(f"  Sample: {', '.join(sorted(words)[:20])}...")
    
    print("\nAll Chinese number words:")
    words = get_number_words_list(Language.CHINESE)
    print(f"  Count: {len(words)}")
    print(f"  Words: {', '.join(sorted(words))}")


def example_special_cases():
    """Special case examples."""
    print_section("Special Cases")
    
    print("\nNumbers with 'and' (British style):")
    words = "one hundred and twenty-three"
    number = words_to_number(words)
    print(f"'{words}' → {number}")
    
    print("\nHyphenated vs space-separated:")
    hyphen = words_to_number("twenty-one")
    space = words_to_number("twenty one")
    print(f"'twenty-one' = {hyphen}, 'twenty one' = {space}")
    
    print("\nAlternative Chinese '两' for two:")
    number = words_to_number("两", Language.CHINESE)
    print(f"'两' → {number}")
    
    print("\nNegative ordinals:")
    neg_first = number_to_words(-1, ordinal=True)
    print(f"(-1, ordinal=True) → '{neg_first}'")


def main():
    """Run all examples."""
    print("=" * 60)
    print("  AllToolkit - Number Words Utilities Examples")
    print("=" * 60)
    
    example_basic_conversions()
    example_ordinal_numbers()
    example_negative_numbers()
    example_decimal_numbers()
    example_chinese_conversions()
    example_words_to_number()
    example_chinese_words_to_number()
    example_currency()
    example_round_trip()
    example_large_numbers()
    example_utility_functions()
    example_special_cases()
    
    print("\n" + "=" * 60)
    print("  Examples Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()