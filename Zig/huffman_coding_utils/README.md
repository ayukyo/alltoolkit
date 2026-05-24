# Huffman Coding Utils

霍夫曼编码工具模块 - 实现经典的无损数据压缩算法，零外部依赖。

## 功能特性

- **霍夫曼编码器** - 基于字符频率构建最优编码树
- **霍夫曼解码器** - 从编码表重建原始数据
- **频率统计** - 计算字符出现频率
- **压缩率分析** - 实时计算压缩效果
- **二进制支持** - 支持任意字节数据编码

## 快速开始

```zig
const std = @import("std");
const huffman = @import("mod.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // 创建编码器
    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    // 构建编码
    const text = "hello world";
    try encoder.build(text);

    // 编码数据
    const encoded = try encoder.encode(text);
    defer allocator.free(encoded);

    // 打印编码表
    huffman.printCodeTable(encoder.getCodeTable());
}
```

## 核心类型

### HuffmanEncoder

```zig
var encoder = HuffmanEncoder.init(allocator);
defer encoder.deinit();

// 从数据构建编码树
try encoder.build(data);

// 编码数据为二进制
const encoded = try encoder.encode(data);

// 获取字符编码
if (encoder.getCode('a')) |code| {
    std.debug.print("'a' -> {s}\n", .{code});
}
```

### HuffmanDecoder

```zig
var decoder = HuffmanDecoder.init(allocator);
defer decoder.deinit();

// 从编码表构建解码树
try decoder.buildFromCodes(encoder.getCodeTable(), allocator);

// 解码数据
const decoded = try decoder.decode(encoded, bit_length, allocator);
defer allocator.free(decoded);
```

### 辅助函数

```zig
// 计算字符频率
var freq = try huffman.calculateFrequency(allocator, data);
defer freq.deinit();

// 打印频率表
huffman.printFrequencyMap(&freq);

// 打印编码表
huffman.printCodeTable(codes);

// 计算压缩率
const ratio = huffman.calculateCompressionRatio(original_len, encoded_bits);
```

## 使用场景

### 文本压缩

```zig
const text = "the quick brown fox jumps over the lazy dog";
try encoder.build(text);
const compressed = try encoder.encode(text);
// 典型压缩率: 40-60%
```

### 二进制数据

```zig
const binary_data = [_]u8{ 0x00, 0x01, 0x00, 0x01, 0x02 };
try encoder.build(&binary_data);
const encoded = try encoder.encode(&binary_data);
```

### 重复数据

```zig
const repetitive = "aaaaaaaab";
try encoder.build(repetitive);
const encoded = try encoder.encode(repetitive);
// 高频字符获得更短编码，压缩率更高
```

## 算法原理

霍夫曼编码是一种基于字符频率的最优前缀编码：

1. **频率统计** - 统计每个字符出现频率
2. **构建优先队列** - 按频率排序
3. **构建霍夫曼树** - 合并最低频率节点
4. **生成编码表** - 左分支为0，右分支为1
5. **编码/解码** - 按编码表转换

## 性能特点

| 特性 | 说明 |
|------|------|
| 空间复杂度 | O(n) - n为不同字符数 |
| 构建时间 | O(n log n) |
| 编码时间 | O(m) - m为数据长度 |
| 解码时间 | O(m) |
| 压缩率 | 依赖数据特征 |

## 测试

```bash
cd Zig/huffman_coding_utils
zig test huffman_coding_utils_test.zig
```

## 示例运行

```bash
cd Zig/huffman_coding_utils
zig run examples/example.zig
```

## 许可证

MIT License