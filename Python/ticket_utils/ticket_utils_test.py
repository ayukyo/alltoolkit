"""
ticket_utils 测试文件

测试所有票据生成和解析功能
"""

import unittest
import time
from datetime import datetime

from mod import (
    TicketGenerator,
    generate_order_number,
    generate_invoice_number,
    generate_ticket_number,
    generate_refund_number,
    generate_tracking_number,
    generate_coupon_code,
    generate_batch_number,
    generate_receipt_number,
    parse_ticket_number,
    validate_luhn,
    generate_custom_ticket,
    batch_generate,
    ticket_info,
    SequentialTicketGenerator
)


class TestTicketGenerator(unittest.TestCase):
    """测试 TicketGenerator 类"""
    
    def test_generate_serial(self):
        """测试流水号格式生成"""
        gen = TicketGenerator(prefix="ORD")
        ticket = gen.generate_serial()
        
        self.assertIn("ORD-", ticket)
        self.assertIn(datetime.now().strftime("%Y%m%d"), ticket)
        # 序号应该是6位
        parts = ticket.split("-")
        self.assertEqual(len(parts[-1]), 6)
    
    def test_generate_serial_without_prefix(self):
        """测试无前缀的流水号生成"""
        gen = TicketGenerator(prefix="")
        ticket = gen.generate_serial()
        
        # 应只有日期和序号
        parts = ticket.split("-")
        self.assertEqual(len(parts), 2)
    
    def test_generate_timestamp(self):
        """测试时间戳格式生成"""
        gen = TicketGenerator(prefix="TKT")
        ticket = gen.generate_timestamp()
        
        self.assertIn("TKT-", ticket)
        # 时间戳应该是14位（YYYYMMDDHHMMSS）
        parts = ticket.split("-")
        timestamp = parts[1]
        self.assertEqual(len(timestamp), 14)
    
    def test_generate_timestamp_with_ms(self):
        """测试带毫秒的时间戳生成"""
        gen = TicketGenerator(prefix="TKT")
        ticket = gen.generate_timestamp(include_ms=True)
        
        # 时间戳应该是17位（YYYYMMDDHHMMSS + 3位毫秒）
        parts = ticket.split("-")
        timestamp = parts[1]
        self.assertEqual(len(timestamp), 17)
    
    def test_generate_timestamp_with_random_suffix(self):
        """测试带随机后缀的时间戳生成"""
        gen = TicketGenerator(prefix="TKT")
        ticket = gen.generate_timestamp(random_suffix=4)
        
        self.assertIn("TKT-", ticket)
        parts = ticket.split("-")
        # 应有随机后缀
        self.assertGreaterEqual(len(parts), 3)
    
    def test_generate_hash(self):
        """测试哈希格式生成"""
        gen = TicketGenerator(prefix="INV")
        ticket = gen.generate_hash()
        
        self.assertIn("INV-", ticket)
        # 哈希应该是8位
        parts = ticket.split("-")
        self.assertEqual(len(parts[1]), 8)
    
    def test_generate_hash_sha256(self):
        """测试 SHA256 哈希生成"""
        gen = TicketGenerator(prefix="INV")
        ticket = gen.generate_hash(algorithm="sha256", length=16)
        
        self.assertIn("INV-", ticket)
        parts = ticket.split("-")
        self.assertEqual(len(parts[1]), 16)
    
    def test_generate_snowflake_like(self):
        """测试类 Snowflake 格式生成"""
        gen = TicketGenerator(prefix="ID")
        ticket = gen.generate_snowflake_like(machine_id=1)
        
        self.assertIn("ID-", ticket)
        # 生成的应该是一个大数字ID
    
    def test_generate_luhn(self):
        """测试带 Luhn 校验位的生成"""
        gen = TicketGenerator(prefix="CARD")
        ticket = gen.generate_luhn()
        
        self.assertIn("CARD-", ticket)
        # 应有校验位
        parts = ticket.split("-")
        number = parts[1]
        self.assertTrue(validate_luhn(number))
    
    def test_generate_luhn_with_base(self):
        """测试指定基础编号的 Luhn 生成"""
        gen = TicketGenerator(prefix="CARD")
        ticket = gen.generate_luhn(base_number="1234567890")
        
        self.assertIn("CARD-", ticket)
        parts = ticket.split("-")
        number = parts[1]
        self.assertEqual(len(number), 11)  # 10位基础 + 1位校验


class TestSpecificGenerators(unittest.TestCase):
    """测试特定票据生成函数"""
    
    def test_generate_order_number(self):
        """测试订单号生成"""
        order = generate_order_number()
        
        self.assertIn("ORD-", order)
        self.assertIn(datetime.now().strftime("%Y%m%d"), order)
    
    def test_generate_order_number_with_check(self):
        """测试带校验位的订单号"""
        order = generate_order_number(include_check=True)
        
        self.assertIn("ORD-", order)
        # 应有校验位
        parts = order.split("-")
        self.assertGreaterEqual(len(parts), 4)
    
    def test_generate_invoice_number(self):
        """测试发票号生成"""
        invoice = generate_invoice_number()
        
        self.assertIn("INV-", invoice)
        # 应有年份后两位
        parts = invoice.split("-")
        year_part = parts[1]
        self.assertEqual(len(year_part), 2)
    
    def test_generate_invoice_number_specific_year(self):
        """测试指定年份的发票号"""
        invoice = generate_invoice_number(year=2025)
        
        self.assertIn("25-", invoice)
    
    def test_generate_ticket_number(self):
        """测试工单号生成"""
        ticket = generate_ticket_number()
        
        self.assertIn("TKT-", ticket)
        parts = ticket.split("-")
        self.assertGreaterEqual(len(parts), 4)
    
    def test_generate_refund_number(self):
        """测试退款单号生成"""
        refund = generate_refund_number()
        
        self.assertIn("REF-", refund)
        self.assertIn(datetime.now().strftime("%Y%m%d"), refund)
    
    def test_generate_tracking_number(self):
        """测试物流追踪号生成"""
        # 测试不同承运商
        sf = generate_tracking_number("SF")
        self.assertIn("SF", sf)
        
        yto = generate_tracking_number("YTO")
        self.assertIn("YT", yto)
        
        jd = generate_tracking_number("JD")
        self.assertIn("JD", jd)
    
    def test_generate_coupon_code(self):
        """测试优惠券码生成"""
        coupon = generate_coupon_code()
        
        self.assertIn("CPN-", coupon)
        # 优惠券码不含易混淆字符
        code_part = coupon.split("-")[1]
        self.assertNotIn("0", code_part)
        self.assertNotIn("O", code_part)
        self.assertNotIn("1", code_part)
        self.assertNotIn("I", code_part)
    
    def test_generate_batch_number(self):
        """测试批次号生成"""
        batch = generate_batch_number()
        
        self.assertIn("BAT-", batch)
        self.assertIn(datetime.now().strftime("%Y%m%d"), batch)
    
    def test_generate_receipt_number(self):
        """测试收据号生成"""
        receipt = generate_receipt_number()
        
        self.assertIn("RCP-", receipt)
        self.assertIn(datetime.now().strftime("%Y%m%d"), receipt)


class TestParsingAndValidation(unittest.TestCase):
    """测试解析和验证功能"""
    
    def test_parse_ticket_number(self):
        """测试票据编号解析"""
        order = generate_order_number()
        info = parse_ticket_number(order)
        
        self.assertTrue(info["valid"])
        self.assertEqual(info["prefix"], "ORD")
        self.assertIsNotNone(info["date"])
        self.assertIsNotNone(info["serial"])
    
    def test_parse_invoice_number(self):
        """测试发票号解析"""
        invoice = generate_invoice_number()
        info = parse_ticket_number(invoice)
        
        self.assertTrue(info["valid"])
        self.assertEqual(info["prefix"], "INV")
    
    def test_parse_complex_ticket(self):
        """测试复杂票据解析"""
        ticket = generate_ticket_number()
        info = parse_ticket_number(ticket)
        
        self.assertTrue(info["valid"])
        self.assertEqual(info["prefix"], "TKT")
        self.assertIsNotNone(info["date"])
        self.assertIsNotNone(info["time"])
    
    def test_validate_luhn_valid(self):
        """测试有效的 Luhn 校验"""
        # 已知有效的测试用例
        self.assertTrue(validate_luhn("79927398713"))  # 标准测试用例
        self.assertTrue(validate_luhn("4242424242424242"))  # 测试信用卡号
    
    def test_validate_luhn_invalid(self):
        """测试无效的 Luhn 校验"""
        self.assertFalse(validate_luhn("79927398710"))  # 修改校验位
        self.assertFalse(validate_luhn("1234567812345678"))
    
    def test_validate_luhn_non_digit(self):
        """测试非纯数字的 Luhn 校验"""
        self.assertFalse(validate_luhn("ABC123"))
        self.assertFalse(validate_luhn(""))
    
    def test_ticket_info(self):
        """测试票据信息获取"""
        order = generate_order_number()
        info = ticket_info(order)
        
        self.assertEqual(info["type"], "订单号")
        self.assertTrue(info["valid"])
        
        refund = generate_refund_number()
        info = ticket_info(refund)
        self.assertEqual(info["type"], "退款单号")


class TestCustomTicket(unittest.TestCase):
    """测试自定义票据生成"""
    
    def test_generate_custom_basic(self):
        """测试基本模板"""
        template = "{prefix}-{date}-{serial}"
        ticket = generate_custom_ticket(template, {"prefix": "TEST"})
        
        self.assertIn("TEST-", ticket)
        self.assertIn(datetime.now().strftime("%Y%m%d"), ticket)
    
    def test_generate_custom_with_rand(self):
        """测试随机变量模板"""
        template = "{prefix}-{rand:4}"
        ticket = generate_custom_ticket(template, {"prefix": "TEST"})
        
        self.assertIn("TEST-", ticket)
        # 4位随机数字
        rand_part = ticket.split("-")[1]
        self.assertEqual(len(rand_part), 4)
        self.assertTrue(rand_part.isdigit())
    
    def test_generate_custom_with_rand_alpha(self):
        """测试随机字母模板"""
        template = "{prefix}-{rand_alpha:4}"
        ticket = generate_custom_ticket(template, {"prefix": "TEST"})
        
        self.assertIn("TEST-", ticket)
        rand_part = ticket.split("-")[1]
        self.assertEqual(len(rand_part), 4)
        self.assertTrue(rand_part.isalpha())
    
    def test_generate_custom_with_rand_alnum(self):
        """测试随机字母数字模板"""
        template = "{prefix}-{rand_alnum:8}"
        ticket = generate_custom_ticket(template, {"prefix": "TEST"})
        
        self.assertIn("TEST-", ticket)
        rand_part = ticket.split("-")[1]
        self.assertEqual(len(rand_part), 8)
        self.assertTrue(rand_part.isalnum())
    
    def test_generate_custom_full(self):
        """测试完整模板"""
        template = "{prefix}-{year}{month}{day}-{time}-{rand_alnum:4}-{serial}"
        ticket = generate_custom_ticket(template, {"prefix": "ORD"})
        
        self.assertIn("ORD-", ticket)
        now = datetime.now()
        self.assertIn(now.strftime("%Y"), ticket)
        self.assertIn(now.strftime("%m"), ticket)
        self.assertIn(now.strftime("%d"), ticket)


class TestBatchGenerate(unittest.TestCase):
    """测试批量生成"""
    
    def test_batch_generate_unique(self):
        """测试批量生成（唯一）"""
        tickets = batch_generate(10, generate_order_number, unique=True)
        
        self.assertEqual(len(tickets), 10)
        # 检查唯一性
        self.assertEqual(len(set(tickets)), 10)
    
    def test_batch_generate_not_unique(self):
        """测试批量生成（不要求唯一）"""
        # 使用固定模板确保可能重复
        def fixed_gen():
            return "TEST-20250101-000001"
        
        tickets = batch_generate(5, fixed_gen, unique=False)
        
        self.assertEqual(len(tickets), 5)
        # 因为固定生成，所以所有都相同
        self.assertEqual(len(set(tickets)), 1)
    
    def test_batch_generate_with_kwargs(self):
        """测试批量生成带参数"""
        tickets = batch_generate(5, generate_invoice_number, unique=True, prefix="MYINV")
        
        self.assertEqual(len(tickets), 5)
        for t in tickets:
            self.assertIn("MYINV-", t)


class TestSequentialTicketGenerator(unittest.TestCase):
    """测试顺序票据生成器"""
    
    def test_sequential_generation(self):
        """测试顺序生成"""
        gen = SequentialTicketGenerator(prefix="SEQ")
        
        tickets = [gen.generate() for _ in range(5)]
        
        self.assertEqual(len(tickets), 5)
        # 序号应该递增
        serials = [int(t.split("-")[-1]) for t in tickets]
        self.assertEqual(serials, [1, 2, 3, 4, 5])
    
    def test_peek_next(self):
        """测试预览下一个"""
        gen = SequentialTicketGenerator(prefix="SEQ")
        
        gen.generate()  # 生成001
        peek = gen.peek_next()  # 应预览002
        actual = gen.generate()  # 应生成002
        
        # 预览和实际应该相同（但不消耗序号）
        self.assertEqual(peek, actual)
    
    def test_get_stats(self):
        """测试获取统计信息"""
        gen = SequentialTicketGenerator(prefix="SEQ", start_serial=100)
        
        for _ in range(5):
            gen.generate()
        
        stats = gen.get_stats()
        
        self.assertEqual(stats["prefix"], "SEQ")
        self.assertEqual(stats["current_serial"], 105)
        self.assertEqual(stats["generated_count"], 5)
    
    def test_reset(self):
        """测试重置"""
        gen = SequentialTicketGenerator(prefix="SEQ")
        
        for _ in range(10):
            gen.generate()
        
        gen.reset(start_serial=1)
        
        stats = gen.get_stats()
        self.assertEqual(stats["current_serial"], 1)
        self.assertEqual(stats["generated_count"], 0)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_order_flow(self):
        """测试订单流程"""
        # 生成订单
        order = generate_order_number()
        
        # 解析订单
        info = parse_ticket_number(order)
        self.assertTrue(info["valid"])
        
        # 生成退款单（关联订单）
        refund = generate_refund_number()
        info = ticket_info(refund)
        self.assertEqual(info["type"], "退款单号")
    
    def test_invoice_flow(self):
        """测试发票流程"""
        # 生成发票号
        invoice = generate_invoice_number()
        
        # 验证格式
        parts = invoice.split("-")
        self.assertEqual(parts[0], "INV")
        self.assertEqual(len(parts[1]), 2)  # 年份后两位
        self.assertEqual(len(parts[2]), 6)  # 6位序号
    
    def test_coupon_flow(self):
        """测试优惠券流程"""
        # 批量生成优惠券
        coupons = batch_generate(100, generate_coupon_code, unique=True)
        
        self.assertEqual(len(coupons), 100)
        self.assertEqual(len(set(coupons)), 100)  # 全部唯一
        
        # 检查每个优惠券不含易混淆字符
        for c in coupons:
            code = c.split("-")[1]
            self.assertNotIn("0", code)
            self.assertNotIn("O", code)


if __name__ == "__main__":
    unittest.main()