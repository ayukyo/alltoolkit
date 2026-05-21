# -*- coding: utf-8 -*-
"""
Typography Utilities Test Suite
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typography_utils import (
    smart_quotes, straighten_quotes,
    normalize_dashes, em_dash, en_dash,
    normalize_ellipsis,
    smartify,
    wrap_text, wrap_paragraphs,
    prevent_widows,
    normalize_spaces, remove_extra_blank_lines,
    count_chars, count_words, count_sentences, count_paragraphs, text_statistics,
    escape_html, unescape_html, escape_markdown,
    title_case, slugify,
    add_line_numbers,
    align_left, align_right, align_center, align_justify,
    normalize_chinese_punctuation, chinese_paragraph_indent,
)


class TestSmartQuotes(unittest.TestCase):
    def test_basic_double_quotes(self):
        result = smart_quotes('He said "hello".')
        self.assertIn('"', result)
        self.assertIn('"', result)

    def test_straighten_quotes(self):
        text = 'He said "hello".'
        result = straighten_quotes(text)
        self.assertEqual(result.count('"'), 2)


class TestDashNormalization(unittest.TestCase):
    def test_range_dash(self):
        result = normalize_dashes('pages 10--20')
        self.assertIn('\u2013', result)  # en dash

    def test_em_dash(self):
        result = em_dash('thought -- or idea')
        self.assertIn('\u2014', result)  # em dash

    def test_hyphen_style(self):
        result = normalize_dashes('a--b', style='hyphen')
        self.assertEqual(result, 'a-b')


class TestEllipsisNormalization(unittest.TestCase):
    def test_three_dots_to_char(self):
        result = normalize_ellipsis('Wait...')
        self.assertEqual(result, 'Wait\u2026')

    def test_keep_three_dots(self):
        result = normalize_ellipsis('Wait...', use_char=False)
        self.assertEqual(result, 'Wait...')


class TestSmartify(unittest.TestCase):
    def test_all_features(self):
        text = 'He said "hello"... wait -- I mean "hi".'
        result = smartify(text)
        self.assertIn('"', result)
        self.assertIn('\u2026', result)  # ellipsis
        self.assertIn('\u2014', result)  # em dash


class TestTextWrapping(unittest.TestCase):
    def test_basic_wrap(self):
        text = 'This is a long text that needs to be wrapped.'
        result = wrap_text(text, width=20)
        lines = result.split('\n')
        for line in lines:
            self.assertLessEqual(len(line), 20)


class TestSpaceNormalization(unittest.TestCase):
    def test_multiple_spaces(self):
        result = normalize_spaces('hello    world')
        self.assertEqual(result, 'hello world')

    def test_leading_trailing_spaces(self):
        result = normalize_spaces('  hello world  ')
        self.assertEqual(result, 'hello world')


class TestCharacterCounting(unittest.TestCase):
    def test_count_chars(self):
        self.assertEqual(count_chars('hello'), 5)
        self.assertEqual(count_chars('hello world', include_spaces=False), 10)

    def test_count_words_english(self):
        self.assertEqual(count_words('hello world'), 2)

    def test_count_words_chinese(self):
        self.assertEqual(count_words('\u4f60\u597d\u4e16\u754c'), 4)

    def test_count_sentences(self):
        self.assertEqual(count_sentences('Hello. World!'), 2)

    def test_text_statistics(self):
        stats = text_statistics('Hello world.')
        self.assertEqual(stats['words'], 2)
        self.assertEqual(stats['sentences'], 1)


class TestHTMLEscaping(unittest.TestCase):
    def test_escape_html(self):
        result = escape_html('<div>Hello & Goodbye</div>')
        self.assertIn('&lt;', result)
        self.assertIn('&gt;', result)
        self.assertIn('&amp;', result)

    def test_unescape_html(self):
        result = unescape_html('&lt;div&gt;Hello&lt;/div&gt;')
        self.assertEqual(result, '<div>Hello</div>')


class TestTitleCase(unittest.TestCase):
    def test_basic_title_case(self):
        result = title_case('the quick brown fox')
        self.assertEqual(result, 'The Quick Brown Fox')

    def test_with_exceptions(self):
        result = title_case('the lord of the rings', exceptions=['the', 'of'])
        self.assertEqual(result, 'The Lord of the Rings')


class TestSlugify(unittest.TestCase):
    def test_basic_slug(self):
        result = slugify('Hello World!')
        self.assertEqual(result, 'hello-world')

    def test_custom_separator(self):
        result = slugify('Hello World', separator='_')
        self.assertEqual(result, 'hello_world')


class TestLineNumbers(unittest.TestCase):
    def test_add_line_numbers(self):
        text = 'Hello\nWorld'
        result = add_line_numbers(text)
        self.assertIn('1', result)
        self.assertIn('2', result)


class TestAlignment(unittest.TestCase):
    def test_align_left(self):
        result = align_left('Hello', 10)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.startswith('Hello'))

    def test_align_right(self):
        result = align_right('Hello', 10)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.endswith('Hello'))

    def test_align_center(self):
        result = align_center('Hi', 6)
        self.assertEqual(len(result), 6)


class TestChineseTypography(unittest.TestCase):
    def test_normalize_chinese_punctuation(self):
        result = normalize_chinese_punctuation('\u4f60\u597d,\u4e16\u754c!')
        self.assertIn('\uff0c', result)  # Chinese comma
        self.assertIn('\uff01', result)  # Chinese exclamation

    def test_chinese_paragraph_indent(self):
        text = '\u7b2c\u4e00\u6bb5\n\n\u7b2c\u4e8c\u6bb5'
        result = chinese_paragraph_indent(text)
        self.assertTrue(result.startswith('\u3000\u3000'))


class TestEdgeCases(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(smart_quotes(''), '')
        self.assertEqual(normalize_dashes(''), '')
        self.assertEqual(normalize_ellipsis(''), '')

    def test_single_character(self):
        self.assertEqual(smart_quotes('a'), 'a')
        self.assertEqual(normalize_spaces(' '), '')


if __name__ == '__main__':
    unittest.main(verbosity=2)