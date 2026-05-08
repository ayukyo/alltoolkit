// Package combination_utils provides utilities for generating combinations
// and permutations of elements in Go.
//
// Features:
//   - Generate all combinations of a given size (nCk)
//   - Generate all permutations
//   - Generate combinations with repetition
//   - Calculate binomial coefficients
//   - Generate power sets
//   - Memory-efficient generators using channels
package combination_utils

import (
	"errors"
	"math"
)

// Combinations generates all combinations of k elements from the input slice.
// Uses backtracking algorithm. Returns empty if k > len(slice) or k < 0.
func Combinations[T any](slice []T, k int) [][]T {
	n := len(slice)
	if k < 0 || k > n {
		return nil
	}
	if k == 0 {
		return [][]T{{}}
	}
	if k == n {
		result := make([]T, n)
		copy(result, slice)
		return [][]T{result}
	}

	var result [][]T
	indices := make([]int, k)
	current := make([]T, k)

	// Initialize first combination
	for i := 0; i < k; i++ {
		indices[i] = i
		current[i] = slice[i]
	}
	result = append(result, cloneSlice(current))

	// Generate subsequent combinations
	for {
		var i int
		for i = k - 1; i >= 0; i-- {
			if indices[i] != n-k+i {
				break
			}
		}
		if i < 0 {
			break
		}
		indices[i]++
		for j := i + 1; j < k; j++ {
			indices[j] = indices[j-1] + 1
		}
		for j := 0; j < k; j++ {
			current[j] = slice[indices[j]]
		}
		result = append(result, cloneSlice(current))
	}

	return result
}

// CombinationsChan generates combinations and sends them through a channel.
// Useful for large datasets where you don't want to store all combinations in memory.
func CombinationsChan[T any](slice []T, k int) <-chan []T {
	ch := make(chan []T)
	go func() {
		defer close(ch)
		n := len(slice)
		if k < 0 || k > n {
			return
		}
		if k == 0 {
			ch <- []T{}
			return
		}
		if k == n {
			result := make([]T, n)
			copy(result, slice)
			ch <- result
			return
		}

		indices := make([]int, k)
		current := make([]T, k)
		for i := 0; i < k; i++ {
			indices[i] = i
			current[i] = slice[i]
		}
		ch <- cloneSlice(current)

		for {
			var i int
			for i = k - 1; i >= 0; i-- {
				if indices[i] != n-k+i {
					break
				}
			}
			if i < 0 {
				break
			}
			indices[i]++
			for j := i + 1; j < k; j++ {
				indices[j] = indices[j-1] + 1
			}
			for j := 0; j < k; j++ {
				current[j] = slice[indices[j]]
			}
			ch <- cloneSlice(current)
		}
	}()
	return ch
}

// Permutations generates all permutations of the input slice.
// Uses Heap's algorithm for efficient generation.
func Permutations[T any](slice []T) [][]T {
	n := len(slice)
	if n == 0 {
		return [][]T{{}}
	}

	// Make a copy to avoid modifying the original
	elements := make([]T, n)
	copy(elements, slice)

	var result [][]T
	var generate func(int)

	generate = func(k int) {
		if k == 1 {
			result = append(result, cloneSlice(elements))
			return
		}
		generate(k - 1)
		for i := 0; i < k-1; i++ {
			if k%2 == 0 {
				elements[i], elements[k-1] = elements[k-1], elements[i]
			} else {
				elements[0], elements[k-1] = elements[k-1], elements[0]
			}
			generate(k - 1)
		}
	}

	generate(n)
	return result
}

// PermutationsChan generates permutations and sends them through a channel.
func PermutationsChan[T any](slice []T) <-chan []T {
	ch := make(chan []T)
	go func() {
		defer close(ch)
		n := len(slice)
		if n == 0 {
			ch <- []T{}
			return
		}

		elements := make([]T, n)
		copy(elements, slice)

		var generate func(int)
		generate = func(k int) {
			if k == 1 {
				ch <- cloneSlice(elements)
				return
			}
			generate(k - 1)
			for i := 0; i < k-1; i++ {
				if k%2 == 0 {
					elements[i], elements[k-1] = elements[k-1], elements[i]
				} else {
					elements[0], elements[k-1] = elements[k-1], elements[0]
				}
				generate(k - 1)
			}
		}

		generate(n)
	}()
	return ch
}

// PermutationsK generates all k-permutations (arrangements) of the input slice.
// k-permutations are ordered arrangements of k elements from n elements.
func PermutationsK[T any](slice []T, k int) [][]T {
	n := len(slice)
	if k < 0 || k > n {
		return nil
	}
	if k == 0 {
		return [][]T{{}}
	}

	var result [][]T
	used := make([]bool, n)
	current := make([]T, k)

	var generate func(int)
	generate = func(pos int) {
		if pos == k {
			result = append(result, cloneSlice(current))
			return
		}
		for i := 0; i < n; i++ {
			if !used[i] {
				used[i] = true
				current[pos] = slice[i]
				generate(pos + 1)
				used[i] = false
			}
		}
	}

	generate(0)
	return result
}

// CombinationsWithRepetition generates all combinations of k elements
// where each element can be chosen multiple times.
func CombinationsWithRepetition[T any](slice []T, k int) [][]T {
	n := len(slice)
	if k < 0 || (n == 0 && k > 0) {
		return nil
	}
	if k == 0 {
		return [][]T{{}}
	}

	var result [][]T
	indices := make([]int, k)
	current := make([]T, k)

	for i := 0; i < k; i++ {
		current[i] = slice[0]
	}
	result = append(result, cloneSlice(current))

	for {
		var i int
		for i = k - 1; i >= 0; i-- {
			if indices[i] != n-1 {
				break
			}
		}
		if i < 0 {
			break
		}
		indices[i]++
		for j := i; j < k; j++ {
			indices[j] = indices[i]
		}
		for j := 0; j < k; j++ {
			current[j] = slice[indices[j]]
		}
		result = append(result, cloneSlice(current))
	}

	return result
}

// PowerSet generates all subsets of the input slice.
// Returns 2^n subsets for a slice of length n.
func PowerSet[T any](slice []T) [][]T {
	n := len(slice)
	if n == 0 {
		return [][]T{{}}
	}

	count := 1 << n // 2^n
	result := make([][]T, 0, count)

	for mask := 0; mask < count; mask++ {
		subset := make([]T, 0) // Initialize as empty slice, not nil
		for i := 0; i < n; i++ {
			if mask&(1<<i) != 0 {
				subset = append(subset, slice[i])
			}
		}
		result = append(result, subset)
	}

	return result
}

// PowerSetChan generates subsets and sends them through a channel.
func PowerSetChan[T any](slice []T) <-chan []T {
	ch := make(chan []T)
	go func() {
		defer close(ch)
		n := len(slice)
		if n == 0 {
			ch <- []T{}
			return
		}

		count := 1 << n
		for mask := 0; mask < count; mask++ {
			subset := make([]T, 0) // Initialize as empty slice, not nil
			for i := 0; i < n; i++ {
				if mask&(1<<i) != 0 {
					subset = append(subset, slice[i])
				}
			}
			ch <- subset
		}
	}()
	return ch
}

// BinomialCoefficient calculates n choose k (nCk).
// Returns the number of ways to choose k items from n items.
// Returns an error if the result overflows or inputs are invalid.
func BinomialCoefficient(n, k int) (int, error) {
	if n < 0 || k < 0 || k > n {
		return 0, errors.New("invalid parameters: n and k must be non-negative with k <= n")
	}
	if k == 0 || k == n {
		return 1, nil
	}
	// Optimize by using smaller k
	if k > n-k {
		k = n - k
	}

	result := 1
	for i := 0; i < k; i++ {
		if result > (math.MaxInt - result) / (n - i) * (i + 1) {
			return 0, errors.New("overflow: result exceeds int max")
		}
		result = result * (n - i) / (i + 1)
	}
	return result, nil
}

// Factorial calculates n! (factorial of n).
// Returns an error if n is negative or the result overflows.
func Factorial(n int) (int, error) {
	if n < 0 {
		return 0, errors.New("factorial is not defined for negative numbers")
	}
	if n > 20 {
		return 0, errors.New("overflow: factorial exceeds int max for n > 20")
	}
	if n <= 1 {
		return 1, nil
	}
	result := 1
	for i := 2; i <= n; i++ {
		result *= i
	}
	return result, nil
}

// CountCombinations returns the number of possible combinations of k elements from n elements.
// Equivalent to BinomialCoefficient.
func CountCombinations(n, k int) (int, error) {
	return BinomialCoefficient(n, k)
}

// CountPermutations returns the number of possible permutations of k elements from n elements.
// P(n, k) = n! / (n-k)!
func CountPermutations(n, k int) (int, error) {
	if n < 0 || k < 0 || k > n {
		return 0, errors.New("invalid parameters: n and k must be non-negative with k <= n")
	}
	result := 1
	for i := 0; i < k; i++ {
		if result > math.MaxInt/(n-i) {
			return 0, errors.New("overflow: result exceeds int max")
		}
		result *= (n - i)
	}
	return result, nil
}

// CountPermutationsAll returns the number of possible permutations of all n elements.
// Equivalent to Factorial(n).
func CountPermutationsAll(n int) (int, error) {
	return Factorial(n)
}

// CountPowerSet returns 2^n (number of subsets).
func CountPowerSet(n int) int {
	if n < 0 || n >= 63 {
		return 0 // Would overflow int
	}
	return 1 << n
}

// CombinationsWithRepetitionCount returns the number of combinations with repetition.
// C(n+k-1, k) = (n+k-1)! / (k! * (n-1)!)
func CombinationsWithRepetitionCount(n, k int) (int, error) {
	if n < 0 || k < 0 {
		return 0, errors.New("invalid parameters: n and k must be non-negative")
	}
	if n == 0 && k > 0 {
		return 0, nil
	}
	return BinomialCoefficient(n+k-1, k)
}

// MultiSetPermutation generates all unique permutations when elements can have duplicates.
// Counts maps each element to its count.
func MultiSetPermutation[T comparable](elements []T) [][]T {
	// Count occurrences
	counts := make(map[T]int)
	for _, e := range elements {
		counts[e]++
	}

	// Extract unique elements
	unique := make([]T, 0, len(counts))
	for e := range counts {
		unique = append(unique, e)
	}

	var result [][]T
	current := make([]T, len(elements))

	var generate func(int)
	generate = func(pos int) {
		if pos == len(elements) {
			result = append(result, cloneSlice(current))
			return
		}
		for _, e := range unique {
			if counts[e] > 0 {
				counts[e]--
				current[pos] = e
				generate(pos + 1)
				counts[e]++
			}
		}
	}

	generate(0)
	return result
}

// MultiSetPermutationCount calculates the number of unique permutations
// for a multiset with given element counts.
func MultiSetPermutationCount(total int, counts ...int) (int, error) {
	if total < 0 {
		return 0, errors.New("total must be non-negative")
	}
	sumCounts := 0
	for _, c := range counts {
		if c < 0 {
			return 0, errors.New("counts must be non-negative")
		}
		sumCounts += c
	}
	if sumCounts != total {
		return 0, errors.New("sum of counts must equal total")
	}

	result := 1
	for i := 1; i <= total; i++ {
		result *= i
	}
	for _, c := range counts {
		if c > 1 {
			for i := 2; i <= c; i++ {
				result /= i
			}
		}
	}
	return result, nil
}

// CartesianProduct generates the Cartesian product of multiple slices.
func CartesianProduct[T any](slices ...[]T) [][]T {
	if len(slices) == 0 {
		return [][]T{{}}
	}

	// Calculate total size
	total := 1
	for _, s := range slices {
		if len(s) == 0 {
			return nil
		}
		total *= len(s)
	}

	result := make([][]T, 0, total)
	indices := make([]int, len(slices))
	current := make([]T, len(slices))

	for i, s := range slices {
		current[i] = s[0]
	}

	for {
		result = append(result, cloneSlice(current))

		// Find rightmost index to increment
		i := len(slices) - 1
		for i >= 0 && indices[i] == len(slices[i])-1 {
			indices[i] = 0
			current[i] = slices[i][0]
			i--
		}
		if i < 0 {
			break
		}
		indices[i]++
		current[i] = slices[i][indices[i]]
	}

	return result
}

// CartesianProductCount returns the size of the Cartesian product.
func CartesianProductCount(lengths ...int) (int, error) {
	if len(lengths) == 0 {
		return 1, nil
	}
	result := 1
	for _, l := range lengths {
		if l < 0 {
			return 0, errors.New("lengths must be non-negative")
		}
		if l == 0 {
			return 0, nil
		}
		if result > math.MaxInt/l {
			return 0, errors.New("overflow")
		}
		result *= l
	}
	return result, nil
}

// Helper function to clone a slice
func cloneSlice[T any](s []T) []T {
	result := make([]T, len(s))
	copy(result, s)
	return result
}