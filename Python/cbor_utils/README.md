# CBOR Utils

CBOR (Concise Binary Object Representation) 编解码工具，零依赖。

## 功能特性

- **CBOR 编码**: Python 对象编码为 CBOR 二进制
- **CBOR 解码**: CBOR 二进制解码为 Python 对象
- **类型支持**: 整数、浮点、字符串、列表、字典、字节
- **特殊类型**: 日期时间、UUID、标签数据
- **流式处理**: 支持部分解析

## 快速开始

```python
from cbor_utils.mod import encode, decode

# 编码
data = {"name": "Alice", "age": 30, "items": [1, 2, 3]}
encoded = encode(data)  # CBOR 二进制

# 解码
decoded = decode(encoded)  # {"name": "Alice", "age": 30, "items": [1, 2, 3]}
```

## 使用示例

### 基础类型编码

```python
from cbor_utils.mod import encode, decode

# 整数
encoded = encode(42)
decoded = decode(encoded)  # 42

# 浮点数
encoded = encode(3.14159)
decoded = decode(encoded)  # 3.14159

# 字符串
encoded = encode("Hello CBOR")
decoded = decode(encoded)  # "Hello CBOR"

# 字节
encoded = encode(b'\x01\x02\x03')
decoded = decode(encoded)  # b'\x01\x02\x03'
```

### 复合类型编码

```python
# 列表
encoded = encode([1, 2, 3, "four"])
decoded = decode(encoded)  # [1, 2, 3, "four"]

# 字典
encoded = encode({"key": "value", "number": 123})
decoded = decode(encoded)  # {"key": "value", "number": 123}

# 嵌套结构
data = {
    "user": {
        "id": 1,
        "name": "Alice",
        "tags": ["admin", "user"]
    },
    "count": 100
}
encoded = encode(data)
decoded = decode(encoded)
```

### 特殊类型

```python
from datetime import datetime, date
from uuid import UUID
from cbor_utils.mod import encode, decode, Tag

# 日期时间
dt = datetime(2024, 1, 1, 12, 0, 0)
encoded = encode(dt)
decoded = decode(encoded)  # datetime 对象

# UUID
uuid = UUID('12345678-1234-5678-1234-567812345678')
encoded = encode(uuid)
decoded = decode(encoded)  # UUID 对象

# 标签数据
tagged = Tag(100, "自定义标签数据")
encoded = encode(tagged)
decoded = decode(encoded)  # Tag 对象
```

### 流式解码

```python
from cbor_utils.mod import CBORStreamDecoder

# 流式解码
decoder = CBORStreamDecoder()

# 分块添加数据
decoder.feed(encoded_data[:100])
decoder.feed(encoded_data[100:])

# 获取解码结果
while decoder.has_items():
    item = decoder.get_item()
    print(item)
```

### 文件读写

```python
from cbor_utils.mod import encode_to_file, decode_from_file

# 写入文件
encode_to_file(data, "data.cbor")

# 从文件读取
decoded = decode_from_file("data.cbor")
```

## API 参考

| 函数 | 说明 |
|------|------|
| `encode(obj)` | 编码为 CBOR |
| `decode(data)` | 解码 CBOR |
| `encode_to_file(obj, path)` | 编码并写入文件 |
| `decode_from_file(path)` | 从文件解码 |

### CBORStreamDecoder

| 方法 | 说明 |
|------|------|
| `feed(data)` | 添加数据块 |
| `has_items()` | 是否有待解码项 |
| `get_item()` | 获取解码项 |

### Tag 类

```python
Tag(tag_number, tag_content)  # CBOR 标签数据
```

## CBOR 类型映射

| Python 类型 | CBOR 类型 |
|-------------|-----------|
| int | Major 0/1 (整数) |
| float | Major 7 (浮点) |
| str | Major 3 (文本) |
| bytes | Major 2 (字节) |
| list | Major 4 (数组) |
| dict | Major 5 (映射) |
| bool | Major 7 (简单值) |
| None | Major 7 (null) |
| datetime | Major 6 (标签) |
| UUID | Major 6 (标签) |

---

**测试覆盖**: 完整测试套件，覆盖基础类型、复合类型、特殊类型等