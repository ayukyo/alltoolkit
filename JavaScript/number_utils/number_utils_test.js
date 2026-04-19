/**
 * Number Utilities Test Suite
 * 数字工具模块测试套件
 * 
 * 运行方式: node number_utils_test.js
 * 
 * @module number_utils_test
 */

const NumberUtils = require('./mod.js');

// 测试统计
let passed = 0;
let failed = 0;
const failures = [];

/**
 * 断言函数
 * @param {boolean} condition - 条件
 * @param {string} message - 测试信息
 */
function assert(condition, message) {
  if (condition) {
    passed++;
    console.log(`✓ ${message}`);
  } else {
    failed++;
    failures.push(message);
    console.log(`✗ ${message}`);
  }
}

/**
 * 断言近似相等
 * @param {number} actual - 实际值
 * @param {number} expected - 预期值
 * @param {string} message - 测试信息
 * @param {number} [epsilon=0.0001] - 容差
 */
function assertApprox(actual, expected, message, epsilon = 0.0001) {
  assert(Math.abs(actual - expected) < epsilon, message);
}

/**
 * 断言数组相等
 * @param {Array} actual - 实际数组
 * @param {Array} expected - 预期数组
 * @param {string} message - 测试信息
 */
function assertArray(actual, expected, message) {
  const equal = actual.length === expected.length && 
                actual.every((v, i) => v === expected[i]);
  assert(equal, message);
}

console.log('\n========================================');
console.log('  Number Utilities Test Suite');
console.log('========================================\n');

// ==================== 类型判断测试 ====================
console.log('📋 类型判断测试');
console.log('----------------------------------------');

assert(NumberUtils.isNumber(42), 'isNumber(42) 应返回 true');
assert(NumberUtils.isNumber(3.14), 'isNumber(3.14) 应返回 true');
assert(!NumberUtils.isNumber('42'), 'isNumber("42") 应返回 false');
assert(!NumberUtils.isNumber(NaN), 'isNumber(NaN) 应返回 false');
assert(!NumberUtils.isNumber(undefined), 'isNumber(undefined) 应返回 false');

assert(NumberUtils.isInteger(42), 'isInteger(42) 应返回 true');
assert(!NumberUtils.isInteger(3.14), 'isInteger(3.14) 应返回 false');
assert(!NumberUtils.isInteger('42'), 'isInteger("42") 应返回 false');

assert(NumberUtils.isFloat(3.14), 'isFloat(3.14) 应返回 true');
assert(!NumberUtils.isFloat(42), 'isFloat(42) 应返回 false');

assert(NumberUtils.isSafeInteger(Number.MAX_SAFE_INTEGER), 'isSafeInteger(MAX_SAFE_INTEGER) 应返回 true');
assert(!NumberUtils.isSafeInteger(Number.MAX_SAFE_INTEGER + 1), 'isSafeInteger(MAX_SAFE_INTEGER + 1) 应返回 false');

assert(NumberUtils.isPositive(42), 'isPositive(42) 应返回 true');
assert(!NumberUtils.isPositive(-1), 'isPositive(-1) 应返回 false');
assert(!NumberUtils.isPositive(0), 'isPositive(0) 应返回 false');

assert(NumberUtils.isNegative(-1), 'isNegative(-1) 应返回 true');
assert(!NumberUtils.isNegative(42), 'isNegative(42) 应返回 false');

assert(NumberUtils.isZero(0), 'isZero(0) 应返回 true');
assert(NumberUtils.isZero(0, 0.001), 'isZero(0, 0.001) 应返回 true');
assert(NumberUtils.isZero(0.0000001, 0.000001), 'isZero(0.0000001, 0.000001) 在容差内应返回 true');

assert(NumberUtils.isEven(42), 'isEven(42) 应返回 true');
assert(!NumberUtils.isEven(43), 'isEven(43) 应返回 false');

assert(NumberUtils.isOdd(43), 'isOdd(43) 应返回 true');
assert(!NumberUtils.isOdd(42), 'isOdd(42) 应返回 false');

// 质数测试
assert(NumberUtils.isPrime(2), 'isPrime(2) 应返回 true');
assert(NumberUtils.isPrime(7), 'isPrime(7) 应返回 true');
assert(NumberUtils.isPrime(11), 'isPrime(11) 应返回 true');
assert(!NumberUtils.isPrime(4), 'isPrime(4) 应返回 false');
assert(!NumberUtils.isPrime(1), 'isPrime(1) 应返回 false');
assert(!NumberUtils.isPrime(0), 'isPrime(0) 应返回 false');

// 完全平方数测试
assert(NumberUtils.isPerfectSquare(4), 'isPerfectSquare(4) 应返回 true');
assert(NumberUtils.isPerfectSquare(16), 'isPerfectSquare(16) 应返回 true');
assert(!NumberUtils.isPerfectSquare(5), 'isPerfectSquare(5) 应返回 false');

// 完全立方数测试
assert(NumberUtils.isPerfectCube(8), 'isPerfectCube(8) 应返回 true');
assert(NumberUtils.isPerfectCube(27), 'isPerfectCube(27) 应返回 true');
assert(!NumberUtils.isPerfectCube(9), 'isPerfectCube(9) 应返回 false');

// 斐波那契数测试
assert(NumberUtils.isFibonacci(0), 'isFibonacci(0) 应返回 true');
assert(NumberUtils.isFibonacci(1), 'isFibonacci(1) 应返回 true');
assert(NumberUtils.isFibonacci(5), 'isFibonacci(5) 应返回 true');
assert(NumberUtils.isFibonacci(8), 'isFibonacci(8) 应返回 true');
assert(!NumberUtils.isFibonacci(4), 'isFibonacci(4) 应返回 false');

// 范围测试
assert(NumberUtils.inRange(5, 1, 10), 'inRange(5, 1, 10) 应返回 true');
assert(NumberUtils.inRange(1, 1, 10), 'inRange(1, 1, 10) 包含边界应返回 true');
assert(!NumberUtils.inRange(1, 1, 10, false), 'inRange(1, 1, 10, false) 不包含边界应返回 false');
assert(!NumberUtils.inRange(11, 1, 10), 'inRange(11, 1, 10) 应返回 false');

// 类型获取测试
assert(NumberUtils.getType(42) === 'safe_integer', 'getType(42) 应返回 safe_integer');
assert(NumberUtils.getType(3.14) === 'float', 'getType(3.14) 应返回 float');
assert(NumberUtils.getType(NaN) === 'nan', 'getType(NaN) 应返回 nan');
assert(NumberUtils.getType(Infinity) === 'infinity', 'getType(Infinity) 应返回 infinity');

// ==================== 解析与转换测试 ====================
console.log('\n📋 解析与转换测试');
console.log('----------------------------------------');

assert(NumberUtils.parse('42') === 42, 'parse("42") 应返回 42');
assert(NumberUtils.parse('3.14') === 3.14, 'parse("3.14") 应返回 3.14');
assert(NumberUtils.parse('abc', 0) === 0, 'parse("abc", 0) 应返回默认值 0');
assert(NumberUtils.parse(null, 10) === 10, 'parse(null, 10) 应返回默认值 10');

assert(NumberUtils.parseInt('42') === 42, 'parseInt("42") 应返回 42');
assert(NumberUtils.parseInt('3.14') === 3, 'parseInt("3.14") 应返回 3');
assert(NumberUtils.parseInt('101', 0, 2) === 5, 'parseInt("101", 0, 2) 二进制应返回 5');

assert(NumberUtils.parseFloat('3.14') === 3.14, 'parseFloat("3.14") 应返回 3.14');
assert(NumberUtils.parseFloat('42abc', 0) === 42, 'parseFloat("42abc") 应返回 42');

assert(NumberUtils.fromString('1,234.56') === 1234.56, 'fromString("1,234.56") 应返回 1234.56');
assert(NumberUtils.fromString(' 42 ') === 42, 'fromString(" 42 ") 应返回 42');

// 进制转换测试
assert(NumberUtils.fromBinary('1010') === 10, 'fromBinary("1010") 应返回 10');
assert(NumberUtils.fromHex('FF') === 255, 'fromHex("FF") 应返回 255');
assert(NumberUtils.fromHex('0xFF') === 255, 'fromHex("0xFF") 应返回 255');
assert(NumberUtils.fromOctal('77') === 63, 'fromOctal("77") 应返回 63');

assert(NumberUtils.toBinary(10) === '1010', 'toBinary(10) 应返回 "1010"');
assert(NumberUtils.toHex(255) === '0xff', 'toHex(255) 应返回 "0xff"');
assert(NumberUtils.toHex(255, false) === 'ff', 'toHex(255, false) 应返回 "ff"');
assert(NumberUtils.toOctal(63) === '0o77', 'toOctal(63) 应返回 "0o77"');

// ==================== 格式化测试 ====================
console.log('\n📋 格式化测试');
console.log('----------------------------------------');

assert(NumberUtils.format(1234567.89, 2) === '1,234,567.89', 'format(1234567.89, 2) 应返回 "1,234,567.89"');
assert(NumberUtils.format(1234, 0) === '1,234', 'format(1234, 0) 应返回 "1,234"');
assert(NumberUtils.format(1234.56, 2, '.', ',') === '1.234,56', 'format(1234.56, 2, ".", ",") 应返回 "1.234,56"');

assert(NumberUtils.formatCurrency(1234.56, '¥', 2) === '¥1,234.56', 'formatCurrency(1234.56) 应返回 "¥1,234.56"');
assert(NumberUtils.formatCurrency(1234.56, '$', 2) === '$1,234.56', 'formatCurrency(1234.56, "$") 应返回 "$1,234.56"');

assert(NumberUtils.formatPercent(0.1234, 2) === '12.34%', 'formatPercent(0.1234, 2) 应返回 "12.34%"');
assert(NumberUtils.formatPercent(12.34, 2, true) === '12.34%', 'formatPercent(12.34, 2, true) 应返回 "12.34%"');

assert(NumberUtils.formatScientific(1234.56, 2) === '1.23e+3', 'formatScientific(1234.56, 2) 应返回 "1.23e+3"');

// 文件大小格式化测试
assert(NumberUtils.formatFileSize(0) === '0 B', 'formatFileSize(0) 应返回 "0 B"');
assert(NumberUtils.formatFileSize(1000) === '1.00 KB', 'formatFileSize(1000) 应返回 "1.00 KB"');
assert(NumberUtils.formatFileSize(1000000) === '1.00 MB', 'formatFileSize(1000000) 应返回 "1.00 MB"');
assert(NumberUtils.formatFileSize(1000000000) === '1.00 GB', 'formatFileSize(1000000000) 应返回 "1.00 GB"');
// 使用二进制单位（1024进制）
assert(NumberUtils.formatFileSize(1024, 2, false) === '1.00 KiB', 'formatFileSize(1024, 2, false) 应返回 "1.00 KiB"');
assert(NumberUtils.formatFileSize(1048576, 2, false) === '1.00 MiB', 'formatFileSize(1048576, 2, false) 应返回 "1.00 MiB"');

// 持续时间格式化测试
assert(NumberUtils.formatDuration(500) === '500ms', 'formatDuration(500) 应返回 "500ms"');
assert(NumberUtils.formatDuration(5000) === '5.00 seconds', 'formatDuration(5000) 应返回 "5.00 seconds"');
assert(NumberUtils.formatDuration(5000, { compact: true }) === '5s', 'formatDuration(5000, compact) 应返回 "5s"');
assert(NumberUtils.formatDuration(90000) === '1 minute 30 seconds', 'formatDuration(90000) 应返回 "1 minute 30 seconds"');

// 中文数字测试
assert(NumberUtils.formatChinese(0) === '零', 'formatChinese(0) 应返回 "零"');
assert(NumberUtils.formatChinese(1) === '一', 'formatChinese(1) 应返回 "一"');
assert(NumberUtils.formatChinese(10) === '十', 'formatChinese(10) 应返回 "十"');
assert(NumberUtils.formatChinese(15) === '十五', 'formatChinese(15) 应返回 "十五"');
assert(NumberUtils.formatChinese(100) === '一百', 'formatChinese(100) 应返回 "一百"');
assert(NumberUtils.formatChinese(123) === '一百二十三', 'formatChinese(123) 应返回 "一百二十三"');
assert(NumberUtils.formatChinese(10000) === '一万', 'formatChinese(10000) 应返回 "一万"');

// ==================== 数学运算测试 ====================
console.log('\n📋 数学运算测试');
console.log('----------------------------------------');

// 精度运算测试
assert(NumberUtils.add(0.1, 0.2) === 0.3, 'add(0.1, 0.2) 应返回 0.3');
assert(NumberUtils.add(0.7, 0.1) === 0.8, 'add(0.7, 0.1) 应返回 0.8');
assert(NumberUtils.subtract(0.3, 0.1) === 0.2, 'subtract(0.3, 0.1) 应返回 0.2');
assertApprox(NumberUtils.multiply(0.1, 0.2), 0.02, 'multiply(0.1, 0.2) 应返回约 0.02');
assertApprox(NumberUtils.divide(0.3, 0.1), 3, 'divide(0.3, 0.1) 应返回约 3');

assert(NumberUtils.modulo(-5, 3) === 1, 'modulo(-5, 3) 应返回 1');
assert(NumberUtils.modulo(5, 3) === 2, 'modulo(5, 3) 应返回 2');

assert(NumberUtils.percentage(25, 100) === 25, 'percentage(25, 100) 应返回 25');
assert(NumberUtils.growthRate(100, 150) === 50, 'growthRate(100, 150) 应返回 50');
assert(NumberUtils.growthRate(100, 50) === -50, 'growthRate(100, 50) 应返回 -50');

// 统计函数测试
assert(NumberUtils.average([1, 2, 3, 4, 5]) === 3, 'average([1,2,3,4,5]) 应返回 3');
assert(NumberUtils.median([1, 2, 3, 4, 5]) === 3, 'median([1,2,3,4,5]) 应返回 3');
assert(NumberUtils.median([1, 2, 3, 4]) === 2.5, 'median([1,2,3,4]) 应返回 2.5');

assertArray(NumberUtils.mode([1, 2, 2, 3, 3, 3]), [3], 'mode([1,2,2,3,3,3]) 应返回 [3]');
assertArray(NumberUtils.mode([1, 1, 2, 2]), [1, 2], 'mode([1,1,2,2]) 应返回 [1, 2]');

assertApprox(NumberUtils.standardDeviation([2, 4, 4, 4, 5, 5, 7, 9]), 2, 'standardDeviation 应返回约 2', 0.1);

// ==================== 范围操作测试 ====================
console.log('\n📋 范围操作测试');
console.log('----------------------------------------');

assert(NumberUtils.clamp(5, 1, 10) === 5, 'clamp(5, 1, 10) 应返回 5');
assert(NumberUtils.clamp(0, 1, 10) === 1, 'clamp(0, 1, 10) 应返回 1');
assert(NumberUtils.clamp(15, 1, 10) === 10, 'clamp(15, 1, 10) 应返回 10');

assertApprox(NumberUtils.mapRange(5, 0, 10, 0, 100), 50, 'mapRange(5, 0, 10, 0, 100) 应返回 50');

assertArray(NumberUtils.range(1, 5), [1, 2, 3, 4], 'range(1, 5) 应返回 [1, 2, 3, 4]');
assertArray(NumberUtils.range(0, 10, 2), [0, 2, 4, 6, 8], 'range(0, 10, 2) 应返回 [0, 2, 4, 6, 8]');

assertArray(NumberUtils.sequence(1, 5), [1, 2, 3, 4, 5], 'sequence(1, 5) 应返回 [1, 2, 3, 4, 5]');
assertArray(NumberUtils.sequence(0, 5, 2), [0, 2, 4, 6, 8], 'sequence(0, 5, 2) 应返回 [0, 2, 4, 6, 8]');

assert(NumberUtils.wrap(5, 0, 10) === 5, 'wrap(5, 0, 10) 应返回 5');
assert(NumberUtils.wrap(-1, 0, 10) === 9, 'wrap(-1, 0, 10) 应返回 9');
assert(NumberUtils.wrap(11, 0, 10) === 1, 'wrap(11, 0, 10) 应返回 1');

assert(NumberUtils.closest(5, [1, 4, 6, 10]) === 4, 'closest(5, [1,4,6,10]) 应返回 4');
assert(NumberUtils.closest(7, [1, 4, 6, 10]) === 6, 'closest(7, [1,4,6,10]) 应返回 6');

// ==================== 随机数测试 ====================
console.log('\n📋 随机数测试');
console.log('----------------------------------------');

// 随机数测试（检查范围）
for (let i = 0; i < 100; i++) {
  const num = NumberUtils.randomInt(1, 10);
  assert(num >= 1 && num <= 10, `randomInt(1, 10) 应在范围内: ${num}`);
}

for (let i = 0; i < 100; i++) {
  const num = NumberUtils.randomFloat(1, 10, 2);
  assert(num >= 1 && num <= 10, `randomFloat(1, 10, 2) 应在范围内: ${num}`);
}

// 随机数组测试
const randomArr = NumberUtils.randomArray(5, 1, 10);
assert(randomArr.length === 5, 'randomArray(5, 1, 10) 应返回长度为 5 的数组');

// 唯一随机数组测试
const uniqueArr = NumberUtils.randomArray(5, 1, 10, true);
const uniqueSet = new Set(uniqueArr);
assert(uniqueSet.size === 5, 'randomArray(5, 1, 10, true) 应返回唯一值数组');

// 打乱数组测试
const original = [1, 2, 3, 4, 5];
const shuffled = NumberUtils.shuffle(original);
assert(shuffled.length === 5, 'shuffle 应保持数组长度');
assert(JSON.stringify([...original].sort()) === JSON.stringify(shuffled.sort()), 'shuffle 应保持元素不变');

// ==================== 数论函数测试 ====================
console.log('\n📋 数论函数测试');
console.log('----------------------------------------');

assert(NumberUtils.gcd(12, 8) === 4, 'gcd(12, 8) 应返回 4');
assert(NumberUtils.gcd(54, 24) === 6, 'gcd(54, 24) 应返回 6');
assert(NumberUtils.gcd(17, 13) === 1, 'gcd(17, 13) 应返回 1');

assert(NumberUtils.lcm(4, 6) === 12, 'lcm(4, 6) 应返回 12');
assert(NumberUtils.lcm(3, 5) === 15, 'lcm(3, 5) 应返回 15');

assert(NumberUtils.factorial(0) === 1, 'factorial(0) 应返回 1');
assert(NumberUtils.factorial(1) === 1, 'factorial(1) 应返回 1');
assert(NumberUtils.factorial(5) === 120, 'factorial(5) 应返回 120');
assert(NumberUtils.factorial(10) === 3628800, 'factorial(10) 应返回 3628800');

assert(NumberUtils.permutation(5, 3) === 60, 'permutation(5, 3) 应返回 60');
assert(NumberUtils.combination(5, 3) === 10, 'combination(5, 3) 应返回 10');
assert(NumberUtils.combination(10, 4) === 210, 'combination(10, 4) 应返回 210');

// 斐波那契测试
assert(NumberUtils.fibonacci(0) === 0, 'fibonacci(0) 应返回 0');
assert(NumberUtils.fibonacci(1) === 1, 'fibonacci(1) 应返回 1');
assert(NumberUtils.fibonacci(10) === 55, 'fibonacci(10) 应返回 55');

// 因数测试
assertArray(NumberUtils.factors(12), [1, 2, 3, 4, 6, 12], 'factors(12) 应返回 [1, 2, 3, 4, 6, 12]');
assertArray(NumberUtils.factors(7), [1, 7], 'factors(7) 应返回 [1, 7]');

// 质因数测试
assertArray(NumberUtils.primeFactors(12), [2, 2, 3], 'primeFactors(12) 应返回 [2, 2, 3]');
assertArray(NumberUtils.primeFactors(30), [2, 3, 5], 'primeFactors(30) 应返回 [2, 3, 5]');

// 互质测试
assert(NumberUtils.areCoprime(8, 15), 'areCoprime(8, 15) 应返回 true');
assert(!NumberUtils.areCoprime(8, 12), 'areCoprime(8, 12) 应返回 false');

// 质数序列测试
assertArray(NumberUtils.generatePrimes(5), [2, 3, 5, 7, 11], 'generatePrimes(5) 应返回 [2, 3, 5, 7, 11]');

// 埃拉托斯特尼筛法测试
assertArray(NumberUtils.sieveOfEratosthenes(10), [2, 3, 5, 7], 'sieveOfEratosthenes(10) 应返回 [2, 3, 5, 7]');

// ==================== 数值处理测试 ====================
console.log('\n📋 数值处理测试');
console.log('----------------------------------------');

assert(NumberUtils.round(3.14159, 2) === 3.14, 'round(3.14159, 2) 应返回 3.14');
assert(NumberUtils.round(3.14159, 0) === 3, 'round(3.14159, 0) 应返回 3');
assert(NumberUtils.round(3.5, 0) === 4, 'round(3.5, 0) 应返回 4');

assert(NumberUtils.ceil(3.14, 1) === 3.2, 'ceil(3.14, 1) 应返回 3.2');
assert(NumberUtils.floor(3.14, 1) === 3.1, 'floor(3.14, 1) 应返回 3.1');
assert(NumberUtils.truncate(3.99) === 3, 'truncate(3.99) 应返回 3');

assertApprox(NumberUtils.roundTo(123.456, 0.01), 123.46, 'roundTo(123.456, 0.01) 应返回约 123.46', 0.001);
assert(NumberUtils.roundTo(123.456, 5) === 125, 'roundTo(123.456, 5) 应返回 125');

assert(NumberUtils.sign(42) === 1, 'sign(42) 应返回 1');
assert(NumberUtils.sign(-42) === -1, 'sign(-42) 应返回 -1');
assert(NumberUtils.sign(0) === 0, 'sign(0) 应返回 0');

assert(NumberUtils.abs(-42) === 42, 'abs(-42) 应返回 42');
assert(NumberUtils.sqrt(16) === 4, 'sqrt(16) 应返回 4');
assert(NumberUtils.cbrt(27) === 3, 'cbrt(27) 应返回 3');
assert(NumberUtils.pow(2, 10) === 1024, 'pow(2, 10) 应返回 1024');

// 对数测试
assertApprox(NumberUtils.log(Math.E), 1, 'log(e) 应返回约 1');
assertApprox(NumberUtils.log10(100), 2, 'log10(100) 应返回约 2');
assertApprox(NumberUtils.log2(8), 3, 'log2(8) 应返回约 3');

// 三角函数测试
assertApprox(NumberUtils.sin(NumberUtils.toRadians(30)), 0.5, 'sin(30°) 应返回约 0.5');
assertApprox(NumberUtils.cos(NumberUtils.toRadians(60)), 0.5, 'cos(60°) 应返回约 0.5');
assertApprox(NumberUtils.toDegrees(Math.PI), 180, 'toDegrees(π) 应返回约 180');
assertApprox(NumberUtils.toRadians(180), Math.PI, 'toRadians(180) 应返回约 π');

// 双曲函数测试
assertApprox(NumberUtils.sinh(0), 0, 'sinh(0) 应返回约 0');
assertApprox(NumberUtils.cosh(0), 1, 'cosh(0) 应返回约 1');
assertApprox(NumberUtils.tanh(0), 0, 'tanh(0) 应返回约 0');

// ==================== 总结 ====================
console.log('\n========================================');
console.log('  测试总结');
console.log('========================================');
console.log(`✓ 通过: ${passed}`);
console.log(`✗ 失败: ${failed}`);
console.log(`总计: ${passed + failed}`);

if (failed > 0) {
  console.log('\n失败的测试:');
  failures.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));
  process.exit(1);
} else {
  console.log('\n🎉 所有测试通过！');
  process.exit(0);
}