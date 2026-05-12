# Tipping Utils - 小费计算工具 💰

支持多国家小费文化、账单分割、百分比计算等功能。

## 特性

- ✅ **零外部依赖** - 仅使用 Python 标准库
- ✅ **多国家支持** - 40+ 国家的小费文化数据
- ✅ **多服务类型** - 餐厅、出租车、酒店、美容等
- ✅ **智能建议** - 根据服务质量自动推荐小费
- ✅ **账单分割** - 均分和按比例分摊
- ✅ **含税计算** - 支持税前/税后小费计算
- ✅ **四舍五入** - 多种舍入方式支持

## 安装

```python
from tipping_utils.mod import *
```

## 快速开始

### 基本小费计算

```python
from tipping_utils.mod import calculate_tip, tip

# 计算 18% 小费
calc = calculate_tip(100.0, 18.0)
print(f"小费: ${calc.tip_amount}, 总计: ${calc.total}")

# 便捷函数
tip_amount, total = tip(100.0, 20.0)
```

### 账单分割

```python
from tipping_utils.mod import split_bill, split

# 4人均分
result = split_bill(150.0, 4, tip_percent=18.0)
print(f"每人: ${result.per_person}")

# 便捷函数
per_person = split(100.0, 4, 20.0)
```

### 国家小费建议

```python
from tipping_utils.mod import suggest_tip, Country, ServiceType

# 美国餐厅建议
tip_amount, note = suggest_tip(100.0, Country.USA, ServiceType.RESTAURANT, "good")
print(f"建议小费: ${tip_amount}")

# 日本无小费文化
tip_amount, note = suggest_tip(100.0, Country.JAPAN, ServiceType.RESTAURANT)
```

## API 参考

### 核心类

#### Country
国家枚举，包含 40+ 国家。

```python
Country.USA      # 美国 - 强小费文化
Country.JAPAN    # 日本 - 无小费文化
Country.CHINA    # 中国 - 无小费文化
Country.FRANCE   # 法国 - 服务费已含
Country.UK       # 英国 - 中等小费文化
```

#### ServiceType
服务类型枚举。

```python
ServiceType.RESTAURANT   # 餐厅
ServiceType.BAR          # 酒吧
ServiceType.TAXI         # 出租车
ServiceType.DELIVERY     # 外卖配送
ServiceType.HOTEL        # 酒店
ServiceType.HAIR_SALON   # 美发沙龙
ServiceType.SPA          # SPA
```

### 计算函数

#### calculate_tip(bill_amount, tip_percent, tax=0.0, tax_included=True)
计算小费。

```python
calc = calculate_tip(100.0, 18.0)
# bill_amount: 100.0
# tip_amount: 18.0
# total: 118.0
```

#### calculate_tip_with_tax(bill_amount, tip_percent, tax_percent, tip_on_pre_tax=True)
含税小费计算。

```python
calc = calculate_tip_with_tax(100.0, 18.0, 8.25)
# tax: 8.25
# tip_amount: 18.0
# grand_total: 126.25
```

#### split_bill(bill_amount, people_count, tip_percent=0.0, tax=0.0, ...)
分割账单。

```python
result = split_bill(100.0, 4, tip_percent=18.0)
# subtotal: 100.0
# tip: 18.0
# total: 118.0
# per_person: 29.5
```

#### split_by_items(items, tip_percent=0.0, ...)
按项目分摊。

```python
items = [("Alice", 50.0), ("Bob", 30.0), ("Charlie", 20.0)]
result = split_by_items(items, tip_percent=18.0)
# {"Alice": 59.0, "Bob": 35.4, "Charlie": 23.6}
```

### 建议函数

#### suggest_tip(bill_amount, country, service_type, service_quality)
根据国家和服务质量建议小费。

```python
tip_amount, note = suggest_tip(100.0, Country.USA, ServiceType.RESTAURANT, "excellent")
# tip_amount: 25.0
```

#### get_tip_recommendation(country, service_type)
获取小费建议详情。

```python
rec = get_tip_recommendation(Country.USA, ServiceType.RESTAURANT)
# min_percent: 15.0
# max_percent: 25.0
# standard_percent: 18.0
# is_expected: True
```

### 辅助函数

#### round_tip(tip_amount, method="nearest", precision=0.25)
四舍五入小费。

```python
rounded = round_tip(3.73, method="nearest", precision=0.25)
# 3.75
```

#### calculate_percentage(bill_amount, tip_amount)
计算小费百分比。

```python
percent = calculate_percentage(100.0, 18.0)
# 18.0
```

#### calculate_quick_tips(bill_amount)
快速计算多个比例。

```python
tips = calculate_quick_tips(100.0)
# {"10%": ..., "15%": ..., "18%": ..., "20%": ..., "25%": ...}
```

#### format_tip_summary(bill_amount, tip_percent, tax=0.0, ...)
格式化小费摘要。

```python
summary = format_tip_summary(100.0, 18.0)
# "账单: $100.00\n小费 (18%): $18.00\n总计: $118.00"
```

### 便捷函数

```python
# 快速计算
tip_amount, total = tip(100.0, 18.0)

# 快速分割
per_person = split(100.0, 4, 18.0)
```

## 小费文化参考

### 强小费文化 (15%+)
- 美国 🇺🇸
- 加拿大 🇨🇦

### 中等小费文化 (5-15%)
- 英国 🇬🇧
- 德国 🇩🇪
- 印度 🇮🇳

### 弱小费文化 (可选)
- 法国 🇫🇷
- 澳大利亚 🇦🇺
- 巴西 🇧🇷

### 无小费文化
- 日本 🇯🇵
- 中国 🇨🇳
- 韩国 🇰🇷
- 新加坡 🇸🇬

## 测试

```bash
python tipping_utils_test.py
```

测试覆盖:
- 基本小费计算
- 含税计算
- 账单分割
- 国家建议
- 四舍五入
- 边界情况

## 示例

```bash
python examples/usage_examples.py
```

## 许可证

MIT License