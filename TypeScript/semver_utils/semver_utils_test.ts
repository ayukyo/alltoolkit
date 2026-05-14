/**
 * Tests for SemVer Utilities Module
 */

import {
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
  incMajor,
  incMinor,
  incPatch,
  inc,
  diff,
  isStable,
  base,
  parseRange,
  satisfies,
  maxSatisfying,
  minSatisfying,
  coerce,
  compareAsc,
  compareDesc,
  SemVer,
  VersionRange,
} from './mod';

// Test helpers
let passed = 0;
let failed = 0;

function assertEqual<T>(actual: T, expected: T, message: string): void {
  if (JSON.stringify(actual) === JSON.stringify(expected)) {
    passed++;
  } else {
    failed++;
    console.error(`❌ ${message}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(actual: boolean, message: string): void {
  if (actual) {
    passed++;
  } else {
    failed++;
    console.error(`❌ ${message}: expected true, got false`);
  }
}

function assertFalse(actual: boolean, message: string): void {
  if (!actual) {
    passed++;
  } else {
    failed++;
    console.error(`❌ ${message}: expected false, got true`);
  }
}

function assertNull<T>(actual: T | null, message: string): void {
  if (actual === null) {
    passed++;
  } else {
    failed++;
    console.error(`❌ ${message}: expected null, got ${JSON.stringify(actual)}`);
  }
}

function testSection(name: string): void {
  console.log(`\n=== ${name} ===`);
}

// ==================== Parse Tests ====================

testSection('Parse');

function testParseBasic() {
  const v = parse('1.2.3');
  assertTrue(v !== null, 'parse basic version');
  if (v) {
    assertEqual(v.major, 1, 'major version');
    assertEqual(v.minor, 2, 'minor version');
    assertEqual(v.patch, 3, 'patch version');
    assertEqual(v.prerelease.length, 0, 'no prerelease');
    assertEqual(v.build.length, 0, 'no build');
  }
}

function testParseWithV() {
  const v = parse('v1.2.3');
  assertTrue(v !== null, 'parse version with v prefix');
}

function testParsePrerelease() {
  const v = parse('1.2.3-alpha.1');
  assertTrue(v !== null, 'parse version with prerelease');
  if (v) {
    assertEqual(v.prerelease.length, 2, 'prerelease identifiers count');
    assertEqual(v.prerelease[0], 'alpha', 'prerelease identifier 1');
    // Numeric prerelease identifiers are stored as numbers (per SemVer spec)
    assertEqual(v.prerelease[1], 1, 'prerelease identifier 2 (numeric)');
  }
}

function testParseBuild() {
  const v = parse('1.2.3+build.123');
  assertTrue(v !== null, 'parse version with build');
  if (v) {
    assertEqual(v.build.length, 2, 'build identifiers count');
    assertEqual(v.build[0], 'build', 'build identifier 1');
    assertEqual(v.build[1], '123', 'build identifier 2');
  }
}

function testParseFull() {
  const v = parse('1.2.3-alpha.1+build.123');
  assertTrue(v !== null, 'parse full version');
  if (v) {
    assertEqual(v.major, 1, 'full version major');
    assertEqual(v.minor, 2, 'full version minor');
    assertEqual(v.patch, 3, 'full version patch');
    assertEqual(v.prerelease.length, 2, 'full version prerelease');
    assertEqual(v.build.length, 2, 'full version build');
  }
}

function testParseInvalid() {
  assertNull(parse(''), 'parse empty string');
  assertNull(parse('1'), 'parse single number');
  assertNull(parse('1.2'), 'parse two numbers');
  assertNull(parse('a.b.c'), 'parse letters');
  assertNull(parse('1.2.3.'), 'parse trailing dot');
}

testParseBasic();
testParseWithV();
testParsePrerelease();
testParseBuild();
testParseFull();
testParseInvalid();

// ==================== Validation Tests ====================

testSection('Validation');

function testIsValid() {
  assertTrue(isValid('1.2.3'), 'valid basic version');
  assertTrue(isValid('v1.2.3'), 'valid version with v');
  assertTrue(isValid('0.0.0'), 'valid zero version');
  assertTrue(isValid('1.2.3-alpha'), 'valid prerelease');
  assertTrue(isValid('1.2.3+build'), 'valid build');
  assertTrue(isValid('1.2.3-alpha.1+build.123'), 'valid full version');
  assertFalse(isValid(''), 'invalid empty');
  assertFalse(isValid('1'), 'invalid single number');
  assertFalse(isValid('1.2'), 'invalid two numbers');
  assertFalse(isValid('a.b.c'), 'invalid letters');
}

testIsValid();

// ==================== Stringify Tests ====================

testSection('Stringify');

function testStringify() {
  const v = parse('1.2.3-alpha.1+build');
  if (v) {
    assertEqual(stringify(v), '1.2.3-alpha.1+build', 'stringify full version');
  }
  
  const v2 = parse('1.2.3');
  if (v2) {
    assertEqual(stringify(v2), '1.2.3', 'stringify basic version');
  }
}

testStringify();

// ==================== Compare Tests ====================

testSection('Compare');

function testCompareBasic() {
  assertEqual(compare('1.2.3', '1.2.3'), 0, 'equal versions');
  assertEqual(compare('1.2.4', '1.2.3'), 1, 'greater patch');
  assertEqual(compare('1.2.3', '1.2.4'), -1, 'lesser patch');
  assertEqual(compare('1.3.0', '1.2.9'), 1, 'greater minor');
  assertEqual(compare('2.0.0', '1.9.9'), 1, 'greater major');
  assertEqual(compare('1.0.0', '2.0.0'), -1, 'lesser major');
}

function testComparePrerelease() {
  assertEqual(compare('1.0.0-alpha', '1.0.0-beta'), -1, 'alpha < beta');
  assertEqual(compare('1.0.0-alpha.1', '1.0.0-alpha.2'), -1, 'alpha.1 < alpha.2');
  assertEqual(compare('1.0.0-alpha', '1.0.0'), -1, 'prerelease < release');
  assertEqual(compare('1.0.0', '1.0.0-alpha'), 1, 'release > prerelease');
  assertEqual(compare('1.0.0-alpha', '1.0.0-alpha'), 0, 'same prerelease');
}

function testCompareNumericVsAlpha() {
  assertEqual(compare('1.0.0-1', '1.0.0-alpha'), -1, 'numeric < alpha prerelease');
  assertEqual(compare('1.0.0-alpha', '1.0.0-1'), 1, 'alpha > numeric prerelease');
}

testCompareBasic();
testComparePrerelease();
testCompareNumericVsAlpha();

// ==================== Comparison Operators Tests ====================

testSection('Comparison Operators');

function testComparisonOps() {
  assertTrue(gt('2.0.0', '1.0.0'), 'gt true');
  assertFalse(gt('1.0.0', '2.0.0'), 'gt false');
  
  assertTrue(lt('1.0.0', '2.0.0'), 'lt true');
  assertFalse(lt('2.0.0', '1.0.0'), 'lt false');
  
  assertTrue(gte('2.0.0', '1.0.0'), 'gte true greater');
  assertTrue(gte('1.0.0', '1.0.0'), 'gte true equal');
  assertFalse(gte('1.0.0', '2.0.0'), 'gte false');
  
  assertTrue(lte('1.0.0', '2.0.0'), 'lte true lesser');
  assertTrue(lte('1.0.0', '1.0.0'), 'lte true equal');
  assertFalse(lte('2.0.0', '1.0.0'), 'lte false');
  
  assertTrue(eq('1.0.0', '1.0.0'), 'eq true');
  assertFalse(eq('1.0.0', '1.0.1'), 'eq false');
  
  assertTrue(neq('1.0.0', '1.0.1'), 'neq true');
  assertFalse(neq('1.0.0', '1.0.0'), 'neq false');
}

testComparisonOps();

// ==================== Max/Min Tests ====================

testSection('Max/Min');

function testMaxMin() {
  const maxResult = max('1.0.0', '2.0.0');
  assertTrue(maxResult !== null, 'max returns version');
  if (maxResult) {
    assertEqual(maxResult.major, 2, 'max selects greater');
  }
  
  const minResult = min('1.0.0', '2.0.0');
  assertTrue(minResult !== null, 'min returns version');
  if (minResult) {
    assertEqual(minResult.major, 1, 'min selects lesser');
  }
}

testMaxMin();

// ==================== Sort Tests ====================

testSection('Sort');

function testSort() {
  const versions = ['2.0.0', '1.0.0', '1.5.0', '1.0.5', '0.9.0'];
  const sorted = sort(versions);
  
  assertEqual(sorted.length, 5, 'sort returns all versions');
  assertEqual(sorted[0].major, 0, 'sort ascending first');
  assertEqual(sorted[4].major, 2, 'sort ascending last');
  
  const rsorted = rsort(versions);
  assertEqual(rsorted[0].major, 2, 'sort descending first');
  assertEqual(rsorted[4].major, 0, 'sort descending last');
}

testSort();

// ==================== Increment Tests ====================

testSection('Increment');

function testIncrement() {
  const v = '1.2.3';
  
  const majorInc = incMajor(v);
  assertTrue(majorInc !== null, 'incMajor returns version');
  if (majorInc) {
    assertEqual(majorInc.major, 2, 'major incremented');
    assertEqual(majorInc.minor, 0, 'minor reset');
    assertEqual(majorInc.patch, 0, 'patch reset');
  }
  
  const minorInc = incMinor(v);
  assertTrue(minorInc !== null, 'incMinor returns version');
  if (minorInc) {
    assertEqual(minorInc.major, 1, 'major unchanged');
    assertEqual(minorInc.minor, 3, 'minor incremented');
    assertEqual(minorInc.patch, 0, 'patch reset');
  }
  
  const patchInc = incPatch(v);
  assertTrue(patchInc !== null, 'incPatch returns version');
  if (patchInc) {
    assertEqual(patchInc.major, 1, 'patch inc major unchanged');
    assertEqual(patchInc.minor, 2, 'patch inc minor unchanged');
    assertEqual(patchInc.patch, 4, 'patch incremented');
  }
  
  const majorByType = inc(v, 'major');
  if (majorByType) {
    assertEqual(majorByType.major, 2, 'inc major by type');
  }
  
  const minorByType = inc(v, 'minor');
  if (minorByType) {
    assertEqual(minorByType.minor, 3, 'inc minor by type');
  }
  
  const patchByType = inc(v, 'patch');
  if (patchByType) {
    assertEqual(patchByType.patch, 4, 'inc patch by type');
  }
}

testIncrement();

// ==================== Diff Tests ====================

testSection('Diff');

function testDiff() {
  assertEqual(diff('1.0.0', '2.0.0'), 'major', 'major diff');
  assertEqual(diff('1.0.0', '1.1.0'), 'minor', 'minor diff');
  assertEqual(diff('1.0.0', '1.0.1'), 'patch', 'patch diff');
  assertEqual(diff('1.0.0', '1.0.0'), null, 'no diff');
  assertEqual(diff('1.0.0-alpha', '1.0.0-beta'), 'prerelease', 'prerelease diff');
}

testDiff();

// ==================== Stability Tests ====================

testSection('Stability');

function testStability() {
  assertTrue(isStable('1.0.0'), 'stable version');
  assertFalse(isStable('1.0.0-alpha'), 'unstable prerelease');
  assertFalse(isStable('1.0.0-beta.1'), 'unstable beta');
  assertTrue(isStable('0.1.0'), '0.x stable');
}

function testBase() {
  assertEqual(base('1.2.3-alpha+build'), '1.2.3', 'base strips prerelease and build');
  assertEqual(base('1.2.3'), '1.2.3', 'base unchanged without extras');
}

testStability();
testBase();

// ==================== Range Parsing Tests ====================

testSection('Range Parsing');

function testParseRange() {
  // Caret range
  const caretRanges = parseRange('^1.2.3');
  assertTrue(caretRanges.length > 0, 'caret range parsed');
  
  // Tilde range
  const tildeRanges = parseRange('~1.2.3');
  assertTrue(tildeRanges.length > 0, 'tilde range parsed');
  
  // Comparison operators
  const gtRanges = parseRange('>1.0.0');
  assertTrue(gtRanges.length > 0, 'greater than range parsed');
  
  const gteRanges = parseRange('>=1.0.0');
  assertTrue(gteRanges.length > 0, 'greater than or equal range parsed');
  
  const ltRanges = parseRange('<2.0.0');
  assertTrue(ltRanges.length > 0, 'less than range parsed');
  
  const lteRanges = parseRange('<=2.0.0');
  assertTrue(lteRanges.length > 0, 'less than or equal range parsed');
  
  // Hyphen range
  const hyphenRanges = parseRange('1.0.0 - 2.0.0');
  assertTrue(hyphenRanges.length > 0, 'hyphen range parsed');
  
  // OR range
  const orRanges = parseRange('1.0.0 || 2.0.0');
  assertEqual(orRanges.length, 2, 'OR range parsed');
  
  // Wildcard
  const starRanges = parseRange('*');
  assertTrue(starRanges.length > 0, 'star wildcard parsed');
  
  // Major wildcard
  const majorWildRanges = parseRange('1.x');
  assertTrue(majorWildRanges.length > 0, 'major wildcard parsed');
  
  // Minor wildcard
  const minorWildRanges = parseRange('1.2.x');
  assertTrue(minorWildRanges.length > 0, 'minor wildcard parsed');
}

testParseRange();

// ==================== Satisfies Tests ====================

testSection('Satisfies');

function testSatisfies() {
  // Exact match
  assertTrue(satisfies('1.2.3', '1.2.3'), 'exact match');
  
  // Caret
  assertTrue(satisfies('1.2.3', '^1.2.3'), 'caret satisfied');
  assertTrue(satisfies('1.2.4', '^1.2.3'), 'caret higher patch');
  assertTrue(satisfies('1.3.0', '^1.2.3'), 'caret higher minor');
  assertFalse(satisfies('2.0.0', '^1.2.3'), 'caret major break');
  
  // Tilde
  assertTrue(satisfies('1.2.3', '~1.2.3'), 'tilde satisfied');
  assertTrue(satisfies('1.2.9', '~1.2.3'), 'tilde higher patch');
  assertFalse(satisfies('1.3.0', '~1.2.3'), 'tilde minor break');
  
  // Comparison
  assertTrue(satisfies('1.5.0', '>1.0.0'), 'greater than');
  assertTrue(satisfies('1.0.0', '>=1.0.0'), 'greater than or equal');
  assertTrue(satisfies('0.5.0', '<1.0.0'), 'less than');
  assertTrue(satisfies('1.0.0', '<=1.0.0'), 'less than or equal');
  
  // Range
  assertTrue(satisfies('1.5.0', '>=1.0.0 <2.0.0'), 'range satisfied');
  assertFalse(satisfies('2.5.0', '>=1.0.0 <2.0.0'), 'range not satisfied');
  
  // OR
  assertTrue(satisfies('1.0.0', '1.0.0 || 2.0.0'), 'OR first');
  assertTrue(satisfies('2.0.0', '1.0.0 || 2.0.0'), 'OR second');
  assertFalse(satisfies('3.0.0', '1.0.0 || 2.0.0'), 'OR none');
  
  // Hyphen
  assertTrue(satisfies('1.5.0', '1.0.0 - 2.0.0'), 'hyphen satisfied');
  assertFalse(satisfies('0.9.0', '1.0.0 - 2.0.0'), 'hyphen below');
  assertFalse(satisfies('2.1.0', '1.0.0 - 2.0.0'), 'hyphen above');
  
  // Wildcard
  assertTrue(satisfies('1.0.0', '*'), 'star wildcard');
  assertTrue(satisfies('1.5.0', '1.x'), 'major wildcard');
  assertTrue(satisfies('1.2.5', '1.2.x'), 'minor wildcard');
  
  // ^0.0.x special case
  assertTrue(satisfies('0.0.3', '^0.0.3'), 'caret 0.0.x equal');
  assertFalse(satisfies('0.0.4', '^0.0.3'), 'caret 0.0.x higher');
  
  // ^0.x.y special case
  assertTrue(satisfies('0.2.5', '^0.2.3'), 'caret 0.x.y satisfied');
  assertFalse(satisfies('0.3.0', '^0.2.3'), 'caret 0.x.y minor break');
}

testSatisfies();

// ==================== Max/Min Satisfying Tests ====================

testSection('Max/Min Satisfying');

function testMaxMinSatisfying() {
  const versions = ['1.0.0', '1.2.3', '1.5.0', '2.0.0', '2.1.0'];
  
  const maxInRange = maxSatisfying(versions, '>=1.0.0 <2.0.0');
  assertTrue(maxInRange !== null, 'maxSatisfying returns version');
  if (maxInRange) {
    assertEqual(stringify(maxInRange), '1.5.0', 'maxSatisfying correct');
  }
  
  const minInRange = minSatisfying(versions, '>=1.0.0 <2.0.0');
  assertTrue(minInRange !== null, 'minSatisfying returns version');
  if (minInRange) {
    assertEqual(stringify(minInRange), '1.0.0', 'minSatisfying correct');
  }
  
  const noMatch = maxSatisfying(versions, '>=3.0.0');
  assertNull(noMatch, 'maxSatisfying no match');
  
  const noMatchMin = minSatisfying(versions, '>=3.0.0');
  assertNull(noMatchMin, 'minSatisfying no match');
}

testMaxMinSatisfying();

// ==================== Coerce Tests ====================

testSection('Coerce');

function testCoerce() {
  const c1 = coerce('v1.2.3');
  assertTrue(c1 !== null, 'coerce v-prefixed');
  if (c1) {
    assertEqual(c1.major, 1, 'coerce major');
    assertEqual(c1.minor, 2, 'coerce minor');
    assertEqual(c1.patch, 3, 'coerce patch');
  }
  
  const c2 = coerce('version 1.2');
  assertTrue(c2 !== null, 'coerce partial');
  if (c2) {
    assertEqual(c2.major, 1, 'coerce partial major');
    assertEqual(c2.minor, 2, 'coerce partial minor');
    assertEqual(c2.patch, 0, 'coerce partial patch default');
  }
  
  const c3 = coerce('1');
  assertTrue(c3 !== null, 'coerce single number');
  if (c3) {
    assertEqual(c3.major, 1, 'coerce single major');
    assertEqual(c3.minor, 0, 'coerce single minor default');
    assertEqual(c3.patch, 0, 'coerce single patch default');
  }
  
  assertNull(coerce('no version here'), 'coerce no match');
}

testCoerce();

// ==================== Compare Asc/Desc Tests ====================

testSection('Compare Asc/Desc');

function testCompareAscDesc() {
  assertEqual(compareAsc('1.0.0', '2.0.0'), -1, 'compareAsc');
  assertEqual(compareDesc('1.0.0', '2.0.0'), 1, 'compareDesc');
}

testCompareAscDesc();

// ==================== Summary ====================

console.log('\n' + '='.repeat(50));
console.log(`✅ Tests passed: ${passed}`);
console.log(`❌ Tests failed: ${failed}`);
console.log(`📊 Total tests: ${passed + failed}`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}