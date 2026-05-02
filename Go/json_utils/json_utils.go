// Package jsonutils provides advanced JSON manipulation and utilities.
// Built on Go's standard encoding/json package with enhanced functionality.
// All functions are safe for concurrent use.
package jsonutils

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"reflect"
	"sort"
	"strconv"
	"strings"
)

// JSONOp represents a JSON operation result
type JSONOp struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// JSONPathResult represents the result of a JSON path query
type JSONPathResult struct {
	Found   bool        `json:"found"`
	Value   interface{} `json:"value,omitempty"`
	Path    string      `json:"path"`
	Matches int         `json:"matches"`
	Error   string      `json:"error,omitempty"`
}

// SchemaField represents a field in a JSON schema
type SchemaField struct {
	Name     string `json:"name"`
	Type     string `json:"type"`
	Required bool   `json:"required"`
	Default  interface{} `json:"default,omitempty"`
}

// JSONSchema represents a simple JSON schema
type JSONSchema struct {
	Name        string        `json:"name"`
	Description string        `json:"description,omitempty"`
	Fields      []SchemaField `json:"fields"`
}

// ValidateResult represents validation result
type ValidateResult struct {
	Valid   bool     `json:"valid"`
	Errors  []string `json:"errors,omitempty"`
	Warnings []string `json:"warnings,omitempty"`
}

// PrettyPrint formats JSON with indentation
//
// Parameters:
//   - data: Input JSON data (string, []byte, or interface{})
//   - indent: Indentation string (e.g., "  " for 2 spaces)
//
// Returns:
//   - Formatted JSON string
//   - Error if formatting fails
//
// Examples:
//
//     json := `{"name":"John","age":30}`
//     formatted, err := PrettyPrint(json, "  ")
//     // Returns indented JSON
func PrettyPrint(data interface{}, indent string) (string, error) {
	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return "", fmt.Errorf("marshal error: %w", err)
		}
	}

	// Parse and re-format with indentation
	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return "", fmt.Errorf("parse error: %w", err)
	}

	if indent == "" {
		indent = "  "
	}

	result, err := json.MarshalIndent(parsed, "", indent)
	if err != nil {
		return "", fmt.Errorf("format error: %w", err)
	}

	return string(result), nil
}

// Minify removes all whitespace from JSON
//
// Parameters:
//   - data: Input JSON data
//
// Returns:
//   - Minified JSON string
//   - Error if minification fails
//
// Example:
//
//     json := `{ "name": "John", "age": 30 }`
//     minified, err := Minify(json)
//     // Returns: {"name":"John","age":30}
func Minify(data interface{}) (string, error) {
	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return "", fmt.Errorf("marshal error: %w", err)
		}
	}

	// Parse to validate
	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return "", fmt.Errorf("parse error: %w", err)
	}

	// Re-marshal without indentation
	result, err := json.Marshal(parsed)
	if err != nil {
		return "", fmt.Errorf("minify error: %w", err)
	}

	return string(result), nil
}

// Get retrieves a value from JSON using dot notation path
//
// Parameters:
//   - data: Input JSON data
//   - path: Dot-notation path (e.g., "user.address.city")
//
// Returns:
//   - JSONPathResult with found value or error
//
// Examples:
//
//     json := `{"user": {"name": "John", "age": 30}}`
//     result := Get(json, "user.name")
//     // result.Found = true, result.Value = "John"
//
//     result := Get(json, "user.email")
//     // result.Found = false
func Get(data interface{}, path string) JSONPathResult {
	result := JSONPathResult{Path: path, Matches: 0}

	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			result.Error = err.Error()
			return result
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		result.Error = err.Error()
		return result
	}

	parts := strings.Split(path, ".")
	value, found := getByPath(parsed, parts)

	if found {
		result.Found = true
		result.Value = value
		result.Matches = 1
	}

	return result
}

// getByPath navigates through nested maps/slices
func getByPath(data interface{}, parts []string) (interface{}, bool) {
	current := data

	for _, part := range parts {
		switch v := current.(type) {
		case map[string]interface{}:
			if val, ok := v[part]; ok {
				current = val
			} else {
				return nil, false
			}
		case []interface{}:
			index, err := strconv.Atoi(part)
			if err != nil || index < 0 || index >= len(v) {
				return nil, false
			}
			current = v[index]
		default:
			return nil, false
		}
	}

	return current, true
}

// Set sets a value in JSON using dot notation path
//
// Parameters:
//   - data: Input JSON data
//   - path: Dot-notation path
//   - value: Value to set
//
// Returns:
//   - Modified JSON string
//   - Error if operation fails
//
// Example:
//
//     json := `{"user": {"name": "John"}}`
//     result, err := Set(json, "user.age", 30)
//     // Returns: {"user":{"name":"John","age":30}}
func Set(data interface{}, path string, value interface{}) (string, error) {
	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return "", fmt.Errorf("marshal error: %w", err)
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return "", fmt.Errorf("parse error: %w", err)
	}

	parts := strings.Split(path, ".")
	if err := setByPath(&parsed, parts, value); err != nil {
		return "", err
	}

	result, err := json.Marshal(parsed)
	if err != nil {
		return "", fmt.Errorf("marshal error: %w", err)
	}

	return string(result), nil
}

// setByPath sets value at specified path
func setByPath(data *interface{}, parts []string, value interface{}) error {
	if len(parts) == 0 {
		*data = value
		return nil
	}

	current := *data
	part := parts[0]
	remaining := parts[1:]

	switch v := current.(type) {
	case map[string]interface{}:
		if len(remaining) == 0 {
			v[part] = value
			return nil
		}
		if _, exists := v[part]; !exists {
			v[part] = make(map[string]interface{})
		}
		nested := v[part]
		return setByPath(&nested, remaining, value)

	case []interface{}:
		index, err := strconv.Atoi(part)
		if err != nil || index < 0 || index >= len(v) {
			return fmt.Errorf("invalid array index: %s", part)
		}
		if len(remaining) == 0 {
			v[index] = value
			return nil
		}
		nested := v[index]
		return setByPath(&nested, remaining, value)

	default:
		return fmt.Errorf("cannot navigate into %T", current)
	}
}

// Delete removes a field from JSON using dot notation path
//
// Parameters:
//   - data: Input JSON data
//   - path: Dot-notation path to delete
//
// Returns:
//   - Modified JSON string
//   - Error if operation fails
//
// Example:
//
//     json := `{"user": {"name": "John", "age": 30}}`
//     result, err := Delete(json, "user.age")
//     // Returns: {"user":{"name":"John"}}
func Delete(data interface{}, path string) (string, error) {
	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return "", fmt.Errorf("marshal error: %w", err)
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return "", fmt.Errorf("parse error: %w", err)
	}

	parts := strings.Split(path, ".")
	if err := deleteByPath(&parsed, parts); err != nil {
		return "", err
	}

	result, err := json.Marshal(parsed)
	if err != nil {
		return "", fmt.Errorf("marshal error: %w", err)
	}

	return string(result), nil
}

// deleteByPath removes field at specified path
func deleteByPath(data *interface{}, parts []string) error {
	if len(parts) == 0 {
		return fmt.Errorf("cannot delete root")
	}

	current := *data
	part := parts[0]
	remaining := parts[1:]

	switch v := current.(type) {
	case map[string]interface{}:
		if len(remaining) == 0 {
			if _, exists := v[part]; !exists {
				return fmt.Errorf("path not found: %s", part)
			}
			delete(v, part)
			return nil
		}
		nested, exists := v[part]
		if !exists {
			return fmt.Errorf("path not found: %s", part)
		}
		return deleteByPath(&nested, remaining)

	case []interface{}:
		index, err := strconv.Atoi(part)
		if err != nil || index < 0 || index >= len(v) {
			return fmt.Errorf("invalid array index: %s", part)
		}
		if len(remaining) == 0 {
			// Remove element from array
			v[index] = nil
			return nil
		}
		nested := v[index]
		return deleteByPath(&nested, remaining)

	default:
		return fmt.Errorf("cannot navigate into %T", current)
	}
}

// Merge combines multiple JSON objects
//
// Parameters:
//   - datas: Variable number of JSON data sources
//
// Returns:
//   - Merged JSON string
//   - Error if merge fails
//
// Note: Later values override earlier values for same keys
//
// Example:
//
//     json1 := `{"a": 1, "b": 2}`
//     json2 := `{"b": 3, "c": 4}`
//     result, err := Merge(json1, json2)
//     // Returns: {"a":1,"b":3,"c":4}
func Merge(datas ...interface{}) (string, error) {
	result := make(map[string]interface{})

	for _, data := range datas {
		var jsonData []byte
		var err error

		switch v := data.(type) {
		case string:
			jsonData = []byte(v)
		case []byte:
			jsonData = v
		default:
			jsonData, err = json.Marshal(data)
			if err != nil {
				return "", fmt.Errorf("marshal error: %w", err)
			}
		}

		var parsed map[string]interface{}
		if err := json.Unmarshal(jsonData, &parsed); err != nil {
			return "", fmt.Errorf("parse error: %w", err)
		}

		// Deep merge
		deepMerge(result, parsed)
	}

	merged, err := json.Marshal(result)
	if err != nil {
		return "", fmt.Errorf("marshal error: %w", err)
	}

	return string(merged), nil
}

// deepMerge recursively merges maps
func deepMerge(dst, src map[string]interface{}) {
	for key, srcVal := range src {
		if dstVal, exists := dst[key]; exists {
			if dstMap, ok := dstVal.(map[string]interface{}); ok {
				if srcMap, ok := srcVal.(map[string]interface{}); ok {
					deepMerge(dstMap, srcMap)
					continue
				}
			}
		}
		dst[key] = srcVal
	}
}

// Validate checks if JSON is valid and optionally validates against schema
//
// Parameters:
//   - data: Input JSON data
//   - schema: Optional JSONSchema for validation
//
// Returns:
//   - ValidateResult with validation status and errors
//
// Example:
//
//     json := `{"name": "John", "age": 30}`
//     result := Validate(json, nil)
//     // result.Valid = true
func Validate(data interface{}, schema *JSONSchema) ValidateResult {
	result := ValidateResult{Valid: true}

	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			result.Valid = false
			result.Errors = append(result.Errors, fmt.Sprintf("marshal error: %v", err))
			return result
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		result.Valid = false
		result.Errors = append(result.Errors, fmt.Sprintf("parse error: %v", err))
		return result
	}

	// Schema validation
	if schema != nil {
		schemaValidate(parsed, schema, &result)
	}

	return result
}

// schemaValidate validates against schema
func schemaValidate(data interface{}, schema *JSONSchema, result *ValidateResult) {
	obj, ok := data.(map[string]interface{})
	if !ok {
		result.Valid = false
		result.Errors = append(result.Errors, "data must be a JSON object")
		return
	}

	fieldMap := make(map[string]SchemaField)
	for _, field := range schema.Fields {
		fieldMap[field.Name] = field
	}

	// Check required fields
	for _, field := range schema.Fields {
		if field.Required {
			if _, exists := obj[field.Name]; !exists {
				result.Valid = false
				result.Errors = append(result.Errors, fmt.Sprintf("missing required field: %s", field.Name))
			}
		}
	}

	// Check field types
	for key, val := range obj {
		if field, exists := fieldMap[key]; exists {
			if err := checkType(val, field.Type); err != nil {
				result.Warnings = append(result.Warnings, fmt.Sprintf("field %s: %v", key, err))
			}
		}
	}
}

// checkType validates value type
func checkType(val interface{}, expectedType string) error {
	if val == nil {
		return nil
	}

	switch expectedType {
	case "string":
		if _, ok := val.(string); !ok {
			return fmt.Errorf("expected string, got %T", val)
		}
	case "number", "int", "float":
		switch val.(type) {
		case float64, float32, int, int64, int32:
			return nil
		default:
			return fmt.Errorf("expected number, got %T", val)
		}
	case "boolean", "bool":
		if _, ok := val.(bool); !ok {
			return fmt.Errorf("expected boolean, got %T", val)
		}
	case "array", "list":
		if _, ok := val.([]interface{}); !ok {
			return fmt.Errorf("expected array, got %T", val)
		}
	case "object", "map":
		if _, ok := val.(map[string]interface{}); !ok {
			return fmt.Errorf("expected object, got %T", val)
		}
	}

	return nil
}

// ExtractKeys extracts all keys from JSON at any level
//
// Parameters:
//   - data: Input JSON data
//
// Returns:
//   - Sorted list of unique keys
//   - Error if extraction fails
//
// Example:
//
//     json := `{"user": {"name": "John", "age": 30}, "status": "active"}`
//     keys, err := ExtractKeys(json)
//     // Returns: ["age", "name", "status", "user"]
func ExtractKeys(data interface{}) ([]string, error) {
	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return nil, fmt.Errorf("marshal error: %w", err)
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return nil, fmt.Errorf("parse error: %w", err)
	}

	keys := make(map[string]bool)
	extractKeysRecursive(parsed, keys)

	result := make([]string, 0, len(keys))
	for key := range keys {
		result = append(result, key)
	}
	sort.Strings(result)

	return result, nil
}

// extractKeysRecursive extracts keys recursively
func extractKeysRecursive(data interface{}, keys map[string]bool) {
	switch v := data.(type) {
	case map[string]interface{}:
		for key, val := range v {
			keys[key] = true
			extractKeysRecursive(val, keys)
		}
	case []interface{}:
		for _, item := range v {
			extractKeysRecursive(item, keys)
		}
	}
}

// CountValues counts occurrences of values in JSON
//
// Parameters:
//   - data: Input JSON data
//   - path: Optional path to count values at (empty for root)
//
// Returns:
//   - Map of values to counts
//   - Error if counting fails
//
// Example:
//
//     json := `{"items": [{"type": "a"}, {"type": "b"}, {"type": "a"}]}`
//     counts, err := CountValues(json, "items.type")
//     // Returns: {"a": 2, "b": 1}
func CountValues(data interface{}, path string) (map[string]int, error) {
	result := make(map[string]int)

	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return nil, fmt.Errorf("marshal error: %w", err)
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return nil, fmt.Errorf("parse error: %w", err)
	}

	if path != "" {
		parts := strings.Split(path, ".")
		// Special handling for array path traversal
		countValuesAtPath(parsed, parts, result)
	} else {
		countValuesRecursive(parsed, result)
	}
	return result, nil
}

// countValuesAtPath counts values at a specific path, handling arrays
func countValuesAtPath(data interface{}, parts []string, counts map[string]int) {
	if len(parts) == 0 {
		if str, ok := data.(string); ok {
			counts[str]++
		} else {
			countValuesRecursive(data, counts)
		}
		return
	}

	part := parts[0]
	remaining := parts[1:]

	switch v := data.(type) {
	case map[string]interface{}:
		if val, ok := v[part]; ok {
			countValuesAtPath(val, remaining, counts)
		}
	case []interface{}:
		// Traverse all array elements
		for _, item := range v {
			countValuesAtPath(item, parts, counts)
		}
	default:
		// Skip
	}
}

// countValuesRecursive counts values recursively
func countValuesRecursive(data interface{}, counts map[string]int) {
	switch v := data.(type) {
	case []interface{}:
		for _, item := range v {
			if str, ok := item.(string); ok {
				counts[str]++
			} else {
				countValuesRecursive(item, counts)
			}
		}
	case map[string]interface{}:
		for _, val := range v {
			if str, ok := val.(string); ok {
				counts[str]++
			} else {
				countValuesRecursive(val, counts)
			}
		}
	}
}

// Transform applies a transformation function to all string values
//
// Parameters:
//   - data: Input JSON data
//   - fn: Transformation function (func(string) string)
//
// Returns:
//   - Transformed JSON string
//   - Error if transformation fails
//
// Example:
//
//     json := `{"name": "john", "city": "new york"}`
//     result, err := Transform(json, strings.ToUpper)
//     // Returns: {"name":"JOHN","city":"NEW YORK"}
func Transform(data interface{}, fn func(string) string) (string, error) {
	var jsonData []byte
	var err error

	switch v := data.(type) {
	case string:
		jsonData = []byte(v)
	case []byte:
		jsonData = v
	default:
		jsonData, err = json.Marshal(data)
		if err != nil {
			return "", fmt.Errorf("marshal error: %w", err)
		}
	}

	var parsed interface{}
	if err := json.Unmarshal(jsonData, &parsed); err != nil {
		return "", fmt.Errorf("parse error: %w", err)
	}

	transformRecursive(&parsed, fn)

	result, err := json.Marshal(parsed)
	if err != nil {
		return "", fmt.Errorf("marshal error: %w", err)
	}

	return string(result), nil
}

// transformRecursive applies transformation recursively
func transformRecursive(data *interface{}, fn func(string) string) {
	switch v := (*data).(type) {
	case string:
		*data = fn(v)
	case []interface{}:
		for i := range v {
			transformRecursive(&v[i], fn)
		}
	case map[string]interface{}:
		newMap := make(map[string]interface{})
		for key, val := range v {
			newKey := fn(key)
			transformRecursive(&val, fn)
			newMap[newKey] = val
		}
		*data = newMap
	}
}

// Diff compares two JSON objects and returns differences
//
// Parameters:
//   - data1: First JSON data
//   - data2: Second JSON data
//
// Returns:
//   - Map with "added", "removed", "changed" keys
//   - Error if comparison fails
//
// Example:
//
//     json1 := `{"a": 1, "b": 2}`
//     json2 := `{"a": 1, "c": 3}`
//     diff, err := Diff(json1, json2)
//     // Returns differences between json1 and json2
func Diff(data1, data2 interface{}) (map[string]interface{}, error) {
	result := map[string]interface{}{
		"added":   map[string]interface{}{},
		"removed": map[string]interface{}{},
		"changed": map[string]interface{}{},
	}

	var obj1, obj2 map[string]interface{}

	// Parse first JSON
	switch v := data1.(type) {
	case string:
		if err := json.Unmarshal([]byte(v), &obj1); err != nil {
			return nil, fmt.Errorf("parse error 1: %w", err)
		}
	case []byte:
		if err := json.Unmarshal(v, &obj1); err != nil {
			return nil, fmt.Errorf("parse error 1: %w", err)
		}
	default:
		jsonData, _ := json.Marshal(data1)
		json.Unmarshal(jsonData, &obj1)
	}

	// Parse second JSON
	switch v := data2.(type) {
	case string:
		if err := json.Unmarshal([]byte(v), &obj2); err != nil {
			return nil, fmt.Errorf("parse error 2: %w", err)
		}
	case []byte:
		if err := json.Unmarshal(v, &obj2); err != nil {
			return nil, fmt.Errorf("parse error 2: %w", err)
		}
	default:
		jsonData, _ := json.Marshal(data2)
		json.Unmarshal(jsonData, &obj2)
	}

	if obj1 == nil {
		obj1 = make(map[string]interface{})
	}
	if obj2 == nil {
		obj2 = make(map[string]interface{})
	}

	diffMaps(obj1, obj2, result)

	return result, nil
}

// diffMaps compares two maps
func diffMaps(obj1, obj2 map[string]interface{}, result map[string]interface{}) {
	added := result["added"].(map[string]interface{})
	removed := result["removed"].(map[string]interface{})
	changed := result["changed"].(map[string]interface{})

	// Find added and changed
	for key, val2 := range obj2 {
		if val1, exists := obj1[key]; !exists {
			added[key] = val2
		} else if !reflect.DeepEqual(val1, val2) {
			changed[key] = map[string]interface{}{
				"old": val1,
				"new": val2,
			}
		}
	}

	// Find removed
	for key, val1 := range obj1 {
		if _, exists := obj2[key]; !exists {
			removed[key] = val1
		}
	}
}

// ReadFile reads and parses JSON from a file
//
// Parameters:
//   - filename: Path to JSON file
//
// Returns:
//   - Parsed JSON as interface{}
//   - Error if reading fails
//
// Example:
//
//     data, err := ReadFile("config.json")
func ReadFile(filename string) (interface{}, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("open error: %w", err)
	}
	defer file.Close()

	var data interface{}
	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&data); err != nil {
		if err == io.EOF {
			return nil, fmt.Errorf("empty file: %s", filename)
		}
		return nil, fmt.Errorf("decode error: %w", err)
	}

	return data, nil
}

// WriteFile writes JSON data to a file
//
// Parameters:
//   - filename: Output file path
//   - data: JSON data to write
//   - indent: Optional indentation (empty for compact)
//
// Returns:
//   - Error if writing fails
//
// Example:
//
//     err := WriteFile("output.json", data, "  ")
func WriteFile(filename string, data interface{}, indent string) error {
	var jsonData []byte
	var err error

	if indent != "" {
		jsonData, err = json.MarshalIndent(data, "", indent)
	} else {
		jsonData, err = json.Marshal(data)
	}
	if err != nil {
		return fmt.Errorf("marshal error: %w", err)
	}

	if err := os.WriteFile(filename, jsonData, 0644); err != nil {
		return fmt.Errorf("write error: %w", err)
	}

	return nil
}

// ToMap converts any JSON-compatible value to map[string]interface{}
//
// Parameters:
//   - data: Input data
//
// Returns:
//   - Map representation
//   - Error if conversion fails
func ToMap(data interface{}) (map[string]interface{}, error) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return nil, fmt.Errorf("marshal error: %w", err)
	}

	var result map[string]interface{}
	if err := json.Unmarshal(jsonData, &result); err != nil {
		return nil, fmt.Errorf("unmarshal error: %w", err)
	}

	return result, nil
}

// FromMap converts map to typed struct
//
// Parameters:
//   - m: Input map
//   - target: Pointer to target struct
//
// Returns:
//   - Error if conversion fails
//
// Example:
//
//     var user User
//     err := FromMap(data, &user)
func FromMap(m map[string]interface{}, target interface{}) error {
	jsonData, err := json.Marshal(m)
	if err != nil {
		return fmt.Errorf("marshal error: %w", err)
	}

	if err := json.Unmarshal(jsonData, target); err != nil {
		return fmt.Errorf("unmarshal error: %w", err)
	}

	return nil
}

// Buffer creates a JSON buffer for efficient building
type Buffer struct {
	buf bytes.Buffer
}

// NewBuffer creates a new JSON buffer
func NewBuffer() *Buffer {
	return &Buffer{}
}

// StartObject begins a JSON object
func (b *Buffer) StartObject() *Buffer {
	b.buf.WriteByte('{')
	return b
}

// EndObject ends a JSON object
func (b *Buffer) EndObject() *Buffer {
	// Remove trailing comma if present
	if b.buf.Len() > 1 && b.buf.Bytes()[b.buf.Len()-1] == ',' {
		b.buf.Truncate(b.buf.Len() - 1)
	}
	b.buf.WriteByte('}')
	return b
}

// Key adds a key to the current object
func (b *Buffer) Key(key string) *Buffer {
	if b.buf.Len() > 1 && b.buf.Bytes()[b.buf.Len()-1] != '{' {
		b.buf.WriteByte(',')
	}
	b.buf.WriteString(fmt.Sprintf(`"%s":`, key))
	return b
}

// AddString adds a string value
func (b *Buffer) AddString(val string) *Buffer {
	b.buf.WriteString(fmt.Sprintf(`"%s"`, escapeJSON(val)))
	return b
}

// Number adds a numeric value
func (b *Buffer) Number(val float64) *Buffer {
	b.buf.WriteString(strconv.FormatFloat(val, 'f', -1, 64))
	return b
}

// Bool adds a boolean value
func (b *Buffer) Bool(val bool) *Buffer {
	if val {
		b.buf.WriteString("true")
	} else {
		b.buf.WriteString("false")
	}
	return b
}

// Null adds a null value
func (b *Buffer) Null() *Buffer {
	b.buf.WriteString("null")
	return b
}

// String returns the built JSON
func (b *Buffer) String() string {
	return b.buf.String()
}

// escapeJSON escapes special characters in strings
func escapeJSON(s string) string {
	s = strings.ReplaceAll(s, `\`, `\\`)
	s = strings.ReplaceAll(s, `"`, `\"`)
	s = strings.ReplaceAll(s, "\n", `\n`)
	s = strings.ReplaceAll(s, "\r", `\r`)
	s = strings.ReplaceAll(s, "\t", `\t`)
	return s
}

// ArrayBuilder helps build JSON arrays
type ArrayBuilder struct {
	buf  bytes.Buffer
	first bool
}

// NewArrayBuilder creates a new array builder
func NewArrayBuilder() *ArrayBuilder {
	ab := &ArrayBuilder{first: true}
	ab.buf.WriteByte('[')
	return ab
}

// Add adds a value to the array
func (ab *ArrayBuilder) Add(val interface{}) *ArrayBuilder {
	if !ab.first {
		ab.buf.WriteByte(',')
	}
	ab.first = false

	jsonData, _ := json.Marshal(val)
	ab.buf.Write(jsonData)
	return ab
}

// String returns the built JSON array
func (ab *ArrayBuilder) String() string {
	ab.buf.WriteByte(']')
	return ab.buf.String()
}
