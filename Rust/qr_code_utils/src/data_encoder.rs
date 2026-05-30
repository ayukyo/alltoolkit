//! 数据编码器 - 将数据编码为 QR 码位流

use super::qr_code::ErrorCorrectionLevel;

/// 数据编码器
pub struct DataEncoder<'a> {
    data: &'a str,
    ec_level: ErrorCorrectionLevel,
}

impl<'a> DataEncoder<'a> {
    /// 创建新的编码器
    pub fn new(data: &'a str, ec_level: ErrorCorrectionLevel) -> Self {
        DataEncoder { data, ec_level }
    }
    
    /// 编码数据，返回版本和编码后的字节
    pub fn encode(&self) -> (usize, Vec<u8>) {
        let data_bytes = self.data.as_bytes();
        
        // 确定所需版本
        let version = self.determine_version(data_bytes.len());
        
        // 编码数据
        let encoded = self.encode_data(data_bytes, version);
        
        (version, encoded)
    }
    
    /// 确定需要的 QR 码版本
    fn determine_version(&self, data_len: usize) -> usize {
        // 简化版本确定：根据数据长度
        // 实际 QR 码版本容量表（字节模式，纠错级别 M）
        let capacities = [
            14,   // v1
            26,   // v2
            42,   // v3
            62,   // v4
            84,   // v5
            106,  // v6
            122,  // v7
            152,  // v8
            180,  // v9
            213,  // v10
            251,  // v11
            287,  // v12
            331,  // v13
            362,  // v14
            412,  // v15
            450,  // v16
            504,  // v17
            560,  // v18
            624,  // v19
            666,  // v20
            711,  // v21
            779,  // v22
            857,  // v23
            911,  // v24
            997,  // v25
            1059, // v26
            1125, // v27
            1190, // v28
            1264, // v29
            1370, // v30
            1452, // v31
            1538, // v32
            1628, // v33
            1722, // v34
            1809, // v35
            1911, // v36
            1989, // v37
            2099, // v38
            2213, // v39
            2331, // v40
        ];
        
        // 根据纠错级别调整容量
        let capacity_multiplier = match self.ec_level {
            ErrorCorrectionLevel::L => 1.0,
            ErrorCorrectionLevel::M => 0.85,
            ErrorCorrectionLevel::Q => 0.7,
            ErrorCorrectionLevel::H => 0.55,
        };
        
        for (version, &capacity) in capacities.iter().enumerate() {
            let adjusted_capacity = (capacity as f64 * capacity_multiplier) as usize;
            if data_len <= adjusted_capacity {
                return version + 1;
            }
        }
        
        // 默认返回最大版本
        40
    }
    
    /// 编码数据为 QR 码格式
    fn encode_data(&self, data: &[u8], version: usize) -> Vec<u8> {
        let mut bits = Vec::new();
        
        // 1. 模式指示器（字节模式 = 0100）
        self.add_bits(&mut bits, 0b0100u8, 4);
        
        // 2. 字符计数指示器
        let count_bits = if version <= 9 { 8 } else { 16 };
        self.add_bits(&mut bits, data.len() as u16, count_bits);
        
        // 3. 数据
        for &byte in data {
            self.add_bits(&mut bits, byte, 8);
        }
        
        // 4. 终止符（0000）
        self.add_bits(&mut bits, 0u8, 4);
        
        // 5. 填充到字节边界
        while bits.len() % 8 != 0 {
            bits.push(false);
        }
        
        // 6. 添加填充码字
        let total_codewords = self.get_total_codewords(version);
        let current_codewords = bits.len() / 8;
        let mut pad_alternator = false;
        
        for _ in current_codewords..total_codewords {
            let pad_byte: u8 = if pad_alternator { 0xEC } else { 0x11 };
            self.add_bits(&mut bits, pad_byte, 8);
            pad_alternator = !pad_alternator;
        }
        
        // 转换为字节
        self.bits_to_bytes(&bits)
    }
    
    /// 添加位到位数组
    fn add_bits<T: Into<u32>>(&self, bits: &mut Vec<bool>, value: T, count: usize) {
        let value = value.into();
        for i in (0..count).rev() {
            bits.push((value >> i) & 1 == 1);
        }
    }
    
    /// 获取总码字数（数据码字 + 纠错码字）
    fn get_total_codewords(&self, version: usize) -> usize {
        // 简化的码字数量表
        let base_codewords = match version {
            1 => 26,
            2 => 44,
            3 => 70,
            4 => 100,
            5 => 134,
            6 => 172,
            7 => 196,
            8 => 242,
            9 => 292,
            10 => 346,
            _ => 346 + (version - 10) * 60,
        };
        
        // 根据纠错级别调整
        let ec_multiplier = match self.ec_level {
            ErrorCorrectionLevel::L => 0.8,
            ErrorCorrectionLevel::M => 0.7,
            ErrorCorrectionLevel::Q => 0.6,
            ErrorCorrectionLevel::H => 0.5,
        };
        
        (base_codewords as f64 * ec_multiplier) as usize
    }
    
    /// 将位数组转换为字节数组
    fn bits_to_bytes(&self, bits: &[bool]) -> Vec<u8> {
        let mut bytes = Vec::new();
        for chunk in bits.chunks(8) {
            let mut byte = 0u8;
            for (i, &bit) in chunk.iter().enumerate() {
                if bit {
                    byte |= 1 << (7 - i);
                }
            }
            bytes.push(byte);
        }
        bytes
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encoder_creation() {
        let encoder = DataEncoder::new("Test", ErrorCorrectionLevel::M);
        assert_eq!(encoder.data, "Test");
    }

    #[test]
    fn test_encode_simple() {
        let encoder = DataEncoder::new("Hello", ErrorCorrectionLevel::L);
        let (version, data) = encoder.encode();
        assert!(version >= 1 && version <= 40);
        assert!(!data.is_empty());
    }

    #[test]
    fn test_version_determination() {
        let encoder = DataEncoder::new("Hi", ErrorCorrectionLevel::L);
        let version = encoder.determine_version(2);
        assert_eq!(version, 1);
        
        let encoder2 = DataEncoder::new("", ErrorCorrectionLevel::L);
        let version2 = encoder2.determine_version(100);
        assert!(version2 > 1);
    }

    #[test]
    fn test_different_ec_levels() {
        for level in [ErrorCorrectionLevel::L, ErrorCorrectionLevel::M,
                      ErrorCorrectionLevel::Q, ErrorCorrectionLevel::H] {
            let encoder = DataEncoder::new("Test", level);
            let (version, _) = encoder.encode();
            assert!(version >= 1);
        }
    }
}