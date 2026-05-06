# Encoding Utilities (编码处理工具集)

全面的编码处理工具集，提供多种编码格式的转换、检测和处理功能。零外部依赖，纯 Python 实现（兼容 Python 3.6+）。

## 功能特性

### 📦 Base64 编码

- **base64_encode()** - Base64 编码（支持 URL-safe）
- **base64_decode()** - Base64 解码
- **base64_encode_json()** - JSON 对象 Base64 编码
- **base64_decode_json()** - Base64 解码为 JSON

### 🔢 Base32 编码

- **base32_encode()** - Base32 编码
- **base32_decode()** - Base32 解码

### 🔐 Base58 编码

- **base58_encode()** - Base58 编码（Bitcoin 地址格式）
- **base58_decode()** - Base58 解码

### 🔗 URL 编码

- **url_encode()** - URL 编码
- **url_decode()** - URL 解码
- **url_encode_query()** - URL 查询参数编码
- **url_decode_query()** - URL 查询参数解码
- **url_encode_all()** - 全字符 URL 编码

### 🔬 Hex 编码

- **hex_encode()** - 十六进制编码
- **hex_decode()** - 十六进制解码
- **hex_encode_with_prefix()** - 带 0x 前缀编码
- **hex_decode_with_prefix()** - 支持 0x 前缀解码

### 📧 Quoted-printable

- **quoted_printable_encode()** - Quoted-printable 编码
- **quoted_printable_decode()** - Quoted-printable 解码

### 🌐 Unicode 规范化

- **unicode_normalize_nfc()** - NFC 规范化
- **unicode_normalize_nfd()** - NFD 规范化
- **unicode_normalize_nfkc()** - NFKC 规范化
- **unicode_normalize_nfkd()** - NFKD 规范化
- **unicode_remove_accents()** - 移除重音符号

### 🔍 编码检测

- **detect_base64()** - 检测 Base64
- **detect_hex()** - 检测 Hex
- **detect_url_encoded()** - 检测 URL 编码
- **detect_encoding()** - 自动检测编码类型
- **auto_decode()** - 自动解码字符串

### ⚡ 批量操作

- **batch_encode()** - 批量编码
- **batch_decode()** - 批量解码
- **convert_encoding()** - 编码格式转换

## 安装

零外部依赖，纯 Python 实现：

```python
from encoding_utils.mod import *
```

## 快速开始

### Base64 编码

```python
from encoding_utils.mod import base64_encode, base64_decode

# 基础编码
encoded = base64_encode("Hello World")
print(encoded)  # "SGVsbG8gV29ybGQ"

# 解码
decoded = base64_decode(encoded).decode()
print(decoded)  # "Hello World"

# URL-safe 编码
encoded = base64_encode("Test", url_safe=True)
```

### Base58 编码（Bitcoin 地址）

```python
from encoding_utils.mod import base58_encode, base58_decode

# 编码
encoded = base58_encode("Hello World")
print(encoded)

# 解码
decoded = base58_decode(encoded).decode()
```

### URL 编码

```python
from encoding_utils.mod import url_encode, url_decode, url_encode_query

# 基础编码
encoded = url_encode("Hello World")
print(encoded)  # "Hello%20World"

# 查询参数
params = {"name": "test", "value": 123}
query = url_encode_query(params)
print(query)  # "name=test&value=123"
```

### Unicode 规范化

```python
from encoding_utils.mod import unicode_normalize_nfc, unicode_remove_accents

# NFC 规范化
normalized = unicode_normalize_nfc("café")

# 移除重音
clean = unicode_remove_accents("café")
print(clean)  # "cafe"
```

### 自动检测解码

```python
from encoding_utils.mod import auto_decode

# 自动检测并解码
decoded, encoding = auto_decode("SGVsbG8=")
print(decoded)  # "Hello"
print(encoding)  # "base64"
```

### 编码转换

```python
from encoding_utils.mod import convert_encoding

# Base64 → Hex
hex_str = convert_encoding("SGVsbG8=", 'base64', 'hex')
print(hex_str)  # "48656c6c6f"
```

## 运行测试

```bash
cd Python/encoding_utils
python encoding_utils_test.py
```

## 运行示例

```bash
cd Python/encoding_utils/examples
python usage_examples.py
```

## 应用场景

1. **Web 开发** - URL 参数编码、数据传输
2. **安全应用** - Base58 Bitcoin 地址生成
3. **邮件处理** - Quoted-printable 编解码
4. **数据处理** - 各种编码格式互转
5. **文本处理** - Unicode 规范化、重音移除
6. **API 开发** - Base64 JSON 编码传输

## 特点

- ✅ 零外部依赖
- ✅ 纯 Python 实现
- ✅ 兼容 Python 3.6+
- ✅ 支持 5+ 种编码格式
- ✅ 编码自动检测
- ✅ Unicode 规范化
- ✅ 批量操作支持
- ✅ 完整的测试覆盖

## 作者

AllToolkit 自动化开发

## 版本

1.0.0 (2026-05-07)