// Package biorhythm_utils provides utilities for calculating biorhythm cycles.
// Biorhythm theory posits that human life is influenced by three rhythmic cycles:
// - Physical cycle: 23 days (strength, coordination, physical well-being)
// - Emotional cycle: 28 days (mood, creativity, emotional sensitivity)
// - Intellectual cycle: 33 days (analytical thinking, memory, concentration)
//
// Each cycle oscillates between -100 and +100, with 0 being a "critical day".
package biorhythm_utils

import (
	"fmt"
	"math"
	"time"
)

// Cycle constants - the number of days for each biorhythm cycle
const (
	PhysicalCycleDays    = 23
	EmotionalCycleDays   = 28
	IntellectualCycleDays = 33
	IntuitiveCycleDays   = 38 // Additional cycle sometimes used
)

// Biorhythm represents the calculated biorhythm values for a specific date
type Biorhythm struct {
	Date         time.Time
	Physical     float64
	Emotional    float64
	Intellectual float64
	Intuitive    float64
	DaysLived    int
}

// CriticalDay represents a day where a cycle crosses zero
type CriticalDay struct {
	Date     time.Time
	Cycle    string
	Type     string // "critical" or "transition"
}

// Phase represents the current phase of a biorhythm cycle
type Phase struct {
	Cycle      string
	DaysIntoCycle int
	TotalDays  int
	Percentage float64
	PhaseName  string // "high", "low", "rising", "falling"
}

// Calculator is the main biorhythm calculator
type Calculator struct {
	birthDate time.Time
}

// NewCalculator creates a new biorhythm calculator for the given birth date
func NewCalculator(birthDate time.Time) *Calculator {
	return &Calculator{birthDate: birthDate}
}

// ParseBirthDate parses a birth date string in various formats
func ParseBirthDate(dateStr string) (time.Time, error) {
	formats := []string{
		"2006-01-02",
		"2006/01/02",
		"01-02-2006",
		"01/02/2006",
		"02-01-2006",
		"02/01/2006",
		"Jan 2, 2006",
		"January 2, 2006",
		"2 Jan 2006",
		"2 January 2006",
	}

	for _, format := range formats {
		if t, err := time.Parse(format, dateStr); err == nil {
			return t, nil
		}
	}

	return time.Time{}, fmt.Errorf("unable to parse date: %s", dateStr)
}

// Calculate computes the biorhythm values for a given date
func (c *Calculator) Calculate(date time.Time) Biorhythm {
	daysLived := daysBetween(c.birthDate, date)

	return Biorhythm{
		Date:         date,
		DaysLived:    daysLived,
		Physical:     calculateCycle(daysLived, PhysicalCycleDays),
		Emotional:    calculateCycle(daysLived, EmotionalCycleDays),
		Intellectual: calculateCycle(daysLived, IntellectualCycleDays),
		Intuitive:    calculateCycle(daysLived, IntuitiveCycleDays),
	}
}

// CalculateToday computes the biorhythm values for today
func (c *Calculator) CalculateToday() Biorhythm {
	return c.Calculate(time.Now())
}

// CalculateRange computes biorhythm values for a range of dates
func (c *Calculator) CalculateRange(startDate, endDate time.Time) []Biorhythm {
	var results []Biorhythm

	for d := startDate; !d.After(endDate); d = d.AddDate(0, 0, 1) {
		results = append(results, c.Calculate(d))
	}

	return results
}

// CalculateForDays computes biorhythm values for N days starting from a date
func (c *Calculator) CalculateForDays(startDate time.Time, days int) []Biorhythm {
	var results []Biorhythm

	for i := 0; i < days; i++ {
		date := startDate.AddDate(0, 0, i)
		results = append(results, c.Calculate(date))
	}

	return results
}

// GetPhases returns the current phase information for all cycles
func (c *Calculator) GetPhases(date time.Time) []Phase {
	daysLived := daysBetween(c.birthDate, date)

	return []Phase{
		getPhase("Physical", daysLived, PhysicalCycleDays),
		getPhase("Emotional", daysLived, EmotionalCycleDays),
		getPhase("Intellectual", daysLived, IntellectualCycleDays),
		getPhase("Intuitive", daysLived, IntuitiveCycleDays),
	}
}

// FindCriticalDays finds all critical days within a date range
func (c *Calculator) FindCriticalDays(startDate, endDate time.Time) []CriticalDay {
	var criticalDays []CriticalDay

	for d := startDate; !d.After(endDate); d = d.AddDate(0, 0, 1) {
		bio := c.Calculate(d)
		prevBio := c.Calculate(d.AddDate(0, 0, -1))

		// Check each cycle for zero crossing
		criticalDays = append(criticalDays, checkCritical(d, "Physical", bio.Physical, prevBio.Physical)...)
		criticalDays = append(criticalDays, checkCritical(d, "Emotional", bio.Emotional, prevBio.Emotional)...)
		criticalDays = append(criticalDays, checkCritical(d, "Intellectual", bio.Intellectual, prevBio.Intellectual)...)
		criticalDays = append(criticalDays, checkCritical(d, "Intuitive", bio.Intellectual, prevBio.Intellectual)...)
	}

	return criticalDays
}

// FindHighDays finds days where all cycles are above a threshold
func (c *Calculator) FindHighDays(startDate, endDate time.Time, threshold float64) []Biorhythm {
	var highDays []Biorhythm

	for d := startDate; !d.After(endDate); d = d.AddDate(0, 0, 1) {
		bio := c.Calculate(d)
		if bio.Physical >= threshold && bio.Emotional >= threshold && bio.Intellectual >= threshold {
			highDays = append(highDays, bio)
		}
	}

	return highDays
}

// FindLowDays finds days where any cycle is below a threshold
func (c *Calculator) FindLowDays(startDate, endDate time.Time, threshold float64) []Biorhythm {
	var lowDays []Biorhythm

	for d := startDate; !d.After(endDate); d = d.AddDate(0, 0, 1) {
		bio := c.Calculate(d)
		if bio.Physical <= threshold || bio.Emotional <= threshold || bio.Intellectual <= threshold {
			lowDays = append(lowDays, bio)
		}
	}

	return lowDays
}

// GetOverallScore computes a weighted average of all cycles
func (c *Calculator) GetOverallScore(date time.Time) float64 {
	bio := c.Calculate(date)

	// Equal weight to primary three cycles
	return (bio.Physical + bio.Emotional + bio.Intellectual) / 3.0
}

// GetCompatibilityScore computes a compatibility score between two people
func GetCompatibilityScore(birthDate1, birthDate2 time.Time) float64 {
	c1 := NewCalculator(birthDate1)
	c2 := NewCalculator(birthDate2)

	bio1 := c1.CalculateToday()
	bio2 := c2.CalculateToday()

	// Calculate phase alignment for each cycle
	physicalDiff := 1.0 - math.Abs(bio1.Physical-bio2.Physical)/200.0
	emotionalDiff := 1.0 - math.Abs(bio1.Emotional-bio2.Emotional)/200.0
	intellectualDiff := 1.0 - math.Abs(bio1.Intellectual-bio2.Intellectual)/200.0

	// Weighted average (emotional is weighted more for relationships)
	return (physicalDiff*0.25 + emotionalDiff*0.4 + intellectualDiff*0.35) * 100
}

// PredictNextPeak predicts the next peak day for a specific cycle
func (c *Calculator) PredictNextPeak(cycleDays int, fromDate time.Time) time.Time {
	daysLived := daysBetween(c.birthDate, fromDate)

	// Calculate position in current cycle
	currentPos := daysLived % cycleDays

	// Days until next peak (peak is at 1/4 of cycle)
	daysToPeak := cycleDays/4 - currentPos
	if daysToPeak <= 0 {
		daysToPeak += cycleDays
	}

	return fromDate.AddDate(0, 0, daysToPeak)
}

// PredictNextTrough predicts the next trough day for a specific cycle
func (c *Calculator) PredictNextTrough(cycleDays int, fromDate time.Time) time.Time {
	daysLived := daysBetween(c.birthDate, fromDate)

	// Calculate position in current cycle
	currentPos := daysLived % cycleDays

	// Days until next trough (trough is at 3/4 of cycle)
	daysToTrough := 3*cycleDays/4 - currentPos
	if daysToTrough <= 0 {
		daysToTrough += cycleDays
	}

	return fromDate.AddDate(0, 0, daysToTrough)
}

// PredictNextCritical predicts the next critical day for a specific cycle
// Critical days occur when the biorhythm value crosses zero (sin = 0)
// This happens at: day 0 (start of cycle) and day cycleDays/2 (middle of cycle)
func (c *Calculator) PredictNextCritical(cycleDays int, fromDate time.Time) time.Time {
	daysLived := daysBetween(c.birthDate, fromDate)

	// Calculate position in current cycle (0 to cycleDays-1)
	currentPos := daysLived % cycleDays
	if currentPos < 0 {
		currentPos += cycleDays
	}

	// Zero crossings happen at:
	// - Day 0 (start of cycle)
	// - Day cycleDays/2 (middle of cycle)
	halfCycle := cycleDays / 2

	// Days until next zero crossing at start of next cycle
	daysToStart := cycleDays - currentPos
	if daysToStart == cycleDays {
		daysToStart = 0 // We're already at start of cycle
	}

	// Days until zero crossing at middle of cycle
	var daysToMiddle int
	if currentPos < halfCycle {
		daysToMiddle = halfCycle - currentPos
	} else {
		daysToMiddle = cycleDays - currentPos + halfCycle
	}

	// Handle edge case where halfCycle equals currentPos
	if currentPos == halfCycle {
		daysToMiddle = 0
	}

	// Return the closest critical day
	if daysToMiddle < daysToStart {
		return fromDate.AddDate(0, 0, daysToMiddle)
	}
	return fromDate.AddDate(0, 0, daysToStart)
}

// FormatBiorhythm creates a formatted string representation
func FormatBiorhythm(bio Biorhythm) string {
	return fmt.Sprintf(
		"Date: %s (Day %d)\n"+
			"  Physical:     %+.1f%% %s\n"+
			"  Emotional:    %+.1f%% %s\n"+
			"  Intellectual: %+.1f%% %s\n"+
			"  Intuitive:    %+.1f%% %s\n"+
			"  Overall:      %+.1f%%",
		bio.Date.Format("2006-01-02"),
		bio.DaysLived,
		bio.Physical, getBar(bio.Physical, 10),
		bio.Emotional, getBar(bio.Emotional, 10),
		bio.Intellectual, getBar(bio.Intellectual, 10),
		bio.Intuitive, getBar(bio.Intuitive, 10),
		(bio.Physical+bio.Emotional+bio.Intellectual)/3,
	)
}

// GetRecommendation returns activity recommendations based on biorhythm values
func GetRecommendation(bio Biorhythm) []string {
	var recommendations []string

	// Physical recommendations
	if bio.Physical >= 50 {
		recommendations = append(recommendations, "Great day for physical activities, sports, and exercise")
	} else if bio.Physical <= -50 {
		recommendations = append(recommendations, "Take it easy physically, rest if needed")
	} else if math.Abs(bio.Physical) < 10 {
		recommendations = append(recommendations, "⚠️ Physical critical day - be cautious with physical activities")
	}

	// Emotional recommendations
	if bio.Emotional >= 50 {
		recommendations = append(recommendations, "Good day for social activities and creative pursuits")
	} else if bio.Emotional <= -50 {
		recommendations = append(recommendations, "May feel emotionally low - practice self-care")
	} else if math.Abs(bio.Emotional) < 10 {
		recommendations = append(recommendations, "⚠️ Emotional critical day - avoid important emotional decisions")
	}

	// Intellectual recommendations
	if bio.Intellectual >= 50 {
		recommendations = append(recommendations, "Excellent day for learning, problem-solving, and mental work")
	} else if bio.Intellectual <= -50 {
		recommendations = append(recommendations, "Mental fatigue possible - postpone complex tasks")
	} else if math.Abs(bio.Intellectual) < 10 {
		recommendations = append(recommendations, "⚠️ Intellectual critical day - double-check important decisions")
	}

	return recommendations
}

// Helper functions

// calculateCycle computes the biorhythm value for a specific cycle
func calculateCycle(daysLived, cycleDays int) float64 {
	// Biorhythm formula: sin(2π * days / cycle) * 100
	radians := 2 * math.Pi * float64(daysLived) / float64(cycleDays)
	return math.Sin(radians) * 100
}

// daysBetween calculates the number of days between two dates
func daysBetween(start, end time.Time) int {
	start = time.Date(start.Year(), start.Month(), start.Day(), 0, 0, 0, 0, time.UTC)
	end = time.Date(end.Year(), end.Month(), end.Day(), 0, 0, 0, 0, time.UTC)

	return int(end.Sub(start).Hours() / 24)
}

// getPhase returns the phase information for a cycle
func getPhase(cycleName string, daysLived, cycleDays int) Phase {
	position := daysLived % cycleDays
	percentage := float64(position) / float64(cycleDays) * 100
	value := calculateCycle(daysLived, cycleDays)

	var phaseName string
	if value >= 50 {
		phaseName = "high"
	} else if value <= -50 {
		phaseName = "low"
	} else if value >= 0 {
		phaseName = "rising"
	} else {
		phaseName = "falling"
	}

	return Phase{
		Cycle:        cycleName,
		DaysIntoCycle: position,
		TotalDays:    cycleDays,
		Percentage:   percentage,
		PhaseName:    phaseName,
	}
}

// checkCritical checks if a cycle is at a critical point
func checkCritical(date time.Time, cycleName string, currentValue, previousValue float64) []CriticalDay {
	var critical []CriticalDay

	// Check for zero crossing
	if (currentValue >= 0 && previousValue < 0) || (currentValue < 0 && previousValue >= 0) {
		critical = append(critical, CriticalDay{
			Date:  date,
			Cycle: cycleName,
			Type:  "critical",
		})
	}

	// Check for near-zero (within 5%)
	if math.Abs(currentValue) < 5 {
		critical = append(critical, CriticalDay{
			Date:  date,
			Cycle: cycleName,
			Type:  "transition",
		})
	}

	return critical
}

// getBar creates a visual bar representation
func getBar(value float64, width int) string {
	if width <= 0 {
		return ""
	}

	filled := int((value + 100) / 200 * float64(width))
	if filled < 0 {
		filled = 0
	}
	if filled > width {
		filled = width
	}

	bar := ""
	for i := 0; i < width; i++ {
		if i < filled {
			bar += "█"
		} else {
			bar += "░"
		}
	}

	return bar
}