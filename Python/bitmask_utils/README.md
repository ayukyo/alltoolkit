# Bitmask Utils - 位掩码操作工具 🔢

提供位掩码创建、操作、查询等功能。适用于权限系统、标志管理、状态机、位操作等场景。零外部依赖，纯 Python 标准库实现。

## 功能特性

- ✅ 基本操作 - 设置、清除、切换、检查位
- ✅ 多位操作 - 批量设置、清除、切换
- ✅ 范围操作 - 设置/清除位范围
- ✅ 查询操作 - 计数、查找、获取位列表
- ✅ 操控操作 - 反转、移位、旋转
- ✅ 逻辑操作 - AND、OR、XOR
- ✅ 比较操作 - 子集、超集、重叠、不相交
- ✅ 转换操作 - 整数、二进制、十六进制、列表、集合
- ✅ 工具函数 - 位计数、奇偶校验、Gray码、幂判断
- ✅ 魔法方法 - 支持Python运算符语法

## 快速开始

### 基本用法

```python
from bitmask_utils import Bitmask

# 创建8位掩码
mask = Bitmask(bits=8)

# 设置位（链式调用）
mask.set(0).set(2).set(4)

# 检查位
mask.has(0)  # True
mask.has(1)  # False

# 清除位
mask.clear(0)

# 切换位
mask.toggle(1)

# 获取值
mask.to_int()  # 整数
mask.to_bin()  # "0b0010101"
mask.to_hex()  # "0x15"
```

### 运算符语法

```python
mask = Bitmask(value=0b1010, bits=8)
other = Bitmask(value=0b1100, bits=8)

# 位运算
result = mask & other  # AND
result = mask | other  # OR
result = mask ^ other  # XOR
result = ~mask         # 反转

# 移位
result = mask << 2     # 左移
result = mask >> 2     # 右移

# 包含检查
if 1 in mask:
    print("位1已设置")

# 紧引访问
mask[0] = 1  # 设置位0
value = mask[1]  # 获取位1的值
```

### 多位操作

```python
mask = Bitmask(bits=8)

# 设置多个位
mask.set_all([0, 1, 2, 3])

# 检查是否全部设置
mask.has_all([0, 1])  # True

# 检查是否有任意一个设置
mask.has_any([4, 5])  # False

# 检查是否全部未设置
mask.has_none([4, 5])  # True

# 清除多个位
mask.clear_all([0, 1])

# 切换多个位
mask.toggle_all([2, 4])
```

### 范围操作

```python
mask = Bitmask(bits=8)

# 设置范围（位0到3）
mask.set_range(0, 3)  # 0b1111

# 清除范围
mask.clear_range(1, 2)
```

### 查询操作

```python
mask = Bitmask(value=0b10101010, bits=8)

# 统计
mask.count_set()    # 4（设置了4个位）
mask.count_clear()  # 4

# 查找
mask.first_set()    # 1（最低设置位）
mask.last_set()     # 7（最高设置位）

# 获取位列表
mask.get_set_bits()    # [1, 3, 5, 7]
mask.get_clear_bits()  # [0, 2, 4, 6]
```

### 旋转和移位

```python
mask = Bitmask(value=0b11000000, bits=8)

# 循环左移
mask.rotate_left(2)  # 0b00000011

# 循环右移
mask.rotate_right(2)  # 0b00000011

# 普通移位（非循环）
mask.shift_left(2)   # 左移，高位丢弃
mask.shift_right(2)  # 右移，低位丢弃
```

### 比较操作

```python
mask1 = Bitmask(value=0b1100, bits=8)
mask2 = Bitmask(value=0b1111, bits=8)
mask3 = Bitmask(value=0b0011, bits=8)

# 子集检查（mask1的所有位都在mask2中）
mask1.is_subset(mask2)  # True

# 超集检查（mask2包含mask1的所有位）
mask2.is_superset(mask1)  # True

# 重叠检查
mask1.overlaps(mask3)  # True（位2重叠）

# 不相交检查
mask_a = Bitmask(value=0b00001111, bits=8)
mask_b = Bitmask(value=0b11110000, bits=8)
mask_a.is_disjoint(mask_b)  # True
```

## 函数式 API

### 创建掩码

```python
from bitmask_utils import create_bitmask, from_bits, from_binary, from_hex

# 从整数创建
mask = create_bitmask(5, bits=8)

# 从位列表创建
mask = from_bits([0, 2, 4], total_bits=8)

# 从二进制字符串创建
mask = from_binary("10101010")
mask = from_binary("0b1100")

# 从十六进制字符串创建
mask = from_hex("ff")
mask = from_hex("0xaa")
```

### 组合掩码

```python
from bitmask_utils import combine_bitmasks, intersect_bitmasks

m1 = Bitmask(value=0b1100, bits=8)
m2 = Bitmask(value=0b0011, bits=8)

# 组合（OR）
combined = combine_bitmasks(m1, m2)  # 0b1111

# 交集（AND）
intersected = intersect_bitmasks(m1, m2)  # 0b0000
```

## 工具函数

```python
from bitmask_utils import (
    count_bits, parity, reverse_bits,
    next_power_of_2, is_power_of_2,
    get_lsb, get_msb, gray_code, from_gray_code
)

# 统计位数
count_bits(255)  # 8

# 奇偶校验
parity(7)  # 1

# 反转位
reverse_bits(0b11010010, 8)  # 0b01001011

# 下一幂
next_power_of_2(10)  # 16

# 判断幂
is_power_of_2(8)  # True

# LSB/MSB
get_lsb(8)   # 3
get_msb(255, bits=8)  # 7

# Gray码
gray_code(5)       # 7
from_gray_code(7)  # 5
```

## 权限系统示例

```python
# 定义权限位
READ = 0
WRITE = 1
DELETE = 2
ADMIN = 3

# 创建权限掩码
permissions = Bitmask(bits=4)
permissions.set(READ).set(WRITE)

# 检查权限
if permissions.has(READ):
    print("可读")

if permissions.has_all([READ, WRITE]):
    print("可读可写")

# 添加权限
permissions.set(DELETE)

# 移除权限
permissions.clear(WRITE)

# 检查是否有管理员权限
if permissions.has(ADMIN):
    print("是管理员")
```

## API 参考

### Bitmask 类

| 方法 | 说明 |
|------|------|
| `set(bit)` | 设置位 |
| `clear(bit)` | 清除位 |
| `toggle(bit)` | 切换位 |
| `has(bit)` | 检查位 |
| `get(bit)` | 获取位值（0或1） |
| `set_all(bits)` | 设置多个位 |
| `clear_all(bits)` | 清除多个位 |
| `toggle_all(bits)` | 切换多个位 |
| `has_all(bits)` | 检查所有位是否设置 |
| `has_any(bits)` | 检查任意位是否设置 |
| `has_none(bits)` | 检查所有位是否未设置 |
| `set_range(start, end)` | 设置位范围 |
| `clear_range(start, end)` | 清除位范围 |
| `count_set()` | 统计设置位数 |
| `count_clear()` | 统计清除位数 |
| `first_set()` | 第一个设置位位置 |
| `last_set()` | 最后一个设置位位置 |
| `get_set_bits()` | 获取设置位列表 |
| `get_clear_bits()` | 获取清除位列表 |
| `invert()` | 反转所有位 |
| `shift_left(n)` | 左移 |
| `shift_right(n)` | 右移 |
| `rotate_left(n)` | 循环左移 |
| `rotate_right(n)` | 循环右移 |
| `and_with(other)` | AND 操作 |
| `or_with(other)` | OR 操作 |
| `xor_with(other)` | XOR 操作 |
| `is_subset(other)` | 子集检查 |
| `is_superset(other)` | 超集检查 |
| `overlaps(other)` | 重叠检查 |
| `is_disjoint(other)` | 不相交检查 |
| `to_int()` | 转整数 |
| `to_bin()` | 转二进制字符串 |
| `to_hex()` | 十六进制字符串 |
| `to_list()` | 转列表（LSB在前） |
| `to_set()` | 转集合（设置位索引） |
| `copy()` | 复制 |
| `reset()` | 重置为0 |
| `fill()` | 填充为全1 |

## 测试

```bash
python Python/bitmask_utils/bitmask_utils_test.py
```

**测试覆盖**: 16+ 测试用例，100% 通过率 ✅

---

**最后更新**: 2026-05-14