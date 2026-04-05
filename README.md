# AllToolkit - Universal Toolkit Library

[![CI](https://github.com/ayukyo/alltoolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ayukyo/alltoolkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Languages](https://img.shields.io/badge/languages-20+-blue)](https://github.com/ayukyo/alltoolkit)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

**一个工具库，20+ 种语言通用** - 为零依赖、生产级、文档完善的日常开发任务提供统一解决方案。

🚀 **快速开始：** 选择你的语言 → 复制代码 → 直接使用（无需安装依赖）

## ✨ 特性

- **零依赖** - 仅使用各语言标准库
- **生产就绪** - 经过测试、性能优化、异常安全
- **文档完善** - 完整注释、参数说明、使用示例
- **20+ 语言** - 覆盖主流编程语言
- **持续更新** - 每小时新增工具函数

## Supported Languages

- Python
- C
- Java
- C++
- C#
- JavaScript
- VB
- SQL
- R
- Delphi
- TypeScript
- **Go** ✨
- **Rust** ✨
- PHP
- Swift
- Kotlin
- ArkTS
- Fortran
- MATLAB
- Perl
- **Ruby** ✨

## 📦 安装（即将推出）

```bash
# Python
pip install alltoolkit

# JavaScript
npm install alltoolkit

# Rust
cargo add alltoolkit

# Go
go get github.com/ayukyo/alltoolkit/Go/string_utils
```

> 💡 目前可以直接复制代码使用，包管理器发布计划中...

## 📁 目录结构

### Directory Layout

```
AllToolkit/
├── {Language}/
│   ├── {module_name}/          # 功能模块目录
│   │   ├── mod.{ext}           # 模块主文件
│   │   ├── {module}_test.{ext} # 测试文件（如有）
│   │   └── README.md           # 模块文档（可选）
│   ├── examples/               # 示例代码目录
│   │   └── {module}_example.{ext}
│   └── README.md               # 语言目录说明
```

### 示例

**Go:**
```
Go/
├── string_utils/
│   ├── string_utils.go
│   └── string_utils_test.go
├── path_utils/
│   ├── path_utils.go
│   └── path_utils_test.go
└── examples/
    ├── string_utils_example.go
    └── path_utils_example.go
```

**Python:**
```
Python/
├── file_utils.py
└── examples/
    └── file_utils_example.py
```

Each language directory contains standalone, dependency-free utility modules with:
- ✅ Complete documentation
- ✅ Parameter descriptions
- ✅ Return value documentation
- ✅ Runnable examples
- ✅ Unit tests (where applicable)

## Philosophy

- **Zero dependencies**: Each function is self-contained
- **Production-ready**: Clean, tested, performant code
- **Well-documented**: Clear comments and usage examples
- **Unicode-safe**: Proper handling of international text

## Latest Addition

### Go - XML Utilities

Location: `Go/xml_utils/mod.go`

Functions:

**Parsing:**
- **ParseString**: `ParseString(xmlString)` - Parse XML from string
- **ParseFile**: `ParseFile(filename)` - Parse XML from file
- **ParseReader**: `ParseReader(reader)` - Parse XML from io.Reader

**Document Creation:**
- **NewDocument**: `NewDocument(rootName)` - Create new XML document
- **SetVersion**: `SetVersion(version)` - Set XML version declaration
- **SetEncoding**: `SetEncoding(encoding)` - Set XML encoding declaration

**Navigation:**
- **Find**: `Find(path)` - Find first element by path (e.g., "root/item/subitem")
- **FindAll**: `FindAll(tagName)` - Find all elements with given tag name
- **FindByAttr**: `FindByAttr(tagName, attrName, attrValue)` - Find element by attribute value
- **Root**: `Root()` - Get root element

**Node Operations:**
- **GetTagName**: `GetTagName()` - Get element tag name
- **SetTagName**: `SetTagName(name)` - Set element tag name
- **Text**: `Text()` - Get text content
- **SetText**: `SetText(text)` - Set text content
- **GetAttr**: `GetAttr(name)` - Get attribute value
- **SetAttr**: `SetAttr(name, value)` - Set attribute value
- **HasAttr**: `HasAttr(name)` - Check if attribute exists
- **RemoveAttr**: `RemoveAttr(name)` - Remove attribute
- **Attrs**: `Attrs()` - Get all attributes as map
- **CreateElement**: `CreateElement(tagName)` - Create child element
- **AddChild**: `AddChild(child)` - Add child node
- **RemoveChild**: `RemoveChild(child)` - Remove child node
- **GetChildren**: `GetChildren()` - Get all child nodes
- **ChildCount**: `ChildCount()` - Get number of children
- **GetParent**: `GetParent()` - Get parent node

**Typed Attribute Access:**
- **GetIntAttr**: `GetIntAttr(name, defaultValue)` - Get attribute as int
- **GetFloatAttr**: `GetFloatAttr(name, defaultValue)` - Get attribute as float64
- **GetBoolAttr**: `GetBoolAttr(name, defaultValue)` - Get attribute as bool

**Serialization:**
- **ToXML**: `ToXML()` - Convert to compact XML string
- **ToPrettyXML**: `ToPrettyXML(indent...)` - Convert to pretty-printed XML
- **SaveToFile**: `SaveToFile(filename, pretty)` - Save to file

**Utility:**
- **IsValidXML**: `IsValidXML(xmlString)` - Check if string is valid XML
- **StripXML**: `StripXML(xmlString)` - Remove XML tags, return plain text
- **ToMap**: `ToMap()` - Convert to nested map structure
- **GetTextByTag**: `GetTextByTag(tagName)` - Get text of first element by tag
- **GetAttrByTag**: `GetAttrByTag(tagName, attrName)` - Get attribute of first element by tag

**Features:**
- Zero dependencies, uses only Go standard library (encoding/xml)
- Full XML parsing with encoding/xml support
- XPath-like navigation with slash-separated paths
- Create and modify XML documents programmatically
- Pretty print and compact output formats
- Type-safe attribute access with defaults
- XML validation and text extraction
- Conversion to/from map structures
- Complete test suite with 10+ test cases
- 10 practical usage examples
- Production-ready for configuration files and data exchange

Compile and run tests:
```bash
cd Go/xml_utils
go test -v
```

Run example:
```bash
cd Go/examples
go run xml_utils_example.go
```

Usage example:
```go
import "github.com/ayukyo/alltoolkit/Go/xml_utils"

// Parse XML
doc, err := xml_utils.ParseString(`
<configuration>
    <database>
        <host>localhost</host>
        <port>5432</port>
    </database>
</configuration>
`)

// Navigate
host := doc.Find("configuration/database/host")
fmt.Println(host.Text()) // "localhost"

// Find all
items := doc.FindAll("item")
for _, item := range items {
    fmt.Println(item.Text())
}

// Find by attribute
node := doc.FindByAttr("item", "id", "2")

// Create XML
doc = xml_utils.NewDocument("root")
child := doc.Root().CreateElement("child")
child.SetAttr("id", "1")
child.SetText("Hello World")

// Output
fmt.Println(doc.ToPrettyXML())
// <?xml version="1.0" encoding="UTF-8"?>
// <root>
//   <child id="1">Hello World</child>
// </root>

// Typed attributes
count := node.GetIntAttr("count", 0)
price := node.GetFloatAttr("price", 0.0)
enabled := node.GetBoolAttr("enabled", false)

// Validation
isValid := xml_utils.IsValidXML(xmlString)

// Strip tags
plainText := xml_utils.StripXML(xmlString)
```

---

### Java - Validation Utilities

Location: `Java/validation_utils/mod.java`

Functions:

**Basic Validation:**
- **isEmpty**: `isEmpty(str)` - Check if string is null or empty
- **isBlank**: `isBlank(str)` - Check if string is null, empty, or whitespace only
- **isNotEmpty**: `isNotEmpty(str)` - Check if string is not null and not empty
- **isNotBlank**: `isNotBlank(str)` - Check if string has content (not null, not blank)

**Email Validation:**
- **isEmail**: `isEmail(email)` - Validate email format (RFC 5322 compliant)

**Phone Validation:**
- **isChinaMobile**: `isChinaMobile(phone)` - Validate China mainland mobile phone number (11 digits, starts with 1)

**IP Address Validation:**
- **isIpv4**: `isIpv4(ip)` - Validate IPv4 address (0.0.0.0 - 255.255.255.255)
- **isIpv6**: `isIpv6(ip)` - Validate IPv6 address (simplified format)

**URL Validation:**
- **isUrl**: `isUrl(url)` - Validate URL format (http/https/ftp)

**ID Card Validation:**
- **isChinaIdCard**: `isChinaIdCard(idCard)` - Validate China mainland ID card number (18 digits with check code verification)

**Credit Card Validation:**
- **isCreditCard**: `isCreditCard(cardNumber)` - Validate credit card number using Luhn algorithm

**Format Validation:**
- **isUuid**: `isUuid(uuid)` - Validate UUID format (8-4-4-4-12 pattern)
- **isHexColor**: `isHexColor(color)` - Validate hex color code (#RGB or #RRGGBB)
- **isNumeric**: `isNumeric(str)` - Check if string contains only digits (optional negative sign)
- **isAlpha**: `isAlpha(str)` - Check if string contains only letters
- **isAlphanumeric**: `isAlphanumeric(str)` - Check if string contains only letters and digits
- **isUsername**: `isUsername(username)` - Validate username (letter开头, 3-20 chars, alphanumeric + underscore)
- **isStrongPassword**: `isStrongPassword(password)` - Validate strong password (8+ chars, uppercase, lowercase, digit, special char)
- **isMacAddress**: `isMacAddress(mac)` - Validate MAC address format (00:1A:2B:3C:4D:5E or 00-1A-2B-3C-4D-5E)
- **isChinese**: `isChinese(str)` - Check if string contains only Chinese characters
- **isDate**: `isDate(date)` - Validate date format (YYYY-MM-DD)
- **isTime**: `isTime(time)` - Validate time format (HH:MM:SS)
- **isChinaZipCode**: `isChinaZipCode(zipCode)` - Validate China postal code (6 digits)

**Range Validation:**
- **lengthBetween**: `lengthBetween(str, min, max)` - Check if string length is within range
- **between**: `between(value, min, max)` - Check if numeric value is within range (int, long, double)

**Regex Validation:**
- **matches**: `matches(str, pattern)` - Check if string matches regex pattern
- **findFirst**: `findFirst(str, pattern)` - Find first regex match in string
- **findAll**: `findAll(str, pattern)` - Find all regex matches in string

**Utility Methods:**
- **isLeapYear**: `isLeapYear(year)` - Check if year is a leap year
- **equals**: `equals(str1, str2)` - Null-safe string equality check
- **equalsIgnoreCase**: `equalsIgnoreCase(str1, str2)` - Null-safe case-insensitive equality check
- **contains**: `contains(str, substr)` - Null-safe substring check
- **startsWith**: `startsWith(str, prefix)` - Null-safe prefix check
- **endsWith**: `endsWith(str, suffix)` - Null-safe suffix check

**ValidationResult Class:**
- **isValid**: Check if validation passed
- **getField**: Get validated field name
- **getMessage**: Get validation message

**Features:**
- Zero dependencies, uses only Java standard library (java.util.regex)
- Null-safe all methods (handle null inputs gracefully)
- RFC 5322 compliant email validation
- Luhn algorithm for credit card validation
- Complete ID card check code verification for China
- IPv4/IPv6 address validation
- Strong password policy enforcement
- 40+ comprehensive unit tests
- 9 practical usage examples
- Production-ready for form validation and data sanitization

Compile and run tests:
```bash
cd Java/validation_utils
javac *.java && java validation_utils.ValidationUtilsTest
```

Run example:
```bash
cd Java
javac -cp . examples/validation_utils_example.java validation_utils/*.java
java -cp . examples.validation_utils_example
```

Usage example:
```java
import validation_utils.ValidationUtils;

// Basic validation
if (ValidationUtils.isBlank(userInput)) {
    System.out.println("Input is required");
}

// Email validation
if (ValidationUtils.isEmail("user@example.com")) {
    // Process valid email
}

// Phone validation (China)
if (ValidationUtils.isChinaMobile("13800138000")) {
    // Valid China mobile number
}

// IP validation
if (ValidationUtils.isIpv4("192.168.1.1")) {
    // Valid IPv4 address
}

// ID card validation (China)
if (ValidationUtils.isChinaIdCard("110101199001011234")) {
    // Valid ID card number
}

// Credit card validation
if (ValidationUtils.isCreditCard("4532015112830366")) {
    // Valid credit card number (Luhn check passed)
}

// Range validation
if (ValidationUtils.lengthBetween(password, 8, 20)) {
    // Password length is valid
}

if (ValidationUtils.between(age, 18, 120)) {
    // Age is within valid range
}

// Regex validation
if (ValidationUtils.matches(input, "^[A-Z]{3}\\d{4}$")) {
    // Matches pattern (e.g., ABC1234)
}

// Find all matches
List<String> numbers = ValidationUtils.findAll(text, "\\d+");

// Null-safe utilities
if (ValidationUtils.equals(str1, str2)) {
    // Strings are equal (null-safe)
}

if (ValidationUtils.contains(text, "keyword")) {
    // Text contains keyword (null-safe)
}
```

---

### Rust - JSON Utilities

Location: `Rust/json_utils/mod.rs`

Functions:

**Parsing:**
- **parse_json**: `parse_json(input)` - Parse JSON string into JsonValue
- **parse_json_or_null**: `parse_json_or_null(input)` - Parse JSON, return null on error
- **is_valid_json**: `is_valid_json(input)` - Check if string is valid JSON

**JSON Value Types:**
- **JsonValue::Null** - Represents JSON null value
- **JsonValue::Bool** - Represents JSON boolean (true/false)
- **JsonValue::Number** - Represents JSON number (f64)
- **JsonValue::String** - Represents JSON string
- **JsonValue::Array** - Represents JSON array with indexed access
- **JsonValue::Object** - Represents JSON object with key-value access

**Type Checking:**
- **is_null**: Check if value is null
- **is_bool**: Check if value is boolean
- **is_number**: Check if value is number
- **is_string**: Check if value is string
- **is_array**: Check if value is array
- **is_object**: Check if value is object

**Type Conversion:**
- **as_bool**: Get value as bool (default: false)
- **as_bool_or**: Get value as bool with custom default
- **as_i64**: Get value as i64 (default: 0)
- **as_i64_or**: Get value as i64 with custom default
- **as_f64**: Get value as f64 (default: 0.0)
- **as_f64_or**: Get value as f64 with custom default
- **as_string**: Get value as String (default: empty)
- **as_string_or**: Get value as String with custom default

**Object Access:**
- **get(key)**: Get property by key, returns JsonValue::Null if not found
- **has(key)**: Check if object has key
- **keys()**: Get all keys as Vec<String>
- **len()**: Get number of entries in array or object
- **is_empty()**: Check if array or object is empty

**Array Access:**
- **get_index(index)**: Get element at index, returns JsonValue::Null if out of bounds

**Generation:**
- **JsonValue::null()**: Create null value
- **JsonValue::bool(value)**: Create boolean value
- **JsonValue::number(value)**: Create number value
- **JsonValue::string(value)**: Create string value
- **JsonValue::array(values)**: Create array value
- **JsonValue::object(map)**: Create object value

**Serialization:**
- **to_json**: Convert JsonValue to compact JSON string
- **to_pretty_json**: Convert JsonValue to pretty-printed JSON (2-space indent)
- **to_pretty_string_with_indent**: Convert with custom indentation

**Utility:**
- **merge**: Merge another JSON object into this one (objects only)
- **From conversions**: Convert from (), bool, i8-i64, u8-u64, f32, f64, String, &str, Vec<T>, HashMap<String, T>, Option<T>

**Error Handling:**
- **JsonError**: Comprehensive error type with position information
- **JsonResult<T>**: Result type alias for JSON operations

**Features:**
- Zero dependencies, uses only Rust standard library
- Complete JSON support: null, boolean, number, string, array, object
- Type-safe access with default values
- Full Unicode and escape sequence support (\\n, \\t, \", \\, \\uXXXX)
- Pretty printing with customizable indentation
- Round-trip parsing (parse → generate → parse)
- Safe parsing with Result return type
- Scientific notation support (1e10, -1.5e-3)
- 50+ comprehensive unit tests
- 15 practical usage examples
- Production-ready for JSON processing tasks

Compile and run tests:
```bash
cd Rust/json_utils
rustc --test mod.rs -o json_test && ./json_test
```

Run example:
```bash
cd Rust/examples
rustc json_utils_example.rs -o json_example && ./json_example
```

Usage example:
```rust
use json_utils::{JsonValue, parse_json};

// Parse JSON
let json = r#"{"name": "John", "age": 30}"#;
let value = parse_json(json).unwrap();

// Access values
let name = value.get("name").as_string();  // "John"
let age = value.get("age").as_i64();       // 30

// Type-safe access with defaults
let missing = value.get("missing").as_string_or("default");

// Create JSON programmatically
let mut map = std::collections::HashMap::new();
map.insert("id".to_string(), JsonValue::number(1.0));
map.insert("name".to_string(), JsonValue::string("Alice"));
let obj = JsonValue::object(map);

// Serialize
println!("{}", obj.to_json());        // Compact
println!("{}", obj.to_pretty_json()); // Pretty printed

// Parse arrays
let arr = parse_json("[1, 2, 3]").unwrap();
let first = arr.get_index(0).as_i64();  // 1

// Validate JSON
let is_valid = is_valid_json("{}");  // true
```

---

### C# - Email Utilities

Location: `C#/email_utils/mod.cs`

Functions:

**Validation:**
- **IsValid**: `EmailUtils.IsValid(email)` - Validate email format (RFC 5322 compliant)
- **IsValidStrict**: `EmailUtils.IsValidStrict(email)` - Stricter validation (no consecutive dots, valid TLD)
- **IsValidMailAddress**: `EmailUtils.IsValidMailAddress(email)` - Validate using .NET MailAddress
- **IsDisposable**: `EmailUtils.IsDisposable(email)` - Check if disposable/temporary email domain
- **IsFreeProvider**: `EmailUtils.IsFreeProvider(email)` - Check if known free email provider (Gmail, Yahoo, etc.)
- **IsBusinessEmail**: `EmailUtils.IsBusinessEmail(email)` - Check if likely business/corporate email

**Parsing:**
- **GetLocalPart**: `EmailUtils.GetLocalPart(email)` - Extract username part before @
- **GetDomain**: `EmailUtils.GetDomain(email)` - Extract domain part after @
- **GetTld**: `EmailUtils.GetTld(email)` - Extract top-level domain (.com, .org, etc.)
- **Parse**: `EmailUtils.Parse(email)` - Parse into EmailParts object with all components

**Formatting:**
- **Normalize**: `EmailUtils.Normalize(email)` - Normalize (lowercase domain, trim whitespace)
- **ToLower**: `EmailUtils.ToLower(email)` - Convert entire email to lowercase
- **Mask**: `EmailUtils.Mask(email, visibleChars, maskChar)` - Mask for privacy (e.g., t***@example.com)
- **ToDisplayName**: `EmailUtils.ToDisplayName(email)` - Generate display name from email (john.doe -> John Doe)

**Manipulation:**
- **ChangeDomain**: `EmailUtils.ChangeDomain(email, newDomain)` - Change email domain
- **AddPlusTag**: `EmailUtils.AddPlusTag(email, tag)` - Add plus addressing tag (user+tag@example.com)
- **RemovePlusTag**: `EmailUtils.RemovePlusTag(email)` - Remove plus tag from email
- **GenerateRandom**: `EmailUtils.GenerateRandom(domain, length)` - Generate random email address
- **GenerateTestEmail**: `EmailUtils.GenerateTestEmail(prefix, domain)` - Generate test email with timestamp

**Bulk Operations:**
- **FilterValid**: `EmailUtils.FilterValid(emails)` - Filter list to valid emails only
- **Deduplicate**: `EmailUtils.Deduplicate(emails)` - Remove duplicates (case-insensitive)
- **ExtractDomains**: `EmailUtils.ExtractDomains(emails)` - Extract unique domains from list
- **GroupByDomain**: `EmailUtils.GroupByDomain(emails)` - Group emails by domain
- **SortByDomain**: `EmailUtils.SortByDomain(emails)` - Sort emails by domain then local part

**Utility:**
- **Equals**: `EmailUtils.Equals(email1, email2)` - Compare emails (case-insensitive)
- **GetProviderType**: `EmailUtils.GetProviderType(email)` - Get EmailProviderType enum (Free, Business, Disposable, Unknown)
- **AddDisposableDomain**: `EmailUtils.AddDisposableDomain(domain)` - Add custom disposable domain
- **AddFreeProviderDomain**: `EmailUtils.AddFreeProviderDomain(domain)` - Add custom free provider domain

**EmailParts Class:**
- Properties: `LocalPart`, `Domain`, `Tld`, `Original`
- Method: `ToString()` - Returns full email address

**EmailProviderType Enum:**
- `Unknown` - Invalid or unrecognized
- `Free` - Free email provider (Gmail, Yahoo, etc.)
- `Business` - Corporate/business email
- `Disposable` - Temporary/disposable email

**Features:**
- Zero dependencies, uses only .NET standard library
- RFC 5322 compliant email validation
- Built-in lists of disposable and free email providers
- Support for plus addressing (Gmail style)
- Privacy masking for display purposes
- Bulk operations for email list processing
- Display name generation from email format
- 45+ comprehensive unit tests
- 7 practical usage examples
- Production-ready for user registration and email processing

Compile and run tests:
```bash
cd C#/email_utils
dotnet build
dotnet run --project email_utils_test.cs
```

Run example:
```bash
cd C#/examples
dotnet run email_utils_example.cs
```

Usage example:
```csharp
using AllToolkit;

// Basic validation
bool isValid = EmailUtils.IsValid("user@example.com");  // true
bool isStrict = EmailUtils.IsValidStrict("user..name@example.com");  // false

// Check email type
bool isGmail = EmailUtils.IsFreeProvider("user@gmail.com");  // true
bool isBusiness = EmailUtils.IsBusinessEmail("user@company.com");  // true
bool isDisposable = EmailUtils.IsDisposable("user@tempmail.com");  // true

// Parse email
var parts = EmailUtils.Parse("john.doe@example.com");
Console.WriteLine(parts.LocalPart);  // "john.doe"
Console.WriteLine(parts.Domain);     // "example.com"
Console.WriteLine(parts.Tld);        // "com"

// Formatting
string masked = EmailUtils.Mask("john.doe@example.com");  // "j***@example.com"
string display = EmailUtils.ToDisplayName("john.doe@example.com");  // "John Doe"
string normalized = EmailUtils.Normalize("User@EXAMPLE.COM");  // "User@example.com"

// Plus addressing (Gmail style)
string tagged = EmailUtils.AddPlusTag("user@gmail.com", "newsletter");
// "user+newsletter@gmail.com"
string clean = EmailUtils.RemovePlusTag("user+tag@gmail.com");
// "user@gmail.com"

// Bulk operations
var emails = new List<string> { "a@gmail.com", "b@gmail.com", "c@company.com" };
var domains = EmailUtils.ExtractDomains(emails);  // [ "gmail.com", "company.com" ]
var grouped = EmailUtils.GroupByDomain(emails);   // Dictionary by domain

// Generate test emails
string random = EmailUtils.GenerateRandom();  // "abc123@example.com"
string test = EmailUtils.GenerateTestEmail();  // "test.1234567890@example.com"
```

---

### Python - INI Config Utilities

Location: `Python/ini_config_utils/mod.py`

Functions:

**IniConfig Class:**
- **read_file**: `config.read_file(filepath, encoding)` - 从文件读取INI配置
- **read_string**: `config.read_string(content)` - 从字符串解析INI配置
- **write_file**: `config.write_file(filepath, encoding)` - 写入配置文件
- **write_string**: `config.write_string()` - 生成INI格式字符串
- **section**: `config.section(name, create)` - 获取或创建节
- **add_section**: `config.add_section(name, comment)` - 添加新节
- **remove_section**: `config.remove_section(name)` - 删除节
- **has_section**: `config.has_section(name)` - 检查节是否存在
- **sections**: `config.sections()` - 获取所有节名称列表
- **get**: `config.get(section, key, default, type_func)` - 获取配置值(支持类型转换)
- **get_int**: `config.get_int(section, key, default)` - 获取整数值
- **get_float**: `config.get_float(section, key, default)` - 获取浮点数值
- **get_bool**: `config.get_bool(section, key, default)` - 获取布尔值
- **get_list**: `config.get_list(section, key, default, separator)` - 获取列表值
- **set**: `config.set(section, key, value, comment)` - 设置配置值
- **has**: `config.has(section, key)` - 检查配置是否存在
- **remove**: `config.remove(section, key)` - 删除配置
- **to_dict**: `config.to_dict()` - 转换为字典
- **from_dict**: `config.from_dict(data)` - 从字典加载
- **copy**: `config.copy()` - 创建深拷贝
- **clear**: `config.clear()` - 清空所有配置
- **merge**: `config.merge(other, overwrite)` - 合并另一个配置
- **validate**: `config.validate(schema)` - 验证配置结构

**IniSection Class:**
- **get**: `section.get(key, default, type_func)` - 获取键值
- **get_int**: `section.get_int(key, default)` - 获取整数值
- **get_float**: `section.get_float(key, default)` - 获取浮点数值
- **get_bool**: `section.get_bool(key, default)` - 获取布尔值
- **get_list**: `section.get_list(key, default, separator)` - 获取列表值
- **set**: `section.set(key, value, comment)` - 设置键值
- **has**: `section.has(key)` - 检查键是否存在
- **remove**: `section.remove(key)` - 删除键
- **keys**: `section.keys()` - 获取所有键名
- **items**: `section.items()` - 获取所有键值对
- **clear**: `section.clear()` - 清空节内数据
- **copy**: `section.copy()` - 创建节的深拷贝

**Convenience Functions:**
- **read_ini**: `read_ini(filepath, encoding)` - 读取INI文件
- **write_ini**: `write_ini(config, filepath, encoding)` - 写入INI文件
- **parse_ini**: `parse_ini(content)` - 解析INI字符串
- **create_ini**: `create_ini(data)` - 从字典创建配置

**Type Conversion:**
- 自动类型转换: int, float, bool, list
- 布尔值支持: true/false, yes/no, 1/0, on/off, enabled/disabled
- 列表值支持: 自定义分隔符，默认逗号

**Comment Support:**
- 全局注释(文件开头)
- 节注释
- 键注释
- 注释保留和写入

**Validation:**
- 结构验证: 检查必需的节和键
- 返回详细的错误信息列表

**Features:**
- Zero dependencies, uses only Python standard library
- Full INI format support with sections and key-value pairs
- Type-safe access with automatic conversion
- Default value support for all getter methods
- Comment preservation during read/write operations
- Unicode/UTF-8 full support (Chinese, Emoji, etc.)
- Dictionary conversion for easy data exchange
- Configuration merging with overwrite control
- Schema validation for configuration integrity
- 44 comprehensive unit tests covering all functionality
- 8 practical usage examples
- Production-ready for application configuration management

Run tests:
```bash
cd Python/ini_config_utils
python ini_config_utils_test.py
```

Run example:
```bash
cd Python/examples
python ini_config_utils_example.py
```

Usage example:
```python
from ini_config_utils.mod import IniConfig, read_ini, parse_ini

# Create and configure
config = IniConfig()
config.set('database', 'host', 'localhost')
config.set('database', 'port', 3306)
config.set('app', 'debug', True)

# Type-safe access
port = config.get_int('database', 'port')  # 3306
debug = config.get_bool('app', 'debug')    # True

# Parse from string
ini_content = """
[database]
host = localhost
port = 5432
"""
config = parse_ini(ini_content)

# Read from file
config = read_ini('config.ini')

# Write to file
config.write_file('output.ini')

# Configuration validation
schema = {
    'database': ['host', 'port', 'username', 'password'],
    'app': ['name', 'debug']
}
errors = config.validate(schema)
```

---

### C++ - Cache Utilities

Location: `C++/cache_utils/mod.hpp`

Functions:

**Cache Class:**
- **Constructor**: `Cache<K, V>(max_size, policy, max_bytes)` - Create cache with size limit, eviction policy, and optional memory limit
- **set**: `cache.set(key, value, ttl)` - Store value with optional TTL (Time To Live)
- **get**: `cache.get(key)` - Retrieve value, returns `std::optional<V>`
- **get_or_default**: `cache.get_or_default(key, default_value)` - Get value or return default
- **get_or_compute**: `cache.get_or_compute(key, factory, ttl)` - Get cached value or compute and store
- **has**: `cache.has(key)` - Check if key exists and not expired
- **remove**: `cache.remove(key)` - Remove entry by key
- **clear**: `cache.clear()` - Remove all entries
- **size**: `cache.size()` - Get number of entries
- **empty**: `cache.empty()` - Check if cache is empty
- **keys**: `cache.keys()` - Get all non-expired keys
- **purge_expired**: `cache.purge_expired()` - Remove all expired entries, returns count
- **stats**: `cache.stats()` - Get cache statistics
- **reset_stats**: `cache.reset_stats()` - Reset statistics counters
- **memory_usage**: `cache.memory_usage()` - Get current memory usage in bytes

**Eviction Policies:**
- `EvictionPolicy::LRU` - Least Recently Used
- `EvictionPolicy::LFU` - Least Frequently Used
- `EvictionPolicy::FIFO` - First In First Out
- `EvictionPolicy::RANDOM` - Random eviction

**CacheStats Structure:**
- **hits**: Number of cache hits
- **misses**: Number of cache misses
- **evictions**: Number of evicted entries
- **expirations**: Number of expired entries
- **current_size**: Current number of entries
- **max_size**: Maximum allowed entries
- **hit_rate()**: Calculate hit rate (0.0 to 1.0)

**CacheEntry Features:**
- Automatic TTL expiration tracking
- Access count tracking (for LFU)
- Last access timestamp (for LRU)
- Creation timestamp (for FIFO)

**Features:**
- Zero dependencies, header-only library (C++11+)
- Thread-safe using std::mutex
- Multiple eviction policies (LRU, LFU, FIFO, RANDOM)
- TTL (Time To Live) support for automatic expiration
- Size-based and memory-based eviction
- Statistics tracking (hits, misses, hit rate)
- Generic template support for any key/value types
- Optional custom size calculator for memory tracking
- 15 comprehensive unit tests
- 10 usage examples covering all functionality
- Production-ready for high-performance caching

Compile and run tests:
```bash
cd C++/cache_utils
g++ -std=c++11 -o cache_utils_test cache_utils_test.cpp && ./cache_utils_test
```

Run example:
```bash
cd C++/examples
g++ -std=c++11 -o cache_utils_example cache_utils_example.cpp && ./cache_utils_example
```

Usage example:
```cpp
#include "cache_utils/mod.hpp"
using namespace alltoolkit;

// Create cache with max 100 entries, LRU eviction
Cache<std::string, std::string> cache(100, EvictionPolicy::LRU);

// Store values
cache.set("name", "Alice");
cache.set("session", "token123", std::chrono::seconds(3600)); // 1 hour TTL

// Retrieve values
auto name = cache.get("name");
if (name.has_value()) {
    std::cout << *name << std::endl;  // "Alice"
}

// Get or compute (lazy loading)
int result = cache.get_or_compute("expensive_key", [&]() {
    return expensive_computation();
}, std::chrono::seconds(60));

// Check statistics
auto stats = cache.stats();
std::cout << "Hit rate: " << (stats.hit_rate() * 100) << "%" << std::endl;
```

---

### ArkTS - Color Utilities

Location: `ArkTS/color_utils/mod.ets`

Functions:

**Color Class:**
- **Constructor**: `new Color(r, g, b, a)` - Create color with RGBA values (0-255 for RGB, 0-1 for alpha)
- **toHex**: `color.toHex()` - Convert to HEX string (#RRGGBB or #RRGGBBAA)
- **toRgb**: `color.toRgb()` - Convert to RGB/RGBA string
- **toHsl**: `color.toHsl()` - Convert to HSL object {h, s, l, a}
- **toHslString**: `color.toHslString()` - Convert to HSL/HSLA string
- **toHsv**: `color.toHsv()` - Convert to HSV object {h, s, v, a}
- **toCmyk**: `color.toCmyk()` - Convert to CMYK object {c, m, y, k, a}
- **lighten**: `color.lighten(amount)` - Lighten by percentage (0-100)
- **darken**: `color.darken(amount)` - Darken by percentage (0-100)
- **saturate**: `color.saturate(amount)` - Increase saturation (0-100)
- **desaturate**: `color.desaturate(amount)` - Decrease saturation (0-100)
- **fade**: `color.fade(amount)` - Reduce alpha by percentage
- **grayscale**: `color.grayscale()` - Get grayscale value (0-255)
- **brightness**: `color.brightness()` - Get brightness value (0-255)
- **isLight**: `color.isLight()` - Check if color is light
- **isDark**: `color.isDark()` - Check if color is dark
- **complement**: `color.complement()` - Get complementary color
- **contrast**: `color.contrast()` - Get black or white contrast color
- **mix**: `color.mix(other, ratio)` - Mix with another color
- **clone**: `color.clone()` - Create a copy
- **equals**: `color.equals(other)` - Compare colors

**ColorUtils Static Methods:**
- **parseHex**: `ColorUtils.parseHex(hex)` - Parse HEX color (#RGB, #RGBA, #RRGGBB, #RRGGBBAA)
- **parseRgb**: `ColorUtils.parseRgb(rgb)` - Parse RGB/RGBA string
- **parseHsl**: `ColorUtils.parseHsl(hsl)` - Parse HSL/HSLA string
- **parse**: `ColorUtils.parse(color)` - Parse any color format + named colors
- **isValid**: `ColorUtils.isValid(color)` - Validate color string
- **hslToRgb**: `ColorUtils.hslToRgb(h, s, l, a)` - Convert HSL to Color
- **hsvToRgb**: `ColorUtils.hsvToRgb(h, s, v, a)` - Convert HSV to Color
- **cmykToRgb**: `ColorUtils.cmykToRgb(c, m, y, k, a)` - Convert CMYK to Color
- **random**: `ColorUtils.random(alpha?)` - Generate random color
- **randomBright**: `ColorUtils.randomBright()` - Generate random bright color
- **randomPastel**: `ColorUtils.randomPastel()` - Generate random pastel color
- **randomDark**: `ColorUtils.randomDark()` - Generate random dark color
- **gradient**: `ColorUtils.gradient(start, end, steps)` - Generate color gradient
- **analogous**: `ColorUtils.analogous(color, count?)` - Generate analogous colors
- **triadic**: `ColorUtils.triadic(color)` - Generate triadic colors
- **tetradic**: `ColorUtils.tetradic(color)` - Generate tetradic colors
- **splitComplementary**: `ColorUtils.splitComplementary(color)` - Generate split complementary
- **monochromatic**: `ColorUtils.monochromatic(color, count?)` - Generate monochromatic colors
- **blend**: `ColorUtils.blend(c1, c2, mode)` - Blend colors using BlendMode
- **luminance**: `ColorUtils.luminance(color)` - Calculate luminance (0-1)
- **contrastRatio**: `ColorUtils.contrastRatio(c1, c2)` - Calculate WCAG contrast ratio
- **meetsWCAGAA**: `ColorUtils.meetsWCAGAA(c1, c2, largeText?)` - Check WCAG AA compliance
- **meetsWCAGAAA**: `ColorUtils.meetsWCAGAAA(c1, c2, largeText?)` - Check WCAG AAA compliance
- **bestContrast**: `ColorUtils.bestContrast(color)` - Get best contrast (black/white)

**BlendMode Enum:**
- `NORMAL`, `MULTIPLY`, `SCREEN`, `OVERLAY`, `DARKEN`, `LIGHTEN`
- `COLOR_DODGE`, `COLOR_BURN`, `DIFFERENCE`, `EXCLUSION`, `HARD_LIGHT`, `SOFT_LIGHT`

**Color Constants:**
- `ColorUtils.BLACK`, `ColorUtils.WHITE`, `ColorUtils.RED`, `ColorUtils.GREEN`, `ColorUtils.BLUE`
- `ColorUtils.YELLOW`, `ColorUtils.CYAN`, `ColorUtils.MAGENTA`, `ColorUtils.TRANSPARENT`

**Features:**
- Zero dependencies, uses only ArkTS standard library
- Full color format support: HEX, RGB, RGBA, HSL, HSLA, HSV, CMYK
- Named color support (black, white, red, etc.)
- Color manipulation: lighten, darken, saturate, desaturate, fade
- Color scheme generation: analogous, triadic, tetradic, monochromatic
- 12 blend modes for advanced color mixing
- WCAG accessibility compliance checking
- Contrast ratio calculation
- Gradient generation
- Complete test suite with 30+ test cases
- 10 comprehensive usage examples
- Production-ready for HarmonyOS UI development

Run tests:
```bash
cd ArkTS/color_utils
# Requires HarmonyOS development environment
```

Run example:
```bash
cd ArkTS/examples
# Requires HarmonyOS development environment
```

Usage example:
```typescript
import { Color, ColorUtils, BlendMode } from './color_utils/mod';

// Create colors
const red = new Color(255, 0, 0);
const blue = new Color(0, 0, 255);

// Parse colors
const parsed = ColorUtils.parseHex('#ff5733');
const fromRgb = ColorUtils.parseRgb('rgb(100, 150, 200)');

// Convert formats
console.log(red.toHex());        // '#ff0000'
console.log(red.toHslString());  // 'hsl(0, 100%, 50%)'

// Manipulate colors
const lighter = red.lighten(20);
const darker = blue.darken(30);
const complement = red.complement();

// Mix colors
const purple = red.mix(blue, 0.5);

// Generate gradients
const gradient = ColorUtils.gradient(red, blue, 5);

// Color schemes
const triadic = ColorUtils.triadic(red);
const analogous = ColorUtils.analogous(blue, 3);

// Accessibility
const contrast = ColorUtils.contrastRatio(red, new Color(255, 255, 255));
const passesAA = ColorUtils.meetsWCAGAA(red, new Color(255, 255, 255));

// Blend modes
const blended = ColorUtils.blend(red, blue, BlendMode.MULTIPLY);
```

---

### Ruby - HTTP Utilities

Location: `Ruby/http_utils/mod.rb`

Functions:

**HTTP Methods:**
- **GET**: `HttpUtils.get(url, options)` - Send HTTP GET request
- **POST**: `HttpUtils.post(url, body, content_type, options)` - Send HTTP POST request
- **POST JSON**: `HttpUtils.post_json(url, data, options)` - Send JSON POST request
- **POST Form**: `HttpUtils.post_form(url, data, options)` - Send form POST request
- **PUT**: `HttpUtils.put(url, body, content_type, options)` - Send HTTP PUT request
- **PUT JSON**: `HttpUtils.put_json(url, data, options)` - Send JSON PUT request
- **DELETE**: `HttpUtils.delete(url, options)` - Send HTTP DELETE request
- **PATCH**: `HttpUtils.patch(url, body, content_type, options)` - Send HTTP PATCH request
- **HEAD**: `HttpUtils.head(url, options)` - Send HTTP HEAD request

**URL Utilities:**
- **URL Encode**: `HttpUtils.url_encode(str)` - URL encode a string (spaces → +)
- **URL Decode**: `HttpUtils.url_decode(str)` - URL decode a string
- **Build Query String**: `HttpUtils.build_query_string(params)` - Build query string from hash
- **Build URL**: `HttpUtils.build_url(base_url, params)` - Build URL with query parameters
- **Parse URL**: `HttpUtils.parse_url(url)` - Parse URL into components (scheme, host, port, path, query, fragment, userinfo)
- **Parse Query String**: `HttpUtils.parse_query_string(query_string)` - Parse query string to hash
- **Validate URL**: `HttpUtils.valid_url?(url)` - Check if string is valid URL
- **Get Domain**: `HttpUtils.get_domain(url)` - Extract domain from URL
- **Get Path**: `HttpUtils.get_path(url)` - Extract path from URL
- **Add Query Params**: `HttpUtils.add_query_params(url, params)` - Add query parameters to URL

**HTTP Response (Response class):**
- **Status Code**: `response.status_code` - HTTP status code
- **Status Message**: `response.status_message` - HTTP status text
- **Headers**: `response.headers` - Response headers hash
- **Body**: `response.body` - Response body string
- **Success**: `response.success?` - True if status 200-299
- **JSON Parse**: `response.json` - Parse body as JSON
- **Is JSON**: `response.json?` - Check if body is valid JSON
- **Get Header**: `response.header(name)` - Get header value (case-insensitive)

**HTTP Options (Options class):**
- **Headers**: Custom request headers hash
- **Timeout**: Request timeout in seconds (default: 30)
- **Follow Redirects**: Auto-follow redirects (default: true)
- **Max Redirects**: Maximum redirect hops (default: 10)
- **Verify SSL**: SSL certificate verification (default: true)

**Features:**
- Zero dependencies, uses only Ruby standard library (net/http, net/https, uri, json, cgi)
- Full HTTP method support: GET, POST, PUT, DELETE, PATCH, HEAD
- Automatic JSON and form data encoding
- Complete URL manipulation utilities
- Custom headers and timeout configuration
- Response time tracking
- SSL/TLS certificate verification control
- Response success status checking
- Built-in JSON validation
- Complete test suite with 30+ test cases
- 11 comprehensive usage examples
- Production-ready for REST API clients

Run tests:
```bash
cd Ruby/http_utils
ruby http_utils_test.rb
```

Run example:
```bash
cd Ruby/examples
ruby http_utils_example.rb
```

Usage example:
```ruby
require_relative 'Ruby/http_utils/mod'

# GET request
response = HttpUtils.get('https://api.example.com/users')
if response.success?
  data = response.json
  puts data.inspect
end

# POST JSON
response = HttpUtils.post_json('https://api.example.com/users', {
  name: 'John',
  email: 'john@example.com'
})

# POST Form
response = HttpUtils.post_form('https://api.example.com/login', {
  username: 'admin',
  password: 'secret'
})

# URL building
url = HttpUtils.build_url('https://api.example.com/search', {
  q: 'hello world',
  page: 1
})
# Result: 'https://api.example.com/search?q=hello+world&page=1'

# URL parsing
parsed = HttpUtils.parse_url('https://api.example.com:8080/v1/users')
# parsed[:host] = 'api.example.com'
# parsed[:port] = 8080

# URL validation
is_valid = HttpUtils.valid_url?('https://example.com')  # true

# Custom options
options = HttpUtils::Options.new
options.timeout = 60
options.headers = { 'Authorization' => 'Bearer token123' }
response = HttpUtils.get('https://api.example.com/protected', options)
```

---

### Kotlin - Crypto Utilities

Location: `Kotlin/crypto_utils/mod.kt`

Functions:

**Hash Functions:**
- **md5**: `md5(input)` - Calculate MD5 hash (32-character hex)
- **sha1**: `sha1(input)` - Calculate SHA1 hash (40-character hex)
- **sha256**: `sha256(input)` - Calculate SHA256 hash (64-character hex)
- **sha384**: `sha384(input)` - Calculate SHA384 hash (96-character hex)
- **sha512**: `sha512(input)` - Calculate SHA512 hash (128-character hex)
- **sha256Bytes**: `sha256Bytes(data)` - Hash byte array
- **sha256File**: `sha256File(filePath)` - Hash file contents
- **hash**: `hash(input, algorithm)` - Generic hash with algorithm

**HMAC Functions:**
- **hmacSha256**: `hmacSha256(message, key)` - Calculate HMAC-SHA256 signature
- **hmacSha512**: `hmacSha512(message, key)` - Calculate HMAC-SHA512 signature
- **verifyHmacSha256**: `verifyHmacSha256(message, key, hmac)` - Verify HMAC-SHA256 signature
- **hmac**: `hmac(message, key, algorithm)` - Generic HMAC calculation

**Base64 Encoding:**
- **base64Encode**: `base64Encode(input)` - Encode string to Base64
- **base64Decode**: `base64Decode(input)` - Decode Base64 string
- **base64EncodeBytes**: `base64EncodeBytes(data)` - Encode byte array to Base64
- **base64DecodeToBytes**: `base64DecodeToBytes(input)` - Decode Base64 to byte array
- **base64UrlEncode**: `base64UrlEncode(input, padding)` - URL-safe Base64 encoding (RFC 4648)
- **base64UrlDecode**: `base64UrlDecode(input)` - Decode URL-safe Base64
- **isValidBase64**: `isValidBase64(input)` - Validate Base64 format

**Hex Encoding:**
- **hexEncode**: `hexEncode(input)` - Encode string to hexadecimal
- **hexDecode**: `hexDecode(input)` - Decode hexadecimal string
- **bytesToHex**: `bytesToHex(bytes)` - Convert byte array to hex
- **hexToBytes**: `hexToBytes(hex)` - Convert hex to byte array
- **isValidHex**: `isValidHex(input)` - Validate hexadecimal format

**UUID Generation:**
- **uuid**: `uuid()` - Generate standard UUID v4 (36 chars with hyphens)
- **uuidSimple**: `uuidSimple()` - Generate UUID without hyphens (32 chars)
- **uuidUpper**: `uuidUpper()` - Generate uppercase UUID
- **isValidUuid**: `isValidUuid(input)` - Validate UUID format

**Random Generation:**
- **randomString**: `randomString(length, chars)` - Generate random string from charset
- **randomAlphanumeric**: `randomAlphanumeric(length)` - Generate alphanumeric string
- **randomNumeric**: `randomNumeric(length)` - Generate numeric-only string
- **randomHex**: `randomHex(length)` - Generate hex string
- **randomHexUpper**: `randomHexUpper(length)` - Generate uppercase hex string
- **randomPassword**: `randomPassword(length)` - Generate secure password with mixed characters

**XOR Encryption:**
- **xorEncrypt**: `xorEncrypt(input, key)` - Simple XOR encryption (returns Base64)
- **xorDecrypt**: `xorDecrypt(input, key)` - Decrypt XOR encrypted data

**URL Encoding:**
- **urlEncode**: `urlEncode(input)` - URL encode string
- **urlDecode**: `urlDecode(input)` - URL decode string

**Validation:**
- **isValidMd5**: `isValidMd5(input)` - Validate MD5 hash format
- **isValidSha1**: `isValidSha1(input)` - Validate SHA1 hash format
- **isValidSha256**: `isValidSha256(input)` - Validate SHA256 hash format
- **isValidSha384**: `isValidSha384(input)` - Validate SHA384 hash format
- **isValidSha512**: `isValidSha512(input)` - Validate SHA512 hash format

**Character Set Constants (CharSets object):**
- `LOWERCASE` - "abcdefghijklmnopqrstuvwxyz"
- `UPPERCASE` - "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
- `DIGITS` - "0123456789"
- `SPECIAL` - "!@#$%^&*()-_=+[]{}|;:,.<>?"
- `HEX` - "0123456789abcdef"
- `HEX_UPPER` - "0123456789ABCDEF"
- `ALPHANUMERIC` - Letters + digits (62 chars)
- `ALL` - All character sets combined

**Features:**
- Zero dependencies, uses only Kotlin/Java standard library
- Cryptographically secure random generation using SecureRandom
- Complete hash support: MD5, SHA1, SHA256, SHA384, SHA512
- HMAC-SHA256/SHA512 for message authentication
- URL-safe Base64 variant (RFC 4648) support
- UUID v4 generation with validation
- Secure password generation with guaranteed character diversity
- XOR encryption for simple obfuscation
- Hash format validation for all supported algorithms
- Complete test suite with 35+ test cases
- 11 comprehensive usage examples covering all functionality
- Production-ready for security-sensitive applications

Compile and run tests:
```bash
cd Kotlin/crypto_utils
kotlinc -include-runtime -d test.jar *.kt && java -jar test.jar
```

Run example:
```bash
cd Kotlin
kotlinc -include-runtime -d example.jar crypto_utils/*.kt examples/crypto_utils_example.kt && java -jar example.jar
```

Usage example:
```kotlin
import crypto_utils.CryptoUtils

// Hash functions
val hash = CryptoUtils.sha256("hello world")
// Returns: "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

// HMAC for API authentication
val signature = CryptoUtils.hmacSha256("payload", "secret_key")
val isValid = CryptoUtils.verifyHmacSha256("payload", "secret_key", signature)

// Base64 encoding
val encoded = CryptoUtils.base64Encode("Hello, World!")
val urlSafe = CryptoUtils.base64UrlEncode("user+name/file", padding = false)

// UUID generation
val uuid = CryptoUtils.uuid()           // "550e8400-e29b-41d4-a716-446655440000"
val simple = CryptoUtils.uuidSimple()   // "550e8400e29b41d4a716446655440000"

// Random generation
val token = CryptoUtils.randomAlphanumeric(32)
val password = CryptoUtils.randomPassword(16)
val otp = CryptoUtils.randomNumeric(6)

// XOR encryption (simple)
val encrypted = CryptoUtils.xorEncrypt("Secret message", "my_key")
val decrypted = CryptoUtils.xorDecrypt(encrypted, "my_key")

// Validation
val isMd5 = CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c592")
val isUuid = CryptoUtils.isValidUuid("550e8400-e29b-41d4-a716-446655440000")
```

---

### Swift - Crypto Utilities

Location: `Swift/crypto_utils/mod.swift`

Functions:

**Hash Functions:**
- **md5**: `md5(input)` - Calculate MD5 hash (32-character hex)
- **sha1**: `sha1(input)` - Calculate SHA1 hash (40-character hex)
- **sha256**: `sha256(input)` - Calculate SHA256 hash (64-character hex)
- **sha384**: `sha384(input)` - Calculate SHA384 hash (96-character hex)
- **sha512**: `sha512(input)` - Calculate SHA512 hash (128-character hex)
- **hash**: `hash(data, algorithm)` - Hash binary data with specified algorithm

**HMAC Functions:**
- **hmacSha256**: `hmacSha256(message:key:)` - Calculate HMAC-SHA256 signature
- **hmacSha512**: `hmacSha512(message:key:)` - Calculate HMAC-SHA512 signature
- **verifyHmacSha256**: `verifyHmacSha256(message:key:hmac:)` - Verify HMAC-SHA256 signature

**Base64 Encoding:**
- **base64Encode**: `base64Encode(input)` - Encode string to Base64
- **base64Decode**: `base64Decode(input)` - Decode Base64 string
- **base64UrlEncode**: `base64UrlEncode(input:padding:)` - URL-safe Base64 encoding (RFC 4648)
- **base64UrlDecode**: `base64UrlDecode(input)` - Decode URL-safe Base64
- **isValidBase64**: `isValidBase64(input)` - Validate Base64 format

**Hex Encoding:**
- **hexEncode**: `hexEncode(input)` - Encode string to hexadecimal
- **hexDecode**: `hexDecode(input)` - Decode hexadecimal string
- **isValidHex**: `isValidHex(input)` - Validate hexadecimal format

**URL Encoding:**
- **urlEncode**: `urlEncode(input)` - URL encode string
- **urlDecode**: `urlDecode(input)` - URL decode string
- **urlEncodeComponent**: `urlEncodeComponent(input)` - URL encode as component (more aggressive)

**UUID Generation:**
- **uuid**: `uuid()` - Generate standard UUID v4 (36 chars with hyphens)
- **uuidUpper**: `uuidUpper()` - Generate uppercase UUID
- **uuidSimple**: `uuidSimple()` - Generate UUID without hyphens (32 chars)
- **isValidUuid**: `isValidUuid(input)` - Validate UUID format

**Random Generation:**
- **randomString**: `randomString(length:characters:)` - Generate random string from charset
- **randomAlphanumeric**: `randomAlphanumeric(length:)` - Generate alphanumeric string
- **randomNumeric**: `randomNumeric(length:)` - Generate numeric-only string
- **randomHex**: `randomHex(length:)` - Generate hex string
- **randomPassword**: `randomPassword(length:)` - Generate secure password with mixed characters

**XOR Encryption:**
- **xorEncrypt**: `xorEncrypt(input:key:)` - Simple XOR encryption (returns Base64)
- **xorDecrypt**: `xorDecrypt(input:key:)` - Decrypt XOR encrypted data

**Validation:**
- **isValidMd5**: `isValidMd5(input)` - Validate MD5 hash format
- **isValidSha1**: `isValidSha1(input)` - Validate SHA1 hash format
- **isValidSha256**: `isValidSha256(input)` - Validate SHA256 hash format
- **isValidHash**: `isValidHash(input:algorithm:)` - Generic hash validation

**Character Set Constants:**
- `lowercaseLetters` - "abcdefghijklmnopqrstuvwxyz"
- `uppercaseLetters` - "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
- `digits` - "0123456789"
- `specialCharacters` - "!@#$%^&*()-_=+[]{}|;:,.<>?"
- `hexCharacters` - "0123456789abcdef"
- `hexCharactersUpper` - "0123456789ABCDEF"
- `urlSafeCharacters` - "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
- `alphanumeric` - Letters + digits (62 chars)
- `allCharacters` - All character sets combined

**Features:**
- Zero dependencies, uses only Apple CryptoKit and Foundation
- Supports iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
- Cryptographically secure random generation using system RNG
- Complete hash support: MD5, SHA1, SHA256, SHA384, SHA512
- HMAC-SHA256/SHA512 for message authentication
- URL-safe Base64 variant (RFC 4648) support
- UUID v4 generation with validation
- Secure password generation with guaranteed character diversity
- XOR encryption for simple obfuscation
- Hash format validation for all supported algorithms
- Complete test suite with 60+ test cases
- 10 comprehensive usage examples covering all functionality
- Production-ready for security-sensitive applications

Run tests:
```bash
cd Swift/crypto_utils
swift test
```

Run example:
```bash
cd Swift/examples
swift crypto_utils_example.swift
```

Usage example:
```swift
import crypto_utils

// Hash functions
let hash = CryptoUtils.sha256("hello world")
// Returns: "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

// HMAC for API authentication
let signature = CryptoUtils.hmacSha256(message: "payload", key: "secret_key")
let isValid = CryptoUtils.verifyHmacSha256(message: "payload", key: "secret_key", hmac: signature)

// Base64 encoding
let encoded = CryptoUtils.base64Encode("Hello, World!")
let urlSafe = CryptoUtils.base64UrlEncode("user+name/file", padding: false)

// UUID generation
let uuid = CryptoUtils.uuid()           // "550e8400-e29b-41d4-a716-446655440000"
let simple = CryptoUtils.uuidSimple()   // "550e8400e29b41d4a716446655440000"

// Random generation
let token = CryptoUtils.randomAlphanumeric(length: 32)
let password = CryptoUtils.randomPassword(length: 16)
let otp = CryptoUtils.randomNumeric(length: 6)

// XOR encryption (simple)
let encrypted = CryptoUtils.xorEncrypt("Secret message", key: "my_key")
let decrypted = CryptoUtils.xorDecrypt(encrypted, key: "my_key")

// Validation
let isMd5 = CryptoUtils.isValidMd5("5d41402abc4b2a76b9719d911017c592")
let isUuid = CryptoUtils.isValidUuid("550e8400-e29b-41d4-a716-446655440000")
```

---

### Rust - Random Utilities

Location: `Rust/random_utils/mod.rs`

Functions:

**Random Number Generation:**
- **random_i32**: `random_i32()` - Generate a random 32-bit signed integer
- **random_i64**: `random_i64()` - Generate a random 64-bit signed integer
- **random_u32**: `random_u32()` - Generate a random 32-bit unsigned integer
- **random_u64**: `random_u64()` - Generate a random 64-bit unsigned integer
- **random_int**: `random_int(min, max)` - Generate a random integer in range [min, max] (inclusive)
- **random_i64_range**: `random_i64_range(min, max)` - Generate a random i64 in range [min, max]
- **random_float**: `random_float()` - Generate a random float in range [0.0, 1.0)
- **random_float_range**: `random_float_range(min, max)` - Generate a random float in range [min, max)
- **random_bool**: `random_bool()` - Generate a random boolean (50% probability)
- **random_bool_with_probability**: `random_bool_with_probability(probability)` - Generate boolean with custom probability

**Random String Generation:**
- **random_string**: `random_string(length)` - Generate random alphabetic string
- **random_alphanumeric**: `random_alphanumeric(length)` - Generate random alphanumeric string
- **random_numeric**: `random_numeric(length)` - Generate random numeric string
- **random_hex**: `random_hex(length)` - Generate random lowercase hex string
- **random_hex_upper**: `random_hex_upper(length)` - Generate random uppercase hex string
- **random_urlsafe**: `random_urlsafe(length)` - Generate URL-safe random string
- **random_string_from_charset**: `random_string_from_charset(length, charset)` - Generate string from custom charset

**Password Generation:**
- **random_password**: `random_password(length)` - Generate secure password with guaranteed character types (min length: 4)

**UUID Generation (RFC 4122 v4):**
- **uuid_v4**: `uuid_v4()` - Generate standard UUID v4 (36 chars with hyphens)
- **uuid_v4_compact**: `uuid_v4_compact()` - Generate compact UUID v4 (32 chars, no hyphens)
- **uuid_v4_upper**: `uuid_v4_upper()` - Generate uppercase UUID v4
- **is_valid_uuid**: `is_valid_uuid(uuid)` - Validate UUID string format

**Random Selection:**
- **pick**: `pick(items)` - Pick a random element from a slice
- **pick_multiple**: `pick_multiple(items, count)` - Pick multiple random elements (with replacement)
- **pick_unique**: `pick_unique(items, count)` - Pick multiple unique random elements (without replacement)
- **shuffle**: `shuffle(items)` - Shuffle a slice in-place
- **shuffled**: `shuffled(items)` - Return a shuffled copy of a slice

**Random Color Generation:**
- **random_rgb**: `random_rgb()` - Generate random RGB color as (r, g, b) tuple
- **random_hex_color**: `random_hex_color()` - Generate random hex color string (e.g., "#ff5733")
- **random_rgba**: `random_rgba()` - Generate random RGBA color as (r, g, b, a) tuple

**Random Date/Time:**
- **random_timestamp**: `random_timestamp(min, max)` - Generate random Unix timestamp
- **random_duration_ms**: `random_duration_ms(min, max)` - Generate random duration in milliseconds

**Statistical Distributions:**
- **random_normal**: `random_normal(mean, std_dev)` - Generate from normal (Gaussian) distribution
- **random_exponential**: `random_exponential(lambda)` - Generate from exponential distribution

**Character Set Constants:**
- `LOWERCASE` - "abcdefghijklmnopqrstuvwxyz"
- `UPPERCASE` - "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
- `DIGITS` - "0123456789"
- `SPECIAL_CHARS` - "!@#$%^&*()-_=+[]{}|;:,.<>?"
- `HEX_CHARS` - "0123456789abcdef"
- `HEX_CHARS_UPPER` - "0123456789ABCDEF"
- `URL_SAFE_CHARS` - "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

**Features:**
- Zero dependencies, uses only Rust standard library (rand crate for enhanced functionality, or pure std)
- Cryptographically secure random generation using thread_rng
- Comprehensive password generation with guaranteed character diversity
- RFC 4122 compliant UUID v4 generation with proper version and variant bits
- Full support for custom character sets
- Statistical distributions (Normal, Exponential) for simulation
- Random selection utilities for collections
- Color generation for graphics and UI applications
- Complete test suite with 20+ test cases
- 7 comprehensive usage examples covering all functionality
- Production-ready for security-sensitive applications

Run tests:
```bash
cd Rust/random_utils
rustc --test mod.rs -o random_test && ./random_test
```

Run example:
```bash
cd Rust/examples
rustc --edition 2021 -L ../random_utils random_utils_example.rs -o random_example && ./random_example
```

Usage example:
```rust
use random_utils::RandomUtils;

// Random numbers
let dice = RandomUtils::random_int(1, 6);
let probability = RandomUtils::random_float();
let biased = RandomUtils::random_bool_with_probability(0.7);

// Random strings
let token = RandomUtils::random_alphanumeric(32);
let hex = RandomUtils::random_hex(16);
let urlsafe = RandomUtils::random_urlsafe(64);

// Secure password
let password = RandomUtils::random_password(16);

// UUID generation
let uuid = RandomUtils::uuid_v4();
let compact = RandomUtils::uuid_v4_compact();

// Random selection
let fruits = vec!["Apple", "Banana", "Cherry"];
let pick = RandomUtils::pick(&fruits);
let shuffled = RandomUtils::shuffled(&fruits);

// Colors
let color = RandomUtils::random_hex_color();  // e.g., "#ff5733"
let (r, g, b) = RandomUtils::random_rgb();

// Distributions
let normal = RandomUtils::random_normal(0.0, 1.0);
let exp = RandomUtils::random_exponential(1.0);
```

---

### Go - CSV Utilities

Location: `Go/csv_utils/mod.go`

Functions:

**Reading:**
- **ReadFile**: `ReadFile(filename)` - Read CSV from file with default options
- **ReadFileWithOptions**: `ReadFileWithOptions(filename, opts)` - Read with custom options
- **ReadString**: `ReadString(data)` - Parse CSV from string
- **ReadStringWithOptions**: `ReadStringWithOptions(data, opts)` - Parse with custom options
- **ReadWithOptions**: `ReadWithOptions(reader, opts)` - Read from any io.Reader

**Writing:**
- **WriteToFile**: `data.WriteToFile(filename)` - Write data to file
- **WriteToFileWithOptions**: `data.WriteToFileWithOptions(filename, opts)` - Write with custom options
- **WriteToString**: `data.WriteToString()` - Convert to CSV string
- **WriteToStringWithOptions**: `data.WriteToStringWithOptions(opts)` - Convert with options
- **WriteWithOptions**: `data.WriteWithOptions(writer, opts)` - Write to io.Writer

**Row Access (CsvRow):**
- **Get**: `row.Get(column)` - Get string value by column name
- **GetInt**: `row.GetInt(column, defaultValue)` - Get integer with default
- **GetFloat**: `row.GetFloat(column, defaultValue)` - Get float64 with default
- **GetBool**: `row.GetBool(column, defaultValue)` - Get boolean with default (supports true/false, yes/no, 1/0)
- **IsEmpty**: `row.IsEmpty()` - Check if row has no data

**Data Filtering:**
- **FilterRows**: `data.FilterRows(predicate)` - Filter rows by predicate function
- **FilterColumns**: `data.FilterColumns(columns)` - Keep only specified columns
- **Find**: `data.Find(predicate)` - Find first matching row
- **FindAll**: `data.FindAll(predicate)` - Find all matching rows
- **Count**: `data.Count(predicate)` - Count matching rows

**Sorting:**
- **SortBy**: `data.SortBy(column)` - Sort by column (ascending, string)
- **SortByWithOptions**: `data.SortByWithOptions(column, ascending, numeric)` - Sort with options

**Column Operations:**
- **GetColumn**: `data.GetColumn(column)` - Get all values as strings
- **GetColumnInt**: `data.GetColumnInt(column)` - Get all values as integers
- **GetColumnFloat**: `data.GetColumnFloat(column)` - Get all values as floats
- **AddColumn**: `data.AddColumn(name, values)` - Add new column
- **RemoveColumn**: `data.RemoveColumn(name)` - Remove column
- **Distinct**: `data.Distinct(column)` - Get unique values

**Row Operations:**
- **GetRow**: `data.GetRow(index)` - Get row by index
- **AddRow**: `data.AddRow(row)` - Add new row
- **RemoveRow**: `data.RemoveRow(index)` - Remove row by index
- **RowCount**: `data.RowCount()` - Get number of rows
- **ColumnCount**: `data.ColumnCount()` - Get number of columns

**Data Transformation:**
- **Transform**: `data.Transform(transformer)` - Apply function to each row
- **TransformColumn**: `data.TransformColumn(column, transformer)` - Transform specific column
- **GroupBy**: `data.GroupBy(column)` - Group rows by column value

**Statistics:**
- **SumColumn**: `data.SumColumn(column)` - Calculate sum of numeric column
- **AvgColumn**: `data.AvgColumn(column)` - Calculate average
- **MinColumn**: `data.MinColumn(column)` - Find minimum value
- **MaxColumn**: `data.MaxColumn(column)` - Find maximum value

**Data Combination:**
- **Join**: `Join(left, right)` - Merge two datasets horizontally (add columns)
- **Merge**: `Merge(first, second)` - Merge two datasets vertically (add rows)

**Validation:**
- **Validate**: `data.Validate()` - Check for missing values, returns invalid row indices
- **IsValid**: `data.IsValid()` - Check if data structure is valid
- **IsValidCsv**: `IsValidCsv(data)` - Check if string is valid CSV

**Conversion:**
- **ToSlice**: `data.ToSlice(hasHeader)` - Convert to 2D string slice
- **ToMapSlice**: `data.ToMapSlice()` - Convert to slice of maps

**Utility:**
- **DetectDelimiter**: `DetectDelimiter(data)` - Auto-detect delimiter (',', ';', '\t', '|')
- **DefaultOptions**: `DefaultOptions()` - Get default CSV options

**CsvWriter:**
- **NewWriter**: `NewWriter()` - Create new CSV writer
- **SetHeaders**: `writer.SetHeaders(headers)` - Set column headers
- **AddRow**: `writer.AddRow(values)` - Add row as string slice
- **AddRowMap**: `writer.AddRowMap(row)` - Add row from map
- **ToCsvData**: `writer.ToCsvData()` - Convert to CsvData
- **SaveToFile**: `writer.SaveToFile(filename)` - Save to file
- **ToString**: `writer.ToString()` - Convert to CSV string

**CsvOptions:**
- **Delimiter**: Field delimiter (default: ',')
- **QuoteChar**: Quote character (default: '"')
- **HasHeader**: First row is header (default: true)
- **TrimSpaces**: Trim leading/trailing spaces (default: true)
- **SkipEmptyRows**: Skip empty rows (default: true)
- **LazyQuotes**: Allow quotes in unquoted fields (default: false)

**Features:**
- Zero dependencies, uses only Go standard library (encoding/csv, io, os)
- Full read/write support with custom delimiters (CSV, TSV, etc.)
- Automatic type conversion (string, int, float, bool)
- Powerful filtering, sorting, and transformation functions
- Data joining (horizontal merge) and merging (vertical merge)
- Column statistics (sum, average, min, max)
- Group by and aggregation support
- Row/column manipulation (add, remove, filter)
- Delimiter auto-detection
- Complete validation functions
- 18 comprehensive usage examples
- 50+ test cases covering all functionality
- Production-ready for data processing tasks

Run tests:
```bash
cd Go/csv_utils
go test -v
```

Run example:
```bash
cd Go/examples
go run csv_utils_example.go
```

Usage example:
```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/csv_utils"
)

func main() {
    // Read CSV file
    data, err := csv_utils.ReadFile("data.csv")
    if err != nil {
        log.Fatal(err)
    }

    // Access data with type conversion
    for _, row := range data.Rows {
        name := row.Get("name")
        age := row.GetInt("age", 0)
        salary := row.GetFloat("salary", 0.0)
        active := row.GetBool("active", false)
        fmt.Printf("%s: %d years old, $%.2f, active=%v\n", name, age, salary, active)
    }

    // Filter rows
    adults := data.FilterRows(func(row csv_utils.CsvRow) bool {
        return row.GetInt("age", 0) >= 18
    })

    // Sort by column
    sorted := data.SortByWithOptions("salary", true, true)

    // Get statistics
    avgSalary := data.AvgColumn("salary")
    totalSalary := data.SumColumn("salary")

    // Write CSV
    writer := csv_utils.NewWriter()
    writer.SetHeaders([]string{"name", "age"})
    writer.AddRow([]string{"Alice", "30"})
    writer.AddRow([]string{"Bob", "25"})
    err = writer.SaveToFile("output.csv")

    // Custom delimiter (TSV)
    opts := csv_utils.DefaultOptions()
    opts.Delimiter = '\t'
    tsvData, _ := csv_utils.ReadFileWithOptions("data.tsv", opts)
}
```

---

### Kotlin - JSON Utilities

Location: `Kotlin/json_utils/mod.kt`

Functions:

**Parsing:**
- **parse**: `JsonUtils.parse(json)` - Parse JSON string into JsonValue
- **parseOrNull**: `JsonUtils.parseOrNull(json)` - Parse safely, return null on error
- **isValid**: `JsonUtils.isValid(json)` - Check if string is valid JSON

**JSON Value Types:**
- **JsonNull**: Represents JSON null value
- **JsonBoolean**: Represents JSON boolean (true/false)
- **JsonNumber**: Represents JSON number (Int, Long, Float, Double)
- **JsonString**: Represents JSON string
- **JsonArray**: Represents JSON array with indexed access
- **JsonObject**: Represents JSON object with key-value access

**Type Checking:**
- **isNull**: Check if value is null
- **isBoolean**: Check if value is boolean
- **isNumber**: Check if value is number
- **isString**: Check if value is string
- **isArray**: Check if value is array
- **isObject**: Check if value is object

**Type Conversion:**
- **asBoolean**: Get value as boolean with default
- **asInt**: Get value as int with default
- **asLong**: Get value as long with default
- **asDouble**: Get value as double with default
- **asString**: Get value as string with default
- **asArray**: Get value as JsonArray
- **asObject**: Get value as JsonObject

**Object Access:**
- **get(key)**: Get property by key, returns JsonNull if not found
- **has(key)**: Check if object has key
- **getString**: Get string property with default
- **getInt**: Get int property with default
- **getDouble**: Get double property with default
- **getBoolean**: Get boolean property with default
- **getObject**: Get nested object
- **getArray**: Get nested array
- **keys**: Get all keys
- **values**: Get all values
- **entries**: Get all key-value entries

**Array Access:**
- **get(index)**: Get element at index, returns JsonNull if out of bounds
- **getString**: Get string element with default
- **getInt**: Get int element with default
- **getDouble**: Get double element with default
- **getBoolean**: Get boolean element with default
- **getObject**: Get nested object element
- **getArray**: Get nested array element

**Generation:**
- **obj**: `JsonUtils.obj("key" to value, ...)` - Create JsonObject from pairs
- **arr**: `JsonUtils.arr(value1, value2, ...)` - Create JsonArray from values
- **toJsonValue**: Convert any Kotlin value to JsonValue
- **toJson**: Convert Kotlin Map/List to JSON string

**Formatting:**
- **toJsonString**: Convert JsonValue to compact JSON string
- **toPrettyString**: Convert JsonValue to pretty-printed JSON
- **prettyPrint**: Pretty print existing JSON string
- **minify**: Minify existing JSON string

**Utilities:**
- **merge**: Merge two JsonObjects
- **plus operator**: Combine two JsonObjects
- **size**: Get size of array or object

**Features:**
- Zero dependencies, uses only Kotlin standard library
- Complete JSON support: null, boolean, number, string, array, object
- Type-safe access with default values
- Full Unicode and escape sequence support
- Pretty printing with customizable indentation
- Round-trip parsing (parse → generate → parse)
- Safe parsing with null return on error
- Kotlin idiomatic API with operator overloading
- Complete test suite with 30 test cases
- 15 comprehensive usage examples
- Production-ready for JSON processing tasks

Compile and run tests:
```bash
cd Kotlin/json_utils
kotlinc -include-runtime -d test.jar *.kt && java -jar test.jar
```

Compile and run example:
```bash
cd Kotlin/examples
kotlinc -cp ../json_utils json_utils_example.kt && kotlin -cp ../json_utils:. JsonUtilsExampleKt
```

Usage example:
```kotlin
import json_utils.*

// Parse JSON
val json = """{"name": "John", "age": 30, "active": true}"""
val obj = JsonUtils.parse(json).asObject()

// Access values
val name = obj.getString("name")        // "John"
val age = obj.getInt("age")             // 30
val active = obj.getBoolean("active")   // true

// Access with defaults
val missing = obj.getString("missing", "default")  // "default"

// Parse arrays
val arr = JsonUtils.parse("[1, 2, 3]").asArray()
val first = arr.getInt(0)               // 1

// Create JSON programmatically
val newObj = JsonUtils.obj(
    "product" to "Laptop",
    "price" to 999.99,
    "tags" to JsonUtils.arr("electronics", "computers")
)
println(newObj.toJsonString())
// {"product":"Laptop","price":999.99,"tags":["electronics","computers"]}

// Pretty print
val pretty = JsonUtils.prettyPrint("""{"a":1,"b":2}""")

// Validate JSON
val isValid = JsonUtils.isValid("{}"))  // true

// Safe parsing
val result = JsonUtils.parseOrNull("invalid")  // null
```

---

### Python - Base64 Utilities

Location: `Python/base64_utils/mod.py`

Functions:

**Encoding:**
- **encode**: `encode(input_data, encoding='utf-8')` - Encode string or bytes to Base64
- **encode_urlsafe**: `encode_urlsafe(input_data, encoding='utf-8', padding=True)` - Encode to URL-safe Base64 (RFC 4648)

**Decoding:**
- **decode**: `decode(base64_string, encoding='utf-8')` - Decode Base64 to string
- **decode_to_bytes**: `decode_to_bytes(base64_string)` - Decode Base64 to bytes
- **decode_urlsafe**: `decode_urlsafe(base64_url_string, encoding='utf-8')` - Decode URL-safe Base64 to string
- **decode_urlsafe_to_bytes**: `decode_urlsafe_to_bytes(base64_url_string)` - Decode URL-safe Base64 to bytes

**URL-safe Conversion:**
- **to_urlsafe**: `to_urlsafe(standard_base64, padding=True)` - Convert standard Base64 to URL-safe format
- **from_urlsafe**: `from_urlsafe(base64_url_string)` - Convert URL-safe Base64 to standard format

**Validation:**
- **is_valid**: `is_valid(base64_string, urlsafe=False)` - Check if string is valid Base64

**Length Calculations:**
- **encoded_length**: `encoded_length(input_length, padding=True)` - Calculate encoded length
- **decoded_max_length**: `decoded_max_length(base64_length)` - Calculate max decoded length

**Features:**
- Zero dependencies, uses only Python standard library (base64, re)
- Supports standard Base64 and URL-safe Base64 (RFC 4648)
- Optional padding control for URL-safe encoding
- Binary data support via bytes type
- Full UTF-8 support including Unicode characters
- Type hints for better IDE support
- Complete input validation with descriptive error messages
- Thread-safe (all methods are static)
- Convenience functions for direct import
- Complete test suite with 22 test cases
- 9 comprehensive usage examples
- Production-ready for data encoding/decoding tasks

Run tests:
```bash
cd Python/base64_utils
python base64_utils_test.py
```

Run example:
```bash
cd Python/examples
python base64_utils_example.py
```

Usage example:
```python
from base64_utils.mod import Base64Utils

# Basic encoding
encoded = Base64Utils.encode("Hello, World!")
# Returns: "SGVsbG8sIFdvcmxkIQ=="

# Basic decoding
decoded = Base64Utils.decode("SGVsbG8sIFdvcmxkIQ==")
# Returns: "Hello, World!"

# URL-safe encoding (for URLs/filenames)
url_safe = Base64Utils.encode_urlsafe("user+name/file", padding=False)
# Returns: "dXNlcituYW1lL2ZpbGU"

# Binary data encoding
binary_data = bytes([0x00, 0x01, 0x02, 0xFF])
encoded = Base64Utils.encode(binary_data)
# Returns: "AAEC/w=="

# Validation
is_valid = Base64Utils.is_valid("SGVsbG8=")  # True
is_invalid = Base64Utils.is_valid("Invalid!")  # False

# Length calculation
length = Base64Utils.encoded_length(100)  # 136

# Convenience functions
from base64_utils.mod import encode, decode
encoded = encode("Hello")
decoded = decode(encoded)
```

---

### C++ - Base64 Utilities

Location: `C++/base64_utils/mod.hpp`

Functions:

**Encoding:**
- **encode**: `encode(input, urlSafe?, padding?)` - Encode string to Base64
- **encode (binary)**: `encode(data, length, urlSafe?, padding?)` - Encode raw bytes to Base64
- **encode (vector)**: `encode(vector<uint8_t>, urlSafe?, padding?)` - Encode byte vector to Base64

**Decoding:**
- **decode**: `decode(input, urlSafe?)` - Decode Base64 to string
- **decodeToBytes**: `decodeToBytes(input, urlSafe?)` - Decode Base64 to binary data

**URL-safe Conversion:**
- **toUrlSafe**: `toUrlSafe(base64, padding?)` - Convert standard Base64 to URL-safe format
- **fromUrlSafe**: `fromUrlSafe(base64Url)` - Convert URL-safe Base64 to standard format

**Validation:**
- **isValid**: `isValid(input, urlSafe?)` - Check if string is valid Base64

**Length Calculations:**
- **encodedLength**: `encodedLength(inputLength, padding?)` - Calculate encoded length
- **decodedMaxLength**: `decodedMaxLength(base64Length)` - Calculate max decoded length

**Features:**
- Zero dependencies, header-only library (C++11+)
- Supports standard Base64 and URL-safe Base64 (RFC 4648)
- Optional padding control
- Binary data support via std::vector<uint8_t>
- Raw pointer interface for C-style arrays
- Complete input validation with descriptive error messages
- Thread-safe (all methods are static and stateless)
- Header-only design - just include and use
- Complete test suite with 29 test cases
- 10 comprehensive usage examples
- Production-ready for data encoding/decoding tasks

Compile and run tests:
```bash
cd C++/base64_utils
g++ -std=c++11 -o base64_utils_test base64_utils_test.cpp && ./base64_utils_test
```

Compile and run example:
```bash
cd C++/examples
g++ -std=c++11 -o base64_utils_example base64_utils_example.cpp && ./base64_utils_example
```

Usage example:
```cpp
#include "base64_utils/mod.hpp"
using namespace alltoolkit;

// Basic encoding
std::string encoded = Base64Utils::encode("Hello, World!");
// Returns: "SGVsbG8sIFdvcmxkIQ=="

// Basic decoding
std::string decoded = Base64Utils::decode("SGVsbG8sIFdvcmxkIQ==");
// Returns: "Hello, World!"

// URL-safe encoding (for URLs/filenames)
std::string urlSafe = Base64Utils::encode("user+name/file", true, false);
// Returns: "dXNlcituYW1lL2ZpbGU"

// Binary data encoding
std::vector<uint8_t> data = {0x00, 0x01, 0x02, 0xFF};
std::string binaryEncoded = Base64Utils::encode(data);
// Returns: "AAEC/w=="

// Validation
bool valid = Base64Utils::isValid("SGVsbG8=");  // true
bool invalid = Base64Utils::isValid("Invalid!"); // false

// Length calculation
size_t len = Base64Utils::encodedLength(100, true);  // 136
```

---

### Ruby - Regex Utilities

Location: `Ruby/regex_utils/mod.rb`

Functions:

**Pattern Matching:**
- **match?**: `match?(str, pattern)` - Check if string matches pattern (preset symbol or Regexp)
- **no_match?**: `no_match?(str, pattern)` - Check if string does not match pattern
- **find**: `find(str, pattern)` - Find first match, returns MatchResult object
- **find_all**: `find_all(str, pattern)` - Find all matches, returns array of strings
- **find_all_with_groups**: `find_all_with_groups(str, pattern)` - Find all matches with capture groups

**String Manipulation:**
- **replace_first**: `replace_first(str, pattern, replacement)` - Replace first occurrence (supports Proc)
- **replace_all**: `replace_all(str, pattern, replacement)` - Replace all occurrences (supports Proc)
- **remove**: `remove(str, pattern)` - Remove all matches
- **remove_first**: `remove_first(str, pattern)` - Remove first match
- **split**: `split(str, pattern)` - Split string by pattern

**Extraction:**
- **extract**: `extract(str, pattern, group)` - Extract specific capture group by index or name
- **contains?**: `contains?(str, pattern)` - Check if string contains pattern
- **count**: `count(str, pattern)` - Count number of matches

**Utility:**
- **escape**: `escape(str)` - Escape special regex characters
- **build**: `build(pattern, options)` - Build regex from string with options
- **valid?**: `valid?(str, preset)` - Validate using preset pattern
- **presets**: `presets` - Get list of available preset names
- **get_preset**: `get_preset(name)` - Get pattern by preset name
- **preset_exists?**: `preset_exists?(name)` - Check if preset exists

**Preset Patterns:**
- `:email` - Email validation (RFC 5322 compliant)
- `:url` - HTTP/HTTPS URL validation
- `:ipv4` - IPv4 address validation
- `:ipv6` - IPv6 address validation
- `:phone` - Phone number validation
- `:credit_card` - Credit card format validation
- `:hex_color` - Hex color (#RGB or #RRGGBB)
- `:date_iso` - ISO date format (YYYY-MM-DD)
- `:date_us` - US date format (MM/DD/YYYY)
- `:date_uk` - UK date format (DD/MM/YYYY)
- `:time` - Time format (HH:MM:SS)
- `:uuid` - UUID v4 validation
- `:uuid_compact` - Compact UUID validation
- `:alphanumeric` - Alphanumeric only
- `:alpha` - Alphabetic only
- `:numeric` - Numeric only
- `:decimal` - Decimal number
- `:whitespace` - Whitespace only
- `:html_tag` - HTML tag pattern
- `:markdown_link` - Markdown link pattern
- `:file_extension` - File extension pattern
- `:twitter_handle` - Twitter handle validation
- `:hashtag` - Hashtag pattern
- `:mac_address` - MAC address validation
- `:zip_code` - US ZIP code validation
- `:ssn` - US SSN validation

**MatchResult Class:**
- `success?` - Check if match was successful
- `matches` - Array of all captures
- `named_groups` - Hash of named capture groups
- `first` / `last` - Access first/last match
- `[]` - Array-style access to captures
- `to_a` / `to_s` - Convert to array or string

Features:
- Zero dependencies, uses only Ruby standard library
- 25+ built-in validation patterns
- Support for custom Regexp patterns
- Named capture groups support
- Proc-based replacements
- Nil-safe operations
- Complete test suite with 60+ test cases
- 20 comprehensive usage examples
- Production-ready for Ruby 2.5+

Run tests:
```bash
cd Ruby/regex_utils
ruby regex_utils_test.rb
```

Run example:
```bash
cd Ruby/examples
ruby regex_utils_example.rb
```

Usage example:
```ruby
require_relative 'regex_utils/mod'

# Validation with presets
RegexUtils.match?("test@example.com", :email)  # => true
RegexUtils.match?("192.168.1.1", :ipv4)        # => true
RegexUtils.valid?("#ffffff", :hex_color)       # => true

# Find matches
result = RegexUtils.find("hello world", /\w+/)
result.success?   # => true
result.first      # => "hello"

# Find all matches
RegexUtils.find_all("a1b2c3", /\d/)  # => ["1", "2", "3"]

# Replace with string
RegexUtils.replace_all("a1b2c3", /\d/, "X")  # => "aXbXcX"

# Replace with Proc (block)
RegexUtils.replace_all("abc", /\w/) { |m| m.upcase }  # => "ABC"

# Extract capture groups
result = RegexUtils.find("hello world", /(?<first>\w+) (?<second>\w+)/)
result.named_groups["first"]   # => "hello"
result.named_groups["second"]  # => "world"

# Extract specific group
RegexUtils.extract("File: doc.pdf", /File:\s*(\S+)/, 1)  # => "doc.pdf"

# Count matches
RegexUtils.count("hello world", /l/)  # => 3

# Check if contains
RegexUtils.contains?("user@example.com", :email)  # => true

# Get all presets
RegexUtils.presets  # => [:email, :url, :ipv4, ...]
```

---

### Delphi - String Utilities

Location: `Delphi/string_utils/mod.pas`

Functions:

**Empty/Blank Checks:**
- **IsBlank**: `IsBlank(S)` - Check if string is empty, nil, or whitespace only
- **IsNotBlank**: `IsNotBlank(S)` - Check if string has content
- **IsEmpty**: `IsEmpty(S)` - Check if string is empty

**Whitespace Handling:**
- **TrimString**: `TrimString(S)` - Remove leading and trailing whitespace
- **TrimLeft**: `TrimLeft(S)` - Remove leading whitespace
- **TrimRight**: `TrimRight(S)` - Remove trailing whitespace
- **RemoveWhitespace**: `RemoveWhitespace(S)` - Remove all whitespace
- **NormalizeWhitespace**: `NormalizeWhitespace(S)` - Collapse multiple spaces to single

**Case Conversion:**
- **ToLower**: `ToLower(S)` - Convert to lowercase
- **ToUpper**: `ToUpper(S)` - Convert to uppercase
- **Capitalize**: `Capitalize(S)` - Capitalize first character
- **Uncapitalize**: `Uncapitalize(S)` - Uncapitalize first character
- **ToTitleCase**: `ToTitleCase(S)` - Convert to Title Case
- **SwapCase**: `SwapCase(S)` - Swap uppercase/lowercase

**Substring Operations:**
- **Substring**: `Substring(S, Start, Len)` - Extract substring
- **SubstringFrom**: `SubstringFrom(S, Start)` - Extract from position to end
- **SubstringTo**: `SubstringTo(S, EndPos)` - Extract from start to position
- **SubstringBetween**: `SubstringBetween(S, Open, Close)` - Extract between markers
- **SubstringAfter**: `SubstringAfter(S, Separator)` - Extract after separator
- **SubstringBefore**: `SubstringBefore(S, Separator)` - Extract before separator
- **SubstringAfterLast**: `SubstringAfterLast(S, Separator)` - Extract after last separator
- **SubstringBeforeLast**: `SubstringBeforeLast(S, Separator)` - Extract before last separator
- **Truncate**: `Truncate(S, MaxLength, Suffix)` - Truncate with ellipsis

**Prefix/Suffix Operations:**
- **StartsWith**: `StartsWith(S, Prefix, IgnoreCase)` - Check prefix
- **EndsWith**: `EndsWith(S, Suffix, IgnoreCase)` - Check suffix
- **RemovePrefix**: `RemovePrefix(S, Prefix)` - Remove prefix if present
- **RemoveSuffix**: `RemoveSuffix(S, Suffix)` - Remove suffix if present

**Find and Count:**
- **CountMatches**: `CountMatches(S, Sub, IgnoreCase)` - Count substring occurrences
- **Contains**: `Contains(S, Sub, IgnoreCase)` - Check if contains substring
- **IndexOf**: `IndexOf(S, Sub, StartPos)` - Find first index
- **LastIndexOf**: `LastIndexOf(S, Sub)` - Find last index

**Replacement:**
- **ReplaceAll**: `ReplaceAll(S, OldSub, NewSub, IgnoreCase)` - Replace all occurrences
- **ReplaceFirst**: `ReplaceFirst(S, OldSub, NewSub)` - Replace first occurrence
- **ReplaceLast**: `ReplaceLast(S, OldSub, NewSub)` - Replace last occurrence

**Padding:**
- **PadLeft**: `PadLeft(S, TotalWidth, PadChar)` - Pad on left
- **PadRight**: `PadRight(S, TotalWidth, PadChar)` - Pad on right
- **Center**: `Center(S, TotalWidth, PadChar)` - Center with padding

**Reverse and Repeat:**
- **Reverse**: `Reverse(S)` - Reverse string
- **RepeatString**: `RepeatString(S, Count)` - Repeat string

**Split and Join:**
- **Split**: `Split(S, Delimiter, Limit)` - Split to TStringList
- **SplitLines**: `SplitLines(S)` - Split by newlines
- **Join**: `Join(Strings, Delimiter)` - Join TStringList

**Naming Conventions:**
- **ToCamelCase**: `ToCamelCase(S)` - Convert to camelCase
- **ToPascalCase**: `ToPascalCase(S)` - Convert to PascalCase
- **ToSnakeCase**: `ToSnakeCase(S)` - Convert to snake_case
- **ToKebabCase**: `ToKebabCase(S)` - Convert to kebab-case

**Validation:**
- **IsValidEmail**: `IsValidEmail(S)` - Validate email format
- **IsValidUrl**: `IsValidUrl(S)` - Validate URL format
- **IsNumeric**: `IsNumeric(S)` - Check if numeric
- **IsInteger**: `IsInteger(S)` - Check if integer
- **IsAlpha**: `IsAlpha(S)` - Check if alphabetic
- **IsAlphanumeric**: `IsAlphanumeric(S)` - Check if alphanumeric

**Random Generation:**
- **RandomString**: `RandomString(Length, Chars)` - Generate random string
- **RandomAlphanumeric**: `RandomAlphanumeric(Length)` - Generate alphanumeric
- **RandomNumeric**: `RandomNumeric(Length)` - Generate numeric
- **RandomPassword**: `RandomPassword(Length)` - Generate secure password

**Encoding/Decoding:**
- **Base64Encode**: `Base64Encode(S)` - Base64 encode
- **Base64Decode**: `Base64Decode(S)` - Base64 decode
- **UrlEncode**: `UrlEncode(S)` - URL encode
- **UrlDecode**: `UrlDecode(S)` - URL decode
- **HtmlEscape**: `HtmlEscape(S)` - Escape HTML entities
- **HtmlUnescape**: `HtmlUnescape(S)` - Unescape HTML entities

**Utilities:**
- **DefaultIfBlank**: `DefaultIfBlank(S, DefaultValue)` - Return default if blank
- **DefaultIfEmpty**: `DefaultIfEmpty(S, DefaultValue)` - Return default if empty
- **Slugify**: `Slugify(S, Separator)` - Create URL-friendly slug
- **StripHtml**: `StripHtml(S)` - Remove HTML tags

Features:
- Zero dependencies, uses only Delphi standard library (SysUtils, Classes)
- Compatible with Delphi 7+ and Free Pascal
- Complete test suite with 60+ test cases
- 12 comprehensive usage examples
- Full Unicode support
- Production-ready for Delphi applications

Compile and run tests:
```bash
cd Delphi/string_utils
fpc string_utils_test.pas && ./string_utils_test
```

Compile and run example:
```bash
cd Delphi/examples
fpc string_utils_example.pas && ./string_utils_example
```

Usage example:
```pascal
uses mod;

// Check blank
if IsBlank(UserInput) then
  ShowMessage('Input is required');

// Case conversion
Title := ToTitleCase('hello world');  // 'Hello World'

// Substring operations
Filename := SubstringAfterLast('/path/to/file.txt', '/');  // 'file.txt'

// Validation
if IsValidEmail(Email) then
  // Process email

// Naming conventions
CamelCase := ToCamelCase('hello-world');  // 'helloWorld'
SnakeCase := ToSnakeCase('HelloWorld');   // 'hello_world'

// Random generation
Password := RandomPassword(16);
Token := RandomAlphanumeric(32);

// Padding
Padded := PadLeft('5', 3, '0');  // '005'

// Encoding
Encoded := Base64Encode('Hello, World!');
UrlSafe := UrlEncode('hello world!');
```

---

### C - HTTP Client Utilities

Location: `C/http_utils/mod.h`, `C/http_utils/mod.c`

Functions:

**HTTP Methods:**
- **GET**: `http_get(url, options)` - Send HTTP GET request
- **POST**: `http_post(url, body, content_type, options)` - Send HTTP POST request
- **POST JSON**: `http_post_json(url, json_data, options)` - Send JSON POST request
- **POST Form**: `http_post_form(url, form_data, options)` - Send form POST request
- **PUT**: `http_put(url, body, content_type, options)` - Send HTTP PUT request
- **PUT JSON**: `http_put_json(url, json_data, options)` - Send JSON PUT request
- **DELETE**: `http_delete(url, options)` - Send HTTP DELETE request
- **PATCH**: `http_patch(url, body, content_type, options)` - Send HTTP PATCH request
- **HEAD**: `http_head(url, options)` - Send HTTP HEAD request

**URL Utilities:**
- **Parse URL**: `url_parse(url)` - Parse URL into components (scheme, host, port, path, query, fragment, userinfo)
- **Build URL**: `url_build(components)` - Build URL from components
- **URL Encode**: `url_encode(str)` - URL encode a string (spaces → +, special chars → %XX)
- **URL Decode**: `url_decode(str)` - URL decode a string
- **Build Query**: `url_build_query_string(keys, values, count)` - Build query string from key-value pairs
- **Add Params**: `url_add_params(base_url, keys, values, count)` - Add query parameters to URL
- **Validate URL**: `url_is_valid(url)` - Check if string is valid URL
- **Get Domain**: `url_get_domain(url)` - Extract domain from URL
- **Get Path**: `url_get_path(url)` - Extract path from URL

**HTTP Headers:**
- **Create Headers**: `http_headers_new()` - Create new headers collection
- **Add Header**: `http_headers_add(headers, key, value)` - Add header to collection
- **Get Header**: `http_headers_get(headers, key)` - Get header value (case-insensitive)
- **Free Headers**: `http_headers_free(headers)` - Free headers collection

**Request Options:**
- **Create Options**: `http_options_new()` - Create default request options
- **Free Options**: `http_options_free(options)` - Free request options
- Options include: custom headers, timeout, redirect handling, SSL verification, proxy, authentication

**HTTP Response:**
- **Free Response**: `http_response_free(response)` - Free HTTP response
- **Get Header**: `http_response_get_header(response, key)` - Get response header
- **Is JSON**: `http_response_is_json(response)` - Check if response body is JSON
- Response fields: status_code, status_text, headers, body, body_length, response_time, url, success

**Utility Functions:**
- **Version**: `http_utils_version()` - Get library version
- **Status Text**: `http_status_text(status_code)` - Get HTTP status text

Features:
- Zero dependencies for URL utilities (standard C library only)
- HTTP requests require libcurl (standard on most systems)
- Full HTTP method support: GET, POST, PUT, DELETE, PATCH, HEAD
- Automatic JSON and form data encoding
- Custom headers and timeout configuration
- Response time tracking
- SSL/TLS certificate verification control
- HTTP proxy support
- Basic authentication support
- URL parsing and building
- Query string manipulation
- Complete test suite with 30+ test cases
- 11 comprehensive usage examples
- Production-ready for REST API clients

Compile and run tests:
```bash
cd C/http_utils
gcc -o http_test mod.c http_utils_test.c -lcurl && ./http_test
```

Compile and run example:
```bash
cd C/examples
gcc -o http_example ../http_utils/mod.c http_utils_example.c -lcurl && ./http_example
```

Usage example:
```c
#include "http_utils/mod.h"
#include <stdio.h>

int main(void) {
    // Simple GET request
    HttpResponse *response = http_get("https://api.example.com/users", NULL);
    if (response->success) {
        printf("Response: %s\n", response->body);
    }
    http_response_free(response);
    
    // POST JSON data
    const char *json = "{\"name\":\"John\",\"age\":30}";
    response = http_post_json("https://api.example.com/users", json, NULL);
    printf("Status: %d %s\n", response->status_code, response->status_text);
    http_response_free(response);
    
    // Custom headers
    HttpRequestOptions *options = http_options_new();
    options->headers = http_headers_new();
    http_headers_add(options->headers, "Authorization", "Bearer token123");
    response = http_get("https://api.example.com/protected", options);
    http_response_free(response);
    http_options_free(options);
    
    // URL manipulation
    UrlComponents *comp = url_parse("https://api.example.com:8080/v1/users?page=1");
    printf("Host: %s, Port: %d\n", comp->host, comp->port);
    url_components_free(comp);
    
    // URL encoding
    char *encoded = url_encode("hello world!");
    printf("Encoded: %s\n", encoded);  // "hello+world%21"
    free(encoded);
    
    // Build query string
    const char *keys[] = {"q", "page"};
    const char *values[] = {"hello world", "1"};
    char *query = url_build_query_string(keys, values, 2);
    printf("Query: %s\n", query);  // "q=hello+world&page=1"
    free(query);
    
    return 0;
}
```

---

### JavaScript - String Utilities

Location: `JavaScript/string_utils/mod.js`

Functions:

**Empty/Blank Checks:**
- **isBlank**: `isBlank(str)` - Check if string is null, undefined, empty, or whitespace only
- **isNotBlank**: `isNotBlank(str)` - Check if string has content
- **isEmpty**: `isEmpty(str)` - Check if string is empty (length === 0)

**Trimming and Whitespace:**
- **trim**: `trim(str)` - Remove leading and trailing whitespace
- **trimLeft**: `trimLeft(str)` - Remove leading whitespace
- **trimRight**: `trimRight(str)` - Remove trailing whitespace
- **removeWhitespace**: `removeWhitespace(str)` - Remove all whitespace from string
- **normalizeWhitespace**: `normalizeWhitespace(str)` - Replace multiple spaces with single space

**Case Conversion:**
- **toLowerCase**: `toLowerCase(str)` - Convert to lowercase
- **toUpperCase**: `toUpperCase(str)` - Convert to uppercase
- **capitalize**: `capitalize(str)` - Capitalize first character
- **uncapitalize**: `uncapitalize(str)` - Uncapitalize first character
- **toTitleCase**: `toTitleCase(str)` - Convert to Title Case
- **swapCase**: `swapCase(str)` - Swap uppercase/lowercase

**Substring Operations:**
- **truncate**: `truncate(str, maxLength, suffix?)` - Truncate string with ellipsis
- **substringBetween**: `substringBetween(str, open, close)` - Extract substring between markers
- **substringAfter**: `substringAfter(str, separator)` - Extract substring after separator
- **substringBefore**: `substringBefore(str, separator)` - Extract substring before separator
- **substringAfterLast**: `substringAfterLast(str, separator)` - Extract substring after last separator
- **substringBeforeLast**: `substringBeforeLast(str, separator)` - Extract substring before last separator

**Prefix/Suffix Operations:**
- **startsWith**: `startsWith(str, prefix, ignoreCase?)` - Check if string starts with prefix
- **endsWith**: `endsWith(str, suffix, ignoreCase?)` - Check if string ends with suffix
- **removePrefix**: `removePrefix(str, prefix)` - Remove prefix if present
- **removeSuffix**: `removeSuffix(str, suffix)` - Remove suffix if present

**Counting and Searching:**
- **countMatches**: `countMatches(str, sub)` - Count occurrences of substring
- **contains**: `contains(str, search, ignoreCase?)` - Check if string contains substring
- **indexOf**: `indexOf(str, search, fromIndex?)` - Find index of substring
- **lastIndexOf**: `lastIndexOf(str, search, fromIndex?)` - Find last index of substring

**Replacement:**
- **replaceAll**: `replaceAll(str, search, replacement)` - Replace all occurrences
- **replaceFirst**: `replaceFirst(str, search, replacement)` - Replace first occurrence
- **replaceLast**: `replaceLast(str, search, replacement)` - Replace last occurrence

**Padding:**
- **padLeft**: `padLeft(str, length, padChar?)` - Pad string on left
- **padRight**: `padRight(str, length, padChar?)` - Pad string on right
- **center**: `center(str, length, padChar?)` - Center string with padding

**Reversal and Repetition:**
- **reverse**: `reverse(str)` - Reverse string
- **repeat**: `repeat(str, count)` - Repeat string count times

**Splitting and Joining:**
- **split**: `split(str, separator?, limit?)` - Split string into array
- **lines**: `lines(str, trimEmpty?)` - Split string by newlines
- **join**: `join(array, separator?)` - Join array elements

**Validation:**
- **isValidEmail**: `isValidEmail(str)` - Validate email format
- **isValidUrl**: `isValidUrl(str)` - Validate URL format
- **isValidIPv4**: `isValidIPv4(str)` - Validate IPv4 address
- **isNumeric**: `isNumeric(str)` - Check if string is numeric
- **isInteger**: `isInteger(str)` - Check if string is integer
- **isAlpha**: `isAlpha(str)` - Check if string is alphabetic
- **isAlphanumeric**: `isAlphanumeric(str)` - Check if string is alphanumeric

**Naming Conventions:**
- **toCamelCase**: `toCamelCase(str)` - Convert to camelCase
- **toPascalCase**: `toPascalCase(str)` - Convert to PascalCase
- **toSnakeCase**: `toSnakeCase(str)` - Convert to snake_case
- **toKebabCase**: `toKebabCase(str)` - Convert to kebab-case

**Random Generation:**
- **random**: `random(length?, chars?)` - Generate random string
- **randomAlphanumeric**: `randomAlphanumeric(length?)` - Generate alphanumeric string
- **randomNumeric**: `randomNumeric(length?)` - Generate numeric string
- **randomAlphabetic**: `randomAlphabetic(length?)` - Generate alphabetic string
- **randomPassword**: `randomPassword(length?)` - Generate secure password

**URL Encoding:**
- **urlEncode**: `urlEncode(str)` - URL encode string
- **urlDecode**: `urlDecode(str)` - URL decode string

**HTML Operations:**
- **slugify**: `slugify(str, separator?)` - Create URL-friendly slug
- **stripHtml**: `stripHtml(str)` - Remove HTML tags
- **escapeHtml**: `escapeHtml(str)` - Escape HTML entities
- **unescapeHtml**: `unescapeHtml(str)` - Unescape HTML entities

**Comparison:**
- **equals**: `equals(str1, str2, ignoreCase?)` - Compare strings
- **compare**: `compare(str1, str2, ignoreCase?)` - Compare strings (returns -1, 0, 1)

**Default Values:**
- **defaultString**: `defaultString(str, defaultStr?)` - Return default if blank
- **defaultIfEmpty**: `defaultIfEmpty(str, defaultStr?)` - Return default if empty

Features:
- Zero dependencies, uses only JavaScript standard library
- Works in both Node.js and browser environments
- Null/undefined safe - all functions handle null/undefined gracefully
- Complete test suite with 82 test cases
- 20 comprehensive usage examples
- Production-ready for web applications

Run tests:
```bash
cd JavaScript/string_utils
node string_utils_test.js
```

Run example:
```bash
cd JavaScript/examples
node string_utils_example.js
```

Usage example:
```javascript
const StringUtils = require('./string_utils/mod.js');

// Empty check
if (StringUtils.isBlank(userInput)) {
    console.log('Input is required');
}

// Case conversion
const title = StringUtils.toTitleCase('hello world'); // 'Hello World'

// Substring operations
const filename = StringUtils.substringAfterLast('/path/to/file.txt', '/'); // 'file.txt'

// Validation
if (StringUtils.isValidEmail(email)) {
    // Process email
}

// Naming conventions
const camelCase = StringUtils.toCamelCase('hello-world'); // 'helloWorld'
const snake_case = StringUtils.toSnakeCase('helloWorld'); // 'hello_world'

// Random generation
const password = StringUtils.randomPassword(16);
const token = StringUtils.randomAlphanumeric(32);

// Padding
const padded = StringUtils.padLeft('5', 3, '0'); // '005'
```

---

### PHP - HTTP Utilities

Location: `PHP/http_utils/mod.php`

Functions:

**HTTP Methods:**
- **GET**: `HttpUtils::get(url, options)` - Send HTTP GET request
- **POST**: `HttpUtils::post(url, body, options)` - Send HTTP POST request
- **POST JSON**: `HttpUtils::postJson(url, data, options)` - Send JSON POST request
- **POST Form**: `HttpUtils::postForm(url, data, options)` - Send form POST request
- **PUT**: `HttpUtils::put(url, body, options)` - Send HTTP PUT request
- **PUT JSON**: `HttpUtils::putJson(url, data, options)` - Send JSON PUT request
- **DELETE**: `HttpUtils::delete(url, options)` - Send HTTP DELETE request
- **PATCH**: `HttpUtils::patch(url, body, options)` - Send HTTP PATCH request
- **HEAD**: `HttpUtils::head(url, options)` - Send HTTP HEAD request

**URL Utilities:**
- **Build URL**: `HttpUtils::buildUrl(baseUrl, params)` - Build URL with query parameters
- **Build Query String**: `HttpUtils::buildQueryString(params)` - Build URL-encoded query string
- **URL Encode**: `HttpUtils::urlEncode(value)` - URL encode a string
- **URL Decode**: `HttpUtils::urlDecode(value)` - URL decode a string
- **Parse URL**: `HttpUtils::parseUrl(url)` - Parse URL into components (scheme, host, port, path, query, fragment, user, pass)
- **Parse Query String**: `HttpUtils::parseQueryString(queryString)` - Parse query string to array
- **Validate URL**: `HttpUtils::isValidUrl(url)` - Check if string is valid URL
- **Get Domain**: `HttpUtils::getDomain(url)` - Extract domain from URL
- **Get Path**: `HttpUtils::getPath(url)` - Extract path from URL
- **Add Query Params**: `HttpUtils::addQueryParams(url, params)` - Add query parameters to URL
- **Remove Query Params**: `HttpUtils::removeQueryParams(url, keys)` - Remove query parameters from URL

**HTTP Response (HttpResponse class):**
- **Status Code**: `$response->statusCode` - HTTP status code
- **Status Text**: `$response->statusText` - HTTP status text
- **Headers**: `$response->headers` - Response headers array
- **Body**: `$response->body` - Response body string
- **Success**: `$response->success` - True if status 200-299
- **Response Time**: `$response->responseTime` - Request duration in seconds
- **JSON Parse**: `$response->json()` - Parse body as JSON
- **Is JSON**: `$response->isJson()` - Check if body is valid JSON

**HTTP Options (HttpOptions class):**
- **Headers**: Custom request headers
- **Timeout**: Request timeout in seconds (default: 30)
- **Follow Redirects**: Auto-follow redirects (default: true)
- **Max Redirects**: Maximum redirect hops (default: 10)
- **Verify SSL**: SSL certificate verification (default: true)
- **Proxy**: HTTP proxy address
- **Authentication**: Username/password for basic auth

Features:
- Zero dependencies, uses only PHP standard library (ext-curl)
- Full HTTP method support: GET, POST, PUT, DELETE, PATCH, HEAD
- Automatic JSON encoding/decoding
- Form data encoding support
- Complete URL manipulation utilities
- Custom headers and timeout configuration
- Response time tracking
- SSL/TLS certificate verification control
- HTTP proxy support
- Basic authentication support
- Response success status checking
- Built-in JSON validation
- Complete test suite with 20+ test cases
- 12 comprehensive usage examples
- Production-ready for REST API clients

Run tests:
```bash
cd PHP/http_utils
php http_utils_test.php
```

Run example:
```bash
cd PHP/examples
php http_utils_example.php
```

Usage example:
```php
require_once 'PHP/http_utils/mod.php';
use AllToolkit\HttpUtils;

// GET request
$response = HttpUtils::get('https://api.example.com/users');
if ($response->success) {
    $data = $response->json();
    print_r($data);
}

// POST JSON
$response = HttpUtils::postJson('https://api.example.com/users', [
    'name' => 'John',
    'email' => 'john@example.com'
]);

// POST Form
$response = HttpUtils::postForm('https://api.example.com/login', [
    'username' => 'admin',
    'password' => 'secret'
]);

// URL building
$url = HttpUtils::buildUrl('https://api.example.com/search', [
    'q' => 'hello world',
    'page' => 1
]);
// Result: 'https://api.example.com/search?q=hello+world&page=1'

// URL parsing
$parts = HttpUtils::parseUrl('https://user:pass@api.example.com:8080/v1/users');
// $parts['scheme'] = 'https'
// $parts['host'] = 'api.example.com'
// $parts['port'] = 8080

// Custom options
$options = new \AllToolkit\HttpOptions();
$options->headers = ['Authorization' => 'Bearer token123'];
$options->timeout = 60;
$response = HttpUtils::get('https://api.example.com/protected', $options);
```

---

### SQL - Date/Time Utilities

Location: `SQL/date_utils/mod.sql`

Functions:

**Date Formatting:**
- **ISO Format**: `DATE_FORMAT(date, '%Y-%m-%d')` (MySQL) / `TO_CHAR(date, 'YYYY-MM-DD')` (PostgreSQL) / `CONVERT(VARCHAR(10), date, 23)` (SQL Server) / `strftime('%Y-%m-%d', date)` (SQLite) - Format date to ISO 8601 standard
- **UK Format**: DD/MM/YYYY format for UK locale
- **US Format**: MM/DD/YYYY format for US locale
- **Chinese Format**: YYYY年MM月DD日 format for Chinese locale
- **Custom Format**: Support for various date format patterns per database

**Date Parsing:**
- **Parse Date**: Convert string to date with format specification
- **ISO Parse**: Parse ISO 8601 formatted dates
- **UK/US Parse**: Parse locale-specific date formats

**Date Arithmetic:**
- **Add Days**: Add/subtract days from a date
- **Add Months**: Add/subtract months from a date
- **Add Years**: Add/subtract years from a date
- **First Day of Month**: Get the first day of any month
- **Last Day of Month**: Get the last day of any month
- **First Day of Year**: Get January 1st of any year
- **Last Day of Year**: Get December 31st of any year

**Date Differences:**
- **Days Between**: Calculate days between two dates
- **Months Between**: Calculate months between two dates
- **Years Between**: Calculate years between two dates
- **Age Calculation**: Calculate age from birth date

**Date Extraction:**
- **Extract Year**: Get year component from date
- **Extract Month**: Get month component from date
- **Extract Day**: Get day component from date
- **Extract Day of Week**: Get day of week (1=Sunday to 7=Saturday)
- **Extract Day of Year**: Get day number in year (1-366)
- **Extract Week Number**: Get ISO week number
- **Extract Quarter**: Get quarter (1-4)
- **Extract Hour/Minute/Second**: Get time components

**Date Validation:**
- **Is Valid Date**: Check if a date string is valid
- **Is Leap Year**: Check if a year is a leap year
- **Is Weekend**: Check if date falls on weekend
- **Is Weekday**: Check if date falls on weekday

**Current Date/Time:**
- **Current Date**: Get today's date
- **Current Datetime**: Get current date and time
- **Current Time**: Get current time
- **Unix Timestamp**: Get current Unix timestamp

Features:
- Multi-database support: MySQL, PostgreSQL, SQL Server, SQLite
- Zero dependencies - uses only standard SQL functions
- Portable syntax with database-specific implementations
- 15 practical examples covering common use cases
- Complete format reference for all supported databases
- Test suite with 10+ test cases
- Production-ready for database date operations

Usage example:
```sql
-- MySQL: Format date
SELECT DATE_FORMAT(order_date, '%d/%m/%Y') AS formatted_date FROM orders;

-- PostgreSQL: Calculate age
SELECT EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) AS age FROM users;

-- SQL Server: Add days
SELECT DATEADD(DAY, 7, order_date) AS due_date FROM orders;

-- SQLite: Get week number
SELECT strftime('%W', order_date) AS week_num FROM orders;

-- Cross-database: First day of month
-- MySQL: DATE_FORMAT(date_col, '%Y-%m-01')
-- PostgreSQL: DATE_TRUNC('month', date_col)::DATE
-- SQL Server: DATEFROMPARTS(YEAR(date_col), MONTH(date_col), 1)
-- SQLite: date(date_col, 'start of month')
```

---

### Rust - Compression Utilities

Location: `Rust/compression_utils/mod.rs`

Functions:

**Run-Length Encoding (RLE):**
- **RLE Encode**: `rle_encode(data)` - Compress data using RLE algorithm
- **RLE Decode**: `rle_decode(data)` - Decompress RLE encoded data
- **RLE Result**: Returns `RleResult` with compressed data, original length, and compression ratio

**Delta Encoding:**
- **Delta Encode**: `delta_encode(data)` - Encode data as differences between consecutive values
- **Delta Decode**: `delta_decode(data)` - Restore original values from delta encoding
- Efficient for time-series data with small incremental changes

**Base64 Encoding:**
- **Base64 Encode**: `base64_encode(data)` - Encode binary to Base64 ASCII string
- **Base64 Decode**: `base64_decode(data)` - Decode Base64 back to binary
- **Validate Base64**: `is_valid_base64(data)` - Check if string is valid Base64

**Hex Encoding:**
- **Hex Encode**: `hex_encode(data)` - Encode binary to hexadecimal string
- **Hex Decode**: `hex_decode(data)` - Decode hex string back to binary
- **Validate Hex**: `is_valid_hex(data)` - Check if string is valid hex

**URL Encoding:**
- **URL Encode**: `url_encode(data)` - Percent-encode string for URLs
- **URL Decode**: `url_decode(data)` - Decode percent-encoded URL string
- Preserves unreserved characters (-_.~)

**Burrows-Wheeler Transform:**
- **BWT Transform**: `bwt_transform(data)` - Perform BWT transformation
- **BWT Reverse**: `bwt_reverse(data, index)` - Reverse BWT to restore original data
- Groups similar characters together for better compression

**LZW Compression:**
- **LZW Compress**: `lzw_compress(data)` - Dictionary-based compression
- **LZW Decompress**: `lzw_decompress(data)` - Decompress LZW encoded data
- Classic Lempel-Ziv-Welch algorithm

**Compression Statistics:**
- **Calc Stats**: `calc_stats(original, compressed)` - Calculate compression statistics
- Returns `CompressionStats` with size, ratio, and space saved

Features:
- Zero dependencies, uses only Rust standard library
- Multiple compression algorithms for different data types
- RLE for repetitive data (e.g., log files, simple graphics)
- Delta encoding for time-series data (e.g., sensor readings)
- Base64/Hex for binary-to-text encoding
- BWT for preprocessing before compression
- LZW for general-purpose compression
- Complete test suite with 25+ test cases
- 11 comprehensive usage examples
- Production-ready for data compression pipelines

Compile and run tests:
```bash
cd Rust/compression_utils
rustc --test mod.rs -o compression_test && ./compression_test
```

Compile and run example:
```bash
cd Rust/examples
rustc --edition 2021 -L ../compression_utils compression_utils_example.rs -o compression_example && ./compression_example
```

Usage example:
```rust
// Run-Length Encoding
let compressed = rle_encode(b"AAABBBCCCC");
assert_eq!(compressed.data, vec![3, b'A', 3, b'B', 4, b'C']);
let decompressed = rle_decode(&compressed.data);

// Delta Encoding for time series
let data = vec![10, 12, 15, 15, 20];
let encoded = delta_encode(&data); // [10, 2, 3, 0, 5]
let decoded = delta_decode(&encoded);

// Base64 encoding
let encoded = base64_encode(b"Hello, World!");
// Returns: "SGVsbG8sIFdvcmxkIQ=="
let decoded = base64_decode(&encoded);

// URL encoding
let encoded = url_encode("hello world!");
// Returns: "hello%20world%21"

// Compression statistics
let stats = calc_stats(100, 60);
// stats.space_saved = 40.0%
```

---

### Java - UUID Utilities

Location: `Java/uuid_utils/mod.java`

Functions:

**UUID v4 Generation (Random):**
- **Generate v4**: `generateV4()` - Generate standard UUID v4 (36 chars with dashes)
- **Generate v4 Compact**: `generateV4Compact()` - Generate UUID without dashes (32 chars)
- **Generate v4 Upper**: `generateV4Upper()` - Generate uppercase UUID v4

**UUID v3/v5 Generation (Name-based):**
- **Generate v3**: `generateV3(namespace, name)` - Generate UUID v3 using MD5 (deterministic)
- **Generate v5**: `generateV5(namespace, name)` - Generate UUID v5 using SHA1 (deterministic)
- **Predefined Namespaces**: `NAMESPACE_DNS`, `NAMESPACE_URL`, `NAMESPACE_OID`, `NAMESPACE_X500`

**Random String Generation:**
- **Random String**: `randomString(length, chars)` - Generate secure random string with custom charset
- **Random Alphanumeric**: `randomAlphanumeric(length)` - Generate alphanumeric string
- **Random Numeric**: `randomNumeric(length)` - Generate numeric-only string
- **Random Hex**: `randomHex(length)` - Generate hexadecimal string
- **Random Password**: `randomPassword(length)` - Generate secure password with mixed character types

**UUID Validation:**
- **Is Valid UUID**: `isValidUUID(uuid)` - Check if string is valid UUID format
- **Is Valid v4**: `isValidV4(uuid)` - Check if string is valid UUID v4
- **Get Version**: `getVersion(uuid)` - Get UUID version (3, 4, 5, or -1)
- **Get Variant**: `getVariant(uuid)` - Get UUID variant (RFC 4122 = 1)

**Format Conversion:**
- **To Compact**: `toCompact(uuid)` - Remove dashes from UUID
- **To Standard**: `toStandard(uuid)` - Add dashes to compact UUID
- **To Upper Case**: `toUpperCase(uuid)` - Convert UUID to uppercase
- **Parse**: `parse(uuid)` - Parse string to java.util.UUID object

**Alternative ID Formats:**
- **Short ID**: `shortId(length)` - Generate Base32 encoded short ID
- **Nano ID**: `nanoId()` / `nanoId(length)` - Generate URL-safe Nano ID (21 chars default)
- **ULID**: `ulid()` - Generate Universally Unique Lexicographically Sortable Identifier (26 chars)

Features:
- Zero dependencies, uses only Java standard library (java.util, java.security)
- Cryptographically secure random generation using SecureRandom
- Supports UUID v3, v4, v5 generation per RFC 4122
- Full UUID validation and format conversion
- Alternative ID formats: Short ID, Nano ID, ULID
- Complete test suite with 69 test cases
- 7 comprehensive usage examples
- Production-ready for distributed systems and database primary keys

Compile and run tests:
```bash
cd Java/uuid_utils
javac *.java
java uuid_utils.uuid_utils_test
```

Compile and run example:
```bash
cd Java
javac -cp . examples/uuid_utils_example.java
java -cp . examples.uuid_utils_example
```

Usage example:
```java
import uuid_utils.mod;

// Generate UUID v4
String uuid = mod.generateV4();
// Returns: "550e8400-e29b-41d4-a716-446655440000"

// Generate compact UUID
String compact = mod.generateV4Compact();
// Returns: "550e8400e29b41d4a716446655440000"

// Generate name-based UUID v5
String v5 = mod.generateV5(mod.NAMESPACE_DNS, "example.com");
// Deterministic: same input always produces same output

// Generate secure password
String password = mod.randomPassword(16);
// Returns: "aB3$kL9@mP2#nQ7!"

// Validate UUID
boolean isValid = mod.isValidUUID("550e8400-e29b-41d4-a716-446655440000");
// Returns: true

// Convert formats
String standard = mod.toStandard("550e8400e29b41d4a716446655440000");
// Returns: "550e8400-e29b-41d4-a716-446655440000"

// Generate Nano ID
String nanoId = mod.nanoId();
// Returns: "V1StGXR8_Z5jdHi6B-myT"

// Generate ULID
String ulid = mod.ulid();
// Returns: "01ARZ3NDEKTSV4RRFFQ69G5FAV"
```

---

### MATLAB - Image Processing Utilities

Location: `MATLAB/image_utils/mod.m`

Functions:

**Color Conversion:**
- **RGB to Grayscale**: `rgb2gray(rgb)` - Convert RGB to grayscale using ITU-R BT.601 standard
- **Grayscale to RGB**: `gray2rgb(gray)` - Replicate grayscale channel to create RGB
- **RGB to HSV**: `rgb2hsv(rgb)` - Convert RGB to HSV color space
- **HSV to RGB**: `hsv2rgb(hsv)` - Convert HSV back to RGB color space

**Image Transformation:**
- **Resize**: `resize(img, [h, w], method)` - Resize image with bilinear/nearest interpolation
- **Crop**: `crop(img, [x, y, w, h])` - Extract rectangular region
- **Rotate**: `rotate(img, angle, method)` - Rotate image by degrees
- **Flip**: `flip(img, direction)` - Horizontal or vertical flip

**Image Filtering:**
- **Box Blur**: `blur(img, kernelSize)` - Apply box blur filter
- **Gaussian Filter**: `gaussianFilter(img, sigma)` - Apply Gaussian blur
- **Sharpen**: `sharpen(img, amount)` - Unsharp mask sharpening
- **Edge Detection**: `edgeDetect(img, method)` - Sobel or Prewitt edge detection

**Image Enhancement:**
- **Brightness**: `brightness(img, delta)` - Adjust brightness (-1 to 1)
- **Contrast**: `contrast(img, factor)` - Adjust contrast
- **Gamma**: `gamma(img, gamma)` - Apply gamma correction
- **Histogram Equalization**: `equalizeHist(img)` - Improve contrast via histogram equalization

**Image Analysis:**
- **Get Size**: `getSize(img)` - Return [height, width, channels]
- **Get Channels**: `getChannels(img)` - Return number of channels
- **Is Grayscale**: `isGrayscale(img)` - Check if image is grayscale
- **Get Histogram**: `getHistogram(img, bins)` - Calculate image histogram

**Utility Functions:**
- **Pad Image**: `padImage(img, padSize, mode)` - Add padding around image
- **Normalize**: `normalize(img, min, max)` - Normalize to range [0,1] or custom
- **Invert**: `invert(img)` - Invert colors (negative)
- **Threshold**: `threshold(img, thresh)` - Create binary image
- **Blend**: `blend(img1, img2, alpha)` - Alpha blend two images

Features:
- Zero dependencies, uses only MATLAB standard library
- Supports uint8, uint16, single, and double data types
- Full RGB and grayscale image support
- Bilinear and nearest neighbor interpolation
- Complete test suite with 25+ test cases
- 20 comprehensive usage examples
- Production-ready for image processing pipelines

Usage example:
```matlab
% Initialize module
utils = mod();

% Load or create an image
img = imread('photo.jpg');  % or create test image

% Color conversion
gray = utils.rgb2gray(img);

% Resize
small = utils.resize(img, [256, 256]);

% Apply filters
blurred = utils.gaussianFilter(img, 2.0);
edges = utils.edgeDetect(img, 'sobel');

% Enhance
bright = utils.brightness(img, 0.3);
highContrast = utils.contrast(img, 1.5);

% Transform
cropped = utils.crop(img, [100, 100, 200, 200]);
rotated = utils.rotate(img, 45);

% Analysis
sz = utils.getSize(img);
hist = utils.getHistogram(img, 256);
```

---

### Go - Crypto Utilities

Location: `Go/crypto_utils/mod.go`

Functions:

**Hash Functions:**
- **MD5 Hash**: `Md5Hash(input)` - Calculate MD5 hash (32-char hex string)
- **SHA1 Hash**: `Sha1Hash(input)` - Calculate SHA1 hash (40-char hex string)
- **SHA256 Hash**: `Sha256Hash(input)` - Calculate SHA256 hash (64-char hex string)
- **SHA512 Hash**: `Sha512Hash(input)` - Calculate SHA512 hash (128-char hex string)
- **SHA256 Bytes**: `Sha256HashBytes(data)` - Calculate SHA256 hash of byte slice

**HMAC Functions:**
- **HMAC-SHA256**: `HmacSha256(message, secret)` - Calculate HMAC-SHA256 with secret key

**Base64 Functions:**
- **Encode**: `Base64Encode(input)` - Encode string to Base64
- **Decode**: `Base64Decode(input)` - Decode Base64 string
- **URL Encode**: `Base64UrlEncode(input)` - URL-safe Base64 encoding (RFC 4648)
- **URL Decode**: `Base64UrlDecode(input)` - Decode URL-safe Base64
- **Validate**: `IsValidBase64(input)` - Check if string is valid Base64

**Random Functions:**
- **Random String**: `RandomString(length, chars)` - Generate secure random string
- **Random Password**: `RandomPassword(length)` - Generate secure password with mixed character types

**UUID Functions:**
- **Generate UUID**: `GenerateUUID()` - Generate version 4 UUID (36 chars with hyphens)
- **Simple UUID**: `GenerateUUIDSimple()` - Generate UUID without hyphens (32 chars)
- **Validate**: `IsValidUUID(uuid)` - Check if string is valid UUID format

**XOR Encryption:**
- **Encrypt**: `XorEncrypt(input, key)` - Simple XOR encryption (returns Base64)
- **Decrypt**: `XorDecrypt(encrypted, key)` - Decrypt XOR encrypted data

**Validation Functions:**
- **Is Valid Hash**: `IsValidHash(hash, algorithm)` - Validate hash format
- **Is Valid MD5**: `IsValidMd5(hash)` - Validate MD5 format
- **Is Valid SHA1**: `IsValidSha1(hash)` - Validate SHA1 format
- **Is Valid SHA256**: `IsValidSha256(hash)` - Validate SHA256 format
- **Is Valid SHA512**: `IsValidSha512(hash)` - Validate SHA512 format

**Constants:**
- `LowerCaseLetters` - "abcdefghijklmnopqrstuvwxyz"
- `UpperCaseLetters` - "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
- `Digits` - "0123456789"
- `SpecialChars` - "!@#$%^&*()-_=+[]{}|;:,.<>?"
- `Alphanumeric` - Letters + digits (62 chars)
- `AllChars` - All character sets combined

Features:
- Zero dependencies, uses only Go standard library (crypto/*, encoding/*, math/big)
- Cryptographically secure random generation using crypto/rand
- Production-ready for security-sensitive applications
- Complete test suite with 30+ test cases
- Full UTF-8 support including Unicode characters
- URL-safe Base64 variant (RFC 4648) support
- UUID v4 generation with RFC 4122 compliance
- Secure password generation with character type enforcement
- Hash format validation for MD5, SHA1, SHA256, SHA512
- XOR encryption for simple obfuscation (not for sensitive data)

Usage example:
```go
package main

import "github.com/ayukyo/alltoolkit/Go/crypto_utils"

func main() {
    // Hash functions
    hash := crypto_utils.Sha256Hash("hello world")
    // Returns: "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    // Base64 encoding
    encoded := crypto_utils.Base64Encode("hello")
    decoded := crypto_utils.Base64Decode(encoded)

    // URL-safe Base64
    urlEncoded := crypto_utils.Base64UrlEncode("hello+world/test")

    // Random generation
    randomStr := crypto_utils.RandomString(16, "")
    password := crypto_utils.RandomPassword(16)

    // UUID generation
    uuid := crypto_utils.GenerateUUID()
    // Returns: "550e8400-e29b-41d4-a716-446655440000"

    // HMAC
    hmac := crypto_utils.HmacSha256("message", "secret_key")

    // XOR encryption
    encrypted := crypto_utils.XorEncrypt("secret", "key")
    decrypted := crypto_utils.XorDecrypt(encrypted, "key")
}
```

---

### ArkTS - HTTP Utilities

Location: `ArkTS/http_utils/mod.ets`

Functions:

**HTTP Methods:**
- **GET**: `httpGet<T>(url, options?)` - Send HTTP GET request
- **POST**: `httpPost<T>(url, body?, options?)` - Send HTTP POST request
- **POST JSON**: `httpPostJson<T>(url, data, options?)` - Send JSON POST request
- **POST Form**: `httpPostForm<T>(url, data, options?)` - Send form POST request
- **PUT**: `httpPut<T>(url, body?, options?)` - Send HTTP PUT request
- **PUT JSON**: `httpPutJson<T>(url, data, options?)` - Send JSON PUT request
- **DELETE**: `httpDelete<T>(url, options?)` - Send HTTP DELETE request
- **PATCH**: `httpPatch<T>(url, body?, options?)` - Send HTTP PATCH request
- **HEAD**: `httpHead<T>(url, options?)` - Send HTTP HEAD request

**URL Utilities:**
- **Build URL**: `buildUrl(baseUrl, params?)` - Build URL with query parameters
- **Build Query String**: `buildQueryString(params)` - Build URL-encoded query string
- **URL Encode**: `urlEncode(value)` - URL encode a string
- **URL Decode**: `urlDecode(value)` - URL decode a string
- **Parse URL**: `parseUrl(url)` - Parse URL into components
- **Get Domain**: `getDomain(url)` - Extract domain from URL
- **Get Path**: `getPath(url)` - Extract path from URL
- **Validate URL**: `isValidUrl(url)` - Check if string is valid URL
- **Parse Query**: `parseQueryString(queryString)` - Parse query string to object
- **Add Params**: `addQueryParams(url, params)` - Add query parameters to URL
- **Remove Params**: `removeQueryParams(url, keys)` - Remove query parameters from URL

Features:
- Zero dependencies, uses only HarmonyOS standard library (@ohos.net.http)
- Full TypeScript/ArkTS type support with generics
- Promise-based API for async/await
- Automatic JSON parsing support
- Form data encoding support
- Custom headers and timeout configuration
- Response time tracking
- Complete URL manipulation utilities
- Comprehensive test suite with 50+ test cases
- Production-ready for HarmonyOS applications

Interfaces:
```typescript
interface HttpResponse<T> {
  statusCode: number;
  statusMessage: string;
  headers: Record<string, string>;
  body: T;
  url: string;
  success: boolean;
  responseTime: number;
}

interface HttpRequestOptions {
  headers?: Record<string, string>;
  timeout?: number;
  parseJson?: boolean;
  contentType?: string;
}
```

Usage example:
```typescript
import { httpGet, httpPostJson, buildUrl } from './http_utils/mod';

// GET request
const response = await httpGet('https://api.example.com/users');
if (response.success) {
  console.info(response.body);
}

// POST JSON
const result = await httpPostJson('https://api.example.com/users', {
  name: 'John',
  age: 30
});

// URL with params
const url = buildUrl('https://api.example.com/search', {
  q: 'hello world',
  page: 1
});
// Result: 'https://api.example.com/search?q=hello%20world&page=1'
```

---

### Fortran - Math Utilities

Location: `Fortran/math_utils/mod.f90`

Functions:

**Vector Operations:**
- **Dot Product**: `dot_product_real(a, b)` - Calculate dot product of two vectors
- **Vector Magnitude**: `vector_magnitude(vec)` - Calculate L2 norm of a vector
- **Normalize Vector**: `normalize_vector(vec)` - Create unit vector
- **Cross Product**: `cross_product(a, b)` - Calculate cross product of two 3D vectors
- **Vector Angle**: `vector_angle(a, b)` - Calculate angle between vectors (radians)
- **Euclidean Distance**: `euclidean_distance(a, b)` - Calculate distance between points

**Statistical Functions:**
- **Mean**: `mean(arr)` / `mean_real(arr)` / `mean_int(arr)` - Calculate arithmetic mean
- **Variance**: `variance(arr, sample)` - Calculate variance (population or sample)
- **Standard Deviation**: `std_dev(arr, sample)` - Calculate standard deviation
- **Median**: `median_real(arr)` - Calculate median value
- **Min/Max**: `min_value(arr)` / `max_value(arr)` - Find extrema
- **Sum/Product**: `sum_values(arr)` / `product_values(arr)` - Aggregate functions

**Numerical Utilities:**
- **Clamp**: `clamp(value, min, max)` - Constrain value to range
- **Linear Interpolation**: `lerp(a, b, t)` - Interpolate between values
- **Smooth Step**: `smoothstep(edge0, edge1, x)` - Hermite interpolation
- **Approximate Equal**: `approx_equal(a, b, tolerance)` - Compare with tolerance
- **Power of Two**: `is_power_of_two(n)` / `next_power_of_two(n)` - Power of two utilities
- **Linspace**: `linspace(start, end, n)` - Generate linearly spaced array
- **Map Range**: `map_range(value, in_min, in_max, out_min, out_max)` - Map between ranges

**Trigonometric Helpers:**
- **Degrees/Radians**: `to_radians(degrees)` / `to_degrees(radians)` - Convert angles
- **Wrap Angle**: `wrap_angle(angle)` / `wrap_angle_signed(angle)` - Normalize angles

**Matrix Operations:**
- **Matrix Multiply**: `matrix_multiply(a, b)` - Multiply two matrices
- **Transpose**: `matrix_transpose(mat)` - Transpose matrix
- **Determinant**: `matrix_determinant(mat)` - Calculate determinant (2x2 or 3x3)
- **Identity**: `identity_matrix(n)` - Create identity matrix

**Interpolation:**
- **Linear Interpolation**: `interp_linear(x, y, xi)` - 1D linear interpolation

Features:
- Zero dependencies, uses only Fortran standard library
- Supports Fortran 90/95/2003+
- Generic interfaces for type flexibility (real/integer)
- Comprehensive documentation with FORD-style comments
- Complete test suite with 40+ test cases
- Production-ready for scientific computing
- Constants: PI, E, EPSILON, DEG_TO_RAD, RAD_TO_DEG

Compile and run tests:
```bash
cd Fortran/math_utils
gfortran -o math_test mod.f90 math_utils_test.f90 && ./math_test
```

Compile and run example:
```bash
cd Fortran/examples
gfortran -o math_example ../math_utils/mod.f90 math_utils_example.f90 && ./math_example
```

Usage example:
```fortran
use math_utils

! Vector operations
real(8) :: v1(3) = [1.0d0, 2.0d0, 3.0d0]
real(8) :: v2(3) = [4.0d0, 5.0d0, 6.0d0]
real(8) :: dot, mag, angle
dot = dot_product_real(v1, v2)
mag = vector_magnitude(v1)
angle = vector_angle(v1, v2)

! Statistics
real(8) :: data(5) = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]
real(8) :: avg, med, std
avg = mean(data)
med = median_real(data)
std = std_dev(data, .true.)  ! Sample std dev

! Numerical utilities
real(8) :: clamped, interpolated
clamped = clamp(15.0d0, 0.0d0, 10.0d0)  ! Returns 10.0
interpolated = lerp(0.0d0, 100.0d0, 0.5d0)  ! Returns 50.0

! Matrix operations
real(8) :: a(2,2) = reshape([1.0d0, 2.0d0, 3.0d0, 4.0d0], [2, 2])
real(8) :: b(2,2) = reshape([5.0d0, 6.0d0, 7.0d0, 8.0d0], [2, 2])
real(8), allocatable :: c(:,:)
c = matrix_multiply(a, b)
```

---

### R - HTTP Utilities

Location: `R/http_utils/mod.R`

Functions:
- **URL 构建**: `build_url(base_url, params)` - 构建带查询参数的完整 URL
- **URL 编码**: `url_encode(str)` - 对字符串进行 URL 编码（空格编码为 %20）
- **URL 解码**: `url_decode(str)` - 对 URL 编码的字符串进行解码
- **URL 解析**: `parse_url(url)` - 解析 URL 为组件列表（scheme, host, port, path, query, fragment, userinfo）
- **查询字符串解析**: `parse_query_string(query_string)` - 解析查询字符串为命名列表
- **查询字符串构建**: `build_query_string(params)` - 从命名列表构建 URL 查询字符串
- **GET 请求**: `http_get(url, headers, timeout)` - 发送 HTTP GET 请求
- **POST 请求**: `http_post(url, body, headers, timeout)` - 发送 HTTP POST 请求
- **POST JSON**: `http_post_json(url, data, headers, timeout)` - 发送 JSON POST 请求
- **POST 表单**: `http_post_form(url, data, headers, timeout)` - 发送表单 POST 请求
- **PUT 请求**: `http_put(url, body, headers, timeout)` - 发送 HTTP PUT 请求
- **PUT JSON**: `http_put_json(url, data, headers, timeout)` - 发送 JSON PUT 请求
- **DELETE 请求**: `http_delete(url, headers, timeout)` - 发送 HTTP DELETE 请求
- **PATCH 请求**: `http_patch(url, body, headers, timeout)` - 发送 HTTP PATCH 请求
- **HEAD 请求**: `http_head(url, headers, timeout)` - 发送 HTTP HEAD 请求
- **JSON 编码**: `json_encode(x)` - 将 R 对象编码为 JSON 字符串
- **JSON 解码**: `json_decode(json)` - 将 JSON 字符串解码为 R 对象
- **URL 验证**: `is_valid_url(url)` - 验证字符串是否为有效的 URL
- **域名提取**: `get_domain(url)` - 从 URL 中提取域名
- **路径提取**: `get_path(url)` - 从 URL 中提取路径
- **超时设置**: `set_http_timeout(seconds)` / `get_http_timeout()` - 配置请求超时

Features:
- 零依赖，仅使用 R 标准库
- 支持多种 HTTP 方法：GET, POST, PUT, DELETE, PATCH, HEAD
- 自动检测并使用 curl（首选）或 wget 作为后端
- 内置 JSON 编解码器（无需外部包如 jsonlite）
- 完整的 URL 解析和构建功能
- URL 编码/解码支持多字节字符（UTF-8）
- 支持自定义请求头和超时配置
- 响应包含状态码、状态消息、响应头、响应体
- 提供完整示例代码 `http_utils_example.R`（11 个实用场景）
- 内置单元测试 `http_utils_test.R`（60+ 测试用例）

运行示例:
```r
source("R/http_utils/mod.R")

# GET 请求
response <- http_get("https://api.example.com/users")
if (response$success) {
  cat(response$body)
}

# POST JSON
response <- http_post_json("https://api.example.com/users",
                           list(name = "John", age = 30))

# URL 操作
url <- build_url("https://api.example.com/search",
                 list(q = "hello world", page = 1))
# 结果: "https://api.example.com/search?q=hello%20world&page=1"

# JSON 操作
data <- list(name = "test", values = c(1, 2, 3))
json <- json_encode(data)
# 结果: '{"name":"test","values":[1,2,3]}'
```

---

### VB - Crypto Utilities

Location: `VB/crypto_utils/mod.vb`

Functions:
- **MD5 哈希**: `Md5Hash(input)` - 计算字符串的 MD5 哈希值（32位小写十六进制）
- **SHA1 哈希**: `Sha1Hash(input)` - 计算字符串的 SHA1 哈希值（40位小写十六进制）
- **SHA256 哈希**: `Sha256Hash(input)` - 计算字符串的 SHA256 哈希值（64位小写十六进制）
- **SHA512 哈希**: `Sha512Hash(input)` - 计算字符串的 SHA512 哈希值（128位小写十六进制）
- **文件哈希**: `Sha256File(filePath)` - 计算文件的 SHA256 哈希值
- **HMAC-SHA256**: `HmacSha256(message, secret)` - 使用密钥计算消息认证码
- **Base64 编码**: `Base64Encode(input)` - 将字符串编码为 Base64
- **Base64 解码**: `Base64Decode(base64)` - 将 Base64 字符串解码为普通字符串
- **URL 安全 Base64 编码**: `Base64UrlEncode(input)` - 编码为 URL 安全的 Base64（替换 +/ 为 -_，移除填充）
- **URL 安全 Base64 解码**: `Base64UrlDecode(base64Url)` - 解码 URL 安全的 Base64
- **随机字符串**: `RandomString(length, chars?)` - 生成指定长度的随机字符串
- **随机密码**: `RandomPassword(length)` - 生成包含大小写字母、数字和特殊字符的密码
- **UUID 生成**: `GenerateUuid()` - 生成标准 UUID v4（带连字符）
- **简化 UUID**: `GenerateUuidSimple()` - 生成无连字符的 32 位 UUID
- **XOR 加密**: `XorEncrypt(input, key)` - 使用 XOR 对称加密（返回 Base64）
- **XOR 解密**: `XorDecrypt(encrypted, key)` - 使用 XOR 对称解密
- **字符串混淆**: `Obfuscate(input)` - 简单的字符串混淆（位移+反转+Base64）
- **字符串反混淆**: `Deobfuscate(obfuscated)` - 反混淆字符串
- **MD5 格式验证**: `IsValidMd5(hash)` - 验证字符串是否为有效的 MD5 格式
- **SHA256 格式验证**: `IsValidSha256(hash)` - 验证字符串是否为有效的 SHA256 格式
- **Base64 格式验证**: `IsValidBase64(base64)` - 验证字符串是否为有效的 Base64

Features:
- 零依赖，仅使用 .NET 标准库（System.Security.Cryptography 等）
- 支持 .NET Framework 4.5+ / .NET Core / .NET 5+
- 完整的 XML 文档注释，支持 IntelliSense
- 安全的空值处理，所有函数接受 null/空字符串参数
- 使用加密安全的随机数生成器（RNGCryptoServiceProvider）
- 完整的 UTF-8 支持（包括中文、Emoji 等多字节字符）
- URL 安全的 Base64 变体（Base64URL）支持
- 提供完整示例代码 `crypto_utils_example.vb`（13个实用场景）
- 内置单元测试 `crypto_utils_test.vb`（30+ 测试用例）

运行示例:
```vb
Imports AllToolkit

' 计算哈希
Dim hash = CryptoUtils.Sha256Hash("Hello, World!")

' Base64 编解码
Dim encoded = CryptoUtils.Base64Encode("你好世界")
Dim decoded = CryptoUtils.Base64Decode(encoded)

' 生成随机密码
Dim password = CryptoUtils.RandomPassword(16)

' XOR 加密
Dim encrypted = CryptoUtils.XorEncrypt("Secret", "my_key")
Dim decrypted = CryptoUtils.XorDecrypt(encrypted, "my_key")
```

---

### Python - File Utilities (新增测试)

Location: `Python/file_utils_test.py`

新增测试覆盖:
- **安全读取测试**: 正常读取、不存在文件、Unicode内容
- **安全写入测试**: 新文件、自动创建目录、原子写入、覆盖
- **文件哈希测试**: MD5/SHA256计算、不存在文件、无效算法
- **文件大小测试**: 字节大小、人类可读格式
- **目录操作测试**: 创建新目录、嵌套目录
- **文件列表测试**: 所有文件、通配符模式、不存在目录
- **复制移动测试**: 成功复制、覆盖控制、移动文件
- **删除文件测试**: 成功删除、missing_ok参数
- **唯一文件名测试**: 新文件、已存在文件

运行测试: `cd Python && python -m pytest file_utils_test.py -v`

---

### Kotlin - DateTime Utilities (新增测试)

Location: `Kotlin/date_time_utils/DateTimeUtilsTest.kt`

新增测试覆盖:
- **时间戳测试**: 当前毫秒/秒、转换
- **格式化测试**: 多种格式、时区处理
- **解析测试**: 正常解析、无效格式、空值
- **相对时间测试**: 刚刚、分钟前、小时前、昨天、未来
- **时间差测试**: 天数差、小时差、绝对值
- **日期判断测试**: 今天、昨天、本周
- **闰年测试**: 闰年判断、月份天数
- **时间计算测试**: 添加天数/小时/分钟
- **年龄测试**: 年龄计算
- **时长格式化**: 完整格式、简短格式
- **工作日测试**: 工作日/周末判断
- **时间范围**: 生成时间范围列表

运行测试: `cd Kotlin/date_time_utils && kotlinc -include-runtime -d test.jar *.kt && java -jar test.jar`

---

### PHP - String Utilities (新增测试)

Location: `PHP/string_utils/StringUtilsTest.php`

新增测试覆盖:
- **空值检查**: isBlank/isNotBlank, null/空/空白处理
- **字符串截取**: substring多字节支持、truncate截断
- **命名转换**: camelToSnake/snakeToCamel, PascalCase支持
- **随机字符串**: random长度验证、边界值
- **前缀后缀**: startsWith/endsWith, 大小写敏感/不敏感
- **移除操作**: removePrefix/removeSuffix
- **行分割**: lines去除空行
- **重复填充**: repeat/pad, 边界值
- **反转**: reverse多字节支持
- **显示宽度**: displayWidth中英文混排
- **大小写**: capitalize/uncapitalize
- **计数**: count子串出现次数
- **相等**: equals安全比较
- **slug**: URL友好转换

运行测试: `cd PHP/string_utils && php StringUtilsTest.php`

---

### Swift - String Utilities (新增测试)

Location: `Swift/string_utils/StringUtilsTest.swift`

新增测试覆盖:
- **空值检查**: isBlank/isNotBlank
- **子串操作**: substring安全索引、truncate截断
- **空白处理**: trimmed/normalizeWhitespaces
- **验证方法**: isValidEmail/isValidChinesePhone/isValidURL/isNumeric
- **正则匹配**: isMatch/matches/firstMatch
- **编码解码**: urlEncoded/urlDecoded/base64Encoded/base64Decoded
- **命名转换**: toCamelCase/toPascalCase/toSnakeCase/toKebabCase
- **其他工具**: repeated/leftPadded/rightPadded/md5/sha256

运行测试: 使用 Xcode 或 `swift test`

---

### Perl - URL Utilities

Location: `Perl/url_utils/mod.pl`

Functions:
- **URL 编码**: `url_encode(str)` - 对字符串进行 URL 编码（空格编码为 %20）
- **URL 解码**: `url_decode(str)` - 对 URL 编码的字符串进行解码
- **组件编码**: `url_encode_component(str)` - 对 URL 组件进行编码（对保留字符也编码）
- **组件解码**: `url_decode_component(str)` - 对 URL 组件编码的字符串进行解码
- **解析查询字符串**: `parse_query_string(qs)` - 解析 URL 查询字符串为哈希引用，支持数组参数
- **构建查询字符串**: `build_query_string(params, options?)` - 从哈希引用构建 URL 查询字符串，支持排序和跳过空值
- **解析 URL**: `parse_url(url)` - 解析 URL 为组件哈希引用（scheme, host, port, path, query, fragment, userinfo）
- **构建 URL**: `build_url(components)` - 从组件哈希引用构建完整 URL
- **验证 URL**: `is_valid_url(url)` - 验证字符串是否为有效的 URL
- **提取域名**: `get_domain(url)` - 从 URL 中提取域名
- **提取路径**: `get_path(url)` - 从 URL 中提取路径
- **添加参数**: `add_query_params(url, params)` - 向 URL 添加查询参数
- **移除参数**: `remove_query_params(url, keys)` - 从 URL 中移除指定的查询参数
- **规范化 URL**: `normalize_url(url)` - 规范化 URL（统一格式、移除默认端口、处理路径中的 . 和 ..）

Features:
- 零依赖，仅使用 Perl 标准库（Exporter、strict、warnings）
- 完整的 POD 文档注释，支持 `perldoc` 查看
- 完整的 RFC 3986 URL 规范支持
- 支持数组参数（同名参数多次出现自动转为数组）
- URL 安全处理，防止注入攻击
- 自动处理默认端口移除（http:80, https:443）
- 路径规范化（处理 . 和 ..）
- 完整的 Unicode/UTF-8 支持
- 提供完整示例代码 `url_utils_example.pl`
- 内置单元测试 `url_utils_test.pl`（20+ 测试用例）

---

### JavaScript - Base64 Utilities

Location: `JavaScript/base64_utils/mod.js`

Functions:
- **编码**: `encode(str, options?)` - 将字符串编码为 Base64，支持 URL 安全变体和填充选项
- **解码**: `decode(base64, options?)` - 将 Base64 字符串解码为普通字符串
- **URL 安全转换**: `toUrlSafe(base64, pad?)` - 将标准 Base64 转换为 URL 安全格式
- **URL 安全还原**: `fromUrlSafe(base64url)` - 将 URL 安全 Base64 转换为标准格式
- **验证**: `isValid(str, options?)` - 验证字符串是否为有效的 Base64
- **转二进制**: `toUint8Array(base64)` - 将 Base64 字符串转换为 Uint8Array
- **二进制编码**: `fromUint8Array(bytes, options?)` - 将 Uint8Array 编码为 Base64
- **计算长度**: `encodedLength(str, options?)` - 计算编码后的字符串长度

Features:
- 零依赖，纯 JavaScript 实现，适用于浏览器和 Node.js
- 完整的 UTF-8 支持（包括中文、Emoji 等多字节字符）
- URL 安全 Base64 变体（Base64URL）支持
- 可选的填充字符控制
- 完整的 Uint8Array 二进制数据处理
- 严格的输入验证和错误处理
- 支持 CommonJS 和 ES Module 导出
- 提供完整示例代码 `base64_utils_example.js`
- 内置单元测试 `base64_utils_test.js`

---

### TypeScript - HTTP Utilities

Location: `TypeScript/http_utils/mod.ts`

Functions:
- **GET 请求**: `get<T>(url, options?)` - 发送 GET 请求，支持泛型类型推断
- **POST 请求**: `post<T>(url, body, options?)` - 发送 JSON POST 请求
- **POST 表单**: `postForm<T>(url, formData, options?)` - 发送表单 POST 请求
- **PUT 请求**: `put<T>(url, body, options?)` - 发送 PUT 请求
- **DELETE 请求**: `del<T>(url, options?)` - 发送 DELETE 请求
- **PATCH 请求**: `patch<T>(url, body, options?)` - 发送 PATCH 请求
- **HEAD 请求**: `head<T>(url, options?)` - 发送 HEAD 请求，获取响应头
- **URL 构建**: `buildUrl(baseUrl, params?)` - 构建带查询参数的完整 URL
- **查询字符串**: `buildQueryString(params)` - 构建 URL 编码的查询字符串
- **URL 编码**: `urlEncode(value)` - URL 编码字符串
- **URL 解码**: `urlDecode(value)` - URL 解码字符串
- **创建客户端**: `createClient(defaultOptions?)` - 创建可复用配置的 HTTP 客户端实例

Features:
- 零依赖，仅使用 TypeScript 原生 fetch API
- 完整的 TypeScript 类型支持（泛型、接口、类型推断）
- 支持请求超时控制（使用 AbortController）
- 自定义请求头、凭证模式、CORS 模式
- 自动 JSON 解析和响应处理
- 自定义错误类：HttpError（包含状态码、响应数据、URL）和 TimeoutError
- 响应包含状态码、状态文本、响应数据、响应头、成功标志、URL
- 提供完整示例代码 `http_utils_example.ts`
- 内置单元测试 `http_utils_test.ts`

---

### C# - HTTP Utilities

Location: `C#/http_utils/mod.cs`

Functions:
- **GET 请求**: `Get(url, options)` / `GetAsync(url, options)` - 发送 GET 请求
- **POST 请求**: `Post(url, body, contentType, options)` / `PostAsync(url, body, contentType, options)` - 发送 POST 请求
- **POST JSON**: `PostJson(url, jsonData, options)` / `PostJsonAsync(url, jsonData, options)` - 发送 JSON POST 请求
- **POST 表单**: `PostForm(url, formData, options)` / `PostFormAsync(url, formData, options)` - 发送表单 POST 请求
- **PUT 请求**: `Put(url, body, contentType, options)` / `PutAsync(url, body, contentType, options)` - 发送 PUT 请求
- **PUT JSON**: `PutJson(url, jsonData, options)` / `PutJsonAsync(url, jsonData, options)` - 发送 JSON PUT 请求
- **DELETE 请求**: `Delete(url, options)` / `DeleteAsync(url, options)` - 发送 DELETE 请求
- **PATCH 请求**: `Patch(url, body, contentType, options)` / `PatchAsync(url, body, contentType, options)` - 发送 PATCH 请求
- **URL 编码**: `UrlEncode(value)` - URL 编码字符串
- **URL 解码**: `UrlDecode(value)` - URL 解码字符串
- **查询字符串**: `BuildQueryString(parameters)` - 构建 URL 查询参数
- **完整 URL**: `BuildUrl(baseUrl, parameters)` - 构建带查询参数的完整 URL

Features:
- 零依赖，仅使用 .NET 标准库 (System.Net.Http)
- 支持 .NET 6.0+ / .NET Framework 4.5+ / .NET Standard 2.0+
- 完整的 XML 文档注释
- 同步和异步 API 双支持
- 内置超时控制和错误处理
- 支持自定义请求头
- 自动请求耗时统计
- 响应包含状态码、响应体、响应头和错误信息
- 提供完整示例代码 `http_utils_example.cs`
- 内置单元测试 `http_utils_test.cs`

---

### C++ - JSON Utilities

Location: `C++/json_utils/mod.hpp`

Functions:
- **构造器**: `Json()` / `Json(nullptr)` / `Json(bool/int/double/string)` - 创建各种类型的 JSON 值
- **数组构造**: `Json::Array({...})` - 从初始化列表创建 JSON 数组
- **对象构造**: `Json::Object({{key, value}, ...})` - 从键值对创建 JSON 对象
- **类型检查**: `isNull()` / `isBoolean()` / `isNumber()` / `isString()` / `isArray()` / `isObject()` - 检查值类型
- **类型转换**: `asBool()` / `asInt()` / `asDouble()` / `asString()` / `asArray()` / `asObject()` - 安全获取值
- **数组访问**: `operator[](size_t index)` - 按索引访问数组元素
- **对象访问**: `operator[](const string& key)` / `has(key)` - 按键访问对象属性
- **安全取值**: `getString(key, default)` / `getInt(key, default)` / `getDouble(key, default)` / `getBool(key, default)` - 带默认值的类型安全访问
- **序列化**: `toString()` - 生成紧凑 JSON 字符串
- **美化输出**: `toPrettyString(indent)` - 生成格式化 JSON 字符串
- **解析**: `Json::parse(json)` / `Json::parse(json, error)` - 解析 JSON 字符串
- **验证**: `Json::isValid(json)` - 验证 JSON 字符串有效性

Features:
- 零依赖，仅使用 C++ 标准库 (C++11+)
- Header-only 设计，单文件即可使用
- 完整支持 JSON 标准 (RFC 8259)
- 类型安全的访问器，带异常处理
- 支持嵌套对象和数组
- 字符串转义处理（支持 \\n, \\t, \" 等）
- Unicode 转义序列支持 (\\uXXXX)
- 美观打印输出
- 带默认值的 getter 方法
- 提供完整示例代码 `json_utils_example.cpp`
- 内置单元测试 `json_utils_test.cpp`

---

### Java - HTTP Utilities

Location: `Java/http_utils/mod.java`

Functions:
- **GET 请求**: `get(url)` / `get(url, headers)` / `get(url, headers, connectTimeout, readTimeout)` - 发送 GET 请求
- **POST 请求**: `post(url, body, headers)` / `postJson(url, jsonBody)` / `postForm(url, formData)` - 发送 POST 请求
- **PUT 请求**: `put(url, body, headers)` / `putJson(url, jsonBody)` - 发送 PUT 请求
- **DELETE 请求**: `delete(url)` / `delete(url, headers)` - 发送 DELETE 请求
- **URL 编码**: `urlEncode(value)` / `urlDecode(value)` - URL 编码解码
- **查询字符串**: `buildQueryString(params)` - 构建 URL 查询参数
- **完整 URL**: `buildUrl(baseUrl, params)` - 构建带查询参数的完整 URL

Features:
- 零第三方依赖，仅使用 Java 标准库 (java.net.HttpURLConnection)
- 完整 Javadoc 文档注释
- 支持自定义连接/读取超时
- 自动处理请求头
- 支持 JSON 和表单数据提交
- 响应包含状态码、响应体和响应头
- 提供完整示例代码 `http_utils_example.java`
- 内置单元测试 `http_utils_test.java`

---

### Swift - Date Utilities

Location: `Swift/date_utils/mod.swift`

Functions:
- **格式化**: `string(format:)` / `iso8601String()` / `dateString()` / `timeString()` / `chineseDateString()`
- **相对时间**: `relativeTimeString()` - "刚刚"、"5 分钟前"、"昨天"等
- **日期计算**: `adding(days:)` / `adding(hours:)` / `adding(minutes:)` / `adding(seconds:)`
- **日期比较**: `isToday()` / `isYesterday()` / `isTomorrow()` / `isThisWeek()` / `isThisMonth()`
- **日期边界**: `startOfDay()` / `endOfDay()` / `startOfWeek()` / `endOfWeek()` / `startOfMonth()` / `endOfMonth()`
- **日期差值**: `days(since:)` / `hours(since:)` / `minutes(since:)` / `seconds(since:)`
- **时间戳**: `timestamp()` (秒级) / `timestampMilliseconds()` (毫秒级)
- **解析**: `from(string:format:)` / `fromISO8601(_:)`
- **特殊判断**: `isWeekend()` / `isWeekday()` / `isLeapYear()` / `daysInMonth()`
- **年龄计算**: `age()` - 精确计算年龄

Features:
- 零依赖，仅使用 Swift 标准库 Foundation
- 完整文档注释
- 支持 iOS 13.0+ / macOS 10.15+ / watchOS 6.0+ / tvOS 13.0+
- 时区安全
- 提供完整示例代码 `ExampleDateUtils.swift`

**Test Suite (NEW):**
Location: `Swift/date_utils/DateUtilsTest.swift`

新增测试覆盖:
- **格式化测试**: 多种格式、ISO8601、中文格式
- **相对时间**: 刚刚、分钟前、小时前、昨天、多天前
- **日期计算**: 添加年/月/日/时/分、跨年跨月边界
- **日期比较**: 同一天、今天、昨天、明天、范围判断
- **日期组件**: 年/月/日/时/分/秒、星期几获取
- **时间戳**: 秒级和毫秒级转换
- **日期边界**: 当天开始/结束、当月开始/结束、闰年2月
- **日期差值**: 天数/小时/分钟差值计算
- **特殊判断**: 周末/工作日、闰年、每月天数
- **年龄计算**: 周岁计算

运行测试: 使用 Xcode 或 `swift test`

---

### C - String Utilities

Location: `C/string_utils/` (实现 + 头文件)

Functions:
- `str_trim(str)` - 去除首尾空白字符
- `str_trim_left(str)` - 去除左侧空白字符
- `str_trim_right(str)` - 去除右侧空白字符
- `str_to_lower(str)` - 转换为小写
- `str_to_upper(str)` - 转换为大写
- `str_reverse(str)` - 反转字符串
- `str_starts_with(str, prefix)` - 检查前缀
- `str_ends_with(str, suffix)` - 检查后缀
- `str_count(str, substr)` - 统计子串出现次数
- `str_copy_safe(dest, src, dest_size)` - 安全字符串复制
- `is_whitespace(c)` - 判断空白字符

Features:
- 零依赖，仅使用标准 C 库 (`string.h`, `ctype.h`)
- 完整 Doxygen 风格注释
- 支持 C/C++ 混合编译
- 安全边界检查
- 提供可运行示例 `example_string_utils.c`

**Test Suite (NEW):**
Location: `C/string_utils/string_utils_test.c`

新增测试覆盖:
- **空白字符检测**: 空格、制表符、换行符、回车符等
- **修剪测试**: 左右修剪、双边修剪、各种空白字符、空字符串、NULL处理
- **大小写转换**: 基本转换、混合内容、空字符串、NULL处理
- **字符串反转**: 奇偶长度、单字符、空字符串、NULL处理
- **前缀后缀检查**: 正常检查、精确匹配、空字符串、NULL处理
- **子串计数**: 基本计数、重叠匹配、未找到、空字符串、NULL处理
- **安全复制**: 基本复制、精确大小、截断处理、空字符串、NULL处理

运行测试:
```bash
cd C/string_utils
gcc -o string_utils_test string_utils.c string_utils_test.c && ./string_utils_test
```

---

### Rust - Collection Utilities

Location: `Rust/collection_utils/mod.rs`

Functions:
- `deduplicate(vec)` - 去重（保持原顺序）
- `group_by(vec, key_fn)` - 按条件分组
- `find_index(vec, predicate)` / `find_last_index()` / `find_all_indices()` - 索引查找
- `intersect(vec1, vec2)` / `union()` / `difference()` - 集合运算（交/并/差）
- `chunk(vec, size)` / `split_into(vec, n)` - 分块操作
- `count_occurrences(vec)` - 频率统计
- `most_frequent(vec)` / `top_frequent(vec, n)` - 最频繁元素
- `partition(vec, predicate)` - 条件分区
- `flatten(vec_of_vecs)` - 扁平化嵌套向量
- `has_duplicates(vec)` - 重复检查
- `sort_by_key(vec, key_fn)` / `sort_by_key_desc()` - 键排序
- `to_map(vec, key_fn, value_fn)` - 转换为 HashMap
- `unique_with_index(vec)` - 带索引的去重

Features:
- 零依赖，仅使用 Rust 标准库
- 支持 Rust 1.70+
- 完整 Rust 文档注释（支持 `cargo doc`）
- 内置 10+ 个单元测试
- 泛型设计，支持任意类型
- 附带可运行示例 `example_collection_utils.rs`

**Test Suite (NEW):**
Location: `Rust/collection_utils/collection_utils_test.rs`

新增测试覆盖:
- **去重测试**: 基本去重、空向量、无重复、全部相同、字符串去重
- **分组测试**: 奇偶分组、空向量、相同键分组
- **索引查找**: 正向/反向查找、所有索引、未找到、空向量
- **集合运算**: 交集、并集、差集的各种边界情况
- **分块操作**: 基本分块、精确分块、空向量、零大小处理
- **频率统计**: 计数、最频繁元素、Top N、平局处理
- **分区扁平化**: 条件分区、空向量处理、嵌套扁平化
- **重复检查**: 有重复、无重复、单元素、空向量
- **排序测试**: 升序/降序排序、空向量、稳定排序验证

运行测试: `cd Rust/collection_utils && rustc --test collection_utils_test.rs -o test && ./test`

---

### Swift - String Utilities

Location: `Swift/string_utils/mod.swift`

Functions:
- **空值检查**: `isBlank` / `isNotBlank`
- **子串操作**: `substring(start:end:)` / `substring(from:)` / `substring(to:)` / `truncate(maxLength:suffix:)`
- **空白处理**: `trimmed()` / `removeAllWhitespaces()` / `normalizeWhitespaces()`
- **验证方法**: `isValidEmail()` / `isValidPhone()` / `isValidURL()` / `isValidIDCard()` / `isValidIPv4()`
- **正则匹配**: `isMatch(pattern:)` / `matches(pattern:)` / `firstMatch(pattern:)` / `replacingMatches(pattern:with:)`
- **编码解码**: `urlEncoded()` / `urlDecoded()` / `base64Encoded()` / `base64Decoded()`
- **命名转换**: `camelCased()` / `pascalCased()` / `snakeCased()` / `kebabCased()`
- **其他工具**: `repeating(count:)` / `padded(length:with:alignment:)` / `reversed()` / `containsIgnoreCase(_:)`
- **类型转换**: `toInt()` / `toDouble()` / `toBool()`

Features:
- 零依赖，仅使用 Swift 标准库
- 完整文档注释
- 支持 iOS 13.0+ / macOS 10.15+ / watchOS 6.0+ / tvOS 13.0+
- Unicode 安全
- 提供完整示例代码 `ExampleStringUtils.swift`

---

### Rust - String Utilities

Location: `Rust/string_utils/mod.rs`

Functions:
- `truncate(s, max_len)` - 按字符数截断（支持 Unicode）
- `truncate_bytes(s, max_bytes)` - 按字节数截断
- `is_blank(s)` / `is_not_blank(s)` - 空值检查
- `count_words(s)` - 统计单词数
- `is_valid_email(s)` - 邮箱格式验证
- `reverse_graphemes(s)` - 安全反转字符串（支持 Unicode）
- `pad(s, width, pad_char, alignment)` - 左右填充

Features:
- 零依赖，仅使用 Rust 标准库
- 完整文档注释
- Unicode 安全（正确处理 emoji 和多字节字符）
- 内置单元测试
- 附带可运行示例

---

### PHP - String Utilities

Location: `PHP/string_utils/mod.php`

Functions:
- `isBlank(str)` / `isNotBlank(str)` - 检查字符串是否为空或仅包含空白字符
- `substring(str, start, length, encoding)` - 安全地截取字符串（支持多字节字符）
- `truncate(str, maxLength, suffix, encoding)` - 截取字符串并添加省略号
- `camelToSnake(str)` - 驼峰命名转下划线命名（snake_case）
- `snakeToCamel(str, capitalizeFirst)` - 下划线命名转驼峰命名（camelCase/PascalCase）
- `random(length, chars)` - 生成随机字符串
- `startsWith(str, prefix, ignoreCase)` - 检查字符串是否以指定前缀开头
- `endsWith(str, suffix, ignoreCase)` - 检查字符串是否以指定后缀结尾
- `removePrefix(str, prefix)` - 移除字符串前缀（如果存在）
- `removeSuffix(str, suffix)` - 移除字符串后缀（如果存在）
- `lines(str, trimEmpty)` - 将字符串按行分割为数组
- `repeat(str, count)` - 重复字符串指定次数
- `pad(str, length, padStr, padType)` - 填充字符串到指定长度
- `reverse(str, encoding)` - 反转字符串（支持多字节字符）
- `displayWidth(str, encoding)` - 计算字符串在终端显示宽度（处理中英文混排）
- `capitalize(str, encoding)` / `uncapitalize(str, encoding)` - 首字母大小写转换
- `count(str, sub, ignoreCase)` - 计算子字符串出现次数
- `equals(str1, str2, ignoreCase)` - 安全地比较两个字符串
- `slug(str, separator)` - 将字符串转换为URL友好的slug

Features:
- 零依赖，仅使用 PHP 标准库
- 完整的 PHPDoc 文档
- 支持多字节字符（UTF-8）
- 空值安全（所有方法接受 null 参数）
- 提供完整示例代码 `ExampleStringUtils.php`

---

### Kotlin - DateTime Utilities

Location: `Kotlin/date_time_utils/mod.kt`

Functions:
- `currentTimeMillis()` / `currentTimeSeconds()` - 获取当前时间戳
- `format(timestamp, pattern)` - 格式化时间戳为字符串
- `parseToMillis(dateString, pattern)` - 解析日期字符串为时间戳
- `getRelativeTimeDesc(timestamp)` - 获取相对时间描述（几分钟前、昨天等）
- `daysBetween(start, end)` / `hoursBetween(start, end)` - 计算时间间隔
- `isToday(timestamp)` / `isYesterday(timestamp)` / `isThisWeek(timestamp)` - 日期判断
- `isWeekday(timestamp)` / `isWeekend(timestamp)` - 工作日/周末判断
- `getStartOfDay(timestamp)` / `getEndOfDay(timestamp)` - 获取当天起止时间
- `addDays(timestamp, days)` / `addHours(timestamp, hours)` / `addMinutes(timestamp, minutes)` - 时间加减
- `isLeapYear(year)` / `getDaysInMonth(year, month)` - 闰年和月份天数
- `getAge(birthTimestamp)` - 计算年龄
- `formatDuration(durationMillis)` / `formatDurationShort(durationMillis)` - 时长格式化
- `getFriendlyDate(timestamp)` - 获取友好日期显示
- `generateTimeRanges(start, end, intervalMinutes)` - 生成时间范围列表

Features:
- 零依赖，仅使用 Kotlin 标准库 (java.time)
- 完整的 KDoc 文档
- 支持多种日期格式
- 时区安全（使用系统默认时区）
- 提供完整示例代码

---

### Python - File Utilities

Location: `Python/file_utils.py` (示例：`Python/examples/file_utils_example.py`)

Functions:
- `safe_read_text(filepath, encoding='utf-8', default=None)` - 安全读取文本文件，自动处理异常
- `safe_write_text(filepath, content, encoding='utf-8', create_dirs=True, atomic=False)` - 安全写入文本文件，支持原子写入
- `get_file_hash(filepath, algorithm='md5', chunk_size=8192)` - 计算文件哈希值（支持大文件分块读取）
- `get_file_size(filepath, human_readable=False)` - 获取文件大小，支持人类可读格式
- `ensure_dir(directory, mode=0o755)` - 确保目录存在，自动创建父目录
- `list_files(directory, pattern='*', recursive=False, include_dirs=False, sort_by='name')` - 列出目录文件，支持通配符和排序
- `copy_file(src, dst, overwrite=False, preserve_metadata=True)` - 安全复制文件
- `move_file(src, dst, overwrite=False)` - 安全移动文件或目录
- `delete_file(filepath, missing_ok=True)` - 安全删除文件
- `get_unique_filename(filepath, suffix_format='_{}')` - 获取唯一文件名（自动添加序号）

Features:
- 纯函数设计，无外部依赖
- 异常安全，所有操作返回状态而非抛出异常
- 支持 Path 对象和字符串路径
- 大文件友好（分块读取哈希）
- 原子写入支持（防止写入中断导致文件损坏）
- 完整类型注解

### Go - Path Utilities

Location: `Go/path_utils/path_utils.go`

Functions:
- `SafeJoin(elems ...string) string` - Safely joins path elements, prevents traversal attacks
- `ExtNoDot(path string) string` - Returns file extension without leading dot (lowercase)
- `BaseNoExt(path string) string` - Returns filename without extension
- `HasExt(path string, exts ...string) bool` - Checks if file has any of specified extensions

Features:
- Cross-platform (Windows, macOS, Linux)
- Security-focused (prevents path traversal)
- Case-insensitive extension matching
- Zero dependencies (uses only standard library)
- Handles edge cases (whitespace, empty components)

### Go - String Utilities

Location: `Go/string_utils/string_utils.go`

Functions:
- `Truncate(s string, maxLen int) string` - Truncates string by rune count with ellipsis
- `TruncateSafe(s string, maxLen int) string` - Truncates string by byte count with ellipsis

Features:
- Unicode-aware (properly handles multi-byte characters)
- UTF-8 safe (never cuts in the middle of a character)
- Zero dependencies (uses only standard library)
- Efficient memory usage (allocates only when needed)

## Usage

See individual language directories for specific usage instructions.

## 🤝 Contributing

欢迎贡献！查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何添加新工具。

### 贡献者

<!-- 贡献者列表将自动更新 -->
- [@ayukyo](https://github.com/ayukyo) - 项目发起者

## 📄 License

MIT License - 免费用于个人和商业项目

## 🔗 Links

- [GitHub Repository](https://github.com/ayukyo/alltoolkit)
- [Issues](https://github.com/ayukyo/alltoolkit/issues)
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

---

## 📦 Latest Addition

### Rust - URL Utilities

Location: `Rust/url_utils/mod.rs`

A comprehensive URL manipulation utility module providing URL parsing, building, encoding/decoding, query string manipulation, and URL validation with zero dependencies.

**URL Parsing:**
- **parse_url**: `parse_url(url)` - Parse URL string into ParsedUrl struct with all components
- **ParsedUrl struct**: Access scheme, host, port, path, query params, fragment, username, password
- **origin**: `url.origin()` - Get origin (scheme + host + port)
- **is_secure**: `url.is_secure()` - Check if URL uses HTTPS

**URL Building:**
- **UrlBuilder**: `UrlBuilder::new()` - Create URLs programmatically
  - **scheme**: Set URL scheme (http/https/ftp)
  - **host**: Set host name
  - **port**: Set port number
  - **username/password**: Set authentication
  - **path**: Set URL path
  - **query_param**: Add query parameters
  - **fragment**: Set URL fragment
  - **build**: Generate final URL string

**URL Encoding/Decoding:**
- **url_encode**: `url_encode(input)` - URL-encode a string (RFC 3986)
- **url_decode**: `url_decode(input)` - URL-decode a string
- Supports special characters, Unicode, spaces (+ or %20)

**Query String Manipulation:**
- **parse_query_string**: `parse_query_string(query)` - Parse query string into HashMap
- **build_query_string**: `build_query_string(params)` - Build query string from HashMap
- **get_param**: `url.get_param(key)` - Get query parameter value
- **set_param**: `url.set_param(key, value)` - Set query parameter
- **remove_param**: `url.remove_param(key)` - Remove query parameter

**URL Validation & Utilities:**
- **is_valid_url**: `is_valid_url(url)` - Check if string is valid URL
- **normalize_url**: `normalize_url(url)` - Normalize URL (lowercase scheme/host, remove default ports)
- **get_domain**: `get_domain(url)` - Extract domain from URL
- **get_path**: `get_path(url)` - Extract path from URL
- **join_url**: `join_url(base, path)` - Join base URL with relative path

**Features:**
- Zero dependencies, uses only Rust standard library
- Full RFC 3986 compliance for URL parsing and encoding
- Support for authentication (username/password)
- IPv6 address support
- Query string parameter manipulation
- URL builder pattern for constructing URLs
- Complete test suite with 25+ test cases
- 10 comprehensive usage examples
- Production-ready for web applications and API clients

Compile and run tests:
```bash
cd Rust/url_utils
rustc --test --edition 2021 mod.rs -o url_test && ./url_test
```

Run example:
```bash
cd Rust/examples
rustc --edition 2021 url_utils_example.rs -o url_example && ./url_example
```

Usage example:
```rust
use url_utils::*;

// Parse a URL
let url = parse_url("https://api.example.com:8080/v1/users?page=1").unwrap();
println!("Host: {}", url.host);  // "api.example.com"
println!("Port: {:?}", url.port); // Some(8080)
println!("Path: {}", url.path);   // "/v1/users"
println!("Page: {:?}", url.get_param("page")); // Some("1")

// Build a URL
let url = UrlBuilder::new()
    .scheme("https")
    .host("api.example.com")
    .path("/v2/search")
    .query_param("q", "rust programming")
    .query_param("limit", "10")
    .build();
// Result: "https://api.example.com/v2/search?q=rust%20programming&limit=10"

// URL encoding/decoding
let encoded = url_encode("hello world!");  // "hello%20world%21"
let decoded = url_decode("hello%20world"); // "hello world"

// Query string manipulation
let mut url = parse_url("https://example.com?existing=value").unwrap();
url.set_param("new", "param");
url.remove_param("existing");

// URL validation
if is_valid_url("https://example.com") {
    println!("Valid URL!");
}

// Join URLs
let full_url = join_url("https://api.example.com/v1", "users").unwrap();
// Result: "https://api.example.com/v1/users"
```

---

### Python - DateTime Utilities

Location: `Python/datetime_utils/mod.py`

A comprehensive date and time utility module for Python providing formatting, parsing, arithmetic, and various date/time operations with zero dependencies.

**Core Functions:**

**Current Time:**
- **now**: `DateTimeUtils.now()` - Get current local datetime
- **now_utc**: `DateTimeUtils.now_utc()` - Get current UTC datetime
- **today**: `DateTimeUtils.today()` - Get today at 00:00:00
- **timestamp**: `DateTimeUtils.timestamp()` - Get current timestamp (seconds)
- **timestamp_ms**: `DateTimeUtils.timestamp_ms()` - Get current timestamp (milliseconds)

**Timestamp Conversion:**
- **timestamp_to_datetime**: `DateTimeUtils.timestamp_to_datetime(ts, unit='s')` - Convert timestamp to datetime
- **datetime_to_timestamp**: `DateTimeUtils.datetime_to_timestamp(dt, unit='s')` - Convert datetime to timestamp

**Formatting & Parsing:**
- **format**: `DateTimeUtils.format(dt, fmt)` - Format datetime to string
- **parse**: `DateTimeUtils.parse(date_string, fmt)` - Parse string to datetime
- **parse_auto**: `DateTimeUtils.parse_auto(date_string)` - Auto-detect format and parse
- **to_iso8601**: `DateTimeUtils.to_iso8601(dt)` - Convert to ISO 8601 format
- **from_iso8601**: `DateTimeUtils.from_iso8601(iso_string)` - Parse ISO 8601 string

**Time Arithmetic:**
- **add_days**: `DateTimeUtils.add_days(dt, days)` - Add/subtract days
- **add_hours**: `DateTimeUtils.add_hours(dt, hours)` - Add/subtract hours
- **add_minutes**: `DateTimeUtils.add_minutes(dt, minutes)` - Add/subtract minutes
- **add_seconds**: `DateTimeUtils.add_seconds(dt, seconds)` - Add/subtract seconds
- **add_months**: `DateTimeUtils.add_months(dt, months)` - Add/subtract months
- **add_years**: `DateTimeUtils.add_years(dt, years)` - Add/subtract years

**Time Difference:**
- **days_between**: `DateTimeUtils.days_between(start, end)` - Calculate days difference
- **hours_between**: `DateTimeUtils.hours_between(start, end)` - Calculate hours difference
- **minutes_between**: `DateTimeUtils.minutes_between(start, end)` - Calculate minutes difference
- **seconds_between**: `DateTimeUtils.seconds_between(start, end)` - Calculate seconds difference

**Date Checks:**
- **is_today**: `DateTimeUtils.is_today(dt)` - Check if date is today
- **is_yesterday**: `DateTimeUtils.is_yesterday(dt)` - Check if date is yesterday
- **is_tomorrow**: `DateTimeUtils.is_tomorrow(dt)` - Check if date is tomorrow
- **is_this_week**: `DateTimeUtils.is_this_week(dt)` - Check if date is this week
- **is_this_month**: `DateTimeUtils.is_this_month(dt)` - Check if date is this month
- **is_this_year**: `DateTimeUtils.is_this_year(dt)` - Check if date is this year
- **is_weekend**: `DateTimeUtils.is_weekend(dt)` - Check if date is weekend
- **is_weekday**: `DateTimeUtils.is_weekday(dt)` - Check if date is weekday
- **is_leap_year**: `DateTimeUtils.is_leap_year(year)` - Check if year is leap year

**Period Boundaries:**
- **start_of_day**: `DateTimeUtils.start_of_day(dt)` - Get start of day (00:00:00)
- **end_of_day**: `DateTimeUtils.end_of_day(dt)` - Get end of day (23:59:59)
- **start_of_week**: `DateTimeUtils.start_of_week(dt)` - Get start of week (Monday)
- **end_of_week**: `DateTimeUtils.end_of_week(dt)` - Get end of week (Sunday)
- **start_of_month**: `DateTimeUtils.start_of_month(dt)` - Get start of month
- **end_of_month**: `DateTimeUtils.end_of_month(dt)` - Get end of month
- **start_of_year**: `DateTimeUtils.start_of_year(dt)` - Get start of year
- **end_of_year**: `DateTimeUtils.end_of_year(dt)` - Get end of year

**Utility Functions:**
- **get_age**: `DateTimeUtils.get_age(birth_date, today)` - Calculate age
- **get_weekday_name**: `DateTimeUtils.get_weekday_name(dt, locale='en')` - Get weekday name (en/cn/short)
- **get_month_name**: `DateTimeUtils.get_month_name(month, locale='en')` - Get month name (en/cn/short)
- **days_in_month**: `DateTimeUtils.days_in_month(year, month)` - Get days in month
- **relative_time**: `DateTimeUtils.relative_time(dt, now)` - Get relative time description (e.g., "5 minutes ago")
- **format_duration**: `DateTimeUtils.format_duration(seconds)` - Format duration to readable string
- **countdown**: `DateTimeUtils.countdown(target, now)` - Calculate countdown to target time
- **generate_date_range**: `DateTimeUtils.generate_date_range(start, end, step_days)` - Generate date range list

**Convenience Functions:**
- **now**: `now()` - Get current datetime
- **format_datetime**: `format_datetime(dt, fmt)` - Format datetime
- **parse_datetime**: `parse_datetime(date_string, fmt)` - Parse datetime
- **days_between**: `days_between(start, end)` - Calculate days difference
- **is_leap_year**: `is_leap_year(year)` - Check leap year
- **get_age**: `get_age(birth_date)` - Calculate age
- **relative_time**: `relative_time(dt)` - Get relative time

**Features:**
- Zero dependencies, uses only Python standard library (datetime, time, calendar)
- Support for multiple date/time formats (ISO 8601, Chinese, US, compact, etc.)
- Automatic format detection for parsing
- Complete time arithmetic (days, hours, minutes, seconds, months, years)
- Smart month/year boundary handling (e.g., Jan 31 + 1 month = Feb 28/29)
- Relative time descriptions in Chinese (刚刚, 5分钟前, 昨天, etc.)
- Period boundary calculations (day, week, month, year)
- Age calculation with birthday handling
- Countdown functionality
- Date range generation
- 50+ comprehensive unit tests
- 16 practical usage examples
- Production-ready for scheduling, logging, and data processing tasks

Run tests:
```bash
cd Python/datetime_utils
python datetime_utils_test.py
```

Run example:
```bash
cd Python/examples
python datetime_utils_example.py
```

Usage example:
```python
from datetime_utils.mod import DateTimeUtils, now, format_datetime, relative_time

# Get current time
current = DateTimeUtils.now()
print(DateTimeUtils.format(current))  # "2024-03-15 10:30:00"

# Parse and format
dt = DateTimeUtils.parse("2024-03-15 10:30:00")
print(DateTimeUtils.format(dt, DateTimeUtils.FORMAT_CHINESE))  # "2024年03月15日 10时30分00秒"

# Auto-parse multiple formats
result = DateTimeUtils.parse_auto("2024-03-15")  # Works!
result = DateTimeUtils.parse_auto("2024/03/15 10:30:00")  # Works!

# Time arithmetic
future = DateTimeUtils.add_days(dt, 5)
future = DateTimeUtils.add_months(dt, 2)

# Date checks
if DateTimeUtils.is_today(dt):
    print("It's today!")
if DateTimeUtils.is_weekend(dt):
    print("It's weekend!")

# Relative time
dt = now() - timedelta(hours=2)
print(relative_time(dt))  # "2小时前"

# Age calculation
birth = datetime(2000, 1, 1)
age = DateTimeUtils.get_age(birth)
print(f"Age: {age}")

# Countdown
target = now() + timedelta(days=2, hours=5)
countdown = DateTimeUtils.countdown(target)
print(f"{countdown['days']} days remaining")

# Date range
start = DateTimeUtils.parse("2024-03-01")
end = DateTimeUtils.parse("2024-03-07")
dates = DateTimeUtils.generate_date_range(start, end)
for d in dates:
    print(DateTimeUtils.format(d, "%Y-%m-%d"))
```

---

### Kotlin - Base64 Utilities

Location: `Kotlin/base64_utils/mod.kt`

A comprehensive Base64 encoding and decoding utility module for Kotlin with support for standard Base64 and URL-safe Base64 (RFC 4648).

**Encoding Functions:**
- **Encode String**: `Base64Utils.encode(input, charset)` - Encode string to Base64
- **Encode Bytes**: `Base64Utils.encode(data)` - Encode byte array to Base64
- **Encode URL-Safe**: `Base64Utils.encodeUrlSafe(input, charset, padding)` - Encode to URL-safe Base64
- **Encode URL-Safe Bytes**: `Base64Utils.encodeUrlSafe(data, padding)` - Encode bytes to URL-safe Base64

**Decoding Functions:**
- **Decode**: `Base64Utils.decode(base64, charset)` - Decode Base64 to string
- **Decode to Bytes**: `Base64Utils.decodeToBytes(base64)` - Decode Base64 to byte array
- **Decode URL-Safe**: `Base64Utils.decodeUrlSafe(base64Url, charset)` - Decode URL-safe Base64 to string
- **Decode URL-Safe to Bytes**: `Base64Utils.decodeUrlSafeToBytes(base64Url)` - Decode URL-safe Base64 to bytes
- **Safe Decode**: `Base64Utils.decodeOrNull(base64, charset)` - Safe decode, returns null on failure
- **Safe URL-Safe Decode**: `Base64Utils.decodeUrlSafeOrNull(base64Url, charset)` - Safe URL-safe decode

**Format Conversion:**
- **To URL-Safe**: `Base64Utils.toUrlSafe(base64, padding)` - Convert standard Base64 to URL-safe format
- **From URL-Safe**: `Base64Utils.fromUrlSafe(base64Url)` - Convert URL-safe Base64 to standard format

**Validation Functions:**
- **Is Valid**: `Base64Utils.isValid(str)` - Check if string is valid Base64
- **Is Valid URL-Safe**: `Base64Utils.isValidUrlSafe(str)` - Check if string is valid URL-safe Base64

**Utility Functions:**
- **Encoded Length**: `Base64Utils.encodedLength(inputLength, padding)` - Calculate encoded string length
- **Decoded Max Length**: `Base64Utils.decodedMaxLength(base64Length)` - Calculate maximum decoded length

**Extension Functions:**
- **String.toBase64()**: Encode string to Base64
- **String.toBase64UrlSafe(padding)**: Encode string to URL-safe Base64
- **String.fromBase64()**: Decode Base64 string
- **String.fromBase64OrNull()**: Safe decode Base64, returns null on failure
- **String.fromBase64UrlSafe()**: Decode URL-safe Base64 string
- **String.fromBase64UrlSafeOrNull()**: Safe decode URL-safe Base64
- **ByteArray.toBase64()**: Encode byte array to Base64
- **ByteArray.toBase64UrlSafe(padding)**: Encode byte array to URL-safe Base64

**Features:**
- Zero dependencies, uses only Kotlin/Java standard library (java.util.Base64)
- Full UTF-8 support including Unicode characters and emoji
- URL-safe Base64 variant (RFC 4648) with optional padding control
- Binary data support via ByteArray
- Safe decoding methods that return null instead of throwing exceptions
- Complete input validation with descriptive error messages
- Convenient extension functions for idiomatic Kotlin usage
- Thread-safe (all methods are stateless)
- 25+ comprehensive unit tests covering all functionality
- 12 practical usage examples
- Production-ready for data encoding/decoding tasks

Compile and run tests:
```bash
cd Kotlin/base64_utils
kotlinc -include-runtime -d test.jar *.kt && java -jar test.jar
```

Run example:
```bash
cd Kotlin/examples
kotlinc -cp ../base64_utils base64_utils_example.kt && kotlin -cp ../base64_utils:. Base64UtilsExampleKt
```

Usage example:
```kotlin
import base64_utils.Base64Utils
import base64_utils.toBase64
import base64_utils.fromBase64
import base64_utils.toBase64UrlSafe
import base64_utils.fromBase64UrlSafe

// Basic encoding
val encoded = Base64Utils.encode("Hello, World!")
// Returns: "SGVsbG8sIFdvcmxkIQ=="

// Basic decoding
val decoded = Base64Utils.decode("SGVsbG8sIFdvcmxkIQ==")
// Returns: "Hello, World!"

// URL-safe encoding (for URLs/filenames)
val urlSafe = Base64Utils.encodeUrlSafe("user+name/file", padding = false)
// Returns: "dXNlcituYW1lL2ZpbGU"

// Binary data encoding
val data = byteArrayOf(0x00, 0x01, 0x02, 0xFF.toByte())
val binaryEncoded = Base64Utils.encode(data)
// Returns: "AAEC/w=="

// Unicode support (Chinese)
val chinese = Base64Utils.encode("你好世界")
val chineseDecoded = Base64Utils.decode(chinese)
// Returns: "你好世界"

// Extension functions
val extEncoded = "Hello".toBase64()
// Returns: "SGVsbG8="

val extDecoded = "SGVsbG8=".fromBase64()
// Returns: "Hello"

// Safe decoding
val result = Base64Utils.decodeOrNull("Invalid")  // Returns null
val valid = Base64Utils.decodeOrNull("SGVsbG8=")  // Returns "Hello"

// Validation
val isValid = Base64Utils.isValid("SGVsbG8=")     // true
val isInvalid = Base64Utils.isValid("Invalid!")   // false

// Convert between formats
val standard = "SGVsbG8sIFdvcmxkIQ=="
val urlSafeFmt = Base64Utils.toUrlSafe(standard, padding = false)
val backToStandard = Base64Utils.fromUrlSafe(urlSafeFmt)
```

---

### VB - HTTP Utilities

Location: `VB/http_utils/mod.vb`

A comprehensive HTTP client utility module for VB.NET with support for GET, POST, PUT, DELETE, PATCH, HEAD requests, URL manipulation, and request customization.

**HTTP Methods:**
- **GET**: `HttpUtils.Get(url, options)` - Send HTTP GET request
- **POST**: `HttpUtils.Post(url, body, contentType, options)` - Send HTTP POST request
- **POST JSON**: `HttpUtils.PostJson(url, jsonData, options)` - Send JSON POST request
- **POST Form**: `HttpUtils.PostForm(url, formData, options)` - Send form POST request
- **PUT**: `HttpUtils.Put(url, body, contentType, options)` - Send HTTP PUT request
- **DELETE**: `HttpUtils.Delete(url, options)` - Send HTTP DELETE request
- **PATCH**: `HttpUtils.Patch(url, body, contentType, options)` - Send HTTP PATCH request
- **HEAD**: `HttpUtils.Head(url, options)` - Send HTTP HEAD request

**URL Utilities:**
- **URL Encode**: `HttpUtils.UrlEncode(value)` - URL encode a string
- **URL Decode**: `HttpUtils.UrlDecode(value)` - URL decode a string
- **Build Query String**: `HttpUtils.BuildQueryString(parameters)` - Build URL-encoded query string
- **Build URL**: `HttpUtils.BuildUrl(baseUrl, parameters)` - Build URL with query parameters
- **Parse URL**: `HttpUtils.ParseUrl(url)` - Parse URL into components (scheme, host, port, path, query, fragment)
- **Validate URL**: `HttpUtils.IsValidUrl(url)` - Check if string is valid URL
- **Get Domain**: `HttpUtils.GetDomain(url)` - Extract domain from URL
- **Get Path**: `HttpUtils.GetPath(url)` - Extract path from URL
- **Add Query Params**: `HttpUtils.AddQueryParams(url, params)` - Add query parameters to URL

**HTTP Response (HttpResponse class):**
- **Status Code**: `response.StatusCode` - HTTP status code
- **Status Description**: `response.StatusDescription` - HTTP status text
- **Body**: `response.Body` - Response body as string
- **Body Bytes**: `response.BodyBytes` - Response body as byte array
- **Headers**: `response.Headers` - Response headers dictionary
- **Success**: `response.IsSuccess` - True if status 200-299
- **Response Time**: `response.ResponseTime` - Request duration in milliseconds
- **JSON Parse**: `response.Json()` - Parse body as JSON object
- **Is JSON**: `response.IsJson()` - Check if body is valid JSON
- **Get Header**: `response.GetHeader(name)` - Get header value by name

**HTTP Options (HttpOptions class):**
- **Headers**: Custom request headers dictionary
- **Timeout**: Request timeout in milliseconds (default: 30000)
- **Allow Redirect**: Auto-follow redirects (default: True)
- **Max Redirects**: Maximum redirect hops (default: 10)
- **Validate SSL**: SSL certificate verification (default: True)
- **Proxy**: HTTP proxy server address
- **Username/Password**: Basic authentication credentials

**Features:**
- Zero dependencies, uses only .NET standard library (System.Net, System.IO, System.Text)
- Supports .NET Framework 4.5+ / .NET Core / .NET 5+
- Full HTTP method support: GET, POST, PUT, DELETE, PATCH, HEAD
- Automatic JSON and form data encoding
- Complete URL manipulation utilities
- Custom headers and timeout configuration
- Response time tracking
- SSL/TLS certificate verification control
- HTTP proxy support
- Basic authentication support
- Response success status checking
- Built-in JSON validation and parsing
- Complete test suite with 30+ test cases
- 9 comprehensive usage examples
- Production-ready for REST API clients

Compile and run tests:
```bash
cd VB/http_utils
vbc http_utils_test.vb mod.vb /r:System.Web.Extensions.dll /out:http_test.exe
http_test.exe
```

Run example:
```bash
cd VB/examples
vbc http_utils_example.vb ../http_utils/mod.vb /r:System.Web.Extensions.dll /out:http_example.exe
http_example.exe
```

Usage example:
```vb
Imports AllToolkit

' Simple GET request
Dim response As HttpResponse = HttpUtils.Get("https://api.example.com/users")
If response.IsSuccess Then
    Console.WriteLine(response.Body)
End If

' POST JSON data
Dim data As New Dictionary(Of String, Object)()
data.Add("name", "John")
data.Add("email", "john@example.com")
Dim response As HttpResponse = HttpUtils.PostJson("https://api.example.com/users", data)

' POST Form data
Dim formData As New Dictionary(Of String, String)()
formData.Add("username", "admin")
formData.Add("password", "secret")
Dim response As HttpResponse = HttpUtils.PostForm("https://api.example.com/login", formData)

' URL building
Dim params As New Dictionary(Of String, String)()
params.Add("q", "hello world")
params.Add("page", "1")
Dim url As String = HttpUtils.BuildUrl("https://api.example.com/search", params)
' Result: 'https://api.example.com/search?q=hello%20world&page=1'

' URL parsing
Dim parts As Dictionary(Of String, String) = HttpUtils.ParseUrl("https://api.example.com:8080/v1/users")
' parts("host") = "api.example.com"
' parts("port") = "8080"

' Custom options
Dim options As New HttpOptions()
options.Timeout = 60000
options.AddHeader("Authorization", "Bearer token123")
Dim response As HttpResponse = HttpUtils.Get("https://api.example.com/protected", options)

' URL validation
Dim isValid As Boolean = HttpUtils.IsValidUrl("https://example.com")  ' True

' URL encoding
Dim encoded As String = HttpUtils.UrlEncode("hello world")  ' "hello%20world"
Dim decoded As String = HttpUtils.UrlDecode("hello%20world")  ' "hello world"
```

---

### C# - Base64 Utilities

Location: `C#/base64_utils/mod.cs`

A comprehensive Base64 encoding and decoding utility module for C# with support for standard Base64 and URL-safe Base64 (RFC 4648).

**Encoding Functions:**
- **Encode**: `Base64Utils.Encode(input)` - Encode string to Base64
- **Encode (bytes)**: `Base64Utils.Encode(data)` - Encode byte array to Base64
- **EncodeUrlSafe**: `Base64Utils.EncodeUrlSafe(input, encoding, padding)` - Encode to URL-safe Base64
- **EncodeUrlSafe (bytes)**: `Base64Utils.EncodeUrlSafe(data, padding)` - Encode bytes to URL-safe Base64

**Decoding Functions:**
- **Decode**: `Base64Utils.Decode(base64, encoding)` - Decode Base64 to string
- **DecodeToBytes**: `Base64Utils.DecodeToBytes(base64)` - Decode Base64 to byte array
- **DecodeUrlSafe**: `Base64Utils.DecodeUrlSafe(base64Url, encoding)` - Decode URL-safe Base64 to string
- **DecodeUrlSafeToBytes**: `Base64Utils.DecodeUrlSafeToBytes(base64Url)` - Decode URL-safe Base64 to bytes
- **TryDecode**: `Base64Utils.TryDecode(base64, encoding)` - Safe decode, returns null on failure
- **TryDecodeToBytes**: `Base64Utils.TryDecodeToBytes(base64)` - Safe decode to bytes, returns null on failure

**Format Conversion:**
- **ToUrlSafe**: `Base64Utils.ToUrlSafe(base64, padding)` - Convert standard Base64 to URL-safe format
- **FromUrlSafe**: `Base64Utils.FromUrlSafe(base64Url)` - Convert URL-safe Base64 to standard format

**Validation Functions:**
- **IsValid**: `Base64Utils.IsValid(base64)` - Check if string is valid Base64
- **IsValidUrlSafe**: `Base64Utils.IsValidUrlSafe(base64Url)` - Check if string is valid URL-safe Base64

**Utility Functions:**
- **GetEncodedLength**: `Base64Utils.GetEncodedLength(inputLength, padding)` - Calculate encoded string length
- **GetDecodedMaxLength**: `Base64Utils.GetDecodedMaxLength(base64Length)` - Calculate maximum decoded length

**Features:**
- Zero dependencies, uses only .NET standard library (System, System.Text)
- Supports .NET Framework 4.5+ / .NET Core / .NET 5+
- Full UTF-8 support including Unicode characters and emoji
- URL-safe Base64 variant (RFC 4648) with optional padding
- Byte array encoding/decoding for binary data
- Safe decoding methods that return null instead of throwing exceptions
- Complete input validation with descriptive error messages
- Thread-safe (all methods are static and stateless)
- 25+ comprehensive unit tests covering all functionality
- 6 practical usage examples
- Production-ready for data encoding/decoding tasks

Compile and run tests:
```bash
cd C#/base64_utils
dotnet build
dotnet run --project base64_utils_test.cs
```

Run example:
```bash
cd C#/examples
dotnet run base64_utils_example.cs
```

Usage example:
```csharp
using AllToolkit;

// Basic encoding
string encoded = Base64Utils.Encode("Hello, World!");
// Returns: "SGVsbG8sIFdvcmxkIQ=="

// Basic decoding
string decoded = Base64Utils.Decode("SGVsbG8sIFdvcmxkIQ==");
// Returns: "Hello, World!"

// URL-safe encoding (for URLs/filenames)
string urlSafe = Base64Utils.EncodeUrlSafe("user+name/file", padding: false);
// Returns: "dXNlcituYW1lL2ZpbGU"

// Binary data encoding
byte[] data = new byte[] { 0x00, 0x01, 0x02, 0xFF };
string binaryEncoded = Base64Utils.Encode(data);
// Returns: "AAEC/w=="

// Validation
bool valid = Base64Utils.IsValid("SGVsbG8=");  // true
bool invalid = Base64Utils.IsValid("Invalid!"); // false

// Safe decoding
string result = Base64Utils.TryDecode("Invalid");  // Returns null
string success = Base64Utils.TryDecode("SGVsbG8=");  // Returns "Hello"

// Length calculation
int encodedLen = Base64Utils.GetEncodedLength(100, true);  // 136
int maxDecoded = Base64Utils.GetDecodedMaxLength(136);     // 102
```

---

### Ruby - Number Utilities

Location: `Ruby/number_utils/mod.rb`

A comprehensive number utility module for Ruby providing formatting, conversion, mathematical operations, and statistical functions.

**Formatting Functions:**
- **format**: `format(number, separator: ',', decimal: '.', precision: nil)` - Format with thousands separator
- **currency**: `currency(number, symbol: '$', precision: 2)` - Format as currency
- **percentage**: `percentage(number, precision: 0, symbol: true)` - Format as percentage
- **compact**: `compact(number, precision: 1)` - Compact notation (K, M, B, T)
- **ordinal**: `ordinal(number)` - Convert to ordinal (1st, 2nd, 3rd)
- **to_words**: `to_words(number)` - Convert number to English words

**Conversion Functions:**
- **to_roman**: `to_roman(number)` - Integer to Roman numeral (1-3999)
- **from_roman**: `from_roman(roman)` - Roman numeral to integer
- **to_binary**: `to_binary(number, prefix: false, min_width: nil)` - Convert to binary
- **to_hex**: `to_hex(number, prefix: false, uppercase: false, min_width: nil)` - Convert to hexadecimal
- **to_octal**: `to_octal(number, prefix: false)` - Convert to octal

**Mathematical Functions:**
- **clamp**: `clamp(number, min, max)` - Clamp value between min and max
- **lerp**: `lerp(start, finish, t)` - Linear interpolation
- **map_range**: `map_range(value, in_min, in_max, out_min, out_max)` - Map between ranges
- **approx_equal**: `approx_equal?(a, b, epsilon: 1e-9)` - Approximate equality check
- **round_to_multiple**: `round_to_multiple(number, multiple)` - Round to nearest multiple
- **round_to_places**: `round_to_places(number, places)` - Round to decimal places

**Statistical Functions:**
- **mean**: `mean(numbers)` - Calculate arithmetic mean
- **median**: `median(numbers)` - Calculate median value
- **mode**: `mode(numbers)` - Calculate mode (most frequent)
- **std_dev**: `std_dev(numbers, sample: false)` - Calculate standard deviation
- **sum_of_squares**: `sum_of_squares(numbers)` - Sum of squares
- **range**: `range(numbers)` - Range (max - min)

**Validation Functions:**
- **number?**: `number?(value)` - Check if numeric
- **integer?**: `integer?(value)` - Check if integer
- **float?**: `float?(value)` - Check if float
- **even?**: `even?(number)` - Check if even
- **odd?**: `odd?(number)` - Check if odd
- **positive?**: `positive?(number)` - Check if positive
- **negative?**: `negative?(number)` - Check if negative
- **zero?**: `zero?(number)` - Check if zero
- **between?**: `between?(number, min, max)` - Check if in range
- **prime?**: `prime?(number)` - Check if prime
- **perfect_square?**: `perfect_square?(number)` - Check if perfect square

**Parsing Functions:**
- **parse**: `parse(str, default: nil)` - Parse string to number
- **parse_int**: `parse_int(str, default: nil, base: 10)` - Parse to integer
- **parse_float**: `parse_float(str, default: nil)` - Parse to float

**Utility Functions:**
- **gcd**: `gcd(a, b)` - Greatest common divisor
- **lcm**: `lcm(a, b)` - Least common multiple
- **factorial**: `factorial(n)` - Calculate factorial
- **fibonacci**: `fibonacci(n)` - Calculate Fibonacci number
- **sqrt**: `sqrt(number)` - Square root
- **nth_root**: `nth_root(number, n)` - Nth root
- **to_radians**: `to_radians(degrees)` - Degrees to radians
- **to_degrees**: `to_degrees(radians)` - Radians to degrees
- **normalize_angle**: `normalize_angle(degrees)` - Normalize to 0-360
- **sum_of_digits**: `sum_of_digits(number)` - Sum of digits
- **reverse_digits**: `reverse_digits(number)` - Reverse digits
- **palindrome?**: `palindrome?(number)` - Check if palindrome

**Random Generation:**
- **random**: `random(min: 0, max: 1)` - Random float in range
- **random_int**: `random_int(min:, max:)` - Random integer in range
- **random_normal**: `random_normal(mean: 0, std_dev: 1)` - Normal distribution

**Convenience Methods:**
- **fmt**: Alias for format
- **cur**: Alias for currency
- **pct**: Alias for percentage

**Features:**
- Zero dependencies, uses only Ruby standard library
- Complete number formatting with internationalization support
- Roman numeral conversion (1-3999)
- Binary, hexadecimal, and octal conversions
- Statistical functions for data analysis
- Prime number and perfect square detection
- Number parsing with default values
- Random number generation with normal distribution
- Comprehensive test suite with 50+ test cases
- 15 practical usage examples
- Production-ready for financial and scientific applications

Run tests:
```bash
cd Ruby/number_utils
ruby number_utils_test.rb
```

Run example:
```bash
cd Ruby/examples
ruby number_utils_example.rb
```

Usage example:
```ruby
require_relative 'Ruby/number_utils/mod'

# Formatting
NumberUtils.format(1234567.89)              # => "1,234,567.89"
NumberUtils.currency(1234.5)                # => "$1,234.50"
NumberUtils.percentage(0.1567, precision: 2)  # => "15.67%"
NumberUtils.compact(1500000)                # => "1.5M"
NumberUtils.ordinal(21)                     # => "21st"
NumberUtils.to_words(123)                   # => "one hundred twenty-three"

# Conversion
NumberUtils.to_roman(2024)                  # => "MMXXIV"
NumberUtils.from_roman("MMXXIV")            # => 2024
NumberUtils.to_binary(255)                  # => "11111111"
NumberUtils.to_hex(255, uppercase: true)    # => "FF"

# Mathematical
NumberUtils.clamp(10, 0, 5)                 # => 5
NumberUtils.lerp(0, 100, 0.5)               # => 50.0
NumberUtils.map_range(5, 0, 10, 0, 100)     # => 50.0

# Statistical
NumberUtils.mean([1, 2, 3, 4, 5])           # => 3.0
NumberUtils.median([1, 2, 3, 4, 5])         # => 3
NumberUtils.std_dev([1, 2, 3, 4, 5])        # => ~1.414

# Validation
NumberUtils.prime?(7)                       # => true
NumberUtils.perfect_square?(16)             # => true
NumberUtils.between?(3, 1, 5)               # => true

# Parsing
NumberUtils.parse("1,234.56")               # => 1234.56
NumberUtils.parse_int("42")                 # => 42
NumberUtils.parse_float("3.14")             # => 3.14

# Utility
NumberUtils.gcd(24, 36)                     # => 12
NumberUtils.factorial(5)                    # => 120
NumberUtils.fibonacci(10)                   # => 55
NumberUtils.palindrome?(121)                # => true
```

---

### Perl - File Utilities

Location: `Perl/file_utils/mod.pl`

A comprehensive file utility module for Perl providing common file operations with zero external dependencies.

**File Operations:**
- **read_file**: `read_file(filepath, encoding)` - Read entire file as string
- **read_file_lines**: `read_file_lines(filepath, encoding)` - Read file as array of lines
- **read_file_binary**: `read_file_binary(filepath)` - Read file as binary data
- **write_file**: `write_file(filepath, content, encoding)` - Write string to file
- **write_file_binary**: `write_file_binary(filepath, data)` - Write binary data to file
- **append_file**: `append_file(filepath, content, encoding)` - Append content to file

**File Checks:**
- **file_exists**: `file_exists(filepath)` - Check if file exists
- **dir_exists**: `dir_exists(dirpath)` - Check if directory exists
- **file_size**: `file_size(filepath)` - Get file size in bytes
- **file_mtime**: `file_mtime(filepath)` - Get modification time (Unix timestamp)
- **file_atime**: `file_atime(filepath)` - Get access time
- **file_ctime**: `file_ctime(filepath)` - Get creation/change time
- **file_mode**: `file_mode(filepath)` - Get file permissions
- **is_readable**: `is_readable(filepath)` - Check if readable
- **is_writable**: `is_writable(filepath)` - Check if writable
- **is_executable**: `is_executable(filepath)` - Check if executable
- **is_file**: `is_file(filepath)` - Check if regular file
- **is_dir**: `is_dir(filepath)` - Check if directory
- **is_symlink**: `is_symlink(filepath)` - Check if symbolic link

**Directory Operations:**
- **list_files**: `list_files(dirpath, pattern)` - List files in directory
- **list_dirs**: `list_dirs(dirpath)` - List subdirectories
- **list_all**: `list_all(dirpath)` - List all entries
- **ensure_dir**: `ensure_dir(dirpath, mode)` - Create directory recursively
- **remove_file**: `remove_file(filepath)` - Delete file
- **remove_dir**: `remove_dir(dirpath)` - Remove empty directory
- **remove_dir_recursive**: `remove_dir_recursive(dirpath)` - Remove directory and contents

**File Manipulation:**
- **copy_file**: `copy_file(src, dst)` - Copy file
- **move_file**: `move_file(src, dst)` - Move/rename file
- **touch**: `touch(filepath)` - Create file or update timestamp
- **truncate_file**: `truncate_file(filepath, size)` - Truncate file to size

**Path Utilities:**
- **get_extension**: `get_extension(filepath)` - Get file extension
- **get_basename**: `get_basename(filepath)` - Get filename without extension
- **get_dirname**: `get_dirname(filepath)` - Get directory path
- **join_path**: `join_path(parts...)` - Join path components
- **normalize_path**: `normalize_path(filepath)` - Normalize path separators

**Utility Functions:**
- **get_temp_dir**: `get_temp_dir()` - Get system temp directory
- **get_temp_file**: `get_temp_file(prefix, suffix)` - Generate temp file path
- **format_size**: `format_size(bytes)` - Format bytes to human readable
- **find_files**: `find_files(dirpath, pattern)` - Find files recursively

**Features:**
- Zero dependencies, uses only Perl standard library
- Full UTF-8 support with configurable encoding
- Binary file support
- Recursive directory operations
- Path manipulation utilities
- Human-readable file size formatting
- 30+ comprehensive test cases
- 10 practical usage examples
- Production-ready for file management tasks

Run tests:
```bash
cd Perl/file_utils
perl file_utils_test.pl
```

Run example:
```bash
cd Perl/examples
perl file_utils_example.pl
```

Usage example:
```perl
use lib 'Perl/file_utils';
use mod;

# Read and write files
my $content = mod::read_file('/path/to/file.txt');
mod::write_file('/path/to/output.txt', 'Hello, World!');

# Check file properties
if (mod::file_exists('/path/to/file.txt')) {
    my $size = mod::file_size('/path/to/file.txt');
    print "File size: " . mod::format_size($size) . "\n";
}

# Directory operations
mod::ensure_dir('/path/to/new/directory');
my $files = mod::list_files('/path/to/directory');
for my $file (@$files) {
    print "Found: $file\n";
}

# Path manipulation
my $path = mod::join_path('home', 'user', 'documents');
my $ext = mod::get_extension('file.txt');  # 'txt'
my $base = mod::get_basename('/path/to/file.txt');  # 'file'
my $dir = mod::get_dirname('/path/to/file.txt');  # '/path/to'

# Copy and move files
mod::copy_file('/source/file.txt', '/dest/file.txt');
mod::move_file('/old/name.txt', '/new/name.txt');

# Find files recursively
my $found = mod::find_files('/search/path', '\.pl$');
for my $file (@$found) {
    print "Found Perl file: $file\n";
}

# Temporary files
my $temp = mod::get_temp_file('prefix', '.tmp');
mod::write_file($temp, 'temporary data');
```

---

### MATLAB - JSON Utilities

Location: `MATLAB/json_utils/mod.m`

A zero-dependency JSON parser and generator for MATLAB. Supports parsing JSON strings to MATLAB structures/cell arrays, and generating JSON strings from MATLAB data types.

**Parsing Functions:**
- **parse**: `utils.parse(jsonString)` - Parse JSON string into MATLAB data structure
- **parseOrNull**: `utils.parseOrNull(jsonString)` - Parse safely, return empty on error
- **parseFile**: `utils.parseFile(filename)` - Parse JSON from file

**Encoding Functions:**
- **encode**: `utils.encode(data)` - Encode MATLAB data to compact JSON string
- **encodePretty**: `utils.encodePretty(data, indent)` - Encode to pretty-printed JSON

**Validation Functions:**
- **isValid**: `utils.isValid(jsonString)` - Check if string is valid JSON
- **isValidFile**: `utils.isValidFile(filename)` - Check if file contains valid JSON

**Utility Functions:**
- **save**: `utils.save(filename, data, pretty)` - Save data to JSON file
- **get**: `utils.get(data, key, defaultValue)` - Safely get value with default
- **getPath**: `utils.getPath(data, path, defaultValue)` - Get nested value using dot notation
- **minify**: `utils.minify(jsonString)` - Remove unnecessary whitespace

**Static Methods:**
- **quickParse**: `json_utils.mod.quickParse(jsonString)` - Static parse without instance
- **quickEncode**: `json_utils.mod.quickEncode(data, pretty)` - Static encode without instance

**Features:**
- Zero dependencies, uses only MATLAB standard library
- Complete JSON support: null, boolean, number, string, array, object
- Nested object and array support
- Unicode escape sequence support (\uXXXX)
- Type-safe access with default values
- Pretty printing with customizable indentation
- File I/O operations
- Safe parsing with graceful error handling
- 25 comprehensive unit tests
- 13 practical usage examples
- Production-ready for configuration files and data exchange

Run tests:
```matlab
cd MATLAB/json_utils
json_utils_test()
```

Run example:
```matlab
cd MATLAB/examples
run('json_utils_example.m')
```

Usage example:
```matlab
% Create instance
utils = json_utils.mod();

% Parse JSON
jsonStr = '{"name": "John", "age": 30, "city": "New York"}';
data = utils.parse(jsonStr);
fprintf('Name: %s, Age: %d\n', data.name, data.age);

% Parse nested JSON
nested = utils.parse('{\n  "user": {\n    "profile": {\n      "name": "Alice"\n    }\n  }\n}');
fprintf('User name: %s\n', nested.user.profile.name);

% Encode to JSON
person = struct('name', 'Bob', 'age', 25);
json = utils.encode(person);
% Returns: '{"name":"Bob","age":25}'

% Pretty print
pretty = utils.encodePretty(person);
% Returns formatted JSON with indentation

% Safe access with defaults
config = utils.parse('{"host": "localhost"}');
host = utils.get(config, 'host', '127.0.0.1');     % "localhost"
port = utils.get(config, 'port', 8080);            % 8080 (default)

% Nested path access
data = utils.parse('{"db": {"conn": {"host": "db.example.com"}}}');
host = utils.getPath(data, 'db.conn.host', 'localhost');

% Validation
isValid = utils.isValid('{"valid": true}');        % true
isValid = utils.isValid('not json');               % false

% Safe parsing
data = utils.parseOrNull('invalid');               % Returns []
data = utils.parseOrNull('{"valid": true}');       % Returns struct

% Minify JSON
compact = utils.minify('{ "a": 1, \n  "b": 2 }');  % '{"a":1,"b":2}'

% Static methods (no instance needed)
data = json_utils.mod.quickParse('{"x": 1}');
json = json_utils.mod.quickEncode(struct('y', 2), true);
```

---

### Ruby - Template Engine Utilities

Location: `Ruby/template_utils/mod.rb`

A lightweight, zero-dependency template engine with variable interpolation, conditionals, loops, and filters.

**Core Classes:**
- **Context**: Template rendering context with data storage and partial template support
  - `get(key)` - Get value from context
  - `has?(key)` - Check if key exists
  - `nest(local_data)` - Create nested context for loops
  - `partial(name)` - Get partial template

- **Template**: Main template parser and renderer
  - `render(context)` - Render template with given context
  - Supports variable interpolation, conditionals, loops, includes

- **Filters**: Built-in text and data filters
  - String: `upcase`, `downcase`, `capitalize`, `titleize`, `strip`, `reverse`
  - HTML: `escape_html`, `strip_html`
  - Array: `join`, `split`, `first`, `last`, `size`, `reverse`
  - Number: `round`, `number_with_delimiter`
  - Utility: `truncate`, `default`, `replace`, `url_encode`

**Template Syntax:**
- Variable interpolation: `{{ variable }}`
- Filters: `{{ variable | upcase }}`, `{{ var | default: "N/A" }}`
- Conditionals: `{% if condition %} ... {% else %} ... {% endif %}`
- Loops: `{% for item in items %} ... {% endfor %}`
- Includes: `{% include "partial_name" %}`
- Comments: `{# This is a comment #}`

**Condition Operators:**
- Equality: `==`, `!=`
- Comparison: `>`, `<`, `>=`, `<=`
- Negation: `not condition`
- Truthy: `{% if variable %}` (checks for non-nil, non-empty)

**Module Functions:**
- **render**: `TemplateUtils.render(template, context, partials)` - Render template string
- **template**: `TemplateUtils.template(source)` - Create Template object
- **register_filter**: `TemplateUtils.register_filter(name) { |value, *args| ... }` - Add custom filter
- **valid?**: `TemplateUtils.valid?(template)` - Check if template is valid

**Convenience Method:**
- `render_template(template, context, partials)` - Top-level shortcut

**Features:**
- Zero dependencies, uses only Ruby standard library
- Full Unicode support
- Nested object access: `{{ user.name }}`
- Custom filter registration
- Partial template support for reusable components
- Comprehensive error handling with custom exception classes
- 25+ built-in filters for common transformations
- 8 comprehensive test categories with 40+ test cases
- 10 practical usage examples including email templates
- Production-ready for dynamic content generation

Run tests:
```bash
cd Ruby/template_utils
ruby template_utils_test.rb
```

Run example:
```bash
cd Ruby/examples
ruby template_utils_example.rb
```

Usage example:
```ruby
require_relative 'Ruby/template_utils/mod'

# Basic variable interpolation
template = "Hello, {{ name | upcase }}!"
result = AllToolkit::TemplateUtils.render(template, { name: "world" })
# => "Hello, WORLD!"

# Conditionals
template = <<~TMPL
  {% if user %}
    Hello, {{ user }}!
  {% else %}
    Welcome, guest!
  {% endif %}
TMPL
result = AllToolkit::TemplateUtils.render(template, { user: "Alice" })

# Loops
template = "{% for item in items %}{{ item }}{% endfor %}"
result = AllToolkit::TemplateUtils.render(template, { items: ["a", "b", "c"] })
# => "abc"

# Filters
template = "{{ price | round: 2 }} - {{ items | join: ', ' }}"
result = AllToolkit::TemplateUtils.render(template, { 
  price: 19.999, 
  items: ["red", "green", "blue"] 
})
# => "20.0 - red, green, blue"

# Partials
partials = { "header" => "<h1>{{ title }}</h1>" }
template = "{% include 'header' %}<p>Content</p>"
result = AllToolkit::TemplateUtils.render(template, { title: "Page" }, partials)
# => "<h1>Page</h1><p>Content</p>"

# Custom filters
AllToolkit::TemplateUtils.register_filter(:double) { |v| v.to_f * 2 }
template = "{{ num | double }}"
result = AllToolkit::TemplateUtils.render(template, { num: 21 })
# => "42.0"
```

---

## 🧪 最新测试更新 (2025-04-05)

### Go - INI Utilities 测试套件

Location: `Go/ini_utils/ini_utils_test.go`

新增测试覆盖:
- **New() 测试**: 创建空 IniFile 对象
- **Parse() 测试**: 解析空字符串、简单键值、带节、带注释、带空行
- **Get() 测试**: 全局键、节键、默认值、不存在键
- **GetInt() 测试**: 有效整数、无效整数返回默认值
- **GetInt64() 测试**: 大整数支持
- **GetFloat64() 测试**: 浮点数解析
- **GetBool() 测试**: true/false 多种格式支持
- **Set() 测试**: 设置全局键、节键、更新现有键
- **SetInt/SetFloat64/SetBool() 测试**: 类型安全设置
- **HasSection() 测试**: 节存在性检查
- **HasKey() 测试**: 键存在性检查
- **DeleteKey() 测试**: 删除键
- **DeleteSection() 测试**: 删除节
- **LoadFile/SaveToFile() 测试**: 文件读写
- **ToString/ToPrettyString() 测试**: 字符串输出
- **GetSections/GetKeys() 测试**: 获取节和键列表

运行测试: `cd Go/ini_utils && go test -v`

---

### Rust - String Utilities 测试套件

Location: `Rust/string_utils/string_utils_test.rs`

新增测试覆盖:
- **truncate() 测试**: 基本截断、Unicode 字符、边界值
- **slugify() 测试**: 基本转换、特殊字符、空字符串
- **count_words() 测试**: 单词计数、多空格、标点符号
- **is_valid_email() 测试**: 有效/无效邮箱格式
- **reverse_graphemes() 测试**: ASCII、Unicode 反转
- **pad() 测试**: 左填充、右填充、边界值

运行测试: `cd Rust/string_utils && rustc --test string_utils_test.rs -o test && ./test`

---

### Rust - Math Utilities 测试套件

Location: `Rust/math_utils/math_utils_test.rs`

新增测试覆盖:
- **clamp() 测试**: f64/i32 边界限制
- **lerp() 测试**: 线性插值
- **map_range() 测试**: 范围映射、边界情况
- **approx_eq() 测试**: 近似相等比较
- **round_to() 测试**: 指定小数位四舍五入
- **mean() 测试**: 平均值计算
- **median() 测试**: 中位数计算（奇数/偶数）
- **min_max() 测试**: 最小最大值
- **std_dev() 测试**: 标准差计算
- **factorial() 测试**: 阶乘计算
- **is_prime() 测试**: 质数判断
- **gcd() 测试**: 最大公约数
- **lcm() 测试**: 最小公倍数
- **to_radians/to_degrees() 测试**: 角度转换
- **normalize_angle_360/180() 测试**: 角度归一化
- **distance_2d/3d() 测试**: 距离计算
- **format_with_commas() 测试**: 千位分隔符格式化

运行测试: `cd Rust/math_utils && rustc --test math_utils_test.rs -o test && ./test`

---

## 📦 Latest Addition

### Ruby - Archive Utilities

Location: `Ruby/archive_utils/mod.rb`

A comprehensive file archiving and compression utility module for Ruby providing ZIP and TAR archive creation, extraction, and management with zero external dependencies.

**ZIP Archive Operations:**
- **create_zip**: `ArchiveUtils.create_zip(zipfile_path, sources, options)` - Create ZIP archive from files/directories
  - Supports compression level control (0-9)
  - Exclude patterns support
  - Preserve or flatten directory structure
  - Base directory for relative paths
- **extract_zip**: `ArchiveUtils.extract_zip(zipfile_path, destination, options)` - Extract ZIP archive
  - Password support for encrypted entries
  - Selective extraction with patterns
  - Overwrite control
- **list_zip**: `ArchiveUtils.list_zip(zipfile_path)` - List ZIP contents
- **zip_stats**: `ArchiveUtils.zip_stats(zipfile_path)` - Get archive statistics
- **valid_zip?**: `ArchiveUtils.valid_zip?(zipfile_path)` - Validate ZIP integrity
- **add_to_zip_archive**: `ArchiveUtils.add_to_zip_archive(zipfile_path, sources, options)` - Add to existing ZIP

**TAR Archive Operations:**
- **create_tar**: `ArchiveUtils.create_tar(tarfile_path, sources, options)` - Create TAR archive
  - Automatic gzip compression for .tar.gz/.tgz files
  - Exclude patterns support
- **extract_tar**: `ArchiveUtils.extract_tar(tarfile_path, destination, options)` - Extract TAR archive
  - Supports both plain .tar and compressed .tar.gz
- **list_tar**: `ArchiveUtils.list_tar(tarfile_path)` - List TAR contents
- **tar_stats**: `ArchiveUtils.tar_stats(tarfile_path)` - Get TAR statistics

**Utility Functions:**
- **extract**: `ArchiveUtils.extract(archive_path, destination, options)` - Auto-detect format and extract
- **list**: `ArchiveUtils.list(archive_path)` - Auto-detect format and list
- **stats**: `ArchiveUtils.stats(archive_path)` - Auto-detect format and get statistics
- **gzip_file**: `ArchiveUtils.gzip_file(source_path, dest_path)` - Compress single file with gzip
- **gunzip_file**: `ArchiveUtils.gunzip_file(source_path, dest_path)` - Decompress gzip file

**ArchiveEntry Class:**
- Properties: `name`, `size`, `compressed_size`, `mtime`, `is_directory`
- Method: `compression_ratio` - Calculate compression percentage

**ArchiveStats Class:**
- Properties: `entry_count`, `total_size`, `total_compressed_size`, `compression_ratio`

**Features:**
- Zero dependencies, uses only Ruby standard library (zip, rubygems/package, zlib)
- Full ZIP format support with compression control
- TAR and compressed TAR (.tar.gz, .tgz) support
- Archive integrity validation
- Statistics and compression ratio calculation
- Pattern-based file exclusion
- Directory structure preservation options
- 15+ comprehensive unit tests
- 16 practical usage examples
- Production-ready for backup and deployment tasks

Run tests:
```bash
cd Ruby/archive_utils
ruby archive_utils_test.rb
```

Run example:
```bash
cd Ruby/examples
ruby archive_utils_example.rb
```

Usage example:
```ruby
require_relative 'Ruby/archive_utils/mod'

# Create a ZIP archive
ArchiveUtils.create_zip('backup.zip', ['documents/', 'photos/'])

# Create with compression options
ArchiveUtils.create_zip('archive.zip', ['files/'], 
  compression: Zlib::BEST_COMPRESSION,
  exclude: ['*.tmp', '*.log']
)

# Extract ZIP
extracted = ArchiveUtils.extract_zip('backup.zip', 'output/')
puts "Extracted #{extracted.length} files"

# List contents
entries = ArchiveUtils.list_zip('backup.zip')
entries.each { |e| puts "#{e.name} (#{e.size} bytes)" }

# Get statistics
stats = ArchiveUtils.zip_stats('backup.zip')
puts "Compression ratio: #{stats.compression_ratio.round(2)}%"

# Create compressed TAR
ArchiveUtils.create_tar('backup.tar.gz', ['documents/'], gzip: true)

# Auto-extract (detects format)
ArchiveUtils.extract('backup.tar.gz', 'output/')
ArchiveUtils.extract('backup.zip', 'output/')

# Gzip single file
ArchiveUtils.gzip_file('document.txt', 'document.txt.gz')
ArchiveUtils.gunzip_file('document.txt.gz', 'document.txt')
```

---

## 📦 Latest Addition

### ArkTS - String Utilities

Location: `ArkTS/string_utils/mod.ets`

A comprehensive string manipulation utility module for ArkTS/HarmonyOS providing common string operations with zero dependencies.

**Empty/Blank Checks:**
- **isBlank**: `isBlank(str)` - Check if string is null, undefined, empty, or whitespace only
- **isNotBlank**: `isNotBlank(str)` - Check if string has content
- **isEmpty**: `isEmpty(str)` - Check if string is empty (length === 0)

**Trimming and Whitespace:**
- **trim**: `trim(str)` - Remove leading and trailing whitespace
- **trimLeft**: `trimLeft(str)` - Remove leading whitespace
- **trimRight**: `trimRight(str)` - Remove trailing whitespace
- **removeWhitespace**: `removeWhitespace(str)` - Remove all whitespace
- **normalizeWhitespace**: `normalizeWhitespace(str)` - Collapse multiple spaces to single space

**Case Conversion:**
- **toLowerCase**: `toLowerCase(str)` - Convert to lowercase
- **toUpperCase**: `toUpperCase(str)` - Convert to uppercase
- **capitalize**: `capitalize(str)` - Capitalize first character
- **uncapitalize**: `uncapitalize(str)` - Uncapitalize first character
- **toTitleCase**: `toTitleCase(str)` - Convert to Title Case
- **toCamelCase**: `toCamelCase(str)` - Convert to camelCase
- **toPascalCase**: `toPascalCase(str)` - Convert to PascalCase
- **toSnakeCase**: `toSnakeCase(str)` - Convert to snake_case
- **toKebabCase**: `toKebabCase(str)` - Convert to kebab-case

**Substring Operations:**
- **truncate**: `truncate(str, maxLength, suffix?)` - Truncate string with ellipsis
- **substringBetween**: `substringBetween(str, open, close)` - Extract substring between markers
- **substringAfter**: `substringAfter(str, separator)` - Extract after first separator
- **substringBefore**: `substringBefore(str, separator)` - Extract before first separator
- **substringAfterLast**: `substringAfterLast(str, separator)` - Extract after last separator
- **substringBeforeLast**: `substringBeforeLast(str, separator)` - Extract before last separator

**Prefix/Suffix Operations:**
- **startsWith**: `startsWith(str, prefix, ignoreCase?)` - Check if string starts with prefix
- **endsWith**: `endsWith(str, suffix, ignoreCase?)` - Check if string ends with suffix
- **removePrefix**: `removePrefix(str, prefix)` - Remove prefix if present
- **removeSuffix**: `removeSuffix(str, suffix)` - Remove suffix if present

**Validation:**
- **isValidEmail**: `isValidEmail(str)` - Validate email format
- **isValidUrl**: `isValidUrl(str)` - Validate URL format
- **isNumeric**: `isNumeric(str)` - Check if numeric
- **isInteger**: `isInteger(str)` - Check if integer
- **isAlpha**: `isAlpha(str)` - Check if alphabetic
- **isAlphanumeric**: `isAlphanumeric(str)` - Check if alphanumeric

**Padding and Alignment:**
- **padLeft**: `padLeft(str, length, padChar?)` - Pad string on left
- **padRight**: `padRight(str, length, padChar?)` - Pad string on right
- **center**: `center(str, length, padChar?)` - Center string with padding

**Search and Replace:**
- **contains**: `contains(str, search, ignoreCase?)` - Check if string contains substring
- **countMatches**: `countMatches(str, search)` - Count occurrences of substring
- **replaceAll**: `replaceAll(str, search, replacement)` - Replace all occurrences

**Split and Join:**
- **split**: `split(str, separator, limit?)` - Split string into array
- **lines**: `lines(str, trimEmpty?)` - Split string by newlines
- **join**: `join(array, separator?)` - Join array elements

**Encoding/Decoding:**
- **base64Encode**: `base64Encode(str)` - Encode string to Base64
- **base64Decode**: `base64Decode(str)` - Decode Base64 string
- **urlEncode**: `urlEncode(str)` - URL encode string
- **urlDecode**: `urlDecode(str)` - URL decode string

**Random Generation:**
- **randomString**: `randomString(length, chars?)` - Generate random string
- **randomAlphanumeric**: `randomAlphanumeric(length)` - Generate alphanumeric string
- **randomNumeric**: `randomNumeric(length)` - Generate numeric string
- **randomAlphabetic**: `randomAlphabetic(length)` - Generate alphabetic string
- **randomPassword**: `randomPassword(length?)` - Generate secure password

**Utility Functions:**
- **reverse**: `reverse(str)` - Reverse string
- **repeat**: `repeat(str, count)` - Repeat string
- **defaultIfBlank**: `defaultIfBlank(str, defaultValue)` - Return default if blank
- **defaultIfEmpty**: `defaultIfEmpty(str, defaultValue)` - Return default if empty
- **equals**: `equals(str1, str2, ignoreCase?)` - Compare strings
- **slugify**: `slugify(str, separator?)` - Create URL-friendly slug

**StringUtils Class:**
- Static class providing all functions as static methods
- Alternative API: `StringUtils.trim(str)`, `StringUtils.toCamelCase(str)`, etc.

**Features:**
- Zero dependencies, uses only ArkTS standard library
- Full TypeScript type support with null/undefined safety
- 50+ comprehensive string manipulation functions
- Case conversion support (camelCase, PascalCase, snake_case, kebab-case)
- Email and URL validation
- Base64 and URL encoding/decoding
- Random string and password generation
- Complete test suite with 40+ test cases
- 13 practical usage examples
- Production-ready for HarmonyOS application development

Run tests:
```bash
cd ArkTS/string_utils
# Requires HarmonyOS development environment
```

Run example:
```bash
cd ArkTS/examples
# Requires HarmonyOS development environment
```

Usage example:
```typescript
import { 
  isBlank, trim, toCamelCase, truncate,
  isValidEmail, padLeft, base64Encode,
  randomPassword, StringUtils 
} from '../string_utils/mod';

// Empty checks
if (isBlank(userInput)) {
  console.log('Input is required');
}

// Case conversion
const camelCase = toCamelCase('hello_world');     // "helloWorld"
const pascalCase = toPascalCase('hello_world');   // "HelloWorld"
const snakeCase = toSnakeCase('HelloWorld');      // "hello_world"
const kebabCase = toKebabCase('HelloWorld');      // "hello-world"

// Substring operations
const filename = substringAfterLast('/path/to/file.txt', '/');  // "file.txt"
const content = substringBetween('<div>content</div>', '<div>', '</div>');  // "content"
const summary = truncate('This is a very long text...', 20);   // "This is a very lo..."

// Validation
if (isValidEmail('user@example.com')) {
  // Process valid email
}

// Padding
const padded = padLeft('5', 3, '0');  // "005"
const centered = center('hi', 6);      // "  hi  "

// Encoding
const encoded = base64Encode('Hello, World!');
const urlSafe = urlEncode('hello world');  // "hello%20world"

// Random generation
const token = randomAlphanumeric(32);
const password = randomPassword(16);

// Using StringUtils class
const trimmed = StringUtils.trim('  hello  ');
const slug = StringUtils.slugify('Hello World!');  // "hello-world"
```

---

## 📦 Latest Addition

### TypeScript - Template Engine Utilities

Location: `TypeScript/template_utils/mod.ts`

A lightweight, zero-dependency template engine for TypeScript with variable interpolation, conditionals, loops, filters, and partial includes.

**Variable Interpolation:**
- **Basic**: `{{ variable }}` - Output variable value
- **Nested**: `{{ user.name }}` - Access nested object properties
- **Safe**: Returns empty string for undefined/null values

**Filters:**
- **String**: `upper`, `lower`, `capitalize`, `title`, `trim`, `reverse`, `truncate`, `replace`
- **HTML**: `escape` - Escape HTML entities
- **Array**: `join`, `first`, `last`, `size`, `sort`, `reverse_array`
- **Number**: `round`, `abs`
- **Utility**: `default`, `url_encode`, `url_decode`
- **Chaining**: `{{ text | trim | upper }}` - Apply multiple filters

**Conditionals:**
- **If**: `{% if condition %} ... {% endif %}`
- **If-Else**: `{% if condition %} ... {% else %} ... {% endif %}`
- **Operators**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Not**: `{% if not user %} ... {% endif %}`

**Loops:**
- **For**: `{% for item in items %} ... {% endfor %}`
- **Loop variables**: `loop.index`, `loop.index1`, `loop.first`, `loop.last`
- **Filters in loops**: `{% for item in items %}{{ item | upper }}{% endfor %}`

**Partials (Includes):**
- **Include**: `{% include "partial_name" %}`
- **Nested rendering**: Partials can include other partials
- **Context inheritance**: Partials share parent context

**Comments:**
- **Syntax**: `{# This is a comment #}`
- **Behavior**: Removed from output

**Custom Filters:**
- **Register**: `engine.registerFilter(name, fn)`
- **Usage**: `{{ value | custom_filter }}`

**TemplateEngine Class:**
- **Constructor**: `new TemplateEngine(options?)`
- **registerFilter**: Add custom filter function
- **getFilter**: Get filter by name
- **render**: Render template with context and partials

**Convenience Function:**
- **renderTemplate**: `renderTemplate(template, context, partials, options?)` - Quick render without class

**Features:**
- Zero dependencies, uses only TypeScript/JavaScript standard library
- Full TypeScript type support with generics
- 20+ built-in filters for common transformations
- Nested object property access
- Filter chaining support
- Partial template includes
- Comment support
- Custom filter registration
- 25+ comprehensive unit tests
- 15 practical usage examples
- Production-ready for email templates, HTML generation, and dynamic content

Compile and run tests:
```bash
cd TypeScript/template_utils
npx tsc template_utils_test.ts && node template_utils_test.js
```

Run example:
```bash
cd TypeScript/examples
npx tsc template_utils_example.ts && node template_utils_example.js
```

Usage example:
```typescript
import { TemplateEngine, renderTemplate } from './template_utils/mod';

// Simple variable interpolation
const result = renderTemplate('Hello, {{ name }}!', { name: 'World' });
// Returns: "Hello, World!"

// Using filters
const upper = renderTemplate('{{ name | upper }}', { name: 'alice' });
// Returns: "ALICE"

// Filter chaining
const chained = renderTemplate('{{ text | trim | upper }}', { text: '  hello  ' });
// Returns: "HELLO"

// Conditionals
const template = `{% if user %}Hello, {{ user }}{% else %}Welcome, guest{% endif %}`;
const result = renderTemplate(template, { user: 'Alice' });
// Returns: "Hello, Alice"

// Loops
const loopTemplate = '{% for item in items %}{{ item }}{% endfor %}';
const loopResult = renderTemplate(loopTemplate, { items: ['a', 'b', 'c'] });
// Returns: "abc"

// Partials
const partials = { header: '<h1>{{ title }}</h1>' };
const page = renderTemplate('{% include "header" %}', { title: 'Page' }, partials);
// Returns: "<h1>Page</h1>"

// Custom filters
const engine = new TemplateEngine();
engine.registerFilter('double', (n: number) => n * 2);
const custom = engine.render('{{ num | double }}', { num: 21 });
// Returns: "42"

// Nested objects
const nested = renderTemplate('{{ user.address.city }}', {
  user: { address: { city: 'New York' } }
});
// Returns: "New York"

// Email template example
const emailTemplate = `Subject: {{ subject | upper }}

Dear {{ user.name | title }},

Thank you for your order of {{ items | size }} items:
{% for item in items %}
- {{ item.name }} - ${{ item.price }}
{% endfor %}

Total: ${{ total | round:2 }}

{% if discount > 0 %}You saved ${{ discount }}!{% endif %}`;

const email = renderTemplate(emailTemplate, {
  subject: 'order confirmation',
  user: { name: 'john doe' },
  items: [{ name: 'Widget', price: 29.99 }],
  total: 29.99,
  discount: 5.00
});
```

# CI Test
