"""
Semantic Versioning Utilities

A comprehensive implementation of Semantic Versioning 2.0.0 (https://semver.org/)
with zero external dependencies.

Features:
- Parse semantic version strings
- Compare versions (supports <, >, <=, >=, ==, !=)
- Version range matching (satisfies)
- Bump versions (major, minor, patch, prerelease)
- Pre-release and build metadata support
- Sort collections of versions
"""

import re
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, Iterator
from functools import total_ordering


@total_ordering
@dataclass
class SemanticVersion:
    """
    Represents a semantic version following SemVer 2.0.0 specification.
    
    Format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
    
    Examples:
        1.0.0
        2.1.3-alpha
        3.0.0-beta.2+build.123
    """
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
    
    def __repr__(self) -> str:
        return f"SemanticVersion({self})"
    
    def __hash__(self) -> int:
        # Build metadata doesn't affect equality/hash
        return hash((self.major, self.minor, self.patch, self.prerelease))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        # Build metadata is ignored in comparisons
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch and
            self.prerelease == other.prerelease
        )
    
    def __lt__(self, other: "SemanticVersion") -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        
        # Compare major.minor.patch
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        
        # When versions are equal, pre-release has lower precedence
        # than normal version
        if self.prerelease is None and other.prerelease is None:
            return False
        if self.prerelease is None:
            return False  # self is release, other is pre-release
        if other.prerelease is None:
            return True   # self is pre-release, other is release
        
        # Compare pre-release identifiers
        return self._compare_prerelease(self.prerelease, other.prerelease) < 0
    
    @staticmethod
    def _compare_prerelease(a: str, b: str) -> int:
        """
        Compare pre-release strings according to SemVer spec.
        
        Identifiers are compared dot-separated:
        - Numeric identifiers are compared as integers
        - Alphanumeric identifiers are compared lexically
        - Numeric identifiers always have lower precedence than alphanumeric
        """
        parts_a = a.split('.')
        parts_b = b.split('.')
        
        for pa, pb in zip(parts_a, parts_b):
            a_is_num = pa.isdigit()
            b_is_num = pb.isdigit()
            
            if a_is_num and b_is_num:
                # Both numeric: compare as integers
                na, nb = int(pa), int(pb)
                if na != nb:
                    return -1 if na < nb else 1
            elif a_is_num:
                # Numeric < alphanumeric
                return -1
            elif b_is_num:
                # Alphanumeric > numeric
                return 1
            else:
                # Both alphanumeric: compare lexically
                if pa != pb:
                    return -1 if pa < pb else 1
        
        # Shorter pre-release has lower precedence
        if len(parts_a) < len(parts_b):
            return -1
        elif len(parts_a) > len(parts_b):
            return 1
        
        return 0
    
    def bump_major(self) -> "SemanticVersion":
        """Increment major version, reset minor and patch."""
        return SemanticVersion(
            major=self.major + 1,
            minor=0,
            patch=0,
            build=self.build
        )
    
    def bump_minor(self) -> "SemanticVersion":
        """Increment minor version, reset patch."""
        return SemanticVersion(
            major=self.major,
            minor=self.minor + 1,
            patch=0,
            build=self.build
        )
    
    def bump_patch(self) -> "SemanticVersion":
        """Increment patch version."""
        return SemanticVersion(
            major=self.major,
            minor=self.minor,
            patch=self.patch + 1,
            build=self.build
        )
    
    def bump_prerelease(self, prerelease_prefix: str = "alpha") -> "SemanticVersion":
        """
        Bump or create pre-release version.
        
        Args:
            prerelease_prefix: Pre-release type (alpha, beta, rc, etc.)
        
        Returns:
            New SemanticVersion with bumped pre-release
        """
        if self.prerelease and self.prerelease.startswith(f"{prerelease_prefix}."):
            try:
                num = int(self.prerelease.split('.')[1])
                new_prerelease = f"{prerelease_prefix}.{num + 1}"
            except (IndexError, ValueError):
                new_prerelease = f"{prerelease_prefix}.1"
        else:
            new_prerelease = f"{prerelease_prefix}.1"
        
        return SemanticVersion(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=new_prerelease
        )
    
    def release(self) -> "SemanticVersion":
        """Remove pre-release identifier to create release version."""
        return SemanticVersion(
            major=self.major,
            minor=self.minor,
            patch=self.patch
        )
    
    def with_build(self, build: str) -> "SemanticVersion":
        """Return a copy with build metadata."""
        return SemanticVersion(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=self.prerelease,
            build=build
        )
    
    @property
    def is_prerelease(self) -> bool:
        """Check if this is a pre-release version."""
        return self.prerelease is not None
    
    @property
    def is_release(self) -> bool:
        """Check if this is a release version (no prerelease)."""
        return self.prerelease is None
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to version tuple (major, minor, patch)."""
        return (self.major, self.minor, self.patch)
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "prerelease": self.prerelease,
            "build": self.build,
            "version": str(self)
        }


# Version regex pattern following SemVer 2.0.0 specification
SEMVER_PATTERN = re.compile(
    r'^(?P<major>0|[1-9]\d*)'
    r'\.(?P<minor>0|[1-9]\d*)'
    r'\.(?P<patch>0|[1-9]\d*)'
    r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)


def parse(version_str: str) -> SemanticVersion:
    """
    Parse a semantic version string.
    
    Args:
        version_str: Version string to parse
        
    Returns:
        SemanticVersion object
        
    Raises:
        ValueError: If version string is not valid SemVer
        
    Examples:
        >>> parse("1.2.3")
        SemanticVersion(1.2.3)
        >>> parse("2.0.0-alpha.1")
        SemanticVersion(2.0.0-alpha.1)
        >>> parse("3.1.4+build.123")
        SemanticVersion(3.1.4+build.123)
    """
    match = SEMVER_PATTERN.match(version_str.strip())
    if not match:
        raise ValueError(f"Invalid semantic version: {version_str}")
    
    groups = match.groupdict()
    
    return SemanticVersion(
        major=int(groups['major']),
        minor=int(groups['minor']),
        patch=int(groups['patch']),
        prerelease=groups.get('prerelease'),
        build=groups.get('build')
    )


def try_parse(version_str: str) -> Optional[SemanticVersion]:
    """
    Try to parse a version string, returning None on failure.
    
    Args:
        version_str: Version string to parse
        
    Returns:
        SemanticVersion or None if invalid
    """
    try:
        return parse(version_str)
    except ValueError:
        return None


def is_valid(version_str: str) -> bool:
    """
    Check if a string is a valid semantic version.
    
    Args:
        version_str: String to check
        
    Returns:
        True if valid SemVer, False otherwise
    """
    return try_parse(version_str) is not None


def compare(a: Union[str, SemanticVersion], b: Union[str, SemanticVersion]) -> int:
    """
    Compare two versions.
    
    Args:
        a: First version (string or SemanticVersion)
        b: Second version (string or SemanticVersion)
        
    Returns:
        -1 if a < b, 0 if a == b, 1 if a > b
        
    Examples:
        >>> compare("1.0.0", "2.0.0")
        -1
        >>> compare("2.0.0", "1.0.0")
        1
        >>> compare("1.0.0", "1.0.0")
        0
    """
    if isinstance(a, str):
        a = parse(a)
    if isinstance(b, str):
        b = parse(b)
    
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def sort_versions(versions: List[Union[str, SemanticVersion]], 
                  reverse: bool = False) -> List[SemanticVersion]:
    """
    Sort a list of versions.
    
    Args:
        versions: List of version strings or SemanticVersion objects
        reverse: Sort in descending order if True
        
    Returns:
        Sorted list of SemanticVersion objects
        
    Examples:
        >>> sort_versions(["2.0.0", "1.0.0", "1.5.0"])
        [SemanticVersion(1.0.0), SemanticVersion(1.5.0), SemanticVersion(2.0.0)]
    """
    parsed = [parse(v) if isinstance(v, str) else v for v in versions]
    return sorted(parsed, reverse=reverse)


def min_version(*versions: Union[str, SemanticVersion]) -> SemanticVersion:
    """Return the minimum version from the given versions."""
    parsed = [parse(v) if isinstance(v, str) else v for v in versions]
    return min(parsed)


def max_version(*versions: Union[str, SemanticVersion]) -> SemanticVersion:
    """Return the maximum version from the given versions."""
    parsed = [parse(v) if isinstance(v, str) else v for v in versions]
    return max(parsed)


class VersionRange:
    """
    Represents a version range constraint.
    
    Supports:
    - Exact: "1.0.0"
    - Greater than: ">1.0.0"
    - Greater than or equal: ">=1.0.0"
    - Less than: "<1.0.0"
    - Less than or equal: "<=1.0.0"
    - Caret range: "^1.2.3" (compatible with 1.2.3)
    - Tilde range: "~1.2.3" (approximately equivalent to 1.2.3)
    - Range: ">=1.0.0 <2.0.0"
    - Or: "1.0.0 || 2.0.0"
    - X-range: "1.x", "1.2.x"
    
    Examples:
        >>> vr = VersionRange("^1.2.3")
        >>> vr.satisfies("1.2.4")
        True
        >>> vr.satisfies("2.0.0")
        False
    """
    
    def __init__(self, range_str: str):
        """
        Initialize a version range.
        
        Args:
            range_str: Range specification string
        """
        self.original = range_str.strip()
        self._constraints = self._parse(self.original)
    
    def _parse(self, range_str: str) -> List[callable]:
        """Parse range string into constraint functions."""
        constraints = []
        
        # Handle OR conditions
        if '||' in range_str:
            parts = range_str.split('||')
            or_ranges = [VersionRange(p.strip()) for p in parts]
            return [lambda v, ranges=or_ranges: any(r.satisfies(v) for r in ranges)]
        
        # Handle space-separated AND conditions
        parts = range_str.split()
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            constraint = self._parse_single(part)
            if constraint:
                constraints.append(constraint)
        
        return constraints
    
    def _parse_single(self, part: str) -> Optional[callable]:
        """Parse a single constraint."""
        # Exact version
        if SEMVER_PATTERN.match(part):
            version = parse(part)
            return lambda v: v == version
        
        # Operators
        if part.startswith('>='):
            version = parse(part[2:])
            return lambda v, ver=version: v >= ver
        if part.startswith('<='):
            version = parse(part[2:])
            return lambda v, ver=version: v <= ver
        if part.startswith('>'):
            version = parse(part[1:])
            return lambda v, ver=version: v > ver
        if part.startswith('<'):
            version = parse(part[1:])
            return lambda v, ver=version: v < ver
        if part.startswith('='):
            version = parse(part[1:])
            return lambda v, ver=version: v == ver
        
        # Caret range ^1.2.3 -> >=1.2.3 <2.0.0
        if part.startswith('^'):
            return self._parse_caret(part[1:])
        
        # Tilde range ~1.2.3 -> >=1.2.3 <1.3.0
        if part.startswith('~'):
            return self._parse_tilde(part[1:])
        
        # X-range: 1.x, 1.2.x, 1.*, 1.2.*
        if 'x' in part or 'X' in part or '*' in part:
            return self._parse_x_range(part)
        
        return None
    
    def _parse_caret(self, version_str: str) -> callable:
        """Parse caret range (^)."""
        # Handle partial versions
        parts = version_str.split('.')
        
        if len(parts) == 1:
            # ^1 -> >=1.0.0 <2.0.0
            major = int(parts[0])
            min_v = SemanticVersion(major, 0, 0)
            max_v = SemanticVersion(major + 1, 0, 0)
        elif len(parts) == 2:
            # ^1.2 -> >=1.2.0 <2.0.0
            major, minor = int(parts[0]), int(parts[1])
            min_v = SemanticVersion(major, minor, 0)
            max_v = SemanticVersion(major + 1, 0, 0)
        else:
            # ^1.2.3 -> >=1.2.3 <2.0.0 (if major > 0)
            # ^0.2.3 -> >=0.2.3 <0.3.0 (if major == 0)
            # ^0.0.3 -> >=0.0.3 <0.0.4 (if major == 0, minor == 0)
            version = parse(version_str)
            min_v = version
            
            if version.major > 0:
                max_v = SemanticVersion(version.major + 1, 0, 0)
            elif version.minor > 0:
                max_v = SemanticVersion(0, version.minor + 1, 0)
            else:
                max_v = SemanticVersion(0, 0, version.patch + 1)
        
        return lambda v, minv=min_v, maxv=max_v: minv <= v < maxv
    
    def _parse_tilde(self, version_str: str) -> callable:
        """Parse tilde range (~)."""
        parts = version_str.split('.')
        
        if len(parts) == 1:
            # ~1 -> >=1.0.0 <2.0.0
            major = int(parts[0])
            min_v = SemanticVersion(major, 0, 0)
            max_v = SemanticVersion(major + 1, 0, 0)
        elif len(parts) == 2:
            # ~1.2 -> >=1.2.0 <1.3.0
            major, minor = int(parts[0]), int(parts[1])
            min_v = SemanticVersion(major, minor, 0)
            max_v = SemanticVersion(major, minor + 1, 0)
        else:
            # ~1.2.3 -> >=1.2.3 <1.3.0 (use full version as min)
            version = parse(version_str)
            min_v = version
            max_v = SemanticVersion(version.major, version.minor + 1, 0)
        
        return lambda v, minv=min_v, maxv=max_v: minv <= v < maxv
    
    def _parse_x_range(self, version_str: str) -> callable:
        """Parse X-range (1.x, 1.2.x, etc.)."""
        parts = version_str.replace('X', 'x').replace('*', 'x').split('.')
        
        if len(parts) >= 3 and parts[2] == 'x':
            # 1.2.x -> >=1.2.0 <1.3.0
            major, minor = int(parts[0]), int(parts[1])
            min_v = SemanticVersion(major, minor, 0)
            max_v = SemanticVersion(major, minor + 1, 0)
        elif len(parts) >= 2 and parts[1] == 'x':
            # 1.x -> >=1.0.0 <2.0.0
            major = int(parts[0])
            min_v = SemanticVersion(major, 0, 0)
            max_v = SemanticVersion(major + 1, 0, 0)
        else:
            return lambda v: False
        
        return lambda v, minv=min_v, maxv=max_v: minv <= v < maxv
    
    def satisfies(self, version: Union[str, SemanticVersion]) -> bool:
        """
        Check if a version satisfies this range.
        
        Args:
            version: Version to check
            
        Returns:
            True if version satisfies the range
        """
        if isinstance(version, str):
            version = parse(version)
        
        return all(constraint(version) for constraint in self._constraints)
    
    def __str__(self) -> str:
        return self.original
    
    def __repr__(self) -> str:
        return f"VersionRange({self.original!r})"


def satisfies(version: Union[str, SemanticVersion], range_str: str) -> bool:
    """
    Check if a version satisfies a range.
    
    Args:
        version: Version to check
        range_str: Range specification
        
    Returns:
        True if version satisfies the range
        
    Examples:
        >>> satisfies("1.2.5", "^1.2.3")
        True
        >>> satisfies("2.0.0", "^1.2.3")
        False
    """
    return VersionRange(range_str).satisfies(version)


def coerce(version_str: str) -> Optional[SemanticVersion]:
    """
    Try to coerce a loose version string into SemVer.
    
    Handles common formats like:
    - "1" -> 1.0.0
    - "1.2" -> 1.2.0
    - "v1.2.3" -> 1.2.3
    
    Args:
        version_str: Version string to coerce
        
    Returns:
        SemanticVersion if coercible, None otherwise
    """
    # Remove leading 'v' or 'V'
    version_str = version_str.strip()
    if version_str and version_str[0].lower() == 'v':
        version_str = version_str[1:]
    
    # Try direct parse first
    parsed = try_parse(version_str)
    if parsed:
        return parsed
    
    # Try to add missing parts
    parts = version_str.replace('-', '.').replace('+', '.').split('.')
    
    try:
        nums = []
        prerelease = None
        build = None
        
        for i, part in enumerate(parts):
            if part.isdigit():
                nums.append(int(part))
            elif i >= 3:
                # Could be prerelease or build
                if prerelease is None:
                    prerelease = part
                else:
                    build = part
        
        # Must have at least one numeric part for coercion
        if not nums:
            return None
        
        while len(nums) < 3:
            nums.append(0)
        
        return SemanticVersion(
            major=nums[0],
            minor=nums[1],
            patch=nums[2],
            prerelease=prerelease,
            build=build
        )
    except (ValueError, IndexError):
        return None


def diff(a: Union[str, SemanticVersion], b: Union[str, SemanticVersion]) -> str:
    """
    Determine the type of difference between two versions.
    
    Args:
        a: First version
        b: Second version
        
    Returns:
        'major', 'minor', 'patch', 'prerelease', or 'none'
        
    Examples:
        >>> diff("1.0.0", "2.0.0")
        'major'
        >>> diff("1.0.0", "1.1.0")
        'minor'
        >>> diff("1.0.0", "1.0.1")
        'patch'
    """
    if isinstance(a, str):
        a = parse(a)
    if isinstance(b, str):
        b = parse(b)
    
    if a.major != b.major:
        return 'major'
    if a.minor != b.minor:
        return 'minor'
    if a.patch != b.patch:
        return 'patch'
    if a.prerelease != b.prerelease:
        return 'prerelease'
    return 'none'


def is_compatible(a: Union[str, SemanticVersion], 
                  b: Union[str, SemanticVersion],
                  strict: bool = False) -> bool:
    """
    Check if two versions are compatible (same major version).
    
    Args:
        a: First version
        b: Second version
        strict: If True, also requires same minor version
        
    Returns:
        True if versions are compatible
        
    Examples:
        >>> is_compatible("1.2.0", "1.3.0")
        True
        >>> is_compatible("1.0.0", "2.0.0")
        False
    """
    if isinstance(a, str):
        a = parse(a)
    if isinstance(b, str):
        b = parse(b)
    
    if strict:
        return a.major == b.major and a.minor == b.minor
    return a.major == b.major


def next_version(version: Union[str, SemanticVersion], 
                 release_type: str) -> SemanticVersion:
    """
    Get the next version for a given release type.
    
    Args:
        version: Current version
        release_type: One of 'major', 'minor', 'patch', 'prerelease'
        
    Returns:
        Next SemanticVersion
        
    Examples:
        >>> next_version("1.2.3", "major")
        SemanticVersion(2.0.0)
        >>> next_version("1.2.3", "minor")
        SemanticVersion(1.3.0)
    """
    if isinstance(version, str):
        version = parse(version)
    
    if release_type == 'major':
        return version.bump_major()
    elif release_type == 'minor':
        return version.bump_minor()
    elif release_type == 'patch':
        return version.bump_patch()
    elif release_type == 'prerelease':
        return version.bump_prerelease()
    else:
        raise ValueError(f"Unknown release type: {release_type}")


class VersionSet:
    """
    A collection of versions with set operations.
    
    Examples:
        >>> vs = VersionSet(["1.0.0", "1.1.0", "2.0.0"])
        >>> "1.1.0" in vs
        True
        >>> vs.latest()
        SemanticVersion(2.0.0)
    """
    
    def __init__(self, versions: Optional[List[Union[str, SemanticVersion]]] = None):
        """Initialize with optional list of versions."""
        self._versions: set = set()
        if versions:
            for v in versions:
                self.add(v)
    
    def add(self, version: Union[str, SemanticVersion]) -> None:
        """Add a version to the set."""
        if isinstance(version, str):
            version = parse(version)
        self._versions.add(version)
    
    def remove(self, version: Union[str, SemanticVersion]) -> None:
        """Remove a version from the set."""
        if isinstance(version, str):
            version = parse(version)
        self._versions.discard(version)
    
    def __contains__(self, version: Union[str, SemanticVersion]) -> bool:
        if isinstance(version, str):
            version = try_parse(version)
            if version is None:
                return False
        return version in self._versions
    
    def __len__(self) -> int:
        return len(self._versions)
    
    def __iter__(self) -> Iterator[SemanticVersion]:
        return iter(self._versions)
    
    def sorted(self, reverse: bool = False) -> List[SemanticVersion]:
        """Return sorted list of versions."""
        return sorted(self._versions, reverse=reverse)
    
    def latest(self) -> Optional[SemanticVersion]:
        """Get the latest (highest) version."""
        if not self._versions:
            return None
        return max(self._versions)
    
    def earliest(self) -> Optional[SemanticVersion]:
        """Get the earliest (lowest) version."""
        if not self._versions:
            return None
        return min(self._versions)
    
    def filter(self, range_str: str) -> "VersionSet":
        """Return new VersionSet with versions that satisfy the range."""
        vr = VersionRange(range_str)
        return VersionSet([v for v in self._versions if vr.satisfies(v)])
    
    def to_list(self) -> List[str]:
        """Convert to list of version strings."""
        return [str(v) for v in sorted(self._versions)]


# Convenience exports
__all__ = [
    'SemanticVersion',
    'VersionRange',
    'VersionSet',
    'parse',
    'try_parse',
    'is_valid',
    'compare',
    'sort_versions',
    'min_version',
    'max_version',
    'satisfies',
    'coerce',
    'diff',
    'is_compatible',
    'next_version',
    'SEMVER_PATTERN',
]