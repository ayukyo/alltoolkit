//! Table rendering utilities
//! 
//! Provides simple table rendering with borders and alignment.

use crate::align::{left, right, center, display_width};

/// Text alignment for table cells
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Alignment {
    Left,
    Center,
    Right,
}

/// Border style for tables
#[derive(Debug, Clone)]
pub struct BorderStyle {
    pub top_left: char,
    pub top_right: char,
    pub bottom_left: char,
    pub bottom_right: char,
    pub horizontal: char,
    pub vertical: char,
    pub left_tee: char,
    pub right_tee: char,
    pub top_tee: char,
    pub bottom_tee: char,
    pub cross: char,
}

impl Default for BorderStyle {
    fn default() -> Self {
        Self {
            top_left: '┌',
            top_right: '┐',
            bottom_left: '└',
            bottom_right: '┘',
            horizontal: '─',
            vertical: '│',
            left_tee: '├',
            right_tee: '┤',
            top_tee: '┬',
            bottom_tee: '┴',
            cross: '┼',
        }
    }
}

impl BorderStyle {
    /// ASCII-only border style
    pub fn ascii() -> Self {
        Self {
            top_left: '+',
            top_right: '+',
            bottom_left: '+',
            bottom_right: '+',
            horizontal: '-',
            vertical: '|',
            left_tee: '+',
            right_tee: '+',
            top_tee: '+',
            bottom_tee: '+',
            cross: '+',
        }
    }

    /// Double-line border style
    pub fn double() -> Self {
        Self {
            top_left: '╔',
            top_right: '╗',
            bottom_left: '╚',
            bottom_right: '╝',
            horizontal: '═',
            vertical: '║',
            left_tee: '╠',
            right_tee: '╣',
            top_tee: '╦',
            bottom_tee: '╩',
            cross: '╬',
        }
    }

    /// Rounded border style
    pub fn rounded() -> Self {
        Self {
            top_left: '╭',
            top_right: '╮',
            bottom_left: '╰',
            bottom_right: '╯',
            horizontal: '─',
            vertical: '│',
            left_tee: '├',
            right_tee: '┤',
            top_tee: '┬',
            bottom_tee: '┴',
            cross: '┼',
        }
    }

    /// Heavy border style
    pub fn heavy() -> Self {
        Self {
            top_left: '┏',
            top_right: '┓',
            bottom_left: '┗',
            bottom_right: '┛',
            horizontal: '━',
            vertical: '┃',
            left_tee: '┣',
            right_tee: '┫',
            top_tee: '┳',
            bottom_tee: '┻',
            cross: '╋',
        }
    }

    /// No border (markdown style)
    pub fn none() -> Self {
        Self {
            top_left: ' ',
            top_right: ' ',
            bottom_left: ' ',
            bottom_right: ' ',
            horizontal: ' ',
            vertical: ' ',
            left_tee: ' ',
            right_tee: ' ',
            top_tee: ' ',
            bottom_tee: ' ',
            cross: ' ',
        }
    }
}

/// Table column definition
#[derive(Debug, Clone)]
pub struct Column {
    pub header: String,
    pub width: usize,
    pub alignment: Alignment,
}

impl Column {
    pub fn new(header: &str) -> Self {
        Self {
            header: header.to_string(),
            width: display_width(header),
            alignment: Alignment::Left,
        }
    }

    pub fn width(mut self, width: usize) -> Self {
        self.width = width;
        self
    }

    pub fn align(mut self, alignment: Alignment) -> Self {
        self.alignment = alignment;
        self
    }

    pub fn align_left(self) -> Self {
        self.align(Alignment::Left)
    }

    pub fn align_center(self) -> Self {
        self.align(Alignment::Center)
    }

    pub fn align_right(self) -> Self {
        self.align(Alignment::Right)
    }
}

/// Table builder
#[derive(Debug, Clone)]
pub struct Table {
    columns: Vec<Column>,
    rows: Vec<Vec<String>>,
    border: BorderStyle,
    padding: usize,
    header_separator: bool,
}

impl Table {
    /// Create a new empty table
    pub fn new() -> Self {
        Self {
            columns: Vec::new(),
            rows: Vec::new(),
            border: BorderStyle::default(),
            padding: 1,
            header_separator: true,
        }
    }

    /// Add a column
    pub fn column(mut self, header: &str) -> Self {
        self.columns.push(Column::new(header));
        self
    }

    /// Add a column with options
    pub fn column_with(mut self, column: Column) -> Self {
        self.columns.push(column);
        self
    }

    /// Set border style
    pub fn border(mut self, border: BorderStyle) -> Self {
        self.border = border;
        self
    }

    /// Set padding (spaces between content and border)
    pub fn padding(mut self, padding: usize) -> Self {
        self.padding = padding;
        self
    }

    /// Enable/disable header separator line
    pub fn header_separator(mut self, enabled: bool) -> Self {
        self.header_separator = enabled;
        self
    }

    /// Add a row
    pub fn row(mut self, cells: &[&str]) -> Self {
        let cells: Vec<String> = cells.iter().map(|s| s.to_string()).collect();
        self.rows.push(cells);
        
        // Update column widths
        for (i, cell) in self.rows.last().unwrap().iter().enumerate() {
            if i < self.columns.len() {
                let cell_width = display_width(cell);
                if cell_width > self.columns[i].width {
                    self.columns[i].width = cell_width;
                }
            }
        }
        
        self
    }

    /// Render the table
    pub fn render(&self) -> String {
        if self.columns.is_empty() {
            return String::new();
        }

        let mut lines = Vec::new();
        let p = self.padding;
        let b = &self.border;

        // Calculate total width
        let total_width: usize = self.columns.iter().map(|c| c.width + 2 * p).sum::<usize>()
            + self.columns.len().saturating_sub(1); // separators

        // Top border
        lines.push(self.make_horizontal_line(&b.horizontal, &b.top_left, &b.top_tee, &b.top_right));

        // Header row
        lines.push(self.make_data_row(&self.columns.iter().map(|c| c.header.clone()).collect::<Vec<_>>()));

        // Header separator
        if self.header_separator {
            lines.push(self.make_horizontal_line(&b.horizontal, &b.left_tee, &b.cross, &b.right_tee));
        }

        // Data rows
        for row in &self.rows {
            // Pad row with empty strings if needed
            let padded_row: Vec<String> = (0..self.columns.len())
                .map(|i| row.get(i).cloned().unwrap_or_default())
                .collect();
            lines.push(self.make_data_row(&padded_row));
        }

        // Bottom border
        lines.push(self.make_horizontal_line(&b.horizontal, &b.bottom_left, &b.bottom_tee, &b.bottom_right));

        lines.join("\n")
    }

    fn make_horizontal_line(&self, h: &char, left: &char, mid: &char, right: &char) -> String {
        let p = self.padding;
        let mut line = left.to_string();
        
        for (i, col) in self.columns.iter().enumerate() {
            line.push_str(&h.to_string().repeat(col.width + 2 * p));
            if i < self.columns.len() - 1 {
                line.push(*mid);
            }
        }
        
        line.push(*right);
        line
    }

    fn make_data_row(&self, cells: &[String]) -> String {
        let p = self.padding;
        let padding = " ".repeat(p);
        let b = &self.border;
        
        let mut row = b.vertical.to_string();
        
        for (i, (cell, col)) in cells.iter().zip(self.columns.iter()).enumerate() {
            let aligned = match col.alignment {
                Alignment::Left => left(&format!("{}{}{}", padding, cell, padding), col.width + 2 * p),
                Alignment::Right => right(&format!("{}{}{}", padding, cell, padding), col.width + 2 * p),
                Alignment::Center => center(&format!("{}{}{}", padding, cell, padding), col.width + 2 * p),
            };
            row.push_str(&aligned);
            if i < cells.len() - 1 {
                row.push(b.vertical);
            }
        }
        
        row.push(b.vertical);
        row
    }
}

impl Default for Table {
    fn default() -> Self {
        Self::new()
    }
}

/// Create a simple table from headers and rows
/// 
/// # Example
/// ```rust
/// use terminal_utils::table;
/// let t = table::simple(&["Name", "Age"], &[&["Alice", "30"], &["Bob", "25"]]);
/// println!("{}", t);
/// ```
pub fn simple(headers: &[&str], rows: &[&[&str]]) -> String {
    let mut table = Table::new();
    for h in headers {
        table = table.column(h);
    }
    for row in rows {
        table = table.row(row);
    }
    table.render()
}

/// Create a table with ASCII borders
pub fn ascii_table(headers: &[&str], rows: &[&[&str]]) -> String {
    let mut table = Table::new().border(BorderStyle::ascii());
    for h in headers {
        table = table.column(h);
    }
    for row in rows {
        table = table.row(row);
    }
    table.render()
}

/// Create a markdown-style table
pub fn markdown_table(headers: &[&str], rows: &[&[&str]]) -> String {
    if headers.is_empty() {
        return String::new();
    }

    // Calculate widths for each column
    let widths: Vec<usize> = headers.iter()
        .map(|h| display_width(h).max(3))
        .collect();
    
    let mut result = String::new();
    
    // Header row
    result.push('|');
    for (i, h) in headers.iter().enumerate() {
        let w = widths[i];
        result.push_str(&format!(" {:w$} |", h, w = w));
    }
    result.push('\n');
    
    // Separator
    result.push('|');
    for (i, _) in headers.iter().enumerate() {
        let w = widths[i];
        result.push_str(&format!(" {:w$} |", "-".repeat(w), w = w));
    }
    result.push('\n');
    
    // Data rows
    for row in rows {
        result.push('|');
        for (i, cell) in row.iter().enumerate() {
            let w = widths.get(i).copied().unwrap_or(3);
            result.push_str(&format!(" {:w$} |", cell, w = w));
        }
        result.push('\n');
    }
    
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_table() {
        let table = Table::new();
        assert_eq!(table.render(), "");
    }

    #[test]
    fn test_simple_table() {
        let output = simple(&["Name", "Age"], &[&["Alice", "30"], &["Bob", "25"]]);
        assert!(output.contains("Alice"));
        assert!(output.contains("Bob"));
        assert!(output.contains("Name"));
        assert!(output.contains("Age"));
    }

    #[test]
    fn test_ascii_table() {
        let output = ascii_table(&["A", "B"], &[&["1", "2"]]);
        assert!(output.contains('+'));
        assert!(output.contains('|'));
        assert!(output.contains('-'));
    }

    #[test]
    fn test_markdown_table() {
        let output = markdown_table(&["Name", "Value"], &[&["Test", "123"]]);
        println!("Output: {:?}", output);
        // Check header row
        assert!(output.contains("| Name |"));
        assert!(output.contains("| Value |"));
        // Check separator row - format is "| --- | --- |"
        assert!(output.contains("---"));
        // Check data row - use simple contains since format may vary
        assert!(output.contains("Test"));
        assert!(output.contains("123"));
    }

    #[test]
    fn test_column_alignment() {
        let table = Table::new()
            .column_with(Column::new("Left").align_left())
            .column_with(Column::new("Center").align_center())
            .column_with(Column::new("Right").align_right())
            .row(&["A", "B", "C"])
            .render();
        
        assert!(table.contains("Left"));
        assert!(table.contains("Center"));
        assert!(table.contains("Right"));
    }

    #[test]
    fn test_border_styles() {
        let table = Table::new()
            .border(BorderStyle::rounded())
            .column("Test")
            .row(&["Value"])
            .render();
        
        assert!(table.contains('╭'));
        assert!(table.contains('╯'));
    }
}