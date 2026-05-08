# Countdown Utils

A comprehensive Go package for countdown timers, duration formatting, and working day calculations. Zero external dependencies.

## Features

- **Duration Parsing & Formatting**: Parse and format durations in multiple styles
- **Countdown Timers**: Create countdowns to target times with progress tracking
- **Timer Control**: Start, pause, resume, reset timers with callbacks
- **Working Days**: Calculate working days (Mon-Fri) between dates
- **Custom Formats**: Flexible format strings with placeholders

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/countdown_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "time"
    "github.com/ayukyo/alltoolkit/Go/countdown_utils"
)

func main() {
    // Create a countdown to a target time
    target := time.Now().Add(2 * time.Hour)
    countdown := countdown_utils.NewCountdown(target)
    
    // Format remaining time
    fmt.Println(countdown_utils.FormatCountdown(countdown.Remaining))
    // Output: 2h 0m 0s
    
    // Compact format (like digital clock)
    fmt.Println(countdown_utils.FormatCountdownCompact(countdown.Remaining))
    // Output: 02:00:00
    
    // Long format (human readable)
    fmt.Println(countdown_utils.FormatCountdownLong(countdown.Remaining))
    // Output: 2 hours and 0 seconds
}
```

## Duration Formatting

```go
// Parse a duration into components
d := countdown_utils.ParseDuration(3*24*time.Hour + 5*time.Hour + 30*time.Minute)

// Multiple format options
fmt.Println(d.Format())         // 3d 5h 30m 0s
fmt.Println(d.FormatCompact())  // 3:05:30:00
fmt.Println(d.FormatDigital())  // 05:30:00
fmt.Println(d.FormatLong())     // 3 days, 5 hours, 30 minutes, and 0 seconds

// Custom format with placeholders
fmt.Println(d.FormatCustom("{d} days, {h} hours"))
// Output: 3 days, 5 hours

// Zero-padded format
fmt.Println(d.FormatCustom("{D} days, {H}:{M}:{S}"))
// Output: 03 days, 05:30:00
```

## Parse Duration Strings

```go
// Parse human-readable duration strings
duration, err := countdown_utils.ParseDurationString("2d 5h 30m 15s")
if err != nil {
    log.Fatal(err)
}
fmt.Println(duration) // 53h30m15s
```

## Countdown to Events

```go
// Countdown to a specific date/time
countdown := countdown_utils.CountdownTo(2025, time.December, 25, 0, 0, 0, time.UTC)

// Countdown to New Year
newYear := countdown_utils.CountdownToNewYear()

// Check if expired
if countdown.IsExpired() {
    fmt.Println("The event has passed!")
}

// Get progress
fmt.Printf("Progress: %.1f%%\n", countdown.ProgressPercent())

// Progress bar visualization
fmt.Println(countdown.FormatProgress(20)) // ████████████░░░░░░░░
```

## Working Days

```go
// Calculate working days between two dates
start := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)
end := time.Date(2024, 1, 10, 0, 0, 0, 0, time.UTC)
days := countdown_utils.WorkingDaysBetween(start, end)
fmt.Printf("Working days: %d\n", days)

// Days until a future date
future := time.Now().AddDate(0, 0, 10)
days := countdown_utils.DaysUntil(future)

// Next/Previous working day
next := countdown_utils.NextWorkingDay(time.Now())
prev := countdown_utils.PreviousWorkingDay(time.Now())

// Add working days
result := countdown_utils.AddWorkingDays(time.Now(), 5)

// Check if weekend/working day
if countdown_utils.IsWeekend(time.Now()) {
    fmt.Println("It's weekend!")
}
```

## Timer with Controls

```go
// Create a timer
timer := countdown_utils.NewTimer(5 * time.Minute)

// Set callbacks
timer.SetOnComplete(func() {
    fmt.Println("Timer completed!")
})

// Control the timer
timer.Start()
timer.Pause()
timer.Resume()
timer.Stop()
timer.Reset()

// Check remaining time
remaining := timer.GetRemaining()
fmt.Println(countdown_utils.FormatCountdown(remaining))

// Check state
switch timer.GetState() {
case countdown_utils.TimerRunning:
    fmt.Println("Timer is running")
case countdown_utils.TimerPaused:
    fmt.Println("Timer is paused")
case countdown_utils.TimerStopped:
    fmt.Println("Timer is stopped")
case countdown_utils.TimerCompleted:
    fmt.Println("Timer is completed")
}
```

## API Reference

### Types

- `Duration` - Broken-down duration with Days, Hours, Minutes, Seconds
- `Countdown` - Countdown to a target time
- `Timer` - Controllable countdown timer
- `TimerState` - Timer states (Stopped, Running, Paused, Completed)

### Key Functions

| Function | Description |
|----------|-------------|
| `ParseDuration(d time.Duration)` | Convert to Duration struct |
| `FormatCountdown(d)` | Format as "1d 2h 3m 4s" |
| `FormatCountdownCompact(d)` | Format as "01:02:03:04" |
| `FormatCountdownLong(d)` | Format as "1 day, 2 hours..." |
| `ParseDurationString(s)` | Parse "1d2h3m4s" string |
| `NewCountdown(target)` | Create countdown to time |
| `NewTimer(duration)` | Create controllable timer |
| `WorkingDaysBetween(start, end)` | Count Mon-Fri days |
| `NextWorkingDay(t)` | Get next working day |
| `AddWorkingDays(t, n)` | Add n working days |
| `IsWeekend(t)` | Check if Sat/Sun |
| `DaysUntil(target)` | Count days to target |
| `CountdownToNewYear()` | Countdown to Jan 1 |

## Format Placeholders

Custom format placeholders:
- `{d}`, `{D}` - Days (unpadded, zero-padded)
- `{h}`, `{H}` - Hours (unpadded, zero-padded)
- `{m}`, `{M}` - Minutes (unpadded, zero-padded)
- `{s}`, `{S}` - Seconds (unpadded, zero-padded)

## Testing

```bash
go test -v
```

## License

MIT License