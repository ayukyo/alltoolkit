/**
 * String Utilities Module for TypeScript
 * 
 * A comprehensive string manipulation utility module with zero dependencies.
 * Provides common string operations, transformations, validations, and formatting.
 * 
 * Features:
 * - Case conversion (camelCase, PascalCase, snake_case, kebab-case, etc.)
 * - String trimming and padding
 * - Truncation and ellipsis
 * - Template interpolation
 * - String escaping and unescaping
 * - Pattern matching and extraction
 * - Character counting and analysis
 * - Encoding utilities
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module string_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Case conversion options
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

/**
 * Truncation options
 */
export interface TruncateOptions {
  length: number;
  suffix?: string;
  preserveWords?: boolean;
}

/**
 * Pad options
 */
export interface PadOptions {
  length: number;
  char?: string;
  position?: 'left' | 'right' | 'both';
}

/**
 * Template options
 */
export interface TemplateOptions {
  prefix?: string;
  suffix?: string;
  escapeChar?: string;
}

/**
 * Escape/unescape options
 */
export interface EscapeOptions {
  escapeHtml?: boolean;
  escapeJson?: boolean;
  escapeXml?: boolean;
  escapeSql?: boolean;
}

/**
 * Character analysis result
 */
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

/**
 * Split options
 */
export interface SplitOptions {
  separator?: string | RegExp;
  limit?: number;
  trim?: boolean;
  removeEmpty?: boolean;
}

// =============================================================================
// Case Conversion
// =============================================================================

/**
 * Split a string into words by various separators
 * @param str - Input string
 * @returns Array of words
 */
export function splitWords(str: string): string[] {
  // Replace common separators with spaces
  let normalized = str
    .replace(/([a-z])([A-Z])/g, '$1 $2')  // camelCase -> camel Case
    .replace(/([A-Z])([A-Z][a-z])/g, '$1 $2')  // HTTPServer -> HTTP Server
    .replace(/[_\-\. ]+/g, ' ')  // snake, kebab, dot, space -> space
    .replace(/\d+/g, ' $& ');  // Numbers as separate words
  
  // Split and filter empty strings
  return normalized.trim().split(/\s+/).filter(word => word.length > 0);
}

/**
 * Convert string to camelCase
 * @param str - Input string
 * @returns camelCase string
 * @example
 * ```typescript
 * toCamelCase("hello_world") // "helloWorld"
 * toCamelCase("Hello-World") // "helloWorld"
 * toCamelCase("hello world") // "helloWorld"
 * ```
 */
export function toCamelCase(str: string): string {
  const words = splitWords(str);
  if (words.length === 0) return '';
  
  return words[0].toLowerCase() + 
    words.slice(1).map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join('');
}

/**
 * Convert string to PascalCase (UpperCamelCase)
 * @param str - Input string
 * @returns PascalCase string
 * @example
 * ```typescript
 * toPascalCase("hello_world") // "HelloWorld"
 * toPascalCase("hello-world") // "HelloWorld"
 * ```
 */
export function toPascalCase(str: string): string {
  const words = splitWords(str);
  return words.map(word => 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join('');
}

/**
 * Convert string to snake_case
 * @param str - Input string
 * @returns snake_case string
 * @example
 * ```typescript
 * toSnakeCase("helloWorld") // "hello_world"
 * toSnakeCase("HelloWorld") // "hello_world"
 * ```
 */
export function toSnakeCase(str: string): string {
  const words = splitWords(str);
  return words.map(word => word.toLowerCase()).join('_');
}

/**
 * Convert string to SCREAMING_SNAKE_CASE
 * @param str - Input string
 * @returns SCREAMING_SNAKE_CASE string
 * @example
 * ```typescript
 * toScreamingSnake("helloWorld") // "HELLO_WORLD"
 * ```
 */
export function toScreamingSnake(str: string): string {
  const words = splitWords(str);
  return words.map(word => word.toUpperCase()).join('_');
}

/**
 * Convert string to kebab-case
 * @param str - Input string
 * @returns kebab-case string
 * @example
 * ```typescript
 * toKebabCase("helloWorld") // "hello-world"
 * ```
 */
export function toKebabCase(str: string): string {
  const words = splitWords(str);
  return words.map(word => word.toLowerCase()).join('-');
}

/**
 * Convert string to SCREAMING-KEBAB-CASE
 * @param str - Input string
 * @returns SCREAMING-KEBAB-CASE string
 * @example
 * ```typescript
 * toScreamingKebab("helloWorld") // "HELLO-WORLD"
 * ```
 */
export function toScreamingKebab(str: string): string {
  const words = splitWords(str);
  return words.map(word => word.toUpperCase()).join('-');
}

/**
 * Convert string to dot.case
 * @param str - Input string
 * @returns dot.case string
 * @example
 * ```typescript
 * toDotCase("helloWorld") // "hello.world"
 * ```
 */
export function toDotCase(str: string): string {
  const words = splitWords(str);
  return words.map(word => word.toLowerCase()).join('.');
}

/**
 * Convert string to space case
 * @param str - Input string
 * @returns space case string
 * @example
 * ```typescript
 * toSpaceCase("helloWorld") // "hello world"
 * ```
 */
export function toSpaceCase(str: string): string {
  const words = splitWords(str);
  return words.map(word => word.toLowerCase()).join(' ');
}

/**
 * Convert string to Title Case
 * @param str - Input string
 * @returns Title Case string
 * @example
 * ```typescript
 * toTitleCase("hello world") // "Hello World"
 * ```
 */
export function toTitleCase(str: string): string {
  const words = splitWords(str);
  return words.map(word => 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ');
}

/**
 * Convert string to specified case style
 * @param str - Input string
 * @param style - Target case style
 * @returns Converted string
 * @example
 * ```typescript
 * toCase("hello_world", "camelCase") // "helloWorld"
 * toCase("helloWorld", "snake_case") // "hello_world"
 * ```
 */
export function toCase(str: string, style: CaseStyle): string {
  const converters: Record<CaseStyle, (s: string) => string> = {
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
  
  return converters[style](str);
}

// =============================================================================
// Trimming and Padding
// =============================================================================

/**
 * Trim whitespace from both ends of a string
 * @param str - Input string
 * @returns Trimmed string
 */
export function trim(str: string): string {
  return str.trim();
}

/**
 * Trim whitespace from the left side of a string
 * @param str - Input string
 * @returns Left-trimmed string
 */
export function trimLeft(str: string): string {
  return str.replace(/^\s+/, '');
}

/**
 * Trim whitespace from the right side of a string
 * @param str - Input string
 * @returns Right-trimmed string
 */
export function trimRight(str: string): string {
  return str.replace(/\s+$/, '');
}

/**
 * Trim specific characters from both ends of a string
 * @param str - Input string
 * @param chars - Characters to trim
 * @returns Trimmed string
 * @example
 * ```typescript
 * trimChars("###hello###", "#") // "hello"
 * ```
 */
export function trimChars(str: string, chars: string): string {
  const escaped = chars.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`^[${escaped}]+|[${escaped}]+$`, 'g');
  return str.replace(pattern, '');
}

/**
 * Pad a string to the specified length
 * @param str - Input string
 * @param options - Pad options
 * @returns Padded string
 * @example
 * ```typescript
 * pad("5", { length: 3, char: "0", position: "left" }) // "005"
 * pad("hi", { length: 5, char: "-", position: "right" }) // "hi---"
 * pad("x", { length: 5, char: "*", position: "both" }) // "**x**"
 * ```
 */
export function pad(str: string, options: PadOptions): string {
  const { length, char = ' ', position = 'left' } = options;
  
  if (str.length >= length) return str;
  if (!char) return str;
  
  const padLength = length - str.length;
  
  switch (position) {
    case 'left':
      return char.repeat(padLength) + str;
    case 'right':
      return str + char.repeat(padLength);
    case 'both':
      const leftPad = Math.floor(padLength / 2);
      const rightPad = padLength - leftPad;
      return char.repeat(leftPad) + str + char.repeat(rightPad);
    default:
      return str;
  }
}

/**
 * Pad a string on the left to the specified length
 * @param str - Input string
 * @param length - Target length
 * @param char - Padding character (default: space)
 * @returns Padded string
 */
export function padLeft(str: string, length: number, char: string = ' '): string {
  return pad(str, { length, char, position: 'left' });
}

/**
 * Pad a string on the right to the specified length
 * @param str - Input string
 * @param length - Target length
 * @param char - Padding character (default: space)
 * @returns Padded string
 */
export function padRight(str: string, length: number, char: string = ' '): string {
  return pad(str, { length, char, position: 'right' });
}

/**
 * Pad a string on both sides to the specified length
 * @param str - Input string
 * @param length - Target length
 * @param char - Padding character (default: space)
 * @returns Padded string
 */
export function padBoth(str: string, length: number, char: string = ' '): string {
  return pad(str, { length, char, position: 'both' });
}

/**
 * Zero-pad a number string
 * @param num - Number or string to pad
 * @param length - Target length
 * @returns Zero-padded string
 * @example
 * ```typescript
 * zeroPad(5, 3) // "005"
 * zeroPad("42", 4) // "0042"
 * ```
 */
export function zeroPad(num: number | string, length: number): string {
  return padLeft(String(num), length, '0');
}

// =============================================================================
// Truncation
// =============================================================================

/**
 * Truncate a string to specified length with ellipsis
 * @param str - Input string
 * @param options - Truncation options
 * @returns Truncated string
 * @example
 * ```typescript
 * truncate("Hello World", { length: 8 }) // "Hello..."
 * truncate("Hello World", { length: 8, suffix: " [more]" }) // "Hello [more]"
 * truncate("Hello World", { length: 8, preserveWords: true }) // "Hello..."
 * ```
 */
export function truncate(str: string, options: TruncateOptions): string {
  const { length, suffix = '...', preserveWords = false } = options;
  
  if (str.length <= length) return str;
  
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

/**
 * Truncate string to fit within a word limit
 * @param str - Input string
 * @param wordCount - Maximum number of words
 * @param suffix - Suffix to add if truncated
 * @returns Truncated string
 * @example
 * ```typescript
 * truncateWords("Hello world this is a test", 3) // "Hello world this..."
 * ```
 */
export function truncateWords(str: string, wordCount: number, suffix: string = '...'): string {
  const words = str.trim().split(/\s+/);
  if (words.length <= wordCount) return str;
  return words.slice(0, wordCount).join(' ') + suffix;
}

// =============================================================================
// Template Interpolation
// =============================================================================

/**
 * Interpolate variables in a template string
 * @param template - Template string with placeholders
 * @param data - Data object with values
 * @param options - Template options
 * @returns Interpolated string
 * @example
 * ```typescript
 * interpolate("Hello, {{name}}!", { name: "World" }) // "Hello, World!"
 * interpolate("Hello, {name}!", { name: "World" }, { prefix: "{", suffix: "}" }) // "Hello, World!"
 * ```
 */
export function interpolate(
  template: string, 
  data: Record<string, unknown>, 
  options: TemplateOptions = {}
): string {
  const { prefix = '{{', suffix = '}}' } = options;
  
  const escapedPrefix = prefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapedSuffix = suffix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  const pattern = new RegExp(`${escapedPrefix}([^${escapedSuffix}]+)${escapedSuffix}`, 'g');
  
  return template.replace(pattern, (_, key) => {
    const trimmedKey = key.trim();
    const value = data[trimmedKey];
    return value !== undefined ? String(value) : '';
  });
}

/**
 * Format a string with positional arguments
 * @param format - Format string with {0}, {1}, etc.
 * @param args - Arguments to insert
 * @returns Formatted string
 * @example
 * ```typescript
 * format("Hello {0}, you are {1} years old", "World", 25) // "Hello World, you are 25 years old"
 * ```
 */
export function format(format: string, ...args: unknown[]): string {
  return format.replace(/{(\d+)}/g, (_, index) => {
    const idx = parseInt(index, 10);
    return idx < args.length ? String(args[idx]) : '';
  });
}

// =============================================================================
// Escaping and Unescaping
// =============================================================================

/**
 * Escape HTML special characters
 * @param str - Input string
 * @returns HTML-escaped string
 * @example
 * ```typescript
 * escapeHtml("<script>alert('xss')</script>") // "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;"
 * ```
 */
export function escapeHtml(str: string): string {
  const escapeMap: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
  };
  
  return str.replace(/[&<>"'/]/g, char => escapeMap[char]);
}

/**
 * Unescape HTML entities
 * @param str - HTML-escaped string
 * @returns Unescaped string
 */
export function unescapeHtml(str: string): string {
  const unescapeMap: Record<string, string> = {
    '&amp;': '&',
    '&lt;': '<',
    '&gt;': '>',
    '&quot;': '"',
    '&#39;': "'",
    '&#x2F;': '/',
  };
  
  return str.replace(/&amp;|&lt;|&gt;|&quot;|&#39;|&#x2F;/g, entity => unescapeMap[entity]);
}

/**
 * Escape JSON special characters
 * @param str - Input string
 * @returns JSON-escaped string
 */
export function escapeJson(str: string): string {
  const escapeMap: Record<string, string> = {
    '"': '\\"',
    '\\': '\\\\',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
  };
  
  return str.replace(/["\\\b\f\n\r\t]/g, char => escapeMap[char]);
}

/**
 * Unescape JSON special characters
 * @param str - JSON-escaped string
 * @returns Unescaped string
 */
export function unescapeJson(str: string): string {
  // Handle JSON escape sequences
  return str
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, '\\')
    .replace(/\\b/g, '\b')
    .replace(/\\f/g, '\f')
    .replace(/\\n/g, '\n')
    .replace(/\\r/g, '\r')
    .replace(/\\t/g, '\t');
}

/**
 * Escape XML special characters
 * @param str - Input string
 * @returns XML-escaped string
 */
export function escapeXml(str: string): string {
  const escapeMap: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&apos;',
  };
  
  return str.replace(/[&<>"']/g, char => escapeMap[char]);
}

/**
 * Escape SQL string for safe inclusion in queries
 * @param str - Input string
 * @returns SQL-escaped string (single quotes doubled)
 * @example
 * ```typescript
 * escapeSql("O'Reilly") // "O''Reilly"
 * ```
 */
export function escapeSql(str: string): string {
  return str.replace(/'/g, "''");
}

/**
 * Escape a string for use in a regular expression
 * @param str - Input string
 * @returns RegExp-safe string
 * @example
 * ```typescript
 * escapeRegExp("hello.world") // "hello\\.world"
 * ```
 */
export function escapeRegExp(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Apply multiple escape operations
 * @param str - Input string
 * @param options - Escape options
 * @returns Escaped string
 */
export function escape(str: string, options: EscapeOptions = {}): string {
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

/**
 * Extract all URLs from a string
 * @param str - Input string
 * @returns Array of URLs
 */
export function extractUrls(str: string): string[] {
  const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi;
  return str.match(urlPattern) || [];
}

/**
 * Extract all email addresses from a string
 * @param str - Input string
 * @returns Array of email addresses
 */
export function extractEmails(str: string): string[] {
  const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  return str.match(emailPattern) || [];
}

/**
 * Extract all phone numbers from a string (basic pattern)
 * @param str - Input string
 * @returns Array of phone numbers
 */
export function extractPhoneNumbers(str: string): string[] {
  const phonePattern = /(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}/g;
  return str.match(phonePattern) || [];
}

/**
 * Extract all hashtags from a string
 * @param str - Input string
 * @returns Array of hashtags (without #)
 */
export function extractHashtags(str: string): string[] {
  const hashtagPattern = /#(\w+)/g;
  const matches = str.matchAll(hashtagPattern);
  return Array.from(matches, m => m[1]);
}

/**
 * Extract all mentions (@username) from a string
 * @param str - Input string
 * @returns Array of usernames (without @)
 */
export function extractMentions(str: string): string[] {
  const mentionPattern = /@(\w+)/g;
  const matches = str.matchAll(mentionPattern);
  return Array.from(matches, m => m[1]);
}

/**
 * Extract all numbers from a string
 * @param str - Input string
 * @param asFloat - If true, extract floating point numbers
 * @returns Array of numbers
 */
export function extractNumbers(str: string, asFloat: boolean = false): number[] {
  const pattern = asFloat ? /-?\d+\.?\d*/g : /-?\d+/g;
  const matches = str.match(pattern);
  return matches ? matches.map(Number) : [];
}

/**
 * Extract text between delimiters
 * @param str - Input string
 * @param start - Start delimiter
 * @param end - End delimiter
 * @param includeDelimiters - Include delimiters in result
 * @returns Array of extracted strings
 * @example
 * ```typescript
 * extractBetween("Hello [World] and [Universe]", "[", "]") // ["World", "Universe"]
 * ```
 */
export function extractBetween(
  str: string, 
  start: string, 
  end: string, 
  includeDelimiters: boolean = false
): string[] {
  const escapedStart = escapeRegExp(start);
  const escapedEnd = escapeRegExp(end);
  const pattern = includeDelimiters 
    ? new RegExp(`(${escapedStart}.*?${escapedEnd})`, 'g')
    : new RegExp(`${escapedStart}(.*?)${escapedEnd}`, 'g');
  
  const matches = str.matchAll(pattern);
  return Array.from(matches, m => includeDelimiters ? m[0] : m[1]);
}

// =============================================================================
// Character Analysis
// =============================================================================

/**
 * Analyze character composition of a string
 * @param str - Input string
 * @returns Character analysis result
 * @example
 * ```typescript
 * analyzeChars("Hello 123!") 
 * // { total: 10, letters: 5, digits: 3, spaces: 1, punctuation: 1, ... }
 * ```
 */
export function analyzeChars(str: string): CharAnalysis {
  const result: CharAnalysis = {
    total: str.length,
    letters: 0,
    digits: 0,
    spaces: 0,
    punctuation: 0,
    uppercase: 0,
    lowercase: 0,
    special: 0,
    unicode: 0,
  };
  
  for (const char of str) {
    if (/\p{L}/u.test(char)) {
      result.letters++;
      if (/\p{Lu}/u.test(char)) result.uppercase++;
      else if (/\p{Ll}/u.test(char)) result.lowercase++;
      if (char.codePointAt(0) || 0 > 127) result.unicode++;
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

/**
 * Count occurrences of a substring
 * @param str - Input string
 * @param substring - Substring to count
 * @param caseSensitive - Case-sensitive search
 * @returns Number of occurrences
 */
export function countOccurrences(str: string, substring: string, caseSensitive: boolean = true): number {
  if (!substring) return 0;
  
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

/**
 * Check if string contains only letters
 * @param str - Input string
 * @returns True if all characters are letters
 */
export function isAlpha(str: string): boolean {
  return /^\p{L}+$/u.test(str);
}

/**
 * Check if string contains only alphanumeric characters
 * @param str - Input string
 * @returns True if all characters are alphanumeric
 */
export function isAlphanumeric(str: string): boolean {
  return /^[\p{L}\p{N}]+$/u.test(str);
}

/**
 * Check if string contains only digits
 * @param str - Input string
 * @returns True if all characters are digits
 */
export function isNumeric(str: string): boolean {
  return /^\p{N}+$/u.test(str);
}

/**
 * Check if string is a valid integer
 * @param str - Input string
 * @returns True if valid integer
 */
export function isInteger(str: string): boolean {
  return /^-?\d+$/.test(str);
}

/**
 * Check if string is a valid float/decimal number
 * @param str - Input string
 * @returns True if valid float
 */
export function isFloat(str: string): boolean {
  return /^-?\d*\.?\d+$/.test(str);
}

// =============================================================================
// String Manipulation
// =============================================================================

/**
 * Reverse a string
 * @param str - Input string
 * @returns Reversed string
 * @example
 * ```typescript
 * reverse("hello") // "olleh"
 * reverse("你好") // "好你"
 * ```
 */
export function reverse(str: string): string {
  return Array.from(str).reverse().join('');
}

/**
 * Remove all whitespace from a string
 * @param str - Input string
 * @returns String without whitespace
 */
export function removeWhitespace(str: string): string {
  return str.replace(/\s+/g, '');
}

/**
 * Remove all digits from a string
 * @param str - Input string
 * @returns String without digits
 */
export function removeDigits(str: string): string {
  return str.replace(/\d+/g, '');
}

/**
 * Remove all non-alphanumeric characters
 * @param str - Input string
 * @returns String with only alphanumeric characters
 */
export function removeSpecialChars(str: string): string {
  return str.replace(/[^\p{L}\p{N}]/gu, '');
}

/**
 * Replace all occurrences of a substring
 * @param str - Input string
 * @param search - Substring to search for
 * @param replace - Replacement string
 * @param caseSensitive - Case-sensitive search
 * @returns String with replacements
 */
export function replaceAll(
  str: string, 
  search: string, 
  replace: string, 
  caseSensitive: boolean = true
): string {
  if (!search) return str;
  
  if (caseSensitive) {
    return str.split(search).join(replace);
  }
  
  const escaped = escapeRegExp(search);
  const pattern = new RegExp(escaped, 'gi');
  return str.replace(pattern, replace);
}

/**
 * Insert a substring at a specific position
 * @param str - Input string
 * @param substring - Substring to insert
 * @param position - Position to insert at
 * @returns String with inserted substring
 * @example
 * ```typescript
 * insertAt("Helo", "l", 2) // "Hello"
 * ```
 */
export function insertAt(str: string, substring: string, position: number): string {
  if (position < 0) position = 0;
  if (position > str.length) position = str.length;
  return str.slice(0, position) + substring + str.slice(position);
}

/**
 * Remove a substring at a specific position
 * @param str - Input string
 * @param start - Start position
 * @param length - Number of characters to remove
 * @returns String with removed substring
 */
export function removeAt(str: string, start: number, length: number = 1): string {
  if (start < 0) start = 0;
  if (start >= str.length) return str;
  return str.slice(0, start) + str.slice(start + length);
}

/**
 * Repeat a string multiple times
 * @param str - Input string
 * @param count - Number of repetitions
 * @param separator - Optional separator between repetitions
 * @returns Repeated string
 * @example
 * ```typescript
 * repeat("ab", 3) // "ababab"
 * repeat("ab", 3, "-") // "ab-ab-ab"
 * ```
 */
export function repeat(str: string, count: number, separator?: string): string {
  if (count <= 0) return '';
  if (!separator) return str.repeat(count);
  return Array(count).fill(str).join(separator);
}

/**
 * Create a string of repeated characters
 * @param char - Character to repeat
 * @param length - Length of resulting string
 * @returns Repeated character string
 */
export function charRepeat(char: string, length: number): string {
  return char.repeat(length);
}

// =============================================================================
// Splitting and Joining
// =============================================================================

/**
 * Split a string with various options
 * @param str - Input string
 * @param options - Split options
 * @returns Array of substrings
 * @example
 * ```typescript
 * split("a, b, c", { separator: ",", trim: true, removeEmpty: true }) // ["a", "b", "c"]
 * ```
 */
export function split(str: string, options: SplitOptions = {}): string[] {
  const { 
    separator = ',', 
    limit, 
    trim = false, 
    removeEmpty = false 
  } = options;
  
  let parts: string[];
  
  if (separator instanceof RegExp) {
    parts = str.split(separator, limit);
  } else {
    parts = str.split(separator, limit);
  }
  
  if (trim) {
    parts = parts.map(p => p.trim());
  }
  
  if (removeEmpty) {
    parts = parts.filter(p => p.length > 0);
  }
  
  return parts;
}

/**
 * Split a string into chunks of equal size
 * @param str - Input string
 * @param chunkSize - Size of each chunk
 * @returns Array of chunks
 * @example
 * ```typescript
 * chunk("abcdefgh", 3) // ["abc", "def", "gh"]
 * ```
 */
export function chunk(str: string, chunkSize: number): string[] {
  if (chunkSize <= 0) return [str];
  
  const chunks: string[] = [];
  for (let i = 0; i < str.length; i += chunkSize) {
    chunks.push(str.slice(i, i + chunkSize));
  }
  return chunks;
}

/**
 * Join array elements with proper grammar
 * @param items - Array of strings
 * @param options - Join options
 * @returns Grammatically correct joined string
 * @example
 * ```typescript
 * joinGrammar(["apple"]) // "apple"
 * joinGrammar(["apple", "banana"]) // "apple and banana"
 * joinGrammar(["apple", "banana", "cherry"]) // "apple, banana, and cherry"
 * ```
 */
export function joinGrammar(
  items: string[], 
  options: { conjunction?: string; oxfordComma?: boolean } = {}
): string {
  const { conjunction = 'and', oxfordComma = true } = options;
  
  if (items.length === 0) return '';
  if (items.length === 1) return items[0];
  if (items.length === 2) return `${items[0]} ${conjunction} ${items[1]}`;
  
  const last = items[items.length - 1];
  const rest = items.slice(0, -1);
  
  const comma = oxfordComma ? ',' : '';
  return `${rest.join(', ')}${comma} ${conjunction} ${last}`;
}

// =============================================================================
// Encoding Utilities
// =============================================================================

/**
 * Encode a string to Base64
 * @param str - Input string
 * @returns Base64 encoded string
 */
export function toBase64(str: string): string {
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(str, 'utf-8').toString('base64');
  }
  return btoa(unescape(encodeURIComponent(str)));
}

/**
 * Decode a Base64 string
 * @param str - Base64 encoded string
 * @returns Decoded string
 */
export function fromBase64(str: string): string {
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(str, 'base64').toString('utf-8');
  }
  return decodeURIComponent(escape(atob(str)));
}

/**
 * Encode a string to URL-safe Base64
 * @param str - Input string
 * @returns URL-safe Base64 encoded string
 */
export function toBase64Url(str: string): string {
  return toBase64(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

/**
 * Decode a URL-safe Base64 string
 * @param str - URL-safe Base64 encoded string
 * @returns Decoded string
 */
export function fromBase64Url(str: string): string {
  const base64 = str.replace(/-/g, '+').replace(/_/g, '/');
  const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=');
  return fromBase64(padded);
}

/**
 * Encode a string for URL (percent encoding)
 * @param str - Input string
 * @returns URL encoded string
 */
export function encodeUrl(str: string): string {
  return encodeURIComponent(str);
}

/**
 * Decode a URL encoded string
 * @param str - URL encoded string
 * @returns Decoded string
 */
export function decodeUrl(str: string): string {
  return decodeURIComponent(str);
}

// =============================================================================
// Comparison and Similarity
// =============================================================================

/**
 * Check if two strings are equal (case-insensitive by default)
 * @param str1 - First string
 * @param str2 - Second string
 * @param caseSensitive - Case-sensitive comparison
 * @returns True if strings are equal
 */
export function equals(str1: string, str2: string, caseSensitive: boolean = false): boolean {
  if (caseSensitive) {
    return str1 === str2;
  }
  return str1.toLowerCase() === str2.toLowerCase();
}

/**
 * Check if string starts with a prefix
 * @param str - Input string
 * @param prefix - Prefix to check
 * @param caseSensitive - Case-sensitive check
 * @returns True if string starts with prefix
 */
export function startsWith(str: string, prefix: string, caseSensitive: boolean = true): boolean {
  if (!caseSensitive) {
    return str.toLowerCase().startsWith(prefix.toLowerCase());
  }
  return str.startsWith(prefix);
}

/**
 * Check if string ends with a suffix
 * @param str - Input string
 * @param suffix - Suffix to check
 * @param caseSensitive - Case-sensitive check
 * @returns True if string ends with suffix
 */
export function endsWith(str: string, suffix: string, caseSensitive: boolean = true): boolean {
  if (!caseSensitive) {
    return str.toLowerCase().endsWith(suffix.toLowerCase());
  }
  return str.endsWith(suffix);
}

/**
 * Check if string contains a substring
 * @param str - Input string
 * @param substring - Substring to find
 * @param caseSensitive - Case-sensitive search
 * @returns True if substring is found
 */
export function contains(str: string, substring: string, caseSensitive: boolean = true): boolean {
  if (!caseSensitive) {
    return str.toLowerCase().includes(substring.toLowerCase());
  }
  return str.includes(substring);
}

/**
 * Calculate Levenshtein distance between two strings
 * @param str1 - First string
 * @param str2 - Second string
 * @returns Levenshtein distance
 * @example
 * ```typescript
 * levenshtein("kitten", "sitting") // 3
 * ```
 */
export function levenshtein(str1: string, str2: string): number {
  const m = str1.length;
  const n = str2.length;
  
  // Create matrix
  const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  
  // Initialize first row and column
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  
  // Fill matrix
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = Math.min(
          dp[i - 1][j] + 1,     // deletion
          dp[i][j - 1] + 1,     // insertion
          dp[i - 1][j - 1] + 1  // substitution
        );
      }
    }
  }
  
  return dp[m][n];
}

/**
 * Calculate similarity ratio between two strings (0-1)
 * @param str1 - First string
 * @param str2 - Second string
 * @returns Similarity ratio (1 = identical, 0 = completely different)
 */
export function similarity(str1: string, str2: string): number {
  const maxLen = Math.max(str1.length, str2.length);
  if (maxLen === 0) return 1;
  
  const distance = levenshtein(str1, str2);
  return 1 - distance / maxLen;
}

/**
 * Find the longest common substring between two strings
 * @param str1 - First string
 * @param str2 - Second string
 * @returns Longest common substring
 */
export function longestCommonSubstring(str1: string, str2: string): string {
  const m = str1.length;
  const n = str2.length;
  
  const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  
  let maxLength = 0;
  let endPos = 0;
  
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
        if (dp[i][j] > maxLength) {
          maxLength = dp[i][j];
          endPos = i;
        }
      }
    }
  }
  
  return str1.slice(endPos - maxLength, endPos);
}

// =============================================================================
// Utility Functions
// =============================================================================

/**
 * Generate a random string
 * @param length - Length of the string
 * @param charset - Character set to use
 * @returns Random string
 * @example
 * ```typescript
 * randomString(10) // "aB3xK9pL2m"
 * randomString(8, "0123456789") // "48291057"
 * ```
 */
export function randomString(length: number, charset?: string): string {
  const chars = charset || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    const values = new Uint32Array(length);
    crypto.getRandomValues(values);
    for (let i = 0; i < length; i++) {
      result += chars[values[i] % chars.length];
    }
  } else {
    for (let i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * chars.length)];
    }
  }
  
  return result;
}

/**
 * Create a slug from a string
 * @param str - Input string
 * @param options - Slug options
 * @returns URL-safe slug
 * @example
 * ```typescript
 * slugify("Hello World!") // "hello-world"
 * slugify("Café & Restaurant") // "cafe-restaurant"
 * ```
 */
export function slugify(
  str: string, 
  options: { lowercase?: boolean; separator?: string; removeSpecial?: boolean } = {}
): string {
  const { lowercase = true, separator = '-', removeSpecial = true } = options;
  
  let result = str;
  
  // Convert to lowercase
  if (lowercase) {
    result = result.toLowerCase();
  }
  
  // Replace accented characters
  result = result.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  
  // Remove special characters
  if (removeSpecial) {
    result = result.replace(/[^\w\s-]/g, '');
  }
  
  // Replace spaces and underscores with separator
  result = result.replace(/[\s_]+/g, separator);
  
  // Replace multiple separators with single
  result = result.replace(new RegExp(`${separator}+`, 'g'), separator);
  
  // Trim separators from ends
  result = result.replace(new RegExp(`^${separator}+|${separator}+$`, 'g'), '');
  
  return result;
}

/**
 * Check if string is empty or whitespace only
 * @param str - Input string
 * @returns True if string is empty or whitespace
 */
export function isEmpty(str: string): boolean {
  return !str || str.trim().length === 0;
}

/**
 * Check if string is not empty
 * @param str - Input string
 * @returns True if string has content
 */
export function isNotEmpty(str: string): boolean {
  return !isEmpty(str);
}

/**
 * Ensure string has a minimum length
 * @param str - Input string
 * @param minLength - Minimum length
 * @param padChar - Character to pad with
 * @returns String with minimum length
 */
export function ensureMinLength(str: string, minLength: number, padChar: string = ' '): string {
  if (str.length >= minLength) return str;
  return padRight(str, minLength, padChar);
}

/**
 * Ensure string does not exceed maximum length
 * @param str - Input string
 * @param maxLength - Maximum length
 * @param suffix - Suffix for truncation
 * @returns String within maximum length
 */
export function ensureMaxLength(str: string, maxLength: number, suffix: string = ''): string {
  if (str.length <= maxLength) return str;
  return truncate(str, { length: maxLength, suffix });
}

/**
 * Capitalize the first letter of a string
 * @param str - Input string
 * @returns String with capitalized first letter
 */
export function capitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Capitalize the first letter of each word
 * @param str - Input string
 * @returns String with capitalized words
 */
export function capitalizeWords(str: string): string {
  return str.replace(/\b\w/g, char => char.toUpperCase());
}

/**
 * Decapitalize the first letter of a string
 * @param str - Input string
 * @returns String with decapitalized first letter
 */
export function decapitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toLowerCase() + str.slice(1);
}

// =============================================================================
// Export All
// =============================================================================

export default {
  // Case conversion
  splitWords,
  toCamelCase,
  toPascalCase,
  toSnakeCase,
  toScreamingSnake,
  toKebabCase,
  toScreamingKebab,
  toDotCase,
  toSpaceCase,
  toTitleCase,
  toCase,
  
  // Trimming and padding
  trim,
  trimLeft,
  trimRight,
  trimChars,
  pad,
  padLeft,
  padRight,
  padBoth,
  zeroPad,
  
  // Truncation
  truncate,
  truncateWords,
  
  // Template interpolation
  interpolate,
  format,
  
  // Escaping
  escapeHtml,
  unescapeHtml,
  escapeJson,
  unescapeJson,
  escapeXml,
  escapeSql,
  escapeRegExp,
  escape,
  
  // Pattern matching
  extractUrls,
  extractEmails,
  extractPhoneNumbers,
  extractHashtags,
  extractMentions,
  extractNumbers,
  extractBetween,
  
  // Character analysis
  analyzeChars,
  countOccurrences,
  isAlpha,
  isAlphanumeric,
  isNumeric,
  isInteger,
  isFloat,
  
  // String manipulation
  reverse,
  removeWhitespace,
  removeDigits,
  removeSpecialChars,
  replaceAll,
  insertAt,
  removeAt,
  repeat,
  charRepeat,
  
  // Splitting and joining
  split,
  chunk,
  joinGrammar,
  
  // Encoding
  toBase64,
  fromBase64,
  toBase64Url,
  fromBase64Url,
  encodeUrl,
  decodeUrl,
  
  // Comparison
  equals,
  startsWith,
  endsWith,
  contains,
  levenshtein,
  similarity,
  longestCommonSubstring,
  
  // Utilities
  randomString,
  slugify,
  isEmpty,
  isNotEmpty,
  ensureMinLength,
  ensureMaxLength,
  capitalize,
  capitalizeWords,
  decapitalize,
};
