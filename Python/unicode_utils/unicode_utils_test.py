"""
Unicode Utilities 测试文件

测试所有 unicode_utils 功能
"""

import unittest
from mod import (
    get_char_info,
    is_emoji,
    is_zero_width,
    contains_emoji,
    contains_zero_width,
    remove_zero_width,
    get_all_emojis,
    normalize_text,
    get_string_stats,
    codepoint_to_char,
    char_to_codepoint,
    string_to_codepoints,
    codepoints_to_string,
    hex_to_char,
    char_to_hex,
    is_valid_unicode,
    get_chars_in_range,
    get_chars_by_category,
    get_name,
    get_chars_by_name,
    detect_encoding,
    strip_invisible,
    is_printable,
    is_rtl,
    is_combining,
    strip_diacritics,
    get_unicode_version,
    info,
    search,
    stats,
)


class TestCharInfo(unittest.TestCase):
    """测试字符信息获取"""
    
    def test_ascii_letter(self):
        """测试 ASCII 字母"""
        char_info = get_char_info('A')
        self.assertEqual(char_info.char, 'A')
        self.assertEqual(char_info.codepoint, 65)
        self.assertEqual(char_info.hex_code, 'U+0041')
        self.assertEqual(char_info.category, 'Lu')
        self.assertTrue(char_info.is_letter)
        self.assertFalse(char_info.is_digit)
        self.assertEqual(char_info.script, 'Latin')
    
    def test_ascii_digit(self):
        """测试 ASCII 数字"""
        char_info = get_char_info('5')
        self.assertEqual(char_info.codepoint, 53)
        self.assertEqual(char_info.category, 'Nd')
        self.assertTrue(char_info.is_digit)
        self.assertFalse(char_info.is_letter)
    
    def test_chinese_character(self):
        """测试中文字符"""
        char_info = get_char_info('中')
        self.assertEqual(char_info.codepoint, 20013)
        self.assertEqual(char_info.hex_code, 'U+4E2D')
        self.assertEqual(char_info.script, 'Han')
        self.assertEqual(char_info.category, 'Lo')
    
    def test_emoji(self):
        """测试表情符号"""
        char_info = get_char_info('😀')
        self.assertEqual(char_info.codepoint, 128512)
        self.assertEqual(char_info.hex_code, 'U+1F600')
        self.assertTrue(char_info.is_emoji)
    
    def test_zero_width(self):
        """测试零宽字符"""
        char_info = get_char_info('\u200B')  # Zero Width Space
        self.assertTrue(char_info.is_zero_width)
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            get_char_info('AB')  # 多字符
    
    def test_uppercase_mapping(self):
        """测试大小写映射"""
        char_info = get_char_info('a')
        self.assertEqual(char_info.uppercase, 'A')
        self.assertIsNone(char_info.lowercase)
    
    def test_lowercase_mapping(self):
        """测试大小写映射"""
        char_info = get_char_info('A')
        self.assertEqual(char_info.lowercase, 'a')
        self.assertIsNone(char_info.uppercase)


class TestEmojiDetection(unittest.TestCase):
    """测试表情符号检测"""
    
    def test_simple_emoji(self):
        """测试简单表情符号"""
        self.assertTrue(is_emoji('😀'))
        self.assertTrue(is_emoji('❤'))
        self.assertTrue(is_emoji('🔥'))
    
    def test_non_emoji(self):
        """测试非表情符号"""
        self.assertFalse(is_emoji('A'))
        self.assertFalse(is_emoji('中'))
        self.assertFalse(is_emoji(' '))
    
    def test_contains_emoji(self):
        """测试字符串包含表情符号"""
        self.assertTrue(contains_emoji('Hello 😃 World'))
        self.assertFalse(contains_emoji('Hello World'))
    
    def test_get_all_emojis(self):
        """测试获取所有表情符号"""
        emojis = get_all_emojis('I ❤️ Python! 😃')
        self.assertIn('❤', emojis)
        self.assertIn('😃', emojis)


class TestZeroWidth(unittest.TestCase):
    """测试零宽字符"""
    
    def test_zero_width_detection(self):
        """测试零宽字符检测"""
        self.assertTrue(is_zero_width('\u200B'))  # Zero Width Space
        self.assertTrue(is_zero_width('\u200C'))  # Zero Width Non-Joiner
        self.assertTrue(is_zero_width('\u200D'))  # Zero Width Joiner
        self.assertFalse(is_zero_width('A'))
    
    def test_contains_zero_width(self):
        """测试字符串包含零宽字符"""
        self.assertTrue(contains_zero_width('Hello\u200BWorld'))
        self.assertFalse(contains_zero_width('Hello World'))
    
    def test_remove_zero_width(self):
        """测试移除零宽字符"""
        result = remove_zero_width('Hello\u200B\u200CWorld')
        self.assertEqual(result, 'HelloWorld')


class TestNormalization(unittest.TestCase):
    """测试 Unicode 规范化"""
    
    def test_nfc_normalization(self):
        """测试 NFC 规范化"""
        # 组合字符与预组合字符
        text = 'é'  # 预组合
        normalized = normalize_text(text, 'NFC')
        self.assertEqual(normalized, 'é')
    
    def test_nfd_normalization(self):
        """测试 NFD 规范化"""
        text = 'é'  # 预组合
        normalized = normalize_text(text, 'NFD')
        # NFD 会分解为 e + 组合重音符号
        self.assertEqual(len(normalized), 2)
    
    def test_nfkc_normalization(self):
        """测试 NFKC 规范化"""
        text = 'ℌ'  # 数学符号 H
        normalized = normalize_text(text, 'NFKC')
        self.assertEqual(normalized, 'H')


class TestStringStats(unittest.TestCase):
    """测试字符串统计"""
    
    def test_simple_stats(self):
        """测试简单字符串统计"""
        stats = get_string_stats('Hello World')
        self.assertEqual(stats['length'], 11)
        self.assertEqual(stats['letters'], 10)
        self.assertEqual(stats['whitespace'], 1)
        self.assertEqual(stats['digits'], 0)
    
    def test_mixed_stats(self):
        """测试混合字符串统计"""
        stats = get_string_stats('Hello123! 你好')
        # Hello (5个字母) + 你好 (2个中文字母) = 7 个字母
        self.assertEqual(stats['letters'], 7)
        self.assertEqual(stats['digits'], 3)
        self.assertGreater(stats['punctuation'], 0)
        self.assertIn('Han', stats['scripts'])
    
    def test_emoji_stats(self):
        """测试表情符号统计"""
        stats = get_string_stats('Hello 😃 World! 🌍')
        self.assertEqual(stats['emoji_count'], 2)


class TestCodepointConversion(unittest.TestCase):
    """测试码点转换"""
    
    def test_codepoint_to_char(self):
        """测试码点转字符"""
        self.assertEqual(codepoint_to_char(65), 'A')
        self.assertEqual(codepoint_to_char(128512), '😀')
        self.assertEqual(codepoint_to_char(20013), '中')
    
    def test_char_to_codepoint(self):
        """测试字符转码点"""
        self.assertEqual(char_to_codepoint('A'), 65)
        self.assertEqual(char_to_codepoint('中'), 20013)
    
    def test_string_to_codepoints(self):
        """测试字符串转码点列表"""
        codepoints = string_to_codepoints('AB')
        self.assertEqual(codepoints, [65, 66])
    
    def test_codepoints_to_string(self):
        """测试码点列表转字符串"""
        text = codepoints_to_string([65, 66])
        self.assertEqual(text, 'AB')
    
    def test_hex_to_char(self):
        """测试十六进制转字符"""
        self.assertEqual(hex_to_char('0041'), 'A')
        self.assertEqual(hex_to_char('U+0041'), 'A')
        self.assertEqual(hex_to_char('1F600'), '😀')
    
    def test_char_to_hex(self):
        """测试字符转十六进制"""
        self.assertEqual(char_to_hex('A'), 'U+0041')
        self.assertEqual(char_to_hex('A', prefix=False), '0041')
        self.assertEqual(char_to_hex('😀'), 'U+1F600')


class TestUnicodeValidation(unittest.TestCase):
    """测试 Unicode 验证"""
    
    def test_valid_unicode(self):
        """测试有效 Unicode"""
        self.assertTrue(is_valid_unicode(0))
        self.assertTrue(is_valid_unicode(65))
        self.assertTrue(is_valid_unicode(0x10FFFF))
    
    def test_invalid_unicode(self):
        """测试无效 Unicode"""
        self.assertFalse(is_valid_unicode(-1))
        self.assertFalse(is_valid_unicode(0x110000))
        # 代理区无效
        self.assertFalse(is_valid_unicode(0xD800))
        self.assertFalse(is_valid_unicode(0xDFFF))


class TestUnicodeRange(unittest.TestCase):
    """测试 Unicode 范围"""
    
    def test_get_chars_in_range(self):
        """测试获取范围内字符"""
        chars = get_chars_in_range(65, 70)  # A-F
        self.assertEqual(chars, ['A', 'B', 'C', 'D', 'E', 'F'])
    
    def test_get_chars_by_category(self):
        """测试按分类获取字符"""
        chars = get_chars_by_category('Lu')
        # 应包含大写字母
        self.assertIn('A', chars)
        self.assertIn('Z', chars)
        # 不应包含小写字母
        self.assertNotIn('a', chars)


class TestUnicodeName(unittest.TestCase):
    """测试 Unicode 名称"""
    
    def test_get_name(self):
        """测试获取名称"""
        self.assertEqual(get_name('A'), 'LATIN CAPITAL LETTER A')
        self.assertEqual(get_name(' '), 'SPACE')
    
    def test_search_by_name(self):
        """测试按名称搜索"""
        results = get_chars_by_name('HEART')
        # 应包含心形符号
        self.assertTrue(len(results) > 0)
        
        # 验证结果格式
        for char, name in results:
            self.assertIn('HEART', name.upper())


class TestEncodingDetection(unittest.TestCase):
    """测试编码检测"""
    
    def test_ascii_text(self):
        """测试纯 ASCII 文本"""
        encoding = detect_encoding('Hello World')
        self.assertEqual(encoding['ASCII'], 11)
    
    def test_chinese_text(self):
        """测试中文文本"""
        encoding = detect_encoding('你好世界')
        self.assertEqual(encoding['CJK'], 4)
    
    def test_mixed_text(self):
        """测试混合文本"""
        encoding = detect_encoding('Hello 你好')
        # Hello + 空格 = 6 个 ASCII
        self.assertEqual(encoding['ASCII'], 6)
        self.assertEqual(encoding['CJK'], 2)


class TestInvisibleCharacters(unittest.TestCase):
    """测试不可见字符处理"""
    
    def test_strip_invisible(self):
        """测试移除不可见字符"""
        text = 'Hello\u0000World'  # 包含 NULL 字符
        result = strip_invisible(text)
        self.assertEqual(result, 'HelloWorld')
    
    def test_is_printable(self):
        """测试可打印判断"""
        self.assertTrue(is_printable('A'))
        self.assertTrue(is_printable(' '))
        self.assertFalse(is_printable('\u0000'))
        self.assertFalse(is_printable('\u200B'))


class TestRTL(unittest.TestCase):
    """测试 RTL 文本"""
    
    def test_is_rtl_arabic(self):
        """测试阿拉伯文 RTL"""
        self.assertTrue(is_rtl('مرحبا'))  # 阿拉伯语
    
    def test_is_rtl_hebrew(self):
        """测试希伯来文 RTL"""
        self.assertTrue(is_rtl('שלום'))  # 希伯来语
    
    def test_not_rtl_latin(self):
        """测试拉丁文非 RTL"""
        self.assertFalse(is_rtl('Hello'))


class TestCombiningCharacters(unittest.TestCase):
    """测试组合字符"""
    
    def test_is_combining(self):
        """测试组合字符判断"""
        # 组合重音符号
        self.assertTrue(is_combining('\u0301'))  # Combining Acute Accent
        self.assertFalse(is_combining('A'))
    
    def test_strip_diacritics(self):
        """测试移除变音符号"""
        # café -> cafe
        result = strip_diacritics('café')
        self.assertEqual(result, 'cafe')
        
        # München -> Munchen
        result = strip_diacritics('München')
        self.assertEqual(result, 'Munchen')


class TestUnicodeVersion(unittest.TestCase):
    """测试 Unicode 版本检测"""
    
    def test_ascii_version(self):
        """测试 ASCII 版本"""
        self.assertEqual(get_unicode_version('A'), '1.0')
    
    def test_chinese_version(self):
        """测试中文版本"""
        # CJK 字符的版本估算基于码点范围
        # 实际 CJK 统一汉字在 Unicode 1.0/3.0 等版本陆续引入
        version = get_unicode_version('中')
        self.assertIn(version, ['1.0', '3.0', '3.1'])


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_info_alias(self):
        """测试 info 别名"""
        char_info = info('A')
        self.assertEqual(char_info.codepoint, 65)
    
    def test_search_alias(self):
        """测试 search 别名"""
        results = search('HEART')
        self.assertTrue(len(results) > 0)
    
    def test_stats_alias(self):
        """测试 stats 别名"""
        s = stats('Hello')
        self.assertEqual(s['length'], 5)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        stats = get_string_stats('')
        self.assertEqual(stats['length'], 0)
        self.assertEqual(stats['letters'], 0)
    
    def test_single_char(self):
        """测试单个字符"""
        self.assertEqual(remove_zero_width('\u200B'), '')
    
    def test_high_codepoint(self):
        """测试高码点字符"""
        char = chr(0x10FFFF)
        self.assertTrue(is_valid_unicode(0x10FFFF))
    
    def test_null_char(self):
        """测试 NULL 字符"""
        self.assertFalse(is_printable('\u0000'))
    
    def test_surrogate_range(self):
        """测试代理区"""
        # 代理区的码点不能直接转字符
        self.assertFalse(is_valid_unicode(0xD800))


if __name__ == '__main__':
    unittest.main(verbosity=2)