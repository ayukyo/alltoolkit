//! # AVL Tree Utils
//! 
//! A self-balancing Binary Search Tree (BST) implementation using the AVL algorithm.
//! 
//! AVL trees maintain O(log n) height by ensuring the balance factor
//! (difference between left and right subtree heights) of every node
//! is at most 1. This guarantees O(log n) time complexity for insert,
//! delete, and search operations.
//! 
//! ## Features
//! 
//! - Insert, delete, search operations
//! - In-order, pre-order, post-order, level-order traversals
//! - Range queries
//! - Min/max retrieval
//! - Predecessor/successor queries
//! - Height and size tracking
//! 
//! ## Example
//! 
//! ```rust
//! use avl_tree_utils::AVLTree;
//! 
//! let mut tree = AVLTree::new();
//! tree.insert(10);
//! tree.insert(20);
//! tree.insert(5);
//! 
//! assert!(tree.contains(&10));
//! assert_eq!(tree.len(), 3);
//! ```

use std::cmp::Ordering;
use std::collections::VecDeque;

/// A node in the AVL tree
#[derive(Debug, Clone)]
struct AVLNode<T> {
    /// The value stored in this node
    value: T,
    /// Left child
    left: Option<Box<AVLNode<T>>>,
    /// Right child
    right: Option<Box<AVLNode<T>>>,
    /// Height of this node (leaf nodes have height 1)
    height: usize,
}

impl<T> AVLNode<T> {
    /// Creates a new node with the given value
    fn new(value: T) -> Self {
        AVLNode {
            value,
            left: None,
            right: None,
            height: 1,
        }
    }

    /// Returns the height of the left subtree
    fn left_height(&self) -> usize {
        self.left.as_ref().map_or(0, |n| n.height)
    }

    /// Returns the height of the right subtree
    fn right_height(&self) -> usize {
        self.right.as_ref().map_or(0, |n| n.height)
    }

    /// Updates the height of this node based on children
    fn update_height(&mut self) {
        self.height = 1 + std::cmp::max(self.left_height(), self.right_height());
    }

    /// Returns the balance factor (left_height - right_height)
    fn balance_factor(&self) -> i32 {
        self.left_height() as i32 - self.right_height() as i32
    }
}

/// An AVL self-balancing binary search tree
#[derive(Debug, Clone)]
pub struct AVLTree<T> {
    root: Option<Box<AVLNode<T>>>,
    size: usize,
}

impl<T> Default for AVLTree<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> AVLTree<T> {
    /// Creates a new empty AVL tree
    pub fn new() -> Self {
        AVLTree {
            root: None,
            size: 0,
        }
    }

    /// Returns the number of elements in the tree
    pub fn len(&self) -> usize {
        self.size
    }

    /// Returns true if the tree is empty
    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    /// Returns the height of the tree (0 if empty)
    pub fn height(&self) -> usize {
        self.root.as_ref().map_or(0, |n| n.height)
    }
}

impl<T: Ord> AVLTree<T> {
    /// Inserts a value into the tree. Returns true if the value was newly inserted.
    pub fn insert(&mut self, value: T) -> bool {
        let inserted = Self::insert_node(&mut self.root, value);
        if inserted {
            self.size += 1;
        }
        inserted
    }

    fn insert_node(node: &mut Option<Box<AVLNode<T>>>, value: T) -> bool {
        match node {
            None => {
                *node = Some(Box::new(AVLNode::new(value)));
                true
            }
            Some(n) => {
                match value.cmp(&n.value) {
                    Ordering::Less => {
                        if !Self::insert_node(&mut n.left, value) {
                            return false;
                        }
                    }
                    Ordering::Greater => {
                        if !Self::insert_node(&mut n.right, value) {
                            return false;
                        }
                    }
                    Ordering::Equal => return false, // Duplicate, not inserted
                }
                n.update_height();
                Self::balance(node);
                true
            }
        }
    }

    /// Removes a value from the tree. Returns true if the value was present.
    pub fn remove(&mut self, value: &T) -> bool {
        if Self::remove_node(&mut self.root, value) {
            self.size -= 1;
            true
        } else {
            false
        }
    }

    fn remove_node(node: &mut Option<Box<AVLNode<T>>>, value: &T) -> bool {
        match node {
            None => false,
            Some(n) => {
                match value.cmp(&n.value) {
                    Ordering::Less => {
                        if !Self::remove_node(&mut n.left, value) {
                            return false;
                        }
                    }
                    Ordering::Greater => {
                        if !Self::remove_node(&mut n.right, value) {
                            return false;
                        }
                    }
                    Ordering::Equal => {
                        // Node to delete found
                        let replacement = Self::extract_replacement(&mut n.right);
                        match replacement {
                            Some(mut repl) => {
                                repl.left = n.left.take();
                                repl.right = n.right.take();
                                repl.update_height();
                                *node = Some(repl);
                            }
                            None => {
                                // No right child, use left child
                                *node = n.left.take();
                                return true;
                            }
                        }
                    }
                }
                if let Some(n) = node {
                    n.update_height();
                    Self::balance(node);
                }
                true
            }
        }
    }

    /// Extracts the minimum node from a subtree
    fn extract_replacement(node: &mut Option<Box<AVLNode<T>>>) -> Option<Box<AVLNode<T>>> {
        match node {
            None => None,
            Some(n) if n.left.is_none() => {
                // This is the minimum node
                let mut extracted = node.take().unwrap();
                *node = extracted.right.take();
                if let Some(n) = node {
                    n.update_height();
                }
                extracted.left = None;
                extracted.right = None;
                extracted.height = 1;
                Some(extracted)
            }
            Some(_) => {
                let result = Self::extract_replacement(&mut node.as_mut().unwrap().left);
                if let Some(n) = node {
                    n.update_height();
                }
                Self::balance(node);
                result
            }
        }
    }

    /// Balances the node using rotations
    fn balance(node: &mut Option<Box<AVLNode<T>>>) {
        let balance_factor = node.as_ref().map_or(0, |n| n.balance_factor());

        if balance_factor > 1 {
            // Left heavy
            let left = node.as_mut().unwrap().left.as_mut().unwrap();
            if left.balance_factor() < 0 {
                // Left-Right case: rotate left first
                Self::rotate_left(&mut node.as_mut().unwrap().left);
            }
            // Left-Left case: rotate right
            Self::rotate_right(node);
        } else if balance_factor < -1 {
            // Right heavy
            let right = node.as_mut().unwrap().right.as_mut().unwrap();
            if right.balance_factor() > 0 {
                // Right-Left case: rotate right first
                Self::rotate_right(&mut node.as_mut().unwrap().right);
            }
            // Right-Right case: rotate left
            Self::rotate_left(node);
        }
    }

    /// Performs a right rotation
    fn rotate_right(node: &mut Option<Box<AVLNode<T>>>) {
        let mut n = node.take().unwrap();
        let mut left = n.left.take().unwrap();
        n.left = left.right.take();
        n.update_height();
        left.right = Some(n);
        left.update_height();
        *node = Some(left);
    }

    /// Performs a left rotation
    fn rotate_left(node: &mut Option<Box<AVLNode<T>>>) {
        let mut n = node.take().unwrap();
        let mut right = n.right.take().unwrap();
        n.right = right.left.take();
        n.update_height();
        right.left = Some(n);
        right.update_height();
        *node = Some(right);
    }

    /// Checks if the tree contains a value
    pub fn contains(&self, value: &T) -> bool {
        let mut current = self.root.as_ref();
        while let Some(node) = current {
            match value.cmp(&node.value) {
                Ordering::Less => current = node.left.as_ref(),
                Ordering::Greater => current = node.right.as_ref(),
                Ordering::Equal => return true,
            }
        }
        false
    }

    /// Returns a reference to the minimum value in the tree
    pub fn min(&self) -> Option<&T> {
        let mut current = self.root.as_ref()?;
        while let Some(left) = current.left.as_ref() {
            current = left;
        }
        Some(&current.value)
    }

    /// Returns a reference to the maximum value in the tree
    pub fn max(&self) -> Option<&T> {
        let mut current = self.root.as_ref()?;
        while let Some(right) = current.right.as_ref() {
            current = right;
        }
        Some(&current.value)
    }

    /// Returns an iterator over the values in in-order (sorted)
    pub fn iter(&self) -> InOrderIter<'_, T> {
        InOrderIter::new(&self.root)
    }

    /// Returns an iterator over values in pre-order
    pub fn iter_pre_order(&self) -> PreOrderIter<'_, T> {
        PreOrderIter::new(&self.root)
    }

    /// Returns an iterator over values in post-order
    pub fn iter_post_order(&self) -> PostOrderIter<'_, T> {
        PostOrderIter::new(&self.root)
    }

    /// Returns an iterator over values in level-order (BFS)
    pub fn iter_level_order(&self) -> LevelOrderIter<'_, T> {
        LevelOrderIter::new(&self.root)
    }

    /// Returns all values in the given range [min, max] in sorted order
    pub fn range(&self, min: &T, max: &T) -> Vec<&T> {
        let mut result = Vec::new();
        Self::range_helper(&self.root, min, max, &mut result);
        result
    }

    fn range_helper<'a>(
        node: &'a Option<Box<AVLNode<T>>>,
        min: &T,
        max: &T,
        result: &mut Vec<&'a T>,
    ) {
        if let Some(n) = node {
            if min < &n.value {
                Self::range_helper(&n.left, min, max, result);
            }
            if &n.value >= min && &n.value <= max {
                result.push(&n.value);
            }
            if max > &n.value {
                Self::range_helper(&n.right, min, max, result);
            }
        }
    }

    /// Returns the predecessor of the given value (largest value less than the given)
    pub fn predecessor(&self, value: &T) -> Option<&T> {
        let mut predecessor = None;
        let mut current = self.root.as_ref();
        
        while let Some(node) = current {
            match value.cmp(&node.value) {
                Ordering::Greater => {
                    predecessor = Some(&node.value);
                    current = node.right.as_ref();
                }
                Ordering::Less | Ordering::Equal => {
                    current = node.left.as_ref();
                }
            }
        }
        predecessor
    }

    /// Returns the successor of the given value (smallest value greater than the given)
    pub fn successor(&self, value: &T) -> Option<&T> {
        let mut successor = None;
        let mut current = self.root.as_ref();
        
        while let Some(node) = current {
            match value.cmp(&node.value) {
                Ordering::Less => {
                    successor = Some(&node.value);
                    current = node.left.as_ref();
                }
                Ordering::Greater | Ordering::Equal => {
                    current = node.right.as_ref();
                }
            }
        }
        successor
    }

    /// Clears all elements from the tree
    pub fn clear(&mut self) {
        self.root = None;
        self.size = 0;
    }

    /// Verifies that the tree is a valid AVL tree
    pub fn verify(&self) -> bool {
        Self::verify_node(&self.root).is_some()
    }

    fn verify_node(node: &Option<Box<AVLNode<T>>>) -> Option<usize> {
        match node {
            None => Some(0),
            Some(n) => {
                // Verify left subtree
                let left_height = Self::verify_node(&n.left)?;
                // Verify right subtree
                let right_height = Self::verify_node(&n.right)?;
                
                // Check balance factor
                let balance = left_height as i32 - right_height as i32;
                if balance.abs() > 1 {
                    return None;
                }
                
                // Check height
                let expected_height = 1 + std::cmp::max(left_height, right_height);
                if n.height != expected_height {
                    return None;
                }
                
                // Check BST property
                if let Some(left) = &n.left {
                    if left.value >= n.value {
                        return None;
                    }
                }
                if let Some(right) = &n.right {
                    if right.value <= n.value {
                        return None;
                    }
                }
                
                Some(n.height)
            }
        }
    }
}

/// In-order iterator (produces sorted output)
pub struct InOrderIter<'a, T> {
    stack: VecDeque<&'a AVLNode<T>>,
}

impl<'a, T> InOrderIter<'a, T> {
    fn new(root: &'a Option<Box<AVLNode<T>>>) -> Self {
        let mut iter = InOrderIter {
            stack: VecDeque::new(),
        };
        iter.push_left(root);
        iter
    }

    fn push_left(&mut self, mut node: &'a Option<Box<AVLNode<T>>>) {
        while let Some(n) = node {
            self.stack.push_back(n);
            node = &n.left;
        }
    }
}

impl<'a, T> Iterator for InOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        let node = self.stack.pop_back()?;
        self.push_left(&node.right);
        Some(&node.value)
    }
}

/// Pre-order iterator
pub struct PreOrderIter<'a, T> {
    stack: VecDeque<&'a AVLNode<T>>,
}

impl<'a, T> PreOrderIter<'a, T> {
    fn new(root: &'a Option<Box<AVLNode<T>>>) -> Self {
        let mut iter = PreOrderIter {
            stack: VecDeque::new(),
        };
        if let Some(n) = root {
            iter.stack.push_back(n);
        }
        iter
    }
}

impl<'a, T> Iterator for PreOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        let node = self.stack.pop_back()?;
        // Push right first, then left, so left is processed first
        if let Some(right) = node.right.as_ref() {
            self.stack.push_back(right);
        }
        if let Some(left) = node.left.as_ref() {
            self.stack.push_back(left);
        }
        Some(&node.value)
    }
}

/// Post-order iterator
pub struct PostOrderIter<'a, T> {
    stack: VecDeque<(&'a AVLNode<T>, bool)>,
}

impl<'a, T> PostOrderIter<'a, T> {
    fn new(root: &'a Option<Box<AVLNode<T>>>) -> Self {
        let mut iter = PostOrderIter {
            stack: VecDeque::new(),
        };
        if let Some(n) = root {
            iter.stack.push_back((n, false));
        }
        iter
    }
}

impl<'a, T> Iterator for PostOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        while let Some((node, visited)) = self.stack.pop_back() {
            if visited {
                return Some(&node.value);
            }
            self.stack.push_back((node, true));
            if let Some(right) = node.right.as_ref() {
                self.stack.push_back((right, false));
            }
            if let Some(left) = node.left.as_ref() {
                self.stack.push_back((left, false));
            }
        }
        None
    }
}

/// Level-order (BFS) iterator
pub struct LevelOrderIter<'a, T> {
    queue: VecDeque<&'a AVLNode<T>>,
}

impl<'a, T> LevelOrderIter<'a, T> {
    fn new(root: &'a Option<Box<AVLNode<T>>>) -> Self {
        let mut iter = LevelOrderIter {
            queue: VecDeque::new(),
        };
        if let Some(n) = root {
            iter.queue.push_back(n);
        }
        iter
    }
}

impl<'a, T> Iterator for LevelOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        let node = self.queue.pop_front()?;
        if let Some(left) = node.left.as_ref() {
            self.queue.push_back(left);
        }
        if let Some(right) = node.right.as_ref() {
            self.queue.push_back(right);
        }
        Some(&node.value)
    }
}

impl<T: Ord> FromIterator<T> for AVLTree<T> {
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        let mut tree = AVLTree::new();
        for item in iter {
            tree.insert(item);
        }
        tree
    }
}

impl<T: Ord> Extend<T> for AVLTree<T> {
    fn extend<I: IntoIterator<Item = T>>(&mut self, iter: I) {
        for item in iter {
            self.insert(item);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_tree() {
        let tree: AVLTree<i32> = AVLTree::new();
        assert!(tree.is_empty());
        assert_eq!(tree.len(), 0);
        assert_eq!(tree.height(), 0);
        assert!(!tree.contains(&1));
        assert_eq!(tree.min(), None);
        assert_eq!(tree.max(), None);
    }

    #[test]
    fn test_single_insert() {
        let mut tree = AVLTree::new();
        assert!(tree.insert(10));
        assert!(!tree.is_empty());
        assert_eq!(tree.len(), 1);
        assert_eq!(tree.height(), 1);
        assert!(tree.contains(&10));
        assert_eq!(tree.min(), Some(&10));
        assert_eq!(tree.max(), Some(&10));
    }

    #[test]
    fn test_duplicate_insert() {
        let mut tree = AVLTree::new();
        assert!(tree.insert(10));
        assert!(!tree.insert(10)); // Duplicate
        assert_eq!(tree.len(), 1);
    }

    #[test]
    fn test_sorted_insert() {
        let mut tree = AVLTree::new();
        for i in 1..=100 {
            tree.insert(i);
            assert!(tree.verify(), "Tree invalid after inserting {}", i);
        }
        assert_eq!(tree.len(), 100);
        assert!(tree.height() <= 8, "Height should be at most log2(100) + 1"); // log2(100) ≈ 6.64, + 1 for safety
    }

    #[test]
    fn test_reverse_sorted_insert() {
        let mut tree = AVLTree::new();
        for i in (1..=100).rev() {
            tree.insert(i);
            assert!(tree.verify(), "Tree invalid after inserting {}", i);
        }
        assert_eq!(tree.len(), 100);
        assert!(tree.height() <= 8);
    }

    #[test]
    fn test_remove() {
        let mut tree = AVLTree::new();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);
        
        assert!(tree.remove(&10));
        assert!(!tree.contains(&10));
        assert_eq!(tree.len(), 2);
        assert!(tree.verify());
    }

    #[test]
    fn test_remove_nonexistent() {
        let mut tree = AVLTree::new();
        tree.insert(10);
        assert!(!tree.remove(&5));
        assert_eq!(tree.len(), 1);
    }

    #[test]
    fn test_min_max() {
        let mut tree = AVLTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        tree.insert(10);
        tree.insert(90);
        
        assert_eq!(tree.min(), Some(&10));
        assert_eq!(tree.max(), Some(&90));
    }

    #[test]
    fn test_predecessor_successor() {
        let mut tree = AVLTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        tree.insert(10);
        tree.insert(30);
        tree.insert(60);
        tree.insert(90);
        
        assert_eq!(tree.predecessor(&50), Some(&30));
        assert_eq!(tree.successor(&50), Some(&60));
        assert_eq!(tree.predecessor(&10), None);
        assert_eq!(tree.successor(&90), None);
    }

    #[test]
    fn test_in_order_traversal() {
        let mut tree = AVLTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        tree.insert(10);
        tree.insert(30);
        
        let values: Vec<_> = tree.iter().collect();
        assert_eq!(values, vec![&10, &25, &30, &50, &75]);
    }

    #[test]
    fn test_pre_order_traversal() {
        let mut tree = AVLTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        
        let values: Vec<_> = tree.iter_pre_order().collect();
        assert_eq!(values.len(), 3);
        assert_eq!(values[0], &50);
    }

    #[test]
    fn test_level_order_traversal() {
        let mut tree = AVLTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        tree.insert(10);
        tree.insert(30);
        
        let values: Vec<_> = tree.iter_level_order().collect();
        assert_eq!(values[0], &50); // Root
        // Children of root
        assert!(values.contains(&&25));
        assert!(values.contains(&&75));
        // Children of 25
        assert!(values.contains(&&10));
        assert!(values.contains(&&30));
    }

    #[test]
    fn test_range_query() {
        let mut tree = AVLTree::new();
        for i in 1..=100 {
            tree.insert(i);
        }
        
        let range = tree.range(&20, &30);
        assert_eq!(range.len(), 11);
        assert_eq!(*range[0], 20);
        assert_eq!(*range[10], 30);
    }

    #[test]
    fn test_clear() {
        let mut tree = AVLTree::new();
        tree.insert(10);
        tree.insert(20);
        tree.insert(30);
        
        tree.clear();
        assert!(tree.is_empty());
        assert_eq!(tree.len(), 0);
    }

    #[test]
    fn test_from_iterator() {
        let tree: AVLTree<i32> = vec![5, 3, 7, 1, 9].into_iter().collect();
        assert_eq!(tree.len(), 5);
        assert!(tree.contains(&5));
        assert!(tree.contains(&3));
        assert!(tree.contains(&7));
        assert!(tree.contains(&1));
        assert!(tree.contains(&9));
    }

    #[test]
    fn test_balance_after_many_operations() {
        let mut tree = AVLTree::new();
        
        // Insert
        for i in 0..1000 {
            tree.insert(i);
        }
        assert!(tree.verify());
        assert!(tree.height() <= 12); // log2(1000) ≈ 10
        
        // Remove every other element
        for i in (0..1000).step_by(2) {
            tree.remove(&i);
        }
        assert!(tree.verify());
        assert_eq!(tree.len(), 500);
    }

    #[test]
    fn test_string_values() {
        let mut tree = AVLTree::new();
        tree.insert("banana");
        tree.insert("apple");
        tree.insert("cherry");
        
        let values: Vec<_> = tree.iter().collect();
        assert_eq!(values, vec![&"apple", &"banana", &"cherry"]);
    }

    #[test]
    fn test_post_order_traversal() {
        let mut tree = AVLTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        
        let values: Vec<_> = tree.iter_post_order().collect();
        // In post-order, leaves come before their parents
        assert_eq!(values.len(), 3);
        // 25 and 75 should come before 50
        let pos_50 = values.iter().position(|&v| *v == 50).unwrap();
        let pos_25 = values.iter().position(|&v| *v == 25).unwrap();
        let pos_75 = values.iter().position(|&v| *v == 75).unwrap();
        assert!(pos_25 < pos_50);
        assert!(pos_75 < pos_50);
    }
}