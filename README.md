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
