"""
name_parser_utils 测试用例

Author: AllToolkit
Date: 2026-05-24
"""

import unittest
from mod import (
    NameParser, ParsedName, parse_name, parse_names, 
    format_name, compare_names, get_initials
)


class TestParsedName(unittest.TestCase):
    """测试 ParsedName 数据类"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        parsed = ParsedName(
            first_name="John",
            middle_name="William",
            last_name="Doe",
            prefix="Mr.",
            suffix="Jr.",
            original="Mr. John William Doe Jr."
        )
        result = parsed.to_dict()
        
        self.assertEqual(result["first_name"], "John")
        self.assertEqual(result["middle_name"], "William")
        self.assertEqual(result["last_name"], "Doe")
        self.assertEqual(result["prefix"], "Mr.")
        self.assertEqual(result["suffix"], "Jr.")
        self.assertEqual(result["original"], "Mr. John William Doe Jr.")
    
    def test_full_name(self):
        """测试生成完整姓名"""
        parsed = ParsedName(
            first_name="John",
            last_name="Doe",
            prefix="Mr.",
            suffix="Jr."
        )
        
        self.assertEqual(parsed.full_name(), "John Doe")
        self.assertEqual(parsed.full_name(include_prefix=True), "Mr. John Doe")
        self.assertEqual(parsed.full_name(include_suffix=True), "John Doe Jr.")
        self.assertEqual(parsed.full_name(include_prefix=True, include_suffix=True), "Mr. John Doe Jr.")
    
    def test_full_name_chinese(self):
        """测试中文完整姓名"""
        parsed = ParsedName(
            chinese_surname="张",
            chinese_given_name="三",
            last_name="张",
            first_name="三"
        )
        
        self.assertEqual(parsed.full_name(), "张三")


class TestNameParserWestern(unittest.TestCase):
    """测试西方名称解析"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_simple_name(self):
        """测试简单名称"""
        result = self.parser.parse("John Doe")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Doe")
        self.assertEqual(result.format_type, "western")
    
    def test_name_with_middle(self):
        """测试带中间名的名称"""
        result = self.parser.parse("John William Doe")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.middle_name, "William")
        self.assertEqual(result.last_name, "Doe")
    
    def test_name_with_prefix(self):
        """测试带前缀的名称"""
        result = self.parser.parse("Mr. John Doe")
        self.assertEqual(result.prefix, "Mr.")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Doe")
    
    def test_name_with_suffix(self):
        """测试带后缀的名称"""
        result = self.parser.parse("John Doe Jr.")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Doe")
        self.assertEqual(result.suffix, "JR.")
    
    def test_name_with_prefix_and_suffix(self):
        """测试带前缀和后缀的名称"""
        result = self.parser.parse("Dr. Jane Smith PhD")
        self.assertEqual(result.prefix, "Dr.")
        self.assertEqual(result.first_name, "Jane")
        self.assertEqual(result.last_name, "Smith")
        self.assertEqual(result.suffix, "PhD")
    
    def test_last_first_format(self):
        """测试姓在前的格式"""
        result = self.parser.parse("Doe, John William")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.middle_name, "William")
        self.assertEqual(result.last_name, "Doe")
    
    def test_single_name(self):
        """测试单名"""
        result = self.parser.parse("Madonna")
        self.assertEqual(result.first_name, "Madonna")
        self.assertEqual(result.last_name, "")
    
    def test_nickname(self):
        """测试昵称"""
        result = self.parser.parse('John "Jack" Doe')
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Doe")
        self.assertEqual(result.nickname, "Jack")
    
    def test_multiple_middle_names(self):
        """测试多个中间名"""
        result = self.parser.parse("John William James Doe")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.middle_name, "William James")
        self.assertEqual(result.last_name, "Doe")
    
    def test_empty_name(self):
        """测试空名称"""
        result = self.parser.parse("")
        self.assertEqual(result.first_name, "")
        self.assertEqual(result.last_name, "")


class TestNameParserChinese(unittest.TestCase):
    """测试中文名称解析"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_simple_chinese_name(self):
        """测试简单中文名"""
        result = self.parser.parse("张三")
        self.assertEqual(result.chinese_surname, "张")
        self.assertEqual(result.chinese_given_name, "三")
        self.assertEqual(result.last_name, "张")
        self.assertEqual(result.first_name, "三")
        self.assertEqual(result.format_type, "chinese")
    
    def test_two_character_surname(self):
        """测试单姓双字名"""
        result = self.parser.parse("李四五")
        self.assertEqual(result.chinese_surname, "李")
        self.assertEqual(result.chinese_given_name, "四五")
    
    def test_compound_surname(self):
        """测试复姓"""
        result = self.parser.parse("欧阳锋")
        self.assertEqual(result.chinese_surname, "欧阳")
        self.assertEqual(result.chinese_given_name, "锋")
    
    def test_compound_surname_two_given(self):
        """测试复姓加双字名"""
        result = self.parser.parse("司马相如")
        self.assertEqual(result.chinese_surname, "司马")
        self.assertEqual(result.chinese_given_name, "相如")
    
    def test_chinese_with_nickname(self):
        """测试中文带昵称"""
        result = self.parser.parse('张三 "小三子"')
        self.assertEqual(result.chinese_surname, "张")
        self.assertEqual(result.chinese_given_name, "三")
        self.assertEqual(result.nickname, "小三子")


class TestNameParserMixed(unittest.TestCase):
    """测试混合名称"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_chinese_with_english_prefix(self):
        """测试中文带英文前缀"""
        result = self.parser.parse("Dr. 张三")
        self.assertEqual(result.prefix, "Dr.")
        self.assertEqual(result.chinese_surname, "张")
        self.assertEqual(result.chinese_given_name, "三")
        self.assertEqual(result.format_type, "mixed")


class TestNameFormatting(unittest.TestCase):
    """测试名称格式化"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_format_western(self):
        """测试西方格式"""
        parsed = self.parser.parse("John William Doe")
        result = self.parser.format_name(parsed, "western")
        self.assertEqual(result, "John William Doe")
    
    def test_format_last_first(self):
        """测试姓在先格式"""
        parsed = self.parser.parse("John William Doe")
        result = self.parser.format_name(parsed, "last_first")
        self.assertEqual(result, "Doe, John William")
    
    def test_format_initials(self):
        """测试首字母格式"""
        parsed = self.parser.parse("John William Doe")
        result = self.parser.format_name(parsed, "initials")
        self.assertEqual(result, "JWD")
    
    def test_format_initials_no_middle(self):
        """测试首字母格式（不含中间名）"""
        parsed = self.parser.parse("John William Doe")
        result = self.parser.format_name(parsed, "initials", include_middle=False)
        self.assertEqual(result, "JD")
    
    def test_format_with_prefix_suffix(self):
        """测试带前缀后缀的格式化"""
        parsed = self.parser.parse("Dr. John Doe PhD")
        result = self.parser.format_name(parsed, "western", include_prefix=True, include_suffix=True)
        self.assertEqual(result, "Dr. John Doe PhD")


class TestNameComparison(unittest.TestCase):
    """测试名称比较"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_identical_names(self):
        """测试完全相同的名称"""
        match, score = self.parser.compare_names("John Doe", "John Doe")
        self.assertTrue(match)
        self.assertEqual(score, 1.0)
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        match, score = self.parser.compare_names("John Doe", "JOHN DOE")
        self.assertTrue(match)
        self.assertEqual(score, 1.0)
    
    def test_different_first_name(self):
        """测试不同名"""
        match, score = self.parser.compare_names("John Doe", "Jane Doe")
        self.assertFalse(match)
    
    def test_different_last_name(self):
        """测试不同姓"""
        match, score = self.parser.compare_names("John Doe", "John Smith")
        self.assertFalse(match)
    
    def test_same_first_initial(self):
        """测试首字母相同"""
        match, score = self.parser.compare_names("John Doe", "Jonathan Doe")
        self.assertTrue(match or score >= 0.5)  # 姓相同，名首字母相同
    
    def test_chinese_names(self):
        """测试中文名比较"""
        match, score = self.parser.compare_names("张三", "张三")
        self.assertTrue(match)
        self.assertEqual(score, 1.0)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_parse_name_function(self):
        """测试 parse_name 函数"""
        result = parse_name("John Doe")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Doe")
    
    def test_parse_names_function(self):
        """测试 parse_names 函数"""
        results = parse_names(["John Doe", "Jane Smith"])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].first_name, "John")
        self.assertEqual(results[1].first_name, "Jane")
    
    def test_format_name_function(self):
        """测试 format_name 函数"""
        result = format_name("John William Doe", "initials")
        self.assertEqual(result, "JWD")
    
    def test_compare_names_function(self):
        """测试 compare_names 函数"""
        match, score = compare_names("John Doe", "John Doe")
        self.assertTrue(match)
    
    def test_get_initials_function(self):
        """测试 get_initials 函数"""
        result = get_initials("John William Doe")
        self.assertEqual(result, "JD")


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_whitespace_handling(self):
        """测试空白处理"""
        result = self.parser.parse("  John   Doe  ")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Doe")
    
    def test_multiple_prefixes(self):
        """测试多个前缀（取第一个）"""
        result = self.parser.parse("Dr. Prof. John Doe")
        self.assertEqual(result.prefix, "Dr.")
    
    def test_multiple_suffixes(self):
        """测试多个后缀（取第一个）"""
        result = self.parser.parse("John Doe Jr. PhD")
        # 只识别第一个后缀
        self.assertIn(result.suffix, ["JR.", "PHD", ""])
    
    def test_special_characters_in_name(self):
        """测试名称中的特殊字符"""
        result = self.parser.parse("Mary-Jane O'Brien")
        self.assertEqual(result.first_name, "Mary-Jane")
        self.assertEqual(result.last_name, "O'Brien")
    
    def test_hyphenated_last_name(self):
        """测试连字符姓氏"""
        result = self.parser.parse("Mary Smith-Johnson")
        self.assertEqual(result.first_name, "Mary")
        self.assertEqual(result.last_name, "Smith-Johnson")
    
    def test_apostrophe_in_name(self):
        """测试名称中的撇号"""
        result = self.parser.parse("Seán O'Connor")
        self.assertEqual(result.first_name, "Seán")
        self.assertEqual(result.last_name, "O'Connor")


class TestCommonLastNames(unittest.TestCase):
    """测试常见姓氏识别"""
    
    def setUp(self):
        self.parser = NameParser()
    
    def test_recognize_common_surname(self):
        """测试识别常见姓氏"""
        result = self.parser.parse("John Smith")
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.last_name, "Smith")
    
    def test_two_part_first_name(self):
        """测试两部分名字（非姓氏）"""
        result = self.parser.parse("Mary Ann Johnson")
        self.assertEqual(result.first_name, "Mary")
        self.assertEqual(result.middle_name, "Ann")
        self.assertEqual(result.last_name, "Johnson")


if __name__ == "__main__":
    unittest.main(verbosity=2)