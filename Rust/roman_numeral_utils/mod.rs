//! 罗马数字工具库 - 零外部依赖
//!
//! 提供完整的罗马数字转换和计算功能
//! 支持阿拉伯数字与罗马数字的相互转换、验证和算术运算

use std::fmt;

/// 罗马数字基本符号
const ROMAN_SYMBOLS: &[(u32, &str)] = &[
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
];

/// 罗马数字解析错误类型
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RomanError {
    /// 无效的罗马数字字符
    InvalidCharacter(char),
    /// 无效的罗马数字格式
    InvalidFormat(String),
    /// 数字超出范围
    OutOfRange(u32),
    /// 空字符串
    EmptyInput,
    /// 重复次数过多
    TooManyRepeats(char),
    /// 非法的减法组合
    IllegalSubtraction(String),
}

impl fmt::Display for RomanError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RomanError::InvalidCharacter(c) => write!(f, "无效的罗马数字字符: '{}'", c),
            RomanError::InvalidFormat(s) => write!(f, "无效的罗马数字格式: '{}'", s),
            RomanError::OutOfRange(n) => write!(f, "数字 {} 超出可表示范围 (1-3999)", n),
            RomanError::EmptyInput => write!(f, "输入不能为空"),
            RomanError::TooManyRepeats(c) => write!(f, "字符 '{}' 重复次数过多", c),
            RomanError::IllegalSubtraction(s) => write!(f, "非法的减法组合: '{}'", s),
        }
    }
}

impl std::error::Error for RomanError {}

/// 罗马数字转换器
pub struct RomanNumeral;

impl RomanNumeral {
    /// 将阿拉伯数字转换为罗马数字
    ///
    /// # 参数
    /// - `num`: 要转换的阿拉伯数字 (1-3999)
    ///
    /// # 返回
    /// 罗马数字字符串
    ///
    /// # 错误
    /// 如果数字超出范围，返回 OutOfRange 错误
    ///
    /// # 示例
    /// ```
    /// use roman_numeral_utils::RomanNumeral;
    ///
    /// assert_eq!(RomanNumeral::from_arabic(1), Ok("I".to_string()));
    /// assert_eq!(RomanNumeral::from_arabic(4), Ok("IV".to_string()));
    /// assert_eq!(RomanNumeral::from_arabic(1994), Ok("MCMXCIV".to_string()));
    /// ```
    pub fn from_arabic(num: u32) -> Result<String, RomanError> {
        if num == 0 {
            return Err(RomanError::OutOfRange(0));
        }
        if num > 3999 {
            return Err(RomanError::OutOfRange(num));
        }

        let mut result = String::new();
        let mut remaining = num;

        for &(value, symbol) in ROMAN_SYMBOLS {
            while remaining >= value {
                result.push_str(symbol);
                remaining -= value;
            }
        }

        Ok(result)
    }

    /// 将罗马数字转换为阿拉伯数字
    ///
    /// # 参数
    /// - `roman`: 罗马数字字符串
    ///
    /// # 返回
    /// 对应的阿拉伯数字
    ///
    /// # 错误
    /// 如果输入无效，返回相应的 RomanError
    ///
    /// # 示例
    /// ```
    /// use roman_numeral_utils::RomanNumeral;
    ///
    /// assert_eq!(RomanNumeral::to_arabic("I"), Ok(1));
    /// assert_eq!(RomanNumeral::to_arabic("IV"), Ok(4));
    /// assert_eq!(RomanNumeral::to_arabic("MCMXCIV"), Ok(1994));
    /// ```
    pub fn to_arabic(roman: &str) -> Result<u32, RomanError> {
        if roman.is_empty() {
            return Err(RomanError::EmptyInput);
        }

        // 首先验证格式
        Self::validate(roman)?;

        let roman = roman.to_uppercase();
        let mut total: u32 = 0;
        let mut prev_value: u32 = 0;

        for c in roman.chars().rev() {
            let value = Self::char_to_value(c)?;

            if value < prev_value {
                total -= value;
            } else {
                total += value;
            }
            prev_value = value;
        }

        Ok(total)
    }

    /// 验证罗马数字是否有效
    ///
    /// # 参数
    /// - `roman`: 要验证的罗马数字字符串
    ///
    /// # 返回
    /// 如果有效返回 Ok(())，否则返回相应的错误
    pub fn validate(roman: &str) -> Result<(), RomanError> {
        if roman.is_empty() {
            return Err(RomanError::EmptyInput);
        }

        let roman = roman.to_uppercase();
        let chars: Vec<char> = roman.chars().collect();

        // 检查无效字符
        for &c in &chars {
            if !Self::is_valid_roman_char(c) {
                return Err(RomanError::InvalidCharacter(c));
            }
        }

        // 检查重复规则
        // I, X, C, M 可以重复最多3次
        // V, L, D 不能重复
        let repeatable = ['I', 'X', 'C', 'M'];
        let non_repeatable = ['V', 'L', 'D'];

        let mut i = 0;
        while i < chars.len() {
            let c = chars[i];

            if non_repeatable.contains(&c) {
                let count = Self::count_consecutive(&chars, i);
                if count > 1 {
                    return Err(RomanError::TooManyRepeats(c));
                }
            }

            if repeatable.contains(&c) {
                let count = Self::count_consecutive(&chars, i);
                if count > 3 {
                    return Err(RomanError::TooManyRepeats(c));
                }
            }

            i += Self::count_consecutive(&chars, i);
        }

        // 检查减法规则
        for i in 0..chars.len().saturating_sub(1) {
            let current = chars[i];
            let next = chars[i + 1];

            let curr_val = Self::char_to_value(current)?;
            let next_val = Self::char_to_value(next)?;

            if curr_val < next_val {
                match current {
                    'I' => {
                        if next != 'V' && next != 'X' {
                            return Err(RomanError::IllegalSubtraction(format!("{}{}", current, next)));
                        }
                    }
                    'X' => {
                        if next != 'L' && next != 'C' {
                            return Err(RomanError::IllegalSubtraction(format!("{}{}", current, next)));
                        }
                    }
                    'C' => {
                        if next != 'D' && next != 'M' {
                            return Err(RomanError::IllegalSubtraction(format!("{}{}", current, next)));
                        }
                    }
                    _ => {
                        return Err(RomanError::IllegalSubtraction(format!("{}{}", current, next)));
                    }
                }
            }
        }

        Ok(())
    }

    /// 检查字符串是否是有效的罗马数字
    pub fn is_valid(roman: &str) -> bool {
        Self::validate(roman).is_ok()
    }

    /// 将罗马数字字符转换为其数值
    fn char_to_value(c: char) -> Result<u32, RomanError> {
        match c {
            'I' => Ok(1),
            'V' => Ok(5),
            'X' => Ok(10),
            'L' => Ok(50),
            'C' => Ok(100),
            'D' => Ok(500),
            'M' => Ok(1000),
            _ => Err(RomanError::InvalidCharacter(c)),
        }
    }

    /// 检查字符是否是有效的罗马数字字符
    fn is_valid_roman_char(c: char) -> bool {
        matches!(c, 'I' | 'V' | 'X' | 'L' | 'C' | 'D' | 'M')
    }

    /// 计算从指定位置开始连续相同字符的数量
    fn count_consecutive(chars: &[char], start: usize) -> usize {
        if start >= chars.len() {
            return 0;
        }
        let target = chars[start];
        chars[start..].iter().take_while(|&&c| c == target).count()
    }
}

/// 罗马数字算术运算器
pub struct RomanArithmetic;

impl RomanArithmetic {
    /// 加法
    pub fn add(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;
        RomanNumeral::from_arabic(num_a + num_b)
    }

    /// 减法
    pub fn subtract(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;

        if num_a <= num_b {
            return Err(RomanError::OutOfRange(0));
        }

        RomanNumeral::from_arabic(num_a - num_b)
    }

    /// 乘法
    pub fn multiply(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;
        RomanNumeral::from_arabic(num_a * num_b)
    }

    /// 整数除法
    pub fn divide(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;

        if num_b == 0 {
            return Err(RomanError::OutOfRange(0));
        }

        RomanNumeral::from_arabic(num_a / num_b)
    }

    /// 取模
    pub fn modulo(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;

        if num_b == 0 {
            return Err(RomanError::OutOfRange(0));
        }

        RomanNumeral::from_arabic(num_a % num_b)
    }

    /// 比较两个罗马数字
    pub fn compare(a: &str, b: &str) -> Result<std::cmp::Ordering, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;
        Ok(num_a.cmp(&num_b))
    }

    /// 找出较大的数
    pub fn max(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;
        RomanNumeral::from_arabic(num_a.max(num_b))
    }

    /// 找出较小的数
    pub fn min(a: &str, b: &str) -> Result<String, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;
        RomanNumeral::from_arabic(num_a.min(num_b))
    }

    /// 幂运算
    pub fn power(base: &str, exp: u32) -> Result<String, RomanError> {
        let num = RomanNumeral::to_arabic(base)?;
        RomanNumeral::from_arabic(num.pow(exp))
    }
}

/// 罗马数字格式化选项
#[derive(Debug, Clone)]
pub struct RomanFormatOptions {
    /// 使用小写
    pub lowercase: bool,
}

impl Default for RomanFormatOptions {
    fn default() -> Self {
        RomanFormatOptions {
            lowercase: false,
        }
    }
}

impl RomanFormatOptions {
    /// 创建新的格式化选项
    pub fn new() -> Self {
        Self::default()
    }

    /// 设置为小写
    pub fn lowercase(mut self) -> Self {
        self.lowercase = true;
        self
    }

    /// 格式化罗马数字
    pub fn format(&self, num: u32) -> Result<String, RomanError> {
        let mut roman = RomanNumeral::from_arabic(num)?;

        if self.lowercase {
            roman = roman.to_lowercase();
        }

        Ok(roman)
    }
}

/// 常见罗马数字常量
pub mod constants {
    /// 1
    pub const I: &str = "I";
    /// 2
    pub const II: &str = "II";
    /// 3
    pub const III: &str = "III";
    /// 4
    pub const IV: &str = "IV";
    /// 5
    pub const V: &str = "V";
    /// 6
    pub const VI: &str = "VI";
    /// 7
    pub const VII: &str = "VII";
    /// 8
    pub const VIII: &str = "VIII";
    /// 9
    pub const IX: &str = "IX";
    /// 10
    pub const X: &str = "X";
    /// 20
    pub const XX: &str = "XX";
    /// 30
    pub const XXX: &str = "XXX";
    /// 40
    pub const XL: &str = "XL";
    /// 50
    pub const L: &str = "L";
    /// 60
    pub const LX: &str = "LX";
    /// 70
    pub const LXX: &str = "LXX";
    /// 80
    pub const LXXX: &str = "LXXX";
    /// 90
    pub const XC: &str = "XC";
    /// 100
    pub const C: &str = "C";
    /// 200
    pub const CC: &str = "CC";
    /// 300
    pub const CCC: &str = "CCC";
    /// 400
    pub const CD: &str = "CD";
    /// 500
    pub const D: &str = "D";
    /// 600
    pub const DC: &str = "DC";
    /// 700
    pub const DCC: &str = "DCC";
    /// 800
    pub const DCCC: &str = "DCCC";
    /// 900
    pub const CM: &str = "CM";
    /// 1000
    pub const M: &str = "M";
    /// 1984
    pub const MCMLXXXIV: &str = "MCMLXXXIV";
    /// 2024
    pub const MMXXIV: &str = "MMXXIV";
    /// 3999
    pub const MMMCMXCIX: &str = "MMMCMXCIX";
}

/// 罗马数字年份转换器
pub struct RomanYear;

impl RomanYear {
    /// 将公元年份转换为罗马数字
    pub fn from_year(year: u32) -> Result<String, RomanError> {
        RomanNumeral::from_arabic(year)
    }

    /// 将罗马数字转换为公元年份
    pub fn to_year(roman: &str) -> Result<u32, RomanError> {
        RomanNumeral::to_arabic(roman)
    }

    /// 获取当前年份的罗马数字表示
    pub fn current_year() -> Result<String, RomanError> {
        // 2024年
        RomanNumeral::from_arabic(2024)
    }

    /// 判断是否是闰年
    pub fn is_leap_year(year: u32) -> bool {
        (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
    }

    /// 将闰年转换为罗马数字并标注
    pub fn leap_year_to_roman(year: u32) -> Result<String, RomanError> {
        let roman = RomanNumeral::from_arabic(year)?;
        if Self::is_leap_year(year) {
            Ok(format!("{} (闰年)", roman))
        } else {
            Ok(roman)
        }
    }
}

/// 序数词转换器
pub struct RomanOrdinal;

impl RomanOrdinal {
    /// 将数字转换为罗马序数词
    /// 在罗马数字后添加后缀表示序数
    pub fn from_number(num: u32) -> Result<String, RomanError> {
        let roman = RomanNumeral::from_arabic(num)?;
        Ok(format!("{}°", roman))
    }

    /// 从罗马序数词解析数字
    pub fn to_number(ordinal: &str) -> Result<u32, RomanError> {
        // 移除序数标记
        let roman = ordinal.trim_end_matches('°')
            .trim_end_matches("st")
            .trim_end_matches("nd")
            .trim_end_matches("rd")
            .trim_end_matches("th");
        RomanNumeral::to_arabic(roman)
    }
}

/// 预定义的历史年份
pub mod historical_years {
    use super::RomanNumeral;

    /// 罗马帝国灭亡（公元476年）
    pub const ROMAN_EMPIRE_FALL: &str = "CDLXXVI";
    /// 发现美洲（1492年）
    pub const AMERICA_DISCOVERY: &str = "MCDXCII";
    /// 法国大革命（1789年）
    pub const FRENCH_REVOLUTION: &str = "MDCCLXXXIX";
    /// 美国独立（1776年）
    pub const US_INDEPENDENCE: &str = "MDCCLXXVI";
    /// 中国人民共和国成立（1949年）
    pub const PRC_FOUNDING: &str = "MCMXLIX";
    /// 千禧年（2000年）
    pub const MILLENNIUM: &str = "MM";

    /// 生成指定年份的罗马数字
    pub fn year_to_roman(year: u32) -> String {
        RomanNumeral::from_arabic(year).unwrap_or_default()
    }
}

/// 罗马数字迭代器 - 生成从指定数开始的罗马数字序列
pub struct RomanIterator {
    current: u32,
    end: u32,
}

impl RomanIterator {
    /// 创建新的迭代器
    pub fn new(start: u32, end: u32) -> Self {
        RomanIterator { current: start, end }
    }

    /// 创建无限迭代器
    pub fn infinite(start: u32) -> Self {
        RomanIterator { current: start, end: 3999 }
    }
}

impl Iterator for RomanIterator {
    type Item = Result<String, RomanError>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current > self.end || self.current > 3999 {
            return None;
        }

        let result = RomanNumeral::from_arabic(self.current);
        self.current += 1;
        Some(result)
    }
}

/// 罗马数字工具函数集合
pub struct RomanUtils;

impl RomanUtils {
    /// 批量转换多个数字
    pub fn from_arabic_batch(nums: &[u32]) -> Vec<Result<String, RomanError>> {
        nums.iter().map(|&n| RomanNumeral::from_arabic(n)).collect()
    }

    /// 批量转换多个罗马数字
    pub fn to_arabic_batch(romans: &[&str]) -> Vec<Result<u32, RomanError>> {
        romans.iter().map(|&r| RomanNumeral::to_arabic(r)).collect()
    }

    /// 找出列表中最大的罗马数字
    pub fn max_in_list(romans: &[&str]) -> Result<String, RomanError> {
        romans.iter()
            .map(|&r| RomanNumeral::to_arabic(r))
            .collect::<Result<Vec<_>, _>>()
            .map(|nums| nums.iter().max().copied().unwrap_or(0))
            .and_then(|max| RomanNumeral::from_arabic(max))
    }

    /// 找出列表中最小的罗马数字
    pub fn min_in_list(romans: &[&str]) -> Result<String, RomanError> {
        romans.iter()
            .map(|&r| RomanNumeral::to_arabic(r))
            .collect::<Result<Vec<_>, _>>()
            .map(|nums| nums.iter().min().copied().unwrap_or(0))
            .and_then(|min| RomanNumeral::from_arabic(min))
    }

    /// 计算罗马数字列表的总和
    pub fn sum(romans: &[&str]) -> Result<String, RomanError> {
        let total: u32 = romans.iter()
            .map(|&r| RomanNumeral::to_arabic(r))
            .collect::<Result<Vec<_>, _>>()?
            .iter()
            .sum();
        RomanNumeral::from_arabic(total)
    }

    /// 计算罗马数字列表的平均值
    pub fn average(romans: &[&str]) -> Result<f64, RomanError> {
        let nums: Vec<u32> = romans.iter()
            .map(|&r| RomanNumeral::to_arabic(r))
            .collect::<Result<Vec<_>, _>>()?;

        if nums.is_empty() {
            return Ok(0.0);
        }

        let total: u32 = nums.iter().sum();
        Ok(total as f64 / nums.len() as f64)
    }

    /// 生成罗马数字乘法表
    pub fn multiplication_table(size: u32) -> Vec<Vec<Result<String, RomanError>>> {
        (1..=size)
            .map(|i| {
                (1..=size)
                    .map(|j| RomanNumeral::from_arabic(i * j))
                    .collect()
            })
            .collect()
    }

    /// 检查两个罗马数字是否相等
    pub fn equals(a: &str, b: &str) -> Result<bool, RomanError> {
        let num_a = RomanNumeral::to_arabic(a)?;
        let num_b = RomanNumeral::to_arabic(b)?;
        Ok(num_a == num_b)
    }

    /// 将罗马数字格式化为带下划线的形式（用于表示大数）
    pub fn format_with_underscore(num: u32) -> Result<String, RomanError> {
        let roman = RomanNumeral::from_arabic(num)?;
        Ok(roman.chars().map(|c| c.to_string()).collect::<Vec<_>>().join("_"))
    }

    /// 解析可能包含分隔符的罗马数字
    pub fn parse_flexible(input: &str) -> Result<u32, RomanError> {
        let cleaned: String = input.chars()
            .filter(|c| !matches!(c, ' ' | '_' | '-' | '.'))
            .collect();
        RomanNumeral::to_arabic(&cleaned)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_from_arabic_basic() {
        assert_eq!(RomanNumeral::from_arabic(1), Ok("I".to_string()));
        assert_eq!(RomanNumeral::from_arabic(2), Ok("II".to_string()));
        assert_eq!(RomanNumeral::from_arabic(3), Ok("III".to_string()));
        assert_eq!(RomanNumeral::from_arabic(4), Ok("IV".to_string()));
        assert_eq!(RomanNumeral::from_arabic(5), Ok("V".to_string()));
        assert_eq!(RomanNumeral::from_arabic(6), Ok("VI".to_string()));
        assert_eq!(RomanNumeral::from_arabic(9), Ok("IX".to_string()));
        assert_eq!(RomanNumeral::from_arabic(10), Ok("X".to_string()));
    }

    #[test]
    fn test_from_arabic_complex() {
        assert_eq!(RomanNumeral::from_arabic(49), Ok("XLIX".to_string()));
        assert_eq!(RomanNumeral::from_arabic(99), Ok("XCIX".to_string()));
        assert_eq!(RomanNumeral::from_arabic(1994), Ok("MCMXCIV".to_string()));
        assert_eq!(RomanNumeral::from_arabic(2024), Ok("MMXXIV".to_string()));
        assert_eq!(RomanNumeral::from_arabic(3999), Ok("MMMCMXCIX".to_string()));
    }

    #[test]
    fn test_from_arabic_edge_cases() {
        assert!(matches!(RomanNumeral::from_arabic(0), Err(RomanError::OutOfRange(_))));
        assert!(matches!(RomanNumeral::from_arabic(4000), Err(RomanError::OutOfRange(_))));
    }

    #[test]
    fn test_to_arabic_basic() {
        assert_eq!(RomanNumeral::to_arabic("I"), Ok(1));
        assert_eq!(RomanNumeral::to_arabic("II"), Ok(2));
        assert_eq!(RomanNumeral::to_arabic("III"), Ok(3));
        assert_eq!(RomanNumeral::to_arabic("IV"), Ok(4));
        assert_eq!(RomanNumeral::to_arabic("V"), Ok(5));
        assert_eq!(RomanNumeral::to_arabic("VI"), Ok(6));
        assert_eq!(RomanNumeral::to_arabic("IX"), Ok(9));
        assert_eq!(RomanNumeral::to_arabic("X"), Ok(10));
    }

    #[test]
    fn test_to_arabic_complex() {
        assert_eq!(RomanNumeral::to_arabic("XLIX"), Ok(49));
        assert_eq!(RomanNumeral::to_arabic("XCIX"), Ok(99));
        assert_eq!(RomanNumeral::to_arabic("MCMXCIV"), Ok(1994));
        assert_eq!(RomanNumeral::to_arabic("MMXXIV"), Ok(2024));
        assert_eq!(RomanNumeral::to_arabic("MMMCMXCIX"), Ok(3999));
    }

    #[test]
    fn test_to_arabic_case_insensitive() {
        assert_eq!(RomanNumeral::to_arabic("mcmxciv"), Ok(1994));
        assert_eq!(RomanNumeral::to_arabic("MmXxIv"), Ok(2024));
    }

    #[test]
    fn test_to_arabic_errors() {
        assert!(matches!(RomanNumeral::to_arabic(""), Err(RomanError::EmptyInput)));
        assert!(matches!(RomanNumeral::to_arabic("ABC"), Err(RomanError::InvalidCharacter('A'))));
        assert!(matches!(RomanNumeral::to_arabic("IIII"), Err(RomanError::TooManyRepeats('I'))));
        assert!(matches!(RomanNumeral::to_arabic("VV"), Err(RomanError::TooManyRepeats('V'))));
        assert!(matches!(RomanNumeral::to_arabic("IC"), Err(RomanError::IllegalSubtraction(_))));
    }

    #[test]
    fn test_roundtrip() {
        for num in [1, 4, 9, 27, 49, 99, 123, 456, 789, 1000, 1994, 2024, 3999] {
            let roman = RomanNumeral::from_arabic(num).unwrap();
            let back = RomanNumeral::to_arabic(&roman).unwrap();
            assert_eq!(num, back, "Roundtrip failed for {}", num);
        }
    }

    #[test]
    fn test_validate() {
        assert!(RomanNumeral::is_valid("I"));
        assert!(RomanNumeral::is_valid("IV"));
        assert!(RomanNumeral::is_valid("MCMXCIV"));
        assert!(!RomanNumeral::is_valid(""));
        assert!(!RomanNumeral::is_valid("IIII"));
        assert!(!RomanNumeral::is_valid("VV"));
        assert!(!RomanNumeral::is_valid("IC"));
    }

    #[test]
    fn test_arithmetic_add() {
        assert_eq!(RomanArithmetic::add("I", "I"), Ok("II".to_string()));
        assert_eq!(RomanArithmetic::add("IV", "VI"), Ok("X".to_string()));
        assert_eq!(RomanArithmetic::add("X", "XC"), Ok("C".to_string()));
        assert_eq!(RomanArithmetic::add("M", "M"), Ok("MM".to_string()));
    }

    #[test]
    fn test_arithmetic_subtract() {
        assert_eq!(RomanArithmetic::subtract("V", "I"), Ok("IV".to_string()));
        assert_eq!(RomanArithmetic::subtract("X", "IV"), Ok("VI".to_string()));
        assert_eq!(RomanArithmetic::subtract("C", "X"), Ok("XC".to_string()));
        assert!(RomanArithmetic::subtract("I", "I").is_err());
        assert!(RomanArithmetic::subtract("I", "V").is_err());
    }

    #[test]
    fn test_arithmetic_multiply() {
        assert_eq!(RomanArithmetic::multiply("II", "III"), Ok("VI".to_string()));
        assert_eq!(RomanArithmetic::multiply("V", "V"), Ok("XXV".to_string()));
        assert_eq!(RomanArithmetic::multiply("X", "X"), Ok("C".to_string()));
    }

    #[test]
    fn test_arithmetic_divide() {
        assert_eq!(RomanArithmetic::divide("X", "II"), Ok("V".to_string()));
        assert_eq!(RomanArithmetic::divide("C", "X"), Ok("X".to_string()));
        assert_eq!(RomanArithmetic::divide("V", "II"), Ok("II".to_string()));
    }

    #[test]
    fn test_arithmetic_modulo() {
        assert_eq!(RomanArithmetic::modulo("VII", "III"), Ok("I".to_string()));
        assert_eq!(RomanArithmetic::modulo("X", "III"), Ok("I".to_string()));
    }

    #[test]
    fn test_arithmetic_compare() {
        use std::cmp::Ordering;
        assert_eq!(RomanArithmetic::compare("I", "II"), Ok(Ordering::Less));
        assert_eq!(RomanArithmetic::compare("V", "V"), Ok(Ordering::Equal));
        assert_eq!(RomanArithmetic::compare("X", "V"), Ok(Ordering::Greater));
    }

    #[test]
    fn test_arithmetic_max_min() {
        assert_eq!(RomanArithmetic::max("V", "X"), Ok("X".to_string()));
        assert_eq!(RomanArithmetic::max("M", "C"), Ok("M".to_string()));
        assert_eq!(RomanArithmetic::min("V", "X"), Ok("V".to_string()));
        assert_eq!(RomanArithmetic::min("M", "C"), Ok("C".to_string()));
    }

    #[test]
    fn test_arithmetic_power() {
        assert_eq!(RomanArithmetic::power("II", 2), Ok("IV".to_string()));
        assert_eq!(RomanArithmetic::power("V", 2), Ok("XXV".to_string()));
        assert_eq!(RomanArithmetic::power("X", 3), Ok("M".to_string()));
    }

    #[test]
    fn test_format_options() {
        let options = RomanFormatOptions::new().lowercase();
        assert_eq!(options.format(1994).unwrap(), "mcmxciv");
        assert_eq!(options.format(2024).unwrap(), "mmxxiv");
    }

    #[test]
    fn test_roman_year() {
        assert_eq!(RomanYear::from_year(2024), Ok("MMXXIV".to_string()));
        assert_eq!(RomanYear::to_year("MCMXCIV"), Ok(1994));
        assert!(RomanYear::is_leap_year(2024));
        assert!(!RomanYear::is_leap_year(2023));
        assert!(RomanYear::is_leap_year(2000));
        assert!(!RomanYear::is_leap_year(1900));
    }

    #[test]
    fn test_roman_ordinal() {
        assert_eq!(RomanOrdinal::from_number(1), Ok("I°".to_string()));
        assert_eq!(RomanOrdinal::from_number(10), Ok("X°".to_string()));
        assert_eq!(RomanOrdinal::to_number("X°"), Ok(10));
        assert_eq!(RomanOrdinal::to_number("Vth"), Ok(5));
    }

    #[test]
    fn test_constants() {
        assert_eq!(constants::I, "I");
        assert_eq!(constants::V, "V");
        assert_eq!(constants::X, "X");
        assert_eq!(constants::L, "L");
        assert_eq!(constants::C, "C");
        assert_eq!(constants::D, "D");
        assert_eq!(constants::M, "M");
        assert_eq!(constants::MMMCMXCIX, "MMMCMXCIX");
        assert_eq!(constants::MMXXIV, "MMXXIV");
    }

    #[test]
    fn test_historical_years() {
        assert_eq!(historical_years::AMERICA_DISCOVERY, "MCDXCII");
        assert_eq!(historical_years::US_INDEPENDENCE, "MDCCLXXVI");
        assert_eq!(historical_years::PRC_FOUNDING, "MCMXLIX");
        assert_eq!(historical_years::MILLENNIUM, "MM");
    }

    #[test]
    fn test_roman_iterator() {
        let mut iter = RomanIterator::new(1, 5);
        assert_eq!(iter.next(), Some(Ok("I".to_string())));
        assert_eq!(iter.next(), Some(Ok("II".to_string())));
        assert_eq!(iter.next(), Some(Ok("III".to_string())));
        assert_eq!(iter.next(), Some(Ok("IV".to_string())));
        assert_eq!(iter.next(), Some(Ok("V".to_string())));
        assert_eq!(iter.next(), None);
    }

    #[test]
    fn test_roman_utils_batch() {
        let results = RomanUtils::from_arabic_batch(&[1, 2, 3, 4, 5]);
        assert_eq!(results.len(), 5);
        assert_eq!(results[0], Ok("I".to_string()));
        assert_eq!(results[4], Ok("V".to_string()));

        let nums = RomanUtils::to_arabic_batch(&["I", "II", "III"]);
        assert_eq!(nums.len(), 3);
        assert_eq!(nums[0], Ok(1));
        assert_eq!(nums[2], Ok(3));
    }

    #[test]
    fn test_roman_utils_aggregates() {
        assert_eq!(RomanUtils::sum(&["I", "II", "III"]), Ok("VI".to_string()));
        assert_eq!(RomanUtils::max_in_list(&["I", "V", "X"]), Ok("X".to_string()));
        assert_eq!(RomanUtils::min_in_list(&["I", "V", "X"]), Ok("I".to_string()));

        let avg = RomanUtils::average(&["II", "IV", "VI"]).unwrap();
        assert!((avg - 4.0).abs() < 0.001);
    }

    #[test]
    fn test_roman_utils_multiplication_table() {
        let table = RomanUtils::multiplication_table(3);
        assert_eq!(table.len(), 3);
        assert_eq!(table[0][0], Ok("I".to_string()));
        assert_eq!(table[1][1], Ok("IV".to_string()));
        assert_eq!(table[2][2], Ok("IX".to_string()));
    }

    #[test]
    fn test_roman_utils_equals() {
        assert!(RomanUtils::equals("V", "V").unwrap());
        assert!(!RomanUtils::equals("V", "X").unwrap());
    }

    #[test]
    fn test_roman_utils_flexible_parse() {
        assert_eq!(RomanUtils::parse_flexible("MCMXCIV"), Ok(1994));
        assert_eq!(RomanUtils::parse_flexible("M CM XC IV"), Ok(1994));
        assert_eq!(RomanUtils::parse_flexible("M-CM-XC-IV"), Ok(1994));
        assert_eq!(RomanUtils::parse_flexible("M_CM_XC_IV"), Ok(1994));
    }

    #[test]
    fn test_all_basic_combinations() {
        let test_cases = [
            (1, "I"), (2, "II"), (3, "III"), (4, "IV"), (5, "V"),
            (6, "VI"), (7, "VII"), (8, "VIII"), (9, "IX"), (10, "X"),
            (11, "XI"), (14, "XIV"), (15, "XV"), (19, "XIX"), (20, "XX"),
            (40, "XL"), (50, "L"), (90, "XC"), (100, "C"),
            (400, "CD"), (500, "D"), (900, "CM"), (1000, "M"),
        ];

        for (num, expected) in test_cases {
            let result = RomanNumeral::from_arabic(num).unwrap();
            assert_eq!(result, expected, "Failed for {}", num);
        }
    }

    #[test]
    fn test_error_display() {
        let err = RomanError::InvalidCharacter('A');
        assert!(err.to_string().contains("A"));

        let err = RomanError::OutOfRange(0);
        assert!(err.to_string().contains("0"));

        let err = RomanError::EmptyInput;
        assert!(err.to_string().contains("空"));
    }
}