# Arithmetic Coding Utils


Arithmetic Coding Utils - 算术编码工具模块

算术编码是一种高效的无损数据压缩算法，将整个消息编码为一个浮点数。
相比哈夫曼编码，算术编码可以更接近信息熵的理论极限。

核心功能：
1. 静态算术编码/解码 - 使用预定义的概率分布
2. 自适应算术编码/解码 - 动态更新概率分布
3. 模型构建 - 从数据构建概率模型
4. 二进制算术编码 - 专门针对二进制数据的优化

特点：
- 零外部依赖
- 支持任意符号集
- 高精度计算，避免精度损失
- 支持自适应模型


## 功能

### 类

- **ArithmeticModel**: 算术编码概率模型
  方法: update, get_probability, get_cumulative_range, get_symbol_from_range, get_symbols
- **ArithmeticEncoder**: 算术编码器
  方法: encode, encode_to_bits, get_encoded_value
- **ArithmeticDecoder**: 算术解码器
  方法: decode, decode_from_bits
- **BinaryArithmeticEncoder**: 二进制算术编码器

专门针对二进制数据（0/1）优化的编码器
  方法: encode, decode
- **AdaptiveArithmeticCodec**: 自适应算术编解码器

动态更新概率模型，适合分布未知的场景
  方法: encode, decode, get_model
- **ArithmeticCodingSession**: 算术编码会话管理器
  方法: encode, decode

### 函数

- **build_model_from_data(data, smoothing**) - 从数据构建概率模型
- **encode_string(text, adaptive**) - 编码字符串的便捷函数
- **decode_string(code, counts, num_symbols**, ...) - 解码字符串的便捷函数
- **calculate_compression_ratio(original_size, encoded_bits**) - 计算压缩比
- **calculate_theoretical_bits(symbols, model**) - 计算理论最优编码位数（基于信息熵）
- **update(self, symbol, initialize**) - 更新符号计数
- **get_probability(self, symbol**) - 获取符号概率
- **get_cumulative_range(self, symbol**) - 获取符号的累积概率范围 [low, high)
- **get_symbol_from_range(self, value**) - 根据累积概率值获取符号
- **get_symbols(self**) - 获取所有符号

... 共 22 个函数

## 使用示例

```python
from mod import build_model_from_data

# 使用 build_model_from_data
result = build_model_from_data()
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
