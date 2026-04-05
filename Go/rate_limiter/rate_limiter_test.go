package rate_limiter

import (
	"context"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// TestTokenBucketBasic tests basic token bucket functionality
func TestTokenBucketBasic(t *testing.T) {
	tb := NewTokenBucket(10, 1)
	defer tb.Stop()

	// Should allow initial burst
	for i := 0; i < 10; i++ {
		if !tb.Allow() {
			t.Errorf("Expected Allow() to return true for request %d", i+1)
		}
	}

	// Should reject after burst
	if tb.Allow() {
		t.Error("Expected Allow() to return false after burst")
	}

	stats := tb.Stats()
	if stats.Allowed != 10 {
		t.Errorf("Expected 10 allowed, got %d", stats.Allowed)
	}
	if stats.Rejected != 1 {
		t.Errorf("Expected 1 rejected, got %d", stats.Rejected)
	}
}

// TestTokenBucketAllowN tests batch allowance
func TestTokenBucketAllowN(t *testing.T) {
	tb := NewTokenBucket(10, 1)
	defer tb.Stop()

	// Should allow batch of 5
	if !tb.AllowN(5) {
		t.Error("Expected AllowN(5) to return true")
	}

	// Should allow another batch of 5
	if !tb.AllowN(5) {
		t.Error("Expected AllowN(5) to return true for second batch")
	}

	// Should reject batch of 1
	if tb.AllowN(1) {
		t.Error("Expected AllowN(1) to return false after exhausting tokens")
	}
}

// TestTokenBucketWait tests waiting for tokens
func TestTokenBucketWait(t *testing.T) {
	tb := NewTokenBucket(1, 10) // 1 capacity, 10 tokens/sec
	defer tb.Stop()

	// Use the token
	tb.Allow()

	// Wait for token with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	err := tb.Wait(ctx)
	if err != nil {
		t.Errorf("Expected Wait to succeed, got error: %v", err)
	}
}

// TestTokenBucketWaitTimeout tests wait timeout
func TestTokenBucketWaitTimeout(t *testing.T) {
	tb := NewTokenBucket(1, 0.1) // 1 capacity, 0.1 tokens/sec (slow refill)
	defer tb.Stop()

	// Use the token
	tb.Allow()

	// Wait with short timeout
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	err := tb.Wait(ctx)
	if err != context.DeadlineExceeded {
		t.Errorf("Expected DeadlineExceeded, got: %v", err)
	}
}

// TestTokenBucketReset tests reset functionality
func TestTokenBucketReset(t *testing.T) {
	tb := NewTokenBucket(10, 1)
	defer tb.Stop()

	// Use some tokens
	tb.AllowN(5)

	// Reset
	tb.Reset()

	// Should allow full burst again
	for i := 0; i < 10; i++ {
		if !tb.Allow() {
			t.Errorf("Expected Allow() to return true after reset for request %d", i+1)
		}
	}

	stats := tb.Stats()
	if stats.Allowed != 10 {
		t.Errorf("Expected 10 allowed after reset, got %d", stats.Allowed)
	}
}

// TestTokenBucketStats tests statistics
func TestTokenBucketStats(t *testing.T) {
	tb := NewTokenBucket(10, 1)
	defer tb.Stop()

	// Use 5 tokens
	tb.AllowN(5)

	stats := tb.Stats()
	if stats.Capacity != 10 {
		t.Errorf("Expected capacity 10, got %d", stats.Capacity)
	}
	if stats.Remaining != 5 {
		t.Errorf("Expected remaining 5, got %d", stats.Remaining)
	}
	if stats.Allowed != 5 {
		t.Errorf("Expected 5 allowed, got %d", stats.Allowed)
	}
}

// TestTokenBucketCallback tests callback functionality
func TestTokenBucketCallback(t *testing.T) {
	tb := NewTokenBucket(1, 1)
	defer tb.Stop()

	// Use the token
	tb.Allow()

	var callbackCalled int32
	tb.SetOnLimitExceeded(func() {
		atomic.AddInt32(&callbackCalled, 1)
	})

	// This should trigger the callback
	tb.Allow()

	if atomic.LoadInt32(&callbackCalled) != 1 {
		t.Error("Expected callback to be called once")
	}
}

// TestFixedWindowBasic tests fixed window functionality
func TestFixedWindowBasic(t *testing.T) {
	fw := NewFixedWindow(5, 100*time.Millisecond)

	// Should allow 5 requests
	for i := 0; i < 5; i++ {
		if !fw.Allow() {
			t.Errorf("Expected Allow() to return true for request %d", i+1)
		}
	}

	// Should reject 6th request
	if fw.Allow() {
		t.Error("Expected Allow() to return false after window is full")
	}

	// Wait for window to reset
	time.Sleep(110 * time.Millisecond)

	// Should allow again
	if !fw.Allow() {
		t.Error("Expected Allow() to return true after window reset")
	}
}

// TestFixedWindowAllowN tests batch allowance
func TestFixedWindowAllowN(t *testing.T) {
	fw := NewFixedWindow(10, time.Second)

	// Should allow batch of 10
	if !fw.AllowN(10) {
		t.Error("Expected AllowN(10) to return true")
	}

	// Should reject batch of 1
	if fw.AllowN(1) {
		t.Error("Expected AllowN(1) to return false after exhausting window")
	}
}

// TestFixedWindowStats tests statistics
func TestFixedWindowStats(t *testing.T) {
	fw := NewFixedWindow(10, time.Second)

	fw.AllowN(3)

	stats := fw.Stats()
	if stats.Capacity != 10 {
		t.Errorf("Expected capacity 10, got %d", stats.Capacity)
	}
	if stats.Remaining != 7 {
		t.Errorf("Expected remaining 7, got %d", stats.Remaining)
	}
	if stats.Allowed != 3 {
		t.Errorf("Expected 3 allowed, got %d", stats.Allowed)
	}
}

// TestSlidingWindowBasic tests sliding window functionality
func TestSlidingWindowBasic(t *testing.T) {
	sw := NewSlidingWindow(5, 100*time.Millisecond)

	// Should allow 5 requests
	for i := 0; i < 5; i++ {
		if !sw.Allow() {
			t.Errorf("Expected Allow() to return true for request %d", i+1)
		}
	}

	// Should reject 6th request
	if sw.Allow() {
		t.Error("Expected Allow() to return false after window is full")
	}

	// Wait for first request to expire
	time.Sleep(110 * time.Millisecond)

	// Should allow again
	if !sw.Allow() {
		t.Error("Expected Allow() to return true after oldest request expired")
	}
}

// TestSlidingWindowStats tests statistics
func TestSlidingWindowStats(t *testing.T) {
	sw := NewSlidingWindow(10, time.Second)

	sw.AllowN(4)

	stats := sw.Stats()
	if stats.Capacity != 10 {
		t.Errorf("Expected capacity 10, got %d", stats.Capacity)
	}
	if stats.Remaining != 6 {
		t.Errorf("Expected remaining 6, got %d", stats.Remaining)
	}
	if stats.Allowed != 4 {
		t.Errorf("Expected 4 allowed, got %d", stats.Allowed)
	}
}

// TestLeakyBucketBasic tests leaky bucket functionality
func TestLeakyBucketBasic(t *testing.T) {
	lb := NewLeakyBucket(10, 5) // 10 req/sec leak, burst 5
	defer lb.Stop()

	// Should allow burst
	for i := 0; i < 5; i++ {
		if !lb.Allow() {
			t.Errorf("Expected Allow() to return true for request %d", i+1)
		}
	}

	// Should reject after burst
	if lb.Allow() {
		t.Error("Expected Allow() to return false after burst")
	}
}

// TestLeakyBucketLeak tests leaking behavior
func TestLeakyBucketLeak(t *testing.T) {
	lb := NewLeakyBucket(100, 1) // 100 req/sec leak, burst 1
	defer lb.Stop()

	// Fill bucket
	lb.Allow()

	// Should reject
	if lb.Allow() {
		t.Error("Expected Allow() to return false when bucket is full")
	}

	// Wait for leak
	time.Sleep(20 * time.Millisecond)

	// Should allow now
	if !lb.Allow() {
		t.Error("Expected Allow() to return true after leak")
	}
}

// TestLeakyBucketStats tests statistics
func TestLeakyBucketStats(t *testing.T) {
	lb := NewLeakyBucket(10, 5)
	defer lb.Stop()

	lb.AllowN(3)

	stats := lb.Stats()
	if stats.Capacity != 5 {
		t.Errorf("Expected capacity 5, got %d", stats.Capacity)
	}
	if stats.Remaining != 2 {
		t.Errorf("Expected remaining 2, got %d", stats.Remaining)
	}
	if stats.Allowed != 3 {
		t.Errorf("Expected 3 allowed, got %d", stats.Allowed)
	}
}

// TestMultiLimiter tests multi-limiter functionality
func TestMultiLimiter(t *testing.T) {
	tb1 := NewTokenBucket(10, 1)
	defer tb1.Stop()
	tb2 := NewTokenBucket(5, 1)
	defer tb2.Stop()

	ml := NewMultiLimiter(tb1, tb2)

	// Should allow 5 requests (limited by tb2)
	for i := 0; i < 5; i++ {
		if !ml.Allow() {
			t.Errorf("Expected Allow() to return true for request %d", i+1)
		}
	}

	// Should reject 6th request
	if ml.Allow() {
		t.Error("Expected Allow() to return false when one limiter is exhausted")
	}
}

// TestPerClientLimiter tests per-client limiter functionality
func TestPerClientLimiter(t *testing.T) {
	pcl := NewPerClientLimiter(func() Limiter {
		return NewFixedWindow(3, time.Second)
	})
	defer pcl.Stop()

	// Client 1 should be allowed 3 requests
	for i := 0; i < 3; i++ {
		if !pcl.Allow("client1") {
			t.Errorf("Expected Allow(client1) to return true for request %d", i+1)
		}
	}

	// Client 1 should be rejected
	if pcl.Allow("client1") {
		t.Error("Expected Allow(client1) to return false after limit")
	}

	// Client 2 should still be allowed
	if !pcl.Allow("client2") {
		t.Error("Expected Allow(client2) to return true for first request")
	}

	// Check client count
	if pcl.ClientCount() != 2 {
		t.Errorf("Expected 2 clients, got %d", pcl.ClientCount())
	}
}

// TestPerClientLimiterStats tests per-client stats
func TestPerClientLimiterStats(t *testing.T) {
	pcl := NewPerClientLimiter(func() Limiter {
		return NewFixedWindow(5, time.Second)
	})
	defer pcl.Stop()

	pcl.Allow("client1")
	pcl.Allow("client2")

	stats := pcl.Stats()
	if len(stats) != 2 {
		t.Errorf("Expected stats for 2 clients, got %d", len(stats))
	}

	if _, ok := stats["client1"]; !ok {
		t.Error("Expected stats for client1")
	}
	if _, ok := stats["client2"]; !ok {
		t.Error("Expected stats for client2")
	}
}

// TestConcurrency tests thread safety
func TestConcurrency(t *testing.T) {
	tb := NewTokenBucket(100, 1000)
	defer tb.Stop()

	var wg sync.WaitGroup
	numGoroutines := 10
	requestsPerGoroutine := 10

	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < requestsPerGoroutine; j++ {
				tb.Allow()
			}
		}()
	}

	wg.Wait()

	stats := tb.Stats()
	expectedTotal := int64(numGoroutines * requestsPerGoroutine)
	if stats.Allowed+stats.Rejected != expectedTotal {
		t.Errorf("Expected total %d, got %d", expectedTotal, stats.Allowed+stats.Rejected)
	}
}

// TestFixedWindowWait tests fixed window wait functionality
func TestFixedWindowWait(t *testing.T) {
	fw := NewFixedWindow(1, 100*time.Millisecond)

	// Use the request
	fw.Allow()

	// Wait for window reset
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	err := fw.Wait(ctx)
	if err != nil {
		t.Errorf("Expected Wait to succeed, got error: %v", err)
	}
}

// TestSlidingWindowWait tests sliding window wait functionality
func TestSlidingWindowWait(t *testing.T) {
	sw := NewSlidingWindow(1, 100*time.Millisecond)

	// Use the request
	sw.Allow()

	// Wait for request to expire
	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	err := sw.Wait(ctx)
	if err != nil {
		t.Errorf("Expected Wait to succeed, got error: %v", err)
	}
}

// TestLeakyBucketWait tests leaky bucket wait functionality
func TestLeakyBucketWait(t *testing.T) {
	lb := NewLeakyBucket(100, 1) // 100 req/sec leak, burst 1
	defer lb.Stop()

	// Fill bucket
	lb.Allow()

	// Wait for leak
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	err := lb.Wait(ctx)
	if err != nil {
		t.Errorf("Expected Wait to succeed, got error: %v", err)
	}
}

// TestLimiterInterface tests that all limiters implement the interface
func TestLimiterInterface(t *testing.T) {
	var _ Limiter = NewTokenBucket(10, 1)
	var _ Limiter = NewFixedWindow(10, time.Second)
	var _ Limiter = NewSlidingWindow(10, time.Second)
	var _ Limiter = NewLeakyBucket(10, 5)
}
