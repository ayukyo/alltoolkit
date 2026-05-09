"""
Postal Code Utilities - 测试文件

测试所有邮政编码验证、格式化、提取等功能。
零外部依赖，仅使用 Python 标准库。

作者: AllToolkit
日期: 2026-05-09
"""

import sys
import os
import unittest
from typing import List

# 添加路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    validate_postal_code,
    format_postal_code,
    normalize_postal_code,
    get_postal_code_info,
    extract_postal_codes,
    detect_country,
    is_valid_postal_code_format,
    get_country_postal_code_info,
    compare_postal_codes,
    get_nearby_postal_codes,
    batch_validate,
    generate_random_postal_code,
    get_supported_countries,
    PostalCodeInfo,
    POSTAL_CODE_RULES,
)


class TestValidatePostalCode(unittest.TestCase):
    """测试邮政编码验证"""
    
    def test_validate_cn_codes(self):
        """测试中国邮编验证"""
        # 有效邮编
        self.assertTrue(validate_postal_code("100001", "CN"))
        self.assertTrue(validate_postal_code("200001", "CN"))
        self.assertTrue(validate_postal_code("510000", "CN"))
        self.assertTrue(validate_postal_code("999999", "CN"))
        
        # 无效邮编
        self.assertFalse(validate_postal_code("10000", "CN"))  # 5位
        self.assertFalse(validate_postal_code("1000001", "CN"))  # 7位
        self.assertFalse(validate_postal_code("abc123", "CN"))  # 包含字母
        self.assertFalse(validate_postal_code("", "CN"))  # 空
        self.assertFalse(validate_postal_code("100001", ""))  # 空国家
    
    def test_validate_us_codes(self):
        """测试美国ZIP码验证"""
        # ZIP格式
        self.assertTrue(validate_postal_code("12345", "US"))
        self.assertTrue(validate_postal_code("90210", "US"))
        self.assertTrue(validate_postal_code("00000", "US"))
        self.assertTrue(validate_postal_code("99999", "US"))
        
        # ZIP+4格式
        self.assertTrue(validate_postal_code("12345-6789", "US"))
        self.assertTrue(validate_postal_code("90210-1234", "US"))
        self.assertTrue(validate_postal_code("00000-0000", "US"))
        
        # 紧凑格式
        self.assertTrue(validate_postal_code("123456789", "US"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("1234", "US"))  # 4位
        self.assertFalse(validate_postal_code("123456", "US"))  # 6位（无连字符）
        self.assertFalse(validate_postal_code("abcde", "US"))  # 字母
        self.assertFalse(validate_postal_code("12345-abc", "US"))  # ZIP+4后4位非数字
    
    def test_validate_jp_codes(self):
        """测试日本邮编验证"""
        # 标准格式
        self.assertTrue(validate_postal_code("100-0001", "JP"))
        self.assertTrue(validate_postal_code("150-0001", "JP"))
        
        # 带〒符号
        self.assertTrue(validate_postal_code("〒100-0001", "JP"))
        self.assertTrue(validate_postal_code("〒150-0001", "JP"))
        
        # 紧凑格式
        self.assertTrue(validate_postal_code("1000001", "JP"))
        self.assertTrue(validate_postal_code("1500001", "JP"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("100001", "JP"))  # 6位
        self.assertFalse(validate_postal_code("abc-1234", "JP"))  # 字母
        self.assertFalse(validate_postal_code("100", "JP"))  # 太短
    
    def test_validate_uk_codes(self):
        """测试英国邮编验证"""
        # 各种有效格式
        self.assertTrue(validate_postal_code("SW1A 1AA", "UK"))
        self.assertTrue(validate_postal_code("M1 1AA", "UK"))
        self.assertTrue(validate_postal_code("B33 8TH", "UK"))
        self.assertTrue(validate_postal_code("CR2 6XH", "UK"))
        self.assertTrue(validate_postal_code("DN55 1PT", "UK"))
        self.assertTrue(validate_postal_code("W1A 1HQ", "UK"))
        self.assertTrue(validate_postal_code("EC1A 1BB", "UK"))
        
        # 无空格格式
        self.assertTrue(validate_postal_code("SW1A1AA", "UK"))
        self.assertTrue(validate_postal_code("M11AA", "UK"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("12345", "UK"))  # 纯数字
        self.assertFalse(validate_postal_code("AAAA", "UK"))  # 纯字母
        self.assertFalse(validate_postal_code("", "UK"))  # 空
    
    def test_validate_ca_codes(self):
        """测试加拿大邮编验证"""
        # 有效格式
        self.assertTrue(validate_postal_code("K1A 0B1", "CA"))
        self.assertTrue(validate_postal_code("V6B 1A1", "CA"))
        self.assertTrue(validate_postal_code("T2P 1J9", "CA"))
        self.assertTrue(validate_postal_code("M5V 3L9", "CA"))
        
        # 无空格格式
        self.assertTrue(validate_postal_code("K1A0B1", "CA"))
        self.assertTrue(validate_postal_code("V6B1A1", "CA"))
        
        # 小写格式
        self.assertTrue(validate_postal_code("k1a 0b1", "CA"))
        self.assertTrue(validate_postal_code("k1a0b1", "CA"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("12345", "CA"))  # 纯数字
        self.assertFalse(validate_postal_code("AAAAAA", "CA"))  # 纯字母
        self.assertFalse(validate_postal_code("K1A 0B", "CA"))  # 太短
        self.assertFalse(validate_postal_code("W1A 0B1", "CA"))  # W不允许在第一位
    
    def test_validate_au_codes(self):
        """测试澳大利亚邮编验证"""
        self.assertTrue(validate_postal_code("2000", "AU"))
        self.assertTrue(validate_postal_code("3000", "AU"))
        self.assertTrue(validate_postal_code("4000", "AU"))
        self.assertTrue(validate_postal_code("0000", "AU"))
        self.assertTrue(validate_postal_code("9999", "AU"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("20000", "AU"))  # 5位
        self.assertFalse(validate_postal_code("abc", "AU"))  # 字母
    
    def test_validate_de_codes(self):
        """测试德国邮编验证"""
        self.assertTrue(validate_postal_code("10115", "DE"))
        self.assertTrue(validate_postal_code("80331", "DE"))
        self.assertTrue(validate_postal_code("50667", "DE"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("1011", "DE"))  # 4位
        self.assertFalse(validate_postal_code("101155", "DE"))  # 6位
    
    def test_validate_fr_codes(self):
        """测试法国邮编验证"""
        self.assertTrue(validate_postal_code("75001", "FR"))
        self.assertTrue(validate_postal_code("13001", "FR"))
        self.assertTrue(validate_postal_code("69001", "FR"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("7500", "FR"))  # 4位
        self.assertFalse(validate_postal_code("750001", "FR"))  # 6位
    
    def test_validate_kr_codes(self):
        """测试韩国邮编验证"""
        self.assertTrue(validate_postal_code("04524", "KR"))
        self.assertTrue(validate_postal_code("06000", "KR"))
        
        # 旧格式
        self.assertTrue(validate_postal_code("100-101", "KR"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("0452", "KR"))  # 4位
        self.assertFalse(validate_postal_code("045245", "KR"))  # 6位
    
    def test_validate_in_codes(self):
        """测试印度PIN码验证"""
        self.assertTrue(validate_postal_code("110001", "IN"))
        self.assertTrue(validate_postal_code("400001", "IN"))
        self.assertTrue(validate_postal_code("700001", "IN"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("11000", "IN"))  # 5位
        self.assertFalse(validate_postal_code("1100001", "IN"))  # 7位
    
    def test_validate_br_codes(self):
        """测试巴西CEP码验证"""
        self.assertTrue(validate_postal_code("01311-000", "BR"))
        self.assertTrue(validate_postal_code("22041-080", "BR"))
        
        # 紧凑格式
        self.assertTrue(validate_postal_code("01311000", "BR"))
        self.assertTrue(validate_postal_code("22041080", "BR"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("01311", "BR"))  # 5位
        self.assertFalse(validate_postal_code("013110001", "BR"))  # 9位
    
    def test_validate_ru_codes(self):
        """测试俄罗斯邮编验证"""
        self.assertTrue(validate_postal_code("101000", "RU"))
        self.assertTrue(validate_postal_code("190000", "RU"))
        self.assertTrue(validate_postal_code("620000", "RU"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("10100", "RU"))  # 5位
        self.assertFalse(validate_postal_code("1010000", "RU"))  # 7位
    
    def test_validate_mx_codes(self):
        """测试墨西哥邮编验证"""
        self.assertTrue(validate_postal_code("06600", "MX"))
        self.assertTrue(validate_postal_code("11560", "MX"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("0660", "MX"))  # 4位
        self.assertFalse(validate_postal_code("066000", "MX"))  # 6位
    
    def test_validate_it_codes(self):
        """测试意大利CAP码验证"""
        self.assertTrue(validate_postal_code("00100", "IT"))
        self.assertTrue(validate_postal_code("20100", "IT"))
        self.assertTrue(validate_postal_code("50100", "IT"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("0010", "IT"))  # 4位
        self.assertFalse(validate_postal_code("001000", "IT"))  # 6位
    
    def test_validate_es_codes(self):
        """测试西班牙邮编验证"""
        self.assertTrue(validate_postal_code("28001", "ES"))
        self.assertTrue(validate_postal_code("08001", "ES"))
        self.assertTrue(validate_postal_code("46001", "ES"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("2800", "ES"))  # 4位
        self.assertFalse(validate_postal_code("280001", "ES"))  # 6位
    
    def test_validate_nl_codes(self):
        """测试荷兰邮编验证"""
        self.assertTrue(validate_postal_code("1011 AB", "NL"))
        self.assertTrue(validate_postal_code("1071 CD", "NL"))
        
        # 紧凑格式
        self.assertTrue(validate_postal_code("1011AB", "NL"))
        self.assertTrue(validate_postal_code("1071CD", "NL"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("1011", "NL"))  # 无字母
        self.assertFalse(validate_postal_code("10111AB", "NL"))  # 5位数字
    
    def test_validate_se_codes(self):
        """测试瑞典邮编验证"""
        self.assertTrue(validate_postal_code("111 22", "SE"))
        self.assertTrue(validate_postal_code("123 45", "SE"))
        
        # 紧凑格式
        self.assertTrue(validate_postal_code("11122", "SE"))
        self.assertTrue(validate_postal_code("12345", "SE"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("1112", "SE"))  # 4位
        self.assertFalse(validate_postal_code("111222", "SE"))  # 6位
    
    def test_validate_pl_codes(self):
        """测试波兰邮编验证"""
        self.assertTrue(validate_postal_code("00-001", "PL"))
        self.assertTrue(validate_postal_code("30-001", "PL"))
        self.assertTrue(validate_postal_code("50-001", "PL"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("00001", "PL"))  # 无连字符
        self.assertFalse(validate_postal_code("00-0001", "PL"))  # 6位
    
    def test_validate_tw_codes(self):
        """测试台湾邮编验证"""
        # 3位格式
        self.assertTrue(validate_postal_code("100", "TW"))
        self.assertTrue(validate_postal_code("106", "TW"))
        
        # 5位格式
        self.assertTrue(validate_postal_code("10001", "TW"))
        self.assertTrue(validate_postal_code("10607", "TW"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("1", "TW"))  # 太短
        self.assertFalse(validate_postal_code("100001", "TW"))  # 6位
    
    def test_validate_sg_codes(self):
        """测试新加坡邮编验证"""
        self.assertTrue(validate_postal_code("018956", "SG"))
        self.assertTrue(validate_postal_code("238858", "SG"))
        self.assertTrue(validate_postal_code("179103", "SG"))
        
        # 无效格式
        self.assertFalse(validate_postal_code("01895", "SG"))  # 5位
        self.assertFalse(validate_postal_code("0189567", "SG"))  # 7位
    
    def test_validate_hk_codes(self):
        """测试香港邮编（香港无标准邮编系统）"""
        self.assertFalse(validate_postal_code("123456", "HK"))  # 香港无标准邮编
    
    def test_validate_unknown_country(self):
        """测试未知国家"""
        self.assertFalse(validate_postal_code("12345", "XX"))  # 未知国家
        self.assertFalse(validate_postal_code("12345", "UNKNOWN"))
    
    def test_validate_whitespace_handling(self):
        """测试空格处理"""
        self.assertTrue(validate_postal_code(" 100001 ", "CN"))  # 带空格
        self.assertTrue(validate_postal_code("  12345  ", "US"))  # 带多空格


class TestFormatPostalCode(unittest.TestCase):
    """测试邮政编码格式化"""
    
    def test_format_cn_codes(self):
        """测试中国邮编格式化"""
        self.assertEqual(format_postal_code("100001", "CN"), "100001")
        self.assertEqual(format_postal_code(" 100001 ", "CN"), "100001")
    
    def test_format_us_codes(self):
        """测试美国ZIP码格式化"""
        # ZIP格式
        self.assertEqual(format_postal_code("12345", "US"), "12345")
        
        # ZIP+4紧凑格式转为标准格式
        self.assertEqual(format_postal_code("123456789", "US"), "12345-6789")
        
        # ZIP+4标准格式保持不变
        self.assertEqual(format_postal_code("12345-6789", "US"), "12345-6789")
    
    def test_format_jp_codes(self):
        """测试日本邮编格式化"""
        # 紧凑格式转为标准格式
        self.assertEqual(format_postal_code("1000001", "JP"), "〒100-0001")
        
        # 已格式化保持不变
        self.assertEqual(format_postal_code("100-0001", "JP"), "〒100-0001")
        self.assertEqual(format_postal_code("〒100-0001", "JP"), "〒100-0001")
    
    def test_format_uk_codes(self):
        """测试英国邮编格式化"""
        self.assertEqual(format_postal_code("SW1A 1AA", "UK"), "SW1A 1AA")
        self.assertEqual(format_postal_code("sw1a 1aa", "UK"), "SW1A 1AA")
        self.assertEqual(format_postal_code("SW1A1AA", "UK"), "SW1A 1AA")
    
    def test_format_ca_codes(self):
        """测试加拿大邮编格式化"""
        # 紧凑格式转为标准格式
        self.assertEqual(format_postal_code("K1A0B1", "CA"), "K1A 0B1")
        
        # 小写转为大写
        self.assertEqual(format_postal_code("k1a 0b1", "CA"), "K1A 0B1")
        self.assertEqual(format_postal_code("k1a0b1", "CA"), "K1A 0B1")
    
    def test_format_nl_codes(self):
        """测试荷兰邮编格式化"""
        self.assertEqual(format_postal_code("1011AB", "NL"), "1011 AB")
        self.assertEqual(format_postal_code("1011 AB", "NL"), "1011 AB")
    
    def test_format_pl_codes(self):
        """测试波兰邮编格式化"""
        self.assertEqual(format_postal_code("00001", "PL"), "00-001")
        self.assertEqual(format_postal_code("00-001", "PL"), "00-001")
    
    def test_format_br_codes(self):
        """测试巴西邮编格式化"""
        self.assertEqual(format_postal_code("01311000", "BR"), "01311-000")
        self.assertEqual(format_postal_code("01311-000", "BR"), "01311-000")


class TestNormalizePostalCode(unittest.TestCase):
    """测试邮政编码标准化"""
    
    def test_normalize_cn_codes(self):
        """测试中国邮编标准化"""
        self.assertEqual(normalize_postal_code("100001", "CN"), "100001")
        self.assertEqual(normalize_postal_code(" 100001 ", "CN"), "100001")
    
    def test_normalize_us_codes(self):
        """测试美国ZIP码标准化"""
        self.assertEqual(normalize_postal_code("12345", "US"), "12345")
        self.assertEqual(normalize_postal_code("12345-6789", "US"), "123456789")
    
    def test_normalize_jp_codes(self):
        """测试日本邮编标准化"""
        self.assertEqual(normalize_postal_code("100-0001", "JP"), "1000001")
        self.assertEqual(normalize_postal_code("〒100-0001", "JP"), "1000001")
    
    def test_normalize_ca_codes(self):
        """测试加拿大邮编标准化"""
        self.assertEqual(normalize_postal_code("K1A 0B1", "CA"), "K1A0B1")
        self.assertEqual(normalize_postal_code("k1a 0b1", "CA"), "K1A0B1")
    
    def test_normalize_uk_codes(self):
        """测试英国邮编标准化"""
        self.assertEqual(normalize_postal_code("SW1A 1AA", "UK"), "SW1A1AA")
        self.assertEqual(normalize_postal_code("sw1a 1aa", "UK"), "SW1A1AA")


class TestGetPostalCodeInfo(unittest.TestCase):
    """测试获取邮政编码详细信息"""
    
    def test_get_info_cn_codes(self):
        """测试中国邮编信息"""
        info = get_postal_code_info("100001", "CN")
        self.assertTrue(info.is_valid)
        self.assertEqual(info.country, "CN")
        self.assertEqual(info.code, "100001")
        self.assertEqual(info.normalized, "100001")
        self.assertEqual(info.format_type, "standard")
    
    def test_get_info_us_codes(self):
        """测试美国ZIP码信息"""
        # ZIP格式
        info = get_postal_code_info("12345", "US")
        self.assertTrue(info.is_valid)
        self.assertEqual(info.country, "US")
        self.assertEqual(info.code, "12345")
        
        # ZIP+4格式
        info = get_postal_code_info("12345-6789", "US")
        self.assertTrue(info.is_valid)
        self.assertEqual(info.code, "12345-6789")
        self.assertEqual(info.format_type, "zip_plus_4")
    
    def test_get_info_ca_codes(self):
        """测试加拿大邮编信息"""
        info = get_postal_code_info("K1A 0B1", "CA")
        self.assertTrue(info.is_valid)
        self.assertEqual(info.country, "CA")
        self.assertEqual(info.code, "K1A 0B1")
        self.assertEqual(info.normalized, "K1A0B1")
    
    def test_get_info_invalid_codes(self):
        """测试无效邮编信息"""
        info = get_postal_code_info("invalid", "CN")
        self.assertFalse(info.is_valid)
        
        info = get_postal_code_info("100001", "XX")
        self.assertFalse(info.is_valid)
    
    def test_get_info_raw_input(self):
        """测试原始输入保留"""
        info = get_postal_code_info("  100001  ", "CN")
        self.assertEqual(info.raw_input, "  100001  ")
        self.assertEqual(info.code, "100001")


class TestExtractPostalCodes(unittest.TestCase):
    """测试从文本提取邮政编码"""
    
    def test_extract_cn_codes(self):
        """测试提取中国邮编"""
        text = "请寄往北京市 100001 或上海 200001"
        codes = extract_postal_codes(text, "CN")
        self.assertEqual(len(codes), 2)
        self.assertIn(("100001", "CN"), codes)
        self.assertIn(("200001", "CN"), codes)
    
    def test_extract_us_codes(self):
        """测试提取美国ZIP码"""
        text = "ZIP: 12345 or 90210-1234"
        codes = extract_postal_codes(text, "US")
        # 注意：90210-1234 中的 90210 也会被匹配
        self.assertEqual(len(codes), 3)
        self.assertIn(("12345", "US"), codes)
        self.assertIn(("90210-1234", "US"), codes)
    
    def test_extract_uk_codes(self):
        """测试提取英国邮编"""
        text = "Address: SW1A 1AA, London and M1 1AA, Manchester"
        codes = extract_postal_codes(text, "UK")
        self.assertEqual(len(codes), 2)
        self.assertIn(("SW1A 1AA", "UK"), codes)
        self.assertIn(("M1 1AA", "UK"), codes)
    
    def test_extract_multiple_countries(self):
        """测试提取多国邮编"""
        text = "CN: 100001, US: 12345, CA: K1A 0B1"
        codes = extract_postal_codes(text)
        # 注意：不指定国家时会尝试所有国家的模式，可能匹配多次
        # 验证包含主要国家的邮编
        self.assertTrue(len(codes) >= 3)
        # 检查包含预期的主要邮编
        found_cn = any(c[1] == "CN" and c[0] == "100001" for c in codes)
        found_ca = any(c[1] == "CA" for c in codes)
        self.assertTrue(found_cn)
        self.assertTrue(found_ca)
    
    def test_extract_no_codes(self):
        """测试无邮编文本"""
        text = "这是一段普通文本，没有邮编"
        codes = extract_postal_codes(text, "CN")
        self.assertEqual(len(codes), 0)


class TestDetectCountry(unittest.TestCase):
    """测试自动检测国家"""
    
    def test_detect_cn_codes(self):
        """测试检测中国邮编"""
        # 6位数字邮编可能是中国、俄罗斯、印度等
        countries = detect_country("100001")
        self.assertIn("CN", countries)
        self.assertIn("RU", countries)
        self.assertIn("IN", countries)
    
    def test_detect_ca_codes(self):
        """测试检测加拿大邮编"""
        countries = detect_country("K1A 0B1")
        self.assertEqual(countries, ["CA"])
    
    def test_detect_uk_codes(self):
        """测试检测英国邮编"""
        countries = detect_country("SW1A 1AA")
        self.assertEqual(countries, ["UK"])
    
    def test_detect_us_codes(self):
        """测试检测美国ZIP码"""
        # 5位数字邮编可能是多个国家
        countries = detect_country("12345")
        self.assertIn("US", countries)
        self.assertIn("DE", countries)
        self.assertIn("FR", countries)
    
    def test_detect_jp_codes(self):
        """测试检测日本邮编"""
        countries = detect_country("100-0001")
        self.assertEqual(countries, ["JP"])
    
    def test_detect_invalid_codes(self):
        """测试检测无效邮编"""
        countries = detect_country("")
        self.assertEqual(len(countries), 0)
        
        countries = detect_country("hello")
        self.assertEqual(len(countries), 0)


class TestIsValidPostalCodeFormat(unittest.TestCase):
    """测试检查是否为有效邮编格式"""
    
    def test_valid_formats(self):
        """测试有效格式"""
        is_valid, countries = is_valid_postal_code_format("100001")
        self.assertTrue(is_valid)
        self.assertTrue(len(countries) > 0)
        
        is_valid, countries = is_valid_postal_code_format("K1A 0B1")
        self.assertTrue(is_valid)
        self.assertEqual(countries, ["CA"])
    
    def test_invalid_formats(self):
        """测试无效格式"""
        is_valid, countries = is_valid_postal_code_format("hello")
        self.assertFalse(is_valid)
        self.assertEqual(len(countries), 0)
        
        is_valid, countries = is_valid_postal_code_format("")
        self.assertFalse(is_valid)
        self.assertEqual(len(countries), 0)


class TestGetCountryPostalCodeInfo(unittest.TestCase):
    """测试获取国家邮编规则信息"""
    
    def test_get_cn_info(self):
        """测试获取中国邮编规则"""
        info = get_country_postal_code_info("CN")
        self.assertEqual(info["name"], "中国")
        self.assertEqual(info["country_code"], "CN")
        self.assertTrue(len(info["patterns"]) > 0)
        self.assertTrue(len(info["example_codes"]) > 0)
    
    def test_get_us_info(self):
        """测试获取美国邮编规则"""
        info = get_country_postal_code_info("US")
        self.assertEqual(info["name"], "美国")
        self.assertEqual(info["country_code"], "US")
        self.assertTrue(len(info["patterns"]) >= 3)  # ZIP, ZIP+4, ZIP+4紧凑
    
    def test_get_unknown_country_info(self):
        """测试获取未知国家信息"""
        info = get_country_postal_code_info("XX")
        self.assertEqual(info, {})


class TestComparePostalCodes(unittest.TestCase):
    """测试比较邮政编码"""
    
    def test_compare_cn_codes(self):
        """测试比较中国邮编"""
        self.assertEqual(compare_postal_codes("100001", "100002", "CN"), -1)
        self.assertEqual(compare_postal_codes("100002", "100001", "CN"), 1)
        self.assertEqual(compare_postal_codes("100001", "100001", "CN"), 0)
    
    def test_compare_us_codes(self):
        """测试比较美国ZIP码"""
        self.assertEqual(compare_postal_codes("12345", "12346", "US"), -1)
        self.assertEqual(compare_postal_codes("123456789", "12345-6789", "US"), 0)  # 标准化后相同
    
    def test_compare_unknown_country(self):
        """测试未知国家比较"""
        self.assertEqual(compare_postal_codes("100001", "100002", "XX"), -1)


class TestGetNearbyPostalCodes(unittest.TestCase):
    """测试获取附近邮政编码"""
    
    def test_nearby_cn_codes(self):
        """测试中国附近邮编"""
        nearby = get_nearby_postal_codes("100001", "CN", 2)
        self.assertIn("099999", nearby)
        self.assertIn("100000", nearby)
        self.assertIn("100001", nearby)
        self.assertIn("100002", nearby)
        self.assertIn("100003", nearby)
        self.assertEqual(len(nearby), 5)
    
    def test_nearby_us_codes(self):
        """测试美国附近ZIP码"""
        nearby = get_nearby_postal_codes("12345", "US", 1)
        self.assertIn("12344", nearby)
        self.assertIn("12345", nearby)
        self.assertIn("12346", nearby)
    
    def test_nearby_non_numeric_codes(self):
        """测试非数字邮编"""
        nearby = get_nearby_postal_codes("K1A 0B1", "CA", 1)
        self.assertEqual(nearby, ["K1A 0B1"])  # 非数字邮编返回原值


class TestBatchValidate(unittest.TestCase):
    """测试批量验证"""
    
    def test_batch_valid(self):
        """测试批量验证有效邮编"""
        batch = [("100001", "CN"), ("12345", "US"), ("K1A 0B1", "CA")]
        result = batch_validate(batch)
        self.assertEqual(len(result["valid"]), 3)
        self.assertEqual(len(result["invalid"]), 0)
    
    def test_batch_mixed(self):
        """测试批量验证混合邮编"""
        batch = [("100001", "CN"), ("invalid", "CN"), ("12345", "US")]
        result = batch_validate(batch)
        self.assertEqual(len(result["valid"]), 2)
        self.assertEqual(len(result["invalid"]), 1)
    
    def test_batch_all_invalid(self):
        """测试批量验证全部无效"""
        batch = [("abc", "CN"), ("xyz", "US")]
        result = batch_validate(batch)
        self.assertEqual(len(result["valid"]), 0)
        self.assertEqual(len(result["invalid"]), 2)


class TestGenerateRandomPostalCode(unittest.TestCase):
    """测试生成随机邮政编码"""
    
    def test_generate_cn_codes(self):
        """测试生成随机中国邮编"""
        code = generate_random_postal_code("CN")
        self.assertIsNotNone(code)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())
    
    def test_generate_us_codes(self):
        """测试生成随机美国ZIP码"""
        code = generate_random_postal_code("US")
        self.assertIsNotNone(code)
        self.assertTrue(len(code) == 5 or len(code) == 10)  # ZIP or ZIP+4
    
    def test_generate_jp_codes(self):
        """测试生成随机日本邮编"""
        code = generate_random_postal_code("JP")
        self.assertIsNotNone(code)
        self.assertTrue(code.startswith("〒"))
    
    def test_generate_ca_codes(self):
        """测试生成随机加拿大邮编"""
        code = generate_random_postal_code("CA")
        self.assertIsNotNone(code)
        self.assertTrue(validate_postal_code(code, "CA"))
    
    def test_generate_unknown_country(self):
        """测试生成未知国家邮编"""
        code = generate_random_postal_code("XX")
        self.assertIsNone(code)


class TestGetSupportedCountries(unittest.TestCase):
    """测试获取支持的国家列表"""
    
    def test_get_supported_countries(self):
        """测试获取支持国家"""
        countries = get_supported_countries()
        self.assertTrue(len(countries) > 0)
        
        # 检查是否包含主要国家
        country_codes = [c["code"] for c in countries]
        self.assertIn("CN", country_codes)
        self.assertIn("US", country_codes)
        self.assertIn("JP", country_codes)
        self.assertIn("UK", country_codes)
        self.assertIn("CA", country_codes)
    
    def test_country_has_name(self):
        """测试国家包含名称"""
        countries = get_supported_countries()
        for country in countries:
            self.assertIn("code", country)
            self.assertIn("name", country)
            self.assertTrue(len(country["name"]) > 0)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertFalse(validate_postal_code("", "CN"))
        self.assertEqual(format_postal_code("", "CN"), "")
        self.assertEqual(normalize_postal_code("", "CN"), "")
    
    def test_none_handling(self):
        """测试None处理"""
        # 函数应该能处理None输入
        self.assertFalse(validate_postal_code(None, "CN"))
        self.assertEqual(format_postal_code(None, "CN"), "")
        self.assertEqual(normalize_postal_code(None, "CN"), "")
    
    def test_whitespace_only(self):
        """测试纯空格"""
        self.assertFalse(validate_postal_code("   ", "CN"))
    
    def test_special_characters(self):
        """测试特殊字符"""
        self.assertFalse(validate_postal_code("!@#$%", "CN"))
        self.assertFalse(validate_postal_code("100\n001", "CN"))
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        # 英国和加拿大邮编应该大小写不敏感
        self.assertTrue(validate_postal_code("sw1a 1aa", "UK"))
        self.assertTrue(validate_postal_code("k1a 0b1", "CA"))
    
    def test_long_code(self):
        """测试超长邮编"""
        self.assertFalse(validate_postal_code("10000100000000000000", "CN"))
    
    def test_mixed_content(self):
        """测试混合内容"""
        self.assertFalse(validate_postal_code("100abc001", "CN"))


class TestConvenienceAliases(unittest.TestCase):
    """测试便捷函数别名"""
    
    def test_validate_alias(self):
        """测试validate别名"""
        from mod import validate
        self.assertEqual(validate("100001", "CN"), validate_postal_code("100001", "CN"))
    
    def test_format_alias(self):
        """测试format别名"""
        from mod import format
        self.assertEqual(format("100001", "CN"), format_postal_code("100001", "CN"))
    
    def test_normalize_alias(self):
        """测试normalize别名"""
        from mod import normalize
        self.assertEqual(normalize("100001", "CN"), normalize_postal_code("100001", "CN"))
    
    def test_info_alias(self):
        """测试info别名"""
        from mod import info
        result = info("100001", "CN")
        self.assertTrue(result.is_valid)
    
    def test_extract_alias(self):
        """测试extract别名"""
        from mod import extract
        codes = extract("Send to 100001", "CN")
        self.assertEqual(len(codes), 1)
    
    def test_detect_alias(self):
        """测试detect别名"""
        from mod import detect
        countries = detect("100001")
        self.assertIn("CN", countries)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
    
    # 统计测试数量
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    print(f"\n总计测试数量: {suite.countTestCases()}")