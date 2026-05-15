# Sleep Cycle Utils (睡眠周期计算工具)

基于人体睡眠周期（约90分钟）的计算工具，帮助用户在最佳时间入睡和起床，减少起床困难。

## 功能特性

- 🌙 **计算最佳起床时间** - 根据入睡时间计算所有可能的起床时间
- ⏰ **计算最佳入睡时间** - 根据期望起床时间反推最佳入睡时间
- 📊 **睡眠质量评估** - 基于睡眠周期数评估睡眠质量
- 🧠 **睡眠阶段分布** - 估算深睡眠、REM睡眠和浅睡眠时间
- 😴 **睡眠债务计算** - 追踪累计睡眠不足并给出恢复建议
- ☕ **午睡建议** - 根据清醒时间推荐最佳午睡时长
- 📈 **睡眠报告生成** - 生成完整睡眠分析报告

## 安装使用

```javascript
const sleepCycle = require('./mod.js');

// 或 ES6 方式
// import * as sleepCycle from './mod.js';
```

## 快速开始

### 计算起床时间

```javascript
const { calculateWakeTime, getAllWakeTimes, formatTime } = sleepCycle;

// 今晚11点入睡，计算所有可能的起床时间
const bedTime = new Date();
bedTime.setHours(23, 0, 0, 0);

const options = getAllWakeTimes(bedTime);
options.forEach(opt => {
  console.log(`${opt.cycles}个周期: ${formatTime(opt.wakeTime)} [${opt.quality.label}]`);
});
// 4个周期: 05:45 [一般]
// 5个周期: 07:15 [良好]
// 6个周期: 08:45 [优秀]
// 7个周期: 10:15 [理想]
```

### 计算入睡时间

```javascript
const { calculateBedTime, getAllBedTimes } = sleepCycle;

// 明早7:30要起床，计算最佳入睡时间
const wakeTime = new Date();
wakeTime.setDate(wakeTime.getDate() + 1);
wakeTime.setHours(7, 30, 0, 0);

const bedOptions = getAllBedTimes(wakeTime);
bedOptions.forEach(opt => {
  console.log(`${opt.cycles}个周期: ${formatTime(opt.bedTime)}`);
});
// 7个周期: 20:45
// 6个周期: 22:15 (推荐)
// 5个周期: 23:45
// 4个周期: 01:15
```

### 睡眠报告

```javascript
const { generateSleepReport } = sleepCycle;

const report = generateSleepReport(
  new Date('2024-01-01T23:00:00'),
  new Date('2024-01-02T07:30:00')
);

console.log(`睡眠时长: ${report.sleepDuration}`);
console.log(`睡眠质量: ${report.quality.label}`);
console.log(`睡眠效率: ${report.efficiency.score}%`);
```

## API 文档

### 常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `SLEEP_CYCLE_DURATION` | 90 | 睡眠周期时长（分钟） |
| `FALL_ASLEEP_TIME` | 15 | 平均入睡时间（分钟） |
| `MIN_SLEEP_CYCLES` | 4 | 最少睡眠周期数 |
| `MAX_SLEEP_CYCLES` | 7 | 最多睡眠周期数 |

### 主要函数

#### `calculateWakeTime(bedTime, cycles)`
根据入睡时间和周期数计算起床时间。

```javascript
const result = calculateWakeTime(new Date('2024-01-01T23:00:00'), 6);
// result.wakeTime: Date对象
// result.cycles: 6
// result.totalSleepHours: "9.2"
// result.quality: { rating, label, description }
```

#### `calculateBedTime(wakeTime, cycles)`
根据起床时间和周期数计算最佳入睡时间。

#### `getAllWakeTimes(bedTime)`
获取所有可能的起床时间（4-7个周期）。

#### `getAllBedTimes(wakeTime)`
获取所有可能的入睡时间（4-7个周期）。

#### `findOptimalSleep(startTime, endTime)`
在给定时间范围内查找最佳睡眠时段。

```javascript
const result = findOptimalSleep(
  new Date('2024-01-01T22:00:00'),
  new Date('2024-01-02T08:00:00')
);
// result.possible: true/false
// result.recommended: { bedTime, wakeTime, cycles, quality }
// result.options: 所有可行方案
```

#### `calculateSleepDebt(idealHours, actualHours, days)`
计算睡眠债务。

```javascript
const debt = calculateSleepDebt(8, 6.5, 7);
// debt.dailyDebt: "1.5"
// debt.totalDebt: "10.5"
// debt.recoveryDays: 11
// debt.recommendation: "中度睡眠不足..."
```

#### `suggestNap(hoursSinceWakeUp)`
根据醒来后的小时数给出午睡建议。

```javascript
const nap = suggestNap(7);
// nap.recommended: true
// nap.duration: 20
// nap.type: "power_nap"
// nap.message: "能量午睡：20分钟，快速恢复精力"
```

#### `generateSleepReport(bedTime, wakeTime)`
生成完整睡眠报告。

## 睡眠科学背景

### 睡眠周期
人类睡眠由多个约90分钟的周期组成，每个周期包含：
- **浅睡眠 (N1, N2)**: 约45-55%
- **深睡眠 (N3)**: 约15-25%
- **REM睡眠**: 约20-25%

### 最佳睡眠时长
| 周期数 | 总时长 | 质量评级 | 适用人群 |
|--------|--------|----------|----------|
| 4 | 6小时 | 一般 | 短睡眠者 |
| 5 | 7.5小时 | 良好 | 大多数成年人 |
| 6 | 9小时 | 优秀 | 青少年、运动员 |
| 7 | 10.5小时 | 理想 | 恢复期、青少年 |

### 为什么在周期结束醒来更好？
在浅睡眠阶段醒来，人感觉清醒、精力充沛。
在深睡眠阶段醒来，会产生"睡眠惯性"，感觉昏沉、疲惫。

## 运行测试

```bash
node test.js
```

## 运行示例

```bash
node examples.js
```

## 许可证

MIT