// Package uuid_utils provides UUID generation and manipulation utilities.
// Zero external dependencies - pure Go standard library implementation.
package uuid_utils

import (
	"crypto/md5"
	"crypto/rand"
	"crypto/sha1"
	"encoding/hex"
	"errors"
	"fmt"
	"regexp"
	"strings"
	"time"
)

// UUID represents a Universally Unique Identifier
type UUID [16]byte

var (
	// ErrInvalidUUID indicates the input string is not a valid UUID
	ErrInvalidUUID = errors.New("invalid UUID format")
	// ErrInvalidVersion indicates an invalid UUID version
	ErrInvalidVersion = errors.New("invalid UUID version")
	// ErrInvalidVariant indicates an invalid UUID variant
	ErrInvalidVariant = errors.New("invalid UUID variant")

	// NilUUID is the nil UUID (all zeros)
	NilUUID = UUID{}

	// uuidRegex matches standard UUID format
	uuidRegex = regexp.MustCompile(`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`)
)

// Version constants
const (
	VersionUnknown = 0
	VersionV1      = 1 // Time-based
	VersionV2      = 2 // DCE security
	VersionV3      = 3 // MD5 hash
	VersionV4      = 4 // Random
	VersionV5      = 5 // SHA-1 hash
)

// Variant constants
const (
	VariantNCS       = 0 // Reserved, NCS backward compatibility
	VariantRFC4122   = 1 // RFC 4122 variant
	VariantMicrosoft = 2 // Microsoft Corporation variant
	VariantFuture    = 3 // Future reserved
)

// NewV4 generates a random UUID (version 4)
func NewV4() (UUID, error) {
	var uuid UUID
	_, err := rand.Read(uuid[:])
	if err != nil {
		return NilUUID, err
	}

	// Set version (4) and variant bits
	uuid[6] = (uuid[6] & 0x0f) | 0x40 // version 4
	uuid[8] = (uuid[8] & 0x3f) | 0x80  // variant RFC 4122

	return uuid, nil
}

// MustNewV4 generates a random UUID (version 4), panics on error
func MustNewV4() UUID {
	uuid, err := NewV4()
	if err != nil {
		panic(err)
	}
	return uuid
}

// NewV3 generates a UUID (version 3) based on MD5 hash of namespace and name
func NewV3(namespace UUID, name string) UUID {
	hash := md5.New()
	hash.Write(namespace[:])
	hash.Write([]byte(name))

	var uuid UUID
	copy(uuid[:], hash.Sum(nil))

	// Set version (3) and variant bits
	uuid[6] = (uuid[6] & 0x0f) | 0x30 // version 3
	uuid[8] = (uuid[8] & 0x3f) | 0x80  // variant RFC 4122

	return uuid
}

// NewV5 generates a UUID (version 5) based on SHA-1 hash of namespace and name
func NewV5(namespace UUID, name string) UUID {
	hash := sha1.New()
	hash.Write(namespace[:])
	hash.Write([]byte(name))

	var uuid UUID
	copy(uuid[:], hash.Sum(nil))

	// Set version (5) and variant bits
	uuid[6] = (uuid[6] & 0x0f) | 0x50 // version 5
	uuid[8] = (uuid[8] & 0x3f) | 0x80  // variant RFC 4122

	return uuid
}

// Parse parses a UUID string in standard format
func Parse(s string) (UUID, error) {
	// Remove braces and urn:uuid: prefix if present
	s = strings.Trim(s, "{}")
	s = strings.TrimPrefix(s, "urn:uuid:")
	s = strings.ReplaceAll(s, "-", "")

	if len(s) != 32 {
		return NilUUID, ErrInvalidUUID
	}

	var uuid UUID
	for i := 0; i < 16; i++ {
		b, err := hex.DecodeString(s[i*2 : i*2+2])
		if err != nil {
			return NilUUID, ErrInvalidUUID
		}
		uuid[i] = b[0]
	}

	return uuid, nil
}

// MustParse parses a UUID string, panics on error
func MustParse(s string) UUID {
	uuid, err := Parse(s)
	if err != nil {
		panic(err)
	}
	return uuid
}

// ParseOrNil parses a UUID string, returns NilUUID on error
func ParseOrNil(s string) UUID {
	uuid, err := Parse(s)
	if err != nil {
		return NilUUID
	}
	return uuid
}

// String returns the UUID in standard format
func (u UUID) String() string {
	return fmt.Sprintf("%08x-%04x-%04x-%04x-%012x",
		u[0:4], u[4:6], u[6:8], u[8:10], u[10:16])
}

// StringNoDash returns the UUID without dashes
func (u UUID) StringNoDash() string {
	return hex.EncodeToString(u[:])
}

// URN returns the UUID as a URN
func (u UUID) URN() string {
	return "urn:uuid:" + u.String()
}

// Bytes returns the UUID as a byte slice
func (u UUID) Bytes() []byte {
	return u[:]
}

// Version returns the UUID version
func (u UUID) Version() int {
	return int(u[6] >> 4)
}

// Variant returns the UUID variant
func (u UUID) Variant() int {
	switch {
	case (u[8] & 0x80) == 0x00:
		return VariantNCS
	case (u[8] & 0xc0) == 0x80:
		return VariantRFC4122
	case (u[8] & 0xe0) == 0xc0:
		return VariantMicrosoft
	default:
		return VariantFuture
	}
}

// IsNil checks if the UUID is the nil UUID
func (u UUID) IsNil() bool {
	return u == NilUUID
}

// IsValid checks if the UUID is valid (not nil and has valid format)
func (u UUID) IsValid() bool {
	return !u.IsNil()
}

// Equals compares two UUIDs for equality
func (u UUID) Equals(other UUID) bool {
	return u == other
}

// Compare compares two UUIDs lexicographically
func (u UUID) Compare(other UUID) int {
	for i := 0; i < 16; i++ {
		if u[i] < other[i] {
			return -1
		}
		if u[i] > other[i] {
			return 1
		}
	}
	return 0
}

// Time returns the timestamp for v1 UUIDs (returns error for other versions)
func (u UUID) Time() (time.Time, error) {
	if u.Version() != VersionV1 {
		return time.Time{}, ErrInvalidVersion
	}

	// Extract 60-bit timestamp
	var timestamp uint64
	timestamp = uint64(u[6]&0x0f) << 56
	timestamp |= uint64(u[7]) << 48
	timestamp |= uint64(u[4]) << 40
	timestamp |= uint64(u[5]) << 32
	timestamp |= uint64(u[0]) << 24
	timestamp |= uint64(u[1]) << 16
	timestamp |= uint64(u[2]) << 8
	timestamp |= uint64(u[3])

	// UUID epoch: October 15, 1582
	uuidEpoch := time.Date(1582, 10, 15, 0, 0, 0, 0, time.UTC)
	duration := time.Duration(timestamp) * 100 * time.Nanosecond

	return uuidEpoch.Add(duration), nil
}

// NodeID returns the node ID for v1 UUIDs
func (u UUID) NodeID() []byte {
	return u[10:16]
}

// ClockSeq returns the clock sequence for v1 UUIDs
func (u UUID) ClockSeq() uint16 {
	return uint16(u[8])<<8 | uint16(u[9])
}

// MarshalText implements encoding.TextMarshaler
func (u UUID) MarshalText() ([]byte, error) {
	return []byte(u.String()), nil
}

// UnmarshalText implements encoding.TextUnmarshaler
func (u *UUID) UnmarshalText(data []byte) error {
	parsed, err := Parse(string(data))
	if err != nil {
		return err
	}
	*u = parsed
	return nil
}

// MarshalBinary implements encoding.BinaryMarshaler
func (u UUID) MarshalBinary() ([]byte, error) {
	return u.Bytes(), nil
}

// UnmarshalBinary implements encoding.BinaryUnmarshaler
func (u *UUID) UnmarshalBinary(data []byte) error {
	if len(data) != 16 {
		return ErrInvalidUUID
	}
	copy(u[:], data)
	return nil
}

// IsValidString checks if a string is a valid UUID
func IsValidString(s string) bool {
	return uuidRegex.MatchString(s)
}

// GenerateV4Batch generates multiple v4 UUIDs at once
func GenerateV4Batch(count int) ([]UUID, error) {
	uuids := make([]UUID, count)
	for i := 0; i < count; i++ {
		uuid, err := NewV4()
		if err != nil {
			return nil, err
		}
		uuids[i] = uuid
	}
	return uuids, nil
}

// Short returns a shortened UUID string (first 8 characters)
func (u UUID) Short() string {
	return hex.EncodeToString(u[:4])
}

// ToUpper returns the UUID string in uppercase
func (u UUID) ToUpper() string {
	return strings.ToUpper(u.String())
}

// ToLower returns the UUID string in lowercase
func (u UUID) ToLower() string {
	return strings.ToLower(u.String())
}

// Format formats the UUID with a given format
func (u UUID) Format(format string) string {
	switch format {
	case "default", "":
		return u.String()
	case "nodash":
		return u.StringNoDash()
	case "urn":
		return u.URN()
	case "braces":
		return "{" + u.String() + "}"
	case "short":
		return u.Short()
	case "upper":
		return u.ToUpper()
	case "lower":
		return u.ToLower()
	default:
		return u.String()
	}
}

// ParseAny parses a UUID string in various formats
func ParseAny(s string) (UUID, error) {
	s = strings.TrimSpace(s)
	s = strings.Trim(s, "{}")

	// Handle URN prefix
	if strings.HasPrefix(strings.ToLower(s), "urn:uuid:") {
		s = strings.TrimPrefix(strings.ToLower(s), "urn:uuid:")
	}

	// Handle no-dash format
	if len(s) == 32 && strings.Count(s, "-") == 0 {
		// Insert dashes
		s = s[0:8] + "-" + s[8:12] + "-" + s[12:16] + "-" + s[16:20] + "-" + s[20:32]
	}

	return Parse(s)
}

// Generator creates a UUID generator with optional prefix
type Generator struct {
	prefix string
}

// NewGenerator creates a new UUID generator
func NewGenerator(prefix string) *Generator {
	return &Generator{prefix: prefix}
}

// Generate generates a new UUID with the configured prefix
func (g *Generator) Generate() (string, error) {
	uuid, err := NewV4()
	if err != nil {
		return "", err
	}
	return g.prefix + uuid.String(), nil
}

// MustGenerate generates a new UUID with prefix, panics on error
func (g *Generator) MustGenerate() string {
	s, err := g.Generate()
	if err != nil {
		panic(err)
	}
	return s
}

// ExtractUUID extracts the UUID part from a prefixed UUID string
func (g *Generator) ExtractUUID(s string) (UUID, error) {
	if !strings.HasPrefix(s, g.prefix) {
		return NilUUID, ErrInvalidUUID
	}
	return Parse(s[len(g.prefix):])
}

// Sort sorts a slice of UUIDs
func Sort(uuids []UUID) {
	for i := 0; i < len(uuids)-1; i++ {
		for j := i + 1; j < len(uuids); j++ {
			if uuids[i].Compare(uuids[j]) > 0 {
				uuids[i], uuids[j] = uuids[j], uuids[i]
			}
		}
	}
}

// Deduplicate removes duplicate UUIDs from a slice
func Deduplicate(uuids []UUID) []UUID {
	seen := make(map[UUID]bool)
	result := make([]UUID, 0)

	for _, uuid := range uuids {
		if !seen[uuid] {
			seen[uuid] = true
			result = append(result, uuid)
		}
	}

	return result
}

// Contains checks if a UUID is in a slice
func Contains(uuids []UUID, target UUID) bool {
	for _, uuid := range uuids {
		if uuid == target {
			return true
		}
	}
	return false
}

// IndexOf finds the index of a UUID in a slice, returns -1 if not found
func IndexOf(uuids []UUID, target UUID) int {
	for i, uuid := range uuids {
		if uuid == target {
			return i
		}
	}
	return -1
}

// Remove removes a UUID from a slice
func Remove(uuids []UUID, target UUID) []UUID {
	idx := IndexOf(uuids, target)
	if idx == -1 {
		return uuids
	}
	return append(uuids[:idx], uuids[idx+1:]...)
}

// Filter filters UUIDs based on a predicate
func Filter(uuids []UUID, predicate func(UUID) bool) []UUID {
	result := make([]UUID, 0)
	for _, uuid := range uuids {
		if predicate(uuid) {
			result = append(result, uuid)
		}
	}
	return result
}

// Map transforms UUIDs using a function
func Map(uuids []UUID, transform func(UUID) string) []string {
	result := make([]string, len(uuids))
	for i, uuid := range uuids {
		result[i] = transform(uuid)
	}
	return result
}

// Strings converts a slice of UUIDs to strings
func Strings(uuids []UUID) []string {
	return Map(uuids, func(u UUID) string { return u.String() })
}

// ParseStrings parses a slice of UUID strings
func ParseStrings(strs []string) ([]UUID, error) {
	uuids := make([]UUID, len(strs))
	for i, s := range strs {
		uuid, err := Parse(s)
		if err != nil {
			return nil, fmt.Errorf("error parsing UUID at index %d: %w", i, err)
		}
		uuids[i] = uuid
	}
	return uuids, nil
}

// Stats holds statistics about a collection of UUIDs
type Stats struct {
	Total      int
	VersionMap map[int]int
	VariantMap map[int]int
	NilCount   int
}

// Analyze analyzes a collection of UUIDs
func Analyze(uuids []UUID) Stats {
	stats := Stats{
		Total:      len(uuids),
		VersionMap: make(map[int]int),
		VariantMap: make(map[int]int),
	}

	for _, uuid := range uuids {
		stats.VersionMap[uuid.Version()]++
		stats.VariantMap[uuid.Variant()]++
		if uuid.IsNil() {
			stats.NilCount++
		}
	}

	return stats
}

// Equal checks if two UUID slices are equal
func Equal(a, b []UUID) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// Clone creates a copy of a UUID slice
func Clone(uuids []UUID) []UUID {
	result := make([]UUID, len(uuids))
	copy(result, uuids)
	return result
}