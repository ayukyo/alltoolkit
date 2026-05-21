// Package sliding_window_average provides a thread-safe sliding window average calculator.
// It efficiently maintains a running average over a fixed-size window of values,
// useful for real-time metrics, monitoring, and time-series analysis.
package sliding_window_average

import (
	"errors"
	"sync"
	"time"
)

// SlidingWindowAverage maintains a fixed-size window of values and computes
// various statistics efficiently.
type SlidingWindowAverage struct {
	mu          sync.RWMutex
	window      []float64
	size        int
	head        int
	count       int
	sum         float64
	sumSquares  float64
	min         float64
	max         float64
	timestamps  []time.Time
	withTime    bool
}

// New creates a new SlidingWindowAverage with the specified window size.
func New(size int) (*SlidingWindowAverage, error) {
	if size <= 0 {
		return nil, errors.New("window size must be positive")
	}
	return &SlidingWindowAverage{
		window: make([]float64, size),
		size:   size,
	}, nil
}

// NewWithTimestamps creates a new SlidingWindowAverage that also tracks timestamps.
func NewWithTimestamps(size int) (*SlidingWindowAverage, error) {
	if size <= 0 {
		return nil, errors.New("window size must be positive")
	}
	return &SlidingWindowAverage{
		window:     make([]float64, size),
		timestamps: make([]time.Time, size),
		size:       size,
		withTime:   true,
	}, nil
}

// Add adds a new value to the window.
// If the window is full, the oldest value is removed.
func (s *SlidingWindowAverage) Add(value float64) {
	s.AddWithTimestamp(value, time.Now())
}

// AddWithTimestamp adds a new value with a specific timestamp.
func (s *SlidingWindowAverage) AddWithTimestamp(value float64, t time.Time) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// If window is full, remove oldest value
	if s.count == s.size {
		// Update sum and sumSquares by removing oldest value
		oldest := s.window[s.head]
		s.sum -= oldest
		s.sumSquares -= oldest * oldest
	} else {
		s.count++
	}

	// Add new value
	s.window[s.head] = value
	s.sum += value
	s.sumSquares += value * value

	// Update timestamps if tracking
	if s.withTime {
		s.timestamps[s.head] = t
	}

	// Update min/max
	if s.count == 1 || value < s.min {
		s.min = value
	}
	if s.count == 1 || value > s.max {
		s.max = value
	}

	// Move head
	s.head = (s.head + 1) % s.size
}

// Average returns the average of all values in the window.
func (s *SlidingWindowAverage) Average() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if s.count == 0 {
		return 0
	}
	return s.sum / float64(s.count)
}

// Sum returns the sum of all values in the window.
func (s *SlidingWindowAverage) Sum() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.sum
}

// Min returns the minimum value in the window.
func (s *SlidingWindowAverage) Min() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.min
}

// Max returns the maximum value in the window.
func (s *SlidingWindowAverage) Max() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.max
}

// Count returns the number of values in the window.
func (s *SlidingWindowAverage) Count() int {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.count
}

// IsFull returns true if the window is full.
func (s *SlidingWindowAverage) IsFull() bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.count == s.size
}

// Variance returns the variance of values in the window.
func (s *SlidingWindowAverage) Variance() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if s.count == 0 {
		return 0
	}

	avg := s.sum / float64(s.count)
	return s.sumSquares/float64(s.count) - avg*avg
}

// StdDev returns the standard deviation of values in the window.
func (s *SlidingWindowAverage) StdDev() float64 {
	variance := s.Variance()
	if variance < 0 {
		return 0
	}
	return sqrt(variance)
}

// Simple sqrt implementation to avoid importing math
func sqrt(x float64) float64 {
	if x <= 0 {
		return 0
	}
	
	// Newton's method
	z := x
	for i := 0; i < 10; i++ {
		z = (z + x/z) / 2
	}
	return z
}

// Values returns a copy of all values in the window in insertion order.
func (s *SlidingWindowAverage) Values() []float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if s.count == 0 {
		return nil
	}

	result := make([]float64, s.count)
	
	// Calculate the start index for oldest value
	start := (s.head - s.count + s.size) % s.size
	
	for i := 0; i < s.count; i++ {
		result[i] = s.window[(start+i)%s.size]
	}
	return result
}

// Clear resets the window.
func (s *SlidingWindowAverage) Clear() {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.window = make([]float64, s.size)
	s.head = 0
	s.count = 0
	s.sum = 0
	s.sumSquares = 0
	s.min = 0
	s.max = 0
	
	if s.withTime {
		s.timestamps = make([]time.Time, s.size)
	}
}

// Median returns the median of values in the window.
func (s *SlidingWindowAverage) Median() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if s.count == 0 {
		return 0
	}

	values := s.Values()
	
	// Simple insertion sort for median
	n := len(values)
	sorted := make([]float64, n)
	copy(sorted, values)
	
	for i := 1; i < n; i++ {
		key := sorted[i]
		j := i - 1
		for j >= 0 && sorted[j] > key {
			sorted[j+1] = sorted[j]
			j--
		}
		sorted[j+1] = key
	}

	if n%2 == 1 {
		return sorted[n/2]
	}
	return (sorted[n/2-1] + sorted[n/2]) / 2
}

// Percentile returns the value at the given percentile (0-100).
func (s *SlidingWindowAverage) Percentile(p float64) float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if s.count == 0 {
		return 0
	}

	if p < 0 {
		p = 0
	}
	if p > 100 {
		p = 100
	}

	values := s.Values()
	n := len(values)
	
	// Simple insertion sort
	sorted := make([]float64, n)
	copy(sorted, values)
	
	for i := 1; i < n; i++ {
		key := sorted[i]
		j := i - 1
		for j >= 0 && sorted[j] > key {
			sorted[j+1] = sorted[j]
			j--
		}
		sorted[j+1] = key
	}

	if n == 1 {
		return sorted[0]
	}

	index := (p / 100) * float64(n-1)
	lower := int(index)
	upper := lower + 1
	
	if upper >= n {
		return sorted[n-1]
	}

	fraction := index - float64(lower)
	return sorted[lower] + fraction*(sorted[upper]-sorted[lower])
}

// Rate returns the rate of change (values per second) based on timestamps.
// Only works if created with NewWithTimestamps.
func (s *SlidingWindowAverage) Rate() float64 {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if !s.withTime || s.count < 2 {
		return 0
	}

	// Find oldest and newest timestamps
	start := (s.head - s.count + s.size) % s.size
	oldest := s.timestamps[start]
	newest := s.timestamps[(s.head - 1 + s.size) % s.size]

	duration := newest.Sub(oldest).Seconds()
	if duration <= 0 {
		return 0
	}

	return s.sum / duration
}

// Stats returns all statistics in a single struct.
type Stats struct {
	Count     int
	Sum       float64
	Average   float64
	Min       float64
	Max       float64
	Variance  float64
	StdDev    float64
	Median    float64
	P25       float64
	P75       float64
	P95       float64
	P99       float64
}

// GetStats returns comprehensive statistics about the window.
func (s *SlidingWindowAverage) GetStats() Stats {
	s.mu.RLock()
	defer s.mu.RUnlock()

	return Stats{
		Count:    s.count,
		Sum:      s.sum,
		Average:  s.Average(),
		Min:      s.min,
		Max:      s.max,
		Variance: s.Variance(),
		StdDev:   s.StdDev(),
		Median:   s.Median(),
		P25:      s.Percentile(25),
		P75:      s.Percentile(75),
		P95:      s.Percentile(95),
		P99:      s.Percentile(99),
	}
}