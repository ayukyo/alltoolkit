# encoding_utils

Go 编码/解码工具库，提供多种常用的编码转换功能。

## 功能特性

### Base64 编码/解码
- 标准 Base64 编码和解码
- URL 安全的 Base64 编码（无填充）
- 分块 Base64 编码（带换行）
- 流式 Base64 编码/解码

### Hex 编码/解码
- 十六进制字符串转换

### URL 编码/解码
- 查询参数编码
- URL 路径编码
- Map 转 Query String

### HTML 编码/解码
- HTML 特殊字符转义
- HTML 实体反转义

### ROT13/N 编码
- ROT13 字母旋转（自反）
- 自定义旋转值 ROT-N

### Run-Length 编码
- 简单的 RLE 压缩/解压

### Binary 编码
- 字节到二进制字符串转换

### Unicode 转义
- Unicode 字符转 `\uXXXX` 格式

### Quoted-Printable
- QP 编码/解码

### 实用工具
- 字符计数（Unicode 感知）
- 可打印字符检测

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/encoding_utils
```

## 快速开始

```go
package main

import (
    "fmt"
    encoding_utils "github.com/ayukyo/alltoolkit/Go/encoding_utils"
)

func main() {
    // Base64
    encoded := encoding_utils.Base64EncodeString("Hello, World!")
    fmt.Println(encoded) // SGVsbG8sIFdvcmxkIQ==
    
    // URL 编码
    params := map[string]string{"name": "John Doe"}
    query := encoding_utils.URLEncodeMap(params)
    fmt.Println(query) // name=John+Doe
    
    // ROT13
    rot := encoding_utils.Rot13("hello")
    fmt.Println(rot) // uryyb
}
```

## API 参考

### Base64

```go
Base64Encode(data []byte) string
Base64Decode(encoded string) ([]byte, error)
Base64URLEncode(data []byte) string
Base64URLDecode(encoded string) ([]byte, error)
Base64EncodeString(text string) string
Base64DecodeString(encoded string) (string, error)
Base64ChunkedEncode(data []byte, lineLength int) string
Base64ChunkedDecode(encoded string) ([]byte, error)
```

### Hex

```go
HexEncode(data []byte) string
HexDecode(encoded string) ([]byte, error)
HexEncodeString(text string) string
HexDecodeString(encoded string) (string, error)
```

### URL

```go
URLEncode(text string) string
URLDecode(encoded string) (string, error)
URLPathEncode(text string) string
URLPathDecode(encoded string) (string, error)
URLEncodeMap(params map[string]string) string
URLDecodeMap(query string) (map[string]string, error)
```

### HTML

```go
HTMLEscape(text string) string
HTMLUnescape(escaped string) string
```

### ROT13/N

```go
Rot13(text string) string
RotN(text string, n int) string
```

### Run-Length Encoding

```go
RLEncode(data []byte) []byte
RLDecode(data []byte) ([]byte, error)
RLEncodeString(text string) string
RLDecodeString(encoded string) (string, error)
```

### Binary

```go
BinaryEncode(data []byte) string
BinaryDecode(binary string) ([]byte, error)
```

### Unicode

```go
UnicodeEscape(text string) string
UnicodeUnescape(escaped string) (string, error)
```

### Quoted-Printable

```go
QuotedPrintableEncode(text string) string
QuotedPrintableDecode(encoded string) (string, error)
```

### Utility

```go
CharCount(text string) (runes int, bytes int)
IsPrintable(text string) bool
```

## 测试

```bash
go test -v
```

## 特性

- ✅ 零外部依赖
- ✅ 完整的单元测试
- ✅ 基准测试
- ✅ 使用示例

## 许可证

MIT