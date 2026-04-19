using System;
using System.Collections.Generic;
using System.Linq;
using AllToolkit.BloomFilter;

namespace AllToolkit.Tests
{
    /// <summary>
    /// BloomFilter 单元测试
    /// </summary>
    class BloomFilterTest
    {
        private static int passed = 0;
        private static int failed = 0;
        private static readonly Random random = new Random(42);

        static void Main(string[] args)
        {
            Console.WriteLine("Running BloomFilter tests...\n");

            TestBasicOperations();
            TestFalsePositiveRate();
            TestCloneAndUnion();
            TestSerialization();
            TestScalableBloomFilter();
            TestCountingBloomFilter();
            TestEdgeCases();
            TestPerformance();

            Console.WriteLine("\n========================================");
            Console.WriteLine($"Results: {passed} passed, {failed} failed");
            Console.WriteLine("========================================");

            Environment.Exit(failed > 0 ? 1 : 0);
        }

        static void Assert(bool condition, string testName)
        {
            if (condition)
            {
                Console.WriteLine($"  ✓ {testName}");
                passed++;
            }
            else
            {
                Console.WriteLine($"  ✗ {testName}");
                failed++;
            }
        }

        static void TestBasicOperations()
        {
            Console.WriteLine("\nBasic Operations Tests:");

            // 创建布隆过滤器
            var filter = new BloomFilter<string>(1000, 0.01);
            Assert(filter.ExpectedItems == 1000, "Expected items set correctly");
            Assert(filter.Count == 0, "Initial count is 0");
            Assert(filter.BitSize > 0, "Bit size calculated");
            Assert(filter.HashFunctionCount > 0, "Hash function count calculated");

            // 添加元素
            filter.Add("hello");
            filter.Add("world");
            Assert(filter.Count == 2, "Count after adding elements");

            // 检查存在
            Assert(filter.MightContain("hello"), "Contains 'hello'");
            Assert(filter.MightContain("world"), "Contains 'world'");
            Assert(!filter.MightContain("notexist"), "Does not contain 'notexist'");

            // Contains 别名测试
            Assert(filter.Contains("hello"), "Contains alias works");

            // 批量添加
            var items = new List<string> { "one", "two", "three", "four", "five" };
            filter.AddRange(items);
            Assert(filter.Count == 7, "Count after AddRange");
            Assert(filter.MightContain("one"), "Contains 'one' after AddRange");

            // 清空
            filter.Clear();
            Assert(filter.Count == 0, "Count after Clear");
            Assert(!filter.MightContain("hello"), "Does not contain after Clear");
        }

        static void TestFalsePositiveRate()
        {
            Console.WriteLine("\nFalse Positive Rate Tests:");

            int expectedItems = 10000;
            double targetFPR = 0.01;
            var filter = new BloomFilter<string>(expectedItems, targetFPR);

            // 添加元素
            var addedItems = new HashSet<string>();
            for (int i = 0; i < expectedItems; i++)
            {
                string item = $"item_{i}";
                filter.Add(item);
                addedItems.Add(item);
            }

            Assert(filter.Count == expectedItems, "All items added");

            // 测试假阳性率
            int falsePositives = 0;
            int testCount = 100000;
            for (int i = 0; i < testCount; i++)
            {
                string testItem = $"test_{i}";
                if (!addedItems.Contains(testItem) && filter.MightContain(testItem))
                {
                    falsePositives++;
                }
            }

            double actualFPR = (double)falsePositives / testCount;
            Console.WriteLine($"    Actual FPR: {actualFPR:P4} (target: {targetFPR:P2})");
            
            // 假阳性率应该接近目标值（允许一些偏差）
            Assert(actualFPR < targetFPR * 3, $"False positive rate within bounds ({actualFPR:P4} < {targetFPR * 3:P2})");

            // 测试估计的假阳性概率
            double estimatedFPR = filter.EstimatedFalsePositiveProbability;
            Console.WriteLine($"    Estimated FPR: {estimatedFPR:P4}");
            Assert(estimatedFPR >= 0 && estimatedFPR < 1, "Estimated FPR in valid range");

            // 测试统计信息
            var stats = filter.GetStats();
            Assert(stats.ItemsAdded == expectedItems, "Stats: ItemsAdded correct");
            Assert(stats.BitSize == filter.BitSize, "Stats: BitSize correct");
            Console.WriteLine($"    Stats: {stats}");
        }

        static void TestCloneAndUnion()
        {
            Console.WriteLine("\nClone and Union Tests:");

            var filter1 = new BloomFilter<int>(1000, 0.01);
            for (int i = 0; i < 100; i++)
            {
                filter1.Add(i);
            }

            // 克隆测试
            var cloned = (BloomFilter<int>)filter1.Clone();
            Assert(cloned.Count == filter1.Count, "Clone has same count");
            Assert(cloned.BitSize == filter1.BitSize, "Clone has same bit size");

            // 验证克隆后的内容
            for (int i = 0; i < 100; i++)
            {
                Assert(cloned.MightContain(i), $"Clone contains {i}");
            }

            // Union 测试
            var filter2 = new BloomFilter<int>(1000, 0.01);
            for (int i = 100; i < 200; i++)
            {
                filter2.Add(i);
            }

            filter1.UnionWith(filter2);

            // 验证 union 后包含两个集合的元素
            for (int i = 0; i < 200; i++)
            {
                Assert(filter1.MightContain(i), $"Union contains {i}");
            }

            // Intersect 测试
            var filter3 = new BloomFilter<int>(1000, 0.01);
            var filter4 = new BloomFilter<int>(1000, 0.01);

            for (int i = 0; i < 100; i++) filter3.Add(i);
            for (int i = 50; i < 150; i++) filter4.Add(i);

            filter3.IntersectWith(filter4);

            // 验证交集
            int intersectionCount = 0;
            for (int i = 0; i < 150; i++)
            {
                if (filter3.MightContain(i))
                {
                    intersectionCount++;
                }
            }
            Console.WriteLine($"    Intersection found ~{intersectionCount} items");
            Assert(intersectionCount > 0, "Intersection contains some items");
        }

        static void TestSerialization()
        {
            Console.WriteLine("\nSerialization Tests:");

            var filter = new BloomFilter<string>(1000, 0.01);
            filter.Add("test1");
            filter.Add("test2");
            filter.Add("test3");

            // 序列化
            byte[] data = filter.ToByteArray();
            Assert(data != null && data.Length > 0, "Serialized to byte array");
            Console.WriteLine($"    Serialized size: {data.Length} bytes");

            // 反序列化
            var restored = BloomFilter<string>.FromByteArray(data, 1000, 0.01);
            Assert(restored.MightContain("test1"), "Restored contains 'test1'");
            Assert(restored.MightContain("test2"), "Restored contains 'test2'");
            Assert(restored.MightContain("test3"), "Restored contains 'test3'");
            Assert(!restored.MightContain("notexist"), "Restored does not contain 'notexist'");

            // GetSerializedSize
            int expectedSize = filter.GetSerializedSize();
            Assert(data.Length == expectedSize, "Serialized size matches GetSerializedSize");
        }

        static void TestScalableBloomFilter()
        {
            Console.WriteLine("\nScalable Bloom Filter Tests:");

            var filter = new ScalableBloomFilter<int>(100, 0.01);

            // 添加大量元素，超过初始容量
            int itemCount = 1000;
            for (int i = 0; i < itemCount; i++)
            {
                filter.Add(i);
            }

            Assert(filter.Count == itemCount, $"Count is {itemCount}");
            Assert(filter.FilterCount > 1, $"Multiple filters created ({filter.FilterCount})");

            // 验证所有元素都可被检测
            int foundCount = 0;
            for (int i = 0; i < itemCount; i++)
            {
                if (filter.MightContain(i)) foundCount++;
            }
            Assert(foundCount == itemCount, "All items found in scalable filter");

            // 获取所有统计
            var allStats = filter.GetAllStats();
            Console.WriteLine($"    Filter layers: {allStats.Count}");
            foreach (var stats in allStats)
            {
                Console.WriteLine($"      {stats}");
            }
        }

        static void TestCountingBloomFilter()
        {
            Console.WriteLine("\nCounting Bloom Filter Tests:");

            var filter = new CountingBloomFilter<string>(1000, 0.01);

            // 添加元素
            filter.Add("item1");
            filter.Add("item2");
            filter.Add("item3");
            Assert(filter.Count == 3, "Count after adding elements");

            // 检查存在
            Assert(filter.MightContain("item1"), "Contains 'item1'");
            Assert(filter.MightContain("item2"), "Contains 'item2'");
            Assert(!filter.MightContain("notexist"), "Does not contain 'notexist'");

            // 删除元素
            bool removed = filter.Remove("item1");
            Assert(removed, "Remove 'item1' succeeded");
            Assert(filter.Count == 2, "Count after remove");

            // 删除后检查
            // 注意：由于计数布隆过滤器的特性，删除后可能仍显示存在（假阳性）
            // 但我们可以验证可以删除存在的元素

            // 删除不存在的元素应该失败
            removed = filter.Remove("notexist");
            Assert(!removed, "Remove non-existent item fails");

            // 清空
            filter.Clear();
            Assert(filter.Count == 0, "Count after Clear");

            // 测试假阳性概率估计
            var filter2 = new CountingBloomFilter<string>(1000, 0.01);
            for (int i = 0; i < 500; i++)
            {
                filter2.Add($"item_{i}");
            }
            double fpr = filter2.EstimatedFalsePositiveProbability;
            Console.WriteLine($"    Estimated FPR: {fpr:P4}");
            Assert(fpr >= 0 && fpr < 1, "Counting filter FPR in valid range");
        }

        static void TestEdgeCases()
        {
            Console.WriteLine("\nEdge Cases Tests:");

            // 小容量过滤器
            var smallFilter = new BloomFilter<string>(10, 0.1);
            smallFilter.Add("a");
            smallFilter.Add("b");
            Assert(smallFilter.Count == 2, "Small filter works");
            Assert(smallFilter.MightContain("a"), "Small filter contains 'a'");

            // 高假阳性率容忍
            var highFPFilter = new BloomFilter<int>(100, 0.5);
            for (int i = 0; i < 50; i++)
            {
                highFPFilter.Add(i);
            }
            Assert(highFPFilter.Count == 50, "High FP filter works");

            // 低假阳性率
            var lowFPFilter = new BloomFilter<int>(100, 0.001);
            for (int i = 0; i < 50; i++)
            {
                lowFPFilter.Add(i);
            }
            Assert(lowFPFilter.Count == 50, "Low FP filter works");

            // 空过滤器操作
            var emptyFilter = new BloomFilter<string>(100);
            Assert(!emptyFilter.MightContain("anything"), "Empty filter contains nothing");
            Assert(emptyFilter.Count == 0, "Empty filter count is 0");

            // 类型测试
            var intFilter = new BloomFilter<int>(100);
            intFilter.Add(42);
            Assert(intFilter.MightContain(42), "Int filter contains 42");
            Assert(!intFilter.MightContain(0), "Int filter does not contain 0");

            var guidFilter = new BloomFilter<Guid>(100);
            var guid = Guid.NewGuid();
            guidFilter.Add(guid);
            Assert(guidFilter.MightContain(guid), "Guid filter contains added guid");
            Assert(!guidFilter.MightContain(Guid.NewGuid()), "Guid filter does not contain random guid");

            // 静态方法测试
            int optimalBits = BloomFilter<string>.OptimalBitSize(1000, 0.01);
            Assert(optimalBits > 0, "OptimalBitSize returns positive value");
            Console.WriteLine($"    Optimal bits for 1000 items, 1% FP: {optimalBits}");

            int optimalHashes = BloomFilter<string>.OptimalHashFunctionCount(optimalBits, 1000);
            Assert(optimalHashes > 0, "OptimalHashFunctionCount returns positive value");
            Console.WriteLine($"    Optimal hash functions: {optimalHashes}");
        }

        static void TestPerformance()
        {
            Console.WriteLine("\nPerformance Tests:");

            int itemCount = 100000;
            double targetFPR = 0.01;

            // 创建和添加性能
            var sw = System.Diagnostics.Stopwatch.StartNew();
            var filter = new BloomFilter<string>(itemCount, targetFPR);
            for (int i = 0; i < itemCount; i++)
            {
                filter.Add($"item_{i}");
            }
            sw.Stop();
            Console.WriteLine($"    Add {itemCount:N0} items: {sw.ElapsedMilliseconds} ms");
            Assert(filter.Count == itemCount, "All items added in performance test");

            // 查询性能
            sw.Restart();
            int foundCount = 0;
            for (int i = 0; i < itemCount; i++)
            {
                if (filter.MightContain($"item_{i}")) foundCount++;
            }
            sw.Stop();
            Console.WriteLine($"    Query {itemCount:N0} existing items: {sw.ElapsedMilliseconds} ms");
            Assert(foundCount == itemCount, "All items found in performance test");

            // 不存在元素的查询性能
            sw.Restart();
            for (int i = 0; i < itemCount; i++)
            {
                filter.MightContain($"notexist_{i}");
            }
            sw.Stop();
            Console.WriteLine($"    Query {itemCount:N0} non-existing items: {sw.ElapsedMilliseconds} ms");

            // 内存使用
            long memoryBytes = filter.GetSerializedSize();
            Console.WriteLine($"    Memory usage: {memoryBytes:N0} bytes ({memoryBytes / 1024.0:N2} KB)");
            Console.WriteLine($"    Bits per item: {(double)filter.BitSize / itemCount:N2}");
        }
    }
}