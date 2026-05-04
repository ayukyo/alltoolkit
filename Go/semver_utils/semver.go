// Package semver_utils provides semantic versioning utilities.
// Zero external dependencies - pure Go implementation.
package semver_utils

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

// Version represents a semantic version as defined by SemVer 2.0.0
// See: https://semver.org/
type Version struct {
	Major      uint64
	Minor      uint64
	Patch      uint64
	Prerelease []string
	Build      []string
	raw        string
}

var (
	// SemVer regex pattern according to SemVer 2.0.0 specification
	semverRegex = regexp.MustCompile(`^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$`)

	// Errors
	ErrInvalidVersion = errors.New("invalid semantic version")
	ErrInvalidPart    = errors.New("invalid version part")
)

// Parse parses a semantic version string into a Version struct.
// Returns ErrInvalidVersion if the string is not a valid semantic version.
func Parse(version string) (*Version, error) {
	if version == "" {
		return nil, ErrInvalidVersion
	}

	version = strings.TrimSpace(version)
	matches := semverRegex.FindStringSubmatch(version)

	if matches == nil {
		return nil, ErrInvalidVersion
	}

	v := &Version{raw: version}

	// Parse major
	major, err := strconv.ParseUint(matches[1], 10, 64)
	if err != nil {
		return nil, err
	}
	v.Major = major

	// Parse minor
	minor, err := strconv.ParseUint(matches[2], 10, 64)
	if err != nil {
		return nil, err
	}
	v.Minor = minor

	// Parse patch
	patch, err := strconv.ParseUint(matches[3], 10, 64)
	if err != nil {
		return nil, err
	}
	v.Patch = patch

	// Parse prerelease (optional)
	if matches[4] != "" {
		v.Prerelease = strings.Split(matches[4], ".")
	}

	// Parse build metadata (optional)
	if matches[5] != "" {
		v.Build = strings.Split(matches[5], ".")
	}

	return v, nil
}

// MustParse parses a semantic version string and panics if it's invalid.
// Use this only when you're certain the version is valid.
func MustParse(version string) *Version {
	v, err := Parse(version)
	if err != nil {
		panic(fmt.Sprintf("semver: %s: %v", version, err))
	}
	return v
}

// String returns the string representation of the version.
func (v *Version) String() string {
	if v.raw != "" {
		return v.raw
	}
	return v.buildString()
}

func (v *Version) buildString() string {
	var sb strings.Builder

	sb.WriteString(strconv.FormatUint(v.Major, 10))
	sb.WriteByte('.')
	sb.WriteString(strconv.FormatUint(v.Minor, 10))
	sb.WriteByte('.')
	sb.WriteString(strconv.FormatUint(v.Patch, 10))

	if len(v.Prerelease) > 0 {
		sb.WriteByte('-')
		sb.WriteString(strings.Join(v.Prerelease, "."))
	}

	if len(v.Build) > 0 {
		sb.WriteByte('+')
		sb.WriteString(strings.Join(v.Build, "."))
	}

	return sb.String()
}

// IsPrerelease returns true if the version has prerelease information.
func (v *Version) IsPrerelease() bool {
	return len(v.Prerelease) > 0
}

// HasBuild returns true if the version has build metadata.
func (v *Version) HasBuild() bool {
	return len(v.Build) > 0
}

// Compare compares two versions.
// Returns:
//   -1 if v < other
//   0 if v == other
//   1 if v > other
func (v *Version) Compare(other *Version) int {
	// Compare major
	if v.Major != other.Major {
		if v.Major < other.Major {
			return -1
		}
		return 1
	}

	// Compare minor
	if v.Minor != other.Minor {
		if v.Minor < other.Minor {
			return -1
		}
		return 1
	}

	// Compare patch
	if v.Patch != other.Patch {
		if v.Patch < other.Patch {
			return -1
		}
		return 1
	}

	// Prerelease versions have lower precedence than normal versions
	vHasPre := v.IsPrerelease()
	otherHasPre := other.IsPrerelease()

	if vHasPre && !otherHasPre {
		return -1
	}
	if !vHasPre && otherHasPre {
		return 1
	}

	// Compare prerelease identifiers
	return v.comparePrerelease(other)
}

func (v *Version) comparePrerelease(other *Version) int {
	pre1 := v.Prerelease
	pre2 := other.Prerelease

	maxLen := len(pre1)
	if len(pre2) > maxLen {
		maxLen = len(pre2)
	}

	for i := 0; i < maxLen; i++ {
		if i >= len(pre1) {
			return -1 // shorter prerelease has higher precedence
		}
		if i >= len(pre2) {
			return 1
		}

		cmp := comparePrereleaseIdentifiers(pre1[i], pre2[i])
		if cmp != 0 {
			return cmp
		}
	}

	return 0
}

func comparePrereleaseIdentifiers(a, b string) int {
	numA, errA := strconv.ParseInt(a, 10, 64)
	numB, errB := strconv.ParseInt(b, 10, 64)

	// Numeric identifiers always have lower precedence than alphanumeric
	if errA == nil && errB != nil {
		return -1
	}
	if errA != nil && errB == nil {
		return 1
	}

	// Both numeric
	if errA == nil && errB == nil {
		if numA < numB {
			return -1
		}
		if numA > numB {
			return 1
		}
		return 0
	}

	// Both alphanumeric - compare lexically
	if a < b {
		return -1
	}
	if a > b {
		return 1
	}
	return 0
}

// LessThan returns true if v < other.
func (v *Version) LessThan(other *Version) bool {
	return v.Compare(other) < 0
}

// LessThanOrEqual returns true if v <= other.
func (v *Version) LessThanOrEqual(other *Version) bool {
	return v.Compare(other) <= 0
}

// GreaterThan returns true if v > other.
func (v *Version) GreaterThan(other *Version) bool {
	return v.Compare(other) > 0
}

// GreaterThanOrEqual returns true if v >= other.
func (v *Version) GreaterThanOrEqual(other *Version) bool {
	return v.Compare(other) >= 0
}

// Equal returns true if v == other.
func (v *Version) Equal(other *Version) bool {
	return v.Compare(other) == 0
}

// BumpMajor increments the major version and resets minor and patch to 0.
// Removes prerelease and build metadata.
func (v *Version) BumpMajor() *Version {
	return &Version{
		Major: v.Major + 1,
		Minor: 0,
		Patch: 0,
	}
}

// BumpMinor increments the minor version and resets patch to 0.
// Removes prerelease and build metadata.
func (v *Version) BumpMinor() *Version {
	return &Version{
		Major: v.Major,
		Minor: v.Minor + 1,
		Patch: 0,
	}
}

// BumpPatch increments the patch version.
// Removes prerelease and build metadata.
func (v *Version) BumpPatch() *Version {
	return &Version{
		Major: v.Major,
		Minor: v.Minor,
		Patch: v.Patch + 1,
	}
}

// SetPrerelease returns a copy of the version with the given prerelease identifiers.
func (v *Version) SetPrerelease(identifiers ...string) (*Version, error) {
	for _, id := range identifiers {
		if !isValidPrereleaseIdentifier(id) {
			return nil, fmt.Errorf("%w: invalid prerelease identifier: %s", ErrInvalidPart, id)
		}
	}
	return &Version{
		Major:      v.Major,
		Minor:      v.Minor,
		Patch:      v.Patch,
		Prerelease: identifiers,
		Build:      v.Build,
	}, nil
}

// SetBuild returns a copy of the version with the given build metadata.
func (v *Version) SetBuild(metadata ...string) (*Version, error) {
	for _, m := range metadata {
		if !isValidBuildMetadata(m) {
			return nil, fmt.Errorf("%w: invalid build metadata: %s", ErrInvalidPart, m)
		}
	}
	return &Version{
		Major:      v.Major,
		Minor:      v.Minor,
		Patch:      v.Patch,
		Prerelease: v.Prerelease,
		Build:      metadata,
	}, nil
}

// WithoutPrerelease returns a copy of the version without prerelease information.
func (v *Version) WithoutPrerelease() *Version {
	return &Version{
		Major: v.Major,
		Minor: v.Minor,
		Patch: v.Patch,
		Build: v.Build,
	}
}

// WithoutBuild returns a copy of the version without build metadata.
func (v *Version) WithoutBuild() *Version {
	return &Version{
		Major:      v.Major,
		Minor:      v.Minor,
		Patch:      v.Patch,
		Prerelease: v.Prerelease,
	}
}

// Clean returns a clean version without prerelease or build metadata.
func (v *Version) Clean() *Version {
	return &Version{
		Major: v.Major,
		Minor: v.Minor,
		Patch: v.Patch,
	}
}

// Validate returns nil if the version string is a valid semantic version.
func Validate(version string) error {
	_, err := Parse(version)
	return err
}

// IsValid returns true if the version string is a valid semantic version.
func IsValid(version string) bool {
	return semverRegex.MatchString(strings.TrimSpace(version))
}

func isValidPrereleaseIdentifier(id string) bool {
	if id == "" {
		return false
	}
	// Must be alphanumeric or hyphen, can't start with leading zero if numeric
	if matched, _ := regexp.MatchString(`^(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)$`, id); !matched {
		return false
	}
	return true
}

func isValidBuildMetadata(meta string) bool {
	if meta == "" {
		return false
	}
	matched, _ := regexp.MatchString(`^[0-9a-zA-Z-]+$`, meta)
	return matched
}

// Sort sorts a slice of versions in ascending order.
func Sort(versions []*Version) {
	for i := 0; i < len(versions)-1; i++ {
		for j := i + 1; j < len(versions); j++ {
			if versions[i].GreaterThan(versions[j]) {
				versions[i], versions[j] = versions[j], versions[i]
			}
		}
	}
}

// SortDescending sorts a slice of versions in descending order.
func SortDescending(versions []*Version) {
	for i := 0; i < len(versions)-1; i++ {
		for j := i + 1; j < len(versions); j++ {
			if versions[i].LessThan(versions[j]) {
				versions[i], versions[j] = versions[j], versions[i]
			}
		}
	}
}

// Max returns the maximum version from a slice.
// Returns nil if the slice is empty.
func Max(versions []*Version) *Version {
	if len(versions) == 0 {
		return nil
	}
	max := versions[0]
	for _, v := range versions[1:] {
		if v.GreaterThan(max) {
			max = v
		}
	}
	return max
}

// Min returns the minimum version from a slice.
// Returns nil if the slice is empty.
func Min(versions []*Version) *Version {
	if len(versions) == 0 {
		return nil
	}
	min := versions[0]
	for _, v := range versions[1:] {
		if v.LessThan(min) {
			min = v
		}
	}
	return min
}

// NewVersion creates a new Version with the given major, minor, and patch.
func NewVersion(major, minor, patch uint64) *Version {
	return &Version{
		Major: major,
		Minor: minor,
		Patch: patch,
	}
}