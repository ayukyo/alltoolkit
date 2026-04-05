// Package log_utils provides a comprehensive logging utility for Go applications.
package log_utils

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"time"
)

// LogLevel represents the severity level of a log message
type LogLevel int

const (
	DEBUG LogLevel = 0
	INFO  LogLevel = 1
	WARN  LogLevel = 2
	ERROR LogLevel = 3
	FATAL LogLevel = 4
)

// OutputType defines where log messages are written
type OutputType int

const (
	OutputStdout OutputType = 0
	OutputStderr OutputType = 1
	OutputFile   OutputType = 2
)

// FormatType defines the log output format
type FormatType int

const (
	FormatText FormatType = 0
	FormatJSON FormatType = 1
)

// Config holds the logger configuration
type Config struct {
	Level         LogLevel
	Output        OutputType
	Format        FormatType
	FilePath      string
	MaxSize       int64
	MaxBackups    int
	IncludeCaller bool
	TimeFormat    string
	Prefix        string
}

// DefaultConfig returns a default configuration
func DefaultConfig() Config {
	return Config{
		Level:         INFO,
		Output:        OutputStdout,
		Format:        FormatText,
		MaxSize:       100 * 1024 * 1024,
		MaxBackups:    5,
		IncludeCaller: false,
		TimeFormat:    time.RFC3339,
		Prefix:        "",
	}
}

// Logger is the main logging struct
type Logger struct {
	config   Config
	mu       sync.Mutex
	writer   io.Writer
	file     *os.File
	fileSize int64
}

// NewLogger creates a new logger with the specified level
func NewLogger(level LogLevel) *Logger {
	config := DefaultConfig()
	config.Level = level
	return NewWithConfig(config)
}

// NewWithConfig creates a new logger with the specified configuration
func NewWithConfig(config Config) *Logger {
	logger := &Logger{
		config: config,
	}

	if config.TimeFormat == "" {
		config.TimeFormat = time.RFC3339
	}

	switch config.Output {
	case OutputStdout:
		logger.writer = os.Stdout
	case OutputStderr:
		logger.writer = os.Stderr
	case OutputFile:
		if err := logger.openFile(); err != nil {
			logger.writer = os.Stderr
			fmt.Fprintf(os.Stderr, "Failed to open log file: %v\n", err)
		}
	}

	return logger
}

// openFile opens or creates the log file
func (l *Logger) openFile() error {
	dir := filepath.Dir(l.config.FilePath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return err
	}

	file, err := os.OpenFile(l.config.FilePath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}

	stat, err := file.Stat()
	if err != nil {
		file.Close()
		return err
	}

	l.file = file
	l.writer = file
	l.fileSize = stat.Size()

	return nil
}

// rotate rotates the log file if it exceeds the maximum size
func (l *Logger) rotate() error {
	if l.config.Output != OutputFile || l.config.MaxSize <= 0 {
		return nil
	}

	if l.fileSize < l.config.MaxSize {
		return nil
	}

	if l.file != nil {
		l.file.Close()
	}

	for i := l.config.MaxBackups - 1; i > 0; i-- {
		oldPath := fmt.Sprintf("%s.%d", l.config.FilePath, i)
		newPath := fmt.Sprintf("%s.%d", l.config.FilePath, i+1)
		os.Rename(oldPath, newPath)
	}

	if l.config.MaxBackups > 0 {
		os.Rename(l.config.FilePath, l.config.FilePath+".1")
	}

	return l.openFile()
}

// Close closes the logger and any open files
func (l *Logger) Close() error {
	l.mu.Lock()
	defer l.mu.Unlock()

	if l.file != nil {
		return l.file.Close()
	}
	return nil
}

// SetLevel sets the minimum log level
func (l *Logger) SetLevel(level LogLevel) {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.config.Level = level
}

// GetLevel returns the current log level
func (l *Logger) GetLevel() LogLevel {
	l.mu.Lock()
	defer l.mu.Unlock()
	return l.config.Level
}

// LevelFromString converts a string to LogLevel
func LevelFromString(s string) LogLevel {
	switch strings.ToUpper(s) {
	case "DEBUG":
		return DEBUG
	case "INFO":
		return INFO
	case "WARN", "WARNING":
		return WARN
	case "ERROR":
		return ERROR
	case "FATAL":
		return FATAL
	default:
		return INFO
	}
}

// String returns the string representation of a log level
func (l LogLevel) String() string {
	switch l {
	case DEBUG:
		return "DEBUG"
	case INFO:
		return "INFO"
	case WARN:
		return "WARN"
	case ERROR:
		return "ERROR"
	case FATAL:
		return "FATAL"
	default:
		return "UNKNOWN"
	}
}

// getCaller returns the caller information (file:line)
func getCaller(skip int) string {
	_, file, line, ok := runtime.Caller(skip)
	if !ok {
		return "unknown:0"
	}
	file = filepath.Base(file)
	return fmt.Sprintf("%s:%d", file, line)
}

// LogEntry represents a single log entry
type LogEntry struct {
	Timestamp time.Time              `json:"timestamp"`
	Level     string                 `json:"level"`
	Message   string                 `json:"message"`
	Caller    string                 `json:"caller,omitempty"`
	Fields    map[string]interface{} `json:"fields,omitempty"`
}

// formatText formats a log entry as text
func (e LogEntry) formatText(timeFormat string) string {
	var parts []string
	parts = append(parts, e.Timestamp.Format(timeFormat))
	parts = append(parts, "["+e.Level+"]")
	if e.Caller != "" {
		parts = append(parts, "("+e.Caller+")")
	}
	parts = append(parts, e.Message)
	
	if len(e.Fields) > 0 {
		var fieldParts []string
		for k, v := range e.Fields {
			fieldParts = append(fieldParts, fmt.Sprintf("%s=%v", k, v))
		}
		parts = append(parts, "{"+strings.Join(fieldParts, " ")+"}")
	}
	
	return strings.Join(parts, " ")
}

// formatJSON formats a log entry as JSON
func (e LogEntry) formatJSON() ([]byte, error) {
	return json.Marshal(e)
}

// log writes a log message with the specified level
func (l *Logger) log(level LogLevel, message string, keysAndValues ...interface{}) {
	if level < l.config.Level {
		return
	}

	l.mu.Lock()
	defer l.mu.Unlock()

	if l.config.Output == OutputFile {
		l.rotate()
	}

	entry := LogEntry{
		Timestamp: time.Now(),
		Level:     level.String(),
		Message:   message,
		Fields:    make(map[string]interface{}),
	}

	if l.config.Prefix != "" {
		entry.Message = l.config.Prefix + " " + entry.Message
	}

	if l.config.IncludeCaller {
		entry.Caller = getCaller(4)
	}

	// Process key-value pairs
	for i := 0; i < len(keysAndValues)-1; i += 2 {
		key, ok := keysAndValues[i].(string)
		if ok {
			entry.Fields[key] = keysAndValues[i+1]
		}
	}

	var output []byte
	var err error

	if l.config.Format == FormatJSON {
		output, err = entry.formatJSON()
		if err != nil {
			output = []byte(entry.formatText(l.config.TimeFormat))
		}
	} else {
		output = []byte(entry.formatText(l.config.TimeFormat))
	}

	output = append(output, '\n')
	n, _ := l.writer.Write(output)
	l.fileSize += int64(n)
}

// Debug logs a debug message
func (l *Logger) Debug(message string, keysAndValues ...interface{}) {
	l.log(DEBUG, message, keysAndValues...)
}

// Info logs an info message
func (l *Logger) Info(message string, keysAndValues ...interface{}) {
	l.log(INFO, message, keysAndValues...)
}

// Warn logs a warning message
func (l *Logger) Warn(message string, keysAndValues ...interface{}) {
	l.log(WARN, message, keysAndValues...)
}

// Error logs an error message
func (l *Logger) Error(message string, keysAndValues ...interface{}) {
	l.log(ERROR, message, keysAndValues...)
}

// Fatal logs a fatal message and exits the application
func (l *Logger) Fatal(message string, keysAndValues ...interface{}) {
	l.log(FATAL, message, keysAndValues...)
	os.Exit(1)
}

// Debugf logs a formatted debug message
func (l *Logger) Debugf(format string, args ...interface{}) {
	l.Debug(fmt.Sprintf(format, args...))
}

// Infof logs a formatted info message
func (l *Logger) Infof(format string, args ...interface{}) {
	l.Info(fmt.Sprintf(format, args...))
}

// Warnf logs a formatted warning message
func (l *Logger) Warnf(format string, args ...interface{}) {
	l.Warn(fmt.Sprintf(format, args...))
}

// Errorf logs a formatted error message
func (l *Logger) Errorf(format string, args ...interface{}) {
	l.Error(fmt.Sprintf(format, args...))
}

// Fatalf logs a formatted fatal message and exits
func (l *Logger) Fatalf(format string, args ...interface{}) {
	l.Fatal(fmt.Sprintf(format, args...))
}

// With returns a new logger with the specified key-value pairs
func (l *Logger) With(keysAndValues ...interface{}) *Logger {
	newLogger := &Logger{
		config:   l.config,
		writer:   l.writer,
		file:     l.file,
		fileSize: l.fileSize,
	}
	return newLogger
}

// WithPrefix returns a new logger with the specified prefix
func (l *Logger) WithPrefix(prefix string) *Logger {
	newConfig := l.config
	newConfig.Prefix = prefix
	return NewWithConfig(newConfig)
}
