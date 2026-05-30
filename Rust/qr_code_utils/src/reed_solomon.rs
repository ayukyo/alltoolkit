//! Reed-Solomon 纠错码生成器
//! 零依赖实现，用于 QR 码纠错

use super::qr_code::ErrorCorrectionLevel;

/// GF(256) 域运算
struct GaloisField;

impl GaloisField {
    /// GF(2^8) 的本原多项式相关常数
    const PRIMITIVE: u8 = 0x1D; // x^8 + x^4 + x^3 + x^2 + 1
    
    /// 预计算的对数表
    fn generate_log_table() -> [u8; 256] {
        let mut log = [0u8; 256];
        let mut x = 1u8;
        
        for i in 0..255 {
            log[x as usize] = i;
            x = x.wrapping_mul(2);
            if x & 0x80 != 0 {
                x ^= Self::PRIMITIVE;
            }
        }
        
        log
    }
    
    /// 预计算的反对数表
    fn generate_antilog_table() -> [u8; 256] {
        let mut antilog = [0u8; 256];
        let mut x = 1u8;
        
        for i in 0..255 {
            antilog[i] = x;
            x = x.wrapping_mul(2);
            if x & 0x80 != 0 {
                x ^= Self::PRIMITIVE;
            }
        }
        antilog[255] = antilog[0];
        
        antilog
    }
}

/// Reed-Solomon 编码器
pub struct ReedSolomon;

impl ReedSolomon {
    /// 为数据添加纠错码
    pub fn add_error_correction(data: &[u8], ec_level: ErrorCorrectionLevel, version: usize) -> Vec<u8> {
        let ec_codewords = Self::get_ec_codewords_count(ec_level, version);
        
        // 生成生成多项式
        let generator = Self::generate_generator_polynomial(ec_codewords);
        
        // 计算纠错码
        let ec_codes = Self::calculate_ec_codewords(data, &generator, ec_codewords);
        
        // 组合数据和纠错码
        let mut result = Vec::with_capacity(data.len() + ec_codewords);
        result.extend_from_slice(data);
        result.extend_from_slice(&ec_codes);
        
        result
    }
    
    /// 获取纠错码字数
    fn get_ec_codewords_count(ec_level: ErrorCorrectionLevel, version: usize) -> usize {
        // 简化的纠错码字数表
        let base_count = match ec_level {
            ErrorCorrectionLevel::L => 7,
            ErrorCorrectionLevel::M => 10,
            ErrorCorrectionLevel::Q => 13,
            ErrorCorrectionLevel::H => 17,
        };
        
        // 根据版本调整
        let version_factor = if version <= 10 { 1 } 
                           else if version <= 20 { 2 } 
                           else if version <= 30 { 3 } 
                           else { 4 };
        
        base_count * version_factor
    }
    
    /// 生成生成多项式
    fn generate_generator_polynomial(degree: usize) -> Vec<u8> {
        if degree == 0 {
            return vec![1];
        }
        
        let log = GaloisField::generate_log_table();
        let antilog = GaloisField::generate_antilog_table();
        
        let mut gen = vec![1u8];
        
        for i in 0..degree {
            let mut new_gen = vec![0u8; gen.len() + 1];
            
            for (j, &coef) in gen.iter().enumerate() {
                // 乘以 (x - α^i)
                new_gen[j] ^= coef; // 减法在 GF(2) 中等于加法
                let exp = (i + j) % 255;
                new_gen[j + 1] ^= Self::gf_multiply(coef, antilog[exp], &log, &antilog);
            }
            
            gen = new_gen;
        }
        
        gen
    }
    
    /// 计算纠错码字
    fn calculate_ec_codewords(data: &[u8], generator: &[u8], ec_count: usize) -> Vec<u8> {
        let log = GaloisField::generate_log_table();
        let antilog = GaloisField::generate_antilog_table();
        
        // 确保 remainder 有足够空间
        let total_len = data.len().max(generator.len()).max(ec_count);
        let mut remainder = vec![0u8; total_len];
        for (i, &byte) in data.iter().enumerate() {
            remainder[i] = byte;
        }
        
        // 多项式除法
        for i in 0..data.len() {
            if remainder[i] != 0 {
                for (j, &gen_coef) in generator.iter().enumerate() {
                    if i + j < remainder.len() {
                        let product = Self::gf_multiply(remainder[i], gen_coef, &log, &antilog);
                        remainder[i + j] ^= product;
                    }
                }
            }
        }
        
        // 取后 ec_count 个字节作为纠错码
        let start = total_len.saturating_sub(ec_count);
        remainder[start..total_len].to_vec()
    }
    
    /// GF(256) 乘法
    fn gf_multiply(a: u8, b: u8, log: &[u8; 256], antilog: &[u8; 256]) -> u8 {
        if a == 0 || b == 0 {
            return 0;
        }
        
        let log_sum = (log[a as usize] as usize + log[b as usize] as usize) % 255;
        antilog[log_sum]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_error_correction() {
        let data = vec![0x40, 0xD5, 0x6C, 0x61, 0x72, 0x67, 0x65];
        let result = ReedSolomon::add_error_correction(&data, ErrorCorrectionLevel::M, 1);
        
        // 结果应该比原始数据长
        assert!(result.len() > data.len());
    }

    #[test]
    fn test_different_ec_levels() {
        let data = vec![1, 2, 3, 4, 5];
        
        for level in [ErrorCorrectionLevel::L, ErrorCorrectionLevel::M,
                      ErrorCorrectionLevel::Q, ErrorCorrectionLevel::H] {
            let result = ReedSolomon::add_error_correction(&data, level, 1);
            assert!(result.len() > data.len());
        }
    }

    #[test]
    fn test_generator_polynomial() {
        // 测试生成多项式
        let gen = ReedSolomon::generate_generator_polynomial(2);
        assert!(!gen.is_empty());
    }

    #[test]
    fn test_empty_data() {
        let data: Vec<u8> = vec![];
        let result = ReedSolomon::add_error_correction(&data, ErrorCorrectionLevel::L, 1);
        // 空数据应该仍然生成纠错码
        assert!(!result.is_empty());
    }
}