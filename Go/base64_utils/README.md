# Base64 Utils for Go

零外部依赖的 Base64 编码/解码工具库，支持多种编码格式、文件操作和自动检测。

## 功能特性

- **多种编码格式**: 标准 Base64、URL-safe、Raw（无填充）编码
- **字符串操作**: 编码/解码字符串，自动检测编码类型
- **文件操作**: 文件编码/解码，读写器支持
- **验证功能**: 检测字符串是否为有效 Base64
- **编码转换**: 不同编码格式之间转换
- **分块处理**: MIME 格式的分块编码/解码
- **批量操作**: 多行文本批量处理
- **安全函数**: 错误恢复，不会 panic

## 安装

```go
import "github.com/ayukyo/alltoolkit/Go/base64_utils"
```

## 快速开始

### 基础编码/解码

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/base64_utils"
)

func main() {
    // 编码字符串
    encoded := base64_utils.EncodeString("Hello, World!")
    fmt.Println(encoded) // SGVsbG8sIFdvcmxkIQ==

    // 解码字符串
    decoded, _ := base64_utils.DecodeString(encoded)
    fmt.Println(decoded) // Hello, World!

    // 编码字节
    data := []byte{0x00, 0x01, 0x02, 0xFF}
    encodedBytes := base64_utils.Encode(data)
    fmt.Println(encodedBytes) // AAEC/w==
}
```

### URL-safe 编码

```go
// 使用 URL-safe 编码（- 和 _ 代替 + 和 /）
encoded := base64_utils.EncodeString("Hello!", base64_utils.URLSafe)

// Raw 编码（无填充）
encoded = base64_utils.EncodeString("Hello!", base64_utils.RawURLSafe)
```

### 自动检测解码

```go
// 自动检测编码类型并解码
decoded, err := base64_utils.AutoDecode("SGVsbG8sIFdvcmxkIQ==")
if err != nil {
    panic(err)
}
fmt.Println(string(decoded)) // Hello, World!
```

### 文件操作

```go
// 编码文件内容
encoded, err := base64_utils.EncodeFile("input.txt")
if err != nil {
    panic(err)
}

// 解码并保存到文件
err = base64_utils.DecodeToFile(encoded, "output.txt")
if err != nil {
    panic(err)
}
```

### 验证函数

```go
// 检查是否为有效 Base64
if base64_utils.IsValid("SGVsbG8sIFdvcmxkIQ==") {
    fmt.Println("Valid!")
}

// 检查任意编码类型
if base64_utils.IsValidAny("SGVsbG8sIFdvcmxkIQ") {
    fmt.Println("Valid in some encoding!")
}
```

### 编码转换

```go
// 标准 Base64 转 Raw URL-safe
rawURL, err := base64_utils.ConvertEncoding(
    "SGVsbG8sIFdvcmxkIQ==",
    base64_utils.Standard,
    base64_utils.RawURLSafe,
)
```

### 分块编码（MIME 格式）

```go
// 每 76 字符换行
longText := "This is a very long text..."
chunked := base64_utils.ChunkedEncode([]byte(longText))

// 解码分块 Base64
decoded, _ := base64_utils.ChunkedDecode(chunked)
```

### 批量处理

```go
// 编码多行
lines := []string{"Hello", "World", "Test"}
encoded := base64_utils.EncodeLines(lines)

// 解码多行
decoded, _ := base64_utils.DecodeLines(encoded)
```

### 填充操作

```go
// 添加填充
padded := base64_utils.AddPadding("SGVsbG8sIFdvcmxkIQ")
// 输出: SGVsbG8sIFdvcmxkIQ==

// 移除填充
raw := base64_utils.RemovePadding("SGVsbG8sIFdvcmxkIQ==")
// 输出: SGVsbG8sIFdvcmxkIQ
```

## API 参考

### 编码函数

| 函数 | 说明 |
|------|------|
| `Encode(data []byte, encType ...EncodingType) string` | 编码字节切片 |
| `EncodeString(s string, encType ...EncodingType) string` | 编码字符串 |
| `EncodeFile(filePath string, encType ...EncodingType) (string, error)` | 编码文件内容 |
| `EncodeReader(r io.Reader, encType ...EncodingType) (string, error)` | 从读取器编码 |
| `ChunkedEncode(data []byte, encType ...EncodingType) string` | 分块编码（MIME） |
| `EncodeLines(lines []string, encType ...EncodingType) []string` | 批量编码多行 |

### 解码函数

| 函数 | 说明 |
|------|------|
| `Decode(encoded string, encType ...EncodingType) ([]byte, error)` | 解码为字节切片 |
| `DecodeString(encoded string, encType ...EncodingType) (string, error)` | 解码为字符串 |
| `AutoDecode(encoded string) ([]byte, error)` | 自动检测编码类型解码 |
| `DecodeToFile(encoded string, filePath string, encType ...EncodingType) error` | 解码并写入文件 |
| `ChunkedDecode(encoded string, encType ...EncodingType) ([]byte, error)` | 解码分块 Base64 |
| `DecodeLines(encodedLines []string, encType ...EncodingType) ([]string, error)` | 批量解码多行 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `IsValid(s string, encType ...EncodingType) bool` | 检查是否为有效 Base64 |
| `IsValidAny(s string) bool` | 检查是否为任意格式的有效 Base64 |
| `GetEncodingType(encoded string) (EncodingType, error)` | 检测编码类型 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `AddPadding(encoded string) string` | 添加填充 |
| `RemovePadding(encoded string) string` | 移除填充 |
| `ConvertEncoding(encoded string, from, to EncodingType) (string, error)` | 转换编码格式 |
| `Size(inputSize int) int` | 计算编码后大小 |
| `DecodeSize(encodedSize int) int` | 计算解码后最大大小 |
| `SafeEncodeString(s string, encType ...EncodingType) string` | 安全编码 |
| `SafeDecodeString(encoded string, encType ...EncodingType) string` | 安全解码（错误时返回原字符串） |

### 编码类型

```go
const (
    Standard     EncodingType = iota // 标准 Base64（+、/、填充）
    URLSafe                          // URL-safe（-、_、填充）
    RawStandard                      // 标准 Base64 无填充
    RawURLSafe                       // URL-safe 无填充
)
```

### 错误类型

```go
var (
    ErrInvalidBase64     = errors.New("invalid base64 encoding")
    ErrEmptyInput        = errors.New("empty input")
    ErrFileNotFound      = errors.New("file not found")
    ErrFileWriteFailed   = errors.New("failed to write file")
    ErrInvalidPadding    = errors.New("invalid padding")
)
```

## 测试

```bash
# 运行测试
go test ./...

# 运行测试并查看覆盖率
go test -cover ./...

# 运行基准测试
go test -bench=. ./...
```

## 许可证

MIT License