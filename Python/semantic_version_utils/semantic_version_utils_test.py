"""
Tests for Semantic Version Utilities

Comprehensive test suite covering all functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SemanticVersion,
    VersionRange,
    VersionSet,
    parse,
    try_parse,
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
    SEMVER_PATTERN,
)


def test_parse():
    """Test version parsing."""
    print("Testing parse()...")
    
    # Basic versions
    v = parse("1.0.0")
    assert v.major == 1
    assert v.minor == 0
    assert v.patch == 0
    assert v.prerelease is None
    assert v.build is None
    
    # With prerelease
    v = parse("1.0.0-alpha")
    assert v.prerelease == "alpha"
    
    # With prerelease and build
    v = parse("1.0.0-alpha.1+build.123")
    assert v.prerelease == "alpha.1"
    assert v.build == "build.123"
    
    # Complex prerelease
    v = parse("2.3.4-beta.2.1")
    assert v.prerelease == "beta.2.1"
    
    # Complex build metadata
    v = parse("1.0.0+20130313144700")
    assert v.build == "20130313144700"
    
    # Invalid versions
    try:
        parse("1.0")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        parse("invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("  ✓ parse() tests passed")


def test_try_parse():
    """Test try_parse function."""
    print("Testing try_parse()...")
    
    assert try_parse("1.0.0") is not None
    assert try_parse("invalid") is None
    assert try_parse("1.0") is None
    
    print("  ✓ try_parse() tests passed")


def test_is_valid():
    """Test version validation."""
    print("Testing is_valid()...")
    
    assert is_valid("1.0.0") is True
    assert is_valid("0.0.1") is True
    assert is_valid("1.2.3-alpha.1+build.123") is True
    assert is_valid("v1.0.0") is False  # 'v' prefix not allowed
    assert is_valid("1.0") is False
    assert is_valid("1") is False
    assert is_valid("") is False
    
    print("  ✓ is_valid() tests passed")


def test_version_comparison():
    """Test version comparison operations."""
    print("Testing version comparison...")
    
    v1 = parse("1.0.0")
    v2 = parse("2.0.0")
    v3 = parse("1.0.0")
    v4 = parse("1.1.0")
    v5 = parse("1.0.1")
    
    # Less than
    assert v1 < v2
    assert v1 < v4
    assert v1 < v5
    assert v4 < v2
    
    # Greater than
    assert v2 > v1
    assert v4 > v1
    assert v5 > v1
    
    # Equal
    assert v1 == v3
    assert v1 != v2
    
    # Less than or equal
    assert v1 <= v3
    assert v1 <= v2
    
    # Greater than or equal
    assert v2 >= v1
    assert v1 >= v3
    
    print("  ✓ Version comparison tests passed")


def test_prerelease_comparison():
    """Test prerelease version comparison."""
    print("Testing prerelease comparison...")
    
    # Prerelease < release
    v_pre = parse("1.0.0-alpha")
    v_release = parse("1.0.0")
    assert v_pre < v_release
    
    # Compare prerelease identifiers
    v1 = parse("1.0.0-alpha.1")
    v2 = parse("1.0.0-alpha.2")
    assert v1 < v2
    
    # Numeric < alphanumeric
    v1 = parse("1.0.0-alpha.1")
    v2 = parse("1.0.0-alpha.beta")
    assert v1 < v2
    
    # Alpha < beta
    v1 = parse("1.0.0-alpha")
    v2 = parse("1.0.0-beta")
    assert v1 < v2
    
    print("  ✓ Prerelease comparison tests passed")


def test_build_metadata():
    """Test build metadata handling."""
    print("Testing build metadata...")
    
    # Build metadata doesn't affect equality
    v1 = parse("1.0.0+build.1")
    v2 = parse("1.0.0+build.2")
    assert v1 == v2
    
    # Build metadata doesn't affect comparison
    v1 = parse("1.0.0-alpha+build.1")
    v2 = parse("1.0.0-alpha+build.2")
    assert v1 == v2
    
    print("  ✓ Build metadata tests passed")


def test_bump_operations():
    """Test version bump operations."""
    print("Testing bump operations...")
    
    v = parse("1.2.3")
    
    # Bump major
    assert str(v.bump_major()) == "2.0.0"
    
    # Bump minor
    assert str(v.bump_minor()) == "1.3.0"
    
    # Bump patch
    assert str(v.bump_patch()) == "1.2.4"
    
    # Bump prerelease
    v_pre = parse("1.0.0-alpha.1")
    assert str(v_pre.bump_prerelease("alpha")) == "1.0.0-alpha.2"
    
    # New prerelease
    assert str(v.bump_prerelease("beta")) == "1.2.3-beta.1"
    
    # Release (remove prerelease)
    v_with_pre = parse("1.0.0-alpha.1")
    assert str(v_with_pre.release()) == "1.0.0"
    
    print("  ✓ Bump operation tests passed")


def test_version_properties():
    """Test version properties."""
    print("Testing version properties...")
    
    v_release = parse("1.0.0")
    assert v_release.is_release is True
    assert v_release.is_prerelease is False
    
    v_pre = parse("1.0.0-alpha")
    assert v_pre.is_release is False
    assert v_pre.is_prerelease is True
    
    # to_tuple
    v = parse("1.2.3")
    assert v.to_tuple() == (1, 2, 3)
    
    # to_dict
    d = v.to_dict()
    assert d["major"] == 1
    assert d["minor"] == 2
    assert d["patch"] == 3
    assert d["version"] == "1.2.3"
    
    print("  ✓ Version property tests passed")


def test_compare_function():
    """Test compare function."""
    print("Testing compare()...")
    
    assert compare("1.0.0", "2.0.0") == -1
    assert compare("2.0.0", "1.0.0") == 1
    assert compare("1.0.0", "1.0.0") == 0
    assert compare("1.0.0-alpha", "1.0.0") == -1
    
    # With SemanticVersion objects
    v1 = parse("1.0.0")
    v2 = parse("2.0.0")
    assert compare(v1, v2) == -1
    
    print("  ✓ compare() tests passed")


def test_sort_versions():
    """Test version sorting."""
    print("Testing sort_versions()...")
    
    versions = ["2.0.0", "1.0.0", "1.5.0", "0.5.0"]
    sorted_v = sort_versions(versions)
    
    assert str(sorted_v[0]) == "0.5.0"
    assert str(sorted_v[1]) == "1.0.0"
    assert str(sorted_v[2]) == "1.5.0"
    assert str(sorted_v[3]) == "2.0.0"
    
    # Reverse sort
    sorted_v = sort_versions(versions, reverse=True)
    assert str(sorted_v[0]) == "2.0.0"
    
    print("  ✓ sort_versions() tests passed")


def test_min_max():
    """Test min/max version functions."""
    print("Testing min_version() and max_version()...")
    
    assert str(min_version("1.0.0", "2.0.0", "0.5.0")) == "0.5.0"
    assert str(max_version("1.0.0", "2.0.0", "0.5.0")) == "2.0.0"
    
    print("  ✓ min_version()/max_version() tests passed")


def test_version_range_basic():
    """Test basic version range operations."""
    print("Testing basic VersionRange...")
    
    # Exact version
    vr = VersionRange("1.0.0")
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.0.1") is False
    
    # Greater than
    vr = VersionRange(">1.0.0")
    assert vr.satisfies("1.0.0") is False
    assert vr.satisfies("1.0.1") is True
    assert vr.satisfies("2.0.0") is True
    
    # Greater than or equal
    vr = VersionRange(">=1.0.0")
    assert vr.satisfies("0.9.0") is False
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.0.1") is True
    
    # Less than
    vr = VersionRange("<2.0.0")
    assert vr.satisfies("1.9.9") is True
    assert vr.satisfies("2.0.0") is False
    
    # Less than or equal
    vr = VersionRange("<=2.0.0")
    assert vr.satisfies("2.0.0") is True
    assert vr.satisfies("2.0.1") is False
    
    print("  ✓ Basic VersionRange tests passed")


def test_version_range_caret():
    """Test caret range (^)."""
    print("Testing caret range (^)...")
    
    # ^1.2.3 -> >=1.2.3 <2.0.0
    vr = VersionRange("^1.2.3")
    assert vr.satisfies("1.2.2") is False
    assert vr.satisfies("1.2.3") is True
    assert vr.satisfies("1.2.4") is True
    assert vr.satisfies("1.9.9") is True
    assert vr.satisfies("2.0.0") is False
    
    # ^0.2.3 -> >=0.2.3 <0.3.0 (special case for 0.x)
    vr = VersionRange("^0.2.3")
    assert vr.satisfies("0.2.3") is True
    assert vr.satisfies("0.2.4") is True
    assert vr.satisfies("0.3.0") is False
    
    # ^0.0.3 -> >=0.0.3 <0.0.4 (special case for 0.0.x)
    vr = VersionRange("^0.0.3")
    assert vr.satisfies("0.0.3") is True
    assert vr.satisfies("0.0.4") is False
    
    # ^1.2 -> >=1.2.0 <2.0.0
    vr = VersionRange("^1.2")
    assert vr.satisfies("1.2.0") is True
    assert vr.satisfies("1.3.0") is True
    assert vr.satisfies("2.0.0") is False
    
    # ^1 -> >=1.0.0 <2.0.0
    vr = VersionRange("^1")
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.9.9") is True
    assert vr.satisfies("2.0.0") is False
    
    print("  ✓ Caret range tests passed")


def test_version_range_tilde():
    """Test tilde range (~)."""
    print("Testing tilde range (~)...")
    
    # ~1.2.3 -> >=1.2.3 <1.3.0
    vr = VersionRange("~1.2.3")
    assert vr.satisfies("1.2.2") is False
    assert vr.satisfies("1.2.3") is True
    assert vr.satisfies("1.2.4") is True
    assert vr.satisfies("1.3.0") is False
    
    # ~1.2 -> >=1.2.0 <1.3.0
    vr = VersionRange("~1.2")
    assert vr.satisfies("1.2.0") is True
    assert vr.satisfies("1.2.9") is True
    assert vr.satisfies("1.3.0") is False
    
    # ~1 -> >=1.0.0 <2.0.0
    vr = VersionRange("~1")
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.9.9") is True
    assert vr.satisfies("2.0.0") is False
    
    print("  ✓ Tilde range tests passed")


def test_version_range_x():
    """Test X-range (1.x, 1.2.x)."""
    print("Testing X-range...")
    
    # 1.2.x -> >=1.2.0 <1.3.0
    vr = VersionRange("1.2.x")
    assert vr.satisfies("1.2.0") is True
    assert vr.satisfies("1.2.9") is True
    assert vr.satisfies("1.3.0") is False
    
    # 1.x -> >=1.0.0 <2.0.0
    vr = VersionRange("1.x")
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.9.9") is True
    assert vr.satisfies("2.0.0") is False
    
    # 1.X and 1.* should work too
    vr = VersionRange("1.X")
    assert vr.satisfies("1.5.0") is True
    
    vr = VersionRange("1.*")
    assert vr.satisfies("1.5.0") is True
    
    print("  ✓ X-range tests passed")


def test_version_range_combined():
    """Test combined ranges."""
    print("Testing combined ranges...")
    
    # >=1.0.0 <2.0.0
    vr = VersionRange(">=1.0.0 <2.0.0")
    assert vr.satisfies("0.9.9") is False
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.9.9") is True
    assert vr.satisfies("2.0.0") is False
    
    # OR condition
    vr = VersionRange("1.0.0 || 2.0.0")
    assert vr.satisfies("1.0.0") is True
    assert vr.satisfies("1.5.0") is False
    assert vr.satisfies("2.0.0") is True
    
    print("  ✓ Combined range tests passed")


def test_satisfies():
    """Test satisfies function."""
    print("Testing satisfies()...")
    
    assert satisfies("1.2.5", "^1.2.3") is True
    assert satisfies("2.0.0", "^1.2.3") is False
    assert satisfies("1.2.3", "~1.2.0") is True
    assert satisfies("1.3.0", "~1.2.0") is False
    
    print("  ✓ satisfies() tests passed")


def test_coerce():
    """Test version coercion."""
    print("Testing coerce()...")
    
    # v prefix
    v = coerce("v1.2.3")
    assert v is not None
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    
    # Single number
    v = coerce("1")
    assert v is not None
    assert v.major == 1
    assert v.minor == 0
    assert v.patch == 0
    
    # Two numbers
    v = coerce("1.2")
    assert v is not None
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 0
    
    # Invalid
    assert coerce("invalid") is None
    
    print("  ✓ coerce() tests passed")


def test_diff():
    """Test version difference detection."""
    print("Testing diff()...")
    
    assert diff("1.0.0", "2.0.0") == "major"
    assert diff("1.0.0", "1.1.0") == "minor"
    assert diff("1.0.0", "1.0.1") == "patch"
    assert diff("1.0.0-alpha", "1.0.0-beta") == "prerelease"
    assert diff("1.0.0", "1.0.0") == "none"
    
    print("  ✓ diff() tests passed")


def test_is_compatible():
    """Test version compatibility check."""
    print("Testing is_compatible()...")
    
    # Same major
    assert is_compatible("1.0.0", "1.1.0") is True
    assert is_compatible("1.0.0", "1.0.1") is True
    
    # Different major
    assert is_compatible("1.0.0", "2.0.0") is False
    
    # Strict mode (same minor)
    assert is_compatible("1.2.0", "1.3.0", strict=True) is False
    assert is_compatible("1.2.0", "1.2.1", strict=True) is True
    
    print("  ✓ is_compatible() tests passed")


def test_next_version():
    """Test next_version function."""
    print("Testing next_version()...")
    
    v = parse("1.2.3")
    
    assert str(next_version(v, "major")) == "2.0.0"
    assert str(next_version(v, "minor")) == "1.3.0"
    assert str(next_version(v, "patch")) == "1.2.4"
    
    # With string input
    assert str(next_version("1.2.3", "major")) == "2.0.0"
    
    # Invalid release type
    try:
        next_version("1.0.0", "invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("  ✓ next_version() tests passed")


def test_version_set():
    """Test VersionSet class."""
    print("Testing VersionSet...")
    
    vs = VersionSet(["1.0.0", "2.0.0", "1.5.0"])
    
    # Membership
    assert "1.0.0" in vs
    assert "1.5.0" in vs
    assert "3.0.0" not in vs
    
    # Size
    assert len(vs) == 3
    
    # Sorted
    sorted_v = vs.sorted()
    assert str(sorted_v[0]) == "1.0.0"
    assert str(sorted_v[1]) == "1.5.0"
    assert str(sorted_v[2]) == "2.0.0"
    
    # Latest and earliest
    assert str(vs.latest()) == "2.0.0"
    assert str(vs.earliest()) == "1.0.0"
    
    # Filter
    filtered = vs.filter("^1.0.0")
    assert len(filtered) == 2
    assert "2.0.0" not in filtered
    
    # Add and remove
    vs.add("3.0.0")
    assert "3.0.0" in vs
    vs.remove("3.0.0")
    assert "3.0.0" not in vs
    
    # To list
    assert vs.to_list() == ["1.0.0", "1.5.0", "2.0.0"]
    
    print("  ✓ VersionSet tests passed")


def test_string_representation():
    """Test string representation."""
    print("Testing string representation...")
    
    v = parse("1.2.3")
    assert str(v) == "1.2.3"
    assert repr(v) == "SemanticVersion(1.2.3)"
    
    v = parse("1.0.0-alpha.1+build.123")
    assert str(v) == "1.0.0-alpha.1+build.123"
    
    vr = VersionRange("^1.0.0")
    assert str(vr) == "^1.0.0"
    assert repr(vr) == "VersionRange('^1.0.0')"
    
    print("  ✓ String representation tests passed")


def test_hash_and_equality():
    """Test hash and equality for use in collections."""
    print("Testing hash and equality...")
    
    v1 = parse("1.0.0")
    v2 = parse("1.0.0")
    v3 = parse("1.0.0+build.1")
    v4 = parse("1.0.0+build.2")
    
    # Equality
    assert v1 == v2
    assert v3 == v4  # Build metadata ignored
    assert v1 == v3  # Build metadata ignored
    
    # Hash (for use in sets/dicts)
    assert hash(v1) == hash(v2)
    assert hash(v3) == hash(v4)
    
    # Use in set
    version_set = {v1, v2, v3}
    assert len(version_set) == 1
    
    # Use in dict
    version_dict = {v1: "value"}
    assert version_dict[v2] == "value"
    
    print("  ✓ Hash and equality tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Semantic Version Utilities Test Suite")
    print("=" * 50 + "\n")
    
    test_parse()
    test_try_parse()
    test_is_valid()
    test_version_comparison()
    test_prerelease_comparison()
    test_build_metadata()
    test_bump_operations()
    test_version_properties()
    test_compare_function()
    test_sort_versions()
    test_min_max()
    test_version_range_basic()
    test_version_range_caret()
    test_version_range_tilde()
    test_version_range_x()
    test_version_range_combined()
    test_satisfies()
    test_coerce()
    test_diff()
    test_is_compatible()
    test_next_version()
    test_version_set()
    test_string_representation()
    test_hash_and_equality()
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()