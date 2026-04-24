// Package debounce_utils provides debouncing and throttling utilities for Go.
// These are useful for rate-limiting function calls, especially in scenarios
// like API requests, event handlers, or search inputs.
package debounce_utils

import (
	"context"
	"sync"
	"time"
)

// Debouncer wraps a function and ensures it's only called after a period of inactivity.
type Debouncer struct {
	mu         sync.Mutex
	delay      time.Duration
	timer      *time.Timer
	lastCall   time.Time
	pending    func()
	ctx        context.Context
	cancel     context.CancelFunc
	leading    bool
	trailing   bool
	maxWait    time.Duration
	maxTimer   *time.Timer
	callCount  int
}

// DebounceOption configures the Debouncer behavior.
type DebounceOption func(*Debouncer)

// WithLeading causes the function to be called on the leading edge (immediately on first call).
func WithLeading() DebounceOption {
	return func(d *Debouncer) {
		d.leading = true
	}
}

// WithTrailing causes the function to be called on the trailing edge (after delay).
// Default is true.
func WithTrailing(trailing bool) DebounceOption {
	return func(d *Debouncer) {
		d.trailing = trailing
	}
}

// WithMaxWait sets the maximum time the debounced function can be delayed.
func WithMaxWait(maxWait time.Duration) DebounceOption {
	return func(d *Debouncer) {
		d.maxWait = maxWait
	}
}

// WithContext sets a context for cancellation.
func WithContext(ctx context.Context) DebounceOption {
	return func(d *Debouncer) {
		d.ctx, d.cancel = context.WithCancel(ctx)
	}
}

// NewDebouncer creates a new Debouncer with the specified delay and options.
func NewDebouncer(delay time.Duration, opts ...DebounceOption) *Debouncer {
	d := &Debouncer{
		delay:    delay,
		trailing: true,
	}
	for _, opt := range opts {
		opt(d)
	}
	if d.ctx == nil {
		d.ctx, d.cancel = context.WithCancel(context.Background())
	}
	return d
}

// Call schedules the function to be executed after the delay.
// If called again before the delay expires, the timer is reset.
func (d *Debouncer) Call(fn func()) {
	d.mu.Lock()
	defer d.mu.Unlock()

	d.pending = fn
	d.callCount++
	now := time.Now()

	// Handle leading edge call
	if d.leading && d.callCount == 1 {
		go fn()
		d.lastCall = now
	}

	// Reset or create the main timer
	if d.timer != nil {
		d.timer.Stop()
	}
	d.timer = time.AfterFunc(d.delay, d.executePending)

	// Handle maxWait timer
	if d.maxWait > 0 {
		if d.maxTimer == nil {
			d.maxTimer = time.AfterFunc(d.maxWait, d.executePending)
		}
	}
}

func (d *Debouncer) executePending() {
	d.mu.Lock()
	defer d.mu.Unlock()

	if d.pending != nil && d.trailing {
		go d.pending()
		d.pending = nil
		d.callCount = 0
	}

	if d.maxTimer != nil {
		d.maxTimer.Stop()
		d.maxTimer = nil
	}
}

// Cancel stops any pending execution.
func (d *Debouncer) Cancel() {
	d.mu.Lock()
	defer d.mu.Unlock()

	if d.timer != nil {
		d.timer.Stop()
		d.timer = nil
	}
	if d.maxTimer != nil {
		d.maxTimer.Stop()
		d.maxTimer = nil
	}
	d.pending = nil
	d.callCount = 0
}

// Flush immediately executes any pending function.
func (d *Debouncer) Flush() {
	d.mu.Lock()
	defer d.mu.Unlock()

	if d.timer != nil {
		d.timer.Stop()
		d.timer = nil
	}
	if d.maxTimer != nil {
		d.maxTimer.Stop()
		d.maxTimer = nil
	}
	if d.pending != nil {
		go d.pending()
		d.pending = nil
	}
	d.callCount = 0
}

// Close releases resources associated with the Debouncer.
func (d *Debouncer) Close() {
	d.Cancel()
	if d.cancel != nil {
		d.cancel()
	}
}

// Throttler wraps a function and ensures it's called at most once per interval.
type Throttler struct {
	mu        sync.Mutex
	interval  time.Duration
	lastCall  time.Time
	timer     *time.Timer
	pending   func()
	leading   bool
	trailing  bool
	ctx       context.Context
	cancel    context.CancelFunc
	callCount int
}

// ThrottleOption configures the Throttler behavior.
type ThrottleOption func(*Throttler)

// WithThrottleLeading causes the function to be called on the leading edge.
// Default is true.
func WithThrottleLeading(leading bool) ThrottleOption {
	return func(t *Throttler) {
		t.leading = leading
	}
}

// WithThrottleTrailing causes the function to be called on the trailing edge.
// Default is true.
func WithThrottleTrailing(trailing bool) ThrottleOption {
	return func(t *Throttler) {
		t.trailing = trailing
	}
}

// WithThrottleContext sets a context for cancellation.
func WithThrottleContext(ctx context.Context) ThrottleOption {
	return func(t *Throttler) {
		t.ctx, t.cancel = context.WithCancel(ctx)
	}
}

// NewThrottler creates a new Throttler with the specified interval and options.
func NewThrottler(interval time.Duration, opts ...ThrottleOption) *Throttler {
	t := &Throttler{
		interval: interval,
		leading:  true,
		trailing: true,
	}
	for _, opt := range opts {
		opt(t)
	}
	if t.ctx == nil {
		t.ctx, t.cancel = context.WithCancel(context.Background())
	}
	return t
}

// Call attempts to execute the function, respecting the throttle interval.
func (t *Throttler) Call(fn func()) {
	t.mu.Lock()
	defer t.mu.Unlock()

	now := time.Now()
	t.pending = fn
	t.callCount++

	elapsed := now.Sub(t.lastCall)

	// If enough time has passed, execute immediately (leading edge)
	if elapsed >= t.interval {
		if t.leading {
			go fn()
			t.lastCall = now
			t.pending = nil
		}
		// Reset for next interval
		if t.timer != nil {
			t.timer.Stop()
		}
		t.timer = time.AfterFunc(t.interval, t.executeTrailing)
		return
	}

	// Otherwise, schedule for trailing edge
	if t.timer == nil {
		remaining := t.interval - elapsed
		t.timer = time.AfterFunc(remaining, t.executeTrailing)
	}
}

func (t *Throttler) executeTrailing() {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.pending != nil && t.trailing {
		go t.pending()
		t.lastCall = time.Now()
		t.pending = nil
		t.callCount = 0
	}
	t.timer = nil
}

// Cancel stops any pending execution.
func (t *Throttler) Cancel() {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.timer != nil {
		t.timer.Stop()
		t.timer = nil
	}
	t.pending = nil
	t.callCount = 0
}

// Flush immediately executes any pending function.
func (t *Throttler) Flush() {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.timer != nil {
		t.timer.Stop()
		t.timer = nil
	}
	if t.pending != nil {
		go t.pending()
		t.pending = nil
		t.lastCall = time.Now()
	}
	t.callCount = 0
}

// Close releases resources associated with the Throttler.
func (t *Throttler) Close() {
	t.Cancel()
	if t.cancel != nil {
		t.cancel()
	}
}

// RateLimiter is a simple token bucket rate limiter.
type RateLimiter struct {
	mu         sync.Mutex
	tokens     float64
	maxTokens  float64
	refillRate float64 // tokens per second
	lastRefill time.Time
}

// NewRateLimiter creates a rate limiter with the specified rate and burst.
// rate: tokens per second, burst: maximum tokens.
func NewRateLimiter(rate float64, burst int) *RateLimiter {
	return &RateLimiter{
		tokens:     float64(burst),
		maxTokens:  float64(burst),
		refillRate: rate,
		lastRefill: time.Now(),
	}
}

// Allow checks if a single token is available and consumes it if so.
func (r *RateLimiter) Allow() bool {
	return r.AllowN(1)
}

// AllowN checks if n tokens are available and consumes them if so.
func (r *RateLimiter) AllowN(n int) bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.refill()
	if r.tokens >= float64(n) {
		r.tokens -= float64(n)
		return true
	}
	return false
}

// refill adds tokens based on elapsed time.
func (r *RateLimiter) refill() {
	now := time.Now()
	elapsed := now.Sub(r.lastRefill).Seconds()
	r.tokens = min(r.maxTokens, r.tokens+elapsed*r.refillRate)
	r.lastRefill = now
}

// Wait blocks until a token is available.
func (r *RateLimiter) Wait(ctx context.Context) error {
	return r.WaitN(ctx, 1)
}

// WaitN blocks until n tokens are available.
func (r *RateLimiter) WaitN(ctx context.Context, n int) error {
	for {
		if r.AllowN(n) {
			return nil
		}
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(time.Millisecond * 10):
			continue
		}
	}
}

// Tokens returns the current number of available tokens.
func (r *RateLimiter) Tokens() float64 {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.refill()
	return r.tokens
}

// Delay wraps a function and adds a delay between calls.
// Useful for spacing out operations like API requests.
type Delay struct {
	mu       sync.Mutex
	delay    time.Duration
	lastCall time.Time
}

// NewDelay creates a new Delay wrapper.
func NewDelay(delay time.Duration) *Delay {
	return &Delay{delay: delay}
}

// Call executes the function with delay enforcement.
func (d *Delay) Call(fn func()) {
	d.mu.Lock()
	defer d.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(d.lastCall)

	if elapsed < d.delay {
		time.Sleep(d.delay - elapsed)
	}

	fn()
	d.lastCall = time.Now()
}

// CallAsync executes the function asynchronously with delay enforcement.
func (d *Delay) CallAsync(fn func()) {
	go d.Call(fn)
}

// Batch collects items and processes them in batches.
type Batch[T any] struct {
	mu       sync.Mutex
	items    []T
	size     int
	processor func([]T)
	timer    *time.Timer
	timeout  time.Duration
}

// BatchOption configures the Batch behavior.
type BatchOption[T any] func(*Batch[T])

// WithBatchTimeout sets the maximum time to wait before processing a partial batch.
func WithBatchTimeout[T any](timeout time.Duration) BatchOption[T] {
	return func(b *Batch[T]) {
		b.timeout = timeout
	}
}

// WithBatchProcessor sets the function to process batches.
func WithBatchProcessor[T any](processor func([]T)) BatchOption[T] {
	return func(b *Batch[T]) {
		b.processor = processor
	}
}

// NewBatch creates a new batch processor.
func NewBatch[T any](size int, opts ...BatchOption[T]) *Batch[T] {
	b := &Batch[T]{
		size:  size,
		items: make([]T, 0, size),
	}
	for _, opt := range opts {
		opt(b)
	}
	return b
}

// Add adds an item to the batch.
// Returns true if the batch was processed.
func (b *Batch[T]) Add(item T) bool {
	b.mu.Lock()
	defer b.mu.Unlock()

	b.items = append(b.items, item)

	// Start timeout timer on first item
	if len(b.items) == 1 && b.timeout > 0 {
		b.timer = time.AfterFunc(b.timeout, func() {
			b.mu.Lock()
			defer b.mu.Unlock()
			b.processBatch()
		})
	}

	// Process if batch is full
	if len(b.items) >= b.size {
		if b.timer != nil {
			b.timer.Stop()
		}
		b.processBatch()
		return true
	}

	return false
}

// Flush processes any pending items immediately.
func (b *Batch[T]) Flush() {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.timer != nil {
		b.timer.Stop()
	}
	b.processBatch()
}

func (b *Batch[T]) processBatch() {
	if len(b.items) == 0 || b.processor == nil {
		return
	}
	items := b.items
	b.items = make([]T, 0, b.size)
	go b.processor(items)
}

// Size returns the current number of items in the batch.
func (b *Batch[T]) Size() int {
	b.mu.Lock()
	defer b.mu.Unlock()
	return len(b.items)
}

// Helper function for min (Go 1.21+ has built-in min, but keeping for compatibility)
func min[T ~int | ~float64](a, b T) T {
	if a < b {
		return a
	}
	return b
}