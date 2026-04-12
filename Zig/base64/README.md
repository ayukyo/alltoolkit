# Base64 Utils - Zig

一个高效、零依赖的 Zig Base64 编码/解码工具库。

## 功能特性

- ✅ **标准 Base64 编码/解码** - 完全符合 RFC 4648 规范
- ✅ **URL 安全模式** - 支持 URL-safe 编码（使用 `-` 和 `_` 替代 `+` 和 `/`）
- ✅ **可选填充** - 支持有填充和无填充两种模式
- ✅ **预分配缓冲区** - 支持编码到预分配缓冲区，避免额外内存分配
- ✅ **输入验证** - 提供 `isValid()` 函数验证 Base64 字符串有效性
- ✅ **长度计算** - 提供 `encodedLen()` 和 `decodedLen()` 计算输出长度
- ✅ **100% 测试覆盖** - 完整的单元测试，包括 RFC 4648 测试向量
- ✅ **零外部依赖** - 仅使用 Zig 标准库

## 安装

将此模块添加到你的 `build.zig.zon`:

```zig
.{
    .dependencies = .{
        .base64 = .{
            .path = "path/to/base64",
        },
    },
}
```

在 `build.zig` 中:

```zig
const base64_mod = b.addModule("base64", .{
    .root_source_file = b.path("path/to/base64/src/main.zig"),
});
exe.root_module.addImport("base64", base64_mod);
```

## 快速开始

```zig
const std = @import("std");
const base64 = @import("base64");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // 编码
    const text = "Hello, World!";
    const encoded = try base64.encode(allocator, text, .{});
    defer allocator.free(encoded);
    std.debug.print("Encoded: {s}\n", .{encoded}); // SGVsbG8sIFdvcmxkIQ==

    // 解码
    const decoded = try base64.decode(allocator, encoded, .{});
    defer allocator.free(decoded);
    std.debug.print("Decoded: {s}\n", .{decoded}); // Hello, World!
}
```

## API 文档

### 编码选项

```zig
pub const EncodeOptions = struct {
    /// URL 安全编码（使用 - 和 _ 替代 + 和 /）
    url_safe: bool = false,
    /// 添加填充字符（=）
    padding: bool = true,
};
```

### 解码选项

```zig
pub const DecodeOptions = struct {
    /// 期望 URL 安全编码
    url_safe: bool = false,
    /// 严格验证填充
    strict_padding: bool = true,
};
```

### 错误类型

```zig
pub const Base64Error = error{
    InvalidCharacter,  // 输入包含无效字符
    InvalidPadding,    // 填充无效
    BufferTooSmall,    // 输出缓冲区太小
};
```

### 函数

#### encode

```zig
pub fn encode(
    allocator: std.mem.Allocator,
    input: []const u8,
    options: EncodeOptions
) ![]u8
```

将字节编码为 Base64 字符串。调用者拥有返回内存的所有权。

#### decode

```zig
pub fn decode(
    allocator: std.mem.Allocator,
    input: []const u8,
    options: DecodeOptions
) Base64Error![]u8
```

将 Base64 字符串解码为字节。调用者拥有返回内存的所有权。自动忽略空白字符。

#### encodeInto

```zig
pub fn encodeInto(
    output: []u8,
    input: []const u8,
    options: EncodeOptions
) Base64Error!usize
```

编码到预分配缓冲区。返回写入的字节数。

#### decodeInto

```zig
pub fn decodeInto(
    output: []u8,
    input: []const u8,
    options: DecodeOptions
) Base64Error!usize
```

解码到预分配缓冲区。返回写入的字节数。

#### isValid

```zig
pub fn isValid(input: []const u8, options: DecodeOptions) bool
```

检查字符串是否为有效的 Base64。

#### encodedLen

```zig
pub fn encodedLen(input_len: usize, options: EncodeOptions) usize
```

计算编码后的字符串长度。

#### decodedLen

```zig
pub fn decodedLen(input_len: usize) usize
```

计算解码后的字节长度（上限）。

## 使用示例

### URL 安全编码

```zig
const binary_data = "\xFF\xFE\xFD\xFC";
const url_safe = try base64.encode(allocator, binary_data, .{ .url_safe = true });
// 输出不含 + 和 /，适合 URL 和文件名使用
```

### 无填充模式

```zig
const text = "Hello";
const no_padding = try base64.encode(allocator, text, .{ .padding = false });
// 输出不含 = 字符
```

### 预分配缓冲区

```zig
var buffer: [100]u8 = undefined;
const text = "Hello, World!";
const written = try base64.encodeInto(&buffer, text, .{});
// 使用 buffer[0..written]
```

### 验证输入

```zig
if (base64.isValid(user_input, .{})) {
    const decoded = try base64.decode(allocator, user_input, .{});
    // 安全使用解码数据
}
```

## 构建与测试

```bash
# 构建库
zig build

# 运行测试
zig build test

# 运行示例
zig build run
```

## RFC 4648 测试向量

本实现通过所有 RFC 4648 标准测试向量：

| 输入      | 编码输出     |
|-----------|--------------|
| (空)      | (空)         |
| f         | Zg==         |
| fo        | Zm8=         |
| foo       | Zm9v         |
| foob      | Zm9vYg==     |
| fooba     | Zm9vYmE=     |
| foobar    | Zm9vYmFy     |

## 性能特点

- O(n) 时间复杂度
- 单次内存分配
- 支持预分配缓冲区避免内存分配
- 无动态内存分配（使用预分配缓冲区时）

## 许可证

MIT License