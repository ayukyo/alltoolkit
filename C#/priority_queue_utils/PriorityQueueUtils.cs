using System;
using System.Collections.Generic;

namespace AllToolkit.PriorityQueueUtils
{
    /// <summary>
    /// 优先队列工具类 - 提供最小堆和最大堆优先队列实现
    /// 零依赖，仅使用 .NET 标准库
    /// </summary>
    
    /// <summary>
    /// 优先队列元素包装类
    /// </summary>
    /// <typeparam name="T">元素类型</typeparam>
    public class PriorityElement<T>
    {
        public T Value { get; }
        public int Priority { get; }

        public PriorityElement(T value, int priority)
        {
            Value = value;
            Priority = priority;
        }

        public override string ToString()
        {
            return $"[{Priority}] {Value}";
        }
    }

    /// <summary>
    /// 最小堆优先队列 - 优先级值越小越先出队
    /// </summary>
    /// <typeparam name="T">元素类型</typeparam>
    public class MinPriorityQueue<T>
    {
        private readonly List<PriorityElement<T>> _heap;

        public int Count => _heap.Count;
        public bool IsEmpty => _heap.Count == 0;

        public MinPriorityQueue()
        {
            _heap = new List<PriorityElement<T>>();
        }

        public MinPriorityQueue(int capacity)
        {
            _heap = new List<PriorityElement<T>>(capacity);
        }

        /// <summary>
        /// 入队 - 插入元素
        /// 时间复杂度: O(log n)
        /// </summary>
        public void Enqueue(T value, int priority)
        {
            var element = new PriorityElement<T>(value, priority);
            _heap.Add(element);
            SiftUp(_heap.Count - 1);
        }

        /// <summary>
        /// 出队 - 取出优先级最高的元素（优先级值最小）
        /// 时间复杂度: O(log n)
        /// </summary>
        public T Dequeue()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");

            var result = _heap[0].Value;
            var last = _heap[_heap.Count - 1];
            _heap.RemoveAt(_heap.Count - 1);

            if (_heap.Count > 0)
            {
                _heap[0] = last;
                SiftDown(0);
            }

            return result;
        }

        /// <summary>
        /// 出队 - 返回完整的元素（包含优先级信息）
        /// </summary>
        public PriorityElement<T> DequeueWithPriority()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");

            var result = _heap[0];
            var last = _heap[_heap.Count - 1];
            _heap.RemoveAt(_heap.Count - 1);

            if (_heap.Count > 0)
            {
                _heap[0] = last;
                SiftDown(0);
            }

            return result;
        }

        /// <summary>
        /// 查看队首元素（不移除）
        /// 时间复杂度: O(1)
        /// </summary>
        public T Peek()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");
            return _heap[0].Value;
        }

        /// <summary>
        /// 查看队首元素（包含优先级信息）
        /// </summary>
        public PriorityElement<T> PeekWithPriority()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");
            return _heap[0];
        }

        /// <summary>
        /// 尝试查看队首元素
        /// </summary>
        public bool TryPeek(out T value, out int priority)
        {
            if (IsEmpty)
            {
                value = default;
                priority = 0;
                return false;
            }

            value = _heap[0].Value;
            priority = _heap[0].Priority;
            return true;
        }

        /// <summary>
        /// 尝试出队
        /// </summary>
        public bool TryDequeue(out T value, out int priority)
        {
            if (IsEmpty)
            {
                value = default;
                priority = 0;
                return false;
            }

            var element = DequeueWithPriority();
            value = element.Value;
            priority = element.Priority;
            return true;
        }

        /// <summary>
        /// 清空队列
        /// </summary>
        public void Clear()
        {
            _heap.Clear();
        }

        /// <summary>
        /// 获取所有元素（不改变队列状态）
        /// </summary>
        public List<PriorityElement<T>> GetAll()
        {
            return new List<PriorityElement<T>>(_heap);
        }

        /// <summary>
        /// 检查是否包含指定值
        /// </summary>
        public bool Contains(T value)
        {
            foreach (var element in _heap)
            {
                if (EqualityComparer<T>.Default.Equals(element.Value, value))
                    return true;
            }
            return false;
        }

        /// <summary>
        /// 检查是否包含指定优先级的元素
        /// </summary>
        public bool Contains(T value, int priority)
        {
            foreach (var element in _heap)
            {
                if (element.Priority == priority && 
                    EqualityComparer<T>.Default.Equals(element.Value, value))
                    return true;
            }
            return false;
        }

        private void SiftUp(int index)
        {
            while (index > 0)
            {
                int parent = (index - 1) / 2;
                if (_heap[index].Priority >= _heap[parent].Priority)
                    break;

                Swap(index, parent);
                index = parent;
            }
        }

        private void SiftDown(int index)
        {
            int count = _heap.Count;
            while (true)
            {
                int left = 2 * index + 1;
                int right = 2 * index + 2;
                int smallest = index;

                if (left < count && _heap[left].Priority < _heap[smallest].Priority)
                    smallest = left;

                if (right < count && _heap[right].Priority < _heap[smallest].Priority)
                    smallest = right;

                if (smallest == index)
                    break;

                Swap(index, smallest);
                index = smallest;
            }
        }

        private void Swap(int i, int j)
        {
            var temp = _heap[i];
            _heap[i] = _heap[j];
            _heap[j] = temp;
        }
    }

    /// <summary>
    /// 最大堆优先队列 - 优先级值越大越先出队
    /// </summary>
    /// <typeparam name="T">元素类型</typeparam>
    public class MaxPriorityQueue<T>
    {
        private readonly List<PriorityElement<T>> _heap;

        public int Count => _heap.Count;
        public bool IsEmpty => _heap.Count == 0;

        public MaxPriorityQueue()
        {
            _heap = new List<PriorityElement<T>>();
        }

        public MaxPriorityQueue(int capacity)
        {
            _heap = new List<PriorityElement<T>>(capacity);
        }

        /// <summary>
        /// 入队 - 插入元素
        /// 时间复杂度: O(log n)
        /// </summary>
        public void Enqueue(T value, int priority)
        {
            var element = new PriorityElement<T>(value, priority);
            _heap.Add(element);
            SiftUp(_heap.Count - 1);
        }

        /// <summary>
        /// 出队 - 取出优先级最高的元素（优先级值最大）
        /// </summary>
        public T Dequeue()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");

            var result = _heap[0].Value;
            var last = _heap[_heap.Count - 1];
            _heap.RemoveAt(_heap.Count - 1);

            if (_heap.Count > 0)
            {
                _heap[0] = last;
                SiftDown(0);
            }

            return result;
        }

        /// <summary>
        /// 出队 - 返回完整的元素
        /// </summary>
        public PriorityElement<T> DequeueWithPriority()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");

            var result = _heap[0];
            var last = _heap[_heap.Count - 1];
            _heap.RemoveAt(_heap.Count - 1);

            if (_heap.Count > 0)
            {
                _heap[0] = last;
                SiftDown(0);
            }

            return result;
        }

        /// <summary>
        /// 查看队首元素
        /// </summary>
        public T Peek()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");
            return _heap[0].Value;
        }

        /// <summary>
        /// 查看队首元素（包含优先级信息）
        /// </summary>
        public PriorityElement<T> PeekWithPriority()
        {
            if (IsEmpty)
                throw new InvalidOperationException("Priority queue is empty");
            return _heap[0];
        }

        /// <summary>
        /// 尝试查看队首元素
        /// </summary>
        public bool TryPeek(out T value, out int priority)
        {
            if (IsEmpty)
            {
                value = default;
                priority = 0;
                return false;
            }

            value = _heap[0].Value;
            priority = _heap[0].Priority;
            return true;
        }

        /// <summary>
        /// 尝试出队
        /// </summary>
        public bool TryDequeue(out T value, out int priority)
        {
            if (IsEmpty)
            {
                value = default;
                priority = 0;
                return false;
            }

            var element = DequeueWithPriority();
            value = element.Value;
            priority = element.Priority;
            return true;
        }

        /// <summary>
        /// 清空队列
        /// </summary>
        public void Clear()
        {
            _heap.Clear();
        }

        /// <summary>
        /// 获取所有元素
        /// </summary>
        public List<PriorityElement<T>> GetAll()
        {
            return new List<PriorityElement<T>>(_heap);
        }

        /// <summary>
        /// 检查是否包含指定值
        /// </summary>
        public bool Contains(T value)
        {
            foreach (var element in _heap)
            {
                if (EqualityComparer<T>.Default.Equals(element.Value, value))
                    return true;
            }
            return false;
        }

        /// <summary>
        /// 检查是否包含指定优先级的元素
        /// </summary>
        public bool Contains(T value, int priority)
        {
            foreach (var element in _heap)
            {
                if (element.Priority == priority && 
                    EqualityComparer<T>.Default.Equals(element.Value, value))
                    return true;
            }
            return false;
        }

        private void SiftUp(int index)
        {
            while (index > 0)
            {
                int parent = (index - 1) / 2;
                if (_heap[index].Priority <= _heap[parent].Priority)
                    break;

                Swap(index, parent);
                index = parent;
            }
        }

        private void SiftDown(int index)
        {
            int count = _heap.Count;
            while (true)
            {
                int left = 2 * index + 1;
                int right = 2 * index + 2;
                int largest = index;

                if (left < count && _heap[left].Priority > _heap[largest].Priority)
                    largest = left;

                if (right < count && _heap[right].Priority > _heap[largest].Priority)
                    largest = right;

                if (largest == index)
                    break;

                Swap(index, largest);
                index = largest;
            }
        }

        private void Swap(int i, int j)
        {
            var temp = _heap[i];
            _heap[i] = _heap[j];
            _heap[j] = temp;
        }
    }

    /// <summary>
    /// 优先队列工具类 - 静态工厂方法
    /// </summary>
    public static class PriorityQueue
    {
        /// <summary>
        /// 创建最小堆优先队列
        /// </summary>
        public static MinPriorityQueue<T> CreateMinQueue<T>()
        {
            return new MinPriorityQueue<T>();
        }

        /// <summary>
        /// 创建指定容量的最小堆优先队列
        /// </summary>
        public static MinPriorityQueue<T> CreateMinQueue<T>(int capacity)
        {
            return new MinPriorityQueue<T>(capacity);
        }

        /// <summary>
        /// 创建最大堆优先队列
        /// </summary>
        public static MaxPriorityQueue<T> CreateMaxQueue<T>()
        {
            return new MaxPriorityQueue<T>();
        }

        /// <summary>
        /// 创建指定容量的最大堆优先队列
        /// </summary>
        public static MaxPriorityQueue<T> CreateMaxQueue<T>(int capacity)
        {
            return new MaxPriorityQueue<T>(capacity);
        }

        /// <summary>
        /// 从集合创建最小堆优先队列
        /// </summary>
        public static MinPriorityQueue<T> FromCollection<T>(IEnumerable<Tuple<T, int>> items)
        {
            var queue = new MinPriorityQueue<T>();
            foreach (var item in items)
            {
                queue.Enqueue(item.Item1, item.Item2);
            }
            return queue;
        }

        /// <summary>
        /// 从集合创建最大堆优先队列
        /// </summary>
        public static MaxPriorityQueue<T> FromCollectionMax<T>(IEnumerable<Tuple<T, int>> items)
        {
            var queue = new MaxPriorityQueue<T>();
            foreach (var item in items)
            {
                queue.Enqueue(item.Item1, item.Item2);
            }
            return queue;
        }

        /// <summary>
        /// 合并多个最小堆优先队列
        /// </summary>
        public static MinPriorityQueue<T> Merge<T>(params MinPriorityQueue<T>[] queues)
        {
            int totalCapacity = 0;
            foreach (var q in queues)
                totalCapacity += q.Count;

            var result = new MinPriorityQueue<T>(totalCapacity);
            foreach (var q in queues)
            {
                var elements = q.GetAll();
                foreach (var e in elements)
                    result.Enqueue(e.Value, e.Priority);
            }
            return result;
        }

        /// <summary>
        /// 合并多个最大堆优先队列
        /// </summary>
        public static MaxPriorityQueue<T> MergeMax<T>(params MaxPriorityQueue<T>[] queues)
        {
            int totalCapacity = 0;
            foreach (var q in queues)
                totalCapacity += q.Count;

            var result = new MaxPriorityQueue<T>(totalCapacity);
            foreach (var q in queues)
            {
                var elements = q.GetAll();
                foreach (var e in elements)
                    result.Enqueue(e.Value, e.Priority);
            }
            return result;
        }
    }
}