# rotation_utils - 旋转操作工具集

提供各种旋转操作的实现，零外部依赖。

## 功能特性

- **数组旋转** - 左旋、右旋，多种高效算法
- **位旋转** - 循环移位操作
- **矩阵旋转** - 90°、180°、270° 旋转
- **字符串旋转** - 字符串循环移位
- **旋转检测** - 判断两个序列是否为旋转关系

## 算法实现

### 数组旋转算法
- **Simple** - 简单切片实现
- **Reversal** - 反转算法（原地操作）
- **Juggling** - 杂耍算法
- **Block Swap** - 分块交换算法

## 主要函数

### rotate_left_simple(arr, k)
左旋数组（简单实现），返回新数组。

```python
rotate_left_simple([1, 2, 3, 4, 5], 2)  # [3, 4, 5, 1, 2]
```

### rotate_right_simple(arr, k)
右旋数组（简单实现），返回新数组。

```python
rotate_right_simple([1, 2, 3, 4, 5], 2)  # [4, 5, 1, 2, 3]
```

### rotate_left_inplace(arr, k)
原地左旋数组（Reversal 算法），不返回新数组。

### rotate_right_inplace(arr, k)
原地右旋数组。

### rotate_bits(value, k, bits=32)
位旋转（循环移位）。

```python
rotate_bits(0b10110011, 3, 8)  # 位循环左移3位
```

### rotate_matrix_90(matrix)
矩阵顺时针旋转90°。

```python
rotate_matrix_90([[1, 2], [3, 4]])  # [[3, 1], [4, 2]]
```

### rotate_matrix_180(matrix)
矩阵旋转180°。

### rotate_matrix_270(matrix)
矩阵逆时针旋转90°。

### rotate_string(s, k)
字符串旋转。

```python
rotate_string("hello", 2)  # "llohe"
```

### is_rotation(a, b)
判断两个序列是否为旋转关系。

```python
is_rotation([1, 2, 3], [2, 3, 1])  # True
is_rotation("abc", "bca")  # True
```

## 使用示例

```python
from rotation_utils import rotate_left_simple, rotate_matrix_90, is_rotation

# 数组旋转
arr = [1, 2, 3, 4, 5]
rotated = rotate_left_simple(arr, 3)
print(rotated)  # [4, 5, 1, 2, 3]

# 矩阵旋转
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotated = rotate_matrix_90(matrix)
print(rotated)  # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

# 旋转检测
print(is_rotation("waterbottle", "erbottlewat"))  # True
```

## 测试

运行测试：
```bash
python rotation_utils/rotation_utils_test.py
```

测试覆盖率：43 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*