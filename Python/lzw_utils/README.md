# LZW 工具库

LZW (Lempel-Ziv-Welch) 基于字典的无损压缩算法实现。

## 简介

LZW 是一种经典的字典压缩算法，由 Abraham Lempel、Jacob Ziv 和 Terry Welch 开发。该算法广泛应用于：
- GIF 图像格式
- TIFF 图像格式
- PDF 文档格式
- UNIX compress 压缩工具

## 核心功能

### 基本压缩解压
```python
from lzw_utils.mod import compress, decompress

# 压缩字节数据
original = b"TOBEORNOTTOBEORTOBEORNOT"
compressed = compress(original)

# 解压缩
restored = decompress(compressed)
assert restored == original
```

### 字符串处理
```python
from lzw_utils.mod import compress_string, decompress_string

# 压缩字符串
text = "Hello, World! 你好，世界！"
compressed = compress_string(text)

# 解压为字符串
restored = decompress_string(compressed)
```

### 十六进制格式
```python
from lzw_utils.mod import compress_to_hex, decompress_from_hex

# 压缩为十六进制字符串（适合文本传输）
data = b"重复的数据容易压缩"
hex_str = compress_to_hex(data)

# 从十六进制解压
restored = decompress_from_hex(hex_str)
```

### 压缩统计
```python
from lzw_utils.mod import get_compression_stats

original = b"A" * 10000
compressed = compress(original)
stats = get_compression_stats(original, compressed)

print(f"压缩率: {stats['ratio']:.2%}")
print(f"节省空间: {stats['saved_percent']:.1f}%")
```

### 流式处理
```python
from lzw_utils.mod import compress_stream

# 大数据流式压缩
large_data = b"..." * 1000000
for chunk in compress_stream(large_data, chunk_size=8192):
    # 处理每个压缩块
    output.write(chunk)
```

### GIF 格式兼容
```python
from lzw_utils.mod import compress_gif, decompress_gif

# GIF 图像数据压缩
pixel_data = bytes([0, 1, 2, 0, 1, 2] * 100)
compressed = compress_gif(pixel_data, min_code_size=8)

# 解压 GIF 数据
restored = decompress_gif(compressed, min_code_size=8)
```

## API 文档

### 函数

| 函数 | 描述 |
|------|------|
| `compress(data, ...)` | 压缩字节数据 |
| `decompress(data, ...)` | 解压缩字节数据 |
| `compress_string(text, ...)` | 压缩字符串 |
| `decompress_string(data, ...)` | 解压为字符串 |
| `compress_to_hex(data)` | 压缩为十六进制字符串 |
| `decompress_from_hex(hex_str)` | 从十六进制解压 |
| `get_compression_ratio(orig, comp)` | 计算压缩率 |
| `get_compression_stats(orig, comp)` | 获取压缩统计 |
| `compress_stream(data, chunk_size)` | 流式压缩生成器 |
| `compress_gif(data, min_code_size)` | GIF 格式压缩 |
| `decompress_gif(data, min_code_size)` | GIF 格式解压 |

### 类

| 类 | 描述 |
|----|------|
| `LZWEncoder` | LZW 编码器（支持流式编码） |
| `LZWDecoder` | LZW 解码器（支持流式解码） |

## 压缩效果

LZW 对以下数据类型压缩效果好：
- 重复模式数据（如 `ABABABAB...`）
- 文本数据（如日志、配置文件）
- 结构化数据（如 CSV）

压缩效果较差的数据：
- 高熵数据（随机字节）
- 已压缩数据（再次压缩可能膨胀）

## 特点

- **零外部依赖**：纯 Python 实现
- **可配置位宽**：支持 9-16 位代码宽度
- **流式处理**：支持大文件分块压缩
- **GIF 兼容**：支持 GIF 格式的 LZW 变体
- **完整测试**：包含完整测试套件

## 原理简介

LZW 算法通过构建字典实现压缩：

1. 初始化字典包含所有单字节序列（0-255）
2. 读取输入数据，查找最长匹配序列
3. 输出匹配序列的代码
4. 将新序列（匹配序列 + 下一个字节）添加到字典
5. 重复步骤 2-4

解压时反向操作，根据代码从字典重建原始数据。

## 测试

```bash
cd Python/lzw_utils
python lzw_utils_test.py
```

## 示例

```bash
cd Python/lzw_utils
python examples/usage_examples.py
```

## 版本信息

- 版本：1.0.0
- 日期：2024-04-24
- 语言：Python 3
- 依赖：无（纯 Python 标准库）