/**
 * 睡眠周期工具使用示例
 * Sleep Cycle Utils Examples
 */

const {
  calculateWakeTime,
  calculateBedTime,
  getAllWakeTimes,
  getAllBedTimes,
  findOptimalSleep,
  calculateSleepDebt,
  suggestNap,
  generateSleepReport,
  formatTime
} = require('./mod.js');

console.log('========================================');
console.log('      睡眠周期计算器使用示例');
console.log('========================================\n');

// 示例1: 计算最佳起床时间
console.log('📅 示例1: 今晚23:00入睡，计算最佳起床时间');
console.log('-'.repeat(40));
const bedTime = new Date();
bedTime.setHours(23, 0, 0, 0);
const wakeOptions = getAllWakeTimes(bedTime);
wakeOptions.forEach(option => {
  console.log(`  ${option.cycles}个周期 (${option.totalSleepHours}小时): ${formatTime(option.wakeTime)} [${option.quality.label}]`);
});
console.log('');

// 示例2: 计算最佳入睡时间
console.log('⏰ 示例2: 明早7:30要起床，计算最佳入睡时间');
console.log('-'.repeat(40));
const wakeTime = new Date();
wakeTime.setDate(wakeTime.getDate() + 1);
wakeTime.setHours(7, 30, 0, 0);
const bedOptions = getAllBedTimes(wakeTime);
console.log(`为了 ${formatTime(wakeTime)} 起床，建议入睡时间:`);
bedOptions.forEach(option => {
  console.log(`  ${option.cycles}个周期 (${option.totalSleepHours}小时): ${formatTime(option.bedTime)} [${option.quality.label}]`);
});
console.log('');

// 示例3: 查找最佳睡眠时段
console.log('🌙 示例3: 22:00-08:00之间查找最佳睡眠时段');
console.log('-'.repeat(40));
const start = new Date();
start.setHours(22, 0, 0, 0);
const end = new Date();
end.setDate(end.getDate() + 1);
end.setHours(8, 0, 0, 0);
const optimal = findOptimalSleep(start, end);
if (optimal.possible) {
  console.log(`推荐方案:`);
  console.log(`  入睡时间: ${formatTime(optimal.recommended.bedTime)}`);
  console.log(`  起床时间: ${formatTime(optimal.recommended.wakeTime)}`);
  console.log(`  睡眠周期: ${optimal.recommended.cycles}个`);
  console.log(`  睡眠质量: ${optimal.recommended.quality.label}`);
  console.log(`\n所有可行方案:`);
  optimal.options.forEach(o => {
    console.log(`  ${o.cycles}周期: ${formatTime(o.bedTime)} → ${formatTime(o.wakeTime)} [${o.quality.label}]`);
  });
}
console.log('');

// 示例4: 计算睡眠债务
console.log('😴 示例4: 计算一周睡眠债务');
console.log('-'.repeat(40));
const debt = calculateSleepDebt(8, 6.5, 7); // 理想8小时，实际6.5小时，7天
console.log(`理想睡眠: 8小时/天`);
console.log(`实际睡眠: 6.5小时/天`);
console.log(`每日债务: ${debt.dailyDebt}小时`);
console.log(`累计债务: ${debt.totalDebt}小时`);
console.log(`恢复天数: ${debt.recoveryDays}天`);
console.log(`建议: ${debt.recommendation}`);
console.log('');

// 示例5: 午睡建议
console.log('☕ 示例5: 午睡时间建议');
console.log('-'.repeat(40));
[4, 7, 10, 15].forEach(hours => {
  const nap = suggestNap(hours);
  if (nap.recommended) {
    console.log(`醒来${hours}小时后: ${nap.message} (${nap.duration}分钟)`);
  } else {
    console.log(`醒来${hours}小时后: ${nap.message}`);
  }
});
console.log('');

// 示例6: 生成睡眠报告
console.log('📊 示例6: 完整睡眠报告');
console.log('-'.repeat(40));
const reportBedTime = new Date();
reportBedTime.setHours(23, 0, 0, 0);
const reportWakeTime = new Date();
reportWakeTime.setDate(reportWakeTime.getDate() + 1);
reportWakeTime.setHours(7, 15, 0, 0);
const report = generateSleepReport(reportBedTime, reportWakeTime);
console.log(`入睡时间: ${report.bedTime}`);
console.log(`起床时间: ${report.wakeTime}`);
console.log(`睡眠时长: ${report.sleepDuration}`);
console.log(`预估周期: ${report.estimatedCycles}个`);
console.log(`睡眠质量: ${report.quality.label}`);
console.log(`睡眠效率: ${report.efficiency.score}% (${report.efficiency.status})`);
console.log(`\n睡眠阶段分布:`);
console.log(`  深睡眠: ${report.stageDistribution.percentages.deepSleep}%`);
console.log(`  REM睡眠: ${report.stageDistribution.percentages.remSleep}%`);
console.log(`  浅睡眠: ${report.stageDistribution.percentages.lightSleep}%`);
console.log(`\n睡眠建议:`);
report.tips.forEach(tip => console.log(`  • ${tip}`));
console.log('');

console.log('========================================');
console.log('         示例演示完成!');
console.log('========================================');