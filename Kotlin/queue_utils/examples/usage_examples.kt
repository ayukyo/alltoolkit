/**
 * AllToolkit - Kotlin Queue Utilities Usage Examples
 * 
 * 展示队列工具模块的各种使用场景
 */

package queue_utils.examples

import queue_utils.*
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

fun main() {
    println("=" .repeat(60))
    println("AllToolkit - Kotlin Queue Utilities Examples")
    println("=" .repeat(60))
    println()
    
    // 示例 1: 循环队列
    circularQueueExample()
    
    // 示例 2: 线程安全队列
    threadSafeQueueExample()
    
    // 示例 3: 优先级队列
    priorityQueueExample()
    
    // 示例 4: 双端队列
    dequeExample()
    
    // 示例 5: 延迟队列
    delayQueueExample()
    
    // 示例 6: 生产者-消费者模式
    producerConsumerExample()
    
    // 示例 7: 任务调度器
    taskSchedulerExample()
    
    // 示例 8: 工具函数
    utilityFunctionsExample()
    
    println("\n" + "=".repeat(60))
    println("All examples completed!")
    println("=".repeat(60))
}

/**
 * 示例 1: 循环队列
 * 适用于固定容量的缓冲区场景
 */
fun circularQueueExample() {
    println("\n📌 Example 1: Circular Queue (Fixed Capacity Buffer)")
    println("-".repeat(50))
    
    // 创建容量为 5 的循环队列
    val buffer = CircularQueue<String>(5)
    
    println("Created circular queue with capacity 5")
    
    // 添加元素
    buffer.enqueue("A")
    buffer.enqueue("B")
    buffer.enqueue("C")
    println("Enqueued: A, B, C")
    println("Size: ${buffer.size}, Available: ${buffer.available()}")
    
    // 填满队列
    buffer.enqueue("D")
    buffer.enqueue("E")
    println("Enqueued: D, E")
    println("Is full: ${buffer.isFull()}")
    
    // 尝试添加到已满队列
    val added = buffer.enqueue("F")
    println("Try to add F to full queue: ${if (added) "success" else "failed"}")
    
    // 出队并查看
    println("Dequeued: ${buffer.dequeue()}")
    println("Peek: ${buffer.peek()}")
    
    // 环形特性演示
    buffer.enqueue("F")
    buffer.enqueue("G")
    println("After adding F, G: ${buffer.toList()}")
    
    println("✅ Circular Queue Example completed\n")
}

/**
 * 示例 2: 线程安全队列
 * 支持阻塞操作和超时
 */
fun threadSafeQueueExample() {
    println("\n📌 Example 2: Thread-Safe Blocking Queue")
    println("-".repeat(50))
    
    // 创建容量为 3 的线程安全队列
    val queue = ThreadSafeQueue<Int>(3)
    
    println("Created thread-safe queue with capacity 3")
    
    // 基本操作
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    println("Enqueued: 1, 2, 3")
    println("Remaining capacity: ${queue.remainingCapacity()}")
    
    // 超时 offer
    val offered = queue.offer(4, 100) // 100ms 超时
    println("Offer 4 with 100ms timeout: ${if (offered) "success" else "failed (queue full)"}")
    
    // 超时 poll
    val polled = queue.poll(50)
    println("Poll with 50ms timeout: $polled")
    
    // 批量转移
    val target = mutableListOf<Int>()
    queue.drainTo(target)
    println("Drained to list: $target")
    
    println("✅ Thread-Safe Queue Example completed\n")
}

/**
 * 示例 3: 优先级队列
 * 任务按优先级处理
 */
fun priorityQueueExample() {
    println("\n📌 Example 3: Priority Queue")
    println("-".repeat(50))
    
    val taskQueue = PriorityAwareQueue<String>()
    
    // 添加不同优先级的任务
    taskQueue.enqueue("Normal task 1", 5)
    taskQueue.enqueue("Urgent task", 1)    // 最高优先级（数值最小）
    taskQueue.enqueue("Normal task 2", 5)
    taskQueue.enqueue("High priority", 2)
    taskQueue.enqueue("Low priority", 10)
    
    println("Tasks added with priorities:")
    taskQueue.toListWithPriority().forEach { (task, priority) ->
        println("  Priority $priority: $task")
    }
    
    println("\nProcessing in priority order:")
    while (taskQueue.isNotEmpty) {
        val (task, priority) = taskQueue.peekWithPriority()!!
        println("  [Priority $priority] Processing: $task")
        taskQueue.dequeue()
    }
    
    println("✅ Priority Queue Example completed\n")
}

/**
 * 示例 4: 双端队列
 * 支持头部和尾部操作
 */
fun dequeExample() {
    println("\n📌 Example 4: Double-Ended Queue (Deque)")
    println("-".repeat(50))
    
    val deque = ArrayDequeImpl<String>()
    
    // 添加到两端
    deque.addFirst("B")
    deque.addFirst("A")  // 头部
    deque.addLast("C")  // 尾部
    deque.addLast("D")   // 尾部
    
    println("After addFirst(A), addFirst(B), addLast(C), addLast(D):")
    println("  Queue: ${deque.toList()}")
    println("  First: ${deque.peekFirst()}, Last: ${deque.peekLast()}")
    
    // 旋转操作
    deque.rotate(1)  // 向右旋转 1 位
    println("\nAfter rotate(1): ${deque.toList()}")
    
    deque.rotate(-2)  // 向左旋转 2 位
    println("After rotate(-2): ${deque.toList()}")
    
    // 从两端移除
    println("\nRemove first: ${deque.removeFirst()}")
    println("Remove last: ${deque.removeLast()}")
    println("Remaining: ${deque.toList()}")
    
    println("✅ Deque Example completed\n")
}

/**
 * 示例 5: 延迟队列
 * 任务延迟执行
 */
fun delayQueueExample() {
    println("\n📌 Example 5: Delay Queue")
    println("-".repeat(50))
    
    val delayQueue = DelayQueue<DelayedTask>()
    
    // 添加延迟任务
    delayQueue.put(DelayedTask({ println("  [Task C] Executed after 200ms") }, 200))
    delayQueue.put(DelayedTask({ println("  [Task A] Executed after 50ms") }, 50))
    delayQueue.put(DelayedTask({ println("  [Task B] Executed after 100ms") }, 100))
    
    println("Added 3 tasks with different delays (50ms, 100ms, 200ms)")
    println("Tasks will execute in delay order (shortest first)")
    println("\nExecuting tasks:")
    
    val startTime = System.currentTimeMillis()
    
    while (delayQueue.isNotEmpty) {
        val task = delayQueue.poll(500) // 500ms 超时
        if (task != null) {
            val elapsed = System.currentTimeMillis() - startTime
            print("  [${elapsed}ms] ")
            task.execute()
        } else {
            break
        }
    }
    
    println("\n✅ Delay Queue Example completed\n")
}

/**
 * 示例 6: 生产者-消费者模式
 * 多线程协作
 */
fun producerConsumerExample() {
    println("\n📌 Example 6: Producer-Consumer Pattern")
    println("-".repeat(50))
    
    val queue = ThreadSafeQueue<Int>(10)
    val itemCount = 20
    val producerLatch = CountDownLatch(1)
    val consumerLatch = CountDownLatch(1)
    val produced = AtomicInteger(0)
    val consumed = AtomicInteger(0)
    
    println("Starting producer-consumer with ${itemCount} items")
    
    // 生产者
    Thread {
        repeat(itemCount) { i ->
            queue.put(i)
            produced.incrementAndGet()
            print("P")
            Thread.sleep(10) // 模拟生产延迟
        }
        producerLatch.countDown()
    }.start()
    
    // 消费者
    Thread {
        repeat(itemCount) {
            queue.take()
            consumed.incrementAndGet()
            print("C")
            Thread.sleep(15) // 模拟消费延迟
        }
        consumerLatch.countDown()
    }.start()
    
    producerLatch.await()
    consumerLatch.await()
    
    println("\n\nProduced: ${produced.get()}, Consumed: ${consumed.get()}")
    println("Queue is empty: ${queue.isEmpty()}")
    
    println("✅ Producer-Consumer Example completed\n")
}

/**
 * 示例 7: 任务调度器
 * 使用优先级队列实现任务调度
 */
fun taskSchedulerExample() {
    println("\n📌 Example 7: Task Scheduler")
    println("-".repeat(50))
    
    data class Task(
        val name: String,
        val priority: Int,
        val description: String
    )
    
    val scheduler = PriorityAwareQueue<Task>()
    
    // 添加任务
    scheduler.enqueue(Task("backup", 10, "Database backup"), 10)
    scheduler.enqueue(Task("email", 3, "Send urgent email"), 3)
    scheduler.enqueue(Task("report", 5, "Generate report"), 5)
    scheduler.enqueue(Task("alert", 1, "System alert"), 1)
    scheduler.enqueue(Task("cleanup", 15, "Temp files cleanup"), 15)
    
    println("Task queue (sorted by priority):")
    scheduler.toListWithPriority().forEach { (task, priority) ->
        println("  [$priority] ${task.name}: ${task.description}")
    }
    
    println("\nExecuting tasks:")
    while (scheduler.isNotEmpty) {
        val task = scheduler.dequeue()!!
        println("  Executing: ${task.name} (priority ${task.priority})")
        println("    → ${task.description}")
    }
    
    println("✅ Task Scheduler Example completed\n")
}

/**
 * 示例 8: 工具函数
 * 队列操作辅助函数
 */
fun utilityFunctionsExample() {
    println("\n📌 Example 8: Utility Functions")
    println("-".repeat(50))
    
    val queue = CircularQueue<Int>(10)
    QueueUtils.enqueueAll(queue, listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    println("Queue: ${queue.toList()}")
    
    // 过滤
    val evens = QueueUtils.filter(queue) { it % 2 == 0 }
    println("Even numbers: $evens")
    
    // 映射
    val squared = QueueUtils.map(queue) { it * it }
    println("Squared: $squared")
    
    // 归约
    val sum = QueueUtils.reduce(queue, 0) { acc, it -> acc + it }
    println("Sum: $sum")
    
    // 查找
    val found = QueueUtils.find(queue) { it > 5 }
    println("First > 5: $found")
    
    // 分区
    val (lessThan5, greaterOrEqual5) = QueueUtils.partition(queue) { it < 5 }
    println("Partition (<5 vs >=5): $lessThan5 | $greaterOrEqual5")
    
    // 分组
    val groups = QueueUtils.groupBy(queue) { it % 3 }
    println("Grouped by mod 3:")
    groups.forEach { (key, values) ->
        println("  $key: $values")
    }
    
    // 去重
    val dupQueue = CircularQueue<Int>(10)
    QueueUtils.enqueueAll(dupQueue, listOf(1, 2, 2, 3, 3, 3, 4))
    println("\nQueue with duplicates: ${dupQueue.toList()}")
    println("Distinct: ${QueueUtils.distinct(dupQueue)}")
    
    // 统计
    val countQueue = CircularQueue<String>(10)
    QueueUtils.enqueueAll(countQueue, listOf("a", "b", "a", "c", "a", "b"))
    println("\nCount occurrences: ${QueueUtils.countOccurrences(countQueue)}")
    
    // 反转
    println("\nReversed: ${QueueUtils.reverse(queue)}")
    
    // 合并
    val q1 = CircularQueue<Int>(5)
    val q2 = CircularQueue<Int>(5)
    QueueUtils.enqueueAll(q1, listOf(1, 2))
    QueueUtils.enqueueAll(q2, listOf(3, 4))
    println("Merged: ${QueueUtils.merge(q1, q2)}")
    
    // 批量操作
    val batchQueue = CircularQueue<Int>(10)
    QueueUtils.enqueueAll(batchQueue, listOf(1, 2, 3, 4, 5))
    println("\nDequeue all: ${QueueUtils.dequeueAll(batchQueue)}")
    println("Dequeue 3 from empty: ${QueueUtils.dequeueN(batchQueue, 3)}")
    
    QueueUtils.enqueueAll(batchQueue, listOf(1, 2, 3, 4, 5))
    println("Dequeue 3 from [1,2,3,4,5]: ${QueueUtils.dequeueN(batchQueue, 3)}")
    
    println("✅ Utility Functions Example completed\n")
}