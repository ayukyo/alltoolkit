# Bandwidth Utils - 带宽计算工具

> 零外部依赖，纯 Python 标准库实现

提供带宽单位换算、下载时间估算、数据传输速率计算等功能。

## 安装

```python
from bandwidth_utils.mod import (
    calculate_transfer_time,
    format_bandwidth,
    format_size,
    parse_bandwidth,
    parse_size,
)
```

## 核心功能

### 1. 计算下载/上传时间

```python
from bandwidth_utils.mod import calculate_transfer_time, download_time

# 完整结果
result = calculate_transfer_time("1 GB", "100 Mbps")
print(f"下载时间: {result.time_formatted}")  # 下载时间: 1m 25.9s
print(f"平均速度: {result.average_speed_formatted}")  # 平均速度: 100.00 Mbps

# 快捷函数
print(download_time("1 GB", "100 Mbps"))  # 1m 25.9s
```

### 2. 计算所需带宽

```python
from bandwidth_utils.mod import calculate_required_bandwidth, needed_bandwidth

# 在指定时间内完成传输需要多少带宽？
info = calculate_required_bandwidth("4.7 GB", "1h")  # DVD 一小时内传完
print(f"所需带宽: {info.format_auto()}")  # 所需带宽: 10.45 Mbps

# 快捷函数
print(needed_bandwidth("1 GB", "10m"))  # 13.33 Mbps
```

### 3. 单位换算

```python
from bandwidth_utils.mod import parse_size, parse_bandwidth, format_size, format_bandwidth

# 解析文件大小
print(parse_size("1 GB"))      # 1073741824 (字节)
print(parse_size("100 MB"))    # 104857600
print(parse_size("500 KB"))    # 512000

# 解析带宽
print(parse_bandwidth("100 Mbps"))  # 100000000.0 (bps)
print(parse_bandwidth("10 MB/s"))   # 80000000.0 (bps)

# 格式化文件大小
print(format_size(1073741824))  # 1.00 GB
print(format_size(1536000000))  # 1.43 GB

# 格式化带宽
print(format_bandwidth(100000000))        # 100.00 Mbps
print(format_bandwidth(100000000, 'MB/s')) # 12.50 MB/s
```

### 4. 时间解析与格式化

```python
from bandwidth_utils.mod import parse_time, format_time

# 解析时间字符串
print(parse_time("1h30m"))   # 5400.0 (秒)
print(parse_time("2 小时"))   # 7200.0
print(parse_time("30m"))      # 1800.0

# 格式化秒数
print(format_time(3661))   # 1h 1m 1s
print(format_time(90))     # 1m 30s
print(format_time(0.5))    # 500ms
```

### 5. 流媒体带宽建议

```python
from bandwidth_utils.mod import bandwidth_for_streaming

# 1080p 60fps 直播需要多少带宽？
info = bandwidth_for_streaming('1080p', 60, 'h265')
print(f"建议带宽: {info['recommended']}")  # 建议带宽: 9.60 Mbps

# 4K 60fps AV1 编码
info = bandwidth_for_streaming('4k', 60, 'av1')
print(f"建议带宽: {info['recommended']}")  # 建议带宽: 16.80 Mbps
```

### 6. 带宽比较

```python
from bandwidth_utils.mod import compare_bandwidths

result = compare_bandwidths("100 Mbps", "50 Mbps", "1 Gbps")
print(f"最快: {result['fastest']}")  # 最快: 1 Gbps
print(f"最慢: {result['slowest']}")  # 最慢: 50 Mbps
print(f"倍数: {result['ratio_fastest_to_slowest']}x")  # 倍数: 20.0x
```

## 支持的单位

### 文件大小
- `B`, `KB`, `MB`, `GB`, `TB`, `PB`, `EB`
- `KiB`, `MiB`, `GiB` 等（二进制单位）
- 支持中英混合、有无空格

### 带宽
- `bps`, `Kbps`, `Mbps`, `Gbps`, `Tbps`（比特每秒）
- `B/s`, `KB/s`, `MB/s`, `GB/s`（字节每秒）

### 时间
- `s`, `sec`, `second`（秒）
- `m`, `min`, `minute`（分钟）
- `h`, `hr`, `hour`（小时）
- `d`, `day`（天）
- 支持组合如 `1h30m`

## API 参考

### 主要函数

| 函数 | 说明 |
|------|------|
| `calculate_transfer_time(size, bandwidth, overhead)` | 计算传输时间 |
| `calculate_required_bandwidth(size, time)` | 计算所需带宽 |
| `parse_size(str)` | 解析文件大小字符串 |
| `parse_bandwidth(str)` | 解析带宽字符串 |
| `parse_time(str)` | 解析时间字符串 |
| `format_size(bytes)` | 格式化文件大小 |
| `format_bandwidth(bps, unit)` | 格式化带宽 |
| `format_time(seconds)` | 格式化时间 |
| `bandwidth_for_streaming(resolution, fps, codec)` | 流媒体带宽建议 |
| `compare_bandwidths(*bandwidths)` | 比较多个带宽 |

### 快捷函数

| 函数 | 说明 |
|------|------|
| `download_time(size, bandwidth)` | 快速计算下载时间 |
| `upload_time(size, bandwidth)` | 快速计算上传时间 |
| `needed_bandwidth(size, time)` | 快速计算所需带宽 |

## 示例场景

### 场景1: 评估下载时间
```python
# 下载一个 50GB 的游戏需要多久？
result = calculate_transfer_time("50 GB", "100 Mbps", overhead_percent=10)
print(f"预计下载时间: {result.time_formatted}")  # 约 1h 14m
```

### 场景2: 规划服务器带宽
```python
# 一天传输 1TB 数据需要多少带宽？
info = calculate_required_bandwidth("1 TB", "24h")
print(f"需要至少 {info.format_auto()} 带宽")  # 约 93 Mbps
```

### 场景3: 流媒体直播设置
```python
# 1080p 30fps H.264 直播
info = bandwidth_for_streaming('1080p', 30, 'h264')
print(f"上传带宽建议: {info['recommended']}")  # 建议 9.60 Mbps
```

## 测试

```bash
python test.py
```

## 许可证

MIT License