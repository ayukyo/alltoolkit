// Example usage of cron_expr_utils package
package main

import (
	"fmt"
	"time"

	cron "github.com/ayukyo/alltoolkit/Go/cron_expr_utils"
)

func main() {
	fmt.Println("=== Cron Expression Utils Examples ===\n")

	// Example 1: Basic parsing
	fmt.Println("--- Example 1: Basic Parsing ---")
	basicExample()

	// Example 2: Matching times
	fmt.Println("\n--- Example 2: Matching Times ---")
	matchingExample()

	// Example 3: Finding next execution times
	fmt.Println("\n--- Example 3: Finding Next Execution Times ---")
	nextExample()

	// Example 4: Using presets
	fmt.Println("\n--- Example 4: Using Presets ---")
	presetsExample()

	// Example 5: Builder pattern
	fmt.Println("\n--- Example 5: Builder Pattern ---")
	builderExample()

	// Example 6: Complex expressions
	fmt.Println("\n--- Example 6: Complex Expressions ---")
	complexExample()

	// Example 7: Validation and description
	fmt.Println("\n--- Example 7: Validation and Description ---")
	validationExample()
}

func basicExample() {
	// Parse a cron expression: every 15 minutes
	expr := "*/15 * * * *"
	cronExpr, err := cron.Parse(expr)
	if err != nil {
		fmt.Printf("Error parsing: %v\n", err)
		return
	}

	fmt.Printf("Parsed: %s\n", cronExpr.String())
	fmt.Printf("Description: %s\n", cronExpr.Describe())

	// Get field values
	minutes := cronExpr.GetFieldValues(0)
	fmt.Printf("Minute values: %v\n", minutes)
}

func matchingExample() {
	// Check if specific times match a cron expression
	expr := "30 9 * * 1-5" // 9:30 AM on weekdays
	cronExpr, _ := cron.Parse(expr)

	// Monday 9:30 AM
	monday := time.Date(2024, 1, 15, 9, 30, 0, 0, time.UTC)
	fmt.Printf("%s matches %q: %v\n", monday.Format("Mon 2006-01-02 15:04"), expr, cronExpr.Matches(monday))

	// Saturday 9:30 AM (should not match)
	saturday := time.Date(2024, 1, 20, 9, 30, 0, 0, time.UTC)
	fmt.Printf("%s matches %q: %v\n", saturday.Format("Mon 2006-01-02 15:04"), expr, cronExpr.Matches(saturday))

	// Monday 9:00 AM (should not match - wrong minute)
	monday9am := time.Date(2024, 1, 15, 9, 0, 0, 0, time.UTC)
	fmt.Printf("%s matches %q: %v\n", monday9am.Format("Mon 2006-01-02 15:04"), expr, cronExpr.Matches(monday9am))
}

func nextExample() {
	// Find the next 5 execution times
	expr := "0 9 * * 1-5" // 9:00 AM on weekdays
	cronExpr, _ := cron.Parse(expr)

	now := time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC) // Monday 10:30 AM
	fmt.Printf("Current time: %s\n", now.Format("Mon 2006-01-02 15:04"))

	next := cronExpr.Next(now)
	fmt.Printf("Next execution: %s\n", next.Format("Mon 2006-01-02 15:04"))

	// Get next 5 executions
	nextTimes := cronExpr.NextN(now, 5)
	fmt.Println("Next 5 executions:")
	for i, t := range nextTimes {
		fmt.Printf("  %d. %s\n", i+1, t.Format("Mon 2006-01-02 15:04"))
	}

	// Find previous execution
	prev := cronExpr.Prev(now)
	fmt.Printf("Previous execution: %s\n", prev.Format("Mon 2006-01-02 15:04"))
}

func presetsExample() {
	// Use predefined cron expressions
	presets := []struct {
		name string
		cron *cron.CronExpr
	}{
		{"EveryMinute", cron.EveryMinute},
		{"EveryHour", cron.EveryHour},
		{"EveryDay", cron.EveryDay},
		{"EveryWeek", cron.EveryWeek},
		{"EveryMonth", cron.EveryMonth},
		{"Weekdays", cron.Weekdays},
		{"Weekends", cron.Weekends},
		{"EveryFifteenMinutes", cron.EveryFifteenMinutes},
		{"EveryThirtyMinutes", cron.EveryThirtyMinutes},
		{"EverySixHours", cron.EverySixHours},
		{"TwiceDaily", cron.TwiceDaily},
	}

	now := time.Now()
	for _, p := range presets {
		next := p.cron.Next(now)
		fmt.Printf("%-25s -> next: %s\n", p.name, next.Format("2006-01-02 15:04"))
	}
}

func builderExample() {
	// Build cron expressions using fluent API

	// Every day at 9:30 AM
	daily, _ := cron.NewBuilder().
		AtMinute(30).
		AtHour(9).
		Build()
	fmt.Printf("Daily at 9:30 AM: %s\n", daily.String())

	// Every 15 minutes
	every15, _ := cron.NewBuilder().
		EveryNMinutes(15).
		Build()
	fmt.Printf("Every 15 minutes: %s\n", every15.String())

	// Every 6 hours at minute 0
	every6h, _ := cron.NewBuilder().
		AtMinute(0).
		EveryNHours(6).
		Build()
	fmt.Printf("Every 6 hours: %s\n", every6h.String())

	// Specific days
	specificDays, _ := cron.NewBuilder().
		AtMinute(0).
		AtHour(9).
		OnDay(1, 15).
		Build()
	fmt.Printf("1st and 15th at 9 AM: %s\n", specificDays.String())

	// Weekdays at specific time
	weekdays, _ := cron.NewBuilder().
		AtMinute(30).
		AtHour(9).
		OnWeekday(1, 2, 3, 4, 5).
		Build()
	fmt.Printf("Weekdays at 9:30 AM: %s\n", weekdays.String())
}

func complexExample() {
	// Complex cron expressions

	expressions := []string{
		"*/5 * * * *",       // Every 5 minutes
		"0 */2 * * *",       // Every 2 hours
		"30 8-17 * * 1-5",   // Every 30 minutes past the hour, 8 AM - 5 PM, weekdays
		"0 0 1 * *",         // First day of every month at midnight
		"0 12 * * 0",        // Every Sunday at noon
		"0 0 29 2 *",        // Feb 29 (leap year only)
		"*/10 9-17 * * 1-5", // Every 10 minutes during business hours on weekdays
		"0 0,12 * * *",      // Twice daily (midnight and noon)
	}

	for _, expr := range expressions {
		c, err := cron.Parse(expr)
		if err != nil {
			fmt.Printf("%-25s - Error: %v\n", expr, err)
			continue
		}

		now := time.Now()
		next := c.Next(now)
		fmt.Printf("%-25s - Next: %s\n", expr, next.Format("2006-01-02 15:04 Mon"))
	}
}

func validationExample() {
	// Validate cron expressions
	expressions := []string{
		"* * * * *",
		"*/15 * * * *",
		"0 9 * * 1-5",
		"invalid",
		"* * * *",
		"* * * * * *",
		"60 * * * *", // Invalid minute
	}

	fmt.Println("Validation:")
	for _, expr := range expressions {
		valid := cron.IsValid(expr)
		fmt.Printf("  %-25s -> %v\n", expr, valid)
	}

	// Get human-readable descriptions
	fmt.Println("\nDescriptions:")
	describeExpressions := []string{
		"* * * * *",
		"0 * * * *",
		"0 0 * * *",
		"30 14 * * *",
		"0 9 * * 1-5",
	}

	for _, expr := range describeExpressions {
		c, _ := cron.Parse(expr)
		fmt.Printf("  %-25s -> %s\n", expr, c.Describe())
	}

	// Helper functions
	fmt.Println("\nHelper functions:")
	fmt.Printf("  Weekday 0: %s\n", cron.GetWeekdayName(0))
	fmt.Printf("  Weekday 3: %s\n", cron.GetWeekdayName(3))
	fmt.Printf("  Month 1: %s\n", cron.GetMonthName(1))
	fmt.Printf("  Month 12: %s\n", cron.GetMonthName(12))
	fmt.Printf("  NormalizeWeekday(7): %d (Sunday as 7 -> 0)\n", cron.NormalizeWeekday(7))
}