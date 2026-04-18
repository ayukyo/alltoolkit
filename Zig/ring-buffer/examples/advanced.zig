const std = @import("std");
const RingBuffer = @import("ring-buffer").RingBuffer;
const BoundedRingBuffer = @import("ring-buffer").BoundedRingBuffer;
const AtomicRingBuffer = @import("ring-buffer").AtomicRingBuffer;

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Ring Buffer 高级示例 ===\n\n", .{});

    // ========================================
    // 示例 1: 日志缓冲区 (覆盖模式)
    // ========================================
    try stdout.print("1. 日志缓冲区 (覆盖最旧日志)\n", .{});
    try stdout.print("-" ++ "-" ** 39 ++ "\n", .{});

    var log_buffer = try RingBuffer([]const u8).init(allocator, 5);
    defer log_buffer.deinit();

    // 模拟日志记录
    const logs = [_][]const u8{
        "[INFO]  系统启动",
        "[INFO]  加载配置",
        "[WARN]  内存使用较高",
        "[ERROR] 连接超时",
        "[INFO]  重连成功",
        "[DEBUG] 检查心跳",
        "[INFO]  处理请求",
    };

    for (logs) |log| {
        const overwritten = log_buffer.pushOverwrite(log);
        if (overwritten) {
            try stdout.print("   覆盖旧日志\n", .{});
        }
        try stdout.print("   {} 保存: {s}\n", .{ log_buffer.length(), log });
    }

    try stdout.print("\n   当前日志 (最近 {} 条):\n", .{log_buffer.length()});
    var iter = log_buffer.iterator();
    while (iter.next()) |log| {
        try stdout.print("   - {s}\n", .{log});
    }

    // ========================================
    // 示例 2: 生产者-消费者模式
    // ========================================
    try stdout.print("\n2. 生产者-消费者模拟\n", .{});
    try stdout.print("-" ** 41 ++ "\n", .{});

    var queue = try RingBuffer(i32).init(allocator, 10);
    defer queue.deinit();

    // 模拟生产
    try stdout.print("   生产者: 添加数据\n", .{});
    for (0..8) |i| {
        try queue.push(@intCast(i * 10));
    }
    try stdout.print("   队列大小: {}/{}\n", .{ queue.length(), queue.capacity });

    // 模拟消费
    try stdout.print("   消费者: 处理数据\n", .{});
    for (0..5) |_| {
        if (queue.pop()) |item| {
            try stdout.print("   - 处理: {}\n", .{item});
        }
    }
    try stdout.print("   剩余: {} 个\n", .{queue.length()});

    // 继续生产
    try stdout.print("   生产者: 添加更多数据\n", .{});
    try queue.push(100);
    try queue.push(110);
    try stdout.print("   队列大小: {}/{}\n", .{ queue.length(), queue.capacity });

    // ========================================
    // 示例 3: 滑动窗口平均值
    // ========================================
    try stdout.print("\n3. 滑动窗口平均值计算\n", .{});
    try stdout.print("-" ** 41 ++ "\n", .{});

    var window = try RingBuffer(f64).init(allocator, 5);
    defer window.deinit();

    const data = [_]f64{ 10.0, 12.0, 15.0, 11.0, 9.0, 14.0, 16.0, 13.0 };
    try stdout.print("   数据: ", .{});
    for (data) |d| try stdout.print("{:.0} ", .{d});
    try stdout.print("\n", .{});

    for (data) |value| {
        _ = window.pushOverwrite(value);

        var sum: f64 = 0;
        var count: usize = 0;
        var win_iter = window.iterator();
        while (win_iter.next()) |v| {
            sum += v;
            count += 1;
        }
        const avg = sum / @as(f64, @floatFromInt(count));
        try stdout.print("   添加 {:.0} -> 窗口平均值: {:.2}\n", .{ value, avg });
    }

    // ========================================
    // 示例 4: 可扩展缓冲区
    // ========================================
    try stdout.print("\n4. 可扩展缓冲区 (BoundedRingBuffer)\n", .{});
    try stdout.print("-" ** 41 ++ "\n", .{});

    var bounded = try BoundedRingBuffer(i32).init(allocator, 2, 8);
    defer bounded.deinit();

    try stdout.print("   初始容量: 2, 最大容量: 8\n", .{});
    try stdout.print("   添加: 1, 2\n", .{});
    try bounded.push(1);
    try bounded.push(2);
    try stdout.print("   当前大小: {}, 是否已满: {}\n", .{ bounded.length(), bounded.isFull() });

    try stdout.print("   添加: 3 (自动扩容)\n", .{});
    try bounded.push(3);
    try stdout.print("   当前大小: {}\n", .{bounded.length()});

    try stdout.print("   弹出: {}\n", .{bounded.pop().?});
    try stdout.print("   弹出: {}\n", .{bounded.pop().?});
    try stdout.print("   弹出: {}\n", .{bounded.pop().?});

    // ========================================
    // 示例 5: 线程安全缓冲区
    // ========================================
    try stdout.print("\n5. 线程安全缓冲区 (AtomicRingBuffer)\n", .{});
    try stdout.print("-" ** 41 ++ "\n", .{});

    var atomic_buffer = try AtomicRingBuffer(i32).init(allocator, 100);
    defer atomic_buffer.deinit();

    try stdout.print("   在主线程中测试基本操作:\n", .{});
    try atomic_buffer.push(42);
    try atomic_buffer.push(84);
    try atomic_buffer.push(126);

    try stdout.print("   大小: {}\n", .{atomic_buffer.length()});
    try stdout.print("   弹出: {}\n", .{atomic_buffer.pop().?});
    try stdout.print("   弹出: {}\n", .{atomic_buffer.pop().?});
    try stdout.print("   弹出: {}\n", .{atomic_buffer.pop().?});
    try stdout.print("   是否为空: {}\n", .{atomic_buffer.isEmpty()});

    // ========================================
    // 示例 6: 命令历史记录
    // ========================================
    try stdout.print("\n6. 命令历史记录器\n", .{});
    try stdout.print("-" ** 41 ++ "\n", .{});

    var history = try RingBuffer([]const u8).init(allocator, 5);
    defer history.deinit();

    const commands = [_][]const u8{
        "ls -la",
        "cd /home",
        "grep pattern file.txt",
        "cat README.md",
        "make build",
        "make test",
        "git status",
    };

    for (commands) |cmd| {
        _ = history.pushOverwrite(cmd);
    }

    try stdout.print("   最近 {} 条命令:\n", .{history.length()});
    var i: usize = 1;
    var h_iter = history.iterator();
    while (h_iter.next()) |cmd| {
        try stdout.print("   {}. {s}\n", .{ i, cmd });
        i += 1;
    }

    // ========================================
    // 示例 7: 使用 asSlices 进行零拷贝访问
    // ========================================
    try stdout.print("\n7. 零拷贝切片访问 (asSlices)\n", .{});
    try stdout.print("-" ** 41 ++ "\n", .{});

    var slice_buffer = try RingBuffer(i32).init(allocator, 10);
    defer slice_buffer.deinit();

    for (0..7) |idx| {
        try slice_buffer.push(@intCast(idx + 1));
    }

    const slices = slice_buffer.asSlices();
    try stdout.print("   第一个切片: ", .{});
    for (slices[0]) |v| try stdout.print("{} ", .{v});
    try stdout.print("\n   第二个切片: ", .{});
    for (slices[1]) |v| try stdout.print("{} ", .{v});
    try stdout.print("\n", .{});

    try stdout.print("\n=== 高级示例完成 ===\n", .{});
}