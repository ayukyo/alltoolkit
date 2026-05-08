// Example usage of countdown_utils package
package main

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/countdown_utils"
)

func main() {
	fmt.Println("=== Countdown Utils Examples ===\n")

	// Example 1: Basic countdown
	fmt.Println("--- Example 1: Basic Countdown ---")
	target := time.Now().Add(2 * time.Hour)
	countdown := countdown_utils.NewCountdown(target)
	fmt.Printf("Target time: %s\n", countdown.Target.Format("2006-01-02 15:04:05"))
	fmt.Printf("Remaining: %s\n", countdown_utils.FormatCountdown(countdown.Remaining))
	fmt.Printf("Compact: %s\n", countdown_utils.FormatCountdownCompact(countdown.Remaining))
	fmt.Printf("Long format: %s\n", countdown_utils.FormatCountdownLong(countdown.Remaining))
	fmt.Println()

	// Example 2: Duration parsing and formatting
	fmt.Println("--- Example 2: Duration Formatting ---")
	d := countdown_utils.ParseDuration(3*24*time.Hour + 5*time.Hour + 30*time.Minute + 15*time.Second)
	fmt.Printf("Duration: %v\n", d.Total)
	fmt.Printf("  Days: %d, Hours: %d, Minutes: %d, Seconds: %d\n", d.Days, d.Hours, d.Minutes, d.Seconds)
	fmt.Printf("  Format: %s\n", d.Format())
	fmt.Printf("  Compact: %s\n", d.FormatCompact())
	fmt.Printf("  Digital: %s\n", d.FormatDigital())
	fmt.Printf("  Long: %s\n", d.FormatLong())
	fmt.Printf("  Custom: %s\n", d.FormatCustom("{d} days, {h} hours, {m} minutes, {s} seconds"))
	fmt.Println()

	// Example 3: Parse duration string
	fmt.Println("--- Example 3: Parse Duration String ---")
	duration, err := countdown_utils.ParseDurationString("2d 5h 30m 15s")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Parsed '2d 5h 30m 15s' = %v\n", duration)
		fmt.Printf("Formatted: %s\n", countdown_utils.FormatCountdown(duration))
	}
	fmt.Println()

	// Example 4: Working days calculations
	fmt.Println("--- Example 4: Working Days ---")
	now := time.Now()
	future := now.AddDate(0, 0, 10) // 10 days from now
	workingDays := countdown_utils.WorkingDaysBetween(now, future)
	fmt.Printf("From %s to %s:\n", now.Format("2006-01-02"), future.Format("2006-01-02"))
	fmt.Printf("  Total days: 10\n")
	fmt.Printf("  Working days: %d\n", workingDays)
	
	nextWorkDay := countdown_utils.NextWorkingDay(now)
	fmt.Printf("Next working day: %s (%s)\n", nextWorkDay.Format("2006-01-02"), nextWorkDay.Weekday())
	
	prevWorkDay := countdown_utils.PreviousWorkingDay(now)
	fmt.Printf("Previous working day: %s (%s)\n", prevWorkDay.Format("2006-01-02"), prevWorkDay.Weekday())
	
	// Add 5 working days
	addedWorkDays := countdown_utils.AddWorkingDays(now, 5)
	fmt.Printf("Add 5 working days: %s (%s)\n", addedWorkDays.Format("2006-01-02"), addedWorkDays.Weekday())
	fmt.Println()

	// Example 5: Countdown to specific event
	fmt.Println("--- Example 5: Countdown to New Year ---")
	newYearCountdown := countdown_utils.CountdownToNewYear()
	newYearCountdown.Update()
	fmt.Printf("Days until New Year: %d\n", countdown_utils.DaysUntil(newYearCountdown.Target))
	fmt.Printf("Time remaining: %s\n", newYearCountdown.GetDuration().FormatLong())
	fmt.Println()

	// Example 6: Timer functionality
	fmt.Println("--- Example 6: Timer ---")
	timer := countdown_utils.NewTimer(5 * time.Second)
	
	completed := make(chan bool)
	timer.SetOnComplete(func() {
		completed <- true
	})
	
	fmt.Println("Starting 5-second timer...")
	timer.Start()
	
	// Check timer state
	for i := 0; i < 3; i++ {
		time.Sleep(1 * time.Second)
		remaining := timer.GetRemaining()
		fmt.Printf("  Remaining: %s\n", countdown_utils.FormatCountdown(remaining))
	}
	
	// Wait for completion
	<-completed
	fmt.Println("  Timer completed!")
	fmt.Println()

	// Example 7: Progress tracking
	fmt.Println("--- Example 7: Progress Tracking ---")
	// Simulate a task with progress
	taskTarget := time.Now().Add(100 * time.Millisecond)
	taskCountdown := countdown_utils.NewCountdown(taskTarget)
	
	fmt.Printf("Progress bar: [%s] %.1f%%\n", taskCountdown.FormatProgress(20), taskCountdown.ProgressPercent())
	
	time.Sleep(50 * time.Millisecond)
	taskCountdown.Update()
	fmt.Printf("Progress bar: [%s] %.1f%%\n", taskCountdown.FormatProgress(20), taskCountdown.ProgressPercent())
	
	time.Sleep(60 * time.Millisecond)
	taskCountdown.Update()
	fmt.Printf("Progress bar: [%s] %.1f%%\n", taskCountdown.FormatProgress(20), taskCountdown.ProgressPercent())
	fmt.Println()

	// Example 8: Weekend check
	fmt.Println("--- Example 8: Weekend Check ---")
	today := time.Now()
	if countdown_utils.IsWeekend(today) {
		fmt.Printf("Today (%s) is a weekend!\n", today.Weekday())
	} else {
		fmt.Printf("Today (%s) is a working day.\n", today.Weekday())
	}
	fmt.Println()

	// Example 9: Custom format with all placeholders
	fmt.Println("--- Example 9: Custom Formats ---")
	d2 := countdown_utils.ParseDuration(5*24*time.Hour + 12*time.Hour + 5*time.Minute + 8*time.Second)
	fmt.Printf("Raw values: %d days, %d hours, %d minutes, %d seconds\n", d2.Days, d2.Hours, d2.Minutes, d2.Seconds)
	fmt.Printf("Padded:     {D}:{H}:{M}:{S} = %s\n", d2.FormatCustom("{D}:{H}:{M}:{S}"))
	fmt.Printf("Unpadded:   {d}:{h}:{m}:{s} = %s\n", d2.FormatCustom("{d}:{h}:{m}:{s}"))
	fmt.Printf("Sentence:   {d} days, {h} hours and {m} minutes = %s\n", d2.FormatCustom("{d} days, {h} hours and {m} minutes"))
	fmt.Println()

	fmt.Println("=== Examples Complete ===")
}