# string_utils

Go 字符串工具模块 - 提供全面的字符串处理功能，零外部依赖。

## 安装

```bash
go get github.com/openclaw/alltoolkit/Go/string_utils
```

## 功能列表

### 📐 大小写转换

| 函数 | 说明 | 示例 |
|------|------|------|
| `ToCamelCase` | 转换为 camelCase | `hello_world` → `helloWorld` |
| `ToPascalCase` | 转换为 PascalCase | `hello_world` → `HelloWorld` |
| `ToSnakeCase` | 转换为 snake_case | `HelloWorld` → `hello_world` |
| `ToKebabCase` | 转换为 kebab-case | `helloWorld` → `hello-world` |
| `ToScreamingSnakeCase` | 转换为 SCREAMING_SNAKE_CASE | `helloWorld` → `HELLO_WORLD` |
| `ToTitleCase` | 转换为 Title Case | `hello world` → `Hello World` |

### ✅ 字符串验证

| 函数 | 说明 |
|------|------|
| `IsEmail` | 验证邮箱格式 |
| `IsPhone` | 验证电话号码 |
| `IsURL` | 验证 HTTP(S) URL |
| `IsUUID` | 验证 UUID 格式 |
| `IsIPv4` | 验证 IPv4 地址 |
| `IsHexColor` | 验证十六进制颜色值 |
| `IsSlug` | 验证 URL Slug |
| `IsEmpty` | 检查是否为空或空白 |
| `IsAlpha` | 检查是否只包含字母 |
| `IsAlphanumeric` | 检查是否只包含字母和数字 |
| `IsNumeric` | 检查是否只包含数字 |
| `IsASCII` | 检查是否只包含 ASCII 字符 |
| `IsLower` | 检查是否全小写 |
| `IsUpper` | 检查是否全大写 |

### 🔍 字符串相似度

| 函数 | 说明 |
|------|------|
| `LevenshteinDistance` | 计算编辑距离 |
| `Similarity` | 计算相似度比例 (0-1) |
| `HammingDistance` | 计算汉明距离 (需等长) |
| `JaroSimilarity` | Jaro 相似度算法 |
| `JaroWinklerSimilarity` | Jaro-Winkler 相似度算法 |

### 🔧 字符串操作

| 函数 | 说明 |
|------|------|
| `Reverse` | 反转字符串 (支持 Unicode) |
| `Truncate` | 截断字符串并添加后缀 |
| `PadLeft` | 左填充 |
| `PadRight` | 右填充 |
| `PadCenter` | 居中填充 |
| `Repeat` | 重复字符串 |

### 📊 字符串分析

| 函数 | 说明 |
|------|------|
| `WordCount` | 单词计数 |
| `CharCount` | 字符计数 (Unicode) |
| `ByteCount` | 字节计数 |
| `LineCount` | 行计数 |
| `Count` | 子串出现次数 |
| `Frequency` | 字符频率统计 |
| `WordFrequency` | 单词频率统计 |
| `LongestWord` | 最长单词 |
| `ShortestWord` | 最短单词 |

### 🎯 特殊检查

| 函数 | 说明 |
|------|------|
| `IsPalindrome` | 回文检测 |
| `IsAnagram` | 变位词检测 |
| `IsPangram` | 全字母句检测 |

### 🔒 字符串掩码

| 函数 | 说明 |
|------|------|
| `Mask` | 通用掩码 |
| `MaskEmail` | 邮箱掩码 |
| `MaskPhone` | 电话掩码 |

### 🔎 模糊匹配

| 函数 | 说明 |
|------|------|
| `FuzzyMatch` | 模糊匹配 (允许遗漏) |
| `FuzzyMatchScore` | 模糊匹配评分 |
| `FindBestMatch` | 找最佳匹配 |

### 🛠️ 其他功能

| 函数 | 说明 |
|------|------|
| `Substring` | 子字符串 (Unicode 安全) |
| `Left` | 取左侧 N 个字符 |
| `Right` | 取右侧 N 个字符 |
| `SplitLines` | 按行分割 |
| `Chunk` | 分块 |
| `Template` | 模板替换 `${key}` |
| `RemoveWhitespace` | 移除空白 |
| `RemoveAccents` | 移除重音符号 |
| `SwapCase` | 交换大小写 |
| `Contains` | 包含检查 (可选大小写敏感) |
| `ContainsAll` | 包含所有 |
| `ContainsAny` | 包含任意 |
| `StartsWith` | 开头检查 |
| `EndsWith` | 结尾检查 |

## 快速示例

```go
package main

import (
    "fmt"
    su "github.com/openclaw/alltoolkit/Go/string_utils"
)

func main() {
    // 大小写转换
    fmt.Println(su.ToCamelCase("hello_world"))      // helloWorld
    fmt.Println(su.ToSnakeCase("HelloWorld"))       // hello_world
    
    // 验证
    fmt.Println(su.IsEmail("test@example.com"))     // true
    fmt.Println(su.IsIPv4("192.168.1.1"))           // true
    
    // 相似度
    fmt.Println(su.LevenshteinDistance("kitten", "sitting"))  // 3
    fmt.Println(su.Similarity("hello", "hallo"))              // 0.8
    
    // 回文检测
    fmt.Println(su.IsPalindrome("A man a plan a canal Panama"))  // true
    
    // 模糊匹配
    candidates := []string{"programming", "programmer", "progress"}
    best, _ := su.FindBestMatch("prg", candidates)
    fmt.Println(best)  // programming
    
    // 掩码
    fmt.Println(su.MaskEmail("user@example.com", '*'))  // u***r@example.com
    fmt.Println(su.Mask("1234567890", 4, 4, '*'))       // 1234****7890
    
    // 模板
    template := "Hello ${name}, welcome to ${place}!"
    values := map[string]string{"name": "World", "place": "Earth"}
    fmt.Println(su.Template(template, values))  // Hello World, welcome to Earth!
}
```

## Unicode 支持

所有函数都正确处理 Unicode 字符：

```go
// 中文
su.Reverse("你好世界")              // 界世好你
su.CharCount("你好世界")            // 4
su.Left("你好世界", 2)              // 你好

// Emoji
su.CharCount("hello🌍world")        // 11
```

## 性能

模块经过性能优化，包含基准测试：

```bash
go test -bench=. -benchmem
```

## 依赖

**零外部依赖** - 仅使用 Go 标准库。

## 许可证

MIT License