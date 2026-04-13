/**
 * Bloom Filter 测试模块
 * 
 * 测试布隆过滤器的各项功能
 * 
 * @author AllToolkit Auto-Generator
 * @date 2026-04-13
 */

package bloom_filter_utils

import kotlin.system.measureNanoTime

/**
 * 测试结果类
 */
data class TestResult(
    val name: String,
    val passed: Boolean,
    val message: String = ""
)

/**
 * 测试运行器
 */
object BloomFilterTest {
    private val results = mutableListOf<TestResult>()
    
    fun runAllTests() {
        println("========================================")
        println("  Bloom Filter 测试套件")
        println("========================================\n")
        
        // 基础功能测试
        testBasicOperations()
        testMightContain()
        testFalsePositiveRate()
        testClearOperation()
        testSerialization()
        
        // 可扩展布隆过滤器测试
        testScalableBloomFilter()
        
        // 计数布隆过滤器测试
        testCountingBloomFilter()
        
        // 性能测试
        testPerformance()
        testMemoryEfficiency()
        
        // 打印结果
        printResults()
    }
    
    /**
     * 测试基础操作
     */
    private fun testBasicOperations() {
        val testName = "基础操作测试"
        try {
            val filter = BloomFilter<String>(1000, 0.01)
            
            // 测试初始状态
            assert(filter.isEmpty()) { "新创建的过滤器应该为空" }
            assert(filter.size() == 0) { "初始大小应为0" }
            
            // 添加元素
            filter.add("hello")
            assert(!filter.isEmpty()) { "添加元素后不应为空" }
            assert(filter.size() == 1) { "大小应为1" }
            
            // 批量添加
            filter.addAll(listOf("world", "kotlin", "bloom"))
            assert(filter.size() == 4) { "批量添加后大小应为4" }
            
            results.add(TestResult(testName, true))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 测试元素检查
     */
    private fun testMightContain() {
        val testName = "元素检查测试"
        try {
            val filter = BloomFilter<Int>(100, 0.01)
            
            // 添加1-50
            for (i in 1..50) {
                filter.add(i)
            }
            
            // 检查已添加的元素
            var allContained = true
            for (i in 1..50) {
                if (!filter.mightContain(i)) {
                    allContained = false
                    break
                }
            }
            assert(allContained) { "已添加的元素应该全部能被找到" }
            
            // 检查未添加的元素（注意可能有假阳性）
            // definitelyNotContains 应该对大部分未添加元素返回 true
            var definitelyNotCount = 0
            for (i in 51..100) {
                if (filter.definitelyNotContains(i)) {
                    definitelyNotCount++
                }
            }
            
            // 由于假阳性概率很低，大部分未添加元素应该确实不存在
            assert(definitelyNotCount >= 45) { "大部分未添加元素应该确实不存在" }
            
            results.add(TestResult(testName, true))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 测试假阳性率
     */
    private fun testFalsePositiveRate() {
        val testName = "假阳性率测试"
        try {
            val expectedInsertions = 10000
            val targetFpp = 0.03
            val filter = BloomFilter<String>(expectedInsertions, targetFpp)
            
            // 添加元素
            for (i in 1..expectedInsertions) {
                filter.add("item_$i")
            }
            
            // 测试假阳性
            val testCount = 10000
            var falsePositives = 0
            for (i in (expectedInsertions + 1)..(expectedInsertions + testCount)) {
                if (filter.mightContain("item_$i")) {
                    falsePositives++
                }
            }
            
            val actualFpp = falsePositives.toDouble() / testCount
            println("\n  假阳性率测试:")
            println("    目标假阳性率: ${String.format("%.4f", targetFpp)}")
            println("    实际假阳性率: ${String.format("%.4f", actualFpp)}")
            println("    估计假阳性率: ${String.format("%.4f", filter.estimateFpp())}")
            
            // 实际假阳性率应该接近目标值（允许一定误差）
            // 注意：由于随机性，实际FPP可能会有波动
            assert(actualFpp < targetFpp * 3) { "实际假阳性率不应过高" }
            
            results.add(TestResult(testName, true, "实际FPP=${String.format("%.4f", actualFpp)}"))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 测试清空操作
     */
    private fun testClearOperation() {
        val testName = "清空操作测试"
        try {
            val filter = BloomFilter<String>(100, 0.01)
            
            filter.addAll(listOf("a", "b", "c", "d", "e"))
            assert(!filter.isEmpty()) { "添加元素后不应为空" }
            
            filter.clear()
            assert(filter.isEmpty()) { "清空后应为空" }
            assert(filter.size() == 0) { "清空后大小应为0" }
            
            // 清空后添加应该正常工作
            filter.add("new")
            assert(filter.mightContain("new")) { "清空后应该能添加新元素" }
            
            results.add(TestResult(testName, true))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 测试序列化
     */
    private fun testSerialization() {
        val testName = "序列化测试"
        try {
            val originalFilter = BloomFilter<Int>(1000, 0.01)
            
            // 添加元素
            for (i in 1..500) {
                originalFilter.add(i)
            }
            
            // 序列化
            val bytes = originalFilter.toByteArray()
            
            // 反序列化
            val restoredFilter = BloomFilter.fromByteArray<Int>(bytes)
            
            // 验证
            assert(restoredFilter.size() == originalFilter.size()) { "大小应该一致" }
            
            // 检查所有元素
            var allMatch = true
            for (i in 1..500) {
                if (restoredFilter.mightContain(i) != originalFilter.mightContain(i)) {
                    allMatch = false
                    break
                }
            }
            assert(allMatch) { "序列化前后应该保持一致性" }
            
            println("\n  序列化测试:")
            println("    原始过滤器: $originalFilter")
            println("    恢复过滤器: $restoredFilter")
            println("    序列化大小: ${bytes.size} bytes")
            
            results.add(TestResult(testName, true, "序列化大小=${bytes.size} bytes"))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 测试可扩展布隆过滤器
     */
    private fun testScalableBloomFilter() {
        val testName = "可扩展布隆过滤器测试"
        try {
            val filter = ScalableBloomFilter<String>(initialCapacity = 100, fpp = 0.01)
            
            // 添加超过初始容量的元素
            for (i in 1..1000) {
                filter.add("item_$i")
            }
            
            assert(filter.size() == 1000) { "大小应为1000" }
            assert(filter.filterCount() > 1) { "应该创建了多个过滤器" }
            
            // 检查元素
            var allContained = true
            for (i in 1..1000) {
                if (!filter.mightContain("item_$i")) {
                    allContained = false
                    break
                }
            }
            assert(allContained) { "所有添加的元素应该能被找到" }
            
            println("\n  可扩展布隆过滤器:")
            println("    过滤器数量: ${filter.filterCount()}")
            println("    总大小: ${filter.size()}")
            println("    内存使用: ${filter.memoryUsage()} bytes")
            
            results.add(TestResult(testName, true, "过滤器数量=${filter.filterCount()}"))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 测试计数布隆过滤器
     */
    private fun testCountingBloomFilter() {
        val testName = "计数布隆过滤器测试"
        try {
            val filter = CountingBloomFilter<String>(1000, 0.01)
            
            // 添加元素
            filter.add("hello")
            filter.add("world")
            
            assert(filter.mightContain("hello")) { "hello应该存在" }
            assert(filter.mightContain("world")) { "world应该存在" }
            assert(filter.size() == 2) { "大小应为2" }
            
            // 删除元素
            assert(filter.remove("hello")) { "删除hello应该成功" }
            assert(!filter.mightContain("hello")) { "删除后hello不应该存在" }
            assert(filter.mightContain("world")) { "world应该仍然存在" }
            
            // 删除不存在的元素
            assert(!filter.remove("nonexistent")) { "删除不存在的元素应返回false" }
            
            results.add(TestResult(testName, true))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 性能测试
     */
    private fun testPerformance() {
        val testName = "性能测试"
        try {
            val filter = BloomFilter<String>(100000, 0.01)
            val testSize = 100000
            
            // 插入性能
            val insertTime = measureNanoTime {
                for (i in 1..testSize) {
                    filter.add("item_$i")
                }
            }
            
            // 查询性能
            val queryTime = measureNanoTime {
                for (i in 1..testSize) {
                    filter.mightContain("item_$i")
                }
            }
            
            val insertNs = insertTime / testSize
            val queryNs = queryTime / testSize
            
            println("\n  性能测试 ($testSize 次操作):")
            println("    平均插入时间: ${insertNs} ns/次")
            println("    平均查询时间: ${queryNs} ns/次")
            println("    总插入时间: ${insertTime / 1_000_000} ms")
            println("    总查询时间: ${queryTime / 1_000_000} ms")
            
            // 性能断言：单次操作应在合理范围内
            assert(insertNs < 10000) { "插入操作应该很快" }
            assert(queryNs < 10000) { "查询操作应该很快" }
            
            results.add(TestResult(testName, true, "插入=${insertNs}ns, 查询=${queryNs}ns"))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    /**
     * 内存效率测试
     */
    private fun testMemoryEfficiency() {
        val testName = "内存效率测试"
        try {
            val expectedInsertions = 100000
            val filter = BloomFilter<String>(expectedInsertions, 0.01)
            
            val memoryBytes = filter.memoryUsage()
            val bitsPerElement = filter.bitArraySize().toDouble() / expectedInsertions
            
            println("\n  内存效率:")
            println("    预期插入数: $expectedInsertions")
            println("    位数组大小: ${filter.bitArraySize()} bits")
            println("    内存使用: ${memoryBytes / 1024} KB")
            println("    每元素位数: ${String.format("%.2f", bitsPerElement)}")
            println("    哈希函数数: ${filter.hashFunctionCount()}")
            
            // 与HashSet对比（粗略估计）
            val hashSetEstimateBytes = expectedInsertions * 100L // 假设每个元素100字节
            val savings = (1 - memoryBytes.toDouble() / hashSetEstimateBytes) * 100
            
            println("    相比HashSet节省: ${String.format("%.1f", savings)}%")
            
            results.add(TestResult(testName, true, "内存=${memoryBytes/1024}KB, 节省${String.format("%.1f", savings)}%"))
        } catch (e: Exception) {
            results.add(TestResult(testName, false, e.message ?: "Unknown error"))
        }
    }
    
    private fun printResults() {
        println("\n========================================")
        println("  测试结果汇总")
        println("========================================")
        
        val passed = results.count { it.passed }
        val total = results.size
        
        results.forEach { result ->
            val status = if (result.passed) "✓ PASS" else "✗ FAIL"
            println("  $status - ${result.name}")
            if (result.message.isNotEmpty()) {
                println("         ${result.message}")
            }
            if (!result.passed) {
                println("         错误: ${result.message}")
            }
        }
        
        println("\n  总计: $passed/$total 通过")
        println("========================================\n")
    }
}

/**
 * 主函数入口
 */
fun main() {
    BloomFilterTest.runAllTests()
}