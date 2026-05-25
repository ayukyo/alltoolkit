const std = @import("std");

/// Bandwidth unit types (in bits per second)
pub const BandwidthUnit = enum(u8) {
    bps, // bits per second
    Kbps, // kilobits per second (1000 bps)
    Mbps, // megabits per second (1000 Kbps)
    Gbps, // gigabits per second (1000 Mbps)
    Tbps, // terabits per second (1000 Gbps)
    Bps, // bytes per second
    KBps, // kilobytes per second (1000 Bps)
    MBps, // megabytes per second (1000 KBps)
    GBps, // gigabytes per second (1000 MBps)
    TBps, // terabytes per second (1000 GBps)
};

/// Data size unit types
pub const DataUnit = enum(u8) {
    bit,
    Kbit,
    Mbit,
    Gbit,
    Tbit,
    Byte,
    KB,
    MB,
    GB,
    TB,
    PB,
    EB,
};

/// Time unit types
pub const TimeUnit = enum(u8) {
    milliseconds,
    seconds,
    minutes,
    hours,
    days,
};

/// Lowercase a string
fn toLowerAlloc(allocator: std.mem.Allocator, input: []const u8) ![]u8 {
    const result = try allocator.alloc(u8, input.len);
    for (input, 0..) |c, i| {
        result[i] = if (c >= 'A' and c <= 'Z') c - 'A' + 'a' else c;
    }
    return result;
}

/// Bandwidth value with unit
pub const Bandwidth = struct {
    value: f64,
    unit: BandwidthUnit,

    /// Create a new bandwidth value
    pub fn init(value: f64, unit: BandwidthUnit) Bandwidth {
        return .{ .value = value, .unit = unit };
    }

    /// Convert to bits per second
    pub fn toBps(self: Bandwidth) f64 {
        return switch (self.unit) {
            .bps => self.value,
            .Kbps => self.value * 1000.0,
            .Mbps => self.value * 1_000_000.0,
            .Gbps => self.value * 1_000_000_000.0,
            .Tbps => self.value * 1_000_000_000_000.0,
            .Bps => self.value * 8.0,
            .KBps => self.value * 8_000.0,
            .MBps => self.value * 8_000_000.0,
            .GBps => self.value * 8_000_000_000.0,
            .TBps => self.value * 8_000_000_000_000.0,
        };
    }

    /// Convert to any unit
    pub fn to(self: Bandwidth, target_unit: BandwidthUnit) Bandwidth {
        const bps = self.toBps();
        const value = switch (target_unit) {
            .bps => bps,
            .Kbps => bps / 1000.0,
            .Mbps => bps / 1_000_000.0,
            .Gbps => bps / 1_000_000_000.0,
            .Tbps => bps / 1_000_000_000_000.0,
            .Bps => bps / 8.0,
            .KBps => bps / 8_000.0,
            .MBps => bps / 8_000_000.0,
            .GBps => bps / 8_000_000_000.0,
            .TBps => bps / 8_000_000_000_000.0,
        };
        return .{ .value = value, .unit = target_unit };
    }

    /// Format bandwidth to string with precision 2
    pub fn format2(self: Bandwidth, allocator: std.mem.Allocator) ![]u8 {
        var buf: [64]u8 = undefined;
        const unit_str = switch (self.unit) {
            .bps => "bps",
            .Kbps => "Kbps",
            .Mbps => "Mbps",
            .Gbps => "Gbps",
            .Tbps => "Tbps",
            .Bps => "B/s",
            .KBps => "KB/s",
            .MBps => "MB/s",
            .GBps => "GB/s",
            .TBps => "TB/s",
        };
        const formatted = try std.fmt.bufPrint(&buf, "{d:.2} {s}", .{ self.value, unit_str });
        return allocator.dupe(u8, formatted);
    }
};

/// Data size value with unit
pub const DataSize = struct {
    value: f64,
    unit: DataUnit,

    /// Create a new data size value
    pub fn init(value: f64, unit: DataUnit) DataSize {
        return .{ .value = value, .unit = unit };
    }

    /// Convert to bits
    pub fn toBits(self: DataSize) f64 {
        return switch (self.unit) {
            .bit => self.value,
            .Kbit => self.value * 1000.0,
            .Mbit => self.value * 1_000_000.0,
            .Gbit => self.value * 1_000_000_000.0,
            .Tbit => self.value * 1_000_000_000_000.0,
            .Byte => self.value * 8.0,
            .KB => self.value * 8_000.0,
            .MB => self.value * 8_000_000.0,
            .GB => self.value * 8_000_000_000.0,
            .TB => self.value * 8_000_000_000_000.0,
            .PB => self.value * 8_000_000_000_000_000.0,
            .EB => self.value * 8_000_000_000_000_000_000.0,
        };
    }

    /// Convert to bytes
    pub fn toBytes(self: DataSize) f64 {
        return self.toBits() / 8.0;
    }

    /// Convert to any unit
    pub fn to(self: DataSize, target_unit: DataUnit) DataSize {
        const bits = self.toBits();
        const value = switch (target_unit) {
            .bit => bits,
            .Kbit => bits / 1000.0,
            .Mbit => bits / 1_000_000.0,
            .Gbit => bits / 1_000_000_000.0,
            .Tbit => bits / 1_000_000_000_000.0,
            .Byte => bits / 8.0,
            .KB => bits / 8_000.0,
            .MB => bits / 8_000_000.0,
            .GB => bits / 8_000_000_000.0,
            .TB => bits / 8_000_000_000_000.0,
            .PB => bits / 8_000_000_000_000_000.0,
            .EB => bits / 8_000_000_000_000_000_000.0,
        };
        return .{ .value = value, .unit = target_unit };
    }

    /// Format data size to string with precision 2
    pub fn format2(self: DataSize, allocator: std.mem.Allocator) ![]u8 {
        var buf: [64]u8 = undefined;
        const unit_str = switch (self.unit) {
            .bit => "bits",
            .Kbit => "Kbit",
            .Mbit => "Mbit",
            .Gbit => "Gbit",
            .Tbit => "Tbit",
            .Byte => "bytes",
            .KB => "KB",
            .MB => "MB",
            .GB => "GB",
            .TB => "TB",
            .PB => "PB",
            .EB => "EB",
        };
        const formatted = try std.fmt.bufPrint(&buf, "{d:.2} {s}", .{ self.value, unit_str });
        return allocator.dupe(u8, formatted);
    }
};

/// Time duration value with unit
pub const Duration = struct {
    value: f64,
    unit: TimeUnit,

    /// Create a new duration value
    pub fn init(value: f64, unit: TimeUnit) Duration {
        return .{ .value = value, .unit = unit };
    }

    /// Convert to seconds
    pub fn toSeconds(self: Duration) f64 {
        return switch (self.unit) {
            .milliseconds => self.value / 1000.0,
            .seconds => self.value,
            .minutes => self.value * 60.0,
            .hours => self.value * 3600.0,
            .days => self.value * 86400.0,
        };
    }

    /// Convert to any unit
    pub fn to(self: Duration, target_unit: TimeUnit) Duration {
        const seconds = self.toSeconds();
        const value = switch (target_unit) {
            .milliseconds => seconds * 1000.0,
            .seconds => seconds,
            .minutes => seconds / 60.0,
            .hours => seconds / 3600.0,
            .days => seconds / 86400.0,
        };
        return .{ .value = value, .unit = target_unit };
    }

    /// Format duration to string with precision 2
    pub fn format2(self: Duration, allocator: std.mem.Allocator) ![]u8 {
        var buf: [64]u8 = undefined;
        const unit_str = switch (self.unit) {
            .milliseconds => "ms",
            .seconds => "s",
            .minutes => "min",
            .hours => "h",
            .days => "days",
        };
        const formatted = try std.fmt.bufPrint(&buf, "{d:.2} {s}", .{ self.value, unit_str });
        return allocator.dupe(u8, formatted);
    }
};

/// Calculate transfer time given data size and bandwidth
pub fn calculateTransferTime(data_size: DataSize, bandwidth: Bandwidth) Duration {
    const bits = data_size.toBits();
    const bps = bandwidth.toBps();
    const seconds = bits / bps;
    return Duration.init(seconds, .seconds);
}

/// Calculate required bandwidth for a given data size and time
pub fn calculateRequiredBandwidth(data_size: DataSize, duration: Duration) Bandwidth {
    const bits = data_size.toBits();
    const seconds = duration.toSeconds();
    const bps = bits / seconds;
    return Bandwidth.init(bps, .bps);
}

/// Calculate data size that can be transferred in given time at given bandwidth
pub fn calculateTransferSize(bandwidth: Bandwidth, duration: Duration) DataSize {
    const bps = bandwidth.toBps();
    const seconds = duration.toSeconds();
    const bits = bps * seconds;
    return DataSize.init(bits, .bit);
}

/// Convert bandwidth to human-readable format (auto-select best unit)
pub fn formatBandwidth(bandwidth: Bandwidth, allocator: std.mem.Allocator) ![]u8 {
    const bps = bandwidth.toBps();

    if (bps >= 1_000_000_000_000.0) {
        return (Bandwidth.init(bps / 1_000_000_000_000.0, .Tbps)).format2(allocator);
    } else if (bps >= 1_000_000_000.0) {
        return (Bandwidth.init(bps / 1_000_000_000.0, .Gbps)).format2(allocator);
    } else if (bps >= 1_000_000.0) {
        return (Bandwidth.init(bps / 1_000_000.0, .Mbps)).format2(allocator);
    } else if (bps >= 1000.0) {
        return (Bandwidth.init(bps / 1000.0, .Kbps)).format2(allocator);
    } else {
        return (Bandwidth.init(bps, .bps)).format2(allocator);
    }
}

/// Convert data size to human-readable format (auto-select best unit)
pub fn formatDataSize(data_size: DataSize, allocator: std.mem.Allocator) ![]u8 {
    const bytes = data_size.toBytes();

    if (bytes >= 1_000_000_000_000.0) {
        return (DataSize.init(bytes / 1_000_000_000_000.0, .TB)).format2(allocator);
    } else if (bytes >= 1_000_000_000.0) {
        return (DataSize.init(bytes / 1_000_000_000.0, .GB)).format2(allocator);
    } else if (bytes >= 1_000_000.0) {
        return (DataSize.init(bytes / 1_000_000.0, .MB)).format2(allocator);
    } else if (bytes >= 1000.0) {
        return (DataSize.init(bytes / 1000.0, .KB)).format2(allocator);
    } else {
        return (DataSize.init(bytes, .Byte)).format2(allocator);
    }
}

/// Convert duration to human-readable format (auto-select best unit)
pub fn formatDuration(duration: Duration, allocator: std.mem.Allocator) ![]u8 {
    const seconds = duration.toSeconds();

    if (seconds >= 86400.0) {
        return (Duration.init(seconds / 86400.0, .days)).format2(allocator);
    } else if (seconds >= 3600.0) {
        return (Duration.init(seconds / 3600.0, .hours)).format2(allocator);
    } else if (seconds >= 60.0) {
        return (Duration.init(seconds / 60.0, .minutes)).format2(allocator);
    } else if (seconds >= 1.0) {
        return (Duration.init(seconds, .seconds)).format2(allocator);
    } else {
        return (Duration.init(seconds * 1000.0, .milliseconds)).format2(allocator);
    }
}

/// Parse data size string (e.g., "100MB", "1.5GB", "500KB")
pub fn parseDataSize(input: []const u8) !DataSize {
    var i: usize = 0;

    // Skip leading whitespace
    while (i < input.len and std.ascii.isWhitespace(input[i])) : (i += 1) {}

    // Parse number
    var value: f64 = 0;
    var decimal_found = false;
    var decimal_place: f64 = 0.1;

    while (i < input.len) : (i += 1) {
        const c = input[i];
        if (std.ascii.isDigit(c)) {
            if (decimal_found) {
                value += @as(f64, @floatFromInt(c - '0')) * decimal_place;
                decimal_place *= 0.1;
            } else {
                value = value * 10.0 + @as(f64, @floatFromInt(c - '0'));
            }
        } else if (c == '.' and !decimal_found) {
            decimal_found = true;
        } else {
            break;
        }
    }

    // Skip whitespace
    while (i < input.len and std.ascii.isWhitespace(input[i])) : (i += 1) {}

    // Parse unit
    const unit_part = toLowerAlloc(std.heap.page_allocator, input[i..]) catch return DataSize.init(0, .Byte);
    defer std.heap.page_allocator.free(unit_part);

    const unit: DataUnit = if (std.mem.startsWith(u8, unit_part, "eb"))
        .EB
    else if (std.mem.startsWith(u8, unit_part, "pb"))
        .PB
    else if (std.mem.startsWith(u8, unit_part, "tb"))
        .TB
    else if (std.mem.startsWith(u8, unit_part, "gb"))
        .GB
    else if (std.mem.startsWith(u8, unit_part, "mb"))
        .MB
    else if (std.mem.startsWith(u8, unit_part, "kb"))
        .KB
    else if (std.mem.startsWith(u8, unit_part, "byte") or std.mem.startsWith(u8, unit_part, "b") or unit_part.len == 0)
        .Byte
    else
        return DataSize.init(0, .Byte);

    return DataSize.init(value, unit);
}

/// Parse bandwidth string (e.g., "100Mbps", "1Gbps", "50KB/s")
pub fn parseBandwidth(input: []const u8) !Bandwidth {
    var i: usize = 0;

    // Skip leading whitespace
    while (i < input.len and std.ascii.isWhitespace(input[i])) : (i += 1) {}

    // Parse number
    var value: f64 = 0;
    var decimal_found = false;
    var decimal_place: f64 = 0.1;

    while (i < input.len) : (i += 1) {
        const c = input[i];
        if (std.ascii.isDigit(c)) {
            if (decimal_found) {
                value += @as(f64, @floatFromInt(c - '0')) * decimal_place;
                decimal_place *= 0.1;
            } else {
                value = value * 10.0 + @as(f64, @floatFromInt(c - '0'));
            }
        } else if (c == '.' and !decimal_found) {
            decimal_found = true;
        } else {
            break;
        }
    }

    // Skip whitespace
    while (i < input.len and std.ascii.isWhitespace(input[i])) : (i += 1) {}

    // Parse unit
    const unit_part = toLowerAlloc(std.heap.page_allocator, input[i..]) catch return Bandwidth.init(0, .bps);
    defer std.heap.page_allocator.free(unit_part);

    const unit: BandwidthUnit = if (std.mem.startsWith(u8, unit_part, "tbps"))
        .Tbps
    else if (std.mem.startsWith(u8, unit_part, "gbps"))
        .Gbps
    else if (std.mem.startsWith(u8, unit_part, "mbps"))
        .Mbps
    else if (std.mem.startsWith(u8, unit_part, "kbps"))
        .Kbps
    else if (std.mem.startsWith(u8, unit_part, "tb/s"))
        .TBps
    else if (std.mem.startsWith(u8, unit_part, "gb/s"))
        .GBps
    else if (std.mem.startsWith(u8, unit_part, "mb/s") or std.mem.startsWith(u8, unit_part, "mib/s") or std.mem.startsWith(u8, unit_part, "m/s"))
        .MBps
    else if (std.mem.startsWith(u8, unit_part, "kb/s") or std.mem.startsWith(u8, unit_part, "kib/s") or std.mem.startsWith(u8, unit_part, "k/s"))
        .KBps
    else if (std.mem.startsWith(u8, unit_part, "tb"))
        .TBps
    else if (std.mem.startsWith(u8, unit_part, "gb"))
        .GBps
    else if (std.mem.startsWith(u8, unit_part, "mb"))
        .MBps
    else if (std.mem.startsWith(u8, unit_part, "kb"))
        .KBps
    else if (std.mem.startsWith(u8, unit_part, "byte") or std.mem.startsWith(u8, unit_part, "b/s"))
        .Bps
    else
        .bps;

    return Bandwidth.init(value, unit);
}

// --- Tests ---

test "bandwidth conversion" {
    const bw = Bandwidth.init(100.0, .Mbps);
    try std.testing.expectApproxEqRel(100_000_000.0, bw.toBps(), 1e-10);

    const kbps = bw.to(.Kbps);
    try std.testing.expectApproxEqRel(100_000.0, kbps.value, 1e-10);
    try std.testing.expectEqual(BandwidthUnit.Kbps, kbps.unit);

    const bps = bw.to(.bps);
    try std.testing.expectApproxEqRel(100_000_000.0, bps.value, 1e-10);
}

test "data size conversion" {
    const size = DataSize.init(1.0, .GB);
    try std.testing.expectApproxEqRel(8_000_000_000.0, size.toBits(), 1e-10);

    const mb = size.to(.MB);
    try std.testing.expectApproxEqRel(1000.0, mb.value, 1e-10);

    const bytes = size.toBytes();
    try std.testing.expectApproxEqRel(1_000_000_000.0, bytes, 1e-10);
}

test "duration conversion" {
    const dur = Duration.init(1.0, .hours);
    try std.testing.expectApproxEqRel(3600.0, dur.toSeconds(), 1e-10);

    const min = dur.to(.minutes);
    try std.testing.expectApproxEqRel(60.0, min.value, 1e-10);
}

test "calculate transfer time" {
    // 100MB at 100Mbps should take 8 seconds
    const data_size = DataSize.init(100.0, .MB);
    const bw = Bandwidth.init(100.0, .Mbps);
    const time = calculateTransferTime(data_size, bw);

    try std.testing.expectApproxEqRel(8.0, time.value, 1e-10);
    try std.testing.expectEqual(TimeUnit.seconds, time.unit);
}

test "calculate required bandwidth" {
    // 100MB in 8 seconds should require 100Mbps
    const data_size = DataSize.init(100.0, .MB);
    const duration = Duration.init(8.0, .seconds);
    const bw = calculateRequiredBandwidth(data_size, duration);
    const mbps = bw.to(.Mbps);

    try std.testing.expectApproxEqRel(100.0, mbps.value, 1e-10);
}

test "calculate transfer size" {
    // 100Mbps for 8 seconds = 100MB
    const bw = Bandwidth.init(100.0, .Mbps);
    const duration = Duration.init(8.0, .seconds);
    const size = calculateTransferSize(bw, duration);
    const mb = size.to(.MB);

    try std.testing.expectApproxEqRel(100.0, mb.value, 1e-10);
}

test "format bandwidth" {
    const allocator = std.testing.allocator;

    const bw1 = Bandwidth.init(1500000.0, .bps);
    const str1 = try formatBandwidth(bw1, allocator);
    defer allocator.free(str1);
    try std.testing.expect(std.mem.startsWith(u8, str1, "1.50 Mbps"));

    const bw2 = Bandwidth.init(1500000000.0, .bps);
    const str2 = try formatBandwidth(bw2, allocator);
    defer allocator.free(str2);
    try std.testing.expect(std.mem.startsWith(u8, str2, "1.50 Gbps"));
}

test "format data size" {
    const allocator = std.testing.allocator;

    const size1 = DataSize.init(1500000.0, .Byte);
    const str1 = try formatDataSize(size1, allocator);
    defer allocator.free(str1);
    try std.testing.expect(std.mem.startsWith(u8, str1, "1.50 MB"));

    const size2 = DataSize.init(1500000000.0, .Byte);
    const str2 = try formatDataSize(size2, allocator);
    defer allocator.free(str2);
    try std.testing.expect(std.mem.startsWith(u8, str2, "1.50 GB"));
}

test "format duration" {
    const allocator = std.testing.allocator;

    const dur1 = Duration.init(90.0, .seconds);
    const str1 = try formatDuration(dur1, allocator);
    defer allocator.free(str1);
    try std.testing.expect(std.mem.startsWith(u8, str1, "1.50 min"));

    const dur2 = Duration.init(7200.0, .seconds);
    const str2 = try formatDuration(dur2, allocator);
    defer allocator.free(str2);
    try std.testing.expect(std.mem.startsWith(u8, str2, "2.00 h"));
}

test "parse data size" {
    const size1 = try parseDataSize("100MB");
    try std.testing.expectApproxEqRel(100.0, size1.value, 1e-10);
    try std.testing.expectEqual(DataUnit.MB, size1.unit);

    const size2 = try parseDataSize("1.5GB");
    try std.testing.expectApproxEqRel(1.5, size2.value, 1e-10);
    try std.testing.expectEqual(DataUnit.GB, size2.unit);

    const size3 = try parseDataSize("500KB");
    try std.testing.expectApproxEqRel(500.0, size3.value, 1e-10);
    try std.testing.expectEqual(DataUnit.KB, size3.unit);
}

test "parse bandwidth" {
    const bw1 = try parseBandwidth("100Mbps");
    try std.testing.expectApproxEqRel(100.0, bw1.value, 1e-10);
    try std.testing.expectEqual(BandwidthUnit.Mbps, bw1.unit);

    const bw2 = try parseBandwidth("1.5Gbps");
    try std.testing.expectApproxEqRel(1.5, bw2.value, 1e-10);
    try std.testing.expectEqual(BandwidthUnit.Gbps, bw2.unit);

    const bw3 = try parseBandwidth("50KB/s");
    try std.testing.expectApproxEqRel(50.0, bw3.value, 1e-10);
    try std.testing.expectEqual(BandwidthUnit.KBps, bw3.unit);
}

test "real-world transfer time calculation" {
    const allocator = std.testing.allocator;

    // Download a 4.7GB DVD at 50Mbps
    const dvd_size = DataSize.init(4.7, .GB);
    const connection = Bandwidth.init(50.0, .Mbps);
    const time = calculateTransferTime(dvd_size, connection);

    // Expected: ~12.6 minutes
    const min = time.to(.minutes);
    try std.testing.expect(min.value > 12.0 and min.value < 13.0);

    // Format it
    const formatted = try formatDuration(time, allocator);
    defer allocator.free(formatted);
}

test "bandwidth from download time" {
    // Download 1GB in 2 minutes, calculate required bandwidth
    const size = DataSize.init(1.0, .GB);
    const time = Duration.init(2.0, .minutes);
    const bw = calculateRequiredBandwidth(size, time);
    const mbps = bw.to(.Mbps);

    // Should be around 66.67 Mbps
    try std.testing.expect(mbps.value > 66.0 and mbps.value < 67.0);
}