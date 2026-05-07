# Huffman Encoding Utils

零依赖的哈夫曼编码工具库，用于文本压缩和编码分析。

## 功能特性

- 🌳 **哈夫曼树构建** - 基于字符频率自动构建最优二叉树
- 📝 **文本编码** - 将文本转换为变长二进制编码
- 🔄 **完全解码** - 将二进制编码无损还原为原始文本
- 📊 **频率分析** - 统计字符出现频率和百分比
- 📈 **压缩统计** - 计算压缩率、节省空间等指标
- 🎨 **树可视化** - 生成ASCII树形结构图
- 💾 **序列化支持** - 可导出/导入编码器状态
- 🌐 **Unicode支持** - 完美支持中文、表情符号等

## 安装

无需安装，纯Python标准库实现，零外部依赖。

## 快速开始

```python
from huffman_encoding_utils import HuffmanEncoder, huffman_encode, huffman_decode

# 方法1: 使用类
encoder = HuffmanEncoder()
encoder.build_tree("hello world")
encoded = encoder.encode("hello world")
decoded = encoder.decode(encoded)
print(f"编码: {encoded}")
print(f"解码: {decoded}")

# 方法2: 使用便捷函数
encoded, encoder = huffman_encode("你好世界")
decoded = huffman_decode(encoded, encoder)
print(decoded)  # 输出: 你好世界
```

## API 参考

### HuffmanEncoder 类

主要的编码器类。

#### 方法

| 方法 | 说明 |
|------|------|
| `build_tree(text)` | 根据文本构建哈夫曼树 |
| `encode(text)` | 编码文本为二进制字符串 |
| `decode(encoded)` | 解码二进制字符串为原始文本 |
| `get_frequency_table(text)` | 获取字符频率表 |
| `get_code_table()` | 获取编码表 |
| `calculate_compression_stats(text)` | 计算压缩统计信息 |
| `visualize_tree()` | 生成树的可视化表示 |
| `to_dict()` | 序列化编码器状态 |
| `from_dict(data)` | 从字典恢复编码器 |

### 便捷函数

```python
# 快捷编码
encoded, encoder = huffman_encode(text)

# 快捷解码
decoded = huffman_decode(encoded, encoder)

# 分析文本
analysis = analyze_text(text)
# 返回: {
#   'text_length': ...,
#   'frequency_table': {...},
#   'code_table': {...},
#   'compression_stats': {...},
#   'tree_visualization': '...'
# }

# 与固定长度编码比较
comparison = compare_with_fixed_encoding(text)
```

## 使用示例

### 基本编解码

```python
from huffman_encoding_utils import HuffmanEncoder

encoder = HuffmanEncoder()

# 构建树并编码
text = "this is an example for huffman encoding"
encoded = encoder.encode(text)
decoded = encoder.decode(encoded)

print(f"原文: {text}")
print(f"编码: {encoded}")
print(f"解码: {decoded}")
print(f"验证: {decoded == text}")  # True
```

### 压缩统计

```python
from huffman_encoding_utils import HuffmanEncoder

encoder = HuffmanEncoder()
encoder.build_tree("aabbbc")

stats = encoder.calculate_compression_stats("aabbbc")
print(f"原始大小: {stats['original_size_bits']} bits")
print(f"编码大小: {stats['encoded_size_bits']} bits")
print(f"压缩率: {stats['compression_ratio']:.3f}")
print(f"节省空间: {stats['space_saved_percent']:.1f}%")
print(f"平均编码长度: {stats['average_code_length']:.2f} bits/字符")
```

### 频率分析

```python
from huffman_encoding_utils import HuffmanEncoder

encoder = HuffmanEncoder()
freq = encoder.get_frequency_table("hello world")

for char, (count, percent) in freq.items():
    print(f"'{char}': {count}次 ({percent:.1f}%)")
```

### 树可视化

```python
from huffman_encoding_utils import HuffmanEncoder

encoder = HuffmanEncoder()
encoder.build_tree("aabbbc")

print(encoder.visualize_tree())
# 输出示例:
# └── * (6)
#     ├── b (3)
#     └── * (3)
#         ├── a (2)
#         └── c (1)
```

### 序列化与恢复

```python
from huffman_encoding_utils import HuffmanEncoder

# 创建并训练编码器
encoder = HuffmanEncoder()
encoder.build_tree("training data")

# 序列化
data = encoder.to_dict()

# 在其他地方恢复
restored = HuffmanEncoder.from_dict(data)
encoded = restored.encode("training data")
```

### 中文支持

```python
from huffman_encoding_utils import HuffmanEncoder

encoder = HuffmanEncoder()
text = "你好世界，这是哈夫曼编码测试"
encoded = encoder.encode(text)
decoded = encoder.decode(encoded)

print(f"原文: {text}")
print(f"验证: {decoded == text}")  # True
```

## 测试

运行测试：

```bash
python -m pytest huffman_encoding_utils_test.py -v
```

或直接运行：

```bash
python huffman_encoding_utils_test.py
```

## 算法说明

哈夫曼编码是一种经典的无损数据压缩算法：

1. **统计频率** - 计算文本中每个字符的出现频率
2. **构建优先队列** - 创建最小堆，频率低的优先
3. **构建哈夫曼树** - 反复合并频率最低的两个节点
4. **生成编码表** - 左子树为0，右子树为1
5. **编码文本** - 根据编码表将字符转换为二进制串

**特点**：
- 无前缀编码：没有任何编码是另一个编码的前缀
- 最优编码：对于给定的字符频率分布，产生最短的编码
- 变长编码：频率高的字符使用更短的编码

## 适用场景

- 数据压缩教学演示
- 文本压缩算法原型
- 编码理论实验
- 信息论基础学习
- 自定义压缩格式

## 限制

- 编码表需要与编码数据一起传输
- 对于小数据量，开销可能大于收益
- 不适合已压缩数据（如图片、视频）

## 许可证

MIT License

## 更新日志

- 2026-04-28: 初始版本发布