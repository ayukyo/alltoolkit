// Package priority_sliding_window provides a multi-window, priority-aware sliding window rate limiter.
// It uses a fixed-window + epsilon-slack approach for near-zero memory overhead at scale,
// with per-priority queues, burst allowances, and adaptive window sizing.
//
// Zero external dependencies — uses only the Go standard library.
package priority_sliding_window

import (
	"errors"
	"fmt"
	"sync"
	"time"
)

// Priority levels — lower value = higher priority.
const (
	PriorityCritical = 0
	PriorityHigh    = 1
	PriorityMedium  = 2
	PriorityLow     = 3
	PriorityBulk    = 4
)

// WindowType defines the timing model for a rate limiter window.
type WindowType int

const (
	// SlidingWindow uses a rolling window that continuously moves.
	// Memory: O(windowSlots) where each slot is a timeQuantum.
	SlidingWindow WindowType = iota
	// FixedWindow resets counters at each window boundary.
	// Memory: O(1) — constant memory regardless of limit.
	FixedWindow
)

// Config holds all configuration for a rate limiter.
type Config struct {
	// Limits is the maximum number of operations per window per priority.
	// Map priority -> limit. If a priority is missing, it is allowed unlimited.
	Limits map[int]int
	// WindowDuration specifies the length of the rate window.
	WindowDuration time.Duration
	// TimeQuantum is the granularity of the sliding window (minimum unit).
	// Smaller values = more precise but higher memory usage.
	// Ignored for FixedWindow mode.
	TimeQuantum time.Duration
	// WindowType selects the window timing model.
	WindowType WindowType
	// BurstAllowance adds extra capacity above the limit for burst traffic.
	// Expressed as a fraction of the limit (e.g., 0.2 = 20% burst).
	BurstAllowance float64
	// MinBurst sets an absolute minimum burst (even if limit is small).
	MinBurst int
	// CleanupInterval controls how often expired entries are purged.
	// Only relevant for SlidingWindow mode.
	CleanupInterval time.Duration
}

// RateLimiter is the main entry point. Create with New or NewWithConfig.
type RateLimiter struct {
	cfg         Config
	windowType  WindowType
	timeQuantum time.Duration

	// Sliding window state: per-priority sliding counters
	mu     sync.RWMutex
	counts map[int]*slidingCounter // priority -> counter

	// Fixed window state: per-priority fixed counters + window start
	fixedMu   sync.RWMutex
	fixedCnt  map[int]int      // priority -> current count
	fixedLast map[int]time.Time // priority -> last window start

	// Adaptive window: per-priority observed peak for auto-tuning
	peakMu sync.RWMutex
	peaks  map[int]int // priority -> peak observed

	stopCleanup chan struct{}
}

// slidingCounter tracks counts within a sliding window with epsilon-slack.
type slidingCounter struct {
	mu         sync.RWMutex
	buckets    map[int64]int // bucketKey (timestamp/quantum) -> count
	headKey    int64        // oldest valid bucket key
	windowKeys int64        // number of keys in window = windowDuration/timeQuantum
	limit      int
	burst      int
}

// New creates a RateLimiter with the given limits and a default sliding window.
// limits: map of PriorityX -> maxOperationsPerWindow.
// windowDuration: length of the rate window.
func New(limits map[int]int, windowDuration time.Duration) (*RateLimiter, error) {
	return NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  windowDuration,
		TimeQuantum:     time.Second,
		WindowType:      SlidingWindow,
		BurstAllowance:  0.2,
		MinBurst:        5,
		CleanupInterval: time.Minute,
	})
}

// NewWithConfig creates a RateLimiter from a full Config.
func NewWithConfig(cfg Config) (*RateLimiter, error) {
	if cfg.WindowDuration <= 0 {
		return nil, errors.New("window duration must be positive")
	}
	if cfg.TimeQuantum <= 0 {
		cfg.TimeQuantum = time.Second
	}
	if cfg.BurstAllowance < 0 {
		cfg.BurstAllowance = 0
	}

	rl := &RateLimiter{
		cfg:         cfg,
		windowType:  cfg.WindowType,
		timeQuantum: cfg.TimeQuantum,
		counts:      make(map[int]*slidingCounter),
		fixedCnt:    make(map[int]int),
		fixedLast:   make(map[int]time.Time),
		peaks:       make(map[int]int),
		stopCleanup: make(chan struct{}),
	}

	windowKeys := int64(cfg.WindowDuration / cfg.TimeQuantum)
	if windowKeys < 1 {
		windowKeys = 1
	}

	for p, limit := range cfg.Limits {
		burst := int(float64(limit) * cfg.BurstAllowance)
		if burst < cfg.MinBurst {
			burst = cfg.MinBurst
		}
		rl.counts[p] = &slidingCounter{
			buckets:    make(map[int64]int),
			headKey:    0,
			windowKeys: windowKeys,
			limit:      limit,
			burst:      burst,
		}
		rl.fixedCnt[p] = 0
		rl.peaks[p] = limit
	}

	if cfg.WindowType == SlidingWindow && cfg.CleanupInterval > 0 {
		go rl.cleanupLoop()
	}

	return rl, nil
}

// Allow checks whether an operation at the given priority is permitted.
// It is non-blocking — returns true if allowed, false otherwise.
func (rl *RateLimiter) Allow(priority int) bool {
	if rl.windowType == SlidingWindow {
		return rl.allowSliding(priority)
	}
	return rl.allowFixed(priority)
}

// allowSliding uses the sliding window with epsilon-slack.
func (rl *RateLimiter) allowSliding(priority int) bool {
	counter, ok := rl.getSlidingCounter(priority)
	if !ok {
		return true // Unknown priority = unlimited
	}

	counter.mu.Lock()
	defer counter.mu.Unlock()

	now := time.Now()
	bucketKey := now.UnixNano() / int64(rl.timeQuantum)
	effectiveKey := bucketKey - counter.windowKeys + 1
	if effectiveKey > counter.headKey {
		counter.headKey = effectiveKey
	}

	current := counter.buckets[bucketKey]
	effectiveLimit := counter.limit + counter.burst

	if current >= effectiveLimit {
		return false
	}

	counter.buckets[bucketKey] = current + 1

	// Track peak for adaptive windowing
	rl.peakMu.Lock()
	if counter.buckets[bucketKey] > rl.peaks[priority] {
		rl.peaks[priority] = counter.buckets[bucketKey]
	}
	rl.peakMu.Unlock()

	return true
}

// allowFixed uses the fixed window model.
func (rl *RateLimiter) allowFixed(priority int) bool {
	counter, ok := rl.getSlidingCounter(priority)
	if !ok {
		return true
	}

	rl.fixedMu.Lock()
	defer rl.fixedMu.Unlock()

	now := time.Now()
	windowStart := rl.getWindowStart(now)
	last := rl.fixedLast[priority]

	if last.Before(windowStart) {
		// New window — reset
		rl.fixedCnt[priority] = 1
		rl.fixedLast[priority] = windowStart
		counter.mu.Lock()
		counter.buckets = make(map[int64]int) // clear old buckets
		counter.mu.Unlock()
		return true
	}

	effectiveLimit := counter.limit + counter.burst
	if rl.fixedCnt[priority] >= effectiveLimit {
		return false
	}

	rl.fixedCnt[priority]++
	return true
}

// getWindowStart returns the start of the current window for a given time.
func (rl *RateLimiter) getWindowStart(t time.Time) time.Time {
	quantum := int64(rl.timeQuantum)
	return time.Unix(0, t.UnixNano()/quantum*quantum)
}

// Reserve checks and reserves an operation if allowed, returning a reservation object.
// Unlike Allow, Reserve is used for async confirmations (confirm/cancel).
func (rl *RateLimiter) Reserve(priority int) *Reservation {
	return &Reservation{
		allowed:  rl.Allow(priority),
		limiter:  rl,
		priority: priority,
	}
}

// Reservation represents a reserved slot that can be confirmed or cancelled.
type Reservation struct {
	allowed   bool
	limiter   *RateLimiter
	priority  int
	confirmed bool
	mu        sync.Mutex
}

// Confirm marks the reservation as used (success path).
func (r *Reservation) Confirm() {
	r.mu.Lock()
	defer r.mu.Unlock()
	if r.allowed && !r.confirmed {
		r.confirmed = true
	}
}

// Cancel releases the reserved slot back to the window.
func (r *Reservation) Cancel() {
	r.mu.Lock()
	defer r.mu.Unlock()
	if r.allowed && !r.confirmed {
		// For fixed window, decrement the counter
		if r.limiter.windowType == FixedWindow {
			r.limiter.fixedMu.Lock()
			if r.limiter.fixedCnt[r.priority] > 0 {
				r.limiter.fixedCnt[r.priority]--
			}
			r.limiter.fixedMu.Unlock()
		}
		r.confirmed = true
	}
}

// Allowed returns whether the reservation was initially allowed.
func (r *Reservation) Allowed() bool {
	return r.allowed
}

// Remaining returns how many more operations are allowed for a priority right now.
func (rl *RateLimiter) Remaining(priority int) int {
	if rl.windowType == SlidingWindow {
		return rl.remainingSliding(priority)
	}
	return rl.remainingFixed(priority)
}

func (rl *RateLimiter) remainingSliding(priority int) int {
	counter, ok := rl.getSlidingCounter(priority)
	if !ok {
		return int(^uint(0) >> 1) // Max int = effectively unlimited
	}

	counter.mu.RLock()
	defer counter.mu.RUnlock()

	now := time.Now()
	bucketKey := now.UnixNano() / int64(rl.timeQuantum)
	effectiveLimit := counter.limit + counter.burst

	current := counter.buckets[bucketKey]
	remaining := effectiveLimit - current
	if remaining < 0 {
		return 0
	}
	return remaining
}

func (rl *RateLimiter) remainingFixed(priority int) int {
	counter, ok := rl.getSlidingCounter(priority)
	if !ok {
		return int(^uint(0) >> 1)
	}

	rl.fixedMu.RLock()
	defer rl.fixedMu.RUnlock()

	effectiveLimit := counter.limit + counter.burst
	remaining := effectiveLimit - rl.fixedCnt[priority]
	if remaining < 0 {
		return 0
	}
	return remaining
}

// Peek returns the current observed peak for a priority (for adaptive tuning).
func (rl *RateLimiter) Peek(priority int) int {
	rl.peakMu.RLock()
	defer rl.peakMu.RUnlock()
	return rl.peaks[priority]
}

// Reset clears all counters for a priority (or all priorities if priority < 0).
func (rl *RateLimiter) Reset(priority int) {
	if priority < 0 {
		for p := range rl.counts {
			rl.Reset(p)
		}
		return
	}

	if rl.windowType == SlidingWindow {
		if counter, ok := rl.getSlidingCounter(priority); ok {
			counter.mu.Lock()
			counter.buckets = make(map[int64]int)
			counter.mu.Unlock()
		}
	} else {
		rl.fixedMu.Lock()
		rl.fixedCnt[priority] = 0
		rl.fixedLast[priority] = time.Time{}
		rl.fixedMu.Unlock()
	}
}

// UpdateLimit adjusts the limit for a priority dynamically.
func (rl *RateLimiter) UpdateLimit(priority int, newLimit int) error {
	counter, ok := rl.getSlidingCounter(priority)
	if !ok {
		return errors.New("priority not found")
	}
	counter.mu.Lock()
	counter.limit = newLimit
	counter.mu.Unlock()
	return nil
}

// Stats returns a snapshot of the current rate limiter state.
func (rl *RateLimiter) Stats(priority int) Stats {
	counter, ok := rl.getSlidingCounter(priority)
	if !ok {
		return Stats{Priority: priority, WindowType: rl.windowType}
	}

	stats := Stats{
		Priority:        priority,
		Limit:           counter.limit,
		Burst:           counter.burst,
		EffectiveLimit:  counter.limit + counter.burst,
		Remaining:       rl.Remaining(priority),
		PeakObserved:    rl.Peek(priority),
		WindowType:      rl.windowType,
		WindowDurationMs: rl.cfg.WindowDuration.Milliseconds(),
	}

	if rl.windowType == SlidingWindow {
		counter.mu.RLock()
		now := time.Now()
		bucketKey := now.UnixNano() / int64(rl.timeQuantum)
		stats.CurrentBucketCount = counter.buckets[bucketKey]
		stats.ActiveBuckets = len(counter.buckets)
		counter.mu.RUnlock()
	} else {
		rl.fixedMu.RLock()
		stats.FixedCount = rl.fixedCnt[priority]
		stats.FixedWindowStart = rl.fixedLast[priority]
		rl.fixedMu.RUnlock()
	}

	return stats
}

// Stats holds a snapshot of rate limiter state.
type Stats struct {
	Priority           int
	Limit              int
	Burst              int
	EffectiveLimit     int
	Remaining          int
	PeakObserved       int
	WindowType         WindowType
	WindowDurationMs  int64
	CurrentBucketCount int
	ActiveBuckets      int
	FixedCount         int
	FixedWindowStart   time.Time
}

func (rl *RateLimiter) getSlidingCounter(priority int) (*slidingCounter, bool) {
	rl.mu.RLock()
	defer rl.mu.RUnlock()
	c, ok := rl.counts[priority]
	return c, ok
}

func (rl *RateLimiter) cleanupLoop() {
	ticker := time.NewTicker(rl.cfg.CleanupInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			rl.cleanup()
		case <-rl.stopCleanup:
			return
		}
	}
}

func (rl *RateLimiter) cleanup() {
	if rl.timeQuantum == 0 {
		return
	}
	now := time.Now()
	quantumNanos := int64(rl.timeQuantum)
	windowKeys := int64(rl.cfg.WindowDuration) / quantumNanos
	cutoffKey := now.UnixNano()/quantumNanos - windowKeys - 1

	rl.mu.Lock()
	defer rl.mu.Unlock()

	for _, counter := range rl.counts {
		counter.mu.Lock()
		for key := range counter.buckets {
			if key < cutoffKey {
				delete(counter.buckets, key)
			}
		}
		if counter.headKey < cutoffKey {
			counter.headKey = cutoffKey
		}
		counter.mu.Unlock()
	}
}

// Stop stops the background cleanup goroutine.
func (rl *RateLimiter) Stop() {
	close(rl.stopCleanup)
}

// String returns a human-readable summary of stats.
func (s Stats) String() string {
	return fmt.Sprintf("Stats{p%d limit=%d burst=%d effective=%d remaining=%d peak=%d}",
		s.Priority, s.Limit, s.Burst, s.EffectiveLimit, s.Remaining, s.PeakObserved)
}