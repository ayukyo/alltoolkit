//! 水塘采样（Reservoir Sampling）算法工具库
//!
//! 水塘采样是一种经典的随机采样算法，用于从未知大小的数据流中
//! 均匀随机地选择 k 个元素。核心特性：
//! - 单次遍历：只需遍历数据一次
//! - O(k) 空间：常数空间复杂度，不随数据量增加
//! - 均匀采样：每个元素被选中的概率相同
//!
//! 本模块提供三种经典算法：
//! - Algorithm R：简单直观，O(n) 时间
//! - Algorithm L：更高效，O(k(1 + log(n/k))) 时间
//! - Weighted Reservoir：加权水塘采样

use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

/// 水塘采样器 - Algorithm R 实现
///
/// 经典的水塘采样算法，适用于从未知大小的数据流中采样。
/// 每个元素被选中的概率都是 k/n，其中 n 是数据流的总大小。
#[derive(Clone, Debug)]
pub struct ReservoirSampler<T> {
    /// 水塘（存储采样结果）
    reservoir: Vec<T>,
    /// 水塘容量
    capacity: usize,
    /// 已处理的元素数量
    processed: usize,
    /// 随机种子
    seed: u64,
}

impl<T: Clone> ReservoirSampler<T> {
    /// 创建新的水塘采样器
    ///
    /// # Arguments
    /// * `capacity` - 水塘容量（采样数量）
    ///
    /// # Example
    /// ```
    /// use reservoir_sampling_utils::ReservoirSampler;
    /// let sampler = ReservoirSampler::<i32>::new(10);
    /// ```
    pub fn new(capacity: usize) -> Self {
        Self::with_seed(capacity, 0)
    }
    
    /// 使用随机种子创建水塘采样器
    ///
    /// # Arguments
    /// * `capacity` - 水塘容量
    /// * `seed` - 随机种子（用于可重复结果）
    pub fn with_seed(capacity: usize, seed: u64) -> Self {
        ReservoirSampler {
            reservoir: Vec::with_capacity(capacity),
            capacity,
            processed: 0,
            seed,
        }
    }
    
    /// 添加元素到采样器（Algorithm R）
    ///
    /// 算法逻辑：
    /// 1. 如果水塘未满，直接添加
    /// 2. 如果水塘已满，以 k/n 的概率替换水塘中的随机元素
    ///
    /// # Arguments
    /// * `item` - 要添加的元素
    pub fn add(&mut self, item: T) {
        self.processed += 1;
        
        if self.reservoir.len() < self.capacity {
            self.reservoir.push(item);
        } else {
            // 生成一个 [0, processed) 范围内的随机索引
            let index = self.random_range(self.processed);
            if index < self.capacity {
                self.reservoir[index] = item;
            }
        }
    }
    
    /// 获取当前水塘中的样本
    pub fn samples(&self) -> &[T] {
        &self.reservoir
    }
    
    /// 获取采样结果（消费采样器）
    pub fn into_samples(self) -> Vec<T> {
        self.reservoir
    }
    
    /// 获取已处理的元素数量
    pub fn processed_count(&self) -> usize {
        self.processed
    }
    
    /// 获取水塘容量
    pub fn capacity(&self) -> usize {
        self.capacity
    }
    
    /// 获取当前样本数量
    pub fn len(&self) -> usize {
        self.reservoir.len()
    }
    
    /// 检查水塘是否为空
    pub fn is_empty(&self) -> bool {
        self.reservoir.is_empty()
    }
    
    /// 检查水塘是否已满
    pub fn is_full(&self) -> bool {
        self.reservoir.len() >= self.capacity
    }
    
    /// 清空采样器（保留容量设置）
    pub fn clear(&mut self) {
        self.reservoir.clear();
        self.processed = 0;
        self.seed += 1; // 改变种子以获得不同的随机序列
    }
    
    /// 重置采样器（包括种子）
    pub fn reset(&mut self) {
        self.clear();
        self.seed = 0;
    }
    
    /// 从迭代器中采样
    ///
    /// # Arguments
    /// * `iter` - 数据迭代器
    ///
    /// # Returns
    /// 采样结果
    pub fn sample<I: Iterator<Item = T>>(mut self, iter: I) -> Vec<T> {
        for item in iter {
            self.add(item);
        }
        self.into_samples()
    }
    
    /// 从切片中采样
    ///
    /// # Arguments
    /// * `data` - 数据切片
    ///
    /// # Returns
    /// 采样结果的克隆
    pub fn sample_from_slice(&mut self, data: &[T]) -> Vec<T> {
        for item in data {
            self.add(item.clone());
        }
        self.samples().to_vec()
    }
    
    /// 生成指定范围内的随机数
    fn random_range(&self, max: usize) -> usize {
        let mut hasher = DefaultHasher::new();
        self.seed.hash(&mut hasher);
        self.processed.hash(&mut hasher);
        (hasher.finish() as usize) % max
    }
}

/// Algorithm L 实现 - 更高效的水塘采样
///
/// Algorithm L 是 Algorithm R 的优化版本，
/// 使用跳跃技术减少随机数生成次数。
/// 时间复杂度：O(k(1 + log(n/k)))
pub struct ReservoirSamplerL<T> {
    reservoir: Vec<T>,
    capacity: usize,
    processed: usize,
    seed: u64,
    // 下一个替换点
    next_replace: usize,
    // 下一个要替换的水塘索引
    replace_index: usize,
}

impl<T: Clone> ReservoirSamplerL<T> {
    /// 创建新的 Algorithm L 采样器
    pub fn new(capacity: usize) -> Self {
        Self::with_seed(capacity, 0)
    }
    
    /// 使用随机种子创建
    pub fn with_seed(capacity: usize, seed: u64) -> Self {
        ReservoirSamplerL {
            reservoir: Vec::with_capacity(capacity),
            capacity,
            processed: 0,
            seed,
            next_replace: capacity + 1,
            replace_index: 0,
        }
    }
    
    /// 添加元素
    pub fn add(&mut self, item: T) {
        self.processed += 1;
        
        if self.reservoir.len() < self.capacity {
            self.reservoir.push(item);
            // 当水塘刚满时，初始化跳跃参数
            if self.reservoir.len() == self.capacity {
                self.init_skip();
            }
        } else {
            // 检查是否到达替换点
            if self.processed >= self.next_replace {
                // 替换水塘中的元素
                self.reservoir[self.replace_index] = item;
                self.init_skip();
            }
        }
    }
    
    /// 初始化跳跃参数
    fn init_skip(&mut self) {
        // 使用几何分布生成跳跃步数
        let u = self.random_f64();
        let skip = (u.ln() / (1.0 - (self.capacity as f64 / self.processed as f64)).ln()).floor() as usize;
        
        self.next_replace = self.processed + skip + 1;
        self.replace_index = self.random_range(self.capacity);
    }
    
    /// 获取样本
    pub fn samples(&self) -> &[T] {
        &self.reservoir
    }
    
    /// 消费采样器获取结果
    pub fn into_samples(self) -> Vec<T> {
        self.reservoir
    }
    
    /// 获取已处理数量
    pub fn processed_count(&self) -> usize {
        self.processed
    }
    
    /// 获取容量
    pub fn capacity(&self) -> usize {
        self.capacity
    }
    
    /// 从迭代器采样
    pub fn sample<I: Iterator<Item = T>>(mut self, iter: I) -> Vec<T> {
        for item in iter {
            self.add(item);
        }
        self.into_samples()
    }
    
    fn random_range(&self, max: usize) -> usize {
        let mut hasher = DefaultHasher::new();
        self.seed.hash(&mut hasher);
        self.processed.hash(&mut hasher);
        (hasher.finish() as usize) % max
    }
    
    fn random_f64(&self) -> f64 {
        let mut hasher = DefaultHasher::new();
        self.seed.hash(&mut hasher);
        self.processed.hash(&mut hasher);
        self.next_replace.hash(&mut hasher);
        (hasher.finish() as f64) / (u64::MAX as f64)
    }
}

/// 加权水塘采样器
///
/// 根据权重对元素进行采样，权重越高的元素被选中的概率越大。
/// 使用 Efraimidis & Spirakis 算法。
#[derive(Clone, Debug)]
pub struct WeightedReservoirSampler<T> {
    reservoir: Vec<(T, f64)>, // (item, priority)
    capacity: usize,
    processed: usize,
    seed: u64,
}

impl<T: Clone> WeightedReservoirSampler<T> {
    /// 创建新的加权采样器
    pub fn new(capacity: usize) -> Self {
        Self::with_seed(capacity, 0)
    }
    
    /// 使用随机种子创建
    pub fn with_seed(capacity: usize, seed: u64) -> Self {
        WeightedReservoirSampler {
            reservoir: Vec::with_capacity(capacity + 1), // 多一个位置用于临时存储
            capacity,
            processed: 0,
            seed,
        }
    }
    
    /// 添加带权重的元素
    ///
    /// # Arguments
    /// * `item` - 元素
    /// * `weight` - 权重（必须为正数）
    pub fn add(&mut self, item: T, weight: f64) {
        assert!(weight > 0.0, "权重必须为正数");
        self.processed += 1;
        
        // 计算优先级：u^(1/w)，其中 u 是 [0,1] 均匀随机数
        let u = self.random_f64();
        let priority = u.powf(1.0 / weight);
        
        if self.reservoir.len() < self.capacity {
            self.reservoir.push((item, priority));
            // 维护最小堆性质
            self.heapify_up(self.reservoir.len() - 1);
        } else {
            // 如果新元素的优先级大于最小优先级，替换
            if priority > self.reservoir[0].1 {
                self.reservoir[0] = (item, priority);
                self.heapify_down(0);
            }
        }
    }
    
    /// 获取样本（不含优先级）
    pub fn samples(&self) -> Vec<&T> {
        self.reservoir.iter().map(|(item, _)| item).collect()
    }
    
    /// 获取样本（消费采样器）
    pub fn into_samples(self) -> Vec<T> {
        self.reservoir.into_iter().map(|(item, _)| item).collect()
    }
    
    /// 获取带优先级的样本
    pub fn samples_with_priority(&self) -> &[(T, f64)] {
        &self.reservoir
    }
    
    /// 获取已处理数量
    pub fn processed_count(&self) -> usize {
        self.processed
    }
    
    /// 获取容量
    pub fn capacity(&self) -> usize {
        self.capacity
    }
    
    /// 从迭代器采样
    pub fn sample<I: Iterator<Item = (T, f64)>>(mut self, iter: I) -> Vec<T> {
        for (item, weight) in iter {
            self.add(item, weight);
        }
        self.into_samples()
    }
    
    fn heapify_up(&mut self, mut index: usize) {
        while index > 0 {
            let parent = (index - 1) / 2;
            if self.reservoir[index].1 < self.reservoir[parent].1 {
                self.reservoir.swap(index, parent);
                index = parent;
            } else {
                break;
            }
        }
    }
    
    fn heapify_down(&mut self, mut index: usize) {
        let len = self.reservoir.len();
        loop {
            let left = 2 * index + 1;
            let right = 2 * index + 2;
            let mut smallest = index;
            
            if left < len && self.reservoir[left].1 < self.reservoir[smallest].1 {
                smallest = left;
            }
            if right < len && self.reservoir[right].1 < self.reservoir[smallest].1 {
                smallest = right;
            }
            
            if smallest != index {
                self.reservoir.swap(index, smallest);
                index = smallest;
            } else {
                break;
            }
        }
    }
    
    fn random_f64(&self) -> f64 {
        let mut hasher = DefaultHasher::new();
        self.seed.hash(&mut hasher);
        self.processed.hash(&mut hasher);
        let r = hasher.finish();
        // 确保不为0（因为要取对数）
        (r as f64 / u64::MAX as f64).max(1e-300)
    }
}

// ============================================================================
// 便捷函数
// ============================================================================

/// 从切片中采样 k 个元素（Algorithm R）
///
/// # Arguments
/// * `data` - 数据切片
/// * `k` - 采样数量
///
/// # Returns
/// 采样结果
///
/// # Example
/// ```
/// use reservoir_sampling_utils::sample_slice;
/// let data = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
/// let sample = sample_slice(&data, 3);
/// ```
pub fn sample_slice<T: Clone>(data: &[T], k: usize) -> Vec<T> {
    if k >= data.len() {
        return data.to_vec();
    }
    
    let mut sampler = ReservoirSampler::new(k);
    for item in data {
        sampler.add(item.clone());
    }
    sampler.into_samples()
}

/// 从迭代器中采样 k 个元素（Algorithm R）
///
/// # Arguments
/// * `iter` - 数据迭代器
/// * `k` - 采样数量
///
/// # Returns
/// 采样结果
pub fn sample_iter<T: Clone, I: Iterator<Item = T>>(iter: I, k: usize) -> Vec<T> {
    ReservoirSampler::new(k).sample(iter)
}

/// 从切片中采样 k 个元素（Algorithm L - 更高效）
///
/// # Arguments
/// * `data` - 数据切片
/// * `k` - 采样数量
///
/// # Returns
/// 采样结果
pub fn sample_slice_l<T: Clone>(data: &[T], k: usize) -> Vec<T> {
    if k >= data.len() {
        return data.to_vec();
    }
    
    let mut sampler = ReservoirSamplerL::new(k);
    for item in data {
        sampler.add(item.clone());
    }
    sampler.into_samples()
}

/// 从切片中进行加权采样
///
/// # Arguments
/// * `data` - 数据切片
/// * `weights` - 权重切片
/// * `k` - 采样数量
///
/// # Returns
/// 采样结果
pub fn sample_weighted<T: Clone>(data: &[T], weights: &[f64], k: usize) -> Vec<T> {
    assert_eq!(data.len(), weights.len(), "数据和权重长度必须相等");
    assert!(k <= data.len(), "采样数量不能超过数据长度");
    
    let mut sampler = WeightedReservoirSampler::new(k);
    for (item, weight) in data.iter().zip(weights.iter()) {
        sampler.add(item.clone(), *weight);
    }
    sampler.into_samples()
}

/// 从切片中采样一个元素
///
/// # Arguments
/// * `data` - 数据切片
///
/// # Returns
/// 采样结果（如果切片非空）
pub fn sample_one<T: Clone>(data: &[T]) -> Option<T> {
    if data.is_empty() {
        return None;
    }
    
    sample_slice(data, 1).into_iter().next()
}

/// 创建分层的随机样本
///
/// 将数据分层，每层独立采样，适用于分层抽样场景。
///
/// # Arguments
/// * `data` - 数据切片
/// * `strata` - 层标记切片
/// * `k_per_stratum` - 每层采样数量
///
/// # Returns
/// 分层采样结果
pub fn sample_stratified<T: Clone, S: Eq + Hash + Clone>(
    data: &[T],
    strata: &[S],
    k_per_stratum: usize,
) -> Vec<T> {
    assert_eq!(data.len(), strata.len(), "数据和层标记长度必须相等");
    
    // 分组
    let mut groups: std::collections::HashMap<S, Vec<T>> = std::collections::HashMap::new();
    for (item, stratum) in data.iter().zip(strata.iter()) {
        groups.entry(stratum.clone()).or_insert_with(Vec::new).push(item.clone());
    }
    
    // 每层独立采样
    let mut result = Vec::new();
    for (_, group) in groups {
        let sample = sample_slice(&group, k_per_stratum);
        result.extend(sample);
    }
    
    result
}

// ============================================================================
// 单元测试
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    
    // ==================== ReservoirSampler 测试 ====================
    
    #[test]
    fn test_basic_sampling() {
        let data: Vec<i32> = (1..=100).collect();
        let sampler = ReservoirSampler::new(10);
        let samples = sampler.sample(data.into_iter());
        
        assert_eq!(samples.len(), 10);
        // 所有样本都应该在原始范围内
        for &s in &samples {
            assert!(s >= 1 && s <= 100);
        }
    }
    
    #[test]
    fn test_empty_data() {
        let sampler = ReservoirSampler::<i32>::new(10);
        let samples = sampler.sample(std::iter::empty());
        assert!(samples.is_empty());
    }
    
    #[test]
    fn test_k_greater_than_n() {
        let data = vec![1, 2, 3, 4, 5];
        let sampler = ReservoirSampler::new(10);
        let samples = sampler.sample(data.into_iter());
        
        // 当 k > n 时，返回所有元素
        assert_eq!(samples.len(), 5);
    }
    
    #[test]
    fn test_k_equals_n() {
        let data: Vec<i32> = (1..=10).collect();
        let sampler = ReservoirSampler::new(10);
        let samples = sampler.sample(data.into_iter());
        
        assert_eq!(samples.len(), 10);
    }
    
    #[test]
    fn test_uniform_distribution() {
        // 测试采样是否大致均匀分布
        // 由于使用哈希函数作为伪随机，只检查基本统计特性
        let data: Vec<i32> = (1..=100).collect();
        let k = 10;
        let trials = 50;
        
        let mut counts: std::collections::HashMap<i32, i32> = std::collections::HashMap::new();
        
        for seed in 0..trials {
            let mut sampler = ReservoirSampler::with_seed(k, seed);
            for &item in &data {
                sampler.add(item);
            }
            for &item in sampler.samples() {
                *counts.entry(item).or_insert(0) += 1;
            }
        }
        
        // 检查采样结果覆盖了大部分元素
        // 期望 k * trials 次采样，每次采样 k 个元素
        let total_samples = k * trials as usize;
        // 每个元素被选中的期望次数
        let expected_per_element = total_samples as f64 / data.len() as f64;
        
        // 检查至少有一半的元素被选中过
        assert!(counts.len() >= data.len() / 2, "采样覆盖范围过小");
        
        // 检查最大计数不超过期望的 3 倍（宽松的均匀性检查）
        let max_count = counts.values().max().copied().unwrap_or(0);
        assert!(max_count as f64 <= expected_per_element * 3.0, "采样分布不够均匀");
    }
    
    #[test]
    fn test_processed_count() {
        let mut sampler = ReservoirSampler::new(5);
        for i in 1..=100 {
            sampler.add(i);
        }
        assert_eq!(sampler.processed_count(), 100);
        assert_eq!(sampler.len(), 5);
    }
    
    #[test]
    fn test_clear_and_reuse() {
        let mut sampler = ReservoirSampler::new(5);
        
        // 第一次采样
        for i in 1..=50 {
            sampler.add(i);
        }
        assert_eq!(sampler.len(), 5);
        assert_eq!(sampler.processed_count(), 50);
        
        // 清空
        sampler.clear();
        assert_eq!(sampler.len(), 0);
        assert_eq!(sampler.processed_count(), 0);
        
        // 第二次采样
        for i in 100..=150 {
            sampler.add(i);
        }
        assert_eq!(sampler.len(), 5);
        assert_eq!(sampler.processed_count(), 51);
    }
    
    #[test]
    fn test_sample_from_slice() {
        let data: Vec<i32> = (1..=100).collect();
        let mut sampler = ReservoirSampler::new(10);
        let samples = sampler.sample_from_slice(&data);
        
        assert_eq!(samples.len(), 10);
    }
    
    #[test]
    fn test_sample_one() {
        let data = vec![1, 2, 3, 4, 5];
        let sample = sample_one(&data);
        assert!(sample.is_some());
        
        let empty: Vec<i32> = vec![];
        let sample = sample_one(&empty);
        assert!(sample.is_none());
    }
    
    // ==================== ReservoirSamplerL 测试 ====================
    
    #[test]
    fn test_algorithm_l_basic() {
        let data: Vec<i32> = (1..=100).collect();
        let sampler = ReservoirSamplerL::new(10);
        let samples = sampler.sample(data.into_iter());
        
        assert_eq!(samples.len(), 10);
        for &s in &samples {
            assert!(s >= 1 && s <= 100);
        }
    }
    
    #[test]
    fn test_algorithm_l_empty() {
        let sampler = ReservoirSamplerL::<i32>::new(10);
        let samples = sampler.sample(std::iter::empty());
        assert!(samples.is_empty());
    }
    
    #[test]
    fn test_algorithm_l_k_greater_than_n() {
        let data = vec![1, 2, 3, 4, 5];
        let sampler = ReservoirSamplerL::new(10);
        let samples = sampler.sample(data.into_iter());
        
        assert_eq!(samples.len(), 5);
    }
    
    // ==================== WeightedReservoirSampler 测试 ====================
    
    #[test]
    fn test_weighted_basic() {
        let mut sampler = WeightedReservoirSampler::new(3);
        sampler.add("a", 1.0);
        sampler.add("b", 1.0);
        sampler.add("c", 1.0);
        sampler.add("d", 1.0);
        sampler.add("e", 1.0);
        
        assert_eq!(sampler.samples().len(), 3);
    }
    
    #[test]
    fn test_weighted_high_weight_preferred() {
        // 高权重元素应该更可能被选中
        let mut high_weight_count = 0;
        let trials = 100;
        
        for seed in 0..trials {
            let mut sampler = WeightedReservoirSampler::with_seed(1, seed);
            sampler.add("low", 1.0);
            sampler.add("high", 100.0);
            
            let samples = sampler.into_samples();
            if samples.contains(&"high") {
                high_weight_count += 1;
            }
        }
        
        // 高权重元素应该几乎总是被选中
        assert!(high_weight_count > trials * 90 / 100);
    }
    
    #[test]
    fn test_weighted_zero_weight_panics() {
        let mut sampler = WeightedReservoirSampler::new(1);
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            sampler.add("item", 0.0);
        }));
        assert!(result.is_err());
    }
    
    #[test]
    fn test_weighted_negative_weight_panics() {
        let mut sampler = WeightedReservoirSampler::new(1);
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            sampler.add("item", -1.0);
        }));
        assert!(result.is_err());
    }
    
    // ==================== 便捷函数测试 ====================
    
    #[test]
    fn test_sample_slice_func() {
        let data: Vec<i32> = (1..=100).collect();
        let samples = sample_slice(&data, 10);
        assert_eq!(samples.len(), 10);
    }
    
    #[test]
    fn test_sample_iter_func() {
        let samples = sample_iter(1..=100, 10);
        assert_eq!(samples.len(), 10);
    }
    
    #[test]
    fn test_sample_weighted_func() {
        let data = vec!["a", "b", "c", "d", "e"];
        let weights = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let samples = sample_weighted(&data, &weights, 3);
        assert_eq!(samples.len(), 3);
    }
    
    #[test]
    fn test_sample_weighted_length_mismatch() {
        let data = vec!["a", "b", "c"];
        let weights = vec![1.0, 2.0];
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            sample_weighted(&data, &weights, 2);
        }));
        assert!(result.is_err());
    }
    
    #[test]
    fn test_sample_stratified_basic() {
        let data = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let strata = vec!["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"];
        let samples = sample_stratified(&data, &strata, 2);
        
        // 每层采样 2 个，共 4 个
        assert_eq!(samples.len(), 4);
    }
    
    #[test]
    fn test_sample_stratified_preserves_strata() {
        // 使用足够的样本确保每层都有代表
        let data: Vec<i32> = (1..=100).collect();
        let strata: Vec<&str> = (0..100).map(|i| if i < 50 { "A" } else { "B" }).collect();
        
        // 运行多次检查分层效果
        for _ in 0..10 {
            let samples = sample_stratified(&data, &strata, 5);
            // A 层 5 个 + B 层 5 个 = 10 个
            assert_eq!(samples.len(), 10);
            
            // 检查 A 层（1-50）和 B 层（51-100）都有样本
            let a_count = samples.iter().filter(|&&x| x <= 50).count();
            let b_count = samples.iter().filter(|&&x| x > 50).count();
            assert_eq!(a_count, 5);
            assert_eq!(b_count, 5);
        }
    }
    
    // ==================== 边界条件测试 ====================
    
    #[test]
    fn test_single_element() {
        let data = vec![42];
        let samples = sample_slice(&data, 1);
        assert_eq!(samples, vec![42]);
    }
    
    #[test]
    fn test_k_zero() {
        let data = vec![1, 2, 3, 4, 5];
        let samples = sample_slice(&data, 0);
        assert!(samples.is_empty());
    }
    
    #[test]
    fn test_large_k() {
        let data = vec![1, 2, 3];
        let samples = sample_slice(&data, 1000);
        assert_eq!(samples.len(), 3);
    }
    
    #[test]
    fn test_string_sampling() {
        let data = vec!["hello", "world", "rust", "sampling", "test"];
        let samples = sample_slice(&data, 3);
        assert_eq!(samples.len(), 3);
    }
    
    #[test]
    fn test_struct_sampling() {
        #[derive(Clone, Debug, PartialEq)]
        struct Point {
            x: i32,
            y: i32,
        }
        
        let data = vec![
            Point { x: 1, y: 1 },
            Point { x: 2, y: 2 },
            Point { x: 3, y: 3 },
        ];
        
        let samples = sample_slice(&data, 2);
        assert_eq!(samples.len(), 2);
    }
    
    // ==================== 性能测试 ====================
    
    #[test]
    fn test_large_dataset() {
        // 测试大数据集的采样效率
        let data: Vec<i32> = (1..=100_000).collect();
        let samples = sample_slice(&data, 100);
        assert_eq!(samples.len(), 100);
    }
    
    #[test]
    fn test_large_sample_size() {
        // 测试大 k 值的采样
        let data: Vec<i32> = (1..=10_000).collect();
        let samples = sample_slice(&data, 5000);
        assert_eq!(samples.len(), 5000);
    }
    
    #[test]
    fn test_multiple_sequential_samples() {
        let mut sampler = ReservoirSampler::new(5);
        
        for i in 1..=100 {
            sampler.add(i);
        }
        assert_eq!(sampler.len(), 5);
        
        sampler.clear();
        
        for i in 101..=200 {
            sampler.add(i);
        }
        assert_eq!(sampler.len(), 5);
    }
}