import Foundation

/**
 * Log Utilities Example
 *
 * Demonstrates various features of the LogUtils module.
 */

// Import the module (in practice, use: import log_utils)
// For this example, we assume the module is in the same directory

// MARK: - Example 1: Basic Logging

func exampleBasicLogging() {
    print("\n=== Example 1: Basic Logging ===")
    
    // Use the shared logger
    Logger.shared.info("Application started")
    Logger.shared.debug("Debug information")
    Logger.shared.warn("This is a warning")
    Logger.shared.error("An error occurred")
    
    // With metadata
    Logger.shared.info("User action", metadata: ["userId": "12345", "action": "login"])
}

// MARK: - Example 2: Custom Log Level

func exampleCustomLogLevel() {
    print("\n=== Example 2: Custom Log Level ===")
    
    // Set minimum log level to warn (debug and info will be filtered)
    LogUtils.setLevel(.warn)
    
    Logger.shared.debug("This will NOT be logged")
    Logger.shared.info("This will NOT be logged")
    Logger.shared.warn("This WILL be logged")
    Logger.shared.error("This WILL be logged")
    
    // Reset to debug for other examples
    LogUtils.setLevel(.debug)
}

// MARK: - Example 3: Console Handler with Emoji

func exampleEmojiLogging() {
    print("\n=== Example 3: Emoji Logging ===")
    
    let emojiHandler = LogUtils.consoleHandler(
        minLevel: .debug,
        useEmoji: true,
        includeSource: false
    )
    
    let logger = Logger.shared
    logger.removeAllHandlers()
    logger.addHandler(emojiHandler)
    
    logger.debug("Debug with emoji")
    logger.info("Info with emoji")
    logger.warn("Warning with emoji")
    logger.error("Error with emoji")
    logger.fatal("Fatal with emoji")
    
    // Reset to default
    logger.removeAllHandlers()
    logger.addHandler(ConsoleLogHandler())
}

// MARK: - Example 4: File Logging

func exampleFileLogging() {
    print("\n=== Example 4: File Logging ===")
    
    let tempDir = FileManager.default.temporaryDirectory
    let logPath = tempDir.appendingPathComponent("app_\(UUID().uuidString).log").path
    
    print("Log file: \(logPath)")
    
    // Create file handler
    let fileHandler = LogUtils.fileHandler(
        path: logPath,
        minLevel: .info,
        maxFileSize: 1024 * 1024,  // 1MB
        maxFiles: 3
    )
    
    let logger = Logger.shared
    logger.removeAllHandlers()
    logger.addHandler(fileHandler)
    
    // Log some messages
    logger.info("Application started")
    logger.info("Processing request...")
    logger.warn("Slow response detected")
    logger.error("Failed to connect to database")
    
    logger.flush()
    
    // Read and display log file
    if let content = try? String(contentsOfFile: logPath, encoding: .utf8) {
        print("\nLog file contents:")
        print(content)
    }
    
    // Cleanup
    try? FileManager.default.removeItem(atPath: logPath)
    
    // Reset
    logger.removeAllHandlers()
    logger.addHandler(ConsoleLogHandler())
}

// MARK: - Example 5: Multiple Handlers

func exampleMultipleHandlers() {
    print("\n=== Example 5: Multiple Handlers ===")
    
    let tempDir = FileManager.default.temporaryDirectory
    let logPath = tempDir.appendingPathComponent("multi_\(UUID().uuidString).log").path
    
    // Configure logger with both console and file handlers
    LogUtils.configure(
        handlers: [
            LogUtils.consoleHandler(minLevel: .info),
            LogUtils.fileHandler(path: logPath, minLevel: .debug)
        ],
        minLevel: .debug
    )
    
    Logger.shared.info("This goes to both console and file")
    Logger.shared.debug("This only goes to file (console filters debug)")
    
    Logger.shared.flush()
    
    // Show file contents
    if let content = try? String(contentsOfFile: logPath, encoding: .utf8) {
        print("\nFile contains \(content.components(separatedBy: .newlines).count - 1) lines")
    }
    
    // Cleanup
    try? FileManager.default.removeItem(atPath: logPath)
    
    // Reset
    Logger.shared.removeAllHandlers()
    Logger.shared.addHandler(ConsoleLogHandler())
}

// MARK: - Example 6: Custom Formatter

func exampleCustomFormatter() {
    print("\n=== Example 6: Custom Formatter ===")
    
    // Create a simple formatter that only shows level and message
    struct SimpleFormatter: LogFormatter {
        func format(_ entry: LogEntry) -> String {
            return "[\(entry.level.shortDescription)] \(entry.message)"
        }
    }
    
    let handler = ConsoleLogHandler(
        formatter: SimpleFormatter(),
        minLevel: .debug
    )
    
    let logger = Logger.shared
    logger.removeAllHandlers()
    logger.addHandler(handler)
    
    logger.info("Simple format info")
    logger.warn("Simple format warning")
    
    // Reset
    logger.removeAllHandlers()
    logger.addHandler(ConsoleLogHandler())
}

// MARK: - Example 7: Conditional Logging

func exampleConditionalLogging() {
    print("\n=== Example 7: Conditional Logging ===")
    
    // Check if a level is enabled before doing expensive operations
    if LogUtils.isEnabled(.debug) {
        let expensiveData = generateExpensiveDebugInfo()
        Logger.shared.debug(expensiveData)
    }
    
    // This pattern is useful when debug info is expensive to generate
    func generateExpensiveDebugInfo() -> String {
        // Simulate expensive operation
        var result = "Debug info: "
        for i in 0..<100 {
            result += "\(i),"
        }
        return result
    }
}

// MARK: - Main

print("Swift LogUtils Examples")
print("=======================")

exampleBasicLogging()
exampleCustomLogLevel()
exampleEmojiLogging()
exampleFileLogging()
exampleMultipleHandlers()
exampleCustomFormatter()
exampleConditionalLogging()

print("\n=== All Examples Completed ===")
