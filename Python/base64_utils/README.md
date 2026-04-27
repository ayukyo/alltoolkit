# Base64 Utils


AllToolkit - Python Base64 Utilities

A zero-dependency, production-ready Base64 encoding/decoding utility module.
Supports standard Base64, URL-safe Base64 (RFC 4648), and binary data handling.

Author: AllToolkit
License: MIT


## 功能

### 类

- **Base64Utils**: Base64 encoding and decoding utilities
  方法: encode, decode, decode_to_bytes, encode_urlsafe, decode_urlsafe ... (11 个方法)

### 函数

- **encode(input_data, encoding**) - Encode string or bytes to Base64.
- **decode(base64_string, encoding**) - Decode Base64 string to regular string.
- **decode_to_bytes(base64_string**) - Decode Base64 string to bytes.
- **encode_urlsafe(input_data, encoding, padding**) - Encode to URL-safe Base64 (RFC 4648).
- **decode_urlsafe(base64_url_string, encoding**) - Decode URL-safe Base64 string to regular string.
- **decode_urlsafe_to_bytes(base64_url_string**) - Decode URL-safe Base64 string to bytes.
- **to_urlsafe(standard_base64, padding**) - Convert standard Base64 to URL-safe Base64.
- **from_urlsafe(base64_url_string**) - Convert URL-safe Base64 to standard Base64.
- **is_valid(base64_string, urlsafe**) - Check if a string is valid Base64.
- **encoded_length(input_length, padding**) - Calculate the length of Base64 encoded output.

... 共 22 个函数

## 使用示例

```python
from mod import encode

# 使用 encode
result = encode()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
