/**
 * SemVer Utils 测试文件
 * 
 * 运行方式：node semver_utils_test.js
 */

const assert = require('assert');
const { SemVer, SemVerUtils } = require('./mod.js');

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

// ============== 解析测试 ==============
testGroup('版本解析测试');

test('解析标准版本', () => {
    const v = SemVerUtils.parse('1.2.3');
    assert.strictEqual(v.major, 1);
    assert.strictEqual(v.minor, 2);
    assert.strictEqual(v.patch, 3);
    assert.strictEqual(v.prerelease.length, 0);
    assert.strictEqual(v.build.length, 0);
});

test('解析带预发布版本', () => {
    const v = SemVerUtils.parse('1.2.3-alpha.1');
    assert.strictEqual(v.major, 1);
    assert.strictEqual(v.minor, 2);
    assert.strictEqual(v.patch, 3);
    assert.deepStrictEqual(v.prerelease, ['alpha', '1']);
});

test('解析带构建元数据', () => {
    const v = SemVerUtils.parse('1.2.3+build.123');
    assert.strictEqual(v.major, 1);
    assert.strictEqual(v.minor, 2);
    assert.strictEqual(v.patch, 3);
    assert.deepStrictEqual(v.build, ['build', '123']);
});

test('解析完整版本', () => {
    const v = SemVerUtils.parse('1.2.3-beta.2+build.456');
    assert.strictEqual(v.major, 1);
    assert.strictEqual(v.minor, 2);
    assert.strictEqual(v.patch, 3);
    assert.deepStrictEqual(v.prerelease, ['beta', '2']);
    assert.deepStrictEqual(v.build, ['build', '456']);
});

test('解析带 v 前缀', () => {
    const v = SemVerUtils.parse('v1.2.3');
    assert.strictEqual(v.major, 1);
    assert.strictEqual(v.minor, 2);
    assert.strictEqual(v.patch, 3);
});

test('解析无效版本返回 null', () => {
    assert.strictEqual(SemVerUtils.parse(''), null);
    assert.strictEqual(SemVerUtils.parse('invalid'), null);
    assert.strictEqual(SemVerUtils.parse('1'), null);
    assert.strictEqual(SemVerUtils.parse('1.2'), null);
    assert.strictEqual(SemVerUtils.parse(null), null);
    assert.strictEqual(SemVerUtils.parse(undefined), null);
});

test('tryParse 无效版本返回默认', () => {
    const v = SemVerUtils.tryParse('invalid', '0.0.0');
    assert.strictEqual(v.major, 0);
    assert.strictEqual(v.minor, 0);
    assert.strictEqual(v.patch, 0);
});

test('版本验证', () => {
    assert.strictEqual(SemVerUtils.isValid('1.2.3'), true);
    assert.strictEqual(SemVerUtils.isValid('v1.2.3'), true);
    assert.strictEqual(SemVerUtils.isValid('1.2.3-alpha'), true);
    assert.strictEqual(SemVerUtils.isValid('invalid'), false);
});

test('清理版本字符串', () => {
    assert.strictEqual(SemVerUtils.clean('v1.2.3-alpha'), '1.2.3-alpha');
    assert.strictEqual(SemVerUtils.clean('  1.2.3+build  '), '1.2.3');
    assert.strictEqual(SemVerUtils.clean('invalid'), null);
});

// ============== SemVer 类测试 ==============
testGroup('SemVer 类测试');

test('toString 方法', () => {
    const v = new SemVer(1, 2, 3, ['alpha', '1'], ['build']);
    assert.strictEqual(v.toString(), '1.2.3-alpha.1+build');
});

test('toCleanString 方法', () => {
    const v = new SemVer(1, 2, 3, ['alpha'], ['build']);
    assert.strictEqual(v.toCleanString(), '1.2.3-alpha');
});

test('toJSON 方法', () => {
    const v = new SemVer(1, 2, 3);
    const json = v.toJSON();
    assert.strictEqual(json.major, 1);
    assert.strictEqual(json.minor, 2);
    assert.strictEqual(json.patch, 3);
    assert.strictEqual(json.version, '1.2.3');
});

test('clone 方法', () => {
    const v1 = new SemVer(1, 2, 3, ['alpha']);
    const v2 = v1.clone();
    assert.strictEqual(v1.toString(), v2.toString());
    v2.patch = 4;
    assert.strictEqual(v1.patch, 3);
    assert.strictEqual(v2.patch, 4);
});

test('isPrerelease 方法', () => {
    assert.strictEqual(new SemVer(1, 2, 3).isPrerelease(), false);
    assert.strictEqual(new SemVer(1, 2, 3, ['alpha']).isPrerelease(), true);
});

test('isStable 方法', () => {
    assert.strictEqual(new SemVer(0, 1, 0).isStable(), false);
    assert.strictEqual(new SemVer(1, 0, 0).isStable(), true);
    assert.strictEqual(new SemVer(1, 0, 0, ['beta']).isStable(), false);
});

// ============== 比较测试 ==============
testGroup('版本比较测试');

test('比较主版本号', () => {
    assert.strictEqual(SemVerUtils.compare('2.0.0', '1.0.0'), 1);
    assert.strictEqual(SemVerUtils.compare('1.0.0', '2.0.0'), -1);
    assert.strictEqual(SemVerUtils.compare('1.0.0', '1.0.0'), 0);
});

test('比较次版本号', () => {
    assert.strictEqual(SemVerUtils.compare('1.2.0', '1.1.0'), 1);
    assert.strictEqual(SemVerUtils.compare('1.1.0', '1.2.0'), -1);
});

test('比较修订版本号', () => {
    assert.strictEqual(SemVerUtils.compare('1.0.2', '1.0.1'), 1);
    assert.strictEqual(SemVerUtils.compare('1.0.1', '1.0.2'), -1);
});

test('预发布版本比较', () => {
    assert.strictEqual(SemVerUtils.compare('1.0.0-alpha', '1.0.0-beta'), -1);
    assert.strictEqual(SemVerUtils.compare('1.0.0-beta', '1.0.0-alpha'), 1);
});

test('预发布版本与正式版本比较', () => {
    assert.strictEqual(SemVerUtils.compare('1.0.0', '1.0.0-alpha'), 1);
    assert.strictEqual(SemVerUtils.compare('1.0.0-alpha', '1.0.0'), -1);
});

test('预发布标识数字比较', () => {
    assert.strictEqual(SemVerUtils.compare('1.0.0-alpha.1', '1.0.0-alpha.2'), -1);
    assert.strictEqual(SemVerUtils.compare('1.0.0-alpha.2', '1.0.0-alpha.1'), 1);
});

test('数字标识符小于字符串标识符', () => {
    assert.strictEqual(SemVerUtils.compare('1.0.0-alpha.1', '1.0.0-alpha.beta'), -1);
});

test('eq 相等比较', () => {
    assert.strictEqual(SemVerUtils.eq('1.2.3', '1.2.3'), true);
    assert.strictEqual(SemVerUtils.eq('1.2.3', '1.2.4'), false);
});

test('neq 不等比较', () => {
    assert.strictEqual(SemVerUtils.neq('1.2.3', '1.2.3'), false);
    assert.strictEqual(SemVerUtils.neq('1.2.3', '1.2.4'), true);
});

test('gt 大于比较', () => {
    assert.strictEqual(SemVerUtils.gt('2.0.0', '1.0.0'), true);
    assert.strictEqual(SemVerUtils.gt('1.0.0', '2.0.0'), false);
});

test('gte 大于等于比较', () => {
    assert.strictEqual(SemVerUtils.gte('1.2.3', '1.2.3'), true);
    assert.strictEqual(SemVerUtils.gte('1.2.4', '1.2.3'), true);
    assert.strictEqual(SemVerUtils.gte('1.2.2', '1.2.3'), false);
});

test('lt 小于比较', () => {
    assert.strictEqual(SemVerUtils.lt('1.0.0', '2.0.0'), true);
    assert.strictEqual(SemVerUtils.lt('2.0.0', '1.0.0'), false);
});

test('lte 小于等于比较', () => {
    assert.strictEqual(SemVerUtils.lte('1.2.3', '1.2.3'), true);
    assert.strictEqual(SemVerUtils.lte('1.2.2', '1.2.3'), true);
    assert.strictEqual(SemVerUtils.lte('1.2.4', '1.2.3'), false);
});

test('isCompatible 兼容版本检查', () => {
    assert.strictEqual(SemVerUtils.isCompatible('1.2.3', '1.3.0'), true);
    assert.strictEqual(SemVerUtils.isCompatible('1.2.3', '2.0.0'), false);
    assert.strictEqual(SemVerUtils.isCompatible('0.1.0', '0.1.1'), true);
    assert.strictEqual(SemVerUtils.isCompatible('0.1.0', '0.2.0'), false);
});

// ============== 版本递增测试 ==============
testGroup('版本递增测试');

test('递增主版本号', () => {
    const v = SemVerUtils.incMajor('1.2.3');
    assert.strictEqual(v.toString(), '2.0.0');
});

test('递增次版本号', () => {
    const v = SemVerUtils.incMinor('1.2.3');
    assert.strictEqual(v.toString(), '1.3.0');
});

test('递增修订版本号', () => {
    const v = SemVerUtils.incPatch('1.2.3');
    assert.strictEqual(v.toString(), '1.2.4');
});

test('递增主版本号时清除预发布', () => {
    const v = SemVerUtils.incMajor('1.2.3-alpha');
    assert.strictEqual(v.toString(), '2.0.0');
});

test('递增预发布版本', () => {
    const v = SemVerUtils.incPrerelease('1.2.3', 'alpha');
    assert.strictEqual(v.toString(), '1.2.3-alpha.1');
});

test('递增已有预发布版本', () => {
    const v = SemVerUtils.incPrerelease('1.2.3-alpha.1');
    assert.strictEqual(v.toString(), '1.2.3-alpha.2');
});

test('设置预发布版本', () => {
    const v = SemVerUtils.setPrerelease('1.2.3', 'beta.1');
    assert.strictEqual(v.toString(), '1.2.3-beta.1');
});

test('设置构建元数据', () => {
    const v = SemVerUtils.setBuild('1.2.3', 'build.123');
    assert.strictEqual(v.toString(), '1.2.3+build.123');
});

// ============== 版本范围测试 ==============
testGroup('版本范围测试');

test('精确版本匹配', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.4', '1.2.3'), false);
});

test('插入符号范围 (^)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '^1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.4', '^1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.3.0', '^1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('2.0.0', '^1.2.3'), false);
});

test('插入符号范围 (^0.x)', () => {
    assert.strictEqual(SemVerUtils.satisfies('0.2.3', '^0.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('0.2.4', '^0.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('0.3.0', '^0.2.3'), false);
});

test('插入符号范围 (^0.0.x)', () => {
    assert.strictEqual(SemVerUtils.satisfies('0.0.3', '^0.0.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('0.0.4', '^0.0.3'), false);
});

test('波浪号范围 (~)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '~1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.4', '~1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.5', '~1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.3.0', '~1.2.3'), false);
});

test('比较符范围 (>=)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.4', '>=1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '>=1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.2', '>=1.2.3'), false);
});

test('比较符范围 (<)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.2', '<1.2.3'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '<1.2.3'), false);
});

test('比较符范围 (> <)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.4', '>1.2.0 <2.0.0'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.0.0', '>1.2.0 <2.0.0'), false);
    assert.strictEqual(SemVerUtils.satisfies('2.0.0', '>1.2.0 <2.0.0'), false);
});

test('连字符范围 (1.0.0 - 2.0.0)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.5.0', '1.0.0 - 2.0.0'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.0.0', '1.0.0 - 2.0.0'), true);
    assert.strictEqual(SemVerUtils.satisfies('2.0.0', '1.0.0 - 2.0.0'), true);
    assert.strictEqual(SemVerUtils.satisfies('0.9.0', '1.0.0 - 2.0.0'), false);
    assert.strictEqual(SemVerUtils.satisfies('2.1.0', '1.0.0 - 2.0.0'), false);
});

test('通配符 (*)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '*'), true);
    assert.strictEqual(SemVerUtils.satisfies('100.200.300', '*'), true);
});

test('主版本通配 (1.*)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '1.*'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.100.100', '1.*'), true);
    assert.strictEqual(SemVerUtils.satisfies('2.0.0', '1.*'), false);
});

test('次版本通配 (1.2.*)', () => {
    assert.strictEqual(SemVerUtils.satisfies('1.2.3', '1.2.*'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.2.100', '1.2.*'), true);
    assert.strictEqual(SemVerUtils.satisfies('1.3.0', '1.2.*'), false);
});

// ============== 排序测试 ==============
testGroup('排序测试');

test('排序版本列表', () => {
    const versions = ['1.2.3', '2.0.0', '1.0.0', '1.2.4'];
    const sorted = SemVerUtils.sort(versions);
    assert.strictEqual(sorted[0].toString(), '1.0.0');
    assert.strictEqual(sorted[1].toString(), '1.2.3');
    assert.strictEqual(sorted[2].toString(), '1.2.4');
    assert.strictEqual(sorted[3].toString(), '2.0.0');
});

test('降序排序', () => {
    const versions = ['1.2.3', '2.0.0', '1.0.0'];
    const sorted = SemVerUtils.sort(versions, { desc: true });
    assert.strictEqual(sorted[0].toString(), '2.0.0');
    assert.strictEqual(sorted[1].toString(), '1.2.3');
    assert.strictEqual(sorted[2].toString(), '1.0.0');
});

test('排序预发布版本', () => {
    const versions = ['1.0.0', '1.0.0-alpha', '1.0.0-beta', '1.0.0-alpha.1'];
    const sorted = SemVerUtils.sort(versions);
    // 根据 SemVer 规范: alpha < alpha.1 (较短数组优先)
    assert.strictEqual(sorted[0].toString(), '1.0.0-alpha');
    assert.strictEqual(sorted[1].toString(), '1.0.0-alpha.1');
    assert.strictEqual(sorted[2].toString(), '1.0.0-beta');
    assert.strictEqual(sorted[3].toString(), '1.0.0');
});

test('获取最大版本', () => {
    const versions = ['1.0.0', '2.0.0', '1.5.0'];
    const max = SemVerUtils.maxSatisfying(versions);
    assert.strictEqual(max.toString(), '2.0.0');
});

test('获取最小版本', () => {
    const versions = ['1.0.0', '2.0.0', '1.5.0'];
    const min = SemVerUtils.minSatisfying(versions);
    assert.strictEqual(min.toString(), '1.0.0');
});

test('过滤满足范围的版本', () => {
    const versions = ['1.0.0', '1.2.3', '1.5.0', '2.0.0'];
    const filtered = SemVerUtils.filterSatisfying(versions, '^1.2.0');
    assert.strictEqual(filtered.length, 2);
    assert.strictEqual(filtered[0].toString(), '1.2.3');
    assert.strictEqual(filtered[1].toString(), '1.5.0');
});

test('获取范围内最大版本', () => {
    const versions = ['1.0.0', '1.2.3', '1.5.0', '1.8.0', '2.0.0'];
    const max = SemVerUtils.maxSatisfyingInRange(versions, '^1.2.0');
    assert.strictEqual(max.toString(), '1.8.0');
});

// ============== 工具方法测试 ==============
testGroup('工具方法测试');

test('diff 差异类型', () => {
    assert.strictEqual(SemVerUtils.diff('1.2.3', '2.0.0'), 'major');
    assert.strictEqual(SemVerUtils.diff('1.2.3', '1.3.0'), 'minor');
    assert.strictEqual(SemVerUtils.diff('1.2.3', '1.2.4'), 'patch');
    assert.strictEqual(SemVerUtils.diff('1.2.3-alpha', '1.2.3-beta'), 'prerelease');
    assert.strictEqual(SemVerUtils.diff('1.2.3', '1.2.3'), null);
});

test('getChangeType 变更类型', () => {
    const upgrade = SemVerUtils.getChangeType('1.2.3', '2.0.0');
    assert.strictEqual(upgrade.direction, 'upgrade');
    assert.strictEqual(upgrade.type, 'major');

    const downgrade = SemVerUtils.getChangeType('2.0.0', '1.2.3');
    assert.strictEqual(downgrade.direction, 'downgrade');
    assert.strictEqual(downgrade.type, 'major');

    const same = SemVerUtils.getChangeType('1.2.3', '1.2.3');
    assert.strictEqual(same.direction, 'same');
    assert.strictEqual(same.type, null);
});

test('analyze 版本分析', () => {
    const info = SemVerUtils.analyze('1.2.3-alpha.1+build.123');
    assert.strictEqual(info.major, 1);
    assert.strictEqual(info.minor, 2);
    assert.strictEqual(info.patch, 3);
    assert.deepStrictEqual(info.prerelease, ['alpha', '1']);
    assert.deepStrictEqual(info.build, ['build', '123']);
    assert.strictEqual(info.isPrerelease, true);
    assert.strictEqual(info.isStable, false);
});

test('analyze 稳定版本分析', () => {
    const info = SemVerUtils.analyze('1.0.0');
    assert.strictEqual(info.isPrerelease, false);
    assert.strictEqual(info.isStable, true);
    assert.strictEqual(info.level, 'stable');
});

test('analyze 实验版本分析', () => {
    const info = SemVerUtils.analyze('0.1.0');
    assert.strictEqual(info.level, 'experimental');
});

test('validateAll 批量验证', () => {
    const versions = ['1.2.3', 'invalid', '2.0.0-beta', 'another-invalid', '1.0.0'];
    const result = SemVerUtils.validateAll(versions);
    assert.strictEqual(result.valid.length, 3);
    assert.strictEqual(result.invalid.length, 2);
    assert.strictEqual(result.stable.length, 2);
    assert.strictEqual(result.prerelease.length, 1);
});

// ============== SemVer 实例方法测试 ==============
testGroup('SemVer 实例方法测试');

test('SemVer 实例比较', () => {
    const v1 = new SemVer(1, 2, 3);
    const v2 = new SemVer(1, 2, 4);
    assert.strictEqual(v1.lt(v2), true);
    assert.strictEqual(v1.gt(v2), false);
    assert.strictEqual(v1.eq(v2), false);
});

test('SemVer 实例与字符串比较', () => {
    const v = new SemVer(1, 2, 3);
    assert.strictEqual(v.eq('1.2.3'), true);
    assert.strictEqual(v.lt('2.0.0'), true);
    assert.strictEqual(v.gt('1.0.0'), true);
});

// ============== 边界条件测试 ==============
testGroup('边界条件测试');

test('null 和 undefined 输入', () => {
    assert.strictEqual(SemVerUtils.parse(null), null);
    assert.strictEqual(SemVerUtils.parse(undefined), null);
    assert.strictEqual(SemVerUtils.isValid(null), false);
});

test('空字符串', () => {
    assert.strictEqual(SemVerUtils.parse(''), null);
    assert.strictEqual(SemVerUtils.isValid(''), false);
});

test('超大版本号', () => {
    const v = SemVerUtils.parse('1000.2000.3000');
    assert.strictEqual(v.major, 1000);
    assert.strictEqual(v.minor, 2000);
    assert.strictEqual(v.patch, 3000);
});

test('复杂预发布标识', () => {
    const v = SemVerUtils.parse('1.0.0-alpha.beta.1.2.3');
    assert.deepStrictEqual(v.prerelease, ['alpha', 'beta', '1', '2', '3']);
});

test('复杂构建元数据', () => {
    const v = SemVerUtils.parse('1.0.0+build.123.sha.abc123');
    assert.deepStrictEqual(v.build, ['build', '123', 'sha', 'abc123']);
});

// ============== 性能测试 ==============
testGroup('性能测试');

test('解析性能 (10000 次)', () => {
    const start = Date.now();
    for (let i = 0; i < 10000; i++) {
        SemVerUtils.parse('1.2.3-alpha.1+build.123');
    }
    const elapsed = Date.now() - start;
    console.log(`   耗时: ${elapsed}ms`);
    assert.ok(elapsed < 200, '解析性能应该在 200ms 内');
});

test('比较性能 (10000 次)', () => {
    const v1 = '1.2.3';
    const v2 = '1.2.4';
    const start = Date.now();
    for (let i = 0; i < 10000; i++) {
        SemVerUtils.compare(v1, v2);
    }
    const elapsed = Date.now() - start;
    console.log(`   耗时: ${elapsed}ms`);
    assert.ok(elapsed < 100, '比较性能应该在 100ms 内');
});

test('范围匹配性能 (10000 次)', () => {
    const start = Date.now();
    for (let i = 0; i < 10000; i++) {
        SemVerUtils.satisfies('1.2.5', '^1.2.0');
    }
    const elapsed = Date.now() - start;
    console.log(`   耗时: ${elapsed}ms`);
    assert.ok(elapsed < 200, '范围匹配性能应该在 200ms 内');
});

// ============== 输出结果 ==============
console.log('\n' + '='.repeat(50));
console.log(`测试完成: ✅ ${passed} 通过, ❌ ${failed} 失败`);
console.log('='.repeat(50));

process.exit(failed === 0 ? 0 : 1);