# Postal Code Utils - 邮政编码工具

多国邮政编码验证、格式化、提取工具库。支持21个国家/地区的邮政编码处理。

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **多国支持** - 支持21个国家/地区的邮编格式
- **完整功能** - 验证、格式化、标准化、提取、自动检测国家
- **生产就绪** - 完整测试、详细文档、错误处理

## 🌍 支持的国家

| 国家 | 代码 | 格式 | 示例 |
|------|------|------|------|
| 中国 | CN | 6位数字 | 100001 |
| 美国 | US | ZIP (5位) 或 ZIP+4 (5-4位) | 12345, 12345-6789 |
| 日本 | JP | 〒NNN-NNNN | 〒100-0001 |
| 英国 | UK | 复杂格式 | SW1A 1AA |
| 加拿大 | CA | ANA NAN | K1A 0B1 |
| 澳大利亚 | AU | 4位数字 | 2000 |
| 德国 | DE | 5位数字 | 10115 |
| 法国 | FR | 5位数字 | 75001 |
| 韩国 | KR | 5位数字或旧格式 | 04524, 100-101 |
| 印度 | IN | 6位数字(PIN) | 110001 |
| 巴西 | BR | NNNNN-NNN(CEP) | 01311-000 |
| 俄罗斯 | RU | 6位数字 | 101000 |
| 墨西哥 | MX | 5位数字 | 06600 |
| 意大利 | IT | 5位数字(CAP) | 00100 |
| 西班牙 | ES | 5位数字 | 28001 |
| 荷兰 | NL | NNNN XX | 1011 AB |
| 瑞典 | SE | NNN NN | 111 22 |
| 波兰 | PL | NN-NNN | 00-001 |
| 台湾 | TW | 3位或5位数字 | 100, 10001 |
| 香港 | HK | 无标准邮编 | - |
| 新加坡 | SG | 6位数字 | 018956 |

## 🚀 快速开始

### 基本验证

```python
from postal_code_utils import validate_postal_code

# 中国邮编
validate_postal_code("100001", "CN")  # True

# 美国ZIP码
validate_postal_code("12345", "US")  # True
validate_postal_code("12345-6789", "US")  # True

# 英国邮编
validate_postal_code("SW1A 1AA", "UK")  # True

# 加拿大邮编
validate_postal_code("K1A 0B1", "CA")  # True
```

### 格式化

```python
from postal_code_utils import format_postal_code

# 美国ZIP+4格式化
format_postal_code("123456789", "US")  # "12345-6789"

# 日本邮编格式化
format_postal_code("1000001", "JP")  # "〒100-0001"

# 加拿大邮编格式化
format_postal_code("K1A0B1", "CA")  # "K1A 0B1"

# 英国邮编格式化（大小写统一）
format_postal_code("sw1a 1aa", "UK")  # "SW1A 1AA"
```

### 标准化

```python
from postal_code_utils import normalize_postal_code

# 去除空格、连字符等
normalize_postal_code("12345-6789", "US")  # "123456789"
normalize_postal_code("K1A 0B1", "CA")  # "K1A0B1"
normalize_postal_code("〒100-0001", "JP")  # "1000001"
```

### 从文本提取

```python
from postal_code_utils import extract_postal_codes

# 指定国家提取
text = "请寄往北京市 100001 或上海 200001"
codes = extract_postal_codes(text, "CN")  # [("100001", "CN"), ("200001", "CN")]

# 多国家提取
text = "CN: 100001, US: 12345, UK: SW1A 1AA"
codes = extract_postal_codes(text)  # [("100001", "CN"), ("12345", "US"), ("SW1A 1AA", "UK")]
```

### 自动检测国家

```python
from postal_code_utils import detect_country

# 根据格式检测可能的国家
detect_country("K1A 0B1")  # ["CA"] - 加拿大格式唯一
detect_country("SW1A 1AA")  # ["UK"] - 英国格式唯一
detect_country("100001")  # ["CN", "RU", "IN"] - 多个国家可能
detect_country("12345")  # ["US", "DE", "FR", ...] - 多个国家可能
```

### 获取详细信息

```python
from postal_code_utils import get_postal_code_info

info = get_postal_code_info("100001", "CN")
print(info.code)  # "100001"
print(info.is_valid)  # True
print(info.normalized)  # "100001"
print(info.format_type)  # "standard"
```

### 批量验证

```python
from postal_code_utils import batch_validate

batch = [
    ("100001", "CN"),
    ("12345", "US"),
    ("K1A 0B1", "CA"),
    ("invalid", "CN"),
]

result = batch_validate(batch)
print(len(result["valid"]))  # 3
print(len(result["invalid"]))  # 1
```

### 获取附近邮编

```python
from postal_code_utils import get_nearby_postal_codes

# 获取附近邮编（仅适用于数字型邮编）
nearby = get_nearby_postal_codes("100001", "CN", delta=2)
# ["099999", "100000", "100001", "100002", "100003"]
```

## 📚 API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `validate_postal_code(code, country)` | 验证邮编是否有效 |
| `format_postal_code(code, country)` | 格式化邮编 |
| `normalize_postal_code(code, country)` | 标准化邮编（去除空格等） |
| `get_postal_code_info(code, country)` | 获取邮编详细信息 |
| `extract_postal_codes(text, country)` | 从文本提取邮编 |
| `detect_country(code)` | 自动检测可能的国家 |
| `batch_validate(batch)` | 批量验证邮编 |
| `get_supported_countries()` | 获取支持的国家列表 |
| `generate_random_postal_code(country)` | 生成随机邮编（测试用） |

### PostalCodeInfo 数据类

```python
class PostalCodeInfo:
    code: str           # 格式化后的邮编
    country: str        # 国家代码
    is_valid: bool      # 是否有效
    normalized: str     # 标准化格式
    region: str         # 地区/省份（如果可识别）
    format_type: str    # 格式类型
    raw_input: str      # 原始输入
```

### 便捷别名

```python
# 简短别名
validate = validate_postal_code
format = format_postal_code
normalize = normalize_postal_code
info = get_postal_code_info
extract = extract_postal_codes
detect = detect_country
```

## 🧪 测试

```bash
python postal_code_utils_test.py
```

测试覆盖:
- ✅ 21个国家邮编验证
- ✅ 格式化和标准化
- ✅ 文本提取
- ✅ 自动检测国家
- ✅ 批量验证
- ✅ 边界情况处理
- ✅ 大小写和空格处理

## 💡 使用场景

1. **地址验证** - 验证用户输入的邮编是否正确
2. **数据清洗** - 标准化数据库中的邮编格式
3. **表单处理** - 自动格式化和验证邮编字段
4. **文本提取** - 从地址文本中提取邮编
5. **批量处理** - API 或数据处理中的批量验证
6. **测试生成** - 自动生成测试邮编数据

## 📄 许可证

MIT License

---

**作者**: AllToolkit  
**日期**: 2026-05-09  
**版本**: 1.0.0