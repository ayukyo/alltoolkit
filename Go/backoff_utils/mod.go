// Package backoff_utils provides backoff algorithms for retry mechanisms.
// Zero external dependencies - pure Go standard library implementation.
//
// Features:
//   - Exponential Backoff with configurable base and multiplier
//   - Jitter strategies (Full, Equal, Decorrelated)
//   - Maximum retry limit and timeout support
//   - Context cancellation support
//   - Custom backoff policies
package backoff_utils

import (
	"context"
	"errors"
	"math"
	"math/rand"
	"sync"
	"time"
)

// BackoffStrategy defines the interface for backoff strategies
type BackoffStrategy interface {
	// Next returns the duration to wait before the next retry attempt.
	// attempt is the current attempt number (0-indexed).
	Next(attempt int) time.Duration
	// Reset resets the backoff strategy to its initial state
	Reset()
}

// Config holds the configuration for backoff strategies
type Config struct {
	// BaseDelay is the initial delay duration
	BaseDelay time.Duration
	// MaxDelay is the maximum delay duration
	MaxDelay time.Duration
	// Multiplier is the factor by which the delay increases
	Multiplier float64
	// JitterFraction is the fraction of jitter to add (0.0 to 1.0)
	JitterFraction float64
	// MaxRetries is the maximum number of retry attempts (0 = unlimited)
	MaxRetries int
}

// DefaultConfig returns a Config with sensible defaults
func DefaultConfig() Config {
	return Config{
		BaseDelay:      100 * time.Millisecond,
		MaxDelay:       30 * time.Second,
		Multiplier:     2.0,
		JitterFraction: 0.0,
		MaxRetries:     5,
	}
}

// ExponentialBackoff implements exponential backoff strategy
type ExponentialBackoff struct {
	config Config
	mu     sync.Mutex
}

// NewExponentialBackoff creates a new ExponentialBackoff with the given config
func NewExponentialBackoff(config Config) *ExponentialBackoff {
	if config.BaseDelay <= 0 {
		config.BaseDelay = DefaultConfig().BaseDelay
	}
	if config.MaxDelay <= 0 {
		config.MaxDelay = DefaultConfig().MaxDelay
	}
	if config.Multiplier <= 1 {
		config.Multiplier = DefaultConfig().Multiplier
	}
	if config.JitterFraction < 0 || config.JitterFraction > 1 {
		config.JitterFraction = 0
	}
	return &ExponentialBackoff{config: config}
}

// Next returns the duration to wait before the next retry attempt
func (b *ExponentialBackoff) Next(attempt int) time.Duration {
	b.mu.Lock()
	defer b.mu.Unlock()

	if attempt < 0 {
		return b.config.BaseDelay
	}

	// Calculate exponential delay
	delay := float64(b.config.BaseDelay) * math.Pow(b.config.Multiplier, float64(attempt))
	
	// Cap at max delay
	if delay > float64(b.config.MaxDelay) {
		delay = float64(b.config.MaxDelay)
	}

	return time.Duration(delay)
}

// Reset resets the backoff strategy
func (b *ExponentialBackoff) Reset() {
	// ExponentialBackoff is stateless, nothing to reset
}

// WithJitter wraps a backoff strategy with jitter
type WithJitter struct {
	strategy       BackoffStrategy
	jitterFraction float64
	rand           *rand.Rand
	mu             sync.Mutex
}

// JitterType defines the type of jitter to apply
type JitterType int

const (
	// JitterFull applies full jitter (random value between 0 and delay)
	JitterFull JitterType = iota
	// JitterEqual applies equal jitter (random value between delay/2 and 3*delay/2)
	JitterEqual
	// JitterDecorrelated applies decorrelated jitter
	JitterDecorrelated
)

// NewWithJitter wraps a backoff strategy with jitter
func NewWithJitter(strategy BackoffStrategy, jitterFraction float64) *WithJitter {
	if jitterFraction < 0 {
		jitterFraction = 0
	}
	if jitterFraction > 1 {
		jitterFraction = 1
	}
	return &WithJitter{
		strategy:       strategy,
		jitterFraction: jitterFraction,
		rand:           rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// Next returns the duration with jitter applied
func (j *WithJitter) Next(attempt int) time.Duration {
	delay := j.strategy.Next(attempt)

	j.mu.Lock()
	defer j.mu.Unlock()

	// Apply jitter
	jitter := float64(delay) * j.jitterFraction * j.rand.Float64()
	return time.Duration(float64(delay) - j.jitterFraction*float64(delay)/2 + jitter)
}

// Reset resets the backoff strategy
func (j *WithJitter) Reset() {
	j.strategy.Reset()
}

// FullJitterBackoff implements full jitter strategy
type FullJitterBackoff struct {
	config Config
	rand   *rand.Rand
	mu     sync.Mutex
}

// NewFullJitterBackoff creates a new FullJitterBackoff
func NewFullJitterBackoff(config Config) *FullJitterBackoff {
	if config.BaseDelay <= 0 {
		config.BaseDelay = DefaultConfig().BaseDelay
	}
	if config.MaxDelay <= 0 {
		config.MaxDelay = DefaultConfig().MaxDelay
	}
	if config.Multiplier <= 1 {
		config.Multiplier = DefaultConfig().Multiplier
	}
	return &FullJitterBackoff{
		config: config,
		rand:   rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// Next returns a random duration between 0 and the calculated delay
func (b *FullJitterBackoff) Next(attempt int) time.Duration {
	b.mu.Lock()
	defer b.mu.Unlock()

	delay := float64(b.config.BaseDelay) * math.Pow(b.config.Multiplier, float64(attempt))
	if delay > float64(b.config.MaxDelay) {
		delay = float64(b.config.MaxDelay)
	}

	// Full jitter: random between 0 and delay
	return time.Duration(b.rand.Float64() * delay)
}

// Reset resets the backoff strategy
func (b *FullJitterBackoff) Reset() {
	// Stateless, nothing to reset
}

// EqualJitterBackoff implements equal jitter strategy
type EqualJitterBackoff struct {
	config Config
	rand   *rand.Rand
	mu     sync.Mutex
}

// NewEqualJitterBackoff creates a new EqualJitterBackoff
func NewEqualJitterBackoff(config Config) *EqualJitterBackoff {
	if config.BaseDelay <= 0 {
		config.BaseDelay = DefaultConfig().BaseDelay
	}
	if config.MaxDelay <= 0 {
		config.MaxDelay = DefaultConfig().MaxDelay
	}
	if config.Multiplier <= 1 {
		config.Multiplier = DefaultConfig().Multiplier
	}
	return &EqualJitterBackoff{
		config: config,
		rand:   rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// Next returns delay/2 + random(0, delay/2)
func (b *EqualJitterBackoff) Next(attempt int) time.Duration {
	b.mu.Lock()
	defer b.mu.Unlock()

	delay := float64(b.config.BaseDelay) * math.Pow(b.config.Multiplier, float64(attempt))
	if delay > float64(b.config.MaxDelay) {
		delay = float64(b.config.MaxDelay)
	}

	// Equal jitter: delay/2 + random(0, delay/2)
	halfDelay := delay / 2
	return time.Duration(halfDelay + b.rand.Float64()*halfDelay)
}

// Reset resets the backoff strategy
func (b *EqualJitterBackoff) Reset() {
	// Stateless, nothing to reset
}

// DecorrelatedJitterBackoff implements decorrelated jitter strategy
type DecorrelatedJitterBackoff struct {
	config    Config
	rand      *rand.Rand
	lastDelay time.Duration
	mu        sync.Mutex
}

// NewDecorrelatedJitterBackoff creates a new DecorrelatedJitterBackoff
func NewDecorrelatedJitterBackoff(config Config) *DecorrelatedJitterBackoff {
	if config.BaseDelay <= 0 {
		config.BaseDelay = DefaultConfig().BaseDelay
	}
	if config.MaxDelay <= 0 {
		config.MaxDelay = DefaultConfig().MaxDelay
	}
	if config.Multiplier <= 1 {
		config.Multiplier = DefaultConfig().Multiplier
	}
	return &DecorrelatedJitterBackoff{
		config:    config,
		rand:      rand.New(rand.NewSource(time.Now().UnixNano())),
		lastDelay: 0,
	}
}

// Next returns a decorrelated jitter duration
func (b *DecorrelatedJitterBackoff) Next(attempt int) time.Duration {
	b.mu.Lock()
	defer b.mu.Unlock()

	var delay float64
	if b.lastDelay == 0 {
		delay = float64(b.config.BaseDelay)
	} else {
		// New delay = min(cap, random(base, sleep * multiplier))
		minDelay := float64(b.config.BaseDelay)
		maxDelay := float64(b.lastDelay) * b.config.Multiplier
		delay = minDelay + b.rand.Float64()*(maxDelay-minDelay)
	}

	if delay > float64(b.config.MaxDelay) {
		delay = float64(b.config.MaxDelay)
	}

	b.lastDelay = time.Duration(delay)
	return b.lastDelay
}

// Reset resets the backoff strategy
func (b *DecorrelatedJitterBackoff) Reset() {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.lastDelay = 0
}

// LinearBackoff implements linear backoff strategy
type LinearBackoff struct {
	config Config
	mu     sync.Mutex
}

// NewLinearBackoff creates a new LinearBackoff
func NewLinearBackoff(config Config) *LinearBackoff {
	if config.BaseDelay <= 0 {
		config.BaseDelay = DefaultConfig().BaseDelay
	}
	if config.MaxDelay <= 0 {
		config.MaxDelay = DefaultConfig().MaxDelay
	}
	return &LinearBackoff{config: config}
}

// Next returns base + (attempt * base) duration
func (b *LinearBackoff) Next(attempt int) time.Duration {
	b.mu.Lock()
	defer b.mu.Unlock()

	if attempt < 0 {
		return b.config.BaseDelay
	}

	delay := float64(b.config.BaseDelay) * float64(attempt+1)
	if delay > float64(b.config.MaxDelay) {
		delay = float64(b.config.MaxDelay)
	}

	return time.Duration(delay)
}

// Reset resets the backoff strategy
func (b *LinearBackoff) Reset() {
	// Stateless, nothing to reset
}

// ConstantBackoff implements constant backoff strategy
type ConstantBackoff struct {
	delay time.Duration
	mu    sync.Mutex
}

// NewConstantBackoff creates a new ConstantBackoff
func NewConstantBackoff(delay time.Duration) *ConstantBackoff {
	if delay <= 0 {
		delay = 100 * time.Millisecond
	}
	return &ConstantBackoff{delay: delay}
}

// Next returns the constant delay
func (b *ConstantBackoff) Next(attempt int) time.Duration {
	return b.delay
}

// Reset resets the backoff strategy
func (b *ConstantBackoff) Reset() {
	// Stateless, nothing to reset
}

// RetryError represents an error from retry attempts
type RetryError struct {
	Err     error
	Attempt int
}

// Error implements the error interface
func (e *RetryError) Error() string {
	return e.Err.Error()
}

// Unwrap returns the underlying error
func (e *RetryError) Unwrap() error {
	return e.Err
}

// ErrMaxRetriesExceeded is returned when max retries are exceeded
var ErrMaxRetriesExceeded = errors.New("maximum retries exceeded")

// ErrContextCanceled is returned when context is canceled
var ErrContextCanceled = errors.New("context canceled")

// RetryableFunc is a function that can be retried
type RetryableFunc func() error

// RetryableFuncWithResult is a function that returns a result and can be retried
type RetryableFuncWithResult[T any] func() (T, error)

// Retrier handles retry logic with backoff
type Retrier struct {
	strategy BackoffStrategy
	config   Config
}

// NewRetrier creates a new Retrier with the given backoff strategy
func NewRetrier(strategy BackoffStrategy, config Config) *Retrier {
	return &Retrier{
		strategy: strategy,
		config:   config,
	}
}

// Do executes the function with retry logic
func (r *Retrier) Do(ctx context.Context, fn RetryableFunc) error {
	return r.DoWithRetry(ctx, fn, r.config.MaxRetries)
}

// DoWithRetry executes the function with a specific max retry count
func (r *Retrier) DoWithRetry(ctx context.Context, fn RetryableFunc, maxRetries int) error {
	var lastErr error

	for attempt := 0; ; attempt++ {
		// Check context
		select {
		case <-ctx.Done():
			return &RetryError{Err: ErrContextCanceled, Attempt: attempt}
		default:
		}

		// Check max retries
		if maxRetries > 0 && attempt >= maxRetries {
			if lastErr != nil {
				return &RetryError{Err: lastErr, Attempt: attempt}
			}
			return &RetryError{Err: ErrMaxRetriesExceeded, Attempt: attempt}
		}

		// Execute function
		err := fn()
		if err == nil {
			return nil
		}
		lastErr = err

		// Calculate backoff
		delay := r.strategy.Next(attempt)

		// Wait for backoff or context cancellation
		select {
		case <-ctx.Done():
			return &RetryError{Err: ErrContextCanceled, Attempt: attempt}
		case <-time.After(delay):
		}
	}
}

// DoWithResult executes a function that returns a result with retry logic
func DoWithResult[T any](ctx context.Context, strategy BackoffStrategy, config Config, fn RetryableFuncWithResult[T]) (T, error) {
	var result T
	retrier := NewRetrier(strategy, config)
	
	err := retrier.Do(ctx, func() error {
		var err error
		result, err = fn()
		return err
	})
	
	return result, err
}

// IsRetryable checks if an error is retryable
type IsRetryable func(error) bool

// DoWithRetryableCheck executes the function with retry logic and custom retryable check
func (r *Retrier) DoWithRetryableCheck(ctx context.Context, fn RetryableFunc, isRetryable IsRetryable, maxRetries int) error {
	var lastErr error

	for attempt := 0; ; attempt++ {
		// Check context
		select {
		case <-ctx.Done():
			return &RetryError{Err: ErrContextCanceled, Attempt: attempt}
		default:
		}

		// Check max retries
		if maxRetries > 0 && attempt >= maxRetries {
			if lastErr != nil {
				return &RetryError{Err: lastErr, Attempt: attempt}
			}
			return &RetryError{Err: ErrMaxRetriesExceeded, Attempt: attempt}
		}

		// Execute function
		err := fn()
		if err == nil {
			return nil
		}

		// Check if error is retryable
		if !isRetryable(err) {
			return &RetryError{Err: err, Attempt: attempt}
		}

		lastErr = err

		// Calculate backoff
		delay := r.strategy.Next(attempt)

		// Wait for backoff or context cancellation
		select {
		case <-ctx.Done():
			return &RetryError{Err: ErrContextCanceled, Attempt: attempt}
		case <-time.After(delay):
		}
	}
}

// Retry wraps Do with default context
func (r *Retrier) Retry(fn RetryableFunc) error {
	return r.Do(context.Background(), fn)
}

// RetryWithTimeout executes the function with a timeout
func (r *Retrier) RetryWithTimeout(fn RetryableFunc, timeout time.Duration) error {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	return r.Do(ctx, fn)
}

// BackoffCalculator provides utility functions for calculating backoff
type BackoffCalculator struct{}

// CalculateExponential calculates exponential backoff
func (BackoffCalculator) CalculateExponential(baseDelay time.Duration, multiplier float64, attempt int) time.Duration {
	delay := float64(baseDelay) * math.Pow(multiplier, float64(attempt))
	return time.Duration(delay)
}

// CalculateLinear calculates linear backoff
func (BackoffCalculator) CalculateLinear(baseDelay time.Duration, attempt int) time.Duration {
	return baseDelay * time.Duration(attempt+1)
}

// CalculateWithJitter adds jitter to a delay
func (BackoffCalculator) CalculateWithJitter(delay time.Duration, jitterFraction float64, rng *rand.Rand) time.Duration {
	if rng == nil {
		rng = rand.New(rand.NewSource(time.Now().UnixNano()))
	}
	jitter := float64(delay) * jitterFraction * rng.Float64()
	return time.Duration(float64(delay) - jitterFraction*float64(delay)/2 + jitter)
}

// CapDelay caps a delay at a maximum value
func (BackoffCalculator) CapDelay(delay, maxDelay time.Duration) time.Duration {
	if delay > maxDelay {
		return maxDelay
	}
	return delay
}

// SleepWithContext sleeps for the given duration, respecting context cancellation
func SleepWithContext(ctx context.Context, d time.Duration) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-time.After(d):
		return nil
	}
}