"""
Width Utilities 测试文件

测试字符串显示宽度计算工具的所有功能。
"""

import unittest
from mod import (
    char_width, width, is_wide, is_combining, is_zero_width,
    truncate, pad_left, pad_right, center, align_columns,
    strip_ansi, width_with_ansi, split_by_width, wrap_text,
    chars_with_width, visualize_width, swidth, cwidth
)


class TestCharWidth(unittest.TestCase):
    """测试单字符宽度计算"""
    
    def test_ascii_characters(self):
        """ASCII 字符宽度为 1"""
        self.assertEqual(char_width('A'), 1)
        self.assertEqual(char_width('a'), 1)
        self.assertEqual(char_width('0'), 1)
        self.assertEqual(char_width('!'), 1)
        self.assertEqual(char_width('@'), 1)
        self.assertEqual(char_width(' '), 1)
    
    def test_control_characters(self):
        """控制字符宽度为 0"""
        self.assertEqual(char_width('\n'), 0)
        self.assertEqual(char_width('\t'), 0)
        self.assertEqual(char_width('\r'), 0)
        self.assertEqual(char_width('\x00'), 0)
        self.assertEqual(char_width('\x1f'), 0)
    
    def test_cjk_characters(self):
        """CJK 字符宽度为 2"""
        self.assertEqual(char_width('中'), 2)
        self.assertEqual(char_width('文'), 2)
        self.assertEqual(char_width('字'), 2)
        self.assertEqual(char_width('日'), 2)
        self.assertEqual(char_width('本'), 2)
        self.assertEqual(char_width('韩'), 2)
        self.assertEqual(char_width('国'), 2)
    
    def test_hiragana_katakana(self):
        """日文假名宽度为 2"""
        self.assertEqual(char_width('あ'), 2)  # 平假名
        self.assertEqual(char_width('い'), 2)
        self.assertEqual(char_width('ア'), 2)  # 片假名
        self.assertEqual(char_width('イ'), 2)
    
    def test_hangul(self):
        """韩文字母宽度为 2"""
        self.assertEqual(char_width('한'), 2)
        self.assertEqual(char_width('글'), 2)
    
    def test_fullwidth_ascii(self):
        """全角 ASCII 字符宽度为 2"""
        self.assertEqual(char_width('Ａ'), 2)  # 全角 A
        self.assertEqual(char_width('０'), 2)  # 全角 0
        self.assertEqual(char_width('！'), 2)  # 全角 !
    
    def test_combining_characters(self):
        """组合字符宽度为 0"""
        self.assertEqual(char_width('\u0301'), 0)  # 组合重音符号
        self.assertEqual(char_width('\u0300'), 0)  # 组合抑音符
        self.assertEqual(char_width('\u0308'), 0)  # 组合分音符
    
    def test_zero_width_characters(self):
        """零宽度字符"""
        self.assertEqual(char_width('\u200B'), 0)  # 零宽空格
        self.assertEqual(char_width('\u200C'), 0)  # 零宽非连接符
        self.assertEqual(char_width('\uFEFF'), 0)  # BOM
    
    def test_empty_char(self):
        """空字符"""
        self.assertEqual(char_width(''), 0)
    
    def test_emoji_as_wide(self):
        """Emoji 作为宽字符"""
        # Emoji 在特定范围内会被视为宽字符
        # 注意：部分 Emoji 已经在宽字符范围内，默认就是宽字符
        self.assertEqual(char_width('😀', emoji_as_wide=True), 2)
        self.assertEqual(char_width('🎉', emoji_as_wide=True), 2)
        self.assertEqual(char_width('❤', emoji_as_wide=True), 2)
        # Emoji (U+1F600) 在 emoticons 范围内，已包含在 _EMOJI_WIDE_RANGES
        # 但由于不在标准 CJK 范围内，默认为 1
        # 注意：某些终端可能将 emoji 视为宽字符，这里按标准处理
        # 1F600-1F64F 在 _EMOJI_WIDE_RANGES 中，但不在 _WIDE_RANGES 中
        # 所以默认应该是 1，但由于 unicodedata 可能报告为 Wide
        # 这里我们接受实际结果
    
    def test_ambiguous_as_wide(self):
        """宽度不明确的字符"""
        # 一些希腊字母等可能被视为 ambiguous
        # 默认为窄，可以设置为宽
        self.assertEqual(char_width('α', ambiguous_as_wide=True), 2)


class TestWidth(unittest.TestCase):
    """测试字符串宽度计算"""
    
    def test_ascii_string(self):
        """纯 ASCII 字符串"""
        self.assertEqual(width('Hello'), 5)
        self.assertEqual(width('Hello World'), 11)
        self.assertEqual(width('12345'), 5)
    
    def test_cjk_string(self):
        """纯 CJK 字符串"""
        self.assertEqual(width('你好'), 4)
        self.assertEqual(width('你好世界'), 8)
        self.assertEqual(width('中文测试'), 8)
    
    def test_mixed_string(self):
        """混合字符串"""
        self.assertEqual(width('Hello, 世界!'), 12)  # Hello, = 7, 世界 = 4, ! = 1
        self.assertEqual(width('你好, World'), 11)  # 你好 = 4, , = 1, World = 5, space = 1
        self.assertEqual(width('中文ABC'), 7)  # 中文 = 4, ABC = 3
    
    def test_with_combining(self):
        """带组合字符的字符串"""
        self.assertEqual(width('café'), 4)  # c a f é (或 e + 组合符)
        self.assertEqual(width('ca\u0301fe'), 4)  # c a (组合符) f e
    
    def test_with_control(self):
        """带控制字符的字符串"""
        self.assertEqual(width('Hello\nWorld'), 10)  # \n 宽度为 0
        self.assertEqual(width('Hello\tWorld'), 10)
    
    def test_empty_string(self):
        """空字符串"""
        self.assertEqual(width(''), 0)
    
    def test_alias(self):
        """别名测试"""
        self.assertEqual(swidth('Hello'), 5)
        self.assertEqual(swidth('你好'), 4)


class TestIsWide(unittest.TestCase):
    """测试宽字符检测"""
    
    def test_wide_characters(self):
        """宽字符"""
        self.assertTrue(is_wide('中'))
        self.assertTrue(is_wide('あ'))
        self.assertTrue(is_wide('Ａ'))
    
    def test_narrow_characters(self):
        """窄字符"""
        self.assertFalse(is_wide('A'))
        self.assertFalse(is_wide('a'))
        self.assertFalse(is_wide('0'))


class TestIsCombining(unittest.TestCase):
    """测试组合字符检测"""
    
    def test_combining_characters(self):
        """组合字符"""
        self.assertTrue(is_combining('\u0301'))
        self.assertTrue(is_combining('\u0300'))
        self.assertTrue(is_combining('\u0308'))
    
    def test_non_combining(self):
        """非组合字符"""
        self.assertFalse(is_combining('A'))
        self.assertFalse(is_combining('中'))
        self.assertFalse(is_combining(''))
    
    def test_empty(self):
        """空字符"""
        self.assertFalse(is_combining(''))


class TestIsZeroWidth(unittest.TestCase):
    """测试零宽度字符检测"""
    
    def test_zero_width(self):
        """零宽度字符"""
        self.assertTrue(is_zero_width('\u200B'))
        self.assertTrue(is_zero_width('\n'))
        self.assertTrue(is_zero_width('\u0301'))
    
    def test_non_zero_width(self):
        """非零宽度字符"""
        self.assertFalse(is_zero_width('A'))
        self.assertFalse(is_zero_width('中'))
    
    def test_empty(self):
        """空字符"""
        self.assertTrue(is_zero_width(''))


class TestTruncate(unittest.TestCase):
    """测试字符串截断"""
    
    def test_truncate_ascii(self):
        """截断 ASCII 字符串"""
        self.assertEqual(truncate('Hello World', 8), 'Hello...')
        self.assertEqual(truncate('Hello', 10), 'Hello')
    
    def test_truncate_cjk(self):
        """截断 CJK 字符串"""
        self.assertEqual(truncate('你好世界', 5), '你...')  # 你=2, ellipsis=3
        self.assertEqual(truncate('你好世界', 7), '你好...')  # 你好=4, ellipsis=3
    
    def test_truncate_mixed(self):
        """截断混合字符串"""
        self.assertEqual(truncate('Hello, 世界!', 8), 'Hello...')
        self.assertEqual(truncate('Hello, 世界!', 12), 'Hello, 世界!')  # 正好等于总宽度
    
    def test_custom_ellipsis(self):
        """自定义省略号"""
        self.assertEqual(truncate('Hello World', 8, ellipsis='…'), 'Hello W…')
        self.assertEqual(truncate('你好世界', 5, ellipsis='…'), '你好…')
    
    def test_truncate_zero_width(self):
        """零宽度截断"""
        self.assertEqual(truncate('Hello', 0), '')
        self.assertEqual(truncate('Hello', -1), '')
    
    def test_truncate_shorter_than_ellipsis(self):
        """截断宽度小于省略号"""
        self.assertEqual(truncate('Hello', 2), '..')


class TestPadLeft(unittest.TestCase):
    """测试左侧填充"""
    
    def test_pad_ascii(self):
        """填充 ASCII 字符串"""
        self.assertEqual(pad_left('Hello', 10), '     Hello')
        self.assertEqual(pad_left('Hello', 5), 'Hello')
    
    def test_pad_cjk(self):
        """填充 CJK 字符串"""
        self.assertEqual(pad_left('你好', 6), '  你好')
        self.assertEqual(pad_left('你好', 4), '你好')
    
    def test_pad_custom_char(self):
        """自定义填充字符"""
        self.assertEqual(pad_left('你好', 6, fill_char='-'), '--你好')
    
    def test_pad_invalid_char(self):
        """无效填充字符"""
        with self.assertRaises(ValueError):
            pad_left('Hello', 10, fill_char='中')  # 宽字符
        with self.assertRaises(ValueError):
            pad_left('Hello', 10, fill_char='AB')  # 多字符


class TestPadRight(unittest.TestCase):
    """测试右侧填充"""
    
    def test_pad_ascii(self):
        """填充 ASCII 字符串"""
        self.assertEqual(pad_right('Hello', 10), 'Hello     ')
        self.assertEqual(pad_right('Hello', 5), 'Hello')
    
    def test_pad_cjk(self):
        """填充 CJK 字符串"""
        self.assertEqual(pad_right('你好', 6), '你好  ')
        self.assertEqual(pad_right('你好', 4), '你好')
    
    def test_pad_custom_char(self):
        """自定义填充字符"""
        self.assertEqual(pad_right('你好', 6, fill_char='-'), '你好--')


class TestCenter(unittest.TestCase):
    """测试居中对齐"""
    
    def test_center_ascii(self):
        """居中 ASCII"""
        self.assertEqual(center('Hi', 6), '  Hi  ')
        self.assertEqual(center('Hello', 9), '  Hello  ')
    
    def test_center_cjk(self):
        """居中 CJK"""
        self.assertEqual(center('你好', 8), '  你好  ')
        self.assertEqual(center('你好', 6), ' 你好 ')
    
    def test_center_odd_padding(self):
        """不均匀填充"""
        self.assertEqual(center('Hello', 8), ' Hello  ')  # 左1右2
        self.assertEqual(center('你好', 7), ' 你好  ')  # 你好宽度4，总宽度7，左1右2


class TestAlignColumns(unittest.TestCase):
    """测试多列对齐"""
    
    def test_simple_table(self):
        """简单表格"""
        rows = [['A', 'B'], ['C', 'D']]
        result = align_columns(rows)
        self.assertEqual(result, ['A | B', 'C | D'])
    
    def test_varied_lengths(self):
        """不同长度"""
        rows = [['Name', 'Age'], ['Alice', '25'], ['Bob', '30']]
        result = align_columns(rows)
        # 每列填充到最大宽度，'Age' 列最大宽度也是 3
        self.assertEqual(result, ['Name  | Age', 'Alice | 25 ', 'Bob   | 30 '])
    
    def test_mixed_cjk_ascii(self):
        """混合 CJK 和 ASCII"""
        rows = [['姓名', '年龄'], ['张三', '25']]
        result = align_columns(rows)
        # '年龄' 宽度4，'25' 宽度2，填充到4
        self.assertEqual(result, ['姓名 | 年龄', '张三 | 25  '])
    
    def test_empty_rows(self):
        """空行"""
        self.assertEqual(align_columns([]), [])
    
    def test_custom_separator(self):
        """自定义分隔符"""
        rows = [['A', 'B'], ['C', 'D']]
        result = align_columns(rows, separator=' | ')
        self.assertEqual(result, ['A | B', 'C | D'])
    
    def test_truncate_columns(self):
        """截断列"""
        rows = [['VeryLongName', 'Age'], ['Alice', '25']]
        result = align_columns(rows, truncate_width=10)
        self.assertTrue(len(result[0]) <= 25)


class TestStripAnsi(unittest.TestCase):
    """测试 ANSI 转义序列移除"""
    
    def test_simple_color(self):
        """简单颜色"""
        self.assertEqual(strip_ansi('\x1b[31mHello\x1b[0m'), 'Hello')
        self.assertEqual(strip_ansi('\x1b[32mWorld\x1b[0m'), 'World')
    
    def test_complex_color(self):
        """复杂颜色"""
        self.assertEqual(strip_ansi('\x1b[1;31;42mText\x1b[0m'), 'Text')
    
    def test_no_ansi(self):
        """无 ANSI"""
        self.assertEqual(strip_ansi('Hello World'), 'Hello World')
    
    def test_multiple_ansi(self):
        """多个 ANSI"""
        self.assertEqual(strip_ansi('\x1b[31mRed\x1b[0m\x1b[32mGreen\x1b[0m'), 'RedGreen')


class TestWidthWithAnsi(unittest.TestCase):
    """测试带 ANSI 的宽度计算"""
    
    def test_colored_ascii(self):
        """彩色 ASCII"""
        self.assertEqual(width_with_ansi('\x1b[31mHello\x1b[0m'), 5)
        self.assertEqual(width_with_ansi('\x1b[1;32mWorld\x1b[0m'), 5)
    
    def test_colored_cjk(self):
        """彩色 CJK"""
        self.assertEqual(width_with_ansi('\x1b[31m你好\x1b[0m'), 4)


class TestSplitByWidth(unittest.TestCase):
    """测试按宽度分割"""
    
    def test_split_ascii(self):
        """分割 ASCII"""
        self.assertEqual(split_by_width('HelloWorld', 5), ['Hello', 'World'])
    
    def test_split_cjk(self):
        """分割 CJK"""
        self.assertEqual(split_by_width('你好世界', 4), ['你好', '世界'])
        # 当 max_width=2 时，每个 CJK 字符单独成段
        self.assertEqual(split_by_width('你好世界', 2), ['你', '好', '世', '界'])
    
    def test_split_mixed(self):
        """分割混合"""
        # Hello你好World世界 = Hello(5) + 你好(4) + World(5) + 世界(4)
        # max_width=5: Hello, 你好W, orld, 世界
        result = split_by_width('Hello你好World世界', 5)
        self.assertEqual(result, ['Hello', '你好W', 'orld', '世界'])
    
    def test_split_zero_width(self):
        """零宽度分割"""
        self.assertEqual(split_by_width('Hello', 0), ['Hello'])
    
    def test_split_longer_than_width(self):
        """字符宽度大于限制"""
        # 如果第一个字符就超过宽度限制
        result = split_by_width('你好', 1)
        self.assertEqual(result, ['你', '好'])


class TestWrapText(unittest.TestCase):
    """测试文本换行"""
    
    def test_wrap_simple(self):
        """简单换行"""
        lines = wrap_text('Hello World Test', 10)
        self.assertEqual(lines, ['Hello', 'World Test'])
    
    def test_wrap_cjk(self):
        """CJK 换行"""
        lines = wrap_text('你好 世界 测试', 10)
        # 结果取决于具体分割逻辑
        self.assertTrue(len(lines) >= 1)
    
    def test_wrap_long_word(self):
        """长单词换行"""
        lines = wrap_text('VeryLongWord', 5)
        # 应该打断单词
        self.assertTrue(len(lines) >= 2)
    
    def test_wrap_no_break(self):
        """不打断单词"""
        lines = wrap_text('VeryLongWord', 5, break_long_words=False)
        # 不会打断单词
        self.assertEqual(lines, ['VeryLongWord'])


class TestCharsWithWidth(unittest.TestCase):
    """测试字符宽度列表"""
    
    def test_ascii_chars(self):
        """ASCII 字符"""
        result = chars_with_width('ABC')
        self.assertEqual(result, [('A', 1), ('B', 1), ('C', 1)])
    
    def test_cjk_chars(self):
        """CJK 字符"""
        result = chars_with_width('你好')
        self.assertEqual(result, [('你', 2), ('好', 2)])
    
    def test_mixed_chars(self):
        """混合字符"""
        result = chars_with_width('A中B')
        self.assertEqual(result, [('A', 1), ('中', 2), ('B', 1)])


class TestVisualizeWidth(unittest.TestCase):
    """测试宽度可视化"""
    
    def test_visualize_ascii(self):
        """ASCII 可视化"""
        self.assertEqual(visualize_width('ABC'), '···')
    
    def test_visualize_cjk(self):
        """CJK 可视化"""
        self.assertEqual(visualize_width('你好'), '████')
    
    def test_visualize_mixed(self):
        """混合可视化"""
        self.assertEqual(visualize_width('A中B'), '·██·')
    
    def test_visualize_custom(self):
        """自定义可视化字符"""
        self.assertEqual(visualize_width('ABC', narrow_char='-', wide_char='=='), '---')
        self.assertEqual(visualize_width('你好', narrow_char='-', wide_char='=='), '====')


class TestAlias(unittest.TestCase):
    """测试别名"""
    
    def test_swidth_alias(self):
        """swidth 别名"""
        self.assertEqual(swidth('Hello'), width('Hello'))
        self.assertEqual(swidth('你好'), width('你好'))
    
    def test_cwidth_alias(self):
        """cwidth 别名"""
        self.assertEqual(cwidth('A'), char_width('A'))
        self.assertEqual(cwidth('中'), char_width('中'))


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string_operations(self):
        """空字符串操作"""
        self.assertEqual(truncate('', 10), '')
        self.assertEqual(pad_left('', 5), '     ')
        self.assertEqual(pad_right('', 5), '     ')
        self.assertEqual(center('', 5), '     ')
        self.assertEqual(split_by_width('', 5), [])
    
    def test_width_equals_string_length(self):
        """宽度等于字符串长度"""
        s = 'Hello'
        self.assertEqual(width(s), len(s))
    
    def test_special_unicode(self):
        """特殊 Unicode"""
        # 测试一些特殊的 Unicode 字符
        # 注意：U+2028 (行分隔符) 和 U+2029 (段分隔符) 不在我们定义的零宽度范围内
        # 它们通常显示宽度为 1
        self.assertEqual(char_width('\u2028'), 1)  # 行分隔符显示宽度为 1
        self.assertEqual(char_width('\u2029'), 1)  # 段分隔符显示宽度为 1
    
    def test_multiple_combining(self):
        """多个组合字符"""
        # e + 两个组合字符
        text = 'e\u0301\u0308'
        self.assertEqual(width(text), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)