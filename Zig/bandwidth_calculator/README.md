# Bandwidth Calculator - Zig

A comprehensive Zig library for bandwidth calculations, data size conversions, and network transfer time estimations. Zero external dependencies.

## Features

- **Bandwidth Unit Conversion**: Convert between bps, Kbps, Mbps, Gbps, Tbps, Bps, KBps, MBps, GBps, TBps
- **Data Size Unit Conversion**: Convert between bits, Kbit, Mbit, Gbit, Tbit, Byte, KB, MB, GB, TB, PB, EB
- **Time Duration Conversion**: Convert between milliseconds, seconds, minutes, hours, days
- **Transfer Time Calculation**: Calculate download/upload time from data size and bandwidth
- **Required Bandwidth Calculation**: Calculate bandwidth needed for a given data size and time limit
- **Transfer Size Calculation**: Calculate data transferred in a given time at a given bandwidth
- **Human-Readable Formatting**: Auto-format bandwidth, data size, and duration to optimal units
- **String Parsing**: Parse data size and bandwidth strings like "100MB", "1.5Gbps"

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .bandwidth_calculator = .{
        .path = "path/to/bandwidth_calculator",
    },
},
```

Or copy the `src/` directory to your project.

## Usage

### Basic Bandwidth Conversion

```zig
const bandwidth = @import("bandwidth_calculator");

// Create a bandwidth value
const bw = bandwidth.Bandwidth.init(100.0, .Mbps);

// Convert to other units
const kbps = bw.to(.Kbps);  // 100,000 Kbps
const gbps = bw.to(.Gbps);  // 0.1 Gbps
const bps = bw.to(.bps);    // 100,000,000 bps
```

### Data Size Conversion

```zig
const size = bandwidth.DataSize.init(1.0, .GB);

const mb = size.to(.MB);   // 1,000 MB
const kb = size.to(.KB);   // 1,000,000 KB
const bits = size.toBits(); // 8,000,000,000 bits
```

### Calculate Transfer Time

```zig
// How long to download 4.7GB at 50Mbps?
const file_size = bandwidth.DataSize.init(4.7, .GB);
const connection = bandwidth.Bandwidth.init(50.0, .Mbps);
const time = bandwidth.calculateTransferTime(file_size, connection);

// Convert to minutes
const minutes = time.to(.minutes);
std.debug.print("Download time: {d:.1} minutes\n", .{minutes.value});
```

### Calculate Required Bandwidth

```zig
// What bandwidth do I need to upload 1GB in 2 minutes?
const size = bandwidth.DataSize.init(1.0, .GB);
const limit = bandwidth.Duration.init(2.0, .minutes);
const bw = bandwidth.calculateRequiredBandwidth(size, limit);

const mbps = bw.to(.Mbps);
std.debug.print("Required bandwidth: {d:.2} Mbps\n", .{mbps.value});
```

### Calculate Transfer Size

```zig
// How much data can I transfer in 1 hour at 10Mbps?
const bw = bandwidth.Bandwidth.init(10.0, .Mbps);
const duration = bandwidth.Duration.init(1.0, .hours);
const size = bandwidth.calculateTransferSize(bw, duration);

const gb = size.to(.GB);
std.debug.print("Transfer size: {d:.2} GB\n", .{gb.value});
```

### Human-Readable Formatting

```zig
const allocator = std.heap.page_allocator;

// Auto-format bandwidth
const bw = bandwidth.Bandwidth.init(1500000000.0, .bps);
const str = try bandwidth.formatBandwidth(bw, allocator);
defer allocator.free(str);
// Output: "1.50 Gbps"

// Auto-format data size
const size = bandwidth.DataSize.init(1536.0, .MB);
const str = try bandwidth.formatDataSize(size, allocator);
// Output: "1.54 GB"

// Auto-format duration
const dur = bandwidth.Duration.init(3665.0, .seconds);
const str = try bandwidth.formatDuration(dur, allocator);
// Output: "1.02 h"
```

### Parse Strings

```zig
// Parse data size
const size = try bandwidth.parseDataSize("4.7GB");
// size.value = 4.7, size.unit = .GB

// Parse bandwidth
const bw = try bandwidth.parseBandwidth("100Mbps");
// bw.value = 100.0, bw.unit = .Mbps
```

## API Reference

### Types

- `BandwidthUnit` - Enum for bandwidth units (bps, Kbps, Mbps, Gbps, Tbps, Bps, KBps, MBps, GBps, TBps)
- `DataUnit` - Enum for data units (bit, Kbit, Mbit, Gbit, Tbit, Byte, KB, MB, GB, TB, PB, EB)
- `TimeUnit` - Enum for time units (milliseconds, seconds, minutes, hours, days)
- `Bandwidth` - Bandwidth value with unit
- `DataSize` - Data size value with unit
- `Duration` - Time duration value with unit

### Functions

- `calculateTransferTime(data_size: DataSize, bandwidth: Bandwidth) Duration`
- `calculateRequiredBandwidth(data_size: DataSize, duration: Duration) Bandwidth`
- `calculateTransferSize(bandwidth: Bandwidth, duration: Duration) DataSize`
- `formatBandwidth(bandwidth: Bandwidth, allocator: Allocator) ![]u8`
- `formatDataSize(data_size: DataSize, allocator: Allocator) ![]u8`
- `formatDuration(duration: Duration, allocator: Allocator) ![]u8`
- `parseDataSize(input: []const u8) !DataSize`
- `parseBandwidth(input: []const u8) !Bandwidth`

### Methods

#### Bandwidth

- `init(value: f64, unit: BandwidthUnit) Bandwidth`
- `toBps() f64` - Convert to bits per second
- `to(target_unit: BandwidthUnit) Bandwidth`
- `format(allocator: Allocator, precision: usize) ![]u8`

#### DataSize

- `init(value: f64, unit: DataUnit) DataSize`
- `toBits() f64` - Convert to bits
- `toBytes() f64` - Convert to bytes
- `to(target_unit: DataUnit) DataSize`
- `format(allocator: Allocator, precision: usize) ![]u8`

#### Duration

- `init(value: f64, unit: TimeUnit) Duration`
- `toSeconds() f64` - Convert to seconds
- `to(target_unit: TimeUnit) Duration`
- `format(allocator: Allocator, precision: usize) ![]u8`

## Building

```bash
# Build the library
zig build

# Run tests
zig build test

# Run example
zig build example
```

## Example Output

```
=== Bandwidth Calculator 示例 ===

1. 带宽单位转换:
   原始: 100 Mbps
   转换为 Kbps: 100000.00 Kbps
   转换为 Gbps: 0.1000 Gbps
   转换为 bps: 100000000 bps

2. 数据大小单位转换:
   原始: 1 GB
   转换为 MB: 1000 MB
   转换为 KB: 1000000 KB
   转换为 bytes: 1000000000 bytes

3. 计算下载时间:
   文件大小: 4.7 GB
   网络速度: 50 Mbps
   下载时间: 12.53 min

4. 计算所需带宽:
   数据大小: 1 GB
   时间限制: 2 分钟
   所需带宽: 66.67 Mbps

5. 计算传输数据量:
   上传速度: 10 Mbps
   上传时长: 1 小时
   传输数据: 4.50 GB

6. 自动格式化显示:
   1500000 bps -> 1.50 Mbps
   1500000000 bps -> 1.50 Gbps
   1536 MB -> 1.54 GB
   3665 秒 -> 1.02 h

7. 解析字符串:
   解析 "4.7GB": 4.7 GB
   解析 "100Mbps": 100 Mbps

8. 实际应用场景:
   场景1 - 流媒体带宽需求:
     视频大小: 50 MB/分钟
     所需带宽: 6.67 Mbps
   场景2 - 云存储上传时间:
     备份大小: 100 GB
     上传速度: 20 Mbps
     预计时间: 11.1 小时
   场景3 - 网络升级决策:
     工作文件: 5 GB
     当前网络 (25 Mbps): 26.7 分钟
     升级网络 (100 Mbps): 6.7 分钟
     节省时间: 20.0 分钟

=== 示例完成 ===
```

## License

MIT License