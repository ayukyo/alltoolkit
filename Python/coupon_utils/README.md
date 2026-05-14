# Coupon Utils 🎫

优惠券工具模块 - 提供优惠券生成、验证、折扣计算等完整功能。

## 功能特性

- **多种优惠券格式** - 字母数字、纯数字、语音友好、自定义模式
- **校验码验证** - 防止优惠券输入错误
- **多种折扣类型** - 百分比、固定金额、买一送一、阶梯折扣
- **过期日期处理** - 有效期管理
- **批量生成** - 支持批量生成并去重
- **使用追踪** - 辅助使用状态管理

## 快速开始

```python
from coupon_utils.mod import CouponGenerator, CouponConfig, DiscountType

# 创建优惠券生成器
generator = CouponGenerator()

# 生成单个优惠券
coupon = generator.generate()
print(coupon)  # "SAVE-20XX-XXXX"

# 批量生成优惠券
coupons = generator.generate_batch(100)
print(f"生成了 {len(coupons)} 个优惠券")

# 自定义配置
config = CouponConfig(
    prefix="PROMO",
    length=10,
    format=CouponFormat.ALPHANUMERIC,
    include_checksum=True
)
generator = CouponGenerator(config)
```

## 核心类

### CouponGenerator

```python
from coupon_utils.mod import CouponGenerator, CouponFormat

generator = CouponGenerator()

# 基础生成
coupon = generator.generate()

# 带校验码的优惠券
coupon = generator.generate_with_checksum()

# 批量生成（自动去重）
coupons = generator.generate_batch(count=1000)
```

### CouponValidator

```python
from coupon_utils.mod import CouponValidator

validator = CouponValidator()

# 验证优惠券格式
is_valid = validator.validate_format("SAVE-2024-ABCD")

# 验证校验码
checksum_valid = validator.validate_checksum("SAVE-2024-ABCD-4")

# 完整验证
result = validator.validate("SAVE-2024-ABCD-4")
# {'format_valid': True, 'checksum_valid': True, 'expired': False}
```

## 折扣计算

```python
from coupon_utils.mod import DiscountCalculator, DiscountType

calc = DiscountCalculator()

# 百分比折扣
discount = calc.calculate(
    original_price=100.0,
    discount_type=DiscountType.PERCENTAGE,
    discount_value=20  # 20%
)
print(discount)  # 80.0

# 固定金额折扣
discount = calc.calculate(
    original_price=100.0,
    discount_type=DiscountType.FIXED,
    discount_value=15
)
print(discount)  # 85.0

# 买一送一
result = calc.calculate_bogo(
    item_price=50.0,
    quantity=3,
    buy_count=2,
    get_count=1
)
```

## 优惠券格式

| 格式 | 说明 | 示例 |
|------|------|------|
| ALPHANUMERIC | 字母数字混合 | A1B2C3D4 |
| NUMERIC | 纯数字 | 12345678 |
| ALPHA | 纯字母 | ABCDEFGH |
| PHONETIC | 语音友好（排除混淆字符） | SAVE-NOW |
| CUSTOM | 自定义字符集 | 按需设置 |

## 配置选项

```python
from coupon_utils.mod import CouponConfig

config = CouponConfig(
    prefix="PROMO",           # 前缀
    suffix="2024",            # 后缀
    length=8,                 # 随机部分长度
    format=CouponFormat.ALPHANUMERIC,
    include_checksum=True,    # 包含校验码
    checksum_length=1,        # 校验码长度
    separator="-",            # 分隔符
    group_size=4,             # 分组大小
    excluded_chars="0O1lI"    # 排除混淆字符
)
```

## 测试

```bash
python Python/coupon_utils/coupon_utils_test.py
```

## 许可证

MIT License