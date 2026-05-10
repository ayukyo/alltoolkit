package biorhythm_utils

import (
	"math"
	"testing"
	"time"
)

func TestParseBirthDate(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
		hasError bool
	}{
		{"ISO format", "1990-05-15", "1990-05-15", false},
		{"US format with slashes", "05/15/1990", "1990-05-15", false},
		{"EU format with dashes", "15-05-1990", "1990-05-15", false},
		{"Month name format", "May 15, 1990", "1990-05-15", false},
		{"Full month name", "May 15, 1990", "1990-05-15", false},
		{"Invalid format", "not-a-date", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ParseBirthDate(tt.input)

			if tt.hasError {
				if err == nil {
					t.Errorf("ParseBirthDate(%q) expected error, got none", tt.input)
				}
				return
			}

			if err != nil {
				t.Errorf("ParseBirthDate(%q) unexpected error: %v", tt.input, err)
				return
			}

			expected, _ := time.Parse("2006-01-02", tt.expected)
			if !result.Equal(expected) {
				t.Errorf("ParseBirthDate(%q) = %v, want %v", tt.input, result, expected)
			}
		})
	}
}

func TestNewCalculator(t *testing.T) {
	birthDate := time.Date(1990, 5, 15, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	if !calc.birthDate.Equal(birthDate) {
		t.Errorf("NewCalculator birthDate mismatch")
	}
}

func TestCalculate(t *testing.T) {
	// Born on Jan 1, 2000, test on Jan 1, 2000 (day 0)
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	// Day 0 should be at 0 for all cycles (sin(0) = 0)
	result := calc.Calculate(birthDate)

	if result.DaysLived != 0 {
		t.Errorf("DaysLived = %d, want 0", result.DaysLived)
	}

	if math.Abs(result.Physical) > 0.01 {
		t.Errorf("Physical at day 0 should be ~0, got %.2f", result.Physical)
	}
}

func TestCalculateCycleValues(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	// Test at quarter cycle (should be at peak = 100)
	// Physical: 23 days, quarter = 5.75 ≈ 6 days
	physicalPeakDate := birthDate.AddDate(0, 0, 6)
	result := calc.Calculate(physicalPeakDate)

	// At ~25% of cycle, sin should be close to 1
	expectedPeak := math.Sin(2*math.Pi*6/23) * 100
	if math.Abs(result.Physical-expectedPeak) > 1 {
		t.Errorf("Physical at day 6 = %.2f, want ~%.2f", result.Physical, expectedPeak)
	}
}

func TestCalculateToday(t *testing.T) {
	birthDate := time.Date(1990, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	result := calc.CalculateToday()

	if result.Date.Year() != time.Now().Year() {
		t.Errorf("CalculateToday year mismatch")
	}

	// Values should be between -100 and 100
	if result.Physical < -100 || result.Physical > 100 {
		t.Errorf("Physical = %.2f, should be in range [-100, 100]", result.Physical)
	}
	if result.Emotional < -100 || result.Emotional > 100 {
		t.Errorf("Emotional = %.2f, should be in range [-100, 100]", result.Emotional)
	}
	if result.Intellectual < -100 || result.Intellectual > 100 {
		t.Errorf("Intellectual = %.2f, should be in range [-100, 100]", result.Intellectual)
	}
}

func TestCalculateRange(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 1, 7, 0, 0, 0, 0, time.UTC)

	results := calc.CalculateRange(start, end)

	if len(results) != 7 {
		t.Errorf("CalculateRange returned %d results, want 7", len(results))
	}

	// Verify dates are correct
	for i, r := range results {
		expected := start.AddDate(0, 0, i)
		if !r.Date.Equal(expected) {
			t.Errorf("Result[%d].Date = %v, want %v", i, r.Date, expected)
		}
	}
}

func TestCalculateForDays(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	results := calc.CalculateForDays(start, 5)

	if len(results) != 5 {
		t.Errorf("CalculateForDays returned %d results, want 5", len(results))
	}
}

func TestGetPhases(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	phases := calc.GetPhases(birthDate)

	if len(phases) != 4 {
		t.Errorf("GetPhases returned %d phases, want 4", len(phases))
	}

	// Check that phase names are valid
	validPhases := map[string]bool{"high": true, "low": true, "rising": true, "falling": true}
	for _, p := range phases {
		if !validPhases[p.PhaseName] {
			t.Errorf("Invalid phase name: %s", p.PhaseName)
		}
	}
}

func TestFindCriticalDays(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	// Look for critical days in a month range
	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 1, 31, 0, 0, 0, 0, time.UTC)

	criticalDays := calc.FindCriticalDays(start, end)

	// Should find at least some critical days in a month
	if len(criticalDays) == 0 {
		t.Log("No critical days found (possible but unusual)")
	}

	// Verify all critical days are within range
	for _, cd := range criticalDays {
		if cd.Date.Before(start) || cd.Date.After(end) {
			t.Errorf("Critical day %v outside range [%v, %v]", cd.Date, start, end)
		}
	}
}

func TestFindHighDays(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 3, 31, 0, 0, 0, 0, time.UTC)

	highDays := calc.FindHighDays(start, end, 80)

	// All high days should have values >= threshold
	for _, d := range highDays {
		if d.Physical < 80 || d.Emotional < 80 || d.Intellectual < 80 {
			t.Errorf("High day found with value < 80: P=%.2f E=%.2f I=%.2f",
				d.Physical, d.Emotional, d.Intellectual)
		}
	}
}

func TestFindLowDays(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 3, 31, 0, 0, 0, 0, time.UTC)

	lowDays := calc.FindLowDays(start, end, -80)

	// All low days should have at least one value <= threshold
	for _, d := range lowDays {
		if d.Physical > -80 && d.Emotional > -80 && d.Intellectual > -80 {
			t.Errorf("Low day found with all values > -80: P=%.2f E=%.2f I=%.2f",
				d.Physical, d.Emotional, d.Intellectual)
		}
	}
}

func TestGetOverallScore(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	score := calc.GetOverallScore(birthDate)

	// Day 0 should have overall score close to 0
	if math.Abs(score) > 0.1 {
		t.Errorf("Overall score at day 0 = %.2f, want ~0", score)
	}
}

func TestGetCompatibilityScore(t *testing.T) {
	birthDate1 := time.Date(1990, 1, 1, 0, 0, 0, 0, time.UTC)
	birthDate2 := time.Date(1990, 1, 2, 0, 0, 0, 0, time.UTC)

	score := GetCompatibilityScore(birthDate1, birthDate2)

	// Score should be between 0 and 100
	if score < 0 || score > 100 {
		t.Errorf("Compatibility score = %.2f, should be in [0, 100]", score)
	}

	// Same birth date should have high compatibility
	sameScore := GetCompatibilityScore(birthDate1, birthDate1)
	if sameScore != 100 {
		t.Errorf("Same birth date compatibility = %.2f, want 100", sameScore)
	}
}

func TestPredictNextPeak(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	fromDate := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	nextPeak := calc.PredictNextPeak(PhysicalCycleDays, fromDate)

	// Next peak should be after from date
	if !nextPeak.After(fromDate) {
		t.Errorf("Next peak %v should be after %v", nextPeak, fromDate)
	}

	// Verify it's actually near a peak
	result := calc.Calculate(nextPeak)
	if result.Physical < 95 {
		t.Errorf("Predicted peak has Physical = %.2f, expected >= 95", result.Physical)
	}
}

func TestPredictNextTrough(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	fromDate := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	nextTrough := calc.PredictNextTrough(PhysicalCycleDays, fromDate)

	// Next trough should be after from date
	if !nextTrough.After(fromDate) {
		t.Errorf("Next trough %v should be after %v", nextTrough, fromDate)
	}

	// Verify it's actually near a trough
	result := calc.Calculate(nextTrough)
	if result.Physical > -95 {
		t.Errorf("Predicted trough has Physical = %.2f, expected <= -95", result.Physical)
	}
}

func TestPredictNextCritical(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	fromDate := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	nextCritical := calc.PredictNextCritical(PhysicalCycleDays, fromDate)

	// Next critical should be on or after from date
	if nextCritical.Before(fromDate) {
		t.Errorf("Next critical %v should be on or after %v", nextCritical, fromDate)
	}

	// Verify it's actually near zero
	// Critical days are at day 0 and day cycle/2 of each cycle
	// Physical cycle is 23 days, so half is 11.5 days - integer truncation may cause small deviation
	result := calc.Calculate(nextCritical)
	if math.Abs(result.Physical) > 15 {
		t.Errorf("Predicted critical has Physical = %.2f, expected near 0 (within 15)", result.Physical)
	}
}

func TestFormatBiorhythm(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	result := calc.Calculate(birthDate)
	formatted := FormatBiorhythm(result)

	// Check that formatted string contains expected elements
	if len(formatted) == 0 {
		t.Error("FormatBiorhythm returned empty string")
	}

	// Should contain cycle names
	checks := []string{"Physical", "Emotional", "Intellectual", "Intuitive", "Overall"}
	for _, check := range checks {
		if !contains(formatted, check) {
			t.Errorf("FormatBiorhythm missing %s", check)
		}
	}
}

func TestGetRecommendation(t *testing.T) {
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	// Test with various dates
	tests := []struct {
		name string
		date time.Time
	}{
		{"Birth day", birthDate},
		{"Today", time.Now()},
		{"Future", birthDate.AddDate(25, 0, 0)},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			bio := calc.Calculate(tt.date)
			recs := GetRecommendation(bio)

			// Should have at least some recommendations
			if len(recs) == 0 {
				t.Log("No recommendations (possible but unusual)")
			}
		})
	}
}

func TestDaysBetween(t *testing.T) {
	tests := []struct {
		name     string
		start    time.Time
		end      time.Time
		expected int
	}{
		{"Same day", time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC), time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC), 0},
		{"One day", time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC), time.Date(2024, 1, 2, 0, 0, 0, 0, time.UTC), 1},
		{"One week", time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC), time.Date(2024, 1, 8, 0, 0, 0, 0, time.UTC), 7},
		{"One month", time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC), time.Date(2024, 2, 1, 0, 0, 0, 0, time.UTC), 31},
		{"Negative", time.Date(2024, 1, 2, 0, 0, 0, 0, time.UTC), time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC), -1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := daysBetween(tt.start, tt.end)
			if result != tt.expected {
				t.Errorf("daysBetween(%v, %v) = %d, want %d", tt.start, tt.end, result, tt.expected)
			}
		})
	}
}

func TestCycleConsistency(t *testing.T) {
	// Test that cycles are consistent (same day offset should produce same relative values)
	birthDate := time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)

	// Calculate for day 100
	day100 := birthDate.AddDate(0, 0, 100)
	bio100 := calc.Calculate(day100)

	// Calculate for day 100 + cycle length (should be same for that cycle)
	day123 := birthDate.AddDate(0, 0, 100+PhysicalCycleDays)
	bio123 := calc.Calculate(day123)

	// Physical should be the same (23-day cycle)
	if math.Abs(bio100.Physical-bio123.Physical) > 0.01 {
		t.Errorf("Physical cycle inconsistent: day 100 = %.4f, day 123 = %.4f",
			bio100.Physical, bio123.Physical)
	}
}

// Benchmark tests
func BenchmarkCalculate(b *testing.B) {
	birthDate := time.Date(1990, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)
	date := time.Now()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calc.Calculate(date)
	}
}

func BenchmarkCalculateRange(b *testing.B) {
	birthDate := time.Date(1990, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)
	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calc.CalculateRange(start, end)
	}
}

func BenchmarkFindCriticalDays(b *testing.B) {
	birthDate := time.Date(1990, 1, 1, 0, 0, 0, 0, time.UTC)
	calc := NewCalculator(birthDate)
	start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2024, 1, 31, 0, 0, 0, 0, time.UTC)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calc.FindCriticalDays(start, end)
	}
}

// Helper function
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > len(substr) &&
		(s[:len(substr)] == substr || s[len(s)-len(substr):] == substr ||
			findSubstring(s, substr)))
}

func findSubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}