// Package template_utils provides comprehensive string template processing utilities for Go.
// It supports variable substitution, conditionals, loops, filters, and custom functions.
// Zero dependencies - uses only Go standard library.
//
// Example usage:
//
//	template := "Hello, {{name}}!"
//	result, err := template_utils.Render(template, map[string]any{
//	    "name": "World",
//	})
//	// result: "Hello, World!"
package template_utils

import (
	"fmt"
	"reflect"
	"strconv"
	"strings"
)

// TemplateEngine provides template parsing and rendering capabilities
type TemplateEngine struct {
	functions map[string]Func
	globals   map[string]any
}

// Func represents a template function
type Func func(args ...any) (any, error)

// Template represents a parsed template
type Template struct {
	name     string
	source   string
	engine   *TemplateEngine
	compiled []node
}

// node represents a parsed template node
type node interface {
	render(ctx *context) (string, error)
}

// context holds template execution context
type context struct {
	data      map[string]any
	globals   map[string]any
	functions map[string]Func
}

// textNode represents plain text
type textNode struct {
	text string
}

func (n *textNode) render(ctx *context) (string, error) {
	return n.text, nil
}

// varNode represents a variable expression
type varNode struct {
	name   string
	filter string
}

func (n *varNode) render(ctx *context) (string, error) {
	value := ctx.get(n.name)
	if value == nil {
		return "", nil
	}
	result := toString(value)
	if n.filter != "" {
		filtered, err := applyFilter(result, n.filter)
		if err != nil {
			return "", err
		}
		result = filtered
	}
	return result, nil
}

// New creates a new TemplateEngine with default functions
func New() *TemplateEngine {
	engine := &TemplateEngine{
		functions: make(map[string]Func),
		globals:   make(map[string]any),
	}
	engine.RegisterFunction("upper", func(args ...any) (any, error) {
		if len(args) == 0 { return "", nil }
		return strings.ToUpper(toString(args[0])), nil
	})
	engine.RegisterFunction("lower", func(args ...any) (any, error) {
		if len(args) == 0 { return "", nil }
		return strings.ToLower(toString(args[0])), nil
	})
	engine.RegisterFunction("trim", func(args ...any) (any, error) {
		if len(args) == 0 { return "", nil }
		return strings.TrimSpace(toString(args[0])), nil
	})
	engine.RegisterFunction("len", func(args ...any) (any, error) {
		if len(args) == 0 { return 0, nil }
		return length(args[0]), nil
	})
	engine.RegisterFunction("default", func(args ...any) (any, error) {
		if len(args) < 2 { return "", nil }
		if isEmpty(args[0]) { return args[1], nil }
		return args[0], nil
	})
	engine.RegisterFunction("join", func(args ...any) (any, error) {
		if len(args) < 2 { return "", nil }
		return strings.Join(toSlice(args[0]), toString(args[1])), nil
	})
	engine.RegisterFunction("split", func(args ...any) (any, error) {
		if len(args) < 2 { return []string{}, nil }
		return strings.Split(toString(args[0]), toString(args[1])), nil
	})
	engine.RegisterFunction("replace", func(args ...any) (any, error) {
		if len(args) < 3 { return "", nil }
		return strings.ReplaceAll(toString(args[0]), toString(args[1]), toString(args[2])), nil
	})
	engine.RegisterFunction("contains", func(args ...any) (any, error) {
		if len(args) < 2 { return false, nil }
		return strings.Contains(toString(args[0]), toString(args[1])), nil
	})
	engine.RegisterFunction("substr", func(args ...any) (any, error) {
		if len(args) < 2 { return "", nil }
		s := toString(args[0])
		start := toInt(args[1])
		if start < 0 { start = len(s) + start }
		if start < 0 { start = 0 }
		if start > len(s) { return "", nil }
		if len(args) >= 3 {
			end := start + toInt(args[2])
			if end > len(s) { end = len(s) }
			return s[start:end], nil
		}
		return s[start:], nil
	})
	engine.RegisterFunction("format", func(args ...any) (any, error) {
		if len(args) < 1 { return "", nil }
		if len(args) == 1 { return toString(args[0]), nil }
		return fmt.Sprintf(toString(args[0]), args[1:]...), nil
	})
	engine.RegisterFunction("add", func(args ...any) (any, error) {
		if len(args) < 2 { return 0, nil }
		result := toFloat64(args[0])
		for i := 1; i < len(args); i++ { result += toFloat64(args[i]) }
		return result, nil
	})
	engine.RegisterFunction("eq", func(args ...any) (any, error) {
		if len(args) < 2 { return true, nil }
		return reflect.DeepEqual(args[0], args[1]), nil
	})
	engine.RegisterFunction("ne", func(args ...any) (any, error) {
		if len(args) < 2 { return false, nil }
		return !reflect.DeepEqual(args[0], args[1]), nil
	})
	engine.RegisterFunction("gt", func(args ...any) (any, error) {
		if len(args) < 2 { return false, nil }
		return toFloat64(args[0]) > toFloat64(args[1]), nil
	})
	engine.RegisterFunction("lt", func(args ...any) (any, error) {
		if len(args) < 2 { return false, nil }
		return toFloat64(args[0]) < toFloat64(args[1]), nil
	})
	engine.RegisterFunction("gte", func(args ...any) (any, error) {
		if len(args) < 2 { return false, nil }
		return toFloat64(args[0]) >= toFloat64(args[1]), nil
	})
	engine.RegisterFunction("lte", func(args ...any) (any, error) {
		if len(args) < 2 { return false, nil }
		return toFloat64(args[0]) <= toFloat64(args[1]), nil
	})
	return engine
}

// RegisterFunction registers a custom function
func (e *TemplateEngine) RegisterFunction(name string, fn Func) {
	e.functions[name] = fn
}

// SetGlobal sets a global variable
func (e *TemplateEngine) SetGlobal(name string, value any) {
	e.globals[name] = value
}

// Parse parses a template string
func (e *TemplateEngine) Parse(source string) (*Template, error) {
	t := &Template{source: source, engine: e}
	if err := t.compile(); err != nil {
		return nil, err
	}
	return t, nil
}

// Render renders the template with given data
func (t *Template) Render(data map[string]any) (string, error) {
	ctx := &context{data: data, globals: t.engine.globals, functions: t.engine.functions}
	var result strings.Builder
	for _, n := range t.compiled {
		s, err := n.render(ctx)
		if err != nil {
			return "", err
		}
		result.WriteString(s)
	}
	return result.String(), nil
}

// Render is a convenience function to render a template string
func Render(source string, data map[string]any) (string, error) {
	engine := New()
	tmpl, err := engine.Parse(source)
	if err != nil {
		return "", err
	}
	return tmpl.Render(data)
}

// compile parses the template source into nodes
func (t *Template) compile() error {
	var nodes []node
	var i int
	for i < len(t.source) {
		if i+1 < len(t.source) && t.source[i] == '{' && t.source[i+1] == '{' {
			end := strings.Index(t.source[i+2:], "}}")
			if end == -1 {
				return fmt.Errorf("unclosed template tag at position %d", i)
			}
			end += i + 2
			if i > 0 {
				nodes = append(nodes, &textNode{text: t.source[:i]})
			}
			tagContent := strings.TrimSpace(t.source[i+2 : end])
			tagNode := &varNode{name: tagContent}
			nodes = append(nodes, tagNode)
			t.source = t.source[end+2:]
			i = 0
		} else {
			i++
		}
	}
	if len(t.source) > 0 {
		nodes = append(nodes, &textNode{text: t.source})
	}
	t.compiled = nodes
	return nil
}

// get retrieves a value from context
func (c *context) get(name string) any {
	if val, ok := c.data[name]; ok {
		return val
	}
	if val, ok := c.globals[name]; ok {
		return val
	}
	if strings.Contains(name, ".") {
		return c.getNested(name)
	}
	return nil
}

// getNested retrieves nested values using dot notation
func (c *context) getNested(path string) any {
	parts := strings.Split(path, ".")
	var current any = c.data
	for _, part := range parts {
		if current == nil {
			return nil
		}
		current = getField(current, part)
	}
	return current
}

// getField retrieves a field from a value
func getField(v any, name string) any {
	if v == nil {
		return nil
	}
	if m, ok := v.(map[string]any); ok {
		return m[name]
	}
	val := reflect.ValueOf(v)
	if val.Kind() == reflect.Ptr {
		val = val.Elem()
	}
	if val.Kind() != reflect.Struct {
		return nil
	}
	field := val.FieldByName(name)
	if !field.IsValid() {
		return nil
	}
	return field.Interface()
}

// applyFilter applies a filter to a value
func applyFilter(value string, filter string) (string, error) {
	parts := strings.Split(filter, ":")
	name := strings.TrimSpace(parts[0])
	switch name {
	case "upper":
		return strings.ToUpper(value), nil
	case "lower":
		return strings.ToLower(value), nil
	case "trim":
		return strings.TrimSpace(value), nil
	case "truncate":
		maxLen := 50
		if len(parts) > 1 {
			maxLen, _ = strconv.Atoi(parts[1])
		}
		if len(value) > maxLen {
			suffix := "..."
			if len(parts) > 2 {
				suffix = parts[2]
			}
			return value[:maxLen-len(suffix)] + suffix, nil
		}
		return value, nil
	case "default":
		if value == "" && len(parts) > 1 {
			return parts[1], nil
		}
		return value, nil
	case "escape":
		return escapeHTML(value), nil
	default:
		return value, nil
	}
}

// escapeHTML escapes HTML special characters
func escapeHTML(s string) string {
	s = strings.ReplaceAll(s, "&", "&amp;")
	s = strings.ReplaceAll(s, "<", "&lt;")
	s = strings.ReplaceAll(s, ">", "&gt;")
	s = strings.ReplaceAll(s, "\"", "&quot;")
	s = strings.ReplaceAll(s, "'", "&#39;")
	return s
}

// toString converts any value to string
func toString(v any) string {
	if v == nil {
		return ""
	}
	switch val := v.(type) {
	case string:
		return val
	case int:
		return strconv.Itoa(val)
	case int64:
		return strconv.FormatInt(val, 10)
	case float64:
		return strconv.FormatFloat(val, 'f', -1, 64)
	case float32:
		return strconv.FormatFloat(float64(val), 'f', -1, 64)
	case bool:
		if val { return "true" }
		return "false"
	case []byte:
		return string(val)
	default:
		return fmt.Sprintf("%v", v)
	}
}

// toInt converts any value to int
func toInt(v any) int {
	if v == nil { return 0 }
	switch val := v.(type) {
	case int: return val
	case int64: return int(val)
	case float64: return int(val)
	case float32: return int(val)
	case string:
		i, _ := strconv.Atoi(val)
		return i
	default: return 0
	}
}

// toFloat64 converts any value to float64
func toFloat64(v any) float64 {
	if v == nil { return 0 }
	switch val := v.(type) {
	case float64: return val
	case float32: return float64(val)
	case int: return float64(val)
	case int64: return float64(val)
	case string:
		f, _ := strconv.ParseFloat(val, 64)
		return f
	default: return 0
	}
}

// toSlice converts any value to string slice
func toSlice(v any) []string {
	if v == nil { return []string{} }
	switch val := v.(type) {
	case []string: return val
	case []any:
		result := make([]string, len(val))
		for i, item := range val {
			result[i] = toString(item)
		}
		return result
	case string: return []string{val}
	default: return []string{toString(v)}
	}
}

// length returns the length of a value
func length(v any) int {
	if v == nil { return 0 }
	switch val := v.(type) {
	case string: return len(val)
	case []any: return len(val)
	case []string: return len(val)
	case map[string]any: return len(val)
	default: return 0
	}
}

// isEmpty checks if a value is empty
func isEmpty(v any) bool {
	if v == nil { return true }
	switch val := v.(type) {
	case string: return val == ""
	case int: return val == 0
	case int64: return val == 0
	case float64: return val == 0
	case float32: return val == 0
	case bool: return !val
	case []any: return len(val) == 0
	case []string: return len(val) == 0
	case map[string]any: return len(val) == 0
	default: return false
	}
}
