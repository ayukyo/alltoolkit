/**
 * AllToolkit - Kotlin Queue Utilities
 * 
 * 零依赖的队列工具模块，仅使用 Kotlin/Java 标准库
 * 支持：线程安全队列、阻塞操作、优先级队列、循环队列、双端队列
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

package queue_utils

import java.util.concurrent.TimeUnit
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock
import kotlin.math.min

/**
 * 普通队列接口
 */
interface Queue<T> {
    val size: Int
    val isEmpty: Boolean
    val isNotEmpty: Boolean get() = !isEmpty
    
    fun enqueue(item: T): Boolean
    fun dequeue(): T?
    fun peek(): T?
    fun clear()
    fun toList(): List<T>
}

/**
 * 阻塞队列接口
 */
interface BlockingQueue<T> : Queue<T> {
    fun put(item: T)
    fun take(): T
    fun offer(item: T, timeoutMs: Long): Boolean
    fun poll(timeoutMs: Long): T?
    fun remainingCapacity(): Int
}

/**
 * 优先级队列接口
 */
interface PriorityQueue<T> : Queue<T> {
    fun enqueue(item: T, priority: Int): Boolean
    fun peekWithPriority(): Pair<T, Int>?
}

/**
 * 双端队列接口
 */
interface Deque<T> : Queue<T> {
    fun addFirst(item: T)
    fun addLast(item: T)
    fun removeFirst(): T?
    fun removeLast(): T?
    fun peekFirst(): T?
    fun peekLast(): T?
}

/**
 * 循环队列实现
 * 固定容量的环形缓冲区队列
 */
class CircularQueue<T>(
    private val capacity: Int
) : Queue<T> {
    
    init {
        require(capacity > 0) { "Capacity must be positive" }
    }
    
    private val buffer = arrayOfNulls<Any?>(capacity)
    private var head = 0
    private var tail = 0
    private var count = 0
    
    override val size: Int get() = count
    override val isEmpty: Boolean get() = count == 0
    
    override fun enqueue(item: T): Boolean {
        if (count >= capacity) return false
        buffer[tail] = item
        tail = (tail + 1) % capacity
        count++
        return true
    }
    
    override fun dequeue(): T? {
        if (count == 0) return null
        @Suppress("UNCHECKED_CAST")
        val item = buffer[head] as T
        buffer[head] = null
        head = (head + 1) % capacity
        count--
        return item
    }
    
    override fun peek(): T? {
        if (count == 0) return null
        @Suppress("UNCHECKED_CAST")
        return buffer[head] as T
    }
    
    override fun clear() {
        for (i in 0 until capacity) buffer[i] = null
        head = 0
        tail = 0
        count = 0
    }
    
    override fun toList(): List<T> {
        val result = mutableListOf<T>()
        for (i in 0 until count) {
            val idx = (head + i) % capacity
            @Suppress("UNCHECKED_CAST")
            result.add(buffer[idx] as T)
        }
        return result
    }
    
    fun isFull(): Boolean = count == capacity
    fun available(): Int = capacity - count
}

/**
 * 线程安全的阻塞队列实现
 * 支持超时操作和生产者-消费者模式
 */
class ThreadSafeQueue<T>(
    private val capacity: Int = Int.MAX_VALUE
) : BlockingQueue<T> {
    
    private val lock = ReentrantLock()
    private val notEmpty = lock.newCondition()
    private val notFull = lock.newCondition()
    
    private val queue = ArrayDeque<T>()
    
    override val size: Int
        get() = lock.withLock { queue.size }
    
    override val isEmpty: Boolean
        get() = lock.withLock { queue.isEmpty() }
    
    override fun enqueue(item: T): Boolean {
        return lock.withLock {
            if (queue.size >= capacity) return false
            queue.addLast(item)
            notEmpty.signal()
            true
        }
    }
    
    override fun dequeue(): T? {
        return lock.withLock { queue.pollFirst() }
    }
    
    override fun peek(): T? {
        return lock.withLock { queue.firstOrNull() }
    }
    
    override fun clear() {
        lock.withLock {
            queue.clear()
            notFull.signalAll()
        }
    }
    
    override fun toList(): List<T> {
        return lock.withLock { queue.toList() }
    }
    
    override fun put(item: T) {
        lock.withLock {
            while (queue.size >= capacity) {
                notFull.await()
            }
            queue.addLast(item)
            notEmpty.signal()
        }
    }
    
    override fun take(): T {
        lock.withLock {
            while (queue.isEmpty()) {
                notEmpty.await()
            }
            val item = queue.removeFirst()
            notFull.signal()
            return item
        }
    }
    
    override fun offer(item: T, timeoutMs: Long): Boolean {
        lock.withLock {
            var remainingNanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs)
            while (queue.size >= capacity) {
                if (remainingNanos <= 0) return false
                remainingNanos = notFull.awaitNanos(remainingNanos)
            }
            queue.addLast(item)
            notEmpty.signal()
            return true
        }
    }
    
    override fun poll(timeoutMs: Long): T? {
        lock.withLock {
            var remainingNanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs)
            while (queue.isEmpty()) {
                if (remainingNanos <= 0) return null
                remainingNanos = notEmpty.awaitNanos(remainingNanos)
            }
            val item = queue.removeFirst()
            notFull.signal()
            return item
        }
    }
    
    override fun remainingCapacity(): Int {
        return lock.withLock { capacity - queue.size }
    }
    
    fun drainTo(collection: MutableCollection<T>, maxElements: Int = Int.MAX_VALUE): Int {
        return lock.withLock {
            val count = min(min(maxElements, queue.size), collection.remainingCapacity())
            repeat(count) {
                queue.pollFirst()?.let { collection.add(it) }
            }
            notFull.signalAll()
            count
        }
    }
}

/**
 * 优先级队列实现
 * 高优先级元素先出队（数值越小优先级越高）
 */
class PriorityAwareQueue<T>(
    private val capacity: Int = Int.MAX_VALUE
) : PriorityQueue<T> {
    
    private data class PriorityItem<T>(val item: T, val priority: Int)
    
    private val items = mutableListOf<PriorityItem<T>>()
    
    override val size: Int get() = items.size
    override val isEmpty: Boolean get() = items.isEmpty()
    
    override fun enqueue(item: T): Boolean = enqueue(item, 0)
    
    override fun enqueue(item: T, priority: Int): Boolean {
        if (items.size >= capacity) return false
        val newItem = PriorityItem(item, priority)
        var index = items.size
        // 使用二分查找找到插入位置
        var low = 0
        var high = items.size - 1
        while (low <= high) {
            val mid = (low + high) / 2
            if (items[mid].priority <= priority) {
                low = mid + 1
            } else {
                high = mid - 1
            }
        }
        items.add(low, newItem)
        return true
    }
    
    override fun dequeue(): T? {
        if (items.isEmpty()) return null
        return items.removeAt(0).item
    }
    
    override fun peek(): T? {
        return items.firstOrNull()?.item
    }
    
    override fun peekWithPriority(): Pair<T, Int>? {
        return items.firstOrNull()?.let { it.item to it.priority }
    }
    
    override fun clear() {
        items.clear()
    }
    
    override fun toList(): List<T> = items.map { it.item }
    
    fun toListWithPriority(): List<Pair<T, Int>> = items.map { it.item to it.priority }
}

/**
 * 双端队列实现
 * 支持头部和尾部的添加/删除操作
 */
class ArrayDequeImpl<T> : Deque<T> {
    
    private val deque = ArrayDeque<T>()
    
    override val size: Int get() = deque.size
    override val isEmpty: Boolean get() = deque.isEmpty()
    
    override fun enqueue(item: T): Boolean {
        deque.addLast(item)
        return true
    }
    
    override fun dequeue(): T? = removeFirst()
    
    override fun peek(): T? = peekFirst()
    
    override fun clear() = deque.clear()
    
    override fun toList(): List<T> = deque.toList()
    
    override fun addFirst(item: T) {
        deque.addFirst(item)
    }
    
    override fun addLast(item: T) {
        deque.addLast(item)
    }
    
    override fun removeFirst(): T? = deque.pollFirst()
    
    override fun removeLast(): T? = deque.pollLast()
    
    override fun peekFirst(): T? = deque.firstOrNull()
    
    override fun peekLast(): T? = deque.lastOrNull()
    
    fun rotate(n: Int) {
        if (deque.isEmpty() || n == 0) return
        val steps = n % deque.size
        repeat(if (steps > 0) steps else deque.size + steps) {
            deque.addFirst(deque.removeLast())
        }
    }
}

/**
 * 延迟队列元素接口
 */
interface Delayed : Comparable<Delayed> {
    fun getDelay(unit: TimeUnit): Long
}

/**
 * 延迟队列实现
 * 元素只有在延迟到期后才能被取出
 */
class DelayQueue<T : Delayed> {
    
    private val lock = ReentrantLock()
    private val available = lock.newCondition()
    private val queue = java.util.PriorityQueue<T>()
    
    val size: Int get() = lock.withLock { queue.size }
    val isEmpty: Boolean get() = lock.withLock { queue.isEmpty() }
    
    fun put(item: T) {
        lock.withLock {
            queue.offer(item)
            if (item == queue.peek()) {
                available.signalAll()
            }
        }
    }
    
    fun take(): T {
        lock.withLock {
            while (true) {
                val first = queue.peek() ?: run {
                    available.await()
                    continue
                }
                
                val delay = first.getDelay(TimeUnit.NANOSECONDS)
                if (delay <= 0) {
                    return queue.poll()
                }
                
                available.awaitNanos(delay)
            }
        }
    }
    
    fun poll(timeoutMs: Long): T? {
        lock.withLock {
            var remainingNanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs)
            
            while (true) {
                val first = queue.peek() ?: return null
                val delay = first.getDelay(TimeUnit.NANOSECONDS)
                
                if (delay <= 0) {
                    return queue.poll()
                }
                
                if (remainingNanos <= 0) {
                    return null
                }
                
                remainingNanos = available.awaitNanos(min(delay, remainingNanos))
            }
        }
    }
    
    fun peek(): T? = lock.withLock { queue.peek() }
    
    fun clear() = lock.withLock { queue.clear() }
    
    fun toList(): List<T> = lock.withLock { queue.toList() }
}

/**
 * 队列工具函数
 */
object QueueUtils {
    
    /**
     * 创建循环队列
     */
    fun <T> circular(capacity: Int): CircularQueue<T> = CircularQueue(capacity)
    
    /**
     * 创建线程安全队列
     */
    fun <T> threadSafe(capacity: Int = Int.MAX_VALUE): ThreadSafeQueue<T> = ThreadSafeQueue(capacity)
    
    /**
     * 创建优先级队列
     */
    fun <T> priority(capacity: Int = Int.MAX_VALUE): PriorityAwareQueue<T> = PriorityAwareQueue(capacity)
    
    /**
     * 创建双端队列
     */
    fun <T> deque(): ArrayDequeImpl<T> = ArrayDequeImpl()
    
    /**
     * 批量入队
     */
    fun <T> enqueueAll(queue: Queue<T>, items: Collection<T>): Int {
        var count = 0
        for (item in items) {
            if (queue.enqueue(item)) count++
            else break
        }
        return count
    }
    
    /**
     * 批量出队
     */
    fun <T> dequeueAll(queue: Queue<T>): List<T> {
        val result = mutableListOf<T>()
        while (queue.isNotEmpty) {
            queue.dequeue()?.let { result.add(it) }
        }
        return result
    }
    
    /**
     * 出队指定数量
     */
    fun <T> dequeueN(queue: Queue<T>, n: Int): List<T> {
        val result = mutableListOf<T>()
        repeat(n) {
            queue.dequeue()?.let { result.add(it) } ?: return@repeat
        }
        return result
    }
    
    /**
     * 查找元素
     */
    fun <T> contains(queue: Queue<T>, item: T): Boolean {
        return queue.toList().contains(item)
    }
    
    /**
     * 查找满足条件的元素
     */
    fun <T> find(queue: Queue<T>, predicate: (T) -> Boolean): T? {
        return queue.toList().find(predicate)
    }
    
    /**
     * 过滤元素
     */
    fun <T> filter(queue: Queue<T>, predicate: (T) -> Boolean): List<T> {
        return queue.toList().filter(predicate)
    }
    
    /**
     * 转换元素
     */
    fun <T, R> map(queue: Queue<T>, transform: (T) -> R): List<R> {
        return queue.toList().map(transform)
    }
    
    /**
     * 反转队列
     */
    fun <T> reverse(queue: Queue<T>): List<T> {
        return queue.toList().reversed()
    }
    
    /**
     * 队列归约
     */
    fun <T, R> reduce(queue: Queue<T>, initial: R, operation: (R, T) -> R): R {
        return queue.toList().fold(initial, operation)
    }
    
    /**
     * 检查所有元素满足条件
     */
    fun <T> all(queue: Queue<T>, predicate: (T) -> Boolean): Boolean {
        return queue.toList().all(predicate)
    }
    
    /**
     * 检查存在元素满足条件
     */
    fun <T> any(queue: Queue<T>, predicate: (T) -> Boolean): Boolean {
        return queue.toList().any(predicate)
    }
    
    /**
     * 合并两个队列
     */
    fun <T> merge(q1: Queue<T>, q2: Queue<T>): List<T> {
        return q1.toList() + q2.toList()
    }
    
    /**
     * 队列分区
     */
    fun <T> partition(queue: Queue<T>, predicate: (T) -> Boolean): Pair<List<T>, List<T>> {
        return queue.toList().partition(predicate)
    }
    
    /**
     * 去重
     */
    fun <T> distinct(queue: Queue<T>): List<T> {
        return queue.toList().distinct()
    }
    
    /**
     * 分组
     */
    inline fun <T, K> groupBy(queue: Queue<T>, crossinline keySelector: (T) -> K): Map<K, List<T>> {
        return queue.toList().groupBy(keySelector)
    }
    
    /**
     * 统计元素出现次数
     */
    fun <T> countOccurrences(queue: Queue<T>): Map<T, Int> {
        return queue.toList().groupingBy { it }.eachCount()
    }
}

/**
 * 延时任务实现示例
 */
class DelayedTask(
    private val task: () -> Unit,
    private val executeTimeNanos: Long
) : Delayed {
    
    constructor(task: () -> Unit, delayMs: Long) : this(
        task,
        System.nanoTime() + TimeUnit.MILLISECONDS.toNanos(delayMs)
    )
    
    override fun getDelay(unit: TimeUnit): Long {
        val remaining = executeTimeNanos - System.nanoTime()
        return unit.convert(remaining, TimeUnit.NANOSECONDS)
    }
    
    override fun compareTo(other: Delayed): Int {
        return (executeTimeNanos - (other as DelayedTask).executeTimeNanos).toInt()
    }
    
    fun execute() = task()
}