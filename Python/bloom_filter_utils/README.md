# Bloom Filter Utils - 布隆过滤器工具库

高效的布隆过滤器实现，零外部依赖，纯 Python 标准库。

## 特性

- **多种布隆过滤器实现**
  - `BloomFilter`: 标准布隆过滤器
  - `ScalableBloomFilter`: 可扩展布隆过滤器（自动扩容）
  - `CountingBloomFilter`: 计数布隆过滤器（支持删除）

- **多种哈希函数**
  - MurmurHash3 (32-bit)
  - FNV-1a (32-bit)
  - DJB2
  - SHA-256

- **完整功能**
  - 自动计算最优参数
  - 序列化/反序列化
  - 文件持久化
  - 统计信息和分析工具
  - 构建器模式（流畅 API）

## 快速开始

### 基础用法

```python
from bloom_filter_utils import BloomFilter

# 创建布隆过滤器（预期 1000 元素，假阳性率 1%）
bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)

# 添加元素
bf.add("hello")
bf.add("world")

# 查询元素
print("hello" in bf)  # True
print("foo" in bf)    # False
```

### 可扩展布隆过滤器

```python
from bloom_filter_utils import ScalableBloomFilter

# 自动扩容
sbf = ScalableBloomFilter(initial_capacity=100, false_positive_rate=0.01)

# 添加超过初始容量的元素
for i in range(10000):
    sbf.add(f"item_{i}")

# 所有元素都可查询
print(f"item_5000" in sbf)  # True
```

### 计数布隆过滤器

```python
from bloom_filter_utils import CountingBloomFilter

# 支持删除
cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01)

cbf.add("hello")
cbf.add("hello")  # 可以多次添加
print(cbf.count("hello"))  # 2

cbf.remove("hello")  # 可以删除
print("hello" in cbf)  # True (还有一次)
```

### 构建器模式

```python
from bloom_filter_utils import BloomFilterBuilder

bf = (BloomFilterBuilder()
      .expected_elements(1000)
      .false_positive_rate(0.01)
      .with_hash('murmur')
      .with_items(['a', 'b', 'c'])
      .build())
```

### 序列化

```python
# 序列化为字节
data = bf.to_bytes()

# 反序列化
bf2 = BloomFilter.from_bytes(data)

# 保存到文件
bf.save('filter.dat')
bf3 = BloomFilter.load('filter.dat')
```

## 核心组件

### BloomFilter

标准布隆过滤器，适合已知元素数量的场景。

| 参数 | 说明 |
|------|------|
| `expected_elements` | 预期元素数量 |
| `false_positive_rate` | 假阳性率 (0 < p < 1) |
| `hash_func` | 哈希函数 ('murmur', 'fnv', 'djb2', 'sha256') |

特性：
- 空间效率高
- O(k) 查询时间
- 无假阴性
- 可能假阳性

### ScalableBloomFilter

可扩展布隆过滤器，适合元素数量未知或增长的场景。

配置参数：
- `initial_capacity`: 初始容量
- `growth_factor`: 容量增长因子 (默认 2.0)
- `fp_rate_factor`: 假阳性率衰减因子 (默认 0.9)

特性：
- 自动扩容
- 假阳性率随过滤器数量增加而降低
- 无假阴性

### CountingBloomFilter

计数布隆过滤器，支持删除操作。

| 参数 | 说明 |
|------|------|
| `counter_bits` | 计数器位数 (4, 8, 16) |

特性：
- 支持删除
- 支持计数估计
- 计数器溢出保护

## 工具函数

### 内存估算

```python
from bloom_filter_utils import estimate_memory_usage

stats = estimate_memory_usage(1000000, 0.01)
print(f"需要 {stats['megabytes']:.2f} MB")
```

### 哈希函数对比

```python
from bloom_filter_utils import compare_hash_functions

results = compare_hash_functions(items, queries, 1000)
for name, data in results.items():
    print(f"{name}: 添加 {data['add_time_ms']}ms, 假阳性率 {data['actual_fp_rate']}")
```

## 使用场景

1. **数据去重** - URL、用户ID、文档ID 去重
2. **缓存穿透防护** - 快速判断数据是否可能存在缓存中
3. **垃圾过滤** - 垃圾邮件关键词、恶意URL过滤
4. **数据库优化** - 减少不必要的数据库查询
5. **推荐系统** - 已推荐内容去重

## 性能特点

| 元素数量 | 假阳性率 | 内存使用 | 哈希数 |
|----------|----------|----------|--------|
| 1,000 | 1% | ~1.2 KB | 7 |
| 10,000 | 1% | ~12 KB | 7 |
| 100,000 | 1% | ~120 KB | 7 |
| 1,000,000 | 1% | ~1.2 MB | 7 |
| 1,000,000 | 0.1% | ~1.8 MB | 10 |

## 测试

```bash
cd bloom_filter_utils
python bloom_filter_utils_test.py
```

测试覆盖：
- 哈希函数测试
- BitArray 操作测试
- 三种布隆过滤器测试
- 序列化/反序列化测试
- 边界情况测试
- 性能测试

## 示例

```bash
python examples.py          # 运行所有示例
python examples.py basic    # 运行特定示例
```

## 文件结构

```
bloom_filter_utils/
├── bloom_filter_utils.py      # 主模块
├── bloom_filter_utils_test.py # 测试文件
├── examples.py                # 使用示例
└── README.md                  # 本文档
```

## API 参考

### BloomFilter

```python
class BloomFilter:
    def __init__(self, expected_elements=10000, false_positive_rate=0.01, hash_func='murmur'):
        pass
    
    def add(self, item) -> None:
        """添加元素"""
    
    def __contains__(self, item) -> bool:
        """检查元素是否可能存在"""
    
    def might_contain(self, item) -> bool:
        """检查元素是否可能存在"""
    
    def update(self, items) -> 'BloomFilter':
        """批量添加"""
    
    def clear(self) -> None:
        """清除所有元素"""
    
    def get_stats(self) -> BloomFilterStats:
        """获取统计信息"""
    
    def to_bytes(self) -> bytes:
        """序列化"""
    
    @classmethod
    def from_bytes(cls, data) -> 'BloomFilter':
        """反序列化"""
    
    def save(self, file) -> None:
        """保存到文件"""
    
    @classmethod
    def load(cls, file) -> 'BloomFilter':
        """从文件加载"""
    
    def union(self, other) -> 'BloomFilter':
        """并集操作"""
    
    def intersect(self, other) -> 'BloomFilter':
        """交集操作"""
```

### ScalableBloomFilter

```python
class ScalableBloomFilter:
    def __init__(self, config=None, **kwargs):
        pass
    
    def add(self, item) -> None:
        """添加元素"""
    
    def __contains__(self, item) -> bool:
        """检查元素"""
    
    def clear(self) -> None:
        """清除"""
    
    def get_stats(self) -> dict:
        """统计信息"""
    
    def to_bytes(self) -> bytes:
        """序列化"""
    
    @classmethod
    def from_bytes(cls, data) -> 'ScalableBloomFilter':
        """反序列化"""
```

### CountingBloomFilter

```python
class CountingBloomFilter:
    def __init__(self, expected_elements=10000, false_positive_rate=0.01, hash_func='murmur', counter_bits=4):
        pass
    
    def add(self, item) -> bool:
        """添加元素（返回是否成功）"""
    
    def remove(self, item) -> bool:
        """删除元素（返回是否成功）"""
    
    def __contains__(self, item) -> bool:
        """检查元素"""
    
    def count(self, item) -> int:
        """估计计数"""
    
    def get_stats(self) -> dict:
        """统计信息"""
```

## 许可

MIT License