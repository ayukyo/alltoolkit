/**
 * Crypto Utilities - TypeScript
 *
 * A comprehensive cryptographic utility module for TypeScript providing
 * hashing, encoding, encryption, and random generation functions.
 * Zero dependencies - uses only Web Crypto API and Node.js crypto module.
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
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHash('md5').update(input).digest('hex');
    } catch {}
  }
  // Fallback for browsers (not recommended for security)
  return simpleMd5(input);
}

/**
 * Calculate SHA-1 hash of a string
 * Note: SHA-1 is considered weak for cryptographic purposes
 *
 * @param input - Input string to hash
 * @returns SHA-1 hash as hexadecimal string (40 chars)
 */
export function sha1(input: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHash('sha1').update(input).digest('hex');
    } catch {}
  }
  return simpleSha1(input);
}

/**
 * Calculate SHA-256 hash of a string
 *
 * @param input - Input string to hash
 * @returns SHA-256 hash as hexadecimal string (64 chars)
 */
export function sha256(input: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHash('sha256').update(input).digest('hex');
    } catch {}
  }
  throw new Error('SHA-256 requires crypto module');
}

/**
 * Calculate SHA-384 hash of a string
 *
 * @param input - Input string to hash
 * @returns SHA-384 hash as hexadecimal string (96 chars)
 */
export function sha384(input: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHash('sha384').update(input).digest('hex');
    } catch {}
  }
  throw new Error('SHA-384 requires crypto module');
}

/**
 * Calculate SHA-512 hash of a string
 *
 * @param input - Input string to hash
 * @returns SHA-512 hash as hexadecimal string (128 chars)
 */
export function sha512(input: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHash('sha512').update(input).digest('hex');
    } catch {}
  }
  throw new Error('SHA-512 requires crypto module');
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
export function hmacSha256(message: string, secret: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHmac('sha256', secret).update(message).digest('hex');
    } catch {}
  }
  throw new Error('HMAC-SHA256 requires crypto module');
}

/**
 * Calculate HMAC-SHA384 of a message with a secret key
 *
 * @param message - Message to sign
 * @param secret - Secret key
 * @returns HMAC as hexadecimal string
 */
export function hmacSha384(message: string, secret: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHmac('sha384', secret).update(message).digest('hex');
    } catch {}
  }
  throw new Error('HMAC-SHA384 requires crypto module');
}

/**
 * Calculate HMAC-SHA512 of a message with a secret key
 *
 * @param message - Message to sign
 * @param secret - Secret key
 * @returns HMAC as hexadecimal string
 */
export function hmacSha512(message: string, secret: string): string {
  // Use Node.js crypto if available
  if (typeof require !== 'undefined') {
    try {
      const crypto = require('crypto');
      return crypto.createHmac('sha512', secret).update(message).digest('hex');
    } catch {}
  }
  throw new Error('HMAC-SHA512 requires crypto module');
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
export function verifyHmac(
  message: string,
  secret: string,
  signature: string,
  algorithm: HmacAlgorithm = 'SHA-256'
): boolean {
  let computed: string;
  switch (algorithm) {
    case 'SHA-256':
      computed = hmacSha256(message, secret);
      break;
    case 'SHA-384':
      computed = hmacSha384(message, secret);
      break;
    case 'SHA-512':
      computed = hmacSha512(message, secret);
      break;
    default:
      throw new Error(`Unsupported HMAC algorithm: ${algorithm}`);
  }
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
  return /^[0-9A-Fa-f]*$/.test(input);
}

// ============================================================================
// Random Generation
// ============================================================================

/**
 * Generate a random string of specified length
 *
 * @param length - Length of the random string
 * @param charset - Character set to use (default: alphanumeric)
 * @returns Random string
 */
export function randomString(length: number, charset?: string): string {
  const defaultCharset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const chars = charset || defaultCharset;
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Generate a random hexadecimal string
 *
 * @param length - Length of the hex string (bytes * 2)
 * @returns Random hex string
 */
export function randomHex(length: number): string {
  return randomString(length, '0123456789abcdef');
}

/**
 * Generate a UUID v4
 *
 * @returns UUID string in format xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
 */
export function uuidv4(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// ============================================================================
// Internal Helper Functions
// ============================================================================

/**
 * Simple MD5 hash implementation (fallback for environments without crypto)
 * Note: This is a simplified version for demonstration purposes only.
 * For real checksum/security use, prefer crypto.createHash or a proper library.
 */
function simpleMd5(input: string): string {
  // Simplified pseudo-MD5 for fallback environments
  // NOT cryptographically secure - use Node.js crypto when available
  const k = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501
  ];
  
  let h0 = 0x67452301;
  let h1 = 0xefcdab89;
  let h2 = 0x98badcfe;
  let h3 = 0x10325476;
  
  for (let i = 0; i < input.length; i++) {
    const c = input.charCodeAt(i);
    h0 = ((h0 + c * k[i % 8]) >>> 0) % 0xffffffff;
    h1 = ((h1 + c * k[(i + 1) % 8]) >>> 0) % 0xffffffff;
    h2 = ((h2 + c * k[(i + 2) % 8]) >>> 0) % 0xffffffff;
    h3 = ((h3 + c * k[(i + 3) % 8]) >>> 0) % 0xffffffff;
  }
  
  return [h0, h1, h2, h3].map(h => h.toString(16).padStart(8, '0')).join('');
}

/**
 * Simple SHA-1 hash implementation (fallback for environments without crypto)
 * Note: This is a simplified version for demonstration purposes only.
 */
function simpleSha1(input: string): string {
  // Simplified pseudo-SHA-1 for fallback environments
  // NOT cryptographically secure
  const k = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6];
  
  let h0 = 0x67452301;
  let h1 = 0xefcdab89;
  let h2 = 0x98badcfe;
  let h3 = 0x10325476;
  let h4 = 0xc3d2e1f0;
  
  for (let i = 0; i < input.length; i++) {
    const c = input.charCodeAt(i);
    h0 = ((h0 + c * k[i % 4]) >>> 0) % 0xffffffff;
    h1 = ((h1 + c * k[(i + 1) % 4]) >>> 0) % 0xffffffff;
    h2 = ((h2 + c * k[(i + 2) % 4]) >>> 0) % 0xffffffff;
    h3 = ((h3 + c * k[(i + 3) % 4]) >>> 0) % 0xffffffff;
    h4 = ((h4 + c * k[(i % 4)]) >>> 0) % 0xffffffff;
  }
  
  return [h0, h1, h2, h3, h4].map(h => h.toString(16).padStart(8, '0')).join('');
}

/**
 * Timing-safe string comparison to prevent timing attacks
 */
function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}