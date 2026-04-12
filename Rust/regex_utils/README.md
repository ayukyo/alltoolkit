# AllToolkit - Rust Regex Utils 🔍

**零依赖正则表达式工具库 - 生产就绪**

---

## 📖 概述

`regex_utils` 提供功能完整的正则表达式匹配、验证、提取和替换功能。包含常用验证模式（邮箱、电话、URL、日期等）、数据提取、文本替换和实用工具函数。基于 Rust 标准 `regex` crate，性能优异，适合生产环境使用。

---

## ✨ 特性

- **常用验证模式** - 邮箱、IPv4/IPv6、URL、电话、日期、UUID 等
- **中国特定格式** - 中国手机号、身份证号、邮编
- **数据提取** - 提取所有匹配、数字、邮箱、URL、捕获组
- **文本替换** - 全部替换、首次替换、删除、HTML 标签清理
- **实用工具** - 匹配计数、分割、转义、模式验证
- **Unicode 支持** - 正确处理多语言文本
- **零额外依赖** - 仅依赖标准 `regex` crate
- **全面测试** - 包含单元测试和集成测试

---

## 🚀 快速开始

### 基础使用

```rust
use regex_utils::{is_email, extract_numbers, replace_all};

// 验证邮箱
assert!(is_email("user@example.com"));
assert!(!is_email("invalid"));

// 提取数字
let numbers = extract_numbers("Price: $100, discount: $20");
assert_eq!(numbers, vec!["100", "20"]);

// 替换文本
let result = replace_all(r"\d+", "abc123def456", "NUM");
assert_eq!(result, "abcNUMdefNUM");
```

### 常用验证

```rust
use regex_utils::{
    is_email, is_ipv4, is_url, is_phone,
    is_date, is_time, is_uuid, is_hex_color,
    is_china_phone, is_china_id, is_china_postcode,
};

// 邮箱验证
assert!(is_email("user@example.com"));

// IP 地址验证
assert!(is_ipv4("192.168.1.1"));

// URL 验证
assert!(is_url("https://example.com"));

// 手机号验证（国际格式）
assert!(is_phone("+1234567890"));

// 中国手机号验证
assert!(is_china_phone("13812345678"));

// 日期时间验证
assert!(is_date("2024-06-15"));
assert!(is_time("14:30:00"));

// UUID 验证
assert!(is_uuid("550e8400-e29b-41d4-a716-446655440000"));

// 十六进制颜色验证
assert!(is_hex_color("#FF5733"));
```

### 数据提取

```rust
use regex_utils::{
    extract_all, extract_numbers, extract_emails,
    extract_urls, extract_first_capture,
    extract_captures, extract_named_captures,
};

// 提取所有匹配
let matches = extract_all(r"\d+", "abc123def456");
assert_eq!(matches, vec!["123", "456"]);

// 提取数字
let numbers = extract_numbers("Price: $100, discount: $20.50");
assert_eq!(numbers, vec!["100", "20", "50"]);

// 提取邮箱
let emails = extract_emails("Contact: user@example.com or admin@test.org");
assert_eq!(emails, vec!["user@example.com", "admin@test.org"]);

// 提取 URL
let urls = extract_urls("Visit https://example.com or http://test.org");
assert_eq!(urls, vec!["https://example.com", "http://test.org"]);

// 提取第一个捕获组
let name = extract_first_capture(r"name=(\w+)", "user=name=John&age=30");
assert_eq!(name, Some("John".to_string()));

// 提取所有捕获组
let matches = extract_captures(r"(\w+)=(\d+)", "a=1 b=2");
assert_eq!(matches, vec![vec!["a", "1"], vec!["b", "2"]]);

// 提取命名捕获组
use std::collections::HashMap;
let data: HashMap<String, String> = extract_named_captures(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",
    "2024-06-15"
);
assert_eq!(data.get("year"), Some(&"2024".to_string()));
```

### 文本替换

```rust
use regex_utils::{
    replace_all, replace_first, remove_all,
    strip_html, normalize_whitespace, sanitize_filename,
};

// 全部替换（支持捕获组）
let result = replace_all(r"(\w+) (\w+)", "John Doe", "$2, $1");
assert_eq!(result, "Doe, John");

// 仅替换第一个匹配
let result = replace_first(r"\d+", "abc123def456", "NUM");
assert_eq!(result, "abcNUMdef456");

// 删除所有匹配
let result = remove_all(r"\s+", "hello   world");
assert_eq!(result, "helloworld");

// 清理 HTML 标签
let result = strip_html("<p>Hello <b>World</b></p>");
assert_eq!(result, "Hello World");

// 规范化空白字符
let result = normalize_whitespace("  hello   world  \n\t test  ");
assert_eq!(result, "hello world test");

// 清理文件名
let result = sanitize_filename("my file: name?.txt");
assert_eq!(result, "my_file_name.txt");
```

### 实用工具

```rust
use regex_utils::{
    count_matches, contains_pattern, split_by,
    escape_regex, is_valid_regex, matches_pattern,
};

// 计算匹配数
let count = count_matches(r"\d+", "abc123def456ghi789");
assert_eq!(count, 3);

// 检查是否包含匹配
assert!(contains_pattern(r"\d+", "abc123"));
assert!(!contains_pattern(r"\d+", "abcdef"));

// 按模式分割
let parts = split_by(r"\s+", "hello world  test");
assert_eq!(parts, vec!["hello", "world", "test"]);

// 转义正则特殊字符
let escaped = escape_regex("price: $100 (50% off)");
assert_eq!(escaped, r"price: \$100 \(50% off\)");

// 验证正则表达式是否有效
assert!(is_valid_regex(r"\d+"));
assert!(!is_valid_regex(r"[\d+"));

// 使用自定义模式匹配
assert!(matches_pattern(r"^\d{3}-\d{4}$", "123-4567"));
```

---

## 📋 内置验证模式

### 通用格式

| 函数 | 说明 | 示例 |
|------|------|------|
| `is_email()` | 邮箱地址 | `user@example.com` |
| `is_ipv4()` | IPv4 地址 | `192.168.1.1` |
| `is_ipv6()` | IPv6 地址 | `2001:0db8:85a3:...` |
| `is_url()` | HTTP/HTTPS URL | `https://example.com` |
| `is_phone()` | 国际手机号 | `+1234567890` |
| `is_date()` | 日期 (YYYY-MM-DD) | `2024-06-15` |
| `is_time()` | 时间 (HH:MM:SS) | `14:30:00` |
| `is_uuid()` | UUID | `550e8400-e29b-...` |
| `is_hex_color()` | 十六进制颜色 | `#FF5733`, `#FFF` |
| `is_username()` | 用户名 (3-20 字符) | `john_doe` |
| `is_strong_password()` | 强密码 | `SecureP@ss1` |

### 中国特定格式

| 函数 | 说明 | 示例 |
|------|------|------|
| `is_china_phone()` | 中国手机号 | `13812345678` |
| `is_china_id()` | 中国身份证号 | `11010519491231002X` |
| `is_china_postcode()` | 中国邮编 | `100000` |
| `is_china_license()` | 中国车牌 | `京 A12345` |

---

## 🔧 高级用法

### 使用模式常量

```rust
use regex_utils::patterns;
use regex::Regex;

// 直接使用预定义模式
let re = Regex::new(patterns::EMAIL).unwrap();
assert!(re.is_match("user@example.com"));
```

### 组合使用

```rust
use regex_utils::{is_email, extract_emails, sanitize_filename};

// 验证并提取文本中的邮箱
fn validate_and_extract_emails(text: &str) -> Vec<String> {
    extract_emails(text)
        .into_iter()
        .filter(|email| is_email(email))
        .collect()
}

// 清理用户输入
fn clean_user_input(input: &str) -> String {
    let sanitized = sanitize_filename(input);
    if sanitized.is_empty() {
        "unnamed".to_string()
    } else {
        sanitized
    }
}
```

---

## 🧪 运行测试

```bash
# 进入目录
cd /home/admin/.openclaw/workspace/AllToolkit/Rust/regex_utils

# 运行所有测试
cargo test

# 运行库测试
cargo test --lib

# 运行示例
cargo run --example basic
cargo run --example advanced

# 运行特定测试
cargo test test_is_email
```

---

## 📦 依赖

仅需 Rust 标准 `regex` crate。在 `Cargo.toml` 中添加：

```toml
[dependencies]
regex = "1"
```

---

## 🎯 最佳实践

### ✅ 推荐用法

```rust
// 1. 使用内置验证函数（已优化）
if is_email(input) {
    // 处理有效邮箱
}

// 2. 提取前检查是否有匹配
let emails = extract_emails(text);
if !emails.is_empty() {
    // 处理提取的邮箱
}

// 3. 使用命名捕获组提高可读性
let data = extract_named_captures(
    r"(?P<area>\d{3})-(?P<prefix>\d{3})-(?P<line>\d{4})",
    phone
);

// 4. 处理可能的无效模式
if is_valid_regex(user_pattern) {
    let matches = extract_all(&user_pattern, text);
    // 处理匹配
}
```

---

## 🔒 安全考虑

1. **正则表达式拒绝服务 (ReDoS)**: 避免使用可能导致指数级回溯的模式
2. **用户输入**: 验证用户提供的正则表达式长度和有效性
3. **隐私数据**: 提取敏感信息（邮箱、电话）时注意数据安全

---

## 📝 版本历史

### 1.0.0 (2026-04-10)

- ✨ 初始版本
- ✅ 15+ 验证函数
- ✅ 10+ 提取函数
- ✅ 6+ 替换函数
- ✅ 6+ 实用工具函数
- ✅ 单元测试和集成测试
- ✅ 完整文档和示例

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 📚 相关资源

- [Rust regex crate 文档](https://docs.rs/regex)
- [Regex101 在线测试](https://regex101.com/)
- [正则表达式入门指南](https://www.runoob.com/regexp/regexp-tutorial.html)

---

**AllToolkit** - 让开发更简单 🚀
