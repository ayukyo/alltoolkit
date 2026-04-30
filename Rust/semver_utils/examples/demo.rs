//! Semver Utils Examples
//!
//! Run with: cargo run --example demo

use semver_utils::{Version, VersionRange, VersionSet, Constraint, Comparator};

fn main() {
    println!("=== Semantic Versioning Utils Demo ===\n");

    // Basic version parsing
    println!("--- Version Parsing ---");
    let v1 = Version::parse("1.2.3").unwrap();
    println!("Simple version: {}", v1);
    println!("  Major: {}, Minor: {}, Patch: {}", v1.major, v1.minor, v1.patch);

    let v2 = Version::parse("2.0.0-alpha.1+build.123").unwrap();
    println!("Complex version: {}", v2);
    println!("  Is pre-release: {}", v2.is_pre_release());
    println!("  Build metadata: {:?}", v2.build);

    // Version comparison
    println!("\n--- Version Comparison ---");
    let v100 = Version::new(1, 0, 0);
    let v110 = Version::new(1, 1, 0);
    let v200 = Version::new(2, 0, 0);

    println!("{} < {} ? {}", v100, v110, v100 < v110);
    println!("{} < {} ? {}", v110, v200, v110 < v200);
    println!("{} == {} ? {}", v100, v100, v100 == v100);

    // Pre-release ordering
    println!("\n--- Pre-release Ordering ---");
    let alpha = Version::parse("1.0.0-alpha").unwrap();
    let beta = Version::parse("1.0.0-beta").unwrap();
    let rc = Version::parse("1.0.0-rc.1").unwrap();
    let release = Version::parse("1.0.0").unwrap();

    println!("Ordering: {} < {} < {} < {}", alpha, beta, rc, release);
    println!("  alpha < beta ? {}", alpha < beta);
    println!("  beta < rc.1 ? {}", beta < rc);
    println!("  rc.1 < release ? {}", rc < release);

    // Version operations
    println!("\n--- Version Operations ---");
    let v = Version::new(1, 2, 3);
    println!("Original: {}", v);
    println!("Next major: {}", v.next_major());
    println!("Next minor: {}", v.next_minor());
    println!("Next patch: {}", v.next_patch());

    // Version compatibility
    println!("\n--- Version Compatibility ---");
    let v12x = Version::new(1, 2, 5);
    let v120 = Version::new(1, 2, 0);
    let v130 = Version::new(1, 3, 0);
    let v200 = Version::new(2, 0, 0);

    println!("Is {} compatible with {} ? {}", v12x, v120, v12x.is_compatible(&v120));
    println!("Is {} compatible with {} ? {}", v12x, v130, v12x.is_compatible(&v130));
    println!("Is {} compatible with {} ? {}", v12x, v200, v12x.is_compatible(&v200));

    // Version range
    println!("\n--- Version Range ---");
    let range = VersionRange::parse(">=1.0.0 <2.0.0").unwrap();
    println!("Range: {}", range);
    println!("  {} satisfies ? {}", v100, range.satisfies(&v100));
    println!("  {} satisfies ? {}", v110, range.satisfies(&v110));
    println!("  {} satisfies ? {}", v200, range.satisfies(&v200));

    // Compatible constraint (~>)
    println!("\n--- Compatible Constraint (~>) ---");
    let compat_range = VersionRange::parse("~>1.2.0").unwrap();
    println!("Range: {}", compat_range);
    let v120_test = Version::new(1, 2, 0);
    let v125 = Version::new(1, 2, 5);
    let v130_test = Version::new(1, 3, 0);
    let v190 = Version::new(1, 9, 0);
    println!("  {} satisfies ? {}", v120_test, compat_range.satisfies(&v120_test));
    println!("  {} satisfies ? {}", v125, compat_range.satisfies(&v125));
    println!("  {} satisfies ? {}", v130_test, compat_range.satisfies(&v130_test));
    println!("  {} satisfies ? {}", v190, compat_range.satisfies(&v190));
    println!("  {} satisfies ? {}", v200, compat_range.satisfies(&v200));

    // Version set (union of ranges)
    println!("\n--- Version Set (Union) ---");
    let set = VersionSet::parse(">=1.0.0 <2.0.0 || >=3.0.0 <4.0.0").unwrap();
    println!("Set: {}", set);
    let v150 = Version::new(1, 5, 0);
    let v250 = Version::new(2, 5, 0);
    let v350 = Version::new(3, 5, 0);
    println!("  {} satisfies ? {}", v150, set.satisfies(&v150));
    println!("  {} satisfies ? {}", v250, set.satisfies(&v250));
    println!("  {} satisfies ? {}", v350, set.satisfies(&v350));

    // Manual constraint building
    println!("\n--- Manual Constraint Building ---");
    let mut range = VersionRange::empty();
    range.add_constraint(Constraint::new(Comparator::GreaterEqual, Version::new(1, 0, 0)));
    range.add_constraint(Constraint::new(Comparator::Less, Version::new(1, 5, 0)));
    println!("Built range: {}", range);
    println!("  {} satisfies ? {}", v100, range.satisfies(&v100));
    println!("  {} satisfies ? {}", v130_test, range.satisfies(&v130_test));
    println!("  {} satisfies ? {}", v200, range.satisfies(&v200));

    println!("\n=== Demo Complete ===");
}