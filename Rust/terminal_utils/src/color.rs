//! ANSI Color utilities
//! 
//! Provides foreground and background color codes for terminal output.

/// Standard ANSI color codes
pub const BLACK: &str = "30";
pub const RED: &str = "31";
pub const GREEN: &str = "32";
pub const YELLOW: &str = "33";
pub const BLUE: &str = "34";
pub const MAGENTA: &str = "35";
pub const CYAN: &str = "36";
pub const WHITE: &str = "37";
pub const BRIGHT_BLACK: &str = "90";
pub const BRIGHT_RED: &str = "91";
pub const BRIGHT_GREEN: &str = "92";
pub const BRIGHT_YELLOW: &str = "93";
pub const BRIGHT_BLUE: &str = "94";
pub const BRIGHT_MAGENTA: &str = "95";
pub const BRIGHT_CYAN: &str = "96";
pub const BRIGHT_WHITE: &str = "97";

/// Standard ANSI background color codes
pub const BG_BLACK: &str = "40";
pub const BG_RED: &str = "41";
pub const BG_GREEN: &str = "42";
pub const BG_YELLOW: &str = "43";
pub const BG_BLUE: &str = "44";
pub const BG_MAGENTA: &str = "45";
pub const BG_CYAN: &str = "46";
pub const BG_WHITE: &str = "47";
pub const BG_BRIGHT_BLACK: &str = "100";
pub const BG_BRIGHT_RED: &str = "101";
pub const BG_BRIGHT_GREEN: &str = "102";
pub const BG_BRIGHT_YELLOW: &str = "103";
pub const BG_BRIGHT_BLUE: &str = "104";
pub const BG_BRIGHT_MAGENTA: &str = "105";
pub const BG_BRIGHT_CYAN: &str = "106";
pub const BG_BRIGHT_WHITE: &str = "107";

/// Returns the ANSI escape sequence for foreground color
/// 
/// # Arguments
/// * `color_code` - The ANSI color code (e.g., "31" for red)
/// 
/// # Example
/// ```rust
/// use terminal_utils::color;
/// println!("{}Red text!{}", color::fg(color::RED), color::reset());
/// ```
pub fn fg(color_code: &str) -> String {
    format!("\x1b[{}m", color_code)
}

/// Returns the ANSI escape sequence for background color
/// 
/// # Arguments
/// * `color_code` - The ANSI background color code (e.g., "41" for red background)
/// 
/// # Example
/// ```rust
/// use terminal_utils::color;
/// println!("{}Red background!{}", color::bg(color::BG_RED), color::reset());
/// ```
pub fn bg(color_code: &str) -> String {
    format!("\x1b[{}m", color_code)
}

/// Returns the ANSI 256-color escape sequence for foreground
/// 
/// # Arguments
/// * `color_index` - Color index (0-255)
/// 
/// # Example
/// ```rust
/// use terminal_utils::color;
/// println!("{}Custom color!{}", color::fg_256(208), color::reset());
/// ```
pub fn fg_256(color_index: u8) -> String {
    format!("\x1b[38;5;{}m", color_index)
}

/// Returns the ANSI 256-color escape sequence for background
/// 
/// # Arguments
/// * `color_index` - Color index (0-255)
pub fn bg_256(color_index: u8) -> String {
    format!("\x1b[48;5;{}m", color_index)
}

/// Returns the ANSI RGB escape sequence for foreground
/// 
/// # Arguments
/// * `r` - Red component (0-255)
/// * `g` - Green component (0-255)
/// * `b` - Blue component (0-255)
pub fn fg_rgb(r: u8, g: u8, b: u8) -> String {
    format!("\x1b[38;2;{};{};{}m", r, g, b)
}

/// Returns the ANSI RGB escape sequence for background
/// 
/// # Arguments
/// * `r` - Red component (0-255)
/// * `g` - Green component (0-255)
/// * `b` - Blue component (0-255)
pub fn bg_rgb(r: u8, g: u8, b: u8) -> String {
    format!("\x1b[48;2;{};{};{}m", r, g, b)
}

/// Returns the ANSI reset sequence
/// 
/// This clears all styling (colors, bold, etc.)
pub fn reset() -> String {
    "\x1b[0m".to_string()
}

/// Convenience function to colorize text
/// 
/// # Arguments
/// * `text` - The text to colorize
/// * `color_code` - The ANSI color code
/// 
/// # Example
/// ```rust
/// use terminal_utils::color;
/// println!("{}", color::colorize("Hello", color::GREEN));
/// ```
pub fn colorize(text: &str, color_code: &str) -> String {
    format!("\x1b[{}m{}\x1b[0m", color_code, text)
}

/// Colorize text with RGB values
pub fn colorize_rgb(text: &str, r: u8, g: u8, b: u8) -> String {
    format!("\x1b[38;2;{};{};{}m{}\x1b[0m", r, g, b, text)
}

/// Convenience functions for common colors
pub fn black(text: &str) -> String { colorize(text, BLACK) }
pub fn red(text: &str) -> String { colorize(text, RED) }
pub fn green(text: &str) -> String { colorize(text, GREEN) }
pub fn yellow(text: &str) -> String { colorize(text, YELLOW) }
pub fn blue(text: &str) -> String { colorize(text, BLUE) }
pub fn magenta(text: &str) -> String { colorize(text, MAGENTA) }
pub fn cyan(text: &str) -> String { colorize(text, CYAN) }
pub fn white(text: &str) -> String { colorize(text, WHITE) }

/// Convenience functions for bright colors
pub fn bright_black(text: &str) -> String { colorize(text, BRIGHT_BLACK) }
pub fn bright_red(text: &str) -> String { colorize(text, BRIGHT_RED) }
pub fn bright_green(text: &str) -> String { colorize(text, BRIGHT_GREEN) }
pub fn bright_yellow(text: &str) -> String { colorize(text, BRIGHT_YELLOW) }
pub fn bright_blue(text: &str) -> String { colorize(text, BRIGHT_BLUE) }
pub fn bright_magenta(text: &str) -> String { colorize(text, BRIGHT_MAGENTA) }
pub fn bright_cyan(text: &str) -> String { colorize(text, BRIGHT_CYAN) }
pub fn bright_white(text: &str) -> String { colorize(text, BRIGHT_WHITE) }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fg() {
        assert_eq!(fg(RED), "\x1b[31m");
    }

    #[test]
    fn test_bg() {
        assert_eq!(bg(BG_RED), "\x1b[41m");
    }

    #[test]
    fn test_reset() {
        assert_eq!(reset(), "\x1b[0m");
    }

    #[test]
    fn test_colorize() {
        assert_eq!(colorize("test", RED), "\x1b[31mtest\x1b[0m");
    }

    #[test]
    fn test_convenience_colors() {
        assert_eq!(red("error"), "\x1b[31merror\x1b[0m");
        assert_eq!(green("success"), "\x1b[32msuccess\x1b[0m");
    }

    #[test]
    fn test_rgb_colors() {
        assert_eq!(fg_rgb(255, 128, 0), "\x1b[38;2;255;128;0m");
        assert_eq!(bg_rgb(0, 128, 255), "\x1b[48;2;0;128;255m");
    }

    #[test]
    fn test_256_colors() {
        assert_eq!(fg_256(208), "\x1b[38;5;208m");
        assert_eq!(bg_256(17), "\x1b[48;5;17m");
    }
}