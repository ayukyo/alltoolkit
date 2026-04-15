/**
 * 随机工具模块
 * 
 * 提供完整的随机数和值生成功能，支持：
 * - 随机整数和浮点数（范围、精度控制）
 * - 随机字符串（字母、数字、特殊字符、自定义字符集）
 * - 随机数组元素选择（单个、多个、不重复）
 * - 随机颜色生成（HEX、RGB、HSL、RGBA）
 * - 随机日期时间生成
 * - UUID v4 生成
 * - 数组洗牌（Fisher-Yates 算法）
 * - 加权随机选择
 * - 概率分布（均匀、正态/高斯、指数）
 * - 加密安全的随机生成
 * - 随机布尔值、枚举值
 * - 批量生成
 * 
 * 零外部依赖，纯 JavaScript 标准库实现。
 * 
 * @module random_utils
 * @version 1.0.0
 */

'use strict';

// ============================================================================
// 常量定义
// ============================================================================

const ALPHABET_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz';
const ALPHABET_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const ALPHABET = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE;
const DIGITS = '0123456789';
const ALPHANUMERIC = ALPHABET + DIGITS;
const SPECIAL_CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?';
const HEX_CHARS = '0123456789abcdef';

// ============================================================================
// 基础随机数生成
// ============================================================================

/**
 * 生成指定范围内的随机整数 [min, max]（包含边界）
 * @param {number} min - 最小值（包含）
 * @param {number} max - 最大值（包含）
 * @returns {number} 随机整数
 * @throws {Error} 如果 min > max 或参数非数字
 * @example
 * randomInt(1, 10) // 返回 1-10 之间的整数
 */
function randomInt(min, max) {
    if (typeof min !== 'number' || typeof max !== 'number') {
        throw new Error('参数必须是数字');
    }
    if (min > max) {
        throw new Error('最小值不能大于最大值');
    }
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * 生成指定范围内的随机浮点数 [min, max)
 * @param {number} min - 最小值（包含）
 * @param {number} max - 最大值（不包含）
 * @param {number} [precision] - 小数位数（可选）
 * @returns {number} 随机浮点数
 * @throws {Error} 如果 min >= max 或参数无效
 * @example
 * randomFloat(0, 1) // 返回 0-1 之间的浮点数
 * randomFloat(0, 100, 2) // 返回两位小数的浮点数
 */
function randomFloat(min, max, precision = null) {
    if (typeof min !== 'number' || typeof max !== 'number') {
        throw new Error('参数必须是数字');
    }
    if (min >= max) {
        throw new Error('最小值必须小于最大值');
    }
    let result = Math.random() * (max - min) + min;
    if (precision !== null && precision >= 0) {
        result = parseFloat(result.toFixed(precision));
    }
    return result;
}

/**
 * 生成随机布尔值
 * @param {number} [probability=0.5] - 返回 true 的概率（0-1）
 * @returns {boolean} 随机布尔值
 * @example
 * randomBool() // 50% 概率返回 true
 * randomBool(0.8) // 80% 概率返回 true
 */
function randomBool(probability = 0.5) {
    if (probability < 0 || probability > 1) {
        throw new Error('概率必须在 0-1 之间');
    }
    return Math.random() < probability;
}

// ============================================================================
// 随机字符串生成
// ============================================================================

/**
 * 生成随机字符串
 * @param {number} length - 字符串长度
 * @param {Object} [options] - 生成选项
 * @param {boolean} [options.lowercase=true] - 包含小写字母
 * @param {boolean} [options.uppercase=true] - 包含大写字母
 * @param {boolean} [options.digits=true] - 包含数字
 * @param {boolean} [options.special=false] - 包含特殊字符
 * @param {string} [options.charset] - 自定义字符集（覆盖其他选项）
 * @param {string} [options.prefix] - 前缀
 * @param {string} [options.suffix] - 后缀
 * @returns {string} 随机字符串
 * @example
 * randomString(10) // 10位字母数字字符串
 * randomString(16, { special: true }) // 包含特殊字符
 * randomString(8, { charset: 'ABC123' }) // 仅使用指定字符
 */
function randomString(length, options = {}) {
    if (typeof length !== 'number' || length < 0) {
        throw new Error('长度必须是非负数');
    }
    
    const {
        lowercase = true,
        uppercase = true,
        digits = true,
        special = false,
        charset = null,
        prefix = '',
        suffix = ''
    } = options;
    
    let chars = charset;
    if (!chars) {
        chars = '';
        if (lowercase) chars += ALPHABET_LOWERCASE;
        if (uppercase) chars += ALPHABET_UPPERCASE;
        if (digits) chars += DIGITS;
        if (special) chars += SPECIAL_CHARS;
        if (!chars) chars = ALPHANUMERIC; // 默认字符集
    }
    
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars[randomInt(0, chars.length - 1)];
    }
    
    return prefix + result + suffix;
}

/**
 * 生成随机十六进制字符串
 * @param {number} length - 字符串长度
 * @returns {string} 十六进制字符串
 * @example
 * randomHex(8) // 返回类似 "a3f2b1c8"
 */
function randomHex(length) {
    return randomString(length, { charset: HEX_CHARS });
}

/**
 * 生成随机数字字符串
 * @param {number} length - 字符串长度
 * @returns {string} 数字字符串
 * @example
 * randomNumeric(6) // 返回类似 "123456"
 */
function randomNumeric(length) {
    return randomString(length, { charset: DIGITS });
}

/**
 * 生成随机字母字符串
 * @param {number} length - 字符串长度
 * @param {boolean} [lowercaseOnly=false] - 仅小写字母
 * @returns {string} 字母字符串
 * @example
 * randomAlpha(8) // 返回类似 "AbCdEfGh"
 * randomAlpha(8, true) // 返回类似 "abcdefgh"
 */
function randomAlpha(length, lowercaseOnly = false) {
    const charset = lowercaseOnly ? ALPHABET_LOWERCASE : ALPHABET;
    return randomString(length, { charset });
}

/**
 * 生成随机密码（强密码）
 * @param {number} [length=16] - 密码长度
 * @returns {string} 强密码（包含大小写字母、数字、特殊字符）
 * @example
 * randomPassword() // 返回16位强密码
 * randomPassword(20) // 返回20位强密码
 */
function randomPassword(length = 16) {
    if (length < 4) {
        throw new Error('密码长度至少为4位');
    }
    
    // 确保每种字符至少有一个
    const parts = [
        ALPHABET_LOWERCASE[randomInt(0, 25)],
        ALPHABET_UPPERCASE[randomInt(0, 25)],
        DIGITS[randomInt(0, 9)],
        SPECIAL_CHARS[randomInt(0, SPECIAL_CHARS.length - 1)]
    ];
    
    // 填充剩余长度
    const remaining = randomString(length - 4, { 
        lowercase: true, 
        uppercase: true, 
        digits: true, 
        special: true 
    });
    
    // 打乱顺序（字符串版本）
    const chars = (parts.join('') + remaining).split('');
    for (let i = chars.length - 1; i > 0; i--) {
        const j = randomInt(0, i);
        [chars[i], chars[j]] = [chars[j], chars[i]];
    }
    return chars.join('');
}

// ============================================================================
// 随机颜色生成
// ============================================================================

/**
 * 生成随机 HEX 颜色
 * @param {boolean} [withHash=true] - 是否包含 # 前缀
 * @returns {string} HEX 颜色值
 * @example
 * randomHexColor() // 返回类似 "#a3f2b1"
 * randomHexColor(false) // 返回类似 "a3f2b1"
 */
function randomHexColor(withHash = true) {
    const hex = randomHex(6);
    return withHash ? `#${hex}` : hex;
}

/**
 * 生成随机 RGB 颜色
 * @returns {Object} RGB 颜色对象 { r, g, b }
 * @example
 * randomRgbColor() // 返回类似 { r: 123, g: 45, b: 200 }
 */
function randomRgbColor() {
    return {
        r: randomInt(0, 255),
        g: randomInt(0, 255),
        b: randomInt(0, 255)
    };
}

/**
 * 生成随机 RGB 颜色字符串
 * @returns {string} RGB 颜色字符串
 * @example
 * randomRgbString() // 返回类似 "rgb(123, 45, 200)"
 */
function randomRgbString() {
    const { r, g, b } = randomRgbColor();
    return `rgb(${r}, ${g}, ${b})`;
}

/**
 * 生成随机 RGBA 颜色
 * @param {number} [alpha] - 透明度（可选，0-1）
 * @returns {Object} RGBA 颜色对象 { r, g, b, a }
 * @example
 * randomRgbaColor() // 返回类似 { r: 123, g: 45, b: 200, a: 0.5 }
 */
function randomRgbaColor(alpha = null) {
    return {
        ...randomRgbColor(),
        a: alpha !== null ? alpha : randomFloat(0, 1, 2)
    };
}

/**
 * 生成随机 RGBA 颜色字符串
 * @param {number} [alpha] - 透明度（可选，0-1）
 * @returns {string} RGBA 颜色字符串
 * @example
 * randomRgbaString() // 返回类似 "rgba(123, 45, 200, 0.50)"
 */
function randomRgbaString(alpha = null) {
    const { r, g, b, a } = randomRgbaColor(alpha);
    return `rgba(${r}, ${g}, ${b}, ${a.toFixed(2)})`;
}

/**
 * 生成随机 HSL 颜色
 * @returns {Object} HSL 颜色对象 { h, s, l }
 * @example
 * randomHslColor() // 返回类似 { h: 180, s: 50, l: 60 }
 */
function randomHslColor() {
    return {
        h: randomInt(0, 360),
        s: randomInt(0, 100),
        l: randomInt(0, 100)
    };
}

/**
 * 生成随机 HSL 颜色字符串
 * @returns {string} HSL 颜色字符串
 * @example
 * randomHslString() // 返回类似 "hsl(180, 50%, 60%)"
 */
function randomHslString() {
    const { h, s, l } = randomHslColor();
    return `hsl(${h}, ${s}%, ${l}%)`;
}

// ============================================================================
// UUID 生成
// ============================================================================

/**
 * 生成 UUID v4
 * @returns {string} UUID 字符串
 * @example
 * uuid() // 返回类似 "550e8400-e29b-41d4-a716-446655440000"
 */
function uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * 生成短 UUID（无连字符）
 * @returns {string} 短 UUID 字符串
 * @example
 * shortUuid() // 返回类似 "550e8400e29b41d4a716446655440000"
 */
function shortUuid() {
    return uuid().replace(/-/g, '');
}

/**
 * 生成指定数量的 UUID 批量
 * @param {number} count - 数量
 * @returns {string[]} UUID 数组
 * @example
 * uuidBatch(5) // 返回5个UUID
 */
function uuidBatch(count) {
    if (typeof count !== 'number' || count < 0) {
        throw new Error('数量必须是非负数');
    }
    return Array.from({ length: count }, () => uuid());
}

// ============================================================================
// 数组操作
// ============================================================================

/**
 * 从数组中随机选择一个元素
 * @param {Array} array - 源数组
 * @returns {*} 随机选择的元素
 * @throws {Error} 如果数组为空
 * @example
 * randomChoice([1, 2, 3, 4, 5]) // 随机返回一个元素
 */
function randomChoice(array) {
    if (!Array.isArray(array) || array.length === 0) {
        throw new Error('数组必须是非空数组');
    }
    return array[randomInt(0, array.length - 1)];
}

/**
 * 从数组中随机选择多个元素（可能重复）
 * @param {Array} array - 源数组
 * @param {number} count - 选择数量
 * @returns {Array} 随机选择的元素数组
 * @example
 * randomChoices([1, 2, 3], 5) // 可能返回 [1, 3, 2, 2, 1]
 */
function randomChoices(array, count) {
    if (!Array.isArray(array) || array.length === 0) {
        throw new Error('数组必须是非空数组');
    }
    if (typeof count !== 'number' || count < 0) {
        throw new Error('数量必须是非负数');
    }
    return Array.from({ length: count }, () => randomChoice(array));
}

/**
 * 从数组中随机选择多个不重复的元素
 * @param {Array} array - 源数组
 * @param {number} count - 选择数量
 * @returns {Array} 随机选择的元素数组
 * @throws {Error} 如果请求数量超过数组长度
 * @example
 * randomSample([1, 2, 3, 4, 5], 3) // 返回3个不重复元素
 */
function randomSample(array, count) {
    if (!Array.isArray(array) || array.length === 0) {
        throw new Error('数组必须是非空数组');
    }
    if (typeof count !== 'number' || count < 0) {
        throw new Error('数量必须是非负数');
    }
    if (count > array.length) {
        throw new Error('选择数量不能超过数组长度');
    }
    
    const shuffled = shuffle([...array]);
    return shuffled.slice(0, count);
}

/**
 * 使用 Fisher-Yates 算法打乱数组
 * @param {Array} array - 源数组
 * @returns {Array} 打乱后的数组（新数组）
 * @example
 * shuffle([1, 2, 3, 4, 5]) // 返回打乱顺序的数组
 */
function shuffle(array) {
    if (!Array.isArray(array)) {
        throw new Error('参数必须是数组');
    }
    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
        const j = randomInt(0, i);
        [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
}

/**
 * 原地打乱数组（修改原数组）
 * @param {Array} array - 源数组
 * @returns {Array} 原数组引用
 * @example
 * const arr = [1, 2, 3];
 * shuffleInPlace(arr); // arr 被打乱
 */
function shuffleInPlace(array) {
    if (!Array.isArray(array)) {
        throw new Error('参数必须是数组');
    }
    for (let i = array.length - 1; i > 0; i--) {
        const j = randomInt(0, i);
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// ============================================================================
// 加权随机
// ============================================================================

/**
 * 加权随机选择
 * @param {Array<{item: *, weight: number}>} items - 带权重的项目数组
 * @returns {*} 随机选择的项目
 * @example
 * weightedChoice([
 *   { item: 'A', weight: 10 },
 *   { item: 'B', weight: 30 },
 *   { item: 'C', weight: 60 }
 * ])
 */
function weightedChoice(items) {
    if (!Array.isArray(items) || items.length === 0) {
        throw new Error('项目数组不能为空');
    }
    
    const totalWeight = items.reduce((sum, { weight }) => sum + (weight || 0), 0);
    if (totalWeight <= 0) {
        throw new Error('总权重必须大于0');
    }
    
    let random = Math.random() * totalWeight;
    
    for (const { item, weight } of items) {
        random -= weight || 0;
        if (random <= 0) {
            return item;
        }
    }
    
    return items[items.length - 1].item;
}

/**
 * 加权随机选择多个项目
 * @param {Array<{item: *, weight: number}>} items - 带权重的项目数组
 * @param {number} count - 选择数量
 * @param {boolean} [unique=false] - 是否不重复选择
 * @returns {Array} 随机选择的项目数组
 */
function weightedChoices(items, count, unique = false) {
    if (!Array.isArray(items) || items.length === 0) {
        throw new Error('项目数组不能为空');
    }
    if (unique && count > items.length) {
        throw new Error('不重复选择数量不能超过项目数量');
    }
    
    const result = [];
    let remainingItems = [...items];
    
    for (let i = 0; i < count; i++) {
        const choice = weightedChoice(remainingItems);
        result.push(choice);
        
        if (unique) {
            remainingItems = remainingItems.filter(({ item }) => item !== choice);
            if (remainingItems.length === 0) break;
        }
    }
    
    return result;
}

// ============================================================================
// 概率分布
// ============================================================================

/**
 * 生成均匀分布的随机数
 * @param {number} min - 最小值
 * @param {number} max - 最大值
 * @returns {number} 均匀分布的随机数
 */
function uniform(min, max) {
    return randomFloat(min, max);
}

/**
 * 生成正态分布（高斯分布）的随机数
 * 使用 Box-Muller 变换
 * @param {number} mean - 均值
 * @param {number} stdDev - 标准差
 * @returns {number} 正态分布的随机数
 * @example
 * normal(0, 1) // 标准正态分布
 * normal(100, 15) // 均值100，标准差15
 */
function normal(mean = 0, stdDev = 1) {
    let u1, u2;
    do {
        u1 = Math.random();
        u2 = Math.random();
    } while (u1 <= Number.EPSILON);
    
    const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    return z0 * stdDev + mean;
}

/**
 * 生成指数分布的随机数
 * @param {number} lambda - 指率参数（lambda > 0）
 * @returns {number} 指数分布的随机数
 * @example
 * exponential(0.5) // lambda = 0.5
 */
function exponential(lambda) {
    if (lambda <= 0) {
        throw new Error('lambda 必须大于 0');
    }
    let u;
    do {
        u = Math.random();
    } while (u <= Number.EPSILON);
    return -Math.log(u) / lambda;
}

/**
 * 生成泊松分布的随机数
 * @param {number} lambda - 期望值
 * @returns {number} 泊松分布的随机整数
 */
function poisson(lambda) {
    if (lambda <= 0) {
        throw new Error('lambda 必须大于 0');
    }
    const L = Math.exp(-lambda);
    let k = 0;
    let p = 1;
    do {
        k++;
        p *= Math.random();
    } while (p > L);
    return k - 1;
}

// ============================================================================
// 随机日期时间
// ============================================================================

/**
 * 生成随机日期
 * @param {Date|string|number} [start] - 开始日期（默认 1970-01-01）
 * @param {Date|string|number} [end] - 结束日期（默认今天）
 * @returns {Date} 随机日期
 * @example
 * randomDate() // 返回 1970 至今的随机日期
 * randomDate('2020-01-01', '2023-12-31') // 指定范围内的随机日期
 */
function randomDate(start = null, end = null) {
    const startDate = start ? new Date(start) : new Date(0);
    const endDate = end ? new Date(end) : new Date();
    
    if (startDate >= endDate) {
        throw new Error('开始日期必须早于结束日期');
    }
    
    const timestamp = randomInt(startDate.getTime(), endDate.getTime());
    return new Date(timestamp);
}

/**
 * 生成随机时间字符串
 * @param {boolean} [withSeconds=false] - 是否包含秒
 * @returns {string} 时间字符串 HH:MM 或 HH:MM:SS
 * @example
 * randomTime() // 返回类似 "14:30"
 * randomTime(true) // 返回类似 "14:30:45"
 */
function randomTime(withSeconds = false) {
    const hours = randomInt(0, 23).toString().padStart(2, '0');
    const minutes = randomInt(0, 59).toString().padStart(2, '0');
    
    if (withSeconds) {
        const seconds = randomInt(0, 59).toString().padStart(2, '0');
        return `${hours}:${minutes}:${seconds}`;
    }
    return `${hours}:${minutes}`;
}

/**
 * 生成随机日期时间字符串
 * @returns {string} 日期时间字符串
 * @example
 * randomDatetime() // 返回类似 "2023-06-15 14:30:45"
 */
function randomDatetime() {
    const date = randomDate();
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day} ${randomTime(true)}`;
}

// ============================================================================
// 加密安全随机
// ============================================================================

/**
 * 生成加密安全的随机整数
 * @param {number} min - 最小值
 * @param {number} max - 最大值
 * @returns {number} 加密安全的随机整数
 */
function cryptoRandomInt(min, max) {
    const range = max - min + 1;
    const bytesNeeded = Math.ceil(Math.log2(range) / 8);
    const maxValid = Math.floor((2 ** (bytesNeeded * 8)) / range) * range - 1;
    
    let randomValue;
    const crypto = require('crypto');
    
    do {
        const buffer = crypto.randomBytes(bytesNeeded);
        randomValue = buffer.readUIntBE(0, bytesNeeded);
    } while (randomValue > maxValid);
    
    return min + (randomValue % range);
}

/**
 * 生成加密安全的随机字符串
 * @param {number} length - 字符串长度
 * @param {string} [charset] - 字符集
 * @returns {string} 加密安全的随机字符串
 */
function cryptoRandomString(length, charset = ALPHANUMERIC) {
    if (typeof length !== 'number' || length < 0) {
        throw new Error('长度必须是非负数');
    }
    return Array.from(
        { length },
        () => charset[cryptoRandomInt(0, charset.length - 1)]
    ).join('');
}

/**
 * 生成加密安全的随机字节
 * @param {number} length - 字节长度
 * @returns {Buffer} 随机字节 Buffer
 */
function cryptoRandomBytes(length) {
    const crypto = require('crypto');
    return crypto.randomBytes(length);
}

// ============================================================================
// 其他实用函数
// ============================================================================

/**
 * 从枚举值中随机选择
 * @param {Object} enumObj - 枚举对象
 * @returns {*} 随机枚举值
 * @example
 * const Status = { PENDING: 'pending', ACTIVE: 'active', DONE: 'done' };
 * randomEnum(Status) // 随机返回一个状态值
 */
function randomEnum(enumObj) {
    const values = Object.values(enumObj);
    return randomChoice(values);
}

/**
 * 生成随机 IP 地址（IPv4）
 * @returns {string} IPv4 地址
 * @example
 * randomIPv4() // 返回类似 "192.168.1.100"
 */
function randomIPv4() {
    return Array.from({ length: 4 }, () => randomInt(0, 255)).join('.');
}

/**
 * 生成随机 MAC 地址
 * @param {string} [separator=':'] - 分隔符
 * @returns {string} MAC 地址
 * @example
 * randomMAC() // 返回类似 "00:1A:2B:3C:4D:5E"
 */
function randomMAC(separator = ':') {
    const parts = Array.from({ length: 6 }, () => randomHex(2).toUpperCase());
    return parts.join(separator);
}

/**
 * 生成随机端口号
 * @param {boolean} [wellKnownOnly=false] - 是否仅返回知名端口
 * @returns {number} 端口号
 * @example
 * randomPort() // 返回 1-65535 之间的端口
 * randomPort(true) // 返回 1-1023 之间的知名端口
 */
function randomPort(wellKnownOnly = false) {
    return wellKnownOnly ? randomInt(1, 1023) : randomInt(1, 65535);
}

/**
 * 生成随机用户名
 * @param {Object} [options] - 选项
 * @param {number} [options.minLength=5] - 最小长度
 * @param {number} [options.maxLength=15] - 最大长度
 * @returns {string} 用户名
 * @example
 * randomUsername() // 返回类似 "cooluser123"
 */
function randomUsername(options = {}) {
    const { minLength = 5, maxLength = 15 } = options;
    const length = randomInt(minLength, maxLength);
    const firstChar = randomAlpha(1, true);
    const rest = randomString(length - 1, { lowercase: true, uppercase: false, digits: true });
    return firstChar + rest;
}

/**
 * 生成随机邮箱
 * @param {string[]} [domains] - 域名列表
 * @returns {string} 邮箱地址
 * @example
 * randomEmail() // 返回类似 "user123@example.com"
 */
function randomEmail(domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com']) {
    const username = randomUsername({ minLength: 5, maxLength: 12 });
    const domain = randomChoice(domains);
    return `${username}@${domain}`;
}

/**
 * 生成随机 URL
 * @param {Object} [options] - 选项
 * @param {string[]} [options.domains] - 域名列表
 * @param {string[]} [options.paths] - 路径列表
 * @returns {string} URL
 */
function randomUrl(options = {}) {
    const { 
        domains = ['example.com', 'test.org', 'demo.net'],
        paths = ['', 'api', 'user', 'data', 'search']
    } = options;
    
    const protocol = randomBool() ? 'https' : 'http';
    const domain = randomChoice(domains);
    const path = randomChoice(paths);
    const hasQuery = randomBool();
    
    let url = `${protocol}://${domain}`;
    if (path) {
        url += `/${path}`;
    }
    if (hasQuery) {
        url += `?id=${randomString(8, { charset: ALPHANUMERIC })}`;
    }
    
    return url;
}

/**
 * 生成随机中国手机号
 * @returns {string} 手机号
 * @example
 * randomChinesePhone() // 返回类似 "13812345678"
 */
function randomChinesePhone() {
    const prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                      '150', '151', '152', '153', '155', '156', '157', '158', '159',
                      '170', '176', '177', '178',
                      '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
                      '191', '199'];
    const prefix = randomChoice(prefixes);
    const suffix = randomNumeric(8);
    return prefix + suffix;
}

/**
 * 随机延迟执行
 * @param {number} minMs - 最小延迟毫秒
 * @param {number} maxMs - 最大延迟毫秒
 * @returns {Promise<void>} Promise
 * @example
 * await randomDelay(100, 500) // 随机延迟 100-500ms
 */
function randomDelay(minMs, maxMs) {
    const delay = randomInt(minMs, maxMs);
    return new Promise(resolve => setTimeout(resolve, delay));
}

// ============================================================================
// 导出
// ============================================================================

module.exports = {
    // 常量
    ALPHABET_LOWERCASE,
    ALPHABET_UPPERCASE,
    ALPHABET,
    DIGITS,
    ALPHANUMERIC,
    SPECIAL_CHARS,
    HEX_CHARS,
    
    // 基础随机数
    randomInt,
    randomFloat,
    randomBool,
    
    // 随机字符串
    randomString,
    randomHex,
    randomNumeric,
    randomAlpha,
    randomPassword,
    
    // 随机颜色
    randomHexColor,
    randomRgbColor,
    randomRgbString,
    randomRgbaColor,
    randomRgbaString,
    randomHslColor,
    randomHslString,
    
    // UUID
    uuid,
    shortUuid,
    uuidBatch,
    
    // 数组操作
    randomChoice,
    randomChoices,
    randomSample,
    shuffle,
    shuffleInPlace,
    
    // 加权随机
    weightedChoice,
    weightedChoices,
    
    // 概率分布
    uniform,
    normal,
    exponential,
    poisson,
    
    // 随机日期时间
    randomDate,
    randomTime,
    randomDatetime,
    
    // 加密安全随机
    cryptoRandomInt,
    cryptoRandomString,
    cryptoRandomBytes,
    
    // 其他实用函数
    randomEnum,
    randomIPv4,
    randomMAC,
    randomPort,
    randomUsername,
    randomEmail,
    randomUrl,
    randomChinesePhone,
    randomDelay
};