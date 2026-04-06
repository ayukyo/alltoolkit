/**
 * Crypto Utilities - TypeScript
 *
 * A comprehensive cryptographic utility module for TypeScript providing
 * hashing, encoding, encryption, and random generation functions.
 * Zero dependencies - uses only Web Crypto API and standard library.
 *
 * @module crypto_utils
 * @version 1.0.0
 * @author AllToolkit
 */

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Supported hash algorithms
 */
export type HashAlgorithm = 'MD5' | 'SHA-1' | 'SHA-256' | 'SHA-384' | 'SHA-512';

/**
 * Supported HMAC algorithms
 */
export type HmacAlgorithm = 'SHA-256' | 'SHA-384' | 'SHA-512';

/**
 * Character set options for random string generation
 */
export interface CharSetOptions {
  lowercase?: boolean;
  uppercase?: boolean;
  digits?: boolean;
  special?: boolean;
  custom?: string;
}

// ============================================================================
// Hash Functions
// ============================================================================

/**
 * Calculate MD5 hash of a string
 * Note: MD5 is not cryptographically secure, use for checksums only
 *
 * @param input - Input string to hash
 * @returns MD5 hash as hexadecimal string (32 chars)
 */
export function md5(input: string): string {
  return md5Hash(input);
}

/**
 * Calculate SHA-1 hash of a string
 * Note: SHA-1 is considered weak for cryptographic purposes
 *
 * @param input - Input string to hash
 * @returns SHA-1 hash as hexadecimal string (40 chars)
 */
export function sha1(input: string): string {
  return sha1Hash(input);
}

/**
 * Calculate SHA-256 hash of a string
 *
 * @param input - Input string to hash
 * @returns SHA-256 hash as hexadecimal string (64 chars)
 */
export function sha256(input: string): string {
  return sha256Hash(input);
}

/**
 * Calculate SHA-384 hash of a string
 *
 * @param input - Input string to hash
 * @returns SHA-384 hash as hexadecimal string (96 chars)
 */
export function sha384(input: string): string {
  return sha384Hash(input);
}

/**
 * Calculate SHA-512 hash of a string
 *
 * @param input - Input string to hash
 * @returns SHA-512 hash as hexadecimal string (128 chars)
 */
export function sha512(input: string): string {
  return sha512Hash(input);
}

/**
 * Calculate hash using specified algorithm
 *
 * @param input - Input string to hash
 * @param algorithm - Hash algorithm to use
 * @returns Hash as hexadecimal string
 */
export function hash(input: string, algorithm: HashAlgorithm): string {
  switch (algorithm) {
    case 'MD5':
      return md5(input);
    case 'SHA-1':
      return sha1(input);
    case 'SHA-256':
      return sha256(input);
    case 'SHA-384':
      return sha384(input);
    case 'SHA-512':
      return sha512(input);
    default:
      throw new Error(`Unsupported hash algorithm: ${algorithm}`);
  }
}

// ============================================================================
// HMAC Functions
// ============================================================================

/**
 * Calculate HMAC-SHA256 of a message with a secret key
 *
 * @param message - Message to sign
 * @param secret - Secret key
 * @returns HMAC as hexadecimal string
 */
export async function hmacSha256(message: string, secret: string): Promise<string> {
  return hmac(message, secret, 'SHA-256');
}

/**
 * Calculate HMAC-SHA384 of a message with a secret key
 *
 * @param message - Message to sign
 * @param secret - Secret key
 * @returns HMAC as hexadecimal string
 */
export async function hmacSha384(message: string, secret: string): Promise<string> {
  return hmac(message, secret, 'SHA-384');
}

/**
 * Calculate HMAC-SHA512 of a message with a secret key
 *
 * @param message - Message to sign
 * @param secret - Secret key
 * @returns HMAC as hexadecimal string
 */
export async function hmacSha512(message: string, secret: string): Promise<string> {
  return hmac(message, secret, 'SHA-512');
}

/**
 * Verify HMAC signature
 *
 * @param message - Original message
 * @param secret - Secret key
 * @param signature - Expected HMAC signature
 * @param algorithm - HMAC algorithm to use
 * @returns True if signature is valid
 */
export async function verifyHmac(
  message: string,
  secret: string,
  signature: string,
  algorithm: HmacAlgorithm = 'SHA-256'
): Promise<boolean> {
  const computed = await hmac(message, secret, algorithm);
  return timingSafeEqual(computed, signature);
}

// ============================================================================
// Base64 Encoding/Decoding
// ============================================================================

/**
 * Encode string to Base64
 *
 * @param input - Input string to encode
 * @returns Base64 encoded string
 */
export function base64Encode(input: string): string {
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(input, 'utf-8').toString('base64');
  } else {
    return btoa(unescape(encodeURIComponent(input)));
  }
}

/**
 * Decode Base64 string
 *
 * @param input - Base64 encoded string
 * @returns Decoded string
 */
export function base64Decode(input: string): string {
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(input, 'base64').toString('utf-8');
  } else {
    return decodeURIComponent(escape(atob(input)));
  }
}

/**
 * Encode string to URL-safe Base64 (RFC 4648)
 *
 * @param input - Input string to encode
 * @param padding - Whether to include padding characters (default: true)
 * @returns URL-safe Base64 encoded string
 */
export function base64UrlEncode(input: string, padding: boolean = true): string {
  let encoded = base64Encode(input)
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
  if (!padding) {
    encoded = encoded.replace(/=/g, '');
  }
  return encoded;
}

/**
 * Decode URL-safe Base64 string
 *
 * @param input - URL-safe Base64 encoded string
 * @returns Decoded string
 */
export function base64UrlDecode(input: string): string {
  const padding = 4 - (input.length % 4);
  if (padding !== 4) {
    input += '='.repeat(padding);
  }
  const standard = input.replace(/-/g, '+').replace(/_/g, '/');
  return base64Decode(standard);
}

/**
 * Check if string is valid Base64
 *
 * @param input - String to validate
 * @returns True if valid Base64
 */
export function isValidBase64(input: string): boolean {
  const base64Regex = /^[A-Za-z0-9+/]*={0,2}$/;
  if (!base64Regex.test(input)) return false;
  if (input.length % 4 !== 0) return false;
  try {
    base64Decode(input);
    return true;
  } catch {
    return false;
  }
}

// ============================================================================
// Hex Encoding/Decoding
// ============================================================================

/**
 * Encode string to hexadecimal
 *
 * @param input - Input string to encode
 * @returns Hexadecimal encoded string
 */
export function hexEncode(input: string): string {
  return input.split('')
    .map(c => c.charCodeAt(0).toString(16).padStart(2, '0'))
    .join('');
}

/**
 * Decode hexadecimal string
 *
 * @param input - Hexadecimal encoded string
 * @returns Decoded string
 */
export function hexDecode(input: string): string {
  if (input.length % 2 !== 0) {
    throw new Error('Invalid hex string: length must be even');
  }
  const bytes: number[] = [];
  for (let i = 0; i < input.length; i += 2) {
    bytes.push(parseInt(input.substr(i, 2), 16));
  }
  return bytes.map(b => String.fromCharCode(b)).join('');
}

/**
 * Check if string is valid hexadecimal
 *
 * @param input - String to validate
 * @returns True if valid hex
 */
export function isValidHex(input: string): boolean {
  return /^[0-9A-Fa-f]*$/.test
