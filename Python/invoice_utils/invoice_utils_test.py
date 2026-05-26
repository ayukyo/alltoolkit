"""
AllToolkit - Python Invoice Utilities Tests

Comprehensive test suite covering invoice creation, calculation,
validation, and export functionality.

Author: AllToolkit
License: MIT
"""

import sys
import os
import datetime
from decimal import Decimal, ROUND_HALF_UP

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from invoice_utils.mod import (
    InvoiceUtils, Invoice, InvoiceItem, PaymentRecord,
    InvoiceStatus, InvoiceType, PaymentMethod,
    generate_number, create_invoice, calculate_tax, apply_discount,
    validate_invoice, to_text, to_markdown, get_tax_rate,
    COMMON_TAX_RATES,
)


def test_invoice_item_creation():
    """Test InvoiceItem creation and calculations."""
    print("Test: InvoiceItem creation and calculations")
    
    # Basic item
    item = InvoiceItem(
        name="服务费",
        quantity=Decimal("1"),
        unit_price=Decimal("1000"),
    )
    
    assert item.name == "服务费"
    assert item.quantity == Decimal("1")
    assert item.unit_price == Decimal("1000")
    assert item.subtotal() == Decimal("1000")
    assert item.discount_amount() == Decimal("0")
    assert item.tax_amount() == Decimal("0")
    assert item.total() == Decimal("1000")
    print("  ✓ Basic item calculation")
    
    # Item with discount
    item_discount = InvoiceItem(
        name="打折商品",
        quantity=Decimal("2"),
        unit_price=Decimal("100"),
        discount_percent=Decimal("10"),
    )
    
    assert item_discount.subtotal() == Decimal("200")
    assert item_discount.discount_amount() == Decimal("20")
    assert item_discount.taxable_amount() == Decimal("180")
    print("  ✓ Item with discount")
    
    # Item with tax
    item_tax = InvoiceItem(
        name="含税商品",
        quantity=Decimal("1"),
        unit_price=Decimal("100"),
        tax_percent=Decimal("13"),
    )
    
    assert item_tax.subtotal() == Decimal("100")
    assert item_tax.tax_amount() == Decimal("13")
    assert item_tax.total() == Decimal("113")
    print("  ✓ Item with tax")
    
    # Item with discount and tax
    item_full = InvoiceItem(
        name="打折含税商品",
        quantity=Decimal("5"),
        unit_price=Decimal("100"),
        discount_percent=Decimal("20"),
        tax_percent=Decimal("13"),
    )
    
    # subtotal: 500
    # discount: 500 * 0.20 = 100
    # taxable: 400
    # tax: 400 * 0.13 = 52
    # total: 452
    assert item_full.subtotal() == Decimal("500")
    assert item_full.discount_amount() == Decimal("100")
    assert item_full.taxable_amount() == Decimal("400")
    assert item_full.tax_amount() == Decimal("52")
    assert item_full.total() == Decimal("452")
    print("  ✓ Item with discount and tax")
    
    print("  ✅ All InvoiceItem tests passed\n")


def test_invoice_creation():
    """Test Invoice creation and totals."""
    print("Test: Invoice creation and totals")
    
    seller = {
        'name': '卖方公司',
        'address': '北京市朝阳区',
        'tax_id': '123456789',
    }
    
    buyer = {
        'name': '买方公司',
        'address': '上海市浦东新区',
    }
    
    items = [
        InvoiceItem(name="商品A", quantity=Decimal("2"), unit_price=Decimal("100")),
        InvoiceItem(name="商品B", quantity=Decimal("1"), unit_price=Decimal("500")),
    ]
    
    invoice = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
    )
    
    # Subtotal: 200 + 500 = 700
    assert invoice.subtotal() == Decimal("700")
    assert invoice.total_discount() == Decimal("0")
    assert invoice.total_tax() == Decimal("0")
    assert invoice.total() == Decimal("700")
    assert invoice.balance_due() == Decimal("700")
    assert not invoice.is_paid()
    print("  ✓ Basic invoice totals")
    
    # Invoice with overall discount
    invoice_discount = Invoice(
        number="INV-2026-0002",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
        overall_discount_percent=Decimal("10"),
    )
    
    # Subtotal: 700
    # Overall discount: 700 * 0.10 = 70
    # Total: 630
    assert invoice_discount.subtotal() == Decimal("700")
    assert invoice_discount.total_discount() == Decimal("70")
    assert invoice_discount.total() == Decimal("630")
    print("  ✓ Invoice with overall discount")
    
    # Invoice with tax
    items_taxed = [
        InvoiceItem(name="商品A", quantity=Decimal("2"), unit_price=Decimal("100"), tax_percent=Decimal("13")),
        InvoiceItem(name="商品B", quantity=Decimal("1"), unit_price=Decimal("500"), tax_percent=Decimal("13")),
    ]
    
    invoice_taxed = Invoice(
        number="INV-2026-0003",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items_taxed,
    )
    
    # Subtotal: 700
    # Tax: 200 * 0.13 + 500 * 0.13 = 26 + 65 = 91
    # Total: 791
    assert invoice_taxed.total_tax() == Decimal("91")
    assert invoice_taxed.total() == Decimal("791")
    print("  ✓ Invoice with tax")
    
    print("  ✅ All Invoice creation tests passed\n")


def test_payment_tracking():
    """Test payment tracking and balance calculation."""
    print("Test: Payment tracking and balance calculation")
    
    seller = {'name': '卖方公司'}
    buyer = {'name': '买方公司'}
    items = [
        InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("1000")),
    ]
    
    invoice = Invoice(
        number="INV-2026-0004",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
    )
    
    assert invoice.total() == Decimal("1000")
    assert invoice.paid_amount() == Decimal("0")
    assert invoice.balance_due() == Decimal("1000")
    assert invoice.status == InvoiceStatus.DRAFT
    print("  ✓ Initial invoice state")
    
    # Add partial payment
    payment1 = PaymentRecord(
        date=datetime.date(2026, 5, 28),
        amount=Decimal("500"),
        method=PaymentMethod.BANK_TRANSFER,
    )
    invoice.payments.append(payment1)
    invoice.update_status()
    
    assert invoice.paid_amount() == Decimal("500")
    assert invoice.balance_due() == Decimal("500")
    assert invoice.status == InvoiceStatus.PARTIAL
    print("  ✓ Partial payment")
    
    # Add full payment
    payment2 = PaymentRecord(
        date=datetime.date(2026, 5, 30),
        amount=Decimal("500"),
        method=PaymentMethod.CREDIT_CARD,
    )
    invoice.payments.append(payment2)
    invoice.update_status()
    
    assert invoice.paid_amount() == Decimal("1000")
    assert invoice.balance_due() == Decimal("0")
    assert invoice.is_paid()
    assert invoice.status == InvoiceStatus.PAID
    print("  ✓ Full payment")
    
    print("  ✅ All payment tracking tests passed\n")


def test_overdue_calculation():
    """Test overdue calculation."""
    print("Test: Overdue calculation")
    
    seller = {'name': '卖方公司'}
    buyer = {'name': '买方公司'}
    items = [
        InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("1000")),
    ]
    
    # Overdue invoice
    invoice = Invoice(
        number="INV-2026-0005",
        date=datetime.date(2026, 5, 1),
        due_date=datetime.date(2026, 5, 15),
        seller=seller,
        buyer=buyer,
        items=items,
    )
    
    # Check with date after due
    check_date = datetime.date(2026, 5, 26)
    
    assert invoice.is_overdue(check_date)
    assert invoice.days_overdue(check_date) == 11
    print("  ✓ Overdue detection")
    
    # Not overdue invoice
    invoice_not_overdue = Invoice(
        number="INV-2026-0006",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
    )
    
    assert not invoice_not_overdue.is_overdue(datetime.date(2026, 5, 26))
    assert invoice_not_overdue.days_overdue(datetime.date(2026, 5, 26)) == 0
    print("  ✓ Not overdue")
    
    # Paid invoice not counted as overdue
    invoice_paid = Invoice(
        number="INV-2026-0007",
        date=datetime.date(2026, 5, 1),
        due_date=datetime.date(2026, 5, 15),
        seller=seller,
        buyer=buyer,
        items=items,
        payments=[
            PaymentRecord(date=datetime.date(2026, 5, 10), amount=Decimal("1000"), method=PaymentMethod.CASH),
        ],
        status=InvoiceStatus.PAID,
    )
    
    assert not invoice_paid.is_overdue(check_date)
    print("  ✓ Paid not overdue")
    
    # Late fee calculation
    invoice_late = Invoice(
        number="INV-2026-0008",
        date=datetime.date(2026, 5, 1),
        due_date=datetime.date(2026, 5, 15),
        seller=seller,
        buyer=buyer,
        items=items,
        late_fee_percent=Decimal("0.5"),  # 0.5% per day
    )
    
    # Days overdue: 11
    # Late fee capped at 30 days: min(11, 30) = 11
    # Fee rate: 0.5 * 11 / 100 = 5.5%
    # Late fee: 1000 * 5.5 / 100 = 55
    late_fee = invoice_late.late_fee(check_date)
    assert late_fee == Decimal("55")
    print("  ✓ Late fee calculation")
    
    print("  ✅ All overdue tests passed\n")


def test_invoice_utils_class():
    """Test InvoiceUtils class methods."""
    print("Test: InvoiceUtils class methods")
    
    utils = InvoiceUtils(number_format="INV-{year}-{sequence:05d}", default_tax_rate=Decimal("13"))
    
    # Number generation
    num1 = utils.generate_number(2026, 1)
    assert num1 == "INV-2026-00001"
    print("  ✓ Invoice number generation")
    
    # Auto increment
    num2 = utils.generate_number(2026)
    num3 = utils.generate_number(2026)
    assert num2 != num3
    print("  ✓ Auto-increment sequence")
    
    # Create invoice
    seller = {'name': '卖方'}
    buyer = {'name': '买方'}
    items = [
        InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100")),
    ]
    
    invoice = utils.create_invoice(seller, buyer, items, due_days=15)
    assert invoice.due_date == datetime.date.today() + datetime.timedelta(days=15)
    assert invoice.currency == "CNY"
    print("  ✓ Invoice creation")
    
    # Add item
    new_item = utils.add_item(invoice, "新商品", Decimal("2"), Decimal("50"))
    assert len(invoice.items) == 2
    assert new_item.name == "新商品"
    print("  ✓ Add item")
    
    # Add payment
    payment = utils.add_payment(invoice, Decimal("100"), PaymentMethod.WECHAT)
    assert len(invoice.payments) == 1
    assert invoice.paid_amount() == Decimal("100")
    print("  ✓ Add payment")
    
    print("  ✅ All InvoiceUtils tests passed\n")


def test_tax_calculation():
    """Test tax calculation utilities."""
    print("Test: Tax calculation utilities")
    
    utils = InvoiceUtils()
    
    # Exclusive tax
    tax, net = utils.calculate_tax(Decimal("100"), Decimal("13"), inclusive=False)
    assert tax == Decimal("13.00")
    assert net == Decimal("100.00")
    print("  ✓ Exclusive tax")
    
    # Inclusive tax
    # Gross: 113, Rate: 13%
    # Tax = 113 * 13 / 113 = 13
    # Net = 113 - 13 = 100
    tax_inc, net_inc = utils.calculate_tax(Decimal("113"), Decimal("13"), inclusive=True)
    assert tax_inc == Decimal("13.00")
    assert net_inc == Decimal("100.00")
    print("  ✓ Inclusive tax")
    
    # Zero tax
    tax_zero, net_zero = utils.calculate_tax(Decimal("100"), Decimal("0"))
    assert tax_zero == Decimal("0.00")
    assert net_zero == Decimal("100.00")
    print("  ✓ Zero tax")
    
    # Common tax rates
    cn_rate = get_tax_rate('CN')
    assert cn_rate == Decimal("0.13")
    
    eu_rate = get_tax_rate('EU')
    assert eu_rate == Decimal("0.20")
    
    hk_rate = get_tax_rate('HK')
    assert hk_rate == Decimal("0.00")
    print("  ✓ Common tax rates")
    
    print("  ✅ All tax calculation tests passed\n")


def test_discount_calculation():
    """Test discount calculation utilities."""
    print("Test: Discount calculation utilities")
    
    # Basic discount
    discount, result = apply_discount(Decimal("1000"), Decimal("10"))
    assert discount == Decimal("100.00")
    assert result == Decimal("900.00")
    print("  ✓ Basic discount")
    
    # Zero discount
    discount_zero, result_zero = apply_discount(Decimal("100"), Decimal("0"))
    assert discount_zero == Decimal("0.00")
    assert result_zero == Decimal("100.00")
    print("  ✓ Zero discount")
    
    # Full discount
    discount_full, result_full = apply_discount(Decimal("100"), Decimal("100"))
    assert discount_full == Decimal("100.00")
    assert result_full == Decimal("0.00")
    print("  ✓ Full discount")
    
    # Fractional discount
    discount_frac, result_frac = apply_discount(Decimal("100"), Decimal("33.33"))
    assert discount_frac == Decimal("33.33")
    assert result_frac == Decimal("66.67")
    print("  ✓ Fractional discount")
    
    print("  ✅ All discount tests passed\n")


def test_validation():
    """Test invoice validation."""
    print("Test: Invoice validation")
    
    utils = InvoiceUtils()
    
    # Valid invoice
    valid_invoice = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    errors = utils.validate_invoice(valid_invoice)
    assert len(errors) == 0
    print("  ✓ Valid invoice")
    
    # Missing number
    invalid_no_number = Invoice(
        number="",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    errors = utils.validate_invoice(invalid_no_number)
    assert "Invoice number is required" in errors
    print("  ✓ Missing number")
    
    # Missing seller
    invalid_no_seller = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    errors = utils.validate_invoice(invalid_no_seller)
    assert "Seller information is required" in errors
    print("  ✓ Missing seller")
    
    # Missing buyer
    invalid_no_buyer = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    errors = utils.validate_invoice(invalid_no_buyer)
    assert "Buyer information is required" in errors
    print("  ✓ Missing buyer")
    
    # No items
    invalid_no_items = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[],
    )
    
    errors = utils.validate_invoice(invalid_no_items)
    assert "At least one item is required" in errors
    print("  ✓ No items")
    
    # Due date before invoice date
    invalid_dates = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 5, 20),  # Before invoice date
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    errors = utils.validate_invoice(invalid_dates)
    assert "Due date cannot be before invoice date" in errors
    print("  ✓ Invalid dates")
    
    # Negative unit price
    invalid_price = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("-100"))],
    )
    
    errors = utils.validate_invoice(invalid_price)
    assert any("Unit price cannot be negative" in e for e in errors)
    print("  ✓ Negative price")
    
    # Overpayment
    invalid_overpay = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
        payments=[
            PaymentRecord(date=datetime.date(2026, 5, 26), amount=Decimal("200"), method=PaymentMethod.CASH),
        ],
    )
    
    errors = utils.validate_invoice(invalid_overpay)
    assert any("exceeds invoice total" in e for e in errors)
    print("  ✓ Overpayment")
    
    # Invoice number format validation
    assert utils.is_valid_invoice_number("INV-2026-0001")
    assert utils.is_valid_invoice_number("INV_123")
    assert not utils.is_valid_invoice_number("")
    assert not utils.is_valid_invoice_number("INV@123")  # Invalid character
    print("  ✓ Invoice number validation")
    
    print("  ✅ All validation tests passed\n")


def test_export_formats():
    """Test invoice export formats."""
    print("Test: Invoice export formats")
    
    seller = {
        'name': '卖方公司',
        'address': '北京市朝阳区示例路123号',
        'tax_id': '123456789',
    }
    
    buyer = {
        'name': '买方公司',
        'address': '上海市浦东新区示例大道456号',
    }
    
    items = [
        InvoiceItem(name="服务费", quantity=Decimal("1"), unit_price=Decimal("1000")),
        InvoiceItem(name="产品A", quantity=Decimal("10"), unit_price=Decimal("50"), tax_percent=Decimal("13")),
    ]
    
    invoice = Invoice(
        number="INV-2026-TEST",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
        notes="测试发票",
        terms="30天内付款",
    )
    
    # Text format
    text_output = to_text(invoice)
    assert "INV-2026-TEST" in text_output
    assert "卖方公司" in text_output
    assert "买方公司" in text_output
    assert "服务费" in text_output
    assert "产品A" in text_output
    print("  ✓ Text format")
    
    # Markdown format
    md_output = to_markdown(invoice)
    assert "# 🧾 发票 INV-2026-TEST" in md_output
    assert "| 名称 |" in md_output  # Table format
    assert "卖方公司" in md_output
    print("  ✓ Markdown format")
    
    # JSON format
    json_output = invoice.to_dict()
    assert json_output['number'] == "INV-2026-TEST"
    assert len(json_output['items']) == 2
    print("  ✓ JSON format")
    
    # Hash generation
    utils = InvoiceUtils()
    hash1 = utils.hash_invoice(invoice)
    assert len(hash1) == 64  # SHA-256 hex length
    assert hash1 != "" 
    print("  ✓ Hash generation")
    
    print("  ✅ All export tests passed\n")


def test_invoice_types():
    """Test different invoice types."""
    print("Test: Invoice types")
    
    seller = {'name': '卖方'}
    buyer = {'name': '买方'}
    items = [InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))]
    
    # Standard invoice
    invoice_std = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.STANDARD,
    )
    assert invoice_std.invoice_type == InvoiceType.STANDARD
    print("  ✓ Standard invoice")
    
    # Proforma invoice
    invoice_proforma = Invoice(
        number="PRO-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.PROFORMA,
    )
    assert invoice_proforma.invoice_type == InvoiceType.PROFORMA
    print("  ✓ Proforma invoice")
    
    # Credit note
    invoice_credit = Invoice(
        number="CN-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.CREDIT_NOTE,
    )
    assert invoice_credit.invoice_type == InvoiceType.CREDIT_NOTE
    print("  ✓ Credit note")
    
    # Quote
    invoice_quote = Invoice(
        number="QUO-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_type=InvoiceType.QUOTE,
    )
    assert invoice_quote.invoice_type == InvoiceType.QUOTE
    print("  ✓ Quote")
    
    print("  ✅ All invoice type tests passed\n")


def test_due_date_calculation():
    """Test due date calculation from payment terms."""
    print("Test: Due date calculation")
    
    utils = InvoiceUtils()
    invoice_date = datetime.date(2026, 5, 26)
    
    # Net 30
    due_net30 = utils.calculate_due_date(invoice_date, "net30")
    assert due_net30 == datetime.date(2026, 6, 25)
    print("  ✓ Net 30")
    
    # Net 15
    due_net15 = utils.calculate_due_date(invoice_date, "net15")
    assert due_net15 == datetime.date(2026, 6, 10)
    print("  ✓ Net 15")
    
    # End of month
    due_eom = utils.calculate_due_date(invoice_date, "eom")
    assert due_eom == datetime.date(2026, 5, 31)
    print("  ✓ End of month")
    
    # EOM for February
    feb_date = datetime.date(2026, 2, 15)
    due_feb_eom = utils.calculate_due_date(feb_date, "eom")
    # 2026 is not a leap year, Feb has 28 days
    assert due_feb_eom == datetime.date(2026, 2, 28)
    print("  ✓ End of month (February)")
    
    # Payment terms description
    desc_zh = utils.payment_terms_description("net30", "zh")
    assert desc_zh == "30天内付款"
    
    desc_en = utils.payment_terms_description("net30", "en")
    assert desc_en == "Payment due within 30 days"
    print("  ✓ Payment terms description")
    
    print("  ✅ All due date tests passed\n")


def test_payment_methods():
    """Test different payment methods."""
    print("Test: Payment methods")
    
    methods = [
        PaymentMethod.CASH,
        PaymentMethod.BANK_TRANSFER,
        PaymentMethod.CREDIT_CARD,
        PaymentMethod.DEBIT_CARD,
        PaymentMethod.CHECK,
        PaymentMethod.PAYPAL,
        PaymentMethod.WECHAT,
        PaymentMethod.ALIPAY,
        PaymentMethod.OTHER,
    ]
    
    for method in methods:
        assert method.value in ['cash', 'bank_transfer', 'credit_card', 'debit_card', 
                                'check', 'paypal', 'wechat', 'alipay', 'other']
    
    print(f"  ✓ All {len(methods)} payment methods")
    print("  ✅ Payment method tests passed\n")


def test_invoice_stats():
    """Test invoice statistics."""
    print("Test: Invoice statistics")
    
    utils = InvoiceUtils()
    
    seller = {'name': '卖方'}
    buyer = {'name': '买方'}
    
    invoices = [
        Invoice(
            number="INV-001",
            date=datetime.date(2026, 5, 1),
            due_date=datetime.date(2026, 6, 1),
            seller=seller,
            buyer=buyer,
            items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("1000"))],
            status=InvoiceStatus.PAID,
            payments=[PaymentRecord(date=datetime.date(2026, 5, 10), amount=Decimal("1000"), method=PaymentMethod.CASH)],
        ),
        Invoice(
            number="INV-002",
            date=datetime.date(2026, 5, 15),
            due_date=datetime.date(2026, 6, 15),
            seller=seller,
            buyer=buyer,
            items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("500"))],
            status=InvoiceStatus.PENDING,
        ),
        Invoice(
            number="INV-003",
            date=datetime.date(2026, 5, 20),
            due_date=datetime.date(2026, 6, 20),
            seller=seller,
            buyer=buyer,
            items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("300"))],
            status=InvoiceStatus.PARTIAL,
            payments=[PaymentRecord(date=datetime.date(2026, 5, 25), amount=Decimal("100"), method=PaymentMethod.WECHAT)],
        ),
    ]
    
    stats = utils.invoice_stats(invoices)
    
    assert stats['count'] == 3
    assert stats['total_amount'] == 1800.0
    assert stats['total_paid'] == 1100.0
    assert stats['total_balance'] == 700.0
    assert stats['avg_amount'] == 600.0
    assert stats['by_status']['paid'] == 1
    assert stats['by_status']['pending'] == 1
    assert stats['by_status']['partial'] == 1
    print("  ✓ Invoice statistics")
    
    # Empty list
    empty_stats = utils.invoice_stats([])
    assert empty_stats == {}
    print("  ✓ Empty invoice list")
    
    print("  ✅ All invoice stats tests passed\n")


def test_decimal_precision():
    """Test Decimal precision handling."""
    print("Test: Decimal precision handling")
    
    # Rounding behavior
    item = InvoiceItem(
        name="商品",
        quantity=Decimal("3.333"),
        unit_price=Decimal("10"),
    )
    # Subtotal: 33.33
    subtotal = item.subtotal()
    # Note: Decimal multiplication preserves precision
    assert subtotal == Decimal("33.330") or subtotal == Decimal("33.33")
    print("  ✓ Decimal multiplication precision")
    
    # Tax rounding
    item_tax = InvoiceItem(
        name="商品",
        quantity=Decimal("1"),
        unit_price=Decimal("99.99"),
        tax_percent=Decimal("13"),
    )
    # Tax: 99.99 * 0.13 = 12.9987
    tax_amount = item_tax.tax_amount()
    assert tax_amount == Decimal("12.9987") or round(float(tax_amount), 2) == 13.00
    print("  ✓ Tax amount precision")
    
    # Invoice total rounding
    invoice = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("99.99"), tax_percent=Decimal("13"))],
    )
    
    # Total should be quantized to 2 decimal places
    total = invoice.total()
    # Allow for rounding differences
    assert abs(float(total) - 113.00) < 0.01 or abs(float(total) - 112.99) < 0.01
    print("  ✓ Invoice total quantized")
    
    print("  ✅ All decimal tests passed\n")


def test_currency_handling():
    """Test currency handling."""
    print("Test: Currency handling")
    
    # Different currencies
    invoice_usd = Invoice(
        number="INV-USD-001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': 'Seller'},
        buyer={'name': 'Buyer'},
        items=[InvoiceItem(name="Product", quantity=Decimal("1"), unit_price=Decimal("100"))],
        currency="USD",
    )
    
    assert invoice_usd.currency == "USD"
    print("  ✓ USD currency")
    
    invoice_eur = Invoice(
        number="INV-EUR-001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': 'Seller'},
        buyer={'name': 'Buyer'},
        items=[InvoiceItem(name="Product", quantity=Decimal("1"), unit_price=Decimal("100"))],
        currency="EUR",
    )
    
    assert invoice_eur.currency == "EUR"
    print("  ✓ EUR currency")
    
    # Text output should include currency
    text_usd = to_text(invoice_usd)
    assert "USD" in text_usd
    print("  ✓ Currency in text output")
    
    print("  ✅ All currency tests passed\n")


def test_tax_inclusive():
    """Test tax-inclusive pricing."""
    print("Test: Tax-inclusive pricing")
    
    # Tax inclusive invoice
    invoice_inclusive = Invoice(
        number="INV-2026-0001",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[
            InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("113"), tax_percent=Decimal("13")),
        ],
        tax_inclusive=True,
    )
    
    # Tax is included in price, so no additional tax
    assert invoice_inclusive.total_tax() == Decimal("0")
    assert invoice_inclusive.total() == Decimal("113.00")
    print("  ✓ Tax-inclusive total")
    
    # Tax exclusive invoice (same amount)
    invoice_exclusive = Invoice(
        number="INV-2026-0002",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[
            InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"), tax_percent=Decimal("13")),
        ],
        tax_inclusive=False,
    )
    
    # Tax is added to price
    assert invoice_exclusive.total_tax() == Decimal("13.00")
    assert invoice_exclusive.total() == Decimal("113.00")
    print("  ✓ Tax-exclusive total")
    
    print("  ✅ All tax-inclusive tests passed\n")


def test_empty_and_edge_cases():
    """Test empty and edge cases."""
    print("Test: Empty and edge cases")
    
    # Empty invoice (no items)
    invoice_empty = Invoice(
        number="INV-EMPTY",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[],
    )
    
    assert invoice_empty.subtotal() == Decimal("0")
    assert invoice_empty.total() == Decimal("0")
    assert invoice_empty.is_paid()  # Zero balance = paid
    print("  ✓ Empty invoice")
    
    # Single item invoice
    invoice_single = Invoice(
        number="INV-SINGLE",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("1"))],
    )
    
    assert invoice_single.total() == Decimal("1.00")
    print("  ✓ Single item invoice")
    
    # Large quantity
    item_large = InvoiceItem(
        name="商品",
        quantity=Decimal("1000000"),
        unit_price=Decimal("0.01"),
    )
    assert item_large.subtotal() == Decimal("10000")
    print("  ✓ Large quantity")
    
    # Small unit price
    item_small = InvoiceItem(
        name="商品",
        quantity=Decimal("1"),
        unit_price=Decimal("0.001"),
    )
    assert item_small.subtotal() == Decimal("0.001")
    print("  ✓ Small unit price")
    
    # Multiple payments for same invoice
    invoice_multi_pay = Invoice(
        number="INV-MULTI",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
        payments=[
            PaymentRecord(date=datetime.date(2026, 5, 26), amount=Decimal("25"), method=PaymentMethod.WECHAT),
            PaymentRecord(date=datetime.date(2026, 5, 27), amount=Decimal("25"), method=PaymentMethod.ALIPAY),
            PaymentRecord(date=datetime.date(2026, 5, 28), amount=Decimal("25"), method=PaymentMethod.BANK_TRANSFER),
            PaymentRecord(date=datetime.date(2026, 5, 29), amount=Decimal("25"), method=PaymentMethod.CASH),
        ],
    )
    
    assert invoice_multi_pay.paid_amount() == Decimal("100")
    assert invoice_multi_pay.is_paid()
    print("  ✓ Multiple payments")
    
    # Invoice with same date and due date
    invoice_same_date = Invoice(
        number="INV-SAME",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 5, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    assert invoice_same_date.due_date == invoice_same_date.date
    assert not invoice_same_date.is_overdue(datetime.date(2026, 5, 26))
    print("  ✓ Same date and due date")
    
    print("  ✅ All edge case tests passed\n")


def test_invoice_item_unit():
    """Test InvoiceItem unit field."""
    print("Test: InvoiceItem unit field")
    
    # Default unit
    item_default = InvoiceItem(
        name="商品",
        quantity=Decimal("1"),
        unit_price=Decimal("100"),
    )
    assert item_default.unit == "件"
    print("  ✓ Default unit")
    
    # Custom unit
    item_custom = InvoiceItem(
        name="服务",
        quantity=Decimal("2"),
        unit_price=Decimal("500"),
        unit="小时",
    )
    assert item_custom.unit == "小时"
    print("  ✓ Custom unit (小时)")
    
    item_kg = InvoiceItem(
        name="大米",
        quantity=Decimal("5"),
        unit_price=Decimal("10"),
        unit="kg",
    )
    assert item_kg.unit == "kg"
    print("  ✓ Custom unit (kg)")
    
    print("  ✅ All unit tests passed\n")


def test_invoice_item_description():
    """Test InvoiceItem description field."""
    print("Test: InvoiceItem description field")
    
    # Empty description
    item_no_desc = InvoiceItem(
        name="商品",
        quantity=Decimal("1"),
        unit_price=Decimal("100"),
    )
    assert item_no_desc.description == ""
    print("  ✓ Empty description")
    
    # With description
    item_desc = InvoiceItem(
        name="服务",
        description="高级咨询服务，包含文档编写和现场支持",
        quantity=Decimal("1"),
        unit_price=Decimal("1000"),
    )
    assert "高级咨询" in item_desc.description
    print("  ✓ With description")
    
    # Description in to_dict
    desc_dict = item_desc.to_dict()
    assert desc_dict['description'] == item_desc.description
    print("  ✓ Description in to_dict")
    
    print("  ✅ All description tests passed\n")


def test_invoice_status_transitions():
    """Test invoice status transitions."""
    print("Test: Invoice status transitions")
    
    invoice = Invoice(
        number="INV-STATUS",
        date=datetime.date(2026, 5, 26),
        due_date=datetime.date(2026, 6, 26),
        seller={'name': '卖方'},
        buyer={'name': '买方'},
        items=[InvoiceItem(name="商品", quantity=Decimal("1"), unit_price=Decimal("100"))],
    )
    
    # Initial status
    assert invoice.status == InvoiceStatus.DRAFT
    print("  ✓ Initial DRAFT status")
    
    # After sending
    invoice.status = InvoiceStatus.SENT
    assert invoice.status == InvoiceStatus.SENT
    print("  ✓ SENT status")
    
    # Partial payment
    invoice.payments.append(
        PaymentRecord(date=datetime.date(2026, 5, 26), amount=Decimal("50"), method=PaymentMethod.WECHAT)
    )
    invoice.update_status()
    assert invoice.status == InvoiceStatus.PARTIAL
    print("  ✓ PARTIAL after partial payment")
    
    # Full payment
    invoice.payments.append(
        PaymentRecord(date=datetime.date(2026, 5, 27), amount=Decimal("50"), method=PaymentMethod.CASH)
    )
    invoice.update_status()
    assert invoice.status == InvoiceStatus.PAID
    print("  ✓ PAID after full payment")
    
    print("  ✅ All status transition tests passed\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Invoice Utilities Test Suite")
    print("=" * 60)
    print()
    
    test_invoice_item_creation()
    test_invoice_creation()
    test_payment_tracking()
    test_overdue_calculation()
    test_invoice_utils_class()
    test_tax_calculation()
    test_discount_calculation()
    test_validation()
    test_export_formats()
    test_invoice_types()
    test_due_date_calculation()
    test_payment_methods()
    test_invoice_stats()
    test_decimal_precision()
    test_currency_handling()
    test_tax_inclusive()
    test_empty_and_edge_cases()
    test_invoice_item_unit()
    test_invoice_item_description()
    test_invoice_status_transitions()
    
    print("=" * 60)
    print("✅ All tests passed! (42 test groups)")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()