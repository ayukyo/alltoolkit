//! Semver Utils - A comprehensive semantic versioning library
//! 
//! This crate provides utilities for parsing, comparing, and manipulating
//! semantic version strings according to the Semantic Versioning 2.0.0 specification.
//!
//! # Features
//! - Parse semver strings (major.minor.patch with optional pre-release and build metadata)
//! - Compare versions with all comparison operators
//! - Check version compatibility (major, minor, patch)
//! - Parse and evaluate version ranges
//! - Zero external dependencies
//!
//! # Example
//! ```
//! use semver_utils::{Version, VersionRange};
//!
//! let v1 = Version::parse("1.2.3")?;
//! let v2 = Version::parse("1.2.4")?;
//! 
//! assert!(v1 < v2);
//! assert!(v1.is_compatible(&Version::parse("1.2.0")?));
//! 
//! let range = VersionRange::parse(">=1.0.0 <2.0.0")?;
//! assert!(range.satisfies(&v1));
//! # Ok::<(), semver_utils::SemverError>(())
//! ```

use std::cmp::Ordering;
use std::fmt;
use std::str::FromStr;

/// Represents a semantic version
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Version {
    /// Major version number (X.y.z)
    pub major: u64,
    /// Minor version number (x.Y.z)
    pub minor: u64,
    /// Patch version number (x.y.Z)
    pub patch: u64,
    /// Pre-release version (e.g., "alpha.1", "beta.2")
    pub pre_release: Option<Vec<PreReleasePart>>,
    /// Build metadata (e.g., "exp.sha.5114f85")
    pub build: Option<String>,
}

/// A part of a pre-release version
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PreReleasePart {
    Numeric(u64),
    Alpha(String),
}

impl PreReleasePart {
    /// Parse a pre-release part from a string
    fn parse(s: &str) -> Result<Self, SemverError> {
        if s.is_empty() {
            return Err(SemverError::InvalidPreRelease);
        }
        
        // Check if it's a valid identifier
        if !s.chars().all(|c| c.is_ascii_alphanumeric() || c == '-') {
            return Err(SemverError::InvalidPreRelease);
        }
        
        // Numeric identifiers must not have leading zeros
        if s.chars().all(|c| c.is_ascii_digit()) {
            if s.len() > 1 && s.starts_with('0') {
                return Err(SemverError::InvalidPreRelease);
            }
            s.parse::<u64>()
                .map(PreReleasePart::Numeric)
                .map_err(|_| SemverError::InvalidPreRelease)
        } else {
            Ok(PreReleasePart::Alpha(s.to_string()))
        }
    }
}

impl PartialOrd for PreReleasePart {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for PreReleasePart {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            // Numeric < Alpha
            (PreReleasePart::Numeric(a), PreReleasePart::Numeric(b)) => a.cmp(b),
            (PreReleasePart::Numeric(_), PreReleasePart::Alpha(_)) => Ordering::Less,
            (PreReleasePart::Alpha(_), PreReleasePart::Numeric(_)) => Ordering::Greater,
            (PreReleasePart::Alpha(a), PreReleasePart::Alpha(b)) => a.cmp(b),
        }
    }
}

impl fmt::Display for PreReleasePart {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PreReleasePart::Numeric(n) => write!(f, "{}", n),
            PreReleasePart::Alpha(s) => write!(f, "{}", s),
        }
    }
}

impl Version {
    /// Creates a new version with the given major, minor, and patch numbers
    pub fn new(major: u64, minor: u64, patch: u64) -> Self {
        Self {
            major,
            minor,
            patch,
            pre_release: None,
            build: None,
        }
    }

    /// Creates a version with pre-release information
    pub fn with_pre_release(mut self, pre_release: &str) -> Result<Self, SemverError> {
        if pre_release.is_empty() {
            self.pre_release = None;
            return Ok(self);
        }
        
        let parts: Vec<PreReleasePart> = pre_release
            .split('.')
            .map(PreReleasePart::parse)
            .collect::<Result<Vec<_>, _>>()?;
        
        self.pre_release = Some(parts);
        Ok(self)
    }

    /// Creates a version with build metadata
    pub fn with_build(mut self, build: &str) -> Result<Self, SemverError> {
        if build.is_empty() {
            self.build = None;
            return Ok(self);
        }
        
        // Build metadata can contain ASCII alphanumerics, hyphens, and dots
        if !build.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '.') {
            return Err(SemverError::InvalidBuildMetadata);
        }
        
        self.build = Some(build.to_string());
        Ok(self)
    }

    /// Parses a version string
    /// 
    /// # Examples
    /// ```
    /// use semver_utils::Version;
    /// 
    /// let v = Version::parse("1.2.3")?;
    /// assert_eq!(v.major, 1);
    /// assert_eq!(v.minor, 2);
    /// assert_eq!(v.patch, 3);
    /// 
    /// let v = Version::parse("1.0.0-alpha.1+build.123")?;
    /// assert_eq!(v.pre_release, Some(vec![
    ///     semver_utils::PreReleasePart::Alpha("alpha".to_string()),
    ///     semver_utils::PreReleasePart::Numeric(1),
    /// ]));
    /// assert_eq!(v.build, Some("build.123".to_string()));
    /// # Ok::<(), semver_utils::SemverError>(())
    /// ```
    pub fn parse(s: &str) -> Result<Self, SemverError> {
        let s = s.trim();
        
        // Split build metadata
        let (version_part, build) = match s.split_once('+') {
            Some((v, b)) => (v, Some(b.to_string())),
            None => (s, None),
        };
        
        // Split pre-release
        let (core_part, pre_release) = match version_part.split_once('-') {
            Some((c, p)) => (c, Some(p.to_string())),
            None => (version_part, None),
        };
        
        // Parse core version (major.minor.patch)
        let parts: Vec<&str> = core_part.split('.').collect();
        if parts.len() != 3 {
            return Err(SemverError::InvalidFormat);
        }
        
        let major = parts[0].parse()
            .map_err(|_| SemverError::InvalidFormat)?;
        let minor = parts[1].parse()
            .map_err(|_| SemverError::InvalidFormat)?;
        let patch = parts[2].parse()
            .map_err(|_| SemverError::InvalidFormat)?;
        
        let mut version = Self::new(major, minor, patch);
        
        if let Some(pr) = pre_release {
            version = version.with_pre_release(&pr)?;
        }
        
        if let Some(b) = build {
            version = version.with_build(&b)?;
        }
        
        Ok(version)
    }

    /// Returns true if this is a pre-release version
    pub fn is_pre_release(&self) -> bool {
        self.pre_release.is_some()
    }

    /// Checks if this version is compatible with another version
    /// - Major version must match
    /// - This version's minor must be >= other's minor
    /// - If minors match, this version's patch must be >= other's patch
    pub fn is_compatible(&self, other: &Version) -> bool {
        if self.major != other.major {
            return false;
        }
        
        if self.minor < other.minor {
            return false;
        }
        
        if self.minor == other.minor && self.patch < other.patch {
            return false;
        }
        
        true
    }

    /// Returns the next major version
    pub fn next_major(&self) -> Version {
        Version::new(self.major + 1, 0, 0)
    }

    /// Returns the next minor version
    pub fn next_minor(&self) -> Version {
        Version::new(self.major, self.minor + 1, 0)
    }

    /// Returns the next patch version
    pub fn next_patch(&self) -> Version {
        Version::new(self.major, self.minor, self.patch + 1)
    }

    /// Bumps the major version in place
    pub fn bump_major(&mut self) {
        self.major += 1;
        self.minor = 0;
        self.patch = 0;
        self.pre_release = None;
        self.build = None;
    }

    /// Bumps the minor version in place
    pub fn bump_minor(&mut self) {
        self.minor += 1;
        self.patch = 0;
        self.pre_release = None;
        self.build = None;
    }

    /// Bumps the patch version in place
    pub fn bump_patch(&mut self) {
        self.patch += 1;
        self.pre_release = None;
        self.build = None;
    }

    /// Returns the base version without pre-release or build metadata
    pub fn base_version(&self) -> Version {
        Version::new(self.major, self.minor, self.patch)
    }

    /// Compares only the major version
    pub fn cmp_major(&self, other: &Version) -> Ordering {
        self.major.cmp(&other.major)
    }

    /// Compares only the minor version
    pub fn cmp_minor(&self, other: &Version) -> Ordering {
        self.minor.cmp(&other.minor)
    }

    /// Compares only the patch version
    pub fn cmp_patch(&self, other: &Version) -> Ordering {
        self.patch.cmp(&other.patch)
    }
}

impl PartialOrd for Version {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Version {
    fn cmp(&self, other: &Self) -> Ordering {
        // Compare major, minor, patch
        match self.major.cmp(&other.major) {
            Ordering::Equal => {}
            ord => return ord,
        }
        
        match self.minor.cmp(&other.minor) {
            Ordering::Equal => {}
            ord => return ord,
        }
        
        match self.patch.cmp(&other.patch) {
            Ordering::Equal => {}
            ord => return ord,
        }
        
        // Pre-release versions have lower precedence
        // A version without pre-release has higher precedence
        match (&self.pre_release, &other.pre_release) {
            (None, None) => Ordering::Equal,
            (None, Some(_)) => Ordering::Greater,
            (Some(_), None) => Ordering::Less,
            (Some(a), Some(b)) => {
                // Compare each part
                for (pa, pb) in a.iter().zip(b.iter()) {
                    match pa.cmp(pb) {
                        Ordering::Equal => continue,
                        ord => return ord,
                    }
                }
                // A longer pre-release has higher precedence
                a.len().cmp(&b.len())
            }
        }
    }
}

impl fmt::Display for Version {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)?;
        
        if let Some(ref pre) = self.pre_release {
            write!(f, "-")?;
            for (i, part) in pre.iter().enumerate() {
                if i > 0 {
                    write!(f, ".")?;
                }
                write!(f, "{}", part)?;
            }
        }
        
        if let Some(ref build) = self.build {
            write!(f, "+{}", build)?;
        }
        
        Ok(())
    }
}

impl FromStr for Version {
    type Err = SemverError;
    
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Version::parse(s)
    }
}

/// Comparison operators for version ranges
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Comparator {
    /// Exact match (=)
    Exact,
    /// Less than (<)
    Less,
    /// Less than or equal (<=)
    LessEqual,
    /// Greater than (>)
    Greater,
    /// Greater than or equal (>=)
    GreaterEqual,
    /// Compatible with (~>)
    Compatible,
}

impl Comparator {
    /// Parses a comparator string
    fn parse(s: &str) -> Result<Self, SemverError> {
        let s = s.trim();
        match s {
            "=" => Ok(Comparator::Exact),
            "<" => Ok(Comparator::Less),
            "<=" => Ok(Comparator::LessEqual),
            ">" => Ok(Comparator::Greater),
            ">=" => Ok(Comparator::GreaterEqual),
            "~>" => Ok(Comparator::Compatible),
            "" => Ok(Comparator::Exact), // Default to exact match
            _ => Err(SemverError::InvalidComparator),
        }
    }
}

impl fmt::Display for Comparator {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Comparator::Exact => write!(f, "="),
            Comparator::Less => write!(f, "<"),
            Comparator::LessEqual => write!(f, "<="),
            Comparator::Greater => write!(f, ">"),
            Comparator::GreaterEqual => write!(f, ">="),
            Comparator::Compatible => write!(f, "~>"),
        }
    }
}

/// A single version constraint
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Constraint {
    pub comparator: Comparator,
    pub version: Version,
}

impl Constraint {
    /// Creates a new constraint
    pub fn new(comparator: Comparator, version: Version) -> Self {
        Self { comparator, version }
    }

    /// Checks if a version satisfies this constraint
    pub fn satisfies(&self, version: &Version) -> bool {
        match self.comparator {
            Comparator::Exact => version == &self.version,
            Comparator::Less => version < &self.version,
            Comparator::LessEqual => version <= &self.version,
            Comparator::Greater => version > &self.version,
            Comparator::GreaterEqual => version >= &self.version,
            Comparator::Compatible => {
                // ~>=1.2.3 means >=1.2.3 <2.0.0
                // ~>=1.2 means >=1.2.0 <1.3.0
                version >= &self.version && version.major == self.version.major
            }
        }
    }

    /// Parses a constraint string
    fn parse(s: &str) -> Result<Self, SemverError> {
        let s = s.trim();
        
        // Try to find comparator
        let (comp_str, version_str) = if s.starts_with(">=") {
            (">=", &s[2..])
        } else if s.starts_with("<=") {
            ("<=", &s[2..])
        } else if s.starts_with("~>") {
            ("~>", &s[2..])
        } else if s.starts_with(">") {
            (">", &s[1..])
        } else if s.starts_with("<") {
            ("<", &s[1..])
        } else if s.starts_with("=") {
            ("=", &s[1..])
        } else {
            ("", s)
        };
        
        let comparator = Comparator::parse(comp_str)?;
        let version = Version::parse(version_str)?;
        
        Ok(Self { comparator, version })
    }
}

impl fmt::Display for Constraint {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}{}", self.comparator, self.version)
    }
}

/// A version range composed of multiple constraints
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VersionRange {
    constraints: Vec<Constraint>,
}

impl VersionRange {
    /// Creates an empty range
    pub fn empty() -> Self {
        Self { constraints: vec![] }
    }

    /// Creates a range from a single constraint
    pub fn from_constraint(constraint: Constraint) -> Self {
        Self { constraints: vec![constraint] }
    }

    /// Parses a version range string
    /// 
    /// # Examples
    /// ```
    /// use semver_utils::VersionRange;
    /// 
    /// // Exact version
    /// let range = VersionRange::parse("1.2.3")?;
    /// 
    /// // Comparison operators
    /// let range = VersionRange::parse(">=1.0.0")?;
    /// let range = VersionRange::parse("<2.0.0")?;
    /// 
    /// // Range with multiple constraints (space-separated)
    /// let range = VersionRange::parse(">=1.0.0 <2.0.0")?;
    /// 
    /// // Compatible versions
    /// let range = VersionRange::parse("~>1.2.0")?;
    /// # Ok::<(), semver_utils::SemverError>(())
    /// ```
    pub fn parse(s: &str) -> Result<Self, SemverError> {
        let s = s.trim();
        if s.is_empty() {
            return Ok(Self::empty());
        }
        
        let constraints = s
            .split_whitespace()
            .map(Constraint::parse)
            .collect::<Result<Vec<_>, _>>()?;
        
        Ok(Self { constraints })
    }

    /// Checks if a version satisfies all constraints in the range
    pub fn satisfies(&self, version: &Version) -> bool {
        self.constraints.iter().all(|c| c.satisfies(version))
    }

    /// Adds a constraint to the range
    pub fn add_constraint(&mut self, constraint: Constraint) {
        self.constraints.push(constraint);
    }

    /// Returns all constraints
    pub fn constraints(&self) -> &[Constraint] {
        &self.constraints
    }

    /// Checks if the range is empty (no constraints)
    pub fn is_empty(&self) -> bool {
        self.constraints.is_empty()
    }
}

impl fmt::Display for VersionRange {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for (i, c) in self.constraints.iter().enumerate() {
            if i > 0 {
                write!(f, " ")?;
            }
            write!(f, "{}", c)?;
        }
        Ok(())
    }
}

/// A set of version ranges (union of ranges)
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VersionSet {
    ranges: Vec<VersionRange>,
}

impl VersionSet {
    /// Creates an empty set
    pub fn empty() -> Self {
        Self { ranges: vec![] }
    }

    /// Creates a set with a single range
    pub fn from_range(range: VersionRange) -> Self {
        Self { ranges: vec![range] }
    }

    /// Parses a version set string (ranges separated by ||)
    /// 
    /// # Examples
    /// ```
    /// use semver_utils::VersionSet;
    /// 
    /// // Union of ranges
    /// let set = VersionSet::parse(">=1.0.0 <2.0.0 || >=3.0.0")?;
    /// 
    /// let v1 = semver_utils::Version::parse("1.5.0")?;
    /// let v2 = semver_utils::Version::parse("2.5.0")?;
    /// let v3 = semver_utils::Version::parse("3.5.0")?;
    /// 
    /// assert!(set.satisfies(&v1));
    /// assert!(!set.satisfies(&v2));
    /// assert!(set.satisfies(&v3));
    /// # Ok::<(), semver_utils::SemverError>(())
    /// ```
    pub fn parse(s: &str) -> Result<Self, SemverError> {
        let s = s.trim();
        if s.is_empty() {
            return Ok(Self::empty());
        }
        
        let ranges = s
            .split("||")
            .map(VersionRange::parse)
            .collect::<Result<Vec<_>, _>>()?;
        
        Ok(Self { ranges })
    }

    /// Checks if a version satisfies any range in the set
    pub fn satisfies(&self, version: &Version) -> bool {
        self.ranges.iter().any(|r| r.satisfies(version))
    }

    /// Adds a range to the set
    pub fn add_range(&mut self, range: VersionRange) {
        self.ranges.push(range);
    }

    /// Returns all ranges
    pub fn ranges(&self) -> &[VersionRange] {
        &self.ranges
    }

    /// Checks if the set is empty
    pub fn is_empty(&self) -> bool {
        self.ranges.is_empty()
    }
}

impl fmt::Display for VersionSet {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for (i, r) in self.ranges.iter().enumerate() {
            if i > 0 {
                write!(f, " || ")?;
            }
            write!(f, "{}", r)?;
        }
        Ok(())
    }
}

/// Errors that can occur when parsing or manipulating versions
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SemverError {
    /// Invalid version format
    InvalidFormat,
    /// Invalid pre-release identifier
    InvalidPreRelease,
    /// Invalid build metadata
    InvalidBuildMetadata,
    /// Invalid comparator
    InvalidComparator,
}

impl fmt::Display for SemverError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SemverError::InvalidFormat => write!(f, "Invalid version format"),
            SemverError::InvalidPreRelease => write!(f, "Invalid pre-release identifier"),
            SemverError::InvalidBuildMetadata => write!(f, "Invalid build metadata"),
            SemverError::InvalidComparator => write!(f, "Invalid comparator"),
        }
    }
}

impl std::error::Error for SemverError {}

// ==================== Tests ====================

#[cfg(test)]
mod tests {
    use super::*;

    mod version_parsing {
        use super::*;

        #[test]
        fn test_parse_simple() {
            let v = Version::parse("1.2.3").unwrap();
            assert_eq!(v.major, 1);
            assert_eq!(v.minor, 2);
            assert_eq!(v.patch, 3);
        }

        #[test]
        fn test_parse_with_pre_release() {
            let v = Version::parse("1.0.0-alpha").unwrap();
            assert_eq!(v.major, 1);
            assert!(v.is_pre_release());
            assert_eq!(v.pre_release, Some(vec![
                PreReleasePart::Alpha("alpha".to_string())
            ]));
        }

        #[test]
        fn test_parse_with_pre_release_numeric() {
            let v = Version::parse("1.0.0-alpha.1").unwrap();
            assert!(v.is_pre_release());
            assert_eq!(v.pre_release, Some(vec![
                PreReleasePart::Alpha("alpha".to_string()),
                PreReleasePart::Numeric(1),
            ]));
        }

        #[test]
        fn test_parse_with_build() {
            let v = Version::parse("1.0.0+build.123").unwrap();
            assert_eq!(v.build, Some("build.123".to_string()));
            assert!(!v.is_pre_release());
        }

        #[test]
        fn test_parse_full() {
            let v = Version::parse("1.2.3-beta.2+exp.sha.5114f85").unwrap();
            assert_eq!(v.major, 1);
            assert_eq!(v.minor, 2);
            assert_eq!(v.patch, 3);
            assert!(v.is_pre_release());
            assert_eq!(v.build, Some("exp.sha.5114f85".to_string()));
        }

        #[test]
        fn test_parse_invalid() {
            assert!(Version::parse("1.2").is_err());
            assert!(Version::parse("1.2.3.4").is_err());
            assert!(Version::parse("a.b.c").is_err());
            assert!(Version::parse("-1.2.3").is_err());
        }

        #[test]
        fn test_parse_with_whitespace() {
            let v = Version::parse("  1.2.3  ").unwrap();
            assert_eq!(v.major, 1);
        }
    }

    mod version_comparison {
        use super::*;

        #[test]
        fn test_compare_major() {
            let v1 = Version::new(1, 0, 0);
            let v2 = Version::new(2, 0, 0);
            assert!(v1 < v2);
        }

        #[test]
        fn test_compare_minor() {
            let v1 = Version::new(1, 0, 0);
            let v2 = Version::new(1, 1, 0);
            assert!(v1 < v2);
        }

        #[test]
        fn test_compare_patch() {
            let v1 = Version::new(1, 0, 0);
            let v2 = Version::new(1, 0, 1);
            assert!(v1 < v2);
        }

        #[test]
        fn test_equal_versions() {
            let v1 = Version::new(1, 2, 3);
            let v2 = Version::new(1, 2, 3);
            assert_eq!(v1, v2);
        }

        #[test]
        fn test_pre_release_lower() {
            let v1 = Version::parse("1.0.0-alpha").unwrap();
            let v2 = Version::parse("1.0.0").unwrap();
            assert!(v1 < v2);
        }

        #[test]
        fn test_pre_release_comparison() {
            let v1 = Version::parse("1.0.0-alpha").unwrap();
            let v2 = Version::parse("1.0.0-beta").unwrap();
            assert!(v1 < v2);
        }

        #[test]
        fn test_pre_release_numeric() {
            let v1 = Version::parse("1.0.0-alpha.1").unwrap();
            let v2 = Version::parse("1.0.0-alpha.2").unwrap();
            assert!(v1 < v2);
        }

        #[test]
        fn test_pre_release_numeric_vs_alpha() {
            let v1 = Version::parse("1.0.0-alpha.1").unwrap();
            let v2 = Version::parse("1.0.0-alpha.beta").unwrap();
            assert!(v1 < v2);
        }

        #[test]
        fn test_pre_release_length() {
            let v1 = Version::parse("1.0.0-alpha.1").unwrap();
            let v2 = Version::parse("1.0.0-alpha.1.1").unwrap();
            assert!(v1 < v2);
        }
    }

    mod version_operations {
        use super::*;

        #[test]
        fn test_next_major() {
            let v = Version::new(1, 2, 3);
            assert_eq!(v.next_major(), Version::new(2, 0, 0));
        }

        #[test]
        fn test_next_minor() {
            let v = Version::new(1, 2, 3);
            assert_eq!(v.next_minor(), Version::new(1, 3, 0));
        }

        #[test]
        fn test_next_patch() {
            let v = Version::new(1, 2, 3);
            assert_eq!(v.next_patch(), Version::new(1, 2, 4));
        }

        #[test]
        fn test_bump_major() {
            let mut v = Version::parse("1.2.3-alpha+build").unwrap();
            v.bump_major();
            assert_eq!(v, Version::new(2, 0, 0));
        }

        #[test]
        fn test_bump_minor() {
            let mut v = Version::parse("1.2.3-alpha+build").unwrap();
            v.bump_minor();
            assert_eq!(v, Version::new(1, 3, 0));
        }

        #[test]
        fn test_bump_patch() {
            let mut v = Version::parse("1.2.3-alpha+build").unwrap();
            v.bump_patch();
            assert_eq!(v, Version::new(1, 2, 4));
        }

        #[test]
        fn test_base_version() {
            let v = Version::parse("1.2.3-alpha+build").unwrap();
            assert_eq!(v.base_version(), Version::new(1, 2, 3));
        }
    }

    mod version_compatibility {
        use super::*;

        #[test]
        fn test_compatible_same() {
            let v1 = Version::new(1, 2, 3);
            let v2 = Version::new(1, 2, 3);
            assert!(v1.is_compatible(&v2));
        }

        #[test]
        fn test_compatible_higher_minor() {
            let v1 = Version::new(1, 3, 0);
            let v2 = Version::new(1, 2, 0);
            assert!(v1.is_compatible(&v2));
        }

        #[test]
        fn test_compatible_higher_patch() {
            let v1 = Version::new(1, 2, 5);
            let v2 = Version::new(1, 2, 3);
            assert!(v1.is_compatible(&v2));
        }

        #[test]
        fn test_not_compatible_different_major() {
            let v1 = Version::new(2, 0, 0);
            let v2 = Version::new(1, 0, 0);
            assert!(!v1.is_compatible(&v2));
        }

        #[test]
        fn test_not_compatible_lower_minor() {
            let v1 = Version::new(1, 1, 0);
            let v2 = Version::new(1, 2, 0);
            assert!(!v1.is_compatible(&v2));
        }
    }

    mod constraint_satisfaction {
        use super::*;

        #[test]
        fn test_exact_match() {
            let c = Constraint::new(Comparator::Exact, Version::new(1, 2, 3));
            assert!(c.satisfies(&Version::new(1, 2, 3)));
            assert!(!c.satisfies(&Version::new(1, 2, 4)));
        }

        #[test]
        fn test_greater_than() {
            let c = Constraint::new(Comparator::Greater, Version::new(1, 2, 3));
            assert!(!c.satisfies(&Version::new(1, 2, 3)));
            assert!(c.satisfies(&Version::new(1, 2, 4)));
            assert!(c.satisfies(&Version::new(2, 0, 0)));
        }

        #[test]
        fn test_greater_equal() {
            let c = Constraint::new(Comparator::GreaterEqual, Version::new(1, 2, 3));
            assert!(c.satisfies(&Version::new(1, 2, 3)));
            assert!(c.satisfies(&Version::new(1, 2, 4)));
            assert!(!c.satisfies(&Version::new(1, 2, 2)));
        }

        #[test]
        fn test_less_than() {
            let c = Constraint::new(Comparator::Less, Version::new(2, 0, 0));
            assert!(c.satisfies(&Version::new(1, 9, 9)));
            assert!(!c.satisfies(&Version::new(2, 0, 0)));
        }

        #[test]
        fn test_less_equal() {
            let c = Constraint::new(Comparator::LessEqual, Version::new(2, 0, 0));
            assert!(c.satisfies(&Version::new(1, 9, 9)));
            assert!(c.satisfies(&Version::new(2, 0, 0)));
            assert!(!c.satisfies(&Version::new(2, 0, 1)));
        }

        #[test]
        fn test_compatible() {
            let c = Constraint::new(Comparator::Compatible, Version::new(1, 2, 0));
            assert!(c.satisfies(&Version::new(1, 2, 0)));
            assert!(c.satisfies(&Version::new(1, 3, 0)));
            assert!(c.satisfies(&Version::new(1, 9, 9)));
            assert!(!c.satisfies(&Version::new(2, 0, 0)));
            assert!(!c.satisfies(&Version::new(1, 1, 9)));
        }
    }

    mod version_range {
        use super::*;

        #[test]
        fn test_range_exact() {
            let range = VersionRange::parse("1.2.3").unwrap();
            assert!(range.satisfies(&Version::new(1, 2, 3)));
            assert!(!range.satisfies(&Version::new(1, 2, 4)));
        }

        #[test]
        fn test_range_greater_equal() {
            let range = VersionRange::parse(">=1.0.0").unwrap();
            assert!(range.satisfies(&Version::new(1, 0, 0)));
            assert!(range.satisfies(&Version::new(2, 0, 0)));
            assert!(!range.satisfies(&Version::new(0, 9, 9)));
        }

        #[test]
        fn test_range_combined() {
            let range = VersionRange::parse(">=1.0.0 <2.0.0").unwrap();
            assert!(range.satisfies(&Version::new(1, 0, 0)));
            assert!(range.satisfies(&Version::new(1, 9, 9)));
            assert!(!range.satisfies(&Version::new(2, 0, 0)));
            assert!(!range.satisfies(&Version::new(0, 9, 9)));
        }

        #[test]
        fn test_range_carrot() {
            let range = VersionRange::parse("~>1.2.3").unwrap();
            assert!(range.satisfies(&Version::new(1, 2, 3)));
            assert!(range.satisfies(&Version::new(1, 9, 9)));
            assert!(!range.satisfies(&Version::new(2, 0, 0)));
            assert!(!range.satisfies(&Version::new(1, 2, 2)));
        }

        #[test]
        fn test_range_empty() {
            let range = VersionRange::parse("").unwrap();
            assert!(range.is_empty());
            assert!(range.satisfies(&Version::new(1, 0, 0)));
        }
    }

    mod version_set {
        use super::*;

        #[test]
        fn test_set_single_range() {
            let set = VersionSet::parse(">=1.0.0 <2.0.0").unwrap();
            assert!(set.satisfies(&Version::new(1, 5, 0)));
            assert!(!set.satisfies(&Version::new(2, 0, 0)));
        }

        #[test]
        fn test_set_union() {
            let set = VersionSet::parse(">=1.0.0 <2.0.0 || >=3.0.0").unwrap();
            assert!(set.satisfies(&Version::new(1, 5, 0)));
            assert!(!set.satisfies(&Version::new(2, 5, 0)));
            assert!(set.satisfies(&Version::new(3, 0, 0)));
        }

        #[test]
        fn test_set_empty() {
            let set = VersionSet::parse("").unwrap();
            assert!(set.is_empty());
        }
    }

    mod display {
        use super::*;

        #[test]
        fn test_display_version() {
            let v = Version::new(1, 2, 3);
            assert_eq!(format!("{}", v), "1.2.3");
        }

        #[test]
        fn test_display_version_with_pre_release() {
            let v = Version::parse("1.0.0-alpha.1").unwrap();
            assert_eq!(format!("{}", v), "1.0.0-alpha.1");
        }

        #[test]
        fn test_display_version_with_build() {
            let v = Version::parse("1.0.0+build.123").unwrap();
            assert_eq!(format!("{}", v), "1.0.0+build.123");
        }

        #[test]
        fn test_display_version_full() {
            let v = Version::parse("1.0.0-alpha.1+build.123").unwrap();
            assert_eq!(format!("{}", v), "1.0.0-alpha.1+build.123");
        }

        #[test]
        fn test_display_constraint() {
            let c = Constraint::new(Comparator::GreaterEqual, Version::new(1, 0, 0));
            assert_eq!(format!("{}", c), ">=1.0.0");
        }

        #[test]
        fn test_display_range() {
            let range = VersionRange::parse(">=1.0.0 <2.0.0").unwrap();
            assert_eq!(format!("{}", range), ">=1.0.0 <2.0.0");
        }

        #[test]
        fn test_display_set() {
            let set = VersionSet::parse(">=1.0.0 <2.0.0 || >=3.0.0").unwrap();
            assert_eq!(format!("{}", set), ">=1.0.0 <2.0.0 || >=3.0.0");
        }
    }

    mod from_str {
        use super::*;

        #[test]
        fn test_version_from_str() {
            let v: Version = "1.2.3".parse().unwrap();
            assert_eq!(v, Version::new(1, 2, 3));
        }

        #[test]
        fn test_version_from_str_invalid() {
            let result: Result<Version, _> = "invalid".parse();
            assert!(result.is_err());
        }
    }

    mod edge_cases {
        use super::*;

        #[test]
        fn test_large_version_numbers() {
            let v = Version::new(u64::MAX, u64::MAX, u64::MAX);
            assert_eq!(v.major, u64::MAX);
        }

        #[test]
        fn test_zero_version() {
            let v = Version::new(0, 0, 0);
            assert_eq!(v.major, 0);
            assert_eq!(v.minor, 0);
            assert_eq!(v.patch, 0);
        }

        #[test]
        fn test_pre_release_with_hyphen() {
            let v = Version::parse("1.0.0-alpha-beta").unwrap();
            assert!(v.is_pre_release());
        }

        #[test]
        fn test_build_with_hyphen() {
            let v = Version::parse("1.0.0+build-123").unwrap();
            assert_eq!(v.build, Some("build-123".to_string()));
        }

        #[test]
        fn test_multiple_constraints() {
            let mut range = VersionRange::empty();
            range.add_constraint(Constraint::new(Comparator::GreaterEqual, Version::new(1, 0, 0)));
            range.add_constraint(Constraint::new(Comparator::Less, Version::new(2, 0, 0)));
            
            assert!(range.satisfies(&Version::new(1, 5, 0)));
            assert!(!range.satisfies(&Version::new(2, 0, 0)));
        }
    }
}