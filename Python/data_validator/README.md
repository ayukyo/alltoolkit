# Data Validator 数据验证工具

全面的数据格式验证工具集，零外部依赖，纯 Python 实现。

## 功能特性

### 支持的验证类型

| 类型 | 函数 | 说明 |
|------|------|------|
| 邮箱 | `validate_email()` | RFC 5322 标准，支持临时邮箱检测、+号别名控制 |
| 中国手机号 | `validate_china_mobile()` | 严格号段验证，运营商识别 |
| 中国身份证 | `validate_china_id()` | 15/18位验证，省份、年龄、性别解析 |
| IPv4 地址 | `validate_ipv4()` | 地址类型检测（私有/公网/环回） |
| IPv6 地址 | `validate_ipv6()` | 标准化、压缩格式、IPv4映射 |
| URL | `validate_url()` | 协议控制、端口验证、安全检测 |
| JSON | `validate_json()` | 格式验证、简化Schema支持 |
| 信用卡 | `validate_credit_card()` | Luhn算法、卡类型识别 |
| 银行卡 | `validate_china_bank_card()` | 中国银行卡验证 |
| 中文姓名 | `validate_chinese_name()` | 常见姓氏识别 |
| 密码 | `validate_password()` | 强度评分、自定义规则 |
| 电话 | `validate_chinese_phone()` | 手机/座机/400/800统一验证 |
| 批量验证 | `validate_batch()` | 批量处理多种类型 |

## 快速使用

```python
from mod import validate_email, validate_china_mobile, validate_china_id

# 邮箱验证
result = validate_email('test@gmail.com')
print(result.is_valid)  # True
print(result.details)   # {'local_part': 'test', 'domain': 'gmail.com', ...}

# 手机号验证（运营商识别）
result = validate_china_mobile('13812345678')
print(result.details['carrier'])  # 中国移动
print(result.details['formatted_with_space'])  # 138 1234 5678

# 身份证验证（解析信息）
result = validate_china_id('110105199003072347')
print(result.details['province'])  # 北京市
print(result.details['age'])       # 年龄
print(result.details['gender'])    # 性别
```

## 验证结果

所有验证函数返回 `ValidationResult` 对象：

```python
class ValidationResult:
    is_valid: bool      # 是否有效
    message: str        # 验证消息
    details: dict       # 详细信息（可选）
    
    # 支持布尔判断
    if result:  # 等同于 result.is_valid
        ...
```

## 详细示例

### 邮箱验证

```python
# 基本验证
validate_email('test@example.com')
validate_email('user+alias@gmail.com')

# 检查域名（拒绝临时邮箱）
validate_email('test@tempmail.com', check_domain=True, allow_temp=False)

# 禁止 +号别名
validate_email('user+tag@gmail.com', allow_plus_alias=False)
```

### 手机号验证

```python
# 严格号段验证
validate_china_mobile('13812345678', strict=True)

# 支持多种格式
validate_china_mobile('+8613812345678')
validate_china_mobile('86 138-1234-5678')

# 返回运营商信息
result = validate_china_mobile('18612345678')
print(result.details['carrier'])  # 中国联通
```

### 身份证验证

```python
# 基本验证
result = validate_china_id('110105199003072347')

# 年龄检查
validate_china_id('...', check_age=True, min_age=18, max_age=65)

# 解析信息
print(result.details['province'])   # 省份
print(result.details['birth_date']) # 出生日期
print(result.details['age'])        # 年龄
print(result.details['gender'])     # 性别（男/女）
```

### IP地址验证

```python
# IPv4
result = validate_ipv4('192.168.1.1')
print(result.details['class'])      # C类私有地址
print(result.details['is_private']) # True
print(result.details['binary'])     # 二进制表示

# IPv6
result = validate_ipv6('2001:db8::1')
print(result.details['normalized']) # 标准化格式
print(result.details['compressed']) # 压缩格式

# 自动检测
validate_ip('192.168.1.1')  # 自动判断 IPv4
validate_ip('::1')          # 自动判断 IPv6
```

### JSON验证

```python
# 基本验证
validate_json('{"key": "value"}')

# Schema验证（简化版）
schema = {
    'type': 'object',
    'required': ['name'],
    'properties': {
        'name': {'type': 'string', 'minLength': 2},
        'age': {'type': 'number', 'minimum': 0, 'maximum': 120}
    }
}
validate_json('{"name": "张三", "age": 25}', schema=schema)
```

### 密码验证

```python
# 基本验证（要求大小写+数字）
validate_password('Password123')

# 自定义规则
validate_password('VeryStrong2024!',
    min_length=10,
    require_special=True,
    special_chars='!@#$%^&*'
)

# 查看强度评分
result = validate_password('StrongPassword123!')
print(result.details['strength'])  # 强/很强/极强
print(result.details['score'])     # 0-8分
```

### 批量验证

```python
emails = ['test@example.com', 'invalid', 'user@gmail.com']
result = validate_batch(emails, 'email')
print(result['valid'])   # 2
print(result['invalid']) # 1

for item in result['items']:
    print(f"{item['input']}: {item['message']}")
```

## 运行测试

```bash
python3 data_validator_test.py
```

## 运行示例

```bash
cd examples
python3 usage_examples.py
```

## 文件结构

```
data_validator/
├── mod.py                 # 主模块（37KB）
├── data_validator_test.py # 测试文件（19KB）
├── README.md              # 说明文档
└── examples/
    └── usage_examples.py  # 使用示例（9KB）
```

## 技术特点

- **零外部依赖**：仅使用 Python 标准库
- **详细返回信息**：每个验证都返回结构化详情
- **灵活配置**：支持自定义规则和参数
- **批量处理**：支持批量验证提高效率
- **类型识别**：自动识别运营商、省份、卡类型等

## 版本

- 创建日期：2026-04-16
- 语言：Python 3
- 作者：AllToolkit 自动生成