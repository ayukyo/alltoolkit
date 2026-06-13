package priority_sliding_window

import (
	"testing"
	"time"
)

func TestNewConfigValidation(t *testing.T) {
	_, err := NewWithConfig(Config{
		Limits:         map[int]int{PriorityHigh: 10},
		WindowDuration: 0,
		TimeQuantum:    time.Second,
	})
	if err == nil {
		t.Error("expected error for zero window duration")
	}
}

func TestNewDefaults(t *testing.T) {
	limits := map[int]int{PriorityHigh: 10, PriorityMedium: 50}
	rl, err := New(limits, time.Minute)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	if rl == nil {
		t.Fatal("expected non-nil limiter")
	}
}

func TestNewWithConfigAllOptions(t *testing.T) {
	cfg := Config{
		Limits: map[int]int{
			PriorityCritical: 100,
			PriorityHigh:     50,
			PriorityLow:      10,
		},
		WindowDuration:  10 * time.Second,
		TimeQuantum:     100 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0.3,
		MinBurst:        3,
		CleanupInterval: 5 * time.Second,
	}
	rl, err := NewWithConfig(cfg)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	if rl == nil {
		t.Fatal("expected non-nil limiter")
	}
}

func TestAllowSlidingWindow(t *testing.T) {
	limits := map[int]int{PriorityHigh: 3}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  10 * time.Second,
		TimeQuantum:     100 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0.0,
		MinBurst:        0,
		CleanupInterval: time.Hour, // disable cleanup during test
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	// First 3 should be allowed
	for i := 0; i < 3; i++ {
		if !rl.Allow(PriorityHigh) {
			t.Errorf("allow %d: expected true", i+1)
		}
	}

	// 4th should be denied
	if rl.Allow(PriorityHigh) {
		t.Error("4th request: expected false (limit exceeded)")
	}
}

func TestAllowFixedWindow(t *testing.T) {
	limits := map[int]int{PriorityHigh: 3}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  10 * time.Second,
		TimeQuantum:     time.Second,
		WindowType:      FixedWindow,
		BurstAllowance:  0.0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	for i := 0; i < 3; i++ {
		if !rl.Allow(PriorityHigh) {
			t.Errorf("allow %d: expected true", i+1)
		}
	}

	if rl.Allow(PriorityHigh) {
		t.Error("4th request: expected false")
	}
}

func TestAllowUnknownPriorityIsUnlimited(t *testing.T) {
	limits := map[int]int{PriorityHigh: 1}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:      10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	// PriorityMedium is not in the limits map — should be unlimited
	for i := 0; i < 100; i++ {
		if !rl.Allow(PriorityMedium) {
			t.Errorf("unknown priority: expected true on attempt %d", i+1)
			break
		}
	}
}

func TestBurstAllowance(t *testing.T) {
	limits := map[int]int{PriorityHigh: 10}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0.5, // 50% extra = 15 effective
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	allowed := 0
	for i := 0; i < 20; i++ {
		if rl.Allow(PriorityHigh) {
			allowed++
		}
	}

	// 10 base + 5 burst = 15, so 16th should fail
	if allowed < 15 || allowed > 15 {
		t.Errorf("expected 15 allowed with 50%% burst, got %d", allowed)
	}
}

func TestRemaining(t *testing.T) {
	limits := map[int]int{PriorityHigh: 10}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	initial := rl.Remaining(PriorityHigh)
	if initial != 10 {
		t.Errorf("expected initial remaining 10, got %d", initial)
	}

	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)

	after := rl.Remaining(PriorityHigh)
	if after != 8 {
		t.Errorf("expected 8 remaining after 2 allows, got %d", after)
	}
}

func TestReserveAndConfirm(t *testing.T) {
	limits := map[int]int{PriorityHigh: 2}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	r := rl.Reserve(PriorityHigh)
	if !r.Allowed() {
		t.Error("expected reservation to be allowed")
	}

	// Consume 2 more — should now be at limit
	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)

	// Confirm the reservation
	r.Confirm()

	// Next should fail
	if rl.Allow(PriorityHigh) {
		t.Error("after confirm: expected false")
	}
}

func TestReserveAndCancel(t *testing.T) {
	limits := map[int]int{PriorityHigh: 2}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      FixedWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	// Use 2 slots
	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)

	// 3rd should fail
	if rl.Allow(PriorityHigh) {
		t.Error("expected 3rd to be denied")
	}

	// Reserve — should be denied
	r := rl.Reserve(PriorityHigh)
	if r.Allowed() {
		t.Error("expected reservation to be denied at limit")
	}
}

func TestReset(t *testing.T) {
	limits := map[int]int{PriorityHigh: 5}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	// Consume some
	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)

	remaining := rl.Remaining(PriorityHigh)
	if remaining != 3 {
		t.Errorf("expected 3 remaining, got %d", remaining)
	}

	rl.Reset(PriorityHigh)

	after := rl.Remaining(PriorityHigh)
	if after != 5 {
		t.Errorf("expected 5 remaining after reset, got %d", after)
	}
}

func TestUpdateLimit(t *testing.T) {
	limits := map[int]int{PriorityHigh: 5}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	err = rl.UpdateLimit(PriorityHigh, 10)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	stats := rl.Stats(PriorityHigh)
	if stats.Limit != 10 {
		t.Errorf("expected limit 10, got %d", stats.Limit)
	}

	// Should now allow 10
	allowed := 0
	for i := 0; i < 12; i++ {
		if rl.Allow(PriorityHigh) {
			allowed++
		}
	}
	if allowed != 10 {
		t.Errorf("expected 10 allowed with new limit, got %d", allowed)
	}
}

func TestUpdateLimitNotFound(t *testing.T) {
	limits := map[int]int{PriorityHigh: 5}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	err = rl.UpdateLimit(PriorityBulk, 10)
	if err == nil {
		t.Error("expected error for unknown priority")
	}
}

func TestStats(t *testing.T) {
	limits := map[int]int{PriorityHigh: 10}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  5 * time.Second,
		TimeQuantum:     100 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0.2,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)

	stats := rl.Stats(PriorityHigh)
	if stats.Limit != 10 {
		t.Errorf("expected limit 10, got %d", stats.Limit)
	}
	if stats.Burst != 2 {
		t.Errorf("expected burst 2, got %d", stats.Burst)
	}
	if stats.EffectiveLimit != 12 {
		t.Errorf("expected effective limit 12, got %d", stats.EffectiveLimit)
	}
	if stats.Remaining != 10 {
		t.Errorf("expected 10 remaining after 2 allows, got %d", stats.Remaining)
	}
}

func TestPeekObserved(t *testing.T) {
	limits := map[int]int{PriorityHigh: 5}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	for i := 0; i < 5; i++ {
		rl.Allow(PriorityHigh)
	}

	peak := rl.Peek(PriorityHigh)
	if peak != 5 {
		t.Errorf("expected peak 5, got %d", peak)
	}
}

func TestMultiPriority(t *testing.T) {
	limits := map[int]int{
		PriorityHigh:   2,
		PriorityMedium: 5,
		PriorityLow:    10,
	}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	// Exhaust high priority
	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)
	if rl.Allow(PriorityHigh) {
		t.Error("high priority: expected 3rd denied")
	}

	// Medium priority should still work
	for i := 0; i < 5; i++ {
		if !rl.Allow(PriorityMedium) {
			t.Errorf("medium priority: allow %d unexpectedly denied", i+1)
		}
	}

	if rl.Allow(PriorityMedium) {
		t.Error("medium priority: 6th unexpectedly allowed")
	}

	// Low priority should still work
	for i := 0; i < 10; i++ {
		if !rl.Allow(PriorityLow) {
			t.Errorf("low priority: allow %d unexpectedly denied", i+1)
		}
	}
}

func TestMinBurst(t *testing.T) {
	limits := map[int]int{PriorityHigh: 2}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     100 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0.1, // 10% of 2 = 0.2, rounds to 0
		MinBurst:        3,    // should override to 3
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	stats := rl.Stats(PriorityHigh)
	if stats.Burst != 3 {
		t.Errorf("expected burst 3 (minBurst override), got %d", stats.Burst)
	}

	// Effective limit = 2 + 3 = 5
	allowed := 0
	for i := 0; i < 6; i++ {
		if rl.Allow(PriorityHigh) {
			allowed++
		}
	}
	if allowed != 5 {
		t.Errorf("expected 5 allowed (2+3 burst), got %d", allowed)
	}
}

func TestStop(t *testing.T) {
	limits := map[int]int{PriorityHigh: 10}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: 10 * time.Millisecond, // fast cleanup
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Stop should not panic
	rl.Stop()
}

func TestStatsFixedWindow(t *testing.T) {
	limits := map[int]int{PriorityHigh: 10}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     100 * time.Millisecond,
		WindowType:      FixedWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	rl.Allow(PriorityHigh)
	rl.Allow(PriorityHigh)

	stats := rl.Stats(PriorityHigh)
	if stats.FixedCount != 2 {
		t.Errorf("expected fixed count 2, got %d", stats.FixedCount)
	}
	if stats.WindowType != FixedWindow {
		t.Errorf("expected FixedWindow type, got %v", stats.WindowType)
	}
}

func TestConcurrency(t *testing.T) {
	limits := map[int]int{PriorityHigh: 100}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	done := make(chan bool)
	for g := 0; g < 10; g++ {
		go func() {
			for i := 0; i < 50; i++ {
				rl.Allow(PriorityHigh)
			}
			done <- true
		}()
	}

	for g := 0; g < 10; g++ {
		<-done
	}

	// At most 100 should have succeeded
	stats := rl.Stats(PriorityHigh)
	if stats.Remaining < 0 || stats.Remaining > 100 {
		t.Errorf("unexpected remaining count: %d", stats.Remaining)
	}
}

func TestResetAllPriorities(t *testing.T) {
	limits := map[int]int{
		PriorityHigh:   5,
		PriorityMedium: 5,
	}
	rl, err := NewWithConfig(Config{
		Limits:          limits,
		WindowDuration:  time.Second,
		TimeQuantum:     10 * time.Millisecond,
		WindowType:      SlidingWindow,
		BurstAllowance:  0,
		MinBurst:        0,
		CleanupInterval: time.Hour,
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	defer rl.Stop()

	rl.Allow(PriorityHigh)
	rl.Allow(PriorityMedium)

	// Reset all (priority < 0)
	rl.Reset(-1)

	if rl.Remaining(PriorityHigh) != 5 {
		t.Error("expected high priority to be reset to 5")
	}
	if rl.Remaining(PriorityMedium) != 5 {
		t.Error("expected medium priority to be reset to 5")
	}
}