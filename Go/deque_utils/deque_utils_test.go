package deque_utils

import (
	"errors"
	"testing"
)

// ============================================================================
// Constructor Tests
// ============================================================================

func TestNewDeque(t *testing.T) {
	d := NewDeque[int]()
	if d == nil {
		t.Fatal("NewDeque returned nil")
	}
	if !d.IsEmpty() {
		t.Error("New deque should be empty")
	}
	if d.Len() != 0 {
		t.Errorf("New deque should have length 0, got %d", d.Len())
	}
}

func TestNewDequeWithCapacity(t *testing.T) {
	d := NewDequeWithCapacity[int](10)
	if d == nil {
		t.Fatal("NewDequeWithCapacity returned nil")
	}
	if d.Cap() < 10 {
		t.Errorf("Expected capacity >= 10, got %d", d.Cap())
	}
	if !d.IsEmpty() {
		t.Error("New deque should be empty")
	}
}

func TestNewDequeFromSlice(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}
	d := NewDequeFromSlice(slice)
	if d.Len() != 5 {
		t.Errorf("Expected length 5, got %d", d.Len())
	}
	
	// Verify elements
	front, err := d.Front()
	if err != nil || front != 1 {
		t.Errorf("Expected front 1, got %d, err: %v", front, err)
	}
	
	back, err := d.Back()
	if err != nil || back != 5 {
		t.Errorf("Expected back 5, got %d, err: %v", back, err)
	}
}

// ============================================================================
// Basic Operations Tests
// ============================================================================

func TestPushFront(t *testing.T) {
	d := NewDeque[int]()
	d.PushFront(1)
	d.PushFront(2)
	d.PushFront(3)
	
	if d.Len() != 3 {
		t.Errorf("Expected length 3, got %d", d.Len())
	}
	
	front, _ := d.Front()
	if front != 3 {
		t.Errorf("Expected front 3, got %d", front)
	}
	
	back, _ := d.Back()
	if back != 1 {
		t.Errorf("Expected back 1, got %d", back)
	}
}

func TestPushBack(t *testing.T) {
	d := NewDeque[int]()
	d.PushBack(1)
	d.PushBack(2)
	d.PushBack(3)
	
	if d.Len() != 3 {
		t.Errorf("Expected length 3, got %d", d.Len())
	}
	
	front, _ := d.Front()
	if front != 1 {
		t.Errorf("Expected front 1, got %d", front)
	}
	
	back, _ := d.Back()
	if back != 3 {
		t.Errorf("Expected back 3, got %d", back)
	}
}

func TestPopFront(t *testing.T) {
	d := NewDeque[int]()
	d.PushBack(1)
	d.PushBack(2)
	d.PushBack(3)
	
	val, err := d.PopFront()
	if err != nil || val != 1 {
		t.Errorf("Expected 1, got %d, err: %v", val, err)
	}
	
	val, err = d.PopFront()
	if err != nil || val != 2 {
		t.Errorf("Expected 2, got %d, err: %v", val, err)
	}
	
	val, err = d.PopFront()
	if err != nil || val != 3 {
		t.Errorf("Expected 3, got %d, err: %v", val, err)
	}
	
	_, err = d.PopFront()
	if err == nil {
		t.Error("Expected error on empty deque")
	}
}

func TestPopBack(t *testing.T) {
	d := NewDeque[int]()
	d.PushBack(1)
	d.PushBack(2)
	d.PushBack(3)
	
	val, err := d.PopBack()
	if err != nil || val != 3 {
		t.Errorf("Expected 3, got %d, err: %v", val, err)
	}
	
	val, err = d.PopBack()
	if err != nil || val != 2 {
		t.Errorf("Expected 2, got %d, err: %v", val, err)
	}
	
	val, err = d.PopBack()
	if err != nil || val != 1 {
		t.Errorf("Expected 1, got %d, err: %v", val, err)
	}
	
	_, err = d.PopBack()
	if err == nil {
		t.Error("Expected error on empty deque")
	}
}

func TestFront(t *testing.T) {
	d := NewDeque[int]()
	
	_, err := d.Front()
	if err == nil {
		t.Error("Expected error on empty deque")
	}
	
	d.PushBack(10)
	front, err := d.Front()
	if err != nil || front != 10 {
		t.Errorf("Expected 10, got %d, err: %v", front, err)
	}
	
	d.PushBack(20)
	front, err = d.Front()
	if err != nil || front != 10 {
		t.Errorf("Front should still be 10, got %d", front)
	}
}

func TestBack(t *testing.T) {
	d := NewDeque[int]()
	
	_, err := d.Back()
	if err == nil {
		t.Error("Expected error on empty deque")
	}
	
	d.PushBack(10)
	back, err := d.Back()
	if err != nil || back != 10 {
		t.Errorf("Expected 10, got %d, err: %v", back, err)
	}
	
	d.PushBack(20)
	back, err = d.Back()
	if err != nil || back != 20 {
		t.Errorf("Back should be 20, got %d", back)
	}
}

// ============================================================================
// Collection Properties Tests
// ============================================================================

func TestLen(t *testing.T) {
	d := NewDeque[int]()
	if d.Len() != 0 {
		t.Errorf("Expected length 0, got %d", d.Len())
	}
	
	for i := 0; i < 100; i++ {
		d.PushBack(i)
		if d.Len() != i+1 {
			t.Errorf("Expected length %d, got %d", i+1, d.Len())
		}
	}
}

func TestIsEmpty(t *testing.T) {
	d := NewDeque[int]()
	if !d.IsEmpty() {
		t.Error("New deque should be empty")
	}
	
	d.PushBack(1)
	if d.IsEmpty() {
		t.Error("Deque with element should not be empty")
	}
	
	d.PopFront()
	if !d.IsEmpty() {
		t.Error("Deque after pop should be empty")
	}
}

func TestClear(t *testing.T) {
	d := NewDeque[int]()
	for i := 0; i < 10; i++ {
		d.PushBack(i)
	}
	
	d.Clear()
	if !d.IsEmpty() {
		t.Error("Deque should be empty after clear")
	}
	if d.Len() != 0 {
		t.Errorf("Length should be 0 after clear, got %d", d.Len())
	}
}

// ============================================================================
// Random Access Tests
// ============================================================================

func TestGet(t *testing.T) {
	d := NewDequeFromSlice([]int{10, 20, 30, 40, 50})
	
	tests := []struct {
		index    int
		expected int
		hasError bool
	}{
		{0, 10, false},
		{1, 20, false},
		{4, 50, false},
		{-1, 0, true},
		{5, 0, true},
		{100, 0, true},
	}
	
	for _, tt := range tests {
		val, err := d.Get(tt.index)
		if tt.hasError {
			if err == nil {
				t.Errorf("Index %d should cause error", tt.index)
			}
		} else {
			if err != nil || val != tt.expected {
				t.Errorf("Index %d: expected %d, got %d, err: %v", tt.index, tt.expected, val, err)
			}
		}
	}
}

func TestSet(t *testing.T) {
	d := NewDequeFromSlice([]int{10, 20, 30, 40, 50})
	
	err := d.Set(2, 300)
	if err != nil || d.data[2] != 300 {
		t.Errorf("Set failed: err=%v, val=%d", err, d.data[2])
	}
	
	err = d.Set(-1, 100)
	if err == nil {
		t.Error("Set should fail with negative index")
	}
	
	err = d.Set(100, 100)
	if err == nil {
		t.Error("Set should fail with out-of-range index")
	}
}

// ============================================================================
// Bulk Operations Tests
// ============================================================================

func TestPushFrontAll(t *testing.T) {
	d := NewDeque[int]()
	d.PushBack(4)
	d.PushBack(5)
	
	d.PushFrontAll([]int{1, 2, 3})
	
	if d.Len() != 5 {
		t.Errorf("Expected length 5, got %d", d.Len())
	}
	
	// Verify order
	expected := []int{1, 2, 3, 4, 5}
	for i, exp := range expected {
		val, _ := d.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestPushBackAll(t *testing.T) {
	d := NewDeque[int]()
	d.PushBack(1)
	d.PushBack(2)
	
	d.PushBackAll([]int{3, 4, 5})
	
	if d.Len() != 5 {
		t.Errorf("Expected length 5, got %d", d.Len())
	}
	
	expected := []int{1, 2, 3, 4, 5}
	for i, exp := range expected {
		val, _ := d.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestPopFrontN(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	
	items, err := d.PopFrontN(3)
	if err != nil || len(items) != 3 {
		t.Errorf("Expected 3 items, got %d, err: %v", len(items), err)
	}
	
	expected := []int{1, 2, 3}
	for i, exp := range expected {
		if items[i] != exp {
			t.Errorf("Item %d: expected %d, got %d", i, exp, items[i])
		}
	}
	
	if d.Len() != 2 {
		t.Errorf("Expected remaining length 2, got %d", d.Len())
	}
	
	// Test pop more than available
	_, err = d.PopFrontN(10)
	if err == nil {
		t.Error("Should fail when popping more than available")
	}
}

func TestPopBackN(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	
	items, err := d.PopBackN(2)
	if err != nil || len(items) != 2 {
		t.Errorf("Expected 2 items, got %d, err: %v", len(items), err)
	}
	
	expected := []int{4, 5}
	for i, exp := range expected {
		if items[i] != exp {
			t.Errorf("Item %d: expected %d, got %d", i, exp, items[i])
		}
	}
	
	if d.Len() != 3 {
		t.Errorf("Expected remaining length 3, got %d", d.Len())
	}
}

// ============================================================================
// Search Operations Tests
// ============================================================================

func TestContains(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	equals := func(a, b int) bool { return a == b }
	
	if !d.Contains(3, equals) {
		t.Error("Should contain 3")
	}
	if d.Contains(10, equals) {
		t.Error("Should not contain 10")
	}
}

func TestIndexOf(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 2, 1})
	equals := func(a, b int) bool { return a == b }
	
	if idx := d.IndexOf(1, equals); idx != 0 {
		t.Errorf("Expected index 0, got %d", idx)
	}
	if idx := d.IndexOf(3, equals); idx != 2 {
		t.Errorf("Expected index 2, got %d", idx)
	}
	if idx := d.IndexOf(10, equals); idx != -1 {
		t.Errorf("Expected -1 for not found, got %d", idx)
	}
}

func TestLastIndexOf(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 2, 1})
	equals := func(a, b int) bool { return a == b }
	
	if idx := d.LastIndexOf(1, equals); idx != 4 {
		t.Errorf("Expected index 4, got %d", idx)
	}
	if idx := d.LastIndexOf(2, equals); idx != 3 {
		t.Errorf("Expected index 3, got %d", idx)
	}
	if idx := d.LastIndexOf(10, equals); idx != -1 {
		t.Errorf("Expected -1 for not found, got %d", idx)
	}
}

func TestFind(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	predicate := func(x int) bool { return x > 3 }
	
	val, err := d.Find(predicate)
	if err != nil || val != 4 {
		t.Errorf("Expected 4, got %d, err: %v", val, err)
	}
	
	predicate2 := func(x int) bool { return x > 10 }
	_, err = d.Find(predicate2)
	if err == nil {
		t.Error("Should not find element > 10")
	}
}

func TestFindAll(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5, 6})
	predicate := func(x int) bool { return x%2 == 0 }
	
	result := d.FindAll(predicate)
	if len(result) != 3 {
		t.Errorf("Expected 3 items, got %d", len(result))
	}
}

func TestCount(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5, 6})
	predicate := func(x int) bool { return x%2 == 0 }
	
	count := d.Count(predicate)
	if count != 3 {
		t.Errorf("Expected count 3, got %d", count)
	}
}

// ============================================================================
// Modification Operations Tests
// ============================================================================

func TestInsertAt(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 4, 5})
	
	err := d.InsertAt(2, 3)
	if err != nil || d.Len() != 5 {
		t.Errorf("Insert failed: err=%v, len=%d", err, d.Len())
	}
	
	val, _ := d.Get(2)
	if val != 3 {
		t.Errorf("Expected 3 at index 2, got %d", val)
	}
	
	// Test insert at front
	err = d.InsertAt(0, 0)
	if err != nil || d.data[0] != 0 {
		t.Errorf("Insert at front failed")
	}
	
	// Test insert at end
	err = d.InsertAt(d.Len(), 6)
	if err != nil {
		t.Errorf("Insert at end failed: %v", err)
	}
}

func TestRemoveAt(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	
	val, err := d.RemoveAt(2)
	if err != nil || val != 3 {
		t.Errorf("Expected to remove 3, got %d, err: %v", val, err)
	}
	
	if d.Len() != 4 {
		t.Errorf("Expected length 4, got %d", d.Len())
	}
	
	_, err = d.RemoveAt(-1)
	if err == nil {
		t.Error("Should fail with negative index")
	}
	
	_, err = d.RemoveAt(100)
	if err == nil {
		t.Error("Should fail with out-of-range index")
	}
}

func TestRemove(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	predicate := func(x int) bool { return x == 3 }
	
	removed := d.Remove(predicate)
	if !removed {
		t.Error("Should have removed element")
	}
	if d.Len() != 4 {
		t.Errorf("Expected length 4, got %d", d.Len())
	}
	
	// Try removing again
	removed = d.Remove(predicate)
	if removed {
		t.Error("Should not have found element to remove")
	}
}

func TestRemoveAll(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 2, 4, 2, 5})
	predicate := func(x int) bool { return x == 2 }
	
	count := d.RemoveAll(predicate)
	if count != 3 {
		t.Errorf("Expected 3 removals, got %d", count)
	}
	if d.Len() != 4 {
		t.Errorf("Expected length 4, got %d", d.Len())
	}
}

// ============================================================================
// Transformation Operations Tests
// ============================================================================

func TestMap(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3})
	result := Map(d, func(x int) int { return x * 2 })
	
	if result.Len() != 3 {
		t.Errorf("Expected length 3, got %d", result.Len())
	}
	
	expected := []int{2, 4, 6}
	for i, exp := range expected {
		val, _ := result.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestFilter(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5, 6})
	result := d.Filter(func(x int) bool { return x%2 == 0 })
	
	if result.Len() != 3 {
		t.Errorf("Expected length 3, got %d", result.Len())
	}
	
	expected := []int{2, 4, 6}
	for i, exp := range expected {
		val, _ := result.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestReduce(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	sum := Reduce(d, 0, func(acc, x int) int { return acc + x })
	
	if sum != 15 {
		t.Errorf("Expected sum 15, got %d", sum)
	}
	
	product := Reduce(d, 1, func(acc, x int) int { return acc * x })
	if product != 120 {
		t.Errorf("Expected product 120, got %d", product)
	}
}

func TestForEach(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3})
	sum := 0
	d.ForEach(func(x int) {
		sum += x
	})
	if sum != 6 {
		t.Errorf("Expected sum 6, got %d", sum)
	}
}

func TestReverse(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	d.Reverse()
	
	expected := []int{5, 4, 3, 2, 1}
	for i, exp := range expected {
		val, _ := d.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestReversed(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	result := d.Reversed()
	
	// Original should be unchanged
	if d.data[0] != 1 {
		t.Error("Original deque should not be modified")
	}
	
	expected := []int{5, 4, 3, 2, 1}
	for i, exp := range expected {
		val, _ := result.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestRotateLeft(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	d.RotateLeft(2)
	
	expected := []int{3, 4, 5, 1, 2}
	for i, exp := range expected {
		val, _ := d.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
	
	// Test with n > length
	d = NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	d.RotateLeft(7) // Same as rotate 2
	for i, exp := range expected {
		val, _ := d.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestRotateRight(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	d.RotateRight(2)
	
	expected := []int{4, 5, 1, 2, 3}
	for i, exp := range expected {
		val, _ := d.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

// ============================================================================
// Slice Operations Tests
// ============================================================================

func TestToSlice(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	slice := d.ToSlice()
	
	if len(slice) != 5 {
		t.Errorf("Expected length 5, got %d", len(slice))
	}
	
	// Modify slice should not affect deque
	slice[0] = 100
	val, _ := d.Get(0)
	if val != 1 {
		t.Error("ToSlice should return a copy")
	}
}

func TestSubDeque(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	sub, err := d.SubDeque(1, 4)
	
	if err != nil || sub.Len() != 3 {
		t.Errorf("Expected length 3, got %d, err: %v", sub.Len(), err)
	}
	
	expected := []int{2, 3, 4}
	for i, exp := range expected {
		val, _ := sub.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
	
	// Test invalid range
	_, err = d.SubDeque(-1, 3)
	if err == nil {
		t.Error("Should fail with negative start")
	}
}

func TestTake(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	result := d.Take(3)
	
	if result.Len() != 3 {
		t.Errorf("Expected length 3, got %d", result.Len())
	}
	
	expected := []int{1, 2, 3}
	for i, exp := range expected {
		val, _ := result.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestTakeLast(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	result := d.TakeLast(3)
	
	if result.Len() != 3 {
		t.Errorf("Expected length 3, got %d", result.Len())
	}
	
	expected := []int{3, 4, 5}
	for i, exp := range expected {
		val, _ := result.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestSkip(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	result := d.Skip(2)
	
	if result.Len() != 3 {
		t.Errorf("Expected length 3, got %d", result.Len())
	}
	
	expected := []int{3, 4, 5}
	for i, exp := range expected {
		val, _ := result.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

// ============================================================================
// Comparison Operations Tests
// ============================================================================

func TestEqual(t *testing.T) {
	equals := func(a, b int) bool { return a == b }
	
	d1 := NewDequeFromSlice([]int{1, 2, 3})
	d2 := NewDequeFromSlice([]int{1, 2, 3})
	d3 := NewDequeFromSlice([]int{1, 2, 4})
	d4 := NewDequeFromSlice([]int{1, 2})
	
	if !d1.Equal(d2, equals) {
		t.Error("Equal deques should be equal")
	}
	if d1.Equal(d3, equals) {
		t.Error("Different deques should not be equal")
	}
	if d1.Equal(d4, equals) {
		t.Error("Different length deques should not be equal")
	}
}

// ============================================================================
// Utility Functions Tests
// ============================================================================

func TestClone(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3})
	clone := d.Clone()
	
	if !d.Equal(clone, func(a, b int) bool { return a == b }) {
		t.Error("Clone should be equal to original")
	}
	
	// Modify clone should not affect original
	clone.PushBack(4)
	if d.Len() == 4 {
		t.Error("Modifying clone should not affect original")
	}
}

func TestAppend(t *testing.T) {
	d1 := NewDequeFromSlice([]int{1, 2, 3})
	d2 := NewDequeFromSlice([]int{4, 5, 6})
	d1.Append(d2)
	
	if d1.Len() != 6 {
		t.Errorf("Expected length 6, got %d", d1.Len())
	}
	
	expected := []int{1, 2, 3, 4, 5, 6}
	for i, exp := range expected {
		val, _ := d1.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestPrepend(t *testing.T) {
	d1 := NewDequeFromSlice([]int{4, 5, 6})
	d2 := NewDequeFromSlice([]int{1, 2, 3})
	d1.Prepend(d2)
	
	if d1.Len() != 6 {
		t.Errorf("Expected length 6, got %d", d1.Len())
	}
	
	expected := []int{1, 2, 3, 4, 5, 6}
	for i, exp := range expected {
		val, _ := d1.Get(i)
		if val != exp {
			t.Errorf("Index %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestSwap(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	
	err := d.Swap(0, 4)
	if err != nil {
		t.Errorf("Swap failed: %v", err)
	}
	
	if d.data[0] != 5 || d.data[4] != 1 {
		t.Error("Swap did not work correctly")
	}
	
	err = d.Swap(-1, 0)
	if err == nil {
		t.Error("Should fail with negative index")
	}
}

// ============================================================================
// Special Operations Tests
// ============================================================================

func TestPushFrontIfEmpty(t *testing.T) {
	d := NewDeque[int]()
	
	if !d.PushFrontIfEmpty(1) {
		t.Error("Should push to empty deque")
	}
	if d.PushFrontIfEmpty(2) {
		t.Error("Should not push to non-empty deque")
	}
}

func TestPushBackIfEmpty(t *testing.T) {
	d := NewDeque[int]()
	
	if !d.PushBackIfEmpty(1) {
		t.Error("Should push to empty deque")
	}
	if d.PushBackIfEmpty(2) {
		t.Error("Should not push to non-empty deque")
	}
}

func TestPopFrontOrDefault(t *testing.T) {
	d := NewDeque[int]()
	
	val := d.PopFrontOrDefault(100)
	if val != 100 {
		t.Errorf("Expected default 100, got %d", val)
	}
	
	d.PushBack(1)
	val = d.PopFrontOrDefault(100)
	if val != 1 {
		t.Errorf("Expected 1, got %d", val)
	}
}

func TestPopBackOrDefault(t *testing.T) {
	d := NewDeque[int]()
	
	val := d.PopBackOrDefault(100)
	if val != 100 {
		t.Errorf("Expected default 100, got %d", val)
	}
	
	d.PushBack(1)
	val = d.PopBackOrDefault(100)
	if val != 1 {
		t.Errorf("Expected 1, got %d", val)
	}
}

func TestMin(t *testing.T) {
	d := NewDequeFromSlice([]int{5, 3, 8, 1, 9, 2})
	less := func(a, b int) bool { return a < b }
	
	min, err := d.Min(less)
	if err != nil || min != 1 {
		t.Errorf("Expected min 1, got %d, err: %v", min, err)
	}
	
	emptyDeque := NewDeque[int]()
	_, err = emptyDeque.Min(less)
	if err == nil {
		t.Error("Should fail on empty deque")
	}
}

func TestMax(t *testing.T) {
	d := NewDequeFromSlice([]int{5, 3, 8, 1, 9, 2})
	less := func(a, b int) bool { return a < b }
	
	max, err := d.Max(less)
	if err != nil || max != 9 {
		t.Errorf("Expected max 9, got %d, err: %v", max, err)
	}
	
	emptyDeque := NewDeque[int]()
	_, err = emptyDeque.Max(less)
	if err == nil {
		t.Error("Should fail on empty deque")
	}
}

func TestAll(t *testing.T) {
	d := NewDequeFromSlice([]int{2, 4, 6, 8})
	predicate := func(x int) bool { return x%2 == 0 }
	
	if !d.All(predicate) {
		t.Error("All elements should be even")
	}
	
	d.PushBack(5)
	if d.All(predicate) {
		t.Error("Not all elements should be even now")
	}
}

func TestAny(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 3, 5, 7})
	predicate := func(x int) bool { return x%2 == 0 }
	
	if d.Any(predicate) {
		t.Error("No elements should be even")
	}
	
	d.PushBack(2)
	if !d.Any(predicate) {
		t.Error("At least one element should be even now")
	}
}

func TestFirst(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	predicate := func(x int) bool { return x > 2 }
	
	val, err := d.First(predicate)
	if err != nil || val != 3 {
		t.Errorf("Expected 3, got %d, err: %v", val, err)
	}
	
	predicate2 := func(x int) bool { return x > 10 }
	_, err = d.First(predicate2)
	if err == nil {
		t.Error("Should not find element > 10")
	}
}

func TestLast(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	predicate := func(x int) bool { return x < 4 }
	
	val, err := d.Last(predicate)
	if err != nil || val != 3 {
		t.Errorf("Expected 3, got %d, err: %v", val, err)
	}
	
	predicate2 := func(x int) bool { return x > 10 }
	_, err = d.Last(predicate2)
	if err == nil {
		t.Error("Should not find element > 10")
	}
}

// ============================================================================
// String Tests
// ============================================================================

func TestString(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3})
	str := d.String()
	
	if str != "Deque[1, 2, 3]" {
		t.Errorf("Unexpected string representation: %s", str)
	}
	
	emptyDeque := NewDeque[int]()
	str = emptyDeque.String()
	if str != "Deque[]" {
		t.Errorf("Expected 'Deque[]', got '%s'", str)
	}
}

// ============================================================================
// Iterator Tests
// ============================================================================

func TestIterator(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	expected := []int{1, 2, 3, 4, 5}
	
	i := 0
	for val := range d.Iterator() {
		if val != expected[i] {
			t.Errorf("Iterator index %d: expected %d, got %d", i, expected[i], val)
		}
		i++
	}
	
	if i != 5 {
		t.Errorf("Expected 5 iterations, got %d", i)
	}
}

func TestReverseIterator(t *testing.T) {
	d := NewDequeFromSlice([]int{1, 2, 3, 4, 5})
	expected := []int{5, 4, 3, 2, 1}
	
	i := 0
	for val := range d.ReverseIterator() {
		if val != expected[i] {
			t.Errorf("ReverseIterator index %d: expected %d, got %d", i, expected[i], val)
		}
		i++
	}
	
	if i != 5 {
		t.Errorf("Expected 5 iterations, got %d", i)
	}
}

// ============================================================================
// Edge Cases Tests
// ============================================================================

func TestEmptyDequeOperations(t *testing.T) {
	d := NewDeque[int]()
	
	_, err := d.PopFront()
	if !errors.Is(err, ErrEmptyDeque) {
		t.Error("PopFront on empty deque should return ErrEmptyDeque")
	}
	
	_, err = d.PopBack()
	if !errors.Is(err, ErrEmptyDeque) {
		t.Error("PopBack on empty deque should return ErrEmptyDeque")
	}
	
	_, err = d.Front()
	if !errors.Is(err, ErrEmptyDeque) {
		t.Error("Front on empty deque should return ErrEmptyDeque")
	}
	
	_, err = d.Back()
	if !errors.Is(err, ErrEmptyDeque) {
		t.Error("Back on empty deque should return ErrEmptyDeque")
	}
}

func TestSingleElementOperations(t *testing.T) {
	d := NewDeque[int]()
	d.PushBack(42)
	
	if d.Len() != 1 {
		t.Errorf("Expected length 1, got %d", d.Len())
	}
	
	front, _ := d.Front()
	back, _ := d.Back()
	if front != 42 || back != 42 {
		t.Error("Front and Back should be the same for single element")
	}
	
	val, _ := d.PopFront()
	if val != 42 {
		t.Errorf("Expected 42, got %d", val)
	}
	
	if !d.IsEmpty() {
		t.Error("Deque should be empty after popping single element")
	}
}

func TestLargeDequeOperations(t *testing.T) {
	d := NewDeque[int]()
	
	// Push 10000 elements
	for i := 0; i < 10000; i++ {
		d.PushBack(i)
	}
	
	if d.Len() != 10000 {
		t.Errorf("Expected length 10000, got %d", d.Len())
	}
	
	// Pop all from front
	for i := 0; i < 10000; i++ {
		val, err := d.PopFront()
		if err != nil || val != i {
			t.Errorf("Expected %d, got %d, err: %v", i, val, err)
			break
		}
	}
	
	if !d.IsEmpty() {
		t.Error("Deque should be empty after popping all elements")
	}
}

// ============================================================================
// String Type Tests
// ============================================================================

func TestStringDeque(t *testing.T) {
	d := NewDeque[string]()
	d.PushBack("hello")
	d.PushBack("world")
	d.PushFront("greeting:")
	
	if d.Len() != 3 {
		t.Errorf("Expected length 3, got %d", d.Len())
	}
	
	front, _ := d.Front()
	if front != "greeting:" {
		t.Errorf("Expected 'greeting:', got '%s'", front)
	}
	
	back, _ := d.Back()
	if back != "world" {
		t.Errorf("Expected 'world', got '%s'", back)
	}
}

// ============================================================================
// Custom Type Tests
// ============================================================================

type Person struct {
	Name string
	Age  int
}

func TestCustomTypeDeque(t *testing.T) {
	d := NewDeque[Person]()
	d.PushBack(Person{"Alice", 30})
	d.PushBack(Person{"Bob", 25})
	d.PushFront(Person{"Charlie", 35})
	
	if d.Len() != 3 {
		t.Errorf("Expected length 3, got %d", d.Len())
	}
	
	front, _ := d.Front()
	if front.Name != "Charlie" {
		t.Errorf("Expected 'Charlie', got '%s'", front.Name)
	}
	
	// Test Find with custom type
	person, err := d.Find(func(p Person) bool { return p.Age == 25 })
	if err != nil || person.Name != "Bob" {
		t.Errorf("Expected Bob (age 25), got %s, err: %v", person.Name, err)
	}
}

// ============================================================================
// Capacity Tests
// ============================================================================

func TestEnsureCapacity(t *testing.T) {
	d := NewDeque[int]()
	d.EnsureCapacity(100)
	
	if d.Cap() < 100 {
		t.Errorf("Expected capacity >= 100, got %d", d.Cap())
	}
}

func TestTrimExcess(t *testing.T) {
	d := NewDequeWithCapacity[int](100)
	for i := 0; i < 10; i++ {
		d.PushBack(i)
	}
	
	d.TrimExcess()
	
	if d.Cap() != 10 {
		t.Errorf("Expected capacity 10, got %d", d.Cap())
	}
}

// ============================================================================
// Benchmarks
// ============================================================================

func BenchmarkPushBack(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < b.N; i++ {
		d.PushBack(i)
	}
}

func BenchmarkPushFront(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < b.N; i++ {
		d.PushFront(i)
	}
}

func BenchmarkPopFront(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < b.N; i++ {
		d.PushBack(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		d.PopFront()
	}
}

func BenchmarkPopBack(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < b.N; i++ {
		d.PushBack(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		d.PopBack()
	}
}

func BenchmarkGet(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < 10000; i++ {
		d.PushBack(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		d.Get(i % 10000)
	}
}

func BenchmarkRotateLeft(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < 1000; i++ {
		d.PushBack(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		d.RotateLeft(1)
	}
}

func BenchmarkFilter(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < 1000; i++ {
		d.PushBack(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		d.Filter(func(x int) bool { return x%2 == 0 })
	}
}

func BenchmarkMap(b *testing.B) {
	d := NewDeque[int]()
	for i := 0; i < 1000; i++ {
		d.PushBack(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Map(d, func(x int) int { return x * 2 })
	}
}