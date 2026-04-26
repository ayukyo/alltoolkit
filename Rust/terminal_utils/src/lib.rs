//! # Terminal Utils
//! 
//! A comprehensive terminal utility library for Rust with zero external dependencies.
//! 
//! ## Features
//! 
//! - **ANSI Colors**: Foreground and background colors with reset support
//! - **Text Styles**: Bold, italic, underline, strikethrough, and more
//! - **Cursor Control**: Move cursor, save/restore position, hide/show
//! - **Screen Control**: Clear screen, clear lines, scroll
//! - **Terminal Size**: Detect terminal dimensions (via env vars)
//! - **Progress Bar**: Simple progress indicators
//! - **Text Alignment**: Left, center, right alignment utilities
//! - **Tables**: Simple table rendering with borders
//! 
//! ## Example
//! 
//! ```rust
//! use terminal_utils::{color, style, cursor, progress};
//! 
//! // Print colored text
//! println!("{}Hello, World!{}", color::fg(color::GREEN), color::reset());
//! 
//! // Print styled text
//! println!("{}Bold and {}Underline!{}", 
//!     style::BOLD, style::UNDERLINE, style::RESET);
//! 
//! // Show a progress bar
//! for i in 0..=100 {
//!     print!("\r{}", progress::bar(i, 100, 30));
//! }
//! println!();
//! ```

pub mod color;
pub mod style;
pub mod cursor;
pub mod screen;
pub mod terminal;
pub mod progress;
pub mod align;
pub mod table;