// Package fractionutils provides a Fraction type for exact rational arithmetic.
// All operations are safe for concurrent use and maintain precision without floating-point errors.
package fractionutils

import (
	"errors"
	"fmt"
	"math"
	"strconv"
	"strings"
)

// Fraction represents a rational number as a numerator and denominator.
// The denominator is always positive, and the fraction is stored in reduced form.
type Fraction struct {
	num int64 // numerator
	den int64 // denominator (always positive)
}

// Errors
var (
	ErrZeroDenominator = errors.New("denominator cannot be zero")
	ErrDivisionByZero  = errors.New("division by zero")
	ErrInvalidFormat   = errors.New("invalid fraction format")
)

// New creates a new Fraction from numerator and denominator.
// The fraction is automatically reduced to lowest terms.
// Returns an error if denominator is zero.
//
// Parameters:
//   - numerator: The numerator of the fraction.
//   - denominator: The denominator of the fraction (must not be zero).
//
// Returns:
//   - A Fraction in reduced form.
//   - An error if denominator is zero.
//
// Example:
//
//     f, _ := New(6, 8)   // Returns 3/4
//     f, _ := New(-2, -4) // Returns 1/2
func New(numerator, denominator int64) (Fraction, error) {
	if denominator == 0 {
		return Fraction{}, ErrZeroDenominator
	}

	// Ensure denominator is positive
	if denominator < 0 {
		numerator = -numerator
		denominator = -denominator
	}

	// Reduce to lowest terms
	g := gcd(abs(numerator), denominator)
	return Fraction{
		num: numerator / g,
		den: denominator / g,
	}, nil
}

// FromInt creates a Fraction from an integer.
//
// Parameters:
//   - n: The integer value.
//
// Returns:
//   - A Fraction representing the integer.
//
// Example:
//
//     f := FromInt(5)  // Returns 5/1
func FromInt(n int64) Fraction {
	return Fraction{num: n, den: 1}
}

// FromFloat creates a Fraction from a float64.
// Uses continued fraction expansion for accurate conversion.
//
// Parameters:
//   - x: The float value to convert.
//   - maxDenominator: Maximum allowed denominator (for precision control).
//
// Returns:
//   - A Fraction approximating the float.
//
// Example:
//
//     f := FromFloat(0.75, 1000)  // Returns 3/4
//     f := FromFloat(3.14159, 100) // Returns 22/7
func FromFloat(x float64, maxDenominator int64) Fraction {
	if x == 0 {
		return Fraction{num: 0, den: 1}
	}

	sign := int64(1)
	if x < 0 {
		sign = -1
		x = -x
	}

	// Handle infinity and NaN
	if math.IsInf(x, 1) || math.IsNaN(x) {
		return Fraction{num: 0, den: 1}
	}

	// Continued fraction expansion
	a0 := int64(x)
	x = x - float64(a0)
	
	if x < 1e-15 {
		return Fraction{num: sign * a0, den: 1}
	}

	// Initialize convergents
	p0, p1 := int64(1), a0
	q0, q1 := int64(0), int64(1)

	for i := 0; i < 100; i++ { // Limit iterations
		if x < 1e-15 {
			break
		}

		recip := 1.0 / x
		a := int64(recip)
		x = recip - float64(a)

		p0, p1 = p1, a*p1+p0
		q0, q1 = q1, a*q1+q0

		if q1 > maxDenominator {
			// Use previous convergent
			f, _ := New(sign*p0, q0)
			return f
		}
	}

	f, _ := New(sign*p1, q1)
	return f
}

// Parse creates a Fraction from a string.
// Supports formats: "3/4", "-5/6", "7" (integer), "2.5" (decimal).
//
// Parameters:
//   - s: The string to parse.
//
// Returns:
//   - The parsed Fraction.
//   - An error if the format is invalid.
//
// Example:
//
//     f, _ := Parse("3/4")    // Returns 3/4
//     f, _ := Parse("-5/6")   // Returns -5/6
//     f, _ := Parse("2.5")    // Returns 5/2
//     f, _ := Parse("7")      // Returns 7/1
func Parse(s string) (Fraction, error) {
	s = strings.TrimSpace(s)
	if s == "" {
		return Fraction{}, ErrInvalidFormat
	}

	// Try integer format
	if !strings.Contains(s, "/") && !strings.Contains(s, ".") {
		n, err := strconv.ParseInt(s, 10, 64)
		if err != nil {
			return Fraction{}, ErrInvalidFormat
		}
		return FromInt(n), nil
	}

	// Try decimal format
	if strings.Contains(s, ".") {
		f, err := strconv.ParseFloat(s, 64)
		if err != nil {
			return Fraction{}, ErrInvalidFormat
		}
		return FromFloat(f, 1000000000), nil
	}

	// Try fraction format
	parts := strings.Split(s, "/")
	if len(parts) != 2 {
		return Fraction{}, ErrInvalidFormat
	}

	num, err := strconv.ParseInt(strings.TrimSpace(parts[0]), 10, 64)
	if err != nil {
		return Fraction{}, ErrInvalidFormat
	}

	den, err := strconv.ParseInt(strings.TrimSpace(parts[1]), 10, 64)
	if err != nil {
		return Fraction{}, ErrInvalidFormat
	}

	return New(num, den)
}

// Numerator returns the numerator of the fraction.
func (f Fraction) Numerator() int64 {
	return f.num
}

// Denominator returns the denominator of the fraction.
func (f Fraction) Denominator() int64 {
	return f.den
}

// Add adds another fraction to this one.
//
// Parameters:
//   - other: The fraction to add.
//
// Returns:
//   - The sum of the two fractions.
//
// Example:
//
//     a, _ := New(1, 2)
//     b, _ := New(1, 3)
//     c := a.Add(b)  // Returns 5/6
func (f Fraction) Add(other Fraction) Fraction {
	// a/b + c/d = (ad + bc) / bd
	num := f.num*other.den + other.num*f.den
	den := f.den * other.den
	result, _ := New(num, den)
	return result
}

// Subtract subtracts another fraction from this one.
//
// Parameters:
//   - other: The fraction to subtract.
//
// Returns:
//   - The difference of the two fractions.
//
// Example:
//
//     a, _ := New(1, 2)
//     b, _ := New(1, 3)
//     c := a.Subtract(b)  // Returns 1/6
func (f Fraction) Subtract(other Fraction) Fraction {
	// a/b - c/d = (ad - bc) / bd
	num := f.num*other.den - other.num*f.den
	den := f.den * other.den
	result, _ := New(num, den)
	return result
}

// Multiply multiplies this fraction by another.
//
// Parameters:
//   - other: The fraction to multiply by.
//
// Returns:
//   - The product of the two fractions.
//
// Example:
//
//     a, _ := New(1, 2)
//     b, _ := New(2, 3)
//     c := a.Multiply(b)  // Returns 1/3
func (f Fraction) Multiply(other Fraction) Fraction {
	// a/b * c/d = ac / bd
	num := f.num * other.num
	den := f.den * other.den
	result, _ := New(num, den)
	return result
}

// Divide divides this fraction by another.
// Returns an error if dividing by zero.
//
// Parameters:
//   - other: The fraction to divide by.
//
// Returns:
//   - The quotient of the two fractions.
//   - An error if the other fraction is zero.
//
// Example:
//
//     a, _ := New(1, 2)
//     b, _ := New(2, 3)
//     c, _ := a.Divide(b)  // Returns 3/4
func (f Fraction) Divide(other Fraction) (Fraction, error) {
	if other.num == 0 {
		return Fraction{}, ErrDivisionByZero
	}
	// a/b ÷ c/d = a/b * d/c = ad / bc
	num := f.num * other.den
	den := f.den * other.num
	return New(num, den)
}

// Negate returns the negation of the fraction.
//
// Example:
//
//     a, _ := New(1, 2)
//     b := a.Negate()  // Returns -1/2
func (f Fraction) Negate() Fraction {
	return Fraction{num: -f.num, den: f.den}
}

// Reciprocal returns the reciprocal (inverse) of the fraction.
// Returns an error if the fraction is zero.
//
// Example:
//
//     a, _ := New(2, 3)
//     b, _ := a.Reciprocal()  // Returns 3/2
func (f Fraction) Reciprocal() (Fraction, error) {
	if f.num == 0 {
		return Fraction{}, ErrDivisionByZero
	}
	return New(f.den, f.num)
}

// Abs returns the absolute value of the fraction.
//
// Example:
//
//     a, _ := New(-3, 4)
//     b := a.Abs()  // Returns 3/4
func (f Fraction) Abs() Fraction {
	if f.num < 0 {
		return Fraction{num: -f.num, den: f.den}
	}
	return f
}

// Sign returns the sign of the fraction: -1, 0, or 1.
//
// Example:
//
//     a, _ := New(-3, 4)
//     s := a.Sign()  // Returns -1
func (f Fraction) Sign() int {
	if f.num < 0 {
		return -1
	}
	if f.num > 0 {
		return 1
	}
	return 0
}

// Compare compares this fraction with another.
// Returns -1 if f < other, 0 if f == other, 1 if f > other.
//
// Example:
//
//     a, _ := New(1, 2)
//     b, _ := New(1, 3)
//     cmp := a.Compare(b)  // Returns 1 (1/2 > 1/3)
func (f Fraction) Compare(other Fraction) int {
	// a/b ? c/d  =>  ad ? bc
	left := f.num * other.den
	right := other.num * f.den
	if left < right {
		return -1
	}
	if left > right {
		return 1
	}
	return 0
}

// Equal checks if two fractions are equal.
func (f Fraction) Equal(other Fraction) bool {
	return f.Compare(other) == 0
}

// LessThan checks if this fraction is less than another.
func (f Fraction) LessThan(other Fraction) bool {
	return f.Compare(other) < 0
}

// GreaterThan checks if this fraction is greater than another.
func (f Fraction) GreaterThan(other Fraction) bool {
	return f.Compare(other) > 0
}

// LessOrEqual checks if this fraction is less than or equal to another.
func (f Fraction) LessOrEqual(other Fraction) bool {
	return f.Compare(other) <= 0
}

// GreaterOrEqual checks if this fraction is greater than or equal to another.
func (f Fraction) GreaterOrEqual(other Fraction) bool {
	return f.Compare(other) >= 0
}

// Float64 returns the fraction as a float64.
//
// Example:
//
//     f, _ := New(1, 4)
//     x := f.Float64()  // Returns 0.25
func (f Fraction) Float64() float64 {
	return float64(f.num) / float64(f.den)
}

// ToInt returns the fraction truncated to an integer.
//
// Example:
//
//     f, _ := New(7, 3)
//     n := f.ToInt()  // Returns 2
func (f Fraction) ToInt() int64 {
	return f.num / f.den
}

// String returns the string representation of the fraction.
// If the fraction is a whole number, returns just the numerator.
//
// Example:
//
//     f, _ := New(3, 4)
//     s := f.String()  // Returns "3/4"
//     
//     g, _ := New(5, 1)
//     t := g.String()  // Returns "5"
func (f Fraction) String() string {
	if f.den == 1 {
		return strconv.FormatInt(f.num, 10)
	}
	return fmt.Sprintf("%d/%d", f.num, f.den)
}

// ToMixed returns the fraction as a mixed number string.
//
// Example:
//
//     f, _ := New(7, 4)
//     s := f.ToMixed()  // Returns "1 3/4"
//     
//     g, _ := New(3, 4)
//     t := g.ToMixed()  // Returns "3/4"
func (f Fraction) ToMixed() string {
	if abs(f.num) < f.den {
		return f.String()
	}

	whole := f.num / f.den
	remainder := abs(f.num % f.den)

	if remainder == 0 {
		return strconv.FormatInt(whole, 10)
	}

	if whole < 0 {
		return fmt.Sprintf("%d %d/%d", whole, remainder, f.den)
	}
	return fmt.Sprintf("%d %d/%d", whole, remainder, f.den)
}

// Pow raises the fraction to an integer power.
//
// Parameters:
//   - n: The exponent (can be negative).
//
// Returns:
//   - The fraction raised to the power n.
//   - An error if the base is zero and exponent is negative.
//
// Example:
//
//     f, _ := New(2, 3)
//     g, _ := f.Pow(2)   // Returns 4/9
//     h, _ := f.Pow(-1)  // Returns 3/2
func (f Fraction) Pow(n int) (Fraction, error) {
	if n == 0 {
		return FromInt(1), nil
	}

	if n < 0 {
		if f.num == 0 {
			return Fraction{}, ErrDivisionByZero
		}
		recip, err := f.Reciprocal()
		if err != nil {
			return Fraction{}, err
		}
		return recip.Pow(-n)
	}

	result := FromInt(1)
	base := f
	for n > 0 {
		if n%2 == 1 {
			result = result.Multiply(base)
		}
		base = base.Multiply(base)
		n /= 2
	}
	return result, nil
}

// Sqrt computes the square root of a fraction if it's a perfect square.
// Returns the exact square root if it exists, otherwise an error.
//
// Example:
//
//     f, _ := New(9, 16)
//     g, err := f.Sqrt()  // Returns 3/4, nil
func (f Fraction) Sqrt() (Fraction, error) {
	if f.num < 0 {
		return Fraction{}, errors.New("cannot compute square root of negative fraction")
	}

	numSqrt := int64(math.Sqrt(float64(f.num)))
	denSqrt := int64(math.Sqrt(float64(f.den)))

	if numSqrt*numSqrt == f.num && denSqrt*denSqrt == f.den {
		return New(numSqrt, denSqrt)
	}

	return Fraction{}, errors.New("fraction is not a perfect square")
}

// IsZero returns true if the fraction equals zero.
func (f Fraction) IsZero() bool {
	return f.num == 0
}

// IsInteger returns true if the fraction is a whole number.
func (f Fraction) IsInteger() bool {
	return f.den == 1
}

// IsPositive returns true if the fraction is positive.
func (f Fraction) IsPositive() bool {
	return f.num > 0
}

// IsNegative returns true if the fraction is negative.
func (f Fraction) IsNegative() bool {
	return f.num < 0
}

// Min returns the smaller of two fractions.
func Min(a, b Fraction) Fraction {
	if a.Compare(b) <= 0 {
		return a
	}
	return b
}

// Max returns the larger of two fractions.
func Max(a, b Fraction) Fraction {
	if a.Compare(b) >= 0 {
		return a
	}
	return b
}

// Sum returns the sum of multiple fractions.
//
// Example:
//
//     f1, _ := New(1, 4)
//     f2, _ := New(1, 3)
//     f3, _ := New(1, 2)
//     total := Sum(f1, f2, f3)  // Returns 13/12
func Sum(fractions ...Fraction) Fraction {
	result := FromInt(0)
	for _, f := range fractions {
		result = result.Add(f)
	}
	return result
}

// Product returns the product of multiple fractions.
//
// Example:
//
//     f1, _ := New(1, 2)
//     f2, _ := New(2, 3)
//     f3, _ := New(3, 4)
//     prod := Product(f1, f2, f3)  // Returns 1/4
func Product(fractions ...Fraction) Fraction {
	result := FromInt(1)
	for _, f := range fractions {
		result = result.Multiply(f)
	}
	return result
}

// Common Denominator Operations

// LCM computes the least common multiple of two integers.
func lcm(a, b int64) int64 {
	return abs(a*b) / gcd(a, b)
}

// GCD computes the greatest common divisor of two integers.
func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

// CommonDenominator returns a new fraction with the specified denominator.
// Returns an error if the conversion would not be exact.
//
// Example:
//
//     f, _ := New(1, 2)
//     g, _ := f.CommonDenominator(8)  // Returns 4/8
func (f Fraction) CommonDenominator(newDen int64) (Fraction, error) {
	if newDen <= 0 {
		return Fraction{}, errors.New("denominator must be positive")
	}

	if f.den == newDen {
		return f, nil
	}

	if newDen%f.den != 0 {
		return Fraction{}, errors.New("cannot convert to exact fraction with given denominator")
	}

	multiplier := newDen / f.den
	return New(f.num*multiplier, newDen)
}

// WithCommonDenominator returns both fractions with a common denominator.
//
// Example:
//
//     a, _ := New(1, 3)
//     b, _ := New(1, 4)
//     a2, b2 := WithCommonDenominator(a, b)  // a2 = 4/12, b2 = 3/12
func WithCommonDenominator(a, b Fraction) (Fraction, Fraction) {
	commonDen := lcm(a.den, b.den)
	aNum := a.num * (commonDen / a.den)
	bNum := b.num * (commonDen / b.den)
	return Fraction{num: aNum, den: commonDen}, Fraction{num: bNum, den: commonDen}
}

// Common fractions as constants
var (
	Zero   = Fraction{num: 0, den: 1}
	One    = Fraction{num: 1, den: 1}
	Half   = Fraction{num: 1, den: 2}
	Third  = Fraction{num: 1, den: 3}
	Quarter = Fraction{num: 1, den: 4}
	Fifth   = Fraction{num: 1, den: 5}
)

// Ratio creates a fraction representing a ratio of two integers.
// Shorthand for New().
//
// Example:
//
//     f := Ratio(3, 4)  // Returns 3/4
func Ratio(num, den int64) Fraction {
	f, _ := New(num, den)
	return f
}