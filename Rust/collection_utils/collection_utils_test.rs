/**
 * AllToolkit - Rust Collection Utilities Test
 * 
 * 集合工具模块单元测试
 * 覆盖正常场景、边界值、异常情况
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

// Include the module under test
mod mod;
use mod::*;

// =============================================================================
// 去重测试
// =============================================================================

#[test]
fn test_deduplicate_basic() {
    let nums = vec![1, 2, 2, 3, 3, 3, 4];
    assert_eq!(deduplicate(nums), vec![1, 2, 3, 4]);
}

#[test]
fn test_deduplicate_empty() {
    let empty: Vec<i32> = vec![];
    assert_eq!(deduplicate(empty), Vec::<i32>::new());
}

#[test]
fn test_deduplicate_no_duplicates() {
    let nums = vec![1, 2, 3, 4, 5];
    assert_eq!(deduplicate(nums), vec![1, 2, 3, 4, 5]);
}

#[test]
fn test_deduplicate_all_same() {
    let nums = vec![1, 1, 1, 1, 1];
    assert_eq!(deduplicate(nums), vec![1]);
}

#[test]
fn test_deduplicate_string() {
    let words = vec!["a", "b", "a", "c", "b"];
    assert_eq!(deduplicate(words), vec!["a", "b", "c"]);
}

// =============================================================================
// 分组测试
// =============================================================================

#[test]
fn test_group_by_even_odd() {
    let nums = vec![1, 2, 3, 4, 5, 6];
    let grouped = group_by(nums, |n| if n % 2 == 0 { "even" } else { "odd" });
    assert_eq!(grouped.get("even").unwrap(), &vec![2, 4, 6]);
    assert_eq!(grouped.get("odd").unwrap(), &vec![1, 3, 5]);
}

#[test]
fn test_group_by_empty() {
    let empty: Vec<i32> = vec![];
    let grouped: std::collections::HashMap<&str, Vec<i32>> = group_by(empty, |_| "key");
    assert!(grouped.is_empty());
}

#[test]
fn test_group_by_all_same_key() {
    let nums = vec![1, 2, 3, 4, 5];
    let grouped = group_by(nums, |_| "all");
    assert_eq!(grouped.get("all").unwrap().len(), 5);
}

// =============================================================================
// 查找索引测试
// =============================================================================

#[test]
fn test_find_index_found() {
    let nums = vec![1, 2, 3, 4, 5];
    assert_eq!(find_index(&nums, |n| *n > 3), Some(3));
}

#[test]
fn test_find_index_not_found() {
    let nums = vec![1, 2, 3, 4, 5];
    assert_eq!(find_index(&nums, |n| *n > 10), None);
}

#[test]
fn test_find_index_empty() {
    let empty: Vec<i32> = vec![];
    assert_eq!(find_index(&empty, |_| true), None);
}

#[test]
fn test_find_index_first() {
    let nums = vec![1, 2, 3, 4, 5];
    assert_eq!(find_index(&nums, |n| *n == 1), Some(0));
}

#[test]
fn test_find_last_index_found() {
    let nums = vec![1, 2, 3, 2, 5];
    assert_eq!(find_last_index(&nums, |n| *n == 2), Some(3));
}

#[test]
fn test_find_last_index_not_found() {
    let nums = vec![1, 2, 3, 4, 5];
    assert_eq!(find_last_index(&nums, |n| *n == 10), None);
}

#[test]
fn test_find_all_indices() {
    let nums = vec![1, 2, 3, 2, 5, 2];
    assert_eq!(find_all_indices(&nums, |n| *n == 2), vec![1, 3, 5]);
}

#[test]
fn test_find_all_indices_none() {
    let nums = vec![1, 2, 3, 4, 5];
    assert_eq!(find_all_indices(&nums, |n| *n == 10), Vec::<usize>::new());
}

// =============================================================================
// 集合运算测试
// =============================================================================

#[test]
fn test_intersect_basic() {
    let a = vec![1, 2, 3, 4];
    let b = vec![3, 4, 5, 6];
    let result = intersect(a, b);
    assert!(result.contains(&3));
    assert!(result.contains(&4));
    assert_eq!(result.len(), 2);
}

#[test]
fn test_intersect_empty() {
    let a = vec![1, 2, 3];
    let b = vec![4, 5, 6];
    let result = intersect(a, b);
    assert!(result.is_empty());
}

#[test]
fn test_intersect_same() {
    let a = vec![1, 2, 3];
    let b = vec![1, 2, 3];
    let result = intersect(a, b);
    assert_eq!(result.len(), 3);
}

#[test]
fn test_union_basic() {
    let a = vec![1, 2, 3];
    let b = vec![3, 4, 5];
    let result = union(a, b);
    assert_eq!(result.len(), 5);
}

#[test]
fn test_union_empty() {
    let a: Vec<i32> = vec![];
    let b = vec![1, 2, 3];
    let result = union(a, b);
    assert_eq!(result.len(), 3);
}

#[test]
fn test_difference_basic() {
    let a = vec![1, 2, 3, 4];
    let b = vec![3, 4, 5, 6];
    let result = difference(a, b);
    assert!(result.contains(&1));
    assert!(result.contains(&2));
    assert!(!result.contains(&3));
}

#[test]
fn test_difference_empty() {
    let a = vec![1, 2, 3];
    let b = vec![1, 2, 3];
    let result = difference(a, b);
    assert!(result.is_empty());
}

// =============================================================================
// 分块测试
// =============================================================================

#[test]
fn test_chunk_basic() {
    let nums = vec![1, 2, 3, 4, 5, 6, 7];
    assert_eq!(chunk(nums, 3), vec![vec![1, 2, 3], vec![4, 5, 6], vec![7]]);
}

#[test]
fn test_chunk_exact() {
    let nums = vec![1, 2, 3, 4, 5, 6];
    assert_eq!(chunk(nums, 3), vec![vec![1, 2, 3], vec![4, 5, 6]]);
}

#[test]
fn test_chunk_size_one() {
    let nums = vec![1, 2, 3];
    assert_eq!(chunk(nums, 1), vec![vec![1], vec![2], vec![3]]);
}

#[test]
fn test_chunk_empty() {
    let empty: Vec<i32> = vec![];
    assert_eq!(chunk(empty, 3), Vec::<Vec<i32>>::new());
}

#[test]
fn test_chunk_zero_size() {
    let nums = vec![1, 2, 3];
    assert_eq!(chunk(nums, 0), Vec::<Vec<i32>>::new());
}

#[test]
fn test_split_into_basic() {
    let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let chunks = split_into(nums, 3);
    assert_eq!(chunks.len(), 3);
    assert_eq!(chunks[0].len(), 4);
    assert_eq!(chunks[1].len(), 3);
    assert_eq!(chunks[2].len(), 3);
}

#[test]
fn test_split_into_empty() {
    let empty: Vec<i32> = vec![];
    assert_eq!(split_into(empty, 3), Vec::<Vec<i32>>::new());
}

#[test]
fn test_split_into_zero() {
    let nums = vec![1, 2, 3];
    assert_eq!(split_into(nums, 0), Vec::<Vec<i32>>::new());
}

// =============================================================================
// 频率统计测试
// =============================================================================

#[test]
fn test_count_occurrences_basic() {
    let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
    let counts = count_occurrences(nums);
    assert_eq!(counts.get(&1), Some(&1));
    assert_eq!(counts.get(&2), Some(&2));
    assert_eq!(counts.get(&3), Some(&3));
    assert_eq!(counts.get(&4), Some(&4));
}

#[test]
fn test_count_occurrences_empty() {
    let empty: Vec<i32> = vec![];
    let counts = count_occurrences(empty);
    assert!(counts.is_empty());
}

#[test]
fn test_most_frequent_basic() {
    let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
    assert_eq!(most_frequent(nums), Some((4, 4)));
}

#[test]
fn test_most_frequent_empty() {
    let empty: Vec<i32> = vec![];
    assert_eq!(most_frequent(empty), None);
}

#[test]
fn test_most_frequent_tie() {
    let nums = vec![1, 1, 2, 2];
    let result = most_frequent(nums);
    assert!(result == Some((1, 2)) || result == Some((2, 2)));
}

#[test]
fn test_top_frequent_basic() {
    let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
    let top2 = top_frequent(nums, 2);
    assert_eq!(top2.len(), 2);
    assert_eq!(top2[0], (4, 4));
    assert_eq!(top2[1], (3, 3));
}

#[test]
fn test_top_frequent_more_than_available() {
    let nums = vec![1, 2, 3];
    let top10 = top_frequent(nums, 10);
    assert_eq!(top10.len(), 3);
}

// =============================================================================
// 分区与扁平化测试
// =============================================================================

#[test]
fn test_partition_basic() {
    let nums = vec![1, 2, 3, 4, 5, 6];
    let (even, odd) = partition(nums, |n| n % 2 == 0);
    assert_eq!(even, vec![2, 4, 6]);
    assert_eq!(odd, vec![1, 3, 5]);
}

#[test]
fn test_partition_empty() {
    let empty: Vec<i32> = vec![];
    let (matched, unmatched) = partition(empty, |_| true);
    assert!(matched.is_empty());
    assert!(unmatched.is_empty());
}

#[test]
fn test_partition_all_match() {
    let nums = vec![2, 4, 6, 8];
    let (even, odd) = partition(nums, |n| n % 2 == 0);
    assert_eq!(even.len(), 4);
    assert!(odd.is_empty());
}

#[test]
fn test_flatten_basic() {
    let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
    assert_eq!(flatten(nested), vec![1, 2, 3, 4, 5]);
}

#[test]
fn test_flatten_empty() {
    let nested: Vec<Vec<i32>> = vec![];
    assert_eq!(flatten(nested), Vec::<i32>::new());
}

#[test]
fn test_flatten_empty_inner() {
    let nested = vec![vec![], vec![1, 2], vec![]];
    assert_eq!(flatten(nested), vec![1, 2]);
}

// =============================================================================
// 重复检查测试
// =============================================================================

#[test]
fn test_has_duplicates_true() {
    assert!(has_duplicates(&[1, 2, 2, 3]));
}

#[test]
fn test_has_duplicates_false() {
    assert!(!has_duplicates(&[1, 2, 3, 4]));
}

#[test]
fn test_has_duplicates_empty() {
    assert!(!has_duplicates(&[] as &[i32]));
}

#[test]
fn test_has_duplicates_single() {
    assert!(!has_duplicates(&[1]));
}

// =============================================================================
// 唯一元素带索引测试
// =============================================================================

#[test]
fn test_unique_with_index_basic() {
    let nums = vec![1, 2, 2, 3, 3, 3, 4];
    let result = unique_with_index(nums);
    assert_eq!(result, vec![(1, 0), (2, 1), (3, 3), (4, 6)]);
}

#[test]
fn test_unique_with_index_empty() {
    let empty: Vec<i32> = vec![];
    assert_eq!(unique_with_index(empty), Vec::<(i32, usize)>::new());
}

#[test]
fn test_unique_with_index_no_duplicates() {
    let nums = vec![1, 2, 3, 4];
    let result = unique_with_index(nums);
    assert_eq!(result, vec![(1, 0), (2, 1), (3, 2), (4, 3)]);
}

// =============================================================================
// HashMap 转换测试
// =============================================================================

#[test]
fn test_to_map_basic() {
    let users = vec![("alice", 25), ("bob", 30)];
    let map = to_map(users, |u| u.0.to_string());
    assert_eq!(map.get("alice"), Some(&("alice", 25)));
    assert_eq!(map.get("bob"), Some(&("bob", 30)));
}

#[test]
fn test_to_map_empty() {
    let empty: Vec<(&str, i32)> = vec![];
    let map = to_map(empty, |u| u.0.to_string());
    assert!(map.is_empty());
}

// =============================================================================
// 排序测试
// =============================================================================

#[test]
fn test_sort_by_key_ascending() {
    let users = vec![("bob", 30), ("alice", 25), ("charlie", 35)];
    let sorted = sort_by_key(users, |u| u.1);
    assert_eq!(sorted, vec![("alice", 25), ("bob", 30), ("charlie", 35)]);
}

#[test]
fn test_sort_by_key_descending() {
    let nums = vec![3, 1, 4, 1, 5, 9, 2, 6];
    let sorted = sort_by_key_desc(nums, |n| *n);
    assert_eq!(sorted, vec![9, 6, 5, 4, 3, 2, 1, 1]);
}

#[test]
fn test_sort_by_key_empty() {
    let empty: Vec<i32> = vec![];
    let sorted = sort_by_key(empty, |n| *n);
    assert!(sorted.is_empty());
}

#[test]
fn test_sort_by_key_stable() {
    let items = vec![("a", 1), ("b", 1), ("c", 2)];
    let sorted = sort_by_key(items.clone(), |item| item.1);
    // Stable sort preserves order of equal elements
    assert_eq!(sorted[0].0, "a");
    assert_eq!(sorted[1].0, "b");
}