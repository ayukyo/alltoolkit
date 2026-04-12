/**
 * validation_utils - 数据验证工具库
 * 
 * 提供常用的数据验证函数，包括：
 * - 邮箱验证
 * - 手机号验证（支持国际格式）
 * - URL验证
 * - 身份证号验证（中国大陆）
 * - 银行卡号验证
 * - 密码强度验证
 * - IP地址验证
 * - 日期验证
 * - 数字范围验证
 * - 字符串长度验证
 * 
 * @version 1.0.0
 * @license MIT
 */

// ==================== 正则表达式常量 ====================

const REGEX = {
  email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  phoneCN: /^1[3-9]\d{9}$/,
  phoneInternational: /^\+?[1-9]\d{6,14}$/,
  url: /^(https?:\/\/)?(([\da-z\.-]+)\.([a-z\.]{2,6})|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))([\/\w \.-]*)*\/?$/,
  urlStrict: /^https?:\/\/([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/,
  ipv4: /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$/,
  ipv6: /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/,
  idCardCN: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/,
  postalCodeCN: /^[1-9]\d{5}$/,
  hexColor: /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/,
  slug: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  alpha: /^[a-zA-Z]+$/,
  alphanumeric: /^[a-zA-Z0-9]+$/,
  username: /^[a-zA-Z][a-zA-Z0-9_]{2,15}$/,
};

// ==================== 基础验证函数 ====================

/**
 * 检查值是否为空（null、undefined 或空字符串）
 */
export function isEmpty(value: string | null | undefined): boolean {
  return value === null || value === undefined || value === '';
}

/**
 * 检查值是否非空
 */
export function isNotEmpty(value: string | null | undefined): boolean {
  return !isEmpty(value);
}

/**
 * 检查值是否为有效的邮箱地址
 */
export function isEmail(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.email.test(value.trim());
}

/**
 * 检查值是否为有效的中国大陆手机号
 */
export function isPhoneCN(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.phoneCN.test(value.trim());
}

/**
 * 检查值是否为有效的国际手机号
 */
export function isPhoneInternational(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.phoneInternational.test(value.trim());
}

/**
 * 检查值是否为有效的URL
 * @param strict 是否严格模式（必须包含协议）
 */
export function isURL(value: string, strict: boolean = false): boolean {
  if (isEmpty(value)) return false;
  const regex = strict ? REGEX.urlStrict : REGEX.url;
  return regex.test(value.trim());
}

// ==================== 身份证验证 ====================

// 中国大陆身份证校验码权重
const ID_CARD_WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
const ID_CARD_CHECK_CODES = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];

/**
 * 检查值是否为有效的中国大陆身份证号
 * 包含格式验证和校验码验证
 */
export function isIDCardCN(value: string): boolean {
  if (isEmpty(value)) return false;
  const idCard = value.trim().toUpperCase();
  
  // 基本格式验证
  if (!REGEX.idCardCN.test(idCard)) return false;
  
  // 校验码验证
  let sum = 0;
  for (let i = 0; i < 17; i++) {
    sum += parseInt(idCard[i]) * ID_CARD_WEIGHTS[i];
  }
  const checkCode = ID_CARD_CHECK_CODES[sum % 11];
  
  return idCard[17] === checkCode;
}

/**
 * 从身份证号提取信息
 */
export function parseIDCardCN(value: string): {
  valid: boolean;
  birthday?: string;
  gender?: '男' | '女';
  province?: string;
} {
  if (!isIDCardCN(value)) {
    return { valid: false };
  }
  
  const idCard = value.trim().toUpperCase();
  
  // 提取生日
  const year = idCard.substring(6, 10);
  const month = idCard.substring(10, 12);
  const day = idCard.substring(12, 14);
  const birthday = `${year}-${month}-${day}`;
  
  // 提取性别（奇数为男，偶数为女）
  const genderCode = parseInt(idCard[16]);
  const gender: '男' | '女' = genderCode % 2 === 1 ? '男' : '女';
  
  // 提取省份码（简化版）
  const provinceCode = idCard.substring(0, 2);
  const provinceMap: Record<string, string> = {
    '11': '北京', '12': '天津', '13': '河北', '14': '山西', '15': '内蒙古',
    '21': '辽宁', '22': '吉林', '23': '黑龙江',
    '31': '上海', '32': '江苏', '33': '浙江', '34': '安徽', '35': '福建', '36': '江西', '37': '山东',
    '41': '河南', '42': '湖北', '43': '湖南', '44': '广东', '45': '广西', '46': '海南',
    '50': '重庆', '51': '四川', '52': '贵州', '53': '云南', '54': '西藏',
    '61': '陕西', '62': '甘肃', '63': '青海', '64': '宁夏', '65': '新疆',
    '71': '台湾', '81': '香港', '82': '澳门'
  };
  const province = provinceMap[provinceCode] || '未知';
  
  return { valid: true, birthday, gender, province };
}

// ==================== 银行卡验证 ====================

/**
 * 使用 Luhn 算法验证银行卡号
 */
export function isBankCard(value: string): boolean {
  if (isEmpty(value)) return false;
  
  const cardNumber = value.replace(/\s/g, '');
  if (!/^\d{13,19}$/.test(cardNumber)) return false;
  
  // Luhn 算法
  let sum = 0;
  let isEven = false;
  
  for (let i = cardNumber.length - 1; i >= 0; i--) {
    let digit = parseInt(cardNumber[i]);
    
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

// ==================== IP 地址验证 ====================

/**
 * 检查值是否为有效的 IPv4 地址
 */
export function isIPv4(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.ipv4.test(value.trim());
}

/**
 * 检查值是否为有效的 IPv6 地址
 */
export function isIPv6(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.ipv6.test(value.trim());
}

/**
 * 检查值是否为有效的 IP 地址（IPv4 或 IPv6）
 */
export function isIP(value: string): boolean {
  return isIPv4(value) || isIPv6(value);
}

// ==================== 密码验证 ====================

export interface PasswordStrength {
  score: number;        // 0-4 分
  level: '很弱' | '弱' | '中等' | '强' | '很强';
  suggestions: string[];
  isValid: boolean;
}

/**
 * 验证密码强度
 * @param password 密码
 * @param minLength 最小长度（默认 8）
 */
export function validatePassword(password: string, minLength: number = 8): PasswordStrength {
  const suggestions: string[] = [];
  let score = 0;
  
  // 长度检查
  if (password.length < minLength) {
    suggestions.push(`密码长度至少需要 ${minLength} 位`);
  } else if (password.length >= minLength) {
    score++;
  }
  
  if (password.length >= 12) score++;
  
  // 包含小写字母
  if (/[a-z]/.test(password)) {
    score++;
  } else {
    suggestions.push('建议包含小写字母');
  }
  
  // 包含大写字母
  if (/[A-Z]/.test(password)) {
    score++;
  } else {
    suggestions.push('建议包含大写字母');
  }
  
  // 包含数字
  if (/\d/.test(password)) {
    score++;
  } else {
    suggestions.push('建议包含数字');
  }
  
  // 包含特殊字符
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    score++;
  } else {
    suggestions.push('建议包含特殊字符');
  }
  
  // 确定强度等级
  const levels: ('很弱' | '弱' | '中等' | '强' | '很强')[] = ['很弱', '弱', '中等', '强', '很强'];
  const levelIndex = Math.min(4, Math.floor(score * 0.7));
  const level = levels[levelIndex];
  
  return {
    score,
    level,
    suggestions,
    isValid: password.length >= minLength && score >= 3
  };
}

// ==================== 数值验证 ====================

/**
 * 检查值是否在指定范围内
 */
export function isInRange(value: number, min: number, max: number): boolean {
  return value >= min && value <= max;
}

/**
 * 检查值是否为整数
 */
export function isInteger(value: number): boolean {
  return Number.isInteger(value);
}

/**
 * 检查值是否为正整数
 */
export function isPositiveInteger(value: number): boolean {
  return Number.isInteger(value) && value > 0;
}

/**
 * 检查值是否为负整数
 */
export function isNegativeInteger(value: number): boolean {
  return Number.isInteger(value) && value < 0;
}

/**
 * 检查值是否为偶数
 */
export function isEven(value: number): boolean {
  return value % 2 === 0;
}

/**
 * 检查值是否为奇数
 */
export function isOdd(value: number): boolean {
  return value % 2 !== 0;
}

/**
 * 检查值是否为质数
 */
export function isPrime(value: number): boolean {
  if (!Number.isInteger(value) || value < 2) return false;
  if (value === 2) return true;
  if (value % 2 === 0) return false;
  
  const sqrt = Math.sqrt(value);
  for (let i = 3; i <= sqrt; i += 2) {
    if (value % i === 0) return false;
  }
  return true;
}

// ==================== 字符串验证 ====================

/**
 * 检查字符串长度是否在指定范围内
 */
export function isLengthInRange(value: string, min: number, max: number): boolean {
  const len = value.length;
  return len >= min && len <= max;
}

/**
 * 检查是否为纯字母
 */
export function isAlpha(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.alpha.test(value);
}

/**
 * 检查是否为字母和数字组合
 */
export function isAlphanumeric(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.alphanumeric.test(value);
}

/**
 * 检查是否为有效的用户名（字母开头，可包含数字和下划线）
 */
export function isUsername(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.username.test(value);
}

/**
 * 检查是否为有效的 slug（URL 友好格式）
 */
export function isSlug(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.slug.test(value);
}

/**
 * 检查是否为有效的十六进制颜色值
 */
export function isHexColor(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.hexColor.test(value);
}

/**
 * 检查是否为有效的中国邮政编码
 */
export function isPostalCodeCN(value: string): boolean {
  if (isEmpty(value)) return false;
  return REGEX.postalCodeCN.test(value);
}

// ==================== 日期验证 ====================

/**
 * 检查字符串是否为有效日期
 * 支持格式：YYYY-MM-DD、YYYY/MM/DD、YYYYMMDD
 */
export function isDate(value: string): boolean {
  if (isEmpty(value)) return false;
  
  // 标准化格式
  let dateStr = value.trim();
  
  // 处理 YYYYMMDD 格式
  if (/^\d{8}$/.test(dateStr)) {
    dateStr = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`;
  }
  
  // 统一分隔符
  dateStr = dateStr.replace(/\//g, '-');
  
  // 验证格式
  if (!/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return false;
  
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return false;
  
  // 验证日期是否真实存在
  const [year, month, day] = dateStr.split('-').map(Number);
  return date.getFullYear() === year &&
         date.getMonth() + 1 === month &&
         date.getDate() === day;
}

/**
 * 检查日期是否在指定范围内
 */
export function isDateInRange(date: string | Date, startDate: string | Date, endDate: string | Date): boolean {
  const d = typeof date === 'string' ? new Date(date) : date;
  const start = typeof startDate === 'string' ? new Date(startDate) : startDate;
  const end = typeof endDate === 'string' ? new Date(endDate) : endDate;
  
  if (isNaN(d.getTime()) || isNaN(start.getTime()) || isNaN(end.getTime())) {
    return false;
  }
  
  return d >= start && d <= end;
}

// ==================== 组合验证 ====================

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * 创建验证器
 */
export class Validator {
  private value: any;
  private errors: string[] = [];

  constructor(value: any) {
    this.value = value;
  }

  static of(value: any): Validator {
    return new Validator(value);
  }

  /**
   * 检查非空
   */
  required(message: string = '此字段不能为空'): Validator {
    if (isEmpty(this.value)) {
      this.errors.push(message);
    }
    return this;
  }

  /**
   * 检查邮箱格式
   */
  email(message: string = '请输入有效的邮箱地址'): Validator {
    if (isNotEmpty(this.value) && !isEmail(this.value)) {
      this.errors.push(message);
    }
    return this;
  }

  /**
   * 检查手机号格式
   */
  phoneCN(message: string = '请输入有效的手机号码'): Validator {
    if (isNotEmpty(this.value) && !isPhoneCN(this.value)) {
      this.errors.push(message);
    }
    return this;
  }

  /**
   * 检查 URL 格式
   */
  url(message: string = '请输入有效的URL', strict: boolean = false): Validator {
    if (isNotEmpty(this.value) && !isURL(this.value, strict)) {
      this.errors.push(message);
    }
    return this;
  }

  /**
   * 检查最小长度
   */
  minLength(min: number, message?: string): Validator {
    const msg = message || `长度不能少于 ${min} 个字符`;
    if (isNotEmpty(this.value) && this.value.length < min) {
      this.errors.push(msg);
    }
    return this;
  }

  /**
   * 检查最大长度
   */
  maxLength(max: number, message?: string): Validator {
    const msg = message || `长度不能超过 ${max} 个字符`;
    if (isNotEmpty(this.value) && this.value.length > max) {
      this.errors.push(msg);
    }
    return this;
  }

  /**
   * 检查数值范围
   */
  range(min: number, max: number, message?: string): Validator {
    const msg = message || `数值必须在 ${min} 到 ${max} 之间`;
    if (this.value !== null && this.value !== undefined) {
      const num = Number(this.value);
      if (isNaN(num) || !isInRange(num, min, max)) {
        this.errors.push(msg);
      }
    }
    return this;
  }

  /**
   * 自定义验证
   */
  custom(validateFn: (value: any) => boolean, message: string): Validator {
    if (isNotEmpty(this.value) && !validateFn(this.value)) {
      this.errors.push(message);
    }
    return this;
  }

  /**
   * 获取验证结果
   */
  result(): ValidationResult {
    return {
      valid: this.errors.length === 0,
      errors: this.errors
    };
  }
}

// ==================== 批量验证 ====================

export interface FieldRule {
  required?: boolean;
  email?: boolean;
  phoneCN?: boolean;
  url?: boolean;
  urlStrict?: boolean;
  idCardCN?: boolean;
  bankCard?: boolean;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  message?: string;
}

export type Schema = Record<string, FieldRule>;

/**
 * 验证对象是否符合指定的 schema
 */
export function validate(data: Record<string, any>, schema: Schema): ValidationResult {
  const errors: string[] = [];

  for (const [field, rules] of Object.entries(schema)) {
    const value = data[field];
    const fieldName = rules.message || field;

    if (rules.required && isEmpty(value)) {
      errors.push(`${fieldName}不能为空`);
      continue;
    }

    if (isEmpty(value)) continue;

    if (rules.email && !isEmail(value)) {
      errors.push(`${fieldName}格式不正确`);
    }

    if (rules.phoneCN && !isPhoneCN(value)) {
      errors.push(`${fieldName}格式不正确`);
    }

    if ((rules.url || rules.urlStrict) && !isURL(value, rules.urlStrict)) {
      errors.push(`${fieldName}格式不正确`);
    }

    if (rules.idCardCN && !isIDCardCN(value)) {
      errors.push(`${fieldName}格式不正确`);
    }

    if (rules.bankCard && !isBankCard(value)) {
      errors.push(`${fieldName}格式不正确`);
    }

    if (rules.minLength !== undefined && value.length < rules.minLength) {
      errors.push(`${fieldName}长度不能少于${rules.minLength}个字符`);
    }

    if (rules.maxLength !== undefined && value.length > rules.maxLength) {
      errors.push(`${fieldName}长度不能超过${rules.maxLength}个字符`);
    }

    if (rules.min !== undefined || rules.max !== undefined) {
      const num = Number(value);
      if (!isNaN(num)) {
        if (rules.min !== undefined && num < rules.min) {
          errors.push(`${fieldName}不能小于${rules.min}`);
        }
        if (rules.max !== undefined && num > rules.max) {
          errors.push(`${fieldName}不能大于${rules.max}`);
        }
      }
    }

    if (rules.pattern && !rules.pattern.test(value)) {
      errors.push(`${fieldName}格式不正确`);
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

// 导出所有函数
export default {
  // 基础验证
  isEmpty,
  isNotEmpty,
  isEmail,
  isPhoneCN,
  isPhoneInternational,
  isURL,
  
  // 身份证
  isIDCardCN,
  parseIDCardCN,
  
  // 银行卡
  isBankCard,
  
  // IP 地址
  isIPv4,
  isIPv6,
  isIP,
  
  // 密码
  validatePassword,
  
  // 数值
  isInRange,
  isInteger,
  isPositiveInteger,
  isNegativeInteger,
  isEven,
  isOdd,
  isPrime,
  
  // 字符串
  isLengthInRange,
  isAlpha,
  isAlphanumeric,
  isUsername,
  isSlug,
  isHexColor,
  isPostalCodeCN,
  
  // 日期
  isDate,
  isDateInRange,
  
  // 工具
  Validator,
  validate
};