package jsonutils

import (
	"encoding/json"
	"os"
	"strings"
	"testing"
)

// TestPrettyPrint tests JSON pretty printing
func TestPrettyPrint(t *testing.T) {
	tests := []struct {
		name     string
		input    interface{}
		indent   string
		wantErr  bool
	}{
		{
			name:    "simple object",
			input:   `{"name":"John","age":30}`,
			indent:  "  ",
			wantErr: false,
		},
		{
			name:    "nested object",
			input:   `{"user":{"name":"John","address":{"city":"NYC"}}}`,
			indent:  "    ",
			wantErr: false,
		},
		{
			name:    "invalid JSON",
			input:   `{invalid}`,
			indent:  "  ",
			wantErr: true,
		},
		{
			name:    "empty indent",
			input:   `{"a":1}`,
			indent:  "",
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := PrettyPrint(tt.input, tt.indent)
			if (err != nil) != tt.wantErr {
				t.Errorf("PrettyPrint() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && !strings.Contains(result, "{") {
				t.Error("PrettyPrint() result should contain JSON")
			}
		})
	}
}

// TestMinify tests JSON minification
func TestMinify(t *testing.T) {
	tests := []struct {
		name    string
		input   interface{}
		wantErr bool
	}{
		{
			name:    "with spaces",
			input:   `{ "name": "John", "age": 30 }`,
			wantErr: false,
		},
		{
			name:    "with newlines",
			input:   "{\n  \"name\": \"John\"\n}",
			wantErr: false,
		},
		{
			name:    "already minified",
			input:   `{"name":"John"}`,
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Minify(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("Minify() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				// Check no unnecessary whitespace
				if strings.Contains(result, " \n") || strings.Contains(result, "\n ") {
					t.Error("Minify() result contains unnecessary whitespace")
				}
			}
		})
	}
}

// TestGet tests JSON path retrieval
func TestGet(t *testing.T) {
	jsonData := `{"user": {"name": "John", "age": 30, "address": {"city": "NYC", "zip": "10001"}}, "status": "active"}`

	tests := []struct {
		name      string
		path      string
		wantFound bool
		wantValue interface{}
	}{
		{"simple key", "status", true, "active"},
		{"nested key", "user.name", true, "John"},
		{"deep nested", "user.address.city", true, "NYC"},
		{"non-existent", "user.email", false, nil},
		{"root level", "user", true, nil}, // Will be map
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Get(jsonData, tt.path)
			if result.Found != tt.wantFound {
				t.Errorf("Get() Found = %v, want %v", result.Found, tt.wantFound)
			}
			if tt.wantFound && tt.wantValue != nil {
				if result.Value != tt.wantValue {
					t.Errorf("Get() Value = %v, want %v", result.Value, tt.wantValue)
				}
			}
		})
	}
}

// TestSet tests JSON path setting
func TestSet(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		path    string
		value   interface{}
		wantErr bool
	}{
		{
			name:    "add new field",
			input:   `{"name": "John"}`,
			path:    "age",
			value:   30,
			wantErr: false,
		},
		{
			name:    "update existing",
			input:   `{"name": "John"}`,
			path:    "name",
			value:   "Jane",
			wantErr: false,
		},
		{
			name:    "nested path",
			input:   `{"user": {}}`,
			path:    "user.name",
			value:   "John",
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Set(tt.input, tt.path, tt.value)
			if (err != nil) != tt.wantErr {
				t.Errorf("Set() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				// Verify the result is valid JSON
				var parsed interface{}
				if err := parseJSON(result, &parsed); err != nil {
					t.Errorf("Set() result is not valid JSON: %v", err)
				}
			}
		})
	}
}

// TestDelete tests JSON field deletion
func TestDelete(t *testing.T) {
	tests := []struct {
		name      string
		input     string
		path      string
		wantErr   bool
		checkPath string
	}{
		{
			name:      "delete simple key",
			input:     `{"name": "John", "age": 30}`,
			path:      "age",
			wantErr:   false,
			checkPath: "age",
		},
		{
			name:      "delete nested key",
			input:     `{"user": {"name": "John", "age": 30}}`,
			path:      "user.age",
			wantErr:   false,
			checkPath: "user.age",
		},
		{
			name:      "non-existent key",
			input:     `{"name": "John"}`,
			path:      "age",
			wantErr:   true,
			checkPath: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Delete(tt.input, tt.path)
			if (err != nil) != tt.wantErr {
				t.Errorf("Delete() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				// Verify the field is removed
				getResult := Get(result, tt.checkPath)
				if getResult.Found {
					t.Error("Delete() field should be removed")
				}
			}
		})
	}
}

// TestMerge tests JSON merging
func TestMerge(t *testing.T) {
	tests := []struct {
		name     string
		inputs   []string
		expected string
		wantErr  bool
	}{
		{
			name:     "simple merge",
			inputs:   []string{`{"a": 1}`, `{"b": 2}`},
			expected: "", // Just check it works
			wantErr:  false,
		},
		{
			name:     "override values",
			inputs:   []string{`{"a": 1, "b": 2}`, `{"b": 3}`},
			expected: "",
			wantErr:  false,
		},
		{
			name:     "deep merge",
			inputs:   []string{`{"user": {"name": "John"}}`, `{"user": {"age": 30}}`},
			expected: "",
			wantErr:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			inputs := make([]interface{}, len(tt.inputs))
			for i, v := range tt.inputs {
				inputs[i] = v
			}
			result, err := Merge(inputs...)
			if (err != nil) != tt.wantErr {
				t.Errorf("Merge() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				var parsed interface{}
				if err := parseJSON(result, &parsed); err != nil {
					t.Errorf("Merge() result is not valid JSON: %v", err)
				}
			}
		})
	}
}

// TestValidate tests JSON validation
func TestValidate(t *testing.T) {
	tests := []struct {
		name     string
		input    interface{}
		schema   *JSONSchema
		wantValid bool
	}{
		{
			name:     "valid JSON",
			input:    `{"name": "John", "age": 30}`,
			schema:   nil,
			wantValid: true,
		},
		{
			name:     "invalid JSON",
			input:    `{invalid}`,
			schema:   nil,
			wantValid: false,
		},
		{
			name:  "valid with schema",
			input: `{"name": "John", "age": 30}`,
			schema: &JSONSchema{
				Name: "User",
				Fields: []SchemaField{
					{Name: "name", Type: "string", Required: true},
					{Name: "age", Type: "number", Required: false},
				},
			},
			wantValid: true,
		},
		{
			name:  "missing required field",
			input: `{"age": 30}`,
			schema: &JSONSchema{
				Name: "User",
				Fields: []SchemaField{
					{Name: "name", Type: "string", Required: true},
				},
			},
			wantValid: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Validate(tt.input, tt.schema)
			if result.Valid != tt.wantValid {
				t.Errorf("Validate() Valid = %v, want %v, errors = %v", result.Valid, tt.wantValid, result.Errors)
			}
		})
	}
}

// TestExtractKeys tests key extraction
func TestExtractKeys(t *testing.T) {
	tests := []struct {
		name     string
		input    interface{}
		wantKeys []string
		wantErr  bool
	}{
		{
			name:     "simple object",
			input:    `{"name": "John", "age": 30}`,
			wantKeys: []string{"age", "name"},
			wantErr:  false,
		},
		{
			name:     "nested object",
			input:    `{"user": {"name": "John", "address": {"city": "NYC"}}}`,
			wantKeys: []string{"address", "city", "name", "user"},
			wantErr:  false,
		},
		{
			name:     "with array",
			input:    `{"items": [{"id": 1}, {"id": 2}]}`,
			wantKeys: []string{"id", "items"},
			wantErr:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			keys, err := ExtractKeys(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("ExtractKeys() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(keys) != len(tt.wantKeys) {
					t.Errorf("ExtractKeys() got %d keys, want %d", len(keys), len(tt.wantKeys))
				}
			}
		})
	}
}

// TestCountValues tests value counting
func TestCountValues(t *testing.T) {
	tests := []struct {
		name   string
		input  string
		path   string
		expect map[string]int
	}{
		{
			name:   "count in array",
			input:  `{"items": ["a", "b", "a", "c", "a"]}`,
			path:   "items",
			expect: map[string]int{"a": 3, "b": 1, "c": 1},
		},
		{
			name:   "count nested",
			input:  `{"data": [{"type": "x"}, {"type": "y"}, {"type": "x"}]}`,
			path:   "data.type",
			expect: map[string]int{"x": 2, "y": 1},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			counts, err := CountValues(tt.input, tt.path)
			if err != nil {
				t.Errorf("CountValues() error = %v", err)
				return
			}
			for k, v := range tt.expect {
				if counts[k] != v {
					t.Errorf("CountValues() count[%s] = %d, want %d", k, counts[k], v)
				}
			}
		})
	}
}

// TestTransform tests value transformation
func TestTransform(t *testing.T) {
	tests := []struct {
		name   string
		input  string
		expect string
	}{
		{
			name:   "uppercase",
			input:  `{"name": "john", "city": "new york"}`,
			expect: `"NAME":"JOHN"`,
		},
		{
			name:   "with numbers",
			input:  `{"name": "john", "age": 30}`,
			expect: `"NAME":"JOHN"`,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Transform(tt.input, strings.ToUpper)
			if err != nil {
				t.Errorf("Transform() error = %v", err)
				return
			}
			if !strings.Contains(result, tt.expect) {
				t.Errorf("Transform() result = %v, should contain %v", result, tt.expect)
			}
		})
	}
}

// TestDiff tests JSON diff
func TestDiff(t *testing.T) {
	tests := []struct {
		name   string
		json1  string
		json2  string
		check  string
		expect bool
	}{
		{
			name:   "added field",
			json1:  `{"a": 1}`,
			json2:  `{"a": 1, "b": 2}`,
			check:  "added",
			expect: true,
		},
		{
			name:   "removed field",
			json1:  `{"a": 1, "b": 2}`,
			json2:  `{"a": 1}`,
			check:  "removed",
			expect: true,
		},
		{
			name:   "changed field",
			json1:  `{"a": 1}`,
			json2:  `{"a": 2}`,
			check:  "changed",
			expect: true,
		},
		{
			name:   "identical",
			json1:  `{"a": 1}`,
			json2:  `{"a": 1}`,
			check:  "added",
			expect: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			diff, err := Diff(tt.json1, tt.json2)
			if err != nil {
				t.Errorf("Diff() error = %v", err)
				return
			}
			checkMap, ok := diff[tt.check].(map[string]interface{})
			if !ok {
				t.Errorf("Diff() %s is not a map", tt.check)
				return
			}
			hasChanges := len(checkMap) > 0
			if hasChanges != tt.expect {
				t.Errorf("Diff() %s has changes = %v, want %v", tt.check, hasChanges, tt.expect)
			}
		})
	}
}

// TestReadFileWriteFile tests file operations
func TestReadFileWriteFile(t *testing.T) {
	filename := "/tmp/test_json_utils.json"
	defer os.Remove(filename)

	testData := map[string]interface{}{
		"name":  "Test",
		"value": 42,
	}

	// Write
	err := WriteFile(filename, testData, "  ")
	if err != nil {
		t.Fatalf("WriteFile() error = %v", err)
	}

	// Read
	data, err := ReadFile(filename)
	if err != nil {
		t.Fatalf("ReadFile() error = %v", err)
	}

	// Verify
	m, ok := data.(map[string]interface{})
	if !ok {
		t.Fatal("ReadFile() data is not a map")
	}
	if m["name"] != "Test" || m["value"] != float64(42) {
		t.Error("ReadFile() data mismatch")
	}
}

// TestBuffer tests JSON buffer building
func TestBuffer(t *testing.T) {
	buf := NewBuffer()
	result := buf.StartObject().
		Key("name").AddString("John").
		Key("age").Number(30).
		Key("active").Bool(true).
		Key("data").Null().
		EndObject().
		String()

	if !strings.Contains(result, `"name":"John"`) {
		t.Error("Buffer missing name")
	}
	if !strings.Contains(result, `"age":30`) {
		t.Error("Buffer missing age")
	}
	if !strings.Contains(result, `"active":true`) {
		t.Error("Buffer missing active")
	}
	if !strings.Contains(result, `"data":null`) {
		t.Error("Buffer missing data")
	}
}

// TestArrayBuilder tests array building
func TestArrayBuilder(t *testing.T) {
	ab := NewArrayBuilder()
	result := ab.
		Add("first").
		Add(42).
		Add(true).
		Add(map[string]interface{}{"key": "value"}).
		String()

	expected := `["first",42,true,{"key":"value"}]`
	if result != expected {
		t.Errorf("ArrayBuilder() result = %v, want %v", result, expected)
	}
}

// TestToMapFromMap tests conversion functions
func TestToMapFromMap(t *testing.T) {
	type Person struct {
		Name string `json:"name"`
		Age  int    `json:"age"`
	}

	person := Person{Name: "John", Age: 30}

	// ToMap
	m, err := ToMap(person)
	if err != nil {
		t.Fatalf("ToMap() error = %v", err)
	}
	if m["name"] != "John" || m["age"] != float64(30) {
		t.Error("ToMap() conversion failed")
	}

	// FromMap
	var p2 Person
	err = FromMap(m, &p2)
	if err != nil {
		t.Fatalf("FromMap() error = %v", err)
	}
	if p2.Name != "John" || p2.Age != 30 {
		t.Error("FromMap() conversion failed")
	}
}

// Helper function to parse JSON
func parseJSON(s string, v interface{}) error {
	return json.Unmarshal([]byte(s), v)
}

// BenchmarkPrettyPrint benchmarks pretty printing
func BenchmarkPrettyPrint(b *testing.B) {
	json := `{"name":"John","age":30,"address":{"city":"NYC","zip":"10001"}}`
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = PrettyPrint(json, "  ")
	}
}

// BenchmarkMinify benchmarks minification
func BenchmarkMinify(b *testing.B) {
	json := `{ "name": "John", "age": 30, "address": { "city": "NYC" } }`
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = Minify(json)
	}
}

// BenchmarkGet benchmarks path retrieval
func BenchmarkGet(b *testing.B) {
	json := `{"user": {"name": "John", "address": {"city": "NYC"}}}`
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = Get(json, "user.address.city")
	}
}

// BenchmarkMerge benchmarks merging
func BenchmarkMerge(b *testing.B) {
	json1 := `{"a": 1, "b": 2, "c": 3}`
	json2 := `{"d": 4, "e": 5, "f": 6}`
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = Merge(json1, json2)
	}
}
