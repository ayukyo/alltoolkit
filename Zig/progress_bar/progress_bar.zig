const std = @import("std");

/// Progress bar configuration options
pub const ProgressBarOptions = struct {
    width: usize = 40,
    fill_char: u8 = '=',
    empty_char: u8 = '-',
    left_bracket: u8 = '[',
    right_bracket: u8 = ']',
    show_percentage: bool = true,
    show_count: bool = false,
    show_time: bool = false,
    show_eta: bool = false,
    prefix: []const u8 = "",
    suffix: []const u8 = "",
};

/// A terminal progress bar
pub const ProgressBar = struct {
    allocator: std.mem.Allocator,
    total: usize,
    current: usize,
    options: ProgressBarOptions,
    start_time: ?i64,
    last_update: i64,
    update_interval_ms: i64,
    writer: std.io.AnyWriter,

    const Self = @This();

    /// Initialize a new progress bar
    pub fn init(allocator: std.mem.Allocator, total: usize, writer: std.io.AnyWriter, options: ProgressBarOptions) Self {
        return .{
            .allocator = allocator,
            .total = total,
            .current = 0,
            .options = options,
            .start_time = null,
            .last_update = 0,
            .update_interval_ms = 100,
            .writer = writer,
        };
    }

    /// Start the progress bar
    pub fn start(self: *Self) !void {
        self.start_time = std.time.milliTimestamp();
        self.last_update = 0;
        try self.render();
    }

    /// Update progress by increment
    pub fn increment(self: *Self) !void {
        try self.update(self.current + 1);
    }

    /// Update progress to a specific value
    pub fn update(self: *Self, current: usize) !void {
        self.current = @min(current, self.total);
        
        const now = std.time.milliTimestamp();
        if (now - self.last_update < self.update_interval_ms and self.current < self.total) {
            return;
        }
        self.last_update = now;
        
        try self.render();
    }

    /// Finish the progress bar
    pub fn finish(self: *Self) !void {
        self.current = self.total;
        try self.render();
        try self.writer.print("\n", .{});
    }

    /// Get current percentage (0-100)
    pub fn percentage(self: Self) usize {
        if (self.total == 0) return 100;
        return @as(usize, @intCast(@divTrunc(@as(i64, @intCast(self.current)) * 100, @as(i64, @intCast(self.total)))));
    }

    /// Get elapsed time in milliseconds
    pub fn elapsedMs(self: Self) i64 {
        if (self.start_time == null) return 0;
        return std.time.milliTimestamp() - self.start_time.?;
    }

    /// Get estimated remaining time in milliseconds
    pub fn etaMs(self: Self) i64 {
        if (self.current == 0 or self.start_time == null) return 0;
        const elapsed = self.elapsedMs();
        if (elapsed == 0) return 0;
        
        const rate = @as(f64, @floatFromInt(self.current)) / @as(f64, @floatFromInt(elapsed));
        const remaining = @as(f64, @floatFromInt(self.total - self.current));
        
        return @as(i64, @intFromFloat(remaining / rate));
    }

    /// Format duration as human-readable string
    fn formatDuration(ms: i64, writer: std.io.AnyWriter) !void {
        const total_seconds = @divTrunc(ms, 1000);
        const hours = @divTrunc(total_seconds, 3600);
        const minutes = @divTrunc(@mod(total_seconds, 3600), 60);
        const seconds = @mod(total_seconds, 60);
        
        if (hours > 0) {
            try writer.print("{d:0>2}:{d:0>2}:{d:0>2}", .{ hours, minutes, seconds });
        } else if (minutes > 0) {
            try writer.print("{d:0>2}:{d:0>2}", .{ minutes, seconds });
        } else {
            try writer.print("{d}s", .{seconds});
        }
    }

    /// Render the progress bar
    fn render(self: Self) !void {
        // Clear current line and move to beginning
        try self.writer.print("\x1b[2K\r", .{});

        // Print prefix
        if (self.options.prefix.len > 0) {
            try self.writer.print("{s} ", .{self.options.prefix});
        }

        // Print left bracket
        try self.writer.writeByte(self.options.left_bracket);

        // Calculate filled portion
        const pct = self.percentage();
        const filled = @as(usize, @intFromFloat(@as(f64, @floatFromInt(pct)) / 100.0 * @as(f64, @floatFromInt(self.options.width))));

        // Print filled portion
        var i: usize = 0;
        while (i < filled) : (i += 1) {
            try self.writer.writeByte(self.options.fill_char);
        }

        // Print empty portion
        while (i < self.options.width) : (i += 1) {
            try self.writer.writeByte(self.options.empty_char);
        }

        // Print right bracket
        try self.writer.writeByte(self.options.right_bracket);

        // Print percentage
        if (self.options.show_percentage) {
            try self.writer.print(" {d:3}%", .{pct});
        }

        // Print count
        if (self.options.show_count) {
            try self.writer.print(" ({d}/{d})", .{ self.current, self.total });
        }

        // Print elapsed time
        if (self.options.show_time) {
            try self.writer.print(" [", .{});
            try formatDuration(self.elapsedMs(), self.writer);
            try self.writer.writeByte(']');
        }

        // Print ETA
        if (self.options.show_eta and self.current > 0) {
            try self.writer.print(" ETA: ", .{});
            try formatDuration(self.etaMs(), self.writer);
        }

        // Print suffix
        if (self.options.suffix.len > 0) {
            try self.writer.print(" {s}", .{self.options.suffix});
        }
    }
};

/// Multi-progress bar manager for tracking multiple items
pub const MultiProgressBar = struct {
    allocator: std.mem.Allocator,
    bars: std.ArrayList(*ProgressBar),
    writer: std.io.AnyWriter,
    last_render_count: usize,

    const Self = @This();

    /// Initialize multi-progress bar
    pub fn init(allocator: std.mem.Allocator, writer: std.io.AnyWriter) Self {
        return .{
            .allocator = allocator,
            .bars = std.ArrayList(*ProgressBar).init(allocator),
            .writer = writer,
            .last_render_count = 0,
        };
    }

    /// Deinitialize
    pub fn deinit(self: *Self) void {
        self.bars.deinit();
    }

    /// Add a progress bar
    pub fn addBar(self: *Self, bar: *ProgressBar) !void {
        try self.bars.append(bar);
        bar.update_interval_ms = 0; // We'll control rendering
    }

    /// Render all bars
    pub fn render(self: *Self) !void {
        // Move cursor up for previous bars
        if (self.last_render_count > 0) {
            try self.writer.print("\x1b[{d}A", .{self.last_render_count});
        }

        for (self.bars.items) |bar| {
            try bar.render();
            try self.writer.print("\n", .{});
        }

        self.last_render_count = self.bars.items.len;
    }
};

/// Spinner for indeterminate progress
pub const Spinner = struct {
    frames: []const u8,
    current_frame: usize,
    interval_ms: i64,
    last_update: i64,
    writer: std.io.AnyWriter,
    message: []const u8,
    done: bool,

    const Self = @This();

    /// Default spinner frames
    pub const default_frames = "|/-\\";

    /// Initialize spinner
    pub fn init(writer: std.io.AnyWriter, message: []const u8) Self {
        return .{
            .frames = default_frames,
            .current_frame = 0,
            .interval_ms = 100,
            .last_update = 0,
            .writer = writer,
            .message = message,
            .done = false,
        };
    }

    /// Initialize spinner with custom frames
    pub fn initWithFrames(writer: std.io.AnyWriter, message: []const u8, frames: []const u8) Self {
        return .{
            .frames = frames,
            .current_frame = 0,
            .interval_ms = 100,
            .last_update = 0,
            .writer = writer,
            .message = message,
            .done = false,
        };
    }

    /// Update spinner
    pub fn tick(self: *Self) !void {
        if (self.done) return;

        const now = std.time.milliTimestamp();
        if (now - self.last_update < self.interval_ms) return;
        self.last_update = now;

        try self.writer.print("\r\x1b[2K{s} {s}", .{ self.frames[self.current_frame..][0..1], self.message });
        
        self.current_frame = (self.current_frame + 1) % self.frames.len;
    }

    /// Complete spinner
    pub fn complete(self: *Self, final_message: []const u8) !void {
        self.done = true;
        try self.writer.print("\r\x1b[2K{s}\n", .{final_message});
    }
};

// ============================================================================
// Tests
// ============================================================================

test "ProgressBar initialization" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    const bar = ProgressBar.init(std.testing.allocator, 100, writer, .{});
    try std.testing.expectEqual(@as(usize, 100), bar.total);
    try std.testing.expectEqual(@as(usize, 0), bar.current);
    try std.testing.expectEqual(@as(usize, 40), bar.options.width);
}

test "ProgressBar percentage calculation" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var bar = ProgressBar.init(std.testing.allocator, 100, writer, .{});
    try std.testing.expectEqual(@as(usize, 0), bar.percentage());
    
    bar.current = 50;
    try std.testing.expectEqual(@as(usize, 50), bar.percentage());
    
    bar.current = 100;
    try std.testing.expectEqual(@as(usize, 100), bar.percentage());
}

test "ProgressBar percentage with non-100 total" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var bar = ProgressBar.init(std.testing.allocator, 250, writer, .{});
    _ = &bar; // force mutation
    bar.current = 125;
    try std.testing.expectEqual(@as(usize, 50), bar.percentage());
}

test "ProgressBar zero total returns 100%" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    const bar = ProgressBar.init(std.testing.allocator, 0, writer, .{});
    try std.testing.expectEqual(@as(usize, 100), bar.percentage());
}

test "ProgressBar update respects max" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var bar = ProgressBar.init(std.testing.allocator, 100, writer, .{});
    bar.start_time = std.time.milliTimestamp();
    
    try bar.update(150);
    try std.testing.expectEqual(@as(usize, 100), bar.current);
}

test "ProgressBar custom options" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    const bar = ProgressBar.init(std.testing.allocator, 100, writer, .{
        .width = 20,
        .fill_char = '#',
        .empty_char = '.',
        .prefix = "Processing",
        .show_count = true,
    });
    
    try std.testing.expectEqual(@as(usize, 20), bar.options.width);
    try std.testing.expectEqual(@as(u8, '#'), bar.options.fill_char);
    try std.testing.expectEqual(@as(u8, '.'), bar.options.empty_char);
}

test "Spinner initialization" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    const spinner = Spinner.init(writer, "Loading...");
    try std.testing.expectEqualStrings("|/-\\", spinner.frames);
    try std.testing.expectEqual(@as(usize, 0), spinner.current_frame);
    try std.testing.expectEqualStrings("Loading...", spinner.message);
}

test "Spinner custom frames" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    const spinner = Spinner.initWithFrames(writer, "Working", "⣾⣽⣻⢿⡿⣟⣯⣷");
    try std.testing.expectEqualStrings("⣾⣽⣻⢿⡿⣟⣯⣷", spinner.frames);
    try std.testing.expectEqualStrings("Working", spinner.message);
}

test "ProgressBar elapsed time" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var bar = ProgressBar.init(std.testing.allocator, 100, writer, .{});
    _ = &bar; // force mutation
    try std.testing.expectEqual(@as(i64, 0), bar.elapsedMs());
    
    bar.start_time = std.time.milliTimestamp() - 5000;
    const elapsed = bar.elapsedMs();
    try std.testing.expect(elapsed >= 5000);
}

test "ProgressBar ETA calculation" {
    var buffer: [1024]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var bar = ProgressBar.init(std.testing.allocator, 100, writer, .{});
    
    // No progress, no ETA
    try std.testing.expectEqual(@as(i64, 0), bar.etaMs());
    
    // Half done after 1 second = 1 second remaining
    bar.start_time = std.time.milliTimestamp() - 1000;
    bar.current = 50;
    const eta = bar.etaMs();
    // Should be approximately 1 second (1000ms), allow some tolerance
    try std.testing.expect(eta > 500 and eta < 2000);
}

test "MultiProgressBar initialization" {
    const allocator = std.testing.allocator;
    var buffer: [2048]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var multi = MultiProgressBar.init(allocator, writer);
    defer multi.deinit();
    
    try std.testing.expectEqual(@as(usize, 0), multi.bars.items.len);
}

test "MultiProgressBar addBar" {
    const allocator = std.testing.allocator;
    var buffer: [2048]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buffer);
    const writer = stream.writer().any();
    
    var multi = MultiProgressBar.init(allocator, writer);
    defer multi.deinit();
    
    var bar1 = ProgressBar.init(allocator, 100, writer, .{});
    var bar2 = ProgressBar.init(allocator, 50, writer, .{});
    
    try multi.addBar(&bar1);
    try multi.addBar(&bar2);
    
    try std.testing.expectEqual(@as(usize, 2), multi.bars.items.len);
}