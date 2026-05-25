/**
 * Stopwatch Utilities - TypeScript
 * 
 * A comprehensive stopwatch and timer utility module providing high-precision
 * timing, lap tracking, split times, and formatting capabilities with zero dependencies.
 * 
 * Features:
 * - High-precision stopwatch with start/stop/reset
 * - Lap time tracking with statistics
 * - Split times (snapshots without stopping)
 * - Countdown timer with callbacks
 * - Formatted output (human-readable, ISO, custom formats)
 * - Statistical analysis (average lap, best lap, worst lap)
 * - Multiple timer instances
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module stopwatch_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Represents a single lap record
 */
export interface Lap {
  /** Lap number (1-indexed) */
  number: number;
  /** Lap start time in milliseconds (absolute) */
  startTime: number;
  /** Lap end time in milliseconds (absolute) */
  endTime: number;
  /** Lap duration in milliseconds */
  duration: number;
  /** Cumulative time up to this lap in milliseconds */
  cumulativeTime: number;
}

/**
 * Represents a split (snapshot) time
 */
export interface Split {
  /** Split number (1-indexed) */
  number: number;
  /** Time in milliseconds when split was taken */
  time: number;
  /** Cumulative time when split was taken */
  cumulativeTime: number;
  /** Optional label for the split */
  label?: string;
}

/**
 * Stopwatch statistics
 */
export interface StopwatchStats {
  /** Total elapsed time in milliseconds */
  totalTime: number;
  /** Number of laps recorded */
  lapCount: number;
  /** Average lap time in milliseconds */
  averageLapTime: number;
  /** Best (fastest) lap time in milliseconds */
  bestLapTime: number;
  /** Best lap number */
  bestLapNumber: number;
  /** Worst (slowest) lap time in milliseconds */
  worstLapTime: number;
  /** Worst lap number */
  worstLapNumber: number;
  /** Lap time standard deviation in milliseconds */
  lapTimeStdDev: number;
  /** First lap time in milliseconds */
  firstLapTime: number;
  /** Last lap time in milliseconds */
  lastLapTime: number;
  /** Range between best and worst lap (ms) */
  lapTimeRange: number;
}

/**
 * Stopwatch state
 */
export type StopwatchState = 'stopped' | 'running' | 'paused';

/**
 * Time components for formatting
 */
export interface TimeComponents {
  hours: number;
  minutes: number;
  seconds: number;
  milliseconds: number;
}

/**
 * High-precision stopwatch with lap and split tracking
 * 
 * @example
 * ```typescript
 * const stopwatch = new Stopwatch();
 * stopwatch.start();
 * // ... do work ...
 * const lap1 = stopwatch.lap();
 * // ... more work ...
 * const lap2 = stopwatch.lap();
 * stopwatch.stop();
 * console.log(stopwatch.getStats());
 * ```
 */
export class Stopwatch {
  private startTime: number = 0;
  private pausedTime: number = 0;
  private accumulatedTime: number = 0;
  private state: StopwatchState = 'stopped';
  private laps: Lap[] = [];
  private splits: Split[] = [];
  private lastLapTime: number = 0;
  private splitCounter: number = 0;

  /**
   * Start the stopwatch
   * @returns The stopwatch instance for chaining
   * @throws Error if stopwatch is already running
   */
  start(): Stopwatch {
    if (this.state === 'running') {
      throw new Error('Stopwatch is already running');
    }
    
    this.startTime = performance.now();
    
    if (this.state === 'paused') {
      // Resuming from pause - adjust start time to account for paused duration
      this.startTime -= this.pausedTime;
    } else {
      // Fresh start - reset everything
      this.accumulatedTime = 0;
      this.laps = [];
      this.splits = [];
      this.lastLapTime = 0;
      this.splitCounter = 0;
    }
    
    this.state = 'running';
    return this;
  }

  /**
   * Stop the stopwatch
   * @returns The stopwatch instance for chaining
   */
  stop(): Stopwatch {
    if (this.state !== 'running') {
      return this;
    }
    
    this.accumulatedTime = this.getElapsedTime();
    this.state = 'stopped';
    return this;
  }

  /**
   * Pause the stopwatch
   * @returns The stopwatch instance for chaining
   */
  pause(): Stopwatch {
    if (this.state !== 'running') {
      return this;
    }
    
    this.accumulatedTime = this.getElapsedTime();
    this.pausedTime = 0;
    this.state = 'paused';
    return this;
  }

  /**
   * Resume the stopwatch from pause
   * @returns The stopwatch instance for chaining
   */
  resume(): Stopwatch {
    if (this.state !== 'paused') {
      return this;
    }
    
    this.start();
    return this;
  }

  /**
   * Reset the stopwatch to initial state
   * @returns The stopwatch instance for chaining
   */
  reset(): Stopwatch {
    this.startTime = 0;
    this.accumulatedTime = 0;
    this.pausedTime = 0;
    this.state = 'stopped';
    this.laps = [];
    this.splits = [];
    this.lastLapTime = 0;
    this.splitCounter = 0;
    return this;
  }

  /**
   * Record a lap time
   * @param label - Optional label for the lap
   * @returns The recorded lap
   * @throws Error if stopwatch is not running
   */
  lap(label?: string): Lap {
    if (this.state !== 'running') {
      throw new Error('Stopwatch must be running to record a lap');
    }
    
    const currentTime = this.getElapsedTime();
    const lapDuration = currentTime - this.lastLapTime;
    const lapNumber = this.laps.length + 1;
    
    const lap: Lap = {
      number: lapNumber,
      startTime: this.lastLapTime,
      endTime: currentTime,
      duration: lapDuration,
      cumulativeTime: currentTime,
    };
    
    this.laps.push(lap);
    this.lastLapTime = currentTime;
    
    return lap;
  }

  /**
   * Record a split (snapshot without stopping)
   * @param label - Optional label for the split
   * @returns The recorded split
   * @throws Error if stopwatch is not running
   */
  split(label?: string): Split {
    if (this.state !== 'running') {
      throw new Error('Stopwatch must be running to record a split');
    }
    
    const currentTime = this.getElapsedTime();
    this.splitCounter++;
    
    const split: Split = {
      number: this.splitCounter,
      time: performance.now(),
      cumulativeTime: currentTime,
      label,
    };
    
    this.splits.push(split);
    return split;
  }

  /**
   * Get the current elapsed time in milliseconds
   * @returns Elapsed time in milliseconds
   */
  getElapsedTime(): number {
    if (this.state === 'stopped') {
      return this.accumulatedTime;
    }
    
    if (this.state === 'paused') {
      return this.accumulatedTime;
    }
    
    return performance.now() - this.startTime + this.accumulatedTime;
  }

  /**
   * Get the current state of the stopwatch
   * @returns The current state
   */
  getState(): StopwatchState {
    return this.state;
  }

  /**
   * Check if the stopwatch is currently running
   * @returns True if running
   */
  isRunning(): boolean {
    return this.state === 'running';
  }

  /**
   * Check if the stopwatch is paused
   * @returns True if paused
   */
  isPaused(): boolean {
    return this.state === 'paused';
  }

  /**
   * Check if the stopwatch is stopped
   * @returns True if stopped
   */
  isStopped(): boolean {
    return this.state === 'stopped';
  }

  /**
   * Get all recorded laps
   * @returns Array of laps
   */
  getLaps(): Lap[] {
    return [...this.laps];
  }

  /**
   * Get all recorded splits
   * @returns Array of splits
   */
  getSplits(): Split[] {
    return [...this.splits];
  }

  /**
   * Get the last lap
   * @returns The last lap or undefined if no laps recorded
   */
  getLastLap(): Lap | undefined {
    return this.laps.length > 0 ? this.laps[this.laps.length - 1] : undefined;
  }

  /**
   * Get the last split
   * @returns The last split or undefined if no splits recorded
   */
  getLastSplit(): Split | undefined {
    return this.splits.length > 0 ? this.splits[this.splits.length - 1] : undefined;
  }

  /**
   * Get a lap by number
   * @param number - Lap number (1-indexed)
   * @returns The lap or undefined if not found
   */
  getLap(number: number): Lap | undefined {
    return this.laps.find(lap => lap.number === number);
  }

  /**
   * Get a split by number
   * @param number - Split number (1-indexed)
   * @returns The split or undefined if not found
   */
  getSplit(number: number): Split | undefined {
    return this.splits.find(split => split.number === number);
  }

  /**
   * Get statistics about recorded laps
   * @returns Statistics object or undefined if no laps
   */
  getStats(): StopwatchStats | undefined {
    if (this.laps.length === 0) {
      return undefined;
    }
    
    const durations = this.laps.map(lap => lap.duration);
    const totalTime = this.getElapsedTime();
    
    const averageLapTime = durations.reduce((a, b) => a + b, 0) / durations.length;
    const bestLapTime = Math.min(...durations);
    const worstLapTime = Math.max(...durations);
    const bestLapNumber = durations.indexOf(bestLapTime) + 1;
    const worstLapNumber = durations.indexOf(worstLapTime) + 1;
    
    // Calculate standard deviation
    const variance = durations.reduce((sum, d) => sum + Math.pow(d - averageLapTime, 2), 0) / durations.length;
    const lapTimeStdDev = Math.sqrt(variance);
    
    return {
      totalTime,
      lapCount: this.laps.length,
      averageLapTime,
      bestLapTime,
      bestLapNumber,
      worstLapTime,
      worstLapNumber,
      lapTimeStdDev,
      firstLapTime: durations[0],
      lastLapTime: durations[durations.length - 1],
      lapTimeRange: worstLapTime - bestLapTime,
    };
  }

  /**
   * Get the elapsed time as formatted string
   * @param format - Format pattern (default: 'HH:mm:ss.SSS')
   * @returns Formatted time string
   */
  format(format: string = 'HH:mm:ss.SSS'): string {
    return formatTime(this.getElapsedTime(), format);
  }
}

/**
 * Countdown timer with callback support
 * 
 * @example
 * ```typescript
 * const countdown = new CountdownTimer(60000, {
 *   onTick: (remaining) => console.log(`${remaining}ms remaining`),
 *   onComplete: () => console.log('Done!'),
 * });
 * countdown.start();
 * ```
 */
export class CountdownTimer {
  private duration: number;
  private remaining: number = 0;
  private startTime: number = 0;
  private pausedRemaining: number = 0;
  private state: StopwatchState = 'stopped';
  private intervalId: ReturnType<typeof setInterval> | null = null;
  private tickInterval: number;
  
  private onTick?: (remaining: number) => void;
  private onComplete?: () => void;
  private onStart?: () => void;
  private onPause?: () => void;
  private onResume?: () => void;
  private onReset?: () => void;

  /**
   * Create a new countdown timer
   * @param durationMs - Duration in milliseconds
   * @param options - Optional callbacks and configuration
   */
  constructor(
    durationMs: number,
    options?: {
      onTick?: (remaining: number) => void;
      onComplete?: () => void;
      onStart?: () => void;
      onPause?: () => void;
      onResume?: () => void;
      onReset?: () => void;
      tickInterval?: number;
    }
  ) {
    this.duration = durationMs;
    this.remaining = durationMs;
    this.tickInterval = options?.tickInterval ?? 100;
    
    if (options) {
      this.onTick = options.onTick;
      this.onComplete = options.onComplete;
      this.onStart = options.onStart;
      this.onPause = options.onPause;
      this.onResume = options.onResume;
      this.onReset = options.onReset;
    }
  }

  /**
   * Start the countdown
   * @returns The timer instance for chaining
   */
  start(): CountdownTimer {
    if (this.state === 'running') {
      return this;
    }
    
    this.startTime = performance.now();
    this.state = 'running';
    
    if (this.state === 'paused') {
      this.duration = this.pausedRemaining;
    }
    
    this.onStart?.();
    
    this.intervalId = setInterval(() => {
      this.update();
    }, this.tickInterval);
    
    return this;
  }

  /**
   * Pause the countdown
   * @returns The timer instance for chaining
   */
  pause(): CountdownTimer {
    if (this.state !== 'running') {
      return this;
    }
    
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    this.pausedRemaining = this.remaining;
    this.state = 'paused';
    this.onPause?.();
    
    return this;
  }

  /**
   * Resume the countdown from pause
   * @returns The timer instance for chaining
   */
  resume(): CountdownTimer {
    if (this.state !== 'paused') {
      return this;
    }
    
    this.duration = this.pausedRemaining;
    this.startTime = performance.now();
    this.state = 'running';
    
    this.onResume?.();
    
    this.intervalId = setInterval(() => {
      this.update();
    }, this.tickInterval);
    
    return this;
  }

  /**
   * Stop and reset the countdown
   * @returns The timer instance for chaining
   */
  stop(): CountdownTimer {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    this.remaining = 0;
    this.state = 'stopped';
    
    return this;
  }

  /**
   * Reset the countdown to initial duration
   * @returns The timer instance for chaining
   */
  reset(): CountdownTimer {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    this.remaining = this.duration;
    this.pausedRemaining = 0;
    this.state = 'stopped';
    this.onReset?.();
    
    return this;
  }

  /**
   * Set a new duration
   * @param durationMs - New duration in milliseconds
   * @returns The timer instance for chaining
   */
  setDuration(durationMs: number): CountdownTimer {
    this.duration = durationMs;
    this.remaining = durationMs;
    this.pausedRemaining = durationMs;
    return this;
  }

  /**
   * Get the remaining time in milliseconds
   * @returns Remaining time in milliseconds
   */
  getRemaining(): number {
    if (this.state === 'paused') {
      return this.pausedRemaining;
    }
    
    if (this.state === 'running') {
      return Math.max(0, this.duration - (performance.now() - this.startTime));
    }
    
    return this.remaining;
  }

  /**
   * Get the elapsed time in milliseconds
   * @returns Elapsed time in milliseconds
   */
  getElapsed(): number {
    return this.duration - this.getRemaining();
  }

  /**
   * Get the progress as a percentage (0-100)
   * @returns Progress percentage
   */
  getProgress(): number {
    if (this.duration === 0) return 100;
    return ((this.duration - this.getRemaining()) / this.duration) * 100;
  }

  /**
   * Get the current state
   * @returns The current state
   */
  getState(): StopwatchState {
    return this.state;
  }

  /**
   * Check if the countdown is running
   * @returns True if running
   */
  isRunning(): boolean {
    return this.state === 'running';
  }

  /**
   * Check if the countdown is complete
   * @returns True if complete
   */
  isComplete(): boolean {
    return this.getRemaining() <= 0;
  }

  /**
   * Check if the countdown is paused
   * @returns True if paused
   */
  isPaused(): boolean {
    return this.state === 'paused';
  }

  /**
   * Format the remaining time
   * @param format - Format pattern
   * @returns Formatted time string
   */
  format(format: string = 'HH:mm:ss.SSS'): string {
    return formatTime(this.getRemaining(), format);
  }

  /**
   * Update internal state (called by interval)
   */
  private update(): void {
    if (this.state !== 'running') return;
    
    this.remaining = Math.max(0, this.duration - (performance.now() - this.startTime));
    
    this.onTick?.(this.remaining);
    
    if (this.remaining <= 0) {
      this.complete();
    }
  }

  /**
   * Handle countdown completion
   */
  private complete(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    this.state = 'stopped';
    this.remaining = 0;
    this.onComplete?.();
  }
}

/**
 * Timer for measuring function execution time
 * 
 * @example
 * ```typescript
 * const result = Timer.time(() => expensiveOperation());
 * console.log(`Took ${result.duration}ms`);
 * ```
 */
export class Timer {
  /**
   * Measure execution time of a synchronous function
   * @param fn - Function to measure
   * @returns Object with result and duration
   */
  static time<T>(fn: () => T): { result: T; duration: number } {
    const start = performance.now();
    const result = fn();
    const duration = performance.now() - start;
    return { result, duration };
  }

  /**
   * Measure execution time of an async function
   * @param fn - Async function to measure
   * @returns Promise with result and duration
   */
  static async timeAsync<T>(fn: () => Promise<T>): Promise<{ result: T; duration: number }> {
    const start = performance.now();
    const result = await fn();
    const duration = performance.now() - start;
    return { result, duration };
  }

  /**
   * Run a function multiple times and return statistics
   * @param fn - Function to benchmark
   * @param iterations - Number of iterations
   * @returns Benchmark results
   */
  static benchmark(
    fn: () => void,
    iterations: number = 100
  ): {
    iterations: number;
    totalTime: number;
    averageTime: number;
    minTime: number;
    maxTime: number;
    times: number[];
  } {
    const times: number[] = [];
    let totalTime = 0;
    
    for (let i = 0; i < iterations; i++) {
      const start = performance.now();
      fn();
      const duration = performance.now() - start;
      times.push(duration);
      totalTime += duration;
    }
    
    return {
      iterations,
      totalTime,
      averageTime: totalTime / iterations,
      minTime: Math.min(...times),
      maxTime: Math.max(...times),
      times,
    };
  }

  /**
   * Create a simple timer that returns elapsed time
   * @returns Function that returns elapsed time in milliseconds
   */
  static create(): () => number {
    const start = performance.now();
    return () => performance.now() - start;
  }

  /**
   * Sleep for a specified duration
   * @param ms - Duration in milliseconds
   * @returns Promise that resolves after the duration
   */
  static sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ==================== Formatting Utilities ====================

/**
 * Convert milliseconds to time components
 * @param ms - Time in milliseconds
 * @returns Time components
 */
export function millisecondsToComponents(ms: number): TimeComponents {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  const milliseconds = Math.floor(ms % 1000);
  
  return { hours, minutes, seconds, milliseconds };
}

/**
 * Convert time components to milliseconds
 * @param components - Time components
 * @returns Time in milliseconds
 */
export function componentsToMilliseconds(components: TimeComponents): number {
  return (
    components.hours * 3600000 +
    components.minutes * 60000 +
    components.seconds * 1000 +
    components.milliseconds
  );
}

/**
 * Format time in milliseconds to a string
 * @param ms - Time in milliseconds
 * @param format - Format pattern
 * @returns Formatted time string
 * 
 * Format tokens:
 * - HH: Hours (2 digits, zero-padded)
 * - H: Hours (1-2 digits)
 * - mm: Minutes (2 digits, zero-padded)
 * - m: Minutes (1-2 digits)
 * - ss: Seconds (2 digits, zero-padded)
 * - s: Seconds (1-2 digits)
 * - SSS: Milliseconds (3 digits, zero-padded)
 * - SS: Milliseconds (2 digits, zero-padded)
 * - S: Milliseconds (1 digit)
 * 
 * @example
 * ```typescript
 * formatTime(3661500, 'HH:mm:ss.SSS'); // "01:01:01.500"
 * formatTime(3661500, 'H:m:s'); // "1:1:1"
 * ```
 */
export function formatTime(ms: number, format: string = 'HH:mm:ss.SSS'): string {
  const { hours, minutes, seconds, milliseconds } = millisecondsToComponents(ms);
  
  let result = format;
  
  // Hours
  result = result.replace(/HH/g, hours.toString().padStart(2, '0'));
  result = result.replace(/H/g, hours.toString());
  
  // Minutes
  result = result.replace(/mm/g, minutes.toString().padStart(2, '0'));
  result = result.replace(/m(?!s)/g, minutes.toString());
  
  // Seconds
  result = result.replace(/ss/g, seconds.toString().padStart(2, '0'));
  result = result.replace(/s(?!S)/g, seconds.toString());
  
  // Milliseconds
  result = result.replace(/SSS/g, milliseconds.toString().padStart(3, '0'));
  result = result.replace(/SS(?!S)/g, Math.floor(milliseconds / 10).toString().padStart(2, '0'));
  result = result.replace(/S(?!S)/g, Math.floor(milliseconds / 100).toString());
  
  return result;
}

/**
 * Format milliseconds to human-readable string
 * @param ms - Time in milliseconds
 * @param options - Formatting options
 * @returns Human-readable time string
 * 
 * @example
 * ```typescript
 * formatHuman(3661500); // "1 hour, 1 minute, 1 second, 500 milliseconds"
 * formatHuman(5000, { compact: true }); // "5s"
 * formatHuman(3661500, { showMs: false }); // "1 hour, 1 minute, 1 second"
 * ```
 */
export function formatHuman(
  ms: number,
  options?: {
    compact?: boolean;
    showMs?: boolean;
    showZeroValues?: boolean;
  }
): string {
  const { hours, minutes, seconds, milliseconds } = millisecondsToComponents(ms);
  const compact = options?.compact ?? false;
  const showMs = options?.showMs ?? true;
  const showZeroValues = options?.showZeroValues ?? false;
  
  const parts: string[] = [];
  
  if (hours > 0 || showZeroValues) {
    if (compact) {
      parts.push(`${hours}h`);
    } else {
      parts.push(`${hours} hour${hours !== 1 ? 's' : ''}`);
    }
  }
  
  if (minutes > 0 || showZeroValues) {
    if (compact) {
      parts.push(`${minutes}m`);
    } else {
      parts.push(`${minutes} minute${minutes !== 1 ? 's' : ''}`);
    }
  }
  
  if (seconds > 0 || showZeroValues) {
    if (compact) {
      parts.push(`${seconds}s`);
    } else {
      parts.push(`${seconds} second${seconds !== 1 ? 's' : ''}`);
    }
  }
  
  if (showMs && (milliseconds > 0 || showZeroValues)) {
    if (compact) {
      parts.push(`${milliseconds}ms`);
    } else {
      parts.push(`${milliseconds} millisecond${milliseconds !== 1 ? 's' : ''}`);
    }
  }
  
  // If no non-zero values and not showing zeros, return appropriate zero string
  if (parts.length === 0) {
    if (showMs) {
      return compact ? '0ms' : '0 milliseconds';
    }
    return compact ? '0s' : '0 seconds';
  }
  
  if (compact) {
    return parts.join(' ');
  }
  
  if (parts.length === 1) {
    return parts[0];
  }
  
  if (parts.length === 2) {
    return parts.join(' and ');
  }
  
  const last = parts.pop()!;
  return `${parts.join(', ')} and ${last}`;
}

/**
 * Parse a time string to milliseconds
 * @param timeString - Time string to parse
 * @returns Time in milliseconds, or null if invalid
 * 
 * Supported formats:
 * - "1:30:45.500" (HH:MM:SS.mmm)
 * - "1:30:45" (HH:MM:SS)
 * - "1:30" (MM:SS)
 * - "30s" (seconds)
 * - "5m" (minutes)
 * - "1h" (hours)
 * - "500ms" (milliseconds)
 * - "1h30m45s" (combined)
 * 
 * @example
 * ```typescript
 * parseTime("1:30:45.500"); // 5445500
 * parseTime("5m"); // 300000
 * parseTime("1h30m"); // 5400000
 * ```
 */
export function parseTime(timeString: string): number | null {
  // Try HH:MM:SS.mmm format (3 parts = hours:minutes:seconds)
  const hms3Match = timeString.match(/^(\d+):(\d+):(\d+)(?:\.(\d+))?$/);
  if (hms3Match) {
    const hours = parseInt(hms3Match[1], 10);
    const minutes = parseInt(hms3Match[2], 10);
    const seconds = parseInt(hms3Match[3], 10);
    const milliseconds = hms3Match[4] ? parseInt(hms3Match[4].padEnd(3, '0').slice(0, 3), 10) : 0;
    return hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds;
  }
  
  // Try MM:SS.mmm format (2 parts = minutes:seconds)
  const ms2Match = timeString.match(/^(\d+):(\d+)(?:\.(\d+))?$/);
  if (ms2Match) {
    const minutes = parseInt(ms2Match[1], 10);
    const seconds = parseInt(ms2Match[2], 10);
    const milliseconds = ms2Match[3] ? parseInt(ms2Match[3].padEnd(3, '0').slice(0, 3), 10) : 0;
    return minutes * 60000 + seconds * 1000 + milliseconds;
  }
  
  // Try combined format (1h30m45s)
  // Note: Must match longer units first (ms before m) to avoid partial matching
  let totalMs = 0;
  let matchFound = false;
  
  // Use regex with ms before m to ensure correct matching
  const combinedRegex = /(\d+)(ms|s|m|h)/g;
  let match;
  
  while ((match = combinedRegex.exec(timeString)) !== null) {
    matchFound = true;
    const value = parseInt(match[1], 10);
    const unit = match[2];
    
    switch (unit) {
      case 'h':
        totalMs += value * 3600000;
        break;
      case 'm':
        totalMs += value * 60000;
        break;
      case 's':
        totalMs += value * 1000;
        break;
      case 'ms':
        totalMs += value;
        break;
    }
  }
  
  if (matchFound) {
    return totalMs;
  }
  
  // Try single unit format
  const singleMatch = timeString.match(/^(\d+)\s*(hour|hours|h|minute|minutes|m|second|seconds|s|millisecond|milliseconds|ms)$/i);
  if (singleMatch) {
    const value = parseInt(singleMatch[1], 10);
    const unit = singleMatch[2].toLowerCase();
    
    if (unit.startsWith('h')) {
      return value * 3600000;
    } else if (unit.startsWith('mi')) {
      return value * 60000;
    } else if (unit.startsWith('s')) {
      return value * 1000;
    } else if (unit === 'ms') {
      return value;
    }
  }
  
  return null;
}

/**
 * Format a lap time with comparison to previous lap
 * @param lap - Lap to format
 * @param previousLap - Previous lap for comparison (optional)
 * @param format - Time format
 * @returns Formatted string with comparison
 */
export function formatLapComparison(
  lap: Lap,
  previousLap?: Lap,
  format: string = 'mm:ss.SSS'
): string {
  const duration = formatTime(lap.duration, format);
  
  if (!previousLap) {
    return `Lap ${lap.number}: ${duration}`;
  }
  
  const diff = lap.duration - previousLap.duration;
  const diffFormatted = formatTime(Math.abs(diff), 'ss.SSS');
  const diffStr = diff >= 0 ? `+${diffFormatted}` : `-${diffFormatted}`;
  
  return `Lap ${lap.number}: ${duration} (${diffStr})`;
}

/**
 * Calculate the pace (time per unit)
 * @param timeMs - Total time in milliseconds
 * @param units - Number of units (e.g., laps, kilometers)
 * @param unitName - Name of the unit (default: "unit")
 * @returns Pace object with time per unit
 */
export function calculatePace(
  timeMs: number,
  units: number,
  unitName: string = 'unit'
): {
  timePerUnit: number;
  formatted: string;
  unitName: string;
} {
  const timePerUnit = units > 0 ? timeMs / units : 0;
  
  return {
    timePerUnit,
    formatted: `${formatTime(timePerUnit, 'mm:ss.SSS')} per ${unitName}`,
    unitName,
  };
}

// ==================== Default Export ====================

export default {
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
};