"""
Unicode Lookup Utilities - Test Suite

Comprehensive tests for all Unicode lookup utility functions.
"""

import unittest
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
    get_block_by_name,
    list_block_characters,
    search_by_name,
    search_by_category,
    get_full_info,
    UnicodeCharInfo,
    get_char_width,
    get_script,
    get_html_entity_named,
    is_char_printable,
    is_char_whitespace,
    is_char_control,
    is_char_letter,
    is_char_digit,
    is_char_numeric,
    is_char_punctuation,
    is_char_symbol,
    is_char_mark,
    is_char_currency,
    is_char_math,
    is_char_emoji,
    normalize_char,
    decompose_char,
    compose_char,
    analyze_string,
    get_string_info,
    convert_to_html_entities,
    convert_from_html_entities,
    get_unicode_version,
    is_valid_unicode,
    get_similar_chars,
    print_char_table,
    escape_unicode,
    unescape_unicode,
    get_combining_chain,
    strip_combining_marks,
    count_width,
    pad_unicode,
    get_unicode_plane,
    list_emojis,
    get_named_entity_list,
    validate_code_point,
    get_char_summary,
    UnicodeCategory,
    UNICODE_BLOCKS,
)


class TestCharNameLookup(unittest.TestCase):
    """Test character name lookup functions."""
    
    def test_get_char_name_basic(self):
        """Test basic character name lookup."""
        self.assertEqual(get_char_name('A'), 'LATIN CAPITAL LETTER A')
        self.assertEqual(get_char_name('a'), 'LATIN SMALL LETTER A')
        self.assertEqual(get_char_name('0'), 'DIGIT ZERO')
        self.assertEqual(get_char_name(' '), 'SPACE')
    
    def test_get_char_name_cjk(self):
        """Test CJK character name lookup."""
        self.assertEqual(get_char_name('中'), 'CJK UNIFIED IDEOGRAPH-4E2D')
        self.assertEqual(get_char_name('日'), 'CJK UNIFIED IDEOGRAPH-65E5')
    
    def test_get_char_name_special(self):
        """Test special character name lookup."""
        self.assertEqual(get_char_name('©'), 'COPYRIGHT SIGN')
        self.assertEqual(get_char_name('€'), 'EURO SIGN')
        self.assertEqual(get_char_name('☃'), 'SNOWMAN')
    
    def test_get_char_name_error(self):
        """Test error handling for invalid input."""
        with self.assertRaises(ValueError):
            get_char_name('AB')  # More than one character
    
    def test_get_char_by_name_basic(self):
        """Test getting character by name."""
        self.assertEqual(get_char_by_name('LATIN CAPITAL LETTER A'), 'A')
        self.assertEqual(get_char_by_name('SNOWMAN'), '☃')
        self.assertEqual(get_char_by_name('COPYRIGHT SIGN'), '©')
    
    def test_get_char_by_name_not_found(self):
        """Test getting character by invalid name."""
        self.assertIsNone(get_char_by_name('INVALID NAME'))
        self.assertIsNone(get_char_by_name(''))


class TestCodePointFunctions(unittest.TestCase):
    """Test code point related functions."""
    
    def test_get_code_point(self):
        """Test getting code point from character."""
        self.assertEqual(get_code_point('A'), 65)
        self.assertEqual(get_code_point('中'), 20013)
        self.assertEqual(get_code_point('€'), 8364)
    
    def test_get_char_by_code_point(self):
        """Test getting character from code point."""
        self.assertEqual(get_char_by_code_point(65), 'A')
        self.assertEqual(get_char_by_code_point(20013), '中')
        self.assertEqual(get_char_by_code_point(8364), '€')
    
    def test_get_char_by_code_point_invalid(self):
        """Test invalid code point handling."""
        with self.assertRaises(ValueError):
            get_char_by_code_point(-1)
        with self.assertRaises(ValueError):
            get_char_by_code_point(0x11FFFF)
    
    def test_validate_code_point(self):
        """Test code point validation."""
        self.assertTrue(validate_code_point(0))
        self.assertTrue(validate_code_point(65))
        self.assertTrue(validate_code_point(0x10FFFF))
        self.assertFalse(validate_code_point(-1))
        self.assertFalse(validate_code_point(0x11FFFF))
        # Surrogate range should be invalid
        self.assertFalse(validate_code_point(0xD800))
        self.assertFalse(validate_code_point(0xDFFF))


class TestCategoryFunctions(unittest.TestCase):
    """Test Unicode category functions."""
    
    def test_get_category(self):
        """Test getting character category."""
        self.assertEqual(get_category('A'), 'Lu')  # Letter, uppercase
        self.assertEqual(get_category('a'), 'Ll')  # Letter, lowercase
        self.assertEqual(get_category('5'), 'Nd')  # Number, decimal digit
        self.assertEqual(get_category(' '), 'Zs')  # Separator, space
        self.assertEqual(get_category('.'), 'Po')  # Punctuation, other
        self.assertEqual(get_category('+'), 'Sm')  # Symbol, math
        self.assertEqual(get_category('$'), 'Sc')  # Symbol, currency
    
    def test_get_category_name(self):
        """Test getting category human-readable name."""
        self.assertEqual(get_category_name('Lu'), 'Letter, uppercase')
        self.assertEqual(get_category_name('Ll'), 'Letter, lowercase')
        self.assertEqual(get_category_name('Nd'), 'Number, decimal digit')
        self.assertEqual(get_category_name('Zs'), 'Separator, space')
        self.assertEqual(get_category_name('XX'), 'Unknown category: XX')


class TestBlockFunctions(unittest.TestCase):
    """Test Unicode block functions."""
    
    def test_get_block_basic(self):
        """Test getting character block."""
        self.assertEqual(get_block('A'), 'Basic Latin')
        self.assertEqual(get_block('é'), 'Latin-1 Supplement')
        self.assertEqual(get_block('中'), 'CJK Unified Ideographs')
        self.assertEqual(get_block('☃'), 'Miscellaneous Symbols')
    
    def test_get_block_by_name(self):
        """Test getting block range by name."""
        self.assertEqual(get_block_by_name('Basic Latin'), (0x0000, 0x007F))
        self.assertEqual(get_block_by_name('CJK Unified Ideographs'), (0x4E00, 0x9FFF))
        self.assertIsNone(get_block_by_name('Invalid Block'))
    
    def test_list_block_characters(self):
        """Test listing characters in a block."""
        chars = list_block_characters('Basic Latin', limit=100)
        self.assertGreaterEqual(len(chars), 50)
        # Printable chars should be in the list
        self.assertIn('A', chars)
        self.assertIn('a', chars)
        # Control chars should NOT be in the list
        self.assertNotIn('\x00', chars)
        self.assertNotIn('\t', chars)
    
    def test_unicode_blocks_dict(self):
        """Test UNICODE_BLOCKS dictionary."""
        self.assertIsInstance(UNICODE_BLOCKS, dict)
        self.assertGreater(len(UNICODE_BLOCKS), 50)
        # Check some major blocks
        self.assertIn('Basic Latin', UNICODE_BLOCKS)
        self.assertIn('CJK Unified Ideographs', UNICODE_BLOCKS)


class TestSearchFunctions(unittest.TestCase):
    """Test search functions."""
    
    def test_search_by_name(self):
        """Test searching characters by name keyword."""
        results = search_by_name('snowman', limit=10)
        self.assertGreater(len(results), 0)
        # SNOWMAN should be in results
        snowman_in_results = any(r['char'] == '☃' for r in results)
        self.assertTrue(snowman_in_results, "SNOWMAN ☃ should be found")
        
        results = search_by_name('COPYRIGHT', limit=10)
        self.assertGreater(len(results), 0)
        self.assertIn('©', [r['char'] for r in results])
    
    def test_search_by_category(self):
        """Test searching by category."""
        chars = search_by_category('Sc')  # Currency symbols
        self.assertIn('$', chars)
        self.assertIn('€', chars)
        self.assertIn('¥', chars)
        self.assertIn('£', chars)


class TestFullInfo(unittest.TestCase):
    """Test full character info function."""
    
    def test_get_full_info_basic(self):
        """Test getting full info for basic character."""
        info = get_full_info('A')
        
        self.assertEqual(info.char, 'A')
        self.assertEqual(info.code_point, 65)
        self.assertEqual(info.name, 'LATIN CAPITAL LETTER A')
        self.assertEqual(info.category, 'Lu')
        self.assertEqual(info.category_name, 'Letter, uppercase')
        self.assertEqual(info.block, 'Basic Latin')
        self.assertEqual(info.script, 'Latin')
        
        # Test type checks
        self.assertTrue(info.is_letter)
        self.assertFalse(info.is_digit)
        self.assertTrue(info.is_printable)
        self.assertFalse(info.is_whitespace)
    
    def test_get_full_info_cjk(self):
        """Test getting full info for CJK character."""
        info = get_full_info('中')
        
        self.assertEqual(info.char, '中')
        self.assertEqual(info.code_point, 20013)
        self.assertEqual(info.category, 'Lo')  # Letter, other
        self.assertEqual(info.block, 'CJK Unified Ideographs')
        self.assertEqual(info.script, 'CJK')
        self.assertEqual(info.width, 'wide')
    
    def test_get_full_info_digit(self):
        """Test getting full info for digit."""
        info = get_full_info('5')
        
        self.assertEqual(info.char, '5')
        self.assertEqual(info.category, 'Nd')
        self.assertTrue(info.is_digit)
        self.assertTrue(info.is_numeric)
        self.assertEqual(info.decimal_value, 5)
        self.assertEqual(info.digit_value, 5)
        self.assertEqual(info.numeric_value, 5.0)
    
    def test_get_full_info_currency(self):
        """Test getting full info for currency symbol."""
        info = get_full_info('$')
        
        self.assertEqual(info.char, '$')
        self.assertEqual(info.category, 'Sc')
        self.assertTrue(info.is_currency)
        self.assertTrue(info.is_symbol)
    
    def test_get_full_info_case_mapping(self):
        """Test case mapping properties."""
        info_upper = get_full_info('A')
        self.assertEqual(info_upper.lowercase, 'a')
        self.assertIsNone(info_upper.uppercase)
        
        info_lower = get_full_info('a')
        self.assertEqual(info_lower.uppercase, 'A')
        self.assertIsNone(info_lower.lowercase)
    
    def test_get_full_info_html_entities(self):
        """Test HTML entity properties."""
        info = get_full_info('<')
        self.assertEqual(info.html_entity_decimal, '&#60;')
        self.assertEqual(info.html_entity_hex, '&#x003C;')
        self.assertEqual(info.html_entity_named, '&lt;')
        
        info = get_full_info('中')
        self.assertEqual(info.html_entity_decimal, '&#20013;')
        self.assertEqual(info.html_entity_hex, '&#x4E2D;')
        self.assertIsNone(info.html_entity_named)
    
    def test_get_full_info_encoding(self):
        """Test encoding properties."""
        info = get_full_info('A')
        self.assertEqual(info.utf8_bytes, b'A')
        self.assertEqual(info.utf8_hex, '41')
        
        info = get_full_info('中')
        self.assertEqual(len(info.utf8_bytes), 3)  # UTF-8 uses 3 bytes for CJK
        self.assertEqual(len(info.utf16_bytes), 2)
    
    def test_get_full_info_error(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            get_full_info('AB')


class TestCharacterTypeChecks(unittest.TestCase):
    """Test character type checking functions."""
    
    def test_is_char_printable(self):
        """Test printable character check."""
        self.assertTrue(is_char_printable('A'))
        self.assertTrue(is_char_printable('中'))
        self.assertTrue(is_char_printable(' '))
        self.assertFalse(is_char_printable('\x00'))  # Control char
        self.assertFalse(is_char_printable('\n'))
    
    def test_is_char_whitespace(self):
        """Test whitespace character check."""
        self.assertTrue(is_char_whitespace(' '))
        self.assertTrue(is_char_whitespace('\t'))
        self.assertTrue(is_char_whitespace('\n'))
        self.assertFalse(is_char_whitespace('A'))
    
    def test_is_char_control(self):
        """Test control character check."""
        self.assertTrue(is_char_control('\x00'))
        self.assertTrue(is_char_control('\n'))
        self.assertTrue(is_char_control('\t'))
        self.assertFalse(is_char_control('A'))
    
    def test_is_char_letter(self):
        """Test letter character check."""
        self.assertTrue(is_char_letter('A'))
        self.assertTrue(is_char_letter('a'))
        self.assertTrue(is_char_letter('中'))
        self.assertTrue(is_char_letter('あ'))
        self.assertFalse(is_char_letter('5'))
        self.assertFalse(is_char_letter('$'))
    
    def test_is_char_digit(self):
        """Test digit character check."""
        self.assertTrue(is_char_digit('0'))
        self.assertTrue(is_char_digit('5'))
        self.assertTrue(is_char_digit('9'))
        self.assertFalse(is_char_digit('A'))
        self.assertFalse(is_char_digit('五'))  # Chinese number is not Nd
    
    def test_is_char_numeric(self):
        """Test numeric character check."""
        self.assertTrue(is_char_numeric('0'))
        self.assertTrue(is_char_numeric('5'))
        self.assertFalse(is_char_numeric('A'))
    
    def test_is_char_punctuation(self):
        """Test punctuation character check."""
        self.assertTrue(is_char_punctuation('.'))
        self.assertTrue(is_char_punctuation(','))
        self.assertTrue(is_char_punctuation('!'))
        self.assertTrue(is_char_punctuation('?'))
        self.assertTrue(is_char_punctuation('('))
        self.assertTrue(is_char_punctuation(')'))
        self.assertFalse(is_char_punctuation('A'))
    
    def test_is_char_symbol(self):
        """Test symbol character check."""
        self.assertTrue(is_char_symbol('+'))
        self.assertTrue(is_char_symbol('='))
        self.assertTrue(is_char_symbol('$'))
        self.assertFalse(is_char_symbol('A'))
    
    def test_is_char_currency(self):
        """Test currency symbol check."""
        self.assertTrue(is_char_currency('$'))
        self.assertTrue(is_char_currency('€'))
        self.assertTrue(is_char_currency('¥'))
        self.assertTrue(is_char_currency('£'))
        self.assertFalse(is_char_currency('A'))
    
    def test_is_char_math(self):
        """Test math symbol check."""
        self.assertTrue(is_char_math('+'))
        self.assertTrue(is_char_math('='))
        self.assertTrue(is_char_math('×'))
        self.assertFalse(is_char_math('$'))
    
    def test_is_char_emoji(self):
        """Test emoji character check."""
        self.assertTrue(is_char_emoji('😀'))
        self.assertTrue(is_char_emoji('🎉'))
        self.assertFalse(is_char_emoji('A'))
        self.assertFalse(is_char_emoji('中'))


class TestWidthAndScript(unittest.TestCase):
    """Test width and script functions."""
    
    def test_get_char_width(self):
        """Test character width estimation."""
        self.assertEqual(get_char_width('A'), 'narrow')
        self.assertEqual(get_char_width('中'), 'wide')
        self.assertEqual(get_char_width('あ'), 'wide')
        # € (U+20AC) is narrow in most contexts (East Asian Width: Na)
        self.assertEqual(get_char_width('€'), 'narrow')
    
    def test_get_script(self):
        """Test script estimation."""
        self.assertEqual(get_script('A'), 'Latin')
        self.assertEqual(get_script('中'), 'CJK')
        self.assertEqual(get_script('あ'), 'Hiragana')
        self.assertEqual(get_script('ア'), 'Katakana')
        self.assertEqual(get_script('α'), 'Greek')
        self.assertEqual(get_script('€'), 'Currency')


class TestNormalization(unittest.TestCase):
    """Test Unicode normalization functions."""
    
    def test_normalize_char(self):
        """Test character normalization."""
        # NFC (compose)
        self.assertEqual(normalize_char('e\u0301', 'NFC'), 'é')
        # NFD (decompose)
        self.assertEqual(normalize_char('é', 'NFD'), 'e\u0301')
    
    def test_decompose_char(self):
        """Test character decomposition."""
        base, marks = decompose_char('é')
        self.assertEqual(base, 'e')
        self.assertEqual(len(marks), 1)
        self.assertEqual(marks[0], '\u0301')  # COMBINING ACUTE ACCENT
        
        base, marks = decompose_char('ã')
        self.assertEqual(base, 'a')
        self.assertEqual(len(marks), 1)
        self.assertEqual(marks[0], '\u0303')  # COMBINING TILDE
    
    def test_compose_char(self):
        """Test character composition."""
        self.assertEqual(compose_char('e', ['\u0301']), 'é')
        self.assertEqual(compose_char('a', ['\u0303']), 'ã')
    
    def test_get_combining_chain(self):
        """Test combining chain extraction."""
        chain = get_combining_chain('é')
        self.assertEqual(chain, ['e', '\u0301'])


class TestStringAnalysis(unittest.TestCase):
    """Test string analysis functions."""
    
    def test_analyze_string_basic(self):
        """Test basic string analysis."""
        stats = analyze_string('Hello World')
        
        self.assertEqual(stats['total_chars'], 11)
        self.assertEqual(stats['letter_count'], 10)
        self.assertEqual(stats['whitespace_count'], 1)
        self.assertFalse(stats['has_non_ascii'])
    
    def test_analyze_string_mixed(self):
        """Test mixed string analysis."""
        stats = analyze_string('Hello 世界! 🌍')
        
        self.assertEqual(stats['total_chars'], 11)
        self.assertEqual(stats['letter_count'], 7)  # Hello + 中 + 世
        self.assertTrue(stats['has_non_ascii'])
        self.assertTrue(stats['has_emoji'])
        self.assertGreater(stats['punctuation_count'], 0)
    
    def test_analyze_string_empty(self):
        """Test empty string analysis."""
        stats = analyze_string('')
        
        self.assertEqual(stats['total_chars'], 0)
        self.assertEqual(stats['letter_count'], 0)
    
    def test_analyze_string_distribution(self):
        """Test character distribution analysis."""
        stats = analyze_string('A中€😀')
        
        self.assertIn('Basic Latin', stats['block_distribution'])
        self.assertIn('CJK Unified Ideographs', stats['block_distribution'])
        self.assertIn('Currency Symbols', stats['block_distribution'])
        
        self.assertIn('Latin', stats['script_distribution'])
        self.assertIn('CJK', stats['script_distribution'])
    
    def test_get_string_info(self):
        """Test getting string info."""
        info = get_string_info('AB')
        
        self.assertEqual(len(info), 2)
        self.assertEqual(info[0]['char'], 'A')
        self.assertEqual(info[0]['name'], 'LATIN CAPITAL LETTER A')
        self.assertEqual(info[1]['char'], 'B')


class TestHTMLEntities(unittest.TestCase):
    """Test HTML entity functions."""
    
    def test_get_html_entity_named(self):
        """Test getting named HTML entity."""
        self.assertEqual(get_html_entity_named('<'), '&lt;')
        self.assertEqual(get_html_entity_named('>'), '&gt;')
        self.assertEqual(get_html_entity_named('&'), '&amp;')
        self.assertEqual(get_html_entity_named('©'), '&copy;')
        self.assertEqual(get_html_entity_named('€'), '&euro;')
        self.assertIsNone(get_html_entity_named('A'))
    
    def test_convert_to_html_entities(self):
        """Test converting to HTML entities."""
        self.assertEqual(convert_to_html_entities('<>'), '&lt;&gt;')
        self.assertEqual(convert_to_html_entities('中'), '&#x4E2D;')
        self.assertEqual(convert_to_html_entities('A'), 'A')  # ASCII preserved
    
    def test_convert_from_html_entities(self):
        """Test converting from HTML entities."""
        self.assertEqual(convert_from_html_entities('&lt;&gt;'), '<>')
        self.assertEqual(convert_from_html_entities('&#x4E2D;'), '中')
        self.assertEqual(convert_from_html_entities('&#65;'), 'A')
        self.assertEqual(convert_from_html_entities('&euro;'), '€')
    
    def test_get_named_entity_list(self):
        """Test getting named entity list."""
        entities = get_named_entity_list()
        
        self.assertIsInstance(entities, dict)
        self.assertGreater(len(entities), 30)
        self.assertEqual(entities['&lt;'], '<')
        self.assertEqual(entities['&euro;'], '€')


class TestMiscellaneous(unittest.TestCase):
    """Test miscellaneous functions."""
    
    def test_get_unicode_version(self):
        """Test Unicode version estimation."""
        self.assertEqual(get_unicode_version('A'), '1.0')
        self.assertEqual(get_unicode_version('€'), '2.0')
        self.assertEqual(get_unicode_version('😀'), '6.0')
    
    def test_is_valid_unicode(self):
        """Test Unicode validation."""
        self.assertTrue(is_valid_unicode('Hello'))
        self.assertTrue(is_valid_unicode('世界'))
        # Lone surrogate should be invalid
        self.assertFalse(is_valid_unicode('\uD800'))
    
    def test_strip_combining_marks(self):
        """Test stripping combining marks."""
        self.assertEqual(strip_combining_marks('éàü'), 'eau')
        self.assertEqual(strip_combining_marks('café'), 'cafe')
    
    def test_count_width(self):
        """Test width counting."""
        self.assertEqual(count_width('Hello'), 5)
        self.assertEqual(count_width('你好'), 4)  # Each CJK is 2 wide
        self.assertEqual(count_width('Hello世界'), 9)  # 5 + 4
    
    def test_pad_unicode(self):
        """Test Unicode padding."""
        self.assertEqual(pad_unicode('你好', 6), '你好  ')
        self.assertEqual(pad_unicode('你好', 6, align='right'), '  你好')
        self.assertEqual(pad_unicode('你好', 6, align='center'), ' 你好 ')
    
    def test_escape_unicode(self):
        """Test Unicode escaping."""
        # Test with actual Chinese characters
        test_str = 'Hello 世界'
        escaped = escape_unicode(test_str)
        # Check that non-ASCII chars are escaped
        self.assertIn('\\u', escaped)
        self.assertTrue(escaped.startswith('Hello '))
        
        # Test escape all
        self.assertEqual(escape_unicode('Hello', escape_all=True), '\\u0048\\u0065\\u006c\\u006c\\u006f')
    
    def test_unescape_unicode(self):
        """Test Unicode unescaping."""
        # Test with escaped Chinese characters
        escaped_str = 'Hello \\u4e16\\u754c'  # 世界
        unescaped = unescape_unicode(escaped_str)
        self.assertEqual(unescaped, 'Hello 世界')
    
    def test_get_unicode_plane(self):
        """Test Unicode plane identification."""
        self.assertEqual(get_unicode_plane(65), 'Basic Multilingual Plane (BMP)')
        self.assertEqual(get_unicode_plane(0x1F600), 'Supplementary Multilingual Plane (SMP)')
    
    def test_list_emojis(self):
        """Test emoji listing."""
        emojis = list_emojis(limit=20)
        self.assertGreater(len(emojis), 0)
        self.assertLessEqual(len(emojis), 20)
        
        faces = list_emojis('face', limit=10)
        self.assertGreater(len(faces), 0)
        # All should be emoji
        for e in emojis:
            self.assertTrue(is_char_emoji(e['char']))
    
    def test_get_char_summary(self):
        """Test character summary."""
        summary = get_char_summary('A')
        self.assertIn('A', summary)
        self.assertIn('LATIN CAPITAL LETTER A', summary)
        self.assertIn('Letter, uppercase', summary)


class TestPrintCharTable(unittest.TestCase):
    """Test character table printing."""
    
    def test_print_char_table_basic(self):
        """Test basic table printing."""
        table = print_char_table(['A', 'B', 'C'])
        
        self.assertIn('A', table)
        self.assertIn('B', table)
        self.assertIn('C', table)
        self.assertIn('U+0041', table)
    
    def test_print_char_table_empty(self):
        """Test empty table."""
        self.assertEqual(print_char_table([]), '')


class TestUnicodeCategoryEnum(unittest.TestCase):
    """Test Unicode category enum."""
    
    def test_category_enum_values(self):
        """Test category enum values."""
        self.assertEqual(UnicodeCategory.LU.value, 'Lu')
        self.assertEqual(UnicodeCategory.LL.value, 'Ll')
        self.assertEqual(UnicodeCategory.ND.value, 'Nd')
        self.assertEqual(UnicodeCategory.SM.value, 'Sm')


if __name__ == '__main__':
    unittest.main(verbosity=2)