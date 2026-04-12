/**
 * String Utilities Module for TypeScript - OPTIMIZED VERSION
 * 
 * Performance improvements, bug fixes, and enhanced boundary handling.
 * 
 * Changes:
 * - Cached regex patterns to avoid recompilation
 * - Optimized splitWords with single-pass parsing
 * - Fixed truncate edge cases (negative length, empty strings)
 * - Improved escape functions with Map lookups
 * - Added input validation for all public functions
 * - Optimized levenshtein with space-efficient algorithm
 * - Better Unicode handling throughout
 * 
 * @module string_utils
 * @version 1.1.0
 * @license MIT
 */

export type CaseStyle = 
  | 'camelCase'
  | 'PascalCase'
  | 'snake_case'
  | 'SCREAMING_SNAKE'
  | 'kebab-case'
  | 'SCREAMING-KEBAB'
  | 'dot.case'
  | 'space case'
  | 'Title Case';

export interface TruncateOptions {
  length: number;
  suffix?: string;
  preserveWords?: boolean;
}

export interface PadOptions {
  length: number;
  char?: string;
  position?: 'left' | 'right' | 'both';
}

export interface TemplateOptions {
  prefix?: string;
  suffix?: string;
  escapeChar?: string;
}

export interface EscapeOptions {
  escapeHtml?: boolean;
  escapeJson?: boolean;
  escapeXml?: boolean;
  escapeSql?: boolean;
}

export interface CharAnalysis {
  total: number;
  letters: number;
  digits: number;
  spaces: number;
  punctuation: number;
  uppercase: number;
  lowercase: number;
  special: number;
  unicode: number;
}

export interface SplitOptions {
  separator?: string | RegExp;
  limit?: number;
  trim?: boolean;
  removeEmpty?: boolean;
}

// =============================================================================
// CACHED REGEX PATTERNS (Performance optimization)
// =============================================================================

const PATTERNS = {
  camelCase: /([a-z])([A-Z])/g,
  multiSeparator: /[_\-\. ]+/g,
  numberSeparator: /\d+/g,
  whitespace: /^\s+|\s+$/g,
  whitespaceLeft: /^\s+/,
  whitespaceRight: /\s+$/,
  url: /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi,
  email: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
  phone: /(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}/g,
  hashtag: /#(\w+)/g,
  mention: /@(\w+)/g,
  digits: /\d+/g,
  specialChars: /[^\p{L}\p{N}]/gu,
  alpha: /^\p{L}+$/u,
  alphanumeric: /^[\p{L}\p{N}]+$/u,
  numeric: /^\p{N}+$/u,
  integer: /^-?\d+$/,
  float: /^-?\d*\.?\d+$/,
  base64: /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/,
} as const;

// Escape maps (using Map for O(1) lookups)
const HTML_ESCAPE_MAP = new Map([
  ['&', '&amp;'],
  ['<', '&lt;'],
  ['>', '&gt;'],
  ['"', '&quot;'],
  ["'", '&#39;'],
  ['/', '&#x2F;'],
]);

const HTML_UNESCAPE_MAP = new Map([
  ['&amp;', '&'],
  ['&lt;', '<'],
  ['&gt;', '>'],
  ['&quot;', '"'],
  ['&#39;', "'"],
  ['&#x2F;', '/'],
]);

const CASE_CONVERTERS: Record<CaseStyle, (s: string) => string> = {
  'camelCase': toCamelCase,
  'PascalCase': toPascalCase,
  'snake_case': toSnakeCase,
  'SCREAMING_SNAKE': toScreamingSnake,
  'kebab-case': toKebabCase,
  'SCREAMING-KEBAB': toScreamingKebab,
  'dot.case': toDotCase,
  'space case': toSpaceCase,
  'Title Case': toTitleCase,
};

// =============================================================================
// Case Conversion
// =============================================================================

/**
 * Split a string into words - OPTIMIZED single-pass implementation
 */
export function splitWords(str: string): string[] {
  if (!str) return [];
  
  const len = str.length;
  if (len === 0) return [];
  
  const words: string[] = [];
  let current = '';
  
  for (let i = 0; i < len; i++) {
    const char = str[i];
    const nextChar = str[i + 1];
    
    // Handle camelCase/PascalCase boundaries
    if (char >= 'A' && char <= 'Z' && i > 0 && nextChar && nextChar >= 'a' && nextChar <= 'z') {
      if (current) {
        words.push(current);
        current = '';
      }
    }
    
    // Handle separators
    if (char === '_' || char === '-' || char === '.' || char === ' ') {
      if (current) {
        words.push(current);
        current = '';
      }
      continue;
    }
    
    // Handle number boundaries
    const isDigit = char >= '0' && char <= '9';
    const prevIsDigit = i > 0 && str[i - 1] >= '0' && str[i - 1] <= '9';
    
    if (isDigit !== prevIsDigit && current) {
      words.push(current);
      current = '';
    }
    
    current += char;
  }
  
  if (current) {
    words.push(current);
  }
  
  return words.filter(w => w.length > 0).map(w => w.toLowerCase());
}

export function toCamelCase(str: string): string {
  if (!str) return '';
  const words = splitWords(str);
  if (words.length === 0) return '';
  
  let result = words[0];
  for (let i = 1; i < words.length; i++) {
    const word = words[i];
    result += word.charAt(0).toUpperCase() + word.slice(1);
  }
  return result;
}

export function toPascalCase(str: string): string {
  if (!str) return '';
  const words = splitWords(str);
  return words.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('');
}

export function toSnakeCase(str: string): string {
  if (!str) return '';
  return splitWords(str).join('_');
}

export function toScreamingSnake(str: string): string {
  if (!str) return '';
  return splitWords(str).join('_').toUpperCase();
}

export function toKebabCase(str: string): string {
  if (!str) return '';
  return splitWords(str).join('-');
}

export function toScreamingKebab(str: string): string {
  if (!str) return '';
  return splitWords(str).join('-').toUpperCase();
}

export function toDotCase(str: string): string {
  if (!str) return '';
  return splitWords(str).join('.');
}

export function toSpaceCase(str: string): string {
  if (!str) return '';
  return splitWords(str).join(' ');
}

export function toTitleCase(str: string): string {
  if (!str) return '';
  const words = splitWords(str);
  return words.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

export function toCase(str: string, style: CaseStyle): string {
  if (!str) return '';
  const converter = CASE_CONVERTERS[style];
  return converter ? converter(str) : str;
}

// =============================================================================
// Trimming and Padding
// =============================================================================

export function trim(str: string): string {
  return str ? str.trim() : '';
}

export function trimLeft(str: string): string {
  return str ? str.replace(PATTERNS.whitespaceLeft, '') : '';
}

export function trimRight(str: string): string {
  return str ? str.replace(PATTERNS.whitespaceRight, '') : '';
}

export function trimChars(str: string, chars: string): string {
  if (!str || !chars) return str || '';
  
  let start = 0;
  let end = str.length;
  
  while (start < end && chars.includes(str[start])) start++;
  while (end > start && chars.includes(str[end - 1])) end--;
  
  return str.slice(start, end);
}

export function pad(str: string, options: PadOptions): string {
  const { length, char = ' ', position = 'left' } = options;
  
  if (!str || length <= 0 || str.length >= length) return str || '';
  if (!char) return str;
  
  const padLength = length - str.length;
  
  switch (position) {
    case 'left':
      return char.repeat(padLength) + str;
    case 'right':
      return str + char.repeat(padLength);
    case 'both': {
      const leftPad = Math.floor(padLength / 2);
      const rightPad = padLength - leftPad;
      return char.repeat(leftPad) + str + char.repeat(rightPad);
    }
    default:
      return str;
  }
}

export function padLeft(str: string, length: number, char: string = ' '): string {
  return pad(str, { length, char, position: 'left' });
}

export function padRight(str: string, length: number, char: string = ' '): string {
  return pad(str, { length, char, position: 'right' });
}

export function padBoth(str: string, length: number, char: string = ' '): string {
  return pad(str, { length, char, position: 'both' });
}

export function zeroPad(num: number | string, length: number): string {
  return padLeft(String(num ?? ''), length, '0');
}

// =============================================================================
// Truncation - FIXED boundary handling
// =============================================================================

export function truncate(str: string, options: TruncateOptions): string {
  const { length, suffix = '...', preserveWords = false } = options;
  
  // Boundary fixes
  if (!str || str.length === 0) return '';
  if (length <= 0) return suffix.slice(0, Math.max(0, length));
  if (length >= str.length) return str;
  
  const maxLength = length - suffix.length;
  if (maxLength <= 0) return suffix.slice(0, length);
  
  if (preserveWords) {
    const truncated = str.slice(0, maxLength);
    const lastSpace = truncated.lastIndexOf(' ');
    if (lastSpace > 0) {
      return truncated.slice(0, lastSpace) + suffix;
    }
    return truncated + suffix;
  }
  
  return str.slice(0, maxLength) + suffix;
}

export function truncateWords(str: string, wordCount: number, suffix: string = '...'): string {
  if (!str || wordCount <= 0) return suffix;
  
  const words = str.trim().split(/\s+/);
  if (words.length <= wordCount) return str;
  return words.slice(0, wordCount).join(' ') + suffix;
}

// =============================================================================
// Template Interpolation
// =============================================================================

export function interpolate(
  template: string, 
  data: Record<string, unknown>, 
  options: TemplateOptions = {}
): string {
  if (!template) return '';
  if (!data || typeof data !== 'object') return template;
  
  const { prefix = '{{', suffix = '}}' } = options;
  
  if (!prefix || !suffix) return template;
  
  const escapedPrefix = prefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapedSuffix = suffix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  const pattern = new RegExp(`${escapedPrefix}([^${escapedSuffix}]+)${escapedSuffix}`, 'g');
  
  return template.replace(pattern, (_, key) => {
    const trimmedKey = key.trim();
    const value = data[trimmedKey];
    return value !== undefined && value !== null ? String(value) : '';
  });
}

export function format(formatStr: string, ...args: unknown[]): string {
  if (!formatStr) return '';
  return formatStr.replace(/{(\d+)}/g, (_, index) => {
    const idx = parseInt(index, 10);
    return idx >= 0 && idx < args.length ? String(args[idx]) : '';
  });
}

// =============================================================================
// Escaping and Unescaping - OPTIMIZED with Map lookups
// =============================================================================

export function escapeHtml(str: string): string {
  if (!str) return '';
  return str.replace(/[&<>"'/]/g, char => HTML_ESCAPE_MAP.get(char) || char);
}

export function unescapeHtml(str: string): string {
  if (!str) return '';
  return str.replace(/&amp;|&lt;|&gt;|&quot;|&#39;|&#x2F;/g, entity => HTML_UNESCAPE_MAP.get(entity) || entity);
}

export function escapeJson(str: string): string {
  if (!str) return '';
  return str.replace(/["\\\b\f\n\r\t]/g, char => {
    const map: Record<string, string> = {
      '"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f',
      '\n': '\\n', '\r': '\\r', '\t': '\\t',
    };
    return map[char] || char;
  });
}

export function unescapeJson(str: string): string {
  if (!str) return '';
  const map: Record<string, string> = {
    '\\"': '"', '\\\\': '\\', '\\b': '\b', '\\f': '\f',
    '\\n': '\n', '\\r': '\r', '\\t': '\t',
  };
  return str.replace(/\\"|\\\\|\\b|\\f|\\n|\\r|\\t/g, seq => map[seq] || seq);
}

export function escapeXml(str: string): string {
  if (!str) return '';
  return str.replace(/[&<>"']/g, char => {
    const map: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' };
    return map[char] || char;
  });
}

export function escapeSql(str: string): string {
  return str ? str.replace(/'/g, "''") : '';
}

export function escapeRegExp(str: string): string {
  return str ? str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') : '';
}

export function escape(str: string, options: EscapeOptions = {}): string {
  if (!str) return '';
  let result = str;
  
  if (options.escapeHtml) result = escapeHtml(result);
  if (options.escapeJson) result = escapeJson(result);
  if (options.escapeXml) result = escapeXml(result);
  if (options.escapeSql) result = escapeSql(result);
  
  return result;
}

// =============================================================================
// Pattern Matching and Extraction
// =============================================================================

export function extractUrls(str: string): string[] {
  if (!str) return [];
  return str.match(PATTERNS.url) || [];
}

export function extractEmails(str: string): string[] {
  if (!str) return [];
  return str.match(PATTERNS.email) || [];
}

export function extractPhoneNumbers(str: string): string[] {
  if (!str) return [];
  return str.match(PATTERNS.phone) || [];
}

export function extractHashtags(str: string): string[] {
  if (!str) return [];
  return Array.from(str.matchAll(PATTERNS.hashtag), m => m[1]);
}

export function extractMentions(str: string): string[] {
  if (!str) return [];
  return Array.from(str.matchAll(PATTERNS.mention), m => m[1]);
}

export function extractNumbers(str: string, asFloat: boolean = false): number[] {
  if (!str) return [];
  const pattern = asFloat ? /-?\d+\.?\d*/g : /-?\d+/g;
  const matches = str.match(pattern);
  return matches ? matches.map(Number).filter(n => !isNaN(n)) : [];
}

export function extractBetween(
  str: string, 
  start: string, 
  end: string, 
  includeDelimiters: boolean = false
): string[] {
  if (!str || !start || !end) return [];
  
  const escapedStart = escapeRegExp(start);
  const escapedEnd = escapeRegExp(end);
  const pattern = includeDelimiters 
    ? new RegExp(`(${escapedStart}.*?${escapedEnd})`, 'g')
    : new RegExp(`${escapedStart}(.*?)${escapedEnd}`, 'g');
  
  return Array.from(str.matchAll(pattern), m => includeDelimiters ? m[0] : m[1]);
}

// =============================================================================
// Character Analysis - OPTIMIZED single-pass
// =============================================================================

export function analyzeChars(str: string): CharAnalysis {
  const result: CharAnalysis = {
    total: str?.length || 0,
    letters: 0, digits: 0, spaces: 0, punctuation: 0,
    uppercase: 0, lowercase: 0, special: 0, unicode: 0,
  };
  
  if (!str) return result;
  
  for (const char of str) {
    const code = char.codePointAt(0) || 0;
    
    if (/\p{L}/u.test(char)) {
      result.letters++;
      if (/\p{Lu}/u.test(char)) result.uppercase++;
      else if (/\p{Ll}/u.test(char)) result.lowercase++;
      if (code > 127) result.unicode++;
    } else if (/\d/.test(char)) {
      result.digits++;
    } else if (/\s/.test(char)) {
      result.spaces++;
    } else if (/\p{P}/u.test(char)) {
      result.punctuation++;
    } else {
      result.special++;
    }
  }
  
  return result;
}

export function countOccurrences(str: string, substring: string, caseSensitive: boolean = true): number {
  if (!str || !substring) return 0;
  
  const source = caseSensitive ? str : str.toLowerCase();
  const search = caseSensitive ? substring : substring.toLowerCase();
  
  let count = 0;
  let pos = 0;
  
  while ((pos = source.indexOf(search, pos)) !== -1) {
    count++;
    pos += search.length;
  }
  
  return count;
}

export function isAlpha(str: string): boolean {
  return str ? PATTERNS.alpha.test(str) : false;
}

export function isAlphanumeric(str: string): boolean {
  return str ? PATTERNS.alphanumeric.test(str) : false;
}

export function isNumeric(str: string): boolean {
  return str ? PATTERNS.numeric.test(str) : false;
}

export function isInteger(str: string): boolean {
  return str ? PATTERNS.integer.test(str) : false;
}

export function isFloat(str: string): boolean {
  return str ? PATTERNS.float.test(str) : false;
}

// =============================================================================
// String Manipulation
// =============================================================================

export function reverse(str: string): string {
  if (!str) return '';
  return Array.from(str).reverse().join('');
}

export function removeWhitespace(str: string): string {
  return str ? str.replace(/\s+/g, '') : '';
}

export function removeDigits(str: string): string {
  return str ? str.replace(PATTERNS.digits, '') : '';
}

export function removeSpecialChars(str: string): string {
  return str ? str.replace(PATTERNS.specialChars, '') : '';
}

export function replaceAll(
  str: string, 
  search: string, 
  replace: string, 
  caseSensitive: boolean = true
): string {
  if (!str || !search) return str || '';
  
  if (caseSensitive) {
    return str.split(search).join(replace);
  }
  
  const escaped = escapeRegExp(search);
  const pattern = new RegExp(escaped, 'gi');
  return str.replace(pattern, replace);
}

export function insertAt(str: string, substring: string, position: number): string {
  if (!str) return substring || '';
  if (position < 0) position = 0;
  if (position > str.length) position = str.length;
  return str.slice(0, position) + (substring || '') + str.slice(position);
}

export function removeAt(str: string, start: number, length: number = 1): string {
  if (!str || start < 0) return str || '';
  if (start >= str.length) return str;
  return str.slice(0, start) + str.slice(start + length);
}

export function repeat(str: string, count: number, separator?: string): string {
  if (!str || count <= 0) return '';
  if (!separator) return str.repeat(count);
  return Array(count).fill(str).join(separator);
}

export function charRepeat(char: string, length: number): string {
  return (char || '').repeat(Math.max(0, length));
}

// =============================================================================
// Splitting and Joining
// =============================================================================

export function split(str: string, options: SplitOptions = {}): string[] {
  const { 
    separator = ',', 
    limit, 
    trim = false, 
    removeEmpty = false 
  } = options;
  
  if (!str) return [];
  
  let parts: string[] = separator instanceof RegExp 
    ? str.split(separator, limit) 
    : str.split(separator, limit);
  
  if (trim) parts = parts.map(p => p.trim());
  if (removeEmpty) parts = parts.filter(p => p.length > 0);
  
  return parts;
}

export function chunk(str: string, chunkSize: number): string[] {
  if (!str || chunkSize <= 0) return [str || ''];
  
  const chunks: string[] = [];
  for (let i = 0; i < str.length; i += chunkSize) {
    chunks.push(str.slice(i, i + chunkSize));
  }
  return chunks;
}

export function joinGrammar(
  items: string[], 
  options: { conjunction?: string; oxfordComma?: boolean } = {}
): string {
  if (!items || items.length === 0) return '';
  if (items.length === 1) return items[0];
  
  const { conjunction = 'and', oxfordComma = true } = options;
  
  if (items.length === 2) return `${items[0]} ${conjunction} ${items[1]}`;
  
  const last = items[items.length - 1];
  const rest = items.slice(0, -1);
  const comma = oxfordComma ? ',' : '';
  
  return `${rest.join(', ')}${comma} ${conjunction} ${last}`;
}

// =============================================================================
// Encoding Utilities
// =============================================================================

export function toBase64(str: string): string {
  if (!str) return '';
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(str, 'utf-8').toString('base64');
  }
  return btoa(unescape(encodeURIComponent(str)));
}

export function fromBase64(str: string): string {
  if (!str) return '';
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(str, 'base64').toString('utf-8');
  }
  return decodeURIComponent(escape(atob(str)));
}

export function toBase64Url(str: string): string {
  return toBase64(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function fromBase64Url(str: string): string {
  if (!str) return '';
  const base64 = str.replace(/-/g, '+').replace(/_/g, '/');
  const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=');
  return fromBase64(padded);
}

export function encodeUrl(str: string): string {
  return str ? encodeURIComponent(str) : '';
}

export function decodeUrl(str: string): string {
  return str ? decodeURIComponent(str) : '';
}

// =============================================================================
// Comparison and Similarity
// =============================================================================

export function equals(str1: string, str2: string, caseSensitive: boolean = false): boolean {
  if (!str1 || !str2) return false;
  return caseSensitive ? str1 === str2 : str1.toLowerCase() === str2.toLowerCase();
}

export function startsWith(str: string, prefix: string, caseSensitive: boolean = true): boolean {
  if (!str || !prefix) return false;
  if (!caseSensitive) return str.toLowerCase().startsWith(prefix.toLowerCase());
  return str.startsWith(prefix);
}

export function endsWith(str: string, suffix: string, caseSensitive: boolean = true): boolean {
  if (!str || !suffix) return false;
  if (!caseSensitive) return str.toLowerCase().endsWith(suffix.toLowerCase());
  return str.endsWith(suffix);
}

export function contains(str: string, substring: string, caseSensitive: boolean = true): boolean {
  if (!str || !substring) return false;
  if (!caseSensitive) return str.toLowerCase().includes(substring.toLowerCase());
  return str.includes(substring);
}

/**
 * Levenshtein distance - OPTIMIZED space-efficient version (O(n) space)
 */
export function levenshtein(str1: string, str2: string): number {
  if (!str1) return str2?.length || 0;
  if (!str2) return str1.length;
  
  const m = str1.length;
  const n = str2.length;
  
  // Use two rows instead of full matrix for O(n) space
  let prev = new Array(n + 1).fill(0);
  let curr = new Array(n + 1).fill(0);
  
  for (let j = 0; j <= n; j++) prev[j] = j;
  
  for (let i = 1; i <= m; i++) {
    curr[0] = i;
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        curr[j] = prev[j - 1];
      } else {
        curr[j] = 1 + Math.min(prev[j], curr[j - 1], prev[j - 1]);
      }
    }
    [prev, curr] = [curr, prev];
  }
  
  return prev[n];
}

export function similarity(str1: string, str2: string): number {
  const maxLen = Math.max(str1?.length || 0, str2?.length || 0);
  if (maxLen === 0) return 1;
  
  const distance = levenshtein(str1, str2);
  return 1 - distance / maxLen;
}

export function longestCommonSubstring(str1: string, str2: string): string {
  if (!str1 || !str2) return '';
  
  const m = str1.length;
  const n = str2.length;
  
  let maxLength = 0;
  let endPos = 0;
  
  // Use two rows for space efficiency
  let prev = new Array(n + 1).fill(0);
  let curr = new Array(n + 1).fill(0);
  
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        curr[j] = prev[j - 1] + 1;
        if (curr[j] > maxLength) {
          maxLength = curr[j];
          endPos = i;
        }
      } else {
        curr[j] = 0;
      }
    }
    [prev, curr] = [curr, prev];
  }
  
  return str1.slice(endPos - maxLength, endPos);
}

// =============================================================================
// Utility Functions
// =============================================================================

export function randomString(length: number, charset?: string): string {
  if (length <= 0) return '';
  
  const chars = charset || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charsLen = chars.length;
  let result = '';
  
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    const values = new Uint32Array(length);
    crypto.getRandomValues(values);
    for (let i = 0; i < length; i++) {
      result += chars[values[i] % charsLen];
    }
  } else {
    for (let i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * charsLen)];
    }
  }
  
  return result;
}

export function slugify(
  str: string, 
  options: { lowercase?: boolean; separator?: string; removeSpecial?: boolean } = {}
): string {
  if (!str) return '';
  
  const { lowercase = true, separator = '-', removeSpecial = true } = options;
  
  let result = str;
  
  if (lowercase) result = result.toLowerCase();
  result = result.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  
  if (removeSpecial) result = result.replace(/[^\w\s-]/g, '');
  
  result = result.replace(/[\s_]+/g, separator)
    .replace(new RegExp(`${separator}+`, 'g'), separator)
    .replace(new RegExp(`^${separator}+|${separator}+$`, 'g'), '');
  
  return result;
}

export function isEmpty(str: string): boolean {
  return !str || str.trim().length === 0;
}

export function isNotEmpty(str: string): boolean {
  return !isEmpty(str);
}

export function ensureMinLength(str: string, minLength: number, padChar: string = ' '): string {
  if (!str) return padChar.repeat(Math.max(0, minLength));
  if (str.length >= minLength) return str;
  return padRight(str, minLength, padChar);
}

export function ensureMaxLength(str: string, maxLength: number, suffix: string = ''): string {
  if (!str) return '';
  if (str.length <= maxLength) return str;
  return truncate(str, { length: maxLength, suffix });
}

export function capitalize(str: string): string {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function capitalizeWords(str: string): string {
  return str ? str.replace(/\b\w/g, char => char.toUpperCase()) : '';
}

export function decapitalize(str: string): string {
  if (!str) return '';
  return str.charAt(0).toLowerCase() + str.slice(1);
}

// =============================================================================
// Default Export
// =============================================================================

export default {
  splitWords, toCamelCase, toPascalCase, toSnakeCase, toScreamingSnake,
  toKebabCase, toScreamingKebab, toDotCase, toSpaceCase, toTitleCase, toCase,
  trim, trimLeft, trimRight, trimChars, pad, padLeft, padRight, padBoth, zeroPad,
  truncate, truncateWords,
  interpolate, format,
  escapeHtml, unescapeHtml, escapeJson, unescapeJson, escapeXml, escapeSql, escapeRegExp, escape,
  extractUrls, extractEmails, extractPhoneNumbers, extractHashtags, extractMentions, extractNumbers, extractBetween,
  analyzeChars, countOccurrences, isAlpha, isAlphanumeric, isNumeric, isInteger, isFloat,
  reverse, removeWhitespace, removeDigits, removeSpecialChars, replaceAll, insertAt, removeAt, repeat, charRepeat,
  split, chunk, joinGrammar,
  toBase64, fromBase64, toBase64Url, fromBase64Url, encodeUrl, decodeUrl,
  equals, startsWith, endsWith, contains, levenshtein, similarity, longestCommonSubstring,
  randomString, slugify, isEmpty, isNotEmpty, ensureMinLength, ensureMaxLength, capitalize, capitalizeWords, decapitalize,
};
