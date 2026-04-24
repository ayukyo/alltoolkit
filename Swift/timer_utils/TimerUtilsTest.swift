/**
 * AllToolkit - Swift Timer Utilities Tests
 *
 * 测试文件，验证计时器工具类的各项功能
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import XCTest
@testable import TimerUtils

final class TimerUtilsTests: XCTestCase {
    
    // MARK: - PrecisionTimer Tests
    
    func testPrecisionTimerBasicOperations() {
        let timer = PrecisionTimer()
        
        // 测试初始状态
        XCTAssertFalse(timer.isRunning)
        XCTAssertEqual(timer.elapsedNanoseconds, 0)
        
        // 测试 start
        timer.start()
        XCTAssertTrue(timer.isRunning)
        
        // 模拟一些工作
        var sum = 0
        for i in 0..<1000 {
            sum += i
        }
        _ = sum
        
        // 测试运行中获取时间
        let runningElapsed = timer.elapsedNanoseconds
        XCTAssertGreaterThan(runningElapsed, 0)
        
        // 测试 stop
        timer.stop()
        XCTAssertFalse(timer.isRunning)
        let stoppedElapsed = timer.elapsedNanoseconds
        XCTAssertGreaterThan(stoppedElapsed, 0)
        
        // 测试 reset
        timer.reset()
        XCTAssertFalse(timer.isRunning)
        XCTAssertEqual(timer.elapsedNanoseconds, 0)
    }
    
    func testPrecisionTimerFormatted() {
        let timer = PrecisionTimer()
        timer.start()
        // 短时间测试
        Thread.sleep(forTimeInterval: 0.001)  // 1ms
        timer.stop()
        
        let formatted = timer.formatted
        // 验证格式化字符串不为空
        XCTAssertFalse(formatted.isEmpty)
    }
    
    func testPrecisionTimerMeasure() {
        let timer = PrecisionTimer()
        let (result, duration) = timer.measure {
            return 1 + 1
        }
        
        XCTAssertEqual(result, 2)
        XCTAssertGreaterThan(duration, 0)
    }
    
    func testPrecisionTimerMeasureWithThrowing() {
        enum TestError: Error {
            case someError
        }
        
        let timer = PrecisionTimer()
        
        // 测试正常返回
        let (result1, duration1) = try! timer.measure {
            return "success"
        }
        XCTAssertEqual(result1, "success")
        XCTAssertGreaterThan(duration1, 0)
        
        // 测试抛出错误
        var threw = false
        do {
            _ = try timer.measure {
                throw TestError.someError
            }
        } catch {
            threw = true
        }
        XCTAssertTrue(threw)
    }
    
    // MARK: - BlockTimer Tests
    
    func testBlockTimer() {
        let timer = BlockTimer("TestOperation", autoPrint: false)
        Thread.sleep(forTimeInterval: 0.01)  // 10ms
        let elapsed = timer.stop()
        
        XCTAssertGreaterThanOrEqual(elapsed, 10)
    }
    
    func testBlockTimerMeasure() {
        let timer = BlockTimer.measure("AutoPrintTest")
        _ = timer
        // 自动打印测试，不抛出异常即可
    }
    
    // MARK: - PerformanceProfiler Tests
    
    func testPerformanceProfilerRecord() {
        let profiler = PerformanceProfiler()
        
        profiler.record("test", duration: 100)
        profiler.record("test", duration: 200)
        profiler.record("test", duration: 150)
        
        let records = profiler.getRecords(named: "test")
        XCTAssertEqual(records.count, 3)
    }
    
    func testPerformanceProfilerStatistics() {
        let profiler = PerformanceProfiler()
        
        // 添加测试数据
        profiler.record("operation", duration: 100)
        profiler.record("operation", duration: 200)
        profiler.record("operation", duration: 150)
        profiler.record("operation", duration: 120)
        profiler.record("operation", duration: 180)
        
        let stats = profiler.statistics(for: "operation")
        
        XCTAssertNotNil(stats)
        XCTAssertEqual(stats!.count, 5)
        XCTAssertEqual(stats!.totalMs, 750)
        XCTAssertEqual(stats!.averageMs, 150)
        XCTAssertEqual(stats!.minMs, 100)
        XCTAssertEqual(stats!.maxMs, 200)
        XCTAssertGreaterThanOrEqual(stats!.medianMs, 120)
        XCTAssertLessThanOrEqual(stats!.medianMs, 180)
    }
    
    func testPerformanceProfilerMeasure() {
        let profiler = PerformanceProfiler()
        
        let result = profiler.measure("fastOperation") {
            return 42
        }
        
        XCTAssertEqual(result, 42)
        
        let records = profiler.getRecords(named: "fastOperation")
        XCTAssertEqual(records.count, 1)
    }
    
    func testPerformanceProfilerClear() {
        let profiler = PerformanceProfiler()
        
        profiler.record("test1", duration: 100)
        profiler.record("test2", duration: 200)
        
        XCTAssertEqual(profiler.getRecords().count, 2)
        
        profiler.clear(named: "test1")
        XCTAssertEqual(profiler.getRecords().count, 1)
        
        profiler.clear()
        XCTAssertEqual(profiler.getRecords().count, 0)
    }
    
    func testPerformanceProfilerCSVExport() {
        let profiler = PerformanceProfiler()
        
        profiler.record("op1", duration: 100)
        profiler.record("op2", duration: 200)
        
        let csv = profiler.exportCSV()
        
        XCTAssertTrue(csv.contains("name,duration_ms,timestamp"))
        XCTAssertTrue(csv.contains("op1,100.0"))
        XCTAssertTrue(csv.contains("op2,200.0"))
    }
    
    // MARK: - CountdownTimer Tests
    
    func testCountdownTimerSetAndStart() {
        let timer = CountdownTimer()
        
        timer.set(seconds: 10)
        
        XCTAssertEqual(timer.remainingSeconds, 10)
        XCTAssertEqual(timer.state, .idle)
    }
    
    func testCountdownTimerStop() {
        let timer = CountdownTimer()
        
        timer.set(seconds: 10)
        timer.start()
        XCTAssertEqual(timer.state, .running)
        
        timer.stop()
        XCTAssertEqual(timer.state, .idle)
        XCTAssertEqual(timer.remainingSeconds, 10)
    }
    
    func testCountdownTimerReset() {
        let timer = CountdownTimer()
        
        timer.set(seconds: 10)
        timer.reset()
        
        XCTAssertEqual(timer.remainingSeconds, 10)
    }
    
    func testCountdownTimerFormatted() {
        let timer = CountdownTimer()
        
        timer.set(seconds: 3661.5)  // 1小时1分1.5秒
        XCTAssertEqual(timer.formatted, "01:01:01.50")
        
        timer.set(seconds: 65.25)  // 1分5.25秒
        XCTAssertEqual(timer.formatted, "01:05.25")
    }
    
    // MARK: - Stopwatch Tests
    
    func testStopwatchBasicOperations() {
        let stopwatch = Stopwatch()
        
        XCTAssertFalse(stopwatch.isRunning)
        XCTAssertEqual(stopwatch.elapsedSeconds, 0)
        XCTAssertEqual(stopwatch.laps.count, 0)
        
        stopwatch.start()
        XCTAssertTrue(stopwatch.isRunning)
        
        Thread.sleep(forTimeInterval: 0.01)
        
        stopwatch.pause()
        XCTAssertFalse(stopwatch.isRunning)
        XCTAssertGreaterThan(stopwatch.elapsedSeconds, 0)
        
        stopwatch.reset()
        XCTAssertFalse(stopwatch.isRunning)
        XCTAssertEqual(stopwatch.elapsedSeconds, 0)
        XCTAssertEqual(stopwatch.laps.count, 0)
    }
    
    func testStopwatchToggle() {
        let stopwatch = Stopwatch()
        
        XCTAssertFalse(stopwatch.isRunning)
        
        stopwatch.toggle()
        XCTAssertTrue(stopwatch.isRunning)
        
        stopwatch.toggle()
        XCTAssertFalse(stopwatch.isRunning)
    }
    
    func testStopwatchLap() {
        let stopwatch = Stopwatch()
        
        stopwatch.start()
        Thread.sleep(forTimeInterval: 0.02)
        
        let lap1 = stopwatch.lap()
        XCTAssertNotNil(lap1)
        XCTAssertEqual(lap1!.number, 1)
        XCTAssertGreaterThanOrEqual(lap1!.lapTime, 0.02)
        
        Thread.sleep(forTimeInterval: 0.01)
        
        let lap2 = stopwatch.lap()
        XCTAssertEqual(lap2!.number, 2)
        
        stopwatch.stop()
        
        XCTAssertEqual(stopwatch.laps.count, 2)
    }
    
    func testStopwatchBestWorstLap() {
        let stopwatch = Stopwatch()
        stopwatch.start()
        
        // 模拟不同的圈速
        Thread.sleep(forTimeInterval: 0.01)
        _ = stopwatch.lap()  // ~10ms
        
        Thread.sleep(forTimeInterval: 0.02)
        _ = stopwatch.lap()  // ~20ms (worst)
        
        Thread.sleep(forTimeInterval: 0.005)
        _ = stopwatch.lap()  // ~5ms (best)
        
        stopwatch.stop()
        
        XCTAssertNotNil(stopwatch.bestLap)
        XCTAssertNotNil(stopwatch.worstLap)
        XCTAssertEqual(stopwatch.bestLap!.number, 3)
        XCTAssertEqual(stopwatch.worstLap!.number, 2)
    }
    
    func testStopwatchFormatted() {
        let stopwatch = Stopwatch()
        
        // 测试小于1分钟的格式
        stopwatch.start()
        stopwatch.pause()
        stopwatch = Stopwatch()
        
        // 手动设置时间（通过内部 accumulatedTime）
        let formatted = stopwatch.formatted
        XCTAssertTrue(formatted.contains("00:00"))
    }
    
    // MARK: - 便捷函数 Tests
    
    func testTimeitFunction() {
        let result = timeit("TestBlock") {
            return 1 + 1
        }
        XCTAssertEqual(result, 2)
    }
    
    func testTimeitWithDetailResult() {
        let (result, ms) = timeit("DetailedTest") {
            Thread.sleep(forTimeInterval: 0.01)
            return "done"
        }
        
        XCTAssertEqual(result, "done")
        XCTAssertGreaterThanOrEqual(ms, 10)
    }
}

// MARK: - XCTest Main Entry

#if !os(macOS) && !os(iOS) && !os(watchOS) && !os(tvOS)
// For Linux Swift testing
extension TimerUtilsTests {
    static var allTests = [
        ("testPrecisionTimerBasicOperations", testPrecisionTimerBasicOperations),
        ("testPrecisionTimerFormatted", testPrecisionTimerFormatted),
        ("testPrecisionTimerMeasure", testPrecisionTimerMeasure),
        ("testPrecisionTimerMeasureWithThrowing", testPrecisionTimerMeasureWithThrowing),
        ("testBlockTimer", testBlockTimer),
        ("testBlockTimerMeasure", testBlockTimerMeasure),
        ("testPerformanceProfilerRecord", testPerformanceProfilerRecord),
        ("testPerformanceProfilerStatistics", testPerformanceProfilerStatistics),
        ("testPerformanceProfilerMeasure", testPerformanceProfilerMeasure),
        ("testPerformanceProfilerClear", testPerformanceProfilerClear),
        ("testPerformanceProfilerCSVExport", testPerformanceProfilerCSVExport),
        ("testCountdownTimerSetAndStart", testCountdownTimerSetAndStart),
        ("testCountdownTimerStop", testCountdownTimerStop),
        ("testCountdownTimerReset", testCountdownTimerReset),
        ("testCountdownTimerFormatted", testCountdownTimerFormatted),
        ("testStopwatchBasicOperations", testStopwatchBasicOperations),
        ("testStopwatchToggle", testStopwatchToggle),
        ("testStopwatchLap", testStopwatchLap),
        ("testStopwatchBestWorstLap", testStopwatchBestWorstLap),
        ("testStopwatchFormatted", testStopwatchFormatted),
        ("testTimeitFunction", testTimeitFunction),
        ("testTimeitWithDetailResult", testTimeitWithDetailResult),
    ]
}
#endif