//! # File Utilities Tests
//!
//! Comprehensive test suite for the file_utils module.

use std::fs;
use std::path::Path;
use std::io::Write;

mod mod_rs;
use mod_rs::{FileUtils, FileError, FileResult, FileInfo};

// Helper to create test directory
fn setup_test_env() -> std::path::PathBuf {
    let test_dir = std::env::temp_dir().join("file_utils_test");
    if test_dir.exists() {
        fs::remove_dir_all(&test_dir).unwrap_or_default();
    }
    fs::create_dir_all(&test_dir).unwrap();
    test_dir
}

// Helper to cleanup test directory
fn cleanup_test_env(test_dir: &Path) {
    if test_dir.exists() {
        fs::remove_dir_all(test_dir).unwrap_or_default();
    }
}

// ============================================================================
// File Reading Tests
// ============================================================================

#[test]
fn test_read_to_string_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_read.txt");
    
    // Create test file
    fs::write(&file_path, "Hello, World!").unwrap();
    
    // Test read
    let result = FileUtils::read_to_string(&file_path);
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), "Hello, World!");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_read_to_string_not_found() {
    let result = FileUtils::read_to_string("/nonexistent/path/file.txt");
    assert!(result.is_err());
    match result {
        Err(FileError::NotFound(_)) => (),
        _ => panic!("Expected NotFound error"),
    }
}

#[test]
fn test_read_to_string_directory() {
    let test_dir = setup_test_env();
    
    // Try to read directory as file
    let result = FileUtils::read_to_string(&test_dir);
    assert!(result.is_err());
    match result {
        Err(FileError::NotAFile(_)) => (),
        _ => panic!("Expected NotAFile error"),
    }
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_read_to_bytes_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_bytes.bin");
    
    // Create binary file
    fs::write(&file_path, &[0x00, 0x01, 0x02, 0xFF]).unwrap();
    
    // Test read
    let result = FileUtils::read_to_bytes(&file_path);
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), vec![0x00, 0x01, 0x02, 0xFF]);
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_read_lines_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_lines.txt");
    
    // Create multi-line file
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(b"Line 1\nLine 2\nLine 3\n").unwrap();
    
    // Test read lines
    let result = FileUtils::read_lines(&file_path);
    assert!(result.is_ok());
    let lines = result.unwrap();
    assert_eq!(lines.len(), 3);
    assert_eq!(lines[0], "Line 1");
    assert_eq!(lines[1], "Line 2");
    assert_eq!(lines[2], "Line 3");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_read_chunks_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_chunks.txt");
    
    // Create file larger than chunk size
    fs::write(&file_path, "This is a test file with some content for chunk reading.").unwrap();
    
    // Test chunk reading
    let mut total_bytes = 0;
    let result = FileUtils::read_chunks(&file_path, 10, |chunk| {
        total_bytes += chunk.len();
    });
    
    assert!(result.is_ok());
    assert_eq!(total_bytes, 54); // Length of test content
    
    cleanup_test_env(&test_dir);
}

// ============================================================================
// File Writing Tests
// ============================================================================

#[test]
fn test_write_string_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_write.txt");
    
    // Write string
    let result = FileUtils::write_string(&file_path, "Test content");
    assert!(result.is_ok());
    
    // Verify content
    let content = fs::read_to_string(&file_path).unwrap();
    assert_eq!(content, "Test content");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_write_bytes_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_write_bytes.bin");
    
    // Write bytes
    let result = FileUtils::write_bytes(&file_path, &[0xDE, 0xAD, 0xBE, 0xEF]);
    assert!(result.is_ok());
    
    // Verify content
    let content = fs::read(&file_path).unwrap();
    assert_eq!(content, vec![0xDE, 0xAD, 0xBE, 0xEF]);
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_append_string_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_append.txt");
    
    // Create initial file
    fs::write(&file_path, "Initial ").unwrap();
    
    // Append to file
    let result = FileUtils::append_string(&file_path, "content");
    assert!(result.is_ok());
    
    // Verify content
    let content = fs::read_to_string(&file_path).unwrap();
    assert_eq!(content, "Initial content");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_append_string_creates_file() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_append_new.txt");
    
    // Append to nonexistent file (should create)
    let result = FileUtils::append_string(&file_path, "New content");
    assert!(result.is_ok());
    
    // Verify content
    let content = fs::read_to_string(&file_path).unwrap();
    assert_eq!(content, "New content");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_append_bytes_success() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_append_bytes.bin");
    
    // Create initial file
    fs::write(&file_path, &[0x00]).unwrap();
    
    // Append bytes
    let result = FileUtils::append_bytes(&file_path, &[0x01, 0x02]);
    assert!(result.is_ok());
    
    // Verify content
    let content = fs::read(&file_path).unwrap();
    assert_eq!(content, vec![0x00, 0x01, 0x02]);
    
    cleanup_test_env(&test_dir);
}

// ============================================================================
// File Existence Tests
// ============================================================================

#[test]
fn test_exists_file() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_exists.txt");
    
    // File doesn't exist initially
    assert!(!FileUtils::exists(&file_path));
    
    // Create file
    fs::write(&file_path, "test").unwrap();
    
    // Now it exists
    assert!(FileUtils::exists(&file_path));
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_exists_directory() {
    let test_dir = setup_test_env();
    
    assert!(FileUtils::exists(&test_dir));
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_is_file() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_is_file.txt");
    
    // Create file
    fs::write(&file_path, "test").unwrap();
    
    assert!(FileUtils::is_file(&file_path));
    assert!(!FileUtils::is_file(&test_dir)); // Directory is not a file
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_is_dir() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_is_dir.txt");
    
    // Create file
    fs::write(&file_path, "test").unwrap();
    
    assert!(FileUtils::is_dir(&test_dir));
    assert!(!FileUtils::is_dir(&file_path)); // File is not a directory
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_is_symlink() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("test_symlink.txt");
    let link_path = test_dir.join("test_link");
    
    // Create file and symlink
    fs::write(&file_path, "test").unwrap();
    
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(&file_path, &link_path).unwrap();
        assert!(FileUtils::is_symlink(&link_path));
        assert!(!FileUtils::is_symlink(&file_path));
    }
    
    cleanup_test_env(&test_dir);
}

// ============================================================================
// Error Type Tests
// ============================================================================

#[test]
fn test_file_error_display() {
    let err = FileError::NotFound("test.txt");
    assert_eq!(err.to_string(), "File not found: test.txt");
    
    let err = FileError::NotAFile("dir/");
    assert_eq!(err.to_string(), "Not a file: dir/");
    
    let err = FileError::IoError("read error");
    assert_eq!(err.to_string(), "IO Error: read error");
}

#[test]
fn test_file_error_clone() {
    let err = FileError::NotFound("test.txt");
    let cloned = err.clone();
    assert_eq!(err, cloned);
}

#[test]
fn test_file_error_partial_eq() {
    let err1 = FileError::NotFound("test.txt");
    let err2 = FileError::NotFound("test.txt");
    let err3 = FileError::NotAFile("test.txt");
    
    assert_eq!(err1, err2);
    assert_ne!(err1, err3);
}

// ============================================================================
// Edge Cases
// ============================================================================

#[test]
fn test_empty_file() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("empty.txt");
    
    // Create empty file
    fs::write(&file_path, "").unwrap();
    
    // Read empty file
    let result = FileUtils::read_to_string(&file_path);
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), "");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_unicode_content() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("unicode.txt");
    
    // Write unicode content
    let unicode_content = "你好世界 🎉 Hello World";
    let result = FileUtils::write_string(&file_path, unicode_content);
    assert!(result.is_ok());
    
    // Read back
    let content = FileUtils::read_to_string(&file_path).unwrap();
    assert_eq!(content, unicode_content);
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_large_content() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("large.txt");
    
    // Create large content (1MB)
    let large_content = "A".repeat(1024 * 1024);
    
    // Write
    let result = FileUtils::write_string(&file_path, &large_content);
    assert!(result.is_ok());
    
    // Read and verify
    let content = FileUtils::read_to_string(&file_path).unwrap();
    assert_eq!(content.len(), 1024 * 1024);
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_overwrite_file() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("overwrite.txt");
    
    // Create initial content
    FileUtils::write_string(&file_path, "Initial").unwrap();
    
    // Overwrite
    FileUtils::write_string(&file_path, "New").unwrap();
    
    // Verify overwritten
    let content = FileUtils::read_to_string(&file_path).unwrap();
    assert_eq!(content, "New");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_multiple_append() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("multi_append.txt");
    
    // Multiple appends
    FileUtils::append_string(&file_path, "Line 1\n").unwrap();
    FileUtils::append_string(&file_path, "Line 2\n").unwrap();
    FileUtils::append_string(&file_path, "Line 3\n").unwrap();
    
    let content = FileUtils::read_to_string(&file_path).unwrap();
    assert_eq!(content, "Line 1\nLine 2\nLine 3\n");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_path_with_spaces() {
    let test_dir = setup_test_env();
    let file_path = test_dir.join("file with spaces.txt");
    
    FileUtils::write_string(&file_path, "content").unwrap();
    let content = FileUtils::read_to_string(&file_path).unwrap();
    assert_eq!(content, "content");
    
    cleanup_test_env(&test_dir);
}

#[test]
fn test_nested_directory_path() {
    let test_dir = setup_test_env();
    let nested_dir = test_dir.join("nested").join("deep").join("path");
    fs::create_dir_all(&nested_dir).unwrap();
    
    let file_path = nested_dir.join("deep_file.txt");
    FileUtils::write_string(&file_path, "deep content").unwrap();
    
    let content = FileUtils::read_to_string(&file_path).unwrap();
    assert_eq!(content, "deep content");
    
    cleanup_test_env(&test_dir);
}

// ============================================================================
// Test Summary
// ============================================================================

#[test]
fn test_summary() {
    println!("\n======================================================================");
    println!("FILE_UTILS TEST SUMMARY");
    println!("======================================================================");
    println!("Tests cover:");
    println!("  - File reading (read_to_string, read_to_bytes, read_lines, read_chunks)");
    println!("  - File writing (write_string, write_bytes, append_string, append_bytes)");
    println!("  - File existence (exists, is_file, is_dir, is_symlink)");
    println!("  - Error handling (NotFound, NotAFile, IoError)");
    println!("  - Edge cases (empty file, unicode, large content, overwrite)");
    println!("======================================================================");
}