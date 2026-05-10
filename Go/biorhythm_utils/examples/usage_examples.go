// Example usage of biorhythm_utils package
package main

import (
	"fmt"
	"time"

	bio "github.com/openclaw/alltoolkit/Go/biorhythm_utils"
)

func main() {
	fmt.Println("=== Biorhythm Calculator Examples ===")
	fmt.Println()

	// Example 1: Basic biorhythm calculation
	example1BasicCalculation()

	// Example 2: Calculate for specific date
	example2SpecificDate()

	// Example 3: Find critical days
	example3CriticalDays()

	// Example 4: Range calculation
	example4RangeCalculation()

	// Example 5: Predict peaks and troughs
	example5Predictions()

	// Example 6: Compatibility score
	example6Compatibility()

	// Example 7: Find best days
	example7BestDays()

	// Example 8: Get recommendations
	example8Recommendations()
}

func example1BasicCalculation() {
	fmt.Println("=== Example 1: Basic Calculation ===")

	// Parse birth date
	birthDate, err := bio.ParseBirthDate("1990-05-15")
	if err != nil {
		fmt.Printf("Error parsing date: %v\n", err)
		return
	}

	// Create calculator
	calc := bio.NewCalculator(birthDate)

	// Calculate today's biorhythm
	today := calc.CalculateToday()

	fmt.Printf("Birth Date: %s\n", birthDate.Format("2006-01-02"))
	fmt.Printf("Today's Biorhythm:\n")
	fmt.Println(bio.FormatBiorhythm(today))
	fmt.Println()
}

func example2SpecificDate() {
	fmt.Println("=== Example 2: Specific Date Calculation ===")

	birthDate, _ := bio.ParseBirthDate("1985-03-20")
	calc := bio.NewCalculator(birthDate)

	// Calculate for a specific important date
	weddingDate, _ := bio.ParseBirthDate("2024-06-15")
	result := calc.Calculate(weddingDate)

	fmt.Printf("Biorhythm for wedding day (%s):\n", weddingDate.Format("2006-01-02"))
	fmt.Printf("  Physical:     %+.1f%%\n", result.Physical)
	fmt.Printf("  Emotional:    %+.1f%%\n", result.Emotional)
	fmt.Printf("  Intellectual: %+.1f%%\n", result.Intellectual)
	fmt.Printf("  Intuitive:    %+.1f%%\n", result.Intuitive)
	fmt.Println()
}

func example3CriticalDays() {
	fmt.Println("=== Example 3: Finding Critical Days ===")

	birthDate, _ := bio.ParseBirthDate("1992-08-10")
	calc := bio.NewCalculator(birthDate)

	// Find critical days in the next month
	today := time.Now()
	nextMonth := today.AddDate(0, 1, 0)

	criticalDays := calc.FindCriticalDays(today, nextMonth)

	fmt.Printf("Critical days in the next month:\n")
	for i, cd := range criticalDays {
		if i >= 10 {
			fmt.Printf("  ... and %d more\n", len(criticalDays)-i)
			break
		}
		fmt.Printf("  %s: %s cycle (%s)\n",
			cd.Date.Format("2006-01-02"),
			cd.Cycle,
			cd.Type)
	}
	fmt.Println()
}

func example4RangeCalculation() {
	fmt.Println("=== Example 4: Range Calculation ===")

	birthDate, _ := bio.ParseBirthDate("1988-12-25")
	calc := bio.NewCalculator(birthDate)

	// Calculate biorhythm for the next 7 days
	results := calc.CalculateForDays(time.Now(), 7)

	fmt.Println("Biorhythm for the next 7 days:")
	fmt.Printf("%-12s %10s %10s %10s %10s\n", "Date", "Physical", "Emotional", "Intellectual", "Intuitive")
	fmt.Println(string(make([]byte, 60)))
	for _, r := range results {
		fmt.Printf("%-12s %9.1f%% %9.1f%% %9.1f%% %9.1f%%\n",
			r.Date.Format("2006-01-02"),
			r.Physical,
			r.Emotional,
			r.Intellectual,
			r.Intuitive)
	}
	fmt.Println()
}

func example5Predictions() {
	fmt.Println("=== Example 5: Predicting Peaks and Troughs ===")

	birthDate, _ := bio.ParseBirthDate("1995-02-14")
	calc := bio.NewCalculator(birthDate)
	today := time.Now()

	fmt.Println("Upcoming biorhythm events:")
	fmt.Println()

	// Predict for each cycle
	cycles := []struct {
		name      string
		days      int
	}{
		{"Physical", bio.PhysicalCycleDays},
		{"Emotional", bio.EmotionalCycleDays},
		{"Intellectual", bio.IntellectualCycleDays},
		{"Intuitive", bio.IntuitiveCycleDays},
	}

	for _, cycle := range cycles {
		nextPeak := calc.PredictNextPeak(cycle.days, today)
		nextTrough := calc.PredictNextTrough(cycle.days, today)
		nextCritical := calc.PredictNextCritical(cycle.days, today)

		fmt.Printf("%s cycle (%d days):\n", cycle.name, cycle.days)
		fmt.Printf("  Next peak:     %s\n", nextPeak.Format("2006-01-02 (Monday)"))
		fmt.Printf("  Next trough:   %s\n", nextTrough.Format("2006-01-02 (Monday)"))
		fmt.Printf("  Next critical: %s\n", nextCritical.Format("2006-01-02 (Monday)"))
		fmt.Println()
	}
}

func example6Compatibility() {
	fmt.Println("=== Example 6: Compatibility Score ===")

	// Calculate compatibility between two people
	person1Birth, _ := bio.ParseBirthDate("1990-05-15")
	person2Birth, _ := bio.ParseBirthDate("1992-08-22")

	score := bio.GetCompatibilityScore(person1Birth, person2Birth)

	fmt.Printf("Person 1 Birth: %s\n", person1Birth.Format("2006-01-02"))
	fmt.Printf("Person 2 Birth: %s\n", person2Birth.Format("2006-01-02"))
	fmt.Printf("Compatibility Score: %.1f%%\n", score)

	// Interpret the score
	var interpretation string
	switch {
	case score >= 80:
		interpretation = "Excellent! Your biorhythms are highly aligned."
	case score >= 60:
		interpretation = "Good! Your biorhythms are well-matched."
	case score >= 40:
		interpretation = "Moderate. Some cycles align, others differ."
	default:
		interpretation = "Low. Your biorhythms are often out of sync."
	}
	fmt.Printf("Interpretation: %s\n\n", interpretation)
}

func example7BestDays() {
	fmt.Println("=== Example 7: Finding Best Days ===")

	birthDate, _ := bio.ParseBirthDate("1991-07-04")
	calc := bio.NewCalculator(birthDate)

	// Find high-energy days in the next month
	today := time.Now()
	nextMonth := today.AddDate(0, 1, 0)

	highDays := calc.FindHighDays(today, nextMonth, 70)

	fmt.Println("Days with all cycles above 70% in the next month:")
	for i, d := range highDays {
		if i >= 5 {
			fmt.Printf("  ... and %d more days\n", len(highDays)-i)
			break
		}
		fmt.Printf("  %s: P=%.0f%% E=%.0f%% I=%.0f%%\n",
			d.Date.Format("2006-01-02 (Mon)"),
			d.Physical, d.Emotional, d.Intellectual)
	}

	// Find low-energy days
	lowDays := calc.FindLowDays(today, nextMonth, -70)

	fmt.Println("\nDays with any cycle below -70%:")
	for i, d := range lowDays {
		if i >= 5 {
			fmt.Printf("  ... and %d more days\n", len(lowDays)-i)
			break
		}
		fmt.Printf("  %s: P=%.0f%% E=%.0f%% I=%.0f%%\n",
			d.Date.Format("2006-01-02 (Mon)"),
			d.Physical, d.Emotional, d.Intellectual)
	}
	fmt.Println()
}

func example8Recommendations() {
	fmt.Println("=== Example 8: Daily Recommendations ===")

	birthDate, _ := bio.ParseBirthDate("1993-11-30")
	calc := bio.NewCalculator(birthDate)

	// Get today's biorhythm and recommendations
	today := calc.CalculateToday()
	recommendations := bio.GetRecommendation(today)

	fmt.Printf("Today's Biorhythm (%s):\n", today.Date.Format("2006-01-02"))
	fmt.Println(bio.FormatBiorhythm(today))
	fmt.Println()

	fmt.Println("Recommendations:")
	for i, rec := range recommendations {
		fmt.Printf("%d. %s\n", i+1, rec)
	}

	// Get phase information
	fmt.Println("\nCurrent Cycle Phases:")
	phases := calc.GetPhases(today.Date)
	for _, p := range phases {
		fmt.Printf("  %s: Day %d/%d (%.1f%%) - %s\n",
			p.Cycle, p.DaysIntoCycle, p.TotalDays, p.Percentage, p.PhaseName)
	}

	// Overall score
	score := calc.GetOverallScore(today.Date)
	fmt.Printf("\nOverall Energy Score: %.1f%%\n", score)
	fmt.Println()
}