// Example program demonstrating log_utils functionality
package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/ayukyo/alltoolkit/Go/log_utils"
)

func main() {
	fmt.Println("=== Log Utils Example ===\n")

	// Example 1: Basic logging with different levels
	fmt.Println("1. Basic logging with different levels:")
	logger := log_utils.NewLogger(log_utils.DEBUG)
	logger.Debug("This is a debug message")
	logger.Info("This is an info message")
	logger.Warn("This is a warning message")
	logger.Error("This is an error message")
	fmt.Println()

	// Example 2: Logging with structured fields
	fmt.Println("2. Logging with structured fields:")
	logger.Info("User logged in", "user_id", 12345, "username", "john_doe", "ip", "192.168.1.1")
	logger.Error("Database connection failed", "error", "connection timeout", "retry", 3)
	fmt.Println()

	// Example 3: Formatted logging
	fmt.Println("3. Formatted logging:")
	logger.Infof("Processing %d items in %s", 42, "batch_001")
	logger.Warnf("Memory usage at %.2f%%", 85.5)
	logger.Errorf("Failed to open file: %s", "/path/to/file.txt")
	fmt.Println()

	// Example 4: Log level filtering
	fmt.Println("4. Log level filtering (only WARN and above):")
	filteredLogger := log_utils.NewLogger(log_utils.WARN)
	filteredLogger.Debug("This debug message will not appear")
	filteredLogger.Info("This info message will not appear")
	filteredLogger.Warn("This warning will appear")
	filteredLogger.Error("This error will appear")
	fmt.Println()

	// Example 5: Custom configuration with JSON format
	fmt.Println("5. JSON format output:")
	jsonConfig := log_utils.Config{
		Level:         log_utils.INFO,
		Output:        log_utils.OutputStdout,
		Format:        log_utils.FormatJSON,
		TimeFormat:    "2006-01-02T15:04:05.000Z",
		IncludeCaller: false,
	}
	jsonLogger := log_utils.NewWithConfig(jsonConfig)
	jsonLogger.Info("JSON formatted log", "service", "api", "version", "1.0.0")
	fmt.Println()

	// Example 6: File logging
	fmt.Println("6. File logging:")
	tempDir := os.TempDir()
	logFile := filepath.Join(tempDir, "example.log")
	
	fileConfig := log_utils.Config{
		Level:      log_utils.DEBUG,
		Output:     log_utils.OutputFile,
		Format:     log_utils.FormatText,
		FilePath:   logFile,
		MaxSize:    1024 * 1024, // 1MB
		MaxBackups: 3,
		TimeFormat: "2006-01-02 15:04:05",
	}
	
	fileLogger := log_utils.NewWithConfig(fileConfig)
	fileLogger.Info("Logging to file", "file", logFile)
	fileLogger.Debug("Debug message in file")
	fileLogger.Warn("Warning message in file")
	fileLogger.Close()
	
	// Read and display the log file content
	content, err := os.ReadFile(logFile)
	if err == nil {
		fmt.Printf("Log file content:\n%s\n", string(content))
	}
	fmt.Println()

	// Example 7: Logger with prefix
	fmt.Println("7. Logger with prefix:")
	prefixedLogger := logger.WithPrefix("[API-Server]")
	prefixedLogger.Info("Server started on port 8080")
	prefixedLogger.Info("Request received", "method", "GET", "path", "/api/users")
	fmt.Println()

	// Example 8: Dynamic log level changes
	fmt.Println("8. Dynamic log level changes:")
	dynamicLogger := log_utils.NewLogger(log_utils.INFO)
	dynamicLogger.Debug("This won't show (level is INFO)")
	dynamicLogger.SetLevel(log_utils.DEBUG)
	dynamicLogger.Debug("This will show now (level changed to DEBUG)")
	fmt.Printf("Current log level: %s\n", dynamicLogger.GetLevel().String())
	fmt.Println()

	// Example 9: String to level conversion
	fmt.Println("9. String to level conversion:")
	levels := []string{"debug", "info", "warn", "warning", "error", "fatal", "unknown"}
	for _, levelStr := range levels {
		level := log_utils.LevelFromString(levelStr)
		fmt.Printf("  LevelFromString(\"%s\") = %s\n", levelStr, level.String())
	}
	fmt.Println()

	// Example 10: Cleanup
	fmt.Println("10. Cleanup:")
	os.Remove(logFile)
	for i := 1; i <= 3; i++ {
		os.Remove(fmt.Sprintf("%s.%d", logFile, i))
	}
	fmt.Println("Cleaned up temporary log files")

	fmt.Println("\n=== Example Complete ===")
}
