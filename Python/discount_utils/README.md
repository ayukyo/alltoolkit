# Discount Utils - 折扣计算工具

一个全面的折扣和价格计算工具模块，零外部依赖。

## 功能特性

### 基础折扣计算
- 百分比折扣 (`apply_percentage_discount`)
- 固定金额折扣 (`apply_fixed_discount`)
- 折扣金额计算 (`calculate_discount_amount`)
- 折扣百分比反算 (`calculate_discount_percentage`)
- 原价计算 (`calculate_original_price`)

### 多重折扣处理
- 顺序折扣叠加 (`apply_sequential_discounts`)
- 最大折扣优先 (`apply_max_discount`)
- 折扣合并（带上限） (`apply_combined_discount`)
- 加权折扣 (`apply_weighted_discounts`)
- 策略化折扣应用 (`apply_discount_with_strategy`)

### 阶梯折扣
- 阶梯折扣应用 (`apply_tiered_discount`)
- 最佳阶梯查找 (`find_best_tier`)
- 升级建议 (`suggest_upgrade_for_tier`)

### 捆绑与促销
- 捆绑折扣计算 (`BundleDiscount`, `calculate_bundle_savings`)
- Buy X Get Y 促销 (`apply_buy_x_get_y`)
- 免费商品计算 (`calculate_free_items`)

### 税费计算
- 税额计算 (`calculate_tax`, `apply_tax`)
- 税费与折扣组合 (`calculate_price_with_tax_and_discount`)
- 支持税前折扣和税后折扣两种模式

### 利润计算
- 利润率计算 (`calculate_profit_margin`)
- 加价计算 (`calculate_markup`)
- 成本反算 (`calculate_cost_from_margin`)
- 保本折扣计算 (`calculate_break_even_discount`)

### 价格比较
- 多源价格比较 (`compare_prices`)
- 批量价格最优选择 (`find_best_bulk_price`)

### 价格格式化
- 价格格式化 (`format_price`)
- 百分比格式化 (`format_percentage`)
- 节省信息格式化 (`format_savings`)

### 优惠券验证
- 优惠券有效性验证 (`validate_coupon`)
- 最低购买要求检查
- 过期日期检查

### 价格历史分析
- 价格趋势分析 (`analyze_price_history`)
- 优惠判断 (`is_good_deal`)

## 使用示例

### 基础折扣
```python
from discount_utils.mod import apply_percentage_discount, apply_fixed_discount

# 20% 折扣
price = apply_percentage_discount(100, 20)  # 80.0

# $20 固定折扣
price = apply_fixed_discount(100, 20)  # 80.0
```

### 多重折扣策略
```python
from discount_utils.mod import apply_sequential_discounts, apply_max_discount

# 顺序叠加: 100 - 10% = 90, 90 - 10% = 81
price = apply_sequential_discounts(100, [10, 10])  # 81.0

# 最大折扣优先
price = apply_max_discount(100, [10, 20, 15])  # 80.0 (应用20%)
```

### 阶梯折扣
```python
from discount_utils.mod import TieredDiscount, apply_tiered_discount, suggest_upgrade_for_tier

tiers = TieredDiscount([
    (100, 5),    # $100以上 5%折扣
    (500, 10),   # $500以上 10%折扣
    (1000, 15),  # $1000以上 15%折扣
])

price = apply_tiered_discount(800, tiers)  # 720.0 (10%折扣)

# 建议: $300购买者需要加$200才能达到10%折扣档
suggestion = suggest_upgrade_for_tier(300, tiers)  # (200, 10)
```

### Buy X Get Y 促销
```python
from discount_utils.mod import apply_buy_x_get_y, calculate_free_items

# 买2送1，买3件单价$10
total = apply_buy_x_get_y(10, 3, 2, 1)  # 20.0 (付2件钱)

# 免费商品数量
free = calculate_free_items(6, 2, 1)  # 2件免费
```

### 完整价格明细
```python
from discount_utils.mod import Discount, calculate_complete_breakdown, DiscountType

d1 = Discount(DiscountType.PERCENTAGE, 10, '会员折扣')
d2 = Discount(DiscountType.PERCENTAGE, 5, '优惠券')

breakdown = calculate_complete_breakdown(
    original_price=100,
    discounts=[d1, d2],
    tax_rate=10  # 10%税费
)

print(f"原价: ${breakdown.original_price}")
print(f"折扣后: ${breakdown.subtotal_after_discount}")
print(f"税费: ${breakdown.tax_amount}")
print(f"最终价格: ${breakdown.final_price}")
print(f"节省: ${breakdown.total_savings} ({breakdown.savings_percentage}%)")
```

### 价格比较
```python
from discount_utils.mod import compare_prices

result = compare_prices([
    ('亚马逊', 100, 10),   # 原价100，10%折扣
    ('京东', 95, 0),       # 原价95，无折扣
    ('天猫', 98, 5),       # 原价98，5%折扣
])

print(f"最优惠: {result['best_source']} 价格 ${result['best_price']}")
```

## 预定义常量

### 常用折扣百分比
```python
COMMON_DISCOUNTS = {
    'minimal': 5,
    'small': 10,
    'medium': 15,
    'standard': 20,
    'half': 50,
    'clearance': 60,
    'deep': 70,
    'fire_sale': 90,
}
```

### 各地区税率（近似值）
```python
TAX_RATES = {
    'US_CA': 7.25,  # 加州
    'UK': 20.0,     # 英国VAT
    'CN': 13.0,     # 中国增值税
    'JP': 10.0,     # 日本消费税
}
```

## 测试

运行测试：
```bash
python3 test_mod.py
```

所有41个测试均已通过。

## 作者

AllToolkit Contributors

## 许可证

MIT License