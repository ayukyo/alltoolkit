# Count-Min Sketch Utils

高效的概率数据结构，用于频率估计和 Heavy Hitters 检测。

## 概述

Count-Min Sketch 是一个次线性空间的数据结构，可以在有限内存中估计数据流中元素的频率。它提供以下特性：

- **空间效率**: 使用固定大小内存，不随数据量增长
- **快速操作**: O(d) 时间复杂度，d 为哈希函数数量
- **无低估**: 估计值永远不小于真实值
- **可合并**: 支持多个 Sketch 的合并操作

## 安装

将 `mod.rs` 文件复制到你的项目中，并重命名为 `count_min_sketch.rs` 或直接使用。

## 快速开始

```rust
mod count_min_sketch;
use count_min_sketch::CountMinSketch;

fn main() {
    // 创建 Count-Min Sketch
    // epsilon = 0.01 (误差参数)
    // delta = 0.001 (失败概率)
    let mut cms = CountMinSketch::new(0.01, 0.001);
    
    // 添加元素
    cms.add(&"apple");
    cms.add(&"banana");
    cms.add(&"apple");
    
    // 查询频率
    println!("apple: {} 次", cms.count(&"apple")); // >= 2
    println!("banana: {} 次", cms.count(&"banana")); // >= 1
    
    // 检查存在性
    if cms.contains(&"apple") {
        println!("apple 存在");
    }
}
```

## API 文档

### CountMinSketch

#### 构造函数

```rust
// 使用误差参数创建
let cms = CountMinSketch::new(epsilon, delta);

// 使用指定维度创建
let cms = CountMinSketch::with_dimensions(width, depth);

// 使用容量和误差率创建
let cms = CountMinSketch::with_capacity(expected_items, error_rate);

// 默认参数
let cms = CountMinSketch::default();
```

#### 方法

| 方法 | 说明 |
|------|------|
| `add(&item)` | 添加元素，计数 +1 |
| `add_n(&item, n)` | 添加元素，计数 +n |
| `count(&item)` | 查询元素估计频率 |
| `count_opt(&item)` | 查询频率，为 0 时返回 None |
| `contains(&item)` | 检查元素是否存在 |
| `remove(&item)` | 减少计数（可能导致不一致） |
| `clear()` | 清空所有计数 |
| `merge(&other)` | 合并另一个 Sketch |
| `similarity(&other)` | 计算与另一个 Sketch 的相似度 |
| `total_count()` | 获取总计数 |
| `memory_usage()` | 获取内存使用（字节） |
| `error_bound()` | 获取当前误差上界 |
| `stats()` | 获取统计信息 |
| `snapshot()` | 获取计数器快照 |
| `from_snapshot()` | 从快照恢复 |

### HeavyHitters

追踪数据流中的高频元素：

```rust
use count_min_sketch::HeavyHitters;

// 追踪前 5 高频元素
let mut hh: HeavyHitters<&str> = HeavyHitters::new(0.01, 0.001, 5);

for _ in 0..100 { hh.add("frequent"); }
for _ in 0..50 { hh.add("medium"); }
for _ in 0..10 { hh.add("rare"); }

// 获取高频元素
let top = hh.get_top();
for (item, count) in top {
    println!("{}: ~{} 次", item, count);
}
```

### FrequencyCounter

追踪满足阈值的高频元素：

```rust
use count_min_sketch::FrequencyCounter;

// 阈值为 50 次
let mut fc: FrequencyCounter<&str> = FrequencyCounter::new(0.01, 0.001, 50);

for _ in 0..100 { fc.add("common"); }
for _ in 0..30 { fc.add("less_common"); }

// 只返回计数 >= 50 的元素
let frequent = fc.get_frequent();
```

## 使用场景

### 1. 网站访问统计

```rust
let mut cms = CountMinSketch::new(0.001, 0.0001);

for url in access_logs {
    cms.add(&url);
}

println!("首页访问: {} 次", cms.count(&"/home"));
```

### 2. 网络流量监控

```rust
let mut cms = CountMinSketch::with_capacity(100_000, 0.01);

for packet in network_stream {
    cms.add_n(&packet.source_ip, packet.size);
}

// 检测高流量 IP
if cms.count(&suspicious_ip) > threshold {
    alert!("异常流量检测!");
}
```

### 3. 分布式计数

```rust
// 多个节点各自收集数据
let mut node1 = CountMinSketch::with_dimensions(1000, 5);
let mut node2 = CountMinSketch::with_dimensions(1000, 5);

// ... 收集数据 ...

// 合并到中心节点
node1.merge(&node2).unwrap();
```

### 4. 实时热门内容

```rust
let mut hh: HeavyHitters<u64> = HeavyHitters::new(0.01, 0.001, 10);

for post_id in stream {
    hh.add(post_id);
}

// 获取当前热门内容
let trending = hh.get_top();
```

## 性能特征

| 操作 | 时间复杂度 | 空间复杂度 |
|------|------------|------------|
| add | O(d) | O(1) |
| count | O(d) | O(1) |
| merge | O(w × d) | O(1) |
| clear | O(w × d) | O(1) |

其中：
- w = 宽度（每行计数器数量）
- d = 深度（哈希函数数量）

## 误差分析

Count-Min Sketch 的误差具有以下特性：

- **误差上限**: ε × N（N 为总计数）
- **成功概率**: ≥ 1 - δ
- **无低估**: 估计值 ≥ 真实值

参数选择：
- **高精度**: ε = 0.001, δ = 0.0001（内存较大）
- **平衡**: ε = 0.01, δ = 0.001（推荐）
- **低内存**: ε = 0.1, δ = 0.01（误差较大）

## 测试

```bash
cd Rust/count_min_sketch_utils
rustc --test mod.rs && ./mod
```

运行示例：

```bash
rustc main.rs && ./main
```

## 许可证

MIT License

## 参考资料

- [Count-Min Sketch - Wikipedia](https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch)
- Cormode, G., & Muthukrishnan, S. (2005). "An improved data stream summary: the count-min sketch and its applications"