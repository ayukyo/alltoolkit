# Adler-32 Utils - 校验和工具 🧮

[![测试状态](https://img.shields.io/badge/tests-passed-brightgreen)]()
[![覆盖率](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

Adler-32 校验和计算工具，零外部依赖，纯 Python 实现。

---

## ✨ 功能特性

### 核心计算
- **基础校验和**：计算数据的 Adler-32 校验值
- **详细结果**：返回校验值、A/B 分量、十六进制表示
- **十六进制转换**：支持整数与十六进制字符串互转

### 流式计算
- **流式更新**：支持增量计算，适合大文件
- **分块处理**：避免内存溢出
- **重置功能**：可重新开始计算

### 文件操作
- **文件校验和**：计算文件的 Adler-32 值
- **批量验证**：验证文件完整性
- **分块读取**：64KB 分块，高效处理大文件

### 组合校验
- **Adler-32 + CRC-32**：双重校验提供更好的错误检测
- **交叉验证**：同时验证两种校验和

### 统计信息
- **字节统计**：字节数、总和、平均值、最值
- **A/B 分量**：分解 Adler-32 的 A 和 B 值

---

## 🚀 快速开始

### 基础用法

```python
from adler32_utils import adler32, adler32_hex

# 基础校验和
print(adler32(b'Hello'))           # 93061621
print(adler32_hex(b'Hello'))       # '058c01f5'

# 字符串输入
print(adler32('Hello'))            # 93061621
```

### 详细结果

```python
from adler32_utils import adler32_detailed

result = adler32_detailed(b'Hello')
print(f"Value: {result.value}")    # 93061621
print(f"Hex: {result.hex}")        # '058c01f5'
print(f"A: {result.a}")            # 501
print(f"B: {result.b}")            # 5640
```

### 流式计算

```python
from adler32_utils import Adler32Streaming

stream = Adler32Streaming()
stream.update(b'Hello')
stream.update(b' World')
print(stream.value)                # 403375133
print(stream.hex)                 # '180b041d'
print(stream.byte_count)           # 11
```

### 文件校验

```python
from adler32_utils import adler32_file, verify_file_adler32

# 计算文件校验和
result = adler32_file('data.bin')
print(result.hex)                  # '02b10305'

# 验证文件
is_valid = verify_file_adler32('data.bin', '02b10305')
print(is_valid)                     # True/False
```

---

## 📚 详细用法

### 增量计算

```python
from adler32_utils import adler32

# 使用初始值进行增量计算
checksum1 = adler32(b'Hello')
checksum2 = adler32(b' World', initial=checksum1)
print(checksum2)                   # 403375133 (与直接计算 b'Hello World' 相同)
```

### 组合校验和

```python
from adler32_utils import compute_combined_checksum, verify_combined_checksum

# 计算双重校验和
adler, crc = compute_combined_checksum(b'Hello')
print(f"Adler-32: {adler}")        # '058c01f5'
print(f"CRC-32: {crc}")           # 'f7ff9e8b'

# 验证
is_valid = verify_combined_checksum(b'Hello', '058c01f5', 'f7ff9e8b')
print(is_valid)                    # (True, True)
```

### A/B 组件操作

```python
from adler32_utils import decompose_adler32, compose_adler32

# 分解
a, b = decompose_adler32(93061621)
print(f"A: {a}, B: {b}")           # A: 501, B: 5640

# 组合
value = compose_adler32(501, 5640)
print(value)                       # 93061621
```

### 比较两个数据

```python
from adler32_utils import compare_adler32

# 比较校验和
print(compare_adler32(b'Hello', b'Hello'))  # True
print(compare_adler32(b'Hello', b'World'))  # False
```

### 统计信息

```python
from adler32_utils import adler32_statistics

stats = adler32_statistics(b'Hello World')
print(stats['checksum'])            # 403375133
print(stats['byte_count'])          # 11
print(stats['byte_average'])        # 87.0
```

### 自检

```python
from adler32_utils import test_adler32

result = test_adler32()
print(result)                       # True (所有测试通过)
```

---

## 🔧 API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `adler32(data, initial=1)` | 计算 Adler-32 校验和 |
| `adler32_detailed(data, initial=1)` | 返回详细结果（含 A/B 分量） |
| `adler32_hex(data)` | 返回十六进制字符串 |

### 流式类

| 类 | 说明 |
|------|------|
| `Adler32Streaming(initial=1)` | 流式计算器 |

### 文件函数

| 函数 | 说明 |
|------|------|
| `adler32_file(file_path, chunk_size=65536)` | 计算文件校验和 |
| `adler32_file_hex(file_path)` | 返回文件校验和（十六进制） |
| `verify_file_adler32(file_path, expected)` | 验证文件校验和 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `verify_adler32(data, expected)` | 验证数据校验和 |
| `compare_adler32(data1, data2)` | 比较两个数据校验和 |
| `compute_combined_checksum(data)` | 计算 Adler-32 + CRC-32 |
| `verify_combined_checksum(data, adler, crc)` | 验证双重校验和 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `adler32_to_hex(value)` | 整数转十六进制 |
| `hex_to_adler32(hex_string)` | 十六进制转整数 |
| `decompose_adler32(value)` | 分解为 A/B |
| `compose_adler32(a, b)` | 从 A/B 组合 |
| `adler32_statistics(data)` | 统计信息 |

### 数据类

| 类 | 说明 |
|------|------|
| `Adler32Result` | 包含 value, hex, a, b |

---

## 📊 算法说明

### Adler-32 算法

Adler-32 是用于检测数据错误的校验算法，比 CRC-32 更快但可靠性稍低。

**公式**：
```
Adler-32 = (B × 65536 + A) mod 2^32
其中：
    A = sum(all_bytes) + 1
    B = sum(all_A_values)
```

**模数**：65521（小于 2^16 的最大素数）

### 应用场景

- **zlib 压缩格式**：zlib 使用 Adler-32 作为默认校验和
- **ZIP 文件格式**：用于检测压缩数据完整性
- **快速校验**：适合对性能要求高但错误检测要求适中的场景

### 与 CRC-32 比较

| 特性 | Adler-32 | CRC-32 |
|------|-----------|--------|
| 速度 | 更快 | 较慢 |
| 可靠性 | 较低 | 较高 |
| 错误检测 | 短数据更优 | 长数据更优 |

---

## 🧪 测试

```bash
# 运行所有测试
python -m pytest adler32_utils/ -v

# 运行特定测试文件
python -m pytest adler32_utils/adler32_utils_test.py -v

# 快速测试
python -m pytest adler32_utils -q
```

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-06-08