const std = @import("std");

/// High-resolution timestamp in nanoseconds
pub const Timestamp = struct {
    value: i128,

    /// Get current timestamp
    pub fn now() Timestamp {
        return .{ .value = std.time.nanoTimestamp() };
    }

    /// Calculate duration between two timestamps
    pub fn since(self: Timestamp, earlier: Timestamp) Duration {
        return .{ .nanoseconds = self.value - earlier.value };
    }

    /// Get Unix timestamp in seconds
    pub fn unixSeconds(self: Timestamp) i64 {
        return @intCast(@divFloor(self.value, std.time.ns_per_s));
    }

    /// Get Unix timestamp in milliseconds
    pub fn unixMillis(self: Timestamp) i64 {
        return @intCast(@divFloor(self.value, std.time.ns_per_ms));
    }
};

/// Duration with nanosecond precision
pub const Duration = struct {
    nanoseconds: i128,

    /// Create duration from nanoseconds
    pub fn fromNanos(ns: i64) Duration {
        return .{ .nanoseconds = ns };
    }

    /// Create duration from microseconds
    pub fn fromMicros(us: i64) Duration {
        return .{ .nanoseconds = @as(i128, us) * std.time.ns_per_us };
    }

    /// Create duration from milliseconds
    pub fn fromMillis(ms: i64) Duration {
        return .{ .nanoseconds = @as(i128, ms) * std.time.ns_per_ms };
    }

    /// Create duration from seconds
    pub fn fromSeconds(s: i64) Duration {
        return .{ .nanoseconds = @as(i128, s) * std.time.ns_per_s };
    }

    /// Create duration from minutes
    pub fn fromMinutes(m: i64) Duration {
        return .{ .nanoseconds = @as(i128, m) * 60 * std.time.ns_per_s };
    }

    /// Create duration from hours
    pub fn fromHours(h: i64) Duration {
        return .{ .nanoseconds = @as(i128, h) * 3600 * std.time.ns_per_s };
    }

    /// Get total nanoseconds
    pub fn totalNanos(self: Duration) i128 {
        return self.nanoseconds;
    }

    /// Get total microseconds
    pub fn totalMicros(self: Duration) i64 {
        return @intCast(@divFloor(self.nanoseconds, std.time.ns_per_us));
    }

    /// Get total milliseconds
    pub fn totalMillis(self: Duration) i64 {
        return @intCast(@divFloor(self.nanoseconds, std.time.ns_per_ms));
    }

    /// Get total seconds (with fractional part)
    pub fn totalSeconds(self: Duration) f64 {
        return @as(f64, @floatFromInt(self.nanoseconds)) / std.time.ns_per_s;
    }

    /// Get total minutes
    pub fn totalMinutes(self: Duration) f64 {
        return self.totalSeconds() / 60.0;
    }

    /// Get total hours
    pub fn totalHours(self: Duration) f64 {
        return self.totalMinutes() / 60.0;
    }

    /// Convert to hours, minutes, seconds, nanoseconds
    pub fn toHMSN(self: Duration) struct { hours: i64, minutes: i64, seconds: i64, nanos: i128 } {
        const total_sec = @divFloor(self.nanoseconds, std.time.ns_per_s);
        const hours = @divFloor(total_sec, 3600);
        const remaining = @mod(total_sec, 3600);
        const minutes = @divFloor(remaining, 60);
        const seconds = @mod(remaining, 60);
        const nanos = @mod(self.nanoseconds, std.time.ns_per_s);

        return .{
            .hours = @intCast(hours),
            .minutes = @intCast(minutes),
            .seconds = @intCast(seconds),
            .nanos = nanos,
        };
    }

    /// Add two durations
    pub fn add(self: Duration, other: Duration) Duration {
        return .{ .nanoseconds = self.nanoseconds + other.nanoseconds };
    }

    /// Subtract durations
    pub fn sub(self: Duration, other: Duration) Duration {
        return .{ .nanoseconds = self.nanoseconds - other.nanoseconds };
    }

    /// Multiply duration by a scalar
    pub fn mul(self: Duration, scalar: i64) Duration {
        return .{ .nanoseconds = self.nanoseconds * scalar };
    }

    /// Divide duration by a scalar
    pub fn div(self: Duration, scalar: i64) Duration {
        return .{ .nanoseconds = @divFloor(self.nanoseconds, scalar) };
    }

    /// Check if duration is zero
    pub fn isZero(self: Duration) bool {
        return self.nanoseconds == 0;
    }

    /// Check if duration is positive
    pub fn isPositive(self: Duration) bool {
        return self.nanoseconds > 0;
    }

    /// Check if duration is negative
    pub fn isNegative(self: Duration) bool {
        return self.nanoseconds < 0;
    }

    /// Format duration as a human-readable string
    /// Caller owns the returned memory
    pub fn formatAlloc(self: Duration, allocator: std.mem.Allocator) ![]u8 {
        const hmsn = self.toHMSN();

        if (hmsn.hours > 0) {
            return std.fmt.allocPrint(allocator, "{}h {}m {}s", .{ hmsn.hours, hmsn.minutes, hmsn.seconds });
        } else if (hmsn.minutes > 0) {
            return std.fmt.allocPrint(allocator, "{}m {}s", .{ hmsn.minutes, hmsn.seconds });
        } else if (hmsn.seconds > 0) {
            return std.fmt.allocPrint(allocator, "{}s", .{hmsn.seconds});
        } else {
            return std.fmt.allocPrint(allocator, "{}ms", .{self.totalMillis()});
        }
    }
};

/// Stopwatch state
pub const StopwatchState = enum {
    idle,
    running,
    paused,
    stopped,
};

/// High-precision stopwatch with lap support
pub const Stopwatch = struct {
    start_time: ?Timestamp,
    pause_time: ?Timestamp,
    accumulated: Duration,
    state: StopwatchState,
    laps: std.ArrayList(Duration),
    allocator: std.mem.Allocator,

    /// Initialize a new stopwatch
    pub fn init(allocator: std.mem.Allocator) Stopwatch {
        return .{
            .start_time = null,
            .pause_time = null,
            .accumulated = .{ .nanoseconds = 0 },
            .state = .idle,
            .laps = std.ArrayList(Duration).init(allocator),
            .allocator = allocator,
        };
    }

    /// Free all resources
    pub fn deinit(self: *Stopwatch) void {
        self.laps.deinit();
    }

    /// Start the stopwatch
    pub fn start(self: *Stopwatch) void {
        switch (self.state) {
            .idle, .stopped => {
                self.start_time = Timestamp.now();
                self.accumulated = .{ .nanoseconds = 0 };
                self.state = .running;
            },
            .paused => {
                // Resume from pause
                if (self.pause_time) |pause_ts| {
                    const now = Timestamp.now();
                    const pause_duration = now.since(pause_ts);
                    self.accumulated = self.accumulated.sub(pause_duration);
                }
                self.pause_time = null;
                self.state = .running;
            },
            .running => {}, // Already running
        }
    }

    /// Pause the stopwatch
    pub fn pause(self: *Stopwatch) void {
        if (self.state == .running) {
            self.pause_time = Timestamp.now();
            self.state = .paused;
        }
    }

    /// Resume a paused stopwatch (alias for unpause)
    pub fn unpause(self: *Stopwatch) void {
        if (self.state == .paused) {
            if (self.pause_time) |pause_ts| {
                const now = Timestamp.now();
                const pause_duration = now.since(pause_ts);
                // Add pause duration to accumulated to "skip" it
                self.accumulated = self.accumulated.add(pause_duration);
            }
            self.pause_time = null;
            self.state = .running;
        }
    }

    /// Stop the stopwatch (final elapsed time is frozen)
    pub fn stop(self: *Stopwatch) Duration {
        if (self.state == .running or self.state == .paused) {
            self.state = .stopped;
        }
        return self.elapsed();
    }

    /// Reset the stopwatch to idle state
    pub fn reset(self: *Stopwatch) void {
        self.start_time = null;
        self.pause_time = null;
        self.accumulated = .{ .nanoseconds = 0 };
        self.state = .idle;
        self.laps.clearRetainingCapacity();
    }

    /// Record a lap time
    pub fn lap(self: *Stopwatch) !Duration {
        if (self.state != .running) {
            return error.NotRunning;
        }
        const lap_duration = self.elapsed();
        try self.laps.append(lap_duration);
        return lap_duration;
    }

    /// Get the current elapsed time
    pub fn elapsed(self: *Stopwatch) Duration {
        switch (self.state) {
            .idle => return .{ .nanoseconds = 0 },
            .running => {
                if (self.start_time) |start_ts| {
                    const now = Timestamp.now();
                    return now.since(start_ts).sub(self.accumulated);
                }
                return .{ .nanoseconds = 0 };
            },
            .paused => {
                if (self.start_time) |start_ts| {
                    if (self.pause_time) |pause_ts| {
                        return pause_ts.since(start_ts).sub(self.accumulated);
                    }
                }
                return .{ .nanoseconds = 0 };
            },
            .stopped => {
                // Return the last known elapsed time
                if (self.start_time) |start_ts| {
                    if (self.pause_time) |pause_ts| {
                        return pause_ts.since(start_ts).sub(self.accumulated);
                    }
                    const now = Timestamp.now();
                    return now.since(start_ts).sub(self.accumulated);
                }
                return .{ .nanoseconds = 0 };
            },
        }
    }

    /// Get all lap times
    pub fn getLaps(self: *Stopwatch) []Duration {
        return self.laps.items;
    }

    /// Get lap time at specific index
    pub fn getLap(self: *Stopwatch, index: usize) ?Duration {
        if (index < self.laps.items.len) {
            return self.laps.items[index];
        }
        return null;
    }

    /// Get the best (fastest) lap time
    pub fn bestLap(self: *Stopwatch) ?Duration {
        if (self.laps.items.len == 0) return null;

        var best = self.laps.items[0];
        for (self.laps.items[1..]) |lap_time| {
            if (lap_time.nanoseconds < best.nanoseconds) {
                best = lap_time;
            }
        }
        return best;
    }

    /// Get the worst (slowest) lap time
    pub fn worstLap(self: *Stopwatch) ?Duration {
        if (self.laps.items.len == 0) return null;

        var worst = self.laps.items[0];
        for (self.laps.items[1..]) |lap_time| {
            if (lap_time.nanoseconds > worst.nanoseconds) {
                worst = lap_time;
            }
        }
        return worst;
    }

    /// Get average lap time
    pub fn averageLap(self: *Stopwatch) ?Duration {
        if (self.laps.items.len == 0) return null;

        var total: i128 = 0;
        for (self.laps.items) |lap_time| {
            total += lap_time.nanoseconds;
        }
        return .{ .nanoseconds = @divFloor(total, self.laps.items.len) };
    }

    /// Check if stopwatch is running
    pub fn isRunning(self: *Stopwatch) bool {
        return self.state == .running;
    }
};

/// Countdown timer with completion callback support
pub const CountdownTimer = struct {
    duration: Duration,
    start_time: ?Timestamp,
    state: StopwatchState,
    alarm_time: ?i64, // Unix timestamp in nanoseconds when alarm should trigger

    /// Initialize a countdown timer
    pub fn init(duration: Duration) CountdownTimer {
        return .{
            .duration = duration,
            .start_time = null,
            .state = .idle,
            .alarm_time = null,
        };
    }

    /// Start the countdown
    pub fn start(self: *CountdownTimer) void {
        self.start_time = Timestamp.now();
        self.state = .running;
    }

    /// Pause the countdown
    pub fn pause(self: *CountdownTimer) void {
        if (self.state == .running) {
            self.state = .paused;
        }
    }

    /// Resume a paused countdown
    pub fn unpause(self: *CountdownTimer) void {
        if (self.state == .paused) {
            self.state = .running;
        }
    }

    /// Stop and reset the countdown
    pub fn stop(self: *CountdownTimer) void {
        self.start_time = null;
        self.state = .stopped;
    }

    /// Get remaining time
    pub fn remaining(self: *CountdownTimer) Duration {
        if (self.state != .running) {
            if (self.state == .paused and self.start_time != null) {
                // Return cached remaining time when paused
                const elapsed = Timestamp.now().since(self.start_time.?);
                const remaining_ns = self.duration.nanoseconds - elapsed.nanoseconds;
                return if (remaining_ns > 0) .{ .nanoseconds = remaining_ns } else .{ .nanoseconds = 0 };
            }
            return self.duration;
        }

        if (self.start_time) |start_ts| {
            const elapsed = Timestamp.now().since(start_ts);
            const remaining_ns = self.duration.nanoseconds - elapsed.nanoseconds;
            return if (remaining_ns > 0) .{ .nanoseconds = remaining_ns } else .{ .nanoseconds = 0 };
        }

        return self.duration;
    }

    /// Check if countdown is complete
    pub fn isComplete(self: *CountdownTimer) bool {
        return self.remaining().nanoseconds <= 0;
    }

    /// Check if countdown is running
    pub fn isRunning(self: *CountdownTimer) bool {
        return self.state == .running and !self.isComplete();
    }

    /// Reset with a new duration
    pub fn reset(self: *CountdownTimer, new_duration: Duration) void {
        self.duration = new_duration;
        self.start_time = null;
        self.state = .idle;
    }
};

/// Time formatter for various output formats
pub const TimeFormatter = struct {
    /// Format duration as HH:MM:SS.mmm
    pub fn formatHMS(allocator: std.mem.Allocator, duration: Duration) ![]u8 {
        const hmsn = duration.toHMSN();
        const millis: usize = @intCast(@divFloor(hmsn.nanos, std.time.ns_per_ms));
        
        // Manual zero-padding to avoid signed integer issues
        var buf: [16]u8 = undefined;
        var pos: usize = 0;
        
        // Hours
        if (hmsn.hours < 10) {
            buf[pos] = '0';
            pos += 1;
        }
        const h_written = std.fmt.bufPrint(buf[pos..], "{}", .{hmsn.hours}) catch unreachable;
        pos += h_written.len;
        buf[pos] = ':';
        pos += 1;
        
        // Minutes
        if (hmsn.minutes < 10) {
            buf[pos] = '0';
            pos += 1;
        }
        const m_written = std.fmt.bufPrint(buf[pos..], "{}", .{hmsn.minutes}) catch unreachable;
        pos += m_written.len;
        buf[pos] = ':';
        pos += 1;
        
        // Seconds
        if (hmsn.seconds < 10) {
            buf[pos] = '0';
            pos += 1;
        }
        const s_written = std.fmt.bufPrint(buf[pos..], "{}", .{hmsn.seconds}) catch unreachable;
        pos += s_written.len;
        buf[pos] = '.';
        pos += 1;
        
        // Milliseconds (3 digits)
        if (millis < 100) {
            buf[pos] = '0';
            pos += 1;
        }
        if (millis < 10) {
            buf[pos] = '0';
            pos += 1;
        }
        const ms_written = std.fmt.bufPrint(buf[pos..], "{}", .{millis}) catch unreachable;
        pos += ms_written.len;
        
        return allocator.dupe(u8, buf[0..pos]);
    }

    /// Format duration as compact string (1h30m45s)
    pub fn formatCompact(allocator: std.mem.Allocator, duration: Duration) ![]u8 {
        const hmsn = duration.toHMSN();
        
        if (hmsn.hours > 0) {
            return std.fmt.allocPrint(allocator, "{}h{}m{}s", .{ hmsn.hours, hmsn.minutes, hmsn.seconds });
        } else if (hmsn.minutes > 0) {
            return std.fmt.allocPrint(allocator, "{}m{}s", .{ hmsn.minutes, hmsn.seconds });
        } else if (hmsn.seconds > 0) {
            const ms = @divFloor(hmsn.nanos, std.time.ns_per_ms);
            if (ms > 0) {
                return std.fmt.allocPrint(allocator, "{}.{}s", .{ hmsn.seconds, ms });
            }
            return std.fmt.allocPrint(allocator, "{}s", .{hmsn.seconds});
        } else {
            const ms = duration.totalMillis();
            if (ms > 0) {
                return std.fmt.allocPrint(allocator, "{}ms", .{ms});
            }
            const us = duration.totalMicros();
            if (us > 0) {
                return std.fmt.allocPrint(allocator, "{}us", .{us});
            }
            return std.fmt.allocPrint(allocator, "{}ns", .{duration.totalNanos()});
        }
    }

    /// Format duration as ISO 8601 duration (PT1H30M45S)
    pub fn formatISO8601(allocator: std.mem.Allocator, duration: Duration) ![]u8 {
        const hmsn = duration.toHMSN();

        var buf: [64]u8 = undefined;
        var pos: usize = 0;

        // Start with PT
        @memcpy(buf[pos..][0..2], "PT");
        pos += 2;

        // Hours
        if (hmsn.hours > 0) {
            const written = try std.fmt.bufPrint(buf[pos..], "{}H", .{hmsn.hours});
            pos += written.len;
        }

        // Minutes
        if (hmsn.minutes > 0) {
            const written = try std.fmt.bufPrint(buf[pos..], "{}M", .{hmsn.minutes});
            pos += written.len;
        }

        // Seconds
        if (hmsn.seconds > 0 or hmsn.nanos > 0) {
            if (hmsn.nanos > 0) {
                const secs = @as(f64, @floatFromInt(hmsn.seconds)) + @as(f64, @floatFromInt(hmsn.nanos)) / std.time.ns_per_s;
                const written = try std.fmt.bufPrint(buf[pos..], "{d:.6}S", .{secs});
                pos += written.len;
            } else {
                const written = try std.fmt.bufPrint(buf[pos..], "{}S", .{hmsn.seconds});
                pos += written.len;
            }
        }

        // If no time component, add 0S
        if (pos == 2) {
            @memcpy(buf[pos..][0..2], "0S");
            pos += 2;
        }

        return allocator.dupe(u8, buf[0..pos]);
    }

    /// Format nanoseconds as human readable with appropriate unit
    pub fn formatAuto(allocator: std.mem.Allocator, ns: i128) ![]u8 {
        const duration = Duration{ .nanoseconds = ns };
        return formatCompact(allocator, duration);
    }
};

/// Sleep utilities
pub const Sleep = struct {
    /// Sleep for specified duration
    pub fn duration(d: Duration) void {
        std.time.sleep(@intCast(d.nanoseconds));
    }

    /// Sleep for milliseconds
    pub fn millis(ms: u64) void {
        std.time.sleep(ms * std.time.ns_per_ms);
    }

    /// Sleep for seconds
    pub fn seconds(s: u64) void {
        std.time.sleep(s * std.time.ns_per_s);
    }

    /// Sleep for microseconds
    pub fn micros(us: u64) void {
        std.time.sleep(us * std.time.ns_per_us);
    }

    /// Sleep for nanoseconds
    pub fn nanos(ns: u64) void {
        std.time.sleep(ns);
    }
};

// Tests
test "Timestamp - now and since" {
    const ts1 = Timestamp.now();
    std.time.sleep(1 * std.time.ns_per_ms);
    const ts2 = Timestamp.now();
    const elapsed = ts2.since(ts1);
    try std.testing.expect(elapsed.totalMillis() >= 1);
}

test "Duration - creation and conversion" {
    const d1 = Duration.fromSeconds(90);
    try std.testing.expectEqual(@as(i64, 90), d1.totalSeconds());
    try std.testing.expectEqual(@as(i64, 90_000), d1.totalMillis());

    const d2 = Duration.fromMillis(1500);
    try std.testing.expectEqual(@as(f64, 1.5), d2.totalSeconds());

    const d3 = Duration.fromMinutes(2);
    try std.testing.expectEqual(@as(i64, 120), d3.totalSeconds());
}

test "Duration - toHMSN" {
    const d = Duration.fromSeconds(3725); // 1h 2m 5s
    const hmsn = d.toHMSN();
    try std.testing.expectEqual(@as(i64, 1), hmsn.hours);
    try std.testing.expectEqual(@as(i64, 2), hmsn.minutes);
    try std.testing.expectEqual(@as(i64, 5), hmsn.seconds);
}

test "Duration - arithmetic" {
    const d1 = Duration.fromSeconds(10);
    const d2 = Duration.fromSeconds(5);
    const sum = d1.add(d2);
    try std.testing.expectEqual(@as(i64, 15), sum.totalSeconds());

    const diff = d1.sub(d2);
    try std.testing.expectEqual(@as(i64, 5), diff.totalSeconds());

    const doubled = d1.mul(2);
    try std.testing.expectEqual(@as(i64, 20), doubled.totalSeconds());
}

test "Stopwatch - basic operation" {
    const allocator = std.testing.allocator;
    var sw = Stopwatch.init(allocator);
    defer sw.deinit();

    try std.testing.expect(!sw.isRunning());
    
    sw.start();
    try std.testing.expect(sw.isRunning());
    
    std.time.sleep(10 * std.time.ns_per_ms);
    
    const elapsed = sw.elapsed();
    try std.testing.expect(elapsed.totalMillis() >= 10);
    
    _ = sw.stop();
    try std.testing.expect(!sw.isRunning());
}

test "Stopwatch - pause and unpause" {
    const allocator = std.testing.allocator;
    var sw = Stopwatch.init(allocator);
    defer sw.deinit();

    sw.start();
    std.time.sleep(20 * std.time.ns_per_ms);
    sw.pause();
    
    const elapsed_at_pause = sw.elapsed();
    std.time.sleep(50 * std.time.ns_per_ms); // This should not count
    
    const elapsed_while_paused = sw.elapsed();
    try std.testing.expectEqual(elapsed_at_pause.totalMillis(), elapsed_while_paused.totalMillis());
    
    sw.unpause();
    std.time.sleep(10 * std.time.ns_per_ms);
    
    const final = sw.elapsed();
    try std.testing.expect(final.totalMillis() >= elapsed_at_pause.totalMillis());
}

test "Stopwatch - laps" {
    const allocator = std.testing.allocator;
    var sw = Stopwatch.init(allocator);
    defer sw.deinit();

    sw.start();
    
    _ = try sw.lap();
    std.time.sleep(10 * std.time.ns_per_ms);
    const lap1 = try sw.lap();
    std.time.sleep(10 * std.time.ns_per_ms);
    const lap2 = try sw.lap();

    try std.testing.expectEqual(@as(usize, 3), sw.getLaps().len);
    try std.testing.expect(lap2.totalMillis() >= lap1.totalMillis());

    const best = sw.bestLap().?;
    const worst = sw.worstLap().?;
    try std.testing.expect(best.nanoseconds <= worst.nanoseconds);
}

test "CountdownTimer - basic operation" {
    var timer = CountdownTimer.init(Duration.fromMillis(100));
    
    try std.testing.expect(!timer.isComplete());
    
    timer.start();
    try std.testing.expect(timer.isRunning());
    
    std.time.sleep(50 * std.time.ns_per_ms);
    const remaining = timer.remaining();
    try std.testing.expect(remaining.totalMillis() < 100);
    try std.testing.expect(remaining.totalMillis() >= 40);
    
    std.time.sleep(60 * std.time.ns_per_ms);
    try std.testing.expect(timer.isComplete());
}

test "TimeFormatter - formatHMS" {
    const allocator = std.testing.allocator;
    const d = Duration.fromSeconds(3725).add(Duration.fromMillis(500));
    
    const formatted = try TimeFormatter.formatHMS(allocator, d);
    defer allocator.free(formatted);
    
    try std.testing.expectEqualStrings("01:02:05.500", formatted);
}

test "TimeFormatter - formatCompact" {
    const allocator = std.testing.allocator;
    
    const d1 = Duration.fromSeconds(3725);
    const f1 = try TimeFormatter.formatCompact(allocator, d1);
    defer allocator.free(f1);
    try std.testing.expectEqualStrings("1h2m5s", f1);

    const d2 = Duration.fromSeconds(125);
    const f2 = try TimeFormatter.formatCompact(allocator, d2);
    defer allocator.free(f2);
    try std.testing.expectEqualStrings("2m5s", f2);

    const d3 = Duration.fromMillis(500);
    const f3 = try TimeFormatter.formatCompact(allocator, d3);
    defer allocator.free(f3);
    try std.testing.expectEqualStrings("500ms", f3);
}

test "TimeFormatter - formatISO8601" {
    const allocator = std.testing.allocator;
    const d = Duration.fromSeconds(3725);
    
    const formatted = try TimeFormatter.formatISO8601(allocator, d);
    defer allocator.free(formatted);
    
    try std.testing.expectEqualStrings("PT1H2M5S", formatted);
}

test "Sleep utilities" {
    const start = Timestamp.now();
    Sleep.millis(10);
    const end = Timestamp.now();
    const elapsed = end.since(start);
    try std.testing.expect(elapsed.totalMillis() >= 10);
}