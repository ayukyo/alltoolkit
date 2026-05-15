/**
 * 睡眠周期工具测试
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
assert.strictEqual(wakeResult.totalSleepMinutes, 555, '总睡眠时间应为555分钟');
console.log(`   入睡: ${formatTime(bedTime)}, 起床: ${formatTime(wakeResult.wakeTime)}`);
console.log('   ✓ 起床时间计算正确\n');

// 测试计算入睡时间
console.log('3. 测试计算入睡时间');
const desiredWakeTime = new Date('2024-01-02T07:00:00');
const bedResult = calculateBedTime(desiredWakeTime, 6);
console.log(`   期望起床: ${formatTime(desiredWakeTime)}, 建议入睡: ${formatTime(bedResult.bedTime)}`);
console.log('   ✓ 入睡时间计算正确\n');

// 测试所有起床时间
console.log('4. 测试获取所有起床时间');
const allWakeTimes = getAllWakeTimes(bedTime);
assert.strictEqual(allWakeTimes.length, 4, '应有4个选项');
allWakeTimes.forEach(r => console.log(`   ${r.cycles}周期: ${formatTime(r.wakeTime)} [${r.quality.label}]`));
console.log('   ✓ 获取所有起床时间正确\n');

// 测试睡眠质量评级
console.log('5. 测试睡眠质量评级');
assert.strictEqual(getSleepQuality(4).rating, 'fair');
assert.strictEqual(getSleepQuality(5).rating, 'good');
assert.strictEqual(getSleepQuality(6).rating, 'excellent');
assert.strictEqual(getSleepQuality(7).rating, 'optimal');
console.log('   ✓ 睡眠质量评级正确\n');

// 测试睡眠阶段分布
console.log('6. 测试睡眠阶段分布');
const distribution = getSleepStageDistribution(6);
assert.strictEqual(distribution.cycles.length, 6);
console.log(`   深睡眠: ${distribution.percentages.deepSleep}%`);
console.log(`   REM: ${distribution.percentages.remSleep}%`);
console.log('   ✓ 睡眠阶段分布正确\n');

// 测试睡眠债务计算
console.log('7. 测试睡眠债务计算');
const debt = calculateSleepDebt(8, 6, 5);
assert.strictEqual(debt.totalDebt, '10.0');
console.log(`   累计债务: ${debt.totalDebt}小时`);
console.log('   ✓ 睡眠债务计算正确\n');

// 测试午睡建议
console.log('8. 测试午睡建议');
const nap1 = suggestNap(7);
assert.strictEqual(nap1.recommended, true);
console.log(`   醒来7小时后: ${nap1.message}`);
console.log('   ✓ 午睡建议正确\n');

// 测试睡眠报告
console.log('9. 测试睡眠报告生成');
const report = generateSleepReport(
  new Date('2024-01-01T23:00:00'),
  new Date('2024-01-02T07:30:00')
);
console.log(`   睡眠时长: ${report.sleepDuration}`);
console.log(`   睡眠质量: ${report.quality.label}`);
console.log(`   睡眠效率: ${report.efficiency.score}%`);
console.log('   ✓ 睡眠报告正确\n');

// 测试错误处理
console.log('10. 测试错误处理');
try {
  calculateWakeTime(bedTime, 3);
  assert.fail('应抛出错误');
} catch (e) {
  console.log('   ✓ 无效周期数正确抛出错误\n');
}

console.log('=== 所有测试通过! ===');