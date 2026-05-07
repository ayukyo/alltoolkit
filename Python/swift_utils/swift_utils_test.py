"""
SWIFT/BIC Utilities 测试模块

Author: AllToolkit
Version: 1.0.0
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SwiftUtils, BicUtils, SwiftCodeType, SwiftNetworkStatus,
    validate_swift, validate_bic, parse_swift, parse_bic,
    get_swift_bank_code, get_swift_country, is_swift_primary, format_swift
)


class TestSwiftValidation(unittest.TestCase):
    """SWIFT代码验证测试"""

    def test_validate_valid_8_char(self):
        """测试有效的8位SWIFT代码"""
        self.assertTrue(SwiftUtils.validate("BKCHCNBJ"))
        self.assertTrue(SwiftUtils.validate("DEUTDEFF"))
        self.assertTrue(SwiftUtils.validate("HSBCGB2L"))

    def test_validate_valid_11_char(self):
        """测试有效的11位SWIFT代码"""
        self.assertTrue(SwiftUtils.validate("BKCHCNBJXXX"))
        self.assertTrue(SwiftUtils.validate("DEUTDEFF500"))
        self.assertTrue(SwiftUtils.validate("HSBCGB2L00A"))

    def test_validate_lowercase(self):
        """测试小写输入"""
        self.assertTrue(SwiftUtils.validate("bkchcnbj"))
        self.assertTrue(SwiftUtils.validate("DEUTdeff"))

    def test_validate_with_spaces(self):
        """测试带空格的输入"""
        self.assertTrue(SwiftUtils.validate("BKCH CNBJ"))
        self.assertTrue(SwiftUtils.validate(" BKCHCNBJ "))
        self.assertTrue(SwiftUtils.validate("BKCH CN BJ XXX"))

    def test_validate_invalid_length(self):
        """测试无效长度"""
        self.assertFalse(SwiftUtils.validate(""))
        self.assertFalse(SwiftUtils.validate("BKCH"))
        self.assertFalse(SwiftUtils.validate("BKCHCNB"))
        self.assertFalse(SwiftUtils.validate("BKCHCNBJX"))
        self.assertFalse(SwiftUtils.validate("BKCHCNBJXXXXX"))

    def test_validate_invalid_country(self):
        """测试无效国家代码"""
        self.assertFalse(SwiftUtils.validate("BKCHXXBJ"))  # XX不是有效国家代码
        self.assertFalse(SwiftUtils.validate("DEUTAABB"))  # AA不是有效国家代码

    def test_validate_invalid_format(self):
        """测试无效格式"""
        self.assertFalse(SwiftUtils.validate("1234CNBJ"))  # 银行代码应为字母
        # 测试银行代码含数字
        self.assertFalse(SwiftUtils.validate("BK1HCNBJ"))

    def test_validate_none(self):
        """测试空输入"""
        self.assertFalse(SwiftUtils.validate(None))
        self.assertFalse(SwiftUtils.validate(""))


class TestSwiftStrictValidation(unittest.TestCase):
    """严格验证测试"""

    def test_strict_valid(self):
        """测试严格验证有效代码"""
        valid, errors = SwiftUtils.validate_strict("BKCHCNBJ")
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_strict_invalid_length(self):
        """测试严格验证无效长度"""
        valid, errors = SwiftUtils.validate_strict("BKCH")
        self.assertFalse(valid)
        self.assertIn("8位", errors[0] if errors else "")

    def test_strict_invalid_bank_code(self):
        """测试严格验证无效银行代码"""
        valid, errors = SwiftUtils.validate_strict("1234CNBJXXX")
        self.assertFalse(valid)
        self.assertTrue(any("银行代码" in e for e in errors))

    def test_strict_invalid_country(self):
        """测试严格验证无效国家代码"""
        valid, errors = SwiftUtils.validate_strict("BKCHXXBJ")
        self.assertFalse(valid)
        self.assertTrue(any("国家代码" in e for e in errors))

    def test_strict_empty(self):
        """测试严格验证空输入"""
        valid, errors = SwiftUtils.validate_strict("")
        self.assertFalse(valid)
        self.assertTrue(len(errors) > 0)


class TestSwiftParsing(unittest.TestCase):
    """SWIFT代码解析测试"""

    def test_parse_8_char(self):
        """测试解析8位SWIFT代码"""
        result = SwiftUtils.parse("BKCHCNBJ")
        self.assertEqual(result["swift_code"], "BKCHCNBJ")
        self.assertEqual(result["bank_code"], "BKCH")
        self.assertEqual(result["country_code"], "CN")
        self.assertEqual(result["location_code"], "BJ")
        self.assertIsNone(result["branch_code"])
        self.assertEqual(result["country_name"], "中国")
        self.assertEqual(result["length"], 8)
        self.assertTrue(result["is_primary"])

    def test_parse_11_char(self):
        """测试解析11位SWIFT代码"""
        result = SwiftUtils.parse("BKCHCNBJXXX")
        self.assertEqual(result["swift_code"], "BKCHCNBJXXX")
        self.assertEqual(result["bank_code"], "BKCH")
        self.assertEqual(result["country_code"], "CN")
        self.assertEqual(result["location_code"], "BJ")
        self.assertEqual(result["branch_code"], "XXX")
        self.assertEqual(result["length"], 11)
        self.assertTrue(result["is_primary"])

    def test_parse_specific_branch(self):
        """测试解析特定分行代码"""
        result = SwiftUtils.parse("BKCHCNBJA01")
        self.assertEqual(result["branch_code"], "A01")
        self.assertFalse(result["is_primary"])

    def test_parse_country_info(self):
        """测试解析国家信息"""
        result = SwiftUtils.parse("HSBCGB2L")
        self.assertEqual(result["country_code"], "GB")
        self.assertEqual(result["country_name"], "英国")
        self.assertEqual(result["country_name_en"], "United Kingdom")
        self.assertEqual(result["country_currency"], "GBP")

    def test_parse_bank_info(self):
        """测试解析银行信息"""
        result = SwiftUtils.parse("BKCHCNBJ")
        self.assertEqual(result["bank_name"], "中国银行")
        self.assertEqual(result["bank_name_en"], "Bank of China")

    def test_parse_lowercase(self):
        """测试解析小写输入"""
        result = SwiftUtils.parse("deutdeff")
        self.assertEqual(result["swift_code"], "DEUTDEFF")
        self.assertEqual(result["bank_code"], "DEUT")

    def test_parse_invalid(self):
        """测试解析无效代码"""
        with self.assertRaises(ValueError):
            SwiftUtils.parse("INVALID")
        with self.assertRaises(ValueError):
            SwiftUtils.parse("BKCHXXBJ")


class TestSwiftExtraction(unittest.TestCase):
    """提取功能测试"""

    def test_get_bank_code(self):
        """测试提取银行代码"""
        self.assertEqual(SwiftUtils.get_bank_code("BKCHCNBJ"), "BKCH")
        self.assertEqual(SwiftUtils.get_bank_code("BKCHCNBJXXX"), "BKCH")
        self.assertEqual(SwiftUtils.get_bank_code("bkchcnbj"), "BKCH")

    def test_get_country_code(self):
        """测试提取国家代码"""
        self.assertEqual(SwiftUtils.get_country_code("BKCHCNBJ"), "CN")
        self.assertEqual(SwiftUtils.get_country_code("DEUTDEFF"), "DE")
        self.assertEqual(SwiftUtils.get_country_code("HSBCGB2L"), "GB")

    def test_get_location_code(self):
        """测试提取地区代码"""
        self.assertEqual(SwiftUtils.get_location_code("BKCHCNBJ"), "BJ")
        self.assertEqual(SwiftUtils.get_location_code("DEUTDEFF"), "FF")
        self.assertEqual(SwiftUtils.get_location_code("HSBCGB2L"), "2L")

    def test_get_branch_code(self):
        """测试提取分行代码"""
        self.assertIsNone(SwiftUtils.get_branch_code("BKCHCNBJ"))
        self.assertEqual(SwiftUtils.get_branch_code("BKCHCNBJXXX"), "XXX")
        self.assertEqual(SwiftUtils.get_branch_code("BKCHCNBJA01"), "A01")


class TestSwiftGeneration(unittest.TestCase):
    """生成功能测试"""

    def test_generate_primary(self):
        """测试生成主要办公机构代码"""
        swift = SwiftUtils.generate_primary("BKCH", "CN", "BJ")
        self.assertEqual(swift, "BKCHCNBJ")

    def test_generate_branch(self):
        """测试生成分行代码"""
        swift = SwiftUtils.generate_branch("BKCH", "CN", "BJ", "XXX")
        self.assertEqual(swift, "BKCHCNBJXXX")

        swift2 = SwiftUtils.generate_branch("DEUT", "DE", "FF", "500")
        self.assertEqual(swift2, "DEUTDEFF500")

    def test_generate_invalid_bank_code(self):
        """测试无效银行代码"""
        with self.assertRaises(ValueError):
            SwiftUtils.generate_primary("1234", "CN", "BJ")
        with self.assertRaises(ValueError):
            SwiftUtils.generate_primary("BKC", "CN", "BJ")  # 不足4位

    def test_generate_invalid_country_code(self):
        """测试无效国家代码"""
        with self.assertRaises(ValueError):
            SwiftUtils.generate_primary("BKCH", "XX", "BJ")
        with self.assertRaises(ValueError):
            SwiftUtils.generate_primary("BKCH", "C", "BJ")  # 不足2位

    def test_generate_invalid_location_code(self):
        """测试无效地区代码"""
        with self.assertRaises(ValueError):
            SwiftUtils.generate_primary("BKCH", "CN", "B")  # 不足2位

    def test_generate_invalid_branch_code(self):
        """测试无效分行代码"""
        with self.assertRaises(ValueError):
            SwiftUtils.generate_branch("BKCH", "CN", "BJ", "XX")
        with self.assertRaises(ValueError):
            SwiftUtils.generate_branch("BKCH", "CN", "BJ", "XXX1")


class TestSwiftPrimaryOffice(unittest.TestCase):
    """主要办公机构判断测试"""

    def test_is_primary_8_char(self):
        """测试8位代码是主要办公机构"""
        self.assertTrue(SwiftUtils.is_primary_office("BKCHCNBJ"))
        self.assertTrue(SwiftUtils.is_primary_office("DEUTDEFF"))

    def test_is_primary_11_char_xxx(self):
        """测试11位代码XXX是主要办公机构"""
        self.assertTrue(SwiftUtils.is_primary_office("BKCHCNBJXXX"))
        self.assertTrue(SwiftUtils.is_primary_office("DEUTDEFFXXX"))

    def test_is_primary_11_char_specific(self):
        """测试11位代码特定分行不是主要办公机构"""
        self.assertFalse(SwiftUtils.is_primary_office("BKCHCNBJA01"))
        self.assertFalse(SwiftUtils.is_primary_office("DEUTDEFF500"))

    def test_get_primary_code(self):
        """测试获取主要办公机构代码"""
        self.assertEqual(SwiftUtils.get_primary_code("BKCHCNBJXXX"), "BKCHCNBJ")
        self.assertEqual(SwiftUtils.get_primary_code("BKCHCNBJA01"), "BKCHCNBJ")
        self.assertEqual(SwiftUtils.get_primary_code("BKCHCNBJ"), "BKCHCNBJ")


class TestSwiftComparison(unittest.TestCase):
    """比较功能测试"""

    def test_compare_same_bank(self):
        """测试同银行比较"""
        result = SwiftUtils.compare("BKCHCNBJ", "BKCHCNBJXXX")
        self.assertTrue(result["same_bank"])
        self.assertTrue(result["same_country"])
        self.assertTrue(result["same_location"])
        self.assertTrue(result["same_bank_system"])
        self.assertTrue(result["is_related"])

    def test_compare_different_bank(self):
        """测试不同银行比较"""
        result = SwiftUtils.compare("BKCHCNBJ", "HSBCGB2L")
        self.assertFalse(result["same_bank"])
        self.assertFalse(result["same_country"])
        self.assertFalse(result["same_bank_system"])

    def test_compare_same_country_different_bank(self):
        """测试同国家不同银行"""
        result = SwiftUtils.compare("BKCHCNBJ", "ICBKCNBJ")
        self.assertFalse(result["same_bank"])
        self.assertTrue(result["same_country"])
        self.assertFalse(result["same_bank_system"])


class TestSwiftFormat(unittest.TestCase):
    """格式化测试"""

    def test_format_uppercase(self):
        """测试转换大写"""
        self.assertEqual(SwiftUtils.format("bkchcnbj"), "BKCHCNBJ")
        self.assertEqual(SwiftUtils.format("deutDEFF"), "DEUTDEFF")

    def test_format_remove_spaces(self):
        """测试去除空格"""
        self.assertEqual(SwiftUtils.format("BKCH CNBJ"), "BKCHCNBJ")
        self.assertEqual(SwiftUtils.format(" BKCH CN BJ "), "BKCHCNBJ")

    def test_format_remove_dashes(self):
        """测试去除连字符"""
        self.assertEqual(SwiftUtils.format("BKCH-CNBJ"), "BKCHCNBJ")
        self.assertEqual(SwiftUtils.format("BKCH-CN-BJ-XXX"), "BKCHCNBJXXX")


class TestCountryInfo(unittest.TestCase):
    """国家信息测试"""

    def test_get_country_info(self):
        """测试获取国家信息"""
        info = SwiftUtils.get_country_info("CN")
        self.assertEqual(info["code"], "CN")
        self.assertEqual(info["name"], "中国")
        self.assertEqual(info["name_en"], "China")
        self.assertEqual(info["currency"], "CNY")

    def test_get_country_info_us(self):
        """测试获取美国信息"""
        info = SwiftUtils.get_country_info("US")
        self.assertEqual(info["code"], "US")
        self.assertEqual(info["name"], "美国")
        self.assertEqual(info["currency"], "USD")

    def test_get_country_info_invalid(self):
        """测试无效国家代码"""
        with self.assertRaises(ValueError):
            SwiftUtils.get_country_info("XX")

    def test_get_all_countries(self):
        """测试获取所有国家"""
        countries = SwiftUtils.get_all_countries()
        self.assertTrue(len(countries) > 200)
        # 检查是否包含常见国家
        cn_found = any(c["code"] == "CN" for c in countries)
        us_found = any(c["code"] == "US" for c in countries)
        self.assertTrue(cn_found)
        self.assertTrue(us_found)


class TestBankExamples(unittest.TestCase):
    """银行示例测试"""

    def test_get_all_bank_examples(self):
        """测试获取所有银行示例"""
        examples = SwiftUtils.get_all_bank_examples()
        self.assertTrue(len(examples) > 0)
        self.assertIn("BKCH", examples)
        self.assertIn("HSBC", examples)

    def test_search_by_country(self):
        """测试按国家搜索银行"""
        cn_banks = SwiftUtils.search_by_country("CN")
        self.assertTrue(len(cn_banks) > 0)
        bank_codes = [b["bank_code"] for b in cn_banks]
        self.assertIn("BKCH", bank_codes)
        self.assertIn("ICBK", bank_codes)

    def test_search_by_country_us(self):
        """测试搜索美国银行"""
        us_banks = SwiftUtils.search_by_country("US")
        self.assertTrue(len(us_banks) > 0)
        bank_codes = [b["bank_code"] for b in us_banks]
        self.assertIn("CITI", bank_codes)
        self.assertIn("BOFA", bank_codes)


class TestBicUtils(unittest.TestCase):
    """BIC工具类测试（别名测试）"""

    def test_bic_validate(self):
        """测试BIC验证"""
        self.assertTrue(BicUtils.validate("BKCHCNBJ"))
        self.assertFalse(BicUtils.validate("INVALID"))

    def test_bic_parse(self):
        """测试BIC解析"""
        result = BicUtils.parse("BKCHCNBJ")
        self.assertEqual(result["bank_code"], "BKCH")
        self.assertEqual(result["country_code"], "CN")

    def test_bic_extract(self):
        """测试BIC提取"""
        self.assertEqual(BicUtils.get_bank_code("BKCHCNBJ"), "BKCH")
        self.assertEqual(BicUtils.get_country_code("BKCHCNBJ"), "CN")
        self.assertEqual(BicUtils.get_location_code("BKCHCNBJ"), "BJ")
        self.assertIsNone(BicUtils.get_branch_code("BKCHCNBJ"))


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""

    def test_validate_swift(self):
        """测试validate_swift函数"""
        self.assertTrue(validate_swift("BKCHCNBJ"))
        self.assertFalse(validate_swift("INVALID"))

    def test_validate_bic(self):
        """测试validate_bic函数"""
        self.assertTrue(validate_bic("BKCHCNBJ"))

    def test_parse_swift(self):
        """测试parse_swift函数"""
        result = parse_swift("BKCHCNBJ")
        self.assertEqual(result["bank_code"], "BKCH")

    def test_parse_bic(self):
        """测试parse_bic函数"""
        result = parse_bic("BKCHCNBJ")
        self.assertEqual(result["country_code"], "CN")

    def test_get_swift_bank_code(self):
        """测试get_swift_bank_code函数"""
        self.assertEqual(get_swift_bank_code("BKCHCNBJ"), "BKCH")

    def test_get_swift_country(self):
        """测试get_swift_country函数"""
        self.assertEqual(get_swift_country("BKCHCNBJ"), "CN")

    def test_is_swift_primary(self):
        """测试is_swift_primary函数"""
        self.assertTrue(is_swift_primary("BKCHCNBJ"))
        self.assertFalse(is_swift_primary("BKCHCNBJA01"))

    def test_format_swift(self):
        """测试format_swift函数"""
        self.assertEqual(format_swift("bkch cnbj"), "BKCHCNBJ")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_numeric_location_code(self):
        """测试数字地区代码"""
        self.assertTrue(SwiftUtils.validate("HSBCGB22"))
        self.assertTrue(SwiftUtils.validate("CITIUS00"))

    def test_mixed_location_code(self):
        """测试字母数字混合地区代码"""
        self.assertTrue(SwiftUtils.validate("HSBCGB2L"))
        self.assertTrue(SwiftUtils.validate("DEUTDEFF"))

    def test_numeric_branch_code(self):
        """测试数字分行代码"""
        self.assertTrue(SwiftUtils.validate("DEUTDEFF500"))
        result = SwiftUtils.parse("DEUTDEFF500")
        self.assertEqual(result["branch_code"], "500")

    def test_all_numeric_branch(self):
        """测试全数字分行代码"""
        self.assertTrue(SwiftUtils.validate("BKCHCNBJ001"))
        result = SwiftUtils.parse("BKCHCNBJ001")
        self.assertEqual(result["branch_code"], "001")
        self.assertFalse(result["is_primary"])

    def test_country_with_no_currency(self):
        """测试无货币国家"""
        # AQ (Antarctica) 没有货币
        info = SwiftUtils.get_country_info("AQ")
        self.assertEqual(info["currency"], "")

    def test_unknown_bank(self):
        """测试未知银行代码"""
        result = SwiftUtils.parse("XXXXCNBJ")
        self.assertEqual(result["bank_name"], "未知银行")
        self.assertEqual(result["bank_name_en"], "Unknown Bank")


class TestNetworkStatus(unittest.TestCase):
    """网络状态解析测试"""

    def test_active_status(self):
        """测试活跃状态"""
        result = SwiftUtils.parse("BKCHCNBJ")  # BJ以B开头（字母）
        self.assertEqual(result["network_status"], "活跃")

    def test_numeric_status(self):
        """测试数字状态"""
        # 使用模拟的SWIFT代码测试
        swift = SwiftUtils.generate_primary("BKCH", "CN", "1J")
        result = SwiftUtils.parse(swift)
        self.assertEqual(result["network_status"], "活跃")


if __name__ == "__main__":
    unittest.main()