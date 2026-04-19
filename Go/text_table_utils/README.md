# text_table_utils

终端表格格式化工具，支持多种边框样式、文本对齐和彩色输出。

## 功能特性

- **多种边框样式**：ASCII、Unicode、双线、圆角、Markdown、无边框
- **文本对齐**：左对齐、居中、右对齐
- **列宽控制**：自动宽度、最小宽度、最大宽度、总宽度限制
- **表头样式**：可开关表头，支持彩色
- **单元格着色**：支持单独设置单元格颜色
- **隐藏列**：动态隐藏指定列
- **Unicode 支持**：正确计算中文字符宽度
- **零外部依赖**：纯 Go 标准库实现

## 安装

```bash
cp -r text_table_utils $GOPATH/src/
```

## 快速开始

### 基础表格

```go
package main

import (
    "fmt"
    table "text_table_utils"
)

func main() {
    // 创建表格
    t := table.NewTable("Name", "Age", "City")
    t.AddRow("Alice", 25, "Beijing")
    t.AddRow("Bob", 30, "Shanghai")
    t.AddRow("Charlie", 28, "Guangzhou")
    t.Print()
}
```

输出：
```
┌─────────┬─────┬───────────┐
│ Name    │ Age │ City      │
├─────────┼─────┼───────────┤
│ Alice   │ 25  │ Beijing   │
│ Bob     │ 30  │ Shanghai  │
│ Charlie │ 28  │ Guangzhou │
└─────────┴─────┴───────────┘
```

### 设置边框样式

```go
// ASCII 样式（兼容所有终端）
t.SetStyle(table.StyleASCII)

// Unicode 样式（默认）
t.SetStyle(table.StyleUnicode)

// 双线样式
t.SetStyle(table.StyleDouble)

// 圆角样式
t.SetStyle(table.StyleRounded)

// Markdown 样式
t.SetStyle(table.StyleMarkdown)

// 无边框
t.SetStyle(table.StyleNone)
```

### 文本对齐

```go
t := table.NewTable("ID", "Name", "Price")
t.SetColumnAlignment(0, table.AlignRight)   // ID 右对齐
t.SetColumnAlignment(1, table.AlignLeft)    // Name 左对齐
t.SetColumnAlignment(2, table.AlignRight)  // Price 右对齐
t.AddRow(1, "Apple", 3.50)
t.AddRow(2, "Banana", 2.80)
```

### 列宽控制

```go
// 设置最小宽度
t.SetColumnMinWidth(0, 10)  // 第一列最小 10 字符

// 设置最大宽度
t.SetColumnMaxWidth(1, 20)  // 第二列最大 20 字符

// 设置表格总宽度
t.SetMaxWidth(80)

// 关闭自动宽度
t.SetAutoWidth(false)
```

### 彩色输出

```go
// 定义颜色函数
red := func(s string) string {
    return "\033[31m" + s + "\033[0m"
}
green := func(s string) string {
    return "\033[32m" + s + "\033[0m"
}

t := table.NewTable("Status", "Message")
t.SetHeaderColor(green)      // 表头绿色
t.SetBorderColor(red)        // 边框红色
t.AddRow("OK", "Success")
```

### 单元格着色

```go
t := table.NewTable("Product", "Stock")

// 使用 Cell 结构体设置颜色
red := func(s string) string { return "\033[31m" + s + "\033[0m" }
green := func(s string) string { return "\033[32m" + s + "\033[0m" }

t.AddRowWithColor([]table.Cell{
    {Text: "Apple", Color: nil},
    {Text: "Low", Color: red},
})
t.AddRowWithColor([]table.Cell{
    {Text: "Banana", Color: nil},
    {Text: "In Stock", Color: green},
})
```

### 隐藏列

```go
t := table.NewTable("ID", "Secret", "Public")
t.HideColumn(1)  // 隐藏第二列
t.AddRow(1, "hidden", "visible")
```

### 快捷函数

```go
// 快速创建简单表格
headers := []string{"Name", "Age"}
rows := [][]string{
    {"Alice", "25"},
    {"Bob", "30"},
}
fmt.Print(table.SimpleTable(headers, rows))

// 创建 Markdown 表格
fmt.Print(table.SimpleMarkdownTable(headers, rows))
```

## API 参考

### Table 方法

| 方法 | 说明 |
|------|------|
| `NewTable(cols...string)` | 创建新表格 |
| `SetStyle(style)` | 设置边框样式 |
| `SetShowHeader(bool)` | 显示/隐藏表头 |
| `SetShowBorders(bool)` | 显示/隐藏边框 |
| `SetPadding(int)` | 设置单元格内边距 |
| `SetAutoWidth(bool)` | 自动列宽开关 |
| `SetMaxWidth(int)` | 设置最大总宽度 |
| `SetColumnAlignment(col, align)` | 设置列对齐 |
| `SetColumnMinWidth(col, width)` | 设置列最小宽度 |
| `SetColumnMaxWidth(col, width)` | 设置列最大宽度 |
| `HideColumn(col)` | 隐藏列 |
| `SetHeaderColor(fn)` | 设置表头颜色 |
| `SetBorderColor(fn)` | 设置边框颜色 |
| `AddRow(cells...)` | 添加行 |
| `AddRowWithColor([]Cell)` | 添加带颜色的行 |
| `String()` | 返回格式化字符串 |
| `Print()` | 打印到标准输出 |

### 边框样式

- `StyleASCII` - 基本 ASCII 字符
- `StyleUnicode` - Unicode 制表符（默认）
- `StyleDouble` - 双线 Unicode
- `StyleRounded` - 圆角 Unicode
- `StyleMarkdown` - Markdown 格式
- `StyleNone` - 无边框

### 对齐方式

- `AlignLeft` - 左对齐
- `AlignCenter` - 居中
- `AlignRight` - 右对齐

## 测试

```bash
cd text_table_utils
go test -v
```

## 示例

查看 `examples/` 目录获取更多使用示例。

## 许可证

MIT License