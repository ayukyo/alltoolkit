/**
 * Currency Utilities - 零依赖货币工具库
 * 
 * 功能：
 * - 货币格式化（支持国际化）
 * - 货币解析
 * - 汇率转换（基于预设汇率）
 * - 货币计算（精确运算避免浮点误差）
 * - 货币符号获取
 * - 常用货币信息
 */

// ============ 常用货币数据 ============

/**
 * 常用货币信息
 */
const CURRENCIES = {
  CNY: { symbol: '¥', name: 'Chinese Yuan', decimalDigits: 2, symbolPosition: 'before' },
  USD: { symbol: '$', name: 'US Dollar', decimalDigits: 2, symbolPosition: 'before' },
  EUR: { symbol: '€', name: 'Euro', decimalDigits: 2, symbolPosition: 'before' },
  GBP: { symbol: '£', name: 'British Pound', decimalDigits: 2, symbolPosition: 'before' },
  JPY: { symbol: '¥', name: 'Japanese Yen', decimalDigits: 0, symbolPosition: 'before' },
  KRW: { symbol: '₩', name: 'South Korean Won', decimalDigits: 0, symbolPosition: 'before' },
  HKD: { symbol: 'HK$', name: 'Hong Kong Dollar', decimalDigits: 2, symbolPosition: 'before' },
  TWD: { symbol: 'NT$', name: 'New Taiwan Dollar', decimalDigits: 2, symbolPosition: 'before' },
  SGD: { symbol: 'S$', name: 'Singapore Dollar', decimalDigits: 2, symbolPosition: 'before' },
  AUD: { symbol: 'A$', name: 'Australian Dollar', decimalDigits: 2, symbolPosition: 'before' },
  CAD: { symbol: 'C$', name: 'Canadian Dollar', decimalDigits: 2, symbolPosition: 'before' },
  CHF: { symbol: 'Fr', name: 'Swiss Franc', decimalDigits: 2, symbolPosition: 'before' },
  INR: { symbol: '₹', name: 'Indian Rupee', decimalDigits: 2, symbolPosition: 'before' },
  RUB: { symbol: '₽', name: 'Russian Ruble', decimalDigits: 2, symbolPosition: 'after' },
  BRL: { symbol: 'R$', name: 'Brazilian Real', decimalDigits: 2, symbolPosition: 'before' },
  THB: { symbol: '฿', name: 'Thai Baht', decimalDigits: 2, symbolPosition: 'before' },
  VND: { symbol: '₫', name: 'Vietnamese Dong', decimalDigits: 0, symbolPosition: 'after' },
  PHP: { symbol: '₱', name: 'Philippine Peso', decimalDigits: 2, symbolPosition: 'before' },
  MYR: { symbol: 'RM', name: 'Malaysian Ringgit', decimalDigits: 2, symbolPosition: 'before' },
  IDR: { symbol: 'Rp', name: 'Indonesian Rupiah', decimalDigits: 0, symbolPosition: 'before' },
};

// 默认汇率（相对于USD，仅作示例，实际应从API获取）
const DEFAULT_RATES = {
  USD: 1,
  CNY: 7.24,
  EUR: 0.92,
  GBP: 0.79,
  JPY: 154.50,
  KRW: 1360,
  HKD: 7.82,
  TWD: 32.10,
  SGD: 1.35,
  AUD: 1.53,
  CAD: 1.36,
  CHF: 0.90,
  INR: 83.12,
  RUB: 89.50,
  BRL: 5.05,
  THB: 36.20,
  VND: 25400,
  PHP: 58.50,
  MYR: 4.72,
  IDR: 16200,
};

// ============ 精确计算工具 ============

/**
 * 将金额转换为整数（以最小单位计）避免浮点误差
 * @param {number} amount - 金额
 * @param {string} currency - 货币代码
 * @returns {number} 整数表示
 */
function toSmallestUnit(amount, currency = 'USD') {
  const decimals = CURRENCIES[currency]?.decimalDigits ?? 2;
  const multiplier = Math.pow(10, decimals);
  return Math.round(amount * multiplier);
}

/**
 * 从最小单位转换回金额
 * @param {number} smallestUnit - 最小单位整数
 * @param {string} currency - 货币代码
 * @returns {number} 金额
 */
function fromSmallestUnit(smallestUnit, currency = 'USD') {
  const decimals = CURRENCIES[currency]?.decimalDigits ?? 2;
  const divisor = Math.pow(10, decimals);
  return smallestUnit / divisor;
}

/**
 * 精确加法
 * @param {number} a - 第一个数
 * @param {number} b - 第二个数
 * @param {number} decimals - 小数位数
 * @returns {number} 精确结果
 */
function preciseAdd(a, b, decimals = 2) {
  const multiplier = Math.pow(10, decimals);
  return Math.round(a * multiplier + b * multiplier) / multiplier;
}

/**
 * 精确减法
 * @param {number} a - 被减数
 * @param {number} b - 减数
 * @param {number} decimals - 小数位数
 * @returns {number} 精确结果
 */
function preciseSubtract(a, b, decimals = 2) {
  const multiplier = Math.pow(10, decimals);
  return Math.round(a * multiplier - b * multiplier) / multiplier;
}

/**
 * 精确乘法
 * @param {number} a - 第一个数
 * @param {number} b - 第二个数
 * @param {number} decimals - 小数位数
 * @returns {number} 精确结果
 */
function preciseMultiply(a, b, decimals = 2) {
  const multiplier = Math.pow(10, decimals);
  return Math.round(a * multiplier * b) / multiplier;
}

/**
 * 精确除法
 * @param {number} a - 被除数
 * @param {number} b - 除数
 * @param {number} decimals - 小数位数
 * @returns {number} 精确结果
 */
function preciseDivide(a, b, decimals = 2) {
  const multiplier = Math.pow(10, decimals);
  return Math.round((a / b) * multiplier) / multiplier;
}

// ============ 格式化工具 ============

/**
 * 格式化货币金额
 * @param {number} amount - 金额
 * @param {Object} options - 选项
 * @param {string} options.currency - 货币代码 (默认 'USD')
 * @param {boolean} options.showSymbol - 是否显示货币符号 (默认 true)
 * @param {boolean} options.showCode - 是否显示货币代码 (默认 false)
 * @param {string} options.thousandsSeparator - 千分位分隔符 (默认 ',')
 * @param {string} options.decimalSeparator - 小数分隔符 (默认 '.')
 * @param {number} options.decimals - 小数位数 (默认按货币设置)
 * @returns {string} 格式化后的字符串
 */
function format(amount, options = {}) {
  const {
    currency = 'USD',
    showSymbol = true,
    showCode = false,
    thousandsSeparator = ',',
    decimalSeparator = '.',
    decimals,
  } = options;

  const currencyInfo = CURRENCIES[currency] || { 
    symbol: currency, 
    decimalDigits: 2, 
    symbolPosition: 'before' 
  };
  
  const decimalDigits = decimals ?? currencyInfo.decimalDigits;
  const fixedAmount = Math.abs(amount).toFixed(decimalDigits);
  const [integerPart, decimalPart] = fixedAmount.split('.');
  
  // 添加千分位分隔符
  const formattedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, thousandsSeparator);
  
  let result = decimalPart 
    ? `${formattedInteger}${decimalSeparator}${decimalPart}`
    : formattedInteger;
  
  // 添加货币符号
  if (showSymbol && currencyInfo.symbol) {
    result = currencyInfo.symbolPosition === 'after'
      ? `${result} ${currencyInfo.symbol}`
      : `${currencyInfo.symbol}${result}`;
  }
  
  // 添加货币代码
  if (showCode) {
    result = `${result} ${currency}`;
  }
  
  // 处理负数
  if (amount < 0) {
    result = showSymbol && currencyInfo.symbolPosition === 'before'
      ? `-${result}`
      : `(${result})`;
  }
  
  return result.trim();
}

/**
 * 格式化为简写形式（K, M, B, T）
 * @param {number} amount - 金额
 * @param {Object} options - 选项
 * @returns {string} 简写形式
 */
function formatCompact(amount, options = {}) {
  const { currency = 'USD', showSymbol = true, decimals = 1 } = options;
  const absAmount = Math.abs(amount);
  const symbol = showSymbol ? (CURRENCIES[currency]?.symbol || currency) : '';
  
  let result;
  if (absAmount >= 1e12) {
    result = `${(absAmount / 1e12).toFixed(decimals)}T`;
  } else if (absAmount >= 1e9) {
    result = `${(absAmount / 1e9).toFixed(decimals)}B`;
  } else if (absAmount >= 1e6) {
    result = `${(absAmount / 1e6).toFixed(decimals)}M`;
  } else if (absAmount >= 1e3) {
    result = `${(absAmount / 1e3).toFixed(decimals)}K`;
  } else {
    result = absAmount.toFixed(decimals);
  }
  
  const prefix = amount < 0 ? '-' : '';
  return showSymbol ? `${prefix}${symbol}${result}` : `${prefix}${result}`;
}

/**
 * 格式化为中文大写金额
 * @param {number} amount - 金额
 * @returns {string} 中文大写金额
 */
function formatChinese(amount) {
  if (amount === 0) return '零元整';
  
  const digits = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖'];
  const units = ['', '拾', '佰', '仟'];
  const bigUnits = ['', '万', '亿', '兆'];
  const decimalUnits = ['角', '分'];
  
  const isNegative = amount < 0;
  amount = Math.abs(amount);
  
  // 分离整数和小数部分
  const integerPart = Math.floor(amount);
  const decimalPart = Math.round((amount - integerPart) * 100);
  
  let result = '';
  
  // 处理整数部分
  if (integerPart > 0) {
    const groups = [];
    let temp = integerPart;
    while (temp > 0) {
      groups.push(temp % 10000);
      temp = Math.floor(temp / 10000);
    }
    
    groups.forEach((group, groupIndex) => {
      if (group === 0) return;
      
      let groupStr = '';
      let hasZero = false;
      
      for (let i = 0; i < 4; i++) {
        const digit = Math.floor(group / Math.pow(10, i)) % 10;
        if (digit === 0) {
          hasZero = true;
        } else {
          if (hasZero && groupStr) {
            groupStr = '零' + groupStr;
          }
          hasZero = false;
          groupStr = digits[digit] + units[i] + groupStr;
        }
      }
      
      result = groupStr + bigUnits[groupIndex] + result;
    });
    
    result += '元';
  }
  
  // 处理小数部分
  if (decimalPart > 0) {
    const jiao = Math.floor(decimalPart / 10);
    const fen = decimalPart % 10;
    
    if (jiao > 0) {
      result += digits[jiao] + decimalUnits[0];
    }
    if (fen > 0) {
      result += digits[fen] + decimalUnits[1];
    }
  } else if (integerPart > 0) {
    result += '整';
  }
  
  return (isNegative ? '负' : '') + result;
}

// ============ 解析工具 ============

/**
 * 解析货币字符串为数字
 * @param {string} currencyString - 货币字符串
 * @param {Object} options - 选项
 * @returns {number} 金额数值
 */
function parse(currencyString, options = {}) {
  const { currency = 'USD' } = options;
  
  // 移除货币符号和代码
  let cleaned = currencyString
    .replace(/[^\d.,\-()]/g, '') // 保留数字、逗号、点、负号、括号
    .replace(/\(/g, '-')
    .replace(/\)/g, '');
  
  // 处理不同的数字格式
  // 欧洲格式: 1.234,56 (点作为千分位，逗号作为小数点)
  // 英美格式: 1,234.56 (逗号作为千分位，点作为小数点)
  
  const lastComma = cleaned.lastIndexOf(',');
  const lastDot = cleaned.lastIndexOf('.');
  
  // 判断格式
  if (lastComma > lastDot) {
    // 欧洲格式：逗号是小数点
    cleaned = cleaned.replace(/\./g, '').replace(',', '.');
  } else {
    // 英美格式：点是小数点
    cleaned = cleaned.replace(/,/g, '');
  }
  
  const result = parseFloat(cleaned);
  return isNaN(result) ? 0 : result;
}

/**
 * 尝试从字符串中提取货币代码
 * @param {string} str - 输入字符串
 * @returns {string|null} 货币代码或 null
 */
function extractCurrencyCode(str) {
  const upperStr = str.toUpperCase();
  for (const code of Object.keys(CURRENCIES)) {
    if (upperStr.includes(code)) {
      return code;
    }
  }
  return null;
}

// ============ 汇率转换 ============

let currentRates = { ...DEFAULT_RATES };

/**
 * 设置汇率
 * @param {Object} rates - 汇率对象 { CNY: 7.24, EUR: 0.92, ... }
 * @param {string} baseCurrency - 基准货币（默认 USD）
 */
function setRates(rates, baseCurrency = 'USD') {
  currentRates = { [baseCurrency]: 1, ...rates };
}

/**
 * 获取当前汇率
 * @returns {Object} 汇率对象
 */
function getRates() {
  return { ...currentRates };
}

/**
 * 货币转换
 * @param {number} amount - 金额
 * @param {string} from - 源货币代码
 * @param {string} to - 目标货币代码
 * @param {number} decimals - 结果小数位数
 * @returns {number} 转换后的金额
 */
function convert(amount, from, to, decimals) {
  if (from === to) return amount;
  
  const fromRate = currentRates[from];
  const toRate = currentRates[to];
  
  if (!fromRate || !toRate) {
    throw new Error(`Unsupported currency: ${!fromRate ? from : to}`);
  }
  
  // 先转换为基准货币，再转换为目标货币
  const baseAmount = amount / fromRate;
  const result = baseAmount * toRate;
  
  const decimalDigits = decimals ?? (CURRENCIES[to]?.decimalDigits ?? 2);
  return parseFloat(result.toFixed(decimalDigits));
}

/**
 * 转换并格式化
 * @param {number} amount - 金额
 * @param {string} from - 源货币代码
 * @param {string} to - 目标货币代码
 * @param {Object} formatOptions - 格式化选项
 * @returns {string} 格式化后的转换结果
 */
function convertAndFormat(amount, from, to, formatOptions = {}) {
  const converted = convert(amount, from, to);
  return format(converted, { currency: to, ...formatOptions });
}

// ============ 货币信息 ============

/**
 * 获取货币信息
 * @param {string} code - 货币代码
 * @returns {Object|null} 货币信息
 */
function getCurrencyInfo(code) {
  return CURRENCIES[code] ? { code, ...CURRENCIES[code] } : null;
}

/**
 * 获取所有支持的货币
 * @returns {Array} 货币代码数组
 */
function getSupportedCurrencies() {
  return Object.keys(CURRENCIES);
}

/**
 * 获取货币符号
 * @param {string} code - 货币代码
 * @returns {string} 货币符号
 */
function getSymbol(code) {
  return CURRENCIES[code]?.symbol || code;
}

/**
 * 检查货币是否支持
 * @param {string} code - 货币代码
 * @returns {boolean}
 */
function isSupported(code) {
  return code in CURRENCIES;
}

// ============ 货币计算 ============

/**
 * 计算百分比
 * @param {number} amount - 金额
 * @param {number} percent - 百分比
 * @param {number} decimals - 小数位数
 * @returns {number} 计算结果
 */
function calculatePercent(amount, percent, decimals = 2) {
  return preciseMultiply(amount, percent / 100, decimals);
}

/**
 * 计算折扣
 * @param {number} amount - 原价
 * @param {number} discountPercent - 折扣百分比
 * @param {number} decimals - 小数位数
 * @returns {Object} { discounted: 折后价, saved: 节省金额 }
 */
function calculateDiscount(amount, discountPercent, decimals = 2) {
  const saved = calculatePercent(amount, discountPercent, decimals);
  const discounted = preciseSubtract(amount, saved, decimals);
  return { discounted, saved };
}

/**
 * 计算税费
 * @param {number} amount - 金额
 * @param {number} taxRate - 税率百分比
 * @param {boolean} inclusive - 是否含税
 * @param {number} decimals - 小数位数
 * @returns {Object} { subtotal: 税前金额, tax: 税额, total: 税后金额 }
 */
function calculateTax(amount, taxRate, inclusive = false, decimals = 2) {
  if (inclusive) {
    const subtotal = preciseDivide(amount, 1 + taxRate / 100, decimals);
    const tax = preciseSubtract(amount, subtotal, decimals);
    return { subtotal, tax, total: amount };
  } else {
    const tax = calculatePercent(amount, taxRate, decimals);
    const total = preciseAdd(amount, tax, decimals);
    return { subtotal: amount, tax, total };
  }
}

/**
 * 分摊金额
 * @param {number} amount - 总金额
 * @param {number} parts - 分成几份
 * @param {number} decimals - 小数位数
 * @returns {Array<number>} 分摊后的金额数组
 */
function split(amount, parts, decimals = 2) {
  const multiplier = Math.pow(10, decimals);
  const total = Math.round(amount * multiplier);
  const baseShare = Math.floor(total / parts);
  const remainder = total % parts;
  
  const shares = Array(parts).fill(baseShare);
  for (let i = 0; i < remainder; i++) {
    shares[i]++;
  }
  
  return shares.map(share => share / multiplier);
}

/**
 * 计算简单利息
 * @param {number} principal - 本金
 * @param {number} rate - 年利率百分比
 * @param {number} years - 年数
 * @returns {Object} { interest: 利息, total: 本息合计 }
 */
function simpleInterest(principal, rate, years) {
  const interest = preciseMultiply(principal, rate / 100 * years, 2);
  const total = preciseAdd(principal, interest, 2);
  return { interest, total };
}

/**
 * 计算复利
 * @param {number} principal - 本金
 * @param {number} rate - 年利率百分比
 * @param {number} years - 年数
 * @param {number} compoundsPerYear - 每年复利次数 (默认12)
 * @returns {Object} { interest: 利息, total: 本息合计 }
 */
function compoundInterest(principal, rate, years, compoundsPerYear = 12) {
  const r = rate / 100;
  const total = principal * Math.pow(1 + r / compoundsPerYear, compoundsPerYear * years);
  const interest = preciseSubtract(total, principal, 2);
  return { interest, total: parseFloat(total.toFixed(2)) };
}

// ============ 导出 ============

module.exports = {
  // 常量
  CURRENCIES,
  DEFAULT_RATES,
  
  // 精确计算
  toSmallestUnit,
  fromSmallestUnit,
  preciseAdd,
  preciseSubtract,
  preciseMultiply,
  preciseDivide,
  
  // 格式化
  format,
  formatCompact,
  formatChinese,
  
  // 解析
  parse,
  extractCurrencyCode,
  
  // 汇率转换
  setRates,
  getRates,
  convert,
  convertAndFormat,
  
  // 货币信息
  getCurrencyInfo,
  getSupportedCurrencies,
  getSymbol,
  isSupported,
  
  // 计算
  calculatePercent,
  calculateDiscount,
  calculateTax,
  split,
  simpleInterest,
  compoundInterest,
};