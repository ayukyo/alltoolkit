const std = @import("std");
const RingBuffer = @import("ring-buffer").RingBuffer;

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Ring Buffer 基础示例 ===\n\n", .{});

    // 1. 创建和基本操作
    try stdout.print("1. 创建缓冲区 (容量: 5)\n", .{});
    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    // 2. 推送元素
    try stdout.print("\n2. 推送元素: 10, 20, 30, 40, 50\n", .{});
    try buffer.push(10);
    try buffer.push(20);
    try buffer.push(30);
    try buffer.push(40);
    try buffer.push(50);

    try stdout.print("   长度: {} / 容量: {}\n", .{ buffer.length(), buffer.capacity });
    try stdout.print("   是否已满: {}\n", .{buffer.isFull()});

    // 3. 查看元素
    try stdout.print("\n3. 查看元素 (不移除)\n", .{});
    try stdout.print("   前端元素: {}\n", .{buffer.peek().?});
    try stdout.print("   后端元素: {}\n", .{buffer.peekBack().?});
    try stdout.print("   索引 2: {}\n", .{buffer.peekAt(2).?});

    // 4. 弹出元素
    try stdout.print("\n4. 弹出元素\n", .{});
    try stdout.print("   弹出: {}\n", .{buffer.pop().?});
    try stdout.print("   弹出: {}\n", .{buffer.pop().?});
    try stdout.print("   长度: {}\n", .{buffer.length()});

    // 5. 批量操作
    try stdout.print("\n5. 批量操作\n", .{});
    const new_items = [_]i32{ 60, 70, 80 };
    const pushed = buffer.pushSlice(&new_items);
    try stdout.print("   推送 {} 个元素\n", .{pushed});

    var dest: [3]i32 = undefined;
    const popped = buffer.popSlice(&dest);
    try stdout.print("   弹出 {} 个元素: ", .{popped});
    for (dest[0..popped]) |item| {
        try stdout.print("{} ", .{item});
    }
    try stdout.print("\n", .{});

    // 6. 迭代器
    try stdout.print("\n6. 使用迭代器遍历剩余元素\n", .{});
    var iter = buffer.iterator();
    try stdout.print("   元素: ", .{});
    while (iter.next()) |item| {
        try stdout.print("{} ", .{item});
    }
    try stdout.print("\n", .{});

    // 7. 查找操作
    try stdout.print("\n7. 查找操作\n", .{});
    try buffer.push(100);
    try buffer.push(200);
    try stdout.print("   包含 100: {}\n", .{buffer.contains(100)});
    try stdout.print("   包含 999: {}\n", .{buffer.contains(999)});
    try stdout.print("   索引 200: {}\n", .{buffer.indexOf(200).?});

    // 8. 清空缓冲区
    try stdout.print("\n8. 清空缓冲区\n", .{});
    buffer.clear();
    try stdout.print("   是否为空: {}\n", .{buffer.isEmpty()});
    try stdout.print("   长度: {}\n", .{buffer.length()});

    try stdout.print("\n=== 示例完成 ===\n", .{});
}