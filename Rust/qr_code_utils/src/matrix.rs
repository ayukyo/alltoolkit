//! QR 码矩阵构建器
//! 负责将编码数据放置到 QR 码矩阵中

use super::qr_code::ErrorCorrectionLevel;

/// QR 码矩阵构建器
pub struct MatrixBuilder;

impl MatrixBuilder {
    /// 构建 QR 码矩阵
    pub fn build(data: &[u8], version: usize, size: usize, ec_level: ErrorCorrectionLevel) -> Vec<Vec<bool>> {
        // 初始化矩阵（false = 白色）
        let mut matrix = vec![vec![false; size]; size];
        
        // 1. 添加定位图案（三个角落的大方块）
        Self::add_finder_patterns(&mut matrix, size);
        
        // 2. 添加分隔符
        Self::add_separator_patterns(&mut matrix, size);
        
        // 3. 添加时序图案
        Self::add_timing_patterns(&mut matrix, size);
        
        // 4. 添加对齐图案（版本 >= 2）
        if version >= 2 {
            Self::add_alignment_patterns(&mut matrix, version, size);
        }
        
        // 5. 添加暗模块
        matrix[size - 8][8] = true;
        
        // 6. 保留格式信息区域
        Self::reserve_format_info(&mut matrix, size);
        
        // 7. 放置数据
        Self::place_data(&mut matrix, data, size);
        
        // 8. 添加格式信息
        Self::add_format_info(&mut matrix, ec_level, size);
        
        // 9. 应用掩码
        Self::apply_mask(&mut matrix, size);
        
        matrix
    }
    
    /// 添加定位图案
    fn add_finder_patterns(matrix: &mut [Vec<bool>], size: usize) {
        // 定位图案尺寸：7x7 外框 + 5x5 黑色 + 3x3 白色 + 1x1 黑色中心
        let positions = [(0, 0), (size - 7, 0), (0, size - 7)];
        
        for &(start_x, start_y) in &positions {
            for y in 0..7 {
                for x in 0..7 {
                    if start_x + x < size && start_y + y < size {
                        let is_black = y == 0 || y == 6 || x == 0 || x == 6 ||
                                       (y >= 2 && y <= 4 && x >= 2 && x <= 4);
                        matrix[start_y + y][start_x + x] = is_black;
                    }
                }
            }
        }
    }
    
    /// 添加分隔符
    fn add_separator_patterns(matrix: &mut [Vec<bool>], size: usize) {
        // 在定位图案周围添加白色分隔符
        // 左上角
        for i in 0..8 {
            matrix[7][i] = false;
            matrix[i][7] = false;
        }
        // 右上角
        for i in 0..8 {
            matrix[7][size - 8 + i] = false;
            matrix[i][size - 8] = false;
        }
        // 左下角
        for i in 0..8 {
            matrix[size - 8][i] = false;
            matrix[size - 8 + i][7] = false;
        }
    }
    
    /// 添加时序图案
    fn add_timing_patterns(matrix: &mut [Vec<bool>], size: usize) {
        // 水平时序图案
        for x in 8..size - 8 {
            matrix[6][x] = x % 2 == 0;
        }
        
        // 垂直时序图案
        for y in 8..size - 8 {
            matrix[y][6] = y % 2 == 0;
        }
    }
    
    /// 添加对齐图案
    fn add_alignment_patterns(matrix: &mut [Vec<bool>], version: usize, size: usize) {
        let positions = Self::get_alignment_positions(version, size);
        
        for &(cx, cy) in &positions {
            // 检查是否与定位图案重叠
            if (cx < 10 && cy < 10) || 
               (cx > size - 10 && cy < 10) || 
               (cx < 10 && cy > size - 10) {
                continue;
            }
            
            // 添加 5x5 对齐图案
            for y in -2..=2 {
                for x in -2..=2 {
                    let px = (cx as isize + x) as usize;
                    let py = (cy as isize + y) as usize;
                    if px < size && py < size {
                        let is_black = y.abs() == 2 || x.abs() == 2 || (y == 0 && x == 0);
                        matrix[py][px] = is_black;
                    }
                }
            }
        }
    }
    
    /// 获取对齐图案位置
    fn get_alignment_positions(version: usize, size: usize) -> Vec<(usize, usize)> {
        let mut positions = Vec::new();
        
        // 对齐图案位置取决于版本
        if version >= 2 {
            let intervals = match version {
                2..=6 => vec![size - 7],
                7..=13 => vec![size - 7, size / 2],
                14..=20 => vec![size - 7, size / 2, size / 4],
                _ => vec![size - 7, size / 2, size / 3],
            };
            
            for &x in &intervals {
                for &y in &intervals {
                    positions.push((x, y));
                }
            }
        }
        
        positions
    }
    
    /// 保留格式信息区域
    fn reserve_format_info(matrix: &mut [Vec<bool>], size: usize) {
        // 左上角格式信息
        for i in 0..9 {
            matrix[8][i] = false; // 水平
            matrix[i][8] = false; // 垂直
        }
        
        // 右上角和左下角格式信息
        for i in 0..8 {
            matrix[8][size - 8 + i] = false; // 右上角
            matrix[size - 8 + i][8] = false; // 左下角
        }
    }
    
    /// 放置数据
    fn place_data(matrix: &mut [Vec<bool>], data: &[u8], size: usize) {
        let mut bit_index = 0;
        let total_bits = data.len() * 8;
        
        // 从右向左，之字形路径
        let mut x: i32 = (size - 1) as i32;
        let mut up = true;
        
        while x >= 0 {
            if x == 6 {
                x -= 1; // 跳过时序图案
            }
            
            let y_range: Vec<usize> = if up {
                (0..size).collect()
            } else {
                (0..size).rev().collect()
            };
            
            for y in y_range {
                // 两列
                for dx in 0..2i32 {
                    let col = (x - dx) as usize;
                    if col < size && !Self::is_reserved(matrix, col, y, size) {
                        if bit_index < total_bits {
                            let byte_index = bit_index / 8;
                            let bit_pos = 7 - (bit_index % 8);
                            let bit = (data[byte_index] >> bit_pos) & 1 == 1;
                            matrix[y][col] = bit;
                            bit_index += 1;
                        }
                    }
                }
            }
            
            x -= 2;
            up = !up;
        }
    }
    
    /// 检查位置是否被保留
    fn is_reserved(_matrix: &[Vec<bool>], x: usize, y: usize, size: usize) -> bool {
        // 检查是否在保留区域
        // 定位图案
        if (x < 9 && y < 9) || (x + 8 >= size && y < 9) || (x < 9 && y + 8 >= size) {
            return true;
        }
        
        // 时序图案
        if x == 6 || y == 6 {
            return true;
        }
        
        // 格式信息区域
        if x == 8 || y == 8 {
            return true;
        }
        
        false
    }
    
    /// 添加格式信息
    fn add_format_info(matrix: &mut [Vec<bool>], ec_level: ErrorCorrectionLevel, size: usize) {
        // 格式信息编码纠错级别和掩码
        let mut format_data = match ec_level {
            ErrorCorrectionLevel::L => 0b01,
            ErrorCorrectionLevel::M => 0b00,
            ErrorCorrectionLevel::Q => 0b11,
            ErrorCorrectionLevel::H => 0b10,
        };
        
        // 添加掩码模式（使用掩码 0）
        format_data = (format_data << 3) | 0b000;
        
        // 计算 BCH 纠错码
        let format_with_ec = Self::calculate_format_ec(format_data);
        
        // 放置格式信息
        let format_bits = Self::to_bits(format_with_ec, 15);
        
        // 水平格式信息（左上到右上）
        for (i, &bit) in format_bits.iter().enumerate() {
            if i < 6 {
                matrix[8][i] = bit;
            } else if i < 8 {
                matrix[8][i + 1] = bit;
            } else {
                matrix[8][size - 15 + i] = bit;
            }
        }
        
        // 垂直格式信息（左上到左下）
        for (i, &bit) in format_bits.iter().enumerate() {
            if i < 8 {
                matrix[size - 1 - i][8] = bit;
            } else {
                matrix[14 - i][8] = bit;
            }
        }
    }
    
    /// 计算格式信息纠错码
    fn calculate_format_ec(data: u16) -> u16 {
        let mut data = data << 10; // 左移 10 位
        
        // BCH(15,5) 多项式：x^10 + x^8 + x^5 + x^4 + x^2 + x + 1
        let generator: u16 = 0b10100110111;
        
        for i in (0..5).rev() {
            if (data >> (10 + i)) & 1 == 1 {
                data ^= generator << i;
            }
        }
        
        data | (1 << 14) // 设置最高位
    }
    
    /// 将整数转换为位数组
    fn to_bits(value: u16, bits: usize) -> Vec<bool> {
        (0..bits).rev().map(|i| (value >> i) & 1 == 1).collect()
    }
    
    /// 应用掩码
    fn apply_mask(matrix: &mut [Vec<bool>], size: usize) {
        // 使用掩码模式 0：(x + y) % 2 == 0
        for y in 0..size {
            for x in 0..size {
                // 只对数据区域应用掩码
                if !Self::is_reserved(matrix, x, y, size) {
                    if (x + y) % 2 == 0 {
                        matrix[y][x] = !matrix[y][x];
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_build_matrix() {
        let data = vec![0x40, 0xD5, 0x6C, 0x61, 0x72, 0x67, 0x65];
        let matrix = MatrixBuilder::build(&data, 1, 21, ErrorCorrectionLevel::M);
        
        // 检查尺寸
        assert_eq!(matrix.len(), 21);
        assert_eq!(matrix[0].len(), 21);
        
        // 检查定位图案（左上角应该是黑色）
        assert!(matrix[0][0]);
        assert!(matrix[6][6]);
    }

    #[test]
    fn test_finder_patterns() {
        let mut matrix = vec![vec![false; 21]; 21];
        MatrixBuilder::add_finder_patterns(&mut matrix, 21);
        
        // 检查左上角定位图案
        assert!(matrix[0][0]);
        assert!(matrix[0][6]);
        assert!(matrix[6][0]);
        assert!(matrix[3][3]); // 中心
    }

    #[test]
    fn test_timing_patterns() {
        let mut matrix = vec![vec![false; 21]; 21];
        MatrixBuilder::add_timing_patterns(&mut matrix, 21);
        
        // 时序图案应该是交替的黑白色
        assert!(matrix[6][8]); // 位置 8 应该是黑色（从位置 0 开始计数）
        assert!(!matrix[6][9]); // 位置 9 应该是白色
    }

    #[test]
    fn test_format_ec() {
        let ec = MatrixBuilder::calculate_format_ec(0b00000);
        assert!(ec > 0);
    }
}