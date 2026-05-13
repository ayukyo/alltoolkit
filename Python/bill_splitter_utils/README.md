# Bill Splitter Utils - 账单分账工具 🧾

提供账单分割、小费计算、费用分摊等功能。零外部依赖，纯 Python 标准库实现。

## 功能特性

- ✅ 账单均分 - 所有参与者平分费用
- ✅ 按项目分账 - 根据每个人消费的项目计算
- ✅ 按比例分账 - 自定义每人支付比例
- ✅ 自定义金额 - 每人指定固定金额
- ✅ 税费处理 - 支持税率计算
- ✅ 小费计算 - 支持多种小费比例
- ✅ 折扣支持 - 支持账单折扣
- ✅ 多币种支持 - 自定义货币符号
- ✅ 链式调用 - 简洁的 API 设计
- ✅ 历史记录 - 保存分账历史

## 快速开始

### 基本用法

```python
from bill_splitter_utils import BillSplitter

# 创建账单分账器
splitter = BillSplitter()

# 添加账单项目
splitter.add_item("Pizza", 30.00)
splitter.add_item("Salad", 15.00)
splitter.add_item("Drink", 10.00)

# 设置参与者
splitter.set_participants(["Alice", "Bob", "Charlie"])

# 设置税率和小费
splitter.set_tax_rate(0.10)   # 10% 税
splitter.set_tip_rate(0.15)   # 15% 小费

# 均分账单
summary = splitter.split_equally()

# 格式化输出
print(splitter.format_summary(summary))
```

### 按项目分账

```python
# 指定每个项目由谁分享
splitter = BillSplitter()
splitter.add_item("Pizza", 30.00, shared_by=["Alice", "Bob"])
splitter.add_item("Salad", 15.00, shared_by=["Charlie"])
splitter.add_item("Drink", 10.00, shared_by=["Alice", "Bob", "Charlie"])
splitter.set_participants(["Alice", "Bob", "Charlie"])

summary = splitter.split_by_items()
```

### 按比例分账

```python
splitter = BillSplitter()
splitter.add_item("Total", 100.00)
splitter.set_participants(["Alice", "Bob", "Charlie"])

# Alice 50%, Bob 30%, Charlie 20%
ratios = {"Alice": 0.5, "Bob": 0.3, "Charlie": 0.2}
summary = splitter.split_by_ratio(ratios)
```

### 自定义金额

```python
splitter = BillSplitter()
splitter.add_item("Total", 100.00)
splitter.add_participant("Alice", custom_amount=60.00)
splitter.add_participant("Bob", custom_amount=40.00)

summary = splitter.split_custom()
```

## 便捷函数

### 快速均分

```python
from bill_splitter_utils import split_bill_equally

result = split_bill_equally(100, 4, tax_rate=0.1, tip_rate=0.15)
# {'per_person': 28.75, 'subtotal': 100.0, 'tax': 10.0, 'tip': 16.5, 'total': 115.0}
```

### 小费计算

```python
from bill_splitter_utils import calculate_tip, suggest_tip

# 计算小费
tip = calculate_tip(100, 0.15)  # 15.0

# 获取小费建议
suggestions = suggest_tip(100)
# {'15%': 15.0, '18%': 18.0, '20%': 20.0, '22%': 22.0}
```

### 多项目分账

```python
from bill_splitter_utils import calculate_split_with_different_items

items = [
    {"name": "Pizza", "price": 30, "shared_by": ["Alice", "Bob"]},
    {"name": "Salad", "price": 15, "shared_by": ["Charlie"]}
]

result = calculate_split_with_different_items(items, ["Alice", "Bob", "Charlie"])
# {'Alice': 15.0, 'Bob': 15.0, 'Charlie': 15.0}
```

### 货币格式化

```python
from bill_splitter_utils import format_currency, parse_currency

# 格式化
formatted = format_currency(123.45)  # "$123.45"
formatted = format_currency(100, symbol="¥")  # "¥100.00"

# 解析
value = parse_currency("$123.45")  # 123.45
value = parse_currency("¥100")  # 100.0
```

## API 参考

### BillSplitter 类

| 方法 | 说明 |
|------|------|
| `add_item(name, price, shared_by)` | 添加账单项目 |
| `set_participants(names)` | 设置参与者 |
| `add_participant(name, items, custom_amount)` | 添加参与者 |
| `set_tax_rate(rate)` | 设置税率 |
| `set_tip_rate(rate)` | 设置小费比例 |
| `set_discount(amount)` | 设置折扣 |
| `split_equally()` | 均分账单 |
| `split_by_items()` | 按项目分账 |
| `split_by_ratio(ratios)` | 按比例分账 |
| `split_custom()` | 自定义金额分账 |
| `get_history()` | 获取历史记录 |
| `clear()` | 清空当前账单 |
| `format_summary(summary)` | 格式化输出 |

### 数据类

- `SplitResult` - 分账结果（姓名、小计、税费、小费、总计）
- `BillSummary` - 账单汇总（小计、税费、小费、折扣、总计、分账明细）

## 测试

```bash
python Python/bill_splitter_utils/bill_splitter_utils_test.py
```

**测试覆盖**: 21+ 测试用例，100% 通过率 ✅

---

**最后更新**: 2026-05-14