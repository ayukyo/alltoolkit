/**
 * Ring Buffer - 环形缓冲区工具模块
 * 
 * 一个高效的固定大小循环缓冲区实现，适用于：
 * - 日志系统（保留最近 N 条记录）
 * - 事件流处理
 * - 音频/视频缓冲
 * - 滑动窗口计算
 * - 生产者-消费者场景
 * 
 * 特点：
 * - O(1) 时间复杂度的入队、出队操作
 * - 线程安全的选项
 * - 支持泛型
 * - 支持迭代和随机访问
 * - 零外部依赖，纯 Kotlin 实现
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-04-15
 */

package ring_buffer_utils

import java.util.concurrent.atomic.AtomicInteger
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock

/**
 * 环形缓冲区主类
 * 
 * @param capacity 缓冲区容量
 * @param threadSafe 是否线程安全，默认 false
 */
class RingBuffer<T>(
    private val capacity: Int,
    private val threadSafe: Boolean = false
) : Iterable<T>, Collection<T> {
    
    // 内部存储数组
    private val buffer: Array<Any?> = arrayOfNulls(capacity)
    
    // 头指针（读取位置）
    private var head: Int = 0
    
    // 尾指针（写入位置）
    private var tail: Int = 0
    
    // 当前元素数量
    private var _size: Int = 0
    
    // 线程安全锁
    private val lock = ReentrantLock()
    
    // 原子计数器（用于线程安全模式）
    private val atomicSize = AtomicInteger(0)
    
    // 覆盖模式：当缓冲区满时，是否覆盖最老的元素
    var overwriteMode: Boolean = true
    
    init {
        require(capacity > 0) { "Capacity must be positive" }
    }
    
    /**
     * 当前缓冲区中的元素数量
     */
    override val size: Int
        get() = if (threadSafe) atomicSize.get() else _size
    
    /**
     * 缓冲区是否为空
     */
    override fun isEmpty(): Boolean = size == 0
    
    /**
     * 缓冲区是否已满
     */
    fun isFull(): Boolean = size == capacity
    
    /**
     * 剩余可用空间
     */
    fun available(): Int = capacity - size
    
    /**
     * 向缓冲区添加元素
     * 
     * @param element 要添加的元素
     * @return true 如果成功添加，false 如果缓冲区已满且 overwriteMode=false
     */
    fun push(element: T): Boolean {
        return if (threadSafe) {
            lock.withLock {
                pushInternal(element)
            }
        } else {
            pushInternal(element)
        }
    }
    
    private fun pushInternal(element: T): Boolean {
        if (isFull() && !overwriteMode) {
            return false
        }
        
        if (isFull()) {
            // 覆盖模式：移动头指针，丢弃最老的元素
            head = (head + 1) % capacity
        } else {
            _size++
            atomicSize.incrementAndGet()
        }
        
        buffer[tail] = element
        tail = (tail + 1) % capacity
        return true
    }
    
    /**
     * 批量添加元素
     * 
     * @param elements 要添加的元素集合
     * @return 成功添加的元素数量
     */
    fun pushAll(elements: Collection<T>): Int {
        return if (threadSafe) {
            lock.withLock {
                var count = 0
                for (element in elements) {
                    if (pushInternal(element)) count++
                }
                count
            }
        } else {
            var count = 0
            for (element in elements) {
                if (pushInternal(element)) count++
            }
            count
        }
    }
    
    /**
     * 从缓冲区取出最老的元素（FIFO）
     * 
     * @return 最老的元素，如果缓冲区为空则返回 null
     */
    fun pop(): T? {
        return if (threadSafe) {
            lock.withLock {
                popInternal()
            }
        } else {
            popInternal()
        }
    }
    
    @Suppress("UNCHECKED_CAST")
    private fun popInternal(): T? {
        if (isEmpty()) return null
        
        val element = buffer[head] as T
        buffer[head] = null // 帮助 GC
        head = (head + 1) % capacity
        _size--
        atomicSize.decrementAndGet()
        return element
    }
    
    /**
     * 查看最老的元素但不移除
     * 
     * @return 最老的元素，如果缓冲区为空则返回 null
     */
    @Suppress("UNCHECKED_CAST")
    fun peek(): T? {
        return if (threadSafe) {
            lock.withLock {
                if (isEmpty()) null else buffer[head] as T
            }
        } else {
            if (isEmpty()) null else buffer[head] as T
        }
    }
    
    /**
     * 查看最新的元素但不移除
     * 
     * @return 最新的元素，如果缓冲区为空则返回 null
     */
    @Suppress("UNCHECKED_CAST")
    fun peekLast(): T? {
        return if (threadSafe) {
            lock.withLock {
                if (isEmpty()) null else buffer[(tail - 1 + capacity) % capacity] as T
            }
        } else {
            if (isEmpty()) null else buffer[(tail - 1 + capacity) % capacity] as T
        }
    }
    
    /**
     * 获取指定索引的元素（相对于最老元素的位置）
     * 
     * @param index 索引，0 表示最老的元素
     * @return 对应位置的元素
     * @throws IndexOutOfBoundsException 如果索引超出范围
     */
    @Suppress("UNCHECKED_CAST")
    operator fun get(index: Int): T {
        if (index < 0 || index >= size) {
            throw IndexOutOfBoundsException("Index: $index, Size: $size")
        }
        
        return if (threadSafe) {
            lock.withLock {
                buffer[(head + index) % capacity] as T
            }
        } else {
            buffer[(head + index) % capacity] as T
        }
    }
    
    /**
     * 清空缓冲区
     */
    fun clear() {
        if (threadSafe) {
            lock.withLock {
                clearInternal()
            }
        } else {
            clearInternal()
        }
    }
    
    private fun clearInternal() {
        for (i in buffer.indices) {
            buffer[i] = null
        }
        head = 0
        tail = 0
        _size = 0
        atomicSize.set(0)
    }
    
    /**
     * 转换为列表（按插入顺序）
     */
    fun toList(): List<T> {
        return if (threadSafe) {
            lock.withLock {
                toListInternal()
            }
        } else {
            toListInternal()
        }
    }
    
    @Suppress("UNCHECKED_CAST")
    private fun toListInternal(): List<T> {
        val result = mutableListOf<T>()
        for (i in 0 until size) {
            result.add(buffer[(head + i) % capacity] as T)
        }
        return result
    }
    
    /**
     * 转换为数组
     */
    fun toArray(): Array<Any?> {
        return toList().toTypedArray()
    }
    
    /**
     * 检查是否包含指定元素
     */
    override fun contains(element: T): Boolean {
        return if (threadSafe) {
            lock.withLock {
                containsInternal(element)
            }
        } else {
            containsInternal(element)
        }
    }
    
    private fun containsInternal(element: T): Boolean {
        for (i in 0 until size) {
            @Suppress("UNCHECKED_CAST")
            if (buffer[(head + i) % capacity] == element) {
                return true
            }
        }
        return false
    }
    
    /**
     * 检查是否包含集合中的所有元素
     */
    override fun containsAll(elements: Collection<T>): Boolean {
        return elements.all { contains(it) }
    }
    
    /**
     * 返回迭代器
     */
    override fun iterator(): Iterator<T> {
        return RingBufferIterator()
    }
    
    /**
     * 反向迭代器（从最新到最老）
     */
    fun reversedIterator(): Iterator<T> {
        return ReversedRingBufferIterator()
    }
    
    /**
     * 获取最近 N 个元素
     */
    fun takeLast(n: Int): List<T> {
        val actualN = minOf(n, size)
        return if (threadSafe) {
            lock.withLock {
                val result = mutableListOf<T>()
                val startIndex = size - actualN
                for (i in startIndex until size) {
                    @Suppress("UNCHECKED_CAST")
                    result.add(buffer[(head + i) % capacity] as T)
                }
                result
            }
        } else {
            val result = mutableListOf<T>()
            val startIndex = size - actualN
            for (i in startIndex until size) {
                @Suppress("UNCHECKED_CAST")
                result.add(buffer[(head + i) % capacity] as T)
            }
            result
        }
    }
    
    /**
     * 获取最早 N 个元素
     */
    fun takeFirst(n: Int): List<T> {
        val actualN = minOf(n, size)
        return if (threadSafe) {
            lock.withLock {
                val result = mutableListOf<T>()
                for (i in 0 until actualN) {
                    @Suppress("UNCHECKED_CAST")
                    result.add(buffer[(head + i) % capacity] as T)
                }
                result
            }
        } else {
            val result = mutableListOf<T>()
            for (i in 0 until actualN) {
                @Suppress("UNCHECKED_CAST")
                result.add(buffer[(head + i) % capacity] as T)
            }
            result
        }
    }
    
    /**
     * 查找满足条件的第一个元素
     */
    fun find(predicate: (T) -> Boolean): T? {
        return if (threadSafe) {
            lock.withLock {
                findInternal(predicate)
            }
        } else {
            findInternal(predicate)
        }
    }
    
    @Suppress("UNCHECKED_CAST")
    private fun findInternal(predicate: (T) -> Boolean): T? {
        for (i in 0 until size) {
            val element = buffer[(head + i) % capacity] as T
            if (predicate(element)) return element
        }
        return null
    }
    
    /**
     * 过滤满足条件的所有元素
     */
    fun filter(predicate: (T) -> Boolean): List<T> {
        return if (threadSafe) {
            lock.withLock {
                filterInternal(predicate)
            }
        } else {
            filterInternal(predicate)
        }
    }
    
    @Suppress("UNCHECKED_CAST")
    private fun filterInternal(predicate: (T) -> Boolean): List<T> {
        val result = mutableListOf<T>()
        for (i in 0 until size) {
            val element = buffer[(head + i) % capacity] as T
            if (predicate(element)) result.add(element)
        }
        return result
    }
    
    /**
     * 对每个元素执行操作
     */
    fun forEach(action: (T) -> Unit) {
        if (threadSafe) {
            lock.withLock {
                forEachInternal(action)
            }
        } else {
            forEachInternal(action)
        }
    }
    
    @Suppress("UNCHECKED_CAST")
    private fun forEachInternal(action: (T) -> Unit) {
        for (i in 0 until size) {
            action(buffer[(head + i) % capacity] as T)
        }
    }
    
    // 内部迭代器类
    private inner class RingBufferIterator : Iterator<T> {
        private var currentIndex = 0
        
        override fun hasNext(): Boolean = currentIndex < size
        
        @Suppress("UNCHECKED_CAST")
        override fun next(): T {
            if (!hasNext()) throw NoSuchElementException()
            val element = buffer[(head + currentIndex) % capacity] as T
            currentIndex++
            return element
        }
    }
    
    // 反向迭代器类
    private inner class ReversedRingBufferIterator : Iterator<T> {
        private var currentIndex = size - 1
        
        override fun hasNext(): Boolean = currentIndex >= 0
        
        @Suppress("UNCHECKED_CAST")
        override fun next(): T {
            if (!hasNext()) throw NoSuchElementException()
            val element = buffer[(head + currentIndex) % capacity] as T
            currentIndex--
            return element
        }
    }
    
    override fun toString(): String {
        return "RingBuffer(capacity=$capacity, size=$size, elements=${toList()})"
    }
}

/**
 * 线程安全的阻塞环形缓冲区
 * 
 * 当缓冲区为空时，take 操作会阻塞等待
 * 当缓冲区满时，put 操作会阻塞等待
 * 
 * @param capacity 缓冲区容量
 */
class BlockingRingBuffer<T>(private val capacity: Int) {
    
    private val buffer = RingBuffer<T>(capacity, threadSafe = false)
    private val lock = ReentrantLock()
    private val notEmpty = lock.newCondition()
    private val notFull = lock.newCondition()
    
    /**
     * 向缓冲区添加元素（如果已满则阻塞等待）
     */
    fun put(element: T) {
        lock.withLock {
            while (buffer.isFull()) {
                notFull.await()
            }
            buffer.push(element)
            notEmpty.signal()
        }
    }
    
    /**
     * 从缓冲区取出元素（如果为空则阻塞等待）
     */
    fun take(): T {
        lock.withLock {
            while (buffer.isEmpty()) {
                notEmpty.await()
            }
            val element = buffer.pop()!!
            notFull.signal()
            return element
        }
    }
    
    /**
     * 尝试添加元素（立即返回）
     * @return true 如果成功添加，false 如果缓冲区已满
     */
    fun offer(element: T): Boolean {
        return lock.withLock {
            if (buffer.isFull()) {
                false
            } else {
                buffer.push(element)
                notEmpty.signal()
                true
            }
        }
    }
    
    /**
     * 尝试取出元素（立即返回）
     * @return 元素，如果为空则返回 null
     */
    fun poll(): T? {
        return lock.withLock {
            if (buffer.isEmpty()) {
                null
            } else {
                val element = buffer.pop()
                notFull.signal()
                element
            }
        }
    }
    
    /**
     * 当前大小
     */
    val size: Int
        get() = lock.withLock { buffer.size }
    
    /**
     * 是否为空
     */
    fun isEmpty(): Boolean = size == 0
    
    /**
     * 是否已满
     */
    fun isFull(): Boolean = size == capacity
}

/**
 * 扩展函数：从列表创建环形缓冲区
 */
fun <T> List<T>.toRingBuffer(capacity: Int = this.size, threadSafe: Boolean = false): RingBuffer<T> {
    val ringBuffer = RingBuffer<T>(capacity, threadSafe)
    ringBuffer.pushAll(this)
    return ringBuffer
}

/**
 * 扩展函数：创建指定容量的空环形缓冲区
 */
fun <T> emptyRingBuffer(capacity: Int, threadSafe: Boolean = false): RingBuffer<T> {
    return RingBuffer(capacity, threadSafe)
}