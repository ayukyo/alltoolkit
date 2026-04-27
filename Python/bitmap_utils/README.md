# Bitmap Utils


Bitmap Utils - 零依赖位图工具库

功能：
- 高效位操作（设置、清除、翻转、查询）
- 位图运算（AND, OR, XOR, NOT, 差集）
- 位图统计（计数、查找、范围操作）
- 序列化与反序列化
- 位图迭代器
- 内存高效的大规模位集操作

作者：AllToolkit 自动化生成
日期：2026-04-22


## 功能

### 类

- **Bitmap**: 高效位图实现，支持大规模位集操作。
使用字节数组存储，内存效率高。
  方法: set, clear, flip, set_range, flip_range ... (44 个方法)
- **SparseBitmap**: 稀疏位图实现

适用于稀疏数据（大部分位为0），使用字典存储，
内存效率更高。
  方法: set, clear, flip, count_set, iter_set_bits ... (8 个方法)

### 函数

- **create_bitmap(size, indices**) - 创建位图的便捷函数
- **bitmap_from_string(s**) - 从二进制字符串创建位图
- **bitmap_union(**) - 多个位图的并集
- **bitmap_intersection(**) - 多个位图的交集
- **bitmap_difference(**) - 多个位图的差集（第一个减去其余所有）
- **set(self, index**) - 设置指定位置的位为1
- **clear(self, index**) - 清除指定位置的位（设为0）
- **flip(self, index**) - 翻转指定位置的位
- **set_range(self, start, end**, ...) - 设置范围内的所有位
- **flip_range(self, start, end**) - 翻转范围内的所有位

... 共 57 个函数

## 使用示例

```python
from mod import create_bitmap

# 使用 create_bitmap
result = create_bitmap()
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
