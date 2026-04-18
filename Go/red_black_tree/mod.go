// Package red_black_tree implements a self-balancing Red-Black Tree data structure.
// Red-Black Trees provide O(log n) time complexity for insert, delete, and search operations.
//
// A Red-Black Tree is a binary search tree with the following properties:
// 1. Every node is either red or black
// 2. The root is black
// 3. All leaves (NIL) are black
// 4. If a node is red, then both its children are black
// 5. Every simple path from a node to descendant leaves contains the same number of black nodes
//
// This implementation is zero-dependency and suitable for production use.
package red_black_tree

import "fmt"

// Color represents the color of a node in the Red-Black Tree
type Color bool

const (
	Red   Color = true
	Black Color = false
)

// Node represents a node in the Red-Black Tree
type Node[T any] struct {
	Key    T
	Color  Color
	Left   *Node[T]
	Right  *Node[T]
	Parent *Node[T]
}

// Tree represents a Red-Black Tree
type Tree[T any] struct {
	root       *Node[T]
	NIL        *Node[T]
	size       int
	comparator func(a, b T) int
}

// New creates a new Red-Black Tree with a custom comparator function.
// The comparator should return:
// - negative if a < b
// - zero if a == b
// - positive if a > b
func New[T any](comparator func(a, b T) int) *Tree[T] {
	nilNode := &Node[T]{Color: Black}
	return &Tree[T]{
		root:       nilNode,
		NIL:        nilNode,
		size:       0,
		comparator: comparator,
	}
}

// NewInt creates a new Red-Black Tree for int keys with default ordering
func NewInt() *Tree[int] {
	return New(func(a, b int) int {
		if a < b {
			return -1
		} else if a > b {
			return 1
		}
		return 0
	})
}

// NewString creates a new Red-Black Tree for string keys with lexicographic ordering
func NewString() *Tree[string] {
	return New(func(a, b string) int {
		if a < b {
			return -1
		} else if a > b {
			return 1
		}
		return 0
	})
}

// Size returns the number of nodes in the tree
func (t *Tree[T]) Size() int {
	return t.size
}

// IsEmpty returns true if the tree has no nodes
func (t *Tree[T]) IsEmpty() bool {
	return t.size == 0
}

// Root returns the root node of the tree (nil if empty)
func (t *Tree[T]) Root() *Node[T] {
	if t.root == t.NIL {
		return nil
	}
	return t.root
}

// Insert adds a new key to the tree
// Returns true if inserted, false if key already exists
func (t *Tree[T]) Insert(key T) bool {
	node := &Node[T]{
		Key:    key,
		Color:  Red,
		Left:   t.NIL,
		Right:  t.NIL,
		Parent: t.NIL,
	}

	var parent *Node[T] = t.NIL
	current := t.root

	for current != t.NIL {
		parent = current
		cmp := t.comparator(key, current.Key)
		if cmp < 0 {
			current = current.Left
		} else if cmp > 0 {
			current = current.Right
		} else {
			// Key already exists
			return false
		}
	}

	node.Parent = parent

	if parent == t.NIL {
		t.root = node
	} else if t.comparator(key, parent.Key) < 0 {
		parent.Left = node
	} else {
		parent.Right = node
	}

	t.size++
	t.insertFixup(node)
	return true
}

// insertFixup restores Red-Black Tree properties after insertion
func (t *Tree[T]) insertFixup(node *Node[T]) {
	for node.Parent.Color == Red {
		if node.Parent == node.Parent.Parent.Left {
			uncle := node.Parent.Parent.Right
			if uncle.Color == Red {
				// Case 1: Uncle is red
				node.Parent.Color = Black
				uncle.Color = Black
				node.Parent.Parent.Color = Red
				node = node.Parent.Parent
			} else {
				if node == node.Parent.Right {
					// Case 2: Uncle is black, node is right child
					node = node.Parent
					t.leftRotate(node)
				}
				// Case 3: Uncle is black, node is left child
				node.Parent.Color = Black
				node.Parent.Parent.Color = Red
				t.rightRotate(node.Parent.Parent)
			}
		} else {
			uncle := node.Parent.Parent.Left
			if uncle.Color == Red {
				// Case 1: Uncle is red (mirror)
				node.Parent.Color = Black
				uncle.Color = Black
				node.Parent.Parent.Color = Red
				node = node.Parent.Parent
			} else {
				if node == node.Parent.Left {
					// Case 2: Uncle is black, node is left child (mirror)
					node = node.Parent
					t.rightRotate(node)
				}
				// Case 3: Uncle is black, node is right child (mirror)
				node.Parent.Color = Black
				node.Parent.Parent.Color = Red
				t.leftRotate(node.Parent.Parent)
			}
		}
	}
	t.root.Color = Black
}

// leftRotate performs a left rotation at the given node
func (t *Tree[T]) leftRotate(x *Node[T]) {
	y := x.Right
	x.Right = y.Left

	if y.Left != t.NIL {
		y.Left.Parent = x
	}

	y.Parent = x.Parent

	if x.Parent == t.NIL {
		t.root = y
	} else if x == x.Parent.Left {
		x.Parent.Left = y
	} else {
		x.Parent.Right = y
	}

	y.Left = x
	x.Parent = y
}

// rightRotate performs a right rotation at the given node
func (t *Tree[T]) rightRotate(x *Node[T]) {
	y := x.Left
	x.Left = y.Right

	if y.Right != t.NIL {
		y.Right.Parent = x
	}

	y.Parent = x.Parent

	if x.Parent == t.NIL {
		t.root = y
	} else if x == x.Parent.Right {
		x.Parent.Right = y
	} else {
		x.Parent.Left = y
	}

	y.Right = x
	x.Parent = y
}

// Search finds a node with the given key
// Returns the node if found, nil otherwise
func (t *Tree[T]) Search(key T) *Node[T] {
	current := t.root

	for current != t.NIL {
		cmp := t.comparator(key, current.Key)
		if cmp < 0 {
			current = current.Left
		} else if cmp > 0 {
			current = current.Right
		} else {
			return current
		}
	}

	return nil
}

// Contains checks if a key exists in the tree
func (t *Tree[T]) Contains(key T) bool {
	return t.Search(key) != nil
}

// Delete removes a key from the tree
// Returns true if deleted, false if key not found
func (t *Tree[T]) Delete(key T) bool {
	node := t.Search(key)
	if node == nil {
		return false
	}

	t.deleteNode(node)
	t.size--
	return true
}

// deleteNode removes a node from the tree
func (t *Tree[T]) deleteNode(node *Node[T]) {
	var y, x *Node[T]

	if node.Left == t.NIL || node.Right == t.NIL {
		y = node
	} else {
		y = t.successor(node)
	}

	if y.Left != t.NIL {
		x = y.Left
	} else {
		x = y.Right
	}

	x.Parent = y.Parent

	if y.Parent == t.NIL {
		t.root = x
	} else if y == y.Parent.Left {
		y.Parent.Left = x
	} else {
		y.Parent.Right = x
	}

	if y != node {
		node.Key = y.Key
	}

	if y.Color == Black {
		t.deleteFixup(x)
	}
}

// deleteFixup restores Red-Black Tree properties after deletion
func (t *Tree[T]) deleteFixup(x *Node[T]) {
	for x != t.root && x.Color == Black {
		if x == x.Parent.Left {
			w := x.Parent.Right
			if w.Color == Red {
				// Case 1: Sibling is red
				w.Color = Black
				x.Parent.Color = Red
				t.leftRotate(x.Parent)
				w = x.Parent.Right
			}

			if w.Left.Color == Black && w.Right.Color == Black {
				// Case 2: Sibling's children are black
				w.Color = Red
				x = x.Parent
			} else {
				if w.Right.Color == Black {
					// Case 3: Sibling's right child is black
					w.Left.Color = Black
					w.Color = Red
					t.rightRotate(w)
					w = x.Parent.Right
				}
				// Case 4: Sibling's right child is red
				w.Color = x.Parent.Color
				x.Parent.Color = Black
				w.Right.Color = Black
				t.leftRotate(x.Parent)
				x = t.root
			}
		} else {
			w := x.Parent.Left
			if w.Color == Red {
				// Case 1: Sibling is red (mirror)
				w.Color = Black
				x.Parent.Color = Red
				t.rightRotate(x.Parent)
				w = x.Parent.Left
			}

			if w.Right.Color == Black && w.Left.Color == Black {
				// Case 2: Sibling's children are black (mirror)
				w.Color = Red
				x = x.Parent
			} else {
				if w.Left.Color == Black {
					// Case 3: Sibling's left child is black (mirror)
					w.Right.Color = Black
					w.Color = Red
					t.leftRotate(w)
					w = x.Parent.Left
				}
				// Case 4: Sibling's left child is red (mirror)
				w.Color = x.Parent.Color
				x.Parent.Color = Black
				w.Left.Color = Black
				t.rightRotate(x.Parent)
				x = t.root
			}
		}
	}
	x.Color = Black
}

// successor returns the node with the smallest key greater than the given node's key
func (t *Tree[T]) successor(node *Node[T]) *Node[T] {
	if node.Right != t.NIL {
		return t.minimum(node.Right)
	}

	y := node.Parent
	for y != t.NIL && node == y.Right {
		node = y
		y = y.Parent
	}
	return y
}

// minimum returns the node with the minimum key in the subtree rooted at node
func (t *Tree[T]) minimum(node *Node[T]) *Node[T] {
	for node.Left != t.NIL {
		node = node.Left
	}
	return node
}

// maximum returns the node with the maximum key in the subtree rooted at node
func (t *Tree[T]) maximum(node *Node[T]) *Node[T] {
	for node.Right != t.NIL {
		node = node.Right
	}
	return node
}

// Min returns the minimum key in the tree
// Returns the key and true if found, zero value and false if tree is empty
func (t *Tree[T]) Min() (T, bool) {
	if t.IsEmpty() {
		var zero T
		return zero, false
	}
	node := t.minimum(t.root)
	return node.Key, true
}

// Max returns the maximum key in the tree
// Returns the key and true if found, zero value and false if tree is empty
func (t *Tree[T]) Max() (T, bool) {
	if t.IsEmpty() {
		var zero T
		return zero, false
	}
	node := t.maximum(t.root)
	return node.Key, true
}

// InOrder returns all keys in ascending order
func (t *Tree[T]) InOrder() []T {
	result := make([]T, 0, t.size)
	t.inOrderWalk(t.root, &result)
	return result
}

func (t *Tree[T]) inOrderWalk(node *Node[T], result *[]T) {
	if node != t.NIL {
		t.inOrderWalk(node.Left, result)
		*result = append(*result, node.Key)
		t.inOrderWalk(node.Right, result)
	}
}

// PreOrder returns all keys in pre-order (root, left, right)
func (t *Tree[T]) PreOrder() []T {
	result := make([]T, 0, t.size)
	t.preOrderWalk(t.root, &result)
	return result
}

func (t *Tree[T]) preOrderWalk(node *Node[T], result *[]T) {
	if node != t.NIL {
		*result = append(*result, node.Key)
		t.preOrderWalk(node.Left, result)
		t.preOrderWalk(node.Right, result)
	}
}

// PostOrder returns all keys in post-order (left, right, root)
func (t *Tree[T]) PostOrder() []T {
	result := make([]T, 0, t.size)
	t.postOrderWalk(t.root, &result)
	return result
}

func (t *Tree[T]) postOrderWalk(node *Node[T], result *[]T) {
	if node != t.NIL {
		t.postOrderWalk(node.Left, result)
		t.postOrderWalk(node.Right, result)
		*result = append(*result, node.Key)
	}
}

// Clear removes all nodes from the tree
func (t *Tree[T]) Clear() {
	t.root = t.NIL
	t.size = 0
}

// Height returns the height of the tree
// Returns -1 for empty tree
func (t *Tree[T]) Height() int {
	return t.height(t.root)
}

func (t *Tree[T]) height(node *Node[T]) int {
	if node == t.NIL {
		return -1
	}
	leftHeight := t.height(node.Left)
	rightHeight := t.height(node.Right)
	if leftHeight > rightHeight {
		return leftHeight + 1
	}
	return rightHeight + 1
}

// Validate checks if the tree satisfies all Red-Black Tree properties
// Returns an error if validation fails, nil otherwise
func (t *Tree[T]) Validate() error {
	if t.IsEmpty() {
		return nil
	}

	// Property 2: Root must be black
	if t.root.Color != Black {
		return fmt.Errorf("root is not black")
	}

	// Check all properties recursively
	_, err := t.validateNode(t.root)
	return err
}

func (t *Tree[T]) validateNode(node *Node[T]) (int, error) {
	if node == t.NIL {
		return 0, nil
	}

	// Property 4: Red nodes have black children
	if node.Color == Red {
		if node.Left.Color != Black || node.Right.Color != Black {
			return 0, fmt.Errorf("red node has non-black child")
		}
	}

	// Property 5: Equal black height on all paths
	leftBlackHeight, err := t.validateNode(node.Left)
	if err != nil {
		return 0, err
	}

	rightBlackHeight, err := t.validateNode(node.Right)
	if err != nil {
		return 0, err
	}

	if leftBlackHeight != rightBlackHeight {
		return 0, fmt.Errorf("unequal black heights: left=%d, right=%d", leftBlackHeight, rightBlackHeight)
	}

	// Add 1 if current node is black
	currentBlackHeight := leftBlackHeight
	if node.Color == Black {
		currentBlackHeight++
	}

	return currentBlackHeight, nil
}

// Range returns all keys in the range [start, end]
func (t *Tree[T]) Range(start, end T) []T {
	result := make([]T, 0)
	t.rangeWalk(t.root, start, end, &result)
	return result
}

func (t *Tree[T]) rangeWalk(node *Node[T], start, end T, result *[]T) {
	if node == t.NIL {
		return
	}

	// If current key > start, explore left subtree
	if t.comparator(node.Key, start) > 0 {
		t.rangeWalk(node.Left, start, end, result)
	}

	// If key is in range, add it
	if t.comparator(node.Key, start) >= 0 && t.comparator(node.Key, end) <= 0 {
		*result = append(*result, node.Key)
	}

	// If current key < end, explore right subtree
	if t.comparator(node.Key, end) < 0 {
		t.rangeWalk(node.Right, start, end, result)
	}
}

// LowerBound returns the first key >= target
// Returns the key and true if found, zero value and false if not found
func (t *Tree[T]) LowerBound(target T) (T, bool) {
	node := t.lowerBoundNode(t.root, target)
	if node == t.NIL {
		var zero T
		return zero, false
	}
	return node.Key, true
}

func (t *Tree[T]) lowerBoundNode(node *Node[T], target T) *Node[T] {
	if node == t.NIL {
		return t.NIL
	}

	cmp := t.comparator(target, node.Key)
	if cmp <= 0 {
		// Target <= current key, check left subtree
		left := t.lowerBoundNode(node.Left, target)
		if left != t.NIL {
			return left
		}
		return node
	}
	// Target > current key, go right
	return t.lowerBoundNode(node.Right, target)
}

// UpperBound returns the first key > target
// Returns the key and true if found, zero value and false if not found
func (t *Tree[T]) UpperBound(target T) (T, bool) {
	node := t.upperBoundNode(t.root, target)
	if node == t.NIL {
		var zero T
		return zero, false
	}
	return node.Key, true
}

func (t *Tree[T]) upperBoundNode(node *Node[T], target T) *Node[T] {
	if node == t.NIL {
		return t.NIL
	}

	cmp := t.comparator(target, node.Key)
	if cmp < 0 {
		// Target < current key
		left := t.upperBoundNode(node.Left, target)
		if left != t.NIL {
			return left
		}
		return node
	}
	// Target >= current key, go right
	return t.upperBoundNode(node.Right, target)
}

// Count returns the number of keys in the range [start, end]
func (t *Tree[T]) Count(start, end T) int {
	return len(t.Range(start, end))
}

// String returns a string representation of the tree (in-order traversal)
func (t *Tree[T]) String() string {
	if t.IsEmpty() {
		return "[]"
	}
	return fmt.Sprintf("%v", t.InOrder())
}

// ForEach executes a function for each key in order
func (t *Tree[T]) ForEach(f func(key T) bool) {
	t.forEachInOrder(t.root, f)
}

func (t *Tree[T]) forEachInOrder(node *Node[T], f func(key T) bool) bool {
	if node == t.NIL {
		return true
	}
	if !t.forEachInOrder(node.Left, f) {
		return false
	}
	if !f(node.Key) {
		return false
	}
	return t.forEachInOrder(node.Right, f)
}

// ToSlice returns all keys as a slice (alias for InOrder)
func (t *Tree[T]) ToSlice() []T {
	return t.InOrder()
}

// FromSlice creates a tree from a slice of keys
func (t *Tree[T]) FromSlice(keys []T) int {
	count := 0
	for _, key := range keys {
		if t.Insert(key) {
			count++
		}
	}
	return count
}