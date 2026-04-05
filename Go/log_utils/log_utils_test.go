package log_utils

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// TestLogLevelString tests LogLevel.String()
func TestLogLevelString(t *testing.T) {
	tests := []struct {
		level    LogLevel
		expected string
	}{
		{DEBUG, "DEBUG"},
		{INFO, "INFO"},
		{WARN, "WARN"},
		{ERROR, "ERROR"},
		{FATAL, "FATAL"},
		{LogLevel(99), "UNKNOWN"},
	}

	for _, test := range tests {
		result := test.level.String()
		if result != test.expected {
			t.Errorf("LogLevel(%d).String() = %s, expected %s", test.level, result, test.expected)
		}
	}
}

// TestLevelFromString tests LevelFromString()
func TestLevelFromString(t *testing.T) {
	tests := []struct {
		input    string
		expected LogLevel
	}{
		{"DEBUG", DEBUG},
		{"debug", DEBUG},
		{"INFO", INFO},
		{"WARN", WARN},
		{"WARNING", WARN},
		{"ERROR", ERROR},
		{"FATAL", FATAL},
		{"unknown", INFO},
		{"", INFO},
	}

	for _, test := range tests {
		result := LevelFromString(test.input)
		if result != test.expected {
			t.Errorf("LevelFromString(%s) = %d, expected %d", test.input, result, test.expected)
		}
	}
}

// TestNewLogger tests NewLogger()
func TestNewLogger(t *testing.T) {
	logger := NewLogger(DEBUG)
	if logger == nil {
		t.Fatal("NewLogger returned nil")
	}
	if logger.GetLevel() != DEBUG {
		t.Errorf("Expected level DEBUG, got %d", logger.GetLevel())
	}
}

// TestDefaultConfig tests DefaultConfig()
func TestDefaultConfig(t *testing.T) {
	config := DefaultConfig()
	if config.Level != INFO {
		t.Errorf("Expected default level INFO, got %d", config.Level)
	}
	if config.Output != OutputStdout {
		t.Errorf("Expected default output stdout, got %d", config.Output)
	}
	if config.Format != FormatText {
		t.Errorf("Expected default format text, got %d", config.Format)
	}
	if config.MaxSize != 100*1024*1024 {
		t.Errorf("Expected default max size 100MB, got %d", config.MaxSize)
	}
}

// TestSetLevel tests SetLevel() and GetLevel()
func TestSetLevel(t *testing.T) {
	logger := NewLogger(INFO)
	
	logger.SetLevel(DEBUG)
	if logger.GetLevel() != DEBUG {
		t.Errorf("Expected level DEBUG after SetLevel, got %d", logger.GetLevel())
	}
	
	logger.SetLevel(ERROR)
	if logger.GetLevel() != ERROR {
		t.Errorf("Expected level ERROR after SetLevel, got %d", logger.GetLevel())
	}
}

// TestLogLevelFiltering tests that messages below the level are filtered
func TestLogLevelFiltering(t *testing.T) {
	// Create a buffer to capture output
	var buf bytes.Buffer
	
	logger := &Logger{
		config: Config{
			Level:      WARN,
			Output:     OutputStdout,
			Format:     FormatText,
			TimeFormat: time.RFC3339,
		},
		writer: &buf,
	}
	
	logger.Debug("debug message")
	logger.Info("info message")
	logger.Warn("warn message")
	logger.Error("error message")
	
	output := buf.String()
	
	if strings.Contains(output, "debug message") {
		t.Error("DEBUG message should be filtered")
	}
	if strings.Contains(output, "info message") {
		t.Error("INFO message should be filtered")
	}
	if !strings.Contains(output, "warn message") {
		t.Error("WARN message should not be filtered")
	}
	if !strings.Contains(output, "error message") {
		t.Error("ERROR message should not be filtered")
	}
}

// TestLogEntryFormatText tests text formatting
func TestLogEntryFormatText(t *testing.T) {
	entry := LogEntry{
		Timestamp: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
		Level:     "INFO",
		Message:   "test message",
		Caller:    "test.go:42",
		Fields:    map[string]interface{}{"key": "value"},
	}
	
	result := entry.formatText("2006-01-02 15:04:05")
	
	if !strings.Contains(result, "2024-01-15 10:30:00") {
		t.Error("Expected timestamp in output")
	}
	if !strings.Contains(result, "[INFO]") {
		t.Error("Expected level in output")
	}
	if !strings.Contains(result, "test message") {
		t.Error("Expected message in output")
	}
	if !strings.Contains(result, "(test.go:42)") {
		t.Error("Expected caller in output")
	}
	if !strings.Contains(result, "key=value") {
		t.Error("Expected fields in output")
	}
}

// TestLogEntryFormatJSON tests JSON formatting
func TestLogEntryFormatJSON(t *testing.T) {
	entry := LogEntry{
		Timestamp: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
		Level:     "INFO",
		Message:   "test message",
		Fields:    map[string]interface{}{"key": "value"},
	}
	
	jsonBytes, err := entry.formatJSON()
	if err != nil {
		t.Fatalf("formatJSON failed: %v", err)
	}
	
	var result map[string]interface{}
	if err := json.Unmarshal(jsonBytes, &result); err != nil {
		t.Fatalf("Failed to unmarshal JSON: %v", err)
	}
	
	if result["level"] != "INFO" {
		t.Errorf("Expected level INFO, got %v", result["level"])
	}
	if result["message"] != "test message" {
		t.Errorf("Expected message 'test message', got %v", result["message"])
	}
}

// TestLoggerWithFields tests logging with key-value pairs
func TestLoggerWithFields(t *testing.T) {
	var buf bytes.Buffer
	
	logger := &Logger{
		config: Config{
			Level:      DEBUG,
			Output:     OutputStdout,
			Format:     FormatText,
			TimeFormat: time.RFC3339,
		},
		writer: &buf,
	}
	
	logger.Info("user action", "user_id", 123, "action", "login")
	
	output := buf.String()
	if !strings.Contains(output, "user_id=123") {
		t.Error("Expected user_id field in output")
	}
	if !strings.Contains(output, "action=login") {
		t.Error("Expected action field in output")
	}
}

// TestLoggerWithPrefix tests prefix functionality
func TestLoggerWithPrefix(t *testing.T) {
	var buf bytes.Buffer
	
	logger := &Logger{
		config: Config{
			Level:      DEBUG,
			Output:     OutputStdout,
			Format:     FormatText,
			TimeFormat: time.RFC3339,
			Prefix:     "[APP]",
		},
		writer: &buf,
	}
	
	logger.Info("test message")
	
	output := buf.String()
	if !strings.Contains(output, "[APP] test message") {
		t.Error("Expected prefix in output")
	}
}

// TestFormattedMethods tests Debugf, Infof, Warnf, Errorf
func TestFormattedMethods(t *testing.T) {
	var buf bytes.Buffer
	
	logger := &Logger{
		config: Config{
			Level:      DEBUG,
			Output:     OutputStdout,
			Format:     FormatText,
			TimeFormat: time.RFC3339,
		},
		writer: &buf,
	}
	
	logger.Debugf("debug %s %d", "test", 42)
	logger.Infof("info %s", "message")
	logger.Warnf("warn %d", 123)
	logger.Errorf("error %s", "failed")
	
	output := buf.String()
	
	if !strings.Contains(output, "debug test 42") {
		t.Error("Expected formatted debug message")
	}
	if !strings.Contains(output, "info message") {
		t.Error("Expected formatted info message")
	}
	if !strings.Contains(output, "warn 123") {
		t.Error("Expected formatted warn message")
	}
	if !strings.Contains(output, "error failed") {
		t.Error("Expected formatted error message")
	}
}

// TestFileLogging tests file output
func TestFileLogging(t *testing.T) {
	// Create temporary directory
	tempDir := t.TempDir()
	logFile := filepath.Join(tempDir, "test.log")
	
	config := Config{
		Level:      DEBUG,
		Output:     OutputFile,
		Format:     FormatText,
		FilePath:   logFile,
		TimeFormat: time.RFC3339,
	}
	
	logger := NewWithConfig(config)
	defer logger.Close()
	
	logger.Info("test message")
	
	// Read the log file
	content, err := os.ReadFile(logFile)
	if err != nil {
		t.Fatalf("Failed to read log file: %v", err)
	}
	
	if !strings.Contains(string(content), "test message") {
		t.Error("Expected message in log file")
	}
}

// TestJSONOutput tests JSON format output
func TestJSONOutput(t *testing.T) {
	var buf bytes.Buffer
	
	logger := &Logger{
		config: Config{
			Level:      DEBUG,
			Output:     OutputStdout,
			Format:     FormatJSON,
			TimeFormat: time.RFC3339,
		},
		writer: &buf,
	}
	
	logger.Info("json test", "key", "value")
	
	// Parse the JSON output
	lines := strings.Split(strings.TrimSpace(buf.String()), "\n")
	if len(lines) == 0 {
		t.Fatal("No output generated")
	}
	
	var entry map[string]interface{}
	if err := json.Unmarshal([]byte(lines[0]), &entry); err != nil {
		t.Fatalf("Failed to parse JSON: %v", err)
	}
	
	if entry["level"] != "INFO" {
		t.Errorf("Expected level INFO, got %v", entry["level"])
	}
	if entry["message"] != "json test" {
		t.Errorf("Expected message 'json test', got %v", entry["message"])
	}
}

// TestClose tests Close()
func TestClose(t *testing.T) {
	tempDir := t.TempDir()
	logFile := filepath.Join(tempDir, "test.log")
	
	config := Config{
		Level:      DEBUG,
		Output:     OutputFile,
		Format:     FormatText,
		FilePath:   logFile,
		TimeFormat: time.RFC3339,
	}
	
	logger := NewWithConfig(config)
	logger.Info("before close")
	
	err := logger.Close()
	if err != nil {
		t.Errorf("Close() returned error: %v", err)
	}
}

// TestWithPrefixMethod tests WithPrefix()
func TestWithPrefixMethod(t *testing.T) {
	logger := NewLogger(INFO)
	newLogger := logger.WithPrefix("[TEST]")
	
	if newLogger.config.Prefix != "[TEST]" {
		t.Errorf("Expected prefix '[TEST]', got '%s'", newLogger.config.Prefix)
	}
}

// TestGetCaller tests getCaller()
func TestGetCaller(t *testing.T) {
	caller := getCaller(1)
	if caller == "" {
		t.Error("getCaller returned empty string")
	}
	if caller == "unknown:0" {
		t.Error("getCaller failed to get caller info")
	}
}
