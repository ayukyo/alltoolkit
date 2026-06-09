// Package count_min_sketch implements a probabilistic data structure for frequency estimation.
// Uses sublinear space for counting item frequencies with controlled error bounds.
package count_min_sketch

import (
	"encoding/binary"
	"hash/fnv"
	"math"
)

// Config holds configuration for Count-Min Sketch
type Config struct {
	Depth uint
	Width uint
	Seed  uint64
}

// CountMinSketch represents a Count-Min Sketch data structure
type CountMinSketch struct {
	table       [][]uint64
	depth       uint
	width       uint
	seed        uint64
	totalCount  uint64
}

// New creates a new Count-Min Sketch with given configuration
func New(depth, width uint) *CountMinSketch {
	if depth < 1 {
		depth = 1
	}
	if width < 2 {
		width = 2
	}
	
	table := make([][]uint64, depth)
	for i := range table {
		table[i] = make([]uint64, width)
	}
	
	return &CountMinSketch{
		table:      table,
		depth:      depth,
		width:      width,
		seed:       0xDEADBEEF,
		totalCount: 0,
	}
}

// NewWithConfig creates a Count-Min Sketch from configuration
func NewWithConfig(config Config) *CountMinSketch {
	return New(config.Depth, config.Width)
}

// Optimal creates configuration based on desired error rate and confidence
// epsilon: relative error bound (e.g., 0.01 = 1% error)
// delta: confidence probability (e.g., 0.01 = 99% confidence)
func Optimal(epsilon, delta float64) Config {
	width := math.Ceil(math.E / epsilon)
	depth := math.Ceil(-math.Log(delta))

	return Config{
		Depth: uint(math.Max(1, depth)),
		Width: uint(math.Max(2, width)),
		Seed:  0xDEADBEEF,
	}
}

// WithRate creates a new sketch with optimal config for given epsilon and delta
func WithRate(epsilon, delta float64) *CountMinSketch {
	config := Optimal(epsilon, delta)
	return New(config.Depth, config.Width)
}

// Update increases the count for an item by delta
func (c *CountMinSketch) Update(item string, delta uint64) {
	hashes := c.getHashes(item)
	for i, h := range hashes {
		idx := h % uint64(c.width)
		c.table[i][idx] += delta
	}
	c.totalCount += delta
}

// Increment increases count by 1
func (c *CountMinSketch) Increment(item string) {
	c.Update(item, 1)
}

// Estimate returns the estimated count for an item (upper bound)
func (c *CountMinSketch) Estimate(item string) uint64 {
	hashes := c.getHashes(item)
	min := uint64(0)
	for i, h := range hashes {
		idx := h % uint64(c.width)
		val := c.table[i][idx]
		if i == 0 || val < min {
			min = val
		}
	}
	return min
}

// TotalCount returns total number of items processed
func (c *CountMinSketch) TotalCount() uint64 {
	return c.totalCount
}

// Dimensions returns (depth, width)
func (c *CountMinSketch) Dimensions() (uint, uint) {
	return c.depth, c.width
}

// Merge combines another sketch into this one (must have same dimensions)
func (c *CountMinSketch) Merge(other *CountMinSketch) error {
	if c.depth != other.depth || c.width != other.width {
		return ErrDimensionMismatch
	}
	for i := uint(0); i < c.depth; i++ {
		for j := uint(0); j < c.width; j++ {
			c.table[i][j] += other.table[i][j]
		}
	}
	c.totalCount += other.totalCount
	return nil
}

// ToBytes serializes the sketch to bytes
func (c *CountMinSketch) ToBytes() []byte {
	totalSize := 32 + int(c.depth)*int(c.width)*8
	bytes := make([]byte, totalSize)
	
	binary.LittleEndian.PutUint64(bytes[0:8], uint64(c.depth))
	binary.LittleEndian.PutUint64(bytes[8:16], uint64(c.width))
	binary.LittleEndian.PutUint64(bytes[16:24], c.seed)
	binary.LittleEndian.PutUint64(bytes[24:32], c.totalCount)
	
	offset := 32
	for i := uint(0); i < c.depth; i++ {
		for j := uint(0); j < c.width; j++ {
			binary.LittleEndian.PutUint64(bytes[offset:offset+8], c.table[i][j])
			offset += 8
		}
	}
	
	return bytes
}

// FromBytes deserializes a sketch from bytes
func FromBytes(bytes []byte) (*CountMinSketch, error) {
	if len(bytes) < 32 {
		return nil, ErrTooShort
	}
	
	depth := binary.LittleEndian.Uint64(bytes[0:8])
	width := binary.LittleEndian.Uint64(bytes[8:16])
	seed := binary.LittleEndian.Uint64(bytes[16:24])
	totalCount := binary.LittleEndian.Uint64(bytes[24:32])
	
	expectedLen := 32 + int(depth)*int(width)*8
	if len(bytes) < expectedLen {
		return nil, ErrInvalidLength
	}
	
	table := make([][]uint64, depth)
	offset := 32
	for i := uint64(0); i < depth; i++ {
		table[i] = make([]uint64, width)
		for j := uint64(0); j < width; j++ {
			table[i][j] = binary.LittleEndian.Uint64(bytes[offset : offset+8])
			offset += 8
		}
	}
	
	return &CountMinSketch{
		table:      table,
		depth:      uint(depth),
		width:      uint(width),
		seed:       seed,
		totalCount: totalCount,
	}, nil
}

// Clear resets the sketch
func (c *CountMinSketch) Clear() {
	for i := range c.table {
		for j := range c.table[i] {
			c.table[i][j] = 0
		}
	}
	c.totalCount = 0
}

func (c *CountMinSketch) getHashes(item string) []uint64 {
	h1 := fnv.New64a()
	h1.Write([]byte(item))
	sum1 := h1.Sum64()
	
	h2 := fnv.New64a()
	seedBytes := []byte{
		byte(c.seed >> 56), byte(c.seed >> 48), byte(c.seed >> 40), byte(c.seed >> 32),
		byte(c.seed >> 24), byte(c.seed >> 16), byte(c.seed >> 8), byte(c.seed),
	}
	h2.Write(seedBytes)
	h2.Write([]byte(item))
	sum2 := h2.Sum64()
	
	hashes := make([]uint64, c.depth)
	for i := uint(0); i < c.depth; i++ {
		hashes[i] = sum1 + uint64(i)*sum2
	}
	return hashes
}

var (
	ErrDimensionMismatch = &errorString{"cannot merge sketches with different dimensions"}
	ErrTooShort         = &errorString{"invalid bytes: too short"}
	ErrInvalidLength    = &errorString{"invalid bytes: incorrect length"}
)

type errorString struct {
	s string
}

func (e *errorString) Error() string {
	return e.s
}