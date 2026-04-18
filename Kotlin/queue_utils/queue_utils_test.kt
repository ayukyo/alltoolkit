/**
 * AllToolkit - Kotlin Queue Utilities Test Suite
 * 
 * 全面测试队列工具模块的所有功能
 * 包括：循环队列、线程安全队列、优先级队列、双端队列、延迟队列、工具函数
 */

package queue_utils

import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger
import kotlin.test.*

/**
 * 测试主类
 */
class QueueUtilsTest {
    
    // ==================== 循环队列测试 ====================
    
    @Test
    fun testCircularQueueBasicOperations() {
        val queue = CircularQueue<Int>(3)
        
        assertTrue(queue.isEmpty())
        assertEquals(0, queue.size)
        assertNull(queue.peek())
        assertNull(queue.dequeue())
        
        assertTrue(queue.enqueue(1))
        assertTrue(queue.enqueue(2))
        assertTrue(queue.enqueue(3))
        
        assertEquals(3, queue.size)
        assertTrue(queue.isFull())
        assertFalse(queue.enqueue(4)) // 已满，无法添加
        
        assertEquals(1, queue.peek())
        assertEquals(1, queue.dequeue())
        assertEquals(2, queue.size)
        
        assertTrue(queue.enqueue(4)) // 空出位置后可以添加
        assertEquals(3, queue.size)
    }
    
    @Test
    fun testCircularQueueWrapAround() {
        val queue = CircularQueue<Int>(3)
        
        // 填满队列
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        // 出队两个
        assertEquals(1, queue.dequeue())
        assertEquals(2, queue.dequeue())
        
        // 添加两个（测试环形）
        assertTrue(queue.enqueue(4))
        assertTrue(queue.enqueue(5))
        
        // 验证顺序
        assertEquals(listOf(3, 4, 5), queue.toList())
    }
    
    @Test
    fun testCircularQueueClear() {
        val queue = CircularQueue<String>(5)
        queue.enqueue("a")
        queue.enqueue("b")
        queue.enqueue("c")
        
        queue.clear()
        
        assertTrue(queue.isEmpty())
        assertEquals(0, queue.size)
        assertNull(queue.peek())
    }
    
    @Test
    fun testCircularQueueToList() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        assertEquals(listOf(1, 2, 3), queue.toList())
    }
    
    @Test
    fun testCircularQueueCapacity() {
        val queue = CircularQueue<Int>(5)
        
        assertEquals(5, queue.available())
        queue.enqueue(1)
        assertEquals(4, queue.available())
        queue.enqueue(2)
        assertEquals(3, queue.available())
        queue.dequeue()
        assertEquals(4, queue.available())
    }
    
    @Test
    fun testCircularQueueInvalidCapacity() {
        assertFailsWith<IllegalArgumentException> {
            CircularQueue<Int>(0)
        }
        assertFailsWith<IllegalArgumentException> {
            CircularQueue<Int>(-1)
        }
    }
    
    // ==================== 线程安全队列测试 ====================
    
    @Test
    fun testThreadSafeQueueBasicOperations() {
        val queue = ThreadSafeQueue<String>()
        
        assertTrue(queue.isEmpty())
        assertTrue(queue.enqueue("a"))
        assertTrue(queue.enqueue("b"))
        assertTrue(queue.enqueue("c"))
        
        assertEquals(3, queue.size)
        assertEquals("a", queue.peek())
        assertEquals("a", queue.dequeue())
        assertEquals("b", queue.dequeue())
        assertEquals("c", queue.dequeue())
        assertTrue(queue.isEmpty())
    }
    
    @Test
    fun testThreadSafeQueueWithCapacity() {
        val queue = ThreadSafeQueue<Int>(2)
        
        assertTrue(queue.enqueue(1))
        assertTrue(queue.enqueue(2))
        assertFalse(queue.enqueue(3)) // 容量已满
        
        assertEquals(2, queue.size)
        assertEquals(0, queue.remainingCapacity())
    }
    
    @Test
    fun testThreadSafeQueueOfferAndPoll() {
        val queue = ThreadSafeQueue<Int>(2)
        
        assertTrue(queue.offer(1, 100))
        assertTrue(queue.offer(2, 100))
        assertFalse(queue.offer(3, 10)) // 超时后失败
        
        assertEquals(1, queue.poll(10))
        assertEquals(2, queue.poll(10))
        assertNull(queue.poll(10)) // 超时后返回 null
    }
    
    @Test
    fun testThreadSafeQueueClear() {
        val queue = ThreadSafeQueue<Int>()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        queue.clear()
        
        assertTrue(queue.isEmpty())
        assertEquals(0, queue.size)
    }
    
    @Test
    fun testThreadSafeQueueDrainTo() {
        val queue = ThreadSafeQueue<Int>()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        
        val target = mutableListOf<Int>()
        val count = queue.drainTo(target, 3)
        
        assertEquals(3, count)
        assertEquals(listOf(1, 2, 3), target)
        assertEquals(listOf(4, 5), queue.toList())
    }
    
    @Test
    fun testThreadSafeQueueConcurrentAccess() {
        val queue = ThreadSafeQueue<Int>()
        val producerCount = 1000
        val consumerCount = 1000
        val latch = CountDownLatch(2)
        val produced = AtomicInteger(0)
        val consumed = AtomicInteger(0)
        
        // 生产者线程
        Thread {
            repeat(producerCount) {
                queue.put(it)
                produced.incrementAndGet()
            }
            latch.countDown()
        }.start()
        
        // 消费者线程
        Thread {
            repeat(consumerCount) {
                queue.take()
                consumed.incrementAndGet()
            }
            latch.countDown()
        }.start()
        
        latch.await(10, TimeUnit.SECONDS)
        
        assertEquals(producerCount, produced.get())
        assertEquals(consumerCount, consumed.get())
        assertTrue(queue.isEmpty())
    }
    
    // ==================== 优先级队列测试 ====================
    
    @Test
    fun testPriorityQueueBasicOperations() {
        val queue = PriorityAwareQueue<String>()
        
        assertTrue(queue.isEmpty())
        queue.enqueue("low", 10)
        queue.enqueue("high", 1)
        queue.enqueue("medium", 5)
        
        assertEquals(3, queue.size)
        assertEquals("high", queue.peek()) // 最高优先级（数值最小）
        
        assertEquals("high", queue.dequeue())
        assertEquals("medium", queue.dequeue())
        assertEquals("low", queue.dequeue())
        assertTrue(queue.isEmpty())
    }
    
    @Test
    fun testPriorityQueueDefaultPriority() {
        val queue = PriorityAwareQueue<Int>()
        
        queue.enqueue(1) // 默认优先级 0
        queue.enqueue(2, -1) // 更高优先级
        queue.enqueue(3, 1) // 更低优先级
        
        assertEquals(2, queue.dequeue()) // -1 优先级最高
        assertEquals(1, queue.dequeue()) // 0 优先级
        assertEquals(3, queue.dequeue()) // 1 优先级
    }
    
    @Test
    fun testPriorityQueuePeekWithPriority() {
        val queue = PriorityAwareQueue<String>()
        queue.enqueue("task1", 5)
        queue.enqueue("task2", 1)
        
        val result = queue.peekWithPriority()
        assertNotNull(result)
        assertEquals("task2", result.first)
        assertEquals(1, result.second)
    }
    
    @Test
    fun testPriorityQueueWithCapacity() {
        val queue = PriorityAwareQueue<Int>(2)
        
        assertTrue(queue.enqueue(1, 1))
        assertTrue(queue.enqueue(2, 2))
        assertFalse(queue.enqueue(3, 0)) // 容量已满
    }
    
    @Test
    fun testPriorityQueueToListWithPriority() {
        val queue = PriorityAwareQueue<String>()
        queue.enqueue("c", 3)
        queue.enqueue("a", 1)
        queue.enqueue("b", 2)
        
        val list = queue.toListWithPriority()
        assertEquals(listOf("a" to 1, "b" to 2, "c" to 3), list)
    }
    
    @Test
    fun testPriorityQueueClear() {
        val queue = PriorityAwareQueue<Int>()
        queue.enqueue(1, 1)
        queue.enqueue(2, 2)
        
        queue.clear()
        
        assertTrue(queue.isEmpty())
        assertEquals(0, queue.size)
    }
    
    // ==================== 双端队列测试 ====================
    
    @Test
    fun testDequeBasicOperations() {
        val deque = ArrayDequeImpl<Int>()
        
        assertTrue(deque.isEmpty())
        deque.addFirst(1)
        deque.addLast(2)
        deque.addFirst(0)
        
        assertEquals(3, deque.size)
        assertEquals(0, deque.peekFirst())
        assertEquals(2, deque.peekLast())
        
        assertEquals(0, deque.removeFirst())
        assertEquals(2, deque.removeLast())
        assertEquals(1, deque.peek())
    }
    
    @Test
    fun testDequeEnqueueDequeue() {
        val deque = ArrayDequeImpl<String>()
        
        assertTrue(deque.enqueue("a"))
        assertTrue(deque.enqueue("b"))
        
        assertEquals("a", deque.dequeue())
        assertEquals("b", deque.dequeue())
        assertNull(deque.dequeue())
    }
    
    @Test
    fun testDequeRotate() {
        val deque = ArrayDequeImpl<Int>()
        deque.enqueue(1)
        deque.enqueue(2)
        deque.enqueue(3)
        deque.enqueue(4)
        
        // 正向旋转
        deque.rotate(1)
        assertEquals(listOf(4, 1, 2, 3), deque.toList())
        
        // 反向旋转
        deque.rotate(-1)
        assertEquals(listOf(1, 2, 3, 4), deque.toList())
        
        // 旋转超过大小
        deque.rotate(6) // 相当于旋转 2
        assertEquals(listOf(3, 4, 1, 2), deque.toList())
    }
    
    @Test
    fun testDequeEmptyOperations() {
        val deque = ArrayDequeImpl<Int>()
        
        assertNull(deque.peekFirst())
        assertNull(deque.peekLast())
        assertNull(deque.removeFirst())
        assertNull(deque.removeLast())
        assertNull(deque.dequeue())
    }
    
    @Test
    fun testDequeClear() {
        val deque = ArrayDequeImpl<Int>()
        deque.addFirst(1)
        deque.addLast(2)
        
        deque.clear()
        
        assertTrue(deque.isEmpty())
    }
    
    // ==================== 延迟队列测试 ====================
    
    @Test
    fun testDelayQueueBasicOperations() {
        val queue = DelayQueue<DelayedTask>()
        
        assertTrue(queue.isEmpty())
        assertEquals(0, queue.size)
        
        val task1 = DelayedTask({ }, 100)
        val task2 = DelayedTask({ }, 50)
        
        queue.put(task1)
        queue.put(task2)
        
        assertEquals(2, queue.size)
        assertFalse(queue.isEmpty())
        
        // 较短延迟的任务应该排在前面
        assertSame(task2, queue.peek())
    }
    
    @Test
    fun testDelayQueueTakeExpiredTask() {
        val queue = DelayQueue<DelayedTask>()
        var executed = false
        val task = DelayedTask({ executed = true }, 10) // 10ms 延迟
        
        queue.put(task)
        
        // 等待延迟到期
        Thread.sleep(20)
        
        val taken = queue.take()
        assertSame(task, taken)
        assertTrue(queue.isEmpty())
    }
    
    @Test
    fun testDelayQueuePollTimeout() {
        val queue = DelayQueue<DelayedTask>()
        val task = DelayedTask({ }, 1000) // 1秒延迟
        
        queue.put(task)
        
        // 尝试获取，但延迟未到期
        val result = queue.poll(10) // 10ms 超时
        assertNull(result)
        assertEquals(1, queue.size) // 任务仍在队列中
    }
    
    @Test
    fun testDelayQueueClear() {
        val queue = DelayQueue<DelayedTask>()
        queue.put(DelayedTask({ }, 100))
        queue.put(DelayedTask({ }, 200))
        
        queue.clear()
        
        assertTrue(queue.isEmpty())
    }
    
    // ==================== 队列工具函数测试 ====================
    
    @Test
    fun testQueueUtilsCreate() {
        val circular = QueueUtils.circular<Int>(10)
        assertTrue(circular.isEmpty())
        assertEquals(10, circular.available())
        
        val threadSafe = QueueUtils.threadSafe<String>(100)
        assertTrue(threadSafe.isEmpty())
        assertEquals(100, threadSafe.remainingCapacity())
        
        val priority = QueueUtils.priority<Int>()
        assertTrue(priority.isEmpty())
        
        val deque = QueueUtils.deque<Int>()
        assertTrue(deque.isEmpty())
    }
    
    @Test
    fun testQueueUtilsEnqueueAll() {
        val queue = CircularQueue<Int>(5)
        val items = listOf(1, 2, 3, 4, 5, 6)
        
        val count = QueueUtils.enqueueAll(queue, items)
        
        assertEquals(5, count) // 只能加入 5 个
        assertEquals(5, queue.size)
        assertTrue(queue.isFull())
    }
    
    @Test
    fun testQueueUtilsDequeueAll() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        val items = QueueUtils.dequeueAll(queue)
        
        assertEquals(listOf(1, 2, 3), items)
        assertTrue(queue.isEmpty())
    }
    
    @Test
    fun testQueueUtilsDequeueN() {
        val queue = CircularQueue<Int>(10)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        
        val items = QueueUtils.dequeueN(queue, 3)
        
        assertEquals(listOf(1, 2, 3), items)
        assertEquals(2, queue.size)
    }
    
    @Test
    fun testQueueUtilsContains() {
        val queue = CircularQueue<String>(5)
        queue.enqueue("a")
        queue.enqueue("b")
        queue.enqueue("c")
        
        assertTrue(QueueUtils.contains(queue, "b"))
        assertFalse(QueueUtils.contains(queue, "d"))
    }
    
    @Test
    fun testQueueUtilsFind() {
        val queue = CircularQueue<Int>(10)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        
        val even = QueueUtils.find(queue) { it % 2 == 0 }
        assertEquals(2, even)
        
        val greater = QueueUtils.find(queue) { it > 10 }
        assertNull(greater)
    }
    
    @Test
    fun testQueueUtilsFilter() {
        val queue = CircularQueue<Int>(10)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        
        val evens = QueueUtils.filter(queue) { it % 2 == 0 }
        assertEquals(listOf(2, 4), evens)
    }
    
    @Test
    fun testQueueUtilsMap() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        val doubled = QueueUtils.map(queue) { it * 2 }
        assertEquals(listOf(2, 4, 6), doubled)
    }
    
    @Test
    fun testQueueUtilsReverse() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        val reversed = QueueUtils.reverse(queue)
        assertEquals(listOf(3, 2, 1), reversed)
        
        // 原队列不变
        assertEquals(listOf(1, 2, 3), queue.toList())
    }
    
    @Test
    fun testQueueUtilsReduce() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        
        val sum = QueueUtils.reduce(queue, 0) { acc, it -> acc + it }
        assertEquals(10, sum)
    }
    
    @Test
    fun testQueueUtilsAll() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(2)
        queue.enqueue(4)
        queue.enqueue(6)
        
        assertTrue(QueueUtils.all(queue) { it % 2 == 0 })
        assertFalse(QueueUtils.all(queue) { it > 5 })
    }
    
    @Test
    fun testQueueUtilsAny() {
        val queue = CircularQueue<Int>(5)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        assertTrue(QueueUtils.any(queue) { it > 2 })
        assertFalse(QueueUtils.any(queue) { it > 10 })
    }
    
    @Test
    fun testQueueUtilsMerge() {
        val q1 = CircularQueue<Int>(5)
        q1.enqueue(1)
        q1.enqueue(2)
        
        val q2 = CircularQueue<Int>(5)
        q2.enqueue(3)
        q2.enqueue(4)
        
        val merged = QueueUtils.merge(q1, q2)
        assertEquals(listOf(1, 2, 3, 4), merged)
    }
    
    @Test
    fun testQueueUtilsPartition() {
        val queue = CircularQueue<Int>(10)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        
        val (evens, odds) = QueueUtils.partition(queue) { it % 2 == 0 }
        assertEquals(listOf(2, 4), evens)
        assertEquals(listOf(1, 3, 5), odds)
    }
    
    @Test
    fun testQueueUtilsDistinct() {
        val queue = CircularQueue<Int>(10)
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(3)
        queue.enqueue(3)
        
        val unique = QueueUtils.distinct(queue)
        assertEquals(listOf(1, 2, 3), unique)
    }
    
    @Test
    fun testQueueUtilsGroupBy() {
        val queue = CircularQueue<String>(10)
        queue.enqueue("apple")
        queue.enqueue("banana")
        queue.enqueue("apricot")
        queue.enqueue("blueberry")
        
        val groups = QueueUtils.groupBy(queue) { it.first() }
        assertEquals(listOf("apple", "apricot"), groups['a'])
        assertEquals(listOf("banana", "blueberry"), groups['b'])
    }
    
    @Test
    fun testQueueUtilsCountOccurrences() {
        val queue = CircularQueue<String>(10)
        queue.enqueue("a")
        queue.enqueue("b")
        queue.enqueue("a")
        queue.enqueue("c")
        queue.enqueue("a")
        
        val counts = QueueUtils.countOccurrences(queue)
        assertEquals(3, counts["a"])
        assertEquals(1, counts["b"])
        assertEquals(1, counts["c"])
    }
    
    // ==================== 边界值测试 ====================
    
    @Test
    fun testEmptyQueueOperations() {
        val queue = CircularQueue<Int>(5)
        
        assertTrue(queue.isEmpty())
        assertNull(queue.peek())
        assertNull(queue.dequeue())
        assertEquals(emptyList<Int>(), queue.toList())
        assertEquals(emptyList<Int>(), QueueUtils.dequeueAll(queue))
    }
    
    @Test
    fun testSingleElementQueue() {
        val queue = CircularQueue<String>(1)
        
        assertTrue(queue.enqueue("only"))
        assertTrue(queue.isFull())
        assertFalse(queue.enqueue("another"))
        
        assertEquals("only", queue.peek())
        assertEquals("only", queue.dequeue())
        assertTrue(queue.isEmpty())
    }
    
    @Test
    fun testLargeQueue() {
        val queue = ThreadSafeQueue<Int>()
        val count = 10000
        
        repeat(count) {
            assertTrue(queue.enqueue(it))
        }
        
        assertEquals(count, queue.size)
        
        repeat(count) {
            assertEquals(it, queue.dequeue())
        }
        
        assertTrue(queue.isEmpty())
    }
    
    @Test
    fun testPriorityQueueSamePriority() {
        val queue = PriorityAwareQueue<Int>()
        
        // 相同优先级，FIFO 顺序
        queue.enqueue(1, 5)
        queue.enqueue(2, 5)
        queue.enqueue(3, 5)
        
        assertEquals(1, queue.dequeue())
        assertEquals(2, queue.dequeue())
        assertEquals(3, queue.dequeue())
    }
    
    @Test
    fun testPriorityQueueNegativePriority() {
        val queue = PriorityAwareQueue<String>()
        
        queue.enqueue("normal", 0)
        queue.enqueue("high", -10)
        queue.enqueue("urgent", -100)
        queue.enqueue("low", 100)
        
        assertEquals("urgent", queue.dequeue())
        assertEquals("high", queue.dequeue())
        assertEquals("normal", queue.dequeue())
        assertEquals("low", queue.dequeue())
    }
}

/**
 * 主函数运行所有测试
 */
fun main() {
    println("=" .repeat(60))
    println("AllToolkit - Kotlin Queue Utilities Test Suite")
    println("=" .repeat(60))
    println()
    
    val testClass = QueueUtilsTest::class
    val methods = testClass.methods.filter { it.name.startsWith("test") }
    
    var passed = 0
    var failed = 0
    val failures = mutableListOf<String>()
    
    for (method in methods.sortedBy { it.name }) {
        try {
            val instance = QueueUtilsTest()
            method.invoke(instance)
            passed++
            println("✅ ${method.name}")
        } catch (e: Exception) {
            failed++
            val cause = e.cause ?: e
            failures.add("${method.name}: ${cause.message}")
            println("❌ ${method.name}: ${cause.message}")
        }
    }
    
    println()
    println("=" .repeat(60))
    println("Test Results: $passed passed, $failed failed")
    println("=" .repeat(60))
    
    if (failures.isNotEmpty()) {
        println("\nFailed Tests:")
        failures.forEach { println("  - $it") }
    }
    
    if (failed == 0) {
        println("\n🎉 All tests passed!")
    } else {
        println("\n⚠️ Some tests failed!")
        kotlin.system.exitProcess(1)
    }
}