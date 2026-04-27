# Ulid Utils


ULID (Universally Unique Lexicographically Sortable Identifier) Utils

A pure Python implementation of ULID - a 26-character, lexicographically 
sortable unique identifier that is URL-safe and uses Crockford's Base32 encoding.

Features:
- Generate ULIDs with timestamp component
- Parse ULIDs to extract timestamp and random components
- Validate ULIDs
- Convert between ULID and other formats (UUID, hex, bytes)
- Monotonic ULID generation (incrementing within same millisecond)

ULID Structure:
- 48 bits timestamp (milliseconds since Unix epoch)
- 80 bits randomness
- Total: 128 bits = 26 characters in Crockford's Base32

Example:
    >>> from ulid_utils import ULID
    >>> ulid = ULID.generate()
    >>> print(ulid)
    01ARZ3NDEKTSV4RRFFQ69G5FAV
    >>> ulid.timestamp()
    1505945976.341


## 功能

### 类

- **ULIDError**: Exception raised for ULID-related errors
- **ULID**: ULID (Universally Unique Lexicographically Sortable Identifier) class
  方法: generate, from_datetime, from_uuid, from_hex, from_int ... (16 个方法)

### 函数

- **generate(timestamp_ms**) - Generate a new ULID.
- **parse(ulid_str**) - Parse a ULID string.
- **is_valid(ulid_str**) - Check if a string is a valid ULID.
- **monotonic(last**) - Generate a monotonic ULID.
- **from_datetime(dt**) - Create a ULID from datetime.
- **from_uuid(uuid_obj**) - Create a ULID from UUID.
- **from_hex(hex_str**) - Create a ULID from hex string.
- **from_int(value**) - Create a ULID from integer.
- **generate_batch(count, timestamp_ms**) - Generate multiple ULIDs.
- **generate_monotonic_batch(count**) - Generate a batch of monotonic ULIDs.

... 共 30 个函数

## 使用示例

```python
from mod import generate

# 使用 generate
result = generate()
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
