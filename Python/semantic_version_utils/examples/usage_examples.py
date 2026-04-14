"""
Semantic Version Utilities - Usage Examples

This file demonstrates practical use cases for semantic version handling.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SemanticVersion,
    VersionRange,
    VersionSet,
    parse,
    is_valid,
    compare,
    sort_versions,
    min_version,
    max_version,
    satisfies,
    coerce,
    diff,
    is_compatible,
    next_version,
)


def example_basic_parsing():
    """Basic version parsing examples."""
    print("\n" + "=" * 50)
    print("Basic Version Parsing")
    print("=" * 50)
    
    # Parse simple version
    v = parse("1.2.3")
    print(f"\nParsed '1.2.3':")
    print(f"  Major: {v.major}")
    print(f"  Minor: {v.minor}")
    print(f"  Patch: {v.patch}")
    
    # Parse version with prerelease
    v = parse("2.0.0-beta.1")
    print(f"\nParsed '2.0.0-beta.1':")
    print(f"  Version: {v}")
    print(f"  Prerelease: {v.prerelease}")
    print(f"  Is prerelease: {v.is_prerelease}")
    
    # Parse version with build metadata
    v = parse("3.1.4+build.20240115")
    print(f"\nParsed '3.1.4+build.20240115':")
    print(f"  Version: {v}")
    print(f"  Build: {v.build}")
    
    # Validate version strings
    print(f"\nIs '1.0.0' valid? {is_valid('1.0.0')}")
    print(f"Is 'v1.0.0' valid? {is_valid('v1.0.0')}")
    print(f"Is '1.0' valid? {is_valid('1.0')}")


def example_version_comparison():
    """Version comparison examples."""
    print("\n" + "=" * 50)
    print("Version Comparison")
    print("=" * 50)
    
    v1 = parse("1.0.0")
    v2 = parse("2.0.0")
    v3 = parse("1.0.0-alpha")
    v4 = parse("1.0.0")
    
    print(f"\nCompare {v1} and {v2}:")
    print(f"  v1 < v2: {v1 < v2}")
    print(f"  v1 > v2: {v1 > v2}")
    
    print(f"\nCompare {v3} and {v4}:")
    print(f"  Prerelease < Release: {v3 < v4}")
    
    print(f"\nUsing compare() function:")
    print(f"  compare('1.0.0', '2.0.0'): {compare('1.0.0', '2.0.0')}")
    print(f"  compare('2.0.0', '1.0.0'): {compare('2.0.0', '1.0.0')}")
    print(f"  compare('1.0.0', '1.0.0'): {compare('1.0.0', '1.0.0')}")


def example_version_bumping():
    """Version bumping examples."""
    print("\n" + "=" * 50)
    print("Version Bumping")
    print("=" * 50)
    
    v = parse("1.2.3")
    
    print(f"\nOriginal version: {v}")
    print(f"  Bump major: {v.bump_major()}")
    print(f"  Bump minor: {v.bump_minor()}")
    print(f"  Bump patch: {v.bump_patch()}")
    
    # Prerelease bumping
    v_pre = parse("1.0.0-alpha.1")
    print(f"\nPrerelease version: {v_pre}")
    print(f"  Bump prerelease: {v_pre.bump_prerelease('alpha')}")
    print(f"  Release (remove prerelease): {v_pre.release()}")


def example_sorting_versions():
    """Sorting version collections."""
    print("\n" + "=" * 50)
    print("Sorting Versions")
    print("=" * 50)
    
    versions = [
        "2.1.0",
        "1.0.0",
        "1.5.0",
        "3.0.0-alpha",
        "0.5.0",
        "2.0.0",
        "1.0.0-beta"
    ]
    
    print(f"\nUnsorted: {versions}")
    
    sorted_v = sort_versions(versions)
    print(f"Sorted: {[str(v) for v in sorted_v]}")
    
    sorted_desc = sort_versions(versions, reverse=True)
    print(f"Descending: {[str(v) for v in sorted_desc]}")
    
    print(f"\nMin version: {min_version(*versions)}")
    print(f"Max version: {max_version(*versions)}")


def example_version_ranges():
    """Version range matching examples."""
    print("\n" + "=" * 50)
    print("Version Range Matching")
    print("=" * 50)
    
    # Caret range
    print("\nCaret range (^1.2.3):")
    vr = VersionRange("^1.2.3")
    test_versions = ["1.2.2", "1.2.3", "1.2.4", "1.9.9", "2.0.0"]
    for v in test_versions:
        print(f"  {v}: {vr.satisfies(v)}")
    
    # Tilde range
    print("\nTilde range (~1.2.3):")
    vr = VersionRange("~1.2.3")
    test_versions = ["1.2.2", "1.2.3", "1.2.4", "1.3.0", "2.0.0"]
    for v in test_versions:
        print(f"  {v}: {vr.satisfies(v)}")
    
    # Comparison operators
    print("\nGreater than or equal (>=1.0.0):")
    vr = VersionRange(">=1.0.0")
    test_versions = ["0.9.9", "1.0.0", "1.0.1", "2.0.0"]
    for v in test_versions:
        print(f"  {v}: {vr.satisfies(v)}")
    
    # Combined range
    print("\nCombined range (>=1.0.0 <2.0.0):")
    vr = VersionRange(">=1.0.0 <2.0.0")
    test_versions = ["0.9.9", "1.0.0", "1.5.0", "1.9.9", "2.0.0"]
    for v in test_versions:
        print(f"  {v}: {vr.satisfies(v)}")
    
    # OR condition
    print("\nOR condition (1.0.0 || 2.0.0):")
    vr = VersionRange("1.0.0 || 2.0.0")
    test_versions = ["0.9.0", "1.0.0", "1.5.0", "2.0.0", "3.0.0"]
    for v in test_versions:
        print(f"  {v}: {vr.satisfies(v)}")


def example_version_set():
    """VersionSet collection examples."""
    print("\n" + "=" * 50)
    print("VersionSet Collection")
    print("=" * 50)
    
    # Create a version set
    versions = [
        "1.0.0", "1.1.0", "1.2.0",
        "2.0.0-alpha", "2.0.0", "2.0.1",
        "3.0.0"
    ]
    vs = VersionSet(versions)
    
    print(f"\nVersion set contains {len(vs)} versions")
    
    # Check membership
    print(f"\nMembership tests:")
    print(f"  1.1.0 in set: {'1.1.0' in vs}")
    print(f"  1.5.0 in set: {'1.5.0' in vs}")
    
    # Get sorted list
    print(f"\nSorted versions: {vs.to_list()}")
    
    # Get latest and earliest
    print(f"Latest version: {vs.latest()}")
    print(f"Earliest version: {vs.earliest()}")
    
    # Filter by range
    filtered = vs.filter("^1.0.0")
    print(f"\nFiltered by ^1.0.0: {filtered.to_list()}")
    
    filtered = vs.filter(">=2.0.0")
    print(f"Filtered by >=2.0.0: {filtered.to_list()}")


def example_dependency_checking():
    """Practical dependency version checking."""
    print("\n" + "=" * 50)
    print("Dependency Version Checking")
    print("=" * 50)
    
    # Check if update is compatible
    current = "1.2.3"
    new = "1.3.0"
    print(f"\nUpdating from {current} to {new}:")
    print(f"  Is compatible: {is_compatible(current, new)}")
    print(f"  Change type: {diff(current, new)}")
    
    # Breaking change detection
    current = "1.2.3"
    new = "2.0.0"
    print(f"\nUpdating from {current} to {new}:")
    print(f"  Is compatible: {is_compatible(current, new)}")
    print(f"  Change type: {diff(current, new)}")
    
    # Check against version constraint
    package_version = "1.5.2"
    constraint = "^1.2.0"
    print(f"\nPackage version {package_version} satisfies {constraint}: {satisfies(package_version, constraint)}")


def example_coercion():
    """Version coercion for loose inputs."""
    print("\n" + "=" * 50)
    print("Version Coercion")
    print("=" * 50)
    
    # Various loose formats
    inputs = ["v1.2.3", "v1", "1.2", "invalid"]
    
    for inp in inputs:
        result = coerce(inp)
        if result:
            print(f"  '{inp}' -> {result}")
        else:
            print(f"  '{inp}' -> (could not coerce)")


def example_changelog_generation():
    """Generate changelog entries by version diff."""
    print("\n" + "=" * 50)
    print("Changelog Generation Helper")
    print("=" * 50)
    
    changes = [
        ("1.0.0", "1.0.1", "Fixed critical bug in parser"),
        ("1.0.1", "1.1.0", "Added new API endpoints"),
        ("1.1.0", "2.0.0", "Breaking: Redesigned API"),
        ("2.0.0", "2.0.1-alpha.1", "Beta release with fixes"),
        ("2.0.1-alpha.1", "2.0.1", "Stable release"),
    ]
    
    print("\n")
    for old, new, desc in changes:
        change_type = diff(old, new)
        emoji = {
            "major": "💥",
            "minor": "✨",
            "patch": "🐛",
            "prerelease": "🚧",
            "none": "➡️"
        }.get(change_type, "•")
        print(f"{emoji} [{old} -> {new}] ({change_type}): {desc}")


def example_release_planning():
    """Plan next release version."""
    print("\n" + "=" * 50)
    print("Release Planning")
    print("=" * 50)
    
    current = parse("1.2.3")
    
    print(f"\nCurrent version: {current}")
    print("\nNext version options:")
    print(f"  Patch release (bugfix):  {next_version(current, 'patch')}")
    print(f"  Minor release (feature): {next_version(current, 'minor')}")
    print(f"  Major release (breaking): {next_version(current, 'major')}")
    print(f"  Pre-release (alpha):      {next_version(current, 'prerelease')}")


def run_all_examples():
    """Run all examples."""
    example_basic_parsing()
    example_version_comparison()
    example_version_bumping()
    example_sorting_versions()
    example_version_ranges()
    example_version_set()
    example_dependency_checking()
    example_coercion()
    example_changelog_generation()
    example_release_planning()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_examples()