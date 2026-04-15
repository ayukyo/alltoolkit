/**
 * 随机工具模块测试
 * 
 * 运行方式: node random_utils_test.js
 */

'use strict';

const assert = require('assert');
const random = require('./mod.js');

// 测试计数器
let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        passed++;
        console.log(`✓ ${name}`);
    } catch (error) {
        failed++;
        console.log(`✗ ${name}`);
        console.log(`  Error: ${error.message}`);
    }
}

function testAsync(name, fn) {
    return fn()
        .then(() => {
            passed++;
            console.log(`✓ ${name}`);
        })
        .catch(error => {
            failed++;
            console.log(`✗ ${name}`);
            console.log(`  Error: ${error.message}`);
        });
}

console.log('\n========================================');
console.log('随机工具模块测试');
console.log('========================================\n');

// ============================================================================
// 常量测试
// ============================================================================

console.log('--- 常量测试 ---');

test('ALPHABET_LOWERCASE 长度正确', () => {
    assert.strictEqual(random.ALPHABET_LOWERCASE.length, 26);
    assert.strictEqual(random.ALPHABET_LOWERCASE, 'abcdefghijklmnopqrstuvwxyz');
});

test('ALPHABET_UPPERCASE 长度正确', () => {
    assert.strictEqual(random.ALPHABET_UPPERCASE.length, 26);
    assert.strictEqual(random.ALPHABET_UPPERCASE, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
});

test('ALPHABET 包含大小写', () => {
    assert.strictEqual(random.ALPHABET.length, 52);
    assert.ok(random.ALPHABET.includes('a'));
    assert.ok(random.ALPHABET.includes('A'));
});

test('DIGITS 长度正确', () => {
    assert.strictEqual(random.DIGITS.length, 10);
    assert.strictEqual(random.DIGITS, '0123456789');
});

test('ALPHANUMERIC 包含字母和数字', () => {
    assert.strictEqual(random.ALPHANUMERIC.length, 62);
});

test('SPECIAL_CHARS 非空', () => {
    assert.ok(random.SPECIAL_CHARS.length > 0);
});

test('HEX_CHARS 长度正确', () => {
    assert.strictEqual(random.HEX_CHARS.length, 16);
});

// ============================================================================
// 基础随机数测试
// ============================================================================

console.log('\n--- 基础随机数测试 ---');

test('randomInt 在范围内', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.randomInt(1, 10);
        assert.ok(result >= 1 && result <= 10);
        assert.ok(Number.isInteger(result));
    }
});

test('randomInt 包含边界值', () => {
    const results = new Set();
    for (let i = 0; i < 1000; i++) {
        results.add(random.randomInt(1, 5));
    }
    assert.ok(results.has(1));
    assert.ok(results.has(5));
});

test('randomInt 边界相等返回该值', () => {
    const result = random.randomInt(5, 5);
    assert.strictEqual(result, 5);
});

test('randomInt 抛出错误：min > max', () => {
    assert.throws(() => random.randomInt(10, 1), /最小值不能大于最大值/);
});

test('randomInt 抛出错误：非数字参数', () => {
    assert.throws(() => random.randomInt('a', 10), /参数必须是数字/);
});

test('randomFloat 在范围内', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.randomFloat(0, 1);
        assert.ok(result >= 0 && result < 1);
    }
});

test('randomFloat 精度控制', () => {
    const result = random.randomFloat(0, 100, 2);
    const decimals = (result.toString().split('.')[1] || '').length;
    assert.ok(decimals <= 2);
});

test('randomFloat 抛出错误：min >= max', () => {
    assert.throws(() => random.randomFloat(1, 1), /最小值必须小于最大值/);
});

test('randomBool 返回布尔值', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.randomBool();
        assert.strictEqual(typeof result, 'boolean');
    }
});

test('randomBool 概率正确', () => {
    let trueCount = 0;
    const trials = 10000;
    for (let i = 0; i < trials; i++) {
        if (random.randomBool(0.7)) trueCount++;
    }
    const ratio = trueCount / trials;
    assert.ok(ratio > 0.65 && ratio < 0.75, `概率 ${ratio} 不在预期范围内`);
});

test('randomBool 抛出错误：无效概率', () => {
    assert.throws(() => random.randomBool(1.5), /概率必须在 0-1 之间/);
});

// ============================================================================
// 随机字符串测试
// ============================================================================

console.log('\n--- 随机字符串测试 ---');

test('randomString 长度正确', () => {
    const result = random.randomString(10);
    assert.strictEqual(result.length, 10);
});

test('randomString 仅小写字母', () => {
    const result = random.randomString(100, { lowercase: true, uppercase: false, digits: false });
    assert.ok(/^[a-z]+$/.test(result));
});

test('randomString 仅大写字母', () => {
    const result = random.randomString(100, { lowercase: false, uppercase: true, digits: false });
    assert.ok(/^[A-Z]+$/.test(result));
});

test('randomString 仅数字', () => {
    const result = random.randomString(100, { lowercase: false, uppercase: false, digits: true });
    assert.ok(/^[0-9]+$/.test(result));
});

test('randomString 包含特殊字符', () => {
    const result = random.randomString(1000, { special: true });
    let hasSpecial = false;
    for (const char of result) {
        if (random.SPECIAL_CHARS.includes(char)) {
            hasSpecial = true;
            break;
        }
    }
    assert.ok(hasSpecial);
});

test('randomString 自定义字符集', () => {
    const result = random.randomString(100, { charset: 'ABC' });
    assert.ok(/^[ABC]+$/.test(result));
});

test('randomString 前缀后缀', () => {
    const result = random.randomString(5, { prefix: 'pre_', suffix: '_suf' });
    assert.ok(result.startsWith('pre_'));
    assert.ok(result.endsWith('_suf'));
    assert.strictEqual(result.length, 5 + 8);
});

test('randomString 抛出错误：负长度', () => {
    assert.throws(() => random.randomString(-1), /长度必须是非负数/);
});

test('randomHex 十六进制字符', () => {
    const result = random.randomHex(20);
    assert.ok(/^[0-9a-f]+$/.test(result));
    assert.strictEqual(result.length, 20);
});

test('randomNumeric 仅数字', () => {
    const result = random.randomNumeric(10);
    assert.ok(/^[0-9]+$/.test(result));
    assert.strictEqual(result.length, 10);
});

test('randomAlpha 仅字母', () => {
    const result = random.randomAlpha(50);
    assert.ok(/^[a-zA-Z]+$/.test(result));
});

test('randomAlpha 仅小写字母', () => {
    const result = random.randomAlpha(50, true);
    assert.ok(/^[a-z]+$/.test(result));
});

test('randomPassword 长度正确', () => {
    const result = random.randomPassword(16);
    assert.strictEqual(result.length, 16);
});

test('randomPassword 包含所有字符类型', () => {
    const result = random.randomPassword(100);
    assert.ok(/[a-z]/.test(result), '缺少小写字母');
    assert.ok(/[A-Z]/.test(result), '缺少大写字母');
    assert.ok(/[0-9]/.test(result), '缺少数字');
    assert.ok(new RegExp(`[${random.SPECIAL_CHARS.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')}]`).test(result), '缺少特殊字符');
});

test('randomPassword 抛出错误：长度太短', () => {
    assert.throws(() => random.randomPassword(3), /密码长度至少为4位/);
});

// ============================================================================
// 随机颜色测试
// ============================================================================

console.log('\n--- 随机颜色测试 ---');

test('randomHexColor 格式正确', () => {
    const result = random.randomHexColor();
    assert.ok(/^#[0-9a-f]{6}$/.test(result));
});

test('randomHexColor 无哈希前缀', () => {
    const result = random.randomHexColor(false);
    assert.ok(/^[0-9a-f]{6}$/.test(result));
});

test('randomRgbColor 值在范围内', () => {
    const result = random.randomRgbColor();
    assert.ok(result.r >= 0 && result.r <= 255);
    assert.ok(result.g >= 0 && result.g <= 255);
    assert.ok(result.b >= 0 && result.b <= 255);
});

test('randomRgbString 格式正确', () => {
    const result = random.randomRgbString();
    assert.ok(/^rgb\(\d+, \d+, \d+\)$/.test(result));
});

test('randomRgbaColor 值在范围内', () => {
    const result = random.randomRgbaColor();
    assert.ok(result.r >= 0 && result.r <= 255);
    assert.ok(result.g >= 0 && result.g <= 255);
    assert.ok(result.b >= 0 && result.b <= 255);
    assert.ok(result.a >= 0 && result.a <= 1);
});

test('randomRgbaColor 固定透明度', () => {
    const result = random.randomRgbaColor(0.5);
    assert.strictEqual(result.a, 0.5);
});

test('randomRgbaString 格式正确', () => {
    const result = random.randomRgbaString();
    assert.ok(/^rgba\(\d+, \d+, \d+, [\d.]+\)$/.test(result));
});

test('randomHslColor 值在范围内', () => {
    const result = random.randomHslColor();
    assert.ok(result.h >= 0 && result.h <= 360);
    assert.ok(result.s >= 0 && result.s <= 100);
    assert.ok(result.l >= 0 && result.l <= 100);
});

test('randomHslString 格式正确', () => {
    const result = random.randomHslString();
    assert.ok(/^hsl\(\d+, \d+%, \d+%\)$/.test(result));
});

// ============================================================================
// UUID 测试
// ============================================================================

console.log('\n--- UUID 测试 ---');

test('uuid 格式正确', () => {
    const result = random.uuid();
    assert.ok(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(result));
});

test('uuid 版本为 4', () => {
    const result = random.uuid();
    assert.strictEqual(result.charAt(14), '4');
});

test('uuid 唯一性', () => {
    const uuids = new Set();
    for (let i = 0; i < 1000; i++) {
        uuids.add(random.uuid());
    }
    assert.strictEqual(uuids.size, 1000);
});

test('shortUuid 无连字符', () => {
    const result = random.shortUuid();
    assert.strictEqual(result.length, 32);
    assert.ok(!result.includes('-'));
});

test('uuidBatch 数量正确', () => {
    const result = random.uuidBatch(10);
    assert.strictEqual(result.length, 10);
    assert.strictEqual(new Set(result).size, 10);
});

test('uuidBatch 抛出错误：负数量', () => {
    assert.throws(() => random.uuidBatch(-1), /数量必须是非负数/);
});

// ============================================================================
// 数组操作测试
// ============================================================================

console.log('\n--- 数组操作测试 ---');

test('randomChoice 返回数组元素', () => {
    const arr = [1, 2, 3, 4, 5];
    for (let i = 0; i < 100; i++) {
        const result = random.randomChoice(arr);
        assert.ok(arr.includes(result));
    }
});

test('randomChoice 抛出错误：空数组', () => {
    assert.throws(() => random.randomChoice([]), /数组必须是非空数组/);
});

test('randomChoices 返回正确数量', () => {
    const arr = [1, 2, 3];
    const result = random.randomChoices(arr, 5);
    assert.strictEqual(result.length, 5);
});

test('randomChoices 可能重复', () => {
    const arr = [1, 2];
    const result = random.randomChoices(arr, 10);
    const unique = new Set(result);
    assert.ok(unique.size < 10); // 应该有重复
});

test('randomSample 返回不重复元素', () => {
    const arr = [1, 2, 3, 4, 5];
    const result = random.randomSample(arr, 3);
    assert.strictEqual(result.length, 3);
    assert.strictEqual(new Set(result).size, 3);
});

test('randomSample 抛出错误：超过数组长度', () => {
    assert.throws(() => random.randomSample([1, 2], 5), /选择数量不能超过数组长度/);
});

test('shuffle 返回所有元素', () => {
    const arr = [1, 2, 3, 4, 5];
    const result = random.shuffle(arr);
    assert.strictEqual(new Set(result).size, 5);
    assert.notDeepStrictEqual(result, [1, 2, 3, 4, 5]); // 可能相等，但概率极低
});

test('shuffle 不修改原数组', () => {
    const arr = [1, 2, 3, 4, 5];
    const copy = [...arr];
    random.shuffle(arr);
    assert.deepStrictEqual(arr, copy);
});

test('shuffleInPlace 修改原数组', () => {
    const arr = [1, 2, 3, 4, 5];
    const result = random.shuffleInPlace(arr);
    assert.strictEqual(arr, result); // 返回同一引用
});

test('shuffle 抛出错误：非数组', () => {
    assert.throws(() => random.shuffle('not array'), /参数必须是数组/);
});

// ============================================================================
// 加权随机测试
// ============================================================================

console.log('\n--- 加权随机测试 ---');

test('weightedChoice 根据权重选择', () => {
    const items = [
        { item: 'A', weight: 1 },
        { item: 'B', weight: 9 }
    ];
    let countA = 0, countB = 0;
    for (let i = 0; i < 1000; i++) {
        const result = random.weightedChoice(items);
        if (result === 'A') countA++;
        else countB++;
    }
    // B 的权重是 A 的 9 倍，所以 B 的概率应该约为 90%
    assert.ok(countB > countA * 5);
});

test('weightedChoice 抛出错误：空数组', () => {
    assert.throws(() => random.weightedChoice([]), /项目数组不能为空/);
});

test('weightedChoice 抛出错误：权重总和为 0', () => {
    assert.throws(() => random.weightedChoice([{ item: 'A', weight: 0 }]), /总权重必须大于0/);
});

test('weightedChoices 返回正确数量', () => {
    const items = [
        { item: 'A', weight: 1 },
        { item: 'B', weight: 1 },
        { item: 'C', weight: 1 }
    ];
    const result = random.weightedChoices(items, 5);
    assert.strictEqual(result.length, 5);
});

test('weightedChoices 不重复选择', () => {
    const items = [
        { item: 'A', weight: 1 },
        { item: 'B', weight: 1 },
        { item: 'C', weight: 1 }
    ];
    const result = random.weightedChoices(items, 3, true);
    assert.strictEqual(new Set(result).size, 3);
});

// ============================================================================
// 概率分布测试
// ============================================================================

console.log('\n--- 概率分布测试 ---');

test('uniform 在范围内', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.uniform(0, 100);
        assert.ok(result >= 0 && result < 100);
    }
});

test('normal 大致符合正态分布', () => {
    const results = [];
    for (let i = 0; i < 1000; i++) {
        results.push(random.normal(50, 10));
    }
    const mean = results.reduce((a, b) => a + b, 0) / results.length;
    assert.ok(mean > 45 && mean < 55, `均值 ${mean} 偏离预期`);
});

test('exponential 大于 0', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.exponential(0.5);
        assert.ok(result >= 0);
    }
});

test('exponential 抛出错误：lambda <= 0', () => {
    assert.throws(() => random.exponential(0), /lambda 必须大于 0/);
    assert.throws(() => random.exponential(-1), /lambda 必须大于 0/);
});

test('poisson 返回非负整数', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.poisson(5);
        assert.ok(Number.isInteger(result) && result >= 0);
    }
});

test('poisson 抛出错误：lambda <= 0', () => {
    assert.throws(() => random.poisson(0), /lambda 必须大于 0/);
});

// ============================================================================
// 随机日期时间测试
// ============================================================================

console.log('\n--- 随机日期时间测试 ---');

test('randomDate 在范围内', () => {
    const start = new Date('2020-01-01');
    const end = new Date('2023-12-31');
    for (let i = 0; i < 100; i++) {
        const result = random.randomDate(start, end);
        assert.ok(result >= start && result <= end);
    }
});

test('randomDate 默认范围', () => {
    const now = new Date();
    const result = random.randomDate();
    assert.ok(result >= new Date(0) && result <= now);
});

test('randomDate 抛出错误：开始晚于结束', () => {
    assert.throws(() => random.randomDate('2023-01-01', '2020-01-01'), /开始日期必须早于结束日期/);
});

test('randomTime 格式正确', () => {
    const result = random.randomTime();
    assert.ok(/^\d{2}:\d{2}$/.test(result));
});

test('randomTime 包含秒', () => {
    const result = random.randomTime(true);
    assert.ok(/^\d{2}:\d{2}:\d{2}$/.test(result));
});

test('randomDatetime 格式正确', () => {
    const result = random.randomDatetime();
    assert.ok(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(result));
});

// ============================================================================
// 加密安全随机测试
// ============================================================================

console.log('\n--- 加密安全随机测试 ---');

test('cryptoRandomInt 在范围内', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.cryptoRandomInt(1, 100);
        assert.ok(result >= 1 && result <= 100);
        assert.ok(Number.isInteger(result));
    }
});

test('cryptoRandomString 长度正确', () => {
    const result = random.cryptoRandomString(32);
    assert.strictEqual(result.length, 32);
});

test('cryptoRandomString 仅字母数字', () => {
    const result = random.cryptoRandomString(100);
    assert.ok(/^[a-zA-Z0-9]+$/.test(result));
});

test('cryptoRandomBytes 返回 Buffer', () => {
    const result = random.cryptoRandomBytes(16);
    assert.ok(Buffer.isBuffer(result));
    assert.strictEqual(result.length, 16);
});

// ============================================================================
// 其他实用函数测试
// ============================================================================

console.log('\n--- 其他实用函数测试 ---');

test('randomEnum 返回枚举值', () => {
    const Status = { PENDING: 'pending', ACTIVE: 'active', DONE: 'done' };
    const values = Object.values(Status);
    for (let i = 0; i < 100; i++) {
        const result = random.randomEnum(Status);
        assert.ok(values.includes(result));
    }
});

test('randomIPv4 格式正确', () => {
    const result = random.randomIPv4();
    assert.ok(/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(result));
    const parts = result.split('.').map(Number);
    parts.forEach(part => {
        assert.ok(part >= 0 && part <= 255);
    });
});

test('randomMAC 格式正确', () => {
    const result = random.randomMAC();
    assert.ok(/^([0-9A-F]{2}:){5}[0-9A-F]{2}$/.test(result));
});

test('randomMAC 自定义分隔符', () => {
    const result = random.randomMAC('-');
    assert.ok(result.includes('-'));
    assert.ok(!result.includes(':'));
});

test('randomPort 在范围内', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.randomPort();
        assert.ok(result >= 1 && result <= 65535);
    }
});

test('randomPort 知名端口', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.randomPort(true);
        assert.ok(result >= 1 && result <= 1023);
    }
});

test('randomUsername 长度正确', () => {
    for (let i = 0; i < 100; i++) {
        const result = random.randomUsername();
        assert.ok(result.length >= 5 && result.length <= 15);
        assert.ok(/^[a-z][a-z0-9]*$/.test(result));
    }
});

test('randomEmail 格式正确', () => {
    const result = random.randomEmail();
    assert.ok(/^[a-z][a-z0-9]*@[a-z]+\.[a-z]+$/.test(result));
});

test('randomEmail 自定义域名', () => {
    const result = random.randomEmail(['test.com']);
    assert.ok(result.endsWith('@test.com'));
});

test('randomUrl 格式正确', () => {
    const result = random.randomUrl();
    assert.ok(/^https?:\/\/.*/.test(result));
});

test('randomChinesePhone 格式正确', () => {
    const result = random.randomChinesePhone();
    assert.strictEqual(result.length, 11);
    assert.ok(/^1[3-9]\d{9}$/.test(result));
});

test('randomDelay 延迟执行', async () => {
    const start = Date.now();
    await random.randomDelay(10, 50);
    const elapsed = Date.now() - start;
    assert.ok(elapsed >= 10 && elapsed <= 100); // 允许一定误差
});

// ============================================================================
// 统计测试
// ============================================================================

console.log('\n--- 统计测试 ---');

test('randomInt 分布均匀', () => {
    const counts = {};
    const trials = 10000;
    for (let i = 0; i < trials; i++) {
        const val = random.randomInt(1, 6);
        counts[val] = (counts[val] || 0) + 1;
    }
    // 每个数字应该出现约 16.67%
    for (let i = 1; i <= 6; i++) {
        const ratio = counts[i] / trials;
        assert.ok(ratio > 0.14 && ratio < 0.20, `数字 ${i} 比例 ${ratio} 偏离预期`);
    }
});

test('normal 标准差', () => {
    const results = [];
    for (let i = 0; i < 10000; i++) {
        results.push(random.normal(0, 1));
    }
    const mean = results.reduce((a, b) => a + b, 0) / results.length;
    const variance = results.reduce((sum, x) => sum + (x - mean) ** 2, 0) / results.length;
    const stdDev = Math.sqrt(variance);
    assert.ok(mean > -0.1 && mean < 0.1, `均值 ${mean} 偏离预期`);
    assert.ok(stdDev > 0.9 && stdDev < 1.1, `标准差 ${stdDev} 偏离预期`);
});

// ============================================================================
// 运行异步测试
// ============================================================================

(async () => {
    await testAsync('randomDelay 异步测试', async () => {
        await random.randomDelay(5, 10);
    });
    
    // 输出结果
    console.log('\n========================================');
    console.log(`测试完成: ${passed} 通过, ${failed} 失败`);
    console.log('========================================\n');
    
    if (failed > 0) {
        process.exit(1);
    }
})();