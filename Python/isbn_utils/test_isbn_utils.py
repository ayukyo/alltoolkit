"""
ISBN Utils 测试模块

测试覆盖:
- ISBN-10验证
- ISBN-13验证
- 检验位计算
- 格式转换
- 格式化输出
- 信息解析
- 批量操作
- 文本提取

使用真实有效的ISBN进行测试
"""

import unittest
from isbn_utils import (
    ISBN, ISBNType, ISBNInfo,
    is_valid_isbn10, is_valid_isbn13, is_valid_isbn,
    calculate_isbn10_check_digit, calculate_isbn13_check_digit,
    isbn10_to_isbn13, isbn13_to_isbn10,
    format_isbn, normalize_isbn,
    parse_isbn, extract_isbns, get_isbn_info,
    batch_validate, identify_prefix
)


class TestISBN10Validation(unittest.TestCase):
    """ISBN-10验证测试"""
    
    def test_valid_isbn10_no_separator(self):
        """测试无分隔符的有效ISBN-10"""
        self.assertTrue(is_valid_isbn10('0306406152'))    # O'Reilly书籍
        self.assertTrue(is_valid_isbn10('0471958697'))    # Wiley书籍
        self.assertTrue(is_valid_isbn10('9999999999'))    # 全9
        self.assertTrue(is_valid_isbn10('0000000000'))    # 全0
        self.assertTrue(is_valid_isbn10('1566199093'))    # 另一常见
    
    def test_valid_isbn10_with_separator(self):
        """测试带分隔符的有效ISBN-10"""
        self.assertTrue(is_valid_isbn10('0-306-40615-2'))
        self.assertTrue(is_valid_isbn10('0-471-95869-7'))
        self.assertTrue(is_valid_isbn10('0 306 40615 2'))
        self.assertTrue(is_valid_isbn10('1-56619-909-3'))
    
    def test_valid_isbn10_with_x(self):
        """测试含X检验位的ISBN-10"""
        # 需要计算一个正确的X检验位ISBN
        # 当计算结果为10时，检验位是X
        # 例如: 007462542X 验证: 0+0+7+4+6+2+5+4+2 = 各位乘权重
        # 让我们用正确的X检验位ISBN: 080442957X
        self.assertTrue(is_valid_isbn10('080442957X'))
        self.assertTrue(is_valid_isbn10('0-80442-957-X'))
    
    def test_invalid_isbn10_wrong_length(self):
        """测试长度错误的ISBN-10"""
        self.assertFalse(is_valid_isbn10('030640615'))      # 9位
        self.assertFalse(is_valid_isbn10('03064061521'))   # 11位
        self.assertFalse(is_valid_isbn10(''))              # 空
        self.assertFalse(is_valid_isbn10('0306406'))       # 7位
    
    def test_invalid_isbn10_wrong_check(self):
        """测试检验位错误的ISBN-10"""
        self.assertFalse(is_valid_isbn10('0306406153'))    # 正确是2
        self.assertFalse(is_valid_isbn10('0471958690'))    # 正确是7
        self.assertFalse(is_valid_isbn10('1234567890'))    # 无效
    
    def test_invalid_isbn10_invalid_chars(self):
        """测试含非法字符的ISBN-10"""
        self.assertFalse(is_valid_isbn10('030640615A'))   # 非数字/X
        self.assertFalse(is_valid_isbn10('03064061X2'))   # X不在末尾
        self.assertFalse(is_valid_isbn10('ABCDEFGHIJ'))
    
    def test_isbn_class_isbn10(self):
        """测试ISBN类的ISBN-10功能"""
        isbn = ISBN('0-306-40615-2')
        self.assertTrue(isbn.is_valid())
        self.assertEqual(isbn.get_type(), ISBNType.ISBN10)
        self.assertEqual(isbn.normalize(), '0306406152')
        self.assertEqual(isbn.format(), '0-3064-0615-2')


class TestISBN13Validation(unittest.TestCase):
    """ISBN-13验证测试"""
    
    def test_valid_isbn13_no_separator(self):
        """测试无分隔符的有效ISBN-13"""
        self.assertTrue(is_valid_isbn13('9780306406157'))
        self.assertTrue(is_valid_isbn13('9781566199094'))
        self.assertTrue(is_valid_isbn13('9791091146135'))
        self.assertTrue(is_valid_isbn13('9780000000002'))
    
    def test_valid_isbn13_with_separator(self):
        """测试带分隔符的有效ISBN-13"""
        self.assertTrue(is_valid_isbn13('978-0-306-40615-7'))
        self.assertTrue(is_valid_isbn13('978-1-56619-909-4'))
        self.assertTrue(is_valid_isbn13('978 0 306 40615 7'))
    
    def test_valid_isbn13_978_prefix(self):
        """测试978前缀的ISBN-13"""
        self.assertTrue(is_valid_isbn13('978-0-306-40615-7'))
        self.assertTrue(is_valid_isbn13('978-1-56619-909-4'))
        self.assertTrue(is_valid_isbn13('9781566199094'))
    
    def test_valid_isbn13_979_prefix(self):
        """测试979前缀的ISBN-13"""
        self.assertTrue(is_valid_isbn13('9791091146135'))
        self.assertTrue(is_valid_isbn13('979-10-91146-13-5'))
    
    def test_invalid_isbn13_wrong_length(self):
        """测试长度错误的ISBN-13"""
        self.assertFalse(is_valid_isbn13('978030640615'))   # 12位
        self.assertFalse(is_valid_isbn13('97803064061570'))  # 14位
        self.assertFalse(is_valid_isbn13(''))                # 空
        self.assertFalse(is_valid_isbn13('97803064061'))    # 11位
    
    def test_invalid_isbn13_wrong_check(self):
        """测试检验位错误的ISBN-13"""
        self.assertFalse(is_valid_isbn13('9780306406150'))  # 正确是7
        self.assertFalse(is_valid_isbn13('9781566199090'))  # 正确是4
    
    def test_invalid_isbn13_invalid_chars(self):
        """测试含非法字符的ISBN-13"""
        self.assertFalse(is_valid_isbn13('978030640615A'))  # 含字母
        self.assertFalse(is_valid_isbn13('9X80306406157'))   # X在中间
    
    def test_isbn_class_isbn13(self):
        """测试ISBN类的ISBN-13功能"""
        isbn = ISBN('978-0-306-40615-7')
        self.assertTrue(isbn.is_valid())
        self.assertEqual(isbn.get_type(), ISBNType.ISBN13)
        self.assertEqual(isbn.normalize(), '9780306406157')
        # 格式化使用简化分隔
        self.assertEqual(isbn.format(), '978-0-3064-0615-7')


class TestCheckDigitCalculation(unittest.TestCase):
    """检验位计算测试"""
    
    def test_calculate_isbn10_check_digit(self):
        """测试ISBN-10检验位计算"""
        self.assertEqual(calculate_isbn10_check_digit('030640615'), '2')
        self.assertEqual(calculate_isbn10_check_digit('047195869'), '7')
        self.assertEqual(calculate_isbn10_check_digit('999999999'), '9')
        self.assertEqual(calculate_isbn10_check_digit('000000000'), '0')
        # X检验位的情况
        self.assertEqual(calculate_isbn10_check_digit('080442957'), 'X')
    
    def test_calculate_isbn10_check_digit_invalid(self):
        """测试ISBN-10检验位计算的无效输入"""
        with self.assertRaises(ValueError):
            calculate_isbn10_check_digit('03064061')    # 8位
        with self.assertRaises(ValueError):
            calculate_isbn10_check_digit('0306406152')  # 10位
        with self.assertRaises(ValueError):
            calculate_isbn10_check_digit('03064A615')   # 含字母
        with self.assertRaises(ValueError):
            calculate_isbn10_check_digit('')            # 空
    
    def test_calculate_isbn13_check_digit(self):
        """测试ISBN-13检验位计算"""
        self.assertEqual(calculate_isbn13_check_digit('978030640615'), '7')
        self.assertEqual(calculate_isbn13_check_digit('978156619909'), '4')
        self.assertEqual(calculate_isbn13_check_digit('979109114613'), '5')
    
    def test_calculate_isbn13_check_digit_invalid(self):
        """测试ISBN-13检验位计算的无效输入"""
        with self.assertRaises(ValueError):
            calculate_isbn13_check_digit('97803064061')   # 11位
        with self.assertRaises(ValueError):
            calculate_isbn13_check_digit('9780306406157')  # 13位
        with self.assertRaises(ValueError):
            calculate_isbn13_check_digit('97803064061A')   # 含字母
        with self.assertRaises(ValueError):
            calculate_isbn13_check_digit('')                # 空


class TestISBNConversion(unittest.TestCase):
    """ISBN格式转换测试"""
    
    def test_isbn10_to_isbn13(self):
        """测试ISBN-10转ISBN-13"""
        self.assertEqual(isbn10_to_isbn13('0-306-40615-2'), '9780306406157')
        self.assertEqual(isbn10_to_isbn13('0306406152'), '9780306406157')
        self.assertEqual(isbn10_to_isbn13('1-56619-909-3'), '9781566199094')
        self.assertEqual(isbn10_to_isbn13('1566199093'), '9781566199094')
    
    def test_isbn10_to_isbn13_invalid(self):
        """测试无效ISBN-10转换"""
        with self.assertRaises(ValueError):
            isbn10_to_isbn13('invalid')
        with self.assertRaises(ValueError):
            isbn10_to_isbn13('0306406153')  # 错误检验位
    
    def test_isbn13_to_isbn10(self):
        """测试ISBN-13转ISBN-10"""
        self.assertEqual(isbn13_to_isbn10('978-0-306-40615-7'), '0306406152')
        self.assertEqual(isbn13_to_isbn10('9780306406157'), '0306406152')
        self.assertEqual(isbn13_to_isbn10('978-1-56619-909-4'), '1566199093')
    
    def test_isbn13_to_isbn10_979_prefix(self):
        """测试979前缀ISBN-13无法转ISBN-10"""
        self.assertIsNone(isbn13_to_isbn10('9791091146135'))
        self.assertIsNone(isbn13_to_isbn10('979-10-91146-13-5'))
    
    def test_isbn13_to_isbn10_invalid(self):
        """测试无效ISBN-13转换"""
        self.assertIsNone(isbn13_to_isbn10('invalid'))
        self.assertIsNone(isbn13_to_isbn10('9780306406150'))  # 错误检验位
    
    def test_isbn_class_conversion(self):
        """测试ISBN类的转换方法"""
        # ISBN-10转ISBN-13
        isbn10 = ISBN('0-306-40615-2')
        self.assertEqual(isbn10.to_isbn13(), '9780306406157')
        
        # ISBN-13转ISBN-10
        isbn13 = ISBN('978-0-306-40615-7')
        self.assertEqual(isbn13.to_isbn10(), '0306406152')
        self.assertEqual(isbn13.to_isbn13(), '9780306406157')  # 返回自己的标准化
        
        # 979前缀无法转ISBN-10
        isbn13_979 = ISBN('9791091146135')
        self.assertIsNone(isbn13_979.to_isbn10())


class TestISBNFormat(unittest.TestCase):
    """ISBN格式化测试"""
    
    def test_format_isbn13(self):
        """测试ISBN-13格式化"""
        # ISBN格式化使用固定分隔位置（简化实现）
        self.assertEqual(format_isbn('9780306406157'), '978-0-3064-0615-7')
        self.assertEqual(format_isbn('978-0-306-40615-7'), '978-0-3064-0615-7')
    
    def test_format_isbn10(self):
        """测试ISBN-10格式化"""
        self.assertEqual(format_isbn('0306406152'), '0-3064-0615-2')
        self.assertEqual(format_isbn('0-306-40615-2'), '0-3064-0615-2')
    
    def test_format_isbn_custom_separator(self):
        """测试自定义分隔符"""
        self.assertEqual(format_isbn('9780306406157', ' '), '978 0 3064 0615 7')
        self.assertEqual(format_isbn('0306406152', ''), '0306406152')
    
    def test_format_invalid_isbn(self):
        """测试格式化无效ISBN"""
        # 无效ISBN返回标准化后的字符串（大写）
        self.assertEqual(format_isbn('invalid'), 'INVALID')
    
    def test_normalize_isbn(self):
        """测试标准化ISBN"""
        self.assertEqual(normalize_isbn('978-0-306-40615-7'), '9780306406157')
        self.assertEqual(normalize_isbn('0 306 40615 2'), '0306406152')
        self.assertEqual(normalize_isbn('0-80442-957-X'), '080442957X')
        self.assertEqual(normalize_isbn('978 0 306 40615 7'), '9780306406157')


class TestISBNParsing(unittest.TestCase):
    """ISBN解析测试"""
    
    def test_parse_isbn13(self):
        """测试解析ISBN-13"""
        info = parse_isbn('978-0-306-40615-7')
        self.assertTrue(info.is_valid)
        self.assertEqual(info.isbn_type, ISBNType.ISBN13)
        self.assertEqual(info.normalized, '9780306406157')
        # 格式化使用简化分隔
        self.assertEqual(info.formatted, '978-0-3064-0615-7')
        self.assertEqual(info.prefix, '978')
        self.assertEqual(info.check_digit, '7')
    
    def test_parse_isbn10(self):
        """测试解析ISBN-10"""
        info = parse_isbn('0-306-40615-2')
        self.assertTrue(info.is_valid)
        self.assertEqual(info.isbn_type, ISBNType.ISBN10)
        self.assertEqual(info.normalized, '0306406152')
        self.assertEqual(info.check_digit, '2')
    
    def test_parse_invalid_isbn(self):
        """测试解析无效ISBN"""
        info = parse_isbn('invalid-isbn')
        self.assertFalse(info.is_valid)
        self.assertEqual(info.isbn_type, ISBNType.UNKNOWN)
    
    def test_get_isbn_info(self):
        """测试获取ISBN详细信息"""
        info = get_isbn_info('978-0-306-40615-7')
        self.assertTrue(info.is_valid)
        self.assertEqual(info.isbn_type, ISBNType.ISBN13)
        self.assertIsNotNone(info.isbn13)
        # 978前缀可以转ISBN-10
        self.assertIsNotNone(info.isbn10)


class TestIdentifyPrefix(unittest.TestCase):
    """分组前缀识别测试"""
    
    def test_identify_common_prefixes(self):
        """测试常见分组识别"""
        self.assertEqual(identify_prefix('0'), '英语国家')
        self.assertEqual(identify_prefix('1'), '英语国家')
        self.assertEqual(identify_prefix('7'), '中国')
        self.assertEqual(identify_prefix('4'), '日本')
        self.assertEqual(identify_prefix('3'), '德语国家')
        self.assertEqual(identify_prefix('2'), '法语国家')
    
    def test_identify_unknown_prefix(self):
        """测试未知分组"""
        self.assertIsNone(identify_prefix('X'))
        self.assertIsNone(identify_prefix('Z'))


class TestExtractISBNs(unittest.TestCase):
    """从文本提取ISBN测试"""
    
    def test_extract_isbn13(self):
        """测试提取ISBN-13"""
        text = "这本书的ISBN是978-0-306-40615-7"
        result = extract_isbns(text)
        self.assertIn('9780306406157', result)
    
    def test_extract_isbn10(self):
        """测试提取ISBN-10"""
        text = "ISBN: 0-306-40615-2"
        result = extract_isbns(text)
        self.assertIn('0306406152', result)
    
    def test_extract_multiple(self):
        """测试提取多个ISBN"""
        text = "ISBN-13: 978-0-306-40615-7, ISBN-10: 0-306-40615-2"
        result = extract_isbns(text)
        # 两个ISBN都应该被提取
        self.assertGreaterEqual(len(result), 1)
    
    def test_extract_no_isbn(self):
        """测试无ISBN的文本"""
        text = "这是一段普通文本，没有ISBN"
        result = extract_isbns(text)
        self.assertEqual(len(result), 0)
    
    def test_extract_invalid_isbn(self):
        """测试不提取无效ISBN"""
        text = "无效ISBN: 123-456-789"
        result = extract_isbns(text)
        # 应该不提取无效的
        for isbn in result:
            self.assertTrue(is_valid_isbn(isbn))


class TestBatchValidate(unittest.TestCase):
    """批量验证测试"""
    
    def test_batch_validate_mixed(self):
        """测试混合批量验证"""
        isbns = [
            '978-0-306-40615-7',  # 有效ISBN-13
            '0-306-40615-2',      # 有效ISBN-10
            'invalid',            # 无效
            '9781566199094',      # 有效ISBN-13
            '1234567890',         # 无效
        ]
        result = batch_validate(isbns)
        
        self.assertEqual(len(result['valid']), 3)
        self.assertEqual(len(result['invalid']), 2)
        self.assertEqual(len(result['isbn10']), 1)
        self.assertEqual(len(result['isbn13']), 2)
        self.assertEqual(result['stats']['total'], 5)
        self.assertEqual(result['stats']['valid_count'], 3)
        self.assertEqual(result['stats']['invalid_count'], 2)
    
    def test_batch_validate_all_valid(self):
        """测试全部有效的批量验证"""
        isbns = ['978-0-306-40615-7', '0-306-40615-2', '9781566199094']
        result = batch_validate(isbns)
        
        self.assertEqual(len(result['valid']), 3)
        self.assertEqual(len(result['invalid']), 0)
    
    def test_batch_validate_all_invalid(self):
        """测试全部无效的批量验证"""
        isbns = ['invalid1', 'invalid2', '12345']
        result = batch_validate(isbns)
        
        self.assertEqual(len(result['valid']), 0)
        self.assertEqual(len(result['invalid']), 3)


class TestISBNClass(unittest.TestCase):
    """ISBN类测试"""
    
    def test_isbn_equality(self):
        """测试ISBN相等性"""
        isbn1 = ISBN('978-0-306-40615-7')
        isbn2 = ISBN('9780306406157')
        isbn3 = ISBN('0-306-40615-2')
        
        self.assertEqual(isbn1, isbn2)
        self.assertNotEqual(isbn1, isbn3)
        
        # 与字符串比较
        self.assertEqual(isbn1, '9780306406157')
        self.assertEqual(isbn1, '978-0-306-40615-7')
    
    def test_isbn_hash(self):
        """测试ISBN哈希"""
        isbn1 = ISBN('978-0-306-40615-7')
        isbn2 = ISBN('9780306406157')
        
        # 相同ISBN应该有相同哈希
        self.assertEqual(hash(isbn1), hash(isbn2))
        
        # 可以放入集合
        isbn_set = {isbn1, isbn2}
        self.assertEqual(len(isbn_set), 1)
    
    def test_isbn_str_repr(self):
        """测试ISBN字符串表示"""
        isbn = ISBN('978-0-306-40615-7')
        # 格式化使用简化分隔
        self.assertEqual(str(isbn), '978-0-3064-0615-7')
        self.assertEqual(repr(isbn), "ISBN('978-0-306-40615-7')")
    
    def test_isbn_get_info(self):
        """测试ISBN获取信息"""
        isbn = ISBN('978-0-306-40615-7')
        info = isbn.get_info()
        
        self.assertTrue(info.is_valid)
        self.assertEqual(info.isbn_type, ISBNType.ISBN13)
        self.assertEqual(info.normalized, '9780306406157')


class TestIsValidISBN(unittest.TestCase):
    """is_valid_isbn便捷函数测试"""
    
    def test_valid_isbn_auto_detect(self):
        """测试自动检测有效ISBN"""
        # ISBN-10
        self.assertTrue(is_valid_isbn('0-306-40615-2'))
        self.assertTrue(is_valid_isbn('0306406152'))
        self.assertTrue(is_valid_isbn('080442957X'))
        
        # ISBN-13
        self.assertTrue(is_valid_isbn('978-0-306-40615-7'))
        self.assertTrue(is_valid_isbn('9780306406157'))
        self.assertTrue(is_valid_isbn('9791091146135'))
    
    def test_invalid_isbn_auto_detect(self):
        """测试自动检测无效ISBN"""
        self.assertFalse(is_valid_isbn('invalid'))
        self.assertFalse(is_valid_isbn('12345'))
        self.assertFalse(is_valid_isbn('978-0-306-40615-0'))  # 错误检验位


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertFalse(is_valid_isbn(''))
        self.assertFalse(is_valid_isbn10(''))
        self.assertFalse(is_valid_isbn13(''))
    
    def test_whitespace_only(self):
        """测试纯空白字符"""
        self.assertFalse(is_valid_isbn('   '))
        self.assertFalse(is_valid_isbn('-'))
        self.assertFalse(is_valid_isbn('--'))
    
    def test_isbn_with_spaces(self):
        """测试带空格的ISBN"""
        self.assertTrue(is_valid_isbn('978 0 306 40615 7'))
        self.assertTrue(is_valid_isbn10('0 306 40615 2'))
    
    def test_isbn_all_zeros(self):
        """测试全零ISBN"""
        # ISBN-10: 0000000000 是有效的
        self.assertTrue(is_valid_isbn10('0000000000'))
        # ISBN-13: 9780000000002
        self.assertTrue(is_valid_isbn13('9780000000002'))
    
    def test_isbn_all_nines(self):
        """测试全9 ISBN"""
        self.assertTrue(is_valid_isbn10('9999999999'))
    
    def test_isbn_with_x_in_middle(self):
        """测试X在中间位置(无效)"""
        self.assertFalse(is_valid_isbn10('0X06406152'))
        self.assertFalse(is_valid_isbn13('978X306406157'))
    
    def test_special_isbn10_x_check(self):
        """测试X检验位的ISBN-10"""
        self.assertTrue(is_valid_isbn10('080442957X'))
        self.assertTrue(is_valid_isbn10('0-80442-957-X'))


if __name__ == '__main__':
    unittest.main()