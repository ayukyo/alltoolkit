# text_diff_utils

文本差异比较工具库，用于比较文本差异、生成统一 diff 格式输出、计算相似度等。

## 功能特性

- **行级差异比较**: 按行比较两段文本的差异
- **字符级差异比较**: 按字符比较两段文本的差异
- **统一差异格式**: 生成 Git 风格的 unified diff 输出
- **相似度计算**: 计算两段文本的相似程度 (0.0 - 1.0)
- **零外部依赖**: 纯 Zig 标准库实现

## 构建与测试

```bash
# 构建库
zig build

# 运行测试
zig build test

# 运行示例
zig build example

# 运行性能基准测试
zig build benchmark
```

## 使用示例

### 基本使用

```zig
const std = @import("std");
const text_diff = @import("text_diff_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    const old_text = "第一行\n第二行\n第三行";
    const new_text = "第一行\n修改的行\n第三行";
    
    // 行级差异比较
    const result = try text_diff.diffLines(allocator, old_text, new_text);
    defer result.deinit();
    
    for (result.items) |item| {
        switch (item.op) {
            .equal => std.debug.print("  {s}\n", .{item.text}),
            .delete => std.debug.print("- {s}\n", .{item.text}),
            .insert => std.debug.print("+ {s}\n", .{item.text}),
        }
    }
    
    // 统计信息
    std.debug.print("新增: {d}, 删除: {d}, 未变: {d}\n", .{
        result.stats.additions,
        result.stats.deletions,
        result.stats.unchanged,
    });
}
```

### 字符级差异

```zig
const result = try text_diff.diffChars(allocator, "Hello World", "Hello Zig");
defer result.deinit();

for (result.items) |item| {
    switch (item.op) {
        .equal => std.debug.print("{s}", .{item.text}),
        .delete => std.debug.print("[-{s}]", .{item.text}),
        .insert => std.debug.print("[+{s}]", .{item.text}),
    }
}
// 输出: Hello [-W][-o][-r][-l][-d][+Z][+i][+g]
```

### 统一差异格式

```zig
const diff = try text_diff.unifiedDiff(allocator, old_text, new_text, .{
    .context_lines = 3,
    .old_filename = "original.txt",
    .new_filename = "modified.txt",
});
defer allocator.free(diff);

std.debug.print("{s}", .{diff});
// 输出:
// --- original.txt
// +++ modified.txt
// @@ -1,3 +1,3 @@
//  第一行
// -第二行
// +修改的行
//  第三行
```

### 相似度计算

```zig
const sim = try text_diff.similarity("hello world", "hello there");
std.debug.print("相似度: {d:.1}%\n", .{sim * 100});
// 输出: 相似度: 50.0%
```

## API 文档

### 类型

#### `DiffOp`
```zig
pub const DiffOp = enum {
    equal,   // 相同内容
    insert,  // 新增内容
    delete,  // 删除内容
};
```

#### `DiffItem`
```zig
pub const DiffItem = struct {
    op: DiffOp,        // 操作类型
    text: []const u8,  // 文本内容
};
```

#### `DiffStats`
```zig
pub const DiffStats = struct {
    additions: usize,   // 新增数量
    deletions: usize,   // 删除数量
    unchanged: usize,   // 未改变数量
    
    pub fn total(self: DiffStats) usize;
    pub fn hasChanges(self: DiffStats) bool;
};
```

#### `DiffResult`
```zig
pub const DiffResult = struct {
    items: []DiffItem,          // 差异项列表
    stats: DiffStats,           // 统计信息
    allocator: std.mem.Allocator,
    
    pub fn deinit(self: *DiffResult) void;
    pub fn getAdditions(self: DiffResult, allocator: std.mem.Allocator) ![]u8;
    pub fn getDeletions(self: DiffResult, allocator: std.mem.Allocator) ![]u8;
};
```

#### `UnifiedDiffOptions`
```zig
pub const UnifiedDiffOptions = struct {
    context_lines: usize = 3,        // 上下文行数
    old_filename: []const u8 = "a",  // 旧文件名
    new_filename: []const u8 = "b",  // 新文件名
};
```

### 函数

#### `diffLines`
```zig
pub fn diffLines(allocator: std.mem.Allocator, old_text: []const u8, new_text: []const u8) !DiffResult
```
按行比较两段文本的差异。

#### `diffChars`
```zig
pub fn diffChars(allocator: std.mem.Allocator, old_text: []const u8, new_text: []const u8) !DiffResult
```
按字符比较两段文本的差异。

#### `unifiedDiff`
```zig
pub fn unifiedDiff(allocator: std.mem.Allocator, old_text: []const u8, new_text: []const u8, options: UnifiedDiffOptions) ![]u8
```
生成统一差异格式的输出。

#### `similarity`
```zig
pub fn similarity(old_text: []const u8, new_text: []const u8) !f64
```
计算两段文本的相似度（0.0 到 1.0）。

#### `applyPatch`
```zig
pub fn applyPatch(allocator: std.mem.Allocator, original: []const u8, patch: []const u8) ![]u8
```
应用补丁到原始文本（实验性功能）。

## 算法

本库使用 LCS（最长公共子序列）算法来计算文本差异：

1. 将文本分割成行或字符
2. 构建 LCS 矩阵
3. 回溯矩阵生成差异序列
4. 合并相邻相同操作（字符级模式）

时间复杂度: O(n*m)，其中 n 和 m 是两段文本的长度。

## 许可证

MIT License