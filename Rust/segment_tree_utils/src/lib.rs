//! # Segment Tree with Lazy Propagation
//!
//! A high-performance segment tree implementation supporting:
//! - Range queries (sum, min, max)
//! - Range updates with lazy propagation
//! - Zero external dependencies (`no_std` compatible)
//!
//! ## Example
//!
//! ```rust
//! use segment_tree_utils::{SegmentTree, Sum, Min, Max};
//!
//! let arr = [1, 3, 2, 7, 5, 9, 4];
//! let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
//! assert_eq!(seg.query(0..4), 13);
//! seg.update_range(1..4, 10);
//! assert_eq!(seg.query(0..4), 43);
//! ```

#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "std")]
use std::vec::Vec;
#[cfg(not(feature = "std"))]
extern crate alloc;
#[cfg(not(feature = "std"))]
use alloc::vec::Vec;

use core::ops::Range;

// ─────────────────────────────────────────────────────────────────────────────
// Trait
// ─────────────────────────────────────────────────────────────────────────────

/// The algebraic operation for a segment tree. Must form a monoid.
pub trait SegmentTreeOps: 'static + Send + Sync {
    type Value: Clone + Default + Send + Sync;
    type Update: Clone + Default + Send + Sync;

    fn merge(left: &Self::Value, right: &Self::Value) -> Self::Value;
    fn identity() -> Self::Value;
    fn apply_update(value: &mut Self::Value, update: &Self::Update, len: usize);
    fn compose_updates(old: &mut Self::Update, new_update: &Self::Update);
    fn is_noop(update: &Self::Update) -> bool;
}

// ─────────────────────────────────────────────────────────────────────────────
// Operation sets
// ─────────────────────────────────────────────────────────────────────────────

/// Range sum tree (additive updates: add `delta` to each element in range)
#[derive(Debug, Clone, Copy, Default)]
pub struct Sum;

impl SegmentTreeOps for Sum {
    type Value = i64;
    type Update = i64;

    fn merge(l: &i64, r: &i64) -> i64 { *l + *r }
    fn identity() -> i64 { 0 }
    fn apply_update(v: &mut i64, delta: &i64, _len: usize) { *v += *delta; }
    fn compose_updates(old: &mut i64, new: &i64) { *old += *new; }
    fn is_noop(u: &i64) -> bool { *u == 0 }
}

/// Range minimum tree
#[derive(Debug, Clone, Copy, Default)]
pub struct Min;

impl SegmentTreeOps for Min {
    type Value = i64;
    type Update = Option<i64>;

    fn merge(l: &i64, r: &i64) -> i64 { *l.min(r) }
    fn identity() -> i64 { i64::MAX }
    fn apply_update(v: &mut i64, set_val: &Option<i64>, _len: usize) {
        if let Some(val) = set_val { *v = *val; }
    }
    fn compose_updates(old: &mut Option<i64>, new: &Option<i64>) {
        if new.is_some() { *old = *new; }
    }
    fn is_noop(u: &Option<i64>) -> bool { u.is_none() }
}

/// Range maximum tree
#[derive(Debug, Clone, Copy, Default)]
pub struct Max;

impl SegmentTreeOps for Max {
    type Value = i64;
    type Update = Option<i64>;

    fn merge(l: &i64, r: &i64) -> i64 { *l.max(r) }
    fn identity() -> i64 { i64::MIN }
    fn apply_update(v: &mut i64, set_val: &Option<i64>, _len: usize) {
        if let Some(val) = set_val { *v = *val; }
    }
    fn compose_updates(old: &mut Option<i64>, new: &Option<i64>) {
        if new.is_some() { *old = *new; }
    }
    fn is_noop(u: &Option<i64>) -> bool { u.is_none() }
}

// ─────────────────────────────────────────────────────────────────────────────
// Segment Tree
// ─────────────────────────────────────────────────────────────────────────────

/// A segment tree with lazy propagation using the standard 1-indexed power-of-2 layout.
/// Tree nodes: 1 = root, children of node i are 2i and 2i+1.
/// Leaves are at indices P .. 2P-1 (P = next power of 2 >= n).
pub struct SegmentTree<O: SegmentTreeOps> {
    /// Aggregated values for each node
    tree: Vec<O::Value>,
    /// Pending lazy updates for each node
    lazy: Vec<O::Update>,
    /// Number of real elements
    n: usize,
    /// P = next power of 2 >= n
    p: usize,
}

impl<O: SegmentTreeOps> Default for SegmentTree<O> {
    fn default() -> Self { Self::new(0) }
}

impl<O: SegmentTreeOps> SegmentTree<O> {
    /// Create a new segment tree for `n` elements (initialized to identity).
    pub fn new(n: usize) -> Self {
        if n == 0 {
            return Self { tree: vec![O::identity()], lazy: vec![O::Update::default()], n: 0, p: 1 };
        }
        let p = n.next_power_of_two();
        Self {
            tree: vec![O::identity(); 2 * p],
            lazy: vec![O::Update::default(); 2 * p],
            n,
            p,
        }
    }

    /// Build from a slice. O(n).
    pub fn from_slice(arr: &[O::Value]) -> Self {
        let n = arr.len();
        if n == 0 { return Self::new(0); }
        let p = n.next_power_of_two();
        let mut tree = vec![O::identity(); 2 * p];
        let lazy = vec![O::Update::default(); 2 * p];

        for (i, v) in arr.iter().enumerate() {
            tree[p + i] = v.clone();
        }
        for i in (1..p).rev() {
            tree[i] = O::merge(&tree[i << 1], &tree[i << 1 | 1]);
        }

        Self { tree, lazy, n, p }
    }

    #[inline] pub fn len(&self) -> usize { self.n }
    #[inline] pub fn is_empty(&self) -> bool { self.n == 0 }

    // ── Internal helpers ──────────────────────────────────────────────────────

    /// Apply `update` to node `node` (covers `len` elements).
    #[inline(always)]
    fn apply(&mut self, node: usize, update: &O::Update, len: usize) {
        if !O::is_noop(update) {
            O::apply_update(&mut self.tree[node], update, len);
            O::compose_updates(&mut self.lazy[node], update);
        }
    }

    /// Propagate lazy value from `node` to its children.
    #[inline(always)]
    fn push(&mut self, node: usize, left_len: usize, right_len: usize) {
        let update = self.lazy[node].clone();
        if !O::is_noop(&update) {
            self.apply(node << 1, &update, left_len);
            self.apply(node << 1 | 1, &update, right_len);
            self.lazy[node] = O::Update::default();
        }
    }

    /// Recalculate tree[node] from its children.
    #[inline(always)]
    fn pull(&mut self, node: usize) {
        self.tree[node] = O::merge(&self.tree[node << 1], &self.tree[node << 1 | 1]);
    }

    // ── Query ────────────────────────────────────────────────────────────────

    /// Query range [l, r] (inclusive).
    /// Recursive: fully-covered nodes return cached value; partial overlap pushes
    /// lazy, recurses, then pulls.
    pub fn query_range(&mut self, l: usize, r: usize) -> O::Value {
        assert!(l <= r && r < self.n);
        self.query_rec(1, 0, self.p, l, r)
    }

    /// node covers array indices [start, start + len) in the underlying data.
    fn query_rec(&mut self, node: usize, start: usize, len: usize, ql: usize, qr: usize) -> O::Value {
        // No overlap: query is entirely to the left or right of this segment
        if qr < start || ql > start + len - 1 {
            return O::identity();
        }
        // Full cover: this segment is entirely inside the query
        if ql <= start && start + len - 1 <= qr {
            return self.tree[node].clone();
        }
        // Partial overlap and len > 1: recurse
        let half = len >> 1;
        let mid = start + half;

        let left_len = half;
        let right_len = len - half;
        self.push(node, left_len, right_len);

        let mut result = O::identity();
        if ql < mid {
            result = O::merge(&result, &self.query_rec(node << 1, start, half, ql, qr));
        }
        if qr > mid - 1 {  // qr >= mid: query overlaps right child [mid, ...)
            result = O::merge(&result, &self.query_rec(node << 1 | 1, mid, len - half, ql, qr));
        }

        // NOTE: Do NOT pull(node) here. pull would recalculate tree[node] from children,
        // but children's tree values may not yet reflect all updates that tree[node]
        // already incorporated. range_update always pulls after modifying children,
        // so tree[node] stays correct without query modifying it.
        result
    }

    /// Query half-open range [start, end).
    #[inline]
    pub fn query(&mut self, range: Range<usize>) -> O::Value {
        if range.start >= range.end { return O::identity(); }
        self.query_range(range.start, range.end - 1)
    }

    // ── Point update ─────────────────────────────────────────────────────────

    /// Set position `idx` to `value`.
    pub fn point_set(&mut self, idx: usize, value: O::Value) {
        assert!(idx < self.n);
        let mut node = self.p + idx;
        self.tree[node] = value;
        node >>= 1;
        while node >= 1 {
            self.pull(node);
            node >>= 1;
        }
    }

    // ── Range update ─────────────────────────────────────────────────────────

    /// Update range [l, r] (inclusive) with `update`.
    pub fn range_update(&mut self, l: usize, r: usize, update: O::Update) {
        assert!(l <= r && r < self.n);
        self.range_update_rec(1, 0, self.p, l, r, &update);
    }

    /// Update half-open range [start, end) with `update`.
    pub fn update_range(&mut self, range: Range<usize>, update: O::Update) {
        if range.start >= range.end { return; }
        self.range_update(range.start, range.end - 1, update);
    }

    /// node covers [start, start + len).
    fn range_update_rec(&mut self, node: usize, start: usize, len: usize, ul: usize, ur: usize, update: &O::Update) {
        // No overlap
        if ur < start || ul > start + len - 1 {
            return;
        }
        // Full cover
        if ul <= start && start + len - 1 <= ur {
            self.apply(node, update, len);
            return;
        }

        let half = len >> 1;
        let mid = start + half;

        let left_len = half;
        let right_len = len - half;
        if left_len > 0 {
            self.push(node, left_len, right_len);
        }

        if ul < mid {
            self.range_update_rec(node << 1, start, half, ul, ur, update);
        }
        if ur > mid {
            self.range_update_rec(node << 1 | 1, mid, len - half, ul, ur, update);
        }

        self.pull(node);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum_build_and_query() {
        let arr = [1i64, 3, 2, 7, 5, 9, 4];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        assert_eq!(seg.query(0..7), 31);
        assert_eq!(seg.query(0..3), 6);
        assert_eq!(seg.query(3..7), 25);
        assert_eq!(seg.query(1..4), 12);
    }

    #[test]
    fn test_sum_point_set() {
        let arr = [1i64, 3, 2, 7];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        seg.point_set(2, 10);
        assert_eq!(seg.query(0..4), 21);
        seg.point_set(0, 0);
        assert_eq!(seg.query(0..4), 20);
    }

    #[test]
    fn test_sum_range_add() {
        let arr = [1i64, 3, 2, 7, 5, 9, 4];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        seg.update_range(1..4, 10);
        assert_eq!(seg.query(0..4), 43);
        assert_eq!(seg.query(0..1), 1);
        assert_eq!(seg.query(4..7), 18);
    }

    #[test]
    fn test_sum_multiple_updates() {
        let arr = [0i64; 5];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        seg.update_range(0..5, 5);
        seg.update_range(1..3, 3);
        seg.update_range(2..5, 2);
        // idx: 0  1  2  3  4
        // val: 5  8 10 10  9
        assert_eq!(seg.query(0..5), 42);
        assert_eq!(seg.query(0..1), 5);
        assert_eq!(seg.query(1..2), 8);
        assert_eq!(seg.query(4..5), 9);
    }

    #[test]
    fn test_min_build_and_query() {
        let arr = [5i64, 2, 8, 1, 9, 3, 7];
        let mut seg: SegmentTree<Min> = SegmentTree::from_slice(&arr);
        assert_eq!(seg.query(0..7), 1);
        assert_eq!(seg.query(0..3), 2);
        assert_eq!(seg.query(4..7), 3);
    }

    #[test]
    fn test_min_range_set() {
        let arr = [5i64, 2, 8, 1, 9, 3, 7];
        let mut seg: SegmentTree<Min> = SegmentTree::from_slice(&arr);
        seg.update_range(1..5, Some(0));
        assert_eq!(seg.query(0..7), 0);
        assert_eq!(seg.query(0..1), 5);
        assert_eq!(seg.query(5..7), 3);
    }

    #[test]
    fn test_max_build_and_query() {
        let arr = [5i64, 2, 8, 1, 9, 3, 7];
        let mut seg: SegmentTree<Max> = SegmentTree::from_slice(&arr);
        assert_eq!(seg.query(0..7), 9);
        assert_eq!(seg.query(0..3), 8);
        assert_eq!(seg.query(4..7), 9);
    }

    #[test]
    fn test_single_element() {
        let arr = [42i64];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        assert_eq!(seg.query(0..1), 42);
        seg.update_range(0..1, 5);
        assert_eq!(seg.query(0..1), 47);
        seg.point_set(0, 10);
        assert_eq!(seg.query(0..1), 10);
    }

    #[test]
    fn test_empty_tree() {
        let arr: [i64; 0] = [];
        let seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        assert!(seg.is_empty());
        assert_eq!(seg.len(), 0);
    }

    #[test]
    fn test_large_array() {
        let n = 100_000;
        let arr: Vec<i64> = (0..n as i64).collect();
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        assert_eq!(seg.query(0..n), (n as i64 - 1) * n as i64 / 2);
        seg.update_range(1000..50000, 1);
        let expected = (n as i64 - 1) * n as i64 / 2 + (50000 - 1000) as i64;
        assert_eq!(seg.query(0..n), expected);
    }

    #[test]
    fn test_point_set_after_range_update() {
        let arr = [1i64, 2, 3, 4, 5];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        seg.update_range(0..3, 10);
        seg.point_set(1, 100);
        // [0,2] += 10: [11,12,13,4,5], then idx 1 = 100
        // [11,100,13,4,5]
        assert_eq!(seg.query(0..5), 133);
        assert_eq!(seg.query(0..1), 11);
        assert_eq!(seg.query(1..2), 100);
        assert_eq!(seg.query(2..3), 13);
    }

    #[test]
    fn test_zero_update() {
        let arr = [1i64, 2, 3, 4, 5];
        let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);
        seg.update_range(0..5, 0);
        assert_eq!(seg.query(0..5), 15);
    }
}
