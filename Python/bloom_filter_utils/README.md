# Bloom Filter Utils | 布隆过滤器工具集

零依赖的高效布隆过滤器 Python 实现，用于快速判断元素是否在集合中。

## 特点

- **零外部依赖**：纯 Python 标准库实现
- **空间高效**：比传统集合节省 90%+ 内存
- **快速查询**：O(k) 时间复杂度
- **可配置误判率**：根据需求平衡空间与精度
- **线程安全**：支持多线程并发访问
- **支持序列化**：可持久化存储和恢复

## 安装使用

无需安装依赖，直接复制 `mod.py` 到项目中即可使用。

```python
from mod import BloomFilter

# 创建过滤器
bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)

# 添加元素
bf.add("example.com")

# 检查存在
if "example.com" in bf:
    print("可能已存在")
```

## 核心类

### BloomFilter

标准布隆过滤器，适用于不需要删除元素的场景。

```python
from mod import BloomFilter

# 创建：预期 10000 元素，误判率 1%
bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)

# 添加元素
bf.add("item1")
bf.add(b"bytes_data")  # 支持字节

# 检查存在
print("item1" in bf)  # True
print("unknown" in bf)  # False（一定不存在）

# 获取统计信息
print(f"元素数量: {len(bf)}")
print(f"误判率: {bf.estimated_false_positive_rate:.4f}")
print(f"负载因子: {bf.load_factor:.4f}")

# 序列化
data = bf.serialize()
bf2 = BloomFilter.deserialize(data)

# 集合操作
union = bf1.union(bf2)      # 并集
inter = bf1.intersection(bf2)  # 交集

# 清空
bf.clear()
```

### CountingBloomFilter

计数布隆过滤器，支持删除操作。

```python
from mod import CountingBloomFilter

cbf = CountingBloomFilter(expected_items=1000)

# 添加
cbf.add("item")

# 删除
cbf.remove("item")

# 计数
cbf.add("item", count=3)  # 添加多次
print(cbf.count("item"))  # 估算次数
```

### ScalableBloomFilter

可扩展布隆过滤器，自动扩容。

```python
from mod import ScalableBloomFilter

sbf = ScalableBloomFilter(initial_capacity=100)

# 自动扩展到任意大小
for i in range(100000):
    sbf.add(f"item_{i}")

# 自动去重
sbf.add("same")
sbf.add("same")
print(len(sbf))  # 1
```

## 便捷函数

```python
from mod import create_filter, create_scalable, estimate_size

# 创建标准过滤器
bf = create_filter(expected_items=10000, false_positive_rate=0.01)

# 创建可扩展过滤器
sbf = create_scalable(initial_capacity=1000)

# 估算资源需求
info = estimate_size(1000000, 0.01)
print(f"需要 {info['mb']} MB 内存")
print(f"需要 {info['hash_functions']} 个哈希函数")
```

## 使用场景

### 1. URL 去重（爬虫）

```python
bf = BloomFilter(expected_items=1000000, false_positive_rate=0.001)

visited_urls = []  # 已访问 URL
for url in new_urls:
    if url in bf:
        continue  # 跳过已访问
    bf.add(url)
    visited_urls.append(url)
    # 爬取 URL...
```

### 2. 缓存穿透防护

```python
# 将所有有效 key 存入布隆过滤器
valid_keys = BloomFilter(expected_items=100000)
for key in database.get_all_keys():
    valid_keys.add(key)

def get(key):
    # 先检查布隆过滤器
    if key not in valid_keys:
        return None  # 一定不存在，避免查数据库
    return cache.get(key) or database.get(key)
```

### 3. 垃圾邮件过滤

```python
spam_keywords = BloomFilter(expected_items=10000)
for word in load_spam_keywords():
    spam_keywords.add(word.lower())

def is_spam(content):
    for word in content.lower().split():
        if word in spam_keywords:
            return True
    return False
```

## 性能参考

| 元素数量 | 误判率 | 内存使用 | 哈希函数 |
|---------|--------|---------|---------|
| 10,000  | 1%     | ~12 KB  | 7       |
| 100,000 | 1%     | ~120 KB | 7       |
| 1,000,000 | 1%   | ~1.2 MB | 7       |
| 10,000,000 | 1%  | ~12 MB  | 7       |
| 100,000,000 | 1% | ~120 MB | 7       |

## 文件说明

```
bloom_filter_utils/
├── mod.py       # 核心实现
├── test.py      # 测试套件
├── examples.py  # 使用示例
└── README.md    # 本文档
```

## 运行测试

```bash
cd bloom_filter_utils
python test.py
```

## 运行示例

```bash
cd bloom_filter_utils
python examples.py
```

## 数学原理

布隆过滤器使用 k 个哈希函数，将元素映射到 m 位的数组中：

- 添加：对元素计算 k 个哈希值，设置对应的位
- 查询：检查 k 个位是否都被设置
- 特性：零假阴性（不会漏判），可能假阳性（可能误判）

最优参数计算：
- 位数组大小：`m = -n * ln(p) / (ln(2))²`
- 哈希函数数：`k = m / n * ln(2)`

## 许可证

MIT License