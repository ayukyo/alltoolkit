# Base58 Utils for Go

零外部依赖的 Base58 编码/解码工具库，支持多种字母表、Base58Check（带校验）、大整数编码和验证功能。

Base58 是一种二进制到文本的编码方案，排除了视觉上容易混淆的字符（0、O、I、l），常用于比特币地址、IPFS CID 等需要人类可读的场景。

## 功能特性

- **多种字母表**: Bitcoin、Flickr、Ripple 字母表支持
- **Base58Check**: 带校验和的编码（比特币地址格式）
- **大整数编码**: 支持任意大整数编码/解码
- **验证功能**: 检测字符串是否为有效 Base58
- **字母表转换**: 不同字母表之间的转换
- **Hex 支持**: Hex 字符串与 Base58 转换
- **零字节处理**: 自动处理前导零字节（编码为 '1'）
- **内置 SHA256**: 零外部依赖，内置 SHA256 实现用于校验和

## 安装

```go
import "github.com/ayukyo/alltoolkit/Go/base58_utils"
```

## 快速开始

### 基础编码/解码

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/base58_utils"
)

func main() {
    // 编码字符串
    encoded := base58_utils.EncodeString("Hello, World!")
    fmt.Println(encoded) // 72k1xXWG59fYdzSNoA

    // 解码字符串
    decoded, _ := base58_utils.DecodeString(encoded)
    fmt.Println(decoded) // Hello, World!

    // 编码字节
    data := []byte{0x00, 0x01, 0x02, 0xFF}
    encodedBytes := base58_utils.Encode(data)
    fmt.Println(encodedBytes) // 1LiA
}
```

### Base58Check（带校验和）

用于比特币地址等需要校验的场景：

```go
// 编码带校验和
data := []byte("payload data")
encoded := base58_utils.EncodeCheck(data)

// 解码并验证校验和
decoded, err := base58_utils.DecodeCheck(encoded)
if err != nil {
    // 校验和无效
}
```

### 不同字母表

```go
// Bitcoin 字母表（默认）
encoded := base58_utils.EncodeString("Test")

// Flickr 字母表
encoded = base58_utils.EncodeStringWithAlphabet("Test", base58_utils.FlickrAlphabet)

// Ripple 字母表
encoded = base58_utils.EncodeStringWithAlphabet("Test", base58_utils.RippleAlphabet)
```

### 大整数编码

```go
import "math/big"

// 编码大整数
num := big.NewInt(12345)
encoded := base58_utils.EncodeInt(num)

// 解码为大整数
decoded, _ := base58_utils.DecodeInt(encoded)
```

### 验证函数

```go
// 检查是否为有效 Base58
if base58_utils.IsValid("2NEpo7TZRRrL6Si7Hqy7jcQ") {
    fmt.Println("Valid!")
}

// 注意: Base58 排除了以下字符
// 0 (零) - 与 O 混淆
// O (大写o) - 与 0 混淆
// I (大写i) - 与 l 混淆
// l (小写L) - 与 I 混淆
```

### Hex 转换

```go
// Hex 转 Base58
encoded, _ := base58_utils.EncodeHex("deadbeef")

// Base58 转 Hex
hex, _ := base58_utils.DecodeHex(encoded)
```

### 前导零处理

```go
// 包含前导零字节的数据
data := []byte{0x00, 0x00, 0x01, 0x02}
encoded := base58_utils.Encode(data) // "111UXe2A"

// 前导零字节编码为 '1'
// 移除前导 '1'
trimmed := base58_utils.TrimLeadingZeros(encoded)

// 统计前导 '1' 数量
count := base58_utils.CountLeadingZeros(encoded)
```

## API 参考

### 编码函数

| 函数 | 说明 |
|------|------|
| `Encode(input []byte) string` | 使用 Bitcoin 字母表编码字节 |
| `EncodeWithAlphabet(input []byte, alphabet *Alphabet) string` | 使用自定义字母表编码 |
| `EncodeString(s string) string` | 编码字符串 |
| `EncodeStringWithAlphabet(s string, alphabet *Alphabet) string` | 使用自定义字母表编码字符串 |
| `EncodeCheck(input []byte) string` | Base58Check 编码（带校验和） |
| `EncodeInt(n *big.Int) string` | 编码大整数 |
| `EncodeHex(hex string) (string, error)` | 编码 Hex 字符串 |

### 解码函数

| 函数 | 说明 |
|------|------|
| `Decode(input string) ([]byte, error)` | 使用 Bitcoin 字母表解码 |
| `DecodeWithAlphabet(input string, alphabet *Alphabet) ([]byte, error)` | 使用自定义字母表解码 |
| `DecodeString(input string) (string, error)` | 解码为字符串 |
| `DecodeStringWithAlphabet(input string, alphabet *Alphabet) (string, error)` | 使用自定义字母表解码为字符串 |
| `DecodeCheck(input string) ([]byte, error)` | Base58Check 解码（验证校验和） |
| `DecodeInt(input string) (*big.Int, error)` | 解码为大整数 |
| `DecodeHex(input string) (string, error)` | 解码为 Hex 字符串 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `IsValid(s string) bool` | 检查是否为有效 Base58（Bitcoin 字母表） |
| `IsValidWithAlphabet(s string, alphabet *Alphabet) bool` | 使用自定义字母表验证 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `TrimLeadingZeros(s string) string` | 移除前导 '1'（零字节编码） |
| `CountLeadingZeros(s string) int` | 统计前导 '1' 数量 |
| `ConvertAlphabet(input string, from, to *Alphabet) (string, error)` | 字母表转换 |
| `Size(inputSize int) int` | 估算编码后大小 |
| `DecodeSize(encodedSize int) int` | 估算解码后大小 |

### 字母表

```go
// Bitcoin 字母表（最常用）
BitcoinAlphabet // "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

// Flickr 字母表
FlickrAlphabet  // "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

// Ripple 字母表
RippleAlphabet  // "rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz"

// 创建自定义字母表
custom := base58_utils.NewAlphabet("your-58-char-alphabet-string")
```

### 错误类型

```go
var (
    ErrInvalidBase58   = errors.New("invalid base58 encoding")
    ErrEmptyInput      = errors.New("empty input")
    ErrInvalidAlphabet = errors.New("invalid alphabet length, must be 58 characters")
)
```

## Base58 vs Base64

| 特性 | Base58 | Base64 |
|------|--------|--------|
| 字符数量 | 58 | 64 |
| 排除字符 | 0, O, I, l | 无 |
| 用途 | 比特币地址、IPFS | 通用编码 |
| 可读性 | 更好 | 一般 |
| 效率 | 略低 | 更高 |

## 测试

```bash
# 运行测试
go test ./...

# 运行测试并查看覆盖率
go test -cover ./...

# 运行基准测试
go test -bench=. ./...
```

## 使用场景

- **比特币地址编码**: 使用 `EncodeCheck` / `DecodeCheck`
- **IPFS CID**: 使用默认 Bitcoin 字母表
- **短链接**: 避免 URL 中的混淆字符
- **API Key**: 生成人类可读的唯一标识
- **密码哈希**: 可选的哈希表示方式

## 许可证

MIT License