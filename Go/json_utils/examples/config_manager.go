// Example: Configuration Manager
// Demonstrates using json_utils for configuration management
package main

import (
	"fmt"
	"os"

	"json_utils"
)

// Config represents application configuration
type Config struct {
	App      AppConfig      `json:"app"`
	Database DatabaseConfig `json:"database"`
	Server   ServerConfig   `json:"server"`
}

type AppConfig struct {
	Name    string `json:"name"`
	Version string `json:"version"`
	Debug   bool   `json:"debug"`
}

type DatabaseConfig struct {
	Host     string `json:"host"`
	Port     int    `json:"port"`
	Name     string `json:"name"`
	Username string `json:"username"`
	Password string `json:"password"`
}

type ServerConfig struct {
	Host string `json:"host"`
	Port int    `json:"port"`
}

func main() {
	fmt.Println("=== Configuration Manager Demo ===\n")

	// Initial configuration
	configJSON := `{
		"app": {
			"name": "MyApplication",
			"version": "1.0.0",
			"debug": false
		},
		"database": {
			"host": "localhost",
			"port": 5432,
			"name": "production_db",
			"username": "admin",
			"password": "secret123"
		},
		"server": {
			"host": "0.0.0.0",
			"port": 8080
		}
	}`

	// 1. Load and validate configuration
	fmt.Println("1. Loading Configuration...")
	fmt.Println("---------------------------")
	result := jsonutils.Validate(configJSON, nil)
	if !result.Valid {
		fmt.Printf("Invalid configuration: %v\n", result.Errors)
		os.Exit(1)
	}
	fmt.Println("✓ Configuration is valid")
	fmt.Println()

	// 2. Access configuration values
	fmt.Println("2. Reading Configuration Values:")
	fmt.Println("---------------------------------")
	appName := jsonutils.Get(configJSON, "app.name")
	appVersion := jsonutils.Get(configJSON, "app.version")
	dbHost := jsonutils.Get(configJSON, "database.host")
	dbPort := jsonutils.Get(configJSON, "database.port")
	serverPort := jsonutils.Get(configJSON, "server.port")

	fmt.Printf("   Application: %s v%s\n", appName.Value, appVersion.Value)
	fmt.Printf("   Database: %s:%d\n", dbHost.Value, dbPort.Value)
	fmt.Printf("   Server Port: %d\n", serverPort.Value)
	fmt.Println()

	// 3. Update configuration for different environment
	fmt.Println("3. Creating Development Configuration:")
	fmt.Println("---------------------------------------")
	devConfig := configJSON
	devConfig, _ = jsonutils.Set(devConfig, "app.debug", true)
	devConfig, _ = jsonutils.Set(devConfig, "database.host", "localhost")
	devConfig, _ = jsonutils.Set(devConfig, "database.name", "dev_db")
	devConfig, _ = jsonutils.Set(devConfig, "server.port", 3000)

	prettyDev, _ := jsonutils.PrettyPrint(devConfig, "  ")
	fmt.Println(prettyDev)
	fmt.Println()

	// 4. Merge with environment-specific overrides
	fmt.Println("4. Merging Environment Overrides:")
	fmt.Println("----------------------------------")
	overrides := `{
		"features": {
			"newUI": true,
			"betaFeatures": true
		},
		"logging": {
			"level": "debug",
			"format": "json"
		}
	}`

	merged, err := jsonutils.Merge(devConfig, overrides)
	if err != nil {
		fmt.Printf("Error merging: %v\n", err)
		os.Exit(1)
	}

	prettyMerged, _ := jsonutils.PrettyPrint(merged, "  ")
	fmt.Println(prettyMerged)
	fmt.Println()

	// 5. Remove sensitive data for logging
	fmt.Println("5. Removing Sensitive Data:")
	fmt.Println("---------------------------")
	safeConfig := merged
	safeConfig, _ = jsonutils.Delete(safeConfig, "database.password")
	safeConfig, _ = jsonutils.Delete(safeConfig, "database.username")

	prettySafe, _ := jsonutils.PrettyPrint(safeConfig, "  ")
	fmt.Println(prettySafe)
	fmt.Println()

	// 6. Extract all configuration keys
	fmt.Println("6. Configuration Keys:")
	fmt.Println("----------------------")
	keys, err := jsonutils.ExtractKeys(safeConfig)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Total keys: %d\n", len(keys))
	fmt.Printf("Keys: %v\n", keys)
	fmt.Println()

	// 7. Compare configurations
	fmt.Println("7. Comparing Configurations:")
	fmt.Println("----------------------------")
	diff, err := jsonutils.Diff(configJSON, merged)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}

	added := diff["added"].(map[string]interface{})
	changed := diff["changed"].(map[string]interface{})

	fmt.Printf("Changes from production:\n")
	fmt.Printf("  - Added: %d fields\n", len(added))
	fmt.Printf("  - Changed: %d fields\n", len(changed))

	for key, val := range changed {
		change := val.(map[string]interface{})
		fmt.Printf("    • %s: %v → %v\n", key, change["old"], change["new"])
	}
	fmt.Println()

	// 8. Save configuration to file
	fmt.Println("8. Saving Configuration:")
	fmt.Println("------------------------")
	err = jsonutils.WriteFile("/tmp/app_config.json", safeConfig, "  ")
	if err != nil {
		fmt.Printf("Error saving: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("✓ Configuration saved to /tmp/app_config.json")

	// 9. Load configuration from file
	loaded, err := jsonutils.ReadFile("/tmp/app_config.json")
	if err != nil {
		fmt.Printf("Error loading: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("✓ Configuration loaded from file")

	// 10. Convert to struct
	fmt.Println("\n9. Converting to Struct:")
	fmt.Println("------------------------")
	var config Config
	m, _ := jsonutils.ToMap(loaded)
	err = jsonutils.FromMap(m, &config)
	if err != nil {
		fmt.Printf("Error converting: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✓ Converted to struct: %+v\n", config.App)
	fmt.Println()

	fmt.Println("=== Demo Complete ===")
}
