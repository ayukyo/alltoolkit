package fractionutils

import (
	"math"
	"testing"
)

func TestNew(t *testing.T) {
	tests := []struct {
		name        string
		num, den    int64
		wantNum     int64
		wantDen     int64
		wantErr     bool
	}{
		{"simple", 1, 2, 1, 2, false},
		{"reduce", 6, 8, 3, 4, false},
		{"negative num", -3, 4, -3, 4, false},
		{"negative den", 3, -4, -3, 4, false},
		{"both negative", -3, -4, 3, 4, false},
		{"zero numerator", 0, 5, 0, 1, false},
		{"zero denominator", 1, 0, 0, 0, true},
		{"whole number", 8, 4, 2, 1, false},
		{"large numbers", 1000000, 500000, 2, 1, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, err := New(tt.num, tt.den)
			if (err != nil) != tt.wantErr {
				t.Errorf("New(%d, %d) error = %v, wantErr %v", tt.num, tt.den, err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if f.num != tt.wantNum || f.den != tt.wantDen {
					t.Errorf("New(%d, %d) = %d/%d, want %d/%d", tt.num, tt.den, f.num, f.den, tt.wantNum, tt.wantDen)
				}
			}
		})
	}
}

func TestFromInt(t *testing.T) {
	tests := []struct {
		name string
		n    int64
		want Fraction
	}{
		{"positive", 5, Fraction{5, 1}},
		{"negative", -3, Fraction{-3, 1}},
		{"zero", 0, Fraction{0, 1}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f := FromInt(tt.n)
			if f != tt.want {
				t.Errorf("FromInt(%d) = %v, want %v", tt.n, f, tt.want)
			}
		})
	}
}

func TestFromFloat(t *testing.T) {
	tests := []struct {
		name          string
		x             float64
		maxDen        int64
		wantFloat     float64
		tolerance     float64
	}{
		{"simple", 0.5, 100, 0.5, 0.0001},
		{"third", 1.0 / 3.0, 100, 1.0 / 3.0, 0.0001},
		{"pi approximation", 3.14159, 100, 3.142857, 0.01},
		{"negative", -0.75, 100, -0.75, 0.0001},
		{"zero", 0, 100, 0, 0.0001},
		{"small", 0.001, 1000, 0.001, 0.0001},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f := FromFloat(tt.x, tt.maxDen)
			got := f.Float64()
			if math.Abs(got-tt.wantFloat) > tt.tolerance {
				t.Errorf("FromFloat(%v, %d).Float64() = %v, want ~%v", tt.x, tt.maxDen, got, tt.wantFloat)
			}
		})
	}
}

func TestParse(t *testing.T) {
	tests := []struct {
		name    string
		s       string
		wantNum int64
		wantDen int64
		wantErr bool
	}{
		{"fraction", "3/4", 3, 4, false},
		{"negative fraction", "-5/6", -5, 6, false},
		{"integer", "7", 7, 1, false},
		{"negative integer", "-3", -3, 1, false},
		{"decimal", "0.5", 1, 2, false},
		{"negative decimal", "-0.25", -1, 4, false},
		{"invalid", "abc", 0, 0, true},
		{"empty", "", 0, 0, true},
		{"invalid fraction", "1/0", 0, 0, true},
		{"spaced fraction", " 3 / 4 ", 3, 4, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, err := Parse(tt.s)
			if (err != nil) != tt.wantErr {
				t.Errorf("Parse(%q) error = %v, wantErr %v", tt.s, err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if f.num != tt.wantNum || f.den != tt.wantDen {
					t.Errorf("Parse(%q) = %d/%d, want %d/%d", tt.s, f.num, f.den, tt.wantNum, tt.wantDen)
				}
			}
		})
	}
}

func TestAdd(t *testing.T) {
	tests := []struct {
		name            string
		aNum, aDen      int64
		bNum, bDen      int64
		wantNum, wantDen int64
	}{
		{"simple", 1, 2, 1, 3, 5, 6},
		{"same denominator", 1, 4, 2, 4, 3, 4},
		{"zero", 0, 1, 3, 4, 3, 4},
		{"negative", 1, 2, -1, 4, 1, 4},
		{"whole result", 1, 4, 3, 4, 1, 1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			a, _ := New(tt.aNum, tt.aDen)
			b, _ := New(tt.bNum, tt.bDen)
			got := a.Add(b)
			if got.num != tt.wantNum || got.den != tt.wantDen {
				t.Errorf("Add() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
			}
		})
	}
}

func TestSubtract(t *testing.T) {
	tests := []struct {
		name            string
		aNum, aDen      int64
		bNum, bDen      int64
		wantNum, wantDen int64
	}{
		{"simple", 1, 2, 1, 3, 1, 6},
		{"same denominator", 3, 4, 1, 4, 1, 2},
		{"zero result", 1, 2, 1, 2, 0, 1},
		{"negative result", 1, 4, 1, 2, -1, 4},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			a, _ := New(tt.aNum, tt.aDen)
			b, _ := New(tt.bNum, tt.bDen)
			got := a.Subtract(b)
			if got.num != tt.wantNum || got.den != tt.wantDen {
				t.Errorf("Subtract() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
			}
		})
	}
}

func TestMultiply(t *testing.T) {
	tests := []struct {
		name            string
		aNum, aDen      int64
		bNum, bDen      int64
		wantNum, wantDen int64
	}{
		{"simple", 1, 2, 2, 3, 1, 3},
		{"cancel", 2, 5, 5, 2, 1, 1},
		{"zero", 0, 1, 3, 4, 0, 1},
		{"negative", -1, 2, 2, 3, -1, 3},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			a, _ := New(tt.aNum, tt.aDen)
			b, _ := New(tt.bNum, tt.bDen)
			got := a.Multiply(b)
			if got.num != tt.wantNum || got.den != tt.wantDen {
				t.Errorf("Multiply() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
			}
		})
	}
}

func TestDivide(t *testing.T) {
	tests := []struct {
		name            string
		aNum, aDen      int64
		bNum, bDen      int64
		wantNum, wantDen int64
		wantErr         bool
	}{
		{"simple", 1, 2, 2, 3, 3, 4, false},
		{"inverse", 3, 4, 1, 1, 3, 4, false},
		{"divide by zero", 1, 2, 0, 1, 0, 0, true},
		{"negative", -1, 2, 2, 3, -3, 4, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			a, _ := New(tt.aNum, tt.aDen)
			b, _ := New(tt.bNum, tt.bDen)
			got, err := a.Divide(b)
			if (err != nil) != tt.wantErr {
				t.Errorf("Divide() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if got.num != tt.wantNum || got.den != tt.wantDen {
					t.Errorf("Divide() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
				}
			}
		})
	}
}

func TestCompare(t *testing.T) {
	tests := []struct {
		name       string
		aNum, aDen int64
		bNum, bDen int64
		want       int
	}{
		{"equal", 1, 2, 2, 4, 0},
		{"less", 1, 3, 1, 2, -1},
		{"greater", 1, 2, 1, 3, 1},
		{"negative compare", -1, 2, 1, 2, -1},
		{"both negative", -1, 2, -1, 3, -1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			a, _ := New(tt.aNum, tt.aDen)
			b, _ := New(tt.bNum, tt.bDen)
			if got := a.Compare(b); got != tt.want {
				t.Errorf("Compare() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestFloat64(t *testing.T) {
	tests := []struct {
		name    string
		num, den int64
		want    float64
	}{
		{"one half", 1, 2, 0.5},
		{"one third", 1, 3, 1.0 / 3.0},
		{"two thirds", 2, 3, 2.0 / 3.0},
		{"negative", -3, 4, -0.75},
		{"zero", 0, 1, 0},
		{"whole", 5, 1, 5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			if got := f.Float64(); math.Abs(got-tt.want) > 1e-10 {
				t.Errorf("Float64() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestString(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		want       string
	}{
		{"simple", 3, 4, "3/4"},
		{"negative", -5, 6, "-5/6"},
		{"whole", 5, 1, "5"},
		{"negative whole", -3, 1, "-3"},
		{"zero", 0, 1, "0"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			if got := f.String(); got != tt.want {
				t.Errorf("String() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestToMixed(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		want       string
	}{
		{"proper fraction", 3, 4, "3/4"},
		{"improper fraction", 7, 4, "1 3/4"},
		{"whole number", 8, 4, "2"},
		{"negative improper", -7, 4, "-1 3/4"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			if got := f.ToMixed(); got != tt.want {
				t.Errorf("ToMixed() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestPow(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		pow        int
		wantNum    int64
		wantDen    int64
		wantErr    bool
	}{
		{"square", 2, 3, 2, 4, 9, false},
		{"cube", 1, 2, 3, 1, 8, false},
		{"zero power", 3, 4, 0, 1, 1, false},
		{"negative power", 2, 3, -1, 3, 2, false},
		{"negative power 2", 2, 3, -2, 9, 4, false},
		{"zero base negative power", 0, 1, -1, 0, 0, true},
		{"one", 1, 1, 100, 1, 1, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			got, err := f.Pow(tt.pow)
			if (err != nil) != tt.wantErr {
				t.Errorf("Pow() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if got.num != tt.wantNum || got.den != tt.wantDen {
					t.Errorf("Pow() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
				}
			}
		})
	}
}

func TestSqrt(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		wantNum    int64
		wantDen    int64
		wantErr    bool
	}{
		{"perfect square", 9, 16, 3, 4, false},
		{"non-perfect square", 2, 1, 0, 0, true},
		{"negative", -1, 1, 0, 0, true},
		{"whole square", 4, 1, 2, 1, false},
		{"one", 1, 1, 1, 1, false},
		{"zero", 0, 1, 0, 1, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			got, err := f.Sqrt()
			if (err != nil) != tt.wantErr {
				t.Errorf("Sqrt() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if got.num != tt.wantNum || got.den != tt.wantDen {
					t.Errorf("Sqrt() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
				}
			}
		})
	}
}

func TestNegate(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		wantNum    int64
		wantDen    int64
	}{
		{"positive", 1, 2, -1, 2},
		{"negative", -3, 4, 3, 4},
		{"zero", 0, 1, 0, 1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			got := f.Negate()
			if got.num != tt.wantNum || got.den != tt.wantDen {
				t.Errorf("Negate() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
			}
		})
	}
}

func TestReciprocal(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		wantNum    int64
		wantDen    int64
		wantErr    bool
	}{
		{"simple", 2, 3, 3, 2, false},
		{"negative", -3, 4, -4, 3, false},
		{"one", 1, 1, 1, 1, false},
		{"zero", 0, 1, 0, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			got, err := f.Reciprocal()
			if (err != nil) != tt.wantErr {
				t.Errorf("Reciprocal() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if got.num != tt.wantNum || got.den != tt.wantDen {
					t.Errorf("Reciprocal() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
				}
			}
		})
	}
}

func TestAbs(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		wantNum    int64
		wantDen    int64
	}{
		{"positive", 3, 4, 3, 4},
		{"negative", -3, 4, 3, 4},
		{"zero", 0, 1, 0, 1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			got := f.Abs()
			if got.num != tt.wantNum || got.den != tt.wantDen {
				t.Errorf("Abs() = %d/%d, want %d/%d", got.num, got.den, tt.wantNum, tt.wantDen)
			}
		})
	}
}

func TestSign(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		want       int
	}{
		{"positive", 3, 4, 1},
		{"negative", -3, 4, -1},
		{"zero", 0, 1, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			if got := f.Sign(); got != tt.want {
				t.Errorf("Sign() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestIsMethods(t *testing.T) {
	tests := []struct {
		name       string
		num, den   int64
		isZero     bool
		isInt      bool
		isPos      bool
		isNeg      bool
	}{
		{"zero", 0, 1, true, true, false, false},
		{"positive int", 5, 1, false, true, true, false},
		{"negative int", -3, 1, false, true, false, true},
		{"positive fraction", 1, 2, false, false, true, false},
		{"negative fraction", -1, 2, false, false, false, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			f, _ := New(tt.num, tt.den)
			if f.IsZero() != tt.isZero {
				t.Errorf("IsZero() = %v, want %v", f.IsZero(), tt.isZero)
			}
			if f.IsInteger() != tt.isInt {
				t.Errorf("IsInteger() = %v, want %v", f.IsInteger(), tt.isInt)
			}
			if f.IsPositive() != tt.isPos {
				t.Errorf("IsPositive() = %v, want %v", f.IsPositive(), tt.isPos)
			}
			if f.IsNegative() != tt.isNeg {
				t.Errorf("IsNegative() = %v, want %v", f.IsNegative(), tt.isNeg)
			}
		})
	}
}

func TestSum(t *testing.T) {
	f1, _ := New(1, 4)
	f2, _ := New(1, 3)
	f3, _ := New(1, 2)
	
	got := Sum(f1, f2, f3)
	want, _ := New(13, 12)
	
	if !got.Equal(want) {
		t.Errorf("Sum() = %v, want %v", got, want)
	}
}

func TestProduct(t *testing.T) {
	f1, _ := New(1, 2)
	f2, _ := New(2, 3)
	f3, _ := New(3, 4)
	
	got := Product(f1, f2, f3)
	want, _ := New(1, 4)
	
	if !got.Equal(want) {
		t.Errorf("Product() = %v, want %v", got, want)
	}
}

func TestMin(t *testing.T) {
	a, _ := New(1, 3)
	b, _ := New(1, 2)
	
	got := Min(a, b)
	if !got.Equal(a) {
		t.Errorf("Min() = %v, want %v", got, a)
	}
}

func TestMax(t *testing.T) {
	a, _ := New(1, 3)
	b, _ := New(1, 2)
	
	got := Max(a, b)
	if !got.Equal(b) {
		t.Errorf("Max() = %v, want %v", got, b)
	}
}

func TestWithCommonDenominator(t *testing.T) {
	a, _ := New(1, 3)
	b, _ := New(1, 4)
	
	a2, b2 := WithCommonDenominator(a, b)
	
	// Should have common denominator of 12
	if a2.den != b2.den {
		t.Errorf("WithCommonDenominator() produced different denominators: %d and %d", a2.den, b2.den)
	}
	
	// Values should be preserved
	if !a2.Equal(a) {
		t.Errorf("a2 changed value from %v to %v", a, a2)
	}
	if !b2.Equal(b) {
		t.Errorf("b2 changed value from %v to %v", b, b2)
	}
}

func TestConstants(t *testing.T) {
	if !Zero.IsZero() {
		t.Error("Zero constant is not zero")
	}
	if !One.Equal(FromInt(1)) {
		t.Error("One constant is not 1")
	}
	if !Half.Equal(Ratio(1, 2)) {
		t.Error("Half constant is not 1/2")
	}
	if !Third.Equal(Ratio(1, 3)) {
		t.Error("Third constant is not 1/3")
	}
	if !Quarter.Equal(Ratio(1, 4)) {
		t.Error("Quarter constant is not 1/4")
	}
	if !Fifth.Equal(Ratio(1, 5)) {
		t.Error("Fifth constant is not 1/5")
	}
}

func TestChainOperations(t *testing.T) {
	// Test: (1/2 + 1/3) * (3/4 - 1/4) / (2/5)
	a, _ := New(1, 2)
	b, _ := New(1, 3)
	c, _ := New(3, 4)
	d, _ := New(1, 4)
	e, _ := New(2, 5)

	sum := a.Add(b)                    // 5/6
	diff := c.Subtract(d)              // 1/2
	product := sum.Multiply(diff)       // 5/12
	result, err := product.Divide(e)    // 25/24

	if err != nil {
		t.Fatalf("Chain operations error: %v", err)
	}

	expected, _ := New(25, 24)
	if !result.Equal(expected) {
		t.Errorf("Chain operations = %v, want %v", result, expected)
	}
}

func TestEdgeCases(t *testing.T) {
	// Very large numbers
	f1, err := New(1000000000, 2000000000)
	if err != nil {
		t.Fatalf("New with large numbers error: %v", err)
	}
	if f1.num != 1 || f1.den != 2 {
		t.Errorf("Large number reduction: got %d/%d, want 1/2", f1.num, f1.den)
	}

	// Float conversion precision
	f2 := FromFloat(0.1, 1000)
	expected := 0.1
	if math.Abs(f2.Float64()-expected) > 1e-10 {
		t.Errorf("Float precision: got %v, want ~%v", f2.Float64(), expected)
	}
}

// Benchmark tests
func BenchmarkNew(b *testing.B) {
	for i := 0; i < b.N; i++ {
		New(12345, 67890)
	}
}

func BenchmarkAdd(b *testing.B) {
	f1, _ := New(1, 2)
	f2, _ := New(1, 3)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		f1.Add(f2)
	}
}

func BenchmarkMultiply(b *testing.B) {
	f1, _ := New(1, 2)
	f2, _ := New(2, 3)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		f1.Multiply(f2)
	}
}

func BenchmarkDivide(b *testing.B) {
	f1, _ := New(1, 2)
	f2, _ := New(2, 3)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		f1.Divide(f2)
	}
}

func BenchmarkParse(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Parse("123/456")
	}
}