#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Changelog Utilities Test Suite
============================================
Comprehensive test suite for the changelog_utils module.

Run: python changelog_utils_test.py
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Data classes
    Version, ChangeEntry, ChangeType, Release, Changelog, ReleaseType,
    
    # Parser functions
    parse_version, parse_date, parse_changelog, parse_changelog_file,
    
    # Generation functions
    create_release, create_changelog, generate_changelog_from_commits,
    
    # Comparison functions
    compare_versions, get_version_diff, get_release_notes,
    
    # Validation functions
    is_valid_version, validate_changelog,
    
    # Utility functions
    bump_version, suggest_next_version, merge_changelogs,
    quick_changelog, extract_version_links,
)


# ============================================================================
# Test Results Tracking
# ============================================================================

class TestOutcomes:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, name: str):
        self.passed += 1
        self.tests.append((name, True))
        print(f"✅ PASS: {name}")
    
    def add_fail(self, name: str, reason: str = ""):
        self.failed += 1
        self.tests.append((name, False))
        print(f"❌ FAIL: {name}")
        if reason:
            print(f"   Reason: {reason}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        return self.failed == 0


results = TestOutcomes()


# ============================================================================
# Test Data
# ============================================================================

SAMPLE_CHANGELOG = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2024-03-15

### Added
- New feature for automatic version bumping
- Support for prerelease versions

### Changed
- Improved parsing performance
- Updated documentation

### Fixed
- Bug in version comparison with prerelease tags

### Security
- Fixed potential XSS vulnerability in description rendering

## [2.0.0] - 2024-02-01

### Added
- **BREAKING** Complete rewrite of the parsing engine
- Support for multiple output formats (Markdown, JSON, plain text)

### Removed
- **BREAKING** Legacy API endpoints have been removed

### Fixed
- Various minor bugs

## [1.5.0] - 2024-01-15

### Added
- New utility functions for version comparison
- Better error handling

### Deprecated
- Old parse() method (use parse_changelog() instead)

## [1.0.0] - 2024-01-01

### Added
- Initial release with core functionality

[2.1.0]: https://github.com/example/repo/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/example/repo/compare/v1.5.0...v2.0.0
[1.5.0]: https://github.com/example/repo/compare/v1.0.0...v1.5.0
[1.0.0]: https://github.com/example/repo/releases/tag/v1.0.0
"""


# ============================================================================
# Version Tests
# ============================================================================

def test_version_parsing():
    """Test version string parsing."""
    # Basic versions
    v = parse_version("1.2.3")
    assert v.major == 1 and v.minor == 2 and v.patch == 3, "Basic version parse failed"
    results.add_pass("Version parsing: basic (1.2.3)")
    
    # With v prefix
    v = parse_version("v2.0.0")
    assert v.major == 2, "Version with 'v' prefix failed"
    results.add_pass("Version parsing: with 'v' prefix")
    
    # With prerelease
    v = parse_version("1.0.0-alpha")
    assert v.prerelease == "alpha", "Prerelease version failed"
    results.add_pass("Version parsing: with prerelease")
    
    # With build metadata
    v = parse_version("1.0.0+build.123")
    assert v.build == "build.123", "Build metadata failed"
    results.add_pass("Version parsing: with build metadata")
    
    # Complete version
    v = parse_version("2.1.3-beta.1+exp.sha.5114f85")
    assert v.major == 2 and v.minor == 1 and v.patch == 3
    assert v.prerelease == "beta.1"
    assert v.build == "exp.sha.5114f85"
    results.add_pass("Version parsing: complete semver")


def test_version_comparison():
    """Test version comparison operations."""
    v1 = parse_version("1.0.0")
    v2 = parse_version("2.0.0")
    v3 = parse_version("1.0.0")
    
    assert v1 < v2, "v1 < v2 failed"
    results.add_pass("Version comparison: less than")
    
    assert v2 > v1, "v2 > v1 failed"
    results.add_pass("Version comparison: greater than")
    
    assert v1 == v3, "v1 == v3 failed"
    results.add_pass("Version comparison: equality")
    
    assert v1 <= v3, "v1 <= v3 failed"
    results.add_pass("Version comparison: less than or equal")
    
    assert v2 >= v1, "v2 >= v1 failed"
    results.add_pass("Version comparison: greater than or equal")
    
    # Prerelease versions
    v_alpha = parse_version("1.0.0-alpha")
    v_beta = parse_version("1.0.0-beta")
    v_release = parse_version("1.0.0")
    
    assert v_alpha < v_beta, "alpha < beta failed"
    assert v_beta < v_release, "beta < release failed"
    results.add_pass("Version comparison: prerelease ordering")


def test_version_bumping():
    """Test version bumping operations."""
    v = parse_version("1.2.3")
    
    assert str(v.bump_major()) == "2.0.0", "Major bump failed"
    results.add_pass("Version bumping: major")
    
    assert str(v.bump_minor()) == "1.3.0", "Minor bump failed"
    results.add_pass("Version bumping: minor")
    
    assert str(v.bump_patch()) == "1.2.4", "Patch bump failed"
    results.add_pass("Version bumping: patch")


def test_version_string():
    """Test version string representation."""
    v = Version(1, 2, 3, "beta.1", "build.123")
    s = str(v)
    assert s == "1.2.3-beta.1+build.123", f"String repr failed: {s}"
    results.add_pass("Version string representation")


def test_version_release_type():
    """Test version release type detection."""
    assert parse_version("2.0.0").get_release_type() == ReleaseType.MAJOR
    results.add_pass("Release type: major")
    
    assert parse_version("1.1.0").get_release_type() == ReleaseType.MINOR
    results.add_pass("Release type: minor")
    
    assert parse_version("1.0.1").get_release_type() == ReleaseType.PATCH
    results.add_pass("Release type: patch")
    
    assert parse_version("1.0.0-alpha").get_release_type() == ReleaseType.PRERELEASE
    results.add_pass("Release type: prerelease")


# ============================================================================
# ChangeEntry Tests
# ============================================================================

def test_change_entry():
    """Test change entry creation and formatting."""
    entry = ChangeEntry(
        description="Added new feature",
        change_type=ChangeType.ADDED,
        scope="api",
        issue_ref="123",
        breaking=False
    )
    
    md = entry.to_markdown()
    assert "**api**:" in md, "Scope not in markdown"
    assert "Added new feature" in md, "Description not in markdown"
    assert "[#123]" in md, "Issue reference not in markdown"
    results.add_pass("Change entry: markdown generation")
    
    # Breaking change
    entry.breaking = True
    md = entry.to_markdown()
    assert "**BREAKING**" in md, "Breaking flag not in markdown"
    results.add_pass("Change entry: breaking change")


# ============================================================================
# Release Tests
# ============================================================================

def test_release_creation():
    """Test release creation."""
    release = create_release(
        version="1.0.0",
        date="2024-01-15",
        description="First stable release",
        changes={
            ChangeType.ADDED: ["Feature A", "Feature B"],
            ChangeType.FIXED: ["Bug fix 1"]
        }
    )
    
    assert str(release.version) == "1.0.0", "Version mismatch"
    assert release.date is not None, "Date not parsed"
    assert release.total_changes() == 3, "Change count mismatch"
    results.add_pass("Release creation: basic")
    
    # Test markdown output
    md = release.to_markdown()
    assert "## [1.0.0]" in md, "Version header missing"
    assert "### Added" in md, "Added section missing"
    assert "### Fixed" in md, "Fixed section missing"
    results.add_pass("Release creation: markdown output")


def test_release_yanked():
    """Test yanked release handling."""
    release = create_release(version="1.0.0", yanked=True)
    md = release.to_markdown()
    assert "[YANKED]" in md, "Yanked flag missing"
    results.add_pass("Release: yanked flag")


# ============================================================================
# Changelog Tests
# ============================================================================

def test_changelog_parsing():
    """Test parsing a complete changelog."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    
    assert changelog.title == "Changelog", f"Title mismatch: {changelog.title}"
    results.add_pass("Changelog parsing: title")
    
    assert len(changelog.releases) == 4, f"Release count mismatch: {len(changelog.releases)}"
    results.add_pass("Changelog parsing: release count")
    
    # Check latest release
    latest = changelog.latest_release()
    assert str(latest.version) == "2.1.0", f"Latest version mismatch: {latest.version}"
    results.add_pass("Changelog parsing: latest version")
    
    # Check changes parsed
    assert latest.total_changes() > 0, "No changes parsed"
    results.add_pass("Changelog parsing: changes extracted")


def test_changelog_get_release():
    """Test getting a specific release."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    
    release = changelog.get_release("2.0.0")
    assert release is not None, "Release not found"
    assert str(release.version) == "2.0.0", "Version mismatch"
    results.add_pass("Changelog: get release by string")
    
    release = changelog.get_release(Version(1, 5, 0))
    assert release is not None, "Release not found by Version object"
    results.add_pass("Changelog: get release by Version object")


def test_changelog_version_list():
    """Test getting all versions."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    versions = changelog.get_versions()
    
    assert len(versions) == 4, "Version count mismatch"
    assert str(versions[0]) == "2.1.0", "First version not latest"
    results.add_pass("Changelog: version list")


def test_changelog_output_formats():
    """Test different output formats."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    
    # Markdown
    md = changelog.to_markdown()
    assert "# Changelog" in md, "Markdown title missing"
    assert "## [2.1.0]" in md, "Release header missing"
    results.add_pass("Changelog output: markdown")
    
    # JSON
    json_dict = changelog.to_json_dict()
    assert "title" in json_dict, "JSON title missing"
    assert "releases" in json_dict, "JSON releases missing"
    results.add_pass("Changelog output: JSON")
    
    # Plain text
    text = changelog.to_plain_text()
    assert "Changelog" in text, "Plain text title missing"
    assert "Version 2.1.0" in text, "Version missing in plain text"
    results.add_pass("Changelog output: plain text")


# ============================================================================
# Comparison Functions Tests
# ============================================================================

def test_compare_versions():
    """Test version comparison function."""
    assert compare_versions("1.0.0", "2.0.0") == -1, "1.0.0 < 2.0.0 failed"
    results.add_pass("Compare versions: less than")
    
    assert compare_versions("2.0.0", "1.0.0") == 1, "2.0.0 > 1.0.0 failed"
    results.add_pass("Compare versions: greater than")
    
    assert compare_versions("1.0.0", "1.0.0") == 0, "1.0.0 == 1.0.0 failed"
    results.add_pass("Compare versions: equal")


def test_version_diff():
    """Test getting changes between versions."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    diff = get_version_diff(changelog, "1.5.0", "2.1.0")
    
    # Should include changes from 2.0.0 and 2.1.0
    total_changes = sum(len(entries) for entries in diff.values())
    assert total_changes > 0, "No diff changes found"
    results.add_pass("Version diff: changes found")


def test_release_notes():
    """Test release notes generation."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    
    notes = get_release_notes(changelog, "2.1.0")
    assert "2.1.0" in notes, "Version not in notes"
    assert "### Added" in notes, "Added section not in notes"
    results.add_pass("Release notes: markdown format")


# ============================================================================
# Validation Tests
# ============================================================================

def test_is_valid_version():
    """Test version validation."""
    assert is_valid_version("1.0.0") == True, "Valid version rejected"
    assert is_valid_version("v2.3.4") == True, "Valid version with 'v' rejected"
    assert is_valid_version("1.0.0-alpha") == True, "Valid prerelease rejected"
    assert is_valid_version("not-a-version") == False, "Invalid version accepted"
    assert is_valid_version("1") == True, "Short version rejected"
    results.add_pass("Version validation")


def test_validate_changelog():
    """Test changelog validation."""
    is_valid, errors = validate_changelog(SAMPLE_CHANGELOG)
    assert is_valid == True, f"Valid changelog rejected: {errors}"
    results.add_pass("Changelog validation: valid")
    
    is_valid, errors = validate_changelog("No title here")
    assert is_valid == False, "Invalid changelog accepted"
    results.add_pass("Changelog validation: invalid")


# ============================================================================
# Utility Functions Tests
# ============================================================================

def test_bump_version():
    """Test version bumping based on change type."""
    v = "1.0.0"
    
    # REMOVES -> major bump
    assert bump_version(v, ChangeType.REMOVED).major == 2, "Removed should bump major"
    results.add_pass("Bump version: removed -> major")
    
    # ADDED -> minor bump
    assert bump_version(v, ChangeType.ADDED).minor == 1, "Added should bump minor"
    results.add_pass("Bump version: added -> minor")
    
    # FIXED -> patch bump
    assert bump_version(v, ChangeType.FIXED).patch == 1, "Fixed should bump patch"
    results.add_pass("Bump version: fixed -> patch")


def test_suggest_next_version():
    """Test suggesting next version."""
    changelog = parse_changelog(SAMPLE_CHANGELOG)
    next_v = suggest_next_version(changelog)
    assert next_v > parse_version("2.1.0"), "Next version should be greater"
    results.add_pass("Suggest next version")


def test_merge_changelogs():
    """Test merging changelogs."""
    c1 = create_changelog(title="Project A")
    c1.add_release(create_release("1.0.0", changes={ChangeType.ADDED: ["Feature A"]}))
    
    c2 = create_changelog(title="Project B")
    c2.add_release(create_release("1.0.0", changes={ChangeType.FIXED: ["Bug fix"]}))
    c2.add_release(create_release("0.9.0", changes={ChangeType.ADDED: ["Initial"]}))
    
    merged = merge_changelogs([c1, c2])
    
    # Should have releases from both
    assert len(merged.releases) >= 2, "Merged changelog missing releases"
    
    # 1.0.0 should have both changes
    r = merged.get_release("1.0.0")
    assert r.total_changes() >= 2, "Changes not merged"
    results.add_pass("Merge changelogs")


def test_quick_changelog():
    """Test quick changelog generation."""
    md = quick_changelog({
        "1.0.0": ["Added new feature", "Fixed critical bug"],
        "0.9.0": ["Initial release"]
    })
    
    assert "# Changelog" in md, "Title missing"
    assert "## [1.0.0]" in md, "Version header missing"
    assert "Added new feature" in md, "Change missing"
    results.add_pass("Quick changelog generation")


def test_extract_version_links():
    """Test extracting version links."""
    links = extract_version_links(SAMPLE_CHANGELOG)
    
    assert "2.1.0" in links, "Link not extracted"
    assert "github.com" in links["2.1.0"], "URL not correct"
    results.add_pass("Extract version links")


# ============================================================================
# Generation Functions Tests
# ============================================================================

def test_generate_from_commits():
    """Test generating release from commits."""
    commits = [
        {"message": "feat: add new feature", "hash": "abc123"},
        {"message": "fix: resolve bug", "hash": "def456"},
        {"message": "feat(api)!: breaking change", "hash": "ghi789"},
        {"message": "docs: update readme", "hash": "jkl012"},
    ]
    
    release = generate_changelog_from_commits(commits, "1.0.0")
    
    # Only conventional commits (feat, fix, etc.) are parsed
    # docs goes to Changed by default
    assert release.total_changes() >= 3, f"Expected at least 3 changes, got {release.total_changes()}"
    
    # Check change types
    added = release.get_changes(ChangeType.ADDED)
    assert len(added) >= 1, "No added changes"
    
    fixed = release.get_changes(ChangeType.FIXED)
    assert len(fixed) >= 1, "No fixed changes"
    results.add_pass("Generate from commits")


def test_create_changelog():
    """Test creating a changelog from scratch."""
    changelog = create_changelog(
        title="My Project",
        description="A sample project changelog"
    )
    
    release1 = create_release(
        version="1.0.0",
        date="2024-01-01",
        changes={
            ChangeType.ADDED: ["Initial release"]
        }
    )
    
    release2 = create_release(
        version="1.1.0",
        date="2024-02-01",
        changes={
            ChangeType.ADDED: [
                ChangeEntry(description="New API", change_type=ChangeType.ADDED, scope="api"),
                "Feature B"
            ],
            ChangeType.FIXED: ["Bug fix"]
        }
    )
    
    changelog.add_release(release1)
    changelog.add_release(release2)
    
    # Check ordering (newest first)
    assert str(changelog.releases[0].version) == "1.1.0", "Releases not sorted"
    
    md = changelog.to_markdown()
    assert "# My Project" in md, "Title missing"
    assert "A sample project changelog" in md, "Description missing"
    assert "**api**:" in md, "Scope missing"
    results.add_pass("Create changelog from scratch")


# ============================================================================
# Date Parsing Tests
# ============================================================================

def test_date_parsing():
    """Test date parsing from various formats."""
    # ISO format
    d = parse_date("2024-01-15")
    assert d is not None and d.year == 2024, "ISO date failed"
    results.add_pass("Date parsing: ISO format")
    
    # US format
    d = parse_date("01/15/2024")
    assert d is not None, "US date failed"
    results.add_pass("Date parsing: US format")
    
    # Written format
    d = parse_date("January 15, 2024")
    assert d is not None, "Written date failed"
    results.add_pass("Date parsing: written format")


# ============================================================================
# Edge Cases Tests
# ============================================================================

def test_empty_changelog():
    """Test handling empty changelog."""
    changelog = parse_changelog("")
    assert len(changelog.releases) == 0, "Empty changelog should have no releases"
    results.add_pass("Empty changelog handling")


def test_malformed_version():
    """Test handling malformed version strings."""
    v = parse_version("1")  # Only major
    assert v.major == 1 and v.minor == 0 and v.patch == 0, "Partial version failed"
    results.add_pass("Partial version parsing")


def test_unicode_in_changelog():
    """Test handling Unicode in changelog."""
    md = """# 变更日志

## [1.0.0] - 2024-01-01

### Added
- 添加了新功能
- 新增 API 接口

### Fixed
- 修复了中文乱码问题
"""
    changelog = parse_changelog(md)
    assert len(changelog.releases) == 1, "Unicode changelog failed"
    results.add_pass("Unicode in changelog")


# ============================================================================
# Run All Tests
# ============================================================================

def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Changelog Utilities Test Suite")
    print("=" * 60)
    print()
    
    # Version tests
    print("--- Version Tests ---")
    test_version_parsing()
    test_version_comparison()
    test_version_bumping()
    test_version_string()
    test_version_release_type()
    print()
    
    # ChangeEntry tests
    print("--- ChangeEntry Tests ---")
    test_change_entry()
    print()
    
    # Release tests
    print("--- Release Tests ---")
    test_release_creation()
    test_release_yanked()
    print()
    
    # Changelog tests
    print("--- Changelog Tests ---")
    test_changelog_parsing()
    test_changelog_get_release()
    test_changelog_version_list()
    test_changelog_output_formats()
    print()
    
    # Comparison tests
    print("--- Comparison Tests ---")
    test_compare_versions()
    test_version_diff()
    test_release_notes()
    print()
    
    # Validation tests
    print("--- Validation Tests ---")
    test_is_valid_version()
    test_validate_changelog()
    print()
    
    # Utility tests
    print("--- Utility Tests ---")
    test_bump_version()
    test_suggest_next_version()
    test_merge_changelogs()
    test_quick_changelog()
    test_extract_version_links()
    print()
    
    # Generation tests
    print("--- Generation Tests ---")
    test_generate_from_commits()
    test_create_changelog()
    print()
    
    # Date tests
    print("--- Date Parsing Tests ---")
    test_date_parsing()
    print()
    
    # Edge cases
    print("--- Edge Cases Tests ---")
    test_empty_changelog()
    test_malformed_version()
    test_unicode_in_changelog()
    print()
    
    # Print summary
    return results.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)