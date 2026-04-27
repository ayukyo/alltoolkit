# Reservoir Sampling Utils


Reservoir Sampling Utils - 水库采样工具集

提供多种水库采样算法实现，用于从未知大小或大数据流中进行随机采样。
所有算法均为 O(n) 时间复杂度和 O(k) 空间复杂度，其中 k 为采样大小。

核心算法:
- Algorithm R (经典水库采样)
- Algorithm L (高效水库采样)
- Weighted Reservoir Sampling (加权水库采样)
- Reservoir Sampling with Replacement (有放回采样)


## 功能

### 类

- **ReservoirSampler**: 经典水库采样算法 (Algorithm R)

适用场景:
- 从数据流中均匀随机采样 k 个元素
- 数据量未知或无法全部加载到内存

时间复杂度: O(n)
空间复杂度: O(k)

示例:
    >>> sampler = ReservoirSampler(3)
    >>> for item in range(10):
    
  方法: add, add_all, sample, reset, size ... (7 个方法)
- **FastReservoirSampler**: 高效水库采样算法 (Algorithm L)

由 Li (1994) 提出，比 Algorithm R 更高效。
使用跳跃技术减少随机数生成次数。

时间复杂度: O(n) 但实际操作更少
空间复杂度: O(k)
  方法: add, add_all, sample, reset, size ... (6 个方法)
- **WeightedReservoirSampler**: 加权水库采样 (Weighted Random Sampling)

每个元素有对应的权重，采样概率与权重成正比。
使用 Efraimidis & Spirakis (2006) 算法。

示例:
    >>> sampler = WeightedReservoirSampler(2)
    >>> sampler
  方法: add, add_all, sample, reset, size ... (6 个方法)
- **ReservoirSamplerWithReplacement**: 有放回水库采样

每个位置独立采样，允许重复元素。
适用于需要独立采样的场景。
  方法: add, add_all, sample, reset, size ... (6 个方法)
- **SamplingStats**: 采样统计信息
  方法: to_dict

### 函数

- **analyze_sample_distribution(sample**) - 分析采样结果的分布
- **stratified_reservoir_sample(items, k, strata_func**, ...) - 分层水库采样
- **two_pass_reservoir_sample(items, k, seed**) - 两遍扫描水库采样
- **reservoir_sample(items, k, seed**) - 从迭代器中采样的便捷函数
- **weighted_sample(items, k, seed**) - 加权采样的便捷函数
- **add(self, item**) - 添加一个元素到采样器
- **add_all(self, items**) - 批量添加元素
- **sample(self**) - 获取当前采样结果
- **reset(self, seed**) - 重置采样器
- **size(self**) - 采样大小

... 共 31 个函数

## 使用示例

```python
from mod import analyze_sample_distribution

# 使用 analyze_sample_distribution
result = analyze_sample_distribution()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
