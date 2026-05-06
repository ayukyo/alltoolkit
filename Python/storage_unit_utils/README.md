# Storage Unit Utils - 存储单位转换与格式化工具库

一个完整的存储单位转换和格式化工具库，支持十进制（SI）和二进制（IEC）单位，零外部依赖。

## 功能特性

### 🔄 单位转换
- 十进制单位：bits, Bytes, KB, MB, GB, TB, PB, EB, ZB, YB
- 二进制单位：KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB
- 比特与字节转换
- 任意单位间转换

### 📝 格式化输出
- 智能格式化：自动选择最合适的单位
- 人类可读格式：短格式和长格式
- 传输速度格式化：KB/s, MB/s
- 带宽格式化：bps, Kbps, Mbps, Gbps

### 🔢 解析输入
- 解析存储大小字符串："1.5GB", "1024 KiB"
- 大小写不敏感
- 支持逗号分隔的数字

### 📊 进度可视化
- 进度条生成
- 百分比计算
- 时间估算

### 🧮 计算功能
- 存储大小比较
- 加法运算
- 减法运算
- 查找最大/最小值

## 快速开始

### 基本转换

```python
from storage_unit_utils import convert, to_bytes, from_bytes

# 十进制转换（SI 单位）
convert(1, "KB", "B")  # 1000.0
convert(1024, "MB", "GB")  # 1.024

# 二进制转换（IEC 单位）
convert(1, "KiB", "B")  # 1024.0
convert(1024, "MiB", "GiB")  # 1.0

# 比特转换
convert(8, "bit", "B")  # 1.0

# 转换为字节
to_bytes(1, "GB")  # 1000000000
to_bytes(1, "GiB")  # 1073741824
```

### 格式化输出

```python
from storage_unit_utils import format_size, smart_format

# 十进制格式化
format_size(1500000000)  # "1.50 GB"

# 二进制格式化
format_size(1073741824, binary=True)  # "1.00 GiB"

# 智能格式化
smart_format(500)  # "500 B"
smart_format(1536)  # "1.54 KB"
```

### 解析输入

```python
from storage_unit_utils import parse_size, parse_to_bytes

# 解析大小
parse_size("1.5GB")  # (1.5, StorageUnit.GIGABYTE)
parse_size("1024 KiB")  # (1024.0, StorageUnit.KIBIBYTE)

# 直接转换为字节
parse_to_bytes("1GB")  # 1000000000
parse_to_bytes("1GiB")  # 1073741824
```

### 进度条

```python
from storage_unit_utils import progress_bar, percentage

# 进度条
progress_bar(500, 1000, width=20)
# "██████████░░░░░░░░░░ 50.0% (500.00 KB/1000.00 KB)"

# 百分比
percentage(500, 1000)  # "50.0%"
```

### 比较和计算

```python
from storage_unit_utils import compare, add, subtract

# 比较
compare("1GB", "500MB")  # 1 (大于)
compare("1024MB", "1GB")  # 0 (相等)

# 加法
add("1GB", "500MB")  # 1500000000 (bytes)
add("1GB", "500MB", unit="MB")  # 1500.0

# 减法
subtract("2GB", "500MB")  # 1500000000
subtract("2GB", "500MB", unit="MB")  # 1500.0
```

### 传输速度

```python
from storage_unit_utils import speed_format, bandwidth_format, estimate_time

# 速度格式化
speed_format(1024 * 1024)  # "1.00 MB/s"

# 带宽格式化
bandwidth_format(100000000)  # "100.00 Mbps"

# 时间估算
estimate_time(1024 * 1024 * 100, 1024 * 1024)  # "1m 40s"
```

### 便捷函数

```python
from storage_unit_utils import kb, mb, gb, tb, kib, mib, gib, tib

# 十进制单位转字节
kb(1)  # 1000
mb(1)  # 1000000
gb(1)  # 1000000000
tb(1)  # 1000000000000

# 二进制单位转字节
kib(1)  # 1024
mib(1)  # 1048576
gib(1)  # 1073741824
tib(1)  # 1099511627776
```

## API 参考

### 转换函数

| 函数 | 描述 |
|------|------|
| `convert(value, from_unit, to_unit)` | 在任意单位间转换 |
| `to_bytes(value, unit)` | 转换为字节数 |
| `from_bytes(bytes_value, unit)` | 从字节转换为指定单位 |

### 格式化函数

| 函数 | 描述 |
|------|------|
| `format_size(bytes, binary=False, precision=2)` | 格式化存储大小 |
| `format_bits(bits, precision=2)` | 格式化比特数 |
| `smart_format(bytes, precision=2)` | 智能格式化 |
| `human_readable(bytes, style="short", binary=False)` | 人类可读格式 |
| `speed_format(bytes_per_second)` | 格式化传输速度 |
| `bandwidth_format(bits_per_second)` | 格式化带宽 |

### 解析函数

| 函数 | 描述 |
|------|------|
| `parse_size(size_str)` | 解析大小字符串为 (值, 单位) |
| `parse_to_bytes(size_str)` | 解析大小字符串为字节数 |

### 计算函数

| 函数 | 描述 |
|------|------|
| `compare(size1, size2)` | 比较两个大小 (-1, 0, 1) |
| `add(*sizes, unit=None)` | 多个大小相加 |
| `subtract(size1, size2, unit=None)` | 两个大小相减 |
| `ratio(part, total)` | 计算比例 |
| `percentage(part, total)` | 计算百分比字符串 |
| `total_size(*sizes, unit=None)` | 计算总大小并格式化 |

### 进度函数

| 函数 | 描述 |
|------|------|
| `progress_bar(used, total, width=20)` | 生成进度条 |
| `estimate_time(remaining, speed)` | 估算剩余时间 |

### 查找函数

| 函数 | 描述 |
|------|------|
| `find_largest_unit(sizes)` | 找最大的大小 |
| `find_smallest_unit(sizes)` | 找最小的尺寸 |

## 单位对照表

### 十进制单位（SI）

| 单位 | 名称 | 基数 |
|------|------|------|
| bit | 比特 | - |
| B | 字节 | - |
| KB | 千字节 | 1000 |
| MB | 兆字节 | 1000² |
| GB | 吉字节 | 1000³ |
| TB | 太字节 | 1000⁴ |
| PB | 拍字节 | 1000⁵ |
| EB | 艾字节 | 1000⁶ |
| ZB | 泽字节 | 1000⁷ |
| YB | 尧字节 | 1000⁸ |

### 二进制单位（IEC）

| 单位 | 名称 | 基数 |
|------|------|------|
| KiB | 千字节 | 1024 |
| MiB | 兆字节 | 1024² |
| GiB | 吉字节 | 1024³ |
| TiB | 太字节 | 1024⁴ |
| PiB | 拍字节 | 1024⁵ |
| EiB | 艾字节 | 1024⁶ |
| ZiB | 泽字节 | 1024⁷ |
| YiB | 尧字节 | 1024⁸ |

## 真实场景示例

### 磁盘空间分析

```python
from storage_unit_utils import *

total_space = tb(1)
used_space = gb(650)

print(f"总容量: {format_size(total_space)}")
print(f"已使用: {format_size(used_space)}")
print(f"使用率: {percentage(used_space, total_space)}")
print(progress_bar(used_space, total_space, width=30))
```

### 文件大小计算

```python
from storage_unit_utils import *

# 计算文件总大小
files = ["5MB", "1.5GB", "500KB"]
total = total_size(*files)
print(f"文件总计: {total}")
```

### 下载进度

```python
from storage_unit_utils import *

file_size = gb(10)
downloaded = gb(3.5)
speed = mb(5)

print(progress_bar(downloaded, file_size, binary=True))
print(f"剩余时间: {estimate_time(file_size - downloaded, speed)}")
```

## 运行测试

```bash
python -m pytest storage_unit_utils/test.py -v
```

## 运行示例

```bash
python storage_unit_utils/examples.py
```

## 许可证

MIT License