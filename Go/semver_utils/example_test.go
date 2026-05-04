package semver_utils

import "fmt"

// Example_basicParsing demonstrates basic version parsing.
func Example_basicParsing() {
	v, err := Parse("1.2.3")
	if err != nil {
		panic(err)
	}
	fmt.Printf("Major: %d, Minor: %d, Patch: %d\n", v.Major, v.Minor, v.Patch)
	// Output: Major: 1, Minor: 2, Patch: 3
}

// Example_versionWithPrerelease demonstrates parsing versions with prerelease info.
func Example_versionWithPrerelease() {
	v, err := Parse("2.0.0-beta.1")
	if err != nil {
		panic(err)
	}
	fmt.Printf("Version: %s\n", v.String())
	fmt.Printf("Is prerelease: %v\n", v.IsPrerelease())
	fmt.Printf("Prerelease: %v\n", v.Prerelease)
	// Output:
	// Version: 2.0.0-beta.1
	// Is prerelease: true
	// Prerelease: [beta 1]
}

// Example_versionWithBuild demonstrates parsing versions with build metadata.
func Example_versionWithBuild() {
	v, err := Parse("1.0.0+build.123")
	if err != nil {
		panic(err)
	}
	fmt.Printf("Version: %s\n", v.String())
	fmt.Printf("Has build: %v\n", v.HasBuild())
	fmt.Printf("Build: %v\n", v.Build)
	// Output:
	// Version: 1.0.0+build.123
	// Has build: true
	// Build: [build 123]
}

// Example_comparingVersions demonstrates version comparison.
func Example_comparingVersions() {
	v1 := MustParse("1.0.0")
	v2 := MustParse("2.0.0")

	if v1.LessThan(v2) {
		fmt.Println("v1 is less than v2")
	}
	if v2.GreaterThan(v1) {
		fmt.Println("v2 is greater than v1")
	}
	// Output:
	// v1 is less than v2
	// v2 is greater than v1
}

// Example_prereleasePrecedence demonstrates prerelease version precedence.
func Example_prereleasePrecedence() {
	release := MustParse("1.0.0")
	alpha := MustParse("1.0.0-alpha")
	beta := MustParse("1.0.0-beta")

	fmt.Printf("alpha < release: %v\n", alpha.LessThan(release))
	fmt.Printf("alpha < beta: %v\n", alpha.LessThan(beta))
	// Output:
	// alpha < release: true
	// alpha < beta: true
}

// Example_bumpingVersions demonstrates version bumping.
func Example_bumpingVersions() {
	v := MustParse("1.2.3")

	fmt.Printf("Original: %s\n", v.String())
	fmt.Printf("Bump Major: %s\n", v.BumpMajor().String())
	fmt.Printf("Bump Minor: %s\n", v.BumpMinor().String())
	fmt.Printf("Bump Patch: %s\n", v.BumpPatch().String())
	// Output:
	// Original: 1.2.3
	// Bump Major: 2.0.0
	// Bump Minor: 1.3.0
	// Bump Patch: 1.2.4
}

// Example_sortingVersions demonstrates sorting a slice of versions.
func Example_sortingVersions() {
	versions := []*Version{
		MustParse("3.0.0"),
		MustParse("1.0.0"),
		MustParse("2.0.0-alpha"),
		MustParse("2.0.0"),
	}

	Sort(versions)
	for _, v := range versions {
		fmt.Println(v.String())
	}
	// Output:
	// 1.0.0
	// 2.0.0-alpha
	// 2.0.0
	// 3.0.0
}

// Example_findingMaxMin demonstrates finding max and min versions.
func Example_findingMaxMin() {
	versions := []*Version{
		MustParse("1.5.0"),
		MustParse("2.0.0"),
		MustParse("0.9.0"),
	}

	fmt.Printf("Max: %s\n", Max(versions).String())
	fmt.Printf("Min: %s\n", Min(versions).String())
	// Output:
	// Max: 2.0.0
	// Min: 0.9.0
}

// Example_modifyingVersion demonstrates creating modified versions.
func Example_modifyingVersion() {
	v := MustParse("1.2.3")

	// Add prerelease
	vWithPre, _ := v.SetPrerelease("alpha", "1")
	fmt.Printf("With prerelease: %s\n", vWithPre.String())

	// Add build metadata
	vWithBuild, _ := v.SetBuild("build", "20240101")
	fmt.Printf("With build: %s\n", vWithBuild.String())

	// Clean version
	fullVersion := MustParse("1.2.3-alpha.1+build.123")
	clean := fullVersion.Clean()
	fmt.Printf("Cleaned: %s\n", clean.String())
	// Output:
	// With prerelease: 1.2.3-alpha.1
	// With build: 1.2.3+build.20240101
	// Cleaned: 1.2.3
}

// Example_validation demonstrates version validation.
func Example_validation() {
	valid := IsValid("1.0.0")
	invalid := IsValid("v1.0.0") // 'v' prefix not allowed in strict semver

	fmt.Printf("1.0.0 is valid: %v\n", valid)
	fmt.Printf("v1.0.0 is valid: %v\n", invalid)
	// Output:
	// 1.0.0 is valid: true
	// v1.0.0 is valid: false
}

// Example_newVersion demonstrates creating a version programmatically.
func Example_newVersion() {
	v := NewVersion(2, 1, 0)
	fmt.Printf("Created version: %s\n", v.String())
	// Output: Created version: 2.1.0
}