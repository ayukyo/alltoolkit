/**
 * Tests for duration_utils
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
} from './mod';

// ==================== parse() tests ====================

function testParseBasic() {
  console.log('Testing parse basic...');
  
  // Simple units
  assertEqual(parse('1ms'), 1, '1ms');
  assertEqual(parse('1s'), 1000, '1s');
  assertEqual(parse('1m'), 60000, '1m');
  assertEqual(parse('1h'), 3600000, '1h');
  assertEqual(parse('1d'), 86400000, '1d');
  assertEqual(parse('1w'), 604800000, '1w');
  
  // Compound durations
  assertEqual(parse('2h30m'), 9000000, '2h30m');
  assertEqual(parse('1d 4h 30m'), 102600000, '1d 4h 30m');
  assertEqual(parse('1h 30m 45s'), 5445000, '1h 30m 45s');
  assertEqual(parse('1h 30m 45s 500ms'), 5445500, '1h 30m 45s 500ms');
  
  // Long unit names
  assertEqual(parse('5 minutes'), 300000, '5 minutes');
  assertEqual(parse('2 hours 30 minutes'), 9000000, '2 hours 30 minutes');
  assertEqual(parse('1 second'), 1000, '1 second');
  
  // Chinese units
  assertEqual(parse('2小时30分'), 9000000, '2小时30分');
  assertEqual(parse('1天2小时'), 93600000, '1天2小时');
  assertEqual(parse('3分30秒'), 210000, '3分30秒');
  assertEqual(parse('1年'), 31536000000, '1年');
  
  // Decimal values
  assertEqual(parse('1.5h'), 5400000, '1.5h');
  assertEqual(parse('0.5d'), 43200000, '0.5d');
  
  // Negative durations
  assertEqual(parse('-1h'), -3600000, '-1h');
  assertEqual(parse('-2h30m'), -9000000, '-2h30m');
  
  // Number input
  assertEqual(parse(5000), 5000, 'number input');
  
  // Default unit
  assertEqual(parse('100'), 100, 'default unit ms');
  assertEqual(parse('100', { defaultUnit: 's' }), 100000, 'default unit s');
  
  // Edge cases
  assertEqual(parse(''), 0, 'empty string');
  assertEqual(parse('  '), 0, 'whitespace');
  assertEqual(parse(0), 0, 'zero');
  
  console.log('  ✓ parse basic tests passed');
}

function testParseStrict() {
  console.log('Testing parse strict mode...');
  
  // Should throw on invalid input
  let threw = false;
  try {
    parse('invalid', { strict: true });
  } catch {
    threw = true;
  }
  assertEqual(threw, true, 'strict mode throws on invalid');
  
  // Should throw on unknown unit
  threw = false;
  try {
    parse('5xyz', { strict: true });
  } catch {
    threw = true;
  }
  assertEqual(threw, true, 'strict mode throws on unknown unit');
  
  // Should not throw in non-strict
  assertEqual(parse('invalid'), 0, 'non-strict returns 0');
  assertEqual(parse('5xyz'), 0, 'non-strict unknown unit returns 0');
  
  console.log('  ✓ parse strict tests passed');
}

function testParseNoNegative() {
  console.log('Testing parse no negative...');
  
  assertEqual(parse('-1h', { allowNegative: false }), 0, 'no negative returns 0');
  assertEqual(parse('-1h', { allowNegative: true }), -3600000, 'allow negative');
  
  console.log('  ✓ parse no negative tests passed');
}

// ==================== format() tests ====================

function testFormatBasic() {
  console.log('Testing format basic...');
  
  // Simple units
  assertEqual(format(1), '1ms', '1ms');
  assertEqual(format(1000), '1s', '1s');
  assertEqual(format(60000), '1m', '1m');
  assertEqual(format(3600000), '1h', '1h');
  assertEqual(format(86400000), '1d', '1d');
  
  // Compound durations
  assertEqual(format(9000000), '2h 30m', '2h 30m');
  assertEqual(format(5445000), '1h 30m 45s', '1h 30m 45s');
  
  // Zero
  assertEqual(format(0), '0ms', 'zero');
  
  // Negative
  assertEqual(format(-3600000), '-1h', 'negative');
  
  // Very large
  assertEqual(format(604800000), '1w', '1 week');
  assertEqual(format(31536000000), '1y', '1 year');
  
  console.log('  ✓ format basic tests passed');
}

function testFormatMaxUnits() {
  console.log('Testing format maxUnits...');
  
  assertEqual(format(5445500, { maxUnits: 1 }), '1h', 'maxUnits 1');
  assertEqual(format(5445500, { maxUnits: 2 }), '1h 30m', 'maxUnits 2');
  assertEqual(format(5445500, { maxUnits: 3 }), '1h 30m 45s', 'maxUnits 3');
  
  console.log('  ✓ format maxUnits tests passed');
}

function testFormatLong() {
  console.log('Testing format long names...');
  
  assertEqual(format(3600000, { short: false }), '1 hour', '1 hour');
  assertEqual(format(7200000, { short: false }), '2 hours', '2 hours');
  assertEqual(format(9000000, { short: false }), '2 hours 30 minutes', '2 hours 30 minutes');
  assertEqual(format(1000, { short: false }), '1 second', '1 second');
  
  console.log('  ✓ format long names tests passed');
}

function testFormatChinese() {
  console.log('Testing format Chinese...');
  
  assertEqual(format(3600000, { chinese: true }), '1小时', '1小时');
  assertEqual(format(9000000, { chinese: true }), '2小时 30分钟', '2小时 30分钟');
  assertEqual(format(5445000, { chinese: true }), '1小时 30分钟 45秒', 'Chinese duration');
  assertEqual(format(86400000, { chinese: true }), '1天', '1天');
  assertEqual(format(0, { chinese: true }), '0毫秒', '0毫秒');
  
  console.log('  ✓ format Chinese tests passed');
}

function testFormatSeparator() {
  console.log('Testing format separator...');
  
  assertEqual(format(9000000, { separator: ', ' }), '2h, 30m', 'comma separator');
  assertEqual(format(9000000, { separator: ' | ' }), '2h | 30m', 'pipe separator');
  
  console.log('  ✓ format separator tests passed');
}

// ==================== Other function tests ====================

function testParseFormat() {
  console.log('Testing parseFormat...');
  
  assertEqual(parseFormat('2h30m', { chinese: true }), '2小时 30分钟', 'parseFormat Chinese');
  assertEqual(parseFormat('5 minutes'), '5m', 'parseFormat short');
  assertEqual(parseFormat('1天', { short: false }), '1 day', 'parseFormat long');
  
  console.log('  ✓ parseFormat tests passed');
}

function testAddSubtractDuration() {
  console.log('Testing addDuration/subtractDuration...');
  
  const base = new Date('2024-01-01T00:00:00Z');
  
  const after1h = addDuration(base, '1h');
  assertEqual(after1h.getTime() - base.getTime(), 3600000, 'add 1h');
  
  const after1d = addDuration(base, '1d');
  assertEqual(after1d.getTime() - base.getTime(), 86400000, 'add 1d');
  
  const before1h = subtractDuration(base, '1h');
  assertEqual(base.getTime() - before1h.getTime(), 3600000, 'subtract 1h');
  
  console.log('  ✓ addDuration/subtractDuration tests passed');
}

function testDiffDates() {
  console.log('Testing diffDates...');
  
  const d1 = new Date('2024-01-01T00:00:00Z');
  const d2 = new Date('2024-01-01T02:30:00Z');
  
  assertEqual(diffDates(d1, d2), '2h 30m', 'diffDates 2h30m');
  assertEqual(diffDates(d2, d1), '2h 30m', 'diffDates reversed');
  assertEqual(diffDates(d1, d2, { chinese: true }), '2小时 30分钟', 'diffDates Chinese');
  
  console.log('  ✓ diffDates tests passed');
}

function testIsDuration() {
  console.log('Testing isDuration...');
  
  assertEqual(isDuration('2h30m'), true, '2h30m');
  assertEqual(isDuration('5 minutes'), true, '5 minutes');
  assertEqual(isDuration('1天'), true, '1天');
  assertEqual(isDuration('-1h'), true, '-1h');
  assertEqual(isDuration('hello'), false, 'hello');
  assertEqual(isDuration(''), false, 'empty');
  assertEqual(isDuration('123'), true, '123 (number only)');
  
  console.log('  ✓ isDuration tests passed');
}

function testNormalize() {
  console.log('Testing normalize...');
  
  assertEqual(normalize('2 hours 30 minutes'), '2h 30m', 'normalize long to short');
  assertEqual(normalize('1天2小时', { chinese: true }), '1天 2小时', 'normalize Chinese');
  assertEqual(normalize('1h 30m 45s'), '1h 30m 45s', 'normalize already short');
  
  console.log('  ✓ normalize tests passed');
}

function testToUnit() {
  console.log('Testing toUnit...');
  
  assertEqual(toUnit('2h30m', 'minutes'), 150, '2h30m to minutes');
  assertEqual(toUnit('1d', 'hours'), 24, '1d to hours');
  assertEqual(toUnit('1h', 'seconds'), 3600, '1h to seconds');
  assertEqual(toUnit('1w', 'days'), 7, '1w to days');
  
  let threw = false;
  try {
    toUnit('1h', 'invalid');
  } catch {
    threw = true;
  }
  assertEqual(threw, true, 'toUnit throws on invalid unit');
  
  console.log('  ✓ toUnit tests passed');
}

// ==================== Duration class tests ====================

function testDurationClass() {
  console.log('Testing Duration class...');
  
  // Constructor and from
  const d1 = new Duration(3600000);
  assertEqual(d1.toMilliseconds(), 3600000, 'Duration constructor');
  
  const d2 = Duration.from('2h30m');
  assertEqual(d2.toMilliseconds(), 9000000, 'Duration.from');
  
  // Between dates
  const date1 = new Date('2024-01-01T00:00:00Z');
  const date2 = new Date('2024-01-01T02:30:00Z');
  const d3 = Duration.between(date1, date2);
  assertEqual(d3.toMilliseconds(), 9000000, 'Duration.between');
  
  // Add/subtract
  const d4 = Duration.from('1h').add('30m');
  assertEqual(d4.toMilliseconds(), 5400000, 'Duration add');
  
  const d5 = Duration.from('2h').subtract('30m');
  assertEqual(d5.toMilliseconds(), 5400000, 'Duration subtract');
  
  // Multiply/divide
  const d6 = Duration.from('1h').multiply(2);
  assertEqual(d6.toMilliseconds(), 7200000, 'Duration multiply');
  
  const d7 = Duration.from('2h').divide(2);
  assertEqual(d7.toMilliseconds(), 3600000, 'Duration divide');
  
  // Conversion methods
  assertEqual(Duration.from('1m').toSeconds(), 60, 'toSeconds');
  assertEqual(Duration.from('2h').toMinutes(), 120, 'toMinutes');
  assertEqual(Duration.from('48h').toDays(), 2, 'toDays');
  
  // Format
  assertEqual(Duration.from('2h30m').format(), '2h 30m', 'Duration.format');
  assertEqual(Duration.from('2h30m').toString(), '2h 30m', 'Duration.toString');
  
  // Chaining
  const d8 = Duration.from('1h')
    .add('30m')
    .multiply(2)
    .subtract('15m');
  assertEqual(d8.toMilliseconds(), 9900000, 'Duration chaining');
  
  // valueOf
  assertEqual(Duration.from('1h') > Duration.from('30m'), true, 'Duration comparison');
  
  console.log('  ✓ Duration class tests passed');
}

// ==================== Helper functions ====================

function assertEqual(actual: unknown, expected: unknown, name: string): void {
  if (actual !== expected) {
    throw new Error(`Assertion failed: ${name}\n  Expected: ${expected}\n  Actual: ${actual}`);
  }
}

// ==================== Run all tests ====================

function runAllTests() {
  console.log('\n=== duration_utils tests ===\n');
  
  testParseBasic();
  testParseStrict();
  testParseNoNegative();
  testFormatBasic();
  testFormatMaxUnits();
  testFormatLong();
  testFormatChinese();
  testFormatSeparator();
  testParseFormat();
  testAddSubtractDuration();
  testDiffDates();
  testIsDuration();
  testNormalize();
  testToUnit();
  testDurationClass();
  
  console.log('\n✅ All tests passed!\n');
}

runAllTests();