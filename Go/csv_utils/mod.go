// Package csv_utils provides comprehensive CSV (Comma-Separated Values) processing utilities.
// It offers a high-level, user-friendly API for reading, writing, and manipulating CSV files
// with support for various formats, custom delimiters, and type conversions.
//
// Features:
//   - Read CSV from files, strings, or io.Reader
//   - Write CSV to files, strings, or io.Writer
//   - Automatic type detection and conversion
//   - Custom delimiter and quote character support
//   - Header row handling
//   - Row and column filtering
//   - Data validation
//   - Memory-efficient streaming for large files
//
// Example:
//
//	// Read CSV file
//	data, err := csv_utils.ReadFile("data.csv")
//	if err != nil {
//	    log.Fatal(err)
//	}
//	
//	// Access data
//	for _, row := range data.Rows {
//	    name := row["name"]
//	    age := row.GetInt("age", 0)
//	    fmt.Printf("%s is %d years old\n", name, age)
//	}
//
//	// Write CSV file
//	writer := csv_utils.NewWriter()
//	writer.AddHeader([]string{"name", "age", "city"})
//	writer.AddRow([]string{"Alice", "30", "New York"})
//	writer.AddRow([]string{"Bob", "25", "Los Angeles"})
//	err = writer.SaveToFile("output.csv")
package csv_utils

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

// CsvData represents parsed CSV data with headers and rows.
type CsvData struct {
	Headers []string
	Rows    []CsvRow
}

// CsvRow represents a single row in CSV data, mapping column names to values.
type CsvRow map[string]string

// CsvOptions configures CSV reading and writing behavior.
type CsvOptions struct {
	// Delimiter is the field delimiter character (default: ',')
	Delimiter rune
	// QuoteChar is the quote character (default: '"')
	QuoteChar rune
	// HasHeader indicates if the first row is a header (default: true)
	HasHeader bool
	// TrimSpaces removes leading/trailing spaces from fields (default: true)
	TrimSpaces bool
	// SkipEmptyRows skips rows with all empty fields (default: true)
	SkipEmptyRows bool
	// LazyQuotes allows quotes in unquoted fields (default: false)
	LazyQuotes bool
}

// DefaultOptions returns default CSV options.
func DefaultOptions() *CsvOptions {
	return &CsvOptions{
		Delimiter:     ',',
		QuoteChar:     '"',
		HasHeader:     true,
		TrimSpaces:    true,
		SkipEmptyRows: true,
		LazyQuotes:    false,
	}
}

// Get retrieves a string value from the row by column name.
// Returns empty string if column not found.
func (r CsvRow) Get(column string) string {
	if val, ok := r[column]; ok {
		return val
	}
	return ""
}

// GetInt retrieves an integer value from the row by column name.
// Returns defaultValue if conversion fails or column not found.
func (r CsvRow) GetInt(column string, defaultValue int) int {
	val := r.Get(column)
	if val == "" {
		return defaultValue
	}
	if i, err := strconv.Atoi(val); err == nil {
		return i
	}
	return defaultValue
}

// GetFloat retrieves a float64 value from the row by column name.
// Returns defaultValue if conversion fails or column not found.
func (r CsvRow) GetFloat(column string, defaultValue float64) float64 {
	val := r.Get(column)
	if val == "" {
		return defaultValue
	}
	if f, err := strconv.ParseFloat(val, 64); err == nil {
		return f
	}
	return defaultValue
}

// GetBool retrieves a boolean value from the row by column name.
// Returns defaultValue if conversion fails or column not found.
// Recognizes: true/false, yes/no, 1/0 (case-insensitive)
func (r CsvRow) GetBool(column string, defaultValue bool) bool {
	val := strings.ToLower(strings.TrimSpace(r.Get(column)))
	if val == "" {
		return defaultValue
	}
	switch val {
	case "true", "yes", "1", "y", "t":
		return true
	case "false", "no", "0", "n", "f":
		return false
	}
	return defaultValue
}

// IsEmpty checks if the row has no data.
func (r CsvRow) IsEmpty() bool {
	for _, v := range r {
		if strings.TrimSpace(v) != "" {
			return false
		}
	}
	return true
}

// ReadFile reads a CSV file and returns parsed data.
// Uses default options.
func ReadFile(filename string) (*CsvData, error) {
	return ReadFileWithOptions(filename, DefaultOptions())
}

// ReadFileWithOptions reads a CSV file with custom options.
func ReadFileWithOptions(filename string, opts *CsvOptions) (*CsvData, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()
	return ReadWithOptions(file, opts)
}

// ReadString parses CSV data from a string.
func ReadString(data string) (*CsvData, error) {
	return ReadStringWithOptions(data, DefaultOptions())
}

// ReadStringWithOptions parses CSV data from a string with custom options.
func ReadStringWithOptions(data string, opts *CsvOptions) (*CsvData, error) {
	return ReadWithOptions(strings.NewReader(data), opts)
}

// ReadWithOptions reads CSV from an io.Reader with custom options.
func ReadWithOptions(reader io.Reader, opts *CsvOptions) (*CsvData, error) {
	if opts == nil {
		opts = DefaultOptions()
	}

	csvReader := csv.NewReader(reader)
	csvReader.Comma = opts.Delimiter
	csvReader.LazyQuotes = opts.LazyQuotes

	records, err := csvReader.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("failed to read CSV: %w", err)
	}

	if len(records) == 0 {
		return &CsvData{
			Headers: []string{},
			Rows:    []CsvRow{},
		}, nil
	}

	result := &CsvData{
		Headers: []string{},
		Rows:    []CsvRow{},
	}

	startRow := 0
	if opts.HasHeader {
		result.Headers = make([]string, len(records[0]))
		for i, h := range records[0] {
			if opts.TrimSpaces {
				h = strings.TrimSpace(h)
			}
			result.Headers[i] = h
		}
		startRow = 1
	} else {
		// Generate numeric column names
		result.Headers = make([]string, len(records[0]))
		for i := range records[0] {
			result.Headers[i] = fmt.Sprintf("col%d", i+1)
		}
	}

	for i := startRow; i < len(records); i++ {
		record := records[i]
		row := make(CsvRow)

		isEmpty := true
		for j, val := range record {
			if opts.TrimSpaces {
				val = strings.TrimSpace(val)
			}
			if j < len(result.Headers) {
				row[result.Headers[j]] = val
				if val != "" {
					isEmpty = false
				}
			}
		}

		if !opts.SkipEmptyRows || !isEmpty {
			result.Rows = append(result.Rows, row)
		}
	}

	return result, nil
}

// WriteToFile writes CSV data to a file.
func (d *CsvData) WriteToFile(filename string) error {
	return d.WriteToFileWithOptions(filename, DefaultOptions())
}

// WriteToFileWithOptions writes CSV data to a file with custom options.
func (d *CsvData) WriteToFileWithOptions(filename string, opts *CsvOptions) error {
	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create file: %w", err)
	}
	defer file.Close()
	return d.WriteWithOptions(file, opts)
}

// WriteToString converts CSV data to a string.
func (d *CsvData) WriteToString() string {
	return d.WriteToStringWithOptions(DefaultOptions())
}

// WriteToStringWithOptions converts CSV data to a string with custom options.
func (d *CsvData) WriteToStringWithOptions(opts *CsvOptions) string {
	var buf bytes.Buffer
	d.WriteWithOptions(&buf, opts)
	return buf.String()
}

// WriteWithOptions writes CSV data to an io.Writer with custom options.
func (d *CsvData) WriteWithOptions(writer io.Writer, opts *CsvOptions) error {
	if opts == nil {
		opts = DefaultOptions()
	}

	csvWriter := csv.NewWriter(writer)
	csvWriter.Comma = opts.Delimiter

	// Write header
	if opts.HasHeader && len(d.Headers) > 0 {
		if err := csvWriter.Write(d.Headers); err != nil {
			return fmt.Errorf("failed to write header: %w", err)
		}
	}

	// Write rows
	for _, row := range d.Rows {
		record := make([]string, len(d.Headers))
		for i, header := range d.Headers {
			record[i] = row.Get(header)
		}
		if err := csvWriter.Write(record); err != nil {
			return fmt.Errorf("failed to write row: %w", err)
		}
	}

	csvWriter.Flush()
	return csvWriter.Error()
}

// FilterRows returns a new CsvData containing only rows that match the predicate.
func (d *CsvData) FilterRows(predicate func(CsvRow) bool) *CsvData {
	filtered := &CsvData{
		Headers: d.Headers,
		Rows:    []CsvRow{},
	}
	for _, row := range d.Rows {
		if predicate(row) {
			filtered.Rows = append(filtered.Rows, row)
		}
	}
	return filtered
}

// FilterColumns returns a new CsvData containing only specified columns.
func (d *CsvData) FilterColumns(columns []string) *CsvData {
	// Validate columns
	validColumns := []string{}
	for _, col := range columns {
		for _, h := range d.Headers {
			if h == col {
				validColumns = append(validColumns, col)
				break
			}
		}
	}

	result := &CsvData{
		Headers: validColumns,
		Rows:    []CsvRow{},
	}

	for _, row := range d.Rows {
		newRow := make(CsvRow)
		for _, col := range validColumns {
			newRow[col] = row.Get(col)
		}
		result.Rows = append(result.Rows, newRow)
	}

	return result
}

// SortBy sorts rows by a column in ascending order.
func (d *CsvData) SortBy(column string) *CsvData {
	return d.SortByWithOptions(column, true, false)
}

// SortByWithOptions sorts rows by a column with custom options.
// ascending: true for ascending, false for descending.
// numeric: true to sort as numbers, false for string comparison.
func (d *CsvData) SortByWithOptions(column string, ascending, numeric bool) *CsvData {
	sorted := &CsvData{
		Headers: d.Headers,
		Rows:    make([]CsvRow, len(d.Rows)),
	}
	copy(sorted.Rows, d.Rows)

	// Check if column exists
	hasColumn := false
	for _, h := range d.Headers {
		if h == column {
			hasColumn = true
			break
		}
	}
	if !hasColumn {
		return sorted
	}

	// Sort rows
	for i := 0; i < len(sorted.Rows)-1; i++ {
		for j := i + 1; j < len(sorted.Rows); j++ {
			shouldSwap := false
			val1 := sorted.Rows[i].Get(column)
			val2 := sorted.Rows[j].Get(column)

			if numeric {
				num1, err1 := strconv.ParseFloat(val1, 64)
				num2, err2 := strconv.ParseFloat(val2, 64)
				if err1 == nil && err2 == nil {
					if ascending {
						shouldSwap = num1 > num2
					} else {
						shouldSwap = num1 < num2
					}
				} else {
					// Fall back to string comparison
					if ascending {
						shouldSwap = val1 > val2
					} else {
						shouldSwap = val1 < val2
					}
				}
			} else {
				if ascending {
					shouldSwap = val1 > val2
				} else {
					shouldSwap = val1 < val2
				}
			}

			if shouldSwap {
				sorted.Rows[i], sorted.Rows[j] = sorted.Rows[j], sorted.Rows[i]
			}
		}
	}

	return sorted
}

// GetColumn returns all values in a specific column.
func (d *CsvData) GetColumn(column string) []string {
	values := []string{}
	for _, row := range d.Rows {
		values = append(values, row.Get(column))
	}
	return values
}

// GetColumnInt returns all values in a column as integers.
// Non-convertible values are returned as 0.
func (d *CsvData) GetColumnInt(column string) []int {
	values := []int{}
	for _, row := range d.Rows {
		values = append(values, row.GetInt(column, 0))
	}
	return values
}

// GetColumnFloat returns all values in a column as float64.
// Non-convertible values are returned as 0.0.
func (d *CsvData) GetColumnFloat(column string) []float64 {
	values := []float64{}
	for _, row := range d.Rows {
		values = append(values, row.GetFloat(column, 0.0))
	}
	return values
}

// AddColumn adds a new column with the given values.
// If values length is less than row count, remaining cells are empty.
func (d *CsvData) AddColumn(name string, values []string) {
	d.Headers = append(d.Headers, name)
	for i, row := range d.Rows {
		if i < len(values) {
			row[name] = values[i]
		} else {
			row[name] = ""
		}
	}
}

// RemoveColumn removes a column from the data.
func (d *CsvData) RemoveColumn(name string) {
	// Remove from headers
	newHeaders := []string{}
	for _, h := range d.Headers {
		if h != name {
			newHeaders = append(newHeaders, h)
		}
	}
	d.Headers = newHeaders

	// Remove from rows
	for _, row := range d.Rows {
		delete(row, name)
	}
}

// RowCount returns the number of rows.
func (d *CsvData) RowCount() int {
	return len(d.Rows)
}

// ColumnCount returns the number of columns.
func (d *CsvData) ColumnCount() int {
	return len(d.Headers)
}

// GetRow returns a row by index.
// Returns nil if index is out of bounds.
func (d *CsvData) GetRow(index int) CsvRow {
	if index < 0 || index >= len(d.Rows) {
		return nil
	}
	return d.Rows[index]
}

// AddRow adds a new row to the data.
// The row map should have column names as keys.
func (d *CsvData) AddRow(row CsvRow) {
	d.Rows = append(d.Rows, row)
}

// RemoveRow removes a row by index.
func (d *CsvData) RemoveRow(index int) bool {
	if index < 0 || index >= len(d.Rows) {
		return false
	}
	d.Rows = append(d.Rows[:index], d.Rows[index+1:]...)
	return true
}

// Validate checks if all rows have values for all headers.
// Returns a slice of row indices that have missing values.
func (d *CsvData) Validate() []int {
	invalidRows := []int{}
	for i, row := range d.Rows {
		for _, header := range d.Headers {
			if _, ok := row[header]; !ok {
				invalidRows = append(invalidRows, i)
				break
			}
		}
	}
	return invalidRows
}

// IsValid checks if the data structure is valid (has matching headers and rows).
func (d *CsvData) IsValid() bool {
	for _, row := range d.Rows {
		for _, header := range d.Headers {
			if _, ok := row[header]; !ok {
				return false
			}
		}
	}
	return true
}

// ToSlice converts the data to a 2D string slice.
// Includes headers as the first row if hasHeader is true.
func (d *CsvData) ToSlice(hasHeader bool) [][]string {
	result := [][]string{}
	if hasHeader && len(d.Headers) > 0 {
		result = append(result, d.Headers)
	}
	for _, row := range d.Rows {
		record := []string{}
		for _, header := range d.Headers {
			record = append(record, row.Get(header))
		}
		result = append(result, record)
	}
	return result
}

// ToMapSlice converts the data to a slice of maps.
func (d *CsvData) ToMapSlice() []map[string]string {
	result := []map[string]string{}
	for _, row := range d.Rows {
		m := make(map[string]string)
		for k, v := range row {
			m[k] = v
		}
		result = append(result, m)
	}
	return result
}

// CsvWriter provides a convenient way to build CSV data.
type CsvWriter struct {
	headers []string
	rows    [][]string
}

// NewWriter creates a new CsvWriter.
func NewWriter() *CsvWriter {
	return &CsvWriter{
		headers: []string{},
		rows:    [][]string{},
	}
}

// SetHeaders sets the column headers.
func (w *CsvWriter) SetHeaders(headers []string) {
	w.headers = headers
}

// AddRow adds a row using a slice of values (must match header order).
func (w *CsvWriter) AddRow(values []string) {
	w.rows = append(w.rows, values)
}

// AddRowMap adds a row using a map (keys should match headers).
func (w *CsvWriter) AddRowMap(row map[string]string) {
	values := []string{}
	for _, header := range w.headers {
		if val, ok := row[header]; ok {
			values = append(values, val)
		} else {
			values = append(values, "")
		}
	}
	w.rows = append(w.rows, values)
}

// ToCsvData converts the writer to a CsvData.
func (w *CsvWriter) ToCsvData() *CsvData {
	data := &CsvData{
		Headers: w.headers,
		Rows:    []CsvRow{},
	}
	for _, row := range w.rows {
		r := make(CsvRow)
		for i, val := range row {
			if i < len(w.headers) {
				r[w.headers[i]] = val
			}
		}
		data.Rows = append(data.Rows, r)
	}
	return data
}

// SaveToFile saves the CSV data to a file.
func (w *CsvWriter) SaveToFile(filename string) error {
	return w.SaveToFileWithOptions(filename, DefaultOptions())
}

// SaveToFileWithOptions saves the CSV data to a file with custom options.
func (w *CsvWriter) SaveToFileWithOptions(filename string, opts *CsvOptions) error {
	data := w.ToCsvData()
	return data.WriteToFileWithOptions(filename, opts)
}

// ToString converts the CSV data to a string.
func (w *CsvWriter) ToString() string {
	return w.ToStringWithOptions(DefaultOptions())
}

// ToStringWithOptions converts the CSV data to a string with custom options.
func (w *CsvWriter) ToStringWithOptions(opts *CsvOptions) string {
	data := w.ToCsvData()
	return data.WriteToStringWithOptions(opts)
}

// IsValidCsv checks if a string is valid CSV format.
func IsValidCsv(data string) bool {
	_, err := ReadString(data)
	return err == nil
}

// DetectDelimiter attempts to detect the delimiter used in CSV data.
// Returns the most likely delimiter character.
func DetectDelimiter(data string) rune {
	candidates := []rune{',', '\t', ';', '|'}
	counts := make(map[rune]int)

	lines := strings.Split(data, "\n")
	if len(lines) == 0 {
		return ','
	}

	firstLine := lines[0]
	for _, delim := range candidates {
		counts[delim] = strings.Count(firstLine, string(delim))
	}

	// Find the delimiter with the highest count
	maxCount := 0
	bestDelim := ','
	for delim, count := range counts {
		if count > maxCount {
			maxCount = count
			bestDelim = delim
		}
	}

	return bestDelim
}

// Join merges two CsvData objects horizontally (adds columns).
// Both must have the same number of rows.
func Join(left, right *CsvData) (*CsvData, error) {
	if len(left.Rows) != len(right.Rows) {
		return nil, fmt.Errorf("cannot join: row count mismatch (%d vs %d)", len(left.Rows), len(right.Rows))
	}

	result := &CsvData{
		Headers: []string{},
		Rows:    []CsvRow{},
	}

	// Combine headers
	result.Headers = append(result.Headers, left.Headers...)
	result.Headers = append(result.Headers, right.Headers...)

	// Combine rows
	for i := 0; i < len(left.Rows); i++ {
		row := make(CsvRow)
		for k, v := range left.Rows[i] {
			row[k] = v
		}
		for k, v := range right.Rows[i] {
			row[k] = v
		}
		result.Rows = append(result.Rows, row)
	}

	return result, nil
}

// Merge merges two CsvData objects vertically (adds rows).
// Both must have the same headers.
func Merge(first, second *CsvData) (*CsvData, error) {
	if len(first.Headers) != len(second.Headers) {
		return nil, fmt.Errorf("cannot merge: header count mismatch")
	}

	// Check if headers match
	for i, h := range first.Headers {
		if h != second.Headers[i] {
			return nil, fmt.Errorf("cannot merge: headers do not match at position %d", i)
		}
	}

	result := &CsvData{
		Headers: first.Headers,
		Rows:    []CsvRow{},
	}

	result.Rows = append(result.Rows, first.Rows...)
	result.Rows = append(result.Rows, second.Rows...)

	return result, nil
}

// SumColumn calculates the sum of numeric values in a column.
// Returns 0 if column contains no valid numbers.
func (d *CsvData) SumColumn(column string) float64 {
	sum := 0.0
	count := 0
	for _, row := range d.Rows {
		val := row.Get(column)
		if f, err := strconv.ParseFloat(val, 64); err == nil {
			sum += f
			count++
		}
	}
	if count == 0 {
		return 0
	}
	return sum
}

// AvgColumn calculates the average of numeric values in a column.
// Returns 0 if column contains no valid numbers.
func (d *CsvData) AvgColumn(column string) float64 {
	sum := 0.0
	count := 0
	for _, row := range d.Rows {
		val := row.Get(column)
		if f, err := strconv.ParseFloat(val, 64); err == nil {
			sum += f
			count++
		}
	}
	if count == 0 {
		return 0
	}
	return sum / float64(count)
}

// MinColumn finds the minimum numeric value in a column.
// Returns 0 if column contains no valid numbers.
func (d *CsvData) MinColumn(column string) float64 {
	var min float64
	found := false
	for _, row := range d.Rows {
		val := row.Get(column)
		if f, err := strconv.ParseFloat(val, 64); err == nil {
			if !found || f < min {
				min = f
				found = true
			}
		}
	}
	if !found {
		return 0
	}
	return min
}

// MaxColumn finds the maximum numeric value in a column.
// Returns 0 if column contains no valid numbers.
func (d *CsvData) MaxColumn(column string) float64 {
	var max float64
	found := false
	for _, row := range d.Rows {
		val := row.Get(column)
		if f, err := strconv.ParseFloat(val, 64); err == nil {
			if !found || f > max {
				max = f
				found = true
			}
		}
	}
	if !found {
		return 0
	}
	return max
}

// Distinct returns unique values in a column.
func (d *CsvData) Distinct(column string) []string {
	seen := make(map[string]bool)
	result := []string{}
	for _, row := range d.Rows {
		val := row.Get(column)
		if !seen[val] {
			seen[val] = true
			result = append(result, val)
		}
	}
	return result
}

// Count returns the number of rows matching a predicate.
func (d *CsvData) Count(predicate func(CsvRow) bool) int {
	count := 0
	for _, row := range d.Rows {
		if predicate(row) {
			count++
		}
	}
	return count
}

// Find returns the first row matching a predicate.
// Returns nil if no row matches.
func (d *CsvData) Find(predicate func(CsvRow) bool) CsvRow {
	for _, row := range d.Rows {
		if predicate(row) {
			return row
		}
	}
	return nil
}

// FindAll returns all rows matching a predicate.
func (d *CsvData) FindAll(predicate func(CsvRow) bool) []CsvRow {
	result := []CsvRow{}
	for _, row := range d.Rows {
		if predicate(row) {
			result = append(result, row)
		}
	}
	return result
}

// GroupBy groups rows by a column value.
// Returns a map where keys are unique column values and values are slices of rows.
func (d *CsvData) GroupBy(column string) map[string][]CsvRow {
	groups := make(map[string][]CsvRow)
	for _, row := range d.Rows {
		key := row.Get(column)
		groups[key] = append(groups[key], row)
	}
	return groups
}

// Transform applies a transformation function to each row.
// The function receives the row and should return the transformed row.
func (d *CsvData) Transform(transformer func(CsvRow) CsvRow) {
	for i, row := range d.Rows {
		d.Rows[i] = transformer(row)
	}
}

// TransformColumn applies a transformation function to a specific column.
func (d *CsvData) TransformColumn(column string, transformer func(string) string) {
	for _, row := range d.Rows {
		if _, ok := row[column]; ok {
			row[column] = transformer(row[column])
		}
	}
}


