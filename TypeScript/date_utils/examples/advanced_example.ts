/**
 * Date Utils - Advanced Usage Examples
 * 
 * 高级使用示例 - 展示 date_utils 模块在实际场景中的应用
 */

import { DateUtils, formatDate, parseDate, addBusinessDays, diffDays } from '../mod.ts';

console.log('📅 Date Utils - Advanced Usage Examples\n');
console.log('='.repeat(50));

// ==================== 场景 1: 项目排期计算 ====================
console.log('\n📋 场景 1: 项目排期计算 (Project Scheduling)\n');

interface ProjectTask {
  name: string;
  startDate: Date;
  duration: number; // 工作日
  endDate?: Date;
}

const projectStart = new Date('2024-03-01');

const tasks: ProjectTask[] = [
  { name: '需求分析', startDate: projectStart, duration: 5 },
  { name: '设计阶段', startDate: projectStart, duration: 10 },
  { name: '开发阶段', startDate: projectStart, duration: 20 },
  { name: '测试阶段', startDate: projectStart, duration: 10 },
  { name: '部署上线', startDate: projectStart, duration: 3 },
];

let currentDate = projectStart;
console.log(`项目开始日期：${formatDate(projectStart, 'YYYY-MM-DD dddd')}\n`);

tasks.forEach((task, index) => {
  // 每个任务从上一个任务结束后的下一个工作日开始
  if (index > 0) {
    currentDate = addBusinessDays(currentDate, 1);
  }
  
  const endDate = addBusinessDays(currentDate, task.duration - 1);
  task.endDate = endDate;
  
  console.log(`${index + 1}. ${task.name}`);
  console.log(`   开始：${formatDate(currentDate, 'YYYY-MM-DD')} (${formatDate(currentDate, 'dddd', 'zh')})`);
  console.log(`   结束：${formatDate(endDate, 'YYYY-MM-DD')} (${formatDate(endDate, 'dddd', 'zh')})`);
  console.log(`   工期：${task.duration} 个工作日`);
  console.log('');
  
  currentDate = endDate;
});

const projectEnd = tasks[tasks.length - 1].endDate!;
const totalDays = diffDays(projectEnd, projectStart) + 1;
const businessDays = tasks.reduce((sum, task) => sum + task.duration, 0);

console.log(`📊 项目总结:`);
console.log(`   总日历天数：${totalDays} 天`);
console.log(`   总工作日：${businessDays} 天`);
console.log(`   预计完成：${formatDate(projectEnd, 'YYYY-MM-DD dddd')}`);

// ==================== 场景 2: 倒计时计算 ====================
console.log('\n' + '='.repeat(50));
console.log('\n⏰ 场景 2: 倒计时计算 (Countdown Timer)\n');

// 假设一些重要日期
const importantDates = [
  { name: '春节', date: new Date('2024-02-10') },
  { name: '国庆节', date: new Date('2024-10-01') },
  { name: '圣诞节', date: new Date('2024-12-25') },
  { name: '新年', date: new Date('2025-01-01') },
];

const now = new Date();

importantDates.forEach(event => {
  const daysLeft = diffDays(event.date, now);
  
  if (daysLeft < 0) {
    console.log(`${event.name}: 已经过去 ${Math.abs(daysLeft)} 天`);
  } else if (daysLeft === 0) {
    console.log(`${event.name}: 就是今天！🎉`);
  } else if (daysLeft <= 7) {
    console.log(`${event.name}: 还有 ${daysLeft} 天！⚡`);
  } else {
    console.log(`${event.name}: 还有 ${daysLeft} 天`);
  }
});

// ==================== 场景 3: 生日提醒 ====================
console.log('\n' + '='.repeat(50));
console.log('\n🎂 场景 3: 生日提醒 (Birthday Reminder)\n');

interface Person {
  name: string;
  birthDate: Date;
}

const friends: Person[] = [
  { name: '张三', birthDate: new Date('1990-04-15') },
  { name: '李四', birthDate: new Date('1988-08-20') },
  { name: '王五', birthDate: new Date('1992-12-05') },
  { name: '赵六', birthDate: new Date('1995-01-30') },
];

console.log('今年即将到来的生日:\n');

const currentYear = now.getFullYear();

friends.forEach(person => {
  // 计算今年的生日
  let birthdayThisYear = new Date(
    currentYear,
    person.birthDate.getMonth(),
    person.birthDate.getDate()
  );
  
  // 如果今年生日已过，计算明年的
  if (birthdayThisYear < now) {
    birthdayThisYear = new Date(
      currentYear + 1,
      person.birthDate.getMonth(),
      person.birthDate.getDate()
    );
  }
  
  const daysUntil = diffDays(birthdayThisYear, now);
  const age = daysUntil < 365 
    ? currentYear - person.birthDate.getFullYear()
    : currentYear + 1 - person.birthDate.getFullYear();
  
  console.log(`${person.name}:`);
  console.log(`  生日：${formatDate(birthdayThisYear, 'MM 月 DD 日')} (${formatDate(birthdayThisYear, 'dddd', 'zh')})`);
  console.log(`  倒计时：${daysUntil} 天`);
  console.log(`  年龄：${age}岁`);
  console.log('');
});

// ==================== 场景 4: 财务报表周期 ====================
console.log('='.repeat(50));
console.log('\n📈 场景 4: 财务报表周期 (Financial Reporting Periods)\n');

const currentYear2 = now.getFullYear();

console.log(`${currentYear2} 年季度划分:\n`);

for (let quarter = 1; quarter <= 4; quarter++) {
  const startMonth = (quarter - 1) * 3;
  const endMonth = startMonth + 2;
  
  const quarterStart = new Date(currentYear2, startMonth, 1);
  const quarterEnd = new Date(currentYear2, endMonth + 1, 0); // Last day of endMonth
  
  const isCurrentQuarter = DateUtils.getQuarter(now) === quarter;
  const marker = isCurrentQuarter ? ' ← 当前季度' : '';
  
  console.log(`Q${quarter}${marker}`);
  console.log(`  开始：${formatDate(quarterStart, 'YYYY-MM-DD')}`);
  console.log(`  结束：${formatDate(quarterEnd, 'YYYY-MM-DD')}`);
  console.log(`  天数：${diffDays(quarterEnd, quarterStart) + 1} 天`);
  console.log('');
}

// ==================== 场景 5: 工作时间计算 ====================
console.log('='.repeat(50));
console.log('\n💼 场景 5: 工作时间计算 (Working Hours)\n');

interface WorkSchedule {
  startTime: string;
  endTime: string;
  lunchStart: string;
  lunchEnd: string;
}

const schedule: WorkSchedule = {
  startTime: '09:00',
  endTime: '18:00',
  lunchStart: '12:00',
  lunchEnd: '13:00',
};

console.log('工作时间安排:');
console.log(`  上班：${schedule.startTime}`);
console.log(`  午休：${schedule.lunchStart} - ${schedule.lunchEnd}`);
console.log(`  下班：${schedule.endTime}`);
console.log('');

// 计算本周工作日
const weekStart = DateUtils.startOfWeek(now);
const weekEnd = DateUtils.endOfWeek(now);

console.log(`本周工作时间 (${formatDate(weekStart, 'MM/DD')} - ${formatDate(weekEnd, 'MM/DD')}):`);

let totalWorkHours = 0;
let currentDay = new Date(weekStart);

while (currentDay <= weekEnd) {
  if (DateUtils.isWeekday(currentDay)) {
    // 每天 8 小时工作（扣除 1 小时午休）
    totalWorkHours += 8;
    console.log(`  ${formatDate(currentDay, 'dddd', 'zh')}: 09:00 - 18:00 (8 小时)`);
  } else {
    console.log(`  ${formatDate(currentDay, 'dddd', 'zh')}: 休息`);
  }
  currentDay = addBusinessDays(currentDay, 1);
}

console.log(`\n  本周总工时：${totalWorkHours} 小时`);

// ==================== 场景 6: 有效期检查 ====================
console.log('\n' + '='.repeat(50));
console.log('\n⏳ 场景 6: 有效期检查 (Expiration Check)\n');

interface Subscription {
  name: string;
  startDate: Date;
  durationDays: number;
}

const subscriptions: Subscription[] = [
  { name: '视频会员', startDate: new Date('2024-01-01'), durationDays: 365 },
  { name: '云存储', startDate: new Date('2024-02-15'), durationDays: 90 },
  { name: '软件授权', startDate: new Date('2024-03-01'), durationDays: 30 },
  { name: '新闻订阅', startDate: new Date('2024-01-20'), durationDays: 60 },
];

console.log('订阅状态:\n');

subscriptions.forEach(sub => {
  const endDate = addBusinessDays(sub.startDate, sub.durationDays);
  const daysLeft = diffDays(endDate, now);
  
  let status: string;
  let emoji: string;
  
  if (daysLeft < 0) {
    status = '已过期';
    emoji = '❌';
  } else if (daysLeft <= 3) {
    status = '即将过期';
    emoji = '⚠️';
  } else if (daysLeft <= 7) {
    status = '快到期了';
    emoji = '⏰';
  } else {
    status = '有效';
    emoji = '✅';
  }
  
  console.log(`${emoji} ${sub.name}`);
  console.log(`   状态：${status}`);
  console.log(`   到期：${formatDate(endDate, 'YYYY-MM-DD')}`);
  if (daysLeft > 0) {
    console.log(`   剩余：${daysLeft} 天`);
  } else {
    console.log(`   过期：${Math.abs(daysLeft)} 天`);
  }
  console.log('');
});

console.log('\n' + '='.repeat(50));
console.log('✅ 高级示例完成！\n');
