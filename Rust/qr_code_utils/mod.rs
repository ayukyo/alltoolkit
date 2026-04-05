//! # QR Code Utilities
//!
//! A zero-dependency QR Code generator for Rust.
//!
//! This module provides functionality to generate QR codes with various
//! error correction levels and output formats including text, SVG, and
//! bitmap representations.
//!
//! ## Features
//!
//! - Zero dependencies, uses only Rust standard library
//! - Supports QR code versions 1-10 (expandable)
//! - Four error correction levels: L, M, Q, H
//! - Multiple output formats: text, SVG
//! - Alphanumeric, numeric, and byte encoding modes
//! - Automatic mode detection
//!
//! ## Example
//!
//! ```rust
//! use qr_code_utils::{QrCode, ErrorCorrectionLevel};
//!
//! // Create a QR code
//! let qr = QrCode::new("Hello, World!", ErrorCorrectionLevel::M).unwrap();
//!
//! // Output as text
//! println!("{}", qr.to_text());
//!
//! // Output as SVG
//! println!("{}", qr.to_svg(4));
//! ```

/// Error correction level for QR codes
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ErrorCorrectionLevel {
    /// Low - ~7% correction
    L,
    /// Medium - ~15% correction
    M,
    /// Quartile - ~25% correction
    Q,
    /// High - ~30% correction
    H,
}

impl ErrorCorrectionLevel {
    /// Get the error correction value (0-3)
    fn value(&self) -> u8 {
        match self {
            ErrorCorrectionLevel::L => 0,
            ErrorCorrectionLevel::M => 1,
            ErrorCorrectionLevel::Q => 2,
            ErrorCorrectionLevel::H => 3,
        }
    }
}

/// QR Code encoding mode
#[derive(Debug, Clone, Copy, PartialEq)]
enum EncodingMode {
    Numeric,
    Alphanumeric,
    Byte,
}

/// QR Code structure
#[derive(Debug, Clone)]
pub struct QrCode {
    /// The version of the QR code
    version: u8,
    /// Error correction level
    error_level: ErrorCorrectionLevel,
    /// The modules (true = dark, false = light)
    modules: Vec<Vec<bool>>,
    /// Size of the QR code
    size: usize,
}

/// QR Code error types
#[derive(Debug, Clone, PartialEq)]
pub enum QrCodeError {
    /// Data is too long for the QR code capacity
    DataTooLong,
    /// Invalid version number
    InvalidVersion,
    /// Invalid error correction level
    InvalidErrorLevel,
    /// Invalid data
    InvalidData,
}

impl std::fmt::Display for QrCodeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            QrCodeError::DataTooLong => write!(f, "Data too long for QR code capacity"),
            QrCodeError::InvalidVersion => write!(f, "Invalid QR code version"),
            QrCodeError::InvalidErrorLevel => write!(f, "Invalid error correction level"),
            QrCodeError::InvalidData => write!(f, "Invalid data"),
        }
    }
}

impl std::error::Error for QrCodeError {}

/// Alphanumeric character set for QR codes
const ALPHANUMERIC_CHARS: &str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:";

/// Capacity table for versions 1-10
/// Format: [version-1][error_level] = (numeric, alphanumeric, byte)
const CAPACITY_TABLE: [[[usize; 3]; 4]; 10] = [
    // Version 1
    [[41, 25, 17], [34, 20, 14], [27, 16, 11], [17, 10, 7]],
    // Version 2
    [[77, 47, 32], [63, 38, 26], [48, 29, 20], [34, 20, 14]],
    // Version 3
    [[127, 77, 53], [101, 61, 42], [77, 47, 32], [58, 35, 24]],
    // Version 4
    [[187, 114, 78], [149, 90, 62], [111, 67, 46], [82, 50, 34]],
    // Version 5
    [[255, 154, 106], [202, 122, 84], [144, 87, 60], [106, 64, 44]],
    // Version 6
    [[322, 195, 134], [255, 154, 106], [178, 108, 74], [139, 84, 58]],
    // Version 7
    [[370, 224, 154], [293, 178, 122], [207, 125, 86], [154, 93, 64]],
    // Version 8
    [[461, 279, 192], [365, 221, 152], [259, 157, 108], [202, 122, 84]],
    // Version 9
    [[552, 335, 230], [432, 262, 180], [312, 189, 130], [235, 143, 98]],
    // Version 10
    [[652, 395, 271], [513, 311, 213], [364, 221, 151], [288, 174, 119]],
];

impl QrCode {
    /// Create a new QR code from string data
    ///
    /// # Arguments
    ///
    /// * `data` - The data to encode
    /// * `error_level` - Error correction level
    ///
    /// # Returns
    ///
    /// Returns `Ok(QrCode)` on success, or `Err(QrCodeError)` on failure
    ///
    /// # Example
    ///
    /// ```rust
    /// use qr_code_utils::{QrCode, ErrorCorrectionLevel};
    ///
    /// let qr = QrCode::new("Hello", ErrorCorrectionLevel::M).unwrap();
    /// ```
    pub fn new(data: &str, error_level: ErrorCorrectionLevel) -> Result<Self, QrCodeError> {
        let mode = Self::detect_mode(data);
        let version = Self::find_version(data.len(), mode, error_level)?;
        Self::with_version(data, version, error_level)
    }

    /// Create a QR code with specific version
    ///
    /// # Arguments
    ///
    /// * `data` - The data to encode
    /// * `version` - QR code version (1-10)
    /// * `error_level` - Error correction level
    pub fn with_version(data: &str, version: u8, error_level: ErrorCorrectionLevel) -> Result<Self, QrCodeError> {
        if version < 1 || version > 10 {
            return Err(QrCodeError::InvalidVersion);
        }

        let size = version as usize * 4 + 17;
        let mut modules = vec![vec![false; size]; size];

        // Create the QR code structure
        let mut qr = QrCode {
            version,
            error_level,
            modules,
            size,
        };

        // Add finder patterns (the three large squares in corners)
        qr.add_finder_patterns();

        // Add separators (white borders around finder patterns)
        qr.add_separators();

        // Add timing patterns (alternating line between finder patterns)
        qr.add_timing_patterns();

        // Add dark module (always present at specific location)
        qr.add_dark_module();

        // Add format information
        qr.add_format_info();

        // Encode and place data
        let encoded = qr.encode_data(data)?;
        qr.place_data(&encoded);

        // Apply mask pattern
        qr.apply_mask();

        Ok(qr)
    }

    /// Detect the best encoding mode for data
    fn detect_mode(data: &str) -> EncodingMode {
        if data.chars().all(|c| c.is_ascii_digit()) {
            EncodingMode::Numeric
        } else if data.chars().all(|c| ALPHANUMERIC_CHARS.contains(c)) {
            EncodingMode::Alphanumeric
        } else {
            EncodingMode::Byte
        }
    }

    /// Find the minimum version needed for the data
    fn find_version(len: usize, mode: EncodingMode, error_level: ErrorCorrectionLevel) -> Result<u8, QrCodeError> {
        let mode_idx = match mode {
            EncodingMode::Numeric => 0,
            EncodingMode::Alphanumeric => 1,
            EncodingMode::Byte => 2,
        };
        let ec_idx = error_level.value() as usize;

        for version in 1..=10 {
            let capacity = CAPACITY_TABLE[version - 1][ec_idx][mode_idx];
            if len <= capacity {
                return Ok(version as u8);
            }
        }

        Err(QrCodeError::DataTooLong)
    }

    /// Get the size of the QR code
    pub fn size(&self) -> usize {
        self.size
    }

    /// Get the version of the QR code
    pub fn version(&self) -> u8 {
        self.version
    }

    /// Get the error correction level
    pub fn error_level(&self) -> ErrorCorrectionLevel {
        self.error_level
    }

    /// Get a module at specific coordinates
    pub fn get_module(&self, row: usize, col: usize) -> Option<bool> {
        if row < self.size && col < self.size {
            Some(self.modules[row][col])
        } else {
            None
        }
    }

    /// Add finder patterns (the three large squares in corners)
    fn add_finder_patterns(&mut self) {
        let positions = [(0, 0), (0, self.size - 7), (self