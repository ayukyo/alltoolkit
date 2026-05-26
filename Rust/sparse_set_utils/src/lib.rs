//! Sparse Set - 高性能稀疏集合实现
//!
//! 稀疏集合是一种支持 O(1) 插入、删除和查找的数据结构。
//! 空间复杂度为 O(max_element)，适合元素值相对集中的场景。
//! 常用于实体组件系统（ECS）和图算法。
//!
//! # 特性
//! - 插入: O(1) 平均
//! - 删除: O(1)
//! - 查找: O(1)
//! - 遍历: O(n) 其中 n 是元素数量
//! - 零外部依赖

use std::ops::{Deref, DerefMut};

/// 稀疏集合 - 高性能整数集合
///
/// 使用两个数组实现：
/// - `sparse`: 稀疏数组，索引为元素值，值为在 dense 数组中的位置
/// - `dense`: 稠密数组，存储实际的元素值
///
/// # 示例
/// ```
/// use sparse_set_utils::SparseSet;
///
/// let mut set = SparseSet::new(100);
/// set.insert(5);
/// set.insert(42);
/// assert!(set.contains(&5));
/// assert!(set.contains(&42));
/// assert_eq!(set.len(), 2);
/// set.remove(&5);
/// assert!(!set.contains(&5));
/// ```
#[derive(Debug, Clone)]
pub struct SparseSet {
    /// 稀疏数组：索引是元素值，值是在 dense 中的位置（+1，0 表示不存在）
    sparse: Vec<usize>,
    /// 稠密数组：存储实际元素
    dense: Vec<usize>,
}

impl SparseSet {
    /// 创建新的稀疏集合
    ///
    /// # 参数
    /// - `capacity`: 元素的最大可能值 + 1
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let set = SparseSet::new(1000);
    /// ```
    pub fn new(capacity: usize) -> Self {
        Self {
            sparse: vec![0; capacity],
            dense: Vec::new(),
        }
    }

    /// 创建具有预分配空间的稀疏集合
    ///
    /// # 参数
    /// - `capacity`: 元素的最大可能值 + 1
    /// - `expected_elements`: 预期元素数量，用于预分配 dense 数组空间
    pub fn with_capacity(capacity: usize, expected_elements: usize) -> Self {
        Self {
            sparse: vec![0; capacity],
            dense: Vec::with_capacity(expected_elements),
        }
    }

    /// 获取集合的最大容量
    pub fn capacity(&self) -> usize {
        self.sparse.len()
    }

    /// 插入元素到集合中
    ///
    /// # 返回
    /// - `true`: 如果元素是新插入的
    /// - `false`: 如果元素已存在
    ///
    /// # 时间复杂度
    /// O(1)
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// assert!(set.insert(42));
    /// assert!(!set.insert(42)); // 重复插入返回 false
    /// ```
    pub fn insert(&mut self, value: usize) -> bool {
        if value >= self.sparse.len() {
            // 扩展 sparse 数组
            self.sparse.resize(value + 1, 0);
        }

        if self.sparse[value] != 0 {
            return false; // 已存在
        }

        self.dense.push(value);
        self.sparse[value] = self.dense.len(); // 使用 1-based 索引
        true
    }

    /// 从集合中移除元素
    ///
    /// # 返回
    /// - `true`: 如果元素存在并被移除
    /// - `false`: 如果元素不存在
    ///
    /// # 时间复杂度
    /// O(1)
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// set.insert(42);
    /// assert!(set.remove(&42));
    /// assert!(!set.remove(&42)); // 再次移除返回 false
    /// ```
    pub fn remove(&mut self, value: &usize) -> bool {
        if *value >= self.sparse.len() {
            return false;
        }

        let dense_index = self.sparse[*value];
        if dense_index == 0 {
            return false; // 不存在
        }

        let dense_index = dense_index - 1; // 转换为 0-based

        // 如果不是最后一个元素，将最后一个元素移到被删除的位置
        if dense_index != self.dense.len() - 1 {
            let last_value = *self.dense.last().unwrap();
            self.dense[dense_index] = last_value;
            self.sparse[last_value] = dense_index + 1;
        }

        self.dense.pop();
        self.sparse[*value] = 0;
        true
    }

    /// 检查元素是否在集合中
    ///
    /// # 时间复杂度
    /// O(1)
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// set.insert(42);
    /// assert!(set.contains(&42));
    /// assert!(!set.contains(&99));
    /// ```
    pub fn contains(&self, value: &usize) -> bool {
        if *value >= self.sparse.len() {
            return false;
        }
        self.sparse[*value] != 0
    }

    /// 获取集合中的元素数量
    pub fn len(&self) -> usize {
        self.dense.len()
    }

    /// 检查集合是否为空
    pub fn is_empty(&self) -> bool {
        self.dense.is_empty()
    }

    /// 清空集合
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// set.insert(42);
    /// set.clear();
    /// assert!(set.is_empty());
    /// ```
    pub fn clear(&mut self) {
        for &value in &self.dense {
            self.sparse[value] = 0;
        }
        self.dense.clear();
    }

    /// 获取集合中所有元素的迭代器
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// set.insert(1);
    /// set.insert(2);
    /// set.insert(3);
    /// 
    /// let sum: usize = set.iter().sum();
    /// assert_eq!(sum, 6);
    /// ```
    pub fn iter(&self) -> impl Iterator<Item = &usize> {
        self.dense.iter()
    }

    /// 将集合转换为 Vec
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// set.insert(1);
    /// set.insert(2);
    /// let vec = set.to_vec();
    /// assert_eq!(vec, vec![1, 2]);
    /// ```
    pub fn to_vec(&self) -> Vec<usize> {
        self.dense.clone()
    }

    /// 保留满足条件的元素，删除其他元素
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut set = SparseSet::new(100);
    /// set.insert(1);
    /// set.insert(2);
    /// set.insert(3);
    /// set.retain(|&x| x % 2 == 0);
    /// assert_eq!(set.len(), 1);
    /// assert!(set.contains(&2));
    /// ```
    pub fn retain<F>(&mut self, mut f: F)
    where
        F: FnMut(&usize) -> bool,
    {
        let mut write_idx = 0;
        for read_idx in 0..self.dense.len() {
            let value = self.dense[read_idx];
            if f(&value) {
                if write_idx != read_idx {
                    self.dense[write_idx] = value;
                    self.sparse[value] = write_idx + 1;
                }
                write_idx += 1;
            } else {
                self.sparse[value] = 0;
            }
        }
        self.dense.truncate(write_idx);
    }

    /// 检查是否是另一个集合的子集
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut a = SparseSet::new(100);
    /// let mut b = SparseSet::new(100);
    /// a.insert(1);
    /// b.insert(1);
    /// b.insert(2);
    /// assert!(a.is_subset(&b));
    /// ```
    pub fn is_subset(&self, other: &SparseSet) -> bool {
        self.iter().all(|x| other.contains(x))
    }

    /// 检查是否与另一个集合有交集
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut a = SparseSet::new(100);
    /// let mut b = SparseSet::new(100);
    /// a.insert(1);
    /// b.insert(1);
    /// b.insert(2);
    /// assert!(a.intersects(&b));
    /// ```
    pub fn intersects(&self, other: &SparseSet) -> bool {
        self.iter().any(|x| other.contains(x))
    }

    /// 计算与另一个集合的交集
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut a = SparseSet::new(100);
    /// let mut b = SparseSet::new(100);
    /// a.insert(1);
    /// a.insert(2);
    /// b.insert(2);
    /// b.insert(3);
    /// let intersection = a.intersection(&b);
    /// assert!(intersection.contains(&2));
    /// assert_eq!(intersection.len(), 1);
    /// ```
    pub fn intersection(&self, other: &SparseSet) -> SparseSet {
        let (smaller, larger) = if self.len() <= other.len() {
            (self, other)
        } else {
            (other, self)
        };

        let mut result = SparseSet::new(smaller.capacity().min(larger.capacity()));
        for &value in smaller.iter() {
            if larger.contains(&value) {
                result.insert(value);
            }
        }
        result
    }

    /// 计算与另一个集合的并集
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut a = SparseSet::new(100);
    /// let mut b = SparseSet::new(100);
    /// a.insert(1);
    /// b.insert(2);
    /// let union = a.union(&b);
    /// assert_eq!(union.len(), 2);
    /// assert!(union.contains(&1));
    /// assert!(union.contains(&2));
    /// ```
    pub fn union(&self, other: &SparseSet) -> SparseSet {
        let mut result = SparseSet::new(self.capacity().max(other.capacity()));
        for &value in self.iter() {
            result.insert(value);
        }
        for &value in other.iter() {
            result.insert(value);
        }
        result
    }

    /// 计算与另一个集合的差集（self - other）
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut a = SparseSet::new(100);
    /// let mut b = SparseSet::new(100);
    /// a.insert(1);
    /// a.insert(2);
    /// b.insert(2);
    /// let diff = a.difference(&b);
    /// assert_eq!(diff.len(), 1);
    /// assert!(diff.contains(&1));
    /// ```
    pub fn difference(&self, other: &SparseSet) -> SparseSet {
        let mut result = SparseSet::new(self.capacity());
        for &value in self.iter() {
            if !other.contains(&value) {
                result.insert(value);
            }
        }
        result
    }

    /// 计算与另一个集合的对称差（只在一个集合中的元素）
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let mut a = SparseSet::new(100);
    /// let mut b = SparseSet::new(100);
    /// a.insert(1);
    /// a.insert(2);
    /// b.insert(2);
    /// b.insert(3);
    /// let sym_diff = a.symmetric_difference(&b);
    /// assert_eq!(sym_diff.len(), 2);
    /// assert!(sym_diff.contains(&1));
    /// assert!(sym_diff.contains(&3));
    /// ```
    pub fn symmetric_difference(&self, other: &SparseSet) -> SparseSet {
        let mut result = SparseSet::new(self.capacity().max(other.capacity()));
        for &value in self.iter() {
            if !other.contains(&value) {
                result.insert(value);
            }
        }
        for &value in other.iter() {
            if !self.contains(&value) {
                result.insert(value);
            }
        }
        result
    }

    /// 从迭代器创建稀疏集合
    ///
    /// # 示例
    /// ```
    /// use sparse_set_utils::SparseSet;
    ///
    /// let set = SparseSet::from_iter(vec![1, 2, 3, 4, 5], 10);
    /// assert_eq!(set.len(), 5);
    /// ```
    pub fn from_iter<I: IntoIterator<Item = usize>>(iter: I, capacity: usize) -> Self {
        let mut set = Self::with_capacity(capacity, 0);
        for value in iter {
            set.insert(value);
        }
        set
    }
}

impl Default for SparseSet {
    fn default() -> Self {
        Self::new(1024)
    }
}

impl<'a> IntoIterator for &'a SparseSet {
    type Item = &'a usize;
    type IntoIter = std::slice::Iter<'a, usize>;

    fn into_iter(self) -> Self::IntoIter {
        self.dense.iter()
    }
}

impl Deref for SparseSet {
    type Target = [usize];

    fn deref(&self) -> &Self::Target {
        &self.dense
    }
}

impl DerefMut for SparseSet {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.dense
    }
}

impl std::iter::FromIterator<usize> for SparseSet {
    fn from_iter<I: IntoIterator<Item = usize>>(iter: I) -> Self {
        let items: Vec<usize> = iter.into_iter().collect();
        let capacity = items.iter().max().map(|m| m + 1).unwrap_or(0);
        Self::from_iter(items, capacity)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_operations() {
        let mut set = SparseSet::new(100);
        
        // 插入
        assert!(set.insert(5));
        assert!(set.insert(10));
        assert!(set.insert(42));
        assert!(!set.insert(5)); // 重复插入
        
        assert_eq!(set.len(), 3);
        
        // 查找
        assert!(set.contains(&5));
        assert!(set.contains(&10));
        assert!(set.contains(&42));
        assert!(!set.contains(&99));
        
        // 删除
        assert!(set.remove(&5));
        assert!(!set.contains(&5));
        assert_eq!(set.len(), 2);
        
        // 删除不存在的元素
        assert!(!set.remove(&5));
        assert!(!set.remove(&999));
    }

    #[test]
    fn test_clear() {
        let mut set = SparseSet::new(100);
        set.insert(1);
        set.insert(2);
        set.insert(3);
        
        set.clear();
        
        assert!(set.is_empty());
        assert!(!set.contains(&1));
        assert!(!set.contains(&2));
        assert!(!set.contains(&3));
    }

    #[test]
    fn test_iter() {
        let mut set = SparseSet::new(100);
        set.insert(1);
        set.insert(2);
        set.insert(3);
        
        let sum: usize = set.iter().sum();
        assert_eq!(sum, 6);
        
        let vec = set.to_vec();
        assert!(vec.contains(&1));
        assert!(vec.contains(&2));
        assert!(vec.contains(&3));
    }

    #[test]
    fn test_retain() {
        let mut set = SparseSet::new(100);
        set.insert(1);
        set.insert(2);
        set.insert(3);
        set.insert(4);
        set.insert(5);
        
        set.retain(|&x| x % 2 == 0);
        
        assert_eq!(set.len(), 2);
        assert!(set.contains(&2));
        assert!(set.contains(&4));
    }

    #[test]
    fn test_set_operations() {
        let mut a = SparseSet::new(100);
        let mut b = SparseSet::new(100);
        
        a.insert(1);
        a.insert(2);
        a.insert(3);
        
        b.insert(2);
        b.insert(3);
        b.insert(4);
        
        // 子集
        let mut c = SparseSet::new(100);
        c.insert(2);
        c.insert(3);
        assert!(c.is_subset(&a));
        
        // 交集
        assert!(a.intersects(&b));
        let intersection = a.intersection(&b);
        assert_eq!(intersection.len(), 2);
        assert!(intersection.contains(&2));
        assert!(intersection.contains(&3));
        
        // 并集
        let union = a.union(&b);
        assert_eq!(union.len(), 4);
        
        // 差集
        let diff = a.difference(&b);
        assert_eq!(diff.len(), 1);
        assert!(diff.contains(&1));
        
        // 对称差
        let sym_diff = a.symmetric_difference(&b);
        assert_eq!(sym_diff.len(), 2);
        assert!(sym_diff.contains(&1));
        assert!(sym_diff.contains(&4));
    }

    #[test]
    fn test_auto_expand() {
        let mut set = SparseSet::new(10);
        assert!(set.insert(5));  // 在初始容量内
        assert!(set.insert(100)); // 超出初始容量，自动扩展
        assert!(set.contains(&100));
    }

    #[test]
    fn test_large_scale() {
        let mut set = SparseSet::new(10000);
        
        // 插入大量元素
        for i in 0..1000 {
            set.insert(i);
        }
        assert_eq!(set.len(), 1000);
        
        // 查找
        for i in 0..1000 {
            assert!(set.contains(&i));
        }
        
        // 删除一半
        for i in (0..1000).step_by(2) {
            set.remove(&i);
        }
        assert_eq!(set.len(), 500);
        
        // 验证
        for i in (0..1000).step_by(2) {
            assert!(!set.contains(&i));
        }
        for i in (1..1000).step_by(2) {
            assert!(set.contains(&i));
        }
    }

    #[test]
    fn test_from_iter() {
        let set = SparseSet::from_iter(vec![1, 2, 3, 4, 5], 10);
        assert_eq!(set.len(), 5);
        
        let set2: SparseSet = vec![10, 20, 30].into_iter().collect();
        assert_eq!(set2.len(), 3);
    }
}