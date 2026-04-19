// Example demonstrating text_table_utils usage
package main

import (
	"fmt"
	table "text_table_utils"
)

// Color functions for terminal output
func red(s string) string {
	return "\033[31m" + s + "\033[0m"
}

func green(s string) string {
	return "\033[32m" + s + "\033[0m"
}

func yellow(s string) string {
	return "\033[33m" + s + "\033[0m"
}

func blue(s string) string {
	return "\033[34m" + s + "\033[0m"
}

func cyan(s string) string {
	return "\033[36m" + s + "\033[0m"
}

func main() {
	fmt.Println("=== text_table_utils Examples ===\n")

	// Example 1: Basic table
	fmt.Println("--- Example 1: Basic Table ---")
	basicTable()

	// Example 2: Different border styles
	fmt.Println("\n--- Example 2: Border Styles ---")
	borderStyles()

	// Example 3: Text alignment
	fmt.Println("\n--- Example 3: Text Alignment ---")
	textAlignment()

	// Example 4: Colored output
	fmt.Println("\n--- Example 4: Colored Output ---")
	coloredOutput()

	// Example 5: Column width control
	fmt.Println("\n--- Example 5: Column Width Control ---")
	columnWidth()

	// Example 6: Markdown table
	fmt.Println("\n--- Example 6: Markdown Table ---")
	markdownTable()

	// Example 7: Unicode support
	fmt.Println("\n--- Example 7: Unicode Support ---")
	unicodeSupport()

	// Example 8: Status report
	fmt.Println("\n--- Example 8: Status Report ---")
	statusReport()
}

func basicTable() {
	t := table.NewTable("ID", "Name", "Department", "Salary")
	t.AddRow(1, "Alice", "Engineering", 85000)
	t.AddRow(2, "Bob", "Marketing", 65000)
	t.AddRow(3, "Charlie", "Sales", 72000)
	t.AddRow(4, "Diana", "HR", 58000)
	t.Print()
}

func borderStyles() {
	data := [][]interface{}{
		{"Apple", 5, "$2.50"},
		{"Banana", 8, "$1.80"},
		{"Orange", 3, "$3.20"},
	}

	styles := []struct {
		name  string
		style table.BorderStyle
	}{
		{"ASCII", table.StyleASCII},
		{"Unicode", table.StyleUnicode},
		{"Double", table.StyleDouble},
		{"Rounded", table.StyleRounded},
		{"None", table.StyleNone},
	}

	for _, s := range styles {
		fmt.Printf("\n%s Style:\n", s.name)
		t := table.NewTable("Item", "Qty", "Price")
		t.SetStyle(s.style)
		for _, row := range data {
			t.AddRow(row...)
		}
		t.Print()
	}
}

func textAlignment() {
	t := table.NewTable("Left", "Center", "Right")
	t.SetColumnAlignment(0, table.AlignLeft)
	t.SetColumnAlignment(1, table.AlignCenter)
	t.SetColumnAlignment(2, table.AlignRight)
	t.AddRow("A", "B", "C")
	t.AddRow("Longer", "Medium", "X")
	t.AddRow("Short", "Y", "ZZZZ")
	t.Print()
}

func coloredOutput() {
	// Table with colored header and border
	t := table.NewTable("Status", "Service", "Uptime")
	t.SetHeaderColor(cyan)
	t.SetBorderColor(blue)
	t.AddRow("✓ Running", "API Server", "99.9%")
	t.AddRow("✓ Running", "Database", "99.8%")
	t.AddRow("⚠ Warning", "Cache", "98.5%")
	t.Print()

	// Table with colored cells
	fmt.Println("\nColored cells:")
	t2 := table.NewTable("Product", "Stock", "Price")
	t2.AddRowWithColor([]table.Cell{
		{Text: "Laptop", Color: nil},
		{Text: "In Stock", Color: green},
		{Text: "$999", Color: nil},
	})
	t2.AddRowWithColor([]table.Cell{
		{Text: "Phone", Color: nil},
		{Text: "Low", Color: yellow},
		{Text: "$699", Color: nil},
	})
	t2.AddRowWithColor([]table.Cell{
		{Text: "Tablet", Color: nil},
		{Text: "Out", Color: red},
		{Text: "$499", Color: nil},
	})
	t2.Print()
}

func columnWidth() {
	t := table.NewTable("ID", "Description", "Amount")
	t.SetColumnMinWidth(0, 5)
	t.SetColumnMinWidth(1, 20)
	t.SetColumnAlignment(2, table.AlignRight)
	t.AddRow(1, "Monthly subscription", 99.99)
	t.AddRow(2, "One-time purchase", 49.50)
	t.AddRow(3, "Annual plan", 999.00)
	t.Print()
}

func markdownTable() {
	headers := []string{"Feature", "Status", "Notes"}
	rows := [][]string{
		{"Basic tables", "✓", "Complete"},
		{"Colored output", "✓", "Complete"},
		{"Unicode support", "✓", "Complete"},
		{"Export formats", "⏳", "In progress"},
	}
	fmt.Println(table.SimpleMarkdownTable(headers, rows))
}

func unicodeSupport() {
	t := table.NewTable("名称", "价格", "库存")
	t.AddRow("苹果", "¥5.50", 100)
	t.AddRow("香蕉", "¥3.20", 150)
	t.AddRow("橙子", "¥4.80", 80)
	t.AddRow("葡萄", "¥12.00", 60)
	t.Print()
}

func statusReport() {
	t := table.NewTable("Service", "Status", "Response Time", "Last Check")
	t.SetHeaderColor(cyan)
	t.AddRowWithColor([]table.Cell{
		{Text: "API Gateway", Color: nil},
		{Text: "● Healthy", Color: green},
		{Text: "12ms", Color: nil},
		{Text: "2026-04-19 19:17", Color: nil},
	})
	t.AddRowWithColor([]table.Cell{
		{Text: "Auth Service", Color: nil},
		{Text: "● Healthy", Color: green},
		{Text: "8ms", Color: nil},
		{Text: "2026-04-19 19:17", Color: nil},
	})
	t.AddRowWithColor([]table.Cell{
		{Text: "Database", Color: nil},
		{Text: "● Healthy", Color: green},
		{Text: "25ms", Color: nil},
		{Text: "2026-04-19 19:17", Color: nil},
	})
	t.AddRowWithColor([]table.Cell{
		{Text: "Cache Server", Color: nil},
		{Text: "⚠ Degraded", Color: yellow},
		{Text: "150ms", Color: nil},
		{Text: "2026-04-19 19:17", Color: nil},
	})
	t.AddRowWithColor([]table.Cell{
		{Text: "Queue Service", Color: nil},
		{Text: "● Down", Color: red},
		{Text: "N/A", Color: nil},
		{Text: "2026-04-19 19:17", Color: nil},
	})
	t.Print()
}