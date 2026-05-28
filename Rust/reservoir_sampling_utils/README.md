# Reservoir Sampling Utils - 水塘采样算法工具库

水塘采样（Reservoir Sampling）是一种经典的随机采样算法，用于从未知大小的数据流中均匀随机地选择 k 个元素。

## 核心特性

- **单次遍历**：只需遍历数据一次，无需预先知道数据大小
- **O(k) 空间**：常数空间复杂度，不随数据量增加
- **均匀采样**：每个元素被选中的概率相同（k/n）
- **零外部依赖**：纯 Rust 标准库实现

## 三种经典算法

### Algorithm R（ReservoirSampler）

经典的水塘采样算法，简单直观：
- 前k个元素直接进入水塘
- 第n个元素以 k/n 的概率替换水塘中的随机元素
- 时间复杂度：O(n)

```rust
use reservoir_sampling_utils::ReservoirSampler;

// 创建采样器
let mut sampler = ReservoirSampler::new(10);

// 添加元素
for item in data_stream {
    sampler.add(item);
}

// 获取样本
let samples = sampler.into_samples();
```

### Algorithm L（ReservoirSamplerL）

更高效的实现，使用跳跃技术：
- 减少随机数生成次数
- 时间复杂度：O(k(1 + log(n/k)))
- 适合大规模数据采样

```rust
use reservoir_sampling_utils::ReservoirSamplerL;

let sampler = ReservoirSamplerL::new(10);
let samples = sampler.sample(data_stream.into_iter());
```

### Weighted Reservoir（WeightedReservoirSampler）

加权水塘采样，根据权重采样：
- 权重越高的元素更可能被选中
- 使用 Efraimidis & Spirakis 算法
- 适合需要优先级的采样场景

```rust
use reservoir_sampling_utils::WeightedReservoirSampler;

let mut sampler = WeightedReservoirSampler::new(5);
sampler.add("important", 10.0);  // 高权重
sampler.add("normal", 1.0);       // 低权重

let samples = sampler.into_samples();
```

## 便捷函数

```rust
use reservoir_sampling_utils::*;

// 从切片采样
let samples = sample_slice(&data, k);

// 从迭代器采样
let samples = sample_iter(1..=1000, k);

// 加权采样
let samples = sample_weighted(&data, &weights, k);

// 采样单个元素
let sample = sample_one(&data);

// 分层采样
let samples = sample_stratified(&data, &strata, k_per_stratum);

// 使用 Algorithm L（更高效）
let samples = sample_slice_l(&data, k);
```

## API 文档

### ReservoirSampler

| 方法 | 说明 |
|------|------|
| `new(capacity)` | 创建指定容量的采样器 |
| `with_seed(capacity, seed)` | 使用随机种子创建（可重复结果） |
| `add(item)` | 添加元素 |
| `samples()` | 获取当前样本（引用） |
| `into_samples()` | 获取样本（消费采样器） |
| `processed_count()` | 已处理的元素数量 |
| `capacity()` | 水塘容量 |
| `len()` | 当前样本数量 |
| `is_empty()` | 检查是否为空 |
| `is_full()` | 检查是否已满 |
| `clear()` | 清空（保留容量） |
| `reset()` | 重置（包括种子） |
| `sample(iter)` | 从迭代器采样 |
| `sample_from_slice(slice)` | 从切片采样 |

### ReservoirSamplerL

| 方法 | 说明 |
|------|------|
| `new(capacity)` | 创建采样器 |
| `with_seed(capacity, seed)` | 使用随机种子创建 |
| `add(item)` | 添加元素 |
| `samples()` | 获取当前样本 |
| `into_samples()` | 获取样本（消费） |
| `processed_count()` | 已处理数量 |
| `capacity()` | 水塘容量 |
| `sample(iter)` | 从迭代器采样 |

### WeightedReservoirSampler

| 方法 | 说明 |
|------|------|
| `new(capacity)` | 创建采样器 |
| `with_seed(capacity, seed)` | 使用随机种子创建 |
| `add(item, weight)` | 添加带权重的元素 |
| `samples()` | 获取样本（引用） |
| `into_samples()` | 获取样本（消费） |
| `samples_with_priority()` | 获取带优先级的样本 |
| `processed_count()` | 已处理数量 |
| `capacity()` | 水塘容量 |
| `sample(iter)` | 从迭代器采样（返回 (item, weight) 元组） |

## 应用场景

- **大数据集采样**：从海量数据中抽取代表性样本
- **流式数据处理**：实时处理无法预知大小的数据流
- **随机抽样调查**：统计抽样、民意调查
- **机器学习**：随机批次选择、数据采样
- **日志分析**：从海量日志中随机抽取样本
- **测试数据生成**：随机选择测试样本
- **推荐系统**：根据权重随机推荐
- **负载均衡**：加权随机选择服务器

## 测试覆盖

30 个单元测试，覆盖：
- 基本采样功能
- 空数据边界条件
- k > n 边界条件
- k = n 边界条件
- k = 0 边界条件
- 单元素数据
- 均匀分布验证
- 处理计数
- 清空和重用
- Algorithm L 功能
- 加权采样功能
- 权重边界检查
- 分层采样
- 大数据集性能
- 大样本数量
- 字符串采样
- 结构体采样
- 文档测试

## 时间复杂度

| 算法 | 时间 | 空间 |
|------|------|------|
| Algorithm R | O(n) | O(k) |
| Algorithm L | O(k(1 + log(n/k))) | O(k) |
| Weighted | O(n log k) | O(k) |

## 许证证

MIT License