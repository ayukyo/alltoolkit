/**
 * Bloom Filter - 布隆过滤器工具模块
 * 
 * 一个空间效率高的概率数据结构，用于判断元素是否在集合中。
 * 特点：
 * - 可能存在假阳性（报告存在但实际不存在）
 * - 不存在假阴性（报告不存在就一定不存在）
 * - 空间效率极高，相比哈希集合可节省90%以上空间
 * 
 * 零外部依赖，纯Kotlin实现
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-04-13
 */

package bloom_filter_utils

import kotlin.math.ceil
import kotlin.math.ln
import kotlin.math.pow

/**
 * 布隆过滤器主类
 * 
 * @param expectedInsertions 预期插入元素数量
 * @param fpp 可接受的假阳性概率 (false positive probability)，默认0.03
 */
class BloomFilter<T>(
    private val expectedInsertions: Int,
    private val fpp: Double = 0.03
) {
    // 位数组大小
    private val bitSize: Int
    
    // 哈希函数数量
    private val hashCount: Int
    
    // 位数组 (使用Long数组实现，每个Long存储64位)
    private val bits: LongArray
    
    // 当前插入元素计数
    private var insertedCount: Int = 0
    
    init {
        require(expectedInsertions > 0) { "预期插入数量必须大于0" }
        require(fpp > 0 && fpp < 1) { "假阳性概率必须在(0, 1)之间" }
        
        // 计算最优参数
        // m = -n*ln(p) / (ln(2)^2)
        // k = m/n * ln(2)
        bitSize = optimalBitSize(expectedInsertions, fpp)
        hashCount = optimalHashCount(bitSize, expectedInsertions)
        
        // 初始化位数组
        val longArraySize = ceil(bitSize.toDouble() / 64).toInt()
        bits = LongArray(longArraySize)
    }
    
    /**
     * 计算最优位数组大小
     */
    private fun optimalBitSize(n: Int, p: Double): Int {
        return ceil(-n * ln(p) / (ln(2.0).pow(2))).toInt()
    }
    
    /**
     * 计算最优哈希函数数量
     */
    private fun optimalHashCount(m: Int, n: Int): Int {
        return maxOf(1, (m.toDouble() / n * ln(2.0)).toInt())
    }
    
    /**
     * 向布隆过滤器添加元素
     * 
     * @param element 要添加的元素
     */
    fun add(element: T) {
        val hashValues = hash(element)
        for (hash in hashValues) {
            setBit(hash)
        }
        insertedCount++
    }
    
    /**
     * 批量添加元素
     * 
     * @param elements 要添加的元素集合
     */
    fun addAll(elements: Collection<T>) {
        elements.forEach { add(it) }
    }
    
    /**
     * 检查元素是否可能在集合中
     * 
     * @param element 要检查的元素
     * @return true表示元素可能存在（可能有假阳性），false表示元素一定不存在
     */
    fun mightContain(element: T): Boolean {
        val hashValues = hash(element)
        return hashValues.all { getBit(it) }
    }
    
    /**
     * 检查元素是否一定不在集合中
     * 
     * @param element 要检查的元素
     * @return true表示元素一定不存在，false表示元素可能存在
     */
    fun definitelyNotContains(element: T): Boolean {
        return !mightContain(element)
    }
    
    /**
     * 获取当前假阳性概率的估计值
     */
    fun estimateFpp(): Double {
        if (insertedCount == 0) return 0.0
        
        // fpp ≈ (1 - e^(-kn/m))^k
        val k = hashCount.toDouble()
        val n = insertedCount.toDouble()
        val m = bitSize.toDouble()
        
        val exponent = -k * n / m
        return (1 - kotlin.math.exp(exponent)).pow(k)
    }
    
    /**
     * 清空布隆过滤器
     */
    fun clear() {
        bits.fill(0)
        insertedCount = 0
    }
    
    /**
     * 检查布隆过滤器是否为空
     */
    fun isEmpty(): Boolean = insertedCount == 0
    
    /**
     * 获取已插入元素数量
     */
    fun size(): Int = insertedCount
    
    /**
     * 获取位数组大小
     */
    fun bitArraySize(): Int = bitSize
    
    /**
     * 获取哈希函数数量
     */
    fun hashFunctionCount(): Int = hashCount
    
    /**
     * 获取内存使用量（字节）
     */
    fun memoryUsage(): Long = bits.size * 8L
    
    /**
     * 计算元素哈希值数组
     * 使用双重哈希技术生成多个哈希值
     */
    private fun hash(element: T): IntArray {
        val result = IntArray(hashCount)
        val elementHash = element.hashCode()
        val elementHash2 = elementHash.ushr(16)
        
        for (i in 0 until hashCount) {
            // 双重哈希: h(i) = h1 + i * h2
            var combinedHash = elementHash + i * elementHash2
            // 确保为正数
            combinedHash = combinedHash and Int.MAX_VALUE
            result[i] = combinedHash % bitSize
        }
        return result
    }
    
    /**
     * 设置位
     */
    private fun setBit(index: Int) {
        val arrayIndex = index / 64
        val bitIndex = index % 64
        bits[arrayIndex] = bits[arrayIndex] or (1L shl bitIndex)
    }
    
    /**
     * 获取位状态
     */
    private fun getBit(index: Int): Boolean {
        val arrayIndex = index / 64
        val bitIndex = index % 64
        return (bits[arrayIndex] and (1L shl bitIndex)) != 0L
    }
    
    /**
     * 序列化为字节数组
     */
    fun toByteArray(): ByteArray {
        val output = mutableListOf<Byte>()
        
        // 写入元数据
        output.addAll(intToBytes(expectedInsertions))
        output.addAll(intToBytes(bitSize))
        output.addAll(intToBytes(hashCount))
        output.addAll(intToBytes(insertedCount))
        
        // 写入位数组
        for (longVal in bits) {
            output.addAll(longToBytes(longVal))
        }
        
        return output.toByteArray()
    }
    
    /**
     * 从字节数组反序列化
     */
    companion object {
        fun <T> fromByteArray(data: ByteArray): BloomFilter<T> {
            var offset = 0
            
            // 读取元数据
            val expectedInsertions = bytesToInt(data, offset)
            offset += 4
            
            val bitSize = bytesToInt(data, offset)
            offset += 4
            
            val hashCount = bytesToInt(data, offset)
            offset += 4
            
            val insertedCount = bytesToInt(data, offset)
            offset += 4
            
            // 创建过滤器
            val filter = BloomFilter<T>(expectedInsertions, 0.03)
            filter.insertedCount = insertedCount
            
            // 读取位数组
            val longArraySize = ceil(bitSize.toDouble() / 64).toInt()
            for (i in 0 until longArraySize) {
                filter.bits[i] = bytesToLong(data, offset)
                offset += 8
            }
            
            return filter
        }
        
        private fun intToBytes(value: Int): List<Byte> {
            return listOf(
                (value shr 24).toByte(),
                (value shr 16).toByte(),
                (value shr 8).toByte(),
                value.toByte()
            )
        }
        
        private fun bytesToInt(data: ByteArray, offset: Int): Int {
            return ((data[offset].toInt() and 0xFF) shl 24) or
                   ((data[offset + 1].toInt() and 0xFF) shl 16) or
                   ((data[offset + 2].toInt() and 0xFF) shl 8) or
                   (data[offset + 3].toInt() and 0xFF)
        }
        
        private fun longToBytes(value: Long): List<Byte> {
            return listOf(
                (value shr 56).toByte(),
                (value shr 48).toByte(),
                (value shr 40).toByte(),
                (value shr 32).toByte(),
                (value shr 24).toByte(),
                (value shr 16).toByte(),
                (value shr 8).toByte(),
                value.toByte()
            )
        }
        
        private fun bytesToLong(data: ByteArray, offset: Int): Long {
            return ((data[offset].toLong() and 0xFF) shl 56) or
                   ((data[offset + 1].toLong() and 0xFF) shl 48) or
                   ((data[offset + 2].toLong() and 0xFF) shl 40) or
                   ((data[offset + 3].toLong() and 0xFF) shl 32) or
                   ((data[offset + 4].toLong() and 0xFF) shl 24) or
                   ((data[offset + 5].toLong() and 0xFF) shl 16) or
                   ((data[offset + 6].toLong() and 0xFF) shl 8) or
                   (data[offset + 7].toLong() and 0xFF)
        }
    }
    
    override fun toString(): String {
        return "BloomFilter(inserted=$insertedCount, bitSize=$bitSize, hashCount=$hashCount, estimatedFpp=${String.format("%.6f", estimateFpp())})"
    }
}

/**
 * 可扩展布隆过滤器
 * 当元素数量超过预期时自动扩展，保持假阳性概率稳定
 */
class ScalableBloomFilter<T>(
    private val initialCapacity: Int = 1000,
    private val fpp: Double = 0.03,
    private val growthFactor: Int = 2
) {
    private val filters = mutableListOf<BloomFilter<T>>()
    private var currentFilter: BloomFilter<T> = BloomFilter(initialCapacity, fpp)
    
    init {
        filters.add(currentFilter)
    }
    
    fun add(element: T) {
        if (currentFilter.size() >= currentFilter.expectedInsertions) {
            // 扩展: 创建新过滤器
            val newCapacity = currentFilter.expectedInsertions * growthFactor
            currentFilter = BloomFilter(newCapacity, fpp / filters.size.coerceAtLeast(1))
            filters.add(currentFilter)
        }
        currentFilter.add(element)
    }
    
    fun addAll(elements: Collection<T>) {
        elements.forEach { add(it) }
    }
    
    fun mightContain(element: T): Boolean {
        return filters.any { it.mightContain(element) }
    }
    
    fun definitelyNotContains(element: T): Boolean = !mightContain(element)
    
    fun size(): Int = filters.sumOf { it.size() }
    
    fun filterCount(): Int = filters.size
    
    fun memoryUsage(): Long = filters.sumOf { it.memoryUsage() }
    
    fun clear() {
        filters.clear()
        currentFilter = BloomFilter(initialCapacity, fpp)
        filters.add(currentFilter)
    }
    
    override fun toString(): String {
        return "ScalableBloomFilter(filters=${filters.size}, totalSize=${size()}, memory=${memoryUsage()} bytes)"
    }
}

/**
 * 计数布隆过滤器
 * 支持删除操作，但使用更多内存
 */
class CountingBloomFilter<T>(
    private val expectedInsertions: Int,
    private val fpp: Double = 0.03,
    private val maxCount: Int = 15 // 每个位的最大计数
) {
    private val bitSize: Int
    private val hashCount: Int
    private val counts: IntArray
    private var insertedCount: Int = 0
    
    init {
        require(expectedInsertions > 0) { "预期插入数量必须大于0" }
        require(fpp > 0 && fpp < 1) { "假阳性概率必须在(0, 1)之间" }
        
        bitSize = ceil(-expectedInsertions * ln(fpp) / (ln(2.0).pow(2))).toInt()
        hashCount = maxOf(1, (bitSize.toDouble() / expectedInsertions * ln(2.0)).toInt())
        counts = IntArray(bitSize)
    }
    
    fun add(element: T) {
        val hashValues = hash(element)
        for (hash in hashValues) {
            if (counts[hash] < maxCount) {
                counts[hash]++
            }
        }
        insertedCount++
    }
    
    fun remove(element: T): Boolean {
        if (!mightContain(element)) return false
        
        val hashValues = hash(element)
        for (hash in hashValues) {
            if (counts[hash] > 0) {
                counts[hash]--
            }
        }
        insertedCount--
        return true
    }
    
    fun mightContain(element: T): Boolean {
        val hashValues = hash(element)
        return hashValues.all { counts[it] > 0 }
    }
    
    fun definitelyNotContains(element: T): Boolean = !mightContain(element)
    
    fun size(): Int = insertedCount
    
    fun clear() {
        counts.fill(0)
        insertedCount = 0
    }
    
    private fun hash(element: T): IntArray {
        val result = IntArray(hashCount)
        val elementHash = element.hashCode()
        val elementHash2 = elementHash.ushr(16)
        
        for (i in 0 until hashCount) {
            var combinedHash = elementHash + i * elementHash2
            combinedHash = combinedHash and Int.MAX_VALUE
            result[i] = combinedHash % bitSize
        }
        return result
    }
    
    override fun toString(): String {
        return "CountingBloomFilter(inserted=$insertedCount, bitSize=$bitSize, hashCount=$hashCount)"
    }
}