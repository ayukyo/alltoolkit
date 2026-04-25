/**
 * Base58 编码/解码工具模块
 * 
 * Base58 是一种二进制到文本的编码方案，主要用于：
 * - Bitcoin 地址编码
 * - IPFS 内容标识符
 * - URL 短链接
 * 
 * 特点：去除了容易混淆的字符 0, O, I, l，以及非字母数字字符 +, /
 */

// Bitcoin 风格的 Base58 字母表（最常用）
const BITCOIN_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

// Flickr 风格的 Base58 字母表
const FLICKR_ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ';

// Ripple 风格的 Base58 字母表
const RIPPLE_ALPHABET = 'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz';

/**
 * Base58 编码器类
 */
export class Base58Encoder {
    private alphabet: string;
    private alphabetMap: Map<string, number>;

    constructor(alphabet: string = BITCOIN_ALPHABET) {
        if (alphabet.length !== 58) {
            throw new Error('Base58 alphabet must contain exactly 58 characters');
        }
        this.alphabet = alphabet;
        this.alphabetMap = new Map();
        for (let i = 0; i < alphabet.length; i++) {
            this.alphabetMap.set(alphabet[i], i);
        }
    }

    /**
     * 将字节数组编码为 Base58 字符串
     * @param bytes 要编码的字节数组
     * @returns Base58 编码字符串
     */
    encode(bytes: Uint8Array): string {
        if (bytes.length === 0) {
            return '';
        }

        // 计算前导零的数量
        let leadingZeros = 0;
        for (let i = 0; i < bytes.length; i++) {
            if (bytes[i] === 0) {
                leadingZeros++;
            } else {
                break;
            }
        }

        // 使用 BigInt 进行精确计算
        let num = BigInt(0);
        for (let i = leadingZeros; i < bytes.length; i++) {
            num = num * BigInt(256) + BigInt(bytes[i]);
        }

        // 转换为 Base58
        const chars: string[] = [];
        while (num > 0) {
            const remainder = num % BigInt(58);
            chars.push(this.alphabet[Number(remainder)]);
            num = num / BigInt(58);
        }

        // 添加前导字符（alphabet[0] 代表零）
        for (let i = 0; i < leadingZeros; i++) {
            chars.push(this.alphabet[0]);
        }

        return chars.reverse().join('');
    }

    /**
     * 将字符串编码为 Base58
     * @param str 要编码的字符串（UTF-8）
     * @returns Base58 编码字符串
     */
    encodeString(str: string): string {
        const encoder = new TextEncoder();
        const bytes = encoder.encode(str);
        return this.encode(bytes);
    }

    /**
     * 将十六进制字符串编码为 Base58
     * @param hex 十六进制字符串
     * @returns Base58 编码字符串
     */
    encodeHex(hex: string): string {
        const bytes = this.hexToBytes(hex);
        return this.encode(bytes);
    }

    /**
     * 将 Base58 字符串解码为字节数组
     * @param str Base58 编码字符串
     * @returns 解码后的字节数组
     */
    decode(str: string): Uint8Array {
        if (str.length === 0) {
            return new Uint8Array(0);
        }

        // 验证并计算前导零字符的数量
        let leadingZeros = 0;
        for (let i = 0; i < str.length; i++) {
            if (str[i] === this.alphabet[0]) {
                leadingZeros++;
            } else {
                break;
            }
        }

        // 使用 BigInt 进行精确计算
        let num = BigInt(0);
        for (let i = leadingZeros; i < str.length; i++) {
            const val = this.alphabetMap.get(str[i]);
            if (val === undefined) {
                throw new Error(`Invalid Base58 character: ${str[i]}`);
            }
            num = num * BigInt(58) + BigInt(val);
        }

        // 转换为字节数组
        const bytes: number[] = [];
        while (num > 0) {
            bytes.push(Number(num % BigInt(256)));
            num = num / BigInt(256);
        }

        // 添加前导零字节
        const result: number[] = [];
        for (let i = 0; i < leadingZeros; i++) {
            result.push(0);
        }

        // 反转字节数组并添加到结果
        for (let i = bytes.length - 1; i >= 0; i--) {
            result.push(bytes[i]);
        }

        return new Uint8Array(result);
    }

    /**
     * 将 Base58 字符串解码为字符串（UTF-8）
     * @param str Base58 编码字符串
     * @returns 解码后的字符串
     */
    decodeString(str: string): string {
        const bytes = this.decode(str);
        const decoder = new TextDecoder();
        return decoder.decode(bytes);
    }

    /**
     * 将 Base58 字符串解码为十六进制字符串
     * @param str Base58 编码字符串
     * @returns 十六进制字符串
     */
    decodeToHex(str: string): string {
        const bytes = this.decode(str);
        return this.bytesToHex(bytes);
    }

    /**
     * 验证 Base58 字符串是否有效
     * @param str 要验证的字符串
     * @returns 是否有效
     */
    isValid(str: string): boolean {
        for (const char of str) {
            if (!this.alphabetMap.has(char)) {
                return false;
            }
        }
        return true;
    }

    /**
     * 十六进制字符串转字节数组
     */
    private hexToBytes(hex: string): Uint8Array {
        if (hex.length === 0) {
            return new Uint8Array(0);
        }
        if (hex.length % 2 !== 0) {
            hex = '0' + hex;
        }
        const bytes = new Uint8Array(hex.length / 2);
        for (let i = 0; i < hex.length; i += 2) {
            bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
        }
        return bytes;
    }

    /**
     * 字节数组转十六进制字符串
     */
    private bytesToHex(bytes: Uint8Array): string {
        return Array.from(bytes)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }
}

// 预定义的编码器实例
export const base58 = new Base58Encoder(BITCOIN_ALPHABET);
export const base58Flickr = new Base58Encoder(FLICKR_ALPHABET);
export const base58Ripple = new Base58Encoder(RIPPLE_ALPHABET);

/**
 * 快捷编码函数（使用 Bitcoin 字母表）
 */
export function encodeBase58(bytes: Uint8Array): string {
    return base58.encode(bytes);
}

/**
 * 快捷解码函数（使用 Bitcoin 字母表）
 */
export function decodeBase58(str: string): Uint8Array {
    return base58.decode(str);
}

/**
 * 编码字符串为 Base58
 */
export function encodeBase58String(str: string): string {
    return base58.encodeString(str);
}

/**
 * 解码 Base58 为字符串
 */
export function decodeBase58String(str: string): string {
    return base58.decodeString(str);
}

/**
 * 编码十六进制为 Base58
 */
export function encodeBase58Hex(hex: string): string {
    return base58.encodeHex(hex);
}

/**
 * 解码 Base58 为十六进制
 */
export function decodeBase58ToHex(str: string): string {
    return base58.decodeToHex(str);
}

/**
 * 验证 Base58 字符串
 */
export function isValidBase58(str: string): boolean {
    return base58.isValid(str);
}

/**
 * 生成随机 Base58 字符串
 * @param length 目标长度
 * @param encoder 可选的编码器实例
 * @returns 随机 Base58 字符串
 */
export function randomBase58(length: number, encoder: Base58Encoder = base58): string {
    // 使用私有属性访问字母表
    const alphabet = (encoder as unknown as { alphabet: string }).alphabet;
    let result = '';
    const randomValues = new Uint8Array(length);
    // 使用 crypto API（Node.js 和浏览器都支持）
    const cryptoModule = typeof crypto !== 'undefined' ? crypto : require('crypto');
    cryptoModule.getRandomValues(randomValues);
    for (let i = 0; i < length; i++) {
        result += alphabet[randomValues[i] % 58];
    }
    return result;
}

/**
 * 将 BigInt 转换为 Base58 字符串
 * @param value BigInt 值
 * @param encoder 可选的编码器实例
 * @returns Base58 编码字符串
 */
export function bigIntToBase58(value: bigint, encoder: Base58Encoder = base58): string {
    if (value < 0n) {
        throw new Error('Cannot encode negative BigInt');
    }
    if (value === 0n) {
        const alphabet = (encoder as unknown as { alphabet: string }).alphabet;
        return alphabet[0];
    }

    const alphabet = (encoder as unknown as { alphabet: string }).alphabet;
    const chars: string[] = [];
    
    while (value > 0n) {
        const remainder = Number(value % 58n);
        chars.push(alphabet[remainder]);
        value = value / 58n;
    }

    return chars.reverse().join('');
}

/**
 * 将 Base58 字符串转换为 BigInt
 * @param str Base58 字符串
 * @param encoder 可选的编码器实例
 * @returns BigInt 值
 */
export function base58ToBigInt(str: string, encoder: Base58Encoder = base58): bigint {
    const alphabetMap = (encoder as unknown as { alphabetMap: Map<string, number> }).alphabetMap;
    let result = 0n;
    
    for (const char of str) {
        const value = alphabetMap.get(char);
        if (value === undefined) {
            throw new Error(`Invalid Base58 character: ${char}`);
        }
        result = result * 58n + BigInt(value);
    }

    return result;
}

/**
 * 计算字符串的 Base58 校验和
 * @param data 输入数据
 * @param length 校验和长度（默认 4）
 * @returns Base58 编码的字符串（带校验和）
 */
export function encodeWithChecksum(data: Uint8Array, length: number = 4): string {
    // 使用简单的哈希算法计算校验和
    const hash = simpleHash(data);
    const checksum = hash.slice(0, length);
    const combined = new Uint8Array(data.length + checksum.length);
    combined.set(data);
    combined.set(checksum, data.length);
    return base58.encode(combined);
}

/**
 * 验证并解码带校验和的 Base58 字符串
 * @param str Base58 编码字符串（带校验和）
 * @param length 校验和长度（默认 4）
 * @returns 解码后的数据，校验失败返回 null
 */
export function decodeWithChecksum(str: string, length: number = 4): Uint8Array | null {
    try {
        const combined = base58.decode(str);
        if (combined.length < length) {
            return null;
        }

        const data = combined.slice(0, combined.length - length);
        const checksum = combined.slice(combined.length - length);
        const expectedChecksum = simpleHash(data).slice(0, length);

        // 比较校验和
        for (let i = 0; i < length; i++) {
            if (checksum[i] !== expectedChecksum[i]) {
                return null;
            }
        }

        return data;
    } catch {
        return null;
    }
}

/**
 * 简单哈希函数（用于校验和）
 */
function simpleHash(data: Uint8Array): Uint8Array {
    const result = new Uint8Array(32);
    let h = 0x811c9dc5;
    
    for (const byte of data) {
        h ^= byte;
        h = Math.imul(h, 0x01000193);
    }
    
    // 扩展到 32 字节
    const view = new DataView(result.buffer);
    view.setUint32(0, h, true);
    
    // 继续混合
    for (let i = 4; i < 32; i++) {
        result[i] = (result[i - 4] * 31 + result[(i - 1) % 4]) ^ (h >> ((i % 4) * 8));
    }
    
    return result;
}

// 导出类型
export type {};