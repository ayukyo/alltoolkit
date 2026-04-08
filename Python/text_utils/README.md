# Text Utils - Python 文本处理工具模块

AllToolkit 的 Python 文本处理工具模块，提供全面的字符串和文本处理功能。

## 📦 功能特性

### 文本清理
- `clean_whitespace()` - 清理和规范化空白字符
- `clean_text()` - 多选项文本清理（标点、数字、大小写）
- `remove_html_tags()` - 移除 HTML 标签
- `remove_urls()` - 移除 URL
- `remove_emojis()` - 移除表情符号

### 文本格式化
- `truncate()` - 截断文本（带后缀）
- `pad_left()` / `pad_right()` / `pad_center()` - 文本填充
- `wrap_text()` - 文本换行
- `indent_text()` - 文本缩进

### 大小写转换
- `to_camel_case()` - 转为 camelCase
- `to_pascal_case()` - 转为 PascalCase
- `to_snake_case()` - 转为 snake_case
- `to_kebab_case()` - 转为 kebab-case
- `to_title_case()` - 转为 Title Case

### 搜索和替换
- `replace_all()` - 多模式替换
- `replace_regex()` - 正则表达式替换
- `find_all()` - 查找所有匹配
- `find_first()` - 查找第一个匹配

### 文本分析
- `count_words()` - 词数统计
- `count_chars()` - 字符数统计
- `count_lines()` - 行数统计
- `word_frequency()` - 词频统计
- `char_frequency()` - 字符频率统计
- `readability_score()` - 可读性评分

### 编码和转义
- `escape_html()` - HTML 转义（防 XSS）
- `unescape_html()` - HTML 反转义
- `escape_regex()` - 正则表达式转义
- `hash_text()` - 文本哈希（MD5/SHA1/SHA256/SHA512）

### 字符串比较
- `levenshtein_distance()` - 编辑距离计算
- `similarity_ratio()` - 相似度比率
- `is_palindrome()` - 回文检查

### 工具函数
- `is_empty()` / `is_not_empty()` - 空值检查
- `reverse_string()` - 字符串反转
- `repeat_string()` - 字符串重复
- `generate_random_string()` - 生成随机字符串
- `extract_numbers()` - 提取数字
- `extract_emails()` - 提取邮箱
- `mask_text()` - 文本掩码（敏感数据）

## 🚀 快速开始

### 安装

无需安装，直接使用：

```python
import sys
sys.path.insert(0, '/path/to/AllToolkit/Python/text_utils')
from mod import clean_text, truncate, to_camel_case
```

### 基本用法

```python
from mod import *

# 文本清理
text = "  Hello, World! 123  "
cleaned = clean_text(text, remove_punctuation=True, remove_digits=True)
print(cleaned)  # "Hello World"

# 截断
long_text = "This is a very long text"
truncated = truncate(long_text, 15)
print(truncated)  # "This is a very..."

# 大小写转换
print(to_camel_case("hello_world"))      # "helloWorld"
print(to_snake_case("helloWorld"))       # "hello_world"
print(to_kebab_case("helloWorld"))       # "hello-world"

# 文本分析
text = "Python is great. Python is powerful."
print(count_words(text))          # 7
print(word_frequency(text))       # {'python': 2, 'is': 2, ...}

# 安全相关
user_input = "<script>alert('XSS')</script>"
safe = escape_html(user_input)
print(safe)  # "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"

# 数据提取
text = "Contact: support@example.com, sales@test.org"
emails = extract_emails(text)
print(emails)  # ['support@example.com', 'sales@test.org']
```

## 📁 文件结构

```
text_utils/
├── mod.py                  # 主模块（所有工具函数）
├── text_utils_test.py      # 测试套件（116 个测试）
├── README.md               # 本文档
└── examples/
    └── usage_examples.py   # 使用示例
```

## ✅ 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/text_utils
python3 text_utils_test.py
```

预期输出：
```
Tests: 116 | Passed: 116 | Failed: 0
All tests passed!
```

## 📖 示例

运行使用示例：

```bash
cd /path/to/AllToolkit/Python/text_utils/examples
python3 usage_examples.py
```

## 💡 实际应用场景

### 1. 用户内容清理

```python
def process_user_content(html_content):
    """处理用户生成的内容"""
    # 移除 HTML 标签
    text = remove_html_tags(html_content)
    # 移除 URL
    text = remove_urls(text)
    # 移除表情符号
    text = remove_emojis(text)
    # 清理空白
    text = clean_whitespace(text)
    return text
```

### 2. API 字段转换

```python
def convert_api_fields(api_response):
    """将 API 的 snake_case 字段转为 Python 的 camelCase"""
    return {to_camel_case(k): v for k, v in api_response.items()}
```

### 3. 密码强度检查

```python
def check_password_strength(password):
    """检查密码强度"""
    score = sum([
        len(password) >= 8,
        len(password) >= 12,
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c.isdigit() for c in password),
        any(c in "!@#$%^&*()" for c in password)
    ])
    return "Weak" if score < 3 else "Medium" if score < 5 else "Strong"
```

### 4. 敏感数据掩码

```python
def mask_sensitive_data(data, data_type):
    """掩码敏感数据"""
    if data_type == 'credit_card':
        return mask_text(data, visible_end=4)
    elif data_type == 'email':
        return mask_text(data, visible_start=2, visible_end=10)
    elif data_type == 'phone':
        return mask_text(data, visible_end=4)
    return data
```

## 🔒 安全特性

- **HTML 转义** - 防止 XSS 攻击
- **密码哈希** - 支持多种哈希算法
- **数据掩码** - 保护敏感信息
- **输入验证** - 所有函数处理 None 安全

## 📊 性能特点

- **零依赖** - 仅使用 Python 标准库
- **高效实现** - 使用内置函数和正则表达式
- **内存友好** - 流式处理大文本

## 📝 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请在 AllToolkit 仓库提交 Issue。
