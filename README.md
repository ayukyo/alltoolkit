# AllToolkit - Universal Toolkit Library

A comprehensive, multi-language collection of utility functions for everyday development tasks.

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

## Structure

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

## License

MIT - Free for personal and commercial use.
