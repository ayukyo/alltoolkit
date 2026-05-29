# Base64 Utils - C 语言 Base64 编码/解码工具库

[English](#english) | [中文](#中文)

<a name="中文"></a>
## 中文

### 简介

`base64_utils` 是一个纯 C 语言实现的 Base64 编码/解码工具库，提供标准 Base64、Base64URL 以及自定义字符集的编码解码功能。零外部依赖，适合嵌入式系统和跨平台应用。

### 功能特性

- ✅ **标准 Base64 编码/解码** - RFC 4648 标准实现
- ✅ **Base64URL 支持** - URL 安全编码（`-` 和 `_` 替代 `+` 和 `/`）
- ✅ **自定义字符集** - 支持任意 64 字符字符集
- ✅ **PEM 格式输出** - 支持带换行的编码（适合证书、密钥等）
- ✅ **二进制数据处理** - 任意字节序列编码
- ✅ **文件操作** - 直接编码/解码文件内容
- ✅ **字符串便捷函数** - 简化字符串操作
- ✅ **十六进制支持** - 十六进制字符串转 Base64
- ✅ **验证函数** - 输入有效性检查
- ✅ **零外部依赖** - 仅使用标准 C 库

### 快速开始

#### 编译

```bash
# 编译库
gcc -c base64_utils.c -o base64_utils.o

# 编译测试
gcc base64_utils_test.c base64_utils.c -o base64_utils_test

# 编译示例
gcc example.c base64_utils.c -o example
```

#### 基础用法

```c
#include "base64_utils.h"
#include <stdio.h>

int main(void) {
    // 编码字符串
    const char* message = "Hello, World!";
    char encoded[256];
    
    size_t len = base64_encode((const unsigned char*)message, 
                                strlen(message), encoded, sizeof(encoded));
    printf("Encoded: %s\n", encoded);  // 输出: SGVsbG8sIFdvcmxkIQ==
    
    // 解码字符串
    unsigned char decoded[256];
    size_t dec_len = base64_decode(encoded, len, decoded, sizeof(decoded));
    decoded[dec_len] = '\0';
    printf("Decoded: %s\n", (char*)decoded);  // 输出: Hello, World!
    
    return 0;
}
```

### API 参考

#### 编码函数

```c
// 计算编码所需缓冲区大小
size_t base64_encode_length(size_t input_len);

// 标准 Base64 编码
size_t base64_encode(const unsigned char* input, size_t input_len,
                     char* output, size_t output_size);

// Base64URL 编码（无填充）
size_t base64url_encode(const unsigned char* input, size_t input_len,
                         char* output, size_t output_size);

// PEM 格式编码（带换行）
size_t base64_encode_with_lines(const unsigned char* input, size_t input_len,
                                 char* output, size_t output_size,
                                 size_t line_width);
```

#### 解码函数

```c
// 计算解码所需缓冲区大小
size_t base64_decode_length(const char* input, size_t input_len);

// 标准 Base64 解码
size_t base64_decode(const char* input, size_t input_len,
                     unsigned char* output, size_t output_size);

// Base64URL 解码
size_t base64url_decode(const char* input, size_t input_len,
                        unsigned char* output, size_t output_size);
```

#### 验证函数

```c
// 验证 Base64 字符串有效性
bool base64_is_valid(const char* input, size_t input_len);

// 验证 Base64URL 字符串有效性
bool base64url_is_valid(const char* input, size_t input_len);
```

#### 字符串便捷函数

```c
// 编码字符串（返回新分配的字符串）
char* base64_encode_string(const char* str);

// 解码字符串（返回新分配的缓冲区）
unsigned char* base64_decode_string(const char* input, size_t* output_len);

// 十六进制字符串转 Base64
char* base64_encode_hex(const char* hex);
```

#### 文件操作

```c
// 编码文件内容
size_t base64_encode_file(const char* filepath, char* output, size_t output_size);

// 解码到文件
bool base64_decode_to_file(const char* input, size_t input_len, const char* filepath);
```

### 使用示例

#### 二进制数据编码

```c
unsigned char binary[] = {0x00, 0xFF, 0xAB, 0xCD};
char encoded[64];
size_t len = base64_encode(binary, 4, encoded, sizeof(encoded));
// 输出: /w/q0==
```

#### URL 安全编码

```c
const char* data = "filename.txt?query=value";
char encoded[128];
base64url_encode((const unsigned char*)data, strlen(data), encoded, sizeof(encoded));
// 输出不含 + 和 / 字符，可直接用于 URL
```

#### PEM 格式（证书风格）

```c
unsigned char key_data[256];
char pem_encoded[512];
base64_encode_with_lines(key_data, 256, pem_encoded, sizeof(pem_encoded), 64);
// 每 64 字符换行，适合证书文件格式
```

### 性能建议

1. **预分配缓冲区** - 使用 `base64_encode_length()` 和 `base64_decode_length()` 预先计算大小
2. **批量处理** - 大数据一次性处理比分块更高效
3. **URL 安全** - 使用 `base64url_*` 函数避免后续字符串替换
4. **先验证** - 解码前用 `base64_is_valid()` 检查输入

### 错误处理

```c
size_t result = base64_decode(input, len, output, size);
if (result == (size_t)-1) {
    printf("Error: %s\n", base64_get_error());
}
```

---

<a name="english"></a>
## English

### Introduction

`base64_utils` is a pure C implementation of Base64 encoding/decoding with zero external dependencies. Supports standard Base64, Base64URL, and custom character sets.

### Features

- ✅ Standard Base64 encode/decode (RFC 4648)
- ✅ Base64URL support (URL-safe encoding)
- ✅ Custom character sets
- ✅ PEM-style output (with line breaks)
- ✅ Binary data handling
- ✅ File operations
- ✅ String convenience functions
- ✅ Hex to Base64 conversion
- ✅ Validation functions
- ✅ Zero external dependencies

### Quick Start

#### Build

```bash
gcc base64_utils_test.c base64_utils.c -o test
gcc example.c base64_utils.c -o example
```

#### Basic Usage

```c
#include "base64_utils.h"

char encoded[256];
base64_encode((unsigned char*)"Hello", 5, encoded, sizeof(encoded));
// encoded = "SGVsbG8="

unsigned char decoded[256];
size_t len = base64_decode("SGVsbG8=", 8, decoded, sizeof(decoded));
// decoded = "Hello"
```

### API Reference

| Function | Description |
|----------|-------------|
| `base64_encode()` | Standard Base64 encoding |
| `base64_decode()` | Standard Base64 decoding |
| `base64url_encode()` | URL-safe encoding (no padding) |
| `base64url_decode()` | URL-safe decoding |
| `base64_encode_with_lines()` | PEM-style encoding |
| `base64_is_valid()` | Validate Base64 string |
| `base64_encode_string()` | Encode C string (allocates) |
| `base64_decode_string()` | Decode to C string (allocates) |
| `base64_encode_file()` | Encode file contents |
| `base64_decode_to_file()` | Decode to file |

### License

MIT License - Part of AllToolkit project.