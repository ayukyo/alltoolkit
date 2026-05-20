// Package rolling_window_utils provides sliding window data structures and statistics utilities.
// It implements a fixed-size rolling window that maintains the last N values and provides
// efficient statistical calculations like moving average, sum, min, max, and more.
package rolling_window_utils

import (
	"math"
	"sync"
)

// RollingWindow represents a fixed-size sliding window that stores numeric values.
// It provides O(1) insert operations and O(1) amortized statistics calculations.
type RollingWindow struct {
	data     []float64
	size     int
	count    int
	head     int
	sum      float64
	minQueue []int // Monotonic queue for O(1) min
	maxQueue []int // Monotonic queue for O(1) max
	mu       sync.RWMutex
}

// NewRollingWindow creates a new RollingWindow with the specified size.
// Size must be at least 1.
func NewRollingWindow(size int) *RollingWindow {
	if size < 1 {
		size = 1
	}
	return &RollingWindow{
		data:     make([]float64, size),
		size:     size,
		minQueue: make([]int, 0, size),
		maxQueue: make([]int, 0, size),
	}
}

// Add inserts a new value into the window, removing the oldest if full.
// This operation is O(1).
func (rw *RollingWindow) Add(value float64) {
	rw.mu.Lock()
	defer rw.mu.Unlock()

	// Remove oldest value from sum if window is full
	if rw.count == rw.size {
		rw.sum -= rw.data[rw.head]
		// Remove from monotonic queues if oldest element is at front
		if len(rw.minQueue) > 0 && rw.minQueue[0] == rw.head {
			rw.minQueue = rw.minQueue[1:]
		}
		if len(rw.maxQueue) > 0 && rw.maxQueue[0] == rw.head {
			rw.maxQueue = rw.maxQueue[1:]
		}
	} else {
		rw.count++
	}

	// Add new value
	rw.sum += value
	idx := rw.head
	rw.data[rw.head] = value
	rw.head = (rw.head + 1) % rw.size

	// Update monotonic queue for minimum
	for len(rw.minQueue) > 0 && rw.data[rw.minQueue[len(rw.minQueue)-1]] >= value {
		rw.minQueue = rw.minQueue[:len(rw.minQueue)-1]
	}
	rw.minQueue = append(rw.minQueue, idx)

	// Update monotonic queue for maximum
	for len(rw.maxQueue) > 0 && rw.data[rw.maxQueue[len(rw.maxQueue)-1]] <= value {
		rw.maxQueue = rw.maxQueue[:len(rw.maxQueue)-1]
	}
	rw.maxQueue = append(rw.maxQueue, idx)
}

// Values returns all values in the window in insertion order.
func (rw *RollingWindow) Values() []float64 {
	rw.mu.RLock()
	defer rw.mu.RUnlock()

	result := make([]float64, rw.count)
	for i := 0; i < rw.count; i++ {
		idx := (rw.head - rw.count + i + rw.size) % rw.size
		result[i] = rw.data[idx]
	}
	return result
}

// Size returns the configured window size.
func (rw *RollingWindow) Size() int {
	return rw.size
}

// Count returns the number of values currently in the window.
func (rw *RollingWindow) Count() int {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	return rw.count
}

// IsFull returns true if the window contains the maximum number of values.
func (rw *RollingWindow) IsFull() bool {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	return rw.count == rw.size
}

// Clear removes all values from the window.
func (rw *RollingWindow) Clear() {
	rw.mu.Lock()
	defer rw.mu.Unlock()
	rw.count = 0
	rw.head = 0
	rw.sum = 0
	rw.minQueue = rw.minQueue[:0]
	rw.maxQueue = rw.maxQueue[:0]
}

// Sum returns the sum of all values in the window.
func (rw *RollingWindow) Sum() float64 {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	return rw.sum
}

// Average returns the arithmetic mean of all values in the window.
// Returns 0 if the window is empty.
func (rw *RollingWindow) Average() float64 {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0
	}
	return rw.sum / float64(rw.count)
}

// Min returns the minimum value in the window.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Min() (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}
	return rw.data[rw.minQueue[0]], true
}

// Max returns the maximum value in the window.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Max() (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}
	return rw.data[rw.maxQueue[0]], true
}

// Range returns the difference between max and min values.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Range() (float64, bool) {
	min, ok := rw.Min()
	if !ok {
		return 0, false
	}
	max, _ := rw.Max()
	return max - min, true
}

// Variance returns the population variance of values in the window.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Variance() (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}

	avg := rw.sum / float64(rw.count)
	var variance float64
	for i := 0; i < rw.count; i++ {
		idx := (rw.head - rw.count + i + rw.size) % rw.size
		diff := rw.data[idx] - avg
		variance += diff * diff
	}
	return variance / float64(rw.count), true
}

// StdDev returns the population standard deviation of values in the window.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) StdDev() (float64, bool) {
	variance, ok := rw.Variance()
	if !ok {
		return 0, false
	}
	return math.Sqrt(variance), true
}

// Median returns the median value in the window.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Median() (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}

	// Copy values for sorting
	values := make([]float64, rw.count)
	for i := 0; i < rw.count; i++ {
		idx := (rw.head - rw.count + i + rw.size) % rw.size
		values[i] = rw.data[idx]
	}

	// Simple insertion sort (efficient for small windows)
	for i := 1; i < len(values); i++ {
		for j := i; j > 0 && values[j] < values[j-1]; j-- {
			values[j], values[j-1] = values[j-1], values[j]
		}
	}

	mid := len(values) / 2
	if len(values)%2 == 0 {
		return (values[mid-1] + values[mid]) / 2, true
	}
	return values[mid], true
}

// Percentile returns the value at a given percentile (0-100).
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Percentile(p float64) (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}

	if p < 0 {
		p = 0
	} else if p > 100 {
		p = 100
	}

	// Copy values for sorting
	values := make([]float64, rw.count)
	for i := 0; i < rw.count; i++ {
		idx := (rw.head - rw.count + i + rw.size) % rw.size
		values[i] = rw.data[idx]
	}

	// Simple insertion sort
	for i := 1; i < len(values); i++ {
		for j := i; j > 0 && values[j] < values[j-1]; j-- {
			values[j], values[j-1] = values[j-1], values[j]
		}
	}

	index := (p / 100) * float64(len(values)-1)
	lower := int(index)
	upper := lower + 1
	if upper >= len(values) {
		return values[len(values)-1], true
	}
	fraction := index - float64(lower)
	return values[lower] + fraction*(values[upper]-values[lower]), true
}

// Last returns the most recently added value.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) Last() (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}
	idx := (rw.head - 1 + rw.size) % rw.size
	return rw.data[idx], true
}

// First returns the oldest value in the window.
// Returns 0 and false if the window is empty.
func (rw *RollingWindow) First() (float64, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return 0, false
	}
	idx := (rw.head - rw.count + rw.size) % rw.size
	return rw.data[idx], true
}

// Statistics returns a snapshot of all window statistics.
type Statistics struct {
	Count     int
	Sum       float64
	Average   float64
	Min       float64
	Max       float64
	Range     float64
	Variance  float64
	StdDev    float64
	Median    float64
	P25       float64
	P75       float64
	P95       float64
	P99       float64
	First     float64
	Last      float64
	IsFull    bool
}

// Stats returns a comprehensive statistics snapshot of the window.
// Returns false if the window is empty.
func (rw *RollingWindow) Stats() (Statistics, bool) {
	rw.mu.RLock()
	defer rw.mu.RUnlock()
	if rw.count == 0 {
		return Statistics{}, false
	}

	min, _ := rw.Min()
	max, _ := rw.Max()
	rng, _ := rw.Range()
	variance, _ := rw.Variance()
	stdDev, _ := rw.StdDev()
	median, _ := rw.Median()
	p25, _ := rw.Percentile(25)
	p75, _ := rw.Percentile(75)
	p95, _ := rw.Percentile(95)
	p99, _ := rw.Percentile(99)
	first, _ := rw.First()
	last, _ := rw.Last()

	return Statistics{
		Count:     rw.count,
		Sum:       rw.sum,
		Average:   rw.sum / float64(rw.count),
		Min:       min,
		Max:       max,
		Range:     rng,
		Variance:  variance,
		StdDev:    stdDev,
		Median:    median,
		P25:       p25,
		P75:       p75,
		P95:       p95,
		P99:       p99,
		First:     first,
		Last:      last,
		IsFull:    rw.count == rw.size,
	}, true
}

// RollingInt is a specialized rolling window for integer values.
type RollingInt struct {
	window *RollingWindow
}

// NewRollingInt creates a new integer rolling window.
func NewRollingInt(size int) *RollingInt {
	return &RollingInt{window: NewRollingWindow(size)}
}

// Add inserts an integer value.
func (ri *RollingInt) Add(value int) {
	ri.window.Add(float64(value))
}

// Values returns all integer values.
func (ri *RollingInt) Values() []int {
	floats := ri.window.Values()
	result := make([]int, len(floats))
	for i, v := range floats {
		result[i] = int(math.Round(v))
	}
	return result
}

// Sum returns the integer sum.
func (ri *RollingInt) Sum() int {
	return int(math.Round(ri.window.Sum()))
}

// Average returns the average (may have decimal).
func (ri *RollingInt) Average() float64 {
	return ri.window.Average()
}

// Min returns the minimum value.
func (ri *RollingInt) Min() (int, bool) {
	v, ok := ri.window.Min()
	return int(math.Round(v)), ok
}

// Max returns the maximum value.
func (ri *RollingInt) Max() (int, bool) {
	v, ok := ri.window.Max()
	return int(math.Round(v)), ok
}

// Count returns the number of values.
func (ri *RollingInt) Count() int {
	return ri.window.Count()
}

// Clear clears the window.
func (ri *RollingInt) Clear() {
	ri.window.Clear()
}

// ExponentialMovingAverage implements EMA calculation.
type ExponentialMovingAverage struct {
	value     float64
	alpha     float64
	initialized bool
	mu        sync.RWMutex
}

// NewEMA creates a new EMA with the given smoothing factor (alpha).
// Alpha should be between 0 and 1. Smaller alpha = more smoothing.
func NewEMA(alpha float64) *ExponentialMovingAverage {
	if alpha < 0 {
		alpha = 0
	} else if alpha > 1 {
		alpha = 1
	}
	return &ExponentialMovingAverage{alpha: alpha}
}

// NewEMAFromPeriod creates an EMA with alpha calculated from period.
// alpha = 2 / (period + 1)
func NewEMAFromPeriod(period int) *ExponentialMovingAverage {
	if period < 1 {
		period = 1
	}
	alpha := 2.0 / float64(period+1)
	return NewEMA(alpha)
}

// Add updates the EMA with a new value.
func (ema *ExponentialMovingAverage) Add(value float64) {
	ema.mu.Lock()
	defer ema.mu.Unlock()
	if !ema.initialized {
		ema.value = value
		ema.initialized = true
	} else {
		ema.value = ema.alpha*value + (1-ema.alpha)*ema.value
	}
}

// Value returns the current EMA value.
func (ema *ExponentialMovingAverage) Value() float64 {
	ema.mu.RLock()
	defer ema.mu.RUnlock()
	return ema.value
}

// Reset clears the EMA state.
func (ema *ExponentialMovingAverage) Reset() {
	ema.mu.Lock()
	defer ema.mu.Unlock()
	ema.value = 0
	ema.initialized = false
}

// IsInitialized returns true if at least one value has been added.
func (ema *ExponentialMovingAverage) IsInitialized() bool {
	ema.mu.RLock()
	defer ema.mu.RUnlock()
	return ema.initialized
}

// CumulativeSum tracks cumulative sums with optional reset.
type CumulativeSum struct {
	sum float64
	mu  sync.RWMutex
}

// NewCumulativeSum creates a new CumulativeSum tracker.
func NewCumulativeSum() *CumulativeSum {
	return &CumulativeSum{}
}

// Add adds a value to the cumulative sum.
func (cs *CumulativeSum) Add(value float64) {
	cs.mu.Lock()
	defer cs.mu.Unlock()
	cs.sum += value
}

// Sum returns the current cumulative sum.
func (cs *CumulativeSum) Sum() float64 {
	cs.mu.RLock()
	defer cs.mu.RUnlock()
	return cs.sum
}

// Reset resets the cumulative sum to zero.
func (cs *CumulativeSum) Reset() float64 {
	cs.mu.Lock()
	defer cs.mu.Unlock()
	result := cs.sum
	cs.sum = 0
	return result
}

// Counter is a simple thread-safe counter.
type Counter struct {
	value int64
	mu    sync.RWMutex
}

// NewCounter creates a new Counter.
func NewCounter() *Counter {
	return &Counter{}
}

// Increment increases the counter by 1.
func (c *Counter) Increment() int64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
	return c.value
}

// Decrement decreases the counter by 1.
func (c *Counter) Decrement() int64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value--
	return c.value
}

// Add adds a delta to the counter.
func (c *Counter) Add(delta int64) int64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value += delta
	return c.value
}

// Value returns the current counter value.
func (c *Counter) Value() int64 {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.value
}

// Reset resets the counter to zero and returns the previous value.
func (c *Counter) Reset() int64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	result := c.value
	c.value = 0
	return result
}