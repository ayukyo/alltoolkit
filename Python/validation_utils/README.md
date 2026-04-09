# Validation Utilities - Python

**全面的数据验证工具库 - 零依赖，生产就绪**

## 📖 概述

`validation_utils` 是一个功能强大的数据验证模块，提供丰富的验证函数，适用于各种数据验证场景。所有函数均使用 Python 标准库实现，零外部依赖。

## ✨ 特性

- **全面的验证器** - 支持邮箱、URL、电话、IP、信用卡、身份证等
- **日期时间验证** - 支持多种日期时间格式
- **数值范围验证** - 支持整数、浮点数范围检查
- **字符串验证** - 支持长度、正则模式匹配
- **组合验证器** - 支持 `all_of`、`any_of`、`optional` 组合
- **批量验证** - `Validator` 类支持多字段批量验证
- **详细错误信息** - 包含字段名和具体错误原因
- **类型安全** - 完整的类型注解支持

## 🚀 快速开始

### 安装

无需安装，直接复制 `mod.py` 到项目中使用：

```python
from mod import is_email, is_phone, is_url, Validator
```

### 基本用法

```python
from mod import is_email, is_phone, validate_url

# 验证邮箱
result = is_email("user@example.com")
if result.is_valid:
    print("邮箱有效！")
else:
    print(f"邮箱无效：{result.error}")

# 快速验证函数
if validate_email("test@example.com"):
    print("✓ 邮箱格式正确")

# 验证中国手机号
if is_phone("13812345678", country='CN').is_valid:
    print("✓ 手机号格式正确")

# 验证 URL
if validate_url("https://example.com"):
    print("✓ URL 格式正确")
```

## 📚 API 参考

### 基础验证器

#### `is_not_none(value, field=None)`
检查值是否不为 None。

```python
is_not_none("hello")  # ValidationResult(valid=True)
is_not_none(None)     # ValidationResult(valid=False)
```

#### `is_not_empty(value, field=None)`
检查值是否不为空（字符串、列表、字典等）。

```python
is_not_empty("hello")  # valid
is_not_empty("")       # invalid
is_not_empty([])       # invalid
is_not_empty(0)        # valid (0 is not empty)
```

#### `is_type(value, expected_type, field=None)`
检查值是否为指定类型。

```python
is_type(42, int)       # valid
is_type("42", int)     # invalid
is_type(3.14, float)   # valid
```

#### `is_in(value, choices, field=None)`
检查值是否在允许的选项中。

```python
is_in("a", ["a", "b", "c"])  # valid
is_in("d", ["a", "b", "c"])  # invalid
```

### 字符串验证器

#### `is_email(value, field=None)`
验证邮箱地址格式。

```python
is_email("user@example.com")     # valid
is_email("invalid-email")        # invalid
is_email("@example.com")         # invalid
```

#### `is_url(value, field=None, allowed_schemes=None)`
验证 URL 格式。

```python
is_url("https://example.com")           # valid
is_url("http://localhost:8080/api")     # valid
is_url("ftp://example.com")             # invalid (only http/https)

# 限制 scheme
is_url("https://example.com", allowed_schemes=["https"])  # valid
is_url("http://example.com", allowed_schemes=["https"])   # invalid
```

#### `is_phone(value, country='CN', field=None)`
验证电话号码格式。

```python
# 中国手机号
is_phone("13812345678", country='CN')    # valid
is_phone("13 8123 4567 8", country='CN') # valid (自动清理分隔符)

# 美国手机号
is_phone("2125551234", country='US')     # valid
is_phone("(212) 555-1234", country='US') # valid
```

#### `is_chinese_id(value, field=None)`
验证中国居民身份证号码（18 位）。

```python
is_chinese_id("11010519491231002X")  # valid
is_chinese_id("123456789012345678")  # invalid
```

包含校验位验证，确保身份证号码真实有效。

#### `is_credit_card(value, card_type=None, field=None)`
验证信用卡号码（使用 Luhn 算法）。

```python
is_credit_card("4532015112830366", card_type='visa')      # valid
is_credit_card("5425233430109903", card_type='mastercard') # valid
is_credit_card("374245455400126", card_type='amex')       # valid

# 不指定卡类型
is_credit_card("4532015112830366")  # valid
```

支持的卡类型：`visa`, `mastercard`, `amex`, `discover`, `jcb`

### IP 地址验证器

#### `is_ipv4(value, field=None)`
验证 IPv4 地址格式。

```python
is_ipv4("192.168.1.1")     # valid
is_ipv4("255.255.255.255") # valid
is_ipv4("256.1.1.1")       # invalid
is_ipv4("192.168.1")       # invalid
```

#### `is_ipv6(value, field=None)`
验证 IPv6 地址格式。

```python
is_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")  # valid
is_ipv6("::1")                                      # valid
is_ipv6("::")                                       # valid
```

#### `is_ip(value, version=None, field=None)`
验证 IP 地址（IPv4 或 IPv6）。

```python
is_ip("192.168.1.1")              # valid (either)
is_ip("::1")                      # valid (either)
is_ip("192.168.1.1", version=4)   # valid (IPv4 only)
is_ip("::1", version=6)           # valid (IPv6 only)
is_ip("::1", version=4)           # invalid
```

### 日期时间验证器

#### `is_date(value, format='YYYY-MM-DD', field=None)`
验证日期字符串格式。

```python
is_date("2024-01-15")              # valid
is_date("2024/01/15", 'YYYY/MM/DD') # valid
is_date("15-01-2024", 'DD-MM-YYYY') # valid
is_date("01/15/2024", 'MM/DD/YYYY') # valid

# 无效日期
is_date("2024-13-01")  # invalid (月份无效)
is_date("2024-02-30")  # invalid (日期无效)
is_date("2023-02-29")  # invalid (非闰年)
```

支持的格式：`YYYY-MM-DD`, `YYYY/MM/DD`, `DD-MM-YYYY`, `MM/DD/YYYY`

#### `is_time(value, format='HH:MM:SS', field=None)`
验证时间字符串格式。

```python
is_time("09:30", 'HH:MM')           # valid
is_time("12:30:45", 'HH:MM:SS')     # valid
is_time("12:30:45.123", 'HH:MM:SS.fff')  # valid

is_time("25:00")  # invalid
is_time("12:60")  # invalid
```

#### `is_datetime(value, format='%Y-%m-%d %H:%M:%S', field=None)`
验证日期时间字符串格式。

```python
is_datetime("2024-01-15 09:30:00")  # valid
is_datetime("2024-01-15T09:30:00", '%Y-%m-%dT%H:%M:%S')  # valid
```

### 数值验证器

#### `is_number(value, field=None)`
检查值是否为数字（int 或 float）。

```python
is_number(42)       # valid
is_number(3.14)     # valid
is_number(True)     # invalid (bool excluded)
is_number("42")     # invalid
```

#### `is_integer(value, field=None)`
检查值是否为整数。

```python
is_integer(42)      # valid
is_integer(3.14)    # invalid
is_integer(True)    # invalid
```

#### `in_range(value, min_val=None, max_val=None, field=None)`
检查数值是否在指定范围内。

```python
in_range(5, 0, 10)     # valid
in_range(0, 0, 10)     # valid (边界)
in_range(10, 0, 10)    # valid (边界)
in_range(-1, 0, 10)    # invalid
in_range(11, 0, 10)    # invalid

# 单边限制
in_range(-100, max_val=10)  # valid
in_range(100, min_val=0)    # valid
```

#### `is_positive(value, field=None)`
检查数值是否为正数（> 0）。

```python
is_positive(1)    # valid
is_positive(0)    # invalid
is_positive(-1)   # invalid
```

#### `is_non_negative(value, field=None)`
检查数值是否为非负数（>= 0）。

```python
is_non_negative(0)    # valid
is_non_negative(1)    # valid
is_non_negative(-1)   # invalid
```

### 字符串长度验证器

#### `has_length(value, min_len=None, max_len=None, field=None)`
检查字符串长度是否在指定范围内。

```python
has_length("hello", 3, 10)    # valid
has_length("ab", 3, 10)       # invalid (太短)
has_length("abcdefghijk", 3, 10)  # invalid (太长)

# 单边限制
has_length("a", max_len=10)       # valid
has_length("very long", min_len=5) # valid
```

#### `matches_pattern(value, pattern, field=None)`
检查字符串是否匹配正则表达式。

```python
import re
matches_pattern("abc123", r'^[a-z]+\d+$')  # valid
matches_pattern("123abc", r'^[a-z]+\d+$')  # invalid

# 使用编译后的模式
pattern = re.compile(r'^test$')
matches_pattern("test", pattern)  # valid
```

### 组合验证器

#### `all_of(validators, field=None)`
创建组合验证器，要求所有验证器都通过。

```python
from mod import all_of, is_type, has_length

# 必须是字符串且长度在 3-10 之间
validator = all_of([
    lambda v, f: is_type(v, str, f),
    lambda v, f: has_length(v, 3, 10, f),
])

validator("hello")   # valid
validator("hi")      # invalid (太短)
validator(123)       # invalid (类型错误)
```

#### `any_of(validators, field=None)`
创建组合验证器，要求至少一个验证器通过。

```python
from mod import any_of, is_email, is_phone

# 可以是邮箱或手机号
validator = any_of([
    lambda v, f: is_email(v, f),
    lambda v, f: is_phone(v, 'CN', f),
])

validator("test@example.com")  # valid (邮箱)
validator("13812345678")       # valid (手机号)
validator("invalid")           # invalid
```

#### `optional(validator, field=None)`
创建可选验证器，允许 None 值。

```python
from mod import optional, is_email

opt_email = optional(is_email)

opt_email(None)              # valid
opt_email("test@example.com") # valid
opt_email("invalid")         # invalid
```

### 批量验证

#### `Validator` 类

用于定义和执行多字段批量验证规则。

```python
from mod import Validator, is_email, in_range, has_length

# 创建验证器
validator = Validator()
validator.rule('email', is_email)
validator.rule('age', lambda v, f: in_range(v, 0, 150, f))
validator.rule('name', lambda v, f: has_length(v, 1, 50, f) if v else 
               ValidationResult(False, v, error="Name required"))

# 验证数据
valid_data = {'email': 'test@example.com', 'age': 25, 'name': 'John'}
result = validator.validate(valid_data)

if result.is_valid:
    print("✓ 数据验证通过")
else:
    print(f"✗ 验证失败：{validator.get_errors()}")

# 严格模式（不允许未知字段）
result = validator.validate(valid_data, strict=True)

# 方法链式调用
chained = (Validator()
    .rule('a', is_integer)
    .rule('b', is_email))

# 抛出异常
try:
    validator.raise_if_invalid({'email': 'invalid', 'age': 200})
except ValidationError as e:
    print(f"验证失败：{e}")
```

### 便捷函数

模块提供一系列便捷函数，直接返回布尔值：

```python
from mod import (
    validate_email, validate_url, validate_phone,
    validate_credit_card, validate_chinese_id,
    validate_ipv4, validate_ipv6, validate_date, validate_range
)

validate_email("test@example.com")    # True
validate_url("https://example.com")   # True
validate_phone("13812345678")         # True
validate_credit_card("4532015112830366")  # True
validate_chinese_id("11010519491231002X") # True
validate_ipv4("192.168.1.1")          # True
validate_ipv6("::1")                  # True
validate_date("2024-01-15")           # True
validate_range(5, 0, 10)              # True
```

## 📋 ValidationResult

所有验证函数返回 `ValidationResult` 对象：

```python
class ValidationResult:
    is_valid: bool      # 验证是否通过
    value: Any          # 验证的值（可能已被清理）
    error: str | None   # 错误信息（如果验证失败）
    field: str | None   # 字段名（如果提供）
    
    # 方法
    __bool__() -> bool  # 支持 if result: 语法
    to_dict() -> dict   # 转换为字典
```

使用示例：

```python
result = is_email("test@example.com")

# 检查是否有效
if result.is_valid:
    print("✓ 验证通过")

# 布尔上下文
if result:
    print("✓ 验证通过")

# 获取错误信息
if not result:
    print(f"✗ 错误：{result.error}")

# 转换为字典
data = result.to_dict()
# {'valid': True, 'value': 'test@example.com', 'error': None, 'field': None}
```

## 🧪 运行测试

```bash
cd AllToolkit/Python/validation_utils
python validation_utils_test.py
```

测试覆盖：
- 正常场景验证
- 边界值测试
- 异常情况处理
- 类型错误处理
- 组合验证器测试
- 批量验证测试

## 💡 实用示例

### 用户注册表单验证

```python
from mod import Validator, is_email, is_phone, has_length, in_range, all_of

# 创建用户验证器
user_validator = Validator()

# 邮箱验证
user_validator.rule('email', is_email)

# 手机号验证
user_validator.rule('phone', lambda v, f: is_phone(v, 'CN', f))

# 用户名：3-20 字符的字母数字
user_validator.rule('username', all_of([
    lambda v, f: has_length(v, 3, 20, f),
    lambda v, f: __import__('re').match(r'^[a-zA-Z0-9_]+$', v) 
                 and ValidationResult(True, v) 
                 or ValidationResult(False, v, error="Username can only contain letters, numbers, and underscores")
]))

# 年龄：18-120
user_validator.rule('age', lambda v, f: in_range(v, 18, 120, f))

# 验证用户数据
user_data = {
    'email': 'user@example.com',
    'phone': '13812345678',
    'username': 'john_doe',
    'age': 25
}

result = user_validator.validate(user_data)
if result.is_valid:
    print("✓ 用户数据验证通过，可以注册")
else:
    print("✗ 验证失败:")
    for field, error in user_validator.get_errors().items():
        print(f"  - {field}: {error}")
```

### API 请求参数验证

```python
from mod import is_url, is_integer, in_range, optional

def validate_api_request(params: dict) -> tuple[bool, dict]:
    """验证 API 请求参数"""
    errors = {}
    
    # 验证回调 URL（可选）
    if 'callback_url' in params:
        result = optional(is_url)(params['callback_url'], 'callback_url')
        if not result.is_valid:
            errors['callback_url'] = result.error
    
    # 验证页码
    if 'page' in params:
        result = in_range(params['page'], 1, 1000, 'page')
        if not result.is_valid:
            errors['page'] = result.error
    
    # 验证每页数量
    if 'per_page' in params:
        result = in_range(params['per_page'], 1, 100, 'per_page')
        if not result.is_valid:
            errors['per_page'] = result.error
    
    return len(errors) == 0, errors
```

### 数据清洗和验证

```python
from mod import is_email, is_phone, is_chinese_id

def clean_and_validate_user_data(data: dict) -> dict:
    """清洗并验证用户数据"""
    cleaned = {}
    errors = {}
    
    # 邮箱
    if data.get('email'):
        result = is_email(data['email'].strip().lower())
        if result.is_valid:
            cleaned['email'] = result.value
        else:
            errors['email'] = result.error
    
    # 手机号（自动清理格式）
    if data.get('phone'):
        result = is_phone(data['phone'], 'CN')
        if result.is_valid:
            cleaned['phone'] = result.value  # 已清理的号码
        else:
            errors['phone'] = result.error
    
    # 身份证（自动转大写）
    if data.get('id_card'):
        result = is_chinese_id(data['id_card'])
        if result.is_valid:
            cleaned['id_card'] = result.value
        else:
            errors['id_card'] = result.error
    
    return {
        'success': len(errors) == 0,
        'data': cleaned,
        'errors': errors
    }
```

## 🔒 安全注意事项

1. **信用卡验证**：本模块仅验证卡号格式和 Luhn 校验，不验证卡片是否真实有效。生产环境请使用支付网关 API。

2. **身份证验证**：本模块验证格式和校验位，不验证身份证是否真实存在。

3. **输入清理**：部分验证器（如电话、信用卡）会返回清理后的值，建议使用返回的 `result.value` 而非原始输入。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**版本**: 1.0.0  
**最后更新**: 2026-04-09  
**作者**: AllToolkit Contributors
