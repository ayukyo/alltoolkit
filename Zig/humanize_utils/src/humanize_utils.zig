const std = @import("std");

/// Humanize operation errors
pub const HumanizeError = error{
    OutOfMemory,
    BufferTooSmall,
    InvalidFormat,
    InvalidValue,
};

// ============================================================================
// File Size Formatting
// ============================================================================

/// Binary units (KiB, MiB, etc.)
const BINARY_UNITS: [9][]const u8 = .{ "B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB" };

/// Decimal units (KB, MB, etc.)
const DECIMAL_UNITS: [9][]const u8 = .{ "B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB" };

/// Format bytes to human-readable size
pub fn formatBytes(
    allocator: std.mem.Allocator,
    size: usize,
    precision: u8,
    binary: bool,
) HumanizeError![]u8 {
    if (size == 0) {
        return allocator.dupe(u8, "0 B");
    }

    const units = if (binary) BINARY_UNITS else DECIMAL_UNITS;
    const base: f64 = if (binary) 1024.0 else 1000.0;

    const size_f: f64 = @floatFromInt(size);
    
    if (size_f < base) {
        var buf: [32]u8 = undefined;
        const len = std.fmt.formatIntBuf(&buf, size, 10, .lower, .{});
        const result = allocator.alloc(u8, len + 2) catch return HumanizeError.OutOfMemory;
        @memcpy(result[0..len], buf[0..len]);
        result[len] = ' ';
        result[len + 1] = 'B';
        return result[0 .. len + 2];
    }

    // Calculate unit index
    var unit_index: usize = 0;
    var size_in_unit: f64 = size_f;
    
    while (size_in_unit >= base and unit_index < units.len - 1) {
        size_in_unit /= base;
        unit_index += 1;
    }

    // Format with fixed precision based on precision parameter
    var buf: [64]u8 = undefined;
    const result_slice = switch (precision) {
        0 => std.fmt.bufPrint(&buf, "{d:.0} {s}", .{ size_in_unit, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        1 => std.fmt.bufPrint(&buf, "{d:.1} {s}", .{ size_in_unit, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        2 => std.fmt.bufPrint(&buf, "{d:.2} {s}", .{ size_in_unit, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        3 => std.fmt.bufPrint(&buf, "{d:.3} {s}", .{ size_in_unit, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        else => std.fmt.bufPrint(&buf, "{d:.2} {s}", .{ size_in_unit, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
    };
    return allocator.dupe(u8, result_slice);
}

/// Parse size string to bytes
pub fn parseSize(size_str: []const u8) HumanizeError!usize {
    var str = size_str;
    
    // Trim whitespace
    while (str.len > 0 and str[0] == ' ') str = str[1..];
    while (str.len > 0 and str[str.len - 1] == ' ') str = str[0 .. str.len - 1];

    // Find where the number ends
    var num_end: usize = 0;
    for (str, 0..) |c, i| {
        if (c == '.' or (c >= '0' and c <= '9')) {
            num_end = i + 1;
        } else {
            break;
        }
    }

    if (num_end == 0) return HumanizeError.InvalidFormat;

    const num_str = str[0..num_end];
    const unit_str = if (num_end < str.len) str[num_end..] else "B";

    // Parse the number
    const num: f64 = std.fmt.parseFloat(f64, num_str) catch return HumanizeError.InvalidFormat;

    // Get multiplier based on unit
    const multiplier = getUnitMultiplier(unit_str);
    
    return @intFromFloat(@round(num * multiplier));
}

fn getUnitMultiplier(unit: []const u8) f64 {
    var u = unit;
    
    // Trim whitespace
    while (u.len > 0 and u[0] == ' ') u = u[1..];

    // Check units (case-insensitive comparison)
    if (std.mem.eql(u8, u, "B") or std.mem.eql(u8, u, "b")) return 1.0;
    
    // Binary units
    if (std.mem.eql(u8, u, "KiB") or std.mem.eql(u8, u, "KIB") or std.mem.eql(u8, u, "kib")) return 1024.0;
    if (std.mem.eql(u8, u, "MiB") or std.mem.eql(u8, u, "MIB") or std.mem.eql(u8, u, "mib")) return 1024.0 * 1024.0;
    if (std.mem.eql(u8, u, "GiB") or std.mem.eql(u8, u, "GIB") or std.mem.eql(u8, u, "gib")) return 1024.0 * 1024.0 * 1024.0;
    if (std.mem.eql(u8, u, "TiB") or std.mem.eql(u8, u, "TIB") or std.mem.eql(u8, u, "tib")) return 1024.0 * 1024.0 * 1024.0 * 1024.0;
    if (std.mem.eql(u8, u, "PiB") or std.mem.eql(u8, u, "PIB") or std.mem.eql(u8, u, "pib")) return 1024.0 * 1024.0 * 1024.0 * 1024.0 * 1024.0;
    
    // Decimal units (accept both K and KB)
    if (std.mem.eql(u8, u, "K") or std.mem.eql(u8, u, "k") or std.mem.eql(u8, u, "KB") or std.mem.eql(u8, u, "kb")) return 1000.0;
    if (std.mem.eql(u8, u, "M") or std.mem.eql(u8, u, "m") or std.mem.eql(u8, u, "MB") or std.mem.eql(u8, u, "mb")) return 1000.0 * 1000.0;
    if (std.mem.eql(u8, u, "G") or std.mem.eql(u8, u, "g") or std.mem.eql(u8, u, "GB") or std.mem.eql(u8, u, "gb")) return 1000.0 * 1000.0 * 1000.0;
    if (std.mem.eql(u8, u, "T") or std.mem.eql(u8, u, "t") or std.mem.eql(u8, u, "TB") or std.mem.eql(u8, u, "tb")) return 1000.0 * 1000.0 * 1000.0 * 1000.0;
    if (std.mem.eql(u8, u, "P") or std.mem.eql(u8, u, "p") or std.mem.eql(u8, u, "PB") or std.mem.eql(u8, u, "pb")) return 1000.0 * 1000.0 * 1000.0 * 1000.0 * 1000.0;

    return 1.0;
}

// ============================================================================
// Duration Formatting
// ============================================================================

/// Duration format type
pub const DurationFormat = enum {
    full,       // HH:MM:SS
    compact,    // 1h30m45s
    text,       // 1 hour 30 minutes
    text_cn,    // 1小时30分钟
};

/// Format duration in seconds to human-readable string
pub fn formatDuration(
    allocator: std.mem.Allocator,
    seconds: u64,
    format: DurationFormat,
) HumanizeError![]u8 {
    const hours = seconds / 3600;
    const minutes = (seconds % 3600) / 60;
    const secs = seconds % 60;

    var buf: [128]u8 = undefined;
    
    switch (format) {
        .full => {
            const result_slice = std.fmt.bufPrint(&buf, "{:0>2}:{:0>2}:{:0>2}", .{ hours, minutes, secs }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        },
        .compact => {
            var pos: usize = 0;
            if (hours > 0) {
                const slice = std.fmt.bufPrint(buf[pos..], "{}h", .{hours}) catch return HumanizeError.BufferTooSmall;
                pos += slice.len;
            }
            if (minutes > 0 or hours > 0) {
                const slice = std.fmt.bufPrint(buf[pos..], "{}m", .{minutes}) catch return HumanizeError.BufferTooSmall;
                pos += slice.len;
            }
            const slice = std.fmt.bufPrint(buf[pos..], "{}s", .{secs}) catch return HumanizeError.BufferTooSmall;
            pos += slice.len;
            return allocator.dupe(u8, buf[0..pos]);
        },
        .text => {
            var pos: usize = 0;
            if (hours > 0) {
                if (hours > 1) {
                    const slice = std.fmt.bufPrint(buf[pos..], "{} hours", .{hours}) catch return HumanizeError.BufferTooSmall;
                    pos += slice.len;
                } else {
                    const slice = std.fmt.bufPrint(buf[pos..], "{} hour", .{hours}) catch return HumanizeError.BufferTooSmall;
                    pos += slice.len;
                }
                if (minutes > 0 or secs > 0) {
                    buf[pos] = ' ';
                    pos += 1;
                }
            }
            if (minutes > 0) {
                if (minutes > 1) {
                    const slice = std.fmt.bufPrint(buf[pos..], "{} minutes", .{minutes}) catch return HumanizeError.BufferTooSmall;
                    pos += slice.len;
                } else {
                    const slice = std.fmt.bufPrint(buf[pos..], "{} minute", .{minutes}) catch return HumanizeError.BufferTooSmall;
                    pos += slice.len;
                }
                if (secs > 0) {
                    buf[pos] = ' ';
                    pos += 1;
                }
            }
            if (secs > 0 or (hours == 0 and minutes == 0)) {
                if (secs > 1) {
                    const slice = std.fmt.bufPrint(buf[pos..], "{} seconds", .{secs}) catch return HumanizeError.BufferTooSmall;
                    pos += slice.len;
                } else {
                    const slice = std.fmt.bufPrint(buf[pos..], "{} second", .{secs}) catch return HumanizeError.BufferTooSmall;
                    pos += slice.len;
                }
            }
            return allocator.dupe(u8, buf[0..pos]);
        },
        .text_cn => {
            var pos: usize = 0;
            if (hours > 0) {
                const slice = std.fmt.bufPrint(buf[pos..], "{}小时", .{hours}) catch return HumanizeError.BufferTooSmall;
                pos += slice.len;
            }
            if (minutes > 0) {
                const slice = std.fmt.bufPrint(buf[pos..], "{}分钟", .{minutes}) catch return HumanizeError.BufferTooSmall;
                pos += slice.len;
            }
            if (secs > 0 or (hours == 0 and minutes == 0)) {
                const slice = std.fmt.bufPrint(buf[pos..], "{}秒", .{secs}) catch return HumanizeError.BufferTooSmall;
                pos += slice.len;
            }
            return allocator.dupe(u8, buf[0..pos]);
        },
    }
}

// ============================================================================
// Number Formatting
// ============================================================================

/// Format number with thousands separators
pub fn formatWithCommas(
    allocator: std.mem.Allocator,
    number: i64,
) HumanizeError![]u8 {
    if (number == 0) {
        return allocator.dupe(u8, "0");
    }

    const abs_num: u64 = @intCast(if (number < 0) @as(u64, @intCast(-number)) else @as(u64, @intCast(number)));
    
    // Count digits
    const digits: usize = blk: {
        var count: usize = 0;
        var n = abs_num;
        while (n > 0) {
            count += 1;
            n /= 10;
        }
        break :blk count;
    };

    // Calculate output size (digits + commas + possible minus sign)
    const commas: usize = if (digits > 3) (digits - 1) / 3 else 0;
    const output_size: usize = digits + commas + (if (number < 0) @as(usize, 1) else @as(usize, 0));
    
    const output = allocator.alloc(u8, output_size) catch return HumanizeError.OutOfMemory;
    var out_pos: usize = 0;

    // Add minus sign if negative
    if (number < 0) {
        output[out_pos] = '-';
        out_pos += 1;
    }

    // Build from left to right with commas
    // First group may have 1, 2, or 3 digits (or 3 if total digits divisible by 3)
    const first_group_size: usize = if (digits % 3 == 0) 3 else digits % 3;
    var remaining_digits: usize = digits - first_group_size;
    
    // Calculate divisor to extract first group
    var divisor: u64 = 1;
    {
        var count: usize = 0;
        while (count < remaining_digits) {
            divisor *= 10;
            count += 1;
        }
    }
    
    var remaining = abs_num;
    
    // Write first group
    var buf: [32]u8 = undefined;
    const first_group = remaining / divisor;
    remaining = remaining % divisor;
    const first_len = std.fmt.formatIntBuf(&buf, first_group, 10, .lower, .{});
    @memcpy(output[out_pos .. out_pos + first_len], buf[0..first_len]);
    out_pos += first_len;
    
    // Write remaining groups (each exactly 3 digits) with commas
    while (remaining_digits > 0) {
        output[out_pos] = ',';
        out_pos += 1;
        
        // Calculate divisor for 3 digits based on remaining digits
        divisor = 1;
        {
            var count: usize = 0;
            while (count < remaining_digits - 3) {
                divisor *= 10;
                count += 1;
            }
        }
        remaining_digits -= 3;
        
        const group = remaining / divisor;
        remaining = remaining % divisor;
        
        // Write 3 digits with leading zeros
        const len = std.fmt.formatIntBuf(&buf, group, 10, .lower, .{ .width = 3, .fill = '0' });
        @memcpy(output[out_pos .. out_pos + len], buf[0..len]);
        out_pos += len;
    }
    
    return output[0..out_pos];
}

/// Format large numbers with abbreviations (K, M, B, T)
pub fn formatNumberCompact(
    allocator: std.mem.Allocator,
    number: i64,
    precision: u8,
) HumanizeError![]u8 {
    if (number == 0) {
        return allocator.dupe(u8, "0");
    }

    const abs_num: f64 = @floatFromInt(if (number < 0) -number else number);
    const sign_prefix: []const u8 = if (number < 0) "-" else "";

    const units: [6][]const u8 = .{ "", "K", "M", "B", "T", "Q" };
    var unit_index: usize = 0;
    var value: f64 = abs_num;

    while (value >= 1000.0 and unit_index < units.len - 1) {
        value /= 1000.0;
        unit_index += 1;
    }

    var buf: [64]u8 = undefined;
    
    if (unit_index == 0) {
        const int_val: i64 = @intFromFloat(@round(value));
        const result_slice = std.fmt.bufPrint(&buf, "{s}{d}", .{ sign_prefix, int_val }) catch return HumanizeError.BufferTooSmall;
        return allocator.dupe(u8, result_slice);
    }

    // Use fixed precision based on parameter
    const result_slice = switch (precision) {
        0 => std.fmt.bufPrint(&buf, "{s}{d:.0} {s}", .{ sign_prefix, value, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        1 => std.fmt.bufPrint(&buf, "{s}{d:.1} {s}", .{ sign_prefix, value, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        2 => std.fmt.bufPrint(&buf, "{s}{d:.2} {s}", .{ sign_prefix, value, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
        else => std.fmt.bufPrint(&buf, "{s}{d:.1} {s}", .{ sign_prefix, value, units[unit_index] }) catch return HumanizeError.BufferTooSmall,
    };
    return allocator.dupe(u8, result_slice);
}

/// Format percentage
pub fn formatPercentage(
    allocator: std.mem.Allocator,
    value: f64,
    precision: u8,
    show_sign: bool,
) HumanizeError![]u8 {
    var buf: [32]u8 = undefined;
    
    const percent = if (value >= -1.0 and value <= 1.0) value * 100.0 else value;
    
    // Use fixed precision based on parameter
    if (show_sign and percent > 0) {
        const result_slice = switch (precision) {
            0 => std.fmt.bufPrint(&buf, "+{d:.0}%", .{percent}) catch return HumanizeError.BufferTooSmall,
            1 => std.fmt.bufPrint(&buf, "+{d:.1}%", .{percent}) catch return HumanizeError.BufferTooSmall,
            2 => std.fmt.bufPrint(&buf, "+{d:.2}%", .{percent}) catch return HumanizeError.BufferTooSmall,
            else => std.fmt.bufPrint(&buf, "+{d:.1}%", .{percent}) catch return HumanizeError.BufferTooSmall,
        };
        return allocator.dupe(u8, result_slice);
    } else {
        const result_slice = switch (precision) {
            0 => std.fmt.bufPrint(&buf, "{d:.0}%", .{percent}) catch return HumanizeError.BufferTooSmall,
            1 => std.fmt.bufPrint(&buf, "{d:.1}%", .{percent}) catch return HumanizeError.BufferTooSmall,
            2 => std.fmt.bufPrint(&buf, "{d:.2}%", .{percent}) catch return HumanizeError.BufferTooSmall,
            else => std.fmt.bufPrint(&buf, "{d:.1}%", .{percent}) catch return HumanizeError.BufferTooSmall,
        };
        return allocator.dupe(u8, result_slice);
    }
}

// ============================================================================
// Relative Time Formatting
// ============================================================================

/// Format relative time (time ago)
pub fn formatRelativeTime(
    allocator: std.mem.Allocator,
    seconds_ago: u64,
    use_chinese: bool,
) HumanizeError![]u8 {
    var buf: [64]u8 = undefined;

    const suffix: []const u8 = if (use_chinese) "前" else " ago";
    
    if (use_chinese) {
        if (seconds_ago < 60) {
            const result_slice = std.fmt.bufPrint(&buf, "{}秒{s}", .{ seconds_ago, suffix }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        } else if (seconds_ago < 3600) {
            const result_slice = std.fmt.bufPrint(&buf, "{}分钟{s}", .{ seconds_ago / 60, suffix }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        } else if (seconds_ago < 86400) {
            const result_slice = std.fmt.bufPrint(&buf, "{}小时{s}", .{ seconds_ago / 3600, suffix }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        } else if (seconds_ago < 2592000) { // 30 days
            const result_slice = std.fmt.bufPrint(&buf, "{}天{s}", .{ seconds_ago / 86400, suffix }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        } else if (seconds_ago < 31536000) { // 365 days
            const result_slice = std.fmt.bufPrint(&buf, "{}个月{s}", .{ seconds_ago / 2592000, suffix }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        } else {
            const result_slice = std.fmt.bufPrint(&buf, "{}年{s}", .{ seconds_ago / 31536000, suffix }) catch return HumanizeError.BufferTooSmall;
            return allocator.dupe(u8, result_slice);
        }
    } else {
        if (seconds_ago < 60) {
            if (seconds_ago == 1) {
                const result_slice = std.fmt.bufPrint(&buf, "{} second{s}", .{ seconds_ago, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            } else {
                const result_slice = std.fmt.bufPrint(&buf, "{} seconds{s}", .{ seconds_ago, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            }
        } else if (seconds_ago < 3600) {
            const mins = seconds_ago / 60;
            if (mins == 1) {
                const result_slice = std.fmt.bufPrint(&buf, "{} minute{s}", .{ mins, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            } else {
                const result_slice = std.fmt.bufPrint(&buf, "{} minutes{s}", .{ mins, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            }
        } else if (seconds_ago < 86400) {
            const hrs = seconds_ago / 3600;
            if (hrs == 1) {
                const result_slice = std.fmt.bufPrint(&buf, "{} hour{s}", .{ hrs, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            } else {
                const result_slice = std.fmt.bufPrint(&buf, "{} hours{s}", .{ hrs, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            }
        } else if (seconds_ago < 2592000) {
            const days = seconds_ago / 86400;
            if (days == 1) {
                const result_slice = std.fmt.bufPrint(&buf, "{} day{s}", .{ days, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            } else {
                const result_slice = std.fmt.bufPrint(&buf, "{} days{s}", .{ days, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            }
        } else if (seconds_ago < 31536000) {
            const months = seconds_ago / 2592000;
            if (months == 1) {
                const result_slice = std.fmt.bufPrint(&buf, "{} month{s}", .{ months, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            } else {
                const result_slice = std.fmt.bufPrint(&buf, "{} months{s}", .{ months, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            }
        } else {
            const years = seconds_ago / 31536000;
            if (years == 1) {
                const result_slice = std.fmt.bufPrint(&buf, "{} year{s}", .{ years, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            } else {
                const result_slice = std.fmt.bufPrint(&buf, "{} years{s}", .{ years, suffix }) catch return HumanizeError.BufferTooSmall;
                return allocator.dupe(u8, result_slice);
            }
        }
    }
}

// ============================================================================
// Text Formatting
// ============================================================================

/// Truncate text with suffix
pub fn truncateText(
    allocator: std.mem.Allocator,
    text: []const u8,
    max_length: usize,
    suffix: []const u8,
) HumanizeError![]u8 {
    if (text.len <= max_length) {
        return allocator.dupe(u8, text);
    }

    const content_length = max_length - suffix.len;
    if (content_length <= 0) {
        return allocator.dupe(u8, suffix);
    }

    const result = allocator.alloc(u8, max_length) catch return HumanizeError.OutOfMemory;
    @memcpy(result[0..content_length], text[0..content_length]);
    @memcpy(result[content_length..max_length], suffix);
    return result;
}

/// Format ordinal numbers (1st, 2nd, 3rd, etc.)
pub fn formatOrdinal(
    allocator: std.mem.Allocator,
    number: usize,
) HumanizeError![]u8 {
    var buf: [16]u8 = undefined;

    const suffix: []const u8 = if (number % 100 >= 11 and number % 100 <= 13)
        "th"
    else switch (number % 10) {
        1 => "st",
        2 => "nd",
        3 => "rd",
        else => "th",
    };

    const result_slice = std.fmt.bufPrint(&buf, "{}{s}", .{ number, suffix }) catch return HumanizeError.BufferTooSmall;
    return allocator.dupe(u8, result_slice);
}

/// Format ordinal numbers in Chinese (第1, 第2, etc.)
pub fn formatOrdinalChinese(
    allocator: std.mem.Allocator,
    number: usize,
) HumanizeError![]u8 {
    var buf: [16]u8 = undefined;
    const result_slice = std.fmt.bufPrint(&buf, "第{}", .{number}) catch return HumanizeError.BufferTooSmall;
    return allocator.dupe(u8, result_slice);
}

// ============================================================================
// List Formatting
// ============================================================================

/// Format a list of strings into a natural language string
pub fn formatList(
    allocator: std.mem.Allocator,
    items: []const []const u8,
    use_chinese: bool,
) HumanizeError![]u8 {
    if (items.len == 0) {
        return allocator.dupe(u8, "");
    }

    if (items.len == 1) {
        return allocator.dupe(u8, items[0]);
    }

    if (items.len == 2) {
        const sep: []const u8 = if (use_chinese) " 和 " else " and ";
        const buf = allocator.alloc(u8, items[0].len + items[1].len + 10) catch return HumanizeError.OutOfMemory;
        const result_slice = std.fmt.bufPrint(buf, "{s}{s}{s}", .{ items[0], sep, items[1] }) catch return HumanizeError.BufferTooSmall;
        const result = allocator.dupe(u8, result_slice) catch return HumanizeError.OutOfMemory;
        allocator.free(buf);
        return result;
    }

    // Calculate total length needed
    var total_len: usize = 0;
    for (items) |item| {
        total_len += item.len;
    }
    total_len += items.len * 2 + 10; // separators and "和" / "and"

    const buf = allocator.alloc(u8, total_len) catch return HumanizeError.OutOfMemory;
    var pos: usize = 0;

    const item_sep: []const u8 = if (use_chinese) "、" else ", ";
    const final_sep: []const u8 = if (use_chinese) " 和 " else " and ";

    // Add all but last item with separators
    for (items[0 .. items.len - 1], 0..) |item, idx| {
        @memcpy(buf[pos .. pos + item.len], item);
        pos += item.len;
        if (idx < items.len - 2) {
            @memcpy(buf[pos .. pos + item_sep.len], item_sep);
            pos += item_sep.len;
        } else {
            @memcpy(buf[pos .. pos + final_sep.len], final_sep);
            pos += final_sep.len;
        }
    }
    
    // Add last item
    const last_item = items[items.len - 1];
    @memcpy(buf[pos .. pos + last_item.len], last_item);
    pos += last_item.len;

    const result = allocator.dupe(u8, buf[0..pos]) catch return HumanizeError.OutOfMemory;
    allocator.free(buf);
    return result;
}

// ============================================================================
// Tests
// ============================================================================

test "formatBytes - basic" {
    const allocator = std.testing.allocator;

    const result1 = try formatBytes(allocator, 0, 2, false);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("0 B", result1);

    const result2 = try formatBytes(allocator, 500, 2, false);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("500 B", result2);

    const result3 = try formatBytes(allocator, 1024, 2, false);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("1.02 KB", result3);

    const result4 = try formatBytes(allocator, 1536, 2, false);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("1.54 KB", result4);

    const result5 = try formatBytes(allocator, 1024, 2, true);
    defer allocator.free(result5);
    try std.testing.expectEqualStrings("1.00 KiB", result5);

    const result6 = try formatBytes(allocator, 1500000, 2, false);
    defer allocator.free(result6);
    try std.testing.expectEqualStrings("1.50 MB", result6);
}

test "parseSize - basic" {
    try std.testing.expectEqual(@as(usize, 1000), try parseSize("1KB"));
    try std.testing.expectEqual(@as(usize, 1024), try parseSize("1KiB"));
    try std.testing.expectEqual(@as(usize, 1500000), try parseSize("1.5MB"));
    try std.testing.expectEqual(@as(usize, 2000000000), try parseSize("2GB"));
    try std.testing.expectEqual(@as(usize, 100), try parseSize("100B"));
}

test "formatDuration - full format" {
    const allocator = std.testing.allocator;

    const result1 = try formatDuration(allocator, 3665, .full);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("01:01:05", result1);

    const result2 = try formatDuration(allocator, 3600, .full);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("01:00:00", result2);

    const result3 = try formatDuration(allocator, 59, .full);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("00:00:59", result3);
}

test "formatDuration - compact format" {
    const allocator = std.testing.allocator;

    const result1 = try formatDuration(allocator, 3665, .compact);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("1h1m5s", result1);

    const result2 = try formatDuration(allocator, 3600, .compact);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("1h0m0s", result2);

    const result3 = try formatDuration(allocator, 90, .compact);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("1m30s", result3);
}

test "formatDuration - text format" {
    const allocator = std.testing.allocator;

    const result1 = try formatDuration(allocator, 3665, .text);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("1 hour 1 minute 5 seconds", result1);

    const result2 = try formatDuration(allocator, 3600, .text);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("1 hour", result2);

    const result3 = try formatDuration(allocator, 90, .text);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("1 minute 30 seconds", result3);

    const result4 = try formatDuration(allocator, 3665, .text_cn);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("1小时1分钟5秒", result4);
}

test "formatWithCommas" {
    const allocator = std.testing.allocator;

    const result1 = try formatWithCommas(allocator, 0);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("0", result1);

    const result2 = try formatWithCommas(allocator, 100);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("100", result2);

    const result3 = try formatWithCommas(allocator, 1000);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("1,000", result3);

    const result4 = try formatWithCommas(allocator, 1000000);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("1,000,000", result4);

    const result5 = try formatWithCommas(allocator, 1234567);
    defer allocator.free(result5);
    try std.testing.expectEqualStrings("1,234,567", result5);

    const result6 = try formatWithCommas(allocator, -1000000);
    defer allocator.free(result6);
    try std.testing.expectEqualStrings("-1,000,000", result6);
}

test "formatNumberCompact" {
    const allocator = std.testing.allocator;

    const result1 = try formatNumberCompact(allocator, 0, 1);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("0", result1);

    const result2 = try formatNumberCompact(allocator, 500, 1);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("500", result2);

    const result3 = try formatNumberCompact(allocator, 1500, 1);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("1.5 K", result3);

    const result4 = try formatNumberCompact(allocator, 1500000, 1);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("1.5 M", result4);

    const result5 = try formatNumberCompact(allocator, 1500000000, 1);
    defer allocator.free(result5);
    try std.testing.expectEqualStrings("1.5 B", result5);

    const result6 = try formatNumberCompact(allocator, -1500000, 1);
    defer allocator.free(result6);
    try std.testing.expectEqualStrings("-1.5 M", result6);
}

test "formatPercentage" {
    const allocator = std.testing.allocator;

    const result1 = try formatPercentage(allocator, 0.5, 1, false);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("50.0%", result1);

    const result2 = try formatPercentage(allocator, 50, 1, false);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("50.0%", result2);

    const result3 = try formatPercentage(allocator, 0.256, 2, false);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("25.60%", result3);

    const result4 = try formatPercentage(allocator, 0.5, 1, true);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("+50.0%", result4);
}

test "formatRelativeTime" {
    const allocator = std.testing.allocator;

    const result1 = try formatRelativeTime(allocator, 30, false);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("30 seconds ago", result1);

    const result2 = try formatRelativeTime(allocator, 1, false);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("1 second ago", result2);

    const result3 = try formatRelativeTime(allocator, 120, false);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("2 minutes ago", result3);

    const result4 = try formatRelativeTime(allocator, 3600, false);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("1 hour ago", result4);

    const result5 = try formatRelativeTime(allocator, 86400, false);
    defer allocator.free(result5);
    try std.testing.expectEqualStrings("1 day ago", result5);

    const result6 = try formatRelativeTime(allocator, 30, true);
    defer allocator.free(result6);
    try std.testing.expectEqualStrings("30秒前", result6);

    const result7 = try formatRelativeTime(allocator, 120, true);
    defer allocator.free(result7);
    try std.testing.expectEqualStrings("2分钟前", result7);
}

test "truncateText" {
    const allocator = std.testing.allocator;

    const result1 = try truncateText(allocator, "Hello World", 20, "...");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("Hello World", result1);

    const result2 = try truncateText(allocator, "Hello World", 8, "...");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("Hello...", result2);

    // Note: Chinese characters are UTF-8 encoded, so truncation at byte level
    // may split characters. For proper Unicode truncation, use a Unicode-aware library.
}

test "formatOrdinal" {
    const allocator = std.testing.allocator;

    const result1 = try formatOrdinal(allocator, 1);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("1st", result1);

    const result2 = try formatOrdinal(allocator, 2);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("2nd", result2);

    const result3 = try formatOrdinal(allocator, 3);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("3rd", result3);

    const result4 = try formatOrdinal(allocator, 4);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("4th", result4);

    const result5 = try formatOrdinal(allocator, 11);
    defer allocator.free(result5);
    try std.testing.expectEqualStrings("11th", result5);

    const result6 = try formatOrdinal(allocator, 21);
    defer allocator.free(result6);
    try std.testing.expectEqualStrings("21st", result6);

    const result7 = try formatOrdinalChinese(allocator, 1);
    defer allocator.free(result7);
    try std.testing.expectEqualStrings("第1", result7);
}

test "formatList" {
    const allocator = std.testing.allocator;

    const items1: []const []const u8 = &.{"a"};
    const result1 = try formatList(allocator, items1, false);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("a", result1);

    const items2: []const []const u8 = &.{ "a", "b" };
    const result2 = try formatList(allocator, items2, false);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("a and b", result2);

    const items3: []const []const u8 = &.{ "a", "b", "c" };
    const result3 = try formatList(allocator, items3, false);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("a, b and c", result3);

    const items4: []const []const u8 = &.{ "苹果", "香蕉", "樱桃" };
    const result4 = try formatList(allocator, items4, true);
    defer allocator.free(result4);
    try std.testing.expectEqualStrings("苹果、香蕉 和 樱桃", result4);
}