# AllToolkit - Python Email Utils 📧

**零依赖电子邮件处理工具 - 生产就绪**

---

## 📖 概述

`email_utils` 提供全面的电子邮件地址处理功能，包括验证、解析、规范化、分类和批量处理。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **RFC 5322 兼容验证** - 准确的邮箱格式验证
- **智能解析** - 支持带显示名称的邮箱格式
- **Gmail 规范化** - 自动处理 Gmail 的点和 + 标签
- **一次性邮箱检测** - 识别 200+ 个临时邮箱域名
- **免费邮箱识别** - 识别主流免费邮箱服务商
- **批量处理** - 去重、排序、分组、提取
- **隐私保护** - 邮箱混淆显示

---

## 🚀 快速开始

### 基础使用

```python
from mod import validate, parse, normalize, is_disposable

# 验证邮箱
is_valid = validate("user@example.com")  # True

# 解析邮箱
parsed = parse('"John Doe" <john@example.com>')
print(parsed.local)        # "john"
print(parsed.domain)       # "example.com"
print(parsed.display_name) # "John Doe"

# 规范化（Gmail 特殊处理）
normalize("John.Doe+tag@Gmail.com")  # "johndoe@gmail.com"

# 检测一次性邮箱
is_disposable("user@mailinator.com")  # True
```

### 高级功能

```python
from mod import (
    extract_from_text, deduplicate, 
    group_by_domain, sort_by_domain, obfuscate
)

# 从文本提取邮箱
text = "Contact: support@example.com or sales@example.com"
emails = extract_from_text(text)

# 去重（支持 Gmail 规范化）
emails = deduplicate([
    "User@Gmail.com",
    "user@gmail.com", 
    "u.s.e.r@gmail.com"
])  # 返回 ["User@Gmail.com"]

# 按域名分组
grouped = group_by_domain([
    "a@gmail.com", "b@gmail.com", "c@yahoo.com"
])
# {"gmail.com": ["a@gmail.com", "b@gmail.com"], "yahoo.com": ["c@yahoo.com"]}

# 混淆显示
obfuscate("john.doe@example.com", show_chars=2)  # "jo*******@example.com"
```

---

## 📚 API 参考

### 验证函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `validate(email)` | 验证邮箱格式 | `bool` |
| `parse(email)` | 解析邮箱为组件 | `EmailAddress` 或 `None` |
| `normalize(email)` | 规范化邮箱 | `str` 或 `None` |

### 分类函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `is_disposable(email)` | 是否一次性邮箱 | `bool` |
| `is_free_provider(email)` | 是否免费邮箱服务商 | `bool` |
| `get_domain(email)` | 提取域名 | `str` 或 `None` |
| `get_local(email)` | 提取本地部分 | `str` 或 `None` |

### 格式化函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `obfuscate(email, show_chars)` | 混淆邮箱显示 | `str` 或 `None` |
| `format_with_name(email, name)` | 格式化带名称的邮箱 | `str` 或 `None` |

### 批量处理函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `extract_from_text(text)` | 从文本提取所有邮箱 | `List[str]` |
| `deduplicate(emails)` | 去重邮箱列表 | `List[str]` |
| `sort_by_domain(emails)` | 按域名排序 | `List[str]` |
| `group_by_domain(emails)` | 按域名分组 | `Dict[str, List[str]]` |

---

## 📋 EmailAddress 数据结构

`parse()` 函数返回的 `EmailAddress` 数据类包含：

```python
@dataclass
class EmailAddress:
    local: str              # @ 前部分
    domain: str             # @ 后部分
    original: str           # 原始字符串
    normalized: str         # 规范化版本
    is_valid: bool          # 验证结果
    display_name: str|None  # 显示名称（如有）
```

---

## 🔍 验证规则

邮箱验证遵循以下规则：

1. **格式检查**: `local@domain.tld`
2. **本地部分**: 最多 64 字符，允许字母、数字和 `._%+-`
3. **域名**: 最多 255 字符，有效 TLD（2+ 字母）
4. **禁止**: 连续点号、首尾点号、空格

---

## 🎯 Gmail 特殊处理

Gmail 邮箱规范化包含：

1. **忽略点号**: `first.last@gmail.com` → `firstlast@gmail.com`
2. **忽略 + 标签**: `user+tag@gmail.com` → `user@gmail.com`
3. **域名统一**: `@googlemail.com` 视为 `@gmail.com`

---

## 📊 一次性邮箱检测

支持检测 200+ 个已知一次性/临时邮箱域名，包括：

- mailinator.com
- 10minutemail.com
- guerrillamail.com
- yopmail.com
- trashmail.com
- ... (完整列表见源码)

---

## 🆚 免费邮箱服务商

识别主流免费邮箱服务商：

- Gmail / Google Mail
- Yahoo Mail
- Hotmail / Outlook / Live
- iCloud / Me / Mac
- ProtonMail / Tutanota
- QQ / 163 / 126 (中国)
- Yandex / Mail.ru (俄罗斯)
- ... (完整列表见源码)

---

## 🧪 运行测试

```bash
cd email_utils
python email_utils_test.py -v
```

### 测试覆盖

- ✅ 有效/无效邮箱验证
- ✅ 边界情况处理
- ✅ 解析带显示名称的邮箱
- ✅ Gmail 规范化（点号、+ 标签）
- ✅ 一次性邮箱检测
- ✅ 免费邮箱识别
- ✅ 邮箱混淆
- ✅ 文本提取
- ✅ 去重（含规范化）
- ✅ 排序和分组
- ✅ 完整工作流程集成测试

---

## 💡 使用场景

### 1. 用户注册验证

```python
def validate_registration(email: str) -> bool:
    if not validate(email):
        return False, "Invalid email format"
    if is_disposable(email):
        return False, "Disposable emails not allowed"
    return True, "OK"
```

### 2. 联系人列表清理

```python
def clean_contacts(raw_text: str) -> list:
    extracted = extract_from_text(raw_text)
    valid = [e for e in extracted if validate(e)]
    return deduplicate(valid)
```

### 3. 邮件列表分析

```python
def analyze_list(emails: list) -> dict:
    return {
        "total": len(emails),
        "valid": len([e for e in emails if validate(e)]),
        "disposable": len([e for e in emails if is_disposable(e)]),
        "business": len([e for e in emails if not is_free_provider(e)]),
    }
```

---

## ⚠️ 注意事项

1. **不验证邮箱是否存在**: 仅验证格式，不检查邮箱是否真实存在
2. **不发送验证邮件**: 需要实际验证请发送确认邮件
3. **DNS 查询**: 不进行 MX 记录查询（保持零依赖）
4. **大小写**: 域名比较不区分大小写，本地部分保留原样

---

## 📁 文件结构

```
email_utils/
├── mod.py                      # 主要实现
├── email_utils_test.py         # 测试套件 (40+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例
    └── advanced_example.py     # 高级使用示例
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
