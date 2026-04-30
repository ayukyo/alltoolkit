//! Morse Code Utilities
//! 
//! A zero-dependency Rust library for encoding and decoding Morse code.
//! 
//! # Features
//! - Text to Morse code encoding
//! - Morse code to text decoding
//! - Support for letters, numbers, and common punctuation
//! - Customizable delimiters
//! - Audio signal generation (beep patterns)

use std::collections::HashMap;

/// Morse code character mapping for letters A-Z
const LETTERS: &[(&str, &str)] = &[
    ("A", ".-"), ("B", "-..."), ("C", "-.-."), ("D", "-.."), ("E", "."),
    ("F", "..-."), ("G", "--."), ("H", "...."), ("I", ".."), ("J", ".---"),
    ("K", "-.-"), ("L", ".-.."), ("M", "--"), ("N", "-."), ("O", "---"),
    ("P", ".--."), ("Q", "--.-"), ("R", ".-."), ("S", "..."), ("T", "-"),
    ("U", "..-"), ("V", "...-"), ("W", ".--"), ("X", "-..-"), ("Y", "-.--"),
    ("Z", "--.."),
];

/// Morse code character mapping for digits 0-9
const DIGITS: &[(&str, &str)] = &[
    ("0", "-----"), ("1", ".----"), ("2", "..---"), ("3", "...--"), ("4", "....-"),
    ("5", "....."), ("6", "-...."), ("7", "--..."), ("8", "---.."), ("9", "----."),
];

/// Morse code character mapping for common punctuation
const PUNCTUATION: &[(&str, &str)] = &[
    (".", ".-.-.-"), (",", "--..--"), ("?", "..--.."), ("'", ".----."),
    ("!", "-.-.--"), ("/", "-..-."), ("(", "-.--."), (")", "-.--.-"),
    ("&", ".-..."), (":", "---..."), (";", "-.-.-."), ("=", "-...-"),
    ("+", ".-.-."), ("-", "-....-"), ("_", "..--.-"), ("\"", ".-..-."),
    ("$", "...-..-"), ("@", ".--.-."),
];

/// Morse code encoder and decoder
pub struct MorseCode {
    char_to_morse: HashMap<char, String>,
    morse_to_char: HashMap<String, char>,
}

impl Default for MorseCode {
    fn default() -> Self {
        Self::new()
    }
}

impl MorseCode {
    /// Create a new MorseCode instance with standard mappings
    pub fn new() -> Self {
        let mut char_to_morse = HashMap::new();
        let mut morse_to_char = HashMap::new();

        // Add letters
        for (c, m) in LETTERS {
            let upper = c.chars().next().unwrap();
            char_to_morse.insert(upper, m.to_string());
            char_to_morse.insert(upper.to_ascii_lowercase(), m.to_string());
            morse_to_char.insert(m.to_string(), upper);
        }

        // Add digits
        for (c, m) in DIGITS {
            let digit = c.chars().next().unwrap();
            char_to_morse.insert(digit, m.to_string());
            morse_to_char.insert(m.to_string(), digit);
        }

        // Add punctuation
        for (c, m) in PUNCTUATION {
            let punct = c.chars().next().unwrap();
            char_to_morse.insert(punct, m.to_string());
            morse_to_char.insert(m.to_string(), punct);
        }

        MorseCode { char_to_morse, morse_to_char }
    }

    /// Encode text to Morse code
    /// 
    /// # Arguments
    /// * `text` - The text to encode
    /// * `letter_delimiter` - Delimiter between letters (default: space)
    /// * `word_delimiter` - Delimiter between words (default: "/")
    /// 
    /// # Returns
    /// Encoded Morse code string
    /// 
    /// # Example
    /// ```
    /// use morse_code_utils::MorseCode;
    /// let morse = MorseCode::new();
    /// let encoded = morse.encode("HELLO WORLD", " ", " / ");
    /// assert_eq!(encoded, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");
    /// ```
    pub fn encode(&self, text: &str, letter_delimiter: &str, word_delimiter: &str) -> String {
        let words: Vec<String> = text.split_whitespace()
            .map(|word| {
                word.chars()
                    .filter_map(|c| self.char_to_morse.get(&c).map(|s| s.as_str()))
                    .collect::<Vec<&str>>()
                    .join(letter_delimiter)
            })
            .collect();

        words.join(word_delimiter)
    }

    /// Encode text to Morse code with default delimiters (space between letters, "/" between words)
    pub fn encode_default(&self, text: &str) -> String {
        self.encode(text, " ", " / ")
    }

    /// Decode Morse code to text
    /// 
    /// # Arguments
    /// * `morse` - The Morse code to decode
    /// * `letter_delimiter` - Delimiter between letters (default: space)
    /// * `word_delimiter` - Delimiter between words (default: "/")
    /// 
    /// # Returns
    /// Decoded text string (uppercase)
    /// 
    /// # Example
    /// ```
    /// use morse_code_utils::MorseCode;
    /// let morse = MorseCode::new();
    /// let decoded = morse.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -..", " ", "/");
    /// assert_eq!(decoded, "HELLO WORLD");
    /// ```
    pub fn decode(&self, morse: &str, letter_delimiter: &str, word_delimiter: &str) -> String {
        let words: Vec<String> = morse.split(word_delimiter)
            .map(|word| {
                word.split(letter_delimiter)
                    .filter_map(|code| {
                        let trimmed = code.trim();
                        if trimmed.is_empty() {
                            None
                        } else {
                            self.morse_to_char.get(trimmed).copied()
                        }
                    })
                    .collect::<String>()
            })
            .collect();

        words.join(" ")
    }

    /// Decode Morse code with default delimiters (space between letters, "/" between words)
    pub fn decode_default(&self, morse: &str) -> String {
        self.decode(morse, " ", "/")
    }

    /// Check if a character can be encoded to Morse code
    pub fn can_encode(&self, c: char) -> bool {
        self.char_to_morse.contains_key(&c)
    }

    /// Check if a Morse code sequence is valid
    pub fn is_valid_morse(&self, code: &str) -> bool {
        code.chars().all(|c| c == '.' || c == '-' || c == ' ' || c == '/')
    }

    /// Get the Morse code for a single character
    pub fn get_morse(&self, c: char) -> Option<&String> {
        self.char_to_morse.get(&c)
    }

    /// Get the character for a Morse code sequence
    pub fn get_char(&self, code: &str) -> Option<&char> {
        self.morse_to_char.get(code)
    }
}

/// Audio signal representation for Morse code
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Signal {
    /// Short signal (dit) - typically 1 unit duration
    Dit,
    /// Long signal (dah) - typically 3 units duration
    Dah,
    /// Gap between signals in same letter - 1 unit duration
    IntraCharGap,
    /// Gap between letters - 3 units duration
    LetterGap,
    /// Gap between words - 7 units duration
    WordGap,
}

/// Generate audio signals from Morse code
/// 
/// # Arguments
/// * `morse` - Morse code string (dots, dashes, spaces, and slashes)
/// 
/// # Returns
/// Vector of signals representing the audio pattern
pub fn to_signals(morse: &str) -> Vec<Signal> {
    let mut signals = Vec::new();
    let chars: Vec<char> = morse.chars().collect();

    for (i, &c) in chars.iter().enumerate() {
        match c {
            '.' => {
                signals.push(Signal::Dit);
                // Add intra-character gap if next char is not space/slash/end
                if i + 1 < chars.len() {
                    let next = chars[i + 1];
                    if next != ' ' && next != '/' {
                        signals.push(Signal::IntraCharGap);
                    }
                }
            }
            '-' => {
                signals.push(Signal::Dah);
                if i + 1 < chars.len() {
                    let next = chars[i + 1];
                    if next != ' ' && next != '/' {
                        signals.push(Signal::IntraCharGap);
                    }
                }
            }
            ' ' => {
                // Check if it's part of " / " (word separator)
                if i > 0 && i + 1 < chars.len() && chars[i - 1] == '/' && chars[i + 1] == '/' {
                    // Already handled by /
                } else if i > 0 && chars[i - 1] == '/' {
                    // Space after / - skip
                } else if i + 1 < chars.len() && chars[i + 1] == '/' {
                    // Space before / - skip
                } else {
                    signals.push(Signal::LetterGap);
                }
            }
            '/' => {
                signals.push(Signal::WordGap);
            }
            _ => {}
        }
    }

    signals
}

/// Convert signals to a duration pattern (in arbitrary units)
/// 
/// Standard timing:
/// - Dit = 1 unit
/// - Dah = 3 units  
/// - Intra-char gap = 1 unit
/// - Letter gap = 3 units
/// - Word gap = 7 units
pub fn to_durations(signals: &[Signal]) -> Vec<(Signal, u32)> {
    signals.iter().map(|s| {
        match s {
            Signal::Dit => (*s, 1),
            Signal::Dah => (*s, 3),
            Signal::IntraCharGap => (*s, 1),
            Signal::LetterGap => (*s, 3),
            Signal::WordGap => (*s, 7),
        }
    }).collect()
}

/// Convert Morse code to a binary string representation
/// 
/// Uses '1' for signal (on) and '0' for gap (off)
/// This is useful for signal processing or visualization
pub fn to_binary(morse: &str) -> String {
    let signals = to_signals(morse);
    let durations = to_durations(&signals);
    
    durations.iter().map(|(signal, duration)| {
        let c = match signal {
            Signal::Dit | Signal::Dah => '1',
            Signal::IntraCharGap | Signal::LetterGap | Signal::WordGap => '0',
        };
        std::iter::repeat(c).take(*duration as usize).collect::<String>()
    }).collect()
}

/// Convert binary representation back to Morse code
pub fn from_binary(binary: &str) -> Option<String> {
    let mut morse = String::new();
    let mut i = 0;
    let chars: Vec<char> = binary.chars().collect();

    while i < chars.len() {
        // Count consecutive 1s (signal)
        let mut ones = 0;
        while i < chars.len() && chars[i] == '1' {
            ones += 1;
            i += 1;
        }

        // Determine if dit or dah
        if ones > 0 {
            if ones <= 2 {
                morse.push('.');
            } else {
                morse.push('-');
            }
        }

        // Count consecutive 0s (gap)
        let mut zeros = 0;
        while i < chars.len() && chars[i] == '0' {
            zeros += 1;
            i += 1;
        }

        // Determine gap type
        if zeros >= 7 {
            morse.push_str(" / ");
        } else if zeros >= 3 {
            morse.push(' ');
        } else if zeros == 0 && i < chars.len() {
            // No gap between characters in same letter - already handled
        }
    }

    Some(morse)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_letters() {
        let morse = MorseCode::new();
        assert_eq!(morse.encode_default("SOS"), "... --- ...");
        assert_eq!(morse.encode_default("HELLO"), ".... . .-.. .-.. ---");
    }

    #[test]
    fn test_encode_with_spaces() {
        let morse = MorseCode::new();
        assert_eq!(morse.encode_default("HELLO WORLD"), ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");
    }

    #[test]
    fn test_encode_numbers() {
        let morse = MorseCode::new();
        assert_eq!(morse.encode_default("123"), ".---- ..--- ...--");
        assert_eq!(morse.encode_default("911"), "----. .---- .----");
    }

    #[test]
    fn test_encode_punctuation() {
        let morse = MorseCode::new();
        assert_eq!(morse.encode_default("HELLO!"), ".... . .-.. .-.. --- -.-.--");
        assert_eq!(morse.encode_default("OK."), "--- -.- .-.-.-");
    }

    #[test]
    fn test_decode_letters() {
        let morse = MorseCode::new();
        assert_eq!(morse.decode_default("... --- ..."), "SOS");
        assert_eq!(morse.decode_default(".... . .-.. .-.. ---"), "HELLO");
    }

    #[test]
    fn test_decode_with_spaces() {
        let morse = MorseCode::new();
        assert_eq!(morse.decode_default(".... . .-.. .-.. --- / .-- --- .-. .-.. -.."), "HELLO WORLD");
    }

    #[test]
    fn test_decode_numbers() {
        let morse = MorseCode::new();
        assert_eq!(morse.decode_default(".---- ..--- ...--"), "123");
        assert_eq!(morse.decode_default("----. .---- .----"), "911");
    }

    #[test]
    fn test_roundtrip() {
        let morse = MorseCode::new();
        let texts = vec![
            "SOS",
            "HELLO WORLD",
            "MORSE CODE",
            "TESTING 123",
            "RUST LANG",
        ];

        for text in texts {
            let encoded = morse.encode_default(text);
            let decoded = morse.decode_default(&encoded);
            assert_eq!(decoded, text);
        }
    }

    #[test]
    fn test_case_insensitive() {
        let morse = MorseCode::new();
        assert_eq!(morse.encode_default("hello"), morse.encode_default("HELLO"));
        assert_eq!(morse.encode_default("HeLLo"), morse.encode_default("HELLO"));
    }

    #[test]
    fn test_can_encode() {
        let morse = MorseCode::new();
        assert!(morse.can_encode('A'));
        assert!(morse.can_encode('a'));
        assert!(morse.can_encode('1'));
        assert!(morse.can_encode('!'));
        assert!(morse.can_encode('@'));
        assert!(!morse.can_encode('~'));
        assert!(!morse.can_encode('#'));
    }

    #[test]
    fn test_is_valid_morse() {
        let morse = MorseCode::new();
        assert!(morse.is_valid_morse("... --- ..."));
        assert!(morse.is_valid_morse(".- -... -.-."));
        assert!(morse.is_valid_morse(".... / .-"));
        assert!(!morse.is_valid_morse("abc"));
        assert!(!morse.is_valid_morse("...x---"));
    }

    #[test]
    fn test_get_morse() {
        let morse = MorseCode::new();
        assert_eq!(morse.get_morse('A'), Some(&".-".to_string()));
        assert_eq!(morse.get_morse('a'), Some(&".-".to_string()));
        assert_eq!(morse.get_morse('0'), Some(&"-----".to_string()));
        assert_eq!(morse.get_morse('~'), None);
    }

    #[test]
    fn test_get_char() {
        let morse = MorseCode::new();
        assert_eq!(morse.get_char(".-"), Some(&'A'));
        assert_eq!(morse.get_char("-----"), Some(&'0'));
        assert_eq!(morse.get_char(".-.-.-"), Some(&'.'));
        assert_eq!(morse.get_char("......"), None);
    }

    #[test]
    fn test_to_signals() {
        let signals = to_signals(".-");
        assert_eq!(signals, vec![
            Signal::Dit,
            Signal::IntraCharGap,
            Signal::Dah,
        ]);
    }

    #[test]
    fn test_to_signals_with_letter_gap() {
        let signals = to_signals(".- .");
        assert_eq!(signals, vec![
            Signal::Dit,
            Signal::IntraCharGap,
            Signal::Dah,
            Signal::LetterGap,
            Signal::Dit,
        ]);
    }

    #[test]
    fn test_to_durations() {
        let signals = vec![Signal::Dit, Signal::Dah, Signal::LetterGap];
        let durations = to_durations(&signals);
        assert_eq!(durations, vec![
            (Signal::Dit, 1),
            (Signal::Dah, 3),
            (Signal::LetterGap, 3),
        ]);
    }

    #[test]
    fn test_to_binary() {
        let binary = to_binary(".-");
        // Dit (1) + IntraCharGap (0) + Dah (111)
        assert_eq!(binary, "10111");
    }

    #[test]
    fn test_from_binary() {
        // 10111 = Dit + gap + Dah
        let morse = from_binary("10111").unwrap();
        assert_eq!(morse, ".-");
    }

    #[test]
    fn test_binary_roundtrip() {
        let morse_code = ".... . .-.. .-.. ---";
        let binary = to_binary(morse_code);
        let restored = from_binary(&binary).unwrap();
        // Note: restored may have different spacing, but signals are the same
        let morse_decoder = MorseCode::new();
        assert_eq!(
            morse_decoder.decode(morse_code, " ", "/"),
            morse_decoder.decode(&restored, " ", "/")
        );
    }

    #[test]
    fn test_sos_signal() {
        let morse = MorseCode::new();
        let encoded = morse.encode_default("SOS");
        let signals = to_signals(&encoded);
        
        // SOS = ... --- ...
        // Should have: dit, gap, dit, gap, dit, letter_gap, dah, gap, dah, gap, dah, letter_gap, dit, gap, dit, gap, dit
        assert!(signals.len() > 10);
        
        let durations = to_durations(&signals);
        let total_time: u32 = durations.iter().map(|(_, d)| d).sum();
        
        // SOS timing: (1+1+1+1+1+3+1) + (1+1+3+1+3+1+3+1+1) + (1+1+3+1+1+1+1+1) = etc
        // Actually: ... --- ... = 
        // Dits: 3 dits * 1 = 3
        // IntraCharGaps: 2 * 1 = 2  
        // LetterGap: 2 * 3 = 6
        // Dahs: 3 dahs * 3 = 9
        // etc.
        assert!(total_time > 0);
    }

    #[test]
    fn test_empty_input() {
        let morse = MorseCode::new();
        assert_eq!(morse.encode_default(""), "");
        assert_eq!(morse.decode_default(""), "");
    }

    #[test]
    fn test_whitespace_handling() {
        let morse = MorseCode::new();
        // Multiple spaces should be treated as single word separator
        assert_eq!(morse.encode_default("HELLO   WORLD"), ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");
        // Leading/trailing spaces should be trimmed
        assert_eq!(morse.encode_default("  HELLO  "), ".... . .-.. .-.. ---");
    }

    #[test]
    fn test_unknown_chars() {
        let morse = MorseCode::new();
        // Unknown characters should be skipped
        let encoded = morse.encode_default("HE~LLO");
        // ~ is not encodable, should be skipped
        assert_eq!(encoded, ".... . .-.. .-.. ---");
    }
}