//! Cursor control utilities
//! 
//! Provides ANSI escape codes for cursor manipulation.

/// Hide the cursor
pub const HIDE: &str = "\x1b[?25l";
/// Show the cursor
pub const SHOW: &str = "\x1b[?25h";
/// Save cursor position
pub const SAVE: &str = "\x1b[s";
/// Restore cursor position
pub const RESTORE: &str = "\x1b[u";

/// Move cursor to home position (1,1)
pub fn home() -> String {
    "\x1b[H".to_string()
}

/// Move cursor to specific position
/// 
/// # Arguments
/// * `row` - Row number (1-indexed)
/// * `col` - Column number (1-indexed)
pub fn to_pos(row: u16, col: u16) -> String {
    format!("\x1b[{};{}H", row, col)
}

/// Move cursor to specific position (alternate format)
/// 
/// # Arguments
/// * `row` - Row number (1-indexed)
/// * `col` - Column number (1-indexed)
pub fn to(row: u16, col: u16) -> String {
    format!("\x1b[{};{}f", row, col)
}

/// Move cursor up by n rows
pub fn up(n: u16) -> String {
    format!("\x1b[{}A", n)
}

/// Move cursor down by n rows
pub fn down(n: u16) -> String {
    format!("\x1b[{}B", n)
}

/// Move cursor right by n columns
pub fn right(n: u16) -> String {
    format!("\x1b[{}C", n)
}

/// Move cursor left by n columns
pub fn left(n: u16) -> String {
    format!("\x1b[{}D", n)
}

/// Move cursor to beginning of line
pub fn line_start() -> String {
    "\r".to_string()
}

/// Move cursor to beginning of next line
pub fn next_line(n: u16) -> String {
    format!("\x1b[{}E", n)
}

/// Move cursor to beginning of previous line
pub fn prev_line(n: u16) -> String {
    format!("\x1b[{}F", n)
}

/// Move cursor to specific column
pub fn to_col(col: u16) -> String {
    format!("\x1b[{}G", col)
}

/// Hide cursor
pub fn hide() -> String {
    HIDE.to_string()
}

/// Show cursor
pub fn show() -> String {
    SHOW.to_string()
}

/// Save cursor position
pub fn save() -> String {
    SAVE.to_string()
}

/// Restore cursor position
pub fn restore() -> String {
    RESTORE.to_string()
}

/// Request cursor position report (terminal will respond with \x1b[row;colR)
pub fn request_pos() -> String {
    "\x1b[6n".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_to_pos() {
        assert_eq!(to_pos(5, 10), "\x1b[5;10H");
    }

    #[test]
    fn test_movements() {
        assert_eq!(up(3), "\x1b[3A");
        assert_eq!(down(2), "\x1b[2B");
        assert_eq!(right(5), "\x1b[5C");
        assert_eq!(left(1), "\x1b[1D");
    }

    #[test]
    fn test_line_movements() {
        assert_eq!(next_line(2), "\x1b[2E");
        assert_eq!(prev_line(1), "\x1b[1F");
        assert_eq!(to_col(10), "\x1b[10G");
    }

    #[test]
    fn test_hide_show() {
        assert_eq!(hide(), "\x1b[?25l");
        assert_eq!(show(), "\x1b[?25h");
    }

    #[test]
    fn test_save_restore() {
        assert_eq!(save(), "\x1b[s");
        assert_eq!(restore(), "\x1b[u");
    }
}