// Package counter_utils provides thread-safe counter utilities for Go.
// It supports atomic operations, named counters, snapshots, and statistics.
package counter_utils

import (
	"sync"
	"sync/atomic"
	"time"
)

// Counter represents a single thread-safe counter with atomic operations.
type Counter struct {
	value int64
}

// NewCounter creates a new Counter initialized to zero.
func NewCounter() *Counter {
	return &Counter{value: 0}
}

// NewCounterWithValue creates a new Counter with an initial value.
func NewCounterWithValue(initial int64) *Counter {
	return &Counter{value: initial}
}

// Increment atomically increments the counter by 1 and returns the new value.
func (c *Counter) Increment() int64 {
	return atomic.AddInt64(&c.value, 1)
}

// IncrementBy atomically increments the counter by delta and returns the new value.
func (c *Counter) IncrementBy(delta int64) int64 {
	return atomic.AddInt64(&c.value, delta)
}

// Decrement atomically decrements the counter by 1 and returns the new value.
func (c *Counter) Decrement() int64 {
	return atomic.AddInt64(&c.value, -1)
}

// DecrementBy atomically decrements the counter by delta and returns the new value.
func (c *Counter) DecrementBy(delta int64) int64 {
	return atomic.AddInt64(&c.value, -delta)
}

// Get atomically returns the current value.
func (c *Counter) Get() int64 {
	return atomic.LoadInt64(&c.value)
}

// Set atomically sets the counter to a new value.
func (c *Counter) Set(newValue int64) {
	atomic.StoreInt64(&c.value, newValue)
}

// Reset atomically resets the counter to zero and returns the previous value.
func (c *Counter) Reset() int64 {
	return atomic.SwapInt64(&c.value, 0)
}

// CompareAndSwap atomically compares and swaps the value.
// Returns true if the swap was successful.
func (c *Counter) CompareAndSwap(oldValue, newValue int64) bool {
	return atomic.CompareAndSwapInt64(&c.value, oldValue, newValue)
}

// Snapshot represents a point-in-time capture of counter values.
type Snapshot struct {
	Timestamp time.Time
	Values    map[string]int64
}

// CounterManager manages multiple named counters with thread-safe operations.
type CounterManager struct {
	mu       sync.RWMutex
	counters map[string]*Counter
	history  []Snapshot
	maxHistory int
}

// NewCounterManager creates a new CounterManager.
func NewCounterManager() *CounterManager {
	return &CounterManager{
		counters:   make(map[string]*Counter),
		history:    make([]Snapshot, 0),
		maxHistory: 100,
	}
}

// NewCounterManagerWithHistory creates a new CounterManager with a custom max history size.
func NewCounterManagerWithHistory(maxHistory int) *CounterManager {
	return &CounterManager{
		counters:   make(map[string]*Counter),
		history:    make([]Snapshot, 0),
		maxHistory: maxHistory,
	}
}

// GetOrCreate gets an existing counter or creates a new one if it doesn't exist.
func (cm *CounterManager) GetOrCreate(name string) *Counter {
	cm.mu.RLock()
	counter, exists := cm.counters[name]
	cm.mu.RUnlock()

	if exists {
		return counter
	}

	cm.mu.Lock()
	defer cm.mu.Unlock()

	// Double-check after acquiring write lock
	if counter, exists := cm.counters[name]; exists {
		return counter
	}

	counter = NewCounter()
	cm.counters[name] = counter
	return counter
}

// Get returns a counter by name, or nil if it doesn't exist.
func (cm *CounterManager) Get(name string) *Counter {
	cm.mu.RLock()
	defer cm.mu.RUnlock()
	return cm.counters[name]
}

// Increment increments a named counter by 1.
// Creates the counter if it doesn't exist.
func (cm *CounterManager) Increment(name string) int64 {
	return cm.GetOrCreate(name).Increment()
}

// IncrementBy increments a named counter by delta.
// Creates the counter if it doesn't exist.
func (cm *CounterManager) IncrementBy(name string, delta int64) int64 {
	return cm.GetOrCreate(name).IncrementBy(delta)
}

// Decrement decrements a named counter by 1.
// Creates the counter if it doesn't exist.
func (cm *CounterManager) Decrement(name string) int64 {
	return cm.GetOrCreate(name).Decrement()
}

// DecrementBy decrements a named counter by delta.
// Creates the counter if it doesn't exist.
func (cm *CounterManager) DecrementBy(name string, delta int64) int64 {
	return cm.GetOrCreate(name).DecrementBy(delta)
}

// GetValue returns the value of a named counter.
// Returns 0 if the counter doesn't exist.
func (cm *CounterManager) GetValue(name string) int64 {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	if counter, exists := cm.counters[name]; exists {
		return counter.Get()
	}
	return 0
}

// SetValue sets a named counter to a specific value.
// Creates the counter if it doesn't exist.
func (cm *CounterManager) SetValue(name string, value int64) {
	cm.GetOrCreate(name).Set(value)
}

// Delete removes a counter by name.
// Returns true if the counter existed and was deleted.
func (cm *CounterManager) Delete(name string) bool {
	cm.mu.Lock()
	defer cm.mu.Unlock()

	if _, exists := cm.counters[name]; exists {
		delete(cm.counters, name)
		return true
	}
	return false
}

// Reset resets a named counter to zero.
// Returns the previous value, or 0 if counter doesn't exist.
func (cm *CounterManager) Reset(name string) int64 {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	if counter, exists := cm.counters[name]; exists {
		return counter.Reset()
	}
	return 0
}

// ResetAll resets all counters to zero.
func (cm *CounterManager) ResetAll() {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	for _, counter := range cm.counters {
		counter.Reset()
	}
}

// Names returns all counter names.
func (cm *CounterManager) Names() []string {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	names := make([]string, 0, len(cm.counters))
	for name := range cm.counters {
		names = append(names, name)
	}
	return names
}

// Count returns the number of counters.
func (cm *CounterManager) Count() int {
	cm.mu.RLock()
	defer cm.mu.RUnlock()
	return len(cm.counters)
}

// GetAll returns a map of all counter names to their current values.
func (cm *CounterManager) GetAll() map[string]int64 {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	result := make(map[string]int64, len(cm.counters))
	for name, counter := range cm.counters {
		result[name] = counter.Get()
	}
	return result
}

// TakeSnapshot captures the current state of all counters.
func (cm *CounterManager) TakeSnapshot() Snapshot {
	cm.mu.RLock()
	values := make(map[string]int64, len(cm.counters))
	for name, counter := range cm.counters {
		values[name] = counter.Get()
	}
	cm.mu.RUnlock()

	snapshot := Snapshot{
		Timestamp: time.Now(),
		Values:    values,
	}

	cm.mu.Lock()
	cm.history = append(cm.history, snapshot)
	if len(cm.history) > cm.maxHistory {
		cm.history = cm.history[1:]
	}
	cm.mu.Unlock()

	return snapshot
}

// GetHistory returns all stored snapshots.
func (cm *CounterManager) GetHistory() []Snapshot {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	result := make([]Snapshot, len(cm.history))
	copy(result, cm.history)
	return result
}

// ClearHistory clears all stored snapshots.
func (cm *CounterManager) ClearHistory() {
	cm.mu.Lock()
	defer cm.mu.Unlock()
	cm.history = make([]Snapshot, 0)
}

// Stats holds statistics about a counter.
type Stats struct {
	Name      string
	Value     int64
	Min       int64
	Max       int64
	Avg       float64
	Count     int64
	UpdatedAt time.Time
}

// StatsCollector collects statistics for a counter over time.
type StatsCollector struct {
	mu     sync.RWMutex
	stats  map[string]*Stats
	values map[string][]int64
	maxValues int
}

// NewStatsCollector creates a new StatsCollector.
func NewStatsCollector() *StatsCollector {
	return &StatsCollector{
		stats:     make(map[string]*Stats),
		values:    make(map[string][]int64),
		maxValues: 1000,
	}
}

// Record records a value for a named counter and updates statistics.
func (sc *StatsCollector) Record(name string, value int64) {
	sc.mu.Lock()
	defer sc.mu.Unlock()

	// Store value
	sc.values[name] = append(sc.values[name], value)
	if len(sc.values[name]) > sc.maxValues {
		sc.values[name] = sc.values[name][1:]
	}

	// Update stats
	stats, exists := sc.stats[name]
	if !exists {
		stats = &Stats{
			Name:  name,
			Min:   value,
			Max:   value,
			Count: 0,
		}
		sc.stats[name] = stats
	}

	stats.Value = value
	stats.UpdatedAt = time.Now()
	stats.Count++

	if value < stats.Min {
		stats.Min = value
	}
	if value > stats.Max {
		stats.Max = value
	}

	// Calculate average
	var sum int64
	for _, v := range sc.values[name] {
		sum += v
	}
	stats.Avg = float64(sum) / float64(len(sc.values[name]))
}

// GetStats returns statistics for a named counter.
func (sc *StatsCollector) GetStats(name string) *Stats {
	sc.mu.RLock()
	defer sc.mu.RUnlock()

	if stats, exists := sc.stats[name]; exists {
		// Return a copy
		copy := *stats
		return &copy
	}
	return nil
}

// GetAllStats returns statistics for all counters.
func (sc *StatsCollector) GetAllStats() map[string]*Stats {
	sc.mu.RLock()
	defer sc.mu.RUnlock()

	result := make(map[string]*Stats, len(sc.stats))
	for name, stats := range sc.stats {
		copy := *stats
		result[name] = &copy
	}
	return result
}

// ResetStats resets statistics for a named counter.
func (sc *StatsCollector) ResetStats(name string) {
	sc.mu.Lock()
	defer sc.mu.Unlock()

	delete(sc.stats, name)
	delete(sc.values, name)
}

// ResetAllStats resets all statistics.
func (sc *StatsCollector) ResetAllStats() {
	sc.mu.Lock()
	defer sc.mu.Unlock()

	sc.stats = make(map[string]*Stats)
	sc.values = make(map[string][]int64)
}

// RateCounter measures the rate of events over time.
type RateCounter struct {
	mu         sync.RWMutex
	events     []time.Time
	windowSize time.Duration
}

// NewRateCounter creates a new RateCounter with a specified time window.
func NewRateCounter(windowSize time.Duration) *RateCounter {
	return &RateCounter{
		events:     make([]time.Time, 0),
		windowSize: windowSize,
	}
}

// Record records an event at the current time.
func (rc *RateCounter) Record() {
	rc.RecordAt(time.Now())
}

// RecordAt records an event at a specific time.
func (rc *RateCounter) RecordAt(t time.Time) {
	rc.mu.Lock()
	defer rc.mu.Unlock()

	rc.events = append(rc.events, t)
	rc.cleanup(t)
}

// cleanup removes events outside the time window.
func (rc *RateCounter) cleanup(now time.Time) {
	cutoff := now.Add(-rc.windowSize)
	
	// Find first event within window
	idx := 0
	for i, t := range rc.events {
		if t.After(cutoff) || t.Equal(cutoff) {
			idx = i
			break
		}
		idx = i + 1
	}

	if idx > 0 {
		rc.events = rc.events[idx:]
	}
}

// Count returns the number of events in the current window.
func (rc *RateCounter) Count() int {
	rc.mu.Lock()
	defer rc.mu.Unlock()

	rc.cleanup(time.Now())
	return len(rc.events)
}

// Rate returns the events per second over the window.
func (rc *RateCounter) Rate() float64 {
	rc.mu.Lock()
	defer rc.mu.Unlock()

	now := time.Now()
	rc.cleanup(now)

	if len(rc.events) == 0 {
		return 0
	}

	windowSeconds := rc.windowSize.Seconds()
	return float64(len(rc.events)) / windowSeconds
}

// Reset clears all recorded events.
func (rc *RateCounter) Reset() {
	rc.mu.Lock()
	defer rc.mu.Unlock()
	rc.events = make([]time.Time, 0)
}

// BucketCounter maintains counts in fixed-size time buckets.
type BucketCounter struct {
	mu          sync.RWMutex
	buckets     []int64
	bucketSize  time.Duration
	startTime   time.Time
	numBuckets  int
}

// NewBucketCounter creates a new BucketCounter.
func NewBucketCounter(bucketSize time.Duration, numBuckets int) *BucketCounter {
	return &BucketCounter{
		buckets:    make([]int64, numBuckets),
		bucketSize: bucketSize,
		startTime:  time.Now(),
		numBuckets: numBuckets,
	}
}

// currentBucket returns the current bucket index.
func (bc *BucketCounter) currentBucket() int {
	elapsed := time.Since(bc.startTime)
	return int(elapsed / bc.bucketSize) % bc.numBuckets
}

// Increment increments the current bucket by 1.
func (bc *BucketCounter) Increment() {
	bc.IncrementBy(1)
}

// IncrementBy increments the current bucket by delta.
func (bc *BucketCounter) IncrementBy(delta int64) {
	bc.mu.Lock()
	defer bc.mu.Unlock()
	bc.buckets[bc.currentBucket()] += delta
}

// GetBucket returns the value of a specific bucket.
func (bc *BucketCounter) GetBucket(idx int) int64 {
	bc.mu.RLock()
	defer bc.mu.RUnlock()

	if idx < 0 || idx >= bc.numBuckets {
		return 0
	}
	return bc.buckets[idx]
}

// GetAllBuckets returns all bucket values.
func (bc *BucketCounter) GetAllBuckets() []int64 {
	bc.mu.RLock()
	defer bc.mu.RUnlock()

	result := make([]int64, bc.numBuckets)
	copy(result, bc.buckets)
	return result
}

// Total returns the sum of all buckets.
func (bc *BucketCounter) Total() int64 {
	bc.mu.RLock()
	defer bc.mu.RUnlock()

	var total int64
	for _, v := range bc.buckets {
		total += v
	}
	return total
}

// Reset clears all buckets.
func (bc *BucketCounter) Reset() {
	bc.mu.Lock()
	defer bc.mu.Unlock()

	for i := range bc.buckets {
		bc.buckets[i] = 0
	}
	bc.startTime = time.Now()
}