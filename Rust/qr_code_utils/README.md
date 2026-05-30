# QR Code Utils

零依赖 QR 码生成器，纯 Rust 实现。

## 功能特性

- ✅ 多种编码模式（数字、字母数字、字节模式）
- ✅ 四种纠错级别（L、M、Q、H）
- ✅ 支持 40 种版本（1-40）
- ✅ ASCII 艺术输出
- ✅ SVG 矢量输出
- ✅ 矩阵格式输出
- ✅ 自定义边距
- ✅ 零外部依赖
- ✅ `no_std` 支持

## 快速开始

```rust
use qr_code_utils::{generate_qr_code, ErrorCorrectionLevel, OutputFormat};

// 最简单的用法
let qr = generate_qr_code("Hello, World!", ErrorCorrectionLevel::M, OutputFormat::Ascii);
println!("{}", qr);
```

## 输出格式

### 1. ASCII 艺术（Unicode）
```rust
let qr = generate_qr_code("Hello", ErrorCorrectionLevel::M, OutputFormat::Ascii);
// 输出使用 ⬛/⬜ 字符
```

### 2. 紧凑 ASCII
```rust
let qr = generate_qr_code("Hello", ErrorCorrectionLevel::M, OutputFormat::AsciiCompact);
// 输出使用 █ 字符，背景透明
```

### 3. 矩阵格式
```rust
let qr = generate_qr_code("Hello", ErrorCorrectionLevel::M, OutputFormat::Matrix);
// 输出使用 ■/□ 字符
```

### 4. SVG 格式
```rust
let qr = generate_qr_code("Hello", ErrorCorrectionLevel::M, OutputFormat::Svg);
// 输出标准 SVG 矢量图形
```

## 纠错级别

| 级别 | 纠错能力 | 适用场景 |
|------|---------|---------|
| L | ~7% | 高质量印刷，空间有限 |
| M | ~15% | 一般用途（推荐） |
| Q | ~25% | 可能受损的场景 |
| H | ~30% | 极端环境，可叠加 Logo |

## API 参考

### 便捷函数

```rust
// 基础生成
fn generate_qr_code(
    data: &str, 
    level: ErrorCorrectionLevel, 
    format: OutputFormat
) -> String;

// 带边距生成
fn generate_qr_code_with_margin(
    data: &str,
    level: ErrorCorrectionLevel,
    format: OutputFormat,
    margin: usize
) -> String;
```

### QrCode 对象

```rust
use qr_code_utils::QrCode;

// 创建 QR 码
let qr = QrCode::new("Hello", ErrorCorrectionLevel::M);

// 获取信息
println!("版本: {}", qr.version());  // 1-40
println!("尺寸: {}", qr.size());     // 边长（模块数）

// 输出方法
qr.to_ascii();                    // ASCII 艺术
qr.to_ascii_with_margin(4);       // 带边距 ASCII
qr.to_ascii_compact();            // 紧凑 ASCII
qr.to_matrix_string();            // 矩阵字符串
qr.to_svg();                      // SVG 字符串
qr.to_svg_with_margin(4);         // 带边距 SVG

// 访问原始数据
let modules = qr.modules();       // &Vec<Vec<bool>>
let is_black = qr.module(0, 0);   // 获取指定位置模块
```

## 示例

### WiFi 配置二维码
```rust
let wifi = "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;";
let qr = generate_qr_code(wifi, ErrorCorrectionLevel::H, OutputFormat::Ascii);
println!("{}", qr);
```

### 联系人名片
```rust
let vcard = "BEGIN:VCARD\nVERSION:3.0\nFN:张三\nTEL:13800138000\nEND:VCARD";
let qr = generate_qr_code(vcard, ErrorCorrectionLevel::M, OutputFormat::Svg);
// 保存到文件或发送到网页
```

### URL 短链接
```rust
let url = "https://github.com/openclaw/openclaw";
let qr = QrCode::new(url, ErrorCorrectionLevel::L);
println!("{}", qr.to_ascii_compact_with_margin(2));
```

## 运行示例

```bash
# 基础示例
cargo run --example basic

# 批量生成
cargo run --example batch

# 格式对比
cargo run --example formats
```

## 运行测试

```bash
cargo test
```

## 技术细节

### 编码流程
1. 数据编码（字节模式）
2. 添加纠错码（Reed-Solomon）
3. 构建矩阵（定位图案、时序图案、对齐图案）
4. 放置数据
5. 添加格式信息
6. 应用掩码

### 数据容量（字节模式，纠错级别 M）

| 版本 | 尺寸 | 容量 |
|-----|------|-----|
| 1 | 21×21 | 14 |
| 5 | 37×37 | 84 |
| 10 | 57×57 | 213 |
| 20 | 97×97 | 666 |
| 40 | 177×177 | 2331 |

## 许可证

MIT License