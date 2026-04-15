/**
 * Ring Buffer 测试文件
 * 
 * 包含完整的单元测试，验证所有功能
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-04-15
 */

package ring_buffer_utils

import org.junit.Test
import org.junit.Assert.*
import org.junit.Before
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

class RingBufferTest {
    
    private lateinit var buffer: RingBuffer<Int>
    
    @Before
    fun setup() {
        buffer = RingBuffer(5)
    }
    
    // ==================== 基本功能测试 ====================
    
    @Test
    fun testEmptyBuffer() {
        assertTrue(buffer.isEmpty())
        assertFalse(buffer.isFull())
        assertEquals(0, buffer.size)
        assertNull(buffer.pop())
        assertNull(buffer.peek())
        assertNull(buffer.peekLast())
    }
    
    @Test
    fun testPushAndPop() {
        assertTrue(buffer.push(1))
        assertEquals(1, buffer.size)
        assertFalse(buffer.isEmpty())
        
        assertTrue(buffer.push(2))
        assertTrue(buffer.push(3))
        
        assertEquals(3, buffer.size)
        assertEquals(1, buffer.peek())
        assertEquals(3, buffer.peekLast())
        
        assertEquals(1, buffer.pop())
        assertEquals(2, buffer.size)
        assertEquals(2, buffer.peek())
    }
    
    @Test
    fun testFIFOOrder() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        for (i in 1..5) {
            assertEquals(i, buffer.pop())
        }
        
        assertTrue(buffer.isEmpty())
    }
    
    @Test
    fun testOverwriteMode() {
        buffer.overwriteMode = true
        
        // 填满缓冲区
        for (i in 1..5) {
            buffer.push(i)
        }
        
        assertTrue(buffer.isFull())
        assertEquals(5, buffer.size)
        
        // 继续添加，应该覆盖最老的元素
        buffer.push(6)
        assertEquals(5, buffer.size)  // 大小不变
        assertEquals(2, buffer.peek()) // 1 被覆盖，现在最老的是 2
        
        buffer.push(7)
        assertEquals(3, buffer.peek()) // 2 被覆盖
    }
    
    @Test
    fun testNonOverwriteMode() {
        buffer.overwriteMode = false
        
        // 填满缓冲区
        for (i in 1..5) {
            assertTrue(buffer.push(i))
        }
        
        // 尝试添加第 6 个元素，应该失败
        assertFalse(buffer.push(6))
        assertEquals(5, buffer.size)
        assertEquals(1, buffer.peek())
    }
    
    // ==================== 容量和可用空间测试 ====================
    
    @Test
    fun testCapacityAndAvailable() {
        assertEquals(5, buffer.capacity)
        assertEquals(5, buffer.available())
        
        buffer.push(1)
        assertEquals(4, buffer.available())
        
        buffer.push(2)
        buffer.push(3)
        assertEquals(2, buffer.available())
        
        buffer.pop()
        assertEquals(3, buffer.available())
    }
    
    // ==================== 索引访问测试 ====================
    
    @Test
    fun testIndexAccess() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        assertEquals(1, buffer[0])
        assertEquals(2, buffer[1])
        assertEquals(3, buffer[2])
        assertEquals(4, buffer[3])
        assertEquals(5, buffer[4])
    }
    
    @Test(expected = IndexOutOfBoundsException::class)
    fun testIndexOutOfBounds() {
        buffer.push(1)
        buffer[5]  // 应该抛出异常
    }
    
    @Test(expected = IndexOutOfBoundsException::class)
    fun testNegativeIndex() {
        buffer.push(1)
        buffer[-1]  // 应该抛出异常
    }
    
    // ==================== 批量操作测试 ====================
    
    @Test
    fun testPushAll() {
        val items = listOf(1, 2, 3, 4, 5)
        val count = buffer.pushAll(items)
        
        assertEquals(5, count)
        assertEquals(5, buffer.size)
        assertEquals(1, buffer.peek())
        assertEquals(5, buffer.peekLast())
    }
    
    @Test
    fun testPushAllOverflow() {
        buffer.overwriteMode = true
        val items = listOf(1, 2, 3, 4, 5, 6, 7, 8)
        val count = buffer.pushAll(items)
        
        assertEquals(8, count)
        assertEquals(5, buffer.size)  // 只有最后 5 个
        assertEquals(4, buffer.peek())  // 最老的是 4
        assertEquals(8, buffer.peekLast())  // 最新的是 8
    }
    
    @Test
    fun testToList() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        val list = buffer.toList()
        assertEquals(listOf(1, 2, 3, 4, 5), list)
    }
    
    @Test
    fun testToArray() {
        for (i in 1..3) {
            buffer.push(i)
        }
        
        val array = buffer.toArray()
        assertEquals(3, array.size)
        assertEquals(1, array[0])
        assertEquals(2, array[1])
        assertEquals(3, array[2])
    }
    
    // ==================== 查询操作测试 ====================
    
    @Test
    fun testContains() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        assertTrue(buffer.contains(3))
        assertTrue(buffer.contains(1))
        assertTrue(buffer.contains(5))
        assertFalse(buffer.contains(6))
        assertFalse(buffer.contains(0))
    }
    
    @Test
    fun testContainsAll() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        assertTrue(buffer.containsAll(listOf(2, 3, 4)))
        assertFalse(buffer.containsAll(listOf(2, 3, 6)))
    }
    
    @Test
    fun testFind() {
        for (i in 1..10) {
            buffer.push(i)
        }
        
        val result = buffer.find { it > 5 }
        assertEquals(6, result)  // 第一个大于 5 的
        
        val notFound = buffer.find { it > 20 }
        assertNull(notFound)
    }
    
    @Test
    fun testFilter() {
        for (i in 1..10) {
            buffer.push(i)
        }
        
        val evens = buffer.filter { it % 2 == 0 }
        assertEquals(listOf(2, 4, 6, 8, 10), evens)
    }
    
    // ==================== take 操作测试 ====================
    
    @Test
    fun testTakeFirst() {
        for (i in 1..10) {
            buffer.push(i)
        }
        
        val first3 = buffer.takeFirst(3)
        assertEquals(listOf(1, 2, 3), first3)
        
        // 原缓冲区不变
        assertEquals(10, buffer.size)
    }
    
    @Test
    fun testTakeLast() {
        for (i in 1..10) {
            buffer.push(i)
        }
        
        val last3 = buffer.takeLast(3)
        assertEquals(listOf(8, 9, 10), last3)
        
        // 原缓冲区不变
        assertEquals(10, buffer.size)
    }
    
    @Test
    fun testTakeMoreThanSize() {
        for (i in 1..3) {
            buffer.push(i)
        }
        
        val first = buffer.takeFirst(10)
        assertEquals(listOf(1, 2, 3), first)
        
        val last = buffer.takeLast(10)
        assertEquals(listOf(1, 2, 3), last)
    }
    
    // ==================== 清空操作测试 ====================
    
    @Test
    fun testClear() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        buffer.clear()
        
        assertTrue(buffer.isEmpty())
        assertEquals(0, buffer.size)
        assertNull(buffer.peek())
        assertNull(buffer.pop())
    }
    
    // ==================== 迭代器测试 ====================
    
    @Test
    fun testIterator() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        val list = mutableListOf<Int>()
        for (item in buffer) {
            list.add(item)
        }
        
        assertEquals(listOf(1, 2, 3, 4, 5), list)
    }
    
    @Test
    fun testReversedIterator() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        val list = mutableListOf<Int>()
        val iter = buffer.reversedIterator()
        while (iter.hasNext()) {
            list.add(iter.next())
        }
        
        assertEquals(listOf(5, 4, 3, 2, 1), list)
    }
    
    @Test
    fun testForEach() {
        for (i in 1..5) {
            buffer.push(i)
        }
        
        var sum = 0
        buffer.forEach { sum += it }
        assertEquals(15, sum)
    }
    
    // ==================== toString 测试 ====================
    
    @Test
    fun testToString() {
        buffer.push(1)
        buffer.push(2)
        buffer.push(3)
        
        val str = buffer.toString()
        assertTrue(str.contains("RingBuffer"))
        assertTrue(str.contains("capacity=5"))
        assertTrue(str.contains("size=3"))
        assertTrue(str.contains("1"))
        assertTrue(str.contains("2"))
        assertTrue(str.contains("3"))
    }
    
    // ==================== 边界条件测试 ====================
    
    @Test
    fun testSingleCapacity() {
        val singleBuffer = RingBuffer<String>(1)
        assertTrue(singleBuffer.isEmpty())
        assertEquals(1, singleBuffer.capacity)
        
        singleBuffer.push("only")
        assertTrue(singleBuffer.isFull())
        assertEquals("only", singleBuffer.peek())
        assertEquals("only", singleBuffer.peekLast())
        
        singleBuffer.push("new")
        assertEquals("new", singleBuffer.peek())
        assertEquals("new", singleBuffer.pop())
        assertTrue(singleBuffer.isEmpty())
    }
    
    @Test
    fun testLargeCapacity() {
        val largeBuffer = RingBuffer<Int>(10000)
        
        for (i in 1..10000) {
            largeBuffer.push(i)
        }
        
        assertTrue(largeBuffer.isFull())
        assertEquals(1, largeBuffer.peek())
        assertEquals(10000, largeBuffer.peekLast())
        
        assertEquals(1, largeBuffer.pop())
        assertEquals(2, largeBuffer.peek())
    }
    
    // ==================== 线程安全测试 ====================
    
    @Test
    fun testThreadSafeBuffer() {
        val threadSafeBuffer = RingBuffer<Int>(100, threadSafe = true)
        val threadCount = 10
        val itemsPerThread = 100
        val latch = CountDownLatch(threadCount)
        val executor = Executors.newFixedThreadPool(threadCount)
        
        // 多线程写入
        for (t in 0 until threadCount) {
            executor.submit {
                for (i in 0 until itemsPerThread) {
                    threadSafeBuffer.push(t * itemsPerThread + i)
                }
                latch.countDown()
            }
        }
        
        latch.await(10, TimeUnit.SECONDS)
        executor.shutdown()
        
        assertEquals(threadCount * itemsPerThread, threadSafeBuffer.size)
    }
    
    @Test
    fun testConcurrentPushPop() {
        val buffer = RingBuffer<Int>(100, threadSafe = true)
        val pushCount = AtomicInteger(0)
        val popCount = AtomicInteger(0)
        val latch = CountDownLatch(2)
        val executor = Executors.newFixedThreadPool(2)
        
        // 生产者线程
        executor.submit {
            for (i in 1..1000) {
                buffer.push(i)
                pushCount.incrementAndGet()
            }
            latch.countDown()
        }
        
        // 消费者线程
        executor.submit {
            for (i in 1..1000) {
                buffer.pop()
                popCount.incrementAndGet()
            }
            latch.countDown()
        }
        
        latch.await(10, TimeUnit.SECONDS)
        executor.shutdown()
        
        // 推送和弹出操作都应该完成
        assertEquals(1000, pushCount.get())
        assertEquals(1000, popCount.get())
    }
}

class BlockingRingBufferTest {
    
    @Test
    fun testBasicOperations() {
        val buffer = BlockingRingBuffer<Int>(3)
        
        assertTrue(buffer.isEmpty())
        assertFalse(buffer.isFull())
        assertEquals(0, buffer.size)
        
        // offer 测试
        assertTrue(buffer.offer(1))
        assertTrue(buffer.offer(2))
        assertTrue(buffer.offer(3))
        assertFalse(buffer.offer(4))  // 满了
        
        assertTrue(buffer.isFull())
        assertEquals(3, buffer.size)
        
        // poll 测试
        assertEquals(1, buffer.poll())
        assertEquals(2, buffer.poll())
        assertEquals(3, buffer.poll())
        assertNull(buffer.poll())  // 空了
    }
    
    @Test
    fun testBlockingPut() {
        val buffer = BlockingRingBuffer<Int>(2)
        val latch = CountDownLatch(1)
        val executor = Executors.newSingleThreadExecutor()
        var putCompleted = false
        
        // 填满缓冲区
        buffer.offer(1)
        buffer.offer(2)
        
        // 启动一个线程尝试 put（应该阻塞）
        executor.submit {
            buffer.put(3)  // 这会阻塞直到有空间
            putCompleted = true
            latch.countDown()
        }
        
        // 等待一小段时间确保线程已经开始等待
        Thread.sleep(100)
        assertFalse(putCompleted)
        
        // 取出一个元素，put 应该可以完成
        buffer.poll()
        
        latch.await(1, TimeUnit.SECONDS)
        executor.shutdown()
        
        assertTrue(putCompleted)
        assertEquals(2, buffer.size)
    }
    
    @Test
    fun testBlockingTake() {
        val buffer = BlockingRingBuffer<Int>(2)
        val latch = CountDownLatch(1)
        val executor = Executors.newSingleThreadExecutor()
        var takenValue: Int? = null
        
        // 启动一个线程尝试 take（应该阻塞）
        executor.submit {
            takenValue = buffer.take()  // 这会阻塞直到有元素
            latch.countDown()
        }
        
        // 等待一小段时间确保线程已经开始等待
        Thread.sleep(100)
        assertNull(takenValue)
        
        // 添加一个元素，take 应该可以完成
        buffer.put(42)
        
        latch.await(1, TimeUnit.SECONDS)
        executor.shutdown()
        
        assertEquals(42, takenValue)
        assertTrue(buffer.isEmpty())
    }
}

class ExtensionFunctionsTest {
    
    @Test
    fun testToRingBuffer() {
        val list = listOf(1, 2, 3, 4, 5)
        val buffer = list.toRingBuffer()
        
        assertEquals(5, buffer.size)
        assertEquals(1, buffer.peek())
        assertEquals(5, buffer.peekLast())
    }
    
    @Test
    fun testToRingBufferWithCapacity() {
        val list = listOf(1, 2, 3, 4, 5)
        val buffer = list.toRingBuffer(capacity = 3)
        
        assertEquals(3, buffer.size)
        assertEquals(3, buffer.peek())  // 只保留最后 3 个
        assertEquals(5, buffer.peekLast())
    }
    
    @Test
    fun testEmptyRingBuffer() {
        val buffer = emptyRingBuffer<String>(10)
        
        assertTrue(buffer.isEmpty())
        assertEquals(10, buffer.capacity)
        assertEquals(0, buffer.size)
    }
    
    @Test
    fun testEmptyRingBufferThreadSafe() {
        val buffer = emptyRingBuffer<Int>(5, threadSafe = true)
        
        assertTrue(buffer.isEmpty())
        assertEquals(5, buffer.capacity)
    }
}

// 测试数据类
data class Person(val name: String, val age: Int)

class RingBufferGenericTest {
    
    @Test
    fun testStringBuffer() {
        val buffer = RingBuffer<String>(3)
        
        buffer.push("hello")
        buffer.push("world")
        buffer.push("kotlin")
        
        assertEquals("hello", buffer.pop())
        assertEquals("world", buffer.pop())
        assertEquals("kotlin", buffer.pop())
    }
    
    @Test
    fun testObjectBuffer() {
        val buffer = RingBuffer<Person>(3)
        
        buffer.push(Person("Alice", 25))
        buffer.push(Person("Bob", 30))
        buffer.push(Person("Charlie", 35))
        
        val first = buffer.pop()
        assertEquals("Alice", first?.name)
        assertEquals(25, first?.age)
        
        val found = buffer.find { it.age > 30 }
        assertEquals("Charlie", found?.name)
    }
    
    @Test
    fun testNullableBuffer() {
        val buffer = RingBuffer<Int?>(3)
        
        buffer.push(1)
        buffer.push(null)
        buffer.push(3)
        
        assertEquals(1, buffer.pop())
        assertNull(buffer.pop())
        assertEquals(3, buffer.pop())
    }
}