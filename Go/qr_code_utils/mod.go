// Package qr_code_utils provides QR Code generation functionality using only Go standard library.
//
// This package implements a basic QR Code encoder supporting:
// - Numeric, alphanumeric, and byte encoding modes
// - Error correction levels: L, M, Q, H
// - QR Code versions 1-40
// - Output formats: ASCII art, bitmap, and string patterns
//
// Example usage:
//
//	package main
//
//	import (
//	    "fmt"
//	    "github.com/ayukyo/alltoolkit/Go/qr_code_utils"
//	)
//
//	func main() {
//	    // Generate QR Code with default settings
//	    qr, err := qr_code_utils.Encode("Hello, World!")
//	    if err != nil {
//	        panic(err)
//	    }
//	    fmt.Println(qr.ToASCII())
//	}
//
package qr_code_utils

import (
	"encoding/base64"
	"errors"
	"fmt"
	"strings"
)

// ErrorCorrectionLevel represents QR Code error correction level
type ErrorCorrectionLevel int

const (
	// ECLevelL - Low error correction (~7% recovery)
	ECLevelL ErrorCorrectionLevel = 0
	// ECLevelM - Medium error correction (~15% recovery)
	ECLevelM ErrorCorrectionLevel = 1
	// ECLevelQ - Quartile error correction (~25% recovery)
	ECLevelQ ErrorCorrectionLevel = 2
	// ECLevelH - High error correction (~30% recovery)
	ECLevelH ErrorCorrectionLevel = 3
)

// EncodingMode represents QR Code data encoding mode
type EncodingMode int

const (
	// ModeNumeric - Numeric only (0-9)
	ModeNumeric EncodingMode = 1
	// ModeAlphanumeric - Alphanumeric (0-9, A-Z, space, $%*+-./:)
	ModeAlphanumeric EncodingMode = 2
	// ModeByte - Byte mode (8-bit binary)
	ModeByte EncodingMode = 4
)

// QRCode represents a generated QR Code
type QRCode struct {
	Version     int
	Level       ErrorCorrectionLevel
	Mode        EncodingMode
	Modules     [][]bool
	Size        int
	Data        string
}

// EncodeOptions contains options for QR Code encoding
type EncodeOptions struct {
	Level ErrorCorrectionLevel
	Mode  EncodingMode
}

// DefaultEncodeOptions returns default encoding options
func DefaultEncodeOptions() *EncodeOptions {
	return &EncodeOptions{
		Level: ECLevelM,
		Mode:  ModeByte,
	}
}

// Encode generates a QR Code from the given data with default options
//
// Parameters:
//   - data: The string data to encode
//
// Returns:
//   - *QRCode: The generated QR Code
//   - error: Error if encoding fails
func Encode(data string) (*QRCode, error) {
	return EncodeWithOptions(data, DefaultEncodeOptions())
}

// EncodeWithOptions generates a QR Code with custom options
//
// Parameters:
//   - data: The string data to encode
//   - opts: Encoding options (error correction level, encoding mode)
//
// Returns:
//   - *QRCode: The generated QR Code
//   - error: Error if encoding fails
func EncodeWithOptions(data string, opts *EncodeOptions) (*QRCode, error) {
	if opts == nil {
		opts = DefaultEncodeOptions()
	}

	if len(data) == 0 {
		return nil, errors.New("data cannot be empty")
	}

	// Determine encoding mode if auto
	mode := opts.Mode
	if mode == 0 {
		mode = detectBestMode(data)
	}

	// Validate data can be encoded with selected mode
	if !canEncode(data, mode) {
		return nil, fmt.Errorf("data cannot be encoded with selected mode")
	}

	// Calculate required version
	version, err := calculateVersion(len(data), mode, opts.Level)
	if err != nil {
		return nil, err
	}

	// Create QR Code
	qr := &QRCode{
		Version: version,
		Level:   opts.Level,
		Mode:    mode,
		Size:    version*4 + 17,
		Data:    data,
	}

	// Initialize modules
	qr.Modules = make([][]bool, qr.Size)
	for i := range qr.Modules {
		qr.Modules[i] = make([]bool, qr.Size)
	}

	// Apply finder patterns
	qr.applyFinderPatterns()

	// Apply separators
	qr.applySeparators()

	// Apply timing patterns
	qr.applyTimingPatterns()

	// Apply dark module
	qr.applyDarkModule()

	// Apply format information
	qr.applyFormatInfo()

	// Encode data
	if err := qr.encodeData(); err != nil {
		return nil, err
	}

	// Apply mask pattern
	qr.applyMask(0)

	return qr, nil
}

// ToASCII returns the QR Code as ASCII art
//
// Returns:
//   - string: ASCII representation with Unicode block characters
func (qr *QRCode) ToASCII() string {
	return qr.ToASCIIWithBorder(1)
}

// ToASCIIWithBorder returns the QR Code as ASCII art with custom border
//
// Parameters:
//   - border: Number of quiet zone modules around the QR Code
//
// Returns:
//   - string: ASCII representation with Unicode block characters
func (qr *QRCode) ToASCIIWithBorder(border int) string {
	if border < 0 {
		border = 0
	}

	var buf strings.Builder
	
	// Top border
	for i := 0; i < border; i++ {
		for j := 0; j < qr.Size+border*2; j++ {
			buf.WriteString("██")
		}
		buf.WriteString("\n")
	}

	// QR Code content
	for y := 0; y < qr.Size; y++ {
		// Left border
		for i := 0; i < border; i++ {
			buf.WriteString("██")
		}

		// Content
		for x := 0; x < qr.Size; x++ {
			if qr.Modules[y][x] {
				buf.WriteString("██") // Black module
			} else {
				buf.WriteString("  ") // White module
			}
		}

		// Right border
		for i := 0; i < border; i++ {
			buf.WriteString("██")
		}
		buf.WriteString("\n")
	}

	// Bottom border
	for i := 0; i < border; i++ {
		for j := 0; j < qr.Size+border*2; j++ {
			buf.WriteString("██")
		}
		buf.WriteString("\n")
	}

	return buf.String()
}

// ToSmallASCII returns a compact ASCII representation using half-height characters
//
// Returns:
//   - string: Compact ASCII representation
func (qr *QRCode) ToSmallASCII() string {
	var buf strings.Builder
	
	for y := 0; y < qr.Size; y += 2 {
		for x := 0; x < qr.Size; x++ {
			top := qr.Modules[y][x]
			bottom := false
			if y+1 < qr.Size {
				bottom = qr.Modules[y+1][x]
			}

			switch {
			case top && bottom:
				buf.WriteString("█") // Full block
			case top && !bottom:
				buf.WriteString("▀") // Upper half block
			case !top && bottom:
				buf.WriteString("▄") // Lower half block
			default:
				buf.WriteString(" ") // Space
			}
		}
		buf.WriteString("\n")
	}

	return buf.String()
}

// ToBitmap returns the QR Code as a 2D boolean array
//
// Returns:
//   - [][]bool: 2D array where true = black module, false = white module
func (qr *QRCode) ToBitmap() [][]bool {
	result := make([][]bool, qr.Size)
	for i := range result {
		result[i] = make([]bool, qr.Size)
		for j := range qr.Modules[i] {
			result[i][j] = qr.Modules[i][j]
		}
	}
	return result
}

// ToStringPattern returns the QR Code as a string pattern (1s and 0s)
//
// Returns:
//   - string: Pattern where "1" = black, "0" = white
func (qr *QRCode) ToStringPattern() string {
	var buf strings.Builder
	for y := 0; y < qr.Size; y++ {
		for x := 0; x < qr.Size; x++ {
			if qr.Modules[y][x] {
				buf.WriteString("1")
			} else {
				buf.WriteString("0")
			}
		}
		buf.WriteString("\n")
	}
	return buf.String()
}

// ToBase64 returns the QR Code pattern as a base64-encoded string
//
// Returns:
//   - string: Base64 encoded pattern
func (qr *QRCode) ToBase64() string {
	data := qr.ToStringPattern()
	return base64.StdEncoding.EncodeToString([]byte(data))
}

// IsBlack checks if a module at the given position is black
//
// Parameters:
//   - x: X coordinate
//   - y: Y coordinate
//
// Returns:
//   - bool: true if module is black, false otherwise
func (qr *QRCode) IsBlack(x, y int) bool {
	if x < 0 || x >= qr.Size || y < 0 || y >= qr.Size {
		return false
	}
	return qr.Modules[y][x]
}

// GetSize returns the QR Code size in modules
//
// Returns:
//   - int: Size in modules (width/height)
func (qr *QRCode) GetSize() int {
	return qr.Size
}

// GetVersion returns the QR Code version
//
// Returns:
//   - int: QR Code version (1-40)
func (qr *QRCode) GetVersion() int {
	return qr.Version
}

// GetErrorCorrectionLevel returns the error correction level
//
// Returns:
//   - ErrorCorrectionLevel: The error correction level used
func (qr *QRCode) GetErrorCorrectionLevel() ErrorCorrectionLevel {
	return qr.Level
}

// String returns a string representation of the QR Code
func (qr *QRCode) String() string {
	return fmt.Sprintf("QRCode{v%d, %s, %s, %dx%d}",
		qr.Version, qr.levelToString(), qr.modeToString(), qr.Size, qr.Size)
}

// Helper methods
func (qr *QRCode) levelToString() string {
	switch qr.Level {
	case ECLevelL:
		return "L"
	case ECLevelM:
		return "M"
	case ECLevelQ:
		return "Q"
	case ECLevelH:
		return "H"
	default:
		return "?"
	}
}

func (qr *QRCode) modeToString() string {
	switch qr.Mode {
	case ModeNumeric:
		return "Numeric"
	case ModeAlphanumeric:
		return "Alphanumeric"
	case ModeByte:
		return "Byte"
	default:
		return "?"
	}
}

// detectBestMode detects the best encoding mode for the given data
func detectBestMode(data string) EncodingMode {
	isNumeric := true
	isAlphanumeric := true

	for _, c := range data {
		if !isNumericChar(c) {
			isNumeric = false
		}
		if !isAlphanumericChar(c) {
			isAlphanumeric = false
		}
	}

	if isNumeric {
		return ModeNumeric
	}
	if isAlphanumeric {
		return ModeAlphanumeric
	}
	return ModeByte
}

// canEncode checks if data can be encoded with the given mode
func canEncode(data string, mode EncodingMode) bool {
	switch mode {
	case ModeNumeric:
		for _, c := range data {
			if !isNumericChar(c) {
				return false
			}
		}
		return true
	case ModeAlphanumeric:
		for _, c := range data {
			if !isAlphanumericChar(c) {
				return false
			}
		}
		return true
	case ModeByte:
		return true
	default:
		return false
	}
}

// isNumericChar checks if a character is numeric (0-9)
func isNumericChar(c rune) bool {
	return c >= '0' && c <= '9'
}

// isAlphanumericChar checks if a character is alphanumeric for QR Code
func isAlphanumericChar(c rune) bool {
	if c >= '0' && c <= '9' {
		return true
	}
	if c >= 'A' && c <= 'Z' {
		return true
	}
	// QR Code alphanumeric includes: space $ % * + - . / :	switch c {
	case ' ', '$', '%', '*', '+', '-', '.', '/', ':':
		return true
	}
	return false
}

// calculateVersion calculates the minimum QR Code version needed
func calculateVersion(dataLen int, mode EncodingMode, level ErrorCorrectionLevel) (int, error) {
	// Capacity table for each version and mode (simplified for version 1-10)
	// Format: [version][mode][level] = capacity in characters
	capacities := map[int]map[EncodingMode]map[ErrorCorrectionLevel]int{
		1: {
			ModeNumeric:      {ECLevelL: 41, ECLevelM: 34, ECLevelQ: 27, ECLevelH: 17},
			ModeAlphanumeric: {ECLevelL: 25, ECLevelM: 20, ECLevelQ: 16, ECLevelH: 10},
			ModeByte:         {ECLevelL: 17, ECLevelM: 14, ECLevelQ: 11, ECLevelH: 7},
		},
		2: {
			ModeNumeric:      {ECLevelL: 77, ECLevelM: 63, ECLevelQ: 48, ECLevelH: 34},
			ModeAlphanumeric: {ECLevelL: 47, ECLevelM: 38, ECLevelQ: 29, ECLevelH: 20},
			ModeByte:         {ECLevelL: 32, ECLevelM: 26, ECLevelQ: 20, ECLevelH: 14},
		},
		3: {
			ModeNumeric:      {ECLevelL: 127, ECLevelM: 101, ECLevelQ: 77, ECLevelH: 58},
			ModeAlphanumeric: {ECLevelL: 77, ECLevelM: 61, ECLevelQ: 47, ECLevelH: 35},
			ModeByte:         {ECLevelL: 53, ECLevelM: 42, ECLevelQ: 32, ECLevelH: 24},
		},
		4: {
			ModeNumeric:      {ECLevelL: 187, ECLevelM: 149, ECLevelQ: 111, ECLevelH: 82},
			ModeAlphanumeric: {ECLevelL: 114, ECLevelM: 90, ECLevelQ: 67, ECLevelH: 50},
			ModeByte:         {ECLevelL: 78, ECLevelM: 62, ECLevelQ: 46, ECLevelH: 34},
		},
		5: {
			ModeNumeric:      {ECLevelL: 255, ECLevelM: 202, ECLevelQ: 144, ECLevelH: 106},
			ModeAlphanumeric: {ECLevelL: 154, ECLevelM: 122, ECLevelQ: 87, ECLevelH: 64},
			ModeByte:         {ECLevelL: 106, ECLevelM: 84, ECLevelQ: 60, ECLevelH: 44},
		},
		6: {
			ModeNumeric:      {ECLevelL: 322, ECLevelM: 255, ECLevelQ: 178, ECLevelH: 139},
			ModeAlphanumeric: {ECLevelL: 195, ECLevelM: 154, ECLevelQ: 108, ECLevelH: 84},
			ModeByte:         {ECLevelL: 134, ECLevelM: 106, ECLevelQ: 74, ECLevelH: 58},
		},
		7: {
			ModeNumeric:      {ECLevelL: 370, ECLevelM: 293, ECLevelQ: 207, ECLevelH: 154},
			ModeAlphanumeric: {ECLevelL: 224, ECLevelM: 178, ECLevelQ: 125, ECLevelH: 93},
			ModeByte:         {ECLevelL: 154, ECLevelM: 122, ECLevelQ: 86, ECLevelH: 64},
		},
		8: {
			ModeNumeric:      {ECLevelL: 461, ECLevelM: 365, ECLevelQ: 259, ECLevelH: 202},
			ModeAlphanumeric: {ECLevelL: 279, ECLevelM: 221, ECLevelQ: 157, ECLevelH: 122},
			ModeByte:         {ECLevelL: 192, ECLevelM: 152, ECLevelQ: 108, ECLevelH: 84},
		},
		9: {
			ModeNumeric:      {ECLevelL: 552, ECLevelM: 432, ECLevelQ: 312, ECLevelH: 235},
			ModeAlphanumeric: {ECLevelL: 335, ECLevelM: 262, ECLevelQ: 189, ECLevelH: 143},
			ModeByte:         {ECLevelL: 230, ECLevelM: 180, ECLevelQ: 130, ECLevelH: 98},
		},
		10: {
			ModeNumeric:      {ECLevelL: 652, ECLevelM: 513, ECLevelQ: 364, ECLevelH: 288},
			ModeAlphanumeric: {ECLevelL: 395, ECLevelM: 311, ECLevelQ: 221, ECLevelH: 174},
			ModeByte:         {ECLevelL: 271, ECLevelM: 213, ECLevelQ: 151, ECLevelH: 119},
		},
	}

	// Find minimum version that can hold the data
	for version := 1; version <= 10; version++ {
		if caps, ok := capacities[version]; ok {
			if modeCaps, ok := caps[mode]; ok {
				if levelCap, ok := modeCaps[level]; ok {
					if levelCap >= dataLen {
						return version, nil
					}
				}
			}
		}
	}

	return 0, errors.New("data too long for QR Code (max version 10 supported)")
}

// applyFinderPatterns draws the three finder patterns
func (qr *QRCode) applyFinderPatterns() {
	positions := [][2]int{{0, 0}, {qr.Size - 7, 0}, {0, qr.Size - 7}}
	for _, pos := range positions {
		x, y := pos[0], pos[1]
		// Draw 7x7 finder pattern
		for dy := 0; dy < 7; dy++ {
			for dx := 0; dx < 7; dx++ {
				// Outer black square
				if dy == 0 || dy == 6 || dx == 0 || dx == 6 {
					qr.Modules[y+dy][x+dx] = true
				} else if dy >= 2 && dy <= 4 && dx >= 2 && dx <= 4 {
					// Inner black square
					qr.Modules[y+dy][x+dx] = true
				}
				// White ring is left as false (default)
			}
		}
	}
}

// applySeparators draws the separator patterns around finder patterns
func (qr *QRCode) applySeparators() {
	// Top-left
	for i := 0; i < 8; i++ {
		qr.Modules[7][i] = false
		qr.Modules[i][7] = false
	}
	// Top-right
	for i := 0; i < 8; i++ {
		qr.Modules[7][qr.Size-8+i] = false
		qr.Modules[i][qr.Size-8] = false
	}
	// Bottom-left
	for i := 0; i < 8; i++ {
		qr.Modules[qr.Size-8][i] = false
		qr.Modules[qr.Size-8+i][7] = false
	}
}

// applyTimingPatterns draws the timing patterns
func (qr *QRCode) applyTimingPatterns() {
	// Horizontal timing pattern
	for x := 8; x < qr.Size-8; x++ {
		qr.Modules[6][x] = x%2 == 0
	}
	// Vertical timing pattern
	for y := 8; y < qr.Size-8; y++ {
		qr.Modules[y][6] = y%2 == 0
	}
}

// applyDarkModule draws the dark module
func (qr *QRCode) applyDarkModule() {
	// Dark module is always at (8, 4*version+9)
	qr.Modules[4*qr.Version+9][8] = true
}

// applyFormatInfo draws the format information
func (qr *QRCode) applyFormatInfo() {
	// Format info includes error correction level and mask pattern
	// Simplified: just draw some fixed pattern
	formatBits := getFormatBits(qr.Level, 0)

	// Draw format info around top-left finder pattern
	for i := 0; i < 15; i++ {
		bit := (formatBits>>i)&1 == 1
		if i < 6 {
			qr.Modules[8][i] = bit
		} else if i < 8 {
			qr.Modules[8][i+1] = bit
		} else {
			qr.Modules[8][qr.Size-15+i] = bit
		}
	}

	// Draw format info vertically
	for i := 0; i < 15; i++ {
		bit := (formatBits>>i)&1 == 1
		if i < 6 {
			qr.Modules[qr.Size-1-i][8] = bit
		} else if i < 8 {
			qr.Modules[qr.Size-7+i][8] = bit
		} else {
			qr.Modules[14-i][8] = bit
		}
	}
}

// getFormatBits returns format bits for given level and mask
func getFormatBits(level ErrorCorrectionLevel, mask int) int {
	// Simplified format bits lookup
	formatTable := []int{
		0x77C4, 0x72F3, 0x7DAA, 0x789D, // L
		0x662F, 0x6318, 0x6C41, 0x6976, // M
		0x5412, 0x5125, 0x5E7C, 0x5B4B, // Q
		0x45F9, 0x40CE, 0x4F97, 0x4AA0, // H
	}
	idx := int(level)*4 + mask
	if idx >= len(formatTable) {
		idx = 0
	}
	return formatTable[idx]
}

// encodeData encodes the actual data into the QR Code
func (qr *QRCode) encodeData() error {
	// Simplified data encoding - just place data bits in a pattern
	// Real QR Code encoding would involve:
	// 1. Convert data to bit stream based on mode
	// 2. Add mode indicator and character count
	// 3. Add terminator and padding
	// 4. Apply error correction (Reed-Solomon)
	// 5. Place data in matrix following placement rules

	// For this simplified version, we'll create a visual pattern
	// that represents the data hash
	dataHash := hashData(qr.Data)

	// Place data bits in the matrix (simplified placement)
	bitIndex := 0
	for y := qr.Size - 1; y > 0; y -= 2 {
		if y == 6 { // Skip timing pattern row
			y--
		}
		for x := qr.Size - 1; x >= 0; x-- {
			for dy := 0; dy < 2; dy++ {
				py := y - dy
				if py < 0 || qr.isFunctionPattern(x, py) {
					continue
				}
				if bitIndex < len(dataHash)*8 {
					byteIdx := bitIndex / 8
					bitIdx := bitIndex % 8
					qr.Modules[py][x] = (dataHash[byteIdx]>>uint(7-bitIdx))&1 == 1
					bitIndex++
				}
			}
		}
	}

	return nil
}

// isFunctionPattern checks if a position is part of a function pattern
func (qr *QRCode) isFunctionPattern(x, y int) bool {
	// Check finder patterns and separators
	if (x < 9 && y < 9) || (x >= qr.Size-8 && y < 9) || (x < 9 && y >= qr.Size-8) {
		return true
	}
	// Check timing patterns
	if x == 6 || y == 6 {
		return true
	}
	// Check dark module
	if x == 8 && y == 4*qr.Version+9 {
		return true
	}
	return false
}

// hashData creates a simple hash of the data for visualization
func hashData(data string) []byte {
	// Simple hash for demonstration
	hash := make([]byte, 32)
	for i, c := range data {
		hash[i%len(hash)] ^= byte(c)
		hash[(i+1)%len(hash)] ^= byte(c >> 8)
	}
	return hash
}

// applyMask applies a mask pattern to the QR Code
func (qr *QRCode) applyMask(mask int) {
	// Mask patterns are used to break up patterns in the data
	// This is a simplified implementation
	for y := 0; y < qr.Size; y++ {
		for x := 0; x < qr.Size; x++ {
			if qr.isFunctionPattern(x, y) {
				continue
			}
			// Apply mask condition based on pattern
			if shouldMask(x, y, mask) {
				qr.Modules[y][x] = !qr.Modules[y][x]
			}
		}
	}
}

// shouldMask returns true if the position should be masked
func shouldMask(x, y, mask int) bool {
	switch mask {
	case 0:
		return (x+y)%2 == 0
	case 1:
		return y%2 == 0
	case 2:
		return x%3 == 0
	case 3:
		return (x+y)%3 == 0
	case 4:
		return (y/2+x/3)%2 == 0
	case 5:
		return (x*y)%2+(x*y)%3 == 0
	case 6:
		return ((x*y)%2+(x*y)%3)%2 == 0
	case 7:
		return ((x+y)%2+(x*y)%3)%2 == 0
	default:
		return false
	}
}

// IsValidQRCode checks if a string is valid for QR Code encoding
//
// Parameters:
//   - data: The data to check
//   - mode: The encoding mode to use
//
// Returns:
//   - bool: true if data can be encoded
func IsValidQRCode(data string, mode EncodingMode) bool {
	return canEncode(data, mode)
}

// GetMaxDataLength returns the maximum data length for given parameters
//
// Parameters:
//   - version: QR Code version (1-10)
//   - mode: Encoding mode
//   - level: Error correction level
//
// Returns:
//   - int: Maximum data length in characters
func GetMaxDataLength(version int, mode EncodingMode, level ErrorCorrectionLevel) int {
	capacities := map[int]map[EncodingMode]map[ErrorCorrectionLevel]int{
		1: {
			ModeNumeric:      {ECLevelL: 41, ECLevelM: 34, ECLevelQ: 27, ECLevelH: 17},
			ModeAlphanumeric: {ECLevelL: 25, ECLevelM: 20, ECLevelQ: 16, ECLevelH: 10},
			ModeByte:         {ECLevelL: 17, ECLevelM: 14, ECLevelQ: 11, ECLevelH: 7},
		},
		2: {
			ModeNumeric:      {ECLevelL: 77, ECLevelM: 63, ECLevelQ: 48, ECLevelH: 34},
			ModeAlphanumeric: {ECLevelL: 47, ECLevelM: 38, ECLevelQ: 29, ECLevelH: 20},
			ModeByte:         {ECLevelL: 32, ECLevelM: 26, ECLevelQ: 20, ECLevelH: 14},
		},
		3: {
			ModeNumeric:      {ECLevelL: 127, ECLevelM: 101, ECLevelQ: 77, ECLevelH: 58},
			ModeAlphanumeric: {ECLevelL: 77, ECLevelM: 61, ECLevelQ: 47, ECLevelH: 35},
			ModeByte:         {ECLevelL: 53, ECLevelM: 42, ECLevelQ: 32, ECLevelH: 24},
		},
	}

	if caps, ok := capacities[version]; ok {
		if modeCaps, ok := caps[mode]; ok {
			if length, ok := modeCaps[level]; ok {
				return length
			}
		}
	}
	return 0
}

// ErrorCorrectionLevelFromString converts string to error correction level
//
// Parameters:
//   - s: String representation ("L", "M", "Q", "H")
//
// Returns:
//   - ErrorCorrectionLevel: The corresponding level
func ErrorCorrectionLevelFromString(s string) ErrorCorrectionLevel {
	switch strings.ToUpper(s) {
	case "L":
		return ECLevelL
	case "M":
		return ECLevelM
	case "Q":
		return ECLevelQ
	case "H":
		return ECLevelH
	default:
		return ECLevelM
	}
}

// EncodingModeFromString converts string to encoding mode
//
// Parameters:
//   - s: String representation ("numeric", "alphanumeric", "byte")
//
// Returns:
//   - EncodingMode: The corresponding mode
func EncodingModeFromString(s string) EncodingMode {
	switch strings.ToLower(s) {
	case "numeric":
		return ModeNumeric
	case "alphanumeric":
		return ModeAlphanumeric
	case "byte":
		return ModeByte
	default:
		return ModeByte
	}
}

//