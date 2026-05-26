package stack_utils

import (
	"strings"
	"testing"
)

// TestStack tests basic stack operations
func TestStack(t *testing.T) {
	s := NewStack[int]()
	if !s.IsEmpty() {
		t.Error("New stack should be empty")
	}
	if s.Size() != 0 {
		t.Error("New stack should have size 0")
	}

	s.Push(1)
	s.Push(2)
	s.Push(3)

	if s.Size() != 3 {
		t.Errorf("Expected size 3, got %d", s.Size())
	}

	item, err := s.Peek()
	if err != nil || item != 3 {
		t.Errorf("Expected peek 3, got %d, err: %v", item, err)
	}

	item, err = s.Pop()
	if err != nil || item != 3 {
		t.Errorf("Expected pop 3, got %d, err: %v", item, err)
	}

	item, err = s.Pop()
	if err != nil || item != 2 {
		t.Errorf("Expected pop 2, got %d, err: %v", item, err)
	}

	item, err = s.Pop()
	if err != nil || item != 1 {
		t.Errorf("Expected pop 1, got %d, err: %v", item, err)
	}

	_, err = s.Pop()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty, got %v", err)
	}
}

// TestStackString tests stack with strings
func TestStackString(t *testing.T) {
	s := NewStack[string]()
	s.Push("hello")
	s.Push("world")

	item, err := s.Pop()
	if err != nil || item != "world" {
		t.Errorf("Expected 'world', got '%s'", item)
	}

	item, err = s.Pop()
	if err != nil || item != "hello" {
		t.Errorf("Expected 'hello', got '%s'", item)
	}
}

// TestStackToSlice tests ToSlice and FromSlice
func TestStackToSlice(t *testing.T) {
	original := []int{1, 2, 3, 4, 5}
	s := FromSlice(original)

	result := s.ToSlice()
	if len(result) != len(original) {
		t.Errorf("Expected length %d, got %d", len(original), len(result))
	}

	for i := range original {
		if result[i] != original[i] {
			t.Errorf("Mismatch at index %d", i)
		}
	}
}

// TestStackClear tests Clear method
func TestStackClear(t *testing.T) {
	s := NewStack[int]()
	s.Push(1)
	s.Push(2)
	s.Push(3)

	s.Clear()
	if !s.IsEmpty() {
		t.Error("Stack should be empty after Clear")
	}
	if s.Size() != 0 {
		t.Errorf("Expected size 0 after Clear, got %d", s.Size())
	}
}

// TestBoundedStack tests bounded stack operations
func TestBoundedStack(t *testing.T) {
	s := NewBoundedStack[int](3)

	if !s.IsEmpty() {
		t.Error("New bounded stack should be empty")
	}
	if s.IsFull() {
		t.Error("New bounded stack should not be full")
	}

	// Push to capacity
	if err := s.Push(1); err != nil {
		t.Errorf("Push should succeed: %v", err)
	}
	if err := s.Push(2); err != nil {
		t.Errorf("Push should succeed: %v", err)
	}
	if err := s.Push(3); err != nil {
		t.Errorf("Push should succeed: %v", err)
	}

	if !s.IsFull() {
		t.Error("Stack should be full")
	}

	// Push beyond capacity
	if err := s.Push(4); err != ErrStackFull {
		t.Errorf("Expected ErrStackFull, got %v", err)
	}

	// Pop and check
	item, err := s.Pop()
	if err != nil || item != 3 {
		t.Errorf("Expected pop 3, got %d", item)
	}

	item, err = s.Peek()
	if err != nil || item != 2 {
		t.Errorf("Expected peek 2, got %d", item)
	}

	// Test capacity and size
	if s.Capacity() != 3 {
		t.Errorf("Expected capacity 3, got %d", s.Capacity())
	}
	if s.Size() != 2 {
		t.Errorf("Expected size 2, got %d", s.Size())
	}
}

// TestMinStack tests minimum stack operations
func TestMinStack(t *testing.T) {
	s := NewMinStack[int]()

	s.Push(5)
	s.Push(3)
	s.Push(7)
	s.Push(2)

	min, err := s.Min()
	if err != nil || min != 2 {
		t.Errorf("Expected min 2, got %d", min)
	}

	// Pop 2
	s.Pop()
	min, err = s.Min()
	if err != nil || min != 3 {
		t.Errorf("Expected min 3 after pop, got %d", min)
	}

	// Pop 7
	s.Pop()
	min, err = s.Min()
	if err != nil || min != 3 {
		t.Errorf("Expected min 3 after second pop, got %d", min)
	}

	// Pop 3
	s.Pop()
	min, err = s.Min()
	if err != nil || min != 5 {
		t.Errorf("Expected min 5 after third pop, got %d", min)
	}
}

// TestMaxStack tests maximum stack operations
func TestMaxStack(t *testing.T) {
	s := NewMaxStack[int]()

	s.Push(2)
	s.Push(7)
	s.Push(3)
	s.Push(5)

	max, err := s.Max()
	if err != nil || max != 7 {
		t.Errorf("Expected max 7, got %d", max)
	}

	// Pop 5
	s.Pop()
	max, err = s.Max()
	if err != nil || max != 7 {
		t.Errorf("Expected max 7 after pop, got %d", max)
	}

	// Pop 3
	s.Pop()
	max, err = s.Max()
	if err != nil || max != 7 {
		t.Errorf("Expected max 7 after second pop, got %d", max)
	}

	// Pop 7
	s.Pop()
	max, err = s.Max()
	if err != nil || max != 2 {
		t.Errorf("Expected max 2 after third pop, got %d", max)
	}
}

// TestIsBalancedParentheses tests parentheses balancing
func TestIsBalancedParentheses(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"()", true},
		{"[]", true},
		{"{}", true},
		{"()[]{}", true},
		{"([{}])", true},
		{"([)]", false},
		{"(((", false},
		{")))", false},
		{"{[()]}", true},
		{"{[(])}", false},
		{"", true},
		{"hello(world)", true},
		{"hello(world", false},
		{"[a,b,{c,d}]", true},
	}

	for _, tt := range tests {
		result := IsBalancedParentheses(tt.input)
		if result != tt.expected {
			t.Errorf("IsBalancedParentheses(%q) = %v, expected %v", tt.input, result, tt.expected)
		}
	}
}

// TestIsBalancedQuotes tests quote balancing
func TestIsBalancedQuotes(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{`""`, true},
		{"''", true},
		{`"hello"`, true},
		{`"hello`, false},
		{"'hello", false},
		{`"hello'world'"`, true}, // 2 double quotes, 2 single quotes
		{`"hel'lo"`, false},      // 2 double quotes, 1 single quote (unbalanced)
		{`""''`, true},
		{`"'`, false},
		{"", true},
		{`"a'b'c"`, true}, // 2 double quotes, 2 single quotes
	}

	for _, tt := range tests {
		result := IsBalancedQuotes(tt.input)
		if result != tt.expected {
			t.Errorf("IsBalancedQuotes(%q) = %v, expected %v", tt.input, result, tt.expected)
		}
	}
}

// TestEvaluatePostfix tests postfix evaluation
func TestEvaluatePostfix(t *testing.T) {
	tests := []struct {
		input    string
		expected float64
		hasError bool
	}{
		{"3 4 +", 7, false},
		{"5 1 2 + 4 * + 3 -", 14, false},
		{"2 3 1 * + 9 -", -4, false},
		{"10 2 /", 5, false},
		{"2 3 ^", 8, false},
		{"3 4 + 2 *", 14, false},
		{"3", 3, false},
	}

	for _, tt := range tests {
		result, err := EvaluatePostfix(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("EvaluatePostfix(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("EvaluatePostfix(%q) unexpected error: %v", tt.input, err)
			} else if result != tt.expected {
				t.Errorf("EvaluatePostfix(%q) = %f, expected %f", tt.input, result, tt.expected)
			}
		}
	}
}

// TestInfixToPostfix tests infix to postfix conversion
func TestInfixToPostfix(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"A+B", "A B +"},
		{"A+B*C", "A B C * +"},
		{"(A+B)*C", "A B + C *"},
		{"A+B*C/D", "A B C * D / +"},
		{"A+B+C", "A B + C +"},
	}

	for _, tt := range tests {
		result := InfixToPostfix(tt.input)
		// Normalize whitespace for comparison
		result = strings.ReplaceAll(result, "  ", " ")
		expected := strings.ReplaceAll(tt.expected, "  ", " ")
		if result != expected {
			t.Errorf("InfixToPostfix(%q) = %q, expected %q", tt.input, result, expected)
		}
	}
}

// TestReverseString tests string reversal
func TestReverseString(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "olleh"},
		{"world", "dlrow"},
		{"", ""},
		{"a", "a"},
		{"ab", "ba"},
		{"12345", "54321"},
		{"Hello, World!", "!dlroW ,olleH"},
	}

	for _, tt := range tests {
		result := ReverseString(tt.input)
		if result != tt.expected {
			t.Errorf("ReverseString(%q) = %q, expected %q", tt.input, result, tt.expected)
		}
	}
}

// TestNextGreaterElement tests next greater element
func TestNextGreaterElement(t *testing.T) {
	tests := []struct {
		input    []int
		expected []int
	}{
		{[]int{4, 5, 2, 25}, []int{5, 25, 25, -1}},
		{[]int{13, 7, 6, 12}, []int{-1, 12, 12, -1}},
		{[]int{1, 2, 3, 4}, []int{2, 3, 4, -1}},
		{[]int{4, 3, 2, 1}, []int{-1, -1, -1, -1}},
	}

	for _, tt := range tests {
		result := NextGreaterElement(tt.input)
		for i := range result {
			if result[i] != tt.expected[i] {
				t.Errorf("NextGreaterElement(%v)[%d] = %d, expected %d", tt.input, i, result[i], tt.expected[i])
			}
		}
	}
}

// TestPreviousSmallerElement tests previous smaller element
func TestPreviousSmallerElement(t *testing.T) {
	tests := []struct {
		input    []int
		expected []int
	}{
		{[]int{1, 3, 0, 2, 5}, []int{-1, 1, -1, 0, 2}},
		{[]int{1, 6, 4, 10, 2, 5}, []int{-1, 1, 1, 4, 1, 2}},
		{[]int{1, 3, 5, 7}, []int{-1, 1, 3, 5}},
	}

	for _, tt := range tests {
		result := PreviousSmallerElement(tt.input)
		for i := range result {
			if result[i] != tt.expected[i] {
				t.Errorf("PreviousSmallerElement(%v)[%d] = %d, expected %d", tt.input, i, result[i], tt.expected[i])
			}
		}
	}
}

// TestIsValidHTML tests HTML validation
func TestIsValidHTML(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"<div></div>", true},
		{"<div><p></p></div>", true},
		{"<div><span></span></div>", true},
		{"<div></div></div>", false},
		{"<div><p></div></p>", false},
		{"<div>", false},
		{"</div>", false},
		{"<div><p><a></a></p></div>", true},
		{"<div class='test'>content</div>", true},
	}

	for _, tt := range tests {
		result := IsValidHTML(tt.input)
		if result != tt.expected {
			t.Errorf("IsValidHTML(%q) = %v, expected %v", tt.input, result, tt.expected)
		}
	}
}

// TestLargestRectangleInHistogram tests histogram rectangle
func TestLargestRectangleInHistogram(t *testing.T) {
	tests := []struct {
		input    []int
		expected int
	}{
		{[]int{2, 1, 5, 6, 2, 3}, 10},
		{[]int{2, 4}, 4},
		{[]int{1}, 1},
		{[]int{1, 1}, 2},
		{[]int{2, 1, 2}, 3},
		{[]int{}, 0},
	}

	for _, tt := range tests {
		result := LargestRectangleInHistogram(tt.input)
		if result != tt.expected {
			t.Errorf("LargestRectangleInHistogram(%v) = %d, expected %d", tt.input, result, tt.expected)
		}
	}
}

// TestDailyTemperatures tests daily temperatures
func TestDailyTemperatures(t *testing.T) {
	tests := []struct {
		input    []int
		expected []int
	}{
		{[]int{73, 74, 75, 71, 69, 72, 76, 73}, []int{1, 1, 4, 2, 1, 1, 0, 0}},
		{[]int{30, 40, 50, 60}, []int{1, 1, 1, 0}},
		{[]int{30, 60, 90}, []int{1, 1, 0}},
		{[]int{90, 80, 70, 60}, []int{0, 0, 0, 0}},
	}

	for _, tt := range tests {
		result := DailyTemperatures(tt.input)
		for i := range result {
			if result[i] != tt.expected[i] {
				t.Errorf("DailyTemperatures(%v)[%d] = %d, expected %d", tt.input, i, result[i], tt.expected[i])
			}
		}
	}
}

// TestEvaluateRPN tests RPN evaluation
func TestEvaluateRPN(t *testing.T) {
	tests := []struct {
		input    []string
		expected int
		hasError bool
	}{
		{[]string{"2", "1", "+", "3", "*"}, 9, false},
		{[]string{"4", "13", "5", "/", "+"}, 6, false},
		{[]string{"10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"}, 22, false},
		{[]string{"3"}, 3, false},
	}

	for _, tt := range tests {
		result, err := EvaluateRPN(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("EvaluateRPN(%v) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("EvaluateRPN(%v) unexpected error: %v", tt.input, err)
			} else if result != tt.expected {
				t.Errorf("EvaluateRPN(%v) = %d, expected %d", tt.input, result, tt.expected)
			}
		}
	}
}

// TestRemoveAdjacentDuplicates tests adjacent duplicate removal
func TestRemoveAdjacentDuplicates(t *testing.T) {
	tests := []struct {
		input    string
		k        int
		expected string
	}{
		{"abcd", 2, "abcd"},
		{"deeedbbcccbdaa", 3, "aa"},
		{"pbbcggttciiippooaais", 2, "ps"},
		{"aaabbbccc", 3, ""},
		{"aabbcc", 2, ""},
	}

	for _, tt := range tests {
		result := RemoveAdjacentDuplicates(tt.input, tt.k)
		if result != tt.expected {
			t.Errorf("RemoveAdjacentDuplicates(%q, %d) = %q, expected %q", tt.input, tt.k, result, tt.expected)
		}
	}
}

// TestStackStringMethod tests the String method
func TestStackStringMethod(t *testing.T) {
	s := NewStack[int]()
	s.Push(1)
	s.Push(2)
	s.Push(3)

	result := s.String()
	if result != "[1 2 3]" {
		t.Errorf("Stack.String() = %q, expected %q", result, "[1 2 3]")
	}
}

// TestNewStackWithCapacity tests stack with pre-allocated capacity
func TestNewStackWithCapacity(t *testing.T) {
	s := NewStackWithCapacity[int](10)
	if s.Size() != 0 {
		t.Errorf("New stack with capacity should have size 0, got %d", s.Size())
	}

	// Push more than initial capacity to test growth
	for i := 0; i < 20; i++ {
		s.Push(i)
	}

	if s.Size() != 20 {
		t.Errorf("Expected size 20, got %d", s.Size())
	}
}

// TestMinStackEdgeCases tests edge cases for MinStack
func TestMinStackEdgeCases(t *testing.T) {
	s := NewMinStack[int]()

	_, err := s.Min()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty, got %v", err)
	}

	_, err = s.Pop()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty, got %v", err)
	}

	// Push same value multiple times
	s.Push(5)
	s.Push(5)
	s.Push(5)

	min, _ := s.Min()
	if min != 5 {
		t.Errorf("Expected min 5, got %d", min)
	}

	s.Pop()
	s.Pop()
	min, _ = s.Min()
	if min != 5 {
		t.Errorf("Expected min still 5, got %d", min)
	}

	s.Pop()
	_, err = s.Min()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty after all pops, got %v", err)
	}
}

// TestMaxStackEdgeCases tests edge cases for MaxStack
func TestMaxStackEdgeCases(t *testing.T) {
	s := NewMaxStack[int]()

	_, err := s.Max()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty, got %v", err)
	}

	// Push descending values
	s.Push(5)
	s.Push(4)
	s.Push(3)

	max, _ := s.Max()
	if max != 5 {
		t.Errorf("Expected max 5, got %d", max)
	}

	s.Pop()
	max, _ = s.Max()
	if max != 5 {
		t.Errorf("Expected max still 5, got %d", max)
	}

	s.Pop()
	s.Pop()
	_, err = s.Max()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty after all pops, got %v", err)
	}
}

// TestBoundedStackEdgeCases tests edge cases for BoundedStack
func TestBoundedStackEdgeCases(t *testing.T) {
	s := NewBoundedStack[int](0)

	if !s.IsFull() {
		t.Error("Zero capacity stack should be full")
	}

	if err := s.Push(1); err != ErrStackFull {
		t.Errorf("Expected ErrStackFull for zero capacity, got %v", err)
	}

	_, err := s.Pop()
	if err != ErrStackEmpty {
		t.Errorf("Expected ErrStackEmpty, got %v", err)
	}
}

// TestNegativeNumbers tests stacks with negative numbers
func TestNegativeNumbers(t *testing.T) {
	// MinStack with negative numbers
	s := NewMinStack[int]()
	s.Push(-5)
	s.Push(-3)
	s.Push(-10)

	min, _ := s.Min()
	if min != -10 {
		t.Errorf("Expected min -10, got %d", min)
	}

	s.Pop()
	min, _ = s.Min()
	if min != -5 {
		t.Errorf("Expected min -5, got %d", min)
	}

	// MaxStack with negative numbers
	maxS := NewMaxStack[int]()
	maxS.Push(-5)
	maxS.Push(-3)
	maxS.Push(-10)

	max, _ := maxS.Max()
	if max != -3 {
		t.Errorf("Expected max -3, got %d", max)
	}
}

// TestStringStack tests stack with strings for MinStack and MaxStack
func TestStringStack(t *testing.T) {
	s := NewStack[string]()
	words := []string{"apple", "banana", "cherry", "date"}

	for _, w := range words {
		s.Push(w)
	}

	for i := len(words) - 1; i >= 0; i-- {
		item, err := s.Pop()
		if err != nil || item != words[i] {
			t.Errorf("Expected %s, got %s", words[i], item)
		}
	}
}

// BenchmarkStackPush benchmarks stack push operations
func BenchmarkStackPush(b *testing.B) {
	s := NewStack[int]()
	for i := 0; i < b.N; i++ {
		s.Push(i)
		if i%1000 == 0 {
			s.Clear()
		}
	}
}

// BenchmarkStackPop benchmarks stack pop operations
func BenchmarkStackPop(b *testing.B) {
	s := NewStack[int]()
	for i := 0; i < b.N; i++ {
		s.Push(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		s.Pop()
	}
}

// BenchmarkMinStackPush benchmarks MinStack push operations
func BenchmarkMinStackPush(b *testing.B) {
	s := NewMinStack[int]()
	for i := 0; i < b.N; i++ {
		s.Push(i)
		if i%1000 == 0 {
			s = NewMinStack[int]()
		}
	}
}

// BenchmarkIsBalancedParentheses benchmarks parentheses balancing
func BenchmarkIsBalancedParentheses(b *testing.B) {
	testStr := "((({{{[[[]]]}}})))"
	for i := 0; i < b.N; i++ {
		IsBalancedParentheses(testStr)
	}
}

// BenchmarkEvaluatePostfix benchmarks postfix evaluation
func BenchmarkEvaluatePostfix(b *testing.B) {
	expr := "3 4 + 2 * 7 / 5 -"
	for i := 0; i < b.N; i++ {
		EvaluatePostfix(expr)
	}
}