# B+ Tree Utils

B+ 树数据结构实现，零依赖，支持高效范围查询。

## 功能特性

- **B+ 树实现**: 完整 B+ 树数据结构
- **范围查询**: 高效的范围查询支持
- **批量插入**: 批量数据插入优化
- **持久化**: JSON 序列化支持
- **可配置**: 自定义节点大小

## 快速开始

```python
from bplustree_utils.mod import BPlusTree

# 创建 B+ 树（节点大小默认为 4）
tree = BPlusTree(order=4)

# 插入数据
tree.insert(10, "value_10")
tree.insert(20, "value_20")
tree.insert(5, "value_5")

# 查询
value = tree.search(10)  # "value_10"

# 范围查询
results = tree.range_query(5, 15)  # [(5, "value_5"), (10, "value_10")]
```

## 使用示例

### 基础操作

```python
from bplustree_utils.mod import BPlusTree

tree = BPlusTree(order=4)

# 插入
tree.insert(1, "one")
tree.insert(2, "two")
tree.insert(3, "three")

# 查询
value = tree.search(2)  # "two"

# 删除
tree.delete(2)
tree.search(2)  # None

# 检查键是否存在
tree.contains(1)  # True
```

### 范围查询

```python
# 插入数据
for i in range(100):
    tree.insert(i, f"value_{i}")

# 范围查询
results = tree.range_query(10, 20)
# [(10, "value_10"), (11, "value_11"), ..., (20, "value_20")]

# 开区间查询
results = tree.range_query(10, 20, include_start=False, include_end=False)
# [(11, "value_11"), ..., (19, "value_19")]
```

### 批量插入

```python
# 批量插入
data = {i: f"v{i}" for i in range(50)}
tree.insert_batch(data)
```

### 遍历

```python
# 正序遍历
for key, value in tree.iterate():
    print(key, value)

# 逆序遍历
for key, value in tree.iterate_reverse():
    print(key, value)

# 获取所有键
keys = tree.keys()

# 获取所有值
values = tree.values()
```

### 统计信息

```python
# 统计
stats = tree.stats()
print(stats['size'])         # 元素数量
print(stats['height'])       # 树高度
print(stats['leaf_count'])   # 叶节点数
print(stats['internal_count'])  # 内部节点数
```

### 序列化

```python
# 导出为 JSON
json_str = tree.to_json()

# 从 JSON 导入
tree2 = BPlusTree.from_json(json_str)
```

## API 参考

### BPlusTree

| 方法 | 说明 |
|------|------|
| `insert(key, value)` | 插入键值对 |
| `insert_batch(data)` | 批量插入 |
| `search(key)` | 查询键 |
| `contains(key)` | 检查键是否存在 |
| `delete(key)` | 删除键 |
| `range_query(start, end)` | 范围查询 |
| `iterate()` | 正序遍历 |
| `iterate_reverse()` | 逆序遍历 |
| `keys()` | 所有键 |
| `values()` | 所有值 |
| `min_key()` | 最小键 |
| `max_key()` | 最大键 |
| `stats()` | 统计信息 |
| `to_json()` | 序列化 |
| `from_json(json_str)` | 反序列化 |

## B+ 树特性

- **所有数据存储在叶节点**: 内部节点只存索引
- **叶节点链表连接**: 便于范围查询
- **自动平衡**: 插入删除时自动调整
- **高效查找**: O(log n) 时间复杂度

## 应用场景

- **数据库索引**: B+ 树是数据库主要索引结构
- **文件系统**: 文件索引管理
- **范围查询**: 需要高效范围查询的场景
- **排序存储**: 保持有序的数据存储

---

**测试覆盖**: 完整测试套件，覆盖插入、删除、查询、范围查询等