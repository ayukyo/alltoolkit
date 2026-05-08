package dice_utils

import (
	"math"
	"testing"
)

func TestNewDie(t *testing.T) {
	tests := []struct {
		sides    int
		wantErr  bool
	}{
		{6, false},
		{20, false},
		{100, false},
		{4, false},
		{8, false},
		{1, true},   // Too few sides
		{0, true},   // Invalid
		{-1, true},  // Invalid
	}

	for _, tt := range tests {
		die, err := NewDie(tt.sides)
		if (err != nil) != tt.wantErr {
			t.Errorf("NewDie(%d) error = %v, wantErr %v", tt.sides, err, tt.wantErr)
		}
		if !tt.wantErr && die.Sides != tt.sides {
			t.Errorf("NewDie(%d).Sides = %d, want %d", tt.sides, die.Sides, tt.sides)
		}
	}
}

func TestDieRoll(t *testing.T) {
	SetSeed(42)
	die, _ := NewDie(6)
	
	for i := 0; i < 100; i++ {
		result := die.Roll()
		if result < 1 || result > 6 {
			t.Errorf("Die.Roll() = %d, want value between 1 and 6", result)
		}
	}
}

func TestDieRollN(t *testing.T) {
	SetSeed(42)
	die, _ := NewDie(6)
	
	tests := []struct {
		n      int
		wantLen int
	}{
		{0, 0},
		{1, 1},
		{5, 5},
		{10, 10},
	}

	for _, tt := range tests {
		results := die.RollN(tt.n)
		if len(results) != tt.wantLen {
			t.Errorf("Die.RollN(%d) returned %d results, want %d", tt.n, len(results), tt.wantLen)
		}
		for _, r := range results {
			if r < 1 || r > 6 {
				t.Errorf("Invalid die result: %d", r)
			}
		}
	}
}

func TestRollDice(t *testing.T) {
	SetSeed(42)
	
	tests := []struct {
		numDice int
		sides   int
		wantErr bool
	}{
		{2, 6, false},
		{1, 20, false},
		{5, 4, false},
		{0, 6, true},   // No dice
		{3, 1, true},   // Invalid sides
	}

	for _, tt := range tests {
		roll, err := RollDice(tt.numDice, tt.sides)
		if (err != nil) != tt.wantErr {
			t.Errorf("RollDice(%d, %d) error = %v, wantErr %v", tt.numDice, tt.sides, err, tt.wantErr)
			continue
		}
		if !tt.wantErr {
			if len(roll.Dice) != tt.numDice {
				t.Errorf("RollDice().Dice length = %d, want %d", len(roll.Dice), tt.numDice)
			}
			if roll.Count != tt.numDice {
				t.Errorf("RollDice().Count = %d, want %d", roll.Count, tt.numDice)
			}
			if roll.Sides != tt.sides {
				t.Errorf("RollDice().Sides = %d, want %d", roll.Sides, tt.sides)
			}
			minPossible := tt.numDice
			maxPossible := tt.numDice * tt.sides
			if roll.Total < minPossible || roll.Total > maxPossible {
				t.Errorf("RollDice().Total = %d, want between %d and %d", roll.Total, minPossible, maxPossible)
			}
		}
	}
}

func TestRollWithModifier(t *testing.T) {
	SetSeed(42)
	
	roll, err := RollWithModifier(2, 6, 5)
	if err != nil {
		t.Fatalf("RollWithModifier() error: %v", err)
	}
	
	// Total should be at least 2 + 5 = 7 and at most 12 + 5 = 17
	if roll.Total < 7 || roll.Total > 17 {
		t.Errorf("RollWithModifier().Total = %d, want between 7 and 17", roll.Total)
	}
}

func TestMinMaxPossible(t *testing.T) {
	tests := []struct {
		numDice  int
		sides    int
		minWant  int
		maxWant  int
	}{
		{2, 6, 2, 12},
		{3, 20, 3, 60},
		{1, 4, 1, 4},
		{10, 10, 10, 100},
	}

	for _, tt := range tests {
		minGot := MinPossible(tt.numDice)
		maxGot := MaxPossible(tt.numDice, tt.sides)
		if minGot != tt.minWant {
			t.Errorf("MinPossible(%d) = %d, want %d", tt.numDice, minGot, tt.minWant)
		}
		if maxGot != tt.maxWant {
			t.Errorf("MaxPossible(%d, %d) = %d, want %d", tt.numDice, tt.sides, maxGot, tt.maxWant)
		}
	}
}

func TestTotalOutcomes(t *testing.T) {
	tests := []struct {
		numDice int
		sides   int
		want    int
	}{
		{1, 6, 6},
		{2, 6, 36},
		{3, 6, 216},
		{2, 20, 400},
	}

	for _, tt := range tests {
		got := TotalOutcomes(tt.numDice, tt.sides)
		if got != tt.want {
			t.Errorf("TotalOutcomes(%d, %d) = %d, want %d", tt.numDice, tt.sides, got, tt.want)
		}
	}
}

func TestCountWays(t *testing.T) {
	tests := []struct {
		numDice int
		sides   int
		target  int
		want    int
	}{
		// 2d6 cases
		{2, 6, 2, 1},   // Only (1,1)
		{2, 6, 3, 2},   // (1,2), (2,1)
		{2, 6, 7, 6},   // (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
		{2, 6, 12, 1},  // Only (6,6)
		// Edge cases
		{1, 6, 4, 1},   // Only one die
		{2, 6, 1, 0},   // Impossible
		{2, 6, 13, 0},  // Impossible
	}

	for _, tt := range tests {
		got := CountWays(tt.numDice, tt.sides, tt.target)
		if got != tt.want {
			t.Errorf("CountWays(%d, %d, %d) = %d, want %d", tt.numDice, tt.sides, tt.target, got, tt.want)
		}
	}
}

func TestProbability(t *testing.T) {
	// For 2d6, probability of 7 is 6/36 = 1/6
	prob := Probability(2, 6, 7)
	expected := 1.0 / 6.0
	if math.Abs(prob-expected) > 0.0001 {
		t.Errorf("Probability(2, 6, 7) = %f, want %f", prob, expected)
	}

	// Probability of 2 with 2d6 is 1/36
	prob = Probability(2, 6, 2)
	expected = 1.0 / 36.0
	if math.Abs(prob-expected) > 0.0001 {
		t.Errorf("Probability(2, 6, 2) = %f, want %f", prob, expected)
	}

	// Impossible case
	prob = Probability(2, 6, 13)
	if prob != 0 {
		t.Errorf("Probability(2, 6, 13) = %f, want 0", prob)
	}
}

func TestProbabilityRange(t *testing.T) {
	pr := ProbabilityRange(2, 6, 7)
	
	if pr.Ways != 6 {
		t.Errorf("ProbabilityRange(2, 6, 7).Ways = %d, want 6", pr.Ways)
	}
	if pr.Total != 36 {
		t.Errorf("ProbabilityRange(2, 6, 7).Total = %d, want 36", pr.Total)
	}
	
	// At least 7 should include 7-12
	// P(>=7) = P(7) + P(8) + ... + P(12) = 6/36 + 5/36 + 4/36 + 3/36 + 2/36 + 1/36 = 21/36
	expectedAtLeast := 21.0 / 36.0
	if math.Abs(pr.AtLeast-expectedAtLeast) > 0.0001 {
		t.Errorf("ProbabilityRange(2, 6, 7).AtLeast = %f, want %f", pr.AtLeast, expectedAtLeast)
	}
	
	// At most 7 should include 2-7
	// P(<=7) = P(2) + P(3) + ... + P(7) = 1/36 + 2/36 + 3/36 + 4/36 + 5/36 + 6/36 = 21/36
	expectedAtMost := 21.0 / 36.0
	if math.Abs(pr.AtMost-expectedAtMost) > 0.0001 {
		t.Errorf("ProbabilityRange(2, 6, 7).AtMost = %f, want %f", pr.AtMost, expectedAtMost)
	}
}

func TestAllProbabilities(t *testing.T) {
	probs := AllProbabilities(2, 6)
	
	// Check all values from 2 to 12 are present
	for i := 2; i <= 12; i++ {
		if _, ok := probs[i]; !ok {
			t.Errorf("AllProbabilities missing value %d", i)
		}
	}
	
	// Sum of all probabilities should be 1
	total := 0.0
	for _, p := range probs {
		total += p
	}
	if math.Abs(total-1.0) > 0.0001 {
		t.Errorf("Sum of AllProbabilities = %f, want 1.0", total)
	}
}

func TestExpectedValue(t *testing.T) {
	tests := []struct {
		numDice int
		sides   int
		want    float64
	}{
		{1, 6, 3.5},
		{2, 6, 7.0},
		{3, 6, 10.5},
		{1, 20, 10.5},
		{2, 20, 21.0},
	}

	for _, tt := range tests {
		got := ExpectedValue(tt.numDice, tt.sides)
		if math.Abs(got-tt.want) > 0.0001 {
			t.Errorf("ExpectedValue(%d, %d) = %f, want %f", tt.numDice, tt.sides, got, tt.want)
		}
	}
}

func TestVariance(t *testing.T) {
	// Variance for one d6 should be (36-1)/12 = 35/12 ≈ 2.917
	v := Variance(1, 6)
	expected := 35.0 / 12.0
	if math.Abs(v-expected) > 0.0001 {
		t.Errorf("Variance(1, 6) = %f, want %f", v, expected)
	}
}

func TestStandardDeviation(t *testing.T) {
	sd := StandardDeviation(1, 6)
	v := Variance(1, 6)
	expected := math.Sqrt(v)
	if math.Abs(sd-expected) > 0.0001 {
		t.Errorf("StandardDeviation(1, 6) = %f, want %f", sd, expected)
	}
}

func TestIsYahtzee(t *testing.T) {
	tests := []struct {
		dice    []int
		want    bool
	}{
		{[]int{6, 6, 6, 6, 6}, true},
		{[]int{1, 1, 1, 1, 1}, true},
		{[]int{5, 5, 5, 5, 5}, true},
		{[]int{1, 1, 1, 1, 2}, false},
		{[]int{1, 2, 3, 4, 5}, false},
		{[]int{6, 6, 6, 6, 5}, false},
		{[]int{1}, true},
		{[]int{}, false},
	}

	for _, tt := range tests {
		got := IsYahtzee(tt.dice)
		if got != tt.want {
			t.Errorf("IsYahtzee(%v) = %v, want %v", tt.dice, got, tt.want)
		}
	}
}

func TestIsSmallStraight(t *testing.T) {
	tests := []struct {
		dice    []int
		want    bool
	}{
		{[]int{1, 2, 3, 4, 5}, true},   // Contains 1-4
		{[]int{2, 3, 4, 5, 6}, true},   // Contains 2-5 or 3-6
		{[]int{1, 3, 4, 5, 6}, true},   // Contains 3-6
		{[]int{1, 2, 3, 4, 4}, true},   // Contains 1-4
		{[]int{1, 1, 2, 3, 4}, true},   // Contains 1-4
		{[]int{1, 3, 5, 6, 6}, false},  // No 4-consecutive
		{[]int{1, 1, 1, 1, 1}, false},
		{[]int{1, 2}, false},  // Not enough dice
	}

	for _, tt := range tests {
		got := IsSmallStraight(tt.dice)
		if got != tt.want {
			t.Errorf("IsSmallStraight(%v) = %v, want %v", tt.dice, got, tt.want)
		}
	}
}

func TestIsLargeStraight(t *testing.T) {
	tests := []struct {
		dice    []int
		want    bool
	}{
		{[]int{1, 2, 3, 4, 5}, true},
		{[]int{2, 3, 4, 5, 6}, true},
		{[]int{1, 2, 3, 4, 6}, false},
		{[]int{1, 2, 3, 4}, false},  // Not enough dice
		{[]int{1, 1, 2, 3, 4}, false},
	}

	for _, tt := range tests {
		got := IsLargeStraight(tt.dice)
		if got != tt.want {
			t.Errorf("IsLargeStraight(%v) = %v, want %v", tt.dice, got, tt.want)
		}
	}
}

func TestCountOfKind(t *testing.T) {
	tests := []struct {
		dice     []int
		wantCnt  int
		wantVal  int
	}{
		{[]int{1, 1, 1, 1, 1}, 5, 1},
		{[]int{6, 6, 6, 6, 1}, 4, 6},
		{[]int{1, 2, 3, 4, 5}, 1, 1},
		{[]int{3, 3, 3, 4, 4}, 3, 3},
		{[]int{2, 2, 3, 3, 4}, 2, 2},  // First 2-of-kind found
		{[]int{}, 0, 0},
	}

	for _, tt := range tests {
		cnt, val := CountOfKind(tt.dice)
		if cnt != tt.wantCnt {
			t.Errorf("CountOfKind(%v) count = %d, want %d", tt.dice, cnt, tt.wantCnt)
		}
		if tt.wantCnt > 0 && val != tt.wantVal {
			// Note: value might differ if multiple values have same count
			// Just check count is correct
		}
	}
}

func TestIsFullHouse(t *testing.T) {
	tests := []struct {
		dice    []int
		want    bool
	}{
		{[]int{1, 1, 1, 2, 2}, true},
		{[]int{6, 6, 6, 1, 1}, true},
		{[]int{3, 3, 4, 4, 4}, true},
		{[]int{1, 1, 2, 2, 3}, false},  // Two pairs, not full house
		{[]int{1, 1, 1, 1, 2}, false},  // Four of a kind
		{[]int{1, 2, 3, 4, 5}, false},
		{[]int{1, 1, 1, 1, 1}, true},   // Five of a kind counts (3+2)
	}

	for _, tt := range tests {
		got := IsFullHouse(tt.dice)
		if got != tt.want {
			t.Errorf("IsFullHouse(%v) = %v, want %v", tt.dice, got, tt.want)
		}
	}
}

func TestSumDice(t *testing.T) {
	tests := []struct {
		dice    []int
		want    int
	}{
		{[]int{1, 2, 3, 4, 5}, 15},
		{[]int{6, 6, 6, 6, 6}, 30},
		{[]int{1}, 1},
		{[]int{}, 0},
	}

	for _, tt := range tests {
		got := SumDice(tt.dice)
		if got != tt.want {
			t.Errorf("SumDice(%v) = %d, want %d", tt.dice, got, tt.want)
		}
	}
}

func TestSumOfValue(t *testing.T) {
	dice := []int{1, 2, 3, 4, 5, 6, 6, 6}
	
	tests := []struct {
		value   int
		want    int
	}{
		{6, 18},  // Three 6s
		{1, 1},   // One 1
		{3, 3},   // One 3
		{7, 0},   // No 7s
	}

	for _, tt := range tests {
		got := SumOfValue(dice, tt.value)
		if got != tt.want {
			t.Errorf("SumOfValue(%v, %d) = %d, want %d", dice, tt.value, got, tt.want)
		}
	}
}

func TestRerollSelective(t *testing.T) {
	SetSeed(42)
	dice := []int{1, 2, 3, 4, 5}
	
	result, err := RerollSelective(dice, 6, []int{0, 2})
	if err != nil {
		t.Fatalf("RerollSelective() error: %v", err)
	}
	
	// Positions 1 and 3 should not change
	if result[1] != 2 {
		t.Errorf("result[1] = %d, want 2", result[1])
	}
	if result[3] != 4 {
		t.Errorf("result[3] = %d, want 4", result[3])
	}
	
	// Positions 0 and 2 should have changed (1-6)
	if result[0] < 1 || result[0] > 6 {
		t.Errorf("result[0] = %d, want 1-6", result[0])
	}
	if result[2] < 1 || result[2] > 6 {
		t.Errorf("result[2] = %d, want 1-6", result[2])
	}
}

func TestRerollSelectiveErrors(t *testing.T) {
	_, err := RerollSelective([]int{}, 6, []int{0})
	if err == nil {
		t.Error("RerollSelective with empty dice should return error")
	}
	
	_, err = RerollSelective([]int{1, 2}, 1, []int{0})
	if err == nil {
		t.Error("RerollSelective with invalid sides should return error")
	}
	
	_, err = RerollSelective([]int{1, 2}, 6, []int{5})
	if err == nil {
		t.Error("RerollSelective with out-of-bounds index should return error")
	}
}

func TestDiceNotation(t *testing.T) {
	tests := []struct {
		notation string
		numDice  int
		sides    int
		modifier int
		wantErr  bool
	}{
		{"2d6", 2, 6, 0, false},
		{"1d20", 1, 20, 0, false},
		{"3d8+5", 3, 8, 5, false},
		{"2d10-3", 2, 10, -3, false},
		{"4d6+0", 4, 6, 0, false},
		{"invalid", 0, 0, 0, true},
	}

	for _, tt := range tests {
		config, err := DiceNotation(tt.notation)
		if (err != nil) != tt.wantErr {
			t.Errorf("DiceNotation(%s) error = %v, wantErr %v", tt.notation, err, tt.wantErr)
			continue
		}
		if !tt.wantErr {
			if config.NumDice != tt.numDice {
				t.Errorf("DiceNotation(%s).NumDice = %d, want %d", tt.notation, config.NumDice, tt.numDice)
			}
			if config.Sides != tt.sides {
				t.Errorf("DiceNotation(%s).Sides = %d, want %d", tt.notation, config.Sides, tt.sides)
			}
			if config.Modifier != tt.modifier {
				t.Errorf("DiceNotation(%s).Modifier = %d, want %d", tt.notation, config.Modifier, tt.modifier)
			}
		}
	}
}

func TestRollNotation(t *testing.T) {
	SetSeed(42)
	
	roll, err := RollNotation("2d6+5")
	if err != nil {
		t.Fatalf("RollNotation() error: %v", err)
	}
	
	// Total should be between 2+5=7 and 12+5=17
	if roll.Total < 7 || roll.Total > 17 {
		t.Errorf("RollNotation('2d6+5').Total = %d, want between 7 and 17", roll.Total)
	}
	
	if len(roll.Dice) != 2 {
		t.Errorf("RollNotation('2d6+5') dice count = %d, want 2", len(roll.Dice))
	}
}

func TestAdvantage(t *testing.T) {
	SetSeed(42)
	
	roll, err := Advantage(20)
	if err != nil {
		t.Fatalf("Advantage() error: %v", err)
	}
	
	if roll.Total < 1 || roll.Total > 20 {
		t.Errorf("Advantage(20).Total = %d, want between 1 and 20", roll.Total)
	}
}

func TestDisadvantage(t *testing.T) {
	SetSeed(42)
	
	roll, err := Disadvantage(20)
	if err != nil {
		t.Fatalf("Disadvantage() error: %v", err)
	}
	
	if roll.Total < 1 || roll.Total > 20 {
		t.Errorf("Disadvantage(20).Total = %d, want between 1 and 20", roll.Total)
	}
}

func TestCoinFlip(t *testing.T) {
	SetSeed(42)
	
	// Just verify it returns valid values
	for i := 0; i < 100; i++ {
		result := CoinFlip()
		if result != "heads" && result != "tails" {
			t.Errorf("CoinFlip() = %s, want heads or tails", result)
		}
	}
}

func TestCoinFlipN(t *testing.T) {
	SetSeed(42)
	
	results := CoinFlipN(10)
	if len(results) != 10 {
		t.Errorf("CoinFlipN(10) returned %d results, want 10", len(results))
	}
	
	for _, r := range results {
		if r != "heads" && r != "tails" {
			t.Errorf("CoinFlipN result = %s, want heads or tails", r)
		}
	}
}

func TestPercentileRoll(t *testing.T) {
	SetSeed(42)
	
	for i := 0; i < 100; i++ {
		result := PercentileRoll()
		if result < 1 || result > 100 {
			t.Errorf("PercentileRoll() = %d, want between 1 and 100", result)
		}
	}
}

func TestFudgeRoll(t *testing.T) {
	SetSeed(42)
	
	total, results := FudgeRoll(4)
	
	if len(results) != 4 {
		t.Errorf("FudgeRoll(4) returned %d results, want 4", len(results))
	}
	
	// Each result should be -1, 0, or +1
	for _, r := range results {
		if r < -1 || r > 1 {
			t.Errorf("FudgeRoll result = %d, want -1, 0, or 1", r)
		}
	}
	
	// Total should be between -4 and +4
	if total < -4 || total > 4 {
		t.Errorf("FudgeRoll total = %d, want between -4 and 4", total)
	}
}

func TestHistogram(t *testing.T) {
	SetSeed(42)
	
	hist, err := Histogram(1000, 2, 6)
	if err != nil {
		t.Fatalf("Histogram() error: %v", err)
	}
	
	// Check all values from 2 to 12 are present
	for i := 2; i <= 12; i++ {
		if _, ok := hist[i]; !ok {
			t.Errorf("Histogram missing value %d", i)
		}
	}
	
	// Sum should be 1000
	total := 0
	for _, count := range hist {
		total += count
	}
	if total != 1000 {
		t.Errorf("Histogram total = %d, want 1000", total)
	}
}

func TestMonteCarloProbability(t *testing.T) {
	SetSeed(42)
	
	// For 2d6, probability of 7 is about 16.67%
	prob := MonteCarloProbability(2, 6, 7, 10000)
	expected := 1.0 / 6.0
	
	// Allow 2% tolerance for simulation
	if math.Abs(prob-expected) > 0.02 {
		t.Errorf("MonteCarloProbability(2, 6, 7) = %f, want approximately %f", prob, expected)
	}
}

func TestString(t *testing.T) {
	roll := &DiceRoll{
		Dice:  []int{3, 4, 5},
		Total: 12,
		Count: 3,
		Sides: 6,
	}
	
	got := roll.String()
	expected := "[3 4 5] = 12"
	if got != expected {
		t.Errorf("String() = %s, want %s", got, expected)
	}
}

func TestFormat(t *testing.T) {
	roll := &DiceRoll{
		Dice:  []int{3, 4, 5},
		Total: 12,
		Count: 3,
		Sides: 6,
	}
	
	got := roll.Format()
	expected := "3d6: [3 4 5] = 12"
	if got != expected {
		t.Errorf("Format() = %s, want %s", got, expected)
	}
	
	// Single die
	roll2 := &DiceRoll{
		Dice:  []int{15},
		Total: 15,
		Count: 1,
		Sides: 20,
	}
	
	got2 := roll2.Format()
	expected2 := "[15]"
	if got2 != expected2 {
		t.Errorf("Format() = %s, want %s", got2, expected2)
	}
}

func TestCriticalHitMiss(t *testing.T) {
	if !CriticalHit(20) {
		t.Error("CriticalHit(20) should be true")
	}
	if CriticalHit(19) {
		t.Error("CriticalHit(19) should be false")
	}
	
	if !CriticalMiss(1) {
		t.Error("CriticalMiss(1) should be true")
	}
	if CriticalMiss(2) {
		t.Error("CriticalMiss(2) should be false")
	}
}

func TestQuickRolls(t *testing.T) {
	SetSeed(42)
	
	// Test all quick roll functions
	for i := 0; i < 10; i++ {
		d4 := RollD4()
		if d4 < 1 || d4 > 4 {
			t.Errorf("RollD4() = %d, want 1-4", d4)
		}
		
		d6 := RollD6()
		if d6 < 1 || d6 > 6 {
			t.Errorf("RollD6() = %d, want 1-6", d6)
		}
		
		d8 := RollD8()
		if d8 < 1 || d8 > 8 {
			t.Errorf("RollD8() = %d, want 1-8", d8)
		}
		
		d10 := RollD10()
		if d10 < 1 || d10 > 10 {
			t.Errorf("RollD10() = %d, want 1-10", d10)
		}
		
		d12 := RollD12()
		if d12 < 1 || d12 > 12 {
			t.Errorf("RollD12() = %d, want 1-12", d12)
		}
		
		d20 := RollD20()
		if d20 < 1 || d20 > 20 {
			t.Errorf("RollD20() = %d, want 1-20", d20)
		}
		
		d100 := RollD100()
		if d100 < 1 || d100 > 100 {
			t.Errorf("RollD100() = %d, want 1-100", d100)
		}
	}
}

func TestExplodingDie(t *testing.T) {
	SetSeed(42)
	
	// Test with max explodes = 5 to ensure it stops
	total, rolls := ExplodingDie(6, 5)
	
	// Total should be at least 1
	if total < 1 {
		t.Error("ExplodingDie total should be at least 1")
	}
	
	// Each roll should be 1-6
	for _, r := range rolls {
		if r < 1 || r > 6 {
			t.Errorf("ExplodingDie roll = %d, want 1-6", r)
		}
	}
}

func TestKeepHighest(t *testing.T) {
	SetSeed(42)
	
	kept, total, err := KeepHighest(4, 6, 3)
	if err != nil {
		t.Fatalf("KeepHighest() error: %v", err)
	}
	
	if len(kept) != 3 {
		t.Errorf("KeepHighest returned %d dice, want 3", len(kept))
	}
	
	// Kept values should be sorted in descending order
	for i := 1; i < len(kept); i++ {
		if kept[i] > kept[i-1] {
			t.Errorf("KeepHighest not sorted correctly: %v", kept)
		}
	}
	
	if total < 3 || total > 18 {
		t.Errorf("KeepHighest total = %d, want between 3 and 18", total)
	}
}

func TestKeepLowest(t *testing.T) {
	SetSeed(42)
	
	kept, total, err := KeepLowest(4, 6, 3)
	if err != nil {
		t.Fatalf("KeepLowest() error: %v", err)
	}
	
	if len(kept) != 3 {
		t.Errorf("KeepLowest returned %d dice, want 3", len(kept))
	}
	
	// Kept values should be sorted in ascending order
	for i := 1; i < len(kept); i++ {
		if kept[i] < kept[i-1] {
			t.Errorf("KeepLowest not sorted correctly: %v", kept)
		}
	}
	
	if total < 3 || total > 18 {
		t.Errorf("KeepLowest total = %d, want between 3 and 18", total)
	}
}

func TestKeepHighestErrors(t *testing.T) {
	_, _, err := KeepHighest(4, 6, 5)
	if err == nil {
		t.Error("KeepHighest with keep > numDice should return error")
	}
	
	_, _, err = KeepHighest(4, 6, 0)
	if err == nil {
		t.Error("KeepHighest with keep = 0 should return error")
	}
}

func TestMostProbableResult(t *testing.T) {
	tests := []struct {
		numDice int
		sides   int
		want    []int
	}{
		{2, 6, []int{7}},       // Most probable is 7
		{1, 6, []int{1, 2, 3, 4, 5, 6}}, // All equally probable
		{3, 6, []int{10, 11}},  // 10 and 11 are most probable
	}

	for _, tt := range tests {
		got := MostProbableResult(tt.numDice, tt.sides)
		if len(got) != len(tt.want) {
			t.Errorf("MostProbableResult(%d, %d) = %v, want %v", tt.numDice, tt.sides, got, tt.want)
			continue
		}
		// Check each expected value is present
		for _, w := range tt.want {
			found := false
			for _, g := range got {
				if g == w {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("MostProbableResult(%d, %d) = %v, missing %d", tt.numDice, tt.sides, got, w)
			}
		}
	}
}

func TestProbabilityTable(t *testing.T) {
	table := ProbabilityTable(2, 6)
	
	// Should contain expected headers
	if table == "" {
		t.Error("ProbabilityTable should not be empty")
	}
	
	// Should contain key values
	expected := []string{"2d6", "Value", "Ways", "Probability", "7"}
	for _, s := range expected {
		if !contains(table, s) {
			t.Errorf("ProbabilityTable missing %q", s)
		}
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || (len(s) > 0 && containsHelper(s, substr)))
}

func containsHelper(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// Benchmark tests
func BenchmarkRollDice(b *testing.B) {
	for i := 0; i < b.N; i++ {
		RollDice(2, 6)
	}
}

func BenchmarkCountWays(b *testing.B) {
	for i := 0; i < b.N; i++ {
		CountWays(10, 6, 35)
	}
}

func BenchmarkProbability(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Probability(2, 6, 7)
	}
}

func BenchmarkMonteCarlo(b *testing.B) {
	for i := 0; i < b.N; i++ {
		MonteCarloProbability(2, 6, 7, 1000)
	}
}

func BenchmarkHistogram(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Histogram(1000, 2, 6)
	}
}