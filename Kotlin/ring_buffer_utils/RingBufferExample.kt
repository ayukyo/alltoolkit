/**
 * Ring Buffer 示例文件
 * 
 * 展示各种使用场景和最佳实践
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-04-15
 */

package ring_buffer_utils

fun main() {
    println("=" .repeat(60))
    println("Ring Buffer 工具模块 - 使用示例")
    println("=" .repeat(60))
    
    // 示例 1: 基本使用
    basicUsageExample()
    
    // 示例 2: 日志系统应用
    logSystemExample()
    
    // 示例 3: 滑动窗口计算
    slidingWindowExample()
    
    // 示例 4: 事件历史记录
    eventHistoryExample()
    
    // 示例 5: 生产者-消费者模式
    producerConsumerExample()
    
    // 示例 6: 线程安全使用
    threadSafeExample()
    
    // 示例 7: 音频缓冲区模拟
    audioBufferExample()
    
    // 示例 8: 扩展函数使用
    extensionFunctionExample()
}

/**
 * 示例 1: 基本使用
 */
fun basicUsageExample() {
    println("\n【示例 1: 基本使用】")
    println("-".repeat(40))
    
    // 创建容量为 5 的环形缓冲区
    val buffer = RingBuffer<Int>(5)
    
    // 添加元素
    println("添加元素 1, 2, 3:")
    buffer.push(1)
    buffer.push(2)
    buffer.push(3)
    println("缓冲区: ${buffer.toList()}")
    println("大小: ${buffer.size}, 可用空间: ${buffer.available()}")
    
    // 查看元素
    println("\n查看操作:")
    println("peek() - 最老元素: ${buffer.peek()}")
    println("peekLast() - 最新元素: ${buffer.peekLast()}")
    
    // 取出元素
    println("\npop() 取出元素:")
    println("取出: ${buffer.pop()}")
    println("缓冲区: ${buffer.toList()}")
    
    // 索引访问
    println("\n索引访问:")
    buffer.push(4)
    buffer.push(5)
    println("缓冲区: ${buffer.toList()}")
    println("buffer[0] = ${buffer[0]} (最老)")
    println("buffer[2] = ${buffer[2]} (中间)")
    println("buffer[${buffer.size - 1}] = ${buffer[buffer.size - 1]} (最新)")
}

/**
 * 示例 2: 日志系统应用 - 保留最近 N 条日志
 */
fun logSystemExample() {
    println("\n【示例 2: 日志系统应用】")
    println("-".repeat(40))
    
    class SimpleLogger(private val maxLogs: Int) {
        private val logBuffer = RingBuffer<LogEntry>(maxLogs)
        
        data class LogEntry(
            val timestamp: Long,
            val level: String,
            val message: String
        )
        
        fun log(level: String, message: String) {
            logBuffer.push(LogEntry(
                timestamp = System.currentTimeMillis(),
                level = level,
                message = message
            ))
        }
        
        fun info(message: String) = log("INFO", message)
        fun warn(message: String) = log("WARN", message)
        fun error(message: String) = log("ERROR", message)
        
        fun getRecentLogs(count: Int = maxLogs): List<LogEntry> {
            return logBuffer.takeLast(count)
        }
        
        fun getErrors(): List<LogEntry> {
            return logBuffer.filter { it.level == "ERROR" }
        }
        
        fun clear() = logBuffer.clear()
    }
    
    val logger = SimpleLogger(5)
    
    logger.info("应用启动")
    logger.info("加载配置文件")
    logger.warn("配置项缺失，使用默认值")
    logger.info("连接数据库")
    logger.error("数据库连接失败")
    logger.info("重试连接...")  // 这会覆盖第一条日志
    logger.info("连接成功")    // 这会覆盖第二条日志
    
    println("最近 5 条日志:")
    logger.getRecentLogs().forEach { 
        println("  [${it.level}] ${it.message}")
    }
    
    println("\n所有错误日志:")
    logger.getErrors().forEach {
        println("  [ERROR] ${it.message}")
    }
}

/**
 * 示例 3: 滑动窗口计算 - 移动平均
 */
fun slidingWindowExample() {
    println("\n【示例 3: 滑动窗口计算】")
    println("-".repeat(40))
    
    class MovingAverage(private val windowSize: Int) {
        private val buffer = RingBuffer<Double>(windowSize)
        private var sum = 0.0
        
        fun add(value: Double): Double {
            // 如果缓冲区满，减去即将被覆盖的值
            if (buffer.isFull()) {
                sum -= buffer.peek()!!
            }
            
            buffer.push(value)
            sum += value
            
            return sum / buffer.size
        }
        
        fun getAverage(): Double {
            if (buffer.isEmpty()) return 0.0
            return sum / buffer.size
        }
        
        fun getValues(): List<Double> = buffer.toList()
        
        fun reset() {
            buffer.clear()
            sum = 0.0
        }
    }
    
    val ma = MovingAverage(5)
    val values = listOf(10.0, 12.0, 15.0, 14.0, 16.0, 18.0, 20.0, 19.0)
    
    println("计算窗口大小为 5 的移动平均:")
    for (value in values) {
        val avg = ma.add(value)
        println("  添加 $value -> 平均: ${"%.2f".format(avg)} (窗口: ${ma.getValues()})")
    }
}

/**
 * 示例 4: 事件历史记录 - 撤销/重做
 */
fun eventHistoryExample() {
    println("\n【示例 4: 事件历史记录】")
    println("-".repeat(40))
    
    class UndoRedoManager<T>(private val maxHistory: Int) {
        private val history = RingBuffer<T>(maxHistory, threadSafe = false)
        private var redoStack = mutableListOf<T>()
        
        fun execute(action: T) {
            history.push(action)
            redoStack.clear()  // 新操作清空重做栈
        }
        
        fun undo(): T? {
            val action = history.pop()
            if (action != null) {
                redoStack.add(action)
            }
            return action
        }
        
        fun redo(): T? {
            if (redoStack.isEmpty()) return null
            val action = redoStack.removeAt(redoStack.size - 1)
            history.push(action)
            return action
        }
        
        fun canUndo(): Boolean = !history.isEmpty()
        fun canRedo(): Boolean = redoStack.isNotEmpty()
        
        fun getHistory(): List<T> = history.toList()
    }
    
    val manager = UndoRedoManager<String>(5)
    
    println("执行操作:")
    manager.execute("创建文件")
    manager.execute("编辑文件")
    manager.execute("保存文件")
    println("历史记录: ${manager.getHistory()}")
    
    println("\n撤销操作:")
    manager.undo()
    println("撤销后历史: ${manager.getHistory()}")
    println("可以重做: ${manager.canRedo()}")
    
    println("\n重做操作:")
    manager.redo()
    println("重做后历史: ${manager.getHistory()}")
}

/**
 * 示例 5: 生产者-消费者模式（非阻塞）
 */
fun producerConsumerExample() {
    println("\n【示例 5: 生产者-消费者模式】")
    println("-".repeat(40))
    
    val buffer = RingBuffer<String>(3)
    buffer.overwriteMode = false
    
    // 模拟生产者
    fun produce(items: List<String>) {
        for (item in items) {
            if (buffer.push(item)) {
                println("  [生产] $item 成功 (大小: ${buffer.size})")
            } else {
                println("  [生产] $item 失败 - 缓冲区已满!")
            }
        }
    }
    
    // 模拟消费者
    fun consume(count: Int) {
        repeat(count) {
            val item = buffer.pop()
            if (item != null) {
                println("  [消费] $item (大小: ${buffer.size})")
            } else {
                println("  [消费] 无内容 - 缓冲区为空!")
            }
        }
    }
    
    println("生产 4 个项目 (容量 3):")
    produce(listOf("A", "B", "C", "D"))
    
    println("\n消费 2 个项目:")
    consume(2)
    
    println("\n继续生产:")
    produce(listOf("E", "F"))
    
    println("\n清空缓冲区:")
    consume(10)
}

/**
 * 示例 6: 线程安全使用
 */
fun threadSafeExample() {
    println("\n【示例 6: 线程安全使用】")
    println("-".repeat(40))
    
    val buffer = RingBuffer<Int>(100, threadSafe = true)
    
    println("多线程环境下的安全操作:")
    
    // 创建多个线程同时写入
    val threads = (1..5).map { threadId ->
        Thread {
            for (i in 1..20) {
                buffer.push(threadId * 100 + i)
                Thread.sleep(1)  // 模拟处理时间
            }
        }
    }
    
    threads.forEach { it.start() }
    threads.forEach { it.join() }
    
    println("最终缓冲区大小: ${buffer.size}")
    println("包含所有写入的元素: ${buffer.size == 100}")
    
    // 演示 takeFirst 和 takeLast
    println("前 5 个元素: ${buffer.takeFirst(5)}")
    println("后 5 个元素: ${buffer.takeLast(5)}")
}

/**
 * 示例 7: 音频缓冲区模拟
 */
fun audioBufferExample() {
    println("\n【示例 7: 音频缓冲区模拟】")
    println("-".repeat(40))
    
    class AudioBuffer(private val capacity: Int) {
        private val buffer = RingBuffer<AudioSample>(capacity, threadSafe = true)
        
        data class AudioSample(
            val left: Float,
            val right: Float,
            val timestamp: Long
        )
        
        fun write(left: Float, right: Float) {
            buffer.push(AudioSample(left, right, System.nanoTime()))
        }
        
        fun read(): AudioSample? = buffer.pop()
        
        fun getBufferLevel(): Double = buffer.size.toDouble() / capacity
        
        fun isUnderrun(): Boolean = buffer.isEmpty()
        
        fun isOverrun(): Boolean = buffer.isFull()
        
        fun clear() = buffer.clear()
    }
    
    val audioBuffer = AudioBuffer(10)
    
    println("模拟音频缓冲:")
    
    // 写入
    println("写入 5 个采样:")
    for (i in 1..5) {
        val sample = i.toFloat() / 10
        audioBuffer.write(sample, sample)
        println("  写入采样: L=$sample, R=$sample")
    }
    println("缓冲区使用率: ${"%.0f".format(audioBuffer.getBufferLevel() * 100)}%")
    
    // 读取
    println("\n读取 3 个采样:")
    repeat(3) {
        val sample = audioBuffer.read()
        println("  读取采样: L=${sample?.left}, R=${sample?.right}")
    }
    println("缓冲区使用率: ${"%.0f".format(audioBuffer.getBufferLevel() * 100)}%")
    
    println("\n缓冲区状态:")
    println("  欠载: ${audioBuffer.isUnderrun()}")
    println("  过载: ${audioBuffer.isOverrun()}")
}

/**
 * 示例 8: 扩展函数使用
 */
fun extensionFunctionExample() {
    println("\n【示例 8: 扩展函数使用】")
    println("-".repeat(40))
    
    // 从列表创建环形缓冲区
    val list = listOf("a", "b", "c", "d", "e")
    println("原始列表: $list")
    
    val buffer1 = list.toRingBuffer()
    println("toRingBuffer(): 容量=${buffer1.capacity}, 内容=${buffer1.toList()}")
    
    val buffer2 = list.toRingBuffer(capacity = 3)
    println("toRingBuffer(3): 容量=${buffer2.capacity}, 内容=${buffer2.toList()}")
    
    // 创建空缓冲区
    val emptyBuffer = emptyRingBuffer<String>(5)
    println("emptyRingBuffer(5): 容量=${emptyBuffer.capacity}, 大小=${emptyBuffer.size}")
    
    // 链式操作
    println("\n链式操作演示:")
    val numbers = (1..10).toList().toRingBuffer(5)
    println("1-10 取最后 5 个: ${numbers.toList()}")
    
    // 过滤
    val evens = numbers.filter { it % 2 == 0 }
    println("过滤偶数: $evens")
    
    // 查找
    val found = numbers.find { it > 5 }
    println("查找 > 5: $found")
    
    // 反向迭代
    print("反向迭代: ")
    numbers.reversedIterator().forEach { print("$it ") }
    println()
}