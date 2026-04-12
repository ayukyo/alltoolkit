// Example: Basic JSON Utils Usage
// Demonstrates fundamental operations with json_utils package
package main

import (
	"fmt"
	"os"

	"json_utils"
)

func main() {
	fmt.Println("=== JSON Utils Basic Usage Demo ===\n")

	// Sample JSON data
	config := `{
		"app": {
			"name": "MyApp",
			"version": "1.0.0",
			"debug": false
		},
		"database": {
			"host": "localhost",
			"port": 5432,
			"name": "mydb"
		},
		"features": ["auth", "api", "admin"]
	}`

	// 1. Pretty Print
	fmt.Println("1. Pretty Print:")
	fmt.Println("----------------")
	pretty, err := jsonutils.PrettyPrint(config, "  ")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Println(pretty)
	fmt.Println()

	// 2. Minify
	fmt.Println("2. Minify:")
	fmt.Println("----------")
	minified, err := jsonutils.Minify(config)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Println(minified)
	fmt.Println()

	// 3. Get values using path
	fmt.Println("3. Get Values:")
	fmt.Println("--------------")
	appName := jsonutils.Get(config, "app.name")
	fmt.Printf("App Name: %v\n", appName.Value)

	dbHost := jsonutils.Get(config, "database.host")
	fmt.Printf("DB Host: %v\n", dbHost.Value)

	dbPort := jsonutils.Get(config, "database.port")
	fmt.Printf("DB Port: %v\n", dbPort.Value)
	fmt.Println()

	// 4. Set values
	fmt.Println("4. Set Values:")
	fmt.Println("--------------")
	updated, err := jsonutils.Set(config, "app.debug", true)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	updated, err = jsonutils.Set(updated, "database.port", 5433)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	updated, err = jsonutils.Set(updated, "cache.enabled", true)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	prettyUpdated, _ := jsonutils.PrettyPrint(updated, "  ")
	fmt.Println(prettyUpdated)
	fmt.Println()

	// 5. Delete fields
	fmt.Println("5. Delete Fields:")
	fmt.Println("-----------------")
	deleted, err := jsonutils.Delete(updated, "app.debug")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	prettyDeleted, _ := jsonutils.PrettyPrint(deleted, "  ")
	fmt.Println(prettyDeleted)
	fmt.Println()

	// 6. Merge JSON objects
	fmt.Println("6. Merge JSON:")
	fmt.Println("--------------")
	extra := `{"logging": {"level": "info", "file": "app.log"}}`
	merged, err := jsonutils.Merge(deleted, extra)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	prettyMerged, _ := jsonutils.PrettyPrint(merged, "  ")
	fmt.Println(prettyMerged)
	fmt.Println()

	// 7. Extract all keys
	fmt.Println("7. Extract Keys:")
	fmt.Println("----------------")
	keys, err := jsonutils.ExtractKeys(merged)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("All keys: %v\n", keys)
	fmt.Println()

	// 8. Validate JSON
	fmt.Println("8. Validate JSON:")
	fmt.Println("-----------------")
	result := jsonutils.Validate(merged, nil)
	fmt.Printf("Valid: %v\n", result.Valid)
	if len(result.Errors) > 0 {
		fmt.Printf("Errors: %v\n", result.Errors)
	}
	fmt.Println()

	// 9. Compare two JSON objects
	fmt.Println("9. Diff JSON:")
	fmt.Println("-------------")
	old := `{"name": "John", "age": 30, "city": "NYC"}`
	new := `{"name": "John", "age": 31, "country": "USA"}`
	diff, err := jsonutils.Diff(old, new)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Added: %v\n", diff["added"])
	fmt.Printf("Removed: %v\n", diff["removed"])
	fmt.Printf("Changed: %v\n", diff["changed"])
	fmt.Println()

	// 10. Transform values
	fmt.Println("10. Transform Values:")
	fmt.Println("---------------------")
	data := `{"name": "john doe", "city": "new york"}`
	upper, err := jsonutils.Transform(data, func(s string) string {
		return fmt.Sprintf("[%s]", s)
	})
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Println(upper)
	fmt.Println()

	fmt.Println("=== Demo Complete ===")
}
