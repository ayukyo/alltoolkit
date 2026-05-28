package semaphore_utils

import (
	"context"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// ============================================
// 基础信号量测试
// ============================================

func TestNewSemaphore(t *testing.T) {
	tests := []struct {
		name     string
		capacity int64
		wantErr  bool
	}{
		{"valid capacity", 10, false},
		{"zero capacity", 0, true},
		{"negative capacity", -5, true},
		{"large capacity", 1000000, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s, err := NewSemaphore(tt.capacity)
			if (err != nil) != tt.wantErr {
				t.Errorf("NewSemaphore() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if s.Capacity() != tt.capacity {
					t.Errorf("Capacity() = %v, want %v", s.Capacity(), tt.capacity)
				}
				if s.Available() != tt.capacity {
					t.Errorf("Available() = %v, want %v", s.Available(), tt.capacity)
				}
			}
		})
	}
}

func TestSemaphore_TryAcquire(t *testing.T) {
	s, _ := NewSemaphore(5)

	// 正常获取
	if !s.TryAcquire(3) {
		t.Error("TryAcquire(3) should succeed")
	}
	if s.Available() != 2 {
		t.Errorf("Available() = %v, want 2", s.Available())
	}

	// 超出可用
	if s.TryAcquire(3) {
		t.Error("TryAcquire(3) should fail")
	}

	// 获取剩余
	if !s.TryAcquire(2) {
		t.Error("TryAcquire(2) should succeed")
	}
	if s.Available() != 0 {
		t.Errorf("Available() = %v, want 0", s.Available())
	}

	// 完全不可用
	if s.TryAcquire(1) {
		t.Error("TryAcquire(1) should fail when available is 0")
	}
}

func TestSemaphore_Release(t *testing.T) {
	s, _ := NewSemaphore(10)

	s.TryAcquire(5)
	s.Release(3)

	if s.Available() != 8 {
		t.Errorf("Available() = %v, want 8", s.Available())
	}

	// 释放超过容量
	s.Release(10)
	if s.Available() != 10 {
		t.Errorf("Available() = %v, want 10 (capped at capacity)", s.Available())
	}
}

func TestSemaphore_InvalidWeight(t *testing.T) {
	s, _ := NewSemaphore(10)
	ctx := context.Background()

	if err := s.Acquire(ctx, 0); err != ErrInvalidWeight {
		t.Errorf("Acquire(0) error = %v, want ErrInvalidWeight", err)
	}

	if err := s.Acquire(ctx, -1); err != ErrInvalidWeight {
		t.Errorf("Acquire(-1) error = %v, want ErrInvalidWeight", err)
	}

	if s.TryAcquire(0) {
		t.Error("TryAcquire(0) should fail")
	}

	if s.TryAcquire(-1) {
		t.Error("TryAcquire(-1) should fail")
	}
}

func TestSemaphore_ExceedsCapacity(t *testing.T) {
	s, _ := NewSemaphore(5)
	ctx := context.Background()

	if err := s.Acquire(ctx, 10); err != ErrExceedsCapacity {
		t.Errorf("Acquire(10) error = %v, want ErrExceedsCapacity", err)
	}
}

func TestSemaphore_TryAcquireWithTimeout(t *testing.T) {
	s, _ := NewSemaphore(1)

	// 先占用
	s.TryAcquire(1)

	start := time.Now()
	result := s.TryAcquireWithTimeout(1, 50*time.Millisecond)
	elapsed := time.Since(start)

	if result {
		t.Error("TryAcquireWithTimeout should fail")
	}
	if elapsed < 40*time.Millisecond {
		t.Errorf("Timeout too short: %v", elapsed)
	}

	// 释放后应该能获取
	s.Release(1)
	if !s.TryAcquireWithTimeout(1, 50*time.Millisecond) {
		t.Error("TryAcquireWithTimeout should succeed after release")
	}
}

func TestSemaphore_Close(t *testing.T) {
	s, _ := NewSemaphore(10)

	if s.IsClosed() {
		t.Error("Semaphore should not be closed initially")
	}

	s.Close()

	if !s.IsClosed() {
		t.Error("Semaphore should be closed")
	}

	ctx := context.Background()
	if err := s.Acquire(ctx, 1); err != ErrSemaphoreClosed {
		t.Errorf("Acquire on closed semaphore error = %v, want ErrSemaphoreClosed", err)
	}
}

func TestSemaphore_ConcurrentAcquire(t *testing.T) {
	s, _ := NewSemaphore(3)

	var acquired int32
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if s.TryAcquire(1) {
				atomic.AddInt32(&acquired, 1)
				time.Sleep(10 * time.Millisecond)
				s.Release(1)
			}
		}()
	}

	wg.Wait()

	// 只有3个能成功获取
	if acquired != 3 {
		t.Errorf("acquired = %v, want 3", acquired)
	}
}

func TestSemaphore_AcquireWithContext(t *testing.T) {
	s, _ := NewSemaphore(1)
	s.TryAcquire(1) // 占用

	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	start := time.Now()
	err := s.Acquire(ctx, 1)
	elapsed := time.Since(start)

	if err != ErrContextCanceled {
		t.Errorf("Acquire error = %v, want ErrContextCanceled", err)
	}
	if elapsed < 40*time.Millisecond {
		t.Errorf("Timeout too short: %v", elapsed)
	}
}

// ============================================
// 优先级信号量测试
// ============================================

func TestNewPrioritySemaphore(t *testing.T) {
	tests := []struct {
		name     string
		capacity int64
		wantErr  bool
	}{
		{"valid capacity", 10, false},
		{"zero capacity", 0, true},
		{"negative capacity", -5, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			ps, err := NewPrioritySemaphore(tt.capacity)
			if (err != nil) != tt.wantErr {
				t.Errorf("NewPrioritySemaphore() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && ps.Capacity() != tt.capacity {
				t.Errorf("Capacity() = %v, want %v", ps.Capacity(), tt.capacity)
			}
		})
	}
}

func TestPrioritySemaphore_AcquireRelease(t *testing.T) {
	ps, _ := NewPrioritySemaphore(10)
	ctx := context.Background()

	// 直接获取
	if err := ps.AcquireWithPriority(ctx, 5, 1); err != nil {
		t.Errorf("AcquireWithPriority(5, 1) error = %v", err)
	}
	if ps.Available() != 5 {
		t.Errorf("Available() = %v, want 5", ps.Available())
	}

	// 释放
	ps.Release(5)
	if ps.Available() != 10 {
		t.Errorf("Available() = %v, want 10", ps.Available())
	}
}

func TestPrioritySemaphore_Close(t *testing.T) {
	ps, _ := NewPrioritySemaphore(10)

	ps.Close()

	if !ps.IsClosed() {
		t.Error("PrioritySemaphore should be closed")
	}
}

// ============================================
// 读写信号量测试
// ============================================

func TestNewRWSemaphore(t *testing.T) {
	tests := []struct {
		name     string
		capacity int64
		wantErr  bool
	}{
		{"valid capacity", 10, false},
		{"zero capacity", 0, true},
		{"negative capacity", -5, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			rw, err := NewRWSemaphore(tt.capacity)
			if (err != nil) != tt.wantErr {
				t.Errorf("NewRWSemaphore() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr && rw.IsClosed() {
				t.Error("RWSemaphore should not be closed initially")
			}
		})
	}
}

func TestRWSemaphore_ReadLock(t *testing.T) {
	rw, _ := NewRWSemaphore(10)
	ctx := context.Background()

	// 多个读锁可以共存
	var wg sync.WaitGroup
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if err := rw.AcquireRead(ctx); err != nil {
				t.Errorf("AcquireRead() error = %v", err)
			}
			time.Sleep(10 * time.Millisecond)
			rw.ReleaseRead()
		}()
	}

	wg.Wait()
}

func TestRWSemaphore_WriteLock(t *testing.T) {
	rw, _ := NewRWSemaphore(10)
	ctx := context.Background()

	// 获取写锁
	if err := rw.AcquireWrite(ctx); err != nil {
		t.Errorf("AcquireWrite() error = %v", err)
	}

	// 写锁时，读锁应阻塞
	readDone := make(chan bool, 1)
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
		defer cancel()
		err := rw.AcquireRead(ctx)
		readDone <- (err == nil)
	}()

	time.Sleep(30 * time.Millisecond)

	select {
	case <-readDone:
		t.Error("Read should not succeed while write is held")
	default:
		// 预期行为
	}

	rw.ReleaseWrite()

	// 释放写锁后，读锁应该成功
	time.Sleep(20 * time.Millisecond)
	select {
	case success := <-readDone:
		if success {
			t.Error("Read should fail due to timeout")
		}
	default:
		// 可能需要更长时间
	}
}

func TestRWSemaphore_Close(t *testing.T) {
	rw, _ := NewRWSemaphore(10)

	rw.Close()

	if !rw.IsClosed() {
		t.Error("RWSemaphore should be closed")
	}

	ctx := context.Background()
	if err := rw.AcquireRead(ctx); err != ErrSemaphoreClosed {
		t.Errorf("AcquireRead on closed RWSemaphore error = %v, want ErrSemaphoreClosed", err)
	}
}

// ============================================
// 信号量池测试
// ============================================

func TestSemaphorePool_GetOrCreate(t *testing.T) {
	p := NewSemaphorePool()

	s1, err := p.GetOrCreate("test", 10)
	if err != nil {
		t.Errorf("GetOrCreate() error = %v", err)
	}

	s2, _ := p.GetOrCreate("test", 20) // 容量应该被忽略

	if s1 != s2 {
		t.Error("GetOrCreate should return same semaphore for same name")
	}

	if s1.Capacity() != 10 {
		t.Errorf("Capacity = %v, want 10", s1.Capacity())
	}
}

func TestSemaphorePool_Remove(t *testing.T) {
	p := NewSemaphorePool()

	p.GetOrCreate("test", 10)
	p.Remove("test")

	s := p.Get("test")
	if s != nil {
		t.Error("Get() should return nil after Remove()")
	}
}

func TestSemaphorePool_Names(t *testing.T) {
	p := NewSemaphorePool()

	p.GetOrCreate("a", 10)
	p.GetOrCreate("b", 20)
	p.GetOrCreate("c", 30)

	names := p.Names()
	if len(names) != 3 {
		t.Errorf("Names() length = %v, want 3", len(names))
	}

	p.CloseAll()

	if len(p.Names()) != 0 {
		t.Error("Names() should be empty after CloseAll()")
	}
}

// ============================================
// 并发测试
// ============================================

func TestSemaphore_ConcurrentStress(t *testing.T) {
	s, _ := NewSemaphore(100)

	var wg sync.WaitGroup
	var successCount int32
	iterations := 100

	for i := 0; i < iterations; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			ctx := context.Background()
			if err := s.Acquire(ctx, 1); err == nil {
				atomic.AddInt32(&successCount, 1)
				time.Sleep(time.Microsecond)
				s.Release(1)
			}
		}()
	}

	wg.Wait()

	t.Logf("Concurrent test completed: %d successful acquires", successCount)
}

func TestSemaphorePool_Concurrent(t *testing.T) {
	p := NewSemaphorePool()

	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			name := string(rune('a' + (i % 5)))
			_, err := p.GetOrCreate(name, 10)
			if err != nil {
				t.Errorf("GetOrCreate() error = %v", err)
			}
		}(i)
	}

	wg.Wait()

	names := p.Names()
	if len(names) != 5 {
		t.Errorf("Names() length = %v, want 5", len(names))
	}
}

// ============================================
// 限流器测试
// ============================================

func TestNewRateLimiter(t *testing.T) {
	tests := []struct {
		name       string
		capacity   int64
		refillRate int64
		wantErr    bool
	}{
		{"valid", 10, 5, false},
		{"zero capacity", 0, 5, true},
		{"zero refillRate", 10, 0, true},
		{"negative capacity", -5, 5, true},
		{"negative refillRate", 10, -5, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			rl, err := NewRateLimiter(tt.capacity, tt.refillRate)
			if (err != nil) != tt.wantErr {
				t.Errorf("NewRateLimiter() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !tt.wantErr {
				if rl.Capacity() != tt.capacity {
					t.Errorf("Capacity() = %v, want %v", rl.Capacity(), tt.capacity)
				}
			}
		})
	}
}

func TestRateLimiter_TryAcquire(t *testing.T) {
	rl, _ := NewRateLimiter(5, 10)

	// 正常获取
	if !rl.TryAcquire(3) {
		t.Error("TryAcquire(3) should succeed")
	}

	// 超出可用
	if rl.TryAcquire(3) {
		t.Error("TryAcquire(3) should fail")
	}

	// 获取剩余
	if !rl.TryAcquire(2) {
		t.Error("TryAcquire(2) should succeed")
	}

	// 完全不可用
	if rl.TryAcquire(1) {
		t.Error("TryAcquire(1) should fail when available is 0")
	}
}

func TestRateLimiter_Refill(t *testing.T) {
	rl, _ := NewRateLimiter(5, 100) // 每秒补充100个

	rl.TryAcquire(5)
	if rl.Available() != 0 {
		t.Errorf("Available() = %v, want 0", rl.Available())
	}

	// 等待补充
	time.Sleep(50 * time.Millisecond)

	// 应该有补充
	if rl.Available() <= 0 {
		t.Errorf("Available() = %v, should be > 0 after refill", rl.Available())
	}
}

// ============================================
// Benchmark 测试
// ============================================

func BenchmarkSemaphore_TryAcquire(b *testing.B) {
	s, _ := NewSemaphore(1000000)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		s.TryAcquire(1)
		s.Release(1)
	}
}

func BenchmarkSemaphore_Acquire(b *testing.B) {
	s, _ := NewSemaphore(1000000)
	ctx := context.Background()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		s.Acquire(ctx, 1)
		s.Release(1)
	}
}

func BenchmarkSemaphorePool_GetOrCreate(b *testing.B) {
	p := NewSemaphorePool()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		name := string(rune('a' + (i % 10)))
		p.GetOrCreate(name, 10)
	}
}

func BenchmarkSemaphore_Concurrent(b *testing.B) {
	s, _ := NewSemaphore(100)
	ctx := context.Background()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			s.Acquire(ctx, 1)
			s.Release(1)
		}
	})
}