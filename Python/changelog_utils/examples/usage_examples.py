#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Changelog Utilities Examples
==========================================
Practical examples demonstrating changelog_utils module usage.

Run: python usage_examples.py
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Version, ChangeEntry, ChangeType, Release, Changelog,
    parse_version, parse_changelog, parse_changelog_file,
    create_release, create_changelog, generate_changelog_from_commits,
    compare_versions, get_version_diff, get_release_notes,
    is_valid_version, validate_changelog,
    bump_version, suggest_next_version, merge_changelogs,
    quick_changelog, extract_version_links,
)


# ============================================================================
# Example 1: Parsing an Existing Changelog
# ============================================================================

def example_parse_changelog():
    """Parse an existing CHANGELOG.md file."""
    print("=" * 60)
    print("Example 1: Parsing an Existing Changelog")
    print("=" * 60)
    
    sample_changelog = """# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2024-03-15

### Added
- **BREAKING** New major API redesign
- Support for JSON output format
- Automatic version bumping suggestions

### Changed
- Improved parsing performance by 50%
- Updated documentation

### Fixed
- Bug in version comparison with prerelease tags

### Security
- Fixed potential vulnerability in date parsing

## [1.5.0] - 2024-02-01

### Added
- New utility functions for version comparison
- Better error handling

### Deprecated
- Old parse() method (use parse_changelog() instead)

## [1.0.0] - 2024-01-01

### Added
- Initial release with core functionality
"""
    
    # Parse the changelog
    changelog = parse_changelog(sample_changelog)
    
    print(f"\nTitle: {changelog.title}")
    print(f"Number of releases: {len(changelog.releases)}")
    
    # Get the latest release
    latest = changelog.latest_release()
    print(f"\nLatest version: {latest.version}")
    print(f"Release date: {latest.date.strftime('%Y-%m-%d') if latest.date else 'N/A'}")
    print(f"Total changes: {latest.total_changes()}")
    
    # List all changes in the latest release
    print("\nChanges in latest release:")
    for change_type, entries in latest.changes.items():
        if entries:
            print(f"  {change_type.value}:")
            for entry in entries:
                print(f"    - {entry.description}")
    
    # Get a specific release
    release_150 = changelog.get_release("1.5.0")
    if release_150:
        print(f"\nVersion 1.5.0 had {release_150.total_changes()} changes")


# ============================================================================
# Example 2: Creating a Changelog from Scratch
# ============================================================================

def example_create_changelog():
    """Create a new changelog programmatically."""
    print("\n" + "=" * 60)
    print("Example 2: Creating a Changelog from Scratch")
    print("=" * 60)
    
    # Create a new changelog
    changelog = create_changelog(
        title="My Awesome Project",
        description="All notable changes to this project will be documented here."
    )
    
    # Create the first release
    v1_0 = create_release(
        version="1.0.0",
        date="2024-01-01",
        description="First stable release!",
        changes={
            ChangeType.ADDED: [
                "Core functionality implemented",
                "Basic API endpoints",
                "Documentation and examples"
            ],
            ChangeType.FIXED: [
                "Initial bug fixes"
            ]
        }
    )
    changelog.add_release(v1_0)
    
    # Create a minor release
    v1_1 = create_release(
        version="1.1.0",
        date="2024-02-15",
        changes={
            ChangeType.ADDED: [
                ChangeEntry(
                    description="New search functionality",
                    change_type=ChangeType.ADDED,
                    scope="api"
                ),
                ChangeEntry(
                    description="Export to CSV",
                    change_type=ChangeType.ADDED,
                    scope="ui"
                )
            ],
            ChangeType.CHANGED: [
                "Improved performance"
            ],
            ChangeType.DEPRECATED: [
                "Old API endpoint will be removed in v2.0"
            ]
        }
    )
    changelog.add_release(v1_1)
    
    # Create a patch release
    v1_1_1 = create_release(
        version="1.1.1",
        date="2024-02-20",
        changes={
            ChangeType.FIXED: [
                ChangeEntry(
                    description="Critical bug in search (#42)",
                    change_type=ChangeType.FIXED,
                    issue_ref="42"
                )
            ],
            ChangeType.SECURITY: [
                "Fixed XSS vulnerability in user input"
            ]
        }
    )
    changelog.add_release(v1_1_1)
    
    # Output as Markdown
    print("\nGenerated Markdown:")
    print("-" * 60)
    print(changelog.to_markdown())
    
    # Output as JSON
    print("\nAs JSON (first release):")
    print("-" * 60)
    import json
    print(json.dumps(changelog.to_json_dict()["releases"][2], indent=2))


# ============================================================================
# Example 3: Version Operations
# ============================================================================

def example_version_operations():
    """Demonstrate version parsing and comparison."""
    print("\n" + "=" * 60)
    print("Example 3: Version Operations")
    print("=" * 60)
    
    # Parse various version formats
    versions = [
        "1.0.0",
        "v2.3.4",
        "1.0.0-alpha",
        "1.0.0-beta.2",
        "1.0.0-rc.1",
        "2.0.0+build.123",
        "1.2.3-beta.1+exp.sha.5114f85"
    ]
    
    print("\nParsing versions:")
    for v_str in versions:
        v = parse_version(v_str)
        print(f"  {v_str:30} -> major={v.major}, minor={v.minor}, patch={v.patch}", end="")
        if v.prerelease:
            print(f", prerelease={v.prerelease}", end="")
        if v.build:
            print(f", build={v.build}", end="")
        print()
    
    # Version comparison
    print("\nVersion comparisons:")
    v1 = parse_version("1.0.0")
    v2 = parse_version("2.0.0")
    v3 = parse_version("1.0.0")
    
    print(f"  {v1} < {v2}: {v1 < v2}")
    print(f"  {v1} == {v3}: {v1 == v3}")
    print(f"  {v1} >= {v3}: {v1 >= v3}")
    
    # Prerelease ordering
    print("\nPrerelease ordering:")
    versions = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-beta", "1.0.0-rc.1", "1.0.0"]
    sorted_versions = sorted([parse_version(v) for v in versions])
    print(f"  Sorted: {' < '.join(str(v) for v in sorted_versions)}")
    
    # Version bumping
    print("\nVersion bumping:")
    v = parse_version("1.2.3")
    print(f"  Original: {v}")
    print(f"  Bump major: {v.bump_major()}")
    print(f"  Bump minor: {v.bump_minor()}")
    print(f"  Bump patch: {v.bump_patch()}")


# ============================================================================
# Example 4: Generating from Commits
# ============================================================================

def example_generate_from_commits():
    """Generate a release from commit messages."""
    print("\n" + "=" * 60)
    print("Example 4: Generating Release from Commits")
    print("=" * 60)
    
    # Simulate commit history (conventional commits format)
    commits = [
        {"message": "feat: add new search API", "hash": "a1b2c3d"},
        {"message": "feat(ui): add dark mode support", "hash": "e4f5g6h"},
        {"message": "feat(api)!: breaking change to authentication", "hash": "i7j8k9l"},
        {"message": "fix: resolve memory leak in parser", "hash": "m0n1o2p"},
        {"message": "fix(ui): correct button alignment", "hash": "q3r4s5t"},
        {"message": "docs: update API documentation", "hash": "u6v7w8x"},
        {"message": "perf: optimize database queries", "hash": "y9z0a1b"},
        {"message": "security: fix potential SQL injection", "hash": "c2d3e4f"},
        {"message": "deprecate: old API endpoint", "hash": "g5h6i7j"},
    ]
    
    # Generate release
    release = generate_changelog_from_commits(
        commits=commits,
        version="2.0.0",
        date=datetime.now()
    )
    
    print(f"\nGenerated release: {release.version}")
    print(f"Total changes: {release.total_changes()}")
    
    print("\nBy type:")
    for change_type, entries in release.changes.items():
        if entries:
            print(f"\n  {change_type.value}:")
            for entry in entries:
                breaking = " [BREAKING]" if entry.breaking else ""
                scope = f" ({entry.scope})" if entry.scope else ""
                print(f"    - {entry.description}{scope}{breaking}")


# ============================================================================
# Example 5: Comparing Versions and Diff
# ============================================================================

def example_version_diff():
    """Get changes between two versions."""
    print("\n" + "=" * 60)
    print("Example 5: Version Diff and Comparison")
    print("=" * 60)
    
    # Create a sample changelog
    changelog = create_changelog()
    
    # Add several releases
    changelog.add_release(create_release("2.0.0", date="2024-03-01", changes={
        ChangeType.ADDED: ["Major new features"],
        ChangeType.REMOVED: ["Legacy API"]
    }))
    changelog.add_release(create_release("1.5.0", date="2024-02-01", changes={
        ChangeType.ADDED: ["Minor features"],
        ChangeType.FIXED: ["Bug fixes"]
    }))
    changelog.add_release(create_release("1.4.0", date="2024-01-15", changes={
        ChangeType.ADDED: ["Some additions"],
        ChangeType.CHANGED: ["Improvements"]
    }))
    changelog.add_release(create_release("1.3.0", date="2024-01-01", changes={
        ChangeType.FIXED: ["Initial fixes"]
    }))
    
    # Get diff between versions
    print("\nChanges from v1.3.0 to v1.5.0:")
    diff = get_version_diff(changelog, "1.3.0", "1.5.0")
    
    for change_type, entries in diff.items():
        if entries:
            print(f"  {change_type.value}: {len(entries)} changes")
    
    # Compare versions
    print("\nVersion comparisons:")
    versions = ["1.3.0", "1.4.0", "1.5.0", "2.0.0"]
    for i in range(len(versions) - 1):
        cmp = compare_versions(versions[i], versions[i + 1])
        print(f"  {versions[i]} vs {versions[i + 1]}: {cmp}")


# ============================================================================
# Example 6: Quick Changelog Generation
# ============================================================================

def example_quick_changelog():
    """Quickly generate a simple changelog."""
    print("\n" + "=" * 60)
    print("Example 6: Quick Changelog Generation")
    print("=" * 60)
    
    # Simple dict-based changelog generation
    md = quick_changelog({
        "2.0.0": [
            "Complete rewrite of the core engine",
            "New modern UI design",
            "Performance improvements"
        ],
        "1.5.0": [
            "Added export functionality",
            "Fixed memory leak",
            "Improved error handling"
        ],
        "1.0.0": [
            "Initial release"
        ]
    }, title="My Project Changelog")
    
    print(md)


# ============================================================================
# Example 7: Validation and Suggestions
# ============================================================================

def example_validation():
    """Validate changelogs and suggest next versions."""
    print("\n" + "=" * 60)
    print("Example 7: Validation and Suggestions")
    print("=" * 60)
    
    # Validate a changelog
    valid_changelog = """# Changelog

## [1.0.0] - 2024-01-01

### Added
- Initial release
"""
    
    is_valid, errors = validate_changelog(valid_changelog)
    print(f"\nValid changelog check: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Invalid changelog
    invalid_changelog = "# Some Notes\n\nNo version headers here."
    is_valid, errors = validate_changelog(invalid_changelog)
    print(f"\nInvalid changelog check: {is_valid}")
    print(f"Errors: {errors}")
    
    # Validate versions
    print("\nVersion validation:")
    test_versions = ["1.0.0", "v2.3.4", "invalid", "1.0.0-alpha.1"]
    for v in test_versions:
        print(f"  {v}: {is_valid_version(v)}")
    
    # Suggest next version
    print("\nSuggesting next version:")
    changelog = parse_changelog(valid_changelog)
    next_v = suggest_next_version(changelog)
    print(f"  After {changelog.latest_release().version}, suggest: {next_v}")
    
    # Based on change type
    print("\nBump suggestions based on change type:")
    v = parse_version("1.0.0")
    print(f"  Removed features -> {bump_version(v, ChangeType.REMOVED)}")
    print(f"  Added features -> {bump_version(v, ChangeType.ADDED)}")
    print(f"  Bug fixes -> {bump_version(v, ChangeType.FIXED)}")


# ============================================================================
# Example 8: Output Formats
# ============================================================================

def example_output_formats():
    """Demonstrate different output formats."""
    print("\n" + "=" * 60)
    print("Example 8: Output Formats")
    print("=" * 60)
    
    changelog = create_changelog(
        title="Format Demo",
        description="Showing different output formats"
    )
    
    changelog.add_release(create_release(
        version="1.0.0",
        date="2024-01-01",
        changes={
            ChangeType.ADDED: ["Feature A", "Feature B"],
            ChangeType.FIXED: ["Bug fix"]
        }
    ))
    
    # Markdown
    print("\n--- Markdown Format ---")
    print(changelog.to_markdown())
    
    # JSON
    print("\n--- JSON Format ---")
    import json
    print(json.dumps(changelog.to_json_dict(), indent=2))
    
    # Plain text
    print("\n--- Plain Text Format ---")
    print(changelog.to_plain_text())


# ============================================================================
# Example 9: Merging Changelogs
# ============================================================================

def example_merge_changelogs():
    """Merge multiple changelogs."""
    print("\n" + "=" * 60)
    print("Example 9: Merging Changelogs")
    print("=" * 60)
    
    # Create two changelogs (e.g., from different branches)
    changelog1 = create_changelog(title="Project A")
    changelog1.add_release(create_release("1.0.0", changes={
        ChangeType.ADDED: ["Feature from branch A"]
    }))
    
    changelog2 = create_changelog(title="Project B")
    changelog2.add_release(create_release("1.0.0", changes={
        ChangeType.FIXED: ["Bug fix from branch B"]
    }))
    changelog2.add_release(create_release("0.9.0", changes={
        ChangeType.ADDED: ["Initial work"]
    }))
    
    # Merge them
    merged = merge_changelogs([changelog1, changelog2])
    
    print(f"\nMerged changelog has {len(merged.releases)} releases")
    print(f"v1.0.0 has {merged.get_release('1.0.0').total_changes()} changes")
    
    print("\nMerged output:")
    print(merged.to_markdown())


# ============================================================================
# Example 10: Real-World Use Case
# ============================================================================

def example_real_world():
    """Real-world use case: maintaining a project changelog."""
    print("\n" + "=" * 60)
    print("Example 10: Real-World Use Case")
    print("=" * 60)
    
    # Simulate reading an existing changelog
    existing = """# Changelog

## [1.0.0] - 2024-01-01

### Added
- Initial release with core features
"""
    
    changelog = parse_changelog(existing)
    
    # Prepare a new release from recent work
    recent_commits = [
        {"message": "feat: add CSV export", "hash": "abc123"},
        {"message": "feat: add JSON export", "hash": "def456"},
        {"message": "fix: resolve encoding issue", "hash": "ghi789"},
        {"message": "docs: update readme", "hash": "jkl012"},
    ]
    
    # Determine next version
    next_version = suggest_next_version(changelog)
    
    # For this example, we'll bump minor for new features
    new_version = changelog.latest_release().version.bump_minor()
    
    print(f"\nCurrent version: {changelog.latest_release().version}")
    print(f"New version will be: {new_version}")
    
    # Generate the release
    new_release = generate_changelog_from_commits(
        commits=recent_commits,
        version=new_version,
        date=datetime.now()
    )
    
    # Add to changelog
    changelog.add_release(new_release)
    
    print("\nUpdated changelog:")
    print("-" * 60)
    print(changelog.to_markdown())
    
    # Generate release notes for the new version
    print("\nRelease notes for v{new_version}:")
    print("-" * 60)
    print(get_release_notes(changelog, new_version))


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("CHANGELOG UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_parse_changelog()
    example_create_changelog()
    example_version_operations()
    example_generate_from_commits()
    example_version_diff()
    example_quick_changelog()
    example_validation()
    example_output_formats()
    example_merge_changelogs()
    example_real_world()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()