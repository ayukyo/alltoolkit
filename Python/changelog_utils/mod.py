#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Changelog Utilities Module
=======================================
A comprehensive changelog parsing, generation, and manipulation utility module 
for Python with zero external dependencies.

Features:
    - Parse CHANGELOG.md (Keep a Changelog format)
    - Generate standardized changelogs
    - Extract version information
    - Compare versions and differences
    - Format conversion (Markdown, JSON, plain text)
    - Version sorting and validation
    - Release note generation

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ============================================================================
# Enums
# ============================================================================

class ChangeType(Enum):
    """Types of changes in Keep a Changelog format."""
    ADDED = "Added"
    CHANGED = "Changed"
    DEPRECATED = "Deprecated"
    REMOVED = "Removed"
    FIXED = "Fixed"
    SECURITY = "Security"


class ReleaseType(Enum):
    """Types of releases based on version changes."""
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"
    BUILD = "build"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Version:
    """Represents a semantic version."""
    major: int = 0
    minor: int = 0
    patch: int = 0
    prerelease: Optional[str] = None
    build: Optional[str] = None
    
    def __str__(self) -> str:
        """Convert to string representation."""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Version):
            return False
        return (self.major == other.major and 
                self.minor == other.minor and 
                self.patch == other.patch and
                self.prerelease == other.prerelease and
                self.build == other.build)
    
    def __lt__(self, other: "Version") -> bool:
        """Compare versions."""
        if not isinstance(other, Version):
            return NotImplemented
        # Compare major, minor, patch
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        # Prerelease versions have lower precedence
        if self.prerelease and not other.prerelease:
            return True
        if not self.prerelease and other.prerelease:
            return False
        if self.prerelease and other.prerelease:
            return self.prerelease < other.prerelease
        return False
    
    def __le__(self, other: "Version") -> bool:
        return self == other or self < other
    
    def __gt__(self, other: "Version") -> bool:
        return not self <= other
    
    def __ge__(self, other: "Version") -> bool:
        return not self < other
    
    @classmethod
    def parse(cls, version_str: str) -> "Version":
        """Parse a version string into a Version object."""
        version_str = version_str.strip()
        # Remove 'v' prefix if present
        if version_str.lower().startswith('v'):
            version_str = version_str[1:]
        
        # Parse build metadata
        build = None
        if '+' in version_str:
            version_str, build = version_str.split('+', 1)
        
        # Parse prerelease
        prerelease = None
        if '-' in version_str:
            version_str, prerelease = version_str.split('-', 1)
        
        # Parse major.minor.patch
        parts = version_str.split('.')
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        
        return cls(major=major, minor=minor, patch=patch, 
                   prerelease=prerelease, build=build)
    
    def bump_major(self) -> "Version":
        """Bump major version."""
        return Version(major=self.major + 1, minor=0, patch=0)
    
    def bump_minor(self) -> "Version":
        """Bump minor version."""
        return Version(major=self.major, minor=self.minor + 1, patch=0)
    
    def bump_patch(self) -> "Version":
        """Bump patch version."""
        return Version(major=self.major, minor=self.minor, patch=self.patch + 1)
    
    def get_release_type(self) -> ReleaseType:
        """Get the release type."""
        if self.prerelease:
            return ReleaseType.PRERELEASE
        if self.build:
            return ReleaseType.BUILD
        if self.major == 0:
            if self.minor == 0:
                return ReleaseType.PATCH
            return ReleaseType.MINOR
        if self.minor == 0 and self.patch == 0:
            return ReleaseType.MAJOR
        if self.patch == 0:
            return ReleaseType.MINOR
        return ReleaseType.PATCH


@dataclass
class ChangeEntry:
    """Represents a single change entry."""
    description: str
    change_type: ChangeType
    scope: Optional[str] = None
    issue_ref: Optional[str] = None
    breaking: bool = False
    
    def to_markdown(self) -> str:
        """Convert to Markdown list item."""
        prefix = "**BREAKING** " if self.breaking else ""
        scope = f"**{self.scope}**: " if self.scope else ""
        issue = f" ([#{self.issue_ref}])" if self.issue_ref else ""
        return f"- {prefix}{scope}{self.description}{issue}"


@dataclass
class Release:
    """Represents a single release."""
    version: Version
    date: Optional[datetime] = None
    yanked: bool = False
    changes: Dict[ChangeType, List[ChangeEntry]] = field(default_factory=dict)
    description: Optional[str] = None
    
    def __post_init__(self):
        """Initialize changes dict if empty."""
        if not self.changes:
            self.changes = {ct: [] for ct in ChangeType}
    
    def add_change(self, entry: ChangeEntry) -> None:
        """Add a change entry."""
        self.changes[entry.change_type].append(entry)
    
    def get_changes(self, change_type: ChangeType) -> List[ChangeEntry]:
        """Get changes by type."""
        return self.changes.get(change_type, [])
    
    def total_changes(self) -> int:
        """Get total number of changes."""
        return sum(len(entries) for entries in self.changes.values())
    
    def to_markdown(self, include_empty: bool = False) -> str:
        """Convert release to Markdown."""
        lines = [f"## [{self.version}]"]
        
        if self.date:
            date_str = self.date.strftime("%Y-%m-%d")
            if self.yanked:
                lines[0] = f"## [{self.version}] - {date_str} [YANKED]"
            else:
                lines[0] = f"## [{self.version}] - {date_str}"
        elif self.yanked:
            lines[0] = f"## [{self.version}] [YANKED]"
        
        if self.description:
            lines.append(self.description)
            lines.append("")
        
        for change_type in ChangeType:
            entries = self.changes.get(change_type, [])
            if entries or include_empty:
                lines.append(f"### {change_type.value}")
                for entry in entries:
                    lines.append(entry.to_markdown())
                if entries:
                    lines.append("")
        
        return "\n".join(lines)


@dataclass
class Changelog:
    """Represents a complete changelog."""
    title: str = "Changelog"
    description: str = ""
    releases: List[Release] = field(default_factory=list)
    
    def add_release(self, release: Release) -> None:
        """Add a release."""
        self.releases.append(release)
        # Sort releases by version (descending)
        self.releases.sort(key=lambda r: r.version, reverse=True)
    
    def get_release(self, version: Union[str, Version]) -> Optional[Release]:
        """Get a release by version."""
        if isinstance(version, str):
            version = Version.parse(version)
        for release in self.releases:
            if release.version == version:
                return release
        return None
    
    def latest_release(self) -> Optional[Release]:
        """Get the latest release."""
        return self.releases[0] if self.releases else None
    
    def get_versions(self) -> List[Version]:
        """Get all versions."""
        return [r.version for r in self.releases]
    
    def to_markdown(self) -> str:
        """Convert changelog to Markdown."""
        lines = [f"# {self.title}", ""]
        
        if self.description:
            lines.append(self.description)
            lines.append("")
        
        for release in self.releases:
            lines.append(release.to_markdown())
            lines.append("")
        
        return "\n".join(lines)
    
    def to_json_dict(self) -> Dict:
        """Convert to JSON-serializable dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "releases": [
                {
                    "version": str(r.version),
                    "date": r.date.isoformat() if r.date else None,
                    "yanked": r.yanked,
                    "description": r.description,
                    "changes": {
                        ct.value: [
                            {
                                "description": e.description,
                                "scope": e.scope,
                                "issue_ref": e.issue_ref,
                                "breaking": e.breaking
                            }
                            for e in entries
                        ]
                        for ct, entries in r.changes.items()
                        if entries
                    }
                }
                for r in self.releases
            ]
        }
    
    def to_plain_text(self) -> str:
        """Convert to plain text."""
        lines = [self.title, "=" * len(self.title), ""]
        
        for release in self.releases:
            date_str = f" ({release.date.strftime('%Y-%m-%d')})" if release.date else ""
            lines.append(f"Version {release.version}{date_str}")
            lines.append("-" * 30)
            
            for change_type, entries in release.changes.items():
                if entries:
                    lines.append(f"\n{change_type.value}:")
                    for entry in entries:
                        prefix = "[BREAKING] " if entry.breaking else ""
                        lines.append(f"  - {prefix}{entry.description}")
            
            lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# Parser Functions
# ============================================================================

def parse_version(version_str: str) -> Version:
    """Parse a version string into a Version object."""
    return Version.parse(version_str)


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse a date string into a datetime object."""
    date_str = date_str.strip()
    
    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",  # US format
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%d %H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def parse_changelog(content: str) -> Changelog:
    """Parse a changelog file content into a Changelog object."""
    lines = content.split('\n')
    changelog = Changelog()
    
    # Extract title
    title_match = re.match(r'^#\s+(.+)$', lines[0] if lines else '')
    if title_match:
        changelog.title = title_match.group(1)
    
    # Extract description (text between title and first release)
    desc_lines = []
    for i, line in enumerate(lines[1:], 1):
        if re.match(r'^##\s+\[', line):
            break
        if line.strip() and not line.startswith('[') and not line.startswith('['):
            desc_lines.append(line)
    changelog.description = '\n'.join(desc_lines).strip()
    
    # Parse releases
    current_release = None
    current_change_type = None
    
    for line in lines:
        # Release header: ## [version] - date or ## [version]
        release_match = re.match(r'^##\s+\[([^\]]+)\](?:\s*-\s*([^\[]+?))?(?:\s+\[YANKED\])?\s*$', line)
        if release_match:
            if current_release:
                changelog.add_release(current_release)
            
            version = Version.parse(release_match.group(1))
            date = parse_date(release_match.group(2)) if release_match.group(2) else None
            yanked = '[YANKED]' in line
            
            current_release = Release(version=version, date=date, yanked=yanked)
            current_change_type = None
            continue
        
        # Change type header: ### Added, ### Changed, etc.
        type_match = re.match(r'^###\s+(\w+)', line)
        if type_match and current_release:
            type_name = type_match.group(1)
            try:
                current_change_type = ChangeType(type_name)
            except ValueError:
                current_change_type = None
            continue
        
        # Change entry: - description
        entry_match = re.match(r'^-\s+(.+)$', line)
        if entry_match and current_release and current_change_type:
            description = entry_match.group(1)
            breaking = '**BREAKING**' in description or 'BREAKING CHANGE:' in description
            
            # Extract issue reference
            issue_ref = None
            issue_match = re.search(r'\(?\[#?(\d+)\]\)?', description)
            if issue_match:
                issue_ref = issue_match.group(1)
            
            # Extract scope
            scope = None
            scope_match = re.match(r'\*\*(.+?)\*\*:\s*', description)
            if scope_match:
                scope = scope_match.group(1)
            
            # Clean description
            desc_clean = re.sub(r'\*\*BREAKING\*\*\s*', '', description)
            desc_clean = re.sub(r'\*\*(.+?)\*\*:\s*', '', desc_clean, count=1)
            desc_clean = re.sub(r'\(?\[#?\d+\]\)?', '', desc_clean).strip()
            
            entry = ChangeEntry(
                description=desc_clean,
                change_type=current_change_type,
                scope=scope,
                issue_ref=issue_ref,
                breaking=breaking
            )
            current_release.add_change(entry)
    
    # Add last release
    if current_release:
        changelog.add_release(current_release)
    
    return changelog


def parse_changelog_file(filepath: str) -> Changelog:
    """Parse a changelog file into a Changelog object."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return parse_changelog(content)


# ============================================================================
# Generation Functions
# ============================================================================

def create_release(
    version: Union[str, Version],
    changes: Optional[Dict[ChangeType, List[Union[str, ChangeEntry]]]] = None,
    date: Optional[Union[datetime, str]] = None,
    description: Optional[str] = None,
    yanked: bool = False
) -> Release:
    """Create a new release."""
    if isinstance(version, str):
        version = Version.parse(version)
    
    if isinstance(date, str):
        date = parse_date(date)
    
    release = Release(
        version=version,
        date=date,
        description=description,
        yanked=yanked
    )
    
    if changes:
        for change_type, entries in changes.items():
            for entry in entries:
                if isinstance(entry, str):
                    entry = ChangeEntry(description=entry, change_type=change_type)
                release.add_change(entry)
    
    return release


def create_changelog(
    title: str = "Changelog",
    description: str = "",
    releases: Optional[List[Release]] = None
) -> Changelog:
    """Create a new changelog."""
    changelog = Changelog(title=title, description=description)
    
    if releases:
        for release in releases:
            changelog.add_release(release)
    
    return changelog


def generate_changelog_from_commits(
    commits: List[Dict[str, str]],
    version: Union[str, Version],
    date: Optional[datetime] = None
) -> Release:
    """
    Generate a release from commit messages.
    
    Args:
        commits: List of dicts with 'message', 'hash', 'author', etc.
        version: Version string or Version object
        date: Release date
    
    Commits should follow conventional commit format:
    - feat: description -> Added
    - fix: description -> Fixed
    - docs: description -> Changed
    - refactor: description -> Changed
    - perf: description -> Changed
    - test: description -> Changed
    - build: description -> Changed
    - ci: description -> Changed
    - chore: description -> Changed
    - deprecate: description -> Deprecated
    - remove: description -> Removed
    - security: description -> Security
    """
    if isinstance(version, str):
        version = Version.parse(version)
    
    release = Release(version=version, date=date)
    
    # Map commit prefixes to change types
    prefix_map = {
        'feat': ChangeType.ADDED,
        'fix': ChangeType.FIXED,
        'security': ChangeType.SECURITY,
        'deprecate': ChangeType.DEPRECATED,
        'remove': ChangeType.REMOVED,
    }
    default_type = ChangeType.CHANGED
    
    for commit in commits:
        message = commit.get('message', '')
        hash_ref = commit.get('hash', '')[:7] if commit.get('hash') else None
        
        # Parse conventional commit
        match = re.match(r'^(\w+)(?:\((\w+)\))?:\s*(.+)$', message)
        if match:
            prefix = match.group(1)
            scope = match.group(2)
            desc = match.group(3)
            
            breaking = 'BREAKING CHANGE' in message or '!' in prefix
            change_type = prefix_map.get(prefix.replace('!', ''), default_type)
            
            entry = ChangeEntry(
                description=desc,
                change_type=change_type,
                scope=scope,
                issue_ref=hash_ref,
                breaking=breaking
            )
            release.add_change(entry)
    
    return release


# ============================================================================
# Comparison Functions
# ============================================================================

def compare_versions(v1: Union[str, Version], v2: Union[str, Version]) -> int:
    """
    Compare two versions.
    
    Returns:
        -1 if v1 < v2
         0 if v1 == v2
         1 if v1 > v2
    """
    if isinstance(v1, str):
        v1 = Version.parse(v1)
    if isinstance(v2, str):
        v2 = Version.parse(v2)
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    return 0


def get_version_diff(
    changelog: Changelog,
    from_version: Union[str, Version],
    to_version: Union[str, Version]
) -> Dict[ChangeType, List[ChangeEntry]]:
    """
    Get all changes between two versions.
    
    Returns a dict of all changes that occurred between from_version and to_version.
    """
    if isinstance(from_version, str):
        from_version = Version.parse(from_version)
    if isinstance(to_version, str):
        to_version = Version.parse(to_version)
    
    diff: Dict[ChangeType, List[ChangeEntry]] = {ct: [] for ct in ChangeType}
    
    for release in changelog.releases:
        if from_version < release.version <= to_version:
            for change_type, entries in release.changes.items():
                diff[change_type].extend(entries)
    
    return diff


def get_release_notes(
    changelog: Changelog,
    version: Union[str, Version],
    format: str = "markdown"
) -> str:
    """
    Generate release notes for a specific version.
    
    Args:
        changelog: Changelog object
        version: Version to generate notes for
        format: Output format ('markdown', 'json', 'text')
    """
    if isinstance(version, str):
        version = Version.parse(version)
    
    release = changelog.get_release(version)
    if not release:
        return ""
    
    if format == "json":
        import json
        return json.dumps(changelog.to_json_dict(), indent=2)
    elif format == "text":
        return changelog.to_plain_text()
    else:
        return release.to_markdown()


# ============================================================================
# Validation Functions
# ============================================================================

def is_valid_version(version_str: str) -> bool:
    """Check if a string is a valid semantic version."""
    try:
        Version.parse(version_str)
        return True
    except (ValueError, IndexError, AttributeError):
        return False


def validate_changelog(content: str) -> Tuple[bool, List[str]]:
    """
    Validate a changelog file content.
    
    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []
    
    # Check for title
    if not re.search(r'^#\s+.+$', content, re.MULTILINE):
        errors.append("Missing changelog title (expected '# Changelog' or similar)")
    
    # Check for at least one release
    if not re.search(r'^##\s+\[.+\]', content, re.MULTILINE):
        errors.append("No releases found (expected '## [version]' sections)")
    
    # Check version formats
    version_matches = re.findall(r'^##\s+\[([^\]]+)\]', content, re.MULTILINE)
    for version in version_matches:
        if not is_valid_version(version):
            errors.append(f"Invalid version format: {version}")
    
    # Check change types
    valid_types = {ct.value for ct in ChangeType}
    type_matches = re.findall(r'^###\s+(\w+)', content, re.MULTILINE)
    for change_type in type_matches:
        if change_type not in valid_types:
            errors.append(f"Unknown change type: {change_type}")
    
    return len(errors) == 0, errors


# ============================================================================
# Utility Functions
# ============================================================================

def bump_version(
    version: Union[str, Version],
    change_type: ChangeType
) -> Version:
    """
    Bump a version based on the type of changes.
    
    - ADDED: Minor bump
    - CHANGED: Minor bump
    - DEPRECATED: Minor bump  
    - REMOVED: Major bump
    - FIXED: Patch bump
    - SECURITY: Patch bump
    """
    if isinstance(version, str):
        version = Version.parse(version)
    
    if change_type in (ChangeType.REMOVED,):
        return version.bump_major()
    elif change_type in (ChangeType.ADDED, ChangeType.CHANGED, ChangeType.DEPRECATED):
        return version.bump_minor()
    else:  # FIXED, SECURITY
        return version.bump_patch()


def suggest_next_version(changelog: Changelog) -> Version:
    """Suggest the next version based on unreleased changes."""
    latest = changelog.latest_release()
    if not latest:
        return Version(major=0, minor=1, patch=0)
    
    # Check if there's an unreleased section (by name, not version)
    unreleased = None
    for release in changelog.releases:
        if str(release.version).lower() == "unreleased" or release.version.major == 0 and release.version.minor == 0 and release.version.patch == 0 and not release.date:
            unreleased = release
            break
    
    if unreleased:
        # Determine bump based on changes
        for change_type in [ChangeType.REMOVED]:
            if unreleased.get_changes(change_type):
                return latest.version.bump_major()
        
        for change_type in [ChangeType.ADDED, ChangeType.CHANGED, ChangeType.DEPRECATED]:
            if unreleased.get_changes(change_type):
                return latest.version.bump_minor()
        
        return latest.version.bump_patch()
    
    return latest.version.bump_patch()


def merge_changelogs(changelogs: List[Changelog]) -> Changelog:
    """Merge multiple changelogs into one."""
    if not changelogs:
        return Changelog()
    
    merged = Changelog(
        title=changelogs[0].title,
        description=changelogs[0].description
    )
    
    # Collect all releases
    all_releases: Dict[str, Release] = {}
    for changelog in changelogs:
        for release in changelog.releases:
            key = str(release.version)
            if key in all_releases:
                # Merge changes
                for ct, entries in release.changes.items():
                    all_releases[key].changes[ct].extend(entries)
            else:
                all_releases[key] = release
    
    # Sort by version descending
    sorted_versions = sorted(
        [Version.parse(v) for v in all_releases.keys()],
        reverse=True
    )
    
    for version in sorted_versions:
        merged.add_release(all_releases[str(version)])
    
    return merged


# ============================================================================
# Convenience Functions
# ============================================================================

def quick_changelog(changes: Dict[str, List[str]], title: str = "Changelog") -> str:
    """
    Quickly generate a simple changelog from a dict.
    
    Args:
        changes: Dict mapping version strings to lists of change descriptions
        title: Changelog title
    
    Example:
        quick_changelog({
            "1.0.0": ["Added feature X", "Fixed bug Y"],
            "0.9.0": ["Initial release"]
        })
    """
    changelog = create_changelog(title=title)
    
    for version_str, descriptions in changes.items():
        release = create_release(version=version_str, date=datetime.now())
        for desc in descriptions:
            # Try to infer change type from description
            lower_desc = desc.lower()
            if any(w in lower_desc for w in ['add', 'new', 'implement', 'create']):
                ct = ChangeType.ADDED
            elif any(w in lower_desc for w in ['fix', 'repair', 'resolve']):
                ct = ChangeType.FIXED
            elif any(w in lower_desc for w in ['remove', 'delete', 'drop']):
                ct = ChangeType.REMOVED
            elif any(w in lower_desc for w in ['deprecate', 'obsolete']):
                ct = ChangeType.DEPRECATED
            elif any(w in lower_desc for w in ['security', 'vulnerability', 'cve']):
                ct = ChangeType.SECURITY
            else:
                ct = ChangeType.CHANGED
            
            release.add_change(ChangeEntry(description=desc, change_type=ct))
        changelog.add_release(release)
    
    return changelog.to_markdown()


def extract_version_links(content: str) -> Dict[str, Optional[str]]:
    """
    Extract version comparison links from changelog footer.
    
    Returns dict mapping version to comparison URL (or None if not a link).
    """
    links = {}
    
    # Find all [version]: url patterns at end of file
    link_pattern = r'^\[([^\]]+)\]:\s*(.+)$'
    for match in re.finditer(link_pattern, content, re.MULTILINE):
        version = match.group(1)
        url = match.group(2)
        links[version] = url
    
    return links


if __name__ == "__main__":
    # Demo
    sample = """# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-01-15

### Added
- New feature for parsing changelogs
- Support for multiple output formats

### Fixed
- Bug in version comparison

### Security
- Fixed vulnerability in date parsing

## [0.9.0] - 2024-01-01

### Added
- Initial release

[1.0.0]: https://github.com/example/repo/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/example/repo/releases/tag/v0.9.0
"""
    
    changelog = parse_changelog(sample)
    print(f"Parsed {len(changelog.releases)} releases")
    print(f"Latest: {changelog.latest_release().version}")
    print(f"Total changes in 1.0.0: {changelog.get_release('1.0.0').total_changes()}")