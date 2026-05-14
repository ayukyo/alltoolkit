/**
 * SemVer Utilities Module for TypeScript
 * 
 * A comprehensive semantic versioning (SemVer) parsing, comparison, and manipulation
 * utility module with zero dependencies.
 * 
 * Features:
 * - Parse semantic version strings (major.minor.patch-prerelease+build)
 * - Compare versions (greater than, less than, equals)
 * - Sort version arrays
 * - Increment versions (major, minor, patch)
 * - Validate semantic version strings
 * - Satisfy version ranges (^, ~, >, <, >=, <=, ||)
 * - Check compatibility and stability
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module semver_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Semantic version object
 */
export interface SemVer {
  major: number;
  minor: number;
  patch: number;
  prerelease: (string | number)[];
  build: string[];
  raw: string;
}

/**
 * Comparator operator for version ranges
 */
export type ComparatorOperator = '>' | '<' | '>=' | '<=' | '=';

/**
 * Version range comparator
 */
export interface Comparator {
  operator: ComparatorOperator;
  version: SemVer;
}

/**
 * Version range (can include multiple comparators)
 */
export interface VersionRange {
  comparators: Comparator[];
}

/**
 * Pre-release identifier types
 */
export type PrereleaseIdentifier = string | number;

/**
 * Parse a semantic version string
 * @param version - Version string to parse
 * @returns Parsed SemVer object or null if invalid
 * @example
 * ```typescript
 * const v = SemverUtils.parse('1.2.3-alpha.1+build.123');
 * // { major: 1, minor: 2, patch: 3, prerelease: ['alpha', 1], build: ['build', '123'], raw: '...' }
 * ```
 */
export function parse(version: string): SemVer | null {
  if (!version || typeof version !== 'string') {
    return null;
  }

  const trimmed = version.trim();
  
  // Regex for semantic versioning
  // Format: major.minor.patch-prerelease+build
  const regex = /^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?(?:\+([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?$/;
  const match = trimmed.match(regex);
  
  if (!match) {
    return null;
  }

  const major = parseInt(match[1], 10);
  const minor = parseInt(match[2], 10);
  const patch = parseInt(match[3], 10);
  
  // Parse prerelease (numeric identifiers converted to numbers per SemVer spec)
  const prerelease: (string | number)[] = match[4] 
    ? match[4].split('.').map(id => {
        const num = parseInt(id, 10);
        // If it's a valid number and the string representation matches, use number
        if (!isNaN(num) && String(num) === id) {
          return num;
        }
        return id;
      })
    : [];
  
  // Parse build
  const build = match[5] ? match[5].split('.') : [];

  return {
    major,
    minor,
    patch,
    prerelease,
    build,
    raw: trimmed,
  };
}

/**
 * Validate a semantic version string
 * @param version - Version string to validate
 * @returns True if valid semantic version
 * @example
 * ```typescript
 * SemverUtils.isValid('1.2.3'); // true
 * SemverUtils.isValid('v1.2.3'); // true
 * SemverUtils.isValid('1.2.3-alpha.1+build'); // true
 * SemverUtils.isValid('1.2'); // false
 * ```
 */
export function isValid(version: string): boolean {
  return parse(version) !== null;
}

/**
 * Convert SemVer object to string
 * @param semver - SemVer object
 * @returns Version string
 * @example
 * ```typescript
 * const v = SemverUtils.parse('1.2.3-alpha.1+build');
 * SemverUtils.stringify(v); // "1.2.3-alpha.1+build"
 * ```
 */
export function stringify(semver: SemVer): string {
  let result = `${semver.major}.${semver.minor}.${semver.patch}`;
  
  if (semver.prerelease.length > 0) {
    result += `-${semver.prerelease.join('.')}`;
  }
  
  if (semver.build.length > 0) {
    result += `+${semver.build.join('.')}`;
  }
  
  return result;
}

/**
 * Compare two semantic versions
 * @param v1 - First version (string or SemVer)
 * @param v2 - Second version (string or SemVer)
 * @returns -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
 * @example
 * ```typescript
 * SemverUtils.compare('1.2.3', '1.2.4'); // -1
 * SemverUtils.compare('1.2.3', '1.2.3'); // 0
 * SemverUtils.compare('2.0.0', '1.9.9'); // 1
 * ```
 */
export function compare(v1: string | SemVer, v2: string | SemVer): number {
  const sv1 = typeof v1 === 'string' ? parse(v1) : v1;
  const sv2 = typeof v2 === 'string' ? parse(v2) : v2;
  
  if (!sv1 || !sv2) {
    throw new Error('Invalid version provided');
  }

  // Compare major.minor.patch
  if (sv1.major !== sv2.major) {
    return sv1.major > sv2.major ? 1 : -1;
  }
  if (sv1.minor !== sv2.minor) {
    return sv1.minor > sv2.minor ? 1 : -1;
  }
  if (sv1.patch !== sv2.patch) {
    return sv1.patch > sv2.patch ? 1 : -1;
  }

  // Compare prerelease
  return comparePrerelease(sv1.prerelease, sv2.prerelease);
}

/**
 * Compare prerelease arrays
 */
function comparePrerelease(p1: (string | number)[], p2: (string | number)[]): number {
  // A version without prerelease has higher precedence
  if (p1.length === 0 && p2.length === 0) return 0;
  if (p1.length === 0) return 1;
  if (p2.length === 0) return -1;

  const maxLen = Math.max(p1.length, p2.length);
  
  for (let i = 0; i < maxLen; i++) {
    // Longer prerelease has higher precedence
    if (i >= p1.length) return -1;
    if (i >= p2.length) return 1;

    const id1 = p1[i];
    const id2 = p2[i];
    
    // Handle numeric vs string comparison
    const isNum1 = typeof id1 === 'number';
    const isNum2 = typeof id2 === 'number';
    
    // Numeric identifiers have lower precedence than alphanumeric
    if (isNum1 && !isNum2) return -1;
    if (!isNum1 && isNum2) return 1;
    
    // Both numeric
    if (isNum1 && isNum2) {
      if (id1 !== id2) return id1 > id2 ? 1 : -1;
    } else {
      // Both alphanumeric (string), compare lexicographically
      const str1 = String(id1);
      const str2 = String(id2);
      const cmp = str1.localeCompare(str2);
      if (cmp !== 0) return cmp;
    }
  }
  
  return 0;
}

/**
 * Check if v1 > v2
 */
export function gt(v1: string | SemVer, v2: string | SemVer): boolean {
  return compare(v1, v2) > 0;
}

/**
 * Check if v1 < v2
 */
export function lt(v1: string | SemVer, v2: string | SemVer): boolean {
  return compare(v1, v2) < 0;
}

/**
 * Check if v1 >= v2
 */
export function gte(v1: string | SemVer, v2: string | SemVer): boolean {
  return compare(v1, v2) >= 0;
}

/**
 * Check if v1 <= v2
 */
export function lte(v1: string | SemVer, v2: string | SemVer): boolean {
  return compare(v1, v2) <= 0;
}

/**
 * Check if v1 == v2
 */
export function eq(v1: string | SemVer, v2: string | SemVer): boolean {
  return compare(v1, v2) === 0;
}

/**
 * Check if v1 != v2
 */
export function neq(v1: string | SemVer, v2: string | SemVer): boolean {
  return compare(v1, v2) !== 0;
}

/**
 * Get the greater of two versions
 */
export function max(v1: string | SemVer, v2: string | SemVer): SemVer | null {
  const sv1 = typeof v1 === 'string' ? parse(v1) : v1;
  const sv2 = typeof v2 === 'string' ? parse(v2) : v2;
  
  if (!sv1) return sv2;
  if (!sv2) return sv1;
  
  return compare(sv1, sv2) >= 0 ? sv1 : sv2;
}

/**
 * Get the lesser of two versions
 */
export function min(v1: string | SemVer, v2: string | SemVer): SemVer | null {
  const sv1 = typeof v1 === 'string' ? parse(v1) : v1;
  const sv2 = typeof v2 === 'string' ? parse(v2) : v2;
  
  if (!sv1) return sv2;
  if (!sv2) return sv1;
  
  return compare(sv1, sv2) <= 0 ? sv1 : sv2;
}

/**
 * Sort an array of versions in ascending order
 */
export function sort(versions: (string | SemVer)[]): SemVer[] {
  return versions
    .map(v => typeof v === 'string' ? parse(v) : v)
    .filter((v): v is SemVer => v !== null)
    .sort(compare);
}

/**
 * Sort an array of versions in descending order
 */
export function rsort(versions: (string | SemVer)[]): SemVer[] {
  return sort(versions).reverse();
}

/**
 * Increment major version
 */
export function incMajor(version: string | SemVer): SemVer | null {
  const sv = typeof version === 'string' ? parse(version) : version;
  if (!sv) return null;
  
  return {
    major: sv.major + 1,
    minor: 0,
    patch: 0,
    prerelease: [],
    build: [],
    raw: '',
  };
}

/**
 * Increment minor version
 */
export function incMinor(version: string | SemVer): SemVer | null {
  const sv = typeof version === 'string' ? parse(version) : version;
  if (!sv) return null;
  
  return {
    major: sv.major,
    minor: sv.minor + 1,
    patch: 0,
    prerelease: [],
    build: [],
    raw: '',
  };
}

/**
 * Increment patch version
 */
export function incPatch(version: string | SemVer): SemVer | null {
  const sv = typeof version === 'string' ? parse(version) : version;
  if (!sv) return null;
  
  return {
    major: sv.major,
    minor: sv.minor,
    patch: sv.patch + 1,
    prerelease: [],
    build: [],
    raw: '',
  };
}

/**
 * Increment version by type
 */
export function inc(version: string | SemVer, type: 'major' | 'minor' | 'patch'): SemVer | null {
  switch (type) {
    case 'major': return incMajor(version);
    case 'minor': return incMinor(version);
    case 'patch': return incPatch(version);
  }
}

/**
 * Get the difference between two versions
 */
export function diff(v1: string | SemVer, v2: string | SemVer): 'major' | 'minor' | 'patch' | 'prerelease' | null {
  const sv1 = typeof v1 === 'string' ? parse(v1) : v1;
  const sv2 = typeof v2 === 'string' ? parse(v2) : v2;
  
  if (!sv1 || !sv2) return null;
  
  if (sv1.major !== sv2.major) return 'major';
  if (sv1.minor !== sv2.minor) return 'minor';
  if (sv1.patch !== sv2.patch) return 'patch';
  if (sv1.prerelease.length !== sv2.prerelease.length || 
      sv1.prerelease.some((p, i) => p !== sv2.prerelease[i])) {
    return 'prerelease';
  }
  
  return null;
}

/**
 * Check if version is stable (no prerelease)
 */
export function isStable(version: string | SemVer): boolean {
  const sv = typeof version === 'string' ? parse(version) : version;
  return sv !== null && sv.prerelease.length === 0;
}

/**
 * Get the base version (without prerelease or build)
 */
export function base(version: string | SemVer): string {
  const sv = typeof version === 'string' ? parse(version) : version;
  if (!sv) return '';
  return `${sv.major}.${sv.minor}.${sv.patch}`;
}

// ==================== Version Range Parsing ====================

/**
 * Parse a version range string
 * Supports: ^, ~, >, <, >=, <=, =, ||, -, *
 */
export function parseRange(range: string): VersionRange[] {
  if (!range || typeof range !== 'string') {
    return [];
  }

  const trimmed = range.trim();
  
  // Handle || (OR)
  const orParts = trimmed.split(/\s*\|\|\s*/);
  
  return orParts.map(part => {
    const comparators: Comparator[] = [];
    
    // Handle hyphen range: 1.0.0 - 2.0.0
    const hyphenMatch = part.match(/^(\S+)\s+-\s+(\S+)$/);
    if (hyphenMatch) {
      const from = parse(hyphenMatch[1]);
      const to = parse(hyphenMatch[2]);
      
      if (from && to) {
        comparators.push({ operator: '>=', version: from });
        comparators.push({ operator: '<=', version: to });
      }
      return { comparators };
    }
    
    // Handle space-separated comparators (AND)
    const parts = part.split(/\s+/).filter(p => p.length > 0);
    
    for (const p of parts) {
      // ^ (caret) - compatible with version
      if (p.startsWith('^')) {
        const v = parse(p.slice(1));
        if (v) {
          comparators.push({ operator: '>=', version: v });
          if (v.major === 0) {
            if (v.minor === 0) {
              // ^0.0.x => >=0.0.x <0.0.(x+1)
              comparators.push({ 
                operator: '<', 
                version: { ...v, patch: v.patch + 1, prerelease: [], build: [], raw: '' }
              });
            } else {
              // ^0.x.y => >=0.x.y <0.(x+1).0
              comparators.push({ 
                operator: '<', 
                version: { ...v, minor: v.minor + 1, patch: 0, prerelease: [], build: [], raw: '' }
              });
            }
          } else {
            // ^x.y.z => >=x.y.z <(x+1).0.0
            comparators.push({ 
              operator: '<', 
              version: { ...v, major: v.major + 1, minor: 0, patch: 0, prerelease: [], build: [], raw: '' }
            });
          }
        }
        continue;
      }
      
      // ~ (tilde) - approximately equivalent
      if (p.startsWith('~')) {
        const v = parse(p.slice(1));
        if (v) {
          comparators.push({ operator: '>=', version: v });
          comparators.push({ 
            operator: '<', 
            version: { ...v, minor: v.minor + 1, patch: 0, prerelease: [], build: [], raw: '' }
          });
        }
        continue;
      }
      
      // * or x - any version
      if (p === '*' || p === 'x' || p === 'X') {
        comparators.push({ operator: '>=', version: { major: 0, minor: 0, patch: 0, prerelease: [], build: [], raw: '0.0.0' } });
        continue;
      }
      
      // Major wildcard: 1.x, 1.*
      const majorWildcard = p.match(/^(\d+)[.][xX*]$/);
      if (majorWildcard) {
        const major = parseInt(majorWildcard[1], 10);
        comparators.push({ 
          operator: '>=', 
          version: { major, minor: 0, patch: 0, prerelease: [], build: [], raw: `${major}.0.0` }
        });
        comparators.push({ 
          operator: '<', 
          version: { major: major + 1, minor: 0, patch: 0, prerelease: [], build: [], raw: '' }
        });
        continue;
      }
      
      // Minor wildcard: 1.2.x, 1.2.*
      const minorWildcard = p.match(/^(\d+)[.](\d+)[.][xX*]$/);
      if (minorWildcard) {
        const major = parseInt(minorWildcard[1], 10);
        const minor = parseInt(minorWildcard[2], 10);
        comparators.push({ 
          operator: '>=', 
          version: { major, minor, patch: 0, prerelease: [], build: [], raw: `${major}.${minor}.0` }
        });
        comparators.push({ 
          operator: '<', 
          version: { major, minor: minor + 1, patch: 0, prerelease: [], build: [], raw: '' }
        });
        continue;
      }
      
      // Standard comparators: >, <, >=, <=, =
      const compMatch = p.match(/^(>=|<=|>|<|=)(.+)$/);
      if (compMatch) {
        const op = compMatch[1] as ComparatorOperator;
        const v = parse(compMatch[2]);
        if (v) {
          comparators.push({ operator: op, version: v });
        }
        continue;
      }
      
      // Plain version (equals)
      const v = parse(p);
      if (v) {
        comparators.push({ operator: '=', version: v });
      }
    }
    
    return { comparators };
  }).filter(r => r.comparators.length > 0);
}

/**
 * Check if a version satisfies a range
 */
export function satisfies(version: string | SemVer, range: string): boolean {
  const sv = typeof version === 'string' ? parse(version) : version;
  if (!sv) return false;
  
  const ranges = parseRange(range);
  if (ranges.length === 0) return false;
  
  // Any of the OR ranges must match
  return ranges.some(r => {
    // All comparators in an AND must match
    return r.comparators.every(c => {
      const cmp = compare(sv, c.version);
      switch (c.operator) {
        case '>': return cmp > 0;
        case '<': return cmp < 0;
        case '>=': return cmp >= 0;
        case '<=': return cmp <= 0;
        case '=': return cmp === 0;
        default: return false;
      }
    });
  });
}

/**
 * Find the highest version that satisfies the range
 */
export function maxSatisfying(versions: (string | SemVer)[], range: string): SemVer | null {
  const parsed = versions
    .map(v => typeof v === 'string' ? parse(v) : v)
    .filter((v): v is SemVer => v !== null && satisfies(v, range));
  
  if (parsed.length === 0) return null;
  
  return parsed.reduce((max, v) => compare(v, max) > 0 ? v : max);
}

/**
 * Find the lowest version that satisfies the range
 */
export function minSatisfying(versions: (string | SemVer)[], range: string): SemVer | null {
  const parsed = versions
    .map(v => typeof v === 'string' ? parse(v) : v)
    .filter((v): v is SemVer => v !== null && satisfies(v, range));
  
  if (parsed.length === 0) return null;
  
  return parsed.reduce((min, v) => compare(v, min) < 0 ? v : min);
}

/**
 * Coerce a string into a semver-like version
 * Extracts version numbers from strings like "v1.2.3", "1.2.3.4", etc.
 */
export function coerce(version: string): SemVer | null {
  if (!version || typeof version !== 'string') {
    return null;
  }

  // Try to match a version pattern
  const match = version.match(/(\d+)(?:\.(\d+))?(?:\.(\d+))?/);
  if (!match) return null;

  const major = parseInt(match[1], 10);
  const minor = match[2] ? parseInt(match[2], 10) : 0;
  const patch = match[3] ? parseInt(match[3], 10) : 0;

  return {
    major,
    minor,
    patch,
    prerelease: [],
    build: [],
    raw: version,
  };
}

/**
 * Compare two versions for sorting (ascending)
 */
export function compareAsc(v1: string | SemVer, v2: string | SemVer): number {
  return compare(v1, v2);
}

/**
 * Compare two versions for sorting (descending)
 */
export function compareDesc(v1: string | SemVer, v2: string | SemVer): number {
  return compare(v2, v1);
}

// ==================== Default Export ====================

/**
 * SemVer Utilities namespace
 */
export const SemverUtils = {
  // Parsing & Validation
  parse,
  isValid,
  stringify,
  coerce,
  
  // Comparison
  compare,
  compareAsc,
  compareDesc,
  gt,
  gte,
  lt,
  lte,
  eq,
  neq,
  max,
  min,
  
  // Sorting
  sort,
  rsort,
  
  // Increment
  inc,
  incMajor,
  incMinor,
  incPatch,
  
  // Utilities
  diff,
  isStable,
  base,
  
  // Range
  parseRange,
  satisfies,
  maxSatisfying,
  minSatisfying,
};

export default SemverUtils;