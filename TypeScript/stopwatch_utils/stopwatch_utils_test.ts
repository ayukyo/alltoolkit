/**
 * Stopwatch Utilities Test Suite
 * 
 * Comprehensive tests for stopwatch, countdown timer, and formatting utilities.
 */

import {
  Stopwatch,
  CountdownTimer,
  Timer,
  millisecondsToComponents,
  componentsToMilliseconds,
  formatTime,
  formatHuman,
  parseTime,
  formatLapComparison,
  calculatePace,
  Lap,
  Split,
} from './mod.js';

// Test helper
function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function assertApprox(actual: number, expected: number, tolerance: number, message: string): void {
  if (Math.abs(actual - expected) > tolerance) {
    throw new Error(`Assertion failed: ${message}. Expected ~${expected}, got ${actual}`);
  }
}

let testsPassed = 0;
let testsFailed = 0;

function runTest(name: string, testFn: () => void): void {
  try {
    testFn();
    testsPassed++;
    console.log(`✓ ${name}`);
  } catch (error) {
    testsFailed++;
    console.log(`✗ ${name}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

// ==================== Stopwatch Tests ====================

console.log('\n=== Stopwatch Tests ===\n');

runTest('Stopwatch initial state', () => {
  const sw = new Stopwatch();
  assert(sw.isStopped(), 'Should be stopped initially');
  assert(!sw.isRunning(), 'Should not be running initially');
  assert(!sw.isPaused(), 'Should not be paused initially');
  assert(sw.getState() === 'stopped', 'State should be stopped');
  assert(sw.getElapsedTime() === 0, 'Elapsed time should be 0');
});

runTest('Stopwatch start and stop', async () => {
  const sw = new Stopwatch();
  sw.start();
  assert(sw.isRunning(), 'Should be running after start');
  
  await Timer.sleep(50);
  
  const elapsedRunning = sw.getElapsedTime();
  assert(elapsedRunning > 0, 'Should have elapsed time while running');
  
  sw.stop();
  assert(sw.isStopped(), 'Should be stopped after stop');
  
  const elapsedAfterStop = sw.getElapsedTime();
  assertApprox(elapsedAfterStop, elapsedRunning, 1, 'Time should freeze after stop');
  
  // Wait more and verify time doesn't change
  await Timer.sleep(50);
  assertApprox(sw.getElapsedTime(), elapsedAfterStop, 1, 'Time should not increase after stop');
});

runTest('Stopwatch pause and resume', async () => {
  const sw = new Stopwatch();
  sw.start();
  
  await Timer.sleep(50);
  const elapsed1 = sw.getElapsedTime();
  
  sw.pause();
  assert(sw.isPaused(), 'Should be paused');
  
  await Timer.sleep(50);
  const elapsedPaused = sw.getElapsedTime();
  assertApprox(elapsedPaused, elapsed1, 1, 'Time should not increase while paused');
  
  sw.resume();
  assert(sw.isRunning(), 'Should be running after resume');
  
  await Timer.sleep(50);
  const elapsed2 = sw.getElapsedTime();
  assert(elapsed2 > elapsed1, 'Time should increase after resume');
});

runTest('Stopwatch reset', async () => {
  const sw = new Stopwatch();
  sw.start();
  
  await Timer.sleep(50);
  sw.stop();
  
  assert(sw.getElapsedTime() > 0, 'Should have elapsed time');
  
  sw.reset();
  assert(sw.getElapsedTime() === 0, 'Elapsed time should be 0 after reset');
  assert(sw.isStopped(), 'Should be stopped after reset');
  assert(sw.getLaps().length === 0, 'Laps should be cleared');
  assert(sw.getSplits().length === 0, 'Splits should be cleared');
});

runTest('Stopwatch lap recording', async () => {
  const sw = new Stopwatch();
  sw.start();
  
  await Timer.sleep(30);
  const lap1 = sw.lap();
  assert(lap1.number === 1, 'Lap number should be 1');
  assert(lap1.duration > 0, 'Lap duration should be positive');
  assert(lap1.cumulativeTime === lap1.endTime, 'Cumulative time should match end time');
  
  await Timer.sleep(30);
  const lap2 = sw.lap();
  assert(lap2.number === 2, 'Lap number should be 2');
  assert(lap2.startTime === lap1.endTime, 'Lap start should be previous lap end');
  
  const laps = sw.getLaps();
  assert(laps.length === 2, 'Should have 2 laps');
});

runTest('Stopwatch split recording', async () => {
  const sw = new Stopwatch();
  sw.start();
  
  await Timer.sleep(20);
  const split1 = sw.split('checkpoint 1');
  assert(split1.number === 1, 'Split number should be 1');
  assert(split1.label === 'checkpoint 1', 'Split label should match');
  assert(split1.cumulativeTime > 0, 'Split should have cumulative time');
  
  await Timer.sleep(20);
  const split2 = sw.split();
  assert(split2.number === 2, 'Split number should be 2');
  
  const splits = sw.getSplits();
  assert(splits.length === 2, 'Should have 2 splits');
});

runTest('Stopwatch statistics', async () => {
  const sw = new Stopwatch();
  sw.start();
  
  await Timer.sleep(20);
  sw.lap();
  
  await Timer.sleep(30);
  sw.lap();
  
  await Timer.sleep(10);
  sw.lap();
  
  const stats = sw.getStats();
  assert(stats !== undefined, 'Should have stats');
  assert(stats!.lapCount === 3, 'Should have 3 laps');
  assert(stats!.bestLapTime <= stats!.worstLapTime, 'Best should be <= worst');
  
  // Verify lap time range
  const durations = sw.getLaps().map(l => l.duration);
  const expectedBest = Math.min(...durations);
  const expectedWorst = Math.max(...durations);
  assertApprox(stats!.bestLapTime, expectedBest, 1, 'Best lap should match');
  assertApprox(stats!.worstLapTime, expectedWorst, 1, 'Worst lap should match');
});

runTest('Stopwatch cannot lap when not running', () => {
  const sw = new Stopwatch();
  
  let threw = false;
  try {
    sw.lap();
  } catch (e) {
    threw = true;
  }
  assert(threw, 'Should throw when lap called on stopped stopwatch');
});

runTest('Stopwatch cannot start twice', () => {
  const sw = new Stopwatch();
  sw.start();
  
  let threw = false;
  try {
    sw.start();
  } catch (e) {
    threw = true;
  }
  assert(threw, 'Should throw when start called twice');
});

// ==================== CountdownTimer Tests ====================

console.log('\n=== CountdownTimer Tests ===\n');

runTest('CountdownTimer initial state', () => {
  const countdown = new CountdownTimer(1000);
  assert(!countdown.isRunning(), 'Should not be running initially');
  assert(countdown.getRemaining() === 1000, 'Remaining should be 1000');
  assert(countdown.getProgress() === 0, 'Progress should be 0');
  assert(!countdown.isComplete(), 'Should not be complete');
});

runTest('CountdownTimer start and tick', async () => {
  let tickCount = 0;
  let lastRemaining = 1000;
  
  const countdown = new CountdownTimer(100, {
    tickInterval: 20,
    onTick: (remaining) => {
      tickCount++;
      assert(remaining <= lastRemaining, 'Remaining should decrease');
      lastRemaining = remaining;
    },
  });
  
  countdown.start();
  
  await Timer.sleep(150);
  
  assert(tickCount > 0, 'Should have received ticks');
  assert(countdown.isComplete(), 'Should be complete');
  assert(countdown.getRemaining() === 0, 'Remaining should be 0');
});

runTest('CountdownTimer pause and resume', async () => {
  const countdown = new CountdownTimer(200, { tickInterval: 50 });
  countdown.start();
  
  await Timer.sleep(50);
  const remaining1 = countdown.getRemaining();
  
  countdown.pause();
  assert(countdown.isPaused(), 'Should be paused');
  
  await Timer.sleep(50);
  const remaining2 = countdown.getRemaining();
  assertApprox(remaining2, remaining1, 20, 'Remaining should not change much while paused');
  
  countdown.resume();
  assert(countdown.isRunning(), 'Should be running after resume');
  
  await Timer.sleep(250);
  assert(countdown.isComplete(), 'Should be complete');
});

runTest('CountdownTimer reset', async () => {
  const countdown = new CountdownTimer(100, { tickInterval: 20 });
  countdown.start();
  
  await Timer.sleep(50);
  
  countdown.reset();
  assert(countdown.getRemaining() === 100, 'Remaining should be back to original');
  assert(!countdown.isRunning(), 'Should not be running after reset');
});

runTest('CountdownTimer onComplete callback', async () => {
  let completed = false;
  
  const countdown = new CountdownTimer(50, {
    tickInterval: 10,
    onComplete: () => {
      completed = true;
    },
  });
  
  countdown.start();
  
  await Timer.sleep(100);
  
  assert(completed, 'onComplete should have been called');
});

runTest('CountdownTimer progress', async () => {
  const countdown = new CountdownTimer(100, { tickInterval: 10 });
  countdown.start();
  
  await Timer.sleep(50);
  const progress = countdown.getProgress();
  assert(progress > 40 && progress < 60, `Progress should be around 50%, got ${progress}`);
});

// ==================== Timer Tests ====================

console.log('\n=== Timer Tests ===\n');

runTest('Timer.time synchronous', () => {
  const result = Timer.time(() => {
    // Simulate some work
    let sum = 0;
    for (let i = 0; i < 1000; i++) {
      sum += i;
    }
    return sum;
  });
  
  assert(result.result === 499500, 'Result should be correct');
  assert(result.duration >= 0, 'Duration should be positive');
});

runTest('Timer.timeAsync asynchronous', async () => {
  const result = await Timer.timeAsync(async () => {
    await Timer.sleep(50);
    return 'done';
  });
  
  assert(result.result === 'done', 'Result should be correct');
  assertApprox(result.duration, 50, 10, 'Duration should be around 50ms');
});

runTest('Timer.benchmark', () => {
  const bench = Timer.benchmark(() => {
    let sum = 0;
    for (let i = 0; i < 100; i++) {
      sum += i;
    }
  }, 10);
  
  assert(bench.iterations === 10, 'Should have 10 iterations');
  assert(bench.averageTime >= 0, 'Average time should be positive');
  assert(bench.minTime <= bench.maxTime, 'Min should be <= max');
  assert(bench.times.length === 10, 'Should have 10 time samples');
});

runTest('Timer.create', async () => {
  const getElapsed = Timer.create();
  
  await Timer.sleep(30);
  
  const elapsed = getElapsed();
  assertApprox(elapsed, 30, 10, 'Elapsed should be around 30ms');
});

runTest('Timer.sleep', async () => {
  const start = performance.now();
  await Timer.sleep(50);
  const elapsed = performance.now() - start;
  assertApprox(elapsed, 50, 10, 'Sleep should last around 50ms');
});

// ==================== Formatting Tests ====================

console.log('\n=== Formatting Tests ===\n');

runTest('millisecondsToComponents', () => {
  const comp = millisecondsToComponents(3661500);
  assert(comp.hours === 1, 'Hours should be 1');
  assert(comp.minutes === 1, 'Minutes should be 1');
  assert(comp.seconds === 1, 'Seconds should be 1');
  assert(comp.milliseconds === 500, 'Milliseconds should be 500');
  
  // Edge case: zero
  const zero = millisecondsToComponents(0);
  assert(zero.hours === 0 && zero.minutes === 0 && zero.seconds === 0 && zero.milliseconds === 0, 'Zero should be all zeros');
  
  // Edge case: large value
  const large = millisecondsToComponents(86400000 + 3600000 + 60000 + 1000 + 500);
  assert(large.hours === 25, '25 hours');
  assert(large.minutes === 1, '1 minute');
  assert(large.seconds === 1, '1 second');
  assert(large.milliseconds === 500, '500 ms');
});

runTest('componentsToMilliseconds', () => {
  const ms = componentsToMilliseconds({ hours: 1, minutes: 1, seconds: 1, milliseconds: 500 });
  assert(ms === 3661500, 'Should be 3661500');
});

runTest('formatTime basic', () => {
  assert(formatTime(3661500, 'HH:mm:ss.SSS') === '01:01:01.500', 'Full format');
  assert(formatTime(3661500, 'H:m:s') === '1:1:1', 'Short format');
  assert(formatTime(5000, 'mm:ss') === '00:05', '5 seconds');
  assert(formatTime(60000, 'mm:ss') === '01:00', '1 minute');
  assert(formatTime(3600000, 'HH:mm') === '01:00', '1 hour');
});

runTest('formatTime edge cases', () => {
  assert(formatTime(0, 'HH:mm:ss.SSS') === '00:00:00.000', 'Zero time');
  assert(formatTime(500, 'SSS') === '500', 'Just milliseconds');
  assert(formatTime(100, 'SS') === '10', 'Milliseconds in SS');
  assert(formatTime(50, 'S') === '0', 'Milliseconds in S');
});

runTest('formatHuman full', () => {
  assert(formatHuman(3661500) === '1 hour, 1 minute, 1 second and 500 milliseconds', 'Full format');
  assert(formatHuman(60000) === '1 minute', 'Single unit');
  assert(formatHuman(61000) === '1 minute and 1 second', 'Two units');
  assert(formatHuman(3661000) === '1 hour, 1 minute and 1 second', 'No milliseconds');
});

runTest('formatHuman compact', () => {
  assert(formatHuman(3661500, { compact: true }) === '1h 1m 1s 500ms', 'Compact format');
  assert(formatHuman(0, { compact: true }) === '0ms', 'Zero compact');
});

runTest('formatHuman options', () => {
  assert(formatHuman(0) === '0 milliseconds', 'Zero without options');
  assert(formatHuman(0, { showZeroValues: true }) === '0 hours, 0 minutes, 0 seconds and 0 milliseconds', 'Show zeros');
  assert(formatHuman(3661500, { showMs: false }) === '1 hour, 1 minute and 1 second', 'Hide milliseconds');
});

runTest('parseTime HH:MM:SS format', () => {
  // 1:30:45 = 1 hour + 30 minutes + 45 seconds = 3600000 + 1800000 + 45000 = 5445000
  assert(parseTime('1:30:45') === 5445000, '1:30:45');
  // 1:30:45.500 = 5445000 + 500 = 5445500
  assert(parseTime('1:30:45.500') === 5445500, '1:30:45.500');
  assert(parseTime('0:00:00') === 0, 'Zero');
  assert(parseTime('10:00:00') === 36000000, '10 hours');
});

runTest('parseTime MM:SS format', () => {
  assert(parseTime('5:30') === 330000, '5:30');
  assert(parseTime('0:00') === 0, 'Zero');
  assert(parseTime('90:00') === 5400000, '90 minutes');
});

runTest('parseTime single unit format', () => {
  assert(parseTime('30s') === 30000, '30s');
  assert(parseTime('5m') === 300000, '5m');
  assert(parseTime('1h') === 3600000, '1h');
  assert(parseTime('500ms') === 500, '500ms');
});

runTest('parseTime combined format', () => {
  assert(parseTime('1h30m') === 5400000, '1h30m');
  assert(parseTime('1h30m45s') === 5445000, '1h30m45s');
  assert(parseTime('1h30m45s500ms') === 5445500, '1h30m45s500ms');
});

runTest('parseTime word format', () => {
  assert(parseTime('1 hour') === 3600000, '1 hour');
  assert(parseTime('2 hours') === 7200000, '2 hours');
  assert(parseTime('30 seconds') === 30000, '30 seconds');
  assert(parseTime('5 minutes') === 300000, '5 minutes');
});

runTest('parseTime invalid', () => {
  assert(parseTime('invalid') === null, 'Invalid string');
  assert(parseTime('') === null, 'Empty string');
  assert(parseTime('abc123') === null, 'Mixed invalid');
});

runTest('formatLapComparison', () => {
  const lap1: Lap = { number: 1, startTime: 0, endTime: 100, duration: 100, cumulativeTime: 100 };
  const lap2: Lap = { number: 2, startTime: 100, endTime: 150, duration: 50, cumulativeTime: 150 };
  
  assert(formatLapComparison(lap1) === 'Lap 1: 00:00.100', 'Lap without comparison');
  assert(formatLapComparison(lap2, lap1) === 'Lap 2: 00:00.050 (-00.050)', 'Lap with faster comparison');
  
  const lap3: Lap = { number: 3, startTime: 150, endTime: 200, duration: 100, cumulativeTime: 200 };
  assert(formatLapComparison(lap3, lap2) === 'Lap 3: 00:00.100 (+00.050)', 'Lap with slower comparison');
});

runTest('calculatePace', () => {
  const pace = calculatePace(120000, 4, 'lap');
  assertApprox(pace.timePerUnit, 30000, 1, '30 seconds per lap');
  assert(pace.formatted.includes('30'), 'Formatted should show 30');
  assert(pace.unitName === 'lap', 'Unit name should be lap');
});

// ==================== Summary ====================

console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);

if (testsFailed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed!');
}