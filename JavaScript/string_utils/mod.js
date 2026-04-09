/**
 * String Utilities - JavaScript String Manipulation Module
 * 
 * A comprehensive collection of string manipulation utilities.
 * Zero dependencies - uses only JavaScript standard library.
 * 
 * @module string_utils
 * @version 1.0.0
 * @author AllToolkit
 * @license MIT
 */

(function(global) {
    'use strict';

    const StringUtils = {};

    // Character set constants
    const LOWERCASE = 'abcdefghijklmnopqrstuvwxyz';
    const UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const DIGITS = '0123456789';
    const SPECIAL_CHARS = '!@#$%^&*()-_=+[]{}|;:,.<>?';
    const ALPHANUMERIC = LOWERCASE + UPPERCASE + DIGITS;
    const ALL_CHARS = ALPHANUMERIC + SPECIAL_CHARS;
    
    // Pre-compiled regex patterns for better performance
    const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    const URL_REGEX = /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;
    const IPV4_REGEX = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

    // Empty/Blank Checks
    StringUtils.isBlank = function(str) {
        if (str === null || str === undefined) return true;
        return String(str).trim().length === 0;
    };

    StringUtils.isNotBlank = function(str) {
        return !StringUtils.isBlank(str);
    };

    StringUtils.isEmpty = function(str) {
        if (str === null || str === undefined) return true;
        return String(str).length === 0;
    };

    // Trimming and Whitespace
    StringUtils.trim = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).trim();
    };

    StringUtils.trimLeft = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).trimStart();
    };

    StringUtils.trimRight = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).trimEnd();
    };

    StringUtils.removeWhitespace = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/\s/g, '');
    };

    StringUtils.normalizeWhitespace = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/\s+/g, ' ').trim();
    };

    // Case Conversion
    StringUtils.toLowerCase = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).toLowerCase();
    };

    StringUtils.toUpperCase = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).toUpperCase();
    };

    StringUtils.capitalize = function(str) {
        if (str === null || str === undefined) return '';
        str = String(str);
        if (str.length === 0) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    };

    StringUtils.uncapitalize = function(str) {
        if (str === null || str === undefined) return '';
        str = String(str);
        if (str.length === 0) return '';
        return str.charAt(0).toLowerCase() + str.slice(1);
    };

    StringUtils.toTitleCase = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/\w\S*/g, function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    };

    StringUtils.swapCase = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/[a-zA-Z]/g, function(c) {
            return c === c.toUpperCase() ? c.toLowerCase() : c.toUpperCase();
        });
    };

    // Substring Operations
    StringUtils.truncate = function(str, maxLength, suffix) {
        if (str === null || str === undefined) return '';
        str = String(str);
        suffix = suffix === undefined ? '...' : String(suffix);
        if (str.length <= maxLength) return str;
        return str.substring(0, maxLength - suffix.length) + suffix;
    };

    StringUtils.substringBetween = function(str, open, close) {
        if (str === null || str === undefined) return null;
        str = String(str);
        const start = str.indexOf(open);
        if (start === -1) return null;
        const end = str.indexOf(close, start + open.length);
        if (end === -1) return null;
        return str.substring(start + open.length, end);
    };

    StringUtils.substringAfter = function(str, separator) {
        if (str === null || str === undefined) return '';
        str = String(str);
        const pos = str.indexOf(separator);
        if (pos === -1) return '';
        return str.substring(pos + separator.length);
    };

    StringUtils.substringBefore = function(str, separator) {
        if (str === null || str === undefined) return '';
        str = String(str);
        const pos = str.indexOf(separator);
        if (pos === -1) return str;
        return str.substring(0, pos);
    };

    StringUtils.substringAfterLast = function(str, separator) {
        if (str === null || str === undefined) return '';
        str = String(str);
        const pos = str.lastIndexOf(separator);
        if (pos === -1) return '';
        return str.substring(pos + separator.length);
    };

    StringUtils.substringBeforeLast = function(str, separator) {
        if (str === null || str === undefined) return '';
        str = String(str);
        const pos = str.lastIndexOf(separator);
        if (pos === -1) return str;
        return str.substring(0, pos);
    };

    // Prefix/Suffix Operations
    StringUtils.startsWith = function(str, prefix, ignoreCase) {
        if (str === null || str === undefined) return prefix === null || prefix === undefined;
        if (prefix === null || prefix === undefined) return false;
        str = String(str);
        prefix = String(prefix);
        if (ignoreCase) {
            str = str.toLowerCase();
            prefix = prefix.toLowerCase();
        }
        return str.indexOf(prefix) === 0;
    };

    StringUtils.endsWith = function(str, suffix, ignoreCase) {
        if (str === null || str === undefined) return suffix === null || suffix === undefined;
        if (suffix === null || suffix === undefined) return false;
        str = String(str);
        suffix = String(suffix);
        if (ignoreCase) {
            str = str.toLowerCase();
            suffix = suffix.toLowerCase();
        }
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    };

    StringUtils.removePrefix = function(str, prefix) {
        if (str === null || str === undefined) return '';
        if (prefix === null || prefix === undefined) return String(str);
        str = String(str);
        prefix = String(prefix);
        if (str.indexOf(prefix) === 0) {
            return str.substring(prefix.length);
        }
        return str;
    };

    StringUtils.removeSuffix = function(str, suffix) {
        if (str === null || str === undefined) return '';
        if (suffix === null || suffix === undefined) return String(str);
        str = String(str);
        suffix = String(suffix);
        if (str.indexOf(suffix, str.length - suffix.length) !== -1) {
            return str.substring(0, str.length - suffix.length);
        }
        return str;
    };

    // Counting and Searching
    StringUtils.countMatches = function(str, sub) {
        if (str === null || str === undefined) return 0;
        if (sub === null || sub === undefined || sub === '') return 0;
        str = String(str);
        sub = String(sub);
        let count = 0;
        let pos = str.indexOf(sub);
        while (pos !== -1) {
            count++;
            pos = str.indexOf(sub, pos + sub.length);
        }
        return count;
    };

    StringUtils.contains = function(str, search, ignoreCase) {
        if (str === null || str === undefined) return search === null || search === undefined;
        if (search === null || search === undefined) return false;
        str = String(str);
        search = String(search);
        if (ignoreCase) {
            str = str.toLowerCase();
            search = search.toLowerCase();
        }
        return str.indexOf(search) !== -1;
    };

    StringUtils.indexOf = function(str, search, fromIndex) {
        if (str === null || str === undefined) return -1;
        if (search === null || search === undefined) return -1;
        str = String(str);
        search = String(search);
        fromIndex = fromIndex || 0;
        return str.indexOf(search, fromIndex);
    };

    StringUtils.lastIndexOf = function(str, search, fromIndex) {
        if (str === null || str === undefined) return -1;
        if (search === null || search === undefined) return -1;
        str = String(str);
        search = String(search);
        return str.lastIndexOf(search, fromIndex);
    };

    // Replacement Operations
    StringUtils.replaceAll = function(str, search, replacement) {
        if (str === null || str === undefined) return '';
        if (search === null || search === undefined || search === '') return String(str);
        str = String(str);
        search = String(search);
        replacement = replacement === undefined ? '' : String(replacement);
        return str.split(search).join(replacement);
    };

    StringUtils.replaceFirst = function(str, search, replacement) {
        if (str === null || str === undefined) return '';
        if (search === null || search === undefined || search === '') return String(str);
        str = String(str);
        search = String(search);
        replacement = replacement === undefined ? '' : String(replacement);
        const pos = str.indexOf(search);
        if (pos === -1) return str;
        return str.substring(0, pos) + replacement + str.substring(pos + search.length);
    };

    StringUtils.replaceLast = function(str, search, replacement) {
        if (str === null || str === undefined) return '';
        if (search === null || search === undefined || search === '') return String(str);
        str = String(str);
        search = String(search);
        replacement = replacement === undefined ? '' : String(replacement);
        const pos = str.lastIndexOf(search);
        if (pos === -1) return str;
        return str.substring(0, pos) + replacement + str.substring(pos + search.length);
    };

    // Padding
    StringUtils.padLeft = function(str, length, padChar) {
        if (str === null || str === undefined) str = '';
        str = String(str);
        padChar = padChar === undefined ? ' ' : String(padChar).charAt(0);
        if (str.length >= length) return str;
        const padding = padChar.repeat(length - str.length);
        return padding + str;
    };

    StringUtils.padRight = function(str, length, padChar) {
        if (str === null || str === undefined) str = '';
        str = String(str);
        padChar = padChar === undefined ? ' ' : String(padChar).charAt(0);
        if (str.length >= length) return str;
        const padding = padChar.repeat(length - str.length);
        return str + padding;
    };

    StringUtils.center = function(str, length, padChar) {
        if (str === null || str === undefined) str = '';
        str = String(str);
        padChar = padChar === undefined ? ' ' : String(padChar).charAt(0);
        if (str.length >= length) return str;
        const totalPad = length - str.length;
        const leftPad = Math.floor(totalPad / 2);
        const rightPad = totalPad - leftPad;
        return padChar.repeat(leftPad) + str + padChar.repeat(rightPad);
    };

    // Reversal and Repetition
    StringUtils.reverse = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).split('').reverse().join('');
    };

    StringUtils.repeat = function(str, count) {
        if (str === null || str === undefined) return '';
        if (count <= 0) return '';
        return String(str).repeat(count);
    };

    // Splitting and Joining
    StringUtils.split = function(str, separator, limit) {
        if (str === null || str === undefined) return [];
        str = String(str);
        if (separator === undefined) return str.split('');
        return str.split(separator, limit);
    };

    StringUtils.lines = function(str, trimEmpty) {
        if (str === null || str === undefined) return [];
        let lines = String(str).split(/\r\n|\n|\r/);
        if (trimEmpty) {
            lines = lines.filter(function(line) { return line.trim() !== ''; });
        }
        return lines;
    };

    StringUtils.join = function(array, separator) {
        if (!array) return '';
        separator = separator === undefined ? '' : String(separator);
        return array.join(separator);
    };

    // Validation
    StringUtils.isValidEmail = function(str) {
        if (str === null || str === undefined) return false;
        return EMAIL_REGEX.test(String(str));
    };

    StringUtils.isValidUrl = function(str) {
        if (str === null || str === undefined) return false;
        return URL_REGEX.test(String(str));
    };

    StringUtils.isValidIPv4 = function(str) {
        if (str === null || str === undefined) return false;
        return IPV4_REGEX.test(String(str));
    };

    StringUtils.isNumeric = function(str) {
        if (str === null || str === undefined) return false;
        str = String(str);
        if (str === '') return false;
        return !isNaN(str) && !isNaN(parseFloat(str));
    };

    StringUtils.isInteger = function(str) {
        if (str === null || str === undefined) return false;
        str = String(str);
        if (str === '') return false;
        const num = Number(str);
        return !isNaN(num) && Number.isInteger(num);
    };

    StringUtils.isAlpha = function(str) {
        if (str === null || str === undefined) return false;
        return /^[a-zA-Z]+$/.test(String(str));
    };

    StringUtils.isAlphanumeric = function(str) {
        if (str === null || str === undefined) return false;
        return /^[a-zA-Z0-9]+$/.test(String(str));
    };

    // Naming Conventions
    StringUtils.toCamelCase = function(str) {
        if (str === null || str === undefined) return '';
        str = String(str);
        return str.replace(/[-_](.)/g, function(match, char) {
            return char.toUpperCase();
        }).replace(/^(.)/, function(match, char) {
            return char.toLowerCase();
        });
    };

    StringUtils.toPascalCase = function(str) {
        if (str === null || str === undefined) return '';
        str = String(str);
        return str.replace(/[-_](.)/g, function(match, char) {
            return char.toUpperCase();
        }).replace(/^(.)/, function(match, char) {
            return char.toUpperCase();
        });
    };

    StringUtils.toSnakeCase = function(str) {
        if (str === null || str === undefined) return '';
        str = String(str);
        return str.replace(/([A-Z])/g, '_$1').toLowerCase().replace(/^_/, '').replace(/[-_]+/g, '_');
    };

    StringUtils.toKebabCase = function(str) {
        if (str === null || str === undefined) return '';
        str = String(str);
        return str.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, '').replace(/[-_]+/g, '-');
    };

    // Random Generation
    StringUtils.random = function(length, chars) {
        length = length || 16;
        chars = chars || ALPHANUMERIC;
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    };

    StringUtils.randomAlphanumeric = function(length) {
        return StringUtils.random(length, ALPHANUMERIC);
    };

    StringUtils.randomNumeric = function(length) {
        return StringUtils.random(length, DIGITS);
    };

    StringUtils.randomAlphabetic = function(length) {
        return StringUtils.random(length, LOWERCASE + UPPERCASE);
    };

    // Password generation constants
    const PASSWORD_MIN_LENGTH = 4;
    const PASSWORD_DEFAULT_LENGTH = 16;
    const PASSWORD_MAX_LENGTH = 1024;
    
    /**
     * Generates a cryptographically secure random password.
     * Ensures at least one lowercase, one uppercase, one digit, and one special character.
     * 
     * @param {number} length - Desired password length (default: 16, min: 4, max: 1024)
     * @returns {string} Generated password
     */
    StringUtils.randomPassword = function(length) {
        // Validate and normalize length with bounds checking
        if (typeof length !== 'number' || !Number.isFinite(length)) {
            length = PASSWORD_DEFAULT_LENGTH;
        } else if (length < PASSWORD_MIN_LENGTH) {
            length = PASSWORD_MIN_LENGTH;
        } else if (length > PASSWORD_MAX_LENGTH) {
            length = PASSWORD_MAX_LENGTH;
        } else {
            length = Math.floor(length);
        }
        
        // Use crypto.getRandomValues when available for cryptographically secure randomness
        const hasCrypto = typeof crypto !== 'undefined' && typeof crypto.getRandomValues === 'function';
        
        // Get secure random integer in range [0, max) using rejection sampling
        const getRandomInt = function(max) {
            if (hasCrypto && max <= 65536) {
                const arr = new Uint32Array(1);
                const maxValid = Math.floor(0x100000000 / max) * max;
                do {
                    crypto.getRandomValues(arr);
                } while (arr[0] >= maxValid);
                return arr[0] % max;
            }
            return Math.floor(Math.random() * max);
        };
        
        // Pre-allocate array for better performance
        const result = new Array(length);
        
        // Build password with guaranteed character diversity
        result[0] = LOWERCASE.charAt(getRandomInt(LOWERCASE.length));
        result[1] = UPPERCASE.charAt(getRandomInt(UPPERCASE.length));
        result[2] = DIGITS.charAt(getRandomInt(DIGITS.length));
        result[3] = SPECIAL_CHARS.charAt(getRandomInt(SPECIAL_CHARS.length));
        
        // Fill remaining length with random characters from all sets
        const allCharsLen = ALL_CHARS.length;
        for (let i = PASSWORD_MIN_LENGTH; i < length; i++) {
            result[i] = ALL_CHARS.charAt(getRandomInt(allCharsLen));
        }
        
        // Fisher-Yates shuffle for unbiased randomization
        for (let i = length - 1; i > 0; i--) {
            const j = getRandomInt(i + 1);
            // Swap in place without temp variable for micro-optimization
            result[i] = result[j] + (result[j] = result[i], '');
        }
        
        return result.join('');
    };

    // URL Encoding
    StringUtils.urlEncode = function(str) {
        if (str === null || str === undefined) return '';
        return encodeURIComponent(String(str));
    };

    StringUtils.urlDecode = function(str) {
        if (str === null || str === undefined) return '';
        try {
            return decodeURIComponent(String(str));
        } catch (e) {
            return '';
        }
    };

    // Slug Generation
    StringUtils.slugify = function(str, separator) {
        if (str === null || str === undefined) return '';
        separator = separator || '-';
        return String(str)
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_-]+/g, separator)
            .replace(/^-+|-+$/g, '');
    };

    // Strip HTML Tags
    StringUtils.stripHtml = function(str) {
        if (str === null || str === undefined) return '';
        return String(str).replace(/<[^>]*>/g, '');
    };

    // Escape HTML
    StringUtils.escapeHtml = function(str) {
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    };

    // Unescape HTML
    StringUtils.unescapeHtml = function(str) {
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&amp;/g, '&')
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&quot;/g, '"')
            .replace(/&#039;/g, "'");
    };

    // Comparison
    StringUtils.equals = function(str1, str2, ignoreCase) {
        if (str1 === null || str1 === undefined) return str2 === null || str2 === undefined;
        if (str2 === null || str2 === undefined) return false;
        str1 = String(str1);
        str2 = String(str2);
        if (ignoreCase) {
            str1 = str1.toLowerCase();
            str2 = str2.toLowerCase();
        }
        return str1 === str2;
    };

    StringUtils.compare = function(str1, str2, ignoreCase) {
        if (str1 === null || str1 === undefined) str1 = '';
        if (str2 === null || str2 === undefined) str2 = '';
        str1 = String(str1);
        str2 = String(str2);
        if (ignoreCase) {
            str1 = str1.toLowerCase();
            str2 = str2.toLowerCase();
        }
        if (str1 < str2) return -1;
        if (str1 > str2) return 1;
        return 0;
    };

    // Default String
    StringUtils.defaultString = function(str, defaultStr) {
        if (StringUtils.isBlank(str)) {
            return defaultStr === undefined ? '' : String(defaultStr);
        }
        return String(str);
    };

    StringUtils.defaultIfEmpty = function(str, defaultStr) {
        if (StringUtils.isEmpty(str)) {
            return defaultStr === undefined ? '' : String(defaultStr);
        }
        return String(str);
    };

    // Export
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = StringUtils;
    }
    if (typeof global !== 'undefined') {
        global.StringUtils = StringUtils;
    }

})(typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : this);