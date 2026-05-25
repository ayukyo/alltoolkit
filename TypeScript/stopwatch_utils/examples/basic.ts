/**
 * Stopwatch Utilities - Examples
 * 
 * This file demonstrates the usage of stopwatch_utils module.
 */

import {
  Stopwatch,
  CountdownTimer,
  Timer,
  formatTime,
  formatHuman,
  parseTime,
  calculatePace,
} from '../mod.ts';

// ==================== Stopwatch Examples ====================

console.log('=== Stopwatch Examples ===\n');

// Example 1: Basic stopwatch usage
console.log('Example 1: Basic Stopwatch');
const stopwatch = new Stopwatch();
stopwatch.start();

// Simulate some work
for (let i = 0; i < 1000000; i++) {
  // Busy work
}

const elapsed = stopwatch.getElapsedTime();
console.log(`Elapsed time: ${formatTime(elapsed, 'HH:mm:ss.SSS')}`);
console.log(`Human-readable: ${formatHuman(elapsed)}`);
stopwatch.stop();
console.log();

// Example 2: Lap timing (simulated race)
console.log('Example 2: Lap Timing (Race Simulation)');
const raceTimer = new Stopwatch();
raceTimer.start();

// Simulate 4 laps with varying durations
console.log('Running 4 laps...\n');

for (let lap = 1; lap <= 4; lap++) {
  // Simulate lap duration (varying)
  const lapTime = 1000 + Math.random() * 500;
  await new Promise(resolve => setTimeout(resolve, lapTime));
  
  const lapRecord = raceTimer.lap();
  console.log(`Lap ${lapRecord.number}: ${formatTime(lapRecord.duration, 'mm:ss.SSS')}`);
}

// Get statistics
const stats = raceTimer.getStats();
if (stats) {
  console.log('\nRace Statistics:');
  console.log(`  Total time: ${formatTime(stats.totalTime, 'mm:ss.SSS')}`);
  console.log(`  Average lap: ${formatTime(stats.averageLapTime, 'ss.SSS')}`);
  console.log(`  Best lap: ${formatTime(stats.bestLapTime, 'ss.SSS')} (Lap ${stats.bestLapNumber})`);
  console.log(`  Worst lap: ${formatTime(stats.worstLapTime, 'ss.SSS')} (Lap ${stats.worstLapNumber})`);
  console.log(`  Consistency (std dev): ${formatTime(stats.lapTimeStdDev, 'ss.SSS')}`);
}
console.log();

// Example 3: Split times (checkpoint tracking)
console.log('Example 3: Split Times (Checkpoint Tracking)');
const checkpointTimer = new Stopwatch();
checkpointTimer.start();

console.log('Processing items with checkpoints...\n');

// Process items and record splits
const items = ['Item A', 'Item B', 'Item C', 'Item D'];
for (const item of items) {
  await new Promise(resolve => setTimeout(resolve, 200 + Math.random() * 100));
  const split = checkpointTimer.split(`Completed ${item}`);
  console.log(`${item}: Split at ${formatTime(split.cumulativeTime, 'ss.SSS')}`);
}

// Show all splits
console.log('\nAll splits:');
checkpointTimer.getSplits().forEach(split => {
  console.log(`  ${split.number}: ${split.label} at ${formatTime(split.cumulativeTime, 'ss.SSS')}`);
});
console.log();

// ==================== CountdownTimer Examples ====================

console.log('=== CountdownTimer Examples ===\n');

// Example 4: Simple countdown
console.log('Example 4: Countdown Timer (5 seconds)');
const countdown = new CountdownTimer(5000, {
  tickInterval: 500,
  onTick: (remaining) => {
    console.log(`  Remaining: ${formatTime(remaining, 'ss.SSS')}`);
  },
  onComplete: () => {
    console.log('  ✅ Countdown complete!');
  },
});

console.log('Starting countdown...');
countdown.start();

await new Promise(resolve => setTimeout(resolve, 6000));
console.log();

// Example 5: Countdown with pause/resume
console.log('Example 5: Countdown with Pause/Resume');
const workoutTimer = new CountdownTimer(3000, {
  tickInterval: 500,
  onTick: (remaining) => {
    console.log(`  Remaining: ${formatTime(remaining, 'ss.SSS')} (${workoutTimer.getProgress().toFixed(1)}%)`);
  },
  onComplete: () => {
    console.log('  ✅ Workout timer complete!');
  },
  onPause: () => {
    console.log('  ⏸️ Timer paused');
  },
  onResume: () => {
    console.log('  ▶️ Timer resumed');
  },
});

workoutTimer.start();
await new Promise(resolve => setTimeout(resolve, 1500));

workoutTimer.pause();
await new Promise(resolve => setTimeout(resolve, 1000));

workoutTimer.resume();
await new Promise(resolve => setTimeout(resolve, 3000));
console.log();

// ==================== Timer Examples ====================

console.log('=== Timer Examples ===\n');

// Example 6: Measure function execution time
console.log('Example 6: Measure Function Execution');
const result = Timer.time(() => {
  let sum = 0;
  for (let i = 0; i < 10000000; i++) {
    sum += i;
  }
  return sum;
});
console.log(`  Result: ${result.result}`);
console.log(`  Duration: ${formatTime(result.duration, 'ss.SSS')}`);
console.log();

// Example 7: Benchmark function
console.log('Example 7: Benchmark Function');
const benchResult = Timer.benchmark(() => {
  let arr = [];
  for (let i = 0; i < 1000; i++) {
    arr.push(i);
  }
  return arr;
}, 10);
console.log(`  Iterations: ${benchResult.iterations}`);
console.log(`  Average: ${formatTime(benchResult.averageTime, 'ss.SSS')}`);
console.log(`  Min: ${formatTime(benchResult.minTime, 'ss.SSS')}`);
console.log(`  Max: ${formatTime(benchResult.maxTime, 'ss.SSS')}`);
console.log();

// ==================== Formatting Examples ====================

console.log('=== Formatting Examples ===\n');

// Example 8: Format time in different ways
console.log('Example 8: Time Formatting');
const sampleTime = 3661500; // 1 hour, 1 minute, 1 second, 500 ms
console.log(`  Standard: ${formatTime(sampleTime, 'HH:mm:ss.SSS')}`);
console.log(`  Compact: ${formatTime(sampleTime, 'H:m:s.S')}`);
console.log(`  Human: ${formatHuman(sampleTime)}`);
console.log(`  Human compact: ${formatHuman(sampleTime, { compact: true })}`);
console.log();

// Example 9: Parse time strings
console.log('Example 9: Parse Time Strings');
console.log(`  '1:30:45' -> ${parseTime('1:30:45')} ms`);
console.log(`  '5:30' -> ${parseTime('5:30')} ms`);
console.log(`  '1h30m' -> ${parseTime('1h30m')} ms`);
console.log(`  '500ms' -> ${parseTime('500ms')} ms`);
console.log(`  '2 hours 30 minutes' -> ${parseTime('2 hours 30 minutes')} ms`);
console.log();

// Example 10: Calculate pace
console.log('Example 10: Calculate Pace');
const raceTime = 3600000; // 1 hour
const laps = 10;
const pace = calculatePace(raceTime, laps, 'lap');
console.log(`  Race time: ${formatTime(raceTime, 'HH:mm:ss')}`);
console.log(`  Laps: ${laps}`);
console.log(`  Pace: ${pace.formatted}`);
console.log();

console.log('=== All Examples Complete ===');