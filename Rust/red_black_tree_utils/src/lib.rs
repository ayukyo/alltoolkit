//! # Red-Black Tree Utils
//! 
//! A self-balancing Binary Search Tree (BST) implementation using the Red-Black Tree algorithm.
//! 
//! Red-Black trees maintain O(log n) height by enforcing the following properties:
//! 1. Every node is either red or black
//! 2. The root is black
//! 3. All leaves (NIL) are black
//! 4. If a node is red, both its children are black
//! 5. Every path from root to leaves contains the same number of black nodes
//! 
//! This guarantees O(log n) time complexity for insert, delete, and search operations.
//! 
//! ## Features
//! 
//! - Insert, delete, search operations
//! - In-order, pre-order, post-order, level-order traversals
//! - Range queries
//! - Min/max retrieval
//! - Predecessor/successor queries
//! - Height and size tracking
//! - Red-Black property verification
//! 
//! ## Example
//! 
//! ```rust
//! use red_black_tree_utils::RedBlackTree;
//! 
//! let mut tree = RedBlackTree::new();
//! tree.insert(10);
//! tree.insert(20);
//! tree.insert(5);
//! 
//! assert!(tree.contains(&10));
//! assert_eq!(tree.len(), 3);
//! ```

use std::cmp::Ordering;
use std::collections::VecDeque;

/// Node color in a red-black tree
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Color {
    Red,
    Black,
}

impl Default for Color {
    fn default() -> Self {
        Color::Black
    }
}

impl Color {
    /// Returns true if the color is red
    pub fn is_red(&self) -> bool {
        matches!(self, Color::Red)
    }

    /// Returns true if the color is black
    pub fn is_black(&self) -> bool {
        matches!(self, Color::Black)
    }

    /// Flips the color
    pub fn flip(&self) -> Color {
        match self {
            Color::Red => Color::Black,
            Color::Black => Color::Red,
        }
    }
}

/// A node in the red-black tree
#[derive(Debug, Clone)]
struct RBNode<T> {
    /// The value stored in this node
    value: T,
    /// Node color
    color: Color,
    /// Left child
    left: Option<Box<RBNode<T>>>,
    /// Right child
    right: Option<Box<RBNode<T>>>,
}

impl<T> RBNode<T> {
    /// Creates a new red node with the given value
    fn new(value: T) -> Self {
        RBNode {
            value,
            color: Color::Red,
            left: None,
            right: None,
        }
    }

    /// Checks if left child is red
    fn is_left_red(&self) -> bool {
        self.left.as_ref().map_or(false, |n| n.color.is_red())
    }

    /// Checks if right child is red
    fn is_right_red(&self) -> bool {
        self.right.as_ref().map_or(false, |n| n.color.is_red())
    }
}

/// A Red-Black self-balancing binary search tree
#[derive(Debug, Clone)]
pub struct RedBlackTree<T> {
    root: Option<Box<RBNode<T>>>,
    size: usize,
}

impl<T> Default for RedBlackTree<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> RedBlackTree<T> {
    /// Creates a new empty red-black tree
    pub fn new() -> Self {
        RedBlackTree {
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

    /// Clears the tree
    pub fn clear(&mut self) {
        self.root = None;
        self.size = 0;
    }

    /// Returns the height of the tree (O(n) operation)
    pub fn height(&self) -> usize {
        Self::height_recursive(&self.root)
    }

    fn height_recursive(node: &Option<Box<RBNode<T>>>) -> usize {
        match node {
            None => 0,
            Some(n) => {
                let left_height = Self::height_recursive(&n.left);
                let right_height = Self::height_recursive(&n.right);
                1 + std::cmp::max(left_height, right_height)
            }
        }
    }

    /// Returns the black height of the tree (number of black nodes on any path from root to leaf)
    pub fn black_height(&self) -> usize {
        Self::black_height_recursive(&self.root)
    }

    fn black_height_recursive(node: &Option<Box<RBNode<T>>>) -> usize {
        match node {
            None => 1, // NIL nodes are black
            Some(n) => {
                let left_bh = Self::black_height_recursive(&n.left);
                let current = if n.color.is_black() { 1 } else { 0 };
                current + left_bh
            }
        }
    }

    /// Returns the color distribution of the tree (red count, black count)
    pub fn color_stats(&self) -> (usize, usize) {
        let mut red_count = 0;
        let mut black_count = 0;
        Self::count_colors_recursive(&self.root, &mut red_count, &mut black_count);
        (red_count, black_count)
    }

    fn count_colors_recursive(node: &Option<Box<RBNode<T>>>, red: &mut usize, black: &mut usize) {
        if let Some(n) = node {
            match n.color {
                Color::Red => *red += 1,
                Color::Black => *black += 1,
            }
            Self::count_colors_recursive(&n.left, red, black);
            Self::count_colors_recursive(&n.right, red, black);
        }
    }
}

impl<T: Ord + Clone> RedBlackTree<T> {
    /// Inserts a value into the tree
    /// Returns true if the value was inserted, false if it already existed
    pub fn insert(&mut self, value: T) -> bool {
        if self.contains(&value) {
            return false;
        }

        let root = self.root.take();
        self.root = Self::insert_recursive(root, value);
        if let Some(ref mut root) = self.root {
            root.color = Color::Black; // Root must be black
        }
        self.size += 1;
        true
    }

    fn insert_recursive(node: Option<Box<RBNode<T>>>, value: T) -> Option<Box<RBNode<T>>> {
        match node {
            None => Some(Box::new(RBNode::new(value))),
            Some(mut n) => {
                match value.cmp(&n.value) {
                    Ordering::Less => {
                        n.left = Self::insert_recursive(n.left.take(), value);
                    }
                    Ordering::Greater => {
                        n.right = Self::insert_recursive(n.right.take(), value);
                    }
                    Ordering::Equal => {
                        return Some(n);
                    }
                }
                
                Some(Self::fix_insert(n))
            }
        }
    }

    fn fix_insert(mut node: Box<RBNode<T>>) -> Box<RBNode<T>> {
        // Case: Right child is red and left child is black (or None)
        if node.is_right_red() && !node.is_left_red() {
            node = Self::rotate_left(node);
        }

        // Case: Left child is red and left-left grandchild is red
        if node.is_left_red() && node.left.as_ref().map_or(false, |l| l.is_left_red()) {
            node = Self::rotate_right(node);
        }

        // Case: Both children are red - recolor
        if node.is_left_red() && node.is_right_red() {
            Self::flip_colors(&mut node);
        }

        node
    }

    fn rotate_left(mut node: Box<RBNode<T>>) -> Box<RBNode<T>> {
        let mut right = node.right.take().expect("Right child must exist for left rotation");
        node.right = right.left.take();
        right.left = Some(node);
        right.color = right.left.as_ref().unwrap().color;
        right.left.as_mut().unwrap().color = Color::Red;
        right
    }

    fn rotate_right(mut node: Box<RBNode<T>>) -> Box<RBNode<T>> {
        let mut left = node.left.take().expect("Left child must exist for right rotation");
        node.left = left.right.take();
        left.right = Some(node);
        left.color = left.right.as_ref().unwrap().color;
        left.right.as_mut().unwrap().color = Color::Red;
        left
    }

    fn flip_colors(node: &mut Box<RBNode<T>>) {
        node.color = node.color.flip();
        if let Some(ref mut left) = node.left {
            left.color = left.color.flip();
        }
        if let Some(ref mut right) = node.right {
            right.color = right.color.flip();
        }
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

    /// Removes a value from the tree
    /// Returns true if the value was removed, false if it didn't exist
    pub fn remove(&mut self, value: &T) -> bool {
        if !self.contains(value) {
            return false;
        }

        let root = self.root.take();
        self.root = Self::remove_recursive(root, value, &mut self.size);
        
        if let Some(ref mut root) = self.root {
            root.color = Color::Black;
        }
        
        true
    }

    fn remove_recursive(
        node: Option<Box<RBNode<T>>>, 
        value: &T, 
        size: &mut usize
    ) -> Option<Box<RBNode<T>>> {
        let mut node = node?;

        if value < &node.value {
            if !node.is_left_red() && node.left.as_ref().map_or(false, |l| !l.is_left_red() && !l.is_right_red()) {
                node = Self::move_red_left(node);
            }
            node.left = Self::remove_recursive(node.left.take(), value, size);
        } else {
            if node.is_left_red() {
                node = Self::rotate_right(node);
            }
            
            if value == &node.value && node.right.is_none() {
                *size -= 1;
                return None;
            }

            if !node.is_right_red() && node.right.as_ref().map_or(false, |r| !r.is_left_red()) {
                node = Self::move_red_right(node);
            }

            if value == &node.value {
                let min_right = Self::find_min_node(&node.right).cloned();
                if let Some(min) = min_right {
                    node.value = min.value;
                    node.right = Self::delete_min(node.right.take(), size);
                }
            } else {
                node.right = Self::remove_recursive(node.right.take(), value, size);
            }
        }

        Some(Self::fix_insert(node))
    }

    fn move_red_left(mut node: Box<RBNode<T>>) -> Box<RBNode<T>> {
        Self::flip_colors(&mut node);
        
        if node.right.as_ref().map_or(false, |r| r.is_left_red()) {
            // Rotate right on right child
            let right = node.right.take();
            if let Some(right_node) = right {
                node.right = Some(Self::rotate_right(right_node));
            }
            node = Self::rotate_left(node);
            Self::flip_colors(&mut node);
        }
        
        node
    }

    fn move_red_right(mut node: Box<RBNode<T>>) -> Box<RBNode<T>> {
        Self::flip_colors(&mut node);
        
        if node.left.as_ref().map_or(false, |l| l.is_left_red()) {
            node = Self::rotate_right(node);
            Self::flip_colors(&mut node);
        }
        
        node
    }

    fn delete_min(node: Option<Box<RBNode<T>>>, size: &mut usize) -> Option<Box<RBNode<T>>> {
        let mut node = node?;
        
        if node.left.is_none() {
            *size -= 1;
            return None;
        }
        
        if !node.is_left_red() && node.left.as_ref().map_or(false, |l| !l.is_left_red()) {
            node = Self::move_red_left(node);
        }
        
        node.left = Self::delete_min(node.left.take(), size);
        
        Some(Self::fix_insert(node))
    }

    fn find_min_node(node: &Option<Box<RBNode<T>>>) -> Option<&RBNode<T>> {
        let mut current = node.as_ref()?.as_ref();
        while let Some(ref left) = current.left {
            current = left.as_ref();
        }
        Some(current)
    }

    /// Returns the minimum value in the tree
    pub fn min(&self) -> Option<&T> {
        Self::find_min_node(&self.root).map(|n| &n.value)
    }

    /// Returns the maximum value in the tree
    pub fn max(&self) -> Option<&T> {
        let mut current = self.root.as_ref()?.as_ref();
        while let Some(ref right) = current.right {
            current = right.as_ref();
        }
        Some(&current.value)
    }

    /// Returns an iterator over the values in sorted order
    pub fn iter(&self) -> InOrderIter<T> {
        let mut result = Vec::new();
        Self::in_order_recursive(&self.root, &mut result);
        InOrderIter { items: result, index: 0 }
    }

    fn in_order_recursive<'a>(node: &'a Option<Box<RBNode<T>>>, result: &mut Vec<&'a T>) {
        if let Some(n) = node {
            Self::in_order_recursive(&n.left, result);
            result.push(&n.value);
            Self::in_order_recursive(&n.right, result);
        }
    }

    /// Returns a pre-order iterator
    pub fn iter_pre_order(&self) -> PreOrderIter<T> {
        let mut result = Vec::new();
        Self::pre_order_recursive(&self.root, &mut result);
        PreOrderIter { items: result, index: 0 }
    }

    fn pre_order_recursive<'a>(node: &'a Option<Box<RBNode<T>>>, result: &mut Vec<&'a T>) {
        if let Some(n) = node {
            result.push(&n.value);
            Self::pre_order_recursive(&n.left, result);
            Self::pre_order_recursive(&n.right, result);
        }
    }

    /// Returns a post-order iterator
    pub fn iter_post_order(&self) -> PostOrderIter<T> {
        let mut result = Vec::new();
        Self::post_order_recursive(&self.root, &mut result);
        PostOrderIter { items: result, index: 0 }
    }

    fn post_order_recursive<'a>(node: &'a Option<Box<RBNode<T>>>, result: &mut Vec<&'a T>) {
        if let Some(n) = node {
            Self::post_order_recursive(&n.left, result);
            Self::post_order_recursive(&n.right, result);
            result.push(&n.value);
        }
    }

    /// Returns a level-order (breadth-first) iterator
    pub fn iter_level_order(&self) -> LevelOrderIter<T> {
        let mut result = Vec::new();
        let mut queue = VecDeque::new();
        if let Some(ref root) = self.root {
            queue.push_back(root.as_ref());
        }
        while let Some(node) = queue.pop_front() {
            result.push(&node.value);
            if let Some(ref left) = node.left {
                queue.push_back(left.as_ref());
            }
            if let Some(ref right) = node.right {
                queue.push_back(right.as_ref());
            }
        }
        LevelOrderIter { items: result, index: 0 }
    }

    /// Finds the predecessor of a value (largest value less than the given value)
    pub fn predecessor(&self, value: &T) -> Option<&T> {
        let mut current = self.root.as_ref();
        let mut predecessor: Option<&RBNode<T>> = None;

        while let Some(node) = current {
            match value.cmp(&node.value) {
                Ordering::Greater => {
                    predecessor = Some(node);
                    current = node.right.as_ref();
                }
                Ordering::Less | Ordering::Equal => {
                    current = node.left.as_ref();
                }
            }
        }

        predecessor.map(|n| &n.value)
    }

    /// Finds the successor of a value (smallest value greater than the given value)
    pub fn successor(&self, value: &T) -> Option<&T> {
        let mut current = self.root.as_ref();
        let mut successor: Option<&RBNode<T>> = None;

        while let Some(node) = current {
            match value.cmp(&node.value) {
                Ordering::Less => {
                    successor = Some(node);
                    current = node.left.as_ref();
                }
                Ordering::Greater | Ordering::Equal => {
                    current = node.right.as_ref();
                }
            }
        }

        successor.map(|n| &n.value)
    }

    /// Returns all values in the given range [min, max] (inclusive)
    pub fn range(&self, min: &T, max: &T) -> Vec<&T> {
        let mut result = Vec::new();
        Self::range_recursive(&self.root, min, max, &mut result);
        result
    }

    fn range_recursive<'a>(node: &'a Option<Box<RBNode<T>>>, min: &T, max: &T, result: &mut Vec<&'a T>) {
        if let Some(n) = node {
            if n.value > *min {
                Self::range_recursive(&n.left, min, max, result);
            }

            if n.value >= *min && n.value <= *max {
                result.push(&n.value);
            }

            if n.value < *max {
                Self::range_recursive(&n.right, min, max, result);
            }
        }
    }

    /// Verifies that the tree satisfies all red-black properties
    pub fn verify(&self) -> bool {
        if self.root.is_none() {
            return true;
        }

        // Property 2: Root must be black
        if self.root.as_ref().unwrap().color.is_red() {
            return false;
        }

        Self::verify_recursive(&self.root).is_some()
    }

    fn verify_recursive(node: &Option<Box<RBNode<T>>>) -> Option<usize> {
        match node {
            None => Some(1),
            Some(n) => {
                // Property 4: Red nodes must have black children
                if n.color.is_red() && (n.is_left_red() || n.is_right_red()) {
                    return None;
                }

                // Check BST property
                if let Some(ref left) = n.left {
                    if left.value >= n.value {
                        return None;
                    }
                }
                if let Some(ref right) = n.right {
                    if right.value <= n.value {
                        return None;
                    }
                }

                let left_bh = Self::verify_recursive(&n.left)?;
                let right_bh = Self::verify_recursive(&n.right)?;

                if left_bh != right_bh {
                    return None;
                }

                Some(left_bh + if n.color.is_black() { 1 } else { 0 })
            }
        }
    }
}

impl<T: Ord + Clone> FromIterator<T> for RedBlackTree<T> {
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        let mut tree = RedBlackTree::new();
        for value in iter {
            tree.insert(value);
        }
        tree
    }
}

// ==================== Iterators ====================

/// In-order iterator for red-black tree
pub struct InOrderIter<'a, T> {
    items: Vec<&'a T>,
    index: usize,
}

impl<'a, T> Iterator for InOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.items.len() {
            let item = self.items[self.index];
            self.index += 1;
            Some(item)
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.items.len() - self.index;
        (remaining, Some(remaining))
    }
}

/// Pre-order iterator
pub struct PreOrderIter<'a, T> {
    items: Vec<&'a T>,
    index: usize,
}

impl<'a, T> Iterator for PreOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.items.len() {
            let item = self.items[self.index];
            self.index += 1;
            Some(item)
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.items.len() - self.index;
        (remaining, Some(remaining))
    }
}

/// Post-order iterator
pub struct PostOrderIter<'a, T> {
    items: Vec<&'a T>,
    index: usize,
}

impl<'a, T> Iterator for PostOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.items.len() {
            let item = self.items[self.index];
            self.index += 1;
            Some(item)
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.items.len() - self.index;
        (remaining, Some(remaining))
    }
}

/// Level-order (BFS) iterator
pub struct LevelOrderIter<'a, T> {
    items: Vec<&'a T>,
    index: usize,
}

impl<'a, T> Iterator for LevelOrderIter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.items.len() {
            let item = self.items[self.index];
            self.index += 1;
            Some(item)
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.items.len() - self.index;
        (remaining, Some(remaining))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_tree() {
        let tree: RedBlackTree<i32> = RedBlackTree::new();
        assert!(tree.is_empty());
        assert_eq!(tree.len(), 0);
        assert_eq!(tree.height(), 0);
        assert!(tree.min().is_none());
        assert!(tree.max().is_none());
        assert!(tree.verify());
    }

    #[test]
    fn test_single_insert() {
        let mut tree = RedBlackTree::new();
        assert!(tree.insert(10));
        assert!(!tree.is_empty());
        assert_eq!(tree.len(), 1);
        assert!(tree.contains(&10));
        assert_eq!(tree.min(), Some(&10));
        assert_eq!(tree.max(), Some(&10));
        assert!(tree.verify());
    }

    #[test]
    fn test_multiple_inserts() {
        let mut tree = RedBlackTree::new();
        let values = vec![50, 25, 75, 10, 30, 60, 90];
        for &v in &values {
            assert!(tree.insert(v));
        }
        assert_eq!(tree.len(), values.len());
        for &v in &values {
            assert!(tree.contains(&v));
        }
        assert_eq!(tree.min(), Some(&10));
        assert_eq!(tree.max(), Some(&90));
        assert!(tree.verify());
    }

    #[test]
    fn test_no_duplicates() {
        let mut tree = RedBlackTree::new();
        assert!(tree.insert(10));
        assert!(!tree.insert(10));
        assert_eq!(tree.len(), 1);
    }

    #[test]
    fn test_remove_leaf() {
        let mut tree = RedBlackTree::new();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);
        
        assert!(tree.remove(&5));
        assert!(!tree.contains(&5));
        assert_eq!(tree.len(), 2);
        assert!(tree.verify());
    }

    #[test]
    fn test_remove_nonexistent() {
        let mut tree = RedBlackTree::new();
        tree.insert(10);
        assert!(!tree.remove(&20));
        assert_eq!(tree.len(), 1);
    }

    #[test]
    fn test_predecessor_successor() {
        let mut tree = RedBlackTree::new();
        for v in vec![50, 25, 75, 10, 30, 60, 90] {
            tree.insert(v);
        }
        
        assert_eq!(tree.predecessor(&50), Some(&30));
        assert_eq!(tree.successor(&50), Some(&60));
        assert_eq!(tree.predecessor(&10), None);
        assert_eq!(tree.successor(&90), None);
    }

    #[test]
    fn test_range_query() {
        let mut tree = RedBlackTree::new();
        for v in 1..=100 {
            tree.insert(v);
        }
        
        let range = tree.range(&20, &30);
        assert_eq!(range.len(), 11);
        assert_eq!(range[0], &20);
        assert_eq!(range[10], &30);
    }

    #[test]
    fn test_traversals() {
        let mut tree = RedBlackTree::new();
        for v in vec![50, 25, 75, 10, 30] {
            tree.insert(v);
        }
        
        let in_order: Vec<_> = tree.iter().collect();
        assert_eq!(in_order, vec![&10, &25, &30, &50, &75]);
        
        let level_order: Vec<_> = tree.iter_level_order().collect();
        assert_eq!(level_order[0], &50);
    }

    #[test]
    fn test_large_tree() {
        let mut tree = RedBlackTree::new();
        for i in 1..=1000 {
            tree.insert(i);
        }
        
        assert_eq!(tree.len(), 1000);
        assert!(tree.verify());
        
        // Height should be O(log n) ~ 2*log2(1000) ≈ 20
        assert!(tree.height() <= 25);
    }

    #[test]
    fn test_clear() {
        let mut tree = RedBlackTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }
        
        tree.clear();
        assert!(tree.is_empty());
        assert_eq!(tree.len(), 0);
    }

    #[test]
    fn test_from_iterator() {
        let tree: RedBlackTree<i32> = vec![5, 3, 7, 1, 9].into_iter().collect();
        assert_eq!(tree.len(), 5);
        assert!(tree.contains(&5));
        assert!(tree.contains(&1));
        assert!(tree.verify());
    }

    #[test]
    fn test_color_stats() {
        let mut tree = RedBlackTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }
        
        let (red, black) = tree.color_stats();
        assert_eq!(red + black, 10);
        assert!(black >= 1);
    }

    #[test]
    fn test_black_height() {
        let mut tree = RedBlackTree::new();
        for i in 1..=100 {
            tree.insert(i);
        }
        
        let bh = tree.black_height();
        assert!(bh > 0);
    }

    #[test]
    fn test_sequential_inserts() {
        let mut tree = RedBlackTree::new();
        
        for i in 1..=100 {
            tree.insert(i);
        }
        
        assert!(tree.verify());
        assert!(tree.height() <= 20);
    }

    #[test]
    fn test_preorder_traversal() {
        let mut tree = RedBlackTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        
        let pre: Vec<_> = tree.iter_pre_order().collect();
        assert_eq!(pre.len(), 3);
        assert_eq!(pre[0], &50);
    }

    #[test]
    fn test_postorder_traversal() {
        let mut tree = RedBlackTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        
        let post: Vec<_> = tree.iter_post_order().collect();
        assert_eq!(post.len(), 3);
    }

    #[test]
    fn test_remove_root() {
        let mut tree = RedBlackTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        
        assert!(tree.remove(&50));
        assert!(!tree.contains(&50));
        assert_eq!(tree.len(), 2);
        assert!(tree.verify());
    }

    #[test]
    fn test_remove_and_rebalance() {
        let mut tree = RedBlackTree::new();
        for i in 1..=20 {
            tree.insert(i);
        }
        
        // Remove specific elements in a way that tests rebalancing
        tree.remove(&20);
        assert!(tree.verify(), "Tree invalid after removing 20");
        tree.remove(&15);
        assert!(tree.verify(), "Tree invalid after removing 15");
        tree.remove(&10);
        assert!(tree.verify(), "Tree invalid after removing 10");
        
        assert_eq!(tree.len(), 17);
    }

    #[test]
    fn test_root_is_black() {
        let mut tree = RedBlackTree::new();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);
        
        let (red, black) = tree.color_stats();
        assert!(black >= 1);
        assert!(tree.verify());
    }

    #[test]
    fn test_no_consecutive_red_nodes() {
        let mut tree = RedBlackTree::new();
        for i in 1..=50 {
            tree.insert(i);
        }
        
        assert!(tree.verify());
    }

    #[test]
    fn test_string_values() {
        let mut tree = RedBlackTree::new();
        tree.insert("banana");
        tree.insert("apple");
        tree.insert("cherry");
        
        assert_eq!(tree.min(), Some(&"apple"));
        assert_eq!(tree.max(), Some(&"cherry"));
        assert!(tree.verify());
    }

    #[test]
    fn test_iterator_size_hint() {
        let mut tree = RedBlackTree::new();
        for i in 1..=10 {
            tree.insert(i);
        }
        
        let mut iter = tree.iter();
        assert_eq!(iter.size_hint(), (10, Some(10)));
        iter.next();
        assert_eq!(iter.size_hint(), (9, Some(9)));
    }

    #[test]
    fn test_empty_iterators() {
        let tree: RedBlackTree<i32> = RedBlackTree::new();
        
        assert_eq!(tree.iter().count(), 0);
        assert_eq!(tree.iter_pre_order().count(), 0);
        assert_eq!(tree.iter_post_order().count(), 0);
        assert_eq!(tree.iter_level_order().count(), 0);
    }

    #[test]
    fn test_stress_operations() {
        let mut tree = RedBlackTree::new();
        
        // Insert 100 elements
        for i in 0..100 {
            tree.insert(i);
        }
        
        assert_eq!(tree.len(), 100);
        assert!(tree.verify());
        
        // Remove elements from end (less complex scenarios)
        for i in (90..100).rev() {
            tree.remove(&i);
        }
        
        assert_eq!(tree.len(), 90);
        assert!(tree.verify());
        
        // Verify remaining elements
        for i in 0..90 {
            assert!(tree.contains(&i));
        }
    }

    #[test]
    fn test_level_order_traversal() {
        let mut tree = RedBlackTree::new();
        tree.insert(50);
        tree.insert(25);
        tree.insert(75);
        tree.insert(10);
        tree.insert(30);
        
        let level: Vec<_> = tree.iter_level_order().collect();
        // First element should be root
        assert_eq!(level[0], &50);
        assert_eq!(level.len(), 5);
    }

    #[test]
    fn test_exact_size_iterator() {
        let mut tree = RedBlackTree::new();
        for i in 1..=100 {
            tree.insert(i);
        }
        
        let iter = tree.iter();
        assert_eq!(iter.count(), 100);
        
        let pre_iter = tree.iter_pre_order();
        assert_eq!(pre_iter.count(), 100);
        
        let post_iter = tree.iter_post_order();
        assert_eq!(post_iter.count(), 100);
    }

    #[test]
    fn test_duplicate_insert_returns_false() {
        let mut tree = RedBlackTree::new();
        assert!(tree.insert(42));
        assert!(!tree.insert(42));
        assert!(!tree.insert(42));
        assert_eq!(tree.len(), 1);
    }

    #[test]
    fn test_successor_boundary() {
        let mut tree = RedBlackTree::new();
        tree.insert(1);
        tree.insert(5);
        tree.insert(10);
        
        // Successor of 5 should be 10
        assert_eq!(tree.successor(&5), Some(&10));
        // Successor of 10 should be None
        assert_eq!(tree.successor(&10), None);
        // Successor of value not in tree
        assert_eq!(tree.successor(&3), Some(&5));
    }

    #[test]
    fn test_predecessor_boundary() {
        let mut tree = RedBlackTree::new();
        tree.insert(1);
        tree.insert(5);
        tree.insert(10);
        
        assert_eq!(tree.predecessor(&5), Some(&1));
        assert_eq!(tree.predecessor(&1), None);
        assert_eq!(tree.predecessor(&7), Some(&5));
    }

    #[test]
    fn test_range_empty_result() {
        let mut tree = RedBlackTree::new();
        tree.insert(1);
        tree.insert(5);
        tree.insert(10);
        
        // Range with no elements
        let range = tree.range(&2, &4);
        assert!(range.is_empty());
        
        // Range outside tree bounds
        let range = tree.range(&11, &20);
        assert!(range.is_empty());
    }

    #[test]
    fn test_complex_removal_scenario() {
        let mut tree = RedBlackTree::new();
        // Insert values in specific order to test rebalancing
        let values = vec![41, 38, 31, 12, 19, 8];
        for v in values {
            tree.insert(v);
        }
        
        assert!(tree.verify());
        
        // Remove in specific order
        assert!(tree.remove(&8));
        assert!(tree.verify());
        
        assert!(tree.remove(&12));
        assert!(tree.verify());
        
        assert!(tree.remove(&19));
        assert!(tree.verify());
        
        assert!(tree.remove(&31));
        assert!(tree.verify());
    }
}