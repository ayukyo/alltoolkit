/**
 * AllToolkit - Swift Timer Utilities
 *
 * 高性能计时器工具类，提供精确的时间测量、性能分析和倒计时功能。
 * 零依赖，仅使用 Swift 标准库和 Foundation 框架。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - 精确计时器

/// 高精度计时器，用于测量代码执行时间
/// 使用 mach_absolute_time 实现纳秒级精度
public final class PrecisionTimer {
    
    private var startTime: UInt64 = 0
    private var endTime: UInt64 = 0
    private var isRunning: Bool = false
    
    /// 时间基准信息
    private static var timebaseInfo: mach_timebase_info_data_t = {
        var info = mach_timebase_info_data_t()
        mach_timebase_info(&info)
        return info
    }()
    
    /// 初始化计时器
    public init() {}
    
    /// 开始计时
    public func start() {
        startTime = mach_absolute_time()
        isRunning = true
    }
    
    /// 停止计时
    public func stop() {
        endTime = mach_absolute_time()
        isRunning = false
    }
    
    /// 重置计时器
    public func reset() {
        startTime = 0
        endTime = 0
        isRunning = false
    }
    
    /// 获取经过的纳秒数
    public var elapsedNanoseconds: UInt64 {
        let end = isRunning ? mach_absolute_time() : endTime
        let elapsed = end - startTime
        return elapsed * UInt64(Self.timebaseInfo.numer) / UInt64(Self.timebaseInfo.denom)
    }
    
    /// 获取经过的微秒数
    public var elapsedMicroseconds: Double {
        return Double(elapsedNanoseconds) / 1_000.0
    }
    
    /// 获取经过的毫秒数
    public var elapsedMilliseconds: Double {
        return Double(elapsedNanoseconds) / 1_000_000.0
    }
    
    /// 获取经过的秒数
    public var elapsedSeconds: Double {
        return Double(elapsedNanoseconds) / 1_000_000_000.0
    }
    
    /// 获取格式化的时间字符串
    public var formatted: String {
        let ns = elapsedNanoseconds
        if ns < 1_000 {
            return "\(ns)ns"
        } else if ns < 1_000_000 {
            return String(format: "%.2fµs", elapsedMicroseconds)
        } else if ns < 1_000_000_000 {
            return String(format: "%.2fms", elapsedMilliseconds)
        } else {
            return String(format: "%.3fs", elapsedSeconds)
        }
    }
    
    /// 测量代码块执行时间并返回结果
    public func measure<T>(_ block: () throws -> T) rethrows -> (result: T, duration: UInt64) {
        start()
        defer { stop() }
        let result = try block()
        return (result, elapsedNanoseconds)
    }
}

// MARK: - 代码块计时器

/// 代码块执行计时器
public struct BlockTimer {
    
    /// 执行名称
    public let name: String
    
    /// 开始时间
    private let startTime: Date
    
    /// 是否自动打印
    private let autoPrint: Bool
    
    /// 初始化并开始计时
    public init(_ name: String, autoPrint: Bool = true) {
        self.name = name
        self.startTime = Date()
        self.autoPrint = autoPrint
    }
    
    /// 结束计时并返回毫秒数
    public func stop() -> Double {
        let elapsed = Date().timeIntervalSince(startTime) * 1000
        if autoPrint {
            print("[\(name)] 耗时: \(String(format: "%.2f", elapsed))ms")
        }
        return elapsed
    }
    
    /// 使用 deinit 自动停止计时
    public static func measure(_ name: String) -> BlockTimer {
        return BlockTimer(name, autoPrint: true)
    }
}

// MARK: - 性能分析器

/// 性能分析器，用于统计分析多次执行的性能数据
public final class PerformanceProfiler {
    
    /// 记录项
    public struct Record {
        public let name: String
        public let duration: TimeInterval  // 毫秒
        public let timestamp: Date
        public let metadata: [String: Any]?
    }
    
    /// 统计结果
    public struct Statistics {
        public let name: String
        public let count: Int
        public let totalMs: Double
        public let averageMs: Double
        public let minMs: Double
        public let maxMs: Double
        public let medianMs: Double
        public let standardDeviation: Double
        public let p95Ms: Double
        public let p99Ms: Double
        
        public var formatted: String {
            """
            [\(name)] 性能统计 (共\(count)次):
              总耗时: \(String(format: "%.2f", totalMs))ms
              平均: \(String(format: "%.2f", averageMs))ms
              最小: \(String(format: "%.2f", minMs))ms
              最大: \(String(format: "%.2f", maxMs))ms
              中位数: \(String(format: "%.2f", medianMs))ms
              标准差: \(String(format: "%.2f", standardDeviation))ms
              P95: \(String(format: "%.2f", p95Ms))ms
              P99: \(String(format: "%.2f", p99Ms))ms
            """
        }
    }
    
    private var records: [Record] = []
    private let lock = NSLock()
    
    /// 初始化分析器
    public init() {}
    
    /// 记录一次执行
    public func record(
        _ name: String,
        duration: TimeInterval,
        metadata: [String: Any]? = nil
    ) {
        let record = Record(
            name: name,
            duration: duration,
            timestamp: Date(),
            metadata: metadata
        )
        lock.lock()
        records.append(record)
        lock.unlock()
    }
    
    /// 测量并记录代码块执行时间
    public func measure<T>(_ name: String, metadata: [String: Any]? = nil, block: () throws -> T) rethrows -> T {
        let start = Date()
        let result = try block()
        let duration = Date().timeIntervalSince(start) * 1000
        record(name, duration: duration, metadata: metadata)
        return result
    }
    
    /// 获取所有记录
    public func getRecords() -> [Record] {
        lock.lock()
        defer { lock.unlock() }
        return records
    }
    
    /// 获取指定名称的记录
    public func getRecords(named name: String) -> [Record] {
        return getRecords().filter { $0.name == name }
    }
    
    /// 计算指定名称的统计数据
    public func statistics(for name: String) -> Statistics? {
        let nameRecords = getRecords(named: name)
        guard !nameRecords.isEmpty else { return nil }
        
        let durations = nameRecords.map { $0.duration }.sorted()
        let count = durations.count
        let total = durations.reduce(0, +)
        let average = total / Double(count)
        let min = durations.first!
        let max = durations.last!
        
        // 中位数
        let median: Double
        if count % 2 == 0 {
            median = (durations[count / 2 - 1] + durations[count / 2]) / 2
        } else {
            median = durations[count / 2]
        }
        
        // 标准差
        let variance = durations.map { pow($0 - average, 2) }.reduce(0, +) / Double(count)
        let stdDev = sqrt(variance)
        
        // 百分位数
        func percentile(_ p: Double) -> Double {
            let index = Int(Double(count - 1) * p)
            return durations[index]
        }
        
        return Statistics(
            name: name,
            count: count,
            totalMs: total,
            averageMs: average,
            minMs: min,
            maxMs: max,
            medianMs: median,
            standardDeviation: stdDev,
            p95Ms: percentile(0.95),
            p99Ms: percentile(0.99)
        )
    }
    
    /// 清除所有记录
    public func clear() {
        lock.lock()
        records.removeAll()
        lock.unlock()
    }
    
    /// 清除指定名称的记录
    public func clear(named name: String) {
        lock.lock()
        records.removeAll { $0.name == name }
        lock.unlock()
    }
    
    /// 导出为 CSV 格式
    public func exportCSV() -> String {
        var csv = "name,duration_ms,timestamp\n"
        let dateFormatter = ISO8601DateFormatter()
        for record in getRecords() {
            csv += "\(record.name),\(record.duration),\(dateFormatter.string(from: record.timestamp))\n"
        }
        return csv
    }
}

// MARK: - 倒计时器

/// 倒计时器
public final class CountdownTimer: ObservableObject {
    
    /// 倒计时状态
    public enum State {
        case idle
        case running
        case paused
        case finished
    }
    
    /// 当前剩余秒数
    @Published public private(set) var remainingSeconds: TimeInterval = 0
    
    /// 当前状态
    @Published public private(set) var state: State = .idle
    
    /// 完成回调
    public var onFinished: (() -> Void)?
    
    /// 每秒回调
    public var onTick: ((TimeInterval) -> Void)?
    
    private var timer: Timer?
    private var targetSeconds: TimeInterval = 0
    private var startTime: Date?
    private var pausedRemaining: TimeInterval = 0
    
    /// 初始化倒计时器
    public init() {}
    
    /// 设置倒计时时间
    public func set(seconds: TimeInterval) {
        stop()
        targetSeconds = seconds
        remainingSeconds = seconds
        state = .idle
    }
    
    /// 开始倒计时
    public func start() {
        guard state != .running else { return }
        
        let seconds = state == .paused ? pausedRemaining : targetSeconds
        startTime = Date()
        
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            self?.updateTimer()
        }
        
        state = .running
    }
    
    /// 暂停倒计时
    public func pause() {
        guard state == .running else { return }
        timer?.invalidate()
        timer = nil
        pausedRemaining = remainingSeconds
        state = .paused
    }
    
    /// 停止并重置倒计时
    public func stop() {
        timer?.invalidate()
        timer = nil
        remainingSeconds = targetSeconds
        state = .idle
    }
    
    /// 重置到初始时间
    public func reset() {
        stop()
        remainingSeconds = targetSeconds
    }
    
    private func updateTimer() {
        guard let startTime = startTime else { return }
        
        let elapsed = Date().timeIntervalSince(startTime)
        remainingSeconds = max(0, (state == .paused ? pausedRemaining : targetSeconds) - elapsed)
        
        onTick?(remainingSeconds)
        
        if remainingSeconds <= 0 {
            timer?.invalidate()
            timer = nil
            state = .finished
            onFinished?()
        }
    }
    
    /// 格式化剩余时间为字符串
    public var formatted: String {
        let hours = Int(remainingSeconds) / 3600
        let minutes = Int(remainingSeconds) % 3600 / 60
        let seconds = Int(remainingSeconds) % 60
        let ms = Int((remainingSeconds - Double(Int(remainingSeconds))) * 100)
        
        if hours > 0 {
            return String(format: "%02d:%02d:%02d.%02d", hours, minutes, seconds, ms)
        } else {
            return String(format: "%02d:%02d.%02d", minutes, seconds, ms)
        }
    }
    
    /// 静态方法：创建一次性计时器
    public static func after(_ seconds: TimeInterval, execute: @escaping () -> Void) -> Timer {
        return Timer.scheduledTimer(withTimeInterval: seconds, repeats: false) { _ in
            execute()
        }
    }
    
    /// 静态方法：创建重复计时器
    public static func every(_ interval: TimeInterval, execute: @escaping () -> Void) -> Timer {
        return Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { _ in
            execute()
        }
    }
}

// MARK: - 秒表

/// 秒表，支持圈数记录
public final class Stopwatch {
    
    /// 圈数记录
    public struct Lap {
        public let number: Int
        public let lapTime: TimeInterval  // 秒
        public let totalTime: TimeInterval  // 秒
        public let timestamp: Date
    }
    
    /// 开始时间
    private(set) public var startTime: Date?
    
    /// 累计时间（用于暂停后恢复）
    private var accumulatedTime: TimeInterval = 0
    
    /// 是否正在运行
    public private(set) var isRunning: Bool = false
    
    /// 圈数记录
    public private(set) var laps: [Lap] = []
    
    /// 初始化秒表
    public init() {}
    
    /// 开始/继续计时
    public func start() {
        guard !isRunning else { return }
        startTime = Date()
        isRunning = true
    }
    
    /// 暂停计时
    public func pause() {
        guard isRunning, let start = startTime else { return }
        accumulatedTime += Date().timeIntervalSince(start)
        isRunning = false
        startTime = nil
    }
    
    /// 切换运行/暂停状态
    public func toggle() {
        if isRunning {
            pause()
        } else {
            start()
        }
    }
    
    /// 重置秒表
    public func reset() {
        startTime = nil
        accumulatedTime = 0
        isRunning = false
        laps.removeAll()
    }
    
    /// 记录一圈
    public func lap() -> Lap? {
        let total = elapsedSeconds
        let lapTime = laps.isEmpty ? total : total - laps.last!.totalTime
        
        let newLap = Lap(
            number: laps.count + 1,
            lapTime: lapTime,
            totalTime: total,
            timestamp: Date()
        )
        
        laps.append(newLap)
        return newLap
    }
    
    /// 获取经过的秒数
    public var elapsedSeconds: TimeInterval {
        if isRunning, let start = startTime {
            return accumulatedTime + Date().timeIntervalSince(start)
        }
        return accumulatedTime
    }
    
    /// 获取经过的毫秒数
    public var elapsedMilliseconds: TimeInterval {
        return elapsedSeconds * 1000
    }
    
    /// 格式化显示
    public var formatted: String {
        let total = elapsedSeconds
        let hours = Int(total) / 3600
        let minutes = Int(total) % 3600 / 60
        let seconds = Int(total) % 60
        let ms = Int((total - Double(Int(total))) * 100)
        
        if hours > 0 {
            return String(format: "%02d:%02d:%02d.%02d", hours, minutes, seconds, ms)
        } else {
            return String(format: "%02d:%02d.%02d", minutes, seconds, ms)
        }
    }
    
    /// 获取最佳圈数
    public var bestLap: Lap? {
        return laps.min { $0.lapTime < $1.lapTime }
    }
    
    /// 获取最差圈数
    public var worstLap: Lap? {
        return laps.max { $0.lapTime < $1.lapTime }
    }
    
    /// 获取平均圈数时间
    public var averageLapTime: TimeInterval? {
        guard !laps.isEmpty else { return nil }
        return laps.map { $0.lapTime }.reduce(0, +) / Double(laps.count)
    }
}

// MARK: - 便捷函数

/// 快速测量代码块执行时间
public func timeit<T>(_ name: String = "Block", block: () throws -> T) rethrows -> T {
    let start = Date()
    let result = try block()
    let elapsed = Date().timeIntervalSince(start) * 1000
    print("[\(name)] 耗时: \(String(format: "%.2f", elapsed))ms")
    return result
}

/// 快速测量代码块执行时间并返回详细结果
public func timeit<T>(_ name: String = "Block", block: () throws -> T) rethrows -> (result: T, milliseconds: Double) {
    let start = Date()
    let result = try block()
    let elapsed = Date().timeIntervalSince(start) * 1000
    return (result, elapsed)
}

/// 延迟执行
public func delay(_ seconds: TimeInterval, execute: @escaping () -> Void) {
    DispatchQueue.main.asyncAfter(deadline: .now() + seconds, execute: execute)
}