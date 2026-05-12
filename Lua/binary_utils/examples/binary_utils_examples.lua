#!/usr/bin/env lua
---
-- Binary Utilities Examples
-- 二进制工具函数使用示例
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local mod_path = path .. "../mod.lua"

-- 加载模块
local BinaryUtils = dofile(mod_path)

print("=" .. string.rep("=", 50))
print("Binary Utilities Examples")
print("=" .. string.rep("=", 50))

-------------------------------------------------------------------------------
-- 示例1：进制转换
-------------------------------------------------------------------------------
print("\n📋 示例1：进制转换")
print("-" .. string.rep("-", 50))

-- 二进制转十进制
local binary = "10101010"
local decimal = BinaryUtils.binary_to_decimal(binary)
print(string.format("二进制 %s -> 十进制 %d", binary, decimal))

-- 十进制转二进制
decimal = 42
binary = BinaryUtils.decimal_to_binary(decimal)
print(string.format("十进制 %d -> 二进制 %s", decimal, binary))

-- 指定位数
binary = BinaryUtils.decimal_to_binary(5, 8)
print(string.format("十进制 5 (8位) -> 二进制 %s", binary))

-- 二进制转十六进制
binary = "11111111"
local hex = BinaryUtils.binary_to_hex(binary)
print(string.format("二进制 %s -> 十六进制 %s", binary, hex))

-- 十六进制转二进制
hex = "FF"
binary = BinaryUtils.hex_to_binary(hex)
print(string.format("十六进制 %s -> 二进制 %s", hex, binary))

-- 二进制转八进制
binary = "11111111"
local octal = BinaryUtils.binary_to_octal(binary)
print(string.format("二进制 %s -> 八进制 %s", binary, octal))

-------------------------------------------------------------------------------
-- 示例2：位运算
-------------------------------------------------------------------------------
print("\n📋 示例2：位运算")
print("-" .. string.rep("-", 50))

local a = "1010"
local b = "1100"

print(string.format("A = %s, B = %s", a, b))
print(string.format("A AND B = %s", BinaryUtils.binary_and(a, b)))
print(string.format("A OR B = %s", BinaryUtils.binary_or(a, b)))
print(string.format("A XOR B = %s", BinaryUtils.binary_xor(a, b)))
print(string.format("NOT A = %s", BinaryUtils.binary_not(a)))

-- 移位操作
local val = "1010"
print(string.format("%s 左移2位 = %s", val, BinaryUtils.left_shift(val, 2)))
print(string.format("%s 右移2位 = %s", val, BinaryUtils.right_shift(val, 2)))

-- 循环移位
print(string.format("%s 循环左移1位 = %s", val, BinaryUtils.rotate_left(val, 1)))
print(string.format("%s 循环右移1位 = %s", val, BinaryUtils.rotate_right(val, 1)))

-------------------------------------------------------------------------------
-- 示例3：算术运算
-------------------------------------------------------------------------------
print("\n📋 示例3：算术运算")
print("-" .. string.rep("-", 50))

local x = "1111"  -- 15
local y = "1"     -- 1

print(string.format("X = %s (%d), Y = %s (%d)", x, BinaryUtils.binary_to_decimal(x), y, BinaryUtils.binary_to_decimal(y)))
print(string.format("X + Y = %s (%d)", BinaryUtils.binary_add(x, y), BinaryUtils.binary_to_decimal(BinaryUtils.binary_add(x, y))))

x = "100"  -- 4
y = "10"   -- 2
print(string.format("X = %s (%d), Y = %s (%d)", x, BinaryUtils.binary_to_decimal(x), y, BinaryUtils.binary_to_decimal(y)))
print(string.format("X - Y = %s (%d)", BinaryUtils.binary_sub(x, y), BinaryUtils.binary_to_decimal(BinaryUtils.binary_sub(x, y))))
print(string.format("X * Y = %s (%d)", BinaryUtils.binary_mul(x, y), BinaryUtils.binary_to_decimal(BinaryUtils.binary_mul(x, y))))
print(string.format("X / Y = %s (%d)", BinaryUtils.binary_div(x, y), BinaryUtils.binary_to_decimal(BinaryUtils.binary_div(x, y))))

-------------------------------------------------------------------------------
-- 示例4：统计计算
-------------------------------------------------------------------------------
print("\n📋 示例4：统计计算")
print("-" .. string.rep("-", 50))

binary = "10101010"
print(string.format("二进制: %s", binary))
print(string.format("1的个数: %d", BinaryUtils.count_bits(binary)))
print(string.format("0的个数: %d", BinaryUtils.count_zeros(binary)))
print(string.format("汉明权重: %d", BinaryUtils.hamming_weight(binary)))

-- 汉明距离
local str1 = "10101010"
local str2 = "11001100"
print(string.format("汉明距离(%s, %s) = %d", str1, str2, BinaryUtils.hamming_distance(str1, str2)))

-------------------------------------------------------------------------------
-- 示例5：字符串操作
-------------------------------------------------------------------------------
print("\n📋 示例5：字符串操作")
print("-" .. string.rep("-", 50))

binary = "00001010"
print(string.format("原始: %s", binary))
print(string.format("去除前导零: %s", BinaryUtils.strip_leading_zeros(binary)))
print(string.format("补齐到8位: %s", BinaryUtils.pad_binary("101", 8)))
print(string.format("反转: %s", BinaryUtils.reverse_binary(binary)))

-- 位操作
binary = "0000"
print(string.format("设置第1位: %s", BinaryUtils.set_bit(binary, 1, 1)))
print(string.format("设置第4位: %s", BinaryUtils.set_bit(binary, 4, 1)))
print(string.format("清除第1位(1111): %s", BinaryUtils.clear_bit("1111", 1)))

-------------------------------------------------------------------------------
-- 示例6：特殊功能
-------------------------------------------------------------------------------
print("\n📋 示例6：特殊功能")
print("-" .. string.rep("-", 50))

-- 奇偶性检查
binary = "10"
print(string.format("%s 是偶数: %s", binary, tostring(BinaryUtils.is_even(binary))))
binary = "11"
print(string.format("%s 是奇数: %s", binary, tostring(BinaryUtils.is_odd(binary))))

-- 二的幂次检查
print(string.format("1 是二的幂次: %s", tostring(BinaryUtils.is_power_of_two("1"))))
print(string.format("10 是二的幂次: %s", tostring(BinaryUtils.is_power_of_two("10"))))
print(string.format("11 是二的幂次: %s", tostring(BinaryUtils.is_power_of_two("11"))))

-- 格式化字节
binary = "1010101010101010"
print(string.format("格式化字节: %s", BinaryUtils.format_as_bytes(binary)))

-------------------------------------------------------------------------------
-- 示例7：字节操作与编码
-------------------------------------------------------------------------------
print("\n📋 示例7：字节操作与编码")
print("-" .. string.rep("-", 50))

-- 字节数组
binary = "1111111100000000"
local bytes = BinaryUtils.to_byte_array(binary)
print(string.format("二进制 %s -> 字节数组 [255, 0]", binary))

-- 从字节数组恢复
binary = BinaryUtils.from_byte_array({255, 0})
print(string.format("字节数组 [255, 0] -> 二进制 %s", binary))

-- ASCII编码
local char = "A"
binary = BinaryUtils.char_to_binary(char)
print(string.format("字符 '%s' -> 二进制 %s", char, binary))
char = BinaryUtils.binary_to_char(binary)
print(string.format("二进制 %s -> 字符 '%s'", binary, char))

-- 字符串编码
local text = "Hello"
binary = BinaryUtils.string_to_binary(text)
print(string.format("字符串 '%s' -> 二进制 (%d bits)", text, #binary))
text = BinaryUtils.binary_to_string(binary)
print(string.format("二进制 -> 字符串 '%s'", text))

-------------------------------------------------------------------------------
-- 示例8：补码与负数
-------------------------------------------------------------------------------
print("\n📋 示例8：补码与负数")
print("-" .. string.rep("-", 50))

-- 正数转补码形式
binary = BinaryUtils.decimal_to_binary_signed(5, 8)
print(string.format("十进制 5 (8位补码) -> 二进制 %s", binary))

-- 负数转补码形式
binary = BinaryUtils.decimal_to_binary_signed(-5, 8)
print(string.format("十进制 -5 (8位补码) -> 二进制 %s", binary))
decimal = BinaryUtils.twos_complement_to_decimal(binary, 8)
print(string.format("补码 %s -> 十进制 %d", binary, decimal))

-------------------------------------------------------------------------------
-- 示例9：模式匹配
-------------------------------------------------------------------------------
print("\n📋 示例9：模式匹配")
print("-" .. string.rep("-", 50))

binary = "10101010"
print(string.format("二进制: %s", binary))
print(string.format("第一个1的位置: %d", BinaryUtils.find_first_one(binary)))
print(string.format("最后一个1的位置: %d", BinaryUtils.find_last_one(binary)))
print(string.format("第一个0的位置: %d", BinaryUtils.find_first_zero(binary)))

-- 查找模式
local pattern = "101"
local pos = BinaryUtils.find_pattern(binary, pattern)
print(string.format("查找模式 '%s': 位置 %d", pattern, pos))

-- 查找所有匹配
local positions = BinaryUtils.find_all_patterns(binary, "10")
print(string.format("查找所有 '10': %d 个匹配", #positions))

-------------------------------------------------------------------------------
-- 示例10：工厂对象模式
-------------------------------------------------------------------------------
print("\n📋 示例10：工厂对象模式")
print("-" .. string.rep("-", 50))

-- 创建对象
local obj = BinaryUtils.create(42)
print(string.format("创建对象(42): binary=%s, decimal=%d, hex=%s", 
    obj.binary, obj.to_decimal(), obj.to_hex()))

-- 链式操作
local a_obj = BinaryUtils.create("1010")
local b_obj = BinaryUtils.create("1100")
print(string.format("AND: %s", a_obj.and_(b_obj).binary))
print(string.format("OR: %s", a_obj.or_(b_obj).binary))
print(string.format("XOR: %s", a_obj.xor_(b_obj).binary))
print(string.format("NOT: %s", a_obj.not_().binary))

-------------------------------------------------------------------------------
-- 示例11：随机生成
-------------------------------------------------------------------------------
print("\n📋 示例11：随机生成")
print("-" .. string.rep("-", 50))

for i = 1, 5 do
    local random_bin = BinaryUtils.random_binary(8)
    print(string.format("随机8位: %s (十进制: %d)", random_bin, BinaryUtils.binary_to_decimal(random_bin)))
end

print("\n" .. string.rep("=", 50))
print("示例完成!")
print(string.rep("=", 50))