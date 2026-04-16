# checksum_utils

零依赖校验和计算工具库，提供多种校验和算法实现。

## 功能特性

- **CRC 算法**
  - CRC32 (IEEE 802.3)
  - CRC64 (ISO 3309)
- **Adler32** - 快速校验和算法
- **Fletcher 算法**
  - Fletcher-16
  - Fletcher-32
  - Fletcher-64
- **Internet Checksum** - IP/TCP/UDP 校验和 (RFC 1071)
- **简单校验和**
  - Sum8 / Sum16 / Sum32
  - XOR8
  - LRC (Longitudinal Redundancy Check)

## 特点

- 零外部依赖
- 支持字节、字符串、文件
- 支持增量计算
- 纯 Python 实现
- 完整的单元测试

## 安装

```python
# 直接复制 mod.py 到项目中使用
from checksum_utils.mod import ChecksumCalculator, crc32, crc64
```

## 快速开始

```python
from checksum_utils.mod import ChecksumCalculator, crc32, adler32

# 基本用法
data = "Hello, World!"

# 使用便捷函数
crc = crc32(data)
print(f"CRC32: {ChecksumCalculator.to_hex(crc, 8)}")

# 使用统一接口
result = ChecksumCalculator.calculate_all(data)
print(result)

# 计算文件校验和
file_crc = ChecksumCalculator.file_crc32("/path/to/file")
```

## API 参考

### 便捷函数

```python
# CRC 校验和
crc32(data) -> int      # CRC32
crc64(data) -> int      # CRC64

# Adler32
adler32(data) -> int

# Fletcher 校验和
fletcher16(data) -> int
fletcher32(data) -> int
fletcher64(data) -> int

# Internet 校验和
internet_checksum(data) -> int
```

### 类方法

```python
# CRC32
CRC32.calculate(data, crc=0) -> int
CRC32.calculate_file(filepath, chunk_size=8192) -> int

# CRC64
CRC64.calculate(data, crc=0) -> int
CRC64.calculate_file(filepath, chunk_size=8192) -> int

# Adler32
Adler32.calculate(data, adler=1) -> int
Adler32.calculate_file(filepath, chunk_size=8192) -> int

# Fletcher
Fletcher.fletcher16(data) -> int
Fletcher.fletcher32(data) -> int
Fletcher.fletcher64(data) -> int

# Internet Checksum
InternetChecksum.calculate(data) -> int
InternetChecksum.verify(data, checksum) -> bool

# 简单校验和
SimpleChecksum.sum8(data) -> int
SimpleChecksum.sum16(data) -> int
SimpleChecksum.sum32(data) -> int
SimpleChecksum.xor8(data) -> int
SimpleChecksum.lrc(data) -> int
```

### ChecksumCalculator 统一接口

```python
# 计算所有校验和
ChecksumCalculator.calculate_all(data) -> dict

# 文件校验和
ChecksumCalculator.file_crc32(filepath) -> int
ChecksumCalculator.file_crc64(filepath) -> int
ChecksumCalculator.file_adler32(filepath) -> int

# 十六进制转换
ChecksumCalculator.to_hex(value, width=8) -> str
```

## 使用示例

### 数据完整性验证

```python
from checksum_utils.mod import crc32

data = "重要数据"
checksum = crc32(data)

# 传输后验证
received_checksum = crc32(data)
if checksum == received_checksum:
    print("数据完整!")
```

### 文件校验

```python
from checksum_utils.mod import CRC32, CRC64

# 计算文件 CRC32
file_crc = CRC32.calculate_file("/path/to/file")
print(f"CRC32: {file_crc:08X}")

# 增量计算大文件
crc = 0
with open("/path/to/large/file", 'rb') as f:
    while chunk := f.read(8192):
        crc = CRC32.calculate(chunk, crc)
```

### 网络协议校验

```python
from checksum_utils.mod import InternetChecksum

# 计算 IP 头部校验和
ip_header = bytes([0x45, 0x00, 0x00, 0x3C, ...])
checksum = InternetChecksum.calculate(ip_header)

# 验证校验和
is_valid = InternetChecksum.verify(ip_header, checksum)
```

## 算法特点

| 算法 | 位宽 | 速度 | 错误检测能力 | 典型应用 |
|------|------|------|-------------|----------|
| CRC32 | 32位 | 中等 | 高 | ZIP, PNG, Ethernet |
| CRC64 | 64位 | 中等 | 非常高 | ISO 3309, 数据存储 |
| Adler32 | 32位 | 快 | 中等 | zlib, PNG |
| Fletcher-16 | 16位 | 快 | 中等 | 通信协议 |
| Internet | 16位 | 快 | 低 | IP, TCP, UDP |
| XOR8 | 8位 | 非常快 | 低 | 简单校验 |
| LRC | 8位 | 快 | 低 | Modbus RTU |

## 许可证

MIT License