//! 基础 QR 码生成示例

use qr_code_utils::{QrCode, ErrorCorrectionLevel, OutputFormat, generate_qr_code};

fn main() {
    println!("=== QR 码生成器基础示例 ===\n");
    
    // 示例 1: 最简单的用法
    println!("1. 生成简单的 QR 码:");
    let qr = generate_qr_code("Hello, World!", ErrorCorrectionLevel::M, OutputFormat::Ascii);
    println!("{}", qr);
    
    println!("\n{}\n", "=".repeat(50));
    
    // 示例 2: 使用紧凑 ASCII 格式
    println!("2. 紧凑格式 QR 码:");
    let qr_compact = generate_qr_code("https://github.com", ErrorCorrectionLevel::L, OutputFormat::AsciiCompact);
    println!("{}", qr_compact);
    
    println!("\n{}\n", "=".repeat(50));
    
    // 示例 3: 不同纠错级别
    println!("3. 不同纠错级别对比:");
    let data = "测试数据";
    for level in [ErrorCorrectionLevel::L, ErrorCorrectionLevel::M, 
                  ErrorCorrectionLevel::Q, ErrorCorrectionLevel::H] {
        let qr = QrCode::new(data, level);
        println!("  级别 {}: {}", level.identifier(), qr.info());
    }
    
    println!("\n{}\n", "=".repeat(50));
    
    // 示例 4: 矩阵格式
    println!("4. 矩阵格式输出:");
    let qr_matrix = generate_qr_code("Matrix", ErrorCorrectionLevel::M, OutputFormat::Matrix);
    println!("{}", qr_matrix);
    
    println!("\n{}\n", "=".repeat(50));
    
    // 示例 5: 直接使用 QrCode 对象
    println!("5. 直接使用 QrCode 对象:");
    let qr = QrCode::new("OpenClaw", ErrorCorrectionLevel::H);
    println!("版本: {}", qr.version());
    println!("尺寸: {}x{}", qr.size(), qr.size());
    println!("\n{}", qr.to_ascii_with_margin(3));
}