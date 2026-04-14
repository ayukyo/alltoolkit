//! # Priority Queue Utilities
//!
//! A comprehensive priority queue implementation for Rust.
//! Zero external dependencies - pure Rust standard library implementation.
//! Supports min-heap and max-heap with thread-safe options.
//!
//! ## Usage
//!
//! ```rust
//! use priority_queue::{MinHeap, MaxHeap, PriorityQueue};
//!
//! let mut min_heap = MinHeap::new();
//! min_heap.push("task_a", 5);
//! min_heap.push("task_b", 1);
//! min_heap.push("task_c", 3);
//!
//! // Pop returns items with lowest priority number first
//! let (val, pri) = min_heap.pop().unwrap();
//! assert_eq!(val, "task_b");
//! assert_eq!(pri, 1);
//! ```

use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::sync::RwLock;

/// Represents an item in the priority queue
#[derive(Debug, Clone)]
pub struct Item<T: Clone> {
    /// The value stored in the item
    pub value: T,
    /// The priority of the item
    pub priority: i32,
}

impl<T: Clone> Item<T> {
    /// Creates a new item with the given value and priority
    pub fn new(value: T, priority: i32) -> Self {
        Self { value, priority }
    }
}

impl<T: Clone + PartialEq> PartialEq for Item<T> {
    fn eq(&self, other: &Self) -> bool {
        self.priority == other.priority && self.value == other.value
    }
}

impl<T: Clone + Eq> Eq for Item<T> {}

/// Wrapper for max-heap ordering (higher priority = higher priority)
#[derive(Debug, Clone)]
pub struct MaxItem<T: Clone + Eq>(Item<T>);

impl<T: Clone + Eq> PartialEq for MaxItem<T> {
    fn eq(&self, other: &Self) -> bool {
        self.0.eq(&other.0)
    }
}

impl<T: Clone + Eq> Eq for MaxItem<T> {}

impl<T: Clone + Eq> Ord for MaxItem<T> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.0.priority.cmp(&other.0.priority)
    }
}

impl<T: Clone + Eq> PartialOrd for MaxItem<T> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// Wrapper for min-heap ordering (lower priority = higher priority)
#[derive(Debug, Clone)]
pub struct MinItem<T: Clone + Eq>(Item<T>);

impl<T: Clone + Eq> PartialEq for MinItem<T> {
    fn eq(&self, other: &Self) -> bool {
        self.0.eq(&other.0)
    }
}

impl<T: Clone + Eq> Eq for MinItem<T> {}

impl<T: Clone + Eq> Ord for MinItem<T> {
    fn cmp(&self, other: &Self) -> Ordering {
        // Reverse comparison for min-heap
        other.0.priority.cmp(&self.0.priority)
    }
}

impl<T: Clone + Eq> PartialOrd for MinItem<T> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// Priority queue trait defining common operations
pub trait PriorityQueue<T> {
    /// Push an item with the given priority
    fn push(&mut self, value: T, priority: i32);

    /// Pop the highest priority item
    fn pop(&mut self) -> Option<(T, i32)>;

    /// Peek at the highest priority item without removing it
    fn peek(&self) -> Option<(&T, i32)>;

    /// Check if the queue is empty
    fn is_empty(&self) -> bool;

    /// Get the number of items in the queue
    fn len(&self) -> usize;

    /// Clear all items from the queue
    fn clear(&mut self);
}

/// Max-heap priority queue (higher priority numbers are popped first)
#[derive(Debug)]
pub struct MaxHeap<T: Clone + Eq> {
    heap: BinaryHeap<MaxItem<T>>,
}

impl<T: Clone + Eq> MaxHeap<T> {
    /// Create a new empty max-heap
    pub fn new() -> Self {
        Self {
            heap: BinaryHeap::new(),
        }
    }

    /// Create a max-heap with a given capacity
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            heap: BinaryHeap::with_capacity(capacity),
        }
    }

    /// Get all items as a vector (order not guaranteed)
    pub fn to_vec(&self) -> Vec<Item<T>> {
        self.heap.iter().map(|i| i.0.clone()).collect()
    }

    /// Get all values in the queue (order not guaranteed)
    pub fn values(&self) -> Vec<T> {
        self.heap.iter().map(|i| i.0.value.clone()).collect()
    }

    /// Check if a value exists in the queue
    pub fn contains<F>(&self, predicate: F) -> bool
    where
        F: Fn(&T) -> bool,
    {
        self.heap.iter().any(|i| predicate(&i.0.value))
    }

    /// Find an item matching a predicate
    pub fn find<F>(&self, predicate: F) -> Option<&Item<T>>
    where
        F: Fn(&T) -> bool,
    {
        self.heap
            .iter()
            .find(|i| predicate(&i.0.value))
            .map(|i| &i.0)
    }

    /// Find all items with a given priority
    pub fn find_by_priority(&self, priority: i32) -> Vec<&Item<T>> {
        self.heap
            .iter()
            .filter(|i| i.0.priority == priority)
            .map(|i| &i.0)
            .collect()
    }

    /// Get the highest priority value (max priority number)
    pub fn peek_priority(&self) -> Option<i32> {
        self.heap.peek().map(|i| i.0.priority)
    }

    /// Drain all items from the queue
    pub fn drain(&mut self) -> impl Iterator<Item = (T, i32)> + '_ {
        self.heap.drain().map(|i| (i.0.value, i.0.priority))
    }
}

impl<T: Clone + Eq> Default for MaxHeap<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Clone + Eq> Clone for MaxHeap<T> {
    fn clone(&self) -> Self {
        Self {
            heap: self.heap.clone(),
        }
    }
}

impl<T: Clone + Eq> PriorityQueue<T> for MaxHeap<T> {
    fn push(&mut self, value: T, priority: i32) {
        self.heap.push(MaxItem(Item::new(value, priority)));
    }

    fn pop(&mut self) -> Option<(T, i32)> {
        self.heap.pop().map(|i| (i.0.value, i.0.priority))
    }

    fn peek(&self) -> Option<(&T, i32)> {
        self.heap.peek().map(|i| (&i.0.value, i.0.priority))
    }

    fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }

    fn len(&self) -> usize {
        self.heap.len()
    }

    fn clear(&mut self) {
        self.heap.clear();
    }
}

/// Min-heap priority queue (lower priority numbers are popped first)
#[derive(Debug)]
pub struct MinHeap<T: Clone + Eq> {
    heap: BinaryHeap<MinItem<T>>,
}

impl<T: Clone + Eq> MinHeap<T> {
    /// Create a new empty min-heap
    pub fn new() -> Self {
        Self {
            heap: BinaryHeap::new(),
        }
    }

    /// Create a min-heap with a given capacity
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            heap: BinaryHeap::with_capacity(capacity),
        }
    }

    /// Get all items as a vector (order not guaranteed)
    pub fn to_vec(&self) -> Vec<Item<T>> {
        self.heap.iter().map(|i| i.0.clone()).collect()
    }

    /// Get all values in the queue (order not guaranteed)
    pub fn values(&self) -> Vec<T> {
        self.heap.iter().map(|i| i.0.value.clone()).collect()
    }

    /// Check if a value exists in the queue
    pub fn contains<F>(&self, predicate: F) -> bool
    where
        F: Fn(&T) -> bool,
    {
        self.heap.iter().any(|i| predicate(&i.0.value))
    }

    /// Find an item matching a predicate
    pub fn find<F>(&self, predicate: F) -> Option<&Item<T>>
    where
        F: Fn(&T) -> bool,
    {
        self.heap
            .iter()
            .find(|i| predicate(&i.0.value))
            .map(|i| &i.0)
    }

    /// Find all items with a given priority
    pub fn find_by_priority(&self, priority: i32) -> Vec<&Item<T>> {
        self.heap
            .iter()
            .filter(|i| i.0.priority == priority)
            .map(|i| &i.0)
            .collect()
    }

    /// Get the highest priority value (min priority number)
    pub fn peek_priority(&self) -> Option<i32> {
        self.heap.peek().map(|i| i.0.priority)
    }

    /// Drain all items from the queue
    pub fn drain(&mut self) -> impl Iterator<Item = (T, i32)> + '_ {
        self.heap.drain().map(|i| (i.0.value, i.0.priority))
    }
}

impl<T: Clone + Eq> Default for MinHeap<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Clone + Eq> Clone for MinHeap<T> {
    fn clone(&self) -> Self {
        Self {
            heap: self.heap.clone(),
        }
    }
}

impl<T: Clone + Eq> PriorityQueue<T> for MinHeap<T> {
    fn push(&mut self, value: T, priority: i32) {
        self.heap.push(MinItem(Item::new(value, priority)));
    }

    fn pop(&mut self) -> Option<(T, i32)> {
        self.heap.pop().map(|i| (i.0.value, i.0.priority))
    }

    fn peek(&self) -> Option<(&T, i32)> {
        self.heap.peek().map(|i| (&i.0.value, i.0.priority))
    }

    fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }

    fn len(&self) -> usize {
        self.heap.len()
    }

    fn clear(&mut self) {
        self.heap.clear();
    }
}

/// Thread-safe wrapper for priority queue
#[derive(Debug)]
pub struct ThreadSafePriorityQueue<T: Clone + Eq> {
    inner: RwLock<MaxHeap<T>>,
}

impl<T: Clone + Eq> ThreadSafePriorityQueue<T> {
    /// Create a new thread-safe max-heap
    pub fn new_max() -> Self {
        Self {
            inner: RwLock::new(MaxHeap::new()),
        }
    }

    /// Create with capacity
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            inner: RwLock::new(MaxHeap::with_capacity(capacity)),
        }
    }

    /// Push an item (thread-safe)
    pub fn push(&self, value: T, priority: i32) {
        self.inner.write().unwrap().push(value, priority);
    }

    /// Pop an item (thread-safe)
    pub fn pop(&self) -> Option<(T, i32)> {
        self.inner.write().unwrap().pop()
    }

    /// Peek at the highest priority item (thread-safe)
    pub fn peek(&self) -> Option<(T, i32)> {
        self.inner
            .read()
            .unwrap()
            .peek()
            .map(|(v, p)| (v.clone(), p))
    }

    /// Check if empty (thread-safe)
    pub fn is_empty(&self) -> bool {
        self.inner.read().unwrap().is_empty()
    }

    /// Get size (thread-safe)
    pub fn len(&self) -> usize {
        self.inner.read().unwrap().len()
    }

    /// Clear (thread-safe)
    pub fn clear(&self) {
        self.inner.write().unwrap().clear();
    }

    /// Get all values (thread-safe)
    pub fn values(&self) -> Vec<T> {
        self.inner.read().unwrap().values()
    }
}

/// Thread-safe min-heap wrapper
#[derive(Debug)]
pub struct ThreadSafeMinHeap<T: Clone + Eq> {
    inner: RwLock<MinHeap<T>>,
}

impl<T: Clone + Eq> ThreadSafeMinHeap<T> {
    /// Create a new thread-safe min-heap
    pub fn new() -> Self {
        Self {
            inner: RwLock::new(MinHeap::new()),
        }
    }

    /// Push an item (thread-safe)
    pub fn push(&self, value: T, priority: i32) {
        self.inner.write().unwrap().push(value, priority);
    }

    /// Pop an item (thread-safe)
    pub fn pop(&self) -> Option<(T, i32)> {
        self.inner.write().unwrap().pop()
    }

    /// Peek at the highest priority item (thread-safe)
    pub fn peek(&self) -> Option<(T, i32)> {
        self.inner
            .read()
            .unwrap()
            .peek()
            .map(|(v, p)| (v.clone(), p))
    }

    /// Check if empty (thread-safe)
    pub fn is_empty(&self) -> bool {
        self.inner.read().unwrap().is_empty()
    }

    /// Get size (thread-safe)
    pub fn len(&self) -> usize {
        self.inner.read().unwrap().len()
    }

    /// Clear (thread-safe)
    pub fn clear(&self) {
        self.inner.write().unwrap().clear();
    }

    /// Get all values (thread-safe)
    pub fn values(&self) -> Vec<T> {
        self.inner.read().unwrap().values()
    }
}

impl<T: Clone + Eq> Default for ThreadSafeMinHeap<T> {
    fn default() -> Self {
        Self::new()
    }
}

/// Priority levels for convenience
pub struct PriorityLevel;

impl PriorityLevel {
    pub const LOWEST: i32 = 0;
    pub const LOW: i32 = 25;
    pub const NORMAL: i32 = 50;
    pub const HIGH: i32 = 75;
    pub const HIGHEST: i32 = 100;
    pub const CRITICAL: i32 = 150;

    /// Get the name of a priority level
    pub fn name(priority: i32) -> &'static str {
        match priority {
            Self::LOWEST => "Lowest",
            Self::LOW => "Low",
            Self::NORMAL => "Normal",
            Self::HIGH => "High",
            Self::HIGHEST => "Highest",
            Self::CRITICAL => "Critical",
            _ => "Custom",
        }
    }
}

/// Utility functions for working with multiple priority queues
pub fn merge_max_heaps<T: Clone + Eq>(heaps: &[&MaxHeap<T>]) -> MaxHeap<T> {
    let total_size = heaps.iter().map(|h| h.len()).sum();
    let mut merged = MaxHeap::with_capacity(total_size);

    for heap in heaps {
        for item in heap.heap.iter() {
            merged.push(item.0.value.clone(), item.0.priority);
        }
    }

    merged
}

/// Merge multiple min-heaps
pub fn merge_min_heaps<T: Clone + Eq>(heaps: &[&MinHeap<T>]) -> MinHeap<T> {
    let total_size = heaps.iter().map(|h| h.len()).sum();
    let mut merged = MinHeap::with_capacity(total_size);

    for heap in heaps {
        for item in heap.heap.iter() {
            merged.push(item.0.value.clone(), item.0.priority);
        }
    }

    merged
}

/// Sort items by priority (descending for max-heap style)
pub fn sort_by_priority_desc<T: Clone>(items: Vec<Item<T>>) -> Vec<Item<T>> {
    let mut sorted = items;
    sorted.sort_by(|a, b| b.priority.cmp(&a.priority));
    sorted
}

/// Sort items by priority (ascending for min-heap style)
pub fn sort_by_priority_asc<T: Clone>(items: Vec<Item<T>>) -> Vec<Item<T>> {
    let mut sorted = items;
    sorted.sort_by(|a, b| a.priority.cmp(&b.priority));
    sorted
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_max_heap_basic() {
        let mut heap = MaxHeap::new();
        assert!(heap.is_empty());
        assert_eq!(heap.len(), 0);

        heap.push("low", 1);
        heap.push("high", 10);
        heap.push("medium", 5);

        assert!(!heap.is_empty());
        assert_eq!(heap.len(), 3);

        // Pop should return highest priority first
        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "high");
        assert_eq!(pri, 10);

        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "medium");
        assert_eq!(pri, 5);

        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "low");
        assert_eq!(pri, 1);

        assert!(heap.pop().is_none());
    }

    #[test]
    fn test_min_heap_basic() {
        let mut heap = MinHeap::new();
        assert!(heap.is_empty());

        heap.push("low", 5);
        heap.push("high", 1);
        heap.push("medium", 3);

        // Pop should return lowest priority number first
        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "high");
        assert_eq!(pri, 1);

        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "medium");
        assert_eq!(pri, 3);

        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "low");
        assert_eq!(pri, 5);
    }

    #[test]
    fn test_peek() {
        let mut heap = MaxHeap::new();
        assert!(heap.peek().is_none());

        heap.push("first", 1);
        heap.push("second", 2);

        // Peek should not remove item
        let (val, pri) = heap.peek().unwrap();
        assert_eq!(*val, "second");
        assert_eq!(pri, 2);
        assert_eq!(heap.len(), 2);

        // Pop should return same item
        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "second");
        assert_eq!(pri, 2);
    }

    #[test]
    fn test_clear() {
        let mut heap = MaxHeap::new();
        for i in 0..10 {
            heap.push(i, i);
        }

        assert_eq!(heap.len(), 10);
        heap.clear();
        assert!(heap.is_empty());
        assert_eq!(heap.len(), 0);
    }

    #[test]
    fn test_contains_and_find() {
        let mut heap = MaxHeap::new();
        heap.push("apple", 1);
        heap.push("banana", 2);
        heap.push("cherry", 3);

        assert!(heap.contains(|v| *v == "banana"));
        assert!(!heap.contains(|v| *v == "orange"));

        let found = heap.find(|v| *v == "apple");
        assert!(found.is_some());
        assert_eq!(found.unwrap().priority, 1);

        let not_found = heap.find(|v| *v == "orange");
        assert!(not_found.is_none());
    }

    #[test]
    fn test_find_by_priority() {
        let mut heap = MinHeap::new();
        heap.push("a", 1);
        heap.push("b", 2);
        heap.push("c", 1);
        heap.push("d", 3);

        let items = heap.find_by_priority(1);
        assert_eq!(items.len(), 2);
    }

    #[test]
    fn test_to_vec_and_values() {
        let mut heap = MaxHeap::new();
        heap.push(10, 1);
        heap.push(20, 2);
        heap.push(30, 3);

        let values = heap.values();
        assert_eq!(values.len(), 3);

        let items = heap.to_vec();
        assert_eq!(items.len(), 3);
    }

    #[test]
    fn test_clone() {
        let mut original = MinHeap::new();
        original.push(1, 10);
        original.push(2, 20);

        let cloned = original.clone();
        original.pop();

        assert_eq!(original.len(), 1);
        assert_eq!(cloned.len(), 2);
    }

    #[test]
    fn test_thread_safe() {
        let heap = ThreadSafePriorityQueue::new_max();
        heap.push("a", 1);
        heap.push("b", 2);
        heap.push("c", 3);

        assert_eq!(heap.len(), 3);
        assert!(!heap.is_empty());

        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "c");
        assert_eq!(pri, 3);

        heap.clear();
        assert!(heap.is_empty());
    }

    #[test]
    fn test_thread_safe_min_heap() {
        let heap = ThreadSafeMinHeap::new();
        heap.push("a", 5);
        heap.push("b", 1);
        heap.push("c", 3);

        let (val, pri) = heap.pop().unwrap();
        assert_eq!(val, "b");
        assert_eq!(pri, 1);
    }

    #[test]
    fn test_priority_level() {
        assert_eq!(PriorityLevel::name(PriorityLevel::LOWEST), "Lowest");
        assert_eq!(PriorityLevel::name(PriorityLevel::NORMAL), "Normal");
        assert_eq!(PriorityLevel::name(PriorityLevel::HIGH), "High");
        assert_eq!(PriorityLevel::name(PriorityLevel::CRITICAL), "Critical");
        assert_eq!(PriorityLevel::name(999), "Custom");
    }

    #[test]
    fn test_with_capacity() {
        let mut heap: MaxHeap<i32> = MaxHeap::with_capacity(100);
        for i in 0..50 {
            heap.push(i, i);
        }
        assert_eq!(heap.len(), 50);
    }

    #[test]
    fn test_drain() {
        let mut heap = MaxHeap::new();
        heap.push(1, 10);
        heap.push(2, 20);
        heap.push(3, 30);

        let items: Vec<_> = heap.drain().collect();
        assert_eq!(items.len(), 3);
        assert!(heap.is_empty());
    }

    #[test]
    fn test_merge_heaps() {
        let mut heap1 = MaxHeap::new();
        heap1.push("a", 10);
        heap1.push("b", 20);

        let mut heap2 = MaxHeap::new();
        heap2.push("c", 30);
        heap2.push("d", 40);

        let mut merged = merge_max_heaps(&[&heap1, &heap2]);
        assert_eq!(merged.len(), 4);

        let (val, pri) = merged.pop().unwrap();
        assert_eq!(pri, 40);
        assert_eq!(val, "d");
    }

    #[test]
    fn test_sort_by_priority() {
        let items = vec![Item::new("a", 30), Item::new("b", 10), Item::new("c", 20)];

        let sorted_desc = sort_by_priority_desc(items.clone());
        assert_eq!(sorted_desc[0].priority, 30);
        assert_eq!(sorted_desc[2].priority, 10);

        let sorted_asc = sort_by_priority_asc(items);
        assert_eq!(sorted_asc[0].priority, 10);
        assert_eq!(sorted_asc[2].priority, 30);
    }

    #[test]
    fn test_item_new() {
        let item = Item::new("test", 42);
        assert_eq!(item.value, "test");
        assert_eq!(item.priority, 42);
    }

    #[test]
    fn test_default() {
        let heap: MaxHeap<i32> = MaxHeap::default();
        assert!(heap.is_empty());

        let min_heap: MinHeap<i32> = MinHeap::default();
        assert!(min_heap.is_empty());
    }

    #[test]
    fn test_generic_types() {
        // Test with different types
        let mut int_heap = MaxHeap::new();
        int_heap.push(42, 1);
        assert_eq!(int_heap.pop().unwrap().0, 42);

        let mut vec_heap = MinHeap::new();
        vec_heap.push(vec![1, 2, 3], 5);
        vec_heap.push(vec![4, 5, 6], 1);
        assert_eq!(vec_heap.pop().unwrap().0, vec![4, 5, 6]);
    }
}
