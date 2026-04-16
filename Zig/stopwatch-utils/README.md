# Stopwatch Utils

A high-precision timing utility library for Zig with zero external dependencies.

## Features

- **High-Resolution Stopwatch**: Nanosecond precision timing with start/stop/pause/resume
- **Lap Timing**: Record and analyze lap times with best/worst/average statistics
- **Countdown Timer**: Precise countdown with pause/resume support
- **Duration Utilities**: Rich duration type with arithmetic operations
- **Time Formatting**: Multiple output formats (HMS, compact, ISO 8601)
- **Timestamp Helpers**: Unix timestamp conversion and duration calculation
- **Zero Dependencies**: Uses only Zig standard library

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .stopwatch_utils = .{
        .url = "https://github.com/ayukyo/alltoolkit/archive/refs/heads/main.tar.gz",
        .hash = "...",
    },
},
```

Or clone directly:

```bash
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Zig/stopwatch-utils
```

## Usage

### Basic Stopwatch

```zig
const std = @import("std");
const stopwatch_utils = @import("stopwatch-utils");

pub fn main() !void {
    var sw = stopwatch_utils.Stopwatch.init(allocator);
    defer sw.deinit();

    // Start timing
    sw.start();
    
    // Do some work...
    doWork();
    
    // Record a lap
    const lap1 = try sw.lap();
    
    // More work...
    moreWork();
    
    // Stop and get total time
    const elapsed = sw.stop();
    std.debug.print("Total: {}ms\n", .{elapsed.totalMillis()});
}
```

### Pause and Resume

```zig
var sw = stopwatch_utils.Stopwatch.init(allocator);
defer sw.deinit();

sw.start();
doWork();

sw.pause();  // Time stops counting
sleep(100);  // This time is not measured
sw.resume(); // Time continues from where it left off

doMoreWork();
const elapsed = sw.stop();
```

### Lap Timing

```zig
var sw = stopwatch_utils.Stopwatch.init(allocator);
defer sw.deinit();

sw.start();

for (0..10) |_| {
    doIteration();
    _ = try sw.lap();
}

// Get statistics
const best = sw.bestLap().?;    // Fastest lap
const worst = sw.worstLap().?;  // Slowest lap
const avg = sw.averageLap().?;  // Average lap time

std.debug.print("Best: {}ms\n", .{best.totalMillis()});
std.debug.print("Worst: {}ms\n", .{worst.totalMillis()});
std.debug.print("Average: {}ms\n", .{avg.totalMillis()});
```

### Countdown Timer

```zig
var timer = stopwatch_utils.CountdownTimer.init(
    stopwatch_utils.Duration.fromSeconds(60)
);

timer.start();

while (!timer.isComplete()) {
    const remaining = timer.remaining();
    std.debug.print("Remaining: {}s\n", .{remaining.totalSeconds()});
    sleep(1000);
}

std.debug.print("Time's up!\n", .{});
```

### Duration Operations

```zig
const d1 = stopwatch_utils.Duration.fromSeconds(90);
const d2 = stopwatch_utils.Duration.fromMinutes(2);

// Arithmetic
const sum = d1.add(d2);           // 3m 30s
const diff = d1.sub(d2);          // -30s
const doubled = d1.mul(2);        // 3m
const halved = d1.div(2);         // 45s

// Conversions
std.debug.print("Seconds: {}\n", .{d1.totalSeconds()});    // 90
std.debug.print("Minutes: {d}\n", .{d1.totalMinutes()});  // 1.5

// Check state
if (d1.isPositive()) {
    std.debug.print("Duration is positive\n", .{});
}
```

### Time Formatting

```zig
const d = stopwatch_utils.Duration.fromSeconds(3661)
    .add(stopwatch_utils.Duration.fromMillis(234));

// HMS format: 01:01:01.234
const hms = try stopwatch_utils.TimeFormatter.formatHMS(allocator, d);
defer allocator.free(hms);

// Compact format: 1h1m1.234s
const compact = try stopwatch_utils.TimeFormatter.formatCompact(allocator, d);
defer allocator.free(compact);

// ISO 8601 format: PT1H1M1.234000S
const iso = try stopwatch_utils.TimeFormatter.formatISO8601(allocator, d);
defer allocator.free(iso);
```

### Timestamps

```zig
const start = stopwatch_utils.Timestamp.now();

// Do work...
doWork();

const end = stopwatch_utils.Timestamp.now();
const elapsed = end.since(start);

std.debug.print("Unix seconds: {}\n", .{start.unixSeconds()});
std.debug.print("Unix millis: {}\n", .{start.unixMillis()});
std.debug.print("Elapsed: {}ms\n", .{elapsed.totalMillis()});
```

### Sleep Utilities

```zig
// Sleep for specific durations
stopwatch_utils.Sleep.seconds(2);
stopwatch_utils.Sleep.millis(500);
stopwatch_utils.Sleep.micros(1000);
stopwatch_utils.Sleep.nanos(100);

// Or use Duration directly
const nap = stopwatch_utils.Duration.fromMillis(100);
stopwatch_utils.Sleep.duration(nap);
```

## API Reference

### Types

| Type | Description |
|------|-------------|
| `Timestamp` | High-resolution timestamp in nanoseconds |
| `Duration` | Time duration with nanosecond precision |
| `Stopwatch` | Multi-lap stopwatch with pause/resume |
| `CountdownTimer` | Countdown timer with completion detection |
| `TimeFormatter` | Time formatting utilities |

### Duration Methods

| Method | Description |
|--------|-------------|
| `fromNanos(ns)` | Create from nanoseconds |
| `fromMicros(us)` | Create from microseconds |
| `fromMillis(ms)` | Create from milliseconds |
| `fromSeconds(s)` | Create from seconds |
| `fromMinutes(m)` | Create from minutes |
| `fromHours(h)` | Create from hours |
| `totalNanos()` | Get total nanoseconds |
| `totalMicros()` | Get total microseconds |
| `totalMillis()` | Get total milliseconds |
| `totalSeconds()` | Get total seconds (f64) |
| `toHMSN()` | Convert to hours/minutes/seconds/nanos |
| `add(d)`, `sub(d)` | Arithmetic operations |
| `mul(n)`, `div(n)` | Scalar operations |

### Stopwatch Methods

| Method | Description |
|--------|-------------|
| `init(allocator)` | Create new stopwatch |
| `deinit()` | Free resources |
| `start()` | Start/resume timing |
| `pause()` | Pause timing |
| `resume()` | Resume from pause |
| `stop()` | Stop timing and return elapsed |
| `reset()` | Reset to idle state |
| `lap()` | Record lap time |
| `elapsed()` | Get current elapsed time |
| `getLaps()` | Get all lap times |
| `bestLap()` | Get fastest lap |
| `worstLap()` | Get slowest lap |
| `averageLap()` | Get average lap time |
| `isRunning()` | Check if running |

## Building

```bash
# Build library
zig build

# Run tests
zig build test

# Run example
zig build example

# Run benchmarks
zig build bench
```

## Performance

Benchmarks on a typical machine:

| Operation | Time |
|-----------|------|
| Timestamp.now() | ~25 ns |
| Duration.add() | ~1 ns |
| Duration.totalMillis() | ~3 ns |
| Stopwatch.elapsed() | ~30 ns |
| Stopwatch.lap() | ~150 ns |
| formatHMS() | ~800 ns |
| formatCompact() | ~600 ns |

## License

MIT License - Part of the AllToolkit project.