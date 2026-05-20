# Rolling Window Utils

A Go package providing sliding window data structures and statistical utilities with zero external dependencies.

## Features

- **RollingWindow**: Fixed-size sliding window with O(1) insert and efficient statistics
- **RollingInt**: Integer-specialized rolling window
- **ExponentialMovingAverage (EMA)**: Single-value EMA tracking
- **CumulativeSum**: Thread-safe cumulative sum tracker
- **Counter**: Simple thread-safe counter

## Installation

```bash
go get rolling_window_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "rolling_window_utils"
)

func main() {
    // Create a rolling window of size 5
    rw := rolling_window_utils.NewRollingWindow(5)
    
    // Add values
    for i := 1; i <= 7; i++ {
        rw.Add(float64(i))
    }
    
    // Window now contains: [3, 4, 5, 6, 7]
    fmt.Printf("Values: %v\n", rw.Values())
    fmt.Printf("Sum: %.0f\n", rw.Sum())
    fmt.Printf("Average: %.2f\n", rw.Average())
    
    min, _ := rw.Min()
    max, _ := rw.Max()
    fmt.Printf("Min: %.0f, Max: %.0f\n", min, max)
}
```

## API Reference

### RollingWindow

```go
// Create a new rolling window
rw := rolling_window_utils.NewRollingWindow(size int)

// Add a value (oldest value is evicted if window is full)
rw.Add(value float64)

// Get current values in insertion order
values := rw.Values()

// Basic statistics
count := rw.Count()           // Number of values in window
sum := rw.Sum()               // Sum of all values
avg := rw.Average()           // Arithmetic mean
min, ok := rw.Min()           // Minimum value
max, ok := rw.Max()           // Maximum value
rng, ok := rw.Range()         // Max - Min
variance, ok := rw.Variance() // Population variance
stdDev, ok := rw.StdDev()     // Population standard deviation
median, ok := rw.Median()     // Median value
p25, ok := rw.Percentile(25)  // 25th percentile
first, ok := rw.First()       // Oldest value
last, ok := rw.Last()         // Newest value

// Comprehensive statistics snapshot
stats, ok := rw.Stats()
// stats contains: Count, Sum, Average, Min, Max, Range, 
//                 Variance, StdDev, Median, P25, P75, P95, P99

// Window management
isFull := rw.IsFull()   // Check if window is at capacity
rw.Clear()              // Remove all values
```

### RollingInt

Integer-specialized rolling window:

```go
ri := rolling_window_utils.NewRollingInt(10)
ri.Add(42)
values := ri.Values()  // Returns []int
sum := ri.Sum()        // Returns int
```

### ExponentialMovingAverage

```go
// Create with smoothing factor (0 < alpha < 1)
ema := rolling_window_utils.NewEMA(0.3)

// Or create from period (alpha = 2 / (period + 1))
ema := rolling_window_utils.NewEMAFromPeriod(10)

ema.Add(100)
ema.Add(110)
value := ema.Value()  // Current EMA

ema.Reset()  // Clear state
initialized := ema.IsInitialized()
```

### CumulativeSum

```go
cs := rolling_window_utils.NewCumulativeSum()
cs.Add(100)
cs.Add(50)
sum := cs.Sum()      // Returns 150
oldSum := cs.Reset() // Returns 150 and resets to 0
```

### Counter

```go
c := rolling_window_utils.NewCounter()
c.Increment()     // Returns new value
c.Decrement()     // Returns new value
c.Add(10)         // Returns new value
value := c.Value()
oldValue := c.Reset()
```

## Performance

- **O(1)** insert operations
- **O(1)** min/max queries (using monotonic queues)
- **O(1)** sum and average
- **O(n)** for median and percentile (requires sorting)
- Thread-safe with read/write locks

## Use Cases

- **Real-time Analytics**: Moving averages, rates, and statistics
- **Monitoring**: Track metrics over sliding time windows
- **Finance**: Technical indicators (MA, EMA, volatility)
- **IoT**: Sensor data smoothing and analysis
- **Rate Limiting**: Count events within time windows
- **Performance Monitoring**: Request/response time tracking

## Example: Stock Price Analysis

```go
rw := rolling_window_utils.NewRollingWindow(20)
ema := rolling_window_utils.NewEMAFromPeriod(20)

prices := []float64{/* ... */}
for _, price := range prices {
    rw.Add(price)
    ema.Add(price)
    
    stats, _ := rw.Stats()
    fmt.Printf("Price: %.2f | SMA: %.2f | EMA: %.2f | Volatility: %.2f\n",
        price, stats.Average, ema.Value(), stats.StdDev)
}
```

## License

MIT License