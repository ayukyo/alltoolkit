# Human Readable Utils

零外部依赖的人性化格式化工具库，用于将数值转换为易读的字符串表示。

## 功能特性

### 1. 字节格式化 (Bytes Formatting)
将字节转换为易读格式：
- `format_bytes(1024)` → "1.00 KB"
- `format_bytes(1536)` → "1.50 KB"
- `format_bytes(1048576)` → "1.00 MB"

支持自定义精度：
- `format_bytes_with_precision(1536, 0)` → "2 KB"
- `format_bytes_with_precision(1536, 1)` → "1.5 KB"

反向解析：
- `parse_bytes("1KB")` → 1024
- `parse_bytes("1.5 MB")` → 1572864

### 2. 时间格式化 (Duration Formatting)
将秒数转换为易读时间：
- `format_duration(3661)` → "1h 1m 1s"
- `format_duration(86400)` → "1d"
- `format_duration_long(90)` → "1 minute 30 seconds"

### 3. 数字格式化 (Number Formatting)
添加千位分隔符：
- `format_number(1000000, ',')` → "1,000,000"
- `format_number(1234567, '_')` → "1_234_567"
- `format_float(1234567.89, 2, ',')` → "1,234,567.89"

### 4. 序数格式化 (Ordinal Formatting)
转换为序数形式：
- `format_ordinal(1)` → "1st"
- `format_ordinal(2)` → "2nd"
- `format_ordinal(21)` → "21st"
- `format_ordinal(111)` → "111th"

### 5. 相对时间 (Relative Time)
生成相对时间描述：
- `format_relative_past(3600)` → "1 hour ago"
- `format_relative_future(86400)` → "in 1 day"
- `format_relative_time(timestamp)` → 自动判断过去/未来

### 6. 其他格式化
- 频率格式化：`format_frequency(1000000)` → "1.00 MHz"
- 百分比格式化：`format_percentage(0.123, 1)` → "12.3%"
- 比例格式化：`format_ratio(0.75, 100)` → "3/4"
- 复数格式化：`format_plural(5, "item", None)` → "5 items"
- 科学记数法：`format_scientific(1234567.0, 2)` → "1.23e6"

## 使用示例

```rust
use human_readable_utils::*;

// 字节格式化
println!("{}", format_bytes(1536)); // 1.50 KB

// 时间格式化
println!("{}", format_duration(3661)); // 1h 1m 1s

// 数字格式化
println!("{}", format_number(1000000, ',')); // 1,000,000

// 序数格式化
println!("{}", format_ordinal(21)); // 21st

// 相对时间
println!("{}", format_relative_past(3600)); // 1 hour ago
```

## 运行测试

```bash
cargo test
```

## 运行示例

```bash
cargo run --example usage_examples
```

## 特点

- ✅ 零外部依赖
- ✅ 支持 B, KB, MB, GB, TB, PB, EB, ZB, YB
- ✅ 时间支持年、天、小时、分钟、秒
- ✅ 正确处理序数（11th, 12th, 13th 特例）
- ✅ 支持解析字节字符串
- ✅ 完整单元测试覆盖

## 作者

AllToolkit - 2026-05-02