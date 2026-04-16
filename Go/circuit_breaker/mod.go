// Package circuit_breaker provides a comprehensive circuit breaker implementation for Go applications.
// It implements the Circuit Breaker pattern for fault tolerance in distributed systems,
// providing automatic failure detection, recovery, and service protection.
//
// The circuit breaker has three states:
//   - Closed: Normal operation, requests flow through
//   - Open: Circuit is open, requests are blocked (fail-fast)
//   - HalfOpen: Testing if service has recovered
//
// Example usage:
//
//	// Create a circuit breaker
//	cb := circuit_breaker.New(circuit_breaker.Config{
//	    FailureThreshold:   5,
//	    SuccessThreshold:   3,
//	    Timeout:           30 * time.Second,
//	    MaxConcurrentCalls: 100,
//	})
//
//	// Execute function with circuit breaker protection
//	result, err := cb.Execute(ctx, func() (interface{}, error) {
//	    return someExternalService()
//	})
//
//	// Check circuit state
//	if cb.State() == circuit_breaker.Open {
//	    log.Println("Circuit is open, service unavailable")
//	}
//
//	// Get statistics
//	stats := cb.Stats()
//	fmt.Printf("Success: %d, Failures: %d, Rejected: %d\n",
//	    stats.Successes, stats.Failures, stats.Rejected)
//
// Features:
// - Zero dependencies, uses only Go standard library
// - Thread-safe implementations with sync.RWMutex
// - Three-state circuit breaker (Closed, Open, HalfOpen)
// - Configurable failure and success thresholds
// - Automatic recovery with timeout
// - Event hooks for monitoring
// - Statistics tracking
// - Context support for cancellation and timeouts
// - Production-ready for microservices and distributed systems
//
package circuit_breaker

import (
	"context"
	"errors"
	"sync"
	"time"
)

// =============================================================================
// Errors
// =============================================================================

var (
	// ErrCircuitOpen is returned when the circuit is open and requests are rejected.
	ErrCircuitOpen = errors.New("circuit breaker is open")

	// ErrTooManyConcurrentCalls is returned when max concurrent calls is exceeded.
	ErrTooManyConcurrentCalls = errors.New("too many concurrent calls")

	// ErrTimeout is returned when operation times out.
	ErrTimeout = errors.New("operation timed out")

	// ErrCancelled is returned when context is cancelled.
	ErrCancelled = errors.New("operation cancelled")
)

// =============================================================================
// State
// =============================================================================

// State represents the circuit breaker state.
type State int

const (
	// Closed state - normal operation, requests flow through.
	Closed State = iota
	// Open state - circuit is open, requests are blocked.
	Open
	// HalfOpen state - testing if service has recovered.
	HalfOpen
)

// String returns the string representation of the state.
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

// =============================================================================
// Event
// =============================================================================

// Event represents a circuit breaker event.
type Event int

const (
	EventStateChange Event = iota
	EventSuccess
	EventFailure
	EventRejected
	EventTimeout
	EventHalfOpenSuccess
	EventHalfOpenFailure
)

// String returns the string representation of the event.
func (e Event) String() string {
	switch e {
	case EventStateChange:
		return "state_change"
	case EventSuccess:
		return "success"
	case EventFailure:
		return "failure"
	case EventRejected:
		return "rejected"
	case EventTimeout:
		return "timeout"
	case EventHalfOpenSuccess:
		return "half_open_success"
	case EventHalfOpenFailure:
		return "half_open_failure"
	default:
		return "unknown"
	}
}

// =============================================================================
// Stats
// =============================================================================

// Stats holds circuit breaker statistics.
type Stats struct {
	TotalCalls      int64
	Successes       int64
	Failures        int64
	RejectedCalls   int64
	TimeoutCalls    int64
	ConcurrentCalls int64
	LastFailureTime time.Time
	LastSuccessTime time.Time
	State           State
}

// FailureRate returns the failure rate as a percentage.
func (s *Stats) FailureRate() float64 {
	if s.TotalCalls == 0 {
		return 0
	}
	return float64(s.Failures) / float64(s.TotalCalls) * 100
}

// SuccessRate returns the success rate as a percentage.
func (s *Stats) SuccessRate() float64 {
	if s.TotalCalls == 0 {
		return 0
	}
	return float64(s.Successes) / float64(s.TotalCalls) * 100
}

// =============================================================================
// Config
// =============================================================================

// Config holds circuit breaker configuration.
type Config struct {
	// FailureThreshold is the number of consecutive failures that trigger Open state.
	// Default: 5
	FailureThreshold int

	// SuccessThreshold is the number of consecutive successes in HalfOpen state
	// to transition back to Closed state.
	// Default: 3
	SuccessThreshold int

	// Timeout is the duration to wait in Open state before transitioning to HalfOpen.
	// Default: 30 seconds
	Timeout time.Duration

	// MaxConcurrentCalls is the maximum number of concurrent calls allowed.
	// Set to 0 for unlimited. Default: 0
	MaxConcurrentCalls int

	// TimeoutDuration is the timeout for each individual call.
	// Set to 0 for no timeout. Default: 0
	TimeoutDuration time.Duration

	// OnStateChange is called when state changes.
	OnStateChange func(oldState, newState State)

	// OnEvent is called for all events.
	OnEvent func(event Event, stats Stats)

	// IsFailure determines if an error should be counted as a failure.
	// If nil, all errors are counted as failures.
	IsFailure func(err error) bool
}

// DefaultConfig returns the default configuration.
func DefaultConfig() Config {
	return Config{
		FailureThreshold:   5,
		SuccessThreshold:   3,
		Timeout:           30 * time.Second,
		MaxConcurrentCalls: 0,
		TimeoutDuration:   0,
	}
}

// =============================================================================
// CircuitBreaker
// =============================================================================

// CircuitBreaker implements the circuit breaker pattern.
type CircuitBreaker struct {
	config Config

	mu               sync.RWMutex
	state            State
	failures         int
	successes        int
	concurrentCalls  int
	lastFailureTime  time.Time
	openTime         time.Time

	stats Stats

	// Counters
	totalCalls      int64
	successCount    int64
	failureCount    int64
	rejectedCount   int64
	timeoutCount    int64
	lastSuccessTime time.Time
}

// New creates a new circuit breaker with the given configuration.
func New(config Config) *CircuitBreaker {
	// Set defaults
	if config.FailureThreshold <= 0 {
		config.FailureThreshold = 5
	}
	if config.SuccessThreshold <= 0 {
		config.SuccessThreshold = 3
	}
	if config.Timeout <= 0 {
		config.Timeout = 30 * time.Second
	}

	return &CircuitBreaker{
		config: config,
		state:  Closed,
		stats:  Stats{State: Closed},
	}
}

// Execute runs the given function with circuit breaker protection.
// Returns ErrCircuitOpen if the circuit is open.
// Returns ErrTooManyConcurrentCalls if max concurrent calls is exceeded.
func (cb *CircuitBreaker) Execute(ctx context.Context, fn func() (interface{}, error)) (interface{}, error) {
	return cb.ExecuteWithFallback(ctx, fn, nil)
}

// ExecuteWithFallback runs the given function with circuit breaker protection
// and a fallback function when the circuit is open.
func (cb *CircuitBreaker) ExecuteWithFallback(ctx context.Context, fn func() (interface{}, error), fallback func(error) (interface{}, error)) (interface{}, error) {
	// Check if circuit allows the call
	if err := cb.beforeCall(); err != nil {
		if fallback != nil {
			return fallback(err)
		}
		return nil, err
	}

	// Track concurrent calls
	cb.incrementConcurrent()
	defer cb.decrementConcurrent()

	// Set up timeout if configured
	var cancel context.CancelFunc
	if cb.config.TimeoutDuration > 0 {
		ctx, cancel = context.WithTimeout(ctx, cb.config.TimeoutDuration)
		defer cancel()
	}

	// Channel to receive result
	type result struct {
		value interface{}
		err   error
	}
	resultCh := make(chan result, 1)

	// Execute in goroutine
	go func() {
		value, err := fn()
		resultCh <- result{value: value, err: err}
	}()

	// Wait for result or context cancellation
	select {
	case <-ctx.Done():
		cb.onTimeout()
		if fallback != nil {
			return fallback(ErrTimeout)
		}
		return nil, ErrTimeout

	case res := <-resultCh:
		if res.err != nil {
			cb.onFailure(res.err)
			return nil, res.err
		}
		cb.onSuccess()
		return res.value, nil
	}
}

// beforeCall checks if the call should be allowed.
func (cb *CircuitBreaker) beforeCall() error {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	// Check state
	switch cb.state {
	case Open:
		// Check if timeout has passed
		if time.Since(cb.openTime) >= cb.config.Timeout {
			// Transition to HalfOpen
			cb.transitionTo(HalfOpen)
		} else {
			// Reject the call
			cb.rejectedCount++
			cb.stats.RejectedCalls = cb.rejectedCount
			cb.stats.LastFailureTime = cb.lastFailureTime
			cb.emitEvent(EventRejected)
			return ErrCircuitOpen
		}

	case HalfOpen:
		// Allow limited calls in HalfOpen state
		// Check if max concurrent calls exceeded
		if cb.config.MaxConcurrentCalls > 0 && cb.concurrentCalls >= cb.config.MaxConcurrentCalls {
			cb.rejectedCount++
			cb.stats.RejectedCalls = cb.rejectedCount
			cb.emitEvent(EventRejected)
			return ErrTooManyConcurrentCalls
		}
	}

	// Check max concurrent calls
	if cb.config.MaxConcurrentCalls > 0 && cb.concurrentCalls >= cb.config.MaxConcurrentCalls {
		cb.rejectedCount++
		cb.stats.RejectedCalls = cb.rejectedCount
		cb.emitEvent(EventRejected)
		return ErrTooManyConcurrentCalls
	}

	cb.totalCalls++
	cb.stats.TotalCalls = cb.totalCalls
	return nil
}

// onSuccess handles a successful call.
func (cb *CircuitBreaker) onSuccess() {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	cb.successCount++
	cb.lastSuccessTime = time.Now()
	cb.stats.Successes = cb.successCount
	cb.stats.LastSuccessTime = cb.lastSuccessTime
	cb.stats.State = cb.state

	// Reset failure counter
	cb.failures = 0

	// Handle based on current state
	switch cb.state {
	case Closed:
		// Nothing to do, already closed
		cb.emitEvent(EventSuccess)

	case HalfOpen:
		cb.successes++
		cb.emitEvent(EventHalfOpenSuccess)

		// Check if we have enough successes to close
		if cb.successes >= cb.config.SuccessThreshold {
			cb.transitionTo(Closed)
		}
	}
}

// onFailure handles a failed call.
func (cb *CircuitBreaker) onFailure(err error) {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	// Check if error should be counted as failure
	if cb.config.IsFailure != nil && !cb.config.IsFailure(err) {
		return
	}

	cb.failureCount++
	cb.lastFailureTime = time.Now()
	cb.stats.Failures = cb.failureCount
	cb.stats.LastFailureTime = cb.lastFailureTime
	cb.stats.State = cb.state

	// Reset success counter
	cb.successes = 0

	// Handle based on current state
	switch cb.state {
	case Closed:
		cb.failures++
		cb.emitEvent(EventFailure)

		// Check if we should open
		if cb.failures >= cb.config.FailureThreshold {
			cb.transitionTo(Open)
		}

	case HalfOpen:
		cb.emitEvent(EventHalfOpenFailure)
		// Any failure in HalfOpen goes back to Open
		cb.transitionTo(Open)
	}
}

// onTimeout handles a timeout.
func (cb *CircuitBreaker) onTimeout() {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	cb.timeoutCount++
	cb.stats.TimeoutCalls = cb.timeoutCount
	cb.emitEvent(EventTimeout)

	// Treat timeout as failure
	cb.failureCount++
	cb.lastFailureTime = time.Now()
	cb.stats.Failures = cb.failureCount
	cb.stats.LastFailureTime = cb.lastFailureTime

	// Reset success counter
	cb.successes = 0

	switch cb.state {
	case Closed:
		cb.failures++
		if cb.failures >= cb.config.FailureThreshold {
			cb.transitionTo(Open)
		}

	case HalfOpen:
		cb.transitionTo(Open)
	}
}

// transitionTo transitions to a new state.
func (cb *CircuitBreaker) transitionTo(newState State) {
	oldState := cb.state
	cb.state = newState
	cb.stats.State = newState

	// Reset counters on state change
	if newState == Closed {
		cb.failures = 0
		cb.successes = 0
	} else if newState == HalfOpen {
		cb.successes = 0
	}

	if newState == Open {
		cb.openTime = time.Now()
	}

	// Emit state change event
	cb.emitEvent(EventStateChange)

	// Call callback if set
	if cb.config.OnStateChange != nil {
		go cb.config.OnStateChange(oldState, newState)
	}
}

// incrementConcurrent increments the concurrent call counter.
func (cb *CircuitBreaker) incrementConcurrent() {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	cb.concurrentCalls++
	cb.stats.ConcurrentCalls = int64(cb.concurrentCalls)
}

// decrementConcurrent decrements the concurrent call counter.
func (cb *CircuitBreaker) decrementConcurrent() {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	cb.concurrentCalls--
	cb.stats.ConcurrentCalls = int64(cb.concurrentCalls)
}

// emitEvent emits an event.
func (cb *CircuitBreaker) emitEvent(event Event) {
	if cb.config.OnEvent != nil {
		statsCopy := cb.getStatsLocked()
		go cb.config.OnEvent(event, statsCopy)
	}
}

// getStatsLocked returns a copy of stats (must hold lock).
func (cb *CircuitBreaker) getStatsLocked() Stats {
	return Stats{
		TotalCalls:      cb.totalCalls,
		Successes:       cb.successCount,
		Failures:       cb.failureCount,
		RejectedCalls:  cb.rejectedCount,
		TimeoutCalls:   cb.timeoutCount,
		ConcurrentCalls: int64(cb.concurrentCalls),
		LastFailureTime: cb.lastFailureTime,
		LastSuccessTime: cb.lastSuccessTime,
		State:          cb.state,
	}
}

// =============================================================================
// Public Methods
// =============================================================================

// State returns the current state of the circuit breaker.
func (cb *CircuitBreaker) State() State {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.state
}

// Stats returns current statistics.
func (cb *CircuitBreaker) Stats() Stats {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.getStatsLocked()
}

// Reset resets the circuit breaker to closed state with zero counters.
func (cb *CircuitBreaker) Reset() {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	cb.state = Closed
	cb.failures = 0
	cb.successes = 0
	cb.concurrentCalls = 0
	cb.totalCalls = 0
	cb.successCount = 0
	cb.failureCount = 0
	cb.rejectedCount = 0
	cb.timeoutCount = 0
	cb.stats = Stats{State: Closed}
}

// Trip manually trips (opens) the circuit breaker.
func (cb *CircuitBreaker) Trip() {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	if cb.state != Open {
		cb.transitionTo(Open)
	}
}

// Allow returns true if the circuit breaker allows the call.
// This is useful for manual integration.
func (cb *CircuitBreaker) Allow() bool {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	switch cb.state {
	case Closed:
		return true
	case Open:
		// Check if timeout has passed
		if time.Since(cb.openTime) >= cb.config.Timeout {
			cb.transitionTo(HalfOpen)
			return true
		}
		return false
	case HalfOpen:
		return true
	}
	return false
}

// RecordSuccess records a successful call (for manual integration).
func (cb *CircuitBreaker) RecordSuccess() {
	cb.onSuccess()
}

// RecordFailure records a failed call (for manual integration).
func (cb *CircuitBreaker) RecordFailure(err error) {
	cb.onFailure(err)
}

// Ready returns true if the circuit is ready to accept calls.
// This is similar to Allow but returns false in HalfOpen if max concurrent is reached.
func (cb *CircuitBreaker) Ready() bool {
	cb.mu.RLock()
	defer cb.mu.RUnlock()

	if cb.state == Open {
		return false
	}
	if cb.config.MaxConcurrentCalls > 0 && cb.concurrentCalls >= cb.config.MaxConcurrentCalls {
		return false
	}
	return true
}

// IsOpen returns true if the circuit is in Open state.
func (cb *CircuitBreaker) IsOpen() bool {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.state == Open
}

// IsClosed returns true if the circuit is in Closed state.
func (cb *CircuitBreaker) IsClosed() bool {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.state == Closed
}

// IsHalfOpen returns true if the circuit is in HalfOpen state.
func (cb *CircuitBreaker) IsHalfOpen() bool {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.state == HalfOpen
}

// TimeUntilRetry returns the duration until the circuit will allow retry.
// Returns 0 if the circuit is not open.
func (cb *CircuitBreaker) TimeUntilRetry() time.Duration {
	cb.mu.RLock()
	defer cb.mu.RUnlock()

	if cb.state != Open {
		return 0
	}

	remaining := cb.config.Timeout - time.Since(cb.openTime)
	if remaining < 0 {
		return 0
	}
	return remaining
}

// =============================================================================
// Runnable Interface
// =============================================================================

// Runnable is a function that returns an error.
type Runnable func() error

// Run executes the runnable with circuit breaker protection.
func (cb *CircuitBreaker) Run(ctx context.Context, r Runnable) error {
	_, err := cb.Execute(ctx, func() (interface{}, error) {
		return nil, r()
	})
	return err
}

// RunWithFallback executes the runnable with circuit breaker protection and fallback.
func (cb *CircuitBreaker) RunWithFallback(ctx context.Context, r Runnable, fallback func(error) error) error {
	_, err := cb.ExecuteWithFallback(ctx,
		func() (interface{}, error) {
			return nil, r()
		},
		func(e error) (interface{}, error) {
			return nil, fallback(e)
		},
	)
	return err
}

// =============================================================================
// Callable Interface
// =============================================================================

// Callable is a function that returns a value and an error.
type Callable func() (interface{}, error)

// Call executes the callable with circuit breaker protection.
func (cb *CircuitBreaker) Call(ctx context.Context, c Callable) (interface{}, error) {
	return cb.Execute(ctx, c)
}

// =============================================================================
// Batch Operations
// =============================================================================

// BatchResult holds the result of a batch operation.
type BatchResult struct {
	Results []interface{}
	Errors  []error
	Stats   Stats
}

// ExecuteBatch executes multiple operations with circuit breaker protection.
func (cb *CircuitBreaker) ExecuteBatch(ctx context.Context, fns []func() (interface{}, error)) BatchResult {
	results := make([]interface{}, len(fns))
	errs := make([]error, len(fns))

	var wg sync.WaitGroup

	for i, fn := range fns {
		wg.Add(1)
		go func(idx int, f func() (interface{}, error)) {
			defer wg.Done()
			results[idx], errs[idx] = cb.Execute(ctx, f)
		}(i, fn)
	}

	wg.Wait()

	return BatchResult{
		Results: results,
		Errors:  errs,
		Stats:   cb.Stats(),
	}
}

// =============================================================================
// Health Check
// =============================================================================

// HealthStatus represents the health status of the circuit breaker.
type HealthStatus struct {
	State           State
	Healthy         bool
	FailureRate     float64
	SuccessRate     float64
	TotalCalls      int64
	ConcurrentCalls int64
	LastFailure     time.Time
	LastSuccess     time.Time
	TimeUntilRetry  time.Duration
}

// Health returns the health status of the circuit breaker.
func (cb *CircuitBreaker) Health() HealthStatus {
	cb.mu.RLock()
	defer cb.mu.RUnlock()

	stats := cb.getStatsLocked()

	healthy := cb.state == Closed || cb.state == HalfOpen

	var timeUntilRetry time.Duration
	if cb.state == Open {
		timeUntilRetry = cb.config.Timeout - time.Since(cb.openTime)
		if timeUntilRetry < 0 {
			timeUntilRetry = 0
		}
	}

	return HealthStatus{
		State:           cb.state,
		Healthy:         healthy,
		FailureRate:     stats.FailureRate(),
		SuccessRate:     stats.SuccessRate(),
		TotalCalls:      stats.TotalCalls,
		ConcurrentCalls: stats.ConcurrentCalls,
		LastFailure:     stats.LastFailureTime,
		LastSuccess:     stats.LastSuccessTime,
		TimeUntilRetry:  timeUntilRetry,
	}
}

// =============================================================================
// String Representation
// =============================================================================

// String returns a string representation of the circuit breaker.
func (cb *CircuitBreaker) String() string {
	stats := cb.Stats()
	return "CircuitBreaker{" +
		"state=" + cb.State().String() +
		", failures=" + formatInt(stats.Failures) +
		", successes=" + formatInt(stats.Successes) +
		", rejected=" + formatInt(stats.RejectedCalls) +
		"}"
}

func formatInt(n int64) string {
	if n < 1000 {
		return string(rune('0'+n%10))
	}
	return string(rune('0'+(n/1000)%10)) + "k+" + formatInt(n%1000)
}