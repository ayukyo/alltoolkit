# Treap Utils


Treap (树堆) 工具模块

Treap 是一种随机化平衡二叉搜索树，结合了二叉搜索树和堆的特性。
- 二叉搜索树性质：左子树所有节点值 < 当前节点值 < 右子树所有节点值
- 堆性质：每个节点的优先级 >= 其子节点的优先级

通过随机优先级，Treap 在期望情况下保持 O(log n) 的高度，
实现高效的插入、删除、查找等操作。

零外部依赖，纯 Python 实现。


## 功能

### 类

- **TreapNode**: Treap 节点类
  方法: update_size
- **Treap**: Treap（树堆）数据结构

特性：
- 支持重复元素
- O(log n) 期望时间复杂度的插入、删除、查找
- 支持范围查询、第 k 小元素查询
- 支持前驱后继查询
  方法: insert, delete, search, contains, is_empty ... (18 个方法)
- **ImplicitTreap**: 隐式 Treap（按位置索引）

支持在任意位置插入/删除元素，维护序列。
用于实现高效序列操作。
  方法: insert_at, delete_at, get_at, set_at, reverse_range ... (6 个方法)
- **ImplicitTreapNode**: 隐式 Treap 节点

### 函数

- **create_treap(keys, key_func**) - 创建 Treap 的便捷函数
- **create_implicit_treap(values**) - 创建隐式 Treap 的便捷函数
- **update_size(self**) - 更新子树大小
- **insert(self, key, priority**) - 插入键值
- **delete(self, key**) - 删除键值
- **search(self, key**) - 查找键值的数量
- **contains(self, key**) - 检查是否包含键值
- **is_empty(self**) - 检查是否为空
- **get_min(self**) - 获取最小键值
- **get_max(self**) - 获取最大键值

... 共 27 个函数

## 使用示例

```python
from mod import create_treap

# 使用 create_treap
result = create_treap()
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
