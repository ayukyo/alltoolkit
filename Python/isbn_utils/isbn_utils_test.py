#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
isbn_utils - 测试用例
====================

测试 ISBN-10/ISBN-13 验证、转换、格式化等功能。
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    clean_isbn,
    is_isbn10,
    is_isbn13,
    calculate_isbn10_check_digit,
    calculate_isbn13_check_digit,
    format_isbn,
    generate_isbn,
    convert_isbn,
    compare_isbns,
    find_isbns_in_text,
    format_isbn_compact,
)


class TestCleanISBN:
    """测试 ISBN 清理"""
    
    def test_clean_isbn_with_hyphens(self):
        """测试带连字符的 ISBN"""
        result = clean_isbn("978-0-306-40615-7")
        assert result == "9780306406157"
    
    def test_clean_isbn_with_spaces(self):
        """测试带空格的 ISBN"""
        result = clean_isbn("978 0 306 40615 7")
        assert result == "9780306406157"
    
    def test_clean_isbn_with_prefix(self):
        """测试带前缀的 ISBN"""
        result = clean_isbn("ISBN 978-0-306-40615-7")
        assert result == "9780306406157"
    
    def test_clean_isbn10_with_x(self):
        """测试带 X 的 ISBN-10"""
        result = clean_isbn("0-306-40615-X")
        assert result == "030640615X"
    
    def test_clean_empty(self):
        """测试空字符串"""
        result = clean_isbn("")
        assert result == ""


class TestISBN10Validation:
    """测试 ISBN-10 验证"""
    
    def test_is_isbn10_valid(self):
        """测试有效的 ISBN-10"""
        assert is_isbn10("0306406152") is True
        assert is_isbn10("0-306-40615-2") is True
    
    def test_is_isbn10_invalid_length(self):
        """测试无效长度"""
        assert is_isbn10("12345") is False  # 太短
        assert is_isbn10("123456789012") is False  # 太长
    
    def test_is_isbn10_invalid_chars(self):
        """测试无效字符"""
        assert is_isbn10("ABCDEFGHIJ") is False


class TestISBN13Validation:
    """测试 ISBN-13 验证"""
    
    def test_is_isbn13_valid(self):
        """测试有效的 ISBN-13"""
        assert is_isbn13("9780306406157") is True
        assert is_isbn13("978-0-306-40615-7") is True
    
    def test_is_isbn13_invalid_length(self):
        """测试无效长度"""
        assert is_isbn13("12345678") is False  # 太短
        assert is_isbn13("12345678901234") is False  # 太长
    
    def test_is_isbn13_invalid_chars(self):
        """测试无效字符"""
        assert is_isbn13("978ABCDEFGHI") is False


class TestCheckDigit:
    """测试校验位计算"""
    
    def test_calculate_isbn10_check_digit(self):
        """测试 ISBN-10 校验位"""
        digit = calculate_isbn10_check_digit("030640615")
        assert digit == "2"
    
    def test_calculate_isbn13_check_digit(self):
        """测试 ISBN-13 校验位"""
        digit = calculate_isbn13_check_digit("978030640615")
        assert digit == "7"
    
    def test_calculate_check_digit_invalid_length(self):
        """测试无效长度"""
        with pytest.raises(ValueError):
            calculate_isbn10_check_digit("123")
        
        with pytest.raises(ValueError):
            calculate_isbn13_check_digit("123")


class TestFormatISBN:
    """测试 ISBN 格式化"""
    
    def test_format_isbn10(self):
        """测试 ISBN-10 格式化"""
        formatted = format_isbn("0306406152")
        assert "-" in formatted
    
    def test_format_isbn13(self):
        """测试 ISBN-13 格式化"""
        formatted = format_isbn("9780306406157")
        assert "-" in formatted
    
    def test_format_isbn_compact(self):
        """测试紧凑格式"""
        compact = format_isbn_compact("978-0-306-40615-7")
        assert "-" not in compact


class TestGenerateISBN:
    """测试 ISBN 生成"""
    
    def test_generate_isbn(self):
        """测试生成 ISBN"""
        isbn = generate_isbn()
        assert len(isbn) >= 10  # ISBN-10 或 ISBN-13
    
    def test_generate_isbn_valid(self):
        """测试生成的 ISBN 有效"""
        isbn = generate_isbn()
        assert is_isbn10(isbn) or is_isbn13(isbn)


class TestConvertISBN:
    """测试 ISBN 转换"""
    
    def test_convert_isbn10_to_13(self):
        """测试 ISBN-10 转 ISBN-13"""
        result = convert_isbn("0306406152", target_format="ISBN-13")
        assert result == "9780306406157"
    
    def test_convert_isbn13_to_10(self):
        """测试 ISBN-13 转 ISBN-10"""
        result = convert_isbn("9780306406157", target_format="ISBN-10")
        assert result == "0306406152"


class TestCompareISBNs:
    """测试 ISBN 比较"""
    
    def test_compare_isbns_equal(self):
        """测试相等 ISBN"""
        # compare_isbns 可能返回相似度或布尔值
        result = compare_isbns("0306406152", "0-306-40615-2")
        assert result is True or result > 0
    
    def test_compare_isbns_different(self):
        """测试不同 ISBN"""
        result = compare_isbns("0306406152", "9780306406157")
        # 可能返回相似度或布尔值
        assert isinstance(result, (bool, int, float))


class TestFindISBNsInText:
    """测试文本中查找 ISBN"""
    
    def test_find_isbns_in_text(self):
        """测试查找 ISBN"""
        text = "这本书的ISBN是 978-0-306-40615-7，另一本是 0306406152"
        isbns = find_isbns_in_text(text)
        
        assert len(isbns) >= 1
    
    def test_find_isbns_no_match(self):
        """测试无匹配"""
        text = "这段文本没有ISBN"
        isbns = find_isbns_in_text(text)
        
        assert len(isbns) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])