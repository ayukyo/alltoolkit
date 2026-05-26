"""
Unicode Lookup Utilities - Usage Examples

This file demonstrates practical usage scenarios for the unicode_lookup_utils module.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode_lookup_utils.mod import (
    get_char_name,
    get_char_by_name,
    get_code_point,
    get_char_by_code_point,
    get_category,
    get_category_name,
    get_block,
    get_script,
    get_full_info,
    search_by_name,
    search_by_category,
    analyze_string,
    convert_to_html_entities,
    convert_from_html_entities,
    list_emojis,
    is_char_emoji,
    is_char_letter,
    is_char_currency,
    decompose_char,
    compose_char,
    strip_combining_marks,
    count_width,
    pad_unicode,
    escape_unicode,
    unescape_unicode,
    get_char_summary,
    print_char_table,
)


def example_basic_lookup():
    """
    Example 1: Basic Character Lookup
    
    Get information about individual characters.
    """
    print("=" * 60)
    print("Example 1: Basic Character Lookup")
    print("=" * 60)
    
    # Get character name
    chars = ['A', '中', '€', '©', '☃', '😀']
    
    print("\nCharacter Names:")
    for char in chars:
        name = get_char_name(char)
        cp = get_code_point(char)
        print(f"  '{char}' (U+{cp:04X}) → {name}")
    
    # Get character by name
    print("\nLookup by Name:")
    names = ['LATIN CAPITAL LETTER A', 'SNOWMAN', 'COPYRIGHT SIGN']
    for name in names:
        char = get_char_by_name(name)
        print(f"  '{name}' → '{char}'")
    
    # Get character by code point
    print("\nLookup by Code Point:")
    code_points = [65, 20013, 8364, 0x1F600]
    for cp in code_points:
        char = get_char_by_code_point(cp)
        name = get_char_name(char)
        print(f"  U+{cp:04X} → '{char}' ({name})")


def example_character_properties():
    """
    Example 2: Character Properties
    
    Get detailed properties of characters.
    """
    print("\n" + "=" * 60)
    print("Example 2: Character Properties")
    print("=" * 60)
    
    chars = ['A', '5', '$', '中', 'é', '😀']
    
    print("\nCharacter Categories and Scripts:")
    for char in chars:
        cat = get_category(char)
        cat_name = get_category_name(cat)
        script = get_script(char)
        block = get_block(char)
        print(f"  '{char}' → {cat} ({cat_name}), Script: {script}, Block: {block}")


def example_full_character_info():
    """
    Example 3: Full Character Information
    
    Get comprehensive information about a character.
    """
    print("\n" + "=" * 60)
    print("Example 3: Full Character Information")
    print("=" * 60)
    
    chars = ['A', '€', '中']
    
    for char in chars:
        info = get_full_info(char)
        print(f"\n  Character: '{char}'")
        print(f"    Code Point: U+{info.code_point:04X}")
        print(f"    Name: {info.name}")
        print(f"    Category: {info.category} ({info.category_name})")
        print(f"    Block: {info.block}")
        print(f"    Script: {info.script}")
        print(f"    Width: {info.width}")
        print(f"    UTF-8: {info.utf8_hex} ({len(info.utf8_bytes)} bytes)")
        print(f"    HTML: {info.html_entity_decimal} / {info.html_entity_hex}")
        if info.html_entity_named:
            print(f"    Named Entity: {info.html_entity_named}")
        print(f"    Type Checks:")
        print(f"      - Letter: {info.is_letter}")
        print(f"      - Digit: {info.is_digit}")
        print(f"      - Symbol: {info.is_symbol}")
        print(f"      - Currency: {info.is_currency}")
        print(f"      - Emoji: {info.is_emoji}")


def example_search_characters():
    """
    Example 4: Search for Characters
    
    Search for characters by name or category.
    """
    print("\n" + "=" * 60)
    print("Example 4: Search for Characters")
    print("=" * 60)
    
    # Search by name keyword
    print("\nSearch by Name 'arrow':")
    results = search_by_name('arrow', limit=10)
    for r in results:
        print(f"  '{r['char']}' (U+{r['code_point']:04X}) - {r['name']}")
    
    # Search for currency symbols
    print("\nCurrency Symbols (Category 'Sc'):")
    chars = search_by_category('Sc')
    for char in chars[:10]:
        name = get_char_name(char)
        print(f"  '{char}' - {name}")
    
    # Search for math symbols
    print("\nMath Symbols (Category 'Sm'):")
    chars = search_by_category('Sm')
    for char in chars[:10]:
        name = get_char_name(char)
        print(f"  '{char}' - {name}")


def example_string_analysis():
    """
    Example 5: String Analysis
    
    Analyze Unicode content in strings.
    """
    print("\n" + "=" * 60)
    print("Example 5: String Analysis")
    print("=" * 60)
    
    strings = [
        'Hello World',
        '你好世界',
        'Hello 世界! 🌍',
        'café résumé',
        'Price: $100 €50 ¥500',
    ]
    
    for s in strings:
        stats = analyze_string(s)
        print(f"\n  String: '{s}'")
        print(f"    Total chars: {stats['total_chars']}")
        print(f"    Letters: {stats['letter_count']}")
        print(f"    Digits: {stats['digit_count']}")
        print(f"    Symbols: {stats['symbol_count']}")
        print(f"    Currency: {stats['currency_count']}")
        print(f"    Emoji: {stats['emoji_count']}")
        print(f"    Has non-ASCII: {stats['has_non_ascii']}")
        print(f"    UTF-8 bytes: {stats['byte_length_utf8']}")
        print(f"    Width: {count_width(s)} columns")


def example_html_entities():
    """
    Example 6: HTML Entity Conversion
    
    Convert between characters and HTML entities.
    """
    print("\n" + "=" * 60)
    print("Example 6: HTML Entity Conversion")
    print("=" * 60)
    
    # Convert to HTML entities
    strings = [
        '<script>alert("XSS")</script>',
        'Copyright © 2024',
        'Price: $100',
        'Hello 世界',
    ]
    
    print("\nConvert to HTML Entities:")
    for s in strings:
        encoded = convert_to_html_entities(s)
        print(f"  '{s}' → '{encoded}'")
    
    # Convert from HTML entities
    entities = [
        '&lt;div&amp;gt;',
        '&copy; 2024 &trade;',
        '&#x4E2D;&#x65E5;',
    ]
    
    print("\nConvert from HTML Entities:")
    for e in entities:
        decoded = convert_from_html_entities(e)
        print(f"  '{e}' → '{decoded}'")


def example_emoji_handling():
    """
    Example 7: Emoji Handling
    
    Work with emoji characters.
    """
    print("\n" + "=" * 60)
    print("Example 7: Emoji Handling")
    print("=" * 60)
    
    # List emojis
    print("\nFace Emojis:")
    emojis = list_emojis('face', limit=10)
    for e in emojis:
        print(f"  '{e['char']}' - {e['name']}")
    
    print("\nAnimal Emojis:")
    emojis = list_emojis('animal', limit=10)
    for e in emojis:
        print(f"  '{e['char']}' - {e['name']}")
    
    print("\nNature Emojis:")
    emojis = list_emojis('nature', limit=10)
    for e in emojis:
        print(f"  '{e['char']}' - {e['name']}")
    
    # Check if emoji
    chars = ['A', '中', '😀', '🎉', '❤️']
    print("\nEmoji Check:")
    for char in chars:
        is_emoji = is_char_emoji(char)
        print(f"  '{char}' → Emoji: {is_emoji}")


def example_normalization():
    """
    Example 8: Unicode Normalization
    
    Handle composed and decomposed characters.
    """
    print("\n" + "=" * 60)
    print("Example 8: Unicode Normalization")
    print("=" * 60)
    
    # Decompose characters
    chars = ['é', 'ã', 'ü', 'ñ']
    
    print("\nDecompose Characters:")
    for char in chars:
        base, marks = decompose_char(char)
        marks_str = ''.join(f'\\u{ord(m):04X}' for m in marks)
        print(f"  '{char}' → base '{base}' + marks [{marks_str}]")
    
    # Compose characters
    print("\nCompose Characters:")
    compositions = [
        ('e', '\u0301'),  # e + acute
        ('a', '\u0303'),  # a + tilde
        ('o', '\u0308'),  # o + diaeresis
    ]
    
    for base, mark in compositions:
        composed = compose_char(base, [mark])
        print(f"  '{base}' + '\\u{ord(mark):04X}' → '{composed}'")
    
    # Strip combining marks
    print("\nStrip Combining Marks:")
    strings = ['café', 'résumé', 'naïve', 'über']
    for s in strings:
        stripped = strip_combining_marks(s)
        print(f"  '{s}' → '{stripped}'")


def example_width_and_padding():
    """
    Example 9: Width Calculation and Padding
    
    Handle character width for display alignment.
    """
    print("\n" + "=" * 60)
    print("Example 9: Width Calculation and Padding")
    print("=" * 60)
    
    strings = ['Hello', '你好', 'Hello世界', '😀😀😀']
    
    print("\nWidth Calculation:")
    for s in strings:
        width = count_width(s)
        print(f"  '{s}' → {width} display columns")
    
    print("\nPadding Examples:")
    texts = ['你好', 'Hello', '😀']
    
    for text in texts:
        padded_left = pad_unicode(text, 10, align='left')
        padded_right = pad_unicode(text, 10, align='right')
        padded_center = pad_unicode(text, 10, align='center')
        
        print(f"  '{text}' (width={count_width(text)}):")
        print(f"    Left:   '{padded_left}'")
        print(f"    Right:  '{padded_right}'")
        print(f"    Center: '{padded_center}'")


def example_unicode_escaping():
    """
    Example 10: Unicode Escaping
    
    Escape and unescape Unicode strings.
    """
    print("\n" + "=" * 60)
    print("Example 10: Unicode Escaping")
    print("=" * 60)
    
    # Escape Unicode
    strings = ['Hello 世界', 'Price: $100', 'Copyright ©']
    
    print("\nEscape Unicode (non-ASCII only):")
    for s in strings:
        escaped = escape_unicode(s)
        print(f"  '{s}' → '{escaped}'")
    
    print("\nEscape All Characters:")
    s = 'Hello'
    escaped = escape_unicode(s, escape_all=True)
    print(f"  '{s}' → '{escaped}'")
    
    # Unescape Unicode
    escaped_strings = [
        'Hello \\u4e16\\u4e2d',
        'Price: \\u0024100',
        '\\u0048\\u0065\\u006c\\u006c\\u006f',
    ]
    
    print("\nUnescape Unicode:")
    for e in escaped_strings:
        unescaped = unescape_unicode(e)
        print(f"  '{e}' → '{unescaped}'")


def example_character_summary():
    """
    Example 11: Character Summary
    
    Get human-readable summaries of characters.
    """
    print("\n" + "=" * 60)
    print("Example 11: Character Summary")
    print("=" * 60)
    
    chars = ['A', '5', '$', '中', '€', '😀', 'é', '©']
    
    print("\nCharacter Summaries:")
    for char in chars:
        summary = get_char_summary(char)
        print(f"  {summary}")


def example_character_table():
    """
    Example 12: Character Table
    
    Display characters in formatted tables.
    """
    print("\n" + "=" * 60)
    print("Example 12: Character Table")
    print("=" * 60)
    
    # Basic Latin printable characters
    chars = [chr(i) for i in range(32, 48)]  # Space to /
    
    print("\nBasic Latin Characters (32-47):")
    table = print_char_table(chars, width=8)
    print(table)
    
    # Currency symbols
    currency_chars = ['$', '¢', '£', '¥', '€', '₹', '₽', '₿']
    
    print("\nCurrency Symbols:")
    table = print_char_table(currency_chars, width=4)
    print(table)


def example_type_checks():
    """
    Example 13: Character Type Checks
    
    Check character types for validation.
    """
    print("\n" + "=" * 60)
    print("Example 13: Character Type Checks")
    print("=" * 60)
    
    # Test various characters
    test_cases = [
        ('A', 'Letter'),
        ('5', 'Digit'),
        ('$', 'Currency'),
        ('+', 'Math Symbol'),
        ('.', 'Punctuation'),
        (' ', 'Whitespace'),
        ('中', 'CJK Letter'),
        ('😀', 'Emoji'),
    ]
    
    print("\nCharacter Type Checks:")
    for char, expected_type in test_cases:
        is_letter = is_char_letter(char)
        is_digit = is_char_currency(char) if 'Currency' in expected_type else False
        is_currency = is_char_currency(char)
        is_emoji = is_char_emoji(char)
        
        checks = []
        if is_letter:
            checks.append('Letter')
        if is_digit:
            checks.append('Digit')
        if is_currency:
            checks.append('Currency')
        if is_emoji:
            checks.append('Emoji')
        
        result = ', '.join(checks) if checks else 'Other'
        print(f"  '{char}' → Expected: {expected_type}, Actual: {result}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("UNICODE LOOKUP UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_basic_lookup()
    example_character_properties()
    example_full_character_info()
    example_search_characters()
    example_string_analysis()
    example_html_entities()
    example_emoji_handling()
    example_normalization()
    example_width_and_padding()
    example_unicode_escaping()
    example_character_summary()
    example_character_table()
    example_type_checks()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()