"""
AllToolkit - Python Invoice Utilities

A zero-dependency, production-ready invoice generation and management utility module.
Supports invoice creation, tax calculation, discount handling, payment tracking,
and multiple export formats.

Author: AllToolkit
License: MIT
"""

import datetime
import re
import hashlib
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP


# =============================================================================
# Constants and Configuration
# =============================================================================

# Default invoice number format
DEFAULT_NUMBER_FORMAT = "INV-{year}-{sequence:04d}"

# Common tax rates by region (as Decimal for precision)
COMMON_TAX_RATES = {
    'CN': Decimal('0.13'),    # China 13% VAT
    'US_CA': Decimal('0.0725'),  # California
    'US_TX': Decimal('0.0625'),  # Texas
    'EU': Decimal('0.20'),    # EU average
    'UK': Decimal('0.20'),    # UK VAT
    'JP': Decimal('0.10'),    # Japan
    'AU': Decimal('0.10'),    # Australia GST
    'IN': Decimal('0.18'),    # India GST
    'SG': Decimal('0.08'),    # Singapore GST
    'HK': Decimal('0.00'),    # Hong Kong (no VAT)
}

# Invoice status
class InvoiceStatus(Enum):
    """Invoice status."""
    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# Payment methods
class PaymentMethod(Enum):
    """Payment method."""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CHECK = "check"
    PAYPAL = "paypal"
    WECHAT = "wechat"
    ALIPAY = "alipay"
    OTHER = "other"


# Invoice type
class InvoiceType(Enum):
    """Invoice type."""
    STANDARD = "standard"
    PROFORMA = "proforma"
    RECURRING = "recurring"
    CREDIT_NOTE = "credit_note"
    DEBIT_NOTE = "debit_note"
    QUOTE = "quote"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class InvoiceItem:
    """Invoice line item."""
    name: str
    description: str = ""
    quantity: Decimal = Decimal('1')
    unit_price: Decimal = Decimal('0')
    unit: str = "件"
    discount_percent: Decimal = Decimal('0')
    tax_percent: Decimal = Decimal('0')
    
    def __post_init__(self):
        """Ensure Decimal types."""
        if not isinstance(self.quantity, Decimal):
            self.quantity = Decimal(str(self.quantity))
        if not isinstance(self.unit_price, Decimal):
            self.unit_price = Decimal(str(self.unit_price))
        if not isinstance(self.discount_percent, Decimal):
            self.discount_percent = Decimal(str(self.discount_percent))
        if not isinstance(self.tax_percent, Decimal):
            self.tax_percent = Decimal(str(self.tax_percent))
    
    def subtotal(self) -> Decimal:
        """Calculate subtotal (quantity * unit_price)."""
        return self.quantity * self.unit_price
    
    def discount_amount(self) -> Decimal:
        """Calculate discount amount."""
        return self.subtotal() * self.discount_percent / Decimal('100')
    
    def taxable_amount(self) -> Decimal:
        """Calculate amount after discount."""
        return self.subtotal() - self.discount_amount()
    
    def tax_amount(self) -> Decimal:
        """Calculate tax amount."""
        return self.taxable_amount() * self.tax_percent / Decimal('100')
    
    def total(self) -> Decimal:
        """Calculate total for this item."""
        return self.taxable_amount() + self.tax_amount()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'quantity': float(self.quantity),
            'unit_price': float(self.unit_price),
            'unit': self.unit,
            'discount_percent': float(self.discount_percent),
            'tax_percent': float(self.tax_percent),
            'subtotal': float(self.subtotal()),
            'discount_amount': float(self.discount_amount()),
            'tax_amount': float(self.tax_amount()),
            'total': float(self.total()),
        }


@dataclass
class PaymentRecord:
    """Payment record for an invoice."""
    date: datetime.date
    amount: Decimal
    method: PaymentMethod
    reference: str = ""
    notes: str = ""
    
    def __post_init__(self):
        """Ensure Decimal type."""
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'date': self.date.isoformat(),
            'amount': float(self.amount),
            'method': self.method.value,
            'reference': self.reference,
            'notes': self.notes,
        }


@dataclass
class Invoice:
    """Complete invoice data."""
    number: str
    date: datetime.date
    due_date: datetime.date
    seller: Dict[str, str] = field(default_factory=dict)
    buyer: Dict[str, str] = field(default_factory=dict)
    items: List[InvoiceItem] = field(default_factory=list)
    payments: List[PaymentRecord] = field(default_factory=list)
    status: InvoiceStatus = InvoiceStatus.DRAFT
    invoice_type: InvoiceType = InvoiceType.STANDARD
    notes: str = ""
    terms: str = ""
    currency: str = "CNY"
    overall_discount_percent: Decimal = Decimal('0')
    tax_inclusive: bool = False
    late_fee_percent: Decimal = Decimal('0')
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    
    def __post_init__(self):
        """Ensure Decimal type."""
        if not isinstance(self.overall_discount_percent, Decimal):
            self.overall_discount_percent = Decimal(str(self.overall_discount_percent))
        if not isinstance(self.late_fee_percent, Decimal):
            self.late_fee_percent = Decimal(str(self.late_fee_percent))
    
    def subtotal(self) -> Decimal:
        """Calculate subtotal (sum of all item subtotals)."""
        return sum(item.subtotal() for item in self.items)
    
    def total_discount(self) -> Decimal:
        """Calculate total discount."""
        item_discounts = sum(item.discount_amount() for item in self.items)
        overall_discount = (self.subtotal() - item_discounts) * self.overall_discount_percent / Decimal('100')
        return item_discounts + overall_discount
    
    def taxable_amount(self) -> Decimal:
        """Calculate taxable amount after discounts."""
        return self.subtotal() - self.total_discount()
    
    def total_tax(self) -> Decimal:
        """Calculate total tax."""
        if self.tax_inclusive:
            # Tax is already included in prices
            return Decimal('0')
        return sum(item.tax_amount() for item in self.items)
    
    def total(self) -> Decimal:
        """Calculate invoice total."""
        base = self.subtotal() - self.total_discount()
        if not self.tax_inclusive:
            base += self.total_tax()
        return base.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def paid_amount(self) -> Decimal:
        """Calculate total paid amount."""
        return sum(p.amount for p in self.payments)
    
    def balance_due(self) -> Decimal:
        """Calculate remaining balance."""
        return self.total() - self.paid_amount()
    
    def is_paid(self) -> bool:
        """Check if invoice is fully paid."""
        return self.balance_due() <= Decimal('0')
    
    def is_overdue(self, check_date: Optional[datetime.date] = None) -> bool:
        """Check if invoice is overdue."""
        if check_date is None:
            check_date = datetime.date.today()
        return check_date > self.due_date and not self.is_paid()
    
    def days_overdue(self, check_date: Optional[datetime.date] = None) -> int:
        """Calculate days overdue."""
        if check_date is None:
            check_date = datetime.date.today()
        if not self.is_overdue(check_date):
            return 0
        return (check_date - self.due_date).days
    
    def late_fee(self, check_date: Optional[datetime.date] = None) -> Decimal:
        """Calculate late fee."""
        days = self.days_overdue(check_date)
        if days <= 0 or self.late_fee_percent <= 0:
            return Decimal('0')
        # Simple late fee calculation: percentage per day (capped)
        fee_rate = self.late_fee_percent * min(days, 30) / Decimal('100')
        return self.balance_due() * fee_rate
    
    def update_status(self) -> InvoiceStatus:
        """Update invoice status based on payment."""
        if self.is_paid():
            self.status = InvoiceStatus.PAID
        elif self.paid_amount() > 0:
            self.status = InvoiceStatus.PARTIAL
        elif self.is_overdue():
            self.status = InvoiceStatus.OVERDUE
        return self.status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'number': self.number,
            'date': self.date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'seller': self.seller,
            'buyer': self.buyer,
            'items': [item.to_dict() for item in self.items],
            'payments': [p.to_dict() for p in self.payments],
            'status': self.status.value,
            'invoice_type': self.invoice_type.value,
            'notes': self.notes,
            'terms': self.terms,
            'currency': self.currency,
            'overall_discount_percent': float(self.overall_discount_percent),
            'tax_inclusive': self.tax_inclusive,
            'late_fee_percent': float(self.late_fee_percent),
            'created_at': self.created_at.isoformat(),
            'subtotal': float(self.subtotal()),
            'total_discount': float(self.total_discount()),
            'total_tax': float(self.total_tax()),
            'total': float(self.total()),
            'paid_amount': float(self.paid_amount()),
            'balance_due': float(self.balance_due()),
            'is_paid': self.is_paid(),
            'is_overdue': self.is_overdue(),
            'days_overdue': self.days_overdue(),
        }


# =============================================================================
# Main Utility Class
# =============================================================================

class InvoiceUtils:
    """
    Comprehensive invoice generation and management utility class.
    
    Features:
    - Invoice creation with customizable formats
    - Tax calculation (inclusive/exclusive)
    - Discount handling (item-level and overall)
    - Payment tracking and balance calculation
    - Invoice number generation
    - Multiple export formats (text, markdown, JSON)
    - Invoice validation and verification
    """
    
    def __init__(self, 
                 number_format: str = DEFAULT_NUMBER_FORMAT,
                 default_currency: str = "CNY",
                 default_tax_rate: Decimal = Decimal('0')):
        """
        Initialize InvoiceUtils.
        
        Args:
            number_format: Invoice number format template
            default_currency: Default currency code
            default_tax_rate: Default tax rate (0 = no tax)
        """
        self.number_format = number_format
        self.default_currency = default_currency
        self.default_tax_rate = default_tax_rate
        self._sequence_counter = 0
    
    # -------------------------------------------------------------------------
    # Invoice Creation
    # -------------------------------------------------------------------------
    
    def generate_number(self, 
                        year: Optional[int] = None,
                        sequence: Optional[int] = None) -> str:
        """
        Generate invoice number.
        
        Args:
            year: Year for invoice number (default: current year)
            sequence: Sequence number (default: auto-increment)
        
        Returns:
            Generated invoice number
        """
        if year is None:
            year = datetime.date.today().year
        
        if sequence is None:
            self._sequence_counter += 1
            sequence = self._sequence_counter
        
        return self.number_format.format(year=year, sequence=sequence)
    
    def create_invoice(self,
                       seller: Dict[str, str],
                       buyer: Dict[str, str],
                       items: List[InvoiceItem],
                       due_days: int = 30,
                       invoice_type: InvoiceType = InvoiceType.STANDARD,
                       notes: str = "",
                       terms: str = "",
                       **kwargs) -> Invoice:
        """
        Create a new invoice.
        
        Args:
            seller: Seller information dict
            buyer: Buyer information dict
            items: List of invoice items
            due_days: Days until due date
            invoice_type: Type of invoice
            notes: Additional notes
            terms: Payment terms
            **kwargs: Additional invoice properties
        
        Returns:
            Invoice object
        """
        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=due_days)
        
        invoice = Invoice(
            number=self.generate_number(),
            date=today,
            due_date=due_date,
            seller=seller,
            buyer=buyer,
            items=items,
            invoice_type=invoice_type,
            notes=notes,
            terms=terms,
            currency=kwargs.get('currency', self.default_currency),
            **{k: v for k, v in kwargs.items() if k not in ['currency']}
        )
        
        return invoice
    
    def add_item(self,
                 invoice: Invoice,
                 name: str,
                 quantity: Decimal,
                 unit_price: Decimal,
                 description: str = "",
                 unit: str = "件",
                 discount_percent: Decimal = Decimal('0'),
                 tax_percent: Decimal = Decimal('0')) -> InvoiceItem:
        """
        Add an item to an invoice.
        
        Args:
            invoice: Invoice to modify
            name: Item name
            quantity: Quantity
            unit_price: Unit price
            description: Item description
            unit: Unit of measurement
            discount_percent: Item discount percentage
            tax_percent: Tax percentage
        
        Returns:
            Added InvoiceItem
        """
        item = InvoiceItem(
            name=name,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
            unit=unit,
            discount_percent=discount_percent,
            tax_percent=tax_percent if tax_percent > 0 else self.default_tax_rate,
        )
        invoice.items.append(item)
        return item
    
    def add_payment(self,
                    invoice: Invoice,
                    amount: Decimal,
                    method: PaymentMethod,
                    date: Optional[datetime.date] = None,
                    reference: str = "",
                    notes: str = "") -> PaymentRecord:
        """
        Add a payment to an invoice.
        
        Args:
            invoice: Invoice to modify
            amount: Payment amount
            method: Payment method
            date: Payment date (default: today)
            reference: Payment reference
            notes: Payment notes
        
        Returns:
            Added PaymentRecord
        """
        if date is None:
            date = datetime.date.today()
        
        payment = PaymentRecord(
            date=date,
            amount=amount,
            method=method,
            reference=reference,
            notes=notes,
        )
        invoice.payments.append(payment)
        invoice.update_status()
        return payment
    
    # -------------------------------------------------------------------------
    # Calculation Utilities
    # -------------------------------------------------------------------------
    
    def calculate_tax(self,
                      amount: Decimal,
                      tax_rate: Decimal,
                      inclusive: bool = False) -> Tuple[Decimal, Decimal]:
        """
        Calculate tax amount.
        
        Args:
            amount: Base amount
            tax_rate: Tax rate as percentage
            inclusive: Whether tax is included in amount
        
        Returns:
            Tuple of (tax_amount, net_amount)
        """
        if inclusive:
            # Tax is included, extract it
            gross = amount
            tax_amount = gross * tax_rate / (Decimal('100') + tax_rate)
            net_amount = gross - tax_amount
        else:
            # Tax is added to amount
            net_amount = amount
            tax_amount = net_amount * tax_rate / Decimal('100')
        
        return (tax_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                net_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def apply_discount(self,
                       amount: Decimal,
                       discount_percent: Decimal) -> Tuple[Decimal, Decimal]:
        """
        Apply discount to amount.
        
        Args:
            amount: Original amount
            discount_percent: Discount percentage
        
        Returns:
            Tuple of (discount_amount, discounted_amount)
        """
        discount_amount = amount * discount_percent / Decimal('100')
        discounted_amount = amount - discount_amount
        return (discount_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                discounted_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def calculate_totals(self, invoice: Invoice) -> Dict[str, Decimal]:
        """
        Calculate all invoice totals.
        
        Args:
            invoice: Invoice to calculate
        
        Returns:
            Dict with subtotal, discount, tax, and total
        """
        return {
            'subtotal': invoice.subtotal(),
            'discount': invoice.total_discount(),
            'taxable_amount': invoice.taxable_amount(),
            'tax': invoice.total_tax(),
            'total': invoice.total(),
            'paid': invoice.paid_amount(),
            'balance': invoice.balance_due(),
        }
    
    # -------------------------------------------------------------------------
    # Tax Rate Utilities
    # -------------------------------------------------------------------------
    
    def get_tax_rate(self, region: str) -> Decimal:
        """
        Get common tax rate for a region.
        
        Args:
            region: Region code (e.g., 'CN', 'US_CA', 'EU')
        
        Returns:
            Tax rate as Decimal
        """
        return COMMON_TAX_RATES.get(region, Decimal('0'))
    
    def list_tax_rates(self) -> Dict[str, Decimal]:
        """
        Get all common tax rates.
        
        Returns:
            Dict of region -> tax rate
        """
        return COMMON_TAX_RATES.copy()
    
    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    
    def validate_invoice(self, invoice: Invoice) -> List[str]:
        """
        Validate invoice for common issues.
        
        Args:
            invoice: Invoice to validate
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        if not invoice.number:
            errors.append("Invoice number is required")
        
        if not invoice.seller:
            errors.append("Seller information is required")
        
        if not invoice.buyer:
            errors.append("Buyer information is required")
        
        if not invoice.items:
            errors.append("At least one item is required")
        
        # Check dates
        if invoice.due_date < invoice.date:
            errors.append("Due date cannot be before invoice date")
        
        # Check items
        for i, item in enumerate(invoice.items):
            if not item.name:
                errors.append(f"Item {i+1}: Name is required")
            if item.quantity <= 0:
                errors.append(f"Item {i+1}: Quantity must be positive")
            if item.unit_price < 0:
                errors.append(f"Item {i+1}: Unit price cannot be negative")
        
        # Check payments
        total_paid = invoice.paid_amount()
        if total_paid > invoice.total():
            errors.append(f"Total paid ({total_paid}) exceeds invoice total ({invoice.total()})")
        
        return errors
    
    def is_valid_invoice_number(self, number: str) -> bool:
        """
        Validate invoice number format.
        
        Args:
            number: Invoice number to validate
        
        Returns:
            True if valid
        """
        if not number:
            return False
        # Allow alphanumeric with hyphens and underscores
        return bool(re.match(r'^[A-Za-z0-9_-]+$', number))
    
    # -------------------------------------------------------------------------
    # Export Formats
    # -------------------------------------------------------------------------
    
    def to_text(self, invoice: Invoice) -> str:
        """
        Convert invoice to plain text format.
        
        Args:
            invoice: Invoice to convert
        
        Returns:
            Plain text invoice
        """
        lines = []
        
        # Header
        lines.append("=" * 50)
        lines.append(f"发票 / INVOICE: {invoice.number}")
        lines.append("=" * 50)
        lines.append("")
        
        # Type and status
        lines.append(f"类型: {invoice.invoice_type.value}")
        lines.append(f"状态: {invoice.status.value}")
        lines.append(f"日期: {invoice.date.strftime('%Y-%m-%d')}")
        lines.append(f"到期日: {invoice.due_date.strftime('%Y-%m-%d')}")
        lines.append("")
        
        # Seller
        lines.append("卖方 / SELLER:")
        for key, value in invoice.seller.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        # Buyer
        lines.append("买方 / BUYER:")
        for key, value in invoice.buyer.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        # Items
        lines.append("-" * 50)
        lines.append("明细 / ITEMS:")
        lines.append("-" * 50)
        
        for item in invoice.items:
            lines.append(f"  {item.name}")
            if item.description:
                lines.append(f"    {item.description}")
            lines.append(f"    数量: {item.quantity} {item.unit} × {item.unit_price} {invoice.currency}")
            if item.discount_percent > 0:
                lines.append(f"    折扣: {item.discount_percent}%")
            if item.tax_percent > 0:
                lines.append(f"    税率: {item.tax_percent}%")
            lines.append(f"    小计: {item.total():.2f} {invoice.currency}")
            lines.append("")
        
        # Totals
        lines.append("-" * 50)
        lines.append(f"合计小计: {invoice.subtotal():.2f} {invoice.currency}")
        if invoice.total_discount() > 0:
            lines.append(f"折扣: -{invoice.total_discount():.2f} {invoice.currency}")
        if invoice.total_tax() > 0:
            lines.append(f"税额: {invoice.total_tax():.2f} {invoice.currency}")
        lines.append("-" * 50)
        lines.append(f"总计: {invoice.total():.2f} {invoice.currency}")
        lines.append("")
        
        # Payments
        if invoice.payments:
            lines.append("-" * 50)
            lines.append("付款记录 / PAYMENTS:")
            lines.append("-" * 50)
            for p in invoice.payments:
                lines.append(f"  {p.date.strftime('%Y-%m-%d')}: {p.amount:.2f} {invoice.currency} ({p.method.value})")
            lines.append(f"已付: {invoice.paid_amount():.2f} {invoice.currency}")
            lines.append(f"余额: {invoice.balance_due():.2f} {invoice.currency}")
            lines.append("")
        
        # Notes and terms
        if invoice.notes:
            lines.append(f"备注: {invoice.notes}")
        
        if invoice.terms:
            lines.append(f"条款: {invoice.terms}")
        
        # Footer
        lines.append("")
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def to_markdown(self, invoice: Invoice) -> str:
        """
        Convert invoice to Markdown format.
        
        Args:
            invoice: Invoice to convert
        
        Returns:
            Markdown formatted invoice
        """
        lines = []
        
        # Header
        lines.append(f"# 🧾 发票 {invoice.number}")
        lines.append("")
        
        # Info table
        lines.append("| 属性 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| 类型 | {invoice.invoice_type.value} |")
        lines.append(f"| 状态 | {invoice.status.value} |")
        lines.append(f"| 日期 | {invoice.date.strftime('%Y-%m-%d')} |")
        lines.append(f"| 到期日 | {invoice.due_date.strftime('%Y-%m-%d')} |")
        lines.append(f"| 货币 | {invoice.currency} |")
        lines.append("")
        
        # Seller
        lines.append("## 🏢 卖方")
        lines.append("")
        for key, value in invoice.seller.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
        
        # Buyer
        lines.append("## 🏠 买方")
        lines.append("")
        for key, value in invoice.buyer.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
        
        # Items table
        lines.append("## 📦 商品明细")
        lines.append("")
        lines.append("| 名称 | 数量 | 单价 | 折扣 | 税率 | 小计 |")
        lines.append("|------|------|------|------|------|------|")
        
        for item in invoice.items:
            lines.append(f"| {item.name} | {item.quantity} {item.unit} | {item.unit_price:.2f} | {item.discount_percent}% | {item.tax_percent}% | {item.total():.2f} |")
        
        lines.append("")
        
        # Totals
        lines.append("## 💰 结算")
        lines.append("")
        lines.append(f"| 项目 | 金额 ({invoice.currency}) |")
        lines.append("|------|------|")
        lines.append(f"| 小计 | {invoice.subtotal():.2f} |")
        if invoice.total_discount() > 0:
            lines.append(f"| 折扣 | -{invoice.total_discount():.2f} |")
        if invoice.total_tax() > 0:
            lines.append(f"| 税额 | {invoice.total_tax():.2f} |")
        lines.append(f"| **总计** | **{invoice.total():.2f}** |")
        
        if invoice.payments:
            lines.append(f"| 已付 | {invoice.paid_amount():.2f} |")
            lines.append(f"| **余额** | **{invoice.balance_due():.2f}** |")
        
        lines.append("")
        
        # Payment records
        if invoice.payments:
            lines.append("## 📅 付款记录")
            lines.append("")
            lines.append("| 日期 | 金额 | 方式 | 参考 |")
            lines.append("|------|------|------|------|")
            for p in invoice.payments:
                lines.append(f"| {p.date.strftime('%Y-%m-%d')} | {p.amount:.2f} | {p.method.value} | {p.reference} |")
            lines.append("")
        
        # Notes and terms
        if invoice.notes:
            lines.append("## 📝 备注")
            lines.append("")
            lines.append(invoice.notes)
            lines.append("")
        
        if invoice.terms:
            lines.append("## 📋 条款")
            lines.append("")
            lines.append(invoice.terms)
            lines.append("")
        
        return "\n".join(lines)
    
    def to_json(self, invoice: Invoice) -> str:
        """
        Convert invoice to JSON string.
        
        Args:
            invoice: Invoice to convert
        
        Returns:
            JSON string
        """
        import json
        return json.dumps(invoice.to_dict(), indent=2, ensure_ascii=False)
    
    # -------------------------------------------------------------------------
    # Invoice Hashing
    # -------------------------------------------------------------------------
    
    def hash_invoice(self, invoice: Invoice) -> str:
        """
        Generate a hash for invoice verification.
        
        Args:
            invoice: Invoice to hash
        
        Returns:
            SHA-256 hash of invoice content
        """
        # Create a canonical representation
        content = f"{invoice.number}|{invoice.date}|{invoice.total()}|{invoice.seller}|{invoice.buyer}|{len(invoice.items)}"
        for item in invoice.items:
            content += f"|{item.name}|{item.quantity}|{item.unit_price}|{item.total()}"
        
        return hashlib.sha256(content.encode()).hexdigest()
    
    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------
    
    def invoice_stats(self, invoices: List[Invoice]) -> Dict[str, Any]:
        """
        Calculate statistics for multiple invoices.
        
        Args:
            invoices: List of invoices
        
        Returns:
            Dict with statistics
        """
        if not invoices:
            return {}
        
        total_amount = sum(inv.total() for inv in invoices)
        total_paid = sum(inv.paid_amount() for inv in invoices)
        total_balance = sum(inv.balance_due() for inv in invoices)
        
        overdue_count = len([inv for inv in invoices if inv.is_overdue()])
        
        avg_amount = total_amount / len(invoices)
        
        return {
            'count': len(invoices),
            'total_amount': float(total_amount),
            'total_paid': float(total_paid),
            'total_balance': float(total_balance),
            'avg_amount': float(avg_amount),
            'by_status': {s.value: len([i for i in invoices if i.status == s]) for s in InvoiceStatus},
            'overdue_count': overdue_count,
            'paid_rate': float(total_paid / total_amount) if total_amount > 0 else 0,
        }
    
    # -------------------------------------------------------------------------
    # Due Date Utilities
    # -------------------------------------------------------------------------
    
    def calculate_due_date(self,
                           invoice_date: datetime.date,
                           terms: str = "net30") -> datetime.date:
        """
        Calculate due date from payment terms.
        
        Args:
            invoice_date: Invoice date
            terms: Payment terms (e.g., 'net30', 'due15', 'eom')
        
        Returns:
            Due date
        """
        # Parse common terms
        if terms.lower() == 'eom':
            # End of month
            next_month = invoice_date.replace(day=1) + datetime.timedelta(days=32)
            return next_month.replace(day=1) - datetime.timedelta(days=1)
        
        if terms.lower().startswith('net'):
            days = int(terms[3:])
            return invoice_date + datetime.timedelta(days=days)
        
        if terms.lower().startswith('due'):
            days = int(terms[4:])
            return invoice_date + datetime.timedelta(days=days)
        
        # Default 30 days
        return invoice_date + datetime.timedelta(days=30)
    
    def payment_terms_description(self, terms: str, lang: str = "zh") -> str:
        """
        Get description for payment terms.
        
        Args:
            terms: Payment terms code
            lang: Language ('zh' or 'en')
        
        Returns:
            Terms description
        """
        descriptions = {
            'net30': {'zh': '30天内付款', 'en': 'Payment due within 30 days'},
            'net15': {'zh': '15天内付款', 'en': 'Payment due within 15 days'},
            'net45': {'zh': '45天内付款', 'en': 'Payment due within 45 days'},
            'net60': {'zh': '60天内付款', 'en': 'Payment due within 60 days'},
            'eom': {'zh': '月底付款', 'en': 'Payment due at end of month'},
            'due_immediate': {'zh': '立即付款', 'en': 'Payment due immediately'},
            'cod': {'zh': '货到付款', 'en': 'Cash on delivery'},
            'pia': {'zh': '预付款', 'en': 'Payment in advance'},
        }
        
        return descriptions.get(terms.lower(), {}).get(lang, terms)


# =============================================================================
# Module-level Functions (Convenience)
# =============================================================================

# Default instance for module-level functions
_default_utils = InvoiceUtils()


def generate_number(year: Optional[int] = None, sequence: Optional[int] = None) -> str:
    """Generate invoice number."""
    return _default_utils.generate_number(year, sequence)


def create_invoice(seller: Dict[str, str],
                   buyer: Dict[str, str],
                   items: List[InvoiceItem],
                   **kwargs) -> Invoice:
    """Create a new invoice."""
    return _default_utils.create_invoice(seller, buyer, items, **kwargs)


def calculate_tax(amount: Decimal, tax_rate: Decimal, inclusive: bool = False) -> Tuple[Decimal, Decimal]:
    """Calculate tax amount."""
    return _default_utils.calculate_tax(amount, tax_rate, inclusive)


def apply_discount(amount: Decimal, discount_percent: Decimal) -> Tuple[Decimal, Decimal]:
    """Apply discount to amount."""
    return _default_utils.apply_discount(amount, discount_percent)


def validate_invoice(invoice: Invoice) -> List[str]:
    """Validate invoice for common issues."""
    return _default_utils.validate_invoice(invoice)


def to_text(invoice: Invoice) -> str:
    """Convert invoice to plain text format."""
    return _default_utils.to_text(invoice)


def to_markdown(invoice: Invoice) -> str:
    """Convert invoice to Markdown format."""
    return _default_utils.to_markdown(invoice)


def get_tax_rate(region: str) -> Decimal:
    """Get common tax rate for a region."""
    return _default_utils.get_tax_rate(region)


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Invoice Utils - Command Line Interface")
        print("Usage: python mod.py <command> [args]")
        print("\nCommands:")
        print("  generate  - Generate sample invoice")
        print("  tax <amount> <rate> - Calculate tax")
        print("  discount <amount> <percent> - Apply discount")
        print("  rates - List common tax rates")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'generate':
        # Create a sample invoice
        seller = {
            'name': '示例公司',
            'address': '北京市朝阳区示例路123号',
            'tax_id': '91110105MA12345678',
        }
        
        buyer = {
            'name': '客户公司',
            'address': '上海市浦东新区示例大道456号',
        }
        
        items = [
            InvoiceItem(name='服务费', quantity=Decimal('1'), unit_price=Decimal('1000')),
            InvoiceItem(name='产品A', quantity=Decimal('10'), unit_price=Decimal('50'), tax_percent=Decimal('13')),
        ]
        
        invoice = create_invoice(seller, buyer, items, notes='示例发票')
        print(to_markdown(invoice))
    
    elif command == 'tax' and len(sys.argv) > 3:
        amount = Decimal(sys.argv[2])
        rate = Decimal(sys.argv[3])
        tax, net = calculate_tax(amount, rate)
        print(f"金额: {amount}")
        print(f"税率: {rate}%")
        print(f"税额: {tax}")
        print(f"净额: {net}")
    
    elif command == 'discount' and len(sys.argv) > 3:
        amount = Decimal(sys.argv[2])
        percent = Decimal(sys.argv[3])
        discount, result = apply_discount(amount, percent)
        print(f"原价: {amount}")
        print(f"折扣: {percent}%")
        print(f"折扣额: {discount}")
        print(f"折后价: {result}")
    
    elif command == 'rates':
        for region, rate in _default_utils.list_tax_rates().items():
            print(f"{region}: {rate}%")
    
    else:
        print(f"Unknown command or missing arguments: {command}")
        sys.exit(1)