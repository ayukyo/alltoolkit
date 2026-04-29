# hamming_code_utils - 汉明码编解码工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./hamming_code_utils_test.py)

零依赖的汉明码实现，支持错误检测和纠正。

## 特性

- **Hamming(7,4)**: 标准 7 位汉明码（4 数据位 + 3 校验位）
- **Hamming(8,4)**: 扩展 8 位汉明码（额外总校验位，可检测双比特错误）
- **单比特纠错**: 自动检测并纠正单比特错误
- **双比特检错**: 扩展模式可检测双比特错误
- **流式处理**: 支持多字节数据编解码
- **零依赖**: 纯 Python 实现

## 安装

```python
from hamming_code_utils import (
    HammingCode,
    HammingStream,
    encode,
    decode,
    hamming_distance,
    generate_hamming_table,
    calculate_code_rate
)
```

## 快速开始

### 基础编码

```python
from hamming_code_utils import HammingCode

# 创建编码器（标准 Hamming(7,4)）
hamming = HammingCode(extended=False)

# 编码 4 位数据 (0-15)
data = 10  # 1010
code = hamming.encode(data)
print(f"数据: {data:04b} -> 编码: {code:07b}")

# 解码（支持错误纠正）
decoded, error_pos = hamming.decode(code)
print(f"解码: {decoded:04b}, 错误位置: {error_pos}")
```

### 错误纠正演示

```python
from hamming_code_utils import HammingCode

hamming = HammingCode(extended=False)

# 编码数据
original_data = 5  # 0101
code = hamming.encode(original_data)
print(f"原始编码: {code:07b}")

# 引入单比特错误
corrupted = hamming.introduce_error(code, position=2)
print(f"损坏编码: {corrupted:07b}")

# 解码并纠正
decoded, error_pos = hamming.decode(corrupted)
print(f"解码数据: {decoded}, 错误位置: {error_pos}")
print(f"纠正成功: {decoded == original_data}")
```

### 扩展汉明码

```python
from hamming_code_utils import HammingCode

# 扩展模式可检测双比特错误
hamming_ext = HammingCode(extended=True)

data = 7
code = hamming_ext.encode(data)
print(f"Hamming(8,4) 编码: {code:08b}")

# 解码
decoded, error_pos = hamming_ext.decode(code)
```

### 流式编解码

```python
from hamming_code_utils import HammingStream

stream = HammingStream(extended=True)

# 编码字节数据
data = b"Hello"
codes = stream.encode_bytes(data)
print(f"编码后: {codes}")

# 解码
decoded, errors = stream.decode_bytes(codes)
print(f"解码后: {decoded}")
print(f"错误位置: {errors}")
```

### 便捷函数

```python
from hamming_code_utils import encode, decode, hamming_distance

# 快速编码
code = encode(10)  # Hamming(7,4)
code_ext = encode(10, extended=True)  # Hamming(8,4)

# 快速解码
data, error_pos = decode(code)

# 计算汉明距离
dist = hamming_distance(0b1010101, 0b1110101)
print(f"汉明距离: {dist}")  # 1
```

## API 参考

### HammingCode 类

#### 构造函数
```python
HammingCode(extended=False)
```
- `extended`: 是否使用扩展模式（Hamming(8,4)）

#### 方法

| 方法 | 参数 | 返回 | 说明 |
|-----|------|-----|------|
| `encode(data)` | int (0-15) | int | 编码 4 位数据 |
| `decode(code)` | int | Tuple[int, Optional[int]] | 解码，返回 (数据, 错误位置) |
| `is_valid(code)` | int | Tuple[bool, Optional[int]] | 检查编码是否有效 |
| `introduce_error(code, pos)` | int, int | int | 在指定位置引入错误 |
| `encode_bits(bits)` | List[int] | List[int] | 编码 4 位列表 |
| `decode_bits(bits)` | List[int] | Tuple[List[int], Optional[int]] | 解码位列表 |

### HammingStream 类

用于多字节数据的流式编解码。

| 方法 | 说明 |
|-----|------|
| `encode_bytes(data)` | 编码字节数据 |
| `decode_bytes(codes)` | 解码为字节数据 |
| `encode_to_bits(data)` | 编码为位列表 |
| `decode_from_bits(bits)` | 从位列表解码 |

### 工具函数

| 函数 | 说明 |
|-----|------|
| `hamming_distance(code1, code2)` | 计算两个编码的汉明距离 |
| `generate_hamming_table(extended)` | 生成所有 16 个值的编码表 |
| `calculate_code_rate(extended)` | 计算编码效率 |

## 理论背景

### Hamming(7,4) 编码

- **数据位**: 4 位
- **校验位**: 3 位
- **总长度**: 7 位
- **编码效率**: 4/7 ≈ 57%
- **纠错能力**: 单比特错误纠正

### Hamming(8,4) 扩展编码

- **额外校验位**: 1 位总校验
- **总长度**: 8 位
- **编码效率**: 50%
- **额外能力**: 可检测双比特错误

## 测试

```bash
python -m pytest hamming_code_utils_test.py -v
```

## 许可证

MIT License