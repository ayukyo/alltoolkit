const std = @import("std");
const stopwatch_utils = @import("stopwatch-utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    var stdout = std.io.getStdOut().writer();

    try stdout.print("\n", .{});
    try stdout.print("╔════════════════════════════════════════════════════════════╗\n", .{});
    try stdout.print("║         Zig Stopwatch Utils - Benchmarks                   ║\n", .{});
    try stdout.print("╚════════════════════════════════════════════════════════════╝\n", .{});
    try stdout.print("\n", .{});

    const iterations = 1000000;

    // Benchmark 1: Timestamp.now()
    try stdout.print("┌─ Timestamp.now() Benchmark ───────────────────────────────┐\n", .{});
    
    var timer = try std.time.Timer.start();
    var i: usize = 0;
    while (i < iterations) : (i += 1) {
        _ = stopwatch_utils.Timestamp.now();
    }
    const timestamp_ns = timer.read();
    const timestamp_per_op = @divFloor(timestamp_ns, iterations);
    
    try stdout.print("│ {d} calls to Timestamp.now()\n", .{iterations});
    try stdout.print("│ Total time: {} ns\n", .{timestamp_ns});
    try stdout.print("│ Per call: {} ns\n", .{timestamp_per_op});
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // Benchmark 2: Duration operations
    try stdout.print("┌─ Duration Operations Benchmark ──────────────────────────┐\n", .{});
    
    const d1 = stopwatch_utils.Duration.fromSeconds(12345);
    const d2 = stopwatch_utils.Duration.fromMinutes(67);
    
    timer.reset();
    i = 0;
    while (i < iterations) : (i += 1) {
        _ = d1.add(d2);
    }
    const add_ns = timer.read();
    
    timer.reset();
    i = 0;
    while (i < iterations) : (i += 1) {
        _ = d1.totalMillis();
    }
    const millis_ns = timer.read();
    
    timer.reset();
    i = 0;
    while (i < iterations) : (i += 1) {
        _ = d1.toHMSN();
    }
    const hmsn_ns = timer.read();
    
    try stdout.print("│ Duration.add():      {} ns/op\n", .{@divFloor(add_ns, iterations)});
    try stdout.print("│ Duration.totalMillis(): {} ns/op\n", .{@divFloor(millis_ns, iterations)});
    try stdout.print("│ Duration.toHMSN():   {} ns/op\n", .{@divFloor(hmsn_ns, iterations)});
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // Benchmark 3: Stopwatch operations
    try stdout.print("┌─ Stopwatch Operations Benchmark ─────────────────────────┐\n", .{});
    
    var sw = stopwatch_utils.Stopwatch.init(allocator);
    defer sw.deinit();
    sw.start();
    
    timer.reset();
    i = 0;
    while (i < iterations) : (i += 1) {
        _ = sw.elapsed();
    }
    const elapsed_ns = timer.read();
    
    timer.reset();
    i = 0;
    while (i < 10000) : (i += 1) {
        _ = try sw.lap();
    }
    const lap_ns = timer.read();
    
    try stdout.print("│ Stopwatch.elapsed(): {} ns/op\n", .{@divFloor(elapsed_ns, iterations)});
    try stdout.print("│ Stopwatch.lap():     {} ns/op (10000 laps)\n", .{@divFloor(lap_ns, 10000)});
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // Benchmark 4: Time formatting
    try stdout.print("┌─ Time Formatting Benchmark ───────────────────────────────┐\n", .{});
    
    const test_duration = stopwatch_utils.Duration.fromSeconds(3661)
        .add(stopwatch_utils.Duration.fromMillis(234));
    
    timer.reset();
    i = 0;
    while (i < 10000) : (i += 1) {
        const f = try stopwatch_utils.TimeFormatter.formatHMS(allocator, test_duration);
        allocator.free(f);
    }
    const hms_fmt_ns = timer.read();
    
    timer.reset();
    i = 0;
    while (i < 10000) : (i += 1) {
        const f = try stopwatch_utils.TimeFormatter.formatCompact(allocator, test_duration);
        allocator.free(f);
    }
    const compact_fmt_ns = timer.read();
    
    timer.reset();
    i = 0;
    while (i < 10000) : (i += 1) {
        const f = try stopwatch_utils.TimeFormatter.formatISO8601(allocator, test_duration);
        allocator.free(f);
    }
    const iso_fmt_ns = timer.read();
    
    try stdout.print("│ formatHMS():       {} ns/op\n", .{@divFloor(hms_fmt_ns, 10000)});
    try stdout.print("│ formatCompact():   {} ns/op\n", .{@divFloor(compact_fmt_ns, 10000)});
    try stdout.print("│ formatISO8601():   {} ns/op\n", .{@divFloor(iso_fmt_ns, 10000)});
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    // Benchmark 5: Countdown timer
    try stdout.print("┌─ Countdown Timer Benchmark ───────────────────────────────┐\n", .{});
    
    var countdown = stopwatch_utils.CountdownTimer.init(stopwatch_utils.Duration.fromSeconds(60));
    countdown.start();
    
    timer.reset();
    i = 0;
    while (i < iterations) : (i += 1) {
        _ = countdown.remaining();
    }
    const remaining_ns = timer.read();
    
    timer.reset();
    i = 0;
    while (i < iterations) : (i += 1) {
        _ = countdown.isComplete();
    }
    const complete_ns = timer.read();
    
    try stdout.print("│ remaining():   {} ns/op\n", .{@divFloor(remaining_ns, iterations)});
    try stdout.print("│ isComplete():  {} ns/op\n", .{@divFloor(complete_ns, iterations)});
    try stdout.print("└───────────────────────────────────────────────────────────┘\n\n", .{});

    try stdout.print("✓ All benchmarks completed!\n\n", .{});
}