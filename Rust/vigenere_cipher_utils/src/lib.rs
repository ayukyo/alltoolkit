//! Vigenère Cipher Utilities
//! 
//! A comprehensive implementation of the Vigenère cipher, a classic polyalphabetic
//! substitution cipher that uses a keyword to encrypt and decrypt messages.
//! 
//! # Features
//! 
//! - Encrypt and decrypt text using the Vigenère cipher
//! - Support for custom alphabets
//! - Configurable handling of non-alphabetic characters
//! - Autokey variant support
//! - Key validation and analysis
//! 
//! # Example
//! 
//! ```rust
//! use vigenere_cipher_utils::{encrypt, decrypt};
//! 
//! let plaintext = "HELLO WORLD";
//! let key = "KEY";
//! 
//! let ciphertext = encrypt(plaintext, key).unwrap();
//! let decrypted = decrypt(&ciphertext, key).unwrap();
//! 
//! assert_eq!(decrypted, plaintext);
//! ```

use std::fmt;

/// Default alphabet used for Vigenère cipher operations
pub const DEFAULT_ALPHABET: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

/// Error types for Vigenère cipher operations
#[derive(Debug, Clone, PartialEq)]
pub enum VigenereError {
    /// The provided key is empty or contains no valid characters
    EmptyKey,
    /// The provided alphabet is empty or contains duplicate characters
    InvalidAlphabet,
    /// The key contains characters not in the alphabet
    KeyContainsInvalidChars(String),
}

impl fmt::Display for VigenereError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            VigenereError::EmptyKey => write!(f, "Key cannot be empty"),
            VigenereError::InvalidAlphabet => write!(f, "Alphabet is invalid (empty or has duplicates)"),
            VigenereError::KeyContainsInvalidChars(c) => {
                write!(f, "Key contains invalid characters: {}", c)
            }
        }
    }
}

impl std::error::Error for VigenereError {}

/// Configuration options for Vigenère cipher operations
#[derive(Debug, Clone)]
pub struct VigenereConfig {
    /// The alphabet to use for encryption/decryption
    pub alphabet: String,
    /// Whether to preserve non-alphabet characters in the output
    pub preserve_non_alpha: bool,
    /// Whether to convert output to uppercase
    pub uppercase_output: bool,
    /// Whether to use autokey mode
    pub autokey: bool,
}

impl Default for VigenereConfig {
    fn default() -> Self {
        VigenereConfig {
            alphabet: DEFAULT_ALPHABET.to_string(),
            preserve_non_alpha: true,
            uppercase_output: true,
            autokey: false,
        }
    }
}

impl VigenereConfig {
    /// Create a new configuration with a custom alphabet
    pub fn with_alphabet(alphabet: &str) -> Result<Self, VigenereError> {
        let config = VigenereConfig {
            alphabet: alphabet.to_uppercase(),
            ..Default::default()
        };
        config.validate_alphabet()?;
        Ok(config)
    }

    /// Validate the alphabet
    fn validate_alphabet(&self) -> Result<(), VigenereError> {
        if self.alphabet.is_empty() {
            return Err(VigenereError::InvalidAlphabet);
        }
        
        let mut seen = std::collections::HashSet::new();
        for c in self.alphabet.chars() {
            if !seen.insert(c) {
                return Err(VigenereError::InvalidAlphabet);
            }
        }
        
        Ok(())
    }
}

/// Validate and normalize a key
fn normalize_key(key: &str, alphabet: &str) -> Result<String, VigenereError> {
    let normalized: String = key.to_uppercase()
        .chars()
        .filter(|c| alphabet.contains(*c))
        .collect();
    
    if normalized.is_empty() {
        return Err(VigenereError::EmptyKey);
    }
    
    // Check if any non-alphabet chars were in the original key
    let invalid_chars: String = key.to_uppercase()
        .chars()
        .filter(|c| !alphabet.contains(*c) && c.is_alphabetic())
        .collect();
    
    if !invalid_chars.is_empty() {
        return Err(VigenereError::KeyContainsInvalidChars(invalid_chars));
    }
    
    Ok(normalized)
}

/// Encrypt plaintext using the Vigenère cipher with default configuration
/// 
/// # Arguments
/// 
/// * `plaintext` - The text to encrypt
/// * `key` - The encryption key
/// 
/// # Returns
/// 
/// The encrypted ciphertext
/// 
/// # Errors
/// 
/// Returns an error if the key is empty or invalid
/// 
/// # Example
/// 
/// ```rust
/// use vigenere_cipher_utils::encrypt;
/// 
/// let ciphertext = encrypt("HELLO", "KEY").unwrap();
/// assert_eq!(ciphertext, "RIJVS");
/// ```
pub fn encrypt(plaintext: &str, key: &str) -> Result<String, VigenereError> {
    encrypt_with_config(plaintext, key, &VigenereConfig::default())
}

/// Encrypt plaintext using the Vigenère cipher with custom configuration
/// 
/// # Arguments
/// 
/// * `plaintext` - The text to encrypt
/// * `key` - The encryption key
/// * `config` - Configuration options
/// 
/// # Returns
/// 
/// The encrypted ciphertext
pub fn encrypt_with_config(
    plaintext: &str,
    key: &str,
    config: &VigenereConfig,
) -> Result<String, VigenereError> {
    config.validate_alphabet()?;
    let normalized_key = normalize_key(key, &config.alphabet)?;
    
    if normalized_key.is_empty() {
        return Err(VigenereError::EmptyKey);
    }
    
    let alphabet: Vec<char> = config.alphabet.chars().collect();
    let alphabet_len = alphabet.len();
    let alpha_map: std::collections::HashMap<char, usize> = alphabet
        .iter()
        .enumerate()
        .map(|(i, &c)| (c, i))
        .collect();
    
    let key_chars: Vec<usize> = normalized_key
        .chars()
        .filter_map(|c| alpha_map.get(&c).copied())
        .collect();
    
    // In autokey mode, extend the key with the plaintext
    let effective_key = if config.autokey {
        let plaintext_chars: Vec<char> = plaintext
            .to_uppercase()
            .chars()
            .filter(|c| alphabet.contains(c))
            .collect();
        
        let mut extended = key_chars.clone();
        for c in plaintext_chars.iter() {
            if let Some(&idx) = alpha_map.get(c) {
                extended.push(idx);
            }
        }
        extended
    } else {
        key_chars
    };
    
    let mut result = String::new();
    let mut key_index = 0;
    
    for c in plaintext.chars() {
        let upper_c = c.to_uppercase().next().unwrap();
        
        if let Some(&char_idx) = alpha_map.get(&upper_c) {
            let key_idx = effective_key[key_index % effective_key.len()];
            let encrypted_idx = (char_idx + key_idx) % alphabet_len;
            
            let encrypted_char = alphabet[encrypted_idx];
            result.push(if config.uppercase_output {
                encrypted_char
            } else {
                encrypted_char.to_lowercase().next().unwrap()
            });
            
            key_index += 1;
        } else if config.preserve_non_alpha {
            result.push(c);
        }
    }
    
    Ok(result)
}

/// Decrypt ciphertext using the Vigenère cipher with default configuration
/// 
/// # Arguments
/// 
/// * `ciphertext` - The text to decrypt
/// * `key` - The decryption key
/// 
/// # Returns
/// 
/// The decrypted plaintext
/// 
/// # Errors
/// 
/// Returns an error if the key is empty or invalid
/// 
/// # Example
/// 
/// ```rust
/// use vigenere_cipher_utils::decrypt;
/// 
/// let plaintext = decrypt("RIJVS", "KEY").unwrap();
/// assert_eq!(plaintext, "HELLO");
/// ```
pub fn decrypt(ciphertext: &str, key: &str) -> Result<String, VigenereError> {
    decrypt_with_config(ciphertext, key, &VigenereConfig::default())
}

/// Decrypt ciphertext using the Vigenère cipher with custom configuration
/// 
/// # Arguments
/// 
/// * `ciphertext` - The text to decrypt
/// * `key` - The decryption key
/// * `config` - Configuration options
/// 
/// # Returns
/// 
/// The decrypted plaintext
pub fn decrypt_with_config(
    ciphertext: &str,
    key: &str,
    config: &VigenereConfig,
) -> Result<String, VigenereError> {
    config.validate_alphabet()?;
    let normalized_key = normalize_key(key, &config.alphabet)?;
    
    if normalized_key.is_empty() {
        return Err(VigenereError::EmptyKey);
    }
    
    let alphabet: Vec<char> = config.alphabet.chars().collect();
    let alphabet_len = alphabet.len();
    let alpha_map: std::collections::HashMap<char, usize> = alphabet
        .iter()
        .enumerate()
        .map(|(i, &c)| (c, i))
        .collect();
    
    let key_chars: Vec<usize> = normalized_key
        .chars()
        .filter_map(|c| alpha_map.get(&c).copied())
        .collect();
    
    // For autokey mode, we need to build the key as we decrypt
    let effective_key = key_chars.clone();
    
    let mut result = String::new();
    let mut key_index = 0;
    
    for c in ciphertext.chars() {
        let upper_c = c.to_uppercase().next().unwrap();
        
        if let Some(&char_idx) = alpha_map.get(&upper_c) {
            // Get the current key character
            let key_idx = if config.autokey {
                if key_index < key_chars.len() {
                    key_chars[key_index]
                } else {
                    // Use the already decrypted character as key
                    let prev_decrypted = result.chars()
                        .filter(|ch| {
                            let uch = ch.to_uppercase().next().unwrap();
                            alpha_map.contains_key(&uch)
                        })
                        .nth(key_index - key_chars.len())
                        .unwrap();
                    let prev_upper = prev_decrypted.to_uppercase().next().unwrap();
                    alpha_map[&prev_upper]
                }
            } else {
                effective_key[key_index % effective_key.len()]
            };
            
            let decrypted_idx = (char_idx + alphabet_len - key_idx) % alphabet_len;
            
            let decrypted_char = alphabet[decrypted_idx];
            result.push(if config.uppercase_output {
                decrypted_char
            } else {
                decrypted_char.to_lowercase().next().unwrap()
            });
            
            key_index += 1;
        } else if config.preserve_non_alpha {
            result.push(c);
        }
    }
    
    Ok(result)
}

/// A Vigenère cipher instance with pre-validated configuration
#[derive(Debug, Clone)]
pub struct VigenereCipher {
    config: VigenereConfig,
}

impl VigenereCipher {
    /// Create a new Vigenère cipher instance with default configuration
    pub fn new() -> Result<Self, VigenereError> {
        Ok(VigenereCipher {
            config: VigenereConfig::default(),
        })
    }
    
    /// Create a new Vigenère cipher instance with custom configuration
    pub fn with_config(config: VigenereConfig) -> Result<Self, VigenereError> {
        config.validate_alphabet()?;
        Ok(VigenereCipher { config })
    }
    
    /// Create a new Vigenère cipher instance with a custom alphabet
    pub fn with_alphabet(alphabet: &str) -> Result<Self, VigenereError> {
        Ok(VigenereCipher {
            config: VigenereConfig::with_alphabet(alphabet)?,
        })
    }
    
    /// Encrypt plaintext
    pub fn encrypt(&self, plaintext: &str, key: &str) -> Result<String, VigenereError> {
        encrypt_with_config(plaintext, key, &self.config)
    }
    
    /// Decrypt ciphertext
    pub fn decrypt(&self, ciphertext: &str, key: &str) -> Result<String, VigenereError> {
        decrypt_with_config(ciphertext, key, &self.config)
    }
    
    /// Get the current configuration
    pub fn config(&self) -> &VigenereConfig {
        &self.config
    }
    
    /// Estimate the key length using the Kasiski examination method
    /// 
    /// Returns a vector of likely key lengths sorted by probability
    pub fn estimate_key_length(&self, ciphertext: &str, max_length: usize) -> Vec<usize> {
        let text: String = ciphertext.to_uppercase()
            .chars()
            .filter(|c| self.config.alphabet.contains(*c))
            .collect();
        
        if text.len() < 4 {
            return vec![1];
        }
        
        // Find repeated sequences and their distances
        let mut distances: Vec<usize> = Vec::new();
        
        for seq_len in 3..=5 {
            for i in 0..text.len().saturating_sub(seq_len) {
                let seq = &text[i..i + seq_len];
                for j in (i + seq_len)..text.len().saturating_sub(seq_len) {
                    if &text[j..j + seq_len] == seq {
                        distances.push(j - i);
                    }
                }
            }
        }
        
        // Find GCD of distances to estimate key length
        let mut gcd_counts: std::collections::HashMap<usize, usize> = std::collections::HashMap::new();
        
        for &dist in &distances {
            for factor in 2..=dist.min(max_length) {
                if dist % factor == 0 {
                    *gcd_counts.entry(factor).or_insert(0) += 1;
                }
            }
        }
        
        let mut results: Vec<(usize, usize)> = gcd_counts.into_iter().collect();
        results.sort_by(|a, b| b.1.cmp(&a.1));
        
        results.into_iter()
            .take(10)
            .map(|(len, _)| len)
            .collect()
    }
    
    /// Calculate the Index of Coincidence for a text
    pub fn index_of_coincidence(&self, text: &str) -> f64 {
        let filtered: String = text.to_uppercase()
            .chars()
            .filter(|c| self.config.alphabet.contains(*c))
            .collect();
        
        let n = filtered.len();
        if n < 2 {
            return 0.0;
        }
        
        let mut freq: std::collections::HashMap<char, usize> = std::collections::HashMap::new();
        
        for c in filtered.chars() {
            *freq.entry(c).or_insert(0) += 1;
        }
        
        let sum: usize = freq.values()
            .map(|&f| f * (f - 1))
            .sum();
        
        (sum as f64) / ((n * (n - 1)) as f64)
    }
}

impl Default for VigenereCipher {
    fn default() -> Self {
        VigenereCipher::new().unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_encrypt_decrypt() {
        let plaintext = "HELLO";
        let key = "KEY";
        
        let ciphertext = encrypt(plaintext, key).unwrap();
        let decrypted = decrypt(&ciphertext, key).unwrap();
        
        assert_eq!(decrypted, plaintext);
    }
    
    #[test]
    fn test_known_ciphertext() {
        // HELLO + KEY = RIJVS
        let ciphertext = encrypt("HELLO", "KEY").unwrap();
        assert_eq!(ciphertext, "RIJVS");
    }
    
    #[test]
    fn test_decrypt_known() {
        // RIJVS - KEY = HELLO
        let plaintext = decrypt("RIJVS", "KEY").unwrap();
        assert_eq!(plaintext, "HELLO");
    }
    
    #[test]
    fn test_preserve_non_alpha() {
        let config = VigenereConfig {
            preserve_non_alpha: true,
            ..Default::default()
        };
        
        let ciphertext = encrypt_with_config("HELLO WORLD!", "KEY", &config).unwrap();
        assert!(ciphertext.contains(' '));
        assert!(ciphertext.contains('!'));
    }
    
    #[test]
    fn test_remove_non_alpha() {
        let config = VigenereConfig {
            preserve_non_alpha: false,
            ..Default::default()
        };
        
        let ciphertext = encrypt_with_config("HELLO WORLD!", "KEY", &config).unwrap();
        assert!(!ciphertext.contains(' '));
        assert!(!ciphertext.contains('!'));
    }
    
    #[test]
    fn test_empty_key() {
        let result = encrypt("HELLO", "");
        assert!(matches!(result, Err(VigenereError::EmptyKey)));
    }
    
    #[test]
    fn test_whitespace_key() {
        let result = encrypt("HELLO", "   ");
        assert!(matches!(result, Err(VigenereError::EmptyKey)));
    }
    
    #[test]
    fn test_case_insensitivity() {
        let c1 = encrypt("hello", "key").unwrap();
        let c2 = encrypt("HELLO", "KEY").unwrap();
        let c3 = encrypt("HeLLo", "KeY").unwrap();
        
        assert_eq!(c1, c2);
        assert_eq!(c2, c3);
    }
    
    #[test]
    fn test_long_text() {
        let plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
        let key = "SECRET";
        
        let ciphertext = encrypt(plaintext, key).unwrap();
        let decrypted = decrypt(&ciphertext, key).unwrap();
        
        assert_eq!(decrypted, plaintext);
    }
    
    #[test]
    fn test_cipher_instance() {
        let cipher = VigenereCipher::new().unwrap();
        
        let plaintext = "ATTACK AT DAWN";
        let key = "LEMON";
        
        let ciphertext = cipher.encrypt(plaintext, key).unwrap();
        let decrypted = cipher.decrypt(&ciphertext, key).unwrap();
        
        assert_eq!(decrypted, plaintext);
    }
    
    #[test]
    fn test_custom_alphabet() {
        let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        let cipher = VigenereCipher::with_alphabet(alphabet).unwrap();
        
        let plaintext = "TEST123";
        let key = "KEY";
        
        let ciphertext = cipher.encrypt(plaintext, key).unwrap();
        let decrypted = cipher.decrypt(&ciphertext, key).unwrap();
        
        assert_eq!(decrypted, plaintext);
    }
    
    #[test]
    fn test_autokey_mode() {
        let config = VigenereConfig {
            autokey: true,
            ..Default::default()
        };
        
        let plaintext = "ATTACKATDAWN";
        let key = "QUEENLY";
        
        let ciphertext = encrypt_with_config(plaintext, key, &config).unwrap();
        let decrypted = decrypt_with_config(&ciphertext, key, &config).unwrap();
        
        assert_eq!(decrypted, plaintext);
    }
    
    #[test]
    fn test_index_of_coincidence() {
        let cipher = VigenereCipher::new().unwrap();
        
        // English text has IC around 0.067 for long texts
        // For shorter texts, the IC can vary more
        let english_ic = cipher.index_of_coincidence(
            "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        );
        // For English text, IC should be around 0.067 (theoretical value)
        // For short texts it can vary but should still be positive
        assert!(english_ic > 0.0);
        
        // Longer English text should have IC closer to 0.067
        let long_english = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOG";
        let long_ic = cipher.index_of_coincidence(long_english);
        // For sufficiently long English text, IC should approach 0.067
        assert!(long_ic > 0.04 && long_ic < 0.10);
    }
    
    #[test]
    fn test_key_length_estimation() {
        let cipher = VigenereCipher::new().unwrap();
        
        // Create a ciphertext encrypted with a key of length 3
        let plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOG";
        let key = "KEY";
        let ciphertext = cipher.encrypt(plaintext, key).unwrap();
        
        let estimated = cipher.estimate_key_length(&ciphertext, 10);
        
        // The estimated key length should include 3
        assert!(estimated.contains(&3) || estimated.iter().any(|&l| l % 3 == 0));
    }
    
    #[test]
    fn test_single_char_key() {
        // Single char key acts like Caesar cipher
        let ciphertext = encrypt("ABC", "A").unwrap();
        assert_eq!(ciphertext, "ABC");
        
        let ciphertext = encrypt("ABC", "B").unwrap();
        assert_eq!(ciphertext, "BCD");
    }
    
    #[test]
    fn test_repeated_key_char() {
        // Key "AAAA" should not change the text
        let plaintext = "HELLO";
        let ciphertext = encrypt(plaintext, "AAAA").unwrap();
        assert_eq!(ciphertext, plaintext);
    }
    
    #[test]
    fn test_lowercase_output() {
        let config = VigenereConfig {
            uppercase_output: false,
            ..Default::default()
        };
        
        let ciphertext = encrypt_with_config("HELLO", "KEY", &config).unwrap();
        assert_eq!(ciphertext, "rijvs");
    }
    
    #[test]
    fn test_vigenere_error_display() {
        assert_eq!(
            format!("{}", VigenereError::EmptyKey),
            "Key cannot be empty"
        );
        assert_eq!(
            format!("{}", VigenereError::InvalidAlphabet),
            "Alphabet is invalid (empty or has duplicates)"
        );
        assert_eq!(
            format!("{}", VigenereError::KeyContainsInvalidChars("X".to_string())),
            "Key contains invalid characters: X"
        );
    }
}