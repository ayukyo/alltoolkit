const std = @import("std");
const text_diff = @import("text_diff_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== 文本差异工具性能基准测试 ===\n\n", .{});

    // 生成测试数据
    std.debug.print("生成测试数据...\n", .{});

    // 测试 1: 小文本比较
    {
        std.debug.print("\n1. 小文本 (100 行):\n", .{});
        var old_text = std.ArrayList(u8).init(allocator);
        defer old_text.deinit();
        var new_text = std.ArrayList(u8).init(allocator);
        defer new_text.deinit();

        var i: usize = 0;
        while (i < 100) : (i += 1) {
            try old_text.writer().print("Line {d:0>3}: This is content for testing\n", .{i});
            if (i % 10 == 5) {
                try new_text.writer().print("Line {d:0>3}: MODIFIED content here\n", .{i});
            } else {
                try new_text.writer().print("Line {d:0>3}: This is content for testing\n", .{i});
            }
        }

        var total_ns: i128 = 0;
        const iterations = 100;
        for (0..iterations) |_| {
            const start = std.time.nanoTimestamp();
            var result = try text_diff.diffLines(allocator, old_text.items, new_text.items);
            result.deinit();
            total_ns += std.time.nanoTimestamp() - start;
        }

        const avg_ns = @divTrunc(total_ns, iterations);
        std.debug.print("   平均耗时: {d} 微秒 ({} 次迭代)\n", .{ @divTrunc(avg_ns, 1000), iterations });
    }

    // 测试 2: 中等文本比较
    {
        std.debug.print("\n2. 中等文本 (1,000 行):\n", .{});
        var old_text = std.ArrayList(u8).init(allocator);
        defer old_text.deinit();
        var new_text = std.ArrayList(u8).init(allocator);
        defer new_text.deinit();

        var i: usize = 0;
        while (i < 1000) : (i += 1) {
            try old_text.writer().print("Line {d:0>4}: This is content for testing purposes\n", .{i});
            if (i % 20 == 10) {
                try new_text.writer().print("Line {d:0>4}: CHANGED content here\n", .{i});
            } else {
                try new_text.writer().print("Line {d:0>4}: This is content for testing purposes\n", .{i});
            }
        }

        var total_ns: i128 = 0;
        const iterations = 10;
        for (0..iterations) |_| {
            const start = std.time.nanoTimestamp();
            var result = try text_diff.diffLines(allocator, old_text.items, new_text.items);
            result.deinit();
            total_ns += std.time.nanoTimestamp() - start;
        }

        const avg_ns = @divTrunc(total_ns, iterations);
        std.debug.print("   平均耗时: {d} 毫秒 ({} 次迭代)\n", .{ @divTrunc(avg_ns, 1_000_000), iterations });
    }

    // 测试 3: 大文本比较
    {
        std.debug.print("\n3. 大文本 (5,000 行):\n", .{});
        var old_text = std.ArrayList(u8).init(allocator);
        defer old_text.deinit();
        var new_text = std.ArrayList(u8).init(allocator);
        defer new_text.deinit();

        var i: usize = 0;
        while (i < 5000) : (i += 1) {
            try old_text.writer().print("Line {d:0>5}: This is content for testing purposes and benchmarking\n", .{i});
            if (i % 50 == 25) {
                try new_text.writer().print("Line {d:0>5}: MODIFIED content for benchmarking\n", .{i});
            } else if (i % 100 == 0) {
                // 跳过一些行（删除）
            } else {
                try new_text.writer().print("Line {d:0>5}: This is content for testing purposes and benchmarking\n", .{i});
            }
        }

        const start = std.time.nanoTimestamp();
        var result = try text_diff.diffLines(allocator, old_text.items, new_text.items);
        defer result.deinit();
        const elapsed = std.time.nanoTimestamp() - start;

        std.debug.print("   耗时: {d} 毫秒\n", .{@divTrunc(elapsed, 1_000_000)});
        std.debug.print("   新增: {d} 行, 删除: {d} 行, 未变: {d} 行\n", .{
            result.stats.additions,
            result.stats.deletions,
            result.stats.unchanged,
        });
    }

    // 测试 4: 字符级差异
    {
        std.debug.print("\n4. 字符级差异 (1000 字符):\n", .{});
        var old_text = std.ArrayList(u8).init(allocator);
        defer old_text.deinit();
        var new_text = std.ArrayList(u8).init(allocator);
        defer new_text.deinit();

        var i: usize = 0;
        while (i < 1000) : (i += 1) {
            const c = @as(u8, @intCast('a' + (i % 26)));
            try old_text.append(c);
            if (i % 20 == 10) {
                try new_text.append('X');
            } else {
                try new_text.append(c);
            }
        }

        var total_ns: i128 = 0;
        const iterations = 50;
        for (0..iterations) |_| {
            const start = std.time.nanoTimestamp();
            var result = try text_diff.diffChars(allocator, old_text.items, new_text.items);
            result.deinit();
            total_ns += std.time.nanoTimestamp() - start;
        }

        const avg_ns = @divTrunc(total_ns, iterations);
        std.debug.print("   平均耗时: {d} 微秒 ({} 次迭代)\n", .{ @divTrunc(avg_ns, 1000), iterations });
    }

    // 测试 5: 相似度计算
    {
        std.debug.print("\n5. 相似度计算 (1000 行):\n", .{});
        var text_a = std.ArrayList(u8).init(allocator);
        defer text_a.deinit();
        var text_b = std.ArrayList(u8).init(allocator);
        defer text_b.deinit();

        var i: usize = 0;
        while (i < 1000) : (i += 1) {
            try text_a.writer().print("Line {d}\n", .{i});
            if (i < 800) {
                try text_b.writer().print("Line {d}\n", .{i});
            }
        }

        var total_ns: i128 = 0;
        const iterations = 100;
        for (0..iterations) |_| {
            const start = std.time.nanoTimestamp();
            _ = try text_diff.similarity(text_a.items, text_b.items);
            total_ns += std.time.nanoTimestamp() - start;
        }

        const avg_ns = @divTrunc(total_ns, iterations);
        const sim = try text_diff.similarity(text_a.items, text_b.items);
        std.debug.print("   相似度: {d:.1}%\n", .{sim * 100});
        std.debug.print("   平均耗时: {d} 微秒 ({} 次迭代)\n", .{ @divTrunc(avg_ns, 1000), iterations });
    }

    // 测试 6: 统一差异格式生成
    {
        std.debug.print("\n6. 统一差异格式生成 (500 行):\n", .{});
        var old_text = std.ArrayList(u8).init(allocator);
        defer old_text.deinit();
        var new_text = std.ArrayList(u8).init(allocator);
        defer new_text.deinit();

        var i: usize = 0;
        while (i < 500) : (i += 1) {
            try old_text.writer().print("Line {d:0>3}: Original content\n", .{i});
            if (i % 25 == 0) {
                try new_text.writer().print("Line {d:0>3}: New content\n", .{i});
            } else {
                try new_text.writer().print("Line {d:0>3}: Original content\n", .{i});
            }
        }

        const start = std.time.nanoTimestamp();
        const diff = try text_diff.unifiedDiff(allocator, old_text.items, new_text.items, .{});
        defer allocator.free(diff);
        const elapsed = std.time.nanoTimestamp() - start;

        std.debug.print("   耗时: {d} 微秒\n", .{@divTrunc(elapsed, 1000)});
        std.debug.print("   输出大小: {d} 字节\n", .{diff.len});
    }

    std.debug.print("\n=== 基准测试完成 ===\n", .{});
}