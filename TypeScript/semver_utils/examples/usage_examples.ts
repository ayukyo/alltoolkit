/**
 * Usage Examples for SemVer Utilities Module
 * 
 * This file demonstrates all features of the semver_utils module.
 */

import SemverUtils, {
  parse,
  isValid,
  stringify,
  compare,
  gt,
  gte,
  lt,
  lte,
  eq,
  neq,
  max,
  min,
  sort,
  rsort,
  inc,
  incMajor,
  incMinor,
  incPatch,
  diff,
  isStable,
  base,
  parseRange,
  satisfies,
  maxSatisfying,
  minSatisfying,
  coerce,
} from '../mod';

console.log('='.repeat(60));
console.log('SemVer Utilities - Usage Examples');
console.log('='.repeat(60));

// ==================== 1. Parsing Semantic Versions ====================

console.log('\n📦 1. Parsing Semantic Versions');
console.log('-'.repeat(40));

// Parse basic version
const v1 = parse('1.2.3');
console.log('parse("1.2.3"):', v1);
// { major: 1, minor: 2, patch: 3, prerelease: [], build: [], raw: '1.2.3' }

// Parse with 'v' prefix
const v2 = parse('v2.0.0');
console.log('parse("v2.0.0"):', v2);

// Parse with prerelease
const v3 = parse('1.0.0-alpha.1');
console.log('parse("1.0.0-alpha.1"):', v3);

// Parse with build metadata
const v4 = parse('1.0.0+build.123');
console.log('parse("1.0.0+build.123"):', v4);

// Parse full version
const v5 = parse('2.1.3-beta.2+exp.sha.5114f85');
console.log('parse("2.1.3-beta.2+exp.sha.5114f85"):', v5);

// ==================== 2. Validation ====================

console.log('\n✅ 2. Validation');
console.log('-'.repeat(40));

console.log('isValid("1.2.3"):', isValid('1.2.3')); // true
console.log('isValid("v1.2.3"):', isValid('v1.2.3')); // true
console.log('isValid("1.2.3-alpha"):', isValid('1.2.3-alpha')); // true
console.log('isValid("1.2"):', isValid('1.2')); // false
console.log('isValid("invalid"):', isValid('invalid')); // false

// ==================== 3. Stringify ====================

console.log('\n📝 3. Stringify');
console.log('-'.repeat(40));

const v = parse('1.2.3-alpha.1+build.123');
if (v) {
  console.log('stringify(parsed):', stringify(v)); // "1.2.3-alpha.1+build.123"
}

// ==================== 4. Comparison ====================

console.log('\n⚖️  4. Comparison');
console.log('-'.repeat(40));

// Basic comparison
console.log('compare("1.2.3", "1.2.4"):', compare('1.2.3', '1.2.4')); // -1
console.log('compare("1.2.3", "1.2.3"):', compare('1.2.3', '1.2.3')); // 0
console.log('compare("2.0.0", "1.9.9"):', compare('2.0.0', '1.9.9')); // 1

// Comparison operators
console.log('gt("2.0.0", "1.0.0"):', gt('2.0.0', '1.0.0')); // true
console.log('lt("1.0.0", "2.0.0"):', lt('1.0.0', '2.0.0')); // true
console.log('gte("1.5.0", "1.5.0"):', gte('1.5.0', '1.5.0')); // true
console.log('lte("1.4.9", "1.5.0"):', lte('1.4.9', '1.5.0')); // true
console.log('eq("1.2.3", "1.2.3"):', eq('1.2.3', '1.2.3')); // true
console.log('neq("1.2.3", "1.2.4"):', neq('1.2.3', '1.2.4')); // true

// Prerelease comparison
console.log('\nPrerelease comparison:');
console.log('compare("1.0.0-alpha", "1.0.0-beta"):', compare('1.0.0-alpha', '1.0.0-beta')); // -1
console.log('compare("1.0.0-alpha.1", "1.0.0-alpha.2"):', compare('1.0.0-alpha.1', '1.0.0-alpha.2')); // -1
console.log('compare("1.0.0-alpha", "1.0.0"):', compare('1.0.0-alpha', '1.0.0')); // -1 (prerelease < release)

// ==================== 5. Max/Min ====================

console.log('\n📈 5. Max/Min');
console.log('-'.repeat(40));

const maxVer = max('1.2.3', '2.0.0');
console.log('max("1.2.3", "2.0.0"):', maxVer ? stringify(maxVer) : null); // "2.0.0"

const minVer = min('1.2.3', '2.0.0');
console.log('min("1.2.3", "2.0.0"):', minVer ? stringify(minVer) : null); // "1.2.3"

// ==================== 6. Sorting ====================

console.log('\n📊 6. Sorting');
console.log('-'.repeat(40));

const versions = ['2.0.0', '1.0.0', '1.5.0', '1.0.5', '0.9.0', '1.5.3'];
console.log('Original:', versions);

const sorted = sort(versions);
console.log('Sorted (asc):', sorted.map(stringify));

const rsorted = rsort(versions);
console.log('Sorted (desc):', rsorted.map(stringify));

// ==================== 7. Incrementing Versions ====================

console.log('\n➕ 7. Incrementing Versions');
console.log('-'.repeat(40));

const baseVersion = '1.2.3';
console.log('Base version:', baseVersion);

const majorInc = incMajor(baseVersion);
console.log('incMajor:', majorInc ? stringify(majorInc) : null); // "2.0.0"

const minorInc = incMinor(baseVersion);
console.log('incMinor:', minorInc ? stringify(minorInc) : null); // "1.3.0"

const patchInc = incPatch(baseVersion);
console.log('incPatch:', patchInc ? stringify(patchInc) : null); // "1.2.4"

// Using inc function
console.log('inc(version, "major"):', inc(baseVersion, 'major') ? stringify(inc(baseVersion, 'major')!) : null);
console.log('inc(version, "minor"):', inc(baseVersion, 'minor') ? stringify(inc(baseVersion, 'minor')!) : null);
console.log('inc(version, "patch"):', inc(baseVersion, 'patch') ? stringify(inc(baseVersion, 'patch')!) : null);

// ==================== 8. Version Difference ====================

console.log('\n🔍 8. Version Difference');
console.log('-'.repeat(40));

console.log('diff("1.0.0", "2.0.0"):', diff('1.0.0', '2.0.0')); // "major"
console.log('diff("1.0.0", "1.1.0"):', diff('1.0.0', '1.1.0')); // "minor"
console.log('diff("1.0.0", "1.0.1"):', diff('1.0.0', '1.0.1')); // "patch"
console.log('diff("1.0.0", "1.0.0"):', diff('1.0.0', '1.0.0')); // null

// ==================== 9. Stability Check ====================

console.log('\n🔒 9. Stability Check');
console.log('-'.repeat(40));

console.log('isStable("1.0.0"):', isStable('1.0.0')); // true
console.log('isStable("1.0.0-alpha"):', isStable('1.0.0-alpha')); // false
console.log('isStable("1.0.0-beta.1"):', isStable('1.0.0-beta.1')); // false
console.log('isStable("1.0.0-rc.1"):', isStable('1.0.0-rc.1')); // false

// Get base version (without prerelease/build)
console.log('base("1.2.3-alpha.1+build"):', base('1.2.3-alpha.1+build')); // "1.2.3"

// ==================== 10. Version Ranges ====================

console.log('\n📐 10. Version Ranges');
console.log('-'.repeat(40));

// Parse ranges
console.log('Parsed ^1.2.3:', JSON.stringify(parseRange('^1.2.3'), null, 2));
console.log('Parsed ~1.2.3:', JSON.stringify(parseRange('~1.2.3'), null, 2));
console.log('Parsed >=1.0.0 <2.0.0:', JSON.stringify(parseRange('>=1.0.0 <2.0.0'), null, 2));
console.log('Parsed 1.0.0 - 2.0.0:', JSON.stringify(parseRange('1.0.0 - 2.0.0'), null, 2));
console.log('Parsed 1.0.0 || 2.0.0:', JSON.stringify(parseRange('1.0.0 || 2.0.0'), null, 2));

// ==================== 11. Satisfies ====================

console.log('\n✓ 11. Satisfies');
console.log('-'.repeat(40));

// Caret range
console.log('satisfies("1.2.3", "^1.2.3"):', satisfies('1.2.3', '^1.2.3')); // true
console.log('satisfies("1.9.9", "^1.2.3"):', satisfies('1.9.9', '^1.2.3')); // true
console.log('satisfies("2.0.0", "^1.2.3"):', satisfies('2.0.0', '^1.2.3')); // false

// Tilde range
console.log('satisfies("1.2.5", "~1.2.3"):', satisfies('1.2.5', '~1.2.3')); // true
console.log('satisfies("1.3.0", "~1.2.3"):', satisfies('1.3.0', '~1.2.3')); // false

// Comparison operators
console.log('satisfies("1.5.0", ">1.0.0"):', satisfies('1.5.0', '>1.0.0')); // true
console.log('satisfies("0.5.0", "<1.0.0"):', satisfies('0.5.0', '<1.0.0')); // true
console.log('satisfies("1.5.0", ">=1.0.0 <2.0.0"):', satisfies('1.5.0', '>=1.0.0 <2.0.0')); // true

// OR
console.log('satisfies("1.0.0", "1.0.0 || 2.0.0"):', satisfies('1.0.0', '1.0.0 || 2.0.0')); // true
console.log('satisfies("3.0.0", "1.0.0 || 2.0.0"):', satisfies('3.0.0', '1.0.0 || 2.0.0')); // false

// Hyphen range
console.log('satisfies("1.5.0", "1.0.0 - 2.0.0"):', satisfies('1.5.0', '1.0.0 - 2.0.0')); // true

// Wildcards
console.log('satisfies("1.5.0", "*"):', satisfies('1.5.0', '*')); // true
console.log('satisfies("1.5.0", "1.x"):', satisfies('1.5.0', '1.x')); // true
console.log('satisfies("2.5.0", "1.x"):', satisfies('2.5.0', '1.x')); // false
console.log('satisfies("1.2.5", "1.2.x"):', satisfies('1.2.5', '1.2.x')); // true

// Special cases for 0.x versions
console.log('\nSpecial cases for 0.x:');
console.log('satisfies("0.0.3", "^0.0.3"):', satisfies('0.0.3', '^0.0.3')); // true
console.log('satisfies("0.0.4", "^0.0.3"):', satisfies('0.0.4', '^0.0.3')); // false
console.log('satisfies("0.2.5", "^0.2.3"):', satisfies('0.2.5', '^0.2.3')); // true
console.log('satisfies("0.3.0", "^0.2.3"):', satisfies('0.3.0', '^0.2.3')); // false

// ==================== 12. Max/Min Satisfying ====================

console.log('\n🎯 12. Max/Min Satisfying');
console.log('-'.repeat(40));

const availableVersions = ['1.0.0', '1.2.3', '1.5.0', '2.0.0', '2.1.0', '3.0.0'];
console.log('Available versions:', availableVersions);

const maxSat = maxSatisfying(availableVersions, '>=1.0.0 <2.0.0');
console.log('maxSatisfying(">=1.0.0 <2.0.0"):', maxSat ? stringify(maxSat) : null); // "1.5.0"

const minSat = minSatisfying(availableVersions, '>=1.0.0 <2.0.0');
console.log('minSatisfying(">=1.0.0 <2.0.0"):', minSat ? stringify(minSat) : null); // "1.0.0"

// Finding latest version in a range
const latestV1 = maxSatisfying(availableVersions, '^1.0.0');
console.log('Latest v1.x:', latestV1 ? stringify(latestV1) : null); // "1.5.0"

// Finding oldest version in a range
const oldestV2 = minSatisfying(availableVersions, '>=2.0.0');
console.log('Oldest v2+:', oldestV2 ? stringify(oldestV2) : null); // "2.0.0"

// ==================== 13. Coerce ====================

console.log('\n🔧 13. Coerce (Extract Version)');
console.log('-'.repeat(40));

console.log('coerce("v1.2.3"):', coerce('v1.2.3')); // { major: 1, minor: 2, patch: 3, ... }
console.log('coerce("version 1.2"):', coerce('version 1.2')); // { major: 1, minor: 2, patch: 0, ... }
console.log('coerce("1"):', coerce('1')); // { major: 1, minor: 0, patch: 0, ... }
console.log('coerce("no version"):', coerce('no version')); // null

// ==================== 14. Real-World Use Cases ====================

console.log('\n🌐 14. Real-World Use Cases');
console.log('-'.repeat(40));

// Package version management
const packageVersions = [
  '1.0.0-alpha',
  '1.0.0-alpha.1',
  '1.0.0-beta',
  '1.0.0-beta.2',
  '1.0.0-rc.1',
  '1.0.0',
  '1.0.1',
  '1.1.0',
  '2.0.0',
];

console.log('All versions:', packageVersions);

// Find all stable versions
const stableVersions = packageVersions.filter(isStable);
console.log('Stable versions:', stableVersions);

// Find the latest stable version
const latestStable = max(stableVersions.map(parse).filter((v): v is NonNullable<typeof v> => v !== null));
console.log('Latest stable:', latestStable ? stringify(latestStable) : null);

// Find versions compatible with ^1.0.0
const compatible = packageVersions.filter(v => satisfies(v, '^1.0.0'));
console.log('Compatible with ^1.0.0:', compatible);

// Sort all versions
const sortedVersions = sort(packageVersions);
console.log('Sorted versions:', sortedVersions.map(stringify));

// Check if a feature is available (version >= required)
function isFeatureAvailable(currentVersion: string, requiredVersion: string): boolean {
  return gte(currentVersion, requiredVersion);
}

console.log('\nFeature availability:');
console.log('Feature X (requires 1.1.0) in 1.0.0:', isFeatureAvailable('1.0.0', '1.1.0')); // false
console.log('Feature X (requires 1.1.0) in 1.2.0:', isFeatureAvailable('1.2.0', '1.1.0')); // true

// Version bump for releases
function getNextVersion(current: string, type: 'major' | 'minor' | 'patch'): string {
  const next = inc(current, type);
  return next ? stringify(next) : current;
}

console.log('\nVersion bumping:');
console.log('Current: 1.2.3');
console.log('Next major:', getNextVersion('1.2.3', 'major'));
console.log('Next minor:', getNextVersion('1.2.3', 'minor'));
console.log('Next patch:', getNextVersion('1.2.3', 'patch'));

// ==================== 15. Using Namespace API ====================

console.log('\n📦 15. Using Namespace API (SemverUtils)');
console.log('-'.repeat(40));

// All functions are available under SemverUtils namespace
const parsed = SemverUtils.parse('2.1.0-beta.1+build.123');
console.log('SemverUtils.parse:', parsed);

console.log('SemverUtils.isValid("1.2.3"):', SemverUtils.isValid('1.2.3'));
console.log('SemverUtils.compare("1.0.0", "2.0.0"):', SemverUtils.compare('1.0.0', '2.0.0'));
console.log('SemverUtils.satisfies("1.5.0", "^1.0.0"):', SemverUtils.satisfies('1.5.0', '^1.0.0'));

console.log('\n' + '='.repeat(60));
console.log('✅ All examples completed!');
console.log('='.repeat(60));