# Backoff Utils

A comprehensive Go package providing backoff algorithms for retry mechanisms with zero external dependencies.

## Features

- **Multiple Backoff Strategies**
  - Exponential Backoff
  - Linear Backoff
  - Constant Backoff
  - Full Jitter Backoff
  - Equal Jitter Backoff
  - Decorrelated Jitter Backoff

- **Advanced Features**
  - Context cancellation support
  - Maximum retry limits
  - Timeout support
  - Custom retryable error detection
  - Generic result support
  - Thread-safe implementations

## Installation

```bash
go get github.com/ayukyo/alltoolkit/backoff_utils
```

## Quick Start

### Basic Exponential Backoff

```go
package main

import (
    "context"
    "fmt"
    "time"
    
    "github.com/ayukyo/alltoolkit/backoff_utils"
)

func main() {
    config := backoff_utils.Config{
        BaseDelay:  100 * time.Millisecond,
        MaxDelay:   30 * time.Second,
        Multiplier: 2.0,
        MaxRetries: 5,
    }
    
    backoff := backoff_utils.NewExponentialBackoff(config)
    
    for i := 0; i < 5; i++ {
        delay := backoff.Next(i)
        fmt.Printf("Attempt %d: %v\n", i, delay)
    }
}
```

### Using Retrier

```go
package main

import (
    "context"
    "errors"
    "fmt"
    "time"
    
    "github.com/ayukyo/alltoolkit/backoff_utils"
)

func main() {
    config := backoff_utils.Config{
        BaseDelay:  100 * time.Millisecond,
        MaxDelay:   5 * time.Second,
        MaxRetries: 3,
    }
    
    backoff := backoff_utils.NewExponentialBackoff(config)
    retrier := backoff_utils.NewRetrier(backoff, config)
    
    err := retrier.Do(context.Background(), func() error {
        // Your operation here
        return nil
    })
    
    if err != nil {
        fmt.Printf("Operation failed: %v\n", err)
    }
}
```

### With Timeout

```go
err := retrier.RetryWithTimeout(func() error {
    // Your operation here
    return nil
}, 10*time.Second)
```

### With Result

```go
result, err := backoff_utils.DoWithResult(context.Background(), backoff, config, func() (string, error) {
    // Your operation that returns a result
    return "success", nil
})
```

### With Context Cancellation

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

err := retrier.Do(ctx, func() error {
    // Your operation here
    return nil
})
```

### Custom Retryable Check

```go
isRetryable := func(err error) bool {
    // Only retry on network errors
    var netErr net.Error
    return errors.As(err, &netErr)
}

err := retrier.DoWithRetryableCheck(ctx, fn, isRetryable, 5)
```

## Backoff Strategies

### 1. Exponential Backoff

Doubles the delay after each attempt:

```
Delay = BaseDelay * (Multiplier ^ Attempt)
```

```go
backoff := backoff_utils.NewExponentialBackoff(backoff_utils.Config{
    BaseDelay:  100 * time.Millisecond,
    MaxDelay:   30 * time.Second,
    Multiplier: 2.0,
})
```

### 2. Linear Backoff

Increases delay linearly:

```
Delay = BaseDelay * (Attempt + 1)
```

```go
backoff := backoff_utils.NewLinearBackoff(backoff_utils.Config{
    BaseDelay: 100 * time.Millisecond,
    MaxDelay:  10 * time.Second,
})
```

### 3. Constant Backoff

Always returns the same delay:

```go
backoff := backoff_utils.NewConstantBackoff(500 * time.Millisecond)
```

### 4. Full Jitter Backoff

Random delay between 0 and calculated delay:

```go
backoff := backoff_utils.NewFullJitterBackoff(backoff_utils.Config{
    BaseDelay:  100 * time.Millisecond,
    MaxDelay:   30 * time.Second,
    Multiplier: 2.0,
})
```

### 5. Equal Jitter Backoff

Half the delay plus random jitter:

```
Delay = (CalculatedDelay / 2) + Random(0, CalculatedDelay / 2)
```

```go
backoff := backoff_utils.NewEqualJitterBackoff(backoff_utils.Config{
    BaseDelay:  100 * time.Millisecond,
    MaxDelay:   30 * time.Second,
    Multiplier: 2.0,
})
```

### 6. Decorrelated Jitter Backoff

Random delay between base and last delay × multiplier:

```go
backoff := backoff_utils.NewDecorrelatedJitterBackoff(backoff_utils.Config{
    BaseDelay:  100 * time.Millisecond,
    MaxDelay:   30 * time.Second,
    Multiplier: 2.0,
})
```

## Configuration

```go
type Config struct {
    BaseDelay      time.Duration // Initial delay
    MaxDelay       time.Duration // Maximum delay cap
    Multiplier     float64       // Exponential multiplier
    JitterFraction float64       // Jitter fraction (0.0 to 1.0)
    MaxRetries     int           // Maximum retry attempts (0 = unlimited)
}
```

### Default Configuration

```go
config := backoff_utils.DefaultConfig()
// BaseDelay:      100ms
// MaxDelay:       30s
// Multiplier:     2.0
// JitterFraction: 0.0
// MaxRetries:     5
```

## Utility Functions

### BackoffCalculator

```go
calc := backoff_utils.BackoffCalculator{}

// Calculate exponential backoff
delay := calc.CalculateExponential(100*time.Millisecond, 2.0, 3)

// Calculate linear backoff
delay := calc.CalculateLinear(100*time.Millisecond, 3)

// Cap delay at maximum
delay := calc.CapDelay(5*time.Second, 3*time.Second)

// Add jitter
delay = calc.CalculateWithJitter(delay, 0.3, nil)
```

### SleepWithContext

```go
// Sleeps for 1 second, respecting context cancellation
err := backoff_utils.SleepWithContext(ctx, 1*time.Second)
if err != nil {
    // Context was cancelled
}
```

## Error Handling

```go
var retryErr *backoff_utils.RetryError
if errors.As(err, &retryErr) {
    fmt.Printf("Failed after %d attempts: %v\n", retryErr.Attempt, retryErr.Err)
    
    if errors.Is(retryErr.Err, backoff_utils.ErrMaxRetriesExceeded) {
        // Max retries exceeded
    }
    if errors.Is(retryErr.Err, backoff_utils.ErrContextCanceled) {
        // Context was cancelled
    }
}
```

## Best Practices

1. **Use Jitter**: Always use jitter to prevent thundering herd problems
2. **Set MaxDelay**: Prevent excessive delays
3. **Use Context**: Support cancellation for graceful shutdowns
4. **Custom Retryable Checks**: Distinguish between retryable and permanent errors

## Thread Safety

All backoff strategies are thread-safe and can be used concurrently:

```go
var wg sync.WaitGroup
backoff := backoff_utils.NewExponentialBackoff(config)

for i := 0; i < 10; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        delay := backoff.Next(0)
        // Use delay...
    }()
}
wg.Wait()
```

## License

MIT License