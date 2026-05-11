// Package cuckoo_filter_utils implements a Cuckoo Filter - a probabilistic data structure
// for set membership testing. Cuckoo filters support adding, removing, and checking
// membership with a configurable false positive rate.
//
// Advantages over Bloom filters:
//   - Supports deletion of items
//   - Lower false positive rate for the same space
//   - Simpler implementation
//
// References:
//   - Fan et al., "Cuckoo Filter: Practically Better Than Bloom", CONCURRENCY 2014
package cuckoo_filter_utils

import (
	"errors"
	"math"
)

// CuckooFilter is a probabilistic set membership data structure.
// It supports add, remove, and contains operations with O(1) expected time.
type CuckooFilter struct {
	buckets    []bucket
	bucketSize uint
	numBuckets uint
	count      uint
	kicks      uint    // Maximum number of kicks during insertion
	hashSeed   uint32  // Seed for hash function
	fpBits     uint    // Fingerprint size in bits
	fpMask     uint8   // Mask for extracting fingerprint
}

// bucket holds a fixed number of fingerprints
type bucket []uint8

// Options contains configuration for the CuckooFilter
type Options struct {
	// Capacity is the expected number of items to store
	Capacity uint
	// FalsePositiveRate is the target false positive probability (0 < p < 1)
	FalsePositiveRate float64
	// BucketSize is the number of fingerprints per bucket (typically 2-4)
	BucketSize uint
	// MaxKicks is the maximum number of kick attempts during insertion
	MaxKicks uint
}

// DefaultOptions returns the default options for a CuckooFilter
func DefaultOptions(capacity uint) Options {
	return Options{
		Capacity:          capacity,
		FalsePositiveRate: 0.03,
		BucketSize:        4,
		MaxKicks:          500,
	}
}

var (
	ErrCapacityZero      = errors.New("capacity must be greater than zero")
	ErrBucketSizeZero    = errors.New("bucket size must be greater than zero")
	ErrFalsePositiveRate = errors.New("false positive rate must be between 0 and 1")
	ErrFilterFull        = errors.New("filter is full")
	ErrItemNotFound      = errors.New("item not found")
)

// New creates a new CuckooFilter with the given options
func New(opts Options) (*CuckooFilter, error) {
	if opts.Capacity == 0 {
		return nil, ErrCapacityZero
	}
	if opts.BucketSize == 0 {
		opts.BucketSize = 4
	}
	if opts.FalsePositiveRate <= 0 || opts.FalsePositiveRate >= 1 {
		opts.FalsePositiveRate = 0.03
	}
	if opts.MaxKicks == 0 {
		opts.MaxKicks = 500
	}

	// Calculate fingerprint size based on false positive rate
	// Formula: f = ceil(log2(1/e)) + ceil(log2(b))
	// where e is false positive rate and b is bucket size
	fpBits := uint(math.Ceil(math.Log2(1/opts.FalsePositiveRate))) + uint(math.Ceil(math.Log2(float64(opts.BucketSize))))
	if fpBits < 4 {
		fpBits = 4
	}
	if fpBits > 8 {
		fpBits = 8 // Limit to uint8
	}

	// Calculate number of buckets
	// We want roughly capacity / load_factor items, where load_factor is about 0.95
	numBuckets := nextPowerOfTwo(uint(float64(opts.Capacity) / 0.95 / float64(opts.BucketSize)))
	if numBuckets < 1 {
		numBuckets = 1
	}

	buckets := make([]bucket, numBuckets)
	for i := range buckets {
		buckets[i] = make(bucket, opts.BucketSize)
		for j := range buckets[i] {
			buckets[i][j] = 0
		}
	}

	return &CuckooFilter{
		buckets:    buckets,
		bucketSize: opts.BucketSize,
		numBuckets: numBuckets,
		count:      0,
		kicks:      opts.MaxKicks,
		hashSeed:   0x5bd1e995, // MurmurHash seed
		fpBits:     fpBits,
		fpMask:     uint8((1 << fpBits) - 1),
	}, nil
}

// nextPowerOfTwo returns the next power of two >= n
func nextPowerOfTwo(n uint) uint {
	if n == 0 {
		return 1
	}
	n--
	n |= n >> 1
	n |= n >> 2
	n |= n >> 4
	n |= n >> 8
	n |= n >> 16
	n |= n >> 32
	return n + 1
}

// hash computes a 32-bit hash of the data using MurmurHash2-like algorithm
func (cf *CuckooFilter) hash(data []byte) uint32 {
	h := cf.hashSeed ^ uint32(len(data))
	for _, b := range data {
		h ^= uint32(b)
		h *= 0x5bd1e995
		h ^= h >> 15
	}
	return h
}

// fingerprint generates a non-zero fingerprint for the data
func (cf *CuckooFilter) fingerprint(data []byte) uint8 {
	h := cf.hash(data)
	fp := uint8(h) & cf.fpMask
	if fp == 0 {
		fp = 1 // Ensure fingerprint is never 0
	}
	return fp
}

// indices computes both bucket indices for a given data and fingerprint
func (cf *CuckooFilter) indices(data []byte, fp uint8) (uint, uint) {
	// Primary index from hash of data
	h := cf.hash(data)
	i1 := uint(h) & (cf.numBuckets - 1)
	
	// Secondary index using partial-key cuckoo hashing: i2 = i1 XOR hash(fp)
	fpHash := cf.hash([]byte{fp})
	i2 := (i1 ^ uint(fpHash)) & (cf.numBuckets - 1)
	
	return i1, i2
}

// Add inserts an item into the filter
func (cf *CuckooFilter) Add(data []byte) error {
	fp := cf.fingerprint(data)
	i1, i2 := cf.indices(data, fp)

	// Try to insert into first bucket
	if cf.insertToBucket(i1, fp) {
		cf.count++
		return nil
	}

	// Try to insert into second bucket
	if cf.insertToBucket(i2, fp) {
		cf.count++
		return nil
	}

	// Need to relocate existing items (kick out)
	return cf.kickInsert(i1, i2, fp)
}

// insertToBucket tries to insert fingerprint into bucket at given index
func (cf *CuckooFilter) insertToBucket(idx uint, fp uint8) bool {
	for i := uint(0); i < cf.bucketSize; i++ {
		if cf.buckets[idx][i] == 0 {
			cf.buckets[idx][i] = fp
			return true
		}
	}
	return false
}

// kickInsert relocates items to make room for the new fingerprint
func (cf *CuckooFilter) kickInsert(i1, i2 uint, fp uint8) error {
	// Pick a random bucket to start kicking from
	idx := i1
	if cf.hash([]byte{fp, byte(i2)})%2 == 1 {
		idx = i2
	}

	for n := uint(0); n < cf.kicks; n++ {
		// Pick a random slot in the current bucket
		slot := (uint(cf.hash([]byte{fp, byte(n), byte(idx >> 8), byte(idx)})) % cf.bucketSize)
		
		// Swap fingerprints
		oldFP := cf.buckets[idx][slot]
		cf.buckets[idx][slot] = fp
		fp = oldFP

		// Compute alternate index for the displaced fingerprint
		fpHash := cf.hash([]byte{fp})
		idx = (idx ^ uint(fpHash)) & (cf.numBuckets - 1)

		// Try to insert the displaced fingerprint
		if cf.insertToBucket(idx, fp) {
			cf.count++
			return nil
		}
	}

	return ErrFilterFull
}

// Contains checks if an item might be in the filter
// Returns false negatives are NOT possible in cuckoo filters
func (cf *CuckooFilter) Contains(data []byte) bool {
	fp := cf.fingerprint(data)
	i1, i2 := cf.indices(data, fp)

	// Check both buckets for the fingerprint
	return cf.bucketsContain(i1, fp) || cf.bucketsContain(i2, fp)
}

// bucketsContain checks if a bucket contains a fingerprint
func (cf *CuckooFilter) bucketsContain(idx uint, fp uint8) bool {
	for i := uint(0); i < cf.bucketSize; i++ {
		if cf.buckets[idx][i] == fp {
			return true
		}
	}
	return false
}

// Remove removes an item from the filter
func (cf *CuckooFilter) Remove(data []byte) bool {
	fp := cf.fingerprint(data)
	i1, i2 := cf.indices(data, fp)

	// Try to remove from first bucket
	if cf.removeFromBucket(i1, fp) {
		cf.count--
		return true
	}

	// Try to remove from second bucket
	if cf.removeFromBucket(i2, fp) {
		cf.count--
		return true
	}

	return false
}

// removeFromBucket removes a fingerprint from a bucket
func (cf *CuckooFilter) removeFromBucket(idx uint, fp uint8) bool {
	for i := uint(0); i < cf.bucketSize; i++ {
		if cf.buckets[idx][i] == fp {
			cf.buckets[idx][i] = 0
			return true
		}
	}
	return false
}

// Count returns the number of items in the filter
func (cf *CuckooFilter) Count() uint {
	return cf.count
}

// Capacity returns the maximum number of items the filter can hold
func (cf *CuckooFilter) Capacity() uint {
	return cf.numBuckets * cf.bucketSize
}

// LoadFactor returns the current load factor (items / capacity)
func (cf *CuckooFilter) LoadFactor() float64 {
	return float64(cf.count) / float64(cf.numBuckets*cf.bucketSize)
}

// FalsePositiveRate returns the expected false positive rate
func (cf *CuckooFilter) FalsePositiveRate() float64 {
	// Approximate false positive rate: 2 * b / 2^f where b is bucket size and f is fingerprint bits
	b := float64(cf.bucketSize)
	f := float64(cf.fpBits)
	return 2 * b / math.Pow(2, f)
}

// Reset clears all items from the filter
func (cf *CuckooFilter) Reset() {
	for i := range cf.buckets {
		for j := range cf.buckets[i] {
			cf.buckets[i][j] = 0
		}
	}
	cf.count = 0
}

// Clone creates a copy of the filter
func (cf *CuckooFilter) Clone() *CuckooFilter {
	newBuckets := make([]bucket, cf.numBuckets)
	for i := range newBuckets {
		newBuckets[i] = make(bucket, cf.bucketSize)
		copy(newBuckets[i], cf.buckets[i])
	}

	return &CuckooFilter{
		buckets:    newBuckets,
		bucketSize: cf.bucketSize,
		numBuckets: cf.numBuckets,
		count:      cf.count,
		kicks:      cf.kicks,
		hashSeed:   cf.hashSeed,
		fpBits:     cf.fpBits,
		fpMask:     cf.fpMask,
	}
}

// Equal checks if two filters are identical
func (cf *CuckooFilter) Equal(other *CuckooFilter) bool {
	if cf.bucketSize != other.bucketSize ||
		cf.numBuckets != other.numBuckets ||
		cf.count != other.count ||
		cf.fpBits != other.fpBits {
		return false
	}

	for i := range cf.buckets {
		for j := range cf.buckets[i] {
			if cf.buckets[i][j] != other.buckets[i][j] {
				return false
			}
		}
	}

	return true
}

// Size returns the memory size of the filter in bytes
func (cf *CuckooFilter) Size() uint {
	return cf.numBuckets * cf.bucketSize
}

// Stats returns filter statistics
type Stats struct {
	Count             uint
	Capacity          uint
	LoadFactor        float64
	FalsePositiveRate float64
	FingerprintBits   uint
	BucketSize        uint
	NumBuckets        uint
	MemoryBytes       uint
}

// GetStats returns statistics about the filter
func (cf *CuckooFilter) GetStats() Stats {
	return Stats{
		Count:             cf.count,
		Capacity:          cf.numBuckets * cf.bucketSize,
		LoadFactor:        cf.LoadFactor(),
		FalsePositiveRate: cf.FalsePositiveRate(),
		FingerprintBits:   cf.fpBits,
		BucketSize:        cf.bucketSize,
		NumBuckets:        cf.numBuckets,
		MemoryBytes:       cf.Size(),
	}
}

// IsFull checks if the filter has reached capacity
func (cf *CuckooFilter) IsFull() bool {
	return cf.count >= cf.numBuckets*cf.bucketSize
}

// IsEmpty checks if the filter is empty
func (cf *CuckooFilter) IsEmpty() bool {
	return cf.count == 0
}

// BucketIndex returns the bucket indices for an item (for debugging)
func (cf *CuckooFilter) BucketIndex(data []byte) (uint, uint) {
	fp := cf.fingerprint(data)
	return cf.indices(data, fp)
}

// ForEach iterates over all non-empty slots
func (cf *CuckooFilter) ForEach(fn func(fp uint8)) {
	for i := range cf.buckets {
		for j := range cf.buckets[i] {
			if cf.buckets[i][j] != 0 {
				fn(cf.buckets[i][j])
			}
		}
	}
}

// FingerprintBits returns the number of bits used for fingerprints
func (cf *CuckooFilter) FingerprintBits() uint {
	return cf.fpBits
}

// AddWithFingerprint adds using just a fingerprint value
func (cf *CuckooFilter) AddWithFingerprint(fp uint8) error {
	// Create synthetic key from fingerprint
	key := []byte{fp, byte(fp ^ 0xFF), byte(fp >> 1)}
	return cf.Add(key)
}

// ContainsFingerprint checks if a fingerprint exists (uses fingerprint as key)
func (cf *CuckooFilter) ContainsFingerprint(fp uint8) bool {
	key := []byte{fp, byte(fp ^ 0xFF), byte(fp >> 1)}
	return cf.Contains(key)
}

// RemoveFingerprint removes a fingerprint (uses fingerprint as key)
func (cf *CuckooFilter) RemoveFingerprint(fp uint8) bool {
	key := []byte{fp, byte(fp ^ 0xFF), byte(fp >> 1)}
	return cf.Remove(key)
}

// Merge combines two filters into a new one
func (cf *CuckooFilter) Merge(other *CuckooFilter) (*CuckooFilter, error) {
	if cf.numBuckets != other.numBuckets || cf.bucketSize != other.bucketSize {
		return nil, errors.New("filters must have same configuration")
	}

	result := cf.Clone()
	for i := range other.buckets {
		for j := range other.buckets[i] {
			if other.buckets[i][j] != 0 {
				fp := other.buckets[i][j]
				// Try to add to same bucket first
				if result.insertToBucket(uint(i), fp) {
					result.count++
				}
			}
		}
	}

	return result, nil
}