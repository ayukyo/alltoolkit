"""
Luhn算法工具测试用例
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from luhn_utils.mod import (
    luhn_checksum,
    calculate_check_digit,
    validate,
    generate_with_check_digit,
    format_card_number,
    mask_card_number,
    identify_card_type,
    validate_card,
    generate_test_card,
    validate_imei,
    generate_imei,
    extract_luhn_info,
)


class TestLuhnChecksum(unittest.TestCase):
    """Luhn校验和测试"""
    
    def test_basic_checksum(self):
        """基础校验和测试"""
        # 4532015112830366 的校验位是 6，校验和应为 0
        self.assertEqual(luhn_checksum("4532015112830366"), 0)
    
    def test_partial_number(self):
        """部分数字校验和测试"""
        # 453201511283036 的校验位应使总和为10的倍数
        check = calculate_check_digit("453201511283036")
        self.assertEqual(check, 6)


class TestCalculateCheckDigit(unittest.TestCase):
    """校验位计算测试"""
    
    def test_visa_check_digit(self):
        """Visa卡校验位"""
        self.assertEqual(calculate_check_digit("453201511283036"), 6)
    
    def test_mastercard_check_digit(self):
        """MasterCard校验位"""
        self.assertEqual(calculate_check_digit("555555555555444"), 4)
    
    def test_amex_check_digit(self):
        """Amex校验位"""
        self.assertEqual(calculate_check_digit("37828224631000"), 5)


class TestValidate(unittest.TestCase):
    """验证功能测试"""
    
    def test_valid_visa(self):
        """有效Visa卡"""
        self.assertTrue(validate("4532015112830366"))
    
    def test_valid_mastercard(self):
        """有效MasterCard"""
        self.assertTrue(validate("5555555555554444"))
    
    def test_valid_amex(self):
        """有效Amex卡"""
        self.assertTrue(validate("378282246310005"))
    
    def test_valid_discover(self):
        """有效Discover卡"""
        self.assertTrue(validate("6011111111111117"))
    
    def test_valid_jcb(self):
        """有效JCB卡"""
        self.assertTrue(validate("3530111333300000"))
    
    def test_invalid_number(self):
        """无效卡号"""
        self.assertFalse(validate("1234567890123456"))
        self.assertFalse(validate("1111111111111111"))  # 多个相同数字通常无效
        self.assertFalse(validate("49927398717"))  # 长度不对
    
    def test_with_formatting(self):
        """带格式化的卡号"""
        self.assertTrue(validate("4532-0151-1283-0366"))
        self.assertTrue(validate("4532 0151 1283 0366"))
    
    def test_too_short(self):
        """过短数字"""
        self.assertFalse(validate("123"))
    
    def test_empty(self):
        """空字符串"""
        self.assertFalse(validate(""))
        self.assertFalse(validate("abc"))


class TestGenerateWithCheckDigit(unittest.TestCase):
    """生成带校验位的号码"""
    
    def test_generate_visa(self):
        """生成Visa格式号码"""
        result = generate_with_check_digit("453201511283036")
        self.assertEqual(result, "4532015112830366")
        self.assertTrue(validate(result))
    
    def test_generate_and_validate(self):
        """生成后验证"""
        for prefix in ["123456", "987654321", "111111111111111"]:
            full = generate_with_check_digit(prefix)
            self.assertTrue(validate(full))


class TestFormatCardNumber(unittest.TestCase):
    """格式化测试"""
    
    def test_format_16_digits(self):
        """16位卡号格式化"""
        self.assertEqual(format_card_number("4532015112830366"), "4532 0151 1283 0366")
    
    def test_format_15_digits(self):
        """15位卡号格式化"""
        self.assertEqual(format_card_number("378282246310005"), "3782 8224 6310 005")
    
    def test_custom_separator(self):
        """自定义分隔符"""
        self.assertEqual(format_card_number("4532015112830366", "-"), "4532-0151-1283-0366")
    
    def test_with_existing_formatting(self):
        """已有格式化"""
        self.assertEqual(format_card_number("4532-0151-1283-0366"), "4532 0151 1283 0366")


class TestMaskCardNumber(unittest.TestCase):
    """遮蔽测试"""
    
    def test_default_mask(self):
        """默认遮蔽"""
        result = mask_card_number("4532015112830366")
        self.assertEqual(result, "4532********0366")
    
    def test_custom_show_digits(self):
        """自定义显示位数"""
        result = mask_card_number("4532015112830366", show_first=6, show_last=4)
        self.assertEqual(result, "453201******0366")
    
    def test_custom_mask_char(self):
        """自定义遮蔽字符"""
        result = mask_card_number("4532015112830366", mask_char="X")
        self.assertEqual(result, "4532XXXXXXXX0366")
    
    def test_short_number(self):
        """短号码"""
        result = mask_card_number("123456")
        self.assertEqual(result, "123456")


class TestIdentifyCardType(unittest.TestCase):
    """卡类型识别测试"""
    
    def test_visa(self):
        """Visa识别"""
        self.assertEqual(identify_card_type("4532015112830366"), "Visa")
    
    def test_mastercard(self):
        """MasterCard识别"""
        self.assertEqual(identify_card_type("5555555555554444"), "MasterCard")
    
    def test_amex(self):
        """Amex识别"""
        self.assertEqual(identify_card_type("378282246310005"), "American Express")
    
    def test_discover(self):
        """Discover识别"""
        self.assertEqual(identify_card_type("6011111111111117"), "Discover")
    
    def test_unknown(self):
        """未知类型"""
        self.assertIsNone(identify_card_type("1234567890123456"))


class TestValidateCard(unittest.TestCase):
    """综合验证测试"""
    
    def test_valid_card_info(self):
        """有效卡信息"""
        is_valid, card_type, formatted = validate_card("4532015112830366")
        self.assertTrue(is_valid)
        self.assertEqual(card_type, "Visa")
        self.assertEqual(formatted, "4532 0151 1283 0366")
    
    def test_invalid_card_info(self):
        """无效卡信息"""
        is_valid, card_type, formatted = validate_card("1234567890123456")
        self.assertFalse(is_valid)
        self.assertIsNone(card_type)


class TestGenerateTestCard(unittest.TestCase):
    """测试卡号生成"""
    
    def test_visa_generation(self):
        """Visa测试卡生成"""
        card = generate_test_card("Visa")
        self.assertTrue(validate(card))
        self.assertEqual(identify_card_type(card), "Visa")
    
    def test_mastercard_generation(self):
        """MasterCard测试卡生成"""
        card = generate_test_card("MasterCard")
        self.assertTrue(validate(card))
        self.assertEqual(identify_card_type(card), "MasterCard")
    
    def test_amex_generation(self):
        """Amex测试卡生成"""
        card = generate_test_card("American Express")
        self.assertTrue(validate(card))


class TestIMEI(unittest.TestCase):
    """IMEI测试"""
    
    def test_valid_imei(self):
        """有效IMEI"""
        self.assertTrue(validate_imei("490154203237518"))
    
    def test_invalid_imei(self):
        """无效IMEI"""
        self.assertFalse(validate_imei("123456789012345"))
    
    def test_wrong_length(self):
        """错误长度"""
        self.assertFalse(validate_imei("12345678901234"))
        self.assertFalse(validate_imei("1234567890123456"))
    
    def test_generate_imei(self):
        """生成IMEI"""
        imei = generate_imei()
        self.assertEqual(len(imei), 15)
        self.assertTrue(validate_imei(imei))
    
    def test_generate_with_custom_values(self):
        """自定义参数生成"""
        imei = generate_imei(tac="12345678", serial="654321")
        self.assertEqual(len(imei), 15)
        self.assertTrue(validate_imei(imei))


class TestExtractLuhnInfo(unittest.TestCase):
    """信息提取测试"""
    
    def test_full_info(self):
        """完整信息"""
        info = extract_luhn_info("4532015112830366")
        self.assertTrue(info["valid"])
        self.assertEqual(info["length"], 16)
        self.assertEqual(info["check_digit"], 6)
        self.assertEqual(info["calculated_check_digit"], 6)
        self.assertTrue(info["check_digit_correct"])
        self.assertEqual(info["card_type"], "Visa")
    
    def test_invalid_info(self):
        """无效卡信息"""
        info = extract_luhn_info("1234567890123456")
        self.assertFalse(info["valid"])
        self.assertIsNone(info["card_type"])
    
    def test_empty_input(self):
        """空输入"""
        info = extract_luhn_info("")
        self.assertFalse(info["valid"])
        self.assertIn("error", info)


if __name__ == "__main__":
    unittest.main(verbosity=2)