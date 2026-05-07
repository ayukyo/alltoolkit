// Package nutrition_utils provides nutrition calculation and analysis utilities.
// Zero external dependencies - pure Go standard library implementation.
package nutrition_utils

import (
	"errors"
	"math"
)

// Errors
var (
	ErrInvalidWeight    = errors.New("weight must be positive")
	ErrInvalidHeight    = errors.New("height must be positive")
	ErrInvalidAge       = errors.New("age must be positive")
	ErrInvalidGender    = errors.New("invalid gender (use 'M' or 'F')")
	ErrInvalidActivity  = errors.New("invalid activity level")
	ErrInvalidGoal      = errors.New("invalid goal")
)

// Gender represents biological sex for BMR calculations
type Gender string

const (
	Male   Gender = "M"
	Female Gender = "F"
)

// ActivityLevel represents daily activity level
type ActivityLevel int

const (
	Sedentary      ActivityLevel = iota // Little or no exercise
	LightlyActive                       // Light exercise 1-3 days/week
	ModeratelyActive                    // Moderate exercise 3-5 days/week
	VeryActive                          // Hard exercise 6-7 days/week
	ExtraActive                         // Very hard exercise & physical job
)

// ActivityMultipliers returns the TDEE multiplier for each activity level
var activityMultipliers = map[ActivityLevel]float64{
	Sedentary:        1.2,
	LightlyActive:    1.375,
	ModeratelyActive: 1.55,
	VeryActive:       1.725,
	ExtraActive:      1.9,
}

// Goal represents fitness goal
type Goal int

const (
	LoseWeight    Goal = iota // Caloric deficit
	MaintainWeight             // Maintenance calories
	GainWeight                 // Caloric surplus
	BuildMuscle                // Slight surplus with high protein
)

// GoalMultipliers returns the calorie adjustment for each goal
var goalMultipliers = map[Goal]float64{
	LoseWeight:    0.8,  // 20% deficit
	MaintainWeight: 1.0,  // Maintenance
	GainWeight:     1.15, // 15% surplus
	BuildMuscle:    1.1,  // 10% surplus
}

// Profile represents a person's physical profile
type Profile struct {
	Weight      float64       // in kg
	Height      float64       // in cm
	Age         int           // in years
	Gender      Gender        // M or F
	Activity    ActivityLevel // Activity level
	Goal        Goal          // Fitness goal
	BodyFat     float64       // Body fat percentage (optional, 0 if unknown)
}

// NutritionResult contains calculated nutrition information
type NutritionResult struct {
	BMR               float64   // Basal Metabolic Rate (calories/day)
	TDEE              float64   // Total Daily Energy Expenditure
	TargetCalories    float64   // Target daily calories based on goal
	BMI               float64   // Body Mass Index
	BMICategory       string    // BMI category
	IdealWeight       float64   // Ideal weight range (Devine formula)
	MinIdealWeight    float64   // Minimum ideal weight (BMI 18.5)
	MaxIdealWeight    float64   // Maximum ideal weight (BMI 24.9)
	WaterIntake       float64   // Recommended daily water intake (liters)
	ProteinGrams      float64   // Recommended daily protein (grams)
	CarbGrams         float64   // Recommended daily carbs (grams)
	FatGrams          float64   // Recommended daily fat (grams)
	FiberGrams        float64   // Recommended daily fiber (grams)
	MacroRatio        MacroRatio // Macronutrient ratio
}

// MacroRatio represents macronutrient distribution
type MacroRatio struct {
	ProteinPercent float64 // Percentage of calories from protein
	CarbPercent    float64 // Percentage of calories from carbs
	FatPercent     float64 // Percentage of calories from fat
}

// Food represents a food item with nutritional information
type Food struct {
	Name          string
	ServingSize   float64 // in grams
	Calories      float64 // per serving
	Protein       float64 // grams per serving
	Carbs         float64 // grams per serving
	Fat           float64 // grams per serving
	Fiber         float64 // grams per serving
	Sugar         float64 // grams per serving
	Sodium        float64 // mg per serving
	Cholesterol   float64 // mg per serving
	SaturatedFat  float64 // grams per serving
	TransFat      float64 // grams per serving
}

// Meal represents a collection of foods
type Meal struct {
	Name  string
	Foods []FoodItem
}

// FoodItem represents a food with quantity
type FoodItem struct {
	Food     Food
	Quantity float64 // multiplier of serving size
}

// DailyLog represents a day's food log
type DailyLog struct {
	Meals     []Meal
	WaterIntake float64 // liters
}

// CalculateBMR calculates Basal Metabolic Rate using Mifflin-St Jeor equation
func CalculateBMR(weight, height float64, age int, gender Gender) (float64, error) {
	if weight <= 0 {
		return 0, ErrInvalidWeight
	}
	if height <= 0 {
		return 0, ErrInvalidHeight
	}
	if age <= 0 {
		return 0, ErrInvalidAge
	}
	if gender != Male && gender != Female {
		return 0, ErrInvalidGender
	}

	var bmr float64
	if gender == Male {
		bmr = 10*weight + 6.25*height - 5*float64(age) + 5
	} else {
		bmr = 10*weight + 6.25*height - 5*float64(age) - 161
	}

	return bmr, nil
}

// CalculateBMRHarrisBenedict calculates BMR using Harris-Benedict equation (older formula)
func CalculateBMRHarrisBenedict(weight, height float64, age int, gender Gender) (float64, error) {
	if weight <= 0 {
		return 0, ErrInvalidWeight
	}
	if height <= 0 {
		return 0, ErrInvalidHeight
	}
	if age <= 0 {
		return 0, ErrInvalidAge
	}
	if gender != Male && gender != Female {
		return 0, ErrInvalidGender
	}

	var bmr float64
	if gender == Male {
		bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * float64(age))
	} else {
		bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * float64(age))
	}

	return bmr, nil
}

// CalculateTDEE calculates Total Daily Energy Expenditure
func CalculateTDEE(bmr float64, activity ActivityLevel) (float64, error) {
	multiplier, ok := activityMultipliers[activity]
	if !ok {
		return 0, ErrInvalidActivity
	}
	return bmr * multiplier, nil
}

// CalculateBMI calculates Body Mass Index
func CalculateBMI(weight, height float64) (float64, error) {
	if weight <= 0 {
		return 0, ErrInvalidWeight
	}
	if height <= 0 {
		return 0, ErrInvalidHeight
	}

	// Height in cm, convert to meters
	heightM := height / 100
	return weight / (heightM * heightM), nil
}

// GetBMICategory returns the BMI category
func GetBMICategory(bmi float64) string {
	switch {
	case bmi < 18.5:
		return "Underweight"
	case bmi < 25:
		return "Normal"
	case bmi < 30:
		return "Overweight"
	default:
		return "Obese"
	}
}

// GetBMICategoryDetailed returns more detailed BMI categories
func GetBMICategoryDetailed(bmi float64) string {
	switch {
	case bmi < 16:
		return "Severely Underweight"
	case bmi < 18.5:
		return "Underweight"
	case bmi < 25:
		return "Normal"
	case bmi < 30:
		return "Overweight"
	case bmi < 35:
		return "Obese Class I"
	case bmi < 40:
		return "Obese Class II"
	default:
		return "Obese Class III"
	}
}

// CalculateIdealWeight calculates ideal weight using Devine formula
func CalculateIdealWeight(height float64, gender Gender) float64 {
	// Devine formula
	// For men: 50 + 2.3 kg for each inch over 5 feet
	// For women: 45.5 + 2.3 kg for each inch over 5 feet

	heightInches := height / 2.54 // Convert cm to inches
	inchesOver5Feet := heightInches - 60

	if gender == Male {
		return 50 + 2.3*inchesOver5Feet
	}
	return 45.5 + 2.3*inchesOver5Feet
}

// CalculateIdealWeightRange calculates ideal weight range based on BMI
func CalculateIdealWeightRange(height float64) (min, max float64) {
	heightM := height / 100
	min = 18.5 * heightM * heightM
	max = 24.9 * heightM * heightM
	return min, max
}

// CalculateWaterIntake calculates recommended daily water intake
func CalculateWaterIntake(weight float64, activity ActivityLevel) float64 {
	// Base: 30-35 ml per kg of body weight
	baseIntake := weight * 0.033 // liters

	// Adjust for activity
	switch activity {
	case LightlyActive:
		baseIntake *= 1.1
	case ModeratelyActive:
		baseIntake *= 1.2
	case VeryActive:
		baseIntake *= 1.3
	case ExtraActive:
		baseIntake *= 1.4
	}

	return math.Round(baseIntake*10) / 10
}

// CalculateMacro calculates macronutrient distribution
func CalculateMacro(calories float64, goal Goal) (protein, carbs, fat float64) {
	var ratio MacroRatio

	switch goal {
	case LoseWeight:
		ratio = MacroRatio{ProteinPercent: 35, CarbPercent: 35, FatPercent: 30}
	case GainWeight, BuildMuscle:
		ratio = MacroRatio{ProteinPercent: 30, CarbPercent: 45, FatPercent: 25}
	default:
		ratio = MacroRatio{ProteinPercent: 25, CarbPercent: 50, FatPercent: 25}
	}

	// Protein: 4 cal/g, Carbs: 4 cal/g, Fat: 9 cal/g
	protein = (calories * ratio.ProteinPercent / 100) / 4
	carbs = (calories * ratio.CarbPercent / 100) / 4
	fat = (calories * ratio.FatPercent / 100) / 9

	return protein, carbs, fat
}

// CalculateFiber calculates recommended daily fiber intake
func CalculateFiber(calories float64) float64 {
	// 14g per 1000 calories is the general recommendation
	return 14 * (calories / 1000)
}

// AnalyzeProfile performs complete nutrition analysis for a profile
func AnalyzeProfile(p Profile) (*NutritionResult, error) {
	// Calculate BMR
	bmr, err := CalculateBMR(p.Weight, p.Height, p.Age, p.Gender)
	if err != nil {
		return nil, err
	}

	// Calculate TDEE
	tdee, err := CalculateTDEE(bmr, p.Activity)
	if err != nil {
		return nil, err
	}

	// Calculate target calories based on goal
	targetCalories := tdee * goalMultipliers[p.Goal]

	// Calculate BMI
	bmi, err := CalculateBMI(p.Weight, p.Height)
	if err != nil {
		return nil, err
	}

	// Calculate ideal weight
	idealWeight := CalculateIdealWeight(p.Height, p.Gender)
	minIdeal, maxIdeal := CalculateIdealWeightRange(p.Height)

	// Calculate water intake
	waterIntake := CalculateWaterIntake(p.Weight, p.Activity)

	// Calculate macros
	protein, carbs, fat := CalculateMacro(targetCalories, p.Goal)
	fiber := CalculateFiber(targetCalories)

	// Get macro ratio
	var ratio MacroRatio
	switch p.Goal {
	case LoseWeight:
		ratio = MacroRatio{ProteinPercent: 35, CarbPercent: 35, FatPercent: 30}
	case GainWeight, BuildMuscle:
		ratio = MacroRatio{ProteinPercent: 30, CarbPercent: 45, FatPercent: 25}
	default:
		ratio = MacroRatio{ProteinPercent: 25, CarbPercent: 50, FatPercent: 25}
	}

	return &NutritionResult{
		BMR:            math.Round(bmr*10) / 10,
		TDEE:           math.Round(tdee*10) / 10,
		TargetCalories: math.Round(targetCalories*10) / 10,
		BMI:            math.Round(bmi*10) / 10,
		BMICategory:    GetBMICategory(bmi),
		IdealWeight:    math.Round(idealWeight*10) / 10,
		MinIdealWeight: math.Round(minIdeal*10) / 10,
		MaxIdealWeight: math.Round(maxIdeal*10) / 10,
		WaterIntake:    waterIntake,
		ProteinGrams:   math.Round(protein*10) / 10,
		CarbGrams:      math.Round(carbs*10) / 10,
		FatGrams:       math.Round(fat*10) / 10,
		FiberGrams:     math.Round(fiber*10) / 10,
		MacroRatio:     ratio,
	}, nil
}

// CalculateCaloriesBurned estimates calories burned for various activities
func CalculateCaloriesBurned(activity string, weight float64, durationMinutes float64) float64 {
	// MET values for various activities
	metValues := map[string]float64{
		"walking":        3.5,
		"running":        9.8,
		"cycling":        7.5,
		"swimming":       8.0,
		"weightlifting":  6.0,
		"yoga":           3.0,
		"dancing":        5.0,
		"hiking":         6.0,
		"basketball":     8.0,
		"soccer":         8.5,
		"tennis":         7.3,
		"golf":           4.3,
		"rowing":         7.0,
		"jumping_jacks":  8.0,
		"pushups":        3.8,
		"situps":         3.8,
		"squats":         5.0,
		"plank":          3.0,
		"jump_rope":      12.0,
		"burpees":        10.0,
		"stairs":         9.0,
		"aerobics":       7.3,
		"pilates":        3.0,
		"boxing":         9.0,
		"sprinting":      15.0,
		"resting":        1.0,
		"sleeping":       0.9,
		"office_work":    1.5,
		"housework":       3.5,
		"gardening":      4.0,
	}

	met, ok := metValues[activity]
	if !ok {
		met = 5.0 // Default moderate activity
	}

	// Calories = MET × weight (kg) × duration (hours)
	hours := durationMinutes / 60
	calories := met * weight * hours

	return math.Round(calories * 10) / 10
}

// CalculateRequiredDeficit calculates daily caloric deficit needed to lose weight
func CalculateRequiredDeficit(currentWeight, targetWeight float64, weeks int) float64 {
	// 1 kg of fat ≈ 7700 calories
	totalWeightToLose := currentWeight - targetWeight
	if totalWeightToLose <= 0 {
		return 0
	}

	totalCaloriesToBurn := totalWeightToLose * 7700
	days := float64(weeks * 7)
	dailyDeficit := totalCaloriesToBurn / days

	return math.Round(dailyDeficit)
}

// CalculateWeightLossTimeline estimates weeks needed to reach target weight
func CalculateWeightLossTimeline(currentWeight, targetWeight, dailyDeficit float64) int {
	totalWeightToLose := currentWeight - targetWeight
	if totalWeightToLose <= 0 || dailyDeficit <= 0 {
		return 0
	}

	totalCaloriesToBurn := totalWeightToLose * 7700
	days := totalCaloriesToBurn / dailyDeficit
	weeks := int(math.Ceil(days / 7))

	return weeks
}

// FoodInfo returns nutritional information per 100g
func (f Food) FoodInfo() Food {
	return Food{
		Name:         f.Name,
		ServingSize:  100,
		Calories:     f.Calories * 100 / f.ServingSize,
		Protein:      f.Protein * 100 / f.ServingSize,
		Carbs:        f.Carbs * 100 / f.ServingSize,
		Fat:          f.Fat * 100 / f.ServingSize,
		Fiber:        f.Fiber * 100 / f.ServingSize,
		Sugar:        f.Sugar * 100 / f.ServingSize,
		Sodium:       f.Sodium * 100 / f.ServingSize,
		Cholesterol:  f.Cholesterol * 100 / f.ServingSize,
		SaturatedFat: f.SaturatedFat * 100 / f.ServingSize,
		TransFat:     f.TransFat * 100 / f.ServingSize,
	}
}

// CalculateNutrition calculates total nutrition for a food item
func (fi FoodItem) CalculateNutrition() Food {
	return Food{
		Name:         fi.Food.Name,
		ServingSize:  fi.Food.ServingSize * fi.Quantity,
		Calories:      fi.Food.Calories * fi.Quantity,
		Protein:       fi.Food.Protein * fi.Quantity,
		Carbs:         fi.Food.Carbs * fi.Quantity,
		Fat:           fi.Food.Fat * fi.Quantity,
		Fiber:         fi.Food.Fiber * fi.Quantity,
		Sugar:         fi.Food.Sugar * fi.Quantity,
		Sodium:        fi.Food.Sodium * fi.Quantity,
		Cholesterol:   fi.Food.Cholesterol * fi.Quantity,
		SaturatedFat:  fi.Food.SaturatedFat * fi.Quantity,
		TransFat:      fi.Food.TransFat * fi.Quantity,
	}
}

// CalculateMealNutrition calculates total nutrition for a meal
func CalculateMealNutrition(meal Meal) Food {
	total := Food{Name: meal.Name}

	for _, item := range meal.Foods {
		nutrition := item.CalculateNutrition()
		total.Calories += nutrition.Calories
		total.Protein += nutrition.Protein
		total.Carbs += nutrition.Carbs
		total.Fat += nutrition.Fat
		total.Fiber += nutrition.Fiber
		total.Sugar += nutrition.Sugar
		total.Sodium += nutrition.Sodium
		total.Cholesterol += nutrition.Cholesterol
		total.SaturatedFat += nutrition.SaturatedFat
		total.TransFat += nutrition.TransFat
		total.ServingSize += nutrition.ServingSize
	}

	return total
}

// CalculateDailyNutrition calculates total nutrition for a day
func CalculateDailyNutrition(log DailyLog) Food {
	total := Food{Name: "Daily Total"}

	for _, meal := range log.Meals {
		nutrition := CalculateMealNutrition(meal)
		total.Calories += nutrition.Calories
		total.Protein += nutrition.Protein
		total.Carbs += nutrition.Carbs
		total.Fat += nutrition.Fat
		total.Fiber += nutrition.Fiber
		total.Sugar += nutrition.Sugar
		total.Sodium += nutrition.Sodium
		total.Cholesterol += nutrition.Cholesterol
		total.SaturatedFat += nutrition.SaturatedFat
		total.TransFat += nutrition.TransFat
		total.ServingSize += nutrition.ServingSize
	}

	return total
}

// NutrientScore represents a nutritional quality score
type NutrientScore struct {
	Overall     float64 // 0-100
	Calorie     float64 // Calorie density score
	Protein     float64 // Protein quality score
	Micronutrient float64 // Micronutrient score
	Balance     float64 // Macro balance score
	Grade       string  // Letter grade (A-F)
}

// ScoreFood calculates a nutritional score for a food item
func ScoreFood(f Food) NutrientScore {
	var score NutrientScore

	// Calorie density score (lower is better)
	calorieDensity := f.Calories / f.ServingSize * 100
	score.Calorie = math.Max(0, 100-calorieDensity/5)

	// Protein score (higher protein % of calories is better)
	if f.Calories > 0 {
		proteinCalories := f.Protein * 4
		proteinPercent := (proteinCalories / f.Calories) * 100
		score.Protein = math.Min(100, proteinPercent*2.5)
	}

	// Balance score (based on macro distribution)
	carbCal := f.Carbs * 4
	fatCal := f.Fat * 9
	proteinCal := f.Protein * 4
	totalCal := carbCal + fatCal + proteinCal

	if totalCal > 0 {
		carbP := carbCal / totalCal * 100
		fatP := fatCal / totalCal * 100
		proteinP := proteinCal / totalCal * 100

		// Ideal: 45-65% carbs, 20-35% fat, 10-35% protein
		carbScore := 100 - math.Abs(carbP-55)*2
		fatScore := 100 - math.Abs(fatP-27.5)*3
		proteinScore := 100 - math.Abs(proteinP-17.5)*2

		score.Balance = math.Max(0, (carbScore+fatScore+proteinScore)/3)
	}

	// Micronutrient proxy (fiber content)
	if f.ServingSize > 0 {
		fiberDensity := f.Fiber / f.ServingSize * 100
		score.Micronutrient = math.Min(100, fiberDensity*10)
	}

	// Overall score
	score.Overall = (score.Calorie*0.2 + score.Protein*0.25 + score.Balance*0.3 + score.Micronutrient*0.25)

	// Grade
	switch {
	case score.Overall >= 90:
		score.Grade = "A"
	case score.Overall >= 80:
		score.Grade = "B"
	case score.Overall >= 70:
		score.Grade = "C"
	case score.Overall >= 60:
		score.Grade = "D"
	default:
		score.Grade = "F"
	}

	return score
}

// Common foods database
var CommonFoods = map[string]Food{
	"chicken_breast": {
		Name: "Chicken Breast", ServingSize: 100,
		Calories: 165, Protein: 31, Carbs: 0, Fat: 3.6, Fiber: 0,
	},
	"brown_rice": {
		Name: "Brown Rice", ServingSize: 100,
		Calories: 216, Protein: 5, Carbs: 45, Fat: 1.8, Fiber: 3.5,
	},
	"broccoli": {
		Name: "Broccoli", ServingSize: 100,
		Calories: 55, Protein: 3.7, Carbs: 11.2, Fat: 0.6, Fiber: 5.1,
	},
	"salmon": {
		Name: "Salmon", ServingSize: 100,
		Calories: 208, Protein: 20, Carbs: 0, Fat: 13, Fiber: 0,
	},
	"egg": {
		Name: "Egg", ServingSize: 50,
		Calories: 78, Protein: 6.3, Carbs: 0.6, Fat: 5.3, Fiber: 0,
	},
	"banana": {
		Name: "Banana", ServingSize: 100,
		Calories: 89, Protein: 1.1, Carbs: 23, Fat: 0.3, Fiber: 2.6,
	},
	"oatmeal": {
		Name: "Oatmeal", ServingSize: 100,
		Calories: 68, Protein: 2.4, Carbs: 12, Fat: 1.4, Fiber: 1.7,
	},
	"milk": {
		Name: "Milk (2%)", ServingSize: 244,
		Calories: 122, Protein: 8.1, Carbs: 12, Fat: 4.8, Fiber: 0,
	},
	"almonds": {
		Name: "Almonds", ServingSize: 28,
		Calories: 164, Protein: 6, Carbs: 6, Fat: 14, Fiber: 3.5,
	},
	"apple": {
		Name: "Apple", ServingSize: 182,
		Calories: 95, Protein: 0.5, Carbs: 25, Fat: 0.3, Fiber: 4.4,
	},
	"beef": {
		Name: "Ground Beef (80/20)", ServingSize: 100,
		Calories: 254, Protein: 17, Carbs: 0, Fat: 20, Fiber: 0,
	},
	"tuna": {
		Name: "Tuna (canned)", ServingSize: 100,
		Calories: 116, Protein: 26, Carbs: 0, Fat: 0.8, Fiber: 0,
	},
	"sweet_potato": {
		Name: "Sweet Potato", ServingSize: 100,
		Calories: 86, Protein: 1.6, Carbs: 20, Fat: 0.1, Fiber: 3,
	},
	"spinach": {
		Name: "Spinach", ServingSize: 100,
		Calories: 23, Protein: 2.9, Carbs: 3.6, Fat: 0.4, Fiber: 2.2,
	},
	"greek_yogurt": {
		Name: "Greek Yogurt", ServingSize: 170,
		Calories: 100, Protein: 17, Carbs: 6, Fat: 0.7, Fiber: 0,
	},
}

// GetFood returns a food from the database
func GetFood(name string) (Food, bool) {
	food, ok := CommonFoods[name]
	return food, ok
}

// AddFood adds a custom food to the database
func AddFood(name string, f Food) {
	CommonFoods[name] = f
}

// CalculateCaloriesFromMacro calculates calories from macronutrients
func CalculateCaloriesFromMacro(protein, carbs, fat float64) float64 {
	return protein*4 + carbs*4 + fat*9
}

// CalculateMacroFromCalories calculates macro grams from calorie percentages
func CalculateMacroFromCalories(calories float64, proteinPct, carbPct, fatPct float64) (protein, carbs, fat float64) {
	protein = (calories * proteinPct / 100) / 4
	carbs = (calories * carbPct / 100) / 4
	fat = (calories * fatPct / 100) / 9
	return
}

// BMIForWeight calculates what BMI a weight would be at given height
func BMIForWeight(weight, height float64) float64 {
	heightM := height / 100
	return weight / (heightM * heightM)
}

// WeightForBMI calculates what weight would achieve a target BMI
func WeightForBMI(targetBMI, height float64) float64 {
	heightM := height / 100
	return targetBMI * heightM * heightM
}

// LeanBodyMass calculates lean body mass using Boer formula
func LeanBodyMass(weight, height float64, gender Gender) float64 {
	heightM := height / 100

	if gender == Male {
		return 0.407*weight + 0.267*heightM*100 - 19.2
	}
	return 0.252*weight + 0.473*heightM*100 - 48.3
}

// BodyFatFromBMI estimates body fat percentage from BMI (Deurenberg formula)
func BodyFatFromBMI(bmi float64, age int, gender Gender) float64 {
	if gender == Male {
		return (1.20 * bmi) + (0.23 * float64(age)) - 16.2
	}
	return (1.20 * bmi) + (0.23 * float64(age)) - 5.4
}

// AdjustCaloriesForActivity adjusts base calories for activity
func AdjustCaloriesForActivity(baseCalories float64, activity ActivityLevel) float64 {
	multiplier, ok := activityMultipliers[activity]
	if !ok {
		multiplier = 1.2
	}
	return baseCalories * multiplier
}

// DailyCalorieRange returns min and max calorie recommendations
func DailyCalorieRange(result *NutritionResult) (min, max float64) {
	min = result.TDEE * 0.8  // Minimum safe intake
	max = result.TDEE * 1.2  // Maximum for weight gain
	return min, max
}

// IsHealthyBMI checks if BMI is in healthy range
func IsHealthyBMI(bmi float64) bool {
	return bmi >= 18.5 && bmi < 25
}

// WeightChangeRate calculates weekly weight change rate
func WeightChangeRate(currentCalories, tdee float64) float64 {
	// Daily deficit/surplus in calories
	diff := currentCalories - tdee
	// Weekly change: 7700 cal = 1kg
	weeklyChange := (diff * 7) / 7700
	return math.Round(weeklyChange*100) / 100
}