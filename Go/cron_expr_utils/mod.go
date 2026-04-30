// Package cron_expr_utils provides cron expression parsing and evaluation.
// It supports standard 5-field cron format: minute hour day month weekday
// Examples: "* * * * *" (every minute), "0 9 * * 1-5" (9 AM on weekdays)
package cron_expr_utils

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// Field represents a single cron field (minute, hour, day, month, weekday)
type Field struct {
	values map[int]bool
}

// CronExpr represents a parsed cron expression
type CronExpr struct {
	minute  Field
	hour    Field
	day     Field
	month   Field
	weekday Field
	raw     string
}

var (
	// ErrInvalidExpression is returned when cron expression is invalid
	ErrInvalidExpression = errors.New("invalid cron expression")
	// ErrInvalidField is returned when a field is invalid
	ErrInvalidField = errors.New("invalid cron field")
)

// Field boundaries for each cron field
var fieldBounds = []struct {
	min, max int
}{
	{0, 59},  // minute
	{0, 23},  // hour
	{1, 31},  // day
	{1, 12},  // month
	{0, 6},   // weekday (0 = Sunday)
}

// Parse parses a cron expression string into a CronExpr
// Format: minute hour day month weekday
// Supports: *, numbers, ranges (1-5), steps (*/5, 1-10/2), lists (1,3,5)
func Parse(expr string) (*CronExpr, error) {
	expr = strings.TrimSpace(expr)
	if expr == "" {
		return nil, ErrInvalidExpression
	}

	fields := strings.Fields(expr)
	if len(fields) != 5 {
		return nil, fmt.Errorf("%w: expected 5 fields, got %d", ErrInvalidExpression, len(fields))
	}

	cron := &CronExpr{raw: expr}

	var err error
	cron.minute, err = parseField(fields[0], fieldBounds[0].min, fieldBounds[0].max)
	if err != nil {
		return nil, fmt.Errorf("minute: %w", err)
	}

	cron.hour, err = parseField(fields[1], fieldBounds[1].min, fieldBounds[1].max)
	if err != nil {
		return nil, fmt.Errorf("hour: %w", err)
	}

	cron.day, err = parseField(fields[2], fieldBounds[2].min, fieldBounds[2].max)
	if err != nil {
		return nil, fmt.Errorf("day: %w", err)
	}

	cron.month, err = parseField(fields[3], fieldBounds[3].min, fieldBounds[3].max)
	if err != nil {
		return nil, fmt.Errorf("month: %w", err)
	}

	cron.weekday, err = parseField(fields[4], fieldBounds[4].min, fieldBounds[4].max)
	if err != nil {
		return nil, fmt.Errorf("weekday: %w", err)
	}

	return cron, nil
}

// parseField parses a single cron field
func parseField(s string, minVal, maxVal int) (Field, error) {
	field := Field{values: make(map[int]bool)}

	// Handle step values (e.g., */5, 1-10/2)
	step := 1
	if strings.Contains(s, "/") {
		parts := strings.Split(s, "/")
		if len(parts) != 2 {
			return field, ErrInvalidField
		}
		s = parts[0]
		stepVal, err := strconv.Atoi(parts[1])
		if err != nil || stepVal <= 0 {
			return field, fmt.Errorf("%w: invalid step value", ErrInvalidField)
		}
		step = stepVal
	}

	// Handle multiple values (e.g., 1,3,5)
	if strings.Contains(s, ",") {
		parts := strings.Split(s, ",")
		for _, part := range parts {
			subField, err := parseField(part, minVal, maxVal)
			if err != nil {
				return field, err
			}
			for v := range subField.values {
				field.values[v] = true
			}
		}
		return field, nil
	}

	// Handle wildcard
	if s == "*" {
		for i := minVal; i <= maxVal; i += step {
			field.values[i] = true
		}
		return field, nil
	}

	// Handle range (e.g., 1-5)
	if strings.Contains(s, "-") {
		parts := strings.Split(s, "-")
		if len(parts) != 2 {
			return field, ErrInvalidField
		}
		start, err := strconv.Atoi(parts[0])
		if err != nil {
			return field, fmt.Errorf("%w: invalid range start", ErrInvalidField)
		}
		end, err := strconv.Atoi(parts[1])
		if err != nil {
			return field, fmt.Errorf("%w: invalid range end", ErrInvalidField)
		}
		if start < minVal || end > maxVal || start > end {
			return field, fmt.Errorf("%w: range out of bounds", ErrInvalidField)
		}
		for i := start; i <= end; i += step {
			field.values[i] = true
		}
		return field, nil
	}

	// Handle single number
	val, err := strconv.Atoi(s)
	if err != nil {
		return field, fmt.Errorf("%w: invalid number", ErrInvalidField)
	}
	if val < minVal || val > maxVal {
		return field, fmt.Errorf("%w: value out of bounds", ErrInvalidField)
	}
	for i := val; i <= maxVal && i < val+step; i += step {
		if i >= minVal {
			field.values[i] = true
		}
	}
	// For step values with single number
	field.values[val] = true

	return field, nil
}

// Matches checks if the given time matches the cron expression
func (c *CronExpr) Matches(t time.Time) bool {
	return c.minute.values[t.Minute()] &&
		c.hour.values[t.Hour()] &&
		c.day.values[t.Day()] &&
		c.month.values[int(t.Month())] &&
		c.weekday.values[int(t.Weekday())]
}

// Next returns the next execution time after the given time
func (c *CronExpr) Next(after time.Time) time.Time {
	// Start from the next minute
	t := after.Add(time.Minute).Truncate(time.Minute)

	// Search up to 5 years in the future (safety limit)
	endTime := t.AddDate(5, 0, 0)

	for t.Before(endTime) {
		if c.matchesWithDayCheck(t) {
			return t
		}
		t = t.Add(time.Minute)
	}

	return time.Time{} // No match found
}

// matchesWithDayCheck checks if time matches, handling day-of-month and day-of-week conflict
func (c *CronExpr) matchesWithDayCheck(t time.Time) bool {
	// Standard cron behavior: day and weekday are OR'd together
	// If both are restricted (not "*"), either can match
	dayRestricted := !c.day.isWildcard(1, 31)
	weekdayRestricted := !c.weekday.isWildcard(0, 6)

	dayMatches := c.day.values[t.Day()]
	weekdayMatches := c.weekday.values[int(t.Weekday())]

	// If both restricted, use OR logic
	if dayRestricted && weekdayRestricted {
		return c.minute.values[t.Minute()] &&
			c.hour.values[t.Hour()] &&
			c.month.values[int(t.Month())] &&
			(dayMatches || weekdayMatches)
	}

	// Otherwise, both must match
	return c.minute.values[t.Minute()] &&
		c.hour.values[t.Hour()] &&
		c.day.values[t.Day()] &&
		c.month.values[int(t.Month())] &&
		c.weekday.values[int(t.Weekday())]
}

// isWildcard checks if the field matches all values
func (f Field) isWildcard(min, max int) bool {
	return len(f.values) == (max - min + 1)
}

// Prev returns the previous execution time before the given time
func (c *CronExpr) Prev(before time.Time) time.Time {
	// Start from the previous minute
	t := before.Truncate(time.Minute).Add(-time.Minute)

	// Search up to 5 years in the past (safety limit)
	endTime := t.AddDate(-5, 0, 0)

	for t.After(endTime) {
		if c.matchesWithDayCheck(t) {
			return t
		}
		t = t.Add(-time.Minute)
	}

	return time.Time{} // No match found
}

// NextN returns the next n execution times after the given time
func (c *CronExpr) NextN(after time.Time, n int) []time.Time {
	result := make([]time.Time, 0, n)
	t := after

	for len(result) < n {
		next := c.Next(t)
		if next.IsZero() {
			break
		}
		result = append(result, next)
		t = next
	}

	return result
}

// String returns the original cron expression string
func (c *CronExpr) String() string {
	return c.raw
}

// GetFieldValues returns all valid values for a given field
// fieldIndex: 0=minute, 1=hour, 2=day, 3=month, 4=weekday
func (c *CronExpr) GetFieldValues(fieldIndex int) []int {
	var field *Field
	switch fieldIndex {
	case 0:
		field = &c.minute
	case 1:
		field = &c.hour
	case 2:
		field = &c.day
	case 3:
		field = &c.month
	case 4:
		field = &c.weekday
	default:
		return nil
	}

	values := make([]int, 0, len(field.values))
	for v := range field.values {
		values = append(values, v)
	}
	return values
}

// MustParse parses a cron expression or panics
func MustParse(expr string) *CronExpr {
	c, err := Parse(expr)
	if err != nil {
		panic(err)
	}
	return c
}

// Common cron expression presets
var (
	// EveryMinute runs every minute
	EveryMinute = MustParse("* * * * *")
	// EveryHour runs at minute 0 of every hour
	EveryHour = MustParse("0 * * * *")
	// EveryDay runs at midnight every day
	EveryDay = MustParse("0 0 * * *")
	// EveryWeek runs at midnight on Sundays
	EveryWeek = MustParse("0 0 * * 0")
	// EveryMonth runs at midnight on the 1st of every month
	EveryMonth = MustParse("0 0 1 * *")
	// Weekdays runs at midnight on weekdays
	Weekdays = MustParse("0 0 * * 1-5")
	// Weekends runs at midnight on weekends
	Weekends = MustParse("0 0 * * 0,6")
	// EveryFifteenMinutes runs every 15 minutes
	EveryFifteenMinutes = MustParse("*/15 * * * *")
	// EveryThirtyMinutes runs every 30 minutes
	EveryThirtyMinutes = MustParse("*/30 * * * *")
	// EverySixHours runs every 6 hours at minute 0
	EverySixHours = MustParse("0 */6 * * *")
	// TwiceDaily runs at midnight and noon
	TwiceDaily = MustParse("0 0,12 * * *")
)

// IsValid validates a cron expression string
func IsValid(expr string) bool {
	_, err := Parse(expr)
	return err == nil
}

// Describe returns a human-readable description of the cron expression
func (c *CronExpr) Describe() string {
	// Simple description generator
	minuteAll := len(c.minute.values) == 60
	hourAll := len(c.hour.values) == 24
	dayAll := len(c.day.values) == 31
	monthAll := len(c.month.values) == 12
	weekdayAll := len(c.weekday.values) == 7

	// Every minute
	if minuteAll && hourAll && dayAll && monthAll && weekdayAll {
		return "Every minute"
	}

	// Every hour at minute X
	if !minuteAll && hourAll && dayAll && monthAll && weekdayAll && len(c.minute.values) == 1 {
		min := getFirstValue(c.minute)
		return fmt.Sprintf("Every hour at minute %d", min)
	}

	// Daily at specific time
	if len(c.minute.values) == 1 && len(c.hour.values) == 1 && dayAll && monthAll && weekdayAll {
		min := getFirstValue(c.minute)
		hour := getFirstValue(c.hour)
		return fmt.Sprintf("Daily at %02d:%02d", hour, min)
	}

	// Weekdays at specific time
	if len(c.minute.values) == 1 && len(c.hour.values) == 1 && dayAll && monthAll &&
		!weekdayAll && isWeekdays(c.weekday) {
		min := getFirstValue(c.minute)
		hour := getFirstValue(c.hour)
		return fmt.Sprintf("Weekdays at %02d:%02d", hour, min)
	}

	// Default: show the raw expression
	return fmt.Sprintf("Cron: %s", c.raw)
}

func getFirstValue(f Field) int {
	for v := range f.values {
		return v
	}
	return 0
}

func isWeekdays(f Field) bool {
	// Check if weekday field is 1-5 (Mon-Fri only)
	for i := 1; i <= 5; i++ {
		if !f.values[i] {
			return false
		}
	}
	for i := 0; i <= 6; i++ {
		if i >= 1 && i <= 5 {
			continue
		}
		if f.values[i] {
			return false
		}
	}
	return true
}

// ParseWithSeconds parses a 6-field cron expression including seconds
// Format: second minute hour day month weekday
func ParseWithSeconds(expr string) (*CronExpr, error) {
	// For simplicity, we strip seconds and use standard parser
	// A full implementation would extend CronExpr to include seconds
	fields := strings.Fields(expr)
	if len(fields) == 6 {
		// Drop the seconds field
		return Parse(strings.Join(fields[1:], " "))
	}
	return Parse(expr)
}

// ValidateRange checks if values in the field are within bounds
func ValidateField(fieldIndex int, values []int) bool {
	if fieldIndex < 0 || fieldIndex >= len(fieldBounds) {
		return false
	}
	bounds := fieldBounds[fieldIndex]
	for _, v := range values {
		if v < bounds.min || v > bounds.max {
			return false
		}
	}
	return true
}

// NormalizeWeekday handles the conflict between 0=Sunday vs 7=Sunday
// Some cron implementations allow 7 for Sunday
func NormalizeWeekday(weekday int) int {
	if weekday == 7 {
		return 0
	}
	return weekday
}

// GetWeekdayName returns the name of a weekday (0-6, Sunday=0)
func GetWeekdayName(weekday int) string {
	names := []string{"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}
	if weekday < 0 || weekday > 6 {
		return "Unknown"
	}
	return names[weekday]
}

// GetMonthName returns the name of a month (1-12)
func GetMonthName(month int) string {
	names := []string{"", "January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"}
	if month < 1 || month > 12 {
		return "Unknown"
	}
	return names[month]
}

// Builder provides a fluent interface for constructing cron expressions
type Builder struct {
	minute, hour, day, month, weekday string
}

// NewBuilder creates a new cron expression builder
func NewBuilder() *Builder {
	return &Builder{
		minute:  "*",
		hour:    "*",
		day:     "*",
		month:   "*",
		weekday: "*",
	}
}

// AtMinute sets specific minute(s)
func (b *Builder) AtMinute(minutes ...int) *Builder {
	b.minute = formatValues(minutes)
	return b
}

// AtHour sets specific hour(s)
func (b *Builder) AtHour(hours ...int) *Builder {
	b.hour = formatValues(hours)
	return b
}

// OnDay sets specific day(s) of month
func (b *Builder) OnDay(days ...int) *Builder {
	b.day = formatValues(days)
	return b
}

// OnMonth sets specific month(s)
func (b *Builder) OnMonth(months ...int) *Builder {
	b.month = formatValues(months)
	return b
}

// OnWeekday sets specific weekday(s) (0=Sunday)
func (b *Builder) OnWeekday(weekdays ...int) *Builder {
	b.weekday = formatValues(weekdays)
	return b
}

// EveryNMinutes sets to run every n minutes
func (b *Builder) EveryNMinutes(n int) *Builder {
	b.minute = fmt.Sprintf("*/%d", n)
	return b
}

// EveryNHours sets to run every n hours
func (b *Builder) EveryNHours(n int) *Builder {
	b.hour = fmt.Sprintf("*/%d", n)
	return b
}

// Build constructs and parses the cron expression
func (b *Builder) Build() (*CronExpr, error) {
	expr := fmt.Sprintf("%s %s %s %s %s", b.minute, b.hour, b.day, b.month, b.weekday)
	return Parse(expr)
}

func formatValues(values []int) string {
	parts := make([]string, len(values))
	for i, v := range values {
		parts[i] = strconv.Itoa(v)
	}
	return strings.Join(parts, ",")
}

// IsExpired checks if the cron expression will never match again
// (e.g., day 31 in February)
func (c *CronExpr) IsExpired() bool {
	// Check if any month has no valid days
	for month := 1; month <= 12; month++ {
		if !c.month.values[month] {
			continue
		}
		// Check if at least one day is valid for this month
		maxDays := daysInMonth(month)
		for day := 1; day <= maxDays; day++ {
			if c.day.values[day] {
				return false
			}
		}
	}
	return true
}

func daysInMonth(month int) int {
	switch month {
	case 2:
		return 29 // Account for leap years
	case 4, 6, 9, 11:
		return 30
	default:
		return 31
	}
}

// ExpressionRegex for basic validation
var ExpressionRegex = regexp.MustCompile(`^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$`)