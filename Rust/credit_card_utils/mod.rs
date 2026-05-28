//! 信用卡工具库 - 零外部依赖
//!
//! 提供信用卡号验证、卡类型识别、格式化等功能
//! 支持 Visa、MasterCard、American Express、Discover、JCB、Diners Club 等主流卡品牌

use std::fmt;

/// 信用卡品牌类型
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CardBrand {
    /// Visa
    Visa,
    /// MasterCard
    MasterCard,
    /// American Express
    Amex,
    /// Discover
    Discover,
    /// JCB
    Jcb,
    /// Diners Club
    DinersClub,
    /// UnionPay (银联)
    UnionPay,
    /// Maestro
    Maestro,
    /// Elo
    Elo,
    /// Mir (俄罗斯)
    Mir,
    /// 未知品牌
    Unknown,
}

impl fmt::Display for CardBrand {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CardBrand::Visa => write!(f, "Visa"),
            CardBrand::MasterCard => write!(f, "MasterCard"),
            CardBrand::Amex => write!(f, "American Express"),
            CardBrand::Discover => write!(f, "Discover"),
            CardBrand::Jcb => write!(f, "JCB"),
            CardBrand::DinersClub => write!(f, "Diners Club"),
            CardBrand::UnionPay => write!(f, "UnionPay"),
            CardBrand::Maestro => write!(f, "Maestro"),
            CardBrand::Elo => write!(f, "Elo"),
            CardBrand::Mir => write!(f, "Mir"),
            CardBrand::Unknown => write!(f, "Unknown"),
        }
    }
}

/// 信用卡信息结构体
#[derive(Debug, Clone)]
pub struct CreditCard {
    /// 原始卡号
    number: String,
    /// 卡品牌
    brand: CardBrand,
    /// 是否有效（通过 Luhn 检查）
    valid: bool,
    /// 卡号长度
    length: usize,
}

impl CreditCard {
    /// 从字符串创建信用卡实例
    /// 自动去除空格和连字符
    pub fn new(number: &str) -> Self {
        let clean_number: String = number
            .chars()
            .filter(|c| c.is_ascii_digit())
            .collect();
        
        let length = clean_number.len();
        let brand = Self::detect_brand(&clean_number);
        let valid = Self::validate_luhn(&clean_number) && Self::validate_length(&clean_number, brand);
        
        CreditCard {
            number: clean_number,
            brand,
            valid,
            length,
        }
    }

    /// 检测信用卡品牌
    fn detect_brand(number: &str) -> CardBrand {
        let chars: Vec<char> = number.chars().collect();
        if chars.is_empty() {
            return CardBrand::Unknown;
        }

        // 获取前缀数字
        let prefix2: String = chars.iter().take(2).collect();
        let prefix3: String = chars.iter().take(3).collect();
        let prefix4: String = chars.iter().take(4).collect();
        let prefix6: String = chars.iter().take(6).collect();

        let prefix2_num: u32 = prefix2.parse().unwrap_or(0);
        let prefix3_num: u32 = prefix3.parse().unwrap_or(0);
        let prefix4_num: u32 = prefix4.parse().unwrap_or(0);
        let prefix6_num: u32 = prefix6.parse().unwrap_or(0);

        // Visa: 以 4 开头
        if chars[0] == '4' {
            return CardBrand::Visa;
        }

        // MasterCard: 51-55 或 2221-2720
        if (prefix2_num >= 51 && prefix2_num <= 55)
            || (prefix6_num >= 222100 && prefix6_num <= 272099)
        {
            return CardBrand::MasterCard;
        }

        // American Express: 34 或 37
        if prefix2_num == 34 || prefix2_num == 37 {
            return CardBrand::Amex;
        }

        // UnionPay: 62 (优先于 Discover，因为 Discover 的部分 BIN 与 UnionPay 重叠)
        if prefix2_num == 62 {
            // Discover 使用的 622126-622925 范围，其他 62 开头归 UnionPay
            if !(prefix6_num >= 622126 && prefix6_num <= 622925) {
                return CardBrand::UnionPay;
            }
        }

        // Discover: 6011, 622126-622925, 644-649, 65
        if prefix4_num == 6011
            || (prefix6_num >= 622126 && prefix6_num <= 622925)
            || (prefix3_num >= 644 && prefix3_num <= 649)
            || prefix2_num == 65
        {
            return CardBrand::Discover;
        }

        // JCB: 3528-3589
        if prefix4_num >= 3528 && prefix4_num <= 3589 {
            return CardBrand::Jcb;
        }

        // Diners Club: 300-305, 36, 38, 39
        if (prefix3_num >= 300 && prefix3_num <= 305)
            || prefix2_num == 36
            || prefix2_num == 38
            || prefix2_num == 39
        {
            return CardBrand::DinersClub;
        }

        // Maestro: 5018, 5020, 5038, 5893, 6304, 6759, 6761-6763
        if prefix4_num == 5018
            || prefix4_num == 5020
            || prefix4_num == 5038
            || prefix4_num == 5893
            || prefix4_num == 6304
            || prefix4_num == 6759
            || (prefix4_num >= 6761 && prefix4_num <= 6763)
        {
            return CardBrand::Maestro;
        }

        // Elo: 特定 BIN 范围
        let elo_bins = [
            401178, 401179, 438935, 457631, 457632, 504175, 506699, 506700,
            506701, 506702, 506703, 506704, 506705, 506706, 506707, 506708,
            506709, 506710, 506711, 506712, 506713, 506714, 506715, 506716,
            506717, 506718, 506719, 506720, 506721, 506722, 506723, 506724,
            506725, 506726, 506727, 506728, 506729, 506730, 506731, 506732,
            506733, 506734, 506735, 506736, 506737, 506738, 506739, 506740,
            506741, 506742, 506743, 506744, 506745, 506746, 506747, 506748,
            506749, 506750, 506751, 506752, 506753, 506754, 506755, 506756,
            506757, 506758, 506759, 506760, 506761, 506762, 506763, 506764,
            506765, 506766, 506767, 506768, 506769, 506770, 506771, 506772,
            506773, 506774, 506775, 506776, 506777, 506778, 506779, 506780,
            506781, 506782, 506783, 506784, 506785, 506786, 506787, 506788,
            506789, 506790, 506791, 506792, 506793, 506794, 506795, 506796,
            506797, 506798, 506799, 627780, 636297,
        ];
        if elo_bins.contains(&prefix6_num) {
            return CardBrand::Elo;
        }

        // Mir: 2200-2204
        if prefix4_num >= 2200 && prefix4_num <= 2204 {
            return CardBrand::Mir;
        }

        CardBrand::Unknown
    }

    /// Luhn 算法验证
    fn validate_luhn(number: &str) -> bool {
        let digits: Vec<u32> = number
            .chars()
            .filter_map(|c| c.to_digit(10))
            .collect();

        if digits.is_empty() {
            return false;
        }

        let sum: u32 = digits
            .iter()
            .rev()
            .enumerate()
            .map(|(i, &d)| {
                if i % 2 == 1 {
                    let doubled = d * 2;
                    if doubled > 9 {
                        doubled - 9
                    } else {
                        doubled
                    }
                } else {
                    d
                }
            })
            .sum();

        sum % 10 == 0
    }

    /// 验证卡号长度
    fn validate_length(number: &str, brand: CardBrand) -> bool {
        let len = number.len();
        match brand {
            CardBrand::Visa => len == 13 || len == 16 || len == 19,
            CardBrand::MasterCard => len == 16,
            CardBrand::Amex => len == 15,
            CardBrand::Discover => len >= 16 && len <= 19,
            CardBrand::Jcb => len == 16,
            CardBrand::DinersClub => len == 14,
            CardBrand::UnionPay => len >= 16 && len <= 19,
            CardBrand::Maestro => len >= 12 && len <= 19,
            CardBrand::Elo => len == 16,
            CardBrand::Mir => len == 16,
            CardBrand::Unknown => len >= 13 && len <= 19,
        }
    }

    /// 获取卡号（纯数字）
    pub fn number(&self) -> &str {
        &self.number
    }

    /// 获取卡品牌
    pub fn brand(&self) -> CardBrand {
        self.brand
    }

    /// 检查是否有效
    pub fn is_valid(&self) -> bool {
        self.valid
    }

    /// 获取卡号长度
    pub fn length(&self) -> usize {
        self.length
    }

    /// 格式化卡号（按品牌添加分隔符）
    pub fn format(&self) -> String {
        match self.brand {
            CardBrand::Visa | CardBrand::MasterCard | CardBrand::Discover | 
            CardBrand::Jcb | CardBrand::UnionPay | CardBrand::Elo | CardBrand::Mir => {
                // #### #### #### ####
                Self::format_chunks(&self.number, 4)
            }
            CardBrand::Amex => {
                // #### ###### #####
                if self.number.len() >= 4 {
                    let mut result = String::new();
                    result.push_str(&self.number[..4]);
                    if self.number.len() >= 10 {
                        result.push(' ');
                        result.push_str(&self.number[4..10]);
                        if self.number.len() >= 15 {
                            result.push(' ');
                            result.push_str(&self.number[10..15]);
                        } else if self.number.len() > 4 {
                            result.push(' ');
                            result.push_str(&self.number[4..]);
                        }
                    } else if self.number.len() > 4 {
                        result.push(' ');
                        result.push_str(&self.number[4..]);
                    }
                    result
                } else {
                    self.number.clone()
                }
            }
            CardBrand::DinersClub => {
                // #### ###### ####
                if self.number.len() >= 4 {
                    let mut result = String::new();
                    result.push_str(&self.number[..4]);
                    if self.number.len() >= 10 {
                        result.push(' ');
                        result.push_str(&self.number[4..10]);
                        if self.number.len() >= 14 {
                            result.push(' ');
                            result.push_str(&self.number[10..14]);
                        } else if self.number.len() > 10 {
                            result.push(' ');
                            result.push_str(&self.number[10..]);
                        }
                    } else if self.number.len() > 4 {
                        result.push(' ');
                        result.push_str(&self.number[4..]);
                    }
                    result
                } else {
                    self.number.clone()
                }
            }
            CardBrand::Maestro | CardBrand::Unknown => {
                Self::format_chunks(&self.number, 4)
            }
        }
    }

    /// 通用格式化（每 n 位一组）
    fn format_chunks(number: &str, chunk_size: usize) -> String {
        number
            .as_bytes()
            .chunks(chunk_size)
            .map(|chunk| std::str::from_utf8(chunk).unwrap_or(""))
            .collect::<Vec<_>>()
            .join(" ")
    }

    /// 获取掩码卡号（只显示后 4 位）
    pub fn mask_last4(&self) -> String {
        if self.number.len() >= 4 {
            let last4 = &self.number[self.number.len() - 4..];
            let mask_len = self.number.len() - 4;
            format!("{}{}", "*".repeat(mask_len), last4)
        } else {
            "*".repeat(self.number.len())
        }
    }

    /// 获取掩码卡号（只显示前 4 位和后 4 位）
    pub fn mask_middle(&self) -> String {
        if self.number.len() >= 8 {
            let first4 = &self.number[..4];
            let last4 = &self.number[self.number.len() - 4..];
            let mask_len = self.number.len() - 8;
            format!("{}{}{}", first4, "*".repeat(mask_len), last4)
        } else {
            self.mask_last4()
        }
    }

    /// 获取银行卡识别码 (BIN/IIN - 前 6 位)
    pub fn bin(&self) -> Option<&str> {
        if self.number.len() >= 6 {
            Some(&self.number[..6])
        } else {
            None
        }
    }

    /// 检查是否为测试卡号
    pub fn is_test_card(&self) -> bool {
        let test_numbers = [
            "4111111111111111", // Visa 测试卡
            "4012888888881881", // Visa 测试卡
            "4222222222222",    // Visa 测试卡
            "5555555555554444", // MasterCard 测试卡
            "5105105105105100", // MasterCard 测试卡
            "378282246310005",  // Amex 测试卡
            "371449635398431",  // Amex 测试卡
            "6011111111111117", // Discover 测试卡
            "6011000990139424", // Discover 测试卡
            "3530111333300000", // JCB 测试卡
            "3566002020360505", // JCB 测试卡
            "3056930009020004", // Diners Club 测试卡
            "38520000023237",   // Diners Club 测试卡
        ];
        test_numbers.contains(&self.number.as_str())
    }
}

/// 信用卡验证器
pub struct CreditCardValidator;

impl CreditCardValidator {
    /// 验证卡号格式和 Luhn 校验
    pub fn validate(number: &str) -> ValidationResult {
        let card = CreditCard::new(number);
        
        let mut errors = Vec::new();
        let mut warnings = Vec::new();

        // 检查卡号长度
        if card.length < 13 {
            errors.push("卡号长度不足".to_string());
        } else if card.length > 19 {
            errors.push("卡号长度过长".to_string());
        }

        // Luhn 校验
        if !Self::check_luhn(number) {
            errors.push("Luhn 校验失败".to_string());
        }

        // 检查品牌匹配
        if card.brand == CardBrand::Unknown {
            warnings.push("未知的信用卡品牌".to_string());
        }

        // 检查是否为测试卡号
        if card.is_test_card() {
            warnings.push("这是一个测试卡号".to_string());
        }

        ValidationResult {
            valid: errors.is_empty(),
            errors,
            warnings,
            brand: card.brand,
            formatted: card.format(),
        }
    }

    /// 单独执行 Luhn 校验
    pub fn check_luhn(number: &str) -> bool {
        CreditCard::validate_luhn(&number.chars().filter(|c| c.is_ascii_digit()).collect::<String>())
    }

    /// 检测卡品牌
    pub fn detect_brand(number: &str) -> CardBrand {
        CreditCard::detect_brand(number)
    }

    /// 验证有效期 (MM/YY 或 MM/YYYY)
    pub fn validate_expiry(expiry: &str) -> bool {
        let parts: Vec<&str> = expiry.split('/').collect();
        if parts.len() != 2 {
            return false;
        }

        let month: u32 = match parts[0].trim().parse() {
            Ok(m) if m >= 1 && m <= 12 => m,
            _ => return false,
        };

        let year: u32 = match parts[1].trim().parse() {
            Ok(y) if y >= 0 => y,
            _ => return false,
        };

        // 简单验证：年份应该在合理范围内
        let current_year = 2024; // 简化处理
        let full_year = if year < 100 { year + 2000 } else { year };
        
        full_year >= current_year && month >= 1 && month <= 12
    }

    /// 验证 CVV
    pub fn validate_cvv(cvv: &str, brand: CardBrand) -> bool {
        let expected_len = match brand {
            CardBrand::Amex => 4,
            _ => 3,
        };
        
        cvv.len() == expected_len && cvv.chars().all(|c| c.is_ascii_digit())
    }
}

/// 验证结果
#[derive(Debug, Clone)]
pub struct ValidationResult {
    /// 是否有效
    pub valid: bool,
    /// 错误信息
    pub errors: Vec<String>,
    /// 警告信息
    pub warnings: Vec<String>,
    /// 识别的品牌
    pub brand: CardBrand,
    /// 格式化的卡号
    pub formatted: String,
}

/// 信用卡生成器（仅用于测试）
pub struct CreditCardGenerator;

impl CreditCardGenerator {
    /// 生成测试用的 Visa 卡号
    pub fn generate_visa() -> String {
        Self::generate_test_card("4", 16)
    }

    /// 生成测试用的 MasterCard 卡号
    pub fn generate_mastercard() -> String {
        let prefixes = ["51", "52", "53", "54", "55"];
        let prefix = prefixes[Self::random_usize() % prefixes.len()];
        Self::generate_test_card(prefix, 16)
    }

    /// 生成测试用的 Amex 卡号
    pub fn generate_amex() -> String {
        let prefixes = ["34", "37"];
        let prefix = prefixes[Self::random_usize() % prefixes.len()];
        Self::generate_test_card(prefix, 15)
    }

    /// 生成测试用的 Discover 卡号
    pub fn generate_discover() -> String {
        Self::generate_test_card("6011", 16)
    }

    /// 内部生成函数
    fn generate_test_card(prefix: &str, total_len: usize) -> String {
        let prefix_len = prefix.len();
        let remaining = total_len - prefix_len - 1; // -1 为校验位

        // 生成随机数字
        let mut number = prefix.to_string();
        for _ in 0..remaining {
            number.push_str(&format!("{}", Self::random_usize() % 10));
        }

        // 计算校验位
        let check_digit = Self::calculate_luhn_check(&number);
        number.push_str(&format!("{}", check_digit));

        number
    }

    /// 计算 Luhn 校验位
    fn calculate_luhn_check(number: &str) -> u32 {
        let digits: Vec<u32> = number
            .chars()
            .filter_map(|c| c.to_digit(10))
            .collect();

        let sum: u32 = digits
            .iter()
            .rev()
            .enumerate()
            .map(|(i, &d)| {
                if i % 2 == 0 {
                    let doubled = d * 2;
                    if doubled > 9 {
                        doubled - 9
                    } else {
                        doubled
                    }
                } else {
                    d
                }
            })
            .sum();

        (10 - (sum % 10)) % 10
    }

    /// 简单伪随机数生成器
    fn random_usize() -> usize {
        use std::time::{SystemTime, UNIX_EPOCH};
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as usize)
            .unwrap_or(0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_visa_validation() {
        // 有效的 Visa 卡号
        let card = CreditCard::new("4111111111111111");
        assert_eq!(card.brand(), CardBrand::Visa);
        assert!(card.is_valid());
        assert_eq!(card.length(), 16);
    }

    #[test]
    fn test_mastercard_validation() {
        let card = CreditCard::new("5555555555554444");
        assert_eq!(card.brand(), CardBrand::MasterCard);
        assert!(card.is_valid());
    }

    #[test]
    fn test_amex_validation() {
        let card = CreditCard::new("378282246310005");
        assert_eq!(card.brand(), CardBrand::Amex);
        assert!(card.is_valid());
        assert_eq!(card.length(), 15);
    }

    #[test]
    fn test_discover_validation() {
        let card = CreditCard::new("6011111111111117");
        assert_eq!(card.brand(), CardBrand::Discover);
        assert!(card.is_valid());
    }

    #[test]
    fn test_jcb_validation() {
        let card = CreditCard::new("3530111333300000");
        assert_eq!(card.brand(), CardBrand::Jcb);
        assert!(card.is_valid());
    }

    #[test]
    fn test_diners_club_validation() {
        // Diners Club 测试卡号 (14 位，以 36 开头)
        let card = CreditCard::new("36490102462661");
        assert_eq!(card.brand(), CardBrand::DinersClub);
        assert!(card.is_valid());
        assert_eq!(card.length(), 14);
    }

    #[test]
    fn test_invalid_luhn() {
        let card = CreditCard::new("4111111111111112");
        assert!(!card.is_valid());
    }

    #[test]
    fn test_format_visa() {
        let card = CreditCard::new("4111111111111111");
        assert_eq!(card.format(), "4111 1111 1111 1111");
    }

    #[test]
    fn test_format_amex() {
        let card = CreditCard::new("378282246310005");
        assert_eq!(card.format(), "3782 822463 10005");
    }

    #[test]
    fn test_mask_last4() {
        let card = CreditCard::new("4111111111111111");
        assert_eq!(card.mask_last4(), "************1111");
    }

    #[test]
    fn test_mask_middle() {
        let card = CreditCard::new("4111111111111111");
        assert_eq!(card.mask_middle(), "4111********1111");
    }

    #[test]
    fn test_bin() {
        let card = CreditCard::new("4111111111111111");
        assert_eq!(card.bin(), Some("411111"));
    }

    #[test]
    fn test_test_card_detection() {
        let card = CreditCard::new("4111111111111111");
        assert!(card.is_test_card());

        // 非测试卡
        let card2 = CreditCard::new("4532015112830366");
        assert!(!card2.is_test_card());
    }

    #[test]
    fn test_validator() {
        let result = CreditCardValidator::validate("4111111111111111");
        assert!(result.valid);
        assert_eq!(result.brand, CardBrand::Visa);
        assert!(result.warnings.iter().any(|w| w.contains("测试")));
    }

    #[test]
    fn test_luhn_check() {
        assert!(CreditCardValidator::check_luhn("4111111111111111"));
        assert!(!CreditCardValidator::check_luhn("4111111111111112"));
    }

    #[test]
    fn test_expiry_validation() {
        assert!(CreditCardValidator::validate_expiry("12/25"));
        assert!(CreditCardValidator::validate_expiry("01/30"));
        assert!(!CreditCardValidator::validate_expiry("13/25")); // 无效月份
        assert!(!CreditCardValidator::validate_expiry("00/25")); // 无效月份
    }

    #[test]
    fn test_cvv_validation() {
        assert!(CreditCardValidator::validate_cvv("123", CardBrand::Visa));
        assert!(CreditCardValidator::validate_cvv("1234", CardBrand::Amex));
        assert!(!CreditCardValidator::validate_cvv("12", CardBrand::Visa)); // 太短
        assert!(!CreditCardValidator::validate_cvv("1234", CardBrand::Visa)); // 太长
    }

    #[test]
    fn test_generate_visa() {
        let number = CreditCardGenerator::generate_visa();
        assert!(number.starts_with('4'));
        assert_eq!(number.len(), 16);
        assert!(CreditCardValidator::check_luhn(&number));
    }

    #[test]
    fn test_generate_mastercard() {
        let number = CreditCardGenerator::generate_mastercard();
        assert!(number.starts_with('5'));
        assert_eq!(number.len(), 16);
        assert!(CreditCardValidator::check_luhn(&number));
    }

    #[test]
    fn test_generate_amex() {
        let number = CreditCardGenerator::generate_amex();
        assert!(number.starts_with('3'));
        assert_eq!(number.len(), 15);
        assert!(CreditCardValidator::check_luhn(&number));
    }

    #[test]
    fn test_card_brand_display() {
        assert_eq!(format!("{}", CardBrand::Visa), "Visa");
        assert_eq!(format!("{}", CardBrand::MasterCard), "MasterCard");
        assert_eq!(format!("{}", CardBrand::Amex), "American Express");
    }

    #[test]
    fn test_empty_number() {
        let card = CreditCard::new("");
        assert_eq!(card.brand(), CardBrand::Unknown);
        assert!(!card.is_valid());
    }

    #[test]
    fn test_with_spaces_and_dashes() {
        let card = CreditCard::new("4111-1111-1111-1111");
        assert_eq!(card.number(), "4111111111111111");
        assert_eq!(card.brand(), CardBrand::Visa);
        assert!(card.is_valid());
    }

    #[test]
    fn test_unionpay() {
        // UnionPay 测试卡号 (62 开头，不在 Discover 的 622126-622925 范围内)
        let card = CreditCard::new("6212345678901234");
        assert_eq!(card.brand(), CardBrand::UnionPay);
    }

    #[test]
    fn test_mir() {
        let card = CreditCard::new("2200123456789012");
        assert_eq!(card.brand(), CardBrand::Mir);
    }
}