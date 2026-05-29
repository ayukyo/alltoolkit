/**
 * Currency Utilities 测试文件
 */

const assert = require('assert');
const {
  format,
  formatCompact,
  formatChinese,
  parse,
  extractCurrencyCode,
  convert,
  convertAndFormat,
  setRates,
  getRates,
  getCurrencyInfo,
  getSupportedCurrencies,
  getSymbol,
  isSupported,
  preciseAdd,
  preciseSubtract,
  preciseMultiply,
  preciseDivide,
  calculatePercent,
  calculateDiscount,
  calculateTax,
  split,
  simpleInterest,
  compoundInterest,
  toSmallestUnit,
  fromSmallestUnit,
} = require('./mod.js');

console.log('=== Currency Utils 测试开始 ===\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}: ${error.message}`);
    failed++;
  }
}

// ============ 精确计算测试 ============

test('preciseAdd - 精确加法', () => {
  assert.strictEqual(preciseAdd(0.1, 0.2), 0.3);
  assert.strictEqual(preciseAdd(0.1, 0.7), 0.8);
  assert.strictEqual(preciseAdd(1.005, 2.005, 3), 3.01);
});

test('preciseSubtract - 精确减法', () => {
  assert.strictEqual(preciseSubtract(0.3, 0.1), 0.2);
  assert.strictEqual(preciseSubtract(1.0, 0.9), 0.1);
});

test('preciseMultiply - 精确乘法', () => {
  assert.strictEqual(preciseMultiply(0.1, 0.2), 0.02);
  assert.strictEqual(preciseMultiply(3, 0.1), 0.3);
});

test('preciseDivide - 精确除法', () => {
  assert.strictEqual(preciseDivide(0.3, 3), 0.1);
  assert.strictEqual(preciseDivide(1, 3, 4), 0.3333);
});

test('toSmallestUnit - 转换为最小单位', () => {
  assert.strictEqual(toSmallestUnit(10.50, 'USD'), 1050);
  assert.strictEqual(toSmallestUnit(100, 'JPY'), 100); // 日元没有小数
});

test('fromSmallestUnit - 从最小单位转换', () => {
  assert.strictEqual(fromSmallestUnit(1050, 'USD'), 10.5);
  assert.strictEqual(fromSmallestUnit(100, 'JPY'), 100);
});

// ============ 格式化测试 ============

test('format - 基本格式化', () => {
  assert.strictEqual(format(1234.56, { currency: 'USD' }), '$1,234.56');
  assert.strictEqual(format(1234.56, { currency: 'CNY' }), '¥1,234.56');
  assert.strictEqual(format(1234.56, { currency: 'EUR' }), '€1,234.56');
});

test('format - 不显示符号', () => {
  assert.strictEqual(format(1234.56, { showSymbol: false }), '1,234.56');
});

test('format - 显示货币代码', () => {
  assert.strictEqual(format(1234.56, { currency: 'CNY', showCode: true }), '¥1,234.56 CNY');
});

test('format - 负数格式化', () => {
  assert.strictEqual(format(-1234.56, { currency: 'USD' }), '-$1,234.56');
});

test('format - 日元无小数', () => {
  assert.strictEqual(format(12345, { currency: 'JPY' }), '¥12,345');
});

test('formatCompact - 简写格式化', () => {
  assert.strictEqual(formatCompact(1500, { currency: 'USD' }), '$1.5K');
  assert.strictEqual(formatCompact(1500000, { currency: 'USD' }), '$1.5M');
  assert.strictEqual(formatCompact(1500000000, { currency: 'USD' }), '$1.5B');
});

test('formatChinese - 中文大写金额', () => {
  assert.strictEqual(formatChinese(0), '零元整');
  assert.strictEqual(formatChinese(100), '壹佰元整');
  assert.strictEqual(formatChinese(123.45), '壹佰贰拾叁元肆角伍分');
  assert.strictEqual(formatChinese(-100), '负壹佰元整');
});

// ============ 解析测试 ============

test('parse - 基本解析', () => {
  assert.strictEqual(parse('$1,234.56'), 1234.56);
  assert.strictEqual(parse('¥100'), 100);
  assert.strictEqual(parse('(500)'), -500);
});

test('parse - 欧洲格式', () => {
  assert.strictEqual(parse('1.234,56'), 1234.56);
});

test('extractCurrencyCode - 提取货币代码', () => {
  assert.strictEqual(extractCurrencyCode('Price: $100 USD'), 'USD');
  assert.strictEqual(extractCurrencyCode('费用: ¥100 CNY'), 'CNY');
  assert.strictEqual(extractCurrencyCode('100 EUR'), 'EUR');
});

// ============ 汇率转换测试 ============

test('convert - 货币转换', () => {
  // 使用默认汇率 USD=1, CNY=7.24
  const result = convert(100, 'USD', 'CNY');
  assert.ok(result > 700 && result < 800);
});

test('convertAndFormat - 转换并格式化', () => {
  const result = convertAndFormat(100, 'USD', 'CNY');
  assert.ok(result.includes('¥'));
});

test('setRates/getRates - 设置和获取汇率', () => {
  setRates({ EUR: 0.85, GBP: 0.75 }, 'USD');
  const rates = getRates();
  assert.strictEqual(rates.EUR, 0.85);
  assert.strictEqual(rates.GBP, 0.75);
  assert.strictEqual(rates.USD, 1);
});

test('convert - 相同货币转换', () => {
  assert.strictEqual(convert(100, 'USD', 'USD'), 100);
});

// ============ 货币信息测试 ============

test('getCurrencyInfo - 获取货币信息', () => {
  const info = getCurrencyInfo('CNY');
  assert.strictEqual(info.symbol, '¥');
  assert.strictEqual(info.name, 'Chinese Yuan');
  assert.strictEqual(info.decimalDigits, 2);
});

test('getSupportedCurrencies - 获取支持的货币', () => {
  const currencies = getSupportedCurrencies();
  assert.ok(currencies.includes('USD'));
  assert.ok(currencies.includes('CNY'));
  assert.ok(currencies.includes('EUR'));
  assert.ok(currencies.length >= 15);
});

test('getSymbol - 获取货币符号', () => {
  assert.strictEqual(getSymbol('USD'), '$');
  assert.strictEqual(getSymbol('CNY'), '¥');
  assert.strictEqual(getSymbol('EUR'), '€');
});

test('isSupported - 检查货币支持', () => {
  assert.strictEqual(isSupported('USD'), true);
  assert.strictEqual(isSupported('CNY'), true);
  assert.strictEqual(isSupported('XYZ'), false);
});

// ============ 计算测试 ============

test('calculatePercent - 计算百分比', () => {
  assert.strictEqual(calculatePercent(100, 10), 10);
  assert.strictEqual(calculatePercent(200, 15), 30);
});

test('calculateDiscount - 计算折扣', () => {
  const result = calculateDiscount(100, 20);
  assert.strictEqual(result.discounted, 80);
  assert.strictEqual(result.saved, 20);
});

test('calculateTax - 计算税费（不含税）', () => {
  const result = calculateTax(100, 10, false);
  assert.strictEqual(result.subtotal, 100);
  assert.strictEqual(result.tax, 10);
  assert.strictEqual(result.total, 110);
});

test('calculateTax - 计算税费（含税）', () => {
  const result = calculateTax(110, 10, true);
  assert.strictEqual(Math.round(result.subtotal), 100);
  assert.strictEqual(Math.round(result.tax), 10);
  assert.strictEqual(result.total, 110);
});

test('split - 分摊金额', () => {
  const shares = split(100, 3);
  const sum = shares.reduce((a, b) => a + b, 0);
  assert.strictEqual(sum, 100);
  assert.strictEqual(shares.length, 3);
  // 检查分摊是否公平（差值最多为0.02，考虑浮点精度）
  const max = Math.max(...shares);
  const min = Math.min(...shares);
  assert.ok(max - min <= 0.02);
});

test('simpleInterest - 简单利息', () => {
  const result = simpleInterest(1000, 5, 2);
  assert.strictEqual(result.interest, 100);
  assert.strictEqual(result.total, 1100);
});

test('compoundInterest - 复利', () => {
  const result = compoundInterest(1000, 5, 2, 12);
  assert.ok(result.interest > 100); // 复利利息大于单利
  assert.ok(result.total > 1100);
});

// ============ 输出结果 ============

console.log('\n=== 测试结果 ===');
console.log(`通过: ${passed}`);
console.log(`失败: ${failed}`);
console.log(`总计: ${passed + failed}`);

if (failed === 0) {
  console.log('\n✓ 所有测试通过！');
  process.exit(0);
} else {
  console.log('\n✗ 存在失败的测试');
  process.exit(1);
}