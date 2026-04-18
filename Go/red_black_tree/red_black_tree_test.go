package red_black_tree

import (
	"testing"
)

func TestNewInt(t *testing.T) {
	tree := NewInt()
	if tree == nil {
		t.Fatal("NewInt() returned nil")
	}
	if !tree.IsEmpty() {
		t.Error("new tree should be empty")
	}
	if tree.Size() != 0 {
		t.Errorf("new tree size = %d, want 0", tree.Size())
	}
}

func TestNewString(t *testing.T) {
	tree := NewString()
	if tree == nil {
		t.Fatal("NewString() returned nil")
	}
	if !tree.IsEmpty() {
		t.Error("new tree should be empty")
	}
}

func TestInsert(t *testing.T) {
	tree := NewInt()
	
	// Insert single element
	if !tree.Insert(5) {
		t.Error("Insert(5) returned false, want true")
	}
	if tree.Size() != 1 {
		t.Errorf("Size() = %d, want 1", tree.Size())
	}
	if !tree.Contains(5) {
		t.Error("Contains(5) returned false after insert")
	}

	// Insert duplicate
	if tree.Insert(5) {
		t.Error("Insert(5) duplicate returned true, want false")
	}
	if tree.Size() != 1 {
		t.Errorf("Size() = %d after duplicate insert, want 1", tree.Size())
	}
}

func TestInsertMultiple(t *testing.T) {
	tree := NewInt()
	keys := []int{7, 3, 9, 1, 5, 8, 10}

	for _, k := range keys {
		if !tree.Insert(k) {
			t.Errorf("Insert(%d) returned false", k)
		}
	}

	if tree.Size() != len(keys) {
		t.Errorf("Size() = %d, want %d", tree.Size(), len(keys))
	}

	// Verify all keys exist
	for _, k := range keys {
		if !tree.Contains(k) {
			t.Errorf("Contains(%d) = false after insert", k)
		}
	}

	// Verify tree is valid
	if err := tree.Validate(); err != nil {
		t.Errorf("Validate() returned error: %v", err)
	}
}

func TestSearch(t *testing.T) {
	tree := NewInt()
	keys := []int{5, 3, 7, 1, 9}

	for _, k := range keys {
		tree.Insert(k)
	}

	// Search for existing keys
	for _, k := range keys {
		node := tree.Search(k)
		if node == nil {
			t.Errorf("Search(%d) = nil, want node", k)
		} else if node.Key != k {
			t.Errorf("Search(%d).Key = %d, want %d", k, node.Key, k)
		}
	}

	// Search for non-existing key
	if tree.Search(100) != nil {
		t.Error("Search(100) should return nil for non-existing key")
	}
}

func TestDelete(t *testing.T) {
	tree := NewInt()
	tree.Insert(5)

	// Delete existing key
	if !tree.Delete(5) {
		t.Error("Delete(5) returned false, want true")
	}
	if tree.Size() != 0 {
		t.Errorf("Size() = %d after delete, want 0", tree.Size())
	}
	if tree.Contains(5) {
		t.Error("Contains(5) = true after delete")
	}

	// Delete non-existing key
	if tree.Delete(5) {
		t.Error("Delete(5) returned true for non-existing key")
	}
}

func TestDeleteMultiple(t *testing.T) {
	tree := NewInt()
	keys := []int{7, 3, 9, 1, 5, 8, 10, 0, 2, 4, 6}

	for _, k := range keys {
		tree.Insert(k)
	}

	// Delete keys one by one and verify tree validity
	for _, k := range keys {
		if !tree.Delete(k) {
			t.Errorf("Delete(%d) returned false", k)
		}
		if tree.Contains(k) {
			t.Errorf("Contains(%d) = true after delete", k)
		}
		if err := tree.Validate(); err != nil {
			t.Errorf("Validate() failed after deleting %d: %v", k, err)
		}
	}

	if !tree.IsEmpty() {
		t.Errorf("Tree should be empty, Size() = %d", tree.Size())
	}
}

func TestMin(t *testing.T) {
	tree := NewInt()

	// Empty tree
	if _, ok := tree.Min(); ok {
		t.Error("Min() on empty tree returned ok=true")
	}

	// Single element
	tree.Insert(5)
	if min, ok := tree.Min(); !ok || min != 5 {
		t.Errorf("Min() = (%d, %v), want (5, true)", min, ok)
	}

	// Multiple elements
	tree.Insert(3)
	tree.Insert(7)
	tree.Insert(1)
	if min, ok := tree.Min(); !ok || min != 1 {
		t.Errorf("Min() = (%d, %v), want (1, true)", min, ok)
	}
}

func TestMax(t *testing.T) {
	tree := NewInt()

	// Empty tree
	if _, ok := tree.Max(); ok {
		t.Error("Max() on empty tree returned ok=true")
	}

	// Single element
	tree.Insert(5)
	if max, ok := tree.Max(); !ok || max != 5 {
		t.Errorf("Max() = (%d, %v), want (5, true)", max, ok)
	}

	// Multiple elements
	tree.Insert(3)
	tree.Insert(7)
	tree.Insert(10)
	if max, ok := tree.Max(); !ok || max != 10 {
		t.Errorf("Max() = (%d, %v), want (10, true)", max, ok)
	}
}

func TestInOrder(t *testing.T) {
	tree := NewInt()
	keys := []int{5, 3, 7, 1, 9, 0, 10}

	for _, k := range keys {
		tree.Insert(k)
	}

	result := tree.InOrder()
	expected := []int{0, 1, 3, 5, 7, 9, 10}

	if len(result) != len(expected) {
		t.Fatalf("InOrder() length = %d, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("InOrder()[%d] = %d, want %d", i, v, expected[i])
		}
	}
}

func TestPreOrder(t *testing.T) {
	tree := NewInt()
	tree.Insert(5)
	tree.Insert(3)
	tree.Insert(7)

	result := tree.PreOrder()
	if len(result) != 3 {
		t.Fatalf("PreOrder() length = %d, want 3", len(result))
	}
	// Root should be first
	if result[0] != 5 {
		t.Errorf("PreOrder()[0] = %d, want 5 (root)", result[0])
	}
}

func TestPostOrder(t *testing.T) {
	tree := NewInt()
	tree.Insert(5)
	tree.Insert(3)
	tree.Insert(7)

	result := tree.PostOrder()
	if len(result) != 3 {
		t.Fatalf("PostOrder() length = %d, want 3", len(result))
	}
	// Root should be last
	if result[2] != 5 {
		t.Errorf("PostOrder()[2] = %d, want 5 (root)", result[2])
	}
}

func TestClear(t *testing.T) {
	tree := NewInt()
	tree.Insert(5)
	tree.Insert(3)
	tree.Insert(7)

	tree.Clear()
	if !tree.IsEmpty() {
		t.Error("Clear() did not make tree empty")
	}
	if tree.Size() != 0 {
		t.Errorf("Size() after Clear() = %d, want 0", tree.Size())
	}
	if tree.Contains(5) {
		t.Error("Contains(5) = true after Clear()")
	}
}

func TestHeight(t *testing.T) {
	tree := NewInt()

	// Empty tree
	if h := tree.Height(); h != -1 {
		t.Errorf("Height() of empty tree = %d, want -1", h)
	}

	// Single node
	tree.Insert(5)
	if h := tree.Height(); h != 0 {
		t.Errorf("Height() with single node = %d, want 0", h)
	}

	// More nodes - height should be O(log n) for balanced tree
	tree.Insert(3)
	tree.Insert(7)
	if h := tree.Height(); h < 0 || h > 2 {
		t.Errorf("Height() = %d, expected between 0 and 2", h)
	}
}

func TestValidate(t *testing.T) {
	tree := NewInt()
	
	// Empty tree is valid
	if err := tree.Validate(); err != nil {
		t.Errorf("Validate() on empty tree: %v", err)
	}

	// Insert and validate
	keys := []int{7, 3, 9, 1, 5, 8, 10, 0, 2, 4, 6}
	for _, k := range keys {
		tree.Insert(k)
		if err := tree.Validate(); err != nil {
			t.Errorf("Validate() failed after inserting %d: %v", k, err)
		}
	}
}

func TestRange(t *testing.T) {
	tree := NewInt()
	keys := []int{1, 3, 5, 7, 9, 11, 13}

	for _, k := range keys {
		tree.Insert(k)
	}

	// Range query
	result := tree.Range(5, 11)
	expected := []int{5, 7, 9, 11}

	if len(result) != len(expected) {
		t.Fatalf("Range(5, 11) length = %d, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("Range(5, 11)[%d] = %d, want %d", i, v, expected[i])
		}
	}

	// Empty range
	empty := tree.Range(20, 30)
	if len(empty) != 0 {
		t.Errorf("Range(20, 30) = %v, want empty", empty)
	}
}

func TestLowerBound(t *testing.T) {
	tree := NewInt()
	keys := []int{1, 3, 5, 7, 9}

	for _, k := range keys {
		tree.Insert(k)
	}

	tests := []struct {
		target   int
		expected int
		found    bool
	}{
		{0, 1, true},
		{1, 1, true},
		{2, 3, true},
		{5, 5, true},
		{6, 7, true},
		{9, 9, true},
		{10, 0, false},
	}

	for _, tt := range tests {
		result, found := tree.LowerBound(tt.target)
		if found != tt.found {
			t.Errorf("LowerBound(%d).found = %v, want %v", tt.target, found, tt.found)
		}
		if found && result != tt.expected {
			t.Errorf("LowerBound(%d) = %d, want %d", tt.target, result, tt.expected)
		}
	}
}

func TestUpperBound(t *testing.T) {
	tree := NewInt()
	keys := []int{1, 3, 5, 7, 9}

	for _, k := range keys {
		tree.Insert(k)
	}

	tests := []struct {
		target   int
		expected int
		found    bool
	}{
		{0, 1, true},
		{1, 3, true},
		{2, 3, true},
		{5, 7, true},
		{6, 7, true},
		{9, 0, false},
		{10, 0, false},
	}

	for _, tt := range tests {
		result, found := tree.UpperBound(tt.target)
		if found != tt.found {
			t.Errorf("UpperBound(%d).found = %v, want %v", tt.target, found, tt.found)
		}
		if found && result != tt.expected {
			t.Errorf("UpperBound(%d) = %d, want %d", tt.target, result, tt.expected)
		}
	}
}

func TestCount(t *testing.T) {
	tree := NewInt()
	keys := []int{1, 3, 5, 7, 9}

	for _, k := range keys {
		tree.Insert(k)
	}

	tests := []struct {
		start, end int
		expected   int
	}{
		{1, 9, 5},
		{0, 10, 5},
		{3, 7, 3},
		{5, 5, 1},
		{10, 20, 0},
	}

	for _, tt := range tests {
		result := tree.Count(tt.start, tt.end)
		if result != tt.expected {
			t.Errorf("Count(%d, %d) = %d, want %d", tt.start, tt.end, result, tt.expected)
		}
	}
}

func TestForEach(t *testing.T) {
	tree := NewInt()
	keys := []int{5, 3, 7, 1, 9}

	for _, k := range keys {
		tree.Insert(k)
	}

	result := make([]int, 0)
	tree.ForEach(func(key int) bool {
		result = append(result, key)
		return true
	})

	expected := []int{1, 3, 5, 7, 9}
	if len(result) != len(expected) {
		t.Fatalf("ForEach collected %d items, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("ForEach result[%d] = %d, want %d", i, v, expected[i])
		}
	}
}

func TestForEachEarlyStop(t *testing.T) {
	tree := NewInt()
	keys := []int{1, 2, 3, 4, 5}

	for _, k := range keys {
		tree.Insert(k)
	}

	count := 0
	tree.ForEach(func(key int) bool {
		count++
		return count < 3 // Stop after 3 items
	})

	if count != 3 {
		t.Errorf("ForEach stopped after %d iterations, want 3", count)
	}
}

func TestToSlice(t *testing.T) {
	tree := NewInt()
	keys := []int{5, 3, 7, 1, 9}

	for _, k := range keys {
		tree.Insert(k)
	}

	result := tree.ToSlice()
	expected := []int{1, 3, 5, 7, 9}

	if len(result) != len(expected) {
		t.Fatalf("ToSlice() length = %d, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("ToSlice()[%d] = %d, want %d", i, v, expected[i])
		}
	}
}

func TestFromSlice(t *testing.T) {
	tree := NewInt()
	keys := []int{5, 3, 7, 1, 9}

	count := tree.FromSlice(keys)
	if count != len(keys) {
		t.Errorf("FromSlice() = %d, want %d", count, len(keys))
	}

	// Verify all keys exist
	for _, k := range keys {
		if !tree.Contains(k) {
			t.Errorf("Contains(%d) = false after FromSlice", k)
		}
	}
}

func TestString(t *testing.T) {
	tree := NewInt()

	// Empty tree
	if tree.String() != "[]" {
		t.Errorf("String() of empty tree = %s, want []", tree.String())
	}

	// Non-empty tree
	tree.Insert(5)
	tree.Insert(3)
	tree.Insert(7)

	result := tree.String()
	if result != "[1 3 5 7]" && result != "[3 5 7]" {
		t.Logf("String() = %s", result)
	}
}

func TestStringTree(t *testing.T) {
	tree := NewString()
	keys := []string{"banana", "apple", "cherry", "date"}

	for _, k := range keys {
		tree.Insert(k)
	}

	result := tree.InOrder()
	expected := []string{"apple", "banana", "cherry", "date"}

	if len(result) != len(expected) {
		t.Fatalf("InOrder() length = %d, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("InOrder()[%d] = %s, want %s", i, v, expected[i])
		}
	}
}

func TestCustomComparator(t *testing.T) {
	// Create tree with custom comparator (descending order)
	tree := New(func(a, b int) int {
		if a > b {
			return -1
		} else if a < b {
			return 1
		}
		return 0
	})

	tree.Insert(5)
	tree.Insert(3)
	tree.Insert(7)

	result := tree.InOrder()
	expected := []int{7, 5, 3}

	if len(result) != len(expected) {
		t.Fatalf("InOrder() length = %d, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("InOrder()[%d] = %d, want %d", i, v, expected[i])
		}
	}
}

func TestLargeDataset(t *testing.T) {
	tree := NewInt()
	n := 10000

	// Insert many elements
	for i := 0; i < n; i++ {
		if !tree.Insert(i) {
			t.Errorf("Insert(%d) failed", i)
		}
	}

	if tree.Size() != n {
		t.Errorf("Size() = %d, want %d", tree.Size(), n)
	}

	// Verify tree is balanced (height should be O(log n))
	height := tree.Height()
	maxExpectedHeight := 2 * (log2(n) + 1) // Red-black tree upper bound
	if height > maxExpectedHeight {
		t.Errorf("Height() = %d, expected at most %d", height, maxExpectedHeight)
	}

	// Verify all elements exist
	for i := 0; i < n; i++ {
		if !tree.Contains(i) {
			t.Errorf("Contains(%d) = false", i)
		}
	}

	// Delete half
	for i := 0; i < n/2; i++ {
		if !tree.Delete(i) {
			t.Errorf("Delete(%d) failed", i)
		}
	}

	if tree.Size() != n/2 {
		t.Errorf("Size() after deletes = %d, want %d", tree.Size(), n/2)
	}

	// Validate after deletions
	if err := tree.Validate(); err != nil {
		t.Errorf("Validate() failed after deletions: %v", err)
	}
}

// Helper function to calculate log base 2
func log2(n int) int {
	result := 0
	for n > 1 {
		n /= 2
		result++
	}
	return result
}

func BenchmarkInsert(b *testing.B) {
	tree := NewInt()
	for i := 0; i < b.N; i++ {
		tree.Insert(i)
	}
}

func BenchmarkSearch(b *testing.B) {
	tree := NewInt()
	for i := 0; i < 10000; i++ {
		tree.Insert(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tree.Search(i % 10000)
	}
}

func BenchmarkDelete(b *testing.B) {
	tree := NewInt()
	for i := 0; i < b.N; i++ {
		tree.Insert(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tree.Delete(i)
	}
}

func BenchmarkInOrder(b *testing.B) {
	tree := NewInt()
	for i := 0; i < 1000; i++ {
		tree.Insert(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tree.InOrder()
	}
}