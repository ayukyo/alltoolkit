package idgenerator

import (
	"strings"
	"testing"
	"time"
)

// ============================================================================
// UUID Tests
// ============================================================================

func TestNewUUID(t *testing.T) {
	uuid, err := NewUUID()
	if err != nil {
		t.Fatalf("NewUUID() error = %v", err)
	}

	// Check version bits (should be 4)
	if uuid[6]&0xf0 != 0x40 {
		t.Errorf("UUID version bits incorrect, got %x", uuid[6]&0xf0)
	}

	// Check variant bits (should be RFC 4122)
	if uuid[8]&0xc0 != 0x80 {
		t.Errorf("UUID variant bits incorrect, got %x", uuid[8]&0xc0)
	}
}

func TestUUIDString(t *testing.T) {
	uuid, err := NewUUID()
	if err != nil {
		t.Fatalf("NewUUID() error = %v", err)
	}

	s := uuid.String()
	if len(s) != 36 {
		t.Errorf("UUID string length = %d, want 36", len(s))
	}

	// Check format (8-4-4-4-12)
	parts := strings.Split(s, "-")
	if len(parts) != 5 {
		t.Errorf("UUID format incorrect, got %d parts", len(parts))
	}
	if len(parts[0]) != 8 || len(parts[1]) != 4 || len(parts[2]) != 4 || len(parts[3]) != 4 || len(parts[4]) != 12 {
		t.Errorf("UUID parts length incorrect")
	}
}

func TestUUIDStringNoDash(t *testing.T) {
	uuid, err := NewUUID()
	if err != nil {
		t.Fatalf("NewUUID() error = %v", err)
	}

	s := uuid.StringNoDash()
	if len(s) != 32 {
		t.Errorf("UUID string without dashes length = %d, want 32", len(s))
	}
	if strings.Contains(s, "-") {
		t.Error("UUID string should not contain dashes")
	}
}

func TestUUIDUniqueness(t *testing.T) {
	uuids := make(map[string]bool)
	const count = 10000

	for i := 0; i < count; i++ {
		uuid, err := NewUUID()
		if err != nil {
			t.Fatalf("NewUUID() error = %v", err)
		}
		s := uuid.String()
		if uuids[s] {
			t.Errorf("Duplicate UUID generated: %s", s)
		}
		uuids[s] = true
	}
}

// ============================================================================
// Snowflake ID Tests
// ============================================================================

func TestNewSnowflakeGenerator(t *testing.T) {
	config := DefaultSnowflakeConfig()
	gen, err := NewSnowflakeGenerator(config)
	if err != nil {
		t.Fatalf("NewSnowflakeGenerator() error = %v", err)
	}

	id, err := gen.Generate()
	if err != nil {
		t.Fatalf("Generate() error = %v", err)
	}
	if id <= 0 {
		t.Errorf("Generated ID should be positive, got %d", id)
	}
}

func TestSnowflakeGeneratorInvalidNodeID(t *testing.T) {
	config := DefaultSnowflakeConfig()
	config.NodeID = -1
	_, err := NewSnowflakeGenerator(config)
	if err == nil {
		t.Error("Expected error for negative NodeID")
	}

	config.NodeID = 1024 // Too large for 10 bits
	_, err = NewSnowflakeGenerator(config)
	if err == nil {
		t.Error("Expected error for NodeID exceeding max")
	}
}

func TestSnowflakeIDComponents(t *testing.T) {
	config := DefaultSnowflakeConfig()
	config.NodeID = 123
	gen, err := NewSnowflakeGenerator(config)
	if err != nil {
		t.Fatalf("NewSnowflakeGenerator() error = %v", err)
	}

	id, err := gen.Generate()
	if err != nil {
		t.Fatalf("Generate() error = %v", err)
	}

	// Extract and verify node ID
	nodeID := gen.ExtractNodeID(id)
	if nodeID != 123 {
		t.Errorf("ExtractNodeID() = %d, want 123", nodeID)
	}

	// Extract and verify timestamp is recent
	timestamp := gen.ExtractTime(id)
	now := time.Now()
	diff := now.Sub(timestamp)
	if diff < 0 {
		diff = -diff
	}
	if diff > time.Second {
		t.Errorf("ExtractTime() timestamp differs from now by %v", diff)
	}
}

func TestSnowflakeUniqueness(t *testing.T) {
	config := DefaultSnowflakeConfig()
	gen, err := NewSnowflakeGenerator(config)
	if err != nil {
		t.Fatalf("NewSnowflakeGenerator() error = %v", err)
	}

	ids := make(map[int64]bool)
	const count = 10000

	for i := 0; i < count; i++ {
		id, err := gen.Generate()
		if err != nil {
			t.Fatalf("Generate() error = %v", err)
		}
		if ids[id] {
			t.Errorf("Duplicate ID generated: %d", id)
		}
		ids[id] = true
	}
}

func TestSnowflakeSequenceIncrement(t *testing.T) {
	config := DefaultSnowflakeConfig()
	gen, err := NewSnowflakeGenerator(config)
	if err != nil {
		t.Fatalf("NewSnowflakeGenerator() error = %v", err)
	}

	id1, _ := gen.Generate()
	seq1 := gen.ExtractSequence(id1)

	id2, _ := gen.Generate()
	seq2 := gen.ExtractSequence(id2)

	// Sequences should be different in same millisecond
	if seq1 == seq2 {
		// This could happen if we're in different milliseconds, check timestamps
		time1 := gen.ExtractTime(id1)
		time2 := gen.ExtractTime(id2)
		if time1.Equal(time2) {
			t.Errorf("Sequences should increment in same millisecond: %d, %d", seq1, seq2)
		}
	}
}

// ============================================================================
// NanoID Tests
// ============================================================================

func TestNewNanoID(t *testing.T) {
	id, err := NewNanoID()
	if err != nil {
		t.Fatalf("NewNanoID() error = %v", err)
	}
	if len(id) != 21 {
		t.Errorf("NanoID length = %d, want 21", len(id))
	}
}

func TestNewNanoIDWithSize(t *testing.T) {
	sizes := []int{8, 10, 16, 24, 32}
	for _, size := range sizes {
		id, err := NewNanoIDWithSize(size)
		if err != nil {
			t.Fatalf("NewNanoIDWithSize(%d) error = %v", size, err)
		}
		if len(id) != size {
			t.Errorf("NanoID length = %d, want %d", len(id), size)
		}
	}
}

func TestNanoIDGeneratorCustomAlphabet(t *testing.T) {
	gen, err := NewNanoIDGenerator(AlphabetLower, 16)
	if err != nil {
		t.Fatalf("NewNanoIDGenerator() error = %v", err)
	}

	for i := 0; i < 100; i++ {
		id, err := gen.Generate()
		if err != nil {
			t.Fatalf("Generate() error = %v", err)
		}
		if len(id) != 16 {
			t.Errorf("NanoID length = %d, want 16", len(id))
		}
		// Check all chars are lowercase
		for _, c := range id {
			if c >= 'A' && c <= 'Z' {
				t.Errorf("NanoID contains uppercase char: %c", c)
			}
		}
	}
}

func TestNanoIDUniqueness(t *testing.T) {
	ids := make(map[string]bool)
	const count = 10000

	for i := 0; i < count; i++ {
		id, err := NewNanoID()
		if err != nil {
			t.Fatalf("NewNanoID() error = %v", err)
		}
		if ids[id] {
			t.Errorf("Duplicate NanoID generated: %s", id)
		}
		ids[id] = true
	}
}

func TestNanoIDAlphabets(t *testing.T) {
	alphabets := []struct {
		name     string
		alphabet string
	}{
		{"Default", DefaultAlphabet},
		{"Lower", AlphabetLower},
		{"Upper", AlphabetUpper},
		{"Hex", AlphabetHex},
		{"Numbers", AlphabetNumbers},
	}

	for _, tc := range alphabets {
		t.Run(tc.name, func(t *testing.T) {
			gen, err := NewNanoIDGenerator(tc.alphabet, 100)
			if err != nil {
				t.Fatalf("NewNanoIDGenerator() error = %v", err)
			}
			id, err := gen.Generate()
			if err != nil {
				t.Fatalf("Generate() error = %v", err)
			}
			// Verify all chars are from alphabet
			for _, c := range id {
				if !strings.ContainsRune(tc.alphabet, c) {
					t.Errorf("NanoID contains char not in alphabet: %c", c)
				}
			}
		})
	}
}

// ============================================================================
// Custom ID Tests
// ============================================================================

func TestCustomIDGenerator(t *testing.T) {
	config := FormatSpec{
		Prefix:    "ORD-",
		Separator: "-",
		Parts: []FormatPart{
			{Type: "timestamp", Format: "20060102"},
			{Type: "random", Length: 4},
			{Type: "sequence", Length: 4},
		},
	}

	gen, err := NewCustomIDGenerator(config)
	if err != nil {
		t.Fatalf("NewCustomIDGenerator() error = %v", err)
	}

	id, err := gen.Generate()
	if err != nil {
		t.Fatalf("Generate() error = %v", err)
	}

	// Check prefix
	if !strings.HasPrefix(id, "ORD-") {
		t.Errorf("ID should have prefix ORD-, got %s", id)
	}

	// Check date format in ID
	dateStr := time.Now().Format("20060102")
	if !strings.Contains(id, dateStr) {
		t.Errorf("ID should contain date %s, got %s", dateStr, id)
	}
}

func TestCustomIDFixedPart(t *testing.T) {
	config := FormatSpec{
		Parts: []FormatPart{
			{Type: "fixed", Value: "TEST"},
			{Type: "random", Length: 4},
		},
	}

	gen, err := NewCustomIDGenerator(config)
	if err != nil {
		t.Fatalf("NewCustomIDGenerator() error = %v", err)
	}

	id, err := gen.Generate()
	if err != nil {
		t.Fatalf("Generate() error = %v", err)
	}

	if !strings.HasPrefix(id, "TEST-") {
		t.Errorf("ID should start with TEST-, got %s", id)
	}
}

func TestCustomIDSequence(t *testing.T) {
	config := FormatSpec{
		Parts: []FormatPart{
			{Type: "sequence", Length: 4},
		},
	}

	gen, _ := NewCustomIDGenerator(config)

	ids := make([]string, 5)
	for i := 0; i < 5; i++ {
		id, err := gen.Generate()
		if err != nil {
			t.Fatalf("Generate() error = %v", err)
		}
		ids[i] = id
	}

	// Sequences should increment
	for i := 1; i < 5; i++ {
		if ids[i] <= ids[i-1] {
			t.Errorf("Sequence should increment: %s, %s", ids[i-1], ids[i])
		}
	}
}

// ============================================================================
// Short ID Tests
// ============================================================================

func TestShortIDGenerator(t *testing.T) {
	gen := NewShortIDGenerator(8)

	id, err := gen.Generate()
	if err != nil {
		t.Fatalf("Generate() error = %v", err)
	}

	if len(id) != 8 {
		t.Errorf("Short ID length = %d, want 8", len(id))
	}

	// Check URL-safe
	for _, c := range id {
		if !((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9')) {
			t.Errorf("Short ID contains non-URL-safe char: %c", c)
		}
	}
}

func TestShortIDUniqueness(t *testing.T) {
	gen := NewShortIDGenerator(8)
	ids := make(map[string]bool)
	const count = 10000

	for i := 0; i < count; i++ {
		id, err := gen.Generate()
		if err != nil {
			t.Fatalf("Generate() error = %v", err)
		}
		if ids[id] {
			t.Errorf("Duplicate Short ID generated: %s", id)
		}
		ids[id] = true
	}
}

// ============================================================================
// Hash ID Tests
// ============================================================================

func TestHashIDGenerator(t *testing.T) {
	gen := NewHashIDGenerator("H-", 8)

	id1 := gen.Generate("test content")
	id2 := gen.Generate("test content")

	// Same content should produce same ID
	if id1 != id2 {
		t.Errorf("Same content should produce same ID: %s != %s", id1, id2)
	}

	// Different content should produce different ID
	id3 := gen.Generate("different content")
	if id1 == id3 {
		t.Error("Different content should produce different ID")
	}
}

func TestHashIDPrefix(t *testing.T) {
	gen := NewHashIDGenerator("PREFIX-", 8)

	id := gen.Generate("content")
	if !strings.HasPrefix(id, "PREFIX-") {
		t.Errorf("Hash ID should have prefix PREFIX-, got %s", id)
	}
}

func TestHashIDLength(t *testing.T) {
	lengths := []int{4, 8, 12, 16}
	for _, length := range lengths {
		gen := NewHashIDGenerator("", length)
		id := gen.Generate("test")
		if len(id) != length {
			t.Errorf("Hash ID length = %d, want %d", len(id), length)
		}
	}
}

// ============================================================================
// Sequential ID Tests
// ============================================================================

func TestSequentialGenerator(t *testing.T) {
	gen := NewSequentialGenerator("ORD-", 6, 1)

	ids := []string{}
	for i := 0; i < 5; i++ {
		ids = append(ids, gen.Next())
	}

	expected := []string{
		"ORD-000001",
		"ORD-000002",
		"ORD-000003",
		"ORD-000004",
		"ORD-000005",
	}

	for i, want := range expected {
		if ids[i] != want {
			t.Errorf("ID[%d] = %s, want %s", i, ids[i], want)
		}
	}
}

func TestSequentialGeneratorNoPadding(t *testing.T) {
	gen := NewSequentialGenerator("ID-", 0, 100)

	id := gen.Next()
	if id != "ID-100" {
		t.Errorf("ID = %s, want ID-100", id)
	}
}

func TestSequentialGeneratorReset(t *testing.T) {
	gen := NewSequentialGenerator("X-", 4, 1)

	gen.Next()
	gen.Next()
	gen.Reset()

	id := gen.Next()
	if id != "X-0001" {
		t.Errorf("After reset, ID = %s, want X-0001", id)
	}
}

func TestSequentialGeneratorCurrent(t *testing.T) {
	gen := NewSequentialGenerator("", 0, 0)

	if gen.Current() != 0 {
		t.Errorf("Initial current = %d, want 0", gen.Current())
	}

	gen.Next()
	if gen.Current() != 1 {
		t.Errorf("After Next(), current = %d, want 1", gen.Current())
	}
}

// ============================================================================
// Benchmark Tests
// ============================================================================

func BenchmarkUUID(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = NewUUID()
	}
}

func BenchmarkSnowflake(b *testing.B) {
	config := DefaultSnowflakeConfig()
	gen, _ := NewSnowflakeGenerator(config)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = gen.Generate()
	}
}

func BenchmarkNanoID(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = NewNanoID()
	}
}

func BenchmarkShortID(b *testing.B) {
	gen := NewShortIDGenerator(8)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = gen.Generate()
	}
}

func BenchmarkHashID(b *testing.B) {
	gen := NewHashIDGenerator("H-", 8)
	content := "benchmark test content"
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = gen.Generate(content)
	}
}

func BenchmarkSequentialID(b *testing.B) {
	gen := NewSequentialGenerator("ID-", 6, 1)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = gen.Next()
	}
}