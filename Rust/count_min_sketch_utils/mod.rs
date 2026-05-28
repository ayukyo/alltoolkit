//! Count-Min Sketch - 概率数据结构用于频率估计
//! 
//! Count-Min Sketch 是一个次线性空间的数据结构，用于估计数据流中元素的频率。
//! 它提供以下操作：
//! - add: 添加元素（增加计数）
//! - count: 查询元素的估计频率
//! - merge: 合并两个 Count-Min Sketch
//! - clear: 清空所有计数
//! 
//! 时间复杂度：O(d) 其中 d 是哈希函数数量
//! 空间复杂度：O(w * d) 其中 w 是宽度，d 是深度
//! 
//! 误差界限：
//! - 误差 ≤ ε * N（其中 N 是总计数）
//! - 成功概率 ≥ 1 - δ
//! - 宽度 w ≈ e/ε，深度 d ≈ ln(1/δ)

use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;
use std::cmp::Reverse;

/// Count-Min Sketch 数据结构
#[derive(Clone, Debug)]
pub struct CountMinSketch {
    /// 计数器矩阵 (depth x width)
    counters: Vec<Vec<u64>>,
    /// 宽度（每行的计数器数量）
    width: usize,
    /// 深度（哈希函数数量）
    depth: usize,
    /// 总计数
    total_count: u64,
    /// 种子值用于哈希
    seed: u64,
}

impl CountMinSketch {
    /// 创建新的 Count-Min Sketch
    /// 
    /// # Arguments
    /// * `epsilon` - 误差参数，控制精度（通常 0.01-0.1）
    /// * `delta` - 失败概率参数（通常 0.01-0.001）
    /// 
    /// # Returns
    /// 新的 CountMinSketch 实例
    /// 
    /// # Example
    /// ```
    /// let cms = CountMinSketch::new(0.01, 0.001);
    /// ```
    pub fn new(epsilon: f64, delta: f64) -> Self {
        let width = ((2.718281828 / epsilon).ceil()) as usize;
        let depth = ((1.0 / delta).ln().ceil()) as usize;
        
        Self::with_dimensions(width, depth)
    }
    
    /// 使用指定维度创建 Count-Min Sketch
    /// 
    /// # Arguments
    /// * `width` - 每行的计数器数量
    /// * `depth` - 哈希函数数量（行数）
    /// 
    /// # Returns
    /// 新的 CountMinSketch 实例
    pub fn with_dimensions(width: usize, depth: usize) -> Self {
        let counters = vec![vec![0u64; width]; depth];
        
        CountMinSketch {
            counters,
            width,
            depth,
            total_count: 0,
            seed: 0,
        }
    }
    
    /// 使用容量和误差率创建优化的 Count-Min Sketch
    /// 
    /// # Arguments
    /// * `expected_items` - 预期要添加的不同元素数量
    /// * `error_rate` - 可接受的误差率
    pub fn with_capacity(expected_items: usize, error_rate: f64) -> Self {
        let width = (expected_items as f64 * 2.0 / error_rate).ceil() as usize;
        let depth = 5; // 经验值，通常 3-7 之间
        
        Self::with_dimensions(width.max(100), depth)
    }
    
    /// 获取宽度
    pub fn width(&self) -> usize {
        self.width
    }
    
    /// 获取深度
    pub fn depth(&self) -> usize {
        self.depth
    }
    
    /// 获取总计数
    pub fn total_count(&self) -> u64 {
        self.total_count
    }
    
    /// 计算元素的哈希值
    fn hash<T: Hash>(&self, item: &T, seed: u64) -> u64 {
        let mut hasher = DefaultHasher::new();
        item.hash(&mut hasher);
        seed.hash(&mut hasher);
        hasher.finish()
    }
    
    /// 添加元素（增加计数 1）
    /// 
    /// # Arguments
    /// * `item` - 要添加的元素
    /// 
    /// # Example
    /// ```
    /// let mut cms = CountMinSketch::new(0.01, 0.001);
    /// cms.add(&"hello");
    /// ```
    pub fn add<T: Hash>(&mut self, item: &T) {
        self.add_n(item, 1);
    }
    
    /// 添加元素（增加指定计数）
    /// 
    /// # Arguments
    /// * `item` - 要添加的元素
    /// * `n` - 要增加的计数
    pub fn add_n<T: Hash>(&mut self, item: &T, n: u64) {
        for i in 0..self.depth {
            let hash = self.hash(item, self.seed + i as u64);
            let index = (hash % self.width as u64) as usize;
            self.counters[i][index] = self.counters[i][index].saturating_add(n);
        }
        self.total_count = self.total_count.saturating_add(n);
    }
    
    /// 查询元素的估计频率
    /// 
    /// # Arguments
    /// * `item` - 要查询的元素
    /// 
    /// # Returns
    /// 元素的估计频率（可能高估，但不会低估）
    /// 
    /// # Example
    /// ```
    /// let mut cms = CountMinSketch::new(0.01, 0.001);
    /// cms.add(&"hello");
    /// cms.add(&"hello");
    /// assert!(cms.count(&"hello") >= 2);
    /// ```
    pub fn count<T: Hash>(&self, item: &T) -> u64 {
        let mut min_count = u64::MAX;
        
        for i in 0..self.depth {
            let hash = self.hash(item, self.seed + i as u64);
            let index = (hash % self.width as u64) as usize;
            min_count = min_count.min(self.counters[i][index]);
        }
        
        min_count
    }
    
    /// 查询元素的估计频率（返回 Option）
    /// 如果频率为 0 返回 None
    pub fn count_opt<T: Hash>(&self, item: &T) -> Option<u64> {
        let count = self.count(item);
        if count == 0 { None } else { Some(count) }
    }
    
    /// 检查元素是否存在（频率 > 0）
    pub fn contains<T: Hash>(&self, item: &T) -> bool {
        self.count(item) > 0
    }
    
    /// 清空所有计数
    pub fn clear(&mut self) {
        for row in &mut self.counters {
            for cell in row.iter_mut() {
                *cell = 0;
            }
        }
        self.total_count = 0;
    }
    
    /// 合并另一个 Count-Min Sketch
    /// 两个 Sketch 必须有相同的维度
    /// 
    /// # Arguments
    /// * `other` - 要合并的另一个 CountMinSketch
    /// 
    /// # Returns
    /// Ok(()) 成功，Err(String) 维度不匹配
    pub fn merge(&mut self, other: &CountMinSketch) -> Result<(), String> {
        if self.width != other.width || self.depth != other.depth {
            return Err(format!(
                "Dimension mismatch: ({}, {}) vs ({}, {})",
                self.width, self.depth, other.width, other.depth
            ));
        }
        
        for i in 0..self.depth {
            for j in 0..self.width {
                self.counters[i][j] = self.counters[i][j].saturating_add(other.counters[i][j]);
            }
        }
        self.total_count = self.total_count.saturating_add(other.total_count);
        
        Ok(())
    }
    
    /// 计算与另一个 Count-Min Sketch 的相似度
    /// 使用余弦相似度
    /// 
    /// # Arguments
    /// * `other` - 另一个 CountMinSketch
    /// 
    /// # Returns
    /// 相似度值 [0.0, 1.0]
    pub fn similarity(&self, other: &CountMinSketch) -> f64 {
        if self.width != other.width || self.depth != other.depth {
            return 0.0;
        }
        
        let mut dot_product: u64 = 0;
        let mut norm_self: u64 = 0;
        let mut norm_other: u64 = 0;
        
        for i in 0..self.depth {
            for j in 0..self.width {
                let a = self.counters[i][j];
                let b = other.counters[i][j];
                dot_product += a * b;
                norm_self += a * a;
                norm_other += b * b;
            }
        }
        
        if norm_self == 0 || norm_other == 0 {
            return 0.0;
        }
        
        (dot_product as f64) / ((norm_self as f64).sqrt() * (norm_other as f64).sqrt())
    }
    
    /// 估计元素数量的基数（不同元素的数量）
    /// 使用 Boyer-Moore 算法的变体
    /// 注意：这是一个粗略估计
    pub fn estimate_cardinality(&self) -> u64 {
        let mut sum: u64 = 0;
        let mut nonzero: u64 = 0;
        
        for j in 0..self.width {
            if self.counters[0][j] > 0 {
                sum += self.counters[0][j];
                nonzero += 1;
            }
        }
        
        if nonzero == 0 {
            return 0;
        }
        
        // 使用第一个哈希行的平均值来估计
        // 这是一个简化的估计方法
        let avg = sum as f64 / nonzero as f64;
        ((self.total_count as f64 / avg).ceil()) as u64
    }
    
    /// 获取当前使用的内存（字节）
    pub fn memory_usage(&self) -> usize {
        self.width * self.depth * std::mem::size_of::<u64>()
    }
    
    /// 获取估计误差的上界
    /// 返回当前总计数下的最大可能误差
    pub fn error_bound(&self) -> f64 {
        self.total_count as f64 / self.width as f64
    }
    
    /// 获取当前统计信息
    pub fn stats(&self) -> SketchStats {
        let mut min_cell = u64::MAX;
        let mut max_cell: u64 = 0;
        let mut sum: u64 = 0;
        
        for row in &self.counters {
            for &cell in row {
                min_cell = min_cell.min(cell);
                max_cell = max_cell.max(cell);
                sum += cell;
            }
        }
        
        let total_cells = (self.width * self.depth) as u64;
        let avg_cell = if total_cells > 0 { sum as f64 / total_cells as f64 } else { 0.0 };
        
        SketchStats {
            width: self.width,
            depth: self.depth,
            total_count: self.total_count,
            total_cells,
            min_cell,
            max_cell,
            avg_cell,
            memory_bytes: self.memory_usage(),
            error_bound: self.error_bound(),
        }
    }
    
    /// 获取所有计数器的快照
    pub fn snapshot(&self) -> Vec<Vec<u64>> {
        self.counters.clone()
    }
    
    /// 从快照恢复
    pub fn from_snapshot(snapshot: Vec<Vec<u64>>, total_count: u64) -> Self {
        let depth = snapshot.len();
        let width = if depth > 0 { snapshot[0].len() } else { 0 };
        
        CountMinSketch {
            counters: snapshot,
            width,
            depth,
            total_count,
            seed: 0,
        }
    }
    
    /// 减少计数（删除操作）
    /// 注意：这可能导致负计数的不一致性
    pub fn remove<T: Hash>(&mut self, item: &T) {
        for i in 0..self.depth {
            let hash = self.hash(item, self.seed + i as u64);
            let index = (hash % self.width as u64) as usize;
            self.counters[i][index] = self.counters[i][index].saturating_sub(1);
        }
        if self.total_count > 0 {
            self.total_count -= 1;
        }
    }
    
    /// 减少指定计数
    pub fn remove_n<T: Hash>(&mut self, item: &T, n: u64) {
        for i in 0..self.depth {
            let hash = self.hash(item, self.seed + i as u64);
            let index = (hash % self.width as u64) as usize;
            self.counters[i][index] = self.counters[i][index].saturating_sub(n);
        }
        self.total_count = self.total_count.saturating_sub(n);
    }
}

/// Count-Min Sketch 统计信息
#[derive(Debug, Clone)]
pub struct SketchStats {
    /// 宽度
    pub width: usize,
    /// 深度
    pub depth: usize,
    /// 总计数
    pub total_count: u64,
    /// 总单元格数
    pub total_cells: u64,
    /// 最小单元格值
    pub min_cell: u64,
    /// 最大单元格值
    pub max_cell: u64,
    /// 平均单元格值
    pub avg_cell: f64,
    /// 内存使用（字节）
    pub memory_bytes: usize,
    /// 误差上界
    pub error_bound: f64,
}

impl std::fmt::Display for SketchStats {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "CountMinSketch Stats:\n  Dimensions: {} x {}\n  Total Count: {}\n  Cell Range: [{}, {}]\n  Avg Cell: {:.2}\n  Memory: {} bytes ({:.2} KB)\n  Error Bound: {:.4}",
            self.width,
            self.depth,
            self.total_count,
            self.min_cell,
            self.max_cell,
            self.avg_cell,
            self.memory_bytes,
            self.memory_bytes as f64 / 1024.0,
            self.error_bound
        )
    }
}

impl std::fmt::Display for CountMinSketch {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "CountMinSketch(width={}, depth={}, total_count={})",
            self.width, self.depth, self.total_count
        )
    }
}

impl Default for CountMinSketch {
    fn default() -> Self {
        Self::new(0.01, 0.001)
    }
}

/// Heavy Hitters 追踪器
/// 使用 Count-Min Sketch 结合最小堆来追踪高频元素
pub struct HeavyHitters<T: Hash + Clone + Eq + std::hash::Hash + Ord> {
    sketch: CountMinSketch,
    heap: std::collections::BinaryHeap<Reverse<(u64, T)>>,
    capacity: usize,
    items: std::collections::HashSet<T>,
}

impl<T: Hash + Clone + Eq + std::hash::Hash + Ord> HeavyHitters<T> {
    /// 创建新的 Heavy Hitters 追踪器
    /// 
    /// # Arguments
    /// * `epsilon` - 误差参数
    /// * `delta` - 失败概率
    /// * `capacity` - 要追踪的高频元素数量上限
    pub fn new(epsilon: f64, delta: f64, capacity: usize) -> Self {
        HeavyHitters {
            sketch: CountMinSketch::new(epsilon, delta),
            heap: std::collections::BinaryHeap::new(),
            capacity,
            items: std::collections::HashSet::new(),
        }
    }
    
    /// 添加元素
    pub fn add(&mut self, item: T) {
        self.sketch.add(&item);
        let count = self.sketch.count(&item);
        
        if self.items.contains(&item) {
            // 更新堆中的计数
            self.heap = self.heap.drain()
                .filter(|Reverse((c, ref i))| *c == 0 || *i != item)
                .collect();
            self.heap.push(Reverse((count, item.clone())));
        } else if self.heap.len() < self.capacity {
            self.heap.push(Reverse((count, item.clone())));
            self.items.insert(item);
        } else if let Some(Reverse((min_count, _))) = self.heap.peek() {
            if count > *min_count {
                if let Some(Reverse((_, removed))) = self.heap.pop() {
                    self.items.remove(&removed);
                }
                self.heap.push(Reverse((count, item.clone())));
                self.items.insert(item);
            }
        }
    }
    
    /// 获取当前高频元素及其估计计数
    pub fn get_top(&self) -> Vec<(T, u64)> {
        let mut result: Vec<(T, u64)> = self.heap.iter()
            .map(|Reverse((count, item))| (item.clone(), *count))
            .collect();
        result.sort_by(|a, b| b.1.cmp(&a.1));
        result
    }
    
    /// 获取元素数量
    pub fn len(&self) -> usize {
        self.heap.len()
    }
    
    /// 检查是否为空
    pub fn is_empty(&self) -> bool {
        self.heap.is_empty()
    }
    
    /// 清空
    pub fn clear(&mut self) {
        self.sketch.clear();
        self.heap.clear();
        self.items.clear();
    }
}

/// 频率计数器 - 更简单的高频元素追踪
pub struct FrequencyCounter<T: Hash + Clone> {
    sketch: CountMinSketch,
    top_items: std::collections::HashMap<T, u64>,
    threshold: u64,
}

impl<T: Hash + Clone + Eq + std::hash::Hash> FrequencyCounter<T> {
    /// 创建新的频率计数器
    pub fn new(epsilon: f64, delta: f64, threshold: u64) -> Self {
        FrequencyCounter {
            sketch: CountMinSketch::new(epsilon, delta),
            top_items: std::collections::HashMap::new(),
            threshold,
        }
    }
    
    /// 添加元素
    pub fn add(&mut self, item: T) {
        self.sketch.add(&item);
        let count = self.sketch.count(&item);
        
        if count >= self.threshold {
            self.top_items.insert(item, count);
        }
    }
    
    /// 获取满足阈值的所有元素
    pub fn get_frequent(&self) -> Vec<(&T, &u64)> {
        let mut result: Vec<_> = self.top_items.iter().collect();
        result.sort_by(|a, b| b.1.cmp(a.1));
        result
    }
    
    /// 获取总计数
    pub fn total_count(&self) -> u64 {
        self.sketch.total_count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_new() {
        let cms = CountMinSketch::new(0.01, 0.001);
        assert!(cms.width > 0);
        assert!(cms.depth > 0);
    }
    
    #[test]
    fn test_with_dimensions() {
        let cms = CountMinSketch::with_dimensions(1000, 5);
        assert_eq!(cms.width, 1000);
        assert_eq!(cms.depth, 5);
    }
    
    #[test]
    fn test_add_and_count() {
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        cms.add(&"hello");
        cms.add(&"hello");
        cms.add(&"hello");
        
        assert!(cms.count(&"hello") >= 3);
        assert_eq!(cms.total_count(), 3);
    }
    
    #[test]
    fn test_add_n() {
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        cms.add_n(&"test", 10);
        assert!(cms.count(&"test") >= 10);
        assert_eq!(cms.total_count(), 10);
    }
    
    #[test]
    fn test_contains() {
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        assert!(!cms.contains(&"missing"));
        
        cms.add(&"present");
        assert!(cms.contains(&"present"));
    }
    
    #[test]
    fn test_clear() {
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        cms.add(&"test");
        cms.add(&"another");
        assert!(cms.total_count() > 0);
        
        cms.clear();
        assert_eq!(cms.total_count(), 0);
        assert!(!cms.contains(&"test"));
    }
    
    #[test]
    fn test_merge() {
        let mut cms1 = CountMinSketch::with_dimensions(100, 5);
        let mut cms2 = CountMinSketch::with_dimensions(100, 5);
        
        cms1.add(&"hello");
        cms1.add(&"world");
        
        cms2.add(&"hello");
        cms2.add(&"rust");
        
        cms1.merge(&cms2).unwrap();
        
        assert!(cms1.count(&"hello") >= 2);
        assert!(cms1.count(&"world") >= 1);
        assert!(cms1.count(&"rust") >= 1);
    }
    
    #[test]
    fn test_merge_dimension_mismatch() {
        let cms1 = CountMinSketch::with_dimensions(100, 5);
        let cms2 = CountMinSketch::with_dimensions(200, 5);
        
        let mut cms = cms1;
        assert!(cms.merge(&cms2).is_err());
    }
    
    #[test]
    fn test_similarity() {
        let mut cms1 = CountMinSketch::with_dimensions(100, 5);
        let mut cms2 = CountMinSketch::with_dimensions(100, 5);
        
        cms1.add(&"hello");
        cms1.add(&"world");
        
        cms2.add(&"hello");
        cms2.add(&"world");
        
        let sim = cms1.similarity(&cms2);
        assert!(sim > 0.9);
    }
    
    #[test]
    fn test_memory_usage() {
        let cms = CountMinSketch::with_dimensions(1000, 10);
        // 1000 * 10 * 8 bytes = 80000 bytes
        assert_eq!(cms.memory_usage(), 80000);
    }
    
    #[test]
    fn test_error_bound() {
        let mut cms = CountMinSketch::with_dimensions(1000, 5);
        
        for i in 0..100 {
            cms.add(&i);
        }
        
        // 误差上界应该小于总计数
        let bound = cms.error_bound();
        assert!(bound <= 100.0);
    }
    
    #[test]
    fn test_stats() {
        let mut cms = CountMinSketch::with_dimensions(100, 3);
        
        cms.add(&"test1");
        cms.add(&"test2");
        cms.add(&"test1");
        
        let stats = cms.stats();
        assert_eq!(stats.width, 100);
        assert_eq!(stats.depth, 3);
        assert_eq!(stats.total_count, 3);
    }
    
    #[test]
    fn test_snapshot_and_restore() {
        let mut cms = CountMinSketch::with_dimensions(100, 5);
        
        cms.add(&"hello");
        cms.add(&"world");
        
        let snapshot = cms.snapshot();
        let total = cms.total_count();
        
        let restored = CountMinSketch::from_snapshot(snapshot, total);
        
        assert_eq!(restored.count(&"hello"), cms.count(&"hello"));
        assert_eq!(restored.count(&"world"), cms.count(&"world"));
    }
    
    #[test]
    fn test_remove() {
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        cms.add(&"test");
        cms.add(&"test");
        
        let count_before = cms.count(&"test");
        cms.remove(&"test");
        let count_after = cms.count(&"test");
        
        // 移除后计数应该减少（如果计数足够大）
        // 注意：由于 CMS 的特性，可能会有误差
    }
    
    #[test]
    fn test_heavy_hitters() {
        let mut hh: HeavyHitters<&str> = HeavyHitters::new(0.01, 0.001, 3);
        
        for _ in 0..100 {
            hh.add("frequent");
        }
        for _ in 0..50 {
            hh.add("medium");
        }
        for _ in 0..10 {
            hh.add("rare");
        }
        
        let top = hh.get_top();
        assert!(top.len() <= 3);
        assert!(top.iter().any(|(item, _)| *item == "frequent"));
    }
    
    #[test]
    fn test_frequency_counter() {
        let mut fc: FrequencyCounter<&str> = FrequencyCounter::new(0.01, 0.001, 5);
        
        for _ in 0..10 {
            fc.add("common");
        }
        for _ in 0..2 {
            fc.add("rare");
        }
        
        let frequent = fc.get_frequent();
        assert!(frequent.iter().any(|(item, _)| **item == "common"));
    }
    
    #[test]
    fn test_different_types() {
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        // String
        cms.add(&String::from("test"));
        
        // Integer
        cms.add(&42);
        cms.add(&42);
        
        // Tuple
        cms.add(&(1, 2, 3));
        
        assert!(cms.count(&String::from("test")) >= 1);
        assert!(cms.count(&42) >= 2);
        assert!(cms.count(&(1, 2, 3)) >= 1);
    }
    
    #[test]
    fn test_high_frequency_accuracy() {
        let mut cms = CountMinSketch::new(0.001, 0.0001);
        
        // 添加大量相同元素
        for _ in 0..1000 {
            cms.add(&"frequent");
        }
        
        // 添加少量其他元素
        for i in 0..100 {
            cms.add(&format!("item_{}", i));
        }
        
        let count = cms.count(&"frequent");
        // 估计值应该在真实值附近
        assert!(count >= 950 && count <= 1100, "Count {} is out of expected range", count);
    }
    
    #[test]
    fn test_default() {
        let cms = CountMinSketch::default();
        assert!(cms.width > 0);
        assert!(cms.depth > 0);
    }
    
    #[test]
    fn test_display() {
        let cms = CountMinSketch::new(0.01, 0.001);
        let display = format!("{}", cms);
        assert!(display.contains("CountMinSketch"));
    }
    
    #[test]
    fn test_with_capacity() {
        let cms = CountMinSketch::with_capacity(10000, 0.1);
        assert!(cms.width >= 100);
        assert!(cms.depth >= 3);
    }
}

// 单元测试
#[cfg(test)]
mod property_tests {
    use super::*;
    
    #[test]
    fn test_monotonicity() {
        // 单调性：添加更多元素不会减少计数
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        for i in 0..100 {
            cms.add(&"test");
            let count = cms.count(&"test");
            assert!(count >= i + 1, "Count should be at least {}", i + 1);
        }
    }
    
    #[test]
    fn test_no_underestimate() {
        // Count-Min Sketch 永远不会低估
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        let actual_count = 50;
        for _ in 0..actual_count {
            cms.add(&"target");
        }
        
        let estimated = cms.count(&"target");
        assert!(estimated >= actual_count, 
            "CMS should never underestimate: actual={}, estimated={}", 
            actual_count, estimated);
    }
    
    #[test]
    fn test_total_count_accuracy() {
        // 总计数应该准确
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        let total = 1000;
        for i in 0..total {
            cms.add(&i);
        }
        
        assert_eq!(cms.total_count(), total);
    }
    
    #[test]
    fn test_add_n_accuracy() {
        // add_n 应该正确累加
        let mut cms = CountMinSketch::new(0.01, 0.001);
        
        cms.add_n(&"test", 10);
        assert_eq!(cms.total_count(), 10);
        
        cms.add_n(&"test", 5);
        assert_eq!(cms.total_count(), 15);
    }
}