package pool_utils

import (
	"context"
	"net"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// TestObjectPool tests the generic object pool
func TestObjectPool(t *testing.T) {
	// Counter for tracking object creation
	var createdCount int64

	pool := NewObjectPool(
		func() *int {
			atomic.AddInt64(&createdCount, 1)
			v := 0
			return &v
		},
		func(obj *int) { *obj = 0 }, // Reset to 0
		2,  // min size
		10, // max size
	)

	// Test initial stats
	stats := pool.Stats()
	if stats.Created != 2 {
		t.Errorf("Expected 2 pre-created objects, got %d", stats.Created)
	}
	if stats.Idle != 2 {
		t.Errorf("Expected 2 idle objects, got %d", stats.Idle)
	}

	// Test get
	obj1, err := pool.Get()
	if err != nil {
		t.Fatalf("Failed to get object: %v", err)
	}
	if obj1 == nil {
		t.Fatal("Expected non-nil object")
	}
	*obj1 = 42 // Modify object

	stats = pool.Stats()
	if stats.Active != 1 {
		t.Errorf("Expected 1 active object, got %d", stats.Active)
	}
	if stats.Idle != 1 {
		t.Errorf("Expected 1 idle object, got %d", stats.Idle)
	}

	// Test put (should reset)
	err = pool.Put(obj1)
	if err != nil {
		t.Fatalf("Failed to put object: %v", err)
	}
	stats = pool.Stats()
	if stats.Active != 0 {
		t.Errorf("Expected 0 active objects after put, got %d", stats.Active)
	}

	// Get again - should be reset
	obj2, err := pool.Get()
	if err != nil {
		t.Fatalf("Failed to get object: %v", err)
	}
	if *obj2 != 0 {
		t.Errorf("Expected reset value 0, got %d", *obj2)
	}
	_ = pool.Put(obj2)

	// Test multiple gets beyond min size
	objs := make([]*int, 0)
	for i := 0; i < 5; i++ {
		obj, err := pool.Get()
		if err != nil {
			t.Fatalf("Failed to get object %d: %v", i, err)
		}
		objs = append(objs, obj)
	}

	stats = pool.Stats()
	if stats.Active != 5 {
		t.Errorf("Expected 5 active objects, got %d", stats.Active)
	}

	// Return all objects
	for _, obj := range objs {
		_ = pool.Put(obj)
	}

	// Close pool
	_ = pool.Close()

	// Test closed pool
	_, err = pool.Get()
	if err != ErrPoolClosed {
		t.Errorf("Expected ErrPoolClosed, got %v", err)
	}
}

// TestObjectPoolValidation tests object validation
func TestObjectPoolValidation(t *testing.T) {
	pool := NewObjectPool(
		func() *int { v := 1; return &v },
		nil,
		2,
		10,
	)

	var destroyedCount int64
	pool.SetValidate(func(obj *int) bool {
		return *obj > 0 // Only accept positive values
	})
	pool.SetDestroy(func(obj *int) {
		atomic.AddInt64(&destroyedCount, 1)
	})

	// Get object
	obj, _ := pool.Get()
	*obj = -1 // Make invalid
	_ = pool.Put(obj)

	// Get again - should create new since previous was invalid
	obj2, _ := pool.Get()
	if *obj2 <= 0 {
		t.Error("Expected new valid object")
	}
	_ = pool.Put(obj2)

	_ = pool.Close()

	// Should have destroyed at least 1 invalid object
	if destroyedCount < 1 {
		t.Error("Expected at least one destroyed object")
	}
}

// TestObjectPoolConcurrent tests concurrent access
func TestObjectPoolConcurrent(t *testing.T) {
	pool := NewObjectPool(
		func() *int { v := 0; return &v },
		func(obj *int) { *obj = 0 },
		5,
		100,
	)

	var wg sync.WaitGroup
	var successCount int64

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			obj, err := pool.Get()
			if err != nil {
				return
			}
			*obj++
			time.Sleep(time.Microsecond) // Simulate work
			_ = pool.Put(obj)
			atomic.AddInt64(&successCount, 1)
		}()
	}

	wg.Wait()
	_ = pool.Close()

	if successCount != 100 {
		t.Errorf("Expected 100 successful operations, got %d", successCount)
	}
}

// TestWorkerPool tests the worker pool
func TestWorkerPool(t *testing.T) {
	wp := NewWorkerPool(5)

	if err := wp.Start(); err != nil {
		t.Fatalf("Failed to start worker pool: %v", err)
	}

	var counter int64
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		err := wp.Submit(func() {
			atomic.AddInt64(&counter, 1)
			wg.Done()
		})
		if err != nil {
			t.Errorf("Failed to submit task: %v", err)
			wg.Done()
		}
	}

	wg.Wait()

	if counter != 100 {
		t.Errorf("Expected 100 task executions, got %d", counter)
	}

	wp.Stop()

	// Test double start
	wp2 := NewWorkerPool(2)
	_ = wp2.Start()
	if err := wp2.Start(); err == nil {
		t.Error("Expected error on double start")
	}
	wp2.Stop()

	// Test submit after stop
	if err := wp.Submit(func() {}); err == nil {
		t.Error("Expected error when submitting to stopped pool")
	}
}

// TestWorkerPoolContext tests worker pool with context
func TestWorkerPoolContext(t *testing.T) {
	wp := NewWorkerPool(2)
	_ = wp.Start()

	var executed int64
	var wg sync.WaitGroup

	// Submit some tasks
	for i := 0; i < 10; i++ {
		wg.Add(1)
		_ = wp.Submit(func() {
			time.Sleep(10 * time.Millisecond)
			atomic.AddInt64(&executed, 1)
			wg.Done()
		})
	}

	wg.Wait()
	wp.Stop()

	if executed != 10 {
		t.Errorf("Expected 10 executions, got %d", executed)
	}
}

// TestConnectionPool tests the connection pool
func TestConnectionPool(t *testing.T) {
	// Use a simple echo server for testing
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to create listener: %v", err)
	}
	defer listener.Close()

	var connCount int64
	var closeCount int64

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			atomic.AddInt64(&connCount, 1)
			go func(c net.Conn) {
				defer func() {
					c.Close()
					atomic.AddInt64(&closeCount, 1)
				}()
				buf := make([]byte, 1024)
				for {
					n, err := c.Read(buf)
					if err != nil {
						return
					}
					_, err = c.Write(buf[:n])
					if err != nil {
						return
					}
				}
			}(conn)
		}
	}()

	addr := listener.Addr().String()
	pool := NewConnectionPool(
		func() (net.Conn, error) {
			return net.Dial("tcp", addr)
		},
		2,                  // min conns
		10,                 // max conns
		5*time.Second,      // idle timeout
	)

	// Set callbacks
	var onCreateCount int64
	pool.SetOnCreate(func(net.Conn) {
		atomic.AddInt64(&onCreateCount, 1)
	})

	// Test get
	conn1, err := pool.Get()
	if err != nil {
		t.Fatalf("Failed to get connection: %v", err)
	}

	stats := pool.Stats()
	if stats.Active != 1 {
		t.Errorf("Expected 1 active connection, got %d", stats.Active)
	}

	// Test use connection
	_, err = conn1.Write([]byte("hello"))
	if err != nil {
		t.Fatalf("Failed to write: %v", err)
	}
	buf := make([]byte, 5)
	_, err = conn1.Read(buf)
	if err != nil {
		t.Fatalf("Failed to read: %v", err)
	}
	if string(buf) != "hello" {
		t.Errorf("Expected 'hello', got %s", string(buf))
	}

	// Return connection
	_ = conn1.Close()

	stats = pool.Stats()
	if stats.Active != 0 {
		t.Errorf("Expected 0 active connections after close, got %d", stats.Active)
	}

	// Test multiple connections
	conns := make([]net.Conn, 0)
	for i := 0; i < 5; i++ {
		conn, err := pool.Get()
		if err != nil {
			t.Fatalf("Failed to get connection %d: %v", i, err)
		}
		conns = append(conns, conn)
	}

	stats = pool.Stats()
	if stats.Active != 5 {
		t.Errorf("Expected 5 active connections, got %d", stats.Active)
	}

	// Return all connections
	for _, conn := range conns {
		_ = conn.Close()
	}

	_ = pool.Close()
}

// TestConnectionPoolHealthCheck tests connection health checks
func TestConnectionPoolHealthCheck(t *testing.T) {
	pool := NewConnectionPool(
		func() (net.Conn, error) {
			return nil, nil // Dummy connection
		},
		0,
		10,
		time.Second,
	)

	// This test is a basic check that the health check function can be set
	pool.SetHealthCheck(func(conn net.Conn) bool {
		return true
	})

	_ = pool.Close()
}

// TestSemaphorePool tests the semaphore pool
func TestSemaphorePool(t *testing.T) {
	sp := NewSemaphorePool(3)

	if sp.Capacity() != 3 {
		t.Errorf("Expected capacity 3, got %d", sp.Capacity())
	}
	if sp.Available() != 3 {
		t.Errorf("Expected 3 available, got %d", sp.Available())
	}

	// Acquire
	sp.Acquire()
	if sp.Available() != 2 {
		t.Errorf("Expected 2 available after acquire, got %d", sp.Available())
	}

	// TryAcquire
	if !sp.TryAcquire() {
		t.Error("Expected TryAcquire to succeed")
	}
	if sp.Available() != 1 {
		t.Errorf("Expected 1 available, got %d", sp.Available())
	}

	// Release
	sp.Release()
	if sp.Available() != 2 {
		t.Errorf("Expected 2 available after release, got %d", sp.Available())
	}

	// Acquire with context
	ctx := context.Background()
	if err := sp.AcquireWithContext(ctx); err != nil {
		t.Errorf("Unexpected error: %v", err)
	}

	sp.Release()
	sp.Release()
	sp.Release()
}

// TestSemaphorePoolContext tests semaphore with context cancellation
func TestSemaphorePoolContext(t *testing.T) {
	sp := NewSemaphorePool(1)

	sp.Acquire() // Fill the semaphore

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
	defer cancel()

	err := sp.AcquireWithContext(ctx)
	if err == nil {
		t.Error("Expected timeout error")
	}
	if err != context.DeadlineExceeded {
		t.Errorf("Expected context.DeadlineExceeded, got %v", err)
	}

	sp.Release()
}

// TestSemaphorePoolConcurrent tests concurrent semaphore usage
func TestSemaphorePoolConcurrent(t *testing.T) {
	sp := NewSemaphorePool(10)

	var counter int64
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			sp.Acquire()
			atomic.AddInt64(&counter, 1)
			time.Sleep(time.Millisecond)
			sp.Release()
		}()
	}

	wg.Wait()

	if counter != 100 {
		t.Errorf("Expected counter 100, got %d", counter)
	}
}

// BenchmarkObjectPool benchmarks object pool operations
func BenchmarkObjectPool(b *testing.B) {
	pool := NewObjectPool(
		func() *int { v := 0; return &v },
		func(obj *int) { *obj = 0 },
		100,
		1000,
	)

	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			obj, _ := pool.Get()
			_ = pool.Put(obj)
		}
	})
}

// BenchmarkWorkerPool benchmarks worker pool operations
func BenchmarkWorkerPool(b *testing.B) {
	wp := NewWorkerPool(10)
	_ = wp.Start()
	defer wp.Stop()

	var wg sync.WaitGroup

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wg.Add(1)
		_ = wp.Submit(func() {
			wg.Done()
		})
	}
	wg.Wait()
}

// BenchmarkSemaphorePool benchmarks semaphore operations
func BenchmarkSemaphorePool(b *testing.B) {
	sp := NewSemaphorePool(100)

	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			sp.Acquire()
			sp.Release()
		}
	})
}