# Splay Tree Utils


Splay Tree (伸展树) 工具模块

提供完整的 Splay Tree 数据结构实现，支持：
- 插入、删除、查找
- 范围查询
- 序列操作（分割、合并）
- 最近邻查询
- 懒惰更新

Splay Tree 是一种自调整的二叉搜索树，具有以下特点：
- 最近访问的元素会被移到根节点（伸展操作）
- 均摊时间复杂度为 O(log n)
- 无需存储额外平衡信息
- 对具有访问局部性的场景性能优异

零外部依赖，纯 Python 标准库实现。

Author: AllToolkit
License: MIT


## 功能

### 类

- **SplayTreeNode**: Splay Tree 节点类

Attributes:
    key: 节点键值
    left: 左子节点
    right: 右子节点
    parent: 父节点
    size: 子树大小
    value: 可选的关联值
    lazy_flip: 懒惰反转标记
- **SplayTree**: Splay Tree (伸展树) 实现

一种自调整的二叉搜索树，通过伸展操作将最近访问的节点移到根。

均摊时间复杂度：
- 插入：O(log n)
- 删除：O(log n)
- 查找：O(log n)
- 范围查询：O(log n + k)

空间复杂度：O(n)

示例:
    >>> tree = SplayTree[int]()
    >>> tree
  方法: root, size, is_empty, insert, search ... (22 个方法)
- **IndexedSplayTree**: 索引伸展树

支持按位置插入、删除、访问的伸展树变体。
适用于序列操作场景。

时间复杂度（均摊）：
- 插入：O(log n)
- 删除：O(log n)
- 访问：O(log n)
- 区间操作：O(log n)

示例:
    >>> seq = IndexedSplayTree[int]()
    >>> seq
  方法: size, is_empty, append

### 函数

- **create_splay_tree(items, key_func**) - 从列表创建伸展树
- **merge_splay_trees(tree1, tree2**) - 合并两棵伸展树
- **root(self**) - 返回根节点
- **size(self**) - 返回树的大小
- **is_empty(self**) - 检查树是否为空
- **insert(self, key, value**) - 插入键值
- **search(self, key**) - 查找键是否存在
- **get(self, key**) - 获取键关联的值
- **delete(self, key**) - 删除键
- **min(self**) - 获取最小键

... 共 31 个函数

## 使用示例

```python
from mod import create_splay_tree

# 使用 create_splay_tree
result = create_splay_tree()
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
