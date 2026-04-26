//! Screen control utilities
//! 
//! Provides ANSI escape codes for screen manipulation.

/// Clear screen
pub const CLEAR_SCREEN: &str = "\x1b[2J";
/// Clear from cursor to end of screen
pub const CLEAR_TO_END: &str = "\x1b[0J";
/// Clear from cursor to start of screen
pub const CLEAR_TO_START: &str = "\x1b[1J";
/// Clear entire line
pub const CLEAR_LINE: &str = "\x1b[2K";
/// Clear from cursor to end of line
pub const CLEAR_LINE_TO_END: &str = "\x1b[0K";
/// Clear from cursor to start of line
pub const CLEAR_LINE_TO_START: &str = "\x1b[1K";

/// Clear the entire screen
pub fn clear_screen() -> String {
    CLEAR_SCREEN.to_string()
}

/// Clear screen and move cursor to home
pub fn clear() -> String {
    format!("{}{}", CLEAR_SCREEN, "\x1b[H")
}

/// Clear from cursor to end of screen
pub fn clear_to_end() -> String {
    CLEAR_TO_END.to_string()
}

/// Clear from cursor to start of screen
pub fn clear_to_start() -> String {
    CLEAR_TO_START.to_string()
}

/// Clear entire line
pub fn clear_line() -> String {
    CLEAR_LINE.to_string()
}

/// Clear from cursor to end of line
pub fn clear_line_to_end() -> String {
    CLEAR_LINE_TO_END.to_string()
}

/// Clear from cursor to start of line
pub fn clear_line_to_start() -> String {
    CLEAR_LINE_TO_START.to_string()
}

/// Scroll screen up by n lines
pub fn scroll_up(n: u16) -> String {
    format!("\x1b[{}S", n)
}

/// Scroll screen down by n lines
pub fn scroll_down(n: u16) -> String {
    format!("\x1b[{}T", n)
}

/// Set scrolling region
pub fn set_scroll_region(top: u16, bottom: u16) -> String {
    format!("\x1b[{};{}r", top, bottom)
}

/// Insert n blank lines
pub fn insert_lines(n: u16) -> String {
    format!("\x1b[{}L", n)
}

/// Delete n lines
pub fn delete_lines(n: u16) -> String {
    format!("\x1b[{}M", n)
}

/// Insert n blank characters
pub fn insert_chars(n: u16) -> String {
    format!("\x1b[{}@", n)
}

/// Delete n characters
pub fn delete_chars(n: u16) -> String {
    format!("\x1b[{}P", n)
}

/// Erase n characters (replace with space)
pub fn erase_chars(n: u16) -> String {
    format!("\x1b[{}X", n)
}

/// Enter alternate screen buffer
pub fn enter_alt_screen() -> String {
    "\x1b[?1049h".to_string()
}

/// Exit alternate screen buffer
pub fn exit_alt_screen() -> String {
    "\x1b[?1049l".to_string()
}

/// Enable line wrapping
pub fn enable_line_wrap() -> String {
    "\x1b[?7h".to_string()
}

/// Disable line wrapping
pub fn disable_line_wrap() -> String {
    "\x1b[?7l".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_clear_screen() {
        assert_eq!(clear_screen(), "\x1b[2J");
    }

    #[test]
    fn test_clear() {
        assert_eq!(clear(), "\x1b[2J\x1b[H");
    }

    #[test]
    fn test_clear_line() {
        assert_eq!(clear_line(), "\x1b[2K");
    }

    #[test]
    fn test_scroll() {
        assert_eq!(scroll_up(5), "\x1b[5S");
        assert_eq!(scroll_down(3), "\x1b[3T");
    }

    #[test]
    fn test_insert_delete_lines() {
        assert_eq!(insert_lines(2), "\x1b[2L");
        assert_eq!(delete_lines(1), "\x1b[1M");
    }

    #[test]
    fn test_alt_screen() {
        assert_eq!(enter_alt_screen(), "\x1b[?1049h");
        assert_eq!(exit_alt_screen(), "\x1b[?1049l");
    }
}