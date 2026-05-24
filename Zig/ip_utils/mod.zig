const std = @import("std");

/// IPv4 地址结构
pub const IPv4 = struct {
    octets: [4]u8,

    /// 从字符串解析 IPv4 地址
    pub fn parse(str: []const u8) !IPv4 {
        var octets: [4]u8 = undefined;
        var idx: usize = 0;
        var start: usize = 0;

        for (str, 0..) |c, i| {
            if (c == '.') {
                if (idx >= 3) return error.TooManyOctets;
                octets[idx] = try parseOctet(str[start..i]);
                idx += 1;
                start = i + 1;
            }
        }

        if (idx != 3) return error.NotEnoughOctets;
        octets[3] = try parseOctet(str[start..]);

        return IPv4{ .octets = octets };
    }

    /// 转换为 32 位无符号整数
    pub fn toU32(self: IPv4) u32 {
        return (@as(u32, self.octets[0]) << 24) |
            (@as(u32, self.octets[1]) << 16) |
            (@as(u32, self.octets[2]) << 8) |
            @as(u32, self.octets[3]);
    }

    /// 从 32 位无符号整数创建
    pub fn fromU32(value: u32) IPv4 {
        return .{
            .octets = .{
                @truncate(value >> 24),
                @truncate(value >> 16),
                @truncate(value >> 8),
                @truncate(value),
            },
        };
    }

    /// 转换为字符串格式
    pub fn toString(self: IPv4, buf: []u8) []u8 {
        const result = std.fmt.bufPrint(buf, "{}.{}.{}.{}", .{
            self.octets[0],
            self.octets[1],
            self.octets[2],
            self.octets[3],
        }) catch buf[0..0];
        return result;
    }

    /// 检查是否为私有地址
    pub fn isPrivate(self: IPv4) bool {
        // 10.0.0.0/8
        if (self.octets[0] == 10) return true;
        // 172.16.0.0/12
        if (self.octets[0] == 172 and self.octets[1] >= 16 and self.octets[1] <= 31) return true;
        // 192.168.0.0/16
        if (self.octets[0] == 192 and self.octets[1] == 168) return true;
        return false;
    }

    /// 检查是否为回环地址
    pub fn isLoopback(self: IPv4) bool {
        return self.octets[0] == 127;
    }

    /// 检查是否为本地链路地址
    pub fn isLinkLocal(self: IPv4) bool {
        return self.octets[0] == 169 and self.octets[1] == 254;
    }

    /// 检查是否为多播地址
    pub fn isMulticast(self: IPv4) bool {
        return self.octets[0] >= 224 and self.octets[0] <= 239;
    }

    /// 检查是否为广播地址
    pub fn isBroadcast(self: IPv4) bool {
        return self.toU32() == 0xFFFFFFFF;
    }

    /// 检查是否为保留地址
    pub fn isReserved(self: IPv4) bool {
        // 0.0.0.0/8
        if (self.octets[0] == 0) return true;
        // 240.0.0.0/4 (except broadcast)
        if (self.octets[0] >= 240 and self.octets[0] <= 255) return true;
        // 100.64.0.0/10 (CGNAT)
        if (self.octets[0] == 100 and self.octets[1] >= 64 and self.octets[1] <= 127) return true;
        // 192.0.0.0/24
        if (self.octets[0] == 192 and self.octets[1] == 0 and self.octets[2] == 0) return true;
        // 192.0.2.0/24
        if (self.octets[0] == 192 and self.octets[1] == 0 and self.octets[2] == 2) return true;
        // 198.51.100.0/24
        if (self.octets[0] == 198 and self.octets[1] == 51 and self.octets[2] == 100) return true;
        // 203.0.113.0/24
        if (self.octets[0] == 203 and self.octets[1] == 0 and self.octets[2] == 113) return true;
        // 198.18.0.0/15
        if (self.octets[0] == 198 and self.octets[1] >= 18 and self.octets[1] <= 19) return true;
        return false;
    }

    /// 检查是否为公网地址
    pub fn isPublic(self: IPv4) bool {
        return !self.isPrivate() and
            !self.isLoopback() and
            !self.isLinkLocal() and
            !self.isMulticast() and
            !self.isBroadcast() and
            !self.isReserved();
    }

    fn parseOctet(str: []const u8) !u8 {
        if (str.len == 0 or str.len > 3) return error.InvalidOctet;
        var value: u32 = 0;
        for (str) |c| {
            if (c < '0' or c > '9') return error.InvalidOctet;
            value = value * 10 + (c - '0');
        }
        if (value > 255) return error.OctetOutOfRange;
        return @truncate(value);
    }
};

/// 子网掩码
pub const SubnetMask = struct {
    prefix_len: u8, // CIDR 前缀长度 (0-32)

    /// 从 CIDR 前缀长度创建
    pub fn fromPrefix(prefix: u8) !SubnetMask {
        if (prefix > 32) return error.InvalidPrefixLength;
        return .{ .prefix_len = prefix };
    }

    /// 从 IPv4 地址创建（必须是有效的子网掩码）
    pub fn fromIPv4(ip: IPv4) !SubnetMask {
        const value = ip.toU32();
        // 检查是否为连续的 1 后跟连续的 0
        const inverted = ~value;
        if (inverted != 0 and (inverted & (inverted + 1)) != 0) {
            return error.InvalidSubnetMask;
        }
        const prefix: u8 = @intCast(32 - @popCount(inverted));
        return .{ .prefix_len = prefix };
    }

    /// 获取网络掩码（IPv4 格式）
    pub fn toIPv4(self: SubnetMask) IPv4 {
        if (self.prefix_len == 0) {
            return IPv4{ .octets = .{ 0, 0, 0, 0 } };
        }
        const mask = @as(u32, 0xFFFFFFFF) << @intCast(32 - self.prefix_len);
        return IPv4.fromU32(mask);
    }

    /// 获取主机位数
    pub fn hostBits(self: SubnetMask) u8 {
        return 32 - self.prefix_len;
    }

    /// 获取主机数量
    pub fn hostCount(self: SubnetMask) u32 {
        if (self.prefix_len == 32) return 1;
        if (self.prefix_len == 31) return 2; // /31 特殊情况
        return @as(u32, 1) << @intCast(self.hostBits());
    }

    /// 获取可用主机数量（排除网络地址和广播地址）
    pub fn usableHostCount(self: SubnetMask) u32 {
        if (self.prefix_len >= 31) return self.hostCount();
        const count = self.hostCount();
        return if (count > 2) count - 2 else 0;
    }
};

/// 子网信息
pub const Subnet = struct {
    network: IPv4,
    mask: SubnetMask,

    /// 从 CIDR 表示法创建（如 "192.168.1.0/24"）
    pub fn fromCIDR(cidr: []const u8) !Subnet {
        const slash_idx = std.mem.indexOfScalar(u8, cidr, '/') orelse return error.InvalidCIDR;
        const ip_str = cidr[0..slash_idx];
        const prefix_str = cidr[slash_idx + 1 ..];

        const network = try IPv4.parse(ip_str);
        const prefix = try std.fmt.parseInt(u8, prefix_str, 10);
        const mask = try SubnetMask.fromPrefix(prefix);

        return .{ .network = network, .mask = mask };
    }

    /// 从网络地址和子网掩码创建
    pub fn init(network: IPv4, mask: SubnetMask) Subnet {
        return .{ .network = network, .mask = mask };
    }

    /// 获取广播地址
    pub fn broadcastAddress(self: Subnet) IPv4 {
        const network = self.network.toU32();
        const host_mask = @as(u32, 0xFFFFFFFF) >> @intCast(self.mask.prefix_len);
        return IPv4.fromU32(network | host_mask);
    }

    /// 获取第一个可用主机地址
    pub fn firstHost(self: Subnet) ?IPv4 {
        if (self.mask.prefix_len >= 31) return null;
        return IPv4.fromU32(self.network.toU32() + 1);
    }

    /// 获取最后一个可用主机地址
    pub fn lastHost(self: Subnet) ?IPv4 {
        if (self.mask.prefix_len >= 31) return null;
        return IPv4.fromU32(self.broadcastAddress().toU32() - 1);
    }

    /// 检查 IP 是否在子网内
    pub fn contains(self: Subnet, ip: IPv4) bool {
        const mask = self.mask.toIPv4().toU32();
        return (ip.toU32() & mask) == (self.network.toU32() & mask);
    }

    /// 获取子网掩码字符串
    pub fn maskString(self: Subnet, buf: []u8) []u8 {
        return self.mask.toIPv4().toString(buf);
    }
};

/// IP 地址范围
pub const IPRange = struct {
    start: IPv4,
    end: IPv4,

    /// 创建 IP 范围
    pub fn init(start: IPv4, end: IPv4) IPRange {
        return .{ .start = start, .end = end };
    }

    /// 检查 IP 是否在范围内
    pub fn contains(self: IPRange, ip: IPv4) bool {
        const value = ip.toU32();
        return value >= self.start.toU32() and value <= self.end.toU32();
    }

    /// 获取范围内的 IP 数量
    pub fn count(self: IPRange) u32 {
        const start = self.start.toU32();
        const end = self.end.toU32();
        return if (end >= start) end - start + 1 else 0;
    }
};

/// 验证 IPv4 地址字符串
pub fn isValidIPv4(str: []const u8) bool {
    _ = IPv4.parse(str) catch return false;
    return true;
}

/// 验证 CIDR 表示法
pub fn isValidCIDR(cidr: []const u8) bool {
    _ = Subnet.fromCIDR(cidr) catch return false;
    return true;
}

/// 计算两个 IP 之间的距离
pub fn ipDistance(a: IPv4, b: IPv4) i64 {
    const a_val: i64 = @as(i64, a.toU32());
    const b_val: i64 = @as(i64, b.toU32());
    return b_val - a_val;
}

/// 获取下一个 IP 地址
pub fn nextIP(ip: IPv4) ?IPv4 {
    const value = ip.toU32();
    if (value == 0xFFFFFFFF) return null;
    return IPv4.fromU32(value + 1);
}

/// 获取上一个 IP 地址
pub fn prevIP(ip: IPv4) ?IPv4 {
    const value = ip.toU32();
    if (value == 0) return null;
    return IPv4.fromU32(value - 1);
}

// ============================================
// 测试
// ============================================

test "IPv4 parsing" {
    const testing = std.testing;

    // 有效地址
    const ip1 = try IPv4.parse("192.168.1.1");
    try testing.expectEqualSlices(u8, &[_]u8{ 192, 168, 1, 1 }, &ip1.octets);

    const ip2 = try IPv4.parse("0.0.0.0");
    try testing.expectEqualSlices(u8, &[_]u8{ 0, 0, 0, 0 }, &ip2.octets);

    const ip3 = try IPv4.parse("255.255.255.255");
    try testing.expectEqualSlices(u8, &[_]u8{ 255, 255, 255, 255 }, &ip3.octets);

    // 无效地址
    try testing.expectError(error.TooManyOctets, IPv4.parse("1.2.3.4.5"));
    try testing.expectError(error.NotEnoughOctets, IPv4.parse("1.2.3"));
    try testing.expectError(error.OctetOutOfRange, IPv4.parse("256.1.1.1"));
    try testing.expectError(error.InvalidOctet, IPv4.parse("1.2.3.abc"));
}

test "IPv4 to/from u32" {
    const testing = std.testing;

    const ip = try IPv4.parse("192.168.1.100");
    const value = ip.toU32();
    try testing.expectEqual(@as(u32, 0xC0A80164), value);

    const ip2 = IPv4.fromU32(value);
    try testing.expectEqualSlices(u8, &ip.octets, &ip2.octets);
}

test "IPv4 address types" {
    const testing = std.testing;

    // 私有地址
    const private1 = try IPv4.parse("10.0.0.1");
    try testing.expect(private1.isPrivate());

    const private2 = try IPv4.parse("172.16.0.1");
    try testing.expect(private2.isPrivate());

    const private3 = try IPv4.parse("192.168.1.1");
    try testing.expect(private3.isPrivate());

    // 回环地址
    const loopback = try IPv4.parse("127.0.0.1");
    try testing.expect(loopback.isLoopback());

    // 本地链路地址
    const link_local = try IPv4.parse("169.254.1.1");
    try testing.expect(link_local.isLinkLocal());

    // 多播地址
    const multicast = try IPv4.parse("224.0.0.1");
    try testing.expect(multicast.isMulticast());

    // 公网地址
    const public = try IPv4.parse("8.8.8.8");
    try testing.expect(public.isPublic());
}

test "SubnetMask" {
    const testing = std.testing;

    // /24 子网掩码
    const mask24 = try SubnetMask.fromPrefix(24);
    const ip24 = mask24.toIPv4();
    try testing.expectEqualSlices(u8, &[_]u8{ 255, 255, 255, 0 }, &ip24.octets);
    try testing.expectEqual(@as(u32, 254), mask24.usableHostCount());

    // /16 子网掩码
    const mask16 = try SubnetMask.fromPrefix(16);
    const ip16 = mask16.toIPv4();
    try testing.expectEqualSlices(u8, &[_]u8{ 255, 255, 0, 0 }, &ip16.octets);

    // 从 IPv4 创建
    const mask_from_ip = try SubnetMask.fromIPv4(try IPv4.parse("255.255.255.0"));
    try testing.expectEqual(@as(u8, 24), mask_from_ip.prefix_len);
}

test "Subnet" {
    const testing = std.testing;

    // 从 CIDR 创建
    const subnet = try Subnet.fromCIDR("192.168.1.0/24");

    // 检查网络地址
    try testing.expectEqualSlices(u8, &[_]u8{ 192, 168, 1, 0 }, &subnet.network.octets);

    // 检查广播地址
    const broadcast = subnet.broadcastAddress();
    try testing.expectEqualSlices(u8, &[_]u8{ 192, 168, 1, 255 }, &broadcast.octets);

    // 检查 IP 是否在子网内
    const ip_in = try IPv4.parse("192.168.1.100");
    try testing.expect(subnet.contains(ip_in));

    const ip_out = try IPv4.parse("192.168.2.1");
    try testing.expect(!subnet.contains(ip_out));
}

test "IPRange" {
    const testing = std.testing;

    const start = try IPv4.parse("192.168.1.1");
    const end = try IPv4.parse("192.168.1.100");
    const range = IPRange.init(start, end);

    // 检查范围内的 IP
    const ip_in = try IPv4.parse("192.168.1.50");
    try testing.expect(range.contains(ip_in));

    // 检查范围外的 IP
    const ip_out = try IPv4.parse("192.168.1.101");
    try testing.expect(!range.contains(ip_out));

    // 检查数量
    try testing.expectEqual(@as(u32, 100), range.count());
}

test "utility functions" {
    const testing = std.testing;

    // 验证函数
    try testing.expect(isValidIPv4("192.168.1.1"));
    try testing.expect(!isValidIPv4("invalid"));
    try testing.expect(isValidCIDR("192.168.1.0/24"));
    try testing.expect(!isValidCIDR("invalid"));

    // IP 距离
    const a = try IPv4.parse("192.168.1.1");
    const b = try IPv4.parse("192.168.1.10");
    try testing.expectEqual(@as(i64, 9), ipDistance(a, b));

    // 下一个/上一个 IP
    const ip = try IPv4.parse("192.168.1.1");
    const next = nextIP(ip).?;
    try testing.expectEqualSlices(u8, &[_]u8{ 192, 168, 1, 2 }, &next.octets);

    const prev = prevIP(next).?;
    try testing.expectEqualSlices(u8, &ip.octets, &prev.octets);
}