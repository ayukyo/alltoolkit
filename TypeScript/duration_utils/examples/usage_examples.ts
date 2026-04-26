/**
 * Duration Utils - Usage Examples
 * 
 * This file demonstrates how to use the duration_utils module
 * for parsing and formatting human-readable duration strings.
 */

import {
  parse,
  format,
  parseFormat,
  addDuration,
  subtractDuration,
  diffDates,
  isDuration,
  normalize,
  toUnit,
  Duration,
} from '../mod';

console.log('=== Duration Utils Examples ===\n');

// ==================== Basic Parsing ====================

console.log('--- Basic Parsing ---');

// Parse simple durations
console.log(`parse('1h')       = ${parse('1h')} ms`);        // 3600000
console.log(`parse('2h30m')    = ${parse('2h30m')} ms`);     // 9000000
console.log(`parse('1d 4h')    = ${parse('1d 4h')} ms`);     // 100800000
console.log(`parse('5 minutes') = ${parse('5 minutes')} ms`); // 300000

// Parse Chinese durations
console.log(`parse('2小时30分') = ${parse('2小时30分')} ms`); // 9000000
console.log(`parse('1天')     = ${parse('1天')} ms`);       // 86400000

console.log('');

// ==================== Basic Formatting ====================

console.log('--- Basic Formatting ---');

console.log(`format(3600000)    = '${format(3600000)}'`);     // '1h'
console.log(`format(9000000)    = '${format(9000000)}'`);     // '2h 30m'
console.log(`format(5445000)    = '${format(5445000)}'`);     // '1h 30m 45s'

console.log('');

// ==================== Long Unit Names ====================

console.log('--- Long Unit Names ---');

console.log(`format(3600000, { short: false }) = '${format(3600000, { short: false })}'`);
// '1 hour'

console.log(`format(9000000, { short: false }) = '${format(9000000, { short: false })}'`);
// '2 hours 30 minutes'

console.log('');

// ==================== Chinese Output ====================

console.log('--- Chinese Output ---');

console.log(`format(3600000, { chinese: true }) = '${format(3600000, { chinese: true })}'`);
// '1小时'

console.log(`format(9000000, { chinese: true }) = '${format(9000000, { chinese: true })}'`);
// '2小时 30分钟'

console.log(`format(5445000, { chinese: true }) = '${format(5445000, { chinese: true })}'`);
// '1小时 30分钟 45秒'

console.log('');

// ==================== Max Units ====================

console.log('--- Limiting Output Units ---');

const ms = 5445500; // 1h 30m 45s 500ms

console.log(`format(${ms}, { maxUnits: 1 }) = '${format(ms, { maxUnits: 1 })}'`);  // '1h'
console.log(`format(${ms}, { maxUnits: 2 }) = '${format(ms, { maxUnits: 2 })}'`);  // '1h 30m'
console.log(`format(${ms}, { maxUnits: 3 }) = '${format(ms, { maxUnits: 3 })}'`);  // '1h 30m 45s'

console.log('');

// ==================== Parse & Format Combined ====================

console.log('--- Parse & Format Combined ---');

console.log(`parseFormat('2 hours 30 minutes') = '${parseFormat('2 hours 30 minutes')}'`);
// '2h 30m'

console.log(`parseFormat('1天2小时', { chinese: true }) = '${parseFormat('1天2小时', { chinese: true })}'`);
// '1天 2小时'

console.log('');

// ==================== Date Operations ====================

console.log('--- Date Operations ---');

const now = new Date();
const later = addDuration(now, '2h30m');
const earlier = subtractDuration(now, '1d');

console.log(`Now: ${now.toISOString()}`);
console.log(`+ 2h30m: ${later.toISOString()}`);
console.log(`- 1d: ${earlier.toISOString()}`);

console.log('');

// ==================== Date Difference ====================

console.log('--- Date Difference ---');

const start = new Date('2024-01-01T09:00:00');
const end = new Date('2024-01-01T17:30:00');

console.log(`Work duration: ${diffDates(start, end)}`); // '8h 30m'
console.log(`Work duration (Chinese): ${diffDates(start, end, { chinese: true })}`); // '8小时 30分钟'

console.log('');

// ==================== Validation ====================

console.log('--- Validation ---');

console.log(`isDuration('2h30m') = ${isDuration('2h30m')}`);   // true
console.log(`isDuration('5 minutes') = ${isDuration('5 minutes')}`); // true
console.log(`isDuration('hello') = ${isDuration('hello')}`);   // false
console.log(`isDuration('123') = ${isDuration('123')}`);       // true (number only)

console.log('');

// ==================== Normalize ====================

console.log('--- Normalize ---');

console.log(`normalize('2 hours 30 minutes') = '${normalize('2 hours 30 minutes')}'`);
// '2h 30m'

console.log(`normalize('1天2小时30分钟', { chinese: true }) = '${normalize('1天2小时30分钟', { chinese: true })}'`);
// '1天 2小时 30分钟'

console.log('');

// ==================== Unit Conversion ====================

console.log('--- Unit Conversion ---');

console.log(`toUnit('2h30m', 'minutes') = ${toUnit('2h30m', 'minutes')} minutes`); // 150
console.log(`toUnit('1d', 'hours') = ${toUnit('1d', 'hours')} hours`);             // 24
console.log(`toUnit('1w', 'days') = ${toUnit('1w', 'days')} days`);                 // 7
console.log(`toUnit('1y', 'days') = ${toUnit('1y', 'days')} days`);                 // 365

console.log('');

// ==================== Duration Class ====================

console.log('--- Duration Class (Fluent API) ---');

// Create durations
const workDay = Duration.from('8h');
const lunch = Duration.from('1h');
const meeting = Duration.from('30m');

// Calculate remaining work time
const remaining = workDay.subtract(lunch).subtract(meeting);
console.log(`Work day: ${workDay.format()}`);
console.log(`Lunch: ${lunch.format()}`);
console.log(`Meeting: ${meeting.format()}`);
console.log(`Remaining: ${remaining.format()}`);
console.log(`Remaining in minutes: ${remaining.toMinutes()}`);

// Chaining operations
const total = Duration.from('1h')
  .add('30m')
  .multiply(2)
  .subtract('15m');

console.log(`\nChained calculation: ${total.format()}`); // '2h 45m'

// Compare durations
const short = Duration.from('1h');
const long = Duration.from('2h');
console.log(`\nComparison: ${short.format()} < ${long.format()} = ${short.valueOf() < long.valueOf()}`);

console.log('');

// ==================== Real World Example: Task Timer ====================

console.log('--- Real World: Task Timer ---');

interface Task {
  name: string;
  duration: string;
}

const tasks: Task[] = [
  { name: 'Planning', duration: '1h30m' },
  { name: 'Development', duration: '4h' },
  { name: 'Testing', duration: '2h15m' },
  { name: 'Review', duration: '45m' },
];

let totalDuration = new Duration(0);

console.log('Task Schedule:');
tasks.forEach(task => {
  const dur = Duration.from(task.duration);
  totalDuration = totalDuration.add(dur);
  console.log(`  - ${task.name}: ${dur.format()}`);
});

console.log(`\nTotal time: ${totalDuration.format()}`);
console.log(`Total in hours: ${totalDuration.toHours().toFixed(2)} hours`);

console.log('');

// ==================== Real World Example: Countdown ====================

console.log('--- Real World: Countdown ---');

function formatCountdown(totalSeconds: number): string {
  return format(totalSeconds * 1000, { maxUnits: 3, showMs: false });
}

const countdowns = [3600, 7200, 86400, 90123];

console.log('Countdown timers:');
countdowns.forEach(seconds => {
  console.log(`  ${seconds}s = ${formatCountdown(seconds)}`);
});

console.log('');

// ==================== Real World Example: Time Zone Differences ====================

console.log('--- Real World: Meeting Time Calculator ---');

const meetingDuration = Duration.from('1h30m');
const localTime = new Date('2024-01-15T10:00:00');

// Calculate meeting end times in different time zones
const timeZones = [
  { name: 'Local', offset: '0h' },
  { name: 'Tokyo', offset: '9h' },
  { name: 'London', offset: '0h' },
  { name: 'New York', offset: '-5h' },
];

console.log(`Meeting: ${meetingDuration.format()} starting at ${localTime.toLocaleTimeString()}`);
console.log('End times:');
timeZones.forEach(tz => {
  const offset = parse(tz.offset);
  const localEnd = addDuration(localTime, meetingDuration);
  const tzEnd = new Date(localEnd.getTime() + offset);
  console.log(`  ${tz.name}: ${tzEnd.toLocaleTimeString()}`);
});

console.log('\n=== End of Examples ===');