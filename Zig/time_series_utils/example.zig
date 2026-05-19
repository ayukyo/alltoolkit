const std = @import("std");
const time_series = @import("time_series.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();

    // Sample stock price data (daily closing prices)
    const stock_prices = [_]f64{
        100.0, 102.5, 101.3, 105.0, 103.8,
        107.2, 106.5, 110.0, 108.5, 112.3,
        115.0, 113.5, 118.0, 116.2, 120.5,
        119.0, 122.0, 121.5, 125.0, 123.8,
    };

    try stdout.print("=== Time Series Analysis Example ===\n\n", .{});
    try stdout.print("Stock Prices (20 days):\n", .{});
    for (stock_prices, 0..) |price, i| {
        try stdout.print("  Day {d:2}: ${d:6.2}\n", .{ i + 1, price });
    }

    // 1. Simple Moving Average
    try stdout.print("\n--- Simple Moving Average (5-day) ---\n", .{});
    const sma = try time_series.simpleMovingAverage(allocator, &stock_prices, 5);
    defer allocator.free(sma);

    for (stock_prices, 0..) |_, i| {
        if (sma[i] > 0) {
            try stdout.print("  Day {d:2}: SMA = ${d:6.2}\n", .{ i + 1, sma[i] });
        }
    }

    // 2. Exponential Moving Average
    try stdout.print("\n--- Exponential Moving Average (5-day) ---\n", .{});
    const ema = try time_series.exponentialMovingAverage(allocator, &stock_prices, 5);
    defer allocator.free(ema);

    for (stock_prices, 0..) |_, i| {
        try stdout.print("  Day {d:2}: EMA = ${d:6.2}\n", .{ i + 1, ema[i] });
    }

    // 3. Trend Detection
    try stdout.print("\n--- Trend Detection ---\n", .{});
    const trend = time_series.detectTrend(&stock_prices);
    try stdout.print("  Overall trend: {s}\n", .{trend.toString()});

    // Analyze trend in two halves
    const first_half = stock_prices[0..10];
    const second_half = stock_prices[10..20];
    try stdout.print("  First 10 days trend: {s}\n", .{time_series.detectTrend(first_half).toString()});
    try stdout.print("  Last 10 days trend: {s}\n", .{time_series.detectTrend(second_half).toString()});

    // 4. Daily Changes
    try stdout.print("\n--- Daily Price Changes ---\n", .{});
    const changes = try time_series.diff(allocator, &stock_prices);
    defer allocator.free(changes);

    for (changes, 0..) |change, i| {
        const sign = if (change >= 0) "+" else "";
        try stdout.print("  Day {d:2} -> {d:2}: {s}{d:6.2}\n", .{ i + 1, i + 2, sign, change });
    }

    // 5. Percentage Changes
    try stdout.print("\n--- Percentage Changes ---\n", .{});
    const pct_changes = try time_series.pctChange(allocator, &stock_prices);
    defer allocator.free(pct_changes);

    for (pct_changes, 0..) |pct, i| {
        try stdout.print("  Day {d:2} -> {d:2}: {d:6.2}%\n", .{ i + 1, i + 2, pct * 100 });
    }

    // 6. Rolling Volatility (Standard Deviation)
    try stdout.print("\n--- Rolling Volatility (5-day window) ---\n", .{});
    const volatility = try time_series.rollingStd(allocator, &stock_prices, 5);
    defer allocator.free(volatility);

    for (stock_prices, 0..) |_, i| {
        if (volatility[i] > 0) {
            try stdout.print("  Day {d:2}: Std Dev = ${d:6.2}\n", .{ i + 1, volatility[i] });
        }
    }

    // 7. Cumulative Return
    try stdout.print("\n--- Cumulative Return ---\n", .{});
    const cumulative = try time_series.cumsum(allocator, changes);
    defer allocator.free(cumulative);

    for (cumulative, 0..) |cum, i| {
        const sign = if (cum >= 0) "+" else "";
        try stdout.print("  Day {d:2}: Total Change = {s}${d:6.2}\n", .{ i + 2, sign, cum });
    }

    // 8. Weighted Moving Average
    try stdout.print("\n--- Weighted Moving Average (5-day) ---\n", .{});
    const wma = try time_series.weightedMovingAverage(allocator, &stock_prices, 5);
    defer allocator.free(wma);

    for (stock_prices, 0..) |_, i| {
        if (wma[i] > 0) {
            try stdout.print("  Day {d:2}: WMA = ${d:6.2}\n", .{ i + 1, wma[i] });
        }
    }

    // Summary Statistics
    try stdout.print("\n=== Summary Statistics ===\n", .{});
    var sum: f64 = 0;
    var min_price = stock_prices[0];
    var max_price = stock_prices[0];
    for (stock_prices) |price| {
        sum += price;
        if (price < min_price) min_price = price;
        if (price > max_price) max_price = price;
    }
    const avg_price = sum / @as(f64, @floatFromInt(stock_prices.len));

    try stdout.print("  Starting Price: ${d:.2}\n", .{stock_prices[0]});
    try stdout.print("  Ending Price:   ${d:.2}\n", .{stock_prices[stock_prices.len - 1]});
    try stdout.print("  Total Return:   {d:.2}%\n", .{(stock_prices[stock_prices.len - 1] / stock_prices[0] - 1) * 100});
    try stdout.print("  Average Price:  ${d:.2}\n", .{avg_price});
    try stdout.print("  Min Price:      ${d:.2}\n", .{min_price});
    try stdout.print("  Max Price:      ${d:.2}\n", .{max_price});
    try stdout.print("  Volatility:     ${d:.2}\n", .{volatility[volatility.len - 1]});

    try stdout.print("\n=== Analysis Complete ===\n", .{});
}