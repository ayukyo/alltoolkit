//! # Weighted Random Selector
//!
//! A high-performance weighted random selector implementation using the **Alias Method**
//! (Vose's algorithm). Provides O(1) time complexity for random selection after O(n) preprocessing.
//!
//! ## Features
//!
//! - **O(1) Selection**: Constant time random selection after initial setup
//! - **Zero Dependencies**: Uses only Rust standard library
//! - **Generic Support**: Works with any type
//! - **Multiple Selection Methods**: Single, multiple, and unique selections
//! - **Interior Mutability**: Uses RefCell for safe mutation through shared references
//!
//! ## Example
//!
//! ```
//! use weighted_random::{Selector, WeightedItem};
//!
//! let items = vec![
//!     WeightedItem::new("common", 70.0),
//!     WeightedItem::new("rare", 20.0),
//!     WeightedItem::new("epic", 8.0),
//!     WeightedItem::new("legendary", 2.0),
//! ];
//!
//! let selector = Selector::new(items).unwrap();
//!
//! // Select a random item based on weights
//! let item = selector.select();
//! println!("Selected: {}", item);
//! ```

use std::cell::RefCell;
use std::collections::VecDeque;
use std::error::Error;
use std::fmt;

/// Error type for weighted random operations
#[derive(Debug, Clone, PartialEq)]
pub enum WeightedRandomError {
    /// Items list is empty
    EmptyItems,
    /// Weight is negative
    NegativeWeight,
    /// Total weight is zero
    ZeroTotalWeight,
    /// Requested more unique items than available
    TooManyUniqueItems,
}

impl fmt::Display for WeightedRandomError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            WeightedRandomError::EmptyItems => write!(f, "items cannot be empty"),
            WeightedRandomError::NegativeWeight => write!(f, "weights cannot be negative"),
            WeightedRandomError::ZeroTotalWeight => write!(f, "total weight cannot be zero"),
            WeightedRandomError::TooManyUniqueItems => {
                write!(f, "cannot select more unique items than available")
            }
        }
    }
}

impl Error for WeightedRandomError {}

/// An item with its weight for selection
#[derive(Debug, Clone, PartialEq)]
pub struct WeightedItem<T> {
    /// The item to be selected
    pub item: T,
    /// The weight (relative probability) of the item
    pub weight: f64,
}

impl<T> WeightedItem<T> {
    /// Creates a new weighted item
    pub fn new(item: T, weight: f64) -> Self {
        Self { item, weight }
    }
}

impl<T: Clone> WeightedItem<T> {
    /// Maps the item to a new type while preserving the weight
    pub fn map<U, F: Fn(T) -> U>(&self, f: F) -> WeightedItem<U> {
        WeightedItem {
            item: f(self.item.clone()),
            weight: self.weight,
        }
    }
}

/// Simple XorShift64 random number generator
#[derive(Debug, Clone)]
struct XorShift64 {
    state: u64,
}

impl XorShift64 {
    fn new() -> Self {
        use std::time::{SystemTime, UNIX_EPOCH};
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64;
        Self {
            state: if seed == 0 { 1 } else { seed },
        }
    }

    fn with_seed(seed: u64) -> Self {
        Self {
            state: if seed == 0 { 1 } else { seed },
        }
    }

    fn next_u64(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x
    }

    fn next_f64(&mut self) -> f64 {
        (self.next_u64() as f64) / (u64::MAX as f64)
    }

    fn next_usize(&mut self, bound: usize) -> usize {
        (self.next_u64() % bound as u64) as usize
    }
}

/// A weighted random selector using the Alias Method
///
/// This implementation uses Vose's Alias Method for O(1) selection.
/// Uses interior mutability via RefCell to allow selection through shared references.
#[derive(Debug)]
pub struct Selector<T> {
    items: Vec<T>,
    weights: Vec<f64>,
    prob: Vec<f64>,
    alias: Vec<usize>,
    total: f64,
    rng: RefCell<XorShift64>,
}

impl<T: Clone> Selector<T> {
    /// Creates a new selector from a vector of weighted items
    ///
    /// # Errors
    ///
    /// Returns an error if:
    /// - Items list is empty
    /// - Any weight is negative
    /// - Total weight is zero
    pub fn new(items: Vec<WeightedItem<T>>) -> Result<Self, WeightedRandomError> {
        Self::validate_items(&items)?;

        let n = items.len();
        let weights: Vec<f64> = items.iter().map(|wi| wi.weight).collect();
        let total: f64 = weights.iter().sum();

        let mut selector = Self {
            items: items.into_iter().map(|wi| wi.item).collect(),
            weights,
            prob: vec![0.0; n],
            alias: (0..n).collect(),
            total,
            rng: RefCell::new(XorShift64::new()),
        };

        selector.build_alias_method();
        Ok(selector)
    }

    /// Creates a selector with a specific seed for reproducible results
    pub fn with_seed(items: Vec<WeightedItem<T>>, seed: u64) -> Result<Self, WeightedRandomError> {
        let selector = Self::new(items)?;
        let mut result = selector;
        result.rng = RefCell::new(XorShift64::with_seed(seed));
        Ok(result)
    }

    fn validate_items(items: &[WeightedItem<T>]) -> Result<(), WeightedRandomError> {
        if items.is_empty() {
            return Err(WeightedRandomError::EmptyItems);
        }

        let mut total = 0.0;
        for wi in items {
            if wi.weight < 0.0 {
                return Err(WeightedRandomError::NegativeWeight);
            }
            total += wi.weight;
        }

        if total == 0.0 {
            return Err(WeightedRandomError::ZeroTotalWeight);
        }

        Ok(())
    }

    /// Builds the probability and alias tables using Vose's Alias Method
    fn build_alias_method(&mut self) {
        let n = self.items.len();
        if n == 0 {
            return;
        }

        if n == 1 {
            self.prob[0] = 1.0;
            self.alias[0] = 0;
            return;
        }

        // Scale weights so average is 1.0
        let avg = self.total / n as f64;
        let scaled: Vec<f64> = self.weights.iter().map(|w| w / avg).collect();

        // Partition into small and large
        let mut small: VecDeque<usize> = VecDeque::new();
        let mut large: VecDeque<usize> = VecDeque::new();

        for (i, &p) in scaled.iter().enumerate() {
            if p < 1.0 {
                small.push_back(i);
            } else {
                large.push_back(i);
            }
        }

        // Build alias tables
        while !small.is_empty() && !large.is_empty() {
            let l = small.pop_front().unwrap();
            let g = large.pop_front().unwrap();

            self.prob[l] = scaled[l];
            self.alias[l] = g;

            let new_prob = scaled[g] + scaled[l] - 1.0;
            if new_prob < 1.0 {
                small.push_back(g);
            } else {
                large.push_back(g);
            }
        }

        // Handle remaining items
        while let Some(i) = small.pop_front() {
            self.prob[i] = 1.0;
        }
        while let Some(i) = large.pop_front() {
            self.prob[i] = 1.0;
        }
    }

    /// Creates a selector from separate items and weights vectors
    pub fn from_vectors(items: Vec<T>, weights: Vec<f64>) -> Result<Self, WeightedRandomError> {
        if items.is_empty() || weights.is_empty() {
            return Err(WeightedRandomError::EmptyItems);
        }
        if items.len() != weights.len() {
            return Err(WeightedRandomError::EmptyItems);
        }

        let weighted: Vec<WeightedItem<T>> = items
            .into_iter()
            .zip(weights.into_iter())
            .map(|(item, weight)| WeightedItem::new(item, weight))
            .collect();

        Self::new(weighted)
    }

    /// Creates a selector from a slice with uniform weights
    pub fn from_slice(items: &[T]) -> Result<Self, WeightedRandomError> {
        if items.is_empty() {
            return Err(WeightedRandomError::EmptyItems);
        }

        let weighted: Vec<WeightedItem<T>> = items
            .iter()
            .map(|item| WeightedItem::new(item.clone(), 1.0))
            .collect();

        Self::new(weighted)
    }
}

impl<T> Selector<T> {
    /// Selects a random index based on weights
    ///
    /// Time complexity: O(1)
    pub fn select_index(&self) -> usize {
        let n = self.items.len();
        if n == 1 {
            return 0;
        }

        let mut rng = self.rng.borrow_mut();
        let i = rng.next_usize(n);
        let r = rng.next_f64();

        if r < self.prob[i] {
            i
        } else {
            self.alias[i]
        }
    }

    /// Selects n random indices (with replacement)
    pub fn select_indices(&self, n: usize) -> Vec<usize> {
        (0..n).map(|_| self.select_index()).collect()
    }

    /// Selects n unique random indices (without replacement)
    ///
    /// # Errors
    ///
    /// Returns an error if n > number of items
    pub fn select_unique_indices(&self, n: usize) -> Result<Vec<usize>, WeightedRandomError> {
        if n > self.items.len() {
            return Err(WeightedRandomError::TooManyUniqueItems);
        }

        let mut indices: Vec<usize> = (0..self.items.len()).collect();
        let mut result = Vec::with_capacity(n);
        let mut rng = self.rng.borrow_mut();

        for i in 0..n {
            let j = i + rng.next_usize(self.items.len() - i);
            indices.swap(i, j);
            result.push(indices[i]);
        }

        Ok(result)
    }

    /// Returns a reference to the item at the given index
    pub fn get(&self, index: usize) -> Option<&T> {
        self.items.get(index)
    }

    /// Returns a reference to the randomly selected item
    pub fn select(&self) -> &T {
        &self.items[self.select_index()]
    }

    /// Returns all items in the selector
    pub fn items(&self) -> &[T] {
        &self.items
    }

    /// Returns the weights for all items
    pub fn weights(&self) -> &[f64] {
        &self.weights
    }

    /// Returns the number of items
    pub fn len(&self) -> usize {
        self.items.len()
    }

    /// Returns true if the selector has no items
    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }

    /// Returns the total weight
    pub fn total_weight(&self) -> f64 {
        self.total
    }

    /// Returns the probability of selecting the item at index i
    pub fn probability(&self, i: usize) -> f64 {
        if i >= self.items.len() {
            return 0.0;
        }
        self.weights[i] / self.total
    }

    /// Returns a reference to the probability table
    pub fn probabilities(&self) -> &[f64] {
        &self.prob
    }

    /// Returns a reference to the alias table
    pub fn aliases(&self) -> &[usize] {
        &self.alias
    }
}

impl<T: Clone> Selector<T> {
    /// Returns a cloned copy of the randomly selected item
    pub fn select_cloned(&self) -> T {
        self.items[self.select_index()].clone()
    }

    /// Selects n random items and returns cloned values (with replacement)
    pub fn select_n_cloned(&self, n: usize) -> Vec<T> {
        (0..n).map(|_| self.select_cloned()).collect()
    }

    /// Selects n unique random items and returns cloned values (without replacement)
    pub fn select_unique_cloned(&self, n: usize) -> Result<Vec<T>, WeightedRandomError> {
        let indices = self.select_unique_indices(n)?;
        Ok(indices.iter().map(|&i| self.items[i].clone()).collect())
    }

    /// Returns a cloned vector of all items
    pub fn items_cloned(&self) -> Vec<T> {
        self.items.clone()
    }
}

impl<T: Clone> Clone for Selector<T> {
    fn clone(&self) -> Self {
        Self {
            items: self.items.clone(),
            weights: self.weights.clone(),
            prob: self.prob.clone(),
            alias: self.alias.clone(),
            total: self.total,
            rng: RefCell::new(self.rng.borrow().clone()),
        }
    }
}

/// A builder for creating selectors with custom configuration
#[derive(Debug)]
pub struct SelectorBuilder<T> {
    items: Vec<WeightedItem<T>>,
    seed: Option<u64>,
}

impl<T: Clone> SelectorBuilder<T> {
    /// Creates a new builder
    pub fn new() -> Self {
        Self {
            items: Vec::new(),
            seed: None,
        }
    }

    /// Adds an item with a weight
    pub fn add(mut self, item: T, weight: f64) -> Self {
        self.items.push(WeightedItem::new(item, weight));
        self
    }

    /// Sets a seed for reproducible results
    pub fn seed(mut self, seed: u64) -> Self {
        self.seed = Some(seed);
        self
    }

    /// Builds the selector
    pub fn build(self) -> Result<Selector<T>, WeightedRandomError> {
        if let Some(seed) = self.seed {
            Selector::with_seed(self.items, seed)
        } else {
            Selector::new(self.items)
        }
    }
}

impl<T: Clone> Default for SelectorBuilder<T> {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_selector_empty() {
        let items: Vec<WeightedItem<i32>> = vec![];
        let result = Selector::new(items);
        assert!(matches!(result, Err(WeightedRandomError::EmptyItems)));
    }

    #[test]
    fn test_new_selector_negative_weight() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", -1.0),
        ];
        let result = Selector::new(items);
        assert!(matches!(result, Err(WeightedRandomError::NegativeWeight)));
    }

    #[test]
    fn test_new_selector_zero_total() {
        let items = vec![
            WeightedItem::new("a", 0.0),
            WeightedItem::new("b", 0.0),
        ];
        let result = Selector::new(items);
        assert!(matches!(result, Err(WeightedRandomError::ZeroTotalWeight)));
    }

    #[test]
    fn test_new_selector_single_item() {
        let items = vec![WeightedItem::new("only", 10.0)];
        let selector = Selector::new(items).unwrap();
        assert_eq!(selector.len(), 1);
        assert_eq!(selector.select(), &"only");
        assert_eq!(selector.select_index(), 0);
    }

    #[test]
    fn test_new_selector_valid() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
            WeightedItem::new("c", 3.0),
        ];
        let selector = Selector::new(items).unwrap();
        assert_eq!(selector.len(), 3);
        assert_eq!(selector.total_weight(), 6.0);
    }

    #[test]
    fn test_select_n_cloned() {
        let items = vec![
            WeightedItem::new(1, 1.0),
            WeightedItem::new(2, 1.0),
            WeightedItem::new(3, 1.0),
        ];
        let selector = Selector::new(items).unwrap();
        let selected = selector.select_n_cloned(5);
        assert_eq!(selected.len(), 5);
        for &item in &selected {
            assert!(item >= 1 && item <= 3);
        }
    }

    #[test]
    fn test_select_unique_cloned() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
            WeightedItem::new("c", 3.0),
        ];
        let selector = Selector::new(items).unwrap();

        let unique = selector.select_unique_cloned(3).unwrap();
        assert_eq!(unique.len(), 3);

        // Check all items are different
        let mut seen = std::collections::HashSet::new();
        for item in unique {
            seen.insert(item);
        }
        assert_eq!(seen.len(), 3);
    }

    #[test]
    fn test_select_unique_too_many() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        let result = selector.select_unique_cloned(3);
        assert!(matches!(result, Err(WeightedRandomError::TooManyUniqueItems)));
    }

    #[test]
    fn test_builder() {
        let selector = SelectorBuilder::new()
            .add("a", 1.0)
            .add("b", 2.0)
            .add("c", 3.0)
            .build()
            .unwrap();

        assert_eq!(selector.len(), 3);
        let item = selector.select();
        assert!(*item == "a" || *item == "b" || *item == "c");
    }

    #[test]
    fn test_builder_with_seed() {
        let selector1 = SelectorBuilder::new()
            .add("a", 1.0)
            .add("b", 2.0)
            .seed(42)
            .build()
            .unwrap();

        let selector2 = SelectorBuilder::new()
            .add("a", 1.0)
            .add("b", 2.0)
            .seed(42)
            .build()
            .unwrap();

        // Same seed should produce same sequence
        for _ in 0..10 {
            assert_eq!(selector1.select_index(), selector2.select_index());
        }
    }

    #[test]
    fn test_from_slice() {
        let items = vec!["a", "b", "c"];
        let selector = Selector::from_slice(&items).unwrap();
        assert_eq!(selector.len(), 3);
    }

    #[test]
    fn test_from_slice_empty() {
        let items: Vec<i32> = vec![];
        let result = Selector::from_slice(&items);
        assert!(matches!(result, Err(WeightedRandomError::EmptyItems)));
    }

    #[test]
    fn test_from_vectors() {
        let selector = Selector::from_vectors(
            vec!["a", "b", "c"],
            vec![1.0, 2.0, 3.0],
        ).unwrap();
        assert_eq!(selector.len(), 3);
        assert_eq!(selector.total_weight(), 6.0);
    }

    #[test]
    fn test_items_accessor() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        assert_eq!(selector.items(), &["a", "b"]);
    }

    #[test]
    fn test_weights_accessor() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        assert_eq!(selector.weights(), &[1.0, 2.0]);
    }

    #[test]
    fn test_is_empty() {
        let items = vec![WeightedItem::new("a", 1.0)];
        let selector = Selector::new(items).unwrap();
        assert!(!selector.is_empty());
    }

    #[test]
    fn test_get() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        assert_eq!(selector.get(0), Some(&"a"));
        assert_eq!(selector.get(1), Some(&"b"));
        assert_eq!(selector.get(100), None);
    }

    #[test]
    fn test_probability() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        assert_eq!(selector.probability(0), 1.0 / 3.0);
        assert_eq!(selector.probability(1), 2.0 / 3.0);
        assert_eq!(selector.probability(100), 0.0);
    }

    #[test]
    fn test_clone() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        let cloned = selector.clone();
        assert_eq!(selector.len(), cloned.len());
        assert_eq!(selector.items(), cloned.items());
    }

    #[test]
    fn test_select_indices() {
        let items = vec![
            WeightedItem::new(1, 1.0),
            WeightedItem::new(2, 1.0),
            WeightedItem::new(3, 1.0),
        ];
        let selector = Selector::new(items).unwrap();
        let indices = selector.select_indices(5);
        assert_eq!(indices.len(), 5);
        for &idx in &indices {
            assert!(idx < 3);
        }
    }

    #[test]
    fn test_select_unique_indices() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
            WeightedItem::new("c", 3.0),
        ];
        let selector = Selector::new(items).unwrap();

        let indices = selector.select_unique_indices(3).unwrap();
        assert_eq!(indices.len(), 3);

        // Check all indices are different
        let mut seen = std::collections::HashSet::new();
        for idx in indices {
            seen.insert(idx);
        }
        assert_eq!(seen.len(), 3);
    }

    #[test]
    fn test_items_cloned() {
        let items = vec![
            WeightedItem::new("a", 1.0),
            WeightedItem::new("b", 2.0),
        ];
        let selector = Selector::new(items).unwrap();
        let cloned = selector.items_cloned();
        assert_eq!(cloned, vec!["a", "b"]);
    }
}