/**
 * 随机工具模块使用示例
 * 
 * 运行方式: node example_usage.js
 */

'use strict';

const random = require('../mod.js');

console.log('\n========================================');
console.log('JavaScript 随机工具模块 - 使用示例');
console.log('========================================\n');

// ============================================================================
// 1. 基础随机数示例
// ============================================================================

console.log('--- 1. 基础随机数 ---');

console.log('随机整数 (1-100):', random.randomInt(1, 100));
console.log('随机整数 (骰子 1-6):', random.randomInt(1, 6));
console.log('随机浮点数 (0-1):', random.randomFloat(0, 1));
console.log('随机浮点数 (0-100, 2位小数):', random.randomFloat(0, 100, 2));
console.log('随机布尔值:', random.randomBool());
console.log('随机布尔值 (80% true):', random.randomBool(0.8));

// ============================================================================
// 2. 随机字符串示例
// ============================================================================

console.log('\n--- 2. 随机字符串 ---');

console.log('随机字符串 (16位):', random.randomString(16));
console.log('仅小写字母 (10位):', random.randomString(10, { lowercase: true, uppercase: false, digits: false }));
console.log('仅大写字母 (10位):', random.randomString(10, { lowercase: false, uppercase: true, digits: false }));
console.log('仅数字 (10位):', random.randomNumeric(10));
console.log('包含特殊字符 (20位):', random.randomString(20, { special: true }));
console.log('自定义字符集 (ABC):', random.randomString(10, { charset: 'ABC' }));
console.log('带前缀后缀:', random.randomString(5, { prefix: 'user_', suffix: '_end' }));
console.log('随机十六进制:', random.randomHex(16));
console.log('随机字母:', random.randomAlpha(10));
console.log('随机字母 (仅小写):', random.randomAlpha(10, true));
console.log('强密码 (16位):', random.randomPassword(16));
console.log('强密码 (20位):', random.randomPassword(20));

// ============================================================================
// 3. 随机颜色示例
// ============================================================================

console.log('\n--- 3. 随机颜色 ---');

console.log('随机 HEX 颜色:', random.randomHexColor());
console.log('随机 HEX 颜色 (无#):', random.randomHexColor(false));
console.log('随机 RGB:', random.randomRgbColor());
console.log('随机 RGB 字符串:', random.randomRgbString());
console.log('随机 RGBA:', random.randomRgbaColor());
console.log('随机 RGBA 字符串:', random.randomRgbaString());
console.log('随机 RGBA (固定透明度):', random.randomRgbaString(0.5));
console.log('随机 HSL:', random.randomHslColor());
console.log('随机 HSL 字符串:', random.randomHslString());

// ============================================================================
// 4. UUID 示例
// ============================================================================

console.log('\n--- 4. UUID ---');

console.log('UUID v4:', random.uuid());
console.log('短 UUID:', random.shortUuid());
console.log('批量 UUID (5个):', random.uuidBatch(5));

// ============================================================================
// 5. 数组操作示例
// ============================================================================

console.log('\n--- 5. 数组操作 ---');

const fruits = ['苹果', '香蕉', '橙子', '葡萄', '西瓜', '芒果'];
console.log('水果列表:', fruits);
console.log('随机选择一个:', random.randomChoice(fruits));
console.log('随机选择多个 (可重复, 5个):', random.randomChoices(fruits, 5));
console.log('随机采样 (不重复, 3个):', random.randomSample(fruits, 3));
console.log('打乱顺序:', random.shuffle(fruits));
console.log('原数组未改变:', fruits);

const numbers = [1, 2, 3, 4, 5];
console.log('\n数字列表:', numbers);
const shuffled = random.shuffle(numbers);
console.log('洗牌后:', shuffled);

// ============================================================================
// 6. 加权随机示例
// ============================================================================

console.log('\n--- 6. 加权随机 ---');

const lootItems = [
    { item: '钻石', weight: 1 },
    { item: '金币', weight: 30 },
    { item: '银币', weight: 50 },
    { item: '铜币', weight: 100 }
];

console.log('宝箱掉落概率:');
console.log('  钻石: 1%');
console.log('  金币: 16%');
console.log('  银币: 26%');
console.log('  铜币: 57%');

console.log('\n模拟开宝箱 10 次:');
for (let i = 0; i < 10; i++) {
    console.log(`  第 ${i + 1} 次: ${random.weightedChoice(lootItems)}`);
}

// ============================================================================
// 7. 概率分布示例
// ============================================================================

console.log('\n--- 7. 概率分布 ---');

console.log('均匀分布 (0-100):', random.uniform(0, 100));

console.log('\n正态分布 (均值=50, 标准差=10):');
const normalSamples = Array.from({ length: 10 }, () => random.normal(50, 10).toFixed(2));
console.log('  10 个样本:', normalSamples.join(', '));

console.log('\n指数分布 (lambda=0.5):');
const expSamples = Array.from({ length: 5 }, () => random.exponential(0.5).toFixed(2));
console.log('  5 个样本:', expSamples.join(', '));

console.log('\n泊松分布 (lambda=5):');
const poissonSamples = Array.from({ length: 10 }, () => random.poisson(5));
console.log('  10 个样本:', poissonSamples.join(', '));

// ============================================================================
// 8. 随机日期时间示例
// ============================================================================

console.log('\n--- 8. 随机日期时间 ---');

console.log('随机日期 (1970-至今):', random.randomDate().toISOString().split('T')[0]);
console.log('随机日期 (2020-2023):', random.randomDate('2020-01-01', '2023-12-31').toISOString().split('T')[0]);
console.log('随机时间:', random.randomTime());
console.log('随机时间 (含秒):', random.randomTime(true));
console.log('随机日期时间:', random.randomDatetime());

// ============================================================================
// 9. 加密安全随机示例
// ============================================================================

console.log('\n--- 9. 加密安全随机 ---');

console.log('加密安全整数 (1-100):', random.cryptoRandomInt(1, 100));
console.log('加密安全字符串 (32位):', random.cryptoRandomString(32));
console.log('加密安全字节 (16字节):', random.cryptoRandomBytes(16).toString('hex'));

// ============================================================================
// 10. 其他实用函数示例
// ============================================================================

console.log('\n--- 10. 其他实用函数 ---');

const Status = { PENDING: '待处理', ACTIVE: '进行中', DONE: '已完成', FAILED: '失败' };
console.log('随机状态:', random.randomEnum(Status));

console.log('随机 IPv4:', random.randomIPv4());
console.log('随机 MAC:', random.randomMAC());
console.log('随机 MAC (-分隔):', random.randomMAC('-'));
console.log('随机端口:', random.randomPort());
console.log('随机知名端口:', random.randomPort(true));
console.log('随机用户名:', random.randomUsername());
console.log('随机邮箱:', random.randomEmail());
console.log('随机邮箱 (自定义域名):', random.randomEmail(['company.cn', 'corp.com']));
console.log('随机 URL:', random.randomUrl());
console.log('随机中国手机号:', random.randomChinesePhone());

// ============================================================================
// 11. 综合应用示例
// ============================================================================

console.log('\n--- 11. 综合应用 ---');

// 模拟用户数据生成
console.log('\n生成 5 个模拟用户:');
for (let i = 0; i < 5; i++) {
    const user = {
        id: random.uuid(),
        username: random.randomUsername(),
        email: random.randomEmail(),
        age: random.randomInt(18, 60),
        color: random.randomHexColor(),
        registered: random.randomDate('2020-01-01', '2023-12-31').toISOString().split('T')[0],
        status: random.randomEnum(Status)
    };
    console.log(`  用户 ${i + 1}:`, JSON.stringify(user, null, 2));
}

// 模拟抽奖
console.log('\n模拟抽奖系统:');
const prizes = [
    { item: '一等奖 - iPhone', weight: 1 },
    { item: '二等奖 - iPad', weight: 5 },
    { item: '三等奖 - AirPods', weight: 20 },
    { item: '安慰奖 - 贴纸', weight: 100 },
    { item: '未中奖', weight: 500 }
];

console.log('抽奖 10 次:');
const results = random.weightedChoices(prizes, 10);
results.forEach((prize, i) => {
    console.log(`  第 ${i + 1} 次: ${prize}`);
});

// 统计分布演示
console.log('\n正态分布统计演示:');
const sampleCount = 1000;
const samples = Array.from({ length: sampleCount }, () => random.normal(100, 15));
const mean = samples.reduce((a, b) => a + b, 0) / sampleCount;
const min = Math.min(...samples);
const max = Math.max(...samples);

console.log(`  样本数量: ${sampleCount}`);
console.log(`  均值: ${mean.toFixed(2)} (预期: 100)`);
console.log(`  最小值: ${min.toFixed(2)}`);
console.log(`  最大值: ${max.toFixed(2)}`);

console.log('\n========================================');
console.log('示例演示完成');
console.log('========================================\n');