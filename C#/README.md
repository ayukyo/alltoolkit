# C# 工具库

AllToolkit 的 C# 实现，提供零依赖的生产级工具函数。

## 已实现的模块

| 模块 | 文件 | 说明 |
|------|------|------|
| string_utils | `string_utils/StringUtils.cs` | 字符串处理工具 |
| http_utils | `http_utils/` | HTTP 请求工具 |
| trie_utils | `trie_utils/TrieUtils.cs` | Trie 前缀树数据结构 |

## 快速开始

```csharp
using AllToolkit.StringUtils;

// 字符串操作
string trimmed = StringUtils.Trim("  hello  ");
string[] parts = StringUtils.Split("a,b,c", ",");
bool isEmail = StringUtils.IsEmail("test@example.com");
```

## 模块详情

### string_utils

提供 40+ 个字符串处理函数：

- **修剪**: `Trim`, `TrimLeft`, `TrimRight`, `TrimChars`
- **分割**: `Split`, `SplitChar`
- **替换**: `Replace`, `ReplaceFirst`, `ReplaceN`
- **查找**: `Count`, `StartsWith`, `EndsWith`, `Contains`
- **大小写**: `ToUpper`, `ToLower`, `ToTitleCase`, `ToSnakeCase`, `ToCamelCase`
- **验证**: `IsBlank`, `IsNumeric`, `IsEmail`, `IsAlphanumeric`
- **子串**: `Left`, `Right`, `Substring`, `DropLeft`, `DropRight`
- **连接**: `Join`, `Repeat`, `Reverse`
- **清理**: `RemoveWhitespace`, `NormalizeWhitespace`
- **截断**: `Truncate`, `TruncateWithEllipsis`
- **填充**: `PadLeft`, `PadRight`, `Center`

详见 [string_utils/README.md](string_utils/README.md)

## 编译说明

```bash
# 编译单个模块
cd string_utils
csc -target:library -out:StringUtils.dll StringUtils.cs

# 运行测试
csc -out:StringUtilsTest.exe StringUtils.cs StringUtilsTest.cs
./StringUtilsTest.exe

# 运行示例
csc -out:StringUtilsExample.exe StringUtils.cs ../examples/StringUtilsExample.cs
./StringUtilsExample.exe
```

## 要求

- .NET Framework 4.5+ 或 .NET Core 2.0+
- C# 7.0+

## 许可证

MIT License
