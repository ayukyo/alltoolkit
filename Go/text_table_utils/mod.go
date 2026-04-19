// Package text_table_utils provides terminal table formatting utilities.
// Supports multiple border styles, text alignment, and colored output.
package text_table_utils

import (
	"fmt"
	"strings"
	"unicode/utf8"
)

// BorderStyle defines the characters used for table borders
type BorderStyle struct {
	TopLeft     string
	TopRight    string
	BottomLeft  string
	BottomRight string
	Horizontal  string
	Vertical    string
	LeftTee     string
	RightTee    string
	TopTee      string
	BottomTee   string
	Cross       string
}

// Predefined border styles
var (
	// StyleASCII uses basic ASCII characters (works on all terminals)
	StyleASCII = BorderStyle{
		TopLeft:     "+",
		TopRight:    "+",
		BottomLeft:  "+",
		BottomRight: "+",
		Horizontal:  "-",
		Vertical:    "|",
		LeftTee:     "+",
		RightTee:    "+",
		TopTee:      "+",
		BottomTee:   "+",
		Cross:       "+",
	}

	// StyleUnicode uses Unicode box drawing characters
	StyleUnicode = BorderStyle{
		TopLeft:     "┌",
		TopRight:    "┐",
		BottomLeft:  "└",
		BottomRight: "┘",
		Horizontal:  "─",
		Vertical:    "│",
		LeftTee:     "├",
		RightTee:    "┤",
		TopTee:      "┬",
		BottomTee:   "┴",
		Cross:       "┼",
	}

	// StyleDouble uses double-line Unicode characters
	StyleDouble = BorderStyle{
		TopLeft:     "╔",
		TopRight:    "╗",
		BottomLeft:  "╚",
		BottomRight: "╝",
		Horizontal:  "═",
		Vertical:    "║",
		LeftTee:     "╠",
		RightTee:    "╣",
		TopTee:      "╦",
		BottomTee:   "╩",
		Cross:       "╬",
	}

	// StyleRounded uses rounded corner Unicode characters
	StyleRounded = BorderStyle{
		TopLeft:     "╭",
		TopRight:    "╮",
		BottomLeft:  "╰",
		BottomRight: "╯",
		Horizontal:  "─",
		Vertical:    "│",
		LeftTee:     "├",
		RightTee:    "┤",
		TopTee:      "┬",
		BottomTee:   "┴",
		Cross:       "┼",
	}

	// StyleMarkdown uses Markdown table format
	StyleMarkdown = BorderStyle{
		TopLeft:     "|",
		TopRight:    "|",
		BottomLeft:  "|",
		BottomRight: "|",
		Horizontal:  "-",
		Vertical:    "|",
		LeftTee:     "|",
		RightTee:    "|",
		TopTee:      "|",
		BottomTee:   "|",
		Cross:       "|",
	}

	// StyleNone renders table without borders
	StyleNone = BorderStyle{
		TopLeft:     "",
		TopRight:    "",
		BottomLeft:  "",
		BottomRight: "",
		Horizontal:  " ",
		Vertical:    " ",
		LeftTee:     "",
		RightTee:    "",
		TopTee:      "",
		BottomTee:   "",
		Cross:       "",
	}
)

// Alignment specifies text alignment within a cell
type Alignment int

const (
	AlignLeft Alignment = iota
	AlignCenter
	AlignRight
)

// ColumnConfig holds configuration for a single column
type ColumnConfig struct {
	Header    string
	Alignment Alignment
	MinWidth  int
	MaxWidth  int
	Hidden    bool
}

// ColorFunc is a function that applies color to text
type ColorFunc func(string) string

// Cell represents a single cell with optional coloring
type Cell struct {
	Text  string
	Color ColorFunc
}

// Table represents a table for rendering
type Table struct {
	style        BorderStyle
	columns      []ColumnConfig
	rows         [][]Cell
	headerColor  ColorFunc
	borderColor  ColorFunc
	showHeader   bool
	showBorders  bool
	padding      int
	autoWidth    bool
	maxWidth     int
}

// NewTable creates a new table with default settings
func NewTable(columns ...string) *Table {
	colConfigs := make([]ColumnConfig, len(columns))
	for i, col := range columns {
		colConfigs[i] = ColumnConfig{
			Header:    col,
			Alignment: AlignLeft,
			MinWidth:  0,
			MaxWidth:  0,
			Hidden:    false,
		}
	}
	return &Table{
		style:       StyleUnicode,
		columns:     colConfigs,
		rows:        make([][]Cell, 0),
		showHeader:  true,
		showBorders: true,
		padding:     1,
		autoWidth:   true,
		maxWidth:    0,
	}
}

// SetStyle sets the border style
func (t *Table) SetStyle(style BorderStyle) *Table {
	t.style = style
	return t
}

// SetHeaderColor sets a color function for the header row
func (t *Table) SetHeaderColor(color ColorFunc) *Table {
	t.headerColor = color
	return t
}

// SetBorderColor sets a color function for borders
func (t *Table) SetBorderColor(color ColorFunc) *Table {
	t.borderColor = color
	return t
}

// SetShowHeader enables or disables header row
func (t *Table) SetShowHeader(show bool) *Table {
	t.showHeader = show
	return t
}

// SetShowBorders enables or disables borders
func (t *Table) SetShowBorders(show bool) *Table {
	t.showBorders = show
	return t
}

// SetPadding sets the cell padding
func (t *Table) SetPadding(padding int) *Table {
	t.padding = padding
	return t
}

// SetAutoWidth enables or disables automatic column width
func (t *Table) SetAutoWidth(auto bool) *Table {
	t.autoWidth = auto
	return t
}

// SetMaxWidth sets maximum total table width (0 = unlimited)
func (t *Table) SetMaxWidth(width int) *Table {
	t.maxWidth = width
	return t
}

// SetColumnAlignment sets alignment for a specific column
func (t *Table) SetColumnAlignment(col int, align Alignment) *Table {
	if col >= 0 && col < len(t.columns) {
		t.columns[col].Alignment = align
	}
	return t
}

// SetColumnMinWidth sets minimum width for a specific column
func (t *Table) SetColumnMinWidth(col int, width int) *Table {
	if col >= 0 && col < len(t.columns) {
		t.columns[col].MinWidth = width
	}
	return t
}

// SetColumnMaxWidth sets maximum width for a specific column
func (t *Table) SetColumnMaxWidth(col int, width int) *Table {
	if col >= 0 && col < len(t.columns) {
		t.columns[col].MaxWidth = width
	}
	return t
}

// HideColumn hides a specific column
func (t *Table) HideColumn(col int) *Table {
	if col >= 0 && col < len(t.columns) {
		t.columns[col].Hidden = true
	}
	return t
}

// AddRow adds a row to the table
func (t *Table) AddRow(cells ...interface{}) *Table {
	row := make([]Cell, len(cells))
	for i, cell := range cells {
		row[i] = Cell{Text: fmt.Sprintf("%v", cell)}
	}
	t.rows = append(t.rows, row)
	return t
}

// AddRowWithColor adds a row with colored cells
func (t *Table) AddRowWithColor(cells []Cell) *Table {
	t.rows = append(t.rows, cells)
	return t
}

// String returns the formatted table as a string
func (t *Table) String() string {
	var sb strings.Builder

	// Calculate visible columns
	visibleCols := make([]int, 0)
	for i, col := range t.columns {
		if !col.Hidden {
			visibleCols = append(visibleCols, i)
		}
	}

	if len(visibleCols) == 0 {
		return ""
	}

	// Calculate column widths
	widths := t.calculateWidths(visibleCols)

	// Render table
	if t.showBorders {
		t.renderBorder(&sb, widths, visibleCols, "top")
	}

	if t.showHeader {
		t.renderHeader(&sb, widths, visibleCols)
		if t.showBorders {
			t.renderBorder(&sb, widths, visibleCols, "separator")
		}
	}

	for _, row := range t.rows {
		t.renderRow(&sb, widths, visibleCols, row)
	}

	if t.showBorders {
		t.renderBorder(&sb, widths, visibleCols, "bottom")
	}

	return sb.String()
}

// calculateWidths calculates the width for each column
func (t *Table) calculateWidths(visibleCols []int) []int {
	widths := make([]int, len(visibleCols))

	// Start with header widths
	for i, colIdx := range visibleCols {
		headerWidth := utf8.RuneCountInString(t.columns[colIdx].Header)
		widths[i] = headerWidth
		if t.columns[colIdx].MinWidth > widths[i] {
			widths[i] = t.columns[colIdx].MinWidth
		}
	}

	// Expand based on content
	if t.autoWidth {
		for _, row := range t.rows {
			for i, colIdx := range visibleCols {
				if colIdx < len(row) {
					cellWidth := utf8.RuneCountInString(row[colIdx].Text)
					if cellWidth > widths[i] {
						widths[i] = cellWidth
					}
				}
			}
		}
	}

	// Apply max width constraints
	for i, colIdx := range visibleCols {
		if t.columns[colIdx].MaxWidth > 0 && widths[i] > t.columns[colIdx].MaxWidth {
			widths[i] = t.columns[colIdx].MaxWidth
		}
	}

	// Apply total max width constraint
	if t.maxWidth > 0 {
		totalWidth := 0
		for _, w := range widths {
			totalWidth += w
		}
		paddingWidth := len(widths) * 2 * t.padding
		borderWidth := (len(widths) + 1) * utf8.RuneCountInString(t.style.Vertical)
		totalWidth += paddingWidth + borderWidth

		if totalWidth > t.maxWidth {
			// Proportionally reduce column widths
			availableWidth := t.maxWidth - paddingWidth - borderWidth
			if availableWidth > 0 {
				totalContentWidth := 0
				for _, w := range widths {
					totalContentWidth += w
				}
				scale := float64(availableWidth) / float64(totalContentWidth)
				for i := range widths {
					widths[i] = int(float64(widths[i]) * scale)
					if widths[i] < 1 {
						widths[i] = 1
					}
				}
			}
		}
	}

	return widths
}

// renderBorder renders a border line
func (t *Table) renderBorder(sb *strings.Builder, widths []int, visibleCols []int, borderType string) {
	var left, right, tee, horizontal string

	switch borderType {
	case "top":
		left = t.style.TopLeft
		right = t.style.TopRight
		tee = t.style.TopTee
		horizontal = t.style.Horizontal
	case "bottom":
		left = t.style.BottomLeft
		right = t.style.BottomRight
		tee = t.style.BottomTee
		horizontal = t.style.Horizontal
	case "separator":
		left = t.style.LeftTee
		right = t.style.RightTee
		tee = t.style.Cross
		horizontal = t.style.Horizontal
	}

	if t.borderColor != nil {
		left = t.borderColor(left)
		right = t.borderColor(right)
		tee = t.borderColor(tee)
		horizontal = t.borderColor(horizontal)
	}

	sb.WriteString(left)
	for i, width := range widths {
		sb.WriteString(strings.Repeat(horizontal, width+2*t.padding))
		if i < len(widths)-1 {
			sb.WriteString(tee)
		}
	}
	sb.WriteString(right)
	sb.WriteString("\n")
}

// renderHeader renders the header row
func (t *Table) renderHeader(sb *strings.Builder, widths []int, visibleCols []int) {
	if t.showBorders {
		vertical := t.style.Vertical
		if t.borderColor != nil {
			vertical = t.borderColor(vertical)
		}
		sb.WriteString(vertical)
	}

	for i, colIdx := range visibleCols {
		header := t.columns[colIdx].Header
		if t.headerColor != nil {
			header = t.headerColor(header)
		}
		sb.WriteString(t.padCell(header, widths[i], t.columns[colIdx].Alignment))
		if t.showBorders {
			vertical := t.style.Vertical
			if t.borderColor != nil {
				vertical = t.borderColor(vertical)
			}
			sb.WriteString(vertical)
		} else if i < len(visibleCols)-1 {
			sb.WriteString(" ")
		}
	}
	sb.WriteString("\n")
}

// renderRow renders a data row
func (t *Table) renderRow(sb *strings.Builder, widths []int, visibleCols []int, row []Cell) {
	if t.showBorders {
		vertical := t.style.Vertical
		if t.borderColor != nil {
			vertical = t.borderColor(vertical)
		}
		sb.WriteString(vertical)
	}

	for i, colIdx := range visibleCols {
		var text string
		var colorFunc ColorFunc

		if colIdx < len(row) {
			text = row[colIdx].Text
			colorFunc = row[colIdx].Color
		}

		if colorFunc != nil {
			text = colorFunc(text)
		}

		sb.WriteString(t.padCell(text, widths[i], t.columns[colIdx].Alignment))
		if t.showBorders {
			vertical := t.style.Vertical
			if t.borderColor != nil {
				vertical = t.borderColor(vertical)
			}
			sb.WriteString(vertical)
		} else if i < len(visibleCols)-1 {
			sb.WriteString(" ")
		}
	}
	sb.WriteString("\n")
}

// padCell pads a cell according to alignment
func (t *Table) padCell(text string, width int, align Alignment) string {
	textWidth := utf8.RuneCountInString(text)
	if textWidth >= width {
		return strings.Repeat(" ", t.padding) + text[:min(len(text), width)] + strings.Repeat(" ", t.padding)
	}

	space := width - textWidth
	padding := strings.Repeat(" ", t.padding)

	switch align {
	case AlignLeft:
		return padding + text + strings.Repeat(" ", space) + padding
	case AlignRight:
		return padding + strings.Repeat(" ", space) + text + padding
	case AlignCenter:
		leftSpace := space / 2
		rightSpace := space - leftSpace
		return padding + strings.Repeat(" ", leftSpace) + text + strings.Repeat(" ", rightSpace) + padding
	}
	return padding + text + strings.Repeat(" ", space) + padding
}

// Print prints the table to stdout
func (t *Table) Print() {
	fmt.Print(t.String())
}

// SimpleTable creates and prints a simple table from headers and rows
func SimpleTable(headers []string, rows [][]string) string {
	table := NewTable(headers...)
	for _, row := range rows {
		cells := make([]interface{}, len(row))
		for i, cell := range row {
			cells[i] = cell
		}
		table.AddRow(cells...)
	}
	return table.String()
}

// MarkdownTable creates a Markdown formatted table
func SimpleMarkdownTable(headers []string, rows [][]string) string {
	table := NewTable(headers...)
	table.SetStyle(StyleMarkdown)
	table.SetShowBorders(false)
	for _, row := range rows {
		cells := make([]interface{}, len(row))
		for i, cell := range row {
			cells[i] = cell
		}
		table.AddRow(cells...)
	}

	// Add markdown header separator
	var sb strings.Builder
	lines := strings.Split(table.String(), "\n")
	if len(lines) > 0 {
		sb.WriteString(lines[0])
		sb.WriteString("\n")

		// Add separator line
		sb.WriteString("|")
		for _, h := range headers {
			sb.WriteString(strings.Repeat("-", utf8.RuneCountInString(h)+2))
			sb.WriteString("|")
		}
		sb.WriteString("\n")

		for i, line := range lines[1:] {
			if line != "" {
				sb.WriteString(line)
				if i < len(lines)-2 {
					sb.WriteString("\n")
				}
			}
		}
	}
	return sb.String()
}

// min returns the minimum of two integers
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}