//! Text style utilities
//! 
//! Provides ANSI escape codes for text styling.

/// Bold text
pub const BOLD: &str = "\x1b[1m";
/// Dim/faint text
pub const DIM: &str = "\x1b[2m";
/// Italic text
pub const ITALIC: &str = "\x1b[3m";
/// Underlined text
pub const UNDERLINE: &str = "\x1b[4m";
/// Blinking text (slow)
pub const BLINK: &str = "\x1b[5m";
/// Reverse video (swap foreground/background)
pub const REVERSE: &str = "\x1b[7m";
/// Hidden/invisible text
pub const HIDDEN: &str = "\x1b[8m";
/// Strikethrough text
pub const STRIKETHROUGH: &str = "\x1b[9m";
/// Double underline
pub const DOUBLE_UNDERLINE: &str = "\x1b[21m";
/// Overlined text
pub const OVERLINE: &str = "\x1b[53m";

/// Reset all styles
pub const RESET: &str = "\x1b[0m";
/// Reset bold
pub const RESET_BOLD: &str = "\x1b[22m";
/// Reset dim
pub const RESET_DIM: &str = "\x1b[22m";
/// Reset italic
pub const RESET_ITALIC: &str = "\x1b[23m";
/// Reset underline
pub const RESET_UNDERLINE: &str = "\x1b[24m";
/// Reset blink
pub const RESET_BLINK: &str = "\x1b[25m";
/// Reset reverse
pub const RESET_REVERSE: &str = "\x1b[27m";
/// Reset hidden
pub const RESET_HIDDEN: &str = "\x1b[28m";
/// Reset strikethrough
pub const RESET_STRIKETHROUGH: &str = "\x1b[29m";
/// Reset overline
pub const RESET_OVERLINE: &str = "\x1b[55m";

/// Apply bold style to text
pub fn bold(text: &str) -> String {
    format!("{}{}{}", BOLD, text, RESET)
}

/// Apply dim style to text
pub fn dim(text: &str) -> String {
    format!("{}{}{}", DIM, text, RESET)
}

/// Apply italic style to text
pub fn italic(text: &str) -> String {
    format!("{}{}{}", ITALIC, text, RESET)
}

/// Apply underline style to text
pub fn underline(text: &str) -> String {
    format!("{}{}{}", UNDERLINE, text, RESET)
}

/// Apply strikethrough style to text
pub fn strikethrough(text: &str) -> String {
    format!("{}{}{}", STRIKETHROUGH, text, RESET)
}

/// Apply blink style to text
pub fn blink(text: &str) -> String {
    format!("{}{}{}", BLINK, text, RESET)
}

/// Apply reverse video to text
pub fn reverse(text: &str) -> String {
    format!("{}{}{}", REVERSE, text, RESET)
}

/// Apply hidden style to text
pub fn hidden(text: &str) -> String {
    format!("{}{}{}", HIDDEN, text, RESET)
}

/// Apply overline style to text
pub fn overline(text: &str) -> String {
    format!("{}{}{}", OVERLINE, text, RESET)
}

/// Apply double underline style to text
pub fn double_underline(text: &str) -> String {
    format!("{}{}{}", DOUBLE_UNDERLINE, text, RESET)
}

/// Combine multiple styles
/// 
/// # Example
/// ```rust
/// use terminal_utils::style;
/// let styled = style::combine("Bold and Italic", &[style::BOLD, style::ITALIC]);
/// ```
pub fn combine(text: &str, styles: &[&str]) -> String {
    let prefix: String = styles.iter().map(|s| s.to_string()).collect();
    format!("{}{}{}", prefix, text, RESET)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bold() {
        assert_eq!(bold("test"), "\x1b[1mtest\x1b[0m");
    }

    #[test]
    fn test_italic() {
        assert_eq!(italic("test"), "\x1b[3mtest\x1b[0m");
    }

    #[test]
    fn test_underline() {
        assert_eq!(underline("test"), "\x1b[4mtest\x1b[0m");
    }

    #[test]
    fn test_strikethrough() {
        assert_eq!(strikethrough("test"), "\x1b[9mtest\x1b[0m");
    }

    #[test]
    fn test_combine() {
        let result = combine("test", &[BOLD, ITALIC]);
        assert!(result.starts_with("\x1b[1m\x1b[3m"));
        assert!(result.ends_with("\x1b[0m"));
    }
}