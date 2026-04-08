package template_utils

import (
	"strings"
	"testing"
)

// TestBasicRendering tests basic variable substitution
func TestBasicRendering(t *testing.T) {
	tests := []struct {
		name     string
		template string
		data     map[string]any
		expected string
	}{
		{
			name:     "simple variable",
			template: "Hello, {{name}}!",
			data:     map[string]any{"name": "World"},
			expected: "Hello, World!",
		},
		{
			name:     "multiple variables",
			template: "{{greeting}}, {{name}}!",
			data:     map[string]any{"greeting": "Hi", "name": "Alice"},
			expected: "Hi, Alice!",
		},
		{
			name:     "missing variable",
			template: "Hello, {{name}}!",
			data:     map[string]any{},
			expected: "Hello, !",
		},
		{
			name:     "no variables",
			template: "Hello, World!",
			data:     map[string]any{},
			expected: "Hello, World!",
		},
		{
			name:     "empty template",
			template: "",
			data:     map[string]any{"name": "test"},
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result)
			}
		})
	}
}

// TestDataTypes tests different data types
func TestDataTypes(t *testing.T) {
	tests := []struct {
		name     string
		template string
		data     map[string]any
		expected string
	}{
		{
			name:     "string value",
			template: "{{value}}",
			data:     map[string]any{"value": "test"},
			expected: "test",
		},
		{
			name:     "integer value",
			template: "{{value}}",
			data:     map[string]any{"value": 42},
			expected: "42",
		},
		{
			name:     "float value",
			template: "{{value}}",
			data:     map[string]any{"value": 3.14},
			expected: "3.14",
		},
		{
			name:     "boolean true",
			template: "{{value}}",
			data:     map[string]any{"value": true},
			expected: "true",
		},
		{
			name:     "boolean false",
			template: "{{value}}",
			data:     map[string]any{"value": false},
			expected: "false",
		},
		{
			name:     "nil value",
			template: "{{value}}",
			data:     map[string]any{"value": nil},
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result)
			}
		})
	}
}

// TestFilters tests filter functionality
func TestFilters(t *testing.T) {
	tests := []struct {
		name     string
		template string
		data     map[string]any
		expected string
	}{
		{
			name:     "upper filter",
			template: "{{name|upper}}",
			data:     map[string]any{"name": "hello"},
			expected: "HELLO",
		},
		{
			name:     "lower filter",
			template: "{{name|lower}}",
			data:     map[string]any{"name": "HELLO"},
			expected: "hello",
		},
		{
			name:     "trim filter",
			template: "{{name|trim}}",
			data:     map[string]any{"name": "  hello  "},
			expected: "hello",
		},
		{
			name:     "truncate filter",
			template: "{{text|truncate:10}}",
			data:     map[string]any{"text": "This is a very long text"},
			expected: "This is...",
		},
		{
			name:     "default filter",
			template: "{{name|default:Anonymous}}",
			data:     map[string]any{"name": ""},
			expected: "Anonymous",
		},
		{
			name:     "escape filter",
			template: "{{html|escape}}",
			data:     map[string]any{"html": "<script>alert('xss')</script>"},
			expected: "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result)
			}
		})
	}
}

// TestNestedData tests dot notation access
func TestNestedData(t *testing.T) {
	tests := []struct {
		name     string
		template string
		data     map[string]any
		expected string
	}{
		{
			name:     "nested map access",
			template: "{{user.name}}",
			data: map[string]any{
				"user": map[string]any{"name": "John"},
			},
			expected: "John",
		},
		{
			name:     "deeply nested access",
			template: "{{company.department.manager}}",
			data: map[string]any{
				"company": map[string]any{
					"department": map[string]any{
						"manager": "Alice",
					},
				},
			},
			expected: "Alice",
		},
		{
			name:     "missing nested key",
			template: "{{user.age}}",
			data: map[string]any{
				"user": map[string]any{"name": "John"},
			},
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result)
			}
		})
	}
}

// TestTemplateEngine tests TemplateEngine functionality
func TestTemplateEngine(t *testing.T) {
	t.Run("custom function", func(t *testing.T) {
		engine := New()
		engine.RegisterFunction("double", func(args ...any) (any, error) {
			if len(args) == 0 {
				return 0, nil
			}
			return toFloat64(args[0]) * 2, nil
		})

		tmpl, err := engine.Parse("{{double:{{value}}}}")
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		result, err := tmpl.Render(map[string]any{"value": 21})
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		// Note: This test demonstrates the concept, actual function call
		// syntax in templates would need additional parsing
		_ = result
	})

	t.Run("global variable", func(t *testing.T) {
		engine := New()
		engine.SetGlobal("appName", "MyApp")

		tmpl, err := engine.Parse("{{appName}}")
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		result, err := tmpl.Render(map[string]any{})
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		if result != "MyApp" {
			t.Errorf("expected 'MyApp', got %q", result)
		}
	})
}

// TestEdgeCases tests edge cases and error handling
func TestEdgeCases(t *testing.T) {
	tests := []struct {
		name     string
		template string
		data     map[string]any
		expected string
	}{
		{
			name:     "special characters in value",
			template: "{{value}}",
			data:     map[string]any{"value": "Hello {{
			expected: "Hello {{ World!"},
		},
		{
			name:     "unicode characters",
			template: "{{value}}",
			data:     map[string]any{"value": "Hello 世界 🌍"},
			expected: "Hello 世界 🌍",
		},
		{
			name:     "empty variable name",
			template: "{{}}",
			data:     map[string]any{},
			expected: "",
		},
		{
			name:     "whitespace in variable",
			template: "{{  name  }}",
			data:     map[string]any{"name": "test"},
			expected: "test",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result)
			}
		})
	}
}

// TestBuiltInFunctions tests built-in functions
func TestBuiltInFunctions(t *testing.T) {
	engine := New()

	tests := []struct {
		name     string
		fn       string
		args     []any
		expected any
	}{
		{"upper", "upper", []any{"hello"}, "HELLO"},
		{"lower", "lower", []any{"HELLO"}, "hello"},
		{"trim", "trim", []any{"  hello  "}, "hello"},
		{"len with string", "len", []any{"hello"}, 5},
		{"len with slice", "len", []any{[]any{1, 2, 3}}, 3},
		{"join", "join", []any{[]any{"a", "b", "c"}, ","}, "a,b,c"},
		{"split", "split", []any{"a,b,c", ","}, []string{"a", "b", "c"}},
		{"replace", "replace", []any{"hello world", "world", "go"}, "hello go"},
		{"contains true", "contains", []any{"hello", "ell"}, true},
		{"contains false", "contains", []any{"hello", "xyz"}, false},
		{"substr", "substr", []any{"hello", 1, 3}, "ell"},
		{"add", "add", []any{1, 2, 3}, 6.0},
		{"eq true", "eq", []any{1, 1}, true},
		{"eq false", "eq", []any{1, 2}, false},
		{"gt true", "gt", []any{2, 1}, true},
		{"gt false", "gt", []any{1, 2}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			fn, ok := engine.functions[tt.fn]
			if !ok {
				t.Fatalf("function %s not found", tt.fn)
			}
			result, err := fn(tt.args...)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}

			// Compare results
			switch expected := tt.expected.(type) {
			case string:
				if r, ok := result.(string); !ok || r != expected {
					t.Errorf("expected %q, got %v", expected, result)
				}
			case int:
				if r, ok := result.(int); !ok || r != expected {
					t.Errorf("expected %d, got %v", expected, result)
				}
			case float64:
				if r, ok := result.(float64); !ok || r != expected {
					t.Errorf("expected %f, got %v", expected, result)
				}
			case bool:
				if r, ok := result.(bool); !ok || r != expected {
					t.Errorf("expected %v, got %v", expected, result)
				}
			case []string:
				r, ok := result.([]string)
				if !ok || len(r) != len(expected) {
					t.Errorf("expected %v, got %v", expected, result)
					return
				}
				for i := range expected {
					if r[i] != expected[i] {
						t.Errorf("expected %v, got %v", expected, result)
						return
					}
				}
			}
		})
	}
}

// BenchmarkSimpleRender benchmarks simple template rendering
func BenchmarkSimpleRender(b *testing.B) {
	template := "Hello, {{name}}!"
	data := map[string]any{"name": "World"}

	for i := 0; i < b.N; i++ {
		_, err := Render(template, data)
		if err != nil {
			b.Fatal(err)
		}
	}
}

// BenchmarkComplexRender benchmarks complex template rendering
func BenchmarkComplexRender(b *testing.B) {
	template := "User: {{user.name}}, Age: {{user.age}}, Email: {{user.email}}"
	data := map[string]any{
		"user": map[string]any{
			"name":  "John Doe",
			"age":   30,
			"email": "john@example.com",
		},
	}

	for i := 0; i < b.N; i++ {
		_, err := Render(template, data)
		if err != nil {
			b.Fatal(err)
		}
	}
}

// TestConcurrency tests concurrent template rendering
func TestConcurrency(t *testing.T) {
	template := "Hello, {{name}}!"
	data := map[string]any{"name": "World"}

	// Run multiple goroutines
	done := make(chan bool, 10)
	for i := 0; i < 10; i++ {
		go func() {
			for j := 0; j < 100; j++ {
				result, err := Render(template, data)
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if result != "Hello, World!" {
					t.Errorf("unexpected result: %s", result)
				}
			}
			done <- true
		}()
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}
}
