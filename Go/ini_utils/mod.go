// Package ini_utils provides a comprehensive INI file parser and writer for Go.
// Zero dependencies - uses only Go standard library.
//
// Features:
// - Read and write INI files
// - Support for sections and global properties
// - Type-safe value getters with defaults
// - Comment preservation (read/write roundtrip)
// - Array values via comma-separated lists
// - Case-insensitive section and key lookup
// - Pretty printing with customizable indentation
//
// Example usage:
//
//	// Load from file
//	ini, err := ini_utils.LoadFile("config.ini")
//	if err != nil {
//	    log.Fatal(err)
//	}
//
//	// Read values
//	dbHost := ini.GetString("database", "host", "localhost")
//	dbPort := ini.GetInt("database", "port", 3306)
//	dbEnabled := ini.GetBool("database", "enabled", false)
//
//	// Set values
//	ini.Set("database", "timeout", "30")
//	ini.SetInt("database", "max_connections", 100)
//
//	// Save back to file
//	err = ini.SaveToFile("config.ini")
package ini_utils

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// IniFile represents an INI configuration file with sections and key-value pairs.
type IniFile struct {
	sections     map[string]map[string]string
	comments     map[string]map[string]string
	sectionOrder []string
	keyOrder     map[string][]string
	globalKeys   map[string]string
	globalOrder  []string
}

// IniOptions configures INI file parsing and writing behavior.
type IniOptions struct {
	Delimiter         string
	CommentChar       string
	AllowNoValue      bool
	PreserveSpacing   bool
	LowercaseKeys     bool
	LowercaseSections bool
}

// DefaultOptions returns the default INI parsing options.
func DefaultOptions() IniOptions {
	return IniOptions{
		Delimiter:         "=",
		CommentChar:       ";",
		AllowNoValue:      false,
		PreserveSpacing:   false,
		LowercaseKeys:     false,
		LowercaseSections: false,
	}
}

// New creates a new empty IniFile.
func New() *IniFile {
	return &IniFile{
		sections:     make(map[string]map[string]string),
		comments:     make(map[string]map[string]string),
		sectionOrder: []string{},
		keyOrder:     make(map[string][]string),
		globalKeys:   make(map[string]string),
		globalOrder:  []string{},
	}
}

// LoadFile loads an INI file from the specified path.
func LoadFile(filename string) (*IniFile, error) {
	return LoadFileWithOptions(filename, DefaultOptions())
}

// LoadFileWithOptions loads an INI file with custom parsing options.
func LoadFileWithOptions(filename string, opts IniOptions) (*IniFile, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}
	return ParseWithOptions(string(data), opts)
}

// Parse parses INI data from a string.
func Parse(data string) (*IniFile, error) {
	return ParseWithOptions(data, DefaultOptions())
}

// ParseWithOptions parses INI data with custom options.
func ParseWithOptions(data string, opts IniOptions) (*IniFile, error) {
	ini := New()
	scanner := bufio.NewScanner(strings.NewReader(data))

	var currentSection string
	var currentComment strings.Builder

	for scanner.Scan() {
		line := scanner.Text()
		trimmed := strings.TrimSpace(line)

		if trimmed == "" {
			continue
		}

		if strings.HasPrefix(trimmed, opts.CommentChar) || strings.HasPrefix(trimmed, "#") {
			if currentComment.Len() > 0 {
				currentComment.WriteString("\n")
			}
			currentComment.WriteString(trimmed)
			continue
		}

		if strings.HasPrefix(trimmed, "[") && strings.HasSuffix(trimmed, "]") {
			sectionName := trimmed[1 : len(trimmed)-1]
			if opts.LowercaseSections {
				sectionName = strings.ToLower(sectionName)
			}

			if _, exists := ini.sections[sectionName]; !exists {
				ini.sections[sectionName] = make(map[string]string)
				ini.comments[sectionName] = make(map[string]string)
				ini.keyOrder[sectionName] = []string{}
				ini.sectionOrder = append(ini.sectionOrder, sectionName)
			}

			currentSection = sectionName

			if currentComment.Len() > 0 {
				ini.comments[sectionName]["__section__"] = currentComment.String()
				currentComment.Reset()
			}
			continue
		}

		delimIdx := strings.Index(trimmed, opts.Delimiter)
		if delimIdx < 0 {
			if opts.AllowNoValue {
				key := trimmed
				if opts.LowercaseKeys {
					key = strings.ToLower(key)
				}
				ini.setKey(currentSection, key, "", currentComment.String())
				currentComment.Reset()
			}
			continue
		}

		key := strings.TrimSpace(trimmed[:delimIdx])
		value := trimmed[delimIdx+1:]
		if !opts.PreserveSpacing {
			value = strings.TrimSpace(value)
		}

		if opts.LowercaseKeys {
			key = strings.ToLower(key)
		}

		ini.setKey(currentSection, key, value, currentComment.String())
		currentComment.Reset()
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("parse error: %w", err)
	}

	return ini, nil
}

func (ini *IniFile) setKey(section, key, value, comment string) {
	if section == "" {
		if _, exists := ini.globalKeys[key]; !exists {
			ini.globalOrder = append(ini.globalOrder, key)
		}
		ini.globalKeys[key] = value
		if comment != "" {
			if ini.comments["__global__"] == nil {
				ini.comments["__global__"] = make(map[string]string)
			}
			ini.comments["__global__"][key] = comment
		}
	} else {
		if _, exists := ini.sections[section][key]; !exists {
			ini.keyOrder[section] = append(ini.keyOrder[section], key)
		}
		ini.sections[section][key] = value
		if comment != "" {
			ini.comments[section][key] = comment
		}
	}
}

// Get retrieves a string value from the specified section and key.
func (ini *IniFile) Get(section, key string, defaultValue string) string {
	if section == "" {
		if val, exists := ini.globalKeys[key]; exists {
			return val
		}
		return defaultValue
	}

	if sec, exists := ini.sections[section]; exists {
		if val, exists := sec[key]; exists {
			return val
		}
	}
	return defaultValue
}

// GetString is an alias for Get.
func (ini *IniFile) GetString(section, key string, defaultValue string) string {
	return ini.Get(section, key, defaultValue)
}

// GetInt retrieves an integer value from the specified section and key.
func (ini *IniFile) GetInt(section, key string, defaultValue int) int {
	val := ini.Get(section, key, "")
	if val == "" {
		return defaultValue
	}
	if intVal, err := strconv.Atoi(val); err == nil {
		return intVal
	}
	return defaultValue
}

// GetInt64 retrieves an int64 value from the specified section and key.
func (ini *IniFile) GetInt64(section, key string, defaultValue int64) int64 {
	val := ini.Get(section, key, "")
	if val == "" {
		return defaultValue
	}
	if intVal, err := strconv.ParseInt(val, 10, 64); err == nil {
		return intVal
	}
	return defaultValue
}

// GetFloat64 retrieves a float64 value from the specified section and key.
func (ini *IniFile) GetFloat64(section, key string, defaultValue float64) float64 {
	val := ini.Get(section, key, "")
	if val == "" {
		return defaultValue
	}
	if floatVal, err := strconv.ParseFloat(val, 64); err == nil {
		return floatVal
	}
	return defaultValue
}

// GetBool retrieves a boolean value from the specified section and key.
func (ini *IniFile) GetBool(section, key string, defaultValue bool) bool {
	val := ini.Get(section, key, "")
	if val == "" {
		return defaultValue
	}
	val = strings.ToLower(val)
	switch val {
	case "true", "yes", "1", "on", "enabled":
		return true
	case "