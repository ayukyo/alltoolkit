// RateAggregate — Sliding Window Rate Aggregator with Percentile Calculations
// Zero dependencies, pure JavaScript

class WindowSize {
  constructor(config) {
    if (config.seconds) this.ms = config.seconds * 1000;
    else if (config.minutes) this.ms = config.minutes * 60 * 1000;
    else if (config.hours) this.ms = config.hours * 3600 * 1000;
    else this.ms = 5 * 60 * 1000;
  }
}

class RateAggregator {
  constructor(config) {
    this.events = [];
    this.windowSize = new WindowSize(config.windowSize || { minutes: 5 });
    this.bucketCount = config.bucketCount || 100;
    this.precision = config.precision || 2;
    this.totalHits = 0;
    this.totalMisses = 0;
  }

  evictOldEvents() {
    const cutoff = Date.now() - this.windowSize.ms;
    this.events = this.events.filter(e => e.timestamp >= cutoff);
  }

  round(value) {
    const multiplier = Math.pow(10, this.precision);
    return Math.round(value * multiplier) / multiplier;
  }

  record(value) {
    this.evictOldEvents();
    this.events.push({ timestamp: Date.now(), value });
  }

  recordHit() {
    this.totalHits++;
    this.evictOldEvents();
    this.events.push({ timestamp: Date.now(), value: 1.0 });
  }

  recordMiss() {
    this.totalMisses++;
    this.evictOldEvents();
    this.events.push({ timestamp: Date.now(), value: 0.0 });
  }

  count() {
    this.evictOldEvents();
    return this.events.length;
  }

  totalHits() { return this.totalHits; }
  totalMisses() { return this.totalMisses; }

  hitRatio() {
    const total = this.totalHits + this.totalMisses;
    return total === 0 ? 0.0 : this.totalHits / total;
  }

  missRatio() { return 1.0 - this.hitRatio(); }

  ratePerSecond() {
    this.evictOldEvents();
    const secs = this.windowSize.ms / 1000;
    return secs === 0 ? 0 : this.round(this.events.length / secs);
  }

  ratePerMinute() {
    this.evictOldEvents();
    const windowSecs = this.windowSize.ms / 1000;
    return windowSecs === 0 ? 0 : this.round(this.events.length * 60.0 / windowSecs);
  }

  ratePerHour() {
    this.evictOldEvents();
    const windowSecs = this.windowSize.ms / 1000;
    return windowSecs === 0 ? 0 : this.round(this.events.length * 3600.0 / windowSecs);
  }

  sum() {
    this.evictOldEvents();
    return this.events.reduce((acc, e) => acc + e.value, 0);
  }

  mean() {
    this.evictOldEvents();
    if (this.events.length === 0) return 0;
    return this.round(this.sum() / this.events.length);
  }

  min() {
    this.evictOldEvents();
    if (this.events.length === 0) return 0;
    return Math.min(...this.events.map(e => e.value));
  }

  max() {
    this.evictOldEvents();
    if (this.events.length === 0) return 0;
    return Math.max(...this.events.map(e => e.value));
  }

  percentile(p) {
    this.evictOldEvents();
    if (this.events.length === 0) return 0;
    const values = this.events.map(e => e.value).sort((a, b) => a - b);
    const idx = Math.round((values.length - 1) * p);
    return this.round(values[Math.min(idx, values.length - 1)]);
  }

  p50() { return this.percentile(0.50); }
  p90() { return this.percentile(0.90); }
  p95() { return this.percentile(0.95); }
  p99() { return this.percentile(0.99); }

  stdDev() {
    this.evictOldEvents();
    if (this.events.length === 0) return 0;
    const meanVal = this.mean();
    const variance = this.events.reduce((acc, e) => {
      const diff = e.value - meanVal;
      return acc + diff * diff;
    }, 0) / this.events.length;
    return this.round(Math.sqrt(variance));
  }

  metrics() {
    this.evictOldEvents();
    const cnt = this.events.length;
    const windowSecs = this.windowSize.ms / 1000;
    return {
      count: cnt,
      ratePerSecond: windowSecs > 0 ? this.round(cnt / windowSecs) : 0,
      ratePerMinute: windowSecs > 0 ? this.round(cnt * 60.0 / windowSecs) : 0,
      ratePerHour: windowSecs > 0 ? this.round(cnt * 3600.0 / windowSecs) : 0,
      sum: this.sum(),
      mean: this.mean(),
      min: this.min(),
      max: this.max(),
      p50: this.p50(),
      p90: this.p90(),
      p95: this.p95(),
      p99: this.p99(),
      stdDev: this.stdDev(),
      totalHits: this.totalHits,
      totalMisses: this.totalMisses,
      hitRatio: this.hitRatio(),
      missRatio: this.missRatio()
    };
  }

  clear() { this.events = []; }
  resetCounters() { this.totalHits = 0; this.totalMisses = 0; }
  windowSizeMs() { return this.windowSize.ms; }
}

class RateAggregatorBuilder {
  constructor() {
    this.windowSize = { minutes: 5 };
    this.bucketCount = 100;
    this.precision = 2;
  }

  windowSize(size) { this.windowSize = size; return this; }
  bucketCount(count) { this.bucketCount = count; return this; }
  precision(p) { this.precision = p; return this; }

  build() {
    return new RateAggregator({
      windowSize: this.windowSize,
      bucketCount: this.bucketCount,
      precision: this.precision
    });
  }
}

module.exports = { RateAggregator, RateAggregatorBuilder, WindowSize };