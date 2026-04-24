/**
 * AllToolkit - Swift Timer Utilities Examples
 *
 * 示例代码，展示计时器工具类的各种用法
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// 导入模块（在实际项目中使用）
// import TimerUtils

// MARK: - 示例：PrecisionTimer 精确计时器

func examplePrecisionTimer() {
    print("=== PrecisionTimer 示例 ===")
    
    // 基本用法
    let timer = PrecisionTimer()
    timer.start()
    
    // 执行一些工作
    var sum = 0
    for i in 0..<100000 {
        sum += i
    }
    _ = sum
    
    timer.stop()
    
    print("纳秒: \(timer.elapsedNanoseconds)")
    print("微秒: \(timer.elapsedMicroseconds)")
    print("毫秒: \(timer.elapsedMilliseconds)")
    print("秒: \(timer.elapsedSeconds)")
    print("格式化: \(timer.formatted)")
    
    // 使用 measure 方法自动测量
    let (result, duration) = timer.measure {
        // 执行复杂计算
        return (0..<1000).reduce(0, +)
    }
    print("计算结果: \(result), 耗时: \(duration)ns")
    print()
}

// MARK: - 示例：BlockTimer 代码块计时器

func exampleBlockTimer() {
    print("=== BlockTimer 示例 ===")
    
    // 自动打印模式
    let timer = BlockTimer("数据处理")
    
    // 模拟数据处理
    var data: [Int] = []
    for i in 0..<10000 {
        data.append(i * i)
    }
    
    let elapsed = timer.stop()
    print("返回的毫秒数: \(elapsed)")
    
    // 使用静态方法
    let _ = BlockTimer.measure("快速操作")
    _ = (0..<1000).map { $0 * 2 }
    // 自动在 deinit 时打印
    print()
}

// MARK: - 示例：PerformanceProfiler 性能分析器

func examplePerformanceProfiler() {
    print("=== PerformanceProfiler 示例 ===")
    
    let profiler = PerformanceProfiler()
    
    // 测量多个操作
    for i in 0..<10 {
        _ = profiler.measure("数组排序") {
            var arr = (0..<1000).map { _ in Int.random(in: 0...10000) }
            arr.sort()
        }
    }
    
    for i in 0..<5 {
        _ = profiler.measure("字符串处理") {
            var s = ""
            for j in 0..<1000 {
                s += "\(j),"
            }
            _ = s
        }
    }
    
    // 获取统计信息
    if let stats = profiler.statistics(for: "数组排序") {
        print(stats.formatted)
    }
    
    if let stats = profiler.statistics(for: "字符串处理") {
        print(stats.formatted)
    }
    
    // 导出 CSV
    let csv = profiler.exportCSV()
    print("\nCSV 导出预览:")
    print(String(csv.prefix(200)))
    print()
}

// MARK: - 示例：CountdownTimer 倒计时器

func exampleCountdownTimer() {
    print("=== CountdownTimer 示例 ===")
    
    let timer = CountdownTimer()
    
    // 设置回调
    timer.onTick = { remaining in
        // 每秒更新
        print("剩余: \(String(format: "%.1f", remaining))秒")
    }
    
    timer.onFinished = {
        print("倒计时结束！")
    }
    
    // 设置3秒倒计时
    timer.set(seconds: 3)
    print("倒计时设置完成: \(timer.formatted)")
    
    // 开始倒计时
    timer.start()
    
    // 注意：在示例中我们使用 RunLoop 来等待
    // 在实际应用中，这通常在主线程自动处理
    print("（实际使用中会自动运行）")
    timer.stop()
    print()
}

// MARK: - 示例：Stopwatch 秒表

func exampleStopwatch() {
    print("=== Stopwatch 示例 ===")
    
    let stopwatch = Stopwatch()
    
    // 开始计时
    stopwatch.start()
    print("秒表启动...")
    
    // 模拟第一圈
    Thread.sleep(forTimeInterval: 0.5)
    let lap1 = stopwatch.lap()
    print("第\(lap1!.number)圈: \(String(format: "%.3f", lap1!.lapTime))秒")
    
    // 模拟第二圈
    Thread.sleep(forTimeInterval: 0.3)
    let lap2 = stopwatch.lap()
    print("第\(lap2!.number)圈: \(String(format: "%.3f", lap2!.lapTime))秒")
    
    // 模拟第三圈
    Thread.sleep(forTimeInterval: 0.2)
    let lap3 = stopwatch.lap()
    print("第\(lap3!.number)圈: \(String(format: "%.3f", lap3!.lapTime))秒")
    
    // 暂停
    stopwatch.pause()
    print("暂停，总时间: \(stopwatch.formatted)")
    
    // 继续计时
    stopwatch.start()
    Thread.sleep(forTimeInterval: 0.1)
    stopwatch.stop()
    
    // 统计信息
    print("\n圈数统计:")
    print("总圈数: \(stopwatch.laps.count)")
    print("总时间: \(stopwatch.formatted)")
    
    if let best = stopwatch.bestLap {
        print("最佳圈: 第\(best.number)圈 - \(String(format: "%.3f", best.lapTime))秒")
    }
    if let worst = stopwatch.worstLap {
        print("最差圈: 第\(worst.number)圈 - \(String(format: "%.3f", worst.lapTime))秒")
    }
    if let avg = stopwatch.averageLapTime {
        print("平均圈速: \(String(format: "%.3f", avg))秒")
    }
    print()
}

// MARK: - 示例：便捷函数

func exampleConvenienceFunctions() {
    print("=== 便捷函数示例 ===")
    
    // timeit - 简单计时
    let result = timeit("快速排序") {
        var arr = (0..<10000).map { _ in Int.random(in: 0...100000) }
        arr.sort()
        return arr
    }
    print("排序完成，元素数: \(result.count)")
    
    // timeit - 带详细结果
    let (sum, ms) = timeit("求和计算") {
        return (0..<1000000).reduce(0, +)
    }
    print("求和结果: \(sum), 耗时: \(String(format: "%.2f", ms))ms")
    
    // delay - 延迟执行
    print("安排延迟任务...")
    delay(0.1) {
        print("延迟任务执行！")
    }
    
    // CountdownTimer 静态方法
    _ = CountdownTimer.every(1.0) {
        // 每秒执行的任务
    }
    
    _ = CountdownTimer.after(5.0) {
        print("5秒后执行")
    }
    print()
}

// MARK: - 实际应用场景

func exampleRealWorldScenarios() {
    print("=== 实际应用场景 ===")
    
    // 场景1：API 响应时间监控
    let apiProfiler = PerformanceProfiler()
    
    func fetchUserData() {
        _ = apiProfiler.measure("API: getUserData") {
            // 模拟网络请求
            Thread.sleep(forTimeInterval: 0.05)
        }
    }
    
    func fetchProductList() {
        _ = apiProfiler.measure("API: getProductList") {
            // 模拟网络请求
            Thread.sleep(forTimeInterval: 0.08)
        }
    }
    
    // 模拟多次请求
    for _ in 0..<5 {
        fetchUserData()
        fetchProductList()
    }
    
    // 分析性能
    if let stats = apiProfiler.statistics(for: "API: getUserData") {
        print("getUserData 平均响应: \(String(format: "%.2f", stats.averageMs))ms")
    }
    
    // 场景2：游戏循环计时
    print("\n游戏循环示例:")
    let gameTimer = PrecisionTimer()
    gameTimer.start()
    
    // 模拟游戏逻辑
    Thread.sleep(forTimeInterval: 0.016)  // ~60fps
    
    gameTimer.stop()
    let frameTime = gameTimer.elapsedMilliseconds
    let fps = 1000.0 / frameTime
    print("帧时间: \(String(format: "%.2f", frameTime))ms, FPS: \(String(format: "%.1f", fps))")
    
    // 场景3：实验时间测量
    print("\n实验计时示例:")
    let experimentStopwatch = Stopwatch()
    experimentStopwatch.start()
    
    print("实验阶段1...")
    Thread.sleep(forTimeInterval: 0.1)
    _ = experimentStopwatch.lap()
    
    print("实验阶段2...")
    Thread.sleep(forTimeInterval: 0.15)
    _ = experimentStopwatch.lap()
    
    print("实验阶段3...")
    Thread.sleep(forTimeInterval: 0.12)
    _ = experimentStopwatch.lap()
    
    experimentStopwatch.stop()
    print("实验总耗时: \(experimentStopwatch.formatted)")
    
    print()
}

// MARK: - 主程序

@main
struct TimerExamples {
    static func main() {
        print("╔════════════════════════════════════════╗")
        print("║  AllToolkit - Swift Timer Utilities    ║")
        print("║         使用示例                       ║")
        print("╚════════════════════════════════════════╝")
        print()
        
        examplePrecisionTimer()
        exampleBlockTimer()
        examplePerformanceProfiler()
        exampleCountdownTimer()
        exampleStopwatch()
        exampleConvenienceFunctions()
        exampleRealWorldScenarios()
        
        print("所有示例完成！")
    }
}