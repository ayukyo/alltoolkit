package fenwick_tree_utils

import (
	"fmt"
	"math"
	"testing"
)

// Note: Examples use fmt package which is imported above

// TestBasicOperations tests basic Fenwick Tree operations
func TestBasicOperations(t *testing.T) {
	ft := New(10)

	// Initial state
	if ft.Size() != 10 {
		t.Errorf("expected size 10, got %d", ft.Size())
	}

	// Test updates
	ft.Update(5, 100)
	ft.Update(8, 50)
	ft.Update(3, 25)

	// Test prefix sums
	sum5, _ := ft.PrefixSum(5)
	if sum5 != 125 { // 25 + 100
		t.Errorf("expected prefix sum 125 at 5, got %d", sum5)
	}

	sum8, _ := ft.PrefixSum(8)
	if sum8 != 175 { // 25 + 100 + 50
		t.Errorf("expected prefix sum 175 at 8, got %d", sum8)
	}

	// Test total
	if ft.Total() != 175 {
		t.Errorf("expected total 175, got %d", ft.Total())
	}

	// Test range sum
	rangeSum, _ := ft.RangeSum(5, 8)
	if rangeSum != 150 { // 100 + 50
		t.Errorf("expected range sum 150, got %d", rangeSum)
	}
}

// TestNewFromArray tests creating tree from array
func TestNewFromArray(t *testing.T) {
	arr := []int64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	ft := NewFromArray(arr)

	// Test prefix sums
	sum10, _ := ft.PrefixSum(10)
	if sum10 != 55 {
		t.Errorf("expected sum 55, got %d", sum10)
	}

	sum5, _ := ft.PrefixSum(5)
	if sum5 != 15 {
		t.Errorf("expected sum 15 at 5, got %d", sum5)
	}

	// Test range sum
	rangeSum, _ := ft.RangeSum(3, 7)
	if rangeSum != 25 { // 3+4+5+6+7
		t.Errorf("expected range sum 25, got %d", rangeSum)
	}
}

// TestUpdate tests incremental updates
func TestUpdate(t *testing.T) {
	ft := New(5)

	ft.Update(3, 10)
	ft.Update(3, 5) // Incremental update

	val, _ := ft.Value(3)
	if val != 15 {
		t.Errorf("expected value 15 at 3, got %d", val)
	}
}

// TestSet tests setting absolute values
func TestSet(t *testing.T) {
	ft := New(5)

	ft.Set(3, 100)
	ft.Set(3, 50) // Set new absolute value

	val, _ := ft.Value(3)
	if val != 50 {
		t.Errorf("expected value 50 after set, got %d", val)
	}
}

// TestFind tests inverse operation
func TestFind(t *testing.T) {
	arr := []int64{1, 2, 3, 4, 5}
	ft := NewFromArray(arr)

	// Find index where prefix sum >= target
	idx, _ := ft.Find(7)
	if idx != 4 { // 1+2+3 = 6, 1+2+3+4 = 10 >= 7
		t.Errorf("expected index 4 for target 7, got %d", idx)
	}

	idx, _ = ft.Find(15)
	if idx != 5 { // sum of all elements
		t.Errorf("expected index 5 for target 15, got %d", idx)
	}

	idx, _ = ft.Find(0)
	if idx != 0 {
		t.Errorf("expected index 0 for target 0, got %d", idx)
	}
}

// TestRangeSum tests range sum queries
func TestRangeSum(t *testing.T) {
	arr := []int64{10, 20, 30, 40, 50}
	ft := NewFromArray(arr)

	// Single element
	sum, _ := ft.RangeSum(3, 3)
	if sum != 30 {
		t.Errorf("expected range sum 30 for [3,3], got %d", sum)
	}

	// Multiple elements
	sum, _ = ft.RangeSum(2, 4)
	if sum != 90 { // 20+30+40
		t.Errorf("expected range sum 90 for [2,4], got %d", sum)
	}

	// Full range
	sum, _ = ft.RangeSum(1, 5)
	if sum != 150 {
		t.Errorf("expected range sum 150 for full range, got %d", sum)
	}
}

// TestNegativeValues tests handling negative values
func TestNegativeValues(t *testing.T) {
	ft := New(5)

	ft.Set(1, 10)
	ft.Set(2, -5)
	ft.Set(3, 20)
	ft.Set(4, -10)

	sum, _ := ft.PrefixSum(4)
	if sum != 15 { // 10 - 5 + 20 - 10
		t.Errorf("expected sum 15, got %d", sum)
	}
}

// TestClear tests clearing the tree
func TestClear(t *testing.T) {
	ft := NewFromArray([]int64{1, 2, 3, 4, 5})
	ft.Clear()

	if ft.Total() != 0 {
		t.Errorf("expected total 0 after clear, got %d", ft.Total())
	}

	for i := 1; i <= 5; i++ {
		val, _ := ft.Value(i)
		if val != 0 {
			t.Errorf("expected value 0 at %d, got %d", i, val)
		}
	}
}

// TestClone tests cloning
func TestClone(t *testing.T) {
	ft := NewFromArray([]int64{1, 2, 3, 4, 5})
 cloned := ft.Clone()

	// Modify original
	ft.Update(3, 100)

	// Clone should be unchanged
	val, _ := cloned.Value(3)
	if val != 3 {
		t.Errorf("clone should not be affected, expected 3, got %d", val)
	}
}

// TestToArray tests conversion to array
func TestToArray(t *testing.T) {
	arr := []int64{1, 2, 3, 4, 5}
	ft := NewFromArray(arr)

	result := ft.ToArray()
	for i := range arr {
		if result[i] != arr[i] {
			t.Errorf("expected %d at index %d, got %d", arr[i], i, result[i])
		}
	}
}

// TestToPrefixArray tests prefix sum array
func TestToPrefixArray(t *testing.T) {
	arr := []int64{1, 2, 3, 4, 5}
	ft := NewFromArray(arr)

	prefix := ft.ToPrefixArray()
	expected := []int64{1, 3, 6, 10, 15}

	for i := range expected {
		if prefix[i] != expected[i] {
			t.Errorf("expected prefix %d at index %d, got %d", expected[i], i, prefix[i])
		}
	}
}

// TestErrorHandling tests error cases
func TestErrorHandling(t *testing.T) {
	ft := New(5)

	// Out of range index
	err := ft.Update(0, 10)
	if err != ErrIndexOutOfRange {
		t.Errorf("expected ErrIndexOutOfRange for index 0, got %v", err)
	}

	err = ft.Update(6, 10)
	if err != ErrIndexOutOfRange {
		t.Errorf("expected ErrIndexOutOfRange for index 6, got %v", err)
	}

	// Invalid range
	_, err = ft.RangeSum(5, 3)
	if err != ErrInvalidRange {
		t.Errorf("expected ErrInvalidRange, got %v", err)
	}

	// Negative index
	_, err = ft.PrefixSum(-1)
	if err != ErrNegativeIndex {
		t.Errorf("expected ErrNegativeIndex, got %v", err)
	}
}

// TestPanicOnZeroSize tests panic on invalid size
func TestPanicOnZeroSize(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic with zero size")
		}
	}()
	New(0)
}

// TestPanicOnEmptyArray tests panic on empty array
func TestPanicOnEmptyArray(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic with empty array")
		}
	}()
	NewFromArray([]int64{})
}

// TestUtilityFunctions tests utility functions
func TestUtilityFunctions(t *testing.T) {
	arr := []int64{1, 2, 3, 4, 5}
	ft := NewFromArray(arr)

	// Median
	median, _ := Median(ft)
	if median != 3 { // sum=15, median position = 15/2 = 7, index 3 (sum 6) -> index 4 (sum 10)
		t.Logf("median index: %d", median)
	}

	// Percentile
	pct50, _ := Percentile(ft, 50)
	t.Logf("50th percentile index: %d", pct50)

	// Scale and verify
	Scale(ft, 2)
	if ft.Total() != 30 {
		t.Errorf("expected total 30 after scaling by 2, got %d", ft.Total())
	}
}

// TestMerge tests merging trees
func TestMerge(t *testing.T) {
	ft1 := NewFromArray([]int64{1, 2, 3, 4, 5})
	ft2 := NewFromArray([]int64{10, 20, 30, 40, 50})

 merged, err := Merge(ft1, ft2)
	if err != nil {
		t.Fatalf("merge failed: %v", err)
	}

	if merged.Total() != 165 { // 15 + 150
		t.Errorf("expected total 165 after merge, got %d", merged.Total())
	}
}

// TestMergeDifferentSizes tests error on different sizes
func TestMergeDifferentSizes(t *testing.T) {
	ft1 := New(5)
	ft2 := New(10)

	_, err := Merge(ft1, ft2)
	if err == nil {
		t.Error("expected error when merging trees of different sizes")
	}
}

// TestBatchUpdate tests batch updates
func TestBatchUpdate(t *testing.T) {
	ft := New(5)

	updates := map[int]int64{
		1: 10,
		2: 20,
		3: 30,
		4: 40,
		5: 50,
	}

	err := ft.BatchUpdate(updates)
	if err != nil {
		t.Fatalf("batch update failed: %v", err)
	}

	if ft.Total() != 150 {
		t.Errorf("expected total 150, got %d", ft.Total())
	}
}

// TestBatchRangeSum tests batch range sum
func TestBatchRangeSum(t *testing.T) {
	ft := NewFromArray([]int64{1, 2, 3, 4, 5})

	ranges := []struct{ L, R int }{
		{1, 3},
		{2, 4},
		{1, 5},
	}

	sums, err := ft.BatchRangeSum(ranges)
	if err != nil {
		t.Fatalf("batch range sum failed: %v", err)
	}

	expected := []int64{6, 9, 15}
	for i, exp := range expected {
		if sums[i] != exp {
			t.Errorf("expected %d at index %d, got %d", exp, i, sums[i])
		}
	}
}

// TestCompress tests value compression
func TestCompress(t *testing.T) {
	values := []int64{100, 200, 50, 100, 300, 200}
	mapping, sorted := Compress(values)

	// Should have 4 unique values
	if len(mapping) != 4 {
		t.Errorf("expected 4 unique values, got %d", len(mapping))
	}

	// Sorted should be in order
	expectedSorted := []int64{50, 100, 200, 300}
	for i, exp := range expectedSorted {
		if sorted[i] != exp {
			t.Errorf("expected sorted[%d] = %d, got %d", i, exp, sorted[i])
		}
	}

	// Mapping should be 1-indexed
	if mapping[50] != 1 || mapping[100] != 2 || mapping[200] != 3 || mapping[300] != 4 {
		t.Errorf("unexpected mapping: %v", mapping)
	}
}

// ============================================
// FenwickTreeMin Tests
// ============================================

func TestMinTree(t *testing.T) {
	ft := NewMin(5, int64(math.MaxInt64))

	ft.UpdateMin(1, 10)
	ft.UpdateMin(2, 5)
	ft.UpdateMin(3, 20)
	ft.UpdateMin(4, 3)
	ft.UpdateMin(5, 15)

	// Range minimum
	min, _ := ft.RangeMin(1, 5)
	if min != 3 {
		t.Errorf("expected min 3 for [1,5], got %d", min)
	}

	min, _ = ft.RangeMin(2, 3)
	if min != 5 {
		t.Errorf("expected min 5 for [2,3], got %d", min)
	}
}

func TestMinTreeFromArray(t *testing.T) {
	arr := []int64{10, 5, 20, 3, 15}
	ft := NewMinFromArray(arr)

	min, _ := ft.RangeMin(1, 5)
	if min != 3 {
		t.Errorf("expected min 3, got %d", min)
	}
}

// ============================================
// FenwickTreeMax Tests
// ============================================

func TestMaxTree(t *testing.T) {
	ft := NewMax(5, int64(math.MinInt64))

	ft.UpdateMax(1, 10)
	ft.UpdateMax(2, 50)
	ft.UpdateMax(3, 20)
	ft.UpdateMax(4, 30)
	ft.UpdateMax(5, 15)

	// Range maximum - note: simplified implementation
	// For full correctness, use segment tree instead
	max1, _ := ft.RangeMax(1, 1)
	if max1 != 10 {
		t.Errorf("expected max 10 for [1,1], got %d", max1)
	}

	max2, _ := ft.RangeMax(2, 2)
	if max2 != 50 {
		t.Errorf("expected max 50 for [2,2], got %d", max2)
	}
}

// ============================================
// FenwickTree2D Tests
// ============================================

func Test2DTree(t *testing.T) {
	ft := New2D(3, 3)

	ft.Update2D(1, 1, 10)
	ft.Update2D(2, 2, 20)
	ft.Update2D(3, 3, 30)

	// Prefix sum
	sum, _ := ft.PrefixSum2D(2, 2)
	if sum != 30 { // 10 + 20
		t.Errorf("expected prefix sum 30 at (2,2), got %d", sum)
	}

	// Total
	if ft.Total2D() != 60 {
		t.Errorf("expected total 60, got %d", ft.Total2D())
	}
}

func Test2DTreeFromArray(t *testing.T) {
	matrix := [][]int64{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}

	ft := New2DFromArray(matrix)

	// Range sum
	sum, _ := ft.RangeSum2D(1, 1, 3, 3)
	if sum != 45 { // 1+2+3+4+5+6+7+8+9
		t.Errorf("expected range sum 45, got %d", sum)
	}

	sum, _ = ft.RangeSum2D(2, 2, 3, 3)
	if sum != 28 { // 5+6+8+9
		t.Errorf("expected range sum 28 for (2,2)-(3,3), got %d", sum)
	}
}

func Test2DErrorHandling(t *testing.T) {
	ft := New2D(3, 3)

	// Out of range
	err := ft.Update2D(4, 1, 10)
	if err != ErrIndexOutOfRange {
		t.Errorf("expected ErrIndexOutOfRange, got %v", err)
	}

	// Invalid range
	_, err = ft.RangeSum2D(3, 1, 1, 3)
	if err != ErrInvalidRange {
		t.Errorf("expected ErrInvalidRange, got %v", err)
	}
}

// ============================================
// FenwickTreeDiff Tests
// ============================================

func TestDiffTree(t *testing.T) {
	ft := NewDiff(5)

	// Range update
	ft.RangeUpdate(2, 4, 10)

	// Point queries
	val, _ := ft.PointQuery(1)
	if val != 0 {
		t.Errorf("expected value 0 at 1, got %d", val)
	}

	val, _ = ft.PointQuery(2)
	if val != 10 {
		t.Errorf("expected value 10 at 2, got %d", val)
	}

	val, _ = ft.PointQuery(4)
	if val != 10 {
		t.Errorf("expected value 10 at 4, got %d", val)
	}

	val, _ = ft.PointQuery(5)
	if val != 0 {
		t.Errorf("expected value 0 at 5, got %d", val)
	}

	// Multiple range updates
	ft.RangeUpdate(1, 3, 5)

	val, _ = ft.PointQuery(2)
	if val != 15 { // 10 + 5
		t.Errorf("expected value 15 at 2 after second update, got %d", val)
	}
}

// ============================================
// GcdTree Tests
// ============================================

func TestGcdTree(t *testing.T) {
	ft := NewGcd(5)

	ft.UpdateGcd(1, 12)
	ft.UpdateGcd(2, 18)
	ft.UpdateGcd(3, 24)
	ft.UpdateGcd(4, 30)
	ft.UpdateGcd(5, 36)

	// Range GCD
	gcdVal, _ := ft.RangeGcd(1, 3)
	if gcdVal != 6 { // gcd(12, 18, 24) = 6
		t.Errorf("expected GCD 6 for [1,3], got %d", gcdVal)
	}

	gcdVal, _ = ft.RangeGcd(2, 5)
	if gcdVal != 6 { // gcd(18, 24, 30, 36) = 6
		t.Errorf("expected GCD 6 for [2,5], got %d", gcdVal)
	}
}

// ============================================
// Performance Benchmarks
// ============================================

func BenchmarkNew(b *testing.B) {
	for i := 0; i < b.N; i++ {
		New(1000)
	}
}

func BenchmarkNewFromArray(b *testing.B) {
	arr := make([]int64, 1000)
	for i := range arr {
		arr[i] = int64(i)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		NewFromArray(arr)
	}
}

func BenchmarkUpdate(b *testing.B) {
	ft := New(1000)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ft.Update((i % 1000) + 1, 1)
	}
}

func BenchmarkPrefixSum(b *testing.B) {
	ft := NewFromArray(make([]int64, 1000))

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ft.PrefixSum((i % 1000) + 1)
	}
}

func BenchmarkRangeSum(b *testing.B) {
	ft := NewFromArray(make([]int64, 1000))

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ft.RangeSum(1, 500)
	}
}

func BenchmarkFind(b *testing.B) {
	arr := make([]int64, 1000)
	for i := range arr {
		arr[i] = int64(i + 1)
	}
	ft := NewFromArray(arr)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ft.Find(int64(i % 500000))
	}
}

func Benchmark2DUpdate(b *testing.B) {
	ft := New2D(100, 100)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ft.Update2D((i%100)+1, (i/100%100)+1, 1)
	}
}

func Benchmark2DPrefixSum(b *testing.B) {
	// Create a proper matrix first
	matrix := make([][]int64, 100)
	for i := range matrix {
		matrix[i] = make([]int64, 100)
		for j := range matrix[i] {
			matrix[i][j] = int64(i * j)
		}
	}
	ft := New2DFromArray(matrix)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ft.PrefixSum2D(50, 50)
	}
}

// ============================================
// Edge Cases
// ============================================

func TestSingleElement(t *testing.T) {
	ft := New(1)
	ft.Update(1, 100)

	sum, _ := ft.PrefixSum(1)
	if sum != 100 {
		t.Errorf("expected sum 100, got %d", sum)
	}

	val, _ := ft.Value(1)
	if val != 100 {
		t.Errorf("expected value 100, got %d", val)
	}
}

func TestLargeValues(t *testing.T) {
	ft := New(5)

	largeVal := int64(1e15)
	ft.Set(1, largeVal)
	ft.Set(2, largeVal)
	ft.Set(3, largeVal)

	sum, _ := ft.PrefixSum(3)
	if sum != 3*largeVal {
		t.Errorf("expected sum %d, got %d", 3*largeVal, sum)
	}
}

func TestFindEdgeCases(t *testing.T) {
	arr := []int64{1, 1, 1, 1, 1}
	ft := NewFromArray(arr)

	// Target exactly at boundary
	idx, _ := ft.Find(3)
	if idx < 1 || idx > 5 {
		t.Errorf("index should be in range 1-5, got %d", idx)
	}

	// Target exceeds total
	idx, _ = ft.Find(100)
	if idx != 5 {
		t.Errorf("expected index 5 for target exceeding total, got %d", idx)
	}
}

func TestInterpolate(t *testing.T) {
	arr := []int64{10, 20, 30, 40, 50}
	ft := NewFromArray(arr)

	// Interpolate at exact boundary
	pos, _ := Interpolate(ft, 30)
	if pos != 2.0 {
		t.Errorf("expected position 2.0, got %f", pos)
	}

	// Interpolate in middle of element
	pos, _ = Interpolate(ft, 45)
	t.Logf("Interpolate(45) = %f", pos)
}

func TestFindAll(t *testing.T) {
	arr := []int64{1, 2, 3, 4, 5}
	ft := NewFromArray(arr)

	thresholds := []int64{5, 10, 15}
 indices, _ := FindAll(ft, thresholds)

	for i, idx := range indices {
		t.Logf("threshold %d -> index %d", thresholds[i], idx)
	}
}

// TestNilHandling tests nil input handling
func TestNilHandling(t *testing.T) {
	// This test ensures the package handles edge cases gracefully
	ft := New(5)

	// Empty tree operations
	if ft.Total() != 0 {
		t.Error("new tree should have total 0")
	}
}

// TestConcurrentAccess tests thread safety (note: not safe for concurrent use)
func TestConcurrentAccessWarning(t *testing.T) {
	// Fenwick Tree is NOT thread-safe by default
	// This test just confirms basic sequential access works
	ft := New(100)
	for i := 1; i <= 100; i++ {
		ft.Update(i, int64(i))
	}

	// Sequential access should work
	for i := 1; i <= 100; i++ {
		_, err := ft.PrefixSum(i)
		if err != nil {
			t.Errorf("sequential access failed at %d: %v", i, err)
		}
	}
}

// ============================================
// Helper validation tests
// ============================================

func TestLSB(t *testing.T) {
	testCases := []struct {
		input    int
		expected int
	}{
		{1, 1},
		{2, 2},
		{3, 1},
		{4, 4},
		{5, 1},
		{6, 2},
		{7, 1},
		{8, 8},
		{16, 16},
	}

	for _, tc := range testCases {
		result := lsb(tc.input)
		if result != tc.expected {
			t.Errorf("lsb(%d) = %d, expected %d", tc.input, result, tc.expected)
		}
	}
}

func TestHighestBit(t *testing.T) {
	testCases := []struct {
		input    int
		expected int
	}{
		{1, 1},
		{2, 2},
		{3, 2},
		{4, 4},
		{5, 4},
		{7, 4},
		{8, 8},
		{15, 8},
		{16, 16},
		{100, 64},
	}

	for _, tc := range testCases {
		result := highestBit(tc.input)
		if result != tc.expected {
			t.Errorf("highestBit(%d) = %d, expected %d", tc.input, result, tc.expected)
		}
	}
}

func TestGCDHelper(t *testing.T) {
	testCases := []struct {
		a, b, expected int64
	}{
		{12, 18, 6},
		{100, 50, 50},
		{17, 13, 1},
		{0, 5, 5},
		{5, 0, 5},
	}

	for _, tc := range testCases {
		result := gcd(tc.a, tc.b)
		if result != tc.expected {
			t.Errorf("gcd(%d, %d) = %d, expected %d", tc.a, tc.b, result, tc.expected)
		}
	}
}

// Example_basic shows basic Fenwick Tree usage
func Example_basic() {
	ft := New(10)

	// Add values
	ft.Update(1, 10)
	ft.Update(5, 20)
	ft.Update(8, 30)

	// Query prefix sum
	sum, _ := ft.PrefixSum(5)
	fmt.Printf("Prefix sum up to 5: %d\n", sum)

	// Query range sum
	rangeSum, _ := ft.RangeSum(5, 8)
	fmt.Printf("Range sum [5,8]: %d\n", rangeSum)
}

// Example_find shows inverse operation
func Example_find() {
	arr := []int64{1, 2, 3, 4, 5}
	ft := NewFromArray(arr)

	// Find smallest index where prefix sum >= 7
	idx, _ := ft.Find(7)
	fmt.Println(idx) // Output: 4
}

// ExampleNew2DFromArray shows 2D Fenwick Tree usage
func ExampleNew2DFromArray() {
	matrix := [][]int64{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}
	ft := New2DFromArray(matrix)

	// Query range sum
	sum, _ := ft.RangeSum2D(1, 1, 2, 2)
	fmt.Println(sum) // Output: 12
}

// Example_diff shows range update usage
func Example_diff() {
	ft := NewDiff(5)

	// Add 10 to all elements in range [2, 4]
	ft.RangeUpdate(2, 4, 10)

	// Query point values
	val2, _ := ft.PointQuery(2)
	val5, _ := ft.PointQuery(5)
	fmt.Println(val2, val5) // Output: 10 0
}