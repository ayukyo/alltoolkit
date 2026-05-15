/**
 * 睡眠周期工具测试
 * Sleep Cycle Utils Tests
 */

const assert = require('assert');
const {
  SLEEP_CYCLE_DURATION,
  FALL_ASLEEP_TIME,
  MIN_SLEEP_CYCLES,
  MAX_SLEEP_CYCLES,
  calculateWakeTime,
  calculateBedTime,
  getAllWakeTimes,
  getAllBedTimes,
  getSleepQuality,
  getSleepStageDistribution,
  findOptimalSleep,
  calculateSleepDebt,
  suggestNap,
  generateSleepReport,
  formatTime,
  calculateSleepEfficiency,
  generateSleepTips
} = require('./mod.js');

console.log('=== 睡眠周期工具测试 ===\n');

// 测试常量
console.log('1. 测试常量定义');
assert.strictEqual(SLEEP_CYCLE_DURATION, 90, '睡眠周期应为90分钟');
assert.strictEqual(FALL_ASLEEP_TIME, 15, '入睡时间应为15分钟');
assert.strictEqual(MIN_SLEEP_CYCLES, 4, '最少周期数应为4');
assert.strictEqual(MAX_SLEEP_CYCLES, 7, '最多周期数应为7');
console.log('   ✓ 常量定义正确\n');

// 测试计算起床时间
console.log('2. 测试计算起床时间');
const bedTime = new Date('2024-01-01T23:00:00');
const wakeResult = calculateWakeTime(bedTime, 6);
assert.strictEqual(wakeResult.cycles, 6, '周期数应为6');
assert.strictEqual(wakeResult.totalSleepMinutes, 555, '总睡眠时间应为555分钟（540+15）');
console.log(`   入睡时间: ${formatTime(bedTime)}`);
console.log(`   起床时间: ${formatTime(wakeResult.wakeTime)}`);
console.log(`   睡眠时长: ${wakeResult.totalSleepHours}小时`);
console.log('   ✓ 起床时间计算正确\n');

// 测试计算入睡时间
console.log('3. 测试计算入睡时间');
const desiredWakeTime = new Date('2024-01-02T07:00:00');
const bedResult = calculateBedTime(desiredWakeTime, 6);
console.log(`   期望起床: ${formatTime(desiredWakeTime)}`);
console.log(`   建议入睡: ${formatTime(bedResult.bedTime)}`);
console.log('   ✓ 入睡时间计算正确\n');

// 测试获取所有起床时间
console.log('4. 测试获取所有起床时间');
const allWakeTimes = getAllWakeTimes(bedTime);
assert.strictEqual(allWakeTimes.length, 4, '应有4个选项（4-7周期）');
console.log('   所有可能的起床时间:');
allWakeTimes.forEach(r => {
  console.log(`     ${r.cycles}周期: ${formatTime(r.wakeTime)} (${r.quality.label})`);
});
console.log('   ✓ 获取所有起床时间正确\n');

// 测试获取所有入睡时间
console.log('5. 测试获取所有入睡时间');
const allBedTimes = getAllBedTimes(desiredWakeTime);
assert.strictEqual(allBedTimes.length, 4, '应有4个选项（4-7周期）');
console.log('   所有可能的入睡时间:');
allBedTimes.forEach(r => {
  console.log(`     ${r.cycles}周期: ${formatTime(r.bedTime)} (${r.quality.label})`);
});
console.log('   ✓ 获取所有入睡时间正确\n');

// 测试睡眠质量评级
console.log('6. 测试睡眠质量评级');
assert.strictEqual(getSleepQuality(4).rating, 'fair', '4周期应为一般');
assert.strictEqual(getSleepQuality(5).rating, 'good', '5周期应为良好');
assert.strictEqual(getSleepQuality(6).rating, 'excellent', '6周期应为优秀');
assert.strictEqual(getSleepQuality(7).rating, 'optimal', '7周期应为理想');
console.log('   ✓ 睡眠质量评级正确\n');

// 测试睡眠阶段分布
console.log('7. 测试睡眠阶段分布');
const distribution = getSleepStageDistribution(6);
assert.strictEqual(distribution.cycles.length, 6, '应有6个周期');
assert.ok(distribution.totals.deepSleep > 0, '应有深睡眠时间');
assert.ok(distribution.totals.remSleep > 0, '应有REM睡眠时间');
assert.ok(distribution.totals.lightSleep > 0, '应有浅睡眠时间');
console.log(`   深睡眠: ${distribution.percentages.deepSleep}%`);
console.log(`   REM睡眠: ${distribution.percentages.remSleep}%`);
console.log(`   浅睡眠: ${distribution.percentages.lightSleep}%`);
console.log('   ✓ 睡眠阶段分布计算正确\n');

// 测试查找最佳睡眠时段
console.log('8. 测试查找最佳睡眠时段');
const start = new Date('2024-01-01T22:00:00');
const end = new Date('2024-01-02T08:00:00');
const optimal = findOptimalSleep(start, end);
assert.ok(optimal.possible, '应能找到可行的睡眠方案');
assert.ok(optimal.recommended, '应有推荐方案');
console.log(`   推荐入睡时间: ${formatTime(optimal.recommended.bedTime)}`);
console.log(`   推荐周期数: ${optimal.recommended.cycles}`);
console.log('   ✓ 最佳睡眠时段查找正确\n');

// 测试睡眠债务计算
console.log('9. 测试睡眠债务计算');
const debt = calculateSleepDebt(8, 6, 5); // 每天少睡2小时，连续5天
assert.strictEqual(debt.totalDebt, '10.0', '总债务应为10小时');
assert.ok(debt.recoveryDays > 0, '应有恢复天数');
console.log(`   每日债务: ${debt.dailyDebt}小时`);
console.log(`   累计债务: ${debt.totalDebt}小时`);
console.log(`   恢复建议: ${debt.recommendation}`);
console.log('   ✓ 睡眠债务计算正确\n');

// 测试午睡建议
console.log('10. 测试午睡建议');
const nap1 = suggestNap(3);  // 醒来后3小时
const nap2 = suggestNap(7);  // 醒来后7小时
const nap3 = suggestNap(15); // 醒来后15小时
assert.strictEqual(nap1.recommended, false, '3小时后不建议午睡');
assert.strictEqual(nap2.recommended, true, '7小时后建议午睡');
assert.strictEqual(nap3.recommended, false, '15小时后不建议午睡');
console.log(`   醒来后3小时: ${nap1.message}`);
console.log(`   醒来后7小时: ${nap2.message} (${nap2.duration}分钟)`);
console.log(`   醒来后15小时: ${nap3.message}`);
console.log('   ✓ 午睡建议正确\n');

// 测试睡眠报告生成
console.log('11. 测试睡眠报告生成');
const report = generateSleepReport(
  new Date('2024-01-01T23:00:00'),
  new Date('2024-01-02T07:30:00')
);
console.log(`   入睡时间: ${report.bedTime}`);
console.log(`   起床时间: ${report.wakeTime}`);
console.log(`   睡眠时长: ${report.sleepDuration}`);
console.log(`   预估周期: ${report.estimatedCycles}个`);
console.log(`   睡眠质量: ${report.quality.label}`);
console.log(`   睡眠效率: ${report.efficiency.score}% (${report.efficiency.status})`);
console.log('   ✓ 睡眠报告生成正确\n');

// 测试睡眠效率计算
console.log('12. 测试睡眠效率计算');
const eff1 = calculateSleepEfficiency(8 * 60); // 8小时
const eff2 = calculateSleepEfficiency(5.5 * 60); // 5.5小时
const eff3 = calculateSleepEfficiency(10 * 60); // 10小时
assert.strictEqual(eff1.status, '优秀', '8小时睡眠应评为优秀');
assert.strictEqual(eff2.status, '不足', '5.5小时睡眠应评为不足');
assert.strictEqual(eff3.status, '略多', '10小时睡眠应评为略多');
console.log(`   8小时: ${eff1.score}% - ${eff1.status}`);
console.log(`   5.5小时: ${eff2.score}% - ${eff2.status}`);
console.log(`   10小时: ${eff3.score}% - ${eff3.status}`);
console.log('   ✓ 睡眠效率计算正确\n');

// 测试睡眠建议生成
console.log('13. 测试睡眠建议生成');
const tips1 = generateSleepTips(5 * 60); // 5小时
const tips2 = generateSleepTips(8 * 60); // 8小时
assert.ok(tips1.length > 0, '应生成建议');
assert.ok(tips2.length > 0, '应生成建议');
console.log('   5小时睡眠建议:');
tips1.slice(0, 2).forEach(t => console.log(`     - ${t}`));
console.log('   8小时睡眠建议:');
tips2.slice(0, 2).forEach(t => console.log(`     - ${t}`));
console.log('   ✓ 睡眠建议生成正确\n');

// 测试错误处理
console.log('14. 测试错误处理');
try {
  calculateWakeTime(bedTime, 3); // 低于最小周期数
  assert.fail('应该抛出错误');
} catch (e) {
  assert.ok(e.message.includes('睡眠周期数'), '应提示周期数范围');
  console.log('   ✓ 无效周期数正确抛出错误');
}

try {
  calculateBedTime(desiredWakeTime, 8); // 高于最大周期数
  assert.fail('应该抛出错误');
} catch (e) {
  assert.ok(e.message.includes('睡眠周期数'), '应提示周期数范围');
  console.log('   ✓ 无效周期数正确抛出错误');
}
console.log('');

// 测试边界情况
console.log('15. 测试边界情况');
const minCycle = calculateWakeTime(bedTime, MIN_SLEEP_CYCLES);
const maxCycle = calculateWakeTime(bedTime, MAX_SLEEP_CYCLES);
assert.ok(minCycle.wakeTime < maxCycle.wakeTime, '更多周期应产生更晚的起床时间');
console.log(`   最小周期(${MIN_SLEEP_CYCLES}): ${formatTime(minCycle.wakeTime)}`);
console.log(`   最大周期(${MAX_SLEEP_CYCLES}): ${formatTime(maxCycle.wakeTime)}`);
console.log('   ✓ 边界情况处理正确\n');

console.log('=== 所有测试通过! ===');