# Quadtree Utils


四叉树工具模块 (Quadtree Utilities)

四叉树是一种树数据结构，用于高效地分割二维空间。
每个内部节点恰好有四个子节点，常用于空间索引、图像压缩、碰撞检测等场景。

核心功能:
- 点插入与删除
- 范围查询 (矩形区域内的所有点)
- 最近邻查询 (KNN)
- 半径查询 (圆形区域内的所有点)
- 边界矩形查询
- 自动分裂与合并
- 支持自定义数据

时间复杂度:
- 插入: O(log n) 平均情况
- 删除: O(log n) 平均情况
- 范围查询: O(log n + k)，k为结果数量
- 最近邻: O(log n) 平均情况

零外部依赖，纯 Python 实现。


## 功能

### 类

- **Point**: 二维点，可携带任意数据
- **Rectangle**: 轴对齐边界矩形 (Axis-Aligned Bounding Box)

Attributes:
    x: 左边界 x 坐标
    y: 上边界 y 坐标
    width: 宽度
    height: 高度
  方法: left, right, top, bottom, center ... (9 个方法)
- **Circle**: 圆形区域
  方法: contains_point, intersects_rect
- **QuadTreeNode**: 四叉树节点
  方法: is_leaf, is_empty, insert, remove, query ... (10 个方法)
- **QuadTree**: 四叉树 - 二维空间索引数据结构

四叉树递归地将二维空间划分为四个象限，适合存储和查询空间点数据。

Example:
    >>> tree = QuadTree(Rectangle(0, 0, 100, 100))
    >>> tree
  方法: boundary, capacity, max_depth, insert, insert_many ... (14 个方法)

### 函数

- **create_quadtree(x, y, width**, ...) - 创建四叉树的便捷函数
- **from_points(points, capacity, max_depth**, ...) - 从点列表创建四叉树
- **left(self**) - 左边界
- **right(self**) - 右边界
- **top(self**) - 上边界
- **bottom(self**) - 下边界
- **center(self**) - 中心点坐标
- **area(self**) - 面积
- **contains_point(self, point**) - 检查点是否在矩形内
- **intersects(self, other**) - 检查两个矩形是否相交

... 共 38 个函数

## 使用示例

```python
from mod import create_quadtree

# 使用 create_quadtree
result = create_quadtree()
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
