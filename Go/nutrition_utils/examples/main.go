package main

import (
	"fmt"
	nutrition "github.com/ayukyo/alltoolkit/Go/nutrition_utils"
)

func main() {
	fmt.Println("=== Nutrition Utils Examples ===\n")

	// Example 1: Complete Profile Analysis
	exampleProfileAnalysis()

	// Example 2: BMI Calculations
	exampleBMI()

	// Example 3: Calorie Calculations
	exampleCalories()

	// Example 4: Weight Planning
	exampleWeightPlanning()

	// Example 5: Food Database & Scoring
	exampleFoodDatabase()

	// Example 6: Meal & Daily Nutrition
	exampleMealTracking()

	// Example 7: Exercise Calorie Burn
	exampleExercise()

	// Example 8: Macro Calculations
	exampleMacro()
}

func exampleProfileAnalysis() {
	fmt.Println("--- Example 1: Complete Profile Analysis ---")

	profiles := []nutrition.Profile{
		{
			Weight:   70,
			Height:   175,
			Age:      30,
			Gender:   nutrition.Male,
			Activity: nutrition.ModeratelyActive,
			Goal:     nutrition.MaintainWeight,
		},
		{
			Weight:   60,
			Height:   165,
			Age:      25,
			Gender:   nutrition.Female,
			Activity: nutrition.LightlyActive,
			Goal:     nutrition.LoseWeight,
		},
		{
			Weight:   85,
			Height:   180,
			Age:      28,
			Gender:   nutrition.Male,
			Activity: nutrition.VeryActive,
			Goal:     nutrition.BuildMuscle,
		},
	}

	for i, profile := range profiles {
		result, err := nutrition.AnalyzeProfile(profile)
		if err != nil {
			fmt.Printf("Profile %d error: %v\n", i+1, err)
			continue
		}

		fmt.Printf("\nProfile %d (%s, %d years, %.0f kg, %.0f cm):\n",
			i+1, profile.Gender, profile.Age, profile.Weight, profile.Height)
		fmt.Printf("  BMR:            %.0f calories/day\n", result.BMR)
		fmt.Printf("  TDEE:           %.0f calories/day\n", result.TDEE)
		fmt.Printf("  Target Calories: %.0f calories/day (%s)\n",
			result.TargetCalories, goalName(profile.Goal))
		fmt.Printf("  BMI:            %.1f (%s)\n", result.BMI, result.BMICategory)
		fmt.Printf("  Ideal Weight:   %.1f kg (range: %.1f - %.1f)\n",
			result.IdealWeight, result.MinIdealWeight, result.MaxIdealWeight)
		fmt.Printf("  Water Intake:   %.1f L/day\n", result.WaterIntake)
		fmt.Printf("  Macros:         %.0fg protein, %.0fg carbs, %.0fg fat\n",
			result.ProteinGrams, result.CarbGrams, result.FatGrams)
		fmt.Printf("  Fiber:          %.1f g/day\n", result.FiberGrams)
	}

	fmt.Println()
}

func exampleBMI() {
	fmt.Println("--- Example 2: BMI Calculations ---")

	weights := []float64{50, 60, 70, 80, 90, 100}
	height := 175.0

	fmt.Printf("\nBMI for different weights at %.0f cm height:\n", height)
	for _, weight := range weights {
		bmi, err := nutrition.CalculateBMI(weight, height)
		if err != nil {
			continue
		}
		category := nutrition.GetBMICategory(bmi)
		detailed := nutrition.GetBMICategoryDetailed(bmi)
		healthy := nutrition.IsHealthyBMI(bmi)
		fmt.Printf("  %.0f kg: BMI %.1f (%s - %s) Healthy: %v\n",
			weight, bmi, category, detailed, healthy)
	}

	// Calculate weight needed for target BMI
	fmt.Printf("\nWeight needed for target BMIs at %.0f cm:\n", height)
	targetBMIs := []float64{18.5, 21.7, 22.9, 24.9}
	for _, targetBMI := range targetBMIs {
		weight := nutrition.WeightForBMI(targetBMI, height)
		fmt.Printf("  BMI %.1f: %.1f kg\n", targetBMI, weight)
	}

	// Ideal weight range
	minIdeal, maxIdeal := nutrition.CalculateIdealWeightRange(height)
	devineIdeal := nutrition.CalculateIdealWeight(height, nutrition.Male)
	fmt.Printf("\nIdeal weight for %.0f cm (Male):\n", height)
	fmt.Printf("  Devine formula: %.1f kg\n", devineIdeal)
	fmt.Printf("  BMI range (18.5-24.9): %.1f - %.1f kg\n", minIdeal, maxIdeal)

	fmt.Println()
}

func exampleCalories() {
	fmt.Println("--- Example 3: Calorie Calculations ---")

	// BMR comparison
	weight := 70.0
	height := 175.0
	age := 30
	gender := nutrition.Male

	mifflinBMR, _ := nutrition.CalculateBMR(weight, height, age, gender)
	harrisBMR, _ := nutrition.CalculateBMRHarrisBenedict(weight, height, age, gender)

	fmt.Printf("\nBMR comparison for Male, %.0f kg, %.0f cm, %d years:\n", weight, height, age)
	fmt.Printf("  Mifflin-St Jeor: %.0f cal/day\n", mifflinBMR)
	fmt.Printf("  Harris-Benedict: %.0f cal/day\n", harrisBMR)

	// TDEE for different activity levels
	fmt.Printf("\nTDEE for different activity levels (BMR: %.0f):\n", mifflinBMR)
	activities := []nutrition.ActivityLevel{
		nutrition.Sedentary,
		nutrition.LightlyActive,
		nutrition.ModeratelyActive,
		nutrition.VeryActive,
		nutrition.ExtraActive,
	}
	for _, activity := range activities {
		tdee, _ := nutrition.CalculateTDEE(mifflinBMR, activity)
		fmt.Printf("  %s: %.0f cal/day\n", activityName(activity), tdee)
	}

	// Calorie adjustments for goals
	fmt.Printf("\nCalorie adjustments for different goals (TDEE: %.0f):\n", mifflinBMR*1.55)
	goals := []nutrition.Goal{
		nutrition.LoseWeight,
		nutrition.MaintainWeight,
		nutrition.GainWeight,
		nutrition.BuildMuscle,
	}
	tdee := mifflinBMR * 1.55 // Moderately active
	for _, goal := range goals {
		protein, carbs, fat := nutrition.CalculateMacro(tdee, goal)
		fmt.Printf("  %s: %.0f cal (%.0fg protein, %.0fg carbs, %.0fg fat)\n",
			goalName(goal), tdee*goalMultiplier(goal), protein, carbs, fat)
	}

	fmt.Println()
}

func exampleWeightPlanning() {
	fmt.Println("--- Example 4: Weight Planning ---")

	currentWeight := 85.0
	targetWeight := 75.0
	weeks := 12

	deficit := nutrition.CalculateRequiredDeficit(currentWeight, targetWeight, weeks)
	fmt.Printf("\nTo lose %.1f kg in %d weeks:\n", currentWeight-targetWeight, weeks)
	fmt.Printf("  Required daily deficit: %.0f calories\n", deficit)

	// Timeline estimation
	dailyDeficit := 500.0
	timeline := nutrition.CalculateWeightLossTimeline(currentWeight, targetWeight, dailyDeficit)
	fmt.Printf("\nWith %.0f cal/day deficit:\n", dailyDeficit)
	fmt.Printf("  Estimated weeks to reach %.1f kg: %d weeks\n", targetWeight, timeline)

	// Weekly weight change rate
	tdee := 2500.0
	calorieIntakes := []float64{1500, 2000, 2500, 3000}
	fmt.Printf("\nWeekly weight change at different calorie intakes (TDEE: %.0f):\n", tdee)
	for _, intake := range calorieIntakes {
		rate := nutrition.WeightChangeRate(intake, tdee)
		direction := "lose"
		if rate > 0 {
			direction = "gain"
		}
		fmt.Printf("  %.0f cal/day: %.2f kg/week (%s)\n", intake, rate, direction)
	}

	fmt.Println()
}

func exampleFoodDatabase() {
	fmt.Println("--- Example 5: Food Database & Scoring ---")

	fmt.Println("\nCommon foods in database:")
	for name, food := range nutrition.CommonFoods {
		fmt.Printf("  %s: %.0f cal, %.1fg protein, %.1fg carbs, %.1fg fat\n",
			name, food.Calories, food.Protein, food.Carbs, food.Fat)
	}

	// Food scoring
	fmt.Println("\nNutrition scores for common foods:")
	scoredFoods := []string{"chicken_breast", "broccoli", "banana", "beef", "spinach"}
	for _, name := range scoredFoods {
		food, ok := nutrition.GetFood(name)
		if !ok {
			continue
		}
		score := nutrition.ScoreFood(food)
		fmt.Printf("  %s: Score %.1f (Grade %s)\n", food.Name, score.Overall, score.Grade)
		fmt.Printf("    Calorie density: %.1f, Protein: %.1f, Balance: %.1f\n",
			score.Calorie, score.Protein, score.Balance)
	}

	// Add custom food
	customFood := nutrition.Food{
		Name:        "Custom Protein Bar",
		ServingSize: 60,
		Calories:    220,
		Protein:     20,
		Carbs:       25,
		Fat:         7,
		Fiber:       3,
	}
	nutrition.AddFood("protein_bar", customFood)

	retrieved, ok := nutrition.GetFood("protein_bar")
	if ok {
		score := nutrition.ScoreFood(retrieved)
		fmt.Printf("\nAdded custom food: %s\n", retrieved.Name)
		fmt.Printf("  Score: %.1f (Grade %s)\n", score.Overall, score.Grade)
	}

	fmt.Println()
}

func exampleMealTracking() {
	fmt.Println("--- Example 6: Meal & Daily Nutrition ---")

	// Create meals
	breakfast := nutrition.Meal{
		Name: "Breakfast",
		Foods: []nutrition.FoodItem{
			{Food: nutrition.CommonFoods["egg"], Quantity: 2},
			{Food: nutrition.CommonFoods["oatmeal"], Quantity: 1.5},
			{Food: nutrition.CommonFoods["banana"], Quantity: 0.5},
		},
	}

	lunch := nutrition.Meal{
		Name: "Lunch",
		Foods: []nutrition.FoodItem{
			{Food: nutrition.CommonFoods["chicken_breast"], Quantity: 1.5},
			{Food: nutrition.CommonFoods["brown_rice"], Quantity: 2},
			{Food: nutrition.CommonFoods["broccoli"], Quantity: 1},
		},
	}

	dinner := nutrition.Meal{
		Name: "Dinner",
		Foods: []nutrition.FoodItem{
			{Food: nutrition.CommonFoods["salmon"], Quantity: 1},
			{Food: nutrition.CommonFoods["sweet_potato"], Quantity: 1.5},
			{Food: nutrition.CommonFoods["spinach"], Quantity: 2},
		},
	}

	// Calculate each meal's nutrition
	meals := []nutrition.Meal{breakfast, lunch, dinner}
	fmt.Println("\nNutrition breakdown by meal:")
	totalCal := 0.0
	totalProtein := 0.0
	for _, meal := range meals {
		nut := nutrition.CalculateMealNutrition(meal)
		fmt.Printf("  %s: %.0f cal, %.1fg protein, %.1fg carbs, %.1fg fat\n",
			meal.Name, nut.Calories, nut.Protein, nut.Carbs, nut.Fat)
		totalCal += nut.Calories
		totalProtein += nut.Protein
	}

	// Daily total
	dailyLog := nutrition.DailyLog{Meals: meals, WaterIntake: 2.5}
	dailyNut := nutrition.CalculateDailyNutrition(dailyLog)

	fmt.Println("\nDaily totals:")
	fmt.Printf("  Calories:   %.0f\n", dailyNut.Calories)
	fmt.Printf("  Protein:    %.1f g\n", dailyNut.Protein)
	fmt.Printf("  Carbs:      %.1f g\n", dailyNut.Carbs)
	fmt.Printf("  Fat:        %.1f g\n", dailyNut.Fat)
	fmt.Printf("  Fiber:      %.1f g\n", dailyNut.Fiber)

	// Calculate from macros
	calculatedCal := nutrition.CalculateCaloriesFromMacro(
		dailyNut.Protein, dailyNut.Carbs, dailyNut.Fat)
	fmt.Printf("  Cal from macros: %.0f\n", calculatedCal)

	fmt.Println()
}

func exampleExercise() {
	fmt.Println("--- Example 7: Exercise Calorie Burn ---")

	weight := 70.0
	duration := 30.0

	fmt.Printf("\nCalories burned for %.0f kg person in %.0f minutes:\n", weight, duration)
	activities := []string{
		"walking", "running", "cycling", "swimming", "weightlifting",
		"yoga", "hiking", "basketball", "tennis", "boxing",
	}
	for _, activity := range activities {
		burned := nutrition.CalculateCaloriesBurned(activity, weight, duration)
		fmt.Printf("  %s: %.1f cal\n", activity, burned)
	}

	// Hourly burn
	fmt.Printf("\nCalories burned for 1 hour activities:\n")
	hourActivities := []string{"running", "swimming", "resting", "office_work", "housework"}
	for _, activity := range hourActivities {
		burned := nutrition.CalculateCaloriesBurned(activity, weight, 60)
		fmt.Printf("  %s: %.1f cal\n", activity, burned)
	}

	fmt.Println()
}

func exampleMacro() {
	fmt.Println("--- Example 8: Macro Calculations ---")

	calories := 2000.0

	fmt.Printf("\nMacro distribution for %.0f calories:\n", calories)

	ratios := []struct {
		name     string
		protein  float64
		carb     float64
		fat      float64
	}{
		{"Standard", 25, 50, 25},
		{"High Protein", 35, 35, 30},
		{"Low Carb", 30, 20, 50},
		{"Athletic", 30, 45, 25},
	}

	for _, ratio := range ratios {
		protein, carbs, fat := nutrition.CalculateMacroFromCalories(
			calories, ratio.protein, ratio.carb, ratio.fat)
		fmt.Printf("  %s: %.0fg protein, %.0fg carbs, %.0fg fat\n",
			ratio.name, protein, carbs, fat)
	}

	// Fiber recommendations
	calorieLevels := []float64{1500, 2000, 2500, 3000}
	fmt.Printf("\nFiber recommendations:\n")
	for _, cal := range calorieLevels {
		fiber := nutrition.CalculateFiber(cal)
		fmt.Printf("  %.0f cal: %.1f g fiber\n", cal, fiber)
	}

	// Water intake by weight and activity
	fmt.Printf("\nWater intake recommendations:\n")
	weights := []float64{50, 60, 70, 80, 90}
	for _, w := range weights {
		sedentary := nutrition.CalculateWaterIntake(w, nutrition.Sedentary)
		active := nutrition.CalculateWaterIntake(w, nutrition.VeryActive)
		fmt.Printf("  %.0f kg: %.1f L (sedentary), %.1f L (very active)\n",
			w, sedentary, active)
	}

	fmt.Println()
}

// Helper functions
func activityName(a nutrition.ActivityLevel) string {
	names := map[nutrition.ActivityLevel]string{
		nutrition.Sedentary:        "Sedentary",
		nutrition.LightlyActive:    "Lightly Active",
		nutrition.ModeratelyActive: "Moderately Active",
		nutrition.VeryActive:       "Very Active",
		nutrition.ExtraActive:      "Extra Active",
	}
	return names[a]
}

func goalName(g nutrition.Goal) string {
	names := map[nutrition.Goal]string{
		nutrition.LoseWeight:    "Lose Weight",
		nutrition.MaintainWeight: "Maintain Weight",
		nutrition.GainWeight:     "Gain Weight",
		nutrition.BuildMuscle:    "Build Muscle",
	}
	return names[g]
}

func goalMultiplier(g nutrition.Goal) float64 {
	multipliers := map[nutrition.Goal]float64{
		nutrition.LoseWeight:     0.8,
		nutrition.MaintainWeight: 1.0,
		nutrition.GainWeight:     1.15,
		nutrition.BuildMuscle:    1.1,
	}
	return multipliers[g]
}