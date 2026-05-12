---
-- Binary Utilities Module
-- 二进制数据处理工具函数库
--
-- 提供常用的二进制数据处理功能，包括转换、操作、验证、解析等。
-- 仅使用 Lua 标准库，零依赖。
--
-- Features:
-- - Binary to Decimal/Hex/Octal conversion
-- - Decimal/Hex/Octal to Binary conversion
-- - Binary arithmetic operations
-- - Binary bitwise operations (AND, OR, XOR, NOT, shifts)
-- - Binary string manipulation
-- - Binary pattern matching
-- - Binary validation and normalization
-- - Floating point binary representation
-- - Binary encoding/decoding utilities
--
-- @author AllToolkit
-- @version 1.0.0
-- @copyright MIT License

local BinaryUtils = {}
local BinaryUtilsMT = { __index = BinaryUtils }

--- 版本号
BinaryUtils.VERSION = "1.0.0"

--- 错误类型
BinaryUtils.Error = {
    InvalidBinary = "Invalid binary string",
    InvalidNumber = "Invalid number",
    InvalidFormat = "Invalid format",
    Overflow = "Value overflow",
    DivideByZero = "Division by zero",
    InvalidBitPosition = "Invalid bit position",
}

-------------------------------------------------------------------------------
-- 常量定义
-------------------------------------------------------------------------------

BinaryUtils.BITS_PER_BYTE = 8
BinaryUtils.MAX_INT_8 = 255
BinaryUtils.MAX_INT_16 = 65535
BinaryUtils.MAX_INT_32 = 4294967295
BinaryUtils.MIN_INT_8_SIGNED = -128
BinaryUtils.MAX_INT_8_SIGNED = 127
BinaryUtils.MIN_INT_16_SIGNED = -32768
BinaryUtils.MAX_INT_16_SIGNED = 32767

-------------------------------------------------------------------------------
-- 验证函数
-------------------------------------------------------------------------------

--- 验证二进制字符串是否有效
-- @param binary 二进制字符串
-- @return boolean 是否有效
function BinaryUtils.is_valid_binary(binary)
    if binary == nil or type(binary) ~= "string" then
        return false
    end
    return binary:match("^[01]+$") ~= nil
end

--- 验证十六进制字符串是否有效
-- @param hex 十六进制字符串
-- @return boolean 是否有效
function BinaryUtils.is_valid_hex(hex)
    if hex == nil or type(hex) ~= "string" then
        return false
    end
    return hex:match("^[0-9a-fA-F]+$") ~= nil
end

--- 验证八进制字符串是否有效
-- @param octal 八进制字符串
-- @return boolean 是否有效
function BinaryUtils.is_valid_octal(octal)
    if octal == nil or type(octal) ~= "string" then
        return false
    end
    return octal:match("^[0-7]+$") ~= nil
end

-------------------------------------------------------------------------------
-- 二进制转其他进制
-------------------------------------------------------------------------------

--- 二进制转十进制
-- @param binary 二进制字符串
-- @return number 十进制数值
function BinaryUtils.binary_to_decimal(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local result = 0
    local len = #binary
    
    for i = 1, len do
        local bit = tonumber(binary:sub(i, i))
        result = result * 2 + bit
    end
    
    return result
end

--- 二进制转十六进制
-- @param binary 二进制字符串
-- @return string 十六进制字符串
function BinaryUtils.binary_to_hex(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    -- 补齐到4位一组
    local padded = binary
    while #padded % 4 ~= 0 do
        padded = "0" .. padded
    end
    
    local hex_chars = "0123456789ABCDEF"
    local result = ""
    
    for i = 1, #padded, 4 do
        local chunk = padded:sub(i, i + 3)
        local value = BinaryUtils.binary_to_decimal(chunk)
        result = result .. hex_chars:sub(value + 1, value + 1)
    end
    
    return result
end

--- 二进制转八进制
-- @param binary 二进制字符串
-- @return string 八进制字符串
function BinaryUtils.binary_to_octal(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    -- 补齐到3位一组
    local padded = binary
    while #padded % 3 ~= 0 do
        padded = "0" .. padded
    end
    
    local result = ""
    
    for i = 1, #padded, 3 do
        local chunk = padded:sub(i, i + 2)
        local value = BinaryUtils.binary_to_decimal(chunk)
        result = result .. tostring(value)
    end
    
    return result
end

-------------------------------------------------------------------------------
-- 其他进制转二进制
-------------------------------------------------------------------------------

--- 十进制转二进制
-- @param decimal 十进制数值
-- @param bits 可选，输出位数
-- @return string 二进制字符串
function BinaryUtils.decimal_to_binary(decimal, bits)
    if decimal == nil or type(decimal) ~= "number" then
        error(BinaryUtils.Error.InvalidNumber)
    end
    
    if decimal < 0 then
        return BinaryUtils.decimal_to_binary_signed(decimal, bits)
    end
    
    if decimal == 0 then
        if bits then
            return string.rep("0", bits)
        end
        return "0"
    end
    
    local result = ""
    local value = decimal
    
    while value > 0 do
        local remainder = value % 2
        result = tostring(remainder) .. result
        value = math.floor(value / 2)
    end
    
    -- 补齐位数
    if bits and #result < bits then
        result = string.rep("0", bits - #result) .. result
    end
    
    return result
end

--- 十进制转二进制（带符号）
-- @param decimal 十进制数值（可以是负数）
-- @param bits 位数（8, 16, 32）
-- @return string 二进制字符串（补码表示）
function BinaryUtils.decimal_to_binary_signed(decimal, bits)
    bits = bits or 8
    
    if bits ~= 8 and bits ~= 16 and bits ~= 32 then
        bits = 8
    end
    
    if decimal >= 0 then
        return BinaryUtils.decimal_to_binary(decimal, bits)
    end
    
    -- 计算补码
    local max_val = 2 ^ bits
    local unsigned = max_val + decimal
    
    return BinaryUtils.decimal_to_binary(unsigned, bits)
end

--- 十六进制转二进制
-- @param hex 十六进制字符串
-- @return string 二进制字符串
function BinaryUtils.hex_to_binary(hex)
    if not BinaryUtils.is_valid_hex(hex) then
        error(BinaryUtils.Error.InvalidFormat)
    end
    
    local hex_to_bin_map = {
        ["0"] = "0000", ["1"] = "0001", ["2"] = "0010", ["3"] = "0011",
        ["4"] = "0100", ["5"] = "0101", ["6"] = "0110", ["7"] = "0111",
        ["8"] = "1000", ["9"] = "1001", ["A"] = "1010", ["a"] = "1010",
        ["B"] = "1011", ["b"] = "1011", ["C"] = "1100", ["c"] = "1100",
        ["D"] = "1101", ["d"] = "1101", ["E"] = "1110", ["e"] = "1110",
        ["F"] = "1111", ["f"] = "1111",
    }
    
    local result = ""
    for i = 1, #hex do
        local char = hex:sub(i, i)
        result = result .. hex_to_bin_map[char]
    end
    
    return result
end

--- 八进制转二进制
-- @param octal 八进制字符串
-- @return string 二进制字符串
function BinaryUtils.octal_to_binary(octal)
    if not BinaryUtils.is_valid_octal(octal) then
        error(BinaryUtils.Error.InvalidFormat)
    end
    
    local oct_to_bin_map = {
        ["0"] = "000", ["1"] = "001", ["2"] = "010", ["3"] = "011",
        ["4"] = "100", ["5"] = "101", ["6"] = "110", ["7"] = "111",
    }
    
    local result = ""
    for i = 1, #octal do
        local char = octal:sub(i, i)
        result = result .. oct_to_bin_map[char]
    end
    
    return result
end

-------------------------------------------------------------------------------
-- 二进制字符串操作
-------------------------------------------------------------------------------

--- 去除前导零
-- @param binary 二进制字符串
-- @return string 去除前导零后的字符串
function BinaryUtils.strip_leading_zeros(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local stripped = binary:gsub("^0+", "")
    
    if stripped == "" then
        return "0"
    end
    
    return stripped
end

--- 补齐位数
-- @param binary 二进制字符串
-- @param bits 目标位数
-- @return string 补齐后的二进制字符串
function BinaryUtils.pad_binary(binary, bits)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    if #binary >= bits then
        return binary:sub(#binary - bits + 1)
    end
    
    return string.rep("0", bits - #binary) .. binary
end

--- 反转二进制字符串
-- @param binary 二进制字符串
-- @return string 反转后的字符串
function BinaryUtils.reverse_binary(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return binary:reverse()
end

--- 获取指定位
-- @param binary 二进制字符串
-- @param position 位位置（从左开始，1为第一位）
-- @return number 该位的值（0或1）
function BinaryUtils.get_bit(binary, position)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    if position < 1 or position > #binary then
        error(BinaryUtils.Error.InvalidBitPosition)
    end
    
    return tonumber(binary:sub(position, position))
end

--- 设置指定位
-- @param binary 二进制字符串
-- @param position 位位置（从左开始）
-- @param value 要设置的值（0或1）
-- @return string 设置后的二进制字符串
function BinaryUtils.set_bit(binary, position, value)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    if position < 1 or position > #binary then
        error(BinaryUtils.Error.InvalidBitPosition)
    end
    
    value = value or 1
    if value ~= 0 and value ~= 1 then
        value = 1
    end
    
    return binary:sub(1, position - 1) .. tostring(value) .. binary:sub(position + 1)
end

--- 清除指定位（设置为0）
-- @param binary 二进制字符串
-- @param position 位位置
-- @return string 清除后的二进制字符串
function BinaryUtils.clear_bit(binary, position)
    return BinaryUtils.set_bit(binary, position, 0)
end

-------------------------------------------------------------------------------
-- 位运算
-------------------------------------------------------------------------------

--- 按位与操作
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_and(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    -- 补齐位数
    local max_len = math.max(#binary1, #binary2)
    binary1 = BinaryUtils.pad_binary(binary1, max_len)
    binary2 = BinaryUtils.pad_binary(binary2, max_len)
    
    local result = ""
    for i = 1, max_len do
        local b1 = tonumber(binary1:sub(i, i))
        local b2 = tonumber(binary2:sub(i, i))
        result = result .. tostring(b1 * b2)
    end
    
    return result
end

--- 按位或操作
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_or(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local max_len = math.max(#binary1, #binary2)
    binary1 = BinaryUtils.pad_binary(binary1, max_len)
    binary2 = BinaryUtils.pad_binary(binary2, max_len)
    
    local result = ""
    for i = 1, max_len do
        local b1 = tonumber(binary1:sub(i, i))
        local b2 = tonumber(binary2:sub(i, i))
        local bit = 0
        if b1 == 1 or b2 == 1 then
            bit = 1
        end
        result = result .. tostring(bit)
    end
    
    return result
end

--- 按位异或操作
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_xor(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local max_len = math.max(#binary1, #binary2)
    binary1 = BinaryUtils.pad_binary(binary1, max_len)
    binary2 = BinaryUtils.pad_binary(binary2, max_len)
    
    local result = ""
    for i = 1, max_len do
        local b1 = tonumber(binary1:sub(i, i))
        local b2 = tonumber(binary2:sub(i, i))
        local bit = (b1 + b2) % 2
        result = result .. tostring(bit)
    end
    
    return result
end

--- 按位非操作（取反）
-- @param binary 二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_not(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local result = ""
    for i = 1, #binary do
        local bit = tonumber(binary:sub(i, i))
        result = result .. tostring(1 - bit)
    end
    
    return result
end

--- 左移操作
-- @param binary 二进制字符串
-- @param shift 移动位数
-- @return string 结果二进制字符串
function BinaryUtils.left_shift(binary, shift)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    shift = shift or 0
    if shift < 0 then
        return BinaryUtils.right_shift(binary, -shift)
    end
    
    return binary .. string.rep("0", shift)
end

--- 右移操作
-- @param binary 二进制字符串
-- @param shift 移动位数
-- @return string 结果二进制字符串
function BinaryUtils.right_shift(binary, shift)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    shift = shift or 0
    if shift < 0 then
        return BinaryUtils.left_shift(binary, -shift)
    end
    
    if shift >= #binary then
        return "0"
    end
    
    return binary:sub(1, #binary - shift)
end

--- 循环左移
-- @param binary 二进制字符串
-- @param shift 移动位数
-- @return string 结果二进制字符串
function BinaryUtils.rotate_left(binary, shift)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    shift = shift % #binary
    if shift == 0 then
        return binary
    end
    
    return binary:sub(shift + 1) .. binary:sub(1, shift)
end

--- 循环右移
-- @param binary 二进制字符串
-- @param shift 移动位数
-- @return string 结果二进制字符串
function BinaryUtils.rotate_right(binary, shift)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    shift = shift % #binary
    if shift == 0 then
        return binary
    end
    
    return binary:sub(#binary - shift + 1) .. binary:sub(1, #binary - shift)
end

-------------------------------------------------------------------------------
-- 二进制算术运算
-------------------------------------------------------------------------------

--- 二进制加法
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_add(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local result = ""
    local carry = 0
    local i = #binary1
    local j = #binary2
    
    while i > 0 or j > 0 or carry > 0 do
        local b1 = 0
        local b2 = 0
        
        if i > 0 then
            b1 = tonumber(binary1:sub(i, i))
            i = i - 1
        end
        
        if j > 0 then
            b2 = tonumber(binary2:sub(j, j))
            j = j - 1
        end
        
        local sum = b1 + b2 + carry
        result = tostring(sum % 2) .. result
        carry = math.floor(sum / 2)
    end
    
    return result
end

--- 二进制减法
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_sub(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local dec1 = BinaryUtils.binary_to_decimal(binary1)
    local dec2 = BinaryUtils.binary_to_decimal(binary2)
    
    if dec2 > dec1 then
        error(BinaryUtils.Error.Overflow)
    end
    
    return BinaryUtils.decimal_to_binary(dec1 - dec2)
end

--- 二进制乘法
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串
function BinaryUtils.binary_mul(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local dec1 = BinaryUtils.binary_to_decimal(binary1)
    local dec2 = BinaryUtils.binary_to_decimal(binary2)
    
    return BinaryUtils.decimal_to_binary(dec1 * dec2)
end

--- 二进制除法
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串（商）
function BinaryUtils.binary_div(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local dec2 = BinaryUtils.binary_to_decimal(binary2)
    if dec2 == 0 then
        error(BinaryUtils.Error.DivideByZero)
    end
    
    local dec1 = BinaryUtils.binary_to_decimal(binary1)
    
    return BinaryUtils.decimal_to_binary(math.floor(dec1 / dec2))
end

--- 二进制取模
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return string 结果二进制字符串（余数）
function BinaryUtils.binary_mod(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local dec2 = BinaryUtils.binary_to_decimal(binary2)
    if dec2 == 0 then
        error(BinaryUtils.Error.DivideByZero)
    end
    
    local dec1 = BinaryUtils.binary_to_decimal(binary1)
    
    return BinaryUtils.decimal_to_binary(dec1 % dec2)
end

-------------------------------------------------------------------------------
-- 统计与计算
-------------------------------------------------------------------------------

--- 计算二进制字符串中1的个数
-- @param binary 二进制字符串
-- @return number 1的个数
function BinaryUtils.count_bits(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local count = 0
    for i = 1, #binary do
        if binary:sub(i, i) == "1" then
            count = count + 1
        end
    end
    
    return count
end

--- 计算二进制字符串中0的个数
-- @param binary 二进制字符串
-- @return number 0的个数
function BinaryUtils.count_zeros(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local count = 0
    for i = 1, #binary do
        if binary:sub(i, i) == "0" then
            count = count + 1
        end
    end
    
    return count
end

--- 计算汉明权重（同count_bits）
-- @param binary 二进制字符串
-- @return number 汉明权重
function BinaryUtils.hamming_weight(binary)
    return BinaryUtils.count_bits(binary)
end

--- 计算汉明距离（两个二进制字符串不同位的个数）
-- @param binary1 第一个二进制字符串
-- @param binary2 第二个二进制字符串
-- @return number 汉明距离
function BinaryUtils.hamming_distance(binary1, binary2)
    if not BinaryUtils.is_valid_binary(binary1) or not BinaryUtils.is_valid_binary(binary2) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local max_len = math.max(#binary1, #binary2)
    binary1 = BinaryUtils.pad_binary(binary1, max_len)
    binary2 = BinaryUtils.pad_binary(binary2, max_len)
    
    local distance = 0
    for i = 1, max_len do
        if binary1:sub(i, i) ~= binary2:sub(i, i) then
            distance = distance + 1
        end
    end
    
    return distance
end

-------------------------------------------------------------------------------
-- 模式匹配与查找
-------------------------------------------------------------------------------

--- 查找第一个1的位置
-- @param binary 二进制字符串
-- @return number 位置索引（从1开始），如果没有1则返回nil
function BinaryUtils.find_first_one(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return binary:find("1")
end

--- 查找最后一个1的位置
-- @param binary 二进制字符串
-- @return number 位置索引（从1开始），如果没有1则返回nil
function BinaryUtils.find_last_one(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    for i = #binary, 1, -1 do
        if binary:sub(i, i) == "1" then
            return i
        end
    end
    
    return nil
end

--- 查找第一个0的位置
-- @param binary 二进制字符串
-- @return number 位置索引（从1开始），如果没有0则返回nil
function BinaryUtils.find_first_zero(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return binary:find("0")
end

--- 查找最后一个0的位置
-- @param binary 二进制字符串
-- @return number 位置索引（从1开始），如果没有0则返回nil
function BinaryUtils.find_last_zero(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    for i = #binary, 1, -1 do
        if binary:sub(i, i) == "0" then
            return i
        end
    end
    
    return nil
end

--- 查找子串
-- @param binary 二进制字符串
-- @param pattern 要查找的模式
-- @return number|nil 找到的起始位置或nil
function BinaryUtils.find_pattern(binary, pattern)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    if not BinaryUtils.is_valid_binary(pattern) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return binary:find(pattern)
end

--- 查找所有匹配位置
-- @param binary 二进制字符串
-- @param pattern 要查找的模式
-- @return table 所有匹配位置的列表
function BinaryUtils.find_all_patterns(binary, pattern)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    if not BinaryUtils.is_valid_binary(pattern) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local positions = {}
    local start = 1
    
    while true do
        local pos = binary:find(pattern, start)
        if pos == nil then
            break
        end
        table.insert(positions, pos)
        start = pos + 1
    end
    
    return positions
end

-------------------------------------------------------------------------------
-- 特殊功能
-------------------------------------------------------------------------------

--- 生成指定长度的随机二进制字符串
-- @param length 长度
-- @return string 随机二进制字符串
function BinaryUtils.random_binary(length)
    length = length or 8
    
    local result = ""
    for i = 1, length do
        if math.random() < 0.5 then
            result = result .. "0"
        else
            result = result .. "1"
        end
    end
    
    return result
end

--- 检查是否为偶数（二进制最后一位为0）
-- @param binary 二进制字符串
-- @return boolean 是否为偶数
function BinaryUtils.is_even(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return binary:sub(#binary, #binary) == "0"
end

--- 检查是否为奇数（二进制最后一位为1）
-- @param binary 二进制字符串
-- @return boolean 是否为奇数
function BinaryUtils.is_odd(binary)
    return not BinaryUtils.is_even(binary)
end

--- 检查是否为二的幂次
-- @param binary 二进制字符串
-- @return boolean 是否为二的幂次
function BinaryUtils.is_power_of_two(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local stripped = BinaryUtils.strip_leading_zeros(binary)
    return BinaryUtils.count_bits(stripped) == 1
end

--- 获取二进制字符串长度（位数）
-- @param binary 二进制字符串
-- @return number 位数
function BinaryUtils.bit_length(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return #binary
end

--- 格式化二进制字符串为字节组
-- @param binary 二进制字符串
-- @return string 格式化后的字符串（每8位一组）
function BinaryUtils.format_as_bytes(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    -- 补齐到8位一组
    local padded = binary
    while #padded % 8 ~= 0 do
        padded = "0" .. padded
    end
    
    local result = ""
    for i = 1, #padded, 8 do
        if result ~= "" then
            result = result .. " "
        end
        result = result .. padded:sub(i, i + 7)
    end
    
    return result
end

--- 从补码解析负数
-- @param binary 补码表示的二进制字符串
-- @param bits 位数
-- @return number 十进制数值（可以是负数）
function BinaryUtils.twos_complement_to_decimal(binary, bits)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    bits = bits or #binary
    
    -- 检查是否为负数（最高位为1）
    if binary:sub(1, 1) == "0" then
        return BinaryUtils.binary_to_decimal(binary)
    end
    
    -- 负数：取反加一得到绝对值
    local inverted = BinaryUtils.binary_not(binary)
    local absolute = BinaryUtils.binary_add(inverted, "1")
    
    local value = BinaryUtils.binary_to_decimal(BinaryUtils.strip_leading_zeros(absolute))
    return -value
end

--- 获取最高有效位位置
-- @param binary 二进制字符串
-- @return number 最高有效位位置（从1开始）
function BinaryUtils.get_msb_position(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return BinaryUtils.find_first_one(binary)
end

--- 获取最低有效位位置
-- @param binary 二进制字符串
-- @return number 最低有效位位置（从1开始）
function BinaryUtils.get_lsb_position(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    return BinaryUtils.find_last_one(binary)
end

-------------------------------------------------------------------------------
-- 字节操作
-------------------------------------------------------------------------------

--- 二进制字符串转字节数组
-- @param binary 二进制字符串
-- @return table 字节值数组
function BinaryUtils.to_byte_array(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    -- 补齐到8位一组
    local padded = binary
    while #padded % 8 ~= 0 do
        padded = "0" .. padded
    end
    
    local bytes = {}
    for i = 1, #padded, 8 do
        local chunk = padded:sub(i, i + 7)
        table.insert(bytes, BinaryUtils.binary_to_decimal(chunk))
    end
    
    return bytes
end

--- 字节数组转二进制字符串
-- @param bytes 字节值数组
-- @return string 二进制字符串
function BinaryUtils.from_byte_array(bytes)
    if bytes == nil or type(bytes) ~= "table" then
        error(BinaryUtils.Error.InvalidArgument)
    end
    
    local result = ""
    for _, byte in ipairs(bytes) do
        result = result .. BinaryUtils.decimal_to_binary(byte, 8)
    end
    
    return result
end

--- ASCII字符转二进制
-- @param char ASCII字符
-- @return string 8位二进制字符串
function BinaryUtils.char_to_binary(char)
    if char == nil or type(char) ~= "string" or #char ~= 1 then
        error(BinaryUtils.Error.InvalidArgument)
    end
    
    return BinaryUtils.decimal_to_binary(string.byte(char), 8)
end

--- 二进制转ASCII字符
-- @param binary 8位二进制字符串
-- @return string ASCII字符
function BinaryUtils.binary_to_char(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    local value = BinaryUtils.binary_to_decimal(binary)
    return string.char(value)
end

--- 字符串转二进制
-- @param str 字符串
-- @return string 二进制字符串
function BinaryUtils.string_to_binary(str)
    if str == nil or type(str) ~= "string" then
        error(BinaryUtils.Error.InvalidArgument)
    end
    
    local result = ""
    for i = 1, #str do
        result = result .. BinaryUtils.char_to_binary(str:sub(i, i))
    end
    
    return result
end

--- 二进制转字符串
-- @param binary 二进制字符串（长度应为8的倍数）
-- @return string 字符串
function BinaryUtils.binary_to_string(binary)
    if not BinaryUtils.is_valid_binary(binary) then
        error(BinaryUtils.Error.InvalidBinary)
    end
    
    -- 补齐到8位一组
    local padded = binary
    while #padded % 8 ~= 0 do
        padded = "0" .. padded
    end
    
    local result = ""
    for i = 1, #padded, 8 do
        local chunk = padded:sub(i, i + 7)
        result = result .. BinaryUtils.binary_to_char(chunk)
    end
    
    return result
end

-------------------------------------------------------------------------------
-- 工厂函数
-------------------------------------------------------------------------------

--- 创建二进制对象
-- @param value 值（可以是数字或字符串）
-- @param bits 可选，位数
-- @return table 二进制对象
function BinaryUtils.create(value, bits)
    local binary
    
    if type(value) == "number" then
        binary = BinaryUtils.decimal_to_binary(value, bits)
    elseif type(value) == "string" then
        if BinaryUtils.is_valid_binary(value) then
            binary = value
        elseif BinaryUtils.is_valid_hex(value) then
            binary = BinaryUtils.hex_to_binary(value)
        elseif BinaryUtils.is_valid_octal(value) then
            binary = BinaryUtils.octal_to_binary(value)
        else
            binary = BinaryUtils.string_to_binary(value)
        end
    else
        error(BinaryUtils.Error.InvalidArgument)
    end
    
    local obj = {
        binary = binary,
        bits = bits or #binary,
    }
    
    -- 添加方法
    obj.to_decimal = function()
        return BinaryUtils.binary_to_decimal(obj.binary)
    end
    
    obj.to_hex = function()
        return BinaryUtils.binary_to_hex(obj.binary)
    end
    
    obj.to_octal = function()
        return BinaryUtils.binary_to_octal(obj.binary)
    end
    
    obj.and_ = function(other)
        local other_binary = type(other) == "string" and other or other.binary
        return BinaryUtils.create(BinaryUtils.binary_and(obj.binary, other_binary))
    end
    
    obj.or_ = function(other)
        local other_binary = type(other) == "string" and other or other.binary
        return BinaryUtils.create(BinaryUtils.binary_or(obj.binary, other_binary))
    end
    
    obj.xor_ = function(other)
        local other_binary = type(other) == "string" and other or other.binary
        return BinaryUtils.create(BinaryUtils.binary_xor(obj.binary, other_binary))
    end
    
    obj.not_ = function()
        return BinaryUtils.create(BinaryUtils.binary_not(obj.binary))
    end
    
    obj.shift_left = function(shift)
        return BinaryUtils.create(BinaryUtils.left_shift(obj.binary, shift))
    end
    
    obj.shift_right = function(shift)
        return BinaryUtils.create(BinaryUtils.right_shift(obj.binary, shift))
    end
    
    return obj
end

return BinaryUtils