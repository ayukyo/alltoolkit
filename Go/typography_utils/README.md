# Typography Utils - Go智能文本排版工具

零外部依赖的排版工具集，提供智能引号转换、破折号规范化、省略号处理、文本换行等功能。

## 功能列表

### 智能引号转换
- `SmartQuotes(text)` - 将直引号转换为弯引号
- `SmartQuotesWithStyle(text, style)` - 使用自定义引号样式转换
- `StraightenQuotes(text)` - 将弯引号转换回直引号

### 破折号规范化
- `NormalizeDashes(text, style)` - 规范化破折号
- `EmDash(text)` - 转换为 em dash (—)
- `EnDash(text)` - 转换为 en dash (–)

### 省略号规范化
- `NormalizeEllipsis(text, useChar)` - 规范化省略号

### 综合排版处理
- `Smartify(text)` - 一站式智能排版处理

### 文本换行
- `WrapText(text, width)` - 按指定宽度换行
- `WrapParagraphs(text, width)` - 按段落换行

### 空白规范化
- `NormalizeSpaces(text)` - 规范化空白字符
- `RemoveExtraBlankLines(text, maxBlank)` - 移除多余空行

### 字符统计
- `GetTextStatistics(text)` - 获取完整文本统计
- `CountChars(text, includeSpaces)` - 统计字符数
- `CountWords(text)` - 统计单词数（支持中英文）
- `CountSentences(text)` - 统计句子数
- `CountParagraphs(text)` - 统计段落数

### HTML/Markdown 转义
- `EscapeHTML(text)` - 转义 HTML 特殊字符
- `UnescapeHTML(text)` - 反转义 HTML 字符
- `EscapeMarkdown(text)` - 转义 Markdown 特殊字符

### 标题处理
- `TitleCase(text)` - 转换为标题格式
- `Slugify(text, separator, lowercase)` - 转换为 URL slug

### 对齐处理
- `AlignLeft(text, width, fillChar)` - 左对齐
- `AlignRight(text, width, fillChar)` - 右对齐
- `AlignCenter(text, width, fillChar)` - 居中对齐
- `AlignJustify(text, width)` - 两端对齐

### 行号添加
- `AddLineNumbers(text, start, width)` - 为文本添加行号

### 中文排版处理
- `NormalizeChinesePunctuation(text)` - 规范化中文标点
- `ChineseParagraphIndent(text, indent)` - 添加首行缩进

## 使用示例

```go
package main

import (
    "fmt"
    "github.com/yourusername/alltoolkit/Go/typography_utils"
)

func main() {
    // 智能引号转换
    text := "He said \"Hello World\"... this is a test -- really!"
    smart := typography_utils.Smartify(text)
    fmt.Println(smart)
    // 输出: He said "Hello World"… this is a test — really!

    // 文本统计
    stats := typography_utils.GetTextStatistics("Hello world. How are you?")
    fmt.Printf("Words: %d, Sentences: %d\n", stats.Words, stats.Sentences)
    // 输出: Words: 5, Sentences: 2

    // 标题格式
    title := typography_utils.TitleCase("the lord of the rings")
    fmt.Println(title)
    // 输出: The Lord of the Rings

    // Slug生成
    slug := typography_utils.Slugify("Hello World!", "-", true)
    fmt.Println(slug)
    // 输出: hello-world

    // 中文标点规范化
    chinese := typography_utils.NormalizeChinesePunctuation("你好,世界!")
    fmt.Println(chinese)
    // 输出: 你好，世界！
}
```

## 测试运行

```bash
go test -v ./Go/typography_utils/
```

## 特性

- ✅ 零外部依赖
- ✅ 支持中英文混合文本
- ✅ 完整的测试覆盖
- ✅ 高性能实现

## 作者

AllToolkit 自动生成

## 日期

2026-05-23