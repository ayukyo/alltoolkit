// Package idgenerator provides various ID generation utilities.
// Supports UUID v4, Snowflake IDs, NanoIDs, and custom format IDs.
// Zero external dependencies - pure Go implementation.
package idgenerator

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"hash/fnv"
	"sync"
	"time"
)

// ============================================================================
// UUID Generator
// ============================================================================

// UUID represents a 128-bit Universal Unique Identifier
type UUID [16]byte

// NewUUID generates a random UUID v4 (RFC 4122 compliant)
func NewUUID() (UUID, error) {
	var uuid UUID
	_, err := rand.Read(uuid[:])
	if err != nil {
		return uuid, fmt.Errorf("failed to generate UUID: %w", err)
	}

	// Set version (4) and variant bits
	uuid[6] = (uuid[6] & 0x0f) | 0x40 // Version 4
	uuid[8] = (uuid[8] & 0x3f) | 0x80 // Variant RFC 4122

	return uuid, nil
}

// String returns the UUID in canonical format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
func (u UUID) String() string {
	return fmt.Sprintf("%08x-%04x-%04x-%04x-%012x",
		u[0:4], u[4:6], u[6:8], u[8:10], u[10:16])
}

// StringNoDash returns the UUID without dashes
func (u UUID) StringNoDash() string {
	return hex.EncodeToString(u[:])
}

// ParseUUID parses a UUID string into UUID type
func ParseUUID(s string) (UUID, error) {
	var uuid UUID
	_, err := hex.Decode(uuid[:], []byte(s))
	if err != nil {
		return uuid, fmt.Errorf("invalid UUID format: %w", err)
	}
	return uuid, nil
}

// ============================================================================
// Snowflake ID Generator
// ============================================================================

// SnowflakeConfig holds configuration for Snowflake ID generator
type SnowflakeConfig struct {
	Epoch      int64 // Custom epoch timestamp in milliseconds
	NodeID     int64 // Node/worker ID (0-1023)
	Sequence   int64 // Initial sequence number
	NodeBits   uint8 // Bits for node ID (default 10)
	SeqBits    uint8 // Bits for sequence (default 12)
	TimeBits   uint8 // Bits for timestamp (default 41)
}

// SnowflakeGenerator generates Twitter Snowflake-like IDs
type SnowflakeGenerator struct {
	mu        sync.Mutex
	epoch     int64
	nodeID    int64
	sequence  int64
	lastTime  int64
	nodeMask  int64
	seqMask   int64
	timeShift uint8
	nodeShift uint8
}

// DefaultSnowflakeConfig returns default Snowflake configuration
func DefaultSnowflakeConfig() SnowflakeConfig {
	return SnowflakeConfig{
		Epoch:    1704067200000, // 2024-01-01 00:00:00 UTC
		NodeID:   0,
		Sequence: 0,
		NodeBits: 10,
		SeqBits:  12,
		TimeBits: 41,
	}
}

// NewSnowflakeGenerator creates a new Snowflake ID generator
func NewSnowflakeGenerator(config SnowflakeConfig) (*SnowflakeGenerator, error) {
	if config.NodeBits == 0 {
		config.NodeBits = 10
	}
	if config.SeqBits == 0 {
		config.SeqBits = 12
	}
	if config.TimeBits == 0 {
		config.TimeBits = 41
	}

	maxNode := int64(1)<<config.NodeBits - 1
	if config.NodeID < 0 || config.NodeID > maxNode {
		return nil, fmt.Errorf("node ID must be between 0 and %d", maxNode)
	}

	return &SnowflakeGenerator{
		epoch:     config.Epoch,
		nodeID:    config.NodeID,
		sequence:  0,
		lastTime:  0,
		nodeMask:  maxNode,
		seqMask:   int64(1)<<config.SeqBits - 1,
		timeShift: config.SeqBits + config.NodeBits,
		nodeShift: config.SeqBits,
	}, nil
}

// Generate creates a new Snowflake ID
func (s *SnowflakeGenerator) Generate() (int64, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().UnixMilli() - s.epoch

	if now < s.lastTime {
		return 0, fmt.Errorf("clock moved backwards, refusing to generate ID")
	}

	if now == s.lastTime {
		s.sequence = (s.sequence + 1) & s.seqMask
		if s.sequence == 0 {
			// Wait for next millisecond
			for now <= s.lastTime {
				time.Sleep(100 * time.Microsecond)
				now = time.Now().UnixMilli() - s.epoch
			}
		}
	} else {
		s.sequence = 0
	}

	s.lastTime = now

	return (now << s.timeShift) | (s.nodeID << s.nodeShift) | s.sequence, nil
}

// GenerateWithTime creates a Snowflake ID and returns it with the timestamp
func (s *SnowflakeGenerator) GenerateWithTime() (id int64, timestamp time.Time, err error) {
	id, err = s.Generate()
	if err != nil {
		return 0, time.Time{}, err
	}
	timestamp = s.ExtractTime(id)
	return id, timestamp, nil
}

// ExtractTime extracts the timestamp from a Snowflake ID
func (s *SnowflakeGenerator) ExtractTime(id int64) time.Time {
	ts := id >> s.timeShift
	return time.UnixMilli(ts + s.epoch)
}

// ExtractNodeID extracts the node ID from a Snowflake ID
func (s *SnowflakeGenerator) ExtractNodeID(id int64) int64 {
	return (id >> s.nodeShift) & s.nodeMask
}

// ExtractSequence extracts the sequence from a Snowflake ID
func (s *SnowflakeGenerator) ExtractSequence(id int64) int64 {
	return id & s.seqMask
}

// ============================================================================
// NanoID Generator
// ============================================================================

// Default alphabet for NanoID
const (
	DefaultAlphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	AlphabetLower   = "0123456789abcdefghijklmnopqrstuvwxyz"
	AlphabetUpper   = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	AlphabetNoDups  = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz" // No confusing chars
	AlphabetHex     = "0123456789abcdef"
	AlphabetNumbers = "0123456789"
)

// NanoIDGenerator generates URL-friendly unique identifiers
type NanoIDGenerator struct {
	alphabet string
	size     int
	mask     byte
	chars    []byte
}

// NewNanoIDGenerator creates a new NanoID generator
func NewNanoIDGenerator(alphabet string, size int) (*NanoIDGenerator, error) {
	if len(alphabet) == 0 {
		alphabet = DefaultAlphabet
	}
	if size <= 0 {
		size = 21 // Default NanoID size
	}
	if size > 256 {
		return nil, fmt.Errorf("size must be <= 256")
	}

	// Calculate mask for uniform distribution
	mask := byte(1)
	for mask < byte(len(alphabet)) {
		mask <<= 1
	}
	mask--

	return &NanoIDGenerator{
		alphabet: alphabet,
		size:     size,
		mask:     mask,
		chars:    []byte(alphabet),
	}, nil
}

// Generate creates a new NanoID
func (n *NanoIDGenerator) Generate() (string, error) {
	bytes := make([]byte, n.size)
	randomBytes := make([]byte, n.size*2)

	_, err := rand.Read(randomBytes)
	if err != nil {
		return "", fmt.Errorf("failed to generate random bytes: %w", err)
	}

	for i := 0; i < n.size; i++ {
		// Use rejection sampling for uniform distribution
		idx := randomBytes[i] & n.mask
		for idx >= byte(len(n.chars)) {
			_, err := rand.Read(randomBytes[i : i+1])
			if err != nil {
				return "", err
			}
			idx = randomBytes[i] & n.mask
		}
		bytes[i] = n.chars[idx]
	}

	return string(bytes), nil
}

// NewNanoID is a convenience function to generate a NanoID with defaults
func NewNanoID() (string, error) {
	gen, err := NewNanoIDGenerator(DefaultAlphabet, 21)
	if err != nil {
		return "", err
	}
	return gen.Generate()
}

// NewNanoIDWithSize generates a NanoID with custom size
func NewNanoIDWithSize(size int) (string, error) {
	gen, err := NewNanoIDGenerator(DefaultAlphabet, size)
	if err != nil {
		return "", err
	}
	return gen.Generate()
}

// ============================================================================
// Custom Format ID Generator
// ============================================================================

// FormatSpec defines a custom ID format
type FormatSpec struct {
	Prefix    string // Prefix to add (e.g., "ORD-")
	Suffix    string // Suffix to add
	Separator string // Separator between parts
	Parts     []FormatPart
}

// FormatPart defines a single part of a custom ID
type FormatPart struct {
	Type   string // "timestamp", "random", "sequence", "fixed"
	Length int    // Length for random/sequence parts
	Value  string // Fixed value for "fixed" type
	Format string // Time format for "timestamp" type (default: "20060102")
}

// CustomIDGenerator generates IDs with custom formats
type CustomIDGenerator struct {
	config   FormatSpec
	sequence int64
	mu       sync.Mutex
}

// NewCustomIDGenerator creates a new custom ID generator
func NewCustomIDGenerator(config FormatSpec) (*CustomIDGenerator, error) {
	return &CustomIDGenerator{
		config:   config,
		sequence: 0,
	}, nil
}

// Generate creates a new custom format ID
func (c *CustomIDGenerator) Generate() (string, error) {
	var parts []string
	now := time.Now()

	for _, part := range c.config.Parts {
		var val string
		var err error

		switch part.Type {
		case "timestamp":
			format := part.Format
			if format == "" {
				format = "20060102"
			}
			val = now.Format(format)

		case "random":
			val, err = c.generateRandom(part.Length)
			if err != nil {
				return "", err
			}

		case "sequence":
			val = c.nextSequence(part.Length)

		case "fixed":
			val = part.Value

		default:
			return "", fmt.Errorf("unknown part type: %s", part.Type)
		}

		parts = append(parts, val)
	}

	sep := c.config.Separator
	if sep == "" {
		sep = "-"
	}

	result := c.config.Prefix
	for i, part := range parts {
		if i > 0 {
			result += sep
		}
		result += part
	}
	result += c.config.Suffix

	return result, nil
}

func (c *CustomIDGenerator) generateRandom(length int) (string, error) {
	if length <= 0 {
		return "", nil
	}

	bytes := make([]byte, length)
	_, err := rand.Read(bytes)
	if err != nil {
		return "", err
	}

	const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for i := range bytes {
		bytes[i] = chars[int(bytes[i])%len(chars)]
	}

	return string(bytes), nil
}

func (c *CustomIDGenerator) nextSequence(length int) string {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.sequence++
	format := fmt.Sprintf("%%0%dd", length)
	return fmt.Sprintf(format, c.sequence%int64(pow10(length)))
}

func pow10(n int) int64 {
	result := int64(1)
	for i := 0; i < n; i++ {
		result *= 10
	}
	return result
}

// ============================================================================
// Short ID Generator (URL-safe, collision-resistant)
// ============================================================================

// ShortIDGenerator generates short, URL-safe unique identifiers
type ShortIDGenerator struct {
	alphabet string
	length   int
}

// NewShortIDGenerator creates a short ID generator
func NewShortIDGenerator(length int) *ShortIDGenerator {
	if length <= 0 {
		length = 8
	}
	return &ShortIDGenerator{
		alphabet: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
		length:   length,
	}
}

// Generate creates a short ID
func (s *ShortIDGenerator) Generate() (string, error) {
	bytes := make([]byte, s.length)
	_, err := rand.Read(bytes)
	if err != nil {
		return "", err
	}

	for i := range bytes {
		bytes[i] = s.alphabet[int(bytes[i])%len(s.alphabet)]
	}

	return string(bytes), nil
}

// ============================================================================
// Hash-based ID Generator (deterministic, consistent)
// ============================================================================

// HashIDGenerator generates IDs based on content hash
type HashIDGenerator struct {
	prefix string
	length int
}

// NewHashIDGenerator creates a hash-based ID generator
func NewHashIDGenerator(prefix string, length int) *HashIDGenerator {
	if length <= 0 {
		length = 8
	}
	return &HashIDGenerator{
		prefix: prefix,
		length: length,
	}
}

// Generate creates a hash-based ID from input content
func (h *HashIDGenerator) Generate(content string) string {
	hasher := fnv.New64a()
	hasher.Write([]byte(content))
	hash := hasher.Sum64()

	const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	result := make([]byte, h.length)

	for i := 0; i < h.length; i++ {
		result[i] = chars[int(hash%uint64(len(chars)))]
		hash /= uint64(len(chars))
		if hash == 0 {
			hash = uint64(i + 1)
		}
	}

	return h.prefix + string(result)
}

// ============================================================================
// Prefixed Sequential ID Generator
// ============================================================================

// SequentialGenerator generates sequential IDs with prefix
type SequentialGenerator struct {
	prefix   string
	counter  int64
	mu       sync.Mutex
	padding  int
	startNum int64
}

// NewSequentialGenerator creates a sequential ID generator
func NewSequentialGenerator(prefix string, padding int, startNum int64) *SequentialGenerator {
	return &SequentialGenerator{
		prefix:   prefix,
		counter:  startNum,
		padding:  padding,
		startNum: startNum,
	}
}

// Next generates the next sequential ID
func (s *SequentialGenerator) Next() string {
	s.mu.Lock()
	defer s.mu.Unlock()

	id := s.counter
	s.counter++

	if s.padding > 0 {
		format := fmt.Sprintf("%%s%%0%dd", s.padding)
		return fmt.Sprintf(format, s.prefix, id)
	}
	return fmt.Sprintf("%s%d", s.prefix, id)
}

// Reset resets the counter to the start number
func (s *SequentialGenerator) Reset() {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.counter = s.startNum
}

// Current returns the current counter value
func (s *SequentialGenerator) Current() int64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.counter
}