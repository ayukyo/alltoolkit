//! # Mask Utils - 敏感数据脱敏工具
//! 
//! 提供多种敏感数据脱敏功能，包括手机号、邮箱、身份证号、银行卡号等
//! 
//! ## 功能特性
//! - 手机号脱敏（支持国际格式）
//! - 邮箱脱敏
//! - 身份证号脱敏（18位中国身份证）
//! - 银行卡号脱敏
//! - 姓名脱敏
//! - 自定义规则脱敏
//! - IP地址脱敏
//! - JSON字段脱敏
//! 
//! ## 示例
//! ```rust
//! use mask_utils::{mask_phone, mask_email, mask_id_card};
//! 
//! let phone = mask_phone("13812345678");
//! assert_eq!(phone, "138****5678");
//! 
//! let email = mask_email("example@domain.com");
//! // "example" 有 7 个字符，保留首尾，中间 5 个星号
//! assert_eq!(email, "e*****e@domain.com");
//! ```

use std::collections::HashMap;

/// 默认脱敏字符
const DEFAULT_MASK_CHAR: char = '*';

/// 手机号脱敏
/// 
/// 将手机号中间4位替换为脱敏字符
/// 
/// # Arguments
/// * `phone` - 原始手机号
/// 
/// # Returns
/// 脱敏后的手机号，格式为：前3位****后4位
/// 
/// # Examples
/// ```
/// use mask_utils::mask_phone;
/// 
/// let result = mask_phone("13812345678");
/// assert_eq!(result, "138****5678");
/// ```
pub fn mask_phone(phone: &str) -> String {
    mask_phone_with_char(phone, DEFAULT_MASK_CHAR)
}

/// 手机号脱敏（自定义脱敏字符）
/// 
/// # Arguments
/// * `phone` - 原始手机号
/// * `mask_char` - 脱敏字符
/// 
/// # Examples
/// ```
/// use mask_utils::mask_phone_with_char;
/// 
/// let result = mask_phone_with_char("13812345678", '#');
/// assert_eq!(result, "138####5678");
/// ```
pub fn mask_phone_with_char(phone: &str, mask_char: char) -> String {
    let trimmed = phone.trim();
    let len = trimmed.chars().count();
    
    // 支持11位中国手机号
    if len == 11 && trimmed.chars().all(|c| c.is_ascii_digit()) {
        let start: String = trimmed.chars().take(3).collect();
        let end: String = trimmed.chars().skip(7).collect();
        let mask_str: String = (0..4).map(|_| mask_char).collect();
        format!("{}{}{}", start, mask_str, end)
    } else {
        // 国际号码格式：保留前3位和后3位
        if len > 6 {
            let visible_start = 3.min(len / 3);
            let visible_end = 3.min(len / 3);
            let start: String = trimmed.chars().take(visible_start).collect();
            let end: String = trimmed.chars().skip(len - visible_end).collect();
            let mask_len = len - visible_start - visible_end;
            let mask_str: String = (0..mask_len).map(|_| mask_char).collect();
            format!("{}{}{}", start, mask_str, end)
        } else {
            trimmed.to_string()
        }
    }
}

/// 邮箱脱敏
/// 
/// 保留邮箱用户名的首尾字符，中间用脱敏字符替换
/// 
/// # Arguments
/// * `email` - 原始邮箱地址
/// 
/// # Examples
/// ```
/// use mask_utils::mask_email;
/// 
/// let result = mask_email("example@domain.com");
/// // "example" 有 7 个字符，保留首尾各 1 位，中间 5 个星号
/// assert_eq!(result, "e*****e@domain.com");
/// ```
pub fn mask_email(email: &str) -> String {
    mask_email_with_char(email, DEFAULT_MASK_CHAR)
}

/// 邮箱脱敏（自定义脱敏字符）
/// 
/// # Arguments
/// * `email` - 原始邮箱地址
/// * `mask_char` - 脱敏字符
pub fn mask_email_with_char(email: &str, mask_char: char) -> String {
    let trimmed = email.trim();
    
    if let Some(at_pos) = trimmed.find('@') {
        let username = &trimmed[..at_pos];
        let domain = &trimmed[at_pos..];
        let username_len = username.chars().count();
        
        if username_len <= 1 {
            // 用户名太短，完全保留或用星号
            if username_len == 1 {
                format!("{}{}", mask_char, domain)
            } else {
                trimmed.to_string()
            }
        } else if username_len == 2 {
            // 两位：显示首位
            let first: String = username.chars().take(1).collect();
            let mask_str: String = mask_char.to_string();
            format!("{}{}{}", first, mask_str, domain)
        } else {
            // 保留首尾字符
            let first: String = username.chars().take(1).collect();
            let last: String = username.chars().skip(username_len - 1).take(1).collect();
            let mask_len = username_len - 2;
            let mask_str: String = (0..mask_len).map(|_| mask_char).collect();
            format!("{}{}{}{}", first, mask_str, last, domain)
        }
    } else {
        trimmed.to_string()
    }
}

/// 身份证号脱敏（18位中国身份证）
/// 
/// 保留前6位（地区码）和后4位，中间用脱敏字符替换
/// 
/// # Arguments
/// * `id_card` - 原始身份证号（15位或18位）
/// 
/// # Examples
/// ```
/// use mask_utils::mask_id_card;
/// 
/// let result = mask_id_card("11010519900307888X");
/// assert_eq!(result, "110105********888X");
/// ```
pub fn mask_id_card(id_card: &str) -> String {
    mask_id_card_with_char(id_card, DEFAULT_MASK_CHAR)
}

/// 身份证号脱敏（自定义脱敏字符）
pub fn mask_id_card_with_char(id_card: &str, mask_char: char) -> String {
    let trimmed = id_card.trim().to_uppercase();
    let len = trimmed.chars().count();
    
    // 支持15位或18位身份证
    if len == 15 || len == 18 {
        let start: String = trimmed.chars().take(6).collect();
        let end: String = trimmed.chars().skip(len - 4).collect();
        let mask_len = len - 10; // 保留前6位和后4位
        let mask_str: String = (0..mask_len).map(|_| mask_char).collect();
        format!("{}{}{}", start, mask_str, end)
    } else {
        trimmed
    }
}

/// 银行卡号脱敏
/// 
/// 保留前6位和后4位，中间用脱敏字符替换
/// 
/// # Arguments
/// * `card_number` - 原始银行卡号
/// 
/// # Examples
/// ```
/// use mask_utils::mask_bank_card;
/// 
/// let result = mask_bank_card("6222021234567890123");
/// // 19 位银行卡号：前 6 + 9 个星号 + 后 4
/// assert_eq!(result, "622202*********0123");
/// ```
pub fn mask_bank_card(card_number: &str) -> String {
    mask_bank_card_with_char(card_number, DEFAULT_MASK_CHAR)
}

/// 银行卡号脱敏（自定义脱敏字符）
pub fn mask_bank_card_with_char(card_number: &str, mask_char: char) -> String {
    let trimmed: String = card_number.chars().filter(|c| c.is_ascii_digit()).collect();
    let len = trimmed.chars().count();
    
    if len >= 10 {
        let start: String = trimmed.chars().take(6).collect();
        let end: String = trimmed.chars().skip(len - 4).collect();
        let mask_len = len - 10; // 保留前6位和后4位
        let mask_str: String = (0..mask_len).map(|_| mask_char).collect();
        format!("{}{}{}", start, mask_str, end)
    } else {
        trimmed
    }
}

/// 姓名脱敏
/// 
/// 中文姓名：保留姓氏，名字用脱敏字符替换
/// 英文姓名：保留首字母，其余用脱敏字符替换
/// 
/// # Arguments
/// * `name` - 原始姓名
/// 
/// # Examples
/// ```
/// use mask_utils::mask_name;
/// 
/// let result = mask_name("张三");
/// assert_eq!(result, "张*");
/// 
/// let result = mask_name("王小明");
/// assert_eq!(result, "王**");
/// ```
pub fn mask_name(name: &str) -> String {
    mask_name_with_char(name, DEFAULT_MASK_CHAR)
}

/// 姓名脱敏（自定义脱敏字符）
pub fn mask_name_with_char(name: &str, mask_char: char) -> String {
    let trimmed = name.trim();
    let chars: Vec<char> = trimmed.chars().collect();
    let len = chars.len();
    
    if len == 0 {
        return String::new();
    }
    
    // 判断是否为中文姓名（首字符为中文字符）
    let is_chinese = chars[0] >= '\u{4E00}' && chars[0] <= '\u{9FFF}';
    
    if is_chinese {
        // 中文姓名：保留姓氏
        if len == 1 {
            trimmed.to_string()
        } else {
            let mask_str: String = (0..len - 1).map(|_| mask_char).collect();
            format!("{}{}", chars[0], mask_str)
        }
    } else {
        // 英文姓名：保留首字母
        if len == 1 {
            trimmed.to_string()
        } else {
            let mask_str: String = (0..len - 1).map(|_| mask_char).collect();
            format!("{}{}", chars[0], mask_str)
        }
    }
}

/// IP地址脱敏
/// 
/// IPv4：保留前两段，后两段用脱敏字符替换
/// IPv6：保留前两段，其余用脱敏字符替换
/// 
/// # Arguments
/// * `ip` - 原始IP地址
/// 
/// # Examples
/// ```
/// use mask_utils::mask_ip;
/// 
/// let result = mask_ip("192.168.1.100");
/// assert_eq!(result, "192.168.*.*");
/// ```
pub fn mask_ip(ip: &str) -> String {
    mask_ip_with_char(ip, DEFAULT_MASK_CHAR)
}

/// IP地址脱敏（自定义脱敏字符）
pub fn mask_ip_with_char(ip: &str, mask_char: char) -> String {
    let trimmed = ip.trim();
    
    if trimmed.contains(':') {
        // IPv6
        let parts: Vec<&str> = trimmed.split(':').collect();
        if parts.len() >= 2 {
            let mask_str = mask_char.to_string();
            let masked_parts: Vec<String> = parts.iter().enumerate().map(|(i, &part)| {
                if i < 2 { part.to_string() } else { mask_str.clone() }
            }).collect();
            masked_parts.join(":")
        } else {
            trimmed.to_string()
        }
    } else {
        // IPv4
        let parts: Vec<&str> = trimmed.split('.').collect();
        if parts.len() == 4 {
            let mask_str = mask_char.to_string();
            format!("{}.{}.{}.{}", parts[0], parts[1], mask_str, mask_str)
        } else {
            trimmed.to_string()
        }
    }
}

/// 自定义脱敏规则
/// 
/// # Arguments
/// * `input` - 原始字符串
/// * `keep_start` - 保留前N个字符
/// * `keep_end` - 保留后N个字符
/// 
/// # Examples
/// ```
/// use mask_utils::mask_custom;
/// 
/// // "abcdef123456" 有 12 个字符，前 3 + 5 个星号 + 后 4
/// let result = mask_custom("abcdef123456", 3, 4);
/// assert_eq!(result, "abc*****3456");
/// ```
pub fn mask_custom(input: &str, keep_start: usize, keep_end: usize) -> String {
    mask_custom_with_char(input, keep_start, keep_end, DEFAULT_MASK_CHAR)
}

/// 自定义脱敏规则（指定脱敏字符）
pub fn mask_custom_with_char(input: &str, keep_start: usize, keep_end: usize, mask_char: char) -> String {
    let len = input.chars().count();
    
    if len == 0 {
        return String::new();
    }
    
    if keep_start + keep_end >= len {
        return input.to_string();
    }
    
    let start: String = input.chars().take(keep_start).collect();
    let end: String = input.chars().skip(len - keep_end).collect();
    let mask_len = len - keep_start - keep_end;
    let mask_str: String = (0..mask_len).map(|_| mask_char).collect();
    
    format!("{}{}{}", start, mask_str, end)
}

/// 完全脱敏（全部替换为脱敏字符）
/// 
/// # Arguments
/// * `input` - 原始字符串
/// 
/// # Examples
/// ```
/// use mask_utils::mask_all;
/// 
/// let result = mask_all("password123");
/// assert_eq!(result, "***********");
/// ```
pub fn mask_all(input: &str) -> String {
    mask_all_with_char(input, DEFAULT_MASK_CHAR)
}

/// 完全脱敏（自定义脱敏字符）
pub fn mask_all_with_char(input: &str, mask_char: char) -> String {
    input.chars().map(|_| mask_char).collect()
}

/// 按长度脱敏
/// 
/// 根据输入长度动态调整脱敏策略：
/// - 长度 <= 2：保留首位
/// - 长度 3-5：保留首尾各1位
/// - 长度 6-10：保留首尾各2位
/// - 长度 > 10：保留前3位和后4位
/// 
/// # Examples
/// ```
/// use mask_utils::mask_by_length;
/// 
/// let result = mask_by_length("abc");
/// assert_eq!(result, "a*c");
/// ```
pub fn mask_by_length(input: &str) -> String {
    mask_by_length_with_char(input, DEFAULT_MASK_CHAR)
}

/// 按长度脱敏（自定义脱敏字符）
pub fn mask_by_length_with_char(input: &str, mask_char: char) -> String {
    let chars: Vec<char> = input.chars().collect();
    let len = chars.len();
    
    if len == 0 {
        return String::new();
    }
    
    if len == 1 {
        return mask_char.to_string();
    }
    
    let (keep_start, keep_end) = match len {
        2 => (1, 0),
        3..=5 => (1, 1),
        6..=10 => (2, 2),
        _ => (3, 4),
    };
    
    mask_custom_with_char(input, keep_start, keep_end, mask_char)
}

/// JSON字段脱敏配置
#[derive(Debug, Clone)]
pub struct JsonMaskConfig {
    /// 需要脱敏的字段名列表
    pub fields: Vec<String>,
    /// 脱敏字符
    pub mask_char: char,
    /// 脱敏类型
    pub mask_type: MaskType,
}

/// 脱敏类型枚举
#[derive(Debug, Clone, Copy)]
pub enum MaskType {
    /// 手机号
    Phone,
    /// 邮箱
    Email,
    /// 身份证号
    IdCard,
    /// 银行卡号
    BankCard,
    /// 姓名
    Name,
    /// IP地址
    Ip,
    /// 完全脱敏
    All,
    /// 自定义（保留前N后M）
    Custom { keep_start: usize, keep_end: usize },
}

impl Default for JsonMaskConfig {
    fn default() -> Self {
        Self {
            fields: Vec::new(),
            mask_char: DEFAULT_MASK_CHAR,
            mask_type: MaskType::All,
        }
    }
}

impl JsonMaskConfig {
    /// 创建新的配置
    pub fn new() -> Self {
        Self::default()
    }
    
    /// 添加需要脱敏的字段
    pub fn with_field(mut self, field: &str) -> Self {
        self.fields.push(field.to_string());
        self
    }
    
    /// 添加多个字段
    pub fn with_fields(mut self, fields: &[&str]) -> Self {
        self.fields.extend(fields.iter().map(|s| s.to_string()));
        self
    }
    
    /// 设置脱敏字符
    pub fn with_mask_char(mut self, mask_char: char) -> Self {
        self.mask_char = mask_char;
        self
    }
    
    /// 设置脱敏类型
    pub fn with_mask_type(mut self, mask_type: MaskType) -> Self {
        self.mask_type = mask_type;
        self
    }
}

/// JSON字符串脱敏
/// 
/// 对JSON字符串中指定字段进行脱敏处理
/// 
/// # Arguments
/// * `json` - JSON字符串
/// * `config` - 脱敏配置
/// 
/// # Examples
/// ```
/// use mask_utils::{mask_json, JsonMaskConfig, MaskType};
/// 
/// let json = r#"{"name":"张三","phone":"13812345678"}"#;
/// let config = JsonMaskConfig::new()
///     .with_field("phone")
///     .with_mask_type(MaskType::Phone);
/// let result = mask_json(json, &config);
/// assert!(result.contains("138****5678"));
/// ```
pub fn mask_json(json: &str, config: &JsonMaskConfig) -> String {
    let mut result = json.to_string();
    
    for field in &config.fields {
        // 使用简单的字符串查找和替换
        let search_prefix = format!(r#""{}":""#, field);
        
        // 在结果中查找该字段
        while let Some(start_pos) = result.find(&search_prefix) {
            let value_start = start_pos + search_prefix.len();
            
            // 查找值的结束位置（下一个引号）
            if let Some(end_pos) = result[value_start..].find('"') {
                let value_end = value_start + end_pos;
                let original_value = &result[value_start..value_end];
                
                // 跳过已经脱敏的值（如果值中包含星号）
                if original_value.contains('*') {
                    break;
                }
                
                let masked_value = apply_mask_type(original_value, config.mask_type, config.mask_char);
                
                // 构建新的 JSON 片段
                let new_segment = format!(r#""{}":"{}""#, field, masked_value);
                let old_segment = format!(r#""{}":"{}""#, field, original_value);
                
                result = result.replace(&old_segment, &new_segment);
                break; // 每个字段只处理一次
            } else {
                break;
            }
        }
    }
    
    result
}

/// 应用脱敏类型
fn apply_mask_type(value: &str, mask_type: MaskType, mask_char: char) -> String {
    match mask_type {
        MaskType::Phone => mask_phone_with_char(value, mask_char),
        MaskType::Email => mask_email_with_char(value, mask_char),
        MaskType::IdCard => mask_id_card_with_char(value, mask_char),
        MaskType::BankCard => mask_bank_card_with_char(value, mask_char),
        MaskType::Name => mask_name_with_char(value, mask_char),
        MaskType::Ip => mask_ip_with_char(value, mask_char),
        MaskType::All => mask_all_with_char(value, mask_char),
        MaskType::Custom { keep_start, keep_end } => {
            mask_custom_with_char(value, keep_start, keep_end, mask_char)
        }
    }
}

/// 批量脱敏
/// 
/// 对多个值应用相同的脱敏规则
/// 
/// # Examples
/// ```
/// use mask_utils::{batch_mask, MaskType};
/// 
/// let phones = vec!["13812345678", "15987654321"];
/// let result = batch_mask(&phones, MaskType::Phone);
/// // "15987654321": 前 3 位是 "159"，后 4 位是 "4321"
/// assert_eq!(result, vec!["138****5678", "159****4321"]);
/// ```
pub fn batch_mask(values: &[&str], mask_type: MaskType) -> Vec<String> {
    batch_mask_with_char(values, mask_type, DEFAULT_MASK_CHAR)
}

/// 批量脱敏（自定义脱敏字符）
pub fn batch_mask_with_char(values: &[&str], mask_type: MaskType, mask_char: char) -> Vec<String> {
    values.iter()
        .map(|v| apply_mask_type(v, mask_type, mask_char))
        .collect()
}

/// 脱敏映射器
/// 
/// 使用HashMap配置字段和脱敏类型的映射关系
/// 
/// # Examples
/// ```
/// use mask_utils::{MaskMapper, MaskType};
/// 
/// let mut mapper = MaskMapper::new();
/// mapper.add("phone", MaskType::Phone);
/// mapper.add("email", MaskType::Email);
/// 
/// let result = mapper.mask_field("phone", "13812345678");
/// assert_eq!(result, "138****5678");
/// ```
pub struct MaskMapper {
    rules: HashMap<String, (MaskType, char)>,
}

impl MaskMapper {
    /// 创建新的映射器
    pub fn new() -> Self {
        Self {
            rules: HashMap::new(),
        }
    }
    
    /// 添加脱敏规则
    pub fn add(&mut self, field: &str, mask_type: MaskType) -> &mut Self {
        self.rules.insert(field.to_string(), (mask_type, DEFAULT_MASK_CHAR));
        self
    }
    
    /// 添加脱敏规则（自定义脱敏字符）
    pub fn add_with_char(&mut self, field: &str, mask_type: MaskType, mask_char: char) -> &mut Self {
        self.rules.insert(field.to_string(), (mask_type, mask_char));
        self
    }
    
    /// 脱敏字段值
    pub fn mask_field(&self, field: &str, value: &str) -> String {
        if let Some((mask_type, mask_char)) = self.rules.get(field) {
            apply_mask_type(value, *mask_type, *mask_char)
        } else {
            value.to_string()
        }
    }
    
    /// 脱敏Map中的所有字段
    pub fn mask_map(&self, data: &HashMap<String, String>) -> HashMap<String, String> {
        data.iter()
            .map(|(k, v)| {
                let masked = self.mask_field(k, v);
                (k.clone(), masked)
            })
            .collect()
    }
}

impl Default for MaskMapper {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_mask_phone() {
        assert_eq!(mask_phone("13812345678"), "138****5678");
        assert_eq!(mask_phone("138 1234 5678"), "138*******678"); // 13字符，保留前3后3
        assert_eq!(mask_phone("123"), "123"); // 太短
        assert_eq!(mask_phone_with_char("13812345678", '#'), "138####5678");
    }
    
    #[test]
    fn test_mask_email() {
        assert_eq!(mask_email("example@domain.com"), "e*****e@domain.com");
        assert_eq!(mask_email("ab@test.com"), "a*@test.com");
        assert_eq!(mask_email("a@test.com"), "*@test.com");
        assert_eq!(mask_email("notanemail"), "notanemail");
    }
    
    #[test]
    fn test_mask_id_card() {
        // 18位身份证: 前6 + 8个星号 + 后4
        assert_eq!(mask_id_card("11010519900307888X"), "110105********888X");
        // 15位身份证: 前6 + 5个星号 + 后4
        assert_eq!(mask_id_card("110105199003078"), "110105*****3078");
        assert_eq!(mask_id_card("123"), "123");
    }
    
    #[test]
    fn test_mask_bank_card() {
        // 19位银行卡: 前6 + 9个星号 + 后4
        assert_eq!(mask_bank_card("6222021234567890123"), "622202*********0123");
        // 去掉空格后19位
        assert_eq!(mask_bank_card("6222 0212 3456 7890 123"), "622202*********0123");
    }
    
    #[test]
    fn test_mask_name() {
        assert_eq!(mask_name("张三"), "张*");
        assert_eq!(mask_name("王小明"), "王**");
        assert_eq!(mask_name("欧阳修"), "欧**");
        assert_eq!(mask_name("John"), "J***");
        assert_eq!(mask_name("A"), "A");
    }
    
    #[test]
    fn test_mask_ip() {
        assert_eq!(mask_ip("192.168.1.100"), "192.168.*.*");
        assert_eq!(mask_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334"), "2001:0db8:*:*:*:*:*:*");
    }
    
    #[test]
    fn test_mask_custom() {
        assert_eq!(mask_custom("abcdef123456", 3, 4), "abc*****3456");
        assert_eq!(mask_custom("abc", 2, 2), "abc"); // keep超过长度
        assert_eq!(mask_custom_with_char("abcdef", 2, 2, '#'), "ab##ef");
    }
    
    #[test]
    fn test_mask_all() {
        assert_eq!(mask_all("password123"), "***********");
        assert_eq!(mask_all_with_char("test", '#'), "####");
    }
    
    #[test]
    fn test_mask_by_length() {
        assert_eq!(mask_by_length("a"), "*");
        assert_eq!(mask_by_length("ab"), "a*");
        assert_eq!(mask_by_length("abc"), "a*c");
        assert_eq!(mask_by_length("abcdef"), "ab**ef");
        assert_eq!(mask_by_length("abcdefghijk"), "abc****hijk");
    }
    
    #[test]
    fn test_batch_mask() {
        let phones = vec!["13812345678", "15987654321"];
        let result = batch_mask(&phones, MaskType::Phone);
        // "15987654321": 前3位=159, 后4位=4321
        assert_eq!(result, vec!["138****5678", "159****4321"]);
    }
    
    #[test]
    fn test_mask_mapper() {
        let mut mapper = MaskMapper::new();
        mapper.add("phone", MaskType::Phone);
        mapper.add("email", MaskType::Email);
        
        assert_eq!(mapper.mask_field("phone", "13812345678"), "138****5678");
        assert_eq!(mapper.mask_field("email", "test@example.com"), "t**t@example.com");
        assert_eq!(mapper.mask_field("unknown", "value"), "value");
    }
    
    #[test]
    fn test_mask_json() {
        let json = r#"{"name":"张三","phone":"13812345678"}"#;
        let config = JsonMaskConfig::new()
            .with_field("phone")
            .with_mask_type(MaskType::Phone);
        let result = mask_json(json, &config);
        assert!(result.contains("138****5678"));
    }
}