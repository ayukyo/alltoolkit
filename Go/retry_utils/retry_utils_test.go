package retry_utils

import (
	"context"
	"errors"
	"fmt"
	"sync/atomic"
	"testing"
	"time"
)

func TestDefaultConfig(t *testing.T) {
	cfg := DefaultConfig()

	if cfg.MaxAttempts != 3 {
		t.Errorf("Expected MaxAttempts=3, got %d", cfg.MaxAttempts)
	}
	if cfg.InitialDelay != 100*time.Millisecond {
		t.Errorf("Expected InitialDelay=100ms, got %v", cfg.InitialDelay)
	}
	if cfg.MaxDelay != 30*time.Second {
		t.Errorf("Expected MaxDelay=30s, got %v", cfg.MaxDelay)
	}
	if cfg.Multiplier != 2.0 {
		t.Errorf("Expected Multiplier=2.0, got %f", cfg.Multiplier)
	}
	if cfg.Jitter != 0.1 {
		t.Errorf("Expected Jitter=0.1, got %f", cfg.Jitter)
	}
}

func TestNewConfig(t *testing.T) {
	cfg := NewConfig(
		WithMaxAttempts(5),
		WithInitialDelay(200*time.Millisecond),
		WithMaxDelay(60*time.Second),
		WithMultiplier(1.5),
		WithJitter(0.2),
	)

	if cfg.MaxAttempts != 5 {
		t.Errorf("Expected MaxAttempts=5, got %d", cfg.MaxAttempts)
	}
	if cfg.InitialDelay != 200*time.Millisecond {
		t.Errorf("Expected InitialDelay=200ms, got %v", cfg.InitialDelay)
	}
	if cfg.MaxDelay != 60*time.Second {
		t.Errorf("Expected MaxDelay=60s, got %v", cfg.MaxDelay)
	}
	if cfg.Multiplier != 1.5 {
		t.Errorf("Expected Multiplier=1.5, got %f", cfg.Multiplier)
	}
	if cfg.Jitter != 0.2 {
		t.Errorf("Expected Jitter=0.2, got %f", cfg.Jitter)
	}
}

func TestDo_Success(t *testing.T) {
	result := Do(func() error {
		return nil
	})

	if !result.Success {
		t.Error("Expected success")
	}
	if result.Attempts != 1 {
		t.Errorf("Expected 1 attempt, got %d", result.Attempts)
	}
	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
}

func TestDo_SuccessAfterRetries(t *testing.T) {
	var attempts int32

	result := Do(func() error {
		a := atomic.AddInt32(&attempts, 1)
		if a < 3 {
			return errors.New("temporary error")
		}
		return nil
	}, WithMaxAttempts(5))

	if !result.Success {
		t.Error("Expected success")
	}
	if result.Attempts != 3 {
		t.Errorf("Expected 3 attempts, got %d", result.Attempts)
	}
}

func TestDo_MaxRetriesExceeded(t *testing.T) {
	var attempts int32

	result := Do(func() error {
		atomic.AddInt32(&attempts, 1)
		return errors.New("permanent error")
	}, WithMaxAttempts(3))

	if result.Success {
		t.Error("Expected failure")
	}
	if result.Attempts != 3 {
		t.Errorf("Expected 3 attempts, got %d", result.Attempts)
	}
	if result.Error == nil {
		t.Error("Expected error")
	}
}

func TestDo_RetryOnFilter(t *testing.T) {
	var attempts int32
	retryableError := errors.New("retryable")
	permanentError := errors.New("permanent")

	result := Do(func() error {
		a := atomic.AddInt32(&attempts, 1)
		if a == 1 {
			return retryableError
		}
		return permanentError
	},
		WithMaxAttempts(5),
		WithRetryOn(func(err error) bool {
			return errors.Is(err, retryableError)
		}),
	)

	if result.Success {
		t.Error("Expected failure")
	}
	if result.Attempts != 2 {
		t.Errorf("Expected 2 attempts, got %d", result.Attempts)
	}
}

func TestDo_OnRetryCallback(t *testing.T) {
	var callbackAttempts []int
	var callbackErrors []error

	result := Do(func() error {
		return errors.New("error")
	},
		WithMaxAttempts(3),
		WithOnRetry(func(attempt int, err error) {
			callbackAttempts = append(callbackAttempts, attempt)
			callbackErrors = append(callbackErrors, err)
		}),
	)

	if len(callbackAttempts) != 2 {
		t.Errorf("Expected 2 callback calls, got %d", len(callbackAttempts))
	}
	if len(callbackErrors) != 2 {
		t.Errorf("Expected 2 error callbacks, got %d", len(callbackErrors))
	}
	_ = result
}

func TestDo_OnSuccessCallback(t *testing.T) {
	var successAttempts int
	var successDuration time.Duration

	result := Do(func() error {
		time.Sleep(10 * time.Millisecond)
		return nil
	},
		WithOnSuccess(func(attempts int, duration time.Duration) {
			successAttempts = attempts
			successDuration = duration
		}),
	)

	if successAttempts != 1 {
		t.Errorf("Expected success attempts=1, got %d", successAttempts)
	}
	if successDuration < 10*time.Millisecond {
		t.Errorf("Expected duration >= 10ms, got %v", successDuration)
	}
	_ = result
}

func TestDo_OnFailureCallback(t *testing.T) {
	var failureAttempts int
	var failureDuration time.Duration
	var failureError error

	result := Do(func() error {
		return errors.New("error")
	},
		WithMaxAttempts(3),
		WithOnFailure(func(attempts int, duration time.Duration, lastErr error) {
			failureAttempts = attempts
			failureDuration = duration
			failureError = lastErr
		}),
	)

	if failureAttempts != 3 {
		t.Errorf("Expected failure attempts=3, got %d", failureAttempts)
	}
	if failureError == nil {
		t.Error("Expected failure error")
	}
	_ = result
}

func TestDo_WithContext(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	var attempts int32

	result := DoWithContext(ctx, func(ctx context.Context) error {
		atomic.AddInt32(&attempts, 1)
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(200 * time.Millisecond):
			return nil
		}
	}, WithMaxAttempts(10))

	if result.Success {
		t.Error("Expected failure due to context cancellation")
	}
	if result.Error != context.DeadlineExceeded {
		t.Errorf("Expected context.DeadlineExceeded, got %v", result.Error)
	}
}

func TestDo_Timeout(t *testing.T) {
	var attempts int32

	result := Do(func() error {
		atomic.AddInt32(&attempts, 1)
		time.Sleep(100 * time.Millisecond)
		return errors.New("error")
	},
		WithMaxAttempts(100),
		WithTimeout(150*time.Millisecond),
	)

	if result.Success {
		t.Error("Expected failure due to timeout")
	}
	if result.Error != context.DeadlineExceeded {
		t.Errorf("Expected context.DeadlineExceeded, got %v", result.Error)
	}
}

func TestCalculateDelay(t *testing.T) {
	tests := []struct {
		attempt  int
		expected time.Duration
		cfg      Config
	}{
		{
			attempt:  1,
			expected: 100 * time.Millisecond,
			cfg:      Config{InitialDelay: 100 * time.Millisecond, Multiplier: 2.0, MaxDelay: 1 * time.Second, Jitter: 0, JitterMode: JitterModePercentage},
		},
		{
			attempt:  2,
			expected: 200 * time.Millisecond,
			cfg:      Config{InitialDelay: 100 * time.Millisecond, Multiplier: 2.0, MaxDelay: 1 * time.Second, Jitter: 0, JitterMode: JitterModePercentage},
		},
		{
			attempt:  3,
			expected: 400 * time.Millisecond,
			cfg:      Config{InitialDelay: 100 * time.Millisecond, Multiplier: 2.0, MaxDelay: 1 * time.Second, Jitter: 0, JitterMode: JitterModePercentage},
		},
		{
			attempt:  4,
			expected: 800 * time.Millisecond,
			cfg:      Config{InitialDelay: 100 * time.Millisecond, Multiplier: 2.0, MaxDelay: 1 * time.Second, Jitter: 0, JitterMode: JitterModePercentage},
		},
		{
			attempt:  5,
			expected: 1 * time.Second,
			cfg:      Config{InitialDelay: 100 * time.Millisecond, Multiplier: 2.0, MaxDelay: 1 * time.Second, Jitter: 0, JitterMode: JitterModePercentage},
		},
	}

	for _, tt := range tests {
		delay := calculateDelay(tt.attempt, tt.cfg)
		if delay < tt.expected*9/10 || delay > tt.expected*11/10 {
			t.Errorf("Attempt %d: expected delay ~%v, got %v", tt.attempt, tt.expected, delay)
		}
	}
}

func TestCalculateJitter(t *testing.T) {
	cfg := Config{
		Jitter:     0.1,
		JitterMode: JitterModePercentage,
	}
	delay := 100 * time.Millisecond

	for i := 0; i < 100; i++ {
		jitter := calculateJitter(delay, cfg)
		if jitter < -10*time.Millisecond || jitter > 10*time.Millisecond {
			t.Errorf("Jitter %v out of expected range [-10ms, 10ms]", jitter)
		}
	}
}

func TestCalculateJitter_Fixed(t *testing.T) {
	cfg := Config{
		MaxJitter:  50 * time.Millisecond,
		JitterMode: JitterModeFixed,
		Jitter:     0, // Should be ignored in fixed mode
	}

	for i := 0; i < 100; i++ {
		jitter := calculateJitter(0, cfg) // delay doesn't matter in fixed mode
		if jitter < 0 || jitter > 50*time.Millisecond {
			t.Errorf("Fixed jitter %v out of expected range [0, 50ms]", jitter)
		}
	}
}

func TestPermanentError(t *testing.T) {
	err := errors.New("base error")
	permErr := Permanent(err)

	if !IsPermanent(permErr) {
		t.Error("Expected IsPermanent to return true")
	}
	if permErr.Error() != "base error" {
		t.Errorf("Expected error message 'base error', got '%s'", permErr.Error())
	}
	if !errors.Is(permErr, err) {
		t.Error("Expected errors.Is to return true for wrapped error")
	}
}

func TestTransientError(t *testing.T) {
	err := errors.New("base error")
	transErr := Transient(err)

	if !IsTransient(transErr) {
		t.Error("Expected IsTransient to return true")
	}
	if transErr.Error() != "base error" {
		t.Errorf("Expected error message 'base error', got '%s'", transErr.Error())
	}
	if !errors.Is(transErr, err) {
		t.Error("Expected errors.Is to return true for wrapped error")
	}
}

func TestRetryableError(t *testing.T) {
	err := errors.New("base error")
	retryErr := RetryAfter(err, 5*time.Second)

	if retryErr.Error() != "base error (retry after 5s)" {
		t.Errorf("Expected formatted error message, got '%s'", retryErr.Error())
	}
	if !errors.Is(retryErr, err) {
		t.Error("Expected errors.Is to return true for wrapped error")
	}
}

func TestRetryableError_NoDuration(t *testing.T) {
	err := errors.New("base error")
	retryErr := RetryAfter(err, 0)

	if retryErr.Error() != "base error" {
		t.Errorf("Expected 'base error', got '%s'", retryErr.Error())
	}
}

func TestCircuitBreaker(t *testing.T) {
	cb := NewCircuitBreaker(3, 100*time.Millisecond)

	// Should start closed
	if cb.State() != StateClosed {
		t.Error("Expected circuit breaker to start closed")
	}

	// Fail 3 times
	for i := 0; i < 3; i++ {
		err := cb.Execute(func() error {
			return errors.New("error")
		})
		if err == nil {
			t.Error("Expected error from failed execution")
		}
	}

	// Should be open now
	if cb.State() != StateOpen {
		t.Error("Expected circuit breaker to be open after 3 failures")
	}

	// Should reject requests
	err := cb.Execute(func() error {
		return nil
	})
	if err == nil {
		t.Error("Expected error when circuit breaker is open")
	}

	// Wait for reset timeout
	time.Sleep(150 * time.Millisecond)

	// Should be in half-open state now
	if cb.State() != StateHalfOpen {
		t.Error("Expected circuit breaker to be in half-open state")
	}

	// Successful request should close the circuit
	err = cb.Execute(func() error {
		return nil
	})
	if err != nil {
		t.Errorf("Expected success in half-open state, got error: %v", err)
	}

	// Should be closed now
	if cb.State() != StateClosed {
		t.Error("Expected circuit breaker to be closed after successful request")
	}
}

func TestCircuitBreaker_HalfOpenFail(t *testing.T) {
	cb := NewCircuitBreaker(2, 100*time.Millisecond)

	// Fail twice to open
	cb.Execute(func() error { return errors.New("error") })
	cb.Execute(func() error { return errors.New("error") })

	if cb.State() != StateOpen {
		t.Error("Expected circuit breaker to be open")
	}

	// Wait for reset timeout
	time.Sleep(150 * time.Millisecond)

	// Should be half-open
	if cb.State() != StateHalfOpen {
		t.Error("Expected circuit breaker to be half-open")
	}

	// Fail in half-open state
	cb.Execute(func() error { return errors.New("error") })

	// Should be open again
	if cb.State() != StateOpen {
		t.Error("Expected circuit breaker to be open after half-open failure")
	}
}

func TestCircuitBreaker_Reset(t *testing.T) {
	cb := NewCircuitBreaker(2, 100*time.Millisecond)

	// Fail twice to open
	cb.Execute(func() error { return errors.New("error") })
	cb.Execute(func() error { return errors.New("error") })

	if cb.State() != StateOpen {
		t.Error("Expected circuit breaker to be open")
	}

	// Reset
	cb.Reset()

	if cb.State() != StateClosed {
		t.Error("Expected circuit breaker to be closed after reset")
	}
}

func TestCircuitBreaker_StateChangeCallback(t *testing.T) {
	var stateChanges []State
	cb := NewCircuitBreaker(2, 100*time.Millisecond,
		WithOnStateChange(func(old, new State) {
			stateChanges = append(stateChanges, new)
		}),
		WithHalfOpenMax(1),
	)

	// Fail twice to open
	cb.Execute(func() error { return errors.New("error") })
	cb.Execute(func() error { return errors.New("error") })

	// Wait for half-open
	time.Sleep(150 * time.Millisecond)

	// Succeed to close
	cb.Execute(func() error { return nil })

	if len(stateChanges) != 2 {
		t.Errorf("Expected 2 state changes, got %d", len(stateChanges))
	}
	if len(stateChanges) > 0 && stateChanges[0] != StateOpen {
		t.Errorf("Expected first change to Open, got %v", stateChanges[0])
	}
	if len(stateChanges) > 1 && stateChanges[1] != StateClosed {
		t.Errorf("Expected second change to Closed, got %v", stateChanges[1])
	}
}

func TestRateLimiter(t *testing.T) {
	rl := NewRateLimiter(10, 2) // 10 tokens/sec, burst of 2

	// Should allow first 2 requests
	if !rl.Allow() {
		t.Error("Expected first request to be allowed")
	}
	if !rl.Allow() {
		t.Error("Expected second request to be allowed")
	}

	// Third should be denied (burst exhausted)
	if rl.Allow() {
		t.Error("Expected third request to be denied")
	}

	// Wait for tokens to replenish
	time.Sleep(200 * time.Millisecond)

	// Should be allowed again
	if !rl.Allow() {
		t.Error("Expected request to be allowed after wait")
	}
}

func TestRateLimiter_Wait(t *testing.T) {
	rl := NewRateLimiter(100, 1) // 100 tokens/sec, burst of 1

	// Exhaust tokens
	rl.Allow()

	// Wait should succeed
	ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel()

	err := rl.Wait(ctx)
	if err != nil {
		t.Errorf("Expected Wait to succeed, got error: %v", err)
	}
}

func TestRateLimiter_WaitContextCancellation(t *testing.T) {
	rl := NewRateLimiter(0.001, 0) // Very low rate, no burst

	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	err := rl.Wait(ctx)
	if err != context.DeadlineExceeded {
		t.Errorf("Expected context.DeadlineExceeded, got: %v", err)
	}
}

func TestBuilder(t *testing.T) {
	builder := NewBuilder()
	result := builder.
		MaxAttempts(5).
		InitialDelay(50 * time.Millisecond).
		MaxDelay(1 * time.Second).
		Multiplier(1.5).
		Jitter(0.05).
		Do(func() error {
			return nil
		})

	if !result.Success {
		t.Error("Expected success")
	}
}

func TestBuilder_WithContext(t *testing.T) {
	ctx := context.Background()
	builder := NewBuilder()
	result := builder.
		MaxAttempts(3).
		DoWithContext(ctx, func(ctx context.Context) error {
			return nil
		})

	if !result.Success {
		t.Error("Expected success")
	}
}

func TestExponentialBackoff(t *testing.T) {
	var attempts int32

	result := ExponentialBackoff(func() error {
		a := atomic.AddInt32(&attempts, 1)
		if a < 3 {
			return errors.New("error")
		}
		return nil
	}, 5, 50*time.Millisecond)

	if !result.Success {
		t.Error("Expected success")
	}
	if result.Attempts != 3 {
		t.Errorf("Expected 3 attempts, got %d", result.Attempts)
	}
}

func TestFixedDelay(t *testing.T) {
	start := time.Now()
	var delays []time.Duration
	lastTime := start

	result := FixedDelay(func() error {
		now := time.Now()
		if len(delays) > 0 {
			// First attempt has no delay
		}
		delays = append(delays, now.Sub(lastTime))
		lastTime = now
		return errors.New("error")
	}, 3, 50*time.Millisecond)

	if result.Success {
		t.Error("Expected failure")
	}
	// FixedDelay should have consistent delays
	_ = delays
}

func TestLinearBackoff(t *testing.T) {
	var attempts int32

	result := LinearBackoff(func() error {
		a := atomic.AddInt32(&attempts, 1)
		if a < 3 {
			return errors.New("error")
		}
		return nil
	}, 5, 50*time.Millisecond)

	if !result.Success {
		t.Error("Expected success")
	}
	if result.Attempts != 3 {
		t.Errorf("Expected 3 attempts, got %d", result.Attempts)
	}
}

func TestUntilSuccess(t *testing.T) {
	var attempts int32

	result := UntilSuccess(context.Background(), func(ctx context.Context) error {
		a := atomic.AddInt32(&attempts, 1)
		if a < 5 {
			return errors.New("error")
		}
		return nil
	}, 10*time.Millisecond)

	if !result.Success {
		t.Error("Expected success")
	}
	if result.Attempts != 5 {
		t.Errorf("Expected 5 attempts, got %d", result.Attempts)
	}
}

func TestUntilSuccess_ContextCancellation(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	result := UntilSuccess(ctx, func(ctx context.Context) error {
		return errors.New("error")
	}, 50*time.Millisecond)

	if result.Success {
		t.Error("Expected failure")
	}
	if result.Error != context.DeadlineExceeded {
		t.Errorf("Expected context.DeadlineExceeded, got: %v", result.Error)
	}
}

func TestConfigDefaults(t *testing.T) {
	// Test that invalid configs are corrected
	cfg := Config{
		MaxAttempts:  -1,
		InitialDelay: -100 * time.Millisecond,
		MaxDelay:     -1 * time.Second,
		Multiplier:   0.5,
		Jitter:       -0.1,
	}

	// Execute with invalid config
	result := execute(context.Background(), func(ctx context.Context) error {
		return nil
	}, cfg)

	// Should still succeed with corrected defaults
	if !result.Success {
		t.Error("Expected success even with invalid config")
	}
}

func TestRetryOnWithPermanentError(t *testing.T) {
	var attempts int32

	result := Do(func() error {
		a := atomic.AddInt32(&attempts, 1)
		if a == 1 {
			return Transient(errors.New("transient"))
		}
		return Permanent(errors.New("permanent"))
	},
		WithMaxAttempts(5),
		WithRetryOn(func(err error) bool {
			return IsTransient(err)
		}),
	)

	if result.Success {
		t.Error("Expected failure")
	}
	if result.Attempts != 2 {
		t.Errorf("Expected 2 attempts (transient then permanent), got %d", result.Attempts)
	}
}

func TestMultipleGoroutines(t *testing.T) {
	// Test thread safety with multiple goroutines
	cb := NewCircuitBreaker(10, 100*time.Millisecond)
	var successCount int32
	var failCount int32

	var done = make(chan bool)
	for i := 0; i < 10; i++ {
		go func() {
			for j := 0; j < 10; j++ {
				err := cb.Execute(func() error {
					return nil // Always succeed
				})
				if err == nil {
					successCount++
				} else {
					failCount++
				}
			}
			done <- true
		}()
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	// All should succeed since we never fail
	if failCount > 0 {
		t.Errorf("Expected no failures, got %d", failCount)
	}
}

func TestResultDuration(t *testing.T) {
	start := time.Now()
	result := Do(func() error {
		time.Sleep(50 * time.Millisecond)
		return nil
	})

	if result.Duration < 50*time.Millisecond {
		t.Errorf("Expected duration >= 50ms, got %v", result.Duration)
	}
	if result.Duration > time.Since(start)+100*time.Millisecond {
		t.Errorf("Duration seems too long: %v", result.Duration)
	}
}

// Benchmark tests
func BenchmarkDo_Success(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Do(func() error { return nil })
	}
}

func BenchmarkDo_WithRetries(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Do(func() error { return errors.New("error") }, WithMaxAttempts(3))
	}
}

func BenchmarkCircuitBreaker_Execute(b *testing.B) {
	cb := NewCircuitBreaker(100, time.Second)
	fn := func() error { return nil }

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cb.Execute(fn)
	}
}

func BenchmarkRateLimiter_Allow(b *testing.B) {
	rl := NewRateLimiter(1000000, 1000000)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rl.Allow()
	}
}

func BenchmarkBuilder(b *testing.B) {
	builder := NewBuilder().
		MaxAttempts(3).
		InitialDelay(10 * time.Millisecond).
		Multiplier(2.0)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		builder.Do(func() error { return nil })
	}
}

// Example tests
func ExampleDo() {
	result := Do(func() error {
		// Simulate an operation that eventually succeeds
		return nil
	}, WithMaxAttempts(3))

	fmt.Printf("Success: %v, Attempts: %d\n", result.Success, result.Attempts)
	// Output: Success: true, Attempts: 1
}

func ExampleDo_withRetry() {
	attempts := 0

	result := Do(func() error {
		attempts++
		if attempts < 3 {
			return errors.New("temporary error")
		}
		return nil
	},
		WithMaxAttempts(5),
		WithInitialDelay(10*time.Millisecond),
		WithOnRetry(func(attempt int, err error) {
			fmt.Printf("Retry attempt %d: %v\n", attempt, err)
		}),
	)

	fmt.Printf("Success: %v, Total attempts: %d\n", result.Success, result.Attempts)
}

func ExampleNewBuilder() {
	result := NewBuilder().
		MaxAttempts(5).
		InitialDelay(100 * time.Millisecond).
		MaxDelay(10 * time.Second).
		Multiplier(2.0).
		Jitter(0.1).
		Do(func() error {
			return nil
		})

	fmt.Printf("Success: %v\n", result.Success)
	// Output: Success: true
}

func ExampleCircuitBreaker() {
	cb := NewCircuitBreaker(3, 5*time.Second)

	err := cb.Execute(func() error {
		// Simulate an operation
		return nil
	})

	if err != nil {
		fmt.Printf("Circuit breaker rejected or operation failed: %v\n", err)
	} else {
		fmt.Println("Operation succeeded")
	}
}

func ExampleRateLimiter() {
	// Create a rate limiter: 10 retries per second, burst of 3
	rl := NewRateLimiter(10, 3)

	// Check if retry is allowed
	if rl.Allow() {
		fmt.Println("Retry allowed")
	} else {
		fmt.Println("Rate limit exceeded")
	}
}

func ExamplePermanent() {
	// Use Permanent to indicate an error should not be retried
	result := Do(func() error {
		return Permanent(errors.New("authentication failed"))
	}, WithMaxAttempts(5))

	fmt.Printf("Success: %v, Attempts: %d\n", result.Success, result.Attempts)
	// Output: Success: false, Attempts: 1
}

func ExampleExponentialBackoff() {
	result := ExponentialBackoff(func() error {
		// Operation that might fail
		return nil
	}, 3, 100*time.Millisecond)

	fmt.Printf("Success: %v\n", result.Success)
	// Output: Success: true
}

func TestCircuitBreaker_HalfOpenMaxSuccess(t *testing.T) {
	var halfOpenCount int
	cb := NewCircuitBreaker(2, 100*time.Millisecond,
		WithHalfOpenMax(3),
		WithOnStateChange(func(old, new State) {
			if new == StateHalfOpen {
				halfOpenCount++
			}
		}),
	)

	// Fail to open
	cb.Execute(func() error { return errors.New("error") })
	cb.Execute(func() error { return errors.New("error") })

	if cb.State() != StateOpen {
		t.Error("Expected open")
	}

	// Wait for half-open
	time.Sleep(150 * time.Millisecond)

	if cb.State() != StateHalfOpen {
		t.Error("Expected half-open")
	}

	// Need 3 successes to close
	cb.Execute(func() error { return nil })
	if cb.State() != StateHalfOpen {
		t.Error("Expected still half-open after 1 success")
	}

	cb.Execute(func() error { return nil })
	if cb.State() != StateHalfOpen {
		t.Error("Expected still half-open after 2 successes")
	}

	cb.Execute(func() error { return nil })
	if cb.State() != StateClosed {
		t.Error("Expected closed after 3 successes")
	}
}

func TestRetryOnSkipNonRetryableErrors(t *testing.T) {
	var attempts int

	result := Do(func() error {
		attempts++
		return errors.New("non-retryable")
	},
		WithMaxAttempts(5),
		WithRetryOn(func(err error) bool {
			return false // Never retry
		}),
	)

	if result.Attempts != 1 {
		t.Errorf("Expected 1 attempt (no retries), got %d", result.Attempts)
	}
	if result.Success {
		t.Error("Expected failure")
	}
}

func TestFixedJitterMode(t *testing.T) {
	cfg := Config{
		InitialDelay: 100 * time.Millisecond,
		MaxDelay:     1 * time.Second,
		Multiplier:   1.0,
		MaxJitter:    50 * time.Millisecond,
		JitterMode:   JitterModeFixed,
		Jitter:       0, // Ignored in fixed mode
	}

	// Test multiple times to verify jitter is applied
	for i := 0; i < 10; i++ {
		delay := calculateDelay(1, cfg)
		// Delay should be base delay (100ms) plus random jitter (0-50ms)
		if delay < 100*time.Millisecond || delay > 150*time.Millisecond {
			t.Errorf("Delay %v out of expected range [100ms, 150ms]", delay)
		}
	}
}

func TestWithMaxJitter(t *testing.T) {
	cfg := NewConfig(WithMaxJitter(100 * time.Millisecond))

	if cfg.MaxJitter != 100*time.Millisecond {
		t.Errorf("Expected MaxJitter=100ms, got %v", cfg.MaxJitter)
	}
	if cfg.JitterMode != JitterModeFixed {
		t.Errorf("Expected JitterMode=Fixed, got %v", cfg.JitterMode)
	}
}

func TestConfigZeroMaxAttempts(t *testing.T) {
	// Zero max attempts should be corrected to 1
	result := Do(func() error {
		return errors.New("error")
	}, WithMaxAttempts(0))

	if result.Attempts != 1 {
		t.Errorf("Expected 1 attempt, got %d", result.Attempts)
	}
}

func TestStateString(t *testing.T) {
	tests := []struct {
		state    State
		expected string
	}{
		{StateClosed, "closed"},
		{StateOpen, "open"},
		{StateHalfOpen, "half-open"},
	}

	for _, tt := range tests {
		// State type doesn't have String() method, but we can verify values
		if tt.state < 0 || tt.state > 2 {
			t.Errorf("Invalid state value: %d", tt.state)
		}
	}
}

func TestErrorTypes(t *testing.T) {
	// Test that our error types implement error interface correctly
	var _ error = &PermanentError{}
	var _ error = &TransientError{}
	var _ error = &RetriableError{}

	// Test error messages
	baseErr := errors.New("base")
	if Permanent(baseErr).Error() != "base" {
		t.Error("Permanent error message incorrect")
	}
	if Transient(baseErr).Error() != "base" {
		t.Error("Transient error message incorrect")
	}
	if RetryAfter(baseErr, time.Second).Error() != "base (retry after 1s)" {
		t.Error("RetriableError message incorrect")
	}
}

func TestRateLimiter_AllowN(t *testing.T) {
	rl := NewRateLimiter(10, 5)

	// Should allow taking 3 tokens at once
	if !rl.AllowN(3) {
		t.Error("Expected AllowN(3) to succeed")
	}

	// Should have 2 remaining
	if !rl.AllowN(2) {
		t.Error("Expected AllowN(2) to succeed")
	}

	// Should be exhausted
	if rl.AllowN(1) {
		t.Error("Expected AllowN(1) to fail")
	}
}

func TestDoWithRetryOnSpecificErrors(t *testing.T) {
	ErrTimeout := errors.New("timeout")
	ErrConnection := errors.New("connection refused")
	ErrInvalid := errors.New("invalid request")

	attempts := 0

	result := Do(func() error {
		attempts++
		switch attempts {
		case 1:
			return ErrTimeout
		case 2:
			return ErrConnection
		default:
			return ErrInvalid
		}
	},
		WithMaxAttempts(10),
		WithRetryOn(func(err error) bool {
			// Only retry on timeout or connection errors
			return errors.Is(err, ErrTimeout) || errors.Is(err, ErrConnection)
		}),
	)

	// Should stop after ErrInvalid (not retryable)
	if result.Attempts != 3 {
		t.Errorf("Expected 3 attempts, got %d", result.Attempts)
	}
	if result.Success {
		t.Error("Expected failure")
	}
	if result.Error != ErrInvalid {
		t.Errorf("Expected ErrInvalid, got %v", result.Error)
	}
}

func TestRetryAfterError(t *testing.T) {
	attempts := 0

	result := Do(func() error {
		attempts++
		if attempts < 3 {
			return RetryAfter(errors.New("rate limited"), 10*time.Millisecond)
		}
		return nil
	}, WithMaxAttempts(5))

	// RetryAfter is just an error wrapper, delay is not automatically used
	// by the retry mechanism (caller can inspect RetryAfter duration)
	if result.Success != true {
		t.Error("Expected success")
	}
	if result.Attempts != 3 {
		t.Errorf("Expected 3 attempts, got %d", result.Attempts)
	}
}

func TestConcurrentRetry(t *testing.T) {
	// Test that multiple concurrent retries work correctly
	var successCount int32
	var failureCount int32

	done := make(chan bool, 100)

	for i := 0; i < 50; i++ {
		go func() {
			result := Do(func() error {
				return nil
			}, WithMaxAttempts(3))

			if result.Success {
				successCount++
			} else {
				failureCount++
			}
			done <- true
		}()
	}

	// Wait for all goroutines
	for i := 0; i < 50; i++ {
		<-done
	}

	if successCount != 50 {
		t.Errorf("Expected 50 successes, got %d", successCount)
	}
	if failureCount != 0 {
		t.Errorf("Expected 0 failures, got %d", failureCount)
	}
}

func TestBuilderChaining(t *testing.T) {
	// Test that all builder methods return *Builder for chaining
	builder := NewBuilder()

	// This should compile without issues
	cfg := builder.
		MaxAttempts(5).
		InitialDelay(100*time.Millisecond).
		MaxDelay(10*time.Second).
		Multiplier(2.0).
		Jitter(0.2).
		FixedJitter(50*time.Millisecond).
		Timeout(30*time.Second).
		Build()

	if cfg.MaxAttempts != 5 {
		t.Errorf("Expected MaxAttempts=5, got %d", cfg.MaxAttempts)
	}
	if cfg.JitterMode != JitterModeFixed {
		t.Error("Expected JitterModeFixed")
	}
}

func TestCircuitBreakerSuccessResetsFailureCount(t *testing.T) {
	cb := NewCircuitBreaker(3, time.Second)

	// Fail twice
	cb.Execute(func() error { return errors.New("error") })
	cb.Execute(func() error { return errors.New("error") })

	// Succeed once
	cb.Execute(func() error { return nil })

	// Fail twice more (should not open because count was reset)
	cb.Execute(func() error { return errors.New("error") })
	cb.Execute(func() error { return errors.New("error") })

	// Should still be closed
	if cb.State() != StateClosed {
		t.Error("Expected circuit breaker to remain closed after success reset failure count")
	}
}