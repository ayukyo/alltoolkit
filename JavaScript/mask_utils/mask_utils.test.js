/**
 * mask_utils 单元测试
 */

const assert = require('assert');
const {
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
    formatBankCard,
    formatPhone,
    formatAmount,
    validatePhone,
    validateEmail,
    validateIdCard,
    validateBankCard,
    validateIP,
    validateCreditCard,
    maskPhoneInText,
    maskEmailInText,
    maskIdCardInText,
    maskBatch
} = require('./mask_utils.js');

console.log('=== mask_utils 单元测试 ===\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`✓ ${name}`);
        passed++;
    } catch (e) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${e.message}`);
        failed++;
    }
}

// ========== maskPhone 测试 ==========
console.log('\n--- maskPhone 测试 ---');

test('手机号脱敏 - 标准11位', () => {
    assert.strictEqual(maskPhone('13812345678'), '138****5678');
});

test('手机号脱敏 - 自定义掩码字符', () => {
    assert.strictEqual(maskPhone('13812345678', { maskChar: 'x' }), '138xxxx5678');
});

test('手机号脱敏 - 自定义显示位数', () => {
    assert.strictEqual(maskPhone('13812345678', { showFirst: 2, showLast: 3 }), '13******678');
});

test('手机号脱敏 - 空值处理', () => {
    assert.strictEqual(maskPhone(''), '');
    assert.strictEqual(maskPhone(null), '');
    assert.strictEqual(maskPhone(undefined), '');
});

test('手机号脱敏 - 短号码原样返回', () => {
    assert.strictEqual(maskPhone('123'), '123');
});

test('手机号脱 - 含非数字字符', () => {
    assert.strictEqual(maskPhone('138-1234-5678'), '138****5678');
});

// ========== maskTelephone 测试 ==========
console.log('\n--- maskTelephone 测试 ---');

test('固话脱敏 - 带横杠', () => {
    const result = maskTelephone('010-12345678');
    assert.ok(result.includes('010'));
    assert.ok(result.includes('5678'));
});

test('固话脱敏 - 纯数字', () => {
    const result = maskTelephone('01012345678');
    assert.ok(result.includes('010'));
});

// ========== maskIdCard 测试 ==========
console.log('\n--- maskIdCard 测试 ---');

test('身份证脱敏 - 18位', () => {
    const result = maskIdCard('110101199001011234');
    assert.ok(result.startsWith('110101'));
    assert.ok(result.endsWith('1234'));
    assert.ok(result.includes('********'));
});

test('身份证脱敏 - 15位', () => {
    const result = maskIdCard('110101900101123');
    assert.ok(result.startsWith('110101'));
});

test('身份证脱敏 - 含空格', () => {
    const result = maskIdCard('110101 19900101 1234');
    assert.ok(result.includes('********'));
});

test('身份证脱敏 - 小写x转大写', () => {
    const result = maskIdCard('11010119900101123x');
    assert.ok(result.endsWith('123X'));
});

// ========== maskBankCard 测试 ==========
console.log('\n--- maskBankCard 测试 ---');

test('银行卡脱敏 - 16位', () => {
    const result = maskBankCard('6222021234567890');
    assert.ok(result.startsWith('6222'));
    assert.ok(result.endsWith('7890'));
});

test('银行卡脱敏 - 19位', () => {
    const result = maskBankCard('6222021234567890123');
    assert.ok(result.startsWith('6222'));
    assert.ok(result.endsWith('0123'));
});

// ========== maskEmail 测试 ==========
console.log('\n--- maskEmail 测试 ---');

test('邮箱脱敏 - 标准格式', () => {
    const result = maskEmail('example@domain.com');
    assert.ok(result.startsWith('e'));
    assert.ok(result.endsWith('@domain.com'));
    assert.ok(result.includes('*'));
});

test('邮箱脱敏 - 长用户名', () => {
    const result = maskEmail('verylongemail@domain.com');
    assert.ok(result.startsWith('v'));
    assert.ok(result.endsWith('@domain.com'));
});

test('邮箱脱敏 - 短用户名', () => {
    const result = maskEmail('a@b.com');
    assert.strictEqual(result, '*@b.com');
});

test('邮箱脱敏 - 无效邮箱', () => {
    assert.strictEqual(maskEmail('invalid'), 'invalid');
    assert.strictEqual(maskEmail('no-at-sign.com'), 'no-at-sign.com');
});

// ========== maskName 测试 ==========
console.log('\n--- maskName 测试 ---');

test('姓名脱敏 - 两个字', () => {
    assert.strictEqual(maskName('张三'), '张*');
});

test('姓名脱敏 - 三个字', () => {
    assert.strictEqual(maskName('张小明'), '张**');
});

test('姓名脱敏 - 四个字', () => {
    assert.strictEqual(maskName('欧阳小明'), '欧***');
});

test('姓名脱敏 - 单字姓名', () => {
    assert.strictEqual(maskName('张'), '张');
});

// ========== maskAddress 测试 ==========
console.log('\n--- maskAddress 测试 ---');

test('地址脱敏 - 完整地址', () => {
    const result = maskAddress('北京市朝阳区望京街道');
    assert.ok(result.startsWith('北京市朝阳区'));
    assert.ok(result.includes('*'));
});

test('地址脱敏 - 简短地址', () => {
    const result = maskAddress('北京市');
    assert.ok(result.length > 0);
});

// ========== maskIP 测试 ==========
console.log('\n--- maskIP 测试 ---');

test('IP脱敏 - IPv4', () => {
    const result = maskIP('192.168.1.100');
    assert.ok(result.startsWith('192.168'));
    assert.ok(result.includes('*'));
});

test('IP脱敏 - 无效IP', () => {
    const result = maskIP('invalid');
    assert.strictEqual(result, 'invalid');
});

// ========== maskCreditCard 测试 ==========
console.log('\n--- maskCreditCard 测试 ---');

test('信用卡脱敏 - Visa', () => {
    const result = maskCreditCard('4532015112830366');
    assert.ok(result.startsWith('4532'));
    assert.ok(result.endsWith('0366'));
});

// ========== maskPassport 测试 ==========
console.log('\n--- maskPassport 测试 ---');

test('护照脱敏 - 标准格式', () => {
    const result = maskPassport('G12345678');
    assert.ok(result.startsWith('G12'));
    assert.ok(result.endsWith('78'));
});

// ========== maskLicensePlate 测试 ==========
console.log('\n--- maskLicensePlate 测试 ---');

test('车牌脱敏 - 标准', () => {
    const result = maskLicensePlate('京A12345');
    assert.ok(result.startsWith('京A'));
    assert.ok(result.endsWith('45'));
});

test('车牌脱敏 - 新能源', () => {
    const result = maskLicensePlate('京AD12345');
    assert.ok(result.includes('*'));
});

// ========== maskSocialCreditCode 测试 ==========
console.log('\n--- maskSocialCreditCode 测试 ---');

test('社会信用代码脱敏', () => {
    const result = maskSocialCreditCode('91110108551385081X');
    assert.ok(result.startsWith('911101'));
    assert.ok(result.endsWith('81X'));
});

// ========== maskCustom 测试 ==========
console.log('\n--- maskCustom 测试 ---');

test('自定义脱敏', () => {
    assert.strictEqual(maskCustom('abcdefghij', 2, 2), 'ab******ij');
});

test('自定义脱敏 - 短字符串', () => {
    assert.strictEqual(maskCustom('abc', 2, 2), 'abc');
});

test('自定义脱敏 - 自定义掩码字符', () => {
    assert.strictEqual(maskCustom('abcdefghij', 2, 2, { maskChar: '#' }), 'ab######ij');
});

// ========== formatBankCard 测试 ==========
console.log('\n--- formatBankCard 测试 ---');

test('银行卡格式化 - 16位', () => {
    assert.strictEqual(formatBankCard('6222021234567890'), '6222 0212 3456 7890');
});

test('银行卡格式化 - 19位', () => {
    const result = formatBankCard('6222021234567890123');
    assert.ok(result.includes('6222'));
});

test('银行卡格式化 - 自定义分隔符', () => {
    assert.strictEqual(formatBankCard('6222021234567890', '-'), '6222-0212-3456-7890');
});

// ========== formatPhone 测试 ==========
console.log('\n--- formatPhone 测试 ---');

test('手机号格式化 - 11位', () => {
    assert.strictEqual(formatPhone('13812345678'), '138 1234 5678');
});

test('手机号格式化 - 自定义分隔符', () => {
    assert.strictEqual(formatPhone('13812345678', '-'), '138-1234-5678');
});

// ========== formatAmount 测试 ==========
console.log('\n--- formatAmount 测试 ---');

test('金额格式化 - 整数', () => {
    assert.strictEqual(formatAmount(1234567), '1,234,567.00');
});

test('金额格式化 - 小数', () => {
    assert.strictEqual(formatAmount(1234567.89), '1,234,567.89');
});

test('金额格式化 - 自定义小数位', () => {
    assert.strictEqual(formatAmount(1234567.89, 4), '1,234,567.8900');
});

test('金额格式化 - 字符串输入', () => {
    assert.strictEqual(formatAmount('1234567.89'), '1,234,567.89');
});

test('金额格式化 - 空值', () => {
    assert.strictEqual(formatAmount(''), '');
    assert.strictEqual(formatAmount(null), '');
});

// ========== validatePhone 测试 ==========
console.log('\n--- validatePhone 测试 ---');

test('手机号验证 - 有效', () => {
    assert.strictEqual(validatePhone('13812345678'), true);
    assert.strictEqual(validatePhone('19912345678'), true);
});

test('手机号验证 - 无效', () => {
    assert.strictEqual(validatePhone('12812345678'), false); // 无效号段
    assert.strictEqual(validatePhone('1381234567'), false);  // 少一位
    assert.strictEqual(validatePhone('138123456789'), false); // 多一位
    assert.strictEqual(validatePhone('abcdefghijk'), false); // 非数字
});

// ========== validateEmail 测试 ==========
console.log('\n--- validateEmail 测试 ---');

test('邮箱验证 - 有效', () => {
    assert.strictEqual(validateEmail('test@example.com'), true);
    assert.strictEqual(validateEmail('user.name@domain.co.uk'), true);
    assert.strictEqual(validateEmail('user+tag@example.org'), true);
});

test('邮箱验证 - 无效', () => {
    assert.strictEqual(validateEmail('invalid'), false);
    assert.strictEqual(validateEmail('no-at-sign.com'), false);
    assert.strictEqual(validateEmail('@domain.com'), false);
    assert.strictEqual(validateEmail('user@'), false);
});

// ========== validateIdCard 测试 ==========
console.log('\n--- validateIdCard 测试 ---');

test('身份证验证 - 有效18位', () => {
    assert.strictEqual(validateIdCard('11010519491231002X'), true);
});

test('身份证验证 - 有效15位', () => {
    assert.strictEqual(validateIdCard('110105491231001'), true);
});

test('身份证验证 - 无效位数', () => {
    assert.strictEqual(validateIdCard('1101051949123100'), false);
});

test('身份证验证 - 无效字符', () => {
    assert.strictEqual(validateIdCard('11010519491231002A'), false);
});

test('身份证验证 - 校验位错误', () => {
    assert.strictEqual(validateIdCard('110105194912310021'), false);
});

// ========== validateBankCard 测试 ==========
console.log('\n--- validateBankCard 测试 ---');

test('银行卡验证 - 有效', () => {
    assert.strictEqual(validateBankCard('4532015112830366'), true); // Visa
    assert.strictEqual(validateBankCard('5500000000000004'), true); // MasterCard
});

test('银行卡验证 - 无效', () => {
    assert.strictEqual(validateBankCard('1234567890123456'), false); // Luhn校验失败
    assert.strictEqual(validateBankCard('123'), false); // 太短
    assert.strictEqual(validateBankCard('abcdefghijklmnop'), false); // 非数字
});

// ========== validateIP 测试 ==========
console.log('\n--- validateIP 测试 ---');

test('IP验证 - 有效IPv4', () => {
    assert.strictEqual(validateIP('192.168.1.1'), true);
    assert.strictEqual(validateIP('0.0.0.0'), true);
    assert.strictEqual(validateIP('255.255.255.255'), true);
});

test('IP验证 - 无效IPv4', () => {
    assert.strictEqual(validateIP('256.1.1.1'), false);
    assert.strictEqual(validateIP('192.168.1'), false);
    assert.strictEqual(validateIP('192.168.1.1.1'), false);
});

// ========== validateCreditCard 测试 ==========
console.log('\n--- validateCreditCard 测试 ---');

test('信用卡验证 - Visa', () => {
    const result = validateCreditCard('4532015112830366');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.type, 'Visa');
});

test('信用卡验证 - MasterCard', () => {
    const result = validateCreditCard('5500000000000004');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.type, 'MasterCard');
});

test('信用卡验证 - 无效', () => {
    const result = validateCreditCard('1234567890123456');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.type, null);
});

// ========== maskPhoneInText 测试 ==========
console.log('\n--- maskPhoneInText 测试 ---');

test('文本中手机号脱敏', () => {
    const result = maskPhoneInText('联系13812345678或13987654321');
    assert.ok(result.includes('138****5678'));
    assert.ok(result.includes('139****4321'));
});

test('文本中手机号脱敏 - 无手机号', () => {
    assert.strictEqual(maskPhoneInText('这是普通文本'), '这是普通文本');
});

// ========== maskEmailInText 测试 ==========
console.log('\n--- maskEmailInText 测试 ---');

test('文本中邮箱脱敏', () => {
    const result = maskEmailInText('联系test@example.com或admin@domain.org');
    assert.ok(result.includes('*'));
    assert.ok(result.includes('@example.com'));
    assert.ok(result.includes('@domain.org'));
});

// ========== maskIdCardInText 测试 ==========
console.log('\n--- maskIdCardInText 测试 ---');

test('文本中身份证脱敏', () => {
    const result = maskIdCardInText('身份证号110101199001011234和123456789012345');
    assert.ok(result.includes('********'));
});

// ========== maskBatch 测试 ==========
console.log('\n--- maskBatch 测试 ---');

test('批量脱敏', () => {
    const data = {
        phone: '13812345678',
        email: 'test@example.com',
        name: '张三'
    };
    const rules = {
        phone: 'phone',
        email: 'email',
        name: 'name'
    };
    const result = maskBatch(data, rules);
    assert.strictEqual(result.phone, '138****5678');
    assert.ok(result.email.startsWith('t'));
    assert.strictEqual(result.name, '张*');
});

test('批量脱敏 - 保留未定义规则的字段', () => {
    const data = {
        phone: '13812345678',
        other: '原始值'
    };
    const rules = { phone: 'phone' };
    const result = maskBatch(data, rules);
    assert.strictEqual(result.other, '原始值');
});

// ========== 边界情况测试 ==========
console.log('\n--- 边界情况测试 ---');

test('空值处理 - 所有函数', () => {
    assert.strictEqual(maskPhone(null), '');
    assert.strictEqual(maskEmail(undefined), '');
    assert.strictEqual(maskIdCard(''), '');
    assert.strictEqual(maskBankCard(''), '');
    assert.strictEqual(maskName(''), '');
    assert.strictEqual(maskAddress(''), '');
    assert.strictEqual(maskIP(''), '');
    assert.strictEqual(maskCustom('', 1, 1), '');
});

test('格式化函数 - 空值', () => {
    assert.strictEqual(formatBankCard(null), '');
    assert.strictEqual(formatPhone(undefined), '');
    assert.strictEqual(formatAmount(''), '');
});

test('验证函数 - 空值', () => {
    assert.strictEqual(validatePhone(null), false);
    assert.strictEqual(validateEmail(undefined), false);
    assert.strictEqual(validateIdCard(''), false);
    assert.strictEqual(validateBankCard(''), false);
    assert.strictEqual(validateIP(''), false);
});

// ========== 输出测试结果 ==========
console.log('\n=== 测试结果 ===');
console.log(`通过: ${passed}`);
console.log(`失败: ${failed}`);
console.log(`总计: ${passed + failed}`);

if (failed > 0) {
    process.exit(1);
}