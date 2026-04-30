/**
 * Validator Utils - 通用验证工具模块
 * 
 * 功能：
 * - 邮箱验证
 * - URL 验证
 * - 手机号验证（中国/国际）
 * - 身份证号验证（中国）
 * - 信用卡号验证（Luhn 算法）
 * - IP 地址验证（IPv4/IPv6）
 * - 密码强度检测
 * - 银行卡号验证
 * 
 * 零外部依赖，纯 JavaScript 实现。
 */

/**
 * 验证错误基类
 */
class ValidationError extends Error {
    constructor(message, field = null) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
    }
}

/**
 * 验证工具类
 */
class ValidatorUtils {
    // ============== 邮箱验证 ==============

    /**
     * 验证邮箱格式
     * @param {string} email - 邮箱地址
     * @returns {boolean} 是否有效
     */
    static isEmail(email) {
        if (!email || typeof email !== 'string') return false;
        const trimmed = email.trim();
        if (trimmed.length > 254) return false;
        // RFC 5322 简化版正则 - 必须包含域名
        const pattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
        return pattern.test(trimmed);
    }

    /**
     * 验证邮箱并返回详细信息
     * @param {string} email - 邮箱地址
     * @returns {Object} 验证结果对象
     */
    static validateEmail(email) {
        const result = {
            valid: false,
            email: email,
            localPart: null,
            domain: null,
            errors: []
        };

        if (!email || typeof email !== 'string') {
            result.errors.push('邮箱不能为空');
            return result;
        }

        email = email.trim();

        if (email.length > 254) {
            result.errors.push('邮箱长度不能超过 254 个字符');
            return result;
        }

        const parts = email.split('@');
        if (parts.length !== 2) {
            result.errors.push('邮箱格式错误：缺少 @ 符号');
            return result;
        }

        const [localPart, domain] = parts;
        result.localPart = localPart;
        result.domain = domain;

        if (!localPart || localPart.length > 64) {
            result.errors.push('本地部分长度必须在 1-64 个字符之间');
        }

        if (!domain || domain.length > 255) {
            result.errors.push('域名无效');
        }

        if (!ValidatorUtils.isEmail(email)) {
            result.errors.push('邮箱格式不符合规范');
            return result;
        }

        result.valid = true;
        return result;
    }

    // ============== URL 验证 ==============

    /**
     * 验证 URL 格式
     * @param {string} url - URL 字符串
     * @param {Object} options - 选项
     * @param {string[]} options.protocols - 允许的协议列表
     * @param {boolean} options.requireProtocol - 是否必须包含协议
     * @returns {boolean} 是否有效
     */
    static isURL(url, options = {}) {
        if (!url || typeof url !== 'string') return false;

        const {
            protocols = ['http', 'https', 'ftp'],
            requireProtocol = true
        } = options;

        url = url.trim();

        try {
            let parsed;
            if (requireProtocol || /^https?:\/\//i.test(url)) {
                parsed = new URL(url);
            } else {
                parsed = new URL('http://' + url);
            }

            return protocols.includes(parsed.protocol.slice(0, -1));
        } catch (e) {
            return false;
        }
    }

    /**
     * 验证 URL 并返回详细信息
     * @param {string} url - URL 字符串
     * @returns {Object} 验证结果对象
     */
    static validateURL(url) {
        const result = {
            valid: false,
            url: url,
            protocol: null,
            hostname: null,
            port: null,
            pathname: null,
            query: null,
            hash: null,
            errors: []
        };

        if (!url || typeof url !== 'string') {
            result.errors.push('URL 不能为空');
            return result;
        }

        url = url.trim();

        try {
            const parsed = new URL(url);
            result.protocol = parsed.protocol.slice(0, -1);
            result.hostname = parsed.hostname;
            result.port = parsed.port || null;
            result.pathname = parsed.pathname;
            result.query = parsed.search || null;
            result.hash = parsed.hash || null;
            result.valid = true;
        } catch (e) {
            result.errors.push(`URL 格式错误: ${e.message}`);
        }

        return result;
    }

    // ============== 手机号验证 ==============

    /**
     * 验证中国手机号
     * @param {string} phone - 手机号字符串
     * @returns {boolean} 是否有效
     */
    static isChinesePhone(phone) {
        if (!phone || typeof phone !== 'string') return false;
        // 中国手机号正则（支持 +86 前缀）
        const cleaned = phone.replace(/[\s\-()]/g, '');
        const pattern = /^(?:\+?86)?1[3-9]\d{9}$/;
        return pattern.test(cleaned);
    }

    /**
     * 验证手机号并返回详细信息
     * @param {string} phone - 手机号字符串
     * @returns {Object} 验证结果对象
     */
    static validateChinesePhone(phone) {
        const result = {
            valid: false,
            phone: phone,
            cleaned: null,
            province: null,
            carrier: null,
            errors: []
        };

        if (!phone || typeof phone !== 'string') {
            result.errors.push('手机号不能为空');
            return result;
        }

        const cleaned = phone.replace(/[\s\-()]/g, '');
        result.cleaned = cleaned;

        // 移除 +86 或 86 前缀
        const number = cleaned.replace(/^(?:\+?86)/, '');

        if (!/^1\d{10}$/.test(number)) {
            result.errors.push('手机号格式错误：应为 11 位数字');
            return result;
        }

        // 运营商号段识别
        const prefix = number.slice(0, 3);
        const carrierMap = {
            '130': '中国联通', '131': '中国联通', '132': '中国联通', '133': '中国电信',
            '134': '中国移动', '135': '中国移动', '136': '中国移动', '137': '中国移动',
            '138': '中国移动', '139': '中国移动', '145': '中国联通', '147': '中国移动',
            '149': '中国电信', '150': '中国移动', '151': '中国移动', '152': '中国移动',
            '153': '中国电信', '155': '中国联通', '156': '中国联通', '157': '中国移动',
            '158': '中国移动', '159': '中国移动', '166': '中国联通', '167': '虚拟运营商',
            '170': '虚拟运营商', '171': '虚拟运营商', '172': '中国移动', '173': '中国电信',
            '174': '中国电信', '175': '中国联通', '176': '中国联通', '177': '中国电信',
            '178': '中国移动', '180': '中国电信', '181': '中国电信', '182': '中国移动',
            '183': '中国移动', '184': '中国移动', '185': '中国联通', '186': '中国联通',
            '187': '中国移动', '188': '中国移动', '189': '中国电信', '190': '中国电信',
            '191': '中国电信', '192': '中国移动', '193': '中国联通', '195': '中国移动',
            '196': '中国联通', '197': '中国移动', '198': '中国移动', '199': '中国电信'
        };

        result.carrier = carrierMap[prefix] || '未知运营商';

        if (!ValidatorUtils.isChinesePhone(phone)) {
            result.errors.push('手机号号段无效');
            return result;
        }

        result.valid = true;
        return result;
    }

    /**
     * 验证国际手机号
     * @param {string} phone - 手机号字符串（E.164 格式）
     * @returns {boolean} 是否有效
     */
    static isInternationalPhone(phone) {
        if (!phone || typeof phone !== 'string') return false;
        const cleaned = phone.replace(/[\s\-()]/g, '');
        // E.164 格式：+号开头，最多 15 位数字
        return /^\+[1-9]\d{1,14}$/.test(cleaned);
    }

    // ============== 身份证号验证（中国） ==============

    /**
     * 验证中国身份证号
     * @param {string} id - 身份证号字符串
     * @returns {boolean} 是否有效
     */
    static isChineseID(id) {
        if (!id || typeof id !== 'string') return false;
        const cleaned = id.trim().toUpperCase();

        // 15 位或 18 位
        if (!/^\d{15}(\d{2}[0-9X])?$/.test(cleaned)) {
            return false;
        }

        // 18 位身份证校验
        if (cleaned.length === 18) {
            return ValidatorUtils._validateIDCheckDigit(cleaned);
        }

        // 15 位身份证（已停用，但仍然验证格式）
        return true;
    }

    /**
     * 验证身份证校验位
     * @private
     */
    static _validateIDCheckDigit(id) {
        const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
        const checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];

        let sum = 0;
        for (let i = 0; i < 17; i++) {
            sum += parseInt(id[i]) * weights[i];
        }

        return id[17] === checkCodes[sum % 11];
    }

    /**
     * 验证身份证并返回详细信息
     * @param {string} id - 身份证号字符串
     * @returns {Object} 验证结果对象
     */
    static validateChineseID(id) {
        const result = {
            valid: false,
            id: id,
            cleaned: null,
            birthday: null,
            gender: null,
            province: null,
            city: null,
            age: null,
            errors: []
        };

        if (!id || typeof id !== 'string') {
            result.errors.push('身份证号不能为空');
            return result;
        }

        const cleaned = id.trim().toUpperCase();
        result.cleaned = cleaned;

        if (!/^\d{15}(\d{2}[0-9X])?$/.test(cleaned)) {
            result.errors.push('身份证号格式错误：应为 15 位或 18 位');
            return result;
        }

        // 解析信息
        let birthdayStr;
        if (cleaned.length === 18) {
            // 校验位验证
            if (!ValidatorUtils._validateIDCheckDigit(cleaned)) {
                result.errors.push('身份证号校验位错误');
                return result;
            }
            birthdayStr = cleaned.slice(6, 14);
        } else {
            birthdayStr = '19' + cleaned.slice(6, 12);
        }

        // 解析生日
        const year = parseInt(birthdayStr.slice(0, 4));
        const month = parseInt(birthdayStr.slice(4, 6));
        const day = parseInt(birthdayStr.slice(6, 8));

        const birthday = new Date(year, month - 1, day);
        if (birthday.getFullYear() !== year ||
            birthday.getMonth() !== month - 1 ||
            birthday.getDate() !== day) {
            result.errors.push('身份证号中的日期无效');
            return result;
        }

        result.birthday = birthdayStr;

        // 计算年龄
        const today = new Date();
        let age = today.getFullYear() - year;
        if (today.getMonth() < month - 1 ||
            (today.getMonth() === month - 1 && today.getDate() < day)) {
            age--;
        }
        result.age = age;

        // 性别（第 17 位，奇数为男）
        const genderIndex = cleaned.length === 18 ? 16 : 14;
        result.gender = parseInt(cleaned[genderIndex]) % 2 === 1 ? '男' : '女';

        // 地区码（简化版，只识别省级）
        const regionCode = cleaned.slice(0, 2);
        const provinceMap = {
            '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省',
            '15': '内蒙古自治区', '21': '辽宁省', '22': '吉林省', '23': '黑龙江省',
            '31': '上海市', '32': '江苏省', '33': '浙江省', '34': '安徽省',
            '35': '福建省', '36': '江西省', '37': '山东省', '41': '河南省',
            '42': '湖北省', '43': '湖南省', '44': '广东省', '45': '广西壮族自治区',
            '46': '海南省', '50': '重庆市', '51': '四川省', '52': '贵州省',
            '53': '云南省', '54': '西藏自治区', '61': '陕西省', '62': '甘肃省',
            '63': '青海省', '64': '宁夏回族自治区', '65': '新疆维吾尔自治区',
            '71': '台湾省', '81': '香港特别行政区', '82': '澳门特别行政区'
        };
        result.province = provinceMap[regionCode] || '未知地区';

        result.valid = true;
        return result;
    }

    // ============== 信用卡号验证 ==============

    /**
     * 使用 Luhn 算法验证卡号
     * @param {string} number - 卡号字符串
     * @returns {boolean} 是否通过 Luhn 检验
     */
    static luhnCheck(number) {
        if (!number || typeof number !== 'string') return false;
        const cleaned = number.replace(/\D/g, '');

        if (cleaned.length < 13 || cleaned.length > 19) return false;

        let sum = 0;
        let isEven = false;

        for (let i = cleaned.length - 1; i >= 0; i--) {
            let digit = parseInt(cleaned[i]);

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
     * 验证信用卡号
     * @param {string} cardNumber - 卡号字符串
     * @returns {boolean} 是否有效
     */
    static isCreditCard(cardNumber) {
        return ValidatorUtils.luhnCheck(cardNumber);
    }

    /**
     * 验证信用卡并返回详细信息
     * @param {string} cardNumber - 卡号字符串
     * @returns {Object} 验证结果对象
     */
    static validateCreditCard(cardNumber) {
        const result = {
            valid: false,
            cardNumber: cardNumber,
            cleaned: null,
            type: null,
            issuer: null,
            errors: []
        };

        if (!cardNumber || typeof cardNumber !== 'string') {
            result.errors.push('卡号不能为空');
            return result;
        }

        const cleaned = cardNumber.replace(/\D/g, '');
        result.cleaned = cleaned;

        if (cleaned.length < 13 || cleaned.length > 19) {
            result.errors.push('卡号长度应在 13-19 位之间');
            return result;
        }

        if (!ValidatorUtils.luhnCheck(cleaned)) {
            result.errors.push('卡号 Luhn 校验失败');
            return result;
        }

        // 识别发卡行
        const issuerPatterns = [
            { pattern: /^4/, issuer: 'Visa', type: 'credit' },
            { pattern: /^5[1-5]/, issuer: 'Mastercard', type: 'credit' },
            { pattern: /^2[2-7]/, issuer: 'Mastercard', type: 'credit' },
            { pattern: /^3[47]/, issuer: 'American Express', type: 'credit' },
            { pattern: /^6(?:011|5)/, issuer: 'Discover', type: 'credit' },
            { pattern: /^35(?:2[89]|[3-8]\d)/, issuer: 'JCB', type: 'credit' },
            { pattern: /^3(?:0[0-5]|[68])/, issuer: 'Diners Club', type: 'credit' },
            { pattern: /^(?:2131|1800|35\d{3})/, issuer: 'JCB', type: 'credit' },
            { pattern: /^(62|88)/, issuer: 'UnionPay', type: 'credit' }
        ];

        for (const { pattern, issuer, type } of issuerPatterns) {
            if (pattern.test(cleaned)) {
                result.issuer = issuer;
                result.type = type;
                break;
            }
        }

        if (!result.issuer) {
            result.issuer = '未知发卡行';
            result.type = 'unknown';
        }

        result.valid = true;
        return result;
    }

    /**
     * 验证银行卡号（中国银联）
     * @param {string} cardNumber - 银行卡号
     * @returns {boolean} 是否有效
     */
    static isBankCard(cardNumber) {
        if (!cardNumber || typeof cardNumber !== 'string') return false;
        const cleaned = cardNumber.replace(/\D/g, '');
        // 银联卡号 16-19 位
        return /^\d{16,19}$/.test(cleaned) && ValidatorUtils.luhnCheck(cleaned);
    }

    // ============== IP 地址验证 ==============

    /**
     * 验证 IPv4 地址
     * @param {string} ip - IP 地址字符串
     * @returns {boolean} 是否有效
     */
    static isIPv4(ip) {
        if (!ip || typeof ip !== 'string') return false;
        const parts = ip.trim().split('.');
        if (parts.length !== 4) return false;

        for (const part of parts) {
            const num = parseInt(part);
            if (isNaN(num) || num < 0 || num > 255) return false;
            if (part !== String(num)) return false; // 避免前导零
        }

        return true;
    }

    /**
     * 验证 IPv6 地址
     * @param {string} ip - IP 地址字符串
     * @returns {boolean} 是否有效
     */
    static isIPv6(ip) {
        if (!ip || typeof ip !== 'string') return false;
        ip = ip.trim();

        // 处理 :: 缩写
        const doubleColon = ip.indexOf('::');
        if (doubleColon !== -1) {
            if (ip.indexOf('::', doubleColon + 1) !== -1) return false; // 只能有一个 ::
        }

        // 分割并验证
        const parts = ip.split(':');
        let hasDoubleColon = ip.includes('::');

        // IPv6 最多 8 组，最少 2 组（带 ::）
        if (parts.length > 8 || (parts.length < 3 && !hasDoubleColon)) return false;

        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];

            // 空部分只允许在 :: 处
            if (part === '') {
                if (!hasDoubleColon) return false;
                continue;
            }

            // 每部分最多 4 个十六进制字符
            if (!/^[0-9a-fA-F]{1,4}$/.test(part)) return false;
        }

        return true;
    }

    /**
     * 验证 IP 地址（IPv4 或 IPv6）
     * @param {string} ip - IP 地址字符串
     * @returns {boolean} 是否有效
     */
    static isIP(ip) {
        return ValidatorUtils.isIPv4(ip) || ValidatorUtils.isIPv6(ip);
    }

    /**
     * 验证 IP 并返回详细信息
     * @param {string} ip - IP 地址字符串
     * @returns {Object} 验证结果对象
     */
    static validateIP(ip) {
        const result = {
            valid: false,
            ip: ip,
            version: null,
            isPrivate: false,
            isLoopback: false,
            isMulticast: false,
            errors: []
        };

        if (!ip || typeof ip !== 'string') {
            result.errors.push('IP 地址不能为空');
            return result;
        }

        ip = ip.trim();

        if (ValidatorUtils.isIPv4(ip)) {
            result.version = 4;
            const parts = ip.split('.').map(Number);

            // 私有地址
            result.isPrivate =
                parts[0] === 10 ||
                (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) ||
                (parts[0] === 192 && parts[1] === 168);

            // 回环地址
            result.isLoopback = parts[0] === 127;

            // 组播地址
            result.isMulticast = parts[0] >= 224 && parts[0] <= 239;

            result.valid = true;
        } else if (ValidatorUtils.isIPv6(ip)) {
            result.version = 6;
            const lower = ip.toLowerCase();

            // 私有地址 (fc00::/7)
            result.isPrivate = lower.startsWith('fc') || lower.startsWith('fd');

            // 回环地址 (::1)
            result.isLoopback = lower === '::1' || lower === '0:0:0:0:0:0:0:1';

            result.valid = true;
        } else {
            result.errors.push('无效的 IP 地址格式');
        }

        return result;
    }

    // ============== 密码强度验证 ==============

    /**
     * 检测密码强度
     * @param {string} password - 密码字符串
     * @returns {Object} 强度评估结果
     */
    static checkPasswordStrength(password) {
        const result = {
            password: password ? '******' : null,
            score: 0,
            strength: 'very-weak',
            level: 0,
            length: 0,
            hasLower: false,
            hasUpper: false,
            hasNumber: false,
            hasSymbol: false,
            suggestions: [],
            errors: []
        };

        if (!password || typeof password !== 'string') {
            result.errors.push('密码不能为空');
            return result;
        }

        result.length = password.length;

        // 检查字符类型
        result.hasLower = /[a-z]/.test(password);
        result.hasUpper = /[A-Z]/.test(password);
        result.hasNumber = /\d/.test(password);
        result.hasSymbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);

        // 计算得分
        let score = 0;

        // 长度得分
        if (password.length >= 8) score += 1;
        if (password.length >= 12) score += 1;
        if (password.length >= 16) score += 1;

        // 字符类型得分
        if (result.hasLower) score += 1;
        if (result.hasUpper) score += 1;
        if (result.hasNumber) score += 1;
        if (result.hasSymbol) score += 1;

        // 惩罚常见弱密码
        const commonPasswords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'monkey', 'master', 'dragon', '111111', 'baseball',
            'iloveyou', 'trustno1', 'sunshine', 'princess', 'admin'
        ];
        if (commonPasswords.includes(password.toLowerCase())) {
            score = Math.max(0, score - 3);
            result.suggestions.push('避免使用常见密码');
        }

        // 连续字符惩罚
        if (/(.)\1{2,}/.test(password)) {
            score = Math.max(0, score - 1);
            result.suggestions.push('避免连续重复字符');
        }

        // 顺序字符惩罚
        if (/(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)/i.test(password)) {
            score = Math.max(0, score - 1);
            result.suggestions.push('避免连续顺序字符');
        }

        result.score = score;

        // 确定强度等级
        if (score < 3) {
            result.strength = 'very-weak';
            result.level = 0;
        } else if (score < 5) {
            result.strength = 'weak';
            result.level = 1;
        } else if (score < 7) {
            result.strength = 'medium';
            result.level = 2;
        } else if (score < 9) {
            result.strength = 'strong';
            result.level = 3;
        } else {
            result.strength = 'very-strong';
            result.level = 4;
        }

        // 生成建议
        if (password.length < 8) {
            result.suggestions.push('密码长度应至少 8 个字符');
        }
        if (!result.hasLower) {
            result.suggestions.push('添加小写字母');
        }
        if (!result.hasUpper) {
            result.suggestions.push('添加大写字母');
        }
        if (!result.hasNumber) {
            result.suggestions.push('添加数字');
        }
        if (!result.hasSymbol) {
            result.suggestions.push('添加特殊符号');
        }

        return result;
    }

    // ============== 通用验证 ==============

    /**
     * 验证是否为空
     * @param {any} value - 要验证的值
     * @returns {boolean} 是否为空
     */
    static isEmpty(value) {
        if (value === null || value === undefined) return true;
        if (typeof value === 'string') return value.trim() === '';
        if (Array.isArray(value)) return value.length === 0;
        if (typeof value === 'object') return Object.keys(value).length === 0;
        return false;
    }

    /**
     * 验证数字范围
     * @param {number} value - 要验证的数字
     * @param {number} min - 最小值
     * @param {number} max - 最大值
     * @returns {boolean} 是否在范围内
     */
    static isInRange(value, min, max) {
        if (typeof value !== 'number' || isNaN(value)) return false;
        return value >= min && value <= max;
    }

    /**
     * 验证字符串长度
     * @param {string} str - 要验证的字符串
     * @param {number} min - 最小长度
     * @param {number} max - 最大长度
     * @returns {boolean} 是否在范围内
     */
    static isLength(str, min, max = Infinity) {
        if (!str || typeof str !== 'string') return false;
        const len = str.length;
        return len >= min && len <= max;
    }

    /**
     * 验证是否为纯数字
     * @param {string} str - 要验证的字符串
     * @returns {boolean} 是否为纯数字
     */
    static isNumeric(str) {
        if (!str || typeof str !== 'string') return false;
        return /^\d+$/.test(str);
    }

    /**
     * 验证是否为字母
     * @param {string} str - 要验证的字符串
     * @returns {boolean} 是否为纯字母
     */
    static isAlpha(str) {
        if (!str || typeof str !== 'string') return false;
        return /^[a-zA-Z]+$/.test(str);
    }

    /**
     * 验证是否为字母数字
     * @param {string} str - 要验证的字符串
     * @returns {boolean} 是否为字母数字
     */
    static isAlphanumeric(str) {
        if (!str || typeof str !== 'string') return false;
        return /^[a-zA-Z0-9]+$/.test(str);
    }

    /**
     * 验证日期格式
     * @param {string} dateStr - 日期字符串
     * @param {string} format - 日期格式（默认 YYYY-MM-DD）
     * @returns {boolean} 是否为有效日期
     */
    static isDate(dateStr, format = 'YYYY-MM-DD') {
        if (!dateStr || typeof dateStr !== 'string') return false;

        let year, month, day;

        if (format === 'YYYY-MM-DD') {
            const match = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})$/);
            if (!match) return false;
            [, year, month, day] = match.map(Number);
        } else if (format === 'DD/MM/YYYY') {
            const match = dateStr.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
            if (!match) return false;
            [, day, month, year] = match.map(Number);
        } else if (format === 'MM/DD/YYYY') {
            const match = dateStr.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
            if (!match) return false;
            [, month, day, year] = match.map(Number);
        } else {
            return false;
        }

        const date = new Date(year, month - 1, day);
        return date.getFullYear() === year &&
               date.getMonth() === month - 1 &&
               date.getDate() === day;
    }

    /**
     * 验证十六进制颜色
     * @param {string} color - 颜色字符串
     * @returns {boolean} 是否为有效的十六进制颜色
     */
    static isHexColor(color) {
        if (!color || typeof color !== 'string') return false;
        return /^#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test(color.trim());
    }

    /**
     * 验证 JSON 字符串
     * @param {string} str - JSON 字符串
     * @returns {boolean} 是否为有效的 JSON
     */
    static isJSON(str) {
        if (!str || typeof str !== 'string') return false;
        try {
            JSON.parse(str);
            return true;
        } catch (e) {
            return false;
        }
    }

    /**
     * 批量验证
     * @param {Object} data - 要验证的数据对象
     * @param {Object} rules - 验证规则
     * @returns {Object} 验证结果
     */
    static validate(data, rules) {
        const result = {
            valid: true,
            errors: {},
            data: {}
        };

        for (const [field, rule] of Object.entries(rules)) {
            const value = data[field];
            const fieldErrors = [];

            // 必填检查
            if (rule.required && ValidatorUtils.isEmpty(value)) {
                fieldErrors.push(rule.message || `${field} 是必填字段`);
            }

            if (!ValidatorUtils.isEmpty(value)) {
                // 类型检查
                if (rule.type) {
                    switch (rule.type) {
                        case 'email':
                            if (!ValidatorUtils.isEmail(value)) {
                                fieldErrors.push(`${field} 不是有效的邮箱地址`);
                            }
                            break;
                        case 'url':
                            if (!ValidatorUtils.isURL(value)) {
                                fieldErrors.push(`${field} 不是有效的 URL`);
                            }
                            break;
                        case 'phone':
                            if (!ValidatorUtils.isChinesePhone(value)) {
                                fieldErrors.push(`${field} 不是有效的手机号`);
                            }
                            break;
                        case 'id':
                            if (!ValidatorUtils.isChineseID(value)) {
                                fieldErrors.push(`${field} 不是有效的身份证号`);
                            }
                            break;
                        case 'number':
                            if (typeof value !== 'number' && isNaN(Number(value))) {
                                fieldErrors.push(`${field} 必须是数字`);
                            }
                            break;
                        case 'integer':
                            if (!Number.isInteger(Number(value))) {
                                fieldErrors.push(`${field} 必须是整数`);
                            }
                            break;
                    }
                }

                // 长度检查
                if (rule.minLength && String(value).length < rule.minLength) {
                    fieldErrors.push(`${field} 长度不能少于 ${rule.minLength} 个字符`);
                }
                if (rule.maxLength && String(value).length > rule.maxLength) {
                    fieldErrors.push(`${field} 长度不能超过 ${rule.maxLength} 个字符`);
                }

                // 范围检查
                if (rule.min !== undefined && Number(value) < rule.min) {
                    fieldErrors.push(`${field} 不能小于 ${rule.min}`);
                }
                if (rule.max !== undefined && Number(value) > rule.max) {
                    fieldErrors.push(`${field} 不能大于 ${rule.max}`);
                }

                // 正则检查
                if (rule.pattern && !rule.pattern.test(value)) {
                    fieldErrors.push(rule.message || `${field} 格式不正确`);
                }

                // 自定义验证
                if (rule.validate && typeof rule.validate === 'function') {
                    const customResult = rule.validate(value);
                    if (customResult !== true) {
                        fieldErrors.push(customResult || `${field} 验证失败`);
                    }
                }
            }

            if (fieldErrors.length > 0) {
                result.valid = false;
                result.errors[field] = fieldErrors;
            } else {
                result.data[field] = value;
            }
        }

        return result;
    }
}

// 便捷函数
const isEmail = ValidatorUtils.isEmail;
const isURL = ValidatorUtils.isURL;
const isChinesePhone = ValidatorUtils.isChinesePhone;
const isChineseID = ValidatorUtils.isChineseID;
const isCreditCard = ValidatorUtils.isCreditCard;
const isBankCard = ValidatorUtils.isBankCard;
const isIPv4 = ValidatorUtils.isIPv4;
const isIPv6 = ValidatorUtils.isIPv6;
const isIP = ValidatorUtils.isIP;
const luhnCheck = ValidatorUtils.luhnCheck;
const checkPasswordStrength = ValidatorUtils.checkPasswordStrength;
const validate = ValidatorUtils.validate;

// 导出
module.exports = {
    // 类
    ValidationError,
    ValidatorUtils,
    // 便捷函数
    isEmail,
    isURL,
    isChinesePhone,
    isChineseID,
    isCreditCard,
    isBankCard,
    isIPv4,
    isIPv6,
    isIP,
    luhnCheck,
    checkPasswordStrength,
    validate
};