# Roman Numeral Utils - Zig 罗马数字工具库

**零依赖、生产就绪的罗马数字转换与操作工具**

---

## ✨ 功能特性

- **整数转罗马数字** - 支持 1-3999 范围的所有整数
- **罗马数字转整数** - 支持大小写不敏感的输入
- **验证功能** - 验证罗马数字格式合法性
- **算术运算** - 加、减、乘、除运算
- **比较功能** - 比较两个罗马数字的大小
- **信息获取** - 获取罗马数字的详细信息
- **范围生成** - 生成指定范围内的罗马数字列表

---

## 🚀 快速开始

### 基本使用

```zig
const std = @import("std");
const roman = @import("roman_numeral_utils/mod.zig");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // 整数转罗马数字
    const result = try roman.intToRoman(allocator, 2024);
    defer allocator.free(result);
    std.debug.print("2024 -> {s}\n", .{result}); // MMXXIV
    
    // 罗马数字转整数
    const value = try roman.romanToInt("MMXXIV");
    std.debug.print("MMXXIV -> {}\n", .{value}); // 2024
    
    // 验证罗马数字
    const valid = roman.isValidRoman("IV");
    std.debug.print("IV valid: {}\n", .{valid}); // true
}
```

---

## 📚 API 文档

### intToRoman

将整数转换为罗马数字。

```zig
pub fn intToRoman(allocator: std.mem.Allocator, num: u32) RomanError![]u8
```

**参数：**
- `allocator`: 内存分配器
- `num`: 要转换的整数 (1-3999)

**返回：**
- 罗马数字字符串

**错误：**
- `OutOfRange`: 数字超出 1-3999 范围

**示例：**

```zig
const r1 = try roman.intToRoman(allocator, 1);    // "I"
const r2 = try roman.intToRoman(allocator, 4);    // "IV"
const r3 = try roman.intToRoman(allocator, 2024); // "MMXXIV"
const r4 = try roman.intToRoman(allocator, 3999); // "MMMCMXCIX"
```

---

### romanToInt

将罗马数字转换为整数。

```zig
pub fn romanToInt(roman: []const u8) RomanError!u32
```

**参数：**
- `roman`: 罗马数字字符串（大小写不敏感）

**返回：**
- 对应的整数

**错误：**
- `EmptyInput`: 输入为空字符串
- `InvalidCharacter`: 包含无效字符
- `InvalidRomanNumeral`: 无效的罗马数字格式

**示例：**

```zig
const v1 = try roman.romanToInt("I");      // 1
const v2 = try roman.romanToInt("IV");     // 4
const v3 = try roman.romanToInt("MMXXIV"); // 2024
const v4 = try roman.romanToInt("mmxxiv"); // 2024 (大小写不敏感)
```

---

### isValidRoman

验证字符串是否为有效的罗马数字。

```zig
pub fn isValidRoman(roman: []const u8) bool
```

**参数：**
- `roman`: 要验证的字符串

**返回：**
- `true` 如果是有效的罗马数字，否则 `false`

**示例：**

```zig
const valid1 = roman.isValidRoman("IV");    // true
const valid2 = roman.isValidRoman("IIII");  // false (I重复超过3次)
const valid3 = roman.isValidRoman("VV");    // false (V不能重复)
const valid4 = roman.isValidRoman("IM");    // false (I不能减M)
```

---

### romanAdd

两个罗马数字相加。

```zig
pub fn romanAdd(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError![]u8
```

**示例：**

```zig
const result1 = try roman.romanAdd(allocator, "X", "V");  // "XV"
const result2 = try roman.romanAdd(allocator, "IV", "VI"); // "X"
```

---

### romanSubtract

两个罗马数字相减。

```zig
pub fn romanSubtract(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError![]u8
```

**示例：**

```zig
const result1 = try roman.romanSubtract(allocator, "X", "V"); // "V"
const result2 = try roman.romanSubtract(allocator, "X", "I"); // "IX"
```

---

### romanMultiply

两个罗马数字相乘。

```zig
pub fn romanMultiply(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError![]u8
```

**示例：**

```zig
const result1 = try roman.romanMultiply(allocator, "V", "II"); // "X"
const result2 = try roman.romanMultiply(allocator, "X", "X");  // "C"
```

---

### romanDivide

两个罗马数字相除，返回商和余数。

```zig
pub fn romanDivide(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError!struct { []u8, []u8 }
```

**示例：**

```zig
const div1 = try roman.romanDivide(allocator, "X", "III");
defer allocator.free(div1[0]);
defer allocator.free(div1[1]);
std.debug.print("{s} 余 {s}\n", .{div1[0], div1[1]}); // "III" 余 "I"

const div2 = try roman.romanDivide(allocator, "X", "II");
defer allocator.free(div2[0]);
defer allocator.free(div2[1]);
std.debug.print("{s} 余 {s}\n", .{div2[0], div2[1]}); // "V" 余 ""
```

---

### romanCompare

比较两个罗马数字的大小。

```zig
pub fn romanCompare(roman1: []const u8, roman2: []const u8) RomanError!i32
```

**返回：**
- `-1` 如果 `roman1 < roman2`
- `0` 如果 `roman1 == roman2`
- `1` 如果 `roman1 > roman2`

**示例：**

```zig
const cmp1 = try roman.romanCompare("V", "X");  // -1 (V < X)
const cmp2 = try roman.romanCompare("X", "X");  // 0 (X == X)
const cmp3 = try roman.romanCompare("X", "V");  // 1 (X > V)
```

---

### getRomanInfo

获取罗马数字的详细信息。

```zig
pub fn getRomanInfo(allocator: std.mem.Allocator, roman: []const u8) RomanError!RomanInfo
```

**返回结构：**

```zig
pub const RomanInfo = struct {
    original: []const u8,  // 原始输入
    value: u32,            // 数值
    valid: bool,           // 是否有效
    length: usize,         // 长度
    components: ?[]const u8, // 规范化组件
};
```

**示例：**

```zig
var info = try roman.getRomanInfo(allocator, "MMXXIV");
defer info.deinit();
std.debug.print("值: {}, 长度: {}, 有效: {}\n", .{info.value, info.length, info.valid});
```

---

### findRomanRange

生成指定范围内所有整数的罗马数字列表。

```zig
pub fn findRomanRange(allocator: std.mem.Allocator, start: u32, end: u32) RomanError![]struct { u32, []u8 }
```

**示例：**

```zig
const range = try roman.findRomanRange(allocator, 1, 10);
defer {
    for (range) |entry| {
        allocator.free(entry[1]);
    }
    allocator.free(range);
}
for (range) |entry| {
    std.debug.print("{} = {s}\n", .{entry[0], entry[1]});
}
// 输出: 1 = I, 2 = II, 3 = III, ..., 10 = X
```

---

## 📋 罗马数字规则

### 基本符号

| 符号 | 值 |
|------|-----|
| I | 1 |
| V | 5 |
| X | 10 |
| L | 50 |
| C | 100 |
| D | 500 |
| M | 1000 |

### 减法原则

罗马数字使用减法原则来避免过多的重复：

| 组合 | 值 | 解释 |
|------|-----|------|
| IV | 4 | 5 - 1 |
| IX | 9 | 10 - 1 |
| XL | 40 | 50 - 10 |
| XC | 90 | 100 - 10 |
| CD | 400 | 500 - 100 |
| CM | 900 | 1000 - 100 |

### 重复规则

- **I, X, C, M** 可以最多重复 3 次
- **V, L, D** 不能重复

### 减法限制

- **I** 只能减 **V** 和 **X**
- **X** 只能减 **L** 和 **C**
- **C** 只能减 **D** 和 **M**

---

## 🧪 测试

运行测试：

```bash
# 运行单元测试
zig test mod.zig

# 运行完整测试套件
zig run roman_numeral_utils_test.zig
```

### 测试覆盖

- ✅ 基本转换测试 (30+ 测试用例)
- ✅ 反向转换测试 (25+ 测试用例)
- ✅ 大小写不敏感测试
- ✅ 无效输入测试 (12+ 测试用例)
- ✅ 验证函数测试
- ✅ 算术运算测试 (加/减/乘/除)
- ✅ 比较测试
- ✅ 历史年份测试
- ✅ 往返转换测试 (1-100)
- ✅ 边界值测试
- ✅ 信息获取测试
- ✅ 范围生成测试

---

## 📝 常见罗马数字

| 数字 | 罗马数字 | 说明 |
|------|----------|------|
| 1 | I | 基本单位 |
| 4 | IV | 第一个减法组合 |
| 5 | V | 五 |
| 10 | X | 十 |
| 50 | L | 五十 |
| 100 | C | 百 |
| 500 | D | 五百 |
| 1000 | M | 千 |
| 1984 | MCMLXXXIV | Orwell 年 |
| 1999 | MCMXCIX | 千禧年前 |
| 2024 | MMXXIV | 当前年份 |
| 3999 | MMMCMXCIX | 最大值 |

---

## 📜 历史年份示例

| 年份 | 罗马数字 | 事件 |
|------|----------|------|
| 753 | DCCLIII | 罗马建城 |
| 1066 | MLXVI | 诺曼征服 |
| 1215 | MCCXV | 大宪章 |
| 1492 | MCDXCII | 哥伦布发现新大陆 |
| 1776 | MDCCLXXVI | 美国独立 |
| 1789 | MDCCLXXXIX | 法国大革命 |
| 1914 | MCMXIV | 一战开始 |
| 1945 | MCMXLV | 二战结束 |
| 1969 | MCMLXIX | 人类登月 |

---

## ⚠️ 错误处理

```zig
pub const RomanError = error{
    InvalidRomanNumeral,  // 无效的罗马数字格式
    OutOfRange,           // 数字超出范围 (1-3999)
    EmptyInput,           // 输入为空
    InvalidCharacter,     // 包含无效字符
    DivisionByZero,       // 除数为零
};
```

---

## 📄 许可证

MIT License - 详见项目 LICENSE 文件

---

## 🔗 相关链接

- **AllToolkit 主项目**: https://github.com/ayukyo/alltoolkit
- **Zig 官网**: https://ziglang.org

---

*最后更新: 2026-05-24*