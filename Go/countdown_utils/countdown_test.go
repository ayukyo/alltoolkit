package countdown_utils

import (
	"testing"
	"time"
)

func TestParseDuration(t *testing.T) {
	tests := []struct {
		name           string
		duration       time.Duration
		expectedDays   int
		expectedHours  int
		expectedMins   int
		expectedSecs   int
	}{
		{"zero", 0, 0, 0, 0, 0},
		{"one second", time.Second, 0, 0, 0, 1},
		{"one minute", time.Minute, 0, 0, 1, 0},
		{"one hour", time.Hour, 0, 1, 0, 0},
		{"one day", 24 * time.Hour, 1, 0, 0, 0},
		{"complex", 2*24*time.Hour + 3*time.Hour + 15*time.Minute + 30*time.Second, 2, 3, 15, 30},
		{"negative", -time.Hour, 0, 1, 0, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ParseDuration(tt.duration)
			if result.Days != tt.expectedDays {
				t.Errorf("expected days %d, got %d", tt.expectedDays, result.Days)
			}
			if result.Hours != tt.expectedHours {
				t.Errorf("expected hours %d, got %d", tt.expectedHours, result.Hours)
			}
			if result.Minutes != tt.expectedMins {
				t.Errorf("expected minutes %d, got %d", tt.expectedMins, result.Minutes)
			}
			if result.Seconds != tt.expectedSecs {
				t.Errorf("expected seconds %d, got %d", tt.expectedSecs, result.Seconds)
			}
		})
	}
}

func TestDurationFormat(t *testing.T) {
	tests := []struct {
		name     string
		duration time.Duration
		expected string
	}{
		{"zero", 0, "0s"},
		{"seconds", 45 * time.Second, "45s"},
		{"minutes", 5 * time.Minute, "5m 0s"},
		{"hours", 3 * time.Hour, "3h 0m 0s"},
		{"days", 2 * 24 * time.Hour, "2d 0h 0m 0s"},
		{"complex", 1*24*time.Hour + 2*time.Hour + 30*time.Minute + 15*time.Second, "1d 2h 30m 15s"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ParseDuration(tt.duration)
			if result.Format() != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result.Format())
			}
		})
	}
}

func TestDurationFormatCompact(t *testing.T) {
	tests := []struct {
		name     string
		duration time.Duration
		expected string
	}{
		{"hours only", 3*time.Hour + 30*time.Minute + 15*time.Second, "03:30:15"},
		{"days included", 2*24*time.Hour + 5*time.Hour + 30*time.Minute + 45*time.Second, "2:05:30:45"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ParseDuration(tt.duration)
			if result.FormatCompact() != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result.FormatCompact())
			}
		})
	}
}

func TestDurationFormatCustom(t *testing.T) {
	d := ParseDuration(1*24*time.Hour + 2*time.Hour + 30*time.Minute + 45*time.Second)
	
	tests := []struct {
		name     string
		format   string
		expected string
	}{
		{"full padded", "{D} days, {H}:{M}:{S}", "01 days, 02:30:45"},
		{"full unpadded", "{d} days, {h}:{m}:{s}", "1 days, 2:30:45"},
		{"clock style", "{H}:{M}:{S}", "02:30:45"},
		{"compact", "{d}d {h}h {m}m {s}s", "1d 2h 30m 45s"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := d.FormatCustom(tt.format)
			if result != tt.expected {
				t.Errorf("expected %q, got %q", tt.expected, result)
			}
		})
	}
}

func TestNewCountdown(t *testing.T) {
	target := time.Now().Add(2 * time.Hour)
	c := NewCountdown(target)
	
	if c.Target != target {
		t.Errorf("expected target %v, got %v", target, c.Target)
	}
	if c.IsPast {
		t.Error("countdown should not be in past")
	}
	if c.Remaining <= 0 {
		t.Error("remaining time should be positive")
	}
}

func TestCountdownIsExpired(t *testing.T) {
	// Past countdown
	pastTarget := time.Now().Add(-1 * time.Hour)
	c := NewCountdown(pastTarget)
	c.Update()
	
	if !c.IsPast {
		t.Error("countdown should be in past")
	}
	if !c.IsExpired() {
		t.Error("countdown should be expired")
	}
	
	// Future countdown
	futureTarget := time.Now().Add(1 * time.Hour)
	c2 := NewCountdown(futureTarget)
	c2.Update()
	
	if c2.IsExpired() {
		t.Error("future countdown should not be expired")
	}
}

func TestTimerBasic(t *testing.T) {
	timer := NewTimer(5 * time.Second)
	
	if timer.GetState() != TimerStopped {
		t.Error("timer should be stopped initially")
	}
	
	timer.Start()
	if timer.GetState() != TimerRunning {
		t.Error("timer should be running after start")
	}
	
	timer.Pause()
	if timer.GetState() != TimerPaused {
		t.Error("timer should be paused after pause")
	}
	
	timer.Resume()
	if timer.GetState() != TimerRunning {
		t.Error("timer should be running after resume")
	}
	
	timer.Stop()
	if timer.GetState() != TimerStopped {
		t.Error("timer should be stopped after stop")
	}
}

func TestTimerReset(t *testing.T) {
	timer := NewTimer(10 * time.Second)
	timer.Start()
	
	remaining := timer.GetRemaining()
	if remaining <= 0 || remaining > 10*time.Second {
		t.Errorf("unexpected remaining time: %v", remaining)
	}
	
	timer.Reset()
	if timer.GetState() != TimerStopped {
		t.Error("timer should be stopped after reset")
	}
	if timer.remaining != 10*time.Second {
		t.Error("remaining should be reset to original duration")
	}
}

func TestWorkingDaysBetween(t *testing.T) {
	// Monday to Friday (Mon, Tue, Wed, Thu) = 4 working days
	monday := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC) // Monday
	friday := time.Date(2024, 1, 5, 0, 0, 0, 0, time.UTC) // Friday
	
	days := WorkingDaysBetween(monday, friday)
	if days != 4 {
		t.Errorf("expected 4 working days, got %d", days)
	}
	
	// Monday to next Monday (5 working days)
	nextMonday := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC)
	days = WorkingDaysBetween(monday, nextMonday)
	if days != 5 {
		t.Errorf("expected 5 working days, got %d", days)
	}
}

func TestIsWeekend(t *testing.T) {
	saturday := time.Date(2024, 1, 6, 0, 0, 0, 0, time.UTC)
	sunday := time.Date(2024, 1, 7, 0, 0, 0, 0, time.UTC)
	monday := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC)
	
	if !IsWeekend(saturday) {
		t.Error("Saturday should be weekend")
	}
	if !IsWeekend(sunday) {
		t.Error("Sunday should be weekend")
	}
	if IsWeekend(monday) {
		t.Error("Monday should not be weekend")
	}
}

func TestIsWorkingDay(t *testing.T) {
	saturday := time.Date(2024, 1, 6, 0, 0, 0, 0, time.UTC)
	monday := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC)
	
	if IsWorkingDay(saturday) {
		t.Error("Saturday should not be a working day")
	}
	if !IsWorkingDay(monday) {
		t.Error("Monday should be a working day")
	}
}

func TestNextWorkingDay(t *testing.T) {
	friday := time.Date(2024, 1, 5, 0, 0, 0, 0, time.UTC)
	next := NextWorkingDay(friday)
	expected := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC) // Monday
	
	if !next.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, next)
	}
	
	monday := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC)
	next = NextWorkingDay(monday)
	expected = time.Date(2024, 1, 9, 0, 0, 0, 0, time.UTC) // Tuesday
	
	if !next.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, next)
	}
}

func TestPreviousWorkingDay(t *testing.T) {
	monday := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC)
	prev := PreviousWorkingDay(monday)
	expected := time.Date(2024, 1, 5, 0, 0, 0, 0, time.UTC) // Friday
	
	if !prev.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, prev)
	}
}

func TestAddWorkingDays(t *testing.T) {
	monday := time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC)
	
	// Add 5 working days should get to next Monday
	result := AddWorkingDays(monday, 5)
	expected := time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC)
	
	if !result.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
	
	// Add negative working days
	result = AddWorkingDays(monday, -1)
	expected = time.Date(2024, 1, 5, 0, 0, 0, 0, time.UTC) // Friday
	
	if !result.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, result)
	}
}

func TestParseDurationString(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected time.Duration
	}{
		{"seconds only", "30s", 30 * time.Second},
		{"minutes only", "5m", 5 * time.Minute},
		{"hours only", "2h", 2 * time.Hour},
		{"days only", "1d", 24 * time.Hour},
		{"complex", "1d2h30m45s", 24*time.Hour + 2*time.Hour + 30*time.Minute + 45*time.Second},
		{"with spaces", "1d 2h 3m 4s", 24*time.Hour + 2*time.Hour + 3*time.Minute + 4*time.Second},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ParseDurationString(tt.input)
			if err != nil {
				t.Errorf("unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("expected %v, got %v", tt.expected, result)
			}
		})
	}
}

func TestParseDurationStringErrors(t *testing.T) {
	_, err := ParseDurationString("invalid")
	if err == nil {
		t.Error("expected error for invalid input")
	}
	
	_, err = ParseDurationString("5x")
	if err == nil {
		t.Error("expected error for unknown unit")
	}
}

func TestCountdownToNewYear(t *testing.T) {
	c := CountdownToNewYear()
	
	if c.Target.Month() != time.January || c.Target.Day() != 1 {
		t.Error("target should be January 1st")
	}
	if c.Target.Year() <= time.Now().Year() {
		t.Error("target should be in the future")
	}
}

func TestCountdownProgress(t *testing.T) {
	// Create a countdown with a short duration
	target := time.Now().Add(1 * time.Second)
	c := NewCountdown(target)
	
	// Progress should be between 0 and 1
	progress := c.Progress()
	if progress < 0 || progress > 1 {
		t.Errorf("progress should be between 0 and 1, got %f", progress)
	}
}

func TestFormatCountdown(t *testing.T) {
	tests := []struct {
		name     string
		duration time.Duration
	}{
		{"seconds", 45 * time.Second},
		{"minutes", 5 * time.Minute},
		{"hours", 3 * time.Hour},
		{"days", 2 * 24 * time.Hour},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := FormatCountdown(tt.duration)
			if result == "" {
				t.Error("result should not be empty")
			}
		})
	}
}

func TestDaysUntilAndSince(t *testing.T) {
	// Test DaysUntil
	future := time.Now().Add(48 * time.Hour)
	days := DaysUntil(future)
	if days != 2 && days != 3 { // Could be 2 or 3 depending on current time
		t.Errorf("unexpected days until: %d", days)
	}
	
	// Test DaysSince
	past := time.Now().Add(-48 * time.Hour)
	days = DaysSince(past)
	if days != 1 && days != 2 { // Could be 1 or 2 depending on current time
		t.Errorf("unexpected days since: %d", days)
	}
}

func TestDurationFormatLong(t *testing.T) {
	d := ParseDuration(1*24*time.Hour + 2*time.Hour + 30*time.Minute + 45*time.Second)
	result := d.FormatLong()
	
	if result == "" {
		t.Error("result should not be empty")
	}
	// Should contain the words "day", "hour", "minute", "second"
	if len(result) < 30 {
		t.Errorf("long format should be descriptive, got: %s", result)
	}
}

func TestTimerGetRemaining(t *testing.T) {
	timer := NewTimer(1 * time.Second)
	timer.Start()
	
	remaining := timer.GetRemaining()
	if remaining > 1*time.Second || remaining <= 0 {
		t.Errorf("unexpected remaining time: %v", remaining)
	}
}

func TestCountdownTo(t *testing.T) {
	c := CountdownTo(2025, time.January, 1, 0, 0, 0, time.UTC)
	
	if c.Target.Year() != 2025 {
		t.Errorf("expected year 2025, got %d", c.Target.Year())
	}
	if c.Target.Month() != time.January {
		t.Errorf("expected month January, got %d", c.Target.Month())
	}
	if c.Target.Day() != 1 {
		t.Errorf("expected day 1, got %d", c.Target.Day())
	}
}

func TestDurationFormatDigital(t *testing.T) {
	d := ParseDuration(2*time.Hour + 30*time.Minute + 45*time.Second)
	result := d.FormatDigital()
	expected := "02:30:45"
	
	if result != expected {
		t.Errorf("expected %q, got %q", expected, result)
	}
}