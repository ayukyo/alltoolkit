# AVL Tree Utils - Python AVL 树工具模块

**零依赖的自平衡二叉搜索树实现，仅使用 Python 标准库**

提供完整的 AVL 树实现，支持插入、删除、查找、遍历、范围查询、顺序统计等操作。

## 📦 模块特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **自平衡** - 自动维护 AVL 平衡性质
- ✅ **O(log n) 操作** - 查找、插入、删除均为对数时间
- ✅ **顺序统计** - 支持第 k 小查询和排名
- ✅ **范围查询** - 高效的范围查询和计数
- ✅ **键值存储** - 支持键关联值
- ✅ **完整测试** - 100+ 测试用例覆盖

## 🚀 快速开始

### 导入模块

```python
from avl_tree_utils import AVLTree, create_avl_tree
```

### 基本使用

```python
# 创建 AVL 树
tree = AVLTree()

# 插入元素
tree.insert(10)
tree.insert(5)
tree.insert(15)

# 查找
tree.contains(10)  # True
tree.search(5)     # AVLNode(5)

# 最小最大值
tree.find_min().key  # 5
tree.find_max().key  # 15

# 删除
tree.delete(10)  # True

# 转为有序列表
tree.to_list()  # [5, 15]
```

### 带值的 AVL 树（键值存储）

```python
tree = AVLTree()
tree.insert("apple", {"color": "red", "price": 1.5})
tree.insert("banana", {"color": "yellow", "price": 0.8})

tree.get_value("apple")  # {"color": "red", "price": 1.5}
tree.to_dict()  # {"apple": {...}, "banana": {...}}
```

### 范围查询

```python
tree = create_avl_tree([(i, None) for i in range(1, 21)])

tree.range_query(5, 10)  # [5, 6, 7, 8, 9, 10]
tree.count_range(5, 15)  # 11

tree.find_floor(7.5).key   # 7
tree.find_ceiling(7.5).key # 8
```

### 顺序统计

```python
tree = create_avl_tree([(i, None) for i in [10, 5, 15, 3, 8, 12]])

tree.find_kth(1).key  # 3（第 1 小）
tree.find_kth(3).key  # 8（第 3 小）
tree.rank(10)         # 4（排名）
```

### 遍历

```python
tree = create_avl_tree([(i, None) for i in [10, 5, 15, 3, 8]])

# 中序遍历（升序）
list(tree.inorder())  # [3, 5, 8, 10, 15]

# 前序遍历
list(tree.preorder())  # [10, 5, 3, 8, 15]

# 后序遍历
list(tree.postorder())  # [3, 8, 5, 15, 10]

# 层序遍历
list(tree.level_order())  # [10, 5, 15, 3, 8]
```

### 工具函数

```python
from avl_tree_utils import (
    from_sorted_list, merge_avl_trees, split_avl_tree,
    dict_to_avl_tree, find_common_elements, get_tree_statistics
)

# 从有序列表最优构建
tree = from_sorted_list([1, 2, 3, 4, 5, 6, 7])

# 合并两个树
merged = merge_avl_trees(tree1, tree2)

# 分割树
left, right = split_avl_tree(tree, 10)

# 字典转树
tree = dict_to_avl_tree({"a": 1, "b": 2})

# 统计信息
stats = get_tree_statistics(tree)
```

## 📚 API 文档

### AVLTree 类

| 方法 | 描述 | 时间复杂度 |
|------|------|-----------|
| `insert(key, value)` | 插入键值 | O(log n) |
| `delete(key)` | 删除键 | O(log n) |
| `search(key)` | 查找节点 | O(log n) |
| `contains(key)` | 检查存在 | O(log n) |
| `find_min()` | 最小节点 | O(log n) |
| `find_max()` | 最大节点 | O(log n) |
| `find_floor(key)` | ≤ key 最大节点 | O(log n) |
| `find_ceiling(key)` | ≥ key 最小节点 | O(log n) |
| `find_kth(k)` | 第 k 小节点 | O(log n) |
| `rank(key)` | 键排名 | O(log n) |
| `count_range(low, high)` | 范围计数 | O(log n) |
| `range_query(low, high)` | 范围查询 | O(log n + k) |
| `delete_min()` | 删除最小 | O(log n) |
| `delete_max()` | 删除最大 | O(log n) |
| `predecessor(key)` | 前驱键 | O(log n) |
| `successor(key)` | 后继键 | O(log n) |
| `depth(key)` | 键深度 | O(log n) |
| `path_to(key)` | 根到键路径 | O(log n) |
| `inorder()` | 中序遍历 | O(n) |
| `preorder()` | 前序遍历 | O(n) |
| `postorder()` | 后序遍历 | O(n) |
| `level_order()` | 层序遍历 | O(n) |
| `to_list()` | 转有序列表 | O(n) |
| `to_dict()` | 转字典 | O(n) |
| `is_valid_avl()` | 验证 AVL 性质 | O(n) |
| `visualize()` | 可视化字符串 | O(n) |

### 属性

| 属性 | 描述 |
|------|------|
| `size` | 节点数量 |
| `height` | 树高度 |
| `is_empty` | 是否为空 |
| `root` | 根节点 |
| `allow_duplicates` | 是否允许重复 |

### 工具函数

| 函数 | 描述 |
|------|------|
| `create_avl_tree(items, allow_duplicates)` | 创建并初始化树 |
| `from_sorted_list(keys, values)` | 从有序列表最优构建 |
| `merge_avl_trees(tree1, tree2)` | 合并两个树 |
| `split_avl_tree(tree, key)` | 分割树 |
| `avl_tree_to_dict(tree)` | 树转字典 |
| `dict_to_avl_tree(dict)` | 字典转树 |
| `find_common_elements(tree1, tree2)` | 找公共元素 |
| `find_difference(tree1, tree2)` | 找差集 |
| `validate_avl_tree(tree)` | 验证树 |
| `get_tree_statistics(tree)` | 获取统计信息 |

## 🧪 测试

```bash
# 运行测试
python Python/avl_tree_utils/avl_tree_utils_test.py
```

测试覆盖：
- AVLNode 基本操作
- 插入删除查找
- 范围查询
- 顺序统计
- 遍历方法
- 自动平衡（LL、RR、LR、RL 旋转）
- 边界值（空树、单节点、大树、负数、浮点、字符串）
- 工具函数
- 性能测试

## 📁 文件结构

```
Python/avl_tree_utils/
├── mod.py               # 主模块（AVL 树实现）
├── avl_tree_utils_test.py  # 测试套件
├── README.md            # 文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## 💡 使用场景

1. **数据库索引** - 高效的键值存储和查询
2. **排序算法** - 通过中序遍历获得有序序列
3. **范围查询** - 快速获取区间内的元素
4. **优先队列** - 通过 find_min/max 实现
5. **集合操作** - 合并、分割、交集、差集
6. **滑动窗口** - 范围查询支持

## 📊 性能特点

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 插入 | O(log n) | O(1) |
| 删除 | O(log n) | O(1) |
| 查找 | O(log n) | O(1) |
| 范围查询 | O(log n + k) | O(k) |
| 遍历 | O(n) | O(1) |

**高度保证**：AVL 树高度最多为 `1.44 * log2(n + 2)`

## 📄 许可证

MIT License - AllToolkit 项目的一部分

---

**作者**: AllToolkit  
**版本**: 1.0.0  
**日期**: 2026-04-18