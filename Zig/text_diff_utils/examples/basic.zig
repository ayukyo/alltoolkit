const std = @import("std");
const text_diff = @import("text_diff_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== 文本差异工具示例 ===\n\n", .{});

    // 示例 1: 行级差异比较
    std.debug.print("1. 行级差异比较:\n", .{});
    const old_text = 
        \\第一行
        \\第二行
        \\第三行
        \\第四行
        \\第五行
    ;
    const new_text = 
        \\第一行
        \\修改的第二行
        \\第三行
        \\新增的行
        \\第五行
    ;

    var result = try text_diff.diffLines(allocator, old_text, new_text);
    defer result.deinit();

    std.debug.print("   原文本:\n", .{});
    std.debug.print("   {s}\n", .{old_text});
    std.debug.print("   新文本:\n", .{});
    std.debug.print("   {s}\n", .{new_text});
    std.debug.print("\n   差异结果:\n", .{});

    for (result.items) |item| {
        switch (item.op) {
            .equal => std.debug.print("     = {s}\n", .{item.text}),
            .delete => std.debug.print("     - {s}\n", .{item.text}),
            .insert => std.debug.print("     + {s}\n", .{item.text}),
        }
    }

    std.debug.print("\n   统计信息:\n", .{});
    std.debug.print("     新增: {d} 行\n", .{result.stats.additions});
    std.debug.print("     删除: {d} 行\n", .{result.stats.deletions});
    std.debug.print("     未变: {d} 行\n", .{result.stats.unchanged});

    // 示例 2: 字符级差异比较
    std.debug.print("\n2. 字符级差异比较:\n", .{});
    var char_result = try text_diff.diffChars(allocator, "Hello World", "Hello Zig");
    defer char_result.deinit();

    std.debug.print("   原字符串: 'Hello World'\n", .{});
    std.debug.print("   新字符串: 'Hello Zig'\n", .{});
    std.debug.print("   差异: ", .{});

    for (char_result.items) |item| {
        switch (item.op) {
            .equal => std.debug.print("{s}", .{item.text}),
            .delete => std.debug.print("[-{s}]", .{item.text}),
            .insert => std.debug.print("[+{s}]", .{item.text}),
        }
    }
    std.debug.print("\n", .{});

    // 示例 3: 统一差异格式输出
    std.debug.print("\n3. 统一差异格式 (Unified Diff):\n", .{});
    const unified = try text_diff.unifiedDiff(allocator, old_text, new_text, .{
        .context_lines = 1,
        .old_filename = "original.txt",
        .new_filename = "modified.txt",
    });
    defer allocator.free(unified);

    std.debug.print("{s}", .{unified});

    // 示例 4: 相似度计算
    std.debug.print("4. 相似度计算:\n", .{});
    const text_a = "apple\nbanana\norange\ngrape";
    const text_b = "apple\nbanana\npear\ngrape";

    const sim = try text_diff.similarity(text_a, text_b);
    std.debug.print("   文本A: '{s}'\n", .{text_a});
    std.debug.print("   文本B: '{s}'\n", .{text_b});
    std.debug.print("   相似度: {d:.1}%\n", .{sim * 100});

    // 示例 5: 完全相同的文本
    std.debug.print("\n5. 完全相同的文本:\n", .{});
    var same_result = try text_diff.diffLines(allocator, "abc\ndef", "abc\ndef");
    defer same_result.deinit();

    std.debug.print("   差异项数: {d}\n", .{same_result.items.len});
    std.debug.print("   无变化: {}\n", .{!same_result.stats.hasChanges()});

    // 示例 6: 一边为空
    std.debug.print("\n6. 一边为空的情况:\n", .{});
    var empty_result = try text_diff.diffLines(allocator, "line1\nline2\nline3", "");
    defer empty_result.deinit();

    std.debug.print("   原文本删除到空:\n", .{});
    for (empty_result.items) |item| {
        std.debug.print("     - {s}\n", .{item.text});
    }

    var add_result = try text_diff.diffLines(allocator, "", "new1\nnew2");
    defer add_result.deinit();

    std.debug.print("   从空添加内容:\n", .{});
    for (add_result.items) |item| {
        std.debug.print("     + {s}\n", .{item.text});
    }

    // 示例 7: 大文本差异
    std.debug.print("\n7. 大文本性能测试:\n", .{});
    var old_large = std.ArrayList(u8).init(allocator);
    defer old_large.deinit();
    var new_large = std.ArrayList(u8).init(allocator);
    defer new_large.deinit();

    var i: usize = 0;
    while (i < 100) : (i += 1) {
        try old_large.writer().print("Line {d}: This is some content\n", .{i});
        if (i != 50) {
            try new_large.writer().print("Line {d}: This is some content\n", .{i});
        } else {
            try new_large.writer().print("Line {d}: This is MODIFIED content\n", .{i});
        }
    }

    const timer = std.time.nanoTimestamp();
    var large_result = try text_diff.diffLines(allocator, old_large.items, new_large.items);
    defer large_result.deinit();
    const elapsed = std.time.nanoTimestamp() - timer;

    std.debug.print("   处理 {d} 行文本\n", .{old_large.items.len});
    std.debug.print("   耗时: {d} 微秒\n", .{@divTrunc(elapsed, 1000)});
    std.debug.print("   新增: {d}, 删除: {d}, 未变: {d}\n", .{
        large_result.stats.additions,
        large_result.stats.deletions,
        large_result.stats.unchanged,
    });

    std.debug.print("\n=== 示例完成 ===\n", .{});
}