# retry_utils

[![Go Reference](https://pkg.go.dev/badge/github.com/ayukyo/alltoolkit/Go/retry_utils.svg)](https://pkg.go.dev/github.com/ayukyo/alltoolkit/Go/retry_utils)

A comprehensive Go library for implementing retry mechanisms with exponential backoff, jitter, circuit breaker pattern, and rate limiting. Zero external dependencies.

## Features

- **Exponential Backoff**: Configurable multiplier-based backoff strategy
- **Jitter Support**: Percentage-based or fixed jitter to prevent thundering herd
- **Context Support**: Full context cancellation and timeout support
- **Circuit Breaker**: Implement the circuit breaker pattern for fault tolerance
- **Rate Limiter**: Token bucket-based rate limiting for retries
- **Error Classification**: Permanent and transient error types
- **Fluent Builder API**: Chain configuration methods for clean code
- **Callbacks**: Hooks for retry, success, and failure events
- **Thread Safe**: Safe for concurrent use

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/retry_utils
```

## Quick Start

### Basic Retry

```go
package main

import (
    "fmt"
    "time"
    retry "github.com/ayukyo/alltoolkit/Go/retry_utils"
)

func main() {
    result := retry.Do(func() error {
        // Your operation here
        return nil // or return an error
    }, retry.WithMaxAttempts(3))

    if result.Success {
        fmt.Printf("Succeeded after %d attempts\n", result.Attempts)
    } else {
        fmt.Printf("Failed after %d attempts: %v\n", result.Attempts, result.Error)
    }
}
```

### Exponential Backoff

```go
result := retry.Do(func() error {
    return someOperation()
},
    retry.WithMaxAttempts(5),
    retry.WithInitialDelay(100*time.Millisecond),
    retry.WithMaxDelay(30*time.Second),
    retry.WithMultiplier(2.0),
    retry.WithJitter(0.1), // 10% jitter
)
```

### Using the Builder Pattern

```go
result := retry.NewBuilder().
    MaxAttempts(5).
    InitialDelay(100 * time.Millisecond).
    MaxDelay(10 * time.Second).
    Multiplier(2.0).
    Jitter(0.1).
    Timeout(30 * time.Second).
    Do(func() error {
        return someOperation()
    })
```

### Context Support

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

result := retry.DoWithContext(ctx, func(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
        return performOperation(ctx)
    }
},
    retry.WithMaxAttempts(10),
    retry.WithInitialDelay(100*time.Millisecond),
)
```

## Error Handling

### Permanent vs Transient Errors

```go
import retry "github.com/ayukyo/alltoolkit/Go/retry_utils"

func someOperation() error {
    err := doSomething()
    
    if isAuthError(err) {
        // Don't retry authentication errors
        return retry.Permanent(err)
    }
    
    if isNetworkError(err) {
        // Explicitly mark as retryable
        return retry.Transient(err)
    }
    
    return err
}

// Check error types
if retry.IsPermanent(err) {
    // Handle permanent error
}

if retry.IsTransient(err) {
    // Handle transient error
}
```

### Retry-After Header Support

```go
func callAPI() error {
    resp, err := http.Get(url)
    if err != nil {
        return err
    }
    
    if resp.StatusCode == 429 {
        delay := parseRetryAfter(resp.Header.Get("Retry-After"))
        return retry.RetryAfter(errors.New("rate limited"), delay)
    }
    
    return nil
}
```

### Custom Retry Filter

```go
var (
    ErrTimeout    = errors.New("timeout")
    ErrConnection = errors.New("connection error")
)

result := retry.Do(func() error {
    return someOperation()
},
    retry.WithMaxAttempts(10),
    retry.WithRetryOn(func(err error) bool {
        // Only retry on specific errors
        return errors.Is(err, ErrTimeout) || errors.Is(err, ErrConnection)
    }),
)
```

## Callbacks

```go
result := retry.Do(func() error {
    return someOperation()
},
    retry.WithMaxAttempts(5),
    retry.WithOnRetry(func(attempt int, err error) {
        log.Printf("Retry attempt %d: %v", attempt, err)
    }),
    retry.WithOnSuccess(func(attempts int, duration time.Duration) {
        log.Printf("Succeeded after %d attempts in %v", attempts, duration)
    }),
    retry.WithOnFailure(func(attempts int, duration time.Duration, lastErr error) {
        log.Printf("Failed after %d attempts in %v: %v", attempts, duration, lastErr)
    }),
)
```

## Circuit Breaker

```go
// Create a circuit breaker: open after 5 failures, reset after 30 seconds
cb := retry.NewCircuitBreaker(5, 30*time.Second,
    retry.WithOnStateChange(func(old, new retry.State) {
        log.Printf("Circuit breaker state: %v -> %v", old, new)
    }),
    retry.WithHalfOpenMax(3), // Require 3 successes to close
)

// Execute operations through the circuit breaker
err := cb.Execute(func() error {
    return someOperation()
})

if err != nil {
    if errors.Is(err, retry.ErrCircuitOpen) {
        // Circuit is open, fail fast
        handleCircuitOpen()
    }
    handleOtherError(err)
}
```

### Circuit Breaker States

| State | Description |
|-------|-------------|
| `StateClosed` | Normal operation, requests pass through |
| `StateOpen` | Circuit is open, all requests fail immediately |
| `StateHalfOpen` | Testing if service recovered, limited requests allowed |

## Rate Limiter

```go
// Create a rate limiter: 10 retries per second, burst of 5
rl := retry.NewRateLimiter(10, 5)

if rl.Allow() {
    // Perform retry
} else {
    // Wait for permission
    err := rl.Wait(context.Background())
    if err != nil {
        // Context was cancelled
    }
}
```

## Convenience Functions

### Exponential Backoff

```go
// Simple exponential backoff with sensible defaults
result := retry.ExponentialBackoff(func() error {
    return someOperation()
}, 5, 100*time.Millisecond) // maxAttempts, initialDelay
```

### Fixed Delay

```go
// Fixed delay between retries
result := retry.FixedDelay(func() error {
    return someOperation()
}, 5, 500*time.Millisecond) // maxAttempts, delay
```

### Linear Backoff

```go
// Linear backoff (delay increases linearly)
result := retry.LinearBackoff(func() error {
    return someOperation()
}, 5, 100*time.Millisecond) // maxAttempts, initialDelay
```

### Infinite Retry

```go
// Retry until success or context cancellation
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()

result := retry.UntilSuccess(ctx, func(ctx context.Context) error {
    return someOperation(ctx)
}, 1*time.Second) // delay between attempts
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `WithMaxAttempts(n)` | Maximum retry attempts | 3 |
| `WithInitialDelay(d)` | Initial delay between retries | 100ms |
| `WithMaxDelay(d)` | Maximum delay cap | 30s |
| `WithMultiplier(m)` | Backoff multiplier | 2.0 |
| `WithJitter(j)` | Jitter percentage (0-1) | 0.1 |
| `WithMaxJitter(d)` | Fixed maximum jitter duration | - |
| `WithRetryOn(fn)` | Error filter function | all errors |
| `WithOnRetry(fn)` | Retry callback | - |
| `WithTimeout(d)` | Total operation timeout | - |

## Result Structure

```go
type Result struct {
    Attempts int           // Total attempts made
    Duration  time.Duration // Total time spent
    Error     error         // Last error (nil if successful)
    Success   bool          // Whether operation succeeded
}
```

## Examples

### HTTP Client with Retry

```go
func fetchWithRetry(url string) (*http.Response, error) {
    var resp *http.Response
    
    result := retry.Do(func() error {
        var err error
        resp, err = http.Get(url)
        if err != nil {
            return err
        }
        
        // Retry on server errors
        if resp.StatusCode >= 500 {
            return fmt.Errorf("server error: %d", resp.StatusCode)
        }
        
        return nil
    },
        retry.WithMaxAttempts(5),
        retry.WithInitialDelay(500*time.Millisecond),
        retry.WithMaxDelay(30*time.Second),
        retry.WithRetryOn(func(err error) bool {
            // Don't retry on 4xx errors
            return !strings.Contains(err.Error(), "404") &&
                   !strings.Contains(err.Error(), "401")
        }),
    )
    
    if !result.Success {
        return nil, result.Error
    }
    
    return resp, nil
}
```

### Database Operation with Circuit Breaker

```go
var dbCircuit = retry.NewCircuitBreaker(5, 30*time.Second)

func queryWithCircuitBreaker(query string) (*sql.Rows, error) {
    err := dbCircuit.Execute(func() error {
        rows, err = db.Query(query)
        return err
    })
    
    if err != nil {
        return nil, err
    }
    
    return rows, nil
}
```

## Testing

Run tests:

```bash
go test ./...
```

Run benchmarks:

```bash
go test -bench=. ./...
```

## License

MIT License