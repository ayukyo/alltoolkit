//! Example: Basic segment tree usage

use segment_tree_utils::{SegmentTree, Sum, Min, Max};

fn main() {
    // ── Sum tree ──────────────────────────────────────────────
    let arr = [1, 3, 2, 7, 5, 9, 4];
    let mut seg: SegmentTree<Sum> = SegmentTree::from_slice(&arr);

    println!("Array: {:?}", &arr);
    println!("Sum of all: {}", seg.query(0..7));
    println!("Sum [0,3): {}", seg.query(0..3)); // 1+3+2 = 6

    // Range add: add 10 to indices [1, 4)
    seg.update_range(1..4, 10);
    println!("\nAfter adding 10 to indices [1,4):");
    println!("Sum [0,7): {}", seg.query(0..7)); // was 31, now 43

    // Point update
    seg.point_set(2, 100);
    println!("After setting index 2 to 100:");
    println!("Sum [0,7): {}", seg.query(0..7));

    // ── Min tree ──────────────────────────────────────────────
    let arr2 = [5, 2, 8, 1, 9, 3, 7];
    let mut seg_min: SegmentTree<Min> = SegmentTree::from_slice(&arr2);
    println!("\nMin tree on {:?}", &arr2);
    println!("Min of all: {}", seg_min.query(0..7));
    println!("Min [0,3): {}", seg_min.query(0..3));

    // ── Max tree ──────────────────────────────────────────────
    let mut seg_max: SegmentTree<Max> = SegmentTree::from_slice(&arr2);
    println!("\nMax tree on {:?}", &arr2);
    println!("Max of all: {}", seg_max.query(0..7));
    println!("Max [4,7): {}", seg_max.query(4..7));
}
