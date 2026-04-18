package slice_utils

import (
	"math/rand"
	"sort"
	"testing"
)

// =============================================================================
// Basic Operations Tests
// =============================================================================

func TestContains(t *testing.T) {
	tests := []struct {
		slice    []int
		element  int
		expected bool
	}{
		{[]int{1, 2, 3}, 2, true},
		{[]int{1, 2, 3}, 4, false},
		{[]int{}, 1, false},
		{[]int{1, 1, 1}, 1, true},
	}

	for _, test := range tests {
		result := Contains(test.slice, test.element)
		if result != test.expected {
			t.Errorf("Contains(%v, %d) = %v; want %v", test.slice, test.element, result, test.expected)
		}
	}
}

func TestContainsString(t *testing.T) {
	slice := []string{"a", "b", "c"}
	if !Contains(slice, "b") {
		t.Error("Expected to contain 'b'")
	}
	if Contains(slice, "d") {
		t.Error("Expected not to contain 'd'")
	}
}

func TestContainsAll(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if !ContainsAll(slice, []int{2, 4}) {
		t.Error("Expected to contain all")
	}
	if ContainsAll(slice, []int{2, 6}) {
		t.Error("Expected not to contain all")
	}
}

func TestContainsAny(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if !ContainsAny(slice, []int{6, 2}) {
		t.Error("Expected to contain any")
	}
	if ContainsAny(slice, []int{6, 7}) {
		t.Error("Expected not to contain any")
	}
}

func TestIndexOf(t *testing.T) {
	tests := []struct {
		slice    []int
		element  int
		expected int
	}{
		{[]int{1, 2, 3}, 2, 1},
		{[]int{1, 2, 3}, 4, -1},
		{[]int{1, 2, 2, 3}, 2, 1},
		{[]int{}, 1, -1},
	}

	for _, test := range tests {
		result := IndexOf(test.slice, test.element)
		if result != test.expected {
			t.Errorf("IndexOf(%v, %d) = %d; want %d", test.slice, test.element, result, test.expected)
		}
	}
}

func TestLastIndexOf(t *testing.T) {
	slice := []int{1, 2, 2, 3, 2}
	if result := LastIndexOf(slice, 2); result != 4 {
		t.Errorf("LastIndexOf(%v, 2) = %d; want 4", slice, result)
	}
	if result := LastIndexOf(slice, 5); result != -1 {
		t.Errorf("LastIndexOf(%v, 5) = %d; want -1", slice, result)
	}
}

func TestCount(t *testing.T) {
	slice := []int{1, 2, 2, 3, 2, 2, 4}
	if result := Count(slice, 2); result != 4 {
		t.Errorf("Count(%v, 2) = %d; want 4", slice, result)
	}
	if result := Count(slice, 5); result != 0 {
		t.Errorf("Count(%v, 5) = %d; want 0", slice, result)
	}
}

func TestCountBy(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	result := CountBy(slice, func(n int) bool { return n%2 == 0 })
	if result != 3 {
		t.Errorf("CountBy(even) = %d; want 3", result)
	}
}

// =============================================================================
// Transformation Operations Tests
// =============================================================================

func TestMap(t *testing.T) {
	slice := []int{1, 2, 3}
	result := Map(slice, func(n int) int { return n * 2 })
	expected := []int{2, 4, 6}
	if !Equal(result, expected) {
		t.Errorf("Map(double) = %v; want %v", result, expected)
	}
}

func TestMapString(t *testing.T) {
	slice := []int{1, 2, 3}
	result := Map(slice, func(n int) string { return string(rune('a' + n - 1)) })
	expected := []string{"a", "b", "c"}
	if !Equal(result, expected) {
		t.Errorf("Map(to string) = %v; want %v", result, expected)
	}
}

func TestFilter(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	result := Filter(slice, func(n int) bool { return n%2 == 0 })
	expected := []int{2, 4, 6}
	if !Equal(result, expected) {
		t.Errorf("Filter(even) = %v; want %v", result, expected)
	}
}

func TestReject(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	result := Reject(slice, func(n int) bool { return n%2 == 0 })
	expected := []int{1, 3, 5}
	if !Equal(result, expected) {
		t.Errorf("Reject(even) = %v; want %v", result, expected)
	}
}

func TestReduce(t *testing.T) {
	slice := []int{1, 2, 3, 4}
	result := Reduce(slice, 0, func(acc, n int) int { return acc + n })
	if result != 10 {
		t.Errorf("Reduce(sum) = %d; want 10", result)
	}
}

func TestReduceWithStrings(t *testing.T) {
	slice := []string{"a", "b", "c"}
	result := Reduce(slice, "", func(acc, s string) string { return acc + s })
	if result != "abc" {
		t.Errorf("Reduce(concat) = %s; want abc", result)
	}
}

func TestReduceRight(t *testing.T) {
	slice := []string{"a", "b", "c"}
	result := ReduceRight(slice, "", func(acc, s string) string { return acc + s })
	if result != "cba" {
		t.Errorf("ReduceRight(concat) = %s; want cba", result)
	}
}

func TestForEach(t *testing.T) {
	slice := []int{1, 2, 3}
	sum := 0
	ForEach(slice, func(n int) { sum += n })
	if sum != 6 {
		t.Errorf("ForEach(sum) = %d; want 6", sum)
	}
}

func TestFlatMap(t *testing.T) {
	slice := []int{1, 2, 3}
	result := FlatMap(slice, func(n int) []int { return []int{n, n * 2} })
	expected := []int{1, 2, 2, 4, 3, 6}
	if !Equal(result, expected) {
		t.Errorf("FlatMap = %v; want %v", result, expected)
	}
}

// =============================================================================
// Slice Manipulation Tests
// =============================================================================

func TestChunk(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6, 7}
	result, err := Chunk(slice, 3)
	if err != nil {
		t.Fatalf("Chunk failed: %v", err)
	}
	if len(result) != 3 {
		t.Fatalf("Chunk length = %d; want 3", len(result))
	}
	if !Equal(result[0], []int{1, 2, 3}) {
		t.Errorf("Chunk[0] = %v; want [1, 2, 3]", result[0])
	}
	if !Equal(result[1], []int{4, 5, 6}) {
		t.Errorf("Chunk[1] = %v; want [4, 5, 6]", result[1])
	}
	if !Equal(result[2], []int{7}) {
		t.Errorf("Chunk[2] = %v; want [7]", result[2])
	}
}

func TestChunkInvalidSize(t *testing.T) {
	_, err := Chunk([]int{1, 2, 3}, 0)
	if err == nil {
		t.Error("Expected error for chunk size 0")
	}
}

func TestFlatten(t *testing.T) {
	slices := [][]int{{1, 2}, {3, 4}, {5}}
	result := Flatten(slices)
	expected := []int{1, 2, 3, 4, 5}
	if !Equal(result, expected) {
		t.Errorf("Flatten = %v; want %v", result, expected)
	}
}

func TestReverse(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	Reverse(slice)
	expected := []int{5, 4, 3, 2, 1}
	if !Equal(slice, expected) {
		t.Errorf("Reverse = %v; want %v", slice, expected)
	}
}

func TestReversed(t *testing.T) {
	slice := []int{1, 2, 3}
	result := Reversed(slice)
	expected := []int{3, 2, 1}
	if !Equal(result, expected) {
		t.Errorf("Reversed = %v; want %v", result, expected)
	}
	if !Equal(slice, []int{1, 2, 3}) {
		t.Errorf("Original slice was modified")
	}
}

func TestTake(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if !Equal(Take(slice, 3), []int{1, 2, 3}) {
		t.Error("Take(3) failed")
	}
	if !Equal(Take(slice, 10), []int{1, 2, 3, 4, 5}) {
		t.Error("Take(10) should return all elements")
	}
	if !Equal(Take(slice, 0), []int{}) {
		t.Error("Take(0) should return empty")
	}
}

func TestTakeWhile(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 1, 2}
	result := TakeWhile(slice, func(n int) bool { return n < 4 })
	if !Equal(result, []int{1, 2, 3}) {
		t.Errorf("TakeWhile(<4) = %v; want [1, 2, 3]", result)
	}
}

func TestTakeLast(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if !Equal(TakeLast(slice, 2), []int{4, 5}) {
		t.Error("TakeLast(2) failed")
	}
}

func TestDrop(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if !Equal(Drop(slice, 2), []int{3, 4, 5}) {
		t.Error("Drop(2) failed")
	}
	if !Equal(Drop(slice, 0), slice) {
		t.Error("Drop(0) should return original")
	}
	if !Equal(Drop(slice, 10), []int{}) {
		t.Error("Drop(10) should return empty")
	}
}

func TestDropWhile(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 1, 2}
	result := DropWhile(slice, func(n int) bool { return n < 4 })
	if !Equal(result, []int{4, 5, 1, 2}) {
		t.Errorf("DropWhile(<4) = %v; want [4, 5, 1, 2]", result)
	}
}

func TestDropLast(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if !Equal(DropLast(slice, 2), []int{1, 2, 3}) {
		t.Error("DropLast(2) failed")
	}
}

// =============================================================================
// Set Operations Tests
// =============================================================================

func TestUnique(t *testing.T) {
	slice := []int{1, 2, 2, 3, 3, 3, 4}
	result := Unique(slice)
	expected := []int{1, 2, 3, 4}
	if !Equal(result, expected) {
		t.Errorf("Unique = %v; want %v", result, expected)
	}
}

func TestUniqueBy(t *testing.T) {
	type Person struct {
		Name string
		Age  int
	}
	slice := []Person{
		{"Alice", 30},
		{"Bob", 25},
		{"Alice", 35},
	}
	result := UniqueBy(slice, func(p Person) string { return p.Name })
	if len(result) != 2 {
		t.Errorf("UniqueBy name count = %d; want 2", len(result))
	}
}

func TestUnion(t *testing.T) {
	slice1 := []int{1, 2, 3}
	slice2 := []int{3, 4, 5}
	result := Union(slice1, slice2)
	expected := []int{1, 2, 3, 4, 5}
	if !Equal(result, expected) {
		t.Errorf("Union = %v; want %v", result, expected)
	}
}

func TestIntersection(t *testing.T) {
	slice1 := []int{1, 2, 3, 4}
	slice2 := []int{3, 4, 5, 6}
	result := Intersection(slice1, slice2)
	expected := []int{3, 4}
	if !Equal(result, expected) {
		t.Errorf("Intersection = %v; want %v", result, expected)
	}
}

func TestDifference(t *testing.T) {
	slice1 := []int{1, 2, 3, 4}
	slice2 := []int{3, 4, 5, 6}
	result := Difference(slice1, slice2)
	expected := []int{1, 2}
	if !Equal(result, expected) {
		t.Errorf("Difference = %v; want %v", result, expected)
	}
}

func TestSymmetricDifference(t *testing.T) {
	slice1 := []int{1, 2, 3}
	slice2 := []int{2, 3, 4}
	result := SymmetricDifference(slice1, slice2)
	if len(result) != 2 {
		t.Errorf("SymmetricDifference length = %d; want 2", len(result))
	}
}

func TestIsSubset(t *testing.T) {
	if !IsSubset([]int{1, 2}, []int{1, 2, 3}) {
		t.Error("[1,2] should be subset of [1,2,3]")
	}
	if IsSubset([]int{1, 4}, []int{1, 2, 3}) {
		t.Error("[1,4] should not be subset of [1,2,3]")
	}
}

func TestIsSuperset(t *testing.T) {
	if !IsSuperset([]int{1, 2, 3}, []int{1, 2}) {
		t.Error("[1,2,3] should be superset of [1,2]")
	}
}

// =============================================================================
// Sorting Operations Tests
// =============================================================================

func TestSortBy(t *testing.T) {
	type Person struct {
		Name string
		Age  int
	}
	slice := []Person{
		{"Bob", 30},
		{"Alice", 25},
		{"Charlie", 35},
	}
	SortBy(slice, func(p Person) int { return p.Age })
	if slice[0].Name != "Alice" || slice[1].Name != "Bob" || slice[2].Name != "Charlie" {
		t.Errorf("SortBy age failed: %v", slice)
	}
}

func TestSortedBy(t *testing.T) {
	slice := []int{3, 1, 4, 1, 5, 9, 2, 6}
	result := SortedBy(slice, func(n int) int { return n })
	if !Equal(result, []int{1, 1, 2, 3, 4, 5, 6, 9}) {
		t.Errorf("SortedBy = %v", result)
	}
	if !Equal(slice, []int{3, 1, 4, 1, 5, 9, 2, 6}) {
		t.Error("Original slice was modified")
	}
}

func TestMin(t *testing.T) {
	slice := []int{3, 1, 4, 1, 5, 9, 2, 6}
	min, err := Min(slice)
	if err != nil || min != 1 {
		t.Errorf("Min = %d, err = %v; want 1", min, err)
	}
}

func TestMax(t *testing.T) {
	slice := []int{3, 1, 4, 1, 5, 9, 2, 6}
	max, err := Max(slice)
	if err != nil || max != 9 {
		t.Errorf("Max = %d, err = %v; want 9", max, err)
	}
}

func TestMinBy(t *testing.T) {
	type Person struct {
		Name string
		Age  int
	}
	slice := []Person{
		{"Bob", 30},
		{"Alice", 25},
		{"Charlie", 35},
	}
	min, err := MinBy(slice, func(p Person) int { return p.Age })
	if err != nil || min.Name != "Alice" {
		t.Errorf("MinBy age = %v; want Alice", min)
	}
}

func TestMaxBy(t *testing.T) {
	type Person struct {
		Name string
		Age  int
	}
	slice := []Person{
		{"Bob", 30},
		{"Alice", 25},
		{"Charlie", 35},
	}
	max, err := MaxBy(slice, func(p Person) int { return p.Age })
	if err != nil || max.Name != "Charlie" {
		t.Errorf("MaxBy age = %v; want Charlie", max)
	}
}

func TestMinEmptySlice(t *testing.T) {
	_, err := Min([]int{})
	if err == nil {
		t.Error("Expected error for empty slice")
	}
}

// =============================================================================
// Search Operations Tests
// =============================================================================

func TestFind(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	result, found := Find(slice, func(n int) bool { return n > 3 })
	if !found || result != 4 {
		t.Errorf("Find(>3) = %d, found = %v; want 4, true", result, found)
	}
}

func TestFindNotFound(t *testing.T) {
	slice := []int{1, 2, 3}
	_, found := Find(slice, func(n int) bool { return n > 10 })
	if found {
		t.Error("Find should not find element")
	}
}

func TestFindIndex(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	result := FindIndex(slice, func(n int) bool { return n > 3 })
	if result != 3 {
		t.Errorf("FindIndex(>3) = %d; want 3", result)
	}
}

func TestFindLast(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	result, found := FindLast(slice, func(n int) bool { return n%2 == 0 })
	if !found || result != 6 {
		t.Errorf("FindLast(even) = %d; want 6", result)
	}
}

func TestEvery(t *testing.T) {
	slice := []int{2, 4, 6, 8}
	if !Every(slice, func(n int) bool { return n%2 == 0 }) {
		t.Error("Every should return true for all even")
	}
	slice2 := []int{2, 3, 6, 8}
	if Every(slice2, func(n int) bool { return n%2 == 0 }) {
		t.Error("Every should return false for mixed")
	}
}

func TestSome(t *testing.T) {
	slice := []int{1, 3, 5, 6, 7}
	if !Some(slice, func(n int) bool { return n%2 == 0 }) {
		t.Error("Some should find an even number")
	}
	slice2 := []int{1, 3, 5, 7}
	if Some(slice2, func(n int) bool { return n%2 == 0 }) {
		t.Error("Some should not find even in odds")
	}
}

// =============================================================================
// Partition and Grouping Tests
// =============================================================================

func TestPartition(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	even, odd := Partition(slice, func(n int) bool { return n%2 == 0 })
	if !Equal(even, []int{2, 4, 6}) {
		t.Errorf("Even partition = %v", even)
	}
	if !Equal(odd, []int{1, 3, 5}) {
		t.Errorf("Odd partition = %v", odd)
	}
}

func TestGroupBy(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	groups := GroupBy(slice, func(n int) int { return n % 2 })
	if len(groups[0]) != 3 {
		t.Errorf("Even group length = %d; want 3", len(groups[0]))
	}
	if len(groups[1]) != 3 {
		t.Errorf("Odd group length = %d; want 3", len(groups[1]))
	}
}

func TestCountByKeys(t *testing.T) {
	slice := []int{1, 2, 2, 3, 3, 3}
	counts := CountByKeys(slice, func(n int) int { return n })
	if counts[1] != 1 || counts[2] != 2 || counts[3] != 3 {
		t.Errorf("CountByKeys = %v", counts)
	}
}

// =============================================================================
// Insert, Remove, Replace Tests
// =============================================================================

func TestInsert(t *testing.T) {
	slice := []int{1, 2, 4}
	result, err := Insert(slice, 2, 3)
	if err != nil {
		t.Fatalf("Insert failed: %v", err)
	}
	if !Equal(result, []int{1, 2, 3, 4}) {
		t.Errorf("Insert = %v; want [1, 2, 3, 4]", result)
	}
}

func TestInsertInvalid(t *testing.T) {
	_, err := Insert([]int{1, 2}, -1, 3)
	if err == nil {
		t.Error("Expected error for negative index")
	}
}

func TestRemove(t *testing.T) {
	slice := []int{1, 2, 3, 4}
	result, err := Remove(slice, 2)
	if err != nil {
		t.Fatalf("Remove failed: %v", err)
	}
	if !Equal(result, []int{1, 2, 4}) {
		t.Errorf("Remove = %v; want [1, 2, 4]", result)
	}
}

func TestRemoveFirst(t *testing.T) {
	slice := []int{1, 2, 2, 3}
	result := RemoveFirst(slice, 2)
	if !Equal(result, []int{1, 2, 3}) {
		t.Errorf("RemoveFirst = %v; want [1, 2, 3]", result)
	}
}

func TestRemoveAll(t *testing.T) {
	slice := []int{1, 2, 2, 2, 3}
	result := RemoveAll(slice, 2)
	if !Equal(result, []int{1, 3}) {
		t.Errorf("RemoveAll = %v; want [1, 3]", result)
	}
}

func TestReplace(t *testing.T) {
	slice := []int{1, 2, 3}
	result, err := Replace(slice, 1, 5)
	if err != nil {
		t.Fatalf("Replace failed: %v", err)
	}
	if !Equal(result, []int{1, 5, 3}) {
		t.Errorf("Replace = %v; want [1, 5, 3]", result)
	}
}

func TestReplaceAll(t *testing.T) {
	slice := []int{1, 2, 2, 2, 3}
	result := ReplaceAll(slice, 2, 5)
	if !Equal(result, []int{1, 5, 5, 5, 3}) {
		t.Errorf("ReplaceAll = %v; want [1, 5, 5, 5, 3]", result)
	}
}

// =============================================================================
// Shuffling and Sampling Tests
// =============================================================================

func TestShuffled(t *testing.T) {
	rand.Seed(42)
	slice := []int{1, 2, 3, 4, 5}
	result := Shuffled(slice)
	if len(result) != len(slice) {
		t.Errorf("Shuffled length = %d; want %d", len(result), len(slice))
	}
	// Check original is not modified
	if !Equal(slice, []int{1, 2, 3, 4, 5}) {
		t.Error("Original slice was modified")
	}
}

func TestSample(t *testing.T) {
	rand.Seed(42)
	slice := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	result, err := Sample(slice, 3)
	if err != nil {
		t.Fatalf("Sample failed: %v", err)
	}
	if len(result) != 3 {
		t.Errorf("Sample length = %d; want 3", len(result))
	}
	// Check all elements are from original
	for _, item := range result {
		if !Contains(slice, item) {
			t.Errorf("Sample contains %d not in original", item)
		}
	}
}

func TestSampleInvalidSize(t *testing.T) {
	_, err := Sample([]int{1, 2}, 5)
	if err == nil {
		t.Error("Expected error for sample size > slice length")
	}
}

func TestRandomElement(t *testing.T) {
	slice := []int{1, 2, 3}
	rand.Seed(42)
	elem, err := RandomElement(slice)
	if err != nil {
		t.Fatalf("RandomElement failed: %v", err)
	}
	if !Contains(slice, elem) {
		t.Errorf("RandomElement = %d; not in slice", elem)
	}
}

func TestRandomElementEmpty(t *testing.T) {
	_, err := RandomElement([]int{})
	if err == nil {
		t.Error("Expected error for empty slice")
	}
}

// =============================================================================
// Utility Functions Tests
// =============================================================================

func TestClone(t *testing.T) {
	slice := []int{1, 2, 3}
	cloned := Clone(slice)
	if !Equal(slice, cloned) {
		t.Errorf("Clone = %v; want %v", cloned, slice)
	}
	cloned[0] = 100
	if slice[0] == 100 {
		t.Error("Clone should be independent")
	}
}

func TestConcat(t *testing.T) {
	result := Concat([]int{1, 2}, []int{3, 4}, []int{5})
	expected := []int{1, 2, 3, 4, 5}
	if !Equal(result, expected) {
		t.Errorf("Concat = %v; want %v", result, expected)
	}
}

func TestRepeat(t *testing.T) {
	result, err := Repeat(5, 3)
	if err != nil {
		t.Fatalf("Repeat failed: %v", err)
	}
	expected := []int{5, 5, 5}
	if !Equal(result, expected) {
		t.Errorf("Repeat = %v; want %v", result, expected)
	}
}

func TestRange(t *testing.T) {
	result := Range(1, 5)
	expected := []int{1, 2, 3, 4}
	if !Equal(result, expected) {
		t.Errorf("Range(1,5) = %v; want %v", result, expected)
	}
}

func TestRangeWithStep(t *testing.T) {
	result, err := RangeWithStep(0, 10, 2)
	if err != nil {
		t.Fatalf("RangeWithStep failed: %v", err)
	}
	expected := []int{0, 2, 4, 6, 8}
	if !Equal(result, expected) {
		t.Errorf("RangeWithStep = %v; want %v", result, expected)
	}
}

func TestRangeWithNegativeStep(t *testing.T) {
	result, err := RangeWithStep(5, 0, -1)
	if err != nil {
		t.Fatalf("RangeWithStep failed: %v", err)
	}
	expected := []int{5, 4, 3, 2, 1}
	if !Equal(result, expected) {
		t.Errorf("RangeWithStep negative = %v; want %v", result, expected)
	}
}

func TestFill(t *testing.T) {
	slice := make([]int, 5)
	Fill(slice, 7)
	for i, v := range slice {
		if v != 7 {
			t.Errorf("Fill[%d] = %d; want 7", i, v)
		}
	}
}

func TestIsEmpty(t *testing.T) {
	if !IsEmpty([]int{}) {
		t.Error("IsEmpty([]) should be true")
	}
	if IsEmpty([]int{1}) {
		t.Error("IsEmpty([1]) should be false")
	}
}

func TestFirst(t *testing.T) {
	slice := []int{1, 2, 3}
	first, err := First(slice)
	if err != nil || first != 1 {
		t.Errorf("First = %d, err = %v; want 1", first, err)
	}
}

func TestLast(t *testing.T) {
	slice := []int{1, 2, 3}
	last, err := Last(slice)
	if err != nil || last != 3 {
		t.Errorf("Last = %d, err = %v; want 3", last, err)
	}
}

func TestNth(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	nth, err := Nth(slice, 2)
	if err != nil || nth != 3 {
		t.Errorf("Nth(2) = %d; want 3", nth)
	}
	// Test negative index
	nth, err = Nth(slice, -1)
	if err != nil || nth != 5 {
		t.Errorf("Nth(-1) = %d; want 5", nth)
	}
}

func TestTail(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	tail := Tail(slice)
	if !Equal(tail, []int{2, 3, 4, 5}) {
		t.Errorf("Tail = %v; want [2, 3, 4, 5]", tail)
	}
}

func TestInit(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	init := Init(slice)
	if !Equal(init, []int{1, 2, 3, 4}) {
		t.Errorf("Init = %v; want [1, 2, 3, 4]", init)
	}
}

func TestEqual(t *testing.T) {
	if !Equal([]int{1, 2, 3}, []int{1, 2, 3}) {
		t.Error("Equal should return true for equal slices")
	}
	if Equal([]int{1, 2, 3}, []int{1, 2, 4}) {
		t.Error("Equal should return false for different slices")
	}
	if Equal([]int{1, 2}, []int{1, 2, 3}) {
		t.Error("Equal should return false for different lengths")
	}
}

// =============================================================================
// Sum, Product, Average Tests
// =============================================================================

func TestSum(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	if result := Sum(slice); result != 15 {
		t.Errorf("Sum = %d; want 15", result)
	}
}

func TestProduct(t *testing.T) {
	slice := []int{1, 2, 3, 4}
	if result := Product(slice); result != 24 {
		t.Errorf("Product = %d; want 24", result)
	}
}

func TestAverage(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	avg, err := Average(slice)
	if err != nil || avg != 3.0 {
		t.Errorf("Average = %f, err = %v; want 3.0", avg, err)
	}
}

func TestMedian(t *testing.T) {
	// Odd length
	slice1 := []int{5, 1, 3, 2, 4}
	med1, err := Median(slice1)
	if err != nil || med1 != 3 {
		t.Errorf("Median(odd) = %d; want 3", med1)
	}
	// Even length
	slice2 := []int{4, 1, 3, 2}
	med2, err := Median(slice2)
	if err != nil || med2 != 2 {
		t.Errorf("Median(even) = %d; want 2", med2)
	}
}

func TestMode(t *testing.T) {
	slice := []int{1, 2, 2, 3, 3, 3, 4}
	mode, err := Mode(slice)
	if err != nil || mode != 3 {
		t.Errorf("Mode = %d; want 3", mode)
	}
}

// =============================================================================
// Zip and Unzip Tests
// =============================================================================

func TestZip(t *testing.T) {
	slice1 := []int{1, 2, 3}
	slice2 := []string{"a", "b", "c"}
	result, err := Zip(slice1, slice2)
	if err != nil {
		t.Fatalf("Zip failed: %v", err)
	}
	if len(result) != 3 {
		t.Errorf("Zip length = %d; want 3", len(result))
	}
	if result[0].First != 1 || result[0].Second != "a" {
		t.Errorf("Zip[0] = {%d, %s}; want {1, a}", result[0].First, result[0].Second)
	}
}

func TestZipDifferentLengths(t *testing.T) {
	slice1 := []int{1, 2, 3}
	slice2 := []string{"a", "b"}
	_, err := Zip(slice1, slice2)
	if err == nil {
		t.Error("Expected error for different lengths")
	}
}

func TestUnzip(t *testing.T) {
	pairs := []Pair[int, string]{
		{1, "a"},
		{2, "b"},
		{3, "c"},
	}
	slice1, slice2 := Unzip(pairs)
	if !Equal(slice1, []int{1, 2, 3}) {
		t.Errorf("Unzip first = %v", slice1)
	}
	if !Equal(slice2, []string{"a", "b", "c"}) {
		t.Errorf("Unzip second = %v", slice2)
	}
}

func TestZipWith(t *testing.T) {
	slice1 := []int{1, 2, 3}
	slice2 := []int{4, 5, 6}
	result, err := ZipWith(slice1, slice2, func(a, b int) int { return a + b })
	if err != nil {
		t.Fatalf("ZipWith failed: %v", err)
	}
	if !Equal(result, []int{5, 7, 9}) {
		t.Errorf("ZipWith = %v; want [5, 7, 9]", result)
	}
}

// =============================================================================
// Benchmark Tests
// =============================================================================

func BenchmarkUnique(b *testing.B) {
	slice := make([]int, 10000)
	for i := range slice {
		slice[i] = i % 100
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Unique(slice)
	}
}

func BenchmarkFilter(b *testing.B) {
	slice := make([]int, 10000)
	for i := range slice {
		slice[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Filter(slice, func(n int) bool { return n%2 == 0 })
	}
}

func BenchmarkMap(b *testing.B) {
	slice := make([]int, 10000)
	for i := range slice {
		slice[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Map(slice, func(n int) int { return n * 2 })
	}
}

func BenchmarkChunk(b *testing.B) {
	slice := make([]int, 10000)
	for i := range slice {
		slice[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Chunk(slice, 100)
	}
}

func BenchmarkGroupBy(b *testing.B) {
	slice := make([]int, 10000)
	for i := range slice {
		slice[i] = i
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		GroupBy(slice, func(n int) int { return n % 100 })
	}
}

// Ensure sort is imported
var _ = sort.Sort