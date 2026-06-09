import { RateAggregator, RateAggregatorBuilder, windowSizeMinutes, windowSizeHours, windowSizeSeconds } from './index';

describe('RateAggregator', () => {
  it('should record and count events', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(100);
    agg.record(200);
    agg.record(150);
    expect(agg.count()).toBe(3);
  });

  it('should calculate percentiles correctly', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    for (let i = 1; i <= 100; i++) {
      agg.record(i);
    }
    const p50 = agg.percentile(0.50);
    const p90 = agg.percentile(0.90);
    const p99 = agg.percentile(0.99);
    expect(p50).toBeGreaterThanOrEqual(49);
    expect(p50).toBeLessThanOrEqual(51);
    expect(p90).toBeGreaterThanOrEqual(89);
    expect(p90).toBeLessThanOrEqual(91);
    expect(p99).toBeGreaterThanOrEqual(98);
    expect(p99).toBeLessThanOrEqual(100);
  });

  it('should track hit/miss ratio', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.recordHit();
    agg.recordHit();
    agg.recordMiss();
    agg.recordHit();
    expect(agg.totalHits()).toBe(3);
    expect(agg.totalMisses()).toBe(1);
    expect(agg.hitRatio()).toBeCloseTo(0.75, 2);
  });

  it('should calculate mean correctly', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(10);
    agg.record(20);
    agg.record(30);
    expect(agg.mean()).toBeCloseTo(20.0, 1);
  });

  it('should calculate sum correctly', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(10);
    agg.record(20);
    agg.record(30);
    expect(agg.sum()).toBeCloseTo(60.0, 1);
  });

  it('should calculate min/max correctly', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(10);
    agg.record(30);
    agg.record(20);
    expect(agg.min()).toBe(10);
    expect(agg.max()).toBe(30);
  });

  it('should handle empty aggregator', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    expect(agg.count()).toBe(0);
    expect(agg.percentile(0.99)).toBe(0);
    expect(agg.mean()).toBe(0);
    expect(agg.hitRatio()).toBe(0);
  });

  it('should return metrics struct', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(100);
    agg.record(200);
    const metrics = agg.metrics();
    expect(metrics.count).toBe(2);
    expect(metrics.mean).toBeCloseTo(150.0, 1);
  });

  it('should use builder pattern', () => {
    const agg = new RateAggregatorBuilder()
      .windowSize(windowSizeHours(1))
      .bucketCount(200)
      .precision(4)
      .build();
    expect(agg.count()).toBe(0);
    expect(agg.windowSizeMs()).toBe(3600 * 1000);
  });

  it('should clear events', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(100);
    expect(agg.count()).toBe(1);
    agg.clear();
    expect(agg.count()).toBe(0);
  });

  it('should calculate p50/p90/p95/p99', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    for (let i = 1; i <= 100; i++) {
      agg.record(i);
    }
    expect(agg.p50()).toBeGreaterThanOrEqual(49);
    expect(agg.p50()).toBeLessThanOrEqual(51);
    expect(agg.p90()).toBeGreaterThanOrEqual(89);
    expect(agg.p90()).toBeLessThanOrEqual(91);
    expect(agg.p95()).toBeGreaterThanOrEqual(94);
    expect(agg.p95()).toBeLessThanOrEqual(96);
    expect(agg.p99()).toBeGreaterThanOrEqual(98);
    expect(agg.p99()).toBeLessThanOrEqual(100);
  });

  it('should calculate standard deviation', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.record(10);
    agg.record(20);
    agg.record(30);
    const stdDev = agg.stdDev();
    expect(stdDev).toBeCloseTo(8.16, 1);
  });

  it('should reset counters', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.recordHit();
    agg.recordHit();
    expect(agg.totalHits()).toBe(2);
    agg.resetCounters();
    expect(agg.totalHits()).toBe(0);
    expect(agg.count()).toBe(2);
  });

  it('should calculate miss ratio', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    agg.recordHit();
    agg.recordMiss();
    expect(agg.missRatio()).toBeCloseTo(0.5, 2);
  });

  it('should calculate rate per minute and hour', () => {
    const agg = new RateAggregator({ windowSize: windowSizeMinutes(5) });
    for (let i = 0; i < 300; i++) {
      agg.record(1.0);
    }
    const rateMin = agg.ratePerMinute();
    const rateHr = agg.ratePerHour();
    expect(rateMin).toBeGreaterThanOrEqual(59);
    expect(rateMin).toBeLessThanOrEqual(61);
    expect(rateHr).toBeGreaterThanOrEqual(3599);
    expect(rateHr).toBeLessThanOrEqual(3601);
  });
});