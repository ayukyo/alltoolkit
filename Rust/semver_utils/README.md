# Semver Utils

A comprehensive semantic versioning library for Rust with zero external dependencies.

## Features

- ✅ Parse semver strings (major.minor.patch with optional pre-release and build metadata)
- ✅ Compare versions with all comparison operators
- ✅ Check version compatibility (major, minor, patch)
- ✅ Parse and evaluate version ranges
- ✅ Version set support (union of ranges with `||`)
- ✅ Zero external dependencies

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
semver_utils = { path = "./semver_utils" }
```

## Quick Start

### Parsing Versions

```rust
use semver_utils::Version;

let v = Version::parse("1.2.3-alpha.1+build.123")?;
assert_eq!(v.major, 1);
assert_eq!(v.minor, 2);
assert_eq!(v.patch, 3);
assert!(v.is_pre_release());
assert_eq!(v.build, Some("build.123".to_string()));
```

### Comparing Versions

```rust
use semver_utils::Version;

let v1 = Version::new(1, 0, 0);
let v2 = Version::new(2, 0, 0);

assert!(v1 < v2);
assert!(v1.is_compatible(&Version::new(1, 0, 5)));
assert!(!v1.is_compatible(&Version::new(2, 0, 0)));
```

### Pre-release Ordering

```rust
use semver_utils::Version;

let alpha = Version::parse("1.0.0-alpha")?;
let beta = Version::parse("1.0.0-beta")?;
let release = Version::parse("1.0.0")?;

assert!(alpha < beta);
assert!(beta < release);
```

### Version Operations

```rust
use semver_utils::Version;

let v = Version::new(1, 2, 3);

assert_eq!(v.next_major(), Version::new(2, 0, 0));
assert_eq!(v.next_minor(), Version::new(1, 3, 0));
assert_eq!(v.next_patch(), Version::new(1, 2, 4));

let mut v2 = Version::new(1, 2, 3);
v2.bump_minor();
assert_eq!(v2, Version::new(1, 3, 0));
```

### Version Ranges

```rust
use semver_utils::{Version, VersionRange};

let range = VersionRange::parse(">=1.0.0 <2.0.0")?;

assert!(range.satisfies(&Version::new(1, 0, 0)));
assert!(range.satisfies(&Version::new(1, 9, 9)));
assert!(!range.satisfies(&Version::new(2, 0, 0)));
```

### Version Sets (Union of Ranges)

```rust
use semver_utils::{Version, VersionSet};

let set = VersionSet::parse(">=1.0.0 <2.0.0 || >=3.0.0")?;

assert!(set.satisfies(&Version::new(1, 5, 0)));
assert!(!set.satisfies(&Version::new(2, 5, 0)));
assert!(set.satisfies(&Version::new(3, 0, 0)));
```

### Manual Constraint Building

```rust
use semver_utils::{Version, VersionRange, Constraint, Comparator};

let mut range = VersionRange::empty();
range.add_constraint(Constraint::new(Comparator::GreaterEqual, Version::new(1, 0, 0)));
range.add_constraint(Constraint::new(Comparator::Less, Version::new(2, 0, 0)));

assert!(range.satisfies(&Version::new(1, 5, 0)));
```

## API Reference

### Version

- `Version::new(major, minor, patch)` - Create a new version
- `Version::parse(s)` - Parse a version string
- `is_pre_release()` - Check if version has pre-release tag
- `is_compatible(other)` - Check compatibility with another version
- `next_major()` / `next_minor()` / `next_patch()` - Get next version
- `bump_major()` / `bump_minor()` / `bump_patch()` - Bump version in place
- `base_version()` - Get version without pre-release or build

### VersionRange

- `VersionRange::parse(s)` - Parse a range string
- `satisfies(version)` - Check if version satisfies all constraints
- `add_constraint(constraint)` - Add a constraint

### VersionSet

- `VersionSet::parse(s)` - Parse a set string (ranges separated by `||`)
- `satisfies(version)` - Check if version satisfies any range

### Comparator

- `Exact` (`=`) - Exact match
- `Less` (`<`) - Less than
- `LessEqual` (`<=`) - Less than or equal
- `Greater` (`>`) - Greater than
- `GreaterEqual` (`>=`) - Greater than or equal
- `Compatible` (`~>`) - Compatible (same major, higher or equal minor.patch)

## License

MIT