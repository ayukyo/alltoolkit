# Binary Utilities Module

二进制数据处理工具函数库，提供常用的二进制数据处理功能。

## 概述

Binary Utils 是一个零依赖的 Lua 模块，提供全面的二进制数据处理功能，包括：

- 进制转换（二进制、十进制、十六进制、八进制）
- 位运算（AND、OR、XOR、NOT、移位、循环移位）
- 二进制算术运算
- 字符串操作与格式化
- 统计计算（位计数、汉明距离等）
- 模式匹配与查找
- 字节操作与编码转换

## 安装

将 `mod.lua` 复制到你的项目目录即可使用。

## 使用方法

```lua
local BinaryUtils = dofile("mod.lua")

-- 进制转换
local decimal = BinaryUtils.binary_to_decimal("1010")  -- 返回 10
local binary = BinaryUtils.decimal_to_binary(10)        -- 返回 "1010"
local hex = BinaryUtils.binary_to_hex("11111111")       -- 返回 "FF"
local octal = BinaryUtils.binary_to_octal("11111111")   -- 返回 "377"

-- 位运算
local result = BinaryUtils.binary_and("1010", "1100")   -- 返回 "1000"
local result = BinaryUtils.binary_or("1010", "1100")    -- 返回 "1110"
local result = BinaryUtils.binary_xor("1010", "1100")   -- 返回 "0110"
local result = BinaryUtils.binary_not("1010")           -- 返回 "0101"

-- 移位操作
local result = BinaryUtils.left_shift("1010", 2)        -- 返回 "101000"
local result = BinaryUtils.right_shift("1010", 2)       -- 返回 "10"

-- 算术运算
local sum = BinaryUtils.binary_add("1010", "1010")      -- 返回 "10100"
local diff = BinaryUtils.binary_sub("100", "10")        -- 返回 "10"
local product = BinaryUtils.binary_mul("10", "10")      -- 返回 "100"

-- 统计
local count = BinaryUtils.count_bits("1010")            -- 返回 2
local distance = BinaryUtils.hamming_distance("1010", "1111")  -- 返回 2

-- 字节操作
local bytes = BinaryUtils.to_byte_array("1111111100000000")  -- 返回 {255, 0}
local text = BinaryUtils.binary_to_string("01000001")        -- 返回 "A"
```

## API 文档

### 验证函数

| 函数 | 描述 |
|------|------|
| `is_valid_binary(binary)` | 验证是否为有效二进制字符串 |
| `is_valid_hex(hex)` | 验证是否为有效十六进制字符串 |
| `is_valid_octal(octal)` | 验证是否为有效八进制字符串 |

### 进制转换

| 函数 | 描述 |
|------|------|
| `binary_to_decimal(binary)` | 二进制转十进制 |
| `decimal_to_binary(decimal, bits)` | 十进制转二进制 |
| `decimal_to_binary_signed(decimal, bits)` | 十进制转二进制（补码） |
| `binary_to_hex(binary)` | 二进制转十六进制 |
| `binary_to_octal(binary)` | 二进制转八进制 |
| `hex_to_binary(hex)` | 十六进制转二进制 |
| `octal_to_binary(octal)` | 八进制转二进制 |

### 字符串操作

| 函数 | 描述 |
|------|------|
| `strip_leading_zeros(binary)` | 去除前导零 |
| `pad_binary(binary, bits)` | 补齐位数 |
| `reverse_binary(binary)` | 反转二进制字符串 |
| `get_bit(binary, position)` | 获取指定位值 |
| `set_bit(binary, position, value)` | 设置指定位值 |
| `clear_bit(binary, position)` | 清除指定位 |

### 位运算

| 函数 | 描述 |
|------|------|
| `binary_and(binary1, binary2)` | 按位与 |
| `binary_or(binary1, binary2)` | 按位或 |
| `binary_xor(binary1, binary2)` | 按位异或 |
| `binary_not(binary)` | 按位非 |
| `left_shift(binary, shift)` | 左移 |
| `right_shift(binary, shift)` | 右移 |
| `rotate_left(binary, shift)` | 循环左移 |
| `rotate_right(binary, shift)` | 循环右移 |

### 算术运算

| 函数 | 描述 |
|------|------|
| `binary_add(binary1, binary2)` | 二进制加法 |
| `binary_sub(binary1, binary2)` | 二进制减法 |
| `binary_mul(binary1, binary2)` | 二进制乘法 |
| `binary_div(binary1, binary2)` | 二进制除法 |
| `binary_mod(binary1, binary2)` | 二进制取模 |

### 统计计算

| 函数 | 描述 |
|------|------|
| `count_bits(binary)` | 计算中1的个数 |
| `count_zeros(binary)` | 计算中0的个数 |
| `hamming_weight(binary)` | 汉明权重 |
| `hamming_distance(binary1, binary2)` | 汉明距离 |

### 特殊功能

| 函数 | 描述 |
|------|------|
| `is_even(binary)` | 检查是否为偶数 |
| `is_odd(binary)` | 检查是否为奇数 |
| `is_power_of_two(binary)` | 检查是否为二的幂次 |
| `bit_length(binary)` | 获取位数 |
| `format_as_bytes(binary)` | 格式化为字节组 |
| `random_binary(length)` | 生成随机二进制字符串 |

### 字节操作

| 函数 | 描述 |
|------|------|
| `to_byte_array(binary)` | 转字节数组 |
| `from_byte_array(bytes)` | 字节数组转二进制 |
| `char_to_binary(char)` | ASCII字符转二进制 |
| `binary_to_char(binary)` | 二进制转ASCII字符 |
| `string_to_binary(str)` | 字符串转二进制 |
| `binary_to_string(binary)` | 二进制转字符串 |

### 工厂函数

| 函数 | 描述 |
|------|------|
| `create(value, bits)` | 创建二进制对象 |

工厂创建的对象方法：
- `to_decimal()` - 转十进制
- `to_hex()` - 十六进制
- `to_octal()` - 转八进制
- `and_(other)` - AND运算
- `or_(other)` - OR运算
- `xor_(other)` - XOR运算
- `not_()` - NOT运算
- `shift_left(shift)` - 左移
- `shift_right(shift)` - 右移

## 错误处理

模块定义了以下错误类型：

- `InvalidBinary` - 无效的二进制字符串
- `InvalidNumber` - 无效的数字
- `InvalidFormat` - 无效的格式
- `Overflow` - 值溢出
- `DivideByZero` - 除零错误
- `InvalidBitPosition` - 无效的位位置

## 常量

| 常量 | 值 | 描述 |
|------|-----|------|
| `BITS_PER_BYTE` | 8 | 每字节位数 |
| `MAX_INT_8` | 255 | 8位无符号最大值 |
| `MAX_INT_16` | 65535 | 16位无符号最大值 |
| `MAX_INT_32` | 4294967295 | 32位无符号最大值 |

## 特性

- ✅ 零外部依赖
- ✅ 纯 Lua 实现
- ✅ 支持补码表示负数
- ✅ 支持位运算和算术运算
- ✅ 支持字符串编码转换
- ✅ 完整的错误处理
- ✅ 面向对象的工厂模式

## 许可证

MIT License

## 作者

AllToolkit