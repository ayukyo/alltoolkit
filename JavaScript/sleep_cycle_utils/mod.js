/**
 * 睡眠周期计算工具模块
 * Sleep Cycle Calculator Utilities
 */

const SLEEP_CYCLE_DURATION = 90;
const FALL_ASLEEP_TIME = 15;
const MIN_SLEEP_CYCLES = 4;
const MAX_SLEEP_CYCLES = 7;

function calculateWakeTime(bedTime, cycles = 6) {
  if (cycles < MIN_SLEEP_CYCLES || cycles > MAX_SLEEP_CYCLES) {
    throw new Error(`周期数应在 ${MIN_SLEEP_CYCLES}-${MAX_SLEEP_CYCLES}`);
  }
  const bedDate = new Date(bedTime);
  const totalMinutes = cycles * SLEEP_CYCLE_DURATION + FALL_ASLEEP_TIME;
  return {
    bedTime: bedDate,
    wakeTime: new Date(bedDate.getTime() + totalMinutes * 60000),
    cycles,
    totalSleepMinutes: totalMinutes,
    totalSleepHours: (totalMinutes / 60).toFixed(1),
    quality: getQuality(cycles)
  };
}

function calculateBedTime(wakeTime, cycles = 6) {
  if (cycles < MIN_SLEEP_CYCLES || cycles > MAX_SLEEP_CYCLES) {
    throw new Error(`周期数应在 ${MIN_SLEEP_CYCLES}-${MAX_SLEEP_CYCLES}`);
  }
  const wakeDate = new Date(wakeTime);
  const totalMinutes = cycles * SLEEP_CYCLE_DURATION + FALL_ASLEEP_TIME;
  return {
    bedTime: new Date(wakeDate.getTime() - totalMinutes * 60000),
    wakeTime: wakeDate,
    cycles,
    totalSleepMinutes: totalMinutes,
    totalSleepHours: (totalMinutes / 60).toFixed(1),
    quality: getQuality(cycles)
  };
}

function getAllWakeTimes(bedTime) {
  const results = [];
  for (let c = MIN_SLEEP_CYCLES; c <= MAX_SLEEP_CYCLES; c++) {
    results.push(calculateWakeTime(bedTime, c));
  }
  return results;
}

function getAllBedTimes(wakeTime) {
  const results = [];
  for (let c = MIN_SLEEP_CYCLES; c <= MAX_SLEEP_CYCLES; c++) {
    results.push(calculateBedTime(wakeTime, c));
  }
  return results;
}

function getQuality(cycles) {
  const map = {
    4: { rating: 'fair', label: '一般' },
    5: { rating: 'good', label: '良好' },
    6: { rating: 'excellent', label: '优秀' },
    7: { rating: 'optimal', label: '理想' }
  };
  return map[cycles] || { rating: 'unknown', label: '未知' };
}

function formatTime(date) {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', hour12: false });
}

function generateSleepReport(bedTime, wakeTime) {
  const bed = new Date(bedTime);
  const wake = new Date(wakeTime);
  const sleepMinutes = (wake - bed) / 60000;
  const cycles = Math.max(MIN_SLEEP_CYCLES, Math.min(MAX_SLEEP_CYCLES, Math.round(sleepMinutes / SLEEP_CYCLE_DURATION)));
  const hours = sleepMinutes / 60;
  let efficiency, status;
  if (hours >= 7 && hours <= 9) { efficiency = 95; status = '优秀'; }
  else if (hours >= 6 && hours < 7) { efficiency = 80; status = '良好'; }
  else if (hours < 6) { efficiency = 60; status = '不足'; }
  else { efficiency = 70; status = '过多'; }
  return {
    bedTime: formatTime(bed),
    wakeTime: formatTime(wake),
    sleepDuration: `${Math.floor(sleepMinutes/60)}小时${Math.round(sleepMinutes%60)}分钟`,
    estimatedCycles: cycles,
    quality: getQuality(cycles),
    efficiency: { score: efficiency, status }
  };
}

function calculateSleepDebt(ideal, actual, days = 1) {
  const dailyDebt = ideal - actual;
  const totalDebt = dailyDebt * days;
  let recommendation = '睡眠充足';
  if (totalDebt > 5) recommendation = '轻微不足，今晚提前30分钟入睡';
  if (totalDebt > 10) recommendation = '中度不足，建议增加1小时睡眠';
  if (totalDebt > 20) recommendation = '严重不足，周末补觉';
  return { dailyDebt, totalDebt, recommendation };
}

function suggestNap(hoursSinceWakeUp) {
  if (hoursSinceWakeUp < 4) return { recommended: false, message: '太早了' };
  if (hoursSinceWakeUp > 14) return { recommended: false, message: '太晚了' };
  if (hoursSinceWakeUp < 10) return { recommended: true, duration: 20, type: 'power_nap', message: '能量午睡20分钟' };
  return { recommended: true, duration: 90, type: 'full_cycle', message: '完整周期午睡90分钟' };
}

module.exports = {
  SLEEP_CYCLE_DURATION,
  FALL_ASLEEP_TIME,
  MIN_SLEEP_CYCLES,
  MAX_SLEEP_CYCLES,
  calculateWakeTime,
  calculateBedTime,
  getAllWakeTimes,
  getAllBedTimes,
  getQuality,
  formatTime,
  generateSleepReport,
  calculateSleepDebt,
  suggestNap
};