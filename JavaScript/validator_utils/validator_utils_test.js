/**
 * Validator Utils 测试文件
 * 
 * 运行方式：node validator_utils_test.js
 */

const assert = require('assert');
const {
    ValidatorUtils,
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
} = require('./mod.js');

// 测试计数器
let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        passed++;
        console.log(`✅ ${name}`);
    } catch (e) {
        failed++;
        console.log(`❌ ${name}`);
        console.log(`   错误: ${e.message}`);
    }
}

function testGroup(name) {
    console.log(`\n${name}`);
    console.log('='.repeat(50));
}

// ============== 邮箱测试 ==============
testGroup('邮箱验证测试');

test('有效邮箱 - 标准格式', () => {
    assert.strictEqual(isEmail('test@example.com'), true);
    assert.strictEqual(isEmail('user.name@example.com'), true);
    assert.strictEqual(isEmail('user+tag@example.com'), true);
    assert.strictEqual(isEmail('test@sub.example.com'), true);
});

test('无效邮箱 - 格式错误', () => {
    assert.strictEqual(isEmail(''), false);
    assert.strictEqual(isEmail('test'), false);
    assert.strictEqual(isEmail('test@'), false);
    assert.strictEqual(isEmail('@example.com'), false);
    assert.strictEqual(isEmail('test@example'), false);
});

test('邮箱详细验证', () => {
    const result = ValidatorUtils.validateEmail('test@example.com');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.localPart, 'test');
    assert.strictEqual(result.domain, 'example.com');
});

// ============== URL 测试 ==============
testGroup('URL 验证测试');

test('有效 URL - HTTP/HTTPS', () => {
    assert.strictEqual(isURL('http://example.com'), true);
    assert.strictEqual(isURL('https://example.com'), true);
    assert.strictEqual(isURL('https://www.example.com/path?query=1'), true);
});

test('无效 URL', () => {
    assert.strictEqual(isURL(''), false);
    assert.strictEqual(isURL('example'), false);
    assert.strictEqual(isURL('ftp://example.com', { protocols: ['http', 'https'] }), false);
});

test('URL 详细验证', () => {
    const result = ValidatorUtils.validateURL('https://example.com:8080/path?q=1#hash');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.protocol, 'https');
    assert.strictEqual(result.hostname, 'example.com');
    assert.strictEqual(result.port, '8080');
    assert.strictEqual(result.pathname, '/path');
});

// ============== 手机号测试 ==============
testGroup('手机号验证测试');

test('有效中国手机号', () => {
    assert.strictEqual(isChinesePhone('13812345678'), true);
    assert.strictEqual(isChinesePhone('15912345678'), true);
    assert.strictEqual(isChinesePhone('+8613812345678'), true);
    assert.strictEqual(isChinesePhone('8613812345678'), true);
});

test('无效手机号', () => {
    assert.strictEqual(isChinesePhone(''), false);
    assert.strictEqual(isChinesePhone('12345678901'), false);
    assert.strictEqual(isChinesePhone('1381234567'), false);
    assert.strictEqual(isChinesePhone('138123456789'), false);
});

test('手机号详细验证 - 运营商识别', () => {
    const result = ValidatorUtils.validateChinesePhone('13812345678');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.carrier, '中国移动');
});

test('手机号详细验证 - 联通', () => {
    const result = ValidatorUtils.validateChinesePhone('13012345678');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.carrier, '中国联通');
});

test('手机号详细验证 - 电信', () => {
    const result = ValidatorUtils.validateChinesePhone('18912345678');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.carrier, '中国电信');
});

test('国际手机号验证', () => {
    assert.strictEqual(ValidatorUtils.isInternationalPhone('+8613812345678'), true);
    assert.strictEqual(ValidatorUtils.isInternationalPhone('+12125551234'), true);
    assert.strictEqual(ValidatorUtils.isInternationalPhone('13812345678'), false);
});

// ============== 身份证测试 ==============
testGroup('身份证验证测试');

test('有效身份证 - 18位', () => {
    // 使用测试身份证号（非真实但校验位正确）
    assert.strictEqual(isChineseID('110105199001011232'), true);
    assert.strictEqual(isChineseID('320311197812180046'), true);
});

test('有效身份证 - 15位', () => {
    assert.strictEqual(isChineseID('110105491231001'), true);
});

test('无效身份证', () => {
    assert.strictEqual(isChineseID(''), false);
    assert.strictEqual(isChineseID('123456789'), false);
    assert.strictEqual(isChineseID('110105194912310020'), false); // 校验位错误
});

test('身份证详细验证', () => {
    const result = ValidatorUtils.validateChineseID('110105199001011232');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.birthday, '19900101');
    assert.strictEqual(result.gender, '男');
    assert.strictEqual(result.province, '北京市');
    assert.ok(result.age !== null);
});

test('身份证详细验证 - 女性', () => {
    const result = ValidatorUtils.validateChineseID('320311197812180046');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.gender, '女');
});

// ============== 信用卡测试 ==============
testGroup('信用卡验证测试');

test('Luhn 算法 - 有效卡号', () => {
    // 使用测试卡号（非真实）
    assert.strictEqual(luhnCheck('4111111111111111'), true); // Visa 测试卡号
    assert.strictEqual(luhnCheck('5500000000000004'), true); // Mastercard 测试卡号
});

test('Luhn 算法 - 无效卡号', () => {
    assert.strictEqual(luhnCheck('4111111111111112'), false);
    assert.strictEqual(luhnCheck(''), false);
    assert.strictEqual(luhnCheck('12345678'), false);
});

test('信用卡验证', () => {
    const result = ValidatorUtils.validateCreditCard('4111111111111111');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.issuer, 'Visa');
});

test('银行卡验证', () => {
    // 使用符合 Luhn 校验的测试银行卡号（银联 62 开头）
    assert.strictEqual(isBankCard('6225881234567898'), true);
    assert.strictEqual(isBankCard('6217001234567893'), true);
    assert.strictEqual(isBankCard('12345678'), false);
});

// ============== IP 地址测试 ==============
testGroup('IP 地址验证测试');

test('IPv4 验证 - 有效', () => {
    assert.strictEqual(isIPv4('192.168.1.1'), true);
    assert.strictEqual(isIPv4('0.0.0.0'), true);
    assert.strictEqual(isIPv4('255.255.255.255'), true);
    assert.strictEqual(isIPv4('127.0.0.1'), true);
});

test('IPv4 验证 - 无效', () => {
    assert.strictEqual(isIPv4(''), false);
    assert.strictEqual(isIPv4('256.1.1.1'), false);
    assert.strictEqual(isIPv4('192.168.1'), false);
    assert.strictEqual(isIPv4('192.168.1.1.1'), false);
    assert.strictEqual(isIPv4('192.168.1.1a'), false);
});

test('IPv6 验证 - 有效', () => {
    assert.strictEqual(isIPv6('::1'), true);
    assert.strictEqual(isIPv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334'), true);
    assert.strictEqual(isIPv6('2001:db8:85a3::8a2e:370:7334'), true);
    assert.strictEqual(isIPv6('::'), true);
    assert.strictEqual(isIPv6('fe80::1'), true);
});

test('IPv6 验证 - 无效', () => {
    assert.strictEqual(isIPv6(''), false);
    assert.strictEqual(isIPv6('192.168.1.1'), false);
    assert.strictEqual(isIPv6('gggg::1'), false);
});

test('IP 验证 - 自动识别', () => {
    assert.strictEqual(isIP('192.168.1.1'), true);
    assert.strictEqual(isIP('::1'), true);
    assert.strictEqual(isIP('invalid'), false);
});

test('IP 详细验证 - 私有地址', () => {
    const result = ValidatorUtils.validateIP('192.168.1.1');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.version, 4);
    assert.strictEqual(result.isPrivate, true);
});

test('IP 详细验证 - 公网地址', () => {
    const result = ValidatorUtils.validateIP('8.8.8.8');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.isPrivate, false);
});

test('IP 详细验证 - 回环地址', () => {
    const result = ValidatorUtils.validateIP('127.0.0.1');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.isLoopback, true);
});

// ============== 密码强度测试 ==============
testGroup('密码强度测试');

test('非常弱密码', () => {
    const result = checkPasswordStrength('123');
    assert.strictEqual(result.level, 0);
    assert.strictEqual(result.strength, 'very-weak');
});

test('弱密码', () => {
    const result = checkPasswordStrength('password');
    assert.ok(result.level <= 1);
});

test('中等密码', () => {
    const result = checkPasswordStrength('Password1');
    assert.ok(result.level >= 1);
});

test('强密码', () => {
    const result = checkPasswordStrength('Str0ng!Pass');
    assert.ok(result.level >= 2);
    assert.strictEqual(result.hasLower, true);
    assert.strictEqual(result.hasUpper, true);
    assert.strictEqual(result.hasNumber, true);
    assert.strictEqual(result.hasSymbol, true);
});

test('非常强密码', () => {
    const result = checkPasswordStrength('Th1sIs@V3ryStr0ngP@ssw0rd!');
    assert.ok(result.level >= 3);
});

test('空密码', () => {
    const result = checkPasswordStrength('');
    assert.strictEqual(result.valid, undefined); // 不报错，但无密码
    assert.strictEqual(result.errors.length > 0, true);
});

test('常见密码检测', () => {
    const result = checkPasswordStrength('password123');
    // 检查是否有建议
    assert.ok(result.suggestions.length > 0 || result.score < 5);
});

// ============== 通用验证测试 ==============
testGroup('通用验证测试');

test('isEmpty', () => {
    assert.strictEqual(ValidatorUtils.isEmpty(null), true);
    assert.strictEqual(ValidatorUtils.isEmpty(undefined), true);
    assert.strictEqual(ValidatorUtils.isEmpty(''), true);
    assert.strictEqual(ValidatorUtils.isEmpty('  '), true);
    assert.strictEqual(ValidatorUtils.isEmpty([]), true);
    assert.strictEqual(ValidatorUtils.isEmpty({}), true);
    assert.strictEqual(ValidatorUtils.isEmpty('test'), false);
    assert.strictEqual(ValidatorUtils.isEmpty([1]), false);
    assert.strictEqual(ValidatorUtils.isEmpty({ a: 1 }), false);
});

test('isInRange', () => {
    assert.strictEqual(ValidatorUtils.isInRange(5, 1, 10), true);
    assert.strictEqual(ValidatorUtils.isInRange(1, 1, 10), true);
    assert.strictEqual(ValidatorUtils.isInRange(10, 1, 10), true);
    assert.strictEqual(ValidatorUtils.isInRange(0, 1, 10), false);
    assert.strictEqual(ValidatorUtils.isInRange(11, 1, 10), false);
});

test('isLength', () => {
    assert.strictEqual(ValidatorUtils.isLength('test', 1, 10), true);
    assert.strictEqual(ValidatorUtils.isLength('test', 5), false);
    assert.strictEqual(ValidatorUtils.isLength('', 1), false);
});

test('isNumeric', () => {
    assert.strictEqual(ValidatorUtils.isNumeric('12345'), true);
    assert.strictEqual(ValidatorUtils.isNumeric('12.34'), false);
    assert.strictEqual(ValidatorUtils.isNumeric('abc'), false);
});

test('isAlpha', () => {
    assert.strictEqual(ValidatorUtils.isAlpha('hello'), true);
    assert.strictEqual(ValidatorUtils.isAlpha('Hello'), true);
    assert.strictEqual(ValidatorUtils.isAlpha('Hello123'), false);
});

test('isAlphanumeric', () => {
    assert.strictEqual(ValidatorUtils.isAlphanumeric('Hello123'), true);
    assert.strictEqual(ValidatorUtils.isAlphanumeric('Hello!'), false);
});

test('isDate', () => {
    assert.strictEqual(ValidatorUtils.isDate('2024-01-15'), true);
    assert.strictEqual(ValidatorUtils.isDate('2024-13-01'), false);
    assert.strictEqual(ValidatorUtils.isDate('2024-02-30'), false);
    assert.strictEqual(ValidatorUtils.isDate('15/01/2024', 'DD/MM/YYYY'), true);
    assert.strictEqual(ValidatorUtils.isDate('01/15/2024', 'MM/DD/YYYY'), true);
});

test('isHexColor', () => {
    assert.strictEqual(ValidatorUtils.isHexColor('#fff'), true);
    assert.strictEqual(ValidatorUtils.isHexColor('#ffffff'), true);
    assert.strictEqual(ValidatorUtils.isHexColor('ffffff'), true);
    assert.strictEqual(ValidatorUtils.isHexColor('#gggggg'), false);
    assert.strictEqual(ValidatorUtils.isHexColor('#ff'), false);
});

test('isJSON', () => {
    assert.strictEqual(ValidatorUtils.isJSON('{"name":"test"}'), true);
    assert.strictEqual(ValidatorUtils.isJSON('[1,2,3]'), true);
    assert.strictEqual(ValidatorUtils.isJSON('invalid'), false);
    assert.strictEqual(ValidatorUtils.isJSON('{invalid}'), false);
});

// ============== 批量验证测试 ==============
testGroup('批量验证测试');

test('批量验证 - 通过', () => {
    const data = {
        email: 'test@example.com',
        name: 'John Doe',
        age: 25
    };
    const rules = {
        email: { type: 'email', required: true },
        name: { required: true, minLength: 2 },
        age: { type: 'number', min: 0, max: 150 }
    };
    const result = validate(data, rules);
    assert.strictEqual(result.valid, true);
    assert.strictEqual(Object.keys(result.errors).length, 0);
});

test('批量验证 - 失败', () => {
    const data = {
        email: 'invalid-email',
        name: 'J',
        age: -5
    };
    const rules = {
        email: { type: 'email', required: true },
        name: { required: true, minLength: 2 },
        age: { type: 'number', min: 0, max: 150 }
    };
    const result = validate(data, rules);
    assert.strictEqual(result.valid, false);
    assert.ok(result.errors.email);
    assert.ok(result.errors.name);
    assert.ok(result.errors.age);
});

test('批量验证 - 必填字段缺失', () => {
    const data = { name: 'John' };
    const rules = {
        email: { required: true, message: '邮箱是必填项' }
    };
    const result = validate(data, rules);
    assert.strictEqual(result.valid, false);
    assert.ok(result.errors.email.includes('邮箱是必填项'));
});

test('批量验证 - 正则验证', () => {
    const data = { phone: '13812345678' };
    const rules = {
        phone: { pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误' }
    };
    const result = validate(data, rules);
    assert.strictEqual(result.valid, true);
});

test('批量验证 - 自定义验证', () => {
    const data = { username: 'admin' };
    const rules = {
        username: {
            validate: (value) => {
                const forbidden = ['admin', 'root', 'user'];
                return forbidden.includes(value.toLowerCase()) 
                    ? '用户名已被禁止使用' 
                    : true;
            }
        }
    };
    const result = validate(data, rules);
    assert.strictEqual(result.valid, false);
    // errors.username 是数组，检查包含错误消息
    assert.ok(result.errors.username && result.errors.username.some(e => e.includes('禁止')));
});

// ============== 边界条件测试 ==============
testGroup('边界条件测试');

test('null 和 undefined 输入', () => {
    assert.strictEqual(isEmail(null), false);
    assert.strictEqual(isEmail(undefined), false);
    assert.strictEqual(isURL(null), false);
    assert.strictEqual(isChinesePhone(undefined), false);
});

test('非字符串输入', () => {
    assert.strictEqual(isEmail(123), false);
    assert.strictEqual(isURL({}), false);
    assert.strictEqual(isChinesePhone([]), false);
});

test('超长输入', () => {
    const longStr = 'a'.repeat(10000);
    assert.strictEqual(isEmail(longStr), false);
    assert.strictEqual(isChinesePhone(longStr), false);
});

// ============== 性能测试 ==============
testGroup('性能测试');

test('Luhn 算法性能 (10000 次)', () => {
    const start = Date.now();
    for (let i = 0; i < 10000; i++) {
        luhnCheck('4111111111111111');
    }
    const elapsed = Date.now() - start;
    console.log(`   耗时: ${elapsed}ms`);
    assert.ok(elapsed < 100, 'Luhn 算法性能应该在 100ms 内');
});

test('邮箱验证性能 (10000 次)', () => {
    const start = Date.now();
    for (let i = 0; i < 10000; i++) {
        isEmail('test@example.com');
    }
    const elapsed = Date.now() - start;
    console.log(`   耗时: ${elapsed}ms`);
    assert.ok(elapsed < 100, '邮箱验证性能应该在 100ms 内');
});

// ============== 输出结果 ==============
console.log('\n' + '='.repeat(50));
console.log(`测试完成: ✅ ${passed} 通过, ❌ ${failed} 失败`);
console.log('='.repeat(50));

process.exit(failed === 0 ? 0 : 1);