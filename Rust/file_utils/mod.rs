//! # File Utilities Module
//!
//! A comprehensive file utility module for Rust providing common file operations
//! with zero external dependencies.
//!
//! ## Features
//!
//! - File reading/writing with various options
//! - Directory operations (create, list, remove)
//! - File metadata and permissions
//! - Path manipulation utilities
//! - File searching and filtering
//! - Temporary file operations
//!
//! ## Example
//!
//! ```rust
//! use file_utils::FileUtils;
//!
//! // Read file content
//! let content = FileUtils::read_to_string("example.txt").unwrap();
//!
//! // Write file content
//! FileUtils::write_string("output.txt", "Hello, World!").unwrap();
//!
//! // Check if file exists
//! if FileUtils::exists("example.txt") {
//!     println!("File exists!");
//! }
//! ```

use std::fs::{self, File, OpenOptions};
use std::io::{self, BufRead, BufReader, Read, Write};
use std::path::{Path, PathBuf};
use std::time::SystemTime;

/// Error type for file operations
#[derive(Debug, Clone, PartialEq)]
pub enum FileError {
    IoError(String),
    NotFound(String),
    PermissionDenied(String),
    AlreadyExists(String),
    InvalidPath(String),
    NotAFile(String),
    NotADirectory(String),
}

impl std::fmt::Display for FileError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FileError::IoError(msg) => write!(f, "IO Error: {}", msg),
            FileError::NotFound(path) => write!(f, "File not found: {}", path),
            FileError::PermissionDenied(path) => write!(f, "Permission denied: {}", path),
            FileError::AlreadyExists(path) => write!(f, "File already exists: {}", path),
            FileError::InvalidPath(path) => write!(f, "Invalid path: {}", path),
            FileError::NotAFile(path) => write!(f, "Not a file: {}", path),
            FileError::NotADirectory(path) => write!(f, "Not a directory: {}", path),
        }
    }
}

impl std::error::Error for FileError {}

impl From<io::Error> for FileError {
    fn from(error: io::Error) -> Self {
        FileError::IoError(error.to_string())
    }
}

/// Result type alias for file operations
pub type FileResult<T> = Result<T, FileError>;

/// File information structure
#[derive(Debug, Clone)]
pub struct FileInfo {
    pub path: PathBuf,
    pub size: u64,
    pub is_file: bool,
    pub is_dir: bool,
    pub is_symlink: bool,
    pub created: Option<SystemTime>,
    pub modified: Option<SystemTime>,
    pub accessed: Option<SystemTime>,
    pub readonly: bool,
}

/// File utilities for common file operations
pub struct FileUtils;

impl FileUtils {
    // =========================================================================
    // File Reading Operations
    // =========================================================================

    /// Read entire file contents as a string
    pub fn read_to_string<P: AsRef<Path>>(path: P) -> FileResult<String> {
        let path = path.as_ref();
        if !path.exists() {
            return Err(FileError::NotFound(path.to_string_lossy().to_string()));
        }
        if !path.is_file() {
            return Err(FileError::NotAFile(path.to_string_lossy().to_string()));
        }
        match fs::read_to_string(path) {
            Ok(content) => Ok(content),
            Err(e) => Err(FileError::IoError(e.to_string())),
        }
    }

    /// Read entire file contents as bytes
    pub fn read_to_bytes<P: AsRef<Path>>(path: P) -> FileResult<Vec<u8>> {
        let path = path.as_ref();
        if !path.exists() {
            return Err(FileError::NotFound(path.to_string_lossy().to_string()));
        }
        if !path.is_file() {
            return Err(FileError::NotAFile(path.to_string_lossy().to_string()));
        }
        match fs::read(path) {
            Ok(bytes) => Ok(bytes),
            Err(e) => Err(FileError::IoError(e.to_string())),
        }
    }

    /// Read file line by line
    pub fn read_lines<P: AsRef<Path>>(path: P) -> FileResult<Vec<String>> {
        let path = path.as_ref();
        if !path.exists() {
            return Err(FileError::NotFound(path.to_string_lossy().to_string()));
        }
        let file = File::open(path).map_err(|e| FileError::IoError(e.to_string()))?;
        let reader = BufReader::new(file);
        let mut lines = Vec::new();
        for line in reader.lines() {
            match line {
                Ok(l) => lines.push(l),
                Err(e) => return Err(FileError::IoError(e.to_string())),
            }
        }
        Ok(lines)
    }

    /// Read file in chunks (for large files)
    pub fn read_chunks<P: AsRef<Path>, F: FnMut(&[u8])>(
        path: P,
        chunk_size: usize,
        mut callback: F,
    ) -> FileResult<()> {
        let path = path.as_ref();
        if !path.exists() {
            return Err(FileError::NotFound(path.to_string_lossy().to_string()));
        }
        let file = File::open(path).map_err(|e| FileError::IoError(e.to_string()))?;
        let mut reader = BufReader::with_capacity(chunk_size, file);
        loop {
            let buffer = reader.fill_buf().map_err(|e| FileError::IoError(e.to_string()))?;
            let length = buffer.len();
            if length == 0 {
                break;
            }
            callback(buffer);
            reader.consume(length);
        }
        Ok(())
    }

    // =========================================================================
    // File Writing Operations
    // =========================================================================

    /// Write string to file (overwrite if exists)
    pub fn write_string<P: AsRef<Path>>(path: P, content: &str) -> FileResult<()> {
        let path = path.as_ref();
        fs::write(path, content).map_err(|e| FileError::IoError(e.to_string()))?;
        Ok(())
    }

    /// Write bytes to file (overwrite if exists)
    pub fn write_bytes<P: AsRef<Path>>(path: P, content: &[u8]) -> FileResult<()> {
        let path = path.as_ref();
        fs::write(path, content).map_err(|e| FileError::IoError(e.to_string()))?;
        Ok(())
    }

    /// Append string to file (create if not exists)
    pub fn append_string<P: AsRef<Path>>(path: P, content: &str) -> FileResult<()> {
        let path = path.as_ref();
        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(path)
            .map_err(|e| FileError::IoError(e.to_string()))?;
        file.write_all(content.as_bytes())
            .map_err(|e| FileError::IoError(e.to_string()))?;
        Ok(())
    }

    /// Append bytes to file (create if not exists)
    pub fn append_bytes<P: AsRef<Path>>(path: P, content: &[u8]) -> FileResult<()> {
        let path = path.as_ref();
        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(path)
            .map_err(|e| FileError::IoError(e.to_string()))?;
        file.write_all(content)
            .map_err(|e| FileError::IoError(e.to_string()))?;
        Ok(())
    }

    // =========================================================================
    // File Existence and Metadata
    // =========================================================================

    /// Check if path exists
    pub fn exists<P: AsRef<Path>>(path: P) -> bool {
        path.as_ref().exists()
    }

    /// Check if path is a file
    pub fn is_file<P: AsRef<Path>>(path: P) -> bool {
        path.as_ref().is_file()
    }

    /// Check if path is a directory
    pub fn is_dir<P: AsRef<Path>>(path: P) -> bool {
        path.as_ref().is_dir()
    }

    /// Check if path is a symbolic link
    pub fn is_symlink<P: AsRef<Path>>(path: P) -> bool {
        fs::symlink_metadata(path).map(|m| m
