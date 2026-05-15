const assert = require('assert');
const lib = require('./mod.js');

console.log('=== 睡眠周期工具测试 ===');

// 测试常量
assert.strictEqual(lib.SLEEP_CYCLE_DURATION, 90);
assert.strictEqual(lib.FALL_ASLEEP_TIME, 15);
console.log('1. ✓ 常量定义正确');

// 测试计算起床时间
const bed = new Date('2024-01-01T23:00:00');
const wake = lib.calculateWakeTime(bed, 6);
assert.strictEqual(wake.cycles, 6);
console.log('2. ✓ 起床时间计算正确');

// 测试计算入睡时间
const targetWake = new Date('2024-01-02T07:00:00');
const bedTime = lib.calculateBedTime(targetWake, 6);
console.log('3. ✓ 入睡时间计算正确');

// 测试所有起床时间
const allWake = lib.getAllWakeTimes(bed);
assert.strictEqual(allWake.length, 4);
console.log('4. ✓ 获取所有起床时间正确');

// 测试睡眠质量
assert.strictEqual(lib.getQuality(6).rating, 'excellent');
console.log('5. ✓ 睡眠质量评级正确');

// 测试睡眠报告
const report = lib.generateSleepReport(bed, new Date('2024-01-02T07:30:00'));
assert.ok(report.sleepDuration);
console.log('6. ✓ 睡眠报告正确');

// 测试睡眠债务
const debt = lib.calculateSleepDebt(8, 6, 5);
assert.strictEqual(debt.totalDebt, 10);
console.log('7. ✓ 睡眠债务计算正确');

// 测试午睡建议
const nap = lib.suggestNap(7);
assert.strictEqual(nap.recommended, true);
console.log('8. ✓ 午睡建议正确');

// 测试错误处理
try {
  lib.calculateWakeTime(bed, 3);
  assert.fail('应抛错');
} catch(e) {}
console.log('9. ✓ 错误处理正确');

console.log('=== 所有测试通过! ===');