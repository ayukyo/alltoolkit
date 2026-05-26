# Invoice Utils - 发票工具模块

发票生成和管理工具模块，支持发票创建、税额计算、折扣处理、付款跟踪和多种导出格式。

## 功能特性

- ✅ 发票创建与编号生成
- ✅ 税额计算（含税/不含税）
- ✅ 折扣处理（单品折扣、整体折扣）
- ✅ 付款跟踪与余额计算
- ✅ 过期检测与滞纳金计算
- ✅ 多种发票类型（标准、形式发票、贷记单、报价单）
- ✅ 多种导出格式（纯文本、Markdown、JSON）
- ✅ 发票验证
- ✅ 统计分析
- ✅ 零外部依赖

## 安装使用

```python
from invoice_utils.mod import (
    InvoiceUtils, Invoice, InvoiceItem, PaymentRecord,
    InvoiceStatus, InvoiceType, PaymentMethod,
)
```

## 快速示例

### 创建发票

```python
from decimal import Decimal
import datetime

# 创建发票项目
items = [
    InvoiceItem(
        name="咨询服务",
        description="高级技术咨询服务",
        quantity=Decimal("2"),
        unit_price=Decimal("500"),
        unit="小时",
        tax_percent=Decimal("13"),
    ),
    InvoiceItem(
        name="产品A",
        quantity=Decimal("10"),
        unit_price=Decimal("100"),
        discount_percent=Decimal("10"),
    ),
]

# 创建发票
seller = {
    'name': '北京示例科技有限公司',
    'address': '北京市朝阳区示例路123号',
    'tax_id': '91110105MA12345678',
    'phone': '010-12345678',
}

buyer = {
    'name': '上海客户公司',
    'address': '上海市浦东新区示例大道456号',
    'contact': '张经理',
}

utils = InvoiceUtils()
invoice = utils.create_invoice(
    seller=seller,
    buyer=buyer,
    items=items,
    due_days=30,
    notes="请按合同约定付款",
    terms="net30",
)

print(f"发票编号: {invoice.number}")
print(f"总金额: {invoice.total()}")
```

### 添加付款记录

```python
# 添加付款
payment = utils.add_payment(
    invoice,
    amount=Decimal("1000"),
    method=PaymentMethod.WECHAT,
    reference="WX20260526123456",
    notes="微信支付",
)

print(f"已付金额: {invoice.paid_amount()}")
print(f"余额: {invoice.balance_due()}")
print(f"状态: {invoice.status.value}")
```

### 导出发票

```python
# 纯文本格式
text_invoice = utils.to_text(invoice)
print(text_invoice)

# Markdown 格式
markdown_invoice = utils.to_markdown(invoice)
print(markdown_invoice)

# JSON 格式
json_invoice = utils.to_json(invoice)
print(json_invoice)
```

## API 参考

### InvoiceItem

发票项目类。

```python
InvoiceItem(
    name: str,                # 项目名称
    description: str = "",    # 项目描述
    quantity: Decimal,        # 数量
    unit_price: Decimal,      # 单价
    unit: str = "件",         # 单位
    discount_percent: Decimal = Decimal('0'),  # 折扣百分比
    tax_percent: Decimal = Decimal('0'),       # 税率百分比
)
```

**方法**：
- `subtotal()` - 小计（数量 × 单价）
- `discount_amount()` - 折扣金额
- `taxable_amount()` - 计税金额（小计 - 折扣）
- `tax_amount()` - 税额
- `total()` - 总计

### Invoice

发票类。

```python
Invoice(
    number: str,              # 发票编号
    date: datetime.date,      # 发票日期
    due_date: datetime.date,  # 到期日期
    seller: Dict[str, str],   # 卖方信息
    buyer: Dict[str, str],    # 买方信息
    items: List[InvoiceItem], # 项目列表
    payments: List[PaymentRecord] = [],  # 付款记录
    status: InvoiceStatus = InvoiceStatus.DRAFT,
    invoice_type: InvoiceType = InvoiceType.STANDARD,
    notes: str = "",
    terms: str = "",
    currency: str = "CNY",
    overall_discount_percent: Decimal = Decimal('0'),
    tax_inclusive: bool = False,
    late_fee_percent: Decimal = Decimal('0'),
)
```

**方法**：
- `subtotal()` - 所有项目小计
- `total_discount()` - 总折扣
- `total_tax()` - 总税额
- `total()` - 发票总额
- `paid_amount()` - 已付金额
- `balance_due()` - 未付余额
- `is_paid()` - 是否已付清
- `is_overdue(check_date)` - 是否过期
- `days_overdue(check_date)` - 过期天数
- `late_fee(check_date)` - 滞纳金
- `update_status()` - 更新状态
- `to_dict()` - 转换为字典

### InvoiceUtils

发票工具类。

**方法**：
- `generate_number()` - 生成发票编号
- `create_invoice()` - 创建发票
- `add_item()` - 添加项目
- `add_payment()` - 添加付款
- `calculate_tax()` - 计算税额
- `apply_discount()` - 应用折扣
- `validate_invoice()` - 验证发票
- `to_text()` - 导出为文本
- `to_markdown()` - 导出为 Markdown
- `to_json()` - 导出为 JSON
- `hash_invoice()` - 生成发票哈希
- `invoice_stats()` - 统计分析
- `get_tax_rate(region)` - 获取地区税率
- `calculate_due_date()` - 计算到期日

### 枚举类型

```python
# 发票状态
class InvoiceStatus(Enum):
    DRAFT = "draft"           # 草稿
    PENDING = "pending"       # 待处理
    SENT = "sent"             # 已发送
    VIEWED = "viewed"         # 已查看
    PAID = "paid"             # 已付款
    PARTIAL = "partial"       # 部分付款
    OVERDUE = "overdue"       # 已过期
    CANCELLED = "cancelled"   # 已取消
    REFUNDED = "refunded"     # 已退款

# 发票类型
class InvoiceType(Enum):
    STANDARD = "standard"     # 标准发票
    PROFORMA = "proforma"     # 形式发票
    RECURRING = "recurring"   # 定期发票
    CREDIT_NOTE = "credit_note"  # 贷记单
    DEBIT_NOTE = "debit_note"    # 借记单
    QUOTE = "quote"           # 报价单

# 付款方式
class PaymentMethod(Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CHECK = "check"
    PAYPAL = "paypal"
    WECHAT = "wechat"
    ALIPAY = "alipay"
    OTHER = "other"
```

## 常用税率

模块内置了常见地区的税率：

| 地区 | 税率 |
|------|------|
| CN (中国) | 13% |
| EU (欧盟) | 20% |
| UK (英国) | 20% |
| JP (日本) | 10% |
| AU (澳大利亚) | 10% GST |
| IN (印度) | 18% GST |
| SG (新加坡) | 8% GST |
| HK (香港) | 0% |

```python
# 获取税率
cn_rate = utils.get_tax_rate('CN')  # Decimal('0.13')
```

## 付款条款

支持常见付款条款格式：

| 条款 | 说明 |
|------|------|
| `net30` | 30天内付款 |
| `net15` | 15天内付款 |
| `net45` | 45天内付款 |
| `eom` | 月底付款 |
| `due_immediate` | 立即付款 |
| `cod` | 货到付款 |

```python
due_date = utils.calculate_due_date(invoice_date, "net30")
desc = utils.payment_terms_description("net30", "zh")  # "30天内付款"
```

## CLI 使用

```bash
# 生成示例发票
python mod.py generate

# 计算税额
python mod.py tax 1000 13

# 计算折扣
python mod.py discount 1000 10

# 查看常见税率
python mod.py rates
```

## 测试

```bash
python invoice_utils_test.py
```

## 许可证

MIT License

---

**AllToolkit** - 多语言工具函数库