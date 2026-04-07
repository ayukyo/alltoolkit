import Foundation

/**
 * Log Utilities Module
 *
 * A comprehensive logging utility for Swift providing multiple log levels,
 * formatted output, file logging, and customizable log handlers.
 *
 * Features:
 * - Multiple log levels: DEBUG, INFO, WARN, ERROR, FATAL
 * - Formatted output with timestamps, log level, and source location
 * - Console and file logging support
 * - Thread-safe logging operations
 * - Customizable log formatters and handlers
 * - Log level filtering
 * - Automatic log file rotation
 *
 * Author: AllToolkit
 * Version: 1.0.0
 */

// MARK: - Log Level

/**
 * Log level enumeration representing the severity of log messages.
 */
public enum LogLevel: Int, CaseIterable, CustomStringConvertible {
    case debug = 0
    case info = 1
    case warn = 2
    case error = 3
    case fatal = 4
    
    public var description: String {
        switch self {
        case .debug: return "DEBUG"
        case .info:  return "INFO"
        case .warn:  return "WARN"
        case .error: return "ERROR"
        case .fatal: return "FATAL"
        }
    }
    
    public var shortDescription: String {
        switch self {
        case .debug: return "D"
        case .info:  return "I"
        case .warn:  return "W"
        case .error: return "E"
        case .fatal: return "F"
        }
    }
    
    public var emoji: String {
        switch self {
        case .debug: return "🐛"
        case .info:  return "ℹ️"
        case .warn:  return "⚠️"
        case .error: return "❌"
        case .fatal: return "💀"
        }
    }
}

// MARK: - Log Entry

/**
 * Represents a single log entry with all metadata.
 */
public struct LogEntry {
    public let timestamp: Date
    public let level: LogLevel
    public let message: String
    public let file: String
    public let function: String
    public let line: Int
    public let thread: String
    public let metadata: [String: Any]?
    
    public init(
        timestamp: Date = Date(),
        level: LogLevel,
        message: String,
        file: String = #file,
        function: String = #function,
        line: Int = #line,
        thread: String = Thread.current.description,
        metadata: [String: Any]? = nil
    ) {
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.file = (file as NSString).lastPathComponent
        self.function = function
        self.line = line
        self.thread = thread
        self.metadata = metadata
    }
}

// MARK: - Log Formatter Protocol

/**
 * Protocol for formatting log entries into strings.
 */
public protocol LogFormatter {
    func format(_ entry: LogEntry) -> String
}

// MARK: - Default Log Formatter

/**
 * Default log formatter with customizable options.
 */
public struct DefaultLogFormatter: LogFormatter {
    public var includeTimestamp: Bool
    public var includeLevel: Bool
    public var includeSource: Bool
    public var includeThread: Bool
    public var useEmoji: Bool
    public var dateFormat: String
    
    public init(
        includeTimestamp: Bool = true,
        includeLevel: Bool = true,
        includeSource: Bool = true,
        includeThread: Bool = false,
        useEmoji: Bool = false,
        dateFormat: String = "yyyy-MM-dd HH:mm:ss.SSS"
    ) {
        self.includeTimestamp = includeTimestamp
        self.includeLevel = includeLevel
        self.includeSource = includeSource
        self.includeThread = includeThread
        self.useEmoji = useEmoji
        self.dateFormat = dateFormat
    }
    
    public func format(_ entry: LogEntry) -> String {
        var parts: [String] = []
        
        if includeTimestamp {
            let formatter = DateFormatter()
            formatter.dateFormat = dateFormat
            parts.append(formatter.string(from: entry.timestamp))
        }
        
        if includeLevel {
            let levelStr = useEmoji ? entry.level.emoji : entry.level.description
            parts.append("[\(levelStr)]")
        }
        
        if includeThread {
            parts.append("[\(entry.thread)]")
        }
        
        if includeSource {
            parts.append("\(entry.file):\(entry.line) \(entry.function)")
        }
        
        parts.append(entry.message)
        
        return parts.joined(separator: " ")
    }
}

// MARK: - Log Handler Protocol

/**
 * Protocol for log handlers that process log entries.
 */
public protocol LogHandler {
    func log(_ entry: LogEntry)
    func flush()
}

// MARK: - Console Log Handler

/**
 * Log handler that outputs to console/stdout.
 */
public class ConsoleLogHandler: LogHandler {
    public var formatter: LogFormatter
    public var minLevel: LogLevel
    private let lock = NSLock()
    
    public init(formatter: LogFormatter = DefaultLogFormatter(), minLevel: LogLevel = .debug) {
        self.formatter = formatter
        self.minLevel = minLevel
    }
    
    public func log(_ entry: LogEntry) {
        guard entry.level.rawValue >= minLevel.rawValue else { return }
        
        lock.lock()
        defer { lock.unlock() }
        
        let formatted = formatter.format(entry)
        print(formatted)
    }
    
    public func flush() {
        fflush(stdout)
    }
}

// MARK: - File Log Handler

/**
 * Log handler that writes to a file with optional rotation.
 */
public class FileLogHandler: LogHandler {
    public var formatter: LogFormatter
    public var minLevel: LogLevel
    public var maxFileSize: Int64
    public var maxFiles: Int
    
    private let fileURL: URL
    private let lock = NSLock()
    private var fileHandle: FileHandle?
    
    public init(
        fileURL: URL,
        formatter: LogFormatter = DefaultLogFormatter(),
        minLevel: LogLevel = .debug,
        maxFileSize: Int64 = 10 * 1024 * 1024,
        maxFiles: Int = 5
    ) {
        self.fileURL = fileURL
        self.formatter = formatter
        self.minLevel = minLevel
        self.maxFileSize = maxFileSize
        self.maxFiles = maxFiles
        
        ensureDirectoryExists()
        openFile()
    }
    
    deinit {
        closeFile()
    }
    
    private func ensureDirectoryExists() {
        let directory = fileURL.deletingLastPathComponent()
        try? FileManager.default.createDirectory(
            at: directory,
            withIntermediateDirectories: true,
            attributes: nil
        )
    }
    
    private func openFile() {
        if !FileManager.default.fileExists(atPath: fileURL.path) {
            FileManager.default.createFile(atPath: fileURL.path, contents: nil, attributes: nil)
        }
        fileHandle = try? FileHandle(forWritingTo: fileURL)
        fileHandle?.seekToEndOfFile()
    }
    
    private func closeFile() {
        fileHandle?.closeFile()
        fileHandle = nil
    }
    
    private func rotateIfNeeded() {
        guard let attributes = try? FileManager.default.attributesOfItem(atPath: fileURL.path),
              let fileSize = attributes[.size] as? Int64,
              fileSize >= maxFileSize else {
            return
        }
        
        closeFile()
        
        for i in (1..<maxFiles).reversed() {
            let oldURL = fileURL.appendingPathExtension("\(i)")
            let newURL = fileURL.appendingPathExtension("\(i + 1)")
            
            if FileManager.default.fileExists(atPath: oldURL.path) {
                try? FileManager.default.removeItem(at: newURL)
                try? FileManager.default.moveItem(at: oldURL, to: newURL)
            }
        }
        
        let rotatedURL = fileURL.appendingPathExtension("1")
        try? FileManager.default.removeItem(at: rotatedURL)
        try? FileManager.default.moveItem(at: fileURL, to: rotatedURL)
        
        openFile()
    }
    
    public func log(_ entry: LogEntry) {
        guard entry.level.rawValue >= minLevel.rawValue else { return }
        
        lock.lock()
        defer { lock.unlock() }
        
        rotateIfNeeded()
        
        let formatted = formatter.format(entry) + "\n"
        if let data = formatted.data(using: .utf8) {
            fileHandle?.write(data)
        }
    }
    
    public func flush() {
        fileHandle?.synchronizeFile()
    }
}

// MARK: - Logger

/**
 * Main logger class that manages log handlers and provides logging methods.
 */
public class Logger {
    public static let shared = Logger()
    
    public var handlers: [LogHandler] = []
    public var minLevel: LogLevel = .debug
    
    private init() {
        handlers.append(ConsoleLogHandler())
    }
    
    public func addHandler(_ handler: LogHandler) {
        handlers.append(handler)
    }
    
    public func removeAllHandlers() {
        handlers.removeAll()
    }
    
    public func log(
        _ level: LogLevel,
        _ message: String,
        file: String = #file,
        function: String = #function,
        line: Int = #line,
        metadata: [String: Any]? = nil
    ) {
        guard level.rawValue >= minLevel.rawValue else { return }
        
        let entry = LogEntry(
            level: level,
            message: message,
            file: file,
            function: function,
            line: line,
            metadata: metadata
        )
        
        for handler in handlers {
            handler.log(entry)
        }
    }
    
    public func debug(_ message: String, file: String = #file, function: String = #function, line: Int = #line, metadata: [String: Any]? = nil) {
        log(.debug, message, file: file, function: function, line: line, metadata: metadata)
    }
    
    public func info(_ message: String, file: String = #file, function: String = #function, line: Int = #line, metadata: [String: Any]? = nil) {
        log(.info, message, file: file, function: function, line: line, metadata: metadata)
    }
    
    public func warn(_ message: String, file: String = #file, function: String = #function, line: Int = #line, metadata: [String: Any]? = nil) {
        log(.warn, message, file: file, function: function, line: line, metadata: metadata)
    }
    
    public func error(_ message: String, file: String = #file, function: String = #function, line: Int = #line, metadata: [String: Any]? = nil) {
        log(.error, message, file: file, function: function, line: line, metadata: metadata)
    }
    
    public func fatal(_ message: String, file: String = #file, function: String = #function, line: Int = #line, metadata: [String: Any]? = nil) {
        log(.fatal, message, file: file, function: function, line: line, metadata: metadata)
    }
    
    public func flush() {
        for handler in handlers {
            handler.flush()
        }
    }
}

// MARK: - Log Utils

/**
 * Utility functions for logging.
 */
public struct LogUtils {
    
    /**
     * Creates a console log handler.
     *
     * - Parameters:
     *   - minLevel: Minimum log level to output
     *   - useEmoji: Whether to use emoji for log levels
     *   - includeSource: Whether to include source file and line
     * - Returns: A configured ConsoleLogHandler
     */
    public static func consoleHandler(
        minLevel: LogLevel = .debug,
        useEmoji: Bool = false,
        includeSource: Bool = true
    ) -> ConsoleLogHandler {
        let formatter = DefaultLogFormatter(
            includeSource: includeSource,
            useEmoji: useEmoji
        )
        return ConsoleLogHandler(formatter: formatter, minLevel: minLevel)
    }
    
    /**
     * Creates a file log handler.
     *
     * - Parameters:
     *   - path: Path to log file
     *   - minLevel: Minimum log level to write
     *   - maxFileSize: Maximum file size before rotation (default 10MB)
     *   - maxFiles: Maximum number of rotated files to keep
     * - Returns: A configured FileLogHandler
     */
    public static func fileHandler(
        path: String,
        minLevel: LogLevel = .debug,
        maxFileSize: Int64 = 10 * 1024 * 1024,
        maxFiles: Int = 5
    ) -> FileLogHandler {
        let url = URL(fileURLWithPath: path)
        return FileLogHandler(
            fileURL: url,
            minLevel: minLevel,
            maxFileSize: maxFileSize,
            maxFiles: maxFiles
        )
    }
    
    /**
     * Configures the shared logger with custom handlers.
     *
     * - Parameters:
     *   - handlers: Array of log handlers
     *   - minLevel: Minimum log level
     */
    public static func configure(
        handlers: [LogHandler],
        minLevel: LogLevel = .debug
    ) {
        Logger.shared.removeAllHandlers()
        for handler in handlers {
            Logger.shared.addHandler(handler)
        }
        Logger.shared.minLevel = minLevel
    }
    
    /**
     * Sets the minimum log level for the shared logger.
     *
     * - Parameter level: The minimum log level
     */
    public static func setLevel(_ level: LogLevel) {
        Logger.shared.minLevel = level
    }
    
    /**
     * Gets the current log level.
     *
     * - Returns: The current minimum log level
     */
    public static func getLevel() -> LogLevel {
        return Logger.shared.minLevel
    }
    
    /**
     * Checks if a log level is enabled.
     *
     * - Parameter level: The log level to check
     * - Returns: True if the level is enabled
     */
    public static func isEnabled(_ level: LogLevel) -> Bool {
        return level.rawValue >= Logger.shared.minLevel.rawValue
    }
    
    /**
     * Flushes all log handlers.
     */
    public static func flush() {
        Logger.shared.flush()
    }
}
