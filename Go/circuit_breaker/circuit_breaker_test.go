package circuit_breaker

import (
	"context"
	"errors"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// =============================================================================
// Test Helper Functions
// =============================================================================

func assertEqual(t *testing.T, expected, actual interface{}) {
	t.Helper()
	if expected != actual {
		t.Errorf("Expected %v, got %v", expected, actual)
	}
}

func assertTrue(t *testing.T, condition bool, msg string) {
	t.Helper()
	if !condition {
		t.Errorf("Expected true: %s", msg)
	}
}

func assertFalse(t *testing.T, condition bool, msg string) {
	t.Helper()
	if condition {
		t.Errorf("Expected false: %s", msg)
	}
}

func assertNoError(t *testing.T, err error) {
	t.Helper()
	if err != nil {
		t.Errorf("Expected no error, got: %v", err)
	}
}

func assertError(t *testing.T, err error) {
	t.Helper()
	if err == nil {
		t.Errorf("Expected error, got nil")
	}
}

func assertErrorIs(t *testing.T, err, target error) {
	t.Helper()
	if !errors.Is(err, target) {
		t.Errorf("Expected error %v, got %v", target, err)
	}
}

// =============================================================================
// Basic Tests
// =============================================================================

func TestNew(t *testing.T) {
	cb := New(DefaultConfig())
	assertEqual(t, Closed, cb.State())
	assertTrue(t, cb.IsClosed(), "Should be closed")
	assertFalse(t, cb.IsOpen(), "Should not be open")
}

func TestNewWithCustomConfig(t *testing.T) {
	config := Config{
		FailureThreshold:   10,
		SuccessThreshold:   5,
		Timeout:           time.Minute,
		MaxConcurrentCalls: 100,
	}
	cb := New(config)
	assertEqual(t, Closed, cb.State())
}

func TestNewWithZeroConfig(t *testing.T) {
	config := Config{} // All zeros
	cb := New(config)
	assertEqual(t, Closed, cb.State())
	// Should use defaults
	assertEqual(t, 5, cb.config.FailureThreshold)
	assertEqual(t, 3, cb.config.SuccessThreshold)
	assertEqual(t, 30*time.Second, cb.config.Timeout)
}

// =============================================================================
// State Transition Tests
// =============================================================================

func TestStateTransitions(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 3,
		SuccessThreshold: 2,
		Timeout:         100 * time.Millisecond,
	})

	ctx := context.Background()

	// Initially closed
	assertEqual(t, Closed, cb.State())

	// Cause failures to trigger Open
	for i := 0; i < 3; i++ {
		_, err := cb.Execute(ctx, func() (interface{}, error) {
			return nil, errors.New("failure")
		})
		assertError(t, err)
	}

	// Should be open now
	assertEqual(t, Open, cb.State())
	assertTrue(t, cb.IsOpen(), "Should be open")

	// Wait for timeout
	time.Sleep(150 * time.Millisecond)

	// Next call should transition to HalfOpen
	_, err := cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	assertNoError(t, err)
	assertEqual(t, HalfOpen, cb.State())

	// Another success should close the circuit
	_, err = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	assertNoError(t, err)
	assertEqual(t, Closed, cb.State())
}

func TestCircuitOpensOnFailures(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 2,
		Timeout:         time.Minute,
	})

	ctx := context.Background()

	// First failure
	_, err := cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure 1")
	})
	assertError(t, err)
	assertEqual(t, Closed, cb.State())

	// Second failure - should open
	_, err = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure 2")
	})
	assertError(t, err)
	assertEqual(t, Open, cb.State())
}

func TestCircuitRejectsWhenOpen(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 1,
		Timeout:         time.Minute,
	})

	ctx := context.Background()

	// Cause failure to open
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	assertEqual(t, Open, cb.State())

	// Should reject
	_, err := cb.Execute(ctx, func() (interface{}, error) {
		return "should not execute", nil
	})
	assertErrorIs(t, err, ErrCircuitOpen)
}

func TestCircuitClosesAfterSuccessInHalfOpen(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 1,
		SuccessThreshold: 2,
		Timeout:         50 * time.Millisecond,
	})

	ctx := context.Background()

	// Open the circuit
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})
	assertEqual(t, Open, cb.State())

	// Wait for timeout
	time.Sleep(60 * time.Millisecond)

	// First success - transitions to HalfOpen
	_, err := cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	assertNoError(t, err)
	assertEqual(t, HalfOpen, cb.State())

	// Second success - should close
	_, err = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	assertNoError(t, err)
	assertEqual(t, Closed, cb.State())
}

func TestCircuitReopensOnFailureInHalfOpen(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 1,
		SuccessThreshold: 2,
		Timeout:         50 * time.Millisecond,
	})

	ctx := context.Background()

	// Open the circuit
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})
	assertEqual(t, Open, cb.State())

	// Wait for timeout
	time.Sleep(60 * time.Millisecond)

	// First success - transitions to HalfOpen
	_, err := cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	assertNoError(t, err)
	assertEqual(t, HalfOpen, cb.State())

	// Failure in HalfOpen - should reopen
	_, err = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})
	assertError(t, err)
	assertEqual(t, Open, cb.State())
}

// =============================================================================
// Success/Failure Counter Tests
// =============================================================================

func TestSuccessesResetFailures(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 5,
	})

	ctx := context.Background()

	// Cause some failures (but not enough to open)
	for i := 0; i < 3; i++ {
		_, _ = cb.Execute(ctx, func() (interface{}, error) {
			return nil, errors.New("failure")
		})
	}

	stats := cb.Stats()
	assertEqual(t, int64(3), stats.Failures)

	// Success should reset failure counter
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})

	// Check that internal counter was reset by verifying we need 5 more failures
	for i := 0; i < 4; i++ {
		_, _ = cb.Execute(ctx, func() (interface{}, error) {
			return nil, errors.New("failure")
		})
	}
	assertEqual(t, Closed, cb.State())

	// One more failure should open
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})
	assertEqual(t, Open, cb.State())
}

// =============================================================================
// Statistics Tests
// =============================================================================

func TestStats(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	ctx := context.Background()

	// Execute some operations
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	stats := cb.Stats()
	assertEqual(t, int64(3), stats.TotalCalls)
	assertEqual(t, int64(2), stats.Successes)
	assertEqual(t, int64(1), stats.Failures)
}

func TestStatsFailureRate(t *testing.T) {
	stats := Stats{
		TotalCalls: 10,
		Successes:  7,
		Failures:   3,
	}

	assertEqual(t, 30.0, stats.FailureRate())
	assertEqual(t, 70.0, stats.SuccessRate())
}

func TestStatsZeroCalls(t *testing.T) {
	stats := Stats{}
	assertEqual(t, 0.0, stats.FailureRate())
	assertEqual(t, 0.0, stats.SuccessRate())
}

// =============================================================================
// Context and Timeout Tests
// =============================================================================

func TestContextCancellation(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	ctx, cancel := context.WithCancel(context.Background())

	// Start a slow operation
	var wg sync.WaitGroup
	var err error
	wg.Add(1)
	go func() {
		defer wg.Done()
		_, err = cb.Execute(ctx, func() (interface{}, error) {
			time.Sleep(200 * time.Millisecond)
			return "result", nil
		})
	}()

	// Cancel after a short time
	time.Sleep(50 * time.Millisecond)
	cancel()

	wg.Wait()

	assertErrorIs(t, err, ErrTimeout)
}

func TestCallTimeout(t *testing.T) {
	cb := New(Config{
		FailureThreshold:   10,
		TimeoutDuration:    50 * time.Millisecond,
	})

	ctx := context.Background()

	_, err := cb.Execute(ctx, func() (interface{}, error) {
		time.Sleep(200 * time.Millisecond)
		return "result", nil
	})

	assertErrorIs(t, err, ErrTimeout)

	// Timeout should count as failure
	stats := cb.Stats()
	assertEqual(t, int64(1), stats.Failures)
}

// =============================================================================
// Fallback Tests
// =============================================================================

func TestFallbackOnOpen(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 1,
		Timeout:         time.Minute,
	})

	ctx := context.Background()

	// Open the circuit
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	// Execute with fallback
	result, err := cb.ExecuteWithFallback(ctx,
		func() (interface{}, error) {
			return "should not execute", nil
		},
		func(e error) (interface{}, error) {
			return "fallback result", nil
		},
	)

	assertNoError(t, err)
	assertEqual(t, "fallback result", result)
}

func TestFallbackOnError(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	ctx := context.Background()

	// Execute with fallback that returns on error
	result, err := cb.ExecuteWithFallback(ctx,
		func() (interface{}, error) {
			return nil, errors.New("some error")
		},
		func(e error) (interface{}, error) {
			return "fallback on error", nil
		},
	)

	// Note: Fallback only triggers on circuit open, not on operation error
	assertError(t, err)
	assertEqual(t, nil, result)
}

// =============================================================================
// Concurrent Tests
// =============================================================================

func TestMaxConcurrentCalls(t *testing.T) {
	cb := New(Config{
		FailureThreshold:   10,
		MaxConcurrentCalls: 2,
	})

	ctx := context.Background()

	var wg sync.WaitGroup
	var successCount int64
	var rejectCount int64

	// Start 5 concurrent operations
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			_, err := cb.Execute(ctx, func() (interface{}, error) {
				time.Sleep(100 * time.Millisecond)
				return "result", nil
			})
			if err == nil {
				atomic.AddInt64(&successCount, 1)
			} else if errors.Is(err, ErrTooManyConcurrentCalls) {
				atomic.AddInt64(&rejectCount, 1)
			}
		}()
	}

	wg.Wait()

	// Only 2 should succeed (max concurrent)
	assertTrue(t, successCount <= 2, "Too many concurrent calls succeeded")
	assertTrue(t, rejectCount > 0, "Some calls should be rejected")
}

func TestConcurrentSafety(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 100,
	})

	ctx := context.Background()
	var wg sync.WaitGroup

	// Run 100 concurrent operations
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			_, _ = cb.Execute(ctx, func() (interface{}, error) {
				return "result", nil
			})
		}()
	}

	wg.Wait()

	stats := cb.Stats()
	assertEqual(t, int64(100), stats.TotalCalls)
	assertEqual(t, int64(100), stats.Successes)
}

// =============================================================================
// Manual Integration Tests
// =============================================================================

func TestAllowAndRecord(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 2,
		Timeout:         100 * time.Millisecond,
	})

	// Should allow initially
	assertTrue(t, cb.Allow(), "Should allow initially")

	// Record failures
	cb.RecordFailure(errors.New("failure 1"))
	assertTrue(t, cb.Allow(), "Should still allow")

	cb.RecordFailure(errors.New("failure 2"))
	assertFalse(t, cb.Allow(), "Should not allow after failures")

	// Wait for timeout
	time.Sleep(150 * time.Millisecond)

	// Should allow again (transition to HalfOpen)
	assertTrue(t, cb.Allow(), "Should allow after timeout")

	// Record success to close
	cb.RecordSuccess()
	assertTrue(t, cb.Allow(), "Should allow after success")
}

func TestTripAndReset(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	assertEqual(t, Closed, cb.State())

	// Trip the circuit
	cb.Trip()
	assertEqual(t, Open, cb.State())
	assertTrue(t, cb.IsOpen(), "Should be open")

	// Reset
	cb.Reset()
	assertEqual(t, Closed, cb.State())
	assertTrue(t, cb.IsClosed(), "Should be closed")

	stats := cb.Stats()
	assertEqual(t, int64(0), stats.TotalCalls)
	assertEqual(t, int64(0), stats.Failures)
}

func TestReady(t *testing.T) {
	cb := New(Config{
		FailureThreshold:   1,
		MaxConcurrentCalls: 2,
	})

	assertTrue(t, cb.Ready(), "Should be ready initially")

	// Open the circuit
	cb.Trip()
	assertFalse(t, cb.Ready(), "Should not be ready when open")
}

// =============================================================================
// TimeUntilRetry Tests
// =============================================================================

func TestTimeUntilRetry(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 1,
		Timeout:         200 * time.Millisecond,
	})

	// Not open, should return 0
	assertEqual(t, time.Duration(0), cb.TimeUntilRetry())

	// Open the circuit
	cb.Trip()

	// Should have a positive duration
	timeUntilRetry := cb.TimeUntilRetry()
	assertTrue(t, timeUntilRetry > 0, "Should have positive time until retry")
	assertTrue(t, timeUntilRetry <= 200*time.Millisecond, "Should be <= timeout")

	// Wait and check again
	time.Sleep(100 * time.Millisecond)
	newTimeUntilRetry := cb.TimeUntilRetry()
	assertTrue(t, newTimeUntilRetry < timeUntilRetry, "Time should decrease")
}

// =============================================================================
// Callback Tests
// =============================================================================

func TestOnStateChange(t *testing.T) {
	var stateChanges []State
	cb := New(Config{
		FailureThreshold: 1,
		Timeout:         50 * time.Millisecond,
		OnStateChange: func(oldState, newState State) {
			stateChanges = append(stateChanges, oldState, newState)
		},
	})

	ctx := context.Background()

	// Open the circuit
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	// Wait for timeout and transition to HalfOpen
	time.Sleep(60 * time.Millisecond)
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})

	// Close with another success
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})

	// Wait for goroutines
	time.Sleep(50 * time.Millisecond)

	// Should have recorded state changes
	assertTrue(t, len(stateChanges) >= 4, "Should have state changes")
}

func TestOnEvent(t *testing.T) {
	var events []Event
	cb := New(Config{
		FailureThreshold: 2,
		OnEvent: func(event Event, stats Stats) {
			events = append(events, event)
		},
	})

	ctx := context.Background()

	// Execute operations
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	// Wait for goroutines
	time.Sleep(50 * time.Millisecond)

	// Should have recorded events
	assertTrue(t, len(events) >= 2, "Should have events")
}

func TestIsFailure(t *testing.T) {
	specialError := errors.New("special error")
	
	cb := New(Config{
		FailureThreshold: 2,
		IsFailure: func(err error) bool {
			// Only count "special error" as failure
			return err == specialError
		},
	})

	ctx := context.Background()

	// Regular errors should not count
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("regular error")
	})
	assertEqual(t, Closed, cb.State())

	// Special error should count
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, specialError
	})
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, specialError
	})
	assertEqual(t, Open, cb.State())
}

// =============================================================================
// Health Tests
// =============================================================================

func TestHealth(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 2,
		Timeout:         100 * time.Millisecond,
	})

	ctx := context.Background()

	// Execute some operations
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return "success", nil
	})
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	health := cb.Health()
	assertTrue(t, health.Healthy, "Should be healthy when closed")
	assertEqual(t, Closed, health.State)
	assertEqual(t, int64(2), health.TotalCalls)

	// Open the circuit
	_, _ = cb.Execute(ctx, func() (interface{}, error) {
		return nil, errors.New("failure")
	})

	health = cb.Health()
	assertFalse(t, health.Healthy, "Should not be healthy when open")
	assertEqual(t, Open, health.State)
	assertTrue(t, health.TimeUntilRetry > 0, "Should have time until retry")
}

// =============================================================================
// String Tests
// =============================================================================

func TestString(t *testing.T) {
	cb := New(DefaultConfig())
	str := cb.String()
	assertTrue(t, len(str) > 0, "String should not be empty")
	assertTrue(t, str == "CircuitBreaker{state=closed, failures=0, successes=0, rejected=0}", 
		"String representation should match")
}

// =============================================================================
// Run and Call Tests
// =============================================================================

func TestRun(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	ctx := context.Background()

	err := cb.Run(ctx, func() error {
		return nil
	})
	assertNoError(t, err)

	err = cb.Run(ctx, func() error {
		return errors.New("some error")
	})
	assertError(t, err)
}

func TestCall(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	ctx := context.Background()

	result, err := cb.Call(ctx, func() (interface{}, error) {
		return "test result", nil
	})
	assertNoError(t, err)
	assertEqual(t, "test result", result)
}

// =============================================================================
// Batch Tests
// =============================================================================

func TestExecuteBatch(t *testing.T) {
	cb := New(Config{
		FailureThreshold: 10,
	})

	ctx := context.Background()

	fns := []func() (interface{}, error){
		func() (interface{}, error) { return 1, nil },
		func() (interface{}, error) { return 2, nil },
		func() (interface{}, error) { return nil, errors.New("error") },
		func() (interface{}, error) { return 4, nil },
	}

	result := cb.ExecuteBatch(ctx, fns)

	assertEqual(t, 4, len(result.Results))
	assertEqual(t, 4, len(result.Errors))
	assertNoError(t, result.Errors[0])
	assertNoError(t, result.Errors[1])
	assertError(t, result.Errors[2])
	assertNoError(t, result.Errors[3])
}

// =============================================================================
// State String Tests
// =============================================================================

func TestStateString(t *testing.T) {
	assertEqual(t, "closed", Closed.String())
	assertEqual(t, "open", Open.String())
	assertEqual(t, "half-open", HalfOpen.String())
}

func TestEventString(t *testing.T) {
	assertEqual(t, "state_change", EventStateChange.String())
	assertEqual(t, "success", EventSuccess.String())
	assertEqual(t, "failure", EventFailure.String())
	assertEqual(t, "rejected", EventRejected.String())
	assertEqual(t, "timeout", EventTimeout.String())
	assertEqual(t, "half_open_success", EventHalfOpenSuccess.String())
	assertEqual(t, "half_open_failure", EventHalfOpenFailure.String())
}

// =============================================================================
// Benchmark Tests
// =============================================================================

func BenchmarkExecute(b *testing.B) {
	cb := New(Config{
		FailureThreshold: 1000000,
	})

	ctx := context.Background()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = cb.Execute(ctx, func() (interface{}, error) {
			return "result", nil
		})
	}
}

func BenchmarkExecuteParallel(b *testing.B) {
	cb := New(Config{
		FailureThreshold:   1000000,
		MaxConcurrentCalls: 0, // unlimited
	})

	ctx := context.Background()

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			_, _ = cb.Execute(ctx, func() (interface{}, error) {
				return "result", nil
			})
		}
	})
}

func BenchmarkStateRead(b *testing.B) {
	cb := New(DefaultConfig())

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = cb.State()
	}
}

func BenchmarkStatsRead(b *testing.B) {
	cb := New(DefaultConfig())

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = cb.Stats()
	}
}