# Bloom Filter Utils 🌸

布隆过滤器工具模块 - 空间高效的概率数据结构，用于快速判断元素是否存在。

## 功能特性

- **布隆过滤器** - 空间高效的成员检测
- **假阳性可控** - 可设置期望的假阳性率
- **最优参数计算** - 自动计算最优位数组大小和哈希函数数量
- **序列化支持** - 支持导出/导入状态
- **统计信息** - 元素数量、填充率、预估假阳性率

## 快速开始

```python
from bloom_filter_utils.mod import BloomFilter

# 创建布隆过滤器（预期10000个元素，假阳性率1%）
bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)

# 添加元素
bf.add("user@example.com")
bf.add("admin@example.com")

# 检查元素是否存在
print(bf.contains("user@example.com"))  # True
print(bf.contains("unknown@example.com"))  # False（可能存在假阳性）

# 批量添加
bf.add_batch(["item1", "item2", "item3"])
```

## 核心类

### BloomFilter

```python
class BloomFilter:
    def __init__(self, expected_items: int = 10000, false_positive_rate: float = 0.01):
        """
        初始化布隆过滤器
        
        Args:
            expected_items: 预期元素数量
            false_positive_rate: 期望的假阳性率 (0-1之间)
        """
```

### 主要方法

| 方法 | 说明 |
|------|------|
| `add(item)` | 添加元素 |
| `contains(item)` | 检查元素是否可能存在 |
| `add_batch(items)` | 批量添加元素 |
| `clear()` | 清空过滤器 |
| `export_state()` | 导出状态（用于持久化） |
| `import_state(state)` | 导入状态 |
| `estimated_false_positive_rate()` | 预估当前假阳性率 |
| `is_full()` | 检查是否已满 |

## 使用场景

### 缓存穿透防护

```python
# 预加载所有有效 key 到布隆过滤器
bf = BloomFilter(expected_items=100000)
for key in db.get_all_keys():
    bf.add(key)

# 查询前先检查
def get_user(user_id):
    if not bf.contains(user_id):
        return None  # 一定不存在，直接返回
    return db.query(user_id)  # 可能存在，查询数据库
```

### URL 去重

```python
bf = BloomFilter(expected_items=1000000)

def should_crawl(url):
    if bf.contains(url):
        return False  # 已爬过
    bf.add(url)
    return True
```

## 性能特点

| 特性 | 说明 |
|------|------|
| 空间复杂度 | O(m)，m 为位数组大小 |
| 时间复杂度 | O(k)，k 为哈希函数数量 |
| 假阳性 | 可能存在 |
| 假阴性 | 不存在 |
| 删除操作 | 不支持（标准布隆过滤器） |

## 数学原理

**最优位数组大小：**
```
m = -n * ln(p) / (ln(2))^2
```
- n: 预期元素数量
- p: 假阳性率

**最优哈希函数数量：**
```
k = (m/n) * ln(2)
```

## 测试

```bash
python Python/bloom_filter_utils/bloom_filter_utils_test.py
```

## 许可证

MIT License