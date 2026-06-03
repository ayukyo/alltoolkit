//! # CRDT Utilities - Conflict-free Replicated Data Types
//!
//! A comprehensive collection of CRDT implementations for distributed systems.
//! These data structures can be updated independently and merged without coordination,
//! making them ideal for collaborative applications, offline-first systems, and distributed databases.
//!
//! ## Implemented CRDTs
//!
//! - **G-Counter**: Grow-only counter (only increments)
//! - **PN-Counter**: Positive-Negative counter (supports increments and decrements)
//! - **2P-Set**: Two-Phase Set (add-only set with tombstones)
//! - **OR-Set**: Observed-Remove Set (add/remove with unique tags)
//! - **LWW-Register**: Last-Writer-Wins Register
//!
//! ## Usage
//!
//! ```rust
//! use crdt_utils::{GCounter, PNCounter, ORSet, LWWRegister};
//!
//! // G-Counter example
//! let mut c1 = GCounter::new("A".to_string());
//! c1.increment(1);
//! let mut c2 = GCounter::new("B".to_string());
//! c2.increment(1);
//! c2.increment(1);
//! c1.merge(&c2);
//! assert_eq!(c1.value(), 3);
//! ```

use std::collections::BTreeMap;
use std::cmp::Ordering;
use serde::{Serialize, Deserialize};

// ============================================================================
// G-Counter (Grow-only Counter)
// ============================================================================

/// A grow-only counter that only supports increments.
/// Each node can only increment its own replica; merging takes the maximum per node.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GCounter {
    /// Node identifier
    node_id: String,
    /// Per-node counters
    state: BTreeMap<String, u64>,
}

impl GCounter {
    /// Create a new G-Counter for the given node
    pub fn new(node_id: String) -> Self {
        Self {
            node_id,
            state: BTreeMap::new(),
        }
    }

    /// Increment this node's counter by `delta`
    pub fn increment(&mut self, delta: u64) {
        *self.state.entry(self.node_id.clone()).or_insert(0) += delta;
    }

    /// Get the total value (sum of all node counters)
    pub fn value(&self) -> u64 {
        self.state.values().sum()
    }

    /// Merge another G-Counter into this one
    pub fn merge(&mut self, other: &GCounter) {
        for (node, value) in &other.state {
            let entry = self.state.entry(node.clone()).or_insert(0);
            *entry = (*entry).max(*value);
        }
    }
}

// ============================================================================
// PN-Counter (Positive-Negative Counter)
// ============================================================================

/// A counter that supports both increments and decrements.
/// Uses two G-Counters internally: one for positive deltas, one for negative.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PNCounter {
    /// Node identifier
    node_id: String,
    /// Positive increments
    positive: BTreeMap<String, u64>,
    /// Negative decrements (stored as positive values)
    negative: BTreeMap<String, u64>,
}

impl PNCounter {
    /// Create a new PN-Counter for the given node
    pub fn new(node_id: String) -> Self {
        Self {
            node_id,
            positive: BTreeMap::new(),
            negative: BTreeMap::new(),
        }
    }

    /// Increment the counter (can be called multiple times)
    pub fn increment(&mut self, delta: u64) {
        *self.positive.entry(self.node_id.clone()).or_insert(0) += delta;
    }

    /// Decrement the counter
    pub fn decrement(&mut self, delta: u64) {
        *self.negative.entry(self.node_id.clone()).or_insert(0) += delta;
    }

    /// Get the current value (positive sum minus negative sum)
    pub fn value(&self) -> i64 {
        let pos: u64 = self.positive.values().sum();
        let neg: u64 = self.negative.values().sum();
        pos as i64 - neg as i64
    }

    /// Merge another PN-Counter into this one
    pub fn merge(&mut self, other: &PNCounter) {
        for (node, value) in &other.positive {
            let entry = self.positive.entry(node.clone()).or_insert(0);
            *entry = (*entry).max(*value);
        }
        for (node, value) in &other.negative {
            let entry = self.negative.entry(node.clone()).or_insert(0);
            *entry = (*entry).max(*value);
        }
    }
}

// ============================================================================
// 2P-Set (Two-Phase Set)
// ============================================================================

/// A add-only set with tombstones. Elements can only be added, never removed
/// from the merged view. Uses tombstones to handle concurrent removes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TwoPhaseSet {
    /// Set of added elements (using BTreeMap to preserve ordering)
    additions: BTreeMap<String, bool>,
    /// Tombstones for removed elements
    removals: BTreeMap<String, bool>,
}

impl TwoPhaseSet {
    /// Create a new empty 2P-Set
    pub fn new() -> Self {
        Self {
            additions: BTreeMap::new(),
            removals: BTreeMap::new(),
        }
    }

    /// Add an element to the set
    pub fn add(&mut self, element: String) {
        if !self.removals.contains_key(&element) {
            self.additions.insert(element, true);
        }
    }

    /// Remove an element (uses tombstone)
    pub fn remove(&mut self, element: &str) {
        if self.additions.contains_key(element) {
            self.removals.insert(element.to_string(), true);
        }
    }

    /// Check if element is in the set (added but not removed)
    pub fn contains(&self, element: &str) -> bool {
        self.additions.contains_key(element) && !self.removals.contains_key(element)
    }

    /// Get all elements in the set
    pub fn elements(&self) -> Vec<String> {
        self.additions
            .keys()
            .filter(|e| !self.removals.contains_key(*e))
            .cloned()
            .collect()
    }

    /// Merge with another 2P-Set
    pub fn merge(&mut self, other: &TwoPhaseSet) {
        for elem in other.additions.keys() {
            if !self.removals.contains_key(elem) {
                self.additions.insert(elem.clone(), true);
            }
        }
        for elem in other.removals.keys() {
            self.removals.insert(elem.clone(), true);
        }
    }
}

impl Default for TwoPhaseSet {
    fn default() -> Self {
        Self::new()
    }
}

// ============================================================================
// OR-Set (Observed-Remove Set)
// ============================================================================

/// An Observed-Remove Set where each add gets a unique tag.
/// Removes only affect elements with matching tags that are still present.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ORSet {
    /// Element -> Set of unique tags (random u64) for active additions
    items: BTreeMap<String, BTreeMap<u64, bool>>,
    /// Element -> Set of tags that have been removed
    removed: BTreeMap<String, BTreeMap<u64, bool>>,
    /// Elements that have been removed by a remove operation (per-element tombstone)
    removed_elements: BTreeMap<String, bool>,
}

impl ORSet {
    /// Create a new empty OR-Set
    pub fn new() -> Self {
        Self {
            items: BTreeMap::new(),
            removed: BTreeMap::new(),
            removed_elements: BTreeMap::new(),
        }
    }

    /// Add an element with a unique tag
    fn add_with_tag(&mut self, element: String, tag: u64) {
        // Clear element-level tombstone if re-adding
        self.removed_elements.remove(&element);
        self.items
            .entry(element.clone())
            .or_insert_with(BTreeMap::new)
            .insert(tag, true);
    }

    /// Add an element with a randomly generated tag
    pub fn add(&mut self, element: String) {
        let tag = rand_tag();
        self.add_with_tag(element, tag);
    }

    /// Remove a specific element (removes all current tags and marks per-element tombstone)
    pub fn remove(&mut self, element: &str) -> bool {
        if let Some(tags) = self.items.get(element).cloned() {
            // Mark element as globally removed (per-element tombstone)
            self.removed_elements.insert(element.to_string(), true);
            let entry = self.removed.entry(element.to_string()).or_insert_with(BTreeMap::new);
            for tag in tags.keys() {
                entry.insert(*tag, true);
            }
            // Clear all tags (remove all current tags)
            self.items.get_mut(element).map(|t| t.retain(|_, _| false));
            true
        } else {
            false
        }
    }

    /// Look up an element
    pub fn lookup(&self, element: &str) -> Vec<u64> {
        self.items
            .get(element)
            .map(|tags| tags.keys().copied().collect())
            .unwrap_or_default()
    }

    /// Check if element exists
    pub fn contains(&self, element: &str) -> bool {
        if self.removed_elements.contains_key(element) {
            return false;
        }
        self.items
            .get(element)
            .map(|tags| !tags.is_empty())
            .unwrap_or(false)
    }

    /// Get all elements
    pub fn elements(&self) -> Vec<String> {
        self.items
            .keys()
            .filter(|e| !self.removed_elements.contains_key(*e))
            .cloned()
            .collect()
    }

    /// Merge with another OR-Set
    pub fn merge(&mut self, other: &ORSet) {
        // Merge per-element removals first
        for elem in other.removed_elements.keys() {
            self.removed_elements.insert(elem.clone(), true);
        }

        // Merge additions (skip elements that are globally removed)
        for (element, tags) in &other.items {
            if self.removed_elements.contains_key(element) {
                continue;
            }
            let entry = self.items.entry(element.clone()).or_insert_with(BTreeMap::new);
            for tag in tags.keys() {
                // Only add if not already removed
                let removed_tag = self.removed.get(element).map(|r| r.contains_key(tag)).unwrap_or(false);
                if !removed_tag {
                    entry.insert(*tag, true);
                }
            }
        }

        // Merge per-tag removals (tombstones)
        for (element, tags) in &other.removed {
            let entry = self.removed.entry(element.clone()).or_insert_with(BTreeMap::new);
            for tag in tags.keys() {
                entry.insert(*tag, true);
            }
            // Clean up items that are fully removed
            if let Some(item_tags) = self.items.get_mut(element) {
                item_tags.retain(|t, _| !entry.contains_key(t));
                if item_tags.is_empty() {
                    self.items.remove(element);
                }
            }
        }
    }
}

impl Default for ORSet {
    fn default() -> Self {
        Self::new()
    }
}

/// Generate a pseudo-random tag using timestamp + element hash
fn rand_tag() -> u64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let mut h: u64 = 0;
    let bytes = now.to_le_bytes();
    for (i, &b) in bytes.iter().enumerate() {
        h = h.wrapping_mul(31).wrapping_add(b as u64);
    }
    h
}

// ============================================================================
// LWW-Register (Last-Writer-Wins Register)
// ============================================================================

/// A register that resolves conflicts by timestamp (Lamport timestamps).
/// The element with the highest timestamp wins.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LWWRegister {
    /// Current value and its timestamp
    value: Option<(String, u64)>,
    /// Monotonically increasing logical clock
    clock: u64,
}

impl LWWRegister {
    /// Create a new empty LWW-Register
    pub fn new() -> Self {
        Self {
            value: None,
            clock: 0,
        }
    }

    /// Set the value with current logical clock
    pub fn set(&mut self, value: String) {
        self.clock += 1;
        self.value = Some((value, self.clock));
    }

    /// Get the current value
    pub fn get(&self) -> Option<&str> {
        self.value.as_ref().map(|(v, _)| v.as_str())
    }

    /// Get the timestamp of current value
    pub fn timestamp(&self) -> Option<u64> {
        self.value.as_ref().map(|(_, ts)| *ts)
    }

    /// Merge with another LWW-Register (highest timestamp wins)
    pub fn merge(&mut self, other: &LWWRegister) {
        let self_val = self.value.take();
        match (self_val, &other.value) {
            (Some((sv, st1)), Some((ov, st2))) if *st2 > st1 => {
                self.clock = self.clock.max(*st2) + 1;
                self.value = Some((ov.clone(), self.clock));
            }
            (Some((sv, _)), Some((ov, st2))) => {
                self.clock = self.clock.max(*st2) + 1;
                self.value = Some((ov.clone(), self.clock));
            }
            (None, Some((ov, st2))) => {
                self.clock = *st2 + 1;
                self.value = Some((ov.clone(), self.clock));
            }
            (Some((sv, st)), None) => {
                self.value = Some((sv, st));
            }
            (None, None) => {}
        }
    }
}

impl Default for LWWRegister {
    fn default() -> Self {
        Self::new()
    }
}

// ============================================================================
// RGA (Replicated Growable Array) - Simplified
// ============================================================================

/// A simple operation-based RGA (Replicated Growable Array).
/// Each operation has a unique ID and a reference ID for ordering.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Operation {
    pub id: u64,
    pub parent_id: Option<u64>,
    pub value: char,
    pub deleted: bool,
}

impl Operation {
    fn new(id: u64, parent_id: Option<u64>, value: char) -> Self {
        Self { id, parent_id, value, deleted: false }
    }
}

/// Simplified RGA for character sequences
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RGA {
    /// All operations
    ops: Vec<Operation>,
    /// Next operation ID
    next_id: u64,
}

impl RGA {
    /// Create a new empty RGA
    pub fn new() -> Self {
        Self { ops: Vec::new(), next_id: 1 }
    }

    /// Insert a character at position (after inserted_at_id)
    pub fn insert(&mut self, c: char, after_id: Option<u64>) {
        let id = self.next_id;
        self.next_id += 1;
        self.ops.push(Operation::new(id, after_id, c));
    }

    /// Delete a character by operation ID
    pub fn delete(&mut self, id: u64) -> bool {
        if let Some(op) = self.ops.iter_mut().find(|o| o.id == id) {
            if !op.deleted {
                op.deleted = true;
                return true;
            }
        }
        false
    }

    /// Get the visible characters in order
    pub fn content(&self) -> String {
        let mut result = String::new();
        for op in &self.ops {
            if !op.deleted {
                result.push(op.value);
            }
        }
        result
    }

    /// Merge with another RGA (union of operations, sorted by id)
    pub fn merge(&mut self, other: &RGA) {
        let max_self_id = self.ops.iter().map(|o| o.id).max().unwrap_or(0);
        for op in &other.ops {
            if !self.ops.iter().any(|o| o.id == op.id) {
                let mut new_op = op.clone();
                if new_op.id <= max_self_id {
                    new_op.id = self.next_id;
                    self.next_id += 1;
                }
                self.ops.push(new_op);
            }
        }
        // Sort by id to preserve insertion order
        self.ops.sort_by(|a, b| {
            match (a.parent_id, b.parent_id) {
                (None, None) | (Some(_), None) | (None, Some(_)) => a.id.cmp(&b.id),
                (Some(p_a), Some(p_b)) => {
                    if p_a == p_b {
                        a.id.cmp(&b.id) // Same parent, sort by id (insertion order)
                    } else {
                        p_a.cmp(&p_b) // Different parents, sort by parent
                    }
                }
            }
        });
    }
}

impl Default for RGA {
    fn default() -> Self {
        Self::new()
    }
}

// ============================================================================
// Vector Clock (for causal ordering)
// ============================================================================

/// A vector clock for tracking causality in distributed systems.
/// Used to determine the partial ordering of events.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VectorClock {
    /// Node -> Clock value
    clock: BTreeMap<String, u64>,
}

impl VectorClock {
    /// Create a new VectorClock
    pub fn new(node_id: &str) -> Self {
        let mut clock = BTreeMap::new();
        clock.insert(node_id.to_string(), 0);
        Self { clock }
    }

    /// Increment this node's clock
    pub fn tick(&mut self, node_id: &str) {
        *self.clock.entry(node_id.to_string()).or_insert(0) += 1;
    }

    /// Merge with another vector clock (take max of each component)
    pub fn merge(&mut self, other: &VectorClock) {
        for (node, ts) in &other.clock {
            let entry = self.clock.entry(node.clone()).or_insert(0);
            *entry = (*entry).max(*ts);
        }
    }

    /// Get the clock value for a node
    pub fn get(&self, node_id: &str) -> u64 {
        self.clock.get(node_id).copied().unwrap_or(0)
    }

    /// Compare with another vector clock
    /// Returns: Equal, Concurrent (partial order), or one dominates
    pub fn compare(&self, other: &VectorClock) -> Ordering {
        let all_nodes: Vec<_> = self.clock.keys().chain(other.clock.keys()).collect();
        let mut self_greater = false;
        let mut other_greater = false;

        for node in all_nodes {
            let s = self.clock.get(node).copied().unwrap_or(0);
            let o = other.clock.get(node).copied().unwrap_or(0);
            if s > o { self_greater = true; }
            if o > s { other_greater = true; }
        }

        if self_greater && other_greater {
            Ordering::Equal // Concurrent
        } else if self_greater {
            Ordering::Greater
        } else if other_greater {
            Ordering::Less
        } else {
            Ordering::Equal
        }
    }

    /// Check if this clock happens-before another
    pub fn happens_before(&self, other: &VectorClock) -> bool {
        let all_nodes: Vec<_> = self.clock.keys().chain(other.clock.keys()).collect();
        let mut dominated = false;

        for node in all_nodes {
            let s = self.clock.get(node).copied().unwrap_or(0);
            let o = other.clock.get(node).copied().unwrap_or(0);
            if s > o { return false; }
            if s < o { dominated = true; }
        }

        dominated
    }
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    // G-Counter tests
    #[test]
    fn test_gcounter_increment() {
        let mut c = GCounter::new("A".to_string());
        c.increment(1);
        c.increment(2);
        assert_eq!(c.value(), 3);
    }

    #[test]
    fn test_gcounter_merge() {
        let mut c1 = GCounter::new("A".to_string());
        c1.increment(5);

        let mut c2 = GCounter::new("B".to_string());
        c2.increment(3);

        c1.merge(&c2);
        assert_eq!(c1.value(), 8);
    }

    #[test]
    fn test_gcounter_concurrent_increment() {
        let mut c1 = GCounter::new("A".to_string());
        c1.increment(10);

        let mut c2 = GCounter::new("B".to_string());
        c2.increment(10);

        c1.merge(&c2);
        assert_eq!(c1.value(), 20);
    }

    #[test]
    fn test_gcounter_max_merge() {
        // When nodes increment at different times
        let mut c1 = GCounter::new("A".to_string());
        c1.increment(3);

        let mut c2 = GCounter::new("A".to_string());
        c2.increment(5);

        c1.merge(&c2);
        assert_eq!(c1.value(), 5); // Takes max, not sum
    }

    // PN-Counter tests
    #[test]
    fn test_pncounter_increment_decrement() {
        let mut c = PNCounter::new("A".to_string());
        c.increment(10);
        c.decrement(3);
        assert_eq!(c.value(), 7);
    }

    #[test]
    fn test_pncounter_merge() {
        let mut c1 = PNCounter::new("A".to_string());
        c1.increment(5);

        let mut c2 = PNCounter::new("B".to_string());
        c2.increment(3);
        c2.decrement(2);

        c1.merge(&c2);
        assert_eq!(c1.value(), 6);
    }

    #[test]
    fn test_pncounter_negative_result() {
        let mut c = PNCounter::new("A".to_string());
        c.decrement(10);
        assert_eq!(c.value(), -10);
    }

    #[test]
    fn test_pncounter_concurrent_ops() {
        let mut c1 = PNCounter::new("A".to_string());
        c1.increment(100);

        let mut c2 = PNCounter::new("B".to_string());
        c2.increment(50);
        c2.decrement(30);

        c1.merge(&c2);
        assert_eq!(c1.value(), 120);
    }

    // 2P-Set tests
    #[test]
    fn test_twophaseset_add() {
        let mut s = TwoPhaseSet::new();
        s.add("apple".to_string());
        s.add("banana".to_string());
        assert!(s.contains("apple"));
        assert!(s.contains("banana"));
        assert!(!s.contains("cherry"));
    }

    #[test]
    fn test_twophaseset_remove() {
        let mut s = TwoPhaseSet::new();
        s.add("apple".to_string());
        s.add("banana".to_string());
        s.remove("apple");
        assert!(!s.contains("apple"));
        assert!(s.contains("banana"));
    }

    #[test]
    fn test_twophaseset_cannot_readd() {
        let mut s = TwoPhaseSet::new();
        s.add("apple".to_string());
        s.remove("apple");
        s.add("apple".to_string()); // Should not re-add after remove
        assert!(!s.contains("apple"));
    }

    #[test]
    fn test_twophaseset_elements() {
        let mut s = TwoPhaseSet::new();
        s.add("a".to_string());
        s.add("b".to_string());
        s.add("c".to_string());
        s.remove("b");
        let elems = s.elements();
        assert_eq!(elems, vec!["a", "c"]);
    }

    #[test]
    fn test_twophaseset_merge() {
        let mut s1 = TwoPhaseSet::new();
        s1.add("a".to_string());
        s1.add("b".to_string());

        let mut s2 = TwoPhaseSet::new();
        s2.add("b".to_string());
        s2.add("c".to_string());
        s2.remove("b");

        s1.merge(&s2);
        assert!(s1.contains("a"));
        assert!(!s1.contains("b")); // Removed in s2
        assert!(s1.contains("c"));
    }

    #[test]
    fn test_twophaseset_concurrent_add_remove() {
        let mut s1 = TwoPhaseSet::new();
        s1.add("x".to_string());

        let mut s2 = TwoPhaseSet::new();
        s2.add("x".to_string());
        s2.remove("x");

        s1.merge(&s2);
        // x was removed in s2, so not in merged result
        assert!(!s1.contains("x"));
    }

    // OR-Set tests
    #[test]
    fn test_orset_add() {
        let mut s = ORSet::new();
        s.add("hello".to_string());
        s.add("world".to_string());
        assert!(s.contains("hello"));
        assert!(s.contains("world"));
        assert!(!s.contains("rust"));
    }

    #[test]
    fn test_orset_remove() {
        let mut s = ORSet::new();
        s.add("apple".to_string());
        s.add("banana".to_string());
        assert!(s.remove("apple"));
        assert!(!s.contains("apple"));
        assert!(s.contains("banana"));
    }

    #[test]
    fn test_orset_concurrent_add() {
        let mut s1 = ORSet::new();
        s1.add("x".to_string());

        let mut s2 = ORSet::new();
        s2.add("x".to_string());

        s1.merge(&s2);
        assert!(s1.contains("x"));
        // Both tags present, still contains x
    }

    #[test]
    fn test_orset_concurrent_add_remove() {
        let mut s1 = ORSet::new();
        s1.add("x".to_string());

        let mut s2 = ORSet::new();
        s2.add("x".to_string());
        s2.remove("x");

        s1.merge(&s2);
        // s2 removed x, so it should be removed in merged result
        assert!(!s1.contains("x"));
    }

    #[test]
    fn test_orset_readd_after_remove() {
        let mut s = ORSet::new();
        s.add("test".to_string());
        s.remove("test");
        s.add("test".to_string()); // Re-add creates new tags
        assert!(s.contains("test"));
    }

    #[test]
    fn test_orset_lookup() {
        let mut s = ORSet::new();
        s.add("x".to_string());
        s.add("x".to_string()); // Second add with different tag
        let tags = s.lookup("x");
        assert_eq!(tags.len(), 2);
    }

    // LWW-Register tests
    #[test]
    fn test_lwwregister_set() {
        let mut r = LWWRegister::new();
        r.set("hello".to_string());
        assert_eq!(r.get(), Some("hello"));
    }

    #[test]
    fn test_lwwregister_overwrite() {
        let mut r = LWWRegister::new();
        r.set("first".to_string());
        r.set("second".to_string());
        assert_eq!(r.get(), Some("second"));
    }

    #[test]
    fn test_lwwregister_merge_winner() {
        let mut r1 = LWWRegister::new();
        r1.set("older".to_string());

        let mut r2 = LWWRegister::new();
        r2.set("newer".to_string());

        r1.merge(&r2);
        assert_eq!(r1.get(), Some("newer"));
    }

    #[test]
    fn test_lwwregister_merge_equal() {
        let mut r1 = LWWRegister::new();
        r1.set("value".to_string());

        let mut r2 = LWWRegister::new();
        r2.set("value".to_string());

        r1.merge(&r2);
        assert_eq!(r1.get(), Some("value"));
    }

    // RGA tests
    #[test]
    fn test_rga_insert() {
        let mut r = RGA::new();
        r.insert('h', None);
        r.insert('e', Some(1));
        r.insert('l', Some(2));
        r.insert('l', Some(3));
        r.insert('o', Some(4));
        assert_eq!(r.content(), "hello");
    }

    #[test]
    fn test_rga_delete() {
        let mut r = RGA::new();
        r.insert('h', None);
        r.insert('e', Some(1));
        r.insert('l', Some(2));
        r.insert('l', Some(3));
        r.insert('o', Some(4));
        r.delete(3); // Delete first 'l'
        assert_eq!(r.content(), "helo");
    }

    #[test]
    fn test_rga_merge() {
        let mut r1 = RGA::new();
        r1.insert('a', None);

        let mut r2 = RGA::new();
        r2.insert('a', None);
        r2.insert('b', Some(1));

        r1.merge(&r2);
        assert_eq!(r1.content(), "ab");
    }

    // VectorClock tests
    #[test]
    fn test_vectorclock_tick() {
        let mut vc = VectorClock::new("A");
        vc.tick("A");
        vc.tick("A");
        // Clock should be 2 (we ticked twice)
        assert!(vc.clock.get("A").is_some());
    }

    #[test]
    fn test_vectorclock_merge() {
        let mut vc1 = VectorClock::new("A");
        vc1.tick("A");
        vc1.tick("A"); // vc1.A = 2

        let mut vc2 = VectorClock::new("B");
        vc2.tick("B"); // vc2.B = 1

        vc1.merge(&vc2);
        assert_eq!(vc1.clock.get("A"), Some(&2));
        assert_eq!(vc1.clock.get("B"), Some(&1));
    }

    #[test]
    fn test_vectorclock_happens_before() {
        let mut vc1 = VectorClock::new("A");
        vc1.tick("A");
        vc1.tick("A"); // vc1 = {A: 2}

        let mut vc2 = VectorClock::new("A");
        vc2.tick("A");
        vc2.tick("A");
        vc2.tick("A"); // vc2 = {A: 3}

        assert!(vc2.happens_before(&vc1) == false);
        assert!(vc1.happens_before(&vc2)); // vc1 happens before vc2
    }

    #[test]
    fn test_vectorclock_concurrent() {
        let mut vc1 = VectorClock::new("A");
        vc1.tick("A"); // vc1 = {A: 1}

        let mut vc2 = VectorClock::new("B");
        vc2.tick("B"); // vc2 = {B: 1}

        // Neither happens-before the other -> concurrent
        assert!(!vc1.happens_before(&vc2));
        assert!(!vc2.happens_before(&vc1));
    }

    #[test]
    fn test_vectorclock_compare() {
        let mut vc1 = VectorClock::new("A");
        vc1.tick("A");
        vc1.tick("A");

        let mut vc2 = VectorClock::new("B");
        vc2.tick("B");
        vc2.tick("B");
        vc2.tick("B");

        // Concurrent
        let cmp = vc1.compare(&vc2);
        assert_eq!(cmp, Ordering::Equal);
    }

    #[test]
    fn test_vectorclock_equal() {
        let mut vc1 = VectorClock::new("A");
        vc1.tick("A");
        vc1.tick("A");

        let mut vc2 = VectorClock::new("A");
        vc2.tick("A");
        vc2.tick("A");

        assert_eq!(vc1.compare(&vc2), Ordering::Equal);
    }

    // Edge cases
    #[test]
    fn test_gcounter_empty() {
        let c = GCounter::new("X".to_string());
        assert_eq!(c.value(), 0);
    }

    #[test]
    fn test_pncounter_empty() {
        let c = PNCounter::new("X".to_string());
        assert_eq!(c.value(), 0);
    }

    #[test]
    fn test_lwwregister_empty() {
        let r = LWWRegister::new();
        assert_eq!(r.get(), None);
    }

    #[test]
    fn test_orset_empty() {
        let s = ORSet::new();
        assert!(s.elements().is_empty());
    }

    #[test]
    fn test_rga_empty() {
        let r = RGA::new();
        assert_eq!(r.content(), "");
    }
}
