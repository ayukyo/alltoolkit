"""
Currency Utils 单元测试
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from mod import (
    Currency, validate_code, get_currency_info, format_currency,
    parse_currency, convert, exchange, get_rate, round_currency,
    format_multi, compare, calculate_fees, cents_to_amount,
    amount_to_cents, list_currencies, get_supported_currencies,
    DEFAULT_RATES, CURRENCY_DATA
)


class TestCurrencyClass(unittest.TestCase):
    """Currency 类测试"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        c = Currency("100", "USD")
        self.assertEqual(c.amount, Decimal("100"))
        self.assertEqual(c.code, "USD")
        self.assertEqual(c.symbol, "$")
        self.assertEqual(c.name, "US Dollar")
    
    def test_invalid_code(self):
        """测试无效货币代码"""
        with self.assertRaises(ValueError):
            Currency(100, "INVALID")
    
    def test_string_amount(self):
        """测试字符串金额"""
        c = Currency("1234.56", "EUR")
        self.assertEqual(c.amount, Decimal("1234.56"))
    
    def test_decimal_amount(self):
        """测试 Decimal 金额"""
        c = Currency(Decimal("999.99"), "JPY")
        self.assertEqual(c.amount, Decimal("999.99"))
    
    def test_arithmetic(self):
        """测试算术运算"""
        c1 = Currency(100, "USD")
        c2 = Currency(50, "USD")
        
        result = c1 + c2
        self.assertEqual(result.amount, Decimal("150"))
        self.assertEqual(result.code, "USD")
        
        result = c1 - c2
        self.assertEqual(result.amount, Decimal("50"))
        
        result = c1 * 2
        self.assertEqual(result.amount, Decimal("200"))
        
        result = c1 / 2
        self.assertEqual(result.amount, Decimal("50"))
    
    def test_arithmetic_with_number(self):
        """测试与数字的运算"""
        c = Currency(100, "USD")
        result = c + 50
        self.assertEqual(result.amount, Decimal("150"))
    
    def test_comparison(self):
        """测试比较运算"""
        c1 = Currency(100, "USD")
        c2 = Currency(150, "USD")
        c3 = Currency(100, "USD")
        
        self.assertTrue(c1 < c2)
        self.assertTrue(c1 <= c3)
        self.assertTrue(c2 > c1)
        self.assertTrue(c2 >= c3)
        self.assertTrue(c1 == c3)
        self.assertFalse(c1 == c2)
    
    def test_mixed_code_operations(self):
        """测试混合货币代码运算（应报错）"""
        c1 = Currency(100, "USD")
        c2 = Currency(50, "EUR")
        
        with self.assertRaises(ValueError):
            c1 + c2
    
    def test_formatted(self):
        """测试格式化"""
        c = Currency("1234.567", "USD")
        formatted = c.formatted()
        self.assertIn("$", formatted)
        self.assertIn("1,234.57", formatted)


class TestValidation(unittest.TestCase):
    """验证函数测试"""
    
    def test_validate_code(self):
        """测试货币代码验证"""
        self.assertTrue(validate_code("USD"))
        self.assertTrue(validate_code("eur"))
        self.assertTrue(validate_code("JPY"))
        self.assertFalse(validate_code("INVALID"))
        self.assertFalse(validate_code(""))
    
    def test_get_currency_info(self):
        """测试获取货币信息"""
        info = get_currency_info("USD")
        self.assertIsNotNone(info)
        self.assertEqual(info["code"], "USD")
        self.assertEqual(info["symbol"], "$")
        self.assertEqual(info["name"], "US Dollar")
        self.assertEqual(info["decimals"], 2)
        
        info = get_currency_info("JPY")
        self.assertEqual(info["decimals"], 0)
        
        self.assertIsNone(get_currency_info("INVALID"))
    
    def test_list_currencies(self):
        """测试货币列表"""
        currencies = list_currencies()
        self.assertIsInstance(currencies, list)
        self.assertIn("USD", currencies)
        self.assertIn("EUR", currencies)
        self.assertIn("JPY", currencies)
        self.assertGreater(len(currencies), 30)


class TestFormatting(unittest.TestCase):
    """格式化测试"""
    
    def test_format_currency(self):
        """测试货币格式化"""
        # 美元格式
        self.assertEqual(format_currency("1234.56", "USD"), "$1,234.56")
        self.assertEqual(format_currency("0.99", "USD"), "$0.99")
        self.assertEqual(format_currency("1000000", "USD"), "$1,000,000.00")
        
        # 日元（无小数）
        self.assertEqual(format_currency("1234", "JPY"), "¥1,234")
        
        # 欧元
        self.assertEqual(format_currency("1234.56", "EUR"), "€1,234.56")
    
    def test_format_negative(self):
        """测试负数格式化"""
        result = format_currency(-1234.56, "USD")
        self.assertIn("-", result)
    
    def test_format_invalid_code(self):
        """测试无效代码格式化"""
        with self.assertRaises(ValueError):
            format_currency(100, "INVALID")


class TestParsing(unittest.TestCase):
    """解析测试"""
    
    def test_parse_simple(self):
        """测试简单解析"""
        amount, code = parse_currency("$1,234.56", "USD")
        self.assertEqual(amount, Decimal("1234.56"))
        
        amount, code = parse_currency("€1.234,56", "EUR")
        self.assertEqual(amount, Decimal("1234.56"))
    
    def test_parse_with_code(self):
        """测试带货币代码的解析"""
        amount, code = parse_currency("1234.56 USD")
        self.assertEqual(amount, Decimal("1234.56"))
        self.assertEqual(code, "USD")
    
    def test_parse_negative(self):
        """测试负数解析"""
        amount, code = parse_currency("-1,234.56")
        self.assertEqual(amount, Decimal("-1234.56"))
    
    def test_parse_integer(self):
        """测试整数解析"""
        amount, code = parse_currency("$100")
        self.assertEqual(amount, Decimal("100"))


class TestConversion(unittest.TestCase):
    """货币转换测试"""
    
    def test_same_currency(self):
        """测试相同货币"""
        result = convert(100, "USD", "USD")
        self.assertEqual(result, Decimal("100"))
    
    def test_usd_to_eur(self):
        """测试 USD 到 EUR 转换"""
        result = convert(100, "USD", "EUR")
        # 使用默认汇率
        rate = DEFAULT_RATES["EUR"] / DEFAULT_RATES["USD"]
        expected = Decimal("100") * Decimal(str(rate))
        self.assertAlmostEqual(float(result), float(expected), places=2)
    
    def test_exchange_function(self):
        """测试 exchange 函数"""
        result = exchange(100, "USD", "EUR")
        self.assertIsInstance(result, Currency)
        self.assertEqual(result.code, "EUR")
    
    def test_get_rate(self):
        """测试获取汇率"""
        rate = get_rate("USD", "EUR")
        expected = DEFAULT_RATES["EUR"] / DEFAULT_RATES["USD"]
        self.assertAlmostEqual(rate, expected, places=4)
        
        # 同一货币
        self.assertEqual(get_rate("USD", "USD"), 1.0)
    
    def test_get_rate_invalid(self):
        """测试无效货币汇率"""
        with self.assertRaises(ValueError):
            get_rate("INVALID", "USD")


class TestRounding(unittest.TestCase):
    """舍入测试"""
    
    def test_round_currency(self):
        """测试货币舍入"""
        # 美元舍入到分
        self.assertEqual(round_currency(100.555, "USD"), Decimal("100.56"))
        self.assertEqual(round_currency(100.554, "USD"), Decimal("100.55"))
        
        # 日元舍入到整数
        self.assertEqual(round_currency(100.5, "JPY"), Decimal("101"))
    
    def test_round_modes(self):
        """测试不同舍入模式"""
        amount = 100.555
        self.assertEqual(round_currency(amount, "USD", "HALF_UP"), Decimal("100.56"))
        self.assertEqual(round_currency(amount, "USD", "FLOOR"), Decimal("100.55"))


class TestMultiCurrency(unittest.TestCase):
    """多币种测试"""
    
    def test_format_multi(self):
        """测试多币种格式化"""
        result = format_multi(1000, "USD", ["USD", "EUR", "CNY"])
        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertIn("CNY", result)
        self.assertIsInstance(result["USD"], str)


class TestComparison(unittest.TestCase):
    """比较测试"""
    
    def test_compare_same_code(self):
        """测试相同货币比较"""
        self.assertEqual(compare(Currency(100, "USD"), Currency(100, "USD")), 0)
        self.assertEqual(compare(Currency(100, "USD"), Currency(200, "USD")), -1)
        self.assertEqual(compare(Currency(200, "USD"), Currency(100, "USD")), 1)
    
    def test_compare_with_numbers(self):
        """测试与数字比较"""
        self.assertEqual(compare(Currency(100, "USD"), 100), 0)


class TestFees(unittest.TestCase):
    """手续费测试"""
    
    def test_basic_fee(self):
        """测试基本手续费"""
        result = calculate_fees(1000, "USD", fee_percent=0.03)
        self.assertEqual(result["fee_percent"], Decimal("30"))
        self.assertEqual(result["fee_fixed"], Decimal("0"))
        self.assertEqual(result["total_fee"], Decimal("30"))
        self.assertEqual(result["net_amount"], Decimal("970"))
    
    def test_fee_with_fixed(self):
        """测试固定手续费"""
        result = calculate_fees(1000, "USD", fee_percent=0.03, fee_fixed=5)
        self.assertEqual(result["fee_percent"], Decimal("30"))
        self.assertEqual(result["fee_fixed"], Decimal("5"))
        self.assertEqual(result["total_fee"], Decimal("35"))
    
    def test_fee_minimum(self):
        """测试最低手续费"""
        result = calculate_fees(100, "USD", fee_percent=0.01, min_fee=5)
        self.assertEqual(result["fee_percent"], Decimal("1"))
        self.assertEqual(result["total_fee"], Decimal("5"))  # 最低5
    
    def test_fee_maximum(self):
        """测试最高手续费"""
        result = calculate_fees(10000, "USD", fee_percent=0.03, max_fee=100)
        self.assertEqual(result["fee_percent"], Decimal("300"))
        self.assertEqual(result["total_fee"], Decimal("100"))  # 最高100


class TestCentsConversion(unittest.TestCase):
    """最小单位转换测试"""
    
    def test_cents_to_amount(self):
        """测试分转元"""
        self.assertEqual(cents_to_amount(10050, "USD"), Decimal("100.50"))
        self.assertEqual(cents_to_amount(1234, "JPY"), Decimal("1234"))
    
    def test_amount_to_cents(self):
        """测试元转分"""
        self.assertEqual(amount_to_cents(100.50, "USD"), 10050)
        self.assertEqual(amount_to_cents(1234, "JPY"), 1234)
    
    def test_roundtrip(self):
        """测试往返转换"""
        original_cents = 123456
        code = "USD"
        amount = cents_to_amount(original_cents, code)
        back = amount_to_cents(amount, code)
        self.assertEqual(back, original_cents)


class TestCurrencyData(unittest.TestCase):
    """货币数据测试"""
    
    def test_all_codes_have_required_fields(self):
        """测试所有货币代码都有必需字段"""
        required_fields = ["code", "name", "symbol", "decimals"]
        for code, data in CURRENCY_DATA.items():
            for field in required_fields:
                self.assertIn(field, data, f"{code} 缺少 {field}")
    
    def test_default_rates_have_usd(self):
        """测试默认汇率包含 USD"""
        self.assertIn("USD", DEFAULT_RATES)
        self.assertEqual(DEFAULT_RATES["USD"], 1.0)


if __name__ == "__main__":
    unittest.main()