/**
 * Currency Utilities 使用示例
 */

const {
  format,
  formatCompact,
  formatChinese,
  parse,
  convert,
  convertAndFormat,
  setRates,
  getCurrencyInfo,
  getSupportedCurrencies,
  getSymbol,
  calculatePercent,
  calculateDiscount,
  calculateTax,
  split,
  simpleInterest,
  compoundInterest,
  preciseAdd,
  preciseSubtract,
  preciseMultiply,
  preciseDivide,
} = require('./mod.js');

console.log('=== Currency Utils 使用示例 ===\n');

// ============ 1. 基本格式化 ============
console.log('--- 1. 基本格式化 ---');
console.log('USD:', format(1234.56, { currency: 'USD' }));
console.log('CNY:', format(1234.56, { currency: 'CNY' }));
console.log('EUR:', format(1234.56, { currency: 'EUR' }));
console.log('JPY (无小数):', format(12345, { currency: 'JPY' }));
console.log('GBP:', format(1234.56, { currency: 'GBP' }));
console.log();

// ============ 2. 格式化选项 ============
console.log('--- 2. 格式化选项 ---');
console.log('不显示符号:', format(1234.56, { showSymbol: false }));
console.log('显示货币代码:', format(1234.56, { currency: 'CNY', showCode: true }));
console.log('自定义分隔符:', format(1234.56, { thousandsSeparator: '.', decimalSeparator: ',' }));
console.log('负数:', format(-1234.56, { currency: 'USD' }));
console.log();

// ============ 3. 简写格式 ============
console.log('--- 3. 简写格式 ---');
console.log('1.5K:', formatCompact(1500, { currency: 'USD' }));
console.log('1.5M:', formatCompact(1500000, { currency: 'USD' }));
console.log('1.5B:', formatCompact(1500000000, { currency: 'USD' }));
console.log('2.3T:', formatCompact(2300000000000, { currency: 'USD' }));
console.log();

// ============ 4. 中文大写金额 ============
console.log('--- 4. 中文大写金额 ---');
console.log('零元整:', formatChinese(0));
console.log('100元:', formatChinese(100));
console.log('123.45元:', formatChinese(123.45));
console.log('10000元:', formatChinese(10000));
console.log('负数:', formatChinese(-100));
console.log();

// ============ 5. 字符串解析 ============
console.log('--- 5. 字符串解析 ---');
console.log('"$1,234.56" ->', parse('$1,234.56'));
console.log('"¥100.50" ->', parse('¥100.50'));
console.log('"(500)" (负数) ->', parse('(500)'));
console.log('欧洲格式 "1.234,56" ->', parse('1.234,56'));
console.log();

// ============ 6. 货币转换 ============
console.log('--- 6. 货币转换 ---');
console.log('当前汇率:', getSupportedCurrencies().slice(0, 5).join(', '), '...');
console.log();
console.log('100 USD -> CNY:', convert(100, 'USD', 'CNY').toFixed(2), 'CNY');
console.log('100 USD -> EUR:', convert(100, 'USD', 'EUR').toFixed(2), 'EUR');
console.log('100 USD -> JPY:', convert(100, 'USD', 'JPY').toFixed(0), 'JPY');
console.log();

// 自定义汇率
console.log('--- 自定义汇率 ---');
setRates({ CNY: 7.20, EUR: 0.90, GBP: 0.78, JPY: 150 });
console.log('设置汇率后 100 USD -> CNY:', convert(100, 'USD', 'CNY').toFixed(2), 'CNY');
console.log();

// ============ 7. 转换并格式化 ============
console.log('--- 7. 转换并格式化 ---');
console.log('100 USD -> CNY:', convertAndFormat(100, 'USD', 'CNY'));
console.log('100 USD -> EUR:', convertAndFormat(100, 'USD', 'EUR'));
console.log('100 USD -> JPY:', convertAndFormat(100, 'USD', 'JPY'));
console.log();

// ============ 8. 货币信息 ============
console.log('--- 8. 货币信息 ---');
const cnyInfo = getCurrencyInfo('CNY');
console.log('CNY 信息:', cnyInfo);
console.log('USD 符号:', getSymbol('USD'));
console.log('支持的货币数量:', getSupportedCurrencies().length);
console.log();

// ============ 9. 百分比计算 ============
console.log('--- 9. 百分比计算 ---');
console.log('100 的 10%:', calculatePercent(100, 10));
console.log('1000 的 15%:', calculatePercent(1000, 15));
console.log();

// ============ 10. 折扣计算 ============
console.log('--- 10. 折扣计算 ---');
const discount = calculateDiscount(200, 25);
console.log('200 元打 75% 折扣:');
console.log('  折后价:', discount.discounted);
console.log('  节省:', discount.saved);
console.log();

// ============ 11. 税费计算 ============
console.log('--- 11. 税费计算 ---');
console.log('不含税计算:');
const tax1 = calculateTax(100, 10, false);
console.log('  税前:', tax1.subtotal);
console.log('  税额:', tax1.tax);
console.log('  税后:', tax1.total);

console.log('\n含税计算:');
const tax2 = calculateTax(110, 10, true);
console.log('  税前:', tax2.subtotal.toFixed(2));
console.log('  税额:', tax2.tax.toFixed(2));
console.log('  税后:', tax2.total);
console.log();

// ============ 12. 金额分摊 ============
console.log('--- 12. 金额分摊 ---');
console.log('100 元分 3 人:', split(100, 3));
console.log('100 元分 6 人:', split(100, 6));
console.log();

// ============ 13. 利息计算 ============
console.log('--- 13. 利息计算 ---');
console.log('简单利息:');
const simple = simpleInterest(10000, 5, 3);
console.log('  本金: 10000, 年利率: 5%, 期限: 3年');
console.log('  利息:', simple.interest);
console.log('  本息合计:', simple.total);

console.log('\n复利:');
const compound = compoundInterest(10000, 5, 3, 12);
console.log('  本金: 10000, 年利率: 5%, 期限: 3年, 月复利');
console.log('  利息:', compound.interest);
console.log('  本息合计:', compound.total);
console.log();

// ============ 14. 精确计算 ============
console.log('--- 14. 精确计算 ---');
console.log('0.1 + 0.2 =', preciseAdd(0.1, 0.2), '(原生 JS:', 0.1 + 0.2, ')');
console.log('0.3 - 0.1 =', preciseSubtract(0.3, 0.1), '(原生 JS:', 0.3 - 0.1, ')');
console.log('0.1 * 0.2 =', preciseMultiply(0.1, 0.2), '(原生 JS:', 0.1 * 0.2, ')');
console.log();

// ============ 15. 实际应用场景 ============
console.log('--- 15. 实际应用场景 ---');

// 购物车计算
console.log('购物车计算:');
const items = [
  { name: '商品A', price: 99.99, qty: 2 },
  { name: '商品B', price: 149.50, qty: 1 },
  { name: '商品C', price: 29.99, qty: 3 },
];
let subtotal = 0;
items.forEach(item => {
  const itemTotal = preciseMultiply(item.price, item.qty);
  subtotal = preciseAdd(subtotal, itemTotal);
  console.log(`  ${item.name}: ${format(item.price)} × ${item.qty} = ${format(itemTotal)}`);
});
const tax = calculateTax(subtotal, 8);
console.log(`  小计: ${format(subtotal)}`);
console.log(`  税费(8%): ${format(tax.tax)}`);
console.log(`  总计: ${format(tax.total)}`);
console.log();

// 工资计算
console.log('工资分摊:');
const salary = 15000;
const shares = split(salary, 4, 2);
const categories = ['房租', '生活费', '储蓄', '投资'];
categories.forEach((cat, i) => {
  console.log(`  ${cat}: ${format(shares[i])}`);
});
console.log();

console.log('=== 示例结束 ===');