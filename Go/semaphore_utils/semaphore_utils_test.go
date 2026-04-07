package semaphore_utils

import (
	"context"
	"sync"
	"testing"
	"time"
)

// TestNew tests semaphore creation
func TestNew(t *testing.T) {
	sem := New(10)
	if sem.Capacity() != 10 {
		t.Errorf("Expected capacity 10, got %d", sem.Capacity())
	}
	if sem.Available() != 10 {
		t.Errorf("Expected 10 available, got %d", sem.Available())
	}
	if sem.InUse() != 0 {
		t.Errorf("Expected 0 in use, got %d", sem.InUse())
	}

	// Test zero capacity defaults to 1
	sem2 := New(0)
	if sem2.Capacity() != 1 {
		t.Errorf("Expected capacity 1 for zero input, got %d", sem2.Capacity())
	}

	// Test negative capacity defaults to 1
	sem3 := New(-5)
	if sem3.Capacity() != 1 {
		t.Errorf("Expected capacity 1 for negative input, got %d", sem3.Capacity())
	}
}

// TestAcquire tests basic acquire/release
func TestAcquire(t *testing.T) {
	sem := New(2)
	ctx := context.Background()

	// Acquire first permit
	if err := sem.Acquire(ctx); err != nil {
		t.Errorf("Failed to acquire: %v", err)
	}
	if sem.Available() != 1 {
		t.Errorf("Expected 1 available, got %d", sem.Available())
	}
	if sem.InUse() != 1 {
		t.Errorf("Expected 1 in use, got %d", sem.InUse())
	}

	// Acquire second permit
	if err := sem.Acquire(ctx); err != nil {
		t.Errorf("Failed to acquire: %v", err)
	}
	if sem.Available() != 0 {
		t.Errorf("Expected 0 available, got %d", sem.Available())
	}
	if sem.InUse() != 2 {
		t.Errorf("Expected 2 in use, got %d", sem.InUse())
	}

	// Release one permit
	sem.Release()
	if sem.Available() != 1 {
		t.Errorf("Expected 1 available after release, got %d", sem.Available())
	}
	if sem.InUse() != 1 {
		t.Errorf("Expected 1 in use after release, got %d", sem.InUse())
	}

	// Release second permit
	sem.Release()
	if sem.Available() != 2 {
		t.Errorf("Expected 2 available after release, got %d", sem.Available())
	}
	if sem.InUse() != 0 {
		t.Errorf("Expected 0 in use after release, got %d", sem.InUse())
	}
}

// TestAcquireTimeout tests timeout functionality
func TestAcquireTimeout(t *testing.T) {
	sem := New(1)
	ctx := context.Background()

	// Acquire the only permit
	if err := sem.Acquire(ctx); err != nil {
		t.Fatalf("Failed to acquire: %v", err)
	}

	// Try to acquire with timeout - should timeout
	start := time.Now()
	err := sem.AcquireTimeout(100 * time.Millisecond)
	elapsed := time.Since(start)

	if err != ErrTimeout {
		t.Errorf("Expected ErrTimeout, got %v", err)
	}
	if elapsed < 100*time.Millisecond || elapsed > 200*time.Millisecond {
		t.Errorf("Expected timeout around 100ms, got %v", elapsed)
	}

	// Release and try again - should succeed
	sem.Release()
	err = sem.AcquireTimeout(100 * time.Millisecond)
	if err != nil {
		t.Errorf("Expected success after release, got %v", err)
	}
}

// TestTryAcquire tests non-blocking acquire
func TestTryAcquire(t *testing.T) {
	sem := New(1)

	// First try should succeed
	if !sem.TryAcquire() {
		t.Error("Expected TryAcquire to succeed")
	}

	// Second try should fail (semaphore full)
	if sem.TryAcquire() {
		t.Error("Expected TryAcquire to fail when full")
	}

	// Release and try again
	sem.Release()
	if !sem.TryAcquire() {
		t.Error("Expected TryAcquire to succeed after release")
	}
}

// TestContextCancellation tests context cancellation
func TestContextCancellation(t *testing.T) {
	sem := New(1)
	ctx, cancel := context.WithCancel(context.Background())

	// Acquire the only permit
	if err := sem.Acquire(ctx); err != nil {
		t.Fatalf("Failed to acquire: %v", err)
	}

	// Start goroutine waiting for permit
	done := make(chan error, 1)
	go func() {
		done <- sem.Acquire(ctx)
	}()

	// Cancel context
	time.Sleep(50 * time.Millisecond)
	cancel()

	// Should get cancellation error
	select {
	case err := <-done:
		if err != ErrCancelled {
			t.Errorf("Expected ErrCancelled, got %v", err)
		}
	case <-time.After(time.Second):
		t.Error("Timeout waiting for cancellation")
	}
}

// TestConcurrency tests concurrent access
func TestConcurrency(t *testing.T) {
	sem := New(3)
	ctx := context.Background()

	var wg sync.WaitGroup
	maxConcurrent := 0
	currentConcurrent := 0
	var mu sync.Mutex

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()

			if err := sem.Acquire(ctx); err != nil {
				t.Errorf("Failed to acquire: %v", err)
				return
			}
			defer sem.Release()

			mu.Lock()
			currentConcurrent++
			if currentConcurrent > maxConcurrent {
				maxConcurrent = currentConcurrent
			}
			mu.Unlock()

			time.Sleep(50 * time.Millisecond)

			mu.Lock()
			currentConcurrent--
			mu.Unlock()
		}()
	}

	wg.Wait()

	if maxConcurrent > 3 {
		t.Errorf("Expected max 3 concurrent, got %d", maxConcurrent)
	}
}

// TestWeightedSemaphore tests weighted semaphore
func TestWeightedSemaphore(t *testing.T) {
	sem := NewWeighted(10)
	ctx := context.Background()

	// Acquire 5 units
	if err := sem.Acquire(ctx, 5); err != nil {
		t.Errorf("Failed to acquire 5: %v", err)
	}
	if sem.Available() != 5 {
		t.Errorf("Expected 5 available, got %d", sem.Available())
	}
	if sem.InUse() != 5 {
		t.Errorf("Expected 5 in use, got %d", sem.InUse())
	}

	// Acquire 3 more units
	if err := sem.Acquire(ctx, 3); err != nil {
		t.Errorf("Failed to acquire 3: %v", err)
	}
	if sem.Available() != 2 {
		t.Errorf("Expected 2 available, got %d", sem.Available())
	}

	// Release 5 units
	sem.Release(5)
	if sem.Available() != 7 {
		t.Errorf("Expected 7 available, got %d", sem.Available())
	}

	// Try to acquire more than capacity
	if err := sem.Acquire(ctx, 20); err == nil {
		t.Error("Expected error when acquiring more than capacity")
	}

	// Try to acquire zero or negative
	if err := sem.Acquire(ctx, 0); err == nil {
		t.Error("Expected error when acquiring zero")
	}
}

// TestWeightedTryAcquire tests weighted try acquire
func TestWeightedTryAcquire(t *testing.T) {
	sem := NewWeighted(10)

	// Should succeed
	if !sem.TryAcquire(5) {
		t.Error("Expected TryAcquire(5) to succeed")
	}

	// Should fail (not enough capacity)
	if sem.TryAcquire(10) {
		t.Error("Expected TryAcquire(10) to fail")
	}

	// Should succeed (exactly enough)
	if !sem.TryAcquire(5) {
		t.Error("Expected TryAcquire(5) to succeed for remaining capacity")
	}

	// Zero or negative should fail
	if sem.TryAcquire(0) {
		t.Error("Expected TryAcquire(0) to fail")
	}
}

// TestWeightedTimeout tests weighted semaphore timeout
func TestWeightedTimeout(t *testing.T) {
	sem := NewWeighted(5)
	ctx := context.Background()

	// Acquire all capacity
	if err := sem.Acquire(ctx, 5); err != nil {
		t.Fatalf("Failed to acquire: %v", err)
	}

	// Try to acquire with timeout - should timeout
	err := sem.AcquireTimeout(100*time.Millisecond, 3)
	if err != ErrTimeout {
		t.Errorf("Expected ErrTimeout, got %v", err)
	}

	// Release and try again
	sem.Release(5)
	err = sem.AcquireTimeout(100*time.Millisecond, 3)
	if err != nil {
		t.Errorf("Expected success after release, got %v", err)
	}
}

// TestSemaphorePool tests semaphore pool
func TestSemaphorePool(t *testing.T) {
	pool := NewPool(2)

	// Get semaphore for key "A"
	semA := pool.Get("A")
	if semA == nil {
		t.Fatal("Expected non-nil semaphore")
	}
	if pool.Size() != 1 {
		t.Errorf("Expected pool size 1, got %d", pool.Size())
	}

	// Get same semaphore again
	semA2 := pool.Get("A")
	if semA != semA2 {
		t.Error("Expected same semaphore for same key")
	}
	if pool.Size() != 1 {
		t.Errorf("Expected pool size still 1, got %d", pool.Size())
	}

	// Get semaphore for key "B"
	semB := pool.Get("B")
	if semB == nil {
		t.Fatal("Expected non-nil semaphore")
	}
	if pool.Size() != 2 {
		t.Errorf("Expected pool size 2, got %d", pool.Size())
	}

	// Check keys
	keys := pool.Keys()
	if len(keys) != 2 {
		t.Errorf("Expected 2 keys, got %d", len(keys))
	}

	// Remove semaphore
	pool.Remove("A")
	if pool.Size() != 1 {
		t.Errorf("Expected pool size 1 after removal, got %d", pool.Size())
	}

	// Get new semaphore for removed key
	semA3 := pool.Get("A")
	if semA == semA3 {
		t.Error("Expected new semaphore after removal")
	}
}

// TestRunWithSemaphore tests helper function
func TestRunWithSemaphore(t *testing.T) {
	sem := New(1)
	ctx := context.Background()

	executed := false
	err := RunWithSemaphore(ctx, sem, func() error {
		executed = true
		return nil
	})

	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if !executed {
		t.Error("Expected function to be executed")
	}
	if sem.InUse() != 0 {
		t.Errorf("Expected semaphore to be released, got %d in use", sem.InUse())
	}
}

// TestRunWithTimeout tests timeout helper
func TestRunWithTimeout(t *testing.T) {
	sem := New(1)

	// First acquire
	sem.Acquire(context.Background())

	// Try to run with timeout - should timeout
	err := RunWithTimeout(100*time.Millisecond, sem, func() error {
		return nil
	})

	if err != ErrTimeout {
		t.Errorf("Expected ErrTimeout, got %v", err)
	}

	// Release and try again
	sem.Release()
	executed := false
	err = RunWithTimeout(100*time.Millisecond, sem, func() error {
		executed = true
		return nil
	})

	if err != nil {
		t.Errorf("Expected success, got %v", err)
	}
	if !executed {
		t.Error("Expected function to be executed")
	}
}

// TestRunWeightedWithSemaphore tests weighted helper
func TestRunWeightedWithSemaphore(t *testing.T) {
	sem := NewWeighted(10)
	ctx := context.Background()

	executed := false
	err := RunWeightedWithSemaphore(ctx, sem, 5, func() error {
		executed = true
		return nil
	})

	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if !executed {
		t.Error("Expected function to be executed")
	}
	if sem.InUse() != 0 {
		t.Errorf("Expected semaphore to be released, got %d in use", sem.InUse())
	}
}

// TestBatchAcquire tests batch acquire
func TestBatchAcquire(t *testing.T) {
	sem1 := NewWeighted(10)
	sem2 := NewWeighted(10)
	ctx := context.Background()

	// Acquire some units first
	sem1.Acquire(ctx, 5)
	sem2.Acquire(ctx, 3)

	// Batch acquire more
	release, err := BatchAcquire(ctx, map[*WeightedSemaphore]int64{
		sem1: 3,
		sem2: 5,
	})

	if err != nil {
		t.Errorf("Expected success, got %v", err)
	}

	if sem1.InUse() != 8 {
		t.Errorf("Expected 8 in sem1, got %d", sem1.InUse())
	}
	if sem2.InUse() != 8 {
		t.Errorf("Expected 8 in sem2, got %d", sem2.InUse())
	}

	// Release
	release()

	if sem1.InUse() != 5 {
		t.Errorf("Expected 5 in sem1 after release, got %d", sem1.InUse())
	}
	if sem2.InUse() != 3 {
		t.Errorf("Expected 3 in sem2 after release, got %d", sem2.InUse())
	}
}

// TestBatchAcquireFailure tests batch acquire failure handling
func TestBatchAcquireFailure(t *testing.T) {
	sem1 := NewWeighted(10)
	sem2 := NewWeighted(5)
	ctx := context.Background()

	// Fill sem2 completely
	sem2.Acquire(ctx, 5)

	// Try batch acquire - should fail on sem2
	release, err := BatchAcquire(ctx, map[*WeightedSemaphore]int64{
		sem1: 3,
		sem2: 1, // This should fail
	})

	if err == nil {
		t.Error("Expected error when batch acquire fails")
	}
	if release != nil {
		t.Error("Expected nil release function on failure")
	}

	// sem1 should not have the units
	if sem1.InUse() != 0 {
		t.Errorf("Expected sem1 to have 0 (rolled back), got %d", sem1.InUse())
	}
}

// TestWaiters tests waiter count
func TestWaiters(t *testing.T) {
	sem := New(1)
	ctx := context.Background()

	// Acquire the only permit
	sem.Acquire(ctx)

	// Start multiple goroutines waiting
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			sem.Acquire(ctx)
			sem.Release()
		}()
	}

	// Give goroutines time to start waiting
	time.Sleep(100 * time.Millisecond)

	if sem.Waiters() != 3 {
		t.Errorf("Expected 3 waiters, got %d", sem.Waiters())
	}

	// Release and wait
	sem.Release()
	wg.Wait()

	if sem.Waiters() != 0 {
		t.Errorf("Expected 0 waiters, got %d", sem.Waiters())
	}
}

// TestWeightedWaiters tests weighted waiter count
func TestWeightedWaiters(t *testing.T) {
	sem := NewWeighted(5)
	ctx := context.Background()

	// Acquire all capacity
	sem.Acquire(ctx, 5)

	// Start goroutine waiting for more than available
	go func() {
		sem.Acquire(ctx, 3)
		sem.Release(3)
	}()

	// Give goroutine time to start waiting
	time.Sleep(50 * time.Millisecond)

	if sem.Waiters() != 1 {
		t.Errorf("Expected 1 waiter, got %d", sem.Waiters())
	}

	// Release and wait
	sem.Release(5)
	time.Sleep(50 * time.Millisecond)

	if sem.Waiters() != 0 {
		t.Errorf("Expected 0 waiters, got %d", sem.Waiters())
	}
}

// BenchmarkAcquire benchmarks semaphore acquire/release
func BenchmarkAcquire(b *testing.B) {
	sem := New(10)
	ctx := context.Background()

	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			sem.Acquire(ctx)
			sem.Release()
		}
	})
}

// BenchmarkWeightedAcquire benchmarks weighted semaphore
func BenchmarkWeightedAcquire(b *testing.B) {
	sem := NewWeighted(100)
	ctx := context.Background()

	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			sem.Acquire(ctx, 1)
			sem.Release(1)
		}
	})
}