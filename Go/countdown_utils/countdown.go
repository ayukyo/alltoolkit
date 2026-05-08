// Package countdown_utils provides countdown and timer utilities.
// It supports calculating time differences, formatting countdown displays,
// and working day calculations with zero external dependencies.
package countdown_utils

import (
	"fmt"
	"math"
	"time"
)

// Duration represents a broken-down duration in human-readable units
type Duration struct {
	Days    int
	Hours   int
	Minutes int
	Seconds int
	Total   time.Duration
}

// Countdown represents a countdown to a specific target time
type Countdown struct {
	Target    time.Time
	Start     time.Time
	Remaining time.Duration
	Elapsed   time.Duration
	IsPast    bool
}

// TimerState represents the state of a timer
type TimerState int

const (
	TimerStopped TimerState = iota
	TimerRunning
	TimerPaused
	TimerCompleted
)

// Timer represents a countdown timer with pause/resume functionality
type Timer struct {
	duration   time.Duration
	remaining  time.Duration
	state      TimerState
	startTime  time.Time
	pauseTime  time.Time
	onTick     func(remaining time.Duration)
	onComplete func()
}

// NewCountdown creates a new countdown to the specified target time
func NewCountdown(target time.Time) *Countdown {
	now := time.Now()
	remaining := target.Sub(now)
	return &Countdown{
		Target:    target,
		Start:     now,
		Remaining: remaining,
		Elapsed:   0,
		IsPast:    remaining < 0,
	}
}

// NewCountdownFromDuration creates a countdown from a duration
func NewCountdownFromDuration(d time.Duration) *Countdown {
	target := time.Now().Add(d)
	return NewCountdown(target)
}

// Update refreshes the countdown with the current time
func (c *Countdown) Update() {
	now := time.Now()
	c.Remaining = c.Target.Sub(now)
	c.Elapsed = c.Target.Sub(c.Start) - c.Remaining
	c.IsPast = c.Remaining < 0
}

// GetDuration returns the remaining time as a Duration struct
func (c *Countdown) GetDuration() Duration {
	return ParseDuration(c.Remaining)
}

// ParseDuration converts a time.Duration into a human-readable Duration struct
func ParseDuration(d time.Duration) Duration {
	abs := d
	if d < 0 {
		abs = -d
	}

	totalSeconds := int(abs.Seconds())
	days := totalSeconds / 86400
	hours := (totalSeconds % 86400) / 3600
	minutes := (totalSeconds % 3600) / 60
	seconds := totalSeconds % 60

	return Duration{
		Days:    days,
		Hours:   hours,
		Minutes: minutes,
		Seconds: seconds,
		Total:   d,
	}
}

// Format formats a Duration in a human-readable string
func (d Duration) Format() string {
	if d.Total < 0 {
		return "-" + d.formatAbs()
	}
	return d.formatAbs()
}

func (d Duration) formatAbs() string {
	parts := []string{}
	if d.Days > 0 {
		parts = append(parts, fmt.Sprintf("%dd", d.Days))
	}
	if d.Hours > 0 || d.Days > 0 {
		parts = append(parts, fmt.Sprintf("%dh", d.Hours))
	}
	if d.Minutes > 0 || d.Hours > 0 || d.Days > 0 {
		parts = append(parts, fmt.Sprintf("%dm", d.Minutes))
	}
	parts = append(parts, fmt.Sprintf("%ds", d.Seconds))
	return fmt.Sprintf("%s", joinParts(parts))
}

// FormatLong formats a Duration in a long, readable format
func (d Duration) FormatLong() string {
	parts := []string{}
	if d.Days > 0 {
		parts = append(parts, pluralize(d.Days, "day"))
	}
	if d.Hours > 0 || d.Days > 0 {
		parts = append(parts, pluralize(d.Hours, "hour"))
	}
	if d.Minutes > 0 || d.Hours > 0 || d.Days > 0 {
		parts = append(parts, pluralize(d.Minutes, "minute"))
	}
	parts = append(parts, pluralize(d.Seconds, "second"))
	
	result := ""
	if d.Total < 0 {
		result = "-"
	}
	return result + joinPartsLong(parts)
}

// FormatCompact formats a Duration in a compact HH:MM:SS or DD:HH:MM:SS format
func (d Duration) FormatCompact() string {
	if d.Days > 0 {
		return fmt.Sprintf("%d:%02d:%02d:%02d", d.Days, d.Hours, d.Minutes, d.Seconds)
	}
	return fmt.Sprintf("%02d:%02d:%02d", d.Hours, d.Minutes, d.Seconds)
}

// FormatDigital formats a Duration like a digital clock
func (d Duration) FormatDigital() string {
	return fmt.Sprintf("%02d:%02d:%02d", d.Hours, d.Minutes, d.Seconds)
}

// FormatCustom formats a Duration using a custom format string
// Supported placeholders: {d}, {h}, {m}, {s}, {D}, {H}, {M}, {S}
// Lowercase = raw numbers, Uppercase = zero-padded (2 digits)
func (d Duration) FormatCustom(format string) string {
	result := format
	result = replacePlaceholder(result, "{d}", d.Days, false)
	result = replacePlaceholder(result, "{D}", d.Days, true)
	result = replacePlaceholder(result, "{h}", d.Hours, false)
	result = replacePlaceholder(result, "{H}", d.Hours, true)
	result = replacePlaceholder(result, "{m}", d.Minutes, false)
	result = replacePlaceholder(result, "{M}", d.Minutes, true)
	result = replacePlaceholder(result, "{s}", d.Seconds, false)
	result = replacePlaceholder(result, "{S}", d.Seconds, true)
	return result
}

// FormatCountdown formats a time.Duration in a human-readable string
func FormatCountdown(d time.Duration) string {
	return ParseDuration(d).Format()
}

// FormatCountdownLong formats a time.Duration in a long format
func FormatCountdownLong(d time.Duration) string {
	return ParseDuration(d).FormatLong()
}

// FormatCountdownCompact formats a time.Duration in compact format
func FormatCountdownCompact(d time.Duration) string {
	return ParseDuration(d).FormatCompact()
}

// TimeUntil calculates the time until a target time
func TimeUntil(target time.Time) time.Duration {
	return target.Sub(time.Now())
}

// TimeSince calculates the time since a past time
func TimeSince(past time.Time) time.Duration {
	return time.Since(past)
}

// DaysUntil calculates the number of days until a target time
func DaysUntil(target time.Time) int {
	d := TimeUntil(target)
	return int(math.Ceil(d.Hours() / 24))
}

// DaysSince calculates the number of days since a past time
func DaysSince(past time.Time) int {
	d := TimeSince(past)
	return int(math.Floor(d.Hours() / 24))
}

// WorkingDaysUntil calculates working days (Mon-Fri) until a target date
func WorkingDaysUntil(target time.Time) int {
	return WorkingDaysBetween(time.Now(), target)
}

// WorkingDaysSince calculates working days (Mon-Fri) since a past date
func WorkingDaysSince(past time.Time) int {
	return WorkingDaysBetween(past, time.Now())
}

// WorkingDaysBetween calculates working days (Mon-Fri) between two dates
func WorkingDaysBetween(start, end time.Time) int {
	if start.After(end) {
		start, end = end, start
	}
	
	count := 0
	current := time.Date(start.Year(), start.Month(), start.Day(), 0, 0, 0, 0, start.Location())
	endDate := time.Date(end.Year(), end.Month(), end.Day(), 0, 0, 0, 0, end.Location())
	
	for current.Before(endDate) {
		weekday := current.Weekday()
		if weekday != time.Saturday && weekday != time.Sunday {
			count++
		}
		current = current.AddDate(0, 0, 1)
	}
	
	return count
}

// IsWeekend checks if a given time falls on a weekend
func IsWeekend(t time.Time) bool {
	weekday := t.Weekday()
	return weekday == time.Saturday || weekday == time.Sunday
}

// IsWorkingDay checks if a given time falls on a working day (Mon-Fri)
func IsWorkingDay(t time.Time) bool {
	return !IsWeekend(t)
}

// NextWorkingDay returns the next working day from a given time
func NextWorkingDay(t time.Time) time.Time {
	next := t.AddDate(0, 0, 1)
	for IsWeekend(next) {
		next = next.AddDate(0, 0, 1)
	}
	return next
}

// PreviousWorkingDay returns the previous working day from a given time
func PreviousWorkingDay(t time.Time) time.Time {
	prev := t.AddDate(0, 0, -1)
	for IsWeekend(prev) {
		prev = prev.AddDate(0, 0, -1)
	}
	return prev
}

// AddWorkingDays adds n working days to a given time
func AddWorkingDays(t time.Time, days int) time.Time {
	result := t
	if days > 0 {
		for i := 0; i < days; i++ {
			result = NextWorkingDay(result)
		}
	} else if days < 0 {
		for i := 0; i > days; i-- {
			result = PreviousWorkingDay(result)
		}
	}
	return result
}

// NewTimer creates a new countdown timer
func NewTimer(duration time.Duration) *Timer {
	return &Timer{
		duration:  duration,
		remaining: duration,
		state:     TimerStopped,
	}
}

// Start begins the timer
func (t *Timer) Start() {
	if t.state == TimerStopped || t.state == TimerCompleted {
		t.remaining = t.duration
		t.state = TimerRunning
		t.startTime = time.Now()
	} else if t.state == TimerPaused {
		t.state = TimerRunning
		t.startTime = time.Now().Add(-t.remaining)
	}
}

// Stop stops the timer
func (t *Timer) Stop() {
	t.state = TimerStopped
	t.remaining = t.duration
}

// Pause pauses the timer
func (t *Timer) Pause() {
	if t.state == TimerRunning {
		t.remaining = t.duration - time.Since(t.startTime)
		t.state = TimerPaused
		t.pauseTime = time.Now()
	}
}

// Resume resumes a paused timer
func (t *Timer) Resume() {
	if t.state == TimerPaused {
		t.state = TimerRunning
		t.startTime = time.Now().Add(-t.remaining)
	}
}

// Reset resets the timer to its initial state
func (t *Timer) Reset() {
	t.remaining = t.duration
	t.state = TimerStopped
}

// GetRemaining returns the remaining time
func (t *Timer) GetRemaining() time.Duration {
	if t.state == TimerRunning {
		remaining := t.duration - time.Since(t.startTime)
		if remaining <= 0 {
			t.state = TimerCompleted
			if t.onComplete != nil {
				t.onComplete()
			}
			return 0
		}
		return remaining
	}
	return t.remaining
}

// GetState returns the current timer state
func (t *Timer) GetState() TimerState {
	return t.state
}

// SetOnTick sets a callback for timer ticks
func (t *Timer) SetOnTick(callback func(remaining time.Duration)) {
	t.onTick = callback
}

// SetOnComplete sets a callback for timer completion
func (t *Timer) SetOnComplete(callback func()) {
	t.onComplete = callback
}

// IsExpired checks if a target time has passed
func (c *Countdown) IsExpired() bool {
	return c.Remaining <= 0
}

// Progress returns the progress as a percentage (0.0 to 1.0)
func (c *Countdown) Progress() float64 {
	if c.Remaining <= 0 {
		return 1.0
	}
	total := c.Target.Sub(c.Start)
	if total <= 0 {
		return 1.0
	}
	return float64(c.Elapsed) / float64(total)
}

// ProgressPercent returns the progress as a percentage (0 to 100)
func (c *Countdown) ProgressPercent() float64 {
	return c.Progress() * 100
}

// FormatProgress returns a progress bar string
func (c *Countdown) FormatProgress(width int) string {
	progress := c.Progress()
	if progress > 1.0 {
		progress = 1.0
	}
	filled := int(float64(width) * progress)
	empty := width - filled
	
	bar := ""
	for i := 0; i < filled; i++ {
		bar += "█"
	}
	for i := 0; i < empty; i++ {
		bar += "░"
	}
	return bar
}

// CountdownToNewYear returns a countdown to the next new year
func CountdownToNewYear() *Countdown {
	now := time.Now()
	nextYear := time.Date(now.Year()+1, 1, 1, 0, 0, 0, 0, now.Location())
	return NewCountdown(nextYear)
}

// CountdownTo returns a countdown to a specific date/time
func CountdownTo(year int, month time.Month, day int, hour, min, sec int, loc *time.Location) *Countdown {
	target := time.Date(year, month, day, hour, min, sec, 0, loc)
	return NewCountdown(target)
}

// ParseDurationString parses a duration string like "1d2h3m4s"
func ParseDurationString(s string) (time.Duration, error) {
	var total time.Duration
	var num int
	var unit rune
	var err error
	
	i := 0
	for i < len(s) {
		// Skip whitespace
		for i < len(s) && s[i] == ' ' {
			i++
		}
		if i >= len(s) {
			break
		}
		
		// Parse number
		start := i
		for i < len(s) && (s[i] >= '0' && s[i] <= '9') {
			i++
		}
		if i == start {
			return 0, fmt.Errorf("expected number at position %d", i)
		}
		num = 0
		for _, c := range s[start:i] {
			num = num*10 + int(c-'0')
		}
		
		// Parse unit
		if i >= len(s) {
			return 0, fmt.Errorf("expected unit after number")
		}
		unit = rune(s[i])
		i++
		
		// Convert to duration
		switch unit {
		case 'd':
			total += time.Duration(num) * 24 * time.Hour
		case 'h':
			total += time.Duration(num) * time.Hour
		case 'm':
			total += time.Duration(num) * time.Minute
		case 's':
			total += time.Duration(num) * time.Second
		default:
			return 0, fmt.Errorf("unknown unit: %c", unit)
		}
	}
	
	return total, err
}

// Helper functions

func joinParts(parts []string) string {
	result := ""
	for i, part := range parts {
		if i > 0 {
			result += " "
		}
		result += part
	}
	return result
}

func joinPartsLong(parts []string) string {
	result := ""
	for i, part := range parts {
		if i > 0 {
			if i == len(parts)-1 {
				result += " and "
			} else {
				result += ", "
			}
		}
		result += part
	}
	return result
}

func pluralize(n int, singular string) string {
	if n == 1 {
		return fmt.Sprintf("%d %s", n, singular)
	}
	return fmt.Sprintf("%d %ss", n, singular)
}

func replacePlaceholder(s string, placeholder string, value int, pad bool) string {
	var replacement string
	if pad {
		replacement = fmt.Sprintf("%02d", value)
	} else {
		replacement = fmt.Sprintf("%d", value)
	}
	
	result := ""
	for i := 0; i < len(s); {
		if i <= len(s)-len(placeholder) && s[i:i+len(placeholder)] == placeholder {
			result += replacement
			i += len(placeholder)
		} else {
			result += string(s[i])
			i++
		}
	}
	return result
}