// Package hyperloglog implements the HyperLogLog algorithm for cardinality estimation.
// HyperLogLog is a probabilistic data structure that estimates the number of distinct elements
// in a very large dataset using very little memory (typically a few KB).
//
// Example: With just 16KB of memory, you can estimate cardinalities up to billions with ~1% error.
// This is widely used in systems like Redis (PFADD/PFCOUNT), BigQuery, and analytics platforms.
package hyperloglog

import (
	"encoding/binary"
	"hash/fnv"
	"math"
)

const (
	// DefaultPrecision is the default precision (number of bits for bucket selection)
	// With precision 14, we use 16384 buckets and achieve ~1% error rate
	DefaultPrecision = 14

	// MinPrecision is the minimum allowed precision
	MinPrecision = 4

	// MaxPrecision is the maximum allowed precision
	MaxPrecision = 16
)

// HyperLogLog is the main data structure for cardinality estimation
type HyperLogLog struct {
	precision uint8
	buckets   []uint8
	numBuckets uint32
}

// New creates a new HyperLogLog instance with the default precision (14)
func New() *HyperLogLog {
	return NewWithPrecision(DefaultPrecision)
}

// NewWithPrecision creates a new HyperLogLog instance with a custom precision
// Higher precision = lower error rate but more memory usage
// Memory usage = 2^precision bytes
// Error rate ≈ 1.04 / sqrt(2^precision)
func NewWithPrecision(precision uint8) *HyperLogLog {
	if precision < MinPrecision {
		precision = MinPrecision
	}
	if precision > MaxPrecision {
		precision = MaxPrecision
	}

	numBuckets := uint32(1) << precision
	return &HyperLogLog{
		precision:  precision,
		buckets:    make([]uint8, numBuckets),
		numBuckets: numBuckets,
	}
}

// hash computes a 64-bit hash of the input data using FNV-1a
func (h *HyperLogLog) hash(data []byte) uint64 {
	hasher := fnv.New64a()
	hasher.Write(data)
	return hasher.Sum64()
}

// countLeadingZeros counts the number of leading zeros plus one
// This is used to find the position of the first 1-bit
func countLeadingZeros(value uint64, maxBits uint8) uint8 {
	// We only look at the lower maxBits bits
	mask := uint64(1) << maxBits
	count := uint8(1)
	for i := uint8(0); i < maxBits; i++ {
		if (value & mask) != 0 {
			return count
		}
		count++
		value <<= 1
	}
	return count
}

// Add inserts an element into the HyperLogLog
// The element can be any byte slice (string, number, etc.)
func (h *HyperLogLog) Add(data []byte) {
	hashValue := h.hash(data)

	// Use the first 'precision' bits for bucket selection
	bucket := hashValue & (uint64(h.numBuckets) - 1)

	// Use the remaining bits for leading zero counting
	remaining := hashValue >> h.precision

	// Count the position of the first 1-bit (rank)
	// We add 1 because we're counting from the position after precision bits
	rank := countLeadingZeros(remaining, 64-h.precision)

	// Update the bucket with the maximum rank seen
	if rank > h.buckets[bucket] {
		h.buckets[bucket] = rank
	}
}

// AddString is a convenience method to add a string element
func (h *HyperLogLog) AddString(s string) {
	h.Add([]byte(s))
}

// AddInt is a convenience method to add an integer element
func (h *HyperLogLog) AddInt(n int64) {
	buf := make([]byte, 8)
	binary.BigEndian.PutUint64(buf, uint64(n))
	h.Add(buf)
}

// Estimate returns the estimated cardinality (number of unique elements)
func (h *HyperLogLog) Estimate() uint64 {
	// Calculate the harmonic mean of 2^(-bucket)
	sum := 0.0
	zeros := 0

	for _, val := range h.buckets {
		if val == 0 {
			zeros++
		}
		sum += math.Pow(2.0, -float64(val))
	}

	// Raw estimate using the HyperLogLog formula
	m := float64(h.numBuckets)
	estimate := alpha(h.numBuckets) * m * m / sum

	// Small range correction (linear counting)
	if estimate <= 2.5*m {
		if zeros > 0 {
			estimate = m * math.Log(m/float64(zeros))
		}
	}

	return uint64(estimate + 0.5)
}

// alpha is the bias correction constant
func alpha(m uint32) float64 {
	switch m {
	case 16:
		return 0.673
	case 32:
		return 0.697
	case 64:
		return 0.709
	default:
		return 0.7213 / (1.0 + 1.079/float64(m))
	}
}

// Merge combines another HyperLogLog into this one
// Both HyperLogLogs must have the same precision
// Returns an error if precisions don't match
func (h *HyperLogLog) Merge(other *HyperLogLog) bool {
	if h.precision != other.precision {
		return false
	}

	for i, val := range other.buckets {
		if val > h.buckets[i] {
			h.buckets[i] = val
		}
	}
	return true
}

// Reset clears all buckets, effectively resetting the HyperLogLog
func (h *HyperLogLog) Reset() {
	for i := range h.buckets {
		h.buckets[i] = 0
	}
}

// Precision returns the precision (number of bits used for bucket selection)
func (h *HyperLogLog) Precision() uint8 {
	return h.precision
}

// MemoryUsage returns the memory usage in bytes
func (h *HyperLogLog) MemoryUsage() int {
	return len(h.buckets)
}

// ErrorRate returns the theoretical error rate
func (h *HyperLogLog) ErrorRate() float64 {
	return 1.04 / math.Sqrt(float64(h.numBuckets))
}

// ToBytes serializes the HyperLogLog to a byte slice
// This is useful for storage or network transmission
func (h *HyperLogLog) ToBytes() []byte {
	// Format: [precision(1 byte)][buckets...]
	result := make([]byte, 1+len(h.buckets))
	result[0] = h.precision
	copy(result[1:], h.buckets)
	return result
}

// FromBytes deserializes a HyperLogLog from a byte slice
func FromBytes(data []byte) (*HyperLogLog, bool) {
	if len(data) < 2 {
		return nil, false
	}

	precision := data[0]
	if precision < MinPrecision || precision > MaxPrecision {
		return nil, false
	}

	hll := NewWithPrecision(precision)
	expectedLen := 1 + int(hll.numBuckets)
	if len(data) != expectedLen {
		return nil, false
	}

	copy(hll.buckets, data[1:])
	return hll, true
}

// Count returns the current estimated cardinality
// This is an alias for Estimate() for API consistency
func (h *HyperLogLog) Count() uint64 {
	return h.Estimate()
}

// Empty returns true if no elements have been added
func (h *HyperLogLog) Empty() bool {
	for _, val := range h.buckets {
		if val > 0 {
			return false
		}
	}
	return true
}

// Clone creates a deep copy of the HyperLogLog
func (h *HyperLogLog) Clone() *HyperLogLog {
	newHll := NewWithPrecision(h.precision)
	copy(newHll.buckets, h.buckets)
	return newHll
}