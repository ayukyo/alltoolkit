//! # Emoji Utilities
//!
//! A zero-dependency Rust library for emoji detection and manipulation.
//!
//! ## Features
//!
//! - Detect emoji in strings
//! - Count, extract, remove, and replace emojis
//! - Unicode 15.1 compatible
//! - Zero external dependencies
//!
//! ## Example
//!
//! ```
//! use emoji_utils::{contains_emoji, count_emoji, extract_emoji, remove_emoji};
//!
//! let text = "Hello 👋 World 🌍!";
//! assert!(contains_emoji(text));
//! assert_eq!(count_emoji(text), 2);
//! assert_eq!(extract_emoji(text), vec!["👋", "🌍"]);
//! assert_eq!(remove_emoji(text), "Hello  World !");
//! ```

use std::char;

/// Check if a character is an emoji.
///
/// Supports Unicode 15.1 emoji ranges including:
/// - Emoticons (U+1F600-U+1F64F)
/// - Miscellaneous Symbols and Pictographs (U+1F300-U+1F5FF)
/// - Transport and Map Symbols (U+1F680-U+1F6FF)
/// - Supplemental Symbols and Pictographs (U+1F900-U+1F9FF)
/// - And many more...
pub fn is_emoji(c: char) -> bool {
    let cp = c as u32;
    
    // Basic emoji ranges
    match cp {
        // Emoticons
        0x1F600..=0x1F64F => true,
        
        // Miscellaneous Symbols and Pictographs
        0x1F300..=0x1F5FF => true,
        
        // Transport and Map Symbols
        0x1F680..=0x1F6FF => true,
        
        // Supplemental Symbols and Pictographs
        0x1F900..=0x1F9FF => true,
        
        // Symbols and Pictographs Extended-A
        0x1FA00..=0x1FA6F => true,
        
        // Symbols and Pictographs Extended-B
        0x1FA70..=0x1FAFF => true,
        
        // Dingbats
        0x2700..=0x27BF => true,
        
        // Miscellaneous Symbols
        0x2600..=0x26FF => true,
        
        // Stars (U+2B50, U+2B55)
        0x2B50 => true, // White Medium Star ⭐
        0x2B55 => true, // Heavy Large Circle ⭕
        
        // Variation Selectors (used for emoji presentation)
        0xFE00..=0xFE0F => true,
        
        // Combining characters for emoji
        0x200D => true, // Zero Width Joiner
        0x20E3 => true, // Combining Enclosing Keycap
        
        // Regional Indicator Symbols (for flag emojis)
        0x1F1E6..=0x1F1FF => true,
        
        // Enclosed characters used in emoji
        0x24C2 => true, // Circled M
        
        // Keycap characters
        0x0023..=0x0039 => false, // Numbers and # handled specially
        
        // Arrows (some are emojis)
        0x2194..=0x21AA => is_arrow_emoji(cp),
        
        // Geometric shapes (some are emojis)
        0x25AA..=0x25FE => true,
        
        // CJK Unified Ideographs extensions with emoji
        0x1F004 => true, // Mahjong Red Dragon
        0x1F0CF => true, // Playing Card Black Joker
        
        _ => false,
    }
}

/// Check if an arrow codepoint is an emoji
fn is_arrow_emoji(cp: u32) -> bool {
    matches!(cp,
        0x2194 | 0x2195 | 0x2196 | 0x2197 | 0x2198 | 0x2199 |
        0x21A9 | 0x21AA
    )
}

/// Check if a string contains any emoji.
///
/// # Example
///
/// ```
/// use emoji_utils::contains_emoji;
///
/// assert!(contains_emoji("Hello 👋"));
/// assert!(!contains_emoji("Hello World"));
/// ```
pub fn contains_emoji(s: &str) -> bool {
    s.chars().any(is_emoji)
}

/// Count the number of emoji in a string.
///
/// Note: Complex emojis (like family emojis with ZWJ) are counted as
/// multiple individual emojis. Use `count_emoji_sequences` for
/// grapheme-cluster-like counting.
///
/// # Example
///
/// ```
/// use emoji_utils::count_emoji;
///
/// assert_eq!(count_emoji("Hello 👋 World 🌍"), 2);
/// assert_eq!(count_emoji("No emoji here"), 0);
/// ```
pub fn count_emoji(s: &str) -> usize {
    s.chars().filter(|c| is_emoji(*c)).count()
}

/// Count emoji sequences (handles ZWJ sequences as single units).
///
/// This counts complex emojis like family emojis (👨‍👩‍👧‍👦) as a single unit.
/// Simple emojis that are adjacent (not connected by ZWJ) are counted separately.
///
/// # Example
///
/// ```
/// use emoji_utils::count_emoji_sequences;
///
/// // Simple emojis - each counted separately
/// assert_eq!(count_emoji_sequences("Hello 👋 World 🌍"), 2);
/// assert_eq!(count_emoji_sequences("😀😃😄"), 3);
/// ```
pub fn count_emoji_sequences(s: &str) -> usize {
    let mut count = 0;
    let mut prev_was_zwj = false;
    
    for c in s.chars() {
        let cp = c as u32;
        
        if cp == 0x200D {
            // Zero Width Joiner - next emoji is part of current sequence
            prev_was_zwj = true;
            continue;
        }
        
        if is_emoji(c) {
            // Only count if NOT connected by ZWJ to previous emoji
            if !prev_was_zwj {
                count += 1;
            }
            prev_was_zwj = false;
        } else if cp >= 0xFE00 && cp <= 0xFE0F {
            // Variation selector - part of sequence, don't reset prev_was_zwj
        } else {
            // Non-emoji, non-ZWJ, non-variation selector
            prev_was_zwj = false;
        }
    }
    
    count
}

/// Extract all emoji characters from a string.
///
/// # Example
///
/// ```
/// use emoji_utils::extract_emoji;
///
/// let emojis = extract_emoji("Hello 👋 World 🌍!");
/// assert_eq!(emojis, vec!["👋", "🌍"]);
/// ```
pub fn extract_emoji(s: &str) -> Vec<String> {
    s.chars()
        .filter(|c| is_emoji(*c))
        .map(|c| c.to_string())
        .collect()
}

/// Extract emoji sequences (handles ZWJ sequences as single units).
///
/// # Example
///
/// ```
/// use emoji_utils::extract_emoji_sequences;
///
/// let emojis = extract_emoji_sequences("Hello 👋 World 🌍");
/// assert_eq!(emojis.len(), 2);
/// ```
pub fn extract_emoji_sequences(s: &str) -> Vec<String> {
    let mut sequences = Vec::new();
    let mut current = String::new();
    let mut in_emoji = false;
    
    for c in s.chars() {
        let cp = c as u32;
        
        if cp == 0x200D {
            // Zero Width Joiner - extend current sequence
            current.push(c);
            continue;
        }
        
        if (cp >= 0xFE00 && cp <= 0xFE0F) || (cp >= 0x1F1E6 && cp <= 0x1F1FF) {
            // Variation selector or regional indicator - extend current
            current.push(c);
            continue;
        }
        
        if is_emoji(c) {
            if !current.is_empty() && !in_emoji {
                sequences.push(current.clone());
                current.clear();
            }
            current.push(c);
            in_emoji = true;
        } else {
            if !current.is_empty() {
                sequences.push(current.clone());
                current.clear();
            }
            in_emoji = false;
        }
    }
    
    if !current.is_empty() {
        sequences.push(current);
    }
    
    sequences
}

/// Remove all emoji from a string.
///
/// # Example
///
/// ```
/// use emoji_utils::remove_emoji;
///
/// assert_eq!(remove_emoji("Hello 👋 World 🌍!"), "Hello  World !");
/// ```
pub fn remove_emoji(s: &str) -> String {
    s.chars()
        .filter(|c| !is_emoji(*c))
        .collect()
}

/// Remove emoji sequences from a string.
///
/// # Example
///
/// ```
/// use emoji_utils::remove_emoji_sequences;
///
/// let result = remove_emoji_sequences("Hello 👋 World 🌍!");
/// assert_eq!(result, "Hello  World !");
/// ```
pub fn remove_emoji_sequences(s: &str) -> String {
    let mut result = String::new();
    let mut chars = s.chars().peekable();
    
    while let Some(c) = chars.next() {
        let cp = c as u32;
        
        if cp == 0x200D {
            // Skip ZWJ
            continue;
        }
        
        if (cp >= 0xFE00 && cp <= 0xFE0F) || (cp >= 0x1F1E6 && cp <= 0x1F1FF) {
            // Skip variation selectors and regional indicators
            continue;
        }
        
        if is_emoji(c) {
            // Skip emoji
            continue;
        }
        
        result.push(c);
    }
    
    result
}

/// Replace all emoji with a replacement string.
///
/// # Example
///
/// ```
/// use emoji_utils::replace_emoji;
///
/// assert_eq!(replace_emoji("Hello 👋 World 🌍!", "[emoji]"), "Hello [emoji] World [emoji]!");
/// ```
pub fn replace_emoji(s: &str, replacement: &str) -> String {
    s.chars()
        .map(|c| {
            if is_emoji(c) {
                replacement.to_string()
            } else {
                c.to_string()
            }
        })
        .collect()
}

/// Check if a string consists only of emojis.
///
/// # Example
///
/// ```
/// use emoji_utils::is_only_emoji;
///
/// assert!(is_only_emoji("👋🌍"));
/// assert!(!is_only_emoji("Hello 👋"));
/// assert!(!is_only_emoji(""));
/// ```
pub fn is_only_emoji(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }
    
    // Check if all significant chars are emoji
    let mut has_emoji = false;
    for c in s.chars() {
        let cp = c as u32;
        // Skip ZWJ, variation selectors, and whitespace
        if cp == 0x200D || (cp >= 0xFE00 && cp <= 0xFE0F) || c.is_whitespace() {
            continue;
        }
        if !is_emoji(c) {
            return false;
        }
        has_emoji = true;
    }
    has_emoji
}

/// Get emoji name/description (basic subset).
///
/// Returns a description for common emojis, or None if unknown.
///
/// # Example
///
/// ```
/// use emoji_utils::get_emoji_name;
///
/// assert_eq!(get_emoji_name('👋'), Some("waving hand"));
/// assert_eq!(get_emoji_name('🌍'), Some("globe showing Europe-Africa"));
/// ```
pub fn get_emoji_name(c: char) -> Option<&'static str> {
    let cp = c as u32;
    
    match cp {
        // Faces
        0x1F600 => Some("grinning face"),
        0x1F601 => Some("beaming face with smiling eyes"),
        0x1F602 => Some("face with tears of joy"),
        0x1F603 => Some("smiling face with open mouth"),
        0x1F604 => Some("smiling face with open mouth and smiling eyes"),
        0x1F605 => Some("smiling face with open mouth and cold sweat"),
        0x1F606 => Some("smiling face with open mouth and tightly-closed eyes"),
        0x1F607 => Some("smiling face with halo"),
        0x1F608 => Some("smiling face with horns"),
        0x1F609 => Some("winking face"),
        0x1F60A => Some("smiling face with smiling eyes"),
        0x1F60B => Some("face savouring delicious food"),
        0x1F60C => Some("relieved face"),
        0x1F60D => Some("smiling face with heart-eyes"),
        0x1F60E => Some("smiling face with sunglasses"),
        0x1F60F => Some("smirking face"),
        
        // Hands
        0x1F44B => Some("waving hand"),
        0x1F44C => Some("OK hand"),
        0x1F44D => Some("thumbs up"),
        0x1F44E => Some("thumbs down"),
        0x1F44F => Some("clapping hands"),
        0x1F44A => Some("oncoming fist"),
        0x270B => Some("raised hand"),
        0x270C => Some("victory hand"),
        
        // Hearts
        0x2764 => Some("red heart"),
        0x1F494 => Some("broken heart"),
        0x1F495 => Some("two hearts"),
        0x1F496 => Some("sparkling heart"),
        0x1F497 => Some("growing heart"),
        0x1F498 => Some("heart with arrow"),
        0x1F499 => Some("blue heart"),
        0x1F49A => Some("green heart"),
        0x1F49B => Some("yellow heart"),
        0x1F49C => Some("purple heart"),
        0x1F49D => Some("heart with ribbon"),
        0x1F49E => Some("revolving hearts"),
        0x1F49F => Some("heart decoration"),
        
        // Earth/Globe
        0x1F30D => Some("globe showing Europe-Africa"),
        0x1F30E => Some("globe showing Americas"),
        0x1F30F => Some("globe showing Asia-Australia"),
        0x1F310 => Some("globe with meridians"),
        0x1F5FA => Some("world map"),
        
        // Nature
        0x1F33A => Some("hibiscus"),
        0x1F33B => Some("sunflower"),
        0x1F33C => Some("blossom"),
        0x1F33D => Some("ear of corn"),
        0x1F33E => Some("sheaf of rice"),
        0x1F33F => Some("herb"),
        0x1F340 => Some("four leaf clover"),
        0x1F341 => Some("maple leaf"),
        0x1F342 => Some("fallen leaf"),
        0x1F343 => Some("leaf fluttering in wind"),
        
        // Animals
        0x1F436 => Some("dog face"),
        0x1F431 => Some("cat face"),
        0x1F98B => Some("butterfly"),
        0x1F43E => Some("paw prints"),
        0x1F983 => Some("turkey"),
        0x1F426 => Some("bird"),
        0x1F41F => Some("fish"),
        0x1F433 => Some("spouting whale"),
        0x1F40D => Some("snake"),
        0x1F42C => Some("dolphin"),
        
        // Food
        0x1F354 => Some("hamburger"),
        0x1F355 => Some("pizza"),
        0x1F369 => Some("doughnut"),
        0x1F36A => Some("cookie"),
        0x1F36B => Some("chocolate bar"),
        0x1F36C => Some("candy"),
        0x1F36D => Some("lollipop"),
        0x1F370 => Some("shortcake"),
        0x1F377 => Some("wine glass"),
        0x1F37A => Some("beer mug"),
        0x1F37B => Some("clinking beer mugs"),
        0x1F37E => Some("bottle with popping cork"),
        0x1F37F => Some("popcorn"),
        
        // Weather
        0x2600 => Some("sun"),
        0x2614 => Some("umbrella with rain drops"),
        0x26C5 => Some("sun behind cloud"),
        0x1F324 => Some("sun behind small cloud"),
        0x1F325 => Some("sun behind large cloud"),
        0x1F326 => Some("sun behind rain cloud"),
        0x1F327 => Some("cloud with rain"),
        0x1F328 => Some("cloud with snow"),
        0x1F329 => Some("cloud with lightning"),
        0x1F32A => Some("cloud with tornado"),
        0x1F32B => Some("fog"),
        0x1F32C => Some("wind face"),
        
        // Technology
        0x1F4F1 => Some("mobile phone"),
        0x1F4F2 => Some("mobile phone with arrow"),
        0x1F4BB => Some("laptop computer"),
        0x1F4C1 => Some("file folder"),
        0x1F4C2 => Some("open file folder"),
        0x1F4C3 => Some("page with curl"),
        0x1F4C4 => Some("page facing up"),
        0x1F4C5 => Some("calendar"),
        0x1F4D2 => Some("ledger"),
        0x1F4DA => Some("books"),
        
        // Symbols
        0x2714 => Some("check mark"),
        0x2716 => Some("cross mark"),
        0x2728 => Some("sparkles"),
        0x2753 => Some("question mark"),
        0x2754 => Some("white question mark"),
        0x2755 => Some("white exclamation mark"),
        0x2757 => Some("exclamation mark"),
        0x26A0 => Some("warning sign"),
        0x26D4 => Some("no entry"),
        0x26EA => Some("church"),
        0x26F5 => Some("sailboat"),
        0x26F3 => Some("flag in hole"),
        0x26BE => Some("baseball"),
        0x26BD => Some("soccer ball"),
        0x26C0 => Some("white circle"),
        0x26C1 => Some("black circle"),
        0x26AA => Some("medium white circle"),
        0x26AB => Some("medium black circle"),
        
        _ => None,
    }
}

/// Emoji category enumeration.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EmojiCategory {
    Smileys,
    People,
    Animals,
    Food,
    Nature,
    Objects,
    Travel,
    Activities,
    Symbols,
    Flags,
    Unknown,
}

/// Get the category of an emoji.
///
/// # Example
///
/// ```
/// use emoji_utils::{get_emoji_category, EmojiCategory};
///
/// assert_eq!(get_emoji_category('👋'), EmojiCategory::People);
/// assert_eq!(get_emoji_category('🌍'), EmojiCategory::Travel);
/// assert_eq!(get_emoji_category('🍕'), EmojiCategory::Food);
/// ```
pub fn get_emoji_category(c: char) -> EmojiCategory {
    let cp = c as u32;
    
    match cp {
        // Smileys & Emotion
        0x1F600..=0x1F64F => EmojiCategory::Smileys,
        
        // People & Body
        0x1F9B0..=0x1F9C3 => EmojiCategory::People,
        0x1F440..=0x1F4A9 | 0x1F4BB..=0x1F4FC => EmojiCategory::People,
        
        // Animals
        0x1F400..=0x1F43F => EmojiCategory::Animals,
        0x1F980..=0x1F9AF => EmojiCategory::Animals,
        
        // Nature (plants, weather, celestial)
        0x1F330..=0x1F34F => EmojiCategory::Nature,
        
        // Food & Drink (covers pizza, hamburger, etc.)
        0x1F350..=0x1F37F => EmojiCategory::Food,
        0x1F32D..=0x1F32F => EmojiCategory::Food,  // Hot dog, taco, burrito
        
        // Travel & Places
        0x1F300..=0x1F30F => EmojiCategory::Travel,
        0x1F680..=0x1F6BF => EmojiCategory::Travel,
        0x1F6D0..=0x1F6FF => EmojiCategory::Travel,
        0x1F3D0..=0x1F3F0 => EmojiCategory::Travel,
        0x26EA | 0x26F2 | 0x26F5 => EmojiCategory::Travel,
        
        // Activities
        0x26BE..=0x26BF => EmojiCategory::Activities,
        0x26F0..=0x26F9 => EmojiCategory::Activities,
        0x1F380..=0x1F39F => EmojiCategory::Activities,
        0x1F3A0..=0x1F3CF => EmojiCategory::Activities,
        
        // Objects
        0x1F4A0..=0x1F4FF => EmojiCategory::Objects,
        0x1F500..=0x1F5FF => EmojiCategory::Objects,
        
        // Symbols (some transport symbols overlap, but we handle them in Travel)
        0x2700..=0x27BF => EmojiCategory::Symbols,
        0x1F6C0..=0x1F6CF => EmojiCategory::Symbols,
        
        // Flags
        0x1F1E6..=0x1F1FF => EmojiCategory::Flags,
        
        _ => EmojiCategory::Unknown,
    }
}

/// Statistics about emojis in a string.
#[derive(Debug, Clone)]
pub struct EmojiStats {
    /// Total number of emoji characters
    pub count: usize,
    /// Number of emoji sequences (ZWJ sequences counted as 1)
    pub sequence_count: usize,
    /// Whether the string contains any emoji
    pub has_emoji: bool,
    /// Whether the string is only emoji (ignoring whitespace)
    pub is_only_emoji: bool,
    /// Unique emojis found
    pub unique_count: usize,
}

/// Get comprehensive emoji statistics for a string.
///
/// # Example
///
/// ```
/// use emoji_utils::get_emoji_stats;
///
/// let stats = get_emoji_stats("Hello 👋 World 🌍!");
/// assert_eq!(stats.count, 2);
/// assert_eq!(stats.sequence_count, 2);
/// assert!(stats.has_emoji);
/// assert!(!stats.is_only_emoji);
/// ```
pub fn get_emoji_stats(s: &str) -> EmojiStats {
    let emojis = extract_emoji(s);
    let count = emojis.len();
    let sequence_count = count_emoji_sequences(s);
    let has_emoji = count > 0;
    let is_only_emoji = is_only_emoji(s);
    
    let mut unique: std::collections::HashSet<char> = std::collections::HashSet::new();
    for c in s.chars() {
        if is_emoji(c) {
            unique.insert(c);
        }
    }
    
    EmojiStats {
        count,
        sequence_count,
        has_emoji,
        is_only_emoji,
        unique_count: unique.len(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_is_emoji() {
        assert!(is_emoji('👋'));
        assert!(is_emoji('🌍'));
        assert!(is_emoji('😀'));
        assert!(is_emoji('❤'));
        assert!(is_emoji('⭐'));
        assert!(!is_emoji('A'));
        assert!(!is_emoji('1'));
        assert!(!is_emoji(' '));
    }
    
    #[test]
    fn test_contains_emoji() {
        assert!(contains_emoji("Hello 👋 World"));
        assert!(contains_emoji("😀"));
        assert!(!contains_emoji("Hello World"));
        assert!(!contains_emoji(""));
    }
    
    #[test]
    fn test_count_emoji() {
        assert_eq!(count_emoji("Hello 👋 World 🌍"), 2);
        assert_eq!(count_emoji("😀😃😄"), 3);
        assert_eq!(count_emoji("No emoji"), 0);
        assert_eq!(count_emoji(""), 0);
    }
    
    #[test]
    fn test_count_emoji_sequences() {
        assert_eq!(count_emoji_sequences("Hello 👋 World 🌍"), 2);
        assert_eq!(count_emoji_sequences("😀😃😄"), 3);
    }
    
    #[test]
    fn test_extract_emoji() {
        let emojis = extract_emoji("Hello 👋 World 🌍!");
        assert_eq!(emojis, vec!["👋", "🌍"]);
        
        let emojis2 = extract_emoji("😀😃😄");
        assert_eq!(emojis2, vec!["😀", "😃", "😄"]);
        
        let emojis3 = extract_emoji("No emoji");
        assert!(emojis3.is_empty());
    }
    
    #[test]
    fn test_remove_emoji() {
        assert_eq!(remove_emoji("Hello 👋 World 🌍!"), "Hello  World !");
        assert_eq!(remove_emoji("😀Test"), "Test");
        assert_eq!(remove_emoji("No emoji"), "No emoji");
    }
    
    #[test]
    fn test_replace_emoji() {
        assert_eq!(replace_emoji("Hello 👋 World 🌍!", "[emoji]"), "Hello [emoji] World [emoji]!");
        assert_eq!(replace_emoji("😀 Test", "*"), "* Test");
    }
    
    #[test]
    fn test_is_only_emoji() {
        assert!(is_only_emoji("👋🌍"));
        assert!(is_only_emoji("😀"));
        assert!(!is_only_emoji("Hello 👋"));
        assert!(!is_only_emoji(""));
        assert!(!is_only_emoji("   "));
    }
    
    #[test]
    fn test_get_emoji_name() {
        assert_eq!(get_emoji_name('👋'), Some("waving hand"));
        assert_eq!(get_emoji_name('🌍'), Some("globe showing Europe-Africa"));
        assert_eq!(get_emoji_name('😀'), Some("grinning face"));
        assert_eq!(get_emoji_name('A'), None);
    }
    
    #[test]
    fn test_get_emoji_category() {
        assert_eq!(get_emoji_category('👋'), EmojiCategory::People);
        assert_eq!(get_emoji_category('🌍'), EmojiCategory::Travel);
        assert_eq!(get_emoji_category('😀'), EmojiCategory::Smileys);
        assert_eq!(get_emoji_category('🍕'), EmojiCategory::Food);
    }
    
    #[test]
    fn test_get_emoji_stats() {
        let stats = get_emoji_stats("Hello 👋 World 🌍!");
        assert_eq!(stats.count, 2);
        assert_eq!(stats.sequence_count, 2);
        assert!(stats.has_emoji);
        assert!(!stats.is_only_emoji);
        assert_eq!(stats.unique_count, 2);
        
        let stats2 = get_emoji_stats("👋👋");
        assert_eq!(stats2.count, 2);
        assert_eq!(stats2.unique_count, 1);
    }
    
    #[test]
    fn test_hearts() {
        assert!(is_emoji('❤'));
        assert!(is_emoji('💙'));
        assert!(is_emoji('💚'));
        assert_eq!(get_emoji_name('❤'), Some("red heart"));
    }
    
    #[test]
    fn test_nature_emoji() {
        assert!(is_emoji('🌸'));
        assert!(is_emoji('🌻'));
        assert!(is_emoji('🍁'));
    }
    
    #[test]
    fn test_food_emoji() {
        assert!(is_emoji('🍕'));
        assert!(is_emoji('🍔'));
        assert!(is_emoji('🍩'));
    }
    
    #[test]
    fn test_animal_emoji() {
        assert!(is_emoji('🐶'));
        assert!(is_emoji('🐱'));
        assert!(is_emoji('🦋'));
    }
}