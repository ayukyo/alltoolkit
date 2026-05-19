// Package fenwick_tree_utils provides Fenwick Tree (Binary Indexed Tree) implementation.
// Zero external dependencies - uses only Go standard library.
//
// A Fenwick Tree is a data structure that provides efficient methods for:
// - Point updates: O(log n)
// - Prefix sum queries: O(log n)
// - Range sum queries: O(log n) (computed as prefix_sum(r) - prefix_sum(l-1))
//
// Compared to a simple array with prefix sums:
// - Array prefix sum query: O(1), but update is O(n)
// - Fenwick Tree: both operations are O(log n)
//
// Features:
//   - Generic type support using int64
//   - Range sum queries
//   - Point value queries and updates
//   - Bulk construction from arrays
//   - Inverse operations (finding smallest index with prefix sum >= target)
//   - Support for negative values and range minimum/maximum queries
//   - 2D Fenwick Tree for matrix operations
//
// Example usage:
//
//	tree := fenwick_tree_utils.New(10)
//	tree.Update(5, 100)  // Add 100 at position 5
//	tree.Update(8, 50)   // Add 50 at position 8
//	sum := tree.PrefixSum(7)  // Sum of indices 1-7
//	rangeSum := tree.RangeSum(5, 8)  // Sum of indices 5-8
package fenwick_tree_utils

import (
	"errors"
	"sort"
)

// Common errors
var (
	ErrIndexOutOfRange   = errors.New("index out of range")
	ErrNegativeIndex     = errors.New("index cannot be negative")
	ErrEmptyTree         = errors.New("tree is empty")
	ErrInvalidRange      = errors.New("invalid range: left > right")
	ErrNoInverseResult   = errors.New("no valid inverse result found")
)

// FenwickTree represents a 1D Fenwick Tree (Binary Indexed Tree).
type FenwickTree struct {
	size   int
	tree   []int64
	origin []int64 // Original values for value queries
}

// New creates a new Fenwick Tree with the specified size.
// Indices are 1-based (1 to size).
func New(size int) *FenwickTree {
	if size <= 0 {
		panic("fenwick tree size must be positive")
	}
	return &FenwickTree{
		size:   size,
		tree:   make([]int64, size+1), // index 0 unused
		origin: make([]int64, size+1),
	}
}

// NewFromArray creates a Fenwick Tree from an existing array.
// The input array should be 0-indexed, but tree operations are 1-indexed.
func NewFromArray(arr []int64) *FenwickTree {
	if len(arr) == 0 {
		panic("input array cannot be empty")
	}

	n := len(arr)
	ft := &FenwickTree{
		size:   n,
		tree:   make([]int64, n+1),
		origin: make([]int64, n+1),
	}

	// Copy original values
	for i := 0; i < n; i++ {
		ft.origin[i+1] = arr[i]
	}

	// Build tree in O(n) time
	for i := 1; i <= n; i++ {
		ft.tree[i] += ft.origin[i]
		j := i + lsb(i)
		if j <= n {
			ft.tree[j] += ft.tree[i]
		}
	}

	return ft
}

// lsb returns the lowest significant bit (rightmost set bit) of i.
func lsb(i int) int {
	return i & (-i)
}

// Size returns the size of the tree.
func (ft *FenwickTree) Size() int {
	return ft.size
}

// Update adds a delta value to the element at index i.
// Index is 1-based.
func (ft *FenwickTree) Update(index int, delta int64) error {
	if index < 1 || index > ft.size {
		return ErrIndexOutOfRange
	}

	ft.origin[index] += delta
	for i := index; i <= ft.size; i += lsb(i) {
		ft.tree[i] += delta
	}
	return nil
}

// Set sets the value at index i to the specified value.
// Index is 1-based.
func (ft *FenwickTree) Set(index int, value int64) error {
	if index < 1 || index > ft.size {
		return ErrIndexOutOfRange
	}

	delta := value - ft.origin[index]
	ft.origin[index] = value
	for i := index; i <= ft.size; i += lsb(i) {
		ft.tree[i] += delta
	}
	return nil
}

// PrefixSum returns the sum of elements from index 1 to index i.
// Index is 1-based.
func (ft *FenwickTree) PrefixSum(index int) (int64, error) {
	if index < 0 {
		return 0, ErrNegativeIndex
	}
	if index > ft.size {
		index = ft.size
	}

	var sum int64
	for i := index; i > 0; i -= lsb(i) {
		sum += ft.tree[i]
	}
	return sum, nil
}

// Sum returns the prefix sum from 1 to index.
// Alias for PrefixSum.
func (ft *FenwickTree) Sum(index int) (int64, error) {
	return ft.PrefixSum(index)
}

// RangeSum returns the sum of elements from index left to index right (inclusive).
// Both indices are 1-based.
func (ft *FenwickTree) RangeSum(left, right int) (int64, error) {
	if left < 1 || right > ft.size {
		return 0, ErrIndexOutOfRange
	}
	if left > right {
		return 0, ErrInvalidRange
	}

	sumRight, _ := ft.PrefixSum(right)
	sumLeft, _ := ft.PrefixSum(left - 1)
	return sumRight - sumLeft, nil
}

// Value returns the value at a specific index.
// Index is 1-based.
func (ft *FenwickTree) Value(index int) (int64, error) {
	if index < 1 || index > ft.size {
		return 0, ErrIndexOutOfRange
	}
	return ft.origin[index], nil
}

// Find finds the smallest index where prefix sum >= target.
// This is the inverse operation of prefix sum.
// Uses binary search on the tree structure for O(log n) complexity.
func (ft *FenwickTree) Find(target int64) (int, error) {
	if target <= 0 {
		return 0, nil
	}

	// Find the largest power of 2 <= size
	pos := 0
	bitMask := highestBit(ft.size)

	for bitMask != 0 {
		nextPos := pos + bitMask
		if nextPos <= ft.size && ft.tree[nextPos] < target {
			target -= ft.tree[nextPos]
			pos = nextPos
		}
		bitMask >>= 1
	}

	if pos >= ft.size {
		return ft.size, nil
	}

	return pos + 1, nil
}

// FindFirst returns the first index where prefix sum >= target.
// Alias for Find.
func (ft *FenwickTree) FindFirst(target int64) (int, error) {
	return ft.Find(target)
}

// highestBit returns the highest power of 2 <= n.
func highestBit(n int) int {
	if n <= 0 {
		return 0
	}
	result := 1
	for result <= n {
		result <<= 1
	}
	return result >> 1
}

// Total returns the total sum of all elements.
func (ft *FenwickTree) Total() int64 {
	sum, _ := ft.PrefixSum(ft.size)
	return sum
}

// Clear resets all values to 0.
func (ft *FenwickTree) Clear() {
	for i := 0; i <= ft.size; i++ {
		ft.tree[i] = 0
		ft.origin[i] = 0
	}
}

// Clone creates a deep copy of the tree.
func (ft *FenwickTree) Clone() *FenwickTree {
	newTree := &FenwickTree{
		size:   ft.size,
		tree:   make([]int64, ft.size+1),
		origin: make([]int64, ft.size+1),
	}
	copy(newTree.tree, ft.tree)
	copy(newTree.origin, ft.origin)
	return newTree
}

// ToArray returns all values as an array (0-indexed).
func (ft *FenwickTree) ToArray() []int64 {
	result := make([]int64, ft.size)
	for i := 1; i <= ft.size; i++ {
		result[i-1] = ft.origin[i]
	}
	return result
}

// ToPrefixArray returns all prefix sums as an array (0-indexed).
func (ft *FenwickTree) ToPrefixArray() []int64 {
	result := make([]int64, ft.size)
	for i := 1; i <= ft.size; i++ {
		result[i-1], _ = ft.PrefixSum(i)
	}
	return result
}

// ============================================
// FenwickTreeMin - For range minimum queries
// ============================================

// FenwickTreeMin supports range minimum queries with point updates.
// Uses inverted operations (updates subtract, queries find minimum).
type FenwickTreeMin struct {
	size   int
	tree1  []int64 // For prefix minimum
	tree2  []int64 // For suffix minimum
	origin []int64
}

// NewMin creates a Fenwick Tree for minimum queries.
// Initialize with a large positive value or specified initial values.
func NewMin(size int, initialValue int64) *FenwickTreeMin {
	if size <= 0 {
		panic("fenwick tree size must be positive")
	}

	ft := &FenwickTreeMin{
		size:   size,
		tree1:  make([]int64, size+1),
		tree2:  make([]int64, size+1),
		origin: make([]int64, size+1),
	}

	// Initialize with max value (so any update will be smaller)
	for i := 0; i <= size; i++ {
		ft.tree1[i] = initialValue
		ft.tree2[i] = initialValue
		ft.origin[i] = initialValue
	}

	return ft
}

// NewMinFromArray creates a min-Fenwick Tree from an existing array.
func NewMinFromArray(arr []int64) *FenwickTreeMin {
	if len(arr) == 0 {
		panic("input array cannot be empty")
	}

	n := len(arr)
	ft := &FenwickTreeMin{
		size:   n,
		tree1:  make([]int64, n+1),
		tree2:  make([]int64, n+1),
		origin: make([]int64, n+1),
	}

	// Copy original values
	for i := 0; i < n; i++ {
		ft.origin[i+1] = arr[i]
	}

	// Build trees
	for i := 1; i <= n; i++ {
		ft.tree1[i] = ft.origin[i]
		ft.tree2[i] = ft.origin[i]
	}

	return ft
}

// UpdateMin updates the minimum at index i.
func (ft *FenwickTreeMin) UpdateMin(index int, value int64) error {
	if index < 1 || index > ft.size {
		return ErrIndexOutOfRange
	}

	ft.origin[index] = value

	// Update tree1 (prefix minimums)
	for i := index; i <= ft.size; i += lsb(i) {
		if value < ft.tree1[i] {
			ft.tree1[i] = value
		}
	}

	// Update tree2 (suffix minimums)
	for i := index; i > 0; i -= lsb(i) {
		if value < ft.tree2[i] {
			ft.tree2[i] = value
		}
	}

	return nil
}

// RangeMin returns the minimum in range [left, right].
func (ft *FenwickTreeMin) RangeMin(left, right int) (int64, error) {
	if left < 1 || right > ft.size {
		return 0, ErrIndexOutOfRange
	}
	if left > right {
		return 0, ErrInvalidRange
	}

	minVal := ft.origin[right]

	// Query from right side
	for i := right; i >= left; {
		next := i - lsb(i)
		if next >= left-1 {
			if ft.tree2[i] < minVal {
				minVal = ft.tree2[i]
			}
			i = next
		} else {
			if ft.origin[i] < minVal {
				minVal = ft.origin[i]
			}
			i--
		}
	}

	return minVal, nil
}

// ============================================
// FenwickTreeMax - For range maximum queries
// ============================================

// FenwickTreeMax supports range maximum queries.
type FenwickTreeMax struct {
	size   int
	tree1  []int64
	tree2  []int64
	origin []int64
}

// NewMax creates a Fenwick Tree for maximum queries.
func NewMax(size int, initialValue int64) *FenwickTreeMax {
	if size <= 0 {
		panic("fenwick tree size must be positive")
	}

	ft := &FenwickTreeMax{
		size:   size,
		tree1:  make([]int64, size+1),
		tree2:  make([]int64, size+1),
		origin: make([]int64, size+1),
	}

	// Initialize with min value
	for i := 0; i <= size; i++ {
		ft.tree1[i] = initialValue
		ft.tree2[i] = initialValue
		ft.origin[i] = initialValue
	}

	return ft
}

// UpdateMax updates the maximum at index i.
func (ft *FenwickTreeMax) UpdateMax(index int, value int64) error {
	if index < 1 || index > ft.size {
		return ErrIndexOutOfRange
	}

	ft.origin[index] = value

	for i := index; i <= ft.size; i += lsb(i) {
		if value > ft.tree1[i] {
			ft.tree1[i] = value
		}
	}

	for i := index; i > 0; i -= lsb(i) {
		if value > ft.tree2[i] {
			ft.tree2[i] = value
		}
	}

	return nil
}

// RangeMax returns the maximum in range [left, right].
func (ft *FenwickTreeMax) RangeMax(left, right int) (int64, error) {
	if left < 1 || right > ft.size {
		return 0, ErrIndexOutOfRange
	}
	if left > right {
		return 0, ErrInvalidRange
	}

	maxVal := ft.origin[right]

	for i := right; i >= left; {
		next := i - lsb(i)
		if next >= left-1 {
			if ft.tree2[i] > maxVal {
				maxVal = ft.tree2[i]
			}
			i = next
		} else {
			if ft.origin[i] > maxVal {
				maxVal = ft.origin[i]
			}
			i--
		}
	}

	return maxVal, nil
}

// ============================================
// FenwickTree2D - For 2D matrix operations
// ============================================

// FenwickTree2D represents a 2D Fenwick Tree for matrix sum queries.
type FenwickTree2D struct {
	rows   int
	cols   int
	tree   [][]int64
	origin [][]int64
}

// New2D creates a 2D Fenwick Tree with specified dimensions.
func New2D(rows, cols int) *FenwickTree2D {
	if rows <= 0 || cols <= 0 {
		panic("dimensions must be positive")
	}

	return &FenwickTree2D{
		rows:   rows,
		cols:   cols,
		tree:   make2DArray(rows+1, cols+1),
		origin: make2DArray(rows+1, cols+1),
	}
}

// New2DFromArray creates a 2D Fenwick Tree from an existing matrix.
func New2DFromArray(matrix [][]int64) *FenwickTree2D {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		panic("matrix cannot be empty")
	}

	rows := len(matrix)
	cols := len(matrix[0])

	ft := &FenwickTree2D{
		rows:   rows,
		cols:   cols,
		tree:   make2DArray(rows+1, cols+1),
		origin: make2DArray(rows+1, cols+1),
	}

	// Copy values and build tree
	for i := 1; i <= rows; i++ {
		for j := 1; j <= cols; j++ {
			ft.origin[i][j] = matrix[i-1][j-1]
		}
	}

	for i := 1; i <= rows; i++ {
		for j := 1; j <= cols; j++ {
			val := ft.origin[i][j]
			for ii := i; ii <= rows; ii += lsb(ii) {
				for jj := j; jj <= cols; jj += lsb(jj) {
					ft.tree[ii][jj] += val
				}
			}
		}
	}

	return ft
}

func make2DArray(rows, cols int) [][]int64 {
	arr := make([][]int64, rows)
	for i := range arr {
		arr[i] = make([]int64, cols)
	}
	return arr
}

// Update2D adds a delta value to element at (row, col).
func (ft *FenwickTree2D) Update2D(row, col int, delta int64) error {
	if row < 1 || row > ft.rows || col < 1 || col > ft.cols {
		return ErrIndexOutOfRange
	}

	ft.origin[row][col] += delta
	for i := row; i <= ft.rows; i += lsb(i) {
		for j := col; j <= ft.cols; j += lsb(j) {
			ft.tree[i][j] += delta
		}
	}
	return nil
}

// PrefixSum2D returns sum of elements from (1,1) to (row, col).
func (ft *FenwickTree2D) PrefixSum2D(row, col int) (int64, error) {
	if row < 0 || col < 0 {
		return 0, ErrNegativeIndex
	}
	if row > ft.rows {
		row = ft.rows
	}
	if col > ft.cols {
		col = ft.cols
	}

	var sum int64
	for i := row; i > 0; i -= lsb(i) {
		for j := col; j > 0; j -= lsb(j) {
			sum += ft.tree[i][j]
		}
	}
	return sum, nil
}

// RangeSum2D returns sum of elements in rectangle (r1,c1) to (r2,c2).
func (ft *FenwickTree2D) RangeSum2D(r1, c1, r2, c2 int) (int64, error) {
	if r1 < 1 || c1 < 1 || r2 > ft.rows || c2 > ft.cols {
		return 0, ErrIndexOutOfRange
	}
	if r1 > r2 || c1 > c2 {
		return 0, ErrInvalidRange
	}

	// Use inclusion-exclusion
	sumR2C2, _ := ft.PrefixSum2D(r2, c2)
	sumR1C2, _ := ft.PrefixSum2D(r1-1, c2)
	sumR2C1, _ := ft.PrefixSum2D(r2, c1-1)
	sumR1C1, _ := ft.PrefixSum2D(r1-1, c1-1)

	return sumR2C2 - sumR1C2 - sumR2C1 + sumR1C1, nil
}

// Value2D returns the value at (row, col).
func (ft *FenwickTree2D) Value2D(row, col int) (int64, error) {
	if row < 1 || row > ft.rows || col < 1 || col > ft.cols {
		return 0, ErrIndexOutOfRange
	}
	return ft.origin[row][col], nil
}

// Total2D returns the total sum of all elements.
func (ft *FenwickTree2D) Total2D() int64 {
	sum, _ := ft.PrefixSum2D(ft.rows, ft.cols)
	return sum
}

// ============================================
// FenwickTreeDiff - For range updates, point queries
// ============================================

// FenwickTreeDiff supports range updates and point queries.
// Uses difference array technique.
type FenwickTreeDiff struct {
	*FenwickTree
}

// NewDiff creates a Fenwick Tree for range updates.
func NewDiff(size int) *FenwickTreeDiff {
	return &FenwickTreeDiff{FenwickTree: New(size)}
}

// RangeUpdate adds delta to all elements in range [left, right].
func (ft *FenwickTreeDiff) RangeUpdate(left, right int, delta int64) error {
	if left < 1 || right > ft.size || left > right {
		return ErrInvalidRange
	}

	// Update at left and right+1 (difference array technique)
	ft.Update(left, delta)
	if right < ft.size {
		ft.Update(right+1, -delta)
	}
	return nil
}

// PointQuery returns the value at a single point after range updates.
func (ft *FenwickTreeDiff) PointQuery(index int) (int64, error) {
	return ft.PrefixSum(index)
}

// ============================================
// Utility Functions
// ============================================

// CountInRange counts elements with values in a range (requires sorted values).
// Uses two Find operations for efficient counting.
func CountInRange(ft *FenwickTree, minVal, maxVal int64) (int, error) {
	// This requires the tree to be built on frequency counts
	// where origin[i] represents count of elements with value i
	lowIdx, _ := ft.Find(minVal)
	highIdx, _ := ft.Find(maxVal + 1)
	return highIdx - lowIdx, nil
}

// Quantile finds the value at a given quantile position.
// Position should be between 1 and total sum.
func Quantile(ft *FenwickTree, position int64) (int, error) {
	if position <= 0 {
		return 0, ErrNegativeIndex
	}
	return ft.Find(position)
}

// Median finds the median position in the tree.
func Median(ft *FenwickTree) (int, error) {
	total := ft.Total()
	if total == 0 {
		return 0, ErrEmptyTree
	}
	return ft.Find(total / 2)
}

// Percentile finds the value at a given percentile (0-100).
func Percentile(ft *FenwickTree, pct float64) (int, error) {
	if pct < 0 || pct > 100 {
		return 0, errors.New("percentile must be between 0 and 100")
	}

	total := ft.Total()
	if total == 0 {
		return 0, ErrEmptyTree
	}

	position := int64(float64(total) * pct / 100)
	if position == 0 {
		position = 1
	}

	return ft.Find(position)
}

// Interpolate finds a fractional index for a given target sum.
// Useful for weighted averages and interpolation.
func Interpolate(ft *FenwickTree, target int64) (float64, error) {
	if target <= 0 {
		return 0, nil
	}

	idx, err := ft.Find(target)
	if err != nil {
		return 0, err
	}

	if idx == 0 {
		return 0, nil
	}

	// Get prefix sum just before this index
	prevSum, _ := ft.PrefixSum(idx - 1)
	value, _ := ft.Value(idx)

	// Interpolate within the element at idx
	if value == 0 {
		return float64(idx), nil
	}

	return float64(idx-1) + float64(target-prevSum)/float64(value), nil
}

// Scale multiplies all values by a factor.
func Scale(ft *FenwickTree, factor int64) {
	for i := 1; i <= ft.size; i++ {
		ft.Set(i, ft.origin[i]*factor)
	}
}

// Shift adds a constant to all values.
func Shift(ft *FenwickTree, constant int64) {
	for i := 1; i <= ft.size; i++ {
		ft.Update(i, constant)
	}
}

// Merge combines two Fenwick trees of the same size.
func Merge(ft1, ft2 *FenwickTree) (*FenwickTree, error) {
	if ft1.size != ft2.size {
		return nil, errors.New("trees must have same size")
	}

	result := New(ft1.size)
	for i := 1; i <= ft1.size; i++ {
		val1, _ := ft1.Value(i)
		val2, _ := ft2.Value(i)
		result.Set(i, val1+val2)
	}

	return result, nil
}

// CumulativeFrequency returns cumulative frequency at each index.
// Useful for visualizing the distribution.
func CumulativeFrequency(ft *FenwickTree) []int64 {
	return ft.ToPrefixArray()
}

// FindAll finds all indices where prefix sum crosses thresholds.
// Returns indices for each threshold value.
func FindAll(ft *FenwickTree, thresholds []int64) ([]int, error) {
	result := make([]int, len(thresholds))
	for i, threshold := range thresholds {
		idx, err := ft.Find(threshold)
		if err != nil {
			return nil, err
		}
		result[i] = idx
	}
	return result, nil
}

// GcdTree creates a Fenwick Tree-like structure for GCD queries.
// Note: GCD doesn't have an inverse, so we use a different approach.
type GcdTree struct {
	size   int
	tree   []int64
	origin []int64
}

// NewGcd creates a tree for GCD queries.
func NewGcd(size int) *GcdTree {
	if size <= 0 {
		panic("size must be positive")
	}
	return &GcdTree{
		size:   size,
		tree:   make([]int64, size+1),
		origin: make([]int64, size+1),
	}
}

// gcd computes the greatest common divisor.
func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

// UpdateGcd updates a value in the GCD tree.
func (gt *GcdTree) UpdateGcd(index int, value int64) error {
	if index < 1 || index > gt.size {
		return ErrIndexOutOfRange
	}

	gt.origin[index] = value
	// Recompute tree (simplified - not true BIT structure)
	for i := index; i <= gt.size; i += lsb(i) {
		gt.tree[i] = value
		for j := i - lsb(i) + 1; j < i; j++ {
			gt.tree[i] = gcd(gt.tree[i], gt.origin[j])
		}
	}
	return nil
}

// RangeGcd returns GCD of elements in [left, right].
func (gt *GcdTree) RangeGcd(left, right int) (int64, error) {
	if left < 1 || right > gt.size || left > right {
		return 0, ErrInvalidRange
	}

	result := gt.origin[left]
	for i := left + 1; i <= right; i++ {
		result = gcd(result, gt.origin[i])
	}
	return result, nil
}

// ============================================
// Batch Operations
// ============================================

// BatchUpdate applies multiple updates efficiently.
func (ft *FenwickTree) BatchUpdate(updates map[int]int64) error {
	for index, delta := range updates {
		if err := ft.Update(index, delta); err != nil {
			return err
		}
	}
	return nil
}

// BatchRangeSum computes multiple range sums.
func (ft *FenwickTree) BatchRangeSum(ranges []struct{ L, R int }) ([]int64, error) {
	results := make([]int64, len(ranges))
	for i, r := range ranges {
		sum, err := ft.RangeSum(r.L, r.R)
		if err != nil {
			return nil, err
		}
		results[i] = sum
	}
	return results, nil
}

// Compress compresses sparse values to dense indices.
// Useful for frequency trees with large value ranges.
func Compress(values []int64) (map[int64]int, []int64) {
	unique := make(map[int64]bool)
	for _, v := range values {
		unique[v] = true
	}

	sorted := make([]int64, 0, len(unique))
	for v := range unique {
		sorted = append(sorted, v)
	}
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i] < sorted[j]
	})

	mapping := make(map[int64]int)
	for i, v := range sorted {
		mapping[v] = i + 1 // 1-indexed
	}

	return mapping, sorted
}

// NewCompressed creates a Fenwick Tree with compressed coordinates.
func NewCompressed(values []int64) (*FenwickTree, map[int64]int) {
	mapping, _ := Compress(values)
	ft := New(len(mapping))
	return ft, mapping
}

// UpdateCompressed updates using compressed coordinates.
func UpdateCompressed(ft *FenwickTree, mapping map[int64]int, originalValue int64, delta int64) error {
	compressedIdx, ok := mapping[originalValue]
	if !ok {
		return errors.New("value not in compressed mapping")
	}
	return ft.Update(compressedIdx, delta)
}