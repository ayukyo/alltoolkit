# HyperLogLog Utils - 基数估计工具库

零外部依赖的 HyperLogLog 实现，用于高效估计大型数据集的唯一元素数量。

## 📖 简介

HyperLogLog 是一种概率算法，能够使用极小的内存估计大规模数据集的基数（唯一元素数量）。本库提供三种实现：

- **HyperLogLog**: 标准实现，适合已知规模的数据集
- **HyperLogLogPlusPlus**: Google 改进版，支持稀疏模式优化
- **SparseHyperLogLog**: 自动精度调整，适合不确定规模的数据集

## 🎯 特点

- ✅ **零外部依赖** - 纯 Python 标准库实现
- ✅ **多种哈希函数** - MurmurHash3、XXHash、SHA256
- ✅ **完整序列化** - 支持字节和文件持久化
- ✅ **集合操作** - 支持合并、交集估计、Jaccard 相似度
- ✅ **构建器 API** - 流畅接口，易于使用

## 📦 安装

```python
# 直接导入使用，无需安装依赖
from hyperloglog_utils import HyperLogLog
```

## 🚀 快速开始

### 基本使用

```python
from hyperloglog_utils import HyperLogLog

# 创建 HyperLogLog (precision 12, 误差约 1.6%)
hll = HyperLogLog(precision=12)

# 添加元素
hll.add("user_1")
hll.add("user_2")
hll.add("user_3")

# 获取估计的基数
estimate = hll.count()
print(f"估计的独立用户数: {estimate:.2f}")
```

### 批量添加

```python
# 使用 update 方法批量添加
users = [f"user_{i}" for i in range(10000)]
hll.update(users)

# 或使用工厂函数
hll = from_iterable(users, precision=12)
```

### 统计独立访客 (UV)

```python
# 网站访客统计
uv_counter = HyperLogLog(precision=14)  # 误差约 0.8%

# 记录每次访问
for visit in visits:
    uv_counter.add(visit.user_id)

# 获取 UV
uv = uv_counter.count()
```

### 合并多个数据集

```python
# 多天的 UV 数据
day1 = HyperLogLog(precision=12)
day2 = HyperLogLog(precision=12)
day3 = HyperLogLog(precision=12)

# 合并计算总 UV
total_uv = day1.merge(day2).merge(day3)

# 计算交集（连续访问用户）
intersection = day1.intersection_cardinality(day2)

# 计算相似度
jaccard = day1.jaccard_similarity(day2)
```

## 🔧 精度与内存

| 精度 | 寄存器数 | 内存 | 误差 |
|------|----------|------|------|
| 8 | 256 | 256B | 6.5% |
| 10 | 1024 | 1KB | 3.3% |
| 12 | 4096 | 4KB | 1.6% |
| 14 | 16384 | 16KB | 0.8% |
| 16 | 65536 | 64KB | 0.4% |

```python
# 查看内存估算
from hyperloglog_utils import estimate_memory

info = estimate_memory(14)
print(f"精度 14: {info['kilobytes']}KB, 误差 {info['relative_error_percent']}%")
```

## 💡 高级用法

### HyperLogLog++ (Google 改进版)

```python
from hyperloglog_utils import HyperLogLogPlusPlus

# 支持稀疏模式，小数据集更精确
hll_pp = HyperLogLogPlusPlus(precision=14)

# 少量数据时保持稀疏表示
for i in range(10):
    hll_pp.add(f"item_{i}")

print(f"稀疏模式: {hll_pp.is_sparse}")  # True
```

### 稀疏 HyperLogLog (自适应精度)

```python
from hyperloglog_utils import SparseHyperLogLog

# 从小精度开始，自动升级
shll = SparseHyperLogLog(initial_precision=6, max_precision=16)

# 小数据集使用低精度节省内存
# 大数据集自动升级到高精度
for i in range(50000):
    shll.add(f"item_{i}")

print(f"当前精度: {shll.precision}")
```

### 序列化

```python
# 序列化为字节
data = hll.to_bytes()

# 反序列化
restored = HyperLogLog.from_bytes(data)

# 文件持久化
hll.save("uv_data.hll")
loaded = HyperLogLog.load("uv_data.hll")
```

### 构建器 API

```python
from hyperloglog_utils import HyperLogLogBuilder

hll = (HyperLogLogBuilder()
       .precision(12)
       .with_hash('murmur')
       .with_items(['a', 'b', 'c'])
       .build())
```

## 📊 使用场景

- **网站 UV 统计** - 独立访客计数
- **数据库查询优化** - 预估结果集大小
- **网络流量分析** - IP 地址去重计数
- **大数据去重** - 快速估计唯一值数量
- **推荐系统** - 用户行为统计
- **监控系统** - 异常事件计数

## 🧪 测试

```bash
python hyperloglog_utils_test.py
```

## 📚 API 参考

### HyperLogLog 类

| 方法 | 说明 |
|------|------|
| `add(item)` | 添加元素 |
| `update(items)` | 批量添加 |
| `count()` | 获取估计基数 |
| `merge(other)` | 合并另一个 HLL |
| `intersection_cardinality(other)` | 估计交集大小 |
| `jaccard_similarity(other)` | 计算 Jaccard 相似度 |
| `to_bytes()` | 序列化为字节 |
| `from_bytes(data)` | 从字节反序列化 |
| `save(file)` | 保存到文件 |
| `load(file)` | 从文件加载 |
| `get_stats()` | 获取统计信息 |
| `clear()` | 清除所有数据 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `create_hll(precision, hash_func)` | 创建 HLL 实例 |
| `from_iterable(items, precision)` | 从集合创建 |
| `merge_multiple(hlls)` | 合并多个 HLL |
| `estimate_memory(precision)` | 估算内存使用 |
| `compare_precision(items, precisions)` | 比较不同精度 |

## 📄 许可证

MIT License