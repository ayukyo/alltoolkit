// Package retry_utils provides flexible retry mechanisms with exponential backoff,
// jitter, context cancellation support, and customizable retry strategies.
package retry_utils

import (
	"context"
	"errors"
	"fmt"
	"math"
	"math/rand"
	"sync"
	"time"
)

// RetryableFunc is a function that can be retried.
type RetryableFunc func() error

// RetryableFuncWithContext is a function that can be retried with context support.
type RetryableFuncWithContext func(ctx context.Context) error

// Config holds the retry configuration.
type Config struct {
	// MaxAttempts is the maximum number of retry attempts (including the initial attempt).
	// Default is 3.
	MaxAttempts int

	// InitialDelay is the initial delay between retries.
	// Default is 100ms.
	InitialDelay time.Duration

	// MaxDelay is the maximum delay between retries.
	// Default is 30s.
	MaxDelay time.Duration

	// Multiplier is the backoff multiplier for exponential backoff.
	// Default is 2.0.
	Multiplier float64

	// Jitter adds randomization to delays to prevent thundering herd.
	// Value should be between 0 and 1. Default is 0.1 (10% jitter).
	Jitter float64

	// MaxJitter is the maximum jitter duration when JitterMode is set to JitterModeFixed.
	// If this is set, Jitter value is ignored.
	MaxJitter time.Duration

	// JitterMode determines how jitter is applied.
	// Default is JitterModePercentage.
	JitterMode JitterMode

	// RetryOn defines which errors should trigger a retry.
	// If nil, all errors trigger retry.
	RetryOn func(error) bool

	// OnRetry is called before each retry attempt with the current attempt number and error.
	OnRetry func(attempt int, err error)

	// OnSuccess is called after successful execution.
	OnSuccess func(attempts int, totalDuration time.Duration)

	// OnFailure is called after all attempts are exhausted.
	OnFailure func(attempts int, totalDuration time.Duration, lastErr error)

	// Timeout is the maximum total duration for all attempts.
	// If 0, no timeout is enforced.
	Timeout time.Duration
}

// JitterMode determines how jitter is calculated.
type JitterMode int

const (
	// JitterModePercentage applies jitter as a percentage of the delay.
	JitterModePercentage JitterMode = iota
	// JitterModeFixed applies a fixed random jitter duration.
	JitterModeFixed
)

// Result holds the result of a retry operation.
type Result struct {
	// Attempts is the total number of attempts made.
	Attempts int
	// Duration is the total time spent on all attempts.
	Duration time.Duration
	// Error is the last error encountered (nil if successful).
	Error error
	// Success indicates if the operation succeeded.
	Success bool
}

// DefaultConfig returns a Config with sensible defaults.
func DefaultConfig() Config {
	return Config{
		MaxAttempts:  3,
		InitialDelay: 100 * time.Millisecond,
		MaxDelay:     30 * time.Second,
		Multiplier:   2.0,
		Jitter:       0.1,
		JitterMode:   JitterModePercentage,
	}
}

// NewConfig creates a new Config with optional modifications.
func NewConfig(opts ...func(*Config)) Config {
	cfg := DefaultConfig()
	for _, opt := range opts {
		opt(&cfg)
	}
	return cfg
}

// WithMaxAttempts sets the maximum number of attempts.
func WithMaxAttempts(n int) func(*Config) {
	return func(c *Config) { c.MaxAttempts = n }
}

// WithInitialDelay sets the initial delay.
func WithInitialDelay(d time.Duration) func(*Config) {
	return func(c *Config) { c.InitialDelay = d }
}

// WithMaxDelay sets the maximum delay.
func WithMaxDelay(d time.Duration) func(*Config) {
	return func(c *Config) { c.MaxDelay = d }
}

// WithMultiplier sets the backoff multiplier.
func WithMultiplier(m float64) func(*Config) {
	return func(c *Config) { c.Multiplier = m }
}

// WithJitter sets the jitter percentage (0-1).
func WithJitter(j float64) func(*Config) {
	return func(c *Config) { c.Jitter = j }
}

// WithMaxJitter sets the maximum fixed jitter duration.
func WithMaxJitter(d time.Duration) func(*Config) {
	return func(c *Config) {
		c.MaxJitter = d
		c.JitterMode = JitterModeFixed
	}
}

// WithRetryOn sets the error filter function.
func WithRetryOn(fn func(error) bool) func(*Config) {
	return func(c *Config) { c.RetryOn = fn }
}

// WithOnRetry sets the retry callback.
func WithOnRetry(fn func(int, error)) func(*Config) {
	return func(c *Config) { c.OnRetry = fn }
}

// WithTimeout sets the total timeout for all attempts.
func WithTimeout(d time.Duration) func(*Config) {
	return func(c *Config) { c.Timeout = d }
}

// Do executes the given function with retry logic.
func Do(fn RetryableFunc, opts ...func(*Config)) Result {
	return DoWithContext(context.Background(), func(ctx context.Context) error {
		return fn()
	}, opts...)
}

// DoWithContext executes the given function with retry logic and context support.
func DoWithContext(ctx context.Context, fn RetryableFuncWithContext, opts ...func(*Config)) Result {
	cfg := NewConfig(opts...)
	return execute(ctx, fn, cfg)
}

// execute performs the retry logic.
func execute(ctx context.Context, fn RetryableFuncWithContext, cfg Config) Result {
	start := time.Now()

	if cfg.MaxAttempts < 1 {
		cfg.MaxAttempts = 1
	}
	if cfg.InitialDelay < 0 {
		cfg.InitialDelay = 0
	}
	if cfg.MaxDelay < 0 {
		cfg.MaxDelay = 0
	}
	if cfg.Multiplier < 1 {
		cfg.Multiplier = 1
	}
	if cfg.Jitter < 0 {
		cfg.Jitter = 0
	}
	if cfg.Jitter > 1 {
		cfg.Jitter = 1
	}

	var ctxWithTimeout context.Context
	var cancel context.CancelFunc
	if cfg.Timeout > 0 {
		ctxWithTimeout, cancel = context.WithTimeout(ctx, cfg.Timeout)
		defer cancel()
	} else {
		ctxWithTimeout = ctx
	}

	var lastErr error
	attempt := 0

	for attempt < cfg.MaxAttempts {
		attempt++

		select {
		case <-ctxWithTimeout.Done():
			return Result{
				Attempts: attempt,
				Duration: time.Since(start),
				Error:    ctxWithTimeout.Err(),
				Success:  false,
			}
		default:
		}

		err := fn(ctxWithTimeout)
		if err == nil {
			result := Result{
				Attempts: attempt,
				Duration: time.Since(start),
				Error:    nil,
				Success:  true,
			}
			if cfg.OnSuccess != nil {
				cfg.OnSuccess(attempt, result.Duration)
			}
			return result
		}

		lastErr = err

		// Check if we should retry this error
		if cfg.RetryOn != nil && !cfg.RetryOn(err) {
			return Result{
				Attempts: attempt,
				Duration: time.Since(start),
				Error:    err,
				Success:  false,
			}
		}

		// Check if we've exhausted attempts
		if attempt >= cfg.MaxAttempts {
			break
		}

		// Calculate delay
		delay := calculateDelay(attempt, cfg)

		// Notify retry callback
		if cfg.OnRetry != nil {
			cfg.OnRetry(attempt, err)
		}

		// Wait for delay or context cancellation
		select {
		case <-ctxWithTimeout.Done():
			return Result{
				Attempts: attempt,
				Duration: time.Since(start),
				Error:    ctxWithTimeout.Err(),
				Success:  false,
			}
		case <-time.After(delay):
		}
	}

	result := Result{
		Attempts: attempt,
		Duration: time.Since(start),
		Error:    lastErr,
		Success:  false,
	}

	if cfg.OnFailure != nil {
		cfg.OnFailure(attempt, result.Duration, lastErr)
	}

	return result
}

// calculateDelay calculates the delay for a given attempt.
func calculateDelay(attempt int, cfg Config) time.Duration {
	// Calculate exponential delay
	delay := float64(cfg.InitialDelay) * math.Pow(cfg.Multiplier, float64(attempt-1))

	// Apply max delay cap
	if delay > float64(cfg.MaxDelay) {
		delay = float64(cfg.MaxDelay)
	}

	// Apply jitter
	jitter := calculateJitter(time.Duration(delay), cfg)
	delay = delay + float64(jitter)

	return time.Duration(delay)
}

// calculateJitter calculates the jitter for a given delay.
func calculateJitter(delay time.Duration, cfg Config) time.Duration {
	if cfg.JitterMode == JitterModeFixed && cfg.MaxJitter > 0 {
		// Fixed jitter mode
		return time.Duration(rand.Float64() * float64(cfg.MaxJitter))
	}

	if cfg.Jitter <= 0 {
		return 0
	}

	// Percentage jitter mode
	jitterRange := float64(delay) * cfg.Jitter
	jitter := (rand.Float64()*2 - 1) * jitterRange // -jitterRange to +jitterRange
	return time.Duration(jitter)
}

// PermanentError wraps an error to indicate it should not be retried.
type PermanentError struct {
	Err error
}

func (e *PermanentError) Error() string { return e.Err.Error() }
func (e *PermanentError) Unwrap() error  { return e.Err }

// Permanent wraps an error to indicate it should not be retried.
func Permanent(err error) error {
	return &PermanentError{Err: err}
}

// IsPermanent checks if an error is a permanent error.
func IsPermanent(err error) bool {
	var perm *PermanentError
	return errors.As(err, &perm)
}

// TransientError wraps an error to indicate it can be retried.
type TransientError struct {
	Err error
}

func (e *TransientError) Error() string { return e.Err.Error() }
func (e *TransientError) Unwrap() error  { return e.Err }

// Transient wraps an error to indicate it can be retried.
func Transient(err error) error {
	return &TransientError{Err: err}
}

// IsTransient checks if an error is a transient error.
func IsTransient(err error) bool {
	var trans *TransientError
	return errors.As(err, &trans)
}

// RetriableError wraps an error with retry metadata.
type RetriableError struct {
	Err        error
	RetryAfter time.Duration
}

func (e *RetriableError) Error() string {
	if e.RetryAfter > 0 {
		return fmt.Sprintf("%s (retry after %v)", e.Err, e.RetryAfter)
	}
	return e.Err.Error()
}

func (e *RetriableError) Unwrap() error { return e.Err }

// RetryAfter creates a retriable error with a suggested retry delay.
func RetryAfter(err error, after time.Duration) error {
	return &RetriableError{Err: err, RetryAfter: after}
}

// CircuitBreaker implements the circuit breaker pattern.
type CircuitBreaker struct {
	mu              sync.RWMutex
	maxFailures     int
	resetTimeout    time.Duration
	state           State
	failures        int
	lastFailTime    time.Time
	onStateChange   func(old, new State)
	halfOpenSuccess int
	halfOpenMax     int
}

// State represents the circuit breaker state.
type State int

const (
	// StateClosed means the circuit is closed and requests go through.
	StateClosed State = iota
	// StateOpen means the circuit is open and requests are rejected.
	StateOpen
	// StateHalfOpen means the circuit is testing if it should close.
	StateHalfOpen
)

// NewCircuitBreaker creates a new circuit breaker.
func NewCircuitBreaker(maxFailures int, resetTimeout time.Duration, opts ...func(*CircuitBreaker)) *CircuitBreaker {
	cb := &CircuitBreaker{
		maxFailures:  maxFailures,
		resetTimeout: resetTimeout,
		state:        StateClosed,
		halfOpenMax:  1,
	}
	for _, opt := range opts {
		opt(cb)
	}
	return cb
}

// WithOnStateChange sets the state change callback.
func WithOnStateChange(fn func(old, new State)) func(*CircuitBreaker) {
	return func(cb *CircuitBreaker) { cb.onStateChange = fn }
}

// WithHalfOpenMax sets the number of successful requests needed in half-open state.
func WithHalfOpenMax(n int) func(*CircuitBreaker) {
	return func(cb *CircuitBreaker) { cb.halfOpenMax = n }
}

// State returns the current state of the circuit breaker.
func (cb *CircuitBreaker) State() State {
	cb.mu.RLock()
	defer cb.mu.RUnlock()
	return cb.currentState()
}

// currentState returns the current state without locking.
func (cb *CircuitBreaker) currentState() State {
	if cb.state == StateOpen {
		if time.Since(cb.lastFailTime) >= cb.resetTimeout {
			return StateHalfOpen
		}
	}
	return cb.state
}

// Execute runs the function through the circuit breaker.
func (cb *CircuitBreaker) Execute(fn func() error) error {
	cb.mu.Lock()
	state := cb.currentState()

	switch state {
	case StateOpen:
		cb.mu.Unlock()
		return errors.New("circuit breaker is open")
	case StateHalfOpen:
		// Allow one request through
	default:
		// StateClosed: proceed normally
	}
	cb.mu.Unlock()

	err := fn()

	cb.mu.Lock()
	defer cb.mu.Unlock()

	if err == nil {
		cb.onSuccess()
		return nil
	}

	cb.onFailure()
	return err
}

// onSuccess handles successful execution.
func (cb *CircuitBreaker) onSuccess() {
	cb.failures = 0

	if cb.state == StateHalfOpen {
		cb.halfOpenSuccess++
		if cb.halfOpenSuccess >= cb.halfOpenMax {
			cb.setState(StateClosed)
		}
	}
}

// onFailure handles failed execution.
func (cb *CircuitBreaker) onFailure() {
	cb.failures++
	cb.lastFailTime = time.Now()

	if cb.state == StateHalfOpen {
		cb.setState(StateOpen)
	} else if cb.failures >= cb.maxFailures {
		cb.setState(StateOpen)
	}
}

// setState changes the circuit breaker state.
func (cb *CircuitBreaker) setState(newState State) {
	if cb.state != newState {
		oldState := cb.state
		cb.state = newState
		cb.halfOpenSuccess = 0
		if cb.onStateChange != nil {
			cb.onStateChange(oldState, newState)
		}
	}
}

// Reset resets the circuit breaker to closed state.
func (cb *CircuitBreaker) Reset() {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	cb.setState(StateClosed)
	cb.failures = 0
}

// Rate is a rate limiter that allows limiting the number of retries per time period.
type Rate struct {
	mu       sync.Mutex
	tokens   float64
	max      float64
	rate     float64 // tokens per second
	lastTime time.Time
}

// NewRateLimiter creates a new rate limiter.
func NewRateLimiter(rate float64, burst int) *Rate {
	return &Rate{
		tokens:   float64(burst),
		max:      float64(burst),
		rate:     rate,
		lastTime: time.Now(),
	}
}

// Allow checks if a retry is allowed.
func (r *Rate) Allow() bool {
	return r.AllowN(1)
}

// AllowN checks if n retries are allowed.
func (r *Rate) AllowN(n int) bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(r.lastTime).Seconds()
	r.lastTime = now

	r.tokens = math.Min(r.max, r.tokens+elapsed*r.rate)

	if r.tokens >= float64(n) {
		r.tokens -= float64(n)
		return true
	}

	return false
}

// Wait blocks until a retry is allowed or context is cancelled.
func (r *Rate) Wait(ctx context.Context) error {
	return r.WaitN(ctx, 1)
}

// WaitN blocks until n retries are allowed or context is cancelled.
func (r *Rate) WaitN(ctx context.Context, n int) error {
	for {
		if r.AllowN(n) {
			return nil
		}

		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(10 * time.Millisecond):
		}
	}
}

// RetryableError types for common scenarios.
var (
	// ErrMaxRetries indicates max retries exceeded.
	ErrMaxRetries = errors.New("maximum retry attempts exceeded")
	// ErrCircuitOpen indicates circuit breaker is open.
	ErrCircuitOpen = errors.New("circuit breaker is open")
	// ErrTimeout indicates timeout exceeded.
	ErrTimeout = errors.New("operation timed out")
)

// Builder provides a fluent interface for building retry configurations.
type Builder struct {
	config Config
}

// NewBuilder creates a new configuration builder.
func NewBuilder() *Builder {
	return &Builder{config: DefaultConfig()}
}

// MaxAttempts sets the maximum attempts.
func (b *Builder) MaxAttempts(n int) *Builder {
	b.config.MaxAttempts = n
	return b
}

// InitialDelay sets the initial delay.
func (b *Builder) InitialDelay(d time.Duration) *Builder {
	b.config.InitialDelay = d
	return b
}

// MaxDelay sets the maximum delay.
func (b *Builder) MaxDelay(d time.Duration) *Builder {
	b.config.MaxDelay = d
	return b
}

// Multiplier sets the backoff multiplier.
func (b *Builder) Multiplier(m float64) *Builder {
	b.config.Multiplier = m
	return b
}

// Jitter sets the jitter percentage.
func (b *Builder) Jitter(j float64) *Builder {
	b.config.Jitter = j
	return b
}

// FixedJitter sets the fixed jitter mode with max duration.
func (b *Builder) FixedJitter(d time.Duration) *Builder {
	b.config.MaxJitter = d
	b.config.JitterMode = JitterModeFixed
	return b
}

// RetryOn sets the error filter.
func (b *Builder) RetryOn(fn func(error) bool) *Builder {
	b.config.RetryOn = fn
	return b
}

// OnRetry sets the retry callback.
func (b *Builder) OnRetry(fn func(int, error)) *Builder {
	b.config.OnRetry = fn
	return b
}

// Timeout sets the total timeout.
func (b *Builder) Timeout(d time.Duration) *Builder {
	b.config.Timeout = d
	return b
}

// Build returns the configured Config.
func (b *Builder) Build() Config {
	return b.config
}

// Do executes the function with the built configuration.
func (b *Builder) Do(fn RetryableFunc) Result {
	return Do(fn, func(c *Config) { *c = b.config })
}

// DoWithContext executes the function with context and the built configuration.
func (b *Builder) DoWithContext(ctx context.Context, fn RetryableFuncWithContext) Result {
	return DoWithContext(ctx, fn, func(c *Config) { *c = b.config })
}

// ExponentialBackoff creates a simple exponential backoff retry.
func ExponentialBackoff(fn RetryableFunc, maxAttempts int, initialDelay time.Duration) Result {
	return Do(fn,
		WithMaxAttempts(maxAttempts),
		WithInitialDelay(initialDelay),
		WithMultiplier(2.0),
	)
}

// FixedDelay creates a fixed delay retry.
func FixedDelay(fn RetryableFunc, maxAttempts int, delay time.Duration) Result {
	return Do(fn,
		WithMaxAttempts(maxAttempts),
		WithInitialDelay(delay),
		WithMultiplier(1.0),
		WithJitter(0),
	)
}

// LinearBackoff creates a linear backoff retry.
func LinearBackoff(fn RetryableFunc, maxAttempts int, initialDelay time.Duration) Result {
	return Do(fn,
		WithMaxAttempts(maxAttempts),
		WithInitialDelay(initialDelay),
		WithMultiplier(1.0),
		WithJitter(0.1),
	)
}

// UntilSuccess retries until success or context cancellation.
func UntilSuccess(ctx context.Context, fn RetryableFuncWithContext, delay time.Duration) Result {
	start := time.Now()
	attempts := 0

	for {
		attempts++
		err := fn(ctx)
		if err == nil {
			return Result{
				Attempts: attempts,
				Duration: time.Since(start),
				Success:  true,
			}
		}

		select {
		case <-ctx.Done():
			return Result{
				Attempts: attempts,
				Duration: time.Since(start),
				Error:    ctx.Err(),
				Success:  false,
			}
		case <-time.After(delay):
		}
	}
}