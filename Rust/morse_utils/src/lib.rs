//! Morse code encoding and decoding utilities
//!
//! This crate provides tools for encoding text to Morse code and decoding
//! Morse code back to text, with customizable timing parameters.

use std::collections::HashMap;

/// Error types for Morse code operations
#[derive(Debug, Clone, PartialEq)]
pub enum MorseError {
    /// Invalid character encountered during encoding
    InvalidCharacter(char),
    /// Invalid Morse symbol encountered during decoding
    InvalidSymbol(String),
    /// Empty input provided
    EmptyInput,
}

impl std::fmt::Display for MorseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MorseError::InvalidCharacter(c) => write!(f, "Invalid character for Morse encoding: '{}'", c),
            MorseError::InvalidSymbol(s) => write!(f, "Invalid Morse symbol: '{}'", s),
            MorseError::EmptyInput => write!(f, "Empty input provided"),
        }
    }
}

impl std::error::Error for MorseError {}

/// Configuration for Morse code timing parameters
#[derive(Debug, Clone, Copy)]
pub struct MorseConfig {
    /// Duration of a dot in milliseconds
    pub dot_duration_ms: u32,
    /// Duration of a dash in milliseconds (typically 3x dot)
    pub dash_duration_ms: u32,
    /// Gap between symbols within a character (1x dot)
    pub symbol_gap_ms: u32,
    /// Gap between characters (3x dot)
    pub char_gap_ms: u32,
    /// Gap between words (7x dot)
    pub word_gap_ms: u32,
}

impl Default for MorseConfig {
    fn default() -> Self {
        Self {
            dot_duration_ms: 60,
            dash_duration_ms: 180,
            symbol_gap_ms: 60,
            char_gap_ms: 180,
            word_gap_ms: 420,
        }
    }
}

impl MorseConfig {
    /// Create a new config with a standard dot duration
    pub fn new(dot_duration_ms: u32) -> Self {
        Self {
            dot_duration_ms,
            dash_duration_ms: dot_duration_ms * 3,
            symbol_gap_ms: dot_duration_ms,
            char_gap_ms: dot_duration_ms * 3,
            word_gap_ms: dot_duration_ms * 7,
        }
    }
}

/// Standard Morse code lookup table
const MORSE_CODE: &[(&str, &str); 53] = &[
    // Letters
    ("A", ".-"), ("B", "-..."), ("C", "-.-."), ("D", "-.."),
    ("E", "."), ("F", "..-."), ("G", "--."), ("H", "...."),
    ("I", ".."), ("J", ".---"), ("K", "-.-"), ("L", ".-.."),
    ("M", "--"), ("N", "-."), ("O", "---"), ("P", ".--."),
    ("Q", "--.-"), ("R", ".-."), ("S", "..."), ("T", "-"),
    ("U", "..-"), ("V", "...-"), ("W", ".--"), ("X", "-..-"),
    ("Y", "-.--"), ("Z", "--.."),
    // Numbers
    ("0", "-----"), ("1", ".----"), ("2", "..---"), ("3", "...--"),
    ("4", "....-"), ("5", "....."), ("6", "-...."), ("7", "--..."),
    ("8", "---.."), ("9", "----."),
    // Punctuation
    (".", ".-.-.-"), (",", "--..--"), ("?", "..--.."),
    ("'", ".----."), ("!", "-.-.--"), ("/", "-..-."),
    ("(", "-.--."), (")", "-.--.-"), ("&", ".-..."),
    (":", "---..."), (";", "-.-.-."), ("=", "-...-"),
    ("+", ".-.-."), ("-", "-....-"), ("_", "..--.-"),
    ("\"", ".-..-."), ("@", ".--.-."),
];

/// Builds the encoding map from char to Morse code
fn build_encode_map() -> HashMap<char, &'static str> {
    MORSE_CODE
        .iter()
        .map(|(c, m)| (c.chars().next().unwrap(), *m))
        .collect()
}

/// Builds the decoding map from Morse code to char
fn build_decode_map() -> HashMap<&'static str, char> {
    MORSE_CODE
        .iter()
        .map(|(c, m)| (*m, c.chars().next().unwrap()))
        .collect()
}

/// Morse code encoder
pub struct MorseEncoder {
    config: MorseConfig,
    encode_map: HashMap<char, &'static str>,
}

impl Default for MorseEncoder {
    fn default() -> Self {
        Self::new()
    }
}

impl MorseEncoder {
    /// Create a new encoder with default configuration
    pub fn new() -> Self {
        Self {
            config: MorseConfig::default(),
            encode_map: build_encode_map(),
        }
    }

    /// Create an encoder with custom configuration
    pub fn with_config(config: MorseConfig) -> Self {
        Self {
            config,
            encode_map: build_encode_map(),
        }
    }

    /// Encode text to Morse code
    ///
    /// # Arguments
    /// * `text` - The text to encode
    ///
    /// # Returns
    /// * `Ok(String)` - The Morse code representation
    /// * `Err(MorseError)` - If encoding fails
    pub fn encode(&self, text: &str) -> Result<String, MorseError> {
        if text.is_empty() {
            return Err(MorseError::EmptyInput);
        }

        let mut result = Vec::new();
        let chars: Vec<char> = text.chars().collect();

        for c in chars.iter() {
            if *c == ' ' {
                result.push('/'.to_string());
            } else if let Some(morse) = self.encode_map.get(&c.to_ascii_uppercase()) {
                result.push(morse.to_string());
            } else {
                // Skip unknown characters or replace with placeholder
                // For this implementation, we skip them silently
                continue;
            }
        }

        Ok(result.join(" "))
    }

    /// Encode a single character to Morse code
    pub fn encode_char(&self, c: char) -> Option<&'static str> {
        self.encode_map.get(&c.to_ascii_uppercase()).copied()
    }

    /// Get the timing configuration
    pub fn config(&self) -> &MorseConfig {
        &self.config
    }

    /// Generate audio samples for Morse code
    ///
    /// Returns a vector of amplitude samples at the given sample rate
    pub fn generate_audio(&self, text: &str, sample_rate: u32, frequency: f32) -> Result<Vec<f32>, MorseError> {
        let morse = self.encode(text)?;
        let mut samples = Vec::new();

        let samples_per_ms = sample_rate as f32 / 1000.0;

        for c in morse.chars() {
            match c {
                '.' => {
                    // Dot tone
                    let dot_samples = (self.config.dot_duration_ms as f32 * samples_per_ms) as usize;
                    Self::add_tone(&mut samples, dot_samples, frequency, sample_rate);
                    // Symbol gap
                    let gap_samples = (self.config.symbol_gap_ms as f32 * samples_per_ms) as usize;
                    Self::add_silence(&mut samples, gap_samples);
                }
                '-' => {
                    // Dash tone
                    let dash_samples = (self.config.dash_duration_ms as f32 * samples_per_ms) as usize;
                    Self::add_tone(&mut samples, dash_samples, frequency, sample_rate);
                    // Symbol gap
                    let gap_samples = (self.config.symbol_gap_ms as f32 * samples_per_ms) as usize;
                    Self::add_silence(&mut samples, gap_samples);
                }
                ' ' => {
                    // Character gap (minus the symbol gap already added)
                    let char_gap_samples = (self.config.char_gap_ms as f32 * samples_per_ms) as usize;
                    Self::add_silence(&mut samples, char_gap_samples);
                }
                '/' => {
                    // Word gap
                    let word_gap_samples = (self.config.word_gap_ms as f32 * samples_per_ms) as usize;
                    Self::add_silence(&mut samples, word_gap_samples);
                }
                _ => {}
            }
        }

        Ok(samples)
    }

    fn add_tone(samples: &mut Vec<f32>, num_samples: usize, frequency: f32, sample_rate: u32) {
        for i in 0..num_samples {
            let t = i as f32 / sample_rate as f32;
            // Simple sine wave with envelope
            let envelope = 1.0 - (i as f32 / num_samples as f32 * 0.1); // Simple decay
            let sample = envelope * (2.0 * std::f32::consts::PI * frequency * t).sin();
            samples.push(sample);
        }
    }

    fn add_silence(samples: &mut Vec<f32>, num_samples: usize) {
        for _ in 0..num_samples {
            samples.push(0.0);
        }
    }
}

/// Morse code decoder
pub struct MorseDecoder {
    decode_map: HashMap<&'static str, char>,
}

impl Default for MorseDecoder {
    fn default() -> Self {
        Self::new()
    }
}

impl MorseDecoder {
    /// Create a new decoder
    pub fn new() -> Self {
        Self {
            decode_map: build_decode_map(),
        }
    }

    /// Decode Morse code to text
    ///
    /// # Arguments
    /// * `morse` - The Morse code string (dots, dashes, spaces, and slashes)
    ///
    /// # Returns
    /// * `Ok(String)` - The decoded text
    /// * `Err(MorseError)` - If decoding fails
    pub fn decode(&self, morse: &str) -> Result<String, MorseError> {
        if morse.trim().is_empty() {
            return Err(MorseError::EmptyInput);
        }

        let mut result = String::new();
        let words: Vec<&str> = morse.split('/').collect();

        for (word_idx, word) in words.iter().enumerate() {
            if word_idx > 0 {
                result.push(' ');
            }

            let chars: Vec<&str> = word.split_whitespace().collect();
            for symbol in chars {
                if let Some(&c) = self.decode_map.get(symbol) {
                    result.push(c);
                } else {
                    return Err(MorseError::InvalidSymbol(symbol.to_string()));
                }
            }
        }

        Ok(result)
    }

    /// Decode a single Morse symbol to a character
    pub fn decode_symbol(&self, symbol: &str) -> Option<char> {
        self.decode_map.get(symbol).copied()
    }

    /// Check if a symbol is valid Morse code
    pub fn is_valid_symbol(&self, symbol: &str) -> bool {
        self.decode_map.contains_key(symbol)
    }
}

/// Convenience function to encode text to Morse code
pub fn encode(text: &str) -> Result<String, MorseError> {
    MorseEncoder::new().encode(text)
}

/// Convenience function to decode Morse code to text
pub fn decode(morse: &str) -> Result<String, MorseError> {
    MorseDecoder::new().decode(morse)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_basic() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode("SOS").unwrap(), "... --- ...");
        assert_eq!(encoder.encode("A").unwrap(), ".-");
        assert_eq!(encoder.encode("HELLO").unwrap(), ".... . .-.. .-.. ---");
    }

    #[test]
    fn test_encode_with_space() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode("HELLO WORLD").unwrap(), ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");
    }

    #[test]
    fn test_encode_numbers() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode("123").unwrap(), ".---- ..--- ...--");
        assert_eq!(encoder.encode("SOS 123").unwrap(), "... --- ... / .---- ..--- ...--");
    }

    #[test]
    fn test_encode_lowercase() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode("hello").unwrap(), ".... . .-.. .-.. ---");
    }

    #[test]
    fn test_encode_empty() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode(""), Err(MorseError::EmptyInput));
    }

    #[test]
    fn test_decode_basic() {
        let decoder = MorseDecoder::new();
        assert_eq!(decoder.decode("... --- ...").unwrap(), "SOS");
        assert_eq!(decoder.decode(".-").unwrap(), "A");
        assert_eq!(decoder.decode(".... . .-.. .-.. ---").unwrap(), "HELLO");
    }

    #[test]
    fn test_decode_with_slash() {
        let decoder = MorseDecoder::new();
        assert_eq!(
            decoder.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -..").unwrap(),
            "HELLO WORLD"
        );
    }

    #[test]
    fn test_decode_empty() {
        let decoder = MorseDecoder::new();
        assert_eq!(decoder.decode(""), Err(MorseError::EmptyInput));
        assert_eq!(decoder.decode("   "), Err(MorseError::EmptyInput));
    }

    #[test]
    fn test_decode_invalid_symbol() {
        let decoder = MorseDecoder::new();
        assert!(matches!(
            decoder.decode("... INVALID ..."),
            Err(MorseError::InvalidSymbol(_))
        ));
    }

    #[test]
    fn test_roundtrip() {
        let encoder = MorseEncoder::new();
        let decoder = MorseDecoder::new();
        
        let original = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
        let encoded = encoder.encode(original).unwrap();
        let decoded = decoder.decode(&encoded).unwrap();
        assert_eq!(decoded, original);
    }

    #[test]
    fn test_encode_char() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode_char('A'), Some(".-"));
        assert_eq!(encoder.encode_char('a'), Some(".-"));
        assert_eq!(encoder.encode_char('Z'), Some("--.."));
        assert_eq!(encoder.encode_char('0'), Some("-----"));
        assert_eq!(encoder.encode_char('@'), Some(".--.-."));
    }

    #[test]
    fn test_decode_symbol() {
        let decoder = MorseDecoder::new();
        assert_eq!(decoder.decode_symbol(".-"), Some('A'));
        assert_eq!(decoder.decode_symbol("--.."), Some('Z'));
        assert_eq!(decoder.decode_symbol("-----"), Some('0'));
        assert_eq!(decoder.decode_symbol("invalid"), None);
    }

    #[test]
    fn test_config() {
        let config = MorseConfig::new(100);
        assert_eq!(config.dot_duration_ms, 100);
        assert_eq!(config.dash_duration_ms, 300);
        assert_eq!(config.symbol_gap_ms, 100);
        assert_eq!(config.char_gap_ms, 300);
        assert_eq!(config.word_gap_ms, 700);
    }

    #[test]
    fn test_convenience_functions() {
        assert_eq!(encode("SOS").unwrap(), "... --- ...");
        assert_eq!(decode("... --- ...").unwrap(), "SOS");
    }

    #[test]
    fn test_punctuation() {
        let encoder = MorseEncoder::new();
        assert_eq!(encoder.encode(".").unwrap(), ".-.-.-");
        assert_eq!(encoder.encode(",").unwrap(), "--..--");
        assert_eq!(encoder.encode("?").unwrap(), "..--..");
    }

    #[test]
    fn test_generate_audio() {
        let encoder = MorseEncoder::new();
        let samples = encoder.generate_audio("SOS", 8000, 600.0).unwrap();
        // Should have generated some samples
        assert!(!samples.is_empty());
        // Check that we have both positive and negative samples (sine wave)
        assert!(samples.iter().any(|&s| s > 0.0));
        assert!(samples.iter().any(|&s| s < 0.0));
    }

    #[test]
    fn test_is_valid_symbol() {
        let decoder = MorseDecoder::new();
        assert!(decoder.is_valid_symbol(".-"));
        assert!(decoder.is_valid_symbol("--.."));
        assert!(!decoder.is_valid_symbol("abc"));
    }
}