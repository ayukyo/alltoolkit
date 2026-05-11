/**
 * SemVer Utils 使用示例
 * 
 * 运行方式：node usage_examples.js
 */

const { SemVer, SemVerUtils } = require('../mod.js');

console.log('='.repeat(60));
console.log('SemVer Utils - 语义化版本工具使用示例');
console.log('='.repeat(60));

// ============== 1. 版本解析 ==============
console.log('\n【1. 版本解析】');

const v1 = SemVerUtils.parse('1.2.3');
console.log(`解析 '1.2.3': major=${v1.major}, minor=${v1.minor}, patch=${v1.patch}`);

const v2 = SemVerUtils.parse('v2.0.0-beta.1+build.123');
console.log(`解析 'v2.0.0-beta.1+build.123':`);
console.log(`  - 版本: ${v2.toString()}`);
console.log(`  - 简洁版: ${v2.toCleanString()}`);
console.log(`  - 预发布: ${v2.prerelease.join(', ')}`);
console.log(`  - 构建: ${v2.build.join(', ')}`);

// 无效版本处理
const invalid = SemVerUtils.parse('invalid');
console.log(`解析无效版本 'invalid': ${invalid === null ? 'null' : invalid}`);

const tryParsed = SemVerUtils.tryParse('invalid', '0.0.0');
console.log(`tryParse 无效版本（默认 0.0.0）: ${tryParsed.toString()}`);

// ============== 2. 版本验证与清理 ==============
console.log('\n【2. 版本验证与清理】');

console.log(`isValid('1.2.3'): ${SemVerUtils.isValid('1.2.3')}`);
console.log(`isValid('v1.2.3-alpha'): ${SemVerUtils.isValid('v1.2.3-alpha')}`);
console.log(`isValid('invalid'): ${SemVerUtils.isValid('invalid')}`);

console.log(`clean('v1.2.3+build'): ${SemVerUtils.clean('v1.2.3+build')}`);
console.log(`clean('  1.2.3-alpha.1  '): ${SemVerUtils.clean('  1.2.3-alpha.1  ')}`);

// ============== 3. 版本比较 ==============
console.log('\n【3. 版本比较】');

const versions = ['1.0.0', '1.2.3', '2.0.0'];
console.log('比较版本:');
for (const v of versions) {
    console.log(`  compare('1.2.3', '${v}'): ${SemVerUtils.compare('1.2.3', v)}`);
}

console.log(`eq('1.2.3', '1.2.3'): ${SemVerUtils.eq('1.2.3', '1.2.3')}`);
console.log(`gt('2.0.0', '1.0.0'): ${SemVerUtils.gt('2.0.0', '1.0.0')}`);
console.log(`lt('1.0.0', '2.0.0'): ${SemVerUtils.lt('1.0.0', '2.0.0')}`);
console.log(`gte('1.2.3', '1.2.0'): ${SemVerUtils.gte('1.2.3', '1.2.0')}`);
console.log(`lte('1.2.0', '1.2.3'): ${SemVerUtils.lte('1.2.0', '1.2.3')}`);

// 预发布版本比较
console.log('\n预发布版本比较:');
console.log(`  compare('1.0.0-alpha', '1.0.0'): ${SemVerUtils.compare('1.0.0-alpha', '1.0.0')}`);
console.log(`  compare('1.0.0-alpha', '1.0.0-beta'): ${SemVerUtils.compare('1.0.0-alpha', '1.0.0-beta')}`);
console.log(`  compare('1.0.0-alpha.1', '1.0.0-alpha.2'): ${SemVerUtils.compare('1.0.0-alpha.1', '1.0.0-alpha.2')}`);

// 兼容性检查
console.log('\n兼容性检查:');
console.log(`  isCompatible('1.2.3', '1.3.0'): ${SemVerUtils.isCompatible('1.2.3', '1.3.0')}`);
console.log(`  isCompatible('1.2.3', '2.0.0'): ${SemVerUtils.isCompatible('1.2.3', '2.0.0')}`);
console.log(`  isCompatible('0.1.0', '0.1.1'): ${SemVerUtils.isCompatible('0.1.0', '0.1.1')}`);

// ============== 4. 版本递增 ==============
console.log('\n【4. 版本递增】');

const base = '1.2.3';
console.log(`基础版本: ${base}`);
console.log(`  incMajor: ${SemVerUtils.incMajor(base).toString()}`);
console.log(`  incMinor: ${SemVerUtils.incMinor(base).toString()}`);
console.log(`  incPatch: ${SemVerUtils.incPatch(base).toString()}`);

const preRelease = '1.2.3-alpha.1';
console.log(`\n带预发布版本: ${preRelease}`);
console.log(`  incPatch (清除预发布): ${SemVerUtils.incPatch(preRelease).toString()}`);
console.log(`  incPrerelease: ${SemVerUtils.incPrerelease(preRelease).toString()}`);

// 设置预发布和构建
console.log('\n设置预发布和构建:');
console.log(`  setPrerelease('1.2.3', 'beta.1'): ${SemVerUtils.setPrerelease('1.2.3', 'beta.1').toString()}`);
console.log(`  setBuild('1.2.3', 'build.123'): ${SemVerUtils.setBuild('1.2.3', 'build.123').toString()}`);

// ============== 5. 版本范围匹配 ==============
console.log('\n【5. 版本范围匹配】');

// 插入符号范围 (^)
console.log('插入符号范围 (^):');
const caretVersions = ['1.2.0', '1.2.5', '1.5.0', '2.0.0'];
for (const v of caretVersions) {
    console.log(`  satisfies('${v}', '^1.2.3'): ${SemVerUtils.satisfies(v, '^1.2.3')}`);
}

// 波浪号范围 (~)
console.log('\n波浪号范围 (~):');
const tildeVersions = ['1.2.3', '1.2.5', '1.3.0', '2.0.0'];
for (const v of tildeVersions) {
    console.log(`  satisfies('${v}', '~1.2.3'): ${SemVerUtils.satisfies(v, '~1.2.3')}`);
}

// 比较符范围
console.log('\n比较符范围:');
console.log(`  satisfies('1.2.5', '>=1.2.0'): ${SemVerUtils.satisfies('1.2.5', '>=1.2.0')}`);
console.log(`  satisfies('1.2.5', '<2.0.0'): ${SemVerUtils.satisfies('1.2.5', '<2.0.0')}`);
console.log(`  satisfies('1.5.0', '>1.2.0 <2.0.0'): ${SemVerUtils.satisfies('1.5.0', '>1.2.0 <2.0.0')}`);

// 连字符范围
console.log('\n连字符范围:');
console.log(`  satisfies('1.5.0', '1.0.0 - 2.0.0'): ${SemVerUtils.satisfies('1.5.0', '1.0.0 - 2.0.0')}`);

// 通配符
console.log('\n通配符:');
console.log(`  satisfies('1.2.3', '*'): ${SemVerUtils.satisfies('1.2.3', '*')}`);
console.log(`  satisfies('1.5.0', '1.*'): ${SemVerUtils.satisfies('1.5.0', '1.*')}`);
console.log(`  satisfies('1.2.5', '1.2.*'): ${SemVerUtils.satisfies('1.2.5', '1.2.*')}`);

// ============== 6. 版本排序 ==============
console.log('\n【6. 版本排序】');

const unsorted = ['2.0.0', '1.0.0', '1.2.3', '1.0.0-alpha', '1.0.0-beta', '1.2.0'];
console.log('原始版本:', unsorted.join(', '));

const sorted = SemVerUtils.sort(unsorted);
console.log('升序排序:', sorted.map(v => v.toString()).join(', '));

const sortedDesc = SemVerUtils.sort(unsorted, { desc: true });
console.log('降序排序:', sortedDesc.map(v => v.toString()).join(', '));

// 最大最小版本
console.log(`\n最大版本: ${SemVerUtils.maxSatisfying(unsorted).toString()}`);
console.log(`最小版本: ${SemVerUtils.minSatisfying(unsorted).toString()}`);

// ============== 7. 过滤版本 ==============
console.log('\n【7. 过滤版本】');

const candidates = ['1.0.0', '1.2.3', '1.5.0', '1.8.0', '2.0.0', '2.1.0'];
const range = '^1.2.0';
const filtered = SemVerUtils.filterSatisfying(candidates, range);
console.log(`版本列表: ${candidates.join(', ')}`);
console.log(`范围 '${range}' 内的版本: ${filtered.map(v => v.toString()).join(', ')}`);

const maxInRange = SemVerUtils.maxSatisfyingInRange(candidates, range);
console.log(`范围内的最大版本: ${maxInRange.toString()}`);

// ============== 8. 版本分析 ==============
console.log('\n【8. 版本分析】');

const analyzeVersion = '1.2.3-beta.1+build.123.sha.abc';
const info = SemVerUtils.analyze(analyzeVersion);
console.log(`分析版本 '${analyzeVersion}':`);
console.log(`  - 主要版本: ${info.major}`);
console.log(`  - 次要版本: ${info.minor}`);
console.log(`  - 修订版本: ${info.patch}`);
console.log(`  - 预发布: ${info.prerelease ? info.prerelease.join('.') : '无'}`);
console.log(`  - 构建: ${info.build ? info.build.join('.') : '无'}`);
console.log(`  - 是否预发布: ${info.isPrerelease}`);
console.log(`  - 是否稳定: ${info.isStable}`);
console.log(`  - 版本级别: ${info.level}`);

// 批量验证
console.log('\n批量验证:');
const batchVersions = ['1.0.0', '2.0.0-beta', 'invalid', '0.1.0', 'also-invalid'];
const validation = SemVerUtils.validateAll(batchVersions);
console.log(`  有效版本: ${validation.valid.length}`);
console.log(`  无效版本: ${validation.invalid.length}`);
console.log(`  稳定版本: ${validation.stable.join(', ')}`);
console.log(`  预发布版本: ${validation.prerelease.join(', ')}`);

// ============== 9. 差异分析 ==============
console.log('\n【9. 差异分析】');

const fromVersion = '1.2.3';
const toVersions = ['1.2.4', '1.3.0', '2.0.0', '1.2.3-beta'];
console.log(`从 '${fromVersion}' 的变更分析:`);
for (const to of toVersions) {
    const change = SemVerUtils.getChangeType(fromVersion, to);
    console.log(`  到 '${to}': ${change.direction} (${change.type || '无变化'})`);
}

// ============== 10. SemVer 类直接使用 ==============
console.log('\n【10. SemVer 类直接使用】');

const semver = new SemVer(1, 2, 3, ['alpha', '1'], ['build', '123']);
console.log('创建 SemVer 实例:');
console.log(`  new SemVer(1, 2, 3, ['alpha', '1'], ['build', '123'])`);
console.log(`  toString(): ${semver.toString()}`);
console.log(`  toCleanString(): ${semver.toCleanString()}`);
console.log(`  isPrerelease(): ${semver.isPrerelease()}`);
console.log(`  isStable(): ${semver.isStable()}`);

// 实例方法比较
const other = new SemVer(1, 2, 4);
console.log(`\n实例比较:`);
console.log(`  ${semver.toString()} < ${other.toString()}: ${semver.lt(other)}`);
console.log(`  ${semver.toString()} eq '1.2.3-alpha.1': ${semver.eq('1.2.3-alpha.1')}`);

// ============== 11. 实际应用场景 ==============
console.log('\n【11. 实际应用场景】');

// 场景 1: 依赖版本管理
console.log('场景 1 - 依赖版本管理:');
const availableVersions = ['1.0.0', '1.2.0', '1.2.3', '1.3.0', '1.4.0-beta', '2.0.0'];
const dependencyRange = '^1.2.0';
const bestMatch = SemVerUtils.maxSatisfyingInRange(availableVersions, dependencyRange);
console.log(`  可用版本: ${availableVersions.join(', ')}`);
console.log(`  依赖要求: '${dependencyRange}'`);
console.log(`  最佳匹配: ${bestMatch.toString()}`);

// 场景 2: 版本发布流程
console.log('\n场景 2 - 版本发布流程:');
let currentVersion = '1.2.3';
console.log(`  当前版本: ${currentVersion}`);
console.log(`  开发预发布: ${SemVerUtils.incPrerelease(currentVersion, 'dev').toString()}`);
console.log(`  Alpha 版本: ${SemVerUtils.incPrerelease(currentVersion, 'alpha').toString()}`);
console.log(`  Beta 版本: ${SemVerUtils.setPrerelease(currentVersion, 'beta.1').toString()}`);
console.log(`  发布版本: ${SemVerUtils.incPatch(SemVerUtils.setPrerelease(currentVersion, null)).toString()}`);
console.log(`  新功能 (minor): ${SemVerUtils.incMinor(currentVersion).toString()}`);
console.log(`  大更新 (major): ${SemVerUtils.incMajor(currentVersion).toString()}`);

// 场景 3: 版本兼容性检查
console.log('\n场景 3 - 版本兼容性检查:');
const installedVersion = '1.2.5';
const peerDependency = '1.2.3';
console.log(`  已安装: ${installedVersion}`);
console.log(`  peer 依赖: ${peerDependency}`);
console.log(`  兼容性: ${SemVerUtils.isCompatible(installedVersion, peerDependency) ? '兼容' : '不兼容'}`);

console.log('\n' + '='.repeat(60));
console.log('示例演示完成！');
console.log('='.repeat(60));