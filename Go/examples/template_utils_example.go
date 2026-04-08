package main

import (
	"fmt"
	"log"

	"github.com/ayukyo/alltoolkit/Go/template_utils"
)

func main() {
	fmt.Println("=== Go Template Utils Examples ===\n")

	// Example 1: Basic variable substitution
	fmt.Println("1. Basic Variable Substitution:")
	result, err := template_utils.Render("Hello, {{name}}!", map[string]any{
		"name": "World",
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("   Template: 'Hello, {{name}}!'\n")
	fmt.Printf("   Result:   %s\n\n", result)

	// Example 2: Multiple variables
	fmt.Println("2. Multiple Variables:")
	result, err = template_utils.Render("{{greeting}}, {{name}}! Welcome to {{place}}.", map[string]any{
		"greeting": "Hello",
		"name":     "Alice",
		"place":    "Wonderland",
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("   Result: %s\n\n", result)

	// Example 3: Using filters
	fmt.Println("3. Using Filters:")

	// Upper filter
	result, _ = template_utils.Render("{{name|upper}}", map[string]any{"name": "john"})
	fmt.Printf("   Upper:   {{name|upper}} -> %s\n", result)

	// Lower filter
	result, _ = template_utils.Render("{{name|lower}}", map[string]any{"name": "JOHN"})
	fmt.Printf("   Lower:   {{name|lower}} -> %s\n", result)

	// Trim filter
	result, _ = template_utils.Render("{{text|trim}}", map[string]any{"text": "  hello  "})
	fmt.Printf("   Trim:    '{{text|trim}}' -> '%s'\n", result)

	// Truncate filter
	result, _ = template_utils.Render("{{text|truncate:20}}", map[string]any{
		"text": "This is a very long text that needs truncation",
	})
	fmt.Printf("   Truncate: {{text|truncate:20}} -> %s\n\n", result)

	// Example 4: Default values
	fmt.Println("4. Default Values:")
	result, _ = template_utils.Render("Hello, {{name|default:Anonymous}}!", map[string]any{
		"name": "",
	})
	fmt.Printf("   Empty name: %s\n", result)

	result, _ = template_utils.Render("Hello, {{name|default:Anonymous}}!", map[string]any{
		"name": "John",
	})
	fmt.Printf("   With name:  %s\n\n", result)

	// Example 5: Nested data access
	fmt.Println("5. Nested Data Access:")
	result, err = template_utils.Render("User: {{user.name}}, Age: {{user.age}}", map[string]any{
		"user": map[string]any{
			"name": "John Doe",
			"age":  30,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("   Template: 'User: {{user.name}}, Age: {{user.age}}'\n")
	fmt.Printf("   Result:   %s\n\n", result)

	// Example 6: Different data types
	fmt.Println("6. Different Data Types:")
	result, _ = template_utils.Render("String: {{s}}, Int: {{i}}, Float: {{f}}, Bool: {{b}}", map[string]any{
		"s": "text",
		"i": 42,
		"f": 3.14,
		"b": true,
	})
	fmt.Printf("   %s\n\n", result)

	// Example 7: Using TemplateEngine with custom functions
	fmt.Println("7. Custom Functions:")
	engine := template_utils.New()
	engine.RegisterFunction("repeat", func(args ...any) (any, error) {
		if len(args) < 2 {
			return "", nil
		}
		s := template_utils.ToString(args[0])
		count := template_utils.ToInt(args[1])
		result := ""
		for i := 0; i < count; i++ {
			result += s
		}
		return result, nil
	})

	// Note: Custom function calls in templates would need additional syntax
	// This demonstrates the engine capability
	fmt.Println("   Custom 'repeat' function registered")
	fmt.Println("   (Function calls in templates: {{repeat:hello:3}} -> hellohellohello)")
	fmt.Println()

	// Example 8: Global variables
	fmt.Println("8. Global Variables:")
	engine2 := template_utils.New()
	engine2.SetGlobal("appName", "MyAwesomeApp")
	engine2.SetGlobal("version", "1.0.0")

	tmpl, _ := engine2.Parse("{{appName}} v{{version}}")
	result, _ = tmpl.Render(map[string]any{})
	fmt.Printf("   Template: '{{appName}} v{{version}}'\n")
	fmt.Printf("   Result:   %s\n\n", result)

	// Example 9: HTML escaping
	fmt.Println("9. HTML Escaping:")
	result, _ = template_utils.Render("{{content|escape}}", map[string]any{
		"content": "<script>alert('XSS')</script>",
	})
	fmt.Printf("   Input:  <script>alert('XSS')</script>\n")
	fmt.Printf("   Output: %s\n\n", result)

	// Example 10: Complex template
	fmt.Println("10. Complex Template:")
	complexTemplate := `User Profile
============
Name:    {{user.name|upper}}
Email:   {{user.email}}
Role:    {{user.role|default:User}}
Status:  {{user.active}}
`
	result, _ = template_utils.Render(complexTemplate, map[string]any{
		"user": map[string]any{
			"name":   "john doe",
			"email":  "john@example.com",
			"role":   "admin",
			"active": true,
		},
	})
	fmt.Println(result)

	// Example 11: Error handling
	fmt.Println("11. Error Handling:")
	_, err = template_utils.Render("{{unclosed", map[string]any{})
	if err != nil {
		fmt.Printf("   Expected error for unclosed tag: %v\n\n", err)
	}

	// Example 12: Performance - reuse engine
	fmt.Println("12. Performance - Reuse Engine:")
	engine3 := template_utils.New()
	tmpl, _ = engine3.Parse("Hello, {{name}}!")

	for i := 1; i <= 3; i++ {
		result, _ = tmpl.Render(map[string]any{"name": fmt.Sprintf("User%d", i)})
		fmt.Printf("   Render %d: %s\n", i, result)
	}

	fmt.Println("\n=== All Examples Completed ===")
}
EOF