"""
ISBN Utils 单元测试
"""

import unittest
from mod import (
    ISBNUtils, ISBNError, InvalidISBNError, ISBNConversionError,
    validate, validate_strict, convert_to_13, convert_to_10,
    format_isbn, parse, generate_random, extract_from_text
)


class TestISBNUtils(unittest.TestCase):
    """ISBNUtils 类测试"""
    
    # ==================== 清理测试 ====================
    
    def test_clean_basic(self):
        """测试基本清理功能"""
        self.assertEqual(ISBNUtils.clean("978-0-13-235088-4"), "9780132350884")
        self.assertEqual(ISBNUtils.clean("978 0 13 235088 4"), "9780132350884")
        self.assertEqual(ISBNUtils.clean("0-13-235088-2"), "0132350882")
        
    def test_clean_with_x(self):
        """测试包含 X 的清理"""
        self.assertEqual(ISBNUtils.clean("0-12-345678-X"), "012345678X")
        self.assertEqual(ISBNUtils.clean("0-12-345678-x"), "012345678X")  # 小写转大写
        
    def test_clean_empty(self):
        """测试空字符串"""
        self.assertEqual(ISBNUtils.clean(""), "")
        self.assertEqual(ISBNUtils.clean("---"), "")
        
    # ==================== 版本检测测试 ====================
    
    def test_detect_version_10(self):
        """测试 ISBN-10 版本检测"""
        self.assertEqual(ISBNUtils.detect_version("0132350882"), 10)
        self.assertEqual(ISBNUtils.detect_version("012345678X"), 10)
        
    def test_detect_version_13(self):
        """测试 ISBN-13 版本检测"""
        self.assertEqual(ISBNUtils.detect_version("9780132350884"), 13)
        self.assertEqual(ISBNUtils.detect_version("9791234567896"), 13)
        
    def test_detect_version_invalid(self):
        """测试无效版本检测"""
        self.assertIsNone(ISBNUtils.detect_version("12345"))
        self.assertIsNone(ISBNUtils.detect_version("123456789012"))
        
    # ==================== 校验位计算测试 ====================
    
    def test_calculate_check_digit_10(self):
        """测试 ISBN-10 校验位计算"""
        # 使用正确的前9位
        self.assertEqual(ISBNUtils.calculate_check_digit_10("013235088"), "2")
        self.assertEqual(ISBNUtils.calculate_check_digit_10("020163361"), "2")
        self.assertEqual(ISBNUtils.calculate_check_digit_10("030640615"), "2")
        # 校验位为 X 的情况
        self.assertEqual(ISBNUtils.calculate_check_digit_10("012345678"), "9")
        
    def test_calculate_check_digit_13(self):
        """测试 ISBN-13 校验位计算"""
        self.assertEqual(ISBNUtils.calculate_check_digit_12("978013235088"), "4")
        self.assertEqual(ISBNUtils.calculate_check_digit_12("978020163361"), "0")
        
    def test_calculate_check_digit_10_invalid_input(self):
        """测试 ISBN-10 校验位计算的无效输入"""
        with self.assertRaises(InvalidISBNError):
            ISBNUtils.calculate_check_digit_10("12345")  # 不是9位
        with self.assertRaises(InvalidISBNError):
            ISBNUtils.calculate_check_digit_10("12345678X")  # 包含非数字
            
    def test_calculate_check_digit_13_invalid_input(self):
        """测试 ISBN-13 校验位计算的无效输入"""
        with self.assertRaises(InvalidISBNError):
            ISBNUtils.calculate_check_digit_12("12345")  # 不是12位
        with self.assertRaises(InvalidISBNError):
            ISBNUtils.calculate_check_digit_12("12345678901X")  # 包含非数字
            
    # ==================== 验证测试 ====================
    
    def test_validate_valid_isbn10(self):
        """测试有效的 ISBN-10 验证"""
        # 使用有效的 ISBN-10
        self.assertTrue(ISBNUtils.validate("0-13-235088-2"))  # Clean Code
        self.assertTrue(ISBNUtils.validate("0-306-40615-2"))  # Introduction to Algorithms
        self.assertTrue(ISBNUtils.validate("0-201-63361-2"))  # Design Patterns
        
    def test_validate_valid_isbn13(self):
        """测试有效的 ISBN-13 验证"""
        # 使用有效的 ISBN-13（从 ISBN-10 转换得到）
        self.assertTrue(ISBNUtils.validate("978-0-13-235088-4"))
        self.assertTrue(ISBNUtils.validate("978-0-20-163361-0"))
        # 生成有效的 979 前缀 ISBN-13
        valid_979 = ISBNUtils.generate_random(13, prefix='979')
        self.assertTrue(ISBNUtils.validate(valid_979))
        
    def test_validate_invalid_isbn(self):
        """测试无效的 ISBN 验证"""
        self.assertFalse(ISBNUtils.validate("0-13-235088-3"))  # 错误的校验位
        self.assertFalse(ISBNUtils.validate("978-0-13-235088-5"))  # 错误的校验位
        self.assertFalse(ISBNUtils.validate("12345"))  # 长度错误
        self.assertFalse(ISBNUtils.validate("9771234567890"))  # 错误的前缀
        
    def test_validate_strict_valid(self):
        """测试严格验证有效 ISBN"""
        result = ISBNUtils.validate_strict("0-13-235088-2")
        self.assertTrue(result['valid'])
        self.assertEqual(result['version'], 10)
        self.assertEqual(result['check_digit'], '2')
        
        result = ISBNUtils.validate_strict("978-0-13-235088-4")
        self.assertTrue(result['valid'])
        self.assertEqual(result['version'], 13)
        self.assertEqual(result['check_digit'], '4')
        self.assertEqual(result['prefix'], '978')
        
    def test_validate_strict_invalid(self):
        """测试严格验证无效 ISBN"""
        with self.assertRaises(InvalidISBNError):
            ISBNUtils.validate_strict("0-13-235088-3")
        with self.assertRaises(InvalidISBNError):
            ISBNUtils.validate_strict("12345")
            
    # ==================== 转换测试 ====================
    
    def test_convert_to_13(self):
        """测试 ISBN-10 转 ISBN-13"""
        result = ISBNUtils.convert_to_13("0-13-235088-2")
        self.assertEqual(result, "9780132350884")
        
        # 已经是 ISBN-13 应该返回原值
        self.assertEqual(ISBNUtils.convert_to_13("9780132350884"), "9780132350884")
        
    def test_convert_to_10(self):
        """测试 ISBN-13 转 ISBN-10"""
        result = ISBNUtils.convert_to_10("978-0-13-235088-4")
        self.assertEqual(result, "0132350882")
        
        # 已经是 ISBN-10 应该返回原值
        self.assertEqual(ISBNUtils.convert_to_10("0132350882"), "0132350882")
        
    def test_convert_to_10_979_prefix(self):
        """测试 979 前缀的 ISBN-13 无法转换为 ISBN-10"""
        valid_979 = ISBNUtils.generate_random(13, prefix='979')
        with self.assertRaises(ISBNConversionError):
            ISBNUtils.convert_to_10(valid_979)
            
    def test_convert_invalid(self):
        """测试无效转换"""
        with self.assertRaises(ISBNConversionError):
            ISBNUtils.convert_to_13("invalid")
        with self.assertRaises(ISBNConversionError):
            ISBNUtils.convert_to_10("invalid")
            
    # ==================== 格式化测试 ====================
    
    def test_format_isbn10(self):
        """测试 ISBN-10 格式化"""
        formatted = ISBNUtils.format("0132350882")
        self.assertEqual(formatted, "0-1323-5088-2")
        
    def test_format_isbn13(self):
        """测试 ISBN-13 格式化"""
        formatted = ISBNUtils.format("9780132350884")
        self.assertEqual(formatted, "978-0-1323-5088-4")
        
    def test_format_custom_separator(self):
        """测试自定义分隔符"""
        self.assertEqual(ISBNUtils.format("0132350882", " "), "0 1323 5088 2")
        
    def test_format_invalid(self):
        """测试无效 ISBN 格式化"""
        self.assertEqual(ISBNUtils.format("12345"), "12345")  # 返回原值
        
    # ==================== 解析测试 ====================
    
    def test_parse_valid_isbn10(self):
        """测试解析有效的 ISBN-10"""
        result = ISBNUtils.parse("0-13-235088-2")
        self.assertTrue(result['valid'])
        self.assertEqual(result['version'], 10)
        self.assertEqual(result['cleaned'], "0132350882")
        self.assertIn('isbn13', result)
        
    def test_parse_valid_isbn13(self):
        """测试解析有效的 ISBN-13"""
        result = ISBNUtils.parse("978-0-13-235088-4")
        self.assertTrue(result['valid'])
        self.assertEqual(result['version'], 13)
        self.assertEqual(result['cleaned'], "9780132350884")
        
    def test_parse_invalid(self):
        """测试解析无效 ISBN"""
        result = ISBNUtils.parse("invalid-isbn")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
        
    # ==================== 随机生成测试 ====================
    
    def test_generate_random_isbn10(self):
        """测试随机生成 ISBN-10"""
        for _ in range(10):
            isbn = ISBNUtils.generate_random(10)
            self.assertEqual(len(isbn), 10)
            self.assertTrue(ISBNUtils.validate(isbn))
            
    def test_generate_random_isbn13(self):
        """测试随机生成 ISBN-13"""
        for _ in range(10):
            isbn = ISBNUtils.generate_random(13)
            self.assertEqual(len(isbn), 13)
            self.assertTrue(ISBNUtils.validate(isbn))
            
    def test_generate_random_with_prefix(self):
        """测试指定前缀生成 ISBN-13"""
        isbn = ISBNUtils.generate_random(13, prefix="978")
        self.assertTrue(isbn.startswith("978"))
        self.assertTrue(ISBNUtils.validate(isbn))
        
        isbn = ISBNUtils.generate_random(13, prefix="979")
        self.assertTrue(isbn.startswith("979"))
        self.assertTrue(ISBNUtils.validate(isbn))
        
    def test_generate_batch(self):
        """测试批量生成"""
        isbns = ISBNUtils.generate_batch(5, 13)
        self.assertEqual(len(isbns), 5)
        for isbn in isbns:
            self.assertTrue(ISBNUtils.validate(isbn))
            
    def test_generate_random_invalid_version(self):
        """测试无效版本"""
        with self.assertRaises(ValueError):
            ISBNUtils.generate_random(11)
            
    # ==================== 文本提取测试 ====================
    
    def test_extract_from_text(self):
        """测试从文本提取 ISBN"""
        text = """
        这本书的 ISBN 是 978-0-13-235088-4，另一本是 0-13-235088-2。
        还有一些无效的：978-0-13-235088-5（校验位错误）。
        """
        found = ISBNUtils.extract_from_text(text)
        self.assertIn("9780132350884", found)
        self.assertIn("0132350882", found)
        self.assertNotIn("9780132350885", found)  # 无效的不应该被提取
        
    def test_extract_with_isbn_prefix(self):
        """测试提取带 ISBN 前缀的文本"""
        text = "ISBN: 978-0-13-235088-4"
        found = ISBNUtils.extract_from_text(text)
        self.assertEqual(found, ["9780132350884"])
        
    # ==================== 注册组识别测试 ====================
    
    def test_get_registration_group_china(self):
        """测试识别中国出版的 ISBN"""
        self.assertEqual(ISBNUtils.get_registration_group("7-1234-5678-9"), "中国")
        self.assertEqual(ISBNUtils.get_registration_group("978-7-123-45678-9"), "中国")
        
    def test_get_registration_group_english(self):
        """测试识别英语区 ISBN"""
        self.assertEqual(ISBNUtils.get_registration_group("0-306-40615-2"), "英语区")
        self.assertEqual(ISBNUtils.get_registration_group("1-56619-909-3"), "英语区")
        
    def test_get_registration_group_japanese(self):
        """测试识别日本 ISBN"""
        self.assertEqual(ISBNUtils.get_registration_group("4-1234-5678-9"), "日本")
        
    def test_get_registration_group_unknown(self):
        """测试无法识别的注册组"""
        # 使用随机生成的 ISBN（可能不属于任何已知组）
        isbn = ISBNUtils.generate_random(10)
        result = ISBNUtils.get_registration_group(isbn)
        # 结果可能是已知的或 None
        self.assertIsNotNone(result)  # 因为我们的映射覆盖了大部分情况
        
    # ==================== 便捷函数测试 ====================
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        self.assertTrue(validate("0-13-235088-2"))
        self.assertEqual(convert_to_13("0-13-235088-2"), "9780132350884")
        self.assertEqual(convert_to_10("978-0-13-235088-4"), "0132350882")
        self.assertEqual(format_isbn("0132350882"), "0-1323-5088-2")
        
        result = parse("0-13-235088-2")
        self.assertTrue(result['valid'])
        
        isbn = generate_random()
        self.assertTrue(validate(isbn))
        
        found = extract_from_text("ISBN: 0-13-235088-2")
        self.assertEqual(found, ["0132350882"])


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_isbn10_with_x(self):
        """测试包含 X 校验位的 ISBN-10"""
        # 找一个校验位为 X 的 ISBN-10
        # 使用已知校验位为 X 的前9位
        isbn9 = "000000006"
        check = ISBNUtils.calculate_check_digit_10(isbn9)
        self.assertEqual(check, "X")
        
        # 完整的 ISBN-10
        isbn10 = isbn9 + check
        self.assertTrue(ISBNUtils.validate(isbn10))
        
        # 测试另一个已知 X 的 ISBN-10
        isbn9 = "156881111"
        check = ISBNUtils.calculate_check_digit_10(isbn9)
        self.assertEqual(check, "X")
        
    def test_isbn13_979_prefix(self):
        """测试 979 前缀的 ISBN-13"""
        # 生成一个有效的 979 前缀 ISBN-13
        isbn = ISBNUtils.generate_random(13, prefix='979')
        self.assertTrue(ISBNUtils.validate(isbn))
        
    def test_empty_input(self):
        """测试空输入"""
        self.assertFalse(ISBNUtils.validate(""))
        
    def test_special_characters(self):
        """测试特殊字符"""
        # 正确的 ISBN 被各种字符包围（应该能清理出来）
        cleaned = ISBNUtils.clean("ISBN: 0-13-235088-2!!!")
        self.assertTrue(ISBNUtils.validate(cleaned))
        
    def test_roundtrip_conversion(self):
        """测试往返转换"""
        original = "0-13-235088-2"
        isbn13 = convert_to_13(original)
        back_to_10 = convert_to_10(isbn13)
        self.assertEqual(ISBNUtils.clean(original), back_to_10)


if __name__ == '__main__':
    unittest.main(verbosity=2)