package bitset_utils

import (
	"testing"
)

func TestNewBitSet(t *testing.T) {
	bs := NewBitSet(100)
	if bs == nil {
		t.Fatal("NewBitSet returned nil")
	}
	if bs.Len() != 0 {
		t.Errorf("Expected length 0, got %d", bs.Len())
	}
	if bs.Cap() < 100 {
		t.Errorf("Expected capacity >= 100, got %d", bs.Cap())
	}
}

func TestNewBitSetFromBytes(t *testing.T) {
	tests := []struct {
		name     string
		bytes    []byte
		expected []int
	}{
		{"empty", []byte{}, []int{}},
		{"single byte", []byte{0b10101010}, []int{1, 3, 5, 7}},
		{"two bytes", []byte{0b00001111, 0b11110000}, []int{0, 1, 2, 3, 12, 13, 14, 15}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			bs := NewBitSetFromBytes(tt.bytes)
			if bs.Len() != len(tt.bytes)*8 {
				t.Errorf("Expected length %d, got %d", len(tt.bytes)*8, bs.Len())
			}
			for _, pos := range tt.expected {
				if !bs.Test(pos) {
					t.Errorf("Expected bit %d to be set", pos)
				}
			}
		})
	}
}

func TestNewBitSetFromString(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected []int
		hasError bool
	}{
		{"empty", "", []int{}, false},
		{"single bit", "1", []int{0}, false},
		{"multiple bits", "10110", []int{1, 2, 4}, false},
		{"all ones", "1111", []int{0, 1, 2, 3}, false},
		{"all zeros", "0000", []int{}, false},
		{"invalid char", "10a01", nil, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			bs, err := NewBitSetFromString(tt.input)
			if tt.hasError {
				if err == nil {
					t.Error("Expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Fatalf("Unexpected error: %v", err)
			}
			for _, pos := range tt.expected {
				if !bs.Test(pos) {
					t.Errorf("Expected bit %d to be set", pos)
				}
			}
		})
	}
}

func TestSetAndGet(t *testing.T) {
	bs := NewBitSet(64)

	// Test initial state
	if bs.Test(0) {
		t.Error("Expected bit 0 to be clear initially")
	}

	// Set bit
	if err := bs.Set(5); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if !bs.Test(5) {
		t.Error("Expected bit 5 to be set")
	}

	// Clear bit
	if err := bs.Clear(5); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if bs.Test(5) {
		t.Error("Expected bit 5 to be clear")
	}

	// Toggle bit
	if err := bs.Toggle(10); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if !bs.Test(10) {
		t.Error("Expected bit 10 to be set after toggle")
	}
	if err := bs.Toggle(10); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if bs.Test(10) {
		t.Error("Expected bit 10 to be clear after second toggle")
	}
}

func TestSetAllClearAllFlipAll(t *testing.T) {
	bs := NewBitSet(128)

	bs.SetAll()
	if bs.Count() != 128 {
		t.Errorf("Expected 128 bits set, got %d", bs.Count())
	}

	bs.ClearAll()
	if bs.Count() != 0 {
		t.Errorf("Expected 0 bits set, got %d", bs.Count())
	}

	bs.SetRange(0, 64)
	bs.FlipAll()
	if bs.Count() != 64 {
		t.Errorf("Expected 64 bits set after flip, got %d", bs.Count())
	}
}

func TestCount(t *testing.T) {
	bs := NewBitSet(100)
	if bs.Count() != 0 {
		t.Errorf("Expected count 0, got %d", bs.Count())
	}

	bs.Set(0)
	bs.Set(10)
	bs.Set(50)
	bs.Set(99)
	if bs.Count() != 4 {
		t.Errorf("Expected count 4, got %d", bs.Count())
	}
}

func TestNextSet(t *testing.T) {
	bs := NewBitSet(200)
	bs.Set(10)
	bs.Set(50)
	bs.Set(100)
	bs.Set(150)

	tests := []struct {
		start    int
		expected int
	}{
		{0, 10},
		{10, 10},
		{11, 50},
		{50, 50},
		{51, 100},
		{101, 150},
		{151, -1},
		{200, -1},
	}

	for _, tt := range tests {
		result := bs.NextSet(tt.start)
		if result != tt.expected {
			t.Errorf("NextSet(%d) = %d, want %d", tt.start, result, tt.expected)
		}
	}
}

func TestNextClear(t *testing.T) {
	bs := NewBitSet(64)
	bs.SetAll()

	bs.Clear(5)
	bs.Clear(20)
	bs.Clear(40)

	tests := []struct {
		start    int
		expected int
	}{
		{0, 5},
		{5, 5},
		{6, 20},
		{20, 20},
		{21, 40},
		{41, -1},
	}

	for _, tt := range tests {
		result := bs.NextClear(tt.start)
		if result != tt.expected {
			t.Errorf("NextClear(%d) = %d, want %d", tt.start, result, tt.expected)
		}
	}
}

func TestAndOrXor(t *testing.T) {
	bs1, _ := NewBitSetFromString("1100")
	bs2, _ := NewBitSetFromString("1010")

	// AND
	and := bs1.And(bs2)
	if and.String() != "1000" {
		t.Errorf("AND: expected 1000, got %s", and.String())
	}

	// OR
	or := bs1.Or(bs2)
	if or.String() != "1110" {
		t.Errorf("OR: expected 1110, got %s", or.String())
	}

	// XOR
	xor := bs1.Xor(bs2)
	if xor.String() != "0110" {
		t.Errorf("XOR: expected 0110, got %s", xor.String())
	}
}

func TestAndNot(t *testing.T) {
	bs1, _ := NewBitSetFromString("1111")
	bs2, _ := NewBitSetFromString("1010")

	result := bs1.AndNot(bs2)
	if result.String() != "0101" {
		t.Errorf("AndNot: expected 0101, got %s", result.String())
	}
}

func TestNot(t *testing.T) {
	bs, _ := NewBitSetFromString("1010")
	result := bs.Not()
	if result.String() != "0101" {
		t.Errorf("Not: expected 0101, got %s", result.String())
	}
}

func TestIntersects(t *testing.T) {
	bs1, _ := NewBitSetFromString("1100")
	bs2, _ := NewBitSetFromString("0011")
	bs3, _ := NewBitSetFromString("1000")

	if bs1.Intersects(bs2) {
		t.Error("bs1 should not intersect with bs2")
	}
	if !bs1.Intersects(bs3) {
		t.Error("bs1 should intersect with bs3")
	}
}

func TestSubset(t *testing.T) {
	bs1, _ := NewBitSetFromString("1000")
	bs2, _ := NewBitSetFromString("1100")
	bs3, _ := NewBitSetFromString("0011")

	if !bs1.Subset(bs2) {
		t.Error("bs1 should be subset of bs2")
	}
	if bs2.Subset(bs1) {
		t.Error("bs2 should not be subset of bs1")
	}
	if bs1.Subset(bs3) {
		t.Error("bs1 should not be subset of bs3")
	}
}

func TestEquals(t *testing.T) {
	bs1, _ := NewBitSetFromString("1010")
	bs2, _ := NewBitSetFromString("1010")
	bs3, _ := NewBitSetFromString("1110")

	if !bs1.Equals(bs2) {
		t.Error("bs1 should equal bs2")
	}
	if bs1.Equals(bs3) {
		t.Error("bs1 should not equal bs3")
	}
}

func TestSetBits(t *testing.T) {
	bs := NewBitSet(100)
	bs.Set(0)
	bs.Set(10)
	bs.Set(50)
	bs.Set(99)

	positions := bs.SetBits()
	expected := []int{0, 10, 50, 99}

	if len(positions) != len(expected) {
		t.Fatalf("Expected %d positions, got %d", len(expected), len(positions))
	}

	for i, pos := range positions {
		if pos != expected[i] {
			t.Errorf("Position %d: expected %d, got %d", i, expected[i], pos)
		}
	}
}

func TestToBytes(t *testing.T) {
	bs := NewBitSet(16)
	bs.Set(0)
	bs.Set(7)
	bs.Set(8)
	bs.Set(15)

	bytes := bs.ToBytes()
	if len(bytes) != 2 {
		t.Fatalf("Expected 2 bytes, got %d", len(bytes))
	}

	// Check bit 0 and 7 in first byte
	if bytes[0] != 0x81 {
		t.Errorf("First byte: expected 0x81, got 0x%02x", bytes[0])
	}
	// Check bit 0 and 7 in second byte (which are bits 8 and 15 overall)
	if bytes[1] != 0x81 {
		t.Errorf("Second byte: expected 0x81, got 0x%02x", bytes[1])
	}
}

func TestString(t *testing.T) {
	bs, _ := NewBitSetFromString("10110")
	if bs.String() != "10110" {
		t.Errorf("String: expected 10110, got %s", bs.String())
	}
}

func TestShiftLeft(t *testing.T) {
	bs, _ := NewBitSetFromString("11")
	if err := bs.ShiftLeft(2); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if bs.String() != "1100" {
		t.Errorf("ShiftLeft: expected 1100, got %s", bs.String())
	}
}

func TestShiftRight(t *testing.T) {
	bs, _ := NewBitSetFromString("1100")
	if err := bs.ShiftRight(2); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if bs.String() != "11" {
		t.Errorf("ShiftRight: expected 11, got %s", bs.String())
	}
}

func TestFirstLastSet(t *testing.T) {
	bs := NewBitSet(100)
	bs.Set(10)
	bs.Set(50)
	bs.Set(90)

	if bs.FirstSet() != 10 {
		t.Errorf("FirstSet: expected 10, got %d", bs.FirstSet())
	}
	if bs.LastSet() != 90 {
		t.Errorf("LastSet: expected 90, got %d", bs.LastSet())
	}

	// Empty BitSet
	empty := NewBitSet(10)
	if empty.FirstSet() != -1 {
		t.Errorf("FirstSet on empty: expected -1, got %d", empty.FirstSet())
	}
	if empty.LastSet() != -1 {
		t.Errorf("LastSet on empty: expected -1, got %d", empty.LastSet())
	}
}

func TestRange(t *testing.T) {
	bs := NewBitSet(100)
	bs.Set(10)
	bs.Set(20)
	bs.Set(30)

	var positions []int
	bs.Range(func(pos int) bool {
		positions = append(positions, pos)
		return true
	})

	expected := []int{10, 20, 30}
	if len(positions) != len(expected) {
		t.Fatalf("Expected %d positions, got %d", len(expected), len(positions))
	}

	for i, pos := range positions {
		if pos != expected[i] {
			t.Errorf("Position %d: expected %d, got %d", i, expected[i], pos)
		}
	}

	// Test early termination
	positions = nil
	bs.Range(func(pos int) bool {
		positions = append(positions, pos)
		return len(positions) < 2
	})

	if len(positions) != 2 {
		t.Errorf("Expected 2 positions with early termination, got %d", len(positions))
	}
}

func TestSetRangeClearRange(t *testing.T) {
	bs := NewBitSet(100)

	if err := bs.SetRange(10, 20); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	for i := 10; i < 20; i++ {
		if !bs.Test(i) {
			t.Errorf("Expected bit %d to be set", i)
		}
	}

	if err := bs.ClearRange(12, 18); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	for i := 12; i < 18; i++ {
		if bs.Test(i) {
			t.Errorf("Expected bit %d to be clear", i)
		}
	}
}

func TestReverse(t *testing.T) {
	bs, _ := NewBitSetFromString("10110")
	bs.Reverse()
	if bs.String() != "01101" {
		t.Errorf("Reverse: expected 01101, got %s", bs.String())
	}
}

func TestClone(t *testing.T) {
	bs1, _ := NewBitSetFromString("1010")
	bs2 := bs1.Clone()

	if !bs1.Equals(bs2) {
		t.Error("Clone should be equal to original")
	}

	bs2.Set(5)
	if bs1.Equals(bs2) {
		t.Error("Modifying clone should not affect original")
	}
}

func TestTruncate(t *testing.T) {
	// Truncate removes n bits from the end (highest positions)
	bs, _ := NewBitSetFromString("00001111") // Bits 0-3 are set
	if err := bs.Truncate(4); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if bs.String() != "1111" {
		t.Errorf("Truncate: expected 1111, got %s", bs.String())
	}

	// Test truncate that removes all bits
	bs2, _ := NewBitSetFromString("10110")
	if err := bs2.Truncate(5); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if bs2.String() != "" {
		t.Errorf("Truncate all: expected empty, got %s", bs2.String())
	}
}

func TestAllAnyNoneIsEmptyIsFull(t *testing.T) {
	bs := NewBitSet(10)

	if !bs.IsEmpty() {
		t.Error("New BitSet should be empty")
	}
	if !bs.None() {
		t.Error("None() should return true for empty BitSet")
	}
	if bs.Any() {
		t.Error("Any() should return false for empty BitSet")
	}
	if bs.IsFull() {
		t.Error("IsFull() should return false for empty BitSet")
	}

	bs.SetAll()

	if bs.IsEmpty() {
		t.Error("SetAll BitSet should not be empty")
	}
	if !bs.IsFull() {
		t.Error("IsFull() should return true after SetAll")
	}
	if !bs.Any() {
		t.Error("Any() should return true after SetAll")
	}

	bs.SetRange(2, 5)
	if !bs.All(2, 5) {
		t.Error("All(2, 5) should return true for range [2, 5)")
	}
}

func TestNegativeAndEdgeCases(t *testing.T) {
	bs := NewBitSet(10)

	// Negative index
	if err := bs.Set(-1); err == nil {
		t.Error("Expected error for negative index in Set")
	}
	if err := bs.Clear(-1); err == nil {
		t.Error("Expected error for negative index in Clear")
	}
	if err := bs.Toggle(-1); err == nil {
		t.Error("Expected error for negative index in Toggle")
	}
	_, err := bs.Get(-1)
	if err == nil {
		t.Error("Expected error for negative index in Get")
	}

	// Out of range
	if err := bs.Clear(100); err == nil {
		t.Error("Expected error for out of range in Clear")
	}
	_, err = bs.Get(100)
	if err == nil {
		t.Error("Expected error for out of range in Get")
	}

	// Empty BitSet operations
	empty := NewBitSet(0)
	if empty.FirstSet() != -1 {
		t.Error("FirstSet on empty should return -1")
	}
}

func BenchmarkSetAndClear(b *testing.B) {
	bs := NewBitSet(10000)
	for i := 0; i < b.N; i++ {
		bs.Set(i % 10000)
		bs.Clear(i % 10000)
	}
}

func BenchmarkCount(b *testing.B) {
	bs := NewBitSet(10000)
	for i := 0; i < 5000; i += 2 {
		bs.Set(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bs.Count()
	}
}

func BenchmarkNextSet(b *testing.B) {
	bs := NewBitSet(10000)
	for i := 0; i < 1000; i++ {
		bs.Set(i * 10)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bs.NextSet(0)
	}
}

func BenchmarkAnd(b *testing.B) {
	bs1 := NewBitSet(10000)
	bs2 := NewBitSet(10000)
	for i := 0; i < 5000; i++ {
		bs1.Set(i * 2)
		bs2.Set(i * 3)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bs1.And(bs2)
	}
}