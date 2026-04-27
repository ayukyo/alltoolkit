# Kd Tree Utils


KD树工具模块 (KD-Tree Utilities)
==============================

提供KD树的完整实现，支持多维空间索引和最近邻搜索。
零外部依赖，纯Python实现。

核心功能：
- KD树的构建和插入
- k近邻搜索 (k-NN)
- 范围查询
- 最近邻搜索
- 删除节点
- 树的平衡检查

作者: AllToolkit 自动生成
日期: 2026-04-22


## 功能

### 类

- **KDNode**: KD树节点
- **KDTree**: KD树实现

一种用于组织k维空间中点的空间分区数据结构。
支持高效的最近邻搜索、范围查询和k近邻查询。

时间复杂度：
- 构建: O(n log n)
- 插入: O(log n) 平均
- 搜索: O(log n) 平均
- 删除: O(log n) 平均

示例：
    >>> tree = KDTree(dimension=2)
    >>> tree
  方法: insert, build, nearest_neighbor, k_nearest_neighbors, range_query ... (15 个方法)
- **KDTreeBuilder**: KD树构建器（流式API）

示例：
    >>> tree = (KDTreeBuilder(2)
    
  方法: add, add_many, build, clear

### 函数

- **create_kd_tree(points, dimension, distance_metric**) - 便捷函数：从点列表创建KD树
- **nearest_neighbor_search(points, query, k**, ...) - 便捷函数：在点集合中查找最近邻
- **insert(self, point, data**) - 插入一个点到KD树中
- **build(self, points**) - 从点列表构建平衡的KD树
- **nearest_neighbor(self, query**) - 查找最近的邻居
- **k_nearest_neighbors(self, query, k**) - 查找k个最近的邻居
- **range_query(self, query**) - 范围查询：查找指定矩形范围内的所有点
- **radius_query(self, center, radius**) - 圆形/球形范围查询：查找距离中心点指定半径内的所有点
- **find(self, point**) - 查找特定点
- **delete(self, point**) - 从KD树中删除一个点

... 共 28 个函数

## 使用示例

```python
from mod import create_kd_tree

# 使用 create_kd_tree
result = create_kd_tree()
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
