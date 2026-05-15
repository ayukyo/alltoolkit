package text_template_utils

import (
	"strings"
	"testing"
)

func TestNewTemplateEngine(t *testing.T) {
	engine := NewTemplateEngine()
	if engine == nil {
		t.Fatal("Expected non-nil template engine")
	}
	if len(engine.funcMap) == 0 {
		t.Error("Expected default functions to be registered")
	}
}

func TestTemplateEngine_Render_BasicVariable(t *testing.T) {
	engine := NewTemplateEngine()

	result, err := engine.Render("Hello, {{.Name}}!", map[string]interface{}{"Name": "World"})
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != "Hello, World!" {
		t.Errorf("Expected 'Hello, World!', got '%s'", result)
	}
}

func TestTemplateEngine_Render_NestedVariables(t *testing.T) {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"User": map[string]interface{}{
			"Name": "Alice",
			"Age":  30,
		},
	}

	result, err := engine.Render("User: {{.User.Name}}, Age: {{.User.Age}}", data)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != "User: Alice, Age: 30" {
		t.Errorf("Expected 'User: Alice, Age: 30', got '%s'", result)
	}
}

func TestTemplateEngine_Render_Conditionals(t *testing.T) {
	engine := NewTemplateEngine()

	tests := []struct {
		name     string
		template string
		data     map[string]interface{}
		expected string
	}{
		{
			name:     "if true",
			template: "{{if .Show}}visible{{end}}",
			data:     map[string]interface{}{"Show": true},
			expected: "visible",
		},
		{
			name:     "if false",
			template: "{{if .Show}}visible{{end}}",
			data:     map[string]interface{}{"Show": false},
			expected: "",
		},
		{
			name:     "if-else true",
			template: "{{if .Show}}yes{{else}}no{{end}}",
			data:     map[string]interface{}{"Show": true},
			expected: "yes",
		},
		{
			name:     "if-else false",
			template: "{{if .Show}}yes{{else}}no{{end}}",
			data:     map[string]interface{}{"Show": false},
			expected: "no",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := engine.Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("Unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("Expected '%s', got '%s'", tt.expected, result)
			}
		})
	}
}

func TestTemplateEngine_Render_Loops(t *testing.T) {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Items": []interface{}{"a", "b", "c"},
	}

	result, err := engine.Render("{{range .Items}}{{.}},{{end}}", data)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != "a,b,c," {
		t.Errorf("Expected 'a,b,c,', got '%s'", result)
	}
}

func TestTemplateEngine_StringFunctions(t *testing.T) {
	engine := NewTemplateEngine()

	tests := []struct {
		name     string
		template string
		data     map[string]interface{}
		expected string
	}{
		{
			name:     "upper",
			template: "{{upper .Text}}",
			data:     map[string]interface{}{"Text": "hello"},
			expected: "HELLO",
		},
		{
			name:     "lower",
			template: "{{lower .Text}}",
			data:     map[string]interface{}{"Text": "HELLO"},
			expected: "hello",
		},
		{
			name:     "trim",
			template: "{{trim .Text}}",
			data:     map[string]interface{}{"Text": "  hello  "},
			expected: "hello",
		},
		{
			name:     "replace",
			template: `{{replace .Text "o" "0" -1}}`,
			data:     map[string]interface{}{"Text": "hello"},
			expected: "hell0",
		},
		{
			name:     "split and join",
			template: `{{join (split .Text ",") "-"}}`,
			data:     map[string]interface{}{"Text": "a,b,c"},
			expected: "a-b-c",
		},
		{
			name:     "contains",
			template: "{{if contains .Text \"ell\"}}yes{{else}}no{{end}}",
			data:     map[string]interface{}{"Text": "hello"},
			expected: "yes",
		},
		{
			name:     "hasPrefix",
			template: "{{if hasPrefix .Text \"hel\"}}yes{{else}}no{{end}}",
			data:     map[string]interface{}{"Text": "hello"},
			expected: "yes",
		},
		{
			name:     "hasSuffix",
			template: "{{if hasSuffix .Text \"lo\"}}yes{{else}}no{{end}}",
			data:     map[string]interface{}{"Text": "hello"},
			expected: "yes",
		},
		{
			name:     "truncate",
			template: "{{truncate .Text 5}}",
			data:     map[string]interface{}{"Text": "hello world"},
			expected: "hello...",
		},
		{
			name:     "substr",
			template: "{{substr .Text 0 5}}",
			data:     map[string]interface{}{"Text": "hello world"},
			expected: "hello",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := engine.Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("Unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("Expected '%s', got '%s'", tt.expected, result)
			}
		})
	}
}

func TestTemplateEngine_NumericFunctions(t *testing.T) {
	engine := NewTemplateEngine()

	tests := []struct {
		name     string
		template string
		data     map[string]interface{}
		expected string
	}{
		{
			name:     "add",
			template: "{{add .A .B}}",
			data:     map[string]interface{}{"A": 5, "B": 3},
			expected: "8",
		},
		{
			name:     "sub",
			template: "{{sub .A .B}}",
			data:     map[string]interface{}{"A": 5, "B": 3},
			expected: "2",
		},
		{
			name:     "mul",
			template: "{{mul .A .B}}",
			data:     map[string]interface{}{"A": 5, "B": 3},
			expected: "15",
		},
		{
			name:     "div",
			template: "{{div .A .B}}",
			data:     map[string]interface{}{"A": 15, "B": 3},
			expected: "5",
		},
		{
			name:     "mod",
			template: "{{mod .A .B}}",
			data:     map[string]interface{}{"A": 7, "B": 3},
			expected: "1",
		},
		{
			name:     "min",
			template: "{{min .A .B}}",
			data:     map[string]interface{}{"A": 5, "B": 3},
			expected: "3",
		},
		{
			name:     "max",
			template: "{{max .A .B}}",
			data:     map[string]interface{}{"A": 5, "B": 3},
			expected: "5",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := engine.Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("Unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("Expected '%s', got '%s'", tt.expected, result)
			}
		})
	}
}

func TestTemplateEngine_DefaultFunction(t *testing.T) {
	engine := NewTemplateEngine()

	tests := []struct {
		name     string
		template string
		data     map[string]interface{}
		expected string
	}{
		{
			name:     "default with value",
			template: "{{default \"N/A\" .Name}}",
			data:     map[string]interface{}{"Name": "Alice"},
			expected: "Alice",
		},
		{
			name:     "default with empty",
			template: "{{default \"N/A\" .Name}}",
			data:     map[string]interface{}{"Name": ""},
			expected: "N/A",
		},
		{
			name:     "default with nil",
			template: "{{default \"N/A\" .Name}}",
			data:     map[string]interface{}{},
			expected: "N/A",
		},
		{
			name:     "empty check true",
			template: "{{if empty .Name}}empty{{else}}not empty{{end}}",
			data:     map[string]interface{}{"Name": ""},
			expected: "empty",
		},
		{
			name:     "empty check false",
			template: "{{if empty .Name}}empty{{else}}not empty{{end}}",
			data:     map[string]interface{}{"Name": "Alice"},
			expected: "not empty",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := engine.Render(tt.template, tt.data)
			if err != nil {
				t.Fatalf("Unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("Expected '%s', got '%s'", tt.expected, result)
			}
		})
	}
}

func TestTemplateEngine_ListFunctions(t *testing.T) {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Items": []interface{}{"a", "b", "c", "d"},
	}

	tests := []struct {
		name     string
		template string
		expected string
	}{
		{
			name:     "first",
			template: "{{first .Items}}",
			expected: "a",
		},
		{
			name:     "last",
			template: "{{last .Items}}",
			expected: "d",
		},
		{
			name:     "length",
			template: "{{length .Items}}",
			expected: "4",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := engine.Render(tt.template, data)
			if err != nil {
				t.Fatalf("Unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("Expected '%s', got '%s'", tt.expected, result)
			}
		})
	}
}

func TestTemplateEngine_MapFunctions(t *testing.T) {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Map": map[string]interface{}{
			"name": "Alice",
			"age":  30,
		},
	}

	t.Run("get", func(t *testing.T) {
		result, err := engine.Render("{{get .Map \"name\"}}", data)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "Alice" {
			t.Errorf("Expected 'Alice', got '%s'", result)
		}
	})

	t.Run("hasKey true", func(t *testing.T) {
		result, err := engine.Render("{{if hasKey .Map \"name\"}}yes{{else}}no{{end}}", data)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "yes" {
			t.Errorf("Expected 'yes', got '%s'", result)
		}
	})

	t.Run("hasKey false", func(t *testing.T) {
		result, err := engine.Render("{{if hasKey .Map \"unknown\"}}yes{{else}}no{{end}}", data)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "no" {
			t.Errorf("Expected 'no', got '%s'", result)
		}
	})
}

func TestTemplateEngine_RegexFunctions(t *testing.T) {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Text": "hello123world456",
	}

	t.Run("match true", func(t *testing.T) {
		result, err := engine.Render(`{{if match "\\d+" .Text}}yes{{else}}no{{end}}`, data)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "yes" {
			t.Errorf("Expected 'yes', got '%s'", result)
		}
	})

	t.Run("match false", func(t *testing.T) {
		result, err := engine.Render(`{{if match "xyz" .Text}}yes{{else}}no{{end}}`, data)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "no" {
			t.Errorf("Expected 'no', got '%s'", result)
		}
	})

	t.Run("findAll", func(t *testing.T) {
		result, err := engine.Render(`{{join (findAll "\\d+" .Text) ","}}`, data)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "123,456" {
			t.Errorf("Expected '123,456', got '%s'", result)
		}
	})
}

func TestTemplateEngine_FormattingFunctions(t *testing.T) {
	engine := NewTemplateEngine()

	t.Run("indent", func(t *testing.T) {
		result, err := engine.Render("{{indent 2 .Text}}", map[string]interface{}{"Text": "hello\nworld"})
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		expected := "  hello\n  world"
		if result != expected {
			t.Errorf("Expected '%s', got '%s'", expected, result)
		}
	})

	t.Run("toString", func(t *testing.T) {
		result, err := engine.Render("{{toString .Num}}", map[string]interface{}{"Num": 42})
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "42" {
			t.Errorf("Expected '42', got '%s'", result)
		}
	})

	t.Run("toInt", func(t *testing.T) {
		result, err := engine.Render("{{add (toInt .Str) 10}}", map[string]interface{}{"Str": "5"})
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if result != "15" {
			t.Errorf("Expected '15', got '%s'", result)
		}
	})
}

func TestTemplateEngine_AddFunc(t *testing.T) {
	engine := NewTemplateEngine()
	engine.AddFunc("double", func(n int) int { return n * 2 })

	result, err := engine.Render("{{double .Num}}", map[string]interface{}{"Num": 5})
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != "10" {
		t.Errorf("Expected '10', got '%s'", result)
	}
}

func TestTemplateEngine_RenderWithDelims(t *testing.T) {
	engine := NewTemplateEngine()

	// Custom delimiters: left="[=", right="=]"
	result, err := engine.RenderWithDelims("Hello, [= .Name =]!", "[=", "=]", map[string]interface{}{"Name": "World"})
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != "Hello, World!" {
		t.Errorf("Expected 'Hello, World!', got '%s'", result)
	}
}

func TestTemplateEngine_Validate(t *testing.T) {
	engine := NewTemplateEngine()

	// Valid template
	if err := engine.Validate("Hello, {{.Name}}!"); err != nil {
		t.Errorf("Expected valid template, got error: %v", err)
	}

	// Invalid template
	if err := engine.Validate("Hello, {{.Name!"); err == nil {
		t.Error("Expected error for invalid template")
	}
}

func TestTemplateEngine_Cache(t *testing.T) {
	engine := NewTemplateEngine()
	engine.SetCache(true)

	// First render should parse
	_, err := engine.Render("Hello, {{.Name}}!", map[string]interface{}{"Name": "World"})
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	// Second render should use cache
	result, err := engine.Render("Hello, {{.Name}}!", map[string]interface{}{"Name": "Alice"})
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != "Hello, Alice!" {
		t.Errorf("Expected 'Hello, Alice!', got '%s'", result)
	}

	// Clear cache
	engine.ClearCache()
	if len(engine.cache) != 0 {
		t.Error("Expected cache to be cleared")
	}
}

// SimpleTemplate tests

func TestSimpleTemplate_Replace(t *testing.T) {
	st := NewSimpleTemplate()

	result := st.Replace("Hello, {{name}}! Welcome to {{place}}.", map[string]string{
		"name":  "Alice",
		"place": "Wonderland",
	})

	if result != "Hello, Alice! Welcome to Wonderland." {
		t.Errorf("Expected 'Hello, Alice! Welcome to Wonderland.', got '%s'", result)
	}
}

func TestSimpleTemplate_ReplaceWithFunc(t *testing.T) {
	st := NewSimpleTemplate()

	result := st.ReplaceWithFunc("Hello, {{name}}! Your score is {{score}}.", map[string]string{
		"name": "Alice",
	}, func(key string) string {
		return "[" + key + "]"
	})

	if result != "Hello, Alice! Your score is [score]." {
		t.Errorf("Expected 'Hello, Alice! Your score is [score].', got '%s'", result)
	}
}

func TestSimpleTemplate_ExtractVariables(t *testing.T) {
	st := NewSimpleTemplate()

	vars := st.ExtractVariables("Hello, {{name}}! {{action}} the {{target}}. {{name}} is here.")

	if len(vars) != 3 {
		t.Errorf("Expected 3 variables, got %d", len(vars))
	}

	// Check that name appears only once (deduplicated)
	count := 0
	for _, v := range vars {
		if v == "name" {
			count++
		}
	}
	if count != 1 {
		t.Errorf("Expected name to appear once, got %d", count)
	}
}

func TestSimpleTemplate_CustomDelimiters(t *testing.T) {
	st := NewSimpleTemplate()
	st.SetDelimiters("<%", "%>")

	result := st.Replace("Hello, <%name%>!", map[string]string{"name": "World"})
	if result != "Hello, World!" {
		t.Errorf("Expected 'Hello, World!', got '%s'", result)
	}
}

// TemplateBuilder tests

func TestTemplateBuilder_Basic(t *testing.T) {
	b := NewTemplateBuilder()
	b.Write("Hello, ").Variable("Name").Write("!")

	if b.Build() != "Hello, {{.Name}}!" {
		t.Errorf("Expected 'Hello, {{.Name}}!', got '%s'", b.Build())
	}
}

func TestTemplateBuilder_IfBlock(t *testing.T) {
	b := NewTemplateBuilder()
	b.IfBlock("Show", func(b *TemplateBuilder) {
		b.WriteIndentedLine("visible content")
	})

	result := b.Build()
	if !strings.Contains(result, "{{if .Show}}") {
		t.Error("Expected if block in result")
	}
	if !strings.Contains(result, "{{end}}") {
		t.Error("Expected end block in result")
	}
	if !strings.Contains(result, "visible content") {
		t.Error("Expected content in result")
	}
}

func TestTemplateBuilder_IfElseBlock(t *testing.T) {
	b := NewTemplateBuilder()
	b.IfElseBlock("Show",
		func(b *TemplateBuilder) {
			b.WriteIndentedLine("yes")
		},
		func(b *TemplateBuilder) {
			b.WriteIndentedLine("no")
		},
	)

	result := b.Build()
	if !strings.Contains(result, "{{if .Show}}") {
		t.Error("Expected if block in result")
	}
	if !strings.Contains(result, "{{else}}") {
		t.Error("Expected else block in result")
	}
	if !strings.Contains(result, "{{end}}") {
		t.Error("Expected end block in result")
	}
}

func TestTemplateBuilder_RangeBlock(t *testing.T) {
	b := NewTemplateBuilder()
	b.RangeBlock("Items", "item", func(b *TemplateBuilder) {
		b.WriteIndented("Item: ").Variable("item").WriteLine("")
	})

	result := b.Build()
	if !strings.Contains(result, "{{range $item := .Items}}") {
		t.Error("Expected range block in result")
	}
	if !strings.Contains(result, "{{end}}") {
		t.Error("Expected end block in result")
	}
}

func TestTemplateBuilder_FuncCall(t *testing.T) {
	b := NewTemplateBuilder()
	b.Write("Upper: ").FuncCall("upper", ".Text")

	if b.Build() != "Upper: {{upper .Text}}" {
		t.Errorf("Expected 'Upper: {{upper .Text}}', got '%s'", b.Build())
	}
}

func TestTemplateBuilder_Indent(t *testing.T) {
	b := NewTemplateBuilder()
	b.SetIndent("  ")
	b.WriteIndentedLine("line1").Indent().WriteIndentedLine("line2").Dedent().WriteIndentedLine("line3")

	result := b.Build()
	lines := strings.Split(strings.TrimSpace(result), "\n")
	if len(lines) != 3 {
		t.Fatalf("Expected 3 lines, got %d", len(lines))
	}
	if lines[0] != "line1" {
		t.Errorf("Expected 'line1', got '%s'", lines[0])
	}
	if lines[1] != "  line2" {
		t.Errorf("Expected '  line2', got '%s'", lines[1])
	}
	if lines[2] != "line3" {
		t.Errorf("Expected 'line3', got '%s'", lines[2])
	}
}

func TestTemplateBuilder_Reset(t *testing.T) {
	b := NewTemplateBuilder()
	b.Write("some content").Indent().Indent()

	if b.indentLevel != 2 {
		t.Errorf("Expected indent level 2, got %d", b.indentLevel)
	}

	b.Reset()

	if b.Build() != "" {
		t.Error("Expected empty builder after reset")
	}
	if b.indentLevel != 0 {
		t.Errorf("Expected indent level 0 after reset, got %d", b.indentLevel)
	}
}

func TestTemplateBuilder_ComplexTemplate(t *testing.T) {
	b := NewTemplateBuilder()
	b.WriteIndentedLine("User Report:")
	b.Indent()
	b.WriteIndented("Name: ").Variable("User.Name").WriteLine("")
	b.WriteIndented("Age: ").Variable("User.Age").WriteLine("")
	b.IfBlock("User.Active", func(b *TemplateBuilder) {
		b.WriteIndentedLine("Status: Active")
	})
	b.RangeBlock("User.Skills", "skill", func(b *TemplateBuilder) {
		b.WriteIndented("- ").Variable("skill").WriteLine("")
	})
	b.Dedent()

	result := b.Build()
	if !strings.Contains(result, "User Report:") {
		t.Error("Expected header in result")
	}
	if !strings.Contains(result, "{{.User.Name}}") {
		t.Error("Expected User.Name variable in result")
	}
	if !strings.Contains(result, "{{range $skill := .User.Skills}}") {
		t.Error("Expected range block in result")
	}
}

// Benchmark tests

func BenchmarkTemplateEngine_Render(b *testing.B) {
	engine := NewTemplateEngine()
	data := map[string]interface{}{
		"Name": "Alice",
		"Age":  30,
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = engine.Render("Hello, {{.Name}}! Age: {{.Age}}", data)
	}
}

func BenchmarkTemplateEngine_Render_WithCache(b *testing.B) {
	engine := NewTemplateEngine()
	engine.SetCache(true)
	data := map[string]interface{}{
		"Name": "Alice",
		"Age":  30,
	}

	// Warm up cache
	_, _ = engine.Render("Hello, {{.Name}}! Age: {{.Age}}", data)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = engine.Render("Hello, {{.Name}}! Age: {{.Age}}", data)
	}
}

func BenchmarkSimpleTemplate_Replace(b *testing.B) {
	st := NewSimpleTemplate()
	vars := map[string]string{
		"name":   "Alice",
		"age":    "30",
		"city":   "Wonderland",
		"active": "true",
	}
	tpl := "Hello, {{name}}! Age: {{age}}, City: {{city}}, Active: {{active}}"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = st.Replace(tpl, vars)
	}
}