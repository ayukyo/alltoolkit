# Red Black Tree Utils


Red-Black Tree Utils - 红黑树工具模块

红黑树是一种自平衡二叉搜索树，具有以下性质：
1. 每个节点要么是红色，要么是黑色
2. 根节点是黑色
3. 所有叶子节点（NIL）是黑色
4. 红色节点的子节点必须是黑色（不能有连续红色节点）
5. 从任一节点到其每个叶子的所有简单路径都包含相同数目的黑色节点

时间复杂度：
- 查找：O(log n)
- 插入：O(log n)
- 删除：O(log n)

应用场景：
- 关联数组（C++ STL map/set）
- 进程调度
- 内存管理
- 文件系统


## 功能

### 类

- **Color**: 红黑树节点颜色
- **Node**: 红黑树节点
  方法: is_red, is_black
- **RedBlackTree**: 红黑树实现

特点：
- 自动平衡，保证树的高度不超过 2*log2(n+1)
- 支持高效的查找、插入、删除操作
- 支持范围查询和有序遍历
  方法: size, is_empty, contains, search, insert ... (20 个方法)
- **RedBlackTreeSet**: 基于红黑树的集合实现

支持高效的插入、删除、查找和范围查询
  方法: add, remove, contains, minimum, maximum ... (9 个方法)
- **RedBlackTreeMap**: 基于红黑树的有序映射实现

支持高效的键值存储和范围查询
  方法: is_empty, put, get, remove, keys ... (13 个方法)

### 函数

- **create_tree(items**) - 从键值对列表创建红黑树
- **create_set(items**) - 从元素列表创建红黑树集合
- **create_map(items**) - 从字典创建红黑树映射
- **is_red(self**) - 检查节点是否为红色
- **is_black(self**) - 检查节点是否为黑色
- **size(self**) - 返回树中节点数量
- **is_empty(self**) - 检查树是否为空
- **contains(self, key**) - 检查键是否存在
- **search(self, key**) - 查找键对应的值
- **insert(self, key, value**) - 插入键值对

... 共 47 个函数

## 使用示例

```python
from mod import create_tree

# 使用 create_tree
result = create_tree()
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
