# Rle Utils


RLE (Run-Length Encoding) Utilities - 游程编码工具

提供完整的游程编码实现，包括：
- 基本游程编码/解码
- 可配置的最小运行长度
- 支持字符串和字节序列
- 多种编码格式输出
- 高效的流式处理

零外部依赖，纯 Python 实现。


## 功能

### 类

- **RLERun**: 表示一个游程（连续相同元素的序列）
- **RLEEncoder**: 游程编码器

将连续重复的元素压缩为 (值, 计数) 对。
支持字符串、字节序列和任意可迭代对象。
  方法: encode_string, encode_bytes, encode_iterable, encode_to_tuples, encode_compact ... (6 个方法)
- **RLEDecoder**: 游程解码器

将游程编码数据解码还原。
  方法: decode_string, decode_bytes, decode_tuples, decode_compact, decode_bytes_packed
- **RLE**: 游程编码高级接口

提供简化的静态方法进行编码和解码。
  方法: encode, decode, encode_compact, decode_compact, encode_bytes ... (8 个方法)
- **StreamingRLEEncoder**: 流式游程编码器

支持分块处理大型数据，适用于流式场景。
  方法: feed, flush, reset

### 函数

- **rle_encode(data, min_run_length**) - 便捷编码函数
- **rle_decode(tuples, as_bytes**) - 便捷解码函数
- **rle_compress(data**) - 便捷紧凑编码函数
- **rle_decompress(data**) - 便捷紧凑解码函数
- **encode_string(self, data**) - 编码字符串
- **encode_bytes(self, data**) - 编码字节序列
- **encode_iterable(self, data**) - 编码任意可迭代对象
- **encode_to_tuples(self, data**) - 编码为元组列表格式
- **encode_compact(self, data**) - 编码为紧凑字符串格式
- **encode_bytes_packed(self, data**) - 编码字节序列为打包格式

... 共 26 个函数

## 使用示例

```python
from mod import rle_encode

# 使用 rle_encode
result = rle_encode()
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
