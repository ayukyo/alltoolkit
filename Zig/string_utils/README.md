# Zig String Utils

一个全面的 Zig 字符串处理工具库，提供常用的字符串操作功能，零外部依赖。

## 功能特性

### Trim 函数
- `trim` - 去除首尾空白字符
- `trimChars` - 去除首尾指定字符
- `trimLeft` - 去除左侧空白
- `trimLeftChars` - 去除左侧指定字符
- `trimRight` - 去除右侧空白
- `trimRightChars` - 去除右侧指定字符

### 大小写转换
- `toUpper` - 转换为大写
- `toLower` - 转换为小写
- `capitalize` - 首字母大写
- `title` - 标题格式（每个单词首字母大写）
- `swapCase` - 交换大小写

### 字符串操作
- `reverse` - 反转字符串
- `repeat` - 重复字符串
- `replace` - 替换所有匹配项
- `replaceN` - 替换前 N 个匹配项

### 分割与连接
- `split` - 按分隔符分割
- `splitWhitespace` - 按空白分割
- `join` - 连接字符串数组

### 填充
- `padLeft` - 左侧填充
- `padRight` - 右侧填充
- `center` - 居中填充

### 前缀后缀
- `startsWith` - 检查前缀
- `endsWith` - 检查后缀
- `removePrefix` - 移除前缀
- `removeSuffix` - 移除后缀

### 统计
- `count` - 统计子串出现次数
- `countChar` - 统计字符出现次数

### 字符分类
- `isAlpha` - 是否全为字母
- `isDigit` - 是否全为数字
- `isAlnum` - 是否全为字母或数字
- `isWhitespace` - 是否全为空白字符
- `isLower` - 是否全为小写
- `isUpper` - 是否全为大写
- `isBlank` - 是否为空或全为空白

### 其他
- `wordWrap` - 自动换行
- `freeSlice` - 释放字符串数组内存

## 使用方法

### 添加依赖

在 `build.zig.zon` 中添加：

```zig
.{
    .dependencies = .{
        .string_utils = .{
            .path = "../string_utils",
        },
    },
}
```

### 在 build.zig 中导入

```zig
const string_utils_dep = b.dependency("string_utils", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("string_utils", string_utils_dep.module("string_utils"));
```

### 代码示例

```zig
const std = @import("std");
const string_utils = @import("string_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // Trim
    const trimmed = try string_utils.trim(allocator, "   hello world   ");
    defer allocator.free(trimmed);
    std.debug.print("{s}\n", .{trimmed}); // "hello world"

    // Split and Join
    const parts = try string_utils.split(allocator, "a,b,c", ",");
    defer string_utils.freeSlice(allocator, parts);
    
    const join_parts = [_][]const u8{ "red", "green", "blue" };
    const joined = try string_utils.join(allocator, &join_parts, ", ");
    defer allocator.free(joined);
    std.debug.print("{s}\n", .{joined}); // "red, green, blue"

    // Replace
    const replaced = try string_utils.replace(allocator, "hello world", "world", "there");
    defer allocator.free(replaced);
    std.debug.print("{s}\n", .{replaced}); // "hello there"

    // Padding
    const padded = try string_utils.padLeft(allocator, "42", '0', 5);
    defer allocator.free(padded);
    std.debug.print("{s}\n", .{padded}); // "00042"

    // Character classification
    if (string_utils.isAlpha("hello")) {
        std.debug.print("Is alphabetic!\n", .{});
    }
}
```

## 运行测试

```bash
zig build test
```

## 运行示例

```bash
zig build example
```

## API 文档

所有需要分配内存的函数返回 `StringError![]u8`：

```zig
pub const StringError = error{
    OutOfMemory,
    InvalidUtf8,
    InvalidIndex,
    BufferTooSmall,
};
```

**重要**: 所有分配内存的函数都需要调用者负责释放内存。

### 辅助函数

```zig
// 释放字符串数组
pub fn freeSlice(allocator: std.mem.Allocator, slice: [][]u8) void
```

## 性能说明

- 所有函数仅使用 Zig 标准库，无外部依赖
- ASCII 字符串优化处理
- UTF-8 字符串支持（部分函数）
- 内存高效：结果字符串精确分配所需大小

## 许可证

MIT License

## 版本历史

- v1.0.0 (2026-04-15) - 初始版本，包含 30+ 字符串操作函数