# -*- coding: utf-8 -*-
"""
AllToolkit - Regex Builder Utilities Tests 🧪

Author: AllToolkit Team
License: MIT
"""

import re
import unittest
from mod import (
    RegexBuilder,
    builder,
    email_pattern,
    phone_cn_pattern,
    url_pattern,
    uuid_pattern,
)


class TestRegexBuilderBasics(unittest.TestCase):
    """基础功能测试"""
    
    def test_empty_builder(self):
        """空构建器"""
        pattern = RegexBuilder().build()
        self.assertEqual(pattern, '')
    
    def test_literal(self):
        """字面文本匹配"""
        pattern = RegexBuilder().literal('hello').build()
        self.assertTrue(re.search(pattern, 'hello world'))
        self.assertFalse(re.search(pattern, 'goodbye'))
    
    def test_literal_escape(self):
        """字面文本自动转义"""
        pattern = RegexBuilder().literal('1+1').build()
        self.assertTrue(re.search(pattern, '1+1'))
        self.assertFalse(re.search(pattern, '111'))
    
    def test_char(self):
        """单字符匹配"""
        pattern = RegexBuilder().char('a').build()
        self.assertEqual(pattern, 'a')
    
    def test_char_invalid(self):
        """多字符应报错"""
        with self.assertRaises(ValueError):
            RegexBuilder().char('abc')
    
    def test_char_class(self):
        """字符类匹配"""
        pattern = RegexBuilder().char_class('a', 'b', 'c').build()
        self.assertEqual(pattern, '[abc]')
        self.assertTrue(re.search(pattern, 'a'))
        self.assertTrue(re.search(pattern, 'b'))
        self.assertFalse(re.search(pattern, 'd'))
    
    def test_char_range(self):
        """字符范围匹配"""
        pattern = RegexBuilder().char_range('a', 'z').build()
        self.assertEqual(pattern, '[a-z]')
        self.assertTrue(re.search(pattern, 'm'))
        self.assertFalse(re.search(pattern, 'M'))
    
    def test_char_ranges(self):
        """多字符范围匹配"""
        pattern = RegexBuilder().char_ranges(('a', 'z'), ('A', 'Z')).build()
        self.assertEqual(pattern, '[a-zA-Z]')
        self.assertTrue(re.search(pattern, 'm'))
        self.assertTrue(re.search(pattern, 'M'))
        self.assertFalse(re.search(pattern, '5'))
    
    def test_negated_char_class(self):
        """否定字符类"""
        pattern = RegexBuilder().negated_char_class('a', 'b', 'c').build()
        self.assertEqual(pattern, '[^abc]')
        self.assertTrue(re.search(pattern, 'd'))
        self.assertFalse(re.search(pattern, 'a'))
    
    def test_any_char(self):
        """任意字符"""
        pattern = RegexBuilder().any_char().build()
        self.assertEqual(pattern, '.')
        self.assertTrue(re.search(pattern, 'a'))
        self.assertTrue(re.search(pattern, '5'))
    
    def test_digit(self):
        """数字字符"""
        pattern = RegexBuilder().digit().build()
        self.assertEqual(pattern, r'\d')
        self.assertTrue(re.search(pattern, '5'))
        self.assertFalse(re.search(pattern, 'a'))
    
    def test_non_digit(self):
        """非数字字符"""
        pattern = RegexBuilder().non_digit().build()
        self.assertEqual(pattern, r'\D')
        self.assertTrue(re.search(pattern, 'a'))
        self.assertFalse(re.search(pattern, '5'))
    
    def test_word_char(self):
        """单词字符"""
        pattern = RegexBuilder().word_char().build()
        self.assertEqual(pattern, r'\w')
        self.assertTrue(re.search(pattern, 'a'))
        self.assertTrue(re.search(pattern, '5'))
        self.assertTrue(re.search(pattern, '_'))
    
    def test_non_word_char(self):
        """非单词字符"""
        pattern = RegexBuilder().non_word_char().build()
        self.assertEqual(pattern, r'\W')
        self.assertTrue(re.search(pattern, '-'))
        self.assertFalse(re.search(pattern, 'a'))
    
    def test_whitespace(self):
        """空白字符"""
        pattern = RegexBuilder().whitespace().build()
        self.assertEqual(pattern, r'\s')
        self.assertTrue(re.search(pattern, ' '))
        self.assertTrue(re.search(pattern, '\t'))
    
    def test_non_whitespace(self):
        """非空白字符"""
        pattern = RegexBuilder().non_whitespace().build()
        self.assertEqual(pattern, r'\S')
        self.assertTrue(re.search(pattern, 'a'))
        self.assertFalse(re.search(pattern, ' '))


class TestRegexBuilderQuantifiers(unittest.TestCase):
    """量词测试"""
    
    def test_optional_pattern(self):
        """可选模式"""
        pattern = RegexBuilder().literal('a').optional().build()
        self.assertEqual(pattern, 'a?')
    
    def test_zero_or_more_pattern(self):
        """零次或多次模式"""
        pattern = RegexBuilder().literal('a').zero_or_more().build()
        self.assertEqual(pattern, 'a*')
    
    def test_one_or_more(self):
        """一次或多次"""
        pattern = RegexBuilder().literal('a').one_or_more().build()
        self.assertTrue(re.search(pattern, 'a'))
        self.assertTrue(re.search(pattern, 'aaa'))
        self.assertFalse(re.search(pattern, ''))
    
    def test_exactly(self):
        """恰好 n 次"""
        pattern = RegexBuilder().literal('a').exactly(3).build()
        self.assertEqual(pattern, 'a{3}')
        self.assertTrue(re.search(pattern, 'aaa'))
    
    def test_min_times(self):
        """至少 n 次"""
        pattern = RegexBuilder().literal('a').min_times(2).build()
        self.assertEqual(pattern, 'a{2,}')
        self.assertFalse(re.search(pattern, 'a'))
        self.assertTrue(re.search(pattern, 'aa'))
    
    def test_min_max(self):
        """n 到 m 次"""
        pattern = RegexBuilder().literal('a').min_max(2, 4).build()
        self.assertEqual(pattern, 'a{2,4}')
        self.assertTrue(re.search(pattern, 'aa'))
        self.assertTrue(re.search(pattern, 'aaa'))
    
    def test_any_of(self):
        """多选一"""
        pattern = RegexBuilder().any_of('cat', 'dog').build()
        self.assertTrue(re.search(pattern, 'cat'))
        self.assertTrue(re.search(pattern, 'dog'))
        self.assertFalse(re.search(pattern, 'bird'))


class TestRegexBuilderAnchors(unittest.TestCase):
    """锚点测试"""
    
    def test_start(self):
        """开头锚点"""
        pattern = RegexBuilder().start().literal('hello').build()
        self.assertEqual(pattern, '^hello')
        self.assertTrue(re.search(pattern, 'hello world'))
        self.assertFalse(re.search(pattern, 'say hello'))
    
    def test_end(self):
        """结尾锚点"""
        pattern = RegexBuilder().literal('world').end().build()
        self.assertEqual(pattern, 'world$')
        self.assertTrue(re.search(pattern, 'hello world'))
    
    def test_word_boundary(self):
        """单词边界"""
        pattern = RegexBuilder().word_boundary().literal('cat').word_boundary().build()
        self.assertTrue(re.search(pattern, 'the cat is here'))
        self.assertFalse(re.search(pattern, 'the category is here'))
    
    def test_start_of_string(self):
        """字符串绝对开头"""
        pattern = RegexBuilder().start_of_string().literal('hello').build()
        self.assertTrue(re.search(pattern, 'hello'))
    
    def test_end_of_string(self):
        """字符串绝对结尾"""
        pattern = RegexBuilder().literal('world').end_of_string().build()
        self.assertTrue(re.search(pattern, 'hello world'))


class TestRegexBuilderGroups(unittest.TestCase):
    """分组测试"""
    
    def test_group(self):
        """捕获组"""
        pattern = RegexBuilder().group(r'\d+').build()
        match = re.search(pattern, '123')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '123')
    
    def test_named_group(self):
        """命名捕获组"""
        pattern = RegexBuilder().group(r'\d+', 'number').build()
        match = re.search(pattern, '123')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '123')
    
    def test_non_capturing_group(self):
        """非捕获组"""
        pattern = RegexBuilder().non_capturing_group(r'\d+').build()
        match = re.search(pattern, '123')
        self.assertIsNotNone(match)
        self.assertEqual(len(match.groups()), 0)
    
    def test_multiple_groups(self):
        """多个捕获组"""
        pattern = (RegexBuilder()
            .group(r'\d{4}', 'year')
            .literal('-')
            .group(r'\d{2}', 'month')
            .literal('-')
            .group(r'\d{2}', 'day')
            .build())
        match = re.search(pattern, '2024-05-10')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('year'), '2024')
        self.assertEqual(match.group('month'), '05')
        self.assertEqual(match.group('day'), '10')


class TestRegexBuilderLookaround(unittest.TestCase):
    """前瞻断言测试"""
    
    def test_lookahead(self):
        """正向前瞻"""
        pattern = RegexBuilder().literal('a').lookahead('b').build()
        self.assertTrue(re.search(pattern, 'ab'))
        self.assertFalse(re.search(pattern, 'ac'))
    
    def test_negative_lookahead(self):
        """负向前瞻"""
        pattern = RegexBuilder().literal('a').negative_lookahead('b').build()
        self.assertTrue(re.search(pattern, 'ac'))
        self.assertFalse(re.search(pattern, 'ab'))


class TestRegexBuilderFlags(unittest.TestCase):
    """标志测试"""
    
    def test_ignore_case(self):
        """忽略大小写"""
        builder = RegexBuilder().literal('hello').ignore_case()
        pattern = builder.compile()
        self.assertTrue(pattern.search('HELLO'))
        self.assertTrue(pattern.search('Hello'))
    
    def test_multiline(self):
        """多行模式"""
        builder = RegexBuilder().start().literal('hello').multiline()
        pattern = builder.compile()
        self.assertTrue(pattern.search('world\nhello'))
    
    def test_dotall(self):
        """dotall 模式"""
        builder = RegexBuilder().any_char().one_or_more().dotall()
        pattern = builder.compile()
        self.assertTrue(pattern.search('hello\nworld'))


class TestRegexBuilderQuickPatterns(unittest.TestCase):
    """快捷模式测试"""
    
    def test_email_quick(self):
        """邮箱快捷模式"""
        pattern = RegexBuilder().email().build()
        self.assertTrue(re.search(pattern, 'test@example.com'))
    
    def test_url_quick(self):
        """URL 快捷模式"""
        pattern = RegexBuilder().url().build()
        self.assertTrue(re.search(pattern, 'https://example.com'))
    
    def test_phone_cn_quick(self):
        """中国手机号快捷模式"""
        pattern = RegexBuilder().phone_cn().build()
        self.assertTrue(re.search(pattern, '13812345678'))
    
    def test_ipv4_quick(self):
        """IPv4 快捷模式"""
        pattern = RegexBuilder().ipv4().build()
        self.assertTrue(re.search(pattern, '192.168.1.1'))
    
    def test_uuid_quick(self):
        """UUID 快捷模式"""
        pattern = RegexBuilder().uuid().build()
        self.assertTrue(re.search(pattern, '123e4567-e89b-12d3-a456-426614174000'))
    
    def test_chinese_quick(self):
        """中文快捷模式"""
        pattern = RegexBuilder().chinese().build()
        self.assertTrue(re.search(pattern, '中'))


class TestRegexBuilderMethods(unittest.TestCase):
    """组合方法测试"""
    
    def test_then(self):
        """then 方法"""
        pattern = RegexBuilder().literal('hello').then(' ').literal('world').build()
        self.assertEqual(pattern, 'hello world')
    
    def test_repeat(self):
        """repeat 方法"""
        pattern = RegexBuilder().repeat(3, 'a').build()
        self.assertTrue(re.search(pattern, 'aaa'))


class TestRegexBuilderTestMethods(unittest.TestCase):
    """测试方法测试"""
    
    def test_test_method(self):
        """test 方法"""
        builder = RegexBuilder().literal('hello')
        self.assertTrue(builder.test('hello world'))
        self.assertFalse(builder.test('goodbye'))
    
    def test_match_method(self):
        """match 方法"""
        builder = RegexBuilder().group(r'\d+', 'num')
        match = builder.match('abc 123 def')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('num'), '123')
    
    def test_split(self):
        """split 方法"""
        builder = RegexBuilder().literal(',')
        result = builder.split('a,b,c')
        self.assertEqual(result, ['a', 'b', 'c'])
    
    def test_str_repr(self):
        """字符串表示"""
        builder = RegexBuilder().literal('hello')
        self.assertEqual(str(builder), 'hello')
        self.assertEqual(repr(builder), "RegexBuilder('hello')")


class TestQuickFunctions(unittest.TestCase):
    """快捷函数测试"""
    
    def test_builder_function(self):
        """builder 函数"""
        pattern = builder().literal('hello').one_or_more().build()
        self.assertTrue(re.search(pattern, 'helloooo'))
    
    def test_email_pattern_func(self):
        """email_pattern 函数"""
        pattern = email_pattern()
        self.assertTrue(re.search(pattern, 'test@example.com'))
    
    def test_phone_cn_pattern_func(self):
        """phone_cn_pattern 函数"""
        pattern = phone_cn_pattern()
        self.assertTrue(re.search(pattern, '13812345678'))
    
    def test_url_pattern_func(self):
        """url_pattern 函数"""
        pattern = url_pattern()
        self.assertTrue(re.search(pattern, 'https://example.com'))
    
    def test_uuid_pattern_func(self):
        """uuid_pattern 函数"""
        pattern = uuid_pattern()
        self.assertTrue(re.search(pattern, '123e4567-e89b-12d3-a456-426614174000'))


class TestComplexPatterns(unittest.TestCase):
    """复杂模式测试"""
    
    def test_chinese_phone(self):
        """中国手机号模式"""
        pattern = (RegexBuilder()
            .literal('1')
            .char_class(*'3456789')
            .digit().exactly(9)
            .build())
        self.assertTrue(re.search(pattern, '13812345678'))
    
    def test_nested_builder(self):
        """嵌套构建器"""
        digit = RegexBuilder().digit()
        year = RegexBuilder().exactly(4, digit.build()).build()
        
        pattern = RegexBuilder().group(year, 'year').build()
        match = re.search(pattern, '2024-05-10')
        self.assertIsNotNone(match)


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_empty_pattern(self):
        """空模式"""
        pattern = RegexBuilder().build()
        self.assertTrue(re.search(pattern, 'anything'))
    
    def test_special_chars_escape(self):
        """特殊字符转义"""
        pattern = RegexBuilder().literal('[]').build()
        self.assertTrue(re.search(pattern, '[]'))
    
    def test_unicode(self):
        """Unicode 字符"""
        pattern = RegexBuilder().literal('你好').build()
        self.assertTrue(re.search(pattern, '你好世界'))
    
    def test_very_long_pattern(self):
        """非常长的模式"""
        builder = RegexBuilder()
        for i in range(50):
            builder.literal('a')
        pattern = builder.build()
        self.assertEqual(len(pattern), 50)
        self.assertTrue(re.search(pattern, 'a' * 50))


if __name__ == '__main__':
    unittest.main(verbosity=2)