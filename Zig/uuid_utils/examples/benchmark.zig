const std = @import("std");
const uuid_utils = @import("uuid_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== UUID Utils 性能基准测试 ===\n\n", .{});

    const iterations = [_]usize{ 1000, 10000, 100000 };

    for (iterations) |n| {
        std.debug.print("生成 {d} 个 UUID v4:\n", .{n});

        const start = std.time.nanoTimestamp();
        var i: usize = 0;
        while (i < n) : (i += 1) {
            _ = try uuid_utils.generateV4();
        }
        const end = std.time.nanoTimestamp();

        const elapsed_ns = @as(f64, @floatFromInt(end - start));
        const elapsed_ms = elapsed_ns / 1_000_000.0;
        const per_uuid_ns = elapsed_ns / @as(f64, @floatFromInt(n));

        std.debug.print("  总耗时: {d:.2} ms\n", .{elapsed_ms});
        std.debug.print("  每个 UUID: {d:.2} ns\n", .{per_uuid_ns});
        std.debug.print("  每秒: {d:.0} UUIDs\n\n", .{1_000_000_000.0 / per_uuid_ns});
    }

    // 解析性能测试
    std.debug.print("解析 {d} 个 UUID 字符串:\n", .{100000});
    const test_uuid_str = "550e8400-e29b-41d4-a716-446655440000";

    const parse_start = std.time.nanoTimestamp();
    var j: usize = 0;
    while (j < 100000) : (j += 1) {
        _ = try uuid_utils.UUID.parse(test_uuid_str);
    }
    const parse_end = std.time.nanoTimestamp();

    const parse_elapsed_ns = @as(f64, @floatFromInt(parse_end - parse_start));
    const parse_elapsed_ms = parse_elapsed_ns / 1_000_000.0;
    const per_parse_ns = parse_elapsed_ns / 100000.0;

    std.debug.print("  总耗时: {d:.2} ms\n", .{parse_elapsed_ms});
    std.debug.print("  每次解析: {d:.2} ns\n\n", .{per_parse_ns});

    // toString 性能测试
    std.debug.print("转换为字符串 {d} 次:\n", .{100000});
    const test_uuid = try uuid_utils.UUID.parse(test_uuid_str);

    const to_string_start = std.time.nanoTimestamp();
    var k: usize = 0;
    while (k < 100000) : (k += 1) {
        const s = try test_uuid.toString(allocator);
        allocator.free(s);
    }
    const to_string_end = std.time.nanoTimestamp();

    const to_string_elapsed_ns = @as(f64, @floatFromInt(to_string_end - to_string_start));
    const to_string_elapsed_ms = to_string_elapsed_ns / 1_000_000.0;
    const per_to_string_ns = to_string_elapsed_ns / 100000.0;

    std.debug.print("  总耗时: {d:.2} ms\n", .{to_string_elapsed_ms});
    std.debug.print("  每次转换: {d:.2} ns\n\n", .{per_to_string_ns});

    // toStringInto 性能测试（预分配缓冲区）
    std.debug.print("转换为字符串（预分配缓冲区） {d} 次:\n", .{100000});
    var buffer: [36]u8 = undefined;

    const into_start = std.time.nanoTimestamp();
    var l: usize = 0;
    while (l < 100000) : (l += 1) {
        _ = test_uuid.toStringInto(&buffer);
    }
    const into_end = std.time.nanoTimestamp();

    const into_elapsed_ns = @as(f64, @floatFromInt(into_end - into_start));
    const into_elapsed_ms = into_elapsed_ns / 1_000_000.0;
    const per_into_ns = into_elapsed_ns / 100000.0;

    std.debug.print("  总耗时: {d:.2} ms\n", .{into_elapsed_ms});
    std.debug.print("  每次转换: {d:.2} ns\n\n", .{per_into_ns});

    std.debug.print("=== 基准测试完成 ===\n", .{});
}