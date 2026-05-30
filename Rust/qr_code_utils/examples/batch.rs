//! 批量 QR 码生成示例

use qr_code_utils::{QrCode, ErrorCorrectionLevel};

fn main() {
    println!("=== 批量 QR 码生成示例 ===\n");
    
    // 要编码的数据列表
    let urls = vec![
        "https://github.com/openclaw/openclaw",
        "https://docs.openclaw.ai",
        "https://clawhub.com",
        "https://discord.com/invite/clawd",
        "mailto:hello@openclaw.ai",
    ];
    
    println!("批量生成 {} 个 URL 的 QR 码:\n", urls.len());
    
    for (i, url) in urls.iter().enumerate() {
        println!("--- QR 码 #{} ---", i + 1);
        println!("URL: {}", url);
        
        let qr = QrCode::new(url, ErrorCorrectionLevel::M);
        println!("信息: {}", qr.info());
        println!();
        println!("{}", qr.to_ascii_compact_with_margin(1));
        println!();
    }
    
    // 不同纠错级别测试
    println!("=== 纠错级别性能测试 ===\n");
    
    let test_data = "这是一个测试字符串，用于演示不同纠错级别下 QR 码的大小变化。";
    
    for level in [ErrorCorrectionLevel::L, ErrorCorrectionLevel::M, 
                  ErrorCorrectionLevel::Q, ErrorCorrectionLevel::H] {
        let qr = QrCode::new(test_data, level);
        let module_count = qr.size() * qr.size();
        
        println!("级别 {}: 版本={}, 尺寸={}x{}, 模块数={}",
            level.identifier(),
            qr.version(),
            qr.size(),
            qr.size(),
            module_count
        );
    }
    
    println!();
    
    // 长文本测试
    println!("=== 长文本编码测试 ===\n");
    
    let long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                     Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
                     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.";
    
    println!("文本长度: {} 字节", long_text.len());
    
    let qr = QrCode::new(long_text, ErrorCorrectionLevel::L);
    println!("QR 码信息: {}", qr.info());
    println!("\n生成的 QR 码:");
    println!("{}", qr.to_ascii_compact_with_margin(1));
}