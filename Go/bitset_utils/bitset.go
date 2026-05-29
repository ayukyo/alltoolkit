// Package bitset_utils provides a comprehensive bitset utility library
// for efficient bit set operations with zero external dependencies.
//
// A BitSet is a dynamic set of bits that can grow as needed.
// It provides efficient operations for bit manipulation, set operations,
// and various utility functions.
package bitset_utils

import (
	"errors"
	"fmt"
	"math/bits"
	"strings"
)

// BitSet represents a dynamic set of bits.
type BitSet struct {
	data   []uint64
	length int // number of bits currently in use
}

// NewBitSet creates a new BitSet with the specified initial capacity.
func NewBitSet(capacity int) *BitSet {
	if capacity < 0 {
		capacity = 0
	}
	words := (capacity + 63) / 64
	if words == 0 {
		words = 1
	}
	return &BitSet{
		data:   make([]uint64, words),
		length: 0,
	}
}

// NewBitSetFrom creates a BitSet from a slice of uint64.
func NewBitSetFrom(data []uint64, length int) *BitSet {
	if length < 0 {
		length = 0
	}
	words := (length + 63) / 64
	if words > len(data) {
		// Extend data if needed
		newData := make([]uint64, words)
		copy(newData, data)
		return &BitSet{data: newData, length: length}
	}
	// Copy data to avoid external modification
	newData := make([]uint64, words)
	copy(newData, data[:words])
	return &BitSet{data: newData, length: length}
}

// NewBitSetFromBytes creates a BitSet from a byte slice.
// Each byte is interpreted with bit 0 as the least significant bit.
func NewBitSetFromBytes(bytes []byte) *BitSet {
	if len(bytes) == 0 {
		return NewBitSet(0)
	}
	bs := NewBitSet(len(bytes) * 8)
	for i, b := range bytes {
		bitOffset := i * 8
		for j := 0; j < 8; j++ {
			if b&(1<<j) != 0 {
				bs.data[(bitOffset+j)/64] |= 1 << ((bitOffset + j) % 64)
			}
		}
	}
	bs.length = len(bytes) * 8
	return bs
}

// NewBitSetFromString creates a BitSet from a binary string (e.g., "10110").
func NewBitSetFromString(s string) (*BitSet, error) {
	if s == "" {
		return NewBitSet(0), nil
	}
	bs := NewBitSet(len(s))
	for i, c := range s {
		if c == '1' {
			bs.Set(len(s) - 1 - i)
		} else if c != '0' {
			return nil, fmt.Errorf("invalid character '%c' at position %d", c, i)
		}
	}
	bs.length = len(s)
	return bs, nil
}

// Clone creates a deep copy of the BitSet.
func (bs *BitSet) Clone() *BitSet {
	data := make([]uint64, len(bs.data))
	copy(data, bs.data)
	return &BitSet{data: data, length: bs.length}
}

// Len returns the number of bits in the BitSet.
func (bs *BitSet) Len() int {
	return bs.length
}

// Cap returns the current capacity of the BitSet.
func (bs *BitSet) Cap() int {
	return len(bs.data) * 64
}

// grow ensures the BitSet has at least n words.
func (bs *BitSet) grow(n int) {
	if n > len(bs.data) {
		newData := make([]uint64, n)
		copy(newData, bs.data)
		bs.data = newData
	}
}

// expand ensures the BitSet can hold at least n bits.
func (bs *BitSet) expand(n int) {
	if n > bs.length {
		words := (n + 63) / 64
		bs.grow(words)
		bs.length = n
	}
}

// Set sets the bit at position i to 1.
func (bs *BitSet) Set(i int) error {
	if i < 0 {
		return errors.New("index cannot be negative")
	}
	bs.expand(i + 1)
	bs.data[i/64] |= 1 << (i % 64)
	return nil
}

// Clear clears the bit at position i (sets to 0).
func (bs *BitSet) Clear(i int) error {
	if i < 0 || i >= bs.length {
		return fmt.Errorf("index %d out of range [0, %d)", i, bs.length)
	}
	bs.data[i/64] &^= 1 << (i % 64)
	return nil
}

// Toggle flips the bit at position i.
func (bs *BitSet) Toggle(i int) error {
	if i < 0 {
		return errors.New("index cannot be negative")
	}
	bs.expand(i + 1)
	bs.data[i/64] ^= 1 << (i % 64)
	return nil
}

// Get returns the value of the bit at position i.
func (bs *BitSet) Get(i int) (bool, error) {
	if i < 0 || i >= bs.length {
		return false, fmt.Errorf("index %d out of range [0, %d)", i, bs.length)
	}
	return (bs.data[i/64] & (1 << (i % 64))) != 0, nil
}

// Test tests if the bit at position i is set.
func (bs *BitSet) Test(i int) bool {
	val, _ := bs.Get(i)
	return val
}

// SetAll sets all bits to 1.
func (bs *BitSet) SetAll() {
	// Extend length to full capacity if not already
	capacity := len(bs.data) * 64
	if bs.length == 0 {
		bs.length = capacity
	}
	for i := range bs.data {
		bs.data[i] = ^uint64(0)
	}
	// Clear unused bits in the last word (if length is not a multiple of 64)
	if rem := bs.length % 64; rem != 0 {
		bs.data[len(bs.data)-1] &= (1 << rem) - 1
	}
}

// ClearAll clears all bits (sets to 0).
func (bs *BitSet) ClearAll() {
	for i := range bs.data {
		bs.data[i] = 0
	}
}

// FlipAll flips all bits.
func (bs *BitSet) FlipAll() {
	for i := range bs.data {
		bs.data[i] = ^bs.data[i]
	}
	// Clear unused bits in the last word
	if rem := bs.length % 64; rem != 0 {
		bs.data[len(bs.data)-1] &= (1 << rem) - 1
	}
}

// Count returns the number of set bits (population count).
func (bs *BitSet) Count() int {
	count := 0
	for _, word := range bs.data {
		count += bits.OnesCount64(word)
	}
	return count
}

// IsEmpty returns true if no bits are set.
func (bs *BitSet) IsEmpty() bool {
	return bs.Count() == 0
}

// IsFull returns true if all bits are set.
func (bs *BitSet) IsFull() bool {
	if bs.length == 0 {
		return false // Empty BitSet is not considered "full"
	}
	return bs.Count() == bs.length
}

// NextSet returns the index of the next set bit >= start.
// Returns -1 if no such bit exists.
func (bs *BitSet) NextSet(start int) int {
	if start < 0 {
		start = 0
	}
	if start >= bs.length {
		return -1
	}

	wordIdx := start / 64
	bitIdx := start % 64

	// Check current word from bitIdx
	if wordIdx < len(bs.data) {
		word := bs.data[wordIdx] >> bitIdx
		if word != 0 {
			return start + bits.TrailingZeros64(word)
		}
	}

	// Check subsequent words
	for i := wordIdx + 1; i < len(bs.data); i++ {
		if bs.data[i] != 0 {
			bit := bits.TrailingZeros64(bs.data[i])
			pos := i*64 + bit
			if pos < bs.length {
				return pos
			}
			return -1
		}
	}

	return -1
}

// NextClear returns the index of the next clear bit >= start.
// Returns -1 if no such bit exists.
func (bs *BitSet) NextClear(start int) int {
	if start < 0 {
		start = 0
	}
	if start >= bs.length {
		return -1
	}

	wordIdx := start / 64
	bitIdx := start % 64

	// Check current word from bitIdx
	if wordIdx < len(bs.data) {
		word := (^bs.data[wordIdx]) >> bitIdx
		if word != 0 {
			return start + bits.TrailingZeros64(word)
		}
	}

	// Check subsequent words
	for i := wordIdx + 1; i < len(bs.data); i++ {
		if bs.data[i] != ^uint64(0) {
			bit := bits.TrailingZeros64(^bs.data[i])
			pos := i*64 + bit
			if pos < bs.length {
				return pos
			}
			return -1
		}
	}

	return -1
}

// And performs bitwise AND with another BitSet.
func (bs *BitSet) And(other *BitSet) *BitSet {
	resultLen := min(bs.length, other.length)
	result := NewBitSet(resultLen)
	result.length = resultLen
	for i := 0; i < len(result.data); i++ {
		if i < len(bs.data) && i < len(other.data) {
			result.data[i] = bs.data[i] & other.data[i]
		}
	}
	return result
}

// Or performs bitwise OR with another BitSet.
func (bs *BitSet) Or(other *BitSet) *BitSet {
	resultLen := max(bs.length, other.length)
	result := NewBitSet(resultLen)
	result.length = resultLen
	for i := 0; i < len(result.data); i++ {
		if i < len(bs.data) && i < len(other.data) {
			result.data[i] = bs.data[i] | other.data[i]
		} else if i < len(bs.data) {
			result.data[i] = bs.data[i]
		} else if i < len(other.data) {
			result.data[i] = other.data[i]
		}
	}
	return result
}

// Xor performs bitwise XOR with another BitSet.
func (bs *BitSet) Xor(other *BitSet) *BitSet {
	resultLen := max(bs.length, other.length)
	result := NewBitSet(resultLen)
	result.length = resultLen
	for i := 0; i < len(result.data); i++ {
		if i < len(bs.data) && i < len(other.data) {
			result.data[i] = bs.data[i] ^ other.data[i]
		} else if i < len(bs.data) {
			result.data[i] = bs.data[i]
		} else if i < len(other.data) {
			result.data[i] = other.data[i]
		}
	}
	return result
}

// AndNot performs bitwise AND NOT with another BitSet (set difference).
func (bs *BitSet) AndNot(other *BitSet) *BitSet {
	result := NewBitSet(bs.length)
	result.length = bs.length
	for i := 0; i < len(result.data); i++ {
		if i < len(bs.data) {
			if i < len(other.data) {
				result.data[i] = bs.data[i] &^ other.data[i]
			} else {
				result.data[i] = bs.data[i]
			}
		}
	}
	return result
}

// Not returns the complement of the BitSet.
func (bs *BitSet) Not() *BitSet {
	result := bs.Clone()
	result.FlipAll()
	return result
}

// Intersects returns true if the BitSet intersects with another BitSet.
func (bs *BitSet) Intersects(other *BitSet) bool {
	minLen := min(len(bs.data), len(other.data))
	for i := 0; i < minLen; i++ {
		if bs.data[i]&other.data[i] != 0 {
			return true
		}
	}
	return false
}

// Subset returns true if bs is a subset of other.
func (bs *BitSet) Subset(other *BitSet) bool {
	minLen := min(len(bs.data), len(other.data))
	for i := 0; i < minLen; i++ {
		if bs.data[i]&^other.data[i] != 0 {
			return false
		}
	}
	// Check remaining words in bs
	for i := minLen; i < len(bs.data); i++ {
		if bs.data[i] != 0 {
			return false
		}
	}
	return true
}

// Equals returns true if the BitSets are equal.
func (bs *BitSet) Equals(other *BitSet) bool {
	if bs.length != other.length {
		return false
	}
	for i := 0; i < len(bs.data); i++ {
		if bs.data[i] != other.data[i] {
			return false
		}
	}
	return true
}

// SetBits returns a slice of all set bit positions.
func (bs *BitSet) SetBits() []int {
	positions := make([]int, 0, bs.Count())
	for i := 0; i < bs.length; {
		next := bs.NextSet(i)
		if next == -1 {
			break
		}
		positions = append(positions, next)
		i = next + 1
	}
	return positions
}

// ClearBits returns a slice of all clear bit positions.
func (bs *BitSet) ClearBits() []int {
	positions := make([]int, 0, bs.length-bs.Count())
	for i := 0; i < bs.length; {
		next := bs.NextClear(i)
		if next == -1 {
			break
		}
		positions = append(positions, next)
		i = next + 1
	}
	return positions
}

// ToBytes converts the BitSet to a byte slice.
func (bs *BitSet) ToBytes() []byte {
	bytes := make([]byte, (bs.length+7)/8)
	for i, word := range bs.data {
		for j := 0; j < 8 && i*8+j < len(bytes); j++ {
			bytes[i*8+j] = byte(word >> (j * 8))
		}
	}
	return bytes
}

// ToUint64Slice converts the BitSet to a []uint64.
func (bs *BitSet) ToUint64Slice() []uint64 {
	result := make([]uint64, len(bs.data))
	copy(result, bs.data)
	return result
}

// String returns a binary string representation.
func (bs *BitSet) String() string {
	if bs.length == 0 {
		return ""
	}
	var sb strings.Builder
	for i := bs.length - 1; i >= 0; i-- {
		if bs.Test(i) {
			sb.WriteByte('1')
		} else {
			sb.WriteByte('0')
		}
	}
	return sb.String()
}

// GoString returns a Go-syntax representation.
func (bs *BitSet) GoString() string {
	return fmt.Sprintf("BitSet{len: %d, data: %v}", bs.length, bs.data)
}

// StringSet returns a set-like string representation (positions of set bits).
func (bs *BitSet) StringSet() string {
	positions := bs.SetBits()
	return fmt.Sprintf("{%v}", positions)
}

// ShiftLeft shifts all bits left by n positions.
func (bs *BitSet) ShiftLeft(n int) error {
	if n < 0 {
		return errors.New("shift amount cannot be negative")
	}
	if n == 0 || bs.length == 0 {
		return nil
	}

	newLength := bs.length + n
	bs.expand(newLength)

	// Shift words
	wordShift := n / 64
	bitShift := n % 64

	for i := len(bs.data) - 1; i >= 0; i-- {
		srcIdx := i - wordShift
		if srcIdx >= 0 {
			bs.data[i] = bs.data[srcIdx] << bitShift
			if bitShift > 0 && srcIdx > 0 {
				bs.data[i] |= bs.data[srcIdx-1] >> (64 - bitShift)
			}
		} else {
			bs.data[i] = 0
		}
	}

	return nil
}

// ShiftRight shifts all bits right by n positions.
func (bs *BitSet) ShiftRight(n int) error {
	if n < 0 {
		return errors.New("shift amount cannot be negative")
	}
	if n == 0 || bs.length == 0 {
		return nil
	}

	if n >= bs.length {
		bs.ClearAll()
		bs.length = 0
		return nil
	}

	wordShift := n / 64
	bitShift := n % 64

	for i := 0; i < len(bs.data); i++ {
		srcIdx := i + wordShift
		if srcIdx < len(bs.data) {
			bs.data[i] = bs.data[srcIdx] >> bitShift
			if bitShift > 0 && srcIdx+1 < len(bs.data) {
				bs.data[i] |= bs.data[srcIdx+1] << (64 - bitShift)
			}
		} else {
			bs.data[i] = 0
		}
	}

	bs.length -= n
	return nil
}

// FirstSet returns the index of the first set bit, or -1 if none.
func (bs *BitSet) FirstSet() int {
	return bs.NextSet(0)
}

// LastSet returns the index of the last set bit, or -1 if none.
func (bs *BitSet) LastSet() int {
	for i := len(bs.data) - 1; i >= 0; i-- {
		if bs.data[i] != 0 {
			bit := 63 - bits.LeadingZeros64(bs.data[i])
			pos := i*64 + bit
			if pos < bs.length {
				return pos
			}
		}
	}
	return -1
}

// Range calls f for each set bit position. Stops if f returns false.
func (bs *BitSet) Range(f func(pos int) bool) {
	for i := 0; i < bs.length; {
		next := bs.NextSet(i)
		if next == -1 {
			break
		}
		if !f(next) {
			break
		}
		i = next + 1
	}
}

// Any returns true if any bit is set (same as !IsEmpty).
func (bs *BitSet) Any() bool {
	return !bs.IsEmpty()
}

// None returns true if no bit is set (same as IsEmpty).
func (bs *BitSet) None() bool {
	return bs.IsEmpty()
}

// All returns true if all bits in range [start, end) are set.
func (bs *BitSet) All(start, end int) bool {
	if start < 0 {
		start = 0
	}
	if end > bs.length {
		end = bs.length
	}
	for i := start; i < end; i++ {
		if !bs.Test(i) {
			return false
		}
	}
	return true
}

// SetRange sets all bits in range [start, end) to 1.
func (bs *BitSet) SetRange(start, end int) error {
	if start < 0 {
		return errors.New("start cannot be negative")
	}
	if start > end {
		return errors.New("start cannot be greater than end")
	}
	bs.expand(end)
	for i := start; i < end; i++ {
		bs.data[i/64] |= 1 << (i % 64)
	}
	return nil
}

// ClearRange clears all bits in range [start, end).
func (bs *BitSet) ClearRange(start, end int) error {
	if start < 0 || end > bs.length {
		return fmt.Errorf("range [%d, %d) out of bounds [0, %d)", start, end, bs.length)
	}
	if start > end {
		return errors.New("start cannot be greater than end")
	}
	for i := start; i < end; i++ {
		bs.data[i/64] &^= 1 << (i % 64)
	}
	return nil
}

// Copy copies bits from src to this BitSet starting at destStart.
func (bs *BitSet) Copy(src *BitSet, destStart int) error {
	if destStart < 0 {
		return errors.New("destStart cannot be negative")
	}
	for i := 0; i < src.length; i++ {
		if src.Test(i) {
			if err := bs.Set(destStart + i); err != nil {
				return err
			}
		}
	}
	return nil
}

// Reverse reverses the order of bits in the BitSet.
func (bs *BitSet) Reverse() {
	if bs.length <= 1 {
		return
	}
	newBs := NewBitSet(bs.length)
	for i := 0; i < bs.length; i++ {
		if bs.Test(i) {
			newBs.Set(bs.length - 1 - i)
		}
	}
	bs.data = newBs.data
}

// Truncate removes n bits from the end of the BitSet.
func (bs *BitSet) Truncate(n int) error {
	if n < 0 {
		return errors.New("n cannot be negative")
	}
	if n >= bs.length {
		bs.length = 0
		bs.data = make([]uint64, 1)
		return nil
	}
	bs.length -= n
	// Clear unused bits
	if rem := bs.length % 64; rem != 0 {
		bs.data[bs.length/64] &= (1 << rem) - 1
	}
	return nil
}

// Helper function for min
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// Helper function for max
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}