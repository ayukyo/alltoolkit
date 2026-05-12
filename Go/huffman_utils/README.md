# huffman_utils

完整的 Huffman 编码/解码工具库，零外部依赖，仅使用 Go 标准库。

## 功能特性

### 核心功能
- **BuildTree** - 从频率数据构建 Huffman 树
- **BuildTreeFromData** - 从原始数据构建 Huffman 树
- **Encode** - Huffman 编码，返回完整编码结果
- **EncodeString** - 字符串编码
- **EncodeWithTree** - 使用现有树编码
- **Decode** - Huffman 解码
- **DecodeString** - 解码为字符串
- **DecodeWithTable** - 使用码表解码

### 频率分析
- **CountFrequencies** - 统计字节频率
- **CountFrequenciesFromString** - 统计字符串频率
- **CountRuneFrequencies** - 统计 UTF-8 字符频率
- **GetTopFrequencies** - 获取最高频率字符

### 规范 Huffman 编码
- **BuildCanonicalCodes** - 构建规范 Huffman 码
- **BuildCanonicalTree** - 从码长构建规范树
- **GetCodeLengths** - 获取各字符码长

### 效率分析
- **CalculateEntropy** - 计算香农熵
- **CalculateExpectedCodeLength** - 计算期望码长
- **CalculateEfficiency** - 计算编码效率
- **GetAverageCodeLength** - 获取平均码长
- **GetMaxCodeLength** - 获取最大码长
- **GetMinCodeLength** - 获取最小码长
- **GetCodeTableStats** - 获取码表统计信息

### 流式处理
- **HuffmanEncoder** - 流式编码器
- **HuffmanDecoder** - 流式解码器
- **BitWriter** - 位写入器
- **BitReader** - 位读取器

### 序列化
- **SerializeTree** - 序列化 Huffman 树
- **DeserializeTree** - 反序列化 Huffman 树
- **SerializeEncodedData** - 序列化编码数据（含树）
- **DeserializeEncodedData** - 反序列化编码数据

### 文件操作
- **EncodeFile** - 编码文件
- **DecodeFile** - 解码文件
- **WriteEncodedFile** - 写入编码文件
- **ReadEncodedFile** - 读取编码文件

### 自适应 Huffman 编码
- **AdaptiveHuffmanEncoder** - FGK 算法自适应编码器

### 工具函数
- **QuickEncode** - 快速编码
- **QuickDecode** - 快速解码
- **GetCompressionStats** - 获取压缩统计
- **MergeFrequencyTables** - 合并频率表
- **CompareHuffmanCodes** - 比较两个码表
- **PrintTree** - 打印树结构
- **ValidateTree** - 验证树结构

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/huffman_utils
```

## 使用示例

### 基本编码和解码

```go
package main

import (
    "fmt"
    huffman "github.com/ayukyo/alltoolkit/Go/huffman_utils"
)

func main() {
    // 原始数据
    data := []byte("hello world")
    
    // 编码
    result := huffman.Encode(data)
    
    fmt.Printf("原始大小: %d 字节\n", result.OriginalSize)
    fmt.Printf("编码大小: %d 字节 (%d 位)\n", result.EncodedSize, result.BitLength)
    fmt.Printf("压缩比: %.2fx\n", result.CompressionRatio)
    
    // 解码
    tree := huffman.BuildTreeFromData(data)
    decoded := huffman.Decode(result.EncodedData, tree, result.BitLength)
    
    fmt.Printf("解码结果: %s\n", decoded.Data)
    fmt.Printf("解码成功: %v\n", decoded.Success)
}
```

### 频率分析

```go
// 统计字符频率
freq := huffman.CountFrequenciesFromString("the quick brown fox")

// 获取最高频率的字符
top := huffman.GetTopFrequencies(freq, 5)
for _, item := range top {
    fmt.Printf("'%c': %d 次\n", item.Char, item.Count)
}

// 计算熵
entropy := huffman.CalculateEntropy(freq, len("the quick brown fox"))
fmt.Printf("香农熵: %.4f 位/字符\n", entropy)
```

### 流式编码

```go
// 从训练数据构建频率表
trainData := "the quick brown fox jumps over the lazy dog"
freq := huffman.CountFrequenciesFromString(trainData)

// 创建流式编码器
encoder := huffman.NewEncoder(freq)

// 分块编码
encoder.WriteBytes([]byte("hello "))
encoder.WriteBytes([]byte("world "))

result := encoder.GetResult()

// 解码
tree := encoder.GetTree()
decoder := huffman.NewDecoder(tree, result.EncodedData)
decoded, _ := decoder.ReadAll()
```

### 文件操作

```go
// 编码文件
result, err := huffman.EncodeFile("input.txt", "output.bin")
if err != nil {
    panic(err)
}

fmt.Printf("压缩比: %.2fx\n", result.CompressionRatio)

// 解码文件
decoded, err := huffman.DecodeFile("output.bin", "decoded.txt")
if err != nil {
    panic(err)
}

fmt.Printf("解码成功: %v\n", decoded.Success)
```

### 规范 Huffman 编码

```go
// 定义码长
codeLengths := map[byte]int{
    'A': 2,
    'B': 2,
    'C': 3,
    'D': 3,
}

// 构建规范码
codes := huffman.BuildCanonicalCodes(codeLengths)
for char, code := range codes {
    fmt.Printf("'%c': %s\n", char, code)
}

// 从码长构建树
tree := huffman.BuildCanonicalTree(codeLengths)
```

### 效率分析

```go
data := []byte("example text for analysis")
freq := huffman.CountFrequencies(data)
tree := huffman.BuildTreeFromData(data)

// 计算熵
entropy := huffman.CalculateEntropy(freq, len(data))

// 计算期望码长
expectedLen := huffman.CalculateExpectedCodeLength(tree, freq)

// 计算效率
efficiency := huffman.CalculateEfficiency(tree, freq)

fmt.Printf("熵: %.4f 位/字符\n", entropy)
fmt.Printf("期望码长: %.4f\n", expectedLen)
fmt.Printf("效率: %.2f%%\n", efficiency*100)
```

### 序列化

```go
// 编码并序列化
data := []byte("hello world")
result := huffman.Encode(data)
serialized := huffman.SerializeEncodedData(result)

// 反序列化并解码
deserialized, err := huffman.DeserializeEncodedData(serialized)
if err != nil {
    panic(err)
}

tree := &huffman.HuffmanTree{
    CodeTable: deserialized.CodeTable,
    CharTable: make(map[string]byte),
}
for char, code := range deserialized.CodeTable {
    tree.CharTable[code] = char
}

decoded := huffman.Decode(deserialized.EncodedData, tree, deserialized.BitLength)
```

### 位操作

```go
// 位写入器
bw := huffman.NewBitWriter()
bw.WriteBit(1)
bw.WriteBit(0)
bw.WriteBits("1011")
data := bw.Bytes()
bitCount := bw.BitCount()

// 位读取器
br := huffman.NewBitReader(data)
bit, _ := br.ReadBit()
bits, _ := br.ReadBits(4)
```

## 压缩性能

对于典型的英文文本，Huffman 编码通常能达到：
- 压缩比：1.5x - 2.5x
- 空间节省：30% - 60%

对于高度倾斜的分布：
- 压缩比：可达 5x 以上
- 空间节省：可达 80% 以上

## 算法说明

### Huffman 编码
- 时间复杂度：O(n log n) 构建树
- 编码/解码：O(n)
- 空间复杂度：O(k)，k 为不同字符数

### 自适应 Huffman 编码 (FGK)
- 动态更新树结构
- 无需预先知道频率分布
- 适用于流式数据

## 测试

```bash
go test -v
```

## 许可证

MIT License