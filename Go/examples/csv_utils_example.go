// Example program demonstrating CSV utilities
package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/ayukyo/alltoolkit/Go/csv_utils"
)

func main() {
	fmt.Println("=== CSV Utils Example ===\n")

	// Example 1: Reading CSV from string
	fmt.Println("1. Reading CSV from string:")
	csvData := `name,age,city,salary
Alice,30,New York,75000
Bob,25,Los Angeles,60000
Charlie,35,Chicago,90000
Diana,28,Seattle,72000`

	data, err := csv_utils.ReadString(csvData)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Headers: %v\n", data.Headers)
	fmt.Printf("Row count: %d\n\n", data.RowCount())

	// Example 2: Accessing data with type conversion
	fmt.Println("2. Accessing data with type conversion:")
	for _, row := range data.Rows {
		name := row.Get("name")
		age := row.GetInt("age", 0)
		city := row.Get("city")
		salary := row.GetFloat("salary", 0.0)
		fmt.Printf("  %s is %d years old, lives in %s, earns $%.2f\n", name, age, city, salary)
	}
	fmt.Println()

	// Example 3: Filtering rows
	fmt.Println("3. Filtering rows (age > 28):")
	olderThan28 := data.FilterRows(func(row csv_utils.CsvRow) bool {
		return row.GetInt("age", 0) > 28
	})
	for _, row := range olderThan28.Rows {
		fmt.Printf("  %s: %d years old\n", row.Get("name"), row.GetInt("age", 0))
	}
	fmt.Println()

	// Example 4: Sorting by column
	fmt.Println("4. Sorting by salary (ascending):")
	sortedBySalary := data.SortByWithOptions("salary", true, true)
	for _, row := range sortedBySalary.Rows {
		fmt.Printf("  %s: $%.2f\n", row.Get("name"), row.GetFloat("salary", 0.0))
	}
	fmt.Println()

	// Example 5: Column statistics
	fmt.Println("5. Column statistics:")
	fmt.Printf("  Average salary: $%.2f\n", data.AvgColumn("salary"))
	fmt.Printf("  Min salary: $%.2f\n", data.MinColumn("salary"))
	fmt.Printf("  Max salary: $%.2f\n", data.MaxColumn("salary"))
	fmt.Printf("  Total salary: $%.2f\n\n", data.SumColumn("salary"))

	// Example 6: Filtering columns
	fmt.Println("6. Filtering columns (name and city only):")
	nameCityOnly := data.FilterColumns([]string{"name", "city"})
	for _, row := range nameCityOnly.Rows {
		fmt.Printf("  %s lives in %s\n", row.Get("name"), row.Get("city"))
	}
	fmt.Println()

	// Example 7: Grouping by column
	fmt.Println("7. Grouping by city:")
	byCity := data.GroupBy("city")
	for city, rows := range byCity {
		names := []string{}
		for _, row := range rows {
			names = append(names, row.Get("name"))
		}
		fmt.Printf("  %s: %v\n", city, names)
	}
	fmt.Println()

	// Example 8: Finding rows
	fmt.Println("8. Finding rows:")
	bob := data.Find(func(row csv_utils.CsvRow) bool {
		return row.Get("name") == "Bob"
	})
	if bob != nil {
		fmt.Printf("  Found Bob: %s\n", bob.Get("city"))
	}

	highEarners := data.FindAll(func(row csv_utils.CsvRow) bool {
		return row.GetFloat("salary", 0) > 70000
	})
	fmt.Printf("  High earners (> $70k): %d people\n", len(highEarners))
	fmt.Println()

	// Example 9: Writing CSV
	fmt.Println("9. Writing CSV:")
	writer := csv_utils.NewWriter()
	writer.SetHeaders([]string{"product", "price", "quantity"})
	writer.AddRow([]string{"Laptop", "999.99", "5"})
	writer.AddRow([]string{"Mouse", "29.99", "20"})
	writer.AddRow([]string{"Keyboard", "79.99", "10"})

	csvString := writer.ToString()
	fmt.Println("  Generated CSV:")
	fmt.Println(csvString)

	// Example 10: Custom delimiter (TSV)
	fmt.Println("10. Reading TSV (tab-separated values):")
	tsvData := `name\tage\tcity
Alice\t30\tNew York
Bob\t25\tLos Angeles`

	opts := csv_utils.DefaultOptions()
	opts.Delimiter = '\t'
	tsv, err := csv_utils.ReadStringWithOptions(tsvData, opts)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("  TSV Headers: %v\n", tsv.Headers)
	fmt.Printf("  First row: %s, %s, %s\n\n",
		tsv.Rows[0].Get("name"),
		tsv.Rows[0].Get("age"),
		tsv.Rows[0].Get("city"))

	// Example 11: Detecting delimiter
	fmt.Println("11. Detecting delimiter:")
	sample1 := "a,b,c"
	sample2 := "a;b;c"
	fmt.Printf("  Delimiter in '%s': %c\n", sample1, csv_utils.DetectDelimiter(sample1))
	fmt.Printf("  Delimiter in '%s': %c\n\n", sample2, csv_utils.DetectDelimiter(sample2))

	// Example 12: Distinct values
	fmt.Println("12. Distinct values:")
	csvWithDuplicates := `category,value
A,10
B,20
A,30
C,40
B,50`

	data2, _ := csv_utils.ReadString(csvWithDuplicates)
	distinctCategories := data2.Distinct("category")
	fmt.Printf("  Distinct categories: %v\n\n", distinctCategories)

	// Example 13: Transforming data
	fmt.Println("13. Transforming data (uppercase names):")
	data.Transform(func(row csv_utils.CsvRow) csv_utils.CsvRow {
		row["name"] = strings.ToUpper(row["name"])
		return row
	})
	for _, row := range data.Rows {
		fmt.Printf("  %s\n", row.Get("name"))
	}
	fmt.Println()

	// Example 14: Joining datasets
	fmt.Println("14. Joining datasets:")
	left := &csv_utils.CsvData{
		Headers: []string{"id", "name"},
		Rows: []csv_utils.CsvRow{
			{"id": "1", "name": "Alice"},
			{"id": "2", "name": "Bob"},
		},
	}
	right := &csv_utils.CsvData{
		Headers: []string{"department", "salary"},
		Rows: []csv_utils.CsvRow{
			{"department": "Engineering", "salary": "90000"},
			{"department": "Sales", "salary": "70000"},
		},
	}
	joined, err := csv_utils.Join(left, right)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("  Joined headers: %v\n", joined.Headers)
	for _, row := range joined.Rows {
		fmt.Printf("  %s works in %s, earns $%s\n",
			row.Get("name"), row.Get("department"), row.Get("salary"))
	}
	fmt.Println()

	// Example 15: Validating CSV
	fmt.Println("15. Validating CSV:")
	validCsv := "a,b\n1,2"
	invalidCsv := "a,b\n1,2,3" // Mismatched columns (will parse but may not be what expected)
	fmt.Printf("  Is '%s' valid? %v\n", validCsv, csv_utils.IsValidCsv(validCsv))
	fmt.Printf("  Is '%s' valid? %v\n\n", invalidCsv, csv_utils.IsValidCsv(invalidCsv))

	// Example 16: Boolean conversion
	fmt.Println("16. Boolean conversion:")
	csvWithBools := `name,active,admin
Alice,true,yes
Bob,false,no
Charlie,1,0`

	data3, _ := csv_utils.ReadString(csvWithBools)
	for _, row := range data3.Rows {
		name := row.Get("name")
		active := row.GetBool("active", false)
		admin := row.GetBool("admin", false)
		fmt.Printf("  %s: active=%v, admin=%v\n", name, active, admin)
	}
	fmt.Println()

	// Example 17: Counting with predicate
	fmt.Println("17. Counting with predicate:")
	count := data.Count(func(row csv_utils.CsvRow) bool {
		return row.GetFloat("salary", 0) > 70000
	})
	fmt.Printf("  Employees earning more than $70k: %d\n\n", count)

	// Example 18: Adding and removing columns
	fmt.Println("18. Adding and removing columns:")
	dataCopy := &csv_utils.CsvData{
		Headers: []string{"name", "age"},
		Rows: []csv_utils.CsvRow{
			{"name": "Alice", "age": "30"},
			{"name": "Bob", "age": "25"},
		},
	}
	dataCopy.AddColumn("country", []string{"USA", "UK"})
	fmt.Printf("  After adding 'country' column: %v\n", dataCopy.Headers)
	dataCopy.RemoveColumn("age")
	fmt.Printf("  After removing 'age' column: %v\n", dataCopy.Headers)
	fmt.Println()

	fmt.Println("=== End of Examples ===")
}
