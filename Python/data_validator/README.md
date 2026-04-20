# Data Validator

纯 Python 数据验证工具包，零外部依赖。

## 功能特性

- ✅ 类型验证（str, int, float, bool, list, dict 等）
- ✅ Schema 结构化验证
- ✅ 自定义验证器与错误消息
- ✅ 嵌套数据结构验证
- ✅ 可选字段与默认值
- ✅ 验证规则（min/max、长度、正则、枚举）
- ✅ 内置常用验证器（email、URL、UUID、IPv4 等）
- ✅ 快捷验证函数

## 快速开始

```python
from mod import Field, Schema, Validators, validate

# 定义 Schema
user_schema = Schema({
    "username": Field(field_type=str, required=True, min_length=3),
    "email": Field(field_type=str, required=True, custom_validator=Validators.email),
    "age": Field(field_type=int, required=False, min_value=0, max_value=150),
    "role": Field(field_type=str, choices=["admin", "user"], default="user")
})

# 验证数据
result = user_schema.validate({
    "username": "johndoe",
    "email": "john@example.com",
    "age": 25
})

if result.is_valid:
    print(f"Valid data: {result.data}")
else:
    for error in result.errors:
        print(f"[{error.field}] {error.message}")
```

## Field 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `field_type` | type | 字段类型（str, int, float, list, dict 等） |
| `required` | bool | 是否必填（默认 True） |
| `default` | Any | 默认值 |
| `min_value` | int/float | 最小值 |
| `max_value` | int/float | 最大值 |
| `min_length` | int | 最小长度 |
| `max_length` | int | 最大长度 |
| `pattern` | str | 正则表达式 |
| `choices` | list | 允许的枚举值 |
| `custom_validator` | Callable | 自定义验证函数 |
| `nested_schema` | Schema | 嵌套对象的 Schema |
| `item_type` | type | 列表元素类型 |

## 内置验证器

```python
from mod import Validators

Validators.email(value)        # 邮箱格式
Validators.url(value)          # URL 格式
Validators.phone(value)        # 电话号码
Validators.uuid(value)         # UUID 格式
Validators.ipv4(value)         # IPv4 地址
Validators.port(value)         # 端口号（0-65535）
Validators.date_iso(value)     # ISO 日期（YYYY-MM-DD）
Validators.datetime_iso(value) # ISO 日期时间
Validators.hex_color(value)    # 十六进制颜色码

# 工厂函数
Validators.password_strength(min_length=8, require_upper=True)
Validators.in_range(min_val, max_val)
Validators.length(min_len, max_len)
```

## 快捷函数

```python
from mod import is_valid_email, is_valid_url, is_valid_phone, is_valid_uuid, is_valid_ipv4

is_valid_email("user@example.com")  # True
is_valid_url("https://example.com")  # True
is_valid_phone("1234567890")         # True
is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")  # True
is_valid_ipv4("192.168.1.1")         # True
```

## 目录结构

```
data_validator/
├── __init__.py      # 模块导出
├── mod.py           # 核心实现
├── tests/
│   └── test_validator.py  # 测试文件
├── examples/
│   └── usage_examples.py  # 使用示例
└── README.md        # 本文档
```

## 运行测试

```bash
cd Python/data_validator
python tests/test_validator.py
```

## 运行示例

```bash
cd Python/data_validator
python examples/usage_examples.py
```

## 许可证

MIT License