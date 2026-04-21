// Package avl_tree_utils implements a self-balancing AVL Tree data structure.
// AVL Trees provide O(log n) time complexity for insert, delete, and search operations.
//
// An AVL Tree is a self-balancing binary search tree where the heights of the
// two child subtrees of any node differ by at most one. This property ensures
// that the tree remains approximately balanced at all times.
//
// Named after inventors Adelson-Velsky and Landis (1962).
// This implementation is zero-dependency and suitable for production use.
package avl_tree_utils

import "fmt"

// Node represents a node in the AVL Tree
type Node[T any] struct {
	Key    T
	Height int
	Left   *Node[T]
	Right  *Node[T]
}

// Tree represents an AVL Tree
type Tree[T any] struct {
	root       *Node[T]
	size       int
	comparator func(a, b T) int
}

// New creates a new AVL Tree with a custom comparator function.
// The comparator should return:
//   - negative if a < b
//   - zero if a == b
//   - positive if a > b
func New[T any](comparator func(a, b T) int) *Tree[T] {
	return &Tree[T]{
		root:       nil,
		size:       0,
		comparator: comparator,
	}
}

// NewInt creates a new AVL Tree for int keys with default ordering
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

// NewString creates a new AVL Tree for string keys with lexicographic ordering
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

// NewFloat64 creates a new AVL Tree for float64 keys
func NewFloat64() *Tree[float64] {
	return New(func(a, b float64) int {
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

// Root returns the root node of the tree
func (t *Tree[T]) Root() *Node[T] {
	return t.root
}

// height returns the height of a node (nil-safe)
func height[T any](node *Node[T]) int {
	if node == nil {
		return 0
	}
	return node.Height
}

// updateHeight updates the height of a node based on its children
func updateHeight[T any](node *Node[T]) {
	if node != nil {
		leftHeight := height(node.Left)
		rightHeight := height(node.Right)
		if leftHeight > rightHeight {
			node.Height = leftHeight + 1
		} else {
			node.Height = rightHeight + 1
		}
	}
}

// balanceFactor returns the balance factor of a node
// Positive = left-heavy, Negative = right-heavy
func balanceFactor[T any](node *Node[T]) int {
	if node == nil {
		return 0
	}
	return height(node.Left) - height(node.Right)
}

// rightRotate performs a right rotation at the given node
func rightRotate[T any](y *Node[T]) *Node[T] {
	x := y.Left
	T2 := x.Right

	// Perform rotation
	x.Right = y
	y.Left = T2

	// Update heights
	updateHeight(y)
	updateHeight(x)

	return x
}

// leftRotate performs a left rotation at the given node
func leftRotate[T any](x *Node[T]) *Node[T] {
	y := x.Right
	T2 := y.Left

	// Perform rotation
	y.Left = x
	x.Right = T2

	// Update heights
	updateHeight(x)
	updateHeight(y)

	return y
}

// balance performs rebalancing at the given node if necessary
func balance[T any](node *Node[T]) *Node[T] {
	if node == nil {
		return nil
	}

	updateHeight(node)
	bf := balanceFactor(node)

	// Left Left Case
	if bf > 1 && balanceFactor(node.Left) >= 0 {
		return rightRotate(node)
	}

	// Right Right Case
	if bf < -1 && balanceFactor(node.Right) <= 0 {
		return leftRotate(node)
	}

	// Left Right Case
	if bf > 1 && balanceFactor(node.Left) < 0 {
		node.Left = leftRotate(node.Left)
		return rightRotate(node)
	}

	// Right Left Case
	if bf < -1 && balanceFactor(node.Right) > 0 {
		node.Right = rightRotate(node.Right)
		return leftRotate(node)
	}

	return node
}

// Insert adds a new key to the tree
// Returns true if inserted, false if key already exists
func (t *Tree[T]) Insert(key T) bool {
	inserted := false
	t.root, inserted = t.insertNode(t.root, key)
	if inserted {
		t.size++
	}
	return inserted
}

func (t *Tree[T]) insertNode(node *Node[T], key T) (*Node[T], bool) {
	if node == nil {
		return &Node[T]{
			Key:    key,
			Height: 1,
		}, true
	}

	cmp := t.comparator(key, node.Key)
	inserted := false

	if cmp < 0 {
		node.Left, inserted = t.insertNode(node.Left, key)
	} else if cmp > 0 {
		node.Right, inserted = t.insertNode(node.Right, key)
	} else {
		// Key already exists
		return node, false
	}

	return balance(node), inserted
}

// Search finds a node with the given key
// Returns the node if found, nil otherwise
func (t *Tree[T]) Search(key T) *Node[T] {
	current := t.root

	for current != nil {
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
	if t.root == nil {
		return false
	}

	deleted := false
	t.root, deleted = t.deleteNode(t.root, key)
	if deleted {
		t.size--
	}
	return deleted
}

func (t *Tree[T]) deleteNode(node *Node[T], key T) (*Node[T], bool) {
	if node == nil {
		return nil, false
	}

	deleted := false
	cmp := t.comparator(key, node.Key)

	if cmp < 0 {
		node.Left, deleted = t.deleteNode(node.Left, key)
	} else if cmp > 0 {
		node.Right, deleted = t.deleteNode(node.Right, key)
	} else {
		// Found the node to delete
		deleted = true

		// Node with one child or no child
		if node.Left == nil {
			return node.Right, true
		} else if node.Right == nil {
			return node.Left, true
		}

		// Node with two children: Get the inorder successor
		successor := t.minNode(node.Right)
		node.Key = successor.Key
		node.Right, _ = t.deleteNode(node.Right, successor.Key)
	}

	return balance(node), deleted
}

// minNode returns the node with the minimum key in the subtree
func (t *Tree[T]) minNode(node *Node[T]) *Node[T] {
	current := node
	for current.Left != nil {
		current = current.Left
	}
	return current
}

// maxNode returns the node with the maximum key in the subtree
func (t *Tree[T]) maxNode(node *Node[T]) *Node[T] {
	current := node
	for current.Right != nil {
		current = current.Right
	}
	return current
}

// Min returns the minimum key in the tree
// Returns the key and true if found, zero value and false if tree is empty
func (t *Tree[T]) Min() (T, bool) {
	if t.IsEmpty() {
		var zero T
		return zero, false
	}
	node := t.minNode(t.root)
	return node.Key, true
}

// Max returns the maximum key in the tree
// Returns the key and true if found, zero value and false if tree is empty
func (t *Tree[T]) Max() (T, bool) {
	if t.IsEmpty() {
		var zero T
		return zero, false
	}
	node := t.maxNode(t.root)
	return node.Key, true
}

// InOrder returns all keys in ascending order
func (t *Tree[T]) InOrder() []T {
	result := make([]T, 0, t.size)
	t.inOrderWalk(t.root, &result)
	return result
}

func (t *Tree[T]) inOrderWalk(node *Node[T], result *[]T) {
	if node != nil {
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
	if node != nil {
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
	if node != nil {
		t.postOrderWalk(node.Left, result)
		t.postOrderWalk(node.Right, result)
		*result = append(*result, node.Key)
	}
}

// LevelOrder returns all keys in level-order (breadth-first)
func (t *Tree[T]) LevelOrder() []T {
	if t.root == nil {
		return []T{}
	}

	result := make([]T, 0, t.size)
	queue := []*Node[T]{t.root}

	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		result = append(result, node.Key)

		if node.Left != nil {
			queue = append(queue, node.Left)
		}
		if node.Right != nil {
			queue = append(queue, node.Right)
		}
	}

	return result
}

// Clear removes all nodes from the tree
func (t *Tree[T]) Clear() {
	t.root = nil
	t.size = 0
}

// Height returns the height of the tree
// Returns 0 for empty tree
func (t *Tree[T]) Height() int {
	return height(t.root)
}

// Validate checks if the tree satisfies all AVL Tree properties
// Returns an error if validation fails, nil otherwise
func (t *Tree[T]) Validate() error {
	if t.IsEmpty() {
		return nil
	}
	return t.validateNode(t.root)
}

func (t *Tree[T]) validateNode(node *Node[T]) error {
	if node == nil {
		return nil
	}

	// Check BST property
	if node.Left != nil {
		if t.comparator(node.Left.Key, node.Key) >= 0 {
			return fmt.Errorf("BST violation: left child %v >= parent %v", node.Left.Key, node.Key)
		}
	}
	if node.Right != nil {
		if t.comparator(node.Right.Key, node.Key) <= 0 {
			return fmt.Errorf("BST violation: right child %v <= parent %v", node.Right.Key, node.Key)
		}
	}

	// Check height consistency
	expectedHeight := 1 + max(height(node.Left), height(node.Right))
	if node.Height != expectedHeight {
		return fmt.Errorf("height inconsistency at node %v: stored=%d, expected=%d", node.Key, node.Height, expectedHeight)
	}

	// Check AVL balance property
	bf := balanceFactor(node)
	if bf < -1 || bf > 1 {
		return fmt.Errorf("AVL balance violation at node %v: balance factor=%d", node.Key, bf)
	}

	// Recursively validate children
	if err := t.validateNode(node.Left); err != nil {
		return err
	}
	return t.validateNode(node.Right)
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Range returns all keys in the range [start, end]
func (t *Tree[T]) Range(start, end T) []T {
	result := make([]T, 0)
	t.rangeWalk(t.root, start, end, &result)
	return result
}

func (t *Tree[T]) rangeWalk(node *Node[T], start, end T, result *[]T) {
	if node == nil {
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
	if node == nil {
		var zero T
		return zero, false
	}
	return node.Key, true
}

func (t *Tree[T]) lowerBoundNode(node *Node[T], target T) *Node[T] {
	if node == nil {
		return nil
	}

	cmp := t.comparator(target, node.Key)
	if cmp <= 0 {
		// Target <= current key, check left subtree
		left := t.lowerBoundNode(node.Left, target)
		if left != nil {
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
	if node == nil {
		var zero T
		return zero, false
	}
	return node.Key, true
}

func (t *Tree[T]) upperBoundNode(node *Node[T], target T) *Node[T] {
	if node == nil {
		return nil
	}

	cmp := t.comparator(target, node.Key)
	if cmp < 0 {
		// Target < current key
		left := t.upperBoundNode(node.Left, target)
		if left != nil {
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
	if node == nil {
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

// IsBalanced checks if the tree is balanced
func (t *Tree[T]) IsBalanced() bool {
	return t.isBalancedNode(t.root)
}

func (t *Tree[T]) isBalancedNode(node *Node[T]) bool {
	if node == nil {
		return true
	}

	bf := balanceFactor(node)
	if bf < -1 || bf > 1 {
		return false
	}

	return t.isBalancedNode(node.Left) && t.isBalancedNode(node.Right)
}

// GetHeight returns the height of a specific node by key
// Returns -1 if key not found
func (t *Tree[T]) GetHeight(key T) int {
	node := t.Search(key)
	if node == nil {
		return -1
	}
	return node.Height
}

// Predecessor returns the largest key less than the given key
// Returns the key and true if found, zero value and false if not found
func (t *Tree[T]) Predecessor(key T) (T, bool) {
	var result T
	found := false

	node := t.root
	for node != nil {
		cmp := t.comparator(key, node.Key)
		if cmp <= 0 {
			node = node.Left
		} else {
			result = node.Key
			found = true
			node = node.Right
		}
	}

	return result, found
}

// Successor returns the smallest key greater than the given key
// Returns the key and true if found, zero value and false if not found
func (t *Tree[T]) Successor(key T) (T, bool) {
	var result T
	found := false

	node := t.root
	for node != nil {
		cmp := t.comparator(key, node.Key)
		if cmp >= 0 {
			node = node.Right
		} else {
			result = node.Key
			found = true
			node = node.Left
		}
	}

	return result, found
}

// KthSmallest returns the k-th smallest key (1-indexed)
// Returns the key and true if found, zero value and false if k is out of range
func (t *Tree[T]) KthSmallest(k int) (T, bool) {
	if k < 1 || k > t.size {
		var zero T
		return zero, false
	}

	keys := t.InOrder()
	return keys[k-1], true
}

// KthLargest returns the k-th largest key (1-indexed)
// Returns the key and true if found, zero value and false if k is out of range
func (t *Tree[T]) KthLargest(k int) (T, bool) {
	if k < 1 || k > t.size {
		var zero T
		return zero, false
	}

	keys := t.InOrder()
	return keys[t.size-k], true
}

// Rank returns the rank of a key (1-indexed, position in sorted order)
// Returns 0 if key not found
func (t *Tree[T]) Rank(key T) int {
	keys := t.InOrder()
	for i, k := range keys {
		if t.comparator(k, key) == 0 {
			return i + 1
		}
	}
	return 0
}