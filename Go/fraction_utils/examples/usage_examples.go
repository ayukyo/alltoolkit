// Example usage of fractionutils package
package main

import (
	"fmt"
	"math"

	"github.com/ayukyo/alltoolkit/fractionutils"
)

func main() {
	fmt.Println("=== Fraction Utils Examples ===\n")

	// 1. Creating Fractions
	fmt.Println("1. Creating Fractions:")
	fmt.Println("------------------------")

	// From numerator and denominator
	f1, _ := fractionutils.New(3, 4)
	fmt.Printf("   New(3, 4) = %s\n", f1)

	// Automatic reduction
	f2, _ := fractionutils.New(6, 8)
	fmt.Printf("   New(6, 8) = %s (auto-reduced)\n", f2)

	// From integer
	f3 := fractionutils.FromInt(5)
	fmt.Printf("   FromInt(5) = %s\n", f3)

	// From float
	f4 := fractionutils.FromFloat(0.75, 100)
	fmt.Printf("   FromFloat(0.75, 100) = %s\n", f4)

	// From string
	f5, _ := fractionutils.Parse("2/3")
	fmt.Printf("   Parse(\"2/3\") = %s\n", f5)

	f6, _ := fractionutils.Parse("1.5")
	fmt.Printf("   Parse(\"1.5\") = %s\n", f6)

	// Using ratio shorthand
	f7 := fractionutils.Ratio(5, 8)
	fmt.Printf("   Ratio(5, 8) = %s\n", f7)

	fmt.Println()

	// 2. Arithmetic Operations
	fmt.Println("2. Arithmetic Operations:")
	fmt.Println("------------------------")

	a, _ := fractionutils.New(1, 2)
	b, _ := fractionutils.New(1, 3)

	fmt.Printf("   a = %s, b = %s\n", a, b)
	fmt.Printf("   a + b = %s\n", a.Add(b))
	fmt.Printf("   a - b = %s\n", a.Subtract(b))
	fmt.Printf("   a × b = %s\n", a.Multiply(b))

	quotient, _ := a.Divide(b)
	fmt.Printf("   a ÷ b = %s\n", quotient)

	c, _ := fractionutils.New(2, 3)
	fmt.Printf("   -%s = %s\n", c, c.Negate())

	recip, _ := c.Reciprocal()
	fmt.Printf("   1/(%s) = %s\n", c, recip)

	fmt.Println()

	// 3. Comparison Operations
	fmt.Println("3. Comparison Operations:")
	fmt.Println("------------------------")

	x, _ := fractionutils.New(1, 2)
	y, _ := fractionutils.New(2, 4)
	z, _ := fractionutils.New(1, 3)

	fmt.Printf("   x = %s, y = %s, z = %s\n", x, y, z)
	fmt.Printf("   %s == %s: %v\n", x, y, x.Equal(y))
	fmt.Printf("   %s < %s: %v\n", z, x, z.LessThan(x))
	fmt.Printf("   %s > %s: %v\n", x, z, x.GreaterThan(z))
	fmt.Printf("   Compare(%s, %s): %d\n", x, z, x.Compare(z))

	fmt.Println()

	// 4. Conversion Methods
	fmt.Println("4. Conversion Methods:")
	fmt.Println("---------------------")

	f, _ := fractionutils.New(7, 4)
	fmt.Printf("   Fraction: %s\n", f)
	fmt.Printf("   Float64: %v\n", f.Float64())
	fmt.Printf("   ToInt: %d\n", f.ToInt())
	fmt.Printf("   ToMixed: %s\n", f.ToMixed())
	fmt.Printf("   String: %s\n", f.String())

	fmt.Println()

	// 5. Mathematical Functions
	fmt.Println("5. Mathematical Functions:")
	fmt.Println("--------------------------")

	base, _ := fractionutils.New(2, 3)
	squared, _ := base.Pow(2)
	cubed, _ := base.Pow(3)
	fmt.Printf("   (%s)² = %s\n", base, squared)
	fmt.Printf("   (%s)³ = %s\n", base, cubed)

	perfectSquare, _ := fractionutils.New(9, 16)
	sqrt, _ := perfectSquare.Sqrt()
	fmt.Printf("   √%s = %s\n", perfectSquare, sqrt)

	fmt.Println()

	// 6. Utility Functions
	fmt.Println("6. Utility Functions:")
	fmt.Println("----------------------")

	pos, _ := fractionutils.New(3, 4)
	neg, _ := fractionutils.New(-3, 4)
	zero := fractionutils.Zero

	fmt.Printf("   %s: IsZero=%v, IsInteger=%v, IsPositive=%v, IsNegative=%v\n",
		pos, pos.IsZero(), pos.IsInteger(), pos.IsPositive(), pos.IsNegative())
	fmt.Printf("   %s: IsZero=%v, IsInteger=%v, IsPositive=%v, IsNegative=%v\n",
		neg, neg.IsZero(), neg.IsInteger(), neg.IsPositive(), neg.IsNegative())
	fmt.Printf("   %s: IsZero=%v, IsInteger=%v, IsPositive=%v, IsNegative=%v\n",
		zero, zero.IsZero(), zero.IsInteger(), zero.IsPositive(), zero.IsNegative())

	fmt.Printf("   Abs(%s) = %s\n", neg, neg.Abs())
	fmt.Printf("   Sign(%s) = %d\n", pos, pos.Sign())
	fmt.Printf("   Sign(%s) = %d\n", neg, neg.Sign())

	fmt.Println()

	// 7. Batch Operations
	fmt.Println("7. Batch Operations:")
	fmt.Println("---------------------")

	fractions := []fractionutils.Fraction{
		fractionutils.Ratio(1, 4),
		fractionutils.Ratio(1, 3),
		fractionutils.Ratio(1, 2),
	}

	sum := fractionutils.Sum(fractions...)
	product := fractionutils.Product(fractions...)

	fmt.Printf("   Fractions: %v, %v, %v\n", fractions[0], fractions[1], fractions[2])
	fmt.Printf("   Sum: %s = %v\n", sum, sum.Float64())
	fmt.Printf("   Product: %s = %v\n", product, product.Float64())

	fmt.Println()

	// 8. Min/Max
	fmt.Println("8. Min/Max:")
	fmt.Println("------------")

	p, _ := fractionutils.New(1, 3)
	q, _ := fractionutils.New(1, 2)
	r, _ := fractionutils.New(3, 4)

	fmt.Printf("   %s, %s, %s\n", p, q, r)
	fmt.Printf("   Min(%s, %s) = %s\n", p, q, fractionutils.Min(p, q))
	fmt.Printf("   Max(%s, %s) = %s\n", q, r, fractionutils.Max(q, r))

	fmt.Println()

	// 9. Common Denominator
	fmt.Println("9. Common Denominator:")
	fmt.Println("-----------------------")

	frac1, _ := fractionutils.New(1, 3)
	frac2, _ := fractionutils.New(1, 4)

	cd1, cd2 := fractionutils.WithCommonDenominator(frac1, frac2)
	fmt.Printf("   Original: %s, %s\n", frac1, frac2)
	fmt.Printf("   Common denom: %s, %s\n", cd1, cd2)

	fmt.Println()

	// 10. Predefined Constants
	fmt.Println("10. Predefined Constants:")
	fmt.Println("--------------------------")

	fmt.Printf("   Zero = %s\n", fractionutils.Zero)
	fmt.Printf("   One = %s\n", fractionutils.One)
	fmt.Printf("   Half = %s\n", fractionutils.Half)
	fmt.Printf("   Third = %s\n", fractionutils.Third)
	fmt.Printf("   Quarter = %s\n", fractionutils.Quarter)
	fmt.Printf("   Fifth = %s\n", fractionutils.Fifth)

	fmt.Println()

	// 11. Real-world Example: Recipe Scaling
	fmt.Println("11. Real-world Example: Recipe Scaling")
	fmt.Println("----------------------------------------")

	// Original recipe serves 4, we want to serve 6
	originalServings := fractionutils.FromInt(4)
	newServings := fractionutils.FromInt(6)
	scale, _ := newServings.Divide(originalServings)

	fmt.Printf("   Original servings: %s\n", originalServings)
	fmt.Printf("   New servings: %s\n", newServings)
	fmt.Printf("   Scale factor: %s = %.2f\n", scale, scale.Float64())

	// Scale ingredients
	cupFlour, _ := fractionutils.New(2, 1)
	cupSugar, _ := fractionutils.New(1, 2)
	tspSalt := fractionutils.FromInt(1)

	fmt.Printf("   %.0f cups flour → %.2f cups\n", cupFlour.Float64(), cupFlour.Multiply(scale).Float64())
	fmt.Printf("   %.1f cups sugar → %.2f cups\n", cupSugar.Float64(), cupSugar.Multiply(scale).Float64())
	fmt.Printf("   %.0f tsp salt → %.2f tsp\n", tspSalt.Float64(), tspSalt.Multiply(scale).Float64())

	fmt.Println()

	// 12. Real-world Example: Financial Calculation
	fmt.Println("12. Real-world Example: Financial Calculation")
	fmt.Println("----------------------------------------------")

	// Calculate exact profit sharing
	totalProfit := fractionutils.FromInt(100000)
	partner1, _ := fractionutils.New(1, 3) // 1/3
	partner2, _ := fractionutils.New(2, 5) // 2/5
	// partner3 gets the rest

	p1Share := totalProfit.Multiply(partner1)
	p2Share := totalProfit.Multiply(partner2)
	p3Share := totalProfit.Subtract(p1Share).Subtract(p2Share)

	fmt.Printf("   Total profit: $%.0f\n", totalProfit.Float64())
	fmt.Printf("   Partner 1 (1/3): $%.2f\n", p1Share.Float64())
	fmt.Printf("   Partner 2 (2/5): $%.2f\n", p2Share.Float64())
	fmt.Printf("   Partner 3 (rest): $%.2f\n", p3Share.Float64())

	// Verify no rounding errors
	verification := p1Share.Add(p2Share).Add(p3Share)
	fmt.Printf("   Verification (sum): $%.2f\n", verification.Float64())
	fmt.Printf("   Exact match: %v\n", verification.Equal(totalProfit))

	fmt.Println()

	// 13. Precision Comparison
	fmt.Println("13. Precision Comparison (Fraction vs Float)")
	fmt.Println("----------------------------------------------")

	// Classic floating-point precision issue
	floatResult := 0.1 + 0.2
	fmt.Printf("   Float: 0.1 + 0.2 = %.17f (imprecise!)\n", floatResult)

	// Fraction gives exact result
	fracA, _ := fractionutils.New(1, 10)
	fracB, _ := fractionutils.New(2, 10)
	fracResult := fracA.Add(fracB)
	fmt.Printf("   Fraction: 1/10 + 2/10 = %s = %.17f (exact!)\n", fracResult, fracResult.Float64())

	// More complex example
	sum1 := float64(0)
	for i := 0; i < 10; i++ {
		sum1 += 0.1
	}
	fmt.Printf("   Float: sum(0.1, 10 times) = %.17f (error: %.17f)\n", sum1, math.Abs(sum1-1.0))

	sum2 := fractionutils.Zero
	for i := 0; i < 10; i++ {
		fracTenth, _ := fractionutils.New(1, 10)
		sum2 = sum2.Add(fracTenth)
	}
	fmt.Printf("   Fraction: sum(1/10, 10 times) = %s = %.17f (exact!)\n", sum2, sum2.Float64())

	fmt.Println()

	// 14. Complex Expression Evaluation
	fmt.Println("14. Complex Expression Evaluation")
	fmt.Println("-----------------------------------")

	// Evaluate: (3/4 + 1/6) * (2/3 - 1/4) ÷ 5/8
	term1, _ := fractionutils.New(3, 4)
	term2, _ := fractionutils.New(1, 6)
	term3, _ := fractionutils.New(2, 3)
	term4, _ := fractionutils.New(1, 4)
	term5, _ := fractionutils.New(5, 8)

	step1 := term1.Add(term2) // 3/4 + 1/6 = 11/12
	step2 := term3.Subtract(term4) // 2/3 - 1/4 = 5/12
	step3 := step1.Multiply(step2) // 11/12 * 5/12 = 55/144
	result, _ := step3.Divide(term5) // 55/144 ÷ 5/8 = 11/18

	fmt.Printf("   Expression: (%s + %s) × (%s - %s) ÷ %s\n", term1, term2, term3, term4, term5)
	fmt.Printf("   Step 1: %s + %s = %s\n", term1, term2, step1)
	fmt.Printf("   Step 2: %s - %s = %s\n", term3, term4, step2)
	fmt.Printf("   Step 3: %s × %s = %s\n", step1, step2, step3)
	fmt.Printf("   Step 4: %s ÷ %s = %s\n", step3, term5, result)
	fmt.Printf("   Final result: %s ≈ %.6f\n", result, result.Float64())

	fmt.Println()
	fmt.Println("=== All Examples Complete ===")
}