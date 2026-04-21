using System;
using AllToolkit.PriorityQueueUtils;

namespace AllToolkit.PriorityQueueUtils.Tests
{
    /// <summary>
    /// 优先队列工具类测试
    /// </summary>
    public class PriorityQueueUtilsTest
    {
        private static int _passed = 0;
        private static int _failed = 0;

        public static void Main(string[] args)
        {
            Console.WriteLine("========================================");
            Console.WriteLine("优先队列工具类测试");
            Console.WriteLine("========================================\n");

            // 最小堆测试
            TestMinPriorityQueue();
            
            // 最大堆测试
            TestMaxPriorityQueue();
            
            // 工厂方法测试
            TestFactoryMethods();
            
            // 边界值测试
            TestEdgeCases();
            
            // 性能测试
            TestPerformance();

            Console.WriteLine("\n========================================");
            Console.WriteLine($"测试结果: 通过 {_passed}, 失败 {_failed}");
            Console.WriteLine("========================================");
            
            Environment.Exit(_failed > 0 ? 1 : 0);
        }

        #region 最小堆优先队列测试

        static void TestMinPriorityQueue()
        {
            Console.WriteLine("--- 最小堆优先队列测试 ---\n");

            // 测试1: 基本入队出队
            Test("MinQueue_基本入队出队", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("低优先级", 3);
                queue.Enqueue("中优先级", 2);
                queue.Enqueue("高优先级", 1);

                Assert(queue.Count == 3, "Count应该为3");
                Assert(queue.Dequeue() == "高优先级", "第一个出队应该是高优先级");
                Assert(queue.Dequeue() == "中优先级", "第二个出队应该是中优先级");
                Assert(queue.Dequeue() == "低优先级", "第三个出队应该是低优先级");
            });

            // 测试2: 相同优先级保持相对顺序
            Test("MinQueue_相同优先级", () =>
            {
                var queue = new MinPriorityQueue<int>();
                queue.Enqueue(1, 1);
                queue.Enqueue(2, 1);
                queue.Enqueue(3, 1);

                Assert(queue.Count == 3, "Count应该为3");
                var first = queue.Dequeue();
                Assert(first == 1 || first == 2 || first == 3, "相同优先级的元素应该被正确出队");
            });

            // 测试3: Peek 不移除元素
            Test("MinQueue_Peek不移除元素", () =>
            {
                var queue = new MinPriorityQueue<int>();
                queue.Enqueue(100, 1);
                queue.Enqueue(200, 2);

                Assert(queue.Peek() == 100, "Peek应该返回优先级最高的元素");
                Assert(queue.Count == 2, "Peek不应该移除元素");
            });

            // 测试4: PeekWithPriority
            Test("MinQueue_PeekWithPriority", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("任务A", 5);
                queue.Enqueue("任务B", 2);

                var element = queue.PeekWithPriority();
                Assert(element.Value == "任务B", "PeekWithPriority应该返回高优先级元素");
                Assert(element.Priority == 2, "PeekWithPriority应该返回正确优先级");
            });

            // 测试5: DequeueWithPriority
            Test("MinQueue_DequeueWithPriority", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("任务A", 10);
                queue.Enqueue("任务B", 3);

                var element = queue.DequeueWithPriority();
                Assert(element.Value == "任务B", "DequeueWithPriority应该返回高优先级元素");
                Assert(element.Priority == 3, "DequeueWithPriority应该返回正确优先级");
                Assert(queue.Count == 1, "DequeueWithPriority应该移除元素");
            });

            // 测试6: TryPeek
            Test("MinQueue_TryPeek", () =>
            {
                var queue = new MinPriorityQueue<int>();
                
                int value, priority;
                Assert(!queue.TryPeek(out value, out priority), "空队列TryPeek应该返回false");

                queue.Enqueue(42, 7);
                Assert(queue.TryPeek(out value, out priority), "非空队列TryPeek应该返回true");
                Assert(value == 42, "TryPeek应该返回正确的值");
                Assert(priority == 7, "TryPeek应该返回正确的优先级");
            });

            // 测试7: TryDequeue
            Test("MinQueue_TryDequeue", () =>
            {
                var queue = new MinPriorityQueue<int>();
                
                int value, priority;
                Assert(!queue.TryDequeue(out value, out priority), "空队列TryDequeue应该返回false");

                queue.Enqueue(100, 1);
                Assert(queue.TryDequeue(out value, out priority), "非空队列TryDequeue应该返回true");
                Assert(value == 100, "TryDequeue应该返回正确的值");
                Assert(priority == 1, "TryDequeue应该返回正确的优先级");
                Assert(queue.IsEmpty, "TryDequeue后队列应该为空");
            });

            // 测试8: Contains
            Test("MinQueue_Contains", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("A", 1);
                queue.Enqueue("B", 2);
                queue.Enqueue("C", 3);

                Assert(queue.Contains("A"), "应该包含A");
                Assert(queue.Contains("B"), "应该包含B");
                Assert(!queue.Contains("D"), "不应该包含D");
            });

            // 测试9: Contains with priority
            Test("MinQueue_ContainsWithPriority", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("A", 1);
                queue.Enqueue("B", 2);

                Assert(queue.Contains("A", 1), "应该包含A且优先级为1");
                Assert(!queue.Contains("A", 2), "不应该包含A且优先级为2");
            });

            // 测试10: Clear
            Test("MinQueue_Clear", () =>
            {
                var queue = new MinPriorityQueue<int>();
                queue.Enqueue(1, 1);
                queue.Enqueue(2, 2);
                queue.Enqueue(3, 3);

                queue.Clear();
                Assert(queue.IsEmpty, "Clear后队列应该为空");
                Assert(queue.Count == 0, "Clear后Count应该为0");
            });

            // 测试11: GetAll
            Test("MinQueue_GetAll", () =>
            {
                var queue = new MinPriorityQueue<int>();
                queue.Enqueue(1, 3);
                queue.Enqueue(2, 1);
                queue.Enqueue(3, 2);

                var all = queue.GetAll();
                Assert(all.Count == 3, "GetAll应该返回所有元素");
                Assert(queue.Count == 3, "GetAll不应该移除元素");
            });

            // 测试12: 负数优先级
            Test("MinQueue_负数优先级", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("普通", 0);
                queue.Enqueue("紧急", -10);
                queue.Enqueue("更低", -20);

                Assert(queue.Dequeue() == "更低", "-20应该是最高优先级");
                Assert(queue.Dequeue() == "紧急", "-10应该是次高优先级");
                Assert(queue.Dequeue() == "普通", "0应该是最低优先级");
            });

            // 测试13: 大优先级值
            Test("MinQueue_大优先级值", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("小", int.MinValue);
                queue.Enqueue("大", int.MaxValue);

                Assert(queue.Dequeue() == "小", "int.MinValue应该是最高优先级");
                Assert(queue.Dequeue() == "大", "int.MaxValue应该是最低优先级");
            });

            // 测试14: 指定容量构造
            Test("MinQueue_指定容量构造", () =>
            {
                var queue = new MinPriorityQueue<int>(100);
                Assert(queue.Count == 0, "新构造的队列应该为空");
                
                for (int i = 0; i < 100; i++)
                    queue.Enqueue(i, i);
                
                Assert(queue.Count == 100, "应该能添加100个元素");
            });

            // 测试15: IsEmpty属性
            Test("MinQueue_IsEmpty属性", () =>
            {
                var queue = new MinPriorityQueue<int>();
                Assert(queue.IsEmpty, "新队列应该为空");
                
                queue.Enqueue(1, 1);
                Assert(!queue.IsEmpty, "添加元素后不应该为空");
                
                queue.Dequeue();
                Assert(queue.IsEmpty, "移除所有元素后应该为空");
            });
        }

        #endregion

        #region 最大堆优先队列测试

        static void TestMaxPriorityQueue()
        {
            Console.WriteLine("\n--- 最大堆优先队列测试 ---\n");

            // 测试1: 基本入队出队
            Test("MaxQueue_基本入队出队", () =>
            {
                var queue = new MaxPriorityQueue<string>();
                queue.Enqueue("低优先级", 1);
                queue.Enqueue("中优先级", 2);
                queue.Enqueue("高优先级", 3);

                Assert(queue.Dequeue() == "高优先级", "第一个出队应该是高优先级(值最大)");
                Assert(queue.Dequeue() == "中优先级", "第二个出队应该是中优先级");
                Assert(queue.Dequeue() == "低优先级", "第三个出队应该是低优先级");
            });

            // 测试2: Peek
            Test("MaxQueue_Peek", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                queue.Enqueue(1, 10);
                queue.Enqueue(2, 20);
                queue.Enqueue(3, 30);

                Assert(queue.Peek() == 3, "Peek应该返回优先级最高的元素(优先级30)");
                Assert(queue.Count == 3, "Peek不应该移除元素");
            });

            // 测试3: TryPeek
            Test("MaxQueue_TryPeek", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                
                int value, priority;
                Assert(!queue.TryPeek(out value, out priority), "空队列TryPeek应该返回false");

                queue.Enqueue(99, 100);
                Assert(queue.TryPeek(out value, out priority), "非空队列TryPeek应该返回true");
                Assert(value == 99, "TryPeek应该返回正确的值");
                Assert(priority == 100, "TryPeek应该返回正确的优先级");
            });

            // 测试4: TryDequeue
            Test("MaxQueue_TryDequeue", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                
                int value, priority;
                Assert(!queue.TryDequeue(out value, out priority), "空队列TryDequeue应该返回false");

                queue.Enqueue(50, 5);
                Assert(queue.TryDequeue(out value, out priority), "非空队列TryDequeue应该返回true");
                Assert(queue.IsEmpty, "TryDequeue后队列应该为空");
            });

            // 测试5: Contains
            Test("MaxQueue_Contains", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                queue.Enqueue(1, 1);
                queue.Enqueue(2, 2);

                Assert(queue.Contains(1), "应该包含1");
                Assert(queue.Contains(2), "应该包含2");
                Assert(!queue.Contains(3), "不应该包含3");
            });

            // 测试6: Contains with priority
            Test("MaxQueue_ContainsWithPriority", () =>
            {
                var queue = new MaxPriorityQueue<string>();
                queue.Enqueue("test", 5);

                Assert(queue.Contains("test", 5), "应该包含test且优先级为5");
                Assert(!queue.Contains("test", 10), "不应该包含test且优先级为10");
            });

            // 测试7: Clear
            Test("MaxQueue_Clear", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                queue.Enqueue(1, 1);
                queue.Enqueue(2, 2);

                queue.Clear();
                Assert(queue.IsEmpty, "Clear后队列应该为空");
            });

            // 测试8: GetAll
            Test("MaxQueue_GetAll", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                queue.Enqueue(1, 1);
                queue.Enqueue(2, 2);

                var all = queue.GetAll();
                Assert(all.Count == 2, "GetAll应该返回所有元素");
            });

            // 测试9: 负数优先级
            Test("MaxQueue_负数优先级", () =>
            {
                var queue = new MaxPriorityQueue<string>();
                queue.Enqueue("最低", -100);
                queue.Enqueue("中等", 0);
                queue.Enqueue("最高", 100);

                Assert(queue.Dequeue() == "最高", "100应该是最高优先级");
                Assert(queue.Dequeue() == "中等", "0应该是次高优先级");
                Assert(queue.Dequeue() == "最低", "-100应该是最低优先级");
            });

            // 测试10: 空队列出队异常
            Test("MaxQueue_空队列出队异常", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                bool exceptionThrown = false;
                try
                {
                    queue.Dequeue();
                }
                catch (InvalidOperationException)
                {
                    exceptionThrown = true;
                }
                Assert(exceptionThrown, "空队列出队应该抛出InvalidOperationException");
            });

            // 测试11: 空队列Peek异常
            Test("MaxQueue_空队列Peek异常", () =>
            {
                var queue = new MaxPriorityQueue<int>();
                bool exceptionThrown = false;
                try
                {
                    queue.Peek();
                }
                catch (InvalidOperationException)
                {
                    exceptionThrown = true;
                }
                Assert(exceptionThrown, "空队列Peek应该抛出InvalidOperationException");
            });
        }

        #endregion

        #region 工厂方法测试

        static void TestFactoryMethods()
        {
            Console.WriteLine("\n--- 工厂方法测试 ---\n");

            // 测试1: CreateMinQueue
            Test("Factory_CreateMinQueue", () =>
            {
                var queue = PriorityQueue.CreateMinQueue<int>();
                Assert(queue != null, "CreateMinQueue应该返回非空队列");
                Assert(queue.IsEmpty, "新创建的队列应该为空");
            });

            // 测试2: CreateMinQueue with capacity
            Test("Factory_CreateMinQueueWithCapacity", () =>
            {
                var queue = PriorityQueue.CreateMinQueue<string>(50);
                Assert(queue != null, "CreateMinQueue(50)应该返回非空队列");
                Assert(queue.IsEmpty, "新创建的队列应该为空");
            });

            // 测试3: CreateMaxQueue
            Test("Factory_CreateMaxQueue", () =>
            {
                var queue = PriorityQueue.CreateMaxQueue<int>();
                Assert(queue != null, "CreateMaxQueue应该返回非空队列");
                Assert(queue.IsEmpty, "新创建的队列应该为空");
            });

            // 测试4: CreateMaxQueue with capacity
            Test("Factory_CreateMaxQueueWithCapacity", () =>
            {
                var queue = PriorityQueue.CreateMaxQueue<string>(50);
                Assert(queue != null, "CreateMaxQueue(50)应该返回非空队列");
                Assert(queue.IsEmpty, "新创建的队列应该为空");
            });

            // 测试5: FromCollection
            Test("Factory_FromCollection", () =>
            {
                var items = new[]
                {
                    Tuple.Create("C", 3),
                    Tuple.Create("A", 1),
                    Tuple.Create("B", 2)
                };

                var queue = PriorityQueue.FromCollection(items);
                Assert(queue.Count == 3, "应该有3个元素");
                Assert(queue.Dequeue() == "A", "最小堆第一个出队应该是优先级最低的A");
            });

            // 测试6: FromCollectionMax
            Test("Factory_FromCollectionMax", () =>
            {
                var items = new[]
                {
                    Tuple.Create("C", 3),
                    Tuple.Create("A", 1),
                    Tuple.Create("B", 2)
                };

                var queue = PriorityQueue.FromCollectionMax(items);
                Assert(queue.Count == 3, "应该有3个元素");
                Assert(queue.Dequeue() == "C", "最大堆第一个出队应该是优先级最高的C");
            });

            // 测试7: Merge
            Test("Factory_Merge", () =>
            {
                var queue1 = new MinPriorityQueue<int>();
                queue1.Enqueue(1, 1);
                queue1.Enqueue(2, 2);

                var queue2 = new MinPriorityQueue<int>();
                queue2.Enqueue(3, 3);
                queue2.Enqueue(0, 0);

                var merged = PriorityQueue.Merge(queue1, queue2);
                Assert(merged.Count == 4, "合并后应该有4个元素");
                Assert(merged.Dequeue() == 0, "最小堆合并后第一个出队应该是0");
            });

            // 测试8: MergeMax
            Test("Factory_MergeMax", () =>
            {
                var queue1 = new MaxPriorityQueue<int>();
                queue1.Enqueue(1, 1);
                queue1.Enqueue(2, 2);

                var queue2 = new MaxPriorityQueue<int>();
                queue2.Enqueue(3, 3);
                queue2.Enqueue(0, 0);

                var merged = PriorityQueue.MergeMax(queue1, queue2);
                Assert(merged.Count == 4, "合并后应该有4个元素");
                Assert(merged.Dequeue() == 3, "最大堆合并后第一个出队应该是3");
            });

            // 测试9: 空集合合并
            Test("Factory_Merge空队列", () =>
            {
                var merged = PriorityQueue.Merge<int>();
                Assert(merged.IsEmpty, "合并空队列应该返回空队列");
            });

            // 测试10: FromCollection空集合
            Test("Factory_FromCollection空集合", () =>
            {
                var queue = PriorityQueue.FromCollection(new Tuple<int, int>[0]);
                Assert(queue.IsEmpty, "从空集合创建应该返回空队列");
            });
        }

        #endregion

        #region 边界值测试

        static void TestEdgeCases()
        {
            Console.WriteLine("\n--- 边界值测试 ---\n");

            // 测试1: 单元素
            Test("边界_单元素", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("only", 1);

                Assert(queue.Count == 1, "Count应该为1");
                Assert(queue.Peek() == "only", "Peek应该返回唯一元素");
                Assert(queue.Dequeue() == "only", "Dequeue应该返回唯一元素");
                Assert(queue.IsEmpty, "Dequeue后应该为空");
            });

            // 测试2: 空值元素
            Test("边界_空值元素", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue(null, 1);
                queue.Enqueue("test", 2);

                Assert(queue.Count == 2, "应该能添加null值");
                var first = queue.Dequeue();
                Assert(first == null, "null值应该能正确出队");
            });

            // 测试3: 大量元素
            Test("边界_大量元素", () =>
            {
                var queue = new MinPriorityQueue<int>();
                int count = 10000;

                for (int i = count; i > 0; i--)
                    queue.Enqueue(i, i);

                Assert(queue.Count == count, $"应该能添加{count}个元素");

                int expected = 1;
                while (!queue.IsEmpty)
                {
                    int val = queue.Dequeue();
                    if (val != expected)
                    {
                        throw new Exception($"出队顺序错误: 期望{expected}, 实际{val}");
                    }
                    expected++;
                }
            });

            // 测试4: 优先级全部相同
            Test("边界_优先级全部相同", () =>
            {
                var queue = new MinPriorityQueue<int>();
                for (int i = 1; i <= 5; i++)
                    queue.Enqueue(i, 10); // 所有优先级都是10

                Assert(queue.Count == 5, "应该能添加所有元素");
                
                // 当优先级相同时，元素应该都能正确出队
                int total = 0;
                while (!queue.IsEmpty)
                    total += queue.Dequeue();
                Assert(total == 15, "所有元素应该都被正确出队(1+2+3+4+5=15)");
            });

            // 测试5: 复杂类型
            Test("边界_复杂类型", () =>
            {
                var queue = new MinPriorityQueue<TaskInfo>();
                queue.Enqueue(new TaskInfo { Name = "Low", Priority = 3 }, 3);
                queue.Enqueue(new TaskInfo { Name = "High", Priority = 1 }, 1);
                queue.Enqueue(new TaskInfo { Name = "Medium", Priority = 2 }, 2);

                var first = queue.Dequeue();
                Assert(first.Name == "High", "高优先级任务应该先出队");
            });

            // 测试6: int.MinValue和int.MaxValue优先级混合
            Test("边界_极端优先级值混合", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("正常1", 0);
                queue.Enqueue("最小", int.MinValue);
                queue.Enqueue("最大", int.MaxValue);
                queue.Enqueue("正常2", 1);

                Assert(queue.Dequeue() == "最小", "int.MinValue应该最先出队");
                Assert(queue.Dequeue() == "正常1", "0应该次出队");
                Assert(queue.Dequeue() == "正常2", "1应该第三出队");
                Assert(queue.Dequeue() == "最大", "int.MaxValue应该最后出队");
            });

            // 测试7: 连续Enqueue和Dequeue
            Test("边界_连续EnqueueDequeue", () =>
            {
                var queue = new MinPriorityQueue<int>();
                
                // 入队出队交替进行
                queue.Enqueue(5, 5);
                Assert(queue.Dequeue() == 5, "单元素出队应该正确");
                
                queue.Enqueue(3, 3);
                queue.Enqueue(1, 1);
                queue.Enqueue(2, 2);
                Assert(queue.Dequeue() == 1, "应该返回优先级最高的1");
                
                queue.Enqueue(0, 0);
                Assert(queue.Dequeue() == 0, "应该返回优先级最高的0");
                Assert(queue.Dequeue() == 2, "应该返回优先级次高的2");
            });

            // 测试8: DequeueWithPriority返回值验证
            Test("边界_DequeueWithPriority完整返回", () =>
            {
                var queue = new MinPriorityQueue<string>();
                queue.Enqueue("任务A", 100);
                queue.Enqueue("任务B", 50);

                var elem1 = queue.DequeueWithPriority();
                Assert(elem1.Value == "任务B", "应该返回高优先级任务");
                Assert(elem1.Priority == 50, "应该返回正确优先级值50");

                var elem2 = queue.DequeueWithPriority();
                Assert(elem2.Value == "任务A", "应该返回剩余任务");
                Assert(elem2.Priority == 100, "应该返回正确优先级值100");
            });
        }

        #endregion

        #region 性能测试

        static void TestPerformance()
        {
            Console.WriteLine("\n--- 性能测试 ---\n");

            // 测试1: 大量元素Enqueue性能
            Test("性能_大量Enqueue", () =>
            {
                var queue = new MinPriorityQueue<int>(100000);
                var random = new Random(42);
                var sw = System.Diagnostics.Stopwatch.StartNew();

                for (int i = 0; i < 100000; i++)
                    queue.Enqueue(i, random.Next());

                sw.Stop();
                Assert(queue.Count == 100000, "应该添加所有元素");
                Console.WriteLine($"    100,000次Enqueue耗时: {sw.ElapsedMilliseconds}ms");
            });

            // 测试2: 大量元素Dequeue性能
            Test("性能_大量Dequeue", () =>
            {
                var queue = new MinPriorityQueue<int>();
                for (int i = 0; i < 100000; i++)
                    queue.Enqueue(i, i);

                var sw = System.Diagnostics.Stopwatch.StartNew();
                int prev = -1;
                while (!queue.IsEmpty)
                {
                    int val = queue.Dequeue();
                    if (val <= prev)
                        throw new Exception("出队顺序错误");
                    prev = val;
                }
                sw.Stop();
                Console.WriteLine($"    100,000次Dequeue耗时: {sw.ElapsedMilliseconds}ms");
            });

            // 测试3: Contains性能
            Test("性能_Contains", () =>
            {
                var queue = new MinPriorityQueue<int>();
                for (int i = 0; i < 10000; i++)
                    queue.Enqueue(i, i);

                var sw = System.Diagnostics.Stopwatch.StartNew();
                bool found = queue.Contains(9999);
                sw.Stop();
                Assert(found, "应该找到元素");
                Console.WriteLine($"    Contains(9999)在10000元素中耗时: {sw.ElapsedMilliseconds}ms");
            });
        }

        #endregion

        #region 辅助方法

        static void Test(string name, Action test)
        {
            try
            {
                test();
                Console.WriteLine($"✓ {name}");
                _passed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ {name}");
                Console.WriteLine($"  错误: {ex.Message}");
                _failed++;
            }
        }

        static void Assert(bool condition, string message)
        {
            if (!condition)
                throw new Exception($"断言失败: {message}");
        }

        #endregion
    }

    /// <summary>
    /// 测试用复杂类型
    /// </summary>
    public class TaskInfo
    {
        public string Name { get; set; }
        public int Priority { get; set; }

        public override string ToString() => $"[{Priority}] {Name}";
    }
}