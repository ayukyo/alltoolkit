//! Additional comprehensive tests for DisjointSet

use disjoint_set::{DisjointSet, LabeledDisjointSet, UnionStrategy};
use std::collections::HashSet;

#[test]
fn test_single_element() {
    let ds = DisjointSet::new(1);
    assert_eq!(ds.len(), 1);
    assert_eq!(ds.set_count(), 1);
}

#[test]
fn test_no_union() {
    let mut ds = DisjointSet::new(10);
    assert_eq!(ds.set_count(), 10);
    
    // All elements are isolated
    for i in 0..10 {
        assert!(ds.is_root(i));
        assert_eq!(ds.set_size(i), 1);
    }
}

#[test]
fn test_all_union() {
    let mut ds = DisjointSet::new(100);
    
    // Union all elements into one set
    for i in 0..99 {
        ds.union(i, i + 1);
    }
    
    assert_eq!(ds.set_count(), 1);
    assert_eq!(ds.largest_set_size(), 100);
    
    // All elements are connected
    for i in 0..100 {
        for j in 0..100 {
            assert!(ds.connected(i, j));
        }
    }
}

#[test]
fn test_union_pairs() {
    let mut ds = DisjointSet::new(10);
    
    // Create pairs: (0,1), (2,3), (4,5), (6,7), (8,9)
    for i in 0..5 {
        ds.union(2 * i, 2 * i + 1);
    }
    
    assert_eq!(ds.set_count(), 5);
    
    // Check pair connectivity
    for i in 0..5 {
        assert!(ds.connected(2 * i, 2 * i + 1));
    }
    
    // Check non-pair connectivity
    assert!(!ds.connected(0, 2));
    assert!(!ds.connected(1, 3));
    assert!(!ds.connected(4, 6));
}

#[test]
fn test_set_size_consistency() {
    let mut ds = DisjointSet::new(10);
    
    ds.union(0, 1);
    ds.union(2, 3);
    ds.union(4, 5);
    ds.union(6, 7);
    ds.union(8, 9);
    
    // Merge some sets
    ds.union(0, 2);
    ds.union(4, 6);
    ds.union(0, 4);
    
    // Check that all elements in the merged set have the same size
    let size = ds.set_size(0);
    for i in 0..8 {
        assert_eq!(ds.set_size(i), size);
    }
    assert_eq!(size, 8);
    
    // The last pair should still be separate
    assert_eq!(ds.set_size(8), 2);
}

#[test]
fn test_elements_in_set_large() {
    let mut ds = DisjointSet::new(100);
    
    // Create one large set
    for i in 0..50 {
        ds.union(i, i + 1);
    }
    
    let set = ds.elements_in_set(0);
    assert_eq!(set.len(), 51);
    
    // All elements 0-50 should be in the set
    for i in 0..=50 {
        assert!(set.contains(&i));
    }
    
    // Elements 51-99 should not be in the set
    for i in 51..100 {
        assert!(!set.contains(&i));
    }
}

#[test]
fn test_all_sets_complete() {
    let mut ds = DisjointSet::new(10);
    
    ds.union(0, 1);
    ds.union(2, 3);
    ds.union(4, 5);
    
    let sets = ds.all_sets();
    
    // Should have 7 sets: {0,1}, {2,3}, {4,5}, {6}, {7}, {8}, {9}
    assert_eq!(sets.len(), 7);
    
    // Total elements should be 10
    let total: usize = sets.iter().map(|s: &HashSet<usize>| s.len()).sum();
    assert_eq!(total, 10);
    
    // Each element should appear exactly once
    let mut seen = vec![false; 10];
    for set in &sets {
        for &elem in set {
            assert!(!seen[elem]);
            seen[elem] = true;
        }
    }
    assert!(seen.iter().all(|&x| x));
}

#[test]
fn test_reset_after_operations() {
    let mut ds = DisjointSet::new(100);
    
    // Create complex structure
    for i in 0..99 {
        ds.union(i, i + 1);
    }
    
    assert_eq!(ds.set_count(), 1);
    
    ds.reset();
    
    assert_eq!(ds.set_count(), 100);
    for i in 0..100 {
        for j in 0..100 {
            if i != j {
                assert!(!ds.connected(i, j));
            }
        }
    }
}

#[test]
fn test_batch_union_empty() {
    let mut ds = DisjointSet::new(5);
    
    let merged = ds.batch_union(vec![]);
    assert_eq!(merged, 0);
    assert_eq!(ds.set_count(), 5);
}

#[test]
fn test_batch_union_complete() {
    let mut ds = DisjointSet::new(100);
    
    let pairs: Vec<_> = (0..99).map(|i| (i, i + 1)).collect();
    let merged = ds.batch_union(pairs);
    
    assert_eq!(merged, 99);
    assert_eq!(ds.set_count(), 1);
}

#[test]
fn test_batch_union_duplicates() {
    let mut ds = DisjointSet::new(5);
    
    let merged = ds.batch_union(vec![
        (0, 1), (0, 1), (0, 1), // Same union multiple times
        (2, 3), (3, 2), // Reverse order, but same set
    ]);
    
    assert_eq!(merged, 2); // Only 2 unique unions
    assert_eq!(ds.set_count(), 3);
}

#[test]
fn test_labeled_dynamic_add() {
    let mut ds: LabeledDisjointSet<String> = LabeledDisjointSet::new();
    
    // Add elements dynamically
    ds.union(&"a".to_string(), &"b".to_string());
    assert_eq!(ds.len(), 2);
    
    ds.union(&"c".to_string(), &"d".to_string());
    assert_eq!(ds.len(), 4);
    
    ds.union(&"b".to_string(), &"c".to_string());
    assert_eq!(ds.len(), 4);
    
    assert!(ds.connected(&"a".to_string(), &"d".to_string()));
    assert_eq!(ds.set_count(), 1);
}

#[test]
fn test_labeled_numeric_keys() {
    let mut ds = LabeledDisjointSet::from_elements(vec![1, 2, 3, 4, 5]);
    
    ds.union(&1, &2);
    ds.union(&3, &4);
    ds.union(&2, &3);
    
    assert!(ds.connected(&1, &4));
    assert!(!ds.connected(&1, &5));
    
    let sets = ds.all_sets();
    assert_eq!(sets.len(), 2);
}

#[test]
fn test_labeled_all_sets() {
    let mut ds = LabeledDisjointSet::from_elements(vec!["a", "b", "c", "d", "e"]);
    
    ds.union(&"a", &"b");
    ds.union(&"c", &"d");
    
    let sets = ds.all_sets();
    assert_eq!(sets.len(), 3);
    
    // Find which set each element belongs to
    let a_set = sets.iter().find(|s: &&HashSet<&str>| s.contains(&"a")).unwrap();
    assert!(a_set.contains(&"b"));
    assert!(!a_set.contains(&"c"));
    
    let c_set = sets.iter().find(|s: &&HashSet<&str>| s.contains(&"c")).unwrap();
    assert!(c_set.contains(&"d"));
}

#[test]
fn test_is_root() {
    let mut ds = DisjointSet::new(5);
    
    // Initially all are roots
    for i in 0..5 {
        assert!(ds.is_root(i));
    }
    
    ds.union(0, 1);
    
    // Only one of 0 or 1 is root now
    let roots_count = (0..5).filter(|&i| ds.is_root(i)).count();
    assert_eq!(roots_count, 4);
}

#[test]
fn test_smallest_non_trivial_set() {
    let mut ds = DisjointSet::new(10);
    
    // No non-trivial sets initially
    assert_eq!(ds.smallest_non_trivial_set_size(), None);
    
    ds.union(0, 1);
    assert_eq!(ds.smallest_non_trivial_set_size(), Some(2));
    
    ds.union(2, 3);
    ds.union(3, 4);
    assert_eq!(ds.smallest_non_trivial_set_size(), Some(2));
    
    ds.union(0, 2);
    assert_eq!(ds.smallest_non_trivial_set_size(), Some(5));
}

#[test]
fn test_from_components_empty() {
    let mut ds = DisjointSet::from_components(5, &vec![]);
    
    assert_eq!(ds.set_count(), 5);
    for i in 0..5 {
        assert_eq!(ds.set_size(i), 1);
    }
}

#[test]
fn test_from_components_singletons() {
    let ds = DisjointSet::from_components(3, &vec![vec![0], vec![1], vec![2]]);
    assert_eq!(ds.set_count(), 3);
}

#[test]
fn test_from_components_mixed() {
    let components = vec![
        vec![0, 1, 2, 3],
        vec![5, 6],
        vec![8, 9],
    ];
    let mut ds = DisjointSet::from_components(10, &components);
    
    assert_eq!(ds.set_count(), 5); // 3 components + 2 singletons (4, 7)
    assert!(ds.connected(0, 3));
    assert!(ds.connected(5, 6));
    assert!(!ds.connected(0, 5));
    assert!(!ds.connected(4, 7));
}

#[test]
fn test_union_by_rank_vs_size() {
    // Create two sets with different strategies
    let mut ds_rank = DisjointSet::with_strategy(8, UnionStrategy::ByRank);
    let mut ds_size = DisjointSet::with_strategy(8, UnionStrategy::BySize);
    
    // Create the same structure in both
    for i in 0..7 {
        ds_rank.union(i, i + 1);
        ds_size.union(i, i + 1);
    }
    
    // Both should have the same final connectivity
    assert_eq!(ds_rank.set_count(), ds_size.set_count());
    assert!(ds_rank.connected(0, 7));
    assert!(ds_size.connected(0, 7));
}

#[test]
fn test_union_returns_correct_value() {
    let mut ds = DisjointSet::new(5);
    
    // First union should return true
    assert!(ds.union(0, 1));
    
    // Second union of same elements should return false
    assert!(!ds.union(0, 1));
    assert!(!ds.union(1, 0));
    
    // Union with new element should return true
    assert!(ds.union(1, 2));
    
    // Elements now in same set
    assert!(!ds.union(0, 2));
}

#[test]
fn test_large_scale() {
    let n = 10000;
    let mut ds = DisjointSet::new(n);
    
    // Create random-ish unions
    for i in 0..n / 2 {
        ds.union(i * 2, i * 2 + 1);
    }
    
    assert_eq!(ds.set_count(), n / 2);
    
    // Merge pairs into quads
    for i in 0..n / 4 {
        ds.union(i * 4, i * 4 + 2);
    }
    
    assert_eq!(ds.set_count(), n / 4);
    
    // Check connectivity within quads
    for i in 0..n / 4 {
        let base = i * 4;
        for j in 0..4 {
            for k in 0..4 {
                assert!(ds.connected(base + j, base + k));
            }
        }
    }
}

#[test]
fn test_root_mapping() {
    let mut ds = DisjointSet::new(5);
    
    ds.union(0, 1);
    ds.union(2, 3);
    ds.union(1, 2);
    
    let mapping = ds.root_mapping();
    
    // Elements 0-3 should have the same root
    assert_eq!(mapping[0], mapping[1]);
    assert_eq!(mapping[1], mapping[2]);
    assert_eq!(mapping[2], mapping[3]);
    
    // Element 4 should have its own root
    assert_ne!(mapping[0], mapping[4]);
}

#[test]
fn test_clone() {
    let mut ds = DisjointSet::new(5);
    ds.union(0, 1);
    ds.union(2, 3);
    
    let cloned = ds.clone();
    
    assert_eq!(cloned.len(), ds.len());
    assert_eq!(cloned.set_count(), ds.set_count());
}

#[test]
fn test_strategy_default() {
    let ds = DisjointSet::new(5);
    assert_eq!(ds.strategy(), UnionStrategy::ByRank);
}

#[test]
fn test_labeled_default() {
    let ds: LabeledDisjointSet<i32> = LabeledDisjointSet::default();
    assert!(ds.is_empty());
}

#[test]
fn test_labeled_set_size_none() {
    let mut ds: LabeledDisjointSet<String> = LabeledDisjointSet::new();
    assert_eq!(ds.set_size(&"nonexistent".to_string()), None);
}

#[test]
fn test_labeled_elements_in_set_none() {
    let mut ds: LabeledDisjointSet<String> = LabeledDisjointSet::new();
    assert_eq!(ds.elements_in_set(&"nonexistent".to_string()), None);
}

#[test]
fn test_labeled_connected_nonexistent() {
    let mut ds: LabeledDisjointSet<String> = LabeledDisjointSet::new();
    assert!(!ds.connected(&"a".to_string(), &"b".to_string()));
}

#[test]
fn test_find_no_compress_structure() {
    let mut ds = DisjointSet::new(5);
    
    // Create a tall tree without path compression
    ds.union(0, 1);
    ds.union(1, 2);
    ds.union(2, 3);
    ds.union(3, 4);
    
    // find_no_compress shouldn't modify parent pointers
    let root = ds.find_no_compress(4);
    
    // The tree structure should still exist (not compressed)
    // Note: This is hard to test directly without internal access,
    // but we can verify the result is correct
    assert_eq!(root, ds.find_no_compress(0));
}

#[test]
fn test_edges_with_invalid_indices() {
    // from_edges should ignore invalid indices
    let edges = vec![(0, 1), (5, 6), (2, 10)]; // 5, 6, 10 are out of bounds
    let mut ds = DisjointSet::from_edges(5, edges);
    
    assert!(ds.connected(0, 1));
    assert_eq!(ds.set_count(), 4); // {0,1}, {2}, {3}, {4}
}

#[test]
fn test_consecutive_unions_same_elements() {
    let mut ds = DisjointSet::new(5);
    
    ds.union(0, 1);
    let size1 = ds.set_size(0);
    
    ds.union(0, 1);
    let size2 = ds.set_size(0);
    
    assert_eq!(size1, size2);
}

#[test]
fn test_chain_vs_star() {
    // Test that both chain and star union patterns give same connectivity
    
    // Chain: 0-1-2-3-4
    let mut ds_chain = DisjointSet::new(5);
    for i in 0..4 {
        ds_chain.union(i, i + 1);
    }
    
    // Star: 0 is center, 1-4 connect to 0
    let mut ds_star = DisjointSet::new(5);
    for i in 1..5 {
        ds_star.union(0, i);
    }
    
    // Both should have same connectivity
    assert_eq!(ds_chain.set_count(), ds_star.set_count());
    
    for i in 0..5 {
        for j in 0..5 {
            assert_eq!(ds_chain.connected(i, j), ds_star.connected(i, j));
        }
    }
}