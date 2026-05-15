package text_template_utils

import (
	"fmt"
	"log"
)

// ExampleTemplateEngine_Render demonstrates basic template rendering
func ExampleTemplateEngine_Render() {
	engine := NewTemplateEngine()

	// Simple variable substitution
	result, err := engine.Render("Hello, {{.Name}}!", map[string]interface{}{
		"Name": "World",
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
	// Output: Hello, World!
}

// ExampleTemplateEngine_Render_nested demonstrates nested data access
func ExampleTemplateEngine_Render_nested() {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"User": map[string]interface{}{
			"Name":    "Alice",
			"Email":   "alice@example.com",
			"Country": "Wonderland",
		},
	}

	result, err := engine.Render("{{.User.Name}} <{{.User.Email}}> from {{.User.Country}}", data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
	// Output: Alice <alice@example.com> from Wonderland
}

// ExampleTemplateEngine_Render_conditionals demonstrates if/else blocks
func ExampleTemplateEngine_Render_conditionals() {
	engine := NewTemplateEngine()

	// User with admin status
	adminUser := map[string]interface{}{
		"Name":  "Admin",
		"Admin": true,
	}

	result1, _ := engine.Render("Welcome, {{.Name}}!{{if .Admin}} [ADMIN]{{end}}", adminUser)
	fmt.Println(result1)

	// Regular user
	regularUser := map[string]interface{}{
		"Name":  "User",
		"Admin": false,
	}

	result2, _ := engine.Render("Welcome, {{.Name}}!{{if .Admin}} [ADMIN]{{end}}", regularUser)
	fmt.Println(result2)
	// Output:
	// Welcome, Admin! [ADMIN]
	// Welcome, User!
}

// ExampleTemplateEngine_Render_loops demonstrates range loops
func ExampleTemplateEngine_Render_loops() {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Items": []interface{}{"Apple", "Banana", "Cherry"},
	}

	result, err := engine.Render(`Shopping List:
{{range $i, $item := .Items}}{{$i}}. {{$item}}
{{end}}`, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
	// Output:
	// Shopping List:
	// 0. Apple
	// 1. Banana
	// 2. Cherry
}

// ExampleTemplateEngine_Render_stringFunctions demonstrates string manipulation
func ExampleTemplateEngine_Render_stringFunctions() {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Text": "  Hello, World!  ",
	}

	result, err := engine.Render(`Original: "{{.Text}}"
Upper: {{upper .Text}}
Lower: {{lower .Text}}
Trimmed: "{{trim .Text}}"
Truncated: {{truncate (trim .Text) 5}}`, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
}

// ExampleTemplateEngine_Render_defaultValues demonstrates default value handling
func ExampleTemplateEngine_Render_defaultValues() {
	engine := NewTemplateEngine()

	// With value
	data1 := map[string]interface{}{"Name": "Alice"}
	result1, _ := engine.Render("Name: {{default \"Anonymous\" .Name}}", data1)
	fmt.Println(result1)

	// Without value (empty string)
	data2 := map[string]interface{}{"Name": ""}
	result2, _ := engine.Render("Name: {{default \"Anonymous\" .Name}}", data2)
	fmt.Println(result2)

	// Without value (nil)
	data3 := map[string]interface{}{}
	result3, _ := engine.Render("Name: {{default \"Anonymous\" .Name}}", data3)
	fmt.Println(result3)
	// Output:
	// Name: Alice
	// Name: Anonymous
	// Name: Anonymous
}

// ExampleTemplateEngine_Render_listFunctions demonstrates list operations
func ExampleTemplateEngine_Render_listFunctions() {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Numbers": []interface{}{1, 2, 3, 4, 5},
		"Names":   []interface{}{"Alice", "Bob", "Charlie"},
	}

	result, err := engine.Render(`Numbers: {{join .Numbers ", "}}
First: {{first .Numbers}}
Last: {{last .Numbers}}
Length: {{length .Numbers}}
Names: {{join .Names ", "}}
Reversed: {{join (reverse .Names) ", "}}`, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
}

// ExampleTemplateEngine_Render_mapFunctions demonstrates map operations
func ExampleTemplateEngine_Render_mapFunctions() {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"Config": map[string]interface{}{
			"host": "localhost",
			"port": 8080,
			"mode": "development",
		},
	}

	result, err := engine.Render(`Server: {{get .Config "host"}}:{{get .Config "port"}}
Mode: {{get .Config "mode"}}
Has port? {{if hasKey .Config "port"}}yes{{else}}no{{end}}
Has ssl? {{if hasKey .Config "ssl"}}yes{{else}}no{{end}}`, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
}

// ExampleTemplateEngine_Render_numericFunctions demonstrates math operations
func ExampleTemplateEngine_Render_numericFunctions() {
	engine := NewTemplateEngine()

	data := map[string]interface{}{
		"A": 10,
		"B": 3,
	}

	result, err := engine.Render(`A = {{.A}}, B = {{.B}}
Add: {{add .A .B}}
Sub: {{sub .A .B}}
Mul: {{mul .A .B}}
Div: {{div .A .B}}
Mod: {{mod .A .B}}
Min: {{min .A .B}}
Max: {{max .A .B}}`, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
}

// ExampleTemplateEngine_AddFunc demonstrates custom function registration
func ExampleTemplateEngine_AddFunc() {
	engine := NewTemplateEngine()

	// Register custom functions
	engine.AddFunc("greet", func(name string) string {
		return fmt.Sprintf("Hello, %s! Nice to meet you.", name)
	})
	engine.AddFunc("formatCurrency", func(amount float64) string {
		return fmt.Sprintf("$%.2f", amount)
	})

	data := map[string]interface{}{
		"Name":   "Alice",
		"Amount": 1234.5,
	}

	result, _ := engine.Render(`{{greet .Name}}
Your balance: {{formatCurrency .Amount}}`, data)
	fmt.Println(result)
}

// ExampleTemplateEngine_RenderWithDelims demonstrates custom delimiters
func ExampleTemplateEngine_RenderWithDelims() {
	engine := NewTemplateEngine()

	// Use custom delimiters for templates that need to preserve {{ }}
	template := `<div class="user">
  <span>[= .Name =]</span>
  <span>[= .Email =]</span>
</div>`

	data := map[string]interface{}{
		"Name":  "Alice",
		"Email": "alice@example.com",
	}

	result, _ := engine.RenderWithDelims(template, "[=", "=]", data)
	fmt.Println(result)
}

// ExampleSimpleTemplate demonstrates simple key-value substitution
func ExampleSimpleTemplate() {
	st := NewSimpleTemplate()

	template := "Hello, {{name}}! Welcome to {{city}}."

	result := st.Replace(template, map[string]string{
		"name": "Alice",
		"city": "Wonderland",
	})

	fmt.Println(result)
	// Output: Hello, Alice! Welcome to Wonderland.
}

// ExampleSimpleTemplate_ExtractVariables demonstrates variable extraction
func ExampleSimpleTemplate_ExtractVariables() {
	st := NewSimpleTemplate()

	template := "Dear {{title}} {{name}}, your order {{orderId}} is ready."
	vars := st.ExtractVariables(template)

	fmt.Printf("Found %d variables: %v\n", len(vars), vars)
	// Output: Found 3 variables: [title name orderId]
}

// ExampleTemplateBuilder demonstrates programmatic template building
func ExampleTemplateBuilder() {
	b := NewTemplateBuilder()

	b.WriteIndentedLine("User Profile:")
	b.Indent()
	b.WriteIndented("Name: ").Variable("User.Name").WriteLine("")
	b.WriteIndented("Email: ").Variable("User.Email").WriteLine("")
	b.WriteIndented("Age: ").Variable("User.Age").WriteLine("")
	b.IfBlock("User.Verified", func(b *TemplateBuilder) {
		b.WriteIndentedLine("Status: Verified ✓")
	})
	b.WriteIndentedLine("Skills:")
	b.Indent()
	b.RangeBlock("User.Skills", "skill", func(b *TemplateBuilder) {
		b.WriteIndented("- ").Variable("skill").WriteLine("")
	})
	b.Dedent()
	b.Dedent()

	template := b.Build()
	fmt.Println(template)
}

// ExampleTemplateBuilder_completeExample demonstrates a complete template building scenario
func ExampleTemplateBuilder_completeExample() {
	engine := NewTemplateEngine()

	// Build template programmatically
	b := NewTemplateBuilder()
	b.WriteIndentedLine("{{if .ShowHeader}}")
	b.Indent()
	b.WriteIndentedLine("Report: {{.Title}}")
	b.WriteIndentedLine("Generated: {{.Date}}")
	b.Dedent()
	b.WriteIndentedLine("{{end}}")
	b.WriteIndentedLine("")
	b.WriteIndentedLine("Summary:")
	b.Indent()
	b.WriteIndentedLine("Total items: {{length .Items}}")
	b.WriteIndentedLine("Items:")
	b.Indent()
	b.RangeBlock("Items", "item", func(b *TemplateBuilder) {
		b.WriteIndented("- {{.item.Name}}: {{.item.Count}}").WriteLine("")
	})
	b.Dedent()
	b.Dedent()

	template := b.Build()

	// Data for rendering
	data := map[string]interface{}{
		"ShowHeader": true,
		"Title":      "Sales Report",
		"Date":       "2024-01-15",
		"Items": []interface{}{
			map[string]interface{}{"Name": "Product A", "Count": 100},
			map[string]interface{}{"Name": "Product B", "Count": 200},
			map[string]interface{}{"Name": "Product C", "Count": 150},
		},
	}

	result, err := engine.Render(template, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
}

// ExampleTemplateEngine_Render_complexTemplate demonstrates a complex real-world template
func ExampleTemplateEngine_Render_complexTemplate() {
	engine := NewTemplateEngine()

	template := `{{if .Header}}========================================
{{.Title}}
========================================
{{end}}Dear {{default "Customer" .Customer.Name}},

Thank you for your order #{{.Order.ID}}!

{{if .Order.Items}}Items ordered:
{{range $i, $item := .Order.Items}}{{$i}}. {{$item.Name}} x {{$item.Quantity}} - {{formatPrice $item.Price}}
{{end}}
{{end}}Subtotal: {{formatPrice .Order.Subtotal}}
{{if .Order.Discount}}Discount: -{{formatPrice .Order.Discount}}
{{end}}Total: {{formatPrice .Order.Total}}

{{if .Order.Shipping}}Shipping Address:
{{.Order.Shipping.Street}}
{{.Order.Shipping.City}}, {{.Order.Shipping.State}} {{.Order.Shipping.Zip}}{{end}}

Best regards,
{{.Company.Name}}`

	// Add custom function
	engine.AddFunc("formatPrice", func(cents int) string {
		return fmt.Sprintf("$%.2f", float64(cents)/100)
	})

	data := map[string]interface{}{
		"Header": true,
		"Title":  "Order Confirmation",
		"Customer": map[string]interface{}{
			"Name": "Alice Smith",
		},
		"Order": map[string]interface{}{
			"ID": "ORD-12345",
			"Items": []interface{}{
				map[string]interface{}{"Name": "Widget A", "Quantity": 2, "Price": 1999},
				map[string]interface{}{"Name": "Widget B", "Quantity": 1, "Price": 2999},
			},
			"Subtotal": 6997,
			"Discount": 500,
			"Total":    6497,
			"Shipping": map[string]interface{}{
				"Street": "123 Main St",
				"City":   "Springfield",
				"State":  "IL",
				"Zip":    "62701",
			},
		},
		"Company": map[string]interface{}{
			"Name": "ACME Corp",
		},
	}

	result, err := engine.Render(template, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result)
}