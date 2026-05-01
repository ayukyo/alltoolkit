package bitmask_utils

import (
	"testing"
)

func TestNewBitMask(t *testing.T) {
	bm := NewBitMask(64)
	if bm.Size() != 64 {
		t.Errorf("Expected size 64, got %d", bm.Size())
	}
	if !bm.IsEmpty() {
		t.Error("Expected empty bitmask")
	}

	// Test with non-multiple of 64
	bm = NewBitMask(100)
	if bm.Size() != 100 {
		t.Errorf("Expected size 100, got %d", bm.Size())
	}

	// Test with zero size
	bm = NewBitMask(0)
	if bm.Size() != 0 {
		t.Errorf("Expected size 0, got %d", bm.Size())
	}
}

func TestNewBitMaskFromUint64(t *testing.T) {
	bm := NewBitMaskFromUint64(0b1010)
	if bm.Size() != 64 {
		t.Errorf("Expected size 64, got %d", bm.Size())
	}
	if !bm.IsSet(1) {
		t.Error("Bit 1 should be set")
	}
	if !bm.IsSet(3) {
		t.Error("Bit 3 should be set")
	}
	if bm.IsSet(0) {
		t.Error("Bit 0 should be clear")
	}
}

func TestSetAndGet(t *testing.T) {
	bm := NewBitMask(64)

	// Test setting and getting bits
	bm.Set(0)
	if !bm.IsSet(0) {
		t.Error("Bit 0 should be set")
	}

	bm.Set(63)
	if !bm.IsSet(63) {
		t.Error("Bit 63 should be set")
	}

	// Test error cases
	err := bm.Set(-1)
	if err == nil {
		t.Error("Expected error for negative position")
	}
	err = bm.Set(64)
	if err == nil {
		t.Error("Expected error for out of range position")
	}
}

func TestClear(t *testing.T) {
	bm := NewBitMask(64)
	bm.Set(5)
	if !bm.IsSet(5) {
		t.Error("Bit 5 should be set")
	}
	bm.Clear(5)
	if bm.IsSet(5) {
		t.Error("Bit 5 should be clear")
	}
}

func TestToggle(t *testing.T) {
	bm := NewBitMask(64)
	if bm.IsSet(10) {
		t.Error("Bit 10 should be clear initially")
	}
	bm.Toggle(10)
	if !bm.IsSet(10) {
		t.Error("Bit 10 should be set after toggle")
	}
	bm.Toggle(10)
	if bm.IsSet(10) {
		t.Error("Bit 10 should be clear after second toggle")
	}
}

func TestSetAllAndClearAll(t *testing.T) {
	bm := NewBitMask(64)
	bm.SetAll()
	if !bm.IsFull() {
		t.Error("Expected all bits to be set")
	}
	if bm.CountOnes() != 64 {
		t.Errorf("Expected 64 ones, got %d", bm.CountOnes())
	}

	bm.ClearAll()
	if !bm.IsEmpty() {
		t.Error("Expected all bits to be clear")
	}
	if bm.CountOnes() != 0 {
		t.Errorf("Expected 0 ones, got %d", bm.CountOnes())
	}
}

func TestCountOnes(t *testing.T) {
	bm := NewBitMask(64)
	bm.Set(0)
	bm.Set(1)
	bm.Set(5)
	bm.Set(10)
	bm.Set(63)

	if bm.CountOnes() != 5 {
		t.Errorf("Expected 5 ones, got %d", bm.CountOnes())
	}
}

func TestFindFirstSet(t *testing.T) {
	bm := NewBitMask(64)
	if bm.FindFirstSet() != -1 {
		t.Error("Expected -1 for empty bitmask")
	}

	bm.Set(5)
	bm.Set(10)
	if bm.FindFirstSet() != 5 {
		t.Errorf("Expected first set at 5, got %d", bm.FindFirstSet())
	}

	bm.Clear(5)
	if bm.FindFirstSet() != 10 {
		t.Errorf("Expected first set at 10, got %d", bm.FindFirstSet())
	}
}

func TestFindFirstClear(t *testing.T) {
	bm := NewBitMask(8)
	bm.SetAll()
	if bm.FindFirstClear() != -1 {
		t.Error("Expected -1 for full bitmask")
	}

	bm.Clear(3)
	if bm.FindFirstClear() != 3 {
		t.Errorf("Expected first clear at 3, got %d", bm.FindFirstClear())
	}
}

func TestFindLastSet(t *testing.T) {
	bm := NewBitMask(64)
	bm.Set(5)
	bm.Set(10)
	bm.Set(63)

	if bm.FindLastSet() != 63 {
		t.Errorf("Expected last set at 63, got %d", bm.FindLastSet())
	}

	bm.Clear(63)
	if bm.FindLastSet() != 10 {
		t.Errorf("Expected last set at 10, got %d", bm.FindLastSet())
	}
}

func TestAndOrXor(t *testing.T) {
	bm1 := NewBitMaskFromUint64(0b1100)
	bm2 := NewBitMaskFromUint64(0b1010)

	bm1.And(bm2)
	if bm1.ToUint64() != 0b1000 {
		t.Errorf("AND result: expected 0b1000, got %b", bm1.ToUint64())
	}

	bm1 = NewBitMaskFromUint64(0b1100)
	bm1.Or(bm2)
	if bm1.ToUint64() != 0b1110 {
		t.Errorf("OR result: expected 0b1110, got %b", bm1.ToUint64())
	}

	bm1 = NewBitMaskFromUint64(0b1100)
	bm1.Xor(bm2)
	if bm1.ToUint64() != 0b0110 {
		t.Errorf("XOR result: expected 0b0110, got %b", bm1.ToUint64())
	}
}

func TestNot(t *testing.T) {
	bm := NewBitMask(4)
	bm.Set(0)
	bm.Set(3)
	bm.Not()

	if !bm.IsSet(1) || !bm.IsSet(2) {
		t.Error("Not operation failed")
	}
	if bm.IsSet(0) || bm.IsSet(3) {
		t.Error("Not operation failed")
	}
}

func TestShift(t *testing.T) {
	bm := NewBitMaskFromUint64(0b101)
	bm.LeftShift(1)
	if bm.ToUint64() != 0b1010 {
		t.Errorf("Left shift: expected 0b1010, got %b", bm.ToUint64())
	}

	bm = NewBitMaskFromUint64(0b1010)
	bm.RightShift(1)
	if bm.ToUint64() != 0b101 {
		t.Errorf("Right shift: expected 0b101, got %b", bm.ToUint64())
	}
}

func TestRotate(t *testing.T) {
	bm := NewBitMask(8)
	bm.Set(0)
	bm.Set(7)

	bm.RotateLeft(1)
	if !bm.IsSet(1) || !bm.IsSet(0) {
		t.Errorf("RotateLeft failed: got %s", bm.ToBinaryString())
	}

	bm = NewBitMask(8)
	bm.Set(0)
	bm.Set(7)
	bm.RotateRight(1)
	if !bm.IsSet(6) || !bm.IsSet(7) {
		t.Errorf("RotateRight failed: got %s", bm.ToBinaryString())
	}
}

func TestReverse(t *testing.T) {
	bm := NewBitMask(8)
	bm.Set(0)
	bm.Set(7)
	bm.Reverse()

	if !bm.IsSet(0) || !bm.IsSet(7) {
		t.Error("Reverse failed")
	}
	if bm.IsSet(1) || bm.IsSet(6) {
		t.Error("Reverse should swap positions")
	}
}

func TestIntersects(t *testing.T) {
	bm1 := NewBitMaskFromUint64(0b1100)
	bm2 := NewBitMaskFromUint64(0b1010)
	bm3 := NewBitMaskFromUint64(0b0011)

	if !bm1.Intersects(bm2) {
		t.Error("bm1 and bm2 should intersect")
	}
	if bm1.Intersects(bm3) {
		t.Error("bm1 and bm3 should not intersect")
	}
}

func TestSubsetOf(t *testing.T) {
	bm1 := NewBitMaskFromUint64(0b1000)
	bm2 := NewBitMaskFromUint64(0b1100)

	if !bm1.SubsetOf(bm2) {
		t.Error("bm1 should be subset of bm2")
	}
	if bm2.SubsetOf(bm1) {
		t.Error("bm2 should not be subset of bm1")
	}
}

func TestToBinaryString(t *testing.T) {
	bm := NewBitMask(8)
	bm.Set(0)
	bm.Set(7)
	expected := "10000001"
	if bm.ToBinaryString() != expected {
		t.Errorf("Expected %s, got %s", expected, bm.ToBinaryString())
	}
}

func TestGetSetBits(t *testing.T) {
	bm := NewBitMask(16)
	bm.Set(0)
	bm.Set(5)
	bm.Set(15)

	bits := bm.GetSetBits()
	if len(bits) != 3 {
		t.Errorf("Expected 3 bits, got %d", len(bits))
	}
	expected := []int{0, 5, 15}
	for i, b := range expected {
		if bits[i] != b {
			t.Errorf("Expected bit %d at position %d, got %d", b, i, bits[i])
		}
	}
}

func TestSetRange(t *testing.T) {
	bm := NewBitMask(16)
	bm.SetRange(5, 10)

	for i := 5; i < 10; i++ {
		if !bm.IsSet(i) {
			t.Errorf("Bit %d should be set", i)
		}
	}
	for i := 0; i < 5; i++ {
		if bm.IsSet(i) {
			t.Errorf("Bit %d should be clear", i)
		}
	}
}

func TestCopyFrom(t *testing.T) {
	bm1 := NewBitMask(64)
	bm2 := NewBitMask(64)
	bm2.Set(5)
	bm2.Set(10)

	bm1.CopyFrom(bm2)

	if !bm1.Equals(bm2) {
		t.Error("CopyFrom failed")
	}
}

func TestClone(t *testing.T) {
	bm1 := NewBitMask(64)
	bm1.Set(5)
	bm2 := bm1.Clone()

	bm1.Clear(5)
	if !bm2.IsSet(5) {
		t.Error("Clone should be independent")
	}
}

func TestSwap(t *testing.T) {
	bm := NewBitMask(16)
	bm.Set(0)
	bm.Clear(5)
	bm.Swap(0, 5)

	if bm.IsSet(0) {
		t.Error("Bit 0 should be clear after swap")
	}
	if !bm.IsSet(5) {
		t.Error("Bit 5 should be set after swap")
	}
}

func TestLargeBitMask(t *testing.T) {
	// Test with a large bitmask (> 64 bits)
	bm := NewBitMask(256)

	bm.Set(0)
	bm.Set(64)
	bm.Set(128)
	bm.Set(255)

	if bm.CountOnes() != 4 {
		t.Errorf("Expected 4 ones, got %d", bm.CountOnes())
	}

	if bm.FindFirstSet() != 0 {
		t.Errorf("Expected first set at 0, got %d", bm.FindFirstSet())
	}

	if bm.FindLastSet() != 255 {
		t.Errorf("Expected last set at 255, got %d", bm.FindLastSet())
	}
}

func TestToBytes(t *testing.T) {
	bm := NewBitMaskFromUint64(0x0102030405060708)
	bytes := bm.ToBytes()

	if len(bytes) != 8 {
		t.Errorf("Expected 8 bytes, got %d", len(bytes))
	}
}

func TestEquals(t *testing.T) {
	bm1 := NewBitMask(64)
	bm2 := NewBitMask(64)
	bm3 := NewBitMask(32)

	if !bm1.Equals(bm2) {
		t.Error("Empty bitmasks should be equal")
	}

	bm1.Set(5)
	bm2.Set(5)
	if !bm1.Equals(bm2) {
		t.Error("Same bitmasks should be equal")
	}

	if bm1.Equals(bm3) {
		t.Error("Different size bitmasks should not be equal")
	}
}

func BenchmarkCountOnes(b *testing.B) {
	bm := NewBitMask(1024)
	bm.SetAll()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bm.CountOnes()
	}
}

func BenchmarkSet(b *testing.B) {
	bm := NewBitMask(1024)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bm.Set(i % 1024)
	}
}

func BenchmarkFindFirstSet(b *testing.B) {
	bm := NewBitMask(1024)
	bm.Set(512)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bm.FindFirstSet()
	}
}