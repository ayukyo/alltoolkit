//! # QR Code Utilities Tests
//!
//! Comprehensive test suite for the qr_code_utils module.

mod mod_rs;
use mod_rs::{QrCode, ErrorCorrectionLevel, QrCodeError, EncodingMode};

// ============================================================================
// QR Code Creation Tests
// ============================================================================

#[test]
fn test_qr_code_new_simple() {
    let result = QrCode::new("Hello", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert!(qr.size() > 0);
    assert!(qr.version() >= 1 && qr.version() <= 10);
}

#[test]
fn test_qr_code_new_numeric() {
    // Numeric data should use Numeric mode
    let result = QrCode::new("1234567890", ErrorCorrectionLevel::L);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.version(), 1); // Numeric has highest capacity
}

#[test]
fn test_qr_code_new_alphanumeric() {
    // Alphanumeric data (no lowercase)
    let result = QrCode::new("ABC123", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert!(qr.version() >= 1);
}

#[test]
fn test_qr_code_new_byte_mode() {
    // Byte mode for lowercase and special characters
    let result = QrCode::new("Hello, World!", ErrorCorrectionLevel::H);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert!(qr.size() > 0);
}

#[test]
fn test_qr_code_empty_string() {
    let result = QrCode::new("", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert!(qr.size() > 0);
}

#[test]
fn test_qr_code_data_to_long() {
    // Create data that exceeds maximum capacity (Version 10, Level H, Byte mode = 119 chars)
    let long_data = "A".repeat(200);
    let result = QrCode::new(&long_data, ErrorCorrectionLevel::H);
    
    assert!(result.is_err());
    match result {
        Err(QrCodeError::DataTooLong) => (),
        _ => panic!("Expected DataTooLong error"),
    }
}

// ============================================================================
// Version Tests
// ============================================================================

#[test]
fn test_qr_code_with_version_1() {
    let result = QrCode::with_version("Test", 1, ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.version(), 1);
    assert_eq!(qr.size(), 21); // Version 1: 4*1 + 17 = 21
}

#[test]
fn test_qr_code_with_version_5() {
    let result = QrCode::with_version("Test", 5, ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.version(), 5);
    assert_eq!(qr.size(), 37); // Version 5: 4*5 + 17 = 37
}

#[test]
fn test_qr_code_with_version_10() {
    let result = QrCode::with_version("Test", 10, ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.version(), 10);
    assert_eq!(qr.size(), 57); // Version 10: 4*10 + 17 = 57
}

#[test]
fn test_qr_code_invalid_version_zero() {
    let result = QrCode::with_version("Test", 0, ErrorCorrectionLevel::M);
    assert!(result.is_err());
    match result {
        Err(QrCodeError::InvalidVersion) => (),
        _ => panic!("Expected InvalidVersion error"),
    }
}

#[test]
fn test_qr_code_invalid_version_too_high() {
    let result = QrCode::with_version("Test", 11, ErrorCorrectionLevel::M);
    assert!(result.is_err());
    match result {
        Err(QrCodeError::InvalidVersion) => (),
        _ => panic!("Expected InvalidVersion error"),
    }
}

// ============================================================================
// Error Correction Level Tests
// ============================================================================

#[test]
fn test_error_correction_level_l() {
    let result = QrCode::new("Test", ErrorCorrectionLevel::L);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.error_level(), ErrorCorrectionLevel::L);
}

#[test]
fn test_error_correction_level_m() {
    let result = QrCode::new("Test", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.error_level(), ErrorCorrectionLevel::M);
}

#[test]
fn test_error_correction_level_q() {
    let result = QrCode::new("Test", ErrorCorrectionLevel::Q);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.error_level(), ErrorCorrectionLevel::Q);
}

#[test]
fn test_error_correction_level_h() {
    let result = QrCode::new("Test", ErrorCorrectionLevel::H);
    assert!(result.is_ok());
    
    let qr = result.unwrap();
    assert_eq!(qr.error_level(), ErrorCorrectionLevel::H);
}

#[test]
fn test_error_correction_level_value() {
    assert_eq!(ErrorCorrectionLevel::L.value(), 0);
    assert_eq!(ErrorCorrectionLevel::M.value(), 1);
    assert_eq!(ErrorCorrectionLevel::Q.value(), 2);
    assert_eq!(ErrorCorrectionLevel::H.value(), 3);
}

// ============================================================================
// Module Access Tests
// ============================================================================

#[test]
fn test_get_module_valid() {
    let qr = QrCode::new("Test", ErrorCorrectionLevel::M).unwrap();
    
    // Finder pattern corners should be dark (true)
    let module = qr.get_module(0, 0);
    assert!(module.is_some());
    assert!(module.unwrap()); // Top-left finder pattern center
}

#[test]
fn test_get_module_out_of_bounds() {
    let qr = QrCode::new("Test", ErrorCorrectionLevel::M).unwrap();
    
    // Out of bounds should return None
    let module = qr.get_module(1000, 0);
    assert!(module.is_none());
    
    let module = qr.get_module(0, 1000);
    assert!(module.is_none());
}

#[test]
fn test_get_module_negative_coords() {
    let qr = QrCode::new("Test", ErrorCorrectionLevel::M).unwrap();
    
    // Rust doesn't allow negative indices, but we can test edge
    let module = qr.get_module(qr.size(), 0);
    assert!(module.is_none());
}

// ============================================================================
// Size Tests
// ============================================================================

#[test]
fn test_size_calculation() {
    // Version formula: size = 4 * version + 17
    
    for version in 1..=10 {
        let qr = QrCode::with_version("Test", version, ErrorCorrectionLevel::M).unwrap();
        let expected_size = 4 * version + 17;
        assert_eq!(qr.size(), expected_size as usize);
    }
}

// ============================================================================
// Encoding Mode Tests (via behavior)
// ============================================================================

#[test]
fn test_numeric_mode_capacity() {
    // Numeric mode has highest capacity
    // Version 1, Level L can hold 41 numeric chars
    let data = "1".repeat(41);
    let result = QrCode::new(&data, ErrorCorrectionLevel::L);
    assert!(result.is_ok());
    assert_eq!(result.unwrap().version(), 1);
}

#[test]
fn test_numeric_mode_exceeds_capacity() {
    // Version 1, Level L: 41 numeric chars max
    let data = "1".repeat(42);
    let result = QrCode::new(&data, ErrorCorrectionLevel::L);
    assert!(result.is_ok());
    assert!(result.unwrap().version() > 1); // Should need version 2
}

#[test]
fn test_alphanumeric_mode_capacity() {
    // Version 1, Level L can hold 25 alphanumeric chars
    let data = "A".repeat(25);
    let result = QrCode::new(&data, ErrorCorrectionLevel::L);
    assert!(result.is_ok());
}

#[test]
fn test_byte_mode_capacity() {
    // Version 1, Level L can hold 17 bytes
    let data = "a".repeat(17); // lowercase forces byte mode
    let result = QrCode::new(&data, ErrorCorrectionLevel::L);
    assert!(result.is_ok());
}

// ============================================================================
// Error Type Tests
// ============================================================================

#[test]
fn test_qr_code_error_display() {
    let err = QrCodeError::DataTooLong;
    assert_eq!(err.to_string(), "Data too long for QR code capacity");
    
    let err = QrCodeError::InvalidVersion;
    assert_eq!(err.to_string(), "Invalid QR code version");
    
    let err = QrCodeError::InvalidData;
    assert_eq!(err.to_string(), "Invalid data");
}

#[test]
fn test_qr_code_error_clone() {
    let err = QrCodeError::DataTooLong;
    let cloned = err.clone();
    assert_eq!(err, cloned);
}

#[test]
fn test_qr_code_error_partial_eq() {
    let err1 = QrCodeError::DataTooLong;
    let err2 = QrCodeError::DataTooLong;
    let err3 = QrCodeError::InvalidVersion;
    
    assert_eq!(err1, err2);
    assert_ne!(err1, err3);
}

// ============================================================================
// Edge Cases
// ============================================================================

#[test]
fn test_single_character() {
    let result = QrCode::new("A", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
}

#[test]
fn test_unicode_characters() {
    // Unicode characters should work (byte mode)
    let result = QrCode::new("你好", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
}

#[test]
fn test_special_characters() {
    // All alphanumeric special chars
    let result = QrCode::new(" $%*+-./:", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
}

#[test]
fn test_url_encoding() {
    let result = QrCode::new("https://example.com/path?query=1", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
}

#[test]
fn test_whitespace() {
    let result = QrCode::new("Hello World", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
    
    let result = QrCode::new("  ", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
}

#[test]
fn test_newlines() {
    let result = QrCode::new("Line1\nLine2", ErrorCorrectionLevel::M);
    assert!(result.is_ok());
}

// ============================================================================
// Capacity Table Verification
// ============================================================================

#[test]
fn test_capacity_table_version1_level_l() {
    // Version 1, Level L: (numeric=41, alphanumeric=25, byte=17)
    assert!(QrCode::new(&"1".repeat(41), ErrorCorrectionLevel::L).is_ok());
    assert!(QrCode::new(&"A".repeat(25), ErrorCorrectionLevel::L).is_ok());
    assert!(QrCode::new(&"a".repeat(17), ErrorCorrectionLevel::L).is_ok());
}

#[test]
fn test_capacity_table_version1_level_m() {
    // Version 1, Level M: (numeric=34, alphanumeric=20, byte=14)
    assert!(QrCode::new(&"1".repeat(34), ErrorCorrectionLevel::M).is_ok());
    assert!(QrCode::new(&"A".repeat(20), ErrorCorrectionLevel::M).is_ok());
    assert!(QrCode::new(&"a".repeat(14), ErrorCorrectionLevel::M).is_ok());
}

#[test]
fn test_capacity_table_version1_level_h() {
    // Version 1, Level H: (numeric=17, alphanumeric=10, byte=7)
    assert!(QrCode::new(&"1".repeat(17), ErrorCorrectionLevel::H).is_ok());
    assert!(QrCode::new(&"A".repeat(10), ErrorCorrectionLevel::H).is_ok());
    assert!(QrCode::new(&"a".repeat(7), ErrorCorrectionLevel::H).is_ok());
}

// ============================================================================
// Finder Pattern Tests
// ============================================================================

#[test]
fn test_finder_patterns_present() {
    let qr = QrCode::new("Test", ErrorCorrectionLevel::M).unwrap();
    
    // Finder patterns should be at three corners
    // Top-left (0,0) - should have dark module
    assert!(qr.get_module(3, 3).unwrap()); // Center of finder pattern
    
    // Top-right
    let right_x = qr.size() - 4;
    assert!(qr.get_module(3, right_x).unwrap()); // Center of top-right finder
    
    // Bottom-left
    let bottom_y = qr.size() - 4;
    assert!(qr.get_module(bottom_y, 3).unwrap()); // Center of bottom-left finder
}

// ============================================================================
// Test Summary
// ============================================================================

#[test]
fn test_summary() {
    println!("\n======================================================================");
    println!("QR_CODE_UTILS TEST SUMMARY");
    println!("======================================================================");
    println!("Tests cover:");
    println!("  - QR Code creation (new, with_version)");
    println!("  - Error correction levels (L, M, Q, H)");
    println!("  - Version validation (1-10)");
    println!("  - Encoding modes (Numeric, Alphanumeric, Byte)");
    println!("  - Module access (get_module)");
    println!("  - Size calculations");
    println!("  - Error types (DataTooLong, InvalidVersion)");
    println!("  - Edge cases (unicode, special chars, whitespace)");
    println!("  - Capacity table verification");
    println!("  - Finder pattern verification");
    println!("======================================================================");
}