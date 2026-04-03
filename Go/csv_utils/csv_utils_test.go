package csv_utils

import (
	"strings"
	"testing"
)

// TestReadString tests reading CSV from string
func TestReadString(t *testing.T) {
	csvData := `name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago`

	data, err := ReadString(csvData)
	if err != nil {
		t.Fatalf("Failed to read CSV: %v", err)
	}

	if len(data.Headers) != 3 {
		t.Errorf("Expected 3 headers, got %d", len(data.Headers))
	}

	if len(data.Rows) != 3 {
		t.Errorf("Expected 3 rows, got %d", len(data.Rows))
	}

	// Check first row
	row := data.Rows[0]
	if row.Get("name") != "Alice" {
		t.Errorf("Expected name 'Alice', got '%s'", row.Get("name"))
	}
	if row.GetInt("age", 0) != 30 {
		t.Errorf("Expected age 30, got %d", row.GetInt("age", 0))
	}
}

// TestReadStringNoHeader tests reading CSV without header
func TestReadStringNoHeader(t *testing.T) {
	csvData := `Alice,30,New York
Bob,25,Los Angeles`

	opts := DefaultOptions()
	opts.HasHeader = false
	data, err := ReadStringWithOptions(csvData, opts)
	if err != nil {
		t.Fatalf("Failed to read CSV: %v", err)
	}

	if len(data.Headers) != 3 {
		t.Errorf("Expected 3 auto-generated headers, got %d", len(data.Headers))
	}

	if data.Headers[0] != "col1" {
		t.Errorf("Expected header 'col1', got '%s'", data.Headers[0])
	}
}

// TestReadStringCustomDelimiter tests reading CSV with custom delimiter
func TestReadStringCustomDelimiter(t *testing.T) {
	csvData := `name;age;city
Alice;30;New York
Bob;25;Los Angeles`

	opts := DefaultOptions()
	opts.Delimiter = ';'
	data, err := ReadStringWithOptions(csvData, opts)
	if err != nil {
		t.Fatalf("Failed to read CSV: %v", err)
	}

	if data.Rows[0].Get("name") != "Alice" {
		t.Errorf("Expected name 'Alice', got '%s'", data.Rows[0].Get("name"))
	}
}

// TestWriteToString tests writing CSV to string
func TestWriteToString(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age", "city"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30", "city": "New York"},
			{"name": "Bob", "age": "25", "city": "Los Angeles"},
		},
	}

	result := data.WriteToString()
	if !strings.Contains(result, "name,age,city") {
		t.Error("Expected header in output")
	}
	if !strings.Contains(result, "Alice,30,New York") {
		t.Error("Expected Alice row in output")
	}
}

// TestCsvRowGetInt tests integer conversion
func TestCsvRowGetInt(t *testing.T) {
	row := CsvRow{"value": "42", "invalid": "abc"}

	if row.GetInt("value", 0) != 42 {
		t.Errorf("Expected 42, got %d", row.GetInt("value", 0))
	}

	if row.GetInt("invalid", 99) != 99 {
		t.Errorf("Expected default 99, got %d", row.GetInt("invalid", 99))
	}

	if row.GetInt("missing", -1) != -1 {
		t.Errorf("Expected default -1, got %d", row.GetInt("missing", -1))
	}
}

// TestCsvRowGetFloat tests float conversion
func TestCsvRowGetFloat(t *testing.T) {
	row := CsvRow{"value": "3.14", "invalid": "abc"}

	if row.GetFloat("value", 0.0) != 3.14 {
		t.Errorf("Expected 3.14, got %f", row.GetFloat("value", 0.0))
	}

	if row.GetFloat("invalid", 1.0) != 1.0 {
		t.Errorf("Expected default 1.0, got %f", row.GetFloat("invalid", 1.0))
	}
}

// TestCsvRowGetBool tests boolean conversion
func TestCsvRowGetBool(t *testing.T) {
	row := CsvRow{
		"true1":  "true",
		"true2":  "yes",
		"true3":  "1",
		"false1": "false",
		"false2": "no",
		"false3": "0",
	}

	if !row.GetBool("true1", false) {
		t.Error("Expected true for 'true'")
	}
	if !row.GetBool("true2", false) {
		t.Error("Expected true for 'yes'")
	}
	if !row.GetBool("true3", false) {
		t.Error("Expected true for '1'")
	}
	if row.GetBool("false1", true) {
		t.Error("Expected false for 'false'")
	}
	if row.GetBool("false2", true) {
		t.Error("Expected false for 'no'")
	}
	if row.GetBool("false3", true) {
		t.Error("Expected false for '0'")
	}
}

// TestFilterRows tests row filtering
func TestFilterRows(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30"},
			{"name": "Bob", "age": "25"},
			{"name": "Charlie", "age": "35"},
		},
	}

	filtered := data.FilterRows(func(row CsvRow) bool {
		return row.GetInt("age", 0) > 25
	})

	if len(filtered.Rows) != 2 {
		t.Errorf("Expected 2 filtered rows, got %d", len(filtered.Rows))
	}
}

// TestFilterColumns tests column filtering
func TestFilterColumns(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age", "city"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30", "city": "New York"},
		},
	}

	filtered := data.FilterColumns([]string{"name", "city"})

	if len(filtered.Headers) != 2 {
		t.Errorf("Expected 2 columns, got %d", len(filtered.Headers))
	}

	if _, ok := filtered.Rows[0]["age"]; ok {
		t.Error("Age column should have been removed")
	}
}

// TestSortBy tests sorting
func TestSortBy(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Charlie", "age": "35"},
			{"name": "Alice", "age": "30"},
			{"name": "Bob", "age": "25"},
		},
	}

	sorted := data.SortBy("name")

	if sorted.Rows[0].Get("name") != "Alice" {
		t.Errorf("Expected first row to be Alice, got %s", sorted.Rows[0].Get("name"))
	}
	if sorted.Rows[1].Get("name") != "Bob" {
		t.Errorf("Expected second row to be Bob, got %s", sorted.Rows[1].Get("name"))
	}
}

// TestSortByNumeric tests numeric sorting
func TestSortByNumeric(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Charlie", "age": "100"},
			{"name": "Alice", "age": "5"},
			{"name": "Bob", "age": "50"},
		},
	}

	sorted := data.SortByWithOptions("age", true, true)

	if sorted.Rows[0].GetInt("age", 0) != 5 {
		t.Errorf("Expected first age to be 5, got %d", sorted.Rows[0].GetInt("age", 0))
	}
	if sorted.Rows[1].GetInt("age", 0) != 50 {
		t.Errorf("Expected second age to be 50, got %d", sorted.Rows[1].GetInt("age", 0))
	}
}

// TestGetColumn tests getting column values
func TestGetColumn(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30"},
			{"name": "Bob", "age": "25"},
		},
	}

	names := data.GetColumn("name")
	if len(names) != 2 {
		t.Errorf("Expected 2 names, got %d", len(names))
	}
	if names[0] != "Alice" {
		t.Errorf("Expected first name to be Alice, got %s", names[0])
	}
}

// TestAddRemoveColumn tests adding and removing columns
func TestAddRemoveColumn(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
			{"name": "Bob"},
		},
	}

	data.AddColumn("age", []string{"30", "25"})

	if len(data.Headers) != 2 {
		t.Errorf("Expected 2 headers after add, got %d", len(data.Headers))
	}

	if data.Rows[0].Get("age") != "30" {
		t.Errorf("Expected age 30, got %s", data.Rows[0].Get("age"))
	}

	data.RemoveColumn("age")

	if len(data.Headers) != 1 {
		t.Errorf("Expected 1 header after remove, got %d", len(data.Headers))
	}
}

// TestAddRemoveRow tests adding and removing rows
func TestAddRemoveRow(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
		},
	}

	data.AddRow(CsvRow{"name": "Bob"})

	if len(data.Rows) != 2 {
		t.Errorf("Expected 2 rows after add, got %d", len(data.Rows))
	}

	if !data.RemoveRow(0) {
		t.Error("RemoveRow should return true for valid index")
	}

	if len(data.Rows) != 1 {
		t.Errorf("Expected 1 row after remove, got %d", len(data.Rows))
	}

	if data.RemoveRow(10) {
		t.Error("RemoveRow should return false for invalid index")
	}
}

// TestValidate tests data validation
func TestValidate(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30"},
			{"name": "Bob"}, // Missing age
		},
	}

	invalid := data.Validate()
	if len(invalid) != 1 {
		t.Errorf("Expected 1 invalid row, got %d", len(invalid))
	}

	if invalid[0] != 1 {
		t.Errorf("Expected invalid row index 1, got %d", invalid[0])
	}
}

// TestStatistics tests column statistics
func TestStatistics(t *testing.T) {
	data := &CsvData{
		Headers: []string{"value"},
		Rows: []CsvRow{
			{"value": "10"},
			{"value": "20"},
			{"value": "30"},
		},
	}

	if data.SumColumn("value") != 60 {
		t.Errorf("Expected sum 60, got %f", data.SumColumn("value"))
	}

	if data.AvgColumn("value") != 20 {
		t.Errorf("Expected avg 20, got %f", data.AvgColumn("value"))
	}

	if data.MinColumn("value") != 10 {
		t.Errorf("Expected min 10, got %f", data.MinColumn("value"))
	}

	if data.MaxColumn("value") != 30 {
		t.Errorf("Expected max 30, got %f", data.MaxColumn("value"))
	}
}

// TestDistinct tests distinct values
func TestDistinct(t *testing.T) {
	data := &CsvData{
		Headers: []string{"category"},
		Rows: []CsvRow{
			{"category": "A"},
			{"category": "B"},
			{"category": "A"},
			{"category": "C"},
		},
	}

	distinct := data.Distinct("category")
	if len(distinct) != 3 {
		t.Errorf("Expected 3 distinct values, got %d", len(distinct))
	}
}

// TestGroupBy tests grouping
func TestGroupBy(t *testing.T) {
	data := &CsvData{
		Headers: []string{"category", "value"},
		Rows: []CsvRow{
			{"category": "A", "value": "1"},
			{"category": "B", "value": "2"},
			{"category": "A", "value": "3"},
		},
	}

	groups := data.GroupBy("category")
	if len(groups) != 2 {
		t.Errorf("Expected 2 groups, got %d", len(groups))
	}

	if len(groups["A"]) != 2 {
		t.Errorf("Expected 2 items in group A, got %d", len(groups["A"]))
	}
}

// TestFind tests finding rows
func TestFind(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30"},
			{"name": "Bob", "age": "25"},
		},
	}

	row := data.Find(func(r CsvRow) bool {
		return r.Get("name") == "Bob"
	})

	if row == nil {
		t.Error("Expected to find Bob")
	} else if row.Get("age") != "25" {
		t.Errorf("Expected age 25, got %s", row.Get("age"))
	}

	notFound := data.Find(func(r CsvRow) bool {
		return r.Get("name") == "Charlie"
	})

	if notFound != nil {
		t.Error("Expected nil for non-existent name")
	}
}

// TestCount tests counting rows
func TestCount(t *testing.T) {
	data := &CsvData{
		Headers: []string{"age"},
		Rows: []CsvRow{
			{"age": "30"},
			{"age": "25"},
			{"age": "35"},
		},
	}

	count := data.Count(func(r CsvRow) bool {
		return r.GetInt("age", 0) > 25
	})

	if count != 2 {
		t.Errorf("Expected count 2, got %d", count)
	}
}

// TestCsvWriter tests the CsvWriter
func TestCsvWriter(t *testing.T) {
	writer := NewWriter()
	writer.SetHeaders([]string{"name", "age"})
	writer.AddRow([]string{"Alice", "30"})
	writer.AddRow([]string{"Bob", "25"})

	data := writer.ToCsvData()
	if len(data.Rows) != 2 {
		t.Errorf("Expected 2 rows, got %d", len(data.Rows))
	}

	result := writer.ToString()
	if !strings.Contains(result, "Alice,30") {
		t.Error("Expected Alice row in output")
	}
}

// TestDetectDelimiter tests delimiter detection
func TestDetectDelimiter(t *testing.T) {
	tests := []struct {
		input     string
		expected  rune
	}{
		{"a,b,c", ','},
		{"a;b;c", ';'},
		{"a\tb\tc", '\t'},
		{"a|b|c", '|'},
	}

	for _, test := range tests {
		delim := DetectDelimiter(test.input)
		if delim != test.expected {
			t.Errorf("For input '%s', expected delimiter %c, got %c", test.input, test.expected, delim)
		}
	}
}

// TestIsValidCsv tests CSV validation
func TestIsValidCsv(t *testing.T) {
	if !IsValidCsv("a,b\n1,2") {
		t.Error("Expected valid CSV")
	}

	// Empty string is valid (produces empty data)
	if !IsValidCsv("") {
		t.Error("Empty string should be valid CSV")
	}
}

// TestJoin tests horizontal merge
func TestJoin(t *testing.T) {
	left := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
			{"name": "Bob"},
		},
	}

	right := &CsvData{
		Headers: []string{"age"},
		Rows: []CsvRow{
			{"age": "30"},
			{"age": "25"},
		},
	}

	joined, err := Join(left, right)
	if err != nil {
		t.Fatalf("Join failed: %v", err)
	}

	if len(joined.Headers) != 2 {
		t.Errorf("Expected 2 headers, got %d", len(joined.Headers))
	}

	if joined.Rows[0].Get("name") != "Alice" || joined.Rows[0].Get("age") != "30" {
		t.Error("Join did not combine rows correctly")
	}
}

// TestMerge tests vertical merge
func TestMerge(t *testing.T) {
	first := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
		},
	}

	second := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Bob"},
		},
	}

	merged, err := Merge(first, second)
	if err != nil {
		t.Fatalf("Merge failed: %v", err)
	}

	if len(merged.Rows) != 2 {
		t.Errorf("Expected 2 rows, got %d", len(merged.Rows))
	}
}

// TestTransform tests row transformation
func TestTransform(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "alice"},
			{"name": "bob"},
		},
	}

	data.Transform(func(row CsvRow) CsvRow {
		row["name"] = strings.ToUpper(row["name"])
		return row
	})

	if data.Rows[0].Get("name") != "ALICE" {
		t.Errorf("Expected ALICE, got %s", data.Rows[0].Get("name"))
	}
}

// TestTransformColumn tests column transformation
func TestTransformColumn(t *testing.T) {
	data := &CsvData{
		Headers: []string{"value"},
		Rows: []CsvRow{
			{"value": "hello"},
			{"value": "world"},
		},
	}

	data.TransformColumn("value", func(s string) string {
		return strings.ToUpper(s)
	})

	if data.Rows[0].Get("value") != "HELLO" {
		t.Errorf("Expected HELLO, got %s", data.Rows[0].Get("value"))
	}
}

// TestEmptyData tests handling of empty data
func TestEmptyData(t *testing.T) {
	data := &CsvData{
		Headers: []string{},
		Rows:    []CsvRow{},
	}

	if data.RowCount() != 0 {
		t.Errorf("Expected 0 rows, got %d", data.RowCount())
	}

	if data.ColumnCount() != 0 {
		t.Errorf("Expected 0 columns, got %d", data.ColumnCount())
	}

	result := data.WriteToString()
	if result != "" {
		t.Errorf("Expected empty string, got '%s'", result)
	}
}

// TestSkipEmptyRows tests skipping empty rows
func TestSkipEmptyRows(t *testing.T) {
	csvData := `name,age
Alice,30

Bob,25
`

	data, err := ReadString(csvData)
	if err != nil {
		t.Fatalf("Failed to read CSV: %v", err	}

	// By default, empty rows are skipped
	if len(data.Rows) != 2 {
		t.Errorf("Expected 2 rows (empty row skipped), got %d", len(data.Rows))
	}
}

// TestTrimSpaces tests space trimming
func TestTrimSpaces(t *testing.T) {
	csvData := `name , age
 Alice , 30 
Bob,25`

	data, err := ReadString(csvData)
	if err != nil {
		t.Fatalf("Failed to read CSV: %v", err)
	}

	// Headers should be trimmed
	if data.Headers[0] != "name" {
		t.Errorf("Expected header '"name"', got '"%s"'", data.Headers[0])
	}

	// Values should be trimmed
	if data.Rows[0].Get("name") != "Alice" {
		t.Errorf("Expected name '"Alice"', got '"%s"'", data.Rows[0].Get("name"))
	}
}

// TestToSlice tests conversion to slice
func TestToSlice(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Alice", "age": "30"},
		},
	}

	slice := data.ToSlice(true)
	if len(slice) != 2 { // header + 1 row
		t.Errorf("Expected 2 slices, got %d", len(slice))
	}

	if slice[0][0] != "name" {
		t.Errorf("Expected first header '"name"', got '"%s"'", slice[0][0])
	}

	if slice[1][0] != "Alice" {
		t.Errorf("Expected first value '"Alice"', got '"%s"'", slice[1][0])
	}
}

// TestToMapSlice tests conversion to map slice
func TestToMapSlice(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
		},
	}

	maps := data.ToMapSlice()
	if len(maps) != 1 {
		t.Errorf("Expected 1 map, got %d", len(maps))
	}

	if maps[0]["name"] != "Alice" {
		t.Errorf("Expected name '"Alice"', got '"%s"'", maps[0]["name"])
	}
}

// TestCsvRowIsEmpty tests empty row detection
func TestCsvRowIsEmpty(t *testing.T) {
	emptyRow := CsvRow{"a": "", "b": "  "}
	if !emptyRow.IsEmpty() {
		t.Error("Expected row to be empty")
	}

	nonEmptyRow := CsvRow{"a": "", "b": "value"}
	if nonEmptyRow.IsEmpty() {
		t.Error("Expected row to not be empty")
	}
}

// TestFindAll tests finding all matching rows
func TestFindAll(t *testing.T) {
	data := &CsvData{
		Headers: []string{"age"},
		Rows: []CsvRow{
			{"age": "30"},
			{"age": "25"},
			{"age": "35"},
		},
	}

	found := data.FindAll(func(r CsvRow) bool {
		return r.GetInt("age", 0) > 25
	})

	if len(found) != 2 {
		t.Errorf("Expected 2 rows, got %d", len(found))
	}
}

// TestGetRow tests getting a row by index
func TestGetRow(t *testing.T) {
	data := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
			{"name": "Bob"},
		},
	}

	row := data.GetRow(0)
	if row == nil {
		t.Error("Expected to get row 0")
	} else if row.Get("name") != "Alice" {
		t.Errorf("Expected Alice, got %s", row.Get("name"))
	}

	if data.GetRow(-1) != nil {
		t.Error("Expected nil for negative index")
	}

	if data.GetRow(10) != nil {
		t.Error("Expected nil for out of bounds index")
	}
}

// TestGetColumnInt tests getting column as integers
func TestGetColumnInt(t *testing.T) {
	data := &CsvData{
		Headers: []string{"age"},
		Rows: []CsvRow{
			{"age": "30"},
			{"age": "25"},
		},
	}

	ages := data.GetColumnInt("age")
	if len(ages) != 2 {
		t.Errorf("Expected 2 ages, got %d", len(ages))
	}

	if ages[0] != 30 {
		t.Errorf("Expected first age 30, got %d", ages[0])
	}
}

// TestGetColumnFloat tests getting column as floats
func TestGetColumnFloat(t *testing.T) {
	data := &CsvData{
		Headers: []string{"value"},
		Rows: []CsvRow{
			{"value": "3.14"},
			{"value": "2.71"},
		},
	}

	values := data.GetColumnFloat("value")
	if len(values) != 2 {
		t.Errorf("Expected 2 values, got %d", len(values))
	}

	if values[0] != 3.14 {
		t.Errorf("Expected first value 3.14, got %f", values[0])
	}
}

// TestRowCountColumnCount tests row and column counting
func TestRowCountColumnCount(t *testing.T) {
	data := &CsvData{
		Headers: []string{"a", "b", "c"},
		Rows: []CsvRow{
			{"a": "1", "b": "2", "c": "3"},
			{"a": "4", "b": "5", "c": "6"},
		},
	}

	if data.RowCount() != 2 {
		t.Errorf("Expected 2 rows, got %d", data.RowCount())
	}

	if data.ColumnCount() != 3 {
		t.Errorf("Expected 3 columns, got %d", data.ColumnCount())
	}
}

// TestIsValid tests data validation
func TestIsValid(t *testing.T) {
	validData := &CsvData{
		Headers: []string{"name"},
		Rows: []CsvRow{
			{"name": "Alice"},
		},
	}

	if !validData.IsValid() {
		t.Error("Expected data to be valid")
	}

	invalidData := &CsvData{
		Headers: []string{"name", "age"},
		Rows: []CsvRow{
			{"name": "Alice"}, // Missing age
		},
	}

	if invalidData.IsValid() {
		t.Error("Expected data to be invalid")
	}
}

// TestLazyQuotes tests lazy quote handling
func TestLazyQuotes(t *testing.T) {
	csvData := `name,description
Alice,She said "hello"
Bob,Normal text`

	opts := DefaultOptions()
	opts.LazyQuotes = true
	data, err := ReadStringWithOptions(csvData, opts)
	if err != nil {
		t.Fatalf("Failed to read CSV with lazy quotes: %v", err)
	}

	if len(data.Rows) != 2 {
		t.Errorf("Expected 2 rows, got %d", len(data.Rows))
	}
}

// TestAddRowMap tests adding row from map
func TestAddRowMap(t *testing.T) {
	writer := NewWriter()
	writer.SetHeaders([]string{"name", "age"})
	writer.AddRowMap(map[string]string{
		"name": "Alice",
		"age":  "30",
	})

	data := writer.ToCsvData()
	if len(data.Rows) != 1 {
		t.Errorf("Expected 1 row, got %d", len(data.Rows))
	}

	if data.Rows[0].Get("name") != "Alice" {
		t.Errorf("Expected name '"Alice"', got '"%s"'", data.Rows[0].Get("name"))
	}
}

// TestJoinError tests join error handling
func TestJoinError(t *testing.T) {
	left := &CsvData{
		Headers: []string{"name"},
		Rows:    []CsvRow{{"name": "Alice"}},
	}

	right := &CsvData{
		Headers: []string{"age"},
		Rows:    []CsvRow{{"age": "30"}, {"age": "25"}},
	}

	_, err := Join(left, right)
	if err == nil {
		t.Error("Expected error for row count mismatch")
	}
}

// TestMergeError tests merge error handling
func TestMergeError(t *testing.T) {
	first := &CsvData{
		Headers: []string{"name"},
		Rows:    []CsvRow{{"name": "Alice"}},
	}

	second := &CsvData{
		Headers: []string{"age"},
		Rows:    []CsvRow{{"age": "30"}},
	}

	_, err := Merge(first, second)
	if err == nil {
		t.Error("Expected error for header mismatch")
	}
}
