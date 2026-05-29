// Package interval_tree_utils provides an Interval Tree (augmented Binary Search Tree)
// for efficient overlapping interval queries.
//
// An interval tree stores intervals and allows querying for all intervals that overlap
// with a given point or interval. Time complexity for insertion and deletion is O(log n),
// and for querying O(log n + k) where k is the number of results.
package interval_tree_utils

import (
	"fmt"
	"sort"
)

// Interval represents a range with a start and end point.
// The interval is half-open: [Start, End) - includes Start but not End.
type Interval struct {
	Start int
	End   int
	Data  interface{} // Optional user data associated with the interval
}

// NewInterval creates a new interval with optional data.
func NewInterval(start, end int, data interface{}) Interval {
	return Interval{Start: start, End: end, Data: data}
}

// Contains checks if a point is within the interval.
func (i Interval) Contains(point int) bool {
	return point >= i.Start && point < i.End
}

// Overlaps checks if this interval overlaps with another interval.
func (i Interval) Overlaps(other Interval) bool {
	return i.Start < other.End && other.Start < i.End
}

// Length returns the length of the interval.
func (i Interval) Length() int {
	return i.End - i.Start
}

// String returns a string representation of the interval.
func (i Interval) String() string {
	if i.Data != nil {
		return fmt.Sprintf("[%d, %d) %v", i.Start, i.End, i.Data)
	}
	return fmt.Sprintf("[%d, %d)", i.Start, i.End)
}

// Node represents a node in the interval tree.
type Node struct {
	Interval    Interval
	MaxEnd      int  // Maximum end value in the subtree rooted at this node
	Left        *Node
	Right       *Node
	Height      int  // Height of the node for AVL balancing
	Balance     int  // Balance factor for AVL
}

// IntervalTree is an AVL-balanced interval tree.
type IntervalTree struct {
	Root   *Node
	Count  int
}

// NewIntervalTree creates a new empty interval tree.
func NewIntervalTree() *IntervalTree {
	return &IntervalTree{}
}

// Insert adds an interval to the tree.
func (t *IntervalTree) Insert(interval Interval) {
	t.Root = t.insert(t.Root, interval)
	t.Count++
}

func (t *IntervalTree) insert(node *Node, interval Interval) *Node {
	if node == nil {
		return &Node{
			Interval: interval,
			MaxEnd:  interval.End,
			Height:  1,
		}
	}

	if interval.Start < node.Interval.Start {
		node.Left = t.insert(node.Left, interval)
	} else {
		node.Right = t.insert(node.Right, interval)
	}

	// Update max end
	node.MaxEnd = max(node.Interval.End, max(getMaxEnd(node.Left), getMaxEnd(node.Right)))

	// Update height and balance
	node.Height = 1 + max(getHeight(node.Left), getHeight(node.Right))
	node.Balance = getHeight(node.Left) - getHeight(node.Right)

	// Rebalance if needed (AVL)
	return t.rebalance(node)
}

// Delete removes an interval from the tree.
func (t *IntervalTree) Delete(interval Interval) bool {
	if t.Root == nil {
		return false
	}
	
	found := false
	t.Root, found = t.delete(t.Root, interval)
	if found {
		t.Count--
	}
	return found
}

func (t *IntervalTree) delete(node *Node, interval Interval) (*Node, bool) {
	if node == nil {
		return nil, false
	}

	found := false

	if interval.Start < node.Interval.Start {
		node.Left, found = t.delete(node.Left, interval)
	} else if interval.Start > node.Interval.Start {
		node.Right, found = t.delete(node.Right, interval)
	} else {
		// Found potential match - check if same interval
		if node.Interval.End == interval.End && node.Interval.Data == interval.Data {
			found = true
			if node.Left == nil {
				return node.Right, true
			}
			if node.Right == nil {
				return node.Left, true
			}
			// Node has two children - find inorder successor
			successor := t.findMin(node.Right)
			node.Interval = successor.Interval
			node.Right, _ = t.delete(node.Right, successor.Interval)
		} else {
			// Same start but different - search both sides
			node.Left, found = t.delete(node.Left, interval)
			if !found {
				node.Right, found = t.delete(node.Right, interval)
			}
		}
	}

	if node == nil {
		return nil, found
	}

	// Update max end
	node.MaxEnd = max(node.Interval.End, max(getMaxEnd(node.Left), getMaxEnd(node.Right)))

	// Update height and balance
	node.Height = 1 + max(getHeight(node.Left), getHeight(node.Right))
	node.Balance = getHeight(node.Left) - getHeight(node.Right)

	return t.rebalance(node), found
}

func (t *IntervalTree) findMin(node *Node) *Node {
	for node.Left != nil {
		node = node.Left
	}
	return node
}

// QueryPoint finds all intervals that contain the given point.
func (t *IntervalTree) QueryPoint(point int) []Interval {
	var results []Interval
	t.queryPoint(t.Root, point, &results)
	return results
}

func (t *IntervalTree) queryPoint(node *Node, point int, results *[]Interval) {
	if node == nil {
		return
	}

	// If point is greater than max end in this subtree, no overlap possible
	if point > node.MaxEnd {
		return
	}

	// Check left subtree
	t.queryPoint(node.Left, point, results)

	// Check current node
	if node.Interval.Contains(point) {
		*results = append(*results, node.Interval)
	}

	// If point is less than interval start, no need to check right
	if point < node.Interval.Start {
		return
	}

	// Check right subtree
	t.queryPoint(node.Right, point, results)
}

// QueryOverlaps finds all intervals that overlap with the given interval.
func (t *IntervalTree) QueryOverlaps(interval Interval) []Interval {
	var results []Interval
	t.queryOverlaps(t.Root, interval, &results)
	return results
}

func (t *IntervalTree) queryOverlaps(node *Node, interval Interval, results *[]Interval) {
	if node == nil {
		return
	}

	// If interval starts after max end in subtree, no overlap possible
	if interval.Start >= node.MaxEnd {
		return
	}

	// Check left subtree
	t.queryOverlaps(node.Left, interval, results)

	// Check current node
	if node.Interval.Overlaps(interval) {
		*results = append(*results, node.Interval)
	}

	// If interval ends before current interval starts, no need to check right
	if interval.End <= node.Interval.Start {
		return
	}

	// Check right subtree
	t.queryOverlaps(node.Right, interval, results)
}

// ContainsPoint checks if any interval contains the given point.
func (t *IntervalTree) ContainsPoint(point int) bool {
	return t.containsPoint(t.Root, point)
}

func (t *IntervalTree) containsPoint(node *Node, point int) bool {
	if node == nil {
		return false
	}

	if point > node.MaxEnd {
		return false
	}

	if node.Interval.Contains(point) {
		return true
	}

	if point < node.Interval.Start {
		return t.containsPoint(node.Left, point)
	}

	return t.containsPoint(node.Left, point) || t.containsPoint(node.Right, point)
}

// HasOverlap checks if any interval overlaps with the given interval.
func (t *IntervalTree) HasOverlap(interval Interval) bool {
	return t.hasOverlap(t.Root, interval)
}

func (t *IntervalTree) hasOverlap(node *Node, interval Interval) bool {
	if node == nil {
		return false
	}

	if interval.Start >= node.MaxEnd {
		return false
	}

	if node.Interval.Overlaps(interval) {
		return true
	}

	if interval.End <= node.Interval.Start {
		return t.hasOverlap(node.Left, interval)
	}

	return t.hasOverlap(node.Left, interval) || t.hasOverlap(node.Right, interval)
}

// GetAll returns all intervals in the tree.
func (t *IntervalTree) GetAll() []Interval {
	var results []Interval
	t.inorder(t.Root, &results)
	return results
}

func (t *IntervalTree) inorder(node *Node, results *[]Interval) {
	if node == nil {
		return
	}
	t.inorder(node.Left, results)
	*results = append(*results, node.Interval)
	t.inorder(node.Right, results)
}

// IsEmpty checks if the tree is empty.
func (t *IntervalTree) IsEmpty() bool {
	return t.Root == nil
}

// Size returns the number of intervals in the tree.
func (t *IntervalTree) Size() int {
	return t.Count
}

// Clear removes all intervals from the tree.
func (t *IntervalTree) Clear() {
	t.Root = nil
	t.Count = 0
}

// Height returns the height of the tree.
func (t *IntervalTree) Height() int {
	return getHeight(t.Root)
}

// FindGaps returns gaps between intervals that don't overlap with any interval in the tree.
// The range parameter specifies the overall range to search for gaps.
func (t *IntervalTree) FindGaps(rangeStart, rangeEnd int) []Interval {
	allIntervals := t.GetAll()
	if len(allIntervals) == 0 {
		return []Interval{{Start: rangeStart, End: rangeEnd}}
	}

	// Sort by start
	sort.Slice(allIntervals, func(i, j int) bool {
		return allIntervals[i].Start < allIntervals[j].Start
	})

	var gaps []Interval
	currentEnd := rangeStart

	for _, iv := range allIntervals {
		if iv.Start > currentEnd && iv.Start > rangeStart {
			gapStart := max(currentEnd, rangeStart)
			gapEnd := min(iv.Start, rangeEnd)
			if gapStart < gapEnd {
				gaps = append(gaps, Interval{Start: gapStart, End: gapEnd})
			}
		}
		if iv.End > currentEnd {
			currentEnd = iv.End
		}
	}

	// Check for gap at the end
	if currentEnd < rangeEnd {
		gaps = append(gaps, Interval{Start: max(currentEnd, rangeStart), End: rangeEnd})
	}

	return gaps
}

// MergeOverlapping returns a new slice of intervals with overlapping intervals merged.
func MergeOverlapping(intervals []Interval) []Interval {
	if len(intervals) == 0 {
		return intervals
	}

	// Sort by start
	sort.Slice(intervals, func(i, j int) bool {
		return intervals[i].Start < intervals[j].Start
	})

	var merged []Interval
	current := intervals[0]

	for i := 1; i < len(intervals); i++ {
		if intervals[i].Start <= current.End {
			// Overlapping - merge
			if intervals[i].End > current.End {
				current.End = intervals[i].End
			}
		} else {
			merged = append(merged, current)
			current = intervals[i]
		}
	}
	merged = append(merged, current)

	return merged
}

// Coverage calculates total coverage (union length) of intervals.
func Coverage(intervals []Interval) int {
	merged := MergeOverlapping(intervals)
	total := 0
	for _, iv := range merged {
		total += iv.Length()
	}
	return total
}

// Intersection returns the intersection of two intervals, or false if they don't overlap.
func Intersection(a, b Interval) (Interval, bool) {
	if !a.Overlaps(b) {
		return Interval{}, false
	}
	return Interval{
		Start: max(a.Start, b.Start),
		End:   min(a.End, b.End),
	}, true
}

// Union returns the union of two intervals if they overlap or are adjacent.
func Union(a, b Interval) (Interval, bool) {
	if !a.Overlaps(b) && a.End != b.Start && b.End != a.Start {
		return Interval{}, false
	}
	return Interval{
		Start: min(a.Start, b.Start),
		End:   max(a.End, b.End),
	}, true
}

// Helper functions

func getHeight(node *Node) int {
	if node == nil {
		return 0
	}
	return node.Height
}

func getMaxEnd(node *Node) int {
	if node == nil {
		return 0
	}
	return node.MaxEnd
}

func (t *IntervalTree) rebalance(node *Node) *Node {
	// Left heavy
	if node.Balance > 1 {
		if getHeight(node.Left.Left) >= getHeight(node.Left.Right) {
			return t.rotateRight(node)
		}
		node.Left = t.rotateLeft(node.Left)
		return t.rotateRight(node)
	}

	// Right heavy
	if node.Balance < -1 {
		if getHeight(node.Right.Right) >= getHeight(node.Right.Left) {
			return t.rotateLeft(node)
		}
		node.Right = t.rotateRight(node.Right)
		return t.rotateLeft(node)
	}

	return node
}

func (t *IntervalTree) rotateRight(y *Node) *Node {
	x := y.Left
	T2 := x.Right

	x.Right = y
	y.Left = T2

	// Update heights
	y.Height = 1 + max(getHeight(y.Left), getHeight(y.Right))
	x.Height = 1 + max(getHeight(x.Left), getHeight(x.Right))

	// Update balance factors
	y.Balance = getHeight(y.Left) - getHeight(y.Right)
	x.Balance = getHeight(x.Left) - getHeight(x.Right)

	// Update max ends
	y.MaxEnd = max(y.Interval.End, max(getMaxEnd(y.Left), getMaxEnd(y.Right)))
	x.MaxEnd = max(x.Interval.End, max(getMaxEnd(x.Left), getMaxEnd(x.Right)))

	return x
}

func (t *IntervalTree) rotateLeft(x *Node) *Node {
	y := x.Right
	T2 := y.Left

	y.Left = x
	x.Right = T2

	// Update heights
	x.Height = 1 + max(getHeight(x.Left), getHeight(x.Right))
	y.Height = 1 + max(getHeight(y.Left), getHeight(y.Right))

	// Update balance factors
	x.Balance = getHeight(x.Left) - getHeight(x.Right)
	y.Balance = getHeight(y.Left) - getHeight(y.Right)

	// Update max ends
	x.MaxEnd = max(x.Interval.End, max(getMaxEnd(x.Left), getMaxEnd(x.Right)))
	y.MaxEnd = max(y.Interval.End, max(getMaxEnd(y.Left), getMaxEnd(y.Right)))

	return y
}

// String returns a visual representation of the tree (for debugging).
func (t *IntervalTree) String() string {
	if t.Root == nil {
		return "Empty tree"
	}
	return t.stringHelper(t.Root, "", true)
}

func (t *IntervalTree) stringHelper(node *Node, prefix string, isTail bool) string {
	if node == nil {
		return ""
	}

	var result string
	result += t.stringHelper(node.Right, prefix+"│   ", false)
	result += fmt.Sprintf("%s%s [%d,%d) maxEnd=%d\n", prefix, getBranch(isTail), node.Interval.Start, node.Interval.End, node.MaxEnd)
	result += t.stringHelper(node.Left, prefix+"│   ", true)

	return result
}

func getBranch(isTail bool) string {
	if isTail {
		return "└── "
	}
	return "┌── "
}