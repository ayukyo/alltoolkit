/**
 * AllToolkit - Rust Collection Utilities
 * 
 * 通用集合/数组工具模块，提供常用的集合操作、分组、去重、查找等功能。
 * 零依赖，仅使用 Rust 标准库。
 * 支持 Rust 1.70+
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

use std::collections::{HashMap, HashSet};
use std::hash::Hash;

// =============================================================================
// 通用集合工具函数
// =============================================================================

/**
 * 从向量中移除重复元素，保持原有顺序
 * 
 * # 参数
 * * `vec` - 输入向量
 * 
 * # 返回值
 * 去重后的新向量
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 2, 3, 3, 3, 4];
 * let unique = deduplicate(nums);
 * assert_eq!(unique, vec![1, 2, 3, 4]);
 * ```
 */
pub fn deduplicate<T: Clone + Eq + Hash>(vec: Vec<T>) -> Vec<T> {
    let mut seen = HashSet::new();
    let mut result = Vec::new();
    
    for item in vec {
        if seen.insert(item.clone()) {
            result.push(item);
        }
    }
    
    result
}

/**
 * 根据条件对向量元素进行分组
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `key_fn` - 分组键生成函数
 * 
 * # 返回值
 * HashMap，键为分组键，值为该组的元素向量
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 4, 5, 6];
 * let grouped = group_by(nums, |n| if n % 2 == 0 { "even" } else { "odd" });
 * assert_eq!(grouped.get("even").unwrap(), &vec![2, 4, 6]);
 * assert_eq!(grouped.get("odd").unwrap(), &vec![1, 3, 5]);
 * ```
 */
pub fn group_by<T, K: Eq + Hash>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> HashMap<K, Vec<T>> {
    let mut groups: HashMap<K, Vec<T>> = HashMap::new();
    
    for item in vec {
        let key = key_fn(&item);
        groups.entry(key).or_insert_with(Vec::new).push(item);
    }
    
    groups
}

/**
 * 查找向量中满足条件的第一个元素索引
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `predicate` - 条件判断函数
 * 
 * # 返回值
 * 满足条件的元素索引，未找到返回 None
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 4, 5];
 * let idx = find_index(&nums, |n| *n > 3);
 * assert_eq!(idx, Some(3));
 * ```
 */
pub fn find_index<T>(vec: &[T], predicate: impl Fn(&T) -> bool) -> Option<usize> {
    vec.iter().position(predicate)
}

/**
 * 查找向量中满足条件的最后一个元素索引
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `predicate` - 条件判断函数
 * 
 * # 返回值
 * 满足条件的最后一个元素索引，未找到返回 None
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 2, 5];
 * let idx = find_last_index(&nums, |n| *n == 2);
 * assert_eq!(idx, Some(3));
 * ```
 */
pub fn find_last_index<T>(vec: &[T], predicate: impl Fn(&T) -> bool) -> Option<usize> {
    vec.iter().rposition(predicate)
}

/**
 * 查找向量中所有满足条件的元素索引
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `predicate` - 条件判断函数
 * 
 * # 返回值
 * 满足条件的所有元素索引向量
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 2, 5, 2];
 * let indices = find_all_indices(&nums, |n| *n == 2);
 * assert_eq!(indices, vec![1, 3, 5]);
 * ```
 */
pub fn find_all_indices<T>(vec: &[T], predicate: impl Fn(&T) -> bool) -> Vec<usize> {
    vec.iter()
        .enumerate()
        .filter(|(_, item)| predicate(item))
        .map(|(idx, _)| idx)
        .collect()
}

/**
 * 获取两个向量的交集（共同元素）
 * 
 * # 参数
 * * `a` - 第一个向量
 * * `b` - 第二个向量
 * 
 * # 返回值
 * 交集元素向量（去重）
 * 
 * # 示例
 * ```
 * let a = vec![1, 2, 3, 4];
 * let b = vec![3, 4, 5, 6];
 * let intersection = intersect(a, b);
 * assert!(intersection.contains(&3));
 * assert!(intersection.contains(&4));
 * ```
 */
pub fn intersect<T: Clone + Eq + Hash>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let set_b: HashSet<T> = b.into_iter().collect();
    let set_a: HashSet<T> = a.into_iter().collect();
    
    set_a.intersection(&set_b).cloned().collect()
}

/**
 * 获取两个向量的并集
 * 
 * # 参数
 * * `a` - 第一个向量
 * * `b` - 第二个向量
 * 
 * # 返回值
 * 并集元素向量（去重）
 * 
 * # 示例
 * ```
 * let a = vec![1, 2, 3];
 * let b = vec![3, 4, 5];
 * let union = union(a, b);
 * assert_eq!(union.len(), 5);
 * ```
 */
pub fn union<T: Clone + Eq + Hash>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let set_a: HashSet<T> = a.into_iter().collect();
    let set_b: HashSet<T> = b.into_iter().collect();
    
    set_a.union(&set_b).cloned().collect()
}

/**
 * 获取在 a 中但不在 b 中的元素（差集）
 * 
 * # 参数
 * * `a` - 第一个向量
 * * `b` - 第二个向量
 * 
 * # 返回值
 * 差集元素向量
 * 
 * # 示例
 * ```
 * let a = vec![1, 2, 3, 4];
 * let b = vec![3, 4, 5, 6];
 * let diff = difference(a, b);
 * assert!(diff.contains(&1));
 * assert!(diff.contains(&2));
 * ```
 */
pub fn difference<T: Clone + Eq + Hash>(a: Vec<T>, b: Vec<T>) -> Vec<T> {
    let set_b: HashSet<T> = b.into_iter().collect();
    
    a.into_iter()
        .filter(|item| !set_b.contains(item))
        .collect::<HashSet<T>>()
        .into_iter()
        .collect()
}

/**
 * 将向量按指定大小分块
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `size` - 每块大小
 * 
 * # 返回值
 * 分块后的向量
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 4, 5, 6, 7];
 * let chunks = chunk(nums, 3);
 * assert_eq!(chunks, vec![vec![1, 2, 3], vec![4, 5, 6], vec![7]]);
 * ```
 */
pub fn chunk<T: Clone>(vec: Vec<T>, size: usize) -> Vec<Vec<T>> {
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

/**
 * 将向量按指定数量均匀分块
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `num_chunks` - 分块数量
 * 
 * # 返回值
 * 分块后的向量
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
 * let chunks = split_into(nums, 3);
 * // 结果: [[1,2,3,4], [5,6,7], [8,9,10]]
 * ```
 */
pub fn split_into<T: Clone>(vec: Vec<T>, num_chunks: usize) -> Vec<Vec<T>> {
    if num_chunks == 0 || vec.is_empty() {
        return Vec::new();
    }
    
    let len = vec.len();
    let chunk_size = (len + num_chunks - 1) / num_chunks; // 向上取整
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

/**
 * 计算向量中每个元素的出现次数
 * 
 * # 参数
 * * `vec` - 输入向量
 * 
 * # 返回值
 * HashMap，键为元素，值为出现次数
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
 * let counts = count_occurrences(nums);
 * assert_eq!(counts.get(&1), Some(&1));
 * assert_eq!(counts.get(&3), Some(&3));
 * assert_eq!(counts.get(&4), Some(&4));
 * ```
 */
pub fn count_occurrences<T: Eq + Hash>(vec: Vec<T>) -> HashMap<T, usize> {
    let mut counts: HashMap<T, usize> = HashMap::new();
    
    for item in vec {
        *counts.entry(item).or_insert(0) += 1;
    }
    
    counts
}

/**
 * 获取向量中出现频率最高的元素
 * 
 * # 参数
 * * `vec` - 输入向量
 * 
 * # 返回值
 * (元素, 次数) 元组，向量为空时返回 None
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
 * let mode = most_frequent(nums);
 * assert_eq!(mode, Some((4, 4)));
 * ```
 */
pub fn most_frequent<T: Eq + Hash + Clone>(vec: Vec<T>) -> Option<(T, usize)> {
    let counts = count_occurrences(vec);
    
    counts.into_iter()
        .max_by_key(|&(_, count)| count)
}

/**
 * 获取向量中出现频率最高的 N 个元素
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `n` - 获取数量
 * 
 * # 返回值
 * (元素, 次数) 元组向量，按频率降序排列
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
 * let top2 = top_frequent(nums, 2);
 * assert_eq!(top2, vec![(4, 4), (3, 3)]);
 * ```
 */
pub fn top_frequent<T: Eq + Hash + Clone>(vec: Vec<T>, n: usize) -> Vec<(T, usize)> {
    let counts = count_occurrences(vec);
    let mut items: Vec<(T, usize)> = counts.into_iter().collect();
    
    items.sort_by(|a, b| b.1.cmp(&a.1)); // 降序
    items.into_iter().take(n).collect()
}

/**
 * 打乱向量元素顺序（Fisher-Yates 洗牌算法）
 * 
 * # 参数
 * * `vec` - 输入向量
 * 
 * # 返回值
 * 打乱顺序后的新向量
 * 
 * # 注意
 * 此函数需要 `rand` crate，如需使用请添加依赖
 */

/**
 * 扁平化嵌套向量
 * 
 * # 参数
 * * `nested` - 嵌套向量
 * 
 * # 返回值
 * 扁平化后的向量
 * 
 * # 示例
 * ```
 * let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
 * let flat = flatten(nested);
 * assert_eq!(flat, vec![1, 2, 3, 4, 5]);
 * ```
 */
pub fn flatten<T: Clone>(nested: Vec<Vec<T>>) -> Vec<T> {
    nested.into_iter().flatten().collect()
}

/**
 * 根据条件过滤向量元素，返回满足和不满足的两组
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `predicate` - 条件判断函数
 * 
 * # 返回值
 * (满足条件的元素, 不满足条件的元素) 元组
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 3, 4, 5, 6];
 * let (even, odd) = partition(nums, |n| n % 2 == 0);
 * assert_eq!(even, vec![2, 4, 6]);
 * assert_eq!(odd, vec![1, 3, 5]);
 * ```
 */
pub fn partition<T>(vec: Vec<T>, predicate: impl Fn(&T) -> bool) -> (Vec<T>, Vec<T>) {
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

/**
 * 检查向量是否包含重复元素
 * 
 * # 参数
 * * `vec` - 输入向量
 * 
 * # 返回值
 * true 如果存在重复元素
 * 
 * # 示例
 * ```
 * let unique = vec![1, 2, 3, 4];
 * let dup = vec![1, 2, 2, 3];
 * assert!(!has_duplicates(unique));
 * assert!(has_duplicates(dup));
 * ```
 */
pub fn has_duplicates<T: Eq + Hash>(vec: &[T]) -> bool {
    let mut seen = HashSet::new();
    for item in vec {
        if !seen.insert(item) {
            return true;
        }
    }
    false
}

/**
 * 获取向量中的唯一元素及其首次出现索引
 * 
 * # 参数
 * * `vec` - 输入向量
 * 
 * # 返回值
 * (元素, 首次索引) 元组向量
 * 
 * # 示例
 * ```
 * let nums = vec![1, 2, 2, 3, 3, 3, 4];
 * let unique_with_index = unique_with_index(nums);
 * assert_eq!(unique_with_index, vec![(1, 0), (2, 1), (3, 3), (4, 6)]);
 * ```
 */
pub fn unique_with_index<T: Clone + Eq + Hash>(vec: Vec<T>) -> Vec<(T, usize)> {
    let mut seen = HashSet::new();
    let mut result = Vec::new();
    
    for (idx, item) in vec.into_iter().enumerate() {
        if seen.insert(item.clone()) {
            result.push((item, idx));
        }
    }
    
    result
}

/**
 * 将向量转换为 HashMap，使用键函数生成键
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `key_fn` - 键生成函数
 * 
 * # 返回值
 * HashMap，键为生成的键，值为原元素
 * 
 * # 注意
 * 如果多个元素生成相同的键，后面的会覆盖前面的
 * 
 * # 示例
 * ```
 * let users = vec![("alice", 25), ("bob", 30)];
 * let map = to_map(users, |u| u.0.to_string());
 * assert_eq!(map.get("alice"), Some(&("alice", 25)));
 * ```
 */
pub fn to_map<T, K: Eq + Hash>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> HashMap<K, T> {
    vec.into_iter()
        .map(|item| {
            let key = key_fn(&item);
            (key, item)
        })
        .collect()
}

/**
 * 按指定字段对向量进行排序（稳定排序）
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `key_fn` - 排序键生成函数
 * 
 * # 返回值
 * 排序后的新向量
 * 
 * # 示例
 * ```
 * let users = vec![("bob", 30), ("alice", 25), ("charlie", 35)];
 * let sorted = sort_by_key(users, |u| u.1);
 * assert_eq!(sorted, vec![("alice", 25), ("bob", 30), ("charlie", 35)]);
 * ```
 */
pub fn sort_by_key<T: Clone, K: Ord>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> Vec<T> {
    let mut result = vec;
    result.sort_by_key(key_fn);
    result
}

/**
 * 按指定字段对向量进行降序排序
 * 
 * # 参数
 * * `vec` - 输入向量
 * * `key_fn` - 排序键生成函数
 * 
 * # 返回值
 * 降序排序后的新向量
 * 
 * # 示例
 * ```
 * let nums = vec![3, 1, 4, 1, 5, 9, 2, 6];
 * let sorted = sort_by_key_desc(nums, |n| *n);
 * assert_eq!(sorted, vec![9, 6, 5, 4, 3, 2, 1, 1]);
 * ```
 */
pub fn sort_by_key_desc<T: Clone, K: Ord>(vec: Vec<T>, key_fn: impl Fn(&T) -> K) -> Vec<T> {
    let mut result = vec;
    result.sort_by(|a, b| key_fn(b).cmp(&key_fn(a)));
    result
}

// =============================================================================
// 测试模块
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deduplicate() {
        let nums = vec![1, 2, 2, 3, 3, 3, 4];
        assert_eq!(deduplicate(nums), vec![1, 2, 3, 4]);
    }

    #[test]
    fn test_group_by() {
        let nums = vec![1, 2, 3, 4, 5, 6];
        let grouped = group_by(nums, |n| if n % 2 == 0 { "even" } else { "odd" });
        assert_eq!(grouped.get("even").unwrap(), &vec![2, 4, 6]);
        assert_eq!(grouped.get("odd").unwrap(), &vec![1, 3, 5]);
    }

    #[test]
    fn test_find_index() {
        let nums = vec![1, 2, 3, 4, 5];
        assert_eq!(find_index(&nums, |n| *n > 3), Some(3));
        assert_eq!(find_index(&nums, |n| *n > 10), None);
    }

    #[test]
    fn test_intersect() {
        let a = vec![1, 2, 3, 4];
        let b = vec![3, 4, 5, 6];
        let result = intersect(a, b);
        assert!(result.contains(&3));
        assert!(result.contains(&4));
        assert_eq!(result.len(), 2);
    }

    #[test]
    fn test_chunk() {
        let nums = vec![1, 2, 3, 4, 5, 6, 7];
        assert_eq!(chunk(nums, 3), vec![vec![1, 2, 3], vec![4, 5, 6], vec![7]]);
    }

    #[test]
    fn test_count_occurrences() {
        let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
        let counts = count_occurrences(nums);
        assert_eq!(counts.get(&1), Some(&1));
        assert_eq!(counts.get(&3), Some(&3));
        assert_eq!(counts.get(&4), Some(&4));
    }

    #[test]
    fn test_most_frequent() {
        let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
        assert_eq!(most_frequent(nums), Some((4, 4)));
    }

    #[test]
    fn test_partition() {
        let nums = vec![1, 2, 3, 4, 5, 6];
        let (even, odd) = partition(nums, |n| n % 2 == 0);
        assert_eq!(even, vec![2, 4, 6]);
        assert_eq!(odd, vec![1, 3, 5]);
    }

    #[test]
    fn test_flatten() {
        let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
        assert_eq!(flatten(nested), vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_has_duplicates() {
        assert!(!has_duplicates(&[1, 2, 3, 4]));
        assert!(has_duplicates(&[1, 2, 2, 3]));
    }
}