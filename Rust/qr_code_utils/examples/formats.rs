//! 不同输出格式示例

use qr_code_utils::{QrCode, ErrorCorrectionLevel, OutputFormat, generate_qr_code, generate_qr_code_with_margin};

fn main() {
    println!("=== QR 码输出格式示例 ===\n");
    
    let data = "Hello";
    
    // 1. ASCII 艺术格式
    println!("1. ASCII 艺术格式（默认）:");
    let ascii = generate_qr_code(data, ErrorCorrectionLevel::M, OutputFormat::Ascii);
    println!("{}", ascii);
    println!("特点: 使用 ⬛/⬜ 字符，适合在支持 Unicode 的终端显示\n");
    
    // 2. 紧凑 ASCII 格式
    println!("{}", "=".repeat(50));
    println!("\n2. 紧凑 ASCII 格式:");
    let compact = generate_qr_code(data, ErrorCorrectionLevel::M, OutputFormat::AsciiCompact);
    println!("{}", compact);
    println!("特点: 使用 █ 字符，背景透明，更紧凑\n");
    
    // 3. 矩阵格式
    println!("{}", "=".repeat(50));
    println!("\n3. 矩阵格式:");
    let matrix = generate_qr_code(data, ErrorCorrectionLevel::M, OutputFormat::Matrix);
    println!("{}", matrix);
    println!("特点: 使用 ■/□ 字符，清晰显示每个模块\n");
    
    // 4. SVG 格式
    println!("{}", "=".repeat(50));
    println!("\n4. SVG 格式:");
    let svg = generate_qr_code(data, ErrorCorrectionLevel::M, OutputFormat::Svg);
    println!("{}", svg.lines().take(5).collect::<Vec<_>>().join("\n"));
    println!("... (共 {} 行)", svg.lines().count());
    println!("特点: 矢量图形，可缩放，适合网页和打印\n");
    
    // 5. 带边距的输出
    println!("{}", "=".repeat(50));
    println!("\n5. 自定义边距:");
    
    for margin in [0, 1, 2, 4] {
        println!("\n边距 = {}:", margin);
        let qr = generate_qr_code_with_margin(
            data,
            ErrorCorrectionLevel::M,
            OutputFormat::AsciiCompact,
            margin
        );
        println!("{}", qr);
    }
    
    // 6. 比较不同纠错级别的大小
    println!("{}", "=".repeat(50));
    println!("\n6. 不同纠错级别的大小比较:");
    
    let data_long = "这是一个更长的测试文本，用来展示不同纠错级别对 QR 码大小的影响。";
    
    println!("\n数据: \"{}\" ({} 字节)\n", data_long, data_long.len());
    
    for level in [ErrorCorrectionLevel::L, ErrorCorrectionLevel::M, 
                  ErrorCorrectionLevel::Q, ErrorCorrectionLevel::H] {
        let qr = QrCode::new(data_long, level);
        let info = qr.info();
        
        // 计算实际使用的模块数
        let mut black_count = 0;
        for row in qr.modules() {
            for &module in row {
                if module {
                    black_count += 1;
                }
            }
        }
        
        println!("级别 {}: {} (黑色模块: {}/{})", 
            level.identifier(), info, black_count, qr.size() * qr.size());
    }
    
    // 7. 实际应用示例
    println!("\n{}", "=".repeat(50));
    println!("\n7. 实际应用示例:");
    
    // WiFi 连接信息
    let wifi = "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;";
    println!("\nWiFi 配置:");
    let wifi_qr = QrCode::new(wifi, ErrorCorrectionLevel::H);
    println!("数据: {}", wifi);
    println!("{}", wifi_qr.to_ascii_compact_with_margin(2));
    
    // 联系人信息
    let contact = "BEGIN:VCARD\nVERSION:3.0\nFN:张三\nTEL:13800138000\nEMAIL:zhangsan@example.com\nEND:VCARD";
    println!("\n联系人名片:");
    let contact_qr = QrCode::new(contact, ErrorCorrectionLevel::M);
    println!("数据: {}", contact.replace('\n', " | "));
    println!("{}", contact_qr.to_ascii_compact_with_margin(2));
}