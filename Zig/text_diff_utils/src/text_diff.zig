const std = @import("std");

/// 差异操作类型
pub const DiffOp = enum {
    equal,   // 相同
    insert,  // 插入
    delete,  // 删除
};

/// 单个差异项
pub const DiffItem = struct {
    op: DiffOp,
    text: []const u8,

    pub fn init(op: DiffOp, text: []const u8) DiffItem {
        return .{ .op = op, .text = text };
    }
};

/// 差异统计信息
pub const DiffStats = struct {
    additions: usize = 0,    // 新增行数
    deletions: usize = 0,    // 删除行数
    unchanged: usize = 0,    // 未改变行数

    pub fn total(self: DiffStats) usize {
        return self.additions + self.deletions + self.unchanged;
    }

    pub fn hasChanges(self: DiffStats) bool {
        return self.additions > 0 or self.deletions > 0;
    }
};

/// 差异结果
pub const DiffResult = struct {
    items: []DiffItem,
    stats: DiffStats,
    allocator: std.mem.Allocator,
    owns_text: bool = false, // 是否拥有文本内存（需要释放）

    pub fn deinit(self: *DiffResult) void {
        if (self.owns_text) {
            // 释放每个差异项的文本
            for (self.items) |item| {
                self.allocator.free(item.text);
            }
        }
        self.allocator.free(self.items);
    }

    /// 获取所有新增内容
    pub fn getAdditions(self: DiffResult, allocator: std.mem.Allocator) ![]u8 {
        var list = std.ArrayList(u8).init(allocator);
        const writer = list.writer();
        
        for (self.items) |item| {
            if (item.op == .insert) {
                try writer.writeAll(item.text);
            }
        }
        
        return list.toOwnedSlice();
    }

    /// 获取所有删除内容
    pub fn getDeletions(self: DiffResult, allocator: std.mem.Allocator) ![]u8 {
        var list = std.ArrayList(u8).init(allocator);
        const writer = list.writer();
        
        for (self.items) |item| {
            if (item.op == .delete) {
                try writer.writeAll(item.text);
            }
        }
        
        return list.toOwnedSlice();
    }
};

/// 行分割器
fn splitLines(allocator: std.mem.Allocator, text: []const u8) ![][]const u8 {
    // 空文本返回空数组
    if (text.len == 0) {
        return allocator.alloc([]const u8, 0);
    }
    
    var lines = std.ArrayList([]const u8).init(allocator);
    var iter = std.mem.splitScalar(u8, text, '\n');
    
    while (iter.next()) |line| {
        try lines.append(line);
    }
    
    return lines.toOwnedSlice();
}

/// 计算 LCS 长度矩阵
fn computeLCSMatrix(allocator: std.mem.Allocator, a: [][]const u8, b: [][]const u8) ![][]usize {
    const m = a.len;
    const n = b.len;
    
    var matrix = try allocator.alloc([]usize, m + 1);
    for (0..m + 1) |i| {
        matrix[i] = try allocator.alloc(usize, n + 1);
        @memset(matrix[i], 0);
    }
    
    for (0..m) |i| {
        for (0..n) |j| {
            if (std.mem.eql(u8, a[i], b[j])) {
                matrix[i + 1][j + 1] = matrix[i][j] + 1;
            } else {
                matrix[i + 1][j + 1] = @max(matrix[i][j + 1], matrix[i + 1][j]);
            }
        }
    }
    
    return matrix;
}

/// 从 LCS 矩阵回溯生成 diff
fn backtrackLCS(
    allocator: std.mem.Allocator,
    matrix: [][]usize,
    a: [][]const u8,
    b: [][]const u8,
    i: usize,
    j: usize,
) ![]DiffItem {
    var items = std.ArrayList(DiffItem).init(allocator);
    errdefer items.deinit();
    
    var ii = i;
    var jj = j;
    
    while (ii > 0 and jj > 0) {
        if (std.mem.eql(u8, a[ii - 1], b[jj - 1])) {
            try items.append(DiffItem.init(.equal, a[ii - 1]));
            ii -= 1;
            jj -= 1;
        } else if (matrix[ii - 1][jj] > matrix[ii][jj - 1]) {
            try items.append(DiffItem.init(.delete, a[ii - 1]));
            ii -= 1;
        } else {
            try items.append(DiffItem.init(.insert, b[jj - 1]));
            jj -= 1;
        }
    }
    
    while (ii > 0) {
        try items.append(DiffItem.init(.delete, a[ii - 1]));
        ii -= 1;
    }
    
    while (jj > 0) {
        try items.append(DiffItem.init(.insert, b[jj - 1]));
        jj -= 1;
    }
    
    // 反转结果
    const result = try items.toOwnedSlice();
    std.mem.reverse(DiffItem, result);
    return result;
}

/// 释放 LCS 矩阵
fn freeLCSMatrix(allocator: std.mem.Allocator, matrix: [][]usize, len: usize) void {
    for (0..len) |i| {
        allocator.free(matrix[i]);
    }
    allocator.free(matrix);
}

/// 计算两个文本的差异（行级别）
pub fn diffLines(allocator: std.mem.Allocator, old_text: []const u8, new_text: []const u8) !DiffResult {
    const old_lines = try splitLines(allocator, old_text);
    defer allocator.free(old_lines);
    
    const new_lines = try splitLines(allocator, new_text);
    defer allocator.free(new_lines);
    
    if (old_lines.len == 0 and new_lines.len == 0) {
        return DiffResult{
            .items = &[_]DiffItem{},
            .stats = .{},
            .allocator = allocator,
        };
    }
    
    // 特殊情况：一边为空
    if (old_lines.len == 0) {
        var items = try allocator.alloc(DiffItem, new_lines.len);
        for (new_lines, 0..) |line, i| {
            items[i] = DiffItem.init(.insert, line);
        }
        return DiffResult{
            .items = items,
            .stats = .{ .additions = new_lines.len },
            .allocator = allocator,
        };
    }
    
    if (new_lines.len == 0) {
        var items = try allocator.alloc(DiffItem, old_lines.len);
        for (old_lines, 0..) |line, i| {
            items[i] = DiffItem.init(.delete, line);
        }
        return DiffResult{
            .items = items,
            .stats = .{ .deletions = old_lines.len },
            .allocator = allocator,
        };
    }
    
    // 计算 LCS 矩阵
    const matrix = try computeLCSMatrix(allocator, old_lines, new_lines);
    defer freeLCSMatrix(allocator, matrix, old_lines.len + 1);
    
    // 回溯生成 diff
    const items = try backtrackLCS(allocator, matrix, old_lines, new_lines, old_lines.len, new_lines.len);
    
    // 计算统计
    const stats = blk: {
        var s = DiffStats{};
        for (items) |item| {
            switch (item.op) {
                .equal => s.unchanged += 1,
                .insert => s.additions += 1,
                .delete => s.deletions += 1,
            }
        }
        break :blk s;
    };
    
    return DiffResult{
        .items = items,
        .stats = stats,
        .allocator = allocator,
    };
}

/// 计算两个字符串的差异（字符级别）
pub fn diffChars(allocator: std.mem.Allocator, old_text: []const u8, new_text: []const u8) !DiffResult {
    if (old_text.len == 0 and new_text.len == 0) {
        return DiffResult{
            .items = &[_]DiffItem{},
            .stats = .{},
            .allocator = allocator,
        };
    }
    
    // 将每个字符作为单独的元素
    const old_chars = try allocator.alloc([]const u8, old_text.len);
    defer allocator.free(old_chars);
    for (old_text, 0..) |_, i| {
        old_chars[i] = old_text[i .. i + 1];
    }
    
    const new_chars = try allocator.alloc([]const u8, new_text.len);
    defer allocator.free(new_chars);
    for (new_text, 0..) |_, i| {
        new_chars[i] = new_text[i .. i + 1];
    }
    
    // 特殊情况
    if (old_text.len == 0) {
        var items = try allocator.alloc(DiffItem, new_text.len);
        for (new_text, 0..) |_, i| {
            items[i] = DiffItem.init(.insert, new_text[i .. i + 1]);
        }
        return DiffResult{
            .items = items,
            .stats = .{ .additions = new_text.len },
            .allocator = allocator,
        };
    }
    
    if (new_text.len == 0) {
        var items = try allocator.alloc(DiffItem, old_text.len);
        for (old_text, 0..) |_, i| {
            items[i] = DiffItem.init(.delete, old_text[i .. i + 1]);
        }
        return DiffResult{
            .items = items,
            .stats = .{ .deletions = old_text.len },
            .allocator = allocator,
        };
    }
    
    // 计算 LCS 矩阵
    const matrix = try computeLCSMatrix(allocator, old_chars, new_chars);
    defer freeLCSMatrix(allocator, matrix, old_text.len + 1);
    
    // 回溯生成 diff
    const items = try backtrackLCS(allocator, matrix, old_chars, new_chars, old_text.len, new_text.len);
    
    // 合并相邻相同操作
    var merged = std.ArrayList(DiffItem).init(allocator);
    if (items.len > 0) {
        var current_op = items[0].op;
        var current_text = std.ArrayList(u8).init(allocator);
        defer current_text.deinit();
        
        for (items) |item| {
            if (item.op == current_op) {
                try current_text.appendSlice(item.text);
            } else {
                const text = try allocator.dupe(u8, current_text.items);
                try merged.append(DiffItem.init(current_op, text));
                current_text.clearRetainingCapacity();
                try current_text.appendSlice(item.text);
                current_op = item.op;
            }
        }
        const text = try allocator.dupe(u8, current_text.items);
        try merged.append(DiffItem.init(current_op, text));
    }
    
    allocator.free(items);
    
    // 计算统计
    var stats = DiffStats{};
    for (merged.items) |item| {
        switch (item.op) {
            .equal => stats.unchanged += item.text.len,
            .insert => stats.additions += item.text.len,
            .delete => stats.deletions += item.text.len,
        }
    }
    
    return DiffResult{
        .items = try merged.toOwnedSlice(),
        .stats = stats,
        .allocator = allocator,
        .owns_text = true, // diffChars 需要释放文本内存
    };
}

/// 统一 Diff 格式输出
pub const UnifiedDiffOptions = struct {
    context_lines: usize = 3,        // 上下文行数
    old_filename: []const u8 = "a",  // 旧文件名
    new_filename: []const u8 = "b",  // 新文件名
};

/// 生成统一 Diff 格式输出
pub fn unifiedDiff(
    allocator: std.mem.Allocator,
    old_text: []const u8,
    new_text: []const u8,
    options: UnifiedDiffOptions,
) ![]u8 {
    var output = std.ArrayList(u8).init(allocator);
    const writer = output.writer();
    
    var result = try diffLines(allocator, old_text, new_text);
    defer result.deinit();
    
    // 如果没有差异，返回空字符串
    if (!result.stats.hasChanges()) {
        return allocator.dupe(u8, "");
    }
    
    // 文件头
    try writer.print("--- {s}\n", .{options.old_filename});
    try writer.print("+++ {s}\n", .{options.new_filename});
    
    // 查找差异块
    var i: usize = 0;
    while (i < result.items.len) {
        // 跳过相同内容，寻找差异
        if (result.items[i].op != .equal) {
            // 找到差异块的开始
            const block_start = if (i >= options.context_lines) i - options.context_lines else 0;
            
            // 找到差异块的结束
            var block_end = i;
            while (block_end < result.items.len and result.items[block_end].op != .equal) {
                block_end += 1;
            }
            // 添加后面的上下文
            block_end = @min(block_end + options.context_lines, result.items.len);
            
            // 计算行号
            var old_line: usize = 1;
            var new_line: usize = 1;
            for (result.items[0..block_start]) |item| {
                switch (item.op) {
                    .equal => {
                        old_line += 1;
                        new_line += 1;
                    },
                    .delete => old_line += 1,
                    .insert => new_line += 1,
                }
            }
            
            // 计算块中的行数
            var old_count: usize = 0;
            var new_count: usize = 0;
            for (result.items[block_start..block_end]) |item| {
                switch (item.op) {
                    .equal => {
                        old_count += 1;
                        new_count += 1;
                    },
                    .delete => old_count += 1,
                    .insert => new_count += 1,
                }
            }
            
            // 输出块头
            if (old_count == 0) {
                try writer.print("@@ -0,0 +{d},{d} @@\n", .{ new_line, new_count });
            } else if (new_count == 0) {
                try writer.print("@@ -{d},{d} +0,0 @@\n", .{ old_line, old_count });
            } else {
                try writer.print("@@ -{d},{d} +{d},{d} @@\n", .{ old_line, old_count, new_line, new_count });
            }
            
            // 输出块内容
            for (result.items[block_start..block_end]) |item| {
                switch (item.op) {
                    .equal => try writer.print(" {s}\n", .{item.text}),
                    .delete => try writer.print("-{s}\n", .{item.text}),
                    .insert => try writer.print("+{s}\n", .{item.text}),
                }
            }
            
            i = block_end;
        } else {
            i += 1;
        }
    }
    
    return output.toOwnedSlice();
}

/// 差异相似度计算（0.0 - 1.0）
pub fn similarity(old_text: []const u8, new_text: []const u8) !f64 {
    const allocator = std.heap.page_allocator;
    var result = try diffLines(allocator, old_text, new_text);
    defer result.deinit();
    
    const total = result.stats.total();
    if (total == 0) return 1.0;
    
    return @as(f64, @floatFromInt(result.stats.unchanged)) / @as(f64, @floatFromInt(total));
}

/// 应用补丁
pub fn applyPatch(allocator: std.mem.Allocator, original: []const u8, patch: []const u8) ![]u8 {
    var output = std.ArrayList(u8).init(allocator);
    var lines = std.mem.splitScalar(u8, original, '\n');
    
    var patch_lines = std.mem.splitScalar(u8, patch, '\n');
    
    // 解析补丁头
    while (patch_lines.next()) |line| {
        if (std.mem.startsWith(u8, line, "@@")) {
            break;
        }
    }
    
    // 应用补丁
    var current_line = lines.next();
    
    while (patch_lines.next()) |line| {
        if (line.len == 0) continue;
        
        const prefix = line[0];
        const content = if (line.len > 1) line[1..] else "";
        
        switch (prefix) {
            ' ' => {
                // 上下文行，保持原样
                if (current_line) |cl| {
                    try output.appendSlice(cl);
                    try output.append('\n');
                    current_line = lines.next();
                }
            },
            '-' => {
                // 删除行，跳过原文件的这一行
                current_line = lines.next();
            },
            '+' => {
                // 新增行
                try output.appendSlice(content);
                try output.append('\n');
            },
            '@' => {
                // 新的块开始，继续处理
            },
            else => {},
        }
    }
    
    // 添加剩余行
    while (current_line) |cl| {
        try output.appendSlice(cl);
        try output.append('\n');
        current_line = lines.next();
    }
    
    return output.toOwnedSlice();
}

// ========== 测试 ==========

test "DiffOp enum values" {
    try std.testing.expectEqual(DiffOp.equal, .equal);
    try std.testing.expectEqual(DiffOp.insert, .insert);
    try std.testing.expectEqual(DiffOp.delete, .delete);
}

test "DiffItem init" {
    const item = DiffItem.init(.insert, "hello");
    try std.testing.expectEqual(DiffOp.insert, item.op);
    try std.testing.expectEqualSlices(u8, "hello", item.text);
}

test "DiffStats total and hasChanges" {
    var stats = DiffStats{ .additions = 5, .deletions = 3, .unchanged = 10 };
    try std.testing.expectEqual(@as(usize, 18), stats.total());
    try std.testing.expect(stats.hasChanges());
    
    stats = DiffStats{};
    try std.testing.expect(!stats.hasChanges());
}

test "diffLines - identical texts" {
    const allocator = std.testing.allocator;
    var result = try diffLines(allocator, "hello\nworld", "hello\nworld");
    defer result.deinit();
    
    try std.testing.expectEqual(@as(usize, 2), result.items.len);
    try std.testing.expectEqual(DiffOp.equal, result.items[0].op);
    try std.testing.expectEqual(DiffOp.equal, result.items[1].op);
    try std.testing.expectEqual(@as(usize, 2), result.stats.unchanged);
}

test "diffLines - empty texts" {
    const allocator = std.testing.allocator;
    
    // 两个空文本
    {
        var result = try diffLines(allocator, "", "");
        defer result.deinit();
        try std.testing.expectEqual(@as(usize, 0), result.items.len);
    }
    
    // 旧文本不为空，新文本为空（删除）
    {
        var result = try diffLines(allocator, "hello\nworld", "");
        defer result.deinit();
        try std.testing.expectEqual(@as(usize, 2), result.items.len);
        try std.testing.expectEqual(DiffOp.delete, result.items[0].op);
        try std.testing.expectEqual(@as(usize, 2), result.stats.deletions);
    }
    
    // 旧文本为空，新文本不为空（添加）
    {
        var result = try diffLines(allocator, "", "hello\nworld");
        defer result.deinit();
        try std.testing.expectEqual(@as(usize, 2), result.items.len);
        try std.testing.expectEqual(DiffOp.insert, result.items[0].op);
        try std.testing.expectEqual(@as(usize, 2), result.stats.additions);
    }
}

test "diffLines - simple changes" {
    const allocator = std.testing.allocator;
    const old_text = "line1\nline2\nline3";
    const new_text = "line1\nmodified\nline3";
    
    var result = try diffLines(allocator, old_text, new_text);
    defer result.deinit();
    
    // 应该有 4 个差异项: equal(line1), delete(line2), insert(modified), equal(line3)
    try std.testing.expect(result.items.len >= 3);
    try std.testing.expectEqual(@as(usize, 1), result.stats.deletions);
    try std.testing.expectEqual(@as(usize, 1), result.stats.additions);
}

test "diffChars - basic" {
    const allocator = std.testing.allocator;
    var result = try diffChars(allocator, "abc", "adc");
    defer result.deinit();
    
    try std.testing.expect(result.items.len >= 3);
    try std.testing.expect(result.stats.hasChanges());
}

test "similarity" {
    const sim = try similarity("hello\nworld\nfoo\nbar", "hello\nworld\nbaz\nqux");
    try std.testing.expect(sim > 0.0 and sim < 1.0);
    
    const identical = try similarity("same", "same");
    try std.testing.expectEqual(@as(f64, 1.0), identical);
    
    const different = try similarity("aaa", "bbb");
    try std.testing.expectEqual(@as(f64, 0.0), different);
}

test "unifiedDiff output" {
    const allocator = std.testing.allocator;
    const old_text = "line1\nline2\nline3\nline4";
    const new_text = "line1\nmodified\nline3\nline4";
    
    const diff = try unifiedDiff(allocator, old_text, new_text, .{
        .old_filename = "old.txt",
        .new_filename = "new.txt",
    });
    defer allocator.free(diff);
    
    try std.testing.expect(std.mem.startsWith(u8, diff, "--- old.txt\n+++ new.txt\n"));
    try std.testing.expect(std.mem.indexOf(u8, diff, "-line2") != null);
    try std.testing.expect(std.mem.indexOf(u8, diff, "+modified") != null);
}

test "splitLines" {
    const allocator = std.testing.allocator;
    const lines = try splitLines(allocator, "a\nb\nc");
    defer allocator.free(lines);
    
    try std.testing.expectEqual(@as(usize, 3), lines.len);
    try std.testing.expectEqualSlices(u8, "a", lines[0]);
    try std.testing.expectEqualSlices(u8, "b", lines[1]);
    try std.testing.expectEqualSlices(u8, "c", lines[2]);
}