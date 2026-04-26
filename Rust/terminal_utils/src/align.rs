//! Text alignment utilities
//! 
//! Provides functions for aligning text in fixed-width fields.

use crate::terminal::size_or_default;

/// Align text to the left in a field of given width
/// 
/// # Arguments
/// * `text` - Text to align
/// * `width` - Total width of the field
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// assert_eq!(align::left("hi", 5), "hi   ");
/// ```
pub fn left(text: &str, width: usize) -> String {
    let display_width = display_width(text);
    if display_width >= width {
        text.to_string()
    } else {
        format!("{}{}", text, " ".repeat(width - display_width))
    }
}

/// Align text to the right in a field of given width
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// assert_eq!(align::right("hi", 5), "   hi");
/// ```
pub fn right(text: &str, width: usize) -> String {
    let display_width = display_width(text);
    if display_width >= width {
        text.to_string()
    } else {
        format!("{}{}", " ".repeat(width - display_width), text)
    }
}

/// Center text in a field of given width
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// assert_eq!(align::center("hi", 6), "  hi  ");
/// ```
pub fn center(text: &str, width: usize) -> String {
    let display_width = display_width(text);
    if display_width >= width {
        text.to_string()
    } else {
        let total_padding = width - display_width;
        let left_padding = total_padding / 2;
        let right_padding = total_padding - left_padding;
        format!("{}{}{}", " ".repeat(left_padding), text, " ".repeat(right_padding))
    }
}

/// Align text to center with specified padding character
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// assert_eq!(align::center_with("hi", 6, '-'), "--hi--");
/// ```
pub fn center_with(text: &str, width: usize, pad: char) -> String {
    let display_width = display_width(text);
    if display_width >= width {
        text.to_string()
    } else {
        let total_padding = width - display_width;
        let left_padding = total_padding / 2;
        let right_padding = total_padding - left_padding;
        format!("{}{}{}", pad.to_string().repeat(left_padding), text, pad.to_string().repeat(right_padding))
    }
}

/// Truncate text to fit width, adding ellipsis if needed
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// // Truncate with ellipsis - result width will be <= specified width
/// let truncated = align::truncate("hello world", 8);
/// assert!(align::display_width(&truncated) <= 8);
/// assert!(truncated.ends_with('…'));
/// ```
pub fn truncate(text: &str, width: usize) -> String {
    let display_width = display_width(text);
    if display_width <= width {
        text.to_string()
    } else if width <= 1 {
        "…".to_string()
    } else {
        // Find how many characters fit
        let mut result = String::new();
        let mut current_width = 0;
        
        for ch in text.chars() {
            let ch_width = char_display_width(ch);
            if current_width + ch_width + 1 > width {
                break;
            }
            result.push(ch);
            current_width += ch_width;
        }
        
        result.push('…');
        result
    }
}

/// Pad text on both sides evenly
pub fn pad_both(text: &str, width: usize) -> String {
    center(text, width)
}

/// Pad text on left to right-align
pub fn pad_left(text: &str, width: usize) -> String {
    right(text, width)
}

/// Pad text on right to left-align
pub fn pad_right(text: &str, width: usize) -> String {
    left(text, width)
}

/// Center text across terminal width
pub fn center_terminal(text: &str) -> String {
    let term_width = size_or_default().width as usize;
    center(text, term_width)
}

/// Right-align text in terminal
pub fn right_terminal(text: &str) -> String {
    let term_width = size_or_default().width as usize;
    right(text, term_width)
}

/// Distribute multiple strings evenly across a width
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// let result = align::distribute(&["left", "right"], 20);
/// // "left          right"
/// ```
pub fn distribute(texts: &[&str], width: usize) -> String {
    if texts.is_empty() {
        return " ".repeat(width);
    }
    
    if texts.len() == 1 {
        return left(texts[0], width);
    }
    
    let total_text_width: usize = texts.iter().map(|t| display_width(t)).sum();
    let total_padding = width.saturating_sub(total_text_width);
    let gaps = texts.len() - 1;
    let padding_per_gap = if gaps > 0 { total_padding / gaps } else { 0 };
    let extra_padding = if gaps > 0 { total_padding % gaps } else { 0 };
    
    let mut result = String::new();
    for (i, text) in texts.iter().enumerate() {
        result.push_str(text);
        if i < gaps {
            let extra = if i < extra_padding { 1 } else { 0 };
            result.push_str(&" ".repeat(padding_per_gap + extra));
        }
    }
    
    result
}

/// Calculate display width of a string (accounting for wide characters)
pub fn display_width(s: &str) -> usize {
    s.chars().map(char_display_width).sum()
}

/// Calculate display width of a single character
fn char_display_width(ch: char) -> usize {
    // Wide characters (CJK, emojis, etc.) take 2 columns
    match ch {
        // CJK Unified Ideographs
        '\u{4E00}'..='\u{9FFF}' => 2,
        // CJK Unified Ideographs Extension A
        '\u{3400}'..='\u{4DBF}' => 2,
        // CJK Unified Ideographs Extension B-F
        '\u{20000}'..='\u{2CEAF}' => 2,
        // CJK Compatibility Ideographs
        '\u{F900}'..='\u{FAFF}' => 2,
        // CJK Symbols and Punctuation
        '\u{3000}'..='\u{303F}' => 2,
        // Hiragana
        '\u{3040}'..='\u{309F}' => 2,
        // Katakana
        '\u{30A0}'..='\u{30FF}' => 2,
        // Hangul Syllables
        '\u{AC00}'..='\u{D7AF}' => 2,
        // Fullwidth ASCII variants
        '\u{FF00}'..='\u{FFEF}' => 2,
        // Control characters have zero width
        '\u{0000}'..='\u{001F}' => 0,
        '\u{007F}' => 0,
        // Default: 1 for ASCII and narrow characters
        _ => 1,
    }
}

/// Repeat a string to fill a given width
/// 
/// # Example
/// ```rust
/// use terminal_utils::align;
/// assert_eq!(align::repeat_to_width("ab", 7), "abababa");
/// ```
pub fn repeat_to_width(s: &str, width: usize) -> String {
    let s_width = display_width(s);
    if s_width == 0 {
        return String::new();
    }
    
    let repeats = width / s_width;
    let remainder = width % s_width;
    
    let mut result = s.repeat(repeats);
    
    // Add partial string for remainder
    if remainder > 0 {
        let mut current_width = 0;
        for ch in s.chars() {
            let ch_width = char_display_width(ch);
            if current_width + ch_width > remainder {
                break;
            }
            result.push(ch);
            current_width += ch_width;
        }
    }
    
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_left() {
        assert_eq!(left("hi", 5), "hi   ");
        assert_eq!(left("hello", 3), "hello");
    }

    #[test]
    fn test_right() {
        assert_eq!(right("hi", 5), "   hi");
        assert_eq!(right("hello", 3), "hello");
    }

    #[test]
    fn test_center() {
        assert_eq!(center("hi", 4), " hi ");
        assert_eq!(center("hi", 5), " hi  ");
        assert_eq!(center("hello", 3), "hello");
    }

    #[test]
    fn test_center_with() {
        assert_eq!(center_with("hi", 6, '-'), "--hi--");
    }

    #[test]
    fn test_truncate() {
        assert_eq!(truncate("hello", 10), "hello");
        // "hello world" (11 chars) truncated to 8 should give "hello w…" (8 chars)
        let truncated = truncate("hello world", 8);
        assert_eq!(display_width(&truncated), 8);
        assert!(truncated.ends_with('…'));
        assert_eq!(truncate("hi", 1), "…");
    }

    #[test]
    fn test_display_width() {
        assert_eq!(display_width("hello"), 5);
        assert_eq!(display_width("你好"), 4); // Chinese chars are wide
        assert_eq!(display_width("abc"), 3);
    }

    #[test]
    fn test_distribute() {
        let result = distribute(&["a", "b"], 10);
        // "a" + spaces + "b" = 10 chars total
        assert_eq!(result.len(), 10);
    }

    #[test]
    fn test_repeat_to_width() {
        assert_eq!(repeat_to_width("ab", 7), "abababa");
        assert_eq!(repeat_to_width("-", 5), "-----");
    }
}