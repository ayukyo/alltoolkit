"""
AllToolkit - Invoice Utils 使用示例

展示发票创建、计算、导出等功能的使用方法。

Author: AllToolkit
License: MIT
"""

import sys
import os
from decimal import Decimal
import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from invoice_utils.mod import (
    InvoiceUtils, Invoice, InvoiceItem, PaymentRecord,
    InvoiceStatus, InvoiceType, PaymentMethod,
)


def example_basic_invoice():
    """示例1: 创建基础发票"""
    print("=" * 60)
    print("示例1: 创建基础发票")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    # 卖方信息
    seller = {
        'name': '北京示例科技有限公司',
        'address': '北京市朝阳区示例路123号',
        'tax_id': '91110105MA12345678',
        'phone': '010-12345678',
    }
    
    # 买方信息
    buyer = {
        'name': '上海客户公司',
        'address': '上海市浦东新区示例大道456号',
        'contact': '张经理',
    }
    
    # 发票项目
    items = [
        InvoiceItem(
            name="咨询服务",
            description="高级技术咨询服务",
            quantity=Decimal("2"),
            unit_price=Decimal("500"),
            unit="小时",
        ),
        InvoiceItem(
            name="产品A",
            description="软件产品",
            quantity=Decimal("10"),
            unit_price=Decimal("100"),
        ),
    ]
    
    # 创建发票
    invoice = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        due_days=30,
        notes="感谢您的支持！",
        terms="请在30天内付款",
    )
    
    # 输出信息
    print(f"\n发票编号: {invoice.number}")
    print(f"发票日期: {invoice.date}")
    print(f"到期日期: {invoice.due_date}")
    print(f"小计金额: {invoice.subtotal()} 元")
    print(f"发票总额: {invoice.total()} 元")
    print(f"当前状态: {invoice.status.value}")
    
    # 导出为文本
    print("\n" + "-" * 40)
    print("文本格式发票:")
    print("-" * 40)
    print(utils.to_text(invoice))
    
    return invoice


def example_invoice_with_tax():
    """示例2: 含税发票"""
    print("=" * 60)
    print("示例2: 含税发票（13%增值税）")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    seller = {'name': '卖方公司', 'tax_id': '123456789'}
    buyer = {'name': '买方公司'}
    
    # 含税项目
    items = [
        InvoiceItem(
            name="商品A",
            quantity=Decimal("5"),
            unit_price=Decimal("1000"),
            tax_percent=Decimal("13"),  # 13% 增值税
        ),
        InvoiceItem(
            name="商品B",
            quantity=Decimal("2"),
            unit_price=Decimal("500"),
            tax_percent=Decimal("13"),
        ),
    ]
    
    invoice = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        currency="CNY",
    )
    
    print(f"\n小计: {invoice.subtotal()} 元")
    print(f"税额: {invoice.total_tax()} 元")
    print(f"总额: {invoice.total()} 元")
    
    # 计算明细
    for item in invoice.items:
        print(f"\n{item.name}:")
        print(f"  小计: {item.subtotal()} 元")
        print(f"  税额: {item.tax_amount()} 元")
        print(f"  总计: {item.total()} 元")
    
    return invoice


def example_invoice_with_discount():
    """示例3: 折扣发票"""
    print("=" * 60)
    print("示例3: 折扣发票")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    seller = {'name': '促销商店'}
    buyer = {'name': '顾客'}
    
    # 单品折扣
    items = [
        InvoiceItem(
            name="打折商品A",
            quantity=Decimal("2"),
            unit_price=Decimal("100"),
            discount_percent=Decimal("20"),  # 20% 折扣
        ),
        InvoiceItem(
            name="打折商品B",
            quantity=Decimal("1"),
            unit_price=Decimal("200"),
            discount_percent=Decimal("10"),
        ),
    ]
    
    # 整体折扣发票
    invoice = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        overall_discount_percent=Decimal("5"),  # 额外5%整体折扣
    )
    
    print(f"\n项目小计: {invoice.subtotal()} 元")
    print(f"单品折扣总额: {sum(item.discount_amount() for item in items)} 元")
    print(f"整体折扣: {(invoice.subtotal() - sum(item.discount_amount() for item in items)) * Decimal('0.05')} 元")
    print(f"总折扣: {invoice.total_discount()} 元")
    print(f"应付金额: {invoice.total()} 元")
    
    return invoice


def example_payment_tracking():
    """示例4: 付款跟踪"""
    print("=" * 60)
    print("示例4: 付款跟踪")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    seller = {'name': '卖方'}
    buyer = {'name': '买方'}
    
    items = [
        InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("1000")),
    ]
    
    invoice = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        due_days=30,
    )
    
    print(f"\n发票总额: {invoice.total()} 元")
    print(f"初始余额: {invoice.balance_due()} 元")
    print(f"初始状态: {invoice.status.value}")
    
    # 分期付款
    print("\n--- 分期付款 ---")
    
    # 第一次付款 (微信支付)
    payment1 = utils.add_payment(
        invoice,
        amount=Decimal("300"),
        method=PaymentMethod.WECHAT,
        reference="WX123456",
    )
    print(f"付款1: 300元 (微信)")
    print(f"已付金额: {invoice.paid_amount()} 元")
    print(f"余额: {invoice.balance_due()} 元")
    print(f"状态: {invoice.status.value}")
    
    # 第二次付款 (支付宝)
    payment2 = utils.add_payment(
        invoice,
        amount=Decimal("300"),
        method=PaymentMethod.ALIPAY,
        reference="ALI789012",
    )
    print(f"\n付款2: 300元 (支付宝)")
    print(f"已付金额: {invoice.paid_amount()} 元")
    print(f"余额: {invoice.balance_due()} 元")
    print(f"状态: {invoice.status.value}")
    
    # 第三次付款 (银行转账)
    payment3 = utils.add_payment(
        invoice,
        amount=Decimal("400"),
        method=PaymentMethod.BANK_TRANSFER,
        reference="BANK20260526",
    )
    print(f"\n付款3: 400元 (银行转账)")
    print(f"已付金额: {invoice.paid_amount()} 元")
    print(f"余额: {invoice.balance_due()} 元")
    print(f"状态: {invoice.status.value}")
    print(f"是否已付清: {invoice.is_paid()}")
    
    return invoice


def example_overdue_invoice():
    """示例5: 过期发票与滞纳金"""
    print("=" * 60)
    print("示例5: 过期发票与滞纳金")
    print("=" * 60)
    
    seller = {'name': '卖方'}
    buyer = {'name': '买方'}
    
    items = [
        InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("1000")),
    ]
    
    # 创建一个已过期的发票
    invoice = Invoice(
        number="INV-OVERDUE-001",
        date=datetime.date(2026, 4, 1),  # 4月1日
        due_date=datetime.date(2026, 4, 30),  # 4月30日到期
        seller=seller,
        buyer=buyer,
        items=items,
        late_fee_percent=Decimal("0.5"),  # 每天滞纳金率 0.5%
    )
    
    # 检查5月26日的状态
    check_date = datetime.date(2026, 5, 26)
    
    print(f"\n发票日期: {invoice.date}")
    print(f"到期日期: {invoice.due_date}")
    print(f"检查日期: {check_date}")
    print(f"是否过期: {invoice.is_overdue(check_date)}")
    print(f"过期天数: {invoice.days_overdue(check_date)} 天")
    print(f"发票总额: {invoice.total()} 元")
    print(f"滞纳金: {invoice.late_fee(check_date)} 元")
    print(f"应付总计: {invoice.total() + invoice.late_fee(check_date)} 元")
    
    return invoice


def example_multiple_invoice_types():
    """示例6: 多种发票类型"""
    print("=" * 60)
    print("示例6: 多种发票类型")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    seller = {'name': '公司'}
    buyer = {'name': '客户'}
    items = [InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))]
    
    # 标准发票
    invoice_standard = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.STANDARD,
    )
    print(f"\n标准发票: {invoice_standard.number}")
    print(f"类型: {invoice_standard.invoice_type.value}")
    
    # 形式发票（报价单性质的预发票）
    invoice_proforma = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.PROFORMA,
    )
    print(f"\n形式发票: {invoice_proforma.number}")
    print(f"类型: {invoice_proforma.invoice_type.value}")
    
    # 报价单
    invoice_quote = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.QUOTE,
    )
    print(f"\n报价单: {invoice_quote.number}")
    print(f"类型: {invoice_quote.invoice_type.value}")
    
    # 贷记单（退款/退货）
    invoice_credit = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.CREDIT_NOTE,
    )
    print(f"\n贷记单: {invoice_credit.number}")
    print(f"类型: {invoice_credit.invoice_type.value}")


def example_markdown_export():
    """示例7: Markdown导出"""
    print("=" * 60)
    print("示例7: Markdown格式导出")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    seller = {
        'name': '北京示例科技有限公司',
        'address': '北京市朝阳区示例路123号',
        'tax_id': '91110105MA12345678',
    }
    
    buyer = {
        'name': '上海客户公司',
        'address': '上海市浦东新区示例大道456号',
    }
    
    items = [
        InvoiceItem(
            name="咨询服务",
            quantity=Decimal("2"),
            unit_price=Decimal("500"),
            unit="小时",
            tax_percent=Decimal("13"),
        ),
        InvoiceItem(
            name="产品A",
            quantity=Decimal("10"),
            unit_price=Decimal("100"),
        ),
    ]
    
    invoice = utils.create_invoice(
        seller=seller,
        buyer=buyer,
        items=items,
        notes="感谢您的支持！",
    )
    
    # 添加付款
    utils.add_payment(invoice, Decimal("500"), PaymentMethod.WECHAT)
    
    print("\nMarkdown格式发票:")
    print(utils.to_markdown(invoice))


def example_tax_inclusive():
    """示例8: 含税价格发票"""
    print("=" * 60)
    print("示例8: 含税价格发票")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    seller = {'name': '卖方'}
    buyer = {'name': '买方'}
    
    # 含税价格（税已包含在单价中）
    items = [
        InvoiceItem(
            name="含税商品",
            quantity=Decimal("1"),
            unit_price=Decimal("113"),  # 含13%税
            tax_percent=Decimal("13"),
        ),
    ]
    
    # 税内含模式
    invoice_inclusive = Invoice(
        number="INV-TAX-INCLUSIVE",
        date=datetime.date.today(),
        due_date=datetime.date.today() + datetime.timedelta(days=30),
        seller=seller,
        buyer=buyer,
        items=items,
        tax_inclusive=True,  # 税内含
    )
    
    print(f"\n含税价格模式:")
    print(f"单价: {items[0].unit_price} 元（含税）")
    print(f"税额: {invoice_inclusive.total_tax()} 元（已包含）")
    print(f"总额: {invoice_inclusive.total()} 元")
    
    # 税外加模式
    invoice_exclusive = Invoice(
        number="INV-TAX-EXCLUSIVE",
        date=datetime.date.today(),
        due_date=datetime.date.today() + datetime.timedelta(days=30),
        seller=seller,
        buyer=buyer,
        items=[InvoiceItem(name="不含税商品", quantity=Decimal("1"), unit_price=Decimal("100"), tax_percent=Decimal("13"))],
        tax_inclusive=False,
    )
    
    print(f"\n不含税价格模式:")
    print(f"单价: {Decimal('100')} 元（不含税）")
    print(f"税额: {invoice_exclusive.total_tax()} 元")
    print(f"总额: {invoice_exclusive.total()} 元")


def example_validation():
    """示例9: 发票验证"""
    print("=" * 60)
    print("示例9: 发票验证")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    # 有效发票
    valid_invoice = Invoice(
        number="INV-VALID-001",
        date=datetime.date.today(),
        due_date=datetime.date.today() + datetime.timedelta(days=30),
        seller={'name': '卖方公司'},
        buyer={'name': '买方公司'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    errors = utils.validate_invoice(valid_invoice)
    print(f"\n有效发票验证结果: {len(errors)} 个错误")
    if errors:
        for err in errors:
            print(f"  - {err}")
    else:
        print("  ✓ 发票有效")
    
    # 无效发票（缺少信息）
    invalid_invoice = Invoice(
        number="",  # 缺少编号
        date=datetime.date.today(),
        due_date=datetime.date.today() - datetime.timedelta(days=1),  # 到期日在发票日期之前
        seller={},  # 缺少卖方
        buyer={},  # 缺少买方
        items=[],  # 缺少项目
    )
    
    errors = utils.validate_invoice(invalid_invoice)
    print(f"\n无效发票验证结果: {len(errors)} 个错误")
    for err in errors:
        print(f"  - {err}")


def example_due_date_calculation():
    """示例10: 到期日计算"""
    print("=" * 60)
    print("示例10: 到期日计算")
    print("=" * 60)
    
    utils = InvoiceUtils()
    invoice_date = datetime.date(2026, 5, 26)
    
    terms = ["net30", "net15", "net45", "net60", "eom"]
    
    print(f"\n发票日期: {invoice_date}")
    print("\n付款条款对应的到期日:")
    
    for term in terms:
        due_date = utils.calculate_due_date(invoice_date, term)
        desc_zh = utils.payment_terms_description(term, "zh")
        desc_en = utils.payment_terms_description(term, "en")
        print(f"  {term}: {due_date} ({desc_zh})")


def example_tax_rates():
    """示例11: 常见税率"""
    print("=" * 60)
    print("示例11: 各地区常见税率")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    regions = ['CN', 'EU', 'UK', 'JP', 'AU', 'IN', 'SG', 'HK']
    
    print("\n常见税率:")
    for region in regions:
        rate = utils.get_tax_rate(region)
        print(f"  {region}: {rate}%")
    
    # 计算税额示例
    print("\n税额计算示例 (1000元):")
    for region in ['CN', 'EU', 'HK']:
        rate = utils.get_tax_rate(region) * 100
        tax, net = utils.calculate_tax(Decimal("1000"), rate)
        print(f"  {region} ({rate}%): 税额 {tax} 元, 净额 {net} 元")


def example_invoice_stats():
    """示例12: 发票统计"""
    print("=" * 60)
    print("示例12: 发票统计")
    print("=" * 60)
    
    utils = InvoiceUtils()
    
    # 创建多张发票
    invoices = []
    
    seller = {'name': '公司'}
    buyer = {'name': '客户'}
    
    for i in range(5):
        invoice = Invoice(
            number=f"INV-{i+1:03d}",
            date=datetime.date(2026, 5, 1) + datetime.timedelta(days=i*5),
            due_date=datetime.date(2026, 6, 1),
            seller=seller,
            buyer=buyer,
            items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal(f"{(i+1)*100}"))],
        )
        invoices.append(invoice)
    
    # 添加付款
    invoices[0].payments.append(PaymentRecord(datetime.date(2026, 5, 5), Decimal("100"), PaymentMethod.CASH))
    invoices[0].update_status()
    
    invoices[1].payments.append(PaymentRecord(datetime.date(2026, 5, 10), Decimal("200"), PaymentMethod.WECHAT))
    invoices[1].update_status()
    
    invoices[2].payments.append(PaymentRecord(datetime.date(2026, 5, 15), Decimal("150"), PaymentMethod.ALIPAY))
    invoices[2].payments.append(PaymentRecord(datetime.date(2026, 5, 20), Decimal("150"), PaymentMethod.BANK_TRANSFER))
    invoices[2].update_status()
    
    # 计算统计
    stats = utils.invoice_stats(invoices)
    
    print(f"\n发票统计:")
    print(f"  发票数量: {stats['count']} 张")
    print(f"  总金额: {stats['total_amount']} 元")
    print(f"  已付金额: {stats['total_paid']} 元")
    print(f"  未付余额: {stats['total_balance']} 元")
    print(f"  平均金额: {stats['avg_amount']} 元")
    print(f"  已付款率: {stats['paid_rate']*100:.1f}%")
    print(f"\n状态分布:")
    for status, count in stats['by_status'].items():
        if count > 0:
            print(f"  {status}: {count} 张")


def run_all_examples():
    """运行所有示例"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "AllToolkit Invoice Utils 示例" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    example_basic_invoice()
    example_invoice_with_tax()
    example_invoice_with_discount()
    example_payment_tracking()
    example_overdue_invoice()
    example_multiple_invoice_types()
    example_markdown_export()
    example_tax_inclusive()
    example_validation()
    example_due_date_calculation()
    example_tax_rates()
    example_invoice_stats()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()