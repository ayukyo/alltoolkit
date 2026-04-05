/**
 * UUID Utilities Module for TypeScript
 * 
 * A comprehensive UUID (Universally Unique Identifier) generation and manipulation
 * utility module with zero dependencies.
 * 
 * Features:
 * - UUID v4 generation (random-based)
 * - UUID v1 generation (timestamp-based)
 * - UUID validation and parsing
 * - Format conversion (standard, compact, uppercase)
 * - Alternative ID formats (Nano ID, Short ID)
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module uuid_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * UUID version enum
 */
export enum UuidVersion {
  V1 = 1,
  V4 = 4,
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
} as const;

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
 * Generate a UUID v4 (random-based)
 * @returns Standard UUID v4 string (36 characters with hyphens)
 * @example
 * ```typescript
 * const uuid = UuidUtils.v4();
 * // "550e8400-e29b-41d4-a716-446655440000"
 * ```
 */
export function v4(): string {
  const bytes = new Uint8Array(16);
  
  // Fill with random values
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    crypto.getRandomValues(bytes);
  } else {
    // Fallback for environments without crypto API
    for (let i = 0; i < 16; i++) {
      bytes[i] = Math.floor(Math.random() * 256);
    }
  }
  
  // Set version (4) - bits 12-15 of time_hi_and_version field
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  
  // Set variant (RFC 4122) - bits 6-7 of clock_seq_hi_and_reserved
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  
  return bytesToUuid(bytes);
}

/**
 * Generate a UUID v1 (timestamp-based)
 * @returns Standard UUID v1 string (36 characters with hyphens)
 * @example
 * ```typescript
 * const uuid = UuidUtils.v1();
 * // "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
 * ```
 */
export function v1(): string {
  const now = Date.now();
  const bytes = new Uint8Array(16);
  
  // Timestamp (60 bits)
  // UUID epoch starts at October 15, 1582
  const uuidEpoch = 122192928000000000; // 100-nanosecond intervals from UUID epoch to Unix epoch
  const timestamp = (now * 10000) + uuidEpoch;
  
  // time_low (32 bits)
  bytes[0] = (timestamp >> 24) & 0xff;
  bytes[1] = (timestamp >> 16) & 0xff;
  bytes[2] = (timestamp >> 8) & 0xff;
  bytes[3] = timestamp & 0xff;
  
  // time_mid (16 bits)
  bytes[4] = (timestamp >> 40) & 0xff;
  bytes[5] = (timestamp >> 32) & 0xff;
  
  // time_hi_and_version (16 bits)
  bytes[6] = ((timestamp >> 56) & 0x0f) | 0x10; // version 1
  bytes[7] = (timestamp >> 48) & 0xff;
  
  // clock_seq_hi_and_reserved (8 bits)
  const clockSeq = Math.floor(Math.random() * 0x3fff);
  bytes[8] = (clockSeq >> 8) & 0x3f | 0x80; // variant RFC 4122
  
  // clock_seq_low (8 bits)
  bytes[9] = clockSeq & 0xff;
  
  // node (48 bits) - random node for this implementation
  for (let i = 10; i < 16; i++) {
    bytes[i] = Math.floor(Math.random() * 256);
  }
  // Set multicast bit to avoid conflicts with real MAC addresses
  bytes[10] |= 0x01;
  
  return bytesToUuid(bytes);
}

/**
 * Generate a compact UUID (without hyphens)
 * @param version - UUID version to generate (default: 4)
 * @returns Compact UUID string (32 characters without hyphens)
 * @example
 * ```typescript
 * const compact = UuidUtils.compact();
 * // "550e8400e29b41d4a716446655440000"
 * ```
 */
export function compact(version: 1 | 4 = 4): string {
  const uuid = version === 1 ? v1() : v4();
  return uuid.replace(/-/g, '');
}

/**
 * Generate an uppercase UUID
 * @param version - UUID version to generate (default: 4)
 * @returns Uppercase UUID string
 * @example
 * ```typescript
 * const upper = UuidUtils.uppercase();
 * // "550E8400-E29B-41D4-A716-446655440000"
 * ```
 */
export function uppercase(version: 1 | 4 = 4): string {
  const uuid = version === 1 ? v1() : v4();
  return uuid.toUpperCase();
}

/**
 * Validate a UUID string
 * @param uuid - UUID string to validate
 * @param version - Specific version to validate against (optional)
 * @returns True if valid UUID
 * @example
 * ```typescript
 * UuidUtils.isValid('550e8400-e29b-41d4-a716-446655440000'); // true
 * UuidUtils.isValid('550e8400-e29b-41d4-a716-446655440000', 4); // true
 * UuidUtils.isValid('invalid'); // false
 * ```
 */
export function isValid(uuid: string, version?: 1 | 3 | 4 | 5): boolean {
  if (!uuid || typeof uuid !== 'string') {
    return false;
  }
  
  const pattern = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-([0-9a-fA-F])[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/;
  const match = uuid.match(pattern);
  
  if (!match) {
    return false;
  }
  
  if (version !== undefined) {
    const detectedVersion = parseInt(match[1], 16);
    return detectedVersion === version;
  }
  
  return true;
}

/**
 * Parse a UUID string into its components
 * @param uuid - UUID string to parse
 * @returns UuidObject with parsed components, or null if invalid
 * @example
 * ```typescript
 * const parsed = UuidUtils.parse('550e8400-e29b-41d4-a716-446655440000');
 * // { version: 4, variant: 1 }
 * ```
 */
export function parse(uuid: string): UuidObject | null {
  if (!isValid(uuid)) {
    return null;
  }
  
  const clean = uuid.replace(/-/g, '').toLowerCase();
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
  }
  
  return result;
}

/**
 * Get UUID version
 * @param uuid - UUID string
 * @returns Version number (1, 3, 4, 5) or -1 if invalid
 * @example
 * ```typescript
 * UuidUtils.getVersion('550e8400-e29b-41d4-a716-446655440000'); // 4
 * ```
 */
export function getVersion(uuid: string): number {
  const parsed = parse(uuid);
  return parsed ? parsed.version : -1;
}

/**
 * Get UUID variant
 * @param uuid - UUID string
 * @returns Variant number (0-3) or -1 if invalid
 * @example
 * ```typescript
 * UuidUtils.getVariant('550e8400-e29b-41d4-a716-446655440000'); // 1 (RFC 4122)
 * ```
 */
export function getVariant(uuid: string): number {
  const parsed = parse(uuid);
  return parsed ? parsed.variant : -1;
}

/**
 * Convert standard UUID to compact format (remove hyphens)
 * @param uuid - UUID string
 * @returns Compact UUID or null if invalid
 * @example
 * ```typescript
 * UuidUtils.toCompact('550e8400-e29b-41d4-a716-446655440000');
 * // "550e8400e29b41d4a716446655440000"
 * ```
 */
export function toCompact(uuid: string): string | null {
  if (!isValid(uuid)) {
    return null;
  }
  return uuid.replace(/-/g, '');
}

/**
 * Convert compact UUID to standard format (add hyphens)
 * @param compact - Compact UUID string (32 characters)
 * @returns Standard UUID or null if invalid
 * @example
 * ```typescript
 * UuidUtils.toStandard('550e8400e29b41d4a716446655440000');
 * // "550e8400-e29b-41d4-a716-446655440000"
 * ```
 */
export function toStandard(compact: string): string | null {
  if (!compact || compact.length !== 32) {
    return null;
  }
  
  const pattern = /^[0-9a-fA-F]{32}$/;
  if (!pattern.test(compact)) {
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
 * @param uuid1 - First UUID
 * @param uuid2 - Second UUID
 * @returns True if UUIDs are equal (case-insensitive)
 * @example
 * ```typescript
 * UuidUtils.equals('550e8400-e29b-41d4-a716-446655440000', '550E8400-E29B-41D4-A716-446655440000');
 * // true
 * ```
 */
export function equals(uuid1: string, uuid2: string): boolean {
  if (!isValid(uuid1) || !isValid(uuid2)) {
    return false;
  }
  return uuid1.toLowerCase() === uuid2.toLowerCase();
}

// ==================== Alternative ID Formats ====================

/**
 * Generate a Nano ID (URL-friendly unique ID)
 * @param size - Length of the ID (default: 21)
 * @returns Nano ID string
 * @example
 * ```typescript
 * const nano = UuidUtils.nanoId();
 * // "V1StGXR8_Z5jdHi6B-myT"
 * ```
 */
export function nanoId(size: number = 21): string {
  const alphabet = CHARSETS.URL_SAFE;
  let id = '';
  
  for (let i = 0; i < size; i++) {
    id += alphabet[randomInt(0, alphabet.length - 1)];
  }
  
  return id;
}

/**
 * Generate a short ID (Base62 encoded)
 * @param length - Length of the ID (default: 8)
 * @returns Short ID string
 * @example
 * ```typescript
 * const short = UuidUtils.shortId();
 * // "aB3xK9mP"
 * ```
 */
export function shortId(length: number = 8): string {
  const alphabet = CHARSETS.ALPHANUMERIC;
  let id = '';
  
  for (let i = 0; i < length; i++) {
    id += alphabet[randomInt(0, alphabet.length - 1)];
  }
  
  return id;
}

// ==================== Random String Generation ====================

/**
 * Generate a random string
 * @param length - Length of the string
 * @param charset - Character set to use (default: alphanumeric)
 * @returns Random string
 * @example
 * ```typescript
 * UuidUtils.randomString(16);
 * // "aB3xK9mPqR2sT5vW"
 * ```
 */
export function randomString(length: number, charset: string = CHARSETS.ALPHANUMERIC): string {
  let result = '';
  for (let i = 0; i < length; i++) {
    result += charset[randomInt(0, charset.length - 1)];
  }
  return result;
}

/**
 * Generate a secure random password
 * @param length - Password length (default: 16, minimum: 8)
 * @returns Secure password string
 * @example
 * ```typescript
 * UuidUtils.randomPassword(16);
 * // "aB3$xK9@mPqR2#sT"
 * ```
 */
export function randomPassword(length: number = 16): string {
  const minLength = 8;
  const len = Math.max(length, minLength);
  
  // Ensure at least one of each character type
  const password = [
    CHARSETS.UPPERCASE[randomInt(0, CHARSETS.UPPERCASE.length - 1)],
    CHARSETS.LOWERCASE[randomInt(0, CHARSETS.LOWERCASE.length - 1)],
    CHARSETS.DIGITS[randomInt(0, CHARSETS.DIGITS.length - 1)],
    CHARSETS.SPECIAL[randomInt(0, CHARSETS.SPECIAL.length - 1)],
  ];
  
  // Fill remaining with all characters
  const allChars = CHARSETS.ALPHANUMERIC + CHARSETS.SPECIAL;
  for (let i = password.length; i < len; i++) {
    password.push(allChars[randomInt(0, allChars.length - 1)]);
  }
  
  // Shuffle the password
  return shuffleArray(password).join('');
}

// ==================== Helper Functions ====================

/**
 * Convert byte array to UUID string
 * @param bytes - 16-byte array
 * @returns UUID string
 */
function bytesToUuid(bytes: Uint8Array): string {
  const hex = Array.from(bytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  
  return [
    hex.slice(0, 8),
    hex.slice(8, 12),
    hex.slice(12, 16),
    hex.slice(16, 20),
    hex.slice(20, 32),
  ].join('-');
}

/**
 * Convert hex string to byte array
 * @param hex - Hex string
 * @returns Byte array
 */
function hexToBytes(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
  }
  return bytes;
}

/**
 * Generate random integer in range [min, max]
 * @param min - Minimum value (inclusive)
 * @param max - Maximum value (inclusive)
 * @returns Random integer
 */
function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Shuffle array using Fisher-Yates algorithm
 * @param array - Array to shuffle
 * @returns Shuffled array
 */
function shuffleArray<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = randomInt(0, i);
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

// ==================== Default Export ====================

/**
 * UUID Utilities namespace
 */
export const UuidUtils = {
  // UUID Generation
  v4,
  v1,
  compact,
  uppercase,
  
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
  UuidVersion,
  UuidVariant,
};

export default UuidUtils;