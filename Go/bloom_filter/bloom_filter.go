// Package bloom_filter implements a space-efficient probabilistic data structure
// for testing whether an element is a member of a set.
//
// False positive matches are possible, but false negatives are not.
// Elements can be added to the set, but not removed.
package bloom_filter

import (
	"encoding/base64"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"hash/fnv"
	"math"
)

// BloomFilter represents a Bloom filter data structure
type BloomFilter struct {
	bitmap    []bool
	size      uint
	hashCount uint
	count     uint
}

// Config holds configuration for creating a Bloom filter
type Config struct {
	// ExpectedItems is the expected number of items to be inserted
	ExpectedItems uint
	// FalsePositiveRate is the desired false positive probability (0.0 - 1.0)
	FalsePositiveRate float64
}

// Stats holds statistics about a Bloom filter
type Stats struct {
	Size             uint    // Size of the bitmap
	HashCount        uint    // Number of hash functions
	ItemCount        uint    // Number of items inserted
	FillRatio        float64 // Percentage of bits set
	ExpectedFP       float64 // Expected false positive rate at current fill
	OptimalFP        float64 // Optimal false positive rate if sized correctly
	CapacityUsed     float64 // Percentage of expected capacity used
}

// New creates a new Bloom filter with the given size and number of hash functions
func New(size, hashCount uint) *BloomFilter {
	return &BloomFilter{
		bitmap:    make([]bool, size),
		size:      size,
		hashCount: hashCount,
		count:     0,
	}
}

// NewWithConfig creates a new Bloom filter optimized for the expected number of items
// and desired false positive rate
func NewWithConfig(config Config) *BloomFilter {
	if config.ExpectedItems == 0 {
		config.ExpectedItems = 1000
	}
	if config.FalsePositiveRate <= 0 || config.FalsePositiveRate >= 1 {
		config.FalsePositiveRate = 0.01
	}

	// Calculate optimal size: m = -n * ln(p) / (ln(2)^2)
	size := uint(math.Ceil(-float64(config.ExpectedItems) * math.Log(config.FalsePositiveRate) / (math.Ln2 * math.Ln2)))

	// Calculate optimal hash count: k = (m/n) * ln(2)
	hashCount := uint(math.Ceil(float64(size) / float64(config.ExpectedItems) * math.Ln2))

	return New(size, hashCount)
}

// NewDefault creates a new Bloom filter with default settings
// (10000 expected items, 1% false positive rate)
func NewDefault() *BloomFilter {
	return NewWithConfig(Config{
		ExpectedItems:     10000,
		FalsePositiveRate: 0.01,
	})
}

// hash generates a hash value for the given data using FNV-1a
func (bf *BloomFilter) hash(data []byte, seed uint) uint {
	h := fnv.New128a()
	h.Write(binary.BigEndian.AppendUint64(nil, uint64(seed)))
	h.Write(data)
	
	var digest [16]byte
	h.Sum(digest[:0])
	
	// Use first 8 bytes for the hash value
	return uint(binary.BigEndian.Uint64(digest[:8])) % bf.size
}

// Add inserts an item into the Bloom filter
func (bf *BloomFilter) Add(data []byte) {
	for i := uint(0); i < bf.hashCount; i++ {
		position := bf.hash(data, i)
		bf.bitmap[position] = true
	}
	bf.count++
}

// AddString inserts a string into the Bloom filter
func (bf *BloomFilter) AddString(s string) {
	bf.Add([]byte(s))
}

// Contains checks if an item might be in the set
// Returns true if the item might be in the set (may be a false positive)
// Returns false if the item is definitely not in the set
func (bf *BloomFilter) Contains(data []byte) bool {
	for i := uint(0); i < bf.hashCount; i++ {
		position := bf.hash(data, i)
		if !bf.bitmap[position] {
			return false
		}
	}
	return true
}

// ContainsString checks if a string might be in the set
func (bf *BloomFilter) ContainsString(s string) bool {
	return bf.Contains([]byte(s))
}

// Clear resets the Bloom filter
func (bf *BloomFilter) Clear() {
	for i := range bf.bitmap {
		bf.bitmap[i] = false
	}
	bf.count = 0
}

// Size returns the size of the bitmap
func (bf *BloomFilter) Size() uint {
	return bf.size
}

// Count returns the number of items inserted
func (bf *BloomFilter) Count() uint {
	return bf.count
}

// HashCount returns the number of hash functions used
func (bf *BloomFilter) HashCount() uint {
	return bf.hashCount
}

// FillRatio returns the fraction of bits that are set
func (bf *BloomFilter) FillRatio() float64 {
	setBits := 0
	for _, bit := range bf.bitmap {
		if bit {
			setBits++
		}
	}
	return float64(setBits) / float64(bf.size)
}

// FalsePositiveRate estimates the current false positive rate
// based on the fill ratio
func (bf *BloomFilter) FalsePositiveRate() float64 {
	// P(false positive) = (1 - e^(-kn/m))^k
	// Simplified: approximately (fillRatio)^k
	return math.Pow(bf.FillRatio(), float64(bf.hashCount))
}

// Stats returns detailed statistics about the Bloom filter
func (bf *BloomFilter) Stats() Stats {
	return Stats{
		Size:         bf.size,
		HashCount:    bf.hashCount,
		ItemCount:    bf.count,
		FillRatio:    bf.FillRatio(),
		ExpectedFP:   bf.FalsePositiveRate(),
		OptimalFP:    calculateOptimalFP(bf.count, bf.size),
		CapacityUsed: 0, // Would need expected items to calculate
	}
}

// calculateOptimalFP calculates the optimal false positive rate
func calculateOptimalFP(n, m uint) float64 {
	if n == 0 || m == 0 {
		return 0
	}
	k := math.Ceil(float64(m) / float64(n) * math.Ln2)
	return math.Pow(1-math.Exp(-float64(n)*k/float64(m)), k)
}

// Export exports the Bloom filter to a JSON-serializable structure
func (bf *BloomFilter) Export() *ExportedFilter {
	// Convert bool slice to byte slice for efficient encoding
	bytes := make([]byte, (bf.size+7)/8)
	for i, bit := range bf.bitmap {
		if bit {
			bytes[i/8] |= 1 << (i % 8)
		}
	}
	
	return &ExportedFilter{
		Size:      bf.size,
		HashCount: bf.hashCount,
		Count:     bf.count,
		Bitmap:    base64.StdEncoding.EncodeToString(bytes),
	}
}

// ExportedFilter is a JSON-serializable representation of a Bloom filter
type ExportedFilter struct {
	Size      uint   `json:"size"`
	HashCount uint   `json:"hash_count"`
	Count     uint   `json:"count"`
	Bitmap    string `json:"bitmap"`
}

// Import creates a Bloom filter from an exported structure
func Import(exported *ExportedFilter) (*BloomFilter, error) {
	if exported == nil {
		return nil, fmt.Errorf("exported filter is nil")
	}
	
	bytes, err := base64.StdEncoding.DecodeString(exported.Bitmap)
	if err != nil {
		return nil, fmt.Errorf("failed to decode bitmap: %w", err)
	}
	
	bf := &BloomFilter{
		size:      exported.Size,
		hashCount: exported.HashCount,
		count:     exported.Count,
		bitmap:    make([]bool, exported.Size),
	}
	
	// Convert byte slice back to bool slice
	for i := uint(0); i < bf.size; i++ {
		byteIndex := i / 8
		bitIndex := i % 8
		if byteIndex < uint(len(bytes)) {
			bf.bitmap[i] = (bytes[byteIndex] & (1 << bitIndex)) != 0
		}
	}
	
	return bf, nil
}

// ToJSON exports the Bloom filter as a JSON string
func (bf *BloomFilter) ToJSON() (string, error) {
	exported := bf.Export()
	data, err := json.Marshal(exported)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// FromJSON creates a Bloom filter from a JSON string
func FromJSON(jsonStr string) (*BloomFilter, error) {
	var exported ExportedFilter
	if err := json.Unmarshal([]byte(jsonStr), &exported); err != nil {
		return nil, err
	}
	return Import(&exported)
}

// Union computes the union of two Bloom filters
// Both filters must have the same size and hash count
func (bf *BloomFilter) Union(other *BloomFilter) (*BloomFilter, error) {
	if bf.size != other.size || bf.hashCount != other.hashCount {
		return nil, fmt.Errorf("filters must have the same size and hash count")
	}
	
	result := New(bf.size, bf.hashCount)
	for i := uint(0); i < bf.size; i++ {
		result.bitmap[i] = bf.bitmap[i] || other.bitmap[i]
	}
	result.count = bf.count + other.count // Approximate
	return result, nil
}

// Intersect computes the intersection of two Bloom filters
// Both filters must have the same size and hash count
func (bf *BloomFilter) Intersect(other *BloomFilter) (*BloomFilter, error) {
	if bf.size != other.size || bf.hashCount != other.hashCount {
		return nil, fmt.Errorf("filters must have the same size and hash count")
	}
	
	result := New(bf.size, bf.hashCount)
	for i := uint(0); i < bf.size; i++ {
		result.bitmap[i] = bf.bitmap[i] && other.bitmap[i]
	}
	// Intersection count is approximated (lower bound)
	result.count = min(bf.count, other.count)
	return result, nil
}

// String returns a string representation of the Bloom filter stats
func (bf *BloomFilter) String() string {
	return fmt.Sprintf("BloomFilter{size=%d, hashCount=%d, count=%d, fillRatio=%.4f, fp=%.6f}",
		bf.size, bf.hashCount, bf.count, bf.FillRatio(), bf.FalsePositiveRate())
}

// min returns the minimum of two uint values
func min(a, b uint) uint {
	if a < b {
		return a
	}
	return b
}