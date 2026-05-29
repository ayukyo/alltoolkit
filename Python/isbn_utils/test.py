"""
ISBN Utils 测试模块

测试 ISBN-10 和 ISBN-13 验证、转换、解析功能
"""

import unittest
from mod import (
    clean_isbn,
    calculate_check_digit_isbn10,
    calculate_check_digit_isbn13,
    is_valid_isbn10,
    is_valid_isbn13,
    is_valid_isbn,
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    detect_isbn_type,
    format_isbn,
    get_registration_group,
    parse_isbn,
    batch_validate,
    find_isbns_in_text,
    compare_isbns,
    ISBNInfo,
)


class TestCleanISBN(unittest.TestCase):
    """测试 ISBN 清理功能"""
    
    def test_clean_with_hyphens(self):
        self.assertEqual(clean_isbn('978-0-306-40615-7'), '9780306406157')
        self.assertEqual(clean_isbn('0-306-40615-2'), '0306406152')
    
    def test_clean_with_spaces(self):
        self.assertEqual(clean_isbn('978 0 306 40615 7'), '9780306406157')
        self.assertEqual(clean_isbn('0 306 40615 2'), '0306406152')
    
    def test_clean_with_mixed(self):
        self.assertEqual(clean_isbn('978-0 306-40615-7'), '9780306406157')
    
    def test_clean_lowercase_x(self):
        self.assertEqual(clean_isbn('0-306-40615-x'), '030640615X')
    
    def test_clean_already_clean(self):
        self.assertEqual(clean_isbn('9780306406157'), '9780306406157')


class TestCalculateCheckDigitISBN10(unittest.TestCase):
    """测试 ISBN-10 校验位计算"""
    
    def test_calculate_check_digit_numeric(self):
        # 已知 ISBN-10 的校验位（已验证）
        self.assertEqual(calculate_check_digit_isbn10('030640615'), '2')  # 银河系漫游指南
        self.assertEqual(calculate_check_digit_isbn10('026203384'), '4')  # 算法导论
        self.assertEqual(calculate_check_digit_isbn10('711553864'), '6')  # Python编程
    
    def test_calculate_check_digit_x(self):
        # 校验位为 X 的情况（计算得到的真实例子）
        self.assertEqual(calculate_check_digit_isbn10('100308625'), 'X')
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            calculate_check_digit_isbn10('12345678')  # 8 位
        with self.assertRaises(ValueError):
            calculate_check_digit_isbn10('12345678a')  # 包含字母


class TestCalculateCheckDigitISBN13(unittest.TestCase):
    """测试 ISBN-13 校验位计算"""
    
    def test_calculate_check_digit(self):
        # 已验证的正确校验位
        self.assertEqual(calculate_check_digit_isbn13('978030640615'), '7')
        self.assertEqual(calculate_check_digit_isbn13('978026203384'), '8')
        self.assertEqual(calculate_check_digit_isbn13('978711553864'), '2')
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            calculate_check_digit_isbn13('97803064061')  # 11 位
        with self.assertRaises(ValueError):
            calculate_check_digit_isbn13('97803064061a')  # 包含字母


class TestIsValidISBN10(unittest.TestCase):
    """测试 ISBN-10 验证"""
    
    def test_valid_isbn10(self):
        self.assertTrue(is_valid_isbn10('0306406152'))  # 银河系漫游指南
        self.assertTrue(is_valid_isbn10('0-306-40615-2'))
        self.assertTrue(is_valid_isbn10('0262033844'))  # 算法导论
        self.assertTrue(is_valid_isbn10('7115538646'))  # Python编程
        self.assertTrue(is_valid_isbn10('100308625X'))  # 以 X 结尾
    
    def test_invalid_isbn10(self):
        self.assertFalse(is_valid_isbn10('0306406153'))  # 错误校验位
        self.assertFalse(is_valid_isbn10('030640615'))   # 太短
        self.assertFalse(is_valid_isbn10('03064061522'))  # 太长
        self.assertFalse(is_valid_isbn10('abcdefghij'))  # 非数字
    
    def test_isbn13_not_isbn10(self):
        self.assertFalse(is_valid_isbn10('9780306406157'))


class TestIsValidISBN13(unittest.TestCase):
    """测试 ISBN-13 验证"""
    
    def test_valid_isbn13(self):
        self.assertTrue(is_valid_isbn13('9780306406157'))
        self.assertTrue(is_valid_isbn13('978-0-306-40615-7'))
        self.assertTrue(is_valid_isbn13('9780262033848'))
        self.assertTrue(is_valid_isbn13('9787115538642'))
        self.assertTrue(is_valid_isbn13('9791234567896'))  # 979 前缀
    
    def test_invalid_isbn13(self):
        self.assertFalse(is_valid_isbn13('9780306406158'))  # 错误校验位
        self.assertFalse(is_valid_isbn13('978030640615'))   # 太短
        self.assertFalse(is_valid_isbn13('97803064061577'))  # 太长
        self.assertFalse(is_valid_isbn13('9770306406154'))  # 无效前缀
    
    def test_isbn10_not_isbn13(self):
        self.assertFalse(is_valid_isbn13('0306406152'))


class TestIsValidISBN(unittest.TestCase):
    """测试通用 ISBN 验证"""
    
    def test_valid_isbn10(self):
        self.assertTrue(is_valid_isbn('0306406152'))
        self.assertTrue(is_valid_isbn('0-306-40615-2'))
    
    def test_valid_isbn13(self):
        self.assertTrue(is_valid_isbn('9780306406157'))
        self.assertTrue(is_valid_isbn('978-0-306-40615-7'))
    
    def test_invalid_isbn(self):
        self.assertFalse(is_valid_isbn('12345'))
        self.assertFalse(is_valid_isbn('not an isbn'))


class TestISBN10ToISBN13(unittest.TestCase):
    """测试 ISBN-10 转 ISBN-13"""
    
    def test_conversion(self):
        self.assertEqual(isbn10_to_isbn13('0306406152'), '9780306406157')
        self.assertEqual(isbn10_to_isbn13('0-306-40615-2'), '9780306406157')
        self.assertEqual(isbn10_to_isbn13('0262033844'), '9780262033848')
        self.assertEqual(isbn10_to_isbn13('7115538646'), '9787115538642')
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            isbn10_to_isbn13('invalid')


class TestISBN13ToISBN10(unittest.TestCase):
    """测试 ISBN-13 转 ISBN-10"""
    
    def test_conversion(self):
        self.assertEqual(isbn13_to_isbn10('9780306406157'), '0306406152')
        self.assertEqual(isbn13_to_isbn10('978-0-306-40615-7'), '0306406152')
        self.assertEqual(isbn13_to_isbn10('9780262033848'), '0262033844')
        self.assertEqual(isbn13_to_isbn10('9787115538642'), '7115538646')
    
    def test_979_prefix_cannot_convert(self):
        # 979 前缀的 ISBN-13 无法转换为 ISBN-10
        self.assertIsNone(isbn13_to_isbn10('9791234567896'))
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            isbn13_to_isbn10('invalid')


class TestDetectISBNType(unittest.TestCase):
    """测试 ISBN 类型检测"""
    
    def test_detect_isbn10(self):
        self.assertEqual(detect_isbn_type('0306406152'), 'ISBN-10')
        self.assertEqual(detect_isbn_type('100308625X'), 'ISBN-10')
    
    def test_detect_isbn13(self):
        self.assertEqual(detect_isbn_type('9780306406157'), 'ISBN-13')
        self.assertEqual(detect_isbn_type('9791234567896'), 'ISBN-13')
    
    def test_detect_invalid(self):
        self.assertIsNone(detect_isbn_type('invalid'))
        self.assertIsNone(detect_isbn_type('12345'))


class TestFormatISBN(unittest.TestCase):
    """测试 ISBN 格式化"""
    
    def test_format_isbn13(self):
        self.assertEqual(format_isbn('9780306406157'), '978-0-306-40615-7')
        self.assertEqual(format_isbn('9780262033848'), '978-0-262-03384-8')
    
    def test_format_isbn10(self):
        self.assertEqual(format_isbn('0306406152'), '0-306-40615-2')
        self.assertEqual(format_isbn('0262033844'), '0-262-03384-4')
    
    def test_format_with_custom_separator(self):
        self.assertEqual(format_isbn('9780306406157', ' '), '978 0 306 40615 7')
        self.assertEqual(format_isbn('0306406152', ''), '0306406152')
    
    def test_format_invalid(self):
        # 无效 ISBN 原样返回
        self.assertEqual(format_isbn('invalid'), 'invalid')


class TestGetRegistrationGroup(unittest.TestCase):
    """测试注册组获取"""
    
    def test_english_group(self):
        self.assertEqual(get_registration_group('0306406152'), 'English (English language)')
        self.assertEqual(get_registration_group('9780306406157'), 'English (English language)')
        self.assertEqual(get_registration_group('0262033844'), 'English (English language)')
    
    def test_chinese_group(self):
        self.assertEqual(get_registration_group('7115538646'), 'China')
        self.assertEqual(get_registration_group('9787115538642'), 'China')
    
    def test_japanese_group(self):
        self.assertEqual(get_registration_group('4123456789'), 'Japan')
    
    def test_korean_group(self):
        self.assertEqual(get_registration_group('8991234567'), 'Korea')
    
    def test_german_group(self):
        self.assertEqual(get_registration_group('3123456789'), 'German')


class TestParseISBN(unittest.TestCase):
    """测试 ISBN 解析"""
    
    def test_parse_valid_isbn10(self):
        info = parse_isbn('0306406152')
        self.assertEqual(info.isbn, '0306406152')
        self.assertEqual(info.isbn10, '0306406152')
        self.assertEqual(info.isbn13, '9780306406157')
        self.assertTrue(info.is_valid)
        self.assertIsNone(info.prefix)
        self.assertEqual(info.check_digit, '2')
    
    def test_parse_valid_isbn13(self):
        info = parse_isbn('9780306406157')
        self.assertEqual(info.isbn, '9780306406157')
        self.assertEqual(info.isbn10, '0306406152')
        self.assertEqual(info.isbn13, '9780306406157')
        self.assertTrue(info.is_valid)
        self.assertEqual(info.prefix, '978')
        self.assertEqual(info.check_digit, '7')
    
    def test_parse_isbn10_with_x_check(self):
        # ISBN-10 以 X 结尾
        info = parse_isbn('100308625X')
        self.assertTrue(info.is_valid)
        self.assertEqual(info.isbn10, '100308625X')
        self.assertEqual(info.check_digit, 'X')
    
    def test_parse_invalid_isbn(self):
        info = parse_isbn('invalid')
        self.assertFalse(info.is_valid)
        self.assertIsNone(info.isbn10)
        self.assertEqual(info.isbn13, '')


class TestBatchValidate(unittest.TestCase):
    """测试批量验证"""
    
    def test_batch_validate(self):
        isbns = [
            '0306406152',
            '9780306406157',
            'invalid',
            '7115538646',
        ]
        result = batch_validate(isbns)
        self.assertTrue(result['0306406152'])
        self.assertTrue(result['9780306406157'])
        self.assertFalse(result['invalid'])
        self.assertTrue(result['7115538646'])


class TestFindISBNsInText(unittest.TestCase):
    """测试文本中提取 ISBN"""
    
    def test_find_isbns(self):
        text = """
        这里有几本书的ISBN：
        ISBN: 978-0-306-40615-7
        另一本书的编号是 0-306-40615-2
        还有一个无效的：1234567890
        有效的中文书：9787115538642
        """
        found = find_isbns_in_text(text)
        self.assertIn('9780306406157', found)
        self.assertIn('0306406152', found)
        self.assertIn('9787115538642', found)
        # 无效的 ISBN 不应该被包含
        self.assertNotIn('1234567890', found)
    
    def test_find_no_isbns(self):
        text = "这段文本没有ISBN"
        found = find_isbns_in_text(text)
        self.assertEqual(found, [])


class TestCompareISBNs(unittest.TestCase):
    """测试 ISBN 比较"""
    
    def test_same_isbn(self):
        self.assertTrue(compare_isbns('0306406152', '0306406152'))
        self.assertTrue(compare_isbns('9780306406157', '9780306406157'))
    
    def test_equivalent_isbns(self):
        # 同一本书的 ISBN-10 和 ISBN-13 应该等价
        self.assertTrue(compare_isbns('0306406152', '9780306406157'))
        self.assertTrue(compare_isbns('9780306406157', '0306406152'))
    
    def test_different_isbns(self):
        self.assertFalse(compare_isbns('0306406152', '0262033844'))
        self.assertFalse(compare_isbns('9780306406157', '9780262033848'))
    
    def test_with_formatting(self):
        self.assertTrue(compare_isbns('0-306-40615-2', '9780306406157'))
        self.assertTrue(compare_isbns('978-0-306-40615-7', '0306406152'))


if __name__ == '__main__':
    unittest.main(verbosity=2)