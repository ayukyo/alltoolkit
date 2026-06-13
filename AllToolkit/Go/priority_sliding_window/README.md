# Priority Sliding Window Rate Limiter

A multi-window, priority-aware rate limiter for Go with support for both sliding and fixed window models, burst allowances, and per-priority independent counters.

## Features

- **Two Window Models**: Sliding window (precise, O(windowSlots) memory) or Fixed window (O(1) memory, resets at boundary)
- **Priority Tiers**: 5 built-in levels (Critical → Bulk); unknown priorities are unlimited
- **Burst Allowance**: Configurable extra headroom above the base limit
- **Reserve/Confirm Pattern**: Async acknowledgment for delayed operations
- **Dynamic Limit Updates**: Adjust limits without restarting
- **Peak Tracking**: Observe traffic peaks for capacity planning
- **Adaptive Memory**: Epsilon-slack garbage collection for sliding windows
- **Zero Dependencies**: Only Go standard library

## Quick Start

```go
package main

import (
    "fmt"
    "time"

    "github.com/ayukyo/alltoolkit/Go/priority_sliding_window"
)

func main() {
    limits := map[int]int{
        priority_sliding_window.PriorityCritical: 1000,
        priority_sliding_window.PriorityHigh:   100,
        priority_sliding_window.PriorityMedium: 50,
        priority_sliding_window.PriorityLow:     10,
    }

    rl, err := priority_sliding_window.New(limits, time.Minute)
    if err != nil {
        panic(err)
    }
    defer rl.Stop()

    // Non-blocking check
    if rl.Allow(priority_sliding_window.PriorityHigh) {
        fmt.Println("Request allowed")
    }

    // Reserve for async confirmation
    r := rl.Reserve(priority_sliding_window.PriorityHigh)
    if r.Allowed() {
        // ... do work ...
        r.Confirm()
    }

    // Check stats
    stats := rl.Stats(priority_sliding_window.PriorityHigh)
    fmt.Printf("Remaining: %d / %d\n", stats.Remaining, stats.Limit)
}
```

## Configuration Options

| Option | Description |
|--------|-------------|
| `Limits` | Per-priority operation limits per window |
| `WindowDuration` | Length of the rate window |
| `TimeQuantum` | Granularity for sliding window buckets |
| `WindowType` | `SlidingWindow` or `FixedWindow` |
| `BurstAllowance` | Extra capacity as fraction (e.g., 0.2 = 20%) |
| `MinBurst` | Absolute minimum burst even for small limits |
| `CleanupInterval` | How often to purge expired buckets |

## License

MIT