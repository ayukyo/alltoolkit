package interval_tree_utils

import (
	"fmt"
	"testing"
)

func TestIntervalCreation(t *testing.T) {
	iv := NewInterval(5, 10, "test data")
	
	if iv.Start != 5 {
		t.Errorf("Expected Start=5, got %d", iv.Start)
	}
	if iv.End != 10 {
		t.Errorf("Expected End=10, got %d", iv.End)
	}
	if iv.Data != "test data" {
		t.Errorf("Expected data='test data', got %v", iv.Data)
	}
}

func TestIntervalContains(t *testing.T) {
	iv := NewInterval(5, 10, nil)
	
	tests := []struct {
		point     int
		expected  bool
	}{
		{4, false},
		{5, true},
		{7, true},
		{9, true},
		{10, false},
		{11, false},
	}
	
	for _, tt := range tests {
		if got := iv.Contains(tt.point); got != tt.expected {
			t.Errorf("Contains(%d) = %v, want %v", tt.point, got, tt.expected)
		}
	}
}

func TestIntervalOverlaps(t *testing.T) {
	iv := NewInterval(5, 10, nil)
	
	tests := []struct {
		other     Interval
		expected  bool
	}{
		{NewInterval(0, 5, nil), false},   // Adjacent, no overlap
		{NewInterval(10, 15, nil), false},  // Adjacent, no overlap
		{NewInterval(3, 6, nil), true},    // Overlaps at start
		{NewInterval(8, 12, nil), true},  // Overlaps at end
		{NewInterval(3, 12, nil), true},   // Contains
		{NewInterval(6, 8, nil), true},    // Contained
		{NewInterval(0, 3, nil), false},   // No overlap
		{NewInterval(11, 15, nil), false}, // No overlap
	}
	
	for _, tt := range tests {
		if got := iv.Overlaps(tt.other); got != tt.expected {
			t.Errorf("Overlaps(%v) = %v, want %v", tt.other, got, tt.expected)
		}
	}
}

func TestIntervalLength(t *testing.T) {
	iv := NewInterval(5, 10, nil)
	if iv.Length() != 5 {
		t.Errorf("Expected Length=5, got %d", iv.Length())
	}
	
	iv2 := NewInterval(0, 100, nil)
	if iv2.Length() != 100 {
		t.Errorf("Expected Length=100, got %d", iv2.Length())
	}
}

func TestIntervalTreeInsert(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, nil))
	tree.Insert(NewInterval(15, 20, nil))
	tree.Insert(NewInterval(1, 3, nil))
	
	if tree.Size() != 3 {
		t.Errorf("Expected Size=3, got %d", tree.Size())
	}
	if tree.IsEmpty() {
		t.Error("Tree should not be empty")
	}
}

func TestIntervalTreeQueryPoint(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, "A"))
	tree.Insert(NewInterval(15, 20, "B"))
	tree.Insert(NewInterval(8, 12, "C"))
	tree.Insert(NewInterval(1, 6, "D"))
	
	tests := []struct {
		point        int
		expectedData []interface{}
	}{
		{0, []interface{}{}},
		{1, []interface{}{"D"}},
		{5, []interface{}{"A", "D"}},  // 5 in [5,10) and [1,6)
		{7, []interface{}{"A"}},        // 7 only in [5,10), not in [8,12)
		{9, []interface{}{"A", "C"}},   // 9 in [5,10) and [8,12)
		{11, []interface{}{"C"}},
		{17, []interface{}{"B"}},
		{25, []interface{}{}},
	}
	
	for _, tt := range tests {
		results := tree.QueryPoint(tt.point)
		if len(results) != len(tt.expectedData) {
			t.Errorf("QueryPoint(%d) returned %d results, want %d", 
				tt.point, len(results), len(tt.expectedData))
			continue
		}
		
		// Check if all expected data is present
		for _, exp := range tt.expectedData {
			found := false
			for _, r := range results {
				if r.Data == exp {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("QueryPoint(%d) missing expected data %v", tt.point, exp)
			}
		}
	}
}

func TestIntervalTreeQueryOverlaps(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, "A"))
	tree.Insert(NewInterval(15, 20, "B"))
	tree.Insert(NewInterval(8, 12, "C"))
	tree.Insert(NewInterval(1, 6, "D"))
	
	tests := []struct {
		interval     Interval
		expectedData []interface{}
	}{
		{NewInterval(0, 1, nil), []interface{}{}},
		{NewInterval(2, 4, nil), []interface{}{"D"}},
		{NewInterval(7, 9, nil), []interface{}{"A", "C"}},
		{NewInterval(9, 11, nil), []interface{}{"A", "C"}},
		{NewInterval(10, 16, nil), []interface{}{"C", "B"}},
		{NewInterval(16, 18, nil), []interface{}{"B"}},
		{NewInterval(25, 30, nil), []interface{}{}},
	}
	
	for _, tt := range tests {
		results := tree.QueryOverlaps(tt.interval)
		if len(results) != len(tt.expectedData) {
			t.Errorf("QueryOverlaps(%v) returned %d results, want %d", 
				tt.interval, len(results), len(tt.expectedData))
		}
	}
}

func TestIntervalTreeContainsPoint(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, nil))
	tree.Insert(NewInterval(15, 20, nil))
	
	if !tree.ContainsPoint(7) {
		t.Error("Expected ContainsPoint(7)=true")
	}
	if !tree.ContainsPoint(17) {
		t.Error("Expected ContainsPoint(17)=true")
	}
	if tree.ContainsPoint(12) {
		t.Error("Expected ContainsPoint(12)=false")
	}
	if tree.ContainsPoint(25) {
		t.Error("Expected ContainsPoint(25)=false")
	}
}

func TestIntervalTreeHasOverlap(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, nil))
	tree.Insert(NewInterval(15, 20, nil))
	
	if !tree.HasOverlap(NewInterval(7, 9, nil)) {
		t.Error("Expected HasOverlap([7,9))=true")
	}
	if !tree.HasOverlap(NewInterval(3, 6, nil)) {
		t.Error("Expected HasOverlap([3,6))=true")
	}
	if tree.HasOverlap(NewInterval(10, 15, nil)) {
		t.Error("Expected HasOverlap([10,15))=false")
	}
}

func TestIntervalTreeDelete(t *testing.T) {
	tree := NewIntervalTree()
	
	iv1 := NewInterval(5, 10, "A")
	iv2 := NewInterval(15, 20, "B")
	
	tree.Insert(iv1)
	tree.Insert(iv2)
	
	if tree.Size() != 2 {
		t.Errorf("Expected Size=2, got %d", tree.Size())
	}
	
	deleted := tree.Delete(iv1)
	if !deleted {
		t.Error("Expected Delete to return true")
	}
	if tree.Size() != 1 {
		t.Errorf("Expected Size=1 after delete, got %d", tree.Size())
	}
	
	results := tree.QueryPoint(7)
	if len(results) != 0 {
		t.Error("Expected no intervals containing point 7")
	}
	
	results = tree.QueryPoint(17)
	if len(results) != 1 {
		t.Error("Expected one interval containing point 17")
	}
}

func TestIntervalTreeClear(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, nil))
	tree.Insert(NewInterval(15, 20, nil))
	
	tree.Clear()
	
	if !tree.IsEmpty() {
		t.Error("Expected tree to be empty after Clear")
	}
	if tree.Size() != 0 {
		t.Errorf("Expected Size=0, got %d", tree.Size())
	}
}

func TestIntervalTreeGetAll(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, nil))
	tree.Insert(NewInterval(15, 20, nil))
	tree.Insert(NewInterval(1, 3, nil))
	
	all := tree.GetAll()
	if len(all) != 3 {
		t.Errorf("Expected 3 intervals, got %d", len(all))
	}
}

func TestIntervalTreeHeight(t *testing.T) {
	tree := NewIntervalTree()
	
	if tree.Height() != 0 {
		t.Errorf("Expected empty tree height=0, got %d", tree.Height())
	}
	
	// Insert nodes to create a balanced tree
	tree.Insert(NewInterval(10, 15, nil))
	if tree.Height() != 1 {
		t.Errorf("Expected height=1, got %d", tree.Height())
	}
	
	tree.Insert(NewInterval(5, 8, nil))
	tree.Insert(NewInterval(15, 20, nil))
	if tree.Height() != 2 {
		t.Errorf("Expected height=2, got %d", tree.Height())
	}
}

func TestIntervalTreeFindGaps(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(5, 10, nil))
	tree.Insert(NewInterval(15, 20, nil))
	tree.Insert(NewInterval(25, 30, nil))
	
	gaps := tree.FindGaps(0, 35)
	expected := []Interval{
		{Start: 0, End: 5},
		{Start: 10, End: 15},
		{Start: 20, End: 25},
		{Start: 30, End: 35},
	}
	
	if len(gaps) != len(expected) {
		t.Errorf("Expected %d gaps, got %d", len(expected), len(gaps))
	}
	
	for i, gap := range gaps {
		if i < len(expected) && (gap.Start != expected[i].Start || gap.End != expected[i].End) {
			t.Errorf("Gap %d: expected %v, got %v", i, expected[i], gap)
		}
	}
}

func TestMergeOverlapping(t *testing.T) {
	intervals := []Interval{
		NewInterval(1, 5, nil),
		NewInterval(3, 7, nil),
		NewInterval(10, 15, nil),
		NewInterval(12, 18, nil),
		NewInterval(20, 25, nil),
	}
	
	merged := MergeOverlapping(intervals)
	
	expected := []Interval{
		{Start: 1, End: 7},
		{Start: 10, End: 18},
		{Start: 20, End: 25},
	}
	
	if len(merged) != len(expected) {
		t.Errorf("Expected %d merged intervals, got %d", len(expected), len(merged))
	}
	
	for i, m := range merged {
		if i < len(expected) && (m.Start != expected[i].Start || m.End != expected[i].End) {
			t.Errorf("Merged %d: expected %v, got %v", i, expected[i], m)
		}
	}
}

func TestCoverage(t *testing.T) {
	intervals := []Interval{
		NewInterval(1, 5, nil),
		NewInterval(3, 7, nil),  // Overlaps with first
		NewInterval(10, 15, nil),
		NewInterval(20, 25, nil),
	}
	
	coverage := Coverage(intervals)
	// [1,7) = 6, [10,15) = 5, [20,25) = 5 = 16
	if coverage != 16 {
		t.Errorf("Expected coverage=16, got %d", coverage)
	}
}

func TestIntersection(t *testing.T) {
	tests := []struct {
		a, b       Interval
		expected   Interval
		overlaps   bool
	}{
		{NewInterval(5, 10, nil), NewInterval(8, 15, nil), NewInterval(8, 10, nil), true},
		{NewInterval(5, 10, nil), NewInterval(10, 15, nil), Interval{}, false},
		{NewInterval(5, 10, nil), NewInterval(3, 7, nil), NewInterval(5, 7, nil), true},
		{NewInterval(5, 10, nil), NewInterval(0, 3, nil), Interval{}, false},
	}
	
	for _, tt := range tests {
		result, ok := Intersection(tt.a, tt.b)
		if ok != tt.overlaps {
			t.Errorf("Intersection(%v, %v) overlaps=%v, want %v", tt.a, tt.b, ok, tt.overlaps)
		}
		if ok && (result.Start != tt.expected.Start || result.End != tt.expected.End) {
			t.Errorf("Intersection(%v, %v) = %v, want %v", tt.a, tt.b, result, tt.expected)
		}
	}
}

func TestUnion(t *testing.T) {
	tests := []struct {
		a, b       Interval
		expected   Interval
		canMerge   bool
	}{
		{NewInterval(5, 10, nil), NewInterval(8, 15, nil), NewInterval(5, 15, nil), true},
		{NewInterval(5, 10, nil), NewInterval(10, 15, nil), NewInterval(5, 15, nil), true}, // Adjacent
		{NewInterval(5, 10, nil), NewInterval(15, 20, nil), Interval{}, false},
		{NewInterval(5, 10, nil), NewInterval(3, 7, nil), NewInterval(3, 10, nil), true},
	}
	
	for _, tt := range tests {
		result, ok := Union(tt.a, tt.b)
		if ok != tt.canMerge {
			t.Errorf("Union(%v, %v) success=%v, want %v", tt.a, tt.b, ok, tt.canMerge)
		}
		if ok && (result.Start != tt.expected.Start || result.End != tt.expected.End) {
			t.Errorf("Union(%v, %v) = %v, want %v", tt.a, tt.b, result, tt.expected)
		}
	}
}

func TestIntervalTreeBalance(t *testing.T) {
	// Insert in sorted order to trigger rebalancing
	tree := NewIntervalTree()
	
	for i := 0; i < 100; i++ {
		tree.Insert(NewInterval(i*10, i*10+5, nil))
	}
	
	// Tree should remain balanced (height should be O(log n))
	height := tree.Height()
	maxExpected := 20 // log2(100) ≈ 7, but with AVL overhead
	
	if height > maxExpected {
		t.Errorf("Tree height %d exceeds expected maximum %d", height, maxExpected)
	}
	
	// Verify all intervals can be found
	for i := 0; i < 100; i++ {
		point := i*10 + 2
		if !tree.ContainsPoint(point) {
			t.Errorf("Expected to find point %d", point)
		}
	}
}

func TestIntervalTreeString(t *testing.T) {
	tree := NewIntervalTree()
	
	if tree.String() != "Empty tree" {
		t.Errorf("Expected 'Empty tree', got %s", tree.String())
	}
	
	tree.Insert(NewInterval(5, 10, nil))
	s := tree.String()
	if s == "Empty tree" || s == "" {
		t.Error("Expected non-empty tree string")
	}
}

func TestIntervalString(t *testing.T) {
	iv1 := NewInterval(5, 10, nil)
	if iv1.String() != "[5, 10)" {
		t.Errorf("Expected '[5, 10)', got %s", iv1.String())
	}
	
	iv2 := NewInterval(5, 10, "test")
	if iv2.String() != "[5, 10) test" {
		t.Errorf("Expected '[5, 10) test', got %s", iv2.String())
	}
}

func TestIntervalTreeWithNegativeValues(t *testing.T) {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(-10, -5, nil))
	tree.Insert(NewInterval(-3, 3, nil))
	tree.Insert(NewInterval(5, 10, nil))
	
	if !tree.ContainsPoint(-7) {
		t.Error("Expected to find point -7")
	}
	if !tree.ContainsPoint(0) {
		t.Error("Expected to find point 0")
	}
	if !tree.ContainsPoint(7) {
		t.Error("Expected to find point 7")
	}
	if tree.ContainsPoint(-4) {
		t.Error("Expected not to find point -4")
	}
}

func TestIntervalTreeWithSameStart(t *testing.T) {
	tree := NewIntervalTree()
	
	// Intervals with same start but different ends
	tree.Insert(NewInterval(5, 10, "A"))
	tree.Insert(NewInterval(5, 15, "B"))
	tree.Insert(NewInterval(5, 8, "C"))
	
	results := tree.QueryPoint(7)
	if len(results) != 3 {
		t.Errorf("Expected 3 intervals containing point 7, got %d", len(results))
	}
	
	results = tree.QueryPoint(12)
	if len(results) != 1 {
		t.Errorf("Expected 1 interval containing point 12, got %d", len(results))
	}
	if len(results) > 0 && results[0].Data != "B" {
		t.Errorf("Expected interval B at point 12, got %v", results[0].Data)
	}
}

// Benchmark tests

func BenchmarkIntervalTreeInsert(b *testing.B) {
	tree := NewIntervalTree()
	for i := 0; i < b.N; i++ {
		tree.Insert(NewInterval(i*10, i*10+5, nil))
	}
}

func BenchmarkIntervalTreeQueryPoint(b *testing.B) {
	tree := NewIntervalTree()
	for i := 0; i < 1000; i++ {
		tree.Insert(NewInterval(i*10, i*10+5, nil))
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tree.QueryPoint(i % 10000)
	}
}

func BenchmarkIntervalTreeQueryOverlaps(b *testing.B) {
	tree := NewIntervalTree()
	for i := 0; i < 1000; i++ {
		tree.Insert(NewInterval(i*10, i*10+5, nil))
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tree.QueryOverlaps(NewInterval(i*10+2, i*10+20, nil))
	}
}

func BenchmarkMergeOverlapping(b *testing.B) {
	intervals := make([]Interval, 1000)
	for i := 0; i < 1000; i++ {
		intervals[i] = NewInterval(i*10, i*10+5, nil)
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		MergeOverlapping(intervals)
	}
}

// Example tests for documentation

func ExampleIntervalTree_QueryPoint() {
	tree := NewIntervalTree()
	
	// Add meeting room bookings (time in 30-minute units)
	tree.Insert(NewInterval(18, 20, "Team A standup"))  // 9:00-10:00
	tree.Insert(NewInterval(22, 24, "Product review"))   // 11:00-12:00
	tree.Insert(NewInterval(28, 32, "Client demo"))     // 14:00-16:00
	tree.Insert(NewInterval(30, 34, "Interview"))       // 15:00-17:00
	
	// Find all bookings at 15:30 (unit 31)
	// 31 is in [28,32) Client demo AND [30,34) Interview
	results := tree.QueryPoint(31)
	
	for _, iv := range results {
		fmt.Printf("At this time: %v\n", iv.Data)
	}
	// Output:
	// At this time: Client demo
	// At this time: Interview
}

func ExampleIntervalTree_QueryOverlaps() {
	tree := NewIntervalTree()
	
	tree.Insert(NewInterval(1, 5, nil))
	tree.Insert(NewInterval(10, 15, nil))
	tree.Insert(NewInterval(20, 25, nil))
	
	// Find all intervals overlapping [5, 22] - touches [1,5] and overlaps [10,15], [20,25]
	results := tree.QueryOverlaps(NewInterval(5, 22, nil))
	
	fmt.Printf("Found %d overlapping intervals\n", len(results))
	// Output:
	// Found 2 overlapping intervals
}

func ExampleMergeOverlapping() {
	intervals := []Interval{
		NewInterval(1, 5, nil),
		NewInterval(3, 7, nil),
		NewInterval(10, 15, nil),
		NewInterval(12, 18, nil),
	}
	
	merged := MergeOverlapping(intervals)
	
	for _, iv := range merged {
		fmt.Printf("%v\n", iv)
	}
	// Output:
	// [1, 7)
	// [10, 18)
}

func ExampleCoverage() {
	intervals := []Interval{
		NewInterval(0, 10, nil),
		NewInterval(5, 15, nil),  // Overlaps with first
		NewInterval(20, 30, nil),
	}
	
	total := Coverage(intervals)
	fmt.Printf("Total coverage: %d\n", total)
	// Output:
	// Total coverage: 25
}