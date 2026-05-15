// Package text_template_utils provides a simple, zero-dependency text templating system.
// It supports variable substitution, conditionals, loops, and custom functions.
package text_template_utils

import (
	"bytes"
	"fmt"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"text/template"
)

// TemplateEngine wraps Go's text/template with additional utilities
type TemplateEngine struct {
	funcMap    template.FuncMap
	cache      map[string]*template.Template
	cacheMutex sync.RWMutex
	useCache   bool
}

// NewTemplateEngine creates a new template engine with default functions
func NewTemplateEngine() *TemplateEngine {
	engine := &TemplateEngine{
		funcMap:  make(template.FuncMap),
		cache:    make(map[string]*template.Template),
		useCache: true,
	}

	// Register default functions
	engine.RegisterDefaultFunctions()

	return engine
}

// RegisterDefaultFunctions adds built-in template functions
func (e *TemplateEngine) RegisterDefaultFunctions() {
	// String functions
	e.AddFunc("upper", strings.ToUpper)
	e.AddFunc("lower", strings.ToLower)
	e.AddFunc("title", strings.Title)
	e.AddFunc("trim", strings.TrimSpace)
	e.AddFunc("trimPrefix", strings.TrimPrefix)
	e.AddFunc("trimSuffix", strings.TrimSuffix)
	e.AddFunc("repeat", strings.Repeat)
	e.AddFunc("replace", strings.Replace)
	e.AddFunc("replaceAll", strings.ReplaceAll)
	e.AddFunc("split", strings.Split)
	e.AddFunc("join", strings.Join)
	e.AddFunc("hasPrefix", strings.HasPrefix)
	e.AddFunc("hasSuffix", strings.HasSuffix)
	e.AddFunc("contains", strings.Contains)

	// String manipulation
	e.AddFunc("substr", func(s string, start, end int) string {
		if start < 0 {
			start = 0
		}
		if end > len(s) {
			end = len(s)
		}
		if start >= end {
			return ""
		}
		return s[start:end]
	})

	e.AddFunc("truncate", func(s string, maxLen int, suffix ...string) string {
		suf := "..."
		if len(suffix) > 0 {
			suf = suffix[0]
		}
		if len(s) <= maxLen {
			return s
		}
		return s[:maxLen] + suf
	})

	// Numeric functions
	e.AddFunc("add", func(a, b int) int { return a + b })
	e.AddFunc("sub", func(a, b int) int { return a - b })
	e.AddFunc("mul", func(a, b int) int { return a * b })
	e.AddFunc("div", func(a, b int) int { return a / b })
	e.AddFunc("mod", func(a, b int) int { return a % b })
	e.AddFunc("min", func(a, b int) int {
		if a < b {
			return a
		}
		return b
	})
	e.AddFunc("max", func(a, b int) int {
		if a > b {
			return a
		}
		return b
	})

	// Type conversion
	e.AddFunc("toString", func(v interface{}) string { return fmt.Sprintf("%v", v) })
	e.AddFunc("toInt", func(s string) int {
		i, _ := strconv.Atoi(s)
		return i
	})
	e.AddFunc("toFloat", func(s string) float64 {
		f, _ := strconv.ParseFloat(s, 64)
		return f
	})

	// Boolean functions
	e.AddFunc("not", func(b bool) bool { return !b })
	e.AddFunc("and", func(a, b bool) bool { return a && b })
	e.AddFunc("or", func(a, b bool) bool { return a || b })

	// Default values
	e.AddFunc("default", func(defaultVal, actualVal interface{}) interface{} {
		if actualVal == nil || actualVal == "" || actualVal == 0 {
			return defaultVal
		}
		return actualVal
	})
	e.AddFunc("empty", func(v interface{}) bool {
		if v == nil {
			return true
		}
		switch val := v.(type) {
		case string:
			return val == ""
		case []interface{}:
			return len(val) == 0
		case map[string]interface{}:
			return len(val) == 0
		}
		return false
	})

	// List/array functions
	e.AddFunc("first", func(v []interface{}) interface{} {
		if len(v) == 0 {
			return nil
		}
		return v[0]
	})
	e.AddFunc("last", func(v []interface{}) interface{} {
		if len(v) == 0 {
			return nil
		}
		return v[len(v)-1]
	})
	e.AddFunc("slice", func(v []interface{}, start, end int) []interface{} {
		if start < 0 {
			start = 0
		}
		if end > len(v) {
			end = len(v)
		}
		if start >= end {
			return []interface{}{}
		}
		return v[start:end]
	})
	e.AddFunc("reverse", func(v []interface{}) []interface{} {
		result := make([]interface{}, len(v))
		for i, val := range v {
			result[len(v)-1-i] = val
		}
		return result
	})
	e.AddFunc("length", func(v interface{}) int {
		switch val := v.(type) {
		case string:
			return len(val)
		case []interface{}:
			return len(val)
		case map[string]interface{}:
			return len(val)
		}
		return 0
	})

	// Map functions
	e.AddFunc("keys", func(m map[string]interface{}) []string {
		keys := make([]string, 0, len(m))
		for k := range m {
			keys = append(keys, k)
		}
		return keys
	})
	e.AddFunc("values", func(m map[string]interface{}) []interface{} {
		values := make([]interface{}, 0, len(m))
		for _, v := range m {
			values = append(values, v)
		}
		return values
	})
	e.AddFunc("get", func(m map[string]interface{}, key string) interface{} {
		return m[key]
	})
	e.AddFunc("hasKey", func(m map[string]interface{}, key string) bool {
		_, ok := m[key]
		return ok
	})

	// Regex functions
	e.AddFunc("match", func(pattern, s string) bool {
		matched, _ := regexp.MatchString(pattern, s)
		return matched
	})
	e.AddFunc("findAll", func(pattern, s string) []string {
		re, err := regexp.Compile(pattern)
		if err != nil {
			return []string{}
		}
		return re.FindAllString(s, -1)
	})

	// Formatting functions
	e.AddFunc("indent", func(spaces int, s string) string {
		pad := strings.Repeat(" ", spaces)
		return pad + strings.ReplaceAll(s, "\n", "\n"+pad)
	})
	e.AddFunc("nindent", func(spaces int, s string) string {
		pad := strings.Repeat(" ", spaces)
		return "\n" + pad + strings.ReplaceAll(s, "\n", "\n"+pad)
	})
}

// AddFunc registers a custom template function
func (e *TemplateEngine) AddFunc(name string, fn interface{}) {
	e.funcMap[name] = fn
}

// SetCache enables or disables template caching
func (e *TemplateEngine) SetCache(enabled bool) {
	e.useCache = enabled
}

// ClearCache clears the template cache
func (e *TemplateEngine) ClearCache() {
	e.cacheMutex.Lock()
	defer e.cacheMutex.Unlock()
	e.cache = make(map[string]*template.Template)
}

// Render executes a template string with the given data
func (e *TemplateEngine) Render(tpl string, data interface{}) (string, error) {
	// Check cache first
	if e.useCache {
		e.cacheMutex.RLock()
		if cached, ok := e.cache[tpl]; ok {
			e.cacheMutex.RUnlock()
			var buf bytes.Buffer
			err := cached.Execute(&buf, data)
			return buf.String(), err
		}
		e.cacheMutex.RUnlock()
	}

	// Parse template
	t, err := template.New("").Funcs(e.funcMap).Parse(tpl)
	if err != nil {
		return "", fmt.Errorf("template parse error: %w", err)
	}

	// Cache the template
	if e.useCache {
		e.cacheMutex.Lock()
		e.cache[tpl] = t
		e.cacheMutex.Unlock()
	}

	// Execute template
	var buf bytes.Buffer
	if err := t.Execute(&buf, data); err != nil {
		return "", fmt.Errorf("template execute error: %w", err)
	}

	return buf.String(), nil
}

// RenderWithDelims renders a template with custom delimiters
func (e *TemplateEngine) RenderWithDelims(tpl string, leftDelim, rightDelim string, data interface{}) (string, error) {
	t, err := template.New("").Delims(leftDelim, rightDelim).Funcs(e.funcMap).Parse(tpl)
	if err != nil {
		return "", fmt.Errorf("template parse error: %w", err)
	}

	var buf bytes.Buffer
	if err := t.Execute(&buf, data); err != nil {
		return "", fmt.Errorf("template execute error: %w", err)
	}

	return buf.String(), nil
}

// RenderFile renders a template file with the given data
func (e *TemplateEngine) RenderFile(name, content string, data interface{}) (string, error) {
	t, err := template.New(name).Funcs(e.funcMap).Parse(content)
	if err != nil {
		return "", fmt.Errorf("template parse error: %w", err)
	}

	var buf bytes.Buffer
	if err := t.Execute(&buf, data); err != nil {
		return "", fmt.Errorf("template execute error: %w", err)
	}

	return buf.String(), nil
}

// Validate checks if a template string is valid
func (e *TemplateEngine) Validate(tpl string) error {
	_, err := template.New("").Funcs(e.funcMap).Parse(tpl)
	return err
}

// SimpleTemplate provides a simplified key-value template substitution
type SimpleTemplate struct {
	delimiters [2]string
	escapeChar string
}

// NewSimpleTemplate creates a new simple template with default delimiters {{ and }}
func NewSimpleTemplate() *SimpleTemplate {
	return &SimpleTemplate{
		delimiters: [2]string{"{{", "}}"},
		escapeChar: "\\",
	}
}

// SetDelimiters sets custom delimiters for the simple template
func (s *SimpleTemplate) SetDelimiters(left, right string) {
	s.delimiters = [2]string{left, right}
}

// SetEscapeChar sets the escape character
func (s *SimpleTemplate) SetEscapeChar(char string) {
	s.escapeChar = char
}

// Replace performs simple key-value substitution
func (s *SimpleTemplate) Replace(tpl string, vars map[string]string) string {
	result := tpl
	for key, value := range vars {
		placeholder := s.delimiters[0] + key + s.delimiters[1]
		result = strings.ReplaceAll(result, placeholder, value)
	}
	return result
}

// ReplaceWithFunc performs substitution with a custom function for missing keys
func (s *SimpleTemplate) ReplaceWithFunc(tpl string, vars map[string]string, missingFunc func(string) string) string {
	// First replace known variables
	result := tpl
	for key, value := range vars {
		placeholder := s.delimiters[0] + key + s.delimiters[1]
		result = strings.ReplaceAll(result, placeholder, value)
	}

	// Handle missing variables
	if missingFunc != nil {
		re := regexp.MustCompile(regexp.QuoteMeta(s.delimiters[0]) + `([^` + regexp.QuoteMeta(s.delimiters[1]) + `]+)` + regexp.QuoteMeta(s.delimiters[1]))
		result = re.ReplaceAllStringFunc(result, func(match string) string {
			// Extract key
			key := strings.TrimPrefix(match, s.delimiters[0])
			key = strings.TrimSuffix(key, s.delimiters[1])
			key = strings.TrimSpace(key)
			return missingFunc(key)
		})
	}

	return result
}

// ExtractVariables extracts all variable names from a template
func (s *SimpleTemplate) ExtractVariables(tpl string) []string {
	re := regexp.MustCompile(regexp.QuoteMeta(s.delimiters[0]) + `([^` + regexp.QuoteMeta(s.delimiters[1]) + `]+)` + regexp.QuoteMeta(s.delimiters[1]))
	matches := re.FindAllString(tpl, -1)

	vars := make([]string, 0, len(matches))
	seen := make(map[string]bool)

	for _, match := range matches {
		key := strings.TrimPrefix(match, s.delimiters[0])
		key = strings.TrimSuffix(key, s.delimiters[1])
		key = strings.TrimSpace(key)
		if !seen[key] {
			seen[key] = true
			vars = append(vars, key)
		}
	}

	return vars
}

// TemplateBuilder helps build templates programmatically
type TemplateBuilder struct {
	strings.Builder
	indentLevel int
	indentStr   string
}

// NewTemplateBuilder creates a new template builder
func NewTemplateBuilder() *TemplateBuilder {
	return &TemplateBuilder{
		indentStr: "  ", // 2 spaces default
	}
}

// SetIndent sets the indentation string
func (b *TemplateBuilder) SetIndent(s string) *TemplateBuilder {
	b.indentStr = s
	return b
}

// Write writes a string to the template
func (b *TemplateBuilder) Write(s string) *TemplateBuilder {
	b.Builder.WriteString(s)
	return b
}

// WriteLine writes a string followed by a newline
func (b *TemplateBuilder) WriteLine(s string) *TemplateBuilder {
	b.Builder.WriteString(s + "\n")
	return b
}

// WriteIndented writes an indented string
func (b *TemplateBuilder) WriteIndented(s string) *TemplateBuilder {
	b.Builder.WriteString(strings.Repeat(b.indentStr, b.indentLevel) + s)
	return b
}

// WriteIndentedLine writes an indented string followed by a newline
func (b *TemplateBuilder) WriteIndentedLine(s string) *TemplateBuilder {
	b.Builder.WriteString(strings.Repeat(b.indentStr, b.indentLevel) + s + "\n")
	return b
}

// Indent increases the indentation level
func (b *TemplateBuilder) Indent() *TemplateBuilder {
	b.indentLevel++
	return b
}

// Dedent decreases the indentation level
func (b *TemplateBuilder) Dedent() *TemplateBuilder {
	if b.indentLevel > 0 {
		b.indentLevel--
	}
	return b
}

// Variable writes a variable placeholder
func (b *TemplateBuilder) Variable(name string) *TemplateBuilder {
	b.Builder.WriteString("{{." + name + "}}")
	return b
}

// IfBlock writes an if block
func (b *TemplateBuilder) IfBlock(condition string, content func(*TemplateBuilder)) *TemplateBuilder {
	b.WriteIndented("{{if ." + condition + "}}\n")
	b.Indent()
	if content != nil {
		content(b)
	}
	b.Dedent()
	b.WriteIndented("{{end}}\n")
	return b
}

// IfElseBlock writes an if-else block
func (b *TemplateBuilder) IfElseBlock(condition string, ifContent func(*TemplateBuilder), elseContent func(*TemplateBuilder)) *TemplateBuilder {
	b.WriteIndented("{{if ." + condition + "}}\n")
	b.Indent()
	if ifContent != nil {
		ifContent(b)
	}
	b.Dedent()
	b.WriteIndented("{{else}}\n")
	b.Indent()
	if elseContent != nil {
		elseContent(b)
	}
	b.Dedent()
	b.WriteIndented("{{end}}\n")
	return b
}

// RangeBlock writes a range block for iteration
func (b *TemplateBuilder) RangeBlock(collection string, itemVar string, content func(*TemplateBuilder)) *TemplateBuilder {
	b.WriteIndented("{{range $" + itemVar + " := ." + collection + "}}\n")
	b.Indent()
	if content != nil {
		content(b)
	}
	b.Dedent()
	b.WriteIndented("{{end}}\n")
	return b
}

// WithBlock writes a with block for scoping
func (b *TemplateBuilder) WithBlock(scope string, content func(*TemplateBuilder)) *TemplateBuilder {
	b.WriteIndented("{{with ." + scope + "}}\n")
	b.Indent()
	if content != nil {
		content(b)
	}
	b.Dedent()
	b.WriteIndented("{{end}}\n")
	return b
}

// FuncCall writes a function call
func (b *TemplateBuilder) FuncCall(funcName string, args ...string) *TemplateBuilder {
	argStr := ""
	if len(args) > 0 {
		argStr = " " + strings.Join(args, " ")
	}
	b.Builder.WriteString("{{" + funcName + argStr + "}}")
	return b
}

// Build returns the built template string
func (b *TemplateBuilder) Build() string {
	return b.Builder.String()
}

// Reset resets the builder
func (b *TemplateBuilder) Reset() *TemplateBuilder {
	b.Builder.Reset()
	b.indentLevel = 0
	return b
}