# AllToolkit - Python Phone Utils 📱

**零依赖电话号码处理工具 - 生产就绪**

---

## 📖 概述

`phone_utils` 提供全面的电话号码处理功能，包括验证、解析、格式化、规范化、国家检测和类型识别。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **国际格式验证** - 支持 100+ 国家/地区
- **智能解析** - 自动识别国家代码和国内号码
- **多格式输出** - E.164、国际格式、国内格式
- **国家检测** - 从号码自动识别国家/地区
- **类型识别** - 区分手机、固话、免费电话、付费电话
- **批量处理** - 提取、去重、排序、分组
- **隐私保护** - 号码脱敏显示

---

## 🚀 快速开始

### 基础使用

```python
from mod import validate, parse, normalize, get_country

# 验证号码
is_valid = validate("+8613812345678")  # True

# 解析号码
parsed = parse("+1-234-567-8900")
print(parsed.country_code)     # "+1"
print(parsed.national_number)  # "2345678900"
print(parsed.country)          # "US"
print(parsed.e164)             # "+12345678900"

# 规范化（E.164 格式）
normalize("+1 (234) 567-8900")  # "+12345678900"

# 检测国家
get_country("+447911123456")  # "GB"
```

### 高级功能

```python
from mod import (
    is_mobile, is_toll_free, get_number_type,
    extract_from_text, deduplicate, group_by_country, mask
)

# 检测号码类型
is_mobile("+8613812345678", "CN")  # True
is_toll_free("+18001234567", "US")  # True

# 从文本提取号码
text = "Contact: +1-234-567-8900 or +86 138 1234 5678"
phones = extract_from_text(text)

# 去重（基于 E.164 格式）
unique = deduplicate([
    "+1-234-567-8900",
    "+12345678900",
    "(234) 567-8900",
])

# 按国家分组
grouped = group_by_country([
    "+12345678900",
    "+8613812345678",
    "+447911123456",
])

# 脱敏显示
mask("+12345678900")  # "+1 ******8900"
mask("+8613812345678", show_last=4)  # "+86 *******5678"
```

---

## 📚 API 参考

### 验证函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `validate(phone, country)` | 验证号码格式 | `bool` |
| `parse(phone, default_country)` | 解析号码为组件 | `PhoneNumber` 或 `None` |
| `normalize(phone, default_country)` | 规范化为 E.164 | `str` 或 `None` |

### 格式化函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `format_international(phone, country)` | 国际格式 | `str` 或 `None` |
| `format_national(phone, country)` | 国内格式 | `str` 或 `None` |
| `mask(phone, show_last)` | 脱敏显示 | `str` 或 `None` |

### 国家检测函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `get_country_code(phone)` | 提取国家代码 | `str` 或 `None` |
| `get_country(phone)` | 检测国家（ISO 代码） | `str` 或 `None` |
| `get_country_name(code)` | 获取国家名称 | `str` 或 `None` |

### 类型检测函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `get_number_type(phone, country)` | 获取号码类型 | `str` 或 `None` |
| `is_mobile(phone, country)` | 是否手机号 | `bool` |
| `is_landline(phone, country)` | 是否固话 | `bool` |
| `is_toll_free(phone, country)` | 是否免费电话 | `bool` |

### 批量处理函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `extract_from_text(text)` | 从文本提取所有号码 | `List[str]` |
| `deduplicate(phones, country)` | 去重号码列表 | `List[str]` |
| `sort_by_country(phones)` | 按国家代码排序 | `List[str]` |
| `group_by_country(phones)` | 按国家分组 | `Dict[str, List[str]]` |

---

## 📋 PhoneNumber 数据结构

`parse()` 函数返回的 `PhoneNumber` 数据类包含：

```python
@dataclass
class PhoneNumber:
    country_code: str       # 国家代码（如 "+1", "+86"）
    national_number: str    # 国内号码（不含国家代码）
    original: str           # 原始输入字符串
    international: str      # 国际格式
    national: str           # 国内格式
    e164: str               # E.164 标准格式
    country: str            # ISO 3166-1 国家代码
    is_valid: bool          # 验证结果
    number_type: str        # "mobile", "landline", "toll_free", "premium"
```

---

## 🌍 支持的国家/地区

支持 100+ 国家/地区，包括：

| 国家代码 | 国家 | 号码长度 | 手机前缀 |
|----------|------|----------|----------|
| +1 | 美国/加拿大 | 10 | 全部 |
| +86 | 中国 | 11 | 13-19 |
| +44 | 英国 | 10-11 | 7 |
| +49 | 德国 | 10-12 | 15-17 |
| +33 | 法国 | 9-10 | 6-7 |
| +81 | 日本 | 9-11 | 70/80/90 |
| +82 | 韩国 | 9-11 | 10 |
| +91 | 印度 | 10 | 6-9 |
| +61 | 澳大利亚 | 9-10 | 4 |
| +55 | 巴西 | 10-11 | 9 |
| +7 | 俄罗斯 | 10-11 | 9 |
| +39 | 意大利 | 9-11 | 3 |
| +34 | 西班牙 | 9 | 6-7 |
| +52 | 墨西哥 | 10 | 1 |
| +62 | 印尼 | 10-13 | 8 |
| +90 | 土耳其 | 10 | 5 |
| +966 | 沙特 | 9 | 5 |
| +54 | 阿根廷 | 10 | 9 |
| +27 | 南非 | 9 | 6-8 |
| +65 | 新加坡 | 8 | 8-9 |

*完整列表见源码 `COUNTRY_CODES` 字典*

---

## 🔍 验证规则

号码验证遵循以下规则：

1. **最小长度**: 7 位数字
2. **最大长度**: 15 位数字（E.164 标准）
3. **国家特定**: 每个国家有特定长度范围
4. **字符合法**: 仅允许数字、空格、括号、连字符、点号、加号

---

## 📊 号码类型检测

### 手机号 (mobile)
根据各国手机号段前缀识别：
- 中国：13x, 14x, 15x, 16x, 17x, 18x, 19x
- 英国：7xxx
- 德国：15x, 16x, 17x
- 美国：全部 NANP 号码均可作为手机

### 固话 (landline)
非手机、非免费、非付费的号码默认为固话。

### 免费电话 (toll_free)
- 美国：800, 833, 844, 855, 866, 877, 888
- 中国：400, 800
- 英国：800, 808
- 德国：800

### 付费电话 (premium)
- 美国：900
- 中国：96x, 95x
- 英国：87x, 90x
- 德国：137, 138, 190

---

## 🧪 运行测试

```bash
cd phone_utils
python phone_utils_test.py -v
```

### 测试覆盖

- ✅ 有效/无效号码验证
- ✅ 带/不带国家代码解析
- ✅ E.164 规范化
- ✅ 国际/国内格式化
- ✅ 国家代码提取
- ✅ 国家检测
- ✅ 号码类型识别（手机/固话/免费/付费）
- ✅ 文本提取
- ✅ 去重（基于 E.164）
- ✅ 排序和分组
- ✅ 脱敏显示
- ✅ 边界情况处理
- ✅ 完整工作流程集成测试

---

## 💡 使用场景

### 1. 用户注册验证

```python
def validate_phone(phone: str, country: str) -> tuple:
    if not validate(phone, country):
        return False, "Invalid phone format"
    
    if not is_mobile(phone, country):
        return False, "Mobile number required"
    
    return True, "OK"
```

### 2. 联系人列表清理

```python
def clean_contacts(raw_text: str) -> list:
    extracted = extract_from_text(raw_text)
    valid = [p for p in extracted if validate(p)]
    return deduplicate(valid)
```

### 3. 国际号码格式化

```python
def format_for_display(phone: str, context: str = "public") -> str:
    if context == "public":
        return mask(phone, show_last=4)
    elif context == "international":
        return format_international(phone)
    else:
        return format_national(phone)
```

### 4. 号码列表分析

```python
def analyze_list(phones: list) -> dict:
    grouped = group_by_country(phones)
    return {
        "total": len(phones),
        "countries": len(grouped),
        "mobiles": len([p for p in phones if is_mobile(p)]),
        "toll_free": len([p for p in phones if is_toll_free(p)]),
        "by_country": {k: len(v) for k, v in grouped.items()},
    }
```

### 5. CRM 系统集成

```python
def normalize_crm_contacts(contacts: list) -> list:
    for contact in contacts:
        if 'phone' in contact:
            parsed = parse(contact['phone'])
            if parsed:
                contact['phone_e164'] = parsed.e164
                contact['country'] = parsed.country
                contact['phone_type'] = parsed.number_type
    return contacts
```

---

## ⚠️ 注意事项

1. **不验证号码是否真实存在**: 仅验证格式，不检查号码是否分配或使用
2. **不进行 HL R 查询**: 需要实际验证请通过运营商 API
3. **国家检测限制**: 某些国家共享国家代码（如 +1 美国/加拿大）
4. **号码类型限制**: 类型检测基于前缀规则，可能有误判
5. **本地号码**: 不带国家代码的号码需要指定 `default_country`

---

## 📁 文件结构

```
phone_utils/
├── mod.py                      # 主要实现
├── phone_utils_test.py         # 测试套件 (30+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 🔗 相关资源

- **E.164 标准**: https://www.itu.int/rec/T-REC-E.164
- **ISO 3166-1**: https://www.iso.org/iso-3166-country-codes.html
- **国家代码列表**: https://en.wikipedia.org/wiki/List_of_country_calling_codes

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
