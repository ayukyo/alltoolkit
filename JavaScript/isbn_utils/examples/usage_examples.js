/**
 * ISBN Utils 使用示例
 */

const {
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

console.log('=== ISBN Utils 使用示例 ===\n');

// ============ 1. 基础验证 ============

console.log('--- 1. 基础验证 ---\n');

const isbn10Valid = '0-13-235088-2';  // 《代码整洁之道》
const isbn13Valid = '978-7-111-21321-0';  // 某中文书

console.log(`验证 ISBN-10 "${isbn10Valid}": ${validate(isbn10Valid)}`);
console.log(`验证 ISBN-13 "${isbn13Valid}": ${validate(isbn13Valid)}`);

console.log(`验证无效 ISBN "0-13-235088-3": ${validate('0-13-235088-3')}`);

// ============ 2. 严格验证（获取详细信息） ============

console.log('\n--- 2. 严格验证 ---\n');

try {
    const result = validateStrict('978-0-13-235088-4');
    console.log('验证结果:', JSON.stringify(result, null, 2));
} catch (e) {
    console.error('验证失败:', e.message);
}

// ============ 3. 格式转换 ============

console.log('\n--- 3. 格式转换 ---\n');

// ISBN-10 转 ISBN-13
const isbn10 = '0306406152';  // 《代码大全》
const isbn13 = convertTo13(isbn10);
console.log(`ISBN-10 "${isbn10}" → ISBN-13 "${isbn13}"`);

// ISBN-13 转 ISBN-10
const isbn13_2 = '9780306406157';
const isbn10_2 = convertTo10(isbn13_2);
console.log(`ISBN-13 "${isbn13_2}" → ISBN-10 "${isbn10_2}"`);

// 注意：979 前缀的 ISBN-13 无法转换为 ISBN-10
console.log('\n979 前缀转换说明:');
try {
    convertTo10('9791091146135');
} catch (e) {
    console.log(`  错误: ${e.message}`);
}

// ============ 4. 格式化输出 ============

console.log('\n--- 4. 格式化输出 ---\n');

const rawISBN = '9780132350884';
console.log(`原始: "${rawISBN}"`);
console.log(`格式化: "${formatISBN(rawISBN)}"`);
console.log(`自定义分隔符: "${formatISBN(rawISBN, ' ')}"`);
console.log(`无分隔符: "${formatISBN(rawISBN, '')}"`);

// ============ 5. 解析详细信息 ============

console.log('\n--- 5. 解析详细信息 ---\n');

const parsed = parseISBN('978-7-111-21321-0');
console.log('解析结果:');
console.log(`  原始值: ${parsed.original}`);
console.log(`  清理后: ${parsed.isbn}`);
console.log(`  版本: ISBN-${parsed.version}`);
console.log(`  有效: ${parsed.valid}`);
console.log(`  格式化: ${parsed.isbnFormatted}`);
console.log(`  校验位: ${parsed.checkDigit}`);
console.log(`  前缀: ${parsed.prefix}`);
if (parsed.isbn10) {
    console.log(`  对应 ISBN-10: ${parsed.isbn10}`);
}

// ============ 6. 生成随机 ISBN（测试用） ============

console.log('\n--- 6. 生成随机 ISBN ---\n');

console.log('随机 ISBN-10:');
for (let i = 0; i < 3; i++) {
    console.log(`  ${generateRandomISBN(10)}`);
}

console.log('\n随机 ISBN-13 (978前缀):');
for (let i = 0; i < 3; i++) {
    console.log(`  ${generateRandomISBN(13, '978')}`);
}

console.log('\n随机 ISBN-13 (979前缀):');
for (let i = 0; i < 3; i++) {
    console.log(`  ${generateRandomISBN(13, '979')}`);
}

// 批量生成
console.log('\n批量生成 5 个 ISBN-13:');
const batch = ISBNUtils.generateBatch(5, 13);
batch.forEach((isbn, i) => console.log(`  ${i + 1}. ${isbn}`));

// ============ 7. 从文本中提取 ISBN ============

console.log('\n--- 7. 从文本中提取 ISBN ---\n');

const sampleText = `
本周推荐书籍：
1. 《代码整洁之道》ISBN: 978-0-13-235088-4
2. 《人月神话》ISBN-10: 0-201-00650-9
3. 《设计模式》ISBN: 978-7-111-21321-0

注意：以下无效 ISBN 不会被提取：
- 错误校验位: 978-0-13-235088-5
- 格式错误: 123-456

请参考 http://example.com/books 获取更多信息。
`;

const extracted = extractISBNFromText(sampleText);
console.log('从文本中提取的有效 ISBN:');
extracted.forEach((isbn, i) => {
    console.log(`  ${i + 1}. ${isbn} (${formatISBN(isbn)})`);
});

// ============ 8. 注册组查询 ============

console.log('\n--- 8. 注册组查询 ---\n');

const testISBNs = [
    { isbn: '7-111-21321-6', name: '《设计模式》' },
    { isbn: '0-13-235088-2', name: '《代码整洁之道》' },
    { isbn: '4-XXXX-XXXX-X', name: '日本书籍' },
    { isbn: '2-XXXX-XXXX-X', name: '法语书籍' },
    { isbn: '978-89-XXXX-XXX-X', name: '韩国书籍' }
];

testISBNs.forEach(item => {
    const group = ISBNUtils.getRegistrationGroup(item.isbn);
    console.log(`${item.isbn} (${item.name}) → ${group || '未知'}`);
});

// ============ 9. 校验位计算 ============

console.log('\n--- 9. 校验位计算 ---\n');

// 计算 ISBN-10 校验位
const isbn9 = '013235088';
const check10 = ISBNUtils.calculateCheckDigit10(isbn9);
console.log(`ISBN-10 前9位 "${isbn9}" 的校验位: ${check10}`);
console.log(`完整 ISBN-10: ${isbn9}${check10}`);

// 计算 ISBN-13 校验位
const isbn12 = '978013235088';
const check13 = ISBNUtils.calculateCheckDigit12(isbn12);
console.log(`\nISBN-13 前12位 "${isbn12}" 的校验位: ${check13}`);
console.log(`完整 ISBN-13: ${isbn12}${check13}`);

// ============ 10. 错误处理 ============

console.log('\n--- 10. 错误处理 ---\n');

// 无效 ISBN 验证
const invalidResults = parseISBN('978-0-13-235088-5'); // 错误校验位
console.log('无效 ISBN 解析结果:');
console.log(`  有效: ${invalidResults.valid}`);
console.log(`  错误: ${invalidResults.error}`);

// 异常捕获
console.log('\n异常处理示例:');
try {
    ISBNUtils.calculateCheckDigit10('12345678'); // 只有8位
} catch (e) {
    console.log(`  捕获异常: ${e.name} - ${e.message}`);
}

console.log('\n=== 示例完成 ===');