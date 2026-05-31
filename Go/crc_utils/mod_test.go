package crc_utils

import (
	"fmt"
	"testing"
)

// TestCRC8 verifies CRC-8 implementation against known check values
func TestCRC8(t *testing.T) {
	crc := CRC8()
	testCases := []struct {
		input    []byte
		expected uint64
	}{
		{[]byte("123456789"), 0xF4},
		{[]byte("hello"), 0x7D},
		{[]byte(""), 0x00},
		{[]byte("\x00\x00\x00\x00"), 0x00},
	}

	for _, tc := range testCases {
		result := crc.Calculate(tc.input)
		if result != tc.expected {
			t.Errorf("CRC8(%q) = 0x%02X, want 0x%02X", string(tc.input), result, tc.expected)
		}
	}
}

// TestCRC16 verifies CRC-16 implementations against known check values
func TestCRC16(t *testing.T) {
	crcs := []*CRC{
		CRC16_CCITT(),
		CRC16_ARC(),
		CRC16_XMODEM(),
		CRC16_X25(),
		CRC16_MODBUS(),
		CRC16_USB(),
	}

	expected := []uint64{
		0x2189, // CCITT
		0xBB3D, // ARC
		0x31C3, // XMODEM
		0x0E53, // X-25
		0x4B37, // MODBUS
		0xB4C8, // USB
	}

	for i, crc := range crcs {
		result := crc.Calculate([]byte("123456789"))
		if result != expected[i] {
			t.Errorf("%T Calculate() = 0x%04X, want 0x%04X", crc, result, expected[i])
		}
	}
}

// TestCRC32 verifies CRC-32 implementation against known check values
func TestCRC32(t *testing.T) {
	crc := CRC32()
	result := crc.Calculate([]byte("123456789"))
	expected := uint64(0xCBF43926)

	if result != expected {
		t.Errorf("CRC32(123456789) = 0x%08X, want 0x%08X", result, expected)
	}
}

// TestCRC32C verifies CRC-32C (Castagnoli) implementation
func TestCRC32C(t *testing.T) {
	crc := CRC32C()
	result := crc.Calculate([]byte("123456789"))
	expected := uint64(0xE3069283)

	if result != expected {
		t.Errorf("CRC32C(123456789) = 0x%08X, want 0x%08X", result, expected)
	}
}

// TestCRC64 verifies CRC-64 implementations
func TestCRC64(t *testing.T) {
	testCases := []struct {
		name     string
		crc      *CRC
		expected uint64
	}{
		{"CRC64_ISO", CRC64_ISO(), 0xB909E8B30248D0D4},
		{"CRC64_ECMA", CRC64_ECMA(), 0x6C40DF5F0B497347},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result := tc.crc.Calculate([]byte("123456789"))
			if result != tc.expected {
				t.Errorf("%s(123456789) = 0x%016X, want 0x%016X", tc.name, result, tc.expected)
			}
		})
	}
}

// TestCRC5 verifies CRC-5 implementations
func TestCRC5(t *testing.T) {
	testCases := []struct {
		name     string
		crc      *CRC
		expected uint64
	}{
		{"CRC5_ITU", CRC5_ITU(), 0x07},
		{"CRC5_USB", CRC5_USB(), 0x19},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result := tc.crc.Calculate([]byte("123456789"))
			if result != tc.expected {
				t.Errorf("%s(123456789) = 0x%02X, want 0x%02X", tc.name, result, tc.expected)
			}
		})
	}
}

// TestCRC8_ROHC verifies CRC-8/ROHC
func TestCRC8_ROHC(t *testing.T) {
	crc := CRC8_ROHC()
	result := crc.Calculate([]byte("123456789"))
	expected := uint64(0xD0)

	if result != expected {
		t.Errorf("CRC8_ROHC(123456789) = 0x%02X, want 0x%02X", result, expected)
	}
}

// TestVerifyCheck tests the VerifyCheck method for all CRC variants
func TestVerifyCheck(t *testing.T) {
	crcs := []struct {
		name string
		crc  *CRC
	}{
		{"CRC5_ITU", CRC5_ITU()},
		{"CRC5_USB", CRC5_USB()},
		{"CRC8", CRC8()},
		{"CRC8_ITU", CRC8_ITU()},
		{"CRC8_ROHC", CRC8_ROHC()},
		{"CRC8_MAXIM", CRC8_MAXIM()},
		{"CRC15_CA", CRC15_CA()},
		{"CRC16_CCITT", CRC16_CCITT()},
		{"CRC16_ARC", CRC16_ARC()},
		{"CRC16_XMODEM", CRC16_XMODEM()},
		{"CRC16_X25", CRC16_X25()},
		{"CRC16_MODBUS", CRC16_MODBUS()},
		{"CRC16_USB", CRC16_USB()},
		{"CRC16_CDMA2000", CRC16_CDMA2000()},
		{"CRC32", CRC32()},
		{"CRC32_BZIP2", CRC32_BZIP2()},
		{"CRC32C", CRC32C()},
		{"CRC32_MPEG2", CRC32_MPEG2()},
		{"CRC64_ISO", CRC64_ISO()},
		{"CRC64_ECMA", CRC64_ECMA()},
		{"CRC64_XZ", CRC64_XZ()},
	}

	for _, tc := range crcs {
		t.Run(tc.name, func(t *testing.T) {
			if !tc.crc.VerifyCheck() {
				t.Errorf("%s VerifyCheck() = false, want true", tc.name)
			}
		})
	}
}

// TestCalculateString tests the CalculateString method
func TestCalculateString(t *testing.T) {
	crc := CRC32()
	result := crc.CalculateString("hello world")
	expected := crc.Calculate([]byte("hello world"))

	if result != expected {
		t.Errorf("CalculateString(hello world) = 0x%08X, want 0x%08X", result, expected)
	}
}

// TestCalculateResult tests the CalculateResult method
func TestCalculateResult(t *testing.T) {
	crc := CRC32()
	data := []byte("test")
	result := crc.CalculateResult(data)

	if result.Value != crc.Calculate(data) {
		t.Errorf("Result.Value mismatch")
	}

	if len(result.Bytes) != 4 {
		t.Errorf("Result.Bytes length = %d, want 4", len(result.Bytes))
	}

	if len(result.Hex) != 8 {
		t.Errorf("Result.Hex length = %d, want 8", len(result.Hex))
	}
}

// TestWidthBits tests the WidthBits method
func TestWidthBits(t *testing.T) {
	testCases := []struct {
		crc      *CRC
		expected uint
	}{
		{CRC5_ITU(), 5},
		{CRC8(), 8},
		{CRC15_CA(), 15},
		{CRC16_CCITT(), 16},
		{CRC32(), 32},
		{CRC64_ECMA(), 64},
	}

	for _, tc := range testCases {
		if tc.crc.WidthBits() != tc.expected {
			t.Errorf("%T.WidthBits() = %d, want %d", tc.crc, tc.crc.WidthBits(), tc.expected)
		}
	}
}

// TestToBytes tests the ToBytes method
func TestToBytes(t *testing.T) {
	crc := CRC32()
	value := uint64(0xDEADBEEF)
	bytes := crc.ToBytes(value)

	if len(bytes) != 4 {
		t.Errorf("len(ToBytes()) = %d, want 4", len(bytes))
	}

	expectedBytes := []byte{0xDE, 0xAD, 0xBE, 0xEF}
	for i, b := range bytes {
		if b != expectedBytes[i] {
			t.Errorf("ToBytes()[%d] = 0x%02X, want 0x%02X", i, b, expectedBytes[i])
		}
	}
}

// TestToHex tests the ToHex method
func TestToHex(t *testing.T) {
	crc := CRC32()
	value := uint64(0xDEADBEEF)
	hex := crc.ToHex(value)

	if hex != "DEADBEEF" {
		t.Errorf("ToHex() = %s, want DEADBEEF", hex)
	}
}

// TestTable tests the Table generation method
func TestTable(t *testing.T) {
	crc := CRC32()
	table := crc.Table()

	if len(table) != 256 {
		t.Errorf("len(Table()) = %d, want 256", len(table))
	}

	// Verify a few known values from the table
	// CRC-32 table entry for 0x00 should be 0x00000000 for non-reflected
	// This is implementation-dependent, just check size and type
	for i, v := range table {
		if v > 0xFFFFFFFF {
			t.Errorf("Table()[%d] = 0x%08X, exceeds 32-bit range", i, v)
		}
	}
}

// TestNewCRC tests creating custom CRC configurations
func TestNewCRC(t *testing.T) {
	// Create a custom CRC-8 with custom parameters
	crc := NewCRC(0x07, 8, 0xFF, 0x00, false, false)

	if crc.width != 8 {
		t.Errorf("width = %d, want 8", crc.width)
	}

	if crc.polynomial != 0x07 {
		t.Errorf("polynomial = 0x%02X, want 0x07", crc.polynomial)
	}
}

// TestBinaryOnesCompliment tests CRC computation with binary data
func TestBinaryOnesCompliment(t *testing.T) {
	crc := CRC32()
	data := []byte{0x00, 0x00, 0x00, 0x00}
	result := crc.Calculate(data)
	// All zeros should produce the init value with XOR
	expected := uint64(0x00000000) // After XOR out with all ones
	if result != expected {
		t.Errorf("CRC32(all zeros) = 0x%08X, want 0x%08X", result, expected)
	}
}

// TestAllBytesCRC8 tests CRC-8 with all possible byte values
func TestAllBytesCRC8(t *testing.T) {
	crc := CRC8()
	data := make([]byte, 256)
	for i := range data {
		data[i] = byte(i)
	}

	result := crc.Calculate(data)
	// Just verify it computes without error and returns a valid 8-bit value
	if result > 0xFF {
		t.Errorf("CRC8(all bytes) = 0x%02X, exceeds 8-bit range", result)
	}
}

// BenchmarkCRC32 benchmarks CRC-32 calculation speed
func BenchmarkCRC32(b *testing.B) {
	crc := CRC32()
	data := []byte("123456789")

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		crc.Calculate(data)
	}
}

// BenchmarkCRC32Large benchmarks CRC-32 with larger data
func BenchmarkCRC32Large(b *testing.B) {
	crc := CRC32()
	data := make([]byte, 1024*1024) // 1MB

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		crc.Calculate(data)
	}
}

// ExampleCRC32 demonstrates usage of the CRC-32 function
func ExampleCRC32() {
	crc := CRC32()
	result := crc.Calculate([]byte("hello world"))
	fmt.Printf("CRC32 of 'hello world' = 0x%08X\n", result)
	// Output: CRC32 of 'hello world' = 0x0D4A2AB6
}