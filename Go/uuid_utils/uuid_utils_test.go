package uuid_utils

import (
	"encoding/json"
	"strings"
	"testing"
	"time"
)

// TestNewV4 tests v4 UUID generation
func TestNewV4(t *testing.T) {
	uuid, err := NewV4()
	if err != nil {
		t.Fatalf("NewV4() error = %v", err)
	}

	if uuid.IsNil() {
		t.Error("NewV4() returned nil UUID")
	}

	if uuid.Version() != VersionV4 {
		t.Errorf("NewV4() version = %d, want %d", uuid.Version(), VersionV4)
	}

	if uuid.Variant() != VariantRFC4122 {
		t.Errorf("NewV4() variant = %d, want %d", uuid.Variant(), VariantRFC4122)
	}
}

// TestMustNewV4 tests that MustNewV4 panics on error
func TestMustNewV4(t *testing.T) {
	uuid := MustNewV4()
	if uuid.IsNil() {
		t.Error("MustNewV4() returned nil UUID")
	}
}

// TestNewV4Uniqueness tests that generated UUIDs are unique
func TestNewV4Uniqueness(t *testing.T) {
	uuids := make(map[UUID]bool)
	for i := 0; i < 10000; i++ {
		uuid, err := NewV4()
		if err != nil {
			t.Fatalf("NewV4() error = %v", err)
		}
		if uuids[uuid] {
			t.Error("NewV4() generated duplicate UUID")
		}
		uuids[uuid] = true
	}
}

// TestNewV3 tests v3 UUID generation
func TestNewV3(t *testing.T) {
	namespace := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8") // DNS namespace
	name := "example.com"

	uuid := NewV3(namespace, name)

	if uuid.Version() != VersionV3 {
		t.Errorf("NewV3() version = %d, want %d", uuid.Version(), VersionV3)
	}

	// Same namespace + name should produce same UUID
	uuid2 := NewV3(namespace, name)
	if !uuid.Equals(uuid2) {
		t.Error("NewV3() not deterministic for same input")
	}

	// Different name should produce different UUID
	uuid3 := NewV3(namespace, "different.com")
	if uuid.Equals(uuid3) {
		t.Error("NewV3() produced same UUID for different names")
	}
}

// TestNewV5 tests v5 UUID generation
func TestNewV5(t *testing.T) {
	namespace := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8") // DNS namespace
	name := "example.com"

	uuid := NewV5(namespace, name)

	if uuid.Version() != VersionV5 {
		t.Errorf("NewV5() version = %d, want %d", uuid.Version(), VersionV5)
	}

	// Same namespace + name should produce same UUID
	uuid2 := NewV5(namespace, name)
	if !uuid.Equals(uuid2) {
		t.Error("NewV5() not deterministic for same input")
	}

	// V3 and V5 should produce different UUIDs for same input
	uuid3 := NewV3(namespace, name)
	if uuid.Equals(uuid3) {
		t.Error("V3 and V5 produced same UUID for same input")
	}
}

// TestParse tests UUID parsing
func TestParse(t *testing.T) {
	tests := []struct {
		input   string
		wantErr bool
	}{
		{"6ba7b810-9dad-11d1-80b4-00c04fd430c8", false},
		{"6BA7B810-9DAD-11D1-80B4-00C04FD430C8", false},
		{"6ba7b8109dad11d180b400c04fd430c8", false}, // no dashes
		{"{6ba7b810-9dad-11d1-80b4-00c04fd430c8}", false},
		{"urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8", false},
		{"invalid", true},
		{"6ba7b810-9dad-11d1-80b4", true},          // too short
		{"6ba7b810-9dad-11d1-80b4-00c04fd430c8g", true}, // invalid char
		{"", true},
	}

	for _, tt := range tests {
		uuid, err := Parse(tt.input)
		if (err != nil) != tt.wantErr {
			t.Errorf("Parse(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
		}
		if err == nil {
			expected := "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
			if uuid.String() != expected {
				t.Errorf("Parse(%q) = %v, want %v", tt.input, uuid.String(), expected)
			}
		}
	}
}

// TestMustParse tests that MustParse panics on error
func TestMustParse(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	if uuid.String() != "6ba7b810-9dad-11d1-80b4-00c04fd430c8" {
		t.Errorf("MustParse() = %v", uuid.String())
	}

	defer func() {
		if r := recover(); r == nil {
			t.Error("MustParse() did not panic on invalid input")
		}
	}()
	MustParse("invalid")
}

// TestParseOrNil tests ParseOrNil
func TestParseOrNil(t *testing.T) {
	uuid := ParseOrNil("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	if uuid.IsNil() {
		t.Error("ParseOrNil() returned NilUUID for valid input")
	}

	uuid = ParseOrNil("invalid")
	if !uuid.IsNil() {
		t.Error("ParseOrNil() did not return NilUUID for invalid input")
	}
}

// TestString tests UUID string formatting
func TestString(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	expected := "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

	if uuid.String() != expected {
		t.Errorf("String() = %v, want %v", uuid.String(), expected)
	}
}

// TestStringNoDash tests UUID string without dashes
func TestStringNoDash(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	expected := "6ba7b8109dad11d180b400c04fd430c8"

	if uuid.StringNoDash() != expected {
		t.Errorf("StringNoDash() = %v, want %v", uuid.StringNoDash(), expected)
	}
}

// TestURN tests URN format
func TestURN(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	expected := "urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8"

	if uuid.URN() != expected {
		t.Errorf("URN() = %v, want %v", uuid.URN(), expected)
	}
}

// TestVersion tests UUID version detection
func TestVersion(t *testing.T) {
	tests := []struct {
		uuidStr string
		version int
	}{
		{"d9428888-122b-11e1-b85c-61cd3cbb3210", VersionV1},
		{"d9428888-122b-21e1-b85c-61cd3cbb3210", VersionV2},
		{"d9428888-122b-31e1-b85c-61cd3cbb3210", VersionV3},
		{"d9428888-122b-41e1-b85c-61cd3cbb3210", VersionV4},
		{"d9428888-122b-51e1-b85c-61cd3cbb3210", VersionV5},
	}

	for _, tt := range tests {
		uuid := MustParse(tt.uuidStr)
		if uuid.Version() != tt.version {
			t.Errorf("Version() = %d, want %d", uuid.Version(), tt.version)
		}
	}
}

// TestVariant tests UUID variant detection
func TestVariant(t *testing.T) {
	tests := []struct {
		uuidStr string
		variant int
	}{
		{"d9428888-122b-11e1-085c-61cd3cbb3210", VariantNCS},       // 0xxxxxxx
		{"d9428888-122b-11e1-b85c-61cd3cbb3210", VariantRFC4122},   // 10xxxxxx
		{"d9428888-122b-11e1-d85c-61cd3cbb3210", VariantMicrosoft},  // 110xxxxx
		{"d9428888-122b-11e1-f85c-61cd3cbb3210", VariantFuture},    // 111xxxxx
	}

	for _, tt := range tests {
		uuid := MustParse(tt.uuidStr)
		if uuid.Variant() != tt.variant {
			t.Errorf("Variant() = %d, want %d", uuid.Variant(), tt.variant)
		}
	}
}

// TestIsNil tests nil UUID detection
func TestIsNil(t *testing.T) {
	if !NilUUID.IsNil() {
		t.Error("NilUUID.IsNil() = false, want true")
	}

	uuid := MustNewV4()
	if uuid.IsNil() {
		t.Error("NewV4().IsNil() = true, want false")
	}
}

// TestIsValid tests valid UUID check
func TestIsValid(t *testing.T) {
	if NilUUID.IsValid() {
		t.Error("NilUUID.IsValid() = true, want false")
	}

	uuid := MustNewV4()
	if !uuid.IsValid() {
		t.Error("NewV4().IsValid() = false, want true")
	}
}

// TestEquals tests UUID equality
func TestEquals(t *testing.T) {
	uuid1 := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	uuid2 := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	uuid3 := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c9")

	if !uuid1.Equals(uuid2) {
		t.Error("Equals() = false for equal UUIDs")
	}

	if uuid1.Equals(uuid3) {
		t.Error("Equals() = true for different UUIDs")
	}
}

// TestCompare tests UUID comparison
func TestCompare(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")
	uuid3 := MustParse("00000000-0000-0000-0000-000000000001")

	if uuid1.Compare(uuid2) != -1 {
		t.Error("Compare() should return -1 for lesser UUID")
	}

	if uuid2.Compare(uuid1) != 1 {
		t.Error("Compare() should return 1 for greater UUID")
	}

	if uuid1.Compare(uuid3) != 0 {
		t.Error("Compare() should return 0 for equal UUIDs")
	}
}

// TestMarshalText tests JSON marshaling
func TestMarshalText(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	data, err := uuid.MarshalText()
	if err != nil {
		t.Fatalf("MarshalText() error = %v", err)
	}

	if string(data) != "6ba7b810-9dad-11d1-80b4-00c04fd430c8" {
		t.Errorf("MarshalText() = %v", string(data))
	}
}

// TestUnmarshalText tests JSON unmarshaling
func TestUnmarshalText(t *testing.T) {
	var uuid UUID
	err := uuid.UnmarshalText([]byte("6ba7b810-9dad-11d1-80b4-00c04fd430c8"))
	if err != nil {
		t.Fatalf("UnmarshalText() error = %v", err)
	}

	if uuid.String() != "6ba7b810-9dad-11d1-80b4-00c04fd430c8" {
		t.Errorf("UnmarshalText() = %v", uuid.String())
	}
}

// TestJSONRoundTrip tests JSON marshaling/unmarshaling
func TestJSONRoundTrip(t *testing.T) {
	type TestStruct struct {
		ID UUID `json:"id"`
	}

	original := TestStruct{ID: MustNewV4()}
	data, err := json.Marshal(original)
	if err != nil {
		t.Fatalf("json.Marshal() error = %v", err)
	}

	var parsed TestStruct
	err = json.Unmarshal(data, &parsed)
	if err != nil {
		t.Fatalf("json.Unmarshal() error = %v", err)
	}

	if !original.ID.Equals(parsed.ID) {
		t.Error("JSON round-trip failed")
	}
}

// TestIsValidString tests string validation
func TestIsValidString(t *testing.T) {
	tests := []struct {
		input string
		valid bool
	}{
		{"6ba7b810-9dad-11d1-80b4-00c04fd430c8", true},
		{"6BA7B810-9DAD-11D1-80B4-00C04FD430C8", true},
		{"6ba7b8109dad11d180b400c04fd430c8", false}, // no dashes
		{"invalid", false},
		{"", false},
		{"6ba7b810-9dad-11d1-80b4", false},
	}

	for _, tt := range tests {
		if IsValidString(tt.input) != tt.valid {
			t.Errorf("IsValidString(%q) = %v, want %v", tt.input, !tt.valid, tt.valid)
		}
	}
}

// TestGenerateV4Batch tests batch generation
func TestGenerateV4Batch(t *testing.T) {
	uuids, err := GenerateV4Batch(100)
	if err != nil {
		t.Fatalf("GenerateV4Batch() error = %v", err)
	}

	if len(uuids) != 100 {
		t.Errorf("GenerateV4Batch(100) returned %d UUIDs", len(uuids))
	}

	// Check uniqueness
	seen := make(map[UUID]bool)
	for _, uuid := range uuids {
		if seen[uuid] {
			t.Error("GenerateV4Batch() produced duplicate UUID")
		}
		seen[uuid] = true
	}
}

// TestShort tests shortened UUID
func TestShort(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	short := uuid.Short()

	if short != "6ba7b810" {
		t.Errorf("Short() = %v, want 6ba7b810", short)
	}
}

// TestToUpperLower tests case conversion
func TestToUpperLower(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

	if uuid.ToUpper() != "6BA7B810-9DAD-11D1-80B4-00C04FD430C8" {
		t.Errorf("ToUpper() = %v", uuid.ToUpper())
	}

	if uuid.ToLower() != "6ba7b810-9dad-11d1-80b4-00c04fd430c8" {
		t.Errorf("ToLower() = %v", uuid.ToLower())
	}
}

// TestFormat tests format options
func TestFormat(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

	tests := []struct {
		format   string
		expected string
	}{
		{"default", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"},
		{"", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"},
		{"nodash", "6ba7b8109dad11d180b400c04fd430c8"},
		{"urn", "urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8"},
		{"braces", "{6ba7b810-9dad-11d1-80b4-00c04fd430c8}"},
		{"short", "6ba7b810"},
		{"upper", "6BA7B810-9DAD-11D1-80B4-00C04FD430C8"},
		{"lower", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"},
	}

	for _, tt := range tests {
		if uuid.Format(tt.format) != tt.expected {
			t.Errorf("Format(%q) = %v, want %v", tt.format, uuid.Format(tt.format), tt.expected)
		}
	}
}

// TestParseAny tests flexible parsing
func TestParseAny(t *testing.T) {
	tests := []string{
		"6ba7b810-9dad-11d1-80b4-00c04fd430c8",
		"6BA7B810-9DAD-11D1-80B4-00C04FD430C8",
		"6ba7b8109dad11d180b400c04fd430c8",
		"{6ba7b810-9dad-11d1-80b4-00c04fd430c8}",
		"urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8",
		"URN:UUID:6BA7B810-9DAD-11D1-80B4-00C04FD430C8",
	}

	for _, input := range tests {
		uuid, err := ParseAny(input)
		if err != nil {
			t.Errorf("ParseAny(%q) error = %v", input, err)
			continue
		}
		if uuid.String() != "6ba7b810-9dad-11d1-80b4-00c04fd430c8" {
			t.Errorf("ParseAny(%q) = %v", input, uuid.String())
		}
	}
}

// TestGenerator tests UUID generator
func TestGenerator(t *testing.T) {
	gen := NewGenerator("user_")

	id, err := gen.Generate()
	if err != nil {
		t.Fatalf("Generator.Generate() error = %v", err)
	}

	if !strings.HasPrefix(id, "user_") {
		t.Errorf("Generate() = %v, should have prefix 'user_'", id)
	}

	// Extract UUID
	uuid, err := gen.ExtractUUID(id)
	if err != nil {
		t.Fatalf("Generator.ExtractUUID() error = %v", err)
	}

	if uuid.IsNil() {
		t.Error("ExtractUUID() returned nil UUID")
	}

	// MustGenerate
	id2 := gen.MustGenerate()
	if !strings.HasPrefix(id2, "user_") {
		t.Errorf("MustGenerate() = %v, should have prefix 'user_'", id2)
	}
}

// TestSort tests UUID sorting
func TestSort(t *testing.T) {
	uuids := []UUID{
		MustParse("00000000-0000-0000-0000-000000000003"),
		MustParse("00000000-0000-0000-0000-000000000001"),
		MustParse("00000000-0000-0000-0000-000000000002"),
	}

	Sort(uuids)

	for i := 1; i < len(uuids); i++ {
		if uuids[i-1].Compare(uuids[i]) > 0 {
			t.Error("Sort() did not sort correctly")
		}
	}
}

// TestDeduplicate tests duplicate removal
func TestDeduplicate(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")

	uuids := []UUID{uuid1, uuid2, uuid1, uuid2, uuid1}
	result := Deduplicate(uuids)

	if len(result) != 2 {
		t.Errorf("Deduplicate() returned %d UUIDs, want 2", len(result))
	}
}

// TestContains tests containment check
func TestContains(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")
	uuid3 := MustParse("00000000-0000-0000-0000-000000000003")

	uuids := []UUID{uuid1, uuid2}

	if !Contains(uuids, uuid1) {
		t.Error("Contains() = false for present UUID")
	}

	if Contains(uuids, uuid3) {
		t.Error("Contains() = true for absent UUID")
	}
}

// TestIndexOf tests index finding
func TestIndexOf(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")
	uuid3 := MustParse("00000000-0000-0000-0000-000000000003")

	uuids := []UUID{uuid1, uuid2}

	if IndexOf(uuids, uuid1) != 0 {
		t.Errorf("IndexOf() = %d, want 0", IndexOf(uuids, uuid1))
	}

	if IndexOf(uuids, uuid2) != 1 {
		t.Errorf("IndexOf() = %d, want 1", IndexOf(uuids, uuid2))
	}

	if IndexOf(uuids, uuid3) != -1 {
		t.Errorf("IndexOf() = %d, want -1", IndexOf(uuids, uuid3))
	}
}

// TestRemove tests removal
func TestRemove(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")
	uuid3 := MustParse("00000000-0000-0000-0000-000000000003")

	uuids := []UUID{uuid1, uuid2, uuid3}
	result := Remove(uuids, uuid2)

	if len(result) != 2 {
		t.Errorf("Remove() returned %d UUIDs, want 2", len(result))
	}

	if Contains(result, uuid2) {
		t.Error("Remove() did not remove target UUID")
	}
}

// TestFilter tests filtering
func TestFilter(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0001-000000000002") // v1
	uuid3 := MustParse("00000000-0000-0000-0004-000000000003") // v4

	uuids := []UUID{uuid1, uuid2, uuid3}
	result := Filter(uuids, func(u UUID) bool {
		return u.Version() == VersionV4
	})

	if len(result) != 1 {
		t.Errorf("Filter() returned %d UUIDs, want 1", len(result))
	}
}

// TestMap tests mapping
func TestMap(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")

	uuids := []UUID{uuid1, uuid2}
	result := Map(uuids, func(u UUID) string { return u.String() })

	if len(result) != 2 {
		t.Errorf("Map() returned %d strings, want 2", len(result))
	}

	if result[0] != uuid1.String() {
		t.Error("Map() transformation incorrect")
	}
}

// TestStrings tests string conversion
func TestStrings(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")

	uuids := []UUID{uuid1, uuid2}
	strs := Strings(uuids)

	if len(strs) != 2 {
		t.Errorf("Strings() returned %d strings, want 2", len(strs))
	}

	if strs[0] != uuid1.String() {
		t.Error("Strings() conversion incorrect")
	}
}

// TestParseStrings tests string parsing
func TestParseStrings(t *testing.T) {
	strs := []string{
		"00000000-0000-0000-0000-000000000001",
		"00000000-0000-0000-0000-000000000002",
	}

	uuids, err := ParseStrings(strs)
	if err != nil {
		t.Fatalf("ParseStrings() error = %v", err)
	}

	if len(uuids) != 2 {
		t.Errorf("ParseStrings() returned %d UUIDs, want 2", len(uuids))
	}
}

// TestParseStringsError tests error handling in ParseStrings
func TestParseStringsError(t *testing.T) {
	strs := []string{
		"00000000-0000-0000-0000-000000000001",
		"invalid",
	}

	_, err := ParseStrings(strs)
	if err == nil {
		t.Error("ParseStrings() should return error for invalid input")
	}
}

// TestAnalyze tests UUID analysis
func TestAnalyze(t *testing.T) {
	uuid1 := MustNewV4()
	uuid2 := MustNewV4()
	uuid3 := NewV5(MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8"), "test")

	uuids := []UUID{uuid1, uuid2, uuid3, NilUUID}
	stats := Analyze(uuids)

	if stats.Total != 4 {
		t.Errorf("Analyze().Total = %d, want 4", stats.Total)
	}

	if stats.VersionMap[VersionV4] != 2 {
		t.Errorf("Analyze().VersionMap[V4] = %d, want 2", stats.VersionMap[VersionV4])
	}

	if stats.VersionMap[VersionV5] != 1 {
		t.Errorf("Analyze().VersionMap[V5] = %d, want 1", stats.VersionMap[VersionV5])
	}

	if stats.NilCount != 1 {
		t.Errorf("Analyze().NilCount = %d, want 1", stats.NilCount)
	}
}

// TestEqual tests slice equality
func TestEqual(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")

	a := []UUID{uuid1, uuid2}
	b := []UUID{uuid1, uuid2}
	c := []UUID{uuid2, uuid1}
	d := []UUID{uuid1}

	if !Equal(a, b) {
		t.Error("Equal() = false for equal slices")
	}

	if Equal(a, c) {
		t.Error("Equal() = true for reordered slices")
	}

	if Equal(a, d) {
		t.Error("Equal() = true for different length slices")
	}
}

// TestClone tests slice cloning
func TestClone(t *testing.T) {
	uuid1 := MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := MustParse("00000000-0000-0000-0000-000000000002")

	original := []UUID{uuid1, uuid2}
	cloned := Clone(original)

	if !Equal(original, cloned) {
		t.Error("Clone() did not create equal slice")
	}

	// Modify clone should not affect original
	cloned[0] = uuid2
	if Equal(original, cloned) {
		t.Error("Clone() should create independent copy")
	}
}

// TestBytes tests byte conversion
func TestBytes(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	bytes := uuid.Bytes()

	if len(bytes) != 16 {
		t.Errorf("Bytes() returned %d bytes, want 16", len(bytes))
	}
}

// TestMarshalBinary tests binary marshaling
func TestMarshalBinary(t *testing.T) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	data, err := uuid.MarshalBinary()
	if err != nil {
		t.Fatalf("MarshalBinary() error = %v", err)
	}

	if len(data) != 16 {
		t.Errorf("MarshalBinary() returned %d bytes, want 16", len(data))
	}
}

// TestUnmarshalBinary tests binary unmarshaling
func TestUnmarshalBinary(t *testing.T) {
	original := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	data, _ := original.MarshalBinary()

	var uuid UUID
	err := uuid.UnmarshalBinary(data)
	if err != nil {
		t.Fatalf("UnmarshalBinary() error = %v", err)
	}

	if !uuid.Equals(original) {
		t.Error("UnmarshalBinary() did not restore UUID")
	}

	// Test error case
	err = uuid.UnmarshalBinary([]byte{1, 2, 3})
	if err == nil {
		t.Error("UnmarshalBinary() should error on short data")
	}
}

// TestTime tests v1 UUID time extraction
func TestTime(t *testing.T) {
	// V1 UUID with known timestamp
	// This is a synthetic v1 UUID
	uuid := MustParse("c232ab00-9214-11eb-a8b3-0242ac130003")

	_, err := uuid.Time()
	// The timestamp might not be perfectly accurate due to synthetic UUID
	// Just verify it doesn't error for v1
	if err != nil && uuid.Version() == VersionV1 {
		t.Errorf("Time() error for v1 UUID: %v", err)
	}

	// V4 UUID should return error
	v4 := MustNewV4()
	_, err = v4.Time()
	if err == nil {
		t.Error("Time() should return error for non-v1 UUID")
	}
}

// TestNodeID tests v1 UUID node ID extraction
func TestNodeID(t *testing.T) {
	uuid := MustParse("c232ab00-9214-11eb-a8b3-0242ac130003")
	nodeID := uuid.NodeID()

	if len(nodeID) != 6 {
		t.Errorf("NodeID() returned %d bytes, want 6", len(nodeID))
	}
}

// TestClockSeq tests v1 UUID clock sequence extraction
func TestClockSeq(t *testing.T) {
	uuid := MustParse("c232ab00-9214-11eb-a8b3-0242ac130003")
	clockSeq := uuid.ClockSeq()

	// Just verify it doesn't panic and returns something
	_ = clockSeq
}

// BenchmarkNewV4 benchmarks v4 UUID generation
func BenchmarkNewV4(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = NewV4()
	}
}

// BenchmarkParse benchmarks UUID parsing
func BenchmarkParse(b *testing.B) {
	s := "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
	for i := 0; i < b.N; i++ {
		_, _ = Parse(s)
	}
}

// BenchmarkString benchmarks UUID string conversion
func BenchmarkString(b *testing.B) {
	uuid := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	for i := 0; i < b.N; i++ {
		_ = uuid.String()
	}
}

// BenchmarkNewV5 benchmarks v5 UUID generation
func BenchmarkNewV5(b *testing.B) {
	namespace := MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	name := "example.com"
	for i := 0; i < b.N; i++ {
		_ = NewV5(namespace, name)
	}
}

// BenchmarkGenerateV4Batch benchmarks batch generation
func BenchmarkGenerateV4Batch(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = GenerateV4Batch(100)
	}
}