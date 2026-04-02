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

### PHP - String Utilities

Location: `PHP/StringUtils.php`

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

Location: `Kotlin/DateTimeUtils.kt`

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

Location: `Python/file_utils.py`

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

Location: `Go/path_utils.go`

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

Location: `Go/string_utils.go`

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
