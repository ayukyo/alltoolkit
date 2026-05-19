const std = @import("std");
const math = std.math;
const ArrayList = std.ArrayList;

/// Time series data point
pub const DataPoint = struct {
    timestamp: i64, // Unix timestamp or sequential index
    value: f64,

    pub fn init(timestamp: i64, value: f64) DataPoint {
        return .{ .timestamp = timestamp, .value = value };
    }
};

/// Simple Moving Average (SMA)
pub fn simpleMovingAverage(allocator: std.mem.Allocator, data: []const f64, window: usize) ![]f64 {
    if (window == 0 or window > data.len) {
        return error.InvalidWindow;
    }

    const result = try allocator.alloc(f64, data.len);
    errdefer allocator.free(result);

    // Initialize with zeros
    @memset(result, 0);

    // Start from window-1, but use checked arithmetic
    var i: usize = window - 1;
    while (i < data.len) : (i += 1) {
        var sum: f64 = 0;
        var j: usize = 0;
        while (j < window) : (j += 1) {
            sum += data[i - (window - 1 - j)];
        }
        result[i] = sum / @as(f64, @floatFromInt(window));
    }

    return result;
}

/// Exponential Moving Average (EMA)
pub fn exponentialMovingAverage(allocator: std.mem.Allocator, data: []const f64, period: usize) ![]f64 {
    if (period == 0 or period > data.len) {
        return error.InvalidPeriod;
    }

    const result = try allocator.alloc(f64, data.len);
    errdefer allocator.free(result);

    const multiplier: f64 = 2.0 / @as(f64, @floatFromInt(period + 1));

    // First EMA value is SMA of first 'period' values
    var sum: f64 = 0;
    for (0..period) |i| {
        sum += data[i];
    }
    result[period - 1] = sum / @as(f64, @floatFromInt(period));

    // Initialize earlier values with the first EMA
    if (period > 1) {
        for (0..period - 1) |idx| {
            result[idx] = result[period - 1];
        }
    }

    // Calculate EMA for remaining values
    var i: usize = period;
    while (i < data.len) : (i += 1) {
        result[i] = (data[i] - result[i - 1]) * multiplier + result[i - 1];
    }

    return result;
}

/// Trend direction
pub const Trend = enum {
    upward,
    downward,
    sideways,

    pub fn toString(self: Trend) []const u8 {
        return switch (self) {
            .upward => "Upward",
            .downward => "Downward",
            .sideways => "Sideways",
        };
    }
};

/// Detect trend using linear regression slope
pub fn detectTrend(data: []const f64) Trend {
    if (data.len < 2) {
        return .sideways;
    }

    const n: f64 = @floatFromInt(data.len);

    // Calculate mean of x and y
    var sum_x: f64 = 0;
    var sum_y: f64 = 0;
    for (data, 0..) |y, i| {
        const x: f64 = @floatFromInt(i);
        sum_x += x;
        sum_y += y;
    }
    const mean_x = sum_x / n;
    const mean_y = sum_y / n;

    // Calculate slope
    var numerator: f64 = 0;
    var denominator: f64 = 0;
    for (data, 0..) |y, i| {
        const x: f64 = @floatFromInt(i);
        numerator += (x - mean_x) * (y - mean_y);
        denominator += (x - mean_x) * (x - mean_x);
    }

    if (denominator == 0) {
        return .sideways;
    }

    const slope = numerator / denominator;

    // Determine trend based on slope relative to mean
    const relative_slope = @abs(slope) / if (mean_y != 0) @abs(mean_y) else 1.0;
    const threshold = 0.01; // 1% threshold for trend detection

    if (relative_slope < threshold) {
        return .sideways;
    }

    return if (slope > 0) .upward else .downward;
}

/// First difference (discrete derivative)
pub fn diff(allocator: std.mem.Allocator, data: []const f64) ![]f64 {
    if (data.len < 2) {
        return error.InsufficientData;
    }

    const result = try allocator.alloc(f64, data.len - 1);
    errdefer allocator.free(result);

    for (result) |*r| {
        r.* = 0;
    }

    var i: usize = 0;
    while (i < data.len - 1) : (i += 1) {
        result[i] = data[i + 1] - data[i];
    }

    return result;
}

/// Seasonal difference with lag
pub fn seasonalDiff(allocator: std.mem.Allocator, data: []const f64, lag: usize) ![]f64 {
    if (lag == 0 or data.len <= lag) {
        return error.InvalidLag;
    }

    const result = try allocator.alloc(f64, data.len - lag);
    errdefer allocator.free(result);

    for (0..data.len - lag) |i| {
        result[i] = data[i + lag] - data[i];
    }

    return result;
}

/// Cumulative sum
pub fn cumsum(allocator: std.mem.Allocator, data: []const f64) ![]f64 {
    if (data.len == 0) {
        return error.EmptyData;
    }

    const result = try allocator.alloc(f64, data.len);
    errdefer allocator.free(result);

    result[0] = data[0];
    var i: usize = 1;
    while (i < data.len) : (i += 1) {
        result[i] = result[i - 1] + data[i];
    }

    return result;
}

/// Percentage change
pub fn pctChange(allocator: std.mem.Allocator, data: []const f64) ![]f64 {
    if (data.len < 2) {
        return error.InsufficientData;
    }

    const result = try allocator.alloc(f64, data.len - 1);
    errdefer allocator.free(result);

    for (result) |*r| {
        r.* = 0;
    }

    var i: usize = 0;
    while (i < data.len - 1) : (i += 1) {
        if (data[i] == 0) {
            result[i] = if (data[i + 1] > 0) std.math.inf(f64) else -std.math.inf(f64);
        } else {
            result[i] = (data[i + 1] - data[i]) / data[i];
        }
    }

    return result;
}

/// Rolling standard deviation
pub fn rollingStd(allocator: std.mem.Allocator, data: []const f64, window: usize) ![]f64 {
    if (window == 0 or window > data.len) {
        return error.InvalidWindow;
    }

    const result = try allocator.alloc(f64, data.len);
    errdefer allocator.free(result);

    for (result) |*r| {
        r.* = 0;
    }

    var idx: usize = window - 1;
    while (idx < data.len) : (idx += 1) {
        // Calculate mean
        var sum: f64 = 0;
        var j: usize = 0;
        while (j < window) : (j += 1) {
            sum += data[idx - (window - 1 - j)];
        }
        const mean = sum / @as(f64, @floatFromInt(window));

        // Calculate variance
        var variance_sum: f64 = 0;
        j = 0;
        while (j < window) : (j += 1) {
            const diff_val = data[idx - (window - 1 - j)] - mean;
            variance_sum += diff_val * diff_val;
        }
        const variance = variance_sum / @as(f64, @floatFromInt(window));

        result[idx] = @sqrt(variance);
    }

    return result;
}

/// Weighted Moving Average (WMA)
pub fn weightedMovingAverage(allocator: std.mem.Allocator, data: []const f64, window: usize) ![]f64 {
    if (window == 0 or window > data.len) {
        return error.InvalidWindow;
    }

    const result = try allocator.alloc(f64, data.len);
    errdefer allocator.free(result);

    for (result) |*r| {
        r.* = 0;
    }

    // Weight sum: 1 + 2 + 3 + ... + n = n*(n+1)/2
    const weight_sum: f64 = @as(f64, @floatFromInt(window)) * @as(f64, @floatFromInt(window + 1)) / 2.0;

    var idx: usize = window - 1;
    while (idx < data.len) : (idx += 1) {
        var weighted_sum: f64 = 0;
        var weight: usize = 1;
        var j: usize = 0;
        while (j < window) : (j += 1) {
            weighted_sum += data[idx - (window - 1 - j)] * @as(f64, @floatFromInt(weight));
            weight += 1;
        }
        result[idx] = weighted_sum / weight_sum;
    }

    return result;
}

// Tests
test "simpleMovingAverage" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 10, 12, 15, 14, 16, 18, 20, 19, 22, 25 };
    const result = try simpleMovingAverage(allocator, &data, 3);
    defer allocator.free(result);

    try std.testing.expectApproxEqAbs(@as(f64, 0), result[0], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0), result[1], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 12.333), result[2], 0.01);
    try std.testing.expectApproxEqAbs(@as(f64, 13.666), result[3], 0.01);
    try std.testing.expectApproxEqAbs(@as(f64, 15.0), result[4], 0.01);
}

test "exponentialMovingAverage" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 10, 12, 15, 14, 16, 18, 20, 19, 22, 25 };
    const result = try exponentialMovingAverage(allocator, &data, 3);
    defer allocator.free(result);

    try std.testing.expectApproxEqAbs(@as(f64, 12.333), result[2], 0.01);
    // EMA should be more responsive to recent changes
    try std.testing.expect(result[9] > 15);
}

test "detectTrend upward" {
    const data = [_]f64{ 10, 12, 14, 16, 18, 20, 22, 24, 26, 28 };
    const trend = detectTrend(&data);
    try std.testing.expectEqual(Trend.upward, trend);
}

test "detectTrend downward" {
    const data = [_]f64{ 28, 26, 24, 22, 20, 18, 16, 14, 12, 10 };
    const trend = detectTrend(&data);
    try std.testing.expectEqual(Trend.downward, trend);
}

test "detectTrend sideways" {
    const data = [_]f64{ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 };
    const trend = detectTrend(&data);
    try std.testing.expectEqual(Trend.sideways, trend);
}

test "diff" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 10, 15, 13, 18, 20 };
    const result = try diff(allocator, &data);
    defer allocator.free(result);

    try std.testing.expectEqual(@as(usize, 4), result.len);
    try std.testing.expectApproxEqAbs(@as(f64, 5), result[0], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, -2), result[1], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 5), result[2], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 2), result[3], 0.001);
}

test "cumsum" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 1, 2, 3, 4, 5 };
    const result = try cumsum(allocator, &data);
    defer allocator.free(result);

    try std.testing.expectApproxEqAbs(@as(f64, 1), result[0], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 3), result[1], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 6), result[2], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 10), result[3], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 15), result[4], 0.001);
}

test "pctChange" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 100, 110, 99, 99, 121 };
    const result = try pctChange(allocator, &data);
    defer allocator.free(result);

    try std.testing.expectApproxEqAbs(@as(f64, 0.1), result[0], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, -0.1), result[1], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0), result[2], 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0.222), result[3], 0.01);
}

test "rollingStd" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 10, 12, 14, 16, 18, 20, 22, 24, 26, 28 };
    const result = try rollingStd(allocator, &data, 3);
    defer allocator.free(result);

    // Linear data should have constant std for each window
    try std.testing.expectApproxEqAbs(@as(f64, 1.633), result[2], 0.01);
    try std.testing.expectApproxEqAbs(@as(f64, 1.633), result[5], 0.01);
}

test "weightedMovingAverage" {
    const allocator = std.testing.allocator;
    const data = [_]f64{ 10, 20, 30, 40, 50 };
    const result = try weightedMovingAverage(allocator, &data, 3);
    defer allocator.free(result);

    // WMA gives more weight to recent values
    try std.testing.expectApproxEqAbs(@as(f64, 23.333), result[2], 0.01);
}

test "DataPoint" {
    const dp = DataPoint.init(1609459200, 42.5);
    try std.testing.expectEqual(@as(i64, 1609459200), dp.timestamp);
    try std.testing.expectApproxEqAbs(@as(f64, 42.5), dp.value, 0.001);
}