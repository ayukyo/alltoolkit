const std = @import("std");
const progress_bar = @import("progress_bar");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    
    // Example 1: Basic progress bar
    try stdout.print("\n=== Basic Progress Bar ===\n", .{});
    
    var basic_bar = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        100,
        stdout.any(),
        .{},
    );
    try basic_bar.start();
    
    var i: usize = 0;
    while (i < 100) : (i += 1) {
        std.time.sleep(20_000_000); // 20ms
        try basic_bar.increment();
    }
    try basic_bar.finish();

    // Example 2: Progress bar with all options
    try stdout.print("\n=== Full-Featured Progress Bar ===\n", .{});
    
    var full_bar = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        50,
        stdout.any(),
        .{
            .width = 30,
            .fill_char = '█',
            .empty_char = '░',
            .prefix = "Downloading",
            .show_percentage = true,
            .show_count = true,
            .show_time = true,
            .show_eta = true,
        },
    );
    try full_bar.start();
    
    i = 0;
    while (i < 50) : (i += 1) {
        std.time.sleep(40_000_000); // 40ms
        try full_bar.increment();
    }
    try full_bar.finish();

    // Example 3: Custom styled progress bar
    try stdout.print("\n=== Custom Styled Progress Bar ===\n", .{});
    
    var styled_bar = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        20,
        stdout.any(),
        .{
            .width = 25,
            .fill_char = '▶',
            .empty_char = '·',
            .left_bracket = '|',
            .right_bracket = '|',
            .prefix = "Processing",
            .suffix = "items",
        },
    );
    try styled_bar.start();
    
    i = 0;
    while (i < 20) : (i += 1) {
        std.time.sleep(50_000_000); // 50ms
        try styled_bar.increment();
    }
    try styled_bar.finish();

    // Example 4: Spinner
    try stdout.print("\n=== Spinner Example ===\n", .{});
    
    var spinner = progress_bar.Spinner.init(stdout.any(), "Loading data...");
    
    i = 0;
    while (i < 30) : (i += 1) {
        std.time.sleep(50_000_000); // 50ms
        try spinner.tick();
    }
    try spinner.complete("✓ Loading complete!\n");

    // Example 5: Spinner with custom frames
    try stdout.print("\n=== Custom Spinner ===\n", .{});
    
    var custom_spinner = progress_bar.Spinner.initWithFrames(
        stdout.any(),
        "Installing dependencies",
        "⣾⣽⣻⢿⡿⣟⣯⣷",
    );
    
    i = 0;
    while (i < 40) : (i += 1) {
        std.time.sleep(40_000_000); // 40ms
        try custom_spinner.tick();
    }
    try custom_spinner.complete("✓ Dependencies installed!\n");

    // Example 6: Multi-progress bars
    try stdout.print("\n=== Multi-Progress Bar ===\n", .{});
    
    var multi = progress_bar.MultiProgressBar.init(std.heap.page_allocator, stdout.any());
    defer multi.deinit();
    
    var bar1 = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        30,
        stdout.any(),
        .{ .prefix = "Task 1", .width = 20 },
    );
    var bar2 = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        50,
        stdout.any(),
        .{ .prefix = "Task 2", .width = 20 },
    );
    var bar3 = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        40,
        stdout.any(),
        .{ .prefix = "Task 3", .width = 20 },
    );
    
    bar1.start_time = std.time.milliTimestamp();
    bar2.start_time = std.time.milliTimestamp();
    bar3.start_time = std.time.milliTimestamp();
    
    try multi.addBar(&bar1);
    try multi.addBar(&bar2);
    try multi.addBar(&bar3);
    
    i = 0;
    while (i < 50) : (i += 1) {
        std.time.sleep(50_000_000); // 50ms
        
        if (i < 30) try bar1.increment();
        if (i < 50) try bar2.increment();
        if (i < 40) try bar3.increment();
        
        try multi.render();
    }
    
    bar1.current = bar1.total;
    bar2.current = bar2.total;
    bar3.current = bar3.total;
    try multi.render();
    
    try stdout.print("\n✓ All tasks complete!\n\n", .{});
}