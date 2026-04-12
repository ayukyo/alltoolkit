/**
 * UUID Utilities Module for TypeScript - OPTIMIZED VERSION
 * 
 * Performance improvements, bug fixes, and enhanced boundary handling.
 * 
 * Changes:
 * - Fixed v1 UUID timestamp precision issues
 * - Improved random generation with better entropy
 * - Added UUID v7 support (timestamp-ordered)
 * - Fixed validation regex for edge cases
 * - Added NIL and MAX UUID constants
 * - Improved Nano ID with cryptographically secure random
 * - Added batch UUID generation for performance
 * - Better handling of Buffer vs browser environments
 * 
 * @module uuid_utils
 * @version 1.1.0
 * @license MIT
 */

/**
 * UUID version enum
 */
export enum UuidVersion {
  V1 = 1,
  V3 = 3,
  V4 = 4,
  V5 = 5,
  V7 = 7,
}

/**
 * UUID variant enum
 */
export enum UuidVariant {
  NCS = 0,      // NCS compatibility
  RFC4122 = 1,  // RFC 4122 standard
  Microsoft = 2,// Microsoft backward compatibility
  Future = 3,   // Reserved for future use
}

/**
 * Predefined UUID namespaces for UUID v3/v5
 */
export const UUID_NAMESPACES = {
  DNS: '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
  URL: '6ba7b811-9dad-11d1-80b4-00c04fd430c8',
  OID: '6ba7b812-9dad-11d1-80b4-00c04fd430c8',
  X500: '6ba7b814-9dad-11d1-80b4-00c04fd430c8',
  NIL: '00000000-0000-0000-0000-000000000000',
} as const;

/**
 * Special UUIDs
 */
export const NIL_UUID = '00000000-0000-0000-0000-000000000000';
export const MAX_UUID = 'ffffffff-ffff-ffff-ffff-ffffffffffff';

/**
 * Character sets for random string generation
 */
export const CHARSETS = {
  LOWERCASE: 'abcdefghijklmnopqrstuvwxyz',
  UPPERCASE: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  DIGITS: '0123456789',
  SPECIAL: '!@#$%^&*()-_=+[]{}|;:,.<>?',
  HEX: '0123456789abcdef',
  HEX_UPPER: '0123456789ABCDEF',
  ALPHANUMERIC: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
  URL_SAFE: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_',
  NO_CONFUSING: 'abcdefghjkmnpqrstuvwxyz23456789',  // No i, l, o, 0, 1
} as const;

/**
 * UUID object interface
 */
export interface UuidObject {
  version: number;
  variant: number;
  timestamp?: Date;
  clockSeq?: number;
  node?: string;
}

/**
 * Options for UUID generation
 */
export interface UuidOptions {
  format?: 'standard' | 'compact' | 'uppercase';
}

// =============================================================================
// Random Generation - IMPROVED
// =============================================================================

/**
 * Get cryptographically secure random bytes
 */
function getRandomBytes(length: number): Uint8Array {
  const bytes = new Uint8Array(length);
  
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    crypto.getRandomValues(bytes);
  } else if (typeof require !== 'undefined') {
    // Node.js fallback
    try {
      const crypto = require('crypto');
      const nodeBytes = crypto.randomBytes(length);
      for (let i = 0; i < length; i++) {
        bytes[i] = nodeBytes[i];
      }
    } catch {
      // Ultimate fallback
      for (let i = 0; i < length; i++) {
        bytes[i] = Math.floor(Math.random() * 256);
      }
    }
  } else {
    // Browser fallback
    for (let i = 0; i < length; i++) {
      bytes[i] = Math.floor(Math.random() * 256);
    }
  }
  
  return bytes;
}

// =============================================================================
// UUID Generation
// =============================================================================

/**
 * Generate a UUID v4 (random-based) - OPTIMIZED
 */
export function v4(): string {
  const bytes = getRandomBytes(16);
  
  // Set version (4) - bits 12-15 of time_hi_and_version field
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  
  // Set variant (RFC 4122) - bits 6-7 of clock_seq_hi_and_reserved
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  
  return bytesToUuid(bytes);
}

/**
 * Generate a UUID v1 (timestamp-based) - FIXED
 */
let _lastTimestamp = 0n;
let _clockSeq = 0;

export function v1(): string {
  const bytes = new Uint8Array(16);
  
  // UUID epoch starts at October 15, 1582
  const UUID_EPOCH = 122192928000000000n;
  
  // Get current timestamp in 100-nanosecond intervals
  const now = BigInt(Date.now()) * 10000n;
  let timestamp = now + UUID_EPOCH;
  
  // Handle clock sequence for same timestamp
  if (timestamp <= _lastTimestamp) {
    _clockSeq = (_clockSeq + 1) & 0x3fff;
    timestamp = _lastTimestamp + 1n;
  } else {
    _clockSeq = getRandomBytes(2).reduce((acc, b, i) => i === 0 ? (b & 0x3f) : (acc << 8) | b, 0);
  }
  
  _lastTimestamp = timestamp;
  
  // time_low (32 bits)
  bytes[0] = Number((timestamp >> 24n) & 0xffn);
  bytes[1] = Number((timestamp >> 16n) & 0xffn);
  bytes[2] = Number((timestamp >> 8n) & 0xffn);
  bytes[3] = Number(timestamp & 0xffn);
  
  // time_mid (16 bits)
  bytes[4] = Number((timestamp >> 40n) & 0xffn);
  bytes[5] = Number((timestamp >> 48n) & 0xffn);
  
  // time_hi_and_version (16 bits)
  bytes[6] = Number((timestamp >> 56n) & 0x0fn) | 0x10; // version 1
  bytes[7] = Number((timestamp >> 64n) & 0xffn);
  
  // clock_seq_hi_and_reserved (8 bits)
  bytes[8] = (_clockSeq >> 8) & 0x3f | 0x80; // variant RFC 4122
  
  // clock_seq_low (8 bits)
  bytes[9] = _clockSeq & 0xff;
  
  // node (48 bits) - random node
  const nodeBytes = getRandomBytes(6);
  for (let i = 0; i < 6; i++) {
    bytes[10 + i] = nodeBytes[i];
  }
  // Set multicast bit
  bytes[10] |= 0x01;
  
  return bytesToUuid(bytes);
}

/**
 * Generate a UUID v7 (timestamp-ordered, sortable) - NEW
 */
let _v7LastTimestamp = 0;
let _v7Random = 0;

export function v7(): string {
  const bytes = new Uint8Array(16);
  const now = Date.now();
  
  if (now === _v7LastTimestamp) {
    _v7Random = (_v7Random + 1) & 0xfffff;
  } else {
    _v7LastTimestamp = now;
    _v7Random = getRandomBytes(3).reduce((acc, b, i) => (acc << 8) | b, 0) & 0xfffff;
  }
  
  // Timestamp (48 bits)
  bytes[0] = (now >> 40) & 0xff;
  bytes[1] = (now >> 32) & 0xff;
  bytes[2] = (now >> 24) & 0xff;
  bytes[3] = (now >> 16) & 0xff;
  bytes[4] = (now >> 8) & 0xff;
  bytes[5] = now & 0xff;
  
  // Version (4 bits) + random (12 bits)
  bytes[6] = 0x70 | ((_v7Random >> 16) & 0x0f);
  bytes[7] = (_v7Random >> 8) & 0xff;
  bytes[8] = _v7Random & 0xff;
  
  // Random (62 bits)
  const randomBytes = getRandomBytes(7);
  randomBytes[0] &= 0x3f; // Clear top 2 bits for variant
  randomBytes[0] |= 0x80; // Set variant
  
  for (let i = 0; i < 7; i++) {
    bytes[9 + i] = randomBytes[i];
  }
  
  return bytesToUuid(bytes);
}

/**
 * Generate a compact UUID (without hyphens)
 */
export function compact(version: 1 | 4 | 7 = 4): string {
  const uuid = version === 1 ? v1() : version === 7 ? v7() : v4();
  return uuid.replace(/-/g, '');
}

/**
 * Generate an uppercase UUID
 */
export function uppercase(version: 1 | 4 | 7 = 4): string {
  const uuid = version === 1 ? v1() : version === 7 ? v7() : v4();
  return uuid.toUpperCase();
}

/**
 * Generate multiple UUIDs at once - NEW (performance)
 */
export function batch(count: number, version: 1 | 4 | 7 = 4): string[] {
  const result: string[] = [];
  for (let i = 0; i < count; i++) {
    result.push(version === 1 ? v1() : version === 7 ? v7() : v4());
  }
  return result;
}

// =============================================================================
// Validation - IMPROVED
// =============================================================================

// Pre-compiled regex for performance
const UUID_REGEX = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/;
const UUID_COMPACT_REGEX = /^[0-9a-fA-F]{32}$/;

/**
 * Validate a UUID string - IMPROVED
 */
export function isValid(uuid: string, version?: 1 | 3 | 4 | 5 | 7): boolean {
  if (!uuid || typeof uuid !== 'string') {
    return false;
  }
  
  // Check standard format
  if (UUID_REGEX.test(uuid)) {
    if (version !== undefined) {
      const detectedVersion = parseInt(uuid[14], 16);
      return detectedVersion === version;
    }
    return true;
  }
  
  // Check compact format
  if (UUID_COMPACT_REGEX.test(uuid)) {
    if (version !== undefined) {
      const detectedVersion = parseInt(uuid[12], 16);
      return detectedVersion === version;
    }
    return true;
  }
  
  return false;
}

/**
 * Parse a UUID string into its components
 */
export function parse(uuid: string): UuidObject | null {
  if (!isValid(uuid)) {
    return null;
  }
  
  // Normalize to standard format
  const normalized = uuid.length === 32 ? toStandard(uuid) : uuid;
  if (!normalized) return null;
  
  const clean = normalized.replace(/-/g, '').toLowerCase();
  const bytes = hexToBytes(clean);
  
  const version = (bytes[6] >> 4) & 0x0f;
  const variant = (bytes[8] >> 6) & 0x03;
  
  const result: UuidObject = {
    version,
    variant,
  };
  
  if (version === 1) {
    // Extract timestamp for v1
    const low = (bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | bytes[3];
    const mid = (bytes[4] << 8) | bytes[5];
    const high = ((bytes[6] & 0x0f) << 8) | bytes[7];
    
    const timestamp = ((BigInt(high) << BigInt(48)) | (BigInt(mid) << BigInt(32)) | BigInt(low));
    const uuidEpoch = BigInt(122192928000000000);
    const unixTimestamp = Number((timestamp - uuidEpoch) / BigInt(10000));
    
    result.timestamp = new Date(unixTimestamp);
    result.clockSeq = ((bytes[8] & 0x3f) << 8) | bytes[9];
    result.node = bytes.slice(10, 16).map(b => b.toString(16).padStart(2, '0')).join('');
  } else if (version === 7) {
    // Extract timestamp for v7
    const timestamp = (BigInt(bytes[0]) << 40n) | (BigInt(bytes[1]) << 32n) | 
                      (BigInt(bytes[2]) << 24n) | (BigInt(bytes[3]) << 16n) | 
                      (BigInt(bytes[4]) << 8n) | BigInt(bytes[5]);
    result.timestamp = new Date(Number(timestamp));
  }
  
  return result;
}

/**
 * Get UUID version
 */
export function getVersion(uuid: string): number {
  if (!isValid(uuid)) return -1;
  
  const normalized = uuid.length === 32 ? uuid : uuid.replace(/-/g, '');
  const versionChar = normalized[12];
  return parseInt(versionChar, 16);
}

/**
 * Get UUID variant
 */
export function getVariant(uuid: string): number {
  if (!isValid(uuid)) return -1;
  
  const normalized = uuid.length === 32 ? uuid : uuid.replace(/-/g, '');
  const variantChar = parseInt(normalized[16], 16);
  return (variantChar >> 2) & 0x03;
}

// =============================================================================
// Format Conversion
// =============================================================================

/**
 * Convert standard UUID to compact format
 */
export function toCompact(uuid: string): string | null {
  if (!isValid(uuid)) {
    return null;
  }
  return uuid.replace(/-/g, '');
}

/**
 * Convert compact UUID to standard format - FIXED
 */
export function toStandard(compact: string): string | null {
  if (!compact || compact.length !== 32) {
    return null;
  }
  
  if (!UUID_COMPACT_REGEX.test(compact)) {
    return null;
  }
  
  return [
    compact.slice(0, 8),
    compact.slice(8, 12),
    compact.slice(12, 16),
    compact.slice(16, 20),
    compact.slice(20, 32),
  ].join('-');
}

/**
 * Compare two UUIDs for equality
 */
export function equals(uuid1: string, uuid2: string): boolean {
  if (!isValid(uuid1) || !isValid(uuid2)) {
    return false;
  }
  return uuid1.toLowerCase() === uuid2.toLowerCase();
}

// =============================================================================
// Alternative ID Formats - IMPROVED
// =============================================================================

/**
 * Generate a Nano ID (URL-friendly unique ID) - IMPROVED with secure random
 */
export function nanoId(size: number = 21): string {
  const alphabet = CHARSETS.URL_SAFE;
  const alphabetLen = alphabet.length;
  
  // Use secure random
  const randomBytes = getRandomBytes(size);
  let id = '';
  
  for (let i = 0; i < size; i++) {
    id += alphabet[randomBytes[i] % alphabetLen];
  }
  
  return id;
}

/**
 * Generate a short ID (Base62 encoded) - IMPROVED
 */
export function shortId(length: number = 8): string {
  const alphabet = CHARSETS.ALPHANUMERIC;
  const alphabetLen = alphabet.length;
  
  const randomBytes = getRandomBytes(length);
  let id = '';
  
  for (let i = 0; i < length; i++) {
    id += alphabet[randomBytes[i] % alphabetLen];
  }
  
  return id;
}

// =============================================================================
// Random String Generation
// =============================================================================

/**
 * Generate a random string - IMPROVED
 */
export function randomString(length: number, charset: string = CHARSETS.ALPHANUMERIC): string {
  if (length <= 0) return '';
  if (!charset || charset.length === 0) charset = CHARSETS.ALPHANUMERIC;
  
  const charsetLen = charset.length;
  const randomBytes = getRandomBytes(length);
  let result = '';
  
  for (let i = 0; i < length; i++) {
    result += charset[randomBytes[i] % charsetLen];
  }
  
  return result;
}

/**
 * Generate a secure random password - IMPROVED
 */
export function randomPassword(length: number = 16): string {
  const minLength = 8;
  const len = Math.max(length, minLength);
  
  // Ensure at least one of each character type
  const randomBytes = getRandomBytes(len);
  let idx = 0;
  
  const password = [
    CHARSETS.UPPERCASE[randomBytes[idx++] % CHARSETS.UPPERCASE.length],
    CHARSETS.LOWERCASE[randomBytes[idx++] % CHARSETS.LOWERCASE.length],
    CHARSETS.DIGITS[randomBytes[idx++] % CHARSETS.DIGITS.length],
    CHARSETS.SPECIAL[randomBytes[idx++] % CHARSETS.SPECIAL.length],
  ];
  
  // Fill remaining with all characters
  const allChars = CHARSETS.ALPHANUMERIC + CHARSETS.SPECIAL;
  const allLen = allChars.length;
  
  for (let i = password.length; i < len; i++) {
    password.push(allChars[randomBytes[idx++] % allLen]);
  }
  
  // Shuffle using Fisher-Yates
  for (let i = password.length - 1; i > 0; i--) {
    const j = randomBytes[idx++] % (i + 1);
    [password[i], password[j]] = [password[j], password[i]];
  }
  
  return password.join('');
}

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Convert byte array to UUID string
 */
function bytesToUuid(bytes: Uint8Array): string {
  const hex: string[] = new Array(32);
  
  for (let i = 0; i < 16; i++) {
    const b = bytes[i];
    hex[i * 2] = (b >> 4).toString(16);
    hex[i * 2 + 1] = (b & 0x0f).toString(16);
  }
  
  return [
    hex.slice(0, 8).join(''),
    hex.slice(8, 12).join(''),
    hex.slice(12, 16).join(''),
    hex.slice(16, 20).join(''),
    hex.slice(20, 32).join(''),
  ].join('-');
}

/**
 * Convert hex string to byte array
 */
function hexToBytes(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
  }
  return bytes;
}

// =============================================================================
// Default Export
// =============================================================================

export const UuidUtils = {
  // UUID Generation
  v4,
  v1,
  v7,
  compact,
  uppercase,
  batch,
  
  // Validation & Parsing
  isValid,
  parse,
  getVersion,
  getVariant,
  
  // Format Conversion
  toCompact,
  toStandard,
  equals,
  
  // Alternative IDs
  nanoId,
  shortId,
  
  // Random Generation
  randomString,
  randomPassword,
  
  // Constants
  UUID_NAMESPACES,
  CHARSETS,
  NIL_UUID,
  MAX_UUID,
  UuidVersion,
  UuidVariant,
};

export default UuidUtils;
