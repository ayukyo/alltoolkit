const std = @import("std");
const uuid_utils = @import("uuid_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== UUID Utils 示例 ===\n\n", .{});

    // 生成随机 UUID v4
    std.debug.print("1. 生成 UUID v4:\n", .{});
    const uuid1 = try uuid_utils.generateV4();
    const str1 = try uuid1.toString(allocator);
    defer allocator.free(str1);
    std.debug.print("   UUID: {s}\n", .{str1});
    std.debug.print("   版本: {}\n", .{uuid1.version()});
    std.debug.print("   变体: {}\n", .{uuid1.variant()});
    std.debug.print("   是否为空: {}\n\n", .{uuid1.isNil()});

    // 紧凑格式
    std.debug.print("2. 紧凑格式（无连字符）:\n", .{});
    const compact = try uuid1.toCompactString(allocator);
    defer allocator.free(compact);
    std.debug.print("   紧凑: {s}\n\n", .{compact});

    // 解析 UUID
    std.debug.print("3. 解析 UUID:\n", .{});
    const input = "550e8400-e29b-41d4-a716-446655440000";
    const parsed = try uuid_utils.UUID.parse(input);
    std.debug.print("   输入: {s}\n", .{input});
    std.debug.print("   版本: {}\n", .{parsed.version()});
    std.debug.print("   变体: {}\n\n", .{parsed.variant()});

    // 验证 UUID 格式
    std.debug.print("4. 验证 UUID 格式:\n", .{});
    std.debug.print("   '{s}' 有效: {}\n", .{ input, uuid_utils.isValid(input) });
    std.debug.print("   'invalid-uuid' 有效: {}\n\n", .{uuid_utils.isValid("invalid-uuid")});

    // 空 UUID
    std.debug.print("5. 空 UUID (Nil UUID):\n", .{});
    const nil_uuid = uuid_utils.nil();
    const nil_str = try nil_uuid.toString(allocator);
    defer allocator.free(nil_str);
    std.debug.print("   空 UUID: {s}\n", .{nil_str});
    std.debug.print("   是否为空: {}\n\n", .{nil_uuid.isNil()});

    // UUID 比较
    std.debug.print("6. UUID 比较:\n", .{});
    const uuid2 = try uuid_utils.generateV4();
    const uuid3 = try uuid_utils.UUID.parse(try uuid2.toString(allocator));
    std.debug.print("   uuid2 == uuid2: {}\n", .{uuid2.eql(uuid2)});
    std.debug.print("   uuid2 == uuid3: {}\n", .{uuid2.eql(uuid3)});
    std.debug.print("   uuid1 == uuid2: {}\n\n", .{uuid1.eql(uuid2)});

    // UUID 排序
    std.debug.print("7. UUID 排序:\n", .{});
    const uuid_a = try uuid_utils.UUID.parse("00000000-0000-4000-8000-000000000001");
    const uuid_b = try uuid_utils.UUID.parse("00000000-0000-4000-8000-000000000002");
    std.debug.print("   uuid_a < uuid_b: {}\n\n", .{uuid_a.lessThan(uuid_b)});

    // 生成多个 UUID
    std.debug.print("8. 批量生成 UUID:\n", .{});
    var i: usize = 0;
    while (i < 5) : (i += 1) {
        const uuid = try uuid_utils.generateV4();
        const s = try uuid.toString(allocator);
        defer allocator.free(s);
        std.debug.print("   {d}: {s}\n", .{ i + 1, s });
    }

    // 使用固定种子生成 UUID
    std.debug.print("\n9. 使用固定种子生成 UUID:\n", .{});
    const seeded_uuid1 = uuid_utils.generateV4WithSeed(12345);
    const seeded_uuid2 = uuid_utils.generateV4WithSeed(12345);
    const s1 = try seeded_uuid1.toString(allocator);
    defer allocator.free(s1);
    const s2 = try seeded_uuid2.toString(allocator);
    defer allocator.free(s2);
    std.debug.print("   种子 12345 - 第1次: {s}\n", .{s1});
    std.debug.print("   种子 12345 - 第2次: {s}\n", .{s2});
    std.debug.print("   两者相等: {}\n\n", .{seeded_uuid1.eql(seeded_uuid2)});

    std.debug.print("=== 示例完成 ===\n", .{});
}