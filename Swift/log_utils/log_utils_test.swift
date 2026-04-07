import Foundation
@testable import log_utils

/**
 * Log Utilities Test Suite
 *
 * Comprehensive tests for the LogUtils module.
 */

// MARK: - LogLevel Tests

func testLogLevel() {
    print("Testing LogLevel...")
    
    // Test descriptions
    assert(LogLevel.debug.description == "DEBUG", "Debug description failed")
    assert(LogLevel.info.description == "INFO", "Info description failed")
    assert(LogLevel.warn.description == "WARN", "Warn description failed")
    assert(LogLevel.error.description == "ERROR", "Error description failed")
    assert(LogLevel.fatal.description == "FATAL", "Fatal description failed")
    
    // Test short descriptions
    assert(LogLevel.debug.shortDescription == "D", "Debug short description failed")
    assert(LogLevel.fatal.shortDescription == "F", "Fatal short description failed")
    
    // Test raw values
    assert(LogLevel.debug.rawValue == 0, "Debug raw value failed")
    assert(LogLevel.fatal.rawValue == 4, "Fatal raw value failed")
    
    print("✓ LogLevel tests passed")
}

// MARK: - LogEntry Tests

func testLogEntry() {
    print("Testing LogEntry...")
    
    let entry = LogEntry(
        level: .info,
        message: "Test message",
        file: "/path/to/file.swift",
        function: "testFunction",
        line: 42
    )
    
    assert(entry.level == .info, "Level mismatch")
    assert(entry.message == "Test message", "Message mismatch")
    assert(entry.file == "file.swift", "File name extraction failed")
    assert(entry.function == "testFunction", "Function mismatch")
    assert(entry.line == 42, "Line mismatch")
    
    print("✓ LogEntry tests passed")
}

// MARK: - DefaultLogFormatter Tests

func testDefaultLogFormatter() {
    print("Testing DefaultLogFormatter...")
    
    let entry = LogEntry(
        timestamp: Date(timeIntervalSince1970: 1609459200), // 2021-01-01 00:00:00 UTC
        level: .info,
        message: "Test",
        file: "test.swift",
        function: "testFunc",
        line: 10
    )
    
    // Test default formatter
    let formatter = DefaultLogFormatter()
    let formatted = formatter.format(entry)
    assert(!formatted.isEmpty, "Formatted string should not be empty")
    assert(formatted.contains("INFO"), "Should contain INFO level")
    assert(formatted.contains("Test"), "Should contain message")
    
    // Test with emoji
    let emojiFormatter = DefaultLogFormatter(useEmoji: true)
    let emojiFormatted = emojiFormatter.format(entry)
    assert(emojiFormatted.contains("ℹ️"), "Should contain info emoji")
    
    // Test without timestamp
    let noTimeFormatter = DefaultLogFormatter(includeTimestamp: false)
    let noTimeFormatted = noTimeFormatter.format(entry)
    assert(!noTimeFormatted.contains("2021"), "Should not contain timestamp")
    
    print("✓ DefaultLogFormatter tests passed")
}

// MARK: - ConsoleLogHandler Tests

func testConsoleLogHandler() {
    print("Testing ConsoleLogHandler...")
    
    let handler = ConsoleLogHandler(minLevel: .warn)
    
    // Test that debug entry is filtered
    let debugEntry = LogEntry(level: .debug, message: "Debug")
    // Should not print (would need manual verification)
    handler.log(debugEntry)
    
    // Test that warn entry passes through
    let warnEntry = LogEntry(level: .warn, message: "Warning")
    handler.log(warnEntry)
    
    handler.flush()
    
    print("✓ ConsoleLogHandler tests passed")
}

// MARK: - FileLogHandler Tests

func testFileLogHandler() {
    print("Testing FileLogHandler...")
    
    let tempDir = FileManager.default.temporaryDirectory
    let logFile = tempDir.appendingPathComponent("test_log_\(UUID().uuidString).log")
    
    let handler = FileLogHandler(
        fileURL: logFile,
        minLevel: .info,
        maxFileSize: 1024 * 1024
    )
    
    // Test logging
    let entry = LogEntry(level: .info, message: "Test log entry")
    handler.log(entry)
    handler.flush()
    
    // Verify file exists and contains content
    assert(FileManager.default.fileExists(atPath: logFile.path), "Log file should exist")
    
    if let content = try? String(contentsOf: logFile, encoding: .utf8) {
        assert(content.contains("Test log entry"), "Log file should contain message")
        assert(content.contains("INFO"), "Log file should contain level")
    } else {
        assert(false, "Could not read log file")
    }
    
    // Cleanup
    try? FileManager.default.removeItem(at: logFile)
    
    print("✓ FileLogHandler tests passed")
}

// MARK: - Logger Tests

func testLogger() {
    print("Testing Logger...")
    
    let logger = Logger.shared
    logger.removeAllHandlers()
    logger.addHandler(ConsoleLogHandler(minLevel: .debug))
    logger.minLevel = .debug
    
    // Test log methods
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warn("Warning message")
    logger.error("Error message")
    logger.fatal("Fatal message")
    
    // Test with metadata
    logger.info("Message with metadata", metadata: ["key": "value"])
    
    logger.flush()
    
    print("✓ Logger tests passed")
}

// MARK: - LogUtils Tests

func testLogUtils() {
    print("Testing LogUtils...")
    
    // Test console handler creation
    let consoleHandler = LogUtils.consoleHandler(minLevel: .info, useEmoji: true)
    assert(consoleHandler.minLevel == .info, "Min level should be info")
    
    // Test file handler creation
    let tempPath = FileManager.default.temporaryDirectory.appendingPathComponent("test.log").path
    let fileHandler = LogUtils.fileHandler(path: tempPath, minLevel: .warn)
    assert(fileHandler.minLevel == .warn, "Min level should be warn")
    
    // Test level configuration
    LogUtils.setLevel(.error)
    assert(LogUtils.getLevel() == .error, "Level should be error")
    assert(LogUtils.isEnabled(.fatal), "Fatal should be enabled")
    assert(!LogUtils.isEnabled(.info), "Info should not be enabled")
    
    // Reset level
    LogUtils.setLevel(.debug)
    
    // Cleanup
    try? FileManager.default.removeItem(atPath: tempPath)
    
    print("✓ LogUtils tests passed")
}

// MARK: - Main Test Runner

func runAllTests() {
    print("\n=== Running LogUtils Tests ===\n")
    
    testLogLevel()
    testLogEntry()
    testDefaultLogFormatter()
    testConsoleLogHandler()
    testFileLogHandler()
    testLogger()
    testLogUtils()
    
    print("\n=== All Tests Passed ===")
}

// Run tests
runAllTests()
