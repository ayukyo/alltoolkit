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
- Rust
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
# CI Test
