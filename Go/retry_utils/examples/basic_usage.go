package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"time"

	retry "github.com/ayukyo/alltoolkit/Go/retry_utils"
)

func main() {
	fmt.Println("=== retry_utils Examples ===\n")

	// Run examples
	basicRetryExample()
	exponentialBackoffExample()
	builderPatternExample()
	contextCancellationExample()
	errorClassificationExample()
	circuitBreakerExample()
	rateLimiterExample()
	convenienceFunctionsExample()
	httpClientExample()
}

// basicRetryExample demonstrates the simplest retry usage
func basicRetryExample() {
	fmt.Println("--- Basic Retry ---")

	attempts := 0
	result := retry.Do(func() error {
		attempts++
		fmt.Printf("  Attempt %d\n", attempts)
		if attempts < 3 {
			return errors.New("temporary error")
		}
		return nil
	}, retry.WithMaxAttempts(5))

	fmt.Printf("  Success: %v, Attempts: %d, Duration: %v\n\n",
		result.Success, result.Attempts, result.Duration)
}

// exponentialBackoffExample shows exponential backoff with jitter
func exponentialBackoffExample() {
	fmt.Println("--- Exponential Backoff ---")

	start := time.Now()
	attempts := 0

	result := retry.Do(func() error {
		attempts++
		delay := time.Since(start).Round(time.Millisecond)
		fmt.Printf("  Attempt %d at %v\n", attempts, delay)
		if attempts < 4 {
			return errors.New("temporary error")
		}
		return nil
	},
		retry.WithMaxAttempts(5),
		retry.WithInitialDelay(100*time.Millisecond),
		retry.WithMaxDelay(1*time.Second),
		retry.WithMultiplier(2.0),
		retry.WithJitter(0.1),
	)

	fmt.Printf("  Total duration: %v\n\n", result.Duration.Round(time.Millisecond))
}

// builderPatternExample demonstrates the fluent builder API
func builderPatternExample() {
	fmt.Println("--- Builder Pattern ---")

	result := retry.NewBuilder().
		MaxAttempts(3).
		InitialDelay(50 * time.Millisecond).
		MaxDelay(500 * time.Millisecond).
		Multiplier(1.5).
		Jitter(0.2).
		OnRetry(func(attempt int, err error) {
			fmt.Printf("  Retrying (attempt %d): %v\n", attempt, err)
		}).
		OnSuccess(func(attempts int, duration time.Duration) {
			fmt.Printf("  Success after %d attempts in %v\n", attempts, duration)
		}).
		Do(func() error {
			return errors.New("simulated error")
		})

	fmt.Printf("  Final result: Success=%v\n\n", result.Success)
}

// contextCancellationExample shows context timeout handling
func contextCancellationExample() {
	fmt.Println("--- Context Cancellation ---")

	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	attempts := 0
	result := retry.DoWithContext(ctx, func(ctx context.Context) error {
		attempts++
		fmt.Printf("  Attempt %d\n", attempts)
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(100 * time.Millisecond):
			return errors.New("operation timeout")
		}
	}, retry.WithMaxAttempts(100))

	fmt.Printf("  Stopped after %d attempts: %v\n\n", result.Attempts, result.Error)
}

// errorClassificationExample demonstrates permanent vs transient errors
func errorClassificationExample() {
	fmt.Println("--- Error Classification ---")

	// Example 1: Permanent error (no retry)
	attempts := 0
	result := retry.Do(func() error {
		attempts++
		fmt.Printf("  Permanent error attempt %d\n", attempts)
		return retry.Permanent(errors.New("authentication failed"))
	}, retry.WithMaxAttempts(5))

	fmt.Printf("  Permanent error stopped after %d attempts\n", result.Attempts)

	// Example 2: Transient error with retry filter
	fmt.Println("\n  With retry filter:")
	attempts = 0
	var ErrTimeout = errors.New("timeout")
	var ErrAuth = errors.New("auth error")

	result = retry.Do(func() error {
		attempts++
		fmt.Printf("  Filtered attempt %d\n", attempts)
		if attempts == 1 {
			return ErrTimeout // Will retry
		}
		return ErrAuth // Will not retry
	},
		retry.WithMaxAttempts(5),
		retry.WithRetryOn(func(err error) bool {
			return errors.Is(err, ErrTimeout)
		}),
	)

	fmt.Printf("  Filtered error stopped after %d attempts\n\n", result.Attempts)
}

// circuitBreakerExample demonstrates the circuit breaker pattern
func circuitBreakerExample() {
	fmt.Println("--- Circuit Breaker ---")

	cb := retry.NewCircuitBreaker(3, 500*time.Millisecond,
		retry.WithOnStateChange(func(old, new retry.State) {
			fmt.Printf("  State changed: %v -> %v\n", stateName(old), stateName(new))
		}),
		retry.WithHalfOpenMax(1),
	)

	// Fail the circuit breaker
	fmt.Println("  Causing failures...")
	for i := 0; i < 3; i++ {
		err := cb.Execute(func() error {
			return errors.New("service error")
		})
		fmt.Printf("  Execute %d: %v, state: %v\n", i+1, err, stateName(cb.State()))
	}

	// Try to execute while open
	fmt.Println("\n  Attempting while open:")
	err := cb.Execute(func() error {
		return nil
	})
	fmt.Printf("  Result: %v, state: %v\n", err, stateName(cb.State()))

	// Wait for reset timeout
	fmt.Println("\n  Waiting for half-open state...")
	time.Sleep(600 * time.Millisecond)
	fmt.Printf("  State after wait: %v\n", stateName(cb.State()))

	// Successful request in half-open state
	err = cb.Execute(func() error {
		return nil
	})
	fmt.Printf("  After success: %v, state: %v\n\n", err, stateName(cb.State()))
}

func stateName(s retry.State) string {
	switch s {
	case retry.StateClosed:
		return "closed"
	case retry.StateOpen:
		return "open"
	case retry.StateHalfOpen:
		return "half-open"
	default:
		return "unknown"
	}
}

// rateLimiterExample demonstrates rate limiting for retries
func rateLimiterExample() {
	fmt.Println("--- Rate Limiter ---")

	// Create rate limiter: 5 retries per second, burst of 2
	rl := retry.NewRateLimiter(5, 2)

	fmt.Println("  Checking rate limit:")
	for i := 0; i < 5; i++ {
		allowed := rl.Allow()
		fmt.Printf("  Request %d: allowed=%v\n", i+1, allowed)
	}

	fmt.Println("\n  Waiting for token:")
	ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel()

	err := rl.Wait(ctx)
	if err != nil {
		fmt.Printf("  Wait failed: %v\n", err)
	} else {
		fmt.Println("  Wait succeeded, token acquired")
	}

	fmt.Println()
}

// convenienceFunctionsExample shows quick retry shortcuts
func convenienceFunctionsExample() {
	fmt.Println("--- Convenience Functions ---")

	// Exponential backoff
	attempts := 0
	result := retry.ExponentialBackoff(func() error {
		attempts++
		return errors.New("error")
	}, 3, 50*time.Millisecond)
	fmt.Printf("  ExponentialBackoff: attempts=%d, success=%v\n", result.Attempts, result.Success)

	// Fixed delay
	attempts = 0
	result = retry.FixedDelay(func() error {
		attempts++
		if attempts < 3 {
			return errors.New("error")
		}
		return nil
	}, 5, 50*time.Millisecond)
	fmt.Printf("  FixedDelay: attempts=%d, success=%v\n", result.Attempts, result.Success)

	// Linear backoff
	attempts = 0
	result = retry.LinearBackoff(func() error {
		attempts++
		if attempts < 3 {
			return errors.New("error")
		}
		return nil
	}, 5, 50*time.Millisecond)
	fmt.Printf("  LinearBackoff: attempts=%d, success=%v\n\n", result.Attempts, result.Success)
}

// httpClientExample shows a real-world HTTP client with retry
func httpClientExample() {
	fmt.Println("--- HTTP Client with Retry ---")

	// Simulated HTTP client with retry
	var doHTTPRequest = func(url string) (*http.Response, error) {
		var resp *http.Response
		var lastErr error

		result := retry.Do(func() error {
			// In a real scenario, this would be an actual HTTP request
			// resp, lastErr = http.Get(url)

			// Simulated responses
			attempts := 0
			attempts++

			// Simulate different responses based on URL
			if url == "http://example.com/success" {
				resp = &http.Response{StatusCode: 200}
				return nil
			} else if url == "http://example.com/retry" {
				if attempts < 3 {
					lastErr = errors.New("server error 503")
					return lastErr
				}
				resp = &http.Response{StatusCode: 200}
				return nil
			}

			lastErr = errors.New("not found")
			return retry.Permanent(lastErr) // Don't retry 404s
		},
			retry.WithMaxAttempts(5),
			retry.WithInitialDelay(100*time.Millisecond),
			retry.WithOnRetry(func(attempt int, err error) {
				fmt.Printf("  Retry %d for %s: %v\n", attempt, url, err)
			}),
		)

		if !result.Success {
			return nil, lastErr
		}
		return resp, nil
	}

	// Test cases
	urls := []string{
		"http://example.com/success",
		"http://example.com/retry",
		"http://example.com/notfound",
	}

	for _, url := range urls {
		resp, err := doHTTPRequest(url)
		if err != nil {
			fmt.Printf("  %s: error - %v\n", url, err)
		} else {
			fmt.Printf("  %s: status %d\n", url, resp.StatusCode)
		}
	}

	fmt.Println()
}

// databaseExample shows a database operation with circuit breaker
func databaseExample() {
	// This would be a real database in production
	var dbCircuit = retry.NewCircuitBreaker(5, 30*time.Second,
		retry.WithOnStateChange(func(old, new retry.State) {
			log.Printf("Database circuit breaker: %v -> %v", stateName(old), stateName(new))
		}),
	)

	// Simulated database query
	var queryWithCircuitBreaker = func(query string) (string, error) {
		var result string
		err := dbCircuit.Execute(func() error {
			// Simulate database query
			result = "data"
			return nil
		})

		if err != nil {
			return "", fmt.Errorf("circuit breaker rejected or query failed: %w", err)
		}

		return result, nil
	}

	_, _ = queryWithCircuitBreaker("SELECT * FROM users")
}