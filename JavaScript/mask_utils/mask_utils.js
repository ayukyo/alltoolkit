/**
 * mask_utils - 数据脱敏/格式化工具
 * 提供敏感信息脱敏、格式化和验证功能
 * 零外部依赖，纯 JavaScript 实现
 */

/**
 * 默认脱敏字符
 */
const DEFAULT_MASK_CHAR = '*';

/**
 * 脱敏选项
 * @typedef {Object} MaskOptions
 * @property {string} maskChar - 脱敏字符，默认 '*'
 * @property {number} showFirst - 显示前几位
 * @property {number} showLast - 显示后几位
 * @property {string} separator - 分隔符
 */

/**
 * 手机号脱敏
 * @param {string} phone - 手机号码
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的手机号
 * @example
 * maskPhone('13812345678') // '138****5678'
 * maskPhone('13812345678', { showFirst: 3, showLast: 4 }) // '138****5678'
 * maskPhone('13812345678', { maskChar: 'x' }) // '138xxxx5678'
 */
function maskPhone(phone, options = {}) {
    if (!phone || typeof phone !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 3, showLast = 4 } = options;
    const cleaned = phone.replace(/\D/g, '');
    
    if (cleaned.length < showFirst + showLast) {
        return phone; // 号码太短，原样返回
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middle = maskChar.repeat(cleaned.length - showFirst - showLast);
    
    return first + middle + last;
}

/**
 * 固定电话脱敏
 * @param {string} tel - 固定电话号码
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的固话
 * @example
 * maskTelephone('010-12345678') // '010-****5678'
 */
function maskTelephone(tel, options = {}) {
    if (!tel || typeof tel !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 3, showLast = 4 } = options;
    const cleaned = tel.replace(/\D/g, '');
    
    if (cleaned.length < showFirst + showLast) {
        return tel;
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middle = maskChar.repeat(cleaned.length - showFirst - showLast);
    
    return first + '-' + middle + '-' + last;
}

/**
 * 身份证号脱敏
 * @param {string} idCard - 身份证号码
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的身份证号
 * @example
 * maskIdCard('110101199001011234') // '110101********1234'
 */
function maskIdCard(idCard, options = {}) {
    if (!idCard || typeof idCard !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 6, showLast = 4 } = options;
    const cleaned = idCard.replace(/\s/g, '').toUpperCase();
    
    if (cleaned.length < showFirst + showLast) {
        return cleaned;
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middle = maskChar.repeat(8); // 身份证中间固定脱敏8位
    
    return first + middle + last;
}

/**
 * 银行卡号脱敏
 * @param {string} bankCard - 银行卡号
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的银行卡号
 * @example
 * maskBankCard('6222021234567890123') // '6222 **** **** 0123'
 */
function maskBankCard(bankCard, options = {}) {
    if (!bankCard || typeof bankCard !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 4, showLast = 4 } = options;
    const cleaned = bankCard.replace(/\s/g, '');
    
    if (cleaned.length < showFirst + showLast) {
        return cleaned;
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middleLength = cleaned.length - showFirst - showLast;
    
    // 格式化为 4位一组
    const maskedMiddle = ' ' + maskChar.repeat(4) + ' ' + maskChar.repeat(4) + ' ';
    return first + maskedMiddle + last;
}

/**
 * 邮箱脱敏
 * @param {string} email - 邮箱地址
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的邮箱
 * @example
 * maskEmail('example@domain.com') // 'e*****@domain.com'
 */
function maskEmail(email, options = {}) {
    if (!email || typeof email !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 1 } = options;
    const atIndex = email.indexOf('@');
    
    if (atIndex < 1) {
        return email; // 无效邮箱
    }
    
    const localPart = email.slice(0, atIndex);
    const domainPart = email.slice(atIndex);
    
    if (localPart.length <= showFirst) {
        return maskChar.repeat(localPart.length) + domainPart;
    }
    
    const first = localPart.slice(0, showFirst);
    const middle = maskChar.repeat(localPart.length - showFirst);
    
    return first + middle + domainPart;
}

/**
 * 姓名脱敏
 * @param {string} name - 姓名
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的姓名
 * @example
 * maskName('张三') // '张*'
 * maskName('张小明') // '张**'
 */
function maskName(name, options = {}) {
    if (!name || typeof name !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 1 } = options;
    const trimmed = name.trim();
    
    if (trimmed.length <= showFirst) {
        return trimmed; // 单字姓名不脱敏
    }
    
    const first = trimmed.slice(0, showFirst);
    const middle = maskChar.repeat(trimmed.length - showFirst);
    
    return first + middle;
}

/**
 * 地址脱敏
 * @param {string} address - 地址
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的地址
 * @example
 * maskAddress('北京市朝阳区望京街道') // '北京市朝阳区****'
 */
function maskAddress(address, options = {}) {
    if (!address || typeof address !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showLast = 0 } = options;
    
    // 保留省市区信息
    const provinceMatch = address.match(/^(.{2,3}?[省市自治区])/);
    const cityMatch = address.match(/^(.+?[市盟地区])/);
    const districtMatch = address.match(/^(.+?[区县旗])/);
    
    let keepLength = 0;
    if (districtMatch) {
        keepLength = districtMatch[1].length;
    } else if (cityMatch) {
        keepLength = cityMatch[1].length;
    } else if (provinceMatch) {
        keepLength = provinceMatch[1].length;
    } else {
        keepLength = Math.floor(address.length / 2);
    }
    
    const keep = address.slice(0, keepLength);
    const maskLength = address.length - keepLength;
    
    if (maskLength <= 0) {
        return address;
    }
    
    return keep + maskChar.repeat(maskLength + showLast);
}

/**
 * IP地址脱敏
 * @param {string} ip - IP地址
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的IP地址
 * @example
 * maskIP('192.168.1.100') // '192.168.*.*'
 */
function maskIP(ip, options = {}) {
    if (!ip || typeof ip !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR } = options;
    
    // IPv4
    if (ip.includes('.')) {
        const parts = ip.split('.');
        if (parts.length === 4) {
            return `${parts[0]}.${parts[1]}.${maskChar.repeat(1)}.${maskChar.repeat(1)}`;
        }
    }
    
    // IPv6 - 简化处理
    if (ip.includes(':')) {
        const parts = ip.split(':');
        if (parts.length >= 4) {
            const masked = parts.slice(0, 2).join(':') + ':' + maskChar.repeat(4);
            return masked;
        }
    }
    
    return ip;
}

/**
 * 信用卡号脱敏
 * @param {string} cardNumber - 信用卡号
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的信用卡号
 * @example
 * maskCreditCard('4532015112830366') // '4532 **** **** 0366'
 */
function maskCreditCard(cardNumber, options = {}) {
    return maskBankCard(cardNumber, options);
}

/**
 * 护照号脱敏
 * @param {string} passport - 护照号
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的护照号
 * @example
 * maskPassport('G12345678') // 'G12****78'
 */
function maskPassport(passport, options = {}) {
    if (!passport || typeof passport !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 3, showLast = 2 } = options;
    const cleaned = passport.toUpperCase();
    
    if (cleaned.length < showFirst + showLast) {
        return cleaned;
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middle = maskChar.repeat(cleaned.length - showFirst - showLast);
    
    return first + middle + last;
}

/**
 * 驾驶证号脱敏
 * @param {string} license - 驾驶证号
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的驾驶证号
 * @example
 * maskDriverLicense('110101199001011234') // '110101********1234'
 */
function maskDriverLicense(license, options = {}) {
    return maskIdCard(license, options);
}

/**
 * 统一社会信用代码脱敏
 * @param {string} code - 统一社会信用代码
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的代码
 * @example
 * maskSocialCreditCode('91110108551385081X') // '911101********81X'
 */
function maskSocialCreditCode(code, options = {}) {
    if (!code || typeof code !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 6, showLast = 3 } = options;
    const cleaned = code.toUpperCase();
    
    if (cleaned.length < showFirst + showLast) {
        return cleaned;
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middle = maskChar.repeat(cleaned.length - showFirst - showLast);
    
    return first + middle + last;
}

/**
 * 车牌号脱敏
 * @param {string} plate - 车牌号
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的车牌号
 * @example
 * maskLicensePlate('京A12345') // '京A***45'
 */
function maskLicensePlate(plate, options = {}) {
    if (!plate || typeof plate !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR, showFirst = 2, showLast = 2 } = options;
    const cleaned = plate.toUpperCase().replace(/\s/g, '');
    
    if (cleaned.length < showFirst + showLast) {
        return cleaned;
    }
    
    const first = cleaned.slice(0, showFirst);
    const last = cleaned.slice(-showLast);
    const middle = maskChar.repeat(cleaned.length - showFirst - showLast);
    
    return first + middle + last;
}

/**
 * 自定义脱敏
 * @param {string} str - 要脱敏的字符串
 * @param {number} showFirst - 显示前几位
 * @param {number} showLast - 显示后几位
 * @param {MaskOptions} options - 其他选项
 * @returns {string} 脱敏后的字符串
 * @example
 * maskCustom('abcdefghij', 2, 2) // 'ab******ij'
 */
function maskCustom(str, showFirst, showLast, options = {}) {
    if (!str || typeof str !== 'string') return '';
    
    const { maskChar = DEFAULT_MASK_CHAR } = options;
    
    if (str.length <= showFirst + showLast) {
        return str;
    }
    
    const first = str.slice(0, showFirst);
    const last = str.slice(-showLast);
    const middle = maskChar.repeat(str.length - showFirst - showLast);
    
    return first + middle + last;
}

/**
 * 格式化银行卡号（每4位一组）
 * @param {string} cardNumber - 银行卡号
 * @param {string} separator - 分隔符，默认空格
 * @returns {string} 格式化后的银行卡号
 * @example
 * formatBankCard('6222021234567890123') // '6222 0212 3456 7890 123'
 */
function formatBankCard(cardNumber, separator = ' ') {
    if (!cardNumber || typeof cardNumber !== 'string') return '';
    
    const cleaned = cardNumber.replace(/\s/g, '');
    const groups = [];
    
    for (let i = 0; i < cleaned.length; i += 4) {
        groups.push(cleaned.slice(i, i + 4));
    }
    
    return groups.join(separator);
}

/**
 * 格式化手机号
 * @param {string} phone - 手机号
 * @param {string} separator - 分隔符，默认空格
 * @returns {string} 格式化后的手机号
 * @example
 * formatPhone('13812345678') // '138 1234 5678'
 */
function formatPhone(phone, separator = ' ') {
    if (!phone || typeof phone !== 'string') return '';
    
    const cleaned = phone.replace(/\D/g, '');
    
    if (cleaned.length === 11) {
        return `${cleaned.slice(0, 3)}${separator}${cleaned.slice(3, 7)}${separator}${cleaned.slice(7)}`;
    }
    
    return cleaned;
}

/**
 * 格式化金额（添加千分位分隔符）
 * @param {number|string} amount - 金额
 * @param {number} decimals - 小数位数，默认2
 * @param {string} separator - 千分位分隔符，默认逗号
 * @returns {string} 格式化后的金额
 * @example
 * formatAmount(1234567.89) // '1,234,567.89'
 */
function formatAmount(amount, decimals = 2, separator = ',') {
    if (amount === null || amount === undefined || amount === '') return '';
    
    const num = parseFloat(amount);
    if (isNaN(num)) return '';
    
    const fixed = num.toFixed(decimals);
    const [integer, decimal] = fixed.split('.');
    
    // 添加千分位
    const formattedInteger = integer.replace(/\B(?=(\d{3})+(?!\d))/g, separator);
    
    return decimal ? `${formattedInteger}.${decimal}` : formattedInteger;
}

/**
 * 验证手机号
 * @param {string} phone - 手机号
 * @returns {boolean} 是否有效
 */
function validatePhone(phone) {
    if (!phone || typeof phone !== 'string') return false;
    const cleaned = phone.replace(/\D/g, '');
    return /^1[3-9]\d{9}$/.test(cleaned);
}

/**
 * 验证邮箱
 * @param {string} email - 邮箱
 * @returns {boolean} 是否有效
 */
function validateEmail(email) {
    if (!email || typeof email !== 'string') return false;
    return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}

/**
 * 验证身份证号
 * @param {string} idCard - 身份证号
 * @returns {boolean} 是否有效
 */
function validateIdCard(idCard) {
    if (!idCard || typeof idCard !== 'string') return false;
    const cleaned = idCard.replace(/\s/g, '').toUpperCase();
    
    // 15位或18位
    if (!/^\d{15}(\d{2}[0-9X])?$/.test(cleaned)) return false;
    
    // 校验位验证（仅18位）
    if (cleaned.length === 18) {
        const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
        const checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
        let sum = 0;
        for (let i = 0; i < 17; i++) {
            sum += parseInt(cleaned[i], 10) * weights[i];
        }
        return checkCodes[sum % 11] === cleaned[17];
    }
    
    return true;
}

/**
 * 验证银行卡号（Luhn算法）
 * @param {string} cardNumber - 银行卡号
 * @returns {boolean} 是否有效
 */
function validateBankCard(cardNumber) {
    if (!cardNumber || typeof cardNumber !== 'string') return false;
    const cleaned = cardNumber.replace(/\s/g, '');
    
    if (!/^\d+$/.test(cleaned) || cleaned.length < 13) return false;
    
    // Luhn算法
    let sum = 0;
    let isEven = false;
    
    for (let i = cleaned.length - 1; i >= 0; i--) {
        let digit = parseInt(cleaned[i], 10);
        
        if (isEven) {
            digit *= 2;
            if (digit > 9) {
                digit -= 9;
            }
        }
        
        sum += digit;
        isEven = !isEven;
    }
    
    return sum % 10 === 0;
}

/**
 * 验证IP地址
 * @param {string} ip - IP地址
 * @returns {boolean} 是否有效
 */
function validateIP(ip) {
    if (!ip || typeof ip !== 'string') return false;
    
    // IPv4
    const ipv4Pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (ipv4Pattern.test(ip)) {
        const parts = ip.split('.');
        return parts.every(part => {
            const num = parseInt(part, 10);
            return num >= 0 && num <= 255;
        });
    }
    
    // IPv6 简化验证
    const ipv6Pattern = /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
    if (ipv6Pattern.test(ip)) {
        return true;
    }
    
    // IPv6 压缩格式
    const ipv6Compressed = /^(([0-9a-fA-F]{1,4}:)*|:){1,7}(:[0-9a-fA-F]{1,4}|:)$/;
    return ipv6Compressed.test(ip);
}

/**
 * 验证信用卡号
 * @param {string} cardNumber - 信用卡号
 * @returns {{ valid: boolean, type: string|null }} 验证结果和卡类型
 */
function validateCreditCard(cardNumber) {
    const result = { valid: false, type: null };
    
    if (!cardNumber || typeof cardNumber !== 'string') return result;
    
    const cleaned = cardNumber.replace(/\s/g, '');
    
    if (!validateBankCard(cleaned)) return result;
    
    result.valid = true;
    
    // 识别卡类型
    if (/^4/.test(cleaned)) {
        result.type = 'Visa';
    } else if (/^5[1-5]/.test(cleaned)) {
        result.type = 'MasterCard';
    } else if (/^3[47]/.test(cleaned)) {
        result.type = 'American Express';
    } else if (/^6(?:011|5)/.test(cleaned)) {
        result.type = 'Discover';
    } else if (/^(?:2131|1800|35)/.test(cleaned)) {
        result.type = 'JCB';
    } else if (/^3(?:0[0-5]|[68])/.test(cleaned)) {
        result.type = 'Diners Club';
    } else if (/^(622|88)/.test(cleaned)) {
        result.type = 'UnionPay';
    }
    
    return result;
}

/**
 * 从文本中提取并脱敏手机号
 * @param {string} text - 文本
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的文本
 * @example
 * maskPhoneInText('联系13812345678或13987654321') // '联系138****5678或139****4321'
 */
function maskPhoneInText(text, options = {}) {
    if (!text || typeof text !== 'string') return '';
    
    const phonePattern = /1[3-9]\d{9}/g;
    return text.replace(phonePattern, match => maskPhone(match, options));
}

/**
 * 从文本中提取并脱敏邮箱
 * @param {string} text - 文本
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的文本
 */
function maskEmailInText(text, options = {}) {
    if (!text || typeof text !== 'string') return '';
    
    const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
    return text.replace(emailPattern, match => maskEmail(match, options));
}

/**
 * 从文本中提取并脱敏身份证号
 * @param {string} text - 文本
 * @param {MaskOptions} options - 脱敏选项
 * @returns {string} 脱敏后的文本
 */
function maskIdCardInText(text, options = {}) {
    if (!text || typeof text !== 'string') return '';
    
    const idCardPattern = /\d{17}[\dXx]|\d{15}/g;
    return text.replace(idCardPattern, match => maskIdCard(match, options));
}

/**
 * 批量脱敏
 * @param {Object} data - 要脱敏的数据对象
 * @param {Object} rules - 脱敏规则
 * @returns {Object} 脱敏后的数据对象
 * @example
 * maskBatch(
 *   { phone: '13812345678', email: 'test@example.com' },
 *   { phone: 'phone', email: 'email' }
 * )
 */
function maskBatch(data, rules) {
    if (!data || typeof data !== 'object') return data;
    
    const result = { ...data };
    
    const maskFunctions = {
        phone: maskPhone,
        telephone: maskTelephone,
        idCard: maskIdCard,
        bankCard: maskBankCard,
        email: maskEmail,
        name: maskName,
        address: maskAddress,
        ip: maskIP,
        creditCard: maskCreditCard,
        passport: maskPassport,
        driverLicense: maskDriverLicense,
        socialCreditCode: maskSocialCreditCode,
        licensePlate: maskLicensePlate
    };
    
    for (const [key, type] of Object.entries(rules)) {
        if (result[key] !== undefined && maskFunctions[type]) {
            result[key] = maskFunctions[type](result[key]);
        }
    }
    
    return result;
}

// 导出所有函数
module.exports = {
    // 脱敏函数
    maskPhone,
    maskTelephone,
    maskIdCard,
    maskBankCard,
    maskEmail,
    maskName,
    maskAddress,
    maskIP,
    maskCreditCard,
    maskPassport,
    maskDriverLicense,
    maskSocialCreditCode,
    maskLicensePlate,
    maskCustom,
    
    // 格式化函数
    formatBankCard,
    formatPhone,
    formatAmount,
    
    // 验证函数
    validatePhone,
    validateEmail,
    validateIdCard,
    validateBankCard,
    validateIP,
    validateCreditCard,
    
    // 文本脱敏
    maskPhoneInText,
    maskEmailInText,
    maskIdCardInText,
    
    // 批量脱敏
    maskBatch
};