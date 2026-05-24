# Luhn Utils 💳

Luhn 算法工具模块，提供信用卡号验证、IMEI 验证、校验位计算等功能。

## 特性

- ✅ **Luhn 校验** - 验证数字是否通过 Luhn 算法
- ✅ **校验位计算** - 为数字生成校验位
- ✅ **信用卡验证** - 完整的信用卡号验证
- ✅ **卡类型识别** - Visa、MasterCard、AmEx 等识别
- ✅ **IMEI 验证** - 国际移动设备识别码验证
- ✅ **测试卡生成** - 生成测试用信用卡号
- ✅ **卡号格式化** - 4 位分组格式化
- ✅ **卡号遮蔽** - 安全显示卡号

## 快速开始

### Luhn 校验验证

```python
from luhn_utils import validate

# 验证卡号
is_valid = validate("4532015112830366")
print(is_valid)  # True

# 无效卡号
is_valid = validate("4532015112830367")
print(is_valid)  # False

# 支持空格和连字符
is_valid = validate("4532-0151-1283-0366")
print(is_valid)  # True
```

### 计算校验位

```python
from luhn_utils import calculate_check_digit, generate_with_check_digit

# 计算校验位
check = calculate_check_digit("7992739871")
print(check)  # 3

# 生成完整数字
full = generate_with_check_digit("7992739871")
print(full)  # '79927398713'
```

### 识别信用卡类型

```python
from luhn_utils import identify_card_type

# Visa 卡
card_type = identify_card_type("4532015112830366")
print(card_type)  # 'Visa'

# MasterCard
card_type = identify_card_type("5555555555554444")
print(card_type)  # 'MasterCard'

# American Express
card_type = identify_card_type("378282246310005")
print(card_type)  # 'American Express'

# 未知类型
card_type = identify_card_type("1234567890123456")
print(card_type)  # None
```

### 完整信用卡验证

```python
from luhn_utils import validate_card

is_valid, card_type, formatted = validate_card("4532015112830366")
print(f"有效: {is_valid}")      # True
print(f"类型: {card_type}")     # Visa
print(f"格式化: {formatted}")   # '4532 0151 1283 0366'
```

### 格式化卡号

```python
from luhn_utils import format_card_number

# 空格分隔
formatted = format_card_number("4532015112830366")
print(formatted)  # '4532 0151 1283 0366'

# 连字符分隔
formatted = format_card_number("4532015112830366", "-")
print(formatted)  # '4532-0151-1283-0366'
```

### 遮蔽卡号

```python
from luhn_utils import mask_card_number

# 默认遮蔽（显示前 4 位和后 4 位）
masked = mask_card_number("4532015112830366")
print(masked)  # '4532********0366'

# 自定义显示位数
masked = mask_card_number("4532015112830366", show_first=6, show_last=2)
print(masked)  # '453201********66'
```

### 生成测试卡号

```python
from luhn_utils import generate_test_card

# Visa 测试卡
visa_card = generate_test_card("Visa")
print(visa_card)
print(validate(visa_card))  # True

# MasterCard
mc_card = generate_test_card("MasterCard")
print(validate(mc_card))  # True

# American Express
amex_card = generate_test_card("American Express")
print(validate(amex_card))  # True
```

### IMEI 验证

```python
from luhn_utils import validate_imei, generate_imei

# 验证 IMEI
is_valid = validate_imei("490154203237518")
print(is_valid)  # True

# 生成 IMEI
imei = generate_imei()
print(imei)
print(validate_imei(imei))  # True

# 自定义 TAC 和序列号
imei = generate_imei(tac="01234567", serial="123456")
print(imei)  # '01234567123456X' (X 为校验位)
```

### 提取完整信息

```python
from luhn_utils import extract_luhn_info

info = extract_luhn_info("4532015112830366")
print(info)
# {
#   'valid': True,
#   'number': '4532015112830366',
#   'length': 16,
#   'card_type': 'Visa',
#   'formatted': '4532 0151 1283 0366',
#   'masked': '4532********0366',
#   'check_digit': '6',
#   'check_digit_correct': True
# }
```

## 支持的信用卡类型

| 类型 | 前缀规则 | 长度 |
|------|----------|------|
| Visa | 以 4 开头 | 13/16 |
| MasterCard | 51-55 或 22-27 | 16 |
| American Express | 34 或 37 | 15 |
| Discover | 6011 或 65 | 16 |
| JCB | 2131/1800/35 | 15/16 |
| Diners Club | 30/36/38 | 14 |
| UnionPay | 以 62 开头 | 16-19 |

## Luhn 算法原理

Luhn 算法（又称"模 10"算法）是一种简单的校验算法：

1. 从右向左，每隔一位数字翻倍
2. 如果翻倍后大于 9，减去 9
3. 计算所有数字的总和
4. 如果总和能被 10 整除，则有效

示例：验证 `4532015112830366`

```
原始数字: 4  5  3  2  0  1  5  1  1  2  8  3  0  3  6  6
处理规则: ×2 ×1 ×2 ×1 ×2 ×1 ×2 ×1 ×2 ×1 ×2 ×1 ×2 ×1 ×2 ×1
处理后:   8  5  6  2  0  1 10  1  2  2 16  3  0  3 12  6
减9调整:  8  5  6  2  0  1  1  1  2  2  7  3  0  3  3  6
总和: 60 → 60 % 10 = 0 → 有效 ✓
```

## 测试

```bash
python Python/luhn_utils/luhn_utils_test.py
```

## 测试用例

- Luhn 校验和计算
- 校验位计算
- 有效/无效卡号验证
- 格式化和遮蔽
- 卡类型识别（Visa/MasterCard/AmEx/Discover/JCB）
- 测试卡生成
- IMEI 验证和生成
- 完整信息提取

## 许可证

MIT License

## ⚠️ 安全提示

- 生成的测试卡号仅供开发测试使用
- 真实卡号请勿存储或传输
- 使用遮蔽功能保护用户隐私