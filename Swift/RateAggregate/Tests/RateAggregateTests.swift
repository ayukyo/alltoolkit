import XCTest
@testable import RateAggregate

final class RateAggregateTests: XCTestCase {
    
    func testBasicRecordAndCount() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(100)
        agg.record(200)
        agg.record(150)
        XCTAssertEqual(agg.count(), 3)
    }
    
    func testPercentileCalculation() {
        let agg = RateAggregator(windowSize: .minutes(5))
        for i in 1...100 {
            agg.record(Double(i))
        }
        let p50 = agg.percentile(0.50)
        let p90 = agg.percentile(0.90)
        let p99 = agg.percentile(0.99)
        XCTAssert(p50 >= 49 && p50 <= 51, "p50 should be ~50, got \(p50)")
        XCTAssert(p90 >= 89 && p90 <= 91, "p90 should be ~90, got \(p90)")
        XCTAssert(p99 >= 98 && p99 <= 100, "p99 should be ~99, got \(p99)")
    }
    
    func testHitMissRatio() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.recordHit()
        agg.recordHit()
        agg.recordMiss()
        agg.recordHit()
        XCTAssertEqual(agg.totalHits(), 3)
        XCTAssertEqual(agg.totalMisses(), 1)
        XCTAssertEqual(agg.hitRatio(), 0.75, accuracy: 0.01)
    }
    
    func testMeanCalculation() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(10)
        agg.record(20)
        agg.record(30)
        XCTAssertEqual(agg.mean(), 20.0, accuracy: 0.01)
    }
    
    func testSumCalculation() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(10)
        agg.record(20)
        agg.record(30)
        XCTAssertEqual(agg.sum(), 60.0, accuracy: 0.01)
    }
    
    func testMinMax() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(10)
        agg.record(30)
        agg.record(20)
        XCTAssertEqual(agg.min(), 10.0)
        XCTAssertEqual(agg.max(), 30.0)
    }
    
    func testEmptyAggregator() {
        let agg = RateAggregator(windowSize: .minutes(5))
        XCTAssertEqual(agg.count(), 0)
        XCTAssertEqual(agg.percentile(0.99), 0)
        XCTAssertEqual(agg.mean(), 0.0)
        XCTAssertEqual(agg.hitRatio(), 0.0)
    }
    
    func testMetricsStruct() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(100)
        agg.record(200)
        let metrics = agg.metrics()
        XCTAssertEqual(metrics.count, 2)
        XCTAssertEqual(metrics.mean, 150.0, accuracy: 0.01)
    }
    
    func testBuilder() {
        let agg = RateAggregatorBuilder()
            .windowSize(.hours(1))
            .bucketCount(200)
            .precision(4)
            .build()
        XCTAssertEqual(agg.count(), 0)
        XCTAssertEqual(agg.windowSizeValue(), .hours(1))
    }
    
    func testClear() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(100)
        XCTAssertEqual(agg.count(), 1)
        agg.clear()
        XCTAssertEqual(agg.count(), 0)
    }
    
    func testP50P90P95P99() {
        let agg = RateAggregator(windowSize: .minutes(5))
        for i in 1...100 {
            agg.record(Double(i))
        }
        XCTAssert(agg.p50() >= 49 && agg.p50() <= 51, "p50 should be ~50")
        XCTAssert(agg.p90() >= 89 && agg.p90() <= 91, "p90 should be ~90")
        XCTAssert(agg.p95() >= 94 && agg.p95() <= 96, "p95 should be ~95")
        XCTAssert(agg.p99() >= 98 && agg.p99() <= 100, "p99 should be ~99")
    }
    
    func testStdDev() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.record(10)
        agg.record(20)
        agg.record(30)
        let stdDev = agg.stdDev()
        XCTAssertEqual(stdDev, 8.16, accuracy: 0.1)
    }
    
    func testResetCounters() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.recordHit()
        agg.recordHit()
        XCTAssertEqual(agg.totalHits(), 2)
        agg.resetCounters()
        XCTAssertEqual(agg.totalHits(), 0)
        XCTAssertEqual(agg.count(), 2)
    }
    
    func testMissRatio() {
        let agg = RateAggregator(windowSize: .minutes(5))
        agg.recordHit()
        agg.recordMiss()
        XCTAssertEqual(agg.missRatio(), 0.5, accuracy: 0.01)
    }
    
    func testSerialization() {
        let agg = RateAggregator(windowSize: .minutes(10))
        agg.record(100)
        agg.recordHit()
        
        let metrics = agg.metrics()
        let encoder = JSONEncoder()
        let data = try! encoder.encode(metrics)
        let decoder = JSONDecoder()
        let restored = try! decoder.decode(RateMetrics.self, from: data)
        XCTAssertEqual(restored.count, 2)
    }
    
    func testRatePerMinuteAndHour() {
        let agg = RateAggregator(windowSize: .minutes(5))
        for _ in 0..<300 {
            agg.record(1.0)
        }
        let rateMin = agg.ratePerMinute()
        let rateHr = agg.ratePerHour()
        XCTAssert(rateMin >= 59 && rateMin <= 61, "rate/min should be ~60, got \(rateMin)")
        XCTAssert(rateHr >= 3599 && rateHr <= 3601, "rate/hr should be ~3600, got \(rateHr)")
    }
}