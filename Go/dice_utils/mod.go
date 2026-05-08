// Package dice_utils provides comprehensive dice utilities for games and probability calculations.
// Supports multiple dice types, probability analysis, and common dice game scenarios.
// Zero external dependencies - pure Go standard library implementation.
package dice_utils

import (
	"errors"
	"fmt"
	"math"
	"math/rand"
	"sort"
	"time"
)

// Die represents a single die with a specified number of sides.
type Die struct {
	Sides int
}

// DiceRoll represents the result of rolling one or more dice.
type DiceRoll struct {
	Dice   []int // Individual die values
	Total  int   // Sum of all dice
	Count  int   // Number of dice rolled
	Sides  int   // Number of sides per die
	History []DiceRoll // For multi-roll tracking
}

// DiceConfig holds configuration for dice operations.
type DiceConfig struct {
	NumDice int
	Sides   int
	Modifier int // Value to add/subtract from total
}

// ProbResult holds probability calculation results.
type ProbResult struct {
	Ways     int     // Number of ways to achieve the result
	Total    int     // Total possible outcomes
	Exact    float64 // Exact probability
	AtLeast  float64 // Probability of getting at least this value
	AtMost   float64 // Probability of getting at most this value
}

var (
	rng = rand.New(rand.NewSource(time.Now().UnixNano()))
)

// NewDie creates a new die with the specified number of sides.
func NewDie(sides int) (*Die, error) {
	if sides < 2 {
		return nil, errors.New("die must have at least 2 sides")
	}
	return &Die{Sides: sides}, nil
}

// Roll rolls a single die and returns the result.
func (d *Die) Roll() int {
	return rng.Intn(d.Sides) + 1
}

// RollN rolls the die n times and returns all results.
func (d *Die) RollN(n int) []int {
	if n <= 0 {
		return []int{}
	}
	results := make([]int, n)
	for i := 0; i < n; i++ {
		results[i] = d.Roll()
	}
	return results
}

// RollDice rolls multiple dice with the same number of sides.
func RollDice(numDice, sides int) (*DiceRoll, error) {
	if numDice < 1 {
		return nil, errors.New("must roll at least 1 die")
	}
	if sides < 2 {
		return nil, errors.New("die must have at least 2 sides")
	}

	die, _ := NewDie(sides)
	dice := die.RollN(numDice)
	total := 0
	for _, v := range dice {
		total += v
	}

	return &DiceRoll{
		Dice:  dice,
		Total: total,
		Count: numDice,
		Sides: sides,
	}, nil
}

// RollWithModifier rolls dice and adds a modifier to the total.
func RollWithModifier(numDice, sides, modifier int) (*DiceRoll, error) {
	roll, err := RollDice(numDice, sides)
	if err != nil {
		return nil, err
	}
	roll.Total += modifier
	return roll, nil
}

// RollMultiple performs multiple dice rolls and returns all results.
func RollMultiple(numRolls, numDice, sides int) ([]DiceRoll, error) {
	if numRolls < 1 {
		return nil, errors.New("must perform at least 1 roll")
	}

	rolls := make([]DiceRoll, numRolls)
	for i := 0; i < numRolls; i++ {
		roll, err := RollDice(numDice, sides)
		if err != nil {
			return nil, err
		}
		rolls[i] = *roll
	}
	return rolls, nil
}

// MinPossible returns the minimum possible total for given dice.
func MinPossible(numDice int) int {
	return numDice
}

// MaxPossible returns the maximum possible total for given dice.
func MaxPossible(numDice, sides int) int {
	return numDice * sides
}

// TotalOutcomes calculates the total number of possible outcomes.
func TotalOutcomes(numDice, sides int) int {
	if numDice < 0 || sides < 0 {
		return 0
	}
	result := 1
	for i := 0; i < numDice; i++ {
		result *= sides
	}
	return result
}

// CountWays counts the number of ways to achieve a specific total.
// Uses dynamic programming for efficiency.
func CountWays(numDice, sides, target int) int {
	if numDice < 1 || sides < 2 {
		return 0
	}

	minVal := numDice
	maxVal := numDice * sides
	if target < minVal || target > maxVal {
		return 0
	}

	// DP approach: ways[i] = number of ways to achieve sum i
	ways := make([]int, maxVal+1)
	ways[0] = 1 // Base case for 0 dice

	for d := 0; d < numDice; d++ {
		newWays := make([]int, maxVal+1)
		for sum := 0; sum <= maxVal; sum++ {
			if ways[sum] > 0 {
				for face := 1; face <= sides; face++ {
					newWays[sum+face] += ways[sum]
				}
			}
		}
		ways = newWays
	}

	return ways[target]
}

// Probability calculates the probability of rolling a specific total.
func Probability(numDice, sides, target int) float64 {
	total := TotalOutcomes(numDice, sides)
	if total == 0 {
		return 0
	}
	ways := CountWays(numDice, sides, target)
	return float64(ways) / float64(total)
}

// ProbabilityRange calculates probability statistics for a target value.
func ProbabilityRange(numDice, sides, target int) *ProbResult {
	total := TotalOutcomes(numDice, sides)
	if total == 0 {
		return &ProbResult{}
	}

	ways := CountWays(numDice, sides, target)
	exact := float64(ways) / float64(total)

	minVal := numDice
	maxVal := numDice * sides

	// Calculate "at least" probability (target or higher)
	atLeastWays := 0
	for t := target; t <= maxVal; t++ {
		atLeastWays += CountWays(numDice, sides, t)
	}
	atLeast := float64(atLeastWays) / float64(total)

	// Calculate "at most" probability (target or lower)
	atMostWays := 0
	for t := minVal; t <= target; t++ {
		atMostWays += CountWays(numDice, sides, t)
	}
	atMost := float64(atMostWays) / float64(total)

	return &ProbResult{
		Ways:    ways,
		Total:   total,
		Exact:   exact,
		AtLeast: atLeast,
		AtMost:  atMost,
	}
}

// AllProbabilities returns probability distribution for all possible totals.
func AllProbabilities(numDice, sides int) map[int]float64 {
	result := make(map[int]float64)
	minVal := numDice
	maxVal := numDice * sides
	total := TotalOutcomes(numDice, sides)

	for t := minVal; t <= maxVal; t++ {
		result[t] = float64(CountWays(numDice, sides, t)) / float64(total)
	}
	return result
}

// ExpectedValue calculates the expected value (mean) of dice rolls.
func ExpectedValue(numDice, sides int) float64 {
	// E[X] for one die is (sides + 1) / 2
	singleMean := float64(sides+1) / 2
	return singleMean * float64(numDice)
}

// Variance calculates the variance of dice rolls.
func Variance(numDice, sides int) float64 {
	// Var[X] for one die is (sides^2 - 1) / 12
	singleVar := float64(sides*sides-1) / 12
	return singleVar * float64(numDice)
}

// StandardDeviation calculates the standard deviation of dice rolls.
func StandardDeviation(numDice, sides int) float64 {
	return math.Sqrt(Variance(numDice, sides))
}

// IsYahtzee checks if all dice show the same value (five-of-a-kind).
func IsYahtzee(dice []int) bool {
	if len(dice) < 1 {
		return false
	}
	first := dice[0]
	for _, d := range dice {
		if d != first {
			return false
		}
	}
	return true
}

// IsSmallStraight checks for a sequence of 4 consecutive values.
func IsSmallStraight(dice []int) bool {
	if len(dice) < 4 {
		return false
	}
	unique := make(map[int]bool)
	for _, d := range dice {
		unique[d] = true
	}
	vals := make([]int, 0, len(unique))
	for v := range unique {
		vals = append(vals, v)
	}
	sort.Ints(vals)

	// Check for 4 consecutive values
	for i := 0; i <= len(vals)-4; i++ {
		if vals[i+3]-vals[i] == 3 {
			consecutive := true
			for j := 0; j < 3; j++ {
				if vals[i+j+1]-vals[i+j] != 1 {
					consecutive = false
					break
				}
			}
			if consecutive {
				return true
			}
		}
	}
	return false
}

// IsLargeStraight checks for a sequence of 5 consecutive values.
func IsLargeStraight(dice []int) bool {
	if len(dice) < 5 {
		return false
	}
	unique := make(map[int]bool)
	for _, d := range dice {
		unique[d] = true
	}
	vals := make([]int, 0, len(unique))
	for v := range unique {
		vals = append(vals, v)
	}
	sort.Ints(vals)

	if len(vals) < 5 {
		return false
	}

	for i := 0; i <= len(vals)-5; i++ {
		consecutive := true
		for j := 0; j < 4; j++ {
			if vals[i+j+1]-vals[i+j] != 1 {
				consecutive = false
				break
			}
		}
		if consecutive {
			return true
		}
	}
	return false
}

// CountOfKind returns the count of the most frequent value.
// Also returns the value.
func CountOfKind(dice []int) (count int, value int) {
	if len(dice) == 0 {
		return 0, 0
	}
	counts := make(map[int]int)
	for _, d := range dice {
		counts[d]++
	}
	maxCount := 0
	maxVal := dice[0]
	for v, c := range counts {
		if c > maxCount {
			maxCount = c
			maxVal = v
		}
	}
	return maxCount, maxVal
}

// IsFullHouse checks for three-of-a-kind plus a pair.
// Five-of-a-kind also counts as full house (can be viewed as 3+2).
func IsFullHouse(dice []int) bool {
	if len(dice) < 5 {
		return false
	}
	counts := make(map[int]int)
	for _, d := range dice {
		counts[d]++
	}
	
	// Check for either:
	// 1) A value with exactly 3 and another with exactly 2
	// 2) A value with 5 (counts as both 3 and 2)
	for v, c := range counts {
		if c == 5 {
			return true // Five-of-a-kind counts as full house
		}
		if c == 3 {
			// Check if another value has exactly 2
			for v2, c2 := range counts {
				if v2 != v && c2 == 2 {
					return true
				}
			}
		}
	}
	return false
}

// SumDice returns the sum of dice values.
func SumDice(dice []int) int {
	total := 0
	for _, d := range dice {
		total += d
	}
	return total
}

// SumOfValue returns the sum of dice showing a specific value.
func SumOfValue(dice []int, value int) int {
	total := 0
	for _, d := range dice {
		if d == value {
			total += d
		}
	}
	return total
}

// RerollSelective rerolls specific dice by index.
func RerollSelective(dice []int, sides int, indices []int) ([]int, error) {
	if len(dice) == 0 {
		return nil, errors.New("no dice to reroll")
	}
	if sides < 2 {
		return nil, errors.New("invalid sides")
	}

	result := make([]int, len(dice))
	copy(result, dice)

	die, _ := NewDie(sides)
	for _, idx := range indices {
		if idx < 0 || idx >= len(dice) {
			return nil, fmt.Errorf("index %d out of bounds", idx)
		}
		result[idx] = die.Roll()
	}
	return result, nil
}

// DiceNotation parses dice notation like "2d6", "3d8+5", "1d20-2".
func DiceNotation(notation string) (*DiceConfig, error) {
	var numDice, sides, modifier int
	var op byte

	n, err := fmt.Sscanf(notation, "%dd%d%c%d", &numDice, &sides, &op, &modifier)
	if err != nil && n < 2 {
		return nil, fmt.Errorf("invalid notation: %s", notation)
	}

	config := &DiceConfig{
		NumDice: numDice,
		Sides:   sides,
	}

	if n == 4 {
		if op == '-' {
			config.Modifier = -modifier
		} else if op == '+' {
			config.Modifier = modifier
		}
	}

	return config, nil
}

// RollNotation rolls dice based on notation string.
func RollNotation(notation string) (*DiceRoll, error) {
	config, err := DiceNotation(notation)
	if err != nil {
		return nil, err
	}

	roll, err := RollDice(config.NumDice, config.Sides)
	if err != nil {
		return nil, err
	}

	roll.Total += config.Modifier
	return roll, nil
}

// Advantage rolls twice and takes the higher result.
func Advantage(sides int) (*DiceRoll, error) {
	roll1, err := RollDice(1, sides)
	if err != nil {
		return nil, err
	}
	roll2, err := RollDice(1, sides)
	if err != nil {
		return nil, err
	}

	if roll1.Total > roll2.Total {
		return roll1, nil
	}
	return roll2, nil
}

// Disadvantage rolls twice and takes the lower result.
func Disadvantage(sides int) (*DiceRoll, error) {
	roll1, err := RollDice(1, sides)
	if err != nil {
		return nil, err
	}
	roll2, err := RollDice(1, sides)
	if err != nil {
		return nil, err
	}

	if roll1.Total < roll2.Total {
		return roll1, nil
	}
	return roll2, nil
}

// CoinFlip simulates a coin flip, returning "heads" or "tails".
func CoinFlip() string {
	if rng.Intn(2) == 0 {
		return "heads"
	}
	return "tails"
}

// CoinFlipN flips n coins and returns the results.
func CoinFlipN(n int) []string {
	results := make([]string, n)
	for i := 0; i < n; i++ {
		results[i] = CoinFlip()
	}
	return results
}

// PercentileRoll rolls a percentile die (d100).
func PercentileRoll() int {
	return rng.Intn(100) + 1
}

// FudgeRoll rolls FUDGE dice (-1, 0, +1).
// Returns the sum and individual results.
func FudgeRoll(numDice int) (int, []int) {
	die, _ := NewDie(3)
	results := die.RollN(numDice)
	total := 0
	for i, v := range results {
		// Map 1->-1, 2->0, 3->+1
		results[i] = v - 2
		total += results[i]
	}
	return total, results
}

// Histogram generates a frequency distribution of multiple rolls.
func Histogram(numRolls, numDice, sides int) (map[int]int, error) {
	rolls, err := RollMultiple(numRolls, numDice, sides)
	if err != nil {
		return nil, err
	}

	hist := make(map[int]int)
	for _, roll := range rolls {
		hist[roll.Total]++
	}
	return hist, nil
}

// MonteCarloProbability estimates probability through simulation.
func MonteCarloProbability(numDice, sides, target, simulations int) float64 {
	if simulations < 1 {
		return 0
	}

	successes := 0
	for i := 0; i < simulations; i++ {
		roll, _ := RollDice(numDice, sides)
		if roll.Total == target {
			successes++
		}
	}
	return float64(successes) / float64(simulations)
}

// SetSeed sets the random seed for reproducible results.
func SetSeed(seed int64) {
	rng = rand.New(rand.NewSource(seed))
}

// String returns a string representation of a dice roll.
func (dr *DiceRoll) String() string {
	return fmt.Sprintf("%v = %d", dr.Dice, dr.Total)
}

// Format formats a dice roll with optional notation.
func (dr *DiceRoll) Format() string {
	if dr.Count == 1 {
		return fmt.Sprintf("[%d]", dr.Dice[0])
	}
	return fmt.Sprintf("%dd%d: %v = %d", dr.Count, dr.Sides, dr.Dice, dr.Total)
}

// CriticalHit checks if a d20 roll is a critical hit (natural 20).
func CriticalHit(roll int) bool {
	return roll == 20
}

// CriticalMiss checks if a d20 roll is a critical miss (natural 1).
func CriticalMiss(roll int) bool {
	return roll == 1
}

// RollD20 rolls a d20 and returns the result.
func RollD20() int {
	roll, _ := RollDice(1, 20)
	return roll.Total
}

// RollD6 rolls a d6 and returns the result.
func RollD6() int {
	roll, _ := RollDice(1, 6)
	return roll.Total
}

// RollD100 rolls a d100 and returns the result.
func RollD100() int {
	return PercentileRoll()
}

// RollD4 rolls a d4 and returns the result.
func RollD4() int {
	roll, _ := RollDice(1, 4)
	return roll.Total
}

// RollD8 rolls a d8 and returns the result.
func RollD8() int {
	roll, _ := RollDice(1, 8)
	return roll.Total
}

// RollD10 rolls a d10 and returns the result.
func RollD10() int {
	roll, _ := RollDice(1, 10)
	return roll.Total
}

// RollD12 rolls a d12 and returns the result.
func RollD12() int {
	roll, _ := RollDice(1, 12)
	return roll.Total
}

// ExplodingDie rolls a die that "explodes" on max value (rolls again and adds).
// maxExplodes limits the number of explosions (0 = unlimited).
func ExplodingDie(sides, maxExplodes int) (int, []int) {
	die, _ := NewDie(sides)
	results := []int{}
	total := 0
	explosions := 0

	for {
		roll := die.Roll()
		results = append(results, roll)
		total += roll

		if roll == sides && (maxExplodes == 0 || explosions < maxExplodes) {
			explosions++
			continue
		}
		break
	}
	return total, results
}

// KeepHighest rolls multiple dice and keeps the highest n.
func KeepHighest(numDice, sides, keep int) ([]int, int, error) {
	if keep > numDice || keep < 1 {
		return nil, 0, fmt.Errorf("keep must be between 1 and %d", numDice)
	}

	die, _ := NewDie(sides)
	rolls := die.RollN(numDice)
	sort.Sort(sort.Reverse(sort.IntSlice(rolls)))

	kept := rolls[:keep]
	total := 0
	for _, v := range kept {
		total += v
	}
	return kept, total, nil
}

// KeepLowest rolls multiple dice and keeps the lowest n.
func KeepLowest(numDice, sides, keep int) ([]int, int, error) {
	if keep > numDice || keep < 1 {
		return nil, 0, fmt.Errorf("keep must be between 1 and %d", numDice)
	}

	die, _ := NewDie(sides)
	rolls := die.RollN(numDice)
	sort.Ints(rolls)

	kept := rolls[:keep]
	total := 0
	for _, v := range kept {
		total += v
	}
	return kept, total, nil
}

// MostProbableResult returns the most likely total(s) for given dice.
func MostProbableResult(numDice, sides int) []int {
	minVal := numDice
	maxVal := numDice * sides

	maxWays := 0
	results := []int{}

	for t := minVal; t <= maxVal; t++ {
		ways := CountWays(numDice, sides, t)
		if ways > maxWays {
			maxWays = ways
			results = []int{t}
		} else if ways == maxWays {
			results = append(results, t)
		}
	}
	return results
}

// ProbabilityTable generates a formatted probability table string.
func ProbabilityTable(numDice, sides int) string {
	minVal := numDice
	maxVal := numDice * sides
	total := TotalOutcomes(numDice, sides)

	result := fmt.Sprintf("Probability Table for %dd%d\n", numDice, sides)
	result += fmt.Sprintf("Total outcomes: %d\n\n", total)
	result += "Value\tWays\tProbability\n"
	result += "----\t----\t-----------\n"

	for t := minVal; t <= maxVal; t++ {
		ways := CountWays(numDice, sides, t)
		prob := float64(ways) / float64(total) * 100
		result += fmt.Sprintf("%d\t%d\t%.4f%%\n", t, ways, prob)
	}
	return result
}