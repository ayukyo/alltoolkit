// Package rate_limiter provides a comprehensive rate limiting utility for Go applications.
// It supports multiple rate limiting algorithms including token bucket, leaky bucket,
// fixed window, and sliding window. All implementations are thread-safe and use only
// the Go standard library.
//
// Example usage:
//
//	// Token bucket rate limiter
//	limiter := rate_limiter.NewTokenBucket(100, 10) // 100 capacity, 10 tokens/sec
//	if limiter.Allow() {
//	    // Process request
//	}
//
//	// Wait for token
//	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
//	defer cancel()
//	if err := limiter.Wait(ctx); err == nil {
//	    // Process request
//	}
//
//	// Fixed window rate limiter
//	fixed := rate_limiter.NewFixedWindow(100, time.Minute) // 100 requests/minute
//	if fixed.Allow() {
//	    // Process request
//	}
//
//	// Sliding window rate limiter
//	sliding := rate_limiter.NewSlidingWindow(100, time.Minute) // 100 requests/minute
//	if sliding.Allow() {
//	    // Process request
//	}
//
//	// Leaky bucket rate limiter
//	leaky := rate_limiter.NewLeakyBucket(10, 100) // 10 req/sec, burst 100
//	if leaky.Allow() {
//	    // Process request
//	}
//
//	// Rate limiter with callback
//	limiter.OnLimitExceeded = func() {
//	    log.Println("Rate limit exceeded")
//	}
//
//	// Get rate limiter stats
//	stats := limiter.Stats()
//	fmt.Printf("Allowed: %d, Rejected: %d\n", stats.Allowed, stats.Rejected)
//
// Features:
// - Zero dependencies, uses only Go standard library
// - Thread-safe implementations with sync.RWMutex
// - Multiple rate limiting algorithms (token bucket, leaky bucket, fixed/sliding window)
// - Context support for cancellation and timeouts
// - Statistics tracking (allowed/rejected counts)
// - Configurable callbacks for rate limit events
// - Burst handling support
// - Production-ready for API rate limiting and throttling
//
package rate_limiter

import (
	"context"
	"sync"
	"time"
)

// Limiter is the interface for all rate limiter implementations.
type Limiter interface {
	// Allow checks if a request should be allowed.
	// Returns true if allowed, false if rate limited.
	Allow() bool

	// AllowN checks if n requests should be allowed.
	// Returns true if all n requests are allowed, false otherwise.
	AllowN(n int) bool

	// Wait blocks until a request is allowed or context is cancelled.
	// Returns error if context is cancelled before token is available.
	Wait(ctx context.Context) error

	// WaitN blocks until n requests are allowed or context is cancelled.
	WaitN(ctx context.Context, n int) error

	// Stats returns current rate limiter statistics.
	Stats() Stats

	// Reset resets the rate limiter to its initial state.
	Reset()

	// Stop stops the rate limiter's background goroutines.
	Stop()
}

// Stats contains rate limiter statistics.
type Stats struct {
	Allowed   int64 // Total number of allowed requests
	Rejected  int64 // Total number of rejected requests
	Remaining int   // Current remaining capacity (tokens/requests)
	Capacity  int   // Maximum capacity
}

// TokenBucket implements the token bucket rate limiting algorithm.
// It allows bursts up to the bucket capacity while maintaining a steady rate.
type TokenBucket struct {
	mu           sync.RWMutex
	capacity     int           // Maximum tokens in bucket
	tokens       float64       // Current tokens
	fillRate     float64       // Tokens added per second
	lastFillTime time.Time     // Last time tokens were added
	allowed      int64         // Allowed request count
	rejected     int64         // Rejected request count
	ticker       *time.Ticker  // Background ticker for token replenishment
	stopCh       chan struct{} // Stop signal
	onLimit      func()        // Callback when limit exceeded
}

// NewTokenBucket creates a new token bucket rate limiter.
// capacity: maximum tokens in bucket (burst size), must be > 0
// fillRate: tokens added per second (sustained rate), must be > 0
func NewTokenBucket(capacity int, fillRate float64) *TokenBucket {
	if capacity <= 0 {
		capacity = 100
	}
	if fillRate <= 0 {
		fillRate = 10
	}
	
	tb := &TokenBucket{
		capacity:     capacity,
		tokens:       float64(capacity),
		fillRate:     fillRate,
		lastFillTime: time.Now(),
		stopCh:       make(chan struct{}),
	}

	// Start background token replenishment
	tb.ticker = time.NewTicker(time.Second / 10) // Check every 100ms
	go tb.replenish()

	return tb
}

// replenish adds tokens to the bucket in the background.
func (tb *TokenBucket) replenish() {
	for {
		select {
		case <-tb.ticker.C:
			tb.mu.Lock()
			now := time.Now()
			elapsed := now.Sub(tb.lastFillTime).Seconds()
			tb.tokens += elapsed * tb.fillRate
			if tb.tokens > float64(tb.capacity) {
				tb.tokens = float64(tb.capacity)
			}
			tb.lastFillTime = now
			tb.mu.Unlock()
		case <-tb.stopCh:
			return
		}
	}
}

// Allow checks if a request should be allowed.
func (tb *TokenBucket) Allow() bool {
	return tb.AllowN(1)
}

// AllowN checks if n requests should be allowed.
func (tb *TokenBucket) AllowN(n int) bool {
	tb.mu.Lock()
	defer tb.mu.Unlock()

	// Replenish tokens based on elapsed time
	now := time.Now()
	elapsed := now.Sub(tb.lastFillTime).Seconds()
	tb.tokens += elapsed * tb.fillRate
	if tb.tokens > float64(tb.capacity) {
		tb.tokens = float64(tb.capacity)
	}
	tb.lastFillTime = now

	// Check if we have enough tokens
	if tb.tokens >= float64(n) {
		tb.tokens -= float64(n)
		tb.allowed++
		return true
	}

	tb.rejected++
	if tb.onLimit != nil {
		tb.onLimit()
	}
	return false
}

// Wait blocks until a request is allowed or context is cancelled.
func (tb *TokenBucket) Wait(ctx context.Context) error {
	return tb.WaitN(ctx, 1)
}

// WaitN blocks until n requests are allowed or context is cancelled.
func (tb *TokenBucket) WaitN(ctx context.Context, n int) error {
	for {
		tb.mu.Lock()
		// Replenish tokens
		now := time.Now()
		elapsed := now.Sub(tb.lastFillTime).Seconds()
		tb.tokens += elapsed * tb.fillRate
		if tb.tokens > float64(tb.capacity) {
			tb.tokens = float64(tb.capacity)
		}
		tb.lastFillTime = now

		if tb.tokens >= float64(n) {
			tb.tokens -= float64(n)
			tb.allowed++
			tb.mu.Unlock()
			return nil
		}
		tb.mu.Unlock()

		// Wait a bit before trying again
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(time.Millisecond * 10):
			continue
		}
	}
}

// Stats returns current rate limiter statistics.
func (tb *TokenBucket) Stats() Stats {
	tb.mu.RLock()
	defer tb.mu.RUnlock()
	return Stats{
		Allowed:   tb.allowed,
		Rejected:  tb.rejected,
		Remaining: int(tb.tokens),
		Capacity:  tb.capacity,
	}
}

// Reset resets the rate limiter to its initial state.
func (tb *TokenBucket) Reset() {
	tb.mu.Lock()
	defer tb.mu.Unlock()
	tb.tokens = float64(tb.capacity)
	tb.allowed = 0
	tb.rejected = 0
	tb.lastFillTime = time.Now()
}

// Stop stops the rate limiter's background goroutines.
func (tb *TokenBucket) Stop() {
	tb.ticker.Stop()
	close(tb.stopCh)
}

// SetOnLimitExceeded sets a callback function to be called when rate limit is exceeded.
func (tb *TokenBucket) SetOnLimitExceeded(fn func()) {
	tb.mu.Lock()
	defer tb.mu.Unlock()
	tb.onLimit = fn
}

// FixedWindow implements the fixed window rate limiting algorithm.
// It allows a fixed number of requests within a fixed time window.
type FixedWindow struct {
	mu        sync.RWMutex
	capacity  int           // Maximum requests per window
	window    time.Duration // Time window duration
	count     int           // Current request count in window
	startTime time.Time     // Window start time
	allowed   int64         // Allowed request count
	rejected  int64         // Rejected request count
	onLimit   func()        // Callback when limit exceeded
}

// NewFixedWindow creates a new fixed window rate limiter.
// capacity: maximum requests allowed per window, must be > 0
// window: time window duration, must be > 0
func NewFixedWindow(capacity int, window time.Duration) *FixedWindow {
	if capacity <= 0 {
		capacity = 100
	}
	if window <= 0 {
		window = time.Minute
	}
	
	return &FixedWindow{
		capacity:  capacity,
		window:    window,
		startTime: time.Now(),
	}
}

// Allow checks if a request should be allowed.
func (fw *FixedWindow) Allow() bool {
	return fw.AllowN(1)
}

// AllowN checks if n requests should be allowed.
func (fw *FixedWindow) AllowN(n int) bool {
	fw.mu.Lock()
	defer fw.mu.Unlock()

	now := time.Now()

	// Check if we need to reset the window
	if now.Sub(fw.startTime) >= fw.window {
		fw.startTime = now
		fw.count = 0
	}

	// Check if we have capacity
	if fw.count+n <= fw.capacity {
		fw.count += n
		fw.allowed++
		return true
	}

	fw.rejected++
	if fw.onLimit != nil {
		fw.onLimit()
	}
	return false
}

// Wait blocks until a request is allowed or context is cancelled.
func (fw *FixedWindow) Wait(ctx context.Context) error {
	return fw.WaitN(ctx, 1)
}

// WaitN blocks until n requests are allowed or context is cancelled.
func (fw *FixedWindow) WaitN(ctx context.Context, n int) error {
	for {
		fw.mu.Lock()
		now := time.Now()

		// Check if we need to reset the window
		if now.Sub(fw.startTime) >= fw.window {
			fw.startTime = now
			fw.count = 0
		}

		if fw.count+n <= fw.capacity {
			fw.count += n
			fw.allowed++
			fw.mu.Unlock()
			return nil
		}

		// Calculate time until window resets
		elapsed := now.Sub(fw.startTime)
		remaining := fw.window - elapsed
		fw.mu.Unlock()

		// Wait for window to reset or context cancellation
		timer := time.NewTimer(remaining)
		select {
		case <-ctx.Done():
			timer.Stop()
			return ctx.Err()
		case <-timer.C:
			continue
		}
	}
}

// Stats returns current rate limiter statistics.
func (fw *FixedWindow) Stats() Stats {
	fw.mu.RLock()
	defer fw.mu.RUnlock()
	return Stats{
		Allowed:   fw.allowed,
		Rejected:  fw.rejected,
		Remaining: fw.capacity - fw.count,
		Capacity:  fw.capacity,
	}
}

// Reset resets the rate limiter to its initial state.
func (fw *FixedWindow) Reset() {
	fw.mu.Lock()
	defer fw.mu.Unlock()
	fw.count = 0
	fw.allowed = 0
	fw.rejected = 0
	fw.startTime = time.Now()
}

// Stop stops the rate limiter (no-op for fixed window).
func (fw *FixedWindow) Stop() {}

// SetOnLimitExceeded sets a callback function to be called when rate limit is exceeded.
func (fw *FixedWindow) SetOnLimitExceeded(fn func()) {
	fw.mu.Lock()
	defer fw.mu.Unlock()
	fw.onLimit = fn
}

// SlidingWindow implements the sliding window rate limiting algorithm.
// It tracks request timestamps and removes expired entries.
type SlidingWindow struct {
	mu        sync.RWMutex
	capacity  int           // Maximum requests per window
	window    time.Duration // Time window duration
	timestamps []time.Time   // Request timestamps
	allowed   int64         // Allowed request count
	rejected  int64         // Rejected request count
	onLimit   func()        // Callback when limit exceeded
}

// NewSlidingWindow creates a new sliding window rate limiter.
// capacity: maximum requests allowed per window, must be > 0
// window: time window duration, must be > 0
func NewSlidingWindow(capacity int, window time.Duration) *SlidingWindow {
	if capacity <= 0 {
		capacity = 100
	}
	if window <= 0 {
		window = time.Minute
	}
	
	return &SlidingWindow{
		capacity:   capacity,
		window:     window,
		timestamps: make([]time.Time, 0, capacity),
	}
}

// cleanup removes expired timestamps from the window.
func (sw *SlidingWindow) cleanup(now time.Time) {
	cutoff := now.Add(-sw.window)
	// Remove timestamps older than the window
	i := 0
	for i < len(sw.timestamps) && sw.timestamps[i].Before(cutoff) {
		i++
	}
	if i > 0 {
		sw.timestamps = sw.timestamps[i:]
	}
}

// Allow checks if a request should be allowed.
func (sw *SlidingWindow) Allow() bool {
	return sw.AllowN(1)
}

// AllowN checks if n requests should be allowed.
func (sw *SlidingWindow) AllowN(n int) bool {
	sw.mu.Lock()
	defer sw.mu.Unlock()

	now := time.Now()
	sw.cleanup(now)

	// Check if we have capacity
	if len(sw.timestamps)+n <= sw.capacity {
		// Add timestamps for n requests
		for i := 0; i < n; i++ {
			sw.timestamps = append(sw.timestamps, now)
		}
		sw.allowed++
		return true
	}

	sw.rejected++
	if sw.onLimit != nil {
		sw.onLimit()
	}
	return false
}

// Wait blocks until a request is allowed or context is cancelled.
func (sw *SlidingWindow) Wait(ctx context.Context) error {
	return sw.WaitN(ctx, 1)
}

// WaitN blocks until n requests are allowed or context is cancelled.
func (sw *SlidingWindow) WaitN(ctx context.Context, n int) error {
	for {
		sw.mu.Lock()
		now := time.Now()
		sw.cleanup(now)

		if len(sw.timestamps)+n <= sw.capacity {
			for i := 0; i < n; i++ {
				sw.timestamps = append(sw.timestamps, now)
			}
			sw.allowed++
			sw.mu.Unlock()
			return nil
		}

		// Find when the oldest timestamp will expire
		if len(sw.timestamps) > 0 {
			oldest := sw.timestamps[0]
			waitTime := oldest.Add(sw.window).Sub(now)
			sw.mu.Unlock()

			timer := time.NewTimer(waitTime)
			select {
			case <-ctx.Done():
				timer.Stop()
				return ctx.Err()
			case <-timer.C:
				continue
			}
		} else {
			sw.mu.Unlock()
			return nil
		}
	}
}

// Stats returns current rate limiter statistics.
func (sw *SlidingWindow) Stats() Stats {
	sw.mu.RLock()
	defer sw.mu.RUnlock()
	return Stats{
		Allowed:   sw.allowed,
		Rejected:  sw.rejected,
		Remaining: sw.capacity - len(sw.timestamps),
		Capacity:  sw.capacity,
	}
}

// Reset resets the rate limiter to its initial state.
func (sw *SlidingWindow) Reset() {
	sw.mu.Lock()
	defer sw.mu.Unlock()
	sw.timestamps = sw.timestamps[:0]
	sw.allowed = 0
	sw.rejected = 0
}

// Stop stops the rate limiter (no-op for sliding window).
func (sw *SlidingWindow) Stop() {}

// SetOnLimitExceeded sets a callback function to be called when rate limit is exceeded.
func (sw *SlidingWindow) SetOnLimitExceeded(fn func()) {
	sw.mu.Lock()
	defer sw.mu.Unlock()
	sw.onLimit = fn
}

// LeakyBucket implements the leaky bucket rate limiting algorithm.
// It processes requests at a fixed rate, allowing bursts up to the bucket size.
type LeakyBucket struct {
	mu         sync.RWMutex
	capacity   int           // Maximum requests in bucket (burst size)
	leakRate   float64       // Requests processed per second
	requests   int           // Current requests in bucket
	lastLeak   time.Time     // Last time bucket leaked
	allowed    int64         // Allowed request count
	rejected   int64         // Rejected request count
	ticker     *time.Ticker  // Background ticker for leaking
	stopCh     chan struct{} // Stop signal
	onLimit    func()        // Callback when limit exceeded
}

// NewLeakyBucket creates a new leaky bucket rate limiter.
// leakRate: requests processed per second (sustained rate), must be > 0
// capacity: maximum requests in bucket (burst size), must be > 0
func NewLeakyBucket(leakRate float64, capacity int) *LeakyBucket {
	if leakRate <= 0 {
		leakRate = 10
	}
	if capacity <= 0 {
		capacity = 100
	}
	
	lb := &LeakyBucket{
		capacity: capacity,
		leakRate: leakRate,
		lastLeak: time.Now(),
		stopCh:   make(chan struct{}),
	}

	// Start background leaking
	lb.ticker = time.NewTicker(time.Second / 10) // Check every 100ms
	go lb.leak()

	return lb
}

// leak removes requests from the bucket in the background.
func (lb *LeakyBucket) leak() {
	for {
		select {
		case <-lb.ticker.C:
			lb.mu.Lock()
			now := time.Now()
			elapsed := now.Sub(lb.lastLeak).Seconds()
			toLeak := int(elapsed * lb.leakRate)
			if toLeak > 0 {
				lb.requests -= toLeak
				if lb.requests < 0 {
					lb.requests = 0
				}
				lb.lastLeak = now
			}
			lb.mu.Unlock()
		case <-lb.stopCh:
			return
		}
	}
}

// Allow checks if a request should be allowed.
func (lb *LeakyBucket) Allow() bool {
	return lb.AllowN(1)
}

// AllowN checks if n requests should be allowed.
func (lb *LeakyBucket) AllowN(n int) bool {
	lb.mu.Lock()
	defer lb.mu.Unlock()

	// Leak requests based on elapsed time
	now := time.Now()
	elapsed := now.Sub(lb.lastLeak).Seconds()
	toLeak := int(elapsed * lb.leakRate)
	if toLeak > 0 {
		lb.requests -= toLeak
		if lb.requests < 0 {
			lb.requests = 0
		}
		lb.lastLeak = now
	}

	// Check if we have capacity
	if lb.requests+n <= lb.capacity {
		lb.requests += n
		lb.allowed++
		return true
	}

	lb.rejected++
	if lb.onLimit != nil {
		lb.onLimit()
	}
	return false
}

// Wait blocks until a request is allowed or context is cancelled.
func (lb *LeakyBucket) Wait(ctx context.Context) error {
	return lb.WaitN(ctx, 1)
}

// WaitN blocks until n requests are allowed or context is cancelled.
func (lb *LeakyBucket) WaitN(ctx context.Context, n int) error {
	for {
		lb.mu.Lock()
		now := time.Now()
		elapsed := now.Sub(lb.lastLeak).Seconds()
		toLeak := int(elapsed * lb.leakRate)
		if toLeak > 0 {
			lb.requests -= toLeak
			if lb.requests < 0 {
				lb.requests = 0
			}
			lb.lastLeak = now
		}

		if lb.requests+n <= lb.capacity {
			lb.requests += n
			lb.allowed++
			lb.mu.Unlock()
			return nil
		}

		// Calculate time until enough capacity is available
		needed := lb.requests + n - lb.capacity
		waitTime := time.Duration(float64(needed) / lb.leakRate * float64(time.Second))
		lb.mu.Unlock()

		timer := time.NewTimer(waitTime)
		select {
		case <-ctx.Done():
			timer.Stop()
			return ctx.Err()
		case <-timer.C:
			continue
		}
	}
}

// Stats returns current rate limiter statistics.
func (lb *LeakyBucket) Stats() Stats {
	lb.mu.RLock()
	defer lb.mu.RUnlock()
	return Stats{
		Allowed:   lb.allowed,
		Rejected:  lb.rejected,
		Remaining: lb.capacity - lb.requests,
		Capacity:  lb.capacity,
	}
}

// Reset resets the rate limiter to its initial state.
func (lb *LeakyBucket) Reset() {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	lb.requests = 0
	lb.allowed = 0
	lb.rejected = 0
	lb.lastLeak = time.Now()
}

// Stop stops the rate limiter's background goroutines.
func (lb *LeakyBucket) Stop() {
	lb.ticker.Stop()
	close(lb.stopCh)
}

// SetOnLimitExceeded sets a callback function to be called when rate limit is exceeded.
func (lb *LeakyBucket) SetOnLimitExceeded(fn func()) {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	lb.onLimit = fn
}

// MultiLimiter combines multiple rate limiters with AND logic.
// A request is allowed only if all limiters allow it.
type MultiLimiter struct {
	limiters []Limiter
}

// NewMultiLimiter creates a new multi-limiter that requires all limiters to allow.
func NewMultiLimiter(limiters ...Limiter) *MultiLimiter {
	return &MultiLimiter{limiters: limiters}
}

// Allow checks if a request should be allowed by all limiters.
func (ml *MultiLimiter) Allow() bool {
	return ml.AllowN(1)
}

// AllowN checks if n requests should be allowed by all limiters.
func (ml *MultiLimiter) AllowN(n int) bool {
	for _, l := range ml.limiters {
		if !l.AllowN(n) {
			return false
		}
	}
	return true
}

// Wait blocks until a request is allowed by all limiters or context is cancelled.
func (ml *MultiLimiter) Wait(ctx context.Context) error {
	return ml.WaitN(ctx, 1)
}

// WaitN blocks until n requests are allowed by all limiters or context is cancelled.
func (ml *MultiLimiter) WaitN(ctx context.Context, n int) error {
	for _, l := range ml.limiters {
		if err := l.WaitN(ctx, n); err != nil {
			return err
		}
	}
	return nil
}

// Stats returns combined statistics from all limiters.
func (ml *MultiLimiter) Stats() Stats {
	if len(ml.limiters) == 0 {
		return Stats{}
	}

	// Return stats from first limiter
	return ml.limiters[0].Stats()
}

// Reset resets all limiters.
func (ml *MultiLimiter) Reset() {
	for _, l := range ml.limiters {
		l.Reset()
	}
}

// Stop stops all limiters.
func (ml *MultiLimiter) Stop() {
	for _, l := range ml.limiters {
		l.Stop()
	}
}

// PerClientLimiter manages rate limiters per client.
type PerClientLimiter struct {
	mu        sync.RWMutex
	limiters  map[string]Limiter
	factory   func() Limiter
}

// NewPerClientLimiter creates a new per-client rate limiter manager.
// factory: function that creates a new limiter for each client
func NewPerClientLimiter(factory func() Limiter) *PerClientLimiter {
	return &PerClientLimiter{
		limiters: make(map[string]Limiter),
		factory:  factory,
	}
}

// Allow checks if a request from the given client should be allowed.
func (pcl *PerClientLimiter) Allow(clientID string) bool {
	return pcl.AllowN(clientID, 1)
}

// AllowN checks if n requests from the given client should be allowed.
func (pcl *PerClientLimiter) AllowN(clientID string, n int) bool {
	pcl.mu.Lock()
	limiter, exists := pcl.limiters[clientID]
	if !exists {
		limiter = pcl.factory()
		pcl.limiters[clientID] = limiter
	}
	pcl.mu.Unlock()

	return limiter.AllowN(n)
}

// GetLimiter returns the limiter for a specific client.
func (pcl *PerClientLimiter) GetLimiter(clientID string) Limiter {
	pcl.mu.RLock()
	limiter, exists := pcl.limiters[clientID]
	pcl.mu.RUnlock()

	if !exists {
		pcl.mu.Lock()
		limiter = pcl.factory()
		pcl.limiters[clientID] = limiter
		pcl.mu.Unlock()
	}

	return limiter
}

// RemoveClient removes a client's limiter.
func (pcl *PerClientLimiter) RemoveClient(clientID string) {
	pcl.mu.Lock()
	if limiter, exists := pcl.limiters[clientID]; exists {
		limiter.Stop()
		delete(pcl.limiters, clientID)
	}
	pcl.mu.Unlock()
}

// ClientCount returns the number of tracked clients.
func (pcl *PerClientLimiter) ClientCount() int {
	pcl.mu.RLock()
	defer pcl.mu.RUnlock()
	return len(pcl.limiters)
}

// Stats returns combined statistics from all clients.
func (pcl *PerClientLimiter) Stats() map[string]Stats {
	pcl.mu.RLock()
	defer pcl.mu.RUnlock()

	stats := make(map[string]Stats)
	for clientID, limiter := range pcl.limiters {
		stats[clientID] = limiter.Stats()
	}
	return stats
}

// Stop stops all client limiters.
func (pcl *PerClientLimiter) Stop() {
	pcl.mu.Lock()
	for _, limiter := range pcl.limiters {
		limiter.Stop()
	}
	pcl.limiters = make(map[string]Limiter)
	pcl.mu.Unlock()
}
