const std = @import("std");
const ip_utils = @import("mod.zig");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    var buf: [64]u8 = undefined;

    // ========================================
    // 示例 1: 解析和验证 IPv4 地址
    // ========================================
    try stdout.print("=== IPv4 地址解析与验证 ===\n", .{});

    const addresses = [_][]const u8{
        "192.168.1.1",
        "10.0.0.1",
        "127.0.0.1",
        "169.254.1.1",
        "224.0.0.1",
        "8.8.8.8",
        "255.255.255.255",
    };

    for (addresses) |addr_str| {
        const ip = ip_utils.IPv4.parse(addr_str) catch {
            try stdout.print("{s}: 无效地址\n", .{addr_str});
            continue;
        };

        try stdout.print("{s}:\n", .{addr_str});
        try stdout.print("  私有地址: {}\n", .{ip.isPrivate()});
        try stdout.print("  回环地址: {}\n", .{ip.isLoopback()});
        try stdout.print("  本地链路: {}\n", .{ip.isLinkLocal()});
        try stdout.print("  多播地址: {}\n", .{ip.isMulticast()});
        try stdout.print("  公网地址: {}\n", .{ip.isPublic()});
        try stdout.print("\n", .{});
    }

    // ========================================
    // 示例 2: 子网计算
    // ========================================
    try stdout.print("=== 子网计算 ===\n", .{});

    const cidr_list = [_][]const u8{
        "192.168.1.0/24",
        "10.0.0.0/8",
        "172.16.0.0/12",
    };

    for (cidr_list) |cidr| {
        const subnet = ip_utils.Subnet.fromCIDR(cidr) catch continue;

        try stdout.print("CIDR: {s}\n", .{cidr});

        const mask_str = subnet.maskString(&buf);
        try stdout.print("  子网掩码: {s}\n", .{mask_str});

        const broadcast = subnet.broadcastAddress();
        const bc_str = broadcast.toString(&buf);
        try stdout.print("  广播地址: {s}\n", .{bc_str});

        try stdout.print("  可用主机数: {}\n", .{subnet.mask.usableHostCount()});

        // 检查特定 IP 是否在子网内
        const test_ip = ip_utils.IPv4.parse("192.168.1.100") catch continue;
        try stdout.print("  192.168.1.100 在子网内: {}\n", .{subnet.contains(test_ip)});
        try stdout.print("\n", .{});
    }

    // ========================================
    // 示例 3: IP 地址转换
    // ========================================
    try stdout.print("=== IP 地址转换 ===\n", .{});

    const ip = try ip_utils.IPv4.parse("192.168.1.100");
    try stdout.print("IP: 192.168.1.100\n", .{});

    // 转换为 32 位整数
    const ip_value = ip.toU32();
    try stdout.print("  32位整数值: {} (0x{X})\n", .{ ip_value, ip_value });

    // 从 32 位整数转换回来
    const ip_back = ip_utils.IPv4.fromU32(ip_value);
    const ip_str = ip_back.toString(&buf);
    try stdout.print("  转换回来: {s}\n", .{ip_str});

    // ========================================
    // 示例 4: IP 范围
    // ========================================
    try stdout.print("\n=== IP 范围 ===\n", .{});

    const start = try ip_utils.IPv4.parse("192.168.1.1");
    const end = try ip_utils.IPv4.parse("192.168.1.100");
    const range = ip_utils.IPRange.init(start, end);

    try stdout.print("范围: 192.168.1.1 - 192.168.1.100\n", .{});
    try stdout.print("  IP 数量: {}\n", .{range.count()});

    // 检查 IP 是否在范围内
    const test1 = try ip_utils.IPv4.parse("192.168.1.50");
    try stdout.print("  192.168.1.50 在范围内: {}\n", .{range.contains(test1)});

    const test2 = try ip_utils.IPv4.parse("192.168.1.200");
    try stdout.print("  192.168.1.200 在范围内: {}\n", .{range.contains(test2)});

    // ========================================
    // 示例 5: IP 遍历
    // ========================================
    try stdout.print("\n=== IP 遍历 ===\n", .{});

    var current = try ip_utils.IPv4.parse("192.168.1.1");
    try stdout.print("前 5 个 IP:\n", .{});

    var i: u32 = 0;
    while (i < 5) : (i += 1) {
        const str = current.toString(&buf);
        try stdout.print("  {s}\n", .{str});
        current = ip_utils.nextIP(current) orelse break;
    }

    // ========================================
    // 示例 6: 验证函数
    // ========================================
    try stdout.print("\n=== 验证函数 ===\n", .{});

    const test_addresses = [_][]const u8{
        "192.168.1.1",
        "256.1.1.1",
        "1.2.3",
        "abc.def.ghi.jkl",
    };

    for (test_addresses) |addr| {
        const valid = ip_utils.isValidIPv4(addr);
        try stdout.print("  {s}: {}\n", .{ addr, valid });
    }

    try stdout.print("\nCIDR 验证:\n", .{});
    const test_cidrs = [_][]const u8{
        "192.168.1.0/24",
        "10.0.0.0/33", // 无效前缀
        "invalid",
    };

    for (test_cidrs) |cidr| {
        const valid = ip_utils.isValidCIDR(cidr);
        try stdout.print("  {s}: {}\n", .{ cidr, valid });
    }
}