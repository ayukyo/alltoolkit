package semver_utils

import (
	"testing"
)

func TestParse(t *testing.T) {
	tests := []struct {
		name      string
		input     string
		wantMajor uint64
		wantMinor uint64
		wantPatch uint64
		wantPre   string
		wantBuild string
		wantErr   bool
	}{
		{
			name:      "simple version",
			input:     "1.2.3",
			wantMajor: 1,
			wantMinor: 2,
			wantPatch: 3,
		},
		{
			name:      "version with prerelease",
			input:     "1.0.0-alpha",
			wantMajor: 1,
			wantMinor: 0,
			wantPatch: 0,
			wantPre:   "alpha",
		},
		{
			name:      "version with prerelease and build",
			input:     "1.0.0-alpha+build.123",
			wantMajor: 1,
			wantMinor: 0,
			wantPatch: 0,
			wantPre:   "alpha",
			wantBuild: "build.123",
		},
		{
			name:      "version with multiple prerelease identifiers",
			input:     "2.1.0-alpha.beta.1",
			wantMajor: 2,
			wantMinor: 1,
			wantPatch: 0,
			wantPre:   "alpha.beta.1",
		},
		{
			name:      "version with build metadata",
			input:     "1.2.3+20130313144700",
			wantMajor: 1,
			wantMinor: 2,
			wantPatch: 3,
			wantBuild: "20130313144700",
		},
		{
			name:      "zero version",
			input:     "0.0.0",
			wantMajor: 0,
			wantMinor: 0,
			wantPatch: 0,
		},
		{
			name:      "large version numbers",
			input:     "999.888.777",
			wantMajor: 999,
			wantMinor: 888,
			wantPatch: 777,
		},
		{
			name:    "invalid - missing patch",
			input:   "1.2",
			wantErr: true,
		},
		{
			name:    "invalid - missing minor and patch",
			input:   "1",
			wantErr: true,
		},
		{
			name:    "invalid - leading zeros in major",
			input:   "01.2.3",
			wantErr: true,
		},
		{
			name:    "invalid - leading zeros in minor",
			input:   "1.02.3",
			wantErr: true,
		},
		{
			name:    "invalid - letters in version",
			input:   "a.b.c",
			wantErr: true,
		},
		{
			name:    "invalid - empty string",
			input:   "",
			wantErr: true,
		},
		{
			name:      "version with hyphen in prerelease",
			input:     "1.0.0-alpha-1",
			wantMajor: 1,
			wantMinor: 0,
			wantPatch: 0,
			wantPre:   "alpha-1",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			v, err := Parse(tt.input)
			if tt.wantErr {
				if err == nil {
					t.Errorf("Parse(%q) expected error, got nil", tt.input)
				}
				return
			}
			if err != nil {
				t.Errorf("Parse(%q) unexpected error: %v", tt.input, err)
				return
			}
			if v.Major != tt.wantMajor {
				t.Errorf("Major = %d, want %d", v.Major, tt.wantMajor)
			}
			if v.Minor != tt.wantMinor {
				t.Errorf("Minor = %d, want %d", v.Minor, tt.wantMinor)
			}
			if v.Patch != tt.wantPatch {
				t.Errorf("Patch = %d, want %d", v.Patch, tt.wantPatch)
			}
			if tt.wantPre != "" && v.Prerelease == nil {
				t.Errorf("Prerelease is nil, want %s", tt.wantPre)
			}
			if tt.wantPre != "" {
				preStr := joinPrerelease(v)
				if preStr != tt.wantPre {
					t.Errorf("Prerelease = %s, want %s", preStr, tt.wantPre)
				}
			}
		})
	}
}

func joinPrerelease(v *Version) string {
	result := ""
	for i, p := range v.Prerelease {
		if i > 0 {
			result += "."
		}
		result += p
	}
	return result
}

func TestString(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{
			name:  "simple version",
			input: "1.2.3",
			want:  "1.2.3",
		},
		{
			name:  "version with prerelease",
			input: "1.0.0-alpha",
			want:  "1.0.0-alpha",
		},
		{
			name:  "full version",
			input: "2.0.0-beta.1+build.123",
			want:  "2.0.0-beta.1+build.123",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			v, err := Parse(tt.input)
			if err != nil {
				t.Fatalf("Parse error: %v", err)
			}
			if got := v.String(); got != tt.want {
				t.Errorf("String() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestCompare(t *testing.T) {
	tests := []struct {
		name     string
		v1       string
		v2       string
		wantCmp  int
		wantLess bool
		wantGt   bool
		wantEq   bool
	}{
		{
			name:     "equal versions",
			v1:       "1.0.0",
			v2:       "1.0.0",
			wantCmp:  0,
			wantLess: false,
			wantGt:   false,
			wantEq:   true,
		},
		{
			name:     "major version difference",
			v1:       "2.0.0",
			v2:       "1.0.0",
			wantCmp:  1,
			wantLess: false,
			wantGt:   true,
			wantEq:   false,
		},
		{
			name:     "minor version difference",
			v1:       "1.1.0",
			v2:       "1.2.0",
			wantCmp:  -1,
			wantLess: true,
			wantGt:   false,
			wantEq:   false,
		},
		{
			name:     "patch version difference",
			v1:       "1.0.2",
			v2:       "1.0.1",
			wantCmp:  1,
			wantLess: false,
			wantGt:   true,
			wantEq:   false,
		},
		{
			name:     "prerelease has lower precedence",
			v1:       "1.0.0-alpha",
			v2:       "1.0.0",
			wantCmp:  -1,
			wantLess: true,
			wantGt:   false,
			wantEq:   false,
		},
		{
			name:     "prerelease comparison alpha vs beta",
			v1:       "1.0.0-alpha",
			v2:       "1.0.0-beta",
			wantCmp:  -1,
			wantLess: true,
			wantGt:   false,
			wantEq:   false,
		},
		{
			name:     "numeric prerelease comparison",
			v1:       "1.0.0-alpha.1",
			v2:       "1.0.0-alpha.2",
			wantCmp:  -1,
			wantLess: true,
			wantGt:   false,
			wantEq:   false,
		},
		{
			name:     "numeric vs alphanumeric prerelease",
			v1:       "1.0.0-alpha.1",
			v2:       "1.0.0-alpha.beta",
			wantCmp:  -1,
			wantLess: true,
			wantGt:   false,
			wantEq:   false,
		},
		{
			name:     "build metadata is ignored",
			v1:       "1.0.0+build1",
			v2:       "1.0.0+build2",
			wantCmp:  0,
			wantLess: false,
			wantGt:   false,
			wantEq:   true,
		},
		{
			name:     "complex prerelease",
			v1:       "1.0.0-alpha.1.2",
			v2:       "1.0.0-alpha.1.3",
			wantCmp:  -1,
			wantLess: true,
			wantGt:   false,
			wantEq:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			v1, err := Parse(tt.v1)
			if err != nil {
				t.Fatalf("Parse v1 error: %v", err)
			}
			v2, err := Parse(tt.v2)
			if err != nil {
				t.Fatalf("Parse v2 error: %v", err)
			}

			if got := v1.Compare(v2); got != tt.wantCmp {
				t.Errorf("Compare() = %d, want %d", got, tt.wantCmp)
			}
			if got := v1.LessThan(v2); got != tt.wantLess {
				t.Errorf("LessThan() = %v, want %v", got, tt.wantLess)
			}
			if got := v1.GreaterThan(v2); got != tt.wantGt {
				t.Errorf("GreaterThan() = %v, want %v", got, tt.wantGt)
			}
			if got := v1.Equal(v2); got != tt.wantEq {
				t.Errorf("Equal() = %v, want %v", got, tt.wantEq)
			}
		})
	}
}

func TestBump(t *testing.T) {
	v, err := Parse("1.2.3")
	if err != nil {
		t.Fatalf("Parse error: %v", err)
	}

	majorBumped := v.BumpMajor()
	if majorBumped.String() != "2.0.0" {
		t.Errorf("BumpMajor() = %s, want 2.0.0", majorBumped.String())
	}

	minorBumped := v.BumpMinor()
	if minorBumped.String() != "1.3.0" {
		t.Errorf("BumpMinor() = %s, want 1.3.0", minorBumped.String())
	}

	patchBumped := v.BumpPatch()
	if patchBumped.String() != "1.2.4" {
		t.Errorf("BumpPatch() = %s, want 1.2.4", patchBumped.String())
	}
}

func TestBumpWithPrerelease(t *testing.T) {
	v, err := Parse("1.2.3-alpha.1+build")
	if err != nil {
		t.Fatalf("Parse error: %v", err)
	}

	majorBumped := v.BumpMajor()
	if majorBumped.String() != "2.0.0" {
		t.Errorf("BumpMajor() = %s, want 2.0.0", majorBumped.String())
	}
	if majorBumped.IsPrerelease() {
		t.Error("Bumped version should not be prerelease")
	}
}

func TestSetPrerelease(t *testing.T) {
	v, err := Parse("1.2.3")
	if err != nil {
		t.Fatalf("Parse error: %v", err)
	}

	newV, err := v.SetPrerelease("alpha", "1")
	if err != nil {
		t.Fatalf("SetPrerelease error: %v", err)
	}
	if newV.String() != "1.2.3-alpha.1" {
		t.Errorf("SetPrerelease() = %s, want 1.2.3-alpha.1", newV.String())
	}
	if !newV.IsPrerelease() {
		t.Error("Version should be prerelease")
	}
}

func TestSetBuild(t *testing.T) {
	v, err := Parse("1.2.3")
	if err != nil {
		t.Fatalf("Parse error: %v", err)
	}

	newV, err := v.SetBuild("build", "123")
	if err != nil {
		t.Fatalf("SetBuild error: %v", err)
	}
	if newV.String() != "1.2.3+build.123" {
		t.Errorf("SetBuild() = %s, want 1.2.3+build.123", newV.String())
	}
	if !newV.HasBuild() {
		t.Error("Version should have build metadata")
	}
}

func TestClean(t *testing.T) {
	v, err := Parse("1.2.3-alpha.1+build.123")
	if err != nil {
		t.Fatalf("Parse error: %v", err)
	}

	clean := v.Clean()
	if clean.String() != "1.2.3" {
		t.Errorf("Clean() = %s, want 1.2.3", clean.String())
	}
}

func TestSort(t *testing.T) {
	versions := []*Version{
		MustParse("3.0.0"),
		MustParse("1.0.0"),
		MustParse("2.0.0"),
		MustParse("1.0.0-alpha"),
		MustParse("1.0.0-beta"),
	}

	Sort(versions)

	expected := []string{"1.0.0-alpha", "1.0.0-beta", "1.0.0", "2.0.0", "3.0.0"}
	for i, v := range versions {
		if v.String() != expected[i] {
			t.Errorf("Sort()[%d] = %s, want %s", i, v.String(), expected[i])
		}
	}
}

func TestMaxMin(t *testing.T) {
	versions := []*Version{
		MustParse("1.0.0"),
		MustParse("3.0.0"),
		MustParse("2.0.0"),
	}

	max := Max(versions)
	if max.String() != "3.0.0" {
		t.Errorf("Max() = %s, want 3.0.0", max.String())
	}

	min := Min(versions)
	if min.String() != "1.0.0" {
		t.Errorf("Min() = %s, want 1.0.0", min.String())
	}

	emptyMax := Max([]*Version{})
	if emptyMax != nil {
		t.Error("Max of empty slice should be nil")
	}

	emptyMin := Min([]*Version{})
	if emptyMin != nil {
		t.Error("Min of empty slice should be nil")
	}
}

func TestIsValid(t *testing.T) {
	tests := []struct {
		input string
		want  bool
	}{
		{"1.0.0", true},
		{"0.0.1", true},
		{"10.20.30", true},
		{"1.0.0-alpha", true},
		{"1.0.0-alpha.1", true},
		{"1.0.0+build", true},
		{"1.0.0-alpha+build", true},
		{"v1.0.0", false}, // 'v' prefix not allowed in strict semver
		{"1.0", false},
		{"1.0.0.0", false},
		{"a.b.c", false},
		{"", false},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			if got := IsValid(tt.input); got != tt.want {
				t.Errorf("IsValid(%q) = %v, want %v", tt.input, got, tt.want)
			}
		})
	}
}

func TestNewVersion(t *testing.T) {
	v := NewVersion(1, 2, 3)
	if v.String() != "1.2.3" {
		t.Errorf("NewVersion() = %s, want 1.2.3", v.String())
	}
}

func TestMustParsePanic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("MustParse should panic on invalid version")
		}
	}()
	MustParse("invalid")
}

func TestLessThanOrEqual(t *testing.T) {
	v1 := MustParse("1.0.0")
	v2 := MustParse("1.0.0")
	v3 := MustParse("2.0.0")

	if !v1.LessThanOrEqual(v2) {
		t.Error("1.0.0 should be <= 1.0.0")
	}
	if !v1.LessThanOrEqual(v3) {
		t.Error("1.0.0 should be <= 2.0.0")
	}
	if v3.LessThanOrEqual(v1) {
		t.Error("2.0.0 should not be <= 1.0.0")
	}
}

func TestGreaterThanOrEqual(t *testing.T) {
	v1 := MustParse("1.0.0")
	v2 := MustParse("1.0.0")
	v3 := MustParse("2.0.0")

	if !v3.GreaterThanOrEqual(v1) {
		t.Error("2.0.0 should be >= 1.0.0")
	}
	if !v2.GreaterThanOrEqual(v1) {
		t.Error("1.0.0 should be >= 1.0.0")
	}
	if v1.GreaterThanOrEqual(v3) {
		t.Error("1.0.0 should not be >= 2.0.0")
	}
}