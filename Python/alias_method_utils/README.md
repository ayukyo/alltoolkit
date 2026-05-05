# alias_method_utils - Alias Method for O(1) Weighted Random Sampling

Walker's Alias Method for efficient weighted random sampling.
After O(n) preprocessing, each sample can be drawn in O(1) time.

## 功能特点

- **O(1) 采样时间**：预处理后每次采样仅需常数时间
- **O(n) 预处理**：构建 alias 表需要线性时间
- **零外部依赖**：纯 Python 标准库实现
- **线程安全**：支持自定义随机数生成器
- **完整统计**：概率查询、权重属性、分布验证

## 使用场景

- 游戏开发：掉落表、生成概率、怪物刷新率
- 蒙特卡洛模拟：加权随机采样
- A/B 测试框架：流量分配
- 负载均衡：加权服务器选择
- 自然语言处理：词分布采样

## 快速开始

```python
from alias_method_utils import AliasMethod, WeightedRandomPicker

# 基本用法
weights = [1, 2, 3, 4]  # 权重比例
alias = AliasMethod(weights)

# 单次采样
sample = alias.sample()  # 返回索引 0-3

# 多次采样
samples = alias.sample_n(10)  # 返回 10 个索引

# 带数据采样
picker = WeightedRandomPicker(['apple', 'banana', 'orange'], [1, 2, 1])
fruit = picker.pick()  # 'banana' 概率最高
```

## API 参考

### AliasMethod

```python
alias = AliasMethod(weights, normalize=True)
```

**参数：**
- `weights`: 权重序列（非负数）
- `normalize`: 是否归一化权重（默认 True）

**方法：**
- `sample()`: 返回一个采样索引
- `sample_n(n, replacement=True)`: 返回 n 个采样索引
- `get_probability(i)`: 查询索引 i 的概率
- `probabilities`: 概率列表属性
- `weights`: 权重列表属性

### WeightedRandomPicker

```python
picker = WeightedRandomPicker(items, weights)
```

**方法：**
- `pick()`: 返回一个采样项
- `pick_n(n)`: 返回 n 个采样项
- `get_item_probability(item)`: 查询项概率

## 性能对比

| 方法 | 预处理 | 单次采样 |
|------|--------|----------|
| Alias Method | O(n) | **O(1)** |
| 线性搜索 | O(1) | O(n) |
| 二分搜索 | O(n) | O(log n) |

对于高频采样场景（如游戏掉落），Alias Method 显著优于其他方法。

## 测试覆盖

- **52 个单元测试，100% 通过率**
- 测试内容：
  - 基本采样、概率验证
  - 边界值（空权重、零权重、负权重）
  - 无重复采样、批量采样
  - 分布均匀性验证

## 许可证

MIT License