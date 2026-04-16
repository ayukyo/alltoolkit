const std = @import("std");
const stopwatch_utils = @import("stopwatch-utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    var stdout = std.io.getStdOut().writer();

    try stdout.print("\n", .{});
    try stdout.print("╔════════════════════════════════════════════════════════════╗\n", .{});
    try stdout.print("║         Zig Stopwatch Utils - Examples                     ║\n", .{});
    try stdout.print("╚════════════════════════════════════════════════════════════╝\n", .{});
    try stdout.print("\n", .{});

    // 1. Basic Duration Operations
    try stdout.print("┌─ Duration Operations ─────────────────────────────────────┐\n", .{});
    
    const d1 = stopwatch_utils.Duration.fromSeconds(3725);
    const d2 = stopwatch_utils.Duration.fromMinutes(30);
    
    try stdout.print("│ Duration 1: {} seconds = ", .{d1.totalSeconds()});
    const f1 = try stopwatch_utils.TimeFormatter.formatCompact(allocator, d1);
    defer allocator.free(f1);
    try stdout.print("{s}\n", .{f1});
    
    try stdout.print("│ Duration 2: {} minutes = ", .{d2.totalMinutes()});
    const f2 = try stopwatch_utils.TimeFormatter.formatCompact(allocator, d2);
    defer allocator.free(f2);
    try stdout.print("{s}\n", .{f2});
    
    const sum = d1.add(d2);
    try stdout.print("│ Sum: ", .{});
    const f3 = try stopwatch_utils.TimeFormatter.formatHMS(allocator, sum);
    defer allocator.free(f3);
    try stdout.print("{s}\n", .{f3});
    
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // 2. Stopwatch Demo
    try stdout.print("┌─ Stopwatch Demo ──────────────────────────────────────────┐\n", .{});
    
    var sw = stopwatch_utils.Stopwatch.init(allocator);
    defer sw.deinit();

    try stdout.print("│ Starting stopwatch...\n", .{});
    sw.start();

    try stdout.print("│ Running task 1 (100ms)...\n", .{});
    std.time.sleep(100 * std.time.ns_per_ms);
    const lap1 = try sw.lap();
    const lap1_fmt = try stopwatch_utils.TimeFormatter.formatCompact(allocator, lap1);
    defer allocator.free(lap1_fmt);
    try stdout.print("│ Lap 1: {s}\n", .{lap1_fmt});

    try stdout.print("│ Running task 2 (150ms)...\n", .{});
    std.time.sleep(150 * std.time.ns_per_ms);
    const lap2 = try sw.lap();
    const lap2_fmt = try stopwatch_utils.TimeFormatter.formatCompact(allocator, lap2);
    defer allocator.free(lap2_fmt);
    try stdout.print("│ Lap 2: {s}\n", .{lap2_fmt});

    try stdout.print("│ Running task 3 (80ms)...\n", .{});
    std.time.sleep(80 * std.time.ns_per_ms);
    _ = try sw.lap();

    const elapsed = sw.stop();
    const elapsed_fmt = try stopwatch_utils.TimeFormatter.formatHMS(allocator, elapsed);
    defer allocator.free(elapsed_fmt);
    try stdout.print("│ Total: {s}\n", .{elapsed_fmt});

    // Lap statistics
    if (sw.bestLap()) |best| {
        const best_fmt = try stopwatch_utils.TimeFormatter.formatCompact(allocator, best);
        defer allocator.free(best_fmt);
        try stdout.print("│ Best lap: {s}\n", .{best_fmt});
    }

    if (sw.worstLap()) |worst| {
        const worst_fmt = try stopwatch_utils.TimeFormatter.formatCompact(allocator, worst);
        defer allocator.free(worst_fmt);
        try stdout.print("│ Worst lap: {s}\n", .{worst_fmt});
    }

    if (sw.averageLap()) |avg| {
        const avg_fmt = try stopwatch_utils.TimeFormatter.formatCompact(allocator, avg);
        defer allocator.free(avg_fmt);
        try stdout.print("│ Average lap: {s}\n", .{avg_fmt});
    }

    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // 3. Countdown Timer Demo
    try stdout.print("┌─ Countdown Timer Demo ───────────────────────────────────┐\n", .{});
    
    var timer = stopwatch_utils.CountdownTimer.init(stopwatch_utils.Duration.fromMillis(200));
    
    try stdout.print("│ Starting 200ms countdown...\n", .{});
    timer.start();

    var last_remaining: i64 = 999;
    while (!timer.isComplete()) {
        const remaining = timer.remaining();
        if (remaining.totalMillis() != last_remaining) {
            last_remaining = remaining.totalMillis();
            if (last_remaining > 0 and @mod(last_remaining, 50) == 0) {
                try stdout.print("│ Remaining: {}ms\n", .{last_remaining});
            }
        }
        std.time.sleep(10 * std.time.ns_per_ms);
    }
    
    try stdout.print("│ Countdown complete!\n", .{});
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // 4. Timestamp Demo
    try stdout.print("┌─ Timestamp Demo ─────────────────────────────────────────┐\n", .{});
    
    const now = stopwatch_utils.Timestamp.now();
    try stdout.print("│ Current Unix timestamp: {} seconds\n", .{now.unixSeconds()});
    try stdout.print("│ Current Unix timestamp: {} milliseconds\n", .{now.unixMillis()});
    
    const start = stopwatch_utils.Timestamp.now();
    std.time.sleep(50 * std.time.ns_per_ms);
    const end = stopwatch_utils.Timestamp.now();
    const duration = end.since(start);
    
    try stdout.print("│ Measured duration: {} nanoseconds\n", .{duration.totalNanos()});
    try stdout.print("│ Measured duration: {} milliseconds\n", .{duration.totalMillis()});
    
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // 5. Time Formatting Demo
    try stdout.print("┌─ Time Formatting Demo ───────────────────────────────────┐\n", .{});
    
    const test_duration = stopwatch_utils.Duration.fromSeconds(3661)
        .add(stopwatch_utils.Duration.fromMillis(234));
    
    const hms = try stopwatch_utils.TimeFormatter.formatHMS(allocator, test_duration);
    defer allocator.free(hms);
    try stdout.print("│ HMS format:      {s}\n", .{hms});
    
    const compact = try stopwatch_utils.TimeFormatter.formatCompact(allocator, test_duration);
    defer allocator.free(compact);
    try stdout.print("│ Compact format:  {s}\n", .{compact});
    
    const iso = try stopwatch_utils.TimeFormatter.formatISO8601(allocator, test_duration);
    defer allocator.free(iso);
    try stdout.print("│ ISO 8601 format: {s}\n", .{iso});
    
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // 6. Pause/Resume Demo
    try stdout.print("┌─ Pause/Resume Demo ───────────────────────────────────────┐\n", .{});
    
    var sw2 = stopwatch_utils.Stopwatch.init(allocator);
    defer sw2.deinit();
    
    try stdout.print("│ Starting stopwatch...\n", .{});
    sw2.start();
    std.time.sleep(50 * std.time.ns_per_ms);
    
    try stdout.print("│ Pausing at ~50ms...\n", .{});
    sw2.pause();
    const paused_time = sw2.elapsed();
    try stdout.print("│ Paused at: {}ms\n", .{paused_time.totalMillis()});
    
    try stdout.print("│ Waiting 100ms while paused (should not count)...\n", .{});
    std.time.sleep(100 * std.time.ns_per_ms);
    
    try stdout.print("│ Resuming...\n", .{});
    sw2.unpause();
    std.time.sleep(50 * std.time.ns_per_ms);
    
    const final_time = sw2.stop();
    try stdout.print("│ Final time: ~{}ms (should be ~100ms)\n", .{final_time.totalMillis()});
    
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    try stdout.print("✓ All examples completed successfully!\n\n", .{});
}