//! QR 码核心实现

use crate::data_encoder::DataEncoder;
use crate::matrix::MatrixBuilder;
use crate::reed_solomon::ReedSolomon;

/// 纠错级别
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorCorrectionLevel {
    /// L - 约 7% 纠错能力
    L,
    /// M - 约 15% 纠错能力
    M,
    /// Q - 约 25% 纠错能力
    Q,
    /// H - 约 30% 纠错能力
    H,
}

impl ErrorCorrectionLevel {
    /// 获取纠错码字数（相对于数据码字的百分比）
    pub fn ec_codewords_percentage(&self) -> usize {
        match self {
            ErrorCorrectionLevel::L => 7,
            ErrorCorrectionLevel::M => 15,
            ErrorCorrectionLevel::Q => 25,
            ErrorCorrectionLevel::H => 30,
        }
    }
    
    /// 获取级别标识符
    pub fn identifier(&self) -> char {
        match self {
            ErrorCorrectionLevel::L => 'L',
            ErrorCorrectionLevel::M => 'M',
            ErrorCorrectionLevel::Q => 'Q',
            ErrorCorrectionLevel::H => 'H',
        }
    }
}

/// QR 码结构
#[derive(Debug, Clone)]
pub struct QrCode {
    /// 版本 (1-40)
    version: usize,
    /// 纠错级别
    ec_level: ErrorCorrectionLevel,
    /// 数据模块矩阵 (true = 黑色, false = 白色)
    modules: Vec<Vec<bool>>,
    /// 尺寸（边长）
    size: usize,
}

impl QrCode {
    /// 创建新的 QR 码
    pub fn new(data: &str, ec_level: ErrorCorrectionLevel) -> Self {
        // 1. 编码数据
        let encoder = DataEncoder::new(data, ec_level);
        let (version, encoded_data) = encoder.encode();
        
        // 2. 添加纠错码
        let data_with_ec = ReedSolomon::add_error_correction(&encoded_data, ec_level, version);
        
        // 3. 构建矩阵
        let size = 17 + version * 4; // QR 码尺寸公式
        let modules = MatrixBuilder::build(&data_with_ec, version, size, ec_level);
        
        QrCode {
            version,
            ec_level,
            modules,
            size,
        }
    }
    
    /// 获取 QR 码尺寸
    pub fn size(&self) -> usize {
        self.size
    }
    
    /// 获取版本
    pub fn version(&self) -> usize {
        self.version
    }
    
    /// 获取模块矩阵
    pub fn modules(&self) -> &[Vec<bool>] {
        &self.modules
    }
    
    /// 获取指定位置的模块值
    pub fn module(&self, x: usize, y: usize) -> bool {
        if x < self.size && y < self.size {
            self.modules[y][x]
        } else {
            false
        }
    }
    
    /// 转换为 ASCII 艺术
    pub fn to_ascii(&self) -> String {
        self.to_ascii_with_margin(2)
    }
    
    /// 转换为带边距的 ASCII 艺术
    pub fn to_ascii_with_margin(&self, margin: usize) -> String {
        let mut result = String::new();
        
        // 上边距
        for _ in 0..margin {
            for _ in 0..self.size + 2 * margin {
                result.push('⬜');
            }
            result.push('\n');
        }
        
        // QR 码主体
        for row in &self.modules {
            // 左边距
            for _ in 0..margin {
                result.push('⬜');
            }
            // 数据
            for &module in row {
                result.push(if module { '⬛' } else { '⬜' });
            }
            // 右边距
            for _ in 0..margin {
                result.push('⬜');
            }
            result.push('\n');
        }
        
        // 下边距
        for _ in 0..margin {
            for _ in 0..self.size + 2 * margin {
                result.push('⬜');
            }
            result.push('\n');
        }
        
        result
    }
    
    /// 转换为紧凑 ASCII 艺术
    pub fn to_ascii_compact(&self) -> String {
        self.to_ascii_compact_with_margin(1)
    }
    
    /// 转换为带边距的紧凑 ASCII 艺术
    pub fn to_ascii_compact_with_margin(&self, margin: usize) -> String {
        let mut result = String::new();
        
        // 上边距
        for _ in 0..margin {
            for _ in 0..self.size + 2 * margin {
                result.push(' ');
            }
            result.push('\n');
        }
        
        // QR 码主体
        for row in &self.modules {
            for _ in 0..margin {
                result.push(' ');
            }
            for &module in row {
                result.push(if module { '█' } else { ' ' });
            }
            for _ in 0..margin {
                result.push(' ');
            }
            result.push('\n');
        }
        
        // 下边距
        for _ in 0..margin {
            for _ in 0..self.size + 2 * margin {
                result.push(' ');
            }
            result.push('\n');
        }
        
        result
    }
    
    /// 转换为矩阵字符串（使用 ■ □）
    pub fn to_matrix_string(&self) -> String {
        self.to_matrix_string_with_margin(0)
    }
    
    /// 转换为带边距的矩阵字符串
    pub fn to_matrix_string_with_margin(&self, margin: usize) -> String {
        let mut result = String::new();
        
        // 上边距
        for _ in 0..margin {
            result.push_str(&"□ ".repeat(self.size + 2 * margin));
            result.push('\n');
        }
        
        // 主体
        for row in &self.modules {
            for _ in 0..margin {
                result.push_str("□ ");
            }
            for &module in row {
                result.push_str(if module { "■ " } else { "□ " });
            }
            for _ in 0..margin {
                result.push_str("□ ");
            }
            result.push('\n');
        }
        
        // 下边距
        for _ in 0..margin {
            result.push_str(&"□ ".repeat(self.size + 2 * margin));
            result.push('\n');
        }
        
        result
    }
    
    /// 转换为 SVG
    pub fn to_svg(&self) -> String {
        self.to_svg_with_margin(4)
    }
    
    /// 转换为带边距的 SVG
    pub fn to_svg_with_margin(&self, margin: usize) -> String {
        let module_size = 10;
        let total_size = (self.size + 2 * margin) * module_size;
        
        let mut svg = format!(
            r#"<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {} {}" width="{}" height="{}">
<rect width="100%" height="100%" fill="white"/>
"#,
            total_size, total_size, total_size, total_size
        );
        
        // 绘制黑色模块
        for (y, row) in self.modules.iter().enumerate() {
            for (x, &module) in row.iter().enumerate() {
                if module {
                    let px = (x + margin) * module_size;
                    let py = (y + margin) * module_size;
                    svg.push_str(&format!(
                        r#"<rect x="{}" y="{}" width="{}" height="{}" fill="black"/>"#,
                        px, py, module_size, module_size
                    ));
                    svg.push('\n');
                }
            }
        }
        
        svg.push_str("</svg>");
        svg
    }
    
    /// 获取信息
    pub fn info(&self) -> String {
        format!(
            "QR Code v{}, EC Level: {}, Size: {}x{}",
            self.version,
            self.ec_level.identifier(),
            self.size,
            self.size
        )
    }
}

impl std::fmt::Display for QrCode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.to_ascii_compact())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_qr_code_creation() {
        let qr = QrCode::new("Hello", ErrorCorrectionLevel::M);
        assert!(qr.size() >= 21); // 版本 1 最小 21x21
    }

    #[test]
    fn test_different_versions() {
        // 短数据应该是版本 1
        let qr1 = QrCode::new("Hi", ErrorCorrectionLevel::L);
        assert_eq!(qr1.version(), 1);
        
        // 较长数据应该需要更高版本
        let long_data = "A".repeat(50);
        let qr2 = QrCode::new(&long_data, ErrorCorrectionLevel::L);
        assert!(qr2.version() >= 1);
    }

    #[test]
    fn test_ascii_output() {
        let qr = QrCode::new("Test", ErrorCorrectionLevel::L);
        let ascii = qr.to_ascii();
        assert!(ascii.contains('⬛') || ascii.contains('⬜'));
    }

    #[test]
    fn test_svg_output() {
        let qr = QrCode::new("SVG", ErrorCorrectionLevel::M);
        let svg = qr.to_svg();
        assert!(svg.starts_with("<svg"));
        assert!(svg.contains("</svg>"));
    }

    #[test]
    fn test_module_access() {
        let qr = QrCode::new("Test", ErrorCorrectionLevel::L);
        // 检查定位图案（应该在角落有黑色模块）
        assert!(qr.module(0, 0)); // 左上角应该是黑色
    }
}