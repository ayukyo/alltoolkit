# AllToolkit - Regex Utilities 🔍

**零依赖 Python 正则表达式工具库**

---

## 📖 概述

`regex_utils` 是一个功能强大的正则表达式工具模块，提供常用模式库、验证、提取、替换、匹配等功能。完全使用 Python 标准库实现，无需任何外部依赖。

### 核心功能

- 📋 **预定义模式库**: 35+ 常用正则表达式模式（邮箱、URL、电话、身份证等）
- ✅ **验证函数**: 一键验证各种数据格式
- 🔍 **提取函数**: 从文本中提取邮箱、URL、话题标签等
- 🔄 **替换函数**: 批量替换、脱敏处理
- 🎯 **匹配搜索**: 高级匹配、分组提取
- 🧹 **文本清洗**: 链式调用，轻松清洗文本
- 📦 **批量处理**: 批量验证、过滤、分组

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/regex_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# 验证邮箱
if validate_email("test@example.com"):
    print("有效的邮箱")

# 提取文本中的 URL
text = "访问 https://example.com 获取更多信息"
urls = extract_urls(text)
print(urls)  # ['https://example.com']

# 脱敏处理
phone = "13800138000"
print(censor_phone(phone))  # 138****8000
```

---

## 📚 API 参考

### 验证函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `validate_email(email)` | 验证邮箱 | `validate_email("test@example.com")` → `True` |
| `validate_url(url)` | 验证 URL | `validate_url("https://example.com")` → `True` |
| `validate_phone(phone, region)` | 验证电话 | `validate_phone("13800138000", "cn")` → `True` |
| `validate_date(date_str, format_type)` | 验证日期 | `validate_date("2024-01-15", "iso")` → `True` |
| `validate_id_card(id_card)` | 验证身份证 | `validate_id_card("110101199001011234")` |
| `validate_password(pwd, strength)` | 验证密码 | `validate_password("Pass@123", "strong")` → `True` |
| `validate_hex_color(color)` | 验证颜色 | `validate_hex_color("#FF5733")` → `True` |
| `validate_uuid(uuid_str)` | 验证 UUID | `validate_uuid("550e8400-e29b-41d4-a716-446655440000")` → `True` |
| `validate_username(username)` | 验证用户名 | `validate_username("john_doe")` → `True` |
| `validate_ipv4(ip)` | 验证 IPv4 | `validate_ipv4("192.168.1.1")` → `True` |
| `validate_ipv6(ip)` | 验证 IPv6 | `validate_ipv6("2001:0db8:85a3::8a2e:0370:7334")` → `True` |
| `validate_domain(domain)` | 验证域名 | `validate_domain("example.com")` → `True` |
| `validate_base64(data)` | 验证 Base64 | `validate_base64("SGVsbG8=")` → `True` |
| `validate_chinese(text)` | 验证纯中文 | `validate_chinese("你好")` → `True` |
| `validate_alphanumeric(text, include_chinese)` | 验证字母数字 | `validate_alphanumeric("abc123")` → `True` |

### 提取函数

| 函数 | 描述 | 返回 |
|------|------|------|
| `extract_emails(text)` | 提取邮箱 | `['test@example.com', ...]` |
| `extract_urls(text)` | 提取 URL | `['https://example.com', ...]` |
| `extract_phones(text, region)` | 提取电话 | `['13800138000', ...]` |
| `extract_dates(text, format_type)` | 提取日期 | `['2024-01-15', ...]` |
| `extract_hashtags(text)` | 提取话题标签 | `['好心情', '周末', ...]` |
| `extract_mentions(text)` | 提取@提及 | `['张三', '李四', ...]` |
| `extract_markdown_links(text)` | 提取 Markdown 链接 | `[('文本', 'URL'), ...]` |
| `extract_html_tags(text)` | 提取 HTML 标签 | `[{'tag_name': 'div', ...}, ...]` |
| `extract_numbers(text, as_float)` | 提取数字 | `[25, 60, 199.99]` |
| `extract_between(text, start, end)` | 提取标记间内容 | `['content1', 'content2']` |

### 替换函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `remove_html_tags(html, keep_content)` | 移除 HTML 标签 | `remove_html_tags("<p>Hello</p>")` → `"Hello"` |
| `remove_mentions(text)` | 移除@提及 | `remove_mentions("@user hello")` → `" hello"` |
| `remove_hashtags(text)` | 移除话题标签 | `remove_hashtags("#topic hello")` → `" hello"` |
| `remove_extra_whitespace(text)` | 移除多余空白 | `remove_extra_whitespace("a  b")` → `"a b"` |
| `normalize_whitespace(text)` | 标准化空白 | `normalize_whitespace("a\n\nb")` → `"a b"` |
| `replace_urls(text, replacement)` | 替换 URL | `replace_urls(text, "[LINK]")` |
| `replace_emails(text, replacement)` | 替换邮箱 | `replace_emails(text, "[EMAIL]")` |
| `replace_phones(text, replacement, region)` | 替换电话 | `replace_phones(text, "[PHONE]")` |
| `censor_text(text, pattern, replacement)` | 按模式屏蔽 | `censor_text(text, r'\d+', '*')` |
| `censor_phone(phone)` | 屏蔽电话 | `censor_phone("13800138000")` → `"138****8000"` |
| `censor_id_card(id_card)` | 屏蔽身份证 | `censor_id_card("110101199001011234")` → `"110101********1234"` |

### 匹配和搜索

| 函数 | 描述 | 示例 |
|------|------|------|
| `find_all_matches(text, pattern)` | 查找所有匹配 | `find_all_matches(text, r'\d+')` |
| `find_first_match(text, pattern)` | 查找第一个匹配 | `find_first_match(text, r'\d+')` |
| `contains_pattern(text, pattern)` | 检查是否包含 | `contains_pattern(text, r'\d+')` → `True` |
| `match_groups(text, pattern)` | 获取分组 | `match_groups(text, r'(\w+)@(\w+)')` |
| `match_named_groups(text, pattern)` | 获取命名分组 | `match_named_groups(text, r'(?P<name>\w+)')` |
| `split_by_pattern(text, pattern)` | 按模式分割 | `split_by_pattern("a,b;c", r'[,;]')` |

### 工具函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `escape_pattern(text)` | 转义正则特殊字符 | `escape_pattern("$100")` → `"\$100"` |
| `compile_pattern(pattern, flags)` | 编译正则 | `compile_pattern(r'\d+', re.IGNORECASE)` |
| `get_pattern_names()` | 获取所有模式名 | `['email', 'url', 'phone_cn', ...]` |
| `get_pattern(pattern_name)` | 获取模式字符串 | `get_pattern('email')` |
| `test_pattern(pattern, test_strings)` | 测试模式 | `test_pattern(r'\d+', ['123', 'abc'])` |
| `pattern_info(pattern_name)` | 获取模式信息 | `pattern_info('email')` |

### 类

#### RegexMatcher

正则表达式匹配器，提供面向对象的使用方式：

```python
matcher = RegexMatcher(r'\d+')
text = "There are 123 apples"

matcher.findall(text)    # ['123']
matcher.search(text)     # Match object
matcher.sub(text, 'NUM') # "There are NUM apples"
```

#### TextCleaner

文本清洗器，支持链式调用：

```python
cleaner = TextCleaner()
result = (cleaner
          .load(text)
          .remove_html()
          .remove_mentions()
          .replace_urls('[LINK]')
          .normalize_whitespace()
          .get())
```

### 批量处理

| 函数 | 描述 | 示例 |
|------|------|------|
| `batch_validate(items, validator_func)` | 批量验证 | `batch_validate(emails, validate_email)` |
| `batch_extract(texts, extractor_func)` | 批量提取 | `batch_extract(texts, extract_urls)` |
| `filter_by_pattern(items, pattern, keep_matching)` | 按模式过滤 | `filter_by_pattern(list, r'a')` |
| `group_by_pattern(items, pattern)` | 按模式分组 | `group_by_pattern(list, r'^[a-c]')` |

---

## 💡 使用示例

### 示例 1: 用户输入验证

```python
from mod import (
    validate_email, validate_phone, validate_password,
    validate_username, validate_id_card
)

def register_user(email, phone, username, password, id_card=None):
    """验证用户注册信息"""
    errors = []
    
    if not validate_email(email):
        errors.append("邮箱格式不正确")
    
    if not validate_phone(phone, 'cn'):
        errors.append("手机号格式不正确")
    
    if not validate_username(username):
        errors.append("用户名格式不正确（字母开头，3-20 位）")
    
    if not validate_password(password, 'strong'):
        errors.append("密码强度不足（需包含大小写字母、数字、特殊字符）")
    
    if id_card and not validate_id_card(id_card):
        errors.append("身份证号码格式不正确")
    
    if errors:
        return {'success': False, 'errors': errors}
    
    return {'success': True, 'message': '验证通过'}

# 使用
result = register_user(
    email='user@example.com',
    phone='13800138000',
    username='john_doe',
    password='Secure@123',
    id_card='110101199001011234'
)
print(result)
```

### 示例 2: 文本内容提取

```python
from mod import (
    extract_emails, extract_urls, extract_hashtags,
    extract_mentions, extract_numbers
)

def analyze_social_post(text):
    """分析社交媒体帖子"""
    return {
        'emails': extract_emails(text),
        'urls': extract_urls(text),
        'hashtags': extract_hashtags(text),
        'mentions': extract_mentions(text),
        'numbers': extract_numbers(text),
        'has_links': len(extract_urls(text)) > 0,
        'has_contacts': len(extract_emails(text) + extract_mentions(text)) > 0,
    }

# 使用
post = """
大家好！@张三 @李四 
今天分享一个好物：https://example.com/product
有问题联系 support@example.com
价格只要 199.99 元！#好物推荐 #省钱攻略
"""

analysis = analyze_social_post(post)
print(analysis)
```

### 示例 3: 敏感信息脱敏

```python
from mod import (
    censor_phone, censor_id_card,
    replace_emails, replace_urls,
    TextCleaner
)

def sanitize_document(text):
    """脱敏文档中的敏感信息"""
    cleaner = TextCleaner()
    return (cleaner
            .load(text)
            .replace_emails('[EMAIL]')
            .replace_urls('[LINK]')
            .censor_phones()
            .get())

# 手动脱敏
def censor_contact_info(text):
    """脱敏联系方式"""
    # 先提取再脱敏
    phones = extract_phones(text)
    for phone in phones:
        text = text.replace(phone, censor_phone(phone))
    
    id_cards = []  # 需要自定义提取逻辑
    for id_card in id_cards:
        text = text.replace(id_card, censor_id_card(id_card))
    
    return text

# 使用
document = """
联系人：张三
电话：13800138000
邮箱：zhangsan@example.com
身份证：110101199001011234
网站：https://example.com
"""

sanitized = sanitize_document(document)
print(sanitized)
```

### 示例 4: 日志分析

```python
from mod import (
    find_all_matches, extract_numbers,
    contains_pattern, split_by_pattern
)

def analyze_log(log_text):
    """分析日志文件"""
    analysis = {
        # 提取 IP 地址
        'ip_addresses': find_all_matches(log_text, r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
        
        # 提取时间戳
        'timestamps': find_all_matches(log_text, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'),
        
        # 提取错误码
        'error_codes': find_all_matches(log_text, r'ERROR_\d+'),
        
        # 检查是否包含敏感词
        'has_errors': contains_pattern(log_text, r'ERROR|FATAL|CRITICAL'),
        'has_warnings': contains_pattern(log_text, r'WARN|WARNING'),
        
        # 提取响应时间
        'response_times': extract_numbers(log_text, as_float=True),
    }
    
    # 计算平均响应时间
    if analysis['response_times']:
        analysis['avg_response_time'] = sum(analysis['response_times']) / len(analysis['response_times'])
    
    return analysis

# 使用
log = """
2024-01-15 10:30:00 INFO Request from 192.168.1.100
2024-01-15 10:30:01 ERROR ERROR_500 Internal server error
2024-01-15 10:30:02 INFO Response time: 125.5ms
2024-01-15 10:30:03 WARNING WARNING_001 High memory usage
"""

result = analyze_log(log)
print(result)
```

### 示例 5: 数据清洗流水线

```python
from mod import (
    TextCleaner, validate_email, validate_phone,
    filter_by_pattern, batch_validate
)

def clean_customer_data(customers):
    """清洗客户数据"""
    cleaned = []
    
    for customer in customers:
        # 使用 TextCleaner 清洗文本字段
        cleaner = TextCleaner()
        name = (cleaner
                .load(customer.get('name', ''))
                .normalize_whitespace()
                .get())
        
        notes = (cleaner
                 .load(customer.get('notes', ''))
                 .remove_html_tags()
                 .replace_urls('')
                 .get())
        
        # 验证联系方式
        email_valid = validate_email(customer.get('email', ''))
        phone_valid = validate_phone(customer.get('phone', ''), 'cn')
        
        cleaned.append({
            'name': name,
            'email': customer.get('email') if email_valid else None,
            'phone': customer.get('phone') if phone_valid else None,
            'notes': notes,
            'valid_email': email_valid,
            'valid_phone': phone_valid,
        })
    
    return cleaned

# 批量验证示例
emails = ['test@example.com', 'invalid', 'user@domain.org']
validation_results = batch_validate(emails, validate_email)
print(validation_results)
# {'test@example.com': True, 'invalid': False, 'user@domain.org': True}

# 过滤示例
names = ['Alice', 'Bob', 'Charlie', 'David']
names_starting_with_a = filter_by_pattern(names, r'^[Aa]', keep_matching=True)
print(names_starting_with_a)  # ['Alice']
```

### 示例 6: Markdown 内容处理

```python
from mod import (
    extract_markdown_links, extract_hashtags,
    remove_html_tags, contains_pattern
)

def process_markdown_content(md_text):
    """处理 Markdown 内容"""
    return {
        # 提取所有链接
        'links': extract_markdown_links(md_text),
        
        # 提取话题标签
        'tags': extract_hashtags(md_text),
        
        # 检查是否包含代码块
        'has_code': contains_pattern(md_text, r'```'),
        
        # 检查是否包含图片
        'has_images': contains_pattern(md_text, r'!\[.*?\]\(.*?\)'),
        
        # 检查是否包含表格
        'has_tables': contains_pattern(md_text, r'\|.*?\|'),
    }

# 使用
content = """
# 我的文章

访问 [Google](https://google.com) 和 [GitHub](https://github.com)

![图片](image.png)

#技术 #编程 #Python
"""

result = process_markdown_content(content)
print(result)
```

### 示例 7: 自定义模式匹配

```python
from mod import (
    RegexMatcher, get_pattern, pattern_info,
    compile_pattern, escape_pattern
)

# 使用预定义模式
email_pattern = get_pattern('email')
print(f"邮箱模式：{email_pattern}")

# 获取模式信息
info = pattern_info('phone_cn')
print(f"中国手机号模式：{info}")

# 创建自定义匹配器
matcher = RegexMatcher(r'\d{4}-\d{2}-\d{2}')  # 日期模式
dates = matcher.findall("今天是 2024-01-15，明天是 2024-01-16")
print(f"提取的日期：{dates}")

# 转义用户输入
user_input = "$100 (50% off)"
safe_pattern = escape_pattern(user_input)
print(f"转义后：{safe_pattern}")

# 编译带标志的正则
case_insensitive = compile_pattern(r'hello', flags=2)  # re.IGNORECASE
result = case_insensitive.search("HELLO world")
print(f"匹配结果：{result.group() if result else None}")
```

---

## 📋 预定义模式列表

### 基础类型
- `email` - 邮箱地址
- `url` - HTTP/HTTPS URL
- `ip_v4` - IPv4 地址
- `ip_v6` - IPv6 地址
- `domain` - 域名
- `hostname` - 主机名

### 电话号码
- `phone_cn` - 中国大陆手机号
- `phone_us` - 美国电话号码
- `phone_intl` - 国际电话号码

### 日期时间
- `date_iso` - ISO 日期格式 (YYYY-MM-DD)
- `date_cn` - 中文日期格式 (YYYY 年 M 月 D 日)
- `datetime_iso` - ISO 日期时间
- `time_24h` - 24 小时制时间
- `time_12h` - 12 小时制时间

### 身份标识
- `id_card_cn` - 中国身份证号码
- `passport` - 护照号码
- `license_plate_cn` - 中国大陆车牌

### 编码和哈希
- `hex_color` - 十六进制颜色
- `base64` - Base64 编码
- `uuid` - UUID
- `md5` - MD5 哈希
- `sha1` - SHA1 哈希
- `sha256` - SHA256 哈希

### 文件路径
- `file_path_unix` - Unix 文件路径
- `file_path_win` - Windows 文件路径
- `file_extension` - 文件扩展名

### 用户名和密码
- `username` - 用户名
- `password_strong` - 强密码
- `password_medium` - 中等强度密码

### 数字和货币
- `integer` - 整数
- `positive_integer` - 正整数
- `decimal` - 小数
- `currency` - 货币金额
- `percentage` - 百分比

### 特殊用途
- `html_tag` - HTML 标签
- `markdown_link` - Markdown 链接
- `mention` - @提及
- `hashtag` - 话题标签
- `emoji` - Emoji 表情

### 空白和字符
- `whitespace` - 纯空白
- `alphanumeric` - 字母数字
- `alphanumeric_cn` - 字母数字中文
- `chinese` - 纯中文
- `ascii` - 纯 ASCII

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/regex_utils
python regex_utils_test.py
```

### 测试覆盖

- ✅ 邮箱验证和提取
- ✅ URL 验证和提取
- ✅ 电话号码验证
- ✅ 日期格式验证
- ✅ 身份证验证和脱敏
- ✅ 密码强度验证
- ✅ 颜色代码验证
- ✅ UUID 验证
- ✅ 话题标签和@提及提取
- ✅ 数字提取
- ✅ HTML 标签移除
- ✅ 空白标准化
- ✅ 文本脱敏
- ✅ 正则匹配和搜索
- ✅ 模式转义
- ✅ RegexMatcher 类
- ✅ TextCleaner 类
- ✅ 批量处理函数
- ✅ IPv4/域名/中文验证

---

## 🔧 扩展和自定义

### 添加自定义模式

```python
from mod import PATTERNS, validate_email

# 添加自定义模式
PATTERNS['custom_pattern'] = r'your-regex-here'

# 现在可以使用
def validate_custom(text):
    import re
    return bool(re.match(PATTERNS['custom_pattern'], text))
```

### 创建自定义验证器

```python
from mod import RegexMatcher

# 创建特定领域的匹配器
class PhoneNumberExtractor:
    def __init__(self):
        self.matcher = RegexMatcher(r'1[3-9]\d{9}')
    
    def extract(self, text):
        return self.matcher.findall(text)
    
    def censor(self, text):
        return self.matcher.sub(text, lambda m: m.group()[:3] + '****' + m.group()[-4:])

# 使用
extractor = PhoneNumberExtractor()
phones = extractor.extract("联系 13800138000 或 19912345678")
print(phones)  # ['13800138000', '19912345678']
```

---

## ⚠️ 注意事项

1. **性能**: 对于大量文本处理，建议预编译正则表达式
2. **Unicode**: 中文匹配使用 Unicode 范围 `\u4e00-\u9fa5`
3. **边界情况**: 身份证校验包含校验码验证逻辑
4. **隐私**: 脱敏函数用于日志和展示，不要用于安全敏感场景

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

---

## 📝 更新日志

### v1.0.0 (2026-04-09)
- ✨ 初始版本
- 📋 35+ 预定义正则模式
- ✅ 15+ 验证函数
- 🔍 10+ 提取函数
- 🔄 12+ 替换和脱敏函数
- 🎯 6+ 匹配搜索函数
- 🧹 TextCleaner 链式清洗
- 📦 4 个批量处理函数
- 🧪 完整测试套件
