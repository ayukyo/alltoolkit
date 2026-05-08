package main

import (
	"fmt"
	"github.com/ayukyo/alltoolkit/Go/dice_utils"
)

func main() {
	fmt.Println("🎲 Dice Utils Examples")
	fmt.Println("======================")

	// Example 1: Basic dice rolling
	fmt.Println("\n--- Example 1: Basic Dice Rolling ---")
	roll1, _ := dice_utils.RollDice(2, 6)
	fmt.Printf("Rolling 2d6: %s\n", roll1.Format())

	roll2, _ := dice_utils.RollDice(1, 20)
	fmt.Printf("Rolling 1d20: %s\n", roll2.Format())

	roll3, _ := dice_utils.RollDice(3, 8)
	fmt.Printf("Rolling 3d8: %s\n", roll3.Format())

	// Example 2: Dice notation
	fmt.Println("\n--- Example 2: Dice Notation ---")
	roll4, _ := dice_utils.RollNotation("4d6+10")
	fmt.Printf("4d6+10: %s\n", roll4.Format())

	roll5, _ := dice_utils.RollNotation("1d20-2")
	fmt.Printf("1d20-2: %s\n", roll5.Format())

	config, _ := dice_utils.DiceNotation("3d10+5")
	fmt.Printf("Parsed '3d10+5': %d dice, %d sides, +%d modifier\n", 
		config.NumDice, config.Sides, config.Modifier)

	// Example 3: Probability calculations
	fmt.Println("\n--- Example 3: Probability Calculations ---")
	prob7 := dice_utils.Probability(2, 6, 7)
	fmt.Printf("Probability of rolling 7 on 2d6: %.4f (%.2f%%)\n", prob7, prob7*100)

	pr := dice_utils.ProbabilityRange(2, 6, 7)
	fmt.Printf("Detailed probability for 7 on 2d6:\n")
	fmt.Printf("  Ways to get 7: %d\n", pr.Ways)
	fmt.Printf("  Total outcomes: %d\n", pr.Total)
	fmt.Printf("  Exact probability: %.4f%%\n", pr.Exact*100)
	fmt.Printf("  At least 7: %.4f%%\n", pr.AtLeast*100)
	fmt.Printf("  At most 7: %.4f%%\n", pr.AtMost*100)

	// Example 4: Statistics
	fmt.Println("\n--- Example 4: Statistics ---")
	ev := dice_utils.ExpectedValue(2, 6)
	var := dice_utils.Variance(2, 6)
	sd := dice_utils.StandardDeviation(2, 6)
	fmt.Printf("Statistics for 2d6:\n")
	fmt.Printf("  Expected Value: %.2f\n", ev)
	fmt.Printf("  Variance: %.4f\n", var)
	fmt.Printf("  Standard Deviation: %.4f\n", sd)

	// Example 5: D&D-style rolling
	fmt.Println("\n--- Example 5: D&D-Style Rolling ---")
	d20 := dice_utils.RollD20()
	fmt.Printf("D20 roll: %d\n", d20)
	if dice_utils.CriticalHit(d20) {
		fmt.Println("🎉 CRITICAL HIT!")
	} else if dice_utils.CriticalMiss(d20) {
		fmt.Println("💀 CRITICAL MISS!")
	}

	adv, _ := dice_utils.Advantage(20)
	fmt.Printf("Advantage roll: %d\n", adv.Total)

	disadv, _ := dice_utils.Disadvantage(20)
	fmt.Printf("Disadvantage roll: %d\n", disadv.Total)

	// Example 6: Quick rolls
	fmt.Println("\n--- Example 6: Quick Roll Functions ---")
	fmt.Printf("D4: %d, D6: %d, D8: %d, D10: %d, D12: %d, D20: %d, D100: %d\n",
		dice_utils.RollD4(), dice_utils.RollD6(), dice_utils.RollD8(),
		dice_utils.RollD10(), dice_utils.RollD12(), dice_utils.RollD20(),
		dice_utils.RollD100())

	// Example 7: Yahtzee-style patterns
	fmt.Println("\n--- Example 7: Yahtzee-Style Patterns ---")
	dice_utils.SetSeed(42)
	dice := []int{1, 1, 1, 2, 2}
	fmt.Printf("Dice: %v\n", dice)
	fmt.Printf("  Is Yahtzee (5-of-a-kind): %v\n", dice_utils.IsYahtzee(dice))
	fmt.Printf("  Is Full House (3+2): %v\n", dice_utils.IsFullHouse(dice))
	cnt, val := dice_utils.CountOfKind(dice)
	fmt.Printf("  Count of kind: %d of value %d\n", cnt, val)

	dice2 := []int{1, 2, 3, 4, 5}
	fmt.Printf("Dice: %v\n", dice2)
	fmt.Printf("  Is Large Straight: %v\n", dice_utils.IsLargeStraight(dice2))
	fmt.Printf("  Is Small Straight: %v\n", dice_utils.IsSmallStraight(dice2))

	dice3 := []int{6, 6, 6, 6, 6}
	fmt.Printf("Dice: %v\n", dice3)
	fmt.Printf("  Is Yahtzee: %v\n", dice_utils.IsYahtzee(dice3))

	// Example 8: Keep highest/lowest (ability score generation)
	fmt.Println("\n--- Example 8: Keep Highest/Lowest ---")
	dice_utils.SetSeed(42)
	keptHi, totalHi, _ := dice_utils.KeepHighest(4, 6, 3)
	fmt.Printf("Roll 4d6, keep highest 3: %v = %d\n", keptHi, totalHi)

	keptLo, totalLo, _ := dice_utils.KeepLowest(4, 6, 3)
	fmt.Printf("Roll 4d6, keep lowest 3: %v = %d\n", keptLo, totalLo)

	// Example 9: Coin flips
	fmt.Println("\n--- Example 9: Coin Flips ---")
	fmt.Printf("Single flip: %s\n", dice_utils.CoinFlip())
	flips := dice_utils.CoinFlipN(10)
	fmt.Printf("10 flips: %v\n", flips)

	// Example 10: FUDGE dice
	fmt.Println("\n--- Example 10: FUDGE Dice ---")
	fudgeTotal, fudgeResults := dice_utils.FudgeRoll(4)
	fmt.Printf("4dF (FUDGE dice): %v = %d\n", fudgeResults, fudgeTotal)

	// Example 11: Exploding dice
	fmt.Println("\n--- Example 11: Exploding Dice ---")
	dice_utils.SetSeed(42)
	explodeTotal, explodeResults := dice_utils.ExplodingDie(6, 3)
	fmt.Printf("Exploding d6 (max 3 explosions): %v = %d\n", explodeResults, explodeTotal)

	// Example 12: Monte Carlo simulation
	fmt.Println("\n--- Example 12: Monte Carlo Probability ---")
	mcProb := dice_utils.MonteCarloProbability(2, 6, 7, 10000)
	actualProb := dice_utils.Probability(2, 6, 7)
	fmt.Printf("Monte Carlo estimate for 2d6=7: %.4f (%.2f%%)\n", mcProb, mcProb*100)
	fmt.Printf("Exact probability: %.4f (%.2f%%)\n", actualProb, actualProb*100)

	// Example 13: Most probable results
	fmt.Println("\n--- Example 13: Most Probable Results ---")
	mostProb := dice_utils.MostProbableResult(2, 6)
	fmt.Printf("Most probable total(s) for 2d6: %v\n", mostProb)

	mostProb3 := dice_utils.MostProbableResult(3, 6)
	fmt.Printf("Most probable total(s) for 3d6: %v\n", mostProb3)

	// Example 14: Percentile roll
	fmt.Println("\n--- Example 14: Percentile Roll ---")
	perc := dice_utils.PercentileRoll()
	fmt.Printf("Percentile (d100): %d\n", perc)

	// Example 15: Selective reroll
	fmt.Println("\n--- Example 15: Selective Reroll ---")
	dice_utils.SetSeed(42)
	original := []int{1, 3, 5, 2, 4}
	rerolled, _ := dice_utils.RerollSelective(original, 6, []int{0, 2})
	fmt.Printf("Original dice: %v\n", original)
	fmt.Printf("Reroll positions [0,2]: %v\n", rerolled)

	// Example 16: Probability table
	fmt.Println("\n--- Example 16: Probability Table ---")
	fmt.Println(dice_utils.ProbabilityTable(2, 6))
}