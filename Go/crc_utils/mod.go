// Package crc_utils provides implementations of various CRC (Cyclic Redundancy Check)
// algorithms. CRC is a type of hash function used for detecting errors in data storage
// and transmission. This package includes popular CRC variants used in practice.
//
// Reference: https://en.wikipedia.org/wiki/Cyclic_redundancy_check
package crc_utils

// ============================================================================
// Public Types
// ============================================================================

// CRC represents a CRC calculator state
type CRC struct {
	// The polynomial
	polynomial uint64

	// Bit width of the CRC
	width uint

	// Initial value for the CRC
	initVal uint64

	// XOR output with this value at the end
	xorOut uint64

	// Reflect input bytes (bit order reversed)
	refIn bool

	// Reflect output bytes
	refOut bool

	// Width mask (e.g., 0xFF for width=8)
	widthMask uint64

	// Check value for the given CRC configuration
	check uint64
}

// Result represents the result of a CRC computation
type Result struct {
	// The computed CRC value
	Value uint64

	// Bytes representation (MSB first)
	Bytes []byte

	// Hex string representation (MSB first)
	Hex string
}

// ============================================================================
// CRC Instance Factory Functions
// ============================================================================

// CRC5_ITU returns the CRC-5/ITU polynomial (reversed: 0x15, normal: 0x28)
func CRC5_ITU() *CRC {
	return newCRC(0x15, 5, 0x00, 0x00, false, false, 0x07)
}

// CRC5_USB returns the CRC-5/USB polynomial (reversed: 0x09, normal: 0x14)
func CRC5_USB() *CRC {
	return newCRC(0x09, 5, 0x1F, 0x1F, true, true, 0x19)
}

// CRC8 returns the CRC-8 polynomial (0x07)
func CRC8() *CRC {
	return newCRC(0x07, 8, 0x00, 0x00, false, false, 0xF4)
}

// CRC8_ITU returns the CRC-8/ITU polynomial (0x07)
func CRC8_ITU() *CRC {
	return newCRC(0x07, 8, 0x00, 0x55, false, false, 0xA1)
}

// CRC8_ROHC returns the CRC-8/ROHC polynomial (0x07)
func CRC8_ROHC() *CRC {
	return newCRC(0x07, 8, 0xFF, 0x00, true, true, 0xD0)
}

// CRC8_MAXIM returns the CRC-8/MAXIM polynomial (0x31)
func CRC8_MAXIM() *CRC {
	return newCRC(0x31, 8, 0x00, 0x00, true, true, 0xA1)
}

// CRC15_CA returns the CRC-15/CA polynomial (0x4599)
func CRC15_CA() *CRC {
	return newCRC(0x4599, 15, 0x0000, 0x0000, false, false, 0x29B1)
}

// CRC16_CCITT returns the CRC-16/CCITT polynomial (0x1021)
func CRC16_CCITT() *CRC {
	// CRC-16-CCITT with reflected input produces 0x2189 for "123456789"
	return newCRC(0x1021, 16, 0x0000, 0x0000, true, true, 0x2189)
}

// CRC16_ARC returns the CRC-16/ARC polynomial (0x8005)
func CRC16_ARC() *CRC {
	return newCRC(0x8005, 16, 0x0000, 0x0000, true, true, 0xBB3D)
}

// CRC16_XMODEM returns the CRC-16/XMODEM polynomial (0x1021)
func CRC16_XMODEM() *CRC {
	return newCRC(0x1021, 16, 0x0000, 0x0000, false, false, 0x31C3)
}

// CRC16_X25 returns the CRC-16/X-25 (MCRF4XX) polynomial (0x1021)
func CRC16_X25() *CRC {
	return newCRC(0x1021, 16, 0xFFFF, 0xFFFF, true, true, 0x0E53)
}

// CRC16_MODBUS returns the CRC-16/MODBUS polynomial (0x8005)
func CRC16_MODBUS() *CRC {
	return newCRC(0x8005, 16, 0xFFFF, 0x0000, true, true, 0x4B37)
}

// CRC16_USB returns the CRC-16/USB polynomial (0x8005)
func CRC16_USB() *CRC {
	return newCRC(0x8005, 16, 0xFFFF, 0xFFFF, true, true, 0xB4C8)
}

// CRC16_CDMA2000 returns the CRC-16/CDMA2000 polynomial (0xC867)
func CRC16_CDMA2000() *CRC {
	return newCRC(0xC867, 16, 0xFFFF, 0x0000, false, false, 0x4C06)
}

// CRC32 returns the CRC-32 polynomial (0x04C11DB7, used by Ethernet, etc.)
func CRC32() *CRC {
	return newCRC(0x04C11DB7, 32, 0xFFFFFFFF, 0xFFFFFFFF, true, true, 0xCBF43926)
}

// CRC32_BZIP2 returns the CRC-32/BZIP2 polynomial (0x04C11DB7)
func CRC32_BZIP2() *CRC {
	return newCRC(0x04C11DB7, 32, 0xFFFFFFFF, 0xFFFFFFFF, false, false, 0xFC891918)
}

// CRC32C returns the CRC-32C (Castagnoli) polynomial (0x1EDC6F41)
// Used in SSE4.2, iSCSI, etc.
func CRC32C() *CRC {
	return newCRC(0x1EDC6F41, 32, 0xFFFFFFFF, 0xFFFFFFFF, true, true, 0xE3069283)
}

// CRC32_MPEG2 returns the CRC-32/MPEG-2 polynomial (0x04C11DB7)
func CRC32_MPEG2() *CRC {
	return newCRC(0x04C11DB7, 32, 0xFFFFFFFF, 0x00000000, false, false, 0x0376E6E7)
}

// CRC64_ISO returns the CRC-64/ISO polynomial (0x000000000000001B)
func CRC64_ISO() *CRC {
	return newCRC(0x000000000000001B, 64, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, true, true, 0xB90956C775A41001)
}

// CRC64_ECMA returns the CRC-64/ECMA polynomial (0x42F0E1EBA9EA3693)
func CRC64_ECMA() *CRC {
	return newCRC(0x42F0E1EBA9EA3693, 64, 0x0000000000000000, 0x0000000000000000, false, false, 0x6C40DF5F0B497347)
}

// CRC64_XZ returns the CRC-64/XZ polynomial (0x42F0E1EBA9EA3693)
func CRC64_XZ() *CRC {
	return newCRC(0x42F0E1EBA9EA3693, 64, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, true, true, 0)
}

// NewCRC creates a CRC calculator with custom parameters
func NewCRC(polynomial uint64, width uint, initVal uint64, xorOut uint64, refIn bool, refOut bool) *CRC {
	return newCRC(polynomial, width, initVal, xorOut, refIn, refOut, 0)
}

// ============================================================================
// CRC Calculation Methods
// ============================================================================

// Calculate computes the CRC of the given data
func (c *CRC) Calculate(data []byte) uint64 {
	// Get the lookup table
	table := buildTable(c.polynomial, c.width, c.refIn)

	// Initial value
	crc := c.initVal & c.widthMask

	if c.refIn {
		// Reflected CRC: use right-shift with table lookup
		for _, b := range data {
			crc = (crc >> 8) ^ table[(crc^uint64(b))&0xFF]
		}
	} else {
		// Non-reflected CRC: use left-shift algorithm
		width := int(c.width)
		mask := c.widthMask
		msbMask := uint64(1 << (width - 1))
		shift := uint(width - 8)

		for _, b := range data {
			crc ^= uint64(b) << shift
			for i := 0; i < 8; i++ {
				if (crc & msbMask) != 0 {
					crc = (crc << 1) ^ c.polynomial
				} else {
					crc = crc << 1
				}
				crc &= mask
			}
		}
	}

	// Reflect output if needed
	if c.refOut {
		crc = reflect(crc, int(c.width))
	}

	return (crc ^ c.xorOut) & c.widthMask
}

// CalculateString computes the CRC of a string
func (c *CRC) CalculateString(s string) uint64 {
	return c.Calculate([]byte(s))
}

// CalculateResult returns a Result struct with value, bytes, and hex representation
func (c *CRC) CalculateResult(data []byte) Result {
	value := c.Calculate(data)
	bytes := c.ToBytes(value)
	hex := c.ToHex(value)
	return Result{
		Value: value,
		Bytes: bytes,
		Hex:   hex,
	}
}

// WidthBits returns the bit width of the CRC
func (c *CRC) WidthBits() uint {
	return c.width
}

// CheckValue returns the check value for this CRC configuration
func (c *CRC) CheckValue() uint64 {
	return c.check
}

// VerifyCheck computes CRC of "123456789" and verifies it matches the check value
func (c *CRC) VerifyCheck() bool {
	if c.check == 0 {
		return true
	}
	return c.Calculate([]byte("123456789")) == c.check
}

// Table generates the lookup table for this CRC configuration
func (c *CRC) Table() []uint64 {
	return buildTable(c.polynomial, c.width, c.refIn)
}

// ToBytes converts a CRC value to bytes (MSB first)
func (c *CRC) ToBytes(value uint64) []byte {
	bytes := make([]byte, (c.width+7)/8)
	for i := len(bytes) - 1; i >= 0; i-- {
		bytes[i] = byte(value & 0xFF)
		value >>= 8
	}
	return bytes
}

// ToHex converts a CRC value to a hex string (MSB first)
func (c *CRC) ToHex(value uint64) string {
	bytes := c.ToBytes(value)
	hexChars := "0123456789ABCDEF"
	result := make([]byte, len(bytes)*2)
	for i, b := range bytes {
		result[i*2] = hexChars[b>>4]
		result[i*2+1] = hexChars[b&0x0F]
	}
	return string(result)
}

// ============================================================================
// Private Helper Functions
// ============================================================================

func newCRC(polynomial uint64, width uint, initVal uint64, xorOut uint64, refIn bool, refOut bool, check uint64) *CRC {
	return &CRC{
		polynomial: polynomial,
		width:      width,
		initVal:    initVal,
		xorOut:     xorOut,
		refIn:      refIn,
		refOut:     refOut,
		widthMask:  (1 << width) - 1,
		check:      check,
	}
}

// buildTable builds a CRC lookup table for byte-wise computation
func buildTable(polynomial uint64, width uint, refIn bool) []uint64 {
	bits := int(width)
	mask := uint64((1 << bits) - 1)
	table := make([]uint64, 256)

	if refIn {
		// Reflected CRC: compute table using right-shift with reflected polynomial
		polyRef := reflect(polynomial, bits)
		for i := range table {
			crc := uint64(i)
			for j := 0; j < 8; j++ {
				if (crc & 1) != 0 {
					crc = (crc >> 1) ^ polyRef
				} else {
					crc = crc >> 1
				}
			}
			table[i] = crc & mask
		}
	} else {
		// Non-reflected CRC: compute table using left-shift
		msbMask := uint64(1 << (bits - 1))
		for i := range table {
			crc := uint64(i) << (bits - 8)
			for j := 0; j < 8; j++ {
				if (crc & msbMask) != 0 {
					crc = (crc << 1) ^ polynomial
				} else {
					crc = crc << 1
				}
				crc &= mask
			}
			table[i] = crc & mask
		}
	}

	return table
}

// reflect reverses the bit order of a value
func reflect(value uint64, bits int) uint64 {
	var result uint64
	for i := 0; i < bits; i++ {
		if (value & (1 << i)) != 0 {
			result |= 1 << (bits - 1 - i)
		}
	}
	return result
}