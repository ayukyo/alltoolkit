//! Color Utils - A comprehensive color manipulation library
//! 
//! This crate provides color conversion, manipulation, and analysis utilities
//! without any external dependencies.
//!
//! # Supported Color Spaces
//! - RGB (Red, Green, Blue)
//! - HSL (Hue, Saturation, Lightness)
//! - HSV (HSB) (Hue, Saturation, Value/Brightness)
//! - CMYK (Cyan, Magenta, Yellow, Key/Black)
//! - HEX (Hexadecimal color codes)
//!
//! # Example
//! ```
//! use color_utils::{Color, ColorSpace};
//!
//! let rgb = Color::rgb(255, 128, 64);
//! let hex = rgb.to_hex();
//! println!("HEX: {}", hex); // #FF8040
//! ```

use std::fmt;
use std::str::FromStr;

/// Represents different color spaces
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ColorSpace {
    RGB,
    HSL,
    HSV,
    CMYK,
}

/// A color representation with RGB values
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Color {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}

impl Color {
    /// Creates a new RGB color
    pub fn rgb(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b, a: 255 }
    }

    /// Creates a new RGBA color
    pub fn rgba(r: u8, g: u8, b: u8, a: u8) -> Self {
        Self { r, g, b, a }
    }

    /// Creates a color from HSL values
    /// H: 0-360, S: 0-100, L: 0-100
    pub fn hsl(h: u16, s: u8, l: u8) -> Self {
        let (r, g, b) = hsl_to_rgb(h, s, l);
        Self::rgb(r, g, b)
    }

    /// Creates a color from HSV values
    /// H: 0-360, S: 0-100, V: 0-100
    pub fn hsv(h: u16, s: u8, v: u8) -> Self {
        let (r, g, b) = hsv_to_rgb(h, s, v);
        Self::rgb(r, g, b)
    }

    /// Creates a color from CMYK values
    /// C, M, Y, K: 0-100
    pub fn cmyk(c: u8, m: u8, y: u8, k: u8) -> Self {
        let (r, g, b) = cmyk_to_rgb(c, m, y, k);
        Self::rgb(r, g, b)
    }

    /// Creates a color from a hex string
    pub fn from_hex(hex: &str) -> Result<Self, ColorError> {
        let hex = hex.trim_start_matches('#');
        
        match hex.len() {
            3 => {
                let r = u8::from_str_radix(&hex[0..1].repeat(2), 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let g = u8::from_str_radix(&hex[1..2].repeat(2), 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let b = u8::from_str_radix(&hex[2..3].repeat(2), 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                Ok(Self::rgb(r, g, b))
            }
            6 => {
                let r = u8::from_str_radix(&hex[0..2], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let g = u8::from_str_radix(&hex[2..4], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let b = u8::from_str_radix(&hex[4..6], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                Ok(Self::rgb(r, g, b))
            }
            8 => {
                let r = u8::from_str_radix(&hex[0..2], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let g = u8::from_str_radix(&hex[2..4], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let b = u8::from_str_radix(&hex[4..6], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                let a = u8::from_str_radix(&hex[6..8], 16)
                    .map_err(|_| ColorError::InvalidHexFormat)?;
                Ok(Self::rgba(r, g, b, a))
            }
            _ => Err(ColorError::InvalidHexFormat),
        }
    }

    /// Returns RGB values as a tuple
    pub fn as_rgb(&self) -> (u8, u8, u8) {
        (self.r, self.g, self.b)
    }

    /// Returns RGBA values as a tuple
    pub fn as_rgba(&self) -> (u8, u8, u8, u8) {
        (self.r, self.g, self.b, self.a)
    }

    /// Converts to HSL color space
    /// Returns (H, S, L) where H: 0-360, S: 0-100, L: 0-100
    pub fn to_hsl(&self) -> (u16, u8, u8) {
        rgb_to_hsl(self.r, self.g, self.b)
    }

    /// Converts to HSV color space
    /// Returns (H, S, V) where H: 0-360, S: 0-100, V: 0-100
    pub fn to_hsv(&self) -> (u16, u8, u8) {
        rgb_to_hsv(self.r, self.g, self.b)
    }

    /// Converts to CMYK color space
    /// Returns (C, M, Y, K) where each value is 0-100
    pub fn to_cmyk(&self) -> (u8, u8, u8, u8) {
        rgb_to_cmyk(self.r, self.g, self.b)
    }

    /// Converts to hex string (with alpha if present)
    pub fn to_hex(&self) -> String {
        if self.a == 255 {
            format!("#{:02X}{:02X}{:02X}", self.r, self.g, self.b)
        } else {
            format!("#{:02X}{:02X}{:02X}{:02X}", self.r, self.g, self.b, self.a)
        }
    }

    /// Converts to RGB hex string (ignores alpha)
    pub fn to_hex_rgb(&self) -> String {
        format!("#{:02X}{:02X}{:02X}", self.r, self.g, self.b)
    }

    /// Returns the red component
    pub fn red(&self) -> u8 {
        self.r
    }

    /// Returns the green component
    pub fn green(&self) -> u8 {
        self.g
    }

    /// Returns the blue component
    pub fn blue(&self) -> u8 {
        self.b
    }

    /// Returns the alpha component
    pub fn alpha(&self) -> u8 {
        self.a
    }

    /// Sets the alpha value
    pub fn with_alpha(mut self, a: u8) -> Self {
        self.a = a;
        self
    }

    /// Calculates the relative luminance (0.0 - 1.0)
    /// Using sRGB luminance coefficients
    pub fn luminance(&self) -> f64 {
        let r = self.r as f64 / 255.0;
        let g = self.g as f64 / 255.0;
        let b = self.b as f64 / 255.0;
        
        // Apply gamma correction
        let r = if r <= 0.03928 { r / 12.92 } else { ((r + 0.055) / 1.055).powf(2.4) };
        let g = if g <= 0.03928 { g / 12.92 } else { ((g + 0.055) / 1.055).powf(2.4) };
        let b = if b <= 0.03928 { b / 12.92 } else { ((b + 0.055) / 1.055).powf(2.4) };
        
        0.2126 * r + 0.7152 * g + 0.0722 * b
    }

    /// Determines if the color is considered "light"
    pub fn is_light(&self) -> bool {
        self.luminance() > 0.5
    }

    /// Determines if the color is considered "dark"
    pub fn is_dark(&self) -> bool {
        !self.is_light()
    }

    /// Calculates contrast ratio with another color
    /// Returns a value between 1.0 and 21.0
    pub fn contrast_ratio(&self, other: &Color) -> f64 {
        let l1 = self.luminance();
        let l2 = other.luminance();
        
        let lighter = l1.max(l2);
        let darker = l1.min(l2);
        
        (lighter + 0.05) / (darker + 0.05)
    }

    /// Gets the WCAG contrast level
    /// Returns: AAA (7:1+), AA (4.5:1+), AA_Large (3:1+), or Fail
    pub fn contrast_level(&self, other: &Color) -> ContrastLevel {
        let ratio = self.contrast_ratio(other);
        
        if ratio >= 7.0 {
            ContrastLevel::AAA
        } else if ratio >= 4.5 {
            ContrastLevel::AA
        } else if ratio >= 3.0 {
            ContrastLevel::AA_Large
        } else {
            ContrastLevel::Fail
        }
    }

    /// Returns a complementary color
    pub fn complementary(&self) -> Color {
        let (h, s, l) = self.to_hsl();
        let new_h = (h + 180) % 360;
        Color::hsl(new_h, s, l)
    }

    /// Mixes two colors together
    /// weight: 0.0 = 100% self, 1.0 = 100% other
    pub fn mix(&self, other: &Color, weight: f64) -> Color {
        let weight = weight.clamp(0.0, 1.0);
        let self_weight = 1.0 - weight;
        
        let r = (self.r as f64 * self_weight + other.r as f64 * weight).round() as u8;
        let g = (self.g as f64 * self_weight + other.g as f64 * weight).round() as u8;
        let b = (self.b as f64 * self_weight + other.b as f64 * weight).round() as u8;
        let a = (self.a as f64 * self_weight + other.a as f64 * weight).round() as u8;
        
        Color::rgba(r, g, b, a)
    }

    /// Lightens the color by a percentage (0-100)
    pub fn lighten(&self, amount: u8) -> Color {
        let (h, s, l) = self.to_hsl();
        let new_l = (l as u16 + amount as u16).min(100) as u8;
        Color::hsl(h, s, new_l)
    }

    /// Darkens the color by a percentage (0-100)
    pub fn darken(&self, amount: u8) -> Color {
        let (h, s, l) = self.to_hsl();
        let new_l = l.saturating_sub(amount);
        Color::hsl(h, s, new_l)
    }

    /// Saturates the color by a percentage (0-100)
    pub fn saturate(&self, amount: u8) -> Color {
        let (h, s, l) = self.to_hsl();
        let new_s = (s as u16 + amount as u16).min(100) as u8;
        Color::hsl(h, new_s, l)
    }

    /// Desaturates the color by a percentage (0-100)
    pub fn desaturate(&self, amount: u8) -> Color {
        let (h, s, l) = self.to_hsl();
        let new_s = s.saturating_sub(amount);
        Color::hsl(h, new_s, l)
    }

    /// Returns a grayscale version of the color
    pub fn grayscale(&self) -> Color {
        let gray = (0.299 * self.r as f64 + 0.587 * self.g as f64 + 0.114 * self.b as f64) as u8;
        Color::rgb(gray, gray, gray)
    }

    /// Inverts the color
    pub fn invert(&self) -> Color {
        Color::rgba(255 - self.r, 255 - self.g, 255 - self.b, self.a)
    }

    /// Returns the color name if it's a named CSS color
    pub fn name(&self) -> Option<&'static str> {
        color_name(self.r, self.g, self.b)
    }

    /// Generates a triadic color scheme (3 colors 120° apart)
    pub fn triadic(&self) -> [Color; 3] {
        let (h, s, l) = self.to_hsl();
        [
            *self,
            Color::hsl((h + 120) % 360, s, l),
            Color::hsl((h + 240) % 360, s, l),
        ]
    }

    /// Generates an analogous color scheme (3 colors 30° apart)
    pub fn analogous(&self) -> [Color; 3] {
        let (h, s, l) = self.to_hsl();
        [
            Color::hsl((h + 330) % 360, s, l),
            *self,
            Color::hsl((h + 30) % 360, s, l),
        ]
    }

    /// Generates a split-complementary color scheme
    pub fn split_complementary(&self) -> [Color; 3] {
        let (h, s, l) = self.to_hsl();
        [
            *self,
            Color::hsl((h + 150) % 360, s, l),
            Color::hsl((h + 210) % 360, s, l),
        ]
    }
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "rgb({}, {}, {})", self.r, self.g, self.b)
    }
}

impl FromStr for Color {
    type Err = ColorError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Color::from_hex(s)
    }
}

/// Contrast level according to WCAG guidelines
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ContrastLevel {
    /// Ratio >= 7:1 (AAA for normal text)
    AAA,
    /// Ratio >= 4.5:1 (AA for normal text)
    AA,
    /// Ratio >= 3:1 (AA for large text)
    AA_Large,
    /// Ratio < 3:1 (fails WCAG)
    Fail,
}

impl fmt::Display for ContrastLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ContrastLevel::AAA => write!(f, "AAA (≥7:1)"),
            ContrastLevel::AA => write!(f, "AA (≥4.5:1)"),
            ContrastLevel::AA_Large => write!(f, "AA Large (≥3:1)"),
            ContrastLevel::Fail => write!(f, "Fail (<3:1)"),
        }
    }
}

/// Color parsing/conversion errors
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ColorError {
    InvalidHexFormat,
    InvalidColorValue,
}

impl fmt::Display for ColorError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ColorError::InvalidHexFormat => write!(f, "Invalid hex color format"),
            ColorError::InvalidColorValue => write!(f, "Invalid color value"),
        }
    }
}

impl std::error::Error for ColorError {}

// ==================== Conversion Functions ====================

/// Converts HSL to RGB
/// H: 0-360, S: 0-100, L: 0-100
fn hsl_to_rgb(h: u16, s: u8, l: u8) -> (u8, u8, u8) {
    let h = h % 360;
    let s = s as f64 / 100.0;
    let l = l as f64 / 100.0;

    if s == 0.0 {
        let gray = (l * 255.0).round() as u8;
        return (gray, gray, gray);
    }

    let c = (1.0 - (2.0 * l - 1.0).abs()) * s;
    let x = c * (1.0 - ((h as f64 / 60.0) % 2.0 - 1.0).abs());
    let m = l - c / 2.0;

    let (r, g, b) = match h {
        0..=59 => (c, x, 0.0),
        60..=119 => (x, c, 0.0),
        120..=179 => (0.0, c, x),
        180..=239 => (0.0, x, c),
        240..=299 => (x, 0.0, c),
        _ => (c, 0.0, x),
    };

    (
        ((r + m) * 255.0).round() as u8,
        ((g + m) * 255.0).round() as u8,
        ((b + m) * 255.0).round() as u8,
    )
}

/// Converts RGB to HSL
/// Returns (H, S, L) where H: 0-360, S: 0-100, L: 0-100
fn rgb_to_hsl(r: u8, g: u8, b: u8) -> (u16, u8, u8) {
    let r = r as f64 / 255.0;
    let g = g as f64 / 255.0;
    let b = b as f64 / 255.0;

    let max = r.max(g).max(b);
    let min = r.min(g).min(b);
    let delta = max - min;

    let l = (max + min) / 2.0;

    if delta == 0.0 {
        return (0, 0, (l * 100.0).round() as u8);
    }

    let s = if l > 0.5 {
        delta / (2.0 - max - min)
    } else {
        delta / (max + min)
    };

    let h = match max {
        x if x == r => ((g - b) / delta) % 6.0,
        x if x == g => (b - r) / delta + 2.0,
        _ => (r - g) / delta + 4.0,
    };

    let h = (h * 60.0 + 360.0) % 360.0;

    (
        h.round() as u16,
        (s * 100.0).round() as u8,
        (l * 100.0).round() as u8,
    )
}

/// Converts HSV to RGB
/// H: 0-360, S: 0-100, V: 0-100
fn hsv_to_rgb(h: u16, s: u8, v: u8) -> (u8, u8, u8) {
    let h = h % 360;
    let s = s as f64 / 100.0;
    let v = v as f64 / 100.0;

    let c = v * s;
    let x = c * (1.0 - ((h as f64 / 60.0) % 2.0 - 1.0).abs());
    let m = v - c;

    let (r, g, b) = match h {
        0..=59 => (c, x, 0.0),
        60..=119 => (x, c, 0.0),
        120..=179 => (0.0, c, x),
        180..=239 => (0.0, x, c),
        240..=299 => (x, 0.0, c),
        _ => (c, 0.0, x),
    };

    (
        ((r + m) * 255.0).round() as u8,
        ((g + m) * 255.0).round() as u8,
        ((b + m) * 255.0).round() as u8,
    )
}

/// Converts RGB to HSV
/// Returns (H, S, V) where H: 0-360, S: 0-100, V: 0-100
fn rgb_to_hsv(r: u8, g: u8, b: u8) -> (u16, u8, u8) {
    let r = r as f64 / 255.0;
    let g = g as f64 / 255.0;
    let b = b as f64 / 255.0;

    let max = r.max(g).max(b);
    let min = r.min(g).min(b);
    let delta = max - min;

    let s = if max == 0.0 { 0.0 } else { delta / max };

    let h = if delta == 0.0 {
        0.0
    } else {
        match max {
            x if x == r => ((g - b) / delta) % 6.0,
            x if x == g => (b - r) / delta + 2.0,
            _ => (r - g) / delta + 4.0,
        }
    };

    let h = (h * 60.0 + 360.0) % 360.0;

    (
        h.round() as u16,
        (s * 100.0).round() as u8,
        (max * 100.0).round() as u8,
    )
}

/// Converts CMYK to RGB
/// C, M, Y, K: 0-100
fn cmyk_to_rgb(c: u8, m: u8, y: u8, k: u8) -> (u8, u8, u8) {
    let c = c as f64 / 100.0;
    let m = m as f64 / 100.0;
    let y = y as f64 / 100.0;
    let k = k as f64 / 100.0;

    let r = 255.0 * (1.0 - c) * (1.0 - k);
    let g = 255.0 * (1.0 - m) * (1.0 - k);
    let b = 255.0 * (1.0 - y) * (1.0 - k);

    (
        r.round() as u8,
        g.round() as u8,
        b.round() as u8,
    )
}

/// Converts RGB to CMYK
/// Returns (C, M, Y, K) where each value is 0-100
fn rgb_to_cmyk(r: u8, g: u8, b: u8) -> (u8, u8, u8, u8) {
    let r = r as f64 / 255.0;
    let g = g as f64 / 255.0;
    let b = b as f64 / 255.0;

    let k = 1.0 - r.max(g).max(b);

    if k == 1.0 {
        return (0, 0, 0, 100);
    }

    let c = (1.0 - r - k) / (1.0 - k);
    let m = (1.0 - g - k) / (1.0 - k);
    let y = (1.0 - b - k) / (1.0 - k);

    (
        (c * 100.0).round() as u8,
        (m * 100.0).round() as u8,
        (y * 100.0).round() as u8,
        (k * 100.0).round() as u8,
    )
}

/// Gets the CSS color name for RGB values
fn color_name(r: u8, g: u8, b: u8) -> Option<&'static str> {
    // Common named colors
    match (r, g, b) {
        (0, 0, 0) => Some("black"),
        (255, 255, 255) => Some("white"),
        (255, 0, 0) => Some("red"),
        (0, 255, 0) => Some("lime"),
        (0, 0, 255) => Some("blue"),
        (255, 255, 0) => Some("yellow"),
        (0, 255, 255) => Some("cyan"),
        (255, 0, 255) => Some("magenta"),
        (128, 128, 128) => Some("gray"),
        (128, 0, 0) => Some("maroon"),
        (0, 128, 0) => Some("green"),
        (0, 0, 128) => Some("navy"),
        (128, 128, 0) => Some("olive"),
        (128, 0, 128) => Some("purple"),
        (0, 128, 128) => Some("teal"),
        (255, 165, 0) => Some("orange"),
        (255, 192, 203) => Some("pink"),
        (255, 215, 0) => Some("gold"),
        (165, 42, 42) => Some("brown"),
        (192, 192, 192) => Some("silver"),
        (240, 128, 128) => Some("lightcoral"),
        (173, 216, 230) => Some("lightblue"),
        (144, 238, 144) => Some("lightgreen"),
        (255, 218, 185) => Some("peachpuff"),
        (255, 182, 193) => Some("lightpink"),
        (221, 160, 221) => Some("plum"),
        (176, 224, 230) => Some("powderblue"),
        _ => None,
    }
}

// ==================== Tests ====================

#[cfg(test)]
mod tests {
    use super::*;

    mod rgb_construction {
        use super::*;

        #[test]
        fn test_rgb_basic() {
            let color = Color::rgb(255, 128, 64);
            assert_eq!(color.as_rgb(), (255, 128, 64));
        }

        #[test]
        fn test_rgba_basic() {
            let color = Color::rgba(255, 128, 64, 128);
            assert_eq!(color.as_rgba(), (255, 128, 64, 128));
        }

        #[test]
        fn test_rgb_zero() {
            let color = Color::rgb(0, 0, 0);
            assert_eq!(color.as_rgb(), (0, 0, 0));
        }

        #[test]
        fn test_rgb_max() {
            let color = Color::rgb(255, 255, 255);
            assert_eq!(color.as_rgb(), (255, 255, 255));
        }

        #[test]
        fn test_with_alpha() {
            let color = Color::rgb(255, 0, 0).with_alpha(128);
            assert_eq!(color.alpha(), 128);
        }
    }

    mod hex_parsing {
        use super::*;

        #[test]
        fn test_hex_3_digit() {
            let color = Color::from_hex("#F80").unwrap();
            assert_eq!(color.as_rgb(), (255, 136, 0));
        }

        #[test]
        fn test_hex_6_digit() {
            let color = Color::from_hex("#FF8000").unwrap();
            assert_eq!(color.as_rgb(), (255, 128, 0));
        }

        #[test]
        fn test_hex_6_digit_lowercase() {
            let color = Color::from_hex("#ff8000").unwrap();
            assert_eq!(color.as_rgb(), (255, 128, 0));
        }

        #[test]
        fn test_hex_8_digit() {
            let color = Color::from_hex("#FF800080").unwrap();
            assert_eq!(color.as_rgba(), (255, 128, 0, 128));
        }

        #[test]
        fn test_hex_without_hash() {
            let color = Color::from_hex("FF8000").unwrap();
            assert_eq!(color.as_rgb(), (255, 128, 0));
        }

        #[test]
        fn test_hex_invalid_length() {
            assert!(matches!(Color::from_hex("#FF"), Err(ColorError::InvalidHexFormat)));
        }

        #[test]
        fn test_hex_invalid_chars() {
            assert!(matches!(Color::from_hex("#GGGGGG"), Err(ColorError::InvalidHexFormat)));
        }
    }

    mod hex_output {
        use super::*;

        #[test]
        fn test_to_hex() {
            let color = Color::rgb(255, 128, 64);
            assert_eq!(color.to_hex(), "#FF8040");
        }

        #[test]
        fn test_to_hex_rgb() {
            let color = Color::rgba(255, 128, 64, 128);
            assert_eq!(color.to_hex_rgb(), "#FF8040");
        }

        #[test]
        fn test_to_hex_with_alpha() {
            let color = Color::rgba(255, 128, 64, 128);
            assert_eq!(color.to_hex(), "#FF804080");
        }

        #[test]
        fn test_to_hex_black() {
            let color = Color::rgb(0, 0, 0);
            assert_eq!(color.to_hex(), "#000000");
        }

        #[test]
        fn test_to_hex_white() {
            let color = Color::rgb(255, 255, 255);
            assert_eq!(color.to_hex(), "#FFFFFF");
        }
    }

    mod hsl_conversion {
        use super::*;

        #[test]
        fn test_hsl_red() {
            let color = Color::hsl(0, 100, 50);
            assert_eq!(color.as_rgb(), (255, 0, 0));
        }

        #[test]
        fn test_hsl_green() {
            let color = Color::hsl(120, 100, 50);
            assert_eq!(color.as_rgb(), (0, 255, 0));
        }

        #[test]
        fn test_hsl_blue() {
            let color = Color::hsl(240, 100, 50);
            assert_eq!(color.as_rgb(), (0, 0, 255));
        }

        #[test]
        fn test_hsl_gray() {
            let color = Color::hsl(0, 0, 50);
            let (r, g, b) = color.as_rgb();
            assert_eq!(r, g);
            assert_eq!(g, b);
        }

        #[test]
        fn test_rgb_to_hsl_red() {
            let (h, s, l) = Color::rgb(255, 0, 0).to_hsl();
            assert_eq!(h, 0);
            assert_eq!(s, 100);
            assert_eq!(l, 50);
        }

        #[test]
        fn test_rgb_to_hsl_white() {
            let (h, s, l) = Color::rgb(255, 255, 255).to_hsl();
            assert_eq!(l, 100);
            assert_eq!(s, 0);
        }

        #[test]
        fn test_rgb_to_hsl_black() {
            let (h, s, l) = Color::rgb(0, 0, 0).to_hsl();
            assert_eq!(l, 0);
        }
    }

    mod hsv_conversion {
        use super::*;

        #[test]
        fn test_hsv_red() {
            let color = Color::hsv(0, 100, 100);
            assert_eq!(color.as_rgb(), (255, 0, 0));
        }

        #[test]
        fn test_hsv_green() {
            let color = Color::hsv(120, 100, 100);
            assert_eq!(color.as_rgb(), (0, 255, 0));
        }

        #[test]
        fn test_hsv_blue() {
            let color = Color::hsv(240, 100, 100);
            assert_eq!(color.as_rgb(), (0, 0, 255));
        }

        #[test]
        fn test_rgb_to_hsv_red() {
            let (h, s, v) = Color::rgb(255, 0, 0).to_hsv();
            assert_eq!(h, 0);
            assert_eq!(s, 100);
            assert_eq!(v, 100);
        }

        #[test]
        fn test_rgb_to_hsv_white() {
            let (h, s, v) = Color::rgb(255, 255, 255).to_hsv();
            assert_eq!(v, 100);
            assert_eq!(s, 0);
        }
    }

    mod cmyk_conversion {
        use super::*;

        #[test]
        fn test_cmyk_black() {
            let color = Color::cmyk(0, 0, 0, 100);
            assert_eq!(color.as_rgb(), (0, 0, 0));
        }

        #[test]
        fn test_cmyk_white() {
            let color = Color::cmyk(0, 0, 0, 0);
            assert_eq!(color.as_rgb(), (255, 255, 255));
        }

        #[test]
        fn test_cmyk_red() {
            let color = Color::cmyk(0, 100, 100, 0);
            assert_eq!(color.as_rgb(), (255, 0, 0));
        }

        #[test]
        fn test_rgb_to_cmyk_black() {
            let (c, m, y, k) = Color::rgb(0, 0, 0).to_cmyk();
            assert_eq!(k, 100);
        }

        #[test]
        fn test_rgb_to_cmyk_white() {
            let (c, m, y, k) = Color::rgb(255, 255, 255).to_cmyk();
            assert_eq!(k, 0);
        }
    }

    mod luminance {
        use super::*;

        #[test]
        fn test_luminance_black() {
            let luminance = Color::rgb(0, 0, 0).luminance();
            assert!(luminance < 0.01);
        }

        #[test]
        fn test_luminance_white() {
            let luminance = Color::rgb(255, 255, 255).luminance();
            assert!(luminance > 0.99);
        }

        #[test]
        fn test_is_light() {
            assert!(Color::rgb(255, 255, 255).is_light());
            assert!(!Color::rgb(0, 0, 0).is_light());
        }

        #[test]
        fn test_is_dark() {
            assert!(Color::rgb(0, 0, 0).is_dark());
            assert!(!Color::rgb(255, 255, 255).is_dark());
        }
    }

    mod contrast {
        use super::*;

        #[test]
        fn test_contrast_black_white() {
            let black = Color::rgb(0, 0, 0);
            let white = Color::rgb(255, 255, 255);
            let ratio = black.contrast_ratio(&white);
            assert!(ratio >= 20.0);
        }

        #[test]
        fn test_contrast_same_color() {
            let color = Color::rgb(128, 128, 128);
            let ratio = color.contrast_ratio(&color);
            assert!((ratio - 1.0).abs() < 0.01);
        }

        #[test]
        fn test_contrast_level_aaa() {
            let black = Color::rgb(0, 0, 0);
            let white = Color::rgb(255, 255, 255);
            assert_eq!(black.contrast_level(&white), ContrastLevel::AAA);
        }

        #[test]
        fn test_contrast_level_fail() {
            let color1 = Color::rgb(100, 100, 100);
            let color2 = Color::rgb(110, 110, 110);
            assert_eq!(color1.contrast_level(&color2), ContrastLevel::Fail);
        }
    }

    mod color_manipulation {
        use super::*;

        #[test]
        fn test_complementary() {
            let color = Color::rgb(255, 0, 0);
            let comp = color.complementary();
            let (h, _, _) = comp.to_hsl();
            assert_eq!(h, 180);
        }

        #[test]
        fn test_mix_equal() {
            let black = Color::rgb(0, 0, 0);
            let white = Color::rgb(255, 255, 255);
            let mixed = black.mix(&white, 0.5);
            assert_eq!(mixed.as_rgb(), (128, 128, 128));
        }

        #[test]
        fn test_lighten() {
            let color = Color::rgb(128, 128, 128);
            let lightened = color.lighten(25);
            let (_, _, l) = lightened.to_hsl();
            assert!(l > 50);
        }

        #[test]
        fn test_darken() {
            let color = Color::rgb(128, 128, 128);
            let darkened = color.darken(25);
            let (_, _, l) = darkened.to_hsl();
            assert!(l < 50);
        }

        #[test]
        fn test_saturate() {
            let color = Color::hsl(180, 50, 50);
            let saturated = color.saturate(30);
            let (_, s, _) = saturated.to_hsl();
            assert_eq!(s, 80);
        }

        #[test]
        fn test_desaturate() {
            let color = Color::hsl(180, 50, 50);
            let desaturated = color.desaturate(30);
            let (_, s, _) = desaturated.to_hsl();
            assert_eq!(s, 20);
        }

        #[test]
        fn test_grayscale() {
            let color = Color::rgb(100, 150, 200);
            let gray = color.grayscale();
            let (r, g, b) = gray.as_rgb();
            assert_eq!(r, g);
            assert_eq!(g, b);
        }

        #[test]
        fn test_invert() {
            let color = Color::rgb(100, 150, 200);
            let inverted = color.invert();
            assert_eq!(inverted.as_rgb(), (155, 105, 55));
        }
    }

    mod color_schemes {
        use super::*;

        #[test]
        fn test_triadic() {
            let color = Color::rgb(255, 0, 0);
            let triadic = color.triadic();
            assert_eq!(triadic.len(), 3);
            
            let h1 = triadic[0].to_hsl().0;
            let h2 = triadic[1].to_hsl().0;
            let h3 = triadic[2].to_hsl().0;
            
            assert!((h2 as i16 - h1 as i16).abs() == 120 || (h2 as i16 - h1 as i16).abs() == 240);
            assert!((h3 as i16 - h2 as i16).abs() == 120 || (h3 as i16 - h2 as i16).abs() == 240);
        }

        #[test]
        fn test_analogous() {
            let color = Color::rgb(255, 0, 0);
            let analogous = color.analogous();
            assert_eq!(analogous.len(), 3);
        }

        #[test]
        fn test_split_complementary() {
            let color = Color::rgb(255, 0, 0);
            let split = color.split_complementary();
            assert_eq!(split.len(), 3);
        }
    }

    mod color_names {
        use super::*;

        #[test]
        fn test_named_black() {
            assert_eq!(Color::rgb(0, 0, 0).name(), Some("black"));
        }

        #[test]
        fn test_named_white() {
            assert_eq!(Color::rgb(255, 255, 255).name(), Some("white"));
        }

        #[test]
        fn test_named_red() {
            assert_eq!(Color::rgb(255, 0, 0).name(), Some("red"));
        }

        #[test]
        fn test_named_blue() {
            assert_eq!(Color::rgb(0, 0, 255).name(), Some("blue"));
        }

        #[test]
        fn test_unnamed_color() {
            assert_eq!(Color::rgb(123, 45, 67).name(), None);
        }
    }

    mod display_and_parse {
        use super::*;

        #[test]
        fn test_display() {
            let color = Color::rgb(255, 128, 64);
            assert_eq!(format!("{}", color), "rgb(255, 128, 64)");
        }

        #[test]
        fn test_from_str() {
            let color: Color = "#FF8040".parse().unwrap();
            assert_eq!(color.as_rgb(), (255, 128, 64));
        }
    }

    mod edge_cases {
        use super::*;

        #[test]
        fn test_overflow_protection() {
            let color = Color::hsl(720, 150, 150);
            // Should not panic, values are clamped/modulo'd
            let _ = color.as_rgb();
        }

        #[test]
        fn test_lighten_max() {
            let color = Color::rgb(200, 200, 200);
            let lightened = color.lighten(100);
            let (_, _, l) = lightened.to_hsl();
            assert_eq!(l, 100);
        }

        #[test]
        fn test_darken_min() {
            let color = Color::rgb(50, 50, 50);
            let darkened = color.darken(100);
            let (_, _, l) = darkened.to_hsl();
            assert_eq!(l, 0);
        }

        #[test]
        fn test_mix_extremes() {
            let color = Color::rgb(255, 0, 0);
            let other = Color::rgb(0, 0, 255);
            
            let result1 = color.mix(&other, 0.0);
            assert_eq!(result1.as_rgb(), color.as_rgb());
            
            let result2 = color.mix(&other, 1.0);
            assert_eq!(result2.as_rgb(), other.as_rgb());
        }
    }
}