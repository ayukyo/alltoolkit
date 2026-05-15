"""
Accent Utils 测试模块

测试文本变音符号处理工具的所有功能。
"""

import unittest
from mod import (
    is_diacritic,
    remove_accents,
    normalize_text,
    has_accents,
    count_accents,
    get_accent_positions,
    find_accented_words,
    compare_accent_insensitive,
    accent_insensitive_search,
    transliterate_to_ascii,
    detect_language_from_accents,
    AccentNormalizer,
    DIACRITIC_RANGES,
    LANGUAGE_MAPPINGS,
)


class TestIsDiacritic(unittest.TestCase):
    """测试 is_diacritic 函数"""
    
    def test_combining_acute_accent(self):
        """测试组合重音符"""
        self.assertTrue(is_diacritic('\u0301'))  # 组合重音符
    
    def test_combining_diaeresis(self):
        """测试组合分音符"""
        self.assertTrue(is_diacritic('\u0308'))  # 组合分音符
    
    def test_regular_character(self):
        """测试普通字符"""
        self.assertFalse(is_diacritic('a'))
        self.assertFalse(is_diacritic('Z'))
        self.assertFalse(is_diacritic('1'))
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertFalse(is_diacritic(''))
    
    def test_diacritic_ranges(self):
        """测试变音符号范围"""
        # 测试范围内的一些字符
        for start, end in DIACRITIC_RANGES:
            # 测试范围开始
            self.assertTrue(is_diacritic(chr(start)))
            # 测试范围中间
            mid = (start + end) // 2
            self.assertTrue(is_diacritic(chr(mid)))


class TestRemoveAccents(unittest.TestCase):
    """测试 remove_accents 函数"""
    
    def test_simple_accent(self):
        """测试简单的变音符号移除"""
        self.assertEqual(remove_accents('café'), 'cafe')
        self.assertEqual(remove_accents('résumé'), 'resume')
    
    def test_multiple_accents(self):
        """测试多个变音符号"""
        self.assertEqual(remove_accents('café au lait'), 'cafe au lait')
        self.assertEqual(remove_accents('über'), 'uber')
    
    def test_no_accents(self):
        """测试无变音符号"""
        self.assertEqual(remove_accents('hello'), 'hello')
        self.assertEqual(remove_accents('Hello World'), 'Hello World')
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(remove_accents(''), '')
    
    def test_german_language(self):
        """测试德语特殊处理"""
        self.assertEqual(remove_accents('über', language='german'), 'ueber')
        self.assertEqual(remove_accents('Äpfel', language='german'), 'Aepfel')
        self.assertEqual(remove_accents('groß', language='german'), 'gross')
    
    def test_french_language(self):
        """测试法语特殊处理"""
        self.assertEqual(remove_accents('cœur', language='french'), 'coeur')
    
    def test_turkish_language(self):
        """测试土耳其语特殊处理"""
        self.assertEqual(remove_accents('İstanbul', language='turkish'), 'Istanbul')
    
    def test_keep_chars(self):
        """测试保留特定字符"""
        # 保留 é 字符
        self.assertEqual(remove_accents('café', keep_chars={'é'}), 'café')
    
    def test_chinese_characters(self):
        """测试中文字符（应该保持不变）"""
        self.assertEqual(remove_accents('你好世界'), '你好世界')


class TestNormalizeText(unittest.TestCase):
    """测试 normalize_text 函数"""
    
    def test_basic_normalization(self):
        """测试基本规范化"""
        self.assertEqual(normalize_text('Café au Lait'), 'cafe au lait')
    
    def test_lowercase(self):
        """测试小写转换"""
        self.assertEqual(normalize_text('HELLO WORLD', lowercase=True), 'hello world')
        self.assertEqual(normalize_text('Hello World', lowercase=False), 'Hello World')
    
    def test_remove_punctuation(self):
        """测试移除标点符号"""
        self.assertEqual(
            normalize_text('Hello, World!', remove_punctuation=True),
            'hello world'
        )
    
    def test_collapse_whitespace(self):
        """测试合并空白字符"""
        self.assertEqual(
            normalize_text('Hello   World', collapse_whitespace=True),
            'hello world'
        )
    
    def test_all_options(self):
        """测试所有选项组合"""
        result = normalize_text(
            '  Café, au Lait!  ',
            lowercase=True,
            remove_accents_flag=True,
            remove_punctuation=True,
            collapse_whitespace=True
        )
        self.assertEqual(result, 'cafe au lait')
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(normalize_text(''), '')


class TestHasAccents(unittest.TestCase):
    """测试 has_accents 函数"""
    
    def test_with_accents(self):
        """测试有变音符号"""
        self.assertTrue(has_accents('café'))
        self.assertTrue(has_accents('résumé'))
        self.assertTrue(has_accents('über'))
    
    def test_without_accents(self):
        """测试无变音符号"""
        self.assertFalse(has_accents('cafe'))
        self.assertFalse(has_accents('resume'))
        self.assertFalse(has_accents('hello'))
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertFalse(has_accents(''))
    
    def test_mixed_text(self):
        """测试混合文本"""
        self.assertTrue(has_accents('Hello café world'))


class TestCountAccents(unittest.TestCase):
    """测试 count_accents 函数"""
    
    def test_single_accent(self):
        """测试单个变音符号"""
        self.assertEqual(count_accents('café'), 1)
    
    def test_multiple_accents(self):
        """测试多个变音符号"""
        self.assertEqual(count_accents('résumé'), 2)
        self.assertEqual(count_accents('café résumé'), 3)  # café(1) + résumé(2)
    
    def test_no_accents(self):
        """测试无变音符号"""
        self.assertEqual(count_accents('cafe'), 0)
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(count_accents(''), 0)
    
    def test_complex_accents(self):
        """测试复杂变音符号"""
        # 某些字符可能有多个组合符号
        self.assertGreater(count_accents('náïve'), 0)


class TestGetAccentPositions(unittest.TestCase):
    """测试 get_accent_positions 函数"""
    
    def test_single_accent_position(self):
        """测试单个变音符号位置"""
        positions = get_accent_positions('café')
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0][0], 3)  # 位置
    
    def test_multiple_accent_positions(self):
        """测试多个变音符号位置"""
        positions = get_accent_positions('résumé')
        self.assertEqual(len(positions), 2)
    
    def test_no_accents(self):
        """测试无变音符号"""
        positions = get_accent_positions('cafe')
        self.assertEqual(len(positions), 0)
    
    def test_empty_string(self):
        """测试空字符串"""
        positions = get_accent_positions('')
        self.assertEqual(len(positions), 0)


class TestFindAccentedWords(unittest.TestCase):
    """测试 find_accented_words 函数"""
    
    def test_find_accented_words(self):
        """测试查找带变音符号的单词"""
        words = find_accented_words('The café has a résumé')
        self.assertIn('café', words)
        self.assertIn('résumé', words)
    
    def test_no_accented_words(self):
        """测试无变音符号的文本"""
        words = find_accented_words('The cafe has a resume')
        self.assertEqual(len(words), 0)
    
    def test_empty_string(self):
        """测试空字符串"""
        words = find_accented_words('')
        self.assertEqual(len(words), 0)


class TestCompareAccentInsensitive(unittest.TestCase):
    """测试 compare_accent_insensitive 函数"""
    
    def test_equal_with_accents(self):
        """测试相等（带变音符号）"""
        self.assertTrue(compare_accent_insensitive('café', 'cafe'))
        self.assertTrue(compare_accent_insensitive('résumé', 'resume'))
    
    def test_equal_both_accented(self):
        """测试相等（都有变音符号）"""
        self.assertTrue(compare_accent_insensitive('café', 'café'))
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertTrue(compare_accent_insensitive('CAFÉ', 'cafe', case_insensitive=True))
        self.assertFalse(compare_accent_insensitive('CAFÉ', 'cafe', case_insensitive=False))
    
    def test_not_equal(self):
        """测试不相等"""
        self.assertFalse(compare_accent_insensitive('café', 'coffee'))
    
    def test_empty_strings(self):
        """测试空字符串"""
        self.assertTrue(compare_accent_insensitive('', ''))


class TestAccentInsensitiveSearch(unittest.TestCase):
    """测试 accent_insensitive_search 函数"""
    
    def test_simple_search(self):
        """测试简单搜索"""
        results = accent_insensitive_search('I love café', 'cafe')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], 'café')
    
    def test_multiple_matches(self):
        """测试多个匹配"""
        results = accent_insensitive_search('café and Café are same', 'cafe')
        self.assertEqual(len(results), 2)
    
    def test_case_insensitive_search(self):
        """测试大小写不敏感搜索"""
        results = accent_insensitive_search('CAFÉ is great', 'cafe', case_insensitive=True)
        self.assertEqual(len(results), 1)
    
    def test_no_matches(self):
        """测试无匹配"""
        results = accent_insensitive_search('Hello World', 'cafe')
        self.assertEqual(len(results), 0)
    
    def test_empty_text(self):
        """测试空文本"""
        results = accent_insensitive_search('', 'cafe')
        self.assertEqual(len(results), 0)


class TestTransliterateToAscii(unittest.TestCase):
    """测试 transliterate_to_ascii 函数"""
    
    def test_basic_transliteration(self):
        """测试基本音译"""
        self.assertEqual(transliterate_to_ascii('café'), 'cafe')
        self.assertEqual(transliterate_to_ascii('résumé'), 'resume')
    
    def test_german_transliteration(self):
        """测试德语音译"""
        self.assertEqual(transliterate_to_ascii('über', language='german'), 'ueber')
    
    def test_chinese_removal(self):
        """测试中文字符移除（非 ASCII）"""
        # 中文字符会被移除
        result = transliterate_to_ascii('你好世界')
        self.assertEqual(result, '')
    
    def test_mixed_text(self):
        """测试混合文本"""
        result = transliterate_to_ascii('Hello café 你好')
        self.assertEqual(result, 'Hello cafe ')


class TestDetectLanguageFromAccents(unittest.TestCase):
    """测试 detect_language_from_accents 函数"""
    
    def test_german_detection(self):
        """测试德语检测"""
        langs = detect_language_from_accents('über')
        self.assertIn('german', langs)
    
    def test_french_detection(self):
        """测试法语检测"""
        langs = detect_language_from_accents('café')
        self.assertIn('french', langs)
    
    def test_spanish_detection(self):
        """测试西班牙语检测"""
        langs = detect_language_from_accents('año')
        self.assertIn('spanish', langs)
    
    def test_portuguese_detection(self):
        """测试葡萄牙语检测"""
        langs = detect_language_from_accents('pão')
        self.assertIn('portuguese', langs)
    
    def test_turkish_detection(self):
        """测试土耳其语检测"""
        langs = detect_language_from_accents('İstanbul')
        self.assertIn('turkish', langs)
    
    def test_no_accents(self):
        """测试无变音符号"""
        langs = detect_language_from_accents('hello')
        self.assertEqual(len(langs), 0)
    
    def test_empty_string(self):
        """测试空字符串"""
        langs = detect_language_from_accents('')
        self.assertEqual(len(langs), 0)


class TestAccentNormalizer(unittest.TestCase):
    """测试 AccentNormalizer 类"""
    
    def test_basic_normalization(self):
        """测试基本规范化"""
        normalizer = AccentNormalizer()
        self.assertEqual(normalizer.normalize('café'), 'cafe')
    
    def test_german_normalization(self):
        """测试德语规范化"""
        normalizer = AccentNormalizer(language='german')
        self.assertEqual(normalizer.normalize('über'), 'ueber')
    
    def test_lowercase_normalization(self):
        """测试小写规范化"""
        normalizer = AccentNormalizer(lowercase=True)
        self.assertEqual(normalizer.normalize('CAFÉ'), 'cafe')
    
    def test_remove_punctuation(self):
        """测试移除标点符号"""
        normalizer = AccentNormalizer(remove_punctuation=True)
        self.assertEqual(normalizer.normalize('café, world!'), 'cafe world')
    
    def test_compare(self):
        """测试比较方法"""
        normalizer = AccentNormalizer()
        self.assertTrue(normalizer.compare('café', 'cafe'))
    
    def test_search(self):
        """测试搜索方法"""
        normalizer = AccentNormalizer()
        results = normalizer.search('I love café', 'cafe')
        self.assertEqual(len(results), 1)


class TestLanguageMappings(unittest.TestCase):
    """测试语言映射常量"""
    
    def test_german_mappings_exist(self):
        """测试德语映射存在"""
        self.assertIn('german', LANGUAGE_MAPPINGS)
        self.assertIn('ä', LANGUAGE_MAPPINGS['german'])
        self.assertIn('ß', LANGUAGE_MAPPINGS['german'])
    
    def test_french_mappings_exist(self):
        """测试法语映射存在"""
        self.assertIn('french', LANGUAGE_MAPPINGS)
        self.assertIn('œ', LANGUAGE_MAPPINGS['french'])
    
    def test_turkish_mappings_exist(self):
        """测试土耳其语映射存在"""
        self.assertIn('turkish', LANGUAGE_MAPPINGS)
        self.assertIn('İ', LANGUAGE_MAPPINGS['turkish'])


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)