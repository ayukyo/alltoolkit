// Package bitmask_utils provides a comprehensive bitmask utility library
// for efficient bit manipulation operations with zero external dependencies.
package bitmask_utils

import (
	"errors"
	"fmt"
	"strings"
)

// BitMask represents a bitmask with efficient bit manipulation operations.
type BitMask struct {
	bits []uint64
	size int // total number of bits
}

// NewBitMask creates a new BitMask with the specified number of bits.
func NewBitMask(size int) *BitMask {
	if size < 0 {
		size = 0
	}
	blocks := (size + 63) / 64
	if blocks == 0 {
		blocks = 1
	}
	return &BitMask{
		bits: make([]uint64, blocks),
		size: size,
	}
}

// NewBitMaskFromUint64 creates a BitMask from a uint64 value.
func NewBitMaskFromUint64(value uint64) *BitMask {
	bm := NewBitMask(64)
	bm.bits[0] = value
	return bm
}

// NewBitMaskFromBytes creates a BitMask from a byte slice.
func NewBitMaskFromBytes(data []byte) *BitMask {
	size := len(data) * 8
	bm := NewBitMask(size)
	for i, b := range data {
		bm.bits[i/8] |= uint64(b) << ((i % 8) * 8)
	}
	return bm
}

// Clone creates a deep copy of the BitMask.
func (bm *BitMask) Clone() *BitMask {
	bits := make([]uint64, len(bm.bits))
	copy(bits, bm.bits)
	return &BitMask{bits: bits, size: bm.size}
}

// Set sets the bit at the specified position.
func (bm *BitMask) Set(pos int) error {
	if pos < 0 || pos >= bm.size {
		return fmt.Errorf("position %d out of range [0, %d)", pos, bm.size)
	}
	bm.bits[pos/64] |= (1 << (pos % 64))
	return nil
}

// Clear clears the bit at the specified position.
func (bm *BitMask) Clear(pos int) error {
	if pos < 0 || pos >= bm.size {
		return fmt.Errorf("position %d out of range [0, %d)", pos, bm.size)
	}
	bm.bits[pos/64] &^= (1 << (pos % 64))
	return nil
}

// Toggle toggles the bit at the specified position.
func (bm *BitMask) Toggle(pos int) error {
	if pos < 0 || pos >= bm.size {
		return fmt.Errorf("position %d out of range [0, %d)", pos, bm.size)
	}
	bm.bits[pos/64] ^= (1 << (pos % 64))
	return nil
}

// Get returns the value of the bit at the specified position.
func (bm *BitMask) Get(pos int) (bool, error) {
	if pos < 0 || pos >= bm.size {
		return false, fmt.Errorf("position %d out of range [0, %d)", pos, bm.size)
	}
	return (bm.bits[pos/64] & (1 << (pos % 64))) != 0, nil
}

// IsSet checks if the bit at the specified position is set.
func (bm *BitMask) IsSet(pos int) bool {
	val, _ := bm.Get(pos)
	return val
}

// IsClear checks if the bit at the specified position is clear.
func (bm *BitMask) IsClear(pos int) bool {
	return !bm.IsSet(pos)
}

// SetAll sets all bits to 1.
func (bm *BitMask) SetAll() {
	for i := range bm.bits {
		bm.bits[i] = ^uint64(0)
	}
	// Clear unused bits in the last block
	if bm.size > 0 {
		lastBlockBits := bm.size % 64
		if lastBlockBits > 0 && len(bm.bits) > 0 {
			bm.bits[len(bm.bits)-1] &= (1 << lastBlockBits) - 1
		}
	}
}

// ClearAll clears all bits to 0.
func (bm *BitMask) ClearAll() {
	for i := range bm.bits {
		bm.bits[i] = 0
	}
}

// CountOnes returns the number of set bits (population count).
func (bm *BitMask) CountOnes() int {
	count := 0
	for _, block := range bm.bits {
		count += popcount(block)
	}
	return count
}

// CountZeros returns the number of clear bits.
func (bm *BitMask) CountZeros() int {
	return bm.size - bm.CountOnes()
}

// popcount returns the number of set bits in a uint64.
func popcount(x uint64) int {
	// Brian Kernighan's algorithm
	count := 0
	for x != 0 {
		x &= x - 1
		count++
	}
	return count
}

// FindFirstSet finds the position of the first set bit.
// Returns -1 if no bit is set.
func (bm *BitMask) FindFirstSet() int {
	for i, block := range bm.bits {
		if block != 0 {
			return i*64 + trailingZeros(block)
		}
	}
	return -1
}

// FindFirstClear finds the position of the first clear bit.
// Returns -1 if all bits are set.
func (bm *BitMask) FindFirstClear() int {
	for i, block := range bm.bits {
		if block != ^uint64(0) {
			pos := i*64 + trailingZeros(^block)
			if pos < bm.size {
				return pos
			}
		}
	}
	return -1
}

// trailingZeros returns the number of trailing zero bits.
func trailingZeros(x uint64) int {
	if x == 0 {
		return 64
	}
	n := 0
	if (x & 0xFFFFFFFF) == 0 {
		n += 32
		x >>= 32
	}
	if (x & 0xFFFF) == 0 {
		n += 16
		x >>= 16
	}
	if (x & 0xFF) == 0 {
		n += 8
		x >>= 8
	}
	if (x & 0x0F) == 0 {
		n += 4
		x >>= 4
	}
	if (x & 0x03) == 0 {
		n += 2
		x >>= 2
	}
	if (x & 0x01) == 0 {
		n += 1
	}
	return n
}

// FindLastSet finds the position of the last set bit.
// Returns -1 if no bit is set.
func (bm *BitMask) FindLastSet() int {
	for i := len(bm.bits) - 1; i >= 0; i-- {
		if bm.bits[i] != 0 {
			return i*64 + highestBitPos(bm.bits[i])
		}
	}
	return -1
}

// highestBitPos returns the position of the highest set bit (0-63).
// Returns -1 if x is 0.
func highestBitPos(x uint64) int {
	if x == 0 {
		return -1
	}
	pos := 0
	if x >= (1 << 32) {
		x >>= 32
		pos += 32
	}
	if x >= (1 << 16) {
		x >>= 16
		pos += 16
	}
	if x >= (1 << 8) {
		x >>= 8
		pos += 8
	}
	if x >= (1 << 4) {
		x >>= 4
		pos += 4
	}
	if x >= (1 << 2) {
		x >>= 2
		pos += 2
	}
	if x >= (1 << 1) {
		pos += 1
	}
	return pos
}

// And performs bitwise AND with another BitMask.
func (bm *BitMask) And(other *BitMask) error {
	if bm.size != other.size {
		return errors.New("bitmask sizes must match")
	}
	for i := range bm.bits {
		bm.bits[i] &= other.bits[i]
	}
	return nil
}

// Or performs bitwise OR with another BitMask.
func (bm *BitMask) Or(other *BitMask) error {
	if bm.size != other.size {
		return errors.New("bitmask sizes must match")
	}
	for i := range bm.bits {
		bm.bits[i] |= other.bits[i]
	}
	return nil
}

// Xor performs bitwise XOR with another BitMask.
func (bm *BitMask) Xor(other *BitMask) error {
	if bm.size != other.size {
		return errors.New("bitmask sizes must match")
	}
	for i := range bm.bits {
		bm.bits[i] ^= other.bits[i]
	}
	return nil
}

// Not performs bitwise NOT (inverts all bits).
func (bm *BitMask) Not() {
	for i := range bm.bits {
		bm.bits[i] = ^bm.bits[i]
	}
	// Clear unused bits in the last block
	if bm.size > 0 {
		lastBlockBits := bm.size % 64
		if lastBlockBits > 0 && len(bm.bits) > 0 {
			bm.bits[len(bm.bits)-1] &= (1 << lastBlockBits) - 1
		}
	}
}

// LeftShift shifts all bits to the left by n positions.
func (bm *BitMask) LeftShift(n int) {
	if n <= 0 || bm.size == 0 {
		return
	}
	if n >= bm.size {
		bm.ClearAll()
		return
	}

	// Shift complete blocks
	blockShift := n / 64
	bitShift := n % 64

	// Shift blocks
	for i := len(bm.bits) - 1; i >= 0; i-- {
		src := i - blockShift
		if src < 0 {
			bm.bits[i] = 0
		} else if bitShift == 0 {
			bm.bits[i] = bm.bits[src]
		} else {
			var result uint64
			result = bm.bits[src] << bitShift
			if src > 0 {
				result |= bm.bits[src-1] >> (64 - bitShift)
			}
			bm.bits[i] = result
		}
	}

	// Clear unused bits in the last block
	lastBlockBits := bm.size % 64
	if lastBlockBits > 0 && len(bm.bits) > 0 {
		bm.bits[len(bm.bits)-1] &= (1 << lastBlockBits) - 1
	}
}

// RightShift shifts all bits to the right by n positions.
func (bm *BitMask) RightShift(n int) {
	if n <= 0 || bm.size == 0 {
		return
	}
	if n >= bm.size {
		bm.ClearAll()
		return
	}

	// Shift complete blocks
	blockShift := n / 64
	bitShift := n % 64

	// Shift blocks
	for i := 0; i < len(bm.bits); i++ {
		src := i + blockShift
		if src >= len(bm.bits) {
			bm.bits[i] = 0
		} else if bitShift == 0 {
			bm.bits[i] = bm.bits[src]
		} else {
			var result uint64
			result = bm.bits[src] >> bitShift
			if src+1 < len(bm.bits) {
				result |= bm.bits[src+1] << (64 - bitShift)
			}
			bm.bits[i] = result
		}
	}
}

// RotateLeft rotates bits to the left by n positions.
func (bm *BitMask) RotateLeft(n int) {
	if bm.size == 0 {
		return
	}
	n = n % bm.size
	if n < 0 {
		n += bm.size
	}
	if n == 0 {
		return
	}

	temp := bm.Clone()
	bm.ClearAll()
	for i := 0; i < bm.size; i++ {
		if val, _ := temp.Get(i); val {
			newPos := (i + n) % bm.size
			bm.Set(newPos)
		}
	}
}

// RotateRight rotates bits to the right by n positions.
func (bm *BitMask) RotateRight(n int) {
	if bm.size == 0 {
		return
	}
	n = n % bm.size
	if n < 0 {
		n += bm.size
	}
	bm.RotateLeft(bm.size - n)
}

// Reverse reverses all bits.
func (bm *BitMask) Reverse() {
	if bm.size <= 1 {
		return
	}

	result := NewBitMask(bm.size)
	for i := 0; i < bm.size; i++ {
		if val, _ := bm.Get(i); val {
			result.Set(bm.size - 1 - i)
		}
	}
	bm.bits = result.bits
}

// IsEmpty checks if all bits are clear.
func (bm *BitMask) IsEmpty() bool {
	for _, block := range bm.bits {
		if block != 0 {
			return false
		}
	}
	return true
}

// IsFull checks if all bits are set.
func (bm *BitMask) IsFull() bool {
	return bm.CountOnes() == bm.size
}

// Equals checks if two BitMasks are equal.
func (bm *BitMask) Equals(other *BitMask) bool {
	if bm.size != other.size {
		return false
	}
	for i := range bm.bits {
		if bm.bits[i] != other.bits[i] {
			return false
		}
	}
	return true
}

// Intersects checks if any bit is set in both BitMasks.
func (bm *BitMask) Intersects(other *BitMask) bool {
	minBlocks := min(len(bm.bits), len(other.bits))
	for i := 0; i < minBlocks; i++ {
		if bm.bits[i]&other.bits[i] != 0 {
			return true
		}
	}
	return false
}

// SubsetOf checks if all set bits in this BitMask are also set in other.
func (bm *BitMask) SubsetOf(other *BitMask) bool {
	minBlocks := min(len(bm.bits), len(other.bits))
	for i := 0; i < minBlocks; i++ {
		if bm.bits[i]&^other.bits[i] != 0 {
			return false
		}
	}
	// Check remaining blocks in bm
	for i := minBlocks; i < len(bm.bits); i++ {
		if bm.bits[i] != 0 {
			return false
		}
	}
	return true
}

// Size returns the total number of bits.
func (bm *BitMask) Size() int {
	return bm.size
}

// ToUint64 converts the BitMask to uint64 (only first 64 bits).
func (bm *BitMask) ToUint64() uint64 {
	if len(bm.bits) == 0 {
		return 0
	}
	return bm.bits[0]
}

// ToBytes converts the BitMask to a byte slice.
func (bm *BitMask) ToBytes() []byte {
	result := make([]byte, len(bm.bits)*8)
	for i, block := range bm.bits {
		for j := 0; j < 8; j++ {
			result[i*8+j] = byte(block >> (j * 8))
		}
	}
	return result
}

// ToBinaryString returns a binary string representation.
func (bm *BitMask) ToBinaryString() string {
	var sb strings.Builder
	for i := bm.size - 1; i >= 0; i-- {
		if val, _ := bm.Get(i); val {
			sb.WriteByte('1')
		} else {
			sb.WriteByte('0')
		}
	}
	return sb.String()
}

// String returns a string representation of the BitMask.
func (bm *BitMask) String() string {
	return fmt.Sprintf("BitMask{size: %d, bits: %s}", bm.size, bm.ToBinaryString())
}

// GoString returns a Go syntax representation.
func (bm *BitMask) GoString() string {
	return fmt.Sprintf("bitmask_utils.NewBitMask(%d).SetBits(%v)", bm.size, bm.GetSetBits())
}

// GetSetBits returns a slice of positions of all set bits.
func (bm *BitMask) GetSetBits() []int {
	var result []int
	for i := 0; i < bm.size; i++ {
		if val, _ := bm.Get(i); val {
			result = append(result, i)
		}
	}
	return result
}

// GetClearBits returns a slice of positions of all clear bits.
func (bm *BitMask) GetClearBits() []int {
	var result []int
	for i := 0; i < bm.size; i++ {
		if val, _ := bm.Get(i); !val {
			result = append(result, i)
		}
	}
	return result
}

// SetBits sets multiple bits at once.
func (bm *BitMask) SetBits(positions []int) error {
	for _, pos := range positions {
		if err := bm.Set(pos); err != nil {
			return err
		}
	}
	return nil
}

// ClearBits clears multiple bits at once.
func (bm *BitMask) ClearBits(positions []int) error {
	for _, pos := range positions {
		if err := bm.Clear(pos); err != nil {
			return err
		}
	}
	return nil
}

// SetRange sets bits in a range [start, end).
func (bm *BitMask) SetRange(start, end int) error {
	if start < 0 || end > bm.size || start > end {
		return fmt.Errorf("invalid range [%d, %d) for size %d", start, end, bm.size)
	}
	for i := start; i < end; i++ {
		bm.bits[i/64] |= (1 << (i % 64))
	}
	return nil
}

// ClearRange clears bits in a range [start, end).
func (bm *BitMask) ClearRange(start, end int) error {
	if start < 0 || end > bm.size || start > end {
		return fmt.Errorf("invalid range [%d, %d) for size %d", start, end, bm.size)
	}
	for i := start; i < end; i++ {
		bm.bits[i/64] &^= (1 << (i % 64))
	}
	return nil
}

// GetRange returns a new BitMask containing bits from the specified range.
func (bm *BitMask) GetRange(start, end int) (*BitMask, error) {
	if start < 0 || end > bm.size || start > end {
		return nil, fmt.Errorf("invalid range [%d, %d) for size %d", start, end, bm.size)
	}
	result := NewBitMask(end - start)
	for i := start; i < end; i++ {
		if val, _ := bm.Get(i); val {
			result.Set(i - start)
		}
	}
	return result, nil
}

// Fill sets bits according to a pattern.
// Pattern is repeated to fill the bitmask.
func (bm *BitMask) Fill(pattern uint64) {
	for i := range bm.bits {
		bm.bits[i] = pattern
	}
	// Clear unused bits in the last block
	if bm.size > 0 {
		lastBlockBits := bm.size % 64
		if lastBlockBits > 0 && len(bm.bits) > 0 {
			bm.bits[len(bm.bits)-1] &= (1 << lastBlockBits) - 1
		}
	}
}

// CopyFrom copies bits from another BitMask.
func (bm *BitMask) CopyFrom(other *BitMask) {
	minBlocks := min(len(bm.bits), len(other.bits))
	for i := 0; i < minBlocks; i++ {
		bm.bits[i] = other.bits[i]
	}
	// Clear remaining blocks
	for i := minBlocks; i < len(bm.bits); i++ {
		bm.bits[i] = 0
	}
}

// Swap swaps the bits at two positions.
func (bm *BitMask) Swap(pos1, pos2 int) error {
	if pos1 < 0 || pos1 >= bm.size || pos2 < 0 || pos2 >= bm.size {
		return fmt.Errorf("position out of range")
	}
	val1, _ := bm.Get(pos1)
	val2, _ := bm.Get(pos2)
	if val1 != val2 {
		bm.Toggle(pos1)
		bm.Toggle(pos2)
	}
	return nil
}

// NextPermutation generates the next permutation of set bits.
// This is useful for generating all combinations.
// Returns false if this is the last permutation.
func (bm *BitMask) NextPermutation() bool {
	// Find the first clear bit after a set bit
	first := bm.FindFirstClear()
	if first == -1 || first == 0 {
		return false
	}

	// Count set bits before first clear
	count := 0
	for i := 0; i < first; i++ {
		if val, _ := bm.Get(i); val {
			count++
		}
	}

	// Clear all bits before first clear
	bm.ClearRange(0, first)

	// Set bits starting from 0
	for i := 0; i < count-1; i++ {
		bm.Set(i)
	}

	// Set the first clear bit
	bm.Set(first)

	return true
}

// PrevPermutation generates the previous permutation of set bits.
// Returns false if this is the first permutation.
func (bm *BitMask) PrevPermutation() bool {
	// Find the first set bit after a clear bit
	firstSet := -1
	for i := 1; i < bm.size; i++ {
		if val, _ := bm.Get(i); val {
			if prevVal, _ := bm.Get(i - 1); !prevVal {
				firstSet = i
				break
			}
		}
	}

	if firstSet == -1 {
		return false
	}

	// Count set bits at and after firstSet
	count := 0
	for i := firstSet; i < bm.size; i++ {
		if val, _ := bm.Get(i); val {
			count++
		}
	}

	// Clear bits from firstSet onwards
	bm.ClearRange(firstSet, bm.size)

	// Set bits at the end
	for i := 0; i < count; i++ {
		bm.Set(firstSet - 1 - i)
	}

	return true
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}