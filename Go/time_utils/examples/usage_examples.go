// Example usage of time_utils package
package main

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/time_utils"
)

func main() {
	fmt.Println("=== Time Utils Examples ===")

	// ==================== Parsing Examples ====================
	fmt.Println("--- Parsing Examples ---")

	// Parse with auto-detection
	t1, _ := time_utils.Parse("2024-01-15T10:30:00Z")
	fmt.Printf("Auto-parse: %v\n", t1)

	t2, _ := time_utils.Parse("2024-01-15 10:30:00")
	fmt.Printf("Auto-parse datetime: %v\n", t2)

	// Parse Unix timestamp
	t3, _ := time_utils.ParseUnix(1705315800)
	fmt.Printf("Unix timestamp: %v\n", t3)

	t4, _ := time_utils.ParseUnix(1705315800000) // milliseconds
	fmt.Printf("Unix millisecond: %v\n", t4)

	// Parse human-readable duration
	d1, _ := time_utils.ParseDuration("1d2h30m")
	fmt.Printf("Parsed duration: %v\n", d1)

	d2, _ := time_utils.ParseDuration("2h 45m 30s")
	fmt.Printf("Parsed duration with spaces: %v\n", d2)

	fmt.Println()

	// ==================== Formatting Examples ====================
	fmt.Println("--- Formatting Examples ---")

	now := time.Date(2024, 1, 15, 10, 30, 45, 0, time.UTC)
	fmt.Printf("FormatDate: %s\n", time_utils.FormatDate(now))
	fmt.Printf("FormatTime: %s\n", time_utils.FormatTime(now))
	fmt.Printf("FormatDateTime: %s\n", time_utils.FormatDateTime(now))
	fmt.Printf("FormatISO8601: %s\n", time_utils.FormatISO8601(now))
	fmt.Printf("Unix timestamp: %d\n", time_utils.FormatUnixTimestamp(now))
	fmt.Printf("Unix millisecond: %d\n", time_utils.FormatUnixMilli(now))

	// Human-readable duration
	fmt.Printf("Human duration (90min): %s\n", time_utils.FormatHumanDuration(90*time.Minute))
	fmt.Printf("Human duration (26h): %s\n", time_utils.FormatHumanDuration(26*time.Hour))
	fmt.Printf("Human duration (500ms): %s\n", time_utils.FormatHumanDuration(500*time.Millisecond))

	fmt.Println()

	// ==================== Time Calculation Examples ====================
	fmt.Println("--- Time Calculation Examples ---")

	base := time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC)
	fmt.Printf("Base time: %v\n", base)
	fmt.Printf("Add 5 days: %v\n", time_utils.AddDays(base, 5))
	fmt.Printf("Add 2 months: %v\n", time_utils.AddMonths(base, 2))
	fmt.Printf("Add 1 year: %v\n", time_utils.AddYears(base, 1))
	fmt.Printf("Subtract 3 days: %v\n", time_utils.AddDays(base, -3))

	// Day boundaries
	fmt.Printf("Start of day: %v\n", time_utils.StartOfDay(base))
	fmt.Printf("End of day: %v\n", time_utils.EndOfDay(base))
	fmt.Printf("Start of week: %v\n", time_utils.StartOfWeek(base))
	fmt.Printf("End of week: %v\n", time_utils.EndOfWeek(base))
	fmt.Printf("Start of month: %v\n", time_utils.StartOfMonth(base))
	fmt.Printf("End of month: %v\n", time_utils.EndOfMonth(base))
	fmt.Printf("Start of year: %v\n", time_utils.StartOfYear(base))
	fmt.Printf("End of year: %v\n", time_utils.EndOfYear(base))

	fmt.Println()

	// ==================== Comparison Examples ====================
	fmt.Println("--- Comparison Examples ---")

	t10 := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	t11 := time.Date(2024, 1, 15, 12, 0, 0, 0, time.UTC)

	fmt.Printf("Is %v before %v: %v\n", t10, t11, time_utils.IsBefore(t10, t11))
	fmt.Printf("Is %v after %v: %v\n", t11, t10, time_utils.IsAfter(t11, t10))
	fmt.Printf("Same day: %v\n", time_utils.IsSameDay(t10, t11))

	// Today/Tomorrow/Yesterday checks
	fmt.Printf("Is today: %v\n", time_utils.IsToday(now))
	fmt.Printf("Is weekend: %v\n", time_utils.IsWeekend(now))

	// Leap year
	fmt.Printf("2024 is leap year: %v\n", time_utils.IsLeapYear(2024))
	fmt.Printf("Days in February 2024: %d\n", time_utils.DaysInMonth(2024, time.February))

	fmt.Println()

	// ==================== Time Difference Examples ====================
	fmt.Println("--- Time Difference Examples ---")

	start := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	end := time.Date(2024, 1, 17, 14, 30, 0, 0, time.UTC)

	fmt.Printf("Difference: %v\n", time_utils.Diff(start, end))
	fmt.Printf("Diff in days: %d\n", time_utils.DiffInDays(start, end))
	fmt.Printf("Diff in hours: %.2f\n", time_utils.DiffInHours(start, end))
	fmt.Printf("Diff in minutes: %.2f\n", time_utils.DiffInMinutes(start, end))
	fmt.Printf("Human diff: %s\n", time_utils.DiffHuman(start, end))

	// Detailed difference
	detailed := time_utils.DiffDetailed(start, end)
	fmt.Printf("Detailed diff: %d days, %d hours, %d minutes, %d seconds\n",
		detailed.Days, detailed.Hours, detailed.Minutes, detailed.Seconds)

	fmt.Println()

	// ==================== Time Range Examples ====================
	fmt.Println("--- Time Range Examples ---")

	rangeStart := time.Date(2024, 1, 15, 9, 0, 0, 0, time.UTC)
	rangeEnd := time.Date(2024, 1, 15, 17, 0, 0, 0, time.UTC)
	tr, _ := time_utils.NewTimeRange(rangeStart, rangeEnd)

	fmt.Printf("Time range: %v to %v\n", tr.Start, tr.End)
	fmt.Printf("Duration: %v\n", tr.Duration())

	// Check if time is in range
	meeting := time.Date(2024, 1, 15, 14, 0, 0, 0, time.UTC)
	fmt.Printf("Is %v in range: %v\n", meeting, tr.Contains(meeting))

	// Split range
	splits := tr.Split(time.Hour)
	fmt.Printf("Split into %d hourly intervals\n", len(splits))

	fmt.Println()

	// ==================== Stopwatch Example ====================
	fmt.Println("--- Stopwatch Example ---")

	sw := time_utils.NewStopwatch()
	sw.Start()

	// Simulate some work
	for i := 0; i < 1000000; i++ {
		_ = i * i
	}

	sw.Stop()
	fmt.Printf("Elapsed: %s\n", sw.ElapsedString())

	sw.Start()
	for i := 0; i < 500000; i++ {
		_ = i * i
	}
	sw.Stop()
	fmt.Printf("Total elapsed: %s\n", sw.ElapsedString())

	fmt.Println()

	// ==================== Countdown Example ====================
	fmt.Println("--- Countdown Example ---")

	cd := time_utils.NewCountdown(2 * time.Hour)
	fmt.Printf("Remaining: %v\n", cd.Remaining())
	fmt.Printf("Is expired: %v\n", cd.IsExpired())

	// Progress (if we know total duration)
	progress := cd.Progress(2 * time.Hour)
	fmt.Printf("Progress: %.2f%%\n", progress*100)

	fmt.Println()

	// ==================== Weekday Calculations ====================
	fmt.Println("--- Weekday Calculations ---")

	// Next Monday from Wednesday
	wed := time.Date(2024, 1, 17, 0, 0, 0, 0, time.UTC)
	nextMon := time_utils.NextWeekday(wed, time.Monday)
	fmt.Printf("Next Monday from %v: %v\n", wed.Format("2006-01-02 (Mon)"), nextMon.Format("2006-01-02 (Mon)"))

	// Previous Friday
	prevFri := time_utils.PreviousWeekday(wed, time.Friday)
	fmt.Printf("Previous Friday: %v\n", prevFri.Format("2006-01-02 (Mon)"))

	// 2nd Tuesday of month
	secondTue := time_utils.NextNthWeekday(2024, time.January, time.Tuesday, 2)
	fmt.Printf("2nd Tuesday of Jan 2024: %v\n", secondTue.Format("2006-01-02"))

	// Last Friday of month
	lastFri := time_utils.LastNthWeekday(2024, time.January, time.Friday)
	fmt.Printf("Last Friday of Jan 2024: %v\n", lastFri.Format("2006-01-02"))

	fmt.Println()

	// ==================== Age Calculation ====================
	fmt.Println("--- Age Calculation ---")

	birthday := time.Date(1990, 5, 20, 0, 0, 0, 0, time.UTC)
	age := time_utils.Age(birthday)
	fmt.Printf("Age from %v: %d years\n", birthday.Format("2006-01-02"), age)

	years, months, days := time_utils.AgeDetailed(birthday)
	fmt.Printf("Detailed age: %d years, %d months, %d days\n", years, months, days)

	fmt.Println()

	// ==================== Utility Functions ====================
	fmt.Println("--- Utility Functions ---")

	// Now in different timezones
	fmt.Printf("Now UTC: %v\n", time_utils.Now())
	fmt.Printf("Now Local: %v\n", time_utils.NowLocal())

	// Convert to different timezone
	loc, _ := time_utils.Location("America/New_York")
	fmt.Printf("Now in New York: %v\n", time_utils.NowIn(loc))

	// Sort times
	times := []time.Time{
		time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 1, 10, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 1, 20, 0, 0, 0, 0, time.UTC),
	}
	sorted := time_utils.SortTimes(times)
	fmt.Printf("Sorted times: %v\n", sorted)

	// Min/Max
	minTime := time_utils.Min(times...)
	maxTime := time_utils.Max(times...)
	fmt.Printf("Min: %v, Max: %v\n", minTime, maxTime)

	// Clamp
	clamped := time_utils.Clamp(
		time.Date(2024, 1, 5, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 1, 10, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 1, 20, 0, 0, 0, 0, time.UTC),
	)
	fmt.Printf("Clamped time: %v\n", clamped.Format("2006-01-02"))

	fmt.Println("\n=== All Examples Complete ===")
}