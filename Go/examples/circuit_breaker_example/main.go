// Example demonstrating circuit breaker usage
package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

// Simulated external service
type ExternalService struct {
	failureRate float64
	callCount   int
}

func (s *ExternalService) Call() (string, error) {
	s.callCount++
	
	// Simulate failure rate
	if float64(s.callCount%10) < s.failureRate*10 {
		return "", errors.New("service unavailable")
	}
	
	return fmt.Sprintf("response-%d", s.callCount), nil
}

func main() {
	fmt.Println("=== Circuit Breaker Example ===")
	fmt.Println()
	
	// This example shows how to use circuit breaker with a simulated service
	// Note: In actual usage, import from "github.com/ayukyo/alltoolkit/Go/circuit_breaker"
	
	// Simulated circuit breaker for demo purposes
	cb := NewSimulatedCircuitBreaker(Config{
		FailureThreshold: 3,
		SuccessThreshold: 2,
		Timeout:         2 * time.Second,
	})
	
	service := &ExternalService{failureRate: 0.6} // 60% failure rate
	
	ctx := context.Background()
	
	fmt.Println("Simulating service calls with 60% failure rate...")
	fmt.Println()
	
	// Make several calls
	for i := 0; i < 15; i++ {
		result, err := cb.Execute(ctx, func() (interface{}, error) {
			return service.Call()
		})
		
		fmt.Printf("Call %2d: ", i+1)
		
		if err != nil {
			if errors.Is(err, ErrCircuitOpen) {
				fmt.Printf("REJECTED (circuit open, retry after %v)\n", cb.TimeUntilRetry())
			} else {
				fmt.Printf("FAILED: %v\n", err)
			}
		} else {
			fmt.Printf("SUCCESS: %v\n", result)
		}
		
		// Show stats
		stats := cb.Stats()
		fmt.Printf("         State: %s | Success: %d | Failures: %d | Rejected: %d\n",
			stats.State, stats.Successes, stats.Failures, stats.RejectedCalls)
		fmt.Println()
		
		// Simulate recovery after circuit opens
		if cb.IsOpen() && i == 8 {
			fmt.Println(">>> Service recovering... reducing failure rate")
			service.failureRate = 0.0 // No more failures
			time.Sleep(cb.TimeUntilRetry() + 100*time.Millisecond)
		}
		
		time.Sleep(100 * time.Millisecond)
	}
	
	fmt.Println("=== Final Stats ===")
	stats := cb.Stats()
	fmt.Printf("Total Calls: %d\n", stats.TotalCalls)
	fmt.Printf("Successes: %d\n", stats.Successes)
	fmt.Printf("Failures: %d\n", stats.Failures)
	fmt.Printf("Rejected: %d\n", stats.RejectedCalls)
	fmt.Printf("Failure Rate: %.1f%%\n", stats.FailureRate())
	fmt.Printf("Final State: %s\n", cb.State())
}

// =============================================================================
// Simulated Circuit Breaker for Demo (simplified version of actual implementation)
// =============================================================================

type State int

const (
	Closed State = iota
	Open
	HalfOpen
)

func (s State) String() string {
	switch s {
	case Closed:
		return "closed"
	case Open:
		return "open"
	case HalfOpen:
		return "half-open"
	default:
		return "unknown"
	}
}

var ErrCircuitOpen = errors.New("circuit breaker is open")

type Stats struct {
	TotalCalls     int64
	Successes      int64
	Failures       int64
	RejectedCalls  int64
	State          State
}

func (s Stats) FailureRate() float64 {
	if s.TotalCalls == 0 {
		return 0
	}
	return float64(s.Failures) / float64(s.TotalCalls) * 100
}

type Config struct {
	FailureThreshold int
	SuccessThreshold int
	Timeout          time.Duration
}

type SimulatedCircuitBreaker struct {
	config           Config
	state           State
	failures        int
	successes       int
	openTime        time.Time
	stats           Stats
}

func NewSimulatedCircuitBreaker(config Config) *SimulatedCircuitBreaker {
	if config.FailureThreshold <= 0 {
		config.FailureThreshold = 5
	}
	if config.SuccessThreshold <= 0 {
		config.SuccessThreshold = 3
	}
	if config.Timeout <= 0 {
		config.Timeout = 30 * time.Second
	}
	return &SimulatedCircuitBreaker{
		config: config,
		state:  Closed,
	}
}

func (cb *SimulatedCircuitBreaker) Execute(ctx context.Context, fn func() (interface{}, error)) (interface{}, error) {
	// Check if circuit allows call
	if cb.state == Open {
		if time.Since(cb.openTime) >= cb.config.Timeout {
			cb.state = HalfOpen
			cb.successes = 0
		} else {
			cb.stats.RejectedCalls++
			return nil, ErrCircuitOpen
		}
	}
	
	cb.stats.TotalCalls++
	
	result, err := fn()
	
	if err != nil {
		cb.onFailure()
		return nil, err
	}
	
	cb.onSuccess()
	return result, nil
}

func (cb *SimulatedCircuitBreaker) onSuccess() {
	cb.stats.Successes++
	cb.failures = 0
	
	if cb.state == HalfOpen {
		cb.successes++
		if cb.successes >= cb.config.SuccessThreshold {
			cb.state = Closed
		}
	}
}

func (cb *SimulatedCircuitBreaker) onFailure() {
	cb.stats.Failures++
	cb.successes = 0
	
	switch cb.state {
	case Closed:
		cb.failures++
		if cb.failures >= cb.config.FailureThreshold {
			cb.state = Open
			cb.openTime = time.Now()
		}
	case HalfOpen:
		cb.state = Open
		cb.openTime = time.Now()
	}
}

func (cb *SimulatedCircuitBreaker) State() State { return cb.state }
func (cb *SimulatedCircuitBreaker) IsOpen() bool { return cb.state == Open }
func (cb *SimulatedCircuitBreaker) Stats() Stats { 
	return Stats{
		TotalCalls:    cb.stats.TotalCalls,
		Successes:     cb.stats.Successes,
		Failures:      cb.stats.Failures,
		RejectedCalls: cb.stats.RejectedCalls,
		State:        cb.state,
	}
}

func (cb *SimulatedCircuitBreaker) TimeUntilRetry() time.Duration {
	if cb.state != Open {
		return 0
	}
	remaining := cb.config.Timeout - time.Since(cb.openTime)
	if remaining < 0 {
		return 0
	}
	return remaining
}