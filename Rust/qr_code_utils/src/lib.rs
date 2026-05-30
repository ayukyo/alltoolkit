//! QR Code Generator - 零依赖 QR 码生成器
//! 
//! 支持功能：
//! - 多种数据编码模式（数字、字母数字、字节模式）
//! - 四种纠错级别（L、M、Q、H）
//! - 多种版本（1-40，对应不同大小）
//! - ASCII 艺术输出
//! - SVG 输出

pub mod qr_code;
pub mod reed_solomon;
pub mod data_encoder;
pub mod matrix;

pub use qr_code::QrCode;
pub use qr_code::ErrorCorrectionLevel;

/// QR 码输出格式
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutputFormat {
    /// ASCII 艺术格式（终端友好）
    Ascii,
    /// ASCII 艺术格式（紧凑，使用单个字符）
    AsciiCompact,
    /// 字符串矩阵（布尔值二维数组）
    Matrix,
    /// SVG 矢量图形
    Svg,
}

/// 生成 QR 码的便捷函数
/// 
/// # 参数
/// - `data`: 要编码的数据
/// - `level`: 纠错级别
/// - `format`: 输出格式
/// 
/// # 返回
/// 编码后的 QR 码字符串（根据格式不同返回不同形式）
/// 
/// # 示例
/// ```rust
/// use qr_code_utils::{generate_qr_code, ErrorCorrectionLevel, OutputFormat};
/// 
/// let result = generate_qr_code("Hello, World!", ErrorCorrectionLevel::M, OutputFormat::Ascii);
/// println!("{}", result);
/// ```
pub fn generate_qr_code(data: &str, level: ErrorCorrectionLevel, format: OutputFormat) -> String {
    let qr = QrCode::new(data, level);
    
    match format {
        OutputFormat::Ascii => qr.to_ascii(),
        OutputFormat::AsciiCompact => qr.to_ascii_compact(),
        OutputFormat::Matrix => qr.to_matrix_string(),
        OutputFormat::Svg => qr.to_svg(),
    }
}

/// 生成指定边距的 QR 码
pub fn generate_qr_code_with_margin(
    data: &str, 
    level: ErrorCorrectionLevel, 
    format: OutputFormat,
    margin: usize
) -> String {
    let qr = QrCode::new(data, level);
    
    match format {
        OutputFormat::Ascii => qr.to_ascii_with_margin(margin),
        OutputFormat::AsciiCompact => qr.to_ascii_compact_with_margin(margin),
        OutputFormat::Matrix => qr.to_matrix_string_with_margin(margin),
        OutputFormat::Svg => qr.to_svg_with_margin(margin),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_simple_qr() {
        let result = generate_qr_code("Hello", ErrorCorrectionLevel::L, OutputFormat::Ascii);
        assert!(!result.is_empty());
        assert!(result.contains('█') || result.contains('⬛'));
    }

    #[test]
    fn test_qr_code_creation() {
        let qr = QrCode::new("Test", ErrorCorrectionLevel::M);
        assert!(qr.size() > 0);
    }

    #[test]
    fn test_different_error_levels() {
        for level in [ErrorCorrectionLevel::L, ErrorCorrectionLevel::M, 
                      ErrorCorrectionLevel::Q, ErrorCorrectionLevel::H] {
            let qr = QrCode::new("Test", level);
            assert!(qr.size() > 0);
        }
    }

    #[test]
    fn test_svg_output() {
        let svg = generate_qr_code("SVG Test", ErrorCorrectionLevel::M, OutputFormat::Svg);
        assert!(svg.contains("<svg"));
        assert!(svg.contains("</svg>"));
    }

    #[test]
    fn test_matrix_output() {
        let matrix = generate_qr_code("Matrix", ErrorCorrectionLevel::L, OutputFormat::Matrix);
        assert!(matrix.contains('■') || matrix.contains('□'));
    }

    #[test]
    fn test_empty_data() {
        let qr = QrCode::new("", ErrorCorrectionLevel::L);
        // 空数据应该仍然生成一个有效的 QR 码结构
        assert!(qr.size() > 0);
    }

    #[test]
    fn test_long_data() {
        let long_data = "A".repeat(100);
        let qr = QrCode::new(&long_data, ErrorCorrectionLevel::L);
        assert!(qr.size() > 0);
    }
}