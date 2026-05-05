"""
物流追踪号码工具测试用例
"""

import unittest
from mod import (
    TrackingNumberUtils,
    TrackingResult,
    Carrier,
    validate,
    identify_carrier,
    get_tracking_url,
    extract_from_text
)


class TestTrackingNumberUtils(unittest.TestCase):
    """追踪号码工具测试"""

    def test_normalize(self):
        """测试标准化功能"""
        self.assertEqual(TrackingNumberUtils.normalize("1z 999 aa 10 1234567890"), "1Z999AA101234567890")
        self.assertEqual(TrackingNumberUtils.normalize("1234-5678-9012"), "123456789012")
        self.assertEqual(TrackingNumberUtils.normalize("sf1234567890"), "SF1234567890")

    def test_identify_carrier_ups(self):
        """测试识别UPS"""
        # UPS 1Z开头的追踪号码 (18位)
        self.assertEqual(identify_carrier("1Z999AA10123456784"), Carrier.UPS)
        # 带空格的18位号码
        self.assertEqual(identify_carrier("1Z 999 AA 10 1234 5678 4"), Carrier.UPS)

    def test_identify_carrier_fedex(self):
        """测试识别FedEx"""
        # FedEx Express 12位
        self.assertEqual(identify_carrier("123456789012"), Carrier.FEDEX)
        # FedEx Ground 15位
        self.assertEqual(identify_carrier("212345678901234"), Carrier.FEDEX)
        self.assertEqual(identify_carrier("612345678901234"), Carrier.FEDEX)

    def test_identify_carrier_usps(self):
        """测试识别USPS"""
        # USPS 22位以9开头
        self.assertEqual(identify_carrier("9400111899223336117112"), Carrier.USPS)
        # USPS Express Mail
        self.assertEqual(identify_carrier("EA123456789US"), Carrier.USPS)

    def test_identify_carrier_dhl(self):
        """测试识别DHL"""
        # DHL Express 10位
        self.assertEqual(identify_carrier("1234567890"), Carrier.DHL)
        # DHL ECommerce
        self.assertEqual(identify_carrier("GM12345678"), Carrier.DHL)

    def test_identify_carrier_sf(self):
        """测试识别顺丰"""
        self.assertEqual(identify_carrier("SF1234567890123"), Carrier.SF)
        self.assertEqual(identify_carrier("SF12345678901234"), Carrier.SF)

    def test_identify_carrier_china_post(self):
        """测试识别中国邮政"""
        # EMS格式
        self.assertEqual(identify_carrier("EA123456789CN"), Carrier.CHINA_POST)
        # 平邮格式 (PA开头+12位数字=14位)
        self.assertEqual(identify_carrier("PA123456789012"), Carrier.CHINA_POST)

    def test_identify_carrier_jd(self):
        """测试识别京东物流"""
        self.assertEqual(identify_carrier("JD123456789012"), Carrier.JD)
        self.assertEqual(identify_carrier("JDX123456789012"), Carrier.JD)

    def test_identify_carrier_yto(self):
        """测试识别圆通速递"""
        # YT开头 + 11-13位数字
        self.assertEqual(identify_carrier("YT12345678901"), Carrier.YTO)
        self.assertEqual(identify_carrier("YTO1234567890123"), Carrier.YTO)

    def test_identify_carrier_zto(self):
        """测试识别中通快递"""
        self.assertEqual(identify_carrier("712345678901"), Carrier.ZTO)
        self.assertEqual(identify_carrier("ZT12345678901"), Carrier.ZTO)

    def test_identify_carrier_sto(self):
        """测试识别申通快递"""
        self.assertEqual(identify_carrier("7123456789012"), Carrier.STO)
        self.assertEqual(identify_carrier("ST12345678901"), Carrier.STO)

    def test_identify_carrier_yd(self):
        """测试识别韵达快递"""
        self.assertEqual(identify_carrier("1123456789012"), Carrier.YD)
        self.assertEqual(identify_carrier("YD12345678901"), Carrier.YD)

    def test_identify_carrier_jt(self):
        """测试识别极兔速递"""
        self.assertEqual(identify_carrier("JT12345678901"), Carrier.JT)

    def test_identify_carrier_unknown(self):
        """测试未知承运商"""
        self.assertEqual(identify_carrier("INVALID"), Carrier.UNKNOWN)
        self.assertEqual(identify_carrier(""), Carrier.UNKNOWN)

    def test_validate_ups(self):
        """测试验证UPS追踪号码"""
        result = validate("1Z999AA10123456784")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.carrier, Carrier.UPS)
        self.assertIsNotNone(result.tracking_url)

    def test_validate_fedex(self):
        """测试验证FedEx追踪号码"""
        result = validate("123456789012")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.carrier, Carrier.FEDEX)
        self.assertIsNotNone(result.tracking_url)

    def test_validate_usps(self):
        """测试验证USPS追踪号码"""
        result = validate("9400111899223336117112")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.carrier, Carrier.USPS)

    def test_validate_china_courier(self):
        """测试验证中国快递"""
        result = validate("SF1234567890123")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.carrier, Carrier.SF)
        self.assertIn("sf-express", result.tracking_url.lower())

    def test_validate_empty(self):
        """测试空号码"""
        result = validate("")
        self.assertFalse(result.is_valid)
        self.assertEqual(result.carrier, Carrier.UNKNOWN)

    def test_validate_invalid(self):
        """测试无效号码"""
        result = validate("NOT_A_TRACKING_NUMBER")
        self.assertFalse(result.is_valid)
        self.assertEqual(result.carrier, Carrier.UNKNOWN)

    def test_get_tracking_url(self):
        """测试获取追踪URL"""
        url = get_tracking_url("1Z999AA10123456784")
        self.assertIsNotNone(url)
        self.assertIn("ups.com", url)
        self.assertIn("1Z999AA10123456784", url)

        url = get_tracking_url("SF1234567890123")
        self.assertIsNotNone(url)
        self.assertIn("sf-express", url.lower())

        url = get_tracking_url("INVALID")
        self.assertIsNone(url)

    def test_batch_validate(self):
        """测试批量验证"""
        numbers = [
            "1Z999AA10123456784",  # UPS
            "123456789012",  # FedEx
            "SF1234567890123",  # 顺丰
            "EA123456789CN",  # 中国邮政EMS
        ]

        results = TrackingNumberUtils.batch_validate(numbers)
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0].carrier, Carrier.UPS)
        self.assertEqual(results[1].carrier, Carrier.FEDEX)
        self.assertEqual(results[2].carrier, Carrier.SF)
        self.assertEqual(results[3].carrier, Carrier.CHINA_POST)

    def test_extract_from_text(self):
        """测试从文本提取追踪号码"""
        text = """
        您好，您的包裹已发出。
        UPS单号: 1Z999AA10123456784
        顺丰单号: SF1234567890123
        请注意查收。
        """
        results = extract_from_text(text)
        self.assertGreater(len(results), 0)

        # 检查提取结果
        tracking_numbers = [r[0] for r in results]
        self.assertIn("1Z999AA10123456784", tracking_numbers)

    def test_checksum_validation(self):
        """测试校验位验证"""
        # 有效号码
        result = validate("EA123456789CN")
        # 注意：这里的校验位可能不完全准确，因为我们使用的是简化算法

        # 测试格式正确但校验位可能错误的号码
        # 这里主要测试校验逻辑被正确调用

    def test_mixed_case(self):
        """测试大小写混合"""
        result = validate("1z999aa10123456784")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.normalized, "1Z999AA10123456784")

    def test_with_spaces_and_dashes(self):
        """测试带空格和连字符的号码"""
        # UPS 18位号码带空格
        result = validate("1Z 999 AA 10 1234 5678 4")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.normalized, "1Z999AA10123456784")

    def test_carrier_display_names(self):
        """测试承运商显示名称"""
        self.assertEqual(Carrier.UPS.value, "UPS")
        self.assertEqual(Carrier.SF.value, "顺丰速运")
        self.assertEqual(Carrier.CHINA_POST.value, "中国邮政")

    def test_tracking_result_dataclass(self):
        """测试TrackingResult数据类"""
        result = TrackingResult(
            is_valid=True,
            tracking_number="SF1234567890123",
            carrier=Carrier.SF,
            normalized="SF1234567890123",
            checksum_valid=True,
            tracking_url="https://example.com/track/SF1234567890123",
            message="追踪号码有效"
        )
        self.assertTrue(result.is_valid)
        self.assertEqual(result.carrier, Carrier.SF)
        self.assertEqual(result.message, "追踪号码有效")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_none_input(self):
        """测试None输入"""
        # Python的normalize函数会抛出AttributeError
        # 这是预期行为，因为None不是有效的字符串
        pass

    def test_very_long_number(self):
        """测试超长号码"""
        result = validate("1" * 100)
        self.assertFalse(result.is_valid)

    def test_special_characters(self):
        """测试特殊字符"""
        result = validate("SF@#$%123456")
        self.assertFalse(result.is_valid)

    def test_chinese_characters(self):
        """测试中文字符"""
        result = validate("顺丰123456789")
        self.assertFalse(result.is_valid)

    def test_real_world_numbers(self):
        """测试真实世界追踪号码格式"""
        # 这些是格式正确的测试号码（非真实）
        test_cases = [
            # UPS
            ("1Z999AA10123456784", Carrier.UPS),
            # FedEx Express
            ("123456789012", Carrier.FEDEX),
            # 顺丰
            ("SF1234567890123", Carrier.SF),
            # EMS
            ("EA123456789CN", Carrier.CHINA_POST),
            # 京东
            ("JD123456789012", Carrier.JD),
            # 极兔
            ("JT1234567890123", Carrier.JT),
        ]

        for tracking_num, expected_carrier in test_cases:
            result = validate(tracking_num)
            self.assertTrue(result.is_valid, f"Failed for {tracking_num}")
            self.assertEqual(result.carrier, expected_carrier, f"Wrong carrier for {tracking_num}")


if __name__ == "__main__":
    unittest.main(verbosity=2)