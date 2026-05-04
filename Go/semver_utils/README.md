# semver_utils

Semantic Versioning (SemVer 2.0.0) utilities for Go with zero external dependencies.

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/semver_utils"
```

## Features

- **Parsing**: Parse semantic version strings with full validation
- **Comparison**: Compare versions according to SemVer precedence rules
- **Modification**: Bump versions, add/remove prerelease and build metadata
- **Sorting**: Sort slices of versions
- **Validation**: Validate version strings
- **Zero dependencies**: Pure Go implementation

## Quick Start

### Parsing Versions

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/semver_utils"
)

func main() {
    // Parse a version
    v, err := semver_utils.Parse("1.2.3-alpha.1+build.123")
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Major: %d\n", v.Major)      // Major: 1
    fmt.Printf("Minor: %d\n", v.Minor)      // Minor: 2
    fmt.Printf("Patch: %d\n", v.Patch)      // Patch: 3
    fmt.Printf("Prerelease: %v\n", v.Prerelease)  // Prerelease: [alpha 1]
    fmt.Printf("Build: %v\n", v.Build)      // Build: [build 123]
}
```

### Comparing Versions

```go
v1 := semver_utils.MustParse("1.0.0")
v2 := semver_utils.MustParse("2.0.0")

// Comparison methods
v1.LessThan(v2)           // true
v1.LessThanOrEqual(v2)    // true
v1.GreaterThan(v2)        // false
v1.GreaterThanOrEqual(v2) // false
v1.Equal(v2)              // false

// Or use Compare for -1, 0, 1 result
v1.Compare(v2)  // -1
```

### Prerelease Precedence

```go
release := semver_utils.MustParse("1.0.0")
alpha := semver_utils.MustParse("1.0.0-alpha")
beta := semver_utils.MustParse("1.0.0-beta")

alpha.LessThan(release)  // true (prerelease < release)
alpha.LessThan(beta)      // true (alpha < beta)
```

### Bumping Versions

```go
v := semver_utils.MustParse("1.2.3")

v.BumpMajor()  // "2.0.0"
v.BumpMinor()  // "1.3.0"
v.BumpPatch()  // "1.2.4"
```

### Modifying Versions

```go
v := semver_utils.MustParse("1.2.3")

// Add prerelease
vWithPre, _ := v.SetPrerelease("alpha", "1")
fmt.Println(vWithPre.String())  // "1.2.3-alpha.1"

// Add build metadata
vWithBuild, _ := v.SetBuild("build", "20240101")
fmt.Println(vWithBuild.String())  // "1.2.3+build.20240101"

// Get clean version (without prerelease/build)
fullVersion := semver_utils.MustParse("1.2.3-alpha+build")
clean := fullVersion.Clean()
fmt.Println(clean.String())  // "1.2.3"
```

### Sorting Versions

```go
versions := []*semver_utils.Version{
    semver_utils.MustParse("3.0.0"),
    semver_utils.MustParse("1.0.0"),
    semver_utils.MustParse("2.0.0-alpha"),
    semver_utils.MustParse("2.0.0"),
}

semver_utils.Sort(versions)
// Result: ["1.0.0", "2.0.0-alpha", "2.0.0", "3.0.0"]
```

### Finding Max/Min

```go
versions := []*semver_utils.Version{
    semver_utils.MustParse("1.5.0"),
    semver_utils.MustParse("2.0.0"),
    semver_utils.MustParse("0.9.0"),
}

max := semver_utils.Max(versions)  // "2.0.0"
min := semver_utils.Min(versions)  // "0.9.0"
```

### Validation

```go
// Quick validation check
semver_utils.IsValid("1.0.0")      // true
semver_utils.IsValid("v1.0.0")     // false ('v' prefix not allowed)
semver_utils.IsValid("1.0")        // false (missing patch)

// Validation with error details
err := semver_utils.Validate("invalid")
if err != nil {
    fmt.Println("Invalid version:", err)
}
```

### Creating Versions Programmatically

```go
v := semver_utils.NewVersion(2, 1, 0)
fmt.Println(v.String())  // "2.1.0"
```

## API Reference

### Types

```go
type Version struct {
    Major      uint64   // Major version number
    Minor      uint64   // Minor version number
    Patch      uint64   // Patch version number
    Prerelease []string // Prerelease identifiers (e.g., ["alpha", "1"])
    Build      []string // Build metadata (e.g., ["build", "123"])
}
```

### Functions

| Function | Description |
|----------|-------------|
| `Parse(string) (*Version, error)` | Parse a semantic version string |
| `MustParse(string) *Version` | Parse and panic on error |
| `NewVersion(major, minor, patch uint64) *Version` | Create a new version |
| `IsValid(string) bool` | Check if string is a valid semver |
| `Validate(string) error` | Validate and return error details |
| `Sort([]*Version)` | Sort versions in ascending order |
| `SortDescending([]*Version)` | Sort versions in descending order |
| `Max([]*Version) *Version` | Return maximum version |
| `Min([]*Version) *Version` | Return minimum version |

### Version Methods

| Method | Description |
|--------|-------------|
| `String() string` | Return string representation |
| `Compare(*Version) int` | Compare with another version (-1, 0, 1) |
| `LessThan(*Version) bool` | Check if less than |
| `LessThanOrEqual(*Version) bool` | Check if less than or equal |
| `GreaterThan(*Version) bool` | Check if greater than |
| `GreaterThanOrEqual(*Version) bool` | Check if greater than or equal |
| `Equal(*Version) bool` | Check if equal |
| `IsPrerelease() bool` | Check if has prerelease |
| `HasBuild() bool` | Check if has build metadata |
| `BumpMajor() *Version` | Increment major, reset minor/patch |
| `BumpMinor() *Version` | Increment minor, reset patch |
| `BumpPatch() *Version` | Increment patch |
| `SetPrerelease(...string) (*Version, error)` | Set prerelease |
| `SetBuild(...string) (*Version, error)` | Set build metadata |
| `WithoutPrerelease() *Version` | Remove prerelease |
| `WithoutBuild() *Version` | Remove build metadata |
| `Clean() *Version` | Remove both prerelease and build |

## SemVer 2.0.0 Compliance

This implementation follows [Semantic Versioning 2.0.0](https://semver.org/) specification:

- ✅ Major.Minor.Patch format
- ✅ Prerelease identifiers (e.g., `-alpha.1`)
- ✅ Build metadata (e.g., `+build.123`)
- ✅ Precedence rules (prerelease < release)
- ✅ Numeric identifiers have lower precedence than alphanumeric
- ✅ Build metadata ignored in comparisons

## License

MIT License