# SemVer Utils

A comprehensive semantic versioning (SemVer) utility library for Zig. Parse, compare, validate, and manipulate semantic version strings according to [SemVer 2.0.0](https://semver.org/).

## Features

- **Parse** semantic version strings with full support for prerelease and build metadata
- **Compare** versions with proper precedence rules
- **Validate** version strings
- **Increment** major, minor, or patch versions
- **Constraints** with support for `=`, `>`, `>=`, `<`, `<=`, `^` (caret), and `~` (tilde)
- **Find** minimum/maximum version from a list
- **Zero external dependencies** - pure Zig implementation

## Installation

### Using Zig Package Manager

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .semver_utils = .{
        .url = "https://github.com/ayukyo/alltoolkit/archive/refs/heads/main.tar.gz",
        .hash = "...",
    },
},
```

### Manual

Copy `src/main.zig` to your project.

## Quick Start

```zig
const std = @import("std");
const semver = @import("semver_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // Parse a version
    var ver = try semver.SemVer.parse(allocator, "1.2.3-alpha.1+build.456");
    defer ver.deinit();

    std.debug.print("{}.{}.{}\n", .{ ver.major, ver.minor, ver.patch });
    // Output: 1.2.3
}
```

## API Reference

### SemVer

The main semantic version struct.

#### Parse

```zig
var ver = try SemVer.parse(allocator, "1.2.3-alpha.1+build.456");
defer ver.deinit();
```

Supports all SemVer 2.0.0 formats:
- `1.0.0` - Basic version
- `1.0.0-alpha` - Prerelease version
- `1.0.0-alpha.1` - Prerelease with numeric identifier
- `1.0.0+build.123` - Version with build metadata
- `1.0.0-alpha.1+exp.sha.5114f85` - Full format

#### Compare

```zig
const result = ver1.compare(ver2);
// Returns: -1 if ver1 < ver2, 0 if equal, 1 if ver1 > ver2
```

#### Format

```zig
const str = try ver.format(allocator);
defer allocator.free(str);
// Returns: "1.2.3-alpha.1+build.456"
```

### Version Constraints

```zig
// Parse a constraint
var constraint = try VersionConstraint.parse(allocator, "^1.2.3");
defer constraint.deinit();

// Check if a version satisfies the constraint
const satisfies = version.satisfies(constraint);
```

#### Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Exact match | `=1.2.3` |
| `>` | Greater than | `>1.2.3` |
| `>=` | Greater than or equal | `>=1.2.3` |
| `<` | Less than | `<1.2.3` |
| `<=` | Less than or equal | `<=1.2.3` |
| `^` | Caret (compatible with) | `^1.2.3` |
| `~` | Tilde (approximately) | `~1.2.3` |

#### Caret (`^`) Semantics

- `^1.2.3` := `>=1.2.3 <2.0.0`
- `^0.2.3` := `>=0.2.3 <0.3.0`
- `^0.0.3` := `>=0.0.3 <0.0.4`

#### Tilde (`~`) Semantics

- `~1.2.3` := `>=1.2.3 <1.3.0`

### Utility Functions

#### isValid

Check if a string is a valid semantic version:

```zig
const valid = semver.isValid("1.2.3"); // true
const invalid = semver.isValid("1.2"); // false
```

#### compare

Compare two version strings:

```zig
const result = try semver.compare(allocator, "1.0.0", "2.0.0");
// Returns: -1 (1.0.0 < 2.0.0)
```

#### max/min

Find the highest/lowest version from a list:

```zig
const versions = [_][]const u8{ "1.0.0", "2.0.0", "1.5.0" };
const highest = try semver.max(allocator, &versions); // "2.0.0"
const lowest = try semver.min(allocator, &versions);   // "1.0.0"
```

#### increment

Increment a version:

```zig
var ver = try SemVer.parse(allocator, "1.2.3");

var major = try semver.increment(allocator, ver, .major); // 2.0.0
var minor = try semver.increment(allocator, ver, .minor); // 1.3.0
var patch = try semver.increment(allocator, ver, .patch); // 1.2.4
```

## Examples

### Basic Usage

```bash
zig build run-basic
```

Demonstrates:
- Parsing versions
- Comparing versions
- Incrementing versions
- Finding max/min
- Validation

### Advanced Usage

```bash
zig build run-advanced
```

Demonstrates:
- Caret and tilde constraints
- Comparison operators
- Prerelease ordering
- Package version selection
- Edge cases (0.x versions)

## Testing

Run the unit tests:

```bash
zig build test
```

## SemVer 2.0.0 Compliance

This library follows the [SemVer 2.0.0 specification](https://semver.org/):

1. Version format: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
2. Precedence rules:
   - Major > Minor > Patch
   - No prerelease > Has prerelease
   - Numeric identifiers compared as integers
   - Non-numeric identifiers compared lexicographically
   - Numeric < Non-numeric

## License

MIT License - Part of [AllToolkit](https://github.com/ayukyo/alltoolkit)