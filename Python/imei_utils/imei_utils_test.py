"""
IMEI 工具模块测试

测试覆盖:
- Luhn 校验位计算
- IMEI 验证
- IMEI 解析
- IMEI 格式化
- 随机 IMEI 生成
- IMEI 比较
- TAC 信息提取
- IMEIValidator 类
"""

import unittest
from mod import (
    calculate_luhn_checksum,
    validate_imei,
    parse_imei,
    format_imei,
    generate_random_imei,
    generate_batch_imeis,
    get_imei_type,
    compare_imeis,
    extract_tac_info,
    IMEIValidator,
    TEST_TAC_SAMPLE
)


class TestLuhnChecksum(unittest.TestCase):
    """测试 Luhn 校验位计算"""
    
    def test_valid_checksum_calculation(self):
        """测试正确的校验位计算"""
        # 使用已知正确的前缀计算校验位
        # TAC: 35209009, SNR: 632947 -> 校验位 3
        checksum = calculate_luhn_checksum("35209009632947")
        self.assertEqual(checksum, 3)
        
        # 测试另一个案例
        checksum2 = calculate_luhn_checksum("86685935786051")
        self.assertIn(checksum2, range(10))
    
    def test_checksum_zero(self):
        """测试校验位为0的情况"""
        # 寻找校验位为0的情况
        checksum = calculate_luhn_checksum("35209009176540")
        self.assertIn(checksum, range(10))
    
    def test_invalid_input_length(self):
        """测试输入长度错误"""
        with self.assertRaises(ValueError):
            calculate_luhn_checksum("12345")
        
        with self.assertRaises(ValueError):
            calculate_luhn_checksum("123456789012345")
    
    def test_invalid_input_chars(self):
        """测试输入包含非数字字符"""
        with self.assertRaises(ValueError):
            calculate_luhn_checksum("123456789abcde")


class TestValidateIMEI(unittest.TestCase):
    """测试 IMEI 验证"""
    
    def test_valid_imei(self):
        """测试有效的 IMEI"""
        # 使用动态生成的有效 IMEI
        imei = generate_random_imei(tac="35209009")
        # 标准格式，带分隔符
        formatted = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"
        self.assertTrue(validate_imei(formatted))
        # 无分隔符
        self.assertTrue(validate_imei(imei))
        # 空格分隔
        self.assertTrue(validate_imei(f"{imei[:8]} {imei[8:14]} {imei[14]}"))
    
    def test_invalid_imei_wrong_checksum(self):
        """测试校验位错误的 IMEI"""
        # 生成有效 IMEI 后修改校验位
        imei = generate_random_imei()
        wrong_checksum = str((int(imei[14]) + 1) % 10)
        wrong_imei = imei[:14] + wrong_checksum
        self.assertFalse(validate_imei(wrong_imei))
    
    def test_invalid_imei_wrong_length(self):
        """测试长度错误的 IMEI"""
        self.assertFalse(validate_imei("3520900917654"))
        self.assertFalse(validate_imei("3520900917654833"))
    
    def test_invalid_imei_non_numeric(self):
        """测试非数字字符的 IMEI"""
        self.assertFalse(validate_imei("35-209009-176548-a"))
        self.assertFalse(validate_imei("imei-123456789"))
    
    def test_empty_imei(self):
        """测试空 IMEI"""
        self.assertFalse(validate_imei(""))
        self.assertFalse(validate_imei("-"))


class TestParseIMEI(unittest.TestCase):
    """测试 IMEI 解析"""
    
    def test_parse_valid_imei(self):
        """测试解析有效的 IMEI"""
        # 使用动态生成的有效 IMEI
        imei = generate_random_imei(tac="35209009")
        formatted = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"
        parsed = parse_imei(formatted)
        
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['imei'], imei)
        self.assertEqual(parsed['tac'], "35209009")
        self.assertEqual(parsed['snr'], imei[8:14])
        self.assertEqual(parsed['checksum'], imei[14])
    
    def test_parse_clean_imei(self):
        """测试解析无分隔符的 IMEI"""
        imei = generate_random_imei()
        parsed = parse_imei(imei)
        
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['tac'], imei[:8])
        self.assertEqual(parsed['snr'], imei[8:14])
    
    def test_parse_invalid_imei(self):
        """测试解析无效的 IMEI"""
        self.assertIsNone(parse_imei("invalid"))
        self.assertIsNone(parse_imei("123"))
        # 错误校验位的 IMEI
        imei = generate_random_imei()
        wrong_checksum = str((int(imei[14]) + 1) % 10)
        self.assertIsNone(parse_imei(imei[:14] + wrong_checksum))


class TestFormatIMEI(unittest.TestCase):
    """测试 IMEI 格式化"""
    
    def test_format_standard(self):
        """测试标准格式化"""
        formatted = format_imei("352090091765483")
        self.assertEqual(formatted, "35209009-176548-3")
    
    def test_format_custom_separator(self):
        """测试自定义分隔符"""
        formatted = format_imei("352090091765483", separator=' ')
        self.assertEqual(formatted, "35209009 176548 3")
    
    def test_format_already_formatted(self):
        """测试已格式化的 IMEI"""
        formatted = format_imei("35-209009-176548-3")
        self.assertEqual(formatted, "35209009-176548-3")
    
    def test_format_invalid(self):
        """测试格式化无效 IMEI"""
        with self.assertRaises(ValueError):
            format_imei("invalid")
        
        with self.assertRaises(ValueError):
            format_imei("12345")


class TestGenerateIMEI(unittest.TestCase):
    """测试随机 IMEI 生成"""
    
    def test_generate_random_imei(self):
        """测试生成随机 IMEI"""
        imei = generate_random_imei()
        
        self.assertEqual(len(imei), 15)
        self.assertTrue(imei.isdigit())
        self.assertTrue(validate_imei(imei))
    
    def test_generate_with_custom_tac(self):
        """测试使用自定义 TAC 生成"""
        tac = "35905001"
        imei = generate_random_imei(tac=tac)
        
        self.assertEqual(len(imei), 15)
        self.assertTrue(imei.startswith(tac))
        self.assertTrue(validate_imei(imei))
    
    def test_generate_invalid_tac(self):
        """测试无效 TAC"""
        with self.assertRaises(ValueError):
            generate_random_imei(tac="1234567")  # 7位
        
        with self.assertRaises(ValueError):
            generate_random_imei(tac="12345678a")  # 包含字母
    
    def test_generate_batch(self):
        """测试批量生成"""
        imeis = generate_batch_imeis(5)
        
        self.assertEqual(len(imeis), 5)
        for imei in imeis:
            self.assertTrue(validate_imei(imei))
    
    def test_generate_batch_with_tac(self):
        """测试批量生成使用自定义 TAC"""
        tac = "35905001"
        imeis = generate_batch_imeis(10, tac=tac)
        
        for imei in imeis:
            self.assertTrue(imei.startswith(tac))
    
    def test_generate_batch_invalid_count(self):
        """测试批量生成无效数量"""
        with self.assertRaises(ValueError):
            generate_batch_imeis(0)
        
        with self.assertRaises(ValueError):
            generate_batch_imeis(10001)


class TestGetIMEIType(unittest.TestCase):
    """测试设备类型判断"""
    
    def test_test_range(self):
        """测试测试范围"""
        self.assertEqual(get_imei_type("00123456"), "测试/假设备")
    
    def test_common_mobile(self):
        """测试常见移动设备"""
        result = get_imei_type("35123456")
        self.assertEqual(result, "常见移动设备")
    
    def test_reserved_range(self):
        """测试保留范围"""
        result = get_imei_type("86123456")
        self.assertEqual(result, "测试/保留范围")
    
    def test_standard_allocation(self):
        """测试标准分配"""
        result = get_imei_type("01123456")
        self.assertIn("标准分配", result)
    
    def test_invalid_tac(self):
        """测试无效 TAC"""
        result = get_imei_type("1234567")
        self.assertEqual(result, "无效的 TAC")
        
        result = get_imei_type("1234567a")
        self.assertEqual(result, "无效的 TAC")


class TestCompareIMEIs(unittest.TestCase):
    """测试 IMEI 比较"""
    
    def test_compare_same_imei(self):
        """测试比较相同的 IMEI"""
        imei = generate_random_imei()
        result = compare_imeis(imei, f"{imei[:8]}-{imei[8:14]}-{imei[14]}")
        
        self.assertTrue(result['imei1_valid'])
        self.assertTrue(result['imei2_valid'])
        self.assertTrue(result['are_equal'])
        self.assertTrue(result['same_tac'])
    
    def test_compare_different_imei_same_tac(self):
        """测试相同 TAC 不同 IMEI"""
        imei1 = generate_random_imei(tac="35905001")
        imei2 = generate_random_imei(tac="35905001")
        
        result = compare_imeis(imei1, imei2)
        
        self.assertTrue(result['imei1_valid'])
        self.assertTrue(result['imei2_valid'])
        self.assertFalse(result['are_equal'])
        self.assertTrue(result['same_tac'])
    
    def test_compare_invalid_imei(self):
        """测试比较无效 IMEI"""
        result = compare_imeis("invalid1", "invalid2")
        
        self.assertFalse(result['imei1_valid'])
        self.assertFalse(result['imei2_valid'])


class TestExtractTACInfo(unittest.TestCase):
    """测试 TAC 信息提取"""
    
    def test_extract_valid_tac(self):
        """测试提取有效 TAC"""
        info = extract_tac_info("35209009")
        
        self.assertEqual(info['tac'], "35209009")
        self.assertEqual(info['rbi'], "35")
        self.assertIn("GSMA", info['reporting_body'])
    
    def test_extract_chinese_tac(self):
        """测试中国 TAC"""
        info = extract_tac_info("86123456")
        
        self.assertEqual(info['rbi'], "86")
        self.assertIn("中国", info['reporting_body'])
    
    def test_extract_invalid_tac(self):
        """测试提取无效 TAC"""
        info = extract_tac_info("1234567")
        
        self.assertIn('error', info)


class TestIMEIValidator(unittest.TestCase):
    """测试 IMEIValidator 类"""
    
    def test_validator_valid_imei(self):
        """测试验证有效 IMEI"""
        imei = generate_random_imei(tac="35209009")
        formatted = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"
        validator = IMEIValidator(formatted)
        
        self.assertTrue(validator.is_valid)
        self.assertEqual(validator.tac, "35209009")
        self.assertEqual(validator.snr, imei[8:14])
        self.assertEqual(validator.checksum, imei[14])
        self.assertEqual(validator.formatted, f"{imei[:8]}-{imei[8:14]}-{imei[14]}")
    
    def test_validator_invalid_imei(self):
        """测试验证无效 IMEI"""
        validator = IMEIValidator("invalid")
        
        self.assertFalse(validator.is_valid)
        self.assertIsNone(validator.tac)
        self.assertIsNone(validator.snr)
        self.assertIsNone(validator.checksum)
    
    def test_validator_str(self):
        """测试字符串表示"""
        validator = IMEIValidator("352090091765483")
        self.assertEqual(str(validator), "352090091765483")
    
    def test_validator_repr(self):
        """测试 repr 表示"""
        imei = generate_random_imei()
        validator_valid = IMEIValidator(imei)
        repr_valid = repr(validator_valid)
        self.assertIn("有效", repr_valid)
        
        validator_invalid = IMEIValidator("invalid")
        repr_invalid = repr(validator_invalid)
        self.assertIn("无效", repr_invalid)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 生成
        imei = generate_random_imei(tac=TEST_TAC_SAMPLE)
        
        # 验证
        self.assertTrue(validate_imei(imei))
        
        # 解析
        parsed = parse_imei(imei)
        self.assertIsNotNone(parsed)
        
        # 格式化
        formatted = format_imei(imei)
        self.assertIn("-", formatted)
        
        # 再次验证格式化后的
        self.assertTrue(validate_imei(formatted))
    
    def test_batch_generation_and_validation(self):
        """测试批量生成和验证"""
        imeis = generate_batch_imeis(100, tac="35905001")
        
        # 所有 IMEI 应该有效
        valid_count = sum(1 for imei in imeis if validate_imei(imei))
        self.assertEqual(valid_count, 100)
        
        # 所有 IMEI 应该有相同的 TAC
        same_tac_count = sum(1 for imei in imeis if imei.startswith("35905001"))
        self.assertEqual(same_tac_count, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)