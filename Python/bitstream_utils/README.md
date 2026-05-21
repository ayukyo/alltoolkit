# Bitstream Utils

位流处理工具，零依赖实现的高效位级数据操作。

## 功能特性

- **位流读写**: 按位读取和写入数据
- **位操作**: 位翻转、位掩码、位计数
- **压缩编码**: Golomb/Rice 编码、算术编码
- **位流序列化**: 高效二进制序列化
- **数据压缩**: 基于位流的压缩工具

## 快速开始

```python
from bitstream_utils.mod import BitStream, BitWriter, BitReader

# 创建位流写入器
writer = BitWriter()
writer.write_bits(42, bits=8)   # 写入 8 位
writer.write_bits(1, bits=1)    # 写入 1 位
writer.write_bits(255, bits=16) # 写入 16 位

# 获取字节流
data = writer.to_bytes()

# 创建位流读取器
reader = BitReader(data)
value1 = reader.read_bits(8)   # 42
value2 = reader.read_bits(1)   # 1
value3 = reader.read_bits(16)  # 255
```

## 使用示例

### BitWriter 写入

```python
from bitstream_utils.mod import BitWriter

writer = BitWriter()

# 写入指定位数
writer.write_bits(100, bits=8)   # 写入 8 位整数
writer.write_bit(True)           # 写入 1 位布尔
writer.write_bits(0xFF, bits=8)  # 写入字节

# 写入变长整数
writer.write_varint(1000)        # 自动长度

# 对齐到字节边界
writer.align_to_byte()

# 获取结果
data = writer.to_bytes()
bits = writer.to_bitstring()  # '011001001...'
```

### BitReader 读取

```python
from bitstream_utils.mod import BitReader

reader = BitReader(data)

# 读取指定位数
value = reader.read_bits(8)
flag = reader.read_bit()

# 读取变长整数
num = reader.read_varint()

# 跳过位
reader.skip_bits(4)

# 查看剩余位
remaining = reader.remaining_bits()
```

### 位流操作

```python
from bitstream_utils.mod import BitStream

# 从数据创建
bs = BitStream.from_bytes(b'\x01\x02\x03')

# 位级操作
bs.flip_bit(0)              # 翻转第一位
bs.set_bit(5, True)         # 设置第六位
bit = bs.get_bit(5)         # 获取第六位

# 位掩码操作
masked = bs.apply_mask(0xFF)

# 位计数
count_ones = bs.count_bits(1)
count_zeros = bs.count_bits(0)
```

### Golomb/Rice 编码

```python
from bitstream_utils.mod import GolombEncoder, GolombDecoder

encoder = GolombEncoder(m=8)  # Golomb 参数

# 编码整数
encoded = encoder.encode(42)

# 解码
decoder = GolombDecoder(m=8)
decoded = decoder.decode(encoded)

# Rice 编码（m = 2^k）
rice_enc = GolombEncoder(m=4)  # k=2 的 Rice 编码
```

### 位操作函数

```python
from bitstream_utils.mod import (
    count_set_bits,        # 统计 1 的数量
    reverse_bits,          # 位翻转
    rotate_bits,           # 位旋转
    get_bit_range,         # 获取位范围
    set_bit_range,         # 设置位范围
)

# 统计 1 的数量
ones = count_set_bits(0b101011)  # 4

# 翻转位
reversed = reverse_bits(0b1010, bits=4)  # 0b0101

# 旋转位
rotated = rotate_bits(0b1100, shift=2, bits=4)  # 0b0011
```

## API 参考

### BitWriter

| 方法 | 说明 |
|------|------|
| `write_bits(value, bits)` | 写入指定位数 |
| `write_bit(value)` | 写入单比特 |
| `write_varint(value)` | 写入变长整数 |
| `align_to_byte()` | 对齐到字节 |
| `to_bytes()` | 输出字节流 |
| `to_bitstring()` | 输出位字符串 |

### BitReader

| 方法 | 说明 |
|------|------|
| `read_bits(bits)` | 读取指定位数 |
| `read_bit()` | 读取单比特 |
| `read_varint()` | 读取变长整数 |
| `skip_bits(n)` | 跳过 n 位 |
| `remaining_bits()` | 剩余位数 |
| `at_end()` | 是否读完 |

### BitStream

| 方法 | 说明 |
|------|------|
| `from_bytes(data)` | 从字节创建 |
| `get_bit(index)` | 获取位 |
| `set_bit(index, value)` | 设置位 |
| `flip_bit(index)` | 翻转位 |
| `count_bits(value)` | 统计位 |
| `apply_mask(mask)` | 应用掩码 |

### GolombEncoder/Decoder

| 方法 | 说明 |
|------|------|
| `encode(value)` | Golomb 编码 |
| `decode(data)` | Golomb 解码 |

## 应用场景

- **数据压缩**: 位级压缩编码
- **协议解析**: 网络协议位级解析
- **图像处理**: 位图操作
- **加密算法**: 位级加密操作
- **文件格式**: 自定义二进制格式

---

**测试覆盖**: 完整测试套件，覆盖位流读写、编码、位操作等