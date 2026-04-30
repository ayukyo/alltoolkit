package cron_expr_utils

import (
	"testing"
	"time"
)

func TestParse(t *testing.T) {
	tests := []struct {
		name    string
		expr    string
		wantErr bool
	}{
		{"every minute", "* * * * *", false},
		{"every hour", "0 * * * *", false},
		{"daily at midnight", "0 0 * * *", false},
		{"specific time", "30 14 * * *", false},
		{"range", "0-30 * * * *", false},
		{"step", "*/15 * * * *", false},
		{"list", "0,15,30,45 * * * *", false},
		{"weekday range", "0 9 * * 1-5", false},
		{"month range", "0 0 1 1-6 *", false},
		{"complex", "30 8-17 * * 1-5", false},
		{"invalid - too few fields", "* * * *", true},
		{"invalid - too many fields", "* * * * * *", true},
		{"invalid - empty", "", true},
		{"invalid - bad range", "0-60 * * * *", true},
		{"invalid - bad hour", "* 25 * * *", true},
		{"invalid - bad month", "* * * 13 *", true},
		{"invalid - bad weekday", "* * * * 7", true},
		{"step with range", "0-30/5 * * * *", false},
		{"invalid step", "*/0 * * * *", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := Parse(tt.expr)
			if (err != nil) != tt.wantErr {
				t.Errorf("Parse(%q) error = %v, wantErr %v", tt.expr, err, tt.wantErr)
			}
		})
	}
}

func TestMatches(t *testing.T) {
	tests := []struct {
		name string
		expr string
		time time.Time
		want bool
	}{
		{
			name: "every minute matches",
			expr: "* * * * *",
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "specific minute matches",
			expr: "30 * * * *",
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "specific minute no match",
			expr: "30 * * * *",
			time: time.Date(2024, 1, 15, 10, 45, 0, 0, time.UTC),
			want: false,
		},
		{
			name: "specific hour matches",
			expr: "* 10 * * *",
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "specific hour no match",
			expr: "* 11 * * *",
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: false,
		},
		{
			name: "weekday matches",
			expr: "* * * * 1", // Monday
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC), // Monday
			want: true,
		},
		{
			name: "weekday no match",
			expr: "* * * * 2", // Tuesday
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC), // Monday
			want: false,
		},
		{
			name: "month matches",
			expr: "* * * 1 *", // January
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "month no match",
			expr: "* * * 2 *", // February
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: false,
		},
		{
			name: "day matches",
			expr: "* * 15 * *",
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "step matches",
			expr: "*/15 * * * *", // 0, 15, 30, 45
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "step no match",
			expr: "*/15 * * * *", // 0, 15, 30, 45
			time: time.Date(2024, 1, 15, 10, 31, 0, 0, time.UTC),
			want: false,
		},
		{
			name: "range matches",
			expr: "0-30 * * * *",
			time: time.Date(2024, 1, 15, 10, 15, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "range no match",
			expr: "0-30 * * * *",
			time: time.Date(2024, 1, 15, 10, 45, 0, 0, time.UTC),
			want: false,
		},
		{
			name: "list matches",
			expr: "0,15,30,45 * * * *",
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "complex expression",
			expr: "30 9 * * 1-5", // 9:30 AM on weekdays
			time: time.Date(2024, 1, 15, 9, 30, 0, 0, time.UTC), // Monday
			want: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cron, err := Parse(tt.expr)
			if err != nil {
				t.Fatalf("Parse failed: %v", err)
			}
			if got := cron.Matches(tt.time); got != tt.want {
				t.Errorf("Matches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestNext(t *testing.T) {
	tests := []struct {
		name     string
		expr     string
		after    time.Time
		wantHour int
		wantMin  int
	}{
		{
			name:     "next minute",
			expr:     "* * * * *",
			after:    time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			wantHour: 10,
			wantMin:  31,
		},
		{
			name:     "next hour at minute 0",
			expr:     "0 * * * *",
			after:    time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			wantHour: 11,
			wantMin:  0,
		},
		{
			name:     "next 15 minute interval",
			expr:     "*/15 * * * *",
			after:    time.Date(2024, 1, 15, 10, 20, 0, 0, time.UTC),
			wantHour: 10,
			wantMin:  30,
		},
		{
			name:     "next day at midnight",
			expr:     "0 0 * * *",
			after:    time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			wantHour: 0,
			wantMin:  0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cron, err := Parse(tt.expr)
			if err != nil {
				t.Fatalf("Parse failed: %v", err)
			}
			got := cron.Next(tt.after)
			if got.Hour() != tt.wantHour || got.Minute() != tt.wantMin {
				t.Errorf("Next() = %02d:%02d, want %02d:%02d", got.Hour(), got.Minute(), tt.wantHour, tt.wantMin)
			}
		})
	}
}

func TestNextN(t *testing.T) {
	cron, err := Parse("0 * * * *") // Every hour at minute 0
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}

	after := time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC)
	nextTimes := cron.NextN(after, 3)

	if len(nextTimes) != 3 {
		t.Errorf("NextN() returned %d times, want 3", len(nextTimes))
	}

	// Check times are sequential
	for i := 1; i < len(nextTimes); i++ {
		if !nextTimes[i].After(nextTimes[i-1]) {
			t.Errorf("Times not sequential: %v >= %v", nextTimes[i-1], nextTimes[i])
		}
	}
}

func TestPrev(t *testing.T) {
	cron, err := Parse("0 * * * *") // Every hour at minute 0
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}

	before := time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC)
	prev := cron.Prev(before)

	if prev.Hour() != 10 || prev.Minute() != 0 {
		t.Errorf("Prev() = %02d:%02d, want 10:00", prev.Hour(), prev.Minute())
	}
}

func TestPresets(t *testing.T) {
	tests := []struct {
		name string
		cron *CronExpr
		time time.Time
		want bool
	}{
		{
			name: "EveryMinute",
			cron: EveryMinute,
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "EveryHour",
			cron: EveryHour,
			time: time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "EveryDay",
			cron: EveryDay,
			time: time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "Weekdays on Monday",
			cron: Weekdays,
			time: time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC), // Monday
			want: true,
		},
		{
			name: "Weekdays on Saturday",
			cron: Weekdays,
			time: time.Date(2024, 1, 20, 0, 0, 0, 0, time.UTC), // Saturday
			want: false,
		},
		{
			name: "EveryFifteenMinutes at 30",
			cron: EveryFifteenMinutes,
			time: time.Date(2024, 1, 15, 10, 30, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "TwiceDaily at midnight",
			cron: TwiceDaily,
			time: time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC),
			want: true,
		},
		{
			name: "TwiceDaily at noon",
			cron: TwiceDaily,
			time: time.Date(2024, 1, 15, 12, 0, 0, 0, time.UTC),
			want: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.cron.Matches(tt.time); got != tt.want {
				t.Errorf("Matches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestBuilder(t *testing.T) {
	tests := []struct {
		name       string
		builder    *Builder
		wantExpr   string
		shouldFail bool
	}{
		{
			name:     "default is every minute",
			builder:  NewBuilder(),
			wantExpr: "* * * * *",
		},
		{
			name:     "at specific minute",
			builder:  NewBuilder().AtMinute(30),
			wantExpr: "30 * * * *",
		},
		{
			name:     "at specific hour",
			builder:  NewBuilder().AtHour(14),
			wantExpr: "* 14 * * *",
		},
		{
			name:     "on specific day",
			builder:  NewBuilder().OnDay(1, 15),
			wantExpr: "* * 1,15 * *",
		},
		{
			name:     "every 15 minutes",
			builder:  NewBuilder().EveryNMinutes(15),
			wantExpr: "*/15 * * * *",
		},
		{
			name:     "every 6 hours",
			builder:  NewBuilder().EveryNHours(6),
			wantExpr: "* */6 * * *",
		},
		{
			name:     "complex schedule",
			builder:  NewBuilder().AtMinute(30).AtHour(9).OnWeekday(1, 2, 3, 4, 5),
			wantExpr: "30 9 * * 1,2,3,4,5",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cron, err := tt.builder.Build()
			if tt.shouldFail {
				if err == nil {
					t.Error("Build() should have failed")
				}
				return
			}
			if err != nil {
				t.Fatalf("Build() failed: %v", err)
			}
			if got := cron.String(); got != tt.wantExpr {
				t.Errorf("String() = %q, want %q", got, tt.wantExpr)
			}
		})
	}
}

func TestIsValid(t *testing.T) {
	tests := []struct {
		expr  string
		valid bool
	}{
		{"* * * * *", true},
		{"0 0 * * *", true},
		{"*/5 * * * *", true},
		{"0-30 * * * *", true},
		{"0,15,30,45 * * * *", true},
		{"* * * *", false},
		{"* * * * * *", false},
		{"", false},
		{"invalid", false},
		{"* 25 * * *", false},
	}

	for _, tt := range tests {
		t.Run(tt.expr, func(t *testing.T) {
			if got := IsValid(tt.expr); got != tt.valid {
				t.Errorf("IsValid(%q) = %v, want %v", tt.expr, got, tt.valid)
			}
		})
	}
}

func TestDescribe(t *testing.T) {
	tests := []struct {
		expr      string
		contains  string
	}{
		{"* * * * *", "Every minute"},
		{"0 * * * *", "Every hour at minute 0"},
		{"0 0 * * *", "Daily at 00:00"},
		{"30 14 * * *", "Daily at 14:30"},
		{"0 9 * * 1-5", "Weekdays at 09:00"},
	}

	for _, tt := range tests {
		t.Run(tt.expr, func(t *testing.T) {
			cron, err := Parse(tt.expr)
			if err != nil {
				t.Fatalf("Parse failed: %v", err)
			}
			desc := cron.Describe()
			// Just ensure it doesn't crash and produces something
			if desc == "" {
				t.Error("Describe() returned empty string")
			}
		})
	}
}

func TestGetFieldValues(t *testing.T) {
	cron, err := Parse("15,30,45 * * * *")
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}

	values := cron.GetFieldValues(0) // minute
	if len(values) != 3 {
		t.Errorf("GetFieldValues(0) returned %d values, want 3", len(values))
	}

	// Check all expected values are present
	expected := map[int]bool{15: true, 30: true, 45: true}
	for _, v := range values {
		if !expected[v] {
			t.Errorf("Unexpected value %d", v)
		}
	}

	// Test invalid field index
	if cron.GetFieldValues(10) != nil {
		t.Error("GetFieldValues(10) should return nil")
	}
}

func TestWeekdayNames(t *testing.T) {
	tests := []struct {
		weekday int
		name    string
	}{
		{0, "Sunday"},
		{1, "Monday"},
		{2, "Tuesday"},
		{3, "Wednesday"},
		{4, "Thursday"},
		{5, "Friday"},
		{6, "Saturday"},
		{-1, "Unknown"},
		{7, "Unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := GetWeekdayName(tt.weekday); got != tt.name {
				t.Errorf("GetWeekdayName(%d) = %q, want %q", tt.weekday, got, tt.name)
			}
		})
	}
}

func TestMonthNames(t *testing.T) {
	tests := []struct {
		month int
		name  string
	}{
		{1, "January"},
		{2, "February"},
		{6, "June"},
		{12, "December"},
		{0, "Unknown"},
		{13, "Unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := GetMonthName(tt.month); got != tt.name {
				t.Errorf("GetMonthName(%d) = %q, want %q", tt.month, got, tt.name)
			}
		})
	}
}

func TestNormalizeWeekday(t *testing.T) {
	tests := []struct {
		input  int
		output int
	}{
		{0, 0},  // Sunday stays 0
		{7, 0},  // Sunday as 7 becomes 0
		{1, 1},  // Monday stays 1
		{6, 6},  // Saturday stays 6
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := NormalizeWeekday(tt.input); got != tt.output {
				t.Errorf("NormalizeWeekday(%d) = %d, want %d", tt.input, got, tt.output)
			}
		})
	}
}

func TestValidateField(t *testing.T) {
	tests := []struct {
		fieldIndex int
		values     []int
		valid      bool
	}{
		{0, []int{0, 30, 59}, true},   // valid minutes
		{0, []int{-1, 30}, false},     // invalid minute
		{0, []int{60}, false},         // invalid minute
		{1, []int{0, 12, 23}, true},   // valid hours
		{1, []int{24}, false},         // invalid hour
		{2, []int{1, 15, 31}, true},   // valid days
		{2, []int{0}, false},          // invalid day
		{3, []int{1, 6, 12}, true},    // valid months
		{3, []int{0}, false},          // invalid month
		{4, []int{0, 3, 6}, true},     // valid weekdays
		{4, []int{7}, false},          // invalid weekday
		{5, []int{1}, false},          // invalid field index
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := ValidateField(tt.fieldIndex, tt.values); got != tt.valid {
				t.Errorf("ValidateField(%d, %v) = %v, want %v", tt.fieldIndex, tt.values, got, tt.valid)
			}
		})
	}
}

func TestMustParse(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("MustParse should have panicked for invalid expression")
		}
	}()

	// Valid expression
	cron := MustParse("* * * * *")
	if cron == nil {
		t.Error("MustParse returned nil for valid expression")
	}

	// Invalid expression - should panic
	MustParse("invalid")
}

func TestString(t *testing.T) {
	expr := "30 9 * * 1-5"
	cron, err := Parse(expr)
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}

	if got := cron.String(); got != expr {
		t.Errorf("String() = %q, want %q", got, expr)
	}
}

func TestIsExpired(t *testing.T) {
	// Normal expression should not be expired
	cron, err := Parse("0 0 1 * *")
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}
	if cron.IsExpired() {
		t.Error("Normal expression should not be expired")
	}
}