# LZ77 Utils - LZ77 压缩算法工具库

零依赖的 LZ77 无损压缩实现。LZ77 是一种基于滑动窗口的压缩算法，是 DEFLATE、gzip、PNG、ZIP 等现代压缩格式的基础。

## 功能特性

- **LZ77 编码** - 滑动窗口压缩算法实现
- **可配置参数** - 窗口大小、前瞻缓冲区、最小匹配长度
- **预设配置** - fast/balanced/maximum/small 四种预设
- **多格式支持** - 字符串和字节数据处理
- **令牌表示** - 结构化的令牌对象，便于分析
- **流式处理** - StreamingLZ77Encoder 支持分块处理
- **压缩分析** - 压缩率、匹配长度分布等统计
- **往返验证** - 自动验证压缩/解压完整性
- **零外部依赖** - 纯 Python 标准库实现

## 快速开始

### 基础压缩

```python
from lz77_utils.mod import LZ77Compressor

# 创建压缩器
compressor = LZ77Compressor()

# 压缩数据
data = "hellohellohellohello"
result = compressor.compress(data)

print(f"原始大小: {result.original_size} 字节")
print(f"压缩后大小: {result.compressed_size} 字节")
print(f"压缩率: {result.compression_ratio:.2f}")
print(f"空间节省: {result.space_saving:.1f}%")
print(f"匹配令牌数: {result.match_count}")
print(f"字面量数: {result.literal_count}")
```

### 解压数据

```python
from lz77_utils.mod import LZ77Compressor

compressor = LZ77Compressor()

# 压缩
result = compressor.compress("abcabcabcabc")

# 解压
decoded = compressor.decompress_to_string(result.tokens)
print(decoded)  # 输出: abcabcabcabc
```

### 使用预设

```python
from lz77_utils.mod import LZ77Compressor

# 快速压缩（小窗口，速度快）
fast = LZ77Compressor.fast()
result1 = fast.compress(data)

# 平衡压缩（默认）
balanced = LZ77Compressor.balanced()
result2 = balanced.compress(data)

# 最大压缩（大窗口，压缩率高）
maximum = LZ77Compressor.maximum()
result3 = maximum.compress(data)

# 比较效果
print(f"Fast 压缩率: {result1.compression_ratio:.2f}")
print(f"Balanced 压缩率: {result2.compression_ratio:.2f}")
print(f"Maximum 压缩率: {result3.compression_ratio:.2f}")
```

### 便捷函数

```python
from lz77_utils.mod import lz77_compress, lz77_decode_to_string

# 快速压缩
result = lz77_compress("repeated data repeated data", preset='balanced')

# 快速解压
decoded = lz77_decode_to_string(result.tokens)
```

### 压缩分析

```python
from lz77_utils.mod import analyze_lz77, compare_presets

# 分析压缩特性
data = "abcabcabcabcabcabc"
analysis = analyze_lz77(data)

print(f"最大匹配长度: {analysis['max_match_length']}")
print(f"平均匹配长度: {analysis['avg_match_length']:.2f}")
print(f"匹配长度分布: {analysis['match_lengths_distribution']}")

# 比较不同预设
comparison = compare_presets(data)
for preset, stats in comparison.items():
    print(f"{preset}: 压缩率={stats['compression_ratio']:.2f}, "
          f"节省={stats['space_saving']:.1f}%")
```

## 核心类

### LZ77Token

令牌对象，表示编码单元。

```python
from lz77_utils.mod import LZ77Token

# 字面量令牌（单个字符/字节）
literal = LZ77Token.literal(65)  # 'A'
print(literal.is_literal)  # True

# 匹配令牌（从窗口复制）
match = LZ77Token.match(offset=10, length=5)
print(match.is_match)  # True
```

### LZ77Result

压缩结果对象。

```python
result = compressor.compress(data)

# 属性
result.tokens           # 令牌列表
result.original_size    # 原始大小
result.compressed_size  # 压缩后大小
result.literal_count    # 字面量数量
result.match_count      # 匹配数量
result.compression_ratio # 压缩率（原始/压缩）
result.space_saving     # 空间节省百分比
result.total_tokens     # 总令牌数
result.match_ratio      # 匹配占比
```

### LZ77Encoder

编码器类。

```python
from lz77_utils.mod import LZ77Encoder

# 创建编码器
encoder = LZ77Encoder(
    window_size=4096,      # 搜索窗口大小
    look_ahead_size=18,    # 前瞻缓冲区大小
    min_match_length=3     # 最小匹配长度
)

# 编码
result = encoder.encode("abcabcabc")

# 编码为元组
tuples = encoder.encode_to_tuples("data")

# 流式编码
for token in encoder.encode_iter("data"):
    print(token)
```

### LZ77Decoder

解码器类。

```python
from lz77_utils.mod import LZ77Decoder

decoder = LZ77Decoder()

# 解码为字节
decoded_bytes = decoder.decode(tokens)

# 解码为字符串
decoded_str = decoder.decode_to_string(tokens)

# 从元组解码
decoded = decoder.decode_tuples([(0, 0, 65), (2, 2, None)])
```

### StreamingLZ77Encoder

流式编码器，支持分块处理。

```python
from lz77_utils.mod import StreamingLZ77Encoder

encoder = StreamingLZ77Encoder(window_size=100)

# 分块输入
chunk1_tokens = encoder.feed("abcabc")
chunk2_tokens = encoder.feed("abcabc")
remaining_tokens = encoder.flush()

# 合并所有令牌
all_tokens = chunk1_tokens + chunk2_tokens + remaining_tokens

# 解码
decoder = LZ77Decoder()
decoded = decoder.decode(all_tokens)
```

## 预设配置

| 预设 | 窗口大小 | 前瞻缓冲区 | 最小匹配 | 适用场景 |
|------|----------|------------|----------|----------|
| fast | 1024 | 15 | 3 | 实时压缩，低延迟 |
| balanced | 4096 | 18 | 3 | 通用场景，平衡压缩率和速度 |
| maximum | 32768 | 258 | 3 | 最大压缩，离线处理 |
| small | 256 | 15 | 2 | 小数据，嵌入式系统 |

## 算法原理

LZ77 算法使用滑动窗口方法：

1. **窗口结构**
   - 搜索窗口：已编码的数据，用于查找匹配
   - 前瞻缓冲区：待编码的数据

2. **编码过程**
   - 在搜索窗口中查找前瞻缓冲区的最长匹配
   - 如果找到足够长的匹配，输出 `(offset, length)` 对
   - 否则输出字面量（单个字符/字节）

3. **解码过程**
   - 字面量：直接输出字符
   - 匹配：从已解码数据中按偏移和长度复制

4. **时间复杂度**
   - 编码：O(n × window_size × look_ahead_size)
   - 解码：O(n)

## API 参考

### 便捷函数

| 函数 | 描述 |
|------|------|
| `lz77_encode(data, ...)` | LZ77 编码 |
| `lz77_decode(tokens)` | 解码为字节 |
| `lz77_decode_to_string(tokens)` | 解码为字符串 |
| `lz77_compress(data, preset)` | 使用预设压缩 |
| `analyze_lz77(data)` | 分析压缩特性 |
| `compare_presets(data)` | 比较不同预设效果 |

### LZ77Compressor 方法

| 方法 | 描述 |
|------|------|
| `compress(data)` | 压缩数据 |
| `decompress(tokens)` | 解压为字节 |
| `decompress_to_string(tokens)` | 解压为字符串 |
| `roundtrip(data)` | 压缩并验证完整性 |

## 应用场景

- 文本压缩（日志、配置文件）
- 数据传输优化
- 压缩算法学习和研究
- 实现自定义压缩格式
- 游戏资源压缩
- 通信协议数据压缩

## 测试

```bash
python lz77_utils_test.py
```

测试覆盖：
- 编码器和解码器功能
- 字符串和字节数据处理
- 流式编码
- 预设配置
- 边界条件
- 数据完整性验证

## 许可证

MIT License