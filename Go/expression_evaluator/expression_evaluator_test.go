package expression_evaluator

import (
	"math"
	"testing"
)

func TestBasicArithmetic(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"2 + 3", 5},
		{"10 - 4", 6},
		{"3 * 4", 12},
		{"20 / 4", 5},
		{"2 ^ 3", 8},
		{"10 % 3", 1},
		{"2 + 3 * 4", 14},
		{"(2 + 3) * 4", 20},
		{"10 - 2 - 3", 5},
		{"2 * 3 + 4", 10},
		{"2 + 3 * 4 - 5", 9},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestOperatorPrecedence(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"2 + 3 * 4", 14},
		{"2 * 3 + 4", 10},
		{"10 - 2 * 3", 4},
		{"2 ^ 3 ^ 2", 512}, // Right associative: 2^(3^2) = 2^9 = 512
		{"(2 ^ 3) ^ 2", 64},
		{"10 / 2 * 5", 25},
		{"10 * 5 / 2", 25},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestParentheses(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"(2 + 3)", 5},
		{"((2 + 3))", 5},
		{"(2 + 3) * (4 - 1)", 15},
		{"((2 + 3) * 4)", 20},
		{"2 * (3 + 4)", 14},
		{"((1 + 2) * (3 + 4))", 21},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestBuiltInFunctions(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"sqrt(16)", 4},
		{"abs(-5)", 5},
		{"floor(3.7)", 3},
		{"ceil(3.2)", 4},
		{"round(3.5)", 4},
		{"sin(0)", 0},
		{"cos(0)", 1},
		{"log(e)", 1},
		{"log10(100)", 2},
		{"log2(8)", 3},
		{"exp(0)", 1},
		{"cbrt(27)", 3},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestMultiArgFunctions(t *testing.T) {
	e := New()

	// Test min/max
	result, err := e.Evaluate("min(3, 1, 2)")
	if err != nil || result != 1 {
		t.Errorf("min(3, 1, 2) = %f, expected 1, err: %v", result, err)
	}

	result, err = e.Evaluate("max(3, 1, 2)")
	if err != nil || result != 3 {
		t.Errorf("max(3, 1, 2) = %f, expected 3, err: %v", result, err)
	}

	result, err = e.Evaluate("avg(10, 20, 30)")
	if err != nil || result != 20 {
		t.Errorf("avg(10, 20, 30) = %f, expected 20, err: %v", result, err)
	}
}

func TestVariables(t *testing.T) {
	e := New()
	e.SetVariable("x", 10)
	e.SetVariable("y", 5)

	tests := []struct {
		expr     string
		expected float64
	}{
		{"x + y", 15},
		{"x * y", 50},
		{"x - y", 5},
		{"x / y", 2},
		{"x ^ 2", 100},
		{"sqrt(x * y)", math.Sqrt(50)},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestConstants(t *testing.T) {
	e := New()

	// Test built-in constants
	piVal, ok := e.GetVariable("pi")
	if !ok || piVal != math.Pi {
		t.Errorf("pi constant not set correctly")
	}

	eVal, ok := e.GetVariable("e")
	if !ok || eVal != math.E {
		t.Errorf("e constant not set correctly")
	}

	// Use in expressions
	result, err := e.Evaluate("sin(pi)")
	if err != nil || math.Abs(result) > 1e-10 {
		t.Errorf("sin(pi) = %f, expected 0, err: %v", result, err)
	}
}

func TestComplexExpressions(t *testing.T) {
	e := New()
	e.SetVariable("x", 5)

	tests := []struct {
		expr     string
		expected float64
	}{
		{"2 * (3 + 4) - 5", 9},
		{"(1 + 2) * (3 + 4) / 7", 3},
		{"sqrt(16) + abs(-3)", 7},
		{"x * 2 + 10", 20},
		{"(x + 5) * 2", 20},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestUnaryMinus(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"-5", -5},
		{"-(-5)", 5},
		{"-5 + 10", 5},
		{"10 - -5", 15},
		{"abs(-10)", 10},
		{"-2 * 3", -6},
		{"2 * -3", -6},
		{"-sqrt(16)", -4},
		{"-x", -10}, // with variable
	}

	e.SetVariable("x", 10)

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestUnaryPlus(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"+5", 5},
		{"+5 + 10", 15},
		{"10 + +5", 15},
		{"+(2 * 3)", 6},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestDecimalNumbers(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"0.5 + 0.5", 1},
		{"3.14 * 2", 6.28},
		{"10.5 / 2", 5.25},
		{"sqrt(2.25)", 1.5},
		{"0.1 + 0.2", 0.3},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		// Use larger tolerance for floating point
		if math.Abs(result-test.expected) > 1e-9 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestWhitespaceHandling(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"2+3", 5},
		{"2 + 3", 5},
		{"  2  +  3  ", 5},
		{"2+3*4", 14},
		{"2 + 3 * 4", 14},
		{"  sqrt(  16  )  ", 4},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestErrorHandling(t *testing.T) {
	e := New()

	// Test undefined variable
	_, err := e.Evaluate("x + 1")
	if err == nil {
		t.Error("Expected error for undefined variable")
	}

	// Test mismatched parentheses
	_, err = e.Evaluate("(2 + 3")
	if err == nil {
		t.Error("Expected error for mismatched parentheses")
	}

	// Test empty expression
	_, err = e.Evaluate("")
	if err == nil {
		t.Error("Expected error for empty expression")
	}

	// Test unknown function
	_, err = e.Evaluate("unknown_func(5)")
	if err == nil {
		t.Error("Expected error for unknown function")
	}
}

func TestCustomFunction(t *testing.T) {
	e := New()

	// Register a custom function
	e.RegisterFunction1("double", func(x float64) float64 {
		return x * 2
	})

	result, err := e.Evaluate("double(5)")
	if err != nil {
		t.Errorf("Error evaluating double(5): %v", err)
	}
	if result != 10 {
		t.Errorf("double(5) = %f, expected 10", result)
	}
}

func TestNestedFunctions(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"sqrt(abs(-16))", 4},
		{"sin(cos(0))", math.Sin(1)},
		{"max(min(5, 10), min(3, 7))", 5},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func TestEvaluateAsString(t *testing.T) {
	e := New()

	result, err := e.EvaluateAsString("2 + 3")
	if err != nil {
		t.Errorf("Error: %v", err)
	}
	if result != "5" {
		t.Errorf("EvaluateAsString returned %s, expected 5", result)
	}
}

func TestIsExpressionValid(t *testing.T) {
	e := New()

	if !e.IsExpressionValid("2 + 3") {
		t.Error("2 + 3 should be valid")
	}

	if e.IsExpressionValid("x + 1") {
		t.Error("x + 1 should be invalid (undefined variable)")
	}

	if e.IsExpressionValid("") {
		t.Error("empty expression should be invalid")
	}
}

func TestGetSupportedFunctions(t *testing.T) {
	e := New()
	fns := e.GetSupportedFunctions()

	if len(fns) == 0 {
		t.Error("Should have at least one function")
	}
}

func TestClearVariables(t *testing.T) {
	e := New()
	e.SetVariable("custom", 42)

	val, ok := e.GetVariable("custom")
	if !ok || val != 42 {
		t.Error("custom variable should be 42")
	}

	e.ClearVariables()

	_, ok = e.GetVariable("custom")
	if ok {
		t.Error("custom variable should be cleared")
	}

	// Constants should still exist
	_, ok = e.GetVariable("pi")
	if !ok {
		t.Error("pi constant should still exist")
	}
}

func TestDivisionByZero(t *testing.T) {
	e := New()

	_, err := e.Evaluate("10 / 0")
	if err == nil {
		t.Error("Expected error for division by zero")
	}
}

func TestNestedParentheses(t *testing.T) {
	e := New()

	tests := []struct {
		expr     string
		expected float64
	}{
		{"((2 + 3) * (4 - 1))", 15},
		{"(((2)))", 2},
		{"((((2 + 3) * 4) - 5) / 3)", 5},
	}

	for _, test := range tests {
		result, err := e.Evaluate(test.expr)
		if err != nil {
			t.Errorf("Error evaluating %s: %v", test.expr, err)
			continue
		}
		if math.Abs(result-test.expected) > 1e-10 {
			t.Errorf("%s = %f, expected %f", test.expr, result, test.expected)
		}
	}
}

func BenchmarkEvaluate(b *testing.B) {
	e := New()
	e.SetVariable("x", 10)

	for i := 0; i < b.N; i++ {
		_, _ = e.Evaluate("x * 2 + sqrt(16) - 5")
	}
}

func BenchmarkEvaluateComplex(b *testing.B) {
	e := New()
	e.SetVariable("x", 10)
	e.SetVariable("y", 20)

	for i := 0; i < b.N; i++ {
		_, _ = e.Evaluate("(x + y) * 2 + sqrt(x * y) - abs(-5)")
	}
}