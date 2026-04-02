/**
 * AllToolkit - Rust Collection Utilities 使用示例
 * 
 * 演示 collection_utils 模块的各种用法
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

// 假设 collection_utils.rs 在同一目录下
// 在实际项目中，应将其作为模块导入：
// mod collection_utils;
// use collection_utils::*;

use std::collections::HashMap;

fn main() {
    println!("=== AllToolkit Rust Collection Utils 示例 ===\n");

    // 1. 去重示例
    println!("1. 去重 (deduplicate)");
    let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
    println!("   原始: {:?}", nums);
    let unique = deduplicate(nums);
    println!("   去重后: {:?}\n", unique);

    // 2. 分组示例
    println!("2. 分组 (group_by)");
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let grouped = group_by(numbers, |n| {
        if n % 3 == 0 { "divisible_by_3" }
        else if n % 2 == 0 { "even" }
        else { "odd" }
    });
    println!("   按类型分组: {:?}\n", grouped);

    // 3. 查找索引示例
    println!("3. 查找索引");
    let data = vec!["apple", "banana", "cherry", "date", "elderberry"];
    if let Some(idx) = find_index(&data, |s| s.starts_with("c")) {
        println!("   第一个以 'c' 开头的元素索引: {}", idx);
    }
    let indices = find_all_indices(&data, |s| s.contains("a"));
    println!("   包含 'a' 的所有元素索引: {:?}\n", indices);

    // 4. 集合运算示例
    println!("4. 集合运算");
    let a = vec![1, 2, 3, 4, 5];
    let b = vec![4, 5, 6, 7, 8];
    println!("   A: {:?}", a);
    println!("   B: {:?}", b);
    println!("   交集: {:?}", intersect(a.clone(), b.clone()));
    println!("   并集: {:?}", union(a.clone(), b.clone()));
    println!("   差集 (A-B): {:?}\n", difference(a.clone(), b.clone()));

    // 5. 分块示例
    println!("5. 分块 (chunk / split_into)");
    let items = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("   原始: {:?}", items);
    println!("   每块3个: {:?}", chunk(items.clone(), 3));
    println!("   分成3组: {:?}\n", split_into(items.clone(), 3));

    // 6. 频率统计示例
    println!("6. 频率统计");
    let votes = vec!["apple", "banana", "apple", "cherry", "banana", "apple"];
    let counts = count_occurrences(votes);
    println!("   投票统计: {:?}", counts);
    if let Some((winner, count)) = most_frequent(counts.keys().cloned().collect::<Vec<_>>()) {
        println!("   最高频: {:?} ({}票)", winner, count);
    }
    println!();

    // 7. 分区示例
    println!("7. 分区 (partition)");
    let scores = vec![85, 92, 78, 65, 88, 91, 73, 96];
    let (pass, fail) = partition(scores, |&s| s >= 80);
    println!("   及格 (>=80): {:?}", pass);
    println!("   不及格 (<80): {:?}\n", fail);

    // 8. 扁平化示例
    println!("8. 扁平化 (flatten)");
    let matrix = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    println!("   二维数组: {:?}", matrix);
    println!("   扁平化后: {:?}\n", flatten(matrix));

    // 9. 排序示例
    println!("9. 排序");
    let users = vec![
        ("Alice", 25),
        ("Bob", 30),
        ("Charlie", 20),
        ("Diana", 28),
    ];
    println!("   原始: {:?}", users);
    let by_age = sort_by_key(users.clone(), |u| u.1);
    println!("   按年龄升序: {:?}", by_age);
    let by_age_desc = sort_by_key_desc(users.clone(), |u| u.1);
    println!("   按年龄降序: {:?}\n", by_age_desc);

    // 10. 去重检查示例
    println!("10. 重复检查");
    let ids1 = vec![101, 102, 103, 104];
    let ids2 = vec![101, 102, 101, 103];
    println!("   {:?} 有重复? {}", ids1, has_duplicates(&ids1));
    println!("   {:?} 有重复? {}\n", ids2, has_duplicates(&ids2));

    println!("=== 示例结束 ===");
}

// =============================================================================
// 以下为简化版函数实现，实际使用时请导入 collection_utils 模块
// =============================================================================

use std::collections::HashSet;
use std::hash::Hash;

fn deduplicate<T: Clone + Eq + Hash>(vec: Vec<T>) -> Vec<T> {
    let mut seen = HashSet::new();
    let mut result = Vec::new();
    for item in vec {
        if seen.insert(item.clone()) {
            result.push(item);
        }
    }
    result
}

fn group_by<T, K: Eq + Hash>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> HashMap<K, Vec<T>> {
    let mut groups: HashMap<K, Vec<T>> = HashMap::new();
    for item in vec {
        let key = key_fn(&item);
        groups.entry(key).or_insert_with(Vec::new).push(item);
    }
    groups
}

fn find_index<T>(vec: &[T], predicate: impl Fn(&T) -> bool) -> Option<usize> {
    vec.iter().position(predicate)
}

fn find_all_indices<T>(vec: &[T], predicate: impl Fn(&T) -> bool) -> Vec<usize> {
    vec.iter()
        .enumerate()
        .filter(|(_, item)| predicate(item))
        .map(|(idx, _)| idx)
        .collect()
}

fn intersect<T: Clone + Eq + Hash>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let set_b: HashSet<T> = b.into_iter().collect();
    let set_a: HashSet<T> = a.into_iter().collect();
    set_a.intersection(&set_b).cloned().collect()
}

fn union<T: Clone + Eq + Hash>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let set_a: HashSet<T> = a.into_iter().collect();
    let set_b: HashSet<T> = b.into_iter().collect();
    set_a.union(&set_b).cloned().collect()
}

fn difference<T: Clone + Eq + Hash>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let set_b: HashSet<T> = b.into_iter().collect();
    a.into_iter()
        .filter(|item| !set_b.contains(item))
        .collect::<HashSet<T>>()
        .into_iter()
        .collect()
}

fn chunk<T: Clone>(vec: Vec<T>, size: usize) -> Vec<Vec<T>> {
    if size == 0 {
        return Vec::new();
    }
    let mut result = Vec::new();
    let mut current = Vec::new();
    for item in vec {
        current.push(item);
        if current.len() == size {
            result.push(current.clone());
            current.clear();
        }
    }
    if !current.is_empty() {
        result.push(current);
    }
    result
}

fn split_into<T: Clone>(vec: Vec<T>, num_chunks: usize) -> Vec<Vec<T>> {
    if num_chunks == 0 || vec.is_empty() {
        return Vec::new();
    }
    let len = vec.len();
    let chunk_size = (len + num_chunks - 1) / num_chunks;
    let mut result = Vec::new();
    let mut iter = vec.into_iter();
    for i in 0..num_chunks {
        let size = if i == num_chunks - 1 {
            len.saturating_sub(i * chunk_size)
        } else {
            chunk_size.min(len - i * chunk_size)
        };
        let chunk: Vec<T> = iter.by_ref().take(size).collect();
        if !chunk.is_empty() {
            result.push(chunk);
        }
    }
    result
}

fn count_occurrences<T: Eq + Hash>(vec: Vec<T>) -> HashMap<T, usize> {
    let mut counts: HashMap<T, usize> = HashMap::new();
    for item in vec {
        *counts.entry(item).or_insert(0) += 1;
    }
    counts
}

fn partition<T>(vec: Vec<T>, predicate: impl Fn(&T) -> bool) -> (Vec<T>, Vec<T>) {
    let mut matched = Vec::new();
    let mut unmatched = Vec::new();
    for item in vec {
        if predicate(&item) {
            matched.push(item);
        } else {
            unmatched.push(item);
        }
    }
    (matched, unmatched)
}

fn flatten<T: Clone>(nested: Vec<Vec<T>>) -> Vec<T> {
    nested.into_iter().flatten().collect()
}

fn has_duplicates<T: Eq + Hash>(vec: &[T]) -> bool {
    let mut seen = HashSet::new();
    for item in vec {
        if !seen.insert(item) {
            return true;
        }
    }
    false
}

fn most_frequent<T: Eq + Hash + Clone>(vec: Vec<T>) -> Option<(T, usize)> {
    let counts = count_occurrences(vec);
    counts.into_iter().max_by_key(|&(_, count)| count)
}

fn sort_by_key<T: Clone, K: Ord>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> Vec<T> {
    let mut result = vec;
    result.sort_by_key(key_fn);
    result
}

fn sort_by_key_desc<T: Clone, K: Ord>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> Vec<T> {
    let mut result = vec;
    result.sort_by(|a, b| key_fn(b).cmp(&key_fn(a)));
    result
}
