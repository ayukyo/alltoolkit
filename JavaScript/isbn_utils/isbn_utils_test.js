/**
 * ISBN Utils 测试文件
 */

const assert = require('assert');
const {
    ISBNError,
    InvalidISBNError,
    ISBNConversionError,
    ISBNUtils,
    validate,
    validateStrict,
    convertTo13,
    convertTo10,
    formatISBN,
    parseISBN,
    generateRandomISBN,
    extractISBNFromText
} = require('./mod.js');

// 颜色输出辅助
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    reset: '\x1b[0m'
};

let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`${colors.green}✓${colors.reset} ${name}`);
        passed++;
    } catch (e) {
        console.log(`${colors.red}✗${colors.reset} ${name}`);
        console.log(`  ${colors.red}Error: ${e.message}${colors.reset}`);
        failed++;
    }
}

console.log('\n=== ISBN Utils 测试 ===\n');

// ============ 基础功能测试 ============

console.log('--- 基础功能测试 ---\n');

test('clean() - 清理 ISBN 字符串', () => {
    assert.strictEqual(ISBNUtils.clean('978-0-13-235088-4'), '9780132350884');
    assert.strictEqual(ISBNUtils.clean('0 13 235088 2'), '0132350882');
    assert.strictEqual(ISBNUtils.clean('ISBN 978-0-13-235088-4'), '9780132350884');
    assert.strictEqual(ISBNUtils.clean('9780132350884'), '9780132350884');
});

test('detectVersion() - 检测 ISBN 版本', () => {
    assert.strictEqual(ISBNUtils.detectVersion('0132350882'), 10);
    assert.strictEqual(ISBNUtils.detectVersion('9780132350884'), 13);
    assert.strictEqual(ISBNUtils.detectVersion('978-0-13-235088-4'), 13);
    assert.strictEqual(ISBNUtils.detectVersion('123'), null);
});

// ============ 校验位计算测试 ============

console.log('\n--- 校验位计算测试 ---\n');

test('calculateCheckDigit10() - 计算 ISBN-10 校验位', () => {
    assert.strictEqual(ISBNUtils.calculateCheckDigit10('013235088'), '2');
    assert.strictEqual(ISBNUtils.calculateCheckDigit10('030640615'), '2');
    assert.strictEqual(ISBNUtils.calculateCheckDigit10('020161622'), 'X'); // 校验位为 X (0-201-61622-X)
});

test('calculateCheckDigit12() - 计算 ISBN-13 校验位', () => {
    assert.strictEqual(ISBNUtils.calculateCheckDigit12('978013235088'), '4');
    assert.strictEqual(ISBNUtils.calculateCheckDigit12('978030640615'), '7');
    assert.strictEqual(ISBNUtils.calculateCheckDigit12('979109114613'), '5');
});

// ============ 验证测试 ============

console.log('\n--- 验证测试 ---\n');

test('validate() - 验证有效的 ISBN-10', () => {
    assert.strictEqual(validate('0-13-235088-2'), true);
    assert.strictEqual(validate('0306406152'), true);
    assert.strictEqual(validate('0-201-61622-X'), true); // 带 X 校验位
});

test('validate() - 验证有效的 ISBN-13', () => {
    assert.strictEqual(validate('978-0-13-235088-4'), true);
    assert.strictEqual(validate('9780306406157'), true);
    assert.strictEqual(validate('9791091146135'), true);
});

test('validate() - 验证无效的 ISBN', () => {
    assert.strictEqual(validate('0-13-235088-3'), false); // 错误校验位
    assert.strictEqual(validate('9780132350885'), false); // 错误校验位
    assert.strictEqual(validate('12345'), false); // 长度错误
    assert.strictEqual(validate('abcdefghij'), false); // 格式错误
});

test('validateStrict() - 严格验证返回详细信息', () => {
    const result = validateStrict('978-0-13-235088-4');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.version, 13);
    assert.strictEqual(result.isbn, '9780132350884');
    assert.strictEqual(result.checkDigit, '4');
    assert.strictEqual(result.prefix, '978');
});

test('validateStrict() - 无效 ISBN 抛出异常', () => {
    assert.throws(() => validateStrict('invalid'), InvalidISBNError);
    assert.throws(() => validateStrict('0-13-235088-3'), InvalidISBNError);
});

// ============ 转换测试 ============

console.log('\n--- 转换测试 ---\n');

test('convertTo13() - ISBN-10 转 ISBN-13', () => {
    assert.strictEqual(convertTo13('0-13-235088-2'), '9780132350884');
    assert.strictEqual(convertTo13('0306406152'), '9780306406157');
    assert.strictEqual(convertTo13('0-201-61622-X'), '9780201616224'); // 带 X 校验位
});

test('convertTo13() - 已是 ISBN-13 则原样返回', () => {
    assert.strictEqual(convertTo13('9780132350884'), '9780132350884');
});

test('convertTo10() - ISBN-13 转 ISBN-10', () => {
    assert.strictEqual(convertTo10('978-0-13-235088-4'), '0132350882');
    assert.strictEqual(convertTo10('9780306406157'), '0306406152');
});

test('convertTo10() - 已是 ISBN-10 则原样返回', () => {
    assert.strictEqual(convertTo10('0132350882'), '0132350882');
});

test('convertTo10() - 979 前缀无法转换', () => {
    assert.throws(() => convertTo10('9791091146135'), ISBNConversionError);
});

// ============ 格式化测试 ============

console.log('\n--- 格式化测试 ---\n');

test('format() - 格式化 ISBN-10', () => {
    assert.strictEqual(formatISBN('0132350882'), '0-1323-5088-2');
    assert.strictEqual(formatISBN('0-13-235088-2'), '0-1323-5088-2');
});

test('format() - 格式化 ISBN-13', () => {
    assert.strictEqual(formatISBN('9780132350884'), '978-0-1323-5088-4');
    assert.strictEqual(formatISBN('978-0-13-235088-4'), '978-0-1323-5088-4');
});

test('format() - 自定义分隔符', () => {
    assert.strictEqual(formatISBN('0132350882', ' '), '0 1323 5088 2');
    assert.strictEqual(formatISBN('9780132350884', ''), '9780132350884');
});

// ============ 解析测试 ============

console.log('\n--- 解析测试 ---\n');

test('parse() - 解析有效的 ISBN-10', () => {
    const result = parseISBN('0-13-235088-2');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.version, 10);
    assert.strictEqual(result.isbn, '0132350882');
    assert.strictEqual(result.isbn13, '9780132350884');
    assert.strictEqual(result.checkDigit, '2');
});

test('parse() - 解析有效的 ISBN-13 (978前缀)', () => {
    const result = parseISBN('978-0-13-235088-4');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.version, 13);
    assert.strictEqual(result.isbn, '9780132350884');
    assert.strictEqual(result.isbn10, '0132350882');
    assert.strictEqual(result.checkDigit, '4');
});

test('parse() - 解析有效的 ISBN-13 (979前缀)', () => {
    const result = parseISBN('9791091146135');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.version, 13);
    assert.strictEqual(result.isbn10, null); // 979 前缀无法转换
});

test('parse() - 解析无效的 ISBN', () => {
    const result = parseISBN('invalid');
    assert.strictEqual(result.valid, false);
    assert.ok(result.error);
});

// ============ 生成测试 ============

console.log('\n--- 生成测试 ---\n');

test('generateRandom() - 生成随机 ISBN-10', () => {
    const isbn = generateRandomISBN(10);
    assert.strictEqual(isbn.length, 10);
    assert.strictEqual(validate(isbn), true);
});

test('generateRandom() - 生成随机 ISBN-13', () => {
    const isbn = generateRandomISBN(13);
    assert.strictEqual(isbn.length, 13);
    assert.strictEqual(validate(isbn), true);
    assert.ok(isbn.startsWith('978') || isbn.startsWith('979'));
});

test('generateRandom() - 生成指定前缀的 ISBN-13', () => {
    const isbn978 = generateRandomISBN(13, '978');
    assert.strictEqual(isbn978.startsWith('978'), true);
    
    const isbn979 = generateRandomISBN(13, '979');
    assert.strictEqual(isbn979.startsWith('979'), true);
});

test('generateBatch() - 批量生成 ISBN', () => {
    const batch = ISBNUtils.generateBatch(5, 13);
    assert.strictEqual(batch.length, 5);
    assert.ok(batch.every(isbn => validate(isbn)));
});

// ============ 文本提取测试 ============

console.log('\n--- 文本提取测试 ---\n');

test('extractFromText() - 从文本中提取 ISBN', () => {
    const text = `
        这本书的 ISBN 是 978-0-13-235088-4，另一本是 0-13-235088-2。
        无效的 ISBN：978-0-13-235088-5（校验位错误）。
    `;
    const isbns = extractISBNFromText(text);
    assert.ok(isbns.includes('9780132350884'));
    assert.ok(isbns.includes('0132350882'));
    assert.ok(!isbns.includes('9780132350885')); // 无效的不应该被提取
});

// ============ 注册组测试 ============

console.log('\n--- 注册组测试 ---\n');

test('getRegistrationGroup() - 获取注册组信息', () => {
    assert.strictEqual(ISBNUtils.getRegistrationGroup('7-111-21321-6'), '中国');
    assert.strictEqual(ISBNUtils.getRegistrationGroup('9787111213210'), '中国');
    assert.strictEqual(ISBNUtils.getRegistrationGroup('0-13-235088-2'), '英语区');
    assert.strictEqual(ISBNUtils.getRegistrationGroup('4-XXXX-XXXX-X'), '日本');
    assert.strictEqual(ISBNUtils.getRegistrationGroup('2-XXXX-XXXX-X'), '法语区');
});

// ============ 边界情况测试 ============

console.log('\n--- 边界情况测试 ---\n');

test('处理带 X 校验位的 ISBN-10', () => {
    assert.strictEqual(validate('0-201-61622-X'), true);
    assert.strictEqual(validate('0-201-61622-x'), true); // 小写 x
    assert.strictEqual(ISBNUtils.calculateCheckDigit10('020161622'), 'X');
});

test('错误处理 - 无效输入', () => {
    assert.throws(() => ISBNUtils.calculateCheckDigit10('12345678'), InvalidISBNError);
    assert.throws(() => ISBNUtils.calculateCheckDigit10('abcdefghi'), InvalidISBNError);
    // 测试包含非数字的 ISBN-12
    assert.throws(() => ISBNUtils.calculateCheckDigit12('abc456789012'), InvalidISBNError);
});

test('错误处理 - 转换错误', () => {
    assert.throws(() => convertTo13('invalid'), ISBNConversionError);
    assert.throws(() => convertTo10('invalid'), ISBNConversionError);
});

// ============ 便捷函数测试 ============

console.log('\n--- 便捷函数测试 ---\n');

test('所有便捷函数正常工作', () => {
    // 验证函数是否导出
    assert.strictEqual(typeof validate, 'function');
    assert.strictEqual(typeof validateStrict, 'function');
    assert.strictEqual(typeof convertTo13, 'function');
    assert.strictEqual(typeof convertTo10, 'function');
    assert.strictEqual(typeof formatISBN, 'function');
    assert.strictEqual(typeof parseISBN, 'function');
    assert.strictEqual(typeof generateRandomISBN, 'function');
    assert.strictEqual(typeof extractISBNFromText, 'function');
    
    // 测试便捷函数
    assert.strictEqual(validate('9780132350884'), true);
    assert.strictEqual(convertTo13('0132350882'), '9780132350884');
    assert.strictEqual(convertTo10('9780132350884'), '0132350882');
    assert.strictEqual(formatISBN('0132350882'), '0-1323-5088-2');
    assert.ok(generateRandomISBN(13).length === 13);
});

// ============ 总结 ============

console.log('\n' + '='.repeat(40));
console.log(`测试完成: ${colors.green}${passed} 通过${colors.reset}, ${colors.red}${failed} 失败${colors.reset}`);
console.log('='.repeat(40) + '\n');

process.exit(failed > 0 ? 1 : 0);