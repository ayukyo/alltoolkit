"""
Mask Utilities 单元测试

测试所有掩码函数的正确性。
"""

import unittest
from mask_utils import (
    mask_email, mask_phone, mask_id_card, mask_bank_card,
    mask_credit_card, mask_name, mask_address, mask_ip,
    mask_password, mask_url, mask_custom, detect_and_mask, batch_mask
)


class TestMaskEmail(unittest.TestCase):
    """邮箱掩码测试"""
    
    def test_normal_email(self):
        self.assertEqual(mask_email("user@example.com"), "us**@*******.com")
        self.assertEqual(mask_email("admin@company.co.uk"), "ad***@**********.uk")
        # Test with more visible domain parts
        self.assertEqual(mask_email("admin@company.co.uk", visible_domain=2), "ad***@*******.co.uk")
    
    def test_short_username(self):
        self.assertEqual(mask_email("a@b.com"), "a@*.com")
        self.assertEqual(mask_email("ab@test.org"), "a*@****.org")
    
    def test_empty_email(self):
        self.assertEqual(mask_email(""), "")
        self.assertEqual(mask_email(None), None)
    
    def test_invalid_email(self):
        self.assertEqual(mask_email("notanemail"), "notanemail")


class TestMaskPhone(unittest.TestCase):
    """手机号掩码测试"""
    
    def test_normal_phone(self):
        self.assertEqual(mask_phone("13812345678"), "138****5678")
    
    def test_phone_with_country_code(self):
        result = mask_phone("+86 13812345678")
        self.assertIn("****", result)
    
    def test_phone_with_formatting(self):
        result = mask_phone("138-1234-5678")
        self.assertIn("****", result)
    
    def test_short_phone(self):
        self.assertEqual(mask_phone("123"), "123")


class TestMaskIdCard(unittest.TestCase):
    """身份证掩码测试"""
    
    def test_18_digit_id(self):
        result = mask_id_card("110101199001011234")
        self.assertTrue(result.startswith("11"))
        self.assertTrue(result.endswith("34"))
        self.assertIn("*", result)
    
    def test_15_digit_id(self):
        result = mask_id_card("110101900101123")
        self.assertIn("*", result)
    
    def test_empty_id(self):
        self.assertEqual(mask_id_card(""), "")
    
    def test_id_with_spaces(self):
        result = mask_id_card("110101 19900101 1234")
        self.assertIn("*", result)


class TestMaskBankCard(unittest.TestCase):
    """银行卡掩码测试"""
    
    def test_16_digit_card(self):
        result = mask_bank_card("6222021234567890")
        self.assertEqual(result, "6222********7890")
    
    def test_19_digit_card(self):
        result = mask_bank_card("6222021234567890123")
        self.assertEqual(result, "6222***********0123")
    
    def test_card_with_spaces(self):
        result = mask_bank_card("6222 0212 3456 7890")
        self.assertIn("*", result)


class TestMaskCreditCard(unittest.TestCase):
    """信用卡掩码测试"""
    
    def test_visa_card(self):
        result = mask_credit_card("4532015112830366")
        self.assertEqual(result, "****-****-****-0366")
    
    def test_mastercard(self):
        result = mask_credit_card("5425233430109903")
        self.assertEqual(result, "****-****-****-9903")
    
    def test_short_card(self):
        self.assertEqual(mask_credit_card("12345"), "12345")


class TestMaskName(unittest.TestCase):
    """姓名掩码测试"""
    
    def test_chinese_short_name(self):
        self.assertEqual(mask_name("张三"), "张*")
    
    def test_chinese_long_name(self):
        self.assertEqual(mask_name("王小明"), "王**")
        self.assertEqual(mask_name("欧阳修远"), "欧***")
    
    def test_english_name(self):
        self.assertEqual(mask_name("John"), "J***")
        self.assertEqual(mask_name("John Smith"), "J*** S****")
    
    def test_empty_name(self):
        self.assertEqual(mask_name(""), "")


class TestMaskAddress(unittest.TestCase):
    """地址掩码测试"""
    
    def test_long_address(self):
        address = "北京市朝阳区建国路88号SOHO现代城A座1001"
        result = mask_address(address)
        self.assertTrue(result.startswith("北京市朝阳区建国路"))
        self.assertIn("1001", result)
        self.assertIn("*", result)
    
    def test_short_address(self):
        self.assertEqual(mask_address("北京"), "北京")


class TestMaskIP(unittest.TestCase):
    """IP 地址掩码测试"""
    
    def test_ipv4(self):
        result = mask_ip("192.168.1.100")
        self.assertEqual(result, "192.168.*.*")
    
    def test_ipv4_mask_1_octet(self):
        result = mask_ip("192.168.1.100", mask_octets=1)
        self.assertEqual(result, "192.168.1.*")
    
    def test_ipv6(self):
        result = mask_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        parts = result.split(":")
        self.assertTrue(parts[0] == "2001")
        self.assertTrue("*" in result)


class TestMaskPassword(unittest.TestCase):
    """密码掩码测试"""
    
    def test_password_with_length(self):
        result = mask_password("MySecret123!")
        self.assertEqual(result, "************ (12 chars)")
    
    def test_password_without_length(self):
        result = mask_password("MySecret123!", show_length=False)
        self.assertEqual(result, "************")
    
    def test_empty_password(self):
        self.assertEqual(mask_password(""), "")


class TestMaskURL(unittest.TestCase):
    """URL 掩码测试"""
    
    def test_url_with_token(self):
        result = mask_url("https://api.example.com/data?token=secret123")
        self.assertIn("token=***", result)
        self.assertNotIn("secret123", result)
    
    def test_url_with_multiple_params(self):
        result = mask_url("https://api.example.com/users?key=abc123&name=test")
        self.assertIn("key=***", result)
        self.assertIn("name=test", result)
    
    def test_url_without_sensitive_params(self):
        result = mask_url("https://example.com/page?id=123&name=test")
        self.assertIn("id=123", result)
        self.assertIn("name=test", result)


class TestMaskCustom(unittest.TestCase):
    """自定义掩码测试"""
    
    def test_custom_pattern(self):
        text = "订单号: ABC123456XYZ"
        result = mask_custom(text, r'[A-Z]{3}\d{6}[A-Z]{3}')
        self.assertEqual(result, "订单号: ************")
    
    def test_multiple_matches(self):
        text = "ID: AAA111BBB, Code: XXX999YYY"
        result = mask_custom(text, r'[A-Z]{3}\d{3}[A-Z]{3}')
        self.assertIn("*", result)


class TestDetectAndMask(unittest.TestCase):
    """自动检测掩码测试"""
    
    def test_detect_email(self):
        text = "联系邮箱: user@example.com"
        result, types = detect_and_mask(text)
        self.assertIn("email", types)
        self.assertNotIn("user@example.com", result)
    
    def test_detect_phone(self):
        text = "手机号: 13812345678"
        result, types = detect_and_mask(text)
        self.assertIn("phone", types)
        self.assertIn("****", result)
    
    def test_detect_multiple(self):
        text = "邮箱: test@example.com，手机: 13812345678"
        result, types = detect_and_mask(text)
        self.assertIn("email", types)
        self.assertIn("phone", types)
    
    def test_detect_nothing(self):
        text = "这是一段普通文本"
        result, types = detect_and_mask(text)
        self.assertEqual(types, [])


class TestBatchMask(unittest.TestCase):
    """批量掩码测试"""
    
    def test_batch_mask(self):
        data = {
            "email": "user@example.com",
            "phone": "13812345678",
            "name": "张三"
        }
        rules = {
            "email": "email",
            "phone": "phone",
            "name": "name"
        }
        result = batch_mask(data, rules)
        self.assertIn("*", result["email"])
        self.assertIn("****", result["phone"])
        self.assertEqual(result["name"], "张*")
    
    def test_batch_mask_partial_rules(self):
        data = {
            "email": "user@example.com",
            "username": "testuser"
        }
        rules = {"email": "email"}
        result = batch_mask(data, rules)
        self.assertIn("*", result["email"])
        self.assertEqual(result["username"], "testuser")


if __name__ == "__main__":
    unittest.main(verbosity=2)