/**
 * ISBN Utils - 国际标准书号工具模块
 * 
 * 功能：
 * - ISBN-10 和 ISBN-13 验证
 * - ISBN 格式转换（10位转13位，13位转10位）
 * - 校验位计算
 * - 随机生成有效 ISBN（用于测试）
 * - ISBN 解析和格式化
 * 
 * 零外部依赖，纯 JavaScript 实现。
 */

/**
 * ISBN 相关错误基类
 */
class ISBNError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ISBNError';
    }
}

/**
 * 无效的 ISBN 错误
 */
class InvalidISBNError extends ISBNError {
    constructor(message) {
        super(message);
        this.name = 'InvalidISBNError';
    }
}

/**
 * ISBN 转换错误
 */
class ISBNConversionError extends ISBNError {
    constructor(message) {
        super(message);
        this.name = 'ISBNConversionError';
    }
}

/**
 * ISBN 工具类
 */
class ISBNUtils {
    // ISBN-13 前缀
    static ISBN_13_PREFIX = '978';
    static ISBN_13_PREFIX_ALT = '979'; // 新的前缀，用于 ISBN-10 用尽后

    /**
     * 清理 ISBN 字符串，移除所有非数字字符（保留 X）
     * @param {string} isbn - 原始 ISBN 字符串
     * @returns {string} 清理后的纯数字字符串（可能包含 X）
     */
    static clean(isbn) {
        return String(isbn).replace(/[^0-9Xx]/g, '').toUpperCase();
    }

    /**
     * 检测 ISBN 版本
     * @param {string} isbn - ISBN 字符串
     * @returns {number|null} 10 或 13，如果无法识别返回 null
     */
    static detectVersion(isbn) {
        const cleaned = ISBNUtils.clean(isbn);
        if (cleaned.length === 10) return 10;
        if (cleaned.length === 13) return 13;
        return null;
    }

    /**
     * 计算 ISBN-10 校验位
     * 
     * ISBN-10 校验位计算：
     * - 前9位数字分别乘以 10, 9, 8, ..., 2
     * - 求和
     * - 对 11 取模
     * - 结果为 11 - (sum % 11)，如果为 10 则为 X
     * 
     * @param {string} isbn9 - ISBN-10 的前9位数字
     * @returns {string} 校验位（0-9 或 X）
     * @throws {InvalidISBNError} 如果输入无效
     */
    static calculateCheckDigit10(isbn9) {
        if (isbn9.length !== 9 || !/^\d{9}$/.test(isbn9)) {
            throw new InvalidISBNError('需要9位数字来计算 ISBN-10 校验位');
        }

        let total = 0;
        for (let i = 0; i < 9; i++) {
            total += parseInt(isbn9[i]) * (10 - i);
        }

        const remainder = total % 11;
        const check = (11 - remainder) % 11;

        return check === 10 ? 'X' : String(check);
    }

    /**
     * 计算 ISBN-13 校验位
     * 
     * ISBN-13 校验位计算：
     * - 前12位数字，奇数位乘以1，偶数位乘以3
     * - 求和
     * - 对 10 取模
     * - 结果为 (10 - (sum % 10)) % 10
     * 
     * @param {string} isbn12 - ISBN-13 的前12位数字
     * @returns {string} 校验位（0-9）
     * @throws {InvalidISBNError} 如果输入无效
     */
    static calculateCheckDigit12(isbn12) {
        if (isbn12.length !== 12 || !/^\d{12}$/.test(isbn12)) {
            throw new InvalidISBNError('需要12位数字来计算 ISBN-13 校验位');
        }

        let total = 0;
        for (let i = 0; i < 12; i++) {
            total += parseInt(isbn12[i]) * (i % 2 === 0 ? 1 : 3);
        }

        return String((10 - (total % 10)) % 10);
    }

    /**
     * 验证 ISBN 是否有效
     * @param {string} isbn - ISBN 字符串（可以是 ISBN-10 或 ISBN-13）
     * @returns {boolean} True 如果有效，False 否则
     */
    static validate(isbn) {
        try {
            ISBNUtils.validateStrict(isbn);
            return true;
        } catch (e) {
            return false;
        }
    }

    /**
     * 严格验证 ISBN 并返回详细信息
     * @param {string} isbn - ISBN 字符串
     * @returns {Object} 包含验证信息的对象
     * @throws {InvalidISBNError} 如果 ISBN 无效
     */
    static validateStrict(isbn) {
        const cleaned = ISBNUtils.clean(isbn);
        const version = ISBNUtils.detectVersion(cleaned);

        if (version === 10) {
            return ISBNUtils._validateISBN10(cleaned);
        } else if (version === 13) {
            return ISBNUtils._validateISBN13(cleaned);
        } else {
            throw new InvalidISBNError(
                `无效的 ISBN 格式：${isbn}（清理后长度：${cleaned.length}）`
            );
        }
    }

    /**
     * 验证 ISBN-10
     * @private
     */
    static _validateISBN10(isbn) {
        if (isbn.length !== 10) {
            throw new InvalidISBNError(`ISBN-10 长度必须为 10，当前：${isbn.length}`);
        }

        // 前9位必须是数字
        if (!/^\d{9}/.test(isbn)) {
            throw new InvalidISBNError('ISBN-10 前9位必须是数字');
        }

        // 最后一位可以是数字或 X
        if (!/[\dX]/.test(isbn[9])) {
            throw new InvalidISBNError('ISBN-10 最后一位必须是数字或 X');
        }

        const expectedCheck = ISBNUtils.calculateCheckDigit10(isbn.slice(0, 9));
        const actualCheck = isbn[9];

        if (expectedCheck !== actualCheck) {
            throw new InvalidISBNError(
                `ISBN-10 校验位错误：期望 ${expectedCheck}，实际 ${actualCheck}`
            );
        }

        return {
            valid: true,
            version: 10,
            isbn: isbn,
            isbnFormatted: ISBNUtils.format(isbn),
            checkDigit: actualCheck
        };
    }

    /**
     * 验证 ISBN-13
     * @private
     */
    static _validateISBN13(isbn) {
        if (isbn.length !== 13 || !/^\d{13}$/.test(isbn)) {
            throw new InvalidISBNError('ISBN-13 必须是 13 位数字');
        }

        // 检查前缀
        if (!isbn.startsWith('978') && !isbn.startsWith('979')) {
            throw new InvalidISBNError('ISBN-13 必须以 978 或 979 开头');
        }

        const expectedCheck = ISBNUtils.calculateCheckDigit12(isbn.slice(0, 12));
        const actualCheck = isbn[12];

        if (expectedCheck !== actualCheck) {
            throw new InvalidISBNError(
                `ISBN-13 校验位错误：期望 ${expectedCheck}，实际 ${actualCheck}`
            );
        }

        return {
            valid: true,
            version: 13,
            isbn: isbn,
            isbnFormatted: ISBNUtils.format(isbn),
            checkDigit: actualCheck,
            prefix: isbn.slice(0, 3)
        };
    }

    /**
     * 将 ISBN-10 转换为 ISBN-13
     * @param {string} isbn - ISBN-10 字符串
     * @returns {string} ISBN-13 字符串
     * @throws {ISBNConversionError} 如果转换失败
     */
    static convertTo13(isbn) {
        const cleaned = ISBNUtils.clean(isbn);

        if (cleaned.length === 13) {
            return cleaned; // 已经是 ISBN-13
        }

        if (cleaned.length !== 10) {
            throw new ISBNConversionError(`无法转换：${isbn}（不是有效的 ISBN-10）`);
        }

        // 先验证 ISBN-10
        try {
            ISBNUtils._validateISBN10(cleaned);
        } catch (e) {
            throw new ISBNConversionError(`无法转换无效的 ISBN-10：${e.message}`);
        }

        // 添加 978 前缀（去掉原校验位）
        const isbn12 = '978' + cleaned.slice(0, 9);

        // 计算新的校验位
        const checkDigit = ISBNUtils.calculateCheckDigit12(isbn12);

        return isbn12 + checkDigit;
    }

    /**
     * 将 ISBN-13 转换为 ISBN-10
     * 
     * 注意：只有 978 前缀的 ISBN-13 可以转换为 ISBN-10
     * 979 前缀的 ISBN-13 没有对应的 ISBN-10
     * 
     * @param {string} isbn - ISBN-13 字符串
     * @returns {string} ISBN-10 字符串
     * @throws {ISBNConversionError} 如果转换失败
     */
    static convertTo10(isbn) {
        const cleaned = ISBNUtils.clean(isbn);

        if (cleaned.length === 10) {
            return cleaned; // 已经是 ISBN-10
        }

        if (cleaned.length !== 13) {
            throw new ISBNConversionError(`无法转换：${isbn}（不是有效的 ISBN-13）`);
        }

        // 验证 ISBN-13
        try {
            ISBNUtils._validateISBN13(cleaned);
        } catch (e) {
            throw new ISBNConversionError(`无法转换无效的 ISBN-13：${e.message}`);
        }

        // 只有 978 前缀可以转换
        if (!cleaned.startsWith('978')) {
            throw new ISBNConversionError(
                `只有 978 前缀的 ISBN-13 可以转换为 ISBN-10，当前前缀：${cleaned.slice(0, 3)}`
            );
        }

        // 去掉前缀和校验位，得到 ISBN-10 的前9位
        const isbn9 = cleaned.slice(3, 12);

        // 计算新的校验位
        const checkDigit = ISBNUtils.calculateCheckDigit10(isbn9);

        return isbn9 + checkDigit;
    }

    /**
     * 格式化 ISBN 为标准显示格式
     * 
     * 简化版格式（均匀分割）：
     * ISBN-10: X-XXXX-XXXX-X
     * ISBN-13: XXX-X-XXXX-XXXX-X
     * 
     * @param {string} isbn - ISBN 字符串
     * @param {string} separator - 分隔符，默认为 '-'
     * @returns {string} 格式化后的 ISBN 字符串
     */
    static format(isbn, separator = '-') {
        const cleaned = ISBNUtils.clean(isbn);
        const version = ISBNUtils.detectVersion(cleaned);

        if (version === 10) {
            // ISBN-10: X-XXXX-XXXX-X
            return [
                cleaned.slice(0, 1),
                cleaned.slice(1, 5),
                cleaned.slice(5, 9),
                cleaned.slice(9)
            ].join(separator);
        } else if (version === 13) {
            // ISBN-13: XXX-X-XXXX-XXXX-X
            return [
                cleaned.slice(0, 3),
                cleaned[3],
                cleaned.slice(4, 8),
                cleaned.slice(8, 12),
                cleaned[12]
            ].join(separator);
        }

        return isbn; // 无法识别格式，返回原值
    }

    /**
     * 解析 ISBN 并返回详细信息
     * @param {string} isbn - ISBN 字符串
     * @returns {Object} 包含解析信息的对象
     */
    static parse(isbn) {
        const cleaned = ISBNUtils.clean(isbn);
        const version = ISBNUtils.detectVersion(cleaned);

        const result = {
            original: isbn,
            cleaned: cleaned,
            version: version,
            valid: false
        };

        if (version === null) {
            result.error = `无法识别的 ISBN 格式，长度：${cleaned.length}`;
            return result;
        }

        try {
            const validation = ISBNUtils.validateStrict(cleaned);
            Object.assign(result, validation);
            result.valid = true;

            if (version === 10) {
                // 尝试转换为 ISBN-13
                try {
                    result.isbn13 = ISBNUtils.convertTo13(cleaned);
                } catch (e) {
                    // 忽略转换失败
                }
            } else if (version === 13) {
                // 尝试转换为 ISBN-10
                try {
                    result.isbn10 = ISBNUtils.convertTo10(cleaned);
                } catch (e) {
                    result.isbn10 = null; // 979 前缀无法转换
                }
            }
        } catch (e) {
            result.error = e.message;
        }

        return result;
    }

    /**
     * 生成随机有效 ISBN（用于测试）
     * @param {number} version - ISBN 版本，10 或 13
     * @param {string|null} prefix - ISBN-13 的前缀（仅用于 version=13），默认随机
     * @returns {string} 随机生成的有效 ISBN 字符串
     * @throws {Error} 如果版本不是 10 或 13
     */
    static generateRandom(version = 13, prefix = null) {
        if (version === 10) {
            // 生成随机的前9位
            let isbn9 = '';
            for (let i = 0; i < 9; i++) {
                isbn9 += Math.floor(Math.random() * 10);
            }
            const check = ISBNUtils.calculateCheckDigit10(isbn9);
            return isbn9 + check;
        } else if (version === 13) {
            // 选择前缀
            if (prefix === null) {
                prefix = Math.random() < 0.5 ? '978' : '979';
            }

            if (prefix !== '978' && prefix !== '979') {
                throw new Error('ISBN-13 前缀必须是 978 或 979');
            }

            // 生成随机的后9位（共12位）
            let isbn12 = prefix;
            for (let i = 0; i < 9; i++) {
                isbn12 += Math.floor(Math.random() * 10);
            }
            const check = ISBNUtils.calculateCheckDigit12(isbn12);
            return isbn12 + check;
        } else {
            throw new Error('版本必须是 10 或 13');
        }
    }

    /**
     * 批量生成随机有效 ISBN
     * @param {number} count - 生成数量
     * @param {number} version - ISBN 版本，10 或 13
     * @returns {string[]} ISBN 字符串数组
     */
    static generateBatch(count, version = 13) {
        const result = [];
        for (let i = 0; i < count; i++) {
            result.push(ISBNUtils.generateRandom(version));
        }
        return result;
    }

    /**
     * 从文本中提取所有 ISBN
     * @param {string} text - 要搜索的文本
     * @returns {string[]} 找到的 ISBN 列表（已验证有效）
     */
    static extractFromText(text) {
        // 匹配可能的 ISBN 模式
        const patterns = [
            // ISBN-13 模式
            /(?:ISBN[-\s]?)?(97[89][-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dX])/gi,
            // ISBN-10 模式
            /(?:ISBN[-\s]?)?(\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dXx])/gi
        ];

        const found = new Set();

        for (const pattern of patterns) {
            const matches = text.match(pattern);
            if (matches) {
                for (const match of matches) {
                    const cleaned = ISBNUtils.clean(match);
                    if (ISBNUtils.validate(cleaned)) {
                        found.add(cleaned);
                    }
                }
            }
        }

        return Array.from(found);
    }

    /**
     * 获取 ISBN 的注册组（国家/地区/语言区）
     * 
     * 这是一个简化版本，只识别常见的组区号
     * 
     * @param {string} isbn - ISBN 字符串
     * @returns {string|null} 注册组名称，如果无法识别返回 null
     */
    static getRegistrationGroup(isbn) {
        const cleaned = ISBNUtils.clean(isbn);

        // 提取组区号部分
        let groupPart;
        if (cleaned.length === 13) {
            // ISBN-13: 去掉 978/979 前缀
            groupPart = cleaned.slice(3);
        } else if (cleaned.length === 10) {
            groupPart = cleaned;
        } else {
            return null;
        }

        // 常见组区号映射（简化版）
        const groupMap = {
            '0': '英语区',
            '1': '英语区',
            '2': '法语区',
            '3': '德语区',
            '4': '日本',
            '5': '俄语区',
            '7': '中国',
            '80': '捷克/斯洛伐克',
            '81': '印度',
            '82': '挪威',
            '83': '波兰',
            '84': '西班牙',
            '85': '巴西',
            '86': '塞尔维亚',
            '87': '丹麦',
            '88': '意大利',
            '89': '韩国',
            '90': '荷兰/比利时',
            '91': '瑞典',
            '92': '国际组织',
            '93': '印度',
            '94': '荷兰',
            '95': '伊朗',
            '96': '台湾',
            '97': '泰国',
            '98': '伊朗',
            '99': '其他国家'
        };

        // 尝试匹配（从长到短）
        for (const length of [2, 1]) {
            if (groupPart.length >= length) {
                const group = groupPart.slice(0, length);
                if (groupMap[group]) {
                    return groupMap[group];
                }
            }
        }

        return null;
    }
}

// 便捷函数
function validate(isbn) {
    return ISBNUtils.validate(isbn);
}

function validateStrict(isbn) {
    return ISBNUtils.validateStrict(isbn);
}

function convertTo13(isbn) {
    return ISBNUtils.convertTo13(isbn);
}

function convertTo10(isbn) {
    return ISBNUtils.convertTo10(isbn);
}

function formatISBN(isbn, separator = '-') {
    return ISBNUtils.format(isbn, separator);
}

function parseISBN(isbn) {
    return ISBNUtils.parse(isbn);
}

function generateRandomISBN(version = 13, prefix = null) {
    return ISBNUtils.generateRandom(version, prefix);
}

function extractISBNFromText(text) {
    return ISBNUtils.extractFromText(text);
}

// 导出
module.exports = {
    // 类
    ISBNError,
    InvalidISBNError,
    ISBNConversionError,
    ISBNUtils,
    // 便捷函数
    validate,
    validateStrict,
    convertTo13,
    convertTo10,
    formatISBN,
    parseISBN,
    generateRandomISBN,
    extractISBNFromText
};