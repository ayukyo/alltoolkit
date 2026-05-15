/**
 * 睡眠周期计算工具模块
 * Sleep Cycle Calculator Utilities
 * 
 * 基于人体睡眠周期（约90分钟）计算最佳睡眠和起床时间
 * 帮助用户在浅睡眠阶段醒来，减少起床困难
 * 
 * @module sleep_cycle_utils
 */

const SLEEP_CYCLE_DURATION = 90; // 睡眠周期时长（分钟）
const FALL_ASLEEP_TIME = 15; // 平均入睡时间（分钟）
const MIN_SLEEP_CYCLES = 4; // 最少睡眠周期数
const MAX_SLEEP_CYCLES = 7; // 最多睡眠周期数

/**
 * 计算最佳起床时间
 * @param {Date} bedTime - 入睡时间
 * @param {number} cycles - 睡眠周期数（4-7）
 * @returns {Object} 起床时间和睡眠信息
 */
function calculateWakeTime(bedTime, cycles = 6) {
  if (cycles < MIN_SLEEP_CYCLES || cycles > MAX_SLEEP_CYCLES) {
    throw new Error(`睡眠周期数应在 ${MIN_SLEEP_CYCLES} 到 ${MAX_SLEEP_CYCLES} 之间`);
  }
  
  const bedDate = new Date(bedTime);
  // 加上入睡时间
  const sleepStart = new Date(bedDate.getTime() + FALL_ASLEEP_TIME * 60000);
  // 计算总睡眠时间
  const totalSleepMinutes = cycles * SLEEP_CYCLE_DURATION;
  const wakeDate = new Date(sleepStart.getTime() + totalSleepMinutes * 60000);
  
  return {
    bedTime: bedDate,
    wakeTime: wakeDate,
    cycles: cycles,
    totalSleepMinutes: totalSleepMinutes + FALL_ASLEEP_TIME,
    totalSleepHours: ((totalSleepMinutes + FALL_ASLEEP_TIME) / 60).toFixed(1),
    quality: getSleepQuality(cycles)
  };
}

/**
 * 计算最佳入睡时间
 * @param {Date} wakeTime - 期望起床时间
 * @param {number} cycles - 睡眠周期数（4-7）
 * @returns {Object} 入睡时间和睡眠信息
 */
function calculateBedTime(wakeTime, cycles = 6) {
  if (cycles < MIN_SLEEP_CYCLES || cycles > MAX_SLEEP_CYCLES) {
    throw new Error(`睡眠周期数应在 ${MIN_SLEEP_CYCLES} 到 ${MAX_SLEEP_CYCLES} 之间`);
  }
  
  const wakeDate = new Date(wakeTime);
  const totalSleepMinutes = cycles * SLEEP_CYCLE_DURATION;
  // 减去睡眠时间和入睡时间
  const bedDate = new Date(wakeDate.getTime() - (totalSleepMinutes + FALL_ASLEEP_TIME) * 60000);
  
  return {
    bedTime: bedDate,
    wakeTime: wakeDate,
    cycles: cycles,
    totalSleepMinutes: totalSleepMinutes + FALL_ASLEEP_TIME,
    totalSleepHours: ((totalSleepMinutes + FALL_ASLEEP_TIME) / 60).toFixed(1),
    quality: getSleepQuality(cycles)
  };
}

/**
 * 获取所有可能的起床时间
 * @param {Date} bedTime - 入睡时间
 * @returns {Array<Object>} 所有可能的起床时间列表
 */
function getAllWakeTimes(bedTime) {
  const results = [];
  for (let cycles = MIN_SLEEP_CYCLES; cycles <= MAX_SLEEP_CYCLES; cycles++) {
    results.push(calculateWakeTime(bedTime, cycles));
  }
  return results;
}

/**
 * 获取所有可能的入睡时间
 * @param {Date} wakeTime - 期望起床时间
 * @returns {Array<Object>} 所有可能的入睡时间列表
 */
function getAllBedTimes(wakeTime) {
  const results = [];
  for (let cycles = MIN_SLEEP_CYCLES; cycles <= MAX_SLEEP_CYCLES; cycles++) {
    results.push(calculateBedTime(wakeTime, cycles));
  }
  return results;
}

/**
 * 获取睡眠质量评级
 * @param {number} cycles - 睡眠周期数
 * @returns {Object} 质量评级信息
 */
function getSleepQuality(cycles) {
  const qualityMap = {
    4: { rating: 'fair', label: '一般', description: '6小时睡眠，勉强够用，下午可能困倦' },
    5: { rating: 'good', label: '良好', description: '7.5小时睡眠，适合大多数成年人' },
    6: { rating: 'excellent', label: '优秀', description: '9小时睡眠，最佳睡眠时长' },
    7: { rating: 'optimal', label: '理想', description: '10.5小时睡眠，适合青少年和恢复期' }
  };
  return qualityMap[cycles] || { rating: 'unknown', label: '未知', description: '' };
}

/**
 * 计算睡眠周期分布
 * @param {number} cycles - 睡眠周期数
 * @returns {Object} 各阶段睡眠分布
 */
function getSleepStageDistribution(cycles) {
  // 基于睡眠科学，典型90分钟周期的阶段分布
  // 前几个周期深睡眠多，后几个周期REM睡眠多
  const stages = [];
  
  for (let i = 0; i < cycles; i++) {
    const cycleNum = i + 1;
    let deepSleep, remSleep, lightSleep;
    
    if (cycleNum <= 2) {
      // 前两个周期：深睡眠为主
      deepSleep = 30 + Math.random() * 10;
      remSleep = 10 + Math.random() * 5;
      lightSleep = 90 - deepSleep - remSleep;
    } else if (cycleNum <= 4) {
      // 中间周期：平衡分布
      deepSleep = 15 + Math.random() * 10;
      remSleep = 20 + Math.random() * 10;
      lightSleep = 90 - deepSleep - remSleep;
    } else {
      // 后期周期：REM为主
      deepSleep = 5 + Math.random() * 5;
      remSleep = 35 + Math.random() * 15;
      lightSleep = 90 - deepSleep - remSleep;
    }
    
    stages.push({
      cycle: cycleNum,
      deepSleep: Math.round(deepSleep),
      remSleep: Math.round(remSleep),
      lightSleep: Math.round(lightSleep)
    });
  }
  
  // 计算总计
  const totals = stages.reduce((acc, s) => ({
    deepSleep: acc.deepSleep + s.deepSleep,
    remSleep: acc.remSleep + s.remSleep,
    lightSleep: acc.lightSleep + s.lightSleep
  }), { deepSleep: 0, remSleep: 0, lightSleep: 0 });
  
  return {
    cycles: stages,
    totals,
    percentages: {
      deepSleep: ((totals.deepSleep / (cycles * 90)) * 100).toFixed(1),
      remSleep: ((totals.remSleep / (cycles * 90)) * 100).toFixed(1),
      lightSleep: ((totals.lightSleep / (cycles * 90)) * 100).toFixed(1)
    }
  };
}

/**
 * 计算两个时间之间的最佳睡眠时段
 * @param {Date} startTime - 可入睡的最早时间
 * @param {Date} endTime - 必须起床的最晚时间
 * @returns {Object} 最佳睡眠建议
 */
function findOptimalSleep(startTime, endTime) {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const availableMinutes = (end - start) / 60000;
  
  if (availableMinutes < (MIN_SLEEP_CYCLES * SLEEP_CYCLE_DURATION + FALL_ASLEEP_TIME)) {
    return {
      possible: false,
      message: '可用时间不足以完成一个完整睡眠周期',
      availableMinutes,
      requiredMinutes: MIN_SLEEP_CYCLES * SLEEP_CYCLE_DURATION + FALL_ASLEEP_TIME
    };
  }
  
  const results = [];
  
  for (let cycles = MIN_SLEEP_CYCLES; cycles <= MAX_SLEEP_CYCLES; cycles++) {
    const neededMinutes = cycles * SLEEP_CYCLE_DURATION + FALL_ASLEEP_TIME;
    if (neededMinutes <= availableMinutes) {
      const bedTime = new Date(end.getTime() - neededMinutes * 60000);
      results.push({
        cycles,
        bedTime,
        wakeTime: end,
        totalSleepHours: (neededMinutes / 60).toFixed(1),
        quality: getSleepQuality(cycles)
      });
    }
  }
  
  // 推荐最佳选项（优先5-6个周期）
  const optimal = results.find(r => r.cycles === 6) || 
                  results.find(r => r.cycles === 5) || 
                  results[results.length - 1];
  
  return {
    possible: true,
    options: results,
    recommended: optimal
  };
}

/**
 * 计算睡眠债务
 * @param {number} idealSleepHours - 理想睡眠时长（小时）
 * @param {number} actualSleepHours - 实际睡眠时长（小时）
 * @param {number} days - 累计天数
 * @returns {Object} 睡眠债务信息
 */
function calculateSleepDebt(idealSleepHours, actualSleepHours, days = 1) {
  const dailyDebt = idealSleepHours - actualSleepHours;
  const totalDebt = dailyDebt * days;
  
  return {
    dailyDebt: dailyDebt.toFixed(1),
    totalDebt: totalDebt.toFixed(1),
    recoveryDays: Math.ceil(Math.abs(totalDebt) / 1), // 每天多睡1小时恢复
    isAccumulating: dailyDebt > 0,
    recommendation: getSleepDebtRecommendation(totalDebt)
  };
}

/**
 * 获取睡眠债务恢复建议
 * @param {number} totalDebt - 累计睡眠债务（小时）
 * @returns {string} 恢复建议
 */
function getSleepDebtRecommendation(totalDebt) {
  if (totalDebt <= 0) {
    return '睡眠充足，继续保持！';
  } else if (totalDebt <= 5) {
    return '轻微睡眠不足，建议今晚提前30分钟入睡';
  } else if (totalDebt <= 10) {
    return '中度睡眠不足，建议今晚增加1小时睡眠';
  } else if (totalDebt <= 20) {
    return '严重睡眠不足，建议周末补觉并调整作息';
  } else {
    return '极度睡眠不足，请立即调整作息，必要时咨询医生';
  }
}

/**
 * 计算午睡时长建议
 * @param {number} hoursSinceWakeUp - 醒来后的小时数
 * @returns {Object} 午睡建议
 */
function suggestNap(hoursSinceWakeUp) {
  // 基于昼夜节律，最佳午睡时间是醒来后6-8小时
  if (hoursSinceWakeUp < 4) {
    return {
      recommended: false,
      message: '现在还太早，建议再等待一段时间',
      bestTime: `${6 - hoursSinceWakeUp}小时后再午睡`
    };
  }
  
  if (hoursSinceWakeUp > 14) {
    return {
      recommended: false,
      message: '太晚了，午睡可能影响晚间睡眠',
      alternative: '建议等待晚间睡眠'
    };
  }
  
  // 根据时间推荐不同午睡时长
  if (hoursSinceWakeUp >= 4 && hoursSinceWakeUp < 8) {
    return {
      recommended: true,
      duration: 20,
      type: 'power_nap',
      message: '能量午睡：20分钟，快速恢复精力',
      warning: '避免超过30分钟，防止睡眠惯性'
    };
  } else {
    return {
      recommended: true,
      duration: 90,
      type: 'full_cycle',
      message: '完整周期午睡：90分钟，完成一个完整睡眠周期',
      warning: '确保有足够时间完成整个周期'
    };
  }
}

/**
 * 格式化时间显示
 * @param {Date} date - 日期对象
 * @returns {string} 格式化的时间字符串
 */
function formatTime(date) {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}

/**
 * 生成睡眠报告
 * @param {Date} bedTime - 入睡时间
 * @param {Date} wakeTime - 起床时间
 * @returns {Object} 完整睡眠报告
 */
function generateSleepReport(bedTime, wakeTime) {
  const bed = new Date(bedTime);
  const wake = new Date(wakeTime);
  const sleepMinutes = (wake - bed) / 60000;
  const cycles = Math.round(sleepMinutes / SLEEP_CYCLE_DURATION);
  const actualCycles = Math.max(MIN_SLEEP_CYCLES, Math.min(MAX_SLEEP_CYCLES, cycles));
  
  return {
    bedTime: formatTime(bed),
    wakeTime: formatTime(wake),
    sleepDuration: `${Math.floor(sleepMinutes / 60)}小时${Math.round(sleepMinutes % 60)}分钟`,
    estimatedCycles: actualCycles,
    quality: getSleepQuality(actualCycles),
    stageDistribution: getSleepStageDistribution(actualCycles),
    efficiency: calculateSleepEfficiency(sleepMinutes),
    tips: generateSleepTips(sleepMinutes)
  };
}

/**
 * 计算睡眠效率
 * @param {number} sleepMinutes - 睡眠时长（分钟）
 * @returns {Object} 睡眠效率信息
 */
function calculateSleepEfficiency(sleepMinutes) {
  const hours = sleepMinutes / 60;
  let efficiency, status;
  
  if (hours >= 7 && hours <= 9) {
    efficiency = 95;
    status = '优秀';
  } else if (hours >= 6 && hours < 7) {
    efficiency = 80;
    status = '良好';
  } else if (hours >= 9 && hours <= 10) {
    efficiency = 85;
    status = '略多';
  } else if (hours < 6) {
    efficiency = 60;
    status = '不足';
  } else {
    efficiency = 70;
    status = '过多';
  }
  
  return {
    score: efficiency,
    status,
    hours: hours.toFixed(1)
  };
}

/**
 * 生成睡眠建议
 * @param {number} sleepMinutes - 睡眠时长（分钟）
 * @returns {Array<string>} 睡眠建议列表
 */
function generateSleepTips(sleepMinutes) {
  const tips = [];
  const hours = sleepMinutes / 60;
  
  if (hours < 6) {
    tips.push('建议今晚提前入睡，争取6-8小时睡眠');
    tips.push('午后可以小睡20分钟补充精力');
  } else if (hours >= 6 && hours < 7.5) {
    tips.push('睡眠时间基本足够，可以尝试增加一个睡眠周期');
  } else if (hours >= 7.5 && hours <= 9) {
    tips.push('睡眠时长理想，继续保持！');
  } else {
    tips.push('睡眠时间偏长，可能影响白天精力');
    tips.push('建议减少一个睡眠周期，保持7.5-9小时');
  }
  
  tips.push('睡前1小时避免使用电子设备');
  tips.push('保持规律的作息时间');
  
  return tips;
}

module.exports = {
  // 常量
  SLEEP_CYCLE_DURATION,
  FALL_ASLEEP_TIME,
  MIN_SLEEP_CYCLES,
  MAX_SLEEP_CYCLES,
  
  // 主要功能
  calculateWakeTime,
  calculateBedTime,
  getAllWakeTimes,
  getAllBedTimes,
  
  // 分析功能
  getSleepQuality,
  getSleepStageDistribution,
  findOptimalSleep,
  calculateSleepDebt,
  suggestNap,
  
  // 报告功能
  generateSleepReport,
  formatTime,
  
  // 辅助功能
  calculateSleepEfficiency,
  generateSleepTips,
  getSleepDebtRecommendation
};