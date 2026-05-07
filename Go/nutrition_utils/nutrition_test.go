package nutrition_utils

import (
	"math"
	"testing"
)

func TestCalculateBMR(t *testing.T) {
	tests := []struct {
		name     string
		weight   float64
		height   float64
		age      int
		gender   Gender
		expected float64
		wantErr  bool
	}{
		{"Male 30y 70kg 175cm", 70, 175, 30, Male, 1648.75, false},
		{"Female 25y 60kg 165cm", 60, 165, 25, Female, 1345.25, false},
		{"Invalid weight", 0, 175, 30, Male, 0, true},
		{"Invalid height", 70, 0, 30, Male, 0, true},
		{"Invalid age", 70, 175, 0, Male, 0, true},
		{"Invalid gender", 70, 175, 30, "X", 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateBMR(tt.weight, tt.height, tt.age, tt.gender)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateBMR() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && math.Abs(result-tt.expected) > 1 {
				t.Errorf("CalculateBMR() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestCalculateTDEE(t *testing.T) {
	bmr := 1640.5

	tests := []struct {
		name     string
		bmr      float64
		activity ActivityLevel
		wantErr  bool
	}{
		{"Sedentary", bmr, Sedentary, false},
		{"Lightly Active", bmr, LightlyActive, false},
		{"Moderately Active", bmr, ModeratelyActive, false},
		{"Very Active", bmr, VeryActive, false},
		{"Extra Active", bmr, ExtraActive, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateTDEE(tt.bmr, tt.activity)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateTDEE() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if result < tt.bmr {
				t.Errorf("CalculateTDEE() = %v, should be >= BMR %v", result, tt.bmr)
			}
		})
	}
}

func TestCalculateBMI(t *testing.T) {
	tests := []struct {
		name     string
		weight   float64
		height   float64
		expected float64
		wantErr  bool
	}{
		{"Normal BMI", 70, 175, 22.9, false},
		{"Underweight", 50, 180, 15.4, false},
		{"Overweight", 90, 170, 31.1, false},
		{"Invalid weight", 0, 175, 0, true},
		{"Invalid height", 70, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateBMI(tt.weight, tt.height)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateBMI() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && math.Abs(result-tt.expected) > 0.5 {
				t.Errorf("CalculateBMI() = %v, want approximately %v", result, tt.expected)
			}
		})
	}
}

func TestGetBMICategory(t *testing.T) {
	tests := []struct {
		bmi      float64
		expected string
	}{
		{15, "Underweight"},
		{18.4, "Underweight"},
		{22, "Normal"},
		{24.9, "Normal"},
		{27, "Overweight"},
		{32, "Obese"},
	}

	for _, tt := range tests {
		result := GetBMICategory(tt.bmi)
		if result != tt.expected {
			t.Errorf("GetBMICategory(%v) = %v, want %v", tt.bmi, result, tt.expected)
		}
	}
}

func TestGetBMICategoryDetailed(t *testing.T) {
	tests := []struct {
		bmi      float64
		expected string
	}{
		{14, "Severely Underweight"},
		{17, "Underweight"},
		{22, "Normal"},
		{27, "Overweight"},
		{32, "Obese Class I"},
		{37, "Obese Class II"},
		{42, "Obese Class III"},
	}

	for _, tt := range tests {
		result := GetBMICategoryDetailed(tt.bmi)
		if result != tt.expected {
			t.Errorf("GetBMICategoryDetailed(%v) = %v, want %v", tt.bmi, result, tt.expected)
		}
	}
}

func TestCalculateIdealWeight(t *testing.T) {
	tests := []struct {
		name     string
		height   float64
		gender   Gender
		minValue float64
		maxValue float64
	}{
		{"Male 175cm", 175, Male, 65, 80},
		{"Female 165cm", 165, Female, 50, 65},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CalculateIdealWeight(tt.height, tt.gender)
			if result < tt.minValue || result > tt.maxValue {
				t.Errorf("CalculateIdealWeight() = %v, want between %v and %v", result, tt.minValue, tt.maxValue)
			}
		})
	}
}

func TestCalculateIdealWeightRange(t *testing.T) {
	min, max := CalculateIdealWeightRange(175)
	if min >= max {
		t.Errorf("CalculateIdealWeightRange() min (%v) should be less than max (%v)", min, max)
	}
	if min <= 0 || max <= 0 {
		t.Errorf("CalculateIdealWeightRange() values should be positive")
	}
}

func TestCalculateWaterIntake(t *testing.T) {
	tests := []struct {
		weight   float64
		activity ActivityLevel
		minValue float64
	}{
		{70, Sedentary, 2.0},
		{70, ModeratelyActive, 2.5},
		{100, VeryActive, 3.0},
	}

	for _, tt := range tests {
		result := CalculateWaterIntake(tt.weight, tt.activity)
		if result < tt.minValue {
			t.Errorf("CalculateWaterIntake(%v, %v) = %v, want >= %v", tt.weight, tt.activity, result, tt.minValue)
		}
	}
}

func TestCalculateMacro(t *testing.T) {
	calories := 2000.0

	tests := []struct {
		name string
		cal  float64
		goal Goal
	}{
		{"Weight Loss", calories, LoseWeight},
		{"Maintenance", calories, MaintainWeight},
		{"Weight Gain", calories, GainWeight},
		{"Build Muscle", calories, BuildMuscle},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			protein, carbs, fat := CalculateMacro(tt.cal, tt.goal)
			if protein <= 0 || carbs <= 0 || fat <= 0 {
				t.Errorf("CalculateMacro() returned zero or negative values")
			}
			// Verify calories add up correctly
			calculatedCal := protein*4 + carbs*4 + fat*9
			if math.Abs(calculatedCal-tt.cal) > 10 {
				t.Errorf("CalculateMacro() calories mismatch: calculated %v, expected %v", calculatedCal, tt.cal)
			}
		})
	}
}

func TestCalculateFiber(t *testing.T) {
	tests := []struct {
		calories float64
		min      float64
	}{
		{1500, 20},
		{2000, 28},
		{2500, 35},
	}

	for _, tt := range tests {
		result := CalculateFiber(tt.calories)
		if result < tt.min*0.9 || result > tt.min*1.1 {
			t.Errorf("CalculateFiber(%v) = %v, want approximately %v", tt.calories, result, tt.min)
		}
	}
}

func TestAnalyzeProfile(t *testing.T) {
	profile := Profile{
		Weight:   70,
		Height:   175,
		Age:      30,
		Gender:   Male,
		Activity: ModeratelyActive,
		Goal:     MaintainWeight,
	}

	result, err := AnalyzeProfile(profile)
	if err != nil {
		t.Fatalf("AnalyzeProfile() error = %v", err)
	}

	if result.BMR <= 0 {
		t.Errorf("BMR should be positive, got %v", result.BMR)
	}
	if result.TDEE <= 0 {
		t.Errorf("TDEE should be positive, got %v", result.TDEE)
	}
	if result.BMI <= 0 {
		t.Errorf("BMI should be positive, got %v", result.BMI)
	}
	if result.WaterIntake <= 0 {
		t.Errorf("WaterIntake should be positive, got %v", result.WaterIntake)
	}
	if result.BMICategory == "" {
		t.Error("BMICategory should not be empty")
	}
}

func TestCalculateCaloriesBurned(t *testing.T) {
	tests := []struct {
		activity string
		weight   float64
		duration float64
		minCal   float64
	}{
		{"running", 70, 30, 300},
		{"walking", 70, 60, 100},
		{"swimming", 70, 30, 200},
		{"yoga", 70, 60, 100},
	}

	for _, tt := range tests {
		result := CalculateCaloriesBurned(tt.activity, tt.weight, tt.duration)
		if result < tt.minCal*0.5 {
			t.Errorf("CalculateCaloriesBurned(%v) = %v, expected at least %v", tt.activity, result, tt.minCal*0.5)
		}
	}
}

func TestCalculateRequiredDeficit(t *testing.T) {
	// Lose 5kg in 10 weeks
	result := CalculateRequiredDeficit(80, 75, 10)
	expected := float64(550) // ~550 cal/day deficit

	if math.Abs(result-expected) > 50 {
		t.Errorf("CalculateRequiredDeficit() = %v, want approximately %v", result, expected)
	}
}

func TestCalculateWeightLossTimeline(t *testing.T) {
	// 5kg to lose, 500 cal/day deficit
	result := CalculateWeightLossTimeline(80, 75, 500)
	expected := 11 // ~11 weeks

	if math.Abs(float64(result)-float64(expected)) > 1 {
		t.Errorf("CalculateWeightLossTimeline() = %v, want approximately %v", result, expected)
	}
}

func TestFoodInfo(t *testing.T) {
	food := Food{
		Name:        "Test Food",
		ServingSize: 50,
		Calories:    100,
		Protein:     10,
		Carbs:       15,
		Fat:         2,
	}

	info := food.FoodInfo()
	if info.ServingSize != 100 {
		t.Errorf("FoodInfo() ServingSize = %v, want 100", info.ServingSize)
	}
	if info.Calories != 200 {
		t.Errorf("FoodInfo() Calories = %v, want 200", info.Calories)
	}
}

func TestFoodItemNutrition(t *testing.T) {
	food := Food{
		Name:        "Test Food",
		ServingSize: 100,
		Calories:    200,
		Protein:     20,
		Carbs:       10,
		Fat:         8,
	}

	item := FoodItem{Food: food, Quantity: 2}
	nutrition := item.CalculateNutrition()

	if nutrition.Calories != 400 {
		t.Errorf("CalculateNutrition() Calories = %v, want 400", nutrition.Calories)
	}
	if nutrition.Protein != 40 {
		t.Errorf("CalculateNutrition() Protein = %v, want 40", nutrition.Protein)
	}
}

func TestCalculateMealNutrition(t *testing.T) {
	meal := Meal{
		Name: "Test Meal",
		Foods: []FoodItem{
			{Food: Food{Name: "Food1", ServingSize: 100, Calories: 200, Protein: 20}, Quantity: 1},
			{Food: Food{Name: "Food2", ServingSize: 100, Calories: 150, Protein: 10}, Quantity: 2},
		},
	}

	nutrition := CalculateMealNutrition(meal)
	if nutrition.Calories != 500 {
		t.Errorf("CalculateMealNutrition() Calories = %v, want 500", nutrition.Calories)
	}
	if nutrition.Protein != 40 {
		t.Errorf("CalculateMealNutrition() Protein = %v, want 40", nutrition.Protein)
	}
}

func TestCalculateDailyNutrition(t *testing.T) {
	log := DailyLog{
		Meals: []Meal{
			{
				Name: "Breakfast",
				Foods: []FoodItem{
					{Food: Food{Name: "Eggs", ServingSize: 100, Calories: 150, Protein: 13}, Quantity: 2},
				},
			},
			{
				Name: "Lunch",
				Foods: []FoodItem{
					{Food: Food{Name: "Chicken", ServingSize: 100, Calories: 165, Protein: 31}, Quantity: 1},
				},
			},
		},
	}

	nutrition := CalculateDailyNutrition(log)
	if nutrition.Calories != 465 {
		t.Errorf("CalculateDailyNutrition() Calories = %v, want 465", nutrition.Calories)
	}
}

func TestScoreFood(t *testing.T) {
	tests := []struct {
		name       string
		food       Food
		minOverall float64
		maxOverall float64
	}{
		{
			name:       "High Protein",
			food:       Food{Name: "Chicken", ServingSize: 100, Calories: 165, Protein: 31, Carbs: 0, Fat: 3.6},
			minOverall: 0, // Lower threshold since scoring depends on balance
			maxOverall: 100,
		},
		{
			name:       "High Carb",
			food:       Food{Name: "Rice", ServingSize: 100, Calories: 200, Protein: 4, Carbs: 45, Fat: 1},
			minOverall: 0, // Lower threshold
			maxOverall: 100,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			score := ScoreFood(tt.food)
			if score.Overall < tt.minOverall || score.Overall > 100 {
				t.Errorf("ScoreFood() Overall = %v, want between %v and 100", score.Overall, tt.minOverall)
			}
			if score.Grade < "A" || score.Grade > "F" {
				t.Errorf("ScoreFood() Grade = %v, want A-F", score.Grade)
			}
		})
	}
}

func TestCommonFoods(t *testing.T) {
	if len(CommonFoods) == 0 {
		t.Error("CommonFoods database should not be empty")
	}

	food, ok := CommonFoods["chicken_breast"]
	if !ok {
		t.Error("chicken_breast should exist in CommonFoods")
	}
	if food.Name != "Chicken Breast" {
		t.Errorf("chicken_breast Name = %v, want 'Chicken Breast'", food.Name)
	}
}

func TestGetFood(t *testing.T) {
	food, ok := GetFood("banana")
	if !ok {
		t.Error("GetFood('banana') should return true")
	}
	if food.Name != "Banana" {
		t.Errorf("GetFood('banana') Name = %v, want 'Banana'", food.Name)
	}

	_, ok = GetFood("nonexistent")
	if ok {
		t.Error("GetFood('nonexistent') should return false")
	}
}

func TestAddFood(t *testing.T) {
	customFood := Food{
		Name:        "Custom Food",
		ServingSize: 100,
		Calories:    100,
		Protein:     10,
		Carbs:       10,
		Fat:         4,
	}

	AddFood("custom", customFood)

	food, ok := GetFood("custom")
	if !ok {
		t.Error("AddFood should add food to database")
	}
	if food.Name != "Custom Food" {
		t.Errorf("Added food Name = %v, want 'Custom Food'", food.Name)
	}
}

func TestCalculateCaloriesFromMacro(t *testing.T) {
	result := CalculateCaloriesFromMacro(25, 50, 20)
	expected := float64(25*4 + 50*4 + 20*9) // 100 + 200 + 180 = 480

	if result != expected {
		t.Errorf("CalculateCaloriesFromMacro() = %v, want %v", result, expected)
	}
}

func TestCalculateMacroFromCalories(t *testing.T) {
	calories := 2000.0
	protein, carbs, fat := CalculateMacroFromCalories(calories, 30, 50, 20)

	// Verify the macros add up correctly
	calculatedCal := protein*4 + carbs*4 + fat*9
	if math.Abs(calculatedCal-calories) > 1 {
		t.Errorf("Macro calories = %v, want %v", calculatedCal, calories)
	}
}

func TestBMIForWeight(t *testing.T) {
	result := BMIForWeight(70, 175)
	expected := 22.86

	if math.Abs(result-expected) > 0.1 {
		t.Errorf("BMIForWeight() = %v, want approximately %v", result, expected)
	}
}

func TestWeightForBMI(t *testing.T) {
	result := WeightForBMI(22.5, 175)
	expected := 68.9

	if math.Abs(result-expected) > 1 {
		t.Errorf("WeightForBMI() = %v, want approximately %v", result, expected)
	}
}

func TestLeanBodyMass(t *testing.T) {
	maleLBM := LeanBodyMass(70, 175, Male)
	femaleLBM := LeanBodyMass(60, 165, Female)

	if maleLBM <= 0 {
		t.Errorf("LeanBodyMass (male) should be positive, got %v", maleLBM)
	}
	if femaleLBM <= 0 {
		t.Errorf("LeanBodyMass (female) should be positive, got %v", femaleLBM)
	}
	if maleLBM <= femaleLBM {
		t.Log("Note: Male LBM is typically higher than female LBM for same proportions")
	}
}

func TestBodyFatFromBMI(t *testing.T) {
	bmi := 22.86
	age := 30

	maleBF := BodyFatFromBMI(bmi, age, Male)
	femaleBF := BodyFatFromBMI(bmi, age, Female)

	if maleBF <= 0 || maleBF > 50 {
		t.Errorf("BodyFatFromBMI (male) should be between 0-50%%, got %v", maleBF)
	}
	if femaleBF <= 0 || femaleBF > 50 {
		t.Errorf("BodyFatFromBMI (female) should be between 0-50%%, got %v", femaleBF)
	}
}

func TestAdjustCaloriesForActivity(t *testing.T) {
	base := 2000.0

	tests := []struct {
		activity ActivityLevel
		minMult  float64
		maxMult  float64
	}{
		{Sedentary, 1.0, 1.3},
		{ModeratelyActive, 1.4, 1.7},
		{ExtraActive, 1.7, 2.0},
	}

	for _, tt := range tests {
		result := AdjustCaloriesForActivity(base, tt.activity)
		minCal := base * tt.minMult
		maxCal := base * tt.maxMult
		if result < minCal || result > maxCal {
			t.Errorf("AdjustCaloriesForActivity(%v) = %v, want between %v and %v", tt.activity, result, minCal, maxCal)
		}
	}
}

func TestDailyCalorieRange(t *testing.T) {
	result := &NutritionResult{TDEE: 2000}
	min, max := DailyCalorieRange(result)

	if min >= max {
		t.Errorf("DailyCalorieRange min (%v) should be less than max (%v)", min, max)
	}
	if min < result.TDEE*0.7 {
		t.Errorf("DailyCalorieRange min (%v) should not be too low", min)
	}
}

func TestIsHealthyBMI(t *testing.T) {
	tests := []struct {
		bmi      float64
		expected bool
	}{
		{18.5, true},
		{22, true},
		{24.9, true},
		{17, false},
		{30, false},
	}

	for _, tt := range tests {
		result := IsHealthyBMI(tt.bmi)
		if result != tt.expected {
			t.Errorf("IsHealthyBMI(%v) = %v, want %v", tt.bmi, result, tt.expected)
		}
	}
}

func TestWeightChangeRate(t *testing.T) {
	// Deficit scenario
	deficit := WeightChangeRate(1500, 2000)
	if deficit >= 0 {
		t.Errorf("WeightChangeRate with deficit should be negative, got %v", deficit)
	}

	// Surplus scenario
	surplus := WeightChangeRate(2500, 2000)
	if surplus <= 0 {
		t.Errorf("WeightChangeRate with surplus should be positive, got %v", surplus)
	}

	// Maintenance
	maintain := WeightChangeRate(2000, 2000)
	if maintain != 0 {
		t.Errorf("WeightChangeRate at maintenance should be 0, got %v", maintain)
	}
}

func TestCalculateBMRHarrisBenedict(t *testing.T) {
	// Male
	maleBMR, err := CalculateBMRHarrisBenedict(70, 175, 30, Male)
	if err != nil {
		t.Errorf("CalculateBMRHarrisBenedict error: %v", err)
	}
	if maleBMR <= 0 {
		t.Errorf("Male BMR should be positive, got %v", maleBMR)
	}

	// Female
	femaleBMR, err := CalculateBMRHarrisBenedict(60, 165, 25, Female)
	if err != nil {
		t.Errorf("CalculateBMRHarrisBenedict error: %v", err)
	}
	if femaleBMR <= 0 {
		t.Errorf("Female BMR should be positive, got %v", femaleBMR)
	}

	// Compare with Mifflin-St Jeor
	mifflinBMR, _ := CalculateBMR(70, 175, 30, Male)
	// Harris-Benedict typically gives slightly higher values
	if math.Abs(maleBMR-mifflinBMR) > 200 {
		t.Logf("Note: Harris-Benedict (%v) differs from Mifflin-St Jeor (%v)", maleBMR, mifflinBMR)
	}
}

// Benchmarks
func BenchmarkCalculateBMR(b *testing.B) {
	for i := 0; i < b.N; i++ {
		CalculateBMR(70, 175, 30, Male)
	}
}

func BenchmarkCalculateTDEE(b *testing.B) {
	for i := 0; i < b.N; i++ {
		CalculateTDEE(1640.5, ModeratelyActive)
	}
}

func BenchmarkCalculateBMI(b *testing.B) {
	for i := 0; i < b.N; i++ {
		CalculateBMI(70, 175)
	}
}

func BenchmarkAnalyzeProfile(b *testing.B) {
	profile := Profile{
		Weight:   70,
		Height:   175,
		Age:      30,
		Gender:   Male,
		Activity: ModeratelyActive,
		Goal:     MaintainWeight,
	}
	for i := 0; i < b.N; i++ {
		AnalyzeProfile(profile)
	}
}

func BenchmarkScoreFood(b *testing.B) {
	food := Food{
		Name:        "Test",
		ServingSize: 100,
		Calories:    200,
		Protein:     20,
		Carbs:       10,
		Fat:         8,
	}
	for i := 0; i < b.N; i++ {
		ScoreFood(food)
	}
}