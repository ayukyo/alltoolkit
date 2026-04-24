package debounce_utils

import (
	"context"
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestDebouncer_Basic(t *testing.T) {
	var counter int32
	d := NewDebouncer(50 * time.Millisecond)
	defer d.Close()

	// Call multiple times rapidly
	for i := 0; i < 5; i++ {
		d.Call(func() {
			atomic.AddInt32(&counter, 1)
		})
		time.Sleep(10 * time.Millisecond)
	}

	// Wait for debounce to complete
	time.Sleep(100 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected 1 call, got %d", counter)
	}
}

func TestDebouncer_Leading(t *testing.T) {
	var counter int32
	d := NewDebouncer(50*time.Millisecond, WithLeading())
	defer d.Close()

	d.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	time.Sleep(10 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected immediate leading call, got %d", counter)
	}

	// Subsequent calls should be debounced
	for i := 0; i < 3; i++ {
		d.Call(func() {
			atomic.AddInt32(&counter, 1)
		})
		time.Sleep(10 * time.Millisecond)
	}

	time.Sleep(100 * time.Millisecond)

	// Should have leading + trailing = 2
	if atomic.LoadInt32(&counter) != 2 {
		t.Errorf("Expected 2 calls (leading + trailing), got %d", counter)
	}
}

func TestDebouncer_Trailing(t *testing.T) {
	var counter int32
	d := NewDebouncer(50*time.Millisecond, WithTrailing(true))
	defer d.Close()

	d.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	time.Sleep(100 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected trailing call, got %d", counter)
	}
}

func TestDebouncer_Cancel(t *testing.T) {
	var counter int32
	d := NewDebouncer(50 * time.Millisecond)
	defer d.Close()

	d.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	d.Cancel()
	time.Sleep(100 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 0 {
		t.Errorf("Expected no calls after cancel, got %d", counter)
	}
}

func TestDebouncer_Flush(t *testing.T) {
	var counter int32
	d := NewDebouncer(100 * time.Millisecond)
	defer d.Close()

	d.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	d.Flush()
	time.Sleep(10 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected immediate call after flush, got %d", counter)
	}
}

func TestDebouncer_MaxWait(t *testing.T) {
	var counter int32
	d := NewDebouncer(200*time.Millisecond, WithMaxWait(50*time.Millisecond))
	defer d.Close()

	// Keep calling before the debounce delay
	for i := 0; i < 10; i++ {
		d.Call(func() {
			atomic.AddInt32(&counter, 1)
		})
		time.Sleep(10 * time.Millisecond)
	}

	time.Sleep(100 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected call triggered by maxWait, got %d", counter)
	}
}

func TestDebouncer_Context(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	d := NewDebouncer(100*time.Millisecond, WithContext(ctx))
	defer d.Close()

	var counter int32
	d.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	// Cancel context
	cancel()
	time.Sleep(10 * time.Millisecond)

	// Should still work (context just for lifecycle management)
	d.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	time.Sleep(150 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 2 {
		t.Errorf("Expected 2 calls, got %d", counter)
	}
}

func TestThrottler_Basic(t *testing.T) {
	var counter int32
	th := NewThrottler(50 * time.Millisecond)
	defer th.Close()

	// First call should execute immediately
	th.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	time.Sleep(10 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected immediate call, got %d", counter)
	}

	// Rapid calls should be throttled
	for i := 0; i < 5; i++ {
		th.Call(func() {
			atomic.AddInt32(&counter, 1)
		})
		time.Sleep(10 * time.Millisecond)
	}

	time.Sleep(100 * time.Millisecond)

	// Should have at most 3 calls: initial + trailing
	c := atomic.LoadInt32(&counter)
	if c > 3 {
		t.Errorf("Expected at most 3 calls, got %d", c)
	}
}

func TestThrottler_NoLeading(t *testing.T) {
	var counter int32
	th := NewThrottler(50*time.Millisecond, WithThrottleLeading(false))
	defer th.Close()

	th.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	time.Sleep(10 * time.Millisecond)

	// Without leading, should not execute immediately
	if atomic.LoadInt32(&counter) != 0 {
		t.Errorf("Expected no immediate call without leading, got %d", counter)
	}

	time.Sleep(100 * time.Millisecond)

	// Should have trailing call
	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected trailing call, got %d", counter)
	}
}

func TestThrottler_Cancel(t *testing.T) {
	var counter int32
	th := NewThrottler(100*time.Millisecond, WithThrottleLeading(false))
	defer th.Close()

	th.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	th.Cancel()
	time.Sleep(150 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 0 {
		t.Errorf("Expected no calls after cancel, got %d", counter)
	}
}

func TestThrottler_Flush(t *testing.T) {
	var counter int32
	th := NewThrottler(100*time.Millisecond, WithThrottleLeading(false))
	defer th.Close()

	th.Call(func() {
		atomic.AddInt32(&counter, 1)
	})

	th.Flush()
	time.Sleep(10 * time.Millisecond)

	if atomic.LoadInt32(&counter) != 1 {
		t.Errorf("Expected immediate call after flush, got %d", counter)
	}
}

func TestRateLimiter_Basic(t *testing.T) {
	rl := NewRateLimiter(10, 5) // 10 tokens/sec, burst of 5

	// Should allow burst
	for i := 0; i < 5; i++ {
		if !rl.Allow() {
			t.Errorf("Expected allow for token %d", i)
		}
	}

	// Should be rate limited
	if rl.Allow() {
		t.Error("Expected rate limit after burst exhausted")
	}

	// Wait for refill
	time.Sleep(200 * time.Millisecond)

	// Should allow again
	if !rl.Allow() {
		t.Error("Expected allow after refill")
	}
}

func TestRateLimiter_Wait(t *testing.T) {
	rl := NewRateLimiter(100, 1) // 100 tokens/sec, burst of 1

	ctx := context.Background()

	// First should succeed immediately
	start := time.Now()
	if err := rl.Wait(ctx); err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	elapsed := time.Since(start)
	if elapsed > 10*time.Millisecond {
		t.Errorf("Wait took too long: %v", elapsed)
	}

	// Second should wait
	start = time.Now()
	if err := rl.Wait(ctx); err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	elapsed = time.Since(start)
	if elapsed < 5*time.Millisecond {
		t.Errorf("Wait should have taken some time: %v", elapsed)
	}
}

func TestRateLimiter_WaitContext(t *testing.T) {
	rl := NewRateLimiter(1, 0) // Very slow, no burst

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
	defer cancel()

	err := rl.Wait(ctx)
	if err != context.DeadlineExceeded {
		t.Errorf("Expected deadline exceeded, got: %v", err)
	}
}

func TestRateLimiter_Tokens(t *testing.T) {
	rl := NewRateLimiter(100, 10)

	if rl.Tokens() != 10 {
		t.Errorf("Expected 10 tokens, got %f", rl.Tokens())
	}

	rl.Allow()

	if rl.Tokens() != 9 {
		t.Errorf("Expected 9 tokens, got %f", rl.Tokens())
	}
}

func TestDelay_Basic(t *testing.T) {
	d := NewDelay(50 * time.Millisecond)

	start := time.Now()
	d.Call(func() {})
	elapsed1 := time.Since(start)

	start = time.Now()
	d.Call(func() {})
	elapsed2 := time.Since(start)

	if elapsed1 > 20*time.Millisecond {
		t.Errorf("First call should be fast: %v", elapsed1)
	}

	if elapsed2 < 40*time.Millisecond {
		t.Errorf("Second call should have delay: %v", elapsed2)
	}
}

func TestDelay_Async(t *testing.T) {
	d := NewDelay(50 * time.Millisecond)
	var wg sync.WaitGroup
	var counter int32

	for i := 0; i < 3; i++ {
		wg.Add(1)
		go d.CallAsync(func() {
			atomic.AddInt32(&counter, 1)
			wg.Done()
		})
	}

	wg.Wait()

	if counter != 3 {
		t.Errorf("Expected 3 calls, got %d", counter)
	}
}

func TestBatch_Basic(t *testing.T) {
	var processed [][]int
	var mu sync.Mutex

	b := NewBatch[int](3, WithBatchProcessor[int](func(items []int) {
		mu.Lock()
		processed = append(processed, items)
		mu.Unlock()
	}))

	b.Add(1)
	b.Add(2)

	time.Sleep(10 * time.Millisecond)

	mu.Lock()
	if len(processed) != 0 {
		t.Errorf("Should not have processed yet, got %d batches", len(processed))
	}
	mu.Unlock()

	b.Add(3) // Should trigger batch

	time.Sleep(50 * time.Millisecond)

	mu.Lock()
	if len(processed) != 1 {
		t.Errorf("Expected 1 batch, got %d", len(processed))
	}
	if len(processed) > 0 && len(processed[0]) != 3 {
		t.Errorf("Expected 3 items in batch, got %d", len(processed[0]))
	}
	mu.Unlock()
}

func TestBatch_Timeout(t *testing.T) {
	var processed [][]int
	var mu sync.Mutex

	b := NewBatch[int](10, WithBatchTimeout[int](50*time.Millisecond), WithBatchProcessor[int](func(items []int) {
		mu.Lock()
		processed = append(processed, items)
		mu.Unlock()
	}))

	b.Add(1)
	b.Add(2)

	time.Sleep(100 * time.Millisecond)

	mu.Lock()
	if len(processed) != 1 {
		t.Errorf("Expected 1 batch from timeout, got %d", len(processed))
	}
	if len(processed) > 0 && len(processed[0]) != 2 {
		t.Errorf("Expected 2 items in batch, got %d", len(processed[0]))
	}
	mu.Unlock()
}

func TestBatch_Flush(t *testing.T) {
	var processed [][]int
	var mu sync.Mutex

	b := NewBatch[int](10, WithBatchProcessor[int](func(items []int) {
		mu.Lock()
		processed = append(processed, items)
		mu.Unlock()
	}))

	b.Add(1)
	b.Add(2)
	b.Flush()

	time.Sleep(50 * time.Millisecond)

	mu.Lock()
	if len(processed) != 1 {
		t.Errorf("Expected 1 batch after flush, got %d", len(processed))
	}
	if len(processed) > 0 && len(processed[0]) != 2 {
		t.Errorf("Expected 2 items in batch, got %d", len(processed[0]))
	}
	mu.Unlock()
}

func TestBatch_Size(t *testing.T) {
	b := NewBatch[int](10)

	if b.Size() != 0 {
		t.Errorf("Expected size 0, got %d", b.Size())
	}

	b.Add(1)
	b.Add(2)

	if b.Size() != 2 {
		t.Errorf("Expected size 2, got %d", b.Size())
	}
}

// Example tests
func ExampleDebouncer() {
	d := NewDebouncer(100 * time.Millisecond)
	defer d.Close()

	// Rapid calls - only the last one will execute
	d.Call(func() { fmt.Println("Call 1") })
	d.Call(func() { fmt.Println("Call 2") })
	d.Call(func() { fmt.Println("Call 3") })

	time.Sleep(200 * time.Millisecond)
	// Output: Call 3
}

func ExampleDebouncer_leading() {
	d := NewDebouncer(100*time.Millisecond, WithLeading())
	defer d.Close()

	// With leading, the first call executes immediately
	d.Call(func() { fmt.Println("First") })
	time.Sleep(150 * time.Millisecond)
	// Output: First
}

func ExampleThrottler() {
	th := NewThrottler(100 * time.Millisecond)
	defer th.Close()

	for i := 0; i < 5; i++ {
		th.Call(func() { fmt.Println("Called") })
		time.Sleep(30 * time.Millisecond)
	}
	time.Sleep(150 * time.Millisecond)
	// Output varies - throttled calls
}

func ExampleRateLimiter() {
	rl := NewRateLimiter(10, 5) // 10 requests/sec, burst of 5

	for i := 0; i < 8; i++ {
		if rl.Allow() {
			fmt.Printf("Request %d allowed\n", i+1)
		} else {
			fmt.Printf("Request %d limited\n", i+1)
		}
	}
	// Output:
	// Request 1 allowed
	// Request 2 allowed
	// Request 3 allowed
	// Request 4 allowed
	// Request 5 allowed
	// Request 6 limited
	// Request 7 limited
	// Request 8 limited
}

func ExampleBatch() {
	b := NewBatch[string](3, WithBatchProcessor[string](func(items []string) {
		fmt.Printf("Processing batch: %v\n", items)
	}))

	b.Add("a")
	b.Add("b")
	b.Add("c") // Triggers batch processing
	time.Sleep(50 * time.Millisecond)
	// Output: Processing batch: [a b c]
}

func ExampleDelay() {
	d := NewDelay(100 * time.Millisecond)

	fmt.Println("Start")
	d.Call(func() { fmt.Println("First") })
	d.Call(func() { fmt.Println("Second") })
	// Output:
	// Start
	// First
	// (waits ~100ms)
	// Second
}

// Benchmark tests
func BenchmarkDebouncer_Call(b *testing.B) {
	d := NewDebouncer(time.Millisecond)
	defer d.Close()

	for i := 0; i < b.N; i++ {
		d.Call(func() {})
	}
}

func BenchmarkThrottler_Call(b *testing.B) {
	th := NewThrottler(time.Microsecond)
	defer th.Close()

	for i := 0; i < b.N; i++ {
		th.Call(func() {})
	}
}

func BenchmarkRateLimiter_Allow(b *testing.B) {
	rl := NewRateLimiter(1000000, 1000000)

	for i := 0; i < b.N; i++ {
		rl.Allow()
	}
}

func BenchmarkBatch_Add(b *testing.B) {
	batch := NewBatch[int](100)

	for i := 0; i < b.N; i++ {
		batch.Add(i)
	}
}

func BenchmarkDelay_Call(b *testing.B) {
	d := NewDelay(time.Nanosecond)

	for i := 0; i < b.N; i++ {
		d.Call(func() {})
	}
}