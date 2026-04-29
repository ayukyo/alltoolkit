# varint_utils - 变长整数编解码工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./varint_utils_test.py)

零依赖的变长整数（Varint）编解码工具，广泛用于 Protocol Buffers、数据库和网络协议。

## 特性

- **无符号变长整数**: 支持 64 位无符号整数编码
- **有符号变长整数**: ZigZag 编码支持负数
- **批量编解码**: 高效的批量处理
- **流式支持**: 处理大数据集的流式接口
- **零依赖**: 纯 Python 实现

## 安装

```python
from varint_utils import (
    encode_unsigned,
    decode_unsigned,
    encode_signed,
    decode_signed,
    encode_batch,
    decode_batch
)
```

## 快速开始

### 无符号变长整数

```python
from varint_utils import encode_unsigned, decode_unsigned

# 编码
encoded = encode_unsigned(300)
print(encoded)  # b'\xac\x02'

# 解码
decoded, bytes_read = decode_unsigned(encoded)
print(decoded)  # 300

# 小数值只占 1 字节
encoded = encode_unsigned(1)
print(encoded)  # b'\x01'
```

### 有符号变长整数（ZigZag 编码）

```python
from varint_utils import encode_signed, decode_signed

# ZigZag 编码将负数映射到正数
# -1 → 1, 1 → 2, -2 → 3, 2 → 4, ...

# 编码
encoded = encode_signed(-1)
print(encoded)  # b'\x01'

# 解码
decoded, bytes_read = decode_signed(encoded)
print(decoded)  # -1
```

### 批量处理

```python
from varint_utils import encode_batch, decode_batch

# 批量编码
values = [1, 300, 16384, 1000000]
encoded = encode_batch(values)
print(encoded)  # 所有值编码后的字节序列

# 批量解码
decoded = decode_batch(encoded)
print(decoded)  # [1, 300, 16384, 1000000]
```

### 流式处理

```python
from varint_utils import stream_encode, stream_decode

# 流式编码
for encoded in stream_encode([1, 2, 3]):
    print(encoded)

# 流式解码
for value in stream_decode(byte_stream):
    print(value)
```

## API 参考

### 无符号编解码

| 函数 | 说明 |
|-----|------|
| `encode_unsigned(value)` | 编码无符号整数 |
| `decode_unsigned(data)` | 解码无符号整数，返回 (值, 字节数) |
| `encode_batch(values)` | 批量编码 |
| `decode_batch(data)` | 批量解码 |

### 有符号编解码（ZigZag）

| 函数 | 说明 |
|-----|------|
| `encode_signed(value)` | 编码有符号整数（ZigZag） |
| `decode_signed(data)` | 解码有符号整数 |
| `zigzag_encode(n)` | ZigZag 编码 |
| `zigzag_decode(n)` | ZigZag 解码 |

### 流式处理

| 函数 | 说明 |
|-----|------|
| `stream_encode(values)` | 流式编码迭代器 |
| `stream_decode(data)` | 流式解码迭代器 |

## 编码原理

### 变长整数编码

- 使用 7 位存储数值
- 第 8 位（MSB）为延续位
- 延续位 = 1 表示还有更多字节
- 延续位 = 0 表示这是最后一个字节

### 编码长度

| 数值范围 | 字节数 |
|---------|--------|
| 0 - 127 | 1 字节 |
| 128 - 16383 | 2 字节 |
| 16384 - 2097151 | 3 字节 |
| 2097152 - 268435455 | 4 字节 |
| 更大 | 5-10 字节 |

### ZigZag 编码公式

```
编码: (n << 1) ^ (n >> 63)
解码: (n >> 1) ^ -(n & 1)
```

这样负数也使用紧凑编码：
- -1 → 1（1 字节）
- -300 → 599（2 字节）

## 测试

```bash
python -m pytest varint_utils_test.py -v
```

## 许可证

MIT License