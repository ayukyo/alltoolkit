//! # Slugify Utils
//!
//! A zero-dependency URL slug generator for Rust.
//! Converts strings into URL-friendly slugs.
//!
//! ## Features
//! - Converts Unicode characters to ASCII equivalents
//! - Removes special characters
//! - Converts to lowercase
//! - Replaces spaces and underscores with hyphens
//! - Removes duplicate hyphens
//! - Trims hyphens from start and end
//!
//! ## Example
//! ```rust
//! use slugify_utils;
//!
//! let slug = slugify_utils::slugify("Hello, World!");
//! assert_eq!(slug, "hello-world");
//! ```

use std::collections::HashMap;

/// Unicode to ASCII character mapping for common transliterations
fn get_unicode_map() -> HashMap<char, &'static str> {
    let mut map = HashMap::new();
    
    // Latin Extended-A
    map.insert('À', "A"); map.insert('Á', "A"); map.insert('Â', "A"); map.insert('Ã', "A");
    map.insert('Ä', "Ae"); map.insert('Å', "A"); map.insert('Æ', "Ae");
    map.insert('Ç', "C");
    map.insert('È', "E"); map.insert('É', "E"); map.insert('Ê', "E"); map.insert('Ë', "E");
    map.insert('Ì', "I"); map.insert('Í', "I"); map.insert('Î', "I"); map.insert('Ï', "I");
    map.insert('Ð', "D");
    map.insert('Ñ', "N");
    map.insert('Ò', "O"); map.insert('Ó', "O"); map.insert('Ô', "O"); map.insert('Õ', "O");
    map.insert('Ö', "Oe"); map.insert('Ø', "O");
    map.insert('Ù', "U"); map.insert('Ú', "U"); map.insert('Û', "U"); map.insert('Ü', "Ue");
    map.insert('Ý', "Y");
    map.insert('Þ', "Th");
    map.insert('ß', "ss");
    
    // Latin Extended-A lowercase
    map.insert('à', "a"); map.insert('á', "a"); map.insert('â', "a"); map.insert('ã', "a");
    map.insert('ä', "ae"); map.insert('å', "a"); map.insert('æ', "ae");
    map.insert('ç', "c");
    map.insert('è', "e"); map.insert('é', "e"); map.insert('ê', "e"); map.insert('ë', "e");
    map.insert('ì', "i"); map.insert('í', "i"); map.insert('î', "i"); map.insert('ï', "i");
    map.insert('ð', "d");
    map.insert('ñ', "n");
    map.insert('ò', "o"); map.insert('ó', "o"); map.insert('ô', "o"); map.insert('õ', "o");
    map.insert('ö', "oe"); map.insert('ø', "o");
    map.insert('ù', "u"); map.insert('ú', "u"); map.insert('û', "u"); map.insert('ü', "ue");
    map.insert('ý', "y"); map.insert('þ', "th");
    map.insert('ÿ', "y");
    
    // Cyrillic (common Russian letters)
    map.insert('а', "a"); map.insert('б', "b"); map.insert('в', "v"); map.insert('г', "g");
    map.insert('д', "d"); map.insert('е', "e"); map.insert('ё', "yo"); map.insert('ж', "zh");
    map.insert('з', "z"); map.insert('и', "i"); map.insert('й', "y"); map.insert('к', "k");
    map.insert('л', "l"); map.insert('м', "m"); map.insert('н', "n"); map.insert('о', "o");
    map.insert('п', "p"); map.insert('р', "r"); map.insert('с', "s"); map.insert('т', "t");
    map.insert('у', "u"); map.insert('ф', "f"); map.insert('х', "kh"); map.insert('ц', "ts");
    map.insert('ч', "ch"); map.insert('ш', "sh"); map.insert('щ', "shch"); map.insert('ъ', "");
    map.insert('ы', "y"); map.insert('ь', ""); map.insert('э', "e"); map.insert('ю', "yu");
    map.insert('я', "ya");
    
    // Cyrillic uppercase
    map.insert('А', "A"); map.insert('Б', "B"); map.insert('В', "V"); map.insert('Г', "G");
    map.insert('Д', "D"); map.insert('Е', "E"); map.insert('Ё', "Yo"); map.insert('Ж', "Zh");
    map.insert('З', "Z"); map.insert('И', "I"); map.insert('Й', "Y"); map.insert('К', "K");
    map.insert('Л', "L"); map.insert('М', "M"); map.insert('Н', "N"); map.insert('О', "O");
    map.insert('П', "P"); map.insert('Р', "R"); map.insert('С', "S"); map.insert('Т', "T");
    map.insert('У', "U"); map.insert('Ф', "F"); map.insert('Х', "Kh"); map.insert('Ц', "Ts");
    map.insert('Ч', "Ch"); map.insert('Ш', "Sh"); map.insert('Щ', "Shch"); map.insert('Ъ', "");
    map.insert('Ы', "Y"); map.insert('Ь', ""); map.insert('Э', "E"); map.insert('Ю', "Yu");
    map.insert('Я', "Ya");
    
    // Greek lowercase (including accented variants)
    map.insert('α', "a"); map.insert('β', "b"); map.insert('γ', "g"); map.insert('δ', "d");
    map.insert('ε', "e"); map.insert('ζ', "z"); map.insert('η', "i"); map.insert('θ', "th");
    map.insert('ι', "i"); map.insert('κ', "k"); map.insert('λ', "l"); map.insert('μ', "m");
    map.insert('ν', "n"); map.insert('ξ', "x"); map.insert('ο', "o"); map.insert('π', "p");
    map.insert('ρ', "r"); map.insert('σ', "s"); map.insert('ς', "s"); map.insert('τ', "t"); map.insert('υ', "y");
    map.insert('φ', "f"); map.insert('χ', "ch"); map.insert('ψ', "ps"); map.insert('ω', "o");
    // Greek lowercase with tonos (accented)
    map.insert('ά', "a"); map.insert('έ', "e"); map.insert('ή', "i"); map.insert('ί', "i");
    map.insert('ό', "o"); map.insert('ύ', "y"); map.insert('ώ', "o");
    
    // Greek uppercase
    map.insert('Α', "A"); map.insert('Β', "B"); map.insert('Γ', "G"); map.insert('Δ', "D");
    map.insert('Ε', "E"); map.insert('Ζ', "Z"); map.insert('Η', "I"); map.insert('Θ', "Th");
    map.insert('Ι', "I"); map.insert('Κ', "K"); map.insert('Λ', "L"); map.insert('Μ', "M");
    map.insert('Ν', "N"); map.insert('Ξ', "X"); map.insert('Ο', "O"); map.insert('Π', "P");
    map.insert('Ρ', "R"); map.insert('Σ', "S"); map.insert('Τ', "T"); map.insert('Υ', "Y");
    map.insert('Φ', "F"); map.insert('Χ', "Ch"); map.insert('Ψ', "Ps"); map.insert('Ω', "O");
    // Greek uppercase with tonos (accented)
    map.insert('Ά', "A"); map.insert('Έ', "E"); map.insert('Ή', "I"); map.insert('Ί', "I");
    map.insert('Ό', "O"); map.insert('Ύ', "Y"); map.insert('Ώ', "O");
    
    // Chinese numerals
    map.insert('一', "1"); map.insert('二', "2"); map.insert('三', "3");
    map.insert('四', "4"); map.insert('五', "5"); map.insert('六', "6");
    map.insert('七', "7"); map.insert('八', "8"); map.insert('九', "9");
    map.insert('十', "10"); map.insert('百', "100"); map.insert('千', "1000");
    
    // Japanese
    map.insert('の', "no");
    
    // Currency symbols (include separator for readability)
    map.insert('$', "-dollar-"); map.insert('€', "-euro-"); map.insert('£', "-pound-");
    map.insert('¥', "-yen-"); map.insert('₹', "-rupee-"); map.insert('₩', "-won-");
    map.insert('¢', "-cent-");
    
    // Other common symbols (include separator for readability)
    map.insert('&', "-and-"); map.insert('@', "-at-"); map.insert('#', "-hash-");
    map.insert('%', "-percent-"); map.insert('+', "-plus-");
    
    map
}

/// Configuration options for slug generation
#[derive(Debug, Clone)]
pub struct SlugifyOptions {
    /// Character to use as separator (default: '-')
    pub separator: char,
    /// Whether to convert to lowercase (default: true)
    pub lowercase: bool,
    /// Whether to transliterate Unicode characters (default: true)
    pub transliterate: bool,
    /// Maximum length of the slug (0 = no limit)
    pub max_length: usize,
    /// Whether to remove trailing numbers
    pub remove_trailing_numbers: bool,
}

impl Default for SlugifyOptions {
    fn default() -> Self {
        SlugifyOptions {
            separator: '-',
            lowercase: true,
            transliterate: true,
            max_length: 0,
            remove_trailing_numbers: false,
        }
    }
}

impl SlugifyOptions {
    /// Create new options with default values
    pub fn new() -> Self {
        Self::default()
    }
    
    /// Set the separator character
    pub fn separator(mut self, sep: char) -> Self {
        self.separator = sep;
        self
    }
    
    /// Set whether to lowercase
    pub fn lowercase(mut self, lower: bool) -> Self {
        self.lowercase = lower;
        self
    }
    
    /// Set whether to transliterate
    pub fn transliterate(mut self, trans: bool) -> Self {
        self.transliterate = trans;
        self
    }
    
    /// Set maximum length
    pub fn max_length(mut self, len: usize) -> Self {
        self.max_length = len;
        self
    }
    
    /// Set whether to remove trailing numbers
    pub fn remove_trailing_numbers(mut self, remove: bool) -> Self {
        self.remove_trailing_numbers = remove;
        self
    }
}

/// Convert a string to a URL-friendly slug with default options
///
/// # Arguments
/// * `input` - The string to convert
///
/// # Returns
/// A URL-friendly slug string
///
/// # Example
/// ```
/// let slug = slugify_utils::slugify("Hello, World!");
/// assert_eq!(slug, "hello-world");
/// ```
pub fn slugify(input: &str) -> String {
    slugify_with_options(input, SlugifyOptions::default())
}

/// Convert a string to a URL-friendly slug with custom options
///
/// # Arguments
/// * `input` - The string to convert
/// * `options` - Custom slugification options
///
/// # Returns
/// A URL-friendly slug string
///
/// # Example
/// ```
/// use slugify_utils::{slugify_with_options, SlugifyOptions};
///
/// let options = SlugifyOptions::new().separator('_').lowercase(false);
/// let slug = slugify_with_options("Hello, World!", options);
/// assert_eq!(slug, "Hello_World");
/// ```
pub fn slugify_with_options(input: &str, options: SlugifyOptions) -> String {
    let unicode_map = get_unicode_map();
    let mut result = String::new();
    let mut prev_separator = false;
    
    for ch in input.chars() {
        // Handle whitespace
        if ch.is_whitespace() || ch == '_' {
            if !prev_separator && !result.is_empty() {
                result.push(options.separator);
                prev_separator = true;
            }
            continue;
        }
        
        // Transliterate Unicode characters
        let processed = if options.transliterate {
            if let Some(replacement) = unicode_map.get(&ch) {
                replacement.to_string()
            } else if ch.is_ascii() {
                ch.to_string()
            } else {
                // Skip unknown Unicode characters
                continue;
            }
        } else {
            // When not transliterating, skip non-ASCII characters
            if !ch.is_ascii() {
                continue;
            }
            ch.to_string()
        };
        
        // Process each character of the replacement
        for pch in processed.chars() {
            if pch.is_alphanumeric() {
                let ch_to_add = if options.lowercase {
                    pch.to_lowercase().next().unwrap_or(pch)
                } else {
                    pch
                };
                result.push(ch_to_add);
                prev_separator = false;
            } else if pch == options.separator || pch == '-' || pch == '_' {
                if !prev_separator && !result.is_empty() {
                    result.push(options.separator);
                    prev_separator = true;
                }
            } else if pch == ' ' {
                if !prev_separator && !result.is_empty() {
                    result.push(options.separator);
                    prev_separator = true;
                }
            }
            // Skip other non-alphanumeric characters (like '.' in decimal numbers)
        }
    }
    
    // Remove trailing separator
    if result.ends_with(options.separator) {
        result.pop();
    }
    
    // Remove trailing numbers if requested
    if options.remove_trailing_numbers {
        while result.ends_with(|c: char| c.is_ascii_digit()) {
            result.pop();
        }
        // Also remove trailing separator after number removal
        if result.ends_with(options.separator) {
            result.pop();
        }
    }
    
    // Truncate to max length if specified
    if options.max_length > 0 && result.len() > options.max_length {
        // Find the last separator within the max length
        let truncated: String = result.chars().take(options.max_length).collect();
        if let Some(pos) = truncated.rfind(options.separator) {
            result = truncated[..pos].to_string();
        } else {
            result = truncated;
        }
    }
    
    result
}

/// Generate a slug from a title with a unique identifier
///
/// # Arguments
/// * `title` - The title to convert
/// * `id` - The unique identifier to append
///
/// # Returns
/// A slug in the format "title-id"
///
/// # Example
/// ```
/// let slug = slugify_utils::slugify_with_id("My Blog Post", 123);
/// assert_eq!(slug, "my-blog-post-123");
/// ```
pub fn slugify_with_id(title: &str, id: u64) -> String {
    let base = slugify(title);
    if base.is_empty() {
        format!("{}", id)
    } else {
        format!("{}-{}", base, id)
    }
}

/// Check if a string is a valid slug
///
/// # Arguments
/// * `s` - The string to check
///
/// # Returns
/// true if the string is a valid slug (only lowercase alphanumeric and hyphens)
///
/// # Example
/// ```
/// assert!(slugify_utils::is_valid_slug("hello-world-123"));
/// assert!(!slugify_utils::is_valid_slug("Hello World!"));
/// ```
pub fn is_valid_slug(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }
    
    // First character must be alphanumeric
    let first = s.chars().next().unwrap();
    if !first.is_ascii_lowercase() && !first.is_ascii_digit() {
        return false;
    }
    
    // Last character must be alphanumeric
    let last = s.chars().last().unwrap();
    if !last.is_ascii_lowercase() && !last.is_ascii_digit() {
        return false;
    }
    
    // All characters must be lowercase alphanumeric or hyphen
    for ch in s.chars() {
        if !ch.is_ascii_lowercase() && !ch.is_ascii_digit() && ch != '-' {
            return false;
        }
    }
    
    true
}

/// Parse a slug back to a readable title
///
/// # Arguments
/// * `slug` - The slug to parse
///
/// # Returns
/// A human-readable title string
///
/// # Example
/// ```
/// let title = slugify_utils::unslugify("hello-world-123");
/// assert_eq!(title, "Hello World 123");
/// ```
pub fn unslugify(slug: &str) -> String {
    let words: Vec<&str> = slug.split('-').collect();
    let capitalized: Vec<String> = words
        .iter()
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                Some(first) => {
                    let first_upper = first.to_uppercase().next().unwrap_or(first);
                    let rest: String = chars.collect();
                    format!("{}{}", first_upper, rest)
                }
                None => String::new(),
            }
        })
        .collect();
    
    capitalized.join(" ")
}

/// Truncate a slug to a maximum length, breaking at word boundaries
///
/// # Arguments
/// * `slug` - The slug to truncate
/// * `max_len` - Maximum length
///
/// # Returns
/// A truncated slug that doesn't break words
///
/// # Example
/// ```
/// let truncated = slugify_utils::truncate_slug("hello-world-from-rust", 10);
/// assert_eq!(truncated, "hello");
/// ```
pub fn truncate_slug(slug: &str, max_len: usize) -> String {
    if slug.len() <= max_len {
        return slug.to_string();
    }
    
    // Find the last separator before max_len
    let truncated: String = slug.chars().take(max_len).collect();
    if let Some(pos) = truncated.rfind('-') {
        truncated[..pos].to_string()
    } else {
        truncated
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_slugify() {
        assert_eq!(slugify("Hello World"), "hello-world");
        assert_eq!(slugify("Hello, World!"), "hello-world");
        assert_eq!(slugify("  Hello  World  "), "hello-world");
    }
    
    #[test]
    fn test_unicode_transliteration() {
        assert_eq!(slugify("Café"), "cafe");
        assert_eq!(slugify("naïve"), "naive");
        assert_eq!(slugify("München"), "muenchen");
        assert_eq!(slugify("北京"), ""); // Chinese characters without transliteration
    }
    
    #[test]
    fn test_cyrillic_transliteration() {
        assert_eq!(slugify("Привет мир"), "privet-mir");
        assert_eq!(slugify("Москва"), "moskva");
    }
    
    #[test]
    fn test_greek_transliteration() {
        assert_eq!(slugify("Αθήνα"), "athina");
        assert_eq!(slugify("λόγος"), "logos");
    }
    
    #[test]
    fn test_special_characters() {
        assert_eq!(slugify("Hello@World"), "hello-at-world");
        assert_eq!(slugify("C# Programming"), "c-hash-programming");
        assert_eq!(slugify("100%"), "100-percent");
    }
    
    #[test]
    fn test_separator_options() {
        let options = SlugifyOptions::new().separator('_');
        assert_eq!(slugify_with_options("Hello World", options), "hello_world");
    }
    
    #[test]
    fn test_lowercase_option() {
        let options = SlugifyOptions::new().lowercase(false);
        assert_eq!(slugify_with_options("Hello World", options), "Hello-World");
    }
    
    #[test]
    fn test_max_length() {
        let options = SlugifyOptions::new().max_length(10);
        assert_eq!(slugify_with_options("Hello Beautiful World", options), "hello");
    }
    
    #[test]
    fn test_transliterate_option() {
        let options = SlugifyOptions::new().transliterate(false);
        // Without transliteration, Unicode chars are skipped, only ASCII remains
        assert_eq!(slugify_with_options("Hello World", options.clone()), "hello-world");
        // Café without transliterate becomes just "caf" since é is skipped
        assert_eq!(slugify_with_options("Café", options), "caf");
    }
    
    #[test]
    fn test_slugify_with_id() {
        assert_eq!(slugify_with_id("My Blog Post", 123), "my-blog-post-123");
        assert_eq!(slugify_with_id("", 456), "456");
    }
    
    #[test]
    fn test_is_valid_slug() {
        assert!(is_valid_slug("hello-world"));
        assert!(is_valid_slug("test-123"));
        assert!(is_valid_slug("a"));
        assert!(!is_valid_slug(""));
        assert!(!is_valid_slug("Hello-World"));
        assert!(!is_valid_slug("hello_world"));
        assert!(!is_valid_slug("-hello"));
        assert!(!is_valid_slug("hello-"));
    }
    
    #[test]
    fn test_unslugify() {
        assert_eq!(unslugify("hello-world"), "Hello World");
        assert_eq!(unslugify("my-blog-post-123"), "My Blog Post 123");
        assert_eq!(unslugify("test"), "Test");
    }
    
    #[test]
    fn test_truncate_slug() {
        assert_eq!(truncate_slug("hello-world-test", 10), "hello");
        assert_eq!(truncate_slug("short", 10), "short");
        assert_eq!(truncate_slug("hello-world", 5), "hello");
    }
    
    #[test]
    fn test_currency_symbols() {
        assert_eq!(slugify("$100"), "dollar-100");
        assert_eq!(slugify("€50 discount"), "euro-50-discount");
        assert_eq!(slugify("£20"), "pound-20");
    }
    
    #[test]
    fn test_multiple_spaces() {
        assert_eq!(slugify("Hello    World"), "hello-world");
        assert_eq!(slugify("  Multiple   Spaces  "), "multiple-spaces");
    }
    
    #[test]
    fn test_mixed_case() {
        assert_eq!(slugify("HELLO WORLD"), "hello-world");
        assert_eq!(slugify("HeLLo WoRLd"), "hello-world");
    }
    
    #[test]
    fn test_numbers() {
        assert_eq!(slugify("Version 2.0"), "version-20");
        assert_eq!(slugify("Top 10 List"), "top-10-list");
    }
    
    #[test]
    fn test_remove_trailing_numbers() {
        let options = SlugifyOptions::new().remove_trailing_numbers(true);
        assert_eq!(slugify_with_options("article-123", options.clone()), "article");
        assert_eq!(slugify_with_options("post-456-test-789", options), "post-456-test");
    }
}