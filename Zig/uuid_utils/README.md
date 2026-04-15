# UUID Utils - Zig

高效、零依赖的 Zig UUID 生成与解析工具库。

## 功能特性

- ✅ **UUID v4 生成** - 基于随机数生成 RFC 4122 兼容的 UUID
- ✅ **UUID 解析** - 支持带连字符和不带连字符的格式
- ✅ **格式转换** - 标准格式和紧凑格式输出
- ✅ **版本检测** - 自动识别 UUID 版本（v1-v5）
- ✅ **变体检测** - 自动识别 UUID 变体（NCS/RFC 4122/Microsoft/Future）
- ✅ **验证功能** - 检查 UUID 字符串格式有效性
- ✅ **Nil UUID** - 生成全零 UUID
- ✅ **比较排序** - 支持相等比较和排序
- ✅ **哈希支持** - 可用作哈希表键
- ✅ **预分配缓冲区** - 支持无分配字符串输出
- ✅ **100% 测试覆盖** - 完整的单元测试
- ✅ **零外部依赖** - 仅使用 Zig 标准库

## 安装

将此模块添加到你的 `build.zig.zon`:

```zig
.{
    .dependencies = .{
        .uuid_utils = .{
            .path = "path/to/uuid_utils",
        },
    },
}
```

在 `build.zig` 中:

```zig
const uuid_mod = b.addModule("uuid_utils", .{
    .root_source_file = b.path("path/to/uuid_utils/src/main.zig"),
});
exe.root_module.addImport("uuid_utils", uuid_mod);
```

## 快速开始

```zig
const std = @import("std");
const uuid = @import("uuid_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // 生成 UUID v4
    const uuid1 = try uuid.generateV4();
    const str = try uuid1.toString(allocator);
    defer allocator.free(str);
    std.debug.print("UUID: {s}\n", .{str});

    // 解析 UUID
    const uuid2 = try uuid.UUID.parse("550e8400-e29b-41d4-a716-446655440000");

    // 比较
    if (uuid1.eql(uuid2)) {
        std.debug.print("UUIDs are equal\n", .{});
    }
}
```

## API 文档

### 类型

#### UUID

UUID 主结构体，包含 16 字节数据。

```zig
pub const UUID = struct {
    bytes: [16]u8,
    
    pub fn parse(input: []const u8) UUIDError!UUID;
    pub fn toString(self: UUID, allocator: std.mem.Allocator) UUIDError![]u8;
    pub fn toCompactString(self: UUID, allocator: std.mem.Allocator) UUIDError![]u8;
    pub fn toStringInto(self: UUID, buffer: []u8) usize;
    pub fn version(self: UUID) Version;
    pub fn variant(self: UUID) Variant;
    pub fn isNil(self: UUID) bool;
    pub fn eql(self: UUID, other: UUID) bool;
    pub fn lessThan(self: UUID, other: UUID) bool;
    pub fn hash(self: UUID) u64;
};
```

#### Version

UUID 版本枚举。

```zig
pub const Version = enum(u4) {
    v1 = 1, // Time-based
    v2 = 2, // DCE Security
    v3 = 3, // MD5 hash
    v4 = 4, // Random
    v5 = 5, // SHA-1 hash
};
```

#### Variant

UUID 变体枚举。

```zig
pub const Variant = enum(u2) {
    ncs = 0,       // NCS backward compatibility
    rfc4122 = 2,   // Standard RFC 4122
    microsoft = 1, // Microsoft backward compatibility
    future = 3,    // Reserved for future
};
```

### 函数

#### generateV4

```zig
pub fn generateV4() UUIDError!UUID
```

生成随机 UUID v4。使用系统随机源初始化。

#### generateV4WithSeed

```zig
pub fn generateV4WithSeed(seed: u64) UUID
```

使用固定种子生成 UUID v4。相同种子产生相同 UUID（用于测试）。

#### nil

```zig
pub fn nil() UUID
```

生成全零的 Nil UUID。

#### isValid

```zig
pub fn isValid(input: []const u8) bool
```

检查字符串是否为有效的 UUID 格式。

### 错误类型

```zig
pub const UUIDError = error{
    InvalidFormat,       // 无效的 UUID 格式
    InvalidHexCharacter, // 无效的十六进制字符
    OutOfMemory,         // 内存分配失败
    RandomError,         // 随机数生成失败
};
```

## 使用示例

### 生成和格式化

```zig
const allocator = std.heap.page_allocator;

// 生成 UUID v4
const uuid = try uuid.generateV4();

// 标准格式（带连字符）
const standard = try uuid.toString(allocator);
defer allocator.free(standard);
// 输出: "550e8400-e29b-41d4-a716-446655440000"

// 紧凑格式（无连字符）
const compact = try uuid.toCompactString(allocator);
defer allocator.free(compact);
// 输出: "550e8400e29b41d4a716446655440000"

// 预分配缓冲区（无内存分配）
var buffer: [36]u8 = undefined;
const len = uuid.toStringInto(&buffer);
std.debug.print("{s}\n", .{buffer[0..len]});
```

### 解析和验证

```zig
// 解析带连字符的 UUID
const uuid1 = try uuid.UUID.parse("550e8400-e29b-41d4-a716-446655440000");

// 解析不带连字符的 UUID
const uuid2 = try uuid.UUID.parse("550e8400e29b41d4a716446655440000");

// 验证格式
if (uuid.isValid(user_input)) {
    const parsed = try uuid.UUID.parse(user_input);
    // 使用 parsed...
}
```

### 版本和变体检测

```zig
const uuid = try uuid.UUID.parse("550e8400-e29b-41d4-a716-446655440000");

std.debug.print("版本: {}\n", .{uuid.version()});   // v4
std.debug.print("变体: {}\n", .{uuid.variant()});   // rfc4122
```

### 比较

```zig
const uuid1 = try uuid.generateV4();
const uuid2 = try uuid.generateV4();

// 相等比较
if (uuid1.eql(uuid2)) {
    std.debug.print("UUIDs are equal\n", .{});
}

// 排序
if (uuid1.lessThan(uuid2)) {
    std.debug.print("uuid1 comes before uuid2\n", .{});
}
```

### Nil UUID

```zig
const nil_uuid = uuid.nil();

if (nil_uuid.isNil()) {
    std.debug.print("This is a nil UUID\n", .{});
}
```

## 构建与测试

```bash
# 构建库
zig build

# 运行测试
zig build test

# 运行示例
zig build example

# 运行性能测试
zig build benchmark
```

## 性能

在典型现代硬件上的大致性能：

| 操作 | 性能 |
|------|------|
| 生成 UUID v4 | ~220 ns/UUID |
| 解析 UUID | ~540 ns/次 |
| toString（分配） | ~4 μs/次 |
| toStringInto（预分配） | ~130 ns/次 |

## UUID 格式

UUID 是 128 位标识符，标准格式为：

```
xxxxxxxx-xxxx-Vxxx-Nxxx-xxxxxxxxxxxx
```

- `V` = 版本号（v4 = 随机）
- `N` = 变体标识（RFC 4122 = 8, 9, A, B）

示例：
- `550e8400-e29b-41d4-a716-446655440000`
- `6ba7b810-9dad-11d1-80b4-00c04fd430c8`

## 许可证

MIT License