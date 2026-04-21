using System;
using AllToolkit.PriorityQueueUtils;

namespace AllToolkit.PriorityQueueUtils.Examples
{
    /// <summary>
    /// 优先队列工具类使用示例
    /// </summary>
    public class UsageExamples
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("========================================");
            Console.WriteLine("优先队列工具类使用示例");
            Console.WriteLine("========================================\n");

            // 示例1: 任务调度
            TaskSchedulerExample();

            // 示例2: Dijkstra最短路径
            DijkstraExample();

            // 示例3: 合并K个有序列表
            MergeKSortedListsExample();

            // 示例4: 实时数据流处理
            DataStreamExample();

            // 示例5: 事件模拟
            EventSimulationExample();

            // 示例6: Top K 问题
            TopKExample();

            Console.WriteLine("\n所有示例执行完成!");
        }

        /// <summary>
        /// 示例1: 任务调度系统
        /// 使用最小堆优先队列实现任务按优先级执行
        /// </summary>
        static void TaskSchedulerExample()
        {
            Console.WriteLine("--- 示例1: 任务调度系统 ---\n");

            var scheduler = new MinPriorityQueue<Task>();

            // 添加不同优先级的任务
            scheduler.Enqueue(new Task { Name = "发送邮件", Description = "发送每日报告邮件" }, 3);
            scheduler.Enqueue(new Task { Name = "数据库备份", Description = "执行数据库备份" }, 1);
            scheduler.Enqueue(new Task { Name = "日志清理", Description = "清理过期日志文件" }, 5);
            scheduler.Enqueue(new Task { Name = "安全扫描", Description = "执行安全漏洞扫描" }, 2);
            scheduler.Enqueue(new Task { Name = "系统更新", Description = "安装安全补丁" }, 1);

            Console.WriteLine("任务执行顺序:");
            int order = 1;
            while (!scheduler.IsEmpty)
            {
                var task = scheduler.Dequeue();
                Console.WriteLine($"  {order++}. {task.Name} - {task.Description}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// 示例2: Dijkstra最短路径算法
        /// 使用优先队列优化最短路径查找
        /// </summary>
        static void DijkstraExample()
        {
            Console.WriteLine("--- 示例2: Dijkstra最短路径 ---\n");

            // 简单图: A-B-C-D
            var distances = new MinPriorityQueue<string>();
            var graph = new Dictionary<string, Dictionary<string, int>>
            {
                ["A"] = new() { ["B"] = 4, ["C"] = 2 },
                ["B"] = new() { ["A"] = 4, ["C"] = 1, ["D"] = 5 },
                ["C"] = new() { ["A"] = 2, ["B"] = 1, ["D"] = 8 },
                ["D"] = new() { ["B"] = 5, ["C"] = 8 }
            };

            // 初始化距离
            distances.Enqueue("A", 0);  // 起点到A的距离为0

            var visited = new HashSet<string>();
            var shortestPaths = new Dictionary<string, int>();

            Console.WriteLine("从节点A开始计算最短路径:");

            while (!distances.IsEmpty)
            {
                var element = distances.DequeueWithPriority();
                var node = element.Value;
                var dist = element.Priority;

                if (visited.Contains(node))
                    continue;

                visited.Add(node);
                shortestPaths[node] = dist;

                Console.WriteLine($"  节点 {node}: 最短距离 = {dist}");

                // 更新邻居距离
                if (graph.ContainsKey(node))
                {
                    foreach (var neighbor in graph[node])
                    {
                        if (!visited.Contains(neighbor.Key))
                        {
                            distances.Enqueue(neighbor.Key, dist + neighbor.Value);
                        }
                    }
                }
            }
            Console.WriteLine();
        }

        /// <summary>
        /// 示例3: 合并K个有序列表
        /// 经典优先队列应用
        /// </summary>
        static void MergeKSortedListsExample()
        {
            Console.WriteLine("--- 示例3: 合并K个有序列表 ---\n");

            // 3个有序列表
            var lists = new[]
            {
                new[] { 1, 4, 7, 10 },
                new[] { 2, 3, 8, 11 },
                new[] { 0, 5, 6, 9 }
            };

            Console.WriteLine("输入列表:");
            for (int i = 0; i < lists.Length; i++)
            {
                Console.WriteLine($"  列表{i + 1}: [{string.Join(", ", lists[i])}]");
            }

            // 使用优先队列合并
            var minHeap = new MinPriorityQueue<int>();
            foreach (var list in lists)
            {
                foreach (var num in list)
                {
                    minHeap.Enqueue(num, num);
                }
            }

            var merged = new List<int>();
            while (!minHeap.IsEmpty)
            {
                merged.Add(minHeap.Dequeue());
            }

            Console.WriteLine($"\n合并结果: [{string.Join(", ", merged)}]\n");
        }

        /// <summary>
        /// 示例4: 实时数据流处理
        /// 维护中位数
        /// </summary>
        static void DataStreamExample()
        {
            Console.WriteLine("--- 示例4: 数据流中位数 ---\n");

            var stream = new[] { 5, 15, 1, 3, 8, 7, 9, 10, 20, 12 };
            var maxHeap = new MaxPriorityQueue<int>();  // 存放较小的一半
            var minHeap = new MinPriorityQueue<int>();  // 存放较大的一半

            Console.WriteLine("数据流: " + string.Join(", ", stream));
            Console.WriteLine("\n实时中位数:");

            foreach (var num in stream)
            {
                // 添加到合适的堆
                if (maxHeap.IsEmpty || num <= maxHeap.Peek())
                {
                    maxHeap.Enqueue(num, num);
                }
                else
                {
                    minHeap.Enqueue(num, num);
                }

                // 平衡两个堆
                if (maxHeap.Count > minHeap.Count + 1)
                {
                    var val = maxHeap.Dequeue();
                    minHeap.Enqueue(val, val);
                }
                else if (minHeap.Count > maxHeap.Count + 1)
                {
                    var val = minHeap.Dequeue();
                    maxHeap.Enqueue(val, val);
                }

                // 计算中位数
                double median;
                if (maxHeap.Count == minHeap.Count)
                {
                    median = (maxHeap.Peek() + minHeap.Peek()) / 2.0;
                }
                else if (maxHeap.Count > minHeap.Count)
                {
                    median = maxHeap.Peek();
                }
                else
                {
                    median = minHeap.Peek();
                }

                Console.WriteLine($"  添加 {num,2} -> 中位数 = {median:F1}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// 示例5: 事件模拟
        /// 模拟事件按时间顺序发生
        /// </summary>
        static void EventSimulationExample()
        {
            Console.WriteLine("--- 示例5: 事件模拟系统 ---\n");

            var events = new MinPriorityQueue<SimulationEvent>();

            // 添加事件 (时间越早优先级越高)
            events.Enqueue(new SimulationEvent { Name = "客户到达", Time = 10.0 }, 10);
            events.Enqueue(new SimulationEvent { Name = "服务开始", Time = 12.0 }, 12);
            events.Enqueue(new SimulationEvent { Name = "另一个客户到达", Time = 15.0 }, 15);
            events.Enqueue(new SimulationEvent { Name = "服务结束", Time = 18.0 }, 18);
            events.Enqueue(new SimulationEvent { Name = "商店关门", Time = 20.0 }, 20);
            // 一个插队事件
            events.Enqueue(new SimulationEvent { Name = "紧急情况", Time = 11.5 }, 11);

            Console.WriteLine("事件按时间顺序发生:");
            double currentTime = 0;
            while (!events.IsEmpty)
            {
                var evt = events.DequeueWithPriority();
                Console.WriteLine($"  时间 {evt.Priority:F1}: {evt.Value.Name}");
                currentTime = evt.Priority;
            }
            Console.WriteLine($"  模拟结束，总时长: {currentTime:F1} 时间单位\n");
        }

        /// <summary>
        /// 示例6: Top K 问题
        /// 找出数据流中最大的K个元素
        /// </summary>
        static void TopKExample()
        {
            Console.WriteLine("--- 示例6: Top K 问题 ---\n");

            var data = new[] { 3, 1, 5, 2, 9, 7, 8, 4, 6, 10, 15, 12, 11, 14, 13 };
            int k = 5;

            Console.WriteLine($"数据: [{string.Join(", ", data)}]");
            Console.WriteLine($"找出最大的 {k} 个元素:");

            // 使用大小为K的最小堆
            var minHeap = new MinPriorityQueue<int>();
            
            foreach (var num in data)
            {
                minHeap.Enqueue(num, num);
                
                // 保持堆大小为K
                if (minHeap.Count > k)
                {
                    minHeap.Dequeue();  // 移除最小的
                }
            }

            // 收集结果
            var topK = new List<int>();
            while (!minHeap.IsEmpty)
            {
                topK.Add(minHeap.Dequeue());
            }
            topK.Sort((a, b) => b.CompareTo(a));  // 降序排列

            Console.WriteLine($"Top {k}: [{string.Join(", ", topK)}]\n");
        }
    }

    #region 辅助类型

    /// <summary>
    /// 任务
    /// </summary>
    public class Task
    {
        public string Name { get; set; }
        public string Description { get; set; }
    }

    /// <summary>
    /// 模拟事件
    /// </summary>
    public class SimulationEvent
    {
        public string Name { get; set; }
        public double Time { get; set; }
    }

    #endregion
}