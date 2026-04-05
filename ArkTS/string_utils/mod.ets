/**
 * String Utilities for ArkTS
 * 
 * A comprehensive string manipulation utility module for ArkTS/HarmonyOS
 * providing common string operations with zero dependencies.
 * 
 * Features:
 * - Empty/blank checks
 * - Case conversion (camelCase, PascalCase, snake_case, kebab-case)
 * - Trimming and whitespace handling
 * - Substring operations
 * - Validation (email, URL, numeric, etc.)
 * - Padding and alignment
 * - Encoding/decoding (Base64, URL)
 * - Random string generation
 * 
 * @module string_utils
 * @version 1.0.0
 */

// ============================================
// Empty/Blank Checks
// ============================================

export function isBlank(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return true;
  }
  return str.trim().length === 0;
}

export function isNotBlank(str: string | null | undefined): boolean {
  return !isBlank(str);
}

export function isEmpty(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return true;
  }
  return str.length === 0;
}

// ============================================
// Trimming and Whitespace
// ============================================

export function trim(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.trim();
}

export function trimLeft(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.replace(/^\s+/, '');
}

export function trimRight(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.replace(/\s+$/, '');
}

export function removeWhitespace(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.replace(/\s/g, '');
}

export function normalizeWhitespace(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.replace(/\s+/g, ' ').trim();
}

// ============================================
// Case Conversion
// ============================================

export function toLowerCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.toLowerCase();
}

export function toUpperCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.toUpperCase();
}

export function capitalize(str: string | null | undefined): string {
  if (str === null || str === undefined || str.length === 0) {
    return str || '';
  }
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function uncapitalize(str: string | null | undefined): string {
  if (str === null || str === undefined || str.length === 0) {
    return str || '';
  }
  return str.charAt(0).toLowerCase() + str.slice(1);
}

export function toTitleCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.replace(/\w\S*/g, (txt) => {
    return txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase();
  });
}

export function toCamelCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return uncapitalize(toPascalCase(str));
}

export function toPascalCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str
    .replace(/[-_\s]+(.)?/g, (_, char) => (char ? char.toUpperCase() : ''))
    .replace(/^./, (char) => char.toUpperCase());
}

export function toSnakeCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str
    .replace(/([A-Z])/g, '_$1')
    .replace(/[-\s]+/g, '_')
    .replace(/^_/, '')
    .toLowerCase();
}

export function toKebabCase(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str
    .replace(/([A-Z])/g, '-$1')
    .replace(/[_\s]+/g, '-')
    .replace(/^-/, '')
    .toLowerCase();
}

// ============================================
// Substring Operations
// ============================================

export function truncate(str: string | null | undefined, maxLength: number, suffix: string = '...'): string {
  if (str === null || str === undefined) {
    return '';
  }
  if (str.length <= maxLength) {
    return str;
  }
  return str.substring(0, maxLength - suffix.length) + suffix;
}

export function substringBetween(str: string | null | undefined, open: string, close: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  const start = str.indexOf(open);
  if (start === -1) {
    return '';
  }
  const end = str.indexOf(close, start + open.length);
  if (end === -1) {
    return '';
  }
  return str.substring(start + open.length, end);
}

export function substringAfter(str: string | null | undefined, separator: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  const index = str.indexOf(separator);
  if (index === -1) {
    return '';
  }
  return str.substring(index + separator.length);
}

export function substringBefore(str: string | null | undefined, separator: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  const index = str.indexOf(separator);
  if (index === -1) {
    return str;
  }
  return str.substring(0, index);
}

export function substringAfterLast(str: string | null | undefined, separator: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  const index = str.lastIndexOf(separator);
  if (index === -1) {
    return '';
  }
  return str.substring(index + separator.length);
}

export function substringBeforeLast(str: string | null | undefined, separator: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  const index = str.lastIndexOf(separator);
  if (index === -1) {
    return str;
  }
  return str.substring(0, index);
}

// ============================================
// Prefix/Suffix Operations
// ============================================

export function startsWith(str: string | null | undefined, prefix: string, ignoreCase: boolean = false): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  if (ignoreCase) {
    return str.toLowerCase().startsWith(prefix.toLowerCase());
  }
  return str.startsWith(prefix);
}

export function endsWith(str: string | null | undefined, suffix: string, ignoreCase: boolean = false): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  if (ignoreCase) {
    return str.toLowerCase().endsWith(suffix.toLowerCase());
  }
  return str.endsWith(suffix);
}

export function removePrefix(str: string | null | undefined, prefix: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  if (str.startsWith(prefix)) {
    return str.substring(prefix.length);
  }
  return str;
}

export function removeSuffix(str: string | null | undefined, suffix: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  if (str.endsWith(suffix)) {
    return str.substring(0, str.length - suffix.length);
  }
  return str;
}

// ============================================
// Validation
// ============================================

export function isValidEmail(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(str);
}

export function isValidUrl(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  const urlRegex = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
  return urlRegex.test(str);
}

export function isNumeric(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  return /^-?\d+(\.\d+)?$/.test(str);
}

export function isInteger(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  return /^-?\d+$/.test(str);
}

export function isAlpha(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  return /^[a-zA-Z]+$/.test(str);
}

export function isAlphanumeric(str: string | null | undefined): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  return /^[a-zA-Z0-9]+$/.test(str);
}

// ============================================
// Padding and Alignment
// ============================================

export function padLeft(str: string | null | undefined, length: number, padChar: string = ' '): string {
  if (str === null || str === undefined) {
    str = '';
  }
  if (str.length >= length) {
    return str;
  }
  const padding = padChar.repeat(length - str.length);
  return padding + str;
}

export function padRight(str: string | null | undefined, length: number, padChar: string = ' '): string {
  if (str === null || str === undefined) {
    str = '';
  }
  if (str.length >= length) {
    return str;
  }
  const padding = padChar.repeat(length - str.length);
  return str + padding;
}

export function center(str: string | null | undefined, length: number, padChar: string = ' '): string {
  if (str === null || str === undefined) {
    str = '';
  }
  if (str.length >= length) {
    return str;
  }
  const totalPadding = length - str.length;
  const leftPadding = Math.floor(totalPadding / 2);
  const rightPadding = totalPadding - leftPadding;
  return padChar.repeat(leftPadding) + str + padChar.repeat(rightPadding);
}

// ============================================
// Search and Replace
// ============================================

export function contains(str: string | null | undefined, search: string, ignoreCase: boolean = false): boolean {
  if (str === null || str === undefined) {
    return false;
  }
  if (ignoreCase) {
    return str.toLowerCase().includes(search.toLowerCase());
  }
  return str.includes(search);
}

export function countMatches(str: string | null | undefined, search: string): number {
  if (str === null || str === undefined || search.length === 0) {
    return 0;
  }
  let count = 0;
  let pos = str.indexOf(search);
  while (pos !== -1) {
    count++;
    pos = str.indexOf(search, pos + search.length);
  }
  return count;
}

export function replaceAll(str: string | null | undefined, search: string, replacement: string): string {
  if (str === null || str === undefined) {
    return '';
  }
  if (search.length === 0) {
    return str;
  }
  return str.split(search).join(replacement);
}

// ============================================
// Split and Join
// ============================================

export function split(str: string | null | undefined, separator: string, limit?: number): string[] {
  if (str === null || str === undefined) {
    return [];
  }
  if (limit !== undefined) {
    return str.split(separator, limit);
  }
  return str.split(separator);
}

export function lines(str: string | null | undefined, trimEmpty: boolean = false): string[] {
  if (str === null || str === undefined) {
    return [];
  }
  const result = str.split(/\r?\n/);
  if (trimEmpty) {
    return result.filter(line => line.trim().length > 0);
  }
  return result;
}

export function join(array: string[], separator: string = ''): string {
  return array.join(separator);
}

// ============================================
// Encoding/Decoding
// ============================================

export function base64Encode(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  const buffer = new Uint8Array(str.length);
  for (let i = 0; i < str.length; i++) {
    buffer[i] = str.charCodeAt(i);
  }
  let result = '';
  const base64Chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
  for (let i = 0; i < buffer.length; i += 3) {
    const b1 = buffer[i];
    const b2 = i + 1 < buffer.length ? buffer[i + 1] : 0;
    const b3 = i + 2 < buffer.length ? buffer[i + 2] : 0;
    const bits = (b1 << 16) | (b2 << 8) | b3;
    result += base64Chars[(bits >> 18) & 0x3F];
    result += base64Chars[(bits >> 12) & 0x3F];
    result += (i + 1 < buffer.length) ? base64Chars[(bits >> 6) & 0x3F] : '=';
    result += (i + 2 < buffer.length) ? base64Chars[bits & 0x3F] : '=';
  }
  return result;
}

export function base64Decode(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  const base64Chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
  const result: number[] = [];
  let i = 0;
  while (i < str.length) {
    const c1 = base64Chars.indexOf(str.charAt(i++));
    const c2 = base64Chars.indexOf(str.charAt(i++));
    const c3 = base64Chars.indexOf(str.charAt(i++));
    const c4 = base64Chars.indexOf(str.charAt(i++));
    const bits = (c1 << 18) | (c2 << 12) | (c3 << 6) | c4;
    result.push((bits >> 16) & 0xFF);
    if (c3 !== 64) result.push((bits >> 8) & 0xFF);
    if (c4 !== 64) result.push(bits & 0xFF);
  }
  return result.map(c => String.fromCharCode(c)).join('');
}

export function urlEncode(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  let result = '';
  for (let i = 0; i < str.length; i++) {
    const char = str.charAt(i);
    if (/[a-zA-Z0-9_.!~*'()-]/.test(char)) {
      result += char;
    } else {
      const code = str.charCodeAt(i);
      result += '%' + (code < 16 ? '0' : '') + code.toString(16).toUpperCase();
    }
  }
  return result;
}

export function urlDecode(str: string | null | undefined): string {
  if (str ===
 null || str === undefined) {
    return '';
  }
  return str.replace(/%([0-9A-Fa-f]{2})/g, (_, hex) => {
    return String.fromCharCode(parseInt(hex, 16));
  });
}

// ============================================
// Random Generation
// ============================================

const DEFAULT_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const LOWERCASE_CHARS = 'abcdefghijklmnopqrstuvwxyz';
const UPPERCASE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const DIGIT_CHARS = '0123456789';
const ALPHANUMERIC_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const SPECIAL_CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?';

export function randomString(length: number, chars: string = DEFAULT_CHARS): string {
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

export function randomAlphanumeric(length: number): string {
  return randomString(length, ALPHANUMERIC_CHARS);
}

export function randomNumeric(length: number): string {
  return randomString(length, DIGIT_CHARS);
}

export function randomAlphabetic(length: number): string {
  return randomString(length, LOWERCASE_CHARS + UPPERCASE_CHARS);
}

export function randomPassword(length: number = 16): string {
  if (length < 4) {
    length = 4;
  }
  let result = '';
  result += randomString(1, UPPERCASE_CHARS);
  result += randomString(1, LOWERCASE_CHARS);
  result += randomString(1, DIGIT_CHARS);
  result += randomString(1, SPECIAL_CHARS);
  result += randomString(length - 4, ALPHANUMERIC_CHARS + SPECIAL_CHARS);
  return shuffleString(result);
}

function shuffleString(str: string): string {
  const arr = str.split('');
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.join('');
}

// ============================================
// Utility Functions
// ============================================

export function reverse(str: string | null | undefined): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str.split('').reverse().join('');
}

export function repeat(str: string | null | undefined, count: number): string {
  if (str === null || str === undefined) {
    return '';
  }
  if (count <= 0) {
    return '';
  }
  return str.repeat(count);
}

export function defaultIfBlank(str: string | null | undefined, defaultValue: string): string {
  return isBlank(str) ? defaultValue : str!;
}

export function defaultIfEmpty(str: string | null | undefined, defaultValue: string): string {
  return isEmpty(str) ? defaultValue : str!;
}

export function equals(str1: string | null | undefined, str2: string | null | undefined, ignoreCase: boolean = false): boolean {
  if (str1 === null || str1 === undefined) {
    return str2 === null || str2 === undefined;
  }
  if (str2 === null || str2 === undefined) {
    return false;
  }
  if (ignoreCase) {
    return str1.toLowerCase() === str2.toLowerCase();
  }
  return str1 === str2;
}

export function slugify(str: string | null | undefined, separator: string = '-'): string {
  if (str === null || str === undefined) {
    return '';
  }
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, separator)
    .replace(new RegExp(`^${separator}+|${separator}+$`, 'g'), '');
}

// ============================================
// StringUtils Class (Alternative API)
// ============================================

export class StringUtils {
  static isBlank = isBlank;
  static isNotBlank = isNotBlank;
  static isEmpty = isEmpty;
  static trim = trim;
  static trimLeft = trimLeft;
  static trimRight = trimRight;
  static removeWhitespace = removeWhitespace;
  static normalizeWhitespace = normalizeWhitespace;
  static toLowerCase = toLowerCase;
  static toUpperCase = toUpperCase;
  static capitalize = capitalize;
  static uncapitalize = uncapitalize;
  static toTitleCase = toTitleCase;
  static toCamelCase = toCamelCase;
  static toPascalCase = toPascalCase;
  static toSnakeCase = toSnakeCase;
  static toKebabCase = toKebabCase;
  static truncate = truncate;
  static substringBetween = substringBetween;
  static substringAfter = substringAfter;
  static substringBefore = substringBefore;
  static substringAfterLast = substringAfterLast;
  static substringBeforeLast = substringBeforeLast;
  static startsWith = startsWith;
  static endsWith = endsWith;
  static removePrefix = removePrefix;
  static removeSuffix = removeSuffix;
  static isValidEmail = isValidEmail;
  static isValidUrl = isValidUrl;
  static isNumeric = isNumeric;
  static isInteger = isInteger;
  static isAlpha = isAlpha;
  static isAlphanumeric = isAlphanumeric;
  static padLeft = padLeft;
  static padRight = padRight;
  static center = center;
  static contains = contains;
  static countMatches = countMatches;
  static replaceAll = replaceAll;
  static split = split;
  static lines = lines;
  static join = join;
  static base64Encode = base64Encode;
  static base64Decode = base64Decode;
  static urlEncode = urlEncode;
  static urlDecode = urlDecode;
  static randomString = randomString;
  static randomAlphanumeric = randomAlphanumeric;
  static randomNumeric = randomNumeric;
  static randomAlphabetic = randomAlphabetic;
  static randomPassword = randomPassword;
  static reverse = reverse;
  static repeat = repeat;
  static defaultIfBlank = defaultIfBlank;
  static defaultIfEmpty = defaultIfEmpty;
  static equals = equals;
  static slugify = slugify;
}

export default StringUtils;
