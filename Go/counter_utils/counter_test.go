package counter_utils

import (
	"sync"
	"testing"
	"time"
)

// Counter Tests

func TestNewCounter(t *testing.T) {
	c := NewCounter()
	if c.Get() != 0 {
		t.Errorf("Expected 0, got %d", c.Get())
	}
}

func TestNewCounterWithValue(t *testing.T) {
	c := NewCounterWithValue(100)
	if c.Get() != 100 {
		t.Errorf("Expected 100, got %d", c.Get())
	}
}

func TestCounterIncrement(t *testing.T) {
	c := NewCounter()
	
	for i := 1; i <= 5; i++ {
		result := c.Increment()
		if result != int64(i) {
			t.Errorf("Expected %d, got %d", i, result)
		}
	}
}

func TestCounterIncrementBy(t *testing.T) {
	c := NewCounter()
	
	result := c.IncrementBy(10)
	if result != 10 {
		t.Errorf("Expected 10, got %d", result)
	}
	
	result = c.IncrementBy(-5)
	if result != 5 {
		t.Errorf("Expected 5, got %d", result)
	}
}

func TestCounterDecrement(t *testing.T) {
	c := NewCounterWithValue(10)
	
	for i := 9; i >= 5; i-- {
		result := c.Decrement()
		if result != int64(i) {
			t.Errorf("Expected %d, got %d", i, result)
		}
	}
}

func TestCounterDecrementBy(t *testing.T) {
	c := NewCounterWithValue(20)
	
	result := c.DecrementBy(5)
	if result != 15 {
		t.Errorf("Expected 15, got %d", result)
	}
}

func TestCounterSet(t *testing.T) {
	c := NewCounter()
	c.Set(42)
	
	if c.Get() != 42 {
		t.Errorf("Expected 42, got %d", c.Get())
	}
}

func TestCounterReset(t *testing.T) {
	c := NewCounterWithValue(100)
	prev := c.Reset()
	
	if prev != 100 {
		t.Errorf("Expected previous value 100, got %d", prev)
	}
	if c.Get() != 0 {
		t.Errorf("Expected 0 after reset, got %d", c.Get())
	}
}

func TestCounterCompareAndSwap(t *testing.T) {
	c := NewCounterWithValue(10)
	
	// Successful swap
	if !c.CompareAndSwap(10, 20) {
		t.Error("Expected CAS to succeed")
	}
	if c.Get() != 20 {
		t.Errorf("Expected 20, got %d", c.Get())
	}
	
	// Failed swap
	if c.CompareAndSwap(10, 30) {
		t.Error("Expected CAS to fail")
	}
	if c.Get() != 20 {
		t.Errorf("Expected 20, got %d", c.Get())
	}
}

func TestCounterConcurrent(t *testing.T) {
	c := NewCounter()
	var wg sync.WaitGroup
	
	numGoroutines := 20
	incrementsPerGoroutine := 1000
	
	wg.Add(numGoroutines)
	for i := 0; i < numGoroutines; i++ {
		go func() {
			defer wg.Done()
			for j := 0; j < incrementsPerGoroutine; j++ {
				c.Increment()
			}
		}()
	}
	
	wg.Wait()
	
	expected := int64(numGoroutines * incrementsPerGoroutine)
	if c.Get() != expected {
		t.Errorf("Expected %d, got %d", expected, c.Get())
	}
}

// CounterManager Tests

func TestCounterManagerGetOrCreate(t *testing.T) {
	cm := NewCounterManager()
	
	c1 := cm.GetOrCreate("test")
	c1.Increment()
	
	c2 := cm.GetOrCreate("test")
	
	if c1 != c2 {
		t.Error("Expected same counter instance")
	}
	if c2.Get() != 1 {
		t.Errorf("Expected 1, got %d", c2.Get())
	}
}

func TestCounterManagerGet(t *testing.T) {
	cm := NewCounterManager()
	
	// Non-existent counter
	if cm.Get("nonexistent") != nil {
		t.Error("Expected nil for non-existent counter")
	}
	
	// Existing counter
	cm.Increment("test")
	if cm.Get("test") == nil {
		t.Error("Expected counter, got nil")
	}
}

func TestCounterManagerIncrement(t *testing.T) {
	cm := NewCounterManager()
	
	cm.Increment("requests")
	cm.Increment("requests")
	cm.Increment("requests")
	
	if cm.GetValue("requests") != 3 {
		t.Errorf("Expected 3, got %d", cm.GetValue("requests"))
	}
}

func TestCounterManagerIncrementBy(t *testing.T) {
	cm := NewCounterManager()
	
	cm.IncrementBy("bytes", 100)
	cm.IncrementBy("bytes", 50)
	
	if cm.GetValue("bytes") != 150 {
		t.Errorf("Expected 150, got %d", cm.GetValue("bytes"))
	}
}

func TestCounterManagerDecrement(t *testing.T) {
	cm := NewCounterManager()
	
	cm.SetValue("available", 10)
	cm.Decrement("available")
	cm.Decrement("available")
	
	if cm.GetValue("available") != 8 {
		t.Errorf("Expected 8, got %d", cm.GetValue("available"))
	}
}

func TestCounterManagerDecrementBy(t *testing.T) {
	cm := NewCounterManager()
	
	cm.SetValue("stock", 100)
	cm.DecrementBy("stock", 30)
	
	if cm.GetValue("stock") != 70 {
		t.Errorf("Expected 70, got %d", cm.GetValue("stock"))
	}
}

func TestCounterManagerDelete(t *testing.T) {
	cm := NewCounterManager()
	
	cm.Increment("test")
	
	if !cm.Delete("test") {
		t.Error("Expected true when deleting existing counter")
	}
	
	if cm.Delete("test") {
		t.Error("Expected false when deleting non-existent counter")
	}
	
	if cm.GetValue("test") != 0 {
		t.Error("Expected 0 for deleted counter")
	}
}

func TestCounterManagerReset(t *testing.T) {
	cm := NewCounterManager()
	
	cm.IncrementBy("counter", 100)
	prev := cm.Reset("counter")
	
	if prev != 100 {
		t.Errorf("Expected previous value 100, got %d", prev)
	}
	if cm.GetValue("counter") != 0 {
		t.Errorf("Expected 0 after reset, got %d", cm.GetValue("counter"))
	}
}

func TestCounterManagerResetAll(t *testing.T) {
	cm := NewCounterManager()
	
	cm.IncrementBy("a", 10)
	cm.IncrementBy("b", 20)
	cm.IncrementBy("c", 30)
	
	cm.ResetAll()
	
	all := cm.GetAll()
	for name, value := range all {
		if value != 0 {
			t.Errorf("Expected 0 for %s, got %d", name, value)
		}
	}
}

func TestCounterManagerNames(t *testing.T) {
	cm := NewCounterManager()
	
	cm.Increment("alpha")
	cm.Increment("beta")
	cm.Increment("gamma")
	
	names := cm.Names()
	if len(names) != 3 {
		t.Errorf("Expected 3 names, got %d", len(names))
	}
}

func TestCounterManagerCount(t *testing.T) {
	cm := NewCounterManager()
	
	if cm.Count() != 0 {
		t.Errorf("Expected 0 counters, got %d", cm.Count())
	}
	
	cm.Increment("a")
	cm.Increment("b")
	
	if cm.Count() != 2 {
		t.Errorf("Expected 2 counters, got %d", cm.Count())
	}
}

func TestCounterManagerGetAll(t *testing.T) {
	cm := NewCounterManager()
	
	cm.IncrementBy("x", 10)
	cm.IncrementBy("y", 20)
	
	all := cm.GetAll()
	
	if all["x"] != 10 {
		t.Errorf("Expected x=10, got %d", all["x"])
	}
	if all["y"] != 20 {
		t.Errorf("Expected y=20, got %d", all["y"])
	}
}

func TestCounterManagerSnapshot(t *testing.T) {
	cm := NewCounterManager()
	
	cm.IncrementBy("requests", 100)
	cm.IncrementBy("errors", 5)
	
	snapshot := cm.TakeSnapshot()
	
	if snapshot.Values["requests"] != 100 {
		t.Errorf("Expected requests=100, got %d", snapshot.Values["requests"])
	}
	if snapshot.Values["errors"] != 5 {
		t.Errorf("Expected errors=5, got %d", snapshot.Values["errors"])
	}
	
	// Modify counter after snapshot
	cm.Increment("requests")
	
	// Snapshot should still have old value
	if snapshot.Values["requests"] != 100 {
		t.Error("Snapshot should be immutable")
	}
}

func TestCounterManagerHistory(t *testing.T) {
	cm := NewCounterManagerWithHistory(10)
	
	// Take multiple snapshots
	for i := 0; i < 5; i++ {
		cm.Increment("counter")
		cm.TakeSnapshot()
	}
	
	history := cm.GetHistory()
	if len(history) != 5 {
		t.Errorf("Expected 5 snapshots, got %d", len(history))
	}
	
	// Verify values progress
	for i, snap := range history {
		expected := int64(i + 1)
		if snap.Values["counter"] != expected {
			t.Errorf("Snapshot %d: expected %d, got %d", i, expected, snap.Values["counter"])
		}
	}
}

func TestCounterManagerHistoryLimit(t *testing.T) {
	cm := NewCounterManagerWithHistory(3)
	
	// Take more snapshots than max history
	for i := 0; i < 10; i++ {
		cm.Increment("counter")
		cm.TakeSnapshot()
	}
	
	history := cm.GetHistory()
	if len(history) != 3 {
		t.Errorf("Expected 3 snapshots (max history), got %d", len(history))
	}
}

func TestCounterManagerClearHistory(t *testing.T) {
	cm := NewCounterManager()
	
	cm.Increment("test")
	cm.TakeSnapshot()
	cm.TakeSnapshot()
	
	cm.ClearHistory()
	
	history := cm.GetHistory()
	if len(history) != 0 {
		t.Errorf("Expected 0 snapshots, got %d", len(history))
	}
}

func TestCounterManagerConcurrent(t *testing.T) {
	cm := NewCounterManager()
	var wg sync.WaitGroup
	
	numGoroutines := 20
	operationsPerGoroutine := 100
	
	// Concurrent increments
	wg.Add(numGoroutines)
	for i := 0; i < numGoroutines; i++ {
		go func() {
			defer wg.Done()
			for j := 0; j < operationsPerGoroutine; j++ {
				cm.Increment("shared")
			}
		}()
	}
	
	wg.Wait()
	
	expected := int64(numGoroutines * operationsPerGoroutine)
	if cm.GetValue("shared") != expected {
		t.Errorf("Expected %d, got %d", expected, cm.GetValue("shared"))
	}
}

// StatsCollector Tests

func TestStatsCollectorRecord(t *testing.T) {
	sc := NewStatsCollector()
	
	sc.Record("temperature", 20)
	sc.Record("temperature", 25)
	sc.Record("temperature", 30)
	
	stats := sc.GetStats("temperature")
	if stats == nil {
		t.Fatal("Expected stats, got nil")
	}
	
	if stats.Min != 20 {
		t.Errorf("Expected min 20, got %d", stats.Min)
	}
	if stats.Max != 30 {
		t.Errorf("Expected max 30, got %d", stats.Max)
	}
	if stats.Count != 3 {
		t.Errorf("Expected count 3, got %d", stats.Count)
	}
}

func TestStatsCollectorAverage(t *testing.T) {
	sc := NewStatsCollector()
	
	sc.Record("values", 10)
	sc.Record("values", 20)
	sc.Record("values", 30)
	
	stats := sc.GetStats("values")
	expected := 20.0
	
	if stats.Avg != expected {
		t.Errorf("Expected avg %f, got %f", expected, stats.Avg)
	}
}

func TestStatsCollectorGetAllStats(t *testing.T) {
	sc := NewStatsCollector()
	
	sc.Record("a", 1)
	sc.Record("b", 2)
	sc.Record("c", 3)
	
	allStats := sc.GetAllStats()
	
	if len(allStats) != 3 {
		t.Errorf("Expected 3 stats, got %d", len(allStats))
	}
}

func TestStatsCollectorResetStats(t *testing.T) {
	sc := NewStatsCollector()
	
	sc.Record("test", 100)
	sc.ResetStats("test")
	
	stats := sc.GetStats("test")
	if stats != nil {
		t.Errorf("Expected nil after reset, got %+v", stats)
	}
}

func TestStatsCollectorResetAllStats(t *testing.T) {
	sc := NewStatsCollector()
	
	sc.Record("a", 1)
	sc.Record("b", 2)
	
	sc.ResetAllStats()
	
	allStats := sc.GetAllStats()
	if len(allStats) != 0 {
		t.Errorf("Expected 0 stats, got %d", len(allStats))
	}
}

// RateCounter Tests

func TestRateCounterRecord(t *testing.T) {
	rc := NewRateCounter(time.Minute)
	
	for i := 0; i < 10; i++ {
		rc.Record()
	}
	
	if rc.Count() != 10 {
		t.Errorf("Expected 10 events, got %d", rc.Count())
	}
}

func TestRateCounterRate(t *testing.T) {
	rc := NewRateCounter(time.Second)
	
	// Record 10 events
	for i := 0; i < 10; i++ {
		rc.Record()
	}
	
	// Rate should be approximately 10 events per second
	rate := rc.Rate()
	if rate < 9.0 || rate > 100.0 {
		t.Errorf("Expected rate around 10-100, got %f", rate)
	}
}

func TestRateCounterReset(t *testing.T) {
	rc := NewRateCounter(time.Minute)
	
	for i := 0; i < 5; i++ {
		rc.Record()
	}
	
	rc.Reset()
	
	if rc.Count() != 0 {
		t.Errorf("Expected 0 events after reset, got %d", rc.Count())
	}
}

func TestRateCounterWindowExpiry(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping in short mode")
	}
	
	rc := NewRateCounter(50 * time.Millisecond)
	
	// Record events
	for i := 0; i < 5; i++ {
		rc.Record()
	}
	
	// Wait for window to expire
	time.Sleep(100 * time.Millisecond)
	
	// Old events should be expired
	if rc.Count() != 0 {
		t.Errorf("Expected 0 events after window expiry, got %d", rc.Count())
	}
}

// BucketCounter Tests

func TestBucketCounterIncrement(t *testing.T) {
	bc := NewBucketCounter(time.Second, 10)
	
	for i := 0; i < 5; i++ {
		bc.Increment()
	}
	
	// Total should be 5
	if bc.Total() != 5 {
		t.Errorf("Expected total 5, got %d", bc.Total())
	}
}

func TestBucketCounterIncrementBy(t *testing.T) {
	bc := NewBucketCounter(time.Second, 10)
	
	bc.IncrementBy(10)
	bc.IncrementBy(20)
	
	if bc.Total() != 30 {
		t.Errorf("Expected total 30, got %d", bc.Total())
	}
}

func TestBucketCounterGetBucket(t *testing.T) {
	bc := NewBucketCounter(time.Second, 10)
	
	bc.IncrementBy(42)
	
	// Current bucket should have 42
	currentIdx := 0 // First bucket after creation
	if bc.GetBucket(currentIdx) != 42 {
		t.Errorf("Expected bucket value 42, got %d", bc.GetBucket(currentIdx))
	}
	
	// Invalid bucket should return 0
	if bc.GetBucket(-1) != 0 {
		t.Error("Expected 0 for invalid bucket index")
	}
	if bc.GetBucket(100) != 0 {
		t.Error("Expected 0 for invalid bucket index")
	}
}

func TestBucketCounterGetAllBuckets(t *testing.T) {
	bc := NewBucketCounter(time.Second, 5)
	
	bc.IncrementBy(10)
	
	buckets := bc.GetAllBuckets()
	
	if len(buckets) != 5 {
		t.Errorf("Expected 5 buckets, got %d", len(buckets))
	}
}

func TestBucketCounterReset(t *testing.T) {
	bc := NewBucketCounter(time.Second, 10)
	
	bc.IncrementBy(100)
	bc.Reset()
	
	if bc.Total() != 0 {
		t.Errorf("Expected total 0 after reset, got %d", bc.Total())
	}
}

func TestBucketCounterConcurrent(t *testing.T) {
	bc := NewBucketCounter(time.Second, 10)
	var wg sync.WaitGroup
	
	numGoroutines := 20
	incrementsPerGoroutine := 100
	
	wg.Add(numGoroutines)
	for i := 0; i < numGoroutines; i++ {
		go func() {
			defer wg.Done()
			for j := 0; j < incrementsPerGoroutine; j++ {
				bc.Increment()
			}
		}()
	}
	
	wg.Wait()
	
	expected := int64(numGoroutines * incrementsPerGoroutine)
	if bc.Total() != expected {
		t.Errorf("Expected total %d, got %d", expected, bc.Total())
	}
}