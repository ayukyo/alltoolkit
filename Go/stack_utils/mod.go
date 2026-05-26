// Package stack_utils provides generic stack implementations and algorithms
package stack_utils

import (
	"errors"
	"fmt"
	"strings"
)

// Common errors
var (
	ErrStackEmpty     = errors.New("stack is empty")
	ErrStackFull      = errors.New("stack is full")
	ErrInvalidParen   = errors.New("invalid parentheses")
	ErrInvalidPostfix = errors.New("invalid postfix expression")
)

// Stack is a generic LIFO (Last In, First Out) data structure
type Stack[T any] struct {
	items []T
}

// NewStack creates a new empty stack
func NewStack[T any]() *Stack[T] {
	return &Stack[T]{
		items: make([]T, 0),
	}
}

// NewStackWithCapacity creates a new stack with pre-allocated capacity
func NewStackWithCapacity[T any](capacity int) *Stack[T] {
	return &Stack[T]{
		items: make([]T, 0, capacity),
	}
}

// Push adds an item to the top of the stack
func (s *Stack[T]) Push(item T) {
	s.items = append(s.items, item)
}

// Pop removes and returns the top item from the stack
func (s *Stack[T]) Pop() (T, error) {
	var zero T
	if s.IsEmpty() {
		return zero, ErrStackEmpty
	}
	index := len(s.items) - 1
	item := s.items[index]
	s.items = s.items[:index]
	return item, nil
}

// Peek returns the top item without removing it
func (s *Stack[T]) Peek() (T, error) {
	var zero T
	if s.IsEmpty() {
		return zero, ErrStackEmpty
	}
	return s.items[len(s.items)-1], nil
}

// IsEmpty returns true if the stack is empty
func (s *Stack[T]) IsEmpty() bool {
	return len(s.items) == 0
}

// Size returns the number of items in the stack
func (s *Stack[T]) Size() int {
	return len(s.items)
}

// Clear removes all items from the stack
func (s *Stack[T]) Clear() {
	s.items = s.items[:0]
}

// ToSlice returns a copy of the stack items (bottom to top)
func (s *Stack[T]) ToSlice() []T {
	result := make([]T, len(s.items))
	copy(result, s.items)
	return result
}

// FromSlice creates a stack from a slice (first element becomes bottom)
func FromSlice[T any](items []T) *Stack[T] {
	s := NewStackWithCapacity[T](len(items))
	s.items = append(s.items, items...)
	return s
}

// String returns a string representation of the stack
func (s *Stack[T]) String() string {
	return fmt.Sprintf("%v", s.items)
}

// BoundedStack is a stack with a maximum capacity
type BoundedStack[T any] struct {
	items    []T
	size     int
	capacity int
}

// NewBoundedStack creates a new stack with fixed capacity
func NewBoundedStack[T any](capacity int) *BoundedStack[T] {
	return &BoundedStack[T]{
		items:    make([]T, capacity),
		size:     0,
		capacity: capacity,
	}
}

// Push adds an item to the top of the stack
func (s *BoundedStack[T]) Push(item T) error {
	if s.size >= s.capacity {
		return ErrStackFull
	}
	s.items[s.size] = item
	s.size++
	return nil
}

// Pop removes and returns the top item
func (s *BoundedStack[T]) Pop() (T, error) {
	var zero T
	if s.size == 0 {
		return zero, ErrStackEmpty
	}
	s.size--
	item := s.items[s.size]
	return item, nil
}

// Peek returns the top item without removing it
func (s *BoundedStack[T]) Peek() (T, error) {
	var zero T
	if s.size == 0 {
		return zero, ErrStackEmpty
	}
	return s.items[s.size-1], nil
}

// IsEmpty returns true if the stack is empty
func (s *BoundedStack[T]) IsEmpty() bool {
	return s.size == 0
}

// IsFull returns true if the stack is full
func (s *BoundedStack[T]) IsFull() bool {
	return s.size >= s.capacity
}

// Size returns the current number of items
func (s *BoundedStack[T]) Size() int {
	return s.size
}

// Capacity returns the maximum capacity
func (s *BoundedStack[T]) Capacity() int {
	return s.capacity
}

// Clear removes all items from the stack
func (s *BoundedStack[T]) Clear() {
	s.size = 0
}

// MinStack is a stack that supports O(1) minimum queries
type MinStack[T Ordered] struct {
	items    []T
	minStack []T
}

// Ordered constraint for comparable and ordered types
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 |
		~string
}

// NewMinStack creates a new stack that tracks minimum
func NewMinStack[T Ordered]() *MinStack[T] {
	return &MinStack[T]{
		items:    make([]T, 0),
		minStack: make([]T, 0),
	}
}

// Push adds an item and updates minimum
func (s *MinStack[T]) Push(item T) {
	s.items = append(s.items, item)
	if len(s.minStack) == 0 || item <= s.minStack[len(s.minStack)-1] {
		s.minStack = append(s.minStack, item)
	}
}

// Pop removes and returns the top item
func (s *MinStack[T]) Pop() (T, error) {
	var zero T
	if len(s.items) == 0 {
		return zero, ErrStackEmpty
	}
	index := len(s.items) - 1
	item := s.items[index]
	s.items = s.items[:index]

	if item == s.minStack[len(s.minStack)-1] {
		s.minStack = s.minStack[:len(s.minStack)-1]
	}
	return item, nil
}

// Peek returns the top item without removing it
func (s *MinStack[T]) Peek() (T, error) {
	var zero T
	if len(s.items) == 0 {
		return zero, ErrStackEmpty
	}
	return s.items[len(s.items)-1], nil
}

// Min returns the minimum element in O(1) time
func (s *MinStack[T]) Min() (T, error) {
	var zero T
	if len(s.minStack) == 0 {
		return zero, ErrStackEmpty
	}
	return s.minStack[len(s.minStack)-1], nil
}

// IsEmpty returns true if the stack is empty
func (s *MinStack[T]) IsEmpty() bool {
	return len(s.items) == 0
}

// Size returns the number of items
func (s *MinStack[T]) Size() int {
	return len(s.items)
}

// MaxStack is a stack that supports O(1) maximum queries
type MaxStack[T Ordered] struct {
	items    []T
	maxStack []T
}

// NewMaxStack creates a new stack that tracks maximum
func NewMaxStack[T Ordered]() *MaxStack[T] {
	return &MaxStack[T]{
		items:    make([]T, 0),
		maxStack: make([]T, 0),
	}
}

// Push adds an item and updates maximum
func (s *MaxStack[T]) Push(item T) {
	s.items = append(s.items, item)
	if len(s.maxStack) == 0 || item >= s.maxStack[len(s.maxStack)-1] {
		s.maxStack = append(s.maxStack, item)
	}
}

// Pop removes and returns the top item
func (s *MaxStack[T]) Pop() (T, error) {
	var zero T
	if len(s.items) == 0 {
		return zero, ErrStackEmpty
	}
	index := len(s.items) - 1
	item := s.items[index]
	s.items = s.items[:index]

	if item == s.maxStack[len(s.maxStack)-1] {
		s.maxStack = s.maxStack[:len(s.maxStack)-1]
	}
	return item, nil
}

// Peek returns the top item without removing it
func (s *MaxStack[T]) Peek() (T, error) {
	var zero T
	if len(s.items) == 0 {
		return zero, ErrStackEmpty
	}
	return s.items[len(s.items)-1], nil
}

// Max returns the maximum element in O(1) time
func (s *MaxStack[T]) Max() (T, error) {
	var zero T
	if len(s.maxStack) == 0 {
		return zero, ErrStackEmpty
	}
	return s.maxStack[len(s.maxStack)-1], nil
}

// IsEmpty returns true if the stack is empty
func (s *MaxStack[T]) IsEmpty() bool {
	return len(s.items) == 0
}

// Size returns the number of items
func (s *MaxStack[T]) Size() int {
	return len(s.items)
}

// IsBalancedParentheses checks if parentheses are balanced
func IsBalancedParentheses(s string) bool {
	stack := NewStack[rune]()
	pairs := map[rune]rune{
		')': '(',
		']': '[',
		'}': '{',
	}

	for _, ch := range s {
		switch ch {
		case '(', '[', '{':
			stack.Push(ch)
		case ')', ']', '}':
			top, err := stack.Pop()
			if err != nil || top != pairs[ch] {
				return false
			}
		}
	}
	return stack.IsEmpty()
}

// IsBalancedQuotes checks if quotes are balanced
func IsBalancedQuotes(s string) bool {
	doubleQuotes := 0
	singleQuotes := 0

	for _, ch := range s {
		switch ch {
		case '"':
			doubleQuotes++
		case '\'':
			singleQuotes++
		}
	}
	return doubleQuotes%2 == 0 && singleQuotes%2 == 0
}

// EvaluatePostfix evaluates a postfix expression (supports +, -, *, /)
func EvaluatePostfix(expression string) (float64, error) {
	stack := NewStack[float64]()
	tokens := strings.Fields(expression)

	operators := map[string]func(float64, float64) float64{
		"+": func(a, b float64) float64 { return a + b },
		"-": func(a, b float64) float64 { return a - b },
		"*": func(a, b float64) float64 { return a * b },
		"/": func(a, b float64) float64 { return a / b },
		"^": func(a, b float64) float64 {
			result := 1.0
			for i := 0; i < int(b); i++ {
				result *= a
			}
			return result
		},
	}

	for _, token := range tokens {
		if op, isOp := operators[token]; isOp {
			b, err := stack.Pop()
			if err != nil {
				return 0, ErrInvalidPostfix
			}
			a, err := stack.Pop()
			if err != nil {
				return 0, ErrInvalidPostfix
			}
			stack.Push(op(a, b))
		} else {
			var num float64
			_, err := fmt.Sscanf(token, "%f", &num)
			if err != nil {
				return 0, fmt.Errorf("invalid token: %s", token)
			}
			stack.Push(num)
		}
	}

	if stack.Size() != 1 {
		return 0, ErrInvalidPostfix
	}
	return stack.Pop()
}

// InfixToPostfix converts infix expression to postfix notation
func InfixToPostfix(expression string) string {
	output := strings.Builder{}
	stack := NewStack[rune]()
	precedence := map[rune]int{
		'+': 1, '-': 1,
		'*': 2, '/': 2,
		'^': 3,
	}

	for _, ch := range expression {
		switch {
		case ch >= '0' && ch <= '9', ch >= 'a' && ch <= 'z', ch >= 'A' && ch <= 'Z':
			output.WriteRune(ch)
			output.WriteRune(' ')
		case ch == '(':
			stack.Push(ch)
		case ch == ')':
			for !stack.IsEmpty() {
				top, _ := stack.Peek()
				if top == '(' {
					break
				}
				stack.Pop()
				output.WriteRune(top)
				output.WriteRune(' ')
			}
			stack.Pop() // Remove '('
		case ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^':
			for !stack.IsEmpty() {
				top, _ := stack.Peek()
				if top == '(' || precedence[ch] > precedence[top] {
					break
				}
				if precedence[ch] == precedence[top] && ch == '^' {
					break // Right associative
				}
				stack.Pop()
				output.WriteRune(top)
				output.WriteRune(' ')
			}
			stack.Push(ch)
		}
	}

	for !stack.IsEmpty() {
		top, _ := stack.Pop()
		output.WriteRune(top)
		output.WriteRune(' ')
	}

	return strings.TrimSpace(output.String())
}

// ReverseString reverses a string using a stack
func ReverseString(s string) string {
	stack := NewStack[rune]()
	for _, ch := range s {
		stack.Push(ch)
	}

	var result strings.Builder
	for !stack.IsEmpty() {
		ch, _ := stack.Pop()
		result.WriteRune(ch)
	}
	return result.String()
}

// NextGreaterElement finds the next greater element for each array element
// Returns an array where result[i] is the next greater element after arr[i],
// or -1 if no greater element exists
func NextGreaterElement(arr []int) []int {
	n := len(arr)
	result := make([]int, n)
	stack := NewStack[int]()

	for i := n - 1; i >= 0; i-- {
		for !stack.IsEmpty() {
			top, _ := stack.Peek()
			if arr[top] > arr[i] {
				break
			}
			stack.Pop()
		}

		if stack.IsEmpty() {
			result[i] = -1 // No greater element
		} else {
			top, _ := stack.Peek()
			result[i] = arr[top]
		}
		stack.Push(i)
	}
	return result
}

// PreviousSmallerElement finds the previous smaller element for each array element
// Returns an array where result[i] is the previous smaller element before arr[i],
// or -1 if no smaller element exists
func PreviousSmallerElement(arr []int) []int {
	n := len(arr)
	result := make([]int, n)
	stack := NewStack[int]()

	for i := 0; i < n; i++ {
		for !stack.IsEmpty() {
			top, _ := stack.Peek()
			if arr[top] < arr[i] {
				break
			}
			stack.Pop()
		}

		if stack.IsEmpty() {
			result[i] = -1 // No smaller element
		} else {
			top, _ := stack.Peek()
			result[i] = arr[top]
		}
		stack.Push(i)
	}
	return result
}

// IsValidHTML checks if HTML tags are properly nested
func IsValidHTML(html string) bool {
	stack := NewStack[string]()
	i := 0

	for i < len(html) {
		if html[i] == '<' {
			j := i + 1
			if j >= len(html) {
				return false
			}

			if html[j] == '/' {
				// Closing tag
				k := j + 1
				for k < len(html) && html[k] != '>' {
					k++
				}
				if k >= len(html) {
					return false
				}
				tag := html[j+1 : k]
				top, err := stack.Pop()
				if err != nil || top != tag {
					return false
				}
				i = k + 1
			} else {
				// Opening tag
				k := j
				for k < len(html) && html[k] != '>' && html[k] != ' ' {
					k++
				}
				if k >= len(html) {
					return false
				}
				tag := html[j:k]
				stack.Push(tag)
				// Skip to end of tag
				for k < len(html) && html[k] != '>' {
					k++
				}
				i = k + 1
			}
		} else {
			i++
		}
	}
	return stack.IsEmpty()
}

// LargestRectangleInHistogram finds the largest rectangle area in a histogram
func LargestRectangleInHistogram(heights []int) int {
	n := len(heights)
	if n == 0 {
		return 0
	}

	stack := NewStack[int]()
	maxArea := 0

	for i := 0; i <= n; i++ {
		h := 0
		if i < n {
			h = heights[i]
		}

		for !stack.IsEmpty() {
			top, _ := stack.Peek()
			if heights[top] <= h {
				break
			}
			height := heights[top]
			stack.Pop()

			var width int
			if stack.IsEmpty() {
				width = i
			} else {
				newTop, _ := stack.Peek()
				width = i - newTop - 1
			}
			area := height * width
			if area > maxArea {
				maxArea = area
			}
		}
		stack.Push(i)
	}
	return maxArea
}

// DailyTemperatures finds how many days until a warmer temperature
func DailyTemperatures(temperatures []int) []int {
	n := len(temperatures)
	result := make([]int, n)
	stack := NewStack[int]()

	for i := 0; i < n; i++ {
		for !stack.IsEmpty() {
			top, _ := stack.Peek()
			if temperatures[i] <= temperatures[top] {
				break
			}
			stack.Pop()
			result[top] = i - top
		}
		stack.Push(i)
	}
	return result
}

// EvaluateRPN evaluates Reverse Polish Notation expression
// Alias for EvaluatePostfix for compatibility
func EvaluateRPN(tokens []string) (int, error) {
	stack := NewStack[int]()

	operators := map[string]func(int, int) int{
		"+": func(a, b int) int { return a + b },
		"-": func(a, b int) int { return a - b },
		"*": func(a, b int) int { return a * b },
		"/": func(a, b int) int { return a / b },
	}

	for _, token := range tokens {
		if op, isOp := operators[token]; isOp {
			b, err := stack.Pop()
			if err != nil {
				return 0, ErrInvalidPostfix
			}
			a, err := stack.Pop()
			if err != nil {
				return 0, ErrInvalidPostfix
			}
			stack.Push(op(a, b))
		} else {
			var num int
			_, err := fmt.Sscanf(token, "%d", &num)
			if err != nil {
				return 0, fmt.Errorf("invalid token: %s", token)
			}
			stack.Push(num)
		}
	}

	if stack.Size() != 1 {
		return 0, ErrInvalidPostfix
	}
	return stack.Pop()
}

// RemoveAdjacentDuplicates removes adjacent duplicate characters
func RemoveAdjacentDuplicates(s string, k int) string {
	// Stack stores (character, count)
	type charCount struct {
		char  rune
		count int
	}
	stack := NewStack[charCount]()

	for _, ch := range s {
		if stack.IsEmpty() {
			stack.Push(charCount{char: ch, count: 1})
		} else {
			top, _ := stack.Peek()
			if top.char == ch {
				if top.count+1 == k {
					stack.Pop()
				} else {
					stack.Pop()
					stack.Push(charCount{char: ch, count: top.count + 1})
				}
			} else {
				stack.Push(charCount{char: ch, count: 1})
			}
		}
	}

	var result strings.Builder
	items := stack.ToSlice()
	for _, item := range items {
		for i := 0; i < item.count; i++ {
			result.WriteRune(item.char)
		}
	}
	return result.String()
}