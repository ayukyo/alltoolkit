//! Terminal size and info utilities
//! 
//! Provides terminal size detection and information.

use std::io::{self, IsTerminal};

/// Terminal size information
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Size {
    pub width: u16,
    pub height: u16,
}

impl Size {
    pub fn new(width: u16, height: u16) -> Self {
        Self { width, height }
    }

    /// Returns the number of columns (width)
    pub fn cols(&self) -> u16 {
        self.width
    }

    /// Returns the number of rows (height)
    pub fn rows(&self) -> u16 {
        self.height
    }

    /// Check if size is valid (both dimensions > 0)
    pub fn is_valid(&self) -> bool {
        self.width > 0 && self.height > 0
    }

    /// Calculate center position for content of given width
    pub fn center_col(&self, content_width: usize) -> u16 {
        if content_width as u16 >= self.width {
            1
        } else {
            (self.width - content_width as u16) / 2 + 1
        }
    }
}

/// Get terminal size - uses environment variables and fallback
/// 
/// Note: For accurate terminal size detection, consider using a crate like `term_size`
/// or `crossterm`. This implementation uses environment variables as a zero-dependency approach.
pub fn size() -> io::Result<Size> {
    // Try environment variables first
    if let (Ok(cols), Ok(rows)) = (
        std::env::var("COLUMNS"),
        std::env::var("LINES")
    ) {
        if let (Ok(cols), Ok(rows)) = (cols.parse::<u16>(), rows.parse::<u16>()) {
            if cols > 0 && rows > 0 {
                return Ok(Size::new(cols, rows));
            }
        }
    }
    
    // Try LINES and COLS (alternate env vars)
    if let (Ok(cols), Ok(rows)) = (
        std::env::var("COLS"),
        std::env::var("LINES")
    ) {
        if let (Ok(cols), Ok(rows)) = (cols.parse::<u16>(), rows.parse::<u16>()) {
            if cols > 0 && rows > 0 {
                return Ok(Size::new(cols, rows));
            }
        }
    }
    
    // Default fallback for terminals
    Ok(Size::new(80, 24))
}

/// Get terminal size with default fallback
pub fn size_or_default() -> Size {
    size().unwrap_or(Size::new(80, 24))
}

/// Check if stdout is connected to a terminal
pub fn is_terminal() -> bool {
    io::stdout().is_terminal()
}

/// Check if stderr is connected to a terminal
pub fn is_stderr_terminal() -> bool {
    io::stderr().is_terminal()
}

/// Check if stdin is connected to a terminal
pub fn is_stdin_terminal() -> bool {
    io::stdin().is_terminal()
}

/// Get terminal width
pub fn width() -> u16 {
    size_or_default().width
}

/// Get terminal height
pub fn height() -> u16 {
    size_or_default().height
}

/// Check if terminal supports colors
pub fn supports_color() -> bool {
    // Check COLORTERM for true color support
    if let Ok(color_term) = std::env::var("COLORTERM") {
        if color_term == "truecolor" || color_term == "24bit" {
            return true;
        }
    }
    
    // Check TERM for basic color support
    if let Ok(term) = std::env::var("TERM") {
        if term.contains("color") || term.contains("256") {
            return true;
        }
    }
    
    // Check NO_COLOR environment variable
    if std::env::var("NO_COLOR").is_ok() {
        return false;
    }
    
    is_terminal()
}

/// Get color level: 0 (none), 16 (basic), 256, or 16777216 (true color)
pub fn color_level() -> usize {
    if !is_terminal() {
        return 0;
    }
    
    if let Ok(color_term) = std::env::var("COLORTERM") {
        if color_term == "truecolor" || color_term == "24bit" {
            return 16_777_216;
        }
    }
    
    if let Ok(term) = std::env::var("TERM") {
        if term.contains("256") || term.contains("xterm") {
            return 256;
        }
        if term.contains("color") {
            return 16;
        }
    }
    
    16
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_size() {
        let size = Size::new(100, 50);
        assert_eq!(size.width, 100);
        assert_eq!(size.height, 50);
        assert_eq!(size.cols(), 100);
        assert_eq!(size.rows(), 50);
    }

    #[test]
    fn test_size_valid() {
        assert!(Size::new(80, 24).is_valid());
        assert!(!Size::new(0, 24).is_valid());
        assert!(!Size::new(80, 0).is_valid());
    }

    #[test]
    fn test_center_col() {
        let size = Size::new(100, 24);
        // Content of width 20 should center around column 41
        assert_eq!(size.center_col(20), 41);
        // Content wider than terminal starts at column 1
        assert_eq!(size.center_col(120), 1);
    }

    #[test]
    fn test_size_or_default() {
        let size = size_or_default();
        assert!(size.is_valid());
    }

    #[test]
    fn test_supports_color() {
        // Just check it doesn't panic
        let _ = supports_color();
    }

    #[test]
    fn test_color_level() {
        let level = color_level();
        assert!(level == 0 || level == 16 || level == 256 || level == 16_777_216);
    }
}