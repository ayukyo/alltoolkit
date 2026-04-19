/**
 * Number Utilities - JavaScript 数字工具模块
 * 
 * 提供常用的数字操作函数，包括格式化、解析、验证、范围操作、数学运算等
 * 零依赖，仅使用 JavaScript 标准库
 * 
 * @module number_utils
 * @version 1.0.0
 */

const NumberUtils = {
  // ==================== 常量定义 ====================

  /**
   * 数学常量
   */
  CONSTANTS: {
    PI: Math.PI,
    E: Math.E,
    LN2: Math.LN2,
    LN10: Math.LN10,
    LOG2E: Math.LOG2E,
    LOG10E: Math.LOG10E,
    SQRT2: Math.SQRT2,
    SQRT1_2: Math.SQRT1_2,
    PHI: (1 + Math.sqrt(5)) / 2, // 黄金比例
    TAU: 2 * Math.PI, // 圆周率的两倍
  },

  /**
   * 数字类型枚举
   */
  TYPES: {
    INTEGER: 'integer',
    FLOAT: 'float',
    NAN: 'nan',
    INFINITY: 'infinity',
    NEGATIVE_INFINITY: 'negative_infinity',
    SAFE_INTEGER: 'safe_integer',
  },

  // ==================== 类型判断 ====================

  /**
   * 检查是否为数字
   * @param {*} value - 要检查的值
   * @returns {boolean} 是否为数字
   */
  isNumber(value) {
    return typeof value === 'number' && !isNaN(value);
  },

  /**
   * 检查是否为整数
   * @param {*} value - 要检查的值
   * @returns {boolean} 是否为整数
   */
  isInteger(value) {
    return Number.isInteger(value);
  },

  /**
   * 检查是否为浮点数
   * @param {*} value - 要检查的值
   * @returns {boolean} 是否为浮点数
   */
  isFloat(value) {
    return this.isNumber(value) && !Number.isInteger(value) && isFinite(value);
  },

  /**
   * 检查是否为安全整数
   * @param {*} value - 要检查的值
   * @returns {boolean} 是否为安全整数
   */
  isSafeInteger(value) {
    return Number.isSafeInteger(value);
  },

  /**
   * 检查是否为正数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为正数
   */
  isPositive(value) {
    return this.isNumber(value) && value > 0;
  },

  /**
   * 检查是否为负数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为负数
   */
  isNegative(value) {
    return this.isNumber(value) && value < 0;
  },

  /**
   * 检查是否为零
   * @param {number} value - 要检查的数字
   * @param {number} [epsilon=Number.EPSILON] - 容差
   * @returns {boolean} 是否为零
   */
  isZero(value, epsilon = Number.EPSILON) {
    return this.isNumber(value) && Math.abs(value) < epsilon;
  },

  /**
   * 检查是否为偶数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为偶数
   */
  isEven(value) {
    return this.isInteger(value) && value % 2 === 0;
  },

  /**
   * 检查是否为奇数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为奇数
   */
  isOdd(value) {
    return this.isInteger(value) && value % 2 !== 0;
  },

  /**
   * 检查是否为质数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为质数
   */
  isPrime(value) {
    if (!this.isInteger(value) || value < 2) return false;
    if (value === 2) return true;
    if (value % 2 === 0) return false;
    for (let i = 3; i <= Math.sqrt(value); i += 2) {
      if (value % i === 0) return false;
    }
    return true;
  },

  /**
   * 检查是否为完全平方数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为完全平方数
   */
  isPerfectSquare(value) {
    if (!this.isInteger(value) || value < 0) return false;
    const sqrt = Math.sqrt(value);
    return sqrt === Math.floor(sqrt);
  },

  /**
   * 检查是否为完全立方数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为完全立方数
   */
  isPerfectCube(value) {
    if (!this.isInteger(value)) return false;
    const cbrt = Math.cbrt(Math.abs(value));
    return cbrt === Math.floor(cbrt);
  },

  /**
   * 检查是否为斐波那契数
   * @param {number} value - 要检查的数字
   * @returns {boolean} 是否为斐波那契数
   */
  isFibonacci(value) {
    if (!this.isInteger(value) || value < 0) return false;
    // 一个数是斐波那契数当且仅当 5*n^2 + 4 或 5*n^2 - 4 是完全平方数
    const n = value;
    return this.isPerfectSquare(5 * n * n + 4) || this.isPerfectSquare(5 * n * n - 4);
  },

  /**
   * 检查是否在范围内
   * @param {number} value - 要检查的数字
   * @param {number} min - 最小值
   * @param {number} max - 最大值
   * @param {boolean} [inclusive=true] - 是否包含边界
   * @returns {boolean} 是否在范围内
   */
  inRange(value, min, max, inclusive = true) {
    if (!this.isNumber(value) || !this.isNumber(min) || !this.isNumber(max)) {
      return false;
    }
    if (inclusive) {
      return value >= min && value <= max;
    }
    return value > min && value < max;
  },

  /**
   * 获取数字类型
   * @param {*} value - 要检查的值
   * @returns {string} 数字类型
   */
  getType(value) {
    if (typeof value !== 'number') return 'not_a_number';
    if (isNaN(value)) return this.TYPES.NAN;
    if (value === Infinity) return this.TYPES.INFINITY;
    if (value === -Infinity) return this.TYPES.NEGATIVE_INFINITY;
    if (Number.isInteger(value)) {
      if (this.isSafeInteger(value)) return this.TYPES.SAFE_INTEGER;
      return this.TYPES.INTEGER;
    }
    return this.TYPES.FLOAT;
  },

  // ==================== 解析与转换 ====================

  /**
   * 安全解析数字
   * @param {*} value - 要解析的值
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @returns {number} 解析后的数字
   */
  parse(value, defaultValue = 0) {
    if (value === null || value === undefined) return defaultValue;
    const num = Number(value);
    return isNaN(num) ? defaultValue : num;
  },

  /**
   * 解析整数
   * @param {*} value - 要解析的值
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @param {number} [radix=10] - 进制
   * @returns {number} 解析后的整数
   */
  parseInt(value, defaultValue = 0, radix = 10) {
    if (typeof value === 'number' && Number.isInteger(value)) {
      return value;
    }
    const parsed = parseInt(value, radix);
    return isNaN(parsed) ? defaultValue : parsed;
  },

  /**
   * 解析浮点数
   * @param {*} value - 要解析的值
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @returns {number} 解析后的浮点数
   */
  parseFloat(value, defaultValue = 0) {
    if (typeof value === 'number' && !isNaN(value)) {
      return value;
    }
    const parsed = parseFloat(value);
    return isNaN(parsed) ? defaultValue : parsed;
  },

  /**
   * 从字符串解析数字（支持千分位）
   * @param {string} str - 要解析的字符串
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @returns {number} 解析后的数字
   */
  fromString(str, defaultValue = 0) {
    if (typeof str !== 'string') return this.parse(str, defaultValue);
    // 移除千分位分隔符和空格
    const cleaned = str.replace(/,/g, '').trim();
    return this.parse(cleaned, defaultValue);
  },

  /**
   * 从二进制字符串解析
   * @param {string} binaryStr - 二进制字符串
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @returns {number} 解析后的数字
   */
  fromBinary(binaryStr, defaultValue = 0) {
    if (!/^[01]+$/.test(binaryStr)) return defaultValue;
    return parseInt(binaryStr, 2);
  },

  /**
   * 从十六进制字符串解析
   * @param {string} hexStr - 十六进制字符串
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @returns {number} 解析后的数字
   */
  fromHex(hexStr, defaultValue = 0) {
    const cleaned = hexStr.replace(/^0x/i, '');
    if (!/^[0-9a-fA-F]+$/.test(cleaned)) return defaultValue;
    return parseInt(cleaned, 16);
  },

  /**
   * 从八进制字符串解析
   * @param {string} octalStr - 八进制字符串
   * @param {number} [defaultValue=0] - 解析失败时的默认值
   * @returns {number} 解析后的数字
   */
  fromOctal(octalStr, defaultValue = 0) {
    const cleaned = octalStr.replace(/^0o?/i, '');
    if (!/^[0-7]+$/.test(cleaned)) return defaultValue;
    return parseInt(cleaned, 8);
  },

  /**
   * 转换为二进制字符串
   * @param {number} value - 要转换的数字
   * @returns {string} 二进制字符串
   */
  toBinary(value) {
    if (!this.isInteger(value)) return 'NaN';
    return Math.abs(value).toString(2);
  },

  /**
   * 转换为十六进制字符串
   * @param {number} value - 要转换的数字
   * @param {boolean} [prefix=true] - 是否添加0x前缀
   * @returns {string} 十六进制字符串
   */
  toHex(value, prefix = true) {
    if (!this.isInteger(value)) return 'NaN';
    const hex = Math.abs(value).toString(16);
    return prefix ? `0x${hex}` : hex;
  },

  /**
   * 转换为八进制字符串
   * @param {number} value - 要转换的数字
   * @param {boolean} [prefix=true] - 是否添加0o前缀
   * @returns {string} 八进制字符串
   */
  toOctal(value, prefix = true) {
    if (!this.isInteger(value)) return 'NaN';
    const octal = Math.abs(value).toString(8);
    return prefix ? `0o${octal}` : octal;
  },

  // ==================== 格式化 ====================

  /**
   * 格式化数字（添加千分位）
   * @param {number} value - 要格式化的数字
   * @param {number} [decimals=0] - 小数位数
   * @param {string} [thousandsSeparator=','] - 千分位分隔符
   * @param {string} [decimalSeparator='.'] - 小数分隔符
   * @returns {string} 格式化后的字符串
   */
  format(value, decimals = 0, thousandsSeparator = ',', decimalSeparator = '.') {
    if (!this.isNumber(value)) return 'NaN';
    
    const fixed = decimals >= 0 ? value.toFixed(decimals) : String(value);
    const [intPart, decPart] = fixed.split('.');
    
    // 添加千分位分隔符
    const formattedInt = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, thousandsSeparator);
    
    return decPart ? `${formattedInt}${decimalSeparator}${decPart}` : formattedInt;
  },

  /**
   * 格式化为货币
   * @param {number} value - 要格式化的数字
   * @param {string} [currency='¥'] - 货币符号
   * @param {number} [decimals=2] - 小数位数
   * @returns {string} 格式化后的货币字符串
   */
  formatCurrency(value, currency = '¥', decimals = 2) {
    if (!this.isNumber(value)) return 'NaN';
    return `${currency}${this.format(Math.abs(value), decimals)}`;
  },

  /**
   * 格式化为百分比
   * @param {number} value - 要格式化的数字（0-1 或 0-100）
   * @param {number} [decimals=2] - 小数位数
   * @param {boolean} [alreadyPercent=false] - 是否已经是百分比形式
   * @returns {string} 格式化后的百分比字符串
   */
  formatPercent(value, decimals = 2, alreadyPercent = false) {
    if (!this.isNumber(value)) return 'NaN';
    const percent = alreadyPercent ? value : value * 100;
    return `${percent.toFixed(decimals)}%`;
  },

  /**
   * 格式化科学计数法
   * @param {number} value - 要格式化的数字
   * @param {number} [decimals=2] - 小数位数
   * @returns {string} 科学计数法字符串
   */
  formatScientific(value, decimals = 2) {
    if (!this.isNumber(value)) return 'NaN';
    return value.toExponential(decimals);
  },

  /**
   * 格式化文件大小
   * @param {number} bytes - 字节数
   * @param {number} [decimals=2] - 小数位数
   * @param {boolean} [si=true] - 是否使用SI单位（1000进制）
   * @returns {string} 格式化后的文件大小
   */
  formatFileSize(bytes, decimals = 2, si = true) {
    if (!this.isNumber(bytes) || bytes < 0) return 'NaN';
    
    const units = si
      ? ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
      : ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    
    const base = si ? 1000 : 1024;
    
    if (bytes === 0) return `0 ${units[0]}`;
    
    const exp = Math.floor(Math.log(bytes) / Math.log(base));
    const index = Math.min(exp, units.length - 1);
    const size = bytes / Math.pow(base, index);
    
    return `${size.toFixed(decimals)} ${units[index]}`;
  },

  /**
   * 格式化持续时间
   * @param {number} ms - 毫秒数
   * @param {Object} [options] - 选项
   * @param {boolean} [options.compact=false] - 是否使用紧凑格式
   * @returns {string} 格式化后的持续时间
   */
  formatDuration(ms, options = {}) {
    if (!this.isNumber(ms)) return 'NaN';
    
    const { compact = false } = options;
    const abs = Math.abs(ms);
    
    if (abs < 1000) return `${ms}ms`;
    if (abs < 60000) {
      const s = (ms / 1000).toFixed(compact ? 0 : 2);
      return compact ? `${s}s` : `${s} seconds`;
    }
    if (abs < 3600000) {
      const m = Math.floor(ms / 60000);
      const s = Math.floor((ms % 60000) / 1000);
      if (compact) return `${m}m${s}s`;
      return `${m} minute${m !== 1 ? 's' : ''} ${s} second${s !== 1 ? 's' : ''}`;
    }
    if (abs < 86400000) {
      const h = Math.floor(ms / 3600000);
      const m = Math.floor((ms % 3600000) / 60000);
      if (compact) return `${h}h${m}m`;
      return `${h} hour${h !== 1 ? 's' : ''} ${m} minute${m !== 1 ? 's' : ''}`;
    }
    
    const d = Math.floor(ms / 86400000);
    const h = Math.floor((ms % 86400000) / 3600000);
    if (compact) return `${d}d${h}h`;
    return `${d} day${d !== 1 ? 's' : ''} ${h} hour${h !== 1 ? 's' : ''}`;
  },

  /**
   * 中文数字格式化
   * @param {number} value - 要格式化的数字
   * @param {Object} [options] - 选项
   * @param {boolean} [options.traditional=false] - 是否使用繁体中文
   * @returns {string} 中文数字
   */
  formatChinese(value, options = {}) {
    if (!this.isInteger(value) || value < 0 || value > 9999999999999999) {
      return String(value);
    }
    
    const { traditional = false } = options;
    
    const chars = traditional
      ? ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
      : ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'];
    
    const units = ['', '十', '百', '千'];
    const bigUnits = ['', '万', '亿', '兆'];
    
    if (value === 0) return chars[0];
    
    // 特殊处理：10-19 的简化写法
    if (value >= 10 && value <= 19) {
      const digit = value % 10;
      if (digit === 0) return '十';
      return '十' + chars[digit];
    }
    
    const result = [];
    let unitIndex = 0;
    
    const processSection = (num) => {
      const section = [];
      let zero = false;
      const isLeading = result.length === 0; // 是否是最高位部分
      
      for (let i = 3; i >= 0; i--) {
        const divisor = Math.pow(10, i);
        const digit = Math.floor(num / divisor) % 10;
        if (digit === 0) {
          zero = true;
        } else {
          if (zero && section.length > 0) {
            section.push(chars[0]);
          }
          zero = false;
          // 对于最高位部分的十位，如果是1，可以省略"一"
          if (isLeading && i === 1 && digit === 1) {
            section.push(units[i]); // 只加"十"，不加"一"
          } else {
            section.push(chars[digit]);
            if (i > 0) section.push(units[i]);
          }
        }
      }
      return section.join('');
    };
    
    while (value > 0) {
      const section = value % 10000;
      if (section > 0) {
        const sectionStr = processSection(section);
        result.unshift(sectionStr + bigUnits[unitIndex]);
      }
      value = Math.floor(value / 10000);
      unitIndex++;
    }
    
    return result.join('');
  },

  // ==================== 数学运算 ====================

  /**
   * 加法（避免精度问题）
   * @param {number} a - 第一个数字
   * @param {number} b - 第二个数字
   * @returns {number} 和
   */
  add(a, b) {
    const decimals = Math.max(
      (String(a).split('.')[1] || '').length,
      (String(b).split('.')[1] || '').length
    );
    const factor = Math.pow(10, decimals);
    return (Math.round(a * factor) + Math.round(b * factor)) / factor;
  },

  /**
   * 减法（避免精度问题）
   * @param {number} a - 被减数
   * @param {number} b - 减数
   * @returns {number} 差
   */
  subtract(a, b) {
    return this.add(a, -b);
  },

  /**
   * 乘法（避免精度问题）
   * @param {number} a - 第一个数字
   * @param {number} b - 第二个数字
   * @returns {number} 积
   */
  multiply(a, b) {
    const decimals = (String(a).split('.')[1] || '').length + 
                     (String(b).split('.')[1] || '').length;
    const factor = Math.pow(10, decimals);
    return (Math.round(a * Math.pow(10, (String(a).split('.')[1] || '').length)) *
            Math.round(b * Math.pow(10, (String(b).split('.')[1] || '').length))) /
           factor;
  },

  /**
   * 除法（避免精度问题）
   * @param {number} a - 被除数
   * @param {number} b - 除数
   * @param {number} [decimals=10] - 结果小数位数
   * @returns {number} 商
   */
  divide(a, b, decimals = 10) {
    if (b === 0) return NaN;
    return Number((a / b).toFixed(decimals));
  },

  /**
   * 求余数
   * @param {number} a - 被除数
   * @param {number} b - 除数
   * @returns {number} 余数
   */
  modulo(a, b) {
    if (b === 0) return NaN;
    return ((a % b) + b) % b;
  },

  /**
   * 计算百分比
   * @param {number} value - 当前值
   * @param {number} total - 总值
   * @param {number} [decimals=2] - 小数位数
   * @returns {number} 百分比
   */
  percentage(value, total, decimals = 2) {
    if (total === 0) return 0;
    return Number(((value / total) * 100).toFixed(decimals));
  },

  /**
   * 计算增长率
   * @param {number} oldValue - 旧值
   * @param {number} newValue - 新值
   * @param {number} [decimals=2] - 小数位数
   * @returns {number} 增长率（百分比）
   */
  growthRate(oldValue, newValue, decimals = 2) {
    if (oldValue === 0) return newValue === 0 ? 0 : 100;
    return Number((((newValue - oldValue) / oldValue) * 100).toFixed(decimals));
  },

  /**
   * 求平均值
   * @param {number[]} numbers - 数字数组
   * @returns {number} 平均值
   */
  average(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) return NaN;
    const sum = numbers.reduce((acc, n) => acc + this.parse(n, 0), 0);
    return sum / numbers.length;
  },

  /**
   * 求中位数
   * @param {number[]} numbers - 数字数组
   * @returns {number} 中位数
   */
  median(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) return NaN;
    const sorted = [...numbers].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 !== 0
      ? sorted[mid]
      : (sorted[mid - 1] + sorted[mid]) / 2;
  },

  /**
   * 求众数
   * @param {number[]} numbers - 数字数组
   * @returns {number[]} 众数数组
   */
  mode(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) return [];
    
    const counts = new Map();
    let maxCount = 0;
    
    for (const n of numbers) {
      const count = (counts.get(n) || 0) + 1;
      counts.set(n, count);
      maxCount = Math.max(maxCount, count);
    }
    
    const modes = [];
    for (const [num, count] of counts) {
      if (count === maxCount) modes.push(num);
    }
    
    return modes;
  },

  /**
   * 求标准差
   * @param {number[]} numbers - 数字数组
   * @param {boolean} [population=true] - 是否为总体标准差
   * @returns {number} 标准差
   */
  standardDeviation(numbers, population = true) {
    if (!Array.isArray(numbers) || numbers.length < 2) return NaN;
    
    const avg = this.average(numbers);
    const squaredDiffs = numbers.map(n => Math.pow(n - avg, 2));
    const avgSquaredDiff = squaredDiffs.reduce((a, b) => a + b, 0) / 
                           (population ? numbers.length : numbers.length - 1);
    
    return Math.sqrt(avgSquaredDiff);
  },

  /**
   * 求方差
   * @param {number[]} numbers - 数字数组
   * @param {boolean} [population=true] - 是否为总体方差
   * @returns {number} 方差
   */
  variance(numbers, population = true) {
    const std = this.standardDeviation(numbers, population);
    return isNaN(std) ? NaN : std * std;
  },

  // ==================== 范围操作 ====================

  /**
   * 限制在范围内
   * @param {number} value - 要限制的值
   * @param {number} min - 最小值
   * @param {number} max - 最大值
   * @returns {number} 限制后的值
   */
  clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  },

  /**
   * 线性插值
   * @param {number} value - 要插值的值
   * @param {number} inMin - 输入最小值
   * @param {number} inMax - 输入最大值
   * @param {number} outMin - 输出最小值
   * @param {number} outMax - 输出最大值
   * @returns {number} 插值后的值
   */
  mapRange(value, inMin, inMax, outMin, outMax) {
    return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
  },

  /**
   * 生成数字范围
   * @param {number} start - 起始值
   * @param {number} end - 结束值
   * @param {number} [step=1] - 步长
   * @returns {number[]} 数字数组
   */
  range(start, end, step = 1) {
    const result = [];
    if (step > 0) {
      for (let i = start; i < end; i += step) {
        result.push(i);
      }
    } else if (step < 0) {
      for (let i = start; i > end; i += step) {
        result.push(i);
      }
    }
    return result;
  },

  /**
   * 生成数字序列
   * @param {number} start - 起始值
   * @param {number} count - 数量
   * @param {number} [step=1] - 步长
   * @returns {number[]} 数字数组
   */
  sequence(start, count, step = 1) {
    const result = [];
    for (let i = 0; i < count; i++) {
      result.push(start + i * step);
    }
    return result;
  },

  /**
   * 循环值
   * @param {number} value - 当前值
   * @param {number} min - 最小值
   * @param {number} max - 最大值
   * @returns {number} 循环后的值
   */
  wrap(value, min, max) {
    const range = max - min;
    return min + ((((value - min) % range) + range) % range);
  },

  /**
   * 最近值
   * @param {number} value - 当前值
   * @param {number[]} candidates - 候选值数组
   * @returns {number} 最接近的值
   */
  closest(value, candidates) {
    if (!Array.isArray(candidates) || candidates.length === 0) return value;
    return candidates.reduce((closest, candidate) => 
      Math.abs(candidate - value) < Math.abs(closest - value) ? candidate : closest
    );
  },

  // ==================== 随机数 ====================

  /**
   * 生成随机整数
   * @param {number} min - 最小值（包含）
   * @param {number} max - 最大值（包含）
   * @returns {number} 随机整数
   */
  randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  },

  /**
   * 生成随机浮点数
   * @param {number} min - 最小值
   * @param {number} max - 最大值
   * @param {number} [decimals=2] - 小数位数
   * @returns {number} 随机浮点数
   */
  randomFloat(min, max, decimals = 2) {
    const random = Math.random() * (max - min) + min;
    return Number(random.toFixed(decimals));
  },

  /**
   * 从数组中随机选择
   * @param {number[]} array - 数字数组
   * @returns {*} 随机选择的元素
   */
  randomChoice(array) {
    if (!Array.isArray(array) || array.length === 0) return undefined;
    return array[Math.floor(Math.random() * array.length)];
  },

  /**
   * 生成随机数组
   * @param {number} count - 数量
   * @param {number} min - 最小值
   * @param {number} max - 最大值
   * @param {boolean} [unique=false] - 是否唯一
   * @returns {number[]} 随机数组
   */
  randomArray(count, min, max, unique = false) {
    if (unique && max - min + 1 < count) {
      throw new Error('Range too small for unique random array');
    }
    
    if (unique) {
      const pool = this.range(min, max + 1);
      const result = [];
      for (let i = 0; i < count; i++) {
        const index = this.randomInt(0, pool.length - 1);
        result.push(pool.splice(index, 1)[0]);
      }
      return result;
    }
    
    return Array.from({ length: count }, () => this.randomInt(min, max));
  },

  /**
   * 打乱数组
   * @param {number[]} array - 数字数组
   * @returns {number[]} 打乱后的数组
   */
  shuffle(array) {
    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  },

  // ==================== 数论函数 ====================

  /**
   * 最大公约数
   * @param {number} a - 第一个数
   * @param {number} b - 第二个数
   * @returns {number} 最大公约数
   */
  gcd(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while (b !== 0) {
      [a, b] = [b, a % b];
    }
    return a;
  },

  /**
   * 最小公倍数
   * @param {number} a - 第一个数
   * @param {number} b - 第二个数
   * @returns {number} 最小公倍数
   */
  lcm(a, b) {
    return Math.abs(a * b) / this.gcd(a, b);
  },

  /**
   * 阶乘
   * @param {number} n - 非负整数
   * @returns {number} 阶乘结果
   */
  factorial(n) {
    if (!this.isInteger(n) || n < 0) return NaN;
    if (n <= 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
      result *= i;
    }
    return result;
  },

  /**
   * 排列数
   * @param {number} n - 总数
   * @param {number} r - 选取数
   * @returns {number} 排列数
   */
  permutation(n, r) {
    if (!this.isInteger(n) || !this.isInteger(r) || n < 0 || r < 0 || r > n) {
      return NaN;
    }
    let result = 1;
    for (let i = n; i > n - r; i--) {
      result *= i;
    }
    return result;
  },

  /**
   * 组合数
   * @param {number} n - 总数
   * @param {number} r - 选取数
   * @returns {number} 组合数
   */
  combination(n, r) {
    if (!this.isInteger(n) || !this.isInteger(r) || n < 0 || r < 0 || r > n) {
      return NaN;
    }
    return this.permutation(n, r) / this.factorial(r);
  },

  /**
   * 斐波那契数列
   * @param {number} n - 项数
   * @returns {number} 第n项斐波那契数
   */
  fibonacci(n) {
    if (!this.isInteger(n) || n < 0) return NaN;
    if (n <= 1) return n;
    
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
      [a, b] = [b, a + b];
    }
    return b;
  },

  /**
   * 获取所有因数
   * @param {number} n - 正整数
   * @returns {number[]} 因数数组
   */
  factors(n) {
    if (!this.isInteger(n) || n <= 0) return [];
    
    const result = [];
    for (let i = 1; i <= Math.sqrt(n); i++) {
      if (n % i === 0) {
        result.push(i);
        if (i !== n / i) {
          result.push(n / i);
        }
      }
    }
    return result.sort((a, b) => a - b);
  },

  /**
   * 质因数分解
   * @param {number} n - 正整数
   * @returns {number[]} 质因数数组
   */
  primeFactors(n) {
    if (!this.isInteger(n) || n <= 1) return [];
    
    const factors = [];
    let d = 2;
    while (n > 1) {
      while (n % d === 0) {
        factors.push(d);
        n = Math.floor(n / d);
      }
      d++;
      if (d * d > n && n > 1) {
        factors.push(n);
        break;
      }
    }
    return factors;
  },

  /**
   * 判断两个数是否互质
   * @param {number} a - 第一个数
   * @param {number} b - 第二个数
   * @returns {boolean} 是否互质
   */
  areCoprime(a, b) {
    return this.gcd(a, b) === 1;
  },

  /**
   * 生成质数序列
   * @param {number} n - 质数数量
   * @returns {number[]} 质数数组
   */
  generatePrimes(n) {
    if (n <= 0) return [];
    
    const primes = [];
    let candidate = 2;
    
    while (primes.length < n) {
      if (this.isPrime(candidate)) {
        primes.push(candidate);
      }
      candidate++;
    }
    
    return primes;
  },

  /**
   * 埃拉托斯特尼筛法
   * @param {number} max - 最大值
   * @returns {number[]} 小于等于max的所有质数
   */
  sieveOfEratosthenes(max) {
    if (!this.isInteger(max) || max < 2) return [];
    
    const sieve = new Array(max + 1).fill(true);
    sieve[0] = sieve[1] = false;
    
    for (let i = 2; i * i <= max; i++) {
      if (sieve[i]) {
        for (let j = i * i; j <= max; j += i) {
          sieve[j] = false;
        }
      }
    }
    
    const primes = [];
    for (let i = 2; i <= max; i++) {
      if (sieve[i]) primes.push(i);
    }
    
    return primes;
  },

  // ==================== 数值处理 ====================

  /**
   * 四舍五入到指定小数位
   * @param {number} value - 要处理的值
   * @param {number} [decimals=0] - 小数位数
   * @returns {number} 处理后的值
   */
  round(value, decimals = 0) {
    const factor = Math.pow(10, decimals);
    return Math.round(value * factor) / factor;
  },

  /**
   * 向上取整到指定小数位
   * @param {number} value - 要处理的值
   * @param {number} [decimals=0] - 小数位数
   * @returns {number} 处理后的值
   */
  ceil(value, decimals = 0) {
    const factor = Math.pow(10, decimals);
    return Math.ceil(value * factor) / factor;
  },

  /**
   * 向下取整到指定小数位
   * @param {number} value - 要处理的值
   * @param {number} [decimals=0] - 小数位数
   * @returns {number} 处理后的值
   */
  floor(value, decimals = 0) {
    const factor = Math.pow(10, decimals);
    return Math.floor(value * factor) / factor;
  },

  /**
   * 截断到指定小数位
   * @param {number} value - 要处理的值
   * @param {number} [decimals=0] - 小数位数
   * @returns {number} 处理后的值
   */
  truncate(value, decimals = 0) {
    const factor = Math.pow(10, decimals);
    return Math.trunc(value * factor) / factor;
  },

  /**
   * 四舍五入到指定精度
   * @param {number} value - 要处理的值
   * @param {number} precision - 精度（如 0.01 表示保留两位小数）
   * @returns {number} 处理后的值
   */
  roundTo(value, precision) {
    return Math.round(value / precision) * precision;
  },

  /**
   * 符号函数
   * @param {number} value - 要处理的值
   * @returns {number} -1, 0, 或 1
   */
  sign(value) {
    return Math.sign(value);
  },

  /**
   * 绝对值
   * @param {number} value - 要处理的值
   * @returns {number} 绝对值
   */
  abs(value) {
    return Math.abs(value);
  },

  /**
   * 平方根
   * @param {number} value - 要处理的值
   * @returns {number} 平方根
   */
  sqrt(value) {
    return Math.sqrt(value);
  },

  /**
   * 立方根
   * @param {number} value - 要处理的值
   * @returns {number} 立方根
   */
  cbrt(value) {
    return Math.cbrt(value);
  },

  /**
   * 幂运算
   * @param {number} base - 底数
   * @param {number} exponent - 指数
   * @returns {number} 幂运算结果
   */
  pow(base, exponent) {
    return Math.pow(base, exponent);
  },

  /**
   * 自然对数
   * @param {number} value - 要处理的值
   * @returns {number} 自然对数
   */
  log(value) {
    return Math.log(value);
  },

  /**
   * 以10为底的对数
   * @param {number} value - 要处理的值
   * @returns {number} 对数
   */
  log10(value) {
    return Math.log10(value);
  },

  /**
   * 以2为底的对数
   * @param {number} value - 要处理的值
   * @returns {number} 对数
   */
  log2(value) {
    return Math.log2(value);
  },

  /**
   * 自然指数
   * @param {number} value - 要处理的值
   * @returns {number} e的value次方
   */
  exp(value) {
    return Math.exp(value);
  },

  /**
   * 三角函数 - 正弦
   * @param {number} radians - 弧度
   * @returns {number} 正弦值
   */
  sin(radians) {
    return Math.sin(radians);
  },

  /**
   * 三角函数 - 余弦
   * @param {number} radians - 弧度
   * @returns {number} 余弦值
   */
  cos(radians) {
    return Math.cos(radians);
  },

  /**
   * 三角函数 - 正切
   * @param {number} radians - 弧度
   * @returns {number} 正切值
   */
  tan(radians) {
    return Math.tan(radians);
  },

  /**
   * 弧度转角度
   * @param {number} radians - 弧度
   * @returns {number} 角度
   */
  toDegrees(radians) {
    return radians * (180 / Math.PI);
  },

  /**
   * 角度转弧度
   * @param {number} degrees - 角度
   * @returns {number} 弧度
   */
  toRadians(degrees) {
    return degrees * (Math.PI / 180);
  },

  /**
   * 双曲函数 - 双曲正弦
   * @param {number} value - 要处理的值
   * @returns {number} 双曲正弦值
   */
  sinh(value) {
    return Math.sinh(value);
  },

  /**
   * 双曲函数 - 双曲余弦
   * @param {number} value - 要处理的值
   * @returns {number} 双曲余弦值
   */
  cosh(value) {
    return Math.cosh(value);
  },

  /**
   * 双曲函数 - 双曲正切
   * @param {number} value - 要处理的值
   * @returns {number} 双曲正切值
   */
  tanh(value) {
    return Math.tanh(value);
  },
};

// 导出模块 - CommonJS
module.exports = NumberUtils;