// Package base58_utils provides comprehensive Base58 encoding and decoding utilities.
// Base58 is a binary-to-text encoding scheme that excludes ambiguous characters
// (0, O, I, l) making it ideal for human-readable encoded data like Bitcoin addresses.
package base58_utils

import (
	"errors"
	"math/big"
)

// Common errors
var (
	ErrInvalidBase58   = errors.New("invalid base58 encoding")
	ErrEmptyInput      = errors.New("empty input")
	ErrInvalidAlphabet = errors.New("invalid alphabet length, must be 58 characters")
)

// Alphabet defines the Base58 alphabet
type Alphabet struct {
	chars    [58]byte
	decode   [256]int8
	encode   [58]byte
}

// Bitcoin alphabet (most common, used by Bitcoin, IPFS)
var BitcoinAlphabet = NewAlphabet("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

// Flickr alphabet (alternative, used by Flickr)
var FlickrAlphabet = NewAlphabet("123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ")

// Ripple alphabet (used by Ripple)
var RippleAlphabet = NewAlphabet("rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz")

// NewAlphabet creates a new Base58 alphabet from a 58-character string
func NewAlphabet(s string) *Alphabet {
	if len(s) != 58 {
		panic(ErrInvalidAlphabet)
	}

	a := &Alphabet{}
	copy(a.encode[:], s)

	for i := range a.decode {
		a.decode[i] = -1
	}

	for i, c := range a.encode {
		a.chars[i] = c
		a.decode[c] = int8(i)
	}

	return a
}

// Encode encodes a byte slice to Base58 string using Bitcoin alphabet
func Encode(input []byte) string {
	return EncodeWithAlphabet(input, BitcoinAlphabet)
}

// EncodeWithAlphabet encodes a byte slice to Base58 string with custom alphabet
func EncodeWithAlphabet(input []byte, alphabet *Alphabet) string {
	if len(input) == 0 {
		return ""
	}

	// Count leading zeros
	leadingZeros := 0
	for _, b := range input {
		if b == 0 {
			leadingZeros++
		} else {
			break
		}
	}

	// Convert to big integer
	num := new(big.Int).SetBytes(input)
	base := big.NewInt(58)
	zero := big.NewInt(0)
	mod := new(big.Int)

	var result []byte

	// Convert to base58
	for num.Cmp(zero) > 0 {
		num.DivMod(num, base, mod)
		result = append(result, alphabet.encode[mod.Int64()])
	}

	// Add leading '1's (the base58 representation of zero)
	for i := 0; i < leadingZeros; i++ {
		result = append(result, alphabet.encode[0])
	}

	// Reverse the result
	for i, j := 0, len(result)-1; i < j; i, j = i+1, j-1 {
		result[i], result[j] = result[j], result[i]
	}

	return string(result)
}

// EncodeString encodes a string to Base58 string
func EncodeString(s string) string {
	return Encode([]byte(s))
}

// EncodeStringWithAlphabet encodes a string to Base58 with custom alphabet
func EncodeStringWithAlphabet(s string, alphabet *Alphabet) string {
	return EncodeWithAlphabet([]byte(s), alphabet)
}

// Decode decodes a Base58 string to byte slice using Bitcoin alphabet
func Decode(input string) ([]byte, error) {
	return DecodeWithAlphabet(input, BitcoinAlphabet)
}

// DecodeWithAlphabet decodes a Base58 string to byte slice with custom alphabet
func DecodeWithAlphabet(input string, alphabet *Alphabet) ([]byte, error) {
	if input == "" {
		return nil, ErrEmptyInput
	}

	// Count leading '1's (the base58 representation of zero)
	leadingOnes := 0
	for _, c := range input {
		if byte(c) == alphabet.encode[0] {
			leadingOnes++
		} else {
			break
		}
	}

	// Convert from base58 to big integer
	num := big.NewInt(0)
	base := big.NewInt(58)

	for _, c := range input {
		index := alphabet.decode[c]
		if index < 0 {
			return nil, ErrInvalidBase58
		}
		num.Mul(num, base)
		num.Add(num, big.NewInt(int64(index)))
	}

	// Convert to bytes
	decoded := num.Bytes()

	// Add leading zeros
	result := make([]byte, leadingOnes+len(decoded))
	copy(result[leadingOnes:], decoded)

	return result, nil
}

// DecodeString decodes a Base58 string to string
func DecodeString(input string) (string, error) {
	decoded, err := Decode(input)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// DecodeStringWithAlphabet decodes a Base58 string to string with custom alphabet
func DecodeStringWithAlphabet(input string, alphabet *Alphabet) (string, error) {
	decoded, err := DecodeWithAlphabet(input, alphabet)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// IsValid checks if a string is valid Base58 (Bitcoin alphabet)
func IsValid(s string) bool {
	return IsValidWithAlphabet(s, BitcoinAlphabet)
}

// IsValidWithAlphabet checks if a string is valid Base58 with custom alphabet
func IsValidWithAlphabet(s string, alphabet *Alphabet) bool {
	if s == "" {
		return false
	}

	for _, c := range s {
		if alphabet.decode[c] < 0 {
			return false
		}
	}
	return true
}

// EncodeInt encodes a big integer to Base58
func EncodeInt(n *big.Int) string {
	return EncodeIntWithAlphabet(n, BitcoinAlphabet)
}

// EncodeIntWithAlphabet encodes a big integer to Base58 with custom alphabet
func EncodeIntWithAlphabet(n *big.Int, alphabet *Alphabet) string {
	if n.Sign() < 0 {
		return ""
	}
	if n.Sign() == 0 {
		return string(alphabet.encode[0])
	}

	return EncodeWithAlphabet(n.Bytes(), alphabet)
}

// DecodeInt decodes a Base58 string to big integer
func DecodeInt(s string) (*big.Int, error) {
	return DecodeIntWithAlphabet(s, BitcoinAlphabet)
}

// DecodeIntWithAlphabet decodes a Base58 string to big integer with custom alphabet
func DecodeIntWithAlphabet(s string, alphabet *Alphabet) (*big.Int, error) {
	if s == "" {
		return nil, ErrEmptyInput
	}

	num := big.NewInt(0)
	base := big.NewInt(58)

	for _, c := range s {
		index := alphabet.decode[c]
		if index < 0 {
			return nil, ErrInvalidBase58
		}
		num.Mul(num, base)
		num.Add(num, big.NewInt(int64(index)))
	}

	return num, nil
}

// EncodeCheck encodes with checksum (Base58Check encoding used in Bitcoin)
func EncodeCheck(input []byte) string {
	return EncodeCheckWithAlphabet(input, BitcoinAlphabet)
}

// EncodeCheckWithAlphabet encodes with checksum using custom alphabet
func EncodeCheckWithAlphabet(input []byte, alphabet *Alphabet) string {
	if len(input) == 0 {
		return ""
	}

	// Double SHA256 checksum
	checksum := doubleSHA256(input)[:4]
	
	// Append checksum
	data := make([]byte, len(input)+4)
	copy(data, input)
	copy(data[len(input):], checksum)

	return EncodeWithAlphabet(data, alphabet)
}

// DecodeCheck decodes Base58Check and validates checksum
func DecodeCheck(input string) ([]byte, error) {
	return DecodeCheckWithAlphabet(input, BitcoinAlphabet)
}

// DecodeCheckWithAlphabet decodes Base58Check with custom alphabet and validates checksum
func DecodeCheckWithAlphabet(input string, alphabet *Alphabet) ([]byte, error) {
	decoded, err := DecodeWithAlphabet(input, alphabet)
	if err != nil {
		return nil, err
	}

	if len(decoded) < 4 {
		return nil, ErrInvalidBase58
	}

	// Split data and checksum
	data := decoded[:len(decoded)-4]
	checksum := decoded[len(decoded)-4:]

	// Verify checksum
	expectedChecksum := doubleSHA256(data)[:4]
	for i := range checksum {
		if checksum[i] != expectedChecksum[i] {
			return nil, ErrInvalidBase58
		}
	}

	return data, nil
}

// doubleSHA256 computes double SHA256 hash
func doubleSHA256(data []byte) []byte {
	// Simple implementation without external dependencies
	// Uses the standard library's crypto/sha256
	// Note: We implement a basic version here
	// For production, use crypto/sha256
	h := newSHA256()
	h.Write(data)
	hash1 := h.Sum(nil)
	
	h = newSHA256()
	h.Write(hash1)
	return h.Sum(nil)
}

// simpleSHA256 is a basic SHA-256 implementation for zero-dependency
type simpleSHA256 struct {
	state [8]uint32
	buf   [64]byte
	len   uint64
	pos   int
}

func newSHA256() *simpleSHA256 {
	h := &simpleSHA256{}
	h.reset()
	return h
}

func (h *simpleSHA256) reset() {
	h.state = [8]uint32{
		0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
		0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
	}
	h.len = 0
	h.pos = 0
}

func (h *simpleSHA256) Write(p []byte) (int, error) {
	n := len(p)
	h.len += uint64(n)

	for len(p) > 0 {
		if h.pos == 0 && len(p) >= 64 {
			h.block(p[:64])
			p = p[64:]
			continue
		}

		copied := copy(h.buf[h.pos:], p)
		h.pos += copied
		p = p[copied:]

		if h.pos == 64 {
			h.block(h.buf[:])
			h.pos = 0
		}
	}

	return n, nil
}

func (h *simpleSHA256) Sum(in []byte) []byte {
	d := *h

	// Padding
	var pad [72]byte
	pad[0] = 0x80
	bits := d.len * 8

	pos := d.pos
	if pos < 56 {
		d.Write(pad[:56-pos])
	} else {
		d.Write(pad[:64-pos])
		d.Write(pad[:56])
	}

	// Length in bits
	for i := uint(0); i < 8; i++ {
		pad[7-i] = byte(bits >> (i * 8))
	}
	d.Write(pad[:8])

	// Output
	var out [32]byte
	for i := range d.state {
		out[i*4] = byte(d.state[i] >> 24)
		out[i*4+1] = byte(d.state[i] >> 16)
		out[i*4+2] = byte(d.state[i] >> 8)
		out[i*4+3] = byte(d.state[i])
	}

	return append(in, out[:]...)
}

func (h *simpleSHA256) block(p []byte) {
	// SHA-256 round constants
	k := [64]uint32{
		0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
		0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
		0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
		0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
		0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
		0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
		0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
		0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
		0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
		0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
		0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
		0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
		0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
		0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
	}

	var w [64]uint32
	for i := 0; i < 16; i++ {
		w[i] = uint32(p[i*4])<<24 | uint32(p[i*4+1])<<16 |
			uint32(p[i*4+2])<<8 | uint32(p[i*4+3])
	}
	for i := 16; i < 64; i++ {
		s0 := w[i-15]>>7 ^ w[i-15]>>18 ^ w[i-15]>>3 ^ w[i-15]<<25 ^ w[i-15]<<14 ^ w[i-15]
		s1 := w[i-2]>>17 ^ w[i-2]>>19 ^ w[i-2]>>10 ^ w[i-2]<<15 ^ w[i-2]<<13
		w[i] = w[i-16] + s0 + w[i-7] + s1
	}

	a, b, c, d, e, f, g := h.state[0], h.state[1], h.state[2], h.state[3],
		h.state[4], h.state[5], h.state[6]
	hh := h.state[7]

	for i := 0; i < 64; i++ {
		S1 := e>>6 ^ e>>11 ^ e>>25 ^ e<<26 ^ e<<21 ^ e<<7
		ch := (e & f) ^ (^e & g)
		temp1 := hh + S1 + ch + k[i] + w[i]
		S0 := a>>2 ^ a>>13 ^ a>>22 ^ a<<30 ^ a<<19 ^ a<<10
		maj := (a & b) ^ (a & c) ^ (b & c)
		temp2 := S0 + maj

		hh = g
		g = f
		f = e
		e = d + temp1
		d = c
		c = b
		b = a
		a = temp1 + temp2
	}

	h.state[0] += a
	h.state[1] += b
	h.state[2] += c
	h.state[3] += d
	h.state[4] += e
	h.state[5] += f
	h.state[6] += g
	h.state[7] += hh
}

// ConvertAlphabet converts a Base58 string from one alphabet to another
func ConvertAlphabet(input string, from, to *Alphabet) (string, error) {
	decoded, err := DecodeWithAlphabet(input, from)
	if err != nil {
		return "", err
	}
	return EncodeWithAlphabet(decoded, to), nil
}

// TrimLeadingZeros trims leading '1' characters (Base58 representation of zero bytes)
func TrimLeadingZeros(s string) string {
	for i, c := range s {
		if c != '1' {
			return s[i:]
		}
	}
	return ""
}

// CountLeadingZeros counts leading '1' characters in Base58 string
func CountLeadingZeros(s string) int {
	count := 0
	for _, c := range s {
		if c == '1' {
			count++
		} else {
			break
		}
	}
	return count
}

// EncodeHex encodes a hex string to Base58
func EncodeHex(hex string) (string, error) {
	if len(hex) == 0 {
		return "", nil
	}

	// Validate hex string
	if len(hex)%2 != 0 {
		hex = "0" + hex
	}

	data := make([]byte, len(hex)/2)
	for i := 0; i < len(hex); i += 2 {
		b, err := hexByte(hex[i], hex[i+1])
		if err != nil {
			return "", err
		}
		data[i/2] = b
	}

	return Encode(data), nil
}

// DecodeHex decodes a Base58 string to hex string
func DecodeHex(input string) (string, error) {
	decoded, err := Decode(input)
	if err != nil {
		return "", err
	}
	return bytesToHex(decoded), nil
}

// hexByte converts two hex characters to a byte
func hexByte(h1, h2 byte) (byte, error) {
	b1, err := hexDigit(h1)
	if err != nil {
		return 0, err
	}
	b2, err := hexDigit(h2)
	if err != nil {
		return 0, err
	}
	return (b1 << 4) | b2, nil
}

// hexDigit converts a hex character to its numeric value
func hexDigit(c byte) (byte, error) {
	switch {
	case '0' <= c && c <= '9':
		return c - '0', nil
	case 'a' <= c && c <= 'f':
		return c - 'a' + 10, nil
	case 'A' <= c && c <= 'F':
		return c - 'A' + 10, nil
	default:
		return 0, ErrInvalidBase58
	}
}

// bytesToHex converts bytes to hex string
func bytesToHex(data []byte) string {
	const hexChars = "0123456789abcdef"
	result := make([]byte, len(data)*2)
	for i, b := range data {
		result[i*2] = hexChars[b>>4]
		result[i*2+1] = hexChars[b&0x0f]
	}
	return string(result)
}

// Size estimates the Base58 encoded size for given input size
func Size(inputSize int) int {
	// Base58 is approximately log(256)/log(58) ≈ 1.37
	// We round up for safety
	return int(float64(inputSize)*1.38) + 1
}

// DecodeSize estimates the decoded size for given encoded size
func DecodeSize(encodedSize int) int {
	// Reverse of above
	return int(float64(encodedSize) / 1.38)
}