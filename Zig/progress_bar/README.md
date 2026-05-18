# Progress Bar Utils (Zig)

A terminal progress bar library for Zig with zero external dependencies. Supports single progress bars, multi-progress bars, and spinners.

## Features

- 📊 **Progress Bar** - Customizable progress bars with percentage, count, elapsed time, and ETA
- 🎯 **Multi-Progress** - Track multiple concurrent progress bars
- ⏳ **Spinner** - Indeterminate progress indicator with custom frames
- 🎨 **Customizable** - Full control over characters, width, prefix, suffix
- 📦 **Zero Dependencies** - Uses only Zig standard library

## Quick Start

```zig
const std = @import("std");
const progress_bar = @import("progress_bar");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    
    var bar = progress_bar.ProgressBar.init(
        std.heap.page_allocator,
        100,
        stdout.any(),
        .{},
    );
    
    try bar.start();
    
    for (0..100) |_| {
        std.time.sleep(20_000_000); // 20ms
        try bar.increment();
    }
    
    try bar.finish();
}
```

## API Reference

### ProgressBar

The main progress bar type.

#### Options

```zig
pub const ProgressBarOptions = struct {
    width: usize = 40,           // Bar width in characters
    fill_char: u8 = '=',         // Character for filled portion
    empty_char: u8 = '-',        // Character for empty portion
    left_bracket: u8 = '[',      // Left bracket character
    right_bracket: u8 = ']',     // Right bracket character
    show_percentage: bool = true, // Show percentage
    show_count: bool = false,    // Show count (current/total)
    show_time: bool = false,     // Show elapsed time
    show_eta: bool = false,      // Show estimated remaining time
    prefix: []const u8 = "",      // Text before bar
    suffix: []const u8 = "",      // Text after bar
};
```

#### Methods

- `init(allocator, total, writer, options)` - Create a new progress bar
- `start()` - Start the progress bar
- `increment()` - Advance by 1
- `update(current)` - Set to specific value
- `finish()` - Complete and print newline
- `percentage()` - Get current percentage (0-100)
- `elapsedMs()` - Get elapsed time in milliseconds
- `etaMs()` - Get estimated remaining time in milliseconds

### MultiProgressBar

Track multiple progress bars simultaneously.

```zig
var multi = progress_bar.MultiProgressBar.init(allocator, writer.any());
defer multi.deinit();

var bar1 = progress_bar.ProgressBar.init(allocator, 100, writer.any(), .{ .prefix = "Task 1" });
var bar2 = progress_bar.ProgressBar.init(allocator, 50, writer.any(), .{ .prefix = "Task 2" });

try multi.addBar(&bar1);
try multi.addBar(&bar2);

bar1.start_time = std.time.milliTimestamp();
bar2.start_time = std.time.milliTimestamp();

while (working) {
    // Update bars...
    try multi.render();
}
```

### Spinner

Indeterminate progress indicator for unknown duration tasks.

```zig
var spinner = progress_bar.Spinner.init(stdout.any(), "Loading...");

while (!done) {
    try spinner.tick();
    // Do work...
}

try spinner.complete("✓ Done!");
```

Custom frames:

```zig
var spinner = progress_bar.Spinner.initWithFrames(
    stdout.any(),
    "Processing",
    "⣾⣽⣻⢿⡿⣟⣯⣷", // Unicode braille frames
);
```

## Examples

### Full-Featured Bar

```zig
var bar = progress_bar.ProgressBar.init(
    allocator,
    1000,
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
```

Output:
```
Downloading [████████████████░░░░░░░░░░░░]  55% (550/1000) [00:12] ETA: 10s
```

## Building

```bash
# Run tests
zig build test

# Run examples
zig build example
```

## License

MIT