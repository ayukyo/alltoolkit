# StringUtils - C# 字符串工具模块

零依赖的 C# 字符串处理工具类，提供常用的字符串操作功能。

## 特性

- ✅ **零依赖** - 仅使用 .NET 标准库
- ✅ **类型安全** - 完整的 null 检查
- ✅ **性能优化** - 使用 StringBuilder 进行大量拼接操作
- ✅ **文档完善** - 完整的中文注释

## 快速开始

```csharp
using AllToolkit.StringUtils;

// 修剪字符串
string trimmed = StringUtils.Trim("  hello  ");  // "hello"

// 分割字符串
string[] parts = StringUtils.Split("a,b,c", ",");  // ["a", "b", "c"]

// 替换字符串
string replaced = StringUtils.Replace("hello world", "world", "C#");  // "hello C#"

// 验证字符串
bool isEmail = StringUtils.IsEmail("test@example.com");  // true
```

## API 文档

### 字符串修剪

| 方法 | 说明 | 示例 |
|------|------|------|
| `Trim(str)` | 去除两侧空白 | `"  hi  "` → `"hi"` |
| `TrimLeft(str)` | 去除左侧空白 | `"  hi  "` → `"hi  "` |
| `TrimRight(str)` | 去除右侧空白 | `"  hi  "` → `"  hi"` |
| `TrimChars(str, chars)` | 去除指定字符 | `"...hi..."` → `"hi"` |

### 字符串分割

| 方法 | 说明 | 示例 |
|------|------|------|
| `Split(str, separator)` | 按字符串分割 | `"a,b,c"` → `["a","b","c"]` |
| `Split(str, separator, max)` | 限制分割次数 | `"a,b,c,d"` → `["a","b,c,d"]` |
| `SplitChar(str, char)` | 按字符分割 | `"a,b,c"` → `["a","b","c"]` |

### 字符串替换

| 方法 | 说明 | 示例 |
|------|------|------|
| `Replace(str, old, new)` | 替换所有 | `"aaa"` → `"bbb"` |
| `ReplaceFirst(str, old, new)` | 只替换第一个 | `"aaa"` → `"baa"` |
| `ReplaceN(str, old, new, n)` | 替换前 N 个 | `"aaa"` → `"bba"` |

### 字符串查找

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `Count(str, substring)` | 统计出现次数 | `int` |
| `StartsWith(str, prefix)` | 是否以指定前缀开头 | `bool` |
| `EndsWith(str, suffix)` | 是否以指定后缀结尾 | `bool` |
| `Contains(str, substring)` | 是否包含子串 | `bool` |

### 大小写转换

| 方法 | 说明 | 示例 |
|------|------|------|
| `ToUpper(str)` | 转大写 | `"hello"` → `"HELLO"` |
| `ToLower(str)` | 转小写 | `"HELLO"` → `"hello"` |
| `ToTitleCase(str)` | 标题格式 | `"hello world"` → `"Hello World"` |
| `ToSnakeCase(str)` | 蛇形命名 | `"HelloWorld"` → `"hello_world"` |
| `ToCamelCase(str)` | 驼峰命名 | `"hello_world"` → `"helloWorld"` |

### 字符串验证

| 方法 | 说明 |
|------|------|
| `IsNullOrEmpty(str)` | 是否为空或 null |
| `IsBlank(str)` | 是否为空白字符 |
| `IsNotBlank(str)` | 是否非空白 |
| `IsNumeric(str)` | 是否为数字 |
| `IsInteger(str)` | 是否为整数 |
| `IsFloat(str)` | 是否为浮点数 |
| `IsAlpha(str)` | 是否全为字母 |
| `IsAlphanumeric(str)` | 是否全为字母数字 |
| `IsEmail(str)` | 是否为邮箱格式 |

### 子字符串操作

| 方法 | 说明 | 示例 |
|------|------|------|
| `Left(str, n)` | 取左边 N 个字符 | `"hello"` → `"hel"` |
| `Right(str, n)` | 取右边 N 个字符 | `"hello"` → `"llo"` |
| `DropLeft(str, n)` | 去掉左边 N 个 | `"hello"` → `"llo"` |
| `DropRight(str, n)` | 去掉右边 N 个 | `"hello"` → `"hel"` |
| `Substring(str, start, len)` | 子字符串 | `"hello"` → `"ell"` |

### 字符串连接与重复

| 方法 | 说明 | 示例 |
|------|------|------|
| `Join(separator, values)` | 连接字符串 | `["a","b"]` → `"a,b"` |
| `Repeat(str, count)` | 重复字符串 | `"ab",3` → `"ababab"` |
| `Reverse(str)` | 反转字符串 | `"hello"` → `"olleh"` |

### 字符串清理

| 方法 | 说明 | 示例 |
|------|------|------|
| `RemoveWhitespace(str)` | 移除所有空白 | `"h e llo"` → `"hello"` |
| `RemoveChars(str, chars)` | 移除指定字符 | `"hello123"` → `"hello"` |
| `NormalizeWhitespace(str)` | 规范化空白 | `"  a   b  "` → `"a b"` |

### 字符串截断

| 方法 | 说明 | 示例 |
|------|------|------|
| `Truncate(str, maxLen)` | 截断字符串 | `"hello",3` → `"hel"` |
| `TruncateWithEllipsis(str, maxLen)` | 截断加省略号 | `"hello",5` → `"he..."` |

### 字符串填充

| 方法 | 说明 | 示例 |
|------|------|------|
| `PadLeft(str, width, char)` | 左填充 | `"hi",5` → `"   hi"` |
| `PadRight(str, width, char)` | 右填充 | `"hi",5` → `"hi   "` |
| `Center(str, width, char)` | 居中 | `"hi",6` → `"  hi  "` |

### 字符串比较

| 方法 | 说明 |
|------|------|
| `EqualsIgnoreCase(s1, s2)` | 忽略大小写比较 |
| `Compare(s1, s2)` | 比较大小 |
| `CompareIgnoreCase(s1, s2)` | 忽略大小写比较 |

## 编译与运行

### 编译库

```bash
# 编译为 DLL
csc -target:library -out:StringUtils.dll StringUtils.cs

# 或者编译为可执行文件（包含测试）
csc -out:StringUtilsTest.exe StringUtils.cs StringUtilsTest.cs
```

### 运行测试

```bash
# 使用 .NET CLI
dotnet new console -n StringUtilsTest
cp StringUtils.cs StringUtilsTest.cs StringUtilsTest/
cd StringUtilsTest
dotnet run

# 或者直接使用 csc
csc -out:StringUtilsTest.exe StringUtils.cs StringUtilsTest.cs
./StringUtilsTest.exe
```

### 运行示例

```bash
csc -out:StringUtilsExample.exe StringUtils.cs ../examples/StringUtilsExample.cs
./StringUtilsExample.exe
```

## 项目集成

### 方式 1：直接复制文件

将 `StringUtils.cs` 复制到你的项目中即可使用。

### 方式 2：作为类库引用

```bash
# 编译为 DLL
csc -target:library -out:AllToolkit.StringUtils.dll StringUtils.cs

# 在其他项目中引用
csc -reference:AllToolkit.StringUtils.dll YourProgram.cs
```

## 许可证

MIT License - 详见项目根目录 LICENSE 文件
