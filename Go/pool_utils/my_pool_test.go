package pool_utils

import (
	"bytes"
	"sync"
	"testing"
	"time"
)

func TestNewPool(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 0)

	if pool == nil {
		t.Fatal("expected non-nil pool")
	}
	if pool.maxSize != 10 {
		t.Errorf("expected maxSize 10, got %d", pool.maxSize)
	}
}

func TestPoolGetPut(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 0)

	obj := pool.Get()
	if obj == nil {
		t.Fatal("expected non-nil object from Get")
	}

	pool.Put(obj)

	avail, active, created := pool.Stats()
	if avail != 1 {
		t.Errorf("expected 1 available, got %d", avail)
	}
	if active != 0 {
		t.Errorf("expected 0 active, got %d", active)
	}
	if created != 1 {
		t.Errorf("expected 1 created, got %d", created)
	}
}

func TestPoolReuse(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 0)

	obj1 := pool.Get()
	buf1 := obj1.(*bytes.Buffer)
	buf1.WriteString("test")

	pool.Put(obj1)

	obj2 := pool.Get()
	buf2 := obj2.(*bytes.Buffer)

	// Should be the same buffer reused
	if buf2 != buf1 {
		t.Error("expected reused buffer")
	}
	// Note: buffer content is not cleared; caller should reset
}

func TestPoolCapacity(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 2, 0)

	obj1 := pool.Get()
	pool.Put(obj1)

	obj2 := pool.Get()
	// Pool has max size 2, we put one back, get another
	// active count is 1 at this point

	_, active, created := pool.Stats()
	if created != 2 {
		t.Errorf("expected 2 created, got %d", created)
	}
	if active != 1 {
		t.Errorf("expected 1 active, got %d", active)
	}

	pool.Put(obj2)
}

func TestPoolOverCapacity(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 2, 0)

	// Fill the pool
	obj1 := pool.Get()
	obj2 := pool.Get()
	pool.Put(obj1)
	pool.Put(obj2)

	// Get both back - pool at capacity
	obj3 := pool.Get()
	obj4 := pool.Get()

	_, _, created := pool.Stats()
	if created != 2 {
		t.Errorf("expected 2 created (factory called once over capacity), got %d", created)
	}

	pool.Put(obj3)
	pool.Put(obj4)
}

func TestPoolClose(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 0)

	obj := pool.Get()
	pool.Put(obj)

	pool.Close()

	avail, active, created := pool.Stats()
	if avail != 0 {
		t.Errorf("expected 0 available after Close, got %d", avail)
	}
	if active != 0 {
		t.Errorf("expected 0 active after Close, got %d", active)
	}
	if created != 0 {
		t.Errorf("expected 0 created after Close, got %d", created)
	}
}

func TestPoolConcurrent(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 100, 0)

	var wg sync.WaitGroup
	for i := 0; i < 50; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			obj := pool.Get()
			time.Sleep(time.Microsecond * 100)
			pool.Put(obj)
		}()
	}
	wg.Wait()

	avail, active, created := pool.Stats()
	if avail < 0 {
		t.Errorf("available should not be negative, got %d", avail)
	}
	if active < 0 {
		t.Errorf("active should not be negative, got %d", active)
	}
	if created < 0 {
		t.Errorf("created should not be negative, got %d", created)
	}
}

func TestPoolTTL(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 50*time.Millisecond)

	obj := pool.Get()
	pool.Put(obj)

	time.Sleep(80 * time.Millisecond)

	pool.Purge()

	avail, _, _ := pool.Stats()
	if avail != 0 {
		t.Errorf("expected 0 available after TTL purge, got %d", avail)
	}
}

func TestPoolPurge(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 20*time.Millisecond)

	for i := 0; i < 5; i++ {
		obj := pool.Get()
		pool.Put(obj)
	}

	time.Sleep(30 * time.Millisecond)
	pool.Purge()

	avail, _, _ := pool.Stats()
	if avail != 0 {
		t.Errorf("expected 0 available after purge, got %d", avail)
	}
}

func TestPoolStats(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 0)

	avail, active, created := pool.Stats()
	if avail != 0 {
		t.Errorf("expected 0 initial available, got %d", avail)
	}
	if active != 0 {
		t.Errorf("expected 0 initial active, got %d", active)
	}
	if created != 0 {
		t.Errorf("expected 0 initial created, got %d", created)
	}
}

func TestPoolResetStats(t *testing.T) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 10, 0)

	obj := pool.Get()
	pool.Put(obj)

	pool.ResetStats()

	_, _, created := pool.Stats()
	if created != 0 {
		t.Errorf("expected 0 after ResetStats, got %d", created)
	}
}

func BenchmarkPoolGetPut(b *testing.B) {
	factory := func() interface{} { return &bytes.Buffer{} }
	pool := New(factory, 1000, 0)

	obj := pool.Get()
	pool.Put(obj)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		obj := pool.Get()
		pool.Put(obj)
	}
}
