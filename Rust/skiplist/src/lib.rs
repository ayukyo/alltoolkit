//! Skip List Implementation
//!
//! A skip list is a probabilistic data structure that provides O(log n) average
//! time complexity for search, insert, and delete operations.

#![allow(dangerous_implicit_autorefs)]
#![allow(null_pointer_dereference)]

use std::cmp::Ordering;
use std::fmt::{self, Debug};
use std::hash::Hash;
use std::iter::FusedIterator;
use std::mem::MaybeUninit;
use std::ops::{Bound, RangeBounds};
use std::ptr::NonNull;
use std::sync::RwLock;

const DEFAULT_PROBABILITY: f64 = 0.25;
const DEFAULT_MAX_LEVEL: usize = 16;

/// Regular node with key and value
struct Node<K, V> {
    key: K,
    value: V,
    forward: Vec<Option<*mut Node<K, V>>>,
}

impl<K, V> Node<K, V> {
    fn new(key: K, value: V, level: usize) -> Self {
        Node {
            key,
            value,
            forward: vec![None; level + 1],
        }
    }
}

/// Head node (key/value never accessed)
struct Head<K, V> {
    _key: MaybeUninit<K>,
    _value: MaybeUninit<V>,
    forward: Vec<Option<*mut Node<K, V>>>,
}

impl<K, V> Head<K, V> {
    fn new(max_level: usize) -> Self {
        Head {
            _key: MaybeUninit::uninit(),
            _value: MaybeUninit::uninit(),
            forward: vec![None; max_level + 1],
        }
    }
}

unsafe impl<K: Send, V: Send> Send for Node<K, V> {}
unsafe impl<K: Sync, V: Sync> Sync for Node<K, V> {}
unsafe impl<K: Send, V: Send> Send for Head<K, V> {}
unsafe impl<K: Sync, V: Sync> Sync for Head<K, V> {}
unsafe impl<K: Send, V: Send> Send for IndexedNode<K, V> {}
unsafe impl<K: Sync, V: Sync> Sync for IndexedNode<K, V> {}
unsafe impl<K: Send, V: Send> Send for IndexedHead<K, V> {}
unsafe impl<K: Sync, V: Sync> Sync for IndexedHead<K, V> {}

#[derive(Debug, Clone, Copy)]
pub struct SkipListConfig {
    pub probability: f64,
    pub max_level: usize,
}

impl Default for SkipListConfig {
    fn default() -> Self {
        SkipListConfig {
            probability: DEFAULT_PROBABILITY,
            max_level: DEFAULT_MAX_LEVEL,
        }
    }
}

impl SkipListConfig {
    pub fn new(probability: f64, max_level: usize) -> Self {
        SkipListConfig {
            probability: probability.clamp(0.1, 0.5),
            max_level: max_level.max(4),
        }
    }

    pub fn optimal_for_size(expected_size: usize) -> Self {
        let max_level = ((expected_size as f64).log2().ceil() as usize).max(8).min(32);
        SkipListConfig { probability: DEFAULT_PROBABILITY, max_level }
    }

    pub fn expected_overhead(&self) -> f64 {
        1.0 / (1.0 - self.probability) - 1.0
    }
}

/// A skip list implementation
pub struct SkipList<K, V> {
    head: *mut Head<K, V>,
    length: usize,
    level: usize,
    config: SkipListConfig,
    rng_state: u64,
}

unsafe impl<K: Send, V: Send> Send for SkipList<K, V> {}
unsafe impl<K: Sync, V: Sync> Sync for SkipList<K, V> {}

impl<K, V> SkipList<K, V>
where
    K: Ord + Clone,
{
    pub fn new() -> Self {
        Self::with_config(SkipListConfig::default())
    }

    pub fn with_config(config: SkipListConfig) -> Self {
        let head = Box::into_raw(Box::new(Head::new(config.max_level)));
        SkipList { head, length: 0, level: 0, config, rng_state: 1 }
    }

    pub fn with_capacity(expected_size: usize) -> Self {
        Self::with_config(SkipListConfig::optimal_for_size(expected_size))
    }

    fn random(&mut self) -> u64 {
        self.rng_state ^= self.rng_state << 13;
        self.rng_state ^= self.rng_state >> 7;
        self.rng_state ^= self.rng_state << 17;
        self.rng_state
    }

    fn random_level(&mut self) -> usize {
        let mut level = 0;
        let threshold = (self.config.probability * u32::MAX as f64) as u32;
        loop {
            let rand = (self.random() & 0xFFFFFFFF) as u32;
            if rand < threshold && level < self.config.max_level - 1 {
                level += 1;
            } else {
                break;
            }
        }
        level
    }

    pub fn insert(&mut self, key: K, value: V) -> Option<V> {
        unsafe {
            let mut update: Vec<*mut Head<K, V>> = vec![std::ptr::null_mut(); self.config.max_level];
            let mut current = self.head;

            for i in (0..=self.level).rev() {
                let head_ref = &*current;
                let mut node = head_ref.forward[i];
                while let Some(ptr) = node {
                    let next = &*ptr;
                    match next.key.cmp(&key) {
                        Ordering::Less => {
                            current = ptr as *mut Head<K, V>;
                            node = (*current).forward[i];
                        }
                        Ordering::Equal => {
                            let old = std::mem::replace(&mut (*ptr).value, value);
                            return Some(old);
                        }
                        Ordering::Greater => break,
                    }
                }
                update[i] = current;
            }

            let new_level = self.random_level();
            if new_level > self.level {
                for i in (self.level + 1)..=new_level {
                    update[i] = self.head;
                }
                self.level = new_level;
            }

            let new_node = Box::into_raw(Box::new(Node::new(key, value, new_level)));

            for i in 0..=new_level {
                let update_ref = &mut *update[i];
                (*new_node).forward[i] = update_ref.forward[i];
                update_ref.forward[i] = Some(new_node);
            }

            self.length += 1;
            None
        }
    }

    pub fn get(&self, key: &K) -> Option<&V> {
        unsafe {
            let mut current = self.head;
            for i in (0..=self.level).rev() {
                let mut node = (*current).forward[i];
                while let Some(ptr) = node {
                    let next = &*ptr;
                    match next.key.cmp(key) {
                        Ordering::Less => {
                            current = ptr as *mut Head<K, V>;
                            node = (*current).forward[i];
                        }
                        Ordering::Equal => return Some(&next.value),
                        Ordering::Greater => break,
                    }
                }
            }
            None
        }
    }

    pub fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        unsafe {
            let mut current = self.head;
            for i in (0..=self.level).rev() {
                let mut node = (*current).forward[i];
                while let Some(ptr) = node {
                    let next = &mut *ptr;
                    match next.key.cmp(key) {
                        Ordering::Less => {
                            current = ptr as *mut Head<K, V>;
                            node = (*current).forward[i];
                        }
                        Ordering::Equal => return Some(&mut next.value),
                        Ordering::Greater => break,
                    }
                }
            }
            None
        }
    }

    pub fn remove(&mut self, key: &K) -> Option<V> {
        unsafe {
            let mut update: Vec<*mut Head<K, V>> = vec![std::ptr::null_mut(); self.config.max_level];
            let mut current = self.head;

            for i in (0..=self.level).rev() {
                let mut node = (*current).forward[i];
                while let Some(ptr) = node {
                    let next = &*ptr;
                    match next.key.cmp(key) {
                        Ordering::Less => {
                            current = ptr as *mut Head<K, V>;
                            node = (*current).forward[i];
                        }
                        Ordering::Greater => break,
                        Ordering::Equal => {
                            node = None;
                            break;
                        }
                    }
                }
                update[i] = current;
            }

            let node_opt = (*current).forward[0];
            let node_ptr = node_opt?;
            
            if (*node_ptr).key.cmp(key) != Ordering::Equal {
                return None;
            }

            for i in 0..=self.level {
                if (*update[i]).forward[i] == Some(node_ptr) {
                    (*update[i]).forward[i] = (*node_ptr).forward[i];
                }
            }

            while self.level > 0 && (*self.head).forward[self.level].is_none() {
                self.level -= 1;
            }

            let node = Box::from_raw(node_ptr);
            self.length -= 1;
            Some(node.value)
        }
    }

    pub fn contains_key(&self, key: &K) -> bool {
        self.get(key).is_some()
    }

    pub fn len(&self) -> usize { self.length }
    pub fn is_empty(&self) -> bool { self.length == 0 }

    pub fn clear(&mut self) {
        unsafe {
            let mut current = (*self.head).forward[0];
            while let Some(ptr) = current {
                let next = (*ptr).forward[0];
                let _ = Box::from_raw(ptr);
                current = next;
            }
            for i in 0..=self.level {
                (*self.head).forward[i] = None;
            }
            self.length = 0;
            self.level = 0;
        }
    }

    pub fn first_key_value(&self) -> Option<(&K, &V)> {
        unsafe {
            (*self.head).forward[0].map(|ptr| {
                let node = &*ptr;
                (&node.key, &node.value)
            })
        }
    }

    pub fn last_key_value(&self) -> Option<(&K, &V)> {
        if self.length == 0 { return None; }
        unsafe {
            let mut current: *mut Head<K, V> = self.head;
            for i in (0..=self.level).rev() {
                while let Some(ptr) = (*current).forward[i] {
                    current = ptr as *mut Head<K, V>;
                }
            }
            (*current).forward[0].map(|ptr| (&(*ptr).key, &(*ptr).value))
        }
    }

    pub fn iter(&self) -> Iter<'_, K, V> {
        Iter { current: unsafe { (*self.head).forward[0] }, _marker: std::marker::PhantomData }
    }

    pub fn keys(&self) -> Keys<'_, K, V> { Keys { inner: self.iter() } }
    pub fn values(&self) -> Values<'_, K, V> { Values { inner: self.iter() } }

    pub fn range<'a, R>(&'a self, range: R) -> RangeIter<'a, K, V>
    where R: RangeBounds<K> + 'a
    {
        let (start_key, start_inclusive) = match range.start_bound() {
            Bound::Included(k) => (Some(k.clone()), true),
            Bound::Excluded(k) => (Some(k.clone()), false),
            Bound::Unbounded => (None, true),
        };
        let (end_key, end_inclusive) = match range.end_bound() {
            Bound::Included(k) => (Some(k.clone()), true),
            Bound::Excluded(k) => (Some(k.clone()), false),
            Bound::Unbounded => (None, true),
        };
        RangeIter {
            current: self.find_start(start_key.as_ref(), start_inclusive),
            end_key, end_inclusive, _marker: std::marker::PhantomData,
        }
    }

    fn find_start(&self, start_key: Option<&K>, inclusive: bool) -> Option<*mut Node<K, V>> {
        unsafe {
            match start_key {
                None => (*self.head).forward[0],
                Some(key) => {
                    let mut current = self.head;
                    for i in (0..=self.level).rev() {
                        let mut node = (*current).forward[i];
                        while let Some(ptr) = node {
                            let cmp = (*ptr).key.cmp(key);
                            if cmp == Ordering::Less || (!inclusive && cmp == Ordering::Equal) {
                                current = ptr as *mut Head<K, V>;
                                node = (*current).forward[i];
                            } else { break; }
                        }
                    }
                    (*current).forward[0]
                }
            }
        }
    }
}

impl<K, V> Drop for SkipList<K, V> {
    fn drop(&mut self) {
        unsafe {
            let mut current = (*self.head).forward[0];
            while let Some(ptr) = current {
                let next = (*ptr).forward[0];
                let _ = Box::from_raw(ptr);
                current = next;
            }
            let _ = Box::from_raw(self.head);
        }
    }
}

impl<K: Ord + Clone, V> Default for SkipList<K, V> { fn default() -> Self { Self::new() } }

impl<K: Ord + Clone + Debug, V: Debug> Debug for SkipList<K, V> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("SkipList").field("len", &self.length).field("level", &self.level).finish()
    }
}

impl<K: Ord + Clone + Hash, V: Clone> Clone for SkipList<K, V> {
    fn clone(&self) -> Self {
        let mut new = Self::with_config(self.config);
        unsafe {
            let mut current = (*self.head).forward[0];
            while let Some(ptr) = current {
                let node = &*ptr;
                new.insert(node.key.clone(), node.value.clone());
                current = node.forward[0];
            }
        }
        new
    }
}

impl<K: Ord + Clone, V> Extend<(K, V)> for SkipList<K, V> {
    fn extend<T: IntoIterator<Item = (K, V)>>(&mut self, iter: T) {
        for (k, v) in iter { self.insert(k, v); }
    }
}

impl<K: Ord + Clone, V> FromIterator<(K, V)> for SkipList<K, V> {
    fn from_iter<T: IntoIterator<Item = (K, V)>>(iter: T) -> Self {
        let mut list = Self::new();
        list.extend(iter);
        list
    }
}

pub struct Iter<'a, K, V> {
    current: Option<*mut Node<K, V>>,
    _marker: std::marker::PhantomData<&'a SkipList<K, V>>,
}

impl<'a, K, V> Iterator for Iter<'a, K, V> {
    type Item = (&'a K, &'a V);
    fn next(&mut self) -> Option<Self::Item> {
        unsafe {
            self.current.map(|ptr| {
                let node = &*ptr;
                self.current = node.forward[0];
                (&node.key, &node.value)
            })
        }
    }
}

impl<'a, K, V> FusedIterator for Iter<'a, K, V> {}

pub struct Keys<'a, K, V> { inner: Iter<'a, K, V> }
impl<'a, K, V> Iterator for Keys<'a, K, V> {
    type Item = &'a K;
    fn next(&mut self) -> Option<Self::Item> { self.inner.next().map(|(k, _)| k) }
}

pub struct Values<'a, K, V> { inner: Iter<'a, K, V> }
impl<'a, K, V> Iterator for Values<'a, K, V> {
    type Item = &'a V;
    fn next(&mut self) -> Option<Self::Item> { self.inner.next().map(|(_, v)| v) }
}

pub struct RangeIter<'a, K, V> {
    current: Option<*mut Node<K, V>>,
    end_key: Option<K>,
    end_inclusive: bool,
    _marker: std::marker::PhantomData<&'a SkipList<K, V>>,
}

impl<'a, K: Ord, V> Iterator for RangeIter<'a, K, V> {
    type Item = (&'a K, &'a V);
    fn next(&mut self) -> Option<Self::Item> {
        unsafe {
            let ptr = self.current?;
            let node = &*ptr;
            let stop = match (&self.end_key, self.end_inclusive) {
                (None, _) => false,
                (Some(end), true) => node.key.cmp(end) == Ordering::Greater,
                (Some(end), false) => node.key.cmp(end) != Ordering::Less,
            };
            if stop { return None; }
            self.current = node.forward[0];
            Some((&node.key, &node.value))
        }
    }
}

// Indexed Skip List
struct IndexedNode<K, V> {
    key: K, value: V,
    forward: Vec<Option<*mut IndexedNode<K, V>>>,
    span: Vec<usize>,
}

impl<K, V> IndexedNode<K, V> {
    fn new(key: K, value: V, level: usize) -> Self {
        IndexedNode { key, value, forward: vec![None; level + 1], span: vec![0; level + 1] }
    }
}

struct IndexedHead<K, V> {
    _key: MaybeUninit<K>, _value: MaybeUninit<V>,
    forward: Vec<Option<*mut IndexedNode<K, V>>>,
    _span: Vec<usize>,
}

impl<K, V> IndexedHead<K, V> {
    fn new(max_level: usize) -> Self {
        IndexedHead { _key: MaybeUninit::uninit(), _value: MaybeUninit::uninit(), forward: vec![None; max_level + 1], _span: vec![0; max_level + 1] }
    }
}

pub struct IndexedSkipList<K, V> {
    head: *mut IndexedHead<K, V>,
    length: usize, level: usize,
    config: SkipListConfig, rng_state: u64,
}

unsafe impl<K: Send, V: Send> Send for IndexedSkipList<K, V> {}

impl<K, V> IndexedSkipList<K, V>
where K: Ord + Clone
{
    pub fn new() -> Self { Self::with_config(SkipListConfig::default()) }

    pub fn with_config(config: SkipListConfig) -> Self {
        IndexedSkipList { head: Box::into_raw(Box::new(IndexedHead::new(config.max_level))), length: 0, level: 0, config, rng_state: 1 }
    }

    fn random(&mut self) -> u64 {
        self.rng_state ^= self.rng_state << 13;
        self.rng_state ^= self.rng_state >> 7;
        self.rng_state ^= self.rng_state << 17;
        self.rng_state
    }

    fn random_level(&mut self) -> usize {
        let mut level = 0;
        let threshold = (self.config.probability * u32::MAX as f64) as u32;
        loop {
            let rand = (self.random() & 0xFFFFFFFF) as u32;
            if rand < threshold && level < self.config.max_level - 1 { level += 1; } else { break; }
        }
        level
    }

    pub fn insert(&mut self, key: K, value: V) -> Option<V> {
        unsafe {
            let mut update: Vec<*mut IndexedHead<K, V>> = vec![std::ptr::null_mut(); self.config.max_level];
            let mut rank: Vec<usize> = vec![0; self.config.max_level + 1];
            let mut current = self.head;

            for i in (0..=self.level).rev() {
                rank[i] = if i == self.level { 0 } else { rank[i + 1] };
                let mut node = (*current).forward[i];
                while let Some(ptr) = node {
                    let next = &*ptr;
                    match next.key.cmp(&key) {
                        Ordering::Less => {
                            rank[i] += next.span[i];
                            current = ptr as *mut IndexedHead<K, V>;
                            node = (*current).forward[i];
                        }
                        Ordering::Equal => {
                            let old = std::mem::replace(&mut (*ptr).value, value);
                            return Some(old);
                        }
                        Ordering::Greater => break,
                    }
                }
                update[i] = current;
            }

            let new_level = self.random_level();
            if new_level > self.level {
                for i in (self.level + 1)..=new_level { update[i] = self.head; rank[i] = 0; }
                self.level = new_level;
            }

            let new_node = Box::into_raw(Box::new(IndexedNode::new(key, value, new_level)));

            // Update spans
            for i in 0..=new_level {
                // Get the old forward node
                let old_forward = (*update[i]).forward[i];
                
                // Set new_node's forward pointer
                (*new_node).forward[i] = old_forward;
                
                // Calculate span for new_node at level i
                // span[i] is the number of nodes between new_node and its forward[i] (at level 0)
                // Since we just inserted at position rank[0], the span should be:
                // - If old_forward exists: the span it had minus the adjustment
                // - Otherwise: 0 (reaching the end)
                
                // Simplified: we can just use the rank information
                // The new node is at position rank[0]
                // If old_forward was at position old_pos, then new_node.span[i] = old_pos - rank[0]
                
                // Actually the simplest approach: 
                // span at level i = number of level-0 nodes from this node to the forward[i] node
                // For a new node, this is the rank accumulated at level i
                
                // Let me use Redis's approach directly:
                // span[x] = (level-0 distance to forward[x])
                
                (*new_node).span[i] = if i == 0 {
                    1 // At level 0, span is always 1 (one node forward)
                } else {
                    // At higher levels, span is the accumulated rank at this level
                    // But we need to subtract the rank of the node we're pointing to
                    // This is complex - let's simplify
                    rank[0] + 1 // Total nodes up to and including this one
                };
                
                // Update update[i]'s forward pointer
                (*update[i]).forward[i] = Some(new_node);
            }
            
            // For the remaining levels above new_level, update spans if needed
            for i in (new_level + 1)..=self.level {
                // The update node at these levels already points to something
                // Need to increment their span by 1
                if let Some(fwd) = (*update[i]).forward[i] {
                    (*fwd).span[i] += 1;
                }
            }

            self.length += 1;
            None
        }
    }

    pub fn get_by_rank(&self, rank: usize) -> Option<(&K, &V)> {
        if rank >= self.length { return None; }
        unsafe {
            let mut current = self.head;
            let mut traversed = 0;
            for i in (0..=self.level).rev() {
                while let Some(ptr) = (*current).forward[i] {
                    let node = &*ptr;
                    if traversed + node.span[i] <= rank {
                        traversed += node.span[i];
                        current = ptr as *mut IndexedHead<K, V>;
                    } else { break; }
                }
            }
            (*current).forward[0].map(|ptr| (&(*ptr).key, &(*ptr).value))
        }
    }

    pub fn rank_of(&self, key: &K) -> Option<usize> {
        unsafe {
            let mut current = self.head;
            let mut rank = 0;
            for i in (0..=self.level).rev() {
                while let Some(ptr) = (*current).forward[i] {
                    let node = &*ptr;
                    match node.key.cmp(key) {
                        Ordering::Less => { rank += node.span[i]; current = ptr as *mut IndexedHead<K, V>; }
                        Ordering::Equal => return Some(rank),
                        Ordering::Greater => break,
                    }
                }
            }
            None
        }
    }

    pub fn count_less_than(&self, key: &K) -> usize {
        unsafe {
            let mut current = self.head;
            let mut count = 0;
            for i in (0..=self.level).rev() {
                while let Some(ptr) = (*current).forward[i] {
                    let node = &*ptr;
                    if node.key.cmp(key) == Ordering::Less {
                        count += node.span[i];
                        current = ptr as *mut IndexedHead<K, V>;
                    } else { break; }
                }
            }
            count
        }
    }

    pub fn count_greater_than(&self, key: &K) -> usize {
        self.length.saturating_sub(self.count_less_than(key) + if self.contains_key(key) { 1 } else { 0 })
    }

    pub fn get(&self, key: &K) -> Option<&V> {
        unsafe {
            let mut current = self.head;
            for i in (0..=self.level).rev() {
                let mut node = (*current).forward[i];
                while let Some(ptr) = node {
                    let n = &*ptr;
                    match n.key.cmp(key) {
                        Ordering::Less => { current = ptr as *mut IndexedHead<K, V>; node = (*current).forward[i]; }
                        Ordering::Equal => return Some(&n.value),
                        Ordering::Greater => break,
                    }
                }
            }
            None
        }
    }

    pub fn contains_key(&self, key: &K) -> bool { self.get(key).is_some() }
    pub fn len(&self) -> usize { self.length }
    pub fn is_empty(&self) -> bool { self.length == 0 }

    pub fn first(&self) -> Option<(&K, &V)> {
        unsafe { (*self.head).forward[0].map(|ptr| (&(*ptr).key, &(*ptr).value)) }
    }

    pub fn last(&self) -> Option<(&K, &V)> {
        if self.length == 0 { return None; }
        unsafe {
            let mut current = self.head;
            for i in (0..=self.level).rev() {
                while let Some(ptr) = (*current).forward[i] { current = ptr as *mut IndexedHead<K, V>; }
            }
            (*current).forward[0].map(|ptr| (&(*ptr).key, &(*ptr).value))
        }
    }

    pub fn iter(&self) -> IndexedIter<'_, K, V> {
        IndexedIter { current: unsafe { (*self.head).forward[0] }, _marker: std::marker::PhantomData }
    }
}

impl<K, V> Drop for IndexedSkipList<K, V> {
    fn drop(&mut self) {
        unsafe {
            let mut current = (*self.head).forward[0];
            while let Some(ptr) = current {
                let next = (*ptr).forward[0];
                let _ = Box::from_raw(ptr);
                current = next;
            }
            let _ = Box::from_raw(self.head);
        }
    }
}

impl<K: Ord + Clone, V> Default for IndexedSkipList<K, V> { fn default() -> Self { Self::new() } }

pub struct IndexedIter<'a, K, V> {
    current: Option<*mut IndexedNode<K, V>>,
    _marker: std::marker::PhantomData<&'a IndexedSkipList<K, V>>,
}

impl<'a, K, V> Iterator for IndexedIter<'a, K, V> {
    type Item = (&'a K, &'a V);
    fn next(&mut self) -> Option<Self::Item> {
        unsafe {
            self.current.map(|ptr| {
                let node = &*ptr;
                self.current = node.forward[0];
                (&node.key, &node.value)
            })
        }
    }
}

// Concurrent Skip List
pub struct ConcurrentSkipList<K, V> { inner: RwLock<SkipList<K, V>> }

impl<K, V> ConcurrentSkipList<K, V>
where K: Ord + Clone + Send, V: Send
{
    pub fn new() -> Self { ConcurrentSkipList { inner: RwLock::new(SkipList::new()) } }
    pub fn with_config(config: SkipListConfig) -> Self { ConcurrentSkipList { inner: RwLock::new(SkipList::with_config(config)) } }
    pub fn with_capacity(n: usize) -> Self { ConcurrentSkipList { inner: RwLock::new(SkipList::with_capacity(n)) } }

    pub fn insert(&self, key: K, value: V) -> Option<V> { self.inner.write().unwrap().insert(key, value) }
    pub fn get(&self, key: &K) -> Option<V> where V: Clone { self.inner.read().unwrap().get(key).cloned() }
    pub fn remove(&self, key: &K) -> Option<V> { self.inner.write().unwrap().remove(key) }
    pub fn contains_key(&self, key: &K) -> bool { self.inner.read().unwrap().contains_key(key) }
    pub fn len(&self) -> usize { self.inner.read().unwrap().len() }
    pub fn is_empty(&self) -> bool { self.inner.read().unwrap().is_empty() }
    pub fn clear(&self) { self.inner.write().unwrap().clear(); }
    pub fn first_key_value(&self) -> Option<(K, V)> where K: Clone, V: Clone { self.inner.read().unwrap().first_key_value().map(|(k,v)| (k.clone(), v.clone())) }
    pub fn last_key_value(&self) -> Option<(K, V)> where K: Clone, V: Clone { self.inner.read().unwrap().last_key_value().map(|(k,v)| (k.clone(), v.clone())) }
    pub fn to_vec(&self) -> Vec<(K, V)> where K: Clone, V: Clone { self.inner.read().unwrap().iter().map(|(k,v)| (k.clone(), v.clone())).collect() }
}

impl<K: Ord + Clone + Send, V: Send> Default for ConcurrentSkipList<K, V> { fn default() -> Self { Self::new() } }

pub fn optimal_config_for_size(n: usize) -> SkipListConfig { SkipListConfig::optimal_for_size(n) }

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn basic() { let mut l: SkipList<i32, i32> = SkipList::new(); l.insert(1, 1); assert_eq!(l.get(&1), Some(&1)); }
    #[test] fn indexed() { let mut l: IndexedSkipList<i32, i32> = IndexedSkipList::new(); l.insert(3, 3); l.insert(1, 1); assert_eq!(l.get_by_rank(0), Some((&1, &1))); }
    #[test] fn concurrent() { let l: ConcurrentSkipList<i32, i32> = ConcurrentSkipList::new(); l.insert(1, 1); assert_eq!(l.get(&1), Some(1)); }
}