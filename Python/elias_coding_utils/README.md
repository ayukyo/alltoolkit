# Elias 编码工具

Elias 编码是一系列用于编码正整数的通用编码方法，广泛应用于数据压缩、信息检索、搜索引擎索引等领域。

## 功能特性

- **Elias Gamma 编码**：适用于较小的整数，简单高效
- **Elias Delta 编码**：更高效的编码方式，适用于较大的整数
- **Elias Omega 编码**：可变长度递归编码，理论上可编码任意大的正整数
- **序列编码/解码**：支持整数列表的批量处理
- **字节格式输出**：支持输出为可传输的字节格式
- **流式编解码器**：提供 Encoder/Decoder 类用于流式处理
- **编码效率分析**：比较不同编码方式的效率，自动选择最优方案

## 安装使用

```python
# 直接导入使用（零外部依赖）
from mod import (
    elias_gamma_encode, elias_gamma_decode,
    elias_delta_encode, elias_delta_decode,
    elias_omega_encode, elias_omega_decode,
)
```

## 快速开始

### Elias Gamma 编码

```python
# 编码
encoded = elias_gamma_encode(5)  # 返回 "00101"
decoded = elias_gamma_decode("00101")  # 返回 5

# 序列编码
numbers = [1, 2, 3, 5, 8]
encoded = elias_gamma_encode_sequence(numbers)
decoded = elias_gamma_decode_sequence(encoded, len(numbers))
```

### Elias Delta 编码

```python
# 对于较大的整数，Delta 编码更高效
encoded = elias_delta_encode(1000)
decoded = elias_delta_decode(encoded)

# 序列编码
numbers = [1, 10, 100, 1000]
encoded = elias_delta_encode_sequence(numbers)
```

### Elias Omega 编码

```python
# Omega 编码使用递归方式
encoded = elias_omega_encode(16)  # 返回 "11101100000"
decoded = elias_omega_decode("11101100000")  # 返回 16
```

### 字节格式输出

```python
# 编码为字节，便于传输或存储
encoded_bytes = elias_gamma_encode(100, as_bytes=True)
decoded = elias_gamma_decode(encoded_bytes)
```

### 流式编解码器

```python
# 使用流式编码器
encoder = EliasEncoder(method='delta')
encoder.encode(1).encode(100).encode(1000)
result = encoder.get_result()

# 使用流式解码器
decoder = EliasDecoder(result, method='delta')
numbers = decoder.decode_all()
```

### 编码效率比较

```python
# 比较不同编码的长度
comparison = compare_encodings(1000)
print(comparison['recommendation'])  # 输出最优编码方式

# 自动选择最优编码
encoded, method = optimal_encode(1000)
```

## 编码规则说明

### Elias Gamma

编码规则：
1. 计算 N = floor(log2(n))
2. 写入 N 个前导零
3. 写入 n 的二进制表示（N+1 位）

例如：
- 1 → "1" (无前导零)
- 2 → "010" (1个前导零 + 二进制10)
- 4 → "00100" (2个前导零 + 二进制100)

### Elias Delta

编码规则：
1. 计算 N = floor(log2(n))
2. 使用 Gamma 编码 N+1
3. 写入 n 的低 N 位

例如：
- 1 → "1"
- 2 → "0100" (Gamma编码2=01 + 低1位=0)
- 4 → "01100" (Gamma编码3=011 + 低2位=00)

### Elias Omega

编码规则：
1. 从 n 开始，将其写成二进制
2. 在前面添加该二进制长度的二进制表示
3. 递归处理长度，直到长度为 1
4. 最后添加终止符 0

例如：
- 1 → "0" (仅终止符)
- 2 → "100" (二进制10 + 终止符0)
- 4 → "10100" (二进制100 + 二进制10 + 终止符0)

## 应用场景

- **搜索引擎**：倒排索引中文档 ID 的压缩存储
- **数据压缩**：整数序列的高效编码
- **网络传输**：减少数据传输量
- **数据库索引**：索引数据的压缩存储
- **信息检索**：位置列表的压缩编码

## 测试

运行测试：
```bash
python elias_coding_utils_test.py
```

运行示例：
```bash
cd examples
python usage_examples.py
```

## 参考资料

- Elias, P. (1975). "Universal codeword sets and representations of the integers"
- 信息论与编码理论教材