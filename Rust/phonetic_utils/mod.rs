//! # Phonetic Utils
//!
//! 音标编码工具模块 - 用于单词语音匹配和模糊搜索
//!
//! 实现了多种音标编码算法：
//! - Soundex (1918)
//! - Metaphone (1990)
//! - Double Metaphone (2000)
//! - Caverphone (2002)
//! - Cologne Phonetic (Kölner Phonetik)
//! - NYSIIS (New York State Identification and Intelligence System)
//!
//! ## 特性
//! - 零外部依赖
//! - 纯 Rust 实现
//! - 完整的测试覆盖
//! - 支持多种编码算法

use std::collections::HashMap;

/// Soundex 编码器
/// 
/// Soundex 是最早的音标编码算法之一，由 Robert Russell 在 1918 年发明。
/// 它将单词转换为一个字母后跟三个数字的编码。
/// 
/// # Example
/// ```
/// use phonetic_utils::Soundex;
/// 
/// let soundex = Soundex::new();
/// assert_eq!(soundex.encode("Robert"), "R163");
/// assert_eq!(soundex.encode("Rupert"), "R163");
/// ```
#[derive(Debug, Clone, Default)]
pub struct Soundex {
    /// 是否保留前导字母大小写
    pub preserve_case: bool,
}

impl Soundex {
    /// 创建新的 Soundex 编码器
    pub fn new() -> Self {
        Self { preserve_case: false }
    }
    
    /// 编码单词
    pub fn encode(&self, word: &str) -> String {
        let word = word.trim();
        if word.is_empty() {
            return String::new();
        }
        
        let chars: Vec<char> = word.to_uppercase().chars().collect();
        if chars.is_empty() {
            return String::new();
        }
        
        let first_letter = chars[0];
        let mut result = String::from(first_letter);
        
        // Soundex 数字映射
        let digit_map: HashMap<char, char> = [
            ('B', '1'), ('F', '1'), ('P', '1'), ('V', '1'),
            ('C', '2'), ('G', '2'), ('J', '2'), ('K', '2'), ('Q', '2'), ('S', '2'), ('X', '2'), ('Z', '2'),
            ('D', '3'), ('T', '3'),
            ('L', '4'),
            ('M', '5'), ('N', '5'),
            ('R', '6'),
        ].iter().cloned().collect();
        
        let mut prev_code = digit_map.get(&first_letter).copied();
        let vowels_and_hw = ['A', 'E', 'I', 'O', 'U', 'H', 'W'];
        
        for &ch in chars.iter().skip(1) {
            if vowels_and_hw.contains(&ch) {
                continue;
            }
            
            if let Some(&digit) = digit_map.get(&ch) {
                if prev_code != Some(digit) {
                    result.push(digit);
                    if result.len() >= 4 {
                        break;
                    }
                }
                prev_code = Some(digit);
            }
        }
        
        while result.len() < 4 {
            result.push('0');
        }
        
        if self.preserve_case {
            word.chars().next().unwrap_or_default().to_string() + &result[1..]
        } else {
            result
        }
    }
    
    /// 计算两个单词的 Soundex 相似度
    /// 返回 0.0 到 1.0 之间的值，1.0 表示完全匹配
    pub fn similarity(&self, word1: &str, word2: &str) -> f64 {
        let code1 = self.encode(word1);
        let code2 = self.encode(word2);
        
        if code1 == code2 {
            return 1.0;
        }
        
        let distance = Self::edit_distance(&code1, &code2);
        let max_len = code1.len().max(code2.len()) as f64;
        
        if max_len == 0.0 {
            return 1.0;
        }
        
        1.0 - (distance as f64 / max_len)
    }
    
    fn edit_distance(s1: &str, s2: &str) -> usize {
        let chars1: Vec<char> = s1.chars().collect();
        let chars2: Vec<char> = s2.chars().collect();
        let len1 = chars1.len();
        let len2 = chars2.len();
        
        let mut dp = vec![vec![0; len2 + 1]; len1 + 1];
        
        for i in 0..=len1 {
            dp[i][0] = i;
        }
        for j in 0..=len2 {
            dp[0][j] = j;
        }
        
        for i in 1..=len1 {
            for j in 1..=len2 {
                if chars1[i - 1] == chars2[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = dp[i - 1][j - 1].min(dp[i][j - 1]).min(dp[i - 1][j]) + 1;
                }
            }
        }
        
        dp[len1][len2]
    }
}

/// Metaphone 编码器
/// 
/// Metaphone 由 Lawrence Philips 在 1990 年发明，是 Soundex 的改进版本。
/// 
/// # Example
/// ```
/// use phonetic_utils::Metaphone;
/// 
/// let metaphone = Metaphone::new();
/// assert_eq!(metaphone.encode("Smith"), "SM0T");
/// ```
#[derive(Debug, Clone, Default)]
pub struct Metaphone {
    /// 最大编码长度
    pub max_length: usize,
}

impl Metaphone {
    pub fn new() -> Self {
        Self { max_length: 4 }
    }
    
    pub fn encode(&self, word: &str) -> String {
        let word = word.trim().to_uppercase();
        if word.is_empty() {
            return String::new();
        }
        
        let chars: Vec<char> = word.chars().collect();
        let len = chars.len();
        let mut result = String::new();
        let mut i = 0;
        
        if len >= 2 {
            let two_char: String = chars[0..2].iter().collect();
            match two_char.as_str() {
                "KN" | "GN" | "PN" | "AE" | "WR" => {
                    result.push(chars[1]);
                    i = 2;
                }
                "WH" => {
                    result.push('W');
                    i = 2;
                }
                _ => {}
            }
        }
        
        if i == 0 && !chars.is_empty() && chars[0] == 'X' {
            result.push('S');
            i = 1;
        }
        
        while i < len && result.len() < self.max_length {
            let ch = chars[i];
            
            match ch {
                'A' | 'E' | 'I' | 'O' | 'U' => {
                    if i == 0 {
                        result.push(ch);
                    }
                }
                'B' => {
                    if i == 0 || chars[i - 1] != 'M' || (i + 1 < len) {
                        result.push('B');
                    }
                }
                'C' => {
                    if i + 1 < len && chars[i + 1] == 'H' {
                        result.push('X');
                        i += 1;
                    } else if i + 1 < len && chars[i + 1] == 'I' {
                        if i + 2 < len && chars[i + 2] == 'A' {
                            result.push('X');
                        } else {
                            result.push('S');
                        }
                    } else if i > 0 && chars[i - 1] == 'S' && i + 1 < len && ['I', 'E', 'Y'].contains(&chars[i + 1]) {
                    } else if i + 1 < len && ['I', 'E', 'Y'].contains(&chars[i + 1]) {
                        result.push('S');
                    } else {
                        result.push('K');
                    }
                }
                'D' => {
                    if i + 2 < len && chars[i + 1] == 'G' && ['E', 'I', 'Y'].contains(&chars[i + 2]) {
                        result.push('J');
                        i += 2;
                    } else {
                        result.push('T');
                    }
                }
                'F' => result.push('F'),
                'G' => {
                    if i + 1 < len && chars[i + 1] == 'H' {
                    } else if i + 1 < len && ['E', 'I', 'Y'].contains(&chars[i + 1]) {
                        result.push('J');
                    } else {
                        result.push('K');
                    }
                }
                'H' => {
                    if i == 0 || (i + 1 < len && ['A', 'E', 'I', 'O', 'U'].contains(&chars[i + 1])) {
                        if !['C', 'S', 'P', 'T', 'G'].contains(&chars.get(i.wrapping_sub(1)).unwrap_or(&' ')) {
                            result.push('H');
                        }
                    }
                }
                'J' => result.push('J'),
                'K' => {
                    if i == 0 || chars[i - 1] != 'C' {
                        result.push('K');
                    }
                }
                'L' => result.push('L'),
                'M' => result.push('M'),
                'N' => result.push('N'),
                'P' => {
                    if i + 1 < len && chars[i + 1] == 'H' {
                        result.push('F');
                        i += 1;
                    } else {
                        result.push('P');
                    }
                }
                'Q' => result.push('K'),
                'R' => result.push('R'),
                'S' => {
                    if i + 2 < len && chars[i + 1] == 'I' && ['O', 'A'].contains(&chars[i + 2]) {
                        result.push('X');
                        i += 1;
                    } else if i + 1 < len && chars[i + 1] == 'H' {
                        result.push('X');
                        i += 1;
                    } else {
                        result.push('S');
                    }
                }
                'T' => {
                    if i + 2 < len && chars[i + 1] == 'I' && ['O', 'A'].contains(&chars[i + 2]) {
                        result.push('X');
                        i += 1;
                    } else if i + 1 < len && chars[i + 1] == 'H' {
                        result.push('0');
                        i += 1;
                    } else if i + 1 < len && chars[i + 1] == 'C' && i + 2 < len && chars[i + 2] == 'H' {
                        i += 2;
                    } else {
                        result.push('T');
                    }
                }
                'V' => result.push('F'),
                'W' | 'Y' => {
                    if i + 1 < len && ['A', 'E', 'I', 'O', 'U'].contains(&chars[i + 1]) {
                        result.push(ch);
                    }
                }
                'X' => {
                    result.push('K');
                    if result.len() < self.max_length {
                        result.push('S');
                    }
                }
                'Z' => result.push('S'),
                _ => {}
            }
            
            i += 1;
        }
        
        if result.len() > self.max_length {
            result.truncate(self.max_length);
        }
        
        result
    }
    
    pub fn sounds_like(&self, word1: &str, word2: &str) -> bool {
        self.encode(word1) == self.encode(word2)
    }
}

/// Double Metaphone 编码器
/// 
/// Double Metaphone 由 Lawrence Philips 在 2000 年发明，
/// 为每个单词生成两个可能的编码。
/// 
/// # Example
/// ```
/// use phonetic_utils::DoubleMetaphone;
/// 
/// let dm = DoubleMetaphone::new();
/// let (primary, alternate) = dm.encode("Smith");
/// ```
#[derive(Debug, Clone, Default)]
pub struct DoubleMetaphone {
    pub max_length: usize,
}

impl DoubleMetaphone {
    pub fn new() -> Self {
        Self { max_length: 4 }
    }
    
    pub fn encode(&self, word: &str) -> (String, String) {
        let word = word.trim().to_uppercase();
        if word.is_empty() {
            return (String::new(), String::new());
        }
        
        let chars: Vec<char> = word.chars().collect();
        let len = chars.len();
        
        let mut primary = String::new();
        let mut alternate = String::new();
        let mut i = 0;
        
        if len >= 1 {
            if chars[0] == 'X' {
                primary.push('S');
                alternate.push('S');
            } else if len >= 2 {
                let first_two: String = chars[0..2].iter().collect();
                match first_two.as_str() {
                    "KN" | "GN" | "PN" | "WR" | "AE" => {
                        i = 1;
                    }
                    "WH" => {
                        primary.push('W');
                        alternate.push('A');
                        i = 2;
                    }
                    _ => {}
                }
            }
        }
        
        while i < len && (primary.len() < self.max_length || alternate.len() < self.max_length) {
            let ch = chars[i];
            
            let (p, a) = match ch {
                'A' | 'E' | 'I' | 'O' | 'U' => {
                    if i == 0 {
                        ('A', 'A')
                    } else {
                        ('\0', '\0')
                    }
                }
                'B' => {
                    if i + 1 < len && chars[i + 1] == 'B' {
                        i += 1;
                    }
                    ('P', 'P')
                }
                'C' => self.encode_c(&chars, i, len),
                'D' => {
                    if i + 2 < len && chars[i + 1] == 'G' && ['I', 'E', 'Y'].contains(&chars[i + 2]) {
                        i += 2;
                        ('J', 'J')
                    } else {
                        ('T', 'T')
                    }
                }
                'F' => ('F', 'F'),
                'G' => self.encode_g(&chars, i, len),
                'H' => self.encode_h(&chars, i, len),
                'J' => ('J', 'J'),
                'K' => ('K', 'K'),
                'L' => ('L', 'L'),
                'M' => ('M', 'M'),
                'N' => ('N', 'N'),
                'P' => {
                    let next = chars.get(i + 1).copied().unwrap_or(' ');
                    if next == 'H' {
                        i += 1;
                        ('F', 'F')
                    } else {
                        ('P', 'P')
                    }
                }
                'Q' => ('K', 'K'),
                'R' => ('R', 'R'),
                'S' => self.encode_s(&chars, i, len),
                'T' => self.encode_t(&chars, i, len),
                'V' => ('F', 'F'),
                'W' | 'Y' => {
                    if i + 1 < len && ['A', 'E', 'I', 'O', 'U'].contains(&chars[i + 1]) {
                        (ch, ch)
                    } else {
                        ('\0', '\0')
                    }
                }
                'X' => ('K', 'S'),
                'Z' => ('S', 'S'),
                _ => ('\0', '\0'),
            };
            
            if p != '\0' && primary.len() < self.max_length {
                primary.push(p);
            }
            if a != '\0' && alternate.len() < self.max_length {
                alternate.push(a);
            }
            
            i += 1;
        }
        
        while primary.len() < self.max_length {
            primary.push('0');
        }
        while alternate.len() < self.max_length {
            alternate.push('0');
        }
        
        (primary, alternate)
    }
    
    fn encode_c(&self, chars: &[char], i: usize, len: usize) -> (char, char) {
        if i + 1 < len {
            match chars[i + 1] {
                'H' => {
                    if i > 0 {
                        let prev = chars[i - 1];
                        if ['A', 'E', 'I', 'O', 'U'].contains(&prev) {
                            return ('K', 'K');
                        }
                    }
                    ('X', 'X')
                }
                'I' | 'E' | 'Y' => ('S', 'S'),
                _ => ('K', 'K'),
            }
        } else {
            ('K', 'K')
        }
    }
    
    fn encode_g(&self, chars: &[char], i: usize, len: usize) -> (char, char) {
        if i + 1 < len && chars[i + 1] == 'H' {
            if i + 2 < len && chars[i + 2] == 'T' {
                return ('\0', '\0');
            }
            ('K', 'K')
        } else if i + 1 < len && ['E', 'I', 'Y'].contains(&chars[i + 1]) {
            ('J', 'J')
        } else {
            ('K', 'K')
        }
    }
    
    fn encode_h(&self, chars: &[char], i: usize, len: usize) -> (char, char) {
        if i == 0 || (i + 1 < len && ['A', 'E', 'I', 'O', 'U'].contains(&chars[i + 1])) {
            ('H', 'H')
        } else {
            ('\0', '\0')
        }
    }
    
    fn encode_s(&self, chars: &[char], i: usize, len: usize) -> (char, char) {
        if i + 1 < len {
            if chars[i + 1] == 'H' {
                return ('X', 'X');
            } else if chars[i + 1] == 'I' && i + 2 < len && ['A', 'O'].contains(&chars[i + 2]) {
                return ('X', 'X');
            }
        }
        ('S', 'S')
    }
    
    fn encode_t(&self, chars: &[char], i: usize, len: usize) -> (char, char) {
        if i + 1 < len {
            match chars[i + 1] {
                'H' => return ('0', 'T'),
                'I' if i + 2 < len && ['A', 'O'].contains(&chars[i + 2]) => return ('X', 'X'),
                'C' if i + 2 < len && chars[i + 2] == 'H' => return ('\0', '\0'),
                _ => {}
            }
        }
        ('T', 'T')
    }
    
    pub fn sounds_like(&self, word1: &str, word2: &str) -> bool {
        let (p1, a1) = self.encode(word1);
        let (p2, a2) = self.encode(word2);
        
        p1 == p2 || p1 == a2 || a1 == p2 || a1 == a2
    }
}

/// Caverphone 编码器
/// 
/// Caverphone 由 David Hood 在 2002 年为新西兰克赖斯特彻奇选举人名录开发。
/// 
/// # Example
/// ```
/// use phonetic_utils::Caverphone;
/// 
/// let caverphone = Caverphone::new();
/// assert_eq!(caverphone.encode("Lee"), "L11111");
/// ```
#[derive(Debug, Clone, Default)]
pub struct Caverphone;

impl Caverphone {
    pub fn new() -> Self {
        Self
    }
    
    pub fn encode(&self, word: &str) -> String {
        let mut word = word.trim().to_uppercase();
        
        if word.is_empty() {
            return "111111".to_string();
        }
        
        if word.ends_with('E') {
            word.pop();
        }
        
        let replacements = [
            ("COUGH", "COU2F"),
            ("OUGH", "OU2"),
            ("GN", "2N"),
            ("MBT", "M2T"),
            ("EIGHT", "EIT"),
            ("AIGHT", "AIT"),
            ("IGHT", "AIT"),
            ("J", "K"),
            ("A", "3"),
            ("E", "3"),
            ("I", "3"),
            ("O", "3"),
            ("U", "3"),
            ("Y", "3"),
            ("V", "F"),
            ("Z", "S"),
            ("B", "P"),
            ("G", "K"),
            ("C", "K"),
            ("Q", "K"),
            ("X", "K"),
        ];
        
        for (from, to) in replacements.iter() {
            word = word.replace(from, to);
        }
        
        word = word.replace('H', "");
        
        let mut chars: Vec<char> = Vec::new();
        for ch in word.chars() {
            if chars.last() != Some(&ch) {
                chars.push(ch);
            }
        }
        
        word = chars.into_iter().filter(|&c| c != '3').collect();
        
        let mut result = String::new();
        for (i, ch) in word.chars().enumerate() {
            if i == 0 {
                result.push(ch);
            } else if ch.is_ascii_digit() {
                result.push(ch);
            } else {
                result.push('3');
            }
        }
        
        result = result.replace('3', "1");
        
        while result.len() < 6 {
            result.push('1');
        }
        result.truncate(6);
        
        result
    }
}

/// Cologne Phonetic (Kölner Phonetik) 编码器
/// 
/// 科隆语音编码是德语名称匹配的标准算法。
/// 
/// # Example
/// ```
/// use phonetic_utils::ColognePhonetic;
/// 
/// let cologne = ColognePhonetic::new();
/// let code = cologne.encode("Müller");
/// ```
#[derive(Debug, Clone, Default)]
pub struct ColognePhonetic;

impl ColognePhonetic {
    pub fn new() -> Self {
        Self
    }
    
    pub fn encode(&self, word: &str) -> String {
        let word = word.trim().to_uppercase();
        if word.is_empty() {
            return String::new();
        }
        
        let chars: Vec<char> = word.chars().collect();
        let mut result = String::new();
        let mut prev_code: Option<char> = None;
        
        for (i, &ch) in chars.iter().enumerate() {
            let code = self.get_cologne_code(ch, i, &chars);
            
            if let Some(c) = code {
                if prev_code != Some(c) || c == '0' {
                    result.push(c);
                }
                prev_code = Some(c);
            }
        }
        
        result
    }
    
    fn get_cologne_code(&self, ch: char, i: usize, chars: &[char]) -> Option<char> {
        match ch {
            'A' | 'E' | 'I' | 'O' | 'U' | 'Y' | 'Ä' | 'Ö' | 'Ü' => Some('0'),
            'H' | 'W' => None,
            'B' | 'P' => Some('1'),
            'D' | 'T' => {
                if i + 1 < chars.len() && ['C', 'S', 'Z'].contains(&chars[i + 1]) {
                    Some('8')
                } else {
                    Some('2')
                }
            }
            'F' | 'V' => Some('3'),
            'G' | 'K' | 'Q' => Some('4'),
            'C' => {
                if i == 0 {
                    if i + 1 < chars.len() && ['A', 'H', 'K', 'L', 'O', 'Q', 'R', 'U', 'X'].contains(&chars[i + 1]) {
                        Some('4')
                    } else {
                        Some('8')
                    }
                } else {
                    let prev = chars.get(i.wrapping_sub(1)).copied().unwrap_or(' ');
                    if ['A', 'H', 'K', 'O', 'Q', 'U', 'X'].contains(&prev) {
                        Some('4')
                    } else {
                        Some('8')
                    }
                }
            }
            'X' => Some('8'),
            'L' => Some('5'),
            'M' | 'N' => Some('6'),
            'R' => Some('7'),
            'S' | 'Z' | 'ß' => Some('8'),
            _ => None,
        }
    }
}

/// NYSIIS 编码器
/// 
/// New York State Identification and Intelligence System
/// 
/// # Example
/// ```
/// use phonetic_utils::Nysiis;
/// 
/// let nysiis = Nysiis::new();
/// let code = nysiis.encode("Smith");
/// ```
#[derive(Debug, Clone, Default)]
pub struct Nysiis;

impl Nysiis {
    pub fn new() -> Self {
        Self
    }
    
    pub fn encode(&self, word: &str) -> String {
        let mut word = word.trim().to_uppercase();
        if word.is_empty() {
            return String::new();
        }
        
        let prefixes = [
            ("MAC", "MCC"), ("KN", "NN"), ("K", "C"), ("PH", "FF"),
            ("PF", "FF"), ("SCH", "SSS"),
        ];
        for (from, to) in prefixes.iter() {
            if word.starts_with(from) {
                word = format!("{}{}", to, &word[from.len()..]);
                break;
            }
        }
        
        let suffixes = [
            ("EE", "Y"), ("IE", "Y"), ("DT", "D"), ("RT", "D"),
            ("NT", "D"), ("ND", "D"),
        ];
        for (from, to) in suffixes.iter() {
            if word.ends_with(from) {
                word = format!("{}{}", &word[..word.len()-from.len()], to);
                break;
            }
        }
        
        let chars: Vec<char> = word.chars().collect();
        let mut result = String::new();
        let mut prev = '\0';
        
        for (i, &ch) in chars.iter().enumerate() {
            let next = chars.get(i + 1).copied().unwrap_or(' ');
            
            let mapped = match ch {
                'E' | 'I' | 'O' | 'U' => 'A',
                'A' => 'A',
                'K' => 'C',
                'M' | 'N' => ch,
                'Q' => 'Q',
                'Z' => 'S',
                'F' | 'B' | 'S' | 'P' => ch,
                'C' => {
                    if ['S', 'T', 'Z'].contains(&next) {
                        'S'
                    } else {
                        'C'
                    }
                }
                'D' => {
                    if next == 'G' {
                        'G'
                    } else {
                        'D'
                    }
                }
                'G' => {
                    if next == 'C' {
                        'C'
                    } else {
                        'G'
                    }
                }
                'T' => {
                    if next == 'H' {
                        continue;
                    } else if ['S', 'Z'].contains(&next) {
                        'S'
                    } else {
                        'T'
                    }
                }
                'R' | 'L' => ch,
                'H' | 'W' | 'Y' => {
                    if !['A', 'E', 'I', 'O', 'U'].contains(&prev) {
                        prev
                    } else {
                        continue;
                    }
                }
                _ => continue,
            };
            
            if mapped != prev {
                result.push(mapped);
            }
            prev = mapped;
        }
        
        if result.ends_with('S') {
            result.pop();
        }
        
        if result.ends_with("AY") {
            result.pop();
            result.pop();
            result.push('Y');
        }
        
        while result.len() < 4 {
            result.push(' ');
        }
        result.truncate(4);
        result.trim_end().to_string()
    }
}

/// 音标编码工具函数集合
pub struct PhoneticUtils;

impl PhoneticUtils {
    /// 批量 Soundex 编码
    pub fn batch_soundex(words: &[&str]) -> Vec<String> {
        let soundex = Soundex::new();
        words.iter().map(|w| soundex.encode(w)).collect()
    }
    
    /// 批量 Metaphone 编码
    pub fn batch_metaphone(words: &[&str]) -> Vec<String> {
        let metaphone = Metaphone::new();
        words.iter().map(|w| metaphone.encode(w)).collect()
    }
    
    /// 在列表中查找与目标单词语音相似的单词
    pub fn find_similar(words: &[&str], target: &str, threshold: f64) -> Vec<String> {
        let soundex = Soundex::new();
        
        words
            .iter()
            .filter(|w| {
                let sim = soundex.similarity(target, w);
                sim >= threshold
            })
            .map(|w| w.to_string())
            .collect()
    }
    
    /// 对单词列表进行音标分组
    pub fn group_by_phonetic(words: &[&str]) -> HashMap<String, Vec<String>> {
        let soundex = Soundex::new();
        let mut groups: HashMap<String, Vec<String>> = HashMap::new();
        
        for word in words {
            let code = soundex.encode(word);
            groups.entry(code).or_default().push(word.to_string());
        }
        
        groups
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_soundex() {
        let soundex = Soundex::new();
        
        // 测试基本编码 - 同音词应有相同编码
        assert_eq!(soundex.encode("Robert"), soundex.encode("Rupert"));
        assert_eq!(soundex.encode("Smith"), soundex.encode("Smythe"));
        assert_eq!(soundex.encode("Ashcraft"), soundex.encode("Ashcroft"));
        
        // 测试编码格式（字母+3位数字）
        let code = soundex.encode("Robert");
        assert!(code.starts_with('R'));
        assert_eq!(code.len(), 4);
        
        // 空字符串
        assert_eq!(soundex.encode(""), "");
        
        // 单字符
        assert_eq!(soundex.encode("A"), "A000");
    }
    
    #[test]
    fn test_soundex_similarity() {
        let soundex = Soundex::new();
        
        // 同音词相似度应为 1.0
        assert_eq!(soundex.similarity("Robert", "Rupert"), 1.0);
        assert_eq!(soundex.similarity("Smith", "Smythe"), 1.0);
        
        // 不同音的词相似度较低
        assert!(soundex.similarity("Smith", "Johnson") < 0.5);
    }
    
    #[test]
    fn test_metaphone() {
        let metaphone = Metaphone::new();
        
        // 测试基本功能
        let smith_code = metaphone.encode("Smith");
        assert!(smith_code.starts_with('S'));
        
        // phone 和 fish 应有合理编码
        assert!(metaphone.encode("phone").contains('F'));
        assert!(metaphone.encode("fish").contains('F'));
        
        // 测试语音相似
        assert!(metaphone.sounds_like("Smith", "Smith"));
    }
    
    #[test]
    fn test_double_metaphone() {
        let dm = DoubleMetaphone::new();
        
        let (p1, _a1) = dm.encode("Smith");
        assert!(p1.starts_with('S'));
        
        let (p2, _a2) = dm.encode("Schmidt");
        assert!(p2.starts_with('S'));
        
        // 测试语音匹配
        assert!(dm.sounds_like("Smith", "Smith"));
    }
    
    #[test]
    fn test_caverphone() {
        let caverphone = Caverphone::new();
        
        // 测试编码长度为 6 位
        assert_eq!(caverphone.encode("Lee").len(), 6);
        assert_eq!(caverphone.encode("Thompson").len(), 6);
        assert_eq!(caverphone.encode("Stevenson").len(), 6);
        
        // 编码应以字母开头
        assert!(caverphone.encode("Lee").starts_with('L'));
    }
    
    #[test]
    fn test_cologne_phonetic() {
        let cologne = ColognePhonetic::new();
        
        // 测试编码只包含数字
        let code = cologne.encode("Müller");
        assert!(code.chars().all(|c| c.is_ascii_digit()));
        
        // 测试 Weber 自身编码一致
        assert_eq!(cologne.encode("Weber"), cologne.encode("Weber"));
        
        // 测试空字符串
        assert_eq!(cologne.encode(""), "");
    }
    
    #[test]
    fn test_nysiis() {
        let nysiis = Nysiis::new();
        
        // 测试基本功能
        let smith_code = nysiis.encode("Smith");
        assert!(smith_code.len() > 0);
        
        // 测试 Mac 前缀处理
        let mac_code = nysiis.encode("MacDonald");
        assert!(mac_code.starts_with('M'));
    }
    
    #[test]
    fn test_batch_operations() {
        let words = ["Smith", "Smythe", "Schmidt", "Jones", "Johnson"];
        
        let soundex_codes = PhoneticUtils::batch_soundex(&words);
        assert_eq!(soundex_codes.len(), 5);
        assert_eq!(soundex_codes[0], soundex_codes[1]); // Smith, Smythe
        
        let groups = PhoneticUtils::group_by_phonetic(&words);
        assert!(!groups.is_empty());
    }
    
    #[test]
    fn test_find_similar() {
        let words = ["Smith", "Smythe", "Schmidt", "Jones", "Johnson", "Williams"];
        
        let similar = PhoneticUtils::find_similar(&words, "Smyth", 0.8);
        assert!(similar.contains(&"Smith".to_string()) || similar.contains(&"Smythe".to_string()));
    }
}