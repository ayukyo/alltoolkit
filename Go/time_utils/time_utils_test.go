package time_utils

import (
	"testing"
	"time"
)

func TestParse(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		wantErr bool
	}{
		{"RFC3339", "2024-01-15T10:30:00Z", false},
		{"DateTime", "2024-01-15 10:30:00", false},
		{"DateOnly", "2024-01-15", false},
		{"Invalid", "not-a-date", true},
		{"Empty", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := Parse(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("Parse(%s) error = %v, wantErr %v", tt.input, err, tt.wantErr)
			}
		})
	}
}

func TestParseUnix(t *testing.T) {
	// Test seconds
	t1, err := ParseUnix(int64(1705315800))
	if err != nil {
		t.Errorf("ParseUnix(seconds) error: %v", err)
	}
	if t1.Year() != 2024 {
		t.Errorf("ParseUnix(seconds) year = %d, want 2024", t1.Year())
	}

	// Test milliseconds
	t2, err := ParseUnix(int64(1705315800000))
	if err != nil {
		t.Errorf("ParseUnix(milliseconds) error: %v", err)
	}
	if t2.Year() != 2024 {
		t.Errorf("ParseUnix(milliseconds) year = %d, want 2024", t2.Year())
	}

	// Test string
	t3, err := ParseUnix("1705315800")
	if err != nil {
		t.Errorf("ParseUnix(string) error: %v", err)
	}
	if t3.Year() != 2024 {
		t.Errorf("ParseUnix(string) year = %d, want 2024", t3.Year())
	}
}

func TestParseDuration(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected time.Duration
	}{
		{"Seconds", "30s", 30 * time.Second},
		{"Minutes", "5m", 5 * time.Minute},
		{"Hours", "2h", 2 * time.Hour},
		{"Days", "1d", 24 * time.Hour},
		{"Combined", "1d2h30m", 26*time.Hour + 30*time.Minute},
		{"Spaces", "1d 2h 30m", 26*time.Hour + 30*time.Minute},
		{"Milliseconds", "500ms", 500 * time.Millisecond},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseDuration(tt.input)
			if err != nil {
				t.Errorf("ParseDuration(%s) error: %v", tt.input, err)
				return
			}
			if got != tt.expected {
				t.Errorf("ParseDuration(%s) = %v, want %v", tt.input, got, tt.expected)
			}
		})
	}
}

func TestFormatFunctions(t *testing.T) {
	now := time.Date(2024, 1, 15, 10, 30, 45, 0, time.UTC)

	if got := FormatDate(now); got != "2024-01-15" {
		t.Errorf("FormatDate() = %s, want 2024-01-15", got)
	}

	if got := FormatTime(now); got != "10:30:45" {
		t.Errorf("FormatTime() = %s, want 10:30:45", got)
	}

	if got := FormatDateTime(now); got != "2024-01-15 10:30:45" {
		t.Errorf("FormatDateTime() = %s, want 2024-01-15 10:30:45", got)
	}

	if got := FormatUnixTimestamp(now); got != now.Unix() {
		t.Errorf("FormatUnixTimestamp() = %d, want %d", got, now.Unix())
	}
}

func TestFormatHumanDuration(t *testing.T) {
	tests := []struct {
		input    time.Duration
		expected string
	}{
		{500 * time.Millisecond, "500ms"},
		{5 * time.Second, "5.0s"},
		{90 * time.Second, "1.5m"},
		{2 * time.Hour, "2.0h"},
		{26 * time.Hour, "1d 2h"},
		{48 * time.Hour, "2d"},
	}

	for _, tt := range tests {
		got := FormatHumanDuration(tt.input)
		if got != tt.expected {
			t.Errorf("FormatHumanDuration(%v) = %s, want %s", tt.input, got, tt.expected)
		}
	}
}

func TestAddFunctions(t *testing.T) {
	base := time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC)

	// AddDays
	got := AddDays(base, 5)
	expected := time.Date(2024, 1, 20, 10, 30, 0, 0, time.UTC)
	if !got.Equal(expected) {
		t.Errorf("AddDays() = %v, want %v", got, expected)
	}

	// AddMonths
	got = AddMonths(base, 2)
	expected = time.Date(2024, 3, 15, 10, 30, 0, 0, time.UTC)
	if !got.Equal(expected) {
		t.Errorf("AddMonths() = %v, want %v", got, expected)
	}

	// AddYears
	got = AddYears(base, 1)
	expected = time.Date(2025, 1, 15, 10, 30, 0, 0, time.UTC)
	if !got.Equal(expected) {
		t.Errorf("AddYears() = %v, want %v", got, expected)
	}
}

func TestStartEndOfDay(t *testing.T) {
	base := time.Date(2024, 1, 15, 10, 30, 45, 123, time.UTC)

	start := StartOfDay(base)
	expectedStart := time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC)
	if !start.Equal(expectedStart) {
		t.Errorf("StartOfDay() = %v, want %v", start, expectedStart)
	}

	end := EndOfDay(base)
	expectedEnd := time.Date(2024, 1, 15, 23, 59, 59, 999999999, time.UTC)
	if !end.Equal(expectedEnd) {
		t.Errorf("EndOfDay() = %v, want %v", end, expectedEnd)
	}
}

func TestStartEndOfMonth(t *testing.T) {
	base := time.Date(2024, 2, 15, 10, 30, 0, 0, time.UTC)

	start := StartOfMonth(base)
	expectedStart := time.Date(2024, 2, 1, 0, 0, 0, 0, time.UTC)
	if !start.Equal(expectedStart) {
		t.Errorf("StartOfMonth() = %v, want %v", start, expectedStart)
	}

	end := EndOfMonth(base)
	expectedEnd := time.Date(2024, 2, 29, 23, 59, 59, 999999999, time.UTC) // 2024 is leap year
	if !end.Equal(expectedEnd) {
		t.Errorf("EndOfMonth() = %v, want %v", end, expectedEnd)
	}
}

func TestStartEndOfWeek(t *testing.T) {
	// Wednesday, Jan 17, 2024
	base := time.Date(2024, 1, 17, 10, 30, 0, 0, time.UTC)

	start := StartOfWeek(base)
	// Monday, Jan 15, 2024
	expectedStart := time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC)
	if !start.Equal(expectedStart) {
		t.Errorf("StartOfWeek() = %v, want %v", start, expectedStart)
	}

	end := EndOfWeek(base)
	// Sunday, Jan 21, 2024
	expectedEnd := time.Date(2024, 1, 21, 23, 59, 59, 999999999, time.UTC)
	if !end.Equal(expectedEnd) {
		t.Errorf("EndOfWeek() = %v, want %v", end, expectedEnd)
	}
}

func TestComparisonFunctions(t *testing.T) {
	t1 := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	t2 := time.Date(2024, 1, 15, 12, 0, 0, 0, time.UTC)

	if !IsBefore(t1, t2) {
		t.Error("IsBefore() should be true")
	}

	if !IsAfter(t2, t1) {
		t.Error("IsAfter() should be true")
	}

	if !IsSameDay(t1, t2) {
		t.Error("IsSameDay() should be true")
	}

	// Test IsWeekend
	weekday := time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC) // Monday
	if IsWeekend(weekday) {
		t.Error("IsWeekend(Monday) should be false")
	}

	weekend := time.Date(2024, 1, 20, 0, 0, 0, 0, time.UTC) // Saturday
	if !IsWeekend(weekend) {
		t.Error("IsWeekend(Saturday) should be true")
	}
}

func TestLeapYear(t *testing.T) {
	if !IsLeapYear(2024) {
		t.Error("2024 should be a leap year")
	}

	if IsLeapYear(2023) {
		t.Error("2023 should not be a leap year")
	}

	if !IsLeapYear(2000) {
		t.Error("2000 should be a leap year (divisible by 400)")
	}

	if IsLeapYear(1900) {
		t.Error("1900 should not be a leap year (divisible by 100 but not 400)")
	}
}

func TestDaysInMonth(t *testing.T) {
	if got := DaysInMonth(2024, time.January); got != 31 {
		t.Errorf("DaysInMonth(January) = %d, want 31", got)
	}

	if got := DaysInMonth(2024, time.February); got != 29 {
		t.Errorf("DaysInMonth(February 2024) = %d, want 29", got)
	}

	if got := DaysInMonth(2023, time.February); got != 28 {
		t.Errorf("DaysInMonth(February 2023) = %d, want 28", got)
	}

	if got := DaysInMonth(2024, time.April); got != 30 {
		t.Errorf("DaysInMonth(April) = %d, want 30", got)
	}
}

func TestDiffFunctions(t *testing.T) {
	t1 := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	t2 := time.Date(2024, 1, 17, 14, 30, 0, 0, time.UTC)

	if got := DiffInDays(t1, t2); got != 2 {
		t.Errorf("DiffInDays() = %d, want 2", got)
	}

	hours := DiffInHours(t1, t2)
	expectedHours := 52.5
	if hours != expectedHours {
		t.Errorf("DiffInHours() = %f, want %f", hours, expectedHours)
	}

	detailed := DiffDetailed(t1, t2)
	if detailed.Days != 2 || detailed.Hours != 4 || detailed.Minutes != 30 {
		t.Errorf("DiffDetailed() = %+v, want Days=2, Hours=4, Minutes=30", detailed)
	}
}

func TestTimeRange(t *testing.T) {
	start := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	end := time.Date(2024, 1, 15, 12, 0, 0, 0, time.UTC)

	tr, err := NewTimeRange(start, end)
	if err != nil {
		t.Errorf("NewTimeRange() error: %v", err)
		return
	}

	// Test Duration
	if tr.Duration() != 2*time.Hour {
		t.Errorf("Duration() = %v, want 2h", tr.Duration())
	}

	// Test Contains
	inside := time.Date(2024, 1, 15, 11, 0, 0, 0, time.UTC)
	if !tr.Contains(inside) {
		t.Error("Contains() should be true for time inside range")
	}

	outside := time.Date(2024, 1, 15, 13, 0, 0, 0, time.UTC)
	if tr.Contains(outside) {
		t.Error("Contains() should be false for time outside range")
	}

	// Test Overlaps
	otherStart := time.Date(2024, 1, 15, 11, 0, 0, 0, time.UTC)
	otherEnd := time.Date(2024, 1, 15, 13, 0, 0, 0, time.UTC)
	other, _ := NewTimeRange(otherStart, otherEnd)
	if !tr.Overlaps(other) {
		t.Error("Overlaps() should be true")
	}

	// Test invalid range
	_, err = NewTimeRange(end, start)
	if err != ErrInvalidRange {
		t.Error("NewTimeRange should return ErrInvalidRange for end before start")
	}
}

func TestTimeRangeSplit(t *testing.T) {
	start := time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 1, 15, 6, 0, 0, 0, time.UTC)

	tr, _ := NewTimeRange(start, end)
	points := tr.Split(time.Hour)

	if len(points) != 7 { // 0, 1, 2, 3, 4, 5, 6
		t.Errorf("Split() returned %d points, want 7", len(points))
	}
}

func TestStopwatch(t *testing.T) {
	sw := NewStopwatch()
	
	// Initially stopped
	if sw.running {
		t.Error("Stopwatch should not be running initially")
	}

	sw.Start()
	if !sw.running {
		t.Error("Stopwatch should be running after Start()")
	}

	sw.Stop()
	if sw.running {
		t.Error("Stopwatch should not be running after Stop()")
	}

	elapsed := sw.Elapsed()
	if elapsed <= 0 {
		t.Error("Elapsed() should be positive after Start/Stop")
	}

	sw.Reset()
	if sw.elapsed != 0 {
		t.Error("Reset() should set elapsed to 0")
	}
}

func TestCountdown(t *testing.T) {
	// Test countdown to a specific duration
	cd := NewCountdown(2 * time.Hour)

	if cd.IsExpired() {
		t.Error("Countdown should not be expired initially")
	}

	remaining := cd.Remaining()
	if remaining <= 0 || remaining > 2*time.Hour {
		t.Errorf("Remaining() = %v, want between 0 and 2h", remaining)
	}

	// Test progress
	progress := cd.Progress(2 * time.Hour)
	if progress < 0 || progress > 1 {
		t.Errorf("Progress() = %f, want between 0 and 1", progress)
	}
}

func TestNextWeekday(t *testing.T) {
	// Wednesday, Jan 17, 2024
	base := time.Date(2024, 1, 17, 10, 0, 0, 0, time.UTC)

	// Next Monday should be Jan 22
	nextMonday := NextWeekday(base, time.Monday)
	expected := time.Date(2024, 1, 22, 10, 0, 0, 0, time.UTC)
	if !nextMonday.Equal(expected) {
		t.Errorf("NextWeekday(Monday) = %v, want %v", nextMonday, expected)
	}

	// Next Friday should be Jan 19
	nextFriday := NextWeekday(base, time.Friday)
	expected = time.Date(2024, 1, 19, 10, 0, 0, 0, time.UTC)
	if !nextFriday.Equal(expected) {
		t.Errorf("NextWeekday(Friday) = %v, want %v", nextFriday, expected)
	}
}

func TestPreviousWeekday(t *testing.T) {
	// Wednesday, Jan 17, 2024
	base := time.Date(2024, 1, 17, 10, 0, 0, 0, time.UTC)

	// Previous Monday should be Jan 15
	prevMonday := PreviousWeekday(base, time.Monday)
	expected := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	if !prevMonday.Equal(expected) {
		t.Errorf("PreviousWeekday(Monday) = %v, want %v", prevMonday, expected)
	}
}

func TestNextNthWeekday(t *testing.T) {
	// 2nd Tuesday of January 2024 should be Jan 9
	tuesday := NextNthWeekday(2024, time.January, time.Tuesday, 2)
	expected := time.Date(2024, 1, 9, 0, 0, 0, 0, time.UTC)
	if !tuesday.Equal(expected) {
		t.Errorf("NextNthWeekday(2nd Tuesday) = %v, want %v", tuesday, expected)
	}

	// 3rd Friday of January 2024 should be Jan 19
	friday := NextNthWeekday(2024, time.January, time.Friday, 3)
	expected = time.Date(2024, 1, 19, 0, 0, 0, 0, time.UTC)
	if !friday.Equal(expected) {
		t.Errorf("NextNthWeekday(3rd Friday) = %v, want %v", friday, expected)
	}
}

func TestLastNthWeekday(t *testing.T) {
	// Last Friday of January 2024 should be Jan 26
	friday := LastNthWeekday(2024, time.January, time.Friday)
	expected := time.Date(2024, 1, 26, 0, 0, 0, 0, time.UTC)
	if !friday.Equal(expected) {
		t.Errorf("LastNthWeekday(Friday) = %v, want %v", friday, expected)
	}
}

func TestAge(t *testing.T) {
	// Test cases would need to mock time.Now() which is tricky
	// Here we just test that Age returns a reasonable value
	birthday := time.Date(1990, 1, 15, 0, 0, 0, 0, time.UTC)
	age := Age(birthday)
	if age < 0 || age > 150 {
		t.Errorf("Age() = %d, seems unreasonable", age)
	}
}

func TestAgeDetailed(t *testing.T) {
	// Birthday: Jan 15, 2020
	// Now (approximate): Jan 2024
	birthday := time.Date(2020, 1, 15, 0, 0, 0, 0, time.UTC)
	years, months, days := AgeDetailed(birthday)

	// Just verify reasonable values
	if years < 0 || years > 10 {
		t.Errorf("AgeDetailed() years = %d, seems unreasonable", years)
	}
	if months < 0 || months > 11 {
		t.Errorf("AgeDetailed() months = %d, seems unreasonable", months)
	}
	if days < 0 || days > 31 {
		t.Errorf("AgeDetailed() days = %d, seems unreasonable", days)
	}
}

func TestSortTimes(t *testing.T) {
	t1 := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	t2 := time.Date(2024, 1, 10, 10, 0, 0, 0, time.UTC)
	t3 := time.Date(2024, 1, 20, 10, 0, 0, 0, time.UTC)

	sorted := SortTimes([]time.Time{t1, t2, t3})

	if !sorted[0].Equal(t2) || !sorted[1].Equal(t1) || !sorted[2].Equal(t3) {
		t.Errorf("SortTimes() = %v, want [%v, %v, %v]", sorted, t2, t1, t3)
	}
}

func TestMinMax(t *testing.T) {
	t1 := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	t2 := time.Date(2024, 1, 10, 10, 0, 0, 0, time.UTC)
	t3 := time.Date(2024, 1, 20, 10, 0, 0, 0, time.UTC)

	minTime := Min(t1, t2, t3)
	if !minTime.Equal(t2) {
		t.Errorf("Min() = %v, want %v", minTime, t2)
	}

	maxTime := Max(t1, t2, t3)
	if !maxTime.Equal(t3) {
		t.Errorf("Max() = %v, want %v", maxTime, t3)
	}
}

func TestClamp(t *testing.T) {
	min := time.Date(2024, 1, 10, 0, 0, 0, 0, time.UTC)
	max := time.Date(2024, 1, 20, 0, 0, 0, 0, time.UTC)

	// Below min
	below := time.Date(2024, 1, 5, 0, 0, 0, 0, time.UTC)
	clamped := Clamp(below, min, max)
	if !clamped.Equal(min) {
		t.Errorf("Clamp(below) = %v, want %v", clamped, min)
	}

	// Above max
	above := time.Date(2024, 1, 25, 0, 0, 0, 0, time.UTC)
	clamped = Clamp(above, min, max)
	if !clamped.Equal(max) {
		t.Errorf("Clamp(above) = %v, want %v", clamped, max)
	}

	// Within range
	within := time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC)
	clamped = Clamp(within, min, max)
	if !clamped.Equal(within) {
		t.Errorf("Clamp(within) = %v, want %v", clamped, within)
	}
}

func TestTimezoneConversion(t *testing.T) {
	// Test ToUTC
	local := time.Date(2024, 1, 15, 10, 0, 0, 0, time.Local)
	utc := ToUTC(local)
	if utc.Location() != time.UTC {
		t.Error("ToUTC() should return UTC time")
	}

	// Test Location
	loc, err := Location("America/New_York")
	if err != nil {
		t.Errorf("Location() error: %v", err)
	}
	if loc == nil {
		t.Error("Location() should return non-nil location")
	}
}

func TestConversionFunctions(t *testing.T) {
	// Test Unix
	t1 := Unix(1705315800, 0)
	if t1.Year() != 2024 {
		t.Errorf("Unix() year = %d, want 2024", t1.Year())
	}

	// Test UnixMilli
	t2 := UnixMilli(1705315800000)
	if t2.Year() != 2024 {
		t.Errorf("UnixMilli() year = %d, want 2024", t2.Year())
	}
}

// Benchmark tests
func BenchmarkParse(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Parse("2024-01-15T10:30:00Z")
	}
}

func BenchmarkFormatDateTime(b *testing.B) {
	t := time.Date(2024, 1, 15, 10, 30, 45, 0, time.UTC)
	for i := 0; i < b.N; i++ {
		FormatDateTime(t)
	}
}

func BenchmarkStartOfDay(b *testing.B) {
	t := time.Date(2024, 1, 15, 10, 30, 45, 123, time.UTC)
	for i := 0; i < b.N; i++ {
		StartOfDay(t)
	}
}

func BenchmarkDiffDetailed(b *testing.B) {
	t1 := time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC)
	t2 := time.Date(2024, 1, 17, 14, 30, 0, 0, time.UTC)
	for i := 0; i < b.N; i++ {
		DiffDetailed(t1, t2)
	}
}

func BenchmarkStopwatchElapsed(b *testing.B) {
	sw := NewStopwatch().Start()
	for i := 0; i < b.N; i++ {
		sw.Elapsed()
	}
}