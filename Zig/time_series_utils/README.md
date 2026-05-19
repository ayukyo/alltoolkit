# Time Series Utils (Zig)

A comprehensive time series analysis library for Zig with zero external dependencies.

## Features

- **Moving Averages**: Simple (SMA), Exponential (EMA), Weighted (WMA)
- **Trend Detection**: Linear regression-based trend analysis
- **Difference Operations**: First difference, seasonal difference
- **Statistical Functions**: Rolling standard deviation, cumulative sum, percentage change
- **Data Structures**: Time series data point structure

## Usage

### Simple Moving Average (SMA)

```zig
const std = @import("std");
const time_series = @import("time_series.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const data = [_]f64{ 10, 12, 15, 14, 16, 18, 20, 19, 22, 25 };
    const sma = try time_series.simpleMovingAverage(allocator, &data, 3);
    defer allocator.free(sma);

    // sma[2] = (10 + 12 + 15) / 3 = 12.33
    // sma[3] = (12 + 15 + 14) / 3 = 13.67
}
```

### Exponential Moving Average (EMA)

```zig
const data = [_]f64{ 10, 12, 15, 14, 16, 18, 20, 19, 22, 25 };
const ema = try time_series.exponentialMovingAverage(allocator, &data, 5);
defer allocator.free(ema);

// EMA gives more weight to recent values
// Multiplier = 2 / (period + 1) = 2/6 = 0.333
```

### Trend Detection

```zig
const upward_data = [_]f64{ 10, 12, 14, 16, 18, 20 };
const trend = time_series.detectTrend(&upward_data);
// trend == .upward

const trend_str = trend.toString(); // "Upward"
```

### Difference Operations

```zig
// First difference (discrete derivative)
const data = [_]f64{ 10, 15, 13, 18, 20 };
const differences = try time_series.diff(allocator, &data);
defer allocator.free(differences);
// differences = [5, -2, 5, 2]

// Seasonal difference with lag
const seasonal = [_]f64{ 10, 20, 30, 15, 25, 35 };
const seasonal_diff = try time_series.seasonalDiff(allocator, &seasonal, 3);
// seasonal_diff = [5, 5, 5] (compare positions 3-0, 4-1, 5-2)
```

### Percentage Change

```zig
const prices = [_]f64{ 100, 110, 99, 99, 121 };
const pct = try time_series.pctChange(allocator, &prices);
defer allocator.free(pct);
// pct = [0.10, -0.10, 0.00, 0.222]
// Meaning: +10%, -10%, 0%, +22.2%
```

### Rolling Standard Deviation

```zig
const data = [_]f64{ 10, 12, 14, 16, 18, 20 };
const rolling_std = try time_series.rollingStd(allocator, &data, 3);
defer allocator.free(rolling_std);
// rolling_std[2] = std([10, 12, 14]) = 1.633
```

### Weighted Moving Average (WMA)

```zig
const data = [_]f64{ 10, 20, 30 };
const wma = try time_series.weightedMovingAverage(allocator, &data, 3);
defer allocator.free(wma);
// wma[2] = (10*1 + 20*2 + 30*3) / (1+2+3) = 130/6 = 21.67
// Most recent value has highest weight
```

### Cumulative Sum

```zig
const data = [_]f64{ 1, 2, 3, 4, 5 };
const cumsum = try time_series.cumsum(allocator, &data);
defer allocator.free(cumsum);
// cumsum = [1, 3, 6, 10, 15]
```

## API Reference

### Types

| Type | Description |
|------|-------------|
| `DataPoint` | Struct with `timestamp: i64` and `value: f64` |
| `Trend` | Enum: `.upward`, `.downward`, `.sideways` |

### Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `simpleMovingAverage` | allocator, data, window | []f64 | SMA with specified window |
| `exponentialMovingAverage` | allocator, data, period | []f64 | EMA with specified period |
| `weightedMovingAverage` | allocator, data, window | []f64 | WMA (linear weights) |
| `detectTrend` | data | Trend | Detect trend direction |
| `diff` | allocator, data | []f64 | First difference |
| `seasonalDiff` | allocator, data, lag | []f64 | Seasonal difference |
| `cumsum` | allocator, data | []f64 | Cumulative sum |
| `pctChange` | allocator, data | []f64 | Percentage change |
| `rollingStd` | allocator, data, window | []f64 | Rolling standard deviation |

## Building & Testing

```bash
# Run tests
zig test time_series.zig

# Build as library
zig build
```

## Algorithm Details

### Simple Moving Average (SMA)
Calculates the unweighted mean of the previous `n` data points.

```
SMA[i] = (data[i-n+1] + ... + data[i]) / n
```

### Exponential Moving Average (EMA)
Uses exponential weighting, giving more importance to recent data.

```
EMA[i] = α * data[i] + (1 - α) * EMA[i-1]
α = 2 / (period + 1)
```

### Weighted Moving Average (WMA)
Linear weighting where recent values have higher weights.

```
WMA[i] = (1*data[i-n+1] + 2*data[i-n+2] + ... + n*data[i]) / (1+2+...+n)
```

### Trend Detection
Uses linear regression to calculate slope, then determines trend based on relative slope magnitude.

## License

MIT License