# Bit Utilities (位操作工具集)

全面的位操作工具集，提供完整的位运算、位掩码、位字段、位向量等功能。

## 功能特性

### 📦 核心类

- **BitVector** - 高效的动态位数组实现
- **BitField** - 位字段提取和插入操作
- **BitMask** - 位掩码创建和操作

### 🔧 位计数

- `count_bits()` - 计算汉明重量（1的个数）
- `count_zeros()` - 计算0的个数
- `parity()` - 奇偶校验计算

### 🔍 位查找

- `find_first_set_bit()` - 找第一个设置的位
- `find_last_set_bit()` - 找最后一个设置的位
- `find_nth_set_bit()` - 找第n个设置的位
- `most_significant_bit()` - 最高有效位位置
- `least_significant_bit()` - 最低有效位位置

### 🔄 位反转与旋转

- `reverse_bits()` - 反转所有位
- `reverse_bytes()` - 反转字节顺序（字节序转换）
- `rotate_left()` - 循环左移
- `rotate_right()` - 循环右移

### 🎯 位操作

- `is_power_of_two()` - 检查是否是2的幂
- `next_power_of_two()` - 获取下一个2的幂
- `previous_power_of_two()` - 获取上一个2的幂
- `gray_code()` - 二进制转格雷码
- `gray_to_binary()` - 格雷码转二进制
- `sign_extend()` - 符号扩展
- `swap_bits()` - 交换两个位
- `align_up()` - 向上对齐
- `align_down()` - 向下对齐

### 📝 格式化

- `to_binary_string()` - 二进制字符串格式化
- `from_binary_string()` - 从二进制字符串解析
- `to_hex_string()` - 十六进制字符串格式化

### 🧮 位集合

- `create_bitset()` - 创建位集合
- `bitset_union()` - 并集
- `bitset_intersection()` - 交集
- `bitset_difference()` - 差集
- `bitset_symmetric_difference()` - 对称差
- `bitset_is_subset()` - 子集检查
- `bitset_is_superset()` - 超集检查
- `bitset_to_list()` - 转换为列表

## 安装

零外部依赖，纯 Python 实现：

```python
from bit_utils.mod import *
```

## 快速开始

### BitVector 示例

```python
from bit_utils.mod import BitVector

# 创建8位向量
bv = BitVector(8, 0b10110101)

# 位操作
bv.set(0)      # 设置第0位为1
bv.clear(2)    # 清除第2位
bv.flip(4)     # 翻转第4位

# 统计
print(bv.count_set_bits())  # 输出: 5

# 转换
print(bv.to_binary_string())  # 输出: 10110101
```

### BitField 示例

```python
from bit_utils.mod import BitField

# 提取位字段
value = 0b10110100
field = BitField.extract(value, 2, 5)  # 提取位2-4
print(field)  # 输出: 6 (0b110)

# 插入位字段
new_value = BitField.insert(value, 2, 5, 0b111)
print(new_value)  # 输出: 188 (0b10111100)
```

### 位掩码示例

```python
from bit_utils.mod import BitMask, to_binary_string

# 创建权限掩码
read_mask = BitMask.create_mask([0])
write_mask = BitMask.create_mask([1])
admin_mask = BitMask.combine_masks(read_mask, write_mask)

print(to_binary_string(admin_mask, width=5))  # 输出: 00011
```

### 格雷码示例

```python
from bit_utils.mod import gray_code, gray_to_binary

# 二进制转格雷码
gray = gray_code(5)
print(gray)  # 输出: 7 (0b111)

# 格雷码转二进制
binary = gray_to_binary(7)
print(binary)  # 输出: 5
```

## 运行测试

```bash
cd Python/bit_utils
python bit_utils_test.py
```

## 运行示例

```bash
cd Python/bit_utils/examples
python usage_examples.py
```

## 应用场景

1. **网络协议解析** - 提取和设置数据包字段
2. **权限系统** - 使用位掩码表示权限
3. **数据压缩** - 位级数据存储
4. **加密算法** - 位运算实现
5. **游戏开发** - 状态标记和碰撞检测
6. **嵌入式系统** - 寄存器操作

## 特点

- ✅ 零外部依赖
- ✅ 纯 Python 实现
- ✅ 完整的测试覆盖
- ✅ 详细的文档和示例
- ✅ 支持大整数操作

## 作者

AllToolkit 自动化开发

## 版本

1.0.0 (2026-04-16)