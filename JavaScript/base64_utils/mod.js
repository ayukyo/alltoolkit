/**
 * Base64 Utilities - 零依赖 Base64 编码/解码工具库
 * 
 * 提供完整的 Base64 编码、解码、URL 安全变体、以及二进制数据处理功能。
 * 纯 JavaScript 实现，适用于浏览器和 Node.js 环境。
 * 
 * @module base64_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * 标准 Base64 字符表
 * @private
 */
const BASE64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';

/**
 * URL 安全 Base64 字符表（将 +/ 替换为 -_）
 * @private
 */
const BASE64URL_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';

/**
 * 将字符串编码为 Base64
 * 
 * @param {string} str - 要编码的字符串
 * @param {Object} options - 编码选项
 * @param {boolean} options.urlSafe - 是否使用 URL 安全变体（默认 false）
 * @param {boolean} options.pad - 是否添加填充字符 =（默认 true）
 * @returns {string} Base64 编码后的字符串
 * @throws {TypeError} 当输入不是字符串时抛出
 * 
 * @example
 * encode('Hello World'); // 'SGVsbG8gV29ybGQ='
 * encode('Hello World', { urlSafe: true }); // 'SGVsbG8gV29ybGQ'
 */
function encode(str, options = {}) {
  if (typeof str !== 'string') {
    throw new TypeError('Input must be a string');
  }
  
  const { urlSafe = false, pad = true } = options;
  const chars = urlSafe ? BASE64URL_CHARS : BASE64_CHARS;
  
  let result = '';
  const bytes = stringToBytes(str);
  
  for (let i = 0; i < bytes.length; i += 3) {
    const b1 = bytes[i];
    const b2 = i + 1 < bytes.length ? bytes[i + 1] : null;
    const b3 = i + 2 < bytes.length ? bytes[i + 2] : null;
    
    // 第一个 6 位
    result += chars[b1 >> 2];
    
    // 第二个 6 位
    const b1Low = b1 & 0x03;
    if (b2 !== null) {
      result += chars[(b1Low << 4) | (b2 >> 4)];
      
      // 第三个 6 位
      const b2Low = b2 & 0x0F;
      if (b3 !== null) {
        result += chars[(b2Low << 2) | (b3 >> 6)];
        // 第四个 6 位
        result += chars[b3 & 0x3F];
      } else {
        result += chars[b2Low << 2];
        if (pad) result += '=';
      }
    } else {
      result += chars[b1Low << 4];
      if (pad) result += '==';
    }
  }
  
  return result;
}

/**
 * 将 Base64 字符串解码为普通字符串
 * 
 * @param {string} base64 - Base64 编码的字符串
 * @param {Object} options - 解码选项
 * @param {boolean} options.urlSafe - 输入是否为 URL 安全变体（默认 false）
 * @returns {string} 解码后的字符串
 * @throws {TypeError} 当输入不是字符串时抛出
 * @throws {Error} 当输入包含无效的 Base64 字符时抛出
 * 
 * @example
 * decode('SGVsbG8gV29ybGQ='); // 'Hello World'
 * decode('SGVsbG8gV29ybGQ', { urlSafe: true }); // 'Hello World'
 */
function decode(base64, options = {}) {
  if (typeof base64 !== 'string') {
    throw new TypeError('Input must be a string');
  }
  
  const { urlSafe = false } = options;
  const chars = urlSafe ? BASE64URL_CHARS : BASE64_CHARS;
  
  // 移除填充字符和空白字符
  const cleanInput = base64.replace(/[=\s]/g, '');
  
  if (cleanInput.length === 0) {
    return '';
  }
  
  // 验证输入
  const validChars = new RegExp(`^[${chars.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&')}]+$`);
  if (!validChars.test(cleanInput)) {
    throw new Error('Invalid Base64 character in input');
  }
  
  const bytes = [];
  
  for (let i = 0; i < cleanInput.length; i += 4) {
    const c1 = chars.indexOf(cleanInput[i]);
    const c2 = chars.indexOf(cleanInput[i + 1] || 'A');
    const c3 = chars.indexOf(cleanInput[i + 2] || 'A');
    const c4 = chars.indexOf(cleanInput[i + 3] || 'A');
    
    // 解码 4 个字符为 3 个字节
    bytes.push((c1 << 2) | (c2 >> 4));
    
    if (cleanInput[i + 2]) {
      bytes.push(((c2 & 0x0F) << 4) | (c3 >> 2));
    }
    
    if (cleanInput[i + 3]) {
      bytes.push(((c3 & 0x03) << 6) | c4);
    }
  }
  
  return bytesToString(bytes);
}

/**
 * 将字符串转换为字节数组（UTF-8 编码）
 * 
 * Optimized: Pre-allocates array capacity, reduces property lookups.
 * 
 * @private
 * @param {string} str - 输入字符串
 * @returns {number[]} 字节数组
 */
function stringToBytes(str) {
  const len = str.length;
  // Pre-allocate with estimated capacity (worst case: 4 bytes per char)
  const bytes = new Array(len * 4);
  let byteIndex = 0;
  
  for (let i = 0; i < len; i++) {
    const code = str.charCodeAt(i);
    
    if (code < 0x80) {
      bytes[byteIndex++] = code;
    } else if (code < 0x800) {
      bytes[byteIndex++] = 0xC0 | (code >> 6);
      bytes[byteIndex++] = 0x80 | (code & 0x3F);
    } else if (code < 0xD800 || code >= 0xE000) {
      bytes[byteIndex++] = 0xE0 | (code >> 12);
      bytes[byteIndex++] = 0x80 | ((code >> 6) & 0x3F);
      bytes[byteIndex++] = 0x80 | (code & 0x3F);
    } else {
      // 处理代理对（surrogate pair）
      i++;
      // Bounds check for incomplete surrogate pair
      if (i >= len) {
        // Invalid surrogate pair at end of string, skip
        continue;
      }
      const nextCode = str.charCodeAt(i);
      const fullCode = 0x10000 + (((code & 0x3FF) << 10) | (nextCode & 0x3FF));
      bytes[byteIndex++] = 0xF0 | (fullCode >> 18);
      bytes[byteIndex++] = 0x80 | ((fullCode >> 12) & 0x3F);
      bytes[byteIndex++] = 0x80 | ((fullCode >> 6) & 0x3F);
      bytes[byteIndex++] = 0x80 | (fullCode & 0x3F);
    }
  }
  
  // Trim array to actual size
  bytes.length = byteIndex;
  return bytes;
}

/**
 * 将字节数组转换为字符串（UTF-8 解码）
 * 
 * Optimized: Uses array for string building, bounds checking for safety.
 * 
 * @private
 * @param {number[]} bytes - 字节数组
 * @returns {string} 解码后的字符串
 */
function bytesToString(bytes) {
  const len = bytes.length;
  // Use array for efficient string building
  const chars = [];
  
  for (let i = 0; i < len; i++) {
    const byte = bytes[i];
    
    if (byte < 0x80) {
      chars.push(String.fromCharCode(byte));
    } else if ((byte & 0xE0) === 0xC0) {
      // Check bounds for multi-byte sequence
      if (i + 1 >= len) break;
      const b1 = byte & 0x1F;
      const b2 = bytes[++i] & 0x3F;
      chars.push(String.fromCharCode((b1 << 6) | b2));
    } else if ((byte & 0xF0) === 0xE0) {
      if (i + 2 >= len) break;
      const b1 = byte & 0x0F;
      const b2 = bytes[++i] & 0x3F;
      const b3 = bytes[++i] & 0x3F;
      chars.push(String.fromCharCode((b1 << 12) | (b2 << 6) | b3));
    } else if ((byte & 0xF8) === 0xF0) {
      if (i + 3 >= len) break;
      const b1 = byte & 0x07;
      const b2 = bytes[++i] & 0x3F;
      const b3 = bytes[++i] & 0x3F;
      const b4 = bytes[++i] & 0x3F;
      const code = ((b1 << 18) | (b2 << 12) | (b3 << 6) | b4) - 0x10000;
      chars.push(String.fromCharCode(0xD800 + (code >> 10)));
      chars.push(String.fromCharCode(0xDC00 + (code & 0x3FF)));
    }
    // Invalid byte sequences are silently skipped
  }
  
  return chars.join('');
}

/**
 * 将 Base64 字符串转换为 URL 安全格式
 * 
 * @param {string} base64 - 标准 Base64 字符串
 * @param {boolean} pad - 是否保留填充字符（默认 false）
 * @returns {string} URL 安全的 Base64 字符串
 * @throws {TypeError} 当输入不是字符串时抛出
 * 
 * @example
 * toUrlSafe('SGVsbG8gV29ybGQ='); // 'SGVsbG8gV29ybGQ'
 */
function toUrlSafe(base64, pad = false) {
  if (typeof base64 !== 'string') {
    throw new TypeError('Input must be a string');
  }
  
  let result = base64.replace(/\+/g, '-').replace(/\//g, '_');
  if (!pad) {
    result = result.replace(/=/g, '');
  }
  return result;
}

/**
 * 将 URL 安全 Base64 转换为标准格式
 * 
 * @param {string} base64url - URL 安全的 Base64 字符串
 * @returns {string} 标准 Base64 字符串
 * @throws {TypeError} 当输入不是字符串时抛出
 * 
 * @example
 * fromUrlSafe('SGVsbG8gV29ybGQ'); // 'SGVsbG8gV29ybGQ='
 */
function fromUrlSafe(base64url) {
  if (typeof base64url !== 'string') {
    throw new TypeError('Input must be a string');
  }
  
  let result = base64url.replace(/-/g, '+').replace(/_/g, '/');
  
  // 添加填充
  const padding = (4 - (result.length % 4)) % 4;
  result += '='.repeat(padding);
  
  return result;
}

/**
 * 验证字符串是否为有效的 Base64
 * 
 * Optimized: Early return for empty strings, efficient regex patterns.
 * 
 * @param {string} str - 要验证的字符串
 * @param {Object} options - 验证选项
 * @param {boolean} options.urlSafe - 是否验证 URL 安全格式（默认 false）
 * @param {boolean} options.allowPadding - 是否允许填充字符（默认 true）
 * @returns {boolean} 是否为有效的 Base64 字符串
 * 
 * @example
 * isValid('SGVsbG8gV29ybGQ='); // true
 * isValid('invalid!!!'); // false
 */
function isValid(str, options = {}) {
  // Fast path: reject non-strings and empty strings
  if (typeof str !== 'string') {
    return false;
  }
  
  const len = str.length;
  if (len === 0) {
    return false;
  }
  
  const { urlSafe = false, allowPadding = true } = options;
  
  // Pre-compiled regex patterns for performance
  const patterns = urlSafe 
    ? (allowPadding ? /^[A-Za-z0-9_-]*={0,2}$/ : /^[A-Za-z0-9_-]+$/)
    : (allowPadding ? /^[A-Za-z0-9+/]*={0,2}$/ : /^[A-Za-z0-9+/]+$/);
  
  if (!patterns.test(str)) {
    return false;
  }
  
  // 检查长度（不含填充）是否为有效 Base64
  // Valid Base64 lengths (without padding): 0, 2, 3 mod 4 (but not 1)
  const cleanLen = len - (str.endsWith('=') ? (str.endsWith('==') ? 2 : 1) : 0);
  if (cleanLen % 4 === 1) {
    return false;
  }
  
  return true;
}

/**
 * 将 Base64 字符串转换为 Uint8Array（二进制数据）
 * 
 * @param {string} base64 - Base64 编码的字符串
 * @returns {Uint8Array} 二进制数据
 * @
throws {TypeError} 当输入不是字符串时抛出
 * @throws {Error} 当输入包含无效的 Base64 字符时抛出
 * 
 * @example
 * const bytes = toUint8Array('SGVsbG8gV29ybGQ=');
 * // Uint8Array(11) [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]
 */
function toUint8Array(base64) {
  if (typeof base64 !== 'string') {
    throw new TypeError('Input must be a string');
  }
  
  // 移除填充字符和空白字符
  const cleanInput = base64.replace(/[=\s]/g, '');
  
  if (cleanInput.length === 0) {
    return new Uint8Array(0);
  }
  
  const bytes = [];
  
  for (let i = 0; i < cleanInput.length; i += 4) {
    const c1 = BASE64_CHARS.indexOf(cleanInput[i]);
    const c2 = BASE64_CHARS.indexOf(cleanInput[i + 1] || 'A');
    const c3 = BASE64_CHARS.indexOf(cleanInput[i + 2] || 'A');
    const c4 = BASE64_CHARS.indexOf(cleanInput[i + 3] || 'A');
    
    if (c1 === -1 || c2 === -1 || c3 === -1 || c4 === -1) {
      throw new Error('Invalid Base64 character in input');
    }
    
    bytes.push((c1 << 2) | (c2 >> 4));
    
    if (cleanInput[i + 2]) {
      bytes.push(((c2 & 0x0F) << 4) | (c3 >> 2));
    }
    
    if (cleanInput[i + 3]) {
      bytes.push(((c3 & 0x03) << 6) | c4);
    }
  }
  
  return new Uint8Array(bytes);
}

/**
 * 将 Uint8Array（二进制数据）编码为 Base64 字符串
 * 
 * @param {Uint8Array} bytes - 二进制数据
 * @param {Object} options - 编码选项
 * @param {boolean} options.urlSafe - 是否使用 URL 安全变体（默认 false）
 * @param {boolean} options.pad - 是否添加填充字符（默认 true）
 * @returns {string} Base64 编码后的字符串
 * @throws {TypeError} 当输入不是 Uint8Array 时抛出
 * 
 * @example
 * const bytes = new Uint8Array([72, 101, 108, 108, 111]);
 * fromUint8Array(bytes); // 'SGVsbG8='
 */
function fromUint8Array(bytes, options = {}) {
  if (!(bytes instanceof Uint8Array)) {
    throw new TypeError('Input must be a Uint8Array');
  }
  
  const { urlSafe = false, pad = true } = options;
  const chars = urlSafe ? BASE64URL_CHARS : BASE64_CHARS;
  
  let result = '';
  
  for (let i = 0; i < bytes.length; i += 3) {
    const b1 = bytes[i];
    const b2 = i + 1 < bytes.length ? bytes[i + 1] : null;
    const b3 = i + 2 < bytes.length ? bytes[i + 2] : null;
    
    result += chars[b1 >> 2];
    
    const b1Low = b1 & 0x03;
    if (b2 !== null) {
      result += chars[(b1Low << 4) | (b2 >> 4)];
      
      const b2Low = b2 & 0x0F;
      if (b3 !== null) {
        result += chars[(b2Low << 2) | (b3 >> 6)];
        result += chars[b3 & 0x3F];
      } else {
        result += chars[b2Low << 2];
        if (pad) result += '=';
      }
    } else {
      result += chars[b1Low << 4];
      if (pad) result += '==';
    }
  }
  
  return result;
}

/**
 * 计算 Base64 编码后的字符串长度
 * 
 * @param {string} str - 原始字符串
 * @param {Object} options - 选项
 * @param {boolean} options.pad - 是否包含填充字符（默认 true）
 * @returns {number} 编码后的长度
 * 
 * @example
 * encodedLength('Hello'); // 8 (SGVsbG8=)
 * encodedLength('Hello', { pad: false }); // 7 (SGVsbG8)
 */
function encodedLength(str, options = {}) {
  if (typeof str !== 'string') {
    return 0;
  }
  
  const { pad = true } = options;
  const bytes = stringToBytes(str);
  const groups = Math.ceil(bytes.length / 3);
  let length = groups * 4;
  
  if (!pad) {
    const remainder = bytes.length % 3;
    if (remainder === 1) length -= 2;
    else if (remainder === 2) length -= 1;
  }
  
  return length;
}

// 导出模块（支持 CommonJS 和 ES Module）
if (typeof module !== 'undefined' && module.exports) {
  // CommonJS
  module.exports = {
    encode,
    decode,
    toUrlSafe,
    fromUrlSafe,
    isValid,
    toUint8Array,
    fromUint8Array,
    encodedLength
  };
}

// ES Module 导出
if (typeof exports !== 'undefined') {
  exports.encode = encode;
  exports.decode = decode;
  exports.toUrlSafe = toUrlSafe;
  exports.fromUrlSafe = fromUrlSafe;
  exports.isValid = isValid;
  exports.toUint8Array = toUint8Array;
  exports.fromUint8Array = fromUint8Array;
  exports.encodedLength = encodedLength;
}
