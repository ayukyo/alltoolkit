package avl_tree_utils

import (
	"testing"
)

func TestNewInt(t *testing.T) {
	tree := NewInt()
	if tree == nil {
		t.Fatal("Expected non-nil tree")
	}
	if !tree.IsEmpty() {
		t.Error("Expected empty tree")
	}
	if tree.Size() != 0 {
		t.Errorf("Expected size 0, got %d", tree.Size())
	}
}

func TestNewString(t *testing.T) {
	tree := NewString()
	if tree == nil {
		t.Fatal("Expected non-nil tree")
	}
	if !tree.IsEmpty() {
		t.Error("Expected empty tree")
	}
}

func TestInsert(t *testing.T) {
	tree := NewInt()

	// Insert first element
	if !tree.Insert(10) {
		t.Error("Expected true for first insert")
	}
	if tree.Size() != 1 {
		t.Errorf("Expected size 1, got %d", tree.Size())
	}

	// Insert duplicate
	if tree.Insert(10) {
		t.Error("Expected false for duplicate insert")
	}
	if tree.Size() != 1 {
		t.Errorf("Expected size still 1, got %d", tree.Size())
	}

	// Insert more elements
	tree.Insert(5)
	tree.Insert(15)
	tree.Insert(3)
	tree.Insert(7)

	if tree.Size() != 5 {
		t.Errorf("Expected size 5, got %d", tree.Size())
	}
}

func TestSearch(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)
	tree.Insert(15)

	// Search for existing keys
	if tree.Search(10) == nil {
		t.Error("Expected to find 10")
	}
	if tree.Search(5) == nil {
		t.Error("Expected to find 5")
	}
	if tree.Search(15) == nil {
		t.Error("Expected to find 15")
	}

	// Search for non-existing key
	if tree.Search(100) != nil {
		t.Error("Expected nil for non-existing key")
	}
}

func TestContains(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)

	if !tree.Contains(10) {
		t.Error("Expected to contain 10")
	}
	if !tree.Contains(5) {
		t.Error("Expected to contain 5")
	}
	if tree.Contains(100) {
		t.Error("Expected not to contain 100")
	}
}

func TestDelete(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)
	tree.Insert(15)

	// Delete existing key
	if !tree.Delete(10) {
		t.Error("Expected true for deleting existing key")
	}
	if tree.Size() != 2 {
		t.Errorf("Expected size 2, got %d", tree.Size())
	}
	if tree.Contains(10) {
		t.Error("Expected 10 to be deleted")
	}

	// Delete non-existing key
	if tree.Delete(100) {
		t.Error("Expected false for deleting non-existing key")
	}
}

func TestMinMax(t *testing.T) {
	tree := NewInt()

	// Empty tree
	_, ok := tree.Min()
	if ok {
		t.Error("Expected false for min on empty tree")
	}
	_, ok = tree.Max()
	if ok {
		t.Error("Expected false for max on empty tree")
	}

	// Insert elements
	values := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range values {
		tree.Insert(v)
	}

	min, ok := tree.Min()
	if !ok || min != 20 {
		t.Errorf("Expected min 20, got %d", min)
	}

	max, ok := tree.Max()
	if !ok || max != 80 {
		t.Errorf("Expected max 80, got %d", max)
	}
}

func TestInOrder(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range values {
		tree.Insert(v)
	}

	expected := []int{20, 30, 40, 50, 60, 70, 80}
	result := tree.InOrder()

	if len(result) != len(expected) {
		t.Fatalf("Expected length %d, got %d", len(expected), len(result))
	}

	for i, v := range expected {
		if result[i] != v {
			t.Errorf("Expected %d at index %d, got %d", v, i, result[i])
		}
	}
}

func TestPreOrder(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)
	tree.Insert(15)

	result := tree.PreOrder()
	if result[0] != 10 {
		t.Errorf("Expected root 10, got %d", result[0])
	}
}

func TestPostOrder(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)
	tree.Insert(15)

	result := tree.PostOrder()
	if len(result) != 3 {
		t.Errorf("Expected 3 elements, got %d", len(result))
	}
}

func TestLevelOrder(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)
	tree.Insert(15)
	tree.Insert(3)
	tree.Insert(7)

	result := tree.LevelOrder()
	if result[0] != 10 {
		t.Errorf("Expected root 10, got %d", result[0])
	}
}

func TestHeight(t *testing.T) {
	tree := NewInt()

	// Empty tree
	if tree.Height() != 0 {
		t.Errorf("Expected height 0 for empty tree, got %d", tree.Height())
	}

	// Single node
	tree.Insert(10)
	if tree.Height() != 1 {
		t.Errorf("Expected height 1, got %d", tree.Height())
	}

	// More nodes - AVL should keep height balanced
	tree.Insert(5)
	tree.Insert(15)
	tree.Insert(3)
	tree.Insert(7)
	tree.Insert(13)
	tree.Insert(17)

	// AVL tree with 7 nodes should have height ~3
	if tree.Height() > 4 {
		t.Errorf("Height too large for AVL tree: %d", tree.Height())
	}
}

func TestValidate(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45}
	for _, v := range values {
		tree.Insert(v)
	}

	if err := tree.Validate(); err != nil {
		t.Errorf("Tree validation failed: %v", err)
	}

	if !tree.IsBalanced() {
		t.Error("Expected tree to be balanced")
	}
}

func TestRange(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range values {
		tree.Insert(v)
	}

	result := tree.Range(30, 60)
	expected := []int{30, 40, 50, 60}

	if len(result) != len(expected) {
		t.Fatalf("Expected length %d, got %d", len(expected), len(result))
	}

	for i, v := range expected {
		if result[i] != v {
			t.Errorf("Expected %d at index %d, got %d", v, i, result[i])
		}
	}
}

func TestLowerBound(t *testing.T) {
	tree := NewInt()
	values := []int{10, 20, 30, 40, 50}
	for _, v := range values {
		tree.Insert(v)
	}

	// Exact match
	if v, ok := tree.LowerBound(30); !ok || v != 30 {
		t.Errorf("Expected 30, got %d, ok=%v", v, ok)
	}

	// No exact match, find next
	if v, ok := tree.LowerBound(25); !ok || v != 30 {
		t.Errorf("Expected 30, got %d, ok=%v", v, ok)
	}

	// Smaller than all
	if v, ok := tree.LowerBound(5); !ok || v != 10 {
		t.Errorf("Expected 10, got %d, ok=%v", v, ok)
	}

	// Larger than all
	if _, ok := tree.LowerBound(100); ok {
		t.Error("Expected false for value larger than all")
	}
}

func TestUpperBound(t *testing.T) {
	tree := NewInt()
	values := []int{10, 20, 30, 40, 50}
	for _, v := range values {
		tree.Insert(v)
	}

	// Exact match, find next greater
	if v, ok := tree.UpperBound(30); !ok || v != 40 {
		t.Errorf("Expected 40, got %d, ok=%v", v, ok)
	}

	// No exact match
	if v, ok := tree.UpperBound(25); !ok || v != 30 {
		t.Errorf("Expected 30, got %d, ok=%v", v, ok)
	}

	// Smaller than all
	if v, ok := tree.UpperBound(5); !ok || v != 10 {
		t.Errorf("Expected 10, got %d, ok=%v", v, ok)
	}

	// Larger than all
	if _, ok := tree.UpperBound(50); ok {
		t.Error("Expected false for value >= max")
	}
}

func TestPredecessor(t *testing.T) {
	tree := NewInt()
	values := []int{10, 20, 30, 40, 50}
	for _, v := range values {
		tree.Insert(v)
	}

	// Predecessor of 30 is 20
	if v, ok := tree.Predecessor(30); !ok || v != 20 {
		t.Errorf("Expected 20, got %d, ok=%v", v, ok)
	}

	// Predecessor of 25 is 20
	if v, ok := tree.Predecessor(25); !ok || v != 20 {
		t.Errorf("Expected 20, got %d, ok=%v", v, ok)
	}

	// No predecessor for smallest
	if _, ok := tree.Predecessor(5); ok {
		t.Error("Expected false for predecessor of smallest")
	}
}

func TestSuccessor(t *testing.T) {
	tree := NewInt()
	values := []int{10, 20, 30, 40, 50}
	for _, v := range values {
		tree.Insert(v)
	}

	// Successor of 30 is 40
	if v, ok := tree.Successor(30); !ok || v != 40 {
		t.Errorf("Expected 40, got %d, ok=%v", v, ok)
	}

	// Successor of 25 is 30
	if v, ok := tree.Successor(25); !ok || v != 30 {
		t.Errorf("Expected 30, got %d, ok=%v", v, ok)
	}

	// No successor for largest
	if _, ok := tree.Successor(55); ok {
		t.Error("Expected false for successor of largest")
	}
}

func TestKthSmallest(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range values {
		tree.Insert(v)
	}

	expected := []int{20, 30, 40, 50, 60, 70, 80}
	for k := 1; k <= 7; k++ {
		if v, ok := tree.KthSmallest(k); !ok || v != expected[k-1] {
			t.Errorf("Expected %d for k=%d, got %d", expected[k-1], k, v)
		}
	}

	// Invalid k
	if _, ok := tree.KthSmallest(0); ok {
		t.Error("Expected false for k=0")
	}
	if _, ok := tree.KthSmallest(8); ok {
		t.Error("Expected false for k=8")
	}
}

func TestKthLargest(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range values {
		tree.Insert(v)
	}

	expected := []int{80, 70, 60, 50, 40, 30, 20}
	for k := 1; k <= 7; k++ {
		if v, ok := tree.KthLargest(k); !ok || v != expected[k-1] {
			t.Errorf("Expected %d for k=%d, got %d", expected[k-1], k, v)
		}
	}
}

func TestRank(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range values {
		tree.Insert(v)
	}

	// Rank tests
	tests := map[int]int{
		20: 1,
		30: 2,
		40: 3,
		50: 4,
		60: 5,
		70: 6,
		80: 7,
	}

	for key, expectedRank := range tests {
		if r := tree.Rank(key); r != expectedRank {
			t.Errorf("Expected rank %d for key %d, got %d", expectedRank, key, r)
		}
	}

	// Non-existing key
	if tree.Rank(100) != 0 {
		t.Error("Expected rank 0 for non-existing key")
	}
}

func TestClear(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(20)
	tree.Insert(30)

	tree.Clear()

	if !tree.IsEmpty() {
		t.Error("Expected empty tree after clear")
	}
	if tree.Size() != 0 {
		t.Errorf("Expected size 0, got %d", tree.Size())
	}
	if tree.Height() != 0 {
		t.Errorf("Expected height 0, got %d", tree.Height())
	}
}

func TestForEach(t *testing.T) {
	tree := NewInt()
	values := []int{50, 30, 70, 20, 40}
	for _, v := range values {
		tree.Insert(v)
	}

	visited := make([]int, 0)
	tree.ForEach(func(key int) bool {
		visited = append(visited, key)
		return true
	})

	expected := []int{20, 30, 40, 50, 70}
	if len(visited) != len(expected) {
		t.Fatalf("Expected %d visited, got %d", len(expected), len(visited))
	}

	for i, v := range expected {
		if visited[i] != v {
			t.Errorf("Expected %d at index %d, got %d", v, i, visited[i])
		}
	}
}

func TestForEachEarlyExit(t *testing.T) {
	tree := NewInt()
	values := []int{10, 20, 30, 40, 50}
	for _, v := range values {
		tree.Insert(v)
	}

	count := 0
	tree.ForEach(func(key int) bool {
		count++
		return count < 3 // Stop after 3
	})

	if count != 3 {
		t.Errorf("Expected 3 iterations, got %d", count)
	}
}

func TestToSlice(t *testing.T) {
	tree := NewInt()
	values := []int{30, 10, 20, 50, 40}
	for _, v := range values {
		tree.Insert(v)
	}

	result := tree.ToSlice()
	expected := []int{10, 20, 30, 40, 50}

	if len(result) != len(expected) {
		t.Fatalf("Expected length %d, got %d", len(expected), len(result))
	}

	for i, v := range expected {
		if result[i] != v {
			t.Errorf("Expected %d at index %d, got %d", v, i, result[i])
		}
	}
}

func TestFromSlice(t *testing.T) {
	tree := NewInt()
	values := []int{30, 10, 20, 50, 40}

	count := tree.FromSlice(values)
	if count != 5 {
		t.Errorf("Expected 5 inserts, got %d", count)
	}

	if tree.Size() != 5 {
		t.Errorf("Expected size 5, got %d", tree.Size())
	}
}

func TestStringTree(t *testing.T) {
	tree := NewString()
	words := []string{"banana", "apple", "cherry", "date", "elderberry"}

	for _, w := range words {
		if !tree.Insert(w) {
			t.Errorf("Failed to insert %s", w)
		}
	}

	if tree.Size() != 5 {
		t.Errorf("Expected size 5, got %d", tree.Size())
	}

	// Check order
	expected := []string{"apple", "banana", "cherry", "date", "elderberry"}
	result := tree.InOrder()

	for i, v := range expected {
		if result[i] != v {
			t.Errorf("Expected %s at index %d, got %s", v, i, result[i])
		}
	}
}

func TestString(t *testing.T) {
	tree := NewInt()
	tree.Insert(10)
	tree.Insert(5)
	tree.Insert(15)

	s := tree.String()
	if s == "[]" {
		t.Error("Expected non-empty string representation")
	}
}

func TestBalanceAfterDeletion(t *testing.T) {
	tree := NewInt()

	// Insert sequential values (worst case for unbalanced BST)
	for i := 1; i <= 100; i++ {
		tree.Insert(i)
	}

	// Verify balance
	if err := tree.Validate(); err != nil {
		t.Errorf("Tree not valid after inserts: %v", err)
	}

	// Delete many elements
	for i := 1; i <= 50; i++ {
		tree.Delete(i)
	}

	// Verify balance after deletions
	if err := tree.Validate(); err != nil {
		t.Errorf("Tree not valid after deletions: %v", err)
	}

	if !tree.IsBalanced() {
		t.Error("Tree should be balanced after deletions")
	}
}

func TestLargeDataset(t *testing.T) {
	tree := NewInt()

	// Insert 10000 random-ish elements
	for i := 0; i < 10000; i++ {
		key := (i * 7) % 20000
		tree.Insert(key)
	}

	if err := tree.Validate(); err != nil {
		t.Errorf("Tree validation failed: %v", err)
	}

	// Height should be O(log n), around 14-15 for 10000 nodes
	if tree.Height() > 20 {
		t.Errorf("Height too large for AVL tree: %d", tree.Height())
	}
}

func TestCount(t *testing.T) {
	tree := NewInt()
	values := []int{10, 20, 30, 40, 50, 60, 70}
	for _, v := range values {
		tree.Insert(v)
	}

	count := tree.Count(25, 55)
	if count != 3 { // 30, 40, 50
		t.Errorf("Expected count 3, got %d", count)
	}
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