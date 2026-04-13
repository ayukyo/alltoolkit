// Package time_utils provides comprehensive time and date manipulation utilities.
// Zero external dependencies - uses only Go standard library.
package time_utils

import (
	"errors"
	"fmt"
	"sort"
	"time"
)

// Common time format constants
const (
	LayoutISO8601      = "2006-01-02T15:04:05Z07:00"
	LayoutISO8601Date  = "2006-01-02"
	LayoutISO8601Time  = "15:04:05"
	LayoutRFC1123      = time.RFC1123
	LayoutRFC3339      = time.RFC3339
	LayoutRFC3339Nano  = time.RFC3339Nano
	LayoutDateTime     = "2006-01-02 15:04:05"
	LayoutDateOnly     = "2006-01-02"
	LayoutTimeOnly     = "15:04:05"
	LayoutDateTimeCN   = "2006年01月02日 15:04:05"
	LayoutDateCN       = "2006年01月02日"
	LayoutUnixDate     = time.UnixDate
	LayoutRubyDate     = time.RubyDate
	LayoutKitchen      = time.Kitchen
	LayoutStamp        = time.Stamp
	LayoutStampMilli   = time.StampMilli
	LayoutStampMicro   = time.StampMicro
	LayoutStampNano    = time.StampNano
)

// Common errors
var (
	ErrInvalidFormat   = errors.New("invalid time format")
	ErrInvalidDuration = errors.New("invalid duration")
	ErrInvalidRange    = errors.New("invalid time range")
	ErrFutureTime     = errors.New("time is in the future")
	ErrPastTime       = errors.New("time is in the past")
)

// ParseOptions provides configuration for parsing time strings
type ParseOptions struct {
	DefaultLocation *time.Location
	Formats         []string
}

// TimeRange represents a time interval
type TimeRange struct {
	Start time.Time
	End   time.Time
}

// Duration represents a human-readable duration
type Duration struct {
	Days    int
	Hours   int
	Minutes int
	Seconds int
}

// ==================== Parsing Functions ====================

// Parse parses a time string with automatic format detection
func Parse(s string, opts ...ParseOptions) (time.Time, error) {
	if s == "" {
		return time.Time{}, ErrInvalidFormat
	}

	var opt ParseOptions
	if len(opts) > 0 {
		opt = opts[0]
	}

	if opt.DefaultLocation == nil {
		opt.DefaultLocation = time.UTC
	}

	// Try common formats
	formats := opt.Formats
	if len(formats) == 0 {
		formats = []string{
			time.RFC3339,
			time.RFC3339Nano,
			"2006-01-02T15:04:05",
			"2006-01-02T15:04:05Z",
			"2006-01-02 15:04:05",
			"2006-01-02 15:04:05 -0700",
			"2006-01-02",
			"01/02/2006",
			"01/02/2006 15:04:05",
			"2006/01/02",
			"2006/01/02 15:04:05",
			time.RFC1123,
			time.RFC1123Z,
			time.UnixDate,
			time.RubyDate,
		}
	}

	for _, format := range formats {
		if t, err := time.Parse(format, s); err == nil {
			return t, nil
		}
		if t, err := time.ParseInLocation(format, s, opt.DefaultLocation); err == nil {
			return t, nil
		}
	}

	return time.Time{}, fmt.Errorf("%w: %s", ErrInvalidFormat, s)
}

// ParseInLocation parses a time string in a specific location
func ParseInLocation(s, format string, loc *time.Location) (time.Time, error) {
	return time.ParseInLocation(format, s, loc)
}

// ParseUnix parses a Unix timestamp (seconds or milliseconds)
func ParseUnix(v interface{}) (time.Time, error) {
	switch t := v.(type) {
	case int64:
		// Auto-detect: if value > 1e12, treat as milliseconds
		if t > 1e12 {
			return time.Unix(0, t*int64(time.Millisecond)), nil
		}
		return time.Unix(t, 0), nil
	case int:
		return time.Unix(int64(t), 0), nil
	case float64:
		sec := int64(t)
		nsec := int64((t - float64(sec)) * 1e9)
		return time.Unix(sec, nsec), nil
	case string:
		// Try parsing as number string
		var num int64
		if _, err := fmt.Sscanf(t, "%d", &num); err == nil {
			if num > 1e12 {
				return time.Unix(0, num*int64(time.Millisecond)), nil
			}
			return time.Unix(num, 0), nil
		}
		return time.Time{}, ErrInvalidFormat
	default:
		return time.Time{}, ErrInvalidFormat
	}
}

// ParseDuration parses a human-readable duration string
// Supports: "1d", "2h", "30m", "45s", "1d2h30m", "1d 2h 30m"
func ParseDuration(s string) (time.Duration, error) {
	if s == "" {
		return 0, ErrInvalidDuration
	}

	var total time.Duration
	var currentNum int64
	var inNumber bool

	for i := 0; i < len(s); i++ {
		c := s[i]
		if c >= '0' && c <= '9' {
			currentNum = currentNum*10 + int64(c-'0')
			inNumber = true
		} else if c == ' ' || c == '\t' {
			continue
		} else if inNumber {
			switch c {
			case 'd':
				total += time.Duration(currentNum) * 24 * time.Hour
			case 'h':
				total += time.Duration(currentNum) * time.Hour
			case 'm':
				if i+1 < len(s) && s[i+1] == 's' {
					total += time.Duration(currentNum) * time.Millisecond
					i++ // skip 's'
				} else {
					total += time.Duration(currentNum) * time.Minute
				}
			case 's':
				total += time.Duration(currentNum) * time.Second
			case 'u', 'µ':
				total += time.Duration(currentNum) * time.Microsecond
			case 'n':
				total += time.Duration(currentNum) * time.Nanosecond
			default:
				return 0, fmt.Errorf("%w: unknown unit '%c'", ErrInvalidDuration, c)
			}
			currentNum = 0
			inNumber = false
		}
	}

	if total == 0 {
		// Try standard duration parsing
		return time.ParseDuration(s)
	}

	return total, nil
}

// ==================== Formatting Functions ====================

// Format formats a time with a given layout
func Format(t time.Time, layout string) string {
	return t.Format(layout)
}

// FormatISO8601 formats time in ISO 8601 format
func FormatISO8601(t time.Time) string {
	return t.Format(LayoutISO8601)
}

// FormatDateTime formats time as "2006-01-02 15:04:05"
func FormatDateTime(t time.Time) string {
	return t.Format(LayoutDateTime)
}

// FormatDate formats time as "2006-01-02"
func FormatDate(t time.Time) string {
	return t.Format(LayoutDateOnly)
}

// FormatTime formats time as "15:04:05"
func FormatTime(t time.Time) string {
	return t.Format(LayoutTimeOnly)
}

// FormatUnixTimestamp returns Unix timestamp in seconds
func FormatUnixTimestamp(t time.Time) int64 {
	return t.Unix()
}

// FormatUnixMilli returns Unix timestamp in milliseconds
func FormatUnixMilli(t time.Time) int64 {
	return t.UnixMilli()
}

// FormatHumanDuration formats duration in human-readable form
func FormatHumanDuration(d time.Duration) string {
	if d < time.Second {
		return fmt.Sprintf("%dms", d.Milliseconds())
	}
	if d < time.Minute {
		return fmt.Sprintf("%.1fs", d.Seconds())
	}
	if d < time.Hour {
		return fmt.Sprintf("%.1fm", d.Minutes())
	}
	if d < 24*time.Hour {
		return fmt.Sprintf("%.1fh", d.Hours())
	}
	days := int(d.Hours()) / 24
	hours := int(d.Hours()) % 24
	if hours == 0 {
		return fmt.Sprintf("%dd", days)
	}
	return fmt.Sprintf("%dd %dh", days, hours)
}

// ==================== Time Calculation Functions ====================

// AddDays adds days to a time
func AddDays(t time.Time, days int) time.Time {
	return t.AddDate(0, 0, days)
}

// AddMonths adds months to a time
func AddMonths(t time.Time, months int) time.Time {
	return t.AddDate(0, months, 0)
}

// AddYears adds years to a time
func AddYears(t time.Time, years int) time.Time {
	return t.AddDate(years, 0, 0)
}

// AddDuration adds a duration to a time
func AddDuration(t time.Time, d time.Duration) time.Time {
	return t.Add(d)
}

// SubtractDuration subtracts a duration from a time
func SubtractDuration(t time.Time, d time.Duration) time.Time {
	return t.Add(-d)
}

// StartOfDay returns the start of the day (00:00:00)
func StartOfDay(t time.Time) time.Time {
	return time.Date(t.Year(), t.Month(), t.Day(), 0, 0, 0, 0, t.Location())
}

// EndOfDay returns the end of the day (23:59:59.999999999)
func EndOfDay(t time.Time) time.Time {
	return time.Date(t.Year(), t.Month(), t.Day(), 23, 59, 59, 999999999, t.Location())
}

// StartOfWeek returns the start of the week (Monday)
func StartOfWeek(t time.Time) time.Time {
	weekday := int(t.Weekday())
	if weekday == 0 {
		weekday = 7 // Sunday = 7 in ISO week
	}
	return StartOfDay(t.AddDate(0, 0, -weekday+1))
}

// EndOfWeek returns the end of the week (Sunday)
func EndOfWeek(t time.Time) time.Time {
	return EndOfDay(StartOfWeek(t).AddDate(0, 0, 6))
}

// StartOfMonth returns the start of the month
func StartOfMonth(t time.Time) time.Time {
	return time.Date(t.Year(), t.Month(), 1, 0, 0, 0, 0, t.Location())
}

// EndOfMonth returns the end of the month
func EndOfMonth(t time.Time) time.Time {
	return time.Date(t.Year(), t.Month()+1, 0, 23, 59, 59, 999999999, t.Location())
}

// StartOfYear returns the start of the year
func StartOfYear(t time.Time) time.Time {
	return time.Date(t.Year(), 1, 1, 0, 0, 0, 0, t.Location())
}

// EndOfYear returns the end of the year
func EndOfYear(t time.Time) time.Time {
	return time.Date(t.Year(), 12, 31, 23, 59, 59, 999999999, t.Location())
}

// ==================== Comparison Functions ====================

// IsBefore checks if t1 is before t2
func IsBefore(t1, t2 time.Time) bool {
	return t1.Before(t2)
}

// IsAfter checks if t1 is after t2
func IsAfter(t1, t2 time.Time) bool {
	return t1.After(t2)
}

// IsEqual checks if two times are equal (including timezone)
func IsEqual(t1, t2 time.Time) bool {
	return t1.Equal(t2)
}

// IsSameDay checks if two times are on the same day
func IsSameDay(t1, t2 time.Time) bool {
	y1, m1, d1 := t1.Date()
	y2, m2, d2 := t2.Date()
	return y1 == y2 && m1 == m2 && d1 == d2
}

// IsSameMonth checks if two times are in the same month
func IsSameMonth(t1, t2 time.Time) bool {
	return t1.Year() == t2.Year() && t1.Month() == t2.Month()
}

// IsSameYear checks if two times are in the same year
func IsSameYear(t1, t2 time.Time) bool {
	return t1.Year() == t2.Year()
}

// IsToday checks if the time is today
func IsToday(t time.Time) bool {
	return IsSameDay(t, time.Now())
}

// IsYesterday checks if the time was yesterday
func IsYesterday(t time.Time) bool {
	return IsSameDay(t, AddDays(time.Now(), -1))
}

// IsTomorrow checks if the time is tomorrow
func IsTomorrow(t time.Time) bool {
	return IsSameDay(t, AddDays(time.Now(), 1))
}

// IsWeekend checks if the time is on a weekend (Saturday or Sunday)
func IsWeekend(t time.Time) bool {
	weekday := t.Weekday()
	return weekday == time.Saturday || weekday == time.Sunday
}

// IsWeekday checks if the time is on a weekday (Monday-Friday)
func IsWeekday(t time.Time) bool {
	return !IsWeekend(t)
}

// IsFuture checks if the time is in the future
func IsFuture(t time.Time) bool {
	return t.After(time.Now())
}

// IsPast checks if the time is in the past
func IsPast(t time.Time) bool {
	return t.Before(time.Now())
}

// IsLeapYear checks if the year is a leap year
func IsLeapYear(year int) bool {
	return year%4 == 0 && (year%100 != 0 || year%400 == 0)
}

// DaysInMonth returns the number of days in a month
func DaysInMonth(year int, month time.Month) int {
	return time.Date(year, month+1, 0, 0, 0, 0, 0, time.UTC).Day()
}

// ==================== Time Difference Functions ====================

// Diff calculates the difference between two times
func Diff(t1, t2 time.Time) time.Duration {
	return t2.Sub(t1)
}

// DiffInDays returns the difference in days
func DiffInDays(t1, t2 time.Time) int {
	d := int(t2.Sub(t1).Hours() / 24)
	return d
}

// DiffInHours returns the difference in hours
func DiffInHours(t1, t2 time.Time) float64 {
	return t2.Sub(t1).Hours()
}

// DiffInMinutes returns the difference in minutes
func DiffInMinutes(t1, t2 time.Time) float64 {
	return t2.Sub(t1).Minutes()
}

// DiffInSeconds returns the difference in seconds
func DiffInSeconds(t1, t2 time.Time) float64 {
	return t2.Sub(t1).Seconds()
}

// DiffHuman returns a human-readable difference
func DiffHuman(t1, t2 time.Time) string {
	d := Diff(t1, t2)
	return FormatHumanDuration(d)
}

// DiffDetailed returns detailed time difference
func DiffDetailed(t1, t2 time.Time) Duration {
	d := t2.Sub(t1)
	totalSeconds := int(d.Seconds())
	
	days := totalSeconds / 86400
	totalSeconds %= 86400
	
	hours := totalSeconds / 3600
	totalSeconds %= 3600
	
	minutes := totalSeconds / 60
	seconds := totalSeconds % 60
	
	return Duration{
		Days:    days,
		Hours:   hours,
		Minutes: minutes,
		Seconds: seconds,
	}
}

// ==================== Time Range Functions ====================

// NewTimeRange creates a new time range
func NewTimeRange(start, end time.Time) (TimeRange, error) {
	if end.Before(start) {
		return TimeRange{}, ErrInvalidRange
	}
	return TimeRange{Start: start, End: end}, nil
}

// Duration returns the duration of the range
func (tr TimeRange) Duration() time.Duration {
	return tr.End.Sub(tr.Start)
}

// Contains checks if a time is within the range
func (tr TimeRange) Contains(t time.Time) bool {
	return (t.Equal(tr.Start) || t.After(tr.Start)) &&
		(t.Equal(tr.End) || t.Before(tr.End))
}

// Overlaps checks if two ranges overlap
func (tr TimeRange) Overlaps(other TimeRange) bool {
	return tr.Start.Before(other.End) && tr.End.After(other.Start)
}

// Split splits the range into equal intervals
func (tr TimeRange) Split(interval time.Duration) []time.Time {
	var result []time.Time
	for t := tr.Start; t.Before(tr.End) || t.Equal(tr.End); t = t.Add(interval) {
		result = append(result, t)
	}
	return result
}

// SplitDays splits the range by days
func (tr TimeRange) SplitDays() []time.Time {
	return tr.Split(24 * time.Hour)
}

// ==================== Utility Functions ====================

// Now returns the current time in UTC
func Now() time.Time {
	return time.Now().UTC()
}

// NowLocal returns the current time in local timezone
func NowLocal() time.Time {
	return time.Now()
}

// NowIn returns the current time in a specific timezone
func NowIn(loc *time.Location) time.Time {
	return time.Now().In(loc)
}

// Unix returns a time from Unix timestamp
func Unix(sec int64, nsec int64) time.Time {
	return time.Unix(sec, nsec)
}

// UnixMilli returns a time from Unix millisecond timestamp
func UnixMilli(msec int64) time.Time {
	return time.Unix(0, msec*int64(time.Millisecond))
}

// Location returns a location by name (e.g., "America/New_York", "Asia/Shanghai")
func Location(name string) (*time.Location, error) {
	return time.LoadLocation(name)
}

// MustLocation returns a location, panics on error
func MustLocation(name string) *time.Location {
	loc, err := time.LoadLocation(name)
	if err != nil {
		panic(err)
	}
	return loc
}

// Convert converts a time to a different timezone
func Convert(t time.Time, loc *time.Location) time.Time {
	return t.In(loc)
}

// ToUTC converts a time to UTC
func ToUTC(t time.Time) time.Time {
	return t.UTC()
}

// ToLocal converts a time to local timezone
func ToLocal(t time.Time) time.Time {
	return t.Local()
}

// ==================== Timer/Stopwatch Functions ====================

// Stopwatch represents a simple stopwatch
type Stopwatch struct {
	start   time.Time
	elapsed time.Duration
	running bool
}

// NewStopwatch creates a new stopwatch
func NewStopwatch() *Stopwatch {
	return &Stopwatch{
		start:   time.Time{},
		elapsed: 0,
		running: false,
	}
}

// Start starts or continues the stopwatch
func (s *Stopwatch) Start() *Stopwatch {
	if !s.running {
		s.start = time.Now()
		s.running = true
	}
	return s
}

// Stop stops the stopwatch
func (s *Stopwatch) Stop() *Stopwatch {
	if s.running {
		s.elapsed += time.Since(s.start)
		s.running = false
	}
	return s
}

// Reset resets the stopwatch
func (s *Stopwatch) Reset() *Stopwatch {
	s.elapsed = 0
	s.running = false
	return s
}

// Elapsed returns the elapsed time
func (s *Stopwatch) Elapsed() time.Duration {
	if s.running {
		return s.elapsed + time.Since(s.start)
	}
	return s.elapsed
}

// ElapsedString returns elapsed time as string
func (s *Stopwatch) ElapsedString() string {
	return FormatHumanDuration(s.Elapsed())
}

// ==================== Countdown Functions ====================

// Countdown represents a countdown timer
type Countdown struct {
	endTime time.Time
}

// NewCountdown creates a new countdown
func NewCountdown(duration time.Duration) *Countdown {
	return &Countdown{
		endTime: time.Now().Add(duration),
	}
}

// NewCountdownTo creates a countdown to a specific time
func NewCountdownTo(t time.Time) *Countdown {
	return &Countdown{
		endTime: t,
	}
}

// Remaining returns the remaining time
func (c *Countdown) Remaining() time.Duration {
	remaining := time.Until(c.endTime)
	if remaining < 0 {
		return 0
	}
	return remaining
}

// IsExpired checks if the countdown has expired
func (c *Countdown) IsExpired() bool {
	return time.Now().After(c.endTime)
}

// IsRunning checks if the countdown is still running
func (c *Countdown) IsRunning() bool {
	return !c.IsExpired()
}

// Progress returns the progress as a percentage (0.0 to 1.0)
func (c *Countdown) Progress(totalDuration time.Duration) float64 {
	elapsed := totalDuration - c.Remaining()
	return float64(elapsed) / float64(totalDuration)
}

// ==================== Cron-like Scheduling ====================

// NextWeekday returns the next occurrence of a specific weekday
func NextWeekday(t time.Time, weekday time.Weekday) time.Time {
	daysAhead := int(weekday) - int(t.Weekday())
	if daysAhead <= 0 {
		daysAhead += 7
	}
	return AddDays(t, daysAhead)
}

// PreviousWeekday returns the previous occurrence of a specific weekday
func PreviousWeekday(t time.Time, weekday time.Weekday) time.Time {
	daysBehind := int(t.Weekday()) - int(weekday)
	if daysBehind <= 0 {
		daysBehind += 7
	}
	return AddDays(t, -daysBehind)
}

// NextNthWeekday returns the nth occurrence of a weekday in a month
// e.g., 2nd Tuesday, 3rd Friday
func NextNthWeekday(year int, month time.Month, weekday time.Weekday, n int) time.Time {
	first := time.Date(year, month, 1, 0, 0, 0, 0, time.UTC)
	count := 0
	
	for d := first; d.Month() == month; d = d.AddDate(0, 0, 1) {
		if d.Weekday() == weekday {
			count++
			if count == n {
				return d
			}
		}
	}
	
	return time.Time{}
}

// LastNthWeekday returns the last nth occurrence of a weekday in a month
// e.g., last Friday of the month
func LastNthWeekday(year int, month time.Month, weekday time.Weekday) time.Time {
	lastDay := time.Date(year, month+1, 0, 0, 0, 0, 0, time.UTC)
	
	for d := lastDay; d.Month() == month; d = d.AddDate(0, 0, -1) {
		if d.Weekday() == weekday {
			return d
		}
	}
	
	return time.Time{}
}

// Age calculates age from birthday
func Age(birthday time.Time) int {
	now := time.Now()
	age := now.Year() - birthday.Year()
	
	// Adjust if birthday hasn't occurred this year yet
	if now.Month() < birthday.Month() ||
		(now.Month() == birthday.Month() && now.Day() < birthday.Day()) {
		age--
	}
	
	return age
}

// AgeDetailed calculates age with months and days
func AgeDetailed(birthday time.Time) (years, months, days int) {
	now := time.Now()
	
	years = now.Year() - birthday.Year()
	months = int(now.Month()) - int(birthday.Month())
	days = now.Day() - birthday.Day()
	
	if days < 0 {
		months--
		days += DaysInMonth(now.Year(), now.Month()-1)
	}
	
	if months < 0 {
		years--
		months += 12
	}
	
	return
}

// SortTimes sorts a slice of times
func SortTimes(times []time.Time) []time.Time {
	sorted := make([]time.Time, len(times))
	copy(sorted, times)
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i].Before(sorted[j])
	})
	return sorted
}

// Min returns the earliest time from a slice
func Min(times ...time.Time) time.Time {
	if len(times) == 0 {
		return time.Time{}
	}
	min := times[0]
	for _, t := range times[1:] {
		if t.Before(min) {
			min = t
		}
	}
	return min
}

// Max returns the latest time from a slice
func Max(times ...time.Time) time.Time {
	if len(times) == 0 {
		return time.Time{}
	}
	max := times[0]
	for _, t := range times[1:] {
		if t.After(max) {
			max = t
		}
	}
	return max
}

// Clamp clamps a time to a range
func Clamp(t, min, max time.Time) time.Time {
	if t.Before(min) {
		return min
	}
	if t.After(max) {
		return max
	}
	return t
}