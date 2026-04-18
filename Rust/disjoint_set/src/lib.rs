//! Disjoint Set (Union-Find) Data Structure
//!
//! A high-performance implementation of the disjoint-set data structure with
//! path compression and union by rank/size optimizations.
//!
//! # Features
//!
//! - Path compression for near O(1) amortized operations
//! - Union by rank or union by size strategies
//! - Connected components tracking
//! - Set size queries
//! - Element iteration within sets
//! - Batch operations support
//!
//! # Examples
//!
//! ```
//! use disjoint_set::DisjointSet;
//!
//! let mut ds = DisjointSet::new(5);
//! ds.union(0, 1);
//! ds.union(2, 3);
//! assert!(ds.connected(0, 1));
//! assert!(!ds.connected(1, 2));
//! assert_eq!(ds.set_count(), 3); // Sets: {0,1}, {2,3}, {4}
//! ```

use std::collections::{HashMap, HashSet};

/// Union strategy for the DisjointSet
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UnionStrategy {
    /// Union by rank - uses tree height for balancing
    ByRank,
    /// Union by size - uses tree size for balancing
    BySize,
}

impl Default for UnionStrategy {
    fn default() -> Self {
        UnionStrategy::ByRank
    }
}

/// A disjoint-set (union-find) data structure.
///
/// This implementation uses path compression and union by rank/size
/// to achieve near O(α(n)) amortized time complexity, where α is the
/// inverse Ackermann function.
#[derive(Debug, Clone)]
pub struct DisjointSet {
    /// Parent pointers for each element
    parent: Vec<usize>,
    /// Rank (approximate height) of each tree
    rank: Vec<usize>,
    /// Size of each set (only valid for roots)
    size: Vec<usize>,
    /// Number of elements
    count: usize,
    /// Number of disjoint sets
    set_count: usize,
    /// Union strategy
    strategy: UnionStrategy,
}

impl DisjointSet {
    /// Creates a new DisjointSet with `n` elements (0 to n-1).
    ///
    /// Initially, each element is in its own set.
    ///
    /// # Arguments
    ///
    /// * `n` - The number of elements.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let ds = DisjointSet::new(5);
    /// assert_eq!(ds.len(), 5);
    /// assert_eq!(ds.set_count(), 5);
    /// ```
    pub fn new(n: usize) -> Self {
        Self::with_strategy(n, UnionStrategy::ByRank)
    }

    /// Creates a new DisjointSet with a specific union strategy.
    ///
    /// # Arguments
    ///
    /// * `n` - The number of elements.
    /// * `strategy` - The union strategy (ByRank or BySize).
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::{DisjointSet, UnionStrategy};
    ///
    /// let ds = DisjointSet::with_strategy(5, UnionStrategy::BySize);
    /// assert_eq!(ds.strategy(), UnionStrategy::BySize);
    /// ```
    pub fn with_strategy(n: usize, strategy: UnionStrategy) -> Self {
        Self {
            parent: (0..n).collect(),
            rank: vec![0; n],
            size: vec![1; n],
            count: n,
            set_count: n,
            strategy,
        }
    }

    /// Creates a new DisjointSet from an iterator of edges.
    ///
    /// # Arguments
    ///
    /// * `n` - The number of elements.
    /// * `edges` - An iterator of (u, v) pairs to union.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let edges = vec![(0, 1), (2, 3), (1, 2)];
    /// let mut ds = DisjointSet::from_edges(5, edges);
    /// assert!(ds.connected(0, 3));
    /// assert!(!ds.connected(0, 4));
    /// ```
    pub fn from_edges<I>(n: usize, edges: I) -> Self
    where
        I: IntoIterator<Item = (usize, usize)>,
    {
        let mut ds = Self::new(n);
        for (u, v) in edges {
            if u < n && v < n {
                ds.union(u, v);
            }
        }
        ds
    }

    /// Returns the number of elements in the DisjointSet.
    pub fn len(&self) -> usize {
        self.count
    }

    /// Returns true if the DisjointSet has no elements.
    pub fn is_empty(&self) -> bool {
        self.count == 0
    }

    /// Returns the number of disjoint sets.
    pub fn set_count(&self) -> usize {
        self.set_count
    }

    /// Returns the current union strategy.
    pub fn strategy(&self) -> UnionStrategy {
        self.strategy
    }

    /// Finds the root (representative) of the set containing `x`.
    ///
    /// Uses path compression for optimization.
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()`.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(3);
    /// ds.union(0, 1);
    /// assert_eq!(ds.find(0), ds.find(1));
    /// ```
    pub fn find(&mut self, x: usize) -> usize {
        assert!(x < self.count, "Index out of bounds");
        
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]); // Path compression
        }
        self.parent[x]
    }

    /// Finds the root without path compression (read-only).
    ///
    /// Useful when you need to inspect the structure without modifying it.
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()`.
    pub fn find_no_compress(&self, mut x: usize) -> usize {
        assert!(x < self.count, "Index out of bounds");
        
        while self.parent[x] != x {
            x = self.parent[x];
        }
        x
    }

    /// Checks if elements `x` and `y` are in the same set.
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()` or `y >= self.len()`.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(3);
    /// assert!(!ds.connected(0, 1));
    /// ds.union(0, 1);
    /// assert!(ds.connected(0, 1));
    /// ```
    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }

    /// Checks if elements `x` and `y` are in the same set without path compression.
    pub fn connected_no_compress(&self, x: usize, y: usize) -> bool {
        self.find_no_compress(x) == self.find_no_compress(y)
    }

    /// Unions the sets containing elements `x` and `y`.
    ///
    /// Returns `true` if the sets were different (a union was performed),
    /// `false` if they were already in the same set.
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()` or `y >= self.len()`.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(3);
    /// assert!(ds.union(0, 1));  // Returns true (merged)
    /// assert!(!ds.union(0, 1)); // Returns false (already same set)
    /// ```
    pub fn union(&mut self, x: usize, y: usize) -> bool {
        let root_x = self.find(x);
        let root_y = self.find(y);
        
        if root_x == root_y {
            return false;
        }
        
        match self.strategy {
            UnionStrategy::ByRank => self.union_by_rank(root_x, root_y),
            UnionStrategy::BySize => self.union_by_size(root_x, root_y),
        }
        
        self.set_count -= 1;
        true
    }

    fn union_by_rank(&mut self, root_x: usize, root_y: usize) {
        if self.rank[root_x] < self.rank[root_y] {
            self.parent[root_x] = root_y;
            self.size[root_y] += self.size[root_x];
        } else if self.rank[root_x] > self.rank[root_y] {
            self.parent[root_y] = root_x;
            self.size[root_x] += self.size[root_y];
        } else {
            self.parent[root_y] = root_x;
            self.rank[root_x] += 1;
            self.size[root_x] += self.size[root_y];
        }
    }

    fn union_by_size(&mut self, root_x: usize, root_y: usize) {
        if self.size[root_x] < self.size[root_y] {
            self.parent[root_x] = root_y;
            self.size[root_y] += self.size[root_x];
        } else {
            self.parent[root_y] = root_x;
            self.size[root_x] += self.size[root_y];
        }
    }

    /// Returns the size of the set containing `x`.
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()`.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(5);
    /// ds.union(0, 1);
    /// ds.union(2, 3);
    /// assert_eq!(ds.set_size(0), 2);
    /// assert_eq!(ds.set_size(2), 2);
    /// assert_eq!(ds.set_size(4), 1);
    /// ```
    pub fn set_size(&mut self, x: usize) -> usize {
        let root = self.find(x);
        self.size[root]
    }

    /// Returns the rank of the tree containing `x` (only meaningful for roots).
    pub fn rank(&mut self, x: usize) -> usize {
        let root = self.find(x);
        self.rank[root]
    }

    /// Returns all elements in the same set as `x`.
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()`.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(5);
    /// ds.union(0, 1);
    /// ds.union(1, 2);
    /// let set = ds.elements_in_set(0);
    /// assert_eq!(set.len(), 3);
    /// assert!(set.contains(&0) && set.contains(&1) && set.contains(&2));
    /// ```
    pub fn elements_in_set(&mut self, x: usize) -> HashSet<usize> {
        let root = self.find(x);
        self.elements_in_set_of_root(root)
    }

    fn elements_in_set_of_root(&self, root: usize) -> HashSet<usize> {
        let mut result = HashSet::new();
        for i in 0..self.count {
            if self.find_no_compress(i) == root {
                result.insert(i);
            }
        }
        result
    }

    /// Returns all disjoint sets as a vector of sets.
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(5);
    /// ds.union(0, 1);
    /// ds.union(2, 3);
    /// let sets = ds.all_sets();
    /// assert_eq!(sets.len(), 3);
    /// ```
    pub fn all_sets(&mut self) -> Vec<HashSet<usize>> {
        // Compress all paths first
        for i in 0..self.count {
            self.find(i);
        }
        
        let mut sets: HashMap<usize, HashSet<usize>> = HashMap::new();
        for i in 0..self.count {
            let root = self.parent[i];
            sets.entry(root).or_default().insert(i);
        }
        sets.into_values().collect()
    }

    /// Returns the root of each element (representative mapping).
    pub fn root_mapping(&mut self) -> Vec<usize> {
        for i in 0..self.count {
            self.find(i);
        }
        self.parent.clone()
    }

    /// Resets the DisjointSet to initial state (each element in its own set).
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(3);
    /// ds.union(0, 1);
    /// assert_eq!(ds.set_count(), 2);
    /// ds.reset();
    /// assert_eq!(ds.set_count(), 3);
    /// ```
    pub fn reset(&mut self) {
        for i in 0..self.count {
            self.parent[i] = i;
            self.rank[i] = 0;
            self.size[i] = 1;
        }
        self.set_count = self.count;
    }

    /// Performs multiple unions at once.
    ///
    /// # Arguments
    ///
    /// * `pairs` - Iterator of (u, v) pairs to union.
    ///
    /// # Returns
    ///
    /// The number of successful unions (pairs that were in different sets).
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(5);
    /// let merged = ds.batch_union(vec![(0, 1), (2, 3), (1, 2), (0, 1)]);
    /// assert_eq!(merged, 3); // Last (0,1) was already merged
    /// assert_eq!(ds.set_count(), 2); // {0,1,2,3} and {4}
    /// ```
    pub fn batch_union<I>(&mut self, pairs: I) -> usize
    where
        I: IntoIterator<Item = (usize, usize)>,
    {
        let mut count = 0;
        for (u, v) in pairs {
            if self.union(u, v) {
                count += 1;
            }
        }
        count
    }

    /// Checks if the element `x` is a root (representative of its set).
    ///
    /// # Panics
    ///
    /// Panics if `x >= self.len()`.
    pub fn is_root(&self, x: usize) -> bool {
        assert!(x < self.count, "Index out of bounds");
        self.parent[x] == x
    }

    /// Returns all root elements (representatives of each set).
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(5);
    /// ds.union(0, 1);
    /// ds.union(2, 3);
    /// let roots = ds.roots();
    /// assert_eq!(roots.len(), 3); // 3 sets
    /// ```
    pub fn roots(&self) -> HashSet<usize> {
        let mut roots = HashSet::new();
        for i in 0..self.count {
            if self.parent[i] == i {
                roots.insert(i);
            }
        }
        roots
    }

    /// Finds all isolated elements (elements in sets of size 1).
    ///
    /// # Examples
    ///
    /// ```
    /// use disjoint_set::DisjointSet;
    ///
    /// let mut ds = DisjointSet::new(5);
    /// ds.union(0, 1);
    /// ds.union(2, 3);
    /// let isolated = ds.isolated_elements();
    /// assert_eq!(isolated, vec![4]);
    /// ```
    pub fn isolated_elements(&self) -> Vec<usize> {
        let mut isolated = Vec::new();
        for i in 0..self.count {
            if self.parent[i] == i && self.size[i] == 1 {
                isolated.push(i);
            }
        }
        isolated
    }

    /// Returns the largest set size.
    pub fn largest_set_size(&self) -> usize {
        self.size.iter().max().copied().unwrap_or(0)
    }

    /// Returns the size of the smallest non-trivial set (size > 1).
    /// Returns None if no non-trivial sets exist.
    pub fn smallest_non_trivial_set_size(&self) -> Option<usize> {
        self.size.iter()
            .enumerate()
            .filter(|&(i, &s)| self.parent[i] == i && s > 1)
            .map(|(_, &s)| s)
            .min()
    }

    /// Counts the number of non-trivial sets (sets with more than one element).
    pub fn non_trivial_set_count(&self) -> usize {
        self.size.iter()
            .enumerate()
            .filter(|&(i, &s)| self.parent[i] == i && s > 1)
            .count()
    }
}

/// A labeled disjoint set that supports arbitrary element types.
///
/// This is useful when you want to use strings or other types as elements
/// instead of numeric indices.
#[derive(Debug, Clone)]
pub struct LabeledDisjointSet<T>
where
    T: Eq + std::hash::Hash + Clone,
{
    /// The underlying DisjointSet
    ds: DisjointSet,
    /// Mapping from labels to indices
    label_to_index: HashMap<T, usize>,
    /// Mapping from indices to labels
    index_to_label: Vec<T>,
}

impl<T> LabeledDisjointSet<T>
where
    T: Eq + std::hash::Hash + Clone,
{
    /// Creates a new empty LabeledDisjointSet.
    pub fn new() -> Self {
        Self {
            ds: DisjointSet::new(0),
            label_to_index: HashMap::new(),
            index_to_label: Vec::new(),
        }
    }

    /// Creates a LabeledDisjointSet from an iterator of elements.
    pub fn from_elements<I>(elements: I) -> Self
    where
        I: IntoIterator<Item = T>,
    {
        let mut set = Self::new();
        for elem in elements {
            set.add_element(elem);
        }
        set
    }

    /// Adds a new element to the set.
    /// Returns the index assigned to this element.
    pub fn add_element(&mut self, label: T) -> usize {
        if let Some(&index) = self.label_to_index.get(&label) {
            return index;
        }
        
        let index = self.index_to_label.len();
        self.label_to_index.insert(label.clone(), index);
        self.index_to_label.push(label);
        
        // Extend the underlying DisjointSet
        self.ds.parent.push(index);
        self.ds.rank.push(0);
        self.ds.size.push(1);
        self.ds.count += 1;
        self.ds.set_count += 1;
        
        index
    }

    /// Returns the number of elements.
    pub fn len(&self) -> usize {
        self.ds.len()
    }

    /// Returns true if there are no elements.
    pub fn is_empty(&self) -> bool {
        self.ds.is_empty()
    }

    /// Returns the number of disjoint sets.
    pub fn set_count(&self) -> usize {
        self.ds.set_count()
    }

    /// Checks if two elements are in the same set.
    pub fn connected(&mut self, a: &T, b: &T) -> bool {
        if let (Some(&i), Some(&j)) = (self.label_to_index.get(a), self.label_to_index.get(b)) {
            self.ds.connected(i, j)
        } else {
            false
        }
    }

    /// Unions the sets containing two elements.
    /// Returns true if they were in different sets.
    pub fn union(&mut self, a: &T, b: &T) -> bool {
        let i = self.label_to_index.get(a).copied().unwrap_or_else(|| self.add_element(a.clone()));
        let j = self.label_to_index.get(b).copied().unwrap_or_else(|| self.add_element(b.clone()));
        self.ds.union(i, j)
    }

    /// Returns the size of the set containing an element.
    pub fn set_size(&mut self, label: &T) -> Option<usize> {
        self.label_to_index.get(label).map(|&i| self.ds.set_size(i))
    }

    /// Returns all elements in the same set as the given element.
    pub fn elements_in_set(&mut self, label: &T) -> Option<HashSet<T>> {
        self.label_to_index.get(label).map(|&i| {
            self.ds.elements_in_set(i)
                .into_iter()
                .map(|idx| self.index_to_label[idx].clone())
                .collect()
        })
    }

    /// Returns all disjoint sets.
    pub fn all_sets(&mut self) -> Vec<HashSet<T>> {
        self.ds.all_sets()
            .into_iter()
            .map(|set| {
                set.into_iter()
                    .map(|idx| self.index_to_label[idx].clone())
                    .collect()
            })
            .collect()
    }

    /// Resets to initial state.
    pub fn reset(&mut self) {
        self.ds.reset();
    }
}

impl<T> Default for LabeledDisjointSet<T>
where
    T: Eq + std::hash::Hash + Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

/// Creates a DisjointSet from a number of connected components.
///
/// # Arguments
///
/// * `n` - Total number of elements.
/// * `components` - A vector of vectors, where each inner vector contains
///   elements that should be in the same set.
///
/// # Examples
///
/// ```
/// use disjoint_set::DisjointSet;
///
/// let components = vec![vec![0, 1, 2], vec![3, 4]];
/// let mut ds = DisjointSet::from_components(6, &components);
/// assert!(ds.connected(0, 2));
/// assert!(ds.connected(3, 4));
/// assert!(!ds.connected(0, 3));
/// assert!(!ds.connected(0, 5));
/// ```
impl DisjointSet {
    pub fn from_components(n: usize, components: &[Vec<usize>]) -> Self {
        let mut ds = Self::new(n);
        for component in components {
            if component.len() > 1 {
                let first = component[0];
                for &elem in &component[1..] {
                    ds.union(first, elem);
                }
            }
        }
        ds
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        let ds = DisjointSet::new(5);
        assert_eq!(ds.len(), 5);
        assert_eq!(ds.set_count(), 5);
        assert!(ds.is_empty() == false);
    }

    #[test]
    fn test_empty() {
        let ds = DisjointSet::new(0);
        assert_eq!(ds.len(), 0);
        assert!(ds.is_empty());
        assert_eq!(ds.set_count(), 0);
    }

    #[test]
    fn test_union_find() {
        let mut ds = DisjointSet::new(5);
        
        assert!(!ds.connected(0, 1));
        assert!(ds.union(0, 1));
        assert!(ds.connected(0, 1));
        assert!(!ds.union(0, 1)); // Already connected
        assert_eq!(ds.set_count(), 4);
    }

    #[test]
    fn test_transitivity() {
        let mut ds = DisjointSet::new(5);
        
        ds.union(0, 1);
        ds.union(1, 2);
        ds.union(2, 3);
        
        assert!(ds.connected(0, 3));
        assert!(ds.connected(1, 3));
        assert!(!ds.connected(0, 4));
    }

    #[test]
    fn test_set_size() {
        let mut ds = DisjointSet::new(5);
        
        assert_eq!(ds.set_size(0), 1);
        
        ds.union(0, 1);
        assert_eq!(ds.set_size(0), 2);
        assert_eq!(ds.set_size(1), 2);
        
        ds.union(2, 3);
        ds.union(0, 2);
        
        assert_eq!(ds.set_size(0), 4);
        assert_eq!(ds.set_size(4), 1);
    }

    #[test]
    fn test_reset() {
        let mut ds = DisjointSet::new(5);
        
        ds.union(0, 1);
        ds.union(2, 3);
        assert_eq!(ds.set_count(), 3);
        
        ds.reset();
        assert_eq!(ds.set_count(), 5);
        assert!(!ds.connected(0, 1));
    }

    #[test]
    fn test_all_sets() {
        let mut ds = DisjointSet::new(5);
        
        ds.union(0, 1);
        ds.union(2, 3);
        
        let sets = ds.all_sets();
        assert_eq!(sets.len(), 3);
        
        // Check that sets contain the right elements
        let total_elements: usize = sets.iter().map(|s| s.len()).sum();
        assert_eq!(total_elements, 5);
    }

    #[test]
    fn test_elements_in_set() {
        let mut ds = DisjointSet::new(5);
        
        ds.union(0, 1);
        ds.union(1, 2);
        
        let set = ds.elements_in_set(0);
        assert_eq!(set.len(), 3);
        assert!(set.contains(&0));
        assert!(set.contains(&1));
        assert!(set.contains(&2));
        assert!(!set.contains(&3));
    }

    #[test]
    fn test_from_edges() {
        let edges = vec![(0, 1), (2, 3), (1, 2)];
        let mut ds = DisjointSet::from_edges(5, edges);
        
        assert!(ds.connected(0, 3));
        assert!(!ds.connected(0, 4));
        assert_eq!(ds.set_count(), 2);
    }

    #[test]
    fn test_batch_union() {
        let mut ds = DisjointSet::new(5);
        
        let merged = ds.batch_union(vec![(0, 1), (2, 3), (1, 2), (0, 1)]);
        assert_eq!(merged, 3); // Last (0,1) was already merged
        assert_eq!(ds.set_count(), 2);
    }

    #[test]
    fn test_union_strategies() {
        let mut ds_rank = DisjointSet::with_strategy(10, UnionStrategy::ByRank);
        let mut ds_size = DisjointSet::with_strategy(10, UnionStrategy::BySize);
        
        for i in 0..9 {
            ds_rank.union(i, i + 1);
            ds_size.union(i, i + 1);
        }
        
        assert!(ds_rank.connected(0, 9));
        assert!(ds_size.connected(0, 9));
        assert_eq!(ds_rank.set_count(), 1);
        assert_eq!(ds_size.set_count(), 1);
    }

    #[test]
    fn test_labeled_disjoint_set() {
        let mut ds: LabeledDisjointSet<String> = LabeledDisjointSet::new();
        
        ds.union(&"a".to_string(), &"b".to_string());
        ds.union(&"b".to_string(), &"c".to_string());
        
        assert!(ds.connected(&"a".to_string(), &"c".to_string()));
        assert_eq!(ds.set_size(&"a".to_string()), Some(3));
        
        let set = ds.elements_in_set(&"a".to_string()).unwrap();
        assert_eq!(set.len(), 3);
    }

    #[test]
    fn test_labeled_from_elements() {
        let mut ds = LabeledDisjointSet::from_elements(vec!["a", "b", "c", "d"]);
        
        ds.union(&"a", &"b");
        ds.union(&"c", &"d");
        
        assert_eq!(ds.set_count(), 2);
    }

    #[test]
    fn test_isolated_elements() {
        let mut ds = DisjointSet::new(5);
        
        ds.union(0, 1);
        ds.union(2, 3);
        
        let isolated = ds.isolated_elements();
        assert_eq!(isolated, vec![4]);
    }

    #[test]
    fn test_roots() {
        let mut ds = DisjointSet::new(5);
        
        ds.union(0, 1);
        ds.union(2, 3);
        
        let roots = ds.roots();
        assert_eq!(roots.len(), 3);
    }

    #[test]
    fn test_from_components() {
        let mut ds = DisjointSet::from_components(6, &vec![vec![0, 1, 2], vec![3, 4]]);
        
        assert!(ds.connected(0, 2));
        assert!(ds.connected(3, 4));
        assert!(!ds.connected(0, 3));
        assert!(!ds.connected(0, 5));
        assert_eq!(ds.set_count(), 3);
    }

    #[test]
    fn test_largest_set_size() {
        let mut ds = DisjointSet::new(5);
        assert_eq!(ds.largest_set_size(), 1);
        
        ds.union(0, 1);
        ds.union(0, 2);
        assert_eq!(ds.largest_set_size(), 3);
        
        ds.union(3, 4);
        assert_eq!(ds.largest_set_size(), 3);
    }

    #[test]
    fn test_non_trivial_set_count() {
        let mut ds = DisjointSet::new(5);
        assert_eq!(ds.non_trivial_set_count(), 0);
        
        ds.union(0, 1);
        ds.union(2, 3);
        assert_eq!(ds.non_trivial_set_count(), 2);
        
        ds.union(0, 2);
        assert_eq!(ds.non_trivial_set_count(), 1);
    }

    #[test]
    fn test_find_no_compress() {
        let mut ds = DisjointSet::new(5);
        ds.union(0, 1);
        ds.union(1, 2);
        
        // find_no_compress doesn't modify the structure
        assert!(ds.connected_no_compress(0, 2));
        assert!(ds.connected_no_compress(0, 1));
    }

    #[test]
    fn test_path_compression() {
        let mut ds = DisjointSet::new(5);
        
        // Create a chain: 0 -> 1 -> 2 -> 3 -> 4
        ds.union(0, 1);
        ds.union(1, 2);
        ds.union(2, 3);
        ds.union(3, 4);
        
        // After find with path compression, the tree should be flattened
        let root = ds.find(4);
        
        // All elements should now point directly to the root
        for i in 0..5 {
            assert_eq!(ds.parent[i], root);
        }
    }

    #[test]
    #[should_panic]
    fn test_find_out_of_bounds() {
        let mut ds = DisjointSet::new(3);
        ds.find(5);
    }

    #[test]
    #[should_panic]
    fn test_union_out_of_bounds() {
        let mut ds = DisjointSet::new(3);
        ds.union(0, 5);
    }
}