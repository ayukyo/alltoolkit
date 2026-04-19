package text_table_utils

import (
	"strings"
	"testing"
)

func TestNewTable(t *testing.T) {
	table := NewTable("Name", "Age", "City")
	if len(table.columns) != 3 {
		t.Errorf("Expected 3 columns, got %d", len(table.columns))
	}
	if table.columns[0].Header != "Name" {
		t.Errorf("Expected 'Name', got '%s'", table.columns[0].Header)
	}
}

func TestAddRow(t *testing.T) {
	table := NewTable("A", "B").AddRow("1", "2").AddRow("3", "4")
	if len(table.rows) != 2 {
		t.Errorf("Expected 2 rows, got %d", len(table.rows))
	}
	if table.rows[0][0].Text != "1" {
		t.Errorf("Expected '1', got '%s'", table.rows[0][0].Text)
	}
}

func TestSetStyle(t *testing.T) {
	table := NewTable("A").SetStyle(StyleASCII)
	if table.style.Horizontal != "-" {
		t.Errorf("Expected '-' for ASCII style, got '%s'", table.style.Horizontal)
	}
}

func TestSetShowHeader(t *testing.T) {
	table := NewTable("A").SetShowHeader(false)
	if table.showHeader {
		t.Error("Expected showHeader to be false")
	}
}

func TestSetShowBorders(t *testing.T) {
	table := NewTable("A").SetShowBorders(false)
	if table.showBorders {
		t.Error("Expected showBorders to be false")
	}
}

func TestSetPadding(t *testing.T) {
	table := NewTable("A").SetPadding(2)
	if table.padding != 2 {
		t.Errorf("Expected padding 2, got %d", table.padding)
	}
}

func TestSetColumnAlignment(t *testing.T) {
	table := NewTable("A", "B", "C")
	table.SetColumnAlignment(1, AlignCenter)
	if table.columns[1].Alignment != AlignCenter {
		t.Errorf("Expected AlignCenter, got %d", table.columns[1].Alignment)
	}
}

func TestHideColumn(t *testing.T) {
	table := NewTable("A", "B", "C").HideColumn(1)
	if !table.columns[1].Hidden {
		t.Error("Expected column 1 to be hidden")
	}
}

func TestStringBasic(t *testing.T) {
	table := NewTable("Name", "Age")
	table.SetStyle(StyleASCII).AddRow("Alice", "25").AddRow("Bob", "30")
	output := table.String()

	if !strings.Contains(output, "Name") {
		t.Error("Expected output to contain 'Name'")
	}
	if !strings.Contains(output, "Alice") {
		t.Error("Expected output to contain 'Alice'")
	}
	if !strings.Contains(output, "Bob") {
		t.Error("Expected output to contain 'Bob'")
	}
}

func TestStringUnicode(t *testing.T) {
	table := NewTable("姓名", "年龄")
	table.SetStyle(StyleUnicode).AddRow("张三", "25").AddRow("李四", "30")
	output := table.String()

	if !strings.Contains(output, "张三") {
		t.Error("Expected output to contain '张三'")
	}
	if !strings.Contains(output, "李四") {
		t.Error("Expected output to contain '李四'")
	}
}

func TestStringNoBorders(t *testing.T) {
	table := NewTable("A", "B")
	table.SetShowBorders(false).AddRow("1", "2")
	output := table.String()

	if strings.Contains(output, "│") {
		t.Error("Expected no borders in output")
	}
}

func TestStringNoHeader(t *testing.T) {
	table := NewTable("A", "B")
	table.SetShowHeader(false).AddRow("1", "2")
	output := table.String()

	if strings.Contains(output, "A") || strings.Contains(output, "B") {
		t.Error("Expected no headers in output")
	}
}

func TestAlignmentLeft(t *testing.T) {
	table := NewTable("Col")
	table.SetStyle(StyleNone).SetShowBorders(false).SetShowHeader(false)
	table.SetColumnAlignment(0, AlignLeft).AddRow("x")
	output := table.String()
	// Left aligned text should start with padding
	if !strings.HasPrefix(strings.TrimSpace(output), "x") {
		t.Errorf("Expected left aligned text, got '%s'", output)
	}
}

func TestAlignmentRight(t *testing.T) {
	table := NewTable("Col")
	table.SetStyle(StyleNone).SetShowBorders(false).SetShowHeader(false).SetPadding(0)
	table.SetColumnAlignment(0, AlignRight).SetColumnMinWidth(0, 10).AddRow("x")
	output := table.String()
	// Right aligned text should have leading spaces
	if !strings.HasPrefix(strings.TrimSpace(output), "         x") {
		t.Errorf("Expected right aligned text, got '%s'", output)
	}
}

func TestAlignmentCenter(t *testing.T) {
	table := NewTable("Col")
	table.SetStyle(StyleNone).SetShowBorders(false).SetShowHeader(false).SetPadding(0)
	table.SetColumnAlignment(0, AlignCenter).SetColumnMinWidth(0, 10).AddRow("x")
	output := table.String()
	// Center aligned text should have spaces on both sides
	if !strings.HasPrefix(strings.TrimSpace(output), "    x") {
		t.Errorf("Expected center aligned text, got '%s'", output)
	}
}

func TestMinWidth(t *testing.T) {
	table := NewTable("A")
	table.SetStyle(StyleNone).SetShowBorders(false).SetShowHeader(false).SetPadding(0)
	table.SetColumnMinWidth(0, 10).AddRow("x")
	output := table.String()
	// Output should be padded to at least 10 characters
	if len(strings.TrimSpace(output)) < 10 {
		t.Errorf("Expected min width 10, got %d", len(strings.TrimSpace(output)))
	}
}

func TestSimpleTable(t *testing.T) {
	headers := []string{"Name", "Age"}
	rows := [][]string{{"Alice", "25"}, {"Bob", "30"}}
	output := SimpleTable(headers, rows)

	if !strings.Contains(output, "Name") || !strings.Contains(output, "Alice") {
		t.Error("Expected SimpleTable to contain headers and data")
	}
}

func TestSimpleMarkdownTable(t *testing.T) {
	headers := []string{"Name", "Age"}
	rows := [][]string{{"Alice", "25"}, {"Bob", "30"}}
	output := SimpleMarkdownTable(headers, rows)

	// Markdown tables should have pipe separators
	if !strings.Contains(output, "|") {
		t.Error("Expected Markdown table to contain pipe characters")
	}
	// Should have header separator line
	if !strings.Contains(output, "---") {
		t.Error("Expected Markdown table to have separator line")
	}
}

func TestMultipleStyles(t *testing.T) {
	styles := []BorderStyle{StyleASCII, StyleUnicode, StyleDouble, StyleRounded, StyleMarkdown, StyleNone}
	table := NewTable("A", "B").AddRow("1", "2")

	for _, style := range styles {
		table.SetStyle(style)
		output := table.String()
		if output == "" {
			t.Error("Expected non-empty output for style")
		}
	}
}

func TestColoredOutput(t *testing.T) {
	redColor := func(s string) string { return "\033[31m" + s + "\033[0m" }

	table := NewTable("A", "B")
	table.SetHeaderColor(redColor).SetBorderColor(redColor)
	table.AddRow("1", "2")

	output := table.String()
	if !strings.Contains(output, "\033[31m") {
		t.Error("Expected colored output")
	}
}

func TestMaxWidth(t *testing.T) {
	table := NewTable("LongHeader", "AnotherHeader")
	table.SetMaxWidth(30).AddRow("VeryLongContent", "MoreContent")
	output := table.String()

	// Table should not exceed max width significantly
	lines := strings.Split(output, "\n")
	for _, line := range lines {
		if len(line) > 35 { // Allow some slack for borders
			t.Errorf("Line exceeds max width: %s", line)
		}
	}
}

func TestEmptyTable(t *testing.T) {
	table := NewTable("A", "B")
	output := table.String()
	if !strings.Contains(output, "A") {
		t.Error("Expected header in empty table")
	}
}

func TestHiddenColumns(t *testing.T) {
	table := NewTable("A", "B", "C")
	table.HideColumn(1).AddRow("1", "2", "3")
	output := table.String()

	if strings.Contains(output, "B") || strings.Contains(output, "2") {
		t.Error("Expected hidden column not to appear in output")
	}
}

func TestCellColor(t *testing.T) {
	greenColor := func(s string) string { return "\033[32m" + s + "\033[0m" }

	table := NewTable("A", "B")
	table.AddRowWithColor([]Cell{
		{Text: "colored", Color: greenColor},
		{Text: "normal", Color: nil},
	})

	output := table.String()
	if !strings.Contains(output, "\033[32mcolored") {
		t.Error("Expected colored cell in output")
	}
}

func TestUnicodeWidth(t *testing.T) {
	// Test that Unicode characters are counted correctly
	table := NewTable("名称", "描述")
	table.SetStyle(StyleUnicode).AddRow("中文测试", "这是一个测试")
	output := table.String()

	// Should render without issues
	if output == "" {
		t.Error("Expected non-empty output for Unicode content")
	}
}

func TestAddRowWithVariousTypes(t *testing.T) {
	table := NewTable("String", "Int", "Float", "Bool")
	table.AddRow("hello", 42, 3.14, true)
	output := table.String()

	if !strings.Contains(output, "hello") {
		t.Error("Expected 'hello' in output")
	}
	if !strings.Contains(output, "42") {
		t.Error("Expected '42' in output")
	}
	if !strings.Contains(output, "3.14") {
		t.Error("Expected '3.14' in output")
	}
	if !strings.Contains(output, "true") {
		t.Error("Expected 'true' in output")
	}
}

func TestMethodChaining(t *testing.T) {
	// Test that all setter methods return *Table for chaining
	table := NewTable("A", "B").
		SetStyle(StyleUnicode).
		SetShowHeader(true).
		SetShowBorders(true).
		SetPadding(2).
		SetAutoWidth(true).
		SetMaxWidth(100).
		SetColumnAlignment(0, AlignCenter).
		SetColumnMinWidth(0, 10).
		SetColumnMaxWidth(0, 50).
		HideColumn(1).
		AddRow("x", "y")

	if table == nil {
		t.Error("Expected table after method chaining")
	}
}

func TestColumnConfig(t *testing.T) {
	table := NewTable("A", "B", "C")
	table.SetColumnAlignment(0, AlignLeft).
		SetColumnAlignment(1, AlignCenter).
		SetColumnAlignment(2, AlignRight).
		SetColumnMinWidth(0, 5).
		SetColumnMinWidth(1, 10).
		SetColumnMinWidth(2, 15)

	if table.columns[0].Alignment != AlignLeft {
		t.Error("Expected AlignLeft for column 0")
	}
	if table.columns[1].Alignment != AlignCenter {
		t.Error("Expected AlignCenter for column 1")
	}
	if table.columns[2].Alignment != AlignRight {
		t.Error("Expected AlignRight for column 2")
	}
	if table.columns[0].MinWidth != 5 {
		t.Error("Expected MinWidth 5 for column 0")
	}
}